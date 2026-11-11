import numpy as np
import pytest

from src.analysis.stability import block_bootstrap_ci, deflated_sharpe_ratio, probabilistic_sharpe_ratio


def test_block_bootstrap_ci_contains_true_mean_for_iid_data() -> None:
    rng = np.random.default_rng(0)
    returns = rng.normal(loc=0.001, scale=0.01, size=500)
    result = block_bootstrap_ci(returns, statistic_fn=np.mean, block_size=5, n_bootstrap=500, seed=1)
    assert result.ci_low < result.point_estimate < result.ci_high
    assert result.ci_low < 0.001 < result.ci_high


def test_block_bootstrap_ci_point_estimate_matches_direct_computation() -> None:
    returns = np.array([0.01, -0.02, 0.03, 0.01, -0.01, 0.02])
    result = block_bootstrap_ci(returns, statistic_fn=np.mean, block_size=2, n_bootstrap=200, seed=2)
    assert result.point_estimate == pytest.approx(np.mean(returns))


def test_block_bootstrap_ci_short_series_degenerate() -> None:
    result = block_bootstrap_ci(np.array([0.01]), statistic_fn=np.mean, block_size=2)
    assert result.ci_low == result.ci_high == result.point_estimate


def test_psr_at_benchmark_with_normal_returns_is_near_half() -> None:
    # observed == benchmark, symmetric normal (skew=0, excess kurtosis=0) -> PSR ~ 0.5
    psr = probabilistic_sharpe_ratio(observed_sharpe=1.0, benchmark_sharpe=1.0, n_returns=252, skew=0.0, kurtosis=0.0)
    assert psr == pytest.approx(0.5, abs=1e-6)


def test_psr_increases_with_observed_sharpe_above_benchmark() -> None:
    psr_low = probabilistic_sharpe_ratio(observed_sharpe=0.5, benchmark_sharpe=0.0, n_returns=252, skew=0.0, kurtosis=0.0)
    psr_high = probabilistic_sharpe_ratio(observed_sharpe=2.0, benchmark_sharpe=0.0, n_returns=252, skew=0.0, kurtosis=0.0)
    assert psr_high > psr_low


def test_psr_increases_with_sample_size_for_positive_excess_sharpe() -> None:
    psr_small_n = probabilistic_sharpe_ratio(observed_sharpe=1.0, benchmark_sharpe=0.0, n_returns=30, skew=0.0, kurtosis=0.0)
    psr_large_n = probabilistic_sharpe_ratio(observed_sharpe=1.0, benchmark_sharpe=0.0, n_returns=2000, skew=0.0, kurtosis=0.0)
    assert psr_large_n > psr_small_n


def test_dsr_with_one_trial_equals_psr_vs_zero() -> None:
    dsr = deflated_sharpe_ratio(
        observed_sharpe=1.0, n_trials=1, variance_of_trial_sharpes=0.1, n_returns=252, skew=0.0, kurtosis=0.0
    )
    psr = probabilistic_sharpe_ratio(observed_sharpe=1.0, benchmark_sharpe=0.0, n_returns=252, skew=0.0, kurtosis=0.0)
    assert dsr == pytest.approx(psr)


def test_dsr_is_lower_than_naive_psr_when_many_trials_run() -> None:
    """The core data-mining defense: after testing many configs, the bar for
    'this Sharpe is genuinely good' rises, so DSR must be strictly lower than
    a naive PSR-against-zero for the same observed Sharpe."""
    naive_psr = probabilistic_sharpe_ratio(observed_sharpe=1.5, benchmark_sharpe=0.0, n_returns=252, skew=0.0, kurtosis=0.0)
    dsr = deflated_sharpe_ratio(
        observed_sharpe=1.5, n_trials=10_000, variance_of_trial_sharpes=0.25, n_returns=252, skew=0.0, kurtosis=0.0
    )
    assert dsr < naive_psr


def test_dsr_rejects_invalid_n_trials() -> None:
    with pytest.raises(ValueError):
        deflated_sharpe_ratio(observed_sharpe=1.0, n_trials=0, variance_of_trial_sharpes=0.1, n_returns=252, skew=0.0, kurtosis=0.0)
