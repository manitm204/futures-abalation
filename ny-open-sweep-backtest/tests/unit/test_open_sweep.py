"""NY-open liquidity sweep: pre-open levels against a plain recomputation, hand-built fade and
continuation triggers, stops / targets / trade-through / stop-first, the side and window rules,
integrity checks on many configs (and that they catch tampered trades), look-ahead truncation,
the placebo override, the grid / lattice / local moves and the market config."""

from __future__ import annotations

from dataclasses import replace
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import polars as pl
import pytest

from src.analysis.neighborhood import LATTICE_OS_V1
from src.data.calendars import TradingCalendar
from src.experiments.funnel_config import load_funnel_config
from src.experiments.funnel_prep import build_dev_record, family_for
from src.experiments.funnel_robustness import local_perturbations_os, perturbations_os
from src.experiments.os_grid import AXES_OS_V1, os_grid_v1
from src.experiments.os_integrity import check_levels, check_sim_integrity, truncation_invariance
from src.strategies.open_sweep.backtest import (
    EOD_EXIT,
    STOP_EXIT,
    TARGET_EXIT,
    TIME_EXIT,
    OSData,
    OSParams,
    os_day_bars,
    planned_trades,
    simulate_open_sweep,
)
from src.strategies.open_sweep.config import OpenSweepV1Config
from src.utils.config_models import ExecutionConfig

ROOT = Path(__file__).resolve().parents[2]
NY = ZoneInfo("America/New_York")
FUT = ExecutionConfig(starting_equity=1_000_000, instrument_type="futures", commission_per_contract=2.5,
                      slippage_ticks_market=1.0, slippage_ticks_stop=1.0, commission_per_share=0.0,
                      commission_minimum=0.0, slippage_bps_market=0.0, slippage_bps_stop=0.0)
TICK = 0.25
CAL = TradingCalendar()
P = OSParams("NQ", "1min", level="onh", side="both", window=30, pen=0.0, confirm=3, mode="fade",
             stop_kind="struct", stop_mult=None, target_kind="none", target_r=None, exit_min=16 * 60)


def _p(**kw) -> OSParams:
    return replace(P, **kw)


def _row(ny: datetime, d: date, o, h, lo, c) -> dict:
    return {"bar_open_ts": ny.astimezone(ZoneInfo("UTC")), "bar_open_ts_ny": ny, "session_date_ny": d,
            "open": float(o), "high": float(h), "low": float(lo), "close": float(c), "volume": 100,
            "price_adjustment": 0.0}


def _frame(rows) -> pl.DataFrame:
    return pl.DataFrame(rows).with_columns(pl.col("bar_open_ts").dt.convert_time_zone("UTC"),
                                           pl.col("bar_open_ts_ny").dt.convert_time_zone("America/New_York"))


def _session_minutes(d: date):
    """(NY datetime) for every Globex minute of session d: 18:00 the evening before .. 16:59."""
    prev = d - timedelta(days=1)
    for t in range(18 * 60, 24 * 60):
        yield datetime(prev.year, prev.month, prev.day, t // 60, t % 60, tzinfo=NY)
    for t in range(0, 17 * 60):
        yield datetime(d.year, d.month, d.day, t // 60, t % 60, tzinfo=NY)


def _random_bars(start=date(2021, 1, 4), end=date(2021, 5, 28), seed=0, vol=2.0) -> pl.DataFrame:
    rng = np.random.default_rng(seed)
    rows, px = [], 13000.0
    for d in CAL.trading_days(start, end):
        for ny in _session_minutes(d):
            m = ny.hour * 60 + ny.minute
            v = vol * (5.0 if 570 <= m < 640 else (0.3 if m < 570 or m >= 1080 else 1.0))
            o = px
            c = round((px + float(rng.normal(0, v))) / TICK) * TICK
            wh = round(abs(float(rng.normal(0, v))) / TICK) * TICK
            wl = round(abs(float(rng.normal(0, v))) / TICK) * TICK
            rows.append(_row(ny, d, o, max(o, c) + TICK + wh, min(o, c) - TICK - wl, c))
            px = c
    return _frame(rows)


def _flat_bars(special: dict[str, tuple] | None = None, n_days: int = 16) -> pl.DataFrame:
    """n_days sessions. Pre-open bars: o=c=100, h=101, l=99 (so onh = [99, 101]); RTH bars:
    o=c=100, h=100.5, l=99.5 (dATR = 1). `special` overrides RTH bars of the LAST session by
    "HH:MM" -> (o, h, l, c)."""
    days = CAL.trading_days(date(2021, 3, 1), date(2021, 4, 30))[:n_days]
    rows = []
    for k, d in enumerate(days):
        for ny in _session_minutes(d):
            m = ny.hour * 60 + ny.minute
            if 570 <= m < 960:
                bar = (100, 100.5, 99.5, 100)
                key = f"{ny.hour:02d}:{ny.minute:02d}"
                if k == len(days) - 1 and special and key in special:
                    bar = special[key]
            else:
                bar = (100, 101, 99, 100)
            rows.append(_row(ny, d, *bar))
    return _frame(rows)


@pytest.fixture(scope="module")
def rand_full() -> pl.DataFrame:
    return _random_bars()


@pytest.fixture(scope="module")
def data(rand_full) -> OSData:
    return OSData(os_day_bars(rand_full))


def test_day_bars_and_levels(rand_full):
    day = os_day_bars(rand_full)
    tod = day["bar_open_ts_ny"].dt.hour().cast(pl.Int32) * 60 + day["bar_open_ts_ny"].dt.minute().cast(pl.Int32)
    assert tod.min() == 570 and tod.max() == 959
    assert check_levels(rand_full, day) == []
    # tampering with one level is caught
    bad = day.with_columns(pl.when(pl.col("session_date_ny") == day["session_date_ny"][500])
                           .then(pl.col("lon_h") + 1).otherwise(pl.col("lon_h")).alias("lon_h"))
    assert check_levels(rand_full, bad)


def test_onh_level_uses_evening_and_morning_only():
    df = _flat_bars({"09:30": (100, 100.5, 99.5, 100)})
    d = OSData(os_day_bars(df))
    H, L = d.levels("onh")
    assert np.allclose(H, 101) and np.allclose(L, 99)
    Hp, Lp = d.levels("pdr")
    assert np.isnan(Hp[0]) and np.allclose(Hp[1:], 100.5) and np.allclose(Lp[1:], 99.5)
    assert np.isnan(d.datr[:14]).all() and np.allclose(d.datr[14:], 1.0)


SWEEP = {"09:30": (100, 101.5, 99.9, 101.2), "09:31": (101.2, 101.4, 100.5, 100.8)}


def test_fade_needs_reclaim_within_confirm():
    d = OSData(os_day_bars(_flat_bars(SWEEP)))
    s = len(d.days) - 1
    a = d.day_start_idx[s]
    plan1 = planned_trades(d, _p(confirm=1))
    assert len(plan1["t"]) == 0  # the penetration bar closed above H
    plan3 = planned_trades(d, _p(confirm=3))
    assert plan3["t"].tolist() == [a + 1] and plan3["e"].tolist() == [a + 2] and plan3["side"].tolist() == [-1]
    sim = simulate_open_sweep(d, _p(confirm=3), exec_config=FUT, starting_equity=1e6)
    assert sim.side.tolist() == [-1]
    assert sim.stop_level[0] == pytest.approx(101.5 + 2 * TICK)   # struct: sweep high + 2 ticks
    assert sim.entry_px[0] == pytest.approx(100 - TICK)           # short at the 09:32 open - 1 tick
    assert sim.exit_reason.tolist() == [EOD_EXIT] or sim.forced_close[0]
    assert check_sim_integrity(sim, d, FUT, _p(confirm=3)) == []


def test_cont_takes_the_break():
    d = OSData(os_day_bars(_flat_bars(SWEEP)))
    a = d.day_start_idx[-1]
    sim = simulate_open_sweep(d, _p(mode="cont", confirm=1), exec_config=FUT, starting_equity=1e6)
    assert sim.signal_idx.tolist() == [a] and sim.entry_idx.tolist() == [a + 1] and sim.side.tolist() == [1]
    # confirm=2 needs a second close above H: 09:31 closed back inside
    assert len(simulate_open_sweep(d, _p(mode="cont", confirm=2), exec_config=FUT, starting_equity=1e6).trades) == 0


def test_side_window_and_penetration_rules():
    d = OSData(os_day_bars(_flat_bars(SWEEP)))
    assert len(planned_trades(d, _p(side="low"))["t"]) == 0
    assert len(planned_trades(d, _p(side="high"))["t"]) == 1
    assert len(planned_trades(d, _p(pen=0.6))["t"]) == 0          # 101.5 is not > 101 + 0.6
    assert len(planned_trades(d, _p(pen=0.4))["t"]) == 1
    late = {"10:05": (100, 101.5, 99.9, 100.5)}
    d2 = OSData(os_day_bars(_flat_bars(late)))
    assert len(planned_trades(d2, _p(window=30))["t"]) == 0
    assert len(planned_trades(d2, _p(window=60))["t"]) == 1
    # a 09:30 open above H makes the high side ineligible
    gap = {"09:30": (101.2, 101.6, 100.6, 100.8)}
    assert len(planned_trades(OSData(os_day_bars(_flat_bars(gap))), _p())["t"]) == 0


def test_target_needs_trade_through_and_stop_first():
    # fade short entered at the 09:32 open (100); struct stop 102.0 (dist 2.0) -> 1R target 98.0
    base = dict(SWEEP)
    touch = {**base, "09:40": (100, 100, 98.0, 99)}            # touches 98.0, no trade-through
    d = OSData(os_day_bars(_flat_bars(touch)))
    p = _p(target_kind="r", target_r=1.0)
    sim = simulate_open_sweep(d, p, exec_config=FUT, starting_equity=1e6)
    assert sim.exit_reason[0] != TARGET_EXIT
    through = {**base, "09:40": (100, 100, 97.75, 99)}
    d = OSData(os_day_bars(_flat_bars(through)))
    sim = simulate_open_sweep(d, p, exec_config=FUT, starting_equity=1e6)
    assert sim.exit_reason[0] == TARGET_EXIT and sim.exit_px[0] == pytest.approx(98.0)
    assert check_sim_integrity(sim, d, FUT, p) == []
    both = {**base, "09:40": (100, 102.5, 97.0, 99)}
    d = OSData(os_day_bars(_flat_bars(both)))
    sim = simulate_open_sweep(d, p, exec_config=FUT, starting_equity=1e6)
    assert sim.exit_reason[0] == STOP_EXIT
    assert sim.exit_px[0] == pytest.approx(102.0 + TICK)
    # range target for a fade short = the range low (99); wrong-side range target skips
    d = OSData(os_day_bars(_flat_bars({**base, "09:50": (100, 100, 98.5, 99)})))
    sim = simulate_open_sweep(d, _p(target_kind="range"), exec_config=FUT, starting_equity=1e6)
    assert sim.exit_reason[0] == TARGET_EXIT and sim.exit_px[0] == pytest.approx(99.0)


def test_time_exit_and_dATR_stop():
    d = OSData(os_day_bars(_flat_bars(SWEEP)))
    p = _p(stop_kind="datr", stop_mult=0.1, exit_min=12 * 60 + 30)
    sim = simulate_open_sweep(d, p, exec_config=FUT, starting_equity=1e6)
    # dATR = 1 -> stop 0.1 above the 100 entry; the flat bars' 100.5 high stops it on the entry bar
    assert sim.exit_reason[0] == STOP_EXIT and sim.stop_level[0] == pytest.approx(100.1)
    p = _p(stop_kind="datr", stop_mult=1.0, exit_min=12 * 60 + 30)
    sim = simulate_open_sweep(d, p, exec_config=FUT, starting_equity=1e6)
    assert sim.exit_reason[0] == TIME_EXIT
    x = sim.exit_idx[0]
    assert d.tod[x] == 12 * 60 + 29
    assert check_sim_integrity(sim, d, FUT, p) == []


GRID_SAMPLE = [_p(level=lv, side=sd, window=w, pen=pe, confirm=k, mode=m, stop_kind=sk, stop_mult=sm,
                  target_kind=tk, target_r=tr, exit_min=x)
               for lv, sd, w, pe, k, m, (sk, sm), (tk, tr), x in [
                   ("onh", "both", 30, 0.0, 1, "fade", ("struct", None), ("none", None), 960),
                   ("onh", "both", 30, 0.0, 3, "cont", ("struct", None), ("r", 2.0), 960),
                   ("asia", "high", 60, 0.05, 5, "fade", ("datr", 0.1), ("range", None), 660),
                   ("lon", "low", 15, 0.0, 1, "cont", ("datr", 0.2), ("r", 1.0), 750),
                   ("box", "both", 60, 0.05, 3, "fade", ("struct", None), ("r", 3.0), 960),
                   ("pdr", "both", 60, 0.0, 1, "fade", ("datr", 0.1), ("range", None), 960),
                   ("pdr", "both", 60, 0.0, 3, "cont", ("struct", None), ("range", None), 750),
                   ("box", "low", 15, 0.05, 3, "cont", ("datr", 0.2), ("none", None), 660),
               ]]


@pytest.mark.parametrize("p", GRID_SAMPLE)
def test_integrity_clean_on_random_data(data, p):
    sim = simulate_open_sweep(data, p, exec_config=FUT, starting_equity=1e6)
    assert len(sim.trades) >= 5
    assert check_sim_integrity(sim, data, FUT, p) == []


def test_random_data_trades_both_modes(data):
    n = {m: len(simulate_open_sweep(data, _p(mode=m, confirm=1), exec_config=FUT, starting_equity=1e6).trades)
         for m in ("fade", "cont")}
    assert n["fade"] > 10 and n["cont"] > 10


def test_integrity_catches_tampering(data):
    p = _p(confirm=1, target_kind="r", target_r=1.0)
    sim = simulate_open_sweep(data, p, exec_config=FUT, starting_equity=1e6)
    assert len(sim.trades) > 3
    s2 = replace(sim, side=-sim.side)
    assert "wrong_direction" in check_sim_integrity(s2, data, FUT, p)
    s3 = replace(sim, entry_idx=sim.entry_idx + 1)
    assert "entry_not_per_rule" in check_sim_integrity(s3, data, FUT, p)
    s4 = replace(sim, stop_level=sim.stop_level + 1.0)
    assert "stop_not_per_rule" in check_sim_integrity(s4, data, FUT, p)
    i = int(np.flatnonzero(sim.exit_reason == TARGET_EXIT)[0])
    px = sim.exit_px.copy()
    px[i] += 5 * sim.side[i]
    assert "target_fill_not_at_target" in check_sim_integrity(replace(sim, exit_px=px), data, FUT, p)
    keep = np.arange(len(sim.entry_idx)) != 0
    s5 = replace(sim, **{k: getattr(sim, k)[keep] for k in (
        "signal_idx", "entry_idx", "exit_idx", "decision_idx", "quantity", "entry_px", "exit_px",
        "entry_commission", "realized_pnl", "forced_close", "exit_reason", "entry_base", "side",
        "stop_level", "target_level")})
    assert "trade_skipped_while_flat" in check_sim_integrity(s5, data, FUT, p)


def test_truncation_invariance(rand_full):
    day = os_day_bars(rand_full)
    for p in GRID_SAMPLE[:4]:
        assert truncation_invariance(day, p, exec_config=FUT) == []


def test_placebo_override(data):
    H, L = data.levels("onh")
    data.level_override["onh"] = (H + 3.0, L - 3.0)
    try:
        sim = simulate_open_sweep(data, _p(confirm=1), exec_config=FUT, starting_equity=1e6)
        assert check_sim_integrity(sim, data, FUT, _p(confirm=1)) == []
    finally:
        data.level_override.clear()


def test_grid_lattice_and_moves():
    g = os_grid_v1(("NQ",))
    assert len(g) == 24300 and len({c.config_id for c in g}) == 24300
    assert set(AXES_OS_V1) - {"timeframe"} <= set(LATTICE_OS_V1.ordered) | set(LATTICE_OS_V1.fixed)
    cfg = OpenSweepV1Config(symbol="NQ", window=30, pen="0.05", confirm=3, stop="d0.10", target="2R", exit="12:30")
    p = OSParams.from_config(cfg)
    labels = {lab for lab, _ in local_perturbations_os(p, load_funnel_config(
        ROOT / "configs/funnel/os_funnel_nq_v1.yaml").parameter_stability.local)}
    assert labels == {"window=25", "window=35", "exit=12:15", "exit=12:45", "pen=0.025", "pen=0.075",
                      "confirm=2", "confirm=4", "stop=d0.05", "stop=d0.15", "target=1.5R", "target=2.5R"}
    fcfg = load_funnel_config(ROOT / "configs/funnel/os_funnel_nq_v1.yaml")
    ps = perturbations_os(p, config_id="x", base_seed=1, pcfg=fcfg.parameter_stability.perturbation)
    assert len(ps) == fcfg.parameter_stability.perturbation.n_per_config
    for q in ps:
        assert q.level == p.level and q.mode == p.mode and q.window >= 5 and q.exit_min <= 960
        assert q.exit_min > 570 + q.window and q.confirm >= 1


def test_market_config_and_record(data):
    fcfg = load_funnel_config(ROOT / "configs/funnel/os_funnel_nq_v1.yaml")
    assert fcfg.strategy == "open_sweep_v1" and fcfg.symbol == "NQ"
    assert fcfg.confidence.transfer_symbol == "ES"
    assert family_for(fcfg).simulate is simulate_open_sweep
    ce = os_grid_v1(("NQ",))[0]
    rec, rets = build_dev_record(ce, data, fcfg=fcfg, exec_config=FUT)
    assert rec["integrity_issues"] == "" and len(rets) > 0
