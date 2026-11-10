from datetime import date

import polars as pl

from src.data.calendars import TradingCalendar
from src.data.normalization import normalize_intraday_rows
from src.data.quality import check_intraday_quality, compare_native_vs_aggregated

CAL = TradingCalendar()


def test_clean_day_has_no_quality_issues() -> None:
    rows = [
        {"date": f"2024-01-02 09:{m:02d}:00", "open": 1, "high": 1.1, "low": 0.9, "close": 1.0, "volume": 10}
        for m in range(30, 60)
    ]
    df = normalize_intraday_rows(rows, symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL)
    report = check_intraday_quality(
        df, symbol="SPY", timeframe="1min", calendar=CAL,
        expected_start=date(2024, 1, 2), expected_end=date(2024, 1, 2),
    )
    assert report.invalid_ohlc_count == 0
    assert report.duplicate_bar_open_ts == 0
    assert report.negative_price_count == 0
    assert report.unsorted is False


def test_detects_invalid_ohlc_high_below_low() -> None:
    df = pl.DataFrame(
        {
            "symbol": ["SPY"], "timeframe": ["1min"],
            "bar_open_ts": [None], "bar_close_ts": [None],
            "bar_open_ts_ny": [None], "bar_close_ts_ny": [None],
            "session_date_ny": [date(2024, 1, 2)],
            "open": [10.0], "high": [9.0], "low": [11.0], "close": [10.0], "volume": [100],
            "is_regular_session": [True], "is_extended_hours": [False],
            "source": ["fmp_native"], "adjustment_status": ["split_adjusted"],
            "schema_version": ["1.0.0"], "cleaning_version": ["1.0.0"],
        }
    ).with_columns(
        pl.col("bar_open_ts").cast(pl.Datetime("us", "UTC")),
        pl.col("bar_close_ts").cast(pl.Datetime("us", "UTC")),
    )
    report = check_intraday_quality(
        df, symbol="SPY", timeframe="1min", calendar=CAL,
        expected_start=date(2024, 1, 2), expected_end=date(2024, 1, 2),
    )
    assert report.invalid_ohlc_count == 1


def test_detects_missing_session_dates() -> None:
    # Only Jan 2 present; Jan 3 and Jan 4 (both trading days) expected but missing.
    rows = [{"date": "2024-01-02 09:30:00", "open": 1, "high": 1.1, "low": 0.9, "close": 1.0, "volume": 10}]
    df = normalize_intraday_rows(rows, symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL)
    report = check_intraday_quality(
        df, symbol="SPY", timeframe="1min", calendar=CAL,
        expected_start=date(2024, 1, 2), expected_end=date(2024, 1, 4),
    )
    assert date(2024, 1, 3) in report.missing_session_dates
    assert date(2024, 1, 4) in report.missing_session_dates
    assert date(2024, 1, 2) not in report.missing_session_dates


def test_detects_large_intraday_gap() -> None:
    rows = [
        {"date": "2024-01-02 09:30:00", "open": 1, "high": 1.1, "low": 0.9, "close": 1.0, "volume": 10},
        {"date": "2024-01-02 10:00:00", "open": 1, "high": 1.1, "low": 0.9, "close": 1.0, "volume": 10},  # 30min gap
    ]
    df = normalize_intraday_rows(rows, symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL)
    report = check_intraday_quality(
        df, symbol="SPY", timeframe="1min", calendar=CAL,
        expected_start=date(2024, 1, 2), expected_end=date(2024, 1, 2), gap_threshold_minutes=15,
    )
    assert report.large_gap_count == 1


def test_empty_frame_reports_all_sessions_missing() -> None:
    df = normalize_intraday_rows([], symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL)
    report = check_intraday_quality(
        df, symbol="SPY", timeframe="1min", calendar=CAL,
        expected_start=date(2024, 1, 2), expected_end=date(2024, 1, 4),
    )
    assert report.row_count == 0
    assert len(report.missing_session_dates) == 3


def test_compare_native_vs_aggregated_identical_frames_zero_mismatch() -> None:
    rows = [
        {"date": "2024-01-02 09:30:00", "open": 1, "high": 1.2, "low": 0.8, "close": 1.1, "volume": 100},
    ]
    df = normalize_intraday_rows(rows, symbol="SPY", timeframe="5min", source="fmp_native", calendar=CAL)
    result = compare_native_vs_aggregated(df, df)
    assert result["overlapping_bars"] == 1
    assert result["mismatch_count_open"] == 0
    assert result["max_abs_diff_close"] == 0.0
