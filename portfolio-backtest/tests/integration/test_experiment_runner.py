from pathlib import Path

import polars as pl
import pytest

from src.data.calendars import TradingCalendar
from src.data.normalization import normalize_intraday_rows
from src.experiments.runner import RunMeta, run_experiment, run_one_config
from src.experiments.sampler import sample_configs
from src.experiments.spaces import DEFAULT_SILVER_BULLET_SPACE
from src.utils.config_models import DEFAULT_EXECUTION_CONFIG

CAL = TradingCalendar()


def _multi_day_bars(n_days: int = 5) -> pl.DataFrame:
    import random

    rng = random.Random(42)
    rows = []
    dates = ["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-08"][:n_days]
    price = 100.0
    for date_str in dates:
        for m in range(390):
            hh = 9 + (30 + m) // 60
            mm = (30 + m) % 60
            price += rng.uniform(-0.3, 0.3)
            o = price
            h = o + abs(rng.uniform(0, 0.4))
            l = o - abs(rng.uniform(0, 0.4))
            c = o + rng.uniform(-0.2, 0.2)
            rows.append({"date": f"{date_str} {hh:02d}:{mm:02d}:00", "open": o, "high": h, "low": l, "close": c, "volume": 1000})
    return normalize_intraday_rows(rows, symbol="SPY", timeframe="1min", source="fmp_native", calendar=CAL)


@pytest.fixture
def bars() -> pl.DataFrame:
    return _multi_day_bars()


@pytest.fixture
def meta(tmp_path: Path) -> RunMeta:
    return RunMeta(
        experiment_id="exp_test", code_version="test", data_manifest_hashes={"SPY_1min": "abc123"},
        execution_config=DEFAULT_EXECUTION_CONFIG,
    )


def test_single_config_run_produces_result_file(tmp_path: Path, bars: pl.DataFrame, meta: RunMeta) -> None:
    samples = sample_configs(DEFAULT_SILVER_BULLET_SPACE, n=1, seed=1)
    results_dir, trades_dir, signals_dir = tmp_path / "results", tmp_path / "trades", tmp_path / "signals"
    result = run_one_config(samples[0], bars, meta=meta, results_dir=results_dir, trades_dir=trades_dir, signals_dir=signals_dir)
    assert result["status"] == "ok"
    assert "n_trades" in result
    assert (results_dir / f"experiment_id=exp_test" / f"{samples[0].config_id}.json").exists()


def test_run_experiment_resumes_and_skips_completed(tmp_path: Path, bars: pl.DataFrame, meta: RunMeta) -> None:
    samples = sample_configs(DEFAULT_SILVER_BULLET_SPACE, n=5, seed=2)
    results_dir, trades_dir, signals_dir = tmp_path / "results", tmp_path / "trades", tmp_path / "signals"

    results1 = run_experiment(samples, bars, meta=meta, results_dir=results_dir, trades_dir=trades_dir, signals_dir=signals_dir)
    assert len(results1) == 5
    assert all(r["status"] in ("ok", "failed") for r in results1)

    # simulate a fresh process resuming: same configs, same dirs -- nothing should
    # be recomputed (we can't easily prove "not recomputed" without a side effect,
    # but we CAN prove all 5 are still reported and files weren't wiped).
    results2 = run_experiment(samples, bars, meta=meta, results_dir=results_dir, trades_dir=trades_dir, signals_dir=signals_dir)
    assert len(results2) == 5
    ids1 = sorted(r["config_id"] for r in results1)
    ids2 = sorted(r["config_id"] for r in results2)
    assert ids1 == ids2


def test_run_experiment_force_recomputes(tmp_path: Path, bars: pl.DataFrame, meta: RunMeta) -> None:
    samples = sample_configs(DEFAULT_SILVER_BULLET_SPACE, n=2, seed=3)
    results_dir, trades_dir, signals_dir = tmp_path / "results", tmp_path / "trades", tmp_path / "signals"
    run_experiment(samples, bars, meta=meta, results_dir=results_dir, trades_dir=trades_dir, signals_dir=signals_dir)
    results = run_experiment(samples, bars, meta=meta, results_dir=results_dir, trades_dir=trades_dir, signals_dir=signals_dir, force=True)
    assert len(results) == 2


def test_config_failure_is_isolated_not_fatal(tmp_path: Path, bars: pl.DataFrame, meta: RunMeta, monkeypatch) -> None:
    from src.strategies.ict_silver_bullet import strategy as strategy_module

    samples = sample_configs(DEFAULT_SILVER_BULLET_SPACE, n=3, seed=4)
    results_dir, trades_dir, signals_dir = tmp_path / "results", tmp_path / "trades", tmp_path / "signals"

    original = strategy_module.SilverBulletStrategy.compute_features
    call_count = {"n": 0}

    def _flaky(self, bars_dict):
        call_count["n"] += 1
        if call_count["n"] == 2:
            raise RuntimeError("simulated feature computation failure")
        return original(self, bars_dict)

    monkeypatch.setattr(strategy_module.SilverBulletStrategy, "compute_features", _flaky)

    results = run_experiment(samples, bars, meta=meta, results_dir=results_dir, trades_dir=trades_dir, signals_dir=signals_dir)
    assert len(results) == 3
    statuses = [r["status"] for r in results]
    assert "failed" in statuses
    assert statuses.count("ok") == 2  # the other two configs still completed


def test_parallel_execution_produces_same_results_as_sequential(tmp_path: Path, bars: pl.DataFrame, meta: RunMeta) -> None:
    """Regression test for a real bug: the parallel path used to pass the full
    bars DataFrame as a per-task argument to ProcessPoolExecutor.submit, which
    re-pickles/pipes a full copy for every single config -- fine for a handful
    of tiny test configs, but on the real 400-config/842k-row pilot this
    produced an apparent multi-hour hang. Workers must now load the data once
    via the pool initializer instead. This test just checks correctness
    (same config_ids, same statuses) with a real multi-worker pool; the
    performance regression itself isn't reproducible at unit-test data sizes."""
    samples = sample_configs(DEFAULT_SILVER_BULLET_SPACE, n=6, seed=42)

    seq_dir = tmp_path / "seq"
    par_dir = tmp_path / "par"
    seq_results = run_experiment(
        samples, bars, meta=meta,
        results_dir=seq_dir / "results", trades_dir=seq_dir / "trades", signals_dir=seq_dir / "signals",
        n_workers=1,
    )
    par_results = run_experiment(
        samples, bars, meta=meta,
        results_dir=par_dir / "results", trades_dir=par_dir / "trades", signals_dir=par_dir / "signals",
        n_workers=2,
    )

    seq_by_id = {r["config_id"]: r["status"] for r in seq_results}
    par_by_id = {r["config_id"]: r["status"] for r in par_results}
    assert seq_by_id == par_by_id
    assert len(par_results) == 6


def test_all_sampled_configs_run_without_crashing_batch(tmp_path: Path, bars: pl.DataFrame, meta: RunMeta) -> None:
    """Broader smoke test: a batch of diverse sampled configs against the same
    small dataset should all resolve to either ok or failed, never raise out of
    run_experiment itself."""
    samples = sample_configs(DEFAULT_SILVER_BULLET_SPACE, n=20, seed=99)
    results_dir, trades_dir, signals_dir = tmp_path / "results", tmp_path / "trades", tmp_path / "signals"
    results = run_experiment(samples, bars, meta=meta, results_dir=results_dir, trades_dir=trades_dir, signals_dir=signals_dir)
    assert len(results) == 20
    assert all(r["status"] in ("ok", "failed") for r in results)
