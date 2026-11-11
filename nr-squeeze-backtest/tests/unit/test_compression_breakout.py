"""Compression breakout (squeeze and NR lines): compression flags and runs, the box and its
causality, entry rules (close / wick, first breakout consumes the run, expiry, filters,
cutoff), exits (stop, target, session close, same-bar ordering), stress knobs, integrity
checks, the two lines' grids and lattices, local / random perturbations and the market
configs."""

from __future__ import annotations

from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import polars as pl
import pytest

from src.analysis.daily_performance import daily_equity
from src.analysis.neighborhood import LATTICE_CB_BBKC_V1, LATTICE_CB_NR_V1, neighbor_ids
from src.experiments.cb_grid import AXES_BBKC_V1, AXES_NR_V1, cb_grid_bbkc, cb_grid_nr, variants_per_symbol
from src.experiments.cb_integrity import check_sim_integrity, independent_compression, truncation_invariance
from src.experiments.funnel_config import load_funnel_config
from src.experiments.funnel_prep import FAMILIES, build_dev_record, family_for
from src.experiments.funnel_robustness import local_perturbations_cb, perturbations_cb
from src.experiments.mr_grid import ConfigEntry
from src.strategies.compression_breakout.backtest import CBData, CBParams, CostModel, simulate_compression_breakout
from src.strategies.compression_breakout.config import NRBreakoutConfig, SqueezeBreakoutConfig
from src.utils.config_models import ExecutionConfig

EC = ExecutionConfig()
FUT = ExecutionConfig(starting_equity=1_000_000, instrument_type="futures", commission_per_contract=2.5,
                      slippage_ticks_market=1.0, slippage_ticks_stop=1.0, commission_per_share=0.0,
                      commission_minimum=0.0, slippage_bps_market=0.0, slippage_bps_stop=0.0)
P = CBParams("SPY", "15min", compression="nr", squeeze_length=None, kc_mult=None, min_squeeze_bars=None,
             nr_lookback=4, entry_type="close", setup_expiry_bars=3, stop_atr=None, target_r=2.0,
             direction="both", trend_filter="none")
CONFIGS = Path("configs/funnel")
MARKETS = {"es", "nq", "ym", "rty", "cl", "gc", "6e", "6j", "zn"}
LINES = {"bbkc": "compression_breakout_bbkc", "nr": "compression_breakout_nr"}


def _p(**kw) -> CBParams:
    return replace(P, **kw)


def _ohlc(days: list[list[tuple[float, float, float, float]]], start=date(2020, 1, 6)) -> pl.DataFrame:
    """15-min RTH bars (09:30 NY open in January), one inner list of (o, h, l, c) per session."""
    rows, d = [], start
    for bars in days:
        while d.weekday() >= 5:
            d += timedelta(days=1)
        t0 = datetime(d.year, d.month, d.day, 14, 30, tzinfo=timezone.utc)
        for i, (o, h, lo, c) in enumerate(bars):
            rows.append({"bar_open_ts": t0 + timedelta(minutes=15 * i), "session_date_ny": d,
                         "open": o, "high": h, "low": lo, "close": c})
        d += timedelta(days=1)
    return pl.DataFrame(rows)


def _plain_day(over: dict[int, tuple] | None = None, n: int = 26, px: float = 100.0) -> list[tuple]:
    """Flat bars whose ranges WIDEN through the session (so no plain bar is NR-N), with
    `over` replacing bars by index."""
    out = [(px, px + 0.5 + 0.005 * i, px - 0.5 - 0.005 * i, px) for i in range(n)]
    for i, b in (over or {}).items():
        out[i] = b
    return out


# Bars 5-6 are NR-4 (range 0.1): box [99.95, 100.05]. Bar 7 closes above it.
SQUEEZE = {5: (100.0, 100.05, 99.95, 100.0), 6: (100.0, 100.05, 99.95, 100.0)}
BREAK_UP = {7: (100.0, 100.4, 99.98, 100.3), 8: (100.3, 100.4, 100.2, 100.35)}


def _walk(n_days=60, per_day=26, seed=0):
    """Random-walk 15-min sessions with quiet and active stretches (so squeezes form)."""
    rng = np.random.default_rng(seed)
    days, px = [], 100.0
    for _ in range(n_days):
        vol = np.where(rng.random(per_day) < 0.4, 0.05, 0.35) * rng.uniform(0.5, 1.5)
        bars = []
        for v in vol:
            o = px
            c = o + rng.normal(0, v)
            h, lo = max(o, c) + abs(rng.normal(0, v / 2)), min(o, c) - abs(rng.normal(0, v / 2))
            bars.append((o, h, lo, c))
            px = c
        days.append(bars)
        px += rng.normal(0, 0.3)  # overnight gap
    return _ohlc(days)


def _sim(bars, p=P, ec=EC, **kw):
    data = CBData(bars)
    return data, simulate_compression_breakout(data, p, exec_config=ec, starting_equity=1e5, **kw)


# --- compression flags, runs and the box ----------------------------------------------------

def test_nr_flag_is_narrowest_of_last_n_with_ties():
    data = CBData(_ohlc([_plain_day(SQUEEZE)]))
    comp = data.compression(P)
    assert np.flatnonzero(comp).tolist() == [5, 6]  # 6 ties bar 5 and still counts
    assert not comp[:3].any()  # warm-up: fewer than N bars
    assert np.array_equal(comp, independent_compression(data, P))


def test_bbkc_flag_matches_hand_computation():
    bars = _walk(seed=3, n_days=10)
    data = CBData(bars)
    p = _p(compression="bbkc", squeeze_length=10, kc_mult=1.5, min_squeeze_bars=1, nr_lookback=None)
    comp = data.compression(p)
    atr = data.atr(10)
    for k in (40, 77, 150, 233):
        sd = np.std(data.close[k - 9:k + 1])
        assert comp[k] == (2.0 * sd < 1.5 * atr[k])
    assert comp.any() and not comp.all()
    assert np.array_equal(comp, independent_compression(data, p))


def test_runs_never_cross_the_session_open():
    end = {24: (100.0, 100.05, 99.95, 100.0), 25: (100.0, 100.05, 99.95, 100.0)}
    start = {0: (100.0, 100.04, 99.96, 100.0), 1: (100.0, 100.04, 99.96, 100.0)}
    data = CBData(_ohlc([_plain_day(end), _plain_day(start)]))
    comp = data.compression(P)
    assert comp[24] and comp[25] and comp[26] and comp[27]
    ru = data.runs(P)
    assert ru["run_start"][26] == 26 and ru["run_start"][25] == 24
    assert ru["last_before"][26] == -1  # yesterday's run is not live at today's first bar


def test_box_excludes_the_decision_bar():
    bars = _ohlc([_plain_day({**SQUEEZE, **BREAK_UP})])
    data = CBData(bars)
    ru = data.runs(P)
    assert ru["last_before"][7] == 6 and ru["run_start"][6] == 5
    assert (ru["box_hi"][6], ru["box_lo"][6]) == (100.05, 99.95)


# --- entries ---------------------------------------------------------------------------------

def test_close_breakout_enters_next_open_with_box_stop_and_target():
    over = {**SQUEEZE, **BREAK_UP, 9: (100.5, 101.2, 100.4, 101.1)}
    data, sim = _sim(_ohlc([_plain_day(over)]))
    costs = CostModel.for_symbol(EC, "SPY")
    assert len(sim.entry_idx) == 1
    assert (sim.signal_idx[0], sim.entry_idx[0], sim.side[0]) == (7, 8, 1)
    assert sim.entry_px[0] == pytest.approx(costs.fill(100.3, "buy"))
    assert sim.stop_level[0] == 99.95
    assert sim.target_level[0] == pytest.approx(100.3 + 2 * 0.35)
    assert sim.exit_reason[0] == "target_exit" and sim.exit_idx[0] == 9
    assert sim.exit_px[0] == pytest.approx(costs.fill(101.0, "sell"))
    assert check_sim_integrity(sim, data, EC, P) == []


def test_wick_entry_fills_at_worse_of_open_and_edge_with_stop_slippage():
    over = {**SQUEEZE, 7: (100.0, 100.4, 99.98, 100.3)}
    p = _p(entry_type="wick", target_r=None)
    data, sim = _sim(_ohlc([_plain_day(over)]), p)
    costs = CostModel.for_symbol(EC, "SPY")
    assert (sim.signal_idx[0], sim.entry_idx[0]) == (7, 7)
    assert sim.entry_px[0] == pytest.approx(costs.fill(100.05, "buy", stop=True))
    gap = {**SQUEEZE, 7: (100.2, 100.4, 100.15, 100.3)}  # opens above the edge: fills at the open
    _, sim2 = _sim(_ohlc([_plain_day(gap)]), p)
    assert sim2.entry_px[0] == pytest.approx(costs.fill(100.2, "buy", stop=True))
    assert check_sim_integrity(sim, data, EC, p) == []


def test_wick_bar_through_both_edges_is_not_traded_and_consumes_the_run():
    over = {**SQUEEZE, 7: (100.0, 100.4, 99.6, 100.0), 8: (100.0, 100.5, 99.99, 100.4)}
    _, sim = _sim(_ohlc([_plain_day(over)]), _p(entry_type="wick"))
    assert len(sim.entry_idx) == 0


def test_first_breakout_consumes_the_run_even_when_filtered():
    # Bar 7 breaks DOWN first; a long-only config must not take bar 8's upside break.
    over = {**SQUEEZE, 7: (100.0, 100.02, 99.7, 99.8), 8: (99.8, 100.5, 99.75, 100.4)}
    _, long_only = _sim(_ohlc([_plain_day(over)]), _p(direction="long"))
    assert len(long_only.entry_idx) == 0
    _, both = _sim(_ohlc([_plain_day(over)]), _p(direction="both"))
    assert both.side.tolist() == [-1] and both.signal_idx.tolist() == [7]


def test_setup_expires_after_expiry_bars():
    late = {**SQUEEZE, 10: (100.0, 100.4, 99.98, 100.3)}  # 4 bars after the last squeeze bar (6)
    _, sim3 = _sim(_ohlc([_plain_day(late)]), _p(setup_expiry_bars=3))
    _, sim6 = _sim(_ohlc([_plain_day(late)]), _p(setup_expiry_bars=6))
    assert len(sim3.entry_idx) == 0 and sim6.signal_idx.tolist() == [10]


def test_min_squeeze_bars_needs_a_long_enough_run():
    bars = _walk(seed=7, n_days=80)
    p1 = _p(compression="bbkc", squeeze_length=10, kc_mult=1.5, min_squeeze_bars=1)
    data, s1 = _sim(bars, p1)
    _, s4 = _sim(bars, replace(p1, min_squeeze_bars=4))
    assert len(s4.entry_idx) < len(s1.entry_idx)
    assert np.all(s4.signal_idx - s4.run_start > 0)
    ru = data.runs(p1)
    r = ru["last_before"][s4.signal_idx]
    assert np.all(r - s4.run_start + 1 >= 4)


def test_trend_filter_only_drops_counter_trend_entries():
    bars = _walk(seed=11, n_days=90)
    data, base = _sim(bars)
    _, filt = _sim(bars, _p(trend_filter="ema50"))
    assert 0 < len(filt.entry_idx) < len(base.entry_idx)
    ema = data.ema_trend
    k = filt.signal_idx
    assert np.all(np.where(filt.side > 0, data.close[k] > ema[k], data.close[k] < ema[k]))


def test_no_entry_in_the_last_30_minutes():
    # Bar 24 closes 15:45, 15 minutes before the last close: too late. Bar 23 (15:30) is allowed.
    late = {23: (100.0, 100.05, 99.95, 100.0), 24: (100.0, 100.4, 99.98, 100.3)}
    _, sim = _sim(_ohlc([_plain_day(late)]))
    assert len(sim.entry_idx) == 0
    _, ok = _sim(_ohlc([_plain_day(late)]), _p(last_entry_cutoff=0))
    assert ok.signal_idx.tolist() == [24]
    edge = {22: (100.0, 100.05, 99.95, 100.0), 23: (100.0, 100.4, 99.98, 100.3)}
    _, at30 = _sim(_ohlc([_plain_day(edge)]))
    assert at30.signal_idx.tolist() == [23]


def test_short_direction_takes_only_shorts():
    bars = _walk(seed=13, n_days=60)
    data, sim = _sim(bars, _p(direction="short"))
    assert len(sim.side) and set(sim.side.tolist()) == {-1}
    assert check_sim_integrity(sim, data, EC, _p(direction="short")) == []


def test_inside_bar_requires_the_nr_bar_inside_the_previous_bar():
    outside = {5: (100.6, 100.65, 100.55, 100.6)}  # narrowest range, but above bar 4's high
    data = CBData(_ohlc([_plain_day(outside)]))
    assert data.compression(P)[5] and not data.compression(_p(inside_bar=True))[5]
    inside = CBData(_ohlc([_plain_day(SQUEEZE)]))
    assert inside.compression(_p(inside_bar=True))[[5, 6]].all()  # bar 6 equals bar 5: inside (non-strict)
    for d in (data, inside):
        assert np.array_equal(d.compression(_p(inside_bar=True)), independent_compression(d, _p(inside_bar=True)))


def test_min_box_width_skips_narrow_boxes_without_consuming_them():
    bars = _ohlc([_plain_day(), _plain_day({**SQUEEZE, **BREAK_UP})])  # box 0.1 wide, ATR(14) ~1
    _, any_box = _sim(bars)
    _, wide = _sim(bars, _p(min_box_atr=0.5))
    assert any_box.signal_idx.tolist() == [26 + 7] and len(wide.entry_idx) == 0
    walk = _walk(seed=14, n_days=80)
    data, sim = _sim(walk, _p(min_box_atr=0.5))
    r = data.runs(P)["last_before"][sim.signal_idx]
    assert len(sim.entry_idx) and np.all(sim.box_hi - sim.box_lo >= 0.5 * data.atr(14)[r])
    assert check_sim_integrity(sim, data, EC, _p(min_box_atr=0.5)) == []
    # The filter changes which setups are live, so these trades break the unfiltered config's rules
    # (an earlier, narrower breakout of the same run would have consumed it there).
    assert "not_first_breakout_of_run" in check_sim_integrity(sim, data, EC, _p(min_box_atr=0.0))


# --- exits -----------------------------------------------------------------------------------

def test_stop_wins_when_a_bar_touches_stop_and_target():
    over = {**SQUEEZE, **BREAK_UP, 9: (100.3, 101.5, 99.5, 100.3)}
    data, sim = _sim(_ohlc([_plain_day(over)]))
    assert sim.exit_reason[0] == "stop_exit" and sim.exit_idx[0] == 9
    assert sim.exit_px[0] == pytest.approx(CostModel.for_symbol(EC, "SPY").fill(99.95, "sell", stop=True))
    assert check_sim_integrity(sim, data, EC, P) == []


def test_wick_entry_bar_checks_only_the_stop():
    p = _p(entry_type="wick", target_r=1.0)
    hits_target = {**SQUEEZE, 7: (100.0, 100.3, 99.98, 100.25)}  # edge 100.05 + 1R (0.1) = 100.15 reached
    data, sim = _sim(_ohlc([_plain_day(hits_target)]), p)
    assert sim.exit_idx[0] > 7
    # A very tight ATR stop inside the entry bar's range: stopped on the entry bar, at the stop.
    # (A warm-up session first, so ATR(14) exists.)
    atr_stop = replace(p, stop_atr=0.01, target_r=None)
    bars = _ohlc([_plain_day(), _plain_day({**SQUEEZE, 7: (100.0, 100.3, 99.97, 100.2)})])
    data, s2 = _sim(bars, atr_stop)
    assert s2.exit_reason[0] == "stop_exit" and s2.entry_idx[0] == s2.exit_idx[0] == 26 + 7
    assert s2.exit_px[0] == pytest.approx(CostModel.for_symbol(EC, "SPY").fill(s2.stop_level[0], "sell", stop=True))
    assert check_sim_integrity(s2, data, EC, atr_stop) == []


def test_session_close_exit_at_last_close_and_final_session_forced():
    above = {i: (100.4, 100.5 + 0.005 * i, 100.3 - 0.005 * i, 100.4) for i in range(9, 26)}  # never hits the stop
    day = _plain_day({**SQUEEZE, **BREAK_UP, **above})
    data, sim = _sim(_ohlc([day, day]), _p(target_r=None))
    assert sim.exit_reason[0] == "eod_exit" and sim.exit_idx[0] == data.sess_end[sim.entry_idx[0]]
    assert sim.exit_px[0] == pytest.approx(CostModel.for_symbol(EC, "SPY").fill(data.close[25], "sell"))
    assert sim.exit_reason[-1] == "forced_close" and sim.forced_close[-1] and sim.exit_idx[-1] == data.n - 1


def test_atr_stop_uses_atr_known_before_the_fill():
    bars = _walk(seed=5, n_days=60)
    p = _p(stop_atr=1.5)
    data, sim = _sim(bars, p)
    e = sim.entry_idx
    assert len(e) > 0
    assert np.allclose(sim.stop_level, data.open[e] - sim.side * 1.5 * data.atr(14)[e - 1])


# --- integrity, look-ahead and stress ---------------------------------------------------------

VARIANTS = [P, _p(entry_type="wick"), _p(stop_atr=1.0, target_r=None), _p(direction="long", trend_filter="ema50"),
            _p(compression="bbkc", squeeze_length=10, kc_mult=1.5, min_squeeze_bars=1),
            _p(compression="bbkc", squeeze_length=20, kc_mult=2.0, min_squeeze_bars=4, entry_type="wick",
               stop_atr=2.0, target_r=3.0, setup_expiry_bars=6),
            _p(direction="short", nr_lookback=7, inside_bar=True),
            _p(nr_lookback=3, min_box_atr=0.5, entry_type="wick", stop_atr=1.0),
            _p(compression="bbkc", squeeze_length=10, kc_mult=2.0, min_squeeze_bars=1, min_box_atr=0.5)]


@pytest.mark.parametrize("seed", range(5))
def test_integrity_clean_and_nothing_held_overnight(seed):
    bars = _walk(seed=seed, n_days=70)
    for p in VARIANTS:
        data, sim = _sim(bars, p)
        assert len(sim.entry_idx) > 0, p
        assert check_sim_integrity(sim, data, EC, p) == [], p
        assert np.all(data.sess[sim.exit_idx] == data.sess[sim.entry_idx])
        assert np.all(sim.entry_idx[1:] > sim.exit_idx[:-1])


def test_no_lookahead_truncation_invariance():
    bars = _walk(seed=4, n_days=50)
    for p in VARIANTS:
        assert truncation_invariance(bars, p, exec_config=EC) == []


def test_integrity_flags_tampered_trades():
    bars = _walk(seed=2, n_days=60)
    data, sim = _sim(bars)
    bad = replace(sim, stop_level=sim.stop_level + 0.5)
    assert "stop_not_per_rule" in check_sim_integrity(bad, data, EC, P)
    bad = replace(sim, box_hi=sim.box_hi + 0.5)
    assert "box_not_from_prior_compression_run" in check_sim_integrity(bad, data, EC, P)
    bad = replace(sim, entry_px=sim.entry_px - 1.0)
    assert "entry_fill_better_than_market" in check_sim_integrity(bad, data, EC, P)
    # A config whose setups expire immediately cannot have produced these trades.
    assert check_sim_integrity(sim, data, EC, _p(setup_expiry_bars=0))


def test_stress_knobs_delay_and_missed_entries():
    bars = _walk(seed=6, n_days=70)
    data, base = _sim(bars)
    _, late = _sim(bars, entry_delay_bars=1)
    assert np.all(late.entry_idx - late.signal_idx == 2)
    _, miss = _sim(bars, missed_entry_frac=0.3, stress_seed=1)
    assert 0 < len(miss.entry_idx) < len(base.entry_idx)
    assert check_sim_integrity(late, data, EC, P) == [] and check_sim_integrity(miss, data, EC, P) == []
    _, again = _sim(bars, missed_entry_frac=0.3, stress_seed=1)
    assert np.array_equal(miss.entry_idx, again.entry_idx)


def test_futures_costs_ticks_and_whole_contracts_for_shorts():
    bars = _walk(seed=8, n_days=60).with_columns((pl.col(c) * 40 for c in ("open", "high", "low", "close")))
    p = _p(symbol="ES")
    data = CBData(bars)
    sim = simulate_compression_breakout(data, p, exec_config=FUT, starting_equity=FUT.starting_equity)
    s = np.flatnonzero(sim.side < 0)[0]
    assert sim.entry_px[s] == pytest.approx(data.open[sim.entry_idx[s]] - 0.25)
    assert sim.quantity[s] % 50 == 0 and sim.quantity[s] > 0
    q = sim.quantity[s]
    assert sim.realized_pnl[s] == pytest.approx((sim.entry_px[s] - sim.exit_px[s]) * q - 2 * 2.5 * q / 50)
    assert check_sim_integrity(sim, data, FUT, p) == []


def test_daily_equity_matches_realized_pnl_at_flat_session_closes():
    bars = _walk(seed=9, n_days=40)
    data, sim = _sim(bars)
    eq = daily_equity(sim, data, 1e5)
    assert eq[-1] == pytest.approx(1e5 + sim.realized_pnl.sum())


# --- grid, lattice, perturbations, configs -----------------------------------------------------

def test_each_line_has_its_own_grid_without_inert_fields():
    bb, nr = cb_grid_bbkc(("ES",)), cb_grid_nr(("ES",))
    assert variants_per_symbol(AXES_BBKC_V1) == len(bb) == 20_736
    assert variants_per_symbol(AXES_NR_V1) == len(nr) == 16_128
    ids = [ce.config_id for ce in bb + nr]
    assert len(set(ids)) == len(ids)
    assert {ce.config.compression for ce in bb} == {"bbkc"} and {ce.config.compression for ce in nr} == {"nr"}
    assert "nr_lookback" not in bb[0].config.model_dump() and "squeeze_length" not in nr[0].config.model_dump()
    with pytest.raises(ValueError):
        NRBreakoutConfig(symbol="ES", squeeze_length=20)  # a squeeze setting is not an NR field
    p = CBParams.from_config(NRBreakoutConfig(symbol="ES", nr_lookback=10, stop="box", target_r="none"))
    assert (p.compression, p.nr_lookback, p.squeeze_length, p.kc_mult) == ("nr", 10, None, None)
    assert p.stop_atr is None and p.target_r is None
    p = CBParams.from_config(SqueezeBreakoutConfig(symbol="ES", kc_mult=2.0, stop="2.0", target_r="3.0"))
    assert (p.compression, p.kc_mult, p.nr_lookback, p.stop_atr, p.target_r) == ("bbkc", 2.0, None, 2.0, 3.0)


def test_lattice_neighbors_hold_categoricals():
    recs = [{"config_id": ce.config_id, **ce.config.model_dump(mode="json")} for ce in cb_grid_bbkc(("ES",))]
    nb = neighbor_ids(recs, lattice=LATTICE_CB_BBKC_V1)
    by = {r["config_id"]: r for r in recs}
    c = next(r for r in recs if r["squeeze_length"] == 20 and r["kc_mult"] == 1.5 and r["timeframe"] == "5min"
             and r["target_r"] == "2.0" and r["min_squeeze_bars"] == 1)
    ns = [by[i] for i in nb[c["config_id"]]]
    assert len(ns) == 10  # squeeze length 2 + kc 2 + min bars 1 + timeframe 1 + expiry 1 + target 2 + min box 1
    fixed = ("entry_type", "stop", "direction", "trend_filter")
    assert all(all(n[k] == c[k] for k in fixed) for n in ns)
    recs = [{"config_id": ce.config_id, **ce.config.model_dump(mode="json")} for ce in cb_grid_nr(("ES",))]
    nb = neighbor_ids(recs, lattice=LATTICE_CB_NR_V1)
    n = next(r for r in recs if r["nr_lookback"] == 7 and r["timeframe"] == "5min" and r["target_r"] == "2.0")
    ns = [i for i in nb[n["config_id"]]]
    assert len(ns) == 7  # NR-N 2 + timeframe 1 + expiry 1 + target 2 + min box 1
    by = {r["config_id"]: r for r in recs}
    assert all(by[i]["inside_bar"] == n["inside_bar"] for i in ns)  # inside bar is categorical


def test_local_and_random_perturbations():
    lcfg = SimpleNamespace(int_rel=0.2, kc_mult_abs=0.25, stop_atr_abs=0.25, target_r_abs=0.5, min_box_atr_abs=0.25)
    bb = _p(compression="bbkc", squeeze_length=20, kc_mult=1.5, min_squeeze_bars=4, stop_atr=1.0, target_r=2.0)
    moves = dict(local_perturbations_cb(bb, lcfg))
    assert sorted(moves) == ["kc_mult=1.25", "kc_mult=1.75", "min_box_atr=0.25", "min_squeeze_bars=3", "min_squeeze_bars=5",
                             "setup_expiry_bars=2", "setup_expiry_bars=4", "squeeze_length=16",
                             "squeeze_length=24", "stop_atr=0.75", "stop_atr=1.25", "target_r=1.5", "target_r=2.5"]
    nr = dict(local_perturbations_cb(_p(nr_lookback=7), lcfg))  # box stop: no stop moves
    assert sorted(nr) == ["min_box_atr=0.25", "nr_lookback=6", "nr_lookback=8", "setup_expiry_bars=2",
                          "setup_expiry_bars=4", "target_r=1.5", "target_r=2.5"]
    assert sorted(k for k in dict(local_perturbations_cb(_p(min_box_atr=0.5), lcfg)) if k.startswith("min_box")) == [
        "min_box_atr=0.25", "min_box_atr=0.75"]
    assert sorted(k for k in dict(local_perturbations_cb(_p(nr_lookback=3), lcfg)) if k.startswith("nr_")) == [
        "nr_lookback=2", "nr_lookback=4"]
    assert sorted(dict(local_perturbations_cb(replace(bb, min_squeeze_bars=1, target_r=None), lcfg))) == [
        "kc_mult=1.25", "kc_mult=1.75", "min_box_atr=0.25", "min_squeeze_bars=2", "setup_expiry_bars=2",
        "setup_expiry_bars=4",
        "squeeze_length=16", "squeeze_length=24", "stop_atr=0.75", "stop_atr=1.25"]
    pc = SimpleNamespace(n_per_config=20, integer_rel_step=0.15, float_rel_step=0.1)
    ps = perturbations_cb(bb, config_id="x", base_seed=1, pcfg=pc)
    assert len(ps) == 20 and all(q.squeeze_length != 20 and q.setup_expiry_bars != 3 for q in ps)
    assert all(q.min_squeeze_bars == 4 and q.entry_type == bb.entry_type and q.nr_lookback == bb.nr_lookback
               for q in ps)
    assert ps == perturbations_cb(bb, config_id="x", base_seed=1, pcfg=pc)
    pn = perturbations_cb(_p(), config_id="y", base_seed=1, pcfg=pc)
    assert all(q.stop_atr is None and q.squeeze_length is None and q.kc_mult is None and q.min_box_atr == 0
               for q in pn)
    pb = perturbations_cb(_p(min_box_atr=0.5, inside_bar=True), config_id="z", base_seed=1, pcfg=pc)
    assert all(q.min_box_atr != 0.5 and 0.45 <= q.min_box_atr <= 0.55 and q.inside_bar for q in pb)


def test_off_grid_kc_mult_is_not_cached():
    data = CBData(_walk(seed=1, n_days=10))
    p = _p(compression="bbkc", squeeze_length=10, min_squeeze_bars=1, nr_lookback=None)
    data.runs(replace(p, kc_mult=1.3712))
    data.runs(replace(p, kc_mult=1.5))
    keys = {k for k in data._cache if k[0] in ("comp", "runs")}
    assert all(1.3712 not in k for k in keys) and any(1.5 in k for k in keys)


# Each squeeze line lives in its own project; the v1 configs of both are checked together.
LINE_CONFIGS = {"bbkc": Path("../bbkc-squeeze-backtest/configs/funnel"), "nr": Path("../nr-squeeze-backtest/configs/funnel")}


def test_market_configs_load_and_share_every_threshold():
    shared = []
    for line, key in LINES.items():
        paths = sorted(LINE_CONFIGS[line].glob(f"cb_{line}_funnel_*_v1.yaml"))
        if not paths:
            pytest.skip(f"the {line} project is not next to this one")
        assert {p.name.split("_")[3] for p in paths} == MARKETS
        dumps = []
        for path in paths:
            f = load_funnel_config(path)
            assert f.strategy == key and family_for(f) is FAMILIES["compression_breakout"]
            loc = f.parameter_stability.local
            assert f.parameter_stability.mode == "local_perturbation" and loc.target_r_abs and loc.stop_atr_abs
            assert (loc.kc_mult_abs is not None) == (line == "bbkc") and loc.min_box_atr_abs == 0.25
            assert f.data.timeframes == ["5min", "15min"] and f.symbol.lower() == path.name.split("_")[3]
            assert not f.data_history.validation_previously_used_for_selection
            sibling = f.research_history[0]
            assert sibling.name.startswith(LINES["nr" if line == "bbkc" else "bbkc"])
            d = f.model_dump(mode="json")
            for k in ("symbol", "data_history", "research_history", "confidence"):
                d.pop(k)
            dumps.append(d)
        assert all(d == dumps[0] for d in dumps)
        d = dict(dumps[0])
        d.pop("strategy"), d["parameter_stability"].pop("local"), d["parameter_stability"].pop("perturbation")
        shared.append(d)
    assert shared[0] == shared[1]  # the lines differ only in strategy and their stage-4 / perturbation moves


def test_dev_record_through_the_funnel_family(tmp_path):
    f = load_funnel_config(CONFIGS / "cb_nr_funnel_es_v1.yaml")
    bars = _walk(seed=12, n_days=60)
    cfg = NRBreakoutConfig(symbol="SPY", timeframe="15min", nr_lookback=4)
    ce = ConfigEntry(config=cfg, config_id="abc")
    rec, rets = build_dev_record(ce, CBData(bars), fcfg=f, exec_config=EC)
    assert rec["integrity_issues"] == "" and rec["config_id"] == "abc" and rec["compression"] == "nr"
    assert "squeeze_length" not in rec
    assert rec["full_n_target_exits"] + rec["full_n_eod_exits"] + rec["full_n_stop_exits"] > 0
    assert len(rets) == 60


# --- squeeze v2 (ES round 2) -------------------------------------------------------------------

def test_v2_grids_one_per_bar_size():
    from src.experiments.cb_grid import AXES_BBKC_V2_5M, AXES_BBKC_V2_15M, cb_grid_bbkc_v2_5m, cb_grid_bbkc_v2_15m
    from src.strategies.compression_breakout.config import SqueezeBreakoutV2_5mConfig, SqueezeBreakoutV2_15mConfig
    assert variants_per_symbol(AXES_BBKC_V2_5M) == 72_576 and variants_per_symbol(AXES_BBKC_V2_15M) == 184_320
    g5, g15 = cb_grid_bbkc_v2_5m(("ES",)), cb_grid_bbkc_v2_15m(("ES",))
    assert len(g5) == 72_576 and len(g15) == 184_320
    assert {c.config.timeframe for c in g5} == {"5min"} and {c.config.timeframe for c in g15} == {"15min"}
    with pytest.raises(ValueError):
        SqueezeBreakoutV2_5mConfig(symbol="ES", timeframe="15min")
    assert {c.config.entry_type for c in g5} == {"wick"}
    with pytest.raises(ValueError):
        SqueezeBreakoutV2_5mConfig(symbol="ES", entry_type="close")  # 5m is wick-only
    with pytest.raises(ValueError):
        SqueezeBreakoutV2_15mConfig(symbol="ES", stop="1.0")  # 15m stops are 1.5 / 2.5 / 3.5 ATR
    p = CBParams.from_config(SqueezeBreakoutV2_15mConfig(symbol="ES", stop="3.5", target_r="4.0", min_box_atr=1.0))
    assert (p.stop_atr, p.target_r, p.min_box_atr, p.nr_lookback) == (3.5, 4.0, 1.0, None)


def test_squeeze_length_one_is_a_break_of_the_days_range_so_far():
    bars = _walk(seed=15, n_days=40)
    p = _p(compression="bbkc", squeeze_length=1, kc_mult=1.0, min_squeeze_bars=1, nr_lookback=None)
    data = CBData(bars)
    comp = data.compression(p)
    assert comp[1:].mean() > 0.99  # sd of one close is 0: (almost) every bar is a squeeze bar
    ru = data.runs(p)
    # (The data's first bar has no ATR yet -- true range needs a prior close -- so skip session 0.)
    ok = (ru["run_start"] >= 0) & (data.sess > 0)
    # Every run starts at the session open and its box is the session's high / low so far.
    assert np.all(ru["run_start"][ok] == data.sess_start[ok])
    for i in np.flatnonzero(ok)[::97]:
        s = data.sess_start[i]
        assert ru["box_hi"][i] == data.high[s:i + 1].max() and ru["box_lo"][i] == data.low[s:i + 1].min()
    _, sim = _sim(bars, p)
    assert len(sim.entry_idx) and len(np.unique(data.sess[sim.signal_idx])) == len(sim.signal_idx)  # once a day
    assert check_sim_integrity(sim, data, EC, p) == []


def test_off_grid_kc_cache_rule_keeps_two_decimal_values():
    data = CBData(_walk(seed=1, n_days=10))
    p = _p(compression="bbkc", squeeze_length=10, min_squeeze_bars=1, nr_lookback=None)
    for kc in (1.3, 1.55, 1.2345):
        data.runs(replace(p, kc_mult=kc))
    kcs = {k[-1] for k in data._cache if k[0] in ("comp", "runs")}
    assert {1.3, 1.55} <= kcs and 1.2345 not in kcs


# --- squeeze v3 (NQ) ---------------------------------------------------------------------------

def test_v3_grids_one_per_bar_size():
    from src.experiments.cb_grid import AXES_BBKC_V3_5M, AXES_BBKC_V3_15M, cb_grid_bbkc_v3_5m, cb_grid_bbkc_v3_15m
    from src.strategies.compression_breakout.config import SqueezeBreakoutV3_5mConfig, SqueezeBreakoutV3_15mConfig
    assert variants_per_symbol(AXES_BBKC_V3_5M) == 27_648 and variants_per_symbol(AXES_BBKC_V3_15M) == 28_800
    g5, g15 = cb_grid_bbkc_v3_5m(("NQ",)), cb_grid_bbkc_v3_15m(("NQ",))
    assert {c.config.timeframe for c in g5} == {"5min"} and {c.config.timeframe for c in g15} == {"15min"}
    assert {c.config.entry_type for c in g5} == {"wick"} and {c.config.entry_type for c in g15} == {"close", "wick"}
    with pytest.raises(ValueError):
        SqueezeBreakoutV3_15mConfig(symbol="NQ", stop="3.0")  # 15m stops are box / 1 / 2 ATR
    p = CBParams.from_config(SqueezeBreakoutV3_15mConfig(symbol="NQ", stop="2.0", target_r="1.5", min_box_atr=0.5))
    assert (p.stop_atr, p.target_r, p.min_box_atr) == (2.0, 1.5, 0.5)
    assert CBParams.from_config(SqueezeBreakoutV3_5mConfig(symbol="NQ", squeeze_length=1)).squeeze_length == 1


# --- resumable develop steps (src/experiments/job_checkpoint.py) ------------------------------

def test_checkpointed_jobs_resume_and_match_run_jobs(tmp_path, monkeypatch):
    from src.experiments import job_checkpoint as jc
    from src.experiments.funnel_prep import Job, run_jobs
    fcfg = load_funnel_config(CONFIGS / "cb_nr_funnel_es_v1.yaml")
    bars = _walk(seed=3, n_days=30)
    frames = {"SPY|15min": bars}
    d0, d1 = bars["session_date_ny"].min(), bars["session_date_ny"].max()
    jobs = [Job(f"j{k}|cost|{m}", _p(nr_lookback=k), d0, d1, cost_multiplier=m) for k in (3, 4, 5) for m in (1.0, 2.0)]
    jobs.append(Job("j4|miss|0", _p(nr_lookback=4), d0, d1, missed_entry_frac=0.5, seed=7))
    ref = run_jobs(jobs, frames, fcfg=fcfg, exec_config=EC, n_workers=1)
    kw = dict(fcfg=fcfg, exec_config=EC, n_workers=1, root=tmp_path, name="s7", fingerprint="f" * 64)

    # First run "crashes" after 3 results; with SAVE_EVERY_S = 0 each one was already saved.
    monkeypatch.setattr(jc, "SAVE_EVERY_S", 0.0)
    real, n = jc.fp._job_worker, {"k": 0}

    def flaky(job):
        n["k"] += 1
        if n["k"] > 3:
            raise KeyboardInterrupt
        return real(job)
    monkeypatch.setattr(jc.fp, "_job_worker", flaky)
    with pytest.raises(KeyboardInterrupt):
        jc.run_jobs_checkpointed(jobs, frames, **kw)
    saved = jc._load(tmp_path / "s7" / ("f" * 16))
    assert len(saved) == 3

    # Resume runs only the other 4 and returns exactly what run_jobs does.
    monkeypatch.setattr(jc.fp, "_job_worker", real)
    calls = []
    monkeypatch.setattr(jc.fp, "_job_worker", lambda job: calls.append(job.key) or real(job))
    out = jc.run_jobs_checkpointed(jobs, frames, **kw)
    assert len(calls) == 4 and set(out) == set(ref)
    for k in ref:
        assert out[k]["metrics"] == ref[k]["metrics"] and out[k]["key"] == k

    # Same backtest under a new label is reused; a changed setting or fingerprint is not.
    calls.clear()
    relabel = [Job("other", jobs[0].params, d0, d1)]
    assert jc.run_jobs_checkpointed(relabel, frames, **kw)["other"]["metrics"] == ref[jobs[0].key]["metrics"]
    assert calls == []
    jc.run_jobs_checkpointed([Job("x", jobs[0].params, d0, d1, cost_multiplier=1.5)], frames, **kw)
    jc.run_jobs_checkpointed(relabel, frames, **{**kw, "fingerprint": "e" * 64})
    assert len(calls) == 2


def test_v4_ym_grid():
    from src.experiments.cb_grid import AXES_BBKC_V4_15M, cb_grid_bbkc_v4_15m
    from src.strategies.compression_breakout.config import SqueezeBreakoutV4_15mConfig
    assert variants_per_symbol(AXES_BBKC_V4_15M) == 3_840
    g = cb_grid_bbkc_v4_15m(("YM",))
    assert {c.config.timeframe for c in g} == {"15min"} and {c.config.min_box_atr for c in g} == {0.0}
    with pytest.raises(ValueError):
        SqueezeBreakoutV4_15mConfig(symbol="YM", stop="1.0")  # stops are box / 1.5 ATR
    p = CBParams.from_config(SqueezeBreakoutV4_15mConfig(symbol="YM", stop="1.5", target_r="1.0"))
    assert (p.stop_atr, p.target_r, p.squeeze_length) == (1.5, 1.0, 25)
