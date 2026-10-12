from datetime import datetime, timedelta, timezone

import polars as pl

from src.features.swings import SwingConfig, available_swings_as_of, detect_swings


def _bars(highs: list[float], lows: list[float]) -> pl.DataFrame:
    base = datetime(2024, 1, 2, 14, 30, tzinfo=timezone.utc)
    n = len(highs)
    open_ts = [base + timedelta(minutes=i) for i in range(n)]
    close_ts = [t + timedelta(minutes=1) for t in open_ts]
    return pl.DataFrame(
        {
            "symbol": ["SPY"] * n,
            "bar_open_ts": open_ts, "bar_close_ts": close_ts,
            "high": [float(x) for x in highs], "low": [float(x) for x in lows],
        }
    )


def test_simple_swing_high_detected_at_center() -> None:
    highs = [1, 2, 3, 5, 3, 2, 1]  # peak at index 3
    lows = [x - 0.5 for x in highs]
    df = _bars(highs, lows)
    swings = detect_swings(df, config=SwingConfig(left_bars=2, right_bars=2))
    high_swings = swings.filter(pl.col("kind") == "high")
    assert high_swings.height == 1
    assert high_swings["source_row_index"][0] == 3
    assert high_swings["price"][0] == 5


def test_simple_swing_low_detected_at_center() -> None:
    lows = [5, 4, 3, 1, 3, 4, 5]  # trough at index 3
    highs = [x + 0.5 for x in lows]
    df = _bars(highs, lows)
    swings = detect_swings(df, config=SwingConfig(left_bars=2, right_bars=2))
    low_swings = swings.filter(pl.col("kind") == "low")
    assert low_swings.height == 1
    assert low_swings["source_row_index"][0] == 3


def test_availability_ts_is_right_bars_after_pivot_close() -> None:
    highs = [1, 2, 3, 5, 3, 2, 1]
    lows = [x - 0.5 for x in highs]
    df = _bars(highs, lows)
    swings = detect_swings(df, config=SwingConfig(left_bars=2, right_bars=2))
    row = swings.filter(pl.col("kind") == "high").row(0, named=True)
    # pivot at index 3, right=2 -> availability = bar index 5's close
    assert row["availability_ts"] == df["bar_close_ts"][5]
    assert row["pivot_ts"] == df["bar_open_ts"][3]
    assert row["availability_ts"] > row["pivot_ts"]


def test_pivot_never_available_before_right_bars_close() -> None:
    """Deliberate future-leak check: querying available_swings_as_of at a timestamp
    BEFORE the right-side confirmation bars have closed must exclude the pivot,
    even though the pivot's price extreme already 'happened' at pivot_ts."""
    highs = [1, 2, 3, 5, 3, 2, 1]
    lows = [x - 0.5 for x in highs]
    df = _bars(highs, lows)
    swings = detect_swings(df, config=SwingConfig(left_bars=2, right_bars=2))

    pivot_ts = df["bar_open_ts"][3]
    just_after_pivot_opens = pivot_ts + timedelta(seconds=30)  # still mid-formation, before confirmation
    available = available_swings_as_of(swings, just_after_pivot_opens)
    assert available.height == 0  # NOT yet available, despite pivot already having occurred

    availability_ts = df["bar_close_ts"][5]
    available_after = available_swings_as_of(swings, availability_ts)
    assert available_after.height == 1  # now available


def test_no_swing_when_flat() -> None:
    highs = [3, 3, 3, 3, 3, 3, 3]
    lows = [2, 2, 2, 2, 2, 2, 2]
    df = _bars(highs, lows)
    swings = detect_swings(df, config=SwingConfig(left_bars=2, right_bars=2, tie_handling="reject"))
    assert swings.height == 0


def test_min_prominence_filters_shallow_pivot() -> None:
    highs = [1, 2, 3, 3.1, 3, 2, 1]  # shallow peak, prominence only 0.1
    lows = [x - 0.5 for x in highs]
    df = _bars(highs, lows)
    swings_strict = detect_swings(df, config=SwingConfig(left_bars=2, right_bars=2, min_prominence_points=1.0))
    swings_loose = detect_swings(df, config=SwingConfig(left_bars=2, right_bars=2, min_prominence_points=0.0))
    assert swings_strict.filter(pl.col("kind") == "high").height == 0
    assert swings_loose.filter(pl.col("kind") == "high").height == 1


def test_too_short_series_returns_empty() -> None:
    df = _bars([1, 2, 3], [0.5, 1.5, 2.5])
    swings = detect_swings(df, config=SwingConfig(left_bars=5, right_bars=5))
    assert swings.height == 0
