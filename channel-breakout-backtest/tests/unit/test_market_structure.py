from datetime import datetime, timedelta, timezone

import polars as pl

from src.features.market_structure import MarketStructureConfig, detect_market_structure_shifts

BASE = datetime(2024, 1, 2, 14, 30, tzinfo=timezone.utc)


def _bars(ohlc: list[tuple[float, float, float, float]]) -> pl.DataFrame:
    n = len(ohlc)
    open_ts = [BASE + timedelta(minutes=i) for i in range(n)]
    o, h, l, c = zip(*ohlc)
    return pl.DataFrame(
        {
            "symbol": ["SPY"] * n, "bar_open_ts": open_ts,
            "open": [float(x) for x in o], "high": [float(x) for x in h],
            "low": [float(x) for x in l], "close": [float(x) for x in c],
        }
    )


def _sweep(direction: str, confirmation_ts) -> pl.DataFrame:
    return pl.DataFrame(
        {"sweep_id": ["swp1"], "direction": [direction], "confirmation_ts": [confirmation_ts]}
    )


def _swing(swing_id: str, kind: str, price: float, availability_ts) -> pl.DataFrame:
    return pl.DataFrame(
        {"swing_id": [swing_id], "kind": [kind], "price": [price], "availability_ts": [availability_ts]}
    )


def test_bullish_mss_breaks_swing_high_close_mode() -> None:
    bars = _bars(
        [
            (100, 100.5, 99.5, 100),  # sweep confirmation bar
            (100, 101.5, 99.9, 101.2),  # breaks swing high (100.8) on close
        ]
    )
    sweeps = _sweep("bullish", bars["bar_open_ts"][0])
    swings = _swing("swh1", "high", 100.8, bars["bar_open_ts"][0] - timedelta(minutes=10))
    mss = detect_market_structure_shifts(bars, sweeps, swings, config=MarketStructureConfig(break_mode="close"))
    assert mss.height == 1
    assert mss.row(0, named=True)["reference_swing_id"] == "swh1"


def test_bearish_mss_breaks_swing_low() -> None:
    bars = _bars(
        [
            (100, 100.5, 99.5, 100),
            (100, 100.2, 98.5, 98.7),  # breaks swing low (99.0) on close
        ]
    )
    sweeps = _sweep("bearish", bars["bar_open_ts"][0])
    swings = _swing("swl1", "low", 99.0, bars["bar_open_ts"][0] - timedelta(minutes=10))
    mss = detect_market_structure_shifts(bars, sweeps, swings, config=MarketStructureConfig(break_mode="close"))
    assert mss.height == 1


def test_swing_not_yet_available_at_sweep_confirmation_is_excluded() -> None:
    bars = _bars([(100, 100.5, 99.5, 100), (100, 101.5, 99.9, 101.2)])
    sweep_conf_ts = bars["bar_open_ts"][0]
    sweeps = _sweep("bullish", sweep_conf_ts)
    # swing becomes available AFTER the sweep confirms -- must not be usable as reference
    future_swing = _swing("swh1", "high", 100.8, sweep_conf_ts + timedelta(minutes=5))
    mss = detect_market_structure_shifts(bars, sweeps, future_swing, config=MarketStructureConfig())
    assert mss.height == 0


def test_wick_mode_breaks_on_high_not_close() -> None:
    bars = _bars(
        [
            (100, 100.5, 99.5, 100),
            (100, 101.5, 99.9, 100.3),  # high breaks 100.8? no high=101.5>100.8 wick break; close=100.3 no close break
        ]
    )
    sweeps = _sweep("bullish", bars["bar_open_ts"][0])
    swings = _swing("swh1", "high", 100.8, bars["bar_open_ts"][0] - timedelta(minutes=10))
    mss_close = detect_market_structure_shifts(bars, sweeps, swings, config=MarketStructureConfig(break_mode="close"))
    mss_wick = detect_market_structure_shifts(bars, sweeps, swings, config=MarketStructureConfig(break_mode="wick"))
    assert mss_close.height == 0
    assert mss_wick.height == 1


def test_max_bars_after_sweep_limits_search() -> None:
    bars = _bars(
        [
            (100, 100.5, 99.5, 100),  # sweep bar
            (100, 100.3, 99.8, 100.1),
            (100.1, 100.3, 99.9, 100.2),
            (100.2, 101.5, 99.9, 101.2),  # breaks here, at bars_after_sweep=3
        ]
    )
    sweeps = _sweep("bullish", bars["bar_open_ts"][0])
    swings = _swing("swh1", "high", 100.8, bars["bar_open_ts"][0] - timedelta(minutes=10))
    mss_limited = detect_market_structure_shifts(
        bars, sweeps, swings, config=MarketStructureConfig(break_mode="close", max_bars_after_sweep=2)
    )
    mss_unlimited = detect_market_structure_shifts(
        bars, sweeps, swings, config=MarketStructureConfig(break_mode="close", max_bars_after_sweep=10)
    )
    assert mss_limited.height == 0
    assert mss_unlimited.height == 1
