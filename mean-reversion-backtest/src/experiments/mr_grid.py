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
    V3_ENTRY_CONFIRMATIONS,
    V3_ENTRY_ZS,
    V3_EXIT_ZS,
    V3_MAX_HOLDS,
    V3_MEAN_LOOKBACKS,
    V3_STD_LOOKBACKS,
    V3_STOP_ATRS,
    MeanReversionConfig,
    MeanReversionV2Config,
    MeanReversionV3Config,
    MeanReversionV5Config,
    MeanReversionV6Config,
    MeanReversionV7Config,
    MeanReversionV8Config,
    MeanReversionV9Config,
    MeanReversionV11Config,
    MeanReversionV12Config,
    MeanReversionV13Config,
    MeanReversionV14Config,
    MeanReversionV15Config,
    MeanReversionV16Config,
    MeanReversionV17Config,
    MeanReversionV21Config,
    V11_ENTRY_CONFIRMATIONS,
    V11_ENTRY_ZS,
    V11_EXIT_ZS,
    V11_MAX_HOLDS,
    V11_MEAN_LOOKBACKS,
    V11_STD_LOOKBACKS,
    V11_STOP_ATRS,
    V11_TIMEFRAMES,
    V11_MEAN_TYPES,
    V12_TIMEFRAMES,
    V12_MEAN_TYPES,
    V12_MEAN_LOOKBACKS,
    V12_STD_LOOKBACKS,
    V12_ENTRY_ZS,
    V12_EXIT_ZS,
    V12_MAX_HOLDS,
    V12_ENTRY_CONFIRMATIONS,
    V12_STOP_ATRS,
    V13_TIMEFRAMES,
    V13_MEAN_TYPES,
    V13_MEAN_LOOKBACKS,
    V13_STD_LOOKBACKS,
    V13_ENTRY_ZS,
    V13_EXIT_ZS,
    V13_MAX_HOLDS,
    V13_ENTRY_CONFIRMATIONS,
    V13_STOP_ATRS,
    V14_TIMEFRAMES,
    V14_MEAN_TYPES,
    V14_MEAN_LOOKBACKS,
    V14_STD_LOOKBACKS,
    V14_ENTRY_ZS,
    V14_EXIT_ZS,
    V14_MAX_HOLDS,
    V14_ENTRY_CONFIRMATIONS,
    V14_STOP_ATRS,
    V15_TIMEFRAMES,
    V15_MEAN_TYPES,
    V15_MEAN_LOOKBACKS,
    V15_STD_LOOKBACKS,
    V15_ENTRY_ZS,
    V15_EXIT_ZS,
    V15_MAX_HOLDS,
    V15_ENTRY_CONFIRMATIONS,
    V15_STOP_ATRS,
    V16_TIMEFRAMES,
    V16_MEAN_TYPES,
    V16_MEAN_LOOKBACKS,
    V16_STD_LOOKBACKS,
    V16_ENTRY_ZS,
    V16_EXIT_ZS,
    V16_MAX_HOLDS,
    V16_ENTRY_CONFIRMATIONS,
    V16_STOP_ATRS,
    V17_TIMEFRAMES,
    V17_MEAN_TYPES,
    V17_MEAN_LOOKBACKS,
    V17_STD_LOOKBACKS,
    V17_ENTRY_ZS,
    V17_EXIT_ZS,
    V17_MAX_HOLDS,
    V17_ENTRY_CONFIRMATIONS,
    V17_STOP_ATRS,
    V21_TIMEFRAMES,
    V21_MEAN_TYPES,
    V21_MEAN_LOOKBACKS,
    V21_STD_LOOKBACKS,
    V21_ENTRY_ZS,
    V21_EXIT_ZS,
    V21_MAX_HOLDS,
    V21_ENTRY_CONFIRMATIONS,
    V21_STOP_ATRS,
    MeanReversionV10Config,
    V10_ENTRY_CONFIRMATIONS,
    V10_ENTRY_ZS,
    V10_EXIT_ZS,
    V10_MAX_HOLDS,
    V10_MEAN_LOOKBACKS,
    V10_STD_LOOKBACKS,
    V10_STOP_ATRS,
    V10_TIMEFRAMES,
    V9_ENTRY_CONFIRMATIONS,
    V9_ENTRY_ZS,
    V9_EXIT_ZS,
    V9_MAX_HOLDS,
    V9_MEAN_LOOKBACKS,
    V9_STD_LOOKBACKS,
    V9_STOP_ATRS,
    V9_TIMEFRAMES,
    V8_ENTRY_CONFIRMATIONS,
    V8_ENTRY_ZS,
    V8_EXIT_ZS,
    V8_MAX_HOLDS,
    V8_MEAN_LOOKBACKS,
    V8_STD_LOOKBACKS,
    V8_STOP_ATRS,
    V8_TIMEFRAMES,
    V7_ENTRY_CONFIRMATIONS,
    V7_ENTRY_ZS,
    V7_EXIT_ZS,
    V7_MAX_HOLDS,
    V7_MEAN_LOOKBACKS,
    V7_STD_LOOKBACKS,
    V7_STOP_ATRS,
    V7_TIMEFRAMES,
    V6_ENTRY_CONFIRMATIONS,
    V6_ENTRY_ZS,
    V6_EXIT_ZS,
    V6_MAX_HOLDS,
    V6_MEAN_LOOKBACKS,
    V6_STD_LOOKBACKS,
    V6_STOP_ATRS,
    V5_ENTRY_CONFIRMATIONS,
    V5_ENTRY_ZS,
    V5_EXIT_ZS,
    V5_MAX_HOLDS,
    V5_MEAN_LOOKBACKS,
    V5_STD_LOOKBACKS,
    V5_STOP_ATRS,
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


AXES_V3: dict[str, tuple] = {
    "timeframe": TIMEFRAMES,
    "mean_type": MEAN_TYPES,
    "mean_lookback": V3_MEAN_LOOKBACKS,
    "std_lookback": V3_STD_LOOKBACKS,
    "entry_z": V3_ENTRY_ZS,
    "exit_z": V3_EXIT_ZS,
    "max_holding_bars": V3_MAX_HOLDS,
    "entry_confirmation": V3_ENTRY_CONFIRMATIONS,
    "stop_atr_multiple": V3_STOP_ATRS,
}


AXES_V5: dict[str, tuple] = {
    "timeframe": TIMEFRAMES,
    "mean_type": MEAN_TYPES,
    "mean_lookback": V5_MEAN_LOOKBACKS,
    "std_lookback": V5_STD_LOOKBACKS,
    "entry_z": V5_ENTRY_ZS,
    "exit_z": V5_EXIT_ZS,
    "max_holding_bars": V5_MAX_HOLDS,
    "entry_confirmation": V5_ENTRY_CONFIRMATIONS,
    "stop_atr_multiple": V5_STOP_ATRS,
}


AXES_V6: dict[str, tuple] = {
    "timeframe": TIMEFRAMES,
    "mean_type": MEAN_TYPES,
    "mean_lookback": V6_MEAN_LOOKBACKS,
    "std_lookback": V6_STD_LOOKBACKS,
    "entry_z": V6_ENTRY_ZS,
    "exit_z": V6_EXIT_ZS,
    "max_holding_bars": V6_MAX_HOLDS,
    "entry_confirmation": V6_ENTRY_CONFIRMATIONS,
    "stop_atr_multiple": V6_STOP_ATRS,
}


AXES_V7: dict[str, tuple] = {
    "timeframe": V7_TIMEFRAMES,
    "mean_type": MEAN_TYPES,
    "mean_lookback": V7_MEAN_LOOKBACKS,
    "std_lookback": V7_STD_LOOKBACKS,
    "entry_z": V7_ENTRY_ZS,
    "exit_z": V7_EXIT_ZS,
    "max_holding_bars": V7_MAX_HOLDS,
    "entry_confirmation": V7_ENTRY_CONFIRMATIONS,
    "stop_atr_multiple": V7_STOP_ATRS,
}


AXES_V8: dict[str, tuple] = {
    "timeframe": V8_TIMEFRAMES,
    "mean_type": MEAN_TYPES,
    "mean_lookback": V8_MEAN_LOOKBACKS,
    "std_lookback": V8_STD_LOOKBACKS,
    "entry_z": V8_ENTRY_ZS,
    "exit_z": V8_EXIT_ZS,
    "max_holding_bars": V8_MAX_HOLDS,
    "entry_confirmation": V8_ENTRY_CONFIRMATIONS,
    "stop_atr_multiple": V8_STOP_ATRS,
}


AXES_V9: dict[str, tuple] = {
    "timeframe": V9_TIMEFRAMES,
    "mean_type": MEAN_TYPES,
    "mean_lookback": V9_MEAN_LOOKBACKS,
    "std_lookback": V9_STD_LOOKBACKS,
    "entry_z": V9_ENTRY_ZS,
    "exit_z": V9_EXIT_ZS,
    "max_holding_bars": V9_MAX_HOLDS,
    "entry_confirmation": V9_ENTRY_CONFIRMATIONS,
    "stop_atr_multiple": V9_STOP_ATRS,
}


AXES_V10: dict[str, tuple] = {
    "timeframe": V10_TIMEFRAMES,
    "mean_type": MEAN_TYPES,
    "mean_lookback": V10_MEAN_LOOKBACKS,
    "std_lookback": V10_STD_LOOKBACKS,
    "entry_z": V10_ENTRY_ZS,
    "exit_z": V10_EXIT_ZS,
    "max_holding_bars": V10_MAX_HOLDS,
    "entry_confirmation": V10_ENTRY_CONFIRMATIONS,
    "stop_atr_multiple": V10_STOP_ATRS,
}


AXES_V11: dict[str, tuple] = {
    "timeframe": V11_TIMEFRAMES,
    "mean_type": V11_MEAN_TYPES,
    "mean_lookback": V11_MEAN_LOOKBACKS,
    "std_lookback": V11_STD_LOOKBACKS,
    "entry_z": V11_ENTRY_ZS,
    "exit_z": V11_EXIT_ZS,
    "max_holding_bars": V11_MAX_HOLDS,
    "entry_confirmation": V11_ENTRY_CONFIRMATIONS,
    "stop_atr_multiple": V11_STOP_ATRS,
}


@dataclass(frozen=True)
class ConfigEntry:
    config: MeanReversionConfig | MeanReversionV2Config | MeanReversionV3Config
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


def mr_grid_v3(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V3, MeanReversionV3Config)


def mr_grid_v5(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V5, MeanReversionV5Config)


def mr_grid_v6(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V6, MeanReversionV6Config)


def mr_grid_v7(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V7, MeanReversionV7Config)


def mr_grid_v8(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V8, MeanReversionV8Config)


def mr_grid_v9(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V9, MeanReversionV9Config)


AXES_V12: dict[str, tuple] = {
    "timeframe": V12_TIMEFRAMES,
    "mean_type": V12_MEAN_TYPES,
    "mean_lookback": V12_MEAN_LOOKBACKS,
    "std_lookback": V12_STD_LOOKBACKS,
    "entry_z": V12_ENTRY_ZS,
    "exit_z": V12_EXIT_ZS,
    "max_holding_bars": V12_MAX_HOLDS,
    "entry_confirmation": V12_ENTRY_CONFIRMATIONS,
    "stop_atr_multiple": V12_STOP_ATRS,
}


AXES_V13: dict[str, tuple] = {
    "timeframe": V13_TIMEFRAMES,
    "mean_type": V13_MEAN_TYPES,
    "mean_lookback": V13_MEAN_LOOKBACKS,
    "std_lookback": V13_STD_LOOKBACKS,
    "entry_z": V13_ENTRY_ZS,
    "exit_z": V13_EXIT_ZS,
    "max_holding_bars": V13_MAX_HOLDS,
    "entry_confirmation": V13_ENTRY_CONFIRMATIONS,
    "stop_atr_multiple": V13_STOP_ATRS,
}


def mr_grid_v10(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V10, MeanReversionV10Config)


def mr_grid_v11(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V11, MeanReversionV11Config)


def mr_grid_v12(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V12, MeanReversionV12Config)


def mr_grid_v13(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V13, MeanReversionV13Config)


AXES_V14: dict[str, tuple] = {
    "timeframe": V14_TIMEFRAMES,
    "mean_type": V14_MEAN_TYPES,
    "mean_lookback": V14_MEAN_LOOKBACKS,
    "std_lookback": V14_STD_LOOKBACKS,
    "entry_z": V14_ENTRY_ZS,
    "exit_z": V14_EXIT_ZS,
    "max_holding_bars": V14_MAX_HOLDS,
    "entry_confirmation": V14_ENTRY_CONFIRMATIONS,
    "stop_atr_multiple": V14_STOP_ATRS,
}


AXES_V15: dict[str, tuple] = {
    "timeframe": V15_TIMEFRAMES,
    "mean_type": V15_MEAN_TYPES,
    "mean_lookback": V15_MEAN_LOOKBACKS,
    "std_lookback": V15_STD_LOOKBACKS,
    "entry_z": V15_ENTRY_ZS,
    "exit_z": V15_EXIT_ZS,
    "max_holding_bars": V15_MAX_HOLDS,
    "entry_confirmation": V15_ENTRY_CONFIRMATIONS,
    "stop_atr_multiple": V15_STOP_ATRS,
}


def mr_grid_v14(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V14, MeanReversionV14Config)


def mr_grid_v15(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V15, MeanReversionV15Config)


AXES_V16: dict[str, tuple] = {
    "timeframe": V16_TIMEFRAMES,
    "mean_type": V16_MEAN_TYPES,
    "mean_lookback": V16_MEAN_LOOKBACKS,
    "std_lookback": V16_STD_LOOKBACKS,
    "entry_z": V16_ENTRY_ZS,
    "exit_z": V16_EXIT_ZS,
    "max_holding_bars": V16_MAX_HOLDS,
    "entry_confirmation": V16_ENTRY_CONFIRMATIONS,
    "stop_atr_multiple": V16_STOP_ATRS,
}


AXES_V17: dict[str, tuple] = {
    "timeframe": V17_TIMEFRAMES,
    "mean_type": V17_MEAN_TYPES,
    "mean_lookback": V17_MEAN_LOOKBACKS,
    "std_lookback": V17_STD_LOOKBACKS,
    "entry_z": V17_ENTRY_ZS,
    "exit_z": V17_EXIT_ZS,
    "max_holding_bars": V17_MAX_HOLDS,
    "entry_confirmation": V17_ENTRY_CONFIRMATIONS,
    "stop_atr_multiple": V17_STOP_ATRS,
}


def mr_grid_v16(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V16, MeanReversionV16Config)


def mr_grid_v17(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V17, MeanReversionV17Config)


AXES_V21: dict[str, tuple] = {
    "timeframe": V21_TIMEFRAMES,
    "mean_type": V21_MEAN_TYPES,
    "mean_lookback": V21_MEAN_LOOKBACKS,
    "std_lookback": V21_STD_LOOKBACKS,
    "entry_z": V21_ENTRY_ZS,
    "exit_z": V21_EXIT_ZS,
    "max_holding_bars": V21_MAX_HOLDS,
    "entry_confirmation": V21_ENTRY_CONFIRMATIONS,
    "stop_atr_multiple": V21_STOP_ATRS,
}


def mr_grid_v21(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V21, MeanReversionV21Config)


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
