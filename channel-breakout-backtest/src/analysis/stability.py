"""Multiple-testing and dependent-returns-aware statistical tools.

Trades are NOT i.i.d. (positions cluster in time, share market regimes, etc.),
so naive t-tests / naive Sharpe confidence intervals are not valid. Block
bootstrap resamples contiguous blocks of the return series to preserve serial
dependence structure. PSR/DSR follow Bailey & Lopez de Prado's formulas and
correct for (a) non-normal return skew/kurtosis and (b) selection bias from
testing many configurations (DSR only).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass(frozen=True)
class BootstrapCI:
    point_estimate: float
    ci_low: float
    ci_high: float
    confidence_level: float
    n_bootstrap: int


def block_bootstrap_ci(
    returns: np.ndarray,
    *,
    statistic_fn,
    block_size: int,
    n_bootstrap: int = 1000,
    confidence_level: float = 0.95,
    seed: int = 42,
) -> BootstrapCI:
    """Moving-block bootstrap: resamples overlapping contiguous blocks of size
    `block_size` (with replacement) to build up resampled series of the same
    length as `returns`, applies `statistic_fn` to each, and reports a
    percentile confidence interval. `block_size` should reflect the return
    series' actual autocorrelation length (e.g. a few trades' worth for daily
    trade-level dependence) -- block_size=1 degenerates to i.i.d. bootstrap,
    which is what this function exists to avoid using by default.
    """
    returns = np.asarray(returns, dtype=float)
    n = len(returns)
    point_estimate = float(statistic_fn(returns))
    if n < 2:
        return BootstrapCI(point_estimate, point_estimate, point_estimate, confidence_level, n_bootstrap)

    rng = np.random.default_rng(seed)
    n_blocks_needed = -(-n // block_size)  # ceil
    starts_max = max(1, n - block_size + 1)

    stats_out = np.empty(n_bootstrap)
    for b in range(n_bootstrap):
        block_starts = rng.integers(0, starts_max, size=n_blocks_needed)
        resampled = np.concatenate([returns[s : s + block_size] for s in block_starts])[:n]
        stats_out[b] = statistic_fn(resampled)

    alpha = 1 - confidence_level
    lo, hi = np.percentile(stats_out, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return BootstrapCI(point_estimate, float(lo), float(hi), confidence_level, n_bootstrap)


def probabilistic_sharpe_ratio(
    observed_sharpe: float, *, benchmark_sharpe: float, n_returns: int, skew: float, kurtosis: float
) -> float:
    """PSR(SR*) = P(true Sharpe > benchmark_sharpe | observed_sharpe, sample size,
    skew, kurtosis). Bailey & Lopez de Prado (2012). `kurtosis` is EXCESS
    kurtosis (normal = 0), matching scipy.stats.kurtosis's default.
    """
    if n_returns < 2:
        raise ValueError("n_returns must be >= 2")
    numerator = (observed_sharpe - benchmark_sharpe) * np.sqrt(n_returns - 1)
    # Published formula uses RAW (non-excess) kurtosis in a (kurt-1)/4 term;
    # this function takes excess kurtosis (normal = 0, matching
    # scipy.stats.kurtosis's default), and excess = raw - 3, so
    # (raw-1)/4 = (excess+2)/4.
    denominator = np.sqrt(max(1e-12, 1 - skew * observed_sharpe + ((kurtosis + 2) / 4) * observed_sharpe**2))
    z = numerator / denominator
    return float(stats.norm.cdf(z))


def deflated_sharpe_ratio(
    observed_sharpe: float,
    *,
    n_trials: int,
    variance_of_trial_sharpes: float,
    n_returns: int,
    skew: float,
    kurtosis: float,
) -> float:
    """DSR: PSR evaluated against the EXPECTED MAXIMUM Sharpe ratio one would
    observe by chance after running `n_trials` independent backtests (i.e. the
    ~10,000-config search), instead of against 0. This is the headline defense
    against "found a great Sharpe by testing thousands of configs" data mining.
    Uses the expected-maximum-of-n-Gaussians approximation from Bailey & Lopez
    de Prado (2014).
    """
    if n_trials < 1:
        raise ValueError("n_trials must be >= 1")
    euler_gamma = 0.5772156649
    if n_trials == 1:
        expected_max_sharpe = 0.0
    else:
        z_term = (1 - euler_gamma) * stats.norm.ppf(1 - 1 / n_trials) + euler_gamma * stats.norm.ppf(1 - 1 / (n_trials * np.e))
        expected_max_sharpe = np.sqrt(variance_of_trial_sharpes) * z_term
    return probabilistic_sharpe_ratio(
        observed_sharpe, benchmark_sharpe=expected_max_sharpe, n_returns=n_returns, skew=skew, kurtosis=kurtosis
    )
