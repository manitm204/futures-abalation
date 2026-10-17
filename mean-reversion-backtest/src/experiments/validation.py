"""Chronological data splits and the multi-stage validation funnel.

Split boundaries are explicit configuration, not hardcoded -- see
DEFAULT_SPLIT for the spec's suggested starting design (subject to actual data
coverage; callers should verify coverage before trusting these dates for a
real run). Funnel thresholds are likewise explicit config, with each stage's
statistical purpose documented rather than left as unexplained magic numbers.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from src.engine.metrics import Metrics


@dataclass(frozen=True)
class ChronologicalSplit:
    development_start: date
    development_end: date
    validation_start: date
    validation_end: date
    holdout_start: date
    holdout_end: date

    def stage_for(self, d: date) -> str | None:
        if self.development_start <= d <= self.development_end:
            return "development"
        if self.validation_start <= d <= self.validation_end:
            return "validation"
        if self.holdout_start <= d <= self.holdout_end:
            return "holdout"
        return None


# Spec's suggested starting design, IF actual coverage supports it -- verify
# against the real downloaded date range before using this for the full study.
DEFAULT_SPLIT = ChronologicalSplit(
    development_start=date(2018, 1, 1), development_end=date(2022, 12, 31),
    validation_start=date(2023, 1, 1), validation_end=date(2024, 12, 31),
    holdout_start=date(2025, 1, 1), holdout_end=date(2026, 12, 31),
)


@dataclass(frozen=True)
class FunnelThresholds:
    # Stage 2: minimum activity
    min_total_trades: int = 30
    min_trades_per_year: float = 5.0
    min_active_quarters: int = 4

    # Stage 3: development performance
    min_dev_net_return_pct: float = 0.0  # must be positive after costs
    min_dev_profit_factor: float = 1.1
    max_dev_drawdown_pct: float = -0.30
    min_dev_sharpe: float | None = None  # optional, off by default

    # Stage 4: validation performance
    min_validation_expectancy: float = 0.0
    max_dev_to_validation_sharpe_degradation_pct: float = 0.50  # validation Sharpe
    # may not be worse than 50% of development Sharpe


@dataclass
class FunnelResult:
    config_id: str
    stage_reached: str
    passed: bool
    failure_reason: str | None = None


def stage1_data_and_config_validity(
    *, has_engine_errors: bool, has_naive_timestamps: bool, has_warmup_violations: bool, has_invalid_order_geometry: bool
) -> FunnelResult | None:
    if has_engine_errors:
        return FunnelResult(config_id="", stage_reached="stage1", passed=False, failure_reason="engine_error")
    if has_naive_timestamps:
        return FunnelResult(config_id="", stage_reached="stage1", passed=False, failure_reason="naive_timestamps")
    if has_warmup_violations:
        return FunnelResult(config_id="", stage_reached="stage1", passed=False, failure_reason="inadequate_warmup")
    if has_invalid_order_geometry:
        return FunnelResult(config_id="", stage_reached="stage1", passed=False, failure_reason="invalid_order_geometry")
    return None  # passes -- caller proceeds to stage 2


def stage2_minimum_activity(
    metrics: Metrics, *, n_years: float, n_active_quarters: int, thresholds: FunnelThresholds
) -> FunnelResult | None:
    if metrics.n_trades < thresholds.min_total_trades:
        return FunnelResult(config_id="", stage_reached="stage2", passed=False, failure_reason="insufficient_total_trades")
    trades_per_year = metrics.n_trades / n_years if n_years > 0 else 0
    if trades_per_year < thresholds.min_trades_per_year:
        return FunnelResult(config_id="", stage_reached="stage2", passed=False, failure_reason="insufficient_trades_per_year")
    if n_active_quarters < thresholds.min_active_quarters:
        return FunnelResult(config_id="", stage_reached="stage2", passed=False, failure_reason="insufficient_active_quarters")
    return None


def stage3_development_performance(metrics: Metrics, *, thresholds: FunnelThresholds) -> FunnelResult | None:
    if metrics.net_pnl <= 0 or metrics.total_return_pct < thresholds.min_dev_net_return_pct:
        return FunnelResult(config_id="", stage_reached="stage3", passed=False, failure_reason="non_positive_dev_return")
    if metrics.profit_factor is None or metrics.profit_factor < thresholds.min_dev_profit_factor:
        return FunnelResult(config_id="", stage_reached="stage3", passed=False, failure_reason="insufficient_profit_factor")
    if metrics.max_drawdown_pct < thresholds.max_dev_drawdown_pct:
        return FunnelResult(config_id="", stage_reached="stage3", passed=False, failure_reason="excessive_drawdown")
    if thresholds.min_dev_sharpe is not None:
        if metrics.sharpe_ratio is None or metrics.sharpe_ratio < thresholds.min_dev_sharpe:
            return FunnelResult(config_id="", stage_reached="stage3", passed=False, failure_reason="insufficient_sharpe")
    return None


def stage4_validation_performance(
    dev_metrics: Metrics, validation_metrics: Metrics, *, thresholds: FunnelThresholds
) -> FunnelResult | None:
    if validation_metrics.expectancy_per_trade is None or validation_metrics.expectancy_per_trade < thresholds.min_validation_expectancy:
        return FunnelResult(config_id="", stage_reached="stage4", passed=False, failure_reason="non_positive_validation_expectancy")
    if validation_metrics.n_trades < thresholds.min_total_trades // 2:
        return FunnelResult(config_id="", stage_reached="stage4", passed=False, failure_reason="insufficient_validation_trades")
    if dev_metrics.sharpe_ratio and dev_metrics.sharpe_ratio > 0:
        if validation_metrics.sharpe_ratio is None:
            return FunnelResult(config_id="", stage_reached="stage4", passed=False, failure_reason="validation_sharpe_unavailable")
        degradation = 1 - (validation_metrics.sharpe_ratio / dev_metrics.sharpe_ratio)
        if degradation > thresholds.max_dev_to_validation_sharpe_degradation_pct:
            return FunnelResult(config_id="", stage_reached="stage4", passed=False, failure_reason="excessive_dev_to_validation_degradation")
    return None


def run_funnel(
    *,
    config_id: str,
    dev_metrics: Metrics,
    validation_metrics: Metrics,
    n_years_dev: float,
    n_active_quarters_dev: int,
    thresholds: FunnelThresholds,
    has_engine_errors: bool = False,
    has_naive_timestamps: bool = False,
    has_warmup_violations: bool = False,
    has_invalid_order_geometry: bool = False,
) -> FunnelResult:
    """Runs stages 1-4 in order, stopping at the first failure. Stages 5 (holdout)
    and 6 (robustness) operate on the SET of survivors, not per-config in
    isolation -- see robustness.py / the experiment CLI for those."""
    checks = [
        stage1_data_and_config_validity(
            has_engine_errors=has_engine_errors, has_naive_timestamps=has_naive_timestamps,
            has_warmup_violations=has_warmup_violations, has_invalid_order_geometry=has_invalid_order_geometry,
        ),
        stage2_minimum_activity(dev_metrics, n_years=n_years_dev, n_active_quarters=n_active_quarters_dev, thresholds=thresholds),
        stage3_development_performance(dev_metrics, thresholds=thresholds),
        stage4_validation_performance(dev_metrics, validation_metrics, thresholds=thresholds),
    ]
    for i, result in enumerate(checks, start=1):
        if result is not None:
            return FunnelResult(config_id=config_id, stage_reached=f"stage{i}", passed=False, failure_reason=result.failure_reason)

    return FunnelResult(config_id=config_id, stage_reached="stage4", passed=True)
