"""Helpers for the funnel's diagnostics: reproducible parameter perturbations,
break-even execution cost, and trade-interval overlap between configs."""

from __future__ import annotations

import math
from dataclasses import replace
from datetime import datetime

import numpy as np

from src.experiments.funnel_config import PerturbationCfg
from src.strategies.mean_reversion.backtest import MRParams
from src.strategies.noise_band.backtest import NBParams
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


def perturbations_v3(p: MRParams, *, config_id: str, base_seed: int, pcfg: PerturbationCfg) -> list[MRParams]:
    """v3 counterpart: mean and std lookbacks move independently (as in v1), the
    holding cap by a non-zero integer of up to `integer_rel_step` (>= 1 bar), z
    thresholds by +/- `z_abs`, an ATR stop by up to +/- `integer_rel_step`
    relative (never below 0.5 ATR); "no stop" stays no stop. Categoricals
    (timeframe, mean_type, entry_confirmation, symbol) are never perturbed."""
    rng = np.random.default_rng(derive_seed(base_seed, "perturb", config_id))

    def step_int(v: int, lo: int) -> int:
        k = max(1, round(pcfg.integer_rel_step * v))
        d = 0
        while d == 0:
            d = int(rng.integers(-k, k + 1))
        return max(lo, v + d)

    out = []
    for _ in range(pcfg.n_per_config):
        stop = p.stop_atr
        if stop is not None:
            stop = max(0.5, stop * (1 + float(rng.uniform(-pcfg.integer_rel_step, pcfg.integer_rel_step))))
        out.append(MRParams(
            symbol=p.symbol, timeframe=p.timeframe, mean_type=p.mean_type,
            mean_lookback=step_int(p.mean_lookback, 2), std_lookback=step_int(p.std_lookback, 2),
            entry_z=p.entry_z + float(rng.uniform(-pcfg.z_abs, pcfg.z_abs)),
            exit_z=p.exit_z + float(rng.uniform(-pcfg.z_abs, pcfg.z_abs)),
            max_hold=step_int(p.max_hold, 1), trend_filter=p.trend_filter,
            entry_confirmation=p.entry_confirmation, cooldown_bars=0, stop_atr=stop,
        ))
    return out


def local_perturbations(p: MRParams, lcfg) -> list[tuple[str, MRParams]]:
    """Stage-4 local test: move ONE setting at a time, down and up, everything else
    held. Mean / std lookbacks and the holding cap go to round(v x (1 -/+ int_rel))
    (half rounds up), at least one bar away from v (lookbacks never below 2, hold
    never below 1); entry / exit z by -/+ their absolute steps; a numeric ATR stop by
    -/+ stop_atr_abs (never below 0.25). "No stop" has no numeric neighbor and is
    left alone, so those configs get two fewer moves. Categoricals (timeframe,
    mean_type, entry_confirmation) are never moved. Returns (label, params)."""
    def ints(v: int, lo: int) -> tuple[int, int]:
        down = min(math.floor(v * (1 - lcfg.int_rel) + 0.5), v - 1)
        up = max(math.floor(v * (1 + lcfg.int_rel) + 0.5), v + 1)
        return max(lo, down), up

    out: list[tuple[str, MRParams]] = []

    def add(name: str, values, field: str) -> None:
        for v in values:
            if v != getattr(p, field):
                out.append((f"{name}={v:g}", replace(p, **{field: v})))

    add("mean_lookback", ints(p.mean_lookback, 2), "mean_lookback")
    add("std_lookback", ints(p.std_lookback, 2), "std_lookback")
    add("entry_z", (round(p.entry_z - lcfg.entry_z_abs, 6), round(p.entry_z + lcfg.entry_z_abs, 6)), "entry_z")
    add("exit_z", (round(p.exit_z - lcfg.exit_z_abs, 6), round(p.exit_z + lcfg.exit_z_abs, 6)), "exit_z")
    add("max_hold", ints(p.max_hold, 1), "max_hold")
    if p.stop_atr is not None:
        add("stop_atr", (max(0.25, round(p.stop_atr - lcfg.stop_atr_abs, 6)),
                         round(p.stop_atr + lcfg.stop_atr_abs, 6)), "stop_atr")
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


# --- noise-band breakout ----------------------------------------------------------------------

def perturbations_nb(p: NBParams, *, config_id: str, base_seed: int, pcfg: PerturbationCfg) -> list[NBParams]:
    """Noise-band counterpart of `perturbations` (diagnostic only): the band lookback
    moves by a non-zero integer of up to `integer_rel_step` (at least 1 session, never
    below 2); the band multiple and an ATR stop that is on by up to +/- `float_rel_step`
    RELATIVE (band >= 0.1, stop >= 0.25 ATR); "no stop" stays no stop. Timeframe, check
    interval, anchor, trail, direction and symbol are never perturbed."""
    rng = np.random.default_rng(derive_seed(base_seed, "perturb", config_id))
    rel = pcfg.float_rel_step if pcfg.float_rel_step is not None else pcfg.integer_rel_step

    def step_int(v: int, lo: int) -> int:
        k = max(1, round(pcfg.integer_rel_step * v))
        d = 0
        while d == 0:
            d = int(rng.integers(-k, k + 1))
        return max(lo, v + d)

    def step_rel(v: float, lo: float) -> float:
        return max(lo, v * (1 + float(rng.uniform(-rel, rel))))

    return [replace(p, band_lookback=step_int(p.band_lookback, 2), band_mult=step_rel(p.band_mult, 0.1),
                    stop_atr=None if p.stop_atr is None else step_rel(p.stop_atr, 0.25))
            for _ in range(pcfg.n_per_config)]


def local_perturbations_nb(p: NBParams, lcfg) -> list[tuple[str, NBParams]]:
    """Stage-4 local test for the noise band: move ONE setting at a time, down and up,
    everything else held. The band lookback goes to round(v x (1 -/+ int_rel)) (half
    rounds up), at least one session away (never below 1); the band multiple by -/+
    band_mult_abs (never below 0.1); a numeric ATR stop by -/+ stop_atr_abs (never below
    0.25). "No stop" has no numeric neighbor, so those configs get two fewer moves. The
    check interval, timeframe and the categoricals are never moved. Returns (label, params)."""
    down = max(1, min(math.floor(p.band_lookback * (1 - lcfg.int_rel) + 0.5), p.band_lookback - 1))
    up = max(math.floor(p.band_lookback * (1 + lcfg.int_rel) + 0.5), p.band_lookback + 1)
    out: list[tuple[str, NBParams]] = []

    def add(name: str, values, field: str) -> None:
        for v in dict.fromkeys(values):  # lookback 1 has no move down
            if v != getattr(p, field):
                out.append((f"{name}={v:g}", replace(p, **{field: v})))

    add("band_lookback", (down, up), "band_lookback")
    add("band_mult", (max(0.1, round(p.band_mult - lcfg.band_mult_abs, 6)),
                      round(p.band_mult + lcfg.band_mult_abs, 6)), "band_mult")
    if p.stop_atr is not None:
        add("stop_atr", (max(0.25, round(p.stop_atr - lcfg.stop_atr_abs, 6)),
                         round(p.stop_atr + lcfg.stop_atr_abs, 6)), "stop_atr")
    return out
