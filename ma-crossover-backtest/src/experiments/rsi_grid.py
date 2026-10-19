"""Full-factorial grids for the RSI-divergence strategy.
v1: 32,768 variants per timeframe x 3 timeframes = 98,304 per symbol.
v2: 34,992 variants per timeframe x 2 timeframes = 69,984 per symbol.
v3: 124,416 variants per timeframe x 2 timeframes = 248,832 per symbol."""

from __future__ import annotations

import itertools
from dataclasses import dataclass

from src.strategies.rsi_divergence import config as C
from src.strategies.rsi_divergence.config import (
    ADX_FILTERS_V2,
    MAX_HOLDS,
    MAX_HOLDS_V2,
    MAX_PIVOT_GAPS_V2,
    MIN_PRICE_DIVS_V2,
    MIN_RSI_DIFFS_V2,
    PIVOT_LEFTS_V2,
    PIVOT_RIGHTS_V2,
    RSI_EXTREMES_V2,
    RSI_LOOKBACKS_V2,
    STOP_ATRS_V2,
    TARGET_RS_V2,
    TIMEFRAMES_V2,
    RSIDivergenceV2Config,
    MAX_PIVOT_GAPS,
    MIN_RSI_DIFFS,
    PIVOT_LEFTS,
    PIVOT_RIGHTS,
    RSI_LOOKBACKS,
    STOP_ATRS,
    TARGET_RS,
    TIMEFRAMES,
    RSIDivergenceConfig,
)
from src.utils.hashing import config_id as compute_config_id

# Axis name -> values, in one place (grid size / report both derive from this).
AXES: dict[str, tuple] = {
    "timeframe": TIMEFRAMES,
    "rsi_lookback": RSI_LOOKBACKS,
    "pivot_left": PIVOT_LEFTS,
    "pivot_right": PIVOT_RIGHTS,
    "max_pivot_gap": MAX_PIVOT_GAPS,
    "min_rsi_diff": MIN_RSI_DIFFS,
    "stop_atr": STOP_ATRS,
    "target_r": TARGET_RS,
    "max_hold": MAX_HOLDS,
}

AXES_V2: dict[str, tuple] = {
    "timeframe": TIMEFRAMES_V2,
    "rsi_lookback": RSI_LOOKBACKS_V2,
    "pivot_left": PIVOT_LEFTS_V2,
    "pivot_right": PIVOT_RIGHTS_V2,
    "max_pivot_gap": MAX_PIVOT_GAPS_V2,
    "min_rsi_diff": MIN_RSI_DIFFS_V2,
    "stop_atr": STOP_ATRS_V2,
    "target_r": TARGET_RS_V2,
    "max_hold": MAX_HOLDS_V2,
    "rsi_extreme": RSI_EXTREMES_V2,
    "adx_filter": ADX_FILTERS_V2,
    "min_price_div_atr": MIN_PRICE_DIVS_V2,
}

AXES_V3: dict[str, tuple] = {
    "timeframe": C.TIMEFRAMES_V3,
    "rsi_lookback": C.RSI_LOOKBACKS_V3,
    "pivot_left": C.PIVOT_LEFTS_V3,
    "pivot_right": C.PIVOT_RIGHTS_V3,
    "max_pivot_gap": C.MAX_PIVOT_GAPS_V3,
    "min_rsi_diff": C.MIN_RSI_DIFFS_V3,
    "stop_atr": C.STOP_ATRS_V3,
    "target_r": C.TARGET_RS_V3,
    "max_hold": C.MAX_HOLDS_V3,
    "rsi_extreme": C.RSI_EXTREMES_V3,
    "adx_filter": C.ADX_FILTERS_V3,
    "min_price_div_atr": C.MIN_PRICE_DIVS_V3,
    "trend_filter": C.TREND_FILTERS_V3,
    "entry_confirmation": C.ENTRY_CONFIRMATIONS_V3,
    "session_window": C.SESSION_WINDOWS_V3,
}


@dataclass(frozen=True)
class ConfigEntry:
    config: RSIDivergenceConfig | RSIDivergenceV2Config | C.RSIDivergenceV3Config
    config_id: str


def variants_per_symbol(axes: dict[str, tuple] = AXES) -> int:
    n = 1
    for v in axes.values():
        n *= len(v)
    return n


def rsi_grid(symbols: tuple[str, ...], *, axes: dict[str, tuple] = AXES, cls=RSIDivergenceConfig) -> list[ConfigEntry]:
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


def rsi_grid_v2(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return rsi_grid(symbols, axes=AXES_V2, cls=RSIDivergenceV2Config)


def rsi_grid_v3(symbols: tuple[str, ...]) -> list[ConfigEntry]:
    return rsi_grid(symbols, axes=AXES_V3, cls=C.RSIDivergenceV3Config)
