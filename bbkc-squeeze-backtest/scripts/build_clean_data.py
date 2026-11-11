"""Normalize raw FMP JSON chunks into canonical cleaned Parquet, partitioned by
symbol/timeframe/year/month. Also builds 5min/15min/1h bars aggregated from 1min
if --also-aggregate is passed. Writes a manifest and quality report.

Usage:
  python scripts/build_clean_data.py --symbol SPY --interval 1min \
      --start 2018-01-01 --end 2026-08-18
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import polars as pl
import typer

from src.data.aggregation import aggregate_bars
from src.data.calendars import TradingCalendar
from src.data.downloader import DownloadReport
from src.data.manifest import build_manifest, write_manifest
from src.data.normalization import normalize_intraday_rows
from src.data.quality import check_intraday_quality
from src.utils.logging import configure_logging, get_logger

PROJECT_ROOT = Path(__file__).resolve().parents[1]
app = typer.Typer()
logger = get_logger(__name__)


def _load_raw_chunks(raw_root: Path, symbol: str, interval: str) -> list[dict]:
    base = raw_root / f"provider=fmp" / f"symbol={symbol}" / f"interval={interval}"
    rows: list[dict] = []
    for path in sorted(base.rglob("chunk_*.json")):
        rows.extend(json.loads(path.read_text()))
    return rows


def _write_clean_parquet(df: pl.DataFrame, clean_root: Path, symbol: str, timeframe: str) -> list[Path]:
    if df.is_empty():
        return []
    written: list[Path] = []
    df = df.with_columns(
        pl.col("session_date_ny").dt.year().alias("_y"),
        pl.col("session_date_ny").dt.month().alias("_m"),
    )
    for (year, month), part in df.group_by(["_y", "_m"], maintain_order=True):
        out_dir = clean_root / f"symbol={symbol}" / f"timeframe={timeframe}" / f"year={year:04d}" / f"month={month:02d}"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "part-0.parquet"
        part.drop(["_y", "_m"]).write_parquet(out_path)
        written.append(out_path)
    return written


@app.command()
def main(
    symbol: str = typer.Option(...),
    interval: str = typer.Option("1min"),
    start: str = typer.Option(...),
    end: str = typer.Option(...),
    raw_root: Path = typer.Option(PROJECT_ROOT / "data" / "raw"),
    clean_root: Path = typer.Option(PROJECT_ROOT / "data" / "clean"),
    metadata_root: Path = typer.Option(PROJECT_ROOT / "data" / "metadata"),
    also_aggregate: bool = typer.Option(True, help="Also build 5min/15min/1h from 1min"),
) -> None:
    configure_logging()
    start_d = datetime.strptime(start, "%Y-%m-%d").date()
    end_d = datetime.strptime(end, "%Y-%m-%d").date()
    calendar = TradingCalendar()

    raw_rows = _load_raw_chunks(raw_root, symbol, interval)
    logger.info("raw_rows_loaded", symbol=symbol, interval=interval, count=len(raw_rows))

    clean = normalize_intraday_rows(
        raw_rows, symbol=symbol, timeframe=interval, source="fmp_native", calendar=calendar
    )
    written = _write_clean_parquet(clean, clean_root, symbol, interval)
    logger.info("clean_parquet_written", symbol=symbol, timeframe=interval, files=len(written))

    quality = check_intraday_quality(
        clean, symbol=symbol, timeframe=interval, calendar=calendar,
        expected_start=start_d, expected_end=end_d,
    )
    logger.info(
        "quality_report", symbol=symbol, timeframe=interval,
        row_count=quality.row_count, duplicates=quality.duplicate_bar_open_ts,
        invalid_ohlc=quality.invalid_ohlc_count, missing_sessions=len(quality.missing_session_dates),
        large_gaps=quality.large_gap_count,
    )

    metadata_root.mkdir(parents=True, exist_ok=True)
    metadata_root.joinpath(f"quality_{symbol}_{interval}.json").write_text(
        json.dumps(
            {
                "symbol": quality.symbol,
                "timeframe": quality.timeframe,
                "row_count": quality.row_count,
                "duplicate_bar_open_ts": quality.duplicate_bar_open_ts,
                "unsorted": quality.unsorted,
                "invalid_ohlc_count": quality.invalid_ohlc_count,
                "negative_price_count": quality.negative_price_count,
                "negative_volume_count": quality.negative_volume_count,
                "missing_session_dates": [d.isoformat() for d in quality.missing_session_dates],
                "incomplete_session_dates": [
                    {"date": d.isoformat(), "actual_bars": a, "expected_bars": e}
                    for d, a, e in quality.incomplete_session_dates
                ],
                "unexpected_bars_outside_session": quality.unexpected_bars_outside_session,
                "large_gap_count": quality.large_gap_count,
                "zero_volume_bar_count": quality.zero_volume_bar_count,
            },
            indent=2,
        )
    )

    # Build a DownloadReport-shaped summary purely from what's on disk, for the manifest.
    chunk_paths = sorted((raw_root / "provider=fmp" / f"symbol={symbol}" / f"interval={interval}").rglob("chunk_*.json"))
    from src.data.downloader import ChunkResult
    from src.utils.hashing import file_checksum
    from datetime import timezone

    fake_report = DownloadReport(symbol=symbol, interval=interval, requested_start=start_d, requested_end=end_d)
    for p in chunk_paths:
        fake_report.chunks.append(
            ChunkResult(
                symbol=symbol, interval=interval, from_date=start_d, to_date=end_d, path=p,
                row_count=len(json.loads(p.read_text())), checksum=file_checksum(p),
                downloaded_at=datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc),
                skipped_existing=True,
            )
        )
    manifest = build_manifest(
        fake_report, quality,
        endpoint=f"/historical-chart/{interval}" if interval != "1d" else "/historical-price-eod/full",
    )
    manifest.actual_coverage_start = clean["session_date_ny"].min() if not clean.is_empty() else None
    manifest.actual_coverage_end = clean["session_date_ny"].max() if not clean.is_empty() else None
    manifest_path = write_manifest(manifest, metadata_root)
    logger.info("manifest_written", path=str(manifest_path))

    if also_aggregate and interval == "1min" and not clean.is_empty():
        for tf in ("5min", "15min", "1h"):
            agg = aggregate_bars(clean, timeframe=tf)
            agg_written = _write_clean_parquet(agg.drop(["n_source_bars", "is_partial_bar"]), clean_root, symbol, tf)
            logger.info("aggregated_written", symbol=symbol, timeframe=tf, files=len(agg_written), rows=agg.height)


if __name__ == "__main__":
    app()
