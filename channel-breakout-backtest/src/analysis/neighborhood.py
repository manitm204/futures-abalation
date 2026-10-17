"""Parameter-neighborhood stability.

A robust configuration should be surrounded by configurations that also work: a
lone profitable island in a sea of losers is almost always overfit. For each
config we look at its IMMEDIATE neighbors on the grid lattice -- one step along a
single ordered axis (optionally also joint one-step moves on two axes) --
holding the categorical axes (trend_filter, symbol) fixed, and measure the
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
# init_stop: "off" means no fixed stop, i.e. an infinitely wide one, so it sits
# AFTER the widest numeric stop (3 ATR), not before the tightest.
ORDERED_AXES: dict[str, list] = {
    "timeframe": ["5min", "15min", "1h"],
    "entry_lookback": [10, 15, 20, 30, 40, 55, 80, 120],
    "exit_ratio": [0.25, 0.50, 0.75, 1.00],
    "buffer_atr": [0.0, 0.10, 0.25, 0.50],
    "init_stop": ["1.5", "2", "3", "off"],
    "confirm": [1, 2],
}
FIXED_AXES = ["symbol", "trend_filter"]
_INDEX = {ax: {v: i for i, v in enumerate(vals)} for ax, vals in ORDERED_AXES.items()}
MAX_SINGLE_AXIS_NEIGHBORS = 2 * len(ORDERED_AXES)


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


def _key(cfg: dict) -> tuple:
    return (
        tuple(cfg[a] for a in FIXED_AXES)
        + tuple(_INDEX[ax][cfg[ax]] for ax in ORDERED_AXES)
    )


def _neighbor_keys(cfg: dict, *, include_joint: bool) -> tuple[list[tuple], list[str]]:
    fixed = tuple(cfg[a] for a in FIXED_AXES)
    base = [_INDEX[ax][cfg[ax]] for ax in ORDERED_AXES]
    axes = list(ORDERED_AXES)
    sizes = [len(ORDERED_AXES[a]) for a in axes]
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


def neighbor_ids(configs: list[dict], *, include_joint: bool = False) -> dict[str, list[str]]:
    """config_id -> ids of its valid immediate neighbors in `configs`."""
    by_key = {_key(c): c["config_id"] for c in configs}
    out = {}
    for c in configs:
        keys, _ = _neighbor_keys(c, include_joint=include_joint)
        out[c["config_id"]] = [by_key[k] for k in keys if k in by_key]
    return out


def neighborhood_stats(
    configs: list[dict],
    *,
    net_return_key: str,
    sharpe_key: str,
    include_joint: bool = False,
    only_ids: set[str] | None = None,
) -> dict[str, NeighborhoodStats]:
    """Map config_id -> NeighborhoodStats. Each input dict needs the axis fields,
    `config_id`, and the chosen development net-return / Sharpe metric values.
    `configs` should be the full universe; `only_ids` restricts which centers
    are evaluated (neighbors are still looked up in the full universe)."""
    by_key: dict[tuple, dict] = {_key(c): c for c in configs}
    out: dict[str, NeighborhoodStats] = {}
    for c in configs:
        if only_ids is not None and c["config_id"] not in only_ids:
            continue
        keys, boundary = _neighbor_keys(c, include_joint=include_joint)
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
