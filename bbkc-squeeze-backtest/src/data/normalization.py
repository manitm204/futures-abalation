"""Raw FMP JSON -> canonical cleaned Polars schema.

Applies the empirically confirmed conventions (see ASSUMPTIONS.md):
  - `date` is an America/New_York naive wall-clock string, open-labeled.
  - Data is split-adjusted.
  - FMP's `historical-chart` intraday endpoint appears to return RTH-only bars
    (390 bars for a full non-early-close day, 09:30-15:59) -- no extended-hours
    bars were observed in verification queries. This is recorded as
    `is_extended_hours=False` for all rows produced here; if a future data pull
    surfaces bars outside the session window, `is_regular_session` will correctly
    flag them rather than silently mislabeling.

This module does NOT repair bad data (no interpolation, no forward-fill, no
silent drop of invalid OHTLC rows) -- see src/data/quality.py for detection.
Deduplication (exact duplicate bar_open_ts) and sorting are the only
transformations applied here, and both are idempotent and recorded via
`cleaning_version`.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Literal

import polars as pl

from src.data.calendars import TradingCalendar
from src.data.schemas import CLEANING_VERSION, CLEAN_BAR_SCHEMA, SCHEMA_VERSION
from src.utils.time import localize_ny, to_utc

INTERVAL_MINUTES = {"1min": 1, "5min": 5, "15min": 15}

BarLabelConvention = Literal["open"]  # only "open" is verified/supported; see ASSUMPTIONS.md


def _parse_ny_naive(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")


def normalize_intraday_rows(
    rows: list[dict],
    *,
    symbol: str,
    timeframe: str,
    source: Literal["fmp_native", "aggregated_from_1min"],
    calendar: TradingCalendar,
    bar_label_convention: BarLabelConvention = "open",
    adjustment_status: str = "split_adjusted",
) -> pl.DataFrame:
    """Convert a list of raw {date, open, high, low, close, volume} dicts into the
    canonical clean schema. Raises if `bar_label_convention` is anything but the
    verified "open" (fail loudly rather than silently assume a different convention).
    """
    if bar_label_convention != "open":
        raise ValueError(
            f"bar_label_convention={bar_label_convention!r} is not verified/supported. "
            "See ASSUMPTIONS.md; only 'open' has been empirically confirmed."
        )
    if timeframe not in INTERVAL_MINUTES:
        raise ValueError(f"Unsupported intraday timeframe: {timeframe!r}")

    interval_minutes = INTERVAL_MINUTES[timeframe]

    if not rows:
        return pl.DataFrame(schema=CLEAN_BAR_SCHEMA)

    bar_open_ts_ny: list[datetime] = []
    bar_close_ts_ny: list[datetime] = []
    for row in rows:
        naive = _parse_ny_naive(row["date"])
        open_ny = localize_ny(naive, label=f"{symbol} {timeframe} bar date")
        close_ny = open_ny + timedelta(minutes=interval_minutes)
        bar_open_ts_ny.append(open_ny)
        bar_close_ts_ny.append(close_ny)

    df = pl.DataFrame(
        {
            "symbol": [symbol] * len(rows),
            "timeframe": [timeframe] * len(rows),
            "bar_open_ts_ny": bar_open_ts_ny,
            "bar_close_ts_ny": bar_close_ts_ny,
            "open": [float(r["open"]) for r in rows],
            "high": [float(r["high"]) for r in rows],
            "low": [float(r["low"]) for r in rows],
            "close": [float(r["close"]) for r in rows],
            "volume": [int(r["volume"]) for r in rows],
        }
    )

    df = df.with_columns(
        [
            pl.col("bar_open_ts_ny").dt.convert_time_zone("UTC").alias("bar_open_ts"),
            pl.col("bar_close_ts_ny").dt.convert_time_zone("UTC").alias("bar_close_ts"),
            pl.col("bar_open_ts_ny").dt.date().alias("session_date_ny"),
            pl.lit(source).alias("source"),
            pl.lit(adjustment_status).alias("adjustment_status"),
            pl.lit(SCHEMA_VERSION).alias("schema_version"),
            pl.lit(CLEANING_VERSION).alias("cleaning_version"),
        ]
    )

    df = _flag_session(df, calendar)

    # Dedupe exact duplicate bar_open_ts (idempotent, recorded transformation --
    # NOT a repair of differing OHLCV values for the same timestamp, which is a
    # quality issue surfaced by src/data/quality.py, not silently resolved here).
    df = df.unique(subset=["symbol", "timeframe", "bar_open_ts"], keep="first")
    df = df.sort("bar_open_ts")

    return df.select(list(CLEAN_BAR_SCHEMA.keys()))


def _flag_session(df: pl.DataFrame, calendar: TradingCalendar) -> pl.DataFrame:
    if df.is_empty():
        return df.with_columns(
            pl.lit(False).alias("is_regular_session"),
            pl.lit(False).alias("is_extended_hours"),
        )

    start = df["session_date_ny"].min()
    end = df["session_date_ny"].max()
    sessions = calendar.sessions(start, end)
    session_by_date = {s.session_date: s for s in sessions}

    is_regular = []
    for open_ny, session_date in zip(df["bar_open_ts_ny"].to_list(), df["session_date_ny"].to_list()):
        session = session_by_date.get(session_date)
        if session is None:
            is_regular.append(False)
            continue
        open_t = open_ny.timetz().replace(tzinfo=None)
        session_open_t = session.open_ny.timetz().replace(tzinfo=None)
        session_close_t = session.close_ny.timetz().replace(tzinfo=None)
        is_regular.append(session_open_t <= open_t < session_close_t)

    return df.with_columns(
        pl.Series("is_regular_session", is_regular, dtype=pl.Boolean),
        pl.lit(False).alias("is_extended_hours"),
    )
