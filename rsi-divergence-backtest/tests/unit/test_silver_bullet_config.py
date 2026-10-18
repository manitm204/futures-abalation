import pytest

from src.strategies.ict_silver_bullet.config import SilverBulletConfig


def test_default_config_valid() -> None:
    cfg = SilverBulletConfig(symbol="SPY")
    assert cfg.windows == ("ny_am", "ny_pm")


def test_london_window_rejected() -> None:
    with pytest.raises(ValueError, match="untestable"):
        SilverBulletConfig(symbol="SPY", windows=("london",))


def test_r_multiple_target_requires_r_value() -> None:
    with pytest.raises(ValueError, match="target_r_multiple is required"):
        SilverBulletConfig(symbol="SPY", target_type="r_multiple", target_r_multiple=None)


def test_fixed_points_target_requires_value() -> None:
    with pytest.raises(ValueError, match="target_fixed_points is required"):
        SilverBulletConfig(symbol="SPY", target_type="fixed_points", target_fixed_points=None)


def test_atr_multiple_stop_requires_value() -> None:
    with pytest.raises(ValueError, match="stop_atr_multiple is required"):
        SilverBulletConfig(symbol="SPY", stop_type="atr_multiple", stop_atr_multiple=None)


def test_fixed_points_stop_requires_value() -> None:
    with pytest.raises(ValueError, match="stop_fixed_points is required"):
        SilverBulletConfig(symbol="SPY", stop_type="fixed_points", stop_fixed_points=None)


def test_max_holding_time_target_requires_minutes() -> None:
    with pytest.raises(ValueError, match="max_holding_minutes is required"):
        SilverBulletConfig(symbol="SPY", target_type="max_holding_time", max_holding_minutes=None)


def test_valid_atr_multiple_stop_config() -> None:
    cfg = SilverBulletConfig(symbol="SPY", stop_type="atr_multiple", stop_atr_multiple=1.5)
    assert cfg.stop_atr_multiple == 1.5


def test_config_is_frozen() -> None:
    cfg = SilverBulletConfig(symbol="SPY")
    with pytest.raises(Exception):
        cfg.symbol = "QQQ"  # type: ignore[misc]


def test_config_hash_stable_and_order_independent() -> None:
    from src.utils.hashing import config_id

    cfg1 = SilverBulletConfig(symbol="SPY", target_r_multiple=2.0, stop_type="swing")
    cfg2 = SilverBulletConfig(symbol="SPY", stop_type="swing", target_r_multiple=2.0)
    assert config_id(cfg1.model_dump(mode="json")) == config_id(cfg2.model_dump(mode="json"))
