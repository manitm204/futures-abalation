"""Typed config + ablation axes for the intraday noise-band breakout (momentum) strategy.

After Zarattini, Aziz & Barbon (2024), "Beat the Market: An Effective Intraday
Momentum Strategy for S&P500 ETF (SPY)". The band around each session's open is
the "noise area": the average absolute move from the open, AT THE SAME TIME OF
DAY, over the previous `band_lookback` sessions, times `band_mult`. A close
outside the band at a check time is treated as a real move and traded in its
direction; every position is flat by the session close.

Axes (the Cartesian grid, v1 = 6,480 variants per symbol):
  timeframe      : 5min, 15min          (bar size)
  band_lookback  : 7, 10, 14, 20, 30    (sessions averaged per time-of-day slot)
  band_mult      : 0.75, 1.0, 1.25, 1.5 (band half-width = band_mult x average move)
  check_minutes  : 15, 30, 60           (signals / trailing exits only at bar closes
                                         that land on a multiple of this from the open)
  anchor         : open                 (band centred on the session open)
                   open_prev_close      (upper edge from max(open, prior close), lower from
                                         min(open, prior close): the paper's gap adjustment)
  trail          : band                 (long exits when a check close falls back inside the band)
                   vwap                 (long exits on a check close below session VWAP)
                   band_vwap            (the tighter of the two: below max(upper band, VWAP))
  direction      : long, short, both
  stop_atr       : none, 1.0, 2.0       (protective stop at entry open -/+ k x ATR(14), intrabar)
"""

from __future__ import annotations

from typing import Literal

from src.utils.config_models import FrozenModel

Timeframe = Literal["5min", "15min"]
Anchor = Literal["open", "open_prev_close"]
Trail = Literal["band", "vwap", "band_vwap"]
Direction = Literal["long", "short", "both"]

TIMEFRAMES: tuple[str, ...] = ("5min", "15min")
BAND_LOOKBACKS: tuple[int, ...] = (7, 10, 14, 20, 30)
BAND_MULTS: tuple[float, ...] = (0.75, 1.0, 1.25, 1.5)
CHECK_MINUTES: tuple[int, ...] = (15, 30, 60)
ANCHORS: tuple[str, ...] = ("open", "open_prev_close")
TRAILS: tuple[str, ...] = ("band", "vwap", "band_vwap")
DIRECTIONS: tuple[str, ...] = ("long", "short", "both")
STOP_ATRS: tuple[str, ...] = ("none", "1.0", "2.0")


class NoiseBandConfig(FrozenModel):
    symbol: str
    timeframe: Timeframe = "5min"
    band_lookback: Literal[7, 10, 14, 20, 30] = 14
    band_mult: Literal[0.75, 1.0, 1.25, 1.5] = 1.0
    check_minutes: Literal[15, 30, 60] = 30
    anchor: Anchor = "open_prev_close"
    trail: Trail = "band_vwap"
    direction: Direction = "both"
    stop_atr_multiple: Literal["none", "1.0", "2.0"] = "none"

    @property
    def stop_atr_value(self) -> float | None:
        return None if self.stop_atr_multiple == "none" else float(self.stop_atr_multiple)
