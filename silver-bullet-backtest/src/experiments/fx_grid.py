"""Grid for the daytime FX-fix reversal line.

  fx_fix_v1 : 405 configs per contract (1-minute bars)
              = leg post / both: 5 switch offsets x 4 post holds x 3 vol gates x 3 stops = 180 each
              + leg pre:         5 switch offsets x 3 vol gates x 3 stops               =  45
The pre leg never uses `post_hold`, so it is pinned to "eod" there instead of being multiplied
out (no duplicate configs, so the raw trial count is the real one).

Later rounds add an AXES_FX_V<n> dict, a config class in src/strategies/fx_fix/config.py, a
lattice in src/analysis/neighborhood.py and an entry in scripts/run_fx_funnel.py SPACES.
"""

from __future__ import annotations

import itertools

from src.experiments.mr_grid import ConfigEntry, variants_per_symbol  # noqa: F401  (re-export)
from src.strategies.fx_fix.config import (
    V1_LEGS,
    V1_POST_HOLDS,
    V1_STOPS,
    V1_SWITCH_OFFSETS,
    V1_VOL_GATES,
    FXFixV1Config,
)
from src.utils.hashing import config_id as compute_config_id

AXES_FX_V1: dict[str, tuple] = {
    "timeframe": ("1min",),
    "leg": V1_LEGS,
    "switch_offset": V1_SWITCH_OFFSETS,
    "post_hold": V1_POST_HOLDS,
    "vol_gate": V1_VOL_GATES,
    "stop": V1_STOPS,
}
# Axes a leg does not use, pinned to one value.
UNUSED_BY_LEG: dict[str, dict[str, object]] = {"pre": {"post_hold": "eod"}}


def _grid(symbols: tuple[str, ...], axes: dict[str, tuple], cls) -> list[ConfigEntry]:
    names = list(axes.keys())
    out: list[ConfigEntry] = []
    seen: set[str] = set()
    for symbol in symbols:
        for combo in itertools.product(*(axes[n] for n in names)):
            kw = dict(zip(names, combo))
            kw.update(UNUSED_BY_LEG.get(kw["leg"], {}))
            cfg = cls(symbol=symbol, **kw)
            cid = compute_config_id(cfg.model_dump(mode="json"))
            if cid in seen:
                continue
            seen.add(cid)
            out.append(ConfigEntry(config=cfg, config_id=cid))
    return out


def fx_grid_v1(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return _grid(symbols, AXES_FX_V1, FXFixV1Config)
