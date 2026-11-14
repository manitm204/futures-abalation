from src.engine.metrics import Metrics
from src.experiments.validation import FunnelThresholds, run_funnel

DEFAULT_THRESHOLDS = FunnelThresholds()


def _metrics(**overrides) -> Metrics:
    base = dict(
        n_signals=100, n_trades=50, fill_rate=0.5, rejection_rate=0.5, n_long=25, n_short=25,
        gross_pnl=1000.0, net_pnl=800.0, total_return_pct=0.05, annualized_return_pct=0.1,
        sharpe_ratio=1.0, sortino_ratio=1.2, max_drawdown_pct=-0.1, calmar_ratio=1.0,
        win_rate=0.5, loss_rate=0.5, avg_win=50.0, avg_loss=-30.0, payoff_ratio=1.67,
        avg_realized_r=0.3, median_realized_r=0.2, profit_factor=1.5, expectancy_per_trade=16.0,
        exposure_pct=None, avg_holding_bars=10.0, commission_total=50.0, slippage_cost_total=20.0,
        max_consecutive_wins=5, max_consecutive_losses=3, intrabar_ambiguous_count=0,
    )
    base.update(overrides)
    return Metrics(**base)


def test_passing_config_reaches_stage4() -> None:
    result = run_funnel(
        config_id="c1", dev_metrics=_metrics(), validation_metrics=_metrics(sharpe_ratio=0.8),
        n_years_dev=5.0, n_active_quarters_dev=10, thresholds=DEFAULT_THRESHOLDS,
    )
    assert result.passed is True
    assert result.stage_reached == "stage4"


def test_engine_error_fails_stage1() -> None:
    result = run_funnel(
        config_id="c1", dev_metrics=_metrics(), validation_metrics=_metrics(),
        n_years_dev=5.0, n_active_quarters_dev=10, thresholds=DEFAULT_THRESHOLDS,
        has_engine_errors=True,
    )
    assert result.passed is False
    assert result.stage_reached == "stage1"
    assert result.failure_reason == "engine_error"


def test_insufficient_trades_fails_stage2() -> None:
    result = run_funnel(
        config_id="c1", dev_metrics=_metrics(n_trades=5), validation_metrics=_metrics(),
        n_years_dev=5.0, n_active_quarters_dev=10, thresholds=DEFAULT_THRESHOLDS,
    )
    assert result.stage_reached == "stage2"
    assert result.failure_reason == "insufficient_total_trades"


def test_negative_dev_return_fails_stage3() -> None:
    result = run_funnel(
        config_id="c1", dev_metrics=_metrics(net_pnl=-500.0, total_return_pct=-0.05),
        validation_metrics=_metrics(), n_years_dev=5.0, n_active_quarters_dev=10, thresholds=DEFAULT_THRESHOLDS,
    )
    assert result.stage_reached == "stage3"
    assert result.failure_reason == "non_positive_dev_return"


def test_excessive_drawdown_fails_stage3() -> None:
    result = run_funnel(
        config_id="c1", dev_metrics=_metrics(max_drawdown_pct=-0.5), validation_metrics=_metrics(),
        n_years_dev=5.0, n_active_quarters_dev=10, thresholds=DEFAULT_THRESHOLDS,
    )
    assert result.stage_reached == "stage3"
    assert result.failure_reason == "excessive_drawdown"


def test_validation_degradation_fails_stage4() -> None:
    result = run_funnel(
        config_id="c1", dev_metrics=_metrics(sharpe_ratio=2.0), validation_metrics=_metrics(sharpe_ratio=0.1),
        n_years_dev=5.0, n_active_quarters_dev=10, thresholds=DEFAULT_THRESHOLDS,
    )
    assert result.stage_reached == "stage4"
    assert result.failure_reason == "excessive_dev_to_validation_degradation"


def test_non_positive_validation_expectancy_fails_stage4() -> None:
    result = run_funnel(
        config_id="c1", dev_metrics=_metrics(), validation_metrics=_metrics(expectancy_per_trade=-5.0),
        n_years_dev=5.0, n_active_quarters_dev=10, thresholds=DEFAULT_THRESHOLDS,
    )
    assert result.stage_reached == "stage4"
    assert result.failure_reason == "non_positive_validation_expectancy"
