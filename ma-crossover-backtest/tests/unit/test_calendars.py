from datetime import date

from src.data.calendars import TradingCalendar


def test_known_holiday_excluded() -> None:
    cal = TradingCalendar()
    days = cal.trading_days(date(2024, 1, 1), date(2024, 1, 5))
    assert date(2024, 1, 1) not in days  # New Year's Day
    assert date(2024, 1, 2) in days


def test_weekend_excluded() -> None:
    cal = TradingCalendar()
    days = cal.trading_days(date(2024, 1, 6), date(2024, 1, 7))
    assert days == []


def test_early_close_detected_thanksgiving_friday() -> None:
    cal = TradingCalendar()
    # Day after Thanksgiving 2023 is a well-known 1pm early close.
    session = cal.session_for(date(2023, 11, 24))
    assert session is not None
    assert session.is_early_close is True


def test_regular_day_not_early_close() -> None:
    cal = TradingCalendar()
    session = cal.session_for(date(2024, 1, 2))
    assert session is not None
    assert session.is_early_close is False


def test_chunk_trading_days_respects_chunk_size() -> None:
    cal = TradingCalendar()
    chunks = cal.chunk_trading_days(date(2024, 1, 2), date(2024, 1, 12), chunk_size=3)
    all_days = cal.trading_days(date(2024, 1, 2), date(2024, 1, 12))
    # Every chunk boundary must itself be a trading day, and chunks must be contiguous
    # in the trading-day sequence (no day skipped, no day duplicated).
    reconstructed: list[date] = []
    for start, end in chunks:
        days_in_chunk = cal.trading_days(start, end)
        assert len(days_in_chunk) <= 3
        reconstructed.extend(days_in_chunk)
    assert reconstructed == all_days


def test_prior_session_skips_weekend() -> None:
    cal = TradingCalendar()
    # Monday 2024-01-08 -> prior session should be Friday 2024-01-05, not Sunday.
    prior = cal.prior_session(date(2024, 1, 8))
    assert prior is not None
    assert prior.session_date == date(2024, 1, 5)
