import pytest

from src.data.aggregation import aggregate_bars
from src.data.calendars import TradingCalendar
from src.data.normalization import normalize_intraday_rows

CAL = TradingCalendar()


def _full_rth_day(date_str: str = "2024-01-02") -> list[dict]:
    rows = []
    for m in range(390):
        hh = 9 + (30 + m) // 60
        mm = (30 + m) % 60
        rows.append(
            {"date": f"{date_str} {hh:02d}:{mm:02d}:00", "open": 1.0, "high": 1.2, "low": 0.8, "close": 1.1, "volume": 10}
        )
    return rows


def _clean_1min(date_str: str = "2024-01-02"):
    return normalize_intraday_rows(_full_rth_day(date_str), symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL)


def test_5min_aggregation_covers_full_session_no_partial() -> None:
    agg = aggregate_bars(_clean_1min(), timeframe="5min")
    assert agg.height == 78  # 390 / 5
    assert agg["is_partial_bar"].sum() == 0
    assert agg["bar_open_ts_ny"][0].strftime("%H:%M") == "09:30"
    assert agg["bar_close_ts_ny"][-1].strftime("%H:%M") == "16:00"


def test_15min_aggregation_covers_full_session_no_partial() -> None:
    agg = aggregate_bars(_clean_1min(), timeframe="15min")
    assert agg.height == 26  # 390 / 15
    assert agg["is_partial_bar"].sum() == 0


def test_1h_aggregation_has_one_partial_final_bar() -> None:
    agg = aggregate_bars(_clean_1min(), timeframe="1h")
    assert agg.height == 7  # 6 full hours + 1 partial 30-min bucket
    assert agg["is_partial_bar"].to_list() == [False] * 6 + [True]
    assert agg["n_source_bars"].to_list()[-1] == 30
    assert agg["bar_open_ts_ny"][0].strftime("%H:%M") == "09:30"


def test_ohlc_aggregation_correctness_on_known_values() -> None:
    rows = [
        {"date": "2024-01-02 09:30:00", "open": 100, "high": 101, "low": 99, "close": 100.5, "volume": 10},
        {"date": "2024-01-02 09:31:00", "open": 100.5, "high": 103, "low": 100, "close": 102, "volume": 20},
        {"date": "2024-01-02 09:32:00", "open": 102, "high": 102.5, "low": 98, "close": 99, "volume": 30},
        {"date": "2024-01-02 09:33:00", "open": 99, "high": 100, "low": 98.5, "close": 99.5, "volume": 40},
        {"date": "2024-01-02 09:34:00", "open": 99.5, "high": 100.2, "low": 99, "close": 100, "volume": 50},
    ]
    df = normalize_intraday_rows(rows, symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL)
    agg = aggregate_bars(df, timeframe="5min")
    assert agg.height == 1
    row = agg.row(0, named=True)
    assert row["open"] == 100  # first bar's open
    assert row["high"] == 103  # max high
    assert row["low"] == 98  # min low
    assert row["close"] == 100  # last bar's close
    assert row["volume"] == 150  # sum


def test_aggregation_rejects_multi_symbol_input() -> None:
    df = _clean_1min()
    df2 = normalize_intraday_rows(_full_rth_day(), symbol="QQQ", timeframe="1min", source="fmp_native", calendar=CAL)
    import polars as pl

    combined = pl.concat([df, df2])
    with pytest.raises(ValueError, match="single symbol"):
        aggregate_bars(combined, timeframe="5min")


def test_aggregation_rejects_unsupported_timeframe() -> None:
    with pytest.raises(ValueError, match="Unsupported"):
        aggregate_bars(_clean_1min(), timeframe="2min")
