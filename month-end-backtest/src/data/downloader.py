"""Resumable, chunked downloader for FMP intraday/daily data.

Design driven by the confirmed FMP 3-trading-day cap on intraday requests
(see ASSUMPTIONS.md, src/data/fmp_client.py): the full requested range is split
into trading-day chunks via TradingCalendar, and each chunk is fetched and
written to its own immutable raw file. Already-downloaded chunk files are never
overwritten (raw data immutability) and are skipped on resume.

Raw storage layout (partitioned by the chunk's first trading day):
  data/raw/provider=fmp/symbol=SPY/interval=1min/year=2024/month=01/chunk_2024-01-02_2024-01-04.json
"""

from __future__ import annotations

import time as _time
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

from src.data.calendars import TradingCalendar
from src.data.fmp_client import (
    MAX_TRADING_DAYS_PER_INTRADAY_REQUEST,
    FmpClient,
    IntradayInterval,
)
from src.utils.hashing import file_checksum
from src.utils.logging import get_logger
from src.utils.serialization import atomic_write_json, raw_file_exists_and_immutable

logger = get_logger(__name__)


@dataclass
class ChunkResult:
    symbol: str
    interval: str
    from_date: date
    to_date: date
    path: Path
    row_count: int
    checksum: str
    downloaded_at: datetime
    skipped_existing: bool


@dataclass
class DownloadReport:
    symbol: str
    interval: str
    requested_start: date
    requested_end: date
    chunks: list[ChunkResult] = field(default_factory=list)
    failed_chunks: list[tuple[date, date, str]] = field(default_factory=list)

    @property
    def actual_coverage_start(self) -> date | None:
        dates = [c.from_date for c in self.chunks if c.row_count > 0]
        return min(dates) if dates else None

    @property
    def actual_coverage_end(self) -> date | None:
        dates = [c.to_date for c in self.chunks if c.row_count > 0]
        return max(dates) if dates else None

    @property
    def total_rows(self) -> int:
        return sum(c.row_count for c in self.chunks)


def _raw_chunk_path(raw_root: Path, symbol: str, interval: str, from_date: date, to_date: date) -> Path:
    return (
        raw_root
        / f"provider=fmp"
        / f"symbol={symbol}"
        / f"interval={interval}"
        / f"year={from_date.year:04d}"
        / f"month={from_date.month:02d}"
        / f"chunk_{from_date.isoformat()}_{to_date.isoformat()}.json"
    )


def download_intraday(
    symbol: str,
    interval: IntradayInterval,
    start: date,
    end: date,
    *,
    client: FmpClient,
    calendar: TradingCalendar,
    raw_root: Path,
    request_delay_seconds: float = 0.25,
    force: bool = False,
) -> DownloadReport:
    """Download `symbol`'s `interval` bars for [start, end] inclusive, chunked to
    respect FMP's confirmed per-request trading-day cap, and resumable: chunks whose
    raw file already exists are skipped unless `force=True`.
    """
    report = DownloadReport(symbol=symbol, interval=interval, requested_start=start, requested_end=end)
    chunks = calendar.chunk_trading_days(start, end, chunk_size=MAX_TRADING_DAYS_PER_INTRADAY_REQUEST)

    for from_date, to_date in chunks:
        path = _raw_chunk_path(raw_root, symbol, interval, from_date, to_date)

        if not force and raw_file_exists_and_immutable(path):
            checksum = file_checksum(path)
            import json

            row_count = len(json.loads(path.read_text()))
            report.chunks.append(
                ChunkResult(
                    symbol=symbol,
                    interval=interval,
                    from_date=from_date,
                    to_date=to_date,
                    path=path,
                    row_count=row_count,
                    checksum=checksum,
                    downloaded_at=datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc),
                    skipped_existing=True,
                )
            )
            continue

        try:
            rows = client.get_intraday_chunk(symbol, interval, from_date, to_date)
        except Exception as exc:  # noqa: BLE001 - intentionally catch-all per config, isolate failures
            logger.error(
                "chunk_download_failed", symbol=symbol, interval=interval,
                from_date=str(from_date), to_date=str(to_date), error=str(exc),
            )
            report.failed_chunks.append((from_date, to_date, str(exc)))
            continue

        atomic_write_json(path, rows)
        checksum = file_checksum(path)
        report.chunks.append(
            ChunkResult(
                symbol=symbol,
                interval=interval,
                from_date=from_date,
                to_date=to_date,
                path=path,
                row_count=len(rows),
                checksum=checksum,
                downloaded_at=datetime.now(timezone.utc),
                skipped_existing=False,
            )
        )
        logger.info(
            "chunk_downloaded", symbol=symbol, interval=interval,
            from_date=str(from_date), to_date=str(to_date), rows=len(rows),
        )
        if request_delay_seconds > 0:
            _time.sleep(request_delay_seconds)

    return report


def download_daily(
    symbol: str,
    start: date,
    end: date,
    *,
    client: FmpClient,
    raw_root: Path,
    force: bool = False,
) -> DownloadReport:
    """Daily EOD has no confirmed pagination cap issue in the range tested, but is
    still stored as a single immutable chunk file for consistency with intraday."""
    report = DownloadReport(symbol=symbol, interval="1d", requested_start=start, requested_end=end)
    path = _raw_chunk_path(raw_root, symbol, "1d", start, end)

    if not force and raw_file_exists_and_immutable(path):
        checksum = file_checksum(path)
        import json

        row_count = len(json.loads(path.read_text()))
        report.chunks.append(
            ChunkResult(
                symbol=symbol, interval="1d", from_date=start, to_date=end, path=path,
                row_count=row_count, checksum=checksum,
                downloaded_at=datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc),
                skipped_existing=True,
            )
        )
        return report

    try:
        rows = client.get_daily(symbol, start, end)
    except Exception as exc:  # noqa: BLE001
        logger.error("daily_download_failed", symbol=symbol, error=str(exc))
        report.failed_chunks.append((start, end, str(exc)))
        return report

    atomic_write_json(path, rows)
    checksum = file_checksum(path)
    report.chunks.append(
        ChunkResult(
            symbol=symbol, interval="1d", from_date=start, to_date=end, path=path,
            row_count=len(rows), checksum=checksum, downloaded_at=datetime.now(timezone.utc),
            skipped_existing=False,
        )
    )
    return report
