"""Grid for the FVG-after-displacement trade, with and against the gap (equity index futures, 1-minute bars).

  fvg_v1 : 24,192 configs per contract
           = 3 windows x 2 modes x 4 displacements x 2 gap minimums x 2 VWAP gates
             x (2 resting entries x 3 waits + market) x 3 stops x 4 targets x 3 holds

The setup-defining axes come first so consecutive configs share cached setup lists.
"""

from __future__ import annotations

import itertools

from src.experiments.mr_grid import ConfigEntry, variants_per_symbol  # noqa: F401  (re-export)
from src.strategies.fvg.config import (
    V1_DISPS,
    V1_ENTRIES,
    V1_FVG_MINS,
    V1_HOLDS,
    V1_MODES,
    V1_STOPS,
    V1_TARGETS,
    V1_VWAPS,
    V1_WAITS,
    V1_WINDOWS,
    FvgV1Config,
)
from src.utils.hashing import config_id as compute_config_id

AXES_FV_V1: dict[str, tuple] = {
    "timeframe": ("1min",),
    "window": V1_WINDOWS,
    "mode": V1_MODES,
    "disp": V1_DISPS,
    "fvg_min": V1_FVG_MINS,
    "vwap": V1_VWAPS,
    "entry": V1_ENTRIES,
    "wait": (0, *V1_WAITS),
    "stop": V1_STOPS,
    "target": V1_TARGETS,
    "hold": V1_HOLDS,
}


def _valid(kw: dict) -> bool:
    """A market entry has no resting order (wait 0); a resting order needs a wait."""
    return (kw["entry"] == "mkt") == (kw["wait"] == 0)


def fv_grid_v1(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    names = list(AXES_FV_V1)
    out: list[ConfigEntry] = []
    seen: set[str] = set()
    for symbol in symbols:
        for combo in itertools.product(*(AXES_FV_V1[n] for n in names)):
            kw = dict(zip(names, combo))
            if not _valid(kw):
                continue
            cfg = FvgV1Config(symbol=symbol, **kw)
            cid = compute_config_id(cfg.model_dump(mode="json"))
            if cid not in seen:
                seen.add(cid)
                out.append(ConfigEntry(config=cfg, config_id=cid))
    return out
