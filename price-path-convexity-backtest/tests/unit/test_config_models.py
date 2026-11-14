from datetime import time
from pathlib import Path

import pytest
import yaml

from src.utils.config_models import (
    DEFAULT_EXECUTION_CONFIG,
    DEFAULT_SILVER_BULLET_WINDOWS,
    ExecutionConfig,
    SilverBulletWindow,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_default_windows_match_spec() -> None:
    by_name = {w.name: w for w in DEFAULT_SILVER_BULLET_WINDOWS}
    assert by_name["london"].start == time(3, 0) and by_name["london"].end == time(4, 0)
    assert by_name["ny_am"].start == time(10, 0) and by_name["ny_am"].end == time(11, 0)
    assert by_name["ny_pm"].start == time(14, 0) and by_name["ny_pm"].end == time(15, 0)


def test_window_rejects_start_after_end() -> None:
    with pytest.raises(ValueError):
        SilverBulletWindow(name="ny_am", start=time(11, 0), end=time(10, 0))


def test_execution_config_is_frozen() -> None:
    cfg = ExecutionConfig()
    with pytest.raises(Exception):
        cfg.starting_equity = 1.0  # type: ignore[misc]


def test_execution_config_rejects_unknown_field() -> None:
    with pytest.raises(Exception):
        ExecutionConfig(bogus_field=1)  # type: ignore[call-arg]


def test_default_execution_yaml_matches_model_defaults() -> None:
    with (PROJECT_ROOT / "configs" / "execution" / "default.yaml").open() as f:
        raw = yaml.safe_load(f)
    loaded = ExecutionConfig(**raw)
    assert loaded == DEFAULT_EXECUTION_CONFIG


def test_execution_config_conservative_defaults() -> None:
    cfg = DEFAULT_EXECUTION_CONFIG
    assert cfg.starting_equity == 100_000.0
    assert cfg.risk_per_trade_pct == 0.0025
    assert cfg.max_open_positions_per_symbol == 1
    assert cfg.allow_pyramiding is False
    assert cfg.allow_overlapping_trades is False
    assert cfg.leverage == 1.0
    assert cfg.intrabar_collision_mode == "stop_first"
