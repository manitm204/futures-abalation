"""Configurable screening funnel for strategy configurations.

Pure stages (operate on stored per-config records; no re-backtest):
  2 trade count + annual coverage, 3 profitability, 4 risk (Sharpe),
  5 neighborhood stability, 7 multiple-testing (BH-FDR, BY alternative),
  8 validation, 11 deduplication, 12 final (untouched) test.
Stages 9 (execution stress) and 10 (market transfer) need re-backtesting and are
driven by the orchestration script, which appends their results here.

Everything is tuned on DEVELOPMENT only; validation is stage 8; the untouched
holdout is touched only at stage 12. Thresholds live in a frozen FunnelThresholds
and are logged per run. Zero survivors is a valid outcome -- nothing is forced.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

import numpy as np

from src.analysis.multiple_testing import benjamini_hochberg, benjamini_yekutieli, block_bootstrap_pvalue
from src.analysis.neighborhood import neighborhood_stats


@dataclass(frozen=True)
class FunnelThresholds:
    # Stage 2 -- trade count + distribution
    min_trades_per_year: float = 30.0
    min_active_years: int = 4           # dev years (of 5) with >= 1 trade
    # Stage 3 -- profitability (after costs)
    min_dev_net_return: float = 0.0     # strictly positive required
    min_profit_factor: float = 1.10
    # Stage 4 -- risk
    min_dev_sharpe: float = 0.5
    # Stage 5 -- neighborhood stability
    min_frac_profitable_neighbors: float = 0.70
    min_median_neighbor_sharpe: float = 0.30
    neighborhood_include_joint: bool = True
    # Stage 7 -- multiple testing
    fdr_q: float = 0.05
    fdr_method: str = "bh"              # "bh" (default) or "by" (dependence-robust)
    # Family the FDR correction is applied over:
    #   "full_search" (default): every tested config is a hypothesis (the honest,
    #     stringent reading of "account for the full search including rejected configs").
    #   "screened": only the configs that reach the FDR stage -- a less conservative
    #     sensitivity that treats pre-screening as narrowing the hypothesis set.
    fdr_family: str = "full_search"
    bootstrap_n: int = 4000
    bootstrap_block: int = 6
    bootstrap_seed: int = 0
    # Stage 8 -- validation
    min_val_net_return: float = 0.0
    min_val_sharpe: float = 0.30
    # Stage 11 -- deduplication
    dedup_corr_threshold: float = 0.80
    # Stage 12 -- final (untouched) test
    min_holdout_net_return: float = 0.0
    min_holdout_sharpe: float = 0.0

    def frozen_dict(self) -> dict:
        return asdict(self)


@dataclass
class StageResult:
    stage: str
    description: str
    n_before: int
    n_after: int
    extra: dict = field(default_factory=dict)


def _passes_activity(rec: dict, n_years_dev: float, t: FunnelThresholds) -> bool:
    tpy = (rec["dev_n_trades"] / n_years_dev) if n_years_dev > 0 else 0.0
    active_years = sum(1 for _, c in (rec.get("dev_trades_by_year") or {}).items() if c and c > 0)
    return tpy >= t.min_trades_per_year and active_years >= t.min_active_years


def run_funnel(records: list[dict], *, thresholds: FunnelThresholds, n_years_dev: float):
    """Run the pure stages (2-5, 7, 8, 11, 12). Returns (stages, state) where
    `state` carries survivor id-sets per stage, per-config rejection reason, the
    p-value / FDR diagnostics, and the surviving records enriched with
    neighborhood + p-value + cluster fields. Stress/transfer are appended later.
    """
    t = thresholds
    by_id = {r["config_id"]: r for r in records}
    m_total = len(records)  # full search -> family size for FDR
    reason: dict[str, str] = {}
    stages: list[StageResult] = []

    # Stage 2: trade count + annual coverage.
    s2 = [r for r in records if _passes_activity(r, n_years_dev, t)]
    for r in records:
        if r not in s2:
            reason[r["config_id"]] = "trade_count_or_coverage"
    stages.append(StageResult("2_trade_count",
        f">= {t.min_trades_per_year:.0f} trades/yr & active in >= {t.min_active_years} dev years",
        len(records), len(s2)))

    # Stage 3: profitability after costs.
    s3 = [r for r in s2 if (r["dev_net_return"] or -1) > t.min_dev_net_return
          and (r["dev_profit_factor"] or 0) >= t.min_profit_factor]
    for r in s2:
        if r not in s3:
            reason[r["config_id"]] = "profitability"
    stages.append(StageResult("3_profitability",
        f"dev net return > 0 & profit factor >= {t.min_profit_factor}", len(s2), len(s3)))

    # Stage 4: risk (daily Sharpe).
    s4 = [r for r in s3 if (r["dev_sharpe"] is not None and r["dev_sharpe"] >= t.min_dev_sharpe)]
    for r in s3:
        if r not in s4:
            reason[r["config_id"]] = "risk_sharpe"
    stages.append(StageResult("4_risk", f"dev Sharpe >= {t.min_dev_sharpe}", len(s3), len(s4)))

    # Stage 5: neighborhood stability (computed over the FULL grid using dev metrics).
    nstats = neighborhood_stats(records, net_return_key="dev_net_return", sharpe_key="dev_sharpe",
                                include_joint=t.neighborhood_include_joint)
    s5 = []
    for r in s4:
        ns = nstats[r["config_id"]]
        r["neighbor_frac_profitable"] = ns.frac_profitable
        r["neighbor_median_sharpe"] = ns.median_sharpe
        r["n_neighbors"] = ns.n_neighbors
        ok = (ns.n_neighbors > 0 and ns.frac_profitable >= t.min_frac_profitable_neighbors
              and (ns.median_sharpe == ns.median_sharpe)  # not NaN
              and ns.median_sharpe >= t.min_median_neighbor_sharpe)
        if ok:
            s5.append(r)
        else:
            reason[r["config_id"]] = "neighborhood_stability"
    stages.append(StageResult("5_neighborhood",
        f">= {t.min_frac_profitable_neighbors:.0%} profitable neighbors & median neighbor Sharpe >= {t.min_median_neighbor_sharpe}",
        len(s4), len(s5)))

    # Stage 7: multiple-testing control (dependence-aware p-values + FDR over the full search).
    for r in s5:
        r["pvalue"] = block_bootstrap_pvalue(
            r.get("monthly_returns") or [], n_boot=t.bootstrap_n, block=t.bootstrap_block, seed=t.bootstrap_seed
        )
    pvals = np.array([r["pvalue"] for r in s5], dtype=float)
    m_fdr = m_total if t.fdr_family == "full_search" else len(s5)
    bh_mask, bh_cut = benjamini_hochberg(pvals, q=t.fdr_q, m_total=m_fdr)
    by_mask, by_cut = benjamini_yekutieli(pvals, q=t.fdr_q, m_total=m_fdr)
    chosen_mask = bh_mask if t.fdr_method == "bh" else by_mask
    s7 = [r for r, keep in zip(s5, chosen_mask) if keep]
    for r, keep in zip(s5, chosen_mask):
        if not keep:
            reason[r["config_id"]] = "fdr_not_significant"
    stages.append(StageResult("7_multiple_testing",
        f"{t.fdr_method.upper()}-FDR q={t.fdr_q}, family={t.fdr_family} (m={m_fdr} of {m_total} tested)",
        len(s5), len(s7),
        extra={"bh_cutoff": bh_cut, "by_cutoff": by_cut, "n_bh": int(bh_mask.sum()),
               "n_by": int(by_mask.sum()), "m_fdr": m_fdr, "m_total": m_total}))

    # Stage 8: validation (survivors run unchanged on validation data).
    s8 = [r for r in s7 if (r["val_net_return"] or -1) > t.min_val_net_return
          and (r["val_sharpe"] is not None and r["val_sharpe"] >= t.min_val_sharpe)]
    for r in s7:
        if r not in s8:
            reason[r["config_id"]] = "validation"
    stages.append(StageResult("8_validation",
        f"validation net return > 0 & Sharpe >= {t.min_val_sharpe}", len(s7), len(s8)))

    state = {
        "by_id": by_id, "reason": reason, "m_total": m_total,
        "survivors_pre_stress": s8,
        "fdr": {"bh_cutoff": bh_cut, "by_cutoff": by_cut, "n_bh": int(bh_mask.sum()), "n_by": int(by_mask.sum())},
    }
    return stages, state


def deduplicate(survivors: list[dict], *, corr_threshold: float) -> tuple[list[dict], dict[str, int]]:
    """Greedy correlation clustering on development monthly returns; keep the
    highest-validation-Sharpe representative per cluster. Returns (reps, cluster_of)."""
    if not survivors:
        return [], {}
    ordered = sorted(survivors, key=lambda r: (r.get("val_sharpe") or -1e9), reverse=True)
    series = {r["config_id"]: np.asarray(r.get("monthly_returns") or [], dtype=float) for r in ordered}

    reps: list[dict] = []
    cluster_of: dict[str, int] = {}
    for r in ordered:
        if r["config_id"] in cluster_of:
            continue
        cid = len(reps)
        reps.append(r)
        cluster_of[r["config_id"]] = cid
        a = series[r["config_id"]]
        for other in ordered:
            oid = other["config_id"]
            if oid in cluster_of:
                continue
            b = series[oid]
            if len(a) == len(b) and len(a) > 2 and np.std(a) > 0 and np.std(b) > 0:
                corr = float(np.corrcoef(a, b)[0, 1])
                if corr >= corr_threshold:
                    cluster_of[oid] = cid
    return reps, cluster_of


def final_test(finalists: list[dict], *, thresholds: FunnelThresholds) -> list[dict]:
    """Evaluate frozen finalists on the untouched holdout; mark pass/fail (report
    only -- selection was frozen before the holdout was touched)."""
    t = thresholds
    out = []
    for r in finalists:
        passed = ((r["holdout_net_return"] or -1) > t.min_holdout_net_return
                  and r["holdout_sharpe"] is not None and r["holdout_sharpe"] >= t.min_holdout_sharpe)
        out.append({**r, "holdout_pass": passed})
    return out
