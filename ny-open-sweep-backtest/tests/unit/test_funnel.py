"""Screening funnel: threshold boundaries, missing metrics, neighborhood
membership, representative selection, dedup linkage, and reporting."""

from __future__ import annotations

import numpy as np
import pytest

from src.analysis.neighborhood import NeighborhoodStats, neighbor_ids, neighborhood_stats
from src.experiments.funnel import (
    DEDUPLICATED,
    HARD_REJECT,
    INSUFFICIENT,
    PASS,
    cluster_by_correlation,
    monthly_returns,
    representative_key,
    select_representatives,
    stage1_integrity,
    stage2_trade_count,
    stage3_performance,
    stage4_parameter_stability,
    stage5_time_stability,
    survivor_table,
)
from src.experiments.funnel_config import load_funnel_config
from src.experiments.funnel_robustness import breakeven_multiplier, interval_overlap, perturbations
from src.strategies.mean_reversion.backtest import MRParams

FCFG = load_funnel_config()
YEARS = FCFG.dev_years


def _rec(cid="c", **kw):
    base = {"config_id": cid, "symbol": "SPY", "timeframe": "15min", "mean_type": "sma", "mean_lookback": 10,
            "std_lookback": 20, "entry_z": -1.0, "exit_z": 0.0, "max_hold": 2, "trend_filter": "none",
            "integrity_issues": "", "dev_n_completed_trades": 200, "dev_net_return": 0.1, "dev_sharpe": 1.0,
            "dev_max_drawdown": -0.1, "dev_concurrent_overlap_trades": 0, "dev_same_session_trade_frac": 0.0}
    for y in YEARS:
        base[f"dev_year_trades_{y}"] = 40
        base[f"dev_year_return_{y}"] = 0.02
    base.update(kw)
    return base


def _with(cfg, section, **kw):
    return cfg.model_copy(update={section: getattr(cfg, section).model_copy(update=kw)})


# --- configuration -------------------------------------------------------------------

def test_config_has_requested_defaults_and_stable_hash():
    c = FCFG
    assert (c.trade_count.min_completed_trades, c.trade_count.min_trades_per_year,
            c.trade_count.min_years_meeting_floor) == (150, 10, 4)
    assert (c.performance.min_sharpe, c.performance.max_drawdown) == (0.75, -0.30)
    assert (c.parameter_stability.min_frac_profitable, c.parameter_stability.min_median_sharpe) == (0.70, 0.30)
    assert c.time_stability.min_profitable_years == 3
    assert (c.dedup.corr_threshold, c.dedup.linkage) == (0.80, "complete")
    assert c.execution_stress.gate_cost_multiplier == 1.5 and c.execution_stress.missed_entry_sims == 100
    assert (c.validation.min_sharpe, c.validation.min_completed_trades) == (0.30, 60)
    assert c.confidence.dsr_threshold == 0.95
    assert c.data_history.holdout_previously_inspected  # never described as untouched
    assert c.config_sha256() == load_funnel_config().config_sha256()
    assert _with(c, "performance", min_sharpe=0.8).config_sha256() != c.config_sha256()


# --- stage 1/2 -----------------------------------------------------------------------

def test_stage1_rejects_integrity_issues():
    assert stage1_integrity(_rec()).status == PASS
    out = stage1_integrity(_rec(integrity_issues="overlapping_positions"))
    assert out.status == HARD_REJECT and "integrity:overlapping_positions" in out.reasons


def test_stage2_boundaries():
    assert stage2_trade_count(_rec(dev_n_completed_trades=150), FCFG).status == PASS
    assert stage2_trade_count(_rec(dev_n_completed_trades=149), FCFG).status == HARD_REJECT
    # exactly 4 years at the 10-trade floor passes; 3 fails
    four = {f"dev_year_trades_{y}": (10 if i < 4 else 9) for i, y in enumerate(YEARS)}
    three = {f"dev_year_trades_{y}": (10 if i < 3 else 9) for i, y in enumerate(YEARS)}
    assert stage2_trade_count(_rec(**four), FCFG).status == PASS
    assert stage2_trade_count(_rec(**three), FCFG).status == HARD_REJECT


def test_stage2_reports_years_and_flags_clustering():
    out = stage2_trade_count(_rec(dev_concurrent_overlap_trades=2, dev_same_session_trade_frac=0.4), FCFG)
    assert out.diagnostics["trades_by_year"] == {y: 40 for y in YEARS}
    assert any("overlapping_positions" in w for w in out.warnings)
    assert any("same_session" in w for w in out.warnings)


# --- stage 3 -------------------------------------------------------------------------

def test_stage3_boundaries():
    assert stage3_performance(_rec(dev_sharpe=0.75), FCFG).status == PASS
    assert stage3_performance(_rec(dev_sharpe=0.7499), FCFG).status == HARD_REJECT
    assert stage3_performance(_rec(dev_net_return=0.0), FCFG).status == HARD_REJECT  # strictly positive
    assert stage3_performance(_rec(dev_max_drawdown=-0.30), FCFG).status == PASS
    assert stage3_performance(_rec(dev_max_drawdown=-0.3001), FCFG).status == HARD_REJECT


def test_stage3_missing_metrics_are_insufficient_not_silent():
    out = stage3_performance(_rec(dev_sharpe=None), FCFG)
    assert out.status == INSUFFICIENT and "sharpe_undefined" in out.reasons
    # an undefined metric never hides a real hard failure
    assert stage3_performance(_rec(dev_sharpe=None, dev_net_return=-0.1), FCFG).status == HARD_REJECT


def test_stage3_unset_risk_limit_flags_incomplete_approval():
    cfg = _with(FCFG, "performance", max_drawdown=None)
    out = stage3_performance(_rec(dev_max_drawdown=-0.9), cfg)
    assert out.status == PASS  # no limit invented
    assert "risk_limit_unset:risk_approval_incomplete" in out.warnings


# --- stage 4 -------------------------------------------------------------------------

def _ns(n=10, frac=0.8, med=0.5, boundary=()):
    return NeighborhoodStats(n, 12, frac if n else None, med, 0, list(boundary))


def test_stage4_boundaries():
    assert stage4_parameter_stability(_ns(frac=0.70, med=0.30), 1.0, FCFG).status == PASS
    assert stage4_parameter_stability(_ns(frac=0.69, med=0.30), 1.0, FCFG).status == HARD_REJECT
    assert stage4_parameter_stability(_ns(frac=0.70, med=0.299), 1.0, FCFG).status == HARD_REJECT


def test_stage4_no_neighbors_is_insufficient_and_boundary_reported():
    out = stage4_parameter_stability(_ns(n=0, med=None), 1.0, FCFG)
    assert out.status == INSUFFICIENT and "no_valid_neighbors" in out.reasons
    out = stage4_parameter_stability(_ns(boundary=("max_hold",)), 1.0, FCFG)
    assert out.status == PASS and any("limited_neighborhood" in w for w in out.warnings)
    assert out.diagnostics["center_minus_median_sharpe"] == pytest.approx(0.5)


def _grid_recs():
    recs = []
    for lb in (5, 10, 15):
        for sd in (10, 15, 20):
            recs.append(_rec(f"{lb}_{sd}", mean_lookback=lb, std_lookback=sd))
    return recs


def test_neighbors_are_immediate_single_axis_from_full_universe():
    recs = _grid_recs()
    ids = neighbor_ids(recs)
    assert sorted(ids["10_15"]) == sorted(["5_15", "15_15", "10_10", "10_20"])  # no diagonals
    assert sorted(ids["5_10"]) == sorted(["10_10", "5_15"])
    # neighbors include configs rejected upstream: center stats see losing neighbors
    for r in recs:
        if r["config_id"] != "10_15":
            r["dev_net_return"], r["dev_sharpe"] = -0.1, -0.5
    ns = neighborhood_stats(recs, net_return_key="dev_net_return", sharpe_key="dev_sharpe", only_ids={"10_15"})
    assert set(ns) == {"10_15"}
    assert ns["10_15"].n_neighbors == 4 and ns["10_15"].frac_profitable == 0.0
    # 15min (middle), mean 10, std 15 interior: 2+2+2; entry_z=-1.0, max_hold=2 on edges, exit_z=0.0 interior
    assert ns["10_15"].n_possible == 2 + 2 + 2 + 1 + 2 + 1
    assert sorted(ns["10_15"].boundary_axes) == ["entry_z", "max_hold"]


def test_neighbor_order_and_categoricals_fixed():
    a = _rec("e10", entry_z=-1.0)
    b = _rec("e125", entry_z=-1.25)
    c = _rec("e15", entry_z=-1.5)
    d = _rec("ema", entry_z=-1.25, mean_type="ema")
    t = _rec("trend", entry_z=-1.25, trend_filter="sma200")
    ids = neighbor_ids([a, b, c, d, t])
    assert sorted(ids["e125"]) == ["e10", "e15"]     # adjacent z thresholds only
    assert ids["e10"] == ["e125"]                   # -1.0 is the shallow edge
    assert ids["ema"] == [] and ids["trend"] == []  # mean_type / trend_filter are never neighbors
    ns = neighborhood_stats([a, b, c], net_return_key="dev_net_return", sharpe_key="dev_sharpe")
    assert "entry_z" in ns["e10"].boundary_axes and ns["e10"].limited_coverage


def test_neighbor_with_undefined_sharpe_counted_separately():
    recs = _grid_recs()
    recs[1]["dev_sharpe"] = None  # 5_15 is a neighbor of 10_15
    ns = neighborhood_stats(recs, net_return_key="dev_net_return", sharpe_key="dev_sharpe")
    assert ns["10_15"].n_sharpe_undefined == 1 and ns["10_15"].n_neighbors == 4


# --- stage 5 -------------------------------------------------------------------------

def test_stage5_boundary_and_diagnostics_are_not_gates():
    three = {f"dev_year_return_{y}": (0.05 if i < 3 else -0.01) for i, y in enumerate(YEARS)}
    two = {f"dev_year_return_{y}": (0.05 if i < 2 else -0.01) for i, y in enumerate(YEARS)}
    assert stage5_time_stability(_rec(**three), FCFG).status == PASS
    assert stage5_time_stability(_rec(**two), FCFG).status == HARD_REJECT
    out = stage5_time_stability(_rec(**three, dev_excl_best_year_return=-0.02, dev_best_year_contribution=None), FCFG)
    assert out.status == PASS
    assert "non_positive_without_best_year" in out.warnings and "contribution_ratios_undefined" in out.warnings


# --- stage 6 -------------------------------------------------------------------------

def test_complete_linkage_prevents_correlation_chaining():
    rng = np.random.default_rng(0)
    x, z = rng.normal(size=60), rng.normal(size=60)
    a = x
    c = 0.6 * x + 0.8 * z            # corr(a, c) ~ 0.6
    b = (a + c) / np.linalg.norm(a + c) * np.linalg.norm(a)  # ~0.9 with both a and c
    series = np.vstack([a, b, c])
    ca = np.corrcoef(series)
    assert ca[0, 1] > 0.8 and ca[1, 2] > 0.8 and ca[0, 2] < 0.8
    single = cluster_by_correlation(["a", "b", "c"], series, threshold=0.8, method="single")
    complete = cluster_by_correlation(["a", "b", "c"], series, threshold=0.8, method="complete")
    assert len(set(single.values())) == 1          # chaining glues a and c
    assert complete["a"] != complete["c"]          # complete linkage does not
    for k in set(complete.values()):
        members = [i for i, n in enumerate("abc") if complete[n] == k]
        assert all(ca[i, j] >= 0.8 for i in members for j in members)


def test_identical_series_cluster_together_and_relabel_deterministically():
    s = np.vstack([np.linspace(0, 1, 30), np.linspace(0, 1, 30) + 1e-6, np.sin(np.arange(30))])
    out = cluster_by_correlation(["z", "y", "x"], s, threshold=0.8)
    assert out["z"] == out["y"] != out["x"]
    assert out["x"] == 0  # cluster ids ordered by smallest member id


def test_representative_selection_order_and_tiebreaks():
    m = [
        {"config_id": "d", "neighbor_median_sharpe": 0.6, "n_profitable_years": 4, "dev_sharpe": 1.0},
        {"config_id": "c", "neighbor_median_sharpe": 0.6, "n_profitable_years": 5, "dev_sharpe": 0.8},
        {"config_id": "b", "neighbor_median_sharpe": 0.6, "n_profitable_years": 5, "dev_sharpe": 0.9},
        {"config_id": "a", "neighbor_median_sharpe": 0.6, "n_profitable_years": 5, "dev_sharpe": 0.9},
        {"config_id": "e", "neighbor_median_sharpe": 0.7, "n_profitable_years": 3, "dev_sharpe": 0.5},
    ]
    assert [r["config_id"] for r in sorted(m, key=representative_key)] == ["e", "a", "b", "c", "d"]
    reps = select_representatives(m, {"a": 0, "b": 0, "c": 0, "d": 1, "e": 1})
    assert [r["config_id"] for r in reps] == ["e", "a"]  # one per cluster, development ordering
    # missing metrics sort last rather than crashing
    assert representative_key({"config_id": "x", "neighbor_median_sharpe": None}) > representative_key(m[0])


def test_monthly_returns_compound_daily():
    days = np.array(["2020-01-02", "2020-01-03", "2020-02-03"], dtype="datetime64[D]")
    m = monthly_returns(np.array([[0.1, 0.1, -0.5]]), days)
    assert m[0] == pytest.approx([0.21, -0.5])


# --- stage 7 / diagnostics helpers ----------------------------------------------------

def test_breakeven_interpolation_and_edge_cases():
    be, st = breakeven_multiplier([1.0, 2.0, 3.0], [0.10, 0.02, -0.02])
    assert st == "interpolated" and be == pytest.approx(2.5)
    assert breakeven_multiplier([1.0, 2.0], [0.1, 0.05])[1] == "profitable_beyond_2.0x"
    assert breakeven_multiplier([1.0, 2.0], [-0.1, -0.2])[0] is None


def test_perturbations_reproducible_and_categoricals_untouched():
    p = MRParams("SPY", "15min", "ema", 20, 40, -1.5, 0.25, 5, "sma200")
    pc = FCFG.parameter_stability.perturbation
    a = perturbations(p, config_id="abc", base_seed=1, pcfg=pc)
    assert len(a) == pc.n_per_config
    assert a == perturbations(p, config_id="abc", base_seed=1, pcfg=pc)
    assert a != perturbations(p, config_id="abd", base_seed=1, pcfg=pc)
    for q in a:
        assert (q.timeframe, q.mean_type, q.trend_filter, q.symbol) == ("15min", "ema", "sma200", "SPY")
        assert q.mean_lookback != 20 and abs(q.mean_lookback - 20) <= 3
        assert q.std_lookback != 40 and abs(q.std_lookback - 40) <= 6
        assert q.max_hold != 5 and abs(q.max_hold - 5) <= 1 and q.max_hold >= 1
        assert abs(q.entry_z + 1.5) <= pc.z_abs and abs(q.exit_z - 0.25) <= pc.z_abs
        assert q.entry_z < q.exit_z


def test_interval_overlap():
    from datetime import datetime as dt
    a = [(dt(2020, 1, 1, 10), dt(2020, 1, 1, 12))]
    b = [(dt(2020, 1, 1, 11), dt(2020, 1, 1, 13))]
    assert interval_overlap(a, b) == pytest.approx(1 / 3)
    assert interval_overlap(a, a) == pytest.approx(1.0)
    assert interval_overlap([], []) is None


def test_survivor_table_percentages_and_zero_survivors():
    t = survivor_table([
        {"stage": "0", "kind": "universe", "evaluated": 100, "passed": 100},
        {"stage": "2", "kind": "hard_gate", "evaluated": 100, "passed": 20},
        {"stage": "9", "kind": "diagnostic_only", "evaluated": 20, "passed": 5},
        {"stage": "3", "kind": "hard_gate", "evaluated": 20, "passed": 0},
        {"stage": "8", "kind": "hard_gate", "evaluated": None, "passed": None},
    ], 100)
    assert t[1]["pct_of_universe"] == 20 and t[1]["pct_of_previous"] == 20
    assert t[3]["pct_of_previous"] == 0  # diagnostic row does not shrink the base
    assert t[4]["pct_of_universe"] is None


def test_status_vocabulary_distinct():
    assert len({PASS, HARD_REJECT, INSUFFICIENT, DEDUPLICATED}) == 4


def test_large_cluster_path_matches_dense_path(monkeypatch):
    import src.experiments.funnel as fn
    rng = np.random.default_rng(5)
    base = rng.normal(size=(12, 60))
    X = np.vstack([base + rng.normal(scale=s, size=base.shape) for s in (0.05, 0.4, 1.5)] + [base[:4]])  # + exact copies
    X[7] = 0.0  # a flat row
    ids = [f"c{i:03d}" for i in range(len(X))]
    dense = fn.cluster_by_correlation(ids, X, threshold=0.8)
    monkeypatch.setattr(fn, "LARGE_CLUSTER_N", 0)
    light = fn.cluster_by_correlation(ids, X, threshold=0.8)
    assert dense == light


def test_grouped_large_clusters_never_cross_groups(monkeypatch):
    import src.experiments.funnel as fn
    rng = np.random.default_rng(9)
    base = rng.normal(size=(6, 60))
    X = np.vstack([base, base + rng.normal(scale=0.05, size=base.shape)])
    ids = [f"c{i:03d}" for i in range(len(X))]
    groups = ["a"] * 6 + ["b"] * 6
    monkeypatch.setattr(fn, "LARGE_CLUSTER_N", 0)
    together = fn.cluster_by_correlation(ids, X, threshold=0.8)
    split = fn.cluster_by_correlation(ids, X, threshold=0.8, groups=groups)
    assert len(set(together.values())) == 6 and len(set(split.values())) == 12
    for i in range(6):  # a series and its near-copy share a cluster only when they share a group
        assert together[ids[i]] == together[ids[i + 6]] and split[ids[i]] != split[ids[i + 6]]
