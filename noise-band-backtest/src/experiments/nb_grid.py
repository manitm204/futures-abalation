"""Full-factorial grids for the noise-band breakout strategy: v1 (8,100 variants per symbol).

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
    NoiseBandConfig,
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
