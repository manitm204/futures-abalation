"""Typed configs + ablation axes for the intraday price-path convexity strategy.

Source: Gulen & Woeppel, "Price-Path Convexity and Short-Horizon Return Predictability", JFQA
(accepted 2025). Over a window of N closes P1..PN,

    convexity = [ (P1 + PN) / 2 - mean(P1..PN) ] / [ (P1 + PN) / 2 ]

i.e. the average gap between the straight line joining the window's end points and the path,
scaled by the end-point midpoint. Positive = convex (the path sagged below the line: an up-move
came late / a down-move came early); negative = concave. The paper finds HIGH convexity
predicts LOWER returns (investors over-extrapolate late, accelerating moves), on daily data.
Every value tested here is intraday, so all of it is extrapolation from the paper.

Signal convention (every form): a HIGH signal fades to SHORT, a LOW signal to LONG.

v1 axes (one grid per bar size; 186,624 configs each):
  lookback        : 8, 12, 16, 24, 32, 48, 64, 96     (N, in bars; spans sessions over RTH bars)
  signal_form     : paper     -- the paper's convexity (midpoint denominator)
                    atr       -- (midpoint - mean) / ATR(14): the same gap in ATR units
                    maxgap    -- the largest-magnitude single gap (line - path), signed, / ATR(14)
                    reversal  -- CONTROL: (PN - P1) / ATR(14), the plain N-bar return. If the
                                 paper form doesn't beat this, convexity adds nothing over
                                 short-term reversal.
  z_lookback      : 250, 500                          (bars of the signal's rolling z-score)
  entry_z         : 0.5, 1.0, 1.5, 2.0                (enter when z crosses beyond +/- this)
  quadrant        : all       -- the paper: trade every extreme signal
                    late      -- only fades of the window's net move (convex up-move -> short,
                                 concave down-move -> long): "fade late moves"
                    early     -- only trades WITH the net move (convex down-move -> short,
                                 concave up-move -> long): the continuation half
  min_move_atr    : 0, 1, 2                           (|PN - P1| >= this x ATR(14))
  direction       : long, short, both
  hold            : half      -- round(N / 2) bars
                    full      -- N bars (the paper's hold = look-back)
                    session   -- until the session close
  stop            : none, 1.5, 2.5                    (x ATR(14) known before the fill)
  trend_filter    : none, ema50, ema200               (long only above EMA, short only below)

Fixed: no new entries in the last 30 minutes; flat at the session close; one position at a
time. The reversal control has no convex/concave split: its z-score is extreme almost only when
the net move points the same way (the z subtracts a rolling mean, so not always), so for it
quadrant=late nearly duplicates all and quadrant=early trades rarely (kept in the full factorial
so every axis has the same values; most of those configs fail the trade-count gate).
"""

from __future__ import annotations

from typing import Literal

from src.utils.config_models import FrozenModel

V1_LOOKBACKS: tuple[int, ...] = (8, 12, 16, 24, 32, 48, 64, 96)
V1_SIGNAL_FORMS: tuple[str, ...] = ("paper", "atr", "maxgap", "reversal")
V1_Z_LOOKBACKS: tuple[int, ...] = (250, 500)
V1_ENTRY_ZS: tuple[float, ...] = (0.5, 1.0, 1.5, 2.0)
V1_QUADRANTS: tuple[str, ...] = ("all", "late", "early")
V1_MIN_MOVE_ATRS: tuple[float, ...] = (0.0, 1.0, 2.0)
V1_DIRECTIONS: tuple[str, ...] = ("long", "short", "both")
V1_HOLDS: tuple[str, ...] = ("half", "full", "session")
V1_STOPS: tuple[str, ...] = ("none", "1.5", "2.5")
V1_TREND_FILTERS: tuple[str, ...] = ("none", "ema50", "ema200")

SIGNAL_FORMS = ("paper", "atr", "maxgap", "reversal")
QUADRANTS = ("all", "late", "early")
LAST_ENTRY_CUTOFF_MINUTES = 30
ATR_PERIOD = 14


def trend_ema_span(trend_filter: str) -> int | None:
    """EMA length of a trend filter ("none" -> None, "ema50" -> 50, ...)."""
    if trend_filter == "none":
        return None
    if trend_filter.startswith("ema") and trend_filter[3:].isdigit() and int(trend_filter[3:]) >= 2:
        return int(trend_filter[3:])
    raise ValueError(f"Unknown trend_filter {trend_filter!r}")


def hold_bars(hold: str, lookback: int) -> int | None:
    """Bars a position is held (None = until the session close)."""
    if hold == "session":
        return None
    if hold.startswith("b") and hold[1:].isdigit() and int(hold[1:]) >= 1:
        return int(hold[1:])  # a fixed number of bars, whatever N is (v5)
    if hold == "full":
        return lookback
    if hold == "half":
        return max(1, (lookback + 1) // 2)
    if hold == "1.5n":
        return (3 * lookback + 1) // 2  # ceil(1.5 N)
    raise ValueError(f"Unknown hold {hold!r}")


class _ConvexityConfig(FrozenModel):
    symbol: str
    timeframe: Literal["5min", "15min"] = "15min"
    lookback: Literal[8, 12, 16, 24, 32, 48, 64, 96] = 24
    signal_form: Literal["paper", "atr", "maxgap", "reversal"] = "paper"
    z_lookback: Literal[250, 500] = 250
    entry_z: Literal[0.5, 1.0, 1.5, 2.0] = 1.0
    quadrant: Literal["all", "late", "early"] = "all"
    min_move_atr: Literal[0.0, 1.0, 2.0] = 0.0
    direction: Literal["long", "short", "both"] = "both"
    hold: Literal["half", "full", "1.5n", "session"] = "full"
    stop: Literal["none", "1.5", "2.5"] = "none"
    trend_filter: Literal["none", "ema50", "ema200"] = "none"

    @property
    def stop_atr_value(self) -> float | None:
        return None if self.stop == "none" else float(self.stop)


# --- path_convexity v1 (186,624 configs per bar size) ----------------------------------------
# Specified by the user (2026-11-16) from the Purdue research report
# (reports/Purdue trading strategy research.md, Pick 1), before any convexity run was made.

class ConvexityV1_15mConfig(_ConvexityConfig):
    timeframe: Literal["15min"] = "15min"


class ConvexityV1_5mConfig(_ConvexityConfig):
    timeframe: Literal["5min"] = "5min"


# --- path_convexity v2 (15-minute bars, 82,944 configs) ---------------------------------------
# Specified by the user (2026-11-16) after reading v1's ES 15m DEVELOPMENT results
# (pc_es_v1_15m; validation not run): short look-backs, a larger minimum net move, one trend
# filter, the ATR-gap form dropped, wider stop range. Run on ES first.
V2_LOOKBACKS: tuple[int, ...] = (5, 8, 11, 15, 20, 50)
V2_SIGNAL_FORMS: tuple[str, ...] = ("paper", "maxgap", "reversal")
V2_Z_LOOKBACKS: tuple[int, ...] = (150, 500)
V2_ENTRY_ZS: tuple[float, ...] = (0.5, 0.75, 1.0, 1.5)
V2_QUADRANTS: tuple[str, ...] = ("all", "early", "late")
V2_MIN_MOVE_ATRS: tuple[float, ...] = (0.0, 1.0, 2.0, 3.0)
V2_DIRECTIONS: tuple[str, ...] = ("long", "short", "both")
V2_HOLDS: tuple[str, ...] = ("half", "full")
V2_STOPS: tuple[str, ...] = ("none", "1.5", "2.5", "3.5")
V2_TREND_FILTERS: tuple[str, ...] = ("none", "ema50")


class ConvexityV2_15mConfig(_ConvexityConfig):
    timeframe: Literal["15min"] = "15min"
    lookback: Literal[5, 8, 11, 15, 20, 50] = 8
    signal_form: Literal["paper", "maxgap", "reversal"] = "paper"
    z_lookback: Literal[150, 500] = 500
    entry_z: Literal[0.5, 0.75, 1.0, 1.5] = 1.0
    min_move_atr: Literal[0.0, 1.0, 2.0, 3.0] = 0.0
    hold: Literal["half", "full"] = "full"
    stop: Literal["none", "1.5", "2.5", "3.5"] = "none"
    trend_filter: Literal["none", "ema50"] = "none"


# --- path_convexity v3 (15-minute bars, 103,680 configs) --------------------------------------
# Specified by the user (2026-11-16) after v2 on ES failed validation/holdout (pc_es_v2_15m;
# #115 lost on ES 2025+). Run on NQ: look-back N 5/10/15/20/50, a short (25) and a medium (250)
# z-score history, a longer 1.5N hold (ceil(1.5 N) bars) and wider 2/3/4 ATR stops.
V3_LOOKBACKS: tuple[int, ...] = (5, 10, 15, 20, 50)
V3_SIGNAL_FORMS: tuple[str, ...] = ("paper", "maxgap", "reversal")
V3_Z_LOOKBACKS: tuple[int, ...] = (25, 250)
V3_ENTRY_ZS: tuple[float, ...] = (0.5, 0.75, 1.0, 1.5)
V3_QUADRANTS: tuple[str, ...] = ("all", "early", "late")
V3_MIN_MOVE_ATRS: tuple[float, ...] = (0.0, 1.0, 2.0, 3.0)
V3_DIRECTIONS: tuple[str, ...] = ("long", "short", "both")
V3_HOLDS: tuple[str, ...] = ("half", "full", "1.5n")
V3_STOPS: tuple[str, ...] = ("none", "2.0", "3.0", "4.0")
V3_TREND_FILTERS: tuple[str, ...] = ("none", "ema50")


class ConvexityV3_15mConfig(_ConvexityConfig):
    timeframe: Literal["15min"] = "15min"
    lookback: Literal[5, 10, 15, 20, 50] = 10
    signal_form: Literal["paper", "maxgap", "reversal"] = "paper"
    z_lookback: Literal[25, 250] = 250
    entry_z: Literal[0.5, 0.75, 1.0, 1.5] = 1.0
    min_move_atr: Literal[0.0, 1.0, 2.0, 3.0] = 0.0
    hold: Literal["half", "full", "1.5n"] = "full"
    stop: Literal["none", "2.0", "3.0", "4.0"] = "none"
    trend_filter: Literal["none", "ema50"] = "none"


# --- path_convexity v4 (15-minute bars, 10,368 configs) ---------------------------------------
# Specified by the user (2026-11-17) after v3 on NQ / GC / 6E / ZN (only NQ showed structure; its
# picks lost on the holdout). A light grid for markets not yet tested, run on CL first: drops
# N = 15, entry 0.75, the N/2 hold and most stops; min net move any / 2 ATR.
V4_LOOKBACKS: tuple[int, ...] = (5, 10, 20, 50)
V4_SIGNAL_FORMS: tuple[str, ...] = ("paper", "maxgap", "reversal")
V4_Z_LOOKBACKS: tuple[int, ...] = (25, 250)
V4_ENTRY_ZS: tuple[float, ...] = (0.5, 1.0, 1.5)
V4_QUADRANTS: tuple[str, ...] = ("all", "early", "late")
V4_MIN_MOVE_ATRS: tuple[float, ...] = (0.0, 2.0)
V4_DIRECTIONS: tuple[str, ...] = ("long", "short", "both")
V4_HOLDS: tuple[str, ...] = ("full", "1.5n")
V4_STOPS: tuple[str, ...] = ("none", "3.0")
V4_TREND_FILTERS: tuple[str, ...] = ("none", "ema50")


class ConvexityV4_15mConfig(_ConvexityConfig):
    timeframe: Literal["15min"] = "15min"
    lookback: Literal[5, 10, 20, 50] = 10
    signal_form: Literal["paper", "maxgap", "reversal"] = "paper"
    z_lookback: Literal[25, 250] = 250
    entry_z: Literal[0.5, 1.0, 1.5] = 1.0
    min_move_atr: Literal[0.0, 2.0] = 0.0
    hold: Literal["full", "1.5n"] = "full"
    stop: Literal["none", "3.0"] = "none"
    trend_filter: Literal["none", "ema50"] = "none"


# --- path_convexity v5 (15-minute bars, 8,640 configs) ---------------------------------------
# Specified by the user (2026-11-26) after v3 on NQ / v2 on ES (picks lost on the 2025+ holdout;
# among the 1,081 NQ finalists, long-only configs had a median validation Sharpe of +0.65 against
# +0.03 for both-sided and -0.59 for short-only). Run on ES and NQ through validation only.
# New: longer look-backs (26 bars = one session; 130 = five), a regime filter (daily trend or
# high volatility), an entry-time window, fixed-bar holds (N-based holds collapse to "session" once
# N >= 20 on 15-minute bars), long-only or both sides. Quadrant fixed to "all", no 15-minute EMA.
#   regime : none | dtrend50 (long only above the prior sessions' 50-day SMA of daily closes, short
#            only below) | volhi (ATR(14)/close at or above its median over the last 1,300 bars)
#   window : all | mid (the entry bar opens 10:00 to 15:00)
V5_LOOKBACKS: tuple[int, ...] = (20, 26, 52, 78, 130)
V5_SIGNAL_FORMS: tuple[str, ...] = ("paper", "maxgap", "reversal")
V5_Z_LOOKBACKS: tuple[int, ...] = (25, 100)
V5_ENTRY_ZS: tuple[float, ...] = (1.0, 1.5)
V5_QUADRANTS: tuple[str, ...] = ("all",)
V5_MIN_MOVE_ATRS: tuple[float, ...] = (2.0, 3.0)
V5_DIRECTIONS: tuple[str, ...] = ("long", "both")
V5_HOLDS: tuple[str, ...] = ("b8", "b16", "session")
V5_STOPS: tuple[str, ...] = ("2.0", "3.0")
V5_TREND_FILTERS: tuple[str, ...] = ("none",)
V5_REGIMES: tuple[str, ...] = ("none", "dtrend50", "volhi")
V5_WINDOWS: tuple[str, ...] = ("all", "mid")
VOLHI_WINDOW_BARS = 1300
DTREND_SESSIONS = 50


class ConvexityV5_15mConfig(_ConvexityConfig):
    timeframe: Literal["15min"] = "15min"
    lookback: Literal[20, 26, 52, 78, 130] = 26
    signal_form: Literal["paper", "maxgap", "reversal"] = "paper"
    z_lookback: Literal[25, 100] = 25
    entry_z: Literal[1.0, 1.5] = 1.0
    quadrant: Literal["all"] = "all"
    min_move_atr: Literal[2.0, 3.0] = 2.0
    direction: Literal["long", "both"] = "long"
    hold: Literal["b8", "b16", "session"] = "b8"
    stop: Literal["2.0", "3.0"] = "2.0"
    trend_filter: Literal["none"] = "none"
    regime: Literal["none", "dtrend50", "volhi"] = "none"
    window: Literal["all", "mid"] = "all"
