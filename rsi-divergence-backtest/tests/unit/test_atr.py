import polars as pl
import pytest

from src.features.atr import true_range, wilder_atr


def _bars(rows: list[tuple[float, float, float]]) -> pl.DataFrame:
    return pl.DataFrame({"high": [r[0] for r in rows], "low": [r[1] for r in rows], "close": [r[2] for r in rows]})


def test_true_range_first_bar_is_null_no_prior_close() -> None:
    df = _bars([(10, 8, 9), (11, 9, 10)])
    df = true_range(df)
    assert df["true_range"][0] is None
    assert df["true_range"][1] == 2.0


def test_wilder_atr_known_hand_computed_values() -> None:
    # Constant TR=2 for indices 1-4, then TR=8 at index 5. period=3.
    rows = [
        (10, 8, 9),
        (11, 9, 10),
        (12, 10, 11),
        (13, 11, 12),
        (14, 12, 13),
        (20, 12, 16),
    ]
    df = wilder_atr(_bars(rows), period=3)
    atr = df["atr"].to_list()
    assert atr[0] is None and atr[1] is None and atr[2] is None
    assert atr[3] == pytest.approx(2.0)  # seed = avg(TR[1..3]) = avg(2,2,2)
    assert atr[4] == pytest.approx(2.0)  # unchanged, TR still 2
    assert atr[5] == pytest.approx(4.0)  # 2 + (8-2)/3 = 4.0


def test_warmup_flag_matches_atr_availability() -> None:
    rows = [(10, 8, 9)] * 6
    df = wilder_atr(_bars(rows), period=3)
    warmup = df["atr_warmup_complete"].to_list()
    atr = df["atr"].to_list()
    assert warmup == [v is not None for v in atr]
    assert warmup[:3] == [False, False, False]


def test_no_signals_before_warmup_is_caller_responsibility_but_flag_is_correct() -> None:
    rows = [(float(10 + i), float(8 + i), float(9 + i)) for i in range(20)]
    df = wilder_atr(_bars(rows), period=14)
    assert df["atr_warmup_complete"][:14].to_list() == [False] * 14
    assert df["atr_warmup_complete"][14:].to_list() == [True] * (20 - 14)


def test_rejects_invalid_period() -> None:
    with pytest.raises(ValueError):
        wilder_atr(_bars([(10, 8, 9)]), period=0)


def test_short_series_returns_all_null() -> None:
    df = wilder_atr(_bars([(10, 8, 9), (11, 9, 10)]), period=14)
    assert all(v is None for v in df["atr"].to_list())
