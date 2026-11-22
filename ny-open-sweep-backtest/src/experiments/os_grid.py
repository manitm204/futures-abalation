"""Grid for the NY-open liquidity sweep (equity index futures, 1-minute bars).

  open_sweep_v1 : 24,300 configs per contract
                  = 5 levels x 3 sides x 3 windows x 2 penetrations x 3 confirms x 2 modes
                    x 3 stops x 5 targets x 3 time exits

The signal-defining axes come first so consecutive configs share a cached trigger set.
"""

from __future__ import annotations

import itertools

from src.experiments.mr_grid import ConfigEntry, variants_per_symbol  # noqa: F401  (re-export)
from src.strategies.open_sweep.config import (
    V1_CONFIRMS,
    V1_EXITS,
    V1_LEVELS,
    V1_MODES,
    V1_PENS,
    V1_SIDES,
    V1_STOPS,
    V1_TARGETS,
    V1_WINDOWS,
    OpenSweepV1Config,
)
from src.utils.hashing import config_id as compute_config_id

AXES_OS_V1: dict[str, tuple] = {
    "timeframe": ("1min",),
    "level": V1_LEVELS,
    "side": V1_SIDES,
    "window": V1_WINDOWS,
    "pen": V1_PENS,
    "confirm": V1_CONFIRMS,
    "mode": V1_MODES,
    "stop": V1_STOPS,
    "target": V1_TARGETS,
    "exit": V1_EXITS,
}


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


def os_grid_v1(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_OS_V1, OpenSweepV1Config)
