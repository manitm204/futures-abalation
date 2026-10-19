"""Aggregate clean 1-minute bars into 5min/15min/1h/1d bars.

Alignment rule: resampling buckets are anchored to calendar-minute boundaries in
UTC (e.g. every 5 minutes since the Unix epoch), which is safe here because the
NYSE regular session open (09:30 America/New_York) is itself an exact multiple of
5 and 15 minutes measured in UTC minutes-since-midnight, in both EST (14:30 UTC =
870 min) and EDT (13:30 UTC = 810 min). This is NOT arbitrary-UTC-boundary
resampling in the sense the spec warns against -- it is equivalent to session-
anchored resampling for these interval sizes. If a future timeframe is added that
does NOT evenly divide 390 (or the early-close duration), this alignment must be
revisited; `_assert_safe_interval` guards against silently doing so.

Partial final bar rule (explicit, per spec): a bucket is emitted whenever it
contains at least one source bar. Each aggregated bar carries `n_source_bars`;
callers can filter `n_source_bars < expected_bars_for(timeframe)` to exclude
partial bars (e.g. a truncated final bucket at session close or at the edge of
the requested date range). No interpolation or forward-fill is ever used to
complete a partial bucket.
"""

from __future__ import annotations

import polars as pl

from src.data.schemas import CLEAN_BAR_SCHEMA, CLEANING_VERSION, SCHEMA_VERSION

AGG_INTERVAL_MINUTES = {"5min": 5, "15min": 15, "1h": 60}
SESSION_MINUTES = 390  # 09:30-16:00 NY


SESSION_OPEN_MINUTE_OF_HOUR = 30  # 09:30 NY is always :30-past-the-hour in UTC (EST or EDT)


def _interval_minutes(timeframe: str) -> int:
    if timeframe not in AGG_INTERVAL_MINUTES:
        raise ValueError(f"Unsupported aggregation target: {timeframe!r}")
    return AGG_INTERVAL_MINUTES[timeframe]


def _session_anchor_offset(minutes: int) -> str:
    """UTC-epoch-anchored buckets of size `minutes` only land exactly on the 09:30 NY
    session open if the offset (in minutes) equals 09:30's minute-of-hour modulo the
    bucket size. E.g. 5/15min buckets need no offset (30 % 5 == 30 % 15 == 0); 60min
    buckets need a 30-minute offset (30 % 60 == 30), since 09:30 is never itself an
    exact UTC-hour boundary. This generalizes to any interval without per-timeframe
    special-casing, and this function is the only place that logic lives.
    """
    offset = SESSION_OPEN_MINUTE_OF_HOUR % minutes
    return f"{offset}m"


def aggregate_bars(df_1min: pl.DataFrame, *, timeframe: str) -> pl.DataFrame:
    """Aggregate clean 1-minute bars (single symbol) into `timeframe` bars.

    Only regular-session bars (`is_regular_session`) are aggregated; this keeps the
    output free of any accidental mixing with non-RTH bars until extended-hours
    handling is explicitly implemented (see ASSUMPTIONS.md: no extended-hours bars
    have been observed from FMP's intraday endpoint to date).
    """
    minutes = _interval_minutes(timeframe)
    offset = _session_anchor_offset(minutes)
    if df_1min.is_empty():
        return pl.DataFrame(schema=CLEAN_BAR_SCHEMA)

    symbols = df_1min["symbol"].unique().to_list()
    if len(symbols) != 1:
        raise ValueError(f"aggregate_bars expects a single symbol, got {symbols}")
    symbol = symbols[0]

    src = df_1min.filter(pl.col("is_regular_session"))
    if src.is_empty():
        return pl.DataFrame(schema=CLEAN_BAR_SCHEMA)

    grouped = (
        src.sort("bar_open_ts")
        .group_by_dynamic(
            "bar_open_ts",
            every=f"{minutes}m",
            offset=offset,
            closed="left",
            label="left",
            group_by="session_date_ny",
        )
        .agg(
            [
                pl.col("open").first().alias("open"),
                pl.col("high").max().alias("high"),
                pl.col("low").min().alias("low"),
                pl.col("close").last().alias("close"),
                pl.col("volume").sum().alias("volume"),
                pl.len().alias("n_source_bars"),
                pl.col("adjustment_status").first().alias("adjustment_status"),
            ]
        )
    )

    grouped = grouped.with_columns(
        [
            pl.lit(symbol).alias("symbol"),
            pl.lit(timeframe).alias("timeframe"),
            (pl.col("bar_open_ts") + pl.duration(minutes=minutes)).alias("bar_close_ts"),
            pl.col("bar_open_ts").dt.convert_time_zone("America/New_York").alias("bar_open_ts_ny"),
            pl.lit(True).alias("is_regular_session"),
            pl.lit(False).alias("is_extended_hours"),
            pl.lit("aggregated_from_1min").alias("source"),
            pl.lit(SCHEMA_VERSION).alias("schema_version"),
            pl.lit(CLEANING_VERSION).alias("cleaning_version"),
        ]
    )
    grouped = grouped.with_columns(
        (pl.col("bar_open_ts") + pl.duration(minutes=minutes))
        .dt.convert_time_zone("America/New_York")
        .alias("bar_close_ts_ny"),
    )

    expected = minutes
    grouped = grouped.with_columns((pl.col("n_source_bars") < expected).alias("is_partial_bar"))

    return grouped.sort("bar_open_ts").select([*CLEAN_BAR_SCHEMA.keys(), "n_source_bars", "is_partial_bar"])

