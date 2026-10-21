"""Dependence-aware significance for the funnel's multiple-testing stage.

`block_bootstrap_pvalue` gives a one-sided p-value for H0: mean net return <= 0,
using a circular moving-block bootstrap so serial dependence in the monthly
return series is respected (an ordinary i.i.d. bootstrap or a plain t-test would
understate the variance of an autocorrelated series).

`benjamini_hochberg` / `benjamini_yekutieli` control the false-discovery rate
across the whole family of tested configurations. BH assumes independence or
positive-regression dependence; strategy configs overlap heavily and violate
that, so BY (valid under *arbitrary* dependence) is offered as the honest
alternative and both are reported. `m_total` lets the correction account for the
FULL search (every tested config is a hypothesis), not just the candidates whose
p-values are passed in.
"""

from __future__ import annotations

import numpy as np


def block_bootstrap_pvalue(
    returns, *, n_boot: int = 2000, block: int = 6, seed: int = 0
) -> float:
    """One-sided p-value for H0: mean(returns) <= 0 via circular block bootstrap.

    Returns 1.0 (no evidence) for a non-positive sample mean or a series too
    short to resample. Imposes H0 by centering the series, then measures how
    often a bootstrap mean reaches the observed mean."""
    x = np.asarray([v for v in returns if v is not None], dtype=float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n < 3:
        return 1.0
    obs = x.mean()
    if obs <= 0:
        return 1.0

    centered = x - obs  # impose H0: mean 0
    block = max(1, min(block, n))
    n_blocks = int(np.ceil(n / block))
    rng = np.random.default_rng(seed)

    # Circular block indices: (n_boot, n_blocks) block starts -> (n_boot, n_blocks, block).
    starts = rng.integers(0, n, size=(n_boot, n_blocks))
    offsets = np.arange(block)
    idx = (starts[:, :, None] + offsets[None, None, :]) % n  # (n_boot, n_blocks, block)
    idx = idx.reshape(n_boot, n_blocks * block)[:, :n]
    boot_means = centered[idx].mean(axis=1)

    # +1 smoothing: a bootstrap p-value is never exactly 0.
    return float((np.sum(boot_means >= obs) + 1) / (n_boot + 1))


def benjamini_hochberg(pvals, *, q: float, m_total: int | None = None):
    """BH step-up. `pvals` may be only the candidate subset; `m_total` (default
    len) is the full family size so the correction accounts for every hypothesis
    tested. Returns (mask over `pvals`, cutoff p-value or None)."""
    p = np.asarray(pvals, dtype=float)
    n = len(p)
    if n == 0:
        return np.zeros(0, dtype=bool), None
    m = m_total if m_total is not None else n
    order = np.argsort(p)
    sorted_p = p[order]
    ranks = np.arange(1, n + 1)
    thresh = ranks / m * q
    passed = sorted_p <= thresh
    if not passed.any():
        return np.zeros(n, dtype=bool), None
    kmax = int(np.max(np.where(passed)[0]))
    cutoff = float(sorted_p[kmax])
    return p <= cutoff, cutoff


def benjamini_yekutieli(pvals, *, q: float, m_total: int | None = None):
    """BY: BH with q divided by the harmonic number H(m); valid under arbitrary
    dependence (the honest choice for overlapping strategy configs)."""
    p = np.asarray(pvals, dtype=float)
    m = m_total if m_total is not None else len(p)
    if m == 0:
        return np.zeros(0, dtype=bool), None
    c_m = np.log(m) + np.euler_gamma + 1.0 / (2 * m)  # harmonic-number approximation
    return benjamini_hochberg(p, q=q / c_m, m_total=m_total)
