"""Daily-series metrics shared by the sleeves, the combined portfolio and SPY.

Every series here is a vector of close-to-close daily returns over the window's
trading days (flat days are 0), the same convention as
src/analysis/daily_performance.py, so the sleeve, portfolio and benchmark numbers
are directly comparable.
"""

from __future__ import annotations

import math

import numpy as np

PPY = 252


def equity_curve(rets: np.ndarray, start: float = 1.0) -> np.ndarray:
    """Equity before day 0 followed by the close of every day (len(rets) + 1)."""
    return start * np.concatenate([[1.0], np.cumprod(1.0 + np.asarray(rets, dtype=float))])


def drawdown(curve: np.ndarray) -> tuple[float, int]:
    """(max drawdown <= 0, longest underwater stretch in trading days)."""
    peak = np.maximum.accumulate(curve)
    under = curve < peak - 1e-12
    longest = cur = 0
    for u in under:
        cur = cur + 1 if u else 0
        longest = max(longest, cur)
    return float((curve / peak - 1.0).min()), int(longest)


def series_metrics(rets: np.ndarray, ppy: int = PPY) -> dict:
    """Return / risk metrics of one daily return series (risk-free rate 0)."""
    r = np.asarray(rets, dtype=float)
    n = len(r)
    curve = equity_curve(r)
    total = float(curve[-1] - 1.0)
    years = n / ppy if n else 0.0
    cagr = float(curve[-1] ** (1.0 / years) - 1.0) if years > 0 and curve[-1] > 0 else None
    sd = float(r.std(ddof=1)) if n > 1 else 0.0
    vol = sd * math.sqrt(ppy) if sd > 0 else None
    sharpe = float(r.mean() / sd * math.sqrt(ppy)) if sd > 0 else None
    downside = float(np.sqrt(np.mean(np.minimum(r, 0.0) ** 2))) if n else 0.0
    sortino = float(r.mean() / downside * math.sqrt(ppy)) if downside > 0 else None
    max_dd, dd_days = drawdown(curve)
    calmar = cagr / -max_dd if cagr is not None and max_dd < 0 else None
    return {
        "n_days": n, "years": years, "total_return": total, "cagr": cagr,
        "ann_vol": vol, "sharpe": sharpe, "sortino": sortino,
        "max_drawdown": max_dd, "max_dd_duration_days": dd_days, "calmar": calmar,
        "best_day": float(r.max()) if n else None, "worst_day": float(r.min()) if n else None,
        "pct_days_positive": float((r > 0).mean()) if n else None,
        "pct_days_flat": float((r == 0).mean()) if n else None,
    }


def combine_sleeves(rets: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Buy-and-hold sleeves (no rebalancing). `rets` is (n_sleeves, n_days).
    Returns (portfolio daily returns, sleeve values per day as (n_sleeves, n_days + 1)
    in units of starting capital)."""
    w = np.asarray(weights, dtype=float)
    if not math.isclose(w.sum(), 1.0, abs_tol=1e-9):
        raise ValueError(f"Sleeve weights must sum to 1, got {w.sum()}")
    values = w[:, None] * np.vstack([equity_curve(r) for r in rets])
    total = values.sum(axis=0)
    return total[1:] / total[:-1] - 1.0, values


def interval_mask(grid: np.ndarray, starts: np.ndarray, ends: np.ndarray) -> np.ndarray:
    """True where grid time t lies in some [start, end). Intervals must be sorted and
    non-overlapping (one position at a time per sleeve)."""
    if len(starts) == 0:
        return np.zeros(len(grid), dtype=bool)
    j = np.searchsorted(starts, grid, side="right") - 1
    ok = j >= 0
    jj = np.where(ok, j, 0)
    return ok & (grid < ends[jj])


def relative_to_benchmark(rets: np.ndarray, bench: np.ndarray, ppy: int = PPY) -> dict:
    """Correlation, beta and annualized alpha (simple, rf = 0) versus a benchmark."""
    r, b = np.asarray(rets, float), np.asarray(bench, float)
    vb = float(b.var(ddof=1))
    beta = float(np.cov(r, b, ddof=1)[0, 1] / vb) if vb > 0 else None
    corr = float(np.corrcoef(r, b)[0, 1]) if r.std() > 0 and b.std() > 0 else None
    alpha = float((r.mean() - beta * b.mean()) * ppy) if beta is not None else None
    up, down = b > 0, b < 0
    up_cap = float(r[up].mean() / b[up].mean()) if up.any() else None
    down_cap = float(r[down].mean() / b[down].mean()) if down.any() else None
    return {"correlation": corr, "beta": beta, "alpha_annual": alpha,
            "up_capture": up_cap, "down_capture": down_cap}


def monthly_returns(days: np.ndarray, rets: np.ndarray) -> dict[str, float]:
    """{'YYYY-MM': compounded return} for a daily series."""
    months = np.array([str(d)[:7] for d in days])
    out = {}
    for m in dict.fromkeys(months):
        out[m] = float(np.prod(1.0 + rets[months == m]) - 1.0)
    return out
