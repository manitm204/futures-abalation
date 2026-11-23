"""Assembles the final research report (Markdown) from whatever artifacts are
available on disk: data manifests, quality reports, experiment results,
funnel outcomes, parameter enrichment tables. Sections for analyses that
haven't been run yet are rendered as explicit "not yet run" placeholders,
never silently omitted or filled with fabricated numbers.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from src.analysis.parameter_analysis import categorical_enrichment
from src.analysis.rankings import top_n


def _load_json_if_exists(path: Path) -> dict | None:
    if path.exists():
        return json.loads(path.read_text())
    return None


def _section_data_coverage(metadata_dir: Path, symbols: list[str], timeframe: str) -> str:
    lines = ["## 2. Data Coverage and Limitations\n"]
    for sym in symbols:
        manifest = _load_json_if_exists(metadata_dir / f"manifest_{sym}_{timeframe}.json")
        quality = _load_json_if_exists(metadata_dir / f"quality_{sym}_{timeframe}.json")
        lines.append(f"### {sym} ({timeframe})\n")
        if manifest is None:
            lines.append("*No manifest found -- data not yet downloaded/built for this symbol.*\n")
            continue
        lines.append(f"- Actual coverage: {manifest.get('actual_coverage_start')} to {manifest.get('actual_coverage_end')}")
        lines.append(f"- Row count: {manifest.get('row_count')}")
        lines.append(f"- Adjustment status: {manifest.get('adjustment_status')}")
        lines.append(f"- Missing sessions: {manifest.get('missing_session_count')}")
        lines.append(f"- Duplicate bars: {manifest.get('duplicate_count')}")
        if quality:
            lines.append(f"- Incomplete sessions (partial-day gaps): {len(quality.get('incomplete_session_dates', []))}")
            lines.append(f"- Invalid OHLC bars: {quality.get('invalid_ohlc_count')}")
            lines.append(f"- Large intraday gaps: {quality.get('large_gap_count')}")
        lines.append("")
    return "\n".join(lines)


def _section_assumptions(project_root: Path) -> str:
    assumptions_path = project_root / "ASSUMPTIONS.md"
    if not assumptions_path.exists():
        return "## 3-5. Timestamp/Session Conventions, Strategy Definitions, Execution Assumptions\n\n*ASSUMPTIONS.md not found.*\n"
    content = assumptions_path.read_text()
    return f"## 3-5. Timestamp/Session Conventions, Strategy Definitions, Execution Assumptions\n\nSee `ASSUMPTIONS.md` for the full, current record. Summary below.\n\n{content}\n"


def _section_search_results(results_dir: Path, experiment_id: str | None) -> str:
    lines = ["## 8-9. Development and Validation Results\n"]
    if experiment_id is None:
        lines.append("*No experiment_id specified -- search results not included.*\n")
        return "\n".join(lines)

    exp_dir = results_dir / f"experiment_id={experiment_id}"
    if not exp_dir.exists():
        lines.append(f"*No results found for experiment_id={experiment_id}.*\n")
        return "\n".join(lines)

    results = []
    for p in exp_dir.glob("*.json"):
        try:
            results.append(json.loads(p.read_text()))
        except Exception:
            continue

    n_ok = sum(1 for r in results if r.get("status") == "ok")
    n_failed = sum(1 for r in results if r.get("status") == "failed")
    lines.append(f"- Total configs run: {len(results)} ({n_ok} ok, {n_failed} failed)\n")

    if n_ok == 0:
        lines.append("*No successful configs -- cannot report rankings.*\n")
        return "\n".join(lines)

    ok_results = [r for r in results if r.get("status") == "ok"]
    top = top_n(ok_results, metric="net_pnl", n=min(10, n_ok))
    lines.append("### Top configs by net P&L (gross vs net; in-sample on the data run against -- NOT a claim of future performance)\n")
    lines.append("| config_id | n_trades | net_pnl | win_rate | profit_factor | sharpe |")
    lines.append("|---|---|---|---|---|---|")
    for r in top:
        m = r.get("metrics", {})
        lines.append(
            f"| {r['config_id']} | {m.get('n_trades')} | {m.get('net_pnl', 0):.2f} | "
            f"{m.get('win_rate', 0):.2%} | {m.get('profit_factor')} | {m.get('sharpe_ratio')} |"
        )
    lines.append("")

    for param in ("stop_type", "target_type", "fvg_entry_rule", "require_market_structure_shift"):
        rows = categorical_enrichment(ok_results, top, param=param)
        if not rows:
            continue
        lines.append(f"### Parameter enrichment: `{param}` (top {len(top)} vs full population, N={n_ok})\n")
        lines.append("| value | baseline freq | top-N freq | enrichment ratio |")
        lines.append("|---|---|---|---|")
        for row in rows:
            ratio_str = f"{row.enrichment_ratio:.2f}" if row.enrichment_ratio is not None else "n/a"
            lines.append(f"| {row.value} | {row.baseline_frequency:.2%} | {row.top_n_frequency:.2%} | {ratio_str} |")
        lines.append("")

    return "\n".join(lines)


def build_report(
    *,
    project_root: Path,
    symbols: list[str],
    timeframe: str = "1min",
    experiment_id: str | None = None,
) -> str:
    generated_at = datetime.now(timezone.utc).isoformat()
    sections = [
        "# ICT Silver Bullet Research Report\n",
        f"*Generated {generated_at}. This is a research artifact; nothing here implies profitability. "
        "See section 20 for cautious conclusions and section 17 for multiple-testing warnings.*\n",
        "## 1. Executive Summary\n\n*Fill in after reviewing sections below -- not auto-generated to avoid "
        "overstating conclusions from partial results.*\n",
        _section_data_coverage(project_root / "data" / "metadata", symbols, timeframe),
        _section_assumptions(project_root),
        "## 6. Parameter-Search Design\n\nSee `src/experiments/spaces.py` for the typed search space and "
        "`src/experiments/sampler.py` for the reproducible stratified-Sobol sampling method.\n",
        "## 7. Validation Funnel\n\nSee `src/experiments/validation.py` for stage definitions and thresholds. "
        "Funnel results for a specific experiment run are not yet included in this auto-generated section.\n",
        _section_search_results(project_root / "runs" / "results", experiment_id),
        "## 10. Final Holdout Results\n\n*Not yet run -- requires the full chronological split and a "
        "completed development/validation cycle first (see ASSUMPTIONS.md split boundaries).*\n",
        "## 11. Walk-Forward Performance\n\n*Not yet run.*\n",
        "## 12. SPY/QQQ Transfer Results\n\n*Not yet run -- requires funnel survivors from both symbols.*\n",
        "## 13. London vs NY AM vs NY PM\n\n*London has zero data coverage (see ASSUMPTIONS.md) -- only "
        "NY AM vs NY PM can be compared in this study.*\n",
        "## 14-16. Parameter Enrichment, Redundancy/Clustering, Cost/Ambiguity Sensitivity\n\n"
        "See section 8-9 above for per-run parameter enrichment. Redundancy clustering and cost sensitivity "
        "require multiple completed configs with trade-level return streams -- not yet run at scale.\n",
        "## 17. Multiple-Testing Warnings\n\n"
        "This study samples up to ~10,000 configurations. Any single config's attractive in-sample Sharpe "
        "ratio is NOT evidence of a real edge on its own -- see `src/analysis/stability.py` for the "
        "Probabilistic and Deflated Sharpe Ratio implementations, which explicitly account for (a) non-normal "
        "return distributions and (b) the number of trials run. A config must survive the full validation "
        "funnel (dev -> validation -> untouched holdout) and show a DSR meaningfully above 0.5 to be taken "
        "seriously, and even then only as an association worth further out-of-sample testing, not causal proof.\n",
        "## 18. Failure Modes and Rejected Hypotheses\n\n*To be filled in from the rejected-setups tables and "
        "funnel failure-reason breakdowns once a full run completes.*\n",
        "## 19. Reproducibility Manifest\n\n"
        f"- Symbols: {symbols}\n- Timeframe: {timeframe}\n- Experiment ID: {experiment_id or 'n/a'}\n"
        "- See runs/manifests/ for the per-experiment manifest (seed, code version, config count).\n",
        "## 20. Conclusions\n\n*Stated cautiously, after a full run: this framework determines what does and "
        "does not survive causal, out-of-sample testing. No conclusion here should be read as investment advice "
        "or as establishing profitability.*\n",
    ]
    return "\n".join(sections)
