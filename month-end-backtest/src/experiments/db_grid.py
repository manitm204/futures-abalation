"""Full-factorial grid for the drift-burst fade.

  drift_burst_v1 : 576 configs per market (1-minute day-session bars)
                   = 3 burst windows x 4 thresholds x 4 volume gates x 2 sides x 3 holds x 2 news filters
  drift_burst_v2 : 10,368 configs per market
                   = 3 windows x 4 thresholds x 4 volume gates x 2 sides x 3 holds x 3 entry modes
                     x 3 targets x 2 stops x 2 trade caps (news filter fixed off)

Later rounds add an AXES_DB_V<n> dict, a config class in src/strategies/drift_burst/config.py, a
lattice in src/analysis/neighborhood.py and an entry in scripts/run_db_funnel.py SPACES.
"""

from __future__ import annotations

from src.experiments.mr_grid import ConfigEntry, _grid, variants_per_symbol  # noqa: F401  (re-export)
from src.strategies.drift_burst.config import (
    V1_BURST_WINDOWS,
    V1_HOLDS,
    V1_NEWS_FILTERS,
    V1_SIDES,
    V1_THRESHOLDS,
    V1_VOL_GATES,
    DriftBurstV1Config,
)

AXES_DB_V1: dict[str, tuple] = {
    "timeframe": ("1min",),
    "burst_window": V1_BURST_WINDOWS,
    "threshold": V1_THRESHOLDS,
    "vol_gate": V1_VOL_GATES,
    "side": V1_SIDES,
    "hold": V1_HOLDS,
    "news_filter": V1_NEWS_FILTERS,
}


def db_grid_v1(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_DB_V1, DriftBurstV1Config)


# --- v2: 10,368 configs (run on ES) ------------------------------------------------------------
from src.strategies.drift_burst.config import (  # noqa: E402
    V2_ENTRY_MODES,
    V2_MAX_TRADES,
    V2_STOPS,
    V2_TARGETS,
    DriftBurstV2Config,
)

AXES_DB_V2: dict[str, tuple] = {
    "timeframe": ("1min",),
    "burst_window": V1_BURST_WINDOWS,
    "threshold": V1_THRESHOLDS,
    "vol_gate": V1_VOL_GATES,
    "side": V1_SIDES,
    "hold": V1_HOLDS,
    "entry_mode": V2_ENTRY_MODES,
    "target": V2_TARGETS,
    "stop": V2_STOPS,
    "max_trades": V2_MAX_TRADES,
}


def db_grid_v2(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_DB_V2, DriftBurstV2Config)
