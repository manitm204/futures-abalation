import pytest

from src.analysis.rankings import percentile_rank, rank_correlation, top_n


def _result(cid: str, sharpe: float | None, net_pnl: float | None = None) -> dict:
    return {"config_id": cid, "metrics": {"sharpe_ratio": sharpe, "net_pnl": net_pnl}}


def test_top_n_sorts_descending_by_default() -> None:
    results = [_result("a", 1.0), _result("b", 3.0), _result("c", 2.0)]
    top = top_n(results, metric="sharpe_ratio", n=2)
    assert [r["config_id"] for r in top] == ["b", "c"]


def test_top_n_excludes_none_metric_values() -> None:
    results = [_result("a", 1.0), _result("b", None), _result("c", 2.0)]
    top = top_n(results, metric="sharpe_ratio", n=5)
    assert [r["config_id"] for r in top] == ["c", "a"]


def test_top_n_lower_is_better_mode() -> None:
    results = [_result("a", 1.0), _result("b", 3.0), _result("c", 2.0)]
    top = top_n(results, metric="sharpe_ratio", n=1, higher_is_better=False)
    assert top[0]["config_id"] == "a"


def test_percentile_rank_of_top_value() -> None:
    results = [_result(f"c{i}", float(i)) for i in range(10)]
    p = percentile_rank(results, metric="sharpe_ratio", config_id="c9")
    # kind="mean" averages strict/weak percentile; top-of-10 -> (100+90)/2 = 95
    assert p == pytest.approx(95.0)


def test_percentile_rank_of_bottom_value() -> None:
    results = [_result(f"c{i}", float(i)) for i in range(10)]
    p = percentile_rank(results, metric="sharpe_ratio", config_id="c0")
    assert p is not None and p < 20


def test_percentile_rank_missing_config_returns_none() -> None:
    results = [_result("a", 1.0)]
    assert percentile_rank(results, metric="sharpe_ratio", config_id="nonexistent") is None


def test_rank_correlation_perfect_positive() -> None:
    results = [_result(f"c{i}", float(i), float(i) * 2) for i in range(10)]
    corr = rank_correlation(results, metric_a="sharpe_ratio", metric_b="net_pnl")
    assert corr is not None
    assert corr.spearman_rho == pytest.approx(1.0)


def test_rank_correlation_perfect_negative() -> None:
    results = [_result(f"c{i}", float(i), float(-i)) for i in range(10)]
    corr = rank_correlation(results, metric_a="sharpe_ratio", metric_b="net_pnl")
    assert corr.spearman_rho == pytest.approx(-1.0)


def test_rank_correlation_insufficient_pairs_returns_none() -> None:
    results = [_result("a", 1.0, 2.0), _result("b", None, 3.0)]
    assert rank_correlation(results, metric_a="sharpe_ratio", metric_b="net_pnl") is None
