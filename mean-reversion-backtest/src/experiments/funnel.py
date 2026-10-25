"""Pure (no-backtest) stage logic for the strategy-screening funnel.

Stages (configs/funnel/mr_funnel.yaml holds every threshold):
  1  backtest integrity           hard gate (per-config checks + run-level look-ahead test)
  2  trade count & coverage       hard gate
  3  performance & risk           hard gate
  4  parameter stability          hard gate (+ perturbation diagnostics)
  5  time stability               light hard gate (+ in-sample diagnostics)
  6  deduplication                best-k representatives per cluster (not a rejection)
  7  execution stress             hard gate (+ diagnostics)
  8  frozen validation            hard gate, separate `validate` command
  9  statistical confidence       diagnostics only (DSR, QQQ transfer)
  10 final holdout                separate, explicit `final-test` command only

Every config gets a status per stage from a fixed vocabulary so hard
rejections, missing evidence, diagnostic warnings and deduplication are never
conflated. Thresholds are read, never tuned; zero survivors is a valid outcome.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform

from src.analysis.neighborhood import NeighborhoodStats
from src.experiments.funnel_config import FunnelConfig

PASS = "pass"
HARD_REJECT = "hard_reject"
INSUFFICIENT = "insufficient_evidence"
DEDUPLICATED = "deduplicated"
NOT_EVALUATED = "not_evaluated"
DIAGNOSTIC = "diagnostic_only"


@dataclass
class Outcome:
    status: str
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    diagnostics: dict = field(default_factory=dict)


def _resolve(hard: list[str], insufficient: list[str], warnings: list[str], diag: dict | None = None) -> Outcome:
    if hard:
        return Outcome(HARD_REJECT, hard + insufficient, warnings, diag or {})
    if insufficient:
        return Outcome(INSUFFICIENT, insufficient, warnings, diag or {})
    return Outcome(PASS, [], warnings, diag or {})


# --- Stage 1 -----------------------------------------------------------------

def stage1_integrity(rec: dict) -> Outcome:
    issues = [x for x in (rec.get("integrity_issues") or "").split(";") if x]
    return _resolve([f"integrity:{x}" for x in issues], [], [])


# --- Stage 2 -----------------------------------------------------------------

def stage2_trade_count(rec: dict, fcfg: FunnelConfig) -> Outcome:
    t = fcfg.trade_count
    years = fcfg.dev_years
    per_year = {y: int(rec.get(f"dev_year_trades_{y}") or 0) for y in years}
    n_ok_years = sum(1 for c in per_year.values() if c >= t.min_trades_per_year)
    completed = int(rec.get("dev_n_completed_trades") or 0)
    hard = []
    if completed < t.min_completed_trades:
        hard.append(f"completed_trades {completed} < {t.min_completed_trades}")
    if n_ok_years < t.min_years_meeting_floor:
        hard.append(f"years_with_>={t.min_trades_per_year}_trades {n_ok_years} < {t.min_years_meeting_floor}")
    warn = []
    if (rec.get("dev_concurrent_overlap_trades") or 0) > 0:
        warn.append("overlapping_positions_reduce_independence")
    ssf = rec.get("dev_same_session_trade_frac")
    if ssf is not None and ssf > 0:
        warn.append(f"same_session_trades_frac={ssf:.2f}")
    return _resolve(hard, [], warn, {"trades_by_year": per_year, "years_meeting_floor": n_ok_years})


# --- Stage 3 -----------------------------------------------------------------

def stage3_performance(rec: dict, fcfg: FunnelConfig) -> Outcome:
    p = fcfg.performance
    hard, insuff, warn = [], [], []
    nr = rec.get("dev_net_return")
    if nr is None:
        insuff.append("net_return_undefined")
    elif not nr > p.min_net_return:
        hard.append(f"net_return {nr:.4f} <= {p.min_net_return}")
    sh = rec.get("dev_sharpe")
    if sh is None:
        insuff.append("sharpe_undefined")
    elif sh < p.min_sharpe:
        hard.append(f"sharpe {sh:.3f} < {p.min_sharpe}")
    dd = rec.get("dev_max_drawdown")
    if p.max_drawdown is None:
        warn.append("risk_limit_unset:risk_approval_incomplete")
    elif dd is None:
        insuff.append("max_drawdown_undefined")
    elif dd < p.max_drawdown:
        hard.append(f"max_drawdown {dd:.3f} < {p.max_drawdown}")
    return _resolve(hard, insuff, warn)


# --- Stage 4 -----------------------------------------------------------------

def stage4_parameter_stability(ns: NeighborhoodStats, center_sharpe: float | None,
                               fcfg: FunnelConfig) -> Outcome:
    s = fcfg.parameter_stability
    diag = {"n_neighbors": ns.n_neighbors, "n_possible_neighbors": ns.n_possible,
            "frac_profitable": ns.frac_profitable, "median_sharpe": ns.median_sharpe,
            "center_minus_median_sharpe": (center_sharpe - ns.median_sharpe
                                           if center_sharpe is not None and ns.median_sharpe is not None else None),
            "n_sharpe_undefined": ns.n_sharpe_undefined, "boundary_axes": ",".join(ns.boundary_axes)}
    warn = []
    if ns.limited_coverage:
        warn.append(f"limited_neighborhood_at_boundary:{','.join(ns.boundary_axes)}")
    if ns.n_sharpe_undefined:
        warn.append(f"neighbors_with_undefined_sharpe={ns.n_sharpe_undefined}")
    if ns.n_neighbors == 0:
        return _resolve([], ["no_valid_neighbors"], warn, diag)
    hard, insuff = [], []
    if ns.frac_profitable < s.min_frac_profitable:
        hard.append(f"neighbor_frac_profitable {ns.frac_profitable:.2f} < {s.min_frac_profitable}")
    if ns.median_sharpe is None:
        insuff.append("no_neighbor_sharpe_defined")
    elif ns.median_sharpe < s.min_median_sharpe:
        hard.append(f"neighbor_median_sharpe {ns.median_sharpe:.3f} < {s.min_median_sharpe}")
    return _resolve(hard, insuff, warn, diag)


# --- Stage 5 -----------------------------------------------------------------

def stage5_time_stability(rec: dict, fcfg: FunnelConfig) -> Outcome:
    t = fcfg.time_stability
    years = fcfg.dev_years
    n_prof = sum(1 for y in years if (rec.get(f"dev_year_return_{y}") or 0) > 0)
    hard = [] if n_prof >= t.min_profitable_years else [f"profitable_years {n_prof} < {t.min_profitable_years}"]
    warn = []
    ex = rec.get("dev_excl_best_year_return")
    if ex is not None and ex <= 0:
        warn.append("non_positive_without_best_year")
    if rec.get("dev_best_year_contribution") is None:
        warn.append("contribution_ratios_undefined")
    if rec.get("dev_dd_recovered") is False:
        warn.append("drawdown_unrecovered_at_window_end")
    return _resolve(hard, [], warn, {"n_profitable_years": n_prof})


# --- Stage 6 -----------------------------------------------------------------

def monthly_returns(daily: np.ndarray, days: np.ndarray) -> np.ndarray:
    """Compound daily returns (rows = series) into calendar-month returns."""
    months = days.astype("datetime64[M]")
    uniq, inv = np.unique(months, return_inverse=True)
    logs = np.log1p(np.asarray(daily, dtype=np.float64))
    out = np.zeros((logs.shape[0], len(uniq)))
    for k in range(len(uniq)):
        out[:, k] = logs[:, inv == k].sum(axis=1)
    return np.expm1(out)


def correlation_matrix(series: np.ndarray) -> np.ndarray:
    """Pearson correlation of rows; rows with zero variance get 0 off-diagonal."""
    X = np.asarray(series, dtype=np.float64)
    sd = X.std(axis=1)
    Z = np.zeros_like(X)
    ok = sd > 0
    Z[ok] = (X[ok] - X[ok].mean(axis=1, keepdims=True)) / sd[ok, None]
    C = (Z @ Z.T) / X.shape[1]
    np.fill_diagonal(C, 1.0)
    return np.clip(C, -1.0, 1.0)


def cluster_by_correlation(ids: list[str], series: np.ndarray, *, threshold: float,
                           method: str = "complete") -> dict[str, int]:
    """Agglomerative clustering on distance 1 - corr, cut at 1 - threshold.

    With complete linkage a cluster's merge height is its MAXIMUM pairwise
    distance, so every pair inside a cluster has corr >= threshold -- no
    correlation chaining (A~B, B~C but A!~C) can glue dissimilar configs."""
    if not ids:
        return {}
    if len(ids) == 1:
        return {ids[0]: 0}
    D = np.clip(1.0 - correlation_matrix(series), 0.0, 2.0)
    np.fill_diagonal(D, 0.0)
    Z = linkage(squareform(D, checks=False), method=method)
    labels = fcluster(Z, t=1.0 - threshold + 1e-12, criterion="distance")
    # Relabel deterministically by the smallest config_id in each cluster.
    first: dict[int, str] = {}
    for cid, lab in zip(ids, labels):
        first[lab] = min(first.get(lab, cid), cid)
    order = {lab: i for i, lab in enumerate(sorted(first, key=lambda k: first[k]))}
    return {cid: order[lab] for cid, lab in zip(ids, labels)}


def representative_key(rec: dict) -> tuple:
    """Deterministic development-stage ordering: higher median stage-4 stability
    Sharpe (grid neighbors, or local perturbations when that is the gate),
    more profitable dev years, higher dev Sharpe, then stable config_id."""
    def neg(x):
        return -x if x is not None else float("inf")
    stab = rec.get("stability_median_sharpe", rec.get("neighbor_median_sharpe"))
    return (neg(stab), neg(rec.get("n_profitable_years")),
            neg(rec.get("dev_sharpe")), rec["config_id"])


def select_representatives(recs: list[dict], cluster_of: dict[str, int], k: int = 1) -> list[dict]:
    """The best `k` members of each cluster (all of them if it has fewer), returned
    in development ordering."""
    by_cluster: dict[int, list[dict]] = {}
    for r in recs:
        by_cluster.setdefault(cluster_of[r["config_id"]], []).append(r)
    reps = [r for members in by_cluster.values() for r in sorted(members, key=representative_key)[:k]]
    return sorted(reps, key=representative_key)


# --- Reporting ---------------------------------------------------------------

def survivor_table(rows: list[dict], universe: int) -> list[dict]:
    """rows: [{stage, evaluated, passed, hard_reject, insufficient, deduplicated, kind}]."""
    out, prev = [], universe
    for r in rows:
        passed = r.get("passed")
        out.append({
            **r,
            "pct_of_universe": (100.0 * passed / universe) if (passed is not None and universe) else None,
            "pct_of_previous": (100.0 * passed / prev) if (passed is not None and prev) else None,
        })
        if passed is not None and r.get("kind") != DIAGNOSTIC:
            prev = passed
    return out
