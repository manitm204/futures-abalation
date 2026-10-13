"""Configurable screening funnel over the ~25k channel-breakout configs (SPY).

Pipeline (thresholds frozen in FunnelThresholds, logged per run):
  prep  re-backtest every config once -> dev/val/holdout metrics + dev monthly
        return series + dev trades-by-year (saved to parquet, reused on re-run)
  2-8   pure stages: trade count+coverage, profitability, risk, neighborhood,
        multiple-testing (BH-FDR over full search; BY reported), validation
  9     execution stress: adverse costs + entry delay + missed entries; break-even cost
  10    market transfer: survivors re-run unchanged on QQQ (soft evidence)
  11    deduplication: cluster by dev monthly-return correlation, keep best rep
  12    final test: untouched holdout (frozen finalists), pass/fail reported

Saves stage counts, rejection reasons, and survivor sets at every stage.
Zero survivors is a valid outcome.

Usage:
  python scripts/run_channel_funnel.py --experiment-id funnel_v1 --n-workers 12
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path

import polars as pl
import typer

from src.data.aggregation import aggregate_bars
from src.engine.metrics import compute_metrics
from src.experiments.ablation_runner import RunMeta, _split_metrics
from src.experiments.channel_grid import channel_grid
from src.experiments.funnel import FunnelThresholds, deduplicate, final_test, run_funnel
from src.experiments.funnel_prep import build_records
from src.experiments.validation import DEFAULT_SPLIT
from src.strategies.channel_breakout.backtest import ChannelData
from src.strategies.channel_breakout.config import ChannelBreakoutConfig
from src.utils.config_models import DEFAULT_EXECUTION_CONFIG
from src.utils.logging import configure_logging, get_logger
from src.utils.serialization import atomic_write_json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
app = typer.Typer()
logger = get_logger(__name__)

N_YEARS_DEV = 5.0  # 2018-2022
TIMEFRAMES = ("5min", "15min", "1h")

# Frozen execution-stress scenario (stage 9).
STRESS = {"slippage_bps": 5.0, "entry_delay_bars": 1, "missed_entry_frac": 0.10, "seed": 7}
BREAKEVEN_BPS = [1.0, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0, 30.0, 50.0]


def _load_1min(clean_root: Path, symbol: str) -> pl.DataFrame:
    base = clean_root / f"symbol={symbol}" / "timeframe=1min"
    files = sorted(base.rglob("*.parquet"))
    return pl.concat([pl.read_parquet(f) for f in files]).sort("bar_open_ts")


def _cfg_from_record(r: dict) -> ChannelBreakoutConfig:
    keys = ("symbol", "timeframe", "entry_lookback", "exit_ratio", "buffer_atr",
            "init_stop", "confirm", "trend_filter", "atr_period")
    return ChannelBreakoutConfig(**{k: r[k] for k in keys if k in r})


def _split_nr_sharpe(data: ChannelData, cfg, meta: RunMeta, **stress) -> dict:
    from src.strategies.channel_breakout.backtest import run_channel_backtest
    eq0 = meta.execution_config.starting_equity
    trades, equity = run_channel_backtest(data, cfg, exec_config=meta.execution_config, starting_equity=eq0, **stress)
    sp = _split_metrics(trades, equity, meta)
    return sp


@app.command()
def main(
    experiment_id: str = typer.Option(...),
    n_workers: int = typer.Option(12),
    fdr_method: str = typer.Option("bh", help="bh (default) or by (dependence-robust)"),
    fdr_family: str = typer.Option("full_search", help="full_search (default) or screened"),
    clean_root: Path = typer.Option(PROJECT_ROOT / "data" / "clean"),
    out_dir: Path = typer.Option(PROJECT_ROOT / "runs" / "funnel"),
    reuse_prep: bool = typer.Option(True, help="Reuse the records parquet if present"),
) -> None:
    configure_logging()
    t0 = time.time()
    exp_dir = out_dir / experiment_id
    exp_dir.mkdir(parents=True, exist_ok=True)
    thresholds = FunnelThresholds(fdr_method=fdr_method, fdr_family=fdr_family)

    # --- SPY frames + grid ---
    spy_1m = _load_1min(clean_root, "SPY")
    spy_frames = {tf: aggregate_bars(spy_1m, timeframe=tf) for tf in TIMEFRAMES}
    grid = channel_grid(("SPY",))
    meta = RunMeta(experiment_id=experiment_id, code_version="funnel", strategy_name="channel_breakout",
                   execution_config=DEFAULT_EXECUTION_CONFIG, split=DEFAULT_SPLIT)

    # --- prep: records (reuse if present) ---
    recs_path = exp_dir / "records.parquet"
    if reuse_prep and recs_path.exists():
        records = pl.read_parquet(recs_path).to_dicts()
        logger.info("records_loaded", n=len(records))
    else:
        logger.info("prep_start", n_configs=len(grid))
        records = build_records(grid, spy_frames, meta=meta, n_workers=n_workers)
        pl.DataFrame(records).write_parquet(recs_path)
        logger.info("prep_done", n=len(records), elapsed_s=round(time.time() - t0, 1))

    # --- pure stages 2-8 ---
    stages, state = run_funnel(records, thresholds=thresholds, n_years_dev=N_YEARS_DEV)
    survivors = state["survivors_pre_stress"]
    logger.info("pure_stages_done", survivors=len(survivors))

    # --- stage 9: execution stress (+ break-even cost) on SPY ---
    spy_data = {tf: ChannelData(df) for tf, df in spy_frames.items()}
    stressed_meta = RunMeta(
        experiment_id=experiment_id, code_version="funnel", strategy_name="channel_breakout",
        execution_config=DEFAULT_EXECUTION_CONFIG.model_copy(update={
            "slippage_bps_market": STRESS["slippage_bps"], "slippage_bps_stop": STRESS["slippage_bps"]}),
        split=DEFAULT_SPLIT,
    )
    stress_survivors = []
    for r in survivors:
        cfg = _cfg_from_record(r)
        data = spy_data[r["timeframe"]]
        sp = _split_nr_sharpe(data, cfg, stressed_meta,
                              entry_delay_bars=STRESS["entry_delay_bars"],
                              missed_entry_frac=STRESS["missed_entry_frac"], stress_seed=STRESS["seed"])
        r["stress_dev_net_return"] = sp["development"]["net_return_pct"]
        r["stress_dev_sharpe"] = sp["development"]["sharpe"]
        # break-even slippage: scan until dev net return crosses 0
        be = None
        prev_bps, prev_nr = None, None
        for bps in BREAKEVEN_BPS:
            m2 = RunMeta(experiment_id=experiment_id, code_version="f", strategy_name="channel_breakout",
                         execution_config=DEFAULT_EXECUTION_CONFIG.model_copy(update={
                             "slippage_bps_market": bps, "slippage_bps_stop": bps}), split=DEFAULT_SPLIT)
            nr = _split_nr_sharpe(data, cfg, m2)["development"]["net_return_pct"] or 0.0
            if nr <= 0:
                be = bps if prev_bps is None else prev_bps + (bps - prev_bps) * (prev_nr / (prev_nr - nr))
                break
            prev_bps, prev_nr = bps, nr
        r["breakeven_slippage_bps"] = be if be is not None else float(BREAKEVEN_BPS[-1])
        if (r["stress_dev_net_return"] or -1) > 0:
            stress_survivors.append(r)
        else:
            state["reason"][r["config_id"]] = "execution_stress"
    stages.append(_mk("9_execution_stress",
        f"net-positive under adverse exec (slippage {STRESS['slippage_bps']}bp, delay {STRESS['entry_delay_bars']} bar, {STRESS['missed_entry_frac']:.0%} missed)",
        len(survivors), len(stress_survivors)))

    # --- stage 10: market transfer to QQQ (soft; not a gate) ---
    qqq_1m = _load_1min(clean_root, "QQQ")
    qqq_data = {tf: ChannelData(aggregate_bars(qqq_1m, timeframe=tf)) for tf in TIMEFRAMES}
    n_transfer_pos = 0
    for r in stress_survivors:
        cfg = _cfg_from_record(r)
        sp = _split_nr_sharpe(qqq_data[r["timeframe"]], cfg, meta)
        r["qqq_val_sharpe"] = sp["validation"]["sharpe"]
        r["qqq_val_net_return"] = sp["validation"]["net_return_pct"]
        if (r["qqq_val_net_return"] or -1) > 0:
            n_transfer_pos += 1
    stages.append(_mk("10_market_transfer",
        "unchanged on QQQ (soft evidence, not a gate)", len(stress_survivors), len(stress_survivors),
        extra={"n_positive_on_qqq": n_transfer_pos}))

    # --- stage 11: dedup ---
    reps, cluster_of = deduplicate(stress_survivors, corr_threshold=thresholds.dedup_corr_threshold)
    stages.append(_mk("11_deduplication",
        f"cluster by dev return corr >= {thresholds.dedup_corr_threshold}; keep best per cluster",
        len(stress_survivors), len(reps), extra={"n_clusters": len(reps)}))

    # --- stage 12: final (untouched) test ---
    finalists = final_test(reps, thresholds=thresholds)
    n_pass = sum(1 for r in finalists if r["holdout_pass"])
    stages.append(_mk("12_final_test",
        f"untouched holdout: net return > 0 & Sharpe >= {thresholds.min_holdout_sharpe}",
        len(reps), n_pass, extra={"n_finalists_evaluated": len(reps)}))

    # --- persist everything ---
    atomic_write_json(exp_dir / "thresholds.json", {**thresholds.frozen_dict(), "stress": STRESS})
    atomic_write_json(exp_dir / "stages.json", [vars(s) for s in stages])
    from collections import Counter
    atomic_write_json(exp_dir / "rejection_counts.json", dict(Counter(state["reason"].values())))
    pl.DataFrame([{"config_id": c, "reason": why} for c, why in state["reason"].items()]).write_parquet(
        exp_dir / "rejections.parquet")

    def _slim(r):
        keys = ["config_id", "symbol", "timeframe", "entry_lookback", "exit_ratio", "buffer_atr",
                "init_stop", "confirm", "trend_filter", "exit_lookback", "dev_n_trades",
                "dev_net_return", "dev_profit_factor", "dev_sharpe", "val_net_return", "val_sharpe",
                "holdout_net_return", "holdout_sharpe", "neighbor_frac_profitable",
                "neighbor_median_sharpe", "pvalue", "stress_dev_net_return", "stress_dev_sharpe",
                "breakeven_slippage_bps", "qqq_val_sharpe", "qqq_val_net_return", "holdout_pass"]
        return {k: r.get(k) for k in keys}

    atomic_write_json(exp_dir / "finalists.json", [_slim({**r, **{"holdout_pass": r.get("holdout_pass")}})
                                                   for r in finalists])
    atomic_write_json(exp_dir / "summary.json", {
        "experiment_id": experiment_id, "symbol": "SPY", "n_configs": len(records),
        "fdr_method": fdr_method, "fdr": state["fdr"], "thresholds": thresholds.frozen_dict(),
        "stages": [vars(s) for s in stages],
        "rejection_counts": dict(Counter(state["reason"].values())),
        "finalists": [_slim(r) for r in finalists],
        "n_finalists": len(finalists), "n_holdout_pass": n_pass,
        "started_at": datetime.now(timezone.utc).isoformat(), "elapsed_s": round(time.time() - t0, 1),
    })
    logger.info("funnel_complete", experiment_id=experiment_id, finalists=len(finalists),
                holdout_pass=n_pass, elapsed_s=round(time.time() - t0, 1))
    typer.echo(f"Funnel done: {len(records)} configs -> {len(reps)} finalists -> {n_pass} pass holdout. See {exp_dir}")


def _mk(stage, desc, nb, na, extra=None):
    from src.experiments.funnel import StageResult
    return StageResult(stage, desc, nb, na, extra or {})


if __name__ == "__main__":
    app()
