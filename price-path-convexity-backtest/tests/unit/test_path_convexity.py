"""Price-path convexity: the four signal forms, the z-score, decisions (fresh cross, quadrant,
minimum move, direction, trend, cutoff), exits (time, stop, session close), integrity checks,
look-ahead, the grid / lattice / local moves and the market configs."""

from __future__ import annotations

from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import polars as pl
import pytest

from src.analysis.neighborhood import LATTICE_PC_V1_15M
from src.experiments.funnel_config import load_funnel_config
from src.experiments.funnel_prep import build_dev_record, family_for
from src.experiments.funnel_robustness import local_perturbations_pc, perturbations_pc
from src.experiments.mr_grid import ConfigEntry
from src.experiments.pc_grid import AXES_PC_V1_15M, pc_grid_v1_5m, pc_grid_v1_15m, variants_per_symbol
from src.experiments.pc_integrity import check_sim_integrity, independent_signal, independent_z, truncation_invariance
from src.strategies.path_convexity.backtest import PCData, PCParams, max_gap, signals, simulate_path_convexity
from src.strategies.path_convexity.config import ConvexityV1_15mConfig, hold_bars
from src.utils.config_models import ExecutionConfig

FUT = ExecutionConfig(starting_equity=1_000_000, instrument_type="futures", commission_per_contract=2.5,
                      slippage_ticks_market=1.0, slippage_ticks_stop=1.0, commission_per_share=0.0,
                      commission_minimum=0.0, slippage_bps_market=0.0, slippage_bps_stop=0.0)
P = PCParams("ES", "15min", lookback=8, signal_form="paper", z_lookback=40, entry_z=1.0, quadrant="all",
             min_move_atr=0.0, direction="both", hold="full", stop_atr=None, trend_filter="none")


def _p(**kw) -> PCParams:
    return replace(P, **kw)


def _bars(closes_by_day: list[np.ndarray], start=date(2020, 1, 6)) -> pl.DataFrame:
    """15-min RTH bars from closes: open = previous close, high / low 0.25 around the bar."""
    rows, d, prev = [], start, None
    for closes in closes_by_day:
        while d.weekday() >= 5:
            d += timedelta(days=1)
        t0 = datetime(d.year, d.month, d.day, 14, 30, tzinfo=timezone.utc)
        for i, c in enumerate(closes):
            o = c if prev is None else prev
            rows.append({"bar_open_ts": t0 + timedelta(minutes=15 * i), "session_date_ny": d, "open": float(o),
                         "high": float(max(o, c) + 0.25), "low": float(min(o, c) - 0.25), "close": float(c)})
            prev = c
        d += timedelta(days=1)
    return pl.DataFrame(rows)


def _walk(n_days=80, per_day=26, seed=0) -> pl.DataFrame:
    rng = np.random.default_rng(seed)
    px, days = 3000.0, []
    for _ in range(n_days):
        steps = rng.normal(0, 2.0, per_day) * np.where(rng.random(per_day) < 0.2, 3, 1)
        c = px + np.cumsum(steps)
        days.append(c)
        px = c[-1]
    return _bars(days)


# --- signal forms -------------------------------------------------------------------------------

def test_paper_convexity_matches_formula():
    c = np.array([100, 100, 100, 100, 110.0])  # late jump: convex
    d = PCData(_bars([c]))
    s = d.signal("paper", 5)
    mid, mean = (100 + 110) / 2, c.mean()
    assert s[4] == pytest.approx((mid - mean) / mid)
    assert s[4] > 0
    assert np.isnan(s[:4]).all()


def test_concave_path_is_negative():
    c = np.array([100, 110, 110, 110, 110.0])  # early jump: concave
    assert PCData(_bars([c])).signal("paper", 5)[4] < 0


def test_atr_form_is_gap_over_atr_and_reversal_is_move_over_atr():
    d = PCData(_walk(3))
    a = d.atr(14)
    k = 40
    w = d.close[k - 7:k + 1]
    gap = (w[0] + w[-1]) / 2 - w.mean()
    assert d.signal("atr", 8)[k] == pytest.approx(gap / a[k])
    assert d.signal("reversal", 8)[k] == pytest.approx((w[-1] - w[0]) / a[k])


def test_max_gap_takes_largest_signed_gap():
    c = np.array([0.0, 1.0, -3.0, 3.0, 4.0])  # line 0..4: gaps 0, 0, 5, 0, 0 -> +5
    assert max_gap(c, 5)[4] == pytest.approx(5.0)
    c2 = np.array([0.0, 4.0, 2.0, 3.0, 4.0])   # gaps 0, -3, 0, 0, 0 -> -3
    assert max_gap(c2, 5)[4] == pytest.approx(-3.0)


@pytest.mark.parametrize("form", ["paper", "atr", "maxgap", "reversal"])
def test_independent_signal_and_z_agree_with_backtester(form):
    d = PCData(_walk(20))
    a = d.atr(14)
    np.testing.assert_allclose(d.signal(form, 12), independent_signal(d.close, a, form, 12), rtol=1e-9, atol=1e-12)
    np.testing.assert_allclose(d.zscore(form, 12, 50), independent_z(d.signal(form, 12), 50), rtol=1e-7, atol=1e-9)


def test_signal_is_causal():
    b = _walk(10)
    full = PCData(b).zscore("atr", 12, 50)
    part = PCData(b.head(150)).zscore("atr", 12, 50)
    np.testing.assert_allclose(part, full[:150], equal_nan=True)


# --- decisions ------------------------------------------------------------------------------------

def test_fresh_cross_only_and_high_signal_shorts():
    d = PCData(_walk(40))
    st = signals(d, _p(signal_form="atr"))
    z = d.zscore("atr", 8, 40)
    for k, s in zip(st["k"], st["side"]):
        if s < 0:
            assert z[k] >= 1.0 and not z[k - 1] >= 1.0
        else:
            assert z[k] <= -1.0 and not z[k - 1] <= -1.0


def test_quadrants_partition_all():
    d = PCData(_walk(40))
    all_k = set(signals(d, _p(signal_form="atr"))["k"].tolist())
    late = signals(d, _p(signal_form="atr", quadrant="late"))
    early = signals(d, _p(signal_form="atr", quadrant="early"))
    assert set(late["k"].tolist()) | set(early["k"].tolist()) <= all_k
    assert not set(late["k"].tolist()) & set(early["k"].tolist())
    m = d.net_move(8)
    assert (late["side"] == -np.sign(m[late["k"]])).all()
    assert (early["side"] == np.sign(m[early["k"]])).all()


def test_reversal_control_is_mostly_late():
    d = PCData(_walk(40))
    a = len(signals(d, _p(signal_form="reversal"))["k"])
    early = len(signals(d, _p(signal_form="reversal", quadrant="early"))["k"])
    late = len(signals(d, _p(signal_form="reversal", quadrant="late"))["k"])
    assert early + late == a and early < 0.1 * a


def test_filters_min_move_direction_cutoff():
    d = PCData(_walk(40))
    st = signals(d, _p(signal_form="atr", min_move_atr=1.0, direction="long"))
    assert (st["side"] > 0).all()
    assert (np.abs(d.net_move(8)[st["k"]]) >= d.atr(14)[st["k"]]).all()
    to_close = d.tod[d.sess_end[st["k"]]] - d.tod[st["k"]]
    assert (to_close >= 30).all() and not d.is_last[st["k"]].any()


# --- execution --------------------------------------------------------------------------------------

def test_hold_bars():
    assert hold_bars("full", 24) == 24 and hold_bars("half", 24) == 12 and hold_bars("half", 7) == 4
    assert hold_bars("session", 24) is None


def test_time_exit_after_n_bars_and_never_overnight():
    d = PCData(_walk(60))
    sim = simulate_path_convexity(d, _p(signal_form="atr", lookback=4, hold="full"), exec_config=FUT,
                                  starting_equity=1e6)
    assert len(sim.entry_idx) > 5
    for e, x, why in zip(sim.entry_idx, sim.exit_idx, sim.exit_reason):
        assert d.sess[e] == d.sess[x]
        if why == "time_exit":
            assert x == e + 3
        assert x - e <= 3
    assert (sim.entry_idx == sim.signal_idx + 1).all()


def test_session_hold_exits_at_close_and_stop_hits():
    d = PCData(_walk(60))
    sim = simulate_path_convexity(d, _p(signal_form="atr", hold="session", stop_atr=0.5), exec_config=FUT,
                                  starting_equity=1e6)
    reasons = set(sim.exit_reason.tolist())
    assert "stop_exit" in reasons and "time_exit" not in reasons
    for x, why in zip(sim.exit_idx, sim.exit_reason):
        if why == "eod_exit":
            assert x == d.sess_end[x]


@pytest.mark.parametrize("form,quad,stop,hold,trend", [
    ("paper", "all", None, "full", "none"), ("atr", "late", 1.5, "half", "ema50"),
    ("maxgap", "early", 2.5, "session", "none"), ("reversal", "all", 1.5, "full", "ema200")])
def test_integrity_clean_and_no_lookahead(form, quad, stop, hold, trend):
    b = _walk(80)
    p = _p(signal_form=form, quadrant=quad, stop_atr=stop, hold=hold, trend_filter=trend, lookback=12)
    d = PCData(b)
    sim = simulate_path_convexity(d, p, exec_config=FUT, starting_equity=1e6)
    assert check_sim_integrity(sim, d, FUT, p) == []
    assert truncation_invariance(b, p, exec_config=FUT) == []


def test_integrity_catches_tampering():
    d = PCData(_walk(60))
    p = _p(signal_form="atr", stop_atr=1.5)
    sim = simulate_path_convexity(d, p, exec_config=FUT, starting_equity=1e6)
    assert len(sim.entry_idx) > 3
    bad = replace(sim, side=-sim.side)
    assert "side_not_per_signal" in check_sim_integrity(bad, d, FUT, p)
    bad = replace(sim, exit_idx=sim.exit_idx + 0, entry_px=sim.entry_px - sim.side * 5.0)
    assert "entry_fill_better_than_market" in check_sim_integrity(bad, d, FUT, p)
    bad = replace(sim, signal_idx=sim.signal_idx[1:], entry_idx=sim.entry_idx[1:], exit_idx=sim.exit_idx[1:],
                  side=sim.side[1:], entry_base=sim.entry_base[1:], entry_px=sim.entry_px[1:],
                  exit_px=sim.exit_px[1:], stop_level=sim.stop_level[1:], exit_reason=sim.exit_reason[1:],
                  quantity=sim.quantity[1:], realized_pnl=sim.realized_pnl[1:],
                  entry_commission=sim.entry_commission[1:], forced_close=sim.forced_close[1:])
    assert "signal_skipped_while_flat" in check_sim_integrity(bad, d, FUT, p)


def test_stress_knobs():
    d = PCData(_walk(60))
    p = _p(signal_form="atr")
    base = simulate_path_convexity(d, p, exec_config=FUT, starting_equity=1e6)
    late = simulate_path_convexity(d, p, exec_config=FUT, starting_equity=1e6, entry_delay_bars=1)
    assert late.entry_idx[0] == base.entry_idx[0] + 1  # later trades shift with the first one
    miss = simulate_path_convexity(d, p, exec_config=FUT, starting_equity=1e6, missed_entry_frac=0.5, stress_seed=3)
    assert len(miss.entry_idx) < len(base.entry_idx)


# --- grid, lattice, local moves, configs ----------------------------------------------------------

def test_grid_size_and_ids():
    assert variants_per_symbol(AXES_PC_V1_15M) == 186_624
    g = pc_grid_v1_15m(("ES",))
    assert len(g) == 186_624 == len({ce.config_id for ce in g})
    assert pc_grid_v1_5m(("ES",))[0].config.timeframe == "5min"


def test_lattice_covers_grid_values():
    for ax, vals in AXES_PC_V1_15M.items():
        if ax in LATTICE_PC_V1_15M.ordered:
            assert set(vals) == set(LATTICE_PC_V1_15M.ordered[ax]), ax
        else:
            assert ax in LATTICE_PC_V1_15M.fixed, ax


def test_local_moves():
    from types import SimpleNamespace
    lcfg = SimpleNamespace(int_rel=0.2, entry_z_abs=0.25, stop_atr_abs=0.25, min_move_atr_abs=0.5)
    mv = dict(local_perturbations_pc(_p(lookback=24, z_lookback=250, stop_atr=1.5, min_move_atr=0.0), lcfg))
    assert set(mv) == {"lookback=19", "lookback=29", "z_lookback=200", "z_lookback=300", "entry_z=0.75",
                       "entry_z=1.25", "stop_atr=1.25", "stop_atr=1.75", "min_move_atr=0.5"}
    mv = dict(local_perturbations_pc(_p(stop_atr=None), lcfg))
    assert not any(k.startswith("stop_atr") for k in mv)
    pert = perturbations_pc(_p(), config_id="x", base_seed=1,
                            pcfg=SimpleNamespace(n_per_config=5, integer_rel_step=0.15, float_rel_step=0.1))
    assert len(pert) == 5 and all(q.signal_form == "paper" and q.lookback != 8 or q.lookback >= 3 for q in pert)


@pytest.mark.parametrize("tf", ["15m", "5m"])
def test_market_configs_load(tf):
    f = load_funnel_config(Path(f"configs/funnel/pc_funnel_es_v1_{tf}.yaml"))
    assert f.strategy == f"path_convexity_v1_{tf}" and f.symbol == "ES"
    assert family_for(f).simulate is simulate_path_convexity


def test_dev_record_runs():
    f = load_funnel_config(Path("configs/funnel/pc_funnel_es_v1_15m.yaml"))
    b = _walk(40)
    cfg = ConvexityV1_15mConfig(symbol="ES", lookback=8, signal_form="atr", z_lookback=250)
    rec, rets = build_dev_record(ConfigEntry(cfg, "abc"), PCData(b), fcfg=f, exec_config=FUT)
    assert rec["integrity_issues"] == "" and len(rets) == len(PCData(b).days)
