"""FX-fix reversal (daytime legs): fix times across daylight-saving mismatches, the 08:00-17:00
bar window, entries / exits per leg, stops, the vol gate's causality, integrity checks (and that
they catch tampered trades), look-ahead truncation, the grid / lattice / local moves and the
market config."""

from __future__ import annotations

from dataclasses import replace
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import polars as pl
import pytest

from src.analysis.neighborhood import LATTICE_FX_V1
from src.experiments.funnel_config import load_funnel_config
from src.experiments.funnel_prep import build_dev_record, family_for
from src.experiments.funnel_robustness import local_perturbations_fx, perturbations_fx
from src.experiments.fx_grid import AXES_FX_V1, fx_grid_v1
from src.experiments.fx_integrity import (
    check_sim_integrity,
    independent_fix_minutes,
    independent_gate,
    truncation_invariance,
)
from src.strategies.fx_fix.backtest import (
    EOD_EXIT,
    STOP_EXIT,
    TIME_EXIT,
    FXData,
    FXParams,
    fix_minutes,
    fx_day_bars,
    planned_trades,
    simulate_fx_fix,
)
from src.strategies.fx_fix.config import ECB_FIX, LONDON_FIX, FXFixV1Config
from src.utils.config_models import ExecutionConfig

ROOT = Path(__file__).resolve().parents[2]
NY = ZoneInfo("America/New_York")
FUT = ExecutionConfig(starting_equity=1_000_000, instrument_type="futures", commission_per_contract=2.5,
                      slippage_ticks_market=1.0, slippage_ticks_stop=1.0, commission_per_share=0.0,
                      commission_minimum=0.0, slippage_bps_market=0.0, slippage_bps_stop=0.0)
TICK = 0.00005
P = FXParams("6E", "1min", leg="post", switch_offset=0, post_hold="eod", vol_gate="none", stop_pct=None)


def _p(**kw) -> FXParams:
    return replace(P, **kw)


def _bars(n_days=6, start=date(2021, 6, 7), seed=0, vol=0.00005, first="07:00", last="17:59",
          drop: set[tuple[date, int]] | None = None) -> pl.DataFrame:
    """1-minute 6E-like bars on weekdays from `first` to `last` NY (both inclusive), random walk.
    `drop` removes (date, NY minute) bars to create gaps."""
    rng = np.random.default_rng(seed)
    h0, m0 = map(int, first.split(":"))
    h1, m1 = map(int, last.split(":"))
    rows, d, px = [], start, 1.20
    made = 0
    while made < n_days:
        if d.weekday() < 5:
            for t in range(h0 * 60 + m0, h1 * 60 + m1 + 1):
                if drop and (d, t) in drop:
                    continue
                ny = datetime(d.year, d.month, d.day, t // 60, t % 60, tzinfo=NY)
                o = px
                c = px + float(rng.normal(0, vol))
                rows.append({"bar_open_ts": ny.astimezone(ZoneInfo("UTC")), "bar_open_ts_ny": ny, "session_date_ny": d,
                             "open": o, "high": max(o, c) + 0.00002, "low": min(o, c) - 0.00002, "close": c,
                             "volume": 100, "price_adjustment": 0.0})
                px = c
            made += 1
        d += timedelta(days=1)
    df = pl.DataFrame(rows)
    return df.with_columns(pl.col("bar_open_ts").dt.convert_time_zone("UTC"),
                           pl.col("bar_open_ts_ny").dt.convert_time_zone("America/New_York"))


def _data(**kw) -> FXData:
    return FXData(fx_day_bars(_bars(**kw)))


def _tod(data: FXData, i: int) -> int:
    return int(data.tod[i])


# --- fix times ---------------------------------------------------------------------------------

@pytest.mark.parametrize("day,london,ecb", [
    (date(2021, 1, 11), 11 * 60, 8 * 60 + 15),        # both on winter time
    (date(2021, 7, 12), 11 * 60, 8 * 60 + 15),        # both on summer time
    (date(2021, 3, 16), 12 * 60, 9 * 60 + 15),        # US on summer time, Europe not yet
    (date(2021, 11, 2), 12 * 60, 9 * 60 + 15),        # Europe back on winter time, US not yet
])
def test_fix_minutes_follow_each_fix_time_zone(day, london, ecb):
    assert fix_minutes(day, LONDON_FIX) == london
    assert fix_minutes(day, ECB_FIX) == ecb
    days = np.array([day], dtype="datetime64[D]")
    assert independent_fix_minutes(days, LONDON_FIX)[0] == london
    assert independent_fix_minutes(days, ECB_FIX)[0] == ecb


def test_day_window_drops_bars_outside_08_to_17():
    raw = _bars(n_days=2)
    b = fx_day_bars(raw)
    tod = (b["bar_open_ts_ny"].dt.hour().cast(pl.Int32) * 60 + b["bar_open_ts_ny"].dt.minute().cast(pl.Int32)).to_numpy()
    assert tod.min() == 8 * 60 and tod.max() == 16 * 60 + 59
    assert b.height == 2 * 540
    with pytest.raises(ValueError):
        fx_day_bars(raw, timeframe="5min")


# --- entries and exits -------------------------------------------------------------------------

def test_post_leg_enters_at_london_fix_open_and_exits_at_last_bar_before_17():
    d = _data(n_days=3)
    s = simulate_fx_fix(d, P, exec_config=FUT, starting_equity=1e6)
    assert len(s.entry_idx) == 3
    for e, x, side, why, px in zip(s.entry_idx, s.exit_idx, s.side, s.exit_reason, s.entry_px):
        assert _tod(d, e) == 11 * 60 and side == 1
        assert _tod(d, x) == 16 * 60 + 59 and x == d.sess_end[x]
        assert px == pytest.approx(d.open[e] + TICK)          # adverse slippage on a buy
    assert set(s.exit_reason[:-1]) == {EOD_EXIT}
    assert s.forced_close[-1] and not s.forced_close[:-1].any()  # last bar of the data


def test_post_hold_and_switch_offset_timing():
    d = _data(n_days=2)
    s = simulate_fx_fix(d, _p(switch_offset=15, post_hold="60"), exec_config=FUT, starting_equity=1e6)
    assert [_tod(d, e) for e in s.entry_idx] == [11 * 60 + 15] * 2
    assert [_tod(d, x) for x in s.exit_idx] == [12 * 60 + 14] * 2  # closes at 12:15
    assert set(s.exit_reason) == {TIME_EXIT}
    for x, px in zip(s.exit_idx, s.exit_px):
        assert px == pytest.approx(d.close[x] - TICK)           # adverse slippage on a sell


def test_pre_leg_is_short_from_ecb_fix_to_switch():
    d = _data(n_days=2)
    s = simulate_fx_fix(d, _p(leg="pre", switch_offset=-5), exec_config=FUT, starting_equity=1e6)
    assert list(s.side) == [-1, -1] and set(s.leg) == {"pre"}
    assert [_tod(d, e) for e in s.entry_idx] == [8 * 60 + 15] * 2
    assert [_tod(d, x) for x in s.exit_idx] == [10 * 60 + 54] * 2
    assert set(s.exit_reason) == {TIME_EXIT}


def test_both_legs_trade_back_to_back_without_overlap():
    d = _data(n_days=2)
    s = simulate_fx_fix(d, _p(leg="both", post_hold="120"), exec_config=FUT, starting_equity=1e6)
    assert list(s.leg) == ["pre", "post", "pre", "post"]
    assert s.entry_idx[1] == s.exit_idx[0] + 1 and s.entry_idx[3] == s.exit_idx[2] + 1
    assert check_sim_integrity(s, d, FUT, _p(leg="both", post_hold="120")) == []


def test_dst_mismatch_day_moves_the_clock_times():
    d = _data(n_days=1, start=date(2021, 3, 16))
    s = simulate_fx_fix(d, _p(leg="both", post_hold="60"), exec_config=FUT, starting_equity=1e6)
    assert [_tod(d, e) for e in s.entry_idx] == [9 * 60 + 15, 12 * 60]


def test_gap_at_entry_time_skips_the_day():
    day = date(2021, 6, 7)
    drop = {(day, t) for t in range(11 * 60, 11 * 60 + 6)}       # 11:00..11:05 missing -> 6 min late
    d = _data(n_days=2, drop=drop)
    plan = planned_trades(d, P)
    assert len(plan["e"]) == 1 and d.session_date[plan["e"][0]] != np.datetime64(day)
    drop_small = {(day, t) for t in range(11 * 60, 11 * 60 + 3)}  # 3 min late -> still traded
    d2 = _data(n_days=2, drop=drop_small)
    s = simulate_fx_fix(d2, P, exec_config=FUT, starting_equity=1e6)
    assert _tod(d2, s.entry_idx[0]) == 11 * 60 + 3
    assert check_sim_integrity(s, d2, FUT, P) == []


def test_stop_exits_at_first_touch_with_worse_fill():
    d = _data(n_days=3, vol=0.0004, seed=3)
    p = _p(stop_pct=0.05)
    s = simulate_fx_fix(d, p, exec_config=FUT, starting_equity=1e6)
    assert STOP_EXIT in set(s.exit_reason)
    for i in np.flatnonzero(s.exit_reason == STOP_EXIT):
        e, x = s.entry_idx[i], s.exit_idx[i]
        stop = d.open[e] * (1 - 0.0005)
        assert s.stop_level[i] == pytest.approx(stop)
        assert d.low[x] <= stop and (d.low[e:x] > stop).all()
        assert s.exit_px[i] == pytest.approx(min(d.open[x], stop) - TICK)
    assert check_sim_integrity(s, d, FUT, p) == []


def test_position_is_unlevered_whole_contracts():
    d = _data(n_days=1)
    s = simulate_fx_fix(d, P, exec_config=FUT, starting_equity=1e6)
    contracts = s.quantity[0] / 125_000
    assert contracts == int(contracts) and contracts * 125_000 * s.entry_px[0] <= 1e6


# --- vol gate ----------------------------------------------------------------------------------

def test_vol_gate_matches_independent_loops_and_is_causal():
    d = FXData(fx_day_bars(_bars(n_days=300, first="08:00", last="16:59", vol=0.00004, seed=5)))
    for gate in ("high", "low"):
        assert np.array_equal(d.gate_ok(gate), independent_gate(d, gate))
    high, low = d.gate_ok("high"), d.gate_ok("low")
    assert not (high & low).any() and (high | low)[275:].all() and not (high | low)[:269].any()
    # Changing only the LAST session's prices cannot change any session's gate (known at the open).
    raw = _bars(n_days=300, first="08:00", last="16:59", vol=0.00004, seed=5)
    last_day = raw["session_date_ny"].max()
    bumped = raw.with_columns(pl.when(pl.col("session_date_ny") == last_day).then(pl.col("close") * 1.01)
                              .otherwise(pl.col("close")).alias("close"))
    d2 = FXData(fx_day_bars(bumped))
    assert np.array_equal(d2.gate_ok("high"), high)


# --- integrity ---------------------------------------------------------------------------------

def test_integrity_clean_on_every_leg_and_setting():
    d = FXData(fx_day_bars(_bars(n_days=280, first="08:00", last="16:59", vol=0.0002, seed=1)))
    for cfg in fx_grid_v1(("6E",))[::7]:
        s = simulate_fx_fix(d, cfg.config, exec_config=FUT, starting_equity=1e6)
        assert check_sim_integrity(s, d, FUT, cfg.config) == [], cfg.config


def test_integrity_catches_tampered_trades():
    d = _data(n_days=4)
    p = _p(leg="both", post_hold="60")
    s = simulate_fx_fix(d, p, exec_config=FUT, starting_equity=1e6)
    assert check_sim_integrity(s, d, FUT, p) == []

    t = replace(s, entry_idx=s.entry_idx.copy(), signal_idx=s.signal_idx.copy(), entry_base=s.entry_base.copy())
    t.entry_idx[1] += 2
    t.signal_idx[1] += 2
    t.entry_base[1] = d.open[t.entry_idx[1]]
    assert "entry_not_at_leg_start" in check_sim_integrity(t, d, FUT, p)

    t = replace(s, side=s.side.copy())
    t.side[0] = 1
    assert "side_not_per_leg" in check_sim_integrity(t, d, FUT, p)

    t = replace(s, entry_px=s.entry_px.copy())
    t.entry_px[1] = d.open[s.entry_idx[1]] - TICK            # a long filled below the open
    assert "entry_fill_better_than_market" in check_sim_integrity(t, d, FUT, p)

    t = replace(s, exit_idx=s.exit_idx.copy())
    t.exit_idx[1] += 3
    assert "time_exit_not_per_rule" in check_sim_integrity(t, d, FUT, p)

    keep = np.arange(len(s.entry_idx)) != 2
    t = replace(s, **{k: getattr(s, k)[keep] for k in ("signal_idx", "entry_idx", "exit_idx", "decision_idx",
                                                       "quantity", "entry_px", "exit_px", "entry_commission",
                                                       "realized_pnl", "forced_close", "exit_reason", "stop_level",
                                                       "entry_base", "side", "leg")})
    assert "trade_skipped_while_flat" in check_sim_integrity(t, d, FUT, p)

    t = replace(s, quantity=s.quantity * 100)
    assert "position_exceeds_equity" in check_sim_integrity(t, d, FUT, p)

    t = replace(s, exit_idx=s.exit_idx.copy())
    t.exit_idx[0] = s.entry_idx[1]
    assert "overlapping_positions" in check_sim_integrity(t, d, FUT, p)


def test_integrity_catches_trades_on_gated_days():
    d = FXData(fx_day_bars(_bars(n_days=280, first="08:00", last="16:59", vol=0.0002, seed=1)))
    s = simulate_fx_fix(d, _p(vol_gate="none"), exec_config=FUT, starting_equity=1e6)
    assert "vol_gate_not_met" in check_sim_integrity(s, d, FUT, _p(vol_gate="high"))


def test_no_lookahead_under_truncation():
    b = fx_day_bars(_bars(n_days=280, first="08:00", last="16:59", vol=0.0002, seed=2))
    for p in (_p(), _p(leg="both", post_hold="60", stop_pct=0.25, vol_gate="high"), _p(leg="pre", vol_gate="low")):
        assert truncation_invariance(b, p, exec_config=FUT, cut_fracs=(0.3, 0.55, 0.8, 0.97)) == []


def test_stress_knobs():
    d = _data(n_days=5)
    base = simulate_fx_fix(d, P, exec_config=FUT, starting_equity=1e6)
    late = simulate_fx_fix(d, P, exec_config=FUT, starting_equity=1e6, entry_delay_bars=1)
    assert (late.entry_idx == base.entry_idx + 1).all()
    miss = simulate_fx_fix(d, P, exec_config=FUT, starting_equity=1e6, missed_entry_frac=0.5, stress_seed=1)
    assert 0 < len(miss.entry_idx) < len(base.entry_idx)


# --- grid, lattice, local moves, config --------------------------------------------------------

def test_grid_has_no_duplicates_and_pins_unused_axes():
    g = fx_grid_v1(("6E",))
    assert len(g) == 405 and len({c.config_id for c in g}) == 405
    assert {c.config.post_hold for c in g if c.config.leg == "pre"} == {"eod"}
    for ax, vals in LATTICE_FX_V1.ordered.items():
        assert set(vals) == set(AXES_FX_V1[ax])


def test_local_and_random_perturbations():
    cfg = load_funnel_config(ROOT / "configs/funnel/fx_funnel_6e_v1.yaml")
    lc = cfg.parameter_stability.local
    moves = dict(local_perturbations_fx(_p(post_hold="120", stop_pct=0.25), lc))
    assert set(moves) == {"switch_offset=-5", "switch_offset=5", "post_hold=90", "post_hold=150",
                          "stop_pct=0.15", "stop_pct=0.35"}
    assert {k for k in dict(local_perturbations_fx(_p(leg="pre"), lc))} == {"switch_offset=-5", "switch_offset=5"}
    d = _data(n_days=2)
    for _, mp in moves.items():
        s = simulate_fx_fix(d, mp, exec_config=FUT, starting_equity=1e6)
        assert check_sim_integrity(s, d, FUT, mp) == []
    ps = perturbations_fx(_p(post_hold="120", stop_pct=0.25), config_id="x", base_seed=1,
                          pcfg=cfg.parameter_stability.perturbation)
    assert len(ps) == 20 and all(q.switch_offset != 0 and q.leg == "post" for q in ps)


def test_funnel_config_and_family_wiring():
    cfg = load_funnel_config(ROOT / "configs/funnel/fx_funnel_6e_v1.yaml")
    assert cfg.strategy == "fx_fix_v1" and cfg.symbol == "6E" and cfg.confidence.transfer_symbol == "6J"
    assert family_for(cfg).simulate is simulate_fx_fix
    d = _data(n_days=3)
    ce = fx_grid_v1(("6E",))[0]
    rec, rets = build_dev_record(ce, d, fcfg=cfg, exec_config=FUT)
    assert rec["integrity_issues"] == "" and len(rets) == len(d.days)


def test_config_rejects_off_grid_values():
    with pytest.raises(Exception):
        FXFixV1Config(symbol="6E", switch_offset=7)
    with pytest.raises(Exception):
        FXFixV1Config(symbol="6E", leg="tokyo")
