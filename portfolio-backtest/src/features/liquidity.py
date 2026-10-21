"""Causal liquidity-level candidates.

Every level carries `formation_ts` (when the price extreme that defines it
occurred) and `availability_ts` (the earliest timestamp at which it may be
referenced by signal/execution logic). For prior-session and pre-window levels
these two often coincide with the point at which the defining window of bars is
known to be *closed off* (not necessarily the extreme's own bar timestamp),
which is the conservative, causal-safe choice.

Levels implemented:
  - prior_session_high / prior_session_low: prior RTH session's high/low.
    availability_ts = the CURRENT session's open (the prior session is fully
    closed out by then; using its own last-bar close would be a few minutes
    into the current session's pre-market for many providers, but since this
    framework only observes RTH-only bars from FMP -- see ASSUMPTIONS.md --
    prior-session data is complete as of prior session's last bar close, and
    is not referenceable before the *current* session begins).
  - pre_window_high / pre_window_low: high/low of the CURRENT session's bars
    from session open up to (not including) a given Silver Bullet window's
    start. Per spec: "Pre-window levels stop updating at window start" --
    availability_ts is fixed at the window's start time and does not advance
    as later bars arrive.
  - swing_high / swing_low: passthrough of confirmed fractal swings (see
    src/features/swings.py) recast into the common liquidity-level schema.

NOT implemented (explicitly, not silently): overnight/extended-hours session
high/low. FMP's intraday endpoint has not been observed to return any bars
outside 09:30-16:00 NY in verification queries (see ASSUMPTIONS.md); computing
an "overnight range" would require guessing at data this framework does not
have. If extended-hours data becomes available, this module must be revisited.
"""

from __future__ import annotations

from datetime import datetime, time

import polars as pl

from src.data.calendars import TradingCalendar

LEVEL_SCHEMA = {
    "level_id": pl.Utf8,
    "type": pl.Utf8,
    "price": pl.Float64,
    "formation_ts": pl.Datetime("us", "UTC"),
    "availability_ts": pl.Datetime("us", "UTC"),
    "timeframe": pl.Utf8,
    "session_date_ny": pl.Date,
    "status": pl.Utf8,  # "active" | "swept" | "invalidated"
    "sweep_ts": pl.Datetime("us", "UTC"),
    "invalidation_reason": pl.Utf8,
}


def _empty_levels() -> pl.DataFrame:
    return pl.DataFrame(schema=LEVEL_SCHEMA)


def prior_session_extremes(df: pl.DataFrame, *, calendar: TradingCalendar, timeframe: str) -> pl.DataFrame:
    """`df`: single-symbol RTH bars, ascending-sorted. One (high, low) level pair
    per session, tagged with the NEXT session's date since that's when it is usable.
    """
    if df.is_empty():
        return _empty_levels()

    sessions = sorted(df["session_date_ny"].unique().to_list())
    if not sessions:
        return _empty_levels()

    # Batch-fetch the calendar's session-open times once for the whole date range
    # instead of once per session date: TradingCalendar.sessions() caches by the
    # exact (start, end) tuple, so len(sessions) separate single-day calls each
    # missed the cache and re-triggered pandas_market_calendars' expensive
    # schedule computation. One batched call is a large, measured speedup.
    calendar_sessions = calendar.sessions(sessions[0], sessions[-1])
    session_open_by_date = {s.session_date: s.open_ny for s in calendar_sessions}

    # Per-day aggregates computed once via group_by instead of one .filter() per
    # session date (same O(n_sessions^2) -> O(n) fix as the calendar lookup).
    day_aggs = (
        df.group_by("session_date_ny", maintain_order=True)
        .agg(pl.col("high").max().alias("day_high"), pl.col("low").min().alias("day_low"), pl.col("bar_close_ts").last().alias("last_close_ts"))
        .sort("session_date_ny")
    )
    agg_by_date = {row["session_date_ny"]: row for row in day_aggs.iter_rows(named=True)}

    records: list[dict] = []
    for i, sess_date in enumerate(sessions[:-1]):
        applies_to = sessions[i + 1]
        agg = agg_by_date[sess_date]
        day_high, day_low, last_close_ts = agg["day_high"], agg["day_low"], agg["last_close_ts"]

        open_ny = session_open_by_date.get(applies_to)
        availability_ts = open_ny.astimezone(last_close_ts.tzinfo) if open_ny is not None else last_close_ts

        for kind, price in (("prior_session_high", day_high), ("prior_session_low", day_low)):
            records.append(
                {
                    "level_id": f"{kind}_{sess_date}",
                    "type": kind,
                    "price": price,
                    "formation_ts": last_close_ts,
                    "availability_ts": availability_ts,
                    "timeframe": timeframe,
                    "session_date_ny": applies_to,
                    "status": "active",
                    "sweep_ts": None,
                    "invalidation_reason": None,
                }
            )
    return pl.DataFrame(records, schema=LEVEL_SCHEMA) if records else _empty_levels()


def pre_window_extremes(
    df: pl.DataFrame, *, window_start: time, window_name: str, timeframe: str
) -> pl.DataFrame:
    """High/low of each session's bars strictly before `window_start` (NY local
    time). Frozen at window start: availability_ts == window start for that
    session, regardless of how many bars preceded it.
    """
    if df.is_empty():
        return _empty_levels()

    records: list[dict] = []
    for sess_date in sorted(df["session_date_ny"].unique().to_list()):
        day_df = df.filter(pl.col("session_date_ny") == sess_date)
        pre_window = day_df.filter(pl.col("bar_open_ts_ny").dt.time() < window_start)
        if pre_window.is_empty():
            continue
        window_start_dt = day_df["bar_open_ts_ny"][0].replace(
            hour=window_start.hour, minute=window_start.minute, second=0, microsecond=0
        )
        window_start_utc = window_start_dt.astimezone(day_df["bar_open_ts"][0].tzinfo)

        high = pre_window["high"].max()
        low = pre_window["low"].min()
        for kind, price in ((f"pre_window_high_{window_name}", high), (f"pre_window_low_{window_name}", low)):
            records.append(
                {
                    "level_id": f"{kind}_{sess_date}",
                    "type": kind,
                    "price": price,
                    "formation_ts": pre_window["bar_close_ts"][-1],
                    "availability_ts": window_start_utc,
                    "timeframe": timeframe,
                    "session_date_ny": sess_date,
                    "status": "active",
                    "sweep_ts": None,
                    "invalidation_reason": None,
                }
            )
    return pl.DataFrame(records, schema=LEVEL_SCHEMA) if records else _empty_levels()


def swing_levels(swings: pl.DataFrame) -> pl.DataFrame:
    """Recast confirmed swings (src/features/swings.py) into the common liquidity
    level schema. availability_ts is passed through unchanged (already causal)."""
    if swings.is_empty():
        return _empty_levels()

    records = []
    for row in swings.iter_rows(named=True):
        kind = "swing_high" if row["kind"] == "high" else "swing_low"
        records.append(
            {
                "level_id": row["swing_id"],
                "type": kind,
                "price": row["price"],
                "formation_ts": row["pivot_ts"],
                "availability_ts": row["availability_ts"],
                "timeframe": row["timeframe"],
                "session_date_ny": None,
                "status": "active",
                "sweep_ts": None,
                "invalidation_reason": None,
            }
        )
    return pl.DataFrame(records, schema=LEVEL_SCHEMA)


def available_levels_as_of(levels: pl.DataFrame, as_of_ts) -> pl.DataFrame:
    if levels.is_empty():
        return levels
    return levels.filter((pl.col("availability_ts") <= as_of_ts) & (pl.col("status") == "active"))
