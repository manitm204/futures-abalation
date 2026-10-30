"""Backtest integrity (stage 1), daily mark-to-market metrics, DSR audit inputs,
and prevention of holdout access."""

from __future__ import annotations

import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import polars as pl
import pytest
from typer.testing import CliRunner

from src.analysis.daily_performance import daily_equity, window_metrics
from src.analysis.stability import (
    correlation_eigenvalues,
    dsr_audit,
    effective_n_observations,
    effective_number_of_trials,
)
from src.experiments import data_access
from src.experiments.data_access import (
    HoldoutAccessError,
    HoldoutAuthorization,
    authorize_holdout_access,
    load_phase_bars,
    read_ledger,
)
from src.experiments.funnel_config import load_funnel_config
from src.experiments.integrity import check_sim_integrity, truncation_invariance
from src.strategies.mean_reversion.backtest import (
    MRData,
    MRParams,
    scale_variable_costs,
    simulate_mean_reversion,
)
from src.utils.config_models import ExecutionConfig

EC = ExecutionConfig()
FCFG = load_funnel_config()


def _bars(closes_by_day: list[list[float]], *, start=date(2020, 1, 6), spread=0.2, opens=None) -> pl.DataFrame:
    """Synthetic 15-min RTH bars; one inner list per session. Open = previous close
    unless `opens` (same shape, None = default) overrides it."""
    rows, d = [], start
    prev = closes_by_day[0][0]
    for k, closes in enumerate(closes_by_day):
        while d.weekday() >= 5:
            d += timedelta(days=1)
        t0 = datetime(d.year, d.month, d.day, 14, 30, tzinfo=timezone.utc)
        for i, c in enumerate(closes):
            o = prev if opens is None or opens[k][i] is None else opens[k][i]
            rows.append({"bar_open_ts": t0 + timedelta(minutes=15 * i), "session_date_ny": d,
                         "open": o, "high": max(o, c) + spread, "low": min(o, c) - spread, "close": c})
            prev = c
        d += timedelta(days=1)
    return pl.DataFrame(rows)


def _random_walk(n_days=40, per_day=26, seed=0):
    rng = np.random.default_rng(seed)
    px = 100 + np.cumsum(rng.normal(0.0, 0.4, n_days * per_day))
    return _bars([list(px[i * per_day:(i + 1) * per_day]) for i in range(n_days)])


P = MRParams("SPY", "15min", "sma", mean_lookback=10, std_lookback=20, entry_z=-1.0, exit_z=0.0,
             max_hold=5, trend_filter="none")


def _sim(bars, p=P, **kw):
    data = MRData(bars)
    return data, simulate_mean_reversion(data, p, exec_config=EC, starting_equity=1e5, **kw)


# --- backtester integrity ---------------------------------------------------------------

def test_no_lookahead_truncation_invariance():
    bars = _random_walk()
    for p in (P, MRParams("SPY", "15min", "ema", 5, 10, -1.5, 0.5, 3, "sma100")):
        assert truncation_invariance(bars, p, exec_config=EC) == []


def test_zscore_matches_definition_and_is_causal():
    bars = _random_walk(seed=7)
    data = MRData(bars)
    z = data.zscore("sma", 10, 20)
    c = bars["close"].to_numpy()
    i = 300
    expect = (c[i] - c[i - 9:i + 1].mean()) / c[i - 19:i + 1].std(ddof=1)
    assert z[i] == pytest.approx(expect)
    assert np.isnan(z[:19]).all()  # std warm-up -> no signal
    # Poisoning future closes cannot change z at or before i.
    poisoned = MRData(bars.with_columns(pl.when(pl.int_range(pl.len()) > i).then(1e6).otherwise(pl.col("close"))
                                        .alias("close")))
    assert np.allclose(poisoned.zscore("sma", 10, 20)[:i + 1], z[:i + 1], equal_nan=True)
    assert np.allclose(poisoned.zscore("ema", 10, 20)[:i + 1], data.zscore("ema", 10, 20)[:i + 1], equal_nan=True)


def test_entry_and_exit_fill_at_next_bar_open():
    data, sim = _sim(_random_walk(seed=3))
    assert len(sim.entry_idx) > 0
    assert np.all(sim.entry_idx == sim.signal_idx + 1)
    done = ~sim.forced_close
    assert np.all(sim.exit_idx[done] == sim.decision_idx[done] + 1)
    assert np.all(sim.decision_idx[done] >= sim.entry_idx[done])
    assert np.all(sim.entry_px >= data.open[sim.entry_idx])
    assert np.all(sim.exit_px[done] <= data.open[sim.exit_idx[done]])
    assert check_sim_integrity(sim, data, EC, P) == []


def test_time_exit_after_exactly_max_hold_bars_and_rearm():
    # Flat, then a sharp drop that keeps grinding lower: z never recovers -> time exits only.
    closes = [100.0 + 0.01 * (k % 2) for k in range(30)] + [99.0 - 0.3 * k for k in range(30)]
    bars = _bars([closes])
    p = MRParams("SPY", "15min", "sma", 5, 10, -1.0, 0.5, 3, "none")
    data, sim = _sim(bars, p)
    z = data.zscore("sma", 5, 10)
    assert len(sim.entry_idx) >= 1 and set(sim.exit_reason[~sim.forced_close]) == {"time_exit"}
    done = ~sim.forced_close
    assert np.all(sim.exit_idx[done] - sim.entry_idx[done] == 3)
    # Re-arm: no re-entry while z stays at/below entry_z after a time exit.
    for k in range(1, len(sim.entry_idx)):
        between = z[sim.exit_idx[k - 1]:sim.signal_idx[k]]
        assert (between > p.entry_z).any()


def test_z_exit_and_trend_filter():
    data, sim = _sim(_random_walk(seed=11))
    z = data.zscore("sma", 10, 20)
    zx = sim.exit_reason == "z_exit"
    assert zx.any() and np.all(z[sim.decision_idx[zx]] >= P.exit_z)
    pf = MRParams(**{**P.__dict__, "trend_filter": "sma100"})
    data2, simf = _sim(_random_walk(seed=11), pf)
    sma = data2.mean("sma", 100)
    assert np.all(data2.close[simf.signal_idx] > sma[simf.signal_idx])
    assert len(simf.entry_idx) <= len(sim.entry_idx) + 5


def test_position_sized_to_equity_without_leverage():
    data, sim = _sim(_random_walk(seed=2))
    eq_before = 1e5 + np.concatenate([[0.0], np.cumsum(sim.realized_pnl)[:-1]])
    assert np.all(sim.quantity * sim.entry_px + sim.entry_commission <= eq_before + 1e-6)
    assert np.all(sim.quantity * sim.entry_px > eq_before - sim.entry_px - 2 * sim.entry_commission)  # ~all of it
    assert all(t.stop_price is None and t.target_price is None for t in sim.trades)


def test_integrity_flags_tampered_results():
    data, sim = _sim(_random_walk(seed=4))
    sim.exit_px = sim.exit_px + 1.0  # better than the open
    sim.signal_idx = sim.signal_idx.copy()
    sim.signal_idx[0] = sim.entry_idx[0]
    issues = check_sim_integrity(sim, data, EC, P)
    assert "exit_fill_better_than_open" in issues and "entry_not_after_signal_bar" in issues


def test_missed_entries_skip_whole_episode_and_are_reproducible():
    bars = _random_walk(seed=1)
    _, base = _sim(bars)
    _, allmiss = _sim(bars, missed_entry_frac=1.0)
    assert len(allmiss.entry_idx) == 0  # every episode missed -> no re-entry one bar later
    _, a = _sim(bars, missed_entry_frac=0.3, stress_seed=9)
    _, b = _sim(bars, missed_entry_frac=0.3, stress_seed=9)
    assert np.array_equal(a.entry_idx, b.entry_idx) and len(a.entry_idx) <= len(base.entry_idx)


def test_cost_scaling_is_from_baseline_and_keeps_fixed_minimum():
    s15 = scale_variable_costs(EC, 1.5)
    assert s15.slippage_bps_market == pytest.approx(1.5 * EC.slippage_bps_market)
    assert s15.commission_per_share == pytest.approx(1.5 * EC.commission_per_share)
    assert s15.commission_minimum == EC.commission_minimum
    assert scale_variable_costs(EC, 2.0).slippage_bps_stop == pytest.approx(2 * EC.slippage_bps_stop)


def test_entry_delay_shifts_fills():
    bars = _random_walk(seed=2)
    _, a = _sim(bars)
    _, d = _sim(bars, entry_delay_bars=1)
    assert np.all(d.entry_idx - d.signal_idx == 2) and np.all(a.entry_idx - a.signal_idx == 1)


# --- daily mark-to-market metrics -------------------------------------------------------

def test_daily_equity_includes_flat_days_and_reconciles():
    data, sim = _sim(_random_walk(seed=4))
    eq = daily_equity(sim, data, 1e5)
    assert len(eq) == len(data.days)
    if not sim.forced_close[-1]:
        assert eq[-1] == pytest.approx(1e5 + sim.realized_pnl.sum())
    first, last = data.days[0].astype(object), data.days[-1].astype(object)
    m, rets = window_metrics(sim, data, eq, start=first, end=last, starting_equity=1e5)
    assert len(rets) == len(data.days)  # one return per trading day, flat days = 0
    assert m["n_completed_trades"] + m["n_forced_close"] == m["n_trades"]
    assert m["concurrent_overlap_trades"] == 0
    assert sum(m["year_trades"].values()) == m["n_completed_trades"]


def test_undefined_metrics_flagged_not_replaced():
    bars = _bars([[100.0] * 26 for _ in range(30)], spread=0.0)  # flat: std 0 -> no signals
    data, sim = _sim(bars)
    eq = daily_equity(sim, data, 1e5)
    m, _ = window_metrics(sim, data, eq, start=data.days[0].astype(object), end=data.days[-1].astype(object),
                          starting_equity=1e5)
    assert m["sharpe"] is None and "sharpe_undefined" in m["flags"]
    assert m["best_year_contribution"] is None
    assert "contribution_ratios_undefined_nonpositive_total" in m["flags"]


# --- DSR audit --------------------------------------------------------------------------

def test_effective_n_and_trials():
    assert effective_n_observations(1000, 0.5) == pytest.approx(1000 / 3)
    assert effective_n_observations(1000, -0.2) == 1000
    rng = np.random.default_rng(0)
    base = rng.normal(size=500)
    ev, n = correlation_eigenvalues(np.vstack([base + 1e-6 * rng.normal(size=500) for _ in range(20)]))
    assert effective_number_of_trials(ev, n)["li_ji"] <= 2.5     # copies of one trial (Li-Ji rounds up)
    assert effective_number_of_trials(ev, n)["participation_ratio"] < 1.1
    ev, n = correlation_eigenvalues(rng.normal(size=(20, 500)))
    assert effective_number_of_trials(ev, n)["li_ji"] > 15      # ~independent trials


def test_dsr_audit_logs_inputs_and_more_trials_lower_dsr():
    rets = np.random.default_rng(1).normal(0.001, 0.01, 1259)
    a = dsr_audit(rets, n_trials=10, variance_of_trial_sharpes=0.002, periods_per_year=252)
    b = dsr_audit(rets, n_trials=10_000, variance_of_trial_sharpes=0.002, periods_per_year=252)
    for k in ("dsr", "benchmark_sharpe_per_period", "n_observations", "n_effective_observations", "skew",
              "excess_kurtosis", "lag1_autocorr", "variance_of_trial_sharpes_per_period", "kurtosis_convention"):
        assert k in a
    assert b["dsr"] < a["dsr"] and b["benchmark_sharpe_per_period"] > a["benchmark_sharpe_per_period"]
    assert a["sharpe_annualized"] == pytest.approx(a["sharpe_per_period"] * np.sqrt(252))


# --- holdout access prevention ------------------------------------------------------------

def _clean_tree(tmp: Path) -> Path:
    """Fake clean store with dev/val partitions and a CORRUPT holdout partition."""
    root = tmp / "clean"
    for y in (2022, 2023, 2025):
        p = root / "symbol=SPY" / "timeframe=1min" / f"year={y}" / "month=01" / "part-0.parquet"
        p.parent.mkdir(parents=True)
        if y == 2025:
            p.write_bytes(b"not a parquet file")  # opening it would raise
        else:
            pl.DataFrame({"bar_open_ts": [datetime(y, 1, 3, 15, tzinfo=timezone.utc)],
                          "session_date_ny": [date(y, 1, 3)], "open": [1.0], "high": [1.0],
                          "low": [1.0], "close": [1.0]}).write_parquet(p)
    return root


def test_development_load_never_reads_later_partitions(tmp_path):
    root, ledger = _clean_tree(tmp_path), tmp_path / "ledger.jsonl"
    df, info = load_phase_bars(FCFG, "SPY", "development", command="t", experiment_id="e",
                               clean_root=root, ledger_path=ledger)
    assert df["session_date_ny"].max() <= FCFG.data.development.end
    df, _ = load_phase_bars(FCFG, "SPY", "validation", command="t", experiment_id="e",
                            clean_root=root, ledger_path=ledger)
    assert df["session_date_ny"].max() == date(2023, 1, 3)
    assert [e["phase"] for e in read_ledger(ledger)] == ["development", "validation"]


def test_holdout_requires_authorization(tmp_path):
    root, ledger = _clean_tree(tmp_path), tmp_path / "ledger.jsonl"
    with pytest.raises(HoldoutAccessError):
        load_phase_bars(FCFG, "SPY", "holdout", command="t", experiment_id="e", clean_root=root, ledger_path=ledger)
    with pytest.raises(HoldoutAccessError):
        authorize_holdout_access(manifest_sha256="abc", confirm=False, command="t")
    with pytest.raises(HoldoutAccessError):
        authorize_holdout_access(manifest_sha256="", confirm=True, command="t")
    with pytest.raises(HoldoutAccessError):
        HoldoutAuthorization("abc", "t", "now", object())  # can't be forged
    assert read_ledger(ledger) == []  # refused attempts load nothing


def test_final_test_command_refuses_without_confirmation(tmp_path, monkeypatch):
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "run_nb_funnel", Path(__file__).resolve().parents[2] / "scripts" / "run_nb_funnel.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    calls = []
    monkeypatch.setattr(mod, "load_phase_bars", lambda *a, **k: calls.append(1))
    manifest = tmp_path / "selection_manifest.json"
    manifest.write_text(json.dumps({"config_sha256": "x", "experiment_id": "e", "candidates": []}))
    res = CliRunner().invoke(mod.app, ["final-test", "--manifest", str(manifest)])
    assert res.exit_code != 0 and isinstance(res.exception, HoldoutAccessError)
    assert calls == []


def test_routine_develop_path_has_no_holdout_reference():
    src = (Path(__file__).resolve().parents[2] / "scripts" / "run_nb_funnel.py").read_text()
    develop_body = src.split("def develop(")[1].split("\n@app.command")[0]
    assert '"holdout"' not in develop_body and "authorize_holdout_access" not in develop_body
    assert data_access.DEFAULT_LEDGER.name == "data_access_ledger.jsonl"
