"""Strategy-screening funnel over the 75,000-config mean-reversion grid (SPY; 5min/15min/1h bars).

Same stages and thresholds as the channel-breakout funnel; only the base strategy
(src/strategies/mean_reversion/) and its grid (src/experiments/mr_grid.py) differ.
The YAML's `strategy` picks the parameter space: `mean_reversion` (v1, 75,000
configs) or `mean_reversion_v2` (v2, 240,000 configs; configs/funnel/mr_funnel_v2.yaml).
All thresholds: configs/funnel/mr_funnel.yaml (hashed into every output).

Commands (each is a separate, explicit step):
  develop     stages 1-7 on DEVELOPMENT data only (2018-2022; later bars are never
              loaded), plus stage-9 diagnostics (DSR audit, QQQ transfer on the
              development period). Freezes the representatives to a hashed manifest.
  validate    stage 8: evaluates the frozen manifest on 2023-2024. Refuses to run
              if the config changed since `develop`. Writes the selection manifest.
  final-test  stage 10: evaluates a frozen selection manifest on the holdout.
              Requires --confirm-holdout-access; every access is ledgered.

Usage:
  python scripts/run_mr_funnel.py develop --experiment-id mr_v1 --n-workers 12
  python scripts/run_mr_funnel.py validate --experiment-id mr_v1
  python scripts/run_mr_funnel.py final-test --manifest runs/funnel/mr_v1/selection_manifest.json \
      --confirm-holdout-access
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import time
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import polars as pl
import typer

from src.analysis.neighborhood import LATTICE_V1, LATTICE_V2, LATTICE_V3, LATTICE_V5, LATTICE_V6, LATTICE_V7, LATTICE_V8, LATTICE_V9, LATTICE_V10, LATTICE_V11, LATTICE_V12, LATTICE_V13, LATTICE_V14, LATTICE_V15, LATTICE_V16, LATTICE_V17, LATTICE_V21, NeighborhoodStats, neighborhood_stats
from src.analysis.stability import correlation_eigenvalues, dsr_audit, effective_number_of_trials
from src.data.aggregation import AGG_INTERVAL_MINUTES, aggregate_bars
from src.experiments.data_access import (
    DEFAULT_LEDGER,
    append_ledger,
    authorize_holdout_access,
    load_phase_bars,
    read_ledger,
)
from src.experiments.funnel import (
    DEDUPLICATED,
    DIAGNOSTIC,
    HARD_REJECT,
    INSUFFICIENT,
    NOT_EVALUATED,
    PASS,
    Outcome,
    cluster_by_correlation,
    correlation_matrix,
    monthly_returns,
    representative_key,
    select_representatives,
    stage1_integrity,
    stage2_trade_count,
    stage3_performance,
    stage4_parameter_stability,
    stage5_time_stability,
    survivor_table,
)
from src.experiments.funnel_config import (
    DEFAULT_FUNNEL_CONFIG,
    PROJECT_ROOT,
    FunnelConfig,
    load_execution_config,
    load_funnel_config,
)
from src.experiments.funnel_prep import Job, build_dev_records, run_jobs
from src.experiments.funnel_robustness import (
    breakeven_multiplier,
    interval_overlap,
    local_perturbations,
    perturbations,
    perturbations_v2,
    perturbations_v3,
    quantile,
)
from src.experiments.integrity import CHECKS, truncation_invariance
from src.experiments.mr_grid import mr_grid, mr_grid_v2, mr_grid_v3, mr_grid_v5, mr_grid_v6, mr_grid_v7, mr_grid_v8, mr_grid_v9, mr_grid_v10, mr_grid_v11, mr_grid_v12, mr_grid_v13, mr_grid_v14, mr_grid_v15, mr_grid_v16, mr_grid_v17, mr_grid_v21
from src.strategies.mean_reversion.backtest import MRParams
from src.strategies.mean_reversion.config import MeanReversionConfig, MeanReversionV2Config, MeanReversionV3Config, MeanReversionV5Config, MeanReversionV6Config, MeanReversionV7Config, MeanReversionV8Config, MeanReversionV9Config, MeanReversionV10Config, MeanReversionV11Config, MeanReversionV12Config, MeanReversionV13Config, MeanReversionV14Config, MeanReversionV15Config, MeanReversionV16Config, MeanReversionV17Config, MeanReversionV21Config
from src.utils.hashing import canonical_json
from src.utils.logging import configure_logging, get_logger
from src.utils.seeds import derive_seed
from src.utils.serialization import atomic_write_json

app = typer.Typer(add_completion=False)
logger = get_logger(__name__)
OUT_ROOT = PROJECT_ROOT / "runs" / "funnel"
PREP_SOURCES = ["src/strategies/mean_reversion/backtest.py", "src/analysis/daily_performance.py",
                "src/experiments/funnel_prep.py", "src/experiments/integrity.py"]
SPACES = {
    "mean_reversion": {
        "grid": mr_grid, "cls": MeanReversionConfig, "lattice": LATTICE_V1, "perturb": perturbations,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
                 "max_hold", "trend_filter"),
    },
    "mean_reversion_v2": {
        "grid": mr_grid_v2, "cls": MeanReversionV2Config, "lattice": LATTICE_V2, "perturb": perturbations_v2,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "entry_z", "exit_z", "max_holding_bars",
                 "trend_filter", "entry_confirmation", "cooldown_bars", "stop_atr_multiple"),
    },
    "mean_reversion_v3": {
        "grid": mr_grid_v3, "cls": MeanReversionV3Config, "lattice": LATTICE_V3, "perturb": perturbations_v3,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
                 "max_holding_bars", "entry_confirmation", "stop_atr_multiple"),
    },
    "mean_reversion_v5": {
        "grid": mr_grid_v5, "cls": MeanReversionV5Config, "lattice": LATTICE_V5, "perturb": perturbations_v3,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
                 "max_holding_bars", "entry_confirmation", "stop_atr_multiple"),
    },    "mean_reversion_v6": {
        "grid": mr_grid_v6, "cls": MeanReversionV6Config, "lattice": LATTICE_V6, "perturb": perturbations_v3,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
                 "max_holding_bars", "entry_confirmation", "stop_atr_multiple"),
    },    "mean_reversion_v7": {
        "grid": mr_grid_v7, "cls": MeanReversionV7Config, "lattice": LATTICE_V7, "perturb": perturbations_v3,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
                 "max_holding_bars", "entry_confirmation", "stop_atr_multiple"),
    },
    "mean_reversion_v8": {
        "grid": mr_grid_v8, "cls": MeanReversionV8Config, "lattice": LATTICE_V8, "perturb": perturbations_v3,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
                 "max_holding_bars", "entry_confirmation", "stop_atr_multiple"),
    },
    "mean_reversion_v10": {
        "grid": mr_grid_v10, "cls": MeanReversionV10Config, "lattice": LATTICE_V10, "perturb": perturbations_v3,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
                 "max_holding_bars", "entry_confirmation", "stop_atr_multiple"),
    },
    "mean_reversion_v11": {
        "grid": mr_grid_v11, "cls": MeanReversionV11Config, "lattice": LATTICE_V11, "perturb": perturbations_v3,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
                 "max_holding_bars", "entry_confirmation", "stop_atr_multiple"),
    },
    "mean_reversion_v12": {
        "grid": mr_grid_v12, "cls": MeanReversionV12Config, "lattice": LATTICE_V12, "perturb": perturbations_v3,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
                 "max_holding_bars", "entry_confirmation", "stop_atr_multiple"),
    },
    "mean_reversion_v13": {
        "grid": mr_grid_v13, "cls": MeanReversionV13Config, "lattice": LATTICE_V13, "perturb": perturbations_v3,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
                 "max_holding_bars", "entry_confirmation", "stop_atr_multiple"),
    },
    "mean_reversion_v14": {
        "grid": mr_grid_v14, "cls": MeanReversionV14Config, "lattice": LATTICE_V14, "perturb": perturbations_v3,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
                 "max_holding_bars", "entry_confirmation", "stop_atr_multiple"),
    },
    "mean_reversion_v15": {
        "grid": mr_grid_v15, "cls": MeanReversionV15Config, "lattice": LATTICE_V15, "perturb": perturbations_v3,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
                 "max_holding_bars", "entry_confirmation", "stop_atr_multiple"),
    },
    "mean_reversion_v16": {
        "grid": mr_grid_v16, "cls": MeanReversionV16Config, "lattice": LATTICE_V16, "perturb": perturbations_v3,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
                 "max_holding_bars", "entry_confirmation", "stop_atr_multiple"),
    },
    "mean_reversion_v17": {
        "grid": mr_grid_v17, "cls": MeanReversionV17Config, "lattice": LATTICE_V17, "perturb": perturbations_v3,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
                 "max_holding_bars", "entry_confirmation", "stop_atr_multiple"),
    },
    "mean_reversion_v21": {
        "grid": mr_grid_v21, "cls": MeanReversionV21Config, "lattice": LATTICE_V21, "perturb": perturbations_v3,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
                 "max_holding_bars", "entry_confirmation", "stop_atr_multiple"),
    },
    "mean_reversion_v9": {
        "grid": mr_grid_v9, "cls": MeanReversionV9Config, "lattice": LATTICE_V9, "perturb": perturbations_v3,
        "keys": ("symbol", "timeframe", "mean_type", "mean_lookback", "std_lookback", "entry_z", "exit_z",
                 "max_holding_bars", "entry_confirmation", "stop_atr_multiple"),
    },
}
SPACE = SPACES["mean_reversion"]
GRID_KEYS = SPACE["keys"]


def _select_space(fcfg: FunnelConfig) -> None:
    """Point the module at the YAML's parameter space (v1 or v2)."""
    global SPACE, GRID_KEYS
    if fcfg.strategy not in SPACES:
        raise typer.BadParameter(f"Unknown strategy {fcfg.strategy!r}; expected one of {sorted(SPACES)}")
    SPACE = SPACES[fcfg.strategy]
    GRID_KEYS = SPACE["keys"]
BREAKEVEN_GRID = [0.0, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 11.0, 15.0, 20.0, 25.0]


# --- helpers ---------------------------------------------------------------------------------

def _sha(obj) -> str:
    return hashlib.sha256(canonical_json(obj).encode()).hexdigest()


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=PROJECT_ROOT, capture_output=True, text=True).stdout


def _provenance(fcfg: FunnelConfig, config_path: Path) -> dict:
    manifests = {}
    for sym in {fcfg.symbol, fcfg.confidence.transfer_symbol} - {None}:
        p = PROJECT_ROOT / "data" / "metadata" / f"manifest_{sym}_1min.json"
        if p.exists():
            m = json.loads(p.read_text())
            manifests[sym] = {k: m.get(k) for k in ("provider", "cleaning_version", "schema_version",
                              "download_timestamp", "actual_coverage_start", "actual_coverage_end",
                              "row_count", "adjustment_status")}
    return {
        "git_commit": _git("rev-parse", "HEAD").strip(),
        "git_dirty": bool(_git("status", "--porcelain", "--untracked-files=no").strip()),
        "git_diff_sha256": hashlib.sha256(_git("diff", "HEAD").encode()).hexdigest(),
        "config_path": str(config_path), "config_sha256": fcfg.config_sha256(), "seed": fcfg.seed,
        "data_manifests": manifests,
        "available_data_endpoint_per_manifest": {s: m["actual_coverage_end"] for s, m in manifests.items()},
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def _frames(fcfg, symbol, phase, *, command, experiment_id, authorization=None):
    bars, info = load_phase_bars(fcfg, symbol, phase, command=command, experiment_id=experiment_id,
                                 authorization=authorization)
    return {f"{symbol}|{tf}": aggregate_bars(bars, timeframe=tf) for tf in fcfg.data.timeframes}, info


def _params(rec: dict, symbol: str | None = None) -> MRParams:
    p = MRParams.from_config(SPACE["cls"](**{k: rec[k] for k in GRID_KEYS if k in rec}))
    return p if symbol is None else MRParams(**{**p.__dict__, "symbol": symbol})


def _set(rec: dict, stage: int, out: Outcome) -> None:
    rec[f"s{stage}_status"] = out.status
    rec[f"s{stage}_reasons"] = "; ".join(out.reasons)
    rec[f"s{stage}_warnings"] = "; ".join(out.warnings)


def _fmt(x, nd=3, pct=False):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "n/a"
    return f"{100 * x:.1f}%" if pct else f"{x:.{nd}f}"


def _prep_fingerprint(fcfg, ec, data_info) -> str:
    src = {p: hashlib.sha256((PROJECT_ROOT / p).read_bytes()).hexdigest() for p in PREP_SOURCES}
    return _sha({"src": src, "exec": ec.model_dump(mode="json"), "data": data_info["partition_fingerprint"],
                 "end": data_info["phase_end"], "metrics": fcfg.metrics.model_dump(mode="json"),
                 "ts": fcfg.time_stability.model_dump(mode="json"),
                 "dev": fcfg.data.development.model_dump(mode="json"), "tfs": fcfg.data.timeframes})


# --- develop ---------------------------------------------------------------------------------

@app.command()
def develop(
    experiment_id: str = typer.Option(...),
    n_workers: int = typer.Option(12),
    config: Path = typer.Option(DEFAULT_FUNNEL_CONFIG),
    out_dir: Path = typer.Option(OUT_ROOT),
    reuse_prep: bool = typer.Option(True, help="Reuse records if the prep fingerprint matches"),
) -> None:
    """Stages 1-7 (+ stage-9 diagnostics) on development data only."""
    configure_logging()
    t0 = time.time()
    fcfg = load_funnel_config(config)
    _select_space(fcfg)
    ec = load_execution_config(fcfg)
    exp = out_dir / experiment_id
    exp.mkdir(parents=True, exist_ok=True)
    prov = _provenance(fcfg, config)
    dev = fcfg.data.development
    sym = fcfg.symbol
    ppy = fcfg.metrics.periods_per_year

    frames, data_info = _frames(fcfg, sym, "development", command="develop", experiment_id=experiment_id)
    grid = SPACE["grid"]((sym,))
    universe = len(grid)

    # ---- Stage 1 (run level): empirical look-ahead test on a seeded sample ----
    rng = np.random.default_rng(derive_seed(fcfg.seed, "integrity_sample"))
    sample = [grid[i] for i in rng.choice(universe, size=min(fcfg.integrity.truncation_check_sample, universe),
                                          replace=False)]
    fracs = tuple(float(x) for x in np.linspace(0.3, 0.9, fcfg.integrity.truncation_points))
    trunc = {ce.config_id: truncation_invariance(frames[f"{sym}|{ce.config.timeframe}"], ce.config,
                                                 exec_config=ec, cut_fracs=fracs)
             for ce in sample}
    trunc_fail = {k: v for k, v in trunc.items() if v}
    integrity_run = {"truncation_sample": len(sample), "cut_fractions": fracs, "failures": trunc_fail,
                     "checks_per_config": CHECKS,
                     "audit_notes": AUDIT_NOTES}
    atomic_write_json(exp / "integrity.json", integrity_run)
    if trunc_fail:
        typer.echo(f"STAGE 1 FAILED: look-ahead detected in {len(trunc_fail)} sampled configs; see {exp/'integrity.json'}")
        raise typer.Exit(2)
    logger.info("stage1_lookahead_ok", sample=len(sample))

    # ---- Prep: one development-only backtest per config ----
    fp = _prep_fingerprint(fcfg, ec, data_info)
    rec_path, ret_path, meta_path = exp / "records.parquet", exp / "dev_daily_returns.npy", exp / "prep_meta.json"
    if reuse_prep and rec_path.exists() and ret_path.exists() and meta_path.exists() \
            and json.loads(meta_path.read_text()).get("fingerprint") == fp:
        records = pl.read_parquet(rec_path).to_dicts()
        R = np.load(ret_path)
        logger.info("prep_reused", n=len(records))
    else:
        records, R = build_dev_records(grid, frames, fcfg=fcfg, exec_config=ec, n_workers=n_workers)
        pl.DataFrame(records, infer_schema_length=None).write_parquet(rec_path)
        np.save(ret_path, R)
        atomic_write_json(meta_path, {"fingerprint": fp, "n": len(records), "built_s": round(time.time() - t0, 1)})
        logger.info("prep_built", n=len(records), elapsed_s=round(time.time() - t0, 1))
    days = np.unique(frames[f"{sym}|{fcfg.data.timeframes[0]}"]["session_date_ny"].to_numpy()
                     .astype("datetime64[D]"))
    days = days[(days >= np.datetime64(dev.start)) & (days <= np.datetime64(dev.end))]
    assert R.shape == (len(records), len(days)), (R.shape, len(days))
    row = {r["config_id"]: i for i, r in enumerate(records)}
    by_id = {r["config_id"]: r for r in records}
    for r in records:
        for s in range(1, 8):
            r[f"s{s}_status"], r[f"s{s}_reasons"], r[f"s{s}_warnings"] = NOT_EVALUATED, "", ""
    table: list[dict] = [{"stage": "0 universe", "kind": "universe", "evaluated": universe, "passed": universe}]

    def gate(stage: int, name: str, pool: list[dict], fn) -> list[dict]:
        keep = []
        for r in pool:
            out = fn(r)
            _set(r, stage, out)
            if out.status == PASS:
                keep.append(r)
        c = Counter(r[f"s{stage}_status"] for r in pool)
        table.append({"stage": name, "kind": "hard_gate", "evaluated": len(pool), "passed": len(keep),
                      "hard_reject": c[HARD_REJECT], "insufficient_evidence": c[INSUFFICIENT],
                      "with_warnings": sum(1 for r in pool if r[f"s{stage}_warnings"])})
        logger.info("stage_done", stage=name, evaluated=len(pool), passed=len(keep))
        return keep

    s1 = gate(1, "1 backtest integrity", records, stage1_integrity)
    s2 = gate(2, "2 trade count & coverage", s1, lambda r: stage2_trade_count(r, fcfg))
    s3 = gate(3, "3 performance & risk", s2, lambda r: stage3_performance(r, fcfg))

    # ---- Stage 4: immediate neighbors from the FULL universe ----
    ps = fcfg.parameter_stability
    nstats = neighborhood_stats(records, net_return_key="dev_net_return", sharpe_key="dev_sharpe",
                                lattice=SPACE["lattice"],
                                include_joint=ps.neighbor_mode == "single_and_joint",
                                only_ids={r["config_id"] for r in s3})

    # Grid-neighbor stats are always recorded; they gate only in grid_neighbors mode.
    for r in s3:
        ns = nstats[r["config_id"]]
        r.update({"neighbor_n_neighbors": ns.n_neighbors, "neighbor_n_possible_neighbors": ns.n_possible,
                  "neighbor_frac_profitable": ns.frac_profitable, "neighbor_median_sharpe": ns.median_sharpe,
                  "neighbor_center_minus_median_sharpe": (r["dev_sharpe"] - ns.median_sharpe
                                                          if ns.median_sharpe is not None else None),
                  "neighbor_n_sharpe_undefined": ns.n_sharpe_undefined,
                  "neighbor_boundary_axes": ",".join(ns.boundary_axes)})
    if ps.mode == "local_perturbation":
        lmoves = {r["config_id"]: local_perturbations(_params(r), ps.local) for r in s3}
        lres = run_jobs([Job(f"{c}|loc|{lab}", p, dev.start, dev.end) for c, mv in lmoves.items() for lab, p in mv],
                        frames, fcfg=fcfg, exec_config=ec, n_workers=n_workers)
        stab = {}
        for c, mv in lmoves.items():
            ms = [(lab, lres[f"{c}|loc|{lab}"]["metrics"]) for lab, _ in mv]
            sh = [m["sharpe"] for _, m in ms if m["sharpe"] is not None]
            stab[c] = NeighborhoodStats(
                n_neighbors=len(ms), n_possible=len(ms),
                frac_profitable=float(np.mean([(m["net_return"] or 0) > 0 for _, m in ms])) if ms else None,
                median_sharpe=float(np.median(sh)) if sh else None, n_sharpe_undefined=len(ms) - len(sh))
            by_id[c]["local_detail"] = json.dumps([{"move": lab, "sharpe": m["sharpe"], "net_return": m["net_return"],
                                                    "trades": m["n_completed_trades"]} for lab, m in ms])
        prefix = "local"
    else:
        stab, prefix = nstats, "neighbor"

    def _s4(r):
        out = stage4_parameter_stability(stab[r["config_id"]], r.get("dev_sharpe"), fcfg)
        for k, v in out.diagnostics.items():
            r[f"{prefix}_{k}"] = v
        r["stability_median_sharpe"] = out.diagnostics["median_sharpe"]
        if prefix == "local":  # reasons name the local test, not grid neighbors
            out.reasons = [x.replace("neighbor_", "local_") for x in out.reasons]
        return out
    s4 = gate(4, "4 parameter stability", s3, _s4)

    # Perturbation diagnostics (never a gate) for stage-4 survivors.
    pjobs = []
    for r in s4:
        for k, p in enumerate(SPACE["perturb"](_params(r), config_id=r["config_id"], base_seed=fcfg.seed,
                                            pcfg=ps.perturbation)):
            pjobs.append(Job(f"{r['config_id']}|p{k}", p, dev.start, dev.end))
    pres = run_jobs(pjobs, frames, fcfg=fcfg, exec_config=ec, n_workers=n_workers)
    for r in s4:
        ms = [pres[f"{r['config_id']}|p{k}"]["metrics"] for k in range(ps.perturbation.n_per_config)]
        sh = [m["sharpe"] for m in ms]
        med = quantile(sh, 0.5)
        r["perturb_n"] = len(ms)
        r["perturb_frac_profitable"] = float(np.mean([m["net_return"] > 0 for m in ms])) if ms else None
        r["perturb_median_sharpe"] = med
        r["perturb_p10_sharpe"] = quantile(sh, 0.1)
        r["perturb_center_minus_median_sharpe"] = (r["dev_sharpe"] - med) if med is not None else None

    s5 = gate(5, "5 time stability", s4, lambda r: stage5_time_stability(r, fcfg))
    for r in s5:
        r["n_profitable_years"] = r.get("dev_n_profitable_years")  # representative ordering key

    # ---- Stage 6: complete-linkage dedup on development monthly returns ----
    dd = fcfg.dedup
    ids5 = [r["config_id"] for r in s5]
    rows5 = [row[c] for c in ids5]
    M5 = monthly_returns(R[rows5], days) if ids5 else np.zeros((0, 0))
    cluster_of = cluster_by_correlation(ids5, M5, threshold=dd.corr_threshold, method=dd.linkage)
    reps = select_representatives(s5, cluster_of, dd.reps_per_cluster)
    rep_ids = {r["config_id"] for r in reps}
    rep_of = {}  # cluster -> its best representative
    for r in reps:
        rep_of.setdefault(cluster_of[r["config_id"]], r["config_id"])
    ijobs = [Job(f"{c}|iv", _params(by_id[c]), dev.start, dev.end, return_series=True) for c in ids5]
    ivs = {k.split("|")[0]: v["intervals"] for k, v in
           run_jobs(ijobs, frames, fcfg=fcfg, exec_config=ec, n_workers=n_workers).items()}
    Cm = correlation_matrix(M5) if ids5 else None
    Cd = correlation_matrix(R[rows5].astype(np.float64)) if ids5 else None
    pos5 = {c: i for i, c in enumerate(ids5)}
    clusters = []
    for k in sorted(set(cluster_of.values())):
        members = sorted([c for c in ids5 if cluster_of[c] == k], key=lambda c: representative_key(by_id[c]))
        rep = rep_of[k]
        idx = [pos5[c] for c in members]
        sub = Cm[np.ix_(idx, idx)]
        others = [c for c in members if c != rep]
        dcorr = [float(Cd[pos5[rep], pos5[c]]) for c in others]
        ovl = [interval_overlap(ivs[rep], ivs[c]) for c in others]
        clusters.append({"cluster": k, "representative": rep, "representatives": [c for c in members if c in rep_ids],
                         "size": len(members), "members": members,
                         "min_pairwise_monthly_corr": float(sub.min()) if len(members) > 1 else None,
                         "rep_daily_corr_min": min(dcorr) if dcorr else None,
                         "rep_daily_corr_median": quantile(dcorr, 0.5),
                         "rep_trade_overlap_median": quantile(ovl, 0.5),
                         "rep_trade_overlap_min": quantile(ovl, 0.0)})
    for r in s5:
        k = cluster_of[r["config_id"]]
        r["dedup_cluster"] = k
        r["dedup_representative"] = rep_of[k]
        if r["config_id"] in rep_ids:
            _set(r, 6, Outcome(PASS))
        else:
            _set(r, 6, Outcome(DEDUPLICATED, [f"represented_by {rep_of[k]} (cluster {k})"]))
    table.append({"stage": "6 deduplication", "kind": "dedup", "evaluated": len(s5), "passed": len(reps),
                  "deduplicated": len(s5) - len(reps), "n_clusters": len(rep_of),
                  "note": f"best {dd.reps_per_cluster} per cluster"})

    # ---- Stage 7: execution stress on representatives (development data) ----
    st = fcfg.execution_stress
    mults = sorted({1.0, st.gate_cost_multiplier, *st.diagnostic_cost_multipliers,
                    *[m for m in BREAKEVEN_GRID if m <= st.breakeven_max_multiplier]})
    sjobs = []
    for r in reps:
        c, p = r["config_id"], _params(r)
        sjobs += [Job(f"{c}|cost|{m}", p, dev.start, dev.end, cost_multiplier=m) for m in mults]
        sjobs.append(Job(f"{c}|delay", p, dev.start, dev.end, entry_delay_bars=st.entry_delay_bars))
        sjobs += [Job(f"{c}|miss|{k}", p, dev.start, dev.end, missed_entry_frac=st.missed_entry_frac,
                      seed=derive_seed(fcfg.seed, "missed", c, str(k))) for k in range(st.missed_entry_sims)]
    sres = run_jobs(sjobs, frames, fcfg=fcfg, exec_config=ec, n_workers=n_workers)

    def _s7(r):
        c = r["config_id"]
        cost = {m: sres[f"{c}|cost|{m}"]["metrics"] for m in mults}
        for m in mults:
            r[f"stress_cost_{m}x_net_return"] = cost[m]["net_return"]
            r[f"stress_cost_{m}x_sharpe"] = cost[m]["sharpe"]
        dl = sres[f"{c}|delay"]["metrics"]
        mins = AGG_INTERVAL_MINUTES[r["timeframe"]]
        r["stress_delay_label"] = f"{st.entry_delay_bars} bar entry delay = {st.entry_delay_bars * mins} min ({r['timeframe']} bars)"
        r["stress_delay_net_return"], r["stress_delay_sharpe"] = dl["net_return"], dl["sharpe"]
        miss = [sres[f"{c}|miss|{k}"]["metrics"] for k in range(st.missed_entry_sims)]
        nr, sh = [m["net_return"] for m in miss], [m["sharpe"] for m in miss]
        r["stress_missed_median_net_return"], r["stress_missed_p10_net_return"] = quantile(nr, 0.5), quantile(nr, 0.1)
        r["stress_missed_median_sharpe"], r["stress_missed_p10_sharpe"] = quantile(sh, 0.5), quantile(sh, 0.1)
        r["stress_missed_frac_positive"] = float(np.mean([x > 0 for x in nr]))
        be, be_status = breakeven_multiplier(mults, [cost[m]["net_return"] for m in mults])
        r["breakeven_cost_multiplier"], r["breakeven_status"] = be, be_status
        r["breakeven_slippage_bps_per_side"] = be * ec.slippage_bps_market if be is not None else None
        g = cost[st.gate_cost_multiplier]["net_return"]
        warn = []
        for m in st.diagnostic_cost_multipliers:
            if not cost[m]["net_return"] > 0:
                warn.append(f"non_positive_at_{m}x_costs")
        if not dl["net_return"] > 0:
            warn.append("non_positive_with_entry_delay")
        if r["stress_missed_p10_net_return"] is not None and r["stress_missed_p10_net_return"] <= 0:
            warn.append("missed_entry_p10_non_positive")
        if g is None:
            return Outcome(INSUFFICIENT, ["stress_net_return_undefined"], warn)
        if not g > 0:
            return Outcome(HARD_REJECT, [f"net_return {g:.4f} <= 0 at {st.gate_cost_multiplier}x costs"], warn)
        return Outcome(PASS, [], warn)
    s7 = gate(7, "7 execution stress", reps, _s7)

    # ---- Freeze representatives BEFORE any validation data is touched ----
    frozen = _manifest(fcfg, ec, prov, experiment_id, s7, by_id, cluster_of)
    frozen_sha = _sha(frozen)
    atomic_write_json(exp / "frozen_representatives.json", frozen)
    (exp / "frozen_representatives.sha256").write_text(frozen_sha + "\n")
    append_ledger({"event": "freeze_representatives", "experiment_id": experiment_id,
                   "manifest_sha256": frozen_sha, "n_candidates": len(s7)})

    # ---- Stage 9 diagnostics: DSR audit + QQQ transfer (development period) ----
    conf = fcfg.confidence
    srs = np.array([r["dev_sharpe_per_period"] for r in records if r.get("dev_sharpe_per_period") is not None])
    var_sr = float(np.var(srs, ddof=1)) if len(srs) > 1 else 0.0
    ev, n_used = correlation_eigenvalues(R)
    neff = effective_number_of_trials(ev, n_used)
    known_prior = sum(t.n_configs or 0 for t in fcfg.research_history)  # the current grid is not listed there
    trial_options = {"li_ji": neff["li_ji"], "participation_ratio": neff["participation_ratio"],
                     "raw": float(universe), "raw_plus_known_prior": float(universe + known_prior)}
    primary = conf.effective_trials_method
    dsr_meta = {"variance_of_trial_sharpes_per_period": var_sr, "n_configs_with_defined_sharpe": int(len(srs)),
                "sharpe_dispersion_source": "every development backtest in the full grid (not survivors)",
                "effective_trials": neff, "trial_count_options": trial_options, "primary_method": primary,
                "serial_dependence": conf.serial_dependence, "calibration_verified": conf.dsr_calibration_verified,
                "research_history": [t.model_dump() for t in fcfg.research_history],
                "unresolved": DSR_UNRESOLVED}
    for r in reps:
        rets = R[row[r["config_id"]]].astype(np.float64)
        audits = {k: dsr_audit(rets, n_trials=v, variance_of_trial_sharpes=var_sr, periods_per_year=ppy,
                               serial_adjust=conf.serial_dependence == "lag1_effective_n")
                  for k, v in trial_options.items()}
        a = audits[primary]
        r["dsr"] = a.get("dsr")
        r["dsr_benchmark_sharpe_annualized"] = a.get("benchmark_sharpe_annualized")
        r["dsr_n_trials"] = a.get("n_trials")
        for k in trial_options:
            r[f"dsr_{k}"] = audits[k].get("dsr")
        r["dsr_label"] = _dsr_label(r["dsr"], conf)
        r["dsr_audit"] = json.dumps(audits, default=float)
    qqq = conf.transfer_symbol
    if qqq and s7:
        qframes, _ = _frames(fcfg, qqq, "development", command="develop:transfer", experiment_id=experiment_id)
        qres = run_jobs([Job(f"{r['config_id']}|qqq", _params(r, qqq), dev.start, dev.end) for r in s7],
                        qframes, fcfg=fcfg, exec_config=ec, n_workers=n_workers)
        for r in s7:
            m = qres[f"{r['config_id']}|qqq"]["metrics"]
            r["qqq_dev_net_return"], r["qqq_dev_sharpe"], r["qqq_dev_max_drawdown"] = (
                m["net_return"], m["sharpe"], m["max_drawdown"])
    labels = Counter(r["dsr_label"] for r in s7)
    table.append({"stage": "8 frozen validation", "kind": "hard_gate", "evaluated": None, "passed": None,
                  "note": "not run in `develop`; run the `validate` command on the frozen manifest"})
    table.append({"stage": "9 DSR / transfer", "kind": DIAGNOSTIC, "evaluated": len(s7), "passed": None,
                  "note": "diagnostic only: " + ", ".join(f"{k}: {v}" for k, v in labels.items())})
    table.append({"stage": "10 final holdout", "kind": "explicit_command", "evaluated": None, "passed": None,
                  "note": "not run; `final-test` command only"})
    stable = survivor_table(table, universe)

    # ---- Persist ----
    for r in records:
        stages = [s for s in range(1, 8) if r[f"s{s}_status"] != NOT_EVALUATED]
        last = stages[-1] if stages else 0
        r["last_stage_evaluated"] = last
        r["final_status"] = r[f"s{last}_status"] if last else NOT_EVALUATED
        r["research_survivor_dev"] = r.get("s7_status") == PASS
    pl.DataFrame(records, infer_schema_length=None).write_parquet(exp / "config_status.parquet")
    np.save(exp / "dev_days.npy", days.astype("datetime64[D]").astype(str))
    atomic_write_json(exp / "survivor_table.json", stable)
    pl.DataFrame(stable, infer_schema_length=None).write_csv(exp / "survivor_table.csv")
    atomic_write_json(exp / "clusters.json", clusters)
    atomic_write_json(exp / "dsr_inputs.json", dsr_meta)
    atomic_write_json(exp / "representatives.json", [_slim(r) for r in reps])
    rej = Counter()
    for r in records:
        for s in range(1, 8):
            if r[f"s{s}_status"] in (HARD_REJECT, INSUFFICIENT):
                for why in r[f"s{s}_reasons"].split("; "):
                    rej[f"s{s}:{r[f's{s}_status']}:{why.split(' ')[0]}"] += 1
    summary = {
        "experiment_id": experiment_id, "mode": "development_only", "symbol": sym, "n_configs": universe,
        "provenance": prov, "data_access": data_info, "data_history": fcfg.data_history.model_dump(),
        "thresholds": fcfg.model_dump(mode="json"), "survivor_table": stable,
        "rejection_reason_counts": dict(sorted(rej.items())),
        "frozen_manifest_sha256": frozen_sha, "n_frozen_candidates": len(s7),
        "dsr": dsr_meta, "integrity": {k: v for k, v in integrity_run.items() if k != "audit_notes"},
        "elapsed_s": round(time.time() - t0, 1),
        "instrument_type": ec.instrument_type, "transfer_symbol": fcfg.confidence.transfer_symbol,
    }
    atomic_write_json(exp / "summary.json", summary)
    (exp / "report.md").write_text(_report(summary, fcfg, reps, clusters, s7, by_id))
    typer.echo(f"develop done: {universe} configs -> {len(reps)} representatives -> {len(s7)} frozen "
               f"research candidates (dev only). See {exp}")


def _dsr_label(dsr, conf) -> str:
    if not conf.dsr_calibration_verified:
        return "unverified"
    if dsr is None:
        return "insufficient search-adjusted evidence"
    return "passes configured DSR criterion" if dsr >= conf.dsr_threshold else "insufficient search-adjusted evidence"


def _manifest(fcfg, ec, prov, experiment_id, cands, by_id, cluster_of) -> dict:
    return {
        "experiment_id": experiment_id, "frozen_at": datetime.now(timezone.utc).isoformat(),
        "config_sha256": fcfg.config_sha256(), "code_version": prov["git_commit"], "git_dirty": prov["git_dirty"],
        "git_diff_sha256": prov["git_diff_sha256"], "seed": fcfg.seed, "symbol": fcfg.symbol,
        "data_windows": fcfg.data.model_dump(mode="json"),
        "selection_rules": {
            "gates": ["1 integrity", "2 trade count", "3 performance & risk", "4 parameter stability",
                      "5 time stability", f"6 dedup (complete linkage, best {fcfg.dedup.reps_per_cluster} per cluster)", "7 execution stress"],
            "ordering": f"median stage-4 Sharpe ({fcfg.parameter_stability.mode}) desc, profitable dev years desc, dev Sharpe desc, config_id asc",
            "validation_is_not_used_for_ranking": True,
        },
        "sizing_and_costs": ec.model_dump(mode="json"),
        "acceptance_validation": fcfg.validation.model_dump(mode="json"),
        "acceptance_holdout": fcfg.holdout.acceptance.model_dump(mode="json"),
        "candidates": [{"dev_order": i + 1, "config_id": r["config_id"],
                        "params": {k: r[k] for k in GRID_KEYS},
                        "cluster": cluster_of[r["config_id"]],
                        "dev_sharpe": r["dev_sharpe"], "dev_net_return": r["dev_net_return"],
                        "neighbor_median_sharpe": r.get("neighbor_median_sharpe"),
                        "stability_median_sharpe": r.get("stability_median_sharpe"),
                        "n_profitable_years": r.get("dev_n_profitable_years")} for i, r in enumerate(cands)],
    }


SLIM_KEYS = ["config_id", "dedup_cluster", "full_n_z_exits", "full_n_time_exits", "full_n_stop_exits", "dev_n_completed_trades", "dev_net_return", "dev_cagr",
             "dev_sharpe", "dev_max_drawdown", "dev_max_dd_duration_days", "dev_profit_factor", "dev_exposure",
             "dev_turnover_annual", "dev_n_profitable_years", "dev_excl_best_year_return", "dev_excl_best_year_sharpe",
             "dev_best_year", "dev_best_year_contribution", "dev_top_k_trades_contribution",
             "dev_top_frac_trades_contribution", "neighbor_n_neighbors", "neighbor_n_possible_neighbors",
             "neighbor_frac_profitable", "neighbor_median_sharpe", "neighbor_center_minus_median_sharpe",
             "neighbor_boundary_axes", "local_n_neighbors", "local_frac_profitable", "local_median_sharpe",
             "local_detail", "stability_median_sharpe", "perturb_median_sharpe", "perturb_p10_sharpe", "perturb_frac_profitable",
             "stress_cost_1.5x_net_return", "stress_cost_2.0x_net_return", "stress_delay_label",
             "stress_delay_net_return", "stress_missed_median_net_return", "stress_missed_p10_net_return",
             "breakeven_cost_multiplier", "breakeven_status", "s7_status", "s7_reasons", "s7_warnings",
             "dsr", "dsr_label", "dsr_n_trials", "dsr_benchmark_sharpe_annualized", "dsr_li_ji",
             "dsr_participation_ratio", "dsr_raw", "dsr_raw_plus_known_prior",
             "qqq_dev_net_return", "qqq_dev_sharpe", "qqq_dev_max_drawdown"]


def _slim(r: dict) -> dict:
    out = {k: r.get(k) for k in (*GRID_KEYS, *SLIM_KEYS)}
    for k, v in r.items():
        if k.startswith(("dev_year_return_", "dev_year_sharpe_", "dev_year_trades_")):
            out[k] = v
    return out


AUDIT_NOTES = [
    "z = (close - mean) / std with mean = SMA/EMA of the last N closes and std = rolling sample std of the last M closes (bars of the config's timeframe), both INCLUDING the signal bar's close; the signal is decided at that close and the entry fills at the NEXT bar's open.",
    "Exits are decided at a close on or after the entry bar (z >= exit_z, or held max_hold bars) and fill at the next bar's open, so a time exit fills exactly max_hold bars after entry.",
    "Trend filter compares the signal bar's close to the SMA(100/150/200 bars) of closes up to that bar; warm-up bars (SMA undefined) never signal.",
    "No profit target exists. v1 has no stop; v2's optional ATR stop is entry fill - k x ATR(14) using the ATR known before the fill, live from the entry bar, filled at the worse of open and stop. Sizing (v1 and v2): as many whole shares as current equity affords (no leverage).",
    "v2 only: the z-score std uses the same window as the mean; positive_bar_return requires the signal bar's close above the previous close; cooldown_bars = N requires the next signal bar to be >= N bars after the previous exit.",
    "After a time exit the setup re-arms only once z closes above entry_z, so the holding cap cannot be undone by an immediate re-entry.",
    "Missed-entry stress skips a whole signal episode (contiguous signal bars), never re-entering one bar later.",
    "Adverse slippage + commission on every fill; a fill at a session's first bar bears the full overnight gap.",
    "Development backtests run on data physically truncated at the development end; open positions are force-closed at the last development bar and flagged (not counted as completed).",
    "Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.",
    "Positions are held overnight (no session-end flattening), as in the channel family; rolling windows run continuously across sessions over RTH bars only.",
]

DSR_UNRESOLVED = [
    "Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.",
    "The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.",
    "Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.",
    "Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).",
]


def _report(summary, fcfg, reps, clusters, s7, by_id) -> str:
    dh = fcfg.data_history
    L = [f"# Screening funnel -- {summary['experiment_id']} (development stages only)", ""]
    pv = summary["provenance"]
    L += [f"- Code: `{pv['git_commit'][:12]}` (dirty working tree: {pv['git_dirty']}, diff sha256 `{pv['git_diff_sha256'][:12]}`)",
          f"- Config: `{pv['config_path']}` sha256 `{pv['config_sha256'][:16]}`; seed {pv['seed']}",
          f"- Data loaded: {summary['data_access']['first_session']} .. {summary['data_access']['actual_last_session']} "
          f"(phase end {summary['data_access']['phase_end']}); available endpoint per manifest: {pv['available_data_endpoint_per_manifest']}",
          f"- Frozen manifest sha256: `{summary['frozen_manifest_sha256'][:16]}` ({summary['n_frozen_candidates']} candidates)",
          "", "## Data history (not untouched)", "",
          f"- Validation 2023-2024 previously used for selection: **{dh.validation_previously_used_for_selection}** -- {dh.validation_note}",
          f"- Holdout 2025+ previously inspected: **{dh.holdout_previously_inspected}** -- {dh.holdout_note}",
          "", "## Survivor counts", "",
          "| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |",
          "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for t in summary["survivor_table"]:
        def g(k):
            v = t.get(k)
            return "" if v is None else (f"{v:.2f}" if isinstance(v, float) else str(v))
        L.append(f"| {t['stage']} | {t['kind']} | {g('evaluated')} | {g('passed')} | {g('hard_reject')} | "
                 f"{g('insufficient_evidence')} | {g('deduplicated')} | {g('with_warnings')} | {g('pct_of_universe')} | "
                 f"{g('pct_of_previous')} | {t.get('note', '')} |")
    L += ["", "## Rejection reasons", "", "| Stage:status:reason | Count |", "|---|---:|"]
    L += [f"| {k} | {v} |" for k, v in summary["rejection_reason_counts"].items()]
    L += ["", "## Representatives (development ordering)", "",
          "Annual figures are **in-sample diagnostics**, not out-of-sample tests.", "",
          "| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | " + f"{summary.get('transfer_symbol') or 'transfer'} dev SR |",
          "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|"]
    for i, r in enumerate(reps, 1):
        L.append(
            f"| {i} | `{r['config_id'][:8]}` | {', '.join(f'{k}={r[k]}' for k in GRID_KEYS if k != 'symbol')} | "
            f"{r.get('full_n_z_exits')}/{r.get('full_n_time_exits')}/{r.get('full_n_stop_exits')} | "
            f"{r['dev_n_completed_trades']} | "
            f"{_fmt(r['dev_net_return'], pct=True)} | {_fmt(r['dev_cagr'], pct=True)} | {_fmt(r['dev_sharpe'], 2)} | "
            f"{_fmt(r['dev_max_drawdown'], pct=True)} | {r['dev_max_dd_duration_days']} | {_fmt(r['dev_profit_factor'], 2)} | "
            f"{_fmt(r['dev_exposure'], pct=True)} | {_fmt(r['dev_turnover_annual'], 1)} | "
            f"{r.get('neighbor_n_neighbors')}/{r.get('neighbor_n_possible_neighbors')} | {_fmt(r.get('neighbor_frac_profitable'), 2)} | "
            f"{_fmt(r.get('neighbor_median_sharpe'), 2)} | {_fmt(r.get('neighbor_center_minus_median_sharpe'), 2)} | "
            f"{r.get('dev_n_profitable_years')} | {_fmt(r.get('dev_excl_best_year_return'), pct=True)} | "
            f"{_fmt(r.get('dev_best_year_contribution'), 2)} | {_fmt(r.get('dev_top_k_trades_contribution'), 2)} | "
            f"{_fmt(r.get('stress_cost_1.5x_net_return'), pct=True)} | {_fmt(r.get('stress_cost_2.0x_net_return'), pct=True)} | "
            f"{_fmt(r.get('stress_delay_net_return'), pct=True)} | {_fmt(r.get('stress_missed_median_net_return'), pct=True)}/"
            f"{_fmt(r.get('stress_missed_p10_net_return'), pct=True)} | {_fmt(r.get('breakeven_cost_multiplier'), 1)} ({r.get('breakeven_status')}) | "
            f"{r['s7_status']} | {_fmt(r.get('dsr'), 3)} ({r.get('dsr_label')}) | {_fmt(r.get('qqq_dev_sharpe'), 2)} |")
    years = fcfg.dev_years
    L += ["", "### Per-year development slices (in-sample diagnostics)", "",
          "| # | " + " | ".join(f"{y} ret / SR / trades" for y in years) + " |", "|---|" + "---|" * len(years)]
    for i, r in enumerate(reps, 1):
        L.append(f"| {i} | " + " | ".join(
            f"{_fmt(r.get(f'dev_year_return_{y}'), pct=True)} / {_fmt(r.get(f'dev_year_sharpe_{y}'), 2)} / {r.get(f'dev_year_trades_{y}')}"
            for y in years) + " |")
    L += ["", "### Clusters", "", "| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |",
          "|---:|---|---:|---:|---|---|"]
    for c in clusters:
        L.append(f"| {c['cluster']} | `{c['representative'][:8]}` | {c['size']} | {_fmt(c['min_pairwise_monthly_corr'], 2)} | "
                 f"{_fmt(c['rep_daily_corr_min'], 2)}/{_fmt(c['rep_daily_corr_median'], 2)} | "
                 f"{_fmt(c['rep_trade_overlap_min'], 2)}/{_fmt(c['rep_trade_overlap_median'], 2)} |")
    L += ["", "Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.",
          "", "## Stage 9 -- DSR audit (diagnostic, not a gate)", ""]
    d = summary["dsr"]
    L += [f"- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)",
          f"- Trial-Sharpe variance (per period): {d['variance_of_trial_sharpes_per_period']:.3e} over {d['n_configs_with_defined_sharpe']} configs ({d['sharpe_dispersion_source']})",
          f"- Effective trials: Li-Ji {d['effective_trials']['li_ji']:.1f}, participation ratio {d['effective_trials']['participation_ratio']:.1f}, "
          f"95%-variance components {d['effective_trials']['n_components_95']} (rank bound T = {d['effective_trials']['rank_bound_T']}); raw grid {d['trial_count_options']['raw']:.0f}; raw + known prior {d['trial_count_options']['raw_plus_known_prior']:.0f}",
          f"- Primary method: {d['primary_method']}; serial dependence: {d['serial_dependence']} (AR(1) effective n); kurtosis passed as excess",
          f"- Calibration verified: **{d['calibration_verified']}** -> labels are `unverified` until reviewed", "",
          "Unresolved:"] + [f"- {x}" for x in d["unresolved"]]
    L += ["", "A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.",
          f"{summary.get('transfer_symbol')} results are unchanged rules on the development period: supporting evidence, not an independent replication.",
          "", "## Integrity audit", ""] + [f"- {x}" for x in AUDIT_NOTES]
    L += [f"- Look-ahead truncation test: {summary['integrity']['truncation_sample']} sampled configs x "
          f"{len(summary['integrity']['cut_fractions'])} cut points, failures: {len(summary['integrity']['failures'])}"]
    if summary.get("instrument_type") == "futures":
        L += ["", "## Futures data and execution", ""] + [f"- {x}" for x in FUTURES_NOTES]
        L += ["", "## Unresolved assumptions", ""] + [f"- {x}" for x in UNRESOLVED_FUTURES]
    else:
        L += ["", "## Unresolved assumptions", ""] + [f"- {x}" for x in UNRESOLVED]
    return "\n".join(L) + "\n"


UNRESOLVED = [
    "Drawdown limit -30% is reused from the channel-breakout funnel (src/experiments/validation.py); that approval was given for 0.25%-risk stop-based sizing, while this strategy invests full equity per trade -- it has not been separately approved for this sizing.",
    "Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.",
    "rf = 0 and idle cash earns 0: Sharpe vs. cash is overstated in high-rate years (2023-2024 ~5%).",
    "Variable cost stress scales per-share commission and slippage bps; the $1 per-order minimum commission is treated as fixed.",
    "Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.",
    "Prices are split-adjusted but NOT dividend-adjusted: SPY's ~1.5%/yr dividend is not credited while long, and each ex-dividend drop slightly lowers z (a small bias toward entries on ex-div dates).",
    "Neighbor lattice: v1 orders timeframe, mean/std lookback, entry/exit z and max hold; v2 orders timeframe, mean lookback, entry/exit z, max holding bars, cooldown and ATR stop (1.0 < 1.5 < 2.0 < 3.0 < none). mean_type, trend_filter (and v2 entry_confirmation) are held fixed (categorical).",
    "All lookbacks, trend SMAs and holding periods are counted in bars of the config's timeframe (e.g. sma200 on 5min bars spans ~2.6 sessions), not in trading days.",
]

FUTURES_NOTES = [
    "Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.",
    "Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC; the 1-minute step there is taken as the roll spread). Point moves are preserved; pre-roll price levels are not real traded prices.",
    "Session: each root's day session only (src/data/futures.py SESSIONS: NYSE 09:30-16:00 NY for equity indexes, 09:00-14:30 NY for crude, 08:20-13:30 NY for gold, 08:20-15:00 NY for FX; sessions under 5% of normal volume are skipped), on NYSE trading days; overnight Globex bars are not traded or used in indicators.",
    "Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.",
    "Costs: slippage in ticks per side (stops too) plus commission per contract per side, from the execution YAML; cost stress scales both.",
    "Positions that straddle a roll are treated as if rolled for free at the adjusted spread (no extra roll commission/slippage).",
]

UNRESOLVED_FUTURES = [
    "Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.",
    "Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.",
    "rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.",
    "Variable cost stress scales per-contract commission and slippage ticks together.",
    "Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.",
    "Whole-contract granularity: at ~$1M equity the position is a handful of ES contracts, so position size steps with price; results are sensitive to starting equity at small sizes.",
    "All lookbacks and holding periods are counted in bars of the config's timeframe (RTH bars only), not in trading days.",
    "entry_confirmation = positive_bar_return means the signal bar closed above the previous bar's close (the 'directional bar' option).",
]


# --- validate --------------------------------------------------------------------------------

@app.command()
def validate(
    experiment_id: str = typer.Option(...),
    n_workers: int = typer.Option(8),
    config: Path = typer.Option(DEFAULT_FUNNEL_CONFIG),
    out_dir: Path = typer.Option(OUT_ROOT),
) -> None:
    """Stage 8: frozen representatives on 2023-2024. No retuning; development ordering preserved."""
    configure_logging()
    exp = out_dir / experiment_id
    fcfg = load_funnel_config(config)
    _select_space(fcfg)
    ec = load_execution_config(fcfg)
    summary = json.loads((exp / "summary.json").read_text())
    manifest = json.loads((exp / "frozen_representatives.json").read_text())
    if _sha(manifest) != summary["frozen_manifest_sha256"]:
        raise typer.BadParameter("Frozen manifest hash mismatch -- manifest was modified after `develop`.")
    if fcfg.config_sha256() != manifest["config_sha256"]:
        raise typer.BadParameter("Config changed since `develop`; thresholds must stay fixed. Re-run develop.")
    v, vc = fcfg.data.validation, fcfg.validation
    frames, info = _frames(fcfg, fcfg.symbol, "validation", command="validate", experiment_id=experiment_id)
    jobs = [Job(c["config_id"], _params(c["params"]), v.start, v.end) for c in manifest["candidates"]]
    res = run_jobs(jobs, frames, fcfg=fcfg, exec_config=ec, n_workers=n_workers)
    results, passed = [], []
    for c in manifest["candidates"]:
        m = res[c["config_id"]]["metrics"]
        hard, insuff = [], []
        if not m["net_return"] > vc.min_net_return:
            hard.append(f"net_return {m['net_return']:.4f} <= {vc.min_net_return}")
        if m["sharpe"] is None:
            insuff.append("sharpe_undefined")
        elif m["sharpe"] < vc.min_sharpe:
            hard.append(f"sharpe {m['sharpe']:.3f} < {vc.min_sharpe}")
        if vc.max_drawdown is not None and m["max_drawdown"] < vc.max_drawdown:
            hard.append(f"max_drawdown {m['max_drawdown']:.3f} < {vc.max_drawdown}")
        if m["n_completed_trades"] < vc.min_completed_trades:
            hard.append(f"completed_trades {m['n_completed_trades']} < {vc.min_completed_trades}")
        status = HARD_REJECT if hard else INSUFFICIENT if insuff else PASS
        results.append({"dev_order": c["dev_order"], "config_id": c["config_id"], "status": status,
                        "reasons": hard + insuff, "metrics": m})
        if status == PASS:
            passed.append(c)
    out = {"experiment_id": experiment_id, "validation_window": [str(v.start), str(v.end)], "data_access": info,
           "validation_previously_used_for_selection": fcfg.data_history.validation_previously_used_for_selection,
           "note": "Ordering is the frozen development ordering; validation results are never used to re-rank.",
           "results": results}
    atomic_write_json(exp / "validation_results.json", out)
    selection = {**manifest, "validated_at": datetime.now(timezone.utc).isoformat(),
                 "frozen_manifest_sha256": summary["frozen_manifest_sha256"],
                 "candidates": passed,
                 "validation_summary": [{k: r[k] for k in ("config_id", "status", "reasons")} for r in results]}
    sel_sha = _sha(selection)
    atomic_write_json(exp / "selection_manifest.json", selection)
    (exp / "selection_manifest.sha256").write_text(sel_sha + "\n")
    append_ledger({"event": "selection_manifest", "experiment_id": experiment_id, "manifest_sha256": sel_sha,
                   "n_candidates": len(passed)})
    typer.echo(f"validate: {len(manifest['candidates'])} frozen -> {len(passed)} pass validation "
               f"(previously-inspected data). Selection manifest sha256 {sel_sha[:16]}")


# --- final-test ------------------------------------------------------------------------------

@app.command("final-test")
def final_test(
    manifest: Path = typer.Option(..., exists=True),
    confirm_holdout_access: bool = typer.Option(False, "--confirm-holdout-access"),
    n_workers: int = typer.Option(4),
    config: Path = typer.Option(DEFAULT_FUNNEL_CONFIG),
) -> None:
    """Stage 10: evaluate a frozen selection manifest on the holdout. Explicit only."""
    configure_logging()
    sel = json.loads(manifest.read_text())
    sel_sha = _sha(sel)
    auth = authorize_holdout_access(manifest_sha256=sel_sha, confirm=confirm_holdout_access, command="final-test")
    fcfg = load_funnel_config(config)
    _select_space(fcfg)
    if fcfg.config_sha256() != sel["config_sha256"]:
        raise typer.BadParameter("Config changed since the manifest was frozen.")
    ec = load_execution_config(fcfg)
    prior = [e for e in read_ledger(DEFAULT_LEDGER) if e.get("phase") == "holdout"]
    frames, info = _frames(fcfg, fcfg.symbol, "holdout", command="final-test",
                           experiment_id=sel["experiment_id"], authorization=auth)
    h, acc = fcfg.data.holdout, fcfg.holdout.acceptance
    end = date.fromisoformat(info["actual_last_session"])
    jobs = [Job(c["config_id"], _params(c["params"]), h.start, end) for c in sel["candidates"]]
    res = run_jobs(jobs, frames, fcfg=fcfg, exec_config=ec, n_workers=n_workers)
    results = []
    for c in sel["candidates"]:  # manifest order; never re-ranked by holdout performance
        m = res[c["config_id"]]["metrics"]
        ok = (m["net_return"] > acc.min_net_return and m["sharpe"] is not None and m["sharpe"] >= acc.min_sharpe
              and (acc.max_drawdown is None or m["max_drawdown"] >= acc.max_drawdown)
              and (acc.min_completed_trades is None or m["n_completed_trades"] >= acc.min_completed_trades))
        results.append({"dev_order": c["dev_order"], "config_id": c["config_id"], "accepted": ok, "metrics": m})
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = {"manifest": str(manifest), "manifest_sha256": sel_sha, "holdout_window": [str(h.start), str(end)],
           "actual_data_endpoint": str(end), "data_access": info, "prior_holdout_accesses": len(prior),
           "holdout_previously_inspected": fcfg.data_history.holdout_previously_inspected,
           "label": ("holdout previously inspected -- NOT an untouched test"
                     if fcfg.data_history.holdout_previously_inspected or prior else "first recorded holdout access"),
           "note": "Results in frozen development order; holdout performance is not used to rank or pick a winner.",
           "results": results}
    atomic_write_json(manifest.parent / f"holdout_results_{stamp}.json", out)
    typer.echo(f"final-test: {sum(r['accepted'] for r in results)}/{len(results)} meet acceptance; {out['label']}")


if __name__ == "__main__":
    app()
