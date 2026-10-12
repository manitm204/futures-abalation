"""Higher-timeframe bias modes.

CRITICAL causal rule: for an intraday signal occurring during session date D, the
CURRENT (in-progress) daily bar for D must never be used to compute daily bias --
only the most recent COMPLETED daily bar (i.e. date < D, or more precisely the
last daily bar whose bar_close_ts is before the intraday timestamp being
evaluated) may be referenced. Every function here takes an explicit `as_of_ts`
and filters the higher-timeframe frame to `bar_close_ts <= as_of_ts` before doing
anything else, so this can't be gotten wrong by a caller forgetting to pre-filter.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

import polars as pl

BiasMode = Literal["none", "prior_daily_direction", "prior_day_close_vs_open", "hourly_swing_structure", "daily_ma20_slope", "price_vs_daily_ma20"]
Bias = Literal["bullish", "bearish", "neutral"]


def _completed_bars_as_of(htf_df: pl.DataFrame, as_of_ts: datetime) -> pl.DataFrame:
    return htf_df.filter(pl.col("bar_close_ts") <= as_of_ts).sort("bar_close_ts")


def resolve_bias(
    mode: BiasMode,
    *,
    as_of_ts: datetime,
    daily_df: pl.DataFrame | None = None,
    hourly_swings: pl.DataFrame | None = None,
    ma_period: int = 20,
) -> Bias | None:
    """Returns the resolved bias, or None if there isn't enough completed history
    to resolve it yet (caller must treat None as "reject signal", not "neutral")."""
    if mode == "none":
        return "neutral"

    daily_modes = ("prior_daily_direction", "prior_day_close_vs_open", "daily_ma20_slope", "price_vs_daily_ma20")
    if mode in daily_modes and daily_df is None:
        # Missing required data is unresolvable, not a crash -- caller must treat
        # None as "reject this signal," same as insufficient history.
        return None

    if mode == "prior_daily_direction":
        completed = _completed_bars_as_of(daily_df, as_of_ts)
        if completed.is_empty():
            return None
        last = completed.tail(1).row(0, named=True)
        if last["close"] > last["open"]:
            return "bullish"
        if last["close"] < last["open"]:
            return "bearish"
        return "neutral"

    if mode == "prior_day_close_vs_open":
        completed = _completed_bars_as_of(daily_df, as_of_ts)
        if completed.height < 2:
            return None
        prior = completed.tail(2).row(0, named=True)  # the day before the most recent completed day
        last = completed.tail(1).row(0, named=True)
        if last["open"] > prior["close"]:
            return "bullish"
        if last["open"] < prior["close"]:
            return "bearish"
        return "neutral"

    if mode == "daily_ma20_slope":
        completed = _completed_bars_as_of(daily_df, as_of_ts)
        if completed.height < ma_period + 1:
            return None
        closes = completed["close"].to_list()
        ma_now = sum(closes[-ma_period:]) / ma_period
        ma_prev = sum(closes[-ma_period - 1 : -1]) / ma_period
        if ma_now > ma_prev:
            return "bullish"
        if ma_now < ma_prev:
            return "bearish"
        return "neutral"

    if mode == "price_vs_daily_ma20":
        completed = _completed_bars_as_of(daily_df, as_of_ts)
        if completed.height < ma_period:
            return None
        closes = completed["close"].to_list()
        ma = sum(closes[-ma_period:]) / ma_period
        last_close = closes[-1]
        if last_close > ma:
            return "bullish"
        if last_close < ma:
            return "bearish"
        return "neutral"

    if mode == "hourly_swing_structure":
        if hourly_swings is None or hourly_swings.is_empty():
            return None
        completed = hourly_swings.filter(pl.col("availability_ts") <= as_of_ts).sort("availability_ts")
        if completed.height < 2:
            return None
        rows = completed.tail(4).to_dicts()  # last few confirmed swings
        highs = [r["price"] for r in rows if r["kind"] == "high"]
        lows = [r["price"] for r in rows if r["kind"] == "low"]
        if len(highs) >= 2 and highs[-1] > highs[-2] and len(lows) >= 2 and lows[-1] > lows[-2]:
            return "bullish"
        if len(highs) >= 2 and highs[-1] < highs[-2] and len(lows) >= 2 and lows[-1] < lows[-2]:
            return "bearish"
        return "neutral"

    raise ValueError(f"Unsupported bias mode: {mode!r}")
