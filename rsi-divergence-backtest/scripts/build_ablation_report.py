"""Turn a completed ablation run into findings: a markdown report + a JSON
summary (the summary feeds an optional visual Artifact).

Strategy-agnostic: the parameter axes and their values are **inferred from the
result configs** (any key that varies across variants, except `symbol`), so the
same report works for every ablation grid in this repo.

Findings produced (all out-of-sample aware):
  1. Activity gate     -- variants trading >= min-trades/year in development.
  2. Leaderboard       -- eligible variants ranked by validation Sharpe.
  3. Best variant      -- its full config and dev -> validation -> holdout table.
  4. Axis ablation     -- per axis value, median dev/validation Sharpe.
  5. Top-cohort shared config -- enrichment of each axis value in the top cohort vs baseline.
  6. In-sample -> OOS rank stability -- Spearman(dev Sharpe, validation Sharpe).
  7. Cross-symbol      -- (multi-symbol runs only) does the best recipe travel?
  8. Verdict           -- did anything survive positive across dev AND validation AND holdout?

Reuses src/analysis/rankings.py and src/analysis/parameter_analysis.py unchanged.

Usage:
  python scripts/build_ablation_report.py --experiment-id channel_v1 --min-trades-per-year 100
"""

from __future__ import annotations

import statistics
from pathlib import Path

import typer

from src.analysis.parameter_analysis import categorical_enrichment
from src.analysis.rankings import rank_correlation, top_n
from src.utils.serialization import atomic_write_json, read_json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
app = typer.Typer()

PRIMARY = "validation_sharpe"
NON_AXIS = {"symbol", "atr_period"}


def _load_results(results_dir: Path, experiment_id: str) -> list[dict]:
    base = results_dir / f"experiment_id={experiment_id}"
    out = []
    for p in sorted(base.glob("*.json")):
        r = read_json(p)
        if r.get("status") == "ok":
            out.append(r)
    return out


def _sort_vals(vals: set):
    try:
        return sorted(vals, key=lambda x: (0, float(x)))
    except (TypeError, ValueError):
        return sorted(vals, key=str)


def _infer_axes(results: list[dict]) -> dict[str, list]:
    """Any config key whose value varies across variants is an axis (except
    symbol / atr_period). Values are returned sorted (numeric if possible)."""
    keys = set()
    for r in results:
        keys |= set(r.get("config", {}).keys())
    axes: dict[str, list] = {}
    for k in keys:
        if k in NON_AXIS:
            continue
        vals = {r["config"].get(k) for r in results if r["config"].get(k) is not None}
        if len(vals) > 1:
            axes[k] = _sort_vals(vals)
    # Deterministic, readable order: non-timeframe axes first, timeframe last.
    ordered = sorted(axes, key=lambda k: (k == "timeframe", k))
    return {k: axes[k] for k in ordered}


def _m(r: dict, key: str):
    return r.get("metrics", {}).get(key)


def _fmt(v, pct=False, nd=2):
    if v is None:
        return "—"
    return f"{v * 100:.1f}%" if pct else f"{v:.{nd}f}"


@app.command()
def main(
    experiment_id: str = typer.Option(...),
    min_trades_per_year: float = typer.Option(100.0, help="Development activity gate"),
    top_cohort_frac: float = typer.Option(0.10, help="Top fraction (by validation Sharpe) for enrichment"),
    results_dir: Path = typer.Option(PROJECT_ROOT / "runs" / "results"),
    out_md: Path = typer.Option(None),
    out_json: Path = typer.Option(None),
) -> None:
    out_md = out_md or (PROJECT_ROOT / "runs" / "reports" / f"{experiment_id}.md")
    out_json = out_json or (PROJECT_ROOT / "runs" / "reports" / f"{experiment_id}_summary.json")

    results = _load_results(results_dir, experiment_id)
    if not results:
        raise typer.BadParameter(f"No ok results for experiment_id={experiment_id}")

    axes = _infer_axes(results)
    axis_names = list(axes.keys())
    symbols = sorted({r["config"].get("symbol") for r in results})

    eligible = [r for r in results if (_m(r, "development_trades_per_year") or 0) >= min_trades_per_year]
    ranked = top_n(eligible, metric=PRIMARY, n=len(eligible), higher_is_better=True)
    best = ranked[0] if ranked else None
    k = max(10, int(len(ranked) * top_cohort_frac))
    cohort = ranked[:k]

    lines: list[str] = []
    A = lines.append

    A("# Ablation Study Findings\n")
    A(f"**Experiment:** `{experiment_id}` · **Symbols:** {', '.join(symbols)}\n")
    A(
        "Full-factorial grid; every variant backtested once over 2018–2026 and scored on three "
        "chronological, non-overlapping splits: **development** (in-sample, 2018–2022), "
        "**validation** (OOS, 2023–2024), and **holdout** (OOS, 2025–2026). Costs applied to every trade.\n"
    )

    A("## Axes tested\n")
    A("| Axis | Values |")
    A("|---|---|")
    for name, vals in axes.items():
        A(f"| `{name}` | {', '.join(str(v) for v in vals)} |")
    A("")
    A(f"- **Total variants run:** {len(results):,} (ok).")
    A(f"- **Activity gate:** ≥ {min_trades_per_year:.0f} trades/yr in development → **{len(eligible):,} eligible**.\n")

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
            "ALL THREE periods** (development, validation, holdout) — the set that did not merely curve-fit "
            "the in-sample window. Treat with caution: with this many variants tried, some pass by chance "
            "(multiple-comparisons risk).\n"
        )
    else:
        A(
            f"**No eligible variant was net-positive after costs across all three periods.** The strategy, in "
            f"any of the {len(eligible):,} forms tried, does not survive honest out-of-sample testing. That "
            "refusal is itself the finding.\n"
        )

    if best:
        A("## Best variant (by validation Sharpe, among eligible)\n")
        cfg = best["config"]
        knobs = ", ".join(f"`{a}={cfg.get(a)}`" for a in axis_names)
        extra = f" · exit_lookback={best.get('exit_lookback')}" if "exit_lookback" in best else ""
        A(f"**{cfg.get('symbol')}** — {knobs}{extra}\n")
        A("| Split | Trades | Trades/yr | Net return | Sharpe | Profit factor | Win rate | Max DD | Expectancy/trade |")
        A("|---|---|---|---|---|---|---|---|---|")
        for s in ("development", "validation", "holdout"):
            g = lambda key: _m(best, f"{s}_{key}")  # noqa: E731
            A(
                f"| {s} | {g('n_trades')} | {g('trades_per_year'):.0f} | {_fmt(g('net_return_pct'), pct=True)} "
                f"| {_fmt(g('sharpe'))} | {_fmt(g('profit_factor'))} | {_fmt(g('win_rate'), pct=True)} "
                f"| {_fmt(g('max_dd'), pct=True)} | {_fmt(g('expectancy'))} |"
            )
        A("")

    # Leaderboard with dynamic axis columns.
    A("## Leaderboard — top 15 eligible (ranked by validation Sharpe)\n")
    header = ["#", "symbol"] + axis_names + ["Dev Shrp", "**Val Shrp**", "Hold Shrp", "Val ret"]
    A("| " + " | ".join(header) + " |")
    A("|" + "---|" * len(header))
    for i, r in enumerate(ranked[:15], 1):
        c = r["config"]
        cells = [str(i), str(c.get("symbol"))] + [str(c.get(a)) for a in axis_names]
        cells += [_fmt(_m(r, "development_sharpe")), f"**{_fmt(_m(r, 'validation_sharpe'))}**",
                  _fmt(_m(r, "holdout_sharpe")), _fmt(_m(r, "validation_net_return_pct"), pct=True)]
        A("| " + " | ".join(cells) + " |")
    A("")

    # Axis ablation importance.
    A("## Axis ablation — median Sharpe by setting (all ok variants)\n")
    axis_importance: dict[str, list[dict]] = {}
    for axis in axis_names:
        A(f"### `{axis}`")
        A("| value | n | median dev Sharpe | median val Sharpe | median holdout Sharpe |")
        A("|---|---|---|---|---|")
        rows = []
        for val in axes[axis]:
            grp = [r for r in results if r["config"].get(axis) == val]

            def med(split, grp=grp):
                xs = [_m(r, f"{split}_sharpe") for r in grp if _m(r, f"{split}_sharpe") is not None]
                return statistics.median(xs) if xs else None

            dev, v, h = med("development"), med("validation"), med("holdout")
            rows.append({"value": val, "n": len(grp), "dev": dev, "val": v, "holdout": h})
            A(f"| {val} | {len(grp)} | {_fmt(dev)} | {_fmt(v)} | {_fmt(h)} |")
        axis_importance[axis] = rows
        A("")

    # Top-cohort enrichment.
    A(f"## Shared configuration in the top cohort (top {len(cohort)} by validation Sharpe)\n")
    A(
        "Enrichment = frequency of an axis value in the top cohort ÷ its frequency in the eligible baseline. "
        "A ratio **> 1** means the top variants disproportionately share that setting. Normalizing by baseline "
        "separates *good* from merely *common*.\n"
    )
    enrichment_out: dict[str, list] = {}
    for axis in axis_names:
        erows = categorical_enrichment(eligible, cohort, param=axis)
        enrichment_out[axis] = [
            {"value": str(r.value), "baseline": r.baseline_frequency, "top": r.top_n_frequency, "ratio": r.enrichment_ratio}
            for r in erows
        ]
        top_line = ", ".join(f"`{r.value}` ×{r.enrichment_ratio:.2f}" for r in erows[:3] if r.enrichment_ratio is not None)
        A(f"- **`{axis}`** — most enriched: {top_line or '—'}")
    A("")

    rc = rank_correlation(eligible, metric_a="development_sharpe", metric_b="validation_sharpe")
    A("## In-sample → out-of-sample rank stability\n")
    if rc:
        verdict = ("essentially **useless**" if abs(rc.spearman_rho) < 0.2 else "carries **some** signal")
        A(
            f"Spearman ρ(development Sharpe, validation Sharpe) = **{rc.spearman_rho:.3f}** (p={rc.p_value:.2g}, "
            f"n={rc.n}). In-sample ranking {verdict} for out-of-sample ranking — the central overfitting check.\n"
        )
    else:
        A("Not enough paired data to compute rank correlation.\n")

    A("## Cross-symbol generalization\n")
    if best and len(symbols) > 1:
        c = best["config"]
        other = [s for s in symbols if s != c.get("symbol")]
        A(f"The best **{c.get('symbol')}** recipe applied unchanged to the other symbol(s):\n")
        A("| Symbol | Dev Sharpe | Val Sharpe | Holdout Sharpe | Val net return |")
        A("|---|---|---|---|---|")
        for sym in [c.get("symbol")] + other:
            twin = next((r for r in results if r["config"].get("symbol") == sym
                         and all(r["config"].get(a) == c.get(a) for a in axis_names)), None)
            if twin:
                A(f"| {sym} | {_fmt(_m(twin,'development_sharpe'))} | {_fmt(_m(twin,'validation_sharpe'))} "
                  f"| {_fmt(_m(twin,'holdout_sharpe'))} | {_fmt(_m(twin,'validation_net_return_pct'), pct=True)} |")
        A("")
    else:
        A("Single-symbol run — cross-symbol generalization not applicable.\n")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines))

    atomic_write_json(
        out_json,
        {
            "experiment_id": experiment_id, "symbols": symbols, "axes": {k: [str(x) for x in v] for k, v in axes.items()},
            "n_variants": len(results), "n_eligible": len(eligible),
            "min_trades_per_year": min_trades_per_year, "n_survivors_all_splits": len(survivors),
            "best": best["config"] if best else None,
            "best_exit_lookback": best.get("exit_lookback") if best else None,
            "best_metrics": best["metrics"] if best else None,
            "leaderboard": [
                {"config": r["config"], "exit_lookback": r.get("exit_lookback"),
                 "metrics": {k2: _m(r, k2) for k2 in (
                     "development_sharpe", "validation_sharpe", "holdout_sharpe",
                     "validation_net_return_pct", "development_net_return_pct", "holdout_net_return_pct",
                     "development_trades_per_year")}}
                for r in ranked[:50]
            ],
            "axis_importance": axis_importance, "enrichment": enrichment_out,
            "rank_stability": {"spearman_rho": rc.spearman_rho, "p_value": rc.p_value, "n": rc.n} if rc else None,
        },
    )
    typer.echo(f"Wrote {out_md} and {out_json}  (variants={len(results)}, eligible={len(eligible)}, survivors={len(survivors)})")


if __name__ == "__main__":
    app()
