"""Typed config + ablation axes for the SPY RSI-divergence strategy.

Axes (the Cartesian grid: 32,768 variants per timeframe, 98,304 per symbol).
Every lookback, pivot width, gap and holding period is a count of BARS of the
chosen timeframe; the same values are used for 5min, 15min and 1h:
  timeframe      : 5min, 15min, 1h
  rsi_lookback   : 7, 10, 14, 21        (Wilder RSI period)
  pivot_left     : 3, 5, 8, 12          (bars left of an RSI pivot low that must be higher)
  pivot_right    : 1, 3                 (bars right of the pivot = confirmation delay)
  max_pivot_gap  : 12, 24, 48, 78       (max bars between the two RSI pivot lows)
  min_rsi_diff   : 0, 3, 5, 8           (RSI points the 2nd pivot low must exceed the 1st by; 0 = any higher low)
  stop_atr       : 0.75, 1.0, 1.5, 2.0  (stop distance below the entry, in ATR(14) multiples; this is 1R)
  target_r       : 1.0, 1.5, 2.0, 3.0   (profit target, in R multiples above the entry)
  max_hold       : 6, 12, 24, 48        (bars)
"""

from __future__ import annotations

from typing import Literal

from src.utils.config_models import FrozenModel

Timeframe = Literal["5min", "15min", "1h"]

TIMEFRAMES: tuple[str, ...] = ("5min", "15min", "1h")
RSI_LOOKBACKS: tuple[int, ...] = (7, 10, 14, 21)
PIVOT_LEFTS: tuple[int, ...] = (3, 5, 8, 12)
PIVOT_RIGHTS: tuple[int, ...] = (1, 3)
MAX_PIVOT_GAPS: tuple[int, ...] = (12, 24, 48, 78)
MIN_RSI_DIFFS: tuple[float, ...] = (0.0, 3.0, 5.0, 8.0)
STOP_ATRS: tuple[float, ...] = (0.75, 1.0, 1.5, 2.0)
TARGET_RS: tuple[float, ...] = (1.0, 1.5, 2.0, 3.0)
MAX_HOLDS: tuple[int, ...] = (6, 12, 24, 48)


class RSIDivergenceConfig(FrozenModel):
    symbol: str
    timeframe: Timeframe = "15min"
    rsi_lookback: Literal[7, 10, 14, 21] = 14
    pivot_left: Literal[3, 5, 8, 12] = 5
    pivot_right: Literal[1, 3] = 1
    max_pivot_gap: Literal[12, 24, 48, 78] = 48
    min_rsi_diff: Literal[0.0, 3.0, 5.0, 8.0] = 0.0
    stop_atr: Literal[0.75, 1.0, 1.5, 2.0] = 1.0
    target_r: Literal[1.0, 1.5, 2.0, 3.0] = 2.0
    max_hold: Literal[6, 12, 24, 48] = 24
