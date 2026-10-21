"""Helpers for the funnel's diagnostics: reproducible parameter perturbations,
break-even execution cost, and trade-interval overlap between configs."""

from __future__ import annotations

import math
from datetime import datetime

import numpy as np

from src.experiments.funnel_config import PerturbationCfg
from src.strategies.ma_crossover.backtest import MAParams
from src.strategies.mean_reversion.backtest import MRParams
from src.strategies.rsi_divergence.backtest import RSIParams
from src.utils.seeds import derive_seed


def perturbations(p: MRParams, *, config_id: str, base_seed: int, pcfg: PerturbationCfg) -> list[MRParams]:
    """`pcfg.n_per_config` jointly perturbed copies of `p`. Integer lookbacks and
    the holding cap move by a non-zero integer of up to `integer_rel_step` (at
    least 1 bar); entry/exit z thresholds move by uniform +/- `z_abs`.
    Categorical parameters (mean_type, trend_filter, symbol) are never
    perturbed. Seeded per config so results are reproducible and independent
    of which other configs are in the run."""
    rng = np.random.default_rng(derive_seed(base_seed, "perturb", config_id))

    def step_int(v: int, lo: int) -> int:
        k = max(1, round(pcfg.integer_rel_step * v))
        d = 0
        while d == 0:
            d = int(rng.integers(-k, k + 1))
        return max(lo, v + d)

    def step_z(v: float) -> float:
        return v + float(rng.uniform(-pcfg.z_abs, pcfg.z_abs))

    return [MRParams(
        symbol=p.symbol, timeframe=p.timeframe, mean_type=p.mean_type,
        mean_lookback=step_int(p.mean_lookback, 2), std_lookback=step_int(p.std_lookback, 2),
        entry_z=step_z(p.entry_z), exit_z=step_z(p.exit_z), max_hold=step_int(p.max_hold, 1),
        trend_filter=p.trend_filter,
    ) for _ in range(pcfg.n_per_config)]


def perturbations_v2(p: MRParams, *, config_id: str, base_seed: int, pcfg: PerturbationCfg) -> list[MRParams]:
    """v2 counterpart of `perturbations`: mean lookback (the std window follows it),
    holding cap and cooldown move by a non-zero integer of up to
    `integer_rel_step` (at least 1 bar; cooldown never below 0); z thresholds by
    +/- `z_abs`; an ATR stop by up to +/- `integer_rel_step` RELATIVE (never below
    0.5 ATR); "no stop" stays no stop. Categoricals (mean_type, trend_filter,
    entry_confirmation, timeframe, symbol) are never perturbed."""
    rng = np.random.default_rng(derive_seed(base_seed, "perturb", config_id))

    def step_int(v: int, lo: int) -> int:
        k = max(1, round(pcfg.integer_rel_step * v))
        d = 0
        while d == 0:
            d = int(rng.integers(-k, k + 1))
        return max(lo, v + d)

    out = []
    for _ in range(pcfg.n_per_config):
        lb = step_int(p.mean_lookback, 2)
        stop = p.stop_atr
        if stop is not None:
            stop = max(0.5, stop * (1 + float(rng.uniform(-pcfg.integer_rel_step, pcfg.integer_rel_step))))
        out.append(MRParams(
            symbol=p.symbol, timeframe=p.timeframe, mean_type=p.mean_type, mean_lookback=lb, std_lookback=lb,
            entry_z=p.entry_z + float(rng.uniform(-pcfg.z_abs, pcfg.z_abs)),
            exit_z=p.exit_z + float(rng.uniform(-pcfg.z_abs, pcfg.z_abs)),
            max_hold=step_int(p.max_hold, 1), trend_filter=p.trend_filter,
            entry_confirmation=p.entry_confirmation, cooldown_bars=step_int(p.cooldown_bars, 0),
            stop_atr=stop,
        ))
    return out


def perturbations_rsi(p: RSIParams, *, config_id: str, base_seed: int, pcfg: PerturbationCfg) -> list[RSIParams]:
    """RSI-divergence counterpart of `perturbations`: RSI period, pivot widths, max
    pivot gap and holding cap move by a non-zero integer of up to
    `integer_rel_step` (at least 1 bar; RSI period >= 2, pivot widths >= 1); the
    minimum RSI difference by uniform +/- `rsi_diff_abs` points (never below 0);
    stop ATR multiple and target R by up to +/- `float_rel_step` RELATIVE (stop
    >= 0.25 ATR, target >= 0.25 R). Timeframe and symbol are never perturbed.
    v2 filters that are on: the RSI-extreme and ADX thresholds and the minimum
    price divergence (ATR multiples) move by up to +/- `float_rel_step` relative.
    A filter that is off stays off and draws nothing, so v1 perturbations are unchanged.
    v3: a trend EMA that is on moves by a non-zero integer of up to `integer_rel_step`
    (>= 2 bars); entry confirmation and session window are categorical and kept."""
    rng = np.random.default_rng(derive_seed(base_seed, "perturb", config_id))

    def step_int(v: int, lo: int) -> int:
        k = max(1, round(pcfg.integer_rel_step * v))
        d = 0
        while d == 0:
            d = int(rng.integers(-k, k + 1))
        return max(lo, v + d)

    def step_rel(v: float, lo: float) -> float:
        return max(lo, v * (1 + float(rng.uniform(-pcfg.float_rel_step, pcfg.float_rel_step))))

    return [RSIParams(
        symbol=p.symbol, timeframe=p.timeframe, rsi_lookback=step_int(p.rsi_lookback, 2),
        pivot_left=step_int(p.pivot_left, 1), pivot_right=step_int(p.pivot_right, 1),
        max_pivot_gap=step_int(p.max_pivot_gap, 2),
        min_rsi_diff=max(0.0, p.min_rsi_diff + float(rng.uniform(-pcfg.rsi_diff_abs, pcfg.rsi_diff_abs))),
        stop_atr=step_rel(p.stop_atr, 0.25), target_r=step_rel(p.target_r, 0.25),
        max_hold=step_int(p.max_hold, 1),
        rsi_extreme_lower=None if p.rsi_extreme_lower is None else step_rel(p.rsi_extreme_lower, 1.0),
        adx_max=None if p.adx_max is None else step_rel(p.adx_max, 1.0),
        min_price_div_atr=step_rel(p.min_price_div_atr, 0.0) if p.min_price_div_atr else 0.0,
        trend_ema=None if p.trend_ema is None else step_int(p.trend_ema, 2),
        entry_breakout=p.entry_breakout, session_window=p.session_window,
    ) for _ in range(pcfg.n_per_config)]


def perturbations_ma(p: MAParams, *, config_id: str, base_seed: int, pcfg: PerturbationCfg) -> list[MAParams]:
    """MA-crossover counterpart of `perturbations`: fast and slow MA lengths move by
    a non-zero integer of up to `integer_rel_step` (at least 1 bar; fast >= 2 and
    always shorter than slow), confirmation bars likewise (never below 1); the ATR
    buffer and an initial stop that is on move by up to +/- `float_rel_step`
    RELATIVE (stop >= 0.25 ATR). A buffer of 0 and a stop that is off stay off and
    draw nothing. MA type pair, slope filter, timeframe and symbol are never perturbed.
    v2 rules that are on: max hold and cooldown move by a non-zero integer of up to
    `integer_rel_step` (max hold >= 1, cooldown >= 0; a cooldown of 0 stays 0); take
    profit, min ADX and max extension by up to +/- `float_rel_step` relative. Rules that
    are off draw nothing, so v1 perturbations are unchanged."""
    rng = np.random.default_rng(derive_seed(base_seed, "perturb", config_id))

    def step_int(v: int, lo: int) -> int:
        k = max(1, round(pcfg.integer_rel_step * v))
        d = 0
        while d == 0:
            d = int(rng.integers(-k, k + 1))
        return max(lo, v + d)

    def step_rel(v: float, lo: float) -> float:
        return max(lo, v * (1 + float(rng.uniform(-pcfg.float_rel_step, pcfg.float_rel_step))))

    out = []
    for _ in range(pcfg.n_per_config):
        fast, slow = step_int(p.fast_length, 2), step_int(p.slow_length, 3)
        out.append(MAParams(
            symbol=p.symbol, timeframe=p.timeframe, ma_pair=p.ma_pair,
            fast_length=min(fast, slow - 1), slow_length=slow, confirm_bars=step_int(p.confirm_bars, 1),
            buffer_atr=step_rel(p.buffer_atr, 0.0) if p.buffer_atr else 0.0,
            stop_atr=None if p.stop_atr is None else step_rel(p.stop_atr, 0.25),
            slope_filter=p.slope_filter,
            max_hold=None if p.max_hold is None else step_int(p.max_hold, 1),
            take_profit_atr=None if p.take_profit_atr is None else step_rel(p.take_profit_atr, 0.25),
            cooldown_bars=step_int(p.cooldown_bars, 0) if p.cooldown_bars else 0,
            min_adx=None if p.min_adx is None else step_rel(p.min_adx, 1.0),
            max_extension_atr=None if p.max_extension_atr is None else step_rel(p.max_extension_atr, 0.25),
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
