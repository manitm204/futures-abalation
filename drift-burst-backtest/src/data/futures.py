"""Databento continuous-futures 1-minute bars -> canonical clean bars.

Source: `GLBX.MDP3` `ohlcv-1m`, `stype_in=continuous`, `<ROOT>.v.0` (front month
by volume), as downloaded by test-dabento/main.py. Those prices are RAW contract
prices: at every roll the series jumps from one contract to the next, and that
jump is carry, not a market move.

Roll handling (difference back-adjustment): at each `instrument_id` change the
gap `first open of the new contract - last close of the old contract` is
treated as the roll spread, and every bar BEFORE the roll is shifted by it, so
the most recent contract is unadjusted. Databento rolls at 00:00 UTC on
consecutive minutes, so the gap is a one-minute step and is almost entirely the
calendar spread. Point differences (and so P&L in points) are preserved; price
LEVELS before the last roll are not real traded prices. `price_adjustment` is
kept per bar (adjusted = raw + price_adjustment) so sizing can use the real
contract value.

Sessions: `is_regular_session` marks each root's day session (SESSIONS below):
the NYSE regular session (09:30-16:00 NY) for equity indexes, the same window the
SPY data used, and the NYMEX day session (09:00-14:30 NY, around settlement) for
crude. Trading days and holidays come from the NYSE calendar, and a session ends
no later than that day's NYSE close (early closes). `session_date_ny` is the NY
date for session bars and the CME trading date (bars from 18:00 NY belong to the
next day) for the rest.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from pathlib import Path

import polars as pl

from src.data.calendars import TradingCalendar
from src.data.schemas import CLEAN_BAR_SCHEMA, CLEANING_VERSION, SCHEMA_VERSION

ADJUSTMENT_STATUS = "back_adjusted_difference"


@dataclass(frozen=True)
class ContractSpec:
    multiplier: float   # $ per 1.0 price point
    tick_size: float    # price points per tick


# CME Group contract specifications (outright tick sizes).
CONTRACT_SPECS: dict[str, ContractSpec] = {
    "ES": ContractSpec(50.0, 0.25),
    "NQ": ContractSpec(20.0, 0.25),
    "YM": ContractSpec(5.0, 1.0),
    "RTY": ContractSpec(50.0, 0.10),
    "CL": ContractSpec(1000.0, 0.01),
    "GC": ContractSpec(100.0, 0.10),
    "6E": ContractSpec(125_000.0, 0.00005),
    "6J": ContractSpec(12_500_000.0, 0.0000005),
    "ZN": ContractSpec(1000.0, 1 / 64),
    "ZB": ContractSpec(1000.0, 1 / 32),
}


@dataclass(frozen=True)
class SessionSpec:
    open_ny: time
    close_ny: time
    label: str


NYSE_RTH = SessionSpec(time(9, 30), time(16, 0), "NYSE regular session 09:30-16:00 NY")
SESSIONS: dict[str, SessionSpec] = {
    "ES": NYSE_RTH, "NQ": NYSE_RTH, "YM": NYSE_RTH, "RTY": NYSE_RTH,
    "CL": SessionSpec(time(9, 0), time(14, 30), "NYMEX crude day session 09:00-14:30 NY (settlement window)"),
    "GC": SessionSpec(time(8, 20), time(13, 30), "COMEX gold day session 08:20-13:30 NY (open outcry hours, settlement 13:30)"),
    "6E": SessionSpec(time(8, 20), time(15, 0), "CME FX day session 08:20-15:00 NY (former pit hours)"),
    "6J": SessionSpec(time(8, 20), time(15, 0), "CME FX day session 08:20-15:00 NY (former pit hours)"),
    "ZN": SessionSpec(time(8, 20), time(15, 0), "CBOT Treasury day session 08:20-15:00 NY (former pit hours)"),
    "ZB": SessionSpec(time(8, 20), time(15, 0), "CBOT Treasury day session 08:20-15:00 NY (former pit hours)"),
}


def session_spec(symbol: str) -> SessionSpec:
    if symbol not in SESSIONS:
        raise KeyError(f"No day session defined for {symbol!r}; add it to SESSIONS in src/data/futures.py")
    return SESSIONS[symbol]


def contract_spec(symbol: str) -> ContractSpec:
    if symbol not in CONTRACT_SPECS:
        raise KeyError(f"No contract spec for {symbol!r}; add it to src/data/futures.py")
    return CONTRACT_SPECS[symbol]


def load_databento_symbol(path: Path, symbol: str) -> pl.DataFrame:
    """Raw rows for one root (e.g. "ES") from the combined Databento parquet."""
    df = (pl.scan_parquet(path).filter(pl.col("symbol") == f"{symbol}.v.0")
          .select("ts_event", "instrument_id", "open", "high", "low", "close", "volume")
          .sort("ts_event").collect())
    if df.is_empty():
        raise ValueError(f"No rows for {symbol}.v.0 in {path}")
    if df["ts_event"].is_duplicated().any():
        raise ValueError(f"Duplicate timestamps for {symbol}")
    return df


def back_adjust(df: pl.DataFrame) -> tuple[pl.DataFrame, list[dict]]:
    """Add `price_adjustment` and shift OHLC by it. Returns (frame, roll log)."""
    prev = pl.col("instrument_id").shift()
    is_roll = prev.is_not_null() & (pl.col("instrument_id") != prev)
    # gap = new contract's first open - old contract's last close, on the roll bar.
    g = df.with_columns(pl.when(is_roll).then(pl.col("open") - pl.col("close").shift())
                        .otherwise(0.0).alias("_gap"), is_roll.alias("_roll"))
    # Each bar is shifted by the sum of the gaps of every roll strictly AFTER it,
    # so the old contract's last close lines up with the new contract's first open.
    after = g["_gap"].reverse().cum_sum().reverse() - g["_gap"]
    out = g.with_columns(after.alias("price_adjustment"))
    out = out.with_columns([(pl.col(c) + pl.col("price_adjustment")).alias(c) for c in ("open", "high", "low", "close")])
    log = [{"ts": str(r["ts_event"]), "to_instrument_id": int(r["instrument_id"]), "gap_points": float(r["_gap"])}
           for r in g.filter(pl.col("_roll")).iter_rows(named=True)]
    return out.drop("_gap", "_roll"), log


def to_clean(df: pl.DataFrame, symbol: str, *, calendar: TradingCalendar | None = None) -> pl.DataFrame:
    """Back-adjusted rows -> CLEAN_BAR_SCHEMA (+ price_adjustment); the root's day session
    (SESSIONS) is flagged on NYSE trading days, ending no later than the NYSE close."""
    cal = calendar or TradingCalendar()
    spec = session_spec(symbol)
    ts = pl.col("ts_event").dt.cast_time_unit("us")
    df = df.with_columns(ts.alias("bar_open_ts")).with_columns(
        (pl.col("bar_open_ts") + pl.duration(minutes=1)).alias("bar_close_ts"),
        pl.col("bar_open_ts").dt.convert_time_zone("America/New_York").alias("bar_open_ts_ny"),
    )
    first = df["bar_open_ts_ny"].min().date()
    last = df["bar_open_ts_ny"].max().date()
    def at(ny: datetime, t: time) -> datetime:  # same NY date, wall-clock time t (zoneinfo handles DST)
        return ny.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
    sess = pl.DataFrame(
        [{"d": s.session_date, "o": at(s.open_ny, spec.open_ny), "c": min(at(s.close_ny, spec.close_ny), s.close_ny)}
         for s in cal.sessions(first, last)],
        schema={"d": pl.Date, "o": pl.Datetime("us", "America/New_York"), "c": pl.Datetime("us", "America/New_York")},
    )
    df = df.with_columns(pl.col("bar_open_ts_ny").dt.date().alias("_d")).join(sess, left_on="_d", right_on="d", how="left")
    rth = (pl.col("o").is_not_null() & (pl.col("bar_open_ts_ny") >= pl.col("o")) & (pl.col("bar_open_ts_ny") < pl.col("c")))
    cme_date = (pl.col("bar_open_ts_ny") + pl.duration(hours=6)).dt.date()
    df = df.with_columns(
        rth.fill_null(False).alias("is_regular_session"),
        pl.when(rth).then(pl.col("_d")).otherwise(cme_date).alias("session_date_ny"),
    )
    df = df.with_columns(
        pl.lit(symbol).alias("symbol"), pl.lit("1min").alias("timeframe"),
        (pl.col("bar_close_ts")).dt.convert_time_zone("America/New_York").alias("bar_close_ts_ny"),
        (~pl.col("is_regular_session")).alias("is_extended_hours"),
        pl.col("volume").cast(pl.Int64),
        pl.lit("databento_glbx_mdp3").alias("source"),
        pl.lit(ADJUSTMENT_STATUS).alias("adjustment_status"),
        pl.lit(SCHEMA_VERSION).alias("schema_version"),
        pl.lit(CLEANING_VERSION).alias("cleaning_version"),
    )
    return df.select([*CLEAN_BAR_SCHEMA.keys(), "price_adjustment", "instrument_id"]).sort("bar_open_ts")


def coverage(df: pl.DataFrame) -> dict:
    rth = df.filter(pl.col("is_regular_session"))
    per = rth.group_by("session_date_ny").len()
    return {"actual_coverage_start": str(rth["session_date_ny"].min()),
            "actual_coverage_end": str(rth["session_date_ny"].max()),
            "row_count": df.height, "rth_rows": rth.height, "rth_sessions": per.height,
            "rth_sessions_under_300_bars": int((per["len"] < 300).sum())}


def illiquid_sessions(df: pl.DataFrame, *, min_volume_frac: float = 0.25, lookback: int = 20) -> pl.DataFrame:
    """Day sessions whose volume is below `min_volume_frac` x the median of the previous
    `lookback` sessions. Databento's volume-ranked `.v.0` series sometimes stays on an
    expiring contract for a day or two (seen on GC at month-ends, ~1% of normal volume),
    so its prices there are stale and not tradable in size."""
    per = (df.filter(pl.col("is_regular_session")).group_by("session_date_ny")
           .agg(pl.col("volume").sum().alias("session_volume"), pl.col("instrument_id").last())
           .sort("session_date_ny"))
    per = per.with_columns(pl.col("session_volume").shift().rolling_median(lookback, min_samples=5).alias("ref_volume"))
    return per.filter(pl.col("session_volume") < min_volume_frac * pl.col("ref_volume"))


def drop_sessions(df: pl.DataFrame, dates: list) -> pl.DataFrame:
    """Unflag the given day sessions (their bars stay, as extended hours, so nothing trades there)."""
    hit = pl.col("is_regular_session") & pl.col("session_date_ny").is_in(dates)
    return df.with_columns(pl.when(hit).then(False).otherwise(pl.col("is_regular_session")).alias("is_regular_session"),
                           pl.when(hit).then(True).otherwise(pl.col("is_extended_hours")).alias("is_extended_hours"))
