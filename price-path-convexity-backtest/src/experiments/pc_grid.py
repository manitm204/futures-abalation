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
