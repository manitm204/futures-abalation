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
from src.strategies.channel_breakout.backtest import (
    ChannelData,
    ChannelParams,
    scale_variable_costs,
    simulate_channel,
)
from src.utils.config_models import ExecutionConfig

EC = ExecutionConfig()
FCFG = load_funnel_config()


def _bars(closes_by_day: list[list[float]], *, start=date(2020, 1, 6), spread=0.2, lows=None) -> pl.DataFrame:
    """Synthetic 15-min RTH bars; one inner list per session."""
    rows, d = [], start
    for k, closes in enumerate(closes_by_day):
        while d.weekday() >= 5:
            d += timedelta(days=1)
        t0 = datetime(d.year, d.month, d.day, 14, 30, tzinfo=timezone.utc)
        prev = closes[0]
        for i, c in enumerate(closes):
            o = prev
            lo = min(o, c) - spread if lows is None or lows[k][i] is None else lows[k][i]
            rows.append({"bar_open_ts": t0 + timedelta(minutes=15 * i), "session_date_ny": d,
                         "open": o, "high": max(o, c) + spread, "low": lo, "close": c})
            prev = c
        d += timedelta(days=1)
    return pl.DataFrame(rows)


def _random_walk(n_days=40, per_day=26, seed=0):
    rng = np.random.default_rng(seed)
    px = 100 + np.cumsum(rng.normal(0.02, 0.4, n_days * per_day))
    return _bars([list(px[i * per_day:(i + 1) * per_day]) for i in range(n_days)])


P = ChannelParams("SPY", "15min", entry_lookback=10, exit_lookback=5, buffer_atr=0.0,
                  init_stop_atr=2.0, confirm=1, trend_filter="off")


# --- backtester integrity ---------------------------------------------------------------

def test_no_lookahead_truncation_invariance():
    bars = _random_walk()
    assert truncation_invariance(bars, P, exec_config=EC, atr_period=14) == []


def test_initial_stop_uses_atr_known_before_entry():
    bars = _random_walk(seed=3)
    data = ChannelData(bars)
    sim = simulate_channel(data, P, exec_config=EC, starting_equity=1e5)
    assert len(sim.entry_idx) > 0
    # Poison the ENTRY bars' ATR: decisions must not change.
    poisoned = ChannelData(bars)
    poisoned.atr = poisoned.atr.copy()
    poisoned.atr[sim.entry_idx] = 1e6
    sim2 = simulate_channel(poisoned, P, exec_config=EC, starting_equity=1e5)
    assert np.array_equal(sim.entry_idx, sim2.entry_idx) and np.allclose(sim.quantity, sim2.quantity)


def test_stop_is_live_on_entry_bar():
    # 20 flat bars (past ATR warm-up), a breakout bar, then an entry bar whose low collapses.
    closes = [100.0] * 20 + [101.5, 101.6, 101.7, 101.8]
    lows = [None] * 21 + [90.0, None, None]
    bars = _bars([closes], lows=[lows])
    p = ChannelParams("SPY", "15min", 10, 5, 0.0, None, 1, "off")
    sim = simulate_channel(ChannelData(bars), p, exec_config=EC, starting_equity=1e5)
    assert len(sim.entry_idx) >= 1
    assert sim.entry_idx[0] == 21 and sim.exit_idx[0] == 21  # stopped out on the entry bar
    assert sim.exit_px[0] < 100.0


def test_gap_through_stop_fills_at_open():
    bars = _random_walk(seed=5)
    data = ChannelData(bars)
    sim = simulate_channel(data, P, exec_config=EC, starting_equity=1e5)
    stop = ~sim.forced_close
    raw = np.minimum(data.open[sim.exit_idx[stop]], sim.stop_level[stop])
    assert np.all(sim.exit_px[stop] <= raw + 1e-9)
    assert check_sim_integrity(sim, data, EC) == []


def test_missed_entries_skip_whole_episode_and_are_reproducible():
    bars = _random_walk(seed=1)
    data = ChannelData(bars)
    base = simulate_channel(data, P, exec_config=EC, starting_equity=1e5)
    allmiss = simulate_channel(data, P, exec_config=EC, starting_equity=1e5, missed_entry_frac=1.0)
    assert len(allmiss.entry_idx) == 0  # every episode missed -> no re-entry one bar later
    a = simulate_channel(data, P, exec_config=EC, starting_equity=1e5, missed_entry_frac=0.3, stress_seed=9)
    b = simulate_channel(data, P, exec_config=EC, starting_equity=1e5, missed_entry_frac=0.3, stress_seed=9)
    assert np.array_equal(a.entry_idx, b.entry_idx) and len(a.entry_idx) <= len(base.entry_idx)


def test_cost_scaling_is_from_baseline_and_keeps_fixed_minimum():
    s15 = scale_variable_costs(EC, 1.5)
    assert s15.slippage_bps_market == pytest.approx(1.5 * EC.slippage_bps_market)
    assert s15.commission_per_share == pytest.approx(1.5 * EC.commission_per_share)
    assert s15.commission_minimum == EC.commission_minimum
    # scaling a stressed config again would compound; callers always start from baseline
    assert scale_variable_costs(EC, 2.0).slippage_bps_stop == pytest.approx(2 * EC.slippage_bps_stop)


def test_entry_delay_shifts_fills():
    data = ChannelData(_random_walk(seed=2))
    a = simulate_channel(data, P, exec_config=EC, starting_equity=1e5)
    d = simulate_channel(data, P, exec_config=EC, starting_equity=1e5, entry_delay_bars=1)
    assert np.all(d.entry_idx - d.signal_idx == 2) and np.all(a.entry_idx - a.signal_idx == 1)


# --- daily mark-to-market metrics -------------------------------------------------------

def test_daily_equity_includes_flat_days_and_reconciles():
    bars = _random_walk(seed=4)
    data = ChannelData(bars)
    sim = simulate_channel(data, P, exec_config=EC, starting_equity=1e5)
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
    bars = _bars([[100.0] * 26 for _ in range(30)], spread=0.0)  # flat: no breakouts
    data = ChannelData(bars)
    sim = simulate_channel(data, P, exec_config=EC, starting_equity=1e5)
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
        "run_channel_funnel", Path(__file__).resolve().parents[2] / "scripts" / "run_channel_funnel.py")
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
    src = (Path(__file__).resolve().parents[2] / "scripts" / "run_channel_funnel.py").read_text()
    develop_body = src.split("def develop(")[1].split("\n@app.command")[0]
    assert '"holdout"' not in develop_body and "authorize_holdout_access" not in develop_body
    assert data_access.DEFAULT_LEDGER.name == "data_access_ledger.jsonl"
