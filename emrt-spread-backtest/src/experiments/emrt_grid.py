"""Full-factorial grids for the EMRT spread line (one grid per pair; the pair is the `symbol`).

  emrt_spread_v1 : 51,840 configs (15min / 30min / 1h bars in one grid)
  emrt_spread_v2 : 13,824 configs (5min / 15min; session-anchored, flat by the close)

Later rounds add an AXES_EMRT_V<n> dict, a config class in src/strategies/emrt_spread/config.py,
a lattice in src/analysis/neighborhood.py and an entry in scripts/run_emrt_funnel.py SPACES.
"""

from __future__ import annotations

from src.experiments.mr_grid import ConfigEntry, _grid, variants_per_symbol  # noqa: F401  (re-export)
from src.strategies.emrt_spread.config import (
    V1_ENTRY_ZS,
    V1_EXITS,
    V1_FORMATIONS,
    V1_HEDGES,
    V1_OVERNIGHTS,
    V1_SIDES,
    V1_STOPS,
    V1_TIME_STOPS,
    V1_TIMEFRAMES,
    V1_Z_MODES,
    EMRTV1Config,
)

AXES_EMRT_V1: dict[str, tuple] = {
    "timeframe": V1_TIMEFRAMES,
    "formation": V1_FORMATIONS,
    "hedge": V1_HEDGES,
    "z_mode": V1_Z_MODES,
    "entry_z": V1_ENTRY_ZS,
    "exit": V1_EXITS,
    "stop": V1_STOPS,
    "time_stop": V1_TIME_STOPS,
    "side": V1_SIDES,
    "overnight": V1_OVERNIGHTS,
}


def emrt_grid_v1(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_EMRT_V1, EMRTV1Config)


from src.strategies.emrt_spread.config import (  # noqa: E402
    V2_ENTRY_ZS,
    V2_EXITS,
    V2_FIRST_ENTRIES,
    V2_FORMATIONS,
    V2_HEDGES,
    V2_OVERNIGHTS,
    V2_SIDES,
    V2_STOPS,
    V2_TIME_STOPS,
    V2_TIMEFRAMES,
    V2_Z_MODES,
    EMRTV2Config,
)

AXES_EMRT_V2: dict[str, tuple] = {
    "timeframe": V2_TIMEFRAMES,
    "formation": V2_FORMATIONS,
    "hedge": V2_HEDGES,
    "z_mode": V2_Z_MODES,
    "entry_z": V2_ENTRY_ZS,
    "exit": V2_EXITS,
    "stop": V2_STOPS,
    "time_stop": V2_TIME_STOPS,
    "side": V2_SIDES,
    "first_entry": V2_FIRST_ENTRIES,
    "overnight": V2_OVERNIGHTS,
}


def emrt_grid_v2(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_EMRT_V2, EMRTV2Config)
