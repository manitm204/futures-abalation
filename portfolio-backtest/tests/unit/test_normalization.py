from datetime import date

import pytest

from src.data.calendars import TradingCalendar
from src.data.normalization import normalize_intraday_rows
from src.data.schemas import assert_clean_schema

CAL = TradingCalendar()


def _row(date_str: str, o: float = 1.0, h: float = 1.1, l: float = 0.9, c: float = 1.05, v: int = 100) -> dict:
    return {"date": date_str, "open": o, "high": h, "low": l, "close": c, "volume": v}


def test_normalize_open_labeled_bar_open_at_930_maps_to_1430_utc() -> None:
    rows = [_row("2024-01-02 09:30:00")]
    df = normalize_intraday_rows(rows, symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL)
    assert_clean_schema(df)
    ts = df["bar_open_ts"][0]
    assert (ts.hour, ts.minute) == (14, 30)


def test_bar_close_is_open_plus_interval() -> None:
    rows = [_row("2024-01-02 09:30:00")]
    df = normalize_intraday_rows(rows, symbol="SPY", timeframe="5min", source="fmp_native", calendar=CAL)
    open_ts = df["bar_open_ts_ny"][0]
    close_ts = df["bar_close_ts_ny"][0]
    assert (close_ts - open_ts).total_seconds() == 5 * 60


def test_first_and_last_rth_bar_flagged_regular_session() -> None:
    rows = [_row("2024-01-02 09:30:00"), _row("2024-01-02 15:59:00")]
    df = normalize_intraday_rows(rows, symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL)
    assert df["is_regular_session"].to_list() == [True, True]


def test_bar_at_session_close_boundary_excluded_half_open() -> None:
    # 16:00:00 is the session close -- half-open [open, close) means a bar labeled
    # exactly at close should NOT be flagged regular-session (would only happen if
    # bad/unexpected data appears at that exact label).
    rows = [_row("2024-01-02 16:00:00")]
    df = normalize_intraday_rows(rows, symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL)
    assert df["is_regular_session"].to_list() == [False]


def test_dedup_exact_duplicate_bar_open_ts() -> None:
    rows = [_row("2024-01-02 09:30:00"), _row("2024-01-02 09:30:00")]
    df = normalize_intraday_rows(rows, symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL)
    assert df.height == 1


def test_output_sorted_by_bar_open_ts() -> None:
    rows = [_row("2024-01-02 09:32:00"), _row("2024-01-02 09:30:00"), _row("2024-01-02 09:31:00")]
    df = normalize_intraday_rows(rows, symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL)
    ts = df["bar_open_ts"].to_list()
    assert ts == sorted(ts)


def test_dst_spring_forward_localization() -> None:
    # 2024-03-10 is US DST start; 09:30 local should map to 13:30 UTC (EDT, UTC-4),
    # not 14:30 (which would be the EST offset).
    rows = [_row("2024-03-11 09:30:00")]  # first trading day after the spring-forward Sunday
    df = normalize_intraday_rows(rows, symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL)
    ts = df["bar_open_ts"][0]
    assert ts.hour == 13


def test_rejects_unverified_bar_label_convention() -> None:
    with pytest.raises(ValueError, match="not verified"):
        normalize_intraday_rows(
            [_row("2024-01-02 09:30:00")],
            symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL,
            bar_label_convention="close",  # type: ignore[arg-type]
        )


def test_empty_rows_returns_empty_conformant_frame() -> None:
    df = normalize_intraday_rows([], symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL)
    assert df.height == 0
    assert_clean_schema(df)
