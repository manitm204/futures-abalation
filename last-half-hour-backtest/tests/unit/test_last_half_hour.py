"""Last-half-hour momentum: the RTH bar window, the signals against hand-computed values, the
direction, the filters (z, rv_high, down_only) and the agreement check, entries / exits / stops
on both sides, early closes, the side override, integrity checks (and that they catch tampered
trades), look-ahead truncation, the grid / lattice / local moves and the market config."""

from __future__ import annotations

from dataclasses import replace
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import polars as pl
import pytest

from src.analysis.neighborhood import LATTICE_LH_V1
from src.data.calendars import TradingCalendar
from src.experiments.funnel_config import load_funnel_config
from src.experiments.funnel_prep import build_dev_record, family_for
from src.experiments.funnel_robustness import local_perturbations_lh, perturbations_lh
from src.experiments.lh_grid import AXES_LH_V1, lh_grid_v1
from src.experiments.lh_integrity import check_sim_integrity, truncation_invariance
from src.strategies.last_half_hour.backtest import (
    EOD_EXIT,
    STOP_EXIT,
    TIME_EXIT,
    LHData,
    LHParams,
    lh_day_bars,
    session_side,
    simulate_last_half_hour,
)
from src.strategies.last_half_hour.config import LastHalfHourV1Config, parse_filter, window_minutes
from src.utils.config_models import ExecutionConfig

ROOT = Path(__file__).resolve().parents[2]
NY = ZoneInfo("America/New_York")
FUT = ExecutionConfig(starting_equity=1_000_000, instrument_type="futures", commission_per_contract=2.5,
                      slippage_ticks_market=1.0, slippage_ticks_stop=1.0, commission_per_share=0.0,
                      commission_minimum=0.0, slippage_bps_market=0.0, slippage_bps_stop=0.0)
TICK = 0.25
P = LHParams("NQ", "1min", signal="prev_close", agree=False, entry_min=15 * 60 + 30, exit_min=16 * 60,
             filter="none")
CAL = TradingCalendar()


def _p(**kw) -> LHParams:
    return replace(P, **kw)


def _bars(start=date(2021, 1, 4), end=date(2021, 6, 30), seed=0, vol=2.0, first="08:00", last="17:59",
          drop: set[tuple[date, int]] | None = None, stop_at: dict[date, int] | None = None) -> pl.DataFrame:
    """1-minute NQ-like bars on NYSE trading days from `first` to `last` NY (inclusive), random
    walk. `drop` removes (date, NY minute) bars; `stop_at` ends a day's bars early."""
    rng = np.random.default_rng(seed)
    h0, m0 = map(int, first.split(":"))
    h1, m1 = map(int, last.split(":"))
    rows, px = [], 13000.0
    for d in CAL.trading_days(start, end):
        t_end = min(h1 * 60 + m1, (stop_at or {}).get(d, 10 ** 6))
        for t in range(h0 * 60 + m0, t_end + 1):
            if drop and (d, t) in drop:
                continue
            ny = datetime(d.year, d.month, d.day, t // 60, t % 60, tzinfo=NY)
            o = px
            c = round((px + float(rng.normal(0, vol))) / TICK) * TICK
            rows.append({"bar_open_ts": ny.astimezone(ZoneInfo("UTC")), "bar_open_ts_ny": ny, "session_date_ny": d,
                         "open": o, "high": max(o, c) + TICK, "low": min(o, c) - TICK, "close": c,
                         "volume": 100, "price_adjustment": 0.0})
            px = c
    df = pl.DataFrame(rows)
    return df.with_columns(pl.col("bar_open_ts").dt.convert_time_zone("UTC"),
                           pl.col("bar_open_ts_ny").dt.convert_time_zone("America/New_York"))


@pytest.fixture(scope="module")
def data() -> LHData:
    return LHData(lh_day_bars(_bars()))


def _sim(data, p):
    return simulate_last_half_hour(data, p, exec_config=FUT, starting_equity=FUT.starting_equity)


# --- bars and signals ---------------------------------------------------------------------------

def test_bar_window_is_rth_only(data):
    assert data.tod.min() == 9 * 60 + 30 and data.tod.max() == 15 * 60 + 59
    assert (data.tod[data.day_start_idx] == 570).all()


def test_signals_match_hand_computation(data):
    s = 10
    a, b = data.day_start_idx[s], data.day_end_idx[s]
    prev = data.close[data.day_end_idx[s - 1]]
    i1529 = a + (15 * 60 + 29 - 570)
    i0959 = a + (9 * 60 + 59 - 570)
    assert data.tod[i1529] == 15 * 60 + 29 and data.tod[i0959] == 9 * 60 + 59
    assert data.signal("prev_close", 930)[s] == pytest.approx(data.close[i1529] / prev - 1)
    assert data.signal("open", 930)[s] == pytest.approx(data.close[i1529] / data.open[a] - 1)
    assert data.signal("first_half", 930)[s] == pytest.approx(data.close[i0959] / prev - 1)
    assert np.isnan(data.signal("prev_close", 930)[0])   # no previous session


def test_direction_follows_signal(data):
    sim = _sim(data, P)
    r = data.signal("prev_close", 930)
    sess = data.sess[sim.entry_idx]
    assert len(sim.entry_idx) > 100
    assert (sim.side == np.sign(r[sess])).all()
    assert (sim.side > 0).any() and (sim.side < 0).any()
    assert (data.tod[sim.entry_idx] == 930).all()
    assert (sim.signal_idx == sim.entry_idx - 1).all()
    assert (sim.exit_idx == data.day_end_idx[sess]).all()
    assert set(sim.exit_reason[:-1]) == {EOD_EXIT} and sim.exit_reason[-1] == "forced_close"


def test_time_exit_before_close(data):
    sim = _sim(data, _p(exit_min=15 * 60 + 50))
    assert (data.tod[sim.exit_idx] == 15 * 60 + 49).all()
    assert set(sim.exit_reason) == {TIME_EXIT}


def test_filters(data):
    base = session_side(data, P)
    r = data.signal("prev_close", 930)
    down = session_side(data, _p(filter="down_only"))
    assert (down <= 0).all() and ((down < 0) == (r < 0)).all()
    z = session_side(data, _p(filter="z", z=1.0))
    sg = data.sigma("prev_close", 930)
    s = 40
    w = r[s - 20:s]
    assert sg[s] == pytest.approx(np.std(w[np.isfinite(w)], ddof=1))
    assert ((z != 0) <= (base != 0)).all()
    assert ((z != 0) == (np.isfinite(sg) & (np.abs(np.nan_to_num(r)) > 1.0 * np.nan_to_num(sg, nan=np.inf)))).all()
    agree = session_side(data, _p(agree=True))
    fh = data.first_half()
    assert ((agree != 0) == ((base != 0) & (np.sign(fh) == np.sign(r)))).all()
    rv = session_side(data, _p(filter="rv_high"))
    assert (rv != 0).sum() > 0 and (rv != 0).sum() < (base != 0).sum()
    assert (rv[:80] == 0).all()   # warm-up: 20 returns + 60 RV values


def test_stops_both_sides(data):
    sim = _sim(data, _p(stop_pct=0.02))
    st = sim.exit_reason == STOP_EXIT
    assert st.any()
    for i in np.flatnonzero(st):
        e, x, sd = sim.entry_idx[i], sim.exit_idx[i], sim.side[i]
        stop = data.open[e] * (1 - sd * 0.02 / 100)
        assert sim.stop_level[i] == pytest.approx(stop)
        assert (data.low[x] <= stop) if sd > 0 else (data.high[x] >= stop)
    assert check_sim_integrity(sim, data, FUT, _p(stop_pct=0.02)) == []
    shorts = st & (sim.side < 0)
    assert shorts.any()


def test_short_pnl_sign(data):
    sim = _sim(data, _p(filter="down_only"))
    assert (sim.side == -1).all()
    t = sim.trades[0]
    assert t.entry_fill.fill_price == data.open[sim.entry_idx[0]] - TICK          # sell 1 tick lower
    assert t.exit_fill.fill_price == data.close[sim.exit_idx[0]] + TICK           # buy back 1 tick higher
    assert t.realized_pnl == pytest.approx((t.entry_fill.fill_price - t.exit_fill.fill_price) * t.quantity
                                           - t.commission_total)


def test_early_close_and_gap_skip():
    d0 = date(2021, 3, 1)
    bars = _bars(stop_at={d0: 13 * 60}, drop={(date(2021, 3, 2), 15 * 60 + 29), (date(2021, 3, 2), 15 * 60 + 28),
                                             (date(2021, 3, 2), 15 * 60 + 27)})
    data = LHData(lh_day_bars(bars))
    sim = _sim(data, P)
    days = set(data.session_date[sim.entry_idx].astype(object))
    assert d0 not in days                    # early close: no 15:30 bar
    assert date(2021, 3, 2) not in days      # decision bar too stale (15:26)
    assert check_sim_integrity(sim, data, FUT, P) == []


def test_side_override(data):
    sim = _sim(data, P)
    flip = -sim.side
    sim2 = simulate_last_half_hour(data, P, exec_config=FUT, starting_equity=FUT.starting_equity, side_override=flip)
    assert (sim2.side == flip).all() and (sim2.entry_idx == sim.entry_idx).all()


# --- integrity ----------------------------------------------------------------------------------

@pytest.mark.parametrize("cfg", [P, _p(agree=True, filter="z", z=0.5), _p(signal="open", filter="rv_high"),
                                 _p(signal="first_half", filter="down_only", stop_pct=0.05),
                                 _p(entry_min=15 * 60, exit_min=15 * 60 + 50)])
def test_integrity_clean(data, cfg):
    assert check_sim_integrity(_sim(data, cfg), data, FUT, cfg) == []


def test_integrity_catches_tampering(data):
    sim = _sim(data, P)
    sim.side = sim.side.copy(); sim.side[3] *= -1
    assert "wrong_direction" in check_sim_integrity(sim, data, FUT, P)
    sim = _sim(data, P)
    sim.entry_px = sim.entry_px.copy(); sim.entry_px[2] -= 5 * sim.side[2]
    assert "entry_fill_better_than_market" in check_sim_integrity(sim, data, FUT, P)
    sim = _sim(data, _p(filter="down_only"))
    assert check_sim_integrity(sim, data, FUT, P) != []   # skipped up days


def test_truncation_invariance():
    bars = lh_day_bars(_bars(end=date(2021, 4, 30)))
    for cfg in (P, _p(filter="z", z=0.5, stop_pct=0.05), _p(signal="open", agree=True, filter="rv_high")):
        assert truncation_invariance(bars, cfg, exec_config=FUT) == []


# --- grid / lattice / moves / config ------------------------------------------------------------

def test_grid():
    g = lh_grid_v1(("NQ",))
    assert len(g) == 500
    assert not any(c.config.signal == "first_half" and c.config.agree == "on" for c in g)
    assert set(AXES_LH_V1["window"]) == set(LATTICE_LH_V1.ordered["window"])
    p = LHParams.from_config(LastHalfHourV1Config(symbol="NQ", window="15:45-16:00", filter="z1.0", stop="0.20"))
    assert (p.entry_min, p.exit_min, p.filter, p.z, p.stop_pct) == (945, 960, "z", 1.0, 0.2)
    assert window_minutes("15:30-15:50") == (930, 950) and parse_filter("rv_high") == ("rv_high", None)


def test_local_moves():
    f = load_funnel_config(ROOT / "configs/funnel/lh_funnel_nq_v1.yaml")
    moves = dict(local_perturbations_lh(_p(filter="z", z=0.5, stop_pct=0.1), f.parameter_stability.local))
    assert set(moves) == {"entry=15:25", "entry=15:35", "exit=15:55", "z=0.25", "z=0.75", "stop_pct=0.05",
                          "stop_pct=0.15"}
    moves = dict(local_perturbations_lh(_p(entry_min=950, exit_min=960), f.parameter_stability.local))
    assert set(moves) == {"entry=15:45", "entry=15:55", "exit=15:55"}
    for p in perturbations_lh(_p(filter="z", z=1.0), config_id="x", base_seed=1, pcfg=f.parameter_stability.perturbation):
        assert p.exit_min <= 960 and p.entry_min <= p.exit_min - 5 and p.z != 1.0


def test_family_record(data):
    f = load_funnel_config(ROOT / "configs/funnel/lh_funnel_nq_v1.yaml")
    assert family_for(f).simulate is simulate_last_half_hour
    ce = lh_grid_v1(("NQ",))[7]
    f2 = f.model_copy(update={"data": f.data.model_copy(update={
        "development": f.data.development.model_copy(update={"start": date(2021, 1, 1), "end": date(2021, 6, 30)})})})
    rec, rets = build_dev_record(ce, data, fcfg=f2, exec_config=FUT)
    assert rec["integrity_issues"] == "" and len(rets) == len(data.days)


def test_session_sides_replace_signal(data):
    sides = np.zeros(len(data.days), dtype=np.int64)
    sides[[5, 6, 9]] = [1, -1, 1]
    cfg = _p(filter="z", z=5.0, agree=True)   # the filter would trade almost nothing
    sim = simulate_last_half_hour(data, cfg, exec_config=FUT, starting_equity=FUT.starting_equity, session_sides=sides)
    assert list(data.sess[sim.entry_idx]) == [5, 6, 9] and list(sim.side) == [1, -1, 1]
