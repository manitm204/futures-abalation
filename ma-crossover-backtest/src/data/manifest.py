"""Manifest records for downloaded/cleaned data, per the project's reproducibility contract."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

from src.data.downloader import DownloadReport
from src.data.quality import QualityReport
from src.data.schemas import CLEANING_VERSION, SCHEMA_VERSION
from src.utils.serialization import atomic_write_json


@dataclass
class DataManifest:
    provider: str
    endpoint: str
    symbol: str
    interval: str
    requested_start: date
    requested_end: date
    actual_coverage_start: date | None
    actual_coverage_end: date | None
    download_timestamp: datetime
    raw_timezone_interpretation: str
    adjustment_status: str
    row_count: int
    missing_session_count: int
    duplicate_count: int
    file_checksums: dict[str, str]
    schema_version: str
    cleaning_version: str
    failed_chunk_count: int

    def to_dict(self) -> dict:
        d = asdict(self)
        d["requested_start"] = self.requested_start.isoformat()
        d["requested_end"] = self.requested_end.isoformat()
        d["actual_coverage_start"] = self.actual_coverage_start.isoformat() if self.actual_coverage_start else None
        d["actual_coverage_end"] = self.actual_coverage_end.isoformat() if self.actual_coverage_end else None
        d["download_timestamp"] = self.download_timestamp.isoformat()
        return d


def build_manifest(
    download_report: DownloadReport,
    quality_report: QualityReport,
    *,
    provider: str = "fmp",
    endpoint: str,
    raw_timezone_interpretation: str = "America/New_York (naive, IANA-localized)",
    adjustment_status: str = "split_adjusted",
) -> DataManifest:
    return DataManifest(
        provider=provider,
        endpoint=endpoint,
        symbol=download_report.symbol,
        interval=download_report.interval,
        requested_start=download_report.requested_start,
        requested_end=download_report.requested_end,
        actual_coverage_start=download_report.actual_coverage_start,
        actual_coverage_end=download_report.actual_coverage_end,
        download_timestamp=datetime.now(timezone.utc),
        raw_timezone_interpretation=raw_timezone_interpretation,
        adjustment_status=adjustment_status,
        row_count=quality_report.row_count,
        missing_session_count=len(quality_report.missing_session_dates),
        duplicate_count=quality_report.duplicate_bar_open_ts,
        file_checksums={str(c.path): c.checksum for c in download_report.chunks},
        schema_version=SCHEMA_VERSION,
        cleaning_version=CLEANING_VERSION,
        failed_chunk_count=len(download_report.failed_chunks),
    )


def write_manifest(manifest: DataManifest, metadata_root: Path) -> Path:
    path = metadata_root / f"manifest_{manifest.symbol}_{manifest.interval}.json"
    atomic_write_json(path, manifest.to_dict())
    return path
