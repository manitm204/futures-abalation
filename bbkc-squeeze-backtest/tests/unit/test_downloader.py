import json
from datetime import date
from pathlib import Path

from src.data.calendars import TradingCalendar
from src.data.downloader import download_intraday

CAL = TradingCalendar()


class FakeFmpClient:
    """Test double: records calls, returns deterministic synthetic bars, never hits the network."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str, date, date]] = []

    def get_intraday_chunk(self, symbol: str, interval: str, from_date: date, to_date: date) -> list[dict]:
        self.calls.append((symbol, interval, from_date, to_date))
        days = CAL.trading_days(from_date, to_date)
        return [
            {
                "date": f"{d.isoformat()} 09:30:00",
                "open": 1.0, "high": 1.1, "low": 0.9, "close": 1.05, "volume": 100,
            }
            for d in days
        ]


def test_download_intraday_chunks_respect_three_day_cap(tmp_path: Path) -> None:
    client = FakeFmpClient()
    report = download_intraday(
        "SPY", "1min", date(2024, 1, 2), date(2024, 1, 12),
        client=client, calendar=CAL, raw_root=tmp_path, request_delay_seconds=0,
    )
    for _, _, from_d, to_d in client.calls:
        assert len(CAL.trading_days(from_d, to_d)) <= 3
    assert report.total_rows > 0
    assert len(report.failed_chunks) == 0


def test_download_intraday_writes_immutable_raw_files(tmp_path: Path) -> None:
    client = FakeFmpClient()
    report = download_intraday(
        "SPY", "1min", date(2024, 1, 2), date(2024, 1, 4),
        client=client, calendar=CAL, raw_root=tmp_path, request_delay_seconds=0,
    )
    assert len(report.chunks) == 3  # one trading day per chunk (2024-01-02/03/04)
    chunk = report.chunks[0]
    assert chunk.path.exists()
    data = json.loads(chunk.path.read_text())
    assert len(data) == chunk.row_count


def test_download_intraday_resume_skips_existing_chunks(tmp_path: Path) -> None:
    client1 = FakeFmpClient()
    download_intraday(
        "SPY", "1min", date(2024, 1, 2), date(2024, 1, 4),
        client=client1, calendar=CAL, raw_root=tmp_path, request_delay_seconds=0,
    )
    assert len(client1.calls) == 3

    client2 = FakeFmpClient()
    report2 = download_intraday(
        "SPY", "1min", date(2024, 1, 2), date(2024, 1, 4),
        client=client2, calendar=CAL, raw_root=tmp_path, request_delay_seconds=0,
    )
    assert len(client2.calls) == 0  # nothing re-downloaded
    assert all(c.skipped_existing for c in report2.chunks)


def test_download_intraday_force_redownloads(tmp_path: Path) -> None:
    client1 = FakeFmpClient()
    download_intraday(
        "SPY", "1min", date(2024, 1, 2), date(2024, 1, 4),
        client=client1, calendar=CAL, raw_root=tmp_path, request_delay_seconds=0,
    )
    client2 = FakeFmpClient()
    download_intraday(
        "SPY", "1min", date(2024, 1, 2), date(2024, 1, 4),
        client=client2, calendar=CAL, raw_root=tmp_path, request_delay_seconds=0, force=True,
    )
    assert len(client2.calls) == 3


def test_download_intraday_catches_per_chunk_failure(tmp_path: Path) -> None:
    class FlakyClient(FakeFmpClient):
        def get_intraday_chunk(self, symbol: str, interval: str, from_date: date, to_date: date) -> list[dict]:
            if from_date == date(2024, 1, 2):
                raise RuntimeError("simulated failure")
            return super().get_intraday_chunk(symbol, interval, from_date, to_date)

    client = FlakyClient()
    report = download_intraday(
        "SPY", "1min", date(2024, 1, 2), date(2024, 1, 12),
        client=client, calendar=CAL, raw_root=tmp_path, request_delay_seconds=0,
    )
    assert len(report.failed_chunks) == 1
    assert len(report.chunks) > 0  # other chunks still succeeded
