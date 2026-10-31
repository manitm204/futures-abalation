"""Typed config + ablation axes for the intraday noise-band breakout (momentum) strategy.

After Zarattini, Aziz & Barbon (2024), "Beat the Market: An Effective Intraday
Momentum Strategy for S&P500 ETF (SPY)". The band around each session's open is
the "noise area": the average absolute move from the open, AT THE SAME TIME OF
DAY, over the previous `band_lookback` sessions, times `band_mult`. A close
outside the band at a check time is treated as a real move and traded in its
direction; every position is flat by the session close.

Axes (the Cartesian grid, v1 = 8,100 variants per symbol):
  timeframe      : 5min, 15min          (bar size)
  band_lookback  : 7, 10, 14, 20, 30    (sessions averaged per time-of-day slot)
  band_mult      : 0.75, 1.0, 1.25, 1.5, 2.0 (band half-width = band_mult x average move)
  check_minutes  : 15, 30, 60           (signals / trailing exits only at bar closes
                                         that land on a multiple of this from the open)
  first_entry_minutes : 15, 30, 60      (no entry signal before this long after the open;
                                         combinations below the first check time act alike)
  anchor         : open                 (band centred on the session open)
                   open_prev_close      (upper edge from max(open, prior close), lower from
                                         min(open, prior close): the paper's gap adjustment)
  trail          : band                 (long exits when a check close falls back inside the band)
                   vwap                 (long exits on a check close below session VWAP)
                   band_vwap            (the tighter of the two: below max(upper band, VWAP))
  direction      : long, short, both
  max_entries_per_session : 1, 2, none  (v4+: entries allowed per session; none = no cap)
  stop_atr       : none                 (v1: no protective stop; the backtester supports
                                         entry open -/+ k x ATR(14), intrabar, for later rounds)
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
BAND_MULTS: tuple[float, ...] = (0.75, 1.0, 1.25, 1.5, 2.0)
CHECK_MINUTES: tuple[int, ...] = (15, 30, 60)
FIRST_ENTRY_MINUTES: tuple[int, ...] = (15, 30, 60)
ANCHORS: tuple[str, ...] = ("open", "open_prev_close")
TRAILS: tuple[str, ...] = ("band", "vwap", "band_vwap")
DIRECTIONS: tuple[str, ...] = ("long", "short", "both")
STOP_ATRS: tuple[str, ...] = ("none",)


class NoiseBandConfig(FrozenModel):
    symbol: str
    timeframe: Timeframe = "5min"
    band_lookback: Literal[7, 10, 14, 20, 30] = 14
    band_mult: Literal[0.75, 1.0, 1.25, 1.5, 2.0] = 1.0
    check_minutes: Literal[15, 30, 60] = 30
    first_entry_minutes: Literal[15, 30, 60] = 30
    anchor: Anchor = "open_prev_close"
    trail: Trail = "band_vwap"
    direction: Direction = "both"
    stop_atr_multiple: Literal["none"] = "none"

    @property
    def stop_atr_value(self) -> float | None:
        return None if self.stop_atr_multiple == "none" else float(self.stop_atr_multiple)

    @property
    def max_entries_value(self) -> int | None:
        """Entries allowed per session (None = no cap). Only v4+ configs have the field."""
        v = getattr(self, "max_entries_per_session", "none")
        return None if v == "none" else int(v)


# --- v2 parameter space (ES round 2, 8,100 variants per symbol) ---------------------------
# Specified by the user after reading ES v1 development results (2018-2022 only; validation
# untouched): 5min bars only (with no stop, 15min decides at the same check times), band
# lookback 3-80 sessions, band multiple 0.25-1.25, the other axes as in v1, no stop.
V2_TIMEFRAMES: tuple[str, ...] = ("5min",)
V2_BAND_LOOKBACKS: tuple[int, ...] = (3, 5, 7, 10, 15, 25, 35, 45, 60, 80)
V2_BAND_MULTS: tuple[float, ...] = (0.25, 0.5, 0.75, 1.0, 1.25)


class NoiseBandV2Config(NoiseBandConfig):
    timeframe: Literal["5min"] = "5min"
    band_lookback: Literal[3, 5, 7, 10, 15, 25, 35, 45, 60, 80] = 10
    band_mult: Literal[0.25, 0.5, 0.75, 1.0, 1.25] = 0.75


# --- v3 parameter space (ES round 3, 16,200 variants per symbol) --------------------------
# The v2 grid re-run on both 5min and 15min bars, at the user's request after v2's
# development results (2018-2022 only; validation untouched).
V3_TIMEFRAMES: tuple[str, ...] = ("5min", "15min")


class NoiseBandV3Config(NoiseBandV2Config):
    timeframe: Literal["5min", "15min"] = "5min"


# --- v4 parameter space (ES round 4, 13,824 variants per symbol) --------------------------
# Specified by the user after reading ES v1-v3 development results (2018-2022 only;
# validation untouched): 5min + 15min, band lookback 1-32 sessions, band multiple
# 0.75-2.0, check 15/30/60, first entry 30/60, anchor open / gap-adjusted, trailing exit
# VWAP / closer of band and VWAP, long / both, and a NEW axis: at most 1 or 2 entries per
# session, or no cap (the v1-v3 behaviour). No stop.
V4_BAND_LOOKBACKS: tuple[int, ...] = (1, 8, 12, 16, 20, 24, 28, 32)
V4_BAND_MULTS: tuple[float, ...] = (0.75, 1.0, 1.25, 1.5, 1.75, 2.0)
V4_FIRST_ENTRY_MINUTES: tuple[int, ...] = (30, 60)
V4_TRAILS: tuple[str, ...] = ("vwap", "band_vwap")
V4_DIRECTIONS: tuple[str, ...] = ("long", "both")
V4_MAX_ENTRIES: tuple = (1, 2, "none")


class NoiseBandV4Config(NoiseBandConfig):
    band_lookback: Literal[1, 8, 12, 16, 20, 24, 28, 32] = 16
    band_mult: Literal[0.75, 1.0, 1.25, 1.5, 1.75, 2.0] = 1.0
    first_entry_minutes: Literal[30, 60] = 30
    trail: Literal["vwap", "band_vwap"] = "vwap"
    direction: Literal["long", "both"] = "both"
    max_entries_per_session: Literal[1, 2, "none"] = "none"
