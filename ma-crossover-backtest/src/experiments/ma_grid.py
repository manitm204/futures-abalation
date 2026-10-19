"""Full-factorial grids for the moving-average crossover strategy.
v1: 20,000 variants per timeframe x 3 timeframes = 60,000 per symbol.
v2: 124,416 variants per timeframe x 2 timeframes = 248,832 per symbol."""

from __future__ import annotations

import itertools
from dataclasses import dataclass

from src.strategies.ma_crossover import config as C
from src.strategies.ma_crossover.config import MACrossoverConfig, MACrossoverV2Config
from src.utils.hashing import config_id as compute_config_id

# Axis name -> values, in one place (grid size / report both derive from this).
AXES: dict[str, tuple] = {
    "timeframe": C.TIMEFRAMES,
    "ma_pair": C.MA_PAIRS,
    "fast_length": C.FAST_LENGTHS,
    "slow_length": C.SLOW_LENGTHS,
    "confirm_bars": C.CONFIRM_BARS,
    "buffer_atr": C.BUFFER_ATRS,
    "stop_atr": C.STOP_ATRS,
    "slope_filter": C.SLOPE_FILTERS,
}

AXES_V2: dict[str, tuple] = {
    "timeframe": C.TIMEFRAMES_V2,
    "ma_pair": C.MA_PAIRS_V2,
    "fast_length": C.FAST_LENGTHS_V2,
    "slow_length": C.SLOW_LENGTHS_V2,
    "confirm_bars": C.CONFIRM_BARS_V2,
    "buffer_atr": C.BUFFER_ATRS_V2,
    "stop_atr": C.STOP_ATRS_V2,
    "slope_filter": C.SLOPE_FILTERS_V2,
    "max_hold": C.MAX_HOLDS_V2,
    "take_profit_atr": C.TAKE_PROFIT_ATRS_V2,
    "cooldown_bars": C.COOLDOWN_BARS_V2,
    "min_adx": C.MIN_ADXS_V2,
    "max_extension_atr": C.MAX_EXTENSION_ATRS_V2,
}


@dataclass(frozen=True)
class ConfigEntry:
    config: MACrossoverConfig | MACrossoverV2Config
    config_id: str


def variants_per_symbol(axes: dict[str, tuple] = AXES) -> int:
    n = 1
    for v in axes.values():
        n *= len(v)
    return n


def ma_grid(symbols: tuple[str, ...], *, axes: dict[str, tuple] = AXES, cls=MACrossoverConfig) -> list[ConfigEntry]:
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


def ma_grid_v2(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return ma_grid(symbols, axes=AXES_V2, cls=MACrossoverV2Config)
