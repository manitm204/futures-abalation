from src.engine.metrics import Metrics
from src.experiments.robustness import parameter_neighborhood_stability, symbol_transfer


def _metrics(**overrides) -> Metrics:
    base = dict(
        n_signals=None, n_trades=10, fill_rate=None, rejection_rate=None, n_long=5, n_short=5,
        gross_pnl=100.0, net_pnl=80.0, total_return_pct=0.05, annualized_return_pct=0.1,
        sharpe_ratio=1.0, sortino_ratio=1.0, max_drawdown_pct=-0.05, calmar_ratio=1.0,
        win_rate=0.5, loss_rate=0.5, avg_win=20.0, avg_loss=-10.0, payoff_ratio=2.0,
        avg_realized_r=0.5, median_realized_r=0.4, profit_factor=2.0, expectancy_per_trade=8.0,
        exposure_pct=None, avg_holding_bars=5.0, commission_total=5.0, slippage_cost_total=2.0,
        max_consecutive_wins=3, max_consecutive_losses=2, intrabar_ambiguous_count=0,
    )
    base.update(overrides)
    return Metrics(**base)


def test_symbol_transfer_no_degradation_when_identical() -> None:
    m = _metrics()
    result = symbol_transfer("SPY", "QQQ", m, m)
    assert result.return_degradation_pct == 0.0
    assert result.sharpe_degradation_pct == 0.0


def test_symbol_transfer_detects_return_degradation() -> None:
    trained = _metrics(total_return_pct=0.10, sharpe_ratio=2.0)
    applied = _metrics(total_return_pct=0.05, sharpe_ratio=1.0)
    result = symbol_transfer("SPY", "QQQ", trained, applied)
    assert result.return_degradation_pct == 0.5  # 50% degradation
    assert result.sharpe_degradation_pct == 0.5


def test_symbol_transfer_negative_degradation_when_applied_outperforms() -> None:
    trained = _metrics(total_return_pct=0.05)
    applied = _metrics(total_return_pct=0.10)
    result = symbol_transfer("SPY", "QQQ", trained, applied)
    assert result.return_degradation_pct < 0  # improvement, not degradation


def test_neighborhood_stability_flags_high_variance_as_unstable() -> None:
    result = parameter_neighborhood_stability(
        center_config_id="c1", center_metric_value=2.0,
        neighbor_metric_values=[0.1, -1.0, 3.5, -2.0, 4.0],  # wild swings
        max_relative_std=0.5,
    )
    assert result.is_stable is False


def test_neighborhood_stability_flags_low_variance_as_stable() -> None:
    result = parameter_neighborhood_stability(
        center_config_id="c1", center_metric_value=2.0,
        neighbor_metric_values=[1.9, 2.1, 2.0, 1.95, 2.05],
        max_relative_std=0.5,
    )
    assert result.is_stable is True


def test_neighborhood_stability_insufficient_neighbors_defaults_stable() -> None:
    result = parameter_neighborhood_stability(center_config_id="c1", center_metric_value=1.0, neighbor_metric_values=[1.1])
    assert result.is_stable is True
