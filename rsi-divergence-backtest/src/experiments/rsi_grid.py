"""Full-factorial grid for the RSI-divergence strategy: 32,768 variants per
timeframe x 3 timeframes = 98,304 variants per symbol."""

from __future__ import annotations

import itertools
from dataclasses import dataclass

from src.strategies.rsi_divergence.config import (
    MAX_HOLDS,
    MAX_PIVOT_GAPS,
    MIN_RSI_DIFFS,
    PIVOT_LEFTS,
    PIVOT_RIGHTS,
    RSI_LOOKBACKS,
    STOP_ATRS,
    TARGET_RS,
    TIMEFRAMES,
    RSIDivergenceConfig,
)
from src.utils.hashing import config_id as compute_config_id

# Axis name -> values, in one place (grid size / report both derive from this).
AXES: dict[str, tuple] = {
    "timeframe": TIMEFRAMES,
    "rsi_lookback": RSI_LOOKBACKS,
    "pivot_left": PIVOT_LEFTS,
    "pivot_right": PIVOT_RIGHTS,
    "max_pivot_gap": MAX_PIVOT_GAPS,
    "min_rsi_diff": MIN_RSI_DIFFS,
    "stop_atr": STOP_ATRS,
    "target_r": TARGET_RS,
    "max_hold": MAX_HOLDS,
}


@dataclass(frozen=True)
class ConfigEntry:
    config: RSIDivergenceConfig
    config_id: str


def variants_per_symbol(axes: dict[str, tuple] = AXES) -> int:
    n = 1
    for v in axes.values():
        n *= len(v)
    return n


def rsi_grid(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    names = list(AXES.keys())
    out: list[ConfigEntry] = []
    seen: set[str] = set()
    for symbol in symbols:
        for combo in itertools.product(*(AXES[n] for n in names)):
            cfg = RSIDivergenceConfig(symbol=symbol, **dict(zip(names, combo)))
            cid = compute_config_id(cfg.model_dump(mode="json"))
            if cid in seen:
                continue
            seen.add(cid)
            out.append(ConfigEntry(config=cfg, config_id=cid))
    return out
