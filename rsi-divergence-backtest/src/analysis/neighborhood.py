"""Parameter-neighborhood stability.

A robust configuration should be surrounded by configurations that also work: a
lone profitable island in a sea of losers is almost always overfit. For each
config we look at its IMMEDIATE neighbors on the grid lattice -- one step along a
single ordered axis (optionally also joint one-step moves on two axes) --
holding the categorical axes (mean_type, trend_filter, symbol) fixed, and measure the
fraction of profitable neighbors and the median neighbor Sharpe.

Neighbors are drawn from the FULL configuration universe, including configs
rejected by earlier gates. A neighbor is "valid" when it exists in the grid and
was backtested; neighbors whose Sharpe is undefined (e.g. zero variance) still
count toward the profitable fraction (they are not profitable) but are excluded
from the median Sharpe, and are counted separately. A config at a grid boundary
has fewer possible neighbors; that limited coverage is reported, not hidden.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field

import numpy as np

# Ordered axes (value order matters for "adjacent"); categorical axes are held fixed.
# entry_z runs from the shallowest to the deepest dip (-1.0 .. -2.0).
ORDERED_AXES: dict[str, list] = {
    "timeframe": ["5min", "15min", "1h"],
    "mean_lookback": [5, 10, 15, 20, 40],
    "std_lookback": [10, 15, 20, 40, 60],
    "entry_z": [-1.0, -1.25, -1.5, -1.75, -2.0],
    "exit_z": [-0.5, -0.25, 0.0, 0.25, 0.5],
    "max_hold": [2, 3, 5, 7, 10],
}
FIXED_AXES = ["symbol", "mean_type", "trend_filter"]
MAX_SINGLE_AXIS_NEIGHBORS = 2 * len(ORDERED_AXES)

# v2 lattice. stop_atr_multiple: "none" means no stop, i.e. an infinitely wide
# one, so it sits AFTER the widest stop (3 ATR), not before the tightest.
ORDERED_AXES_V2: dict[str, list] = {
    "timeframe": ["5min", "15min", "1h"],
    "mean_lookback": [8, 12, 20, 32, 48],
    "entry_z": [-1.0, -1.25, -1.5, -1.75, -2.0],
    "exit_z": [-0.25, 0.0, 0.25, 0.5],
    "max_holding_bars": [2, 4, 8, 16],
    "cooldown_bars": [0, 1, 2, 4, 8],
    "stop_atr_multiple": ["1.0", "1.5", "2.0", "3.0", "none"],
}
FIXED_AXES_V2 = ["symbol", "mean_type", "trend_filter", "entry_confirmation"]

# RSI-divergence lattice: every axis is ordered (no categoricals besides symbol).
ORDERED_AXES_RSI: dict[str, list] = {
    "timeframe": ["5min", "15min", "1h"],
    "rsi_lookback": [7, 10, 14, 21],
    "pivot_left": [3, 5, 8, 12],
    "pivot_right": [1, 3],
    "max_pivot_gap": [12, 24, 48, 78],
    "min_rsi_diff": [0.0, 3.0, 5.0, 8.0],
    "stop_atr": [0.75, 1.0, 1.5, 2.0],
    "target_r": [1.0, 1.5, 2.0, 3.0],
    "max_hold": [6, 12, 24, 48],
}
FIXED_AXES_RSI = ["symbol"]

# RSI-divergence v2 lattice. The filters run from loosest to strictest (off first);
# pivot_right has a single value, so it is held fixed rather than ordered.
ORDERED_AXES_RSI_V2: dict[str, list] = {
    "timeframe": ["5min", "15min"],
    "rsi_lookback": [7, 10, 14],
    "pivot_left": [3, 5, 8],
    "max_pivot_gap": [8, 12, 24],
    "min_rsi_diff": [0.0, 5.0],
    "stop_atr": [1.5, 2.0, 2.5],
    "target_r": [1.5, 2.0, 3.0],
    "max_hold": [24, 48],
    "rsi_extreme": ["off", "40/60", "30/70"],
    "adx_filter": ["off", "lt30", "lt20"],
    "min_price_div_atr": [0.0, 0.1, 0.25, 0.5],
}
FIXED_AXES_RSI_V2 = ["symbol", "pivot_right"]

# RSI-divergence v3 lattice. Single-value axes (pivot_right, adx_filter) and the
# categorical rules (trend filter, entry confirmation, session window) are held
# fixed; "off" has no natural place among EMA lengths, as with MR's trend_filter.
ORDERED_AXES_RSI_V3: dict[str, list] = {
    "timeframe": ["5min", "15min"],
    "rsi_lookback": [7, 10, 14],
    "pivot_left": [3, 5],
    "max_pivot_gap": [12, 24],
    "min_rsi_diff": [0.0, 5.0],
    "stop_atr": [1.5, 2.0, 2.5],
    "target_r": [1.5, 2.0, 3.0],
    "max_hold": [24, 48, 72],
    "rsi_extreme": ["off", "40/60", "30/70"],
    "min_price_div_atr": [0.0, 0.25],
}
FIXED_AXES_RSI_V3 = ["symbol", "pivot_right", "adx_filter", "trend_filter", "entry_confirmation", "session_window"]


@dataclass(frozen=True)
class Lattice:
    ordered: dict[str, list]
    fixed: list[str]

    @property
    def index(self) -> dict[str, dict]:
        return {ax: {v: i for i, v in enumerate(vals)} for ax, vals in self.ordered.items()}


LATTICE_V1 = Lattice(ORDERED_AXES, FIXED_AXES)
LATTICE_V2 = Lattice(ORDERED_AXES_V2, FIXED_AXES_V2)
LATTICE_RSI = Lattice(ORDERED_AXES_RSI, FIXED_AXES_RSI)
LATTICE_RSI_V2 = Lattice(ORDERED_AXES_RSI_V2, FIXED_AXES_RSI_V2)
LATTICE_RSI_V3 = Lattice(ORDERED_AXES_RSI_V3, FIXED_AXES_RSI_V3)


@dataclass(frozen=True)
class NeighborhoodStats:
    n_neighbors: int                 # valid neighbors found in the universe
    n_possible: int                  # lattice positions inside the grid bounds
    frac_profitable: float | None    # None when n_neighbors == 0
    median_sharpe: float | None      # None when no neighbor has a defined Sharpe
    n_sharpe_undefined: int = 0
    boundary_axes: list[str] = field(default_factory=list)

    @property
    def limited_coverage(self) -> bool:
        return bool(self.boundary_axes)


def _key(cfg: dict, lat: Lattice, idx: dict) -> tuple:
    return tuple(cfg[a] for a in lat.fixed) + tuple(idx[ax][cfg[ax]] for ax in lat.ordered)


def _neighbor_keys(cfg: dict, *, include_joint: bool, lat: Lattice, idx: dict) -> tuple[list[tuple], list[str]]:
    fixed = tuple(cfg[a] for a in lat.fixed)
    base = [idx[ax][cfg[ax]] for ax in lat.ordered]
    axes = list(lat.ordered)
    sizes = [len(lat.ordered[a]) for a in axes]
    out: list[tuple] = []
    boundary = [a for a, b, s in zip(axes, base, sizes) if b == 0 or b == s - 1]

    def shifted(moves: dict[int, int]) -> tuple | None:
        pos = list(base)
        for ai, delta in moves.items():
            pos[ai] += delta
            if pos[ai] < 0 or pos[ai] >= sizes[ai]:
                return None
        return fixed + tuple(pos)

    for ai in range(len(axes)):
        for delta in (-1, 1):
            k = shifted({ai: delta})
            if k is not None:
                out.append(k)
    if include_joint:
        for ai, aj in itertools.combinations(range(len(axes)), 2):
            for da, db in itertools.product((-1, 1), (-1, 1)):
                k = shifted({ai: da, aj: db})
                if k is not None:
                    out.append(k)
    return out, boundary


def neighbor_ids(configs: list[dict], *, include_joint: bool = False,
                 lattice: Lattice = LATTICE_V1) -> dict[str, list[str]]:
    """config_id -> ids of its valid immediate neighbors in `configs`."""
    idx = lattice.index
    by_key = {_key(c, lattice, idx): c["config_id"] for c in configs}
    out = {}
    for c in configs:
        keys, _ = _neighbor_keys(c, include_joint=include_joint, lat=lattice, idx=idx)
        out[c["config_id"]] = [by_key[k] for k in keys if k in by_key]
    return out


def neighborhood_stats(
    configs: list[dict],
    *,
    net_return_key: str,
    sharpe_key: str,
    include_joint: bool = False,
    only_ids: set[str] | None = None,
    lattice: Lattice = LATTICE_V1,
) -> dict[str, NeighborhoodStats]:
    """Map config_id -> NeighborhoodStats. Each input dict needs the axis fields,
    `config_id`, and the chosen development net-return / Sharpe metric values.
    `configs` should be the full universe; `only_ids` restricts which centers
    are evaluated (neighbors are still looked up in the full universe)."""
    idx = lattice.index
    by_key: dict[tuple, dict] = {_key(c, lattice, idx): c for c in configs}
    out: dict[str, NeighborhoodStats] = {}
    for c in configs:
        if only_ids is not None and c["config_id"] not in only_ids:
            continue
        keys, boundary = _neighbor_keys(c, include_joint=include_joint, lat=lattice, idx=idx)
        neigh = [by_key[k] for k in keys if k in by_key]
        if not neigh:
            out[c["config_id"]] = NeighborhoodStats(0, len(keys), None, None, 0, boundary)
            continue
        profitable = sum(1 for d in neigh if (d.get(net_return_key) or 0) > 0)
        sharpes = [d.get(sharpe_key) for d in neigh if d.get(sharpe_key) is not None]
        out[c["config_id"]] = NeighborhoodStats(
            n_neighbors=len(neigh),
            n_possible=len(keys),
            frac_profitable=profitable / len(neigh),
            median_sharpe=float(np.median(sharpes)) if sharpes else None,
            n_sharpe_undefined=len(neigh) - len(sharpes),
            boundary_axes=boundary,
        )
    return out
