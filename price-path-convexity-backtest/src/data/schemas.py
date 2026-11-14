"""Canonical schemas for raw and cleaned market data.

Schema versioning: bump SCHEMA_VERSION whenever the cleaned-data column set or
semantics change. The manifest records the schema_version used to produce each
cleaned partition so downstream consumers can detect stale/incompatible data.
"""

from __future__ import annotations

import polars as pl

SCHEMA_VERSION = "1.0.0"
CLEANING_VERSION = "1.0.0"

# Raw FMP intraday response, as received, before any timezone interpretation.
# `date` is kept as a plain string exactly as returned by the API — we do not
# parse/localize it until normalization, where the bar-label convention is
# applied explicitly and recorded.
RAW_FMP_INTRADAY_SCHEMA = {
    "date": pl.Utf8,
    "open": pl.Float64,
    "high": pl.Float64,
    "low": pl.Float64,
    "close": pl.Float64,
    "volume": pl.Int64,
}

# Canonical cleaned intraday bar schema. Every cleaned Parquet file conforms to this.
CLEAN_BAR_SCHEMA = {
    "symbol": pl.Utf8,
    "timeframe": pl.Utf8,  # e.g. "1min", "5min", "15min", "1h", "1d"
    "bar_open_ts": pl.Datetime(time_unit="us", time_zone="UTC"),
    "bar_close_ts": pl.Datetime(time_unit="us", time_zone="UTC"),
    "bar_open_ts_ny": pl.Datetime(time_unit="us", time_zone="America/New_York"),
    "bar_close_ts_ny": pl.Datetime(time_unit="us", time_zone="America/New_York"),
    "session_date_ny": pl.Date,
    "open": pl.Float64,
    "high": pl.Float64,
    "low": pl.Float64,
    "close": pl.Float64,
    "volume": pl.Int64,
    "is_regular_session": pl.Boolean,
    "is_extended_hours": pl.Boolean,
    "source": pl.Utf8,  # "fmp_native" or "aggregated_from_1min"
    "adjustment_status": pl.Utf8,  # "raw" | "split_adjusted" | "unknown"
    "schema_version": pl.Utf8,
    "cleaning_version": pl.Utf8,
}

VALID_TIMEFRAMES = ("1min", "5min", "15min", "1h", "1d")


def empty_clean_frame() -> pl.DataFrame:
    return pl.DataFrame(schema=CLEAN_BAR_SCHEMA)


def assert_clean_schema(df: pl.DataFrame) -> None:
    missing = set(CLEAN_BAR_SCHEMA) - set(df.schema)
    if missing:
        raise ValueError(f"Cleaned frame missing required columns: {sorted(missing)}")
    for col, dtype in CLEAN_BAR_SCHEMA.items():
        actual = df.schema[col]
        if actual != dtype:
            raise ValueError(f"Column {col!r} has dtype {actual}, expected {dtype}")
