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


# --- v3 parameter space (futures, 46,080 variants per symbol) -----------------------------
# Separate mean and volatility (std) windows, no trend filter, no cooldown.
# Lengths are bars. entry_confirmation "positive_bar_return" = the signal bar
# closes above the previous close (a directional up bar). stop "none" = no stop.
V3_MEAN_LOOKBACKS: tuple[int, ...] = (5, 12, 40)
V3_STD_LOOKBACKS: tuple[int, ...] = (10, 20, 40, 80)
V3_ENTRY_ZS: tuple[float, ...] = (-1.5, -2.0, -2.5, -3.0)
V3_EXIT_ZS: tuple[float, ...] = (-1.0, -0.5, 0.0, 0.5)
V3_MAX_HOLDS: tuple[int, ...] = (5, 10, 16, 30)
V3_ENTRY_CONFIRMATIONS: tuple[str, ...] = ("none", "positive_bar_return")
V3_STOP_ATRS: tuple[str, ...] = ("none", "1.0", "1.5", "2.0", "2.5")


class MeanReversionV3Config(FrozenModel):
    symbol: str
    timeframe: Timeframe = "15min"
    mean_type: MeanType = "sma"
    mean_lookback: Literal[5, 12, 40] = 12
    std_lookback: Literal[10, 20, 40, 80] = 20
    entry_z: Literal[-1.5, -2.0, -2.5, -3.0] = -2.0
    exit_z: Literal[-1.0, -0.5, 0.0, 0.5] = 0.0
    max_holding_bars: Literal[5, 10, 16, 30] = 10
    entry_confirmation: Literal["none", "positive_bar_return"] = "none"
    stop_atr_multiple: Literal["none", "1.0", "1.5", "2.0", "2.5"] = "none"

    @property
    def max_hold(self) -> int:
        return self.max_holding_bars

    @property
    def trend_filter(self) -> str:
        return "none"

    @property
    def stop_atr_value(self) -> float | None:
        return None if self.stop_atr_multiple == "none" else float(self.stop_atr_multiple)


# --- v5 parameter space (futures, 41,472 variants per symbol) -----------------------------
# Same rules as v3 with finer average / volatility lengths (v3's 5/12/40 and
# 10/20/40/80 left gaps around the region the survivors used).
V5_MEAN_LOOKBACKS: tuple[int, ...] = (20, 30, 40, 50, 60, 80)
V5_STD_LOOKBACKS: tuple[int, ...] = (10, 15, 20, 25, 30, 40, 60, 80)
V5_ENTRY_ZS: tuple[float, ...] = (-2.0, -2.5, -3.0)
V5_EXIT_ZS: tuple[float, ...] = (-1.0, -0.5, 0.0, 0.5)
V5_MAX_HOLDS: tuple[int, ...] = (5, 10)
V5_ENTRY_CONFIRMATIONS: tuple[str, ...] = ("none", "positive_bar_return")
V5_STOP_ATRS: tuple[str, ...] = ("none", "1.0", "2.0")


class MeanReversionV5Config(MeanReversionV3Config):
    mean_lookback: Literal[20, 30, 40, 50, 60, 80] = 40
    std_lookback: Literal[10, 15, 20, 25, 30, 40, 60, 80] = 20
    entry_z: Literal[-2.0, -2.5, -3.0] = -2.5
    max_holding_bars: Literal[5, 10] = 5
    stop_atr_multiple: Literal["none", "1.0", "2.0"] = "none"


# --- v6 parameter space (NQ zoom, 21,600 variants per symbol) ------------------------------
# Narrowed around the NQ v5 survivors: short volatility lengths, average 20-50,
# deeper entries, up-bar confirmation only, stop none / 1.5 x ATR.
V6_MEAN_LOOKBACKS: tuple[int, ...] = (20, 25, 30, 40, 50)
V6_STD_LOOKBACKS: tuple[int, ...] = (5, 8, 10, 15, 20, 25)
V6_ENTRY_ZS: tuple[float, ...] = (-2.0, -2.5, -3.0, -3.5)
V6_EXIT_ZS: tuple[float, ...] = (-1.25, -1.0, -0.5, 0.0, 0.5)
V6_MAX_HOLDS: tuple[int, ...] = (3, 5, 10)
V6_ENTRY_CONFIRMATIONS: tuple[str, ...] = ("positive_bar_return",)
V6_STOP_ATRS: tuple[str, ...] = ("none", "1.5")


class MeanReversionV6Config(MeanReversionV3Config):
    mean_lookback: Literal[20, 25, 30, 40, 50] = 30
    std_lookback: Literal[5, 8, 10, 15, 20, 25] = 10
    entry_z: Literal[-2.0, -2.5, -3.0, -3.5] = -2.0
    exit_z: Literal[-1.25, -1.0, -0.5, 0.0, 0.5] = 0.0
    max_holding_bars: Literal[3, 5, 10] = 5
    entry_confirmation: Literal["positive_bar_return"] = "positive_bar_return"
    stop_atr_multiple: Literal["none", "1.5"] = "none"


# --- v7 parameter space (YM round 2, 72,000 variants per symbol) ---------------------------
# 15min / 1h only, longer averages (to 100), short volatility lengths, wider entry,
# exit, hold and stop ranges, confirmation on/off.
V7_TIMEFRAMES: tuple[str, ...] = ("15min", "1h")
V7_MEAN_LOOKBACKS: tuple[int, ...] = (20, 30, 40, 50, 80, 100)
V7_STD_LOOKBACKS: tuple[int, ...] = (10, 15, 20, 25)
V7_ENTRY_ZS: tuple[float, ...] = (-1.75, -2.0, -2.5, -3.0, -3.5)
V7_EXIT_ZS: tuple[float, ...] = (-1.0, -0.5, 0.0, 0.5, 1.0)
V7_MAX_HOLDS: tuple[int, ...] = (5, 10, 15)
V7_ENTRY_CONFIRMATIONS: tuple[str, ...] = ("none", "positive_bar_return")
V7_STOP_ATRS: tuple[str, ...] = ("none", "0.75", "1.0", "1.5", "2.0")


class MeanReversionV7Config(MeanReversionV3Config):
    timeframe: Literal["15min", "1h"] = "1h"
    mean_lookback: Literal[20, 30, 40, 50, 80, 100] = 50
    std_lookback: Literal[10, 15, 20, 25] = 20
    entry_z: Literal[-1.75, -2.0, -2.5, -3.0, -3.5] = -2.0
    exit_z: Literal[-1.0, -0.5, 0.0, 0.5, 1.0] = 0.0
    max_holding_bars: Literal[5, 10, 15] = 10
    stop_atr_multiple: Literal["none", "0.75", "1.0", "1.5", "2.0"] = "none"


# --- v8 parameter space (RTY round 2, 84,672 variants per symbol) --------------------------
# 15min / 1h only, averages to 100, short AND long volatility lengths (10-20, 60-120),
# deeper entries (to -4), exits -1.25..1, short holds (3/5/8), confirmation on/off.
V8_TIMEFRAMES: tuple[str, ...] = ("15min", "1h")
V8_MEAN_LOOKBACKS: tuple[int, ...] = (20, 30, 40, 50, 60, 80, 100)
V8_STD_LOOKBACKS: tuple[int, ...] = (10, 15, 20, 60, 80, 100, 120)
V8_ENTRY_ZS: tuple[float, ...] = (-2.5, -3.0, -3.5, -4.0)
V8_EXIT_ZS: tuple[float, ...] = (-1.25, -1.0, -0.5, 0.0, 0.5, 1.0)
V8_MAX_HOLDS: tuple[int, ...] = (3, 5, 8)
V8_ENTRY_CONFIRMATIONS: tuple[str, ...] = ("none", "positive_bar_return")
V8_STOP_ATRS: tuple[str, ...] = ("none", "1.0", "2.0")


class MeanReversionV8Config(MeanReversionV3Config):
    timeframe: Literal["15min", "1h"] = "1h"
    mean_lookback: Literal[20, 30, 40, 50, 60, 80, 100] = 50
    std_lookback: Literal[10, 15, 20, 60, 80, 100, 120] = 20
    entry_z: Literal[-2.5, -3.0, -3.5, -4.0] = -2.5
    exit_z: Literal[-1.25, -1.0, -0.5, 0.0, 0.5, 1.0] = 0.0
    max_holding_bars: Literal[3, 5, 8] = 5
    stop_atr_multiple: Literal["none", "1.0", "2.0"] = "none"


# --- v9 parameter space (CL round 2, 17,280 variants per symbol) ---------------------------
# 15min only, averages 30-100, volatility 10-30, entries -2..-3.5, short holds (3/5/8).
V9_TIMEFRAMES: tuple[str, ...] = ("15min",)
V9_MEAN_LOOKBACKS: tuple[int, ...] = (30, 40, 50, 60, 80, 100)
V9_STD_LOOKBACKS: tuple[int, ...] = (10, 15, 20, 25, 30)
V9_ENTRY_ZS: tuple[float, ...] = (-2.0, -2.5, -3.0, -3.5)
V9_EXIT_ZS: tuple[float, ...] = (-1.0, -0.5, 0.0, 0.5)
V9_MAX_HOLDS: tuple[int, ...] = (3, 5, 8)
V9_ENTRY_CONFIRMATIONS: tuple[str, ...] = ("none", "positive_bar_return")
V9_STOP_ATRS: tuple[str, ...] = ("none", "1.0", "2.0")


class MeanReversionV9Config(MeanReversionV3Config):
    timeframe: Literal["15min"] = "15min"
    mean_lookback: Literal[30, 40, 50, 60, 80, 100] = 40
    std_lookback: Literal[10, 15, 20, 25, 30] = 20
    entry_z: Literal[-2.0, -2.5, -3.0, -3.5] = -2.0
    exit_z: Literal[-1.0, -0.5, 0.0, 0.5] = 0.0
    max_holding_bars: Literal[3, 5, 8] = 5
    stop_atr_multiple: Literal["none", "1.0", "2.0"] = "none"


# --- v10 parameter space (ES final round, 15min (864 variants per symbol)) ---------------------------
# 15min only: averages 32-57 and volatility 12-27 in steps around the 15min stable region,
# entry -2.5/-3, exit -1/0, hold 3/5/7, up-bar confirmation, no stop.
V10_TIMEFRAMES: tuple[str, ...] = ("15min",)
V10_MEAN_LOOKBACKS: tuple[int, ...] = (32, 37, 42, 47, 52, 57)
V10_STD_LOOKBACKS: tuple[int, ...] = (12, 15, 18, 21, 24, 27)
V10_ENTRY_ZS: tuple[float, ...] = (-2.5, -3.0)
V10_EXIT_ZS: tuple[float, ...] = (-1.0, 0.0)
V10_MAX_HOLDS: tuple[int, ...] = (3, 5, 7)
V10_ENTRY_CONFIRMATIONS: tuple[str, ...] = ("positive_bar_return",)
V10_STOP_ATRS: tuple[str, ...] = ("none",)


class MeanReversionV10Config(MeanReversionV3Config):
    timeframe: Literal["15min"] = "15min"
    mean_lookback: Literal[32, 37, 42, 47, 52, 57] = 32
    std_lookback: Literal[12, 15, 18, 21, 24, 27] = 12
    entry_z: Literal[-2.5, -3.0] = -2.5
    exit_z: Literal[-1.0, 0.0] = -1.0
    max_holding_bars: Literal[3, 5, 7] = 3
    entry_confirmation: Literal["positive_bar_return"] = "positive_bar_return"
    stop_atr_multiple: Literal["none"] = "none"


# --- v11 parameter space (ES final round, 1h (6,804 variants per symbol)) ---------------------------
# 1h SMA only: averages 28-46 and 80-100, volatility 12-22 and 80-100 (the two 1h
# stable clusters), entry -1.5..-2.5, exit -1..0, hold 3/5/8, confirmation on/off, stop none/1/2 ATR.
V11_TIMEFRAMES: tuple[str, ...] = ("1h",)
V11_MEAN_LOOKBACKS: tuple[int, ...] = (28, 34, 40, 46, 80, 90, 100)
V11_STD_LOOKBACKS: tuple[int, ...] = (12, 17, 22, 80, 90, 100)
V11_ENTRY_ZS: tuple[float, ...] = (-1.5, -2.0, -2.5)
V11_EXIT_ZS: tuple[float, ...] = (-1.0, -0.5, 0.0)
V11_MAX_HOLDS: tuple[int, ...] = (3, 5, 8)
V11_ENTRY_CONFIRMATIONS: tuple[str, ...] = ("none", "positive_bar_return")
V11_STOP_ATRS: tuple[str, ...] = ("none", "1.0", "2.0")
V11_MEAN_TYPES: tuple[str, ...] = ("sma",)


class MeanReversionV11Config(MeanReversionV3Config):
    timeframe: Literal["1h"] = "1h"
    mean_type: Literal["sma"] = "sma"
    mean_lookback: Literal[28, 34, 40, 46, 80, 90, 100] = 28
    std_lookback: Literal[12, 17, 22, 80, 90, 100] = 12
    entry_z: Literal[-1.5, -2.0, -2.5] = -1.5
    exit_z: Literal[-1.0, -0.5, 0.0] = -1.0
    max_holding_bars: Literal[3, 5, 8] = 3
    entry_confirmation: Literal["none", "positive_bar_return"] = "none"
    stop_atr_multiple: Literal["none", "1.0", "2.0"] = "none"


# --- v12 parameter space (NQ final round, 15min (1,152 variants per symbol)) ------------------------
# 15min only, specified by the user: SMA/EMA, averages 40-90, volatility 18-43 in steps of 5 plus 60/80,
# entry -2.5/-3/-3.5, exit -1/-0.5, hold 3/5, up-bar confirmation, no stop.
V12_TIMEFRAMES: tuple[str, ...] = ("15min",)
V12_MEAN_TYPES: tuple[str, ...] = ("sma", "ema")
V12_MEAN_LOOKBACKS: tuple[int, ...] = (40, 50, 60, 70, 80, 90)
V12_STD_LOOKBACKS: tuple[int, ...] = (18, 23, 28, 33, 38, 43, 60, 80)
V12_ENTRY_ZS: tuple[float, ...] = (-2.5, -3.0, -3.5)
V12_EXIT_ZS: tuple[float, ...] = (-1.0, -0.5)
V12_MAX_HOLDS: tuple[int, ...] = (3, 5)
V12_ENTRY_CONFIRMATIONS: tuple[str, ...] = ("positive_bar_return",)
V12_STOP_ATRS: tuple[str, ...] = ("none",)


class MeanReversionV12Config(MeanReversionV3Config):
    timeframe: Literal["15min"] = "15min"
    mean_lookback: Literal[40, 50, 60, 70, 80, 90] = 40
    std_lookback: Literal[18, 23, 28, 33, 38, 43, 60, 80] = 18
    entry_z: Literal[-2.5, -3.0, -3.5] = -2.5
    exit_z: Literal[-1.0, -0.5] = -1.0
    max_holding_bars: Literal[3, 5] = 3
    entry_confirmation: Literal["positive_bar_return"] = "positive_bar_return"
    stop_atr_multiple: Literal["none"] = "none"


# --- v13 parameter space (NQ final round, 1h (3,456 variants per symbol)) ---------------------------
# 1h only, specified by the user: SMA/EMA, averages 23/28/32/37, volatility 6-70, entry -2/-2.5/-3,
# exit -1/0, hold 5/8/12, up-bar confirmation, stop none/1.5/2 x ATR.
V13_TIMEFRAMES: tuple[str, ...] = ("1h",)
V13_MEAN_TYPES: tuple[str, ...] = ("sma", "ema")
V13_MEAN_LOOKBACKS: tuple[int, ...] = (23, 28, 32, 37)
V13_STD_LOOKBACKS: tuple[int, ...] = (6, 9, 12, 15, 20, 30, 50, 70)
V13_ENTRY_ZS: tuple[float, ...] = (-2.0, -2.5, -3.0)
V13_EXIT_ZS: tuple[float, ...] = (-1.0, 0.0)
V13_MAX_HOLDS: tuple[int, ...] = (5, 8, 12)
V13_ENTRY_CONFIRMATIONS: tuple[str, ...] = ("positive_bar_return",)
V13_STOP_ATRS: tuple[str, ...] = ("none", "1.5", "2.0")


class MeanReversionV13Config(MeanReversionV3Config):
    timeframe: Literal["1h"] = "1h"
    mean_lookback: Literal[23, 28, 32, 37] = 23
    std_lookback: Literal[6, 9, 12, 15, 20, 30, 50, 70] = 6
    entry_z: Literal[-2.0, -2.5, -3.0] = -2.0
    exit_z: Literal[-1.0, 0.0] = -1.0
    max_holding_bars: Literal[5, 8, 12] = 5
    entry_confirmation: Literal["positive_bar_return"] = "positive_bar_return"
    stop_atr_multiple: Literal["none", "1.5", "2.0"] = "none"


# --- v14 parameter space (YM final round, 15min (17,280 variants per symbol)) ----------------------
# 15min only, specified by the user: SMA/EMA, averages 32-52 in steps of 5, volatility 12-27 in steps
# of 5 plus 50/75, entry -2.5 to -4, exit -1.5/-1/0, hold 3/5/8/12, confirmation none/up, stop none/1.3/1.8.
V14_TIMEFRAMES: tuple[str, ...] = ("15min",)
V14_MEAN_TYPES: tuple[str, ...] = ("sma", "ema")
V14_MEAN_LOOKBACKS: tuple[int, ...] = (32, 37, 42, 47, 52)
V14_STD_LOOKBACKS: tuple[int, ...] = (12, 17, 22, 27, 50, 75)
V14_ENTRY_ZS: tuple[float, ...] = (-2.5, -3.0, -3.5, -4.0)
V14_EXIT_ZS: tuple[float, ...] = (-1.5, -1.0, 0.0)
V14_MAX_HOLDS: tuple[int, ...] = (3, 5, 8, 12)
V14_ENTRY_CONFIRMATIONS: tuple[str, ...] = ("none", "positive_bar_return")
V14_STOP_ATRS: tuple[str, ...] = ("none", "1.3", "1.8")


class MeanReversionV14Config(MeanReversionV3Config):
    timeframe: Literal["15min"] = "15min"
    mean_lookback: Literal[32, 37, 42, 47, 52] = 32
    std_lookback: Literal[12, 17, 22, 27, 50, 75] = 12
    entry_z: Literal[-2.5, -3.0, -3.5, -4.0] = -2.5
    exit_z: Literal[-1.5, -1.0, 0.0] = -1.0
    max_holding_bars: Literal[3, 5, 8, 12] = 3
    entry_confirmation: Literal["none", "positive_bar_return"] = "none"
    stop_atr_multiple: Literal["none", "1.3", "1.8"] = "none"


# --- v15 parameter space (YM final round, 1h (23,328 variants per symbol)) -------------------------
# 1h only, specified by the user: SMA/EMA, averages 15-45 in steps of 10 plus 75-115, volatility
# 12/17/22/50/60/80, entry -1.5/-2/-2.5, exit -1/-0.5/0, hold 3/5/8/12, confirmation none/up,
# stop none/0.75/1.5 x ATR.
V15_TIMEFRAMES: tuple[str, ...] = ("1h",)
V15_MEAN_TYPES: tuple[str, ...] = ("sma", "ema")
V15_MEAN_LOOKBACKS: tuple[int, ...] = (15, 25, 35, 45, 75, 85, 95, 105, 115)
V15_STD_LOOKBACKS: tuple[int, ...] = (12, 17, 22, 50, 60, 80)
V15_ENTRY_ZS: tuple[float, ...] = (-1.5, -2.0, -2.5)
V15_EXIT_ZS: tuple[float, ...] = (-1.0, -0.5, 0.0)
V15_MAX_HOLDS: tuple[int, ...] = (3, 5, 8, 12)
V15_ENTRY_CONFIRMATIONS: tuple[str, ...] = ("none", "positive_bar_return")
V15_STOP_ATRS: tuple[str, ...] = ("none", "0.75", "1.5")


class MeanReversionV15Config(MeanReversionV3Config):
    timeframe: Literal["1h"] = "1h"
    mean_lookback: Literal[15, 25, 35, 45, 75, 85, 95, 105, 115] = 15
    std_lookback: Literal[12, 17, 22, 50, 60, 80] = 12
    entry_z: Literal[-1.5, -2.0, -2.5] = -1.5
    exit_z: Literal[-1.0, -0.5, 0.0] = -1.0
    max_holding_bars: Literal[3, 5, 8, 12] = 3
    entry_confirmation: Literal["none", "positive_bar_return"] = "none"
    stop_atr_multiple: Literal["none", "0.75", "1.5"] = "none"


# --- v16 parameter space (RTY final round, 15min (13,608 variants per symbol)) ---------------------
# 15min only, specified by the user: SMA/EMA, averages 35-115 in steps of 10, volatility 15 and 55-105 in steps
# of 10, entry -2/-2.5/-3, exit -1/0/+1, hold 3/5/8, confirmation none/up, stop none/1.5 x ATR.
V16_TIMEFRAMES: tuple[str, ...] = ("15min",)
V16_MEAN_TYPES: tuple[str, ...] = ("sma", "ema")
V16_MEAN_LOOKBACKS: tuple[int, ...] = (35, 45, 55, 65, 75, 85, 95, 105, 115)
V16_STD_LOOKBACKS: tuple[int, ...] = (15, 55, 65, 75, 85, 95, 105)
V16_ENTRY_ZS: tuple[float, ...] = (-2.0, -2.5, -3.0)
V16_EXIT_ZS: tuple[float, ...] = (-1.0, 0.0, 1.0)
V16_MAX_HOLDS: tuple[int, ...] = (3, 5, 8)
V16_ENTRY_CONFIRMATIONS: tuple[str, ...] = ("none", "positive_bar_return")
V16_STOP_ATRS: tuple[str, ...] = ("none", "1.5")


class MeanReversionV16Config(MeanReversionV3Config):
    timeframe: Literal["15min"] = "15min"
    mean_lookback: Literal[35, 45, 55, 65, 75, 85, 95, 105, 115] = 35
    std_lookback: Literal[15, 55, 65, 75, 85, 95, 105] = 15
    entry_z: Literal[-2.0, -2.5, -3.0] = -2.0
    exit_z: Literal[-1.0, 0.0, 1.0] = -1.0
    max_holding_bars: Literal[3, 5, 8] = 3
    entry_confirmation: Literal["none", "positive_bar_return"] = "none"
    stop_atr_multiple: Literal["none", "1.5"] = "none"


# --- v17 parameter space (RTY final round, 1h (8,640 variants per symbol)) ---------------------
# 1h only, specified by the user: SMA/EMA, averages 70-120 in steps of 10, volatility 10/12/15/18/20,
# entry -2.5/-3, exit -1/0/+1, hold 5/8/12, confirmation none/up, stop none/1.5/2/2.5 x ATR.
V17_TIMEFRAMES: tuple[str, ...] = ("1h",)
V17_MEAN_TYPES: tuple[str, ...] = ("sma", "ema")
V17_MEAN_LOOKBACKS: tuple[int, ...] = (70, 80, 90, 100, 110, 120)
V17_STD_LOOKBACKS: tuple[int, ...] = (10, 12, 15, 18, 20)
V17_ENTRY_ZS: tuple[float, ...] = (-2.5, -3.0)
V17_EXIT_ZS: tuple[float, ...] = (-1.0, 0.0, 1.0)
V17_MAX_HOLDS: tuple[int, ...] = (5, 8, 12)
V17_ENTRY_CONFIRMATIONS: tuple[str, ...] = ("none", "positive_bar_return")
V17_STOP_ATRS: tuple[str, ...] = ("none", "1.5", "2.0", "2.5")


class MeanReversionV17Config(MeanReversionV3Config):
    timeframe: Literal["1h"] = "1h"
    mean_lookback: Literal[70, 80, 90, 100, 110, 120] = 70
    std_lookback: Literal[10, 12, 15, 18, 20] = 10
    entry_z: Literal[-2.5, -3.0] = -2.5
    exit_z: Literal[-1.0, 0.0, 1.0] = -1.0
    max_holding_bars: Literal[5, 8, 12] = 5
    entry_confirmation: Literal["none", "positive_bar_return"] = "none"
    stop_atr_multiple: Literal["none", "1.5", "2.0", "2.5"] = "none"


# --- v21 parameter space (6E round 2, 1h (24,000 variants per symbol)) -------------------------
# 1h only, specified by the user after reading 6E v5: SMA/EMA, averages 60/70/80/90/100/120,
# volatility 6/8/10/12/15, entry -1.5/-1.75/-2/-2.25/-2.5, exit -1/-0.5/0/+0.5,
# hold 3/4/5/6/8, no confirmation, stop none/1.5/2/2.5 x ATR.
V21_TIMEFRAMES: tuple[str, ...] = ("1h",)
V21_MEAN_TYPES: tuple[str, ...] = ("sma", "ema")
V21_MEAN_LOOKBACKS: tuple[int, ...] = (60, 70, 80, 90, 100, 120)
V21_STD_LOOKBACKS: tuple[int, ...] = (6, 8, 10, 12, 15)
V21_ENTRY_ZS: tuple[float, ...] = (-1.5, -1.75, -2.0, -2.25, -2.5)
V21_EXIT_ZS: tuple[float, ...] = (-1.0, -0.5, 0.0, 0.5)
V21_MAX_HOLDS: tuple[int, ...] = (3, 4, 5, 6, 8)
V21_ENTRY_CONFIRMATIONS: tuple[str, ...] = ("none",)
V21_STOP_ATRS: tuple[str, ...] = ("none", "1.5", "2.0", "2.5")


class MeanReversionV21Config(MeanReversionV3Config):
    timeframe: Literal["1h"] = "1h"
    mean_lookback: Literal[60, 70, 80, 90, 100, 120] = 60
    std_lookback: Literal[6, 8, 10, 12, 15] = 6
    entry_z: Literal[-1.5, -1.75, -2.0, -2.25, -2.5] = -2.0
    exit_z: Literal[-1.0, -0.5, 0.0, 0.5] = -1.0
    max_holding_bars: Literal[3, 4, 5, 6, 8] = 5
    entry_confirmation: Literal["none"] = "none"
    stop_atr_multiple: Literal["none", "1.5", "2.0", "2.5"] = "none"
