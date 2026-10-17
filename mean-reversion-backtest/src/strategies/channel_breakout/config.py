"""Typed config + ablation axes for the channel-breakout strategy.

Axes (the Cartesian grid):
  timeframe        : 5min, 15min, 1h
  entry_lookback   : 10, 15, 20, 30, 40, 55, 80, 120  (Donchian entry channel, bars)
  exit_ratio       : 0.25, 0.50, 0.75, 1.00  -> exit_lookback = max(1, floor(entry*ratio))
  buffer_atr       : 0.0, 0.10, 0.25, 0.50   (breakout buffer, in ATR above the channel)
  init_stop        : off, 1.5, 2, 3          (fixed initial stop, in ATR; off = channel exit only)
  confirm          : 1, 2                     (consecutive closes beyond the breakout threshold)
  trend_filter     : off, sma50, sma100, sma200, ema50, ema100, ema200, ema50_gt_ema200
"""

from __future__ import annotations

import math
from typing import Literal

from src.utils.config_models import FrozenModel

Timeframe = Literal["5min", "15min", "1h"]
InitStop = Literal["off", "1.5", "2", "3"]
TrendFilter = Literal[
    "off", "sma50", "sma100", "sma200", "ema50", "ema100", "ema200", "ema50_gt_ema200"
]

ENTRY_LOOKBACKS: tuple[int, ...] = (10, 15, 20, 30, 40, 55, 80, 120)
EXIT_RATIOS: tuple[float, ...] = (0.25, 0.50, 0.75, 1.00)
BUFFER_ATRS: tuple[float, ...] = (0.0, 0.10, 0.25, 0.50)
INIT_STOPS: tuple[str, ...] = ("off", "1.5", "2", "3")
CONFIRMS: tuple[int, ...] = (1, 2)
TREND_FILTERS: tuple[str, ...] = (
    "off", "sma50", "sma100", "sma200", "ema50", "ema100", "ema200", "ema50_gt_ema200"
)


class ChannelBreakoutConfig(FrozenModel):
    symbol: str
    timeframe: Timeframe = "15min"
    entry_lookback: Literal[10, 15, 20, 30, 40, 55, 80, 120] = 20
    exit_ratio: Literal[0.25, 0.50, 0.75, 1.00] = 0.50
    buffer_atr: Literal[0.0, 0.10, 0.25, 0.50] = 0.0
    init_stop: InitStop = "off"
    confirm: Literal[1, 2] = 1
    trend_filter: TrendFilter = "off"
    atr_period: int = 14

    @property
    def exit_lookback(self) -> int:
        return max(1, math.floor(self.entry_lookback * self.exit_ratio))

    @property
    def init_stop_atr(self) -> float | None:
        return None if self.init_stop == "off" else float(self.init_stop)
