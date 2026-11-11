"""Full-factorial grids for the compression-breakout lines. Each compression type is its own
strategy line with its own rounds; they share the backtester and the SHARED axes.

  compression_breakout_bbkc v1 : 18 squeeze settings x 1,152 shared = 20,736 variants per symbol
  compression_breakout_nr   v1 : 14 NR settings      x 1,152 shared = 16,128 variants per symbol

Later rounds of a line add an AXES_<LINE>_V<n> dict, a config class in
src/strategies/compression_breakout/config.py, a lattice in src/analysis/neighborhood.py
and an entry in scripts/run_cb_funnel.py SPACES.
"""

from __future__ import annotations

from src.experiments.mr_grid import ConfigEntry, _grid, variants_per_symbol  # noqa: F401  (re-export)
from src.strategies.compression_breakout.config import (
    DIRECTIONS,
    ENTRY_TYPES,
    INSIDE_BARS,
    KC_MULTS,
    MIN_BOX_ATRS,
    MIN_SQUEEZE_BARS,
    NR_LOOKBACKS,
    SETUP_EXPIRIES,
    SQUEEZE_LENGTHS,
    STOPS,
    TARGETS,
    TIMEFRAMES,
    TREND_FILTERS,
    NRBreakoutConfig,
    SqueezeBreakoutConfig,
)

SHARED_AXES_V1: dict[str, tuple] = {
    "timeframe": TIMEFRAMES,
    "entry_type": ENTRY_TYPES,
    "setup_expiry_bars": SETUP_EXPIRIES,
    "stop": STOPS,
    "target_r": TARGETS,
    "direction": DIRECTIONS,
    "trend_filter": TREND_FILTERS,
    "min_box_atr": MIN_BOX_ATRS,
}

AXES_BBKC_V1: dict[str, tuple] = {
    "squeeze_length": SQUEEZE_LENGTHS,
    "kc_mult": KC_MULTS,
    "min_squeeze_bars": MIN_SQUEEZE_BARS,
    **SHARED_AXES_V1,
}

AXES_NR_V1: dict[str, tuple] = {
    "nr_lookback": NR_LOOKBACKS,
    "inside_bar": INSIDE_BARS,
    **SHARED_AXES_V1,
}


def cb_grid_bbkc(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_BBKC_V1, SqueezeBreakoutConfig)


def cb_grid_nr(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_NR_V1, NRBreakoutConfig)


# --- squeeze v2 (ES round 2): one grid per bar size, so two runs -----------------------------
from src.strategies.compression_breakout.config import (  # noqa: E402
    V2_5M_ENTRY_TYPES,
    V2_5M_KC_MULTS,
    V2_5M_MIN_BOX_ATRS,
    V2_5M_MIN_SQUEEZE_BARS,
    V2_5M_SETUP_EXPIRIES,
    V2_5M_SQUEEZE_LENGTHS,
    V2_5M_STOPS,
    V2_5M_TARGETS,
    V2_15M_KC_MULTS,
    V2_15M_MIN_BOX_ATRS,
    V2_15M_MIN_SQUEEZE_BARS,
    V2_15M_SQUEEZE_LENGTHS,
    V2_15M_STOPS,
    V2_15M_TARGETS,
    V2_DIRECTIONS,
    V2_SETUP_EXPIRIES,
    SqueezeBreakoutV2_5mConfig,
    SqueezeBreakoutV2_15mConfig,
)

AXES_BBKC_V2_5M: dict[str, tuple] = {
    "timeframe": ("5min",),
    "squeeze_length": V2_5M_SQUEEZE_LENGTHS,
    "kc_mult": V2_5M_KC_MULTS,
    "min_squeeze_bars": V2_5M_MIN_SQUEEZE_BARS,
    "entry_type": V2_5M_ENTRY_TYPES,
    "setup_expiry_bars": V2_5M_SETUP_EXPIRIES,
    "stop": V2_5M_STOPS,
    "target_r": V2_5M_TARGETS,
    "direction": V2_DIRECTIONS,
    "trend_filter": TREND_FILTERS,
    "min_box_atr": V2_5M_MIN_BOX_ATRS,
}

AXES_BBKC_V2_15M: dict[str, tuple] = {
    "timeframe": ("15min",),
    "squeeze_length": V2_15M_SQUEEZE_LENGTHS,
    "kc_mult": V2_15M_KC_MULTS,
    "min_squeeze_bars": V2_15M_MIN_SQUEEZE_BARS,
    "entry_type": ENTRY_TYPES,
    "setup_expiry_bars": V2_SETUP_EXPIRIES,
    "stop": V2_15M_STOPS,
    "target_r": V2_15M_TARGETS,
    "direction": V2_DIRECTIONS,
    "trend_filter": TREND_FILTERS,
    "min_box_atr": V2_15M_MIN_BOX_ATRS,
}


def cb_grid_bbkc_v2_5m(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_BBKC_V2_5M, SqueezeBreakoutV2_5mConfig)


def cb_grid_bbkc_v2_15m(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_BBKC_V2_15M, SqueezeBreakoutV2_15mConfig)


# --- squeeze v3 (NQ): one grid per bar size, so two runs -------------------------------------
from src.strategies.compression_breakout.config import (  # noqa: E402
    V3_5M_ENTRY_TYPES,
    V3_5M_KC_MULTS,
    V3_5M_MIN_SQUEEZE_BARS,
    V3_5M_SETUP_EXPIRIES,
    V3_5M_SQUEEZE_LENGTHS,
    V3_5M_STOPS,
    V3_5M_TARGETS,
    V3_15M_KC_MULTS,
    V3_15M_MIN_SQUEEZE_BARS,
    V3_15M_SETUP_EXPIRIES,
    V3_15M_SQUEEZE_LENGTHS,
    V3_15M_STOPS,
    V3_15M_TARGETS,
    V3_DIRECTIONS,
    V3_MIN_BOX_ATRS,
    SqueezeBreakoutV3_5mConfig,
    SqueezeBreakoutV3_15mConfig,
)

AXES_BBKC_V3_5M: dict[str, tuple] = {
    "timeframe": ("5min",),
    "squeeze_length": V3_5M_SQUEEZE_LENGTHS,
    "kc_mult": V3_5M_KC_MULTS,
    "min_squeeze_bars": V3_5M_MIN_SQUEEZE_BARS,
    "entry_type": V3_5M_ENTRY_TYPES,
    "setup_expiry_bars": V3_5M_SETUP_EXPIRIES,
    "stop": V3_5M_STOPS,
    "target_r": V3_5M_TARGETS,
    "direction": V3_DIRECTIONS,
    "trend_filter": TREND_FILTERS,
    "min_box_atr": V3_MIN_BOX_ATRS,
}

AXES_BBKC_V3_15M: dict[str, tuple] = {
    "timeframe": ("15min",),
    "squeeze_length": V3_15M_SQUEEZE_LENGTHS,
    "kc_mult": V3_15M_KC_MULTS,
    "min_squeeze_bars": V3_15M_MIN_SQUEEZE_BARS,
    "entry_type": ENTRY_TYPES,
    "setup_expiry_bars": V3_15M_SETUP_EXPIRIES,
    "stop": V3_15M_STOPS,
    "target_r": V3_15M_TARGETS,
    "direction": V3_DIRECTIONS,
    "trend_filter": TREND_FILTERS,
    "min_box_atr": V3_MIN_BOX_ATRS,
}


def cb_grid_bbkc_v3_5m(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_BBKC_V3_5M, SqueezeBreakoutV3_5mConfig)


def cb_grid_bbkc_v3_15m(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_BBKC_V3_15M, SqueezeBreakoutV3_15mConfig)


# --- squeeze v4 (YM): 15-minute bars only -----------------------------------------------------
from src.strategies.compression_breakout.config import (  # noqa: E402
    V4_15M_KC_MULTS,
    V4_15M_MIN_BOX_ATRS,
    V4_15M_MIN_SQUEEZE_BARS,
    V4_15M_SETUP_EXPIRIES,
    V4_15M_SQUEEZE_LENGTHS,
    V4_15M_STOPS,
    V4_15M_TARGETS,
    SqueezeBreakoutV4_15mConfig,
)

AXES_BBKC_V4_15M: dict[str, tuple] = {
    "timeframe": ("15min",),
    "squeeze_length": V4_15M_SQUEEZE_LENGTHS,
    "kc_mult": V4_15M_KC_MULTS,
    "min_squeeze_bars": V4_15M_MIN_SQUEEZE_BARS,
    "entry_type": ENTRY_TYPES,
    "setup_expiry_bars": V4_15M_SETUP_EXPIRIES,
    "stop": V4_15M_STOPS,
    "target_r": V4_15M_TARGETS,
    "direction": V3_DIRECTIONS,
    "trend_filter": TREND_FILTERS,
    "min_box_atr": V4_15M_MIN_BOX_ATRS,
}


def cb_grid_bbkc_v4_15m(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_BBKC_V4_15M, SqueezeBreakoutV4_15mConfig)
