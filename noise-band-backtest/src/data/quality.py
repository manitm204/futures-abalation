"""Data-quality checks over cleaned bar frames.

Every function here DETECTS and REPORTS issues; none of them repair data. Per
project policy, "repairs" (interpolation, forward-fill, dropping bad rows) must
never happen silently -- if a future workflow needs a repair step, it must be a
separate, explicitly invoked, and logged transformation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

import polars as pl

from src.data.calendars import TradingCalendar


@dataclass
class QualityReport:
    symbol: str
    timeframe: str
    row_count: int
    duplicate_bar_open_ts: int
    unsorted: bool
    invalid_ohlc_count: int
    negative_price_count: int
    negative_volume_count: int
    missing_session_dates: list[date]
    incomplete_session_dates: list[tuple]  # (date, actual_bar_count, expected_bar_count)
    unexpected_bars_outside_session: int
    large_gap_count: int
    large_gaps: list[tuple] = field(default_factory=list)
    zero_volume_bar_count: int = 0


def _duplicate_count(df: pl.DataFrame) -> int:
    n = df.height
    n_unique = df.select("symbol", "timeframe", "bar_open_ts").unique().height
    return n - n_unique


def _is_sorted(df: pl.DataFrame) -> bool:
    ts = df["bar_open_ts"].to_list()
    return ts == sorted(ts)


def _invalid_ohlc_mask(df: pl.DataFrame) -> pl.Series:
    return (
        (pl.col("high") < pl.col("low"))
        | (pl.col("high") < pl.col("open"))
        | (pl.col("high") < pl.col("close"))
        | (pl.col("low") > pl.col("open"))
        | (pl.col("low") > pl.col("close"))
    )


_INTERVAL_MINUTES = {"1min": 1, "5min": 5, "15min": 15}


def _expected_bar_count(session_date: date, calendar: TradingCalendar, timeframe: str) -> int | None:
    interval = _INTERVAL_MINUTES.get(timeframe)
    if interval is None:
        return None  # unknown timeframe (e.g. 1h/1d) -- completeness check not defined
    session = calendar.session_for(session_date)
    if session is None:
        return None
    duration_minutes = (session.close_ny - session.open_ny).total_seconds() / 60
    return int(duration_minutes // interval)


def check_intraday_quality(
    df: pl.DataFrame,
    *,
    symbol: str,
    timeframe: str,
    calendar: TradingCalendar,
    expected_start: date,
    expected_end: date,
    gap_threshold_minutes: int = 15,
    completeness_tolerance: float = 0.99,
) -> QualityReport:
    if df.is_empty():
        return QualityReport(
            symbol=symbol, timeframe=timeframe, row_count=0, duplicate_bar_open_ts=0,
            unsorted=False, invalid_ohlc_count=0, negative_price_count=0,
            negative_volume_count=0, missing_session_dates=calendar.trading_days(expected_start, expected_end),
            incomplete_session_dates=[], unexpected_bars_outside_session=0, large_gap_count=0,
        )

    dup_count = _duplicate_count(df)
    unsorted = not _is_sorted(df)
    invalid_ohlc = df.filter(_invalid_ohlc_mask(df)).height
    negative_price = df.filter(
        (pl.col("open") < 0) | (pl.col("high") < 0) | (pl.col("low") < 0) | (pl.col("close") < 0)
    ).height
    negative_volume = df.filter(pl.col("volume") < 0).height
    zero_volume = df.filter(pl.col("volume") == 0).height
    outside_session = df.filter(~pl.col("is_regular_session")).height

    present_dates = set(df["session_date_ny"].unique().to_list())
    expected_dates = set(calendar.trading_days(expected_start, expected_end))
    missing_dates = sorted(expected_dates - present_dates)

    incomplete_dates: list[tuple] = []
    if "is_regular_session" in df.columns:
        regular_only = df.filter(pl.col("is_regular_session"))
        counts = regular_only.group_by("session_date_ny").agg(pl.len().alias("n")).sort("session_date_ny")
        for d, n in zip(counts["session_date_ny"].to_list(), counts["n"].to_list()):
            expected = _expected_bar_count(d, calendar, timeframe)
            if expected is not None and n < expected * completeness_tolerance:
                incomplete_dates.append((d, n, expected))

    regular = df.filter(pl.col("is_regular_session")).sort("bar_open_ts")
    gaps: list[tuple] = []
    if regular.height > 1:
        ts = regular["bar_open_ts"].to_list()
        sess = regular["session_date_ny"].to_list()
        for i in range(1, len(ts)):
            if sess[i] != sess[i - 1]:
                continue  # session boundary, not a gap
            delta_minutes = (ts[i] - ts[i - 1]).total_seconds() / 60
            if delta_minutes > gap_threshold_minutes:
                gaps.append((ts[i - 1], ts[i], delta_minutes))

    return QualityReport(
        symbol=symbol,
        timeframe=timeframe,
        row_count=df.height,
        duplicate_bar_open_ts=dup_count,
        unsorted=unsorted,
        invalid_ohlc_count=invalid_ohlc,
        negative_price_count=negative_price,
        negative_volume_count=negative_volume,
        missing_session_dates=missing_dates,
        incomplete_session_dates=incomplete_dates,
        unexpected_bars_outside_session=outside_session,
        large_gap_count=len(gaps),
        large_gaps=gaps,
        zero_volume_bar_count=zero_volume,
    )


def compare_native_vs_aggregated(native: pl.DataFrame, aggregated: pl.DataFrame, *, tolerance: float = 1e-6) -> dict:
    """Compare FMP-native N-min bars against internally aggregated N-min bars on
    overlapping timestamps. Returns per-column max absolute difference and a count
    of mismatched bars beyond `tolerance` (OHLC) — used to sanity-check aggregation
    against FMP's own 5min/15min endpoints on sampled dates.
    """
    joined = native.join(
        aggregated, on=["symbol", "timeframe", "bar_open_ts"], how="inner", suffix="_agg"
    )
    if joined.is_empty():
        return {"overlapping_bars": 0}

    result = {"overlapping_bars": joined.height}
    for col in ("open", "high", "low", "close"):
        diff = (joined[col] - joined[f"{col}_agg"]).abs()
        result[f"max_abs_diff_{col}"] = float(diff.max())
        result[f"mismatch_count_{col}"] = int((diff > tolerance).sum())
    vol_diff = (joined["volume"] - joined["volume_agg"]).abs()
    result["max_abs_diff_volume"] = int(vol_diff.max())
    result["mismatch_count_volume"] = int((vol_diff > 0).sum())
    return result
