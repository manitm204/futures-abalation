"""Turn a completed ablation run into findings: a markdown report + a JSON
summary (the summary feeds an optional visual Artifact).

Findings produced (all out-of-sample aware):
  1. Activity gate     -- variants trading >= min-trades/year in development.
  2. Leaderboard       -- eligible variants ranked by validation Sharpe.
  3. Best variant      -- its full config and dev -> validation -> holdout table.
  4. Axis ablation     -- per axis value, median dev/validation Sharpe (which knob moves results).
  5. Top-cohort shared config -- enrichment of each axis value in the top cohort vs baseline
                          (normalized, so a merely-common value isn't mistaken for a good one).
  6. In-sample -> OOS rank stability -- Spearman(dev Sharpe, validation Sharpe) (overfitting check).
  7. Cross-symbol      -- does the best variant's recipe also work on the other symbol?
  8. Verdict           -- did anything survive positive across dev AND validation AND holdout?

Reuses src/analysis/rankings.py and src/analysis/parameter_analysis.py unchanged.

Usage:
  python scripts/build_ablation_report.py --experiment-id donchian_v1 --min-trades-per-year 100
"""

from __future__ import annotations

import statistics
from pathlib import Path

import typer

from src.analysis.parameter_analysis import categorical_enrichment
from src.analysis.rankings import rank_correlation, top_n
from src.experiments.grid import AXES
from src.utils.serialization import atomic_write_json, read_json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
app = typer.Typer()

ABLATION_AXES = [k for k in AXES if k != "timeframe"] + ["timeframe"]
PRIMARY = "validation_sharpe"


def _load_results(results_dir: Path, experiment_id: str) -> list[dict]:
    base = results_dir / f"experiment_id={experiment_id}"
    out = []
    for p in sorted(base.glob("*.json")):
        r = read_json(p)
        if r.get("status") == "ok":
            out.append(r)
    return out


def _m(r: dict, key: str):
    return r.get("metrics", {}).get(key)


def _fmt(v, pct=False, nd=2):
    if v is None:
        return "—"
    if pct:
        return f"{v * 100:.1f}%"
    return f"{v:.{nd}f}"


def _split_row(r: dict, split: str) -> str:
    g = lambda k: _m(r, f"{split}_{k}")  # noqa: E731
    return (
        f"| {split} | {g('n_trades')} | {g('trades_per_year'):.0f} | {_fmt(g('net_return_pct'), pct=True)} "
        f"| {_fmt(g('sharpe'))} | {_fmt(g('profit_factor'))} | {_fmt(g('win_rate'), pct=True)} "
        f"| {_fmt(g('max_dd'), pct=True)} | {_fmt(g('expectancy'))} |"
    )


@app.command()
def main(
    experiment_id: str = typer.Option(...),
    min_trades_per_year: float = typer.Option(100.0, help="Development activity gate"),
    top_cohort_frac: float = typer.Option(0.10, help="Top fraction (by validation Sharpe) for enrichment"),
    results_dir: Path = typer.Option(PROJECT_ROOT / "runs" / "results"),
    out_md: Path = typer.Option(PROJECT_ROOT / "runs" / "reports" / "ablation.md"),
    out_json: Path = typer.Option(PROJECT_ROOT / "runs" / "reports" / "ablation_summary.json"),
) -> None:
    results = _load_results(results_dir, experiment_id)
    if not results:
        raise typer.BadParameter(f"No ok results for experiment_id={experiment_id}")

    eligible = [r for r in results if (_m(r, "development_trades_per_year") or 0) >= min_trades_per_year]

    # Leaderboard + best by validation Sharpe among the activity-gated set.
    ranked = top_n(eligible, metric=PRIMARY, n=len(eligible), higher_is_better=True)
    best = ranked[0] if ranked else None

    # Top cohort for enrichment.
    k = max(10, int(len(ranked) * top_cohort_frac))
    cohort = ranked[:k]

    lines: list[str] = []
    A = lines.append

    A(f"# Donchian Breakout — Ablation Study Findings\n")
    A(f"**Experiment:** `{experiment_id}` · **Base strategy:** Donchian channel breakout (intraday, RTH)\n")
    A(
        "The study enumerates the **full factorial** of the discrete axes below and backtests every "
        "variant once over 2018–2026, scoring each on three chronological, non-overlapping splits: "
        "**development** (in-sample, 2018–2022), **validation** (out-of-sample, 2023–2024), and "
        "**holdout** (out-of-sample, 2025–2026). Costs (commission + slippage) are applied to every trade.\n"
    )

    A("## Axes tested\n")
    A("| Axis | Values |")
    A("|---|---|")
    for name, vals in AXES.items():
        A(f"| `{name}` | {', '.join(str(v) for v in vals)} |")
    A("")
    A(f"- **Total variants run:** {len(results):,} (ok). ")
    A(f"- **Activity gate:** ≥ {min_trades_per_year:.0f} trades/yr in development → **{len(eligible):,} eligible**.\n")

    # --- Verdict (stated up front, honestly) ---
    survivors = [
        r for r in eligible
        if (_m(r, "development_net_return_pct") or -1) > 0
        and (_m(r, "validation_net_return_pct") or -1) > 0
        and (_m(r, "holdout_net_return_pct") or -1) > 0
    ]
    A("## Verdict\n")
    if survivors:
        A(
            f"**{len(survivors)} of {len(eligible):,} eligible variants were net-positive after costs in "
            f"ALL THREE periods** (development, validation, and holdout). This is the set that did not simply "
            "curve-fit the in-sample window. Details below; treat even these with caution given the number of "
            "variants tried (multiple-comparisons risk).\n"
        )
    else:
        A(
            f"**No variant was net-positive after costs across all three periods** (development, validation, AND "
            f"holdout) while meeting the activity gate. In other words, the naive Donchian breakout — on SPY/QQQ "
            "intraday RTH, with realistic costs — does **not** survive honest out-of-sample testing in any of the "
            f"{len(eligible):,} forms tried. That is itself the finding: the ablation did its job by refusing to "
            "manufacture a false positive.\n"
        )

    # --- Best variant ---
    if best:
        A("## Best variant (by validation Sharpe, among eligible)\n")
        cfg = best["config"]
        knobs = ", ".join(f"`{a}={cfg[a]}`" for a in ABLATION_AXES)
        A(f"**{cfg['symbol']}** — {knobs}\n")
        A("| Split | Trades | Trades/yr | Net return | Sharpe | Profit factor | Win rate | Max DD | Expectancy/trade |")
        A("|---|---|---|---|---|---|---|---|---|")
        for s in ("development", "validation", "holdout"):
            A(_split_row(best, s))
        A("")

    # --- Leaderboard ---
    A("## Leaderboard — top 15 eligible (ranked by validation Sharpe)\n")
    A("| # | Symbol | TF | lookback | breakout | trend | dir | stop | target | time_exit | Dev Shrp | **Val Shrp** | Hold Shrp | Val ret |")
    A("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(ranked[:15], 1):
        c = r["config"]
        A(
            f"| {i} | {c['symbol']} | {c['timeframe']} | {c['channel_lookback']} | {c['breakout_price']} "
            f"| {c['trend_filter']} | {c['direction']} | {c['stop']} | {c['target']} | {c['time_exit']} "
            f"| {_fmt(_m(r,'development_sharpe'))} | **{_fmt(_m(r,'validation_sharpe'))}** "
            f"| {_fmt(_m(r,'holdout_sharpe'))} | {_fmt(_m(r,'validation_net_return_pct'), pct=True)} |"
        )
    A("")

    # --- Axis ablation importance ---
    A("## Axis ablation — median Sharpe by setting (all ok variants)\n")
    A("How much each knob moves results, holding nothing else fixed (marginal over the whole grid).\n")
    axis_importance: dict[str, list[dict]] = {}
    for axis in ABLATION_AXES + (["timeframe"] if "timeframe" not in ABLATION_AXES else []):
        A(f"### `{axis}`")
        A("| value | n | median dev Sharpe | median val Sharpe | median holdout Sharpe |")
        A("|---|---|---|---|---|")
        rows = []
        for val in AXES[axis]:
            grp = [r for r in results if r["config"].get(axis) == val]
            def med(split):
                xs = [_m(r, f"{split}_sharpe") for r in grp if _m(r, f"{split}_sharpe") is not None]
                return statistics.median(xs) if xs else None
            dev, v, h = med("development"), med("validation"), med("holdout")
            rows.append({"value": val, "n": len(grp), "dev": dev, "val": v, "holdout": h})
            A(f"| {val} | {len(grp)} | {_fmt(dev)} | {_fmt(v)} | {_fmt(h)} |")
        axis_importance[axis] = rows
        A("")

    # --- Top-cohort shared config (enrichment) ---
    A(f"## Shared configuration in the top cohort (top {len(cohort)} by validation Sharpe)\n")
    A(
        "Enrichment = how much more frequent an axis value is in the top cohort than in the eligible baseline. "
        "A ratio **> 1** means the top variants disproportionately share that setting; **< 1** means they avoid it. "
        "Normalizing by baseline frequency is what separates *'good'* from merely *'common'*.\n"
    )
    enrichment_out: dict[str, list] = {}
    for axis in ABLATION_AXES:
        rows = categorical_enrichment(eligible, cohort, param=axis)
        enrichment_out[axis] = [
            {"value": str(r.value), "baseline": r.baseline_frequency, "top": r.top_n_frequency, "ratio": r.enrichment_ratio}
            for r in rows
        ]
        top_line = ", ".join(
            f"`{r.value}` ×{r.enrichment_ratio:.2f}" for r in rows[:2] if r.enrichment_ratio is not None
        )
        A(f"- **`{axis}`** — most enriched: {top_line or '—'}")
    A("")

    # --- In-sample -> OOS rank stability ---
    rc = rank_correlation(eligible, metric_a="development_sharpe", metric_b="validation_sharpe")
    A("## In-sample → out-of-sample rank stability\n")
    if rc:
        verdict = (
            "In-sample ranking is essentially **useless** for predicting out-of-sample ranking"
            if abs(rc.spearman_rho) < 0.2 else
            "In-sample ranking carries **some** signal for out-of-sample ranking"
        )
        A(
            f"Spearman ρ(development Sharpe, validation Sharpe) = **{rc.spearman_rho:.3f}** "
            f"(p={rc.p_value:.2g}, n={rc.n}). {verdict} — the central overfitting check: if ρ≈0, picking the "
            "in-sample winner is no better than chance out of sample.\n"
        )
    else:
        A("Not enough paired data to compute rank correlation.\n")

    # --- Cross-symbol generalization ---
    A("## Cross-symbol generalization\n")
    if best:
        c = best["config"]
        other = "QQQ" if c["symbol"] == "SPY" else "SPY"
        twin = next(
            (r for r in results if all(r["config"].get(a) == c[a] for a in ABLATION_AXES) and r["config"]["symbol"] == other),
            None,
        )
        if twin:
            A(f"The best **{c['symbol']}** recipe, applied unchanged to **{other}**:\n")
            A("| Symbol | Dev Sharpe | Val Sharpe | Holdout Sharpe | Val net return |")
            A("|---|---|---|---|---|")
            for r in (best, twin):
                A(
                    f"| {r['config']['symbol']} | {_fmt(_m(r,'development_sharpe'))} | {_fmt(_m(r,'validation_sharpe'))} "
                    f"| {_fmt(_m(r,'holdout_sharpe'))} | {_fmt(_m(r,'validation_net_return_pct'), pct=True)} |"
                )
            A("\nIf the twin's numbers collapse, the 'best' recipe was symbol-specific curve-fitting, not a real edge.\n")
        else:
            A(f"No matching {other} variant found for the best recipe.\n")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines))

    atomic_write_json(
        out_json,
        {
            "experiment_id": experiment_id,
            "n_variants": len(results),
            "n_eligible": len(eligible),
            "min_trades_per_year": min_trades_per_year,
            "n_survivors_all_splits": len(survivors),
            "best": best["config"] if best else None,
            "best_metrics": best["metrics"] if best else None,
            "leaderboard": [
                {"config": r["config"], "metrics": {k2: _m(r, k2) for k2 in (
                    "development_sharpe", "validation_sharpe", "holdout_sharpe",
                    "validation_net_return_pct", "development_net_return_pct", "holdout_net_return_pct",
                    "development_trades_per_year")}}
                for r in ranked[:50]
            ],
            "axis_importance": axis_importance,
            "enrichment": enrichment_out,
            "rank_stability": {"spearman_rho": rc.spearman_rho, "p_value": rc.p_value, "n": rc.n} if rc else None,
        },
    )
    typer.echo(f"Wrote {out_md} and {out_json}  (variants={len(results)}, eligible={len(eligible)}, survivors={len(survivors)})")


if __name__ == "__main__":
    app()
