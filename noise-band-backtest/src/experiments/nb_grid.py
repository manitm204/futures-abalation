"""Full-factorial grids for the noise-band breakout strategy: v1 and v2 (8,100 variants per symbol each).

Later rounds (narrowed or market-specific grids, like the mean-reversion v5..v21) add
an AXES_V<n> dict, a NoiseBandV<n>Config in src/strategies/noise_band/config.py, a
lattice in src/analysis/neighborhood.py and an entry in scripts/run_nb_funnel.py SPACES.
"""

from __future__ import annotations

from src.experiments.mr_grid import ConfigEntry, _grid, variants_per_symbol  # noqa: F401  (re-export)
from src.strategies.noise_band.config import (
    ANCHORS,
    BAND_LOOKBACKS,
    BAND_MULTS,
    CHECK_MINUTES,
    DIRECTIONS,
    FIRST_ENTRY_MINUTES,
    STOP_ATRS,
    TIMEFRAMES,
    TRAILS,
    V2_BAND_LOOKBACKS,
    V2_BAND_MULTS,
    V2_TIMEFRAMES,
    V3_TIMEFRAMES,
    V4_BAND_LOOKBACKS,
    V4_BAND_MULTS,
    V4_DIRECTIONS,
    V4_FIRST_ENTRY_MINUTES,
    V4_MAX_ENTRIES,
    V4_TRAILS,
    V5_BAND_LOOKBACKS,
    V5_BAND_MULTS,
    V5_LAST_ENTRY_CUTOFFS,
    V6_BAND_LOOKBACKS,
    V6_BAND_MULTS,
    V6_MOMENTUM_MINUTES,
    V7_BAND_LOOKBACKS,
    V7_MAX_EXTENSIONS,
    V7_MOMENTUM_MINUTES,
    V7_REL_VOLUMES,
    NoiseBandConfig,
    NoiseBandV2Config,
    NoiseBandV3Config,
    NoiseBandV4Config,
    NoiseBandV5Config,
    NoiseBandV6Config,
    NoiseBandV7Config,
)

AXES_V1: dict[str, tuple] = {
    "timeframe": TIMEFRAMES,
    "band_lookback": BAND_LOOKBACKS,
    "band_mult": BAND_MULTS,
    "check_minutes": CHECK_MINUTES,
    "first_entry_minutes": FIRST_ENTRY_MINUTES,
    "anchor": ANCHORS,
    "trail": TRAILS,
    "direction": DIRECTIONS,
    "stop_atr_multiple": STOP_ATRS,
}


def nb_grid(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V1, NoiseBandConfig)


AXES_V2: dict[str, tuple] = {**AXES_V1, "timeframe": V2_TIMEFRAMES, "band_lookback": V2_BAND_LOOKBACKS,
                             "band_mult": V2_BAND_MULTS}


def nb_grid_v2(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V2, NoiseBandV2Config)


AXES_V3: dict[str, tuple] = {**AXES_V2, "timeframe": V3_TIMEFRAMES}


def nb_grid_v3(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V3, NoiseBandV3Config)


AXES_V4: dict[str, tuple] = {
    "timeframe": TIMEFRAMES,
    "band_lookback": V4_BAND_LOOKBACKS,
    "band_mult": V4_BAND_MULTS,
    "check_minutes": CHECK_MINUTES,
    "first_entry_minutes": V4_FIRST_ENTRY_MINUTES,
    "anchor": ANCHORS,
    "trail": V4_TRAILS,
    "direction": V4_DIRECTIONS,
    "max_entries_per_session": V4_MAX_ENTRIES,
    "stop_atr_multiple": STOP_ATRS,
}


def nb_grid_v4(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V4, NoiseBandV4Config)


AXES_V5: dict[str, tuple] = {
    "timeframe": TIMEFRAMES,
    "band_lookback": V5_BAND_LOOKBACKS,
    "band_mult": V5_BAND_MULTS,
    "check_minutes": CHECK_MINUTES,
    "first_entry_minutes": FIRST_ENTRY_MINUTES,
    "anchor": ANCHORS,
    "trail": TRAILS,
    "direction": V4_DIRECTIONS,
    "max_entries_per_session": V4_MAX_ENTRIES,
    "last_entry_cutoff_minutes": V5_LAST_ENTRY_CUTOFFS,
    "stop_atr_multiple": STOP_ATRS,
}


def nb_grid_v5(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V5, NoiseBandV5Config)


AXES_V6: dict[str, tuple] = {
    "timeframe": ("15min",),
    "band_lookback": V6_BAND_LOOKBACKS,
    "band_mult": V6_BAND_MULTS,
    "check_minutes": (15,),
    "first_entry_minutes": (60,),
    "anchor": ("open_prev_close",),
    "trail": V4_TRAILS,
    "direction": V4_DIRECTIONS,
    "max_entries_per_session": V4_MAX_ENTRIES,
    "last_entry_cutoff_minutes": V5_LAST_ENTRY_CUTOFFS,
    "momentum_minutes": V6_MOMENTUM_MINUTES,
    "stop_atr_multiple": STOP_ATRS,
}


def nb_grid_v6(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V6, NoiseBandV6Config)


AXES_V7: dict[str, tuple] = {
    "timeframe": ("15min",),
    "band_lookback": V7_BAND_LOOKBACKS,
    "band_mult": V6_BAND_MULTS,
    "check_minutes": (15,),
    "first_entry_minutes": (60,),
    "anchor": ("open_prev_close",),
    "trail": ("vwap",),
    "direction": ("both",),
    "max_entries_per_session": ("none",),
    "last_entry_cutoff_minutes": (60,),
    "momentum_minutes": V7_MOMENTUM_MINUTES,
    "max_extension": V7_MAX_EXTENSIONS,
    "rel_volume": V7_REL_VOLUMES,
    "stop_atr_multiple": STOP_ATRS,
}


def nb_grid_v7(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_V7, NoiseBandV7Config)
