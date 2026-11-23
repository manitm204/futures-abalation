"""Parameter enrichment and distribution analysis for top-performing configs.

Per spec: enrichment must be normalized by baseline sampling frequency, not
raw top-N counts -- a value that's common in the full sampled population will
naturally also be common in the top N by chance, which is not evidence of
that value being associated with better performance.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def _get_param(result: dict, param: str):
    return result.get("config", {}).get(param)


@dataclass(frozen=True)
class EnrichmentRow:
    value: object
    baseline_frequency: float
    top_n_frequency: float
    enrichment_ratio: float | None  # top_n_frequency / baseline_frequency
    baseline_count: int
    top_n_count: int


def categorical_enrichment(
    all_results: list[dict], top_results: list[dict], *, param: str
) -> list[EnrichmentRow]:
    """Enrichment table for a categorical parameter: for each observed value,
    how much more (or less) common is it in `top_results` versus its baseline
    rate across `all_results`. Ratio > 1 means enriched, < 1 means depleted.
    """
    baseline_values = [_get_param(r, param) for r in all_results]
    top_values = [_get_param(r, param) for r in top_results]

    n_baseline = len(baseline_values)
    n_top = len(top_values)
    if n_baseline == 0:
        return []

    distinct = sorted({v for v in baseline_values if v is not None}, key=str)
    rows: list[EnrichmentRow] = []
    for v in distinct:
        baseline_count = sum(1 for x in baseline_values if x == v)
        top_count = sum(1 for x in top_values if x == v)
        baseline_freq = baseline_count / n_baseline
        top_freq = (top_count / n_top) if n_top > 0 else 0.0
        ratio = (top_freq / baseline_freq) if baseline_freq > 0 else None
        rows.append(
            EnrichmentRow(
                value=v, baseline_frequency=baseline_freq, top_n_frequency=top_freq,
                enrichment_ratio=ratio, baseline_count=baseline_count, top_n_count=top_count,
            )
        )
    return sorted(rows, key=lambda r: (r.enrichment_ratio or 0), reverse=True)


@dataclass(frozen=True)
class NumericDistributionComparison:
    param: str
    baseline_median: float
    baseline_p25: float
    baseline_p75: float
    top_n_median: float
    top_n_p25: float
    top_n_p75: float
    n_baseline: int
    n_top_n: int


def numeric_distribution_comparison(
    all_results: list[dict], top_results: list[dict], *, param: str
) -> NumericDistributionComparison | None:
    baseline = np.array([_get_param(r, param) for r in all_results if _get_param(r, param) is not None], dtype=float)
    top = np.array([_get_param(r, param) for r in top_results if _get_param(r, param) is not None], dtype=float)
    if len(baseline) == 0 or len(top) == 0:
        return None
    return NumericDistributionComparison(
        param=param,
        baseline_median=float(np.median(baseline)), baseline_p25=float(np.percentile(baseline, 25)),
        baseline_p75=float(np.percentile(baseline, 75)),
        top_n_median=float(np.median(top)), top_n_p25=float(np.percentile(top, 25)),
        top_n_p75=float(np.percentile(top, 75)),
        n_baseline=len(baseline), n_top_n=len(top),
    )
