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
    NoiseBandConfig,
    NoiseBandV2Config,
    NoiseBandV3Config,
    NoiseBandV4Config,
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
