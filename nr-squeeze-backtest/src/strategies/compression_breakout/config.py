"""Typed configs + ablation axes for the intraday volatility-compression breakout strategies.

Volatility clusters: quiet stretches tend to end in a sharp move whose direction the quiet
itself does not reveal. Compression decides WHEN (the market has gone unusually quiet),
the breakout decides WHICH WAY (the side price escapes the compression box on). Every
position is flat by the session close.

Each compression type is its own strategy line, with its own parameter space and its own
rounds (v1, v2, ...); they share one backtester (backtest.py):
  compression_breakout_bbkc : TTM-style squeeze -- Bollinger Bands (SMA(L) -/+ 2 sd(L) of
         closes) sit inside the Keltner Channel (SMA(L) -/+ kc_mult x ATR(L)). Same centre, so
         "inside" is 2 x sd(L) < kc_mult x ATR(L). Must hold for at least min_squeeze_bars
         bars in a row.
  compression_breakout_nr   : NR-N (Crabel) -- the bar's high-low range is the narrowest of
         the last nr_lookback bars (itself included; ties count as narrowest).
The box is the high / low of the run of consecutive compression bars.

Shared axes (every line, 1,152 combinations in v1):
  timeframe         : 5min, 15min
  entry_type        : close                 (decided at a bar close beyond the box, filled at
                                             the next bar's open)
                      wick                  (stop order resting at the box edge: filled intrabar
                                             at the worse of the bar's open and the edge)
  setup_expiry_bars : 3, 6                  (bars after the last compression bar the box stays live)
  stop              : box                   (the far side of the box)
                      1.0, 2.0              (entry price -/+ that many ATR(14), known before the fill)
  target_r          : 1.0, 2.0, 3.0, none   (take profit at entry + target_r x the stop distance;
                                             none = stop or session close only)
  direction         : long, short, both
  trend_filter      : none                  (any breakout)
                      ema50                 (long only above EMA(50) of closes, short only below)
  min_box_atr       : 0.0, 0.5              (the box must be at least this x ATR(14) wide, ATR at
                                             the box's last bar; 0 = any box. Small boxes make
                                             R so small that costs dominate)

Squeeze v1 (20,736 variants per symbol) adds:
  squeeze_length    : 10, 20, 30            (BB / KC length L, in bars)
  kc_mult           : 1.0, 1.5, 2.0         (Keltner width in ATR(L))
  min_squeeze_bars  : 1, 4                  (squeeze bars in a row before the box counts)
NR v1 (16,128 variants per symbol) adds:
  nr_lookback       : 3, 4, 5, 7, 10, 14, 20 (N of NR-N)
  inside_bar        : False, True           (True: the NR bar must also be an inside bar, its
                                             high <= the previous bar's high and its low >= the
                                             previous bar's low -- Crabel's NR4/ID)

Fixed in v1: BB width 2 sd, no new entries in the last 30 minutes before the session close.
"""

from __future__ import annotations

from typing import Literal

from src.utils.config_models import FrozenModel

# Shared axes.
TIMEFRAMES: tuple[str, ...] = ("5min", "15min")
ENTRY_TYPES: tuple[str, ...] = ("close", "wick")
SETUP_EXPIRIES: tuple[int, ...] = (3, 6)
STOPS: tuple[str, ...] = ("box", "1.0", "2.0")
TARGETS: tuple[str, ...] = ("1.0", "2.0", "3.0", "none")
DIRECTIONS: tuple[str, ...] = ("long", "short", "both")
TREND_FILTERS: tuple[str, ...] = ("none", "ema50")
MIN_BOX_ATRS: tuple[float, ...] = (0.0, 0.5)

# Squeeze (BB inside KC) axes.
SQUEEZE_LENGTHS: tuple[int, ...] = (10, 20, 30)
KC_MULTS: tuple[float, ...] = (1.0, 1.5, 2.0)
MIN_SQUEEZE_BARS: tuple[int, ...] = (1, 4)

# NR-N axes.
NR_LOOKBACKS: tuple[int, ...] = (3, 4, 5, 7, 10, 14, 20)
INSIDE_BARS: tuple[bool, ...] = (False, True)

BB_STD = 2.0
LAST_ENTRY_CUTOFF_MINUTES = 30
TREND_EMA = 50
ATR_PERIOD = 14


def trend_ema_span(trend_filter: str) -> int | None:
    """EMA length of a trend filter ("none" -> None, "ema50" -> 50, ...)."""
    if trend_filter == "none":
        return None
    if trend_filter.startswith("ema") and trend_filter[3:].isdigit() and int(trend_filter[3:]) >= 2:
        return int(trend_filter[3:])
    raise ValueError(f"Unknown trend_filter {trend_filter!r}")


class _BreakoutConfig(FrozenModel):
    """Settings every compression line shares."""

    symbol: str
    timeframe: Literal["5min", "15min"] = "15min"
    entry_type: Literal["close", "wick"] = "close"
    setup_expiry_bars: Literal[3, 6] = 3
    stop: Literal["box", "1.0", "2.0"] = "box"
    target_r: Literal["1.0", "2.0", "3.0", "none"] = "2.0"
    direction: Literal["long", "short", "both"] = "both"
    trend_filter: Literal["none", "ema50"] = "none"
    min_box_atr: Literal[0.0, 0.5] = 0.0

    @property
    def stop_atr_value(self) -> float | None:
        """ATR multiple of the stop, or None for the box stop."""
        return None if self.stop == "box" else float(self.stop)

    @property
    def target_r_value(self) -> float | None:
        return None if self.target_r == "none" else float(self.target_r)


# --- compression_breakout_bbkc v1 (20,736 variants per symbol) ------------------------------

class SqueezeBreakoutConfig(_BreakoutConfig):
    compression: Literal["bbkc"] = "bbkc"
    squeeze_length: Literal[10, 20, 30] = 20
    kc_mult: Literal[1.0, 1.5, 2.0] = 1.5
    min_squeeze_bars: Literal[1, 4] = 1


# --- compression_breakout_nr v1 (16,128 variants per symbol) -------------------------------

class NRBreakoutConfig(_BreakoutConfig):
    compression: Literal["nr"] = "nr"
    nr_lookback: Literal[3, 4, 5, 7, 10, 14, 20] = 7
    inside_bar: bool = False


# --- compression_breakout_bbkc v2 (ES round 2; one grid per bar size) ------------------------
# Specified by the user after reading ES v1's development AND validation results
# (cb_bbkc_es_v1). Each bar size gets its own grid, so v2 is two runs (15m: 184,320 configs;
# 5m: 72,576). The 5m grid was re-specified after ES v2 15m's development and validation
# results (cb_bbkc_es_v2_15m); the first 5m draft (230,400 configs, squeeze 1/3/5/8/12) was
# stopped during its development backtests, before any result was computed. Squeeze lengths
# above a session's 78 five-minute bars reach back into earlier sessions (indicators run over
# consecutive day-session bars, as everywhere in this backtester).
V2_5M_SQUEEZE_LENGTHS: tuple[int, ...] = (3, 8, 12, 20, 40, 60, 80)
V2_5M_KC_MULTS: tuple[float, ...] = (0.5, 1.0, 1.3, 1.7, 2.0, 2.5)
V2_5M_MIN_SQUEEZE_BARS: tuple[int, ...] = (1, 4, 10)
V2_5M_ENTRY_TYPES: tuple[str, ...] = ("wick",)
V2_5M_SETUP_EXPIRIES: tuple[int, ...] = (1, 3, 8)
V2_SETUP_EXPIRIES: tuple[int, ...] = (1, 3, 6, 9)  # 15m
V2_5M_STOPS: tuple[str, ...] = ("box", "1.0", "2.0", "3.0")
V2_5M_TARGETS: tuple[str, ...] = ("2.0", "3.0", "4.0", "none")
V2_DIRECTIONS: tuple[str, ...] = ("long", "both")
V2_5M_MIN_BOX_ATRS: tuple[float, ...] = (0.0, 0.3, 0.8)

V2_15M_SQUEEZE_LENGTHS: tuple[int, ...] = (5, 10, 15, 20, 25, 30, 40, 50)
V2_15M_KC_MULTS: tuple[float, ...] = (1.0, 1.5, 2.0, 2.5, 3.0)
V2_15M_MIN_SQUEEZE_BARS: tuple[int, ...] = (1, 3, 5)
V2_15M_STOPS: tuple[str, ...] = ("box", "1.5", "2.5", "3.5")
V2_15M_TARGETS: tuple[str, ...] = ("2.0", "3.0", "4.0", "none")
V2_15M_MIN_BOX_ATRS: tuple[float, ...] = (0.0, 0.5, 1.0)


class SqueezeBreakoutV2_5mConfig(_BreakoutConfig):
    timeframe: Literal["5min"] = "5min"
    compression: Literal["bbkc"] = "bbkc"
    squeeze_length: Literal[3, 8, 12, 20, 40, 60, 80] = 20
    kc_mult: Literal[0.5, 1.0, 1.3, 1.7, 2.0, 2.5] = 1.7
    min_squeeze_bars: Literal[1, 4, 10] = 1
    entry_type: Literal["wick"] = "wick"
    setup_expiry_bars: Literal[1, 3, 8] = 3
    stop: Literal["box", "1.0", "2.0", "3.0"] = "box"
    target_r: Literal["2.0", "3.0", "4.0", "none"] = "2.0"
    direction: Literal["long", "both"] = "both"
    min_box_atr: Literal[0.0, 0.3, 0.8] = 0.0


class SqueezeBreakoutV2_15mConfig(_BreakoutConfig):
    timeframe: Literal["15min"] = "15min"
    compression: Literal["bbkc"] = "bbkc"
    squeeze_length: Literal[5, 10, 15, 20, 25, 30, 40, 50] = 10
    kc_mult: Literal[1.0, 1.5, 2.0, 2.5, 3.0] = 2.0
    min_squeeze_bars: Literal[1, 3, 5] = 1
    setup_expiry_bars: Literal[1, 3, 6, 9] = 3
    stop: Literal["box", "1.5", "2.5", "3.5"] = "box"
    target_r: Literal["2.0", "3.0", "4.0", "none"] = "2.0"
    direction: Literal["long", "both"] = "both"
    min_box_atr: Literal[0.0, 0.5, 1.0] = 0.0


# --- compression_breakout_bbkc v3 (NQ; one grid per bar size) ---------------------------------
# Specified by the user (2026-11-11) after reading ES v2's development, validation and holdout
# results (cb_bbkc_es_v2_5m / _15m); first squeeze round run on NQ. Two runs again (5m: 27,648
# configs, wick entry only; 15m: 28,800). Squeeze length 1 makes (almost) every bar a squeeze
# bar, so its box is the session's range so far.
V3_5M_SQUEEZE_LENGTHS: tuple[int, ...] = (1, 3, 5, 10, 15, 30)
V3_5M_KC_MULTS: tuple[float, ...] = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0)
V3_5M_MIN_SQUEEZE_BARS: tuple[int, ...] = (1, 4)
V3_5M_ENTRY_TYPES: tuple[str, ...] = ("wick",)
V3_5M_SETUP_EXPIRIES: tuple[int, ...] = (1, 3, 10)
V3_5M_STOPS: tuple[str, ...] = ("box", "1.0", "2.0", "3.0")
V3_5M_TARGETS: tuple[str, ...] = ("2.0", "3.0", "4.0", "none")
V3_DIRECTIONS: tuple[str, ...] = ("long", "both")
V3_MIN_BOX_ATRS: tuple[float, ...] = (0.0, 0.5)

V3_15M_SQUEEZE_LENGTHS: tuple[int, ...] = (5, 15, 30, 50, 70)
V3_15M_KC_MULTS: tuple[float, ...] = (1.0, 1.5, 2.0, 2.5, 3.0)
V3_15M_MIN_SQUEEZE_BARS: tuple[int, ...] = (1, 3)
V3_15M_SETUP_EXPIRIES: tuple[int, ...] = (1, 3, 7)
V3_15M_STOPS: tuple[str, ...] = ("box", "1.0", "2.0")
V3_15M_TARGETS: tuple[str, ...] = ("1.5", "2.5", "3.0", "none")


class SqueezeBreakoutV3_5mConfig(_BreakoutConfig):
    timeframe: Literal["5min"] = "5min"
    compression: Literal["bbkc"] = "bbkc"
    squeeze_length: Literal[1, 3, 5, 10, 15, 30] = 10
    kc_mult: Literal[0.5, 1.0, 1.5, 2.0, 2.5, 3.0] = 1.5
    min_squeeze_bars: Literal[1, 4] = 1
    entry_type: Literal["wick"] = "wick"
    setup_expiry_bars: Literal[1, 3, 10] = 3
    stop: Literal["box", "1.0", "2.0", "3.0"] = "box"
    target_r: Literal["2.0", "3.0", "4.0", "none"] = "2.0"
    direction: Literal["long", "both"] = "both"


class SqueezeBreakoutV3_15mConfig(_BreakoutConfig):
    timeframe: Literal["15min"] = "15min"
    compression: Literal["bbkc"] = "bbkc"
    squeeze_length: Literal[5, 15, 30, 50, 70] = 15
    kc_mult: Literal[1.0, 1.5, 2.0, 2.5, 3.0] = 2.0
    min_squeeze_bars: Literal[1, 3] = 1
    setup_expiry_bars: Literal[1, 3, 7] = 3
    stop: Literal["box", "1.0", "2.0"] = "box"
    target_r: Literal["1.5", "2.5", "3.0", "none"] = "2.5"
    direction: Literal["long", "both"] = "both"


# --- compression_breakout_bbkc v4 (YM; 15-minute bars only) -----------------------------------
# Specified by the user (2026-11-11) after reading the ES v2 and NQ v3 squeeze results
# (development, validation and holdout). First squeeze run on YM. 3,840 configs.
V4_15M_SQUEEZE_LENGTHS: tuple[int, ...] = (15, 25, 35, 45)
V4_15M_KC_MULTS: tuple[float, ...] = (1.5, 2.0, 2.5, 3.0, 3.5)
V4_15M_MIN_SQUEEZE_BARS: tuple[int, ...] = (1, 4)
V4_15M_SETUP_EXPIRIES: tuple[int, ...] = (1, 4)
V4_15M_STOPS: tuple[str, ...] = ("box", "1.5")
V4_15M_TARGETS: tuple[str, ...] = ("1.0", "2.5", "none")
V4_15M_MIN_BOX_ATRS: tuple[float, ...] = (0.0,)


class SqueezeBreakoutV4_15mConfig(_BreakoutConfig):
    timeframe: Literal["15min"] = "15min"
    compression: Literal["bbkc"] = "bbkc"
    squeeze_length: Literal[15, 25, 35, 45] = 25
    kc_mult: Literal[1.5, 2.0, 2.5, 3.0, 3.5] = 2.5
    min_squeeze_bars: Literal[1, 4] = 1
    setup_expiry_bars: Literal[1, 4] = 1
    stop: Literal["box", "1.5"] = "box"
    target_r: Literal["1.0", "2.5", "none"] = "2.5"
    direction: Literal["long", "both"] = "both"
    min_box_atr: Literal[0.0] = 0.0


# --- compression_breakout_nr v2 (15-minute bars only, 207,360 configs) ----------------------
# Specified by the user (2026-11-13) as a wide ~200k NR-N grid on 15-minute bars, before any NR-N
# run had been made (cb_nr_*_v1 was never run). Two axes are new to the NR line:
#   min_nr_bars   : 1 / 2 NR bars in a row before the box counts (2 = a narrowing pair: the
#                   second bar is no wider than the first, as both are the narrowest of N)
#   trend_filter  : EMA length 20 / 50 / 200 bars (or none) instead of EMA(50) only
# NR-2 is "no wider than the previous bar"; NR-30 reaches about one session back on 15m bars.
V2_NR_LOOKBACKS: tuple[int, ...] = (2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 30)
V2_NR_MIN_NR_BARS: tuple[int, ...] = (1, 2)
V2_NR_SETUP_EXPIRIES: tuple[int, ...] = (1, 3, 6)
V2_NR_STOPS: tuple[str, ...] = ("box", "1.0", "1.5", "2.5")
V2_NR_TARGETS: tuple[str, ...] = ("1.0", "2.0", "3.0", "5.0", "none")
V2_NR_TREND_FILTERS: tuple[str, ...] = ("none", "ema20", "ema50", "ema200")
V2_NR_MIN_BOX_ATRS: tuple[float, ...] = (0.0, 0.3, 0.75)


class NRBreakoutV2_15mConfig(_BreakoutConfig):
    timeframe: Literal["15min"] = "15min"
    compression: Literal["nr"] = "nr"
    nr_lookback: Literal[2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 30] = 7
    inside_bar: bool = False
    min_nr_bars: Literal[1, 2] = 1
    setup_expiry_bars: Literal[1, 3, 6] = 3
    stop: Literal["box", "1.0", "1.5", "2.5"] = "box"
    target_r: Literal["1.0", "2.0", "3.0", "5.0", "none"] = "2.0"
    trend_filter: Literal["none", "ema20", "ema50", "ema200"] = "none"
    min_box_atr: Literal[0.0, 0.3, 0.75] = 0.0


# --- compression_breakout_nr v3 (15-minute bars only, 145,152 configs) ----------------------
# Specified by the user (2026-11-13) after reading NR v2's development and validation results
# (cb_nr_es_v2_15m). Two axes are new:
#   max_range_atr : every NR bar must also have high - low <= this x ATR(14) at that bar
#                   ("off" = relative narrowness only). Absolute vs relative quiet.
#   max_hold_bars : time stop -- close at the close of the Nth bar after the entry bar unless
#                   the stop / target / session close came first (0 = no time stop).
# NR-50 / NR-80 reach about two / three sessions back on 15m bars.
V3_NR_LOOKBACKS: tuple[int, ...] = (2, 3, 5, 10, 25, 50, 80)
V3_NR_MIN_NR_BARS: tuple[int, ...] = (1, 2, 4)
V3_NR_SETUP_EXPIRIES: tuple[int, ...] = (1, 3)
V3_NR_STOPS: tuple[str, ...] = ("box", "1.0")
V3_NR_TARGETS: tuple[str, ...] = ("1.0", "2.5", "4.0", "none")
V3_NR_DIRECTIONS: tuple[str, ...] = ("long", "both")
V3_NR_TREND_FILTERS: tuple[str, ...] = ("none", "ema200")
V3_NR_MIN_BOX_ATRS: tuple[float, ...] = (0.0, 0.3, 0.5)
V3_NR_MAX_RANGE_ATRS: tuple[str, ...] = ("off", "0.5", "0.8")
V3_NR_MAX_HOLD_BARS: tuple[int, ...] = (0, 4, 8)


class NRBreakoutV3_15mConfig(_BreakoutConfig):
    timeframe: Literal["15min"] = "15min"
    compression: Literal["nr"] = "nr"
    nr_lookback: Literal[2, 3, 5, 10, 25, 50, 80] = 10
    inside_bar: bool = False
    min_nr_bars: Literal[1, 2, 4] = 1
    setup_expiry_bars: Literal[1, 3] = 1
    stop: Literal["box", "1.0"] = "box"
    target_r: Literal["1.0", "2.5", "4.0", "none"] = "2.5"
    direction: Literal["long", "both"] = "both"
    trend_filter: Literal["none", "ema200"] = "none"
    min_box_atr: Literal[0.0, 0.3, 0.5] = 0.0
    max_range_atr: Literal["off", "0.5", "0.8"] = "off"
    max_hold_bars: Literal[0, 4, 8] = 0

    @property
    def max_range_atr_value(self) -> float | None:
        return None if self.max_range_atr == "off" else float(self.max_range_atr)


# --- compression_breakout_nr v4 (15-minute bars only, 2,304 configs) ------------------------
# Specified by the user (2026-11-13) after reading NR v3 on ES (cb_nr_es_v3_15m), for the
# other markets (NQ, YM first). Wick entry, 1 NR bar, setup live 1 bar and no time stop are
# fixed; the NR range cap is off / 0.5 ATR(14).
V4_NR_LOOKBACKS: tuple[int, ...] = (2, 3, 4, 8, 16, 50)
V4_NR_STOPS: tuple[str, ...] = ("box", "1.0", "1.5")
V4_NR_TARGETS: tuple[str, ...] = ("1.0", "2.0", "3.5", "none")
V4_NR_DIRECTIONS: tuple[str, ...] = ("long", "both")
V4_NR_TREND_FILTERS: tuple[str, ...] = ("none", "ema200")
V4_NR_MIN_BOX_ATRS: tuple[float, ...] = (0.0, 0.3)
V4_NR_MAX_RANGE_ATRS: tuple[str, ...] = ("off", "0.5")


class NRBreakoutV4_15mConfig(_BreakoutConfig):
    timeframe: Literal["15min"] = "15min"
    compression: Literal["nr"] = "nr"
    nr_lookback: Literal[2, 3, 4, 8, 16, 50] = 8
    inside_bar: bool = False
    min_nr_bars: Literal[1] = 1
    entry_type: Literal["wick"] = "wick"
    setup_expiry_bars: Literal[1] = 1
    stop: Literal["box", "1.0", "1.5"] = "box"
    target_r: Literal["1.0", "2.0", "3.5", "none"] = "2.0"
    direction: Literal["long", "both"] = "both"
    trend_filter: Literal["none", "ema200"] = "none"
    min_box_atr: Literal[0.0, 0.3] = 0.0
    max_range_atr: Literal["off", "0.5"] = "off"
    max_hold_bars: Literal[0] = 0

    @property
    def max_range_atr_value(self) -> float | None:
        return None if self.max_range_atr == "off" else float(self.max_range_atr)
