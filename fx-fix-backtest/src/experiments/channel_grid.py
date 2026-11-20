"""Full-factorial grid for the channel-breakout strategy."""

from __future__ import annotations

import itertools
from dataclasses import dataclass

from src.strategies.channel_breakout.config import (
    BUFFER_ATRS,
    CONFIRMS,
    ENTRY_LOOKBACKS,
    EXIT_RATIOS,
    INIT_STOPS,
    TREND_FILTERS,
    ChannelBreakoutConfig,
)
from src.utils.hashing import config_id as compute_config_id

# Axis name -> values, in one place (grid size / report both derive from this).
AXES: dict[str, tuple] = {
    "timeframe": ("5min", "15min", "1h"),
    "entry_lookback": ENTRY_LOOKBACKS,
    "exit_ratio": EXIT_RATIOS,
    "buffer_atr": BUFFER_ATRS,
    "init_stop": INIT_STOPS,
    "confirm": CONFIRMS,
    "trend_filter": TREND_FILTERS,
}


@dataclass(frozen=True)
class ConfigEntry:
    config: ChannelBreakoutConfig
    config_id: str


def variants_per_symbol() -> int:
    n = 1
    for v in AXES.values():
        n *= len(v)
    return n


def channel_grid(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    names = list(AXES.keys())
    out: list[ConfigEntry] = []
    seen: set[str] = set()
    for symbol in symbols:
        for combo in itertools.product(*(AXES[n] for n in names)):
            params = dict(zip(names, combo))
            cfg = ChannelBreakoutConfig(symbol=symbol, **params)
            cid = compute_config_id(cfg.model_dump(mode="json"))
            if cid in seen:
                continue
            seen.add(cid)
            out.append(ConfigEntry(config=cfg, config_id=cid))
    return out
