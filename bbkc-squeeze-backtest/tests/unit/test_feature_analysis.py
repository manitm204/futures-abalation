import polars as pl
import pytest

from src.analysis.feature_analysis import compare_winners_vs_losers, window_performance_breakdown


def test_compare_winners_vs_losers_basic() -> None:
    trades = pl.DataFrame(
        {
            "realized_pnl": [100.0, 200.0, -50.0, -30.0],
            "fvg_size_atr_multiple": [2.0, 3.0, 0.5, 0.8],
        }
    )
    comp = compare_winners_vs_losers(trades, feature_col="fvg_size_atr_multiple")
    assert comp.n_winners == 2
    assert comp.n_losers == 2
    assert comp.winner_median == pytest.approx(2.5)
    assert comp.loser_median == pytest.approx(0.65)


def test_compare_winners_vs_losers_none_when_no_losers() -> None:
    trades = pl.DataFrame({"realized_pnl": [100.0, 200.0], "atr": [1.0, 2.0]})
    assert compare_winners_vs_losers(trades, feature_col="atr") is None


def test_window_performance_breakdown() -> None:
    trades = pl.DataFrame(
        {
            "window": ["ny_am", "ny_am", "ny_pm"],
            "realized_pnl": [100.0, -50.0, 200.0],
        }
    )
    result = window_performance_breakdown(trades)
    am = result.filter(pl.col("window") == "ny_am")
    assert am["n_trades"][0] == 2
    assert am["net_pnl"][0] == pytest.approx(50.0)
    assert am["win_rate"][0] == pytest.approx(0.5)
