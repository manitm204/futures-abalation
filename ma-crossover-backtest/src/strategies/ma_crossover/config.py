"""Typed config + ablation axes for the SPY moving-average crossover strategy.

Axes (the Cartesian grid: 20,000 variants per timeframe, 60,000 per symbol).
Every length and bar count is in BARS of the chosen timeframe; the same values
are used for 5min, 15min and 1h:
  timeframe     : 5min, 15min, 1h
  ma_pair       : SMA/SMA, EMA/EMA, EMA/SMA, SMA/EMA   (fast MA type / slow MA type)
  fast_length   : 5, 8, 12, 16, 20
  slow_length   : 40, 60, 80, 100, 150
  confirm_bars  : 1, 2, 3, 4      (the fast MA must have been above the slow MA for this
                                   many consecutive completed bars; 1 = no extra confirmation)
  buffer_atr    : 0, 0.10, 0.20, 0.35, 0.50
                                  (fast - slow >= this x ATR(14) at the signal bar; 0 = off)
  stop_atr      : off, 1.5, 2.0, 2.5, 3.0
                                  (initial stop this x ATR(14) below the entry open; None = off)
  slope_filter  : off, on         (slow MA above its value SLOPE_BARS bars earlier)
Long-only: the bearish side of the crossover and of the slope filter is unused.
"""

from __future__ import annotations

from typing import Literal

from src.utils.config_models import FrozenModel

TIMEFRAMES: tuple[str, ...] = ("5min", "15min", "1h")
MA_PAIRS: tuple[str, ...] = ("SMA/SMA", "EMA/EMA", "EMA/SMA", "SMA/EMA")
FAST_LENGTHS: tuple[int, ...] = (5, 8, 12, 16, 20)
SLOW_LENGTHS: tuple[int, ...] = (40, 60, 80, 100, 150)
CONFIRM_BARS: tuple[int, ...] = (1, 2, 3, 4)
BUFFER_ATRS: tuple[float, ...] = (0.0, 0.10, 0.20, 0.35, 0.50)
STOP_ATRS: tuple[float | None, ...] = (None, 1.5, 2.0, 2.5, 3.0)
SLOPE_FILTERS: tuple[bool, ...] = (False, True)

SLOPE_BARS = 5


class MACrossoverConfig(FrozenModel):
    symbol: str
    timeframe: Literal["5min", "15min", "1h"] = "15min"
    ma_pair: Literal["SMA/SMA", "EMA/EMA", "EMA/SMA", "SMA/EMA"] = "SMA/SMA"
    fast_length: Literal[5, 8, 12, 16, 20] = 12
    slow_length: Literal[40, 60, 80, 100, 150] = 80
    confirm_bars: Literal[1, 2, 3, 4] = 1
    buffer_atr: Literal[0.0, 0.10, 0.20, 0.35, 0.50] = 0.0
    stop_atr: Literal[None, 1.5, 2.0, 2.5, 3.0] = None
    slope_filter: bool = False


# --- v2 parameter space (ma_v2) ----------------------------------------------------------
# 2 x 2 x 3 x 4 x 2 x 2 x 2 x 2 x 4 x 3 x 3 x 3 x 3 = 248,832 variants per symbol
# (124,416 per timeframe). v1's axes narrowed (slow length adds 200) plus five new rules,
# each "off" by default so v1 configs behave exactly as before:
#   max_hold          : off, 8, 16, 32   (time exit: decided at the close of the max_hold-th
#                       bar held, filled at the next open, even without a cross back)
#   take_profit_atr   : off, 2.0, 4.0    (limit target = entry-bar open + k x ATR(14) known
#                       before the fill, live from the entry bar)
#   cooldown_bars     : 0, 4, 12         (after ANY exit, no entry may fill until this many
#                       bars after the exit bar)
#   min_adx           : off, 15, 25      (Wilder ADX(14) at the signal bar >= threshold)
#   max_extension_atr : off, 1.5, 3.0    (close - slow MA <= k x ATR(14) at the signal bar)
TIMEFRAMES_V2: tuple[str, ...] = ("5min", "15min")
MA_PAIRS_V2: tuple[str, ...] = ("EMA/EMA", "SMA/EMA")
FAST_LENGTHS_V2: tuple[int, ...] = (5, 8, 12)
SLOW_LENGTHS_V2: tuple[int, ...] = (80, 100, 150, 200)
CONFIRM_BARS_V2: tuple[int, ...] = (1, 2)
BUFFER_ATRS_V2: tuple[float, ...] = (0.0, 0.20)
STOP_ATRS_V2: tuple[float | None, ...] = (None, 2.0)
SLOPE_FILTERS_V2: tuple[bool, ...] = (False, True)
MAX_HOLDS_V2: tuple[int | None, ...] = (None, 8, 16, 32)
TAKE_PROFIT_ATRS_V2: tuple[float | None, ...] = (None, 2.0, 4.0)
COOLDOWN_BARS_V2: tuple[int, ...] = (0, 4, 12)
MIN_ADXS_V2: tuple[float | None, ...] = (None, 15.0, 25.0)
MAX_EXTENSION_ATRS_V2: tuple[float | None, ...] = (None, 1.5, 3.0)


class MACrossoverV2Config(FrozenModel):
    symbol: str
    timeframe: Literal["5min", "15min"] = "15min"
    ma_pair: Literal["EMA/EMA", "SMA/EMA"] = "EMA/EMA"
    fast_length: Literal[5, 8, 12] = 8
    slow_length: Literal[80, 100, 150, 200] = 100
    confirm_bars: Literal[1, 2] = 1
    buffer_atr: Literal[0.0, 0.20] = 0.0
    stop_atr: Literal[None, 2.0] = None
    slope_filter: bool = False
    max_hold: Literal[None, 8, 16, 32] = None
    take_profit_atr: Literal[None, 2.0, 4.0] = None
    cooldown_bars: Literal[0, 4, 12] = 0
    min_adx: Literal[None, 15.0, 25.0] = None
    max_extension_atr: Literal[None, 1.5, 3.0] = None
