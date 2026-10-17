"""NYSE/NYSE Arca session calendar wrapper.

Single source of truth for: which dates are trading days, regular-session open/close
(America/New_York), and early closes. Used by the downloader (to chunk requests),
normalization (to flag regular vs extended-hours bars and detect missing sessions),
and aggregation (to align resampling to session boundaries, not arbitrary UTC
boundaries).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time

import pandas_market_calendars as mcal

from src.utils.time import NY_TZ, localize_ny

CALENDAR_NAME = "NYSE"
REGULAR_OPEN = time(9, 30)
REGULAR_CLOSE = time(16, 0)


@dataclass(frozen=True)
class Session:
    session_date: date
    open_ny: datetime
    close_ny: datetime
    is_early_close: bool


class TradingCalendar:
    def __init__(self, calendar_name: str = CALENDAR_NAME) -> None:
        self._cal = mcal.get_calendar(calendar_name)
        self._schedule_cache: dict[tuple[date, date], "list[Session]"] = {}

    def sessions(self, start: date, end: date) -> list[Session]:
        """Trading sessions in [start, end] inclusive, ascending by date."""
        key = (start, end)
        if key in self._schedule_cache:
            return self._schedule_cache[key]

        schedule = self._cal.schedule(start_date=start, end_date=end)
        sessions: list[Session] = []
        for session_date, row in schedule.iterrows():
            open_ny = row["market_open"].tz_convert(NY_TZ).to_pydatetime()
            close_ny = row["market_close"].tz_convert(NY_TZ).to_pydatetime()
            is_early = close_ny.timetz().replace(tzinfo=None) < REGULAR_CLOSE
            sessions.append(
                Session(
                    session_date=session_date.date(),
                    open_ny=open_ny,
                    close_ny=close_ny,
                    is_early_close=is_early,
                )
            )
        self._schedule_cache[key] = sessions
        return sessions

    def trading_days(self, start: date, end: date) -> list[date]:
        return [s.session_date for s in self.sessions(start, end)]

    def is_trading_day(self, d: date) -> bool:
        return len(self.trading_days(d, d)) == 1

    def session_for(self, d: date) -> Session | None:
        days = self.sessions(d, d)
        return days[0] if days else None

    def prior_session(self, d: date, *, lookback_days: int = 10) -> Session | None:
        """The most recent trading session strictly before `d`."""
        from datetime import timedelta

        window_start = d - timedelta(days=lookback_days)
        sessions = [s for s in self.sessions(window_start, d) if s.session_date < d]
        return sessions[-1] if sessions else None

    def chunk_trading_days(self, start: date, end: date, *, chunk_size: int) -> list[tuple[date, date]]:
        """Split the trading days in [start, end] into consecutive chunks of `chunk_size`.

        Used to respect FMP's confirmed 3-trading-day-per-request cap on the 1min
        endpoint: request each chunk's (first_day, last_day) as (from, to).
        """
        days = self.trading_days(start, end)
        chunks: list[tuple[date, date]] = []
        for i in range(0, len(days), chunk_size):
            group = days[i : i + chunk_size]
            chunks.append((group[0], group[-1]))
        return chunks
