"""Funnel stage gating, neighborhood stability, and dedup."""

from __future__ import annotations

import numpy as np

from src.analysis.neighborhood import neighborhood_stats
from src.experiments.funnel import FunnelThresholds, deduplicate, final_test, run_funnel


def _rec(cid, **kw):
    base = dict(
        config_id=cid, symbol="SPY", timeframe="15min", entry_lookback=20, exit_ratio=0.5,
        buffer_atr=0.0, init_stop="off", confirm=1, trend_filter="off",
        dev_n_trades=200, dev_trades_by_year={2018: 40, 2019: 40, 2020: 40, 2021: 40, 2022: 40},
        dev_net_return=0.1, dev_profit_factor=1.3, dev_sharpe=0.9,
        val_net_return=0.05, val_sharpe=0.6, holdout_net_return=0.02, holdout_sharpe=0.4,
        monthly_returns=list(np.random.default_rng(hash(cid) % 2**32).normal(0.01, 0.01, 60)),
    )
    base.update(kw)
    return base


def test_stage2_trade_count_and_coverage():
    recs = [
        _rec("ok"),
        _rec("too_few", dev_n_trades=50),  # 10/yr < 30
        _rec("not_spread", dev_n_trades=200, dev_trades_by_year={2018: 200}),  # 1 active year
    ]
    stages, state = run_funnel(recs, thresholds=FunnelThresholds(), n_years_dev=5.0)
    s2 = next(s for s in stages if s.stage == "2_trade_count")
    assert s2.n_before == 3 and s2.n_after == 1
    assert state["reason"]["too_few"] == "trade_count_or_coverage"
    assert state["reason"]["not_spread"] == "trade_count_or_coverage"


def test_profitability_and_risk_gates():
    recs = [
        _rec("good"),
        _rec("unprofitable", dev_net_return=-0.01),
        _rec("low_pf", dev_profit_factor=1.02),
        _rec("low_sharpe", dev_sharpe=0.2),
    ]
    _, state = run_funnel(recs, thresholds=FunnelThresholds(min_frac_profitable_neighbors=0.0,
                          min_median_neighbor_sharpe=-9, fdr_q=1.0), n_years_dev=5.0)
    assert state["reason"]["unprofitable"] == "profitability"
    assert state["reason"]["low_pf"] == "profitability"
    assert state["reason"]["low_sharpe"] == "risk_sharpe"


def test_neighborhood_isolated_vs_supported():
    # A profitable island with losing neighbors fails; a supported one passes.
    recs = []
    for lb in (10, 15, 20):
        for er in (0.25, 0.5, 0.75):
            net = 0.1 if (lb, er) == (15, 0.5) else -0.1  # island at center
            recs.append(_rec(f"{lb}_{er}", entry_lookback=lb, exit_ratio=er,
                             dev_net_return=net, dev_sharpe=0.9 if net > 0 else -0.5))
    ns = neighborhood_stats(recs, net_return_key="dev_net_return", sharpe_key="dev_sharpe")
    assert ns["15_0.5"].frac_profitable < 0.7  # island: neighbors all losing


def test_dedup_collapses_correlated_survivors():
    base = list(np.linspace(0.01, 0.02, 60))
    a = _rec("a", val_sharpe=1.0, monthly_returns=base)
    b = _rec("b", val_sharpe=0.8, monthly_returns=[x + 1e-6 for x in base])  # ~identical
    c = _rec("c", val_sharpe=0.9, monthly_returns=list(np.random.default_rng(5).normal(0, 0.02, 60)))
    reps, cluster = deduplicate([a, b, c], corr_threshold=0.9)
    assert cluster["a"] == cluster["b"]        # correlated pair merged
    assert len(reps) == 2                       # a (rep of a,b) + c
    assert any(r["config_id"] == "a" for r in reps)  # higher val_sharpe kept


def test_final_test_marks_pass_fail():
    out = final_test([_rec("p", holdout_sharpe=0.5), _rec("f", holdout_sharpe=-0.2)],
                     thresholds=FunnelThresholds())
    flags = {r["config_id"]: r["holdout_pass"] for r in out}
    assert flags["p"] is True and flags["f"] is False


def test_zero_survivors_is_allowed():
    recs = [_rec("x", dev_net_return=-1.0)]
    stages, state = run_funnel(recs, thresholds=FunnelThresholds(), n_years_dev=5.0)
    assert len(state["survivors_pre_stress"]) == 0  # nothing forced through
