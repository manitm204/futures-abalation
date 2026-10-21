"""Typed config + ablation axes for the SPY mean-reversion strategy.

Axes (the Cartesian grid, 75,000 variants per symbol). Every lookback, SMA
length and holding period is a count of BARS of the chosen timeframe (the
same convention as the channel-breakout grid):
  timeframe     : 5min, 15min, 1h
  mean_type     : sma, ema
  mean_lookback : 5, 10, 15, 20, 40      (bars)
  std_lookback  : 10, 15, 20, 40, 60     (rolling std of CLOSE PRICE, bars)
  entry_z       : -1.0, -1.25, -1.5, -1.75, -2.0
  exit_z        : -0.5, -0.25, 0.0, 0.25, 0.5
  max_hold      : 2, 3, 5, 7, 10         (bars)
  trend_filter  : none, sma100, sma150, sma200   (close above that SMA at the signal close)

z = (close - mean) / std. Every exit_z is above every entry_z, so an entry can
never immediately satisfy its own exit rule.
"""

from __future__ import annotations

from typing import Literal

from src.utils.config_models import FrozenModel

Timeframe = Literal["5min", "15min", "1h"]
MeanType = Literal["sma", "ema"]
TrendFilter = Literal["none", "sma100", "sma150", "sma200"]

TIMEFRAMES: tuple[str, ...] = ("5min", "15min", "1h")
MEAN_TYPES: tuple[str, ...] = ("sma", "ema")
MEAN_LOOKBACKS: tuple[int, ...] = (5, 10, 15, 20, 40)
STD_LOOKBACKS: tuple[int, ...] = (10, 15, 20, 40, 60)
ENTRY_ZS: tuple[float, ...] = (-1.0, -1.25, -1.5, -1.75, -2.0)
EXIT_ZS: tuple[float, ...] = (-0.5, -0.25, 0.0, 0.25, 0.5)
MAX_HOLDS: tuple[int, ...] = (2, 3, 5, 7, 10)
TREND_FILTERS: tuple[str, ...] = ("none", "sma100", "sma150", "sma200")


class MeanReversionConfig(FrozenModel):
    symbol: str
    timeframe: Timeframe = "15min"
    mean_type: MeanType = "sma"
    mean_lookback: Literal[5, 10, 15, 20, 40] = 10
    std_lookback: Literal[10, 15, 20, 40, 60] = 20
    entry_z: Literal[-1.0, -1.25, -1.5, -1.75, -2.0] = -1.5
    exit_z: Literal[-0.5, -0.25, 0.0, 0.25, 0.5] = 0.0
    max_hold: Literal[2, 3, 5, 7, 10] = 5
    trend_filter: TrendFilter = "none"


# --- v2 parameter space (mr_v2, 240,000 variants per symbol) ------------------------------
# No separate std axis: the z-score's std uses the same window as the mean.
# Lengths are bars. stop_atr_multiple "none" = no stop.
V2_MEAN_LOOKBACKS: tuple[int, ...] = (8, 12, 20, 32, 48)
V2_EXIT_ZS: tuple[float, ...] = (-0.25, 0.0, 0.25, 0.5)
V2_MAX_HOLDS: tuple[int, ...] = (2, 4, 8, 16)
V2_TREND_FILTERS: tuple[str, ...] = ("none", "above_sma_100")
V2_ENTRY_CONFIRMATIONS: tuple[str, ...] = ("none", "positive_bar_return")
V2_COOLDOWNS: tuple[int, ...] = (0, 1, 2, 4, 8)
V2_STOP_ATRS: tuple[str, ...] = ("none", "1.0", "1.5", "2.0", "3.0")


class MeanReversionV2Config(FrozenModel):
    symbol: str
    timeframe: Timeframe = "15min"
    mean_type: MeanType = "sma"
    mean_lookback: Literal[8, 12, 20, 32, 48] = 20
    entry_z: Literal[-1.0, -1.25, -1.5, -1.75, -2.0] = -1.5
    exit_z: Literal[-0.25, 0.0, 0.25, 0.5] = 0.0
    max_holding_bars: Literal[2, 4, 8, 16] = 4
    trend_filter: Literal["none", "above_sma_100"] = "none"
    entry_confirmation: Literal["none", "positive_bar_return"] = "none"
    cooldown_bars: Literal[0, 1, 2, 4, 8] = 0
    stop_atr_multiple: Literal["none", "1.0", "1.5", "2.0", "3.0"] = "none"

    @property
    def std_lookback(self) -> int:
        return self.mean_lookback

    @property
    def max_hold(self) -> int:
        return self.max_holding_bars

    @property
    def stop_atr_value(self) -> float | None:
        return None if self.stop_atr_multiple == "none" else float(self.stop_atr_multiple)
