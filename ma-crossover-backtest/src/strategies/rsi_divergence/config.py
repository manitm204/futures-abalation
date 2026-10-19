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


# --- v2 parameter space (rsi_v2) ---------------------------------------------------------
# 2 x 3 x 3 x 1 x 3 x 2 x 3 x 3 x 2 x 3 x 3 x 4 = 69,984 variants per symbol
# (34,992 per timeframe). Three new filters on top of the v1 divergence rule:
#   rsi_extreme       : off, 40/60, 30/70  (the FIRST pivot's RSI must be <= the lower
#                       threshold; the strategy is long-only, so only the bullish side
#                       (lower threshold) applies)
#   adx_filter        : off, lt30, lt20    (ADX(14) at the confirmation close < 30 / < 20)
#   min_price_div_atr : 0, 0.1, 0.25, 0.5  (low_q - low_p >= k x ATR(14) at the second
#                       pivot p; 0 still requires a strictly lower low)
TIMEFRAMES_V2: tuple[str, ...] = ("5min", "15min")
RSI_LOOKBACKS_V2: tuple[int, ...] = (7, 10, 14)
PIVOT_LEFTS_V2: tuple[int, ...] = (3, 5, 8)
PIVOT_RIGHTS_V2: tuple[int, ...] = (1,)
MAX_PIVOT_GAPS_V2: tuple[int, ...] = (8, 12, 24)
MIN_RSI_DIFFS_V2: tuple[float, ...] = (0.0, 5.0)
STOP_ATRS_V2: tuple[float, ...] = (1.5, 2.0, 2.5)
TARGET_RS_V2: tuple[float, ...] = (1.5, 2.0, 3.0)
MAX_HOLDS_V2: tuple[int, ...] = (24, 48)
RSI_EXTREMES_V2: tuple[str, ...] = ("off", "40/60", "30/70")
ADX_FILTERS_V2: tuple[str, ...] = ("off", "lt30", "lt20")
MIN_PRICE_DIVS_V2: tuple[float, ...] = (0.0, 0.1, 0.25, 0.5)

RSI_EXTREME_LOWER: dict[str, float | None] = {"off": None, "40/60": 40.0, "30/70": 30.0}
ADX_MAX: dict[str, float | None] = {"off": None, "lt30": 30.0, "lt20": 20.0}


class RSIDivergenceV2Config(FrozenModel):
    symbol: str
    timeframe: Literal["5min", "15min"] = "15min"
    rsi_lookback: Literal[7, 10, 14] = 14
    pivot_left: Literal[3, 5, 8] = 5
    pivot_right: Literal[1] = 1
    max_pivot_gap: Literal[8, 12, 24] = 12
    min_rsi_diff: Literal[0.0, 5.0] = 0.0
    stop_atr: Literal[1.5, 2.0, 2.5] = 2.0
    target_r: Literal[1.5, 2.0, 3.0] = 2.0
    max_hold: Literal[24, 48] = 24
    rsi_extreme: Literal["off", "40/60", "30/70"] = "off"
    adx_filter: Literal["off", "lt30", "lt20"] = "off"
    min_price_div_atr: Literal[0.0, 0.1, 0.25, 0.5] = 0.0


# --- v3 parameter space (rsi_v3) ---------------------------------------------------------
# 2 x 3 x 2 x 1 x 2 x 2 x 3 x 3 x 3 x 3 x 1 x 2 x 4 x 2 x 4 = 248,832 variants per symbol
# (124,416 per timeframe). Three new rules on top of v2 (long-only, so only the
# long side of each applies):
#   trend_filter       : off, ema20, ema50, ema200  (close at the confirmation bar c
#                        must be ABOVE EMA(n) of closes at c)
#   entry_confirmation : immediate (enter at the open after c) or breakout (a close
#                        above high_c within the next BREAKOUT_BARS bars, entering
#                        at the open after that close; no breakout -> no trade)
#   session_window     : full, excl_first30, excl_last30, excl_first_last30 (the entry
#                        FILL bar may not open in 09:30-10:00 / 15:30-16:00 New York
#                        time; an excluded entry is skipped, not deferred)
TIMEFRAMES_V3: tuple[str, ...] = ("5min", "15min")
RSI_LOOKBACKS_V3: tuple[int, ...] = (7, 10, 14)
PIVOT_LEFTS_V3: tuple[int, ...] = (3, 5)
PIVOT_RIGHTS_V3: tuple[int, ...] = (1,)
MAX_PIVOT_GAPS_V3: tuple[int, ...] = (12, 24)
MIN_RSI_DIFFS_V3: tuple[float, ...] = (0.0, 5.0)
STOP_ATRS_V3: tuple[float, ...] = (1.5, 2.0, 2.5)
TARGET_RS_V3: tuple[float, ...] = (1.5, 2.0, 3.0)
MAX_HOLDS_V3: tuple[int, ...] = (24, 48, 72)
RSI_EXTREMES_V3: tuple[str, ...] = ("off", "40/60", "30/70")
ADX_FILTERS_V3: tuple[str, ...] = ("off",)
MIN_PRICE_DIVS_V3: tuple[float, ...] = (0.0, 0.25)
TREND_FILTERS_V3: tuple[str, ...] = ("off", "ema20", "ema50", "ema200")
ENTRY_CONFIRMATIONS_V3: tuple[str, ...] = ("immediate", "breakout")
SESSION_WINDOWS_V3: tuple[str, ...] = ("full", "excl_first30", "excl_last30", "excl_first_last30")

BREAKOUT_BARS = 3
TREND_EMA: dict[str, int | None] = {"off": None, "ema20": 20, "ema50": 50, "ema200": 200}


class RSIDivergenceV3Config(FrozenModel):
    symbol: str
    timeframe: Literal["5min", "15min"] = "15min"
    rsi_lookback: Literal[7, 10, 14] = 14
    pivot_left: Literal[3, 5] = 5
    pivot_right: Literal[1] = 1
    max_pivot_gap: Literal[12, 24] = 12
    min_rsi_diff: Literal[0.0, 5.0] = 0.0
    stop_atr: Literal[1.5, 2.0, 2.5] = 2.0
    target_r: Literal[1.5, 2.0, 3.0] = 2.0
    max_hold: Literal[24, 48, 72] = 48
    rsi_extreme: Literal["off", "40/60", "30/70"] = "off"
    adx_filter: Literal["off"] = "off"
    min_price_div_atr: Literal[0.0, 0.25] = 0.0
    trend_filter: Literal["off", "ema20", "ema50", "ema200"] = "off"
    entry_confirmation: Literal["immediate", "breakout"] = "immediate"
    session_window: Literal["full", "excl_first30", "excl_last30", "excl_first_last30"] = "full"
