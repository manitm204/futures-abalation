import pytest

from src.data.fmp_client import FmpResponseError, _validate_list_response


def test_validate_list_response_accepts_well_formed_rows() -> None:
    rows = [{"date": "2024-01-02 09:30:00", "open": 1, "high": 2, "low": 0.5, "close": 1.5, "volume": 100}]
    out = _validate_list_response(rows, ("date", "open", "high", "low", "close", "volume"), context="test")
    assert out == rows


def test_validate_list_response_rejects_error_dict() -> None:
    payload = {"Error Message": "Invalid API KEY"}
    with pytest.raises(FmpResponseError, match="error payload"):
        _validate_list_response(payload, ("date",), context="test")


def test_validate_list_response_rejects_missing_field() -> None:
    rows = [{"date": "2024-01-02 09:30:00", "open": 1}]  # missing high/low/close/volume
    with pytest.raises(FmpResponseError, match="missing required fields"):
        _validate_list_response(rows, ("date", "open", "high", "low", "close", "volume"), context="test")


def test_validate_list_response_rejects_non_list_non_dict() -> None:
    with pytest.raises(FmpResponseError, match="expected a JSON list"):
        _validate_list_response("not json", ("date",), context="test")
