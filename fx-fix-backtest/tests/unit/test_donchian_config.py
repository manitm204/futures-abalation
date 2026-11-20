"""DonchianBreakoutConfig: derived accessors and model strictness."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.strategies.donchian_breakout.config import DonchianBreakoutConfig


def _cfg(**kw):
    base = dict(symbol="SPY")
    base.update(kw)
    return DonchianBreakoutConfig(**base)


def test_stop_and_target_accessors():
    assert _cfg(stop="atr_1.5").stop_atr_multiple == 1.5
    assert _cfg(stop="atr_2.5").stop_atr_multiple == 2.5
    assert _cfg(stop="channel_mid").stop_atr_multiple is None
    assert _cfg(target="r_1.5").target_r_multiple == 1.5
    assert _cfg(target="r_3.0").target_r_multiple == 3.0
    assert _cfg(target="none").target_r_multiple is None


def test_trend_and_direction_accessors():
    assert _cfg(trend_filter="none").trend_filter_ma_period is None
    assert _cfg(trend_filter="sma50").trend_filter_ma_period == 50
    assert _cfg(trend_filter="sma200").trend_filter_ma_period == 200
    assert _cfg(direction="both").allow_short is True
    assert _cfg(direction="long_only").allow_short is False


def test_max_holding_bars_depends_on_timeframe():
    assert _cfg(timeframe="15min", time_exit="eod").max_holding_bars is None
    assert _cfg(timeframe="15min", time_exit="max_120min").max_holding_bars == 8   # 120/15
    assert _cfg(timeframe="1h", time_exit="max_120min").max_holding_bars == 2      # 120/60


def test_model_is_frozen_and_forbids_extra():
    c = _cfg()
    with pytest.raises(ValidationError):
        DonchianBreakoutConfig(symbol="SPY", bogus_axis=1)
    with pytest.raises((ValidationError, TypeError, AttributeError)):
        c.channel_lookback = 40  # frozen


def test_invalid_axis_value_rejected():
    with pytest.raises(ValidationError):
        DonchianBreakoutConfig(symbol="SPY", channel_lookback=99)
    with pytest.raises(ValidationError):
        DonchianBreakoutConfig(symbol="SPY", breakout_price="midpoint")
