"""Grid for last-half-hour momentum (equity index futures, 1-minute RTH bars).

  last_half_hour_v1 : 500 configs per contract
                      = 5 signal variants (prev_close / open, each with agree off|on; first_half)
                        x 5 windows x 5 filters x 4 stops

Later rounds add an AXES_LH_V<n> dict, a config class in src/strategies/last_half_hour/config.py,
a lattice in src/analysis/neighborhood.py and an entry in scripts/run_lh_funnel.py SPACES.
"""

from __future__ import annotations

import itertools

from src.experiments.mr_grid import ConfigEntry, variants_per_symbol  # noqa: F401  (re-export)
from src.strategies.last_half_hour.config import (
    V1_AGREE,
    V1_FILTERS,
    V1_SIGNALS,
    V1_STOPS,
    V1_WINDOWS,
    LastHalfHourV1Config,
)
from src.utils.hashing import config_id as compute_config_id

AXES_LH_V1: dict[str, tuple] = {
    "timeframe": ("1min",),
    "signal": V1_SIGNALS,
    "agree": V1_AGREE,
    "window": V1_WINDOWS,
    "filter": V1_FILTERS,
    "stop": V1_STOPS,
}


def _v1_valid(kw: dict) -> bool:
    return not (kw["signal"] == "first_half" and kw["agree"] == "on")


def _grid(symbols: tuple[str, ...], axes: dict[str, tuple], cls, valid=lambda kw: True) -> list[ConfigEntry]:
    names = list(axes.keys())
    out: list[ConfigEntry] = []
    seen: set[str] = set()
    for symbol in symbols:
        for combo in itertools.product(*(axes[n] for n in names)):
            kw = dict(zip(names, combo))
            if not valid(kw):
                continue
            cfg = cls(symbol=symbol, **kw)
            cid = compute_config_id(cfg.model_dump(mode="json"))
            if cid in seen:
                continue
            seen.add(cid)
            out.append(ConfigEntry(config=cfg, config_id=cid))
    return out


def lh_grid_v1(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_LH_V1, LastHalfHourV1Config, _v1_valid)
