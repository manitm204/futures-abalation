"""Full-factorial grids for the price-path convexity line.

  path_convexity_v1_15m : 186,624 configs (15-minute bars)
  path_convexity_v1_5m  : 186,624 configs (5-minute bars; same values, lookbacks in 5m bars)

Later rounds add an AXES_PC_V<n> dict, a config class in src/strategies/path_convexity/config.py,
a lattice in src/analysis/neighborhood.py and an entry in scripts/run_pc_funnel.py SPACES.
"""

from __future__ import annotations

from src.experiments.mr_grid import ConfigEntry, _grid, variants_per_symbol  # noqa: F401  (re-export)
from src.strategies.path_convexity.config import (
    V1_DIRECTIONS,
    V1_ENTRY_ZS,
    V1_HOLDS,
    V1_LOOKBACKS,
    V1_MIN_MOVE_ATRS,
    V1_QUADRANTS,
    V1_SIGNAL_FORMS,
    V1_STOPS,
    V1_TREND_FILTERS,
    V1_Z_LOOKBACKS,
    ConvexityV1_5mConfig,
    ConvexityV1_15mConfig,
)

_AXES_PC_V1: dict[str, tuple] = {
    "lookback": V1_LOOKBACKS,
    "signal_form": V1_SIGNAL_FORMS,
    "z_lookback": V1_Z_LOOKBACKS,
    "entry_z": V1_ENTRY_ZS,
    "quadrant": V1_QUADRANTS,
    "min_move_atr": V1_MIN_MOVE_ATRS,
    "direction": V1_DIRECTIONS,
    "hold": V1_HOLDS,
    "stop": V1_STOPS,
    "trend_filter": V1_TREND_FILTERS,
}
AXES_PC_V1_15M: dict[str, tuple] = {"timeframe": ("15min",), **_AXES_PC_V1}
AXES_PC_V1_5M: dict[str, tuple] = {"timeframe": ("5min",), **_AXES_PC_V1}


def pc_grid_v1_15m(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_PC_V1_15M, ConvexityV1_15mConfig)


def pc_grid_v1_5m(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_PC_V1_5M, ConvexityV1_5mConfig)


# --- v2: 15-minute bars, 82,944 configs -----------------------------------------------------
from src.strategies.path_convexity.config import (  # noqa: E402
    V2_DIRECTIONS,
    V2_ENTRY_ZS,
    V2_HOLDS,
    V2_LOOKBACKS,
    V2_MIN_MOVE_ATRS,
    V2_QUADRANTS,
    V2_SIGNAL_FORMS,
    V2_STOPS,
    V2_TREND_FILTERS,
    V2_Z_LOOKBACKS,
    ConvexityV2_15mConfig,
)

AXES_PC_V2_15M: dict[str, tuple] = {
    "timeframe": ("15min",),
    "lookback": V2_LOOKBACKS,
    "signal_form": V2_SIGNAL_FORMS,
    "z_lookback": V2_Z_LOOKBACKS,
    "entry_z": V2_ENTRY_ZS,
    "quadrant": V2_QUADRANTS,
    "min_move_atr": V2_MIN_MOVE_ATRS,
    "direction": V2_DIRECTIONS,
    "hold": V2_HOLDS,
    "stop": V2_STOPS,
    "trend_filter": V2_TREND_FILTERS,
}


def pc_grid_v2_15m(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_PC_V2_15M, ConvexityV2_15mConfig)


# --- v3: 15-minute bars, 103,680 configs (run on NQ) -----------------------------------------
from src.strategies.path_convexity.config import (  # noqa: E402
    V3_DIRECTIONS,
    V3_ENTRY_ZS,
    V3_HOLDS,
    V3_LOOKBACKS,
    V3_MIN_MOVE_ATRS,
    V3_QUADRANTS,
    V3_SIGNAL_FORMS,
    V3_STOPS,
    V3_TREND_FILTERS,
    V3_Z_LOOKBACKS,
    ConvexityV3_15mConfig,
)

AXES_PC_V3_15M: dict[str, tuple] = {
    "timeframe": ("15min",),
    "lookback": V3_LOOKBACKS,
    "signal_form": V3_SIGNAL_FORMS,
    "z_lookback": V3_Z_LOOKBACKS,
    "entry_z": V3_ENTRY_ZS,
    "quadrant": V3_QUADRANTS,
    "min_move_atr": V3_MIN_MOVE_ATRS,
    "direction": V3_DIRECTIONS,
    "hold": V3_HOLDS,
    "stop": V3_STOPS,
    "trend_filter": V3_TREND_FILTERS,
}


def pc_grid_v3_15m(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_PC_V3_15M, ConvexityV3_15mConfig)


# --- v4: 15-minute bars, 10,368 configs (light grid; run on CL) -------------------------------
from src.strategies.path_convexity.config import (  # noqa: E402
    V4_DIRECTIONS,
    V4_ENTRY_ZS,
    V4_HOLDS,
    V4_LOOKBACKS,
    V4_MIN_MOVE_ATRS,
    V4_QUADRANTS,
    V4_SIGNAL_FORMS,
    V4_STOPS,
    V4_TREND_FILTERS,
    V4_Z_LOOKBACKS,
    ConvexityV4_15mConfig,
)

AXES_PC_V4_15M: dict[str, tuple] = {
    "timeframe": ("15min",),
    "lookback": V4_LOOKBACKS,
    "signal_form": V4_SIGNAL_FORMS,
    "z_lookback": V4_Z_LOOKBACKS,
    "entry_z": V4_ENTRY_ZS,
    "quadrant": V4_QUADRANTS,
    "min_move_atr": V4_MIN_MOVE_ATRS,
    "direction": V4_DIRECTIONS,
    "hold": V4_HOLDS,
    "stop": V4_STOPS,
    "trend_filter": V4_TREND_FILTERS,
}


def pc_grid_v4_15m(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_PC_V4_15M, ConvexityV4_15mConfig)
