import polars as pl
import pytest

from src.data.schemas import CLEAN_BAR_SCHEMA, assert_clean_schema, empty_clean_frame


def test_empty_clean_frame_matches_schema() -> None:
    df = empty_clean_frame()
    assert_clean_schema(df)  # should not raise


def test_assert_clean_schema_rejects_missing_column() -> None:
    df = empty_clean_frame().drop("bar_open_ts")
    with pytest.raises(ValueError, match="missing required columns"):
        assert_clean_schema(df)


def test_assert_clean_schema_rejects_wrong_dtype() -> None:
    df = empty_clean_frame()
    df = df.with_columns(pl.col("symbol").cast(pl.Int64).alias("symbol"))
    with pytest.raises(ValueError, match="dtype"):
        assert_clean_schema(df)


def test_clean_bar_schema_timezones_are_iana_not_fixed_offset() -> None:
    assert CLEAN_BAR_SCHEMA["bar_open_ts"].time_zone == "UTC"
    assert CLEAN_BAR_SCHEMA["bar_open_ts_ny"].time_zone == "America/New_York"
