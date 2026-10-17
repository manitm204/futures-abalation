"""Assemble the Markdown research report from available manifests/results.

Usage:
  python scripts/build_report.py --symbol SPY --symbol QQQ --experiment-id smoke3
"""

from __future__ import annotations

from pathlib import Path

import typer

from src.analysis.reports import build_report

PROJECT_ROOT = Path(__file__).resolve().parents[1]
app = typer.Typer()


@app.command()
def main(
    symbol: list[str] = typer.Option(..., help="Repeatable, e.g. --symbol SPY --symbol QQQ"),
    timeframe: str = typer.Option("1min"),
    experiment_id: str = typer.Option(None),
    output: Path = typer.Option(PROJECT_ROOT / "runs" / "reports" / "report.md"),
) -> None:
    report = build_report(project_root=PROJECT_ROOT, symbols=symbol, timeframe=timeframe, experiment_id=experiment_id)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report)
    typer.echo(f"Report written to {output}")


if __name__ == "__main__":
    app()
