"""Portfolio combination, exposure and sleeve-loading tests."""

from __future__ import annotations

import numpy as np
import pytest

from src.experiments.funnel_config import PROJECT_ROOT
from src.portfolio.metrics import (
    combine_sleeves,
    drawdown,
    equity_curve,
    interval_mask,
    monthly_returns,
    relative_to_benchmark,
    series_metrics,
)
from src.portfolio.sleeves import load_portfolio_config, load_sleeve

CONFIG = PROJECT_ROOT / "configs" / "portfolio" / "portfolio_v1.yaml"


def test_combine_is_sum_of_independent_sleeves():
    rng = np.random.default_rng(0)
    R = rng.normal(0, 0.01, size=(3, 50))
    w = np.array([0.5, 0.3, 0.2])
    port, values = combine_sleeves(R, w)
    expected = sum(wi * equity_curve(r) for wi, r in zip(w, R))
    np.testing.assert_allclose(equity_curve(port), expected)
    np.testing.assert_allclose(values[:, 0], w)


def test_combine_rejects_bad_weights():
    with pytest.raises(ValueError):
        combine_sleeves(np.zeros((2, 3)), np.array([0.5, 0.6]))


def test_flat_sleeve_dilutes_return():
    R = np.vstack([np.full(10, 0.01), np.zeros(10)])
    port, _ = combine_sleeves(R, np.array([0.5, 0.5]))
    assert equity_curve(port)[-1] - 1 == pytest.approx(0.5 * (1.01 ** 10 - 1))


def test_series_metrics_basics():
    r = np.array([0.1, -0.5, 0.2])
    m = series_metrics(r, ppy=3)
    assert m["total_return"] == pytest.approx(1.1 * 0.5 * 1.2 - 1)
    assert m["cagr"] == pytest.approx(m["total_return"])  # exactly one year
    assert m["max_drawdown"] == pytest.approx(-0.5)
    assert series_metrics(np.zeros(5))["sharpe"] is None


def test_drawdown_duration():
    dd, days = drawdown(np.array([1.0, 0.9, 0.95, 1.0, 1.1, 1.0]))
    assert dd == pytest.approx(-0.1)
    assert days == 2


def test_interval_mask_half_open():
    t = np.arange(10)
    m = interval_mask(t, np.array([2, 6]), np.array([4, 7]))
    assert m.tolist() == [False, False, True, True, False, False, True, False, False, False]
    assert not interval_mask(t, np.array([], int), np.array([], int)).any()


def test_relative_to_benchmark_scaled_copy():
    b = np.random.default_rng(1).normal(0, 0.01, 200)
    rel = relative_to_benchmark(0.5 * b, b)
    assert rel["beta"] == pytest.approx(0.5)
    assert rel["correlation"] == pytest.approx(1.0)
    assert rel["alpha_annual"] == pytest.approx(0.0, abs=1e-12)


def test_monthly_returns_compound():
    days = np.array(["2025-01-30", "2025-01-31", "2025-02-03"], dtype="datetime64[D]")
    out = monthly_returns(days, np.array([0.1, 0.1, -0.5]))
    assert out == {"2025-01": pytest.approx(0.21), "2025-02": pytest.approx(-0.5)}


def test_sleeves_load_rank_one_candidates():
    pcfg = load_portfolio_config(CONFIG)
    sleeves = [load_sleeve(s) for s in pcfg.sleeves]
    assert [s.manifest["experiment_id"] for s in sleeves] == ["mr_v2", "rsi_v3", "ma_v2"]
    for s in sleeves:
        assert s.candidate is s.manifest["candidates"][0]
        assert s.params.symbol == "SPY"
    assert [s.timeframe for s in sleeves] == ["1h", "5min", "15min"]
