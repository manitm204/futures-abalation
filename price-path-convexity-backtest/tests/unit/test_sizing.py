from src.engine.sizing import compute_position_size
from src.utils.config_models import ExecutionConfig

CFG = ExecutionConfig()  # $100k equity, 0.25% risk


def test_basic_sizing() -> None:
    # risk = 100000 * 0.0025 = 250; stop_distance = 1.0 -> 250 shares
    result = compute_position_size(equity=100_000, entry_price=100.0, stop_price=99.0, config=CFG)
    assert result.accepted is True
    assert result.quantity == 250


def test_rejects_zero_stop_distance() -> None:
    result = compute_position_size(equity=100_000, entry_price=100.0, stop_price=100.0, config=CFG)
    assert result.accepted is False
    assert result.rejection_reason == "invalid_stop_distance"


def test_rejects_negative_effective_stop_distance_handled_via_abs() -> None:
    # short trade: stop above entry -- distance should still be positive via abs()
    result = compute_position_size(equity=100_000, entry_price=100.0, stop_price=101.0, config=CFG)
    assert result.accepted is True
    assert result.quantity == 250


def test_quantity_rounds_down_to_whole_shares() -> None:
    # risk=250, stop_distance=3.0 -> 83.33 -> floor to 83
    result = compute_position_size(equity=100_000, entry_price=100.0, stop_price=97.0, config=CFG)
    assert result.quantity == 83


def test_rejects_when_quantity_rounds_to_zero() -> None:
    # tiny equity, huge stop distance
    result = compute_position_size(equity=100.0, entry_price=100.0, stop_price=50.0, config=CFG)
    assert result.accepted is False
    assert result.rejection_reason == "quantity_rounds_to_zero"


def test_rejects_insufficient_buying_power_no_leverage() -> None:
    # extremely tight stop -> huge raw quantity that exceeds equity notional
    result = compute_position_size(equity=1_000, entry_price=100.0, stop_price=99.99, config=CFG)
    assert result.accepted is True
    assert result.quantity * 100.0 <= 1_000  # capped by buying power, no leverage
