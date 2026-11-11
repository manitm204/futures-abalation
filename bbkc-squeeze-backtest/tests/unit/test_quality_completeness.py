from datetime import date

from src.data.calendars import TradingCalendar
from src.data.normalization import normalize_intraday_rows
from src.data.quality import check_intraday_quality

CAL = TradingCalendar()


def test_session_present_but_truncated_is_flagged_incomplete() -> None:
    """A session that has SOME bars but stops well short of the full RTH count
    (e.g. a real FMP data gap observed on QQQ 2024-01-26, which had only 4 of the
    expected 390 bars) must be caught even though missing_session_dates won't
    catch it -- the date IS present in the data, just incomplete."""
    rows = [
        {"date": f"2024-01-02 09:{m:02d}:00", "open": 1, "high": 1.1, "low": 0.9, "close": 1.0, "volume": 10}
        for m in range(30, 34)  # only 4 bars instead of a full 390-bar RTH session
    ]
    df = normalize_intraday_rows(rows, symbol="QQQ", timeframe="1min", source="fmp_native", calendar=CAL)
    report = check_intraday_quality(
        df, symbol="QQQ", timeframe="1min", calendar=CAL,
        expected_start=date(2024, 1, 2), expected_end=date(2024, 1, 2),
    )
    assert date(2024, 1, 2) not in report.missing_session_dates  # date IS present
    assert len(report.incomplete_session_dates) == 1
    d, actual, expected = report.incomplete_session_dates[0]
    assert d == date(2024, 1, 2)
    assert actual == 4
    assert expected == 390


def test_full_session_not_flagged_incomplete() -> None:
    rows = [
        {"date": f"2024-01-02 {9 + (30+m)//60:02d}:{(30+m)%60:02d}:00", "open": 1, "high": 1.1, "low": 0.9, "close": 1.0, "volume": 10}
        for m in range(390)
    ]
    df = normalize_intraday_rows(rows, symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL)
    report = check_intraday_quality(
        df, symbol="SPY", timeframe="1min", calendar=CAL,
        expected_start=date(2024, 1, 2), expected_end=date(2024, 1, 2),
    )
    assert report.incomplete_session_dates == []
