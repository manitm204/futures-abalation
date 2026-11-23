from datetime import time

import polars as pl

from src.data.calendars import TradingCalendar
from src.data.normalization import normalize_intraday_rows
from src.features.liquidity import (
    available_levels_as_of,
    pre_window_extremes,
    prior_session_extremes,
    swing_levels,
)
from src.features.swings import SwingConfig, detect_swings

CAL = TradingCalendar()


def _rth_day(date_str: str, base_price: float) -> list[dict]:
    rows = []
    for m in range(390):
        hh = 9 + (30 + m) // 60
        mm = (30 + m) % 60
        # ramp price up during the day so high/low are distinguishable
        px = base_price + m * 0.01
        rows.append(
            {
                "date": f"{date_str} {hh:02d}:{mm:02d}:00",
                "open": px, "high": px + 0.05, "low": px - 0.05, "close": px, "volume": 10,
            }
        )
    return rows


def _two_day_df() -> pl.DataFrame:
    rows = _rth_day("2024-01-02", 100.0) + _rth_day("2024-01-03", 200.0)
    return normalize_intraday_rows(rows, symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL)


def test_prior_session_extremes_apply_to_next_session_only() -> None:
    df = _two_day_df()
    levels = prior_session_extremes(df, calendar=CAL, timeframe="1min")
    # Jan 2 has no prior session in this 2-day dataset -> only levels for Jan 3 exist
    assert set(levels["session_date_ny"].to_list()) == {df["session_date_ny"].unique().sort().to_list()[1]}
    high_level = levels.filter(pl.col("type") == "prior_session_high").row(0, named=True)
    day1 = df.filter(pl.col("session_date_ny") == df["session_date_ny"][0])
    assert high_level["price"] == day1["high"].max()


def test_prior_session_level_not_available_until_next_session_open() -> None:
    df = _two_day_df()
    levels = prior_session_extremes(df, calendar=CAL, timeframe="1min")
    day2_open = df.filter(pl.col("session_date_ny") == df["session_date_ny"].unique().sort()[1])["bar_open_ts"][0]

    just_before = day2_open.replace(microsecond=0)
    from datetime import timedelta

    before_open = day2_open - timedelta(minutes=1)
    assert available_levels_as_of(levels, before_open).height == 0
    assert available_levels_as_of(levels, day2_open).height == 2  # high + low


def test_pre_window_extremes_freeze_at_window_start() -> None:
    df = _two_day_df().filter(pl.col("session_date_ny") == pl.col("session_date_ny").min())
    window_start = time(10, 0)
    levels = pre_window_extremes(df, window_start=window_start, window_name="ny_am", timeframe="1min")
    assert levels.height == 2  # high + low for the one session

    # availability_ts must be exactly the window start in UTC, not later
    row = levels.row(0, named=True)
    assert row["availability_ts"].time().hour == 15  # 10:00 NY = 15:00 UTC in Jan (EST)

    # the high/low must only reflect bars strictly before 10:00, not the whole day
    pre_window_bars = df.filter(pl.col("bar_open_ts_ny").dt.time() < window_start)
    expected_high = pre_window_bars["high"].max()
    highs = levels.filter(pl.col("type") == "pre_window_high_ny_am")
    assert highs["price"][0] == expected_high


def test_swing_levels_preserve_availability_ts() -> None:
    df = _two_day_df()
    swings = detect_swings(df, config=SwingConfig(left_bars=3, right_bars=3))
    levels = swing_levels(swings)
    if swings.height > 0:
        assert levels.height == swings.height
        assert levels["availability_ts"].to_list() == swings["availability_ts"].to_list()
        assert set(levels["type"].unique().to_list()) <= {"swing_high", "swing_low"}


def test_available_levels_as_of_excludes_inactive_status() -> None:
    df = _two_day_df()
    levels = prior_session_extremes(df, calendar=CAL, timeframe="1min")
    levels = levels.with_columns(pl.lit("swept").alias("status"))
    far_future = levels["availability_ts"].max()
    assert available_levels_as_of(levels, far_future).height == 0
