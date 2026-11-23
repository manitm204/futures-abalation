"""Helpers for the funnel's diagnostics: reproducible parameter perturbations,
break-even execution cost, and trade-interval overlap between configs."""

from __future__ import annotations

import math
from dataclasses import replace
from datetime import datetime

import numpy as np

from src.experiments.funnel_config import PerturbationCfg
from src.strategies.compression_breakout.backtest import CBParams
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


# --- compression breakout ---------------------------------------------------------------------

def perturbations_cb(p: CBParams, *, config_id: str, base_seed: int, pcfg: PerturbationCfg) -> list[CBParams]:
    """Compression-breakout counterpart of `perturbations` (diagnostic only), jointly moving the
    settings the config's compression type uses: the squeeze length (never below 5) or NR-N
    (never below 2) and the setup expiry (never below 1) by a non-zero integer of up to
    `integer_rel_step` (at least 1 bar); the Keltner multiple (>= 0.25), an ATR stop (>= 0.25),
    a profit target (>= 0.25R) and a non-zero minimum box width by up to +/- `float_rel_step`
    RELATIVE. The box stop, "no target", no minimum box width, min_squeeze_bars, min_nr_bars, inside_bar,
    timeframe, entry type, direction, trend filter and symbol are never perturbed."""
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

    out = []
    for _ in range(pcfg.n_per_config):
        kw: dict = {}
        if p.compression == "bbkc":
            kw["squeeze_length"] = step_int(p.squeeze_length, 5)
            kw["kc_mult"] = step_rel(p.kc_mult, 0.25)
        else:
            kw["nr_lookback"] = step_int(p.nr_lookback, 2)
        kw["setup_expiry_bars"] = step_int(p.setup_expiry_bars, 1)
        if p.stop_atr is not None:
            kw["stop_atr"] = step_rel(p.stop_atr, 0.25)
        if p.target_r is not None:
            kw["target_r"] = step_rel(p.target_r, 0.25)
        if p.min_box_atr > 0:
            kw["min_box_atr"] = step_rel(p.min_box_atr, 0.0)
        out.append(replace(p, **kw))
    return out


def local_perturbations_cb(p: CBParams, lcfg) -> list[tuple[str, CBParams]]:
    """Stage-4 local test for the compression breakout: move ONE setting at a time, down and
    up, everything else held. Bar counts the config's compression type uses (squeeze length
    and min squeeze bars, or NR-N and min NR bars when set) and the setup expiry go to round(v x (1 -/+ int_rel)) (half
    rounds up), at least one bar away (squeeze length >= 2, NR-N >= 2, the others >= 1); the
    Keltner multiple by -/+ kc_mult_abs (>= 0.25); an ATR stop by -/+ stop_atr_abs (>= 0.25);
    a profit target by -/+ target_r_abs (>= 0.25R); the minimum box width by -/+
    min_box_atr_abs (>= 0, so a width of 0 only moves up). The box stop and "no target" have
    no numeric neighbor, so those configs get fewer moves. Timeframe and the categoricals
    (entry type, direction, trend filter, inside bar) are never moved. Returns (label, params)."""
    out: list[tuple[str, CBParams]] = []

    def add(name: str, values, field: str) -> None:
        for v in dict.fromkeys(values):
            if v != getattr(p, field):
                out.append((f"{name}={v:g}", replace(p, **{field: v})))

    def ints(v: int, lo: int) -> tuple[int, int]:
        down = max(lo, min(math.floor(v * (1 - lcfg.int_rel) + 0.5), v - 1))
        return down, max(math.floor(v * (1 + lcfg.int_rel) + 0.5), v + 1)

    if p.compression == "bbkc":
        add("squeeze_length", ints(p.squeeze_length, 2), "squeeze_length")
        add("kc_mult", (max(0.25, round(p.kc_mult - lcfg.kc_mult_abs, 6)),
                        round(p.kc_mult + lcfg.kc_mult_abs, 6)), "kc_mult")
        add("min_squeeze_bars", ints(p.min_squeeze_bars, 1), "min_squeeze_bars")
    else:
        add("nr_lookback", ints(p.nr_lookback, 2), "nr_lookback")
        if p.min_nr_bars is not None:  # an axis only in NR rounds that set it (v2 on)
            add("min_nr_bars", ints(p.min_nr_bars, 1), "min_nr_bars")
        if p.max_range_atr is not None:  # NR v3 range cap; "off" has no numeric neighbor
            step = lcfg.max_range_atr_abs if lcfg.max_range_atr_abs is not None else 0.1
            add("max_range_atr", (max(0.1, round(p.max_range_atr - step, 6)),
                                  round(p.max_range_atr + step, 6)), "max_range_atr")
    if p.max_hold_bars:  # time stop (NR v3); "none" has no numeric neighbor
        add("max_hold_bars", ints(p.max_hold_bars, 1), "max_hold_bars")
    add("setup_expiry_bars", ints(p.setup_expiry_bars, 1), "setup_expiry_bars")
    if p.stop_atr is not None:
        add("stop_atr", (max(0.25, round(p.stop_atr - lcfg.stop_atr_abs, 6)),
                         round(p.stop_atr + lcfg.stop_atr_abs, 6)), "stop_atr")
    if p.target_r is not None:
        add("target_r", (max(0.25, round(p.target_r - lcfg.target_r_abs, 6)),
                         round(p.target_r + lcfg.target_r_abs, 6)), "target_r")
    add("min_box_atr", (max(0.0, round(p.min_box_atr - lcfg.min_box_atr_abs, 6)),
                        round(p.min_box_atr + lcfg.min_box_atr_abs, 6)), "min_box_atr")
    return out


# --- price-path convexity ----------------------------------------------------------------------

def perturbations_pc(p, *, config_id: str, base_seed: int, pcfg: PerturbationCfg) -> list:
    """Convexity counterpart of `perturbations` (diagnostic only), jointly moving the look-back N
    (never below 3) and the z-score look-back (never below 20) by a non-zero integer of up to
    `integer_rel_step` (at least 1 bar), and the entry z (>= 0.1), an ATR stop (>= 0.25) and a
    non-zero minimum net move by up to +/- `float_rel_step` RELATIVE. The hold rule follows N
    (half / full scale with it). Signal form, quadrant, direction, hold type, trend filter,
    timeframe and symbol are never perturbed."""
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

    out = []
    for _ in range(pcfg.n_per_config):
        kw: dict = {"lookback": step_int(p.lookback, 3), "z_lookback": step_int(p.z_lookback, 20),
                    "entry_z": step_rel(p.entry_z, 0.1)}
        if p.stop_atr is not None:
            kw["stop_atr"] = step_rel(p.stop_atr, 0.25)
        if p.min_move_atr > 0:
            kw["min_move_atr"] = step_rel(p.min_move_atr, 0.0)
        out.append(replace(p, **kw))
    return out


def local_perturbations_pc(p, lcfg) -> list[tuple[str, object]]:
    """Stage-4 local test for the convexity line: move ONE setting at a time, down and up,
    everything else held. The look-back N and the z-score look-back go to round(v x (1 -/+
    int_rel)) (half rounds up), at least one bar away (N >= 3, z look-back >= 20); the entry z by
    -/+ entry_z_abs (>= 0.1); an ATR stop by -/+ stop_atr_abs (>= 0.25); the minimum net move by
    -/+ min_move_atr_abs (>= 0, so 0 only moves up). "No stop" has no numeric neighbor. Signal
    form, quadrant, direction, hold type and trend filter are never moved. Returns (label, params)."""
    out: list = []

    def add(name: str, values, field: str) -> None:
        for v in dict.fromkeys(values):
            if v != getattr(p, field):
                out.append((f"{name}={v:g}", replace(p, **{field: v})))

    def ints(v: int, lo: int) -> tuple[int, int]:
        down = max(lo, min(math.floor(v * (1 - lcfg.int_rel) + 0.5), v - 1))
        return down, max(math.floor(v * (1 + lcfg.int_rel) + 0.5), v + 1)

    add("lookback", ints(p.lookback, 3), "lookback")
    add("z_lookback", ints(p.z_lookback, 20), "z_lookback")
    add("entry_z", (max(0.1, round(p.entry_z - lcfg.entry_z_abs, 6)), round(p.entry_z + lcfg.entry_z_abs, 6)),
        "entry_z")
    if p.stop_atr is not None:
        add("stop_atr", (max(0.25, round(p.stop_atr - lcfg.stop_atr_abs, 6)),
                         round(p.stop_atr + lcfg.stop_atr_abs, 6)), "stop_atr")
    add("min_move_atr", (max(0.0, round(p.min_move_atr - lcfg.min_move_atr_abs, 6)),
                         round(p.min_move_atr + lcfg.min_move_atr_abs, 6)), "min_move_atr")
    return out


# --- FX fix ------------------------------------------------------------------------------------

def perturbations_fx(p, *, config_id: str, base_seed: int, pcfg: PerturbationCfg) -> list:
    """FX-fix counterpart of `perturbations` (diagnostic only): jointly moves the switch time by a
    non-zero whole number of minutes up to +/- 10, a numeric post hold by up to +/-
    `integer_rel_step` RELATIVE (at least 1 minute) and a stop by up to +/- `float_rel_step`
    RELATIVE (>= 0.05%). Leg, vol gate, "eod" hold, "no stop", timeframe and symbol are never
    perturbed."""
    rng = np.random.default_rng(derive_seed(base_seed, "perturb", config_id))
    rel = pcfg.float_rel_step if pcfg.float_rel_step is not None else pcfg.integer_rel_step
    out = []
    for _ in range(pcfg.n_per_config):
        d = 0
        while d == 0:
            d = int(rng.integers(-10, 11))
        kw: dict = {"switch_offset": p.switch_offset + d}
        if p.post_hold != "eod" and p.leg != "pre":
            h = int(p.post_hold)
            k = max(1, round(pcfg.integer_rel_step * h))
            dh = 0
            while dh == 0:
                dh = int(rng.integers(-k, k + 1))
            kw["post_hold"] = str(max(5, h + dh))
        if p.stop_pct is not None:
            kw["stop_pct"] = max(0.05, p.stop_pct * (1 + float(rng.uniform(-rel, rel))))
        out.append(replace(p, **kw))
    return out


def local_perturbations_fx(p, lcfg) -> list[tuple[str, object]]:
    """Stage-4 local test for the FX-fix line: move ONE setting at a time, down and up,
    everything else held. The switch time by -/+ switch_offset_abs minutes; a numeric post hold
    by -/+ post_hold_abs minutes (>= 5; legs that use it only); a stop by -/+ stop_pct_abs
    (>= 0.05%). "eod" and "no stop" have no numeric neighbor. Leg and vol gate are never moved.
    Returns (label, params)."""
    out: list = []

    def add(name: str, values, field: str, fmt=lambda v: f"{v:g}") -> None:
        for v in dict.fromkeys(values):
            if v != getattr(p, field):
                out.append((f"{name}={fmt(v)}", replace(p, **{field: v})))

    so = lcfg.switch_offset_abs or 5
    add("switch_offset", (p.switch_offset - so, p.switch_offset + so), "switch_offset")
    if p.post_hold != "eod" and p.leg != "pre":
        h, step = int(p.post_hold), lcfg.post_hold_abs or 15
        add("post_hold", (str(max(5, h - step)), str(h + step)), "post_hold", fmt=str)
    if p.stop_pct is not None:
        step = lcfg.stop_pct_abs or 0.05
        add("stop_pct", (max(0.05, round(p.stop_pct - step, 6)), round(p.stop_pct + step, 6)), "stop_pct")
    return out


# --- drift burst -------------------------------------------------------------------------------

def perturbations_db(p, *, config_id: str, base_seed: int, pcfg: PerturbationCfg) -> list:
    """Drift-burst counterpart of `perturbations` (diagnostic only): jointly moves the burst
    window (>= 2) and the hold (>= 1) by a non-zero integer of up to `integer_rel_step` RELATIVE (at
    least 1 minute), and the threshold (>= 2.0) and a volume gate (>= 1.0) by up to +/-
    `float_rel_step` RELATIVE. Side, news filter, "no gate", timeframe and symbol are never
    perturbed."""
    rng = np.random.default_rng(derive_seed(base_seed, "perturb", config_id))
    rel = pcfg.float_rel_step if pcfg.float_rel_step is not None else pcfg.integer_rel_step

    def step_int(v: int, lo: int) -> int:
        k = max(1, round(pcfg.integer_rel_step * v))
        d = 0
        while d == 0:
            d = int(rng.integers(-k, k + 1))
        return max(lo, v + d)

    out = []
    for _ in range(pcfg.n_per_config):
        kw: dict = {"burst_window": step_int(p.burst_window, 2), "hold": step_int(p.hold, 1),
                    "threshold": max(2.0, p.threshold * (1 + float(rng.uniform(-rel, rel))))}
        if p.vol_gate is not None:
            kw["vol_gate"] = max(1.0, p.vol_gate * (1 + float(rng.uniform(-rel, rel))))
        if p.target is not None:
            kw["target"] = max(0.1, p.target * (1 + float(rng.uniform(-rel, rel))))
        if p.stop is not None:
            kw["stop"] = max(0.25, p.stop * (1 + float(rng.uniform(-rel, rel))))
        out.append(replace(p, **kw))
    return out


def local_perturbations_db(p, lcfg) -> list[tuple[str, object]]:
    """Stage-4 local test for the drift-burst line: move ONE setting at a time, down and up,
    everything else held. Burst window and hold go to round(v x (1 -/+ int_rel)) (half rounds up),
    at least one minute away (window >= 2, hold >= 1); the threshold by -/+ threshold_abs (>= 2.0);
    a volume gate by -/+ vol_gate_abs (>= 1.0). "No gate", side and news filter are never moved.
    Returns (label, params)."""
    out: list = []

    def add(name: str, values, field: str) -> None:
        for v in dict.fromkeys(values):
            if v != getattr(p, field):
                out.append((f"{name}={v:g}", replace(p, **{field: v})))

    def ints(v: int, lo: int) -> tuple[int, int]:
        down = max(lo, min(math.floor(v * (1 - lcfg.int_rel) + 0.5), v - 1))
        return down, max(math.floor(v * (1 + lcfg.int_rel) + 0.5), v + 1)

    add("burst_window", ints(p.burst_window, 2), "burst_window")
    add("hold", ints(p.hold, 1), "hold")
    ta = lcfg.threshold_abs or 0.25
    add("threshold", (max(2.0, round(p.threshold - ta, 6)), round(p.threshold + ta, 6)), "threshold")
    if p.vol_gate is not None:
        va = lcfg.vol_gate_abs or 0.25
        add("vol_gate", (max(1.0, round(p.vol_gate - va, 6)), round(p.vol_gate + va, 6)), "vol_gate")
    # v2 axes: moved only when the YAML sets their step (v1 runs never move them).
    if p.target is not None and lcfg.target_abs:
        add("target", (max(0.1, round(p.target - lcfg.target_abs, 6)), round(p.target + lcfg.target_abs, 6)), "target")
    if p.stop is not None and lcfg.stop_burst_abs:
        add("stop", (max(0.25, round(p.stop - lcfg.stop_burst_abs, 6)), round(p.stop + lcfg.stop_burst_abs, 6)), "stop")
    if lcfg.max_trades_step:
        st = lcfg.max_trades_step
        add("max_trades", (max(1, p.max_trades - st), p.max_trades + st), "max_trades")
    return out


# --- month end ---------------------------------------------------------------------------------

def perturbations_me(p, *, config_id: str, base_seed: int, pcfg: PerturbationCfg) -> list:
    """Month-end counterpart of `perturbations` (diagnostic only): jointly moves the entry time
    and the exit target by a non-zero whole number of minutes up to +/- 30 each (entry kept at or
    after 08:00 and at least 15 minutes before the exit), and a stop by up to +/- `float_rel_step`
    RELATIVE (>= 0.05%). Window, exit rule, event filter, "no stop", timeframe and symbol are never
    perturbed."""
    rng = np.random.default_rng(derive_seed(base_seed, "perturb", config_id))

    def nz(k: int) -> int:
        d = 0
        while d == 0:
            d = int(rng.integers(-k, k + 1))
        return d

    out = []
    for _ in range(pcfg.n_per_config):
        shift = p.exit_shift + nz(30)
        entry = max(8 * 60, p.entry_min + nz(30))
        entry = min(entry, 15 * 60 - 15 + shift)
        kw: dict = {"entry_min": entry, "exit_shift": shift}
        if p.stop_pct is not None:
            rel = pcfg.float_rel_step if pcfg.float_rel_step is not None else pcfg.integer_rel_step
            kw["stop_pct"] = max(0.05, p.stop_pct * (1 + float(rng.uniform(-rel, rel))))
        out.append(replace(p, **kw))
    return out


def local_perturbations_me(p, lcfg) -> list[tuple[str, object]]:
    """Stage-4 local test for the month-end line: move ONE setting at a time, down and up,
    everything else held. The entry time by -/+ entry_shift_abs minutes (not before 08:00); the
    exit target by -/+ exit_shift_abs minutes; the window by -/+ window_step days and (v2) the
    first-days count by -/+ first_days_step (each >= 0, never both 0); a stop by
    -/+ stop_pct_abs (>= 0.05%). The exit rule, the event filter and "no stop" are never moved.
    Returns (label, params)."""
    out: list = []

    def add(name: str, values, field: str, fmt) -> None:
        for v in dict.fromkeys(values):
            if v != getattr(p, field):
                out.append((f"{name}={fmt(v)}", replace(p, **{field: v})))

    hhmm = lambda m: f"{m // 60:02d}:{m % 60:02d}"  # noqa: E731
    es = lcfg.entry_shift_abs or 30
    add("entry", (max(8 * 60, p.entry_min - es), p.entry_min + es), "entry_min", hhmm)
    xs = lcfg.exit_shift_abs or 15
    add("exit_shift", (p.exit_shift - xs, p.exit_shift + xs), "exit_shift", lambda v: f"{v:+d}min")
    ws = lcfg.window_step or 1
    add("window", (max(0 if p.first_days else 1, p.window - ws), p.window + ws), "window", str)
    if lcfg.first_days_step:  # v2 only
        fs = lcfg.first_days_step
        add("first_days", (max(0 if p.window else 1, p.first_days - fs), p.first_days + fs), "first_days", str)
    if p.stop_pct is not None:
        st = lcfg.stop_pct_abs or 0.10
        add("stop_pct", (max(0.05, round(p.stop_pct - st, 6)), round(p.stop_pct + st, 6)), "stop_pct",
            lambda v: f"{v:g}")
    return out


def perturbations_lh(p, *, config_id: str, base_seed: int, pcfg: PerturbationCfg) -> list:
    """Last-half-hour counterpart of `perturbations` (diagnostic only): jointly moves the entry
    and exit times by a non-zero whole number of minutes up to +/- 5 each (entry at or after
    14:30, exit at most 16:00 and at least 5 minutes after the entry), a z threshold and a stop by
    up to +/- `float_rel_step` RELATIVE. Signal, agreement, filter kind, "no stop", timeframe and
    symbol are never perturbed."""
    rng = np.random.default_rng(derive_seed(base_seed, "perturb", config_id))

    def nz(k: int) -> int:
        d = 0
        while d == 0:
            d = int(rng.integers(-k, k + 1))
        return d

    rel = pcfg.float_rel_step if pcfg.float_rel_step is not None else pcfg.integer_rel_step
    out = []
    for _ in range(pcfg.n_per_config):
        entry = max(14 * 60 + 30, p.entry_min + nz(5))
        exit_ = min(16 * 60, p.exit_min + nz(5))
        entry = min(entry, exit_ - 5)
        kw: dict = {"entry_min": entry, "exit_min": exit_}
        if p.z is not None:
            kw["z"] = max(0.05, p.z * (1 + float(rng.uniform(-rel, rel))))
        if p.stop_pct is not None:
            kw["stop_pct"] = max(0.02, p.stop_pct * (1 + float(rng.uniform(-rel, rel))))
        out.append(replace(p, **kw))
    return out


def local_perturbations_lh(p, lcfg) -> list[tuple[str, object]]:
    """Stage-4 local test for last-half-hour momentum: move ONE setting at a time, down and up,
    everything else held. The entry time by -/+ entry_shift_abs minutes and the exit time by
    -/+ exit_shift_abs minutes (exit never after 16:00, always >= 5 minutes after the entry); a
    z threshold by -/+ threshold_abs (>= 0.05); a stop by -/+ stop_pct_abs (>= 0.02%). Signal,
    agreement, filter kind and "no stop" are never moved. Returns (label, params)."""
    out: list = []

    def add(name: str, values, field: str, fmt) -> None:
        for v in dict.fromkeys(values):
            if v != getattr(p, field):
                out.append((f"{name}={fmt(v)}", replace(p, **{field: v})))

    hhmm = lambda m: f"{m // 60:02d}:{m % 60:02d}"  # noqa: E731
    es = lcfg.entry_shift_abs or 5
    add("entry", [m for m in (p.entry_min - es, p.entry_min + es) if m <= p.exit_min - 5], "entry_min", hhmm)
    xs = lcfg.exit_shift_abs or 5
    add("exit", [m for m in (p.exit_min - xs, p.exit_min + xs) if p.entry_min + 5 <= m <= 16 * 60], "exit_min", hhmm)
    if p.z is not None:
        za = lcfg.threshold_abs or 0.25
        add("z", (max(0.05, round(p.z - za, 6)), round(p.z + za, 6)), "z", lambda v: f"{v:g}")
    if p.stop_pct is not None:
        st = lcfg.stop_pct_abs or 0.05
        add("stop_pct", (max(0.02, round(p.stop_pct - st, 6)), round(p.stop_pct + st, 6)), "stop_pct",
            lambda v: f"{v:g}")
    return out


def perturbations_os(p, *, config_id: str, base_seed: int, pcfg: PerturbationCfg) -> list:
    """NY-open sweep counterpart of `perturbations` (diagnostic only): jointly moves the window by
    a non-zero whole number of minutes up to +/- 5 (>= 5), the time exit by up to +/- 15 minutes
    (after the window, by 16:00), the confirm count by -1/0/+1 (>= 1), and the penetration, a dATR
    stop and an R target by up to +/- `float_rel_step` RELATIVE. Level, side, mode, the stop and
    target kinds, timeframe and symbol are never perturbed."""
    rng = np.random.default_rng(derive_seed(base_seed, "perturb", config_id))

    def nz(k: int) -> int:
        d = 0
        while d == 0:
            d = int(rng.integers(-k, k + 1))
        return d

    rel = pcfg.float_rel_step if pcfg.float_rel_step is not None else pcfg.integer_rel_step
    out = []
    for _ in range(pcfg.n_per_config):
        window = max(5, p.window + nz(5))
        exit_ = min(16 * 60, p.exit_min + nz(15))
        exit_ = max(exit_, 9 * 60 + 30 + window + 5)
        kw: dict = {"window": window, "exit_min": exit_,
                    "confirm": max(1, p.confirm + int(rng.integers(-1, 2))),
                    "pen": max(0.0, p.pen * (1 + float(rng.uniform(-rel, rel)))) if p.pen > 0
                    else float(rng.uniform(0, 0.01))}
        if p.stop_mult is not None:
            kw["stop_mult"] = max(0.03, p.stop_mult * (1 + float(rng.uniform(-rel, rel))))
        if p.target_r is not None:
            kw["target_r"] = max(0.25, p.target_r * (1 + float(rng.uniform(-rel, rel))))
        out.append(replace(p, **kw))
    return out


def local_perturbations_os(p, lcfg) -> list[tuple[str, object]]:
    """Stage-4 local test for the NY-open sweep: move ONE setting at a time, down and up,
    everything else held. Window -/+ entry_shift_abs minutes (>= 5); time exit -/+ exit_shift_abs
    minutes (after the window end, by 16:00); penetration -/+ threshold_abs x dATR (>= 0);
    confirm -/+ window_step bars (>= 1); a dATR stop -/+ stop_pct_abs x dATR (>= 0.03); an R
    target -/+ target_r_abs (>= 0.5). Level, side, mode, the structural stop and the
    none/range targets are never moved. Returns (label, params)."""
    out: list = []

    def add(name: str, values, field: str, fmt) -> None:
        for v in dict.fromkeys(values):
            if v != getattr(p, field):
                out.append((f"{name}={fmt(v)}", replace(p, **{field: v})))

    hhmm = lambda m: f"{m // 60:02d}:{m % 60:02d}"  # noqa: E731
    ws = lcfg.entry_shift_abs or 5
    add("window", [w for w in (p.window - ws, p.window + ws) if w >= 5 and 9 * 60 + 30 + w < p.exit_min],
        "window", str)
    xs = lcfg.exit_shift_abs or 15
    add("exit", [m for m in (p.exit_min - xs, p.exit_min + xs) if 9 * 60 + 30 + p.window < m <= 16 * 60],
        "exit_min", hhmm)
    pa = lcfg.threshold_abs or 0.025
    add("pen", (max(0.0, round(p.pen - pa, 6)), round(p.pen + pa, 6)), "pen", lambda v: f"{v:g}")
    cs = lcfg.window_step or 1
    add("confirm", (max(1, p.confirm - cs), p.confirm + cs), "confirm", str)
    if p.stop_mult is not None:
        st = lcfg.stop_pct_abs or 0.05
        add("stop", (max(0.03, round(p.stop_mult - st, 6)), round(p.stop_mult + st, 6)), "stop_mult",
            lambda v: f"d{v:g}")
    if p.target_r is not None:
        ta = lcfg.target_r_abs or 0.5
        add("target", (max(0.5, round(p.target_r - ta, 6)), round(p.target_r + ta, 6)), "target_r",
            lambda v: f"{v:g}R")
    return out


def perturbations_sb(p, *, config_id: str, base_seed: int, pcfg: PerturbationCfg) -> list:
    """Silver Bullet counterpart of `perturbations` (diagnostic only): jointly moves the FVG
    minimum, the displacement threshold and an R target by up to +/- `float_rel_step` RELATIVE
    (a zero FVG minimum moves to [0, 0.1]), the swing length by -1/0/+1 (>= 2) and the order life
    by a non-zero whole number of bars up to +/- 10 (>= 5). Window, sweep requirement, entry,
    stop and target kinds, timeframe and symbol are never perturbed."""
    rng = np.random.default_rng(derive_seed(base_seed, "perturb", config_id))
    rel = pcfg.float_rel_step if pcfg.float_rel_step is not None else pcfg.integer_rel_step
    out = []
    for _ in range(pcfg.n_per_config):
        d = 0
        while d == 0:
            d = int(rng.integers(-10, 11))
        kw: dict = {"fvg_min": max(0.0, p.fvg_min * (1 + float(rng.uniform(-rel, rel)))) if p.fvg_min > 0
                    else float(rng.uniform(0, 0.1)),
                    "disp": max(0.0, p.disp * (1 + float(rng.uniform(-rel, rel)))),
                    "swing": max(2, p.swing + int(rng.integers(-1, 2))),
                    "max_age": max(5, p.max_age + d)}
        if p.target_r is not None:
            kw["target_r"] = max(0.5, p.target_r * (1 + float(rng.uniform(-rel, rel))))
        out.append(replace(p, **kw))
    return out


def local_perturbations_sb(p, lcfg) -> list[tuple[str, object]]:
    """Stage-4 local test for the Silver Bullet: move ONE setting at a time, down and up,
    everything else held. FVG minimum -/+ fvg_min_abs ATR (>= 0); displacement -/+ disp_abs ATR
    (>= 0); an R target -/+ target_r_abs (>= 1); and the two grid-fixed choices, swing length
    -/+ swing_step bars (>= 2) and order life -/+ max_age_step bars (>= 5). Window, sweep
    requirement, entry, stop and the liq/none targets are never moved. Returns (label, params)."""
    out: list = []

    def add(name: str, values, field: str, fmt) -> None:
        for v in dict.fromkeys(values):
            if v != getattr(p, field):
                out.append((f"{name}={fmt(v)}", replace(p, **{field: v})))

    fa = lcfg.fvg_min_abs or 0.25
    add("fvg_min", (max(0.0, round(p.fvg_min - fa, 6)), round(p.fvg_min + fa, 6)), "fvg_min", lambda v: f"{v:g}")
    da = lcfg.disp_abs or 0.25
    add("disp", (max(0.0, round(p.disp - da, 6)), round(p.disp + da, 6)), "disp", lambda v: f"{v:g}")
    if p.target_r is not None:
        ta = lcfg.target_r_abs or 0.5
        add("target", (max(1.0, round(p.target_r - ta, 6)), round(p.target_r + ta, 6)), "target_r",
            lambda v: f"{v:g}R")
    ss = lcfg.swing_step or 1
    add("swing", (max(2, p.swing - ss), p.swing + ss), "swing", str)
    ms = lcfg.max_age_step or 10
    add("max_age", (max(5, p.max_age - ms), p.max_age + ms), "max_age", str)
    return out


def perturbations_fv(p, *, config_id: str, base_seed: int, pcfg: PerturbationCfg) -> list:
    """FVG counterpart of `perturbations` (diagnostic only): jointly moves the displacement, the gap
    minimum (a zero one to [0, 0.1]), an ATR stop and an R target by up to +/- `float_rel_step`
    RELATIVE, a resting order's wait by a non-zero whole number of bars up to +/- 5 (>= 1) and the
    hold by up to +/- 5 minutes (>= 5). Window, mode, VWAP gate, entry kind, stop / target kinds,
    timeframe and symbol are never perturbed."""
    rng = np.random.default_rng(derive_seed(base_seed, "perturb", config_id))
    rel = pcfg.float_rel_step if pcfg.float_rel_step is not None else pcfg.integer_rel_step

    def nz(k: int) -> int:
        d = 0
        while d == 0:
            d = int(rng.integers(-k, k + 1))
        return d
    out = []
    for _ in range(pcfg.n_per_config):
        kw: dict = {"disp": max(0.0, p.disp * (1 + float(rng.uniform(-rel, rel)))),
                    "fvg_min": max(0.0, p.fvg_min * (1 + float(rng.uniform(-rel, rel)))) if p.fvg_min > 0
                    else float(rng.uniform(0, 0.1)),
                    "hold": max(5, p.hold + nz(5))}
        if p.entry != "mkt":
            kw["wait"] = max(1, p.wait + nz(5))
        if p.stop_mult is not None:
            kw["stop_mult"] = max(1.0, p.stop_mult * (1 + float(rng.uniform(-rel, rel))))
        if p.target_r is not None:
            kw["target_r"] = max(0.5, p.target_r * (1 + float(rng.uniform(-rel, rel))))
        out.append(replace(p, **kw))
    return out


def local_perturbations_fv(p, lcfg) -> list[tuple[str, object]]:
    """Stage-4 local test for the FVG trade: move ONE setting at a time, down and up, everything
    else held. Displacement -/+ disp_abs ATR (>= 0); gap minimum -/+ fvg_min_abs ATR (>= 0); a
    resting order's wait -/+ wait_step bars (>= 1); an ATR stop -/+ stop_mult_abs (>= 1); an R
    target -/+ target_r_abs (>= 0.5); the hold -/+ hold_step minutes (>= 5). Window, mode, VWAP
    gate, entry kind, the struct stop and the no-target setting are never moved."""
    out: list = []

    def add(name: str, values, field: str, fmt) -> None:
        for v in dict.fromkeys(values):
            if v != getattr(p, field):
                out.append((f"{name}={fmt(v)}", replace(p, **{field: v})))

    da = lcfg.disp_abs or 0.25
    add("disp", (max(0.0, round(p.disp - da, 6)), round(p.disp + da, 6)), "disp", lambda v: f"{v:g}")
    fa = lcfg.fvg_min_abs or 0.25
    add("fvg_min", (max(0.0, round(p.fvg_min - fa, 6)), round(p.fvg_min + fa, 6)), "fvg_min", lambda v: f"{v:g}")
    if p.entry != "mkt":
        ws = lcfg.wait_step or 5
        add("wait", (max(1, p.wait - ws), p.wait + ws), "wait", str)
    if p.stop_mult is not None:
        sa = lcfg.stop_mult_abs or 0.5
        add("stop", (max(1.0, round(p.stop_mult - sa, 6)), round(p.stop_mult + sa, 6)), "stop_mult",
            lambda v: f"a{v:g}")
    if p.target_r is not None:
        ta = lcfg.target_r_abs or 0.5
        add("target", (max(0.5, round(p.target_r - ta, 6)), round(p.target_r + ta, 6)), "target_r",
            lambda v: f"{v:g}R")
    hs = lcfg.hold_step or 5
    add("hold", (max(5, p.hold - hs), p.hold + hs), "hold", str)
    return out
