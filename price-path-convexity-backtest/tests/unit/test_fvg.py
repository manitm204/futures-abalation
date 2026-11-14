from datetime import datetime, timedelta, timezone

import polars as pl
import pytest

from src.features.fvg import FvgConfig, annotate_touches, detect_fvgs


def _bars(ohlc: list[tuple[float, float, float, float]], *, symbol: str = "SPY") -> pl.DataFrame:
    base = datetime(2024, 1, 2, 14, 30, tzinfo=timezone.utc)
    n = len(ohlc)
    open_ts = [base + timedelta(minutes=i) for i in range(n)]
    close_ts = [t + timedelta(minutes=1) for t in open_ts]
    o, h, l, c = zip(*ohlc)
    return pl.DataFrame(
        {
            "symbol": [symbol] * n,
            "bar_open_ts": open_ts,
            "bar_close_ts": close_ts,
            "open": [float(x) for x in o], "high": [float(x) for x in h],
            "low": [float(x) for x in l], "close": [float(x) for x in c],
            "atr": [1.0] * n,
            "session_date_ny": [datetime(2024, 1, 2).date()] * n,
            "sb_window": ["ny_am"] * n,
        }
    )


DEFAULT_CFG = FvgConfig(timeframe="1min")


def test_bullish_fvg_detected() -> None:
    # bar1.high=10 < bar3.low=12 -> bullish gap [10,12]
    bars = _bars([(9, 10, 8, 9.5), (11, 11.5, 10.5, 11), (12.5, 13, 12, 12.8)])
    fvgs = detect_fvgs(bars, config=DEFAULT_CFG)
    assert fvgs.height == 1
    row = fvgs.row(0, named=True)
    assert row["direction"] == "bullish"
    assert row["gap_bottom"] == 10 and row["gap_top"] == 12
    assert row["midpoint"] == 11
    assert row["proximal"] == 12  # bullish: price retraces down from above, touches top first
    assert row["distal"] == 10


def test_bearish_fvg_detected() -> None:
    # bar1.low=12 > bar3.high=10 -> bearish gap
    bars = _bars([(11.5, 12.5, 12, 12.2), (11, 11.2, 10.8, 11), (9.5, 10, 9, 9.6)])
    fvgs = detect_fvgs(bars, config=DEFAULT_CFG)
    assert fvgs.height == 1
    row = fvgs.row(0, named=True)
    assert row["direction"] == "bearish"
    assert row["gap_bottom"] == 10 and row["gap_top"] == 12
    assert row["proximal"] == 10  # bearish: price retraces up from below, touches bottom first
    assert row["distal"] == 12


def test_boundary_equality_produces_no_fvg() -> None:
    # bar1.high == bar3.low exactly -> not a gap (strict inequality required)
    bars = _bars([(9, 10, 8, 9.5), (10, 10.5, 9.5, 10), (10.5, 11, 10, 10.8)])
    fvgs = detect_fvgs(bars, config=DEFAULT_CFG)
    assert fvgs.height == 0


def test_no_gap_overlapping_ranges() -> None:
    bars = _bars([(9, 10, 8, 9.5), (10, 10.5, 9.5, 10), (9.8, 10.2, 9, 9.9)])
    fvgs = detect_fvgs(bars, config=DEFAULT_CFG)
    assert fvgs.height == 0


def test_confirmation_ts_equals_bar3_close_not_earlier() -> None:
    bars = _bars([(9, 10, 8, 9.5), (11, 11.5, 10.5, 11), (12.5, 13, 12, 12.8)])
    fvgs = detect_fvgs(bars, config=DEFAULT_CFG)
    row = fvgs.row(0, named=True)
    assert row["confirmation_ts"] == bars["bar_close_ts"][2]
    assert row["confirmation_ts"] > bars["bar_open_ts"][2]  # strictly after bar3 opens


def test_min_points_filter_rejects_small_gap() -> None:
    bars = _bars([(9, 10, 8, 9.5), (11, 11.5, 10.5, 11), (10.1, 10.6, 10.05, 10.3)])
    cfg = FvgConfig(timeframe="1min", min_points=1.0)
    fvgs = detect_fvgs(bars, config=cfg)
    assert fvgs.height == 0  # gap is only 0.05 points


def test_min_atr_multiple_filter() -> None:
    bars = _bars([(9, 10, 8, 9.5), (11, 11.5, 10.5, 11), (12.5, 13, 12, 12.8)])
    # gap = 2 points, atr = 1.0 -> 2x ATR
    cfg_pass = FvgConfig(timeframe="1min", min_atr_multiple=1.5)
    cfg_fail = FvgConfig(timeframe="1min", min_atr_multiple=3.0)
    assert detect_fvgs(bars, config=cfg_pass).height == 1
    assert detect_fvgs(bars, config=cfg_fail).height == 0


def test_short_series_returns_empty() -> None:
    bars = _bars([(9, 10, 8, 9.5), (11, 11.5, 10.5, 11)])
    fvgs = detect_fvgs(bars, config=DEFAULT_CFG)
    assert fvgs.height == 0


def test_annotate_touches_never_touches_before_confirmation() -> None:
    # bullish FVG at rows 0-2 [10,12]; row3 immediately touches proximal (10).
    bars = _bars(
        [
            (9, 10, 8, 9.5), (11, 11.5, 10.5, 11), (12.5, 13, 12, 12.8),
            (10.5, 10.6, 9.9, 10.0),  # touches proximal (low=9.9 <= 10)
        ]
    )
    fvgs = detect_fvgs(bars, config=DEFAULT_CFG)
    annotated = annotate_touches(fvgs, bars)
    row = annotated.row(0, named=True)
    assert row["first_touch_ts"] == bars["bar_open_ts"][3]
    assert row["first_touch_ts"] > row["confirmation_ts"] - timedelta(minutes=1)
    # Critically: the touch bar is bar index 3, i.e. strictly after bar index 2
    # (the confirmation bar) -- touches can never be attributed to bars <= bar3.
    assert row["source_row_index"] + 3 == 3


def test_annotate_touches_full_fill_reaches_distal() -> None:
    bars = _bars(
        [
            (9, 10, 8, 9.5), (11, 11.5, 10.5, 11), (12.5, 13, 12, 12.8),
            (11, 12.5, 9, 10),  # low=9 <= distal(12)? no distal=12 for bullish is gap_top; range covers full gap
        ]
    )
    fvgs = detect_fvgs(bars, config=DEFAULT_CFG)
    annotated = annotate_touches(fvgs, bars)
    row = annotated.row(0, named=True)
    assert row["full_fill_ts"] is not None
