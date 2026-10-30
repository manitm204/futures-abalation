"""Full-factorial grid of DonchianBreakoutConfig variants -- the ablation space.

Unlike src/experiments/sampler.py (random/Sobol sampling of a mostly-continuous
ICT space), the Donchian study enumerates EVERY combination of a small set of
discrete axes. That is the whole point of an ablation: each variant differs from
others by known, interpretable settings, so the report can attribute performance
to specific choices rather than to an opaque point in a continuous space.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

from src.strategies.donchian_breakout.config import DonchianBreakoutConfig
from src.utils.hashing import config_id as compute_config_id

# The ablation axes, in one place so the grid size is trivially tunable.
AXES: dict[str, tuple] = {
    "timeframe": ("15min", "1h"),
    "channel_lookback": (20, 40, 60),
    "breakout_price": ("close", "wick", "typical"),
    "trend_filter": ("none", "sma50", "sma200"),
    "direction": ("both", "long_only"),
    "stop": ("atr_1.5", "atr_2.5", "channel_mid"),
    "target": ("r_1.5", "r_3.0", "none"),
    "time_exit": ("eod", "max_120min"),
}


@dataclass(frozen=True)
class GridConfig:
    config: DonchianBreakoutConfig
    config_id: str


def variants_per_symbol() -> int:
    n = 1
    for values in AXES.values():
        n *= len(values)
    return n


def donchian_grid(symbols: tuple[str, ...]) -> list[GridConfig]:
    """Every (symbol x axis-combination) variant. config_id is derived from the
    full config (including symbol/timeframe), so ids are globally unique and the
    run is resumable/deduplicated exactly like the ICT search."""
    names = list(AXES.keys())
    out: list[GridConfig] = []
    seen: set[str] = set()
    for symbol in symbols:
        for combo in itertools.product(*(AXES[n] for n in names)):
            params = dict(zip(names, combo))
            cfg = DonchianBreakoutConfig(symbol=symbol, **params)
            cid = compute_config_id(cfg.model_dump(mode="json"))
            if cid in seen:
                continue
            seen.add(cid)
            out.append(GridConfig(config=cfg, config_id=cid))
    return out
