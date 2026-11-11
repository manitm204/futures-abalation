from datetime import datetime, timedelta, timezone

import polars as pl

from src.features.bias import resolve_bias


def _daily(rows: list[tuple[str, float, float]]) -> pl.DataFrame:
    # rows: (date_str, open, close); bar_close_ts = end of that date at 21:00 UTC (16:00 EST)
    dates = [datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc) for d, _, _ in rows]
    close_ts = [d + timedelta(hours=21) for d in dates]
    return pl.DataFrame(
        {
            "bar_close_ts": close_ts,
            "open": [o for _, o, _ in rows],
            "close": [c for _, _, c in rows],
        }
    )


def test_none_mode_is_always_neutral() -> None:
    assert resolve_bias("none", as_of_ts=datetime(2024, 1, 5, tzinfo=timezone.utc)) == "neutral"


def test_prior_daily_direction_bullish() -> None:
    daily = _daily([("2024-01-02", 100, 105)])
    as_of = datetime(2024, 1, 3, 14, 0, tzinfo=timezone.utc)  # during Jan 3 session
    bias = resolve_bias("prior_daily_direction", as_of_ts=as_of, daily_df=daily)
    assert bias == "bullish"


def test_prior_daily_direction_excludes_current_unfinished_bar() -> None:
    """The critical anti-look-ahead check: an as_of_ts DURING Jan 3's session, with
    Jan 3's own daily bar not yet closed, must resolve bias from Jan 2 only -- never
    from Jan 3's in-progress (and therefore not-yet-in-daily_df) bar."""
    daily = _daily([("2024-01-02", 100, 95)])  # Jan 2 bearish
    # Jan 3's daily bar doesn't exist in the frame at all yet (still forming) --
    # simulates the live/causal situation where the current day's bar isn't written
    # until it closes.
    as_of = datetime(2024, 1, 3, 15, 0, tzinfo=timezone.utc)
    bias = resolve_bias("prior_daily_direction", as_of_ts=as_of, daily_df=daily)
    assert bias == "bearish"  # from Jan 2, not contaminated by Jan 3's partial action


def test_prior_daily_direction_even_if_current_day_bar_present_but_not_closed() -> None:
    """Defense in depth: even if a caller accidentally includes a same-day row whose
    bar_close_ts is AFTER as_of_ts (i.e. not actually closed yet), it must be filtered out."""
    daily = _daily([("2024-01-02", 100, 95), ("2024-01-03", 95, 200)])  # Jan3 wildly bullish but not closed
    as_of = datetime(2024, 1, 3, 15, 0, tzinfo=timezone.utc)  # before Jan3's 21:00 UTC close
    bias = resolve_bias("prior_daily_direction", as_of_ts=as_of, daily_df=daily)
    assert bias == "bearish"  # must still use Jan 2, ignoring Jan3's not-yet-closed bar


def test_returns_none_when_insufficient_history() -> None:
    daily = _daily([])
    bias = resolve_bias("prior_daily_direction", as_of_ts=datetime(2024, 1, 3, tzinfo=timezone.utc), daily_df=daily)
    assert bias is None


def test_prior_day_close_vs_open() -> None:
    daily = _daily([("2024-01-02", 100, 110), ("2024-01-03", 112, 108)])
    as_of = datetime(2024, 1, 4, 15, 0, tzinfo=timezone.utc)
    bias = resolve_bias("prior_day_close_vs_open", as_of_ts=as_of, daily_df=daily)
    assert bias == "bullish"  # Jan3 open (112) > Jan2 close (110)


def test_daily_ma20_slope_requires_period_plus_one_bars() -> None:
    daily = _daily([(f"2024-01-{i:02d}", 100 + i, 100 + i) for i in range(1, 21)])
    as_of = datetime(2024, 1, 25, tzinfo=timezone.utc)
    bias = resolve_bias("daily_ma20_slope", as_of_ts=as_of, daily_df=daily, ma_period=20)
    assert bias is None  # only 20 bars total, need 21 (period+1)


def test_daily_ma20_slope_upward() -> None:
    daily = _daily([(f"2024-01-{i:02d}", 100 + i, 100 + i) for i in range(1, 22)])
    as_of = datetime(2024, 1, 25, tzinfo=timezone.utc)
    bias = resolve_bias("daily_ma20_slope", as_of_ts=as_of, daily_df=daily, ma_period=20)
    assert bias == "bullish"


def test_hourly_swing_structure_bullish() -> None:
    ts0 = datetime(2024, 1, 2, 15, 0, tzinfo=timezone.utc)
    swings = pl.DataFrame(
        {
            "kind": ["low", "high", "low", "high"],
            "price": [100.0, 105.0, 102.0, 108.0],
            "availability_ts": [ts0 + timedelta(hours=i) for i in range(4)],
        }
    )
    as_of = ts0 + timedelta(hours=5)
    bias = resolve_bias("hourly_swing_structure", as_of_ts=as_of, hourly_swings=swings)
    assert bias == "bullish"  # higher highs (105->108) and higher lows (100->102)


def test_daily_dependent_mode_with_none_daily_df_returns_none_not_crash() -> None:
    """Regression test: daily_df=None must resolve to None (rejected/unresolvable),
    never raise AttributeError. Caught during Phase 7 experiment-runner smoke
    testing, where the strategy layer doesn't yet wire daily bars through, so
    every bias_mode != "none" config was crashing instead of being rejected."""
    as_of = datetime(2024, 1, 3, tzinfo=timezone.utc)
    for mode in ("prior_daily_direction", "prior_day_close_vs_open", "daily_ma20_slope", "price_vs_daily_ma20"):
        assert resolve_bias(mode, as_of_ts=as_of, daily_df=None) is None


def test_unsupported_mode_raises() -> None:
    import pytest

    with pytest.raises(ValueError):
        resolve_bias("bogus_mode", as_of_ts=datetime(2024, 1, 2, tzinfo=timezone.utc))  # type: ignore[arg-type]
