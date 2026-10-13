"""Parameter-neighborhood stability.

A robust configuration should be surrounded by configurations that also work: a
lone profitable island in a sea of losers is almost always overfit. For each
config we look at its neighbors on the grid lattice -- one step along a single
ordered axis, and (optionally) joint one-step moves along two axes at once --
holding the categorical axes (trend_filter, symbol) fixed, and measure the
fraction of profitable neighbors and the median neighbor Sharpe.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

import numpy as np

# Ordered axes (value order matters for "adjacent"); categorical axes are held fixed.
ORDERED_AXES: dict[str, list] = {
    "timeframe": ["5min", "15min", "1h"],
    "entry_lookback": [10, 15, 20, 30, 40, 55, 80, 120],
    "exit_ratio": [0.25, 0.50, 0.75, 1.00],
    "buffer_atr": [0.0, 0.10, 0.25, 0.50],
    "init_stop": ["off", "1.5", "2", "3"],
    "confirm": [1, 2],
}
FIXED_AXES = ["symbol", "trend_filter"]
_INDEX = {ax: {v: i for i, v in enumerate(vals)} for ax, vals in ORDERED_AXES.items()}


@dataclass(frozen=True)
class NeighborhoodStats:
    n_neighbors: int
    frac_profitable: float
    median_sharpe: float


def _key(cfg: dict) -> tuple:
    return (
        tuple(cfg[a] for a in FIXED_AXES)
        + tuple(_INDEX[ax][cfg[ax]] for ax in ORDERED_AXES)
    )


def _neighbor_keys(cfg: dict, *, include_joint: bool) -> list[tuple]:
    fixed = tuple(cfg[a] for a in FIXED_AXES)
    base = [_INDEX[ax][cfg[ax]] for ax in ORDERED_AXES]
    axes = list(ORDERED_AXES)
    sizes = [len(ORDERED_AXES[a]) for a in axes]
    out: list[tuple] = []

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
    return out


def neighborhood_stats(
    configs: list[dict],
    *,
    net_return_key: str,
    sharpe_key: str,
    include_joint: bool = True,
) -> dict[str, NeighborhoodStats]:
    """Map config_id -> NeighborhoodStats. Each input dict needs the axis fields,
    `config_id`, and the chosen development net-return / Sharpe metric values."""
    by_key: dict[tuple, dict] = {_key(c): c for c in configs}
    out: dict[str, NeighborhoodStats] = {}
    for c in configs:
        neigh = [by_key[k] for k in _neighbor_keys(c, include_joint=include_joint) if k in by_key]
        if not neigh:
            out[c["config_id"]] = NeighborhoodStats(0, 0.0, float("nan"))
            continue
        profitable = sum(1 for d in neigh if (d.get(net_return_key) or 0) > 0)
        sharpes = [d.get(sharpe_key) for d in neigh if d.get(sharpe_key) is not None]
        out[c["config_id"]] = NeighborhoodStats(
            n_neighbors=len(neigh),
            frac_profitable=profitable / len(neigh),
            median_sharpe=float(np.median(sharpes)) if sharpes else float("nan"),
        )
    return out
