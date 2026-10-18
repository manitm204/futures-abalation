"""Ranking and rank-correlation utilities over per-config result records.

Each "result" is expected to be a dict as produced by
src/experiments/runner.py (config_id, metrics, ...). These functions operate
on that dict shape directly rather than requiring a bespoke object, since
results are loaded straight from the JSON files on disk for analysis.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


def _metric(result: dict, metric: str) -> float | None:
    return result.get("metrics", {}).get(metric)


def top_n(results: list[dict], *, metric: str, n: int, higher_is_better: bool = True) -> list[dict]:
    """Selects the top `n` results by `metric`, dropping results where the
    metric is None (missing/unresolvable) rather than treating None as worst
    or best -- an explicit exclusion, not a silent ordering assumption."""
    valid = [r for r in results if _metric(r, metric) is not None]
    valid.sort(key=lambda r: _metric(r, metric), reverse=higher_is_better)
    return valid[:n]


def percentile_rank(results: list[dict], *, metric: str, config_id: str) -> float | None:
    """Percentile (0-100) of `config_id`'s metric value within the full
    population -- used to judge "is this config actually unusual," not just
    "is it in the top N," since top-N membership alone is sensitive to
    sampling density near the cutoff."""
    values = [_metric(r, metric) for r in results if _metric(r, metric) is not None]
    target = next((r for r in results if r["config_id"] == config_id), None)
    if target is None or _metric(target, metric) is None or not values:
        return None
    target_val = _metric(target, metric)
    return float(stats.percentileofscore(values, target_val, kind="mean"))


@dataclass(frozen=True)
class RankCorrelation:
    spearman_rho: float
    p_value: float
    n: int


def rank_correlation(results: list[dict], *, metric_a: str, metric_b: str) -> RankCorrelation | None:
    """Spearman rank correlation between two metrics across the same set of
    configs (e.g. development-stage Sharpe vs validation-stage Sharpe) --
    used to check whether in-sample ranking predicts out-of-sample ranking at
    all, which naive top-N selection on development data alone cannot answer.
    """
    pairs = [
        (_metric(r, metric_a), _metric(r, metric_b))
        for r in results
        if _metric(r, metric_a) is not None and _metric(r, metric_b) is not None
    ]
    if len(pairs) < 3:
        return None
    a_vals, b_vals = zip(*pairs)
    rho, p = stats.spearmanr(a_vals, b_vals)
    return RankCorrelation(spearman_rho=float(rho), p_value=float(p), n=len(pairs))
