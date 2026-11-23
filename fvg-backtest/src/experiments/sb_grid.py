"""Grid for ICT's Silver Bullet / 2022 Model with placebo windows (equity index futures, 1-minute bars).

  silver_bullet_v1 : 1,728 configs per contract
                     = 6 windows x 3 FVG minimums x 3 displacement levels x 2 entries x 2 stops
                       x 4 targets x 2 sweep requirements

The setup-defining axes come first so consecutive configs share cached setup lists.
"""

from __future__ import annotations

import itertools

from src.experiments.mr_grid import ConfigEntry, variants_per_symbol  # noqa: F401  (re-export)
from src.strategies.silver_bullet.config import (
    V1_DISPS,
    V1_ENTRIES,
    V1_FVG_MINS,
    V1_STOPS,
    V1_SWEEPS,
    V1_TARGETS,
    V1_WINDOWS,
    SilverBulletV1Config,
)
from src.utils.hashing import config_id as compute_config_id

AXES_SB_V1: dict[str, tuple] = {
    "timeframe": ("1min",),
    "window": V1_WINDOWS,
    "sweep": V1_SWEEPS,
    "fvg_min": V1_FVG_MINS,
    "disp": V1_DISPS,
    "entry": V1_ENTRIES,
    "stop": V1_STOPS,
    "target": V1_TARGETS,
}


def _grid(symbols: tuple[str, ...], axes: dict[str, tuple], cls) -> list[ConfigEntry]:
    names = list(axes.keys())
    out: list[ConfigEntry] = []
    seen: set[str] = set()
    for symbol in symbols:
        for combo in itertools.product(*(axes[n] for n in names)):
            cfg = cls(symbol=symbol, **dict(zip(names, combo)))
            cid = compute_config_id(cfg.model_dump(mode="json"))
            if cid in seen:
                continue
            seen.add(cid)
            out.append(ConfigEntry(config=cfg, config_id=cid))
    return out


def sb_grid_v1(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_SB_V1, SilverBulletV1Config)
