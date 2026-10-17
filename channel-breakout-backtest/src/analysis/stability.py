"""Multiple-testing and dependent-returns-aware statistical tools.

Trades are NOT i.i.d. (positions cluster in time, share market regimes, etc.),
so naive t-tests / naive Sharpe confidence intervals are not valid. Block
bootstrap resamples contiguous blocks of the return series to preserve serial
dependence structure. PSR/DSR follow Bailey & Lopez de Prado's formulas and
correct for (a) non-normal return skew/kurtosis and (b) selection bias from
testing many configurations (DSR only).
"""

from __future__ import annotations

import math
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


def expected_max_sharpe(*, n_trials: int, variance_of_trial_sharpes: float) -> float:
    """Expected MAXIMUM (per-period) Sharpe ratio across `n_trials` independent
    trials whose Sharpe estimates have variance `variance_of_trial_sharpes`,
    under the null of zero true edge. Expected-maximum-of-n-Gaussians
    approximation from Bailey & Lopez de Prado (2014). Returns 0.0 for a single
    trial (no selection to correct for)."""
    if n_trials < 1:
        raise ValueError("n_trials must be >= 1")
    if n_trials == 1:
        return 0.0
    euler_gamma = 0.5772156649
    z_term = (1 - euler_gamma) * stats.norm.ppf(1 - 1 / n_trials) + euler_gamma * stats.norm.ppf(1 - 1 / (n_trials * np.e))
    return float(np.sqrt(max(0.0, variance_of_trial_sharpes)) * z_term)


def sharpe_moments(returns) -> tuple[float, int, float, float] | None:
    """(per-period Sharpe, n, skew, EXCESS kurtosis) from a return series, or
    None if too short / degenerate. Sharpe is mean/std with ddof=1; moments feed
    the PSR/DSR non-normality correction and are in the same per-period units."""
    x = np.asarray([v for v in (returns if returns is not None else []) if v is not None], dtype=float)
    x = x[np.isfinite(x)]
    if len(x) < 3:
        return None
    sd = float(x.std(ddof=1))
    if sd == 0:
        return None
    return float(x.mean() / sd), len(x), float(stats.skew(x)), float(stats.kurtosis(x))


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
    sr_star = expected_max_sharpe(n_trials=n_trials, variance_of_trial_sharpes=variance_of_trial_sharpes)
    return probabilistic_sharpe_ratio(
        observed_sharpe, benchmark_sharpe=sr_star, n_returns=n_returns, skew=skew, kurtosis=kurtosis
    )


# --- Search-adjusted confidence (funnel stage 9) -----------------------------


def lag1_autocorr(returns) -> float | None:
    x = np.asarray(returns, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) < 4 or x[:-1].std() == 0 or x[1:].std() == 0:
        return None
    return float(np.corrcoef(x[:-1], x[1:])[0, 1])


def effective_n_observations(n: int, rho1: float | None) -> float:
    """AR(1) effective sample size n * (1 - rho) / (1 + rho) for positive lag-1
    autocorrelation; negative/undefined rho leaves n unchanged (conservative:
    never inflates the sample)."""
    if rho1 is None or rho1 <= 0:
        return float(n)
    return float(n) * (1 - rho1) / (1 + rho1)


def correlation_eigenvalues(returns_matrix: np.ndarray) -> tuple[np.ndarray, int]:
    """Eigenvalues of the N x N correlation matrix of N return series (rows) over
    T periods, computed via the T x T dual Gram matrix (same non-zero spectrum).
    Rows with zero variance are dropped. Returns (eigenvalues desc, N used)."""
    X = np.asarray(returns_matrix, dtype=np.float64)
    sd = X.std(axis=1, ddof=1)
    X = X[sd > 0]
    n, t = X.shape
    if n < 2:
        return np.array([float(n)]), n
    Z = (X - X.mean(axis=1, keepdims=True)) / X.std(axis=1, ddof=1, keepdims=True)
    G = (Z.T @ Z) / (t - 1)  # T x T, trace == n
    ev = np.linalg.eigvalsh(G)[::-1]
    return np.clip(ev, 0.0, None), n


def effective_number_of_trials(eigenvalues: np.ndarray, n_series: int) -> dict:
    """Effective number of independent trials from the correlation spectrum.

    li_ji: Li & Ji (2005) sum_i [I(l_i >= 1) + (l_i - floor(l_i))]
    participation_ratio: (sum l)^2 / sum l^2 (tends to be small/conservative)
    n_components_95: eigenvectors needed for 95% of the variance.
    All are bounded by the number of periods T (matrix rank)."""
    ev = np.asarray(eigenvalues, dtype=float)
    li_ji = float(np.sum((ev >= 1).astype(float) + (ev - np.floor(ev))))
    pr = float(ev.sum() ** 2 / np.sum(ev**2)) if np.sum(ev**2) > 0 else 1.0
    frac = np.cumsum(ev) / ev.sum() if ev.sum() > 0 else np.array([1.0])
    n95 = int(np.searchsorted(frac, 0.95) + 1)
    return {"li_ji": max(1.0, li_ji), "participation_ratio": max(1.0, pr),
            "n_components_95": n95, "n_series": int(n_series), "rank_bound_T": int(len(ev))}


def dsr_audit(
    returns,
    *,
    n_trials: float,
    variance_of_trial_sharpes: float,
    periods_per_year: int,
    serial_adjust: bool = True,
) -> dict:
    """DSR with every input and assumption logged. Sharpe, benchmark SR* and the
    trial-Sharpe variance are all in the SAME per-period (daily) units; skew is
    the sample skew and kurtosis is EXCESS (converted to the paper's raw-kurtosis
    term inside `probabilistic_sharpe_ratio`). Serial dependence is handled by
    replacing n with the AR(1) effective sample size."""
    mom = sharpe_moments(returns)
    if mom is None:
        return {"dsr": None, "status_reason": "undefined_return_moments"}
    sr, n, sk, ku = mom
    rho = lag1_autocorr(returns) if serial_adjust else None
    n_eff = effective_n_observations(n, rho) if serial_adjust else float(n)
    n_trials_int = max(1, int(round(n_trials)))
    sr_star = expected_max_sharpe(n_trials=n_trials_int, variance_of_trial_sharpes=variance_of_trial_sharpes)
    n_used = max(2, int(math.floor(n_eff)))
    dsr = probabilistic_sharpe_ratio(sr, benchmark_sharpe=sr_star, n_returns=n_used, skew=sk, kurtosis=ku)
    psr0 = probabilistic_sharpe_ratio(sr, benchmark_sharpe=0.0, n_returns=n_used, skew=sk, kurtosis=ku)
    ann = math.sqrt(periods_per_year)
    return {
        "dsr": dsr, "psr_vs_zero": psr0,
        "sharpe_per_period": sr, "sharpe_annualized": sr * ann,
        "benchmark_sharpe_per_period": sr_star, "benchmark_sharpe_annualized": sr_star * ann,
        "n_trials": n_trials_int, "variance_of_trial_sharpes_per_period": variance_of_trial_sharpes,
        "n_observations": n, "n_effective_observations": n_eff, "n_used": n_used,
        "lag1_autocorr": rho, "skew": sk, "excess_kurtosis": ku,
        "kurtosis_convention": "excess (normal=0); PSR uses (excess+2)/4 == (raw-1)/4",
        "return_frequency": "daily", "periods_per_year": periods_per_year,
    }
