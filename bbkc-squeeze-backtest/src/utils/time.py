"""Canonical timestamp contract for the framework.

Rules (see project spec / README "Timestamp contract"):
  - All timestamps that reach features/signals/execution MUST be timezone-aware.
  - Canonical storage timezone is UTC. A parallel `timestamp_ny` column carries the
    America/New_York (IANA) local representation for session/window logic.
  - Bars are normalized to explicit `bar_open_ts` / `bar_close_ts` columns using a
    half-open interval [bar_open_ts, bar_close_ts). No column is ever named plain
    `timestamp` past the normalization layer, to force callers to be explicit about
    which edge of the bar they mean.
  - Whether a raw provider timestamp is bar-open or bar-close labeled is a data-source
    property, not something this module guesses. See src/data/normalization.py and
    the ASSUMPTIONS.md entry for FMP's convention.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

NY_TZ = ZoneInfo("America/New_York")
UTC_TZ = timezone.utc


class NaiveTimestampError(ValueError):
    """Raised whenever a timezone-naive datetime reaches code that requires tz-aware input."""


def require_aware(dt: datetime, *, label: str = "timestamp") -> datetime:
    """Fail loudly if `dt` is timezone-naive. Never silently localize."""
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        raise NaiveTimestampError(
            f"{label} is timezone-naive ({dt!r}). Refusing to guess a timezone. "
            "Naive timestamps must never reach feature/signal/execution code."
        )
    return dt


def to_utc(dt: datetime, *, label: str = "timestamp") -> datetime:
    require_aware(dt, label=label)
    return dt.astimezone(UTC_TZ)


def to_ny(dt: datetime, *, label: str = "timestamp") -> datetime:
    require_aware(dt, label=label)
    return dt.astimezone(NY_TZ)


def localize_ny(naive_dt: datetime, *, label: str = "timestamp") -> datetime:
    """Explicitly attach the America/New_York IANA zone to a naive local wall-clock time.

    This is the ONLY sanctioned place to attach a timezone to a naive datetime, and it
    must only be called when the source convention (e.g. FMP intraday `date` field) has
    been documented/verified as NY-local wall-clock time. Uses IANA rules so DST is
    handled correctly (no fixed UTC offsets).
    """
    if naive_dt.tzinfo is not None:
        raise ValueError(f"{label} is already timezone-aware; refusing to re-localize: {naive_dt!r}")
    return naive_dt.replace(tzinfo=NY_TZ)


def in_half_open_window(
    ts_ny: datetime, window_start: time, window_end: time, *, label: str = "timestamp"
) -> bool:
    """True if the NY-local wall-clock time-of-day of `ts_ny` falls in [window_start, window_end)."""
    require_aware(ts_ny, label=label)
    t = ts_ny.timetz().replace(tzinfo=None)
    return window_start <= t < window_end


def session_date_ny(ts_ny: datetime, *, label: str = "timestamp") -> date:
    require_aware(ts_ny, label=label)
    return ts_ny.astimezone(NY_TZ).date()


def is_dst_transition_day(d: date, tz: ZoneInfo = NY_TZ) -> bool:
    """True if the UTC offset at local midnight differs from local 23:00 on date `d`."""
    start = datetime.combine(d, time(0, 0), tzinfo=tz)
    end = datetime.combine(d, time(23, 0), tzinfo=tz)
    return start.utcoffset() != end.utcoffset()


def bar_close_from_open(bar_open_ts: datetime, bar_minutes: int) -> datetime:
    require_aware(bar_open_ts, label="bar_open_ts")
    return bar_open_ts + timedelta(minutes=bar_minutes)
