"""Drift-burst fade: the burst statistic and volume norm against independent implementations,
peak detection and fade side, the filters (side, volume gate, news zones), one trade a day, exits,
integrity checks (and that they catch tampered trades), look-ahead truncation, stress knobs, the
grid / lattice / local moves and the market config."""

from __future__ import annotations

from dataclasses import replace
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import polars as pl
import pytest

from src.analysis.neighborhood import LATTICE_DB_V1
from src.experiments.db_grid import AXES_DB_V1, db_grid_v1
from src.experiments.db_integrity import (
    check_sim_integrity,
    in_news,
    independent_tstat,
    independent_vnorm,
    truncation_invariance,
)
from src.experiments.funnel_config import load_funnel_config
from src.experiments.funnel_prep import build_dev_record, family_for
from src.experiments.funnel_robustness import local_perturbations_db, perturbations_db
from src.strategies.drift_burst.backtest import (
    EOD_EXIT,
    TIME_EXIT,
    DBData,
    DBParams,
    db_day_bars,
    signals,
    simulate_drift_burst,
)
from src.strategies.drift_burst.config import DriftBurstV1Config
from src.utils.config_models import ExecutionConfig

ROOT = Path(__file__).resolve().parents[2]
NY = ZoneInfo("America/New_York")
FUT = ExecutionConfig(starting_equity=1_000_000, instrument_type="futures", commission_per_contract=2.5,
                      slippage_ticks_market=1.0, slippage_ticks_stop=1.0, commission_per_share=0.0,
                      commission_minimum=0.0, slippage_bps_market=0.0, slippage_bps_stop=0.0)
TICK = 0.25
P = DBParams("ES", "1min", burst_window=5, threshold=4.0, vol_gate=None, side="both", hold=5, news_filter="off")


def _p(**kw) -> DBParams:
    return replace(P, **kw)


def _bars(n_days=30, start=date(2021, 6, 7), seed=0, sigma=0.5, bursts=None, vol=1000,
          extra_rth=False) -> pl.DataFrame:
    """1-minute ES-like bars 09:30-15:59 NY (plus 08:00-09:29 non-RTH bars if extra_rth).
    `bursts`: {(day_index, minute_of_session): (size_points, volume_multiplier, n_minutes)} adds
    a steady move of size/n per minute for n minutes with volume x multiplier."""
    rng = np.random.default_rng(seed)
    rows, d, px, made = [], start, 4000.0, 0
    bursts = bursts or {}
    while made < n_days:
        if d.weekday() < 5:
            first = 8 * 60 if extra_rth else 9 * 60 + 30
            active: dict[int, tuple[float, float]] = {}
            for (di, m0), (size, vm, nmin) in bursts.items():
                if di == made:
                    for j in range(nmin):
                        active[m0 + j] = (size / nmin, vm)
            for t in range(first, 16 * 60):
                ny = datetime(d.year, d.month, d.day, t // 60, t % 60, tzinfo=NY)
                m = t - (9 * 60 + 30)
                step, vm = active.get(m, (0.0, 1.0))
                o = px
                c = px + step + float(rng.normal(0, sigma))
                rows.append({"bar_open_ts": ny.astimezone(ZoneInfo("UTC")), "bar_open_ts_ny": ny, "session_date_ny": d,
                             "open": o, "high": max(o, c) + 0.25, "low": min(o, c) - 0.25, "close": c,
                             "volume": int(vol * vm * (1 + 0.1 * rng.random())), "price_adjustment": 0.0,
                             "is_regular_session": t >= 9 * 60 + 30})
                px = c
            made += 1
        d += timedelta(days=1)
    return pl.DataFrame(rows).with_columns(pl.col("bar_open_ts").dt.convert_time_zone("UTC"),
                                           pl.col("bar_open_ts_ny").dt.convert_time_zone("America/New_York"))


def _data(**kw) -> DBData:
    return DBData(db_day_bars(_bars(**kw)))


# --- statistic and volume norm -----------------------------------------------------------------

def test_tstat_and_vnorm_match_independent_implementations():
    d = _data(n_days=25, seed=1, sigma=0.7)
    for k in (3, 5, 10):
        a, b = d.tstat(k), independent_tstat(d, k)
        assert np.array_equal(np.isfinite(a), np.isfinite(b))
        assert np.allclose(a[np.isfinite(a)], b[np.isfinite(b)], rtol=1e-9)
        # The first 6k minutes of every session have no statistic.
        assert not np.isfinite(a[d.pos < 6 * k]).any()
    assert np.allclose(d.vnorm(), independent_vnorm(d), equal_nan=True)
    assert not np.isfinite(d.vnorm()[d.sess < 10]).any() and np.isfinite(d.vnorm()[d.sess >= 10]).all()


def test_tstat_hand_calculation():
    d = _data(n_days=1, seed=2)
    k, i = 3, 40
    lc = np.log(d.close)
    r = np.diff(lc)[i - k - 15:i - k]                 # returns of bars i-k-14 .. i-k
    s = np.sqrt(np.mean(r ** 2))
    assert d.tstat(k)[i] == pytest.approx((lc[i] - lc[i - k]) / (s * np.sqrt(k)))


def test_day_bars_keep_only_the_regular_session():
    b = db_day_bars(_bars(n_days=2, extra_rth=True))
    assert b.height == 2 * 390 and b["is_regular_session"].all()
    with pytest.raises(ValueError):
        db_day_bars(_bars(n_days=1), timeframe="5min")


# --- signals and trades ------------------------------------------------------------------------

def _burst_data(size=-25.0, vm=4.0, day=12, minute=120, n_days=15, nmin=4, **kw):
    return _data(n_days=n_days, bursts={(day, minute): (size, vm, nmin)}, **kw)


def test_drop_burst_is_faded_long_after_peak():
    d = _burst_data()
    s = simulate_drift_burst(d, P, exec_config=FUT, starting_equity=1e6)
    day = np.flatnonzero(d.session_date[s.entry_idx] == d.days[12])
    assert len(day) == 1
    i = int(day[0])
    t, e = int(s.signal_idx[i]), int(s.entry_idx[i])
    T = d.tstat(5)
    assert s.side[i] == 1 and T[t - 1] < -4.0
    assert not np.isfinite(T[t]) or np.sign(T[t]) != np.sign(T[t - 1]) or abs(T[t]) < abs(T[t - 1])
    assert e == t + 1 and s.entry_px[i] == pytest.approx(d.open[e] + TICK)
    assert s.exit_idx[i] == e + 4 and s.exit_reason[i] == TIME_EXIT
    assert s.exit_px[i] == pytest.approx(d.close[e + 4] - TICK)
    assert check_sim_integrity(s, d, FUT, P) == []


def test_spike_is_faded_short_and_long_only_skips_it():
    d = _burst_data(size=25.0)
    s = simulate_drift_burst(d, P, exec_config=FUT, starting_equity=1e6)
    on_day = s.side[d.session_date[s.entry_idx] == d.days[12]]
    assert list(on_day) == [-1]
    lo = simulate_drift_burst(d, _p(side="long_only"), exec_config=FUT, starting_equity=1e6)
    assert (lo.side > 0).all() and not (d.session_date[lo.entry_idx] == d.days[12]).any()


def test_volume_gate():
    quiet = _burst_data(vm=1.0)
    loud = _burst_data(vm=4.0)
    p = _p(vol_gate=2.0)
    on12 = lambda d, s: (d.session_date[s.entry_idx] == d.days[12]).any()  # noqa: E731
    assert not on12(quiet, simulate_drift_burst(quiet, p, exec_config=FUT, starting_equity=1e6))
    s = simulate_drift_burst(loud, p, exec_config=FUT, starting_equity=1e6)
    assert on12(loud, s) and check_sim_integrity(s, loud, FUT, p) == []


def test_news_filter_blocks_bursts_near_10am():
    d = _burst_data(minute=28)          # 09:58-10:01 burst
    p_on = _p(news_filter="on")
    assert any(d.session_date[simulate_drift_burst(d, P, exec_config=FUT, starting_equity=1e6).entry_idx] == d.days[12])
    s = simulate_drift_burst(d, p_on, exec_config=FUT, starting_equity=1e6)
    assert not (d.session_date[s.entry_idx] == d.days[12]).any()
    assert check_sim_integrity(s, d, FUT, p_on) == []
    i = int(np.flatnonzero((d.session_date == d.days[12]) & (d.tod == 10 * 60 + 2))[0])
    assert in_news(d, 5, i) and d.news_blocked(5)[i]


def test_wednesday_zone_only_on_wednesdays():
    d = _data(n_days=5, start=date(2021, 6, 7))          # Mon..Fri
    wed = d.weekday == 2
    at = (d.tod == 14 * 60 + 10)
    assert (d.news_blocked(5)[wed & at]).all() and not (d.news_blocked(5)[~wed & at]).any()


def test_one_trade_per_session_and_hold_to_close():
    d = _data(n_days=15, bursts={(12, 120): (-25.0, 4.0, 4), (12, 200): (-25.0, 4.0, 4)})
    s = simulate_drift_burst(d, _p(hold=30), exec_config=FUT, starting_equity=1e6)
    assert (d.session_date[s.entry_idx] == d.days[12]).sum() == 1
    late = _data(n_days=15, bursts={(12, 375): (-30.0, 4.0, 4)})
    s2 = simulate_drift_burst(late, _p(hold=30), exec_config=FUT, starting_equity=1e6)
    i = np.flatnonzero(late.session_date[s2.entry_idx] == late.days[12])
    assert len(i) == 1 and s2.exit_reason[i[0]] == EOD_EXIT and s2.exit_idx[i[0]] == late.sess_end[s2.exit_idx[i[0]]]
    assert check_sim_integrity(s2, late, FUT, _p(hold=30)) == []


# --- integrity ---------------------------------------------------------------------------------

def test_integrity_clean_across_the_grid():
    d = _data(n_days=40, seed=4, sigma=1.0, bursts={(15, 100): (-30, 4, 3), (22, 200): (30, 3, 5),
                                                     (30, 60): (-20, 2, 8), (35, 150): (25, 5, 2)})
    for ce in db_grid_v1(("ES",))[::5]:
        s = simulate_drift_burst(d, ce.config, exec_config=FUT, starting_equity=1e6)
        assert check_sim_integrity(s, d, FUT, ce.config) == [], ce.config


def test_integrity_catches_tampered_trades():
    d = _data(n_days=20, bursts={(12, 120): (-25.0, 4.0, 4), (15, 150): (25.0, 4.0, 4)})
    s = simulate_drift_burst(d, P, exec_config=FUT, starting_equity=1e6)
    assert len(s.entry_idx) >= 2 and check_sim_integrity(s, d, FUT, P) == []
    j = int(np.flatnonzero(d.session_date[s.entry_idx] == d.days[12])[0])

    t = replace(s, side=s.side.copy())
    t.side[j] = -t.side[j]
    assert "side_not_fade" in check_sim_integrity(t, d, FUT, P)

    t = replace(s, signal_idx=s.signal_idx.copy())
    t.signal_idx[j] -= 30
    assert "peak_below_threshold" in check_sim_integrity(t, d, FUT, P)

    t = replace(s, entry_px=s.entry_px.copy())
    t.entry_px[j] = d.open[s.entry_idx[j]] - TICK         # a long filled below the open
    assert "entry_fill_better_than_market" in check_sim_integrity(t, d, FUT, P)

    t = replace(s, exit_idx=s.exit_idx.copy())
    t.exit_idx[j] += 2
    assert "time_exit_not_per_rule" in check_sim_integrity(t, d, FUT, P)

    keep = np.arange(len(s.entry_idx)) != j
    t = replace(s, **{k: getattr(s, k)[keep] for k in ("signal_idx", "entry_idx", "exit_idx", "decision_idx",
                                                       "quantity", "entry_px", "exit_px", "entry_commission",
                                                       "realized_pnl", "forced_close", "exit_reason", "stop_level",
                                                       "entry_base", "side", "peak_t")})
    assert "signal_skipped_while_flat" in check_sim_integrity(t, d, FUT, P)

    t = replace(s, quantity=s.quantity * 100)
    assert "position_exceeds_equity" in check_sim_integrity(t, d, FUT, P)

    assert "volume_gate_not_met" in check_sim_integrity(s, d, FUT, _p(vol_gate=50.0))


def test_no_lookahead_under_truncation():
    b = db_day_bars(_bars(n_days=40, seed=5, sigma=1.0, bursts={(15, 100): (-30, 4, 3), (22, 200): (30, 3, 5),
                                                                 (30, 60): (-20, 2, 8), (35, 150): (25, 5, 2)}))
    for p in (P, _p(burst_window=10, threshold=3.5, vol_gate=1.5, news_filter="on", hold=30),
              _p(burst_window=3, side="long_only", hold=15)):
        assert truncation_invariance(b, p, exec_config=FUT, cut_fracs=(0.3, 0.55, 0.8, 0.97)) == []


def test_stress_knobs():
    d = _data(n_days=30, seed=6, sigma=1.0, bursts={(15, 100): (-30, 4, 3), (22, 200): (30, 3, 5)})
    p = _p(threshold=3.5)
    base = simulate_drift_burst(d, p, exec_config=FUT, starting_equity=1e6)
    late = simulate_drift_burst(d, p, exec_config=FUT, starting_equity=1e6, entry_delay_bars=1)
    assert len(base.entry_idx) >= 2 and (late.entry_idx[:2] == base.entry_idx[:2] + 1).all()
    miss = simulate_drift_burst(d, p, exec_config=FUT, starting_equity=1e6, missed_entry_frac=0.5, stress_seed=3)
    assert len(miss.entry_idx) <= len(base.entry_idx)


# --- grid, lattice, local moves, config --------------------------------------------------------

def test_grid_and_lattice():
    g = db_grid_v1(("ES",))
    assert len(g) == 576 and len({c.config_id for c in g}) == 576
    for ax, vals in LATTICE_DB_V1.ordered.items():
        assert set(vals) == set(AXES_DB_V1[ax])


def test_local_and_random_perturbations():
    cfg = load_funnel_config(ROOT / "configs/funnel/db_funnel_es_v1.yaml")
    lc = cfg.parameter_stability.local
    moves = dict(local_perturbations_db(_p(burst_window=5, hold=15, threshold=4.0, vol_gate=2.0), lc))
    assert set(moves) == {"burst_window=4", "burst_window=6", "hold=12", "hold=18", "threshold=3.75",
                          "threshold=4.25", "vol_gate=1.75", "vol_gate=2.25"}
    assert "vol_gate=1.75" not in dict(local_perturbations_db(P, lc))
    d = _burst_data()
    for _, mp in moves.items():
        s = simulate_drift_burst(d, mp, exec_config=FUT, starting_equity=1e6)
        assert check_sim_integrity(s, d, FUT, mp) == []
    ps = perturbations_db(_p(vol_gate=2.0), config_id="x", base_seed=1, pcfg=cfg.parameter_stability.perturbation)
    assert len(ps) == 20 and all(q.side == "both" and q.burst_window >= 2 for q in ps)


def test_funnel_config_and_family_wiring():
    cfg = load_funnel_config(ROOT / "configs/funnel/db_funnel_es_v1.yaml")
    assert cfg.strategy == "drift_burst_v1" and cfg.symbol == "ES" and cfg.confidence.transfer_symbol == "NQ"
    assert family_for(cfg).simulate is simulate_drift_burst
    d = _burst_data()
    rec, rets = build_dev_record(db_grid_v1(("ES",))[0], d, fcfg=cfg, exec_config=FUT)
    assert rec["integrity_issues"] == "" and len(rets) == len(d.days)


def test_config_rejects_off_grid_values():
    with pytest.raises(Exception):
        DriftBurstV1Config(symbol="ES", threshold=4.2)
    with pytest.raises(Exception):
        DriftBurstV1Config(symbol="ES", side="short_only")
    assert signals(_data(n_days=1), P)["k"].dtype == np.int64


# --- v2: entry modes, target / stop, trade cap -------------------------------------------------

from src.experiments.db_grid import AXES_DB_V2, db_grid_v2  # noqa: E402
from src.analysis.neighborhood import LATTICE_DB_V2  # noqa: E402
from src.strategies.drift_burst.backtest import STOP_EXIT, TARGET_EXIT  # noqa: E402
from src.strategies.drift_burst.config import DriftBurstV2Config  # noqa: E402


def test_v2_defaults_reproduce_v1_exactly():
    d = _data(n_days=40, seed=4, sigma=1.0, bursts={(15, 100): (-30, 4, 3), (22, 200): (30, 3, 5)})
    for ce in db_grid_v1(("ES",))[::11]:
        v1 = simulate_drift_burst(d, ce.config, exec_config=FUT, starting_equity=1e6)
        c = ce.config
        if c.news_filter != "off":
            continue
        v2 = simulate_drift_burst(d, DriftBurstV2Config(symbol="ES", burst_window=c.burst_window, threshold=c.threshold,
                                                        vol_gate=c.vol_gate, side=c.side, hold=c.hold),
                                  exec_config=FUT, starting_equity=1e6)
        assert np.array_equal(v1.entry_idx, v2.entry_idx) and np.allclose(v1.realized_pnl, v2.realized_pnl)


def test_entry_modes_are_zero_one_two_bars_after_the_reference_bar():
    d = _burst_data(size=-30.0, nmin=6)
    T = d.tstat(5)
    ents = {}
    for mode in ("cross", "peak", "confirm"):
        s = simulate_drift_burst(d, _p(entry_mode=mode), exec_config=FUT, starting_equity=1e6)
        i = int(np.flatnonzero(d.session_date[s.entry_idx] == d.days[12])[0])
        ents[mode] = int(s.signal_idx[i])
        assert check_sim_integrity(s, d, FUT, _p(entry_mode=mode)) == []
    t = ents["cross"]
    assert abs(T[t]) > 4.0 and not abs(T[t - 1]) > 4.0          # fresh cross
    assert ents["cross"] < ents["peak"] <= ents["confirm"]


def test_target_and_stop_fills():
    d = _data(n_days=40, seed=7, sigma=1.5, bursts={(15, 100): (-30, 4, 3), (22, 200): (30, 3, 5),
                                                     (30, 60): (-25, 4, 3), (35, 150): (25, 5, 2)})
    p = _p(threshold=3.5, target=0.5, stop=1.0, max_trades=3, hold=30)
    s = simulate_drift_burst(d, p, exec_config=FUT, starting_equity=1e6)
    assert check_sim_integrity(s, d, FUT, p) == []
    reasons = set(s.exit_reason)
    assert TARGET_EXIT in reasons or STOP_EXIT in reasons
    for i in range(len(s.entry_idx)):
        e, x, dd = s.entry_idx[i], s.exit_idx[i], s.side[i]
        assert s.target_level[i] == pytest.approx(d.open[e] + dd * 0.5 * s.burst_pts[i])
        assert s.stop_level[i] == pytest.approx(d.open[e] - dd * 1.0 * s.burst_pts[i])
        if s.exit_reason[i] == TARGET_EXIT:
            best = max(d.open[x], s.target_level[i]) if dd > 0 else min(d.open[x], s.target_level[i])
            assert s.exit_px[i] == pytest.approx(best - dd * TICK)
        if s.exit_reason[i] == STOP_EXIT:
            worst = min(d.open[x], s.stop_level[i]) if dd > 0 else max(d.open[x], s.stop_level[i])
            assert s.exit_px[i] == pytest.approx(worst - dd * TICK)


def test_trade_cap_per_session():
    d = _data(n_days=15, bursts={(12, 120): (-25.0, 4.0, 4), (12, 200): (-25.0, 4.0, 4), (12, 280): (25.0, 4.0, 4)})
    one = simulate_drift_burst(d, _p(max_trades=1), exec_config=FUT, starting_equity=1e6)
    three = simulate_drift_burst(d, _p(max_trades=3), exec_config=FUT, starting_equity=1e6)
    day = lambda s: int((d.session_date[s.entry_idx] == d.days[12]).sum())  # noqa: E731
    assert day(one) == 1 and 2 <= day(three) <= 3
    assert check_sim_integrity(three, d, FUT, _p(max_trades=3)) == []
    assert "too_many_trades_in_session" in check_sim_integrity(three, d, FUT, _p(max_trades=1))


def test_v2_integrity_catches_tampered_stop_and_target():
    d = _data(n_days=40, seed=7, sigma=1.5, bursts={(15, 100): (-30, 4, 3), (22, 200): (30, 3, 5)})
    p = _p(threshold=3.5, target=0.5, stop=1.0, hold=30)
    s = simulate_drift_burst(d, p, exec_config=FUT, starting_equity=1e6)
    assert len(s.entry_idx) and check_sim_integrity(s, d, FUT, p) == []
    t = replace(s, stop_level=s.stop_level + 1.0)
    assert "stop_not_per_rule" in check_sim_integrity(t, d, FUT, p)
    t = replace(s, target_level=s.target_level + 1.0)
    assert "target_not_per_rule" in check_sim_integrity(t, d, FUT, p)
    t = replace(s, exit_reason=np.array(["target_exit"] * len(s.entry_idx), dtype=object))
    issues = check_sim_integrity(t, d, FUT, p)
    assert issues and set(issues) & {"target_exit_without_touch", "target_fill_better_than_rule", "time_exit_not_per_rule"}


def test_v2_no_lookahead_under_truncation():
    b = db_day_bars(_bars(n_days=40, seed=8, sigma=1.5, bursts={(15, 100): (-30, 4, 3), (22, 200): (30, 3, 5),
                                                                 (30, 60): (-25, 4, 3), (35, 150): (25, 5, 2)}))
    for p in (_p(entry_mode="cross", target=0.5, stop=1.0, max_trades=3, threshold=3.5),
              _p(entry_mode="confirm", target=1.0, max_trades=3, burst_window=3, hold=30)):
        assert truncation_invariance(b, p, exec_config=FUT, cut_fracs=(0.3, 0.55, 0.8, 0.97)) == []


def test_v2_grid_lattice_and_local_moves():
    g = db_grid_v2(("ES",))
    assert len(g) == 10_368 and len({c.config_id for c in g}) == 10_368
    for ax, vals in LATTICE_DB_V2.ordered.items():
        assert set(vals) == set(AXES_DB_V2[ax])
    cfg = load_funnel_config(ROOT / "configs/funnel/db_funnel_es_v2.yaml")
    assert cfg.strategy == "drift_burst_v2"
    moves = dict(local_perturbations_db(_p(target=0.5, stop=1.0, max_trades=3), cfg.parameter_stability.local))
    assert {"target=0.25", "target=0.75", "stop=0.75", "stop=1.25", "max_trades=2", "max_trades=4"} <= set(moves)
    # v1's config sets no v2 steps, so v1 runs never move the v2 axes.
    v1 = load_funnel_config(ROOT / "configs/funnel/db_funnel_es_v1.yaml").parameter_stability.local
    assert not any(k.startswith(("target", "stop", "max_trades")) for k in dict(local_perturbations_db(P, v1)))
    d = _burst_data()
    for _, mp in moves.items():
        assert check_sim_integrity(simulate_drift_burst(d, mp, exec_config=FUT, starting_equity=1e6), d, FUT, mp) == []
