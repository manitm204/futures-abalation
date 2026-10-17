"""Helpers for the funnel's diagnostics: reproducible parameter perturbations,
break-even execution cost, and trade-interval overlap between configs."""

from __future__ import annotations

import math
from datetime import datetime

import numpy as np

from src.experiments.funnel_config import PerturbationCfg
from src.strategies.channel_breakout.backtest import ChannelParams
from src.utils.seeds import derive_seed


def perturbations(p: ChannelParams, *, config_id: str, base_seed: int, pcfg: PerturbationCfg) -> list[ChannelParams]:
    """`pcfg.n_per_config` jointly perturbed copies of `p`. Integer lookbacks move
    by a non-zero integer of up to `integer_rel_step` (at least 1 bar); numeric
    buffer/stop move by uniform amounts. Categorical / structural parameters
    (timeframe, trend_filter, confirm, symbol) are never numerically perturbed;
    an `off` ATR stop stays off. Seeded per config so results are reproducible
    and independent of which other configs are in the run."""
    rng = np.random.default_rng(derive_seed(base_seed, "perturb", config_id))

    def step_int(v: int, lo: int) -> int:
        k = max(1, round(pcfg.integer_rel_step * v))
        d = 0
        while d == 0:
            d = int(rng.integers(-k, k + 1))
        return max(lo, v + d)

    out = []
    for _ in range(pcfg.n_per_config):
        stop = p.init_stop_atr
        if stop is not None:
            stop = max(pcfg.min_init_stop_atr, stop + float(rng.uniform(-pcfg.init_stop_atr_abs, pcfg.init_stop_atr_abs)))
        out.append(ChannelParams(
            symbol=p.symbol, timeframe=p.timeframe,
            entry_lookback=step_int(p.entry_lookback, 2),
            exit_lookback=step_int(p.exit_lookback, 1),
            buffer_atr=max(0.0, p.buffer_atr + float(rng.uniform(-pcfg.buffer_atr_abs, pcfg.buffer_atr_abs))),
            init_stop_atr=stop, confirm=p.confirm, trend_filter=p.trend_filter,
        ))
    return out


def breakeven_multiplier(mults: list[float], net_returns: list[float | None]) -> tuple[float | None, str]:
    """Cost multiplier at which development net return crosses zero, by linear
    interpolation between the bracketing grid points. Returns (value, status)."""
    pts = [(m, r) for m, r in sorted(zip(mults, net_returns)) if r is not None]
    if not pts:
        return None, "undefined"
    if pts[0][1] <= 0:
        return None, f"not_profitable_at_{pts[0][0]}x"
    for (m0, r0), (m1, r1) in zip(pts, pts[1:]):
        if r1 <= 0 < r0:
            return m0 + (m1 - m0) * r0 / (r0 - r1), "interpolated"
    return None, f"profitable_beyond_{pts[-1][0]}x"


def interval_overlap(a: list[tuple[datetime, datetime]], b: list[tuple[datetime, datetime]]) -> float | None:
    """Jaccard overlap of time-in-market: |A ∩ B| / |A ∪ B| over holding intervals.
    Each list must be sorted and non-overlapping (single-position engine)."""
    def total(xs):
        return sum((y - x).total_seconds() for x, y in xs)
    ta, tb = total(a), total(b)
    if ta + tb <= 0:
        return None
    i = j = 0
    inter = 0.0
    while i < len(a) and j < len(b):
        lo = max(a[i][0], b[j][0])
        hi = min(a[i][1], b[j][1])
        if hi > lo:
            inter += (hi - lo).total_seconds()
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    union = ta + tb - inter
    return inter / union if union > 0 else None


def quantile(xs: list[float], q: float) -> float | None:
    v = [x for x in xs if x is not None and math.isfinite(x)]
    return float(np.quantile(v, q)) if v else None
