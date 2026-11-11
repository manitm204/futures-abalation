from datetime import date, datetime, time, timezone

import pytest

from src.utils.time import (
    NaiveTimestampError,
    in_half_open_window,
    is_dst_transition_day,
    localize_ny,
    require_aware,
    session_date_ny,
    to_ny,
    to_utc,
)


def test_require_aware_rejects_naive_datetime() -> None:
    naive = datetime(2024, 1, 2, 9, 30)
    with pytest.raises(NaiveTimestampError):
        require_aware(naive)


def test_require_aware_accepts_aware_datetime() -> None:
    aware = datetime(2024, 1, 2, 9, 30, tzinfo=timezone.utc)
    assert require_aware(aware) is aware


def test_localize_ny_rejects_already_aware() -> None:
    aware = datetime(2024, 1, 2, 9, 30, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        localize_ny(aware)


def test_localize_ny_standard_time_offset() -> None:
    # Jan 2 2024 is EST (UTC-5), not DST.
    ny = localize_ny(datetime(2024, 1, 2, 9, 30))
    utc = to_utc(ny)
    assert utc.hour == 14 and utc.minute == 30


def test_localize_ny_daylight_time_offset() -> None:
    # July 2 2024 is EDT (UTC-4).
    ny = localize_ny(datetime(2024, 7, 2, 9, 30))
    utc = to_utc(ny)
    assert utc.hour == 13 and utc.minute == 30


@pytest.mark.parametrize(
    "d,expected",
    [
        (date(2024, 3, 10), True),  # spring forward (US DST start 2024)
        (date(2024, 11, 3), True),  # fall back (US DST end 2024)
        (date(2024, 3, 11), False),
        (date(2024, 6, 15), False),
        (date(2024, 12, 25), False),
    ],
)
def test_dst_transition_days(d: date, expected: bool) -> None:
    assert is_dst_transition_day(d) is expected


def test_in_half_open_window_boundaries() -> None:
    start, end = time(10, 0), time(11, 0)
    at_start = localize_ny(datetime(2024, 6, 3, 10, 0))
    just_before_end = localize_ny(datetime(2024, 6, 3, 10, 59, 59))
    at_end = localize_ny(datetime(2024, 6, 3, 11, 0))
    before_start = localize_ny(datetime(2024, 6, 3, 9, 59, 59))

    assert in_half_open_window(at_start, start, end) is True
    assert in_half_open_window(just_before_end, start, end) is True
    assert in_half_open_window(at_end, start, end) is False
    assert in_half_open_window(before_start, start, end) is False


def test_session_date_ny_across_midnight_utc() -> None:
    # 23:30 UTC on Jan 1 is 18:30 EST on Jan 1 -- same NY calendar date.
    utc_ts = datetime(2024, 1, 1, 23, 30, tzinfo=timezone.utc)
    assert session_date_ny(utc_ts) == date(2024, 1, 1)
    # 03:30 UTC on Jan 2 is 22:30 EST on Jan 1 -- still Jan 1 in NY.
    utc_ts2 = datetime(2024, 1, 2, 3, 30, tzinfo=timezone.utc)
    assert session_date_ny(utc_ts2) == date(2024, 1, 1)
