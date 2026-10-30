"""Donchian signal semantics on crafted bars: breakout_price (close/wick/typical),
direction gating, stop/target geometry, no look-ahead, last-bar-of-session drop."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import polars as pl

from src.strategies.donchian_breakout.config import DonchianBreakoutConfig
from src.strategies.donchian_breakout.signals import generate_signals

CID = "cfg_test"


def _bars(ohlc: list[tuple[float, float, float, float]], *, session_day: int = 2) -> pl.DataFrame:
    """Build a single-session 15-min frame from (open, high, low, close) tuples."""
    start = datetime(2024, 1, session_day, 14, 30, tzinfo=timezone.utc)  # 09:30 NY
    rows = []
    for i, (o, h, l, c) in enumerate(ohlc):
        bo = start + timedelta(minutes=15 * i)
        rows.append(
            {
                "symbol": "SPY", "timeframe": "15min",
                "bar_open_ts": bo, "bar_close_ts": bo + timedelta(minutes=15),
                "session_date_ny": datetime(2024, 1, session_day).date(),
                "open": o, "high": h, "low": l, "close": c, "volume": 1000.0,
            }
        )
    return pl.DataFrame(rows)


# 20 flat bars establish a channel at high=100 / low=99 (lookback=20), then the
# test bar fires, and trailing bars ensure it is not the last bar of the session.
FLAT = (100.0, 100.0, 99.0, 99.5)
LB = 20
WARMUP = [FLAT] * LB          # indices 0..19
TRAIL = [FLAT, FLAT]
SIG_IDX = LB                  # the signal bar is at index 20


def _cfg(**kw):
    base = dict(symbol="SPY", timeframe="15min", channel_lookback=LB, atr_period=14)
    base.update(kw)
    return DonchianBreakoutConfig(**base)


def test_wick_breakout_fires_but_close_does_not():
    # bar4: high 101 pierces the 100 channel, but close 100 does not exceed it.
    bars = _bars(WARMUP + [(100.0, 101.0, 99.5, 100.0)] + TRAIL)

    close_sig, _ = generate_signals(bars, config=_cfg(breakout_price="close"), config_id=CID)
    assert close_sig.height == 0  # nothing closes beyond the channel

    wick_sig, _ = generate_signals(bars, config=_cfg(breakout_price="wick"), config_id=CID)
    assert wick_sig.height == 1
    assert wick_sig["direction"][0] == "long"


def test_typical_price_breakout():
    # typical = (101 + 99.5 + 100)/3 = 100.17 > 100 -> fires; close alone would not.
    bars = _bars(WARMUP + [(100.0, 101.0, 99.5, 100.0)] + TRAIL)
    sig, _ = generate_signals(bars, config=_cfg(breakout_price="typical"), config_id=CID)
    assert sig.height == 1 and sig["direction"][0] == "long"


def test_short_breakout_and_long_only_suppression():
    # bar4 low 98 pierces the 99 lower channel on the downside.
    bars = _bars(WARMUP + [(99.5, 100.0, 98.0, 99.5)] + TRAIL)

    both, _ = generate_signals(bars, config=_cfg(breakout_price="wick", direction="both"), config_id=CID)
    assert both.height == 1 and both["direction"][0] == "short"

    long_only, _ = generate_signals(bars, config=_cfg(breakout_price="wick", direction="long_only"), config_id=CID)
    assert long_only.height == 0  # shorts suppressed, no long here


def test_no_lookahead_submission_is_signal_bar_close():
    bars = _bars(WARMUP + [(100.0, 101.0, 99.5, 100.0)] + TRAIL)
    sig, _ = generate_signals(bars, config=_cfg(breakout_price="wick"), config_id=CID)
    # submission_ts is the signal bar's CLOSE, i.e. the next bar's open -> next-bar fill.
    assert sig["submission_ts"][0] == bars["bar_close_ts"][SIG_IDX]


def test_stop_and_target_geometry_long():
    bars = _bars(WARMUP + [(100.0, 101.0, 99.5, 100.0)] + TRAIL)
    sig, _ = generate_signals(
        bars, config=_cfg(breakout_price="wick", stop="atr_1.5", target="r_1.5"), config_id=CID
    )
    row = sig.to_dicts()[0]
    entry, stop, target = row["entry_ref_price"], row["stop_price"], row["target_price"]
    assert stop < entry < target  # long: stop below, target above
    # target is 1.5R above entry
    assert abs((target - entry) - 1.5 * (entry - stop)) < 1e-6


def test_channel_mid_stop_and_no_target():
    bars = _bars(WARMUP + [(100.0, 101.0, 99.5, 100.0)] + TRAIL)
    sig, _ = generate_signals(
        bars, config=_cfg(breakout_price="wick", stop="channel_mid", target="none"), config_id=CID
    )
    row = sig.to_dicts()[0]
    assert row["target_price"] is None
    assert abs(row["stop_price"] - 99.5) < 1e-6  # mid of [99,100] channel


def test_last_bar_of_session_signal_is_dropped():
    # Breakout on the final bar of the session cannot be entered intraday -> dropped.
    bars = _bars(WARMUP + [(100.0, 101.0, 99.5, 100.0)])  # no trailing bars
    sig, _ = generate_signals(bars, config=_cfg(breakout_price="wick"), config_id=CID)
    assert sig.height == 0
