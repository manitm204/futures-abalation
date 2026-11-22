"""Grid for the Treasury month-end long (day session only).

  month_end_v1 : 972 configs per contract (1-minute bars)
                 = 6 windows x 6 entry times x 3 exit rules x 3 event filters x 3 stops
  month_end_v2 : 4,864 configs per contract (turn of the month, equity index futures)
                 = 19 day sets (last 0-4 x first 0-3, not both 0) x 32 entry/exit pairs (exit
                 after entry) x 2 event filters x 4 stops

Later rounds add an AXES_ME_V<n> dict, a config class in src/strategies/month_end/config.py, a
lattice in src/analysis/neighborhood.py and an entry in scripts/run_me_funnel.py SPACES.
"""

from __future__ import annotations

import itertools

from src.experiments.mr_grid import ConfigEntry, variants_per_symbol  # noqa: F401  (re-export)
from src.strategies.month_end.config import (
    V1_ENTRIES,
    V1_EVENT_FILTERS,
    V1_EXITS,
    V1_STOPS,
    V1_WINDOWS,
    V2_ENTRIES,
    V2_EVENT_FILTERS,
    V2_EXITS,
    V2_FIRST_DAYS,
    V2_STOPS,
    V2_WINDOWS,
    MonthEndV1Config,
    MonthEndV2Config,
    hhmm_minutes,
)
from src.utils.hashing import config_id as compute_config_id

AXES_ME_V1: dict[str, tuple] = {
    "timeframe": ("1min",),
    "window": V1_WINDOWS,
    "entry": V1_ENTRIES,
    "exit": V1_EXITS,
    "event_filter": V1_EVENT_FILTERS,
    "stop": V1_STOPS,
}


AXES_ME_V2: dict[str, tuple] = {
    "timeframe": ("1min",),
    "window": V2_WINDOWS,
    "first_days": V2_FIRST_DAYS,
    "entry": V2_ENTRIES,
    "exit": V2_EXITS,
    "event_filter": V2_EVENT_FILTERS,
    "stop": V2_STOPS,
}


def _v2_valid(kw: dict) -> bool:
    return kw["window"] + kw["first_days"] >= 1 and hhmm_minutes(kw["exit"]) > hhmm_minutes(kw["entry"])


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


def me_grid_v1(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_ME_V1, MonthEndV1Config)


def me_grid_v2(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_ME_V2, MonthEndV2Config, _v2_valid)
