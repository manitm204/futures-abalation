"""Post-hoc robustness checks over a set of (typically funnel-surviving)
configs' trade results. These are diagnostic/comparative, not re-optimization:
none of these functions select or tune anything, they only summarize.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Callable

from src.engine.events import Trade
from src.engine.metrics import Metrics, compute_metrics


@dataclass
class TransferResult:
    trained_symbol: str
    applied_symbol: str
    trained_metrics: Metrics
    applied_metrics: Metrics
    return_degradation_pct: float | None
    sharpe_degradation_pct: float | None


def symbol_transfer(
    trained_symbol: str, applied_symbol: str, trained_metrics: Metrics, applied_metrics: Metrics
) -> TransferResult:
    ret_degradation = None
    if trained_metrics.total_return_pct not in (None, 0):
        ret_degradation = 1 - (applied_metrics.total_return_pct / trained_metrics.total_return_pct)
    sharpe_degradation = None
    if trained_metrics.sharpe_ratio not in (None, 0):
        sharpe_degradation = 1 - ((applied_metrics.sharpe_ratio or 0) / trained_metrics.sharpe_ratio)
    return TransferResult(
        trained_symbol=trained_symbol, applied_symbol=applied_symbol,
        trained_metrics=trained_metrics, applied_metrics=applied_metrics,
        return_degradation_pct=ret_degradation, sharpe_degradation_pct=sharpe_degradation,
    )


def window_comparison(trades: list[Trade], *, starting_equity: float) -> dict[str, Metrics]:
    by_window: dict[str, list[Trade]] = defaultdict(list)
    for t in trades:
        by_window[t.window or "unknown"].append(t)
    return {w: compute_metrics(ts, [], starting_equity=starting_equity) for w, ts in by_window.items()}


def year_by_year(trades: list[Trade], *, starting_equity: float) -> dict[int, Metrics]:
    by_year: dict[int, list[Trade]] = defaultdict(list)
    for t in trades:
        if t.exit_fill is not None:
            by_year[t.exit_fill.fill_ts.year].append(t)
    return {y: compute_metrics(ts, [], starting_equity=starting_equity) for y, ts in by_year.items()}


def cost_sensitivity(
    rerun_fn: Callable[[float, float], list[Trade]], *, starting_equity: float, multipliers: tuple[float, ...] = (0.5, 1.0, 1.5, 2.0)
) -> dict[float, Metrics]:
    """`rerun_fn(commission_multiplier, slippage_multiplier)` must re-run the
    backtest under scaled cost assumptions and return the resulting trades --
    this module doesn't own the engine invocation, only the comparison."""
    return {m: compute_metrics(rerun_fn(m, m), [], starting_equity=starting_equity) for m in multipliers}


def intrabar_ambiguity_sensitivity(
    rerun_fn: Callable[[str], list[Trade]], *, starting_equity: float
) -> dict[str, Metrics]:
    modes = ("stop_first", "target_first", "discard_ambiguous")
    return {mode: compute_metrics(rerun_fn(mode), [], starting_equity=starting_equity) for mode in modes}


@dataclass
class NeighborhoodStabilityResult:
    center_config_id: str
    center_metric_value: float
    neighbor_metric_values: list[float]
    std_dev: float
    is_stable: bool


def parameter_neighborhood_stability(
    center_config_id: str,
    center_metric_value: float,
    neighbor_metric_values: list[float],
    *,
    max_relative_std: float = 0.5,
) -> NeighborhoodStabilityResult:
    """A config whose small parameter perturbations swing performance wildly is
    a data-mining red flag even if the center point looks great. `neighbor_metric_values`
    must come from configs that differ from the center by ONE parameter changed
    by one grid/sample step -- selecting genuine neighbors is the caller's job
    (this function only judges the spread once given the values)."""
    import statistics

    if len(neighbor_metric_values) < 2:
        return NeighborhoodStabilityResult(center_config_id, center_metric_value, neighbor_metric_values, 0.0, True)

    std = statistics.stdev(neighbor_metric_values)
    denom = abs(center_metric_value) if center_metric_value != 0 else 1.0
    relative_std = std / denom
    return NeighborhoodStabilityResult(
        center_config_id=center_config_id, center_metric_value=center_metric_value,
        neighbor_metric_values=neighbor_metric_values, std_dev=std, is_stable=relative_std <= max_relative_std,
    )
