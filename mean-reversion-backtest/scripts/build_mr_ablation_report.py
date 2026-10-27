"""Per-axis ablation report for a mean-reversion funnel run, DEVELOPMENT data only.

Reads runs/funnel/<experiment>/config_status.parquet (written by
`run_mr_funnel.py develop`; one development backtest per grid config) and asks
which settings matter, without touching validation or holdout data:

  1. Axis ablation -- per axis value: configs, % profitable, median / p90 dev
     Sharpe, % clearing the stage-3 Sharpe bar, % reaching the stage-3 survivors.
  2. Activity-eligible view -- the same medians among configs that pass the
     stage-2 trade-count gate (so low-activity configs don't dominate).
  3. Top-cohort enrichment -- share of each axis value among the top-N eligible
     configs by dev Sharpe vs. its share of the whole grid (lift).
  4. Funnel survival by stage.

Everything here is in-sample. It describes the search surface; it is not
evidence that any setting works out of sample.

Usage:
  PYTHONPATH=. python scripts/build_mr_ablation_report.py --experiment-id mr_es_v3 \
      --config configs/funnel/mr_funnel_es_v3.yaml
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import polars as pl
import typer

from src.experiments.funnel_config import load_funnel_config
from src.experiments.mr_grid import AXES, AXES_V2, AXES_V3, AXES_V5, AXES_V6, AXES_V7, AXES_V8, AXES_V9, AXES_V10, AXES_V11, AXES_V12, AXES_V13, AXES_V14, AXES_V15, AXES_V16, AXES_V17, AXES_V18, AXES_V19, AXES_V20, AXES_V21
from src.utils.serialization import atomic_write_json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
AXES_BY_STRATEGY = {"mean_reversion": AXES, "mean_reversion_v2": AXES_V2, "mean_reversion_v3": AXES_V3, "mean_reversion_v5": AXES_V5, "mean_reversion_v6": AXES_V6, "mean_reversion_v7": AXES_V7, "mean_reversion_v8": AXES_V8, "mean_reversion_v9": AXES_V9, "mean_reversion_v10": AXES_V10, "mean_reversion_v11": AXES_V11, "mean_reversion_v12": AXES_V12, "mean_reversion_v13": AXES_V13, "mean_reversion_v14": AXES_V14, "mean_reversion_v15": AXES_V15, "mean_reversion_v16": AXES_V16, "mean_reversion_v17": AXES_V17, "mean_reversion_v18": AXES_V18, "mean_reversion_v19": AXES_V19, "mean_reversion_v20": AXES_V20, "mean_reversion_v21": AXES_V21}
app = typer.Typer(add_completion=False)


def _f(x, nd=2, pct=False) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "n/a"
    return f"{100 * x:.1f}%" if pct else f"{x:.{nd}f}"


def _q(s: pl.Series, q: float) -> float | None:
    s = s.drop_nulls()
    return float(s.quantile(q)) if len(s) else None


@app.command()
def main(
    experiment_id: str = typer.Option(...),
    config: Path = typer.Option(...),
    top_n: int = typer.Option(100, help="Top-cohort size (eligible configs by dev Sharpe)"),
    runs_root: Path = typer.Option(PROJECT_ROOT / "runs" / "funnel"),
) -> None:
    fcfg = load_funnel_config(config)
    axes = AXES_BY_STRATEGY[fcfg.strategy]
    exp = runs_root / experiment_id
    df = pl.read_parquet(exp / "config_status.parquet")
    sh_bar = fcfg.performance.min_sharpe
    df = df.with_columns(
        (pl.col("s2_status") == "pass").alias("_eligible"),
        (pl.col("dev_net_return") > 0).alias("_profitable"),
        (pl.col("dev_sharpe") >= sh_bar).alias("_sharpe_ok"),
        (pl.col("s3_status") == "pass").alias("_s3"),
        (pl.col("s7_status") == "pass").alias("_survivor"),
    )
    n = df.height
    elig = df.filter("_eligible")
    top = elig.sort("dev_sharpe", descending=True, nulls_last=True).head(top_n)

    rows = []
    for ax, vals in axes.items():
        for v in vals:
            sub = df.filter(pl.col(ax) == v)
            esub = elig.filter(pl.col(ax) == v)
            share = sub.height / n
            tshare = top.filter(pl.col(ax) == v).height / top.height if top.height else None
            rows.append({
                "axis": ax, "value": str(v), "n": sub.height,
                "pct_profitable": float(sub["_profitable"].mean()),
                "median_sharpe": _q(sub["dev_sharpe"], 0.5), "p90_sharpe": _q(sub["dev_sharpe"], 0.9),
                "pct_sharpe_ok": float(sub["_sharpe_ok"].fill_null(False).mean()),
                "pct_eligible": float(sub["_eligible"].mean()),
                "eligible_median_sharpe": _q(esub["dev_sharpe"], 0.5),
                "n_stage3": int(sub["_s3"].sum()), "n_survivors": int(sub["_survivor"].sum()),
                "median_trades": _q(sub["dev_n_completed_trades"].cast(pl.Float64), 0.5),
                "top_share": tshare, "grid_share": share,
                "top_lift": (tshare / share) if tshare is not None and share else None,
            })

    # Spread of median Sharpe across an axis's values = how much that axis matters.
    importance = []
    for ax in axes:
        meds = [r["median_sharpe"] for r in rows if r["axis"] == ax and r["median_sharpe"] is not None]
        importance.append({"axis": ax, "median_sharpe_range": (max(meds) - min(meds)) if meds else None})
    importance.sort(key=lambda r: -(r["median_sharpe_range"] or 0))

    stable = pl.read_csv(exp / "survivor_table.csv").to_dicts()
    best = elig.sort("dev_sharpe", descending=True, nulls_last=True).head(15)

    L = [f"# Ablation (development only) -- {experiment_id}", "",
         f"- Symbol {fcfg.symbol}, strategy `{fcfg.strategy}`, {n:,} configs, development "
         f"{fcfg.data.development.start}..{fcfg.data.development.end}. Validation and holdout are NOT used here.",
         f"- Eligible = passes stage 2 (>= {fcfg.trade_count.min_completed_trades} completed trades, "
         f">= {fcfg.trade_count.min_trades_per_year}/yr in >= {fcfg.trade_count.min_years_meeting_floor} years): "
         f"{elig.height:,} configs ({_f(elig.height / n, pct=True)}).",
         f"- Grid-wide: {_f(float(df['_profitable'].mean()), pct=True)} profitable, median dev Sharpe "
         f"{_f(_q(df['dev_sharpe'], 0.5))}, {int(df['_sharpe_ok'].fill_null(False).sum())} configs with Sharpe >= {sh_bar}.",
         "", "## Funnel survival", "", "| Stage | Evaluated | Passed | Note |", "|---|---:|---:|---|"]
    for t in stable:
        L.append(f"| {t['stage']} | {t.get('evaluated') if t.get('evaluated') is not None else ''} | "
                 f"{t.get('passed') if t.get('passed') is not None else ''} | {t.get('note') or ''} |")
    L += ["", "## Which axes matter (range of per-value median dev Sharpe)", "",
          "| Axis | Median-Sharpe range |", "|---|---:|"]
    L += [f"| {r['axis']} | {_f(r['median_sharpe_range'], 3)} |" for r in importance]
    L += ["", "## Per-axis ablation", "",
          f"Top cohort = best {top.height} eligible configs by dev Sharpe; lift = share in top cohort / share of grid.", "",
          "| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |",
          "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in rows:
        L.append(f"| {r['axis']} | {r['value']} | {r['n']} | {_f(r['pct_profitable'], pct=True)} | "
                 f"{_f(r['median_sharpe'])} | {_f(r['p90_sharpe'])} | {_f(r['pct_sharpe_ok'], pct=True)} | "
                 f"{_f(r['pct_eligible'], pct=True)} | {_f(r['eligible_median_sharpe'])} | {_f(r['median_trades'], 0)} | "
                 f"{r['n_stage3']} | {r['n_survivors']} | {_f(r['top_lift'])} |")
    L += ["", "## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)", "",
          "| # | " + " | ".join(axes) + " | trades | net ret | Sharpe | maxDD | final stage status |",
          "|---|" + "---|" * len(axes) + "---:|---:|---:|---:|---|"]
    for i, r in enumerate(best.iter_rows(named=True), 1):
        L.append(f"| {i} | " + " | ".join(str(r[a]) for a in axes) +
                 f" | {r['dev_n_completed_trades']} | {_f(r['dev_net_return'], pct=True)} | {_f(r['dev_sharpe'])} | "
                 f"{_f(r['dev_max_drawdown'], pct=True)} | s{r['last_stage_evaluated']} {r['final_status']} |")
    L += ["", "All figures are in-sample development results across a large search; the best rows are "
          "expected to look good by chance alone. Out-of-sample evidence comes only from `validate`."]
    (exp / "ablation.md").write_text("\n".join(L) + "\n")
    atomic_write_json(exp / "ablation_summary.json", {"experiment_id": experiment_id, "n_configs": n,
                      "n_eligible": elig.height, "axis_importance": importance, "axes": rows})
    typer.echo(f"wrote {exp / 'ablation.md'}")


if __name__ == "__main__":
    app()
