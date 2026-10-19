"""Full-factorial grids for the mean-reversion strategy: v1 (75,000 variants per
symbol) and v2 (240,000 variants per symbol)."""

from __future__ import annotations

import itertools
from dataclasses import dataclass

from src.strategies.mean_reversion.config import (
    ENTRY_ZS,
    EXIT_ZS,
    MAX_HOLDS,
    MEAN_LOOKBACKS,
    MEAN_TYPES,
    STD_LOOKBACKS,
    TIMEFRAMES,
    TREND_FILTERS,
    V2_COOLDOWNS,
    V2_ENTRY_CONFIRMATIONS,
    V2_EXIT_ZS,
    V2_MAX_HOLDS,
    V2_MEAN_LOOKBACKS,
    V2_STOP_ATRS,
    V2_TREND_FILTERS,
    MeanReversionConfig,
    MeanReversionV2Config,
)
from src.utils.hashing import config_id as compute_config_id

# Axis name -> values, in one place (grid size / report both derive from this).
AXES: dict[str, tuple] = {
    "timeframe": TIMEFRAMES,
    "mean_type": MEAN_TYPES,
    "mean_lookback": MEAN_LOOKBACKS,
    "std_lookback": STD_LOOKBACKS,
    "entry_z": ENTRY_ZS,
    "exit_z": EXIT_ZS,
    "max_hold": MAX_HOLDS,
    "trend_filter": TREND_FILTERS,
}


AXES_V2: dict[str, tuple] = {
    "timeframe": TIMEFRAMES,
    "mean_type": MEAN_TYPES,
    "mean_lookback": V2_MEAN_LOOKBACKS,
    "entry_z": ENTRY_ZS,
    "exit_z": V2_EXIT_ZS,
    "max_holding_bars": V2_MAX_HOLDS,
    "trend_filter": V2_TREND_FILTERS,
    "entry_confirmation": V2_ENTRY_CONFIRMATIONS,
    "cooldown_bars": V2_COOLDOWNS,
    "stop_atr_multiple": V2_STOP_ATRS,
}


@dataclass(frozen=True)
class ConfigEntry:
    config: MeanReversionConfig | MeanReversionV2Config
    config_id: str


def variants_per_symbol(axes: dict[str, tuple] = AXES) -> int:
    n = 1
    for v in axes.values():
        n *= len(v)
    return n


def mr_grid(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES, MeanReversionConfig)


def mr_grid_v2(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V2, MeanReversionV2Config)


def _grid(symbols: tuple[str, ...], axes: dict[str, tuple], cls) -> list[ConfigEntry]:
    names = list(axes.keys())
    out: list[ConfigEntry] = []
    seen: set[str] = set()
    for symbol in symbols:
        for combo in itertools.product(*(axes[n] for n in names)):
            cfg = cls(symbol=symbol, **dict(zip(names, combo)))
            cid = compute_config_id(cfg.model_dump(mode="json"))
            if cid in seen:
                continue
            seen.add(cid)
            out.append(ConfigEntry(config=cfg, config_id=cid))
    return out
