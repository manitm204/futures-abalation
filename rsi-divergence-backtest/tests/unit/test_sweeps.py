from datetime import datetime, timedelta, timezone

import polars as pl

from src.features.sweeps import SweepConfig, detect_sweeps


def _bars(ohlc: list[tuple[float, float, float, float]]) -> pl.DataFrame:
    base = datetime(2024, 1, 2, 14, 30, tzinfo=timezone.utc)
    n = len(ohlc)
    open_ts = [base + timedelta(minutes=i) for i in range(n)]
    o, h, l, c = zip(*ohlc)
    return pl.DataFrame(
        {
            "symbol": ["SPY"] * n,
            "bar_open_ts": open_ts,
            "open": [float(x) for x in o], "high": [float(x) for x in h],
            "low": [float(x) for x in l], "close": [float(x) for x in c],
            "atr": [1.0] * n,
        }
    )


def _level(level_id: str, level_type: str, price: float, avail_ts) -> pl.DataFrame:
    return pl.DataFrame(
        {
            "level_id": [level_id], "type": [level_type], "price": [price],
            "availability_ts": [avail_ts],
        }
    )


def test_bullish_sweep_same_bar_reclaim() -> None:
    bars = _bars([(100, 101, 98, 100.5)])  # low=98 sweeps below level=99, close=100.5 reclaims
    levels = _level("lvl1", "prior_session_low", 99.0, bars["bar_open_ts"][0])
    sweeps = detect_sweeps(bars, levels, config=SweepConfig(k_bars=3))
    assert sweeps.height == 1
    row = sweeps.row(0, named=True)
    assert row["direction"] == "bullish"
    assert row["bars_to_reclaim"] == 0
    assert row["penetration_points"] == 1.0


def test_bullish_sweep_reclaim_within_k_bars() -> None:
    bars = _bars(
        [
            (100, 101, 98, 98.5),  # penetrates, does not reclaim (close < level)
            (98.5, 99, 98, 98.7),  # still below
            (98.7, 100.5, 98.5, 100.2),  # reclaims here (close > 99)
        ]
    )
    levels = _level("lvl1", "prior_session_low", 99.0, bars["bar_open_ts"][0])
    sweeps = detect_sweeps(bars, levels, config=SweepConfig(k_bars=3))
    assert sweeps.height == 1
    assert sweeps.row(0, named=True)["bars_to_reclaim"] == 2


def test_no_reclaim_within_k_bars_means_no_sweep() -> None:
    bars = _bars(
        [
            (100, 101, 98, 98.5),
            (98.5, 99, 97, 97.5),
            (97.5, 98, 96, 96.5),  # never reclaims above 99 within k_bars=3
        ]
    )
    levels = _level("lvl1", "prior_session_low", 99.0, bars["bar_open_ts"][0])
    sweeps = detect_sweeps(bars, levels, config=SweepConfig(k_bars=3))
    assert sweeps.height == 0


def test_bearish_sweep_of_high() -> None:
    bars = _bars([(100, 102, 99.5, 99.8)])  # high=102 sweeps above level=101, close=99.8 reclaims below
    levels = _level("lvl1", "prior_session_high", 101.0, bars["bar_open_ts"][0])
    sweeps = detect_sweeps(bars, levels, config=SweepConfig(k_bars=3))
    assert sweeps.height == 1
    assert sweeps.row(0, named=True)["direction"] == "bearish"


def test_level_not_available_yet_is_not_swept() -> None:
    bars = _bars([(100, 101, 98, 100.5)])
    future_avail = bars["bar_open_ts"][0] + timedelta(minutes=5)
    levels = _level("lvl1", "prior_session_low", 99.0, future_avail)
    sweeps = detect_sweeps(bars, levels, config=SweepConfig(k_bars=3))
    assert sweeps.height == 0


def test_min_penetration_filter() -> None:
    bars = _bars([(100, 101, 98.9, 100.5)])  # penetration = 0.1
    levels = _level("lvl1", "prior_session_low", 99.0, bars["bar_open_ts"][0])
    sweeps = detect_sweeps(bars, levels, config=SweepConfig(k_bars=3, min_penetration_points=0.5))
    assert sweeps.height == 0


def test_repeated_sweeps_disallowed_by_default() -> None:
    bars = _bars(
        [
            (100, 101, 98, 100.5),  # sweep 1
            (100.5, 101, 98, 100.5),  # would be sweep 2 of same level
        ]
    )
    levels = _level("lvl1", "prior_session_low", 99.0, bars["bar_open_ts"][0])
    sweeps = detect_sweeps(bars, levels, config=SweepConfig(k_bars=1, allow_repeated_sweeps=False))
    assert sweeps.height == 1


def test_level_goes_stale_after_max_level_age_bars() -> None:
    # penetration happens at bar index 3, but max_level_age_bars=2 means the
    # level is no longer eligible by then (available at bar 0, stale after bar 2).
    bars = _bars(
        [
            (100, 100.5, 99.5, 100.2),
            (100.2, 100.5, 99.8, 100.1),
            (100.1, 100.5, 99.9, 100.0),
            (100, 101, 98, 100.5),  # would sweep low=99 here, but level is stale
        ]
    )
    levels = _level("lvl1", "prior_session_low", 99.0, bars["bar_open_ts"][0])
    sweeps = detect_sweeps(bars, levels, config=SweepConfig(k_bars=3, max_level_age_bars=2))
    assert sweeps.height == 0


def test_max_level_age_bars_none_means_unbounded() -> None:
    bars = _bars(
        [
            (100, 100.5, 99.5, 100.2),
            (100.2, 100.5, 99.8, 100.1),
            (100.1, 100.5, 99.9, 100.0),
            (100, 101, 98, 100.5),  # sweep still eligible with no age limit
        ]
    )
    levels = _level("lvl1", "prior_session_low", 99.0, bars["bar_open_ts"][0])
    sweeps = detect_sweeps(bars, levels, config=SweepConfig(k_bars=3, max_level_age_bars=None))
    assert sweeps.height == 1


def test_default_config_has_bounded_age() -> None:
    assert SweepConfig().max_level_age_bars == 500


def test_repeated_sweeps_allowed_when_configured() -> None:
    bars = _bars(
        [
            (100, 101, 98, 100.5),
            (100.5, 101, 98, 100.5),
        ]
    )
    levels = _level("lvl1", "prior_session_low", 99.0, bars["bar_open_ts"][0])
    sweeps = detect_sweeps(bars, levels, config=SweepConfig(k_bars=1, allow_repeated_sweeps=True))
    assert sweeps.height == 2
