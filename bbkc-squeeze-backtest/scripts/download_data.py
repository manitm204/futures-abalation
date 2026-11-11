"""Download raw FMP intraday/daily data for one or more symbols.

Usage:
  python scripts/download_data.py --symbol SPY --interval 1min \
      --start 2018-01-01 --end 2026-08-18

Writes immutable raw JSON chunks under data/raw/. Resumable: re-running with the
same arguments skips already-downloaded chunks. Use --force to re-download.
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import typer
from dotenv import load_dotenv

from src.data.calendars import TradingCalendar
from src.data.downloader import download_daily, download_intraday
from src.data.fmp_client import FmpClient
from src.utils.logging import configure_logging, get_logger

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

app = typer.Typer()
logger = get_logger(__name__)


@app.command()
def main(
    symbol: str = typer.Option(..., help="Ticker, e.g. SPY"),
    interval: str = typer.Option("1min", help="1min, 5min, 15min, or 1d"),
    start: str = typer.Option(..., help="YYYY-MM-DD"),
    end: str = typer.Option(..., help="YYYY-MM-DD"),
    raw_root: Path = typer.Option(PROJECT_ROOT / "data" / "raw"),
    force: bool = typer.Option(False, help="Re-download even if raw files already exist"),
    request_delay_seconds: float = typer.Option(0.25),
) -> None:
    configure_logging()
    start_d = datetime.strptime(start, "%Y-%m-%d").date()
    end_d = datetime.strptime(end, "%Y-%m-%d").date()
    calendar = TradingCalendar()

    with FmpClient() as client:
        if interval == "1d":
            report = download_daily(symbol, start_d, end_d, client=client, raw_root=raw_root, force=force)
        else:
            report = download_intraday(
                symbol, interval, start_d, end_d,  # type: ignore[arg-type]
                client=client, calendar=calendar, raw_root=raw_root,
                request_delay_seconds=request_delay_seconds, force=force,
            )

    logger.info(
        "download_complete",
        symbol=symbol, interval=interval,
        chunks=len(report.chunks), failed=len(report.failed_chunks),
        total_rows=report.total_rows,
        coverage_start=str(report.actual_coverage_start),
        coverage_end=str(report.actual_coverage_end),
    )
    if report.failed_chunks:
        logger.error("some_chunks_failed", failed=report.failed_chunks)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
