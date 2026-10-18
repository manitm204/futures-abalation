"""Thin, verified client for the FMP `stable` API.

Only implements what has been empirically confirmed against a live key (see
ASSUMPTIONS.md) or documented in FMP's own published examples:

  - Intraday: GET /stable/historical-chart/{interval}?symbol=&from=&to=&apikey=
    interval in {1min, 5min, 15min}. CONFIRMED: hard-capped at exactly 3 trading
    days per request (1170 bars for 1min), silently truncated to the 3 trading
    days ending at/before `to` if a wider range is requested. Callers MUST chunk.
  - Daily EOD: GET /stable/historical-price-eod/full?symbol=&from=&to=&apikey=
  - Splits: GET /stable/splits?symbol=

Response validation: raises FmpResponseError on non-200, on a JSON object where a
list was expected (FMP returns `{"Error Message": ...}` style dicts on failure),
or on missing required fields.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date
from typing import Any, Literal

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

BASE_URL = "https://financialmodelingprep.com/stable"
IntradayInterval = Literal["1min", "5min", "15min"]

REQUIRED_INTRADAY_FIELDS = ("date", "open", "high", "low", "close", "volume")
REQUIRED_DAILY_FIELDS = ("date", "open", "high", "low", "close", "volume")

# Empirically confirmed cap (see ASSUMPTIONS.md): the 1min endpoint returns at most
# the 3 CALENDAR days ending at `to`, filtered to trading days -- NOT 3 trading days.
# A (from, to) pair whose trading days span a weekend/holiday within that 3-calendar-
# day window silently loses the earlier day(s). Chunking one trading day per request
# sidesteps this entirely and is what every verification query confirmed works
# reliably. Kept as a constant, not silently assumed inside downloader logic, so a
# future re-verification only touches this file.
MAX_TRADING_DAYS_PER_INTRADAY_REQUEST = 1


class FmpResponseError(RuntimeError):
    """Raised when FMP returns an error payload, wrong shape, or missing fields."""


class FmpRateLimitError(RuntimeError):
    """Raised on HTTP 429; caller/retry layer decides how to back off."""


@dataclass(frozen=True)
class FmpClientConfig:
    api_key: str
    base_url: str = BASE_URL
    timeout_seconds: float = 30.0
    max_retries: int = 5

    @classmethod
    def from_env(cls) -> "FmpClientConfig":
        key = os.environ.get("FMP_API_KEY")
        if not key:
            raise RuntimeError(
                "FMP_API_KEY is not set. Export it or add it to .env (see .env.example)."
            )
        return cls(api_key=key)


def _validate_list_response(payload: Any, required_fields: tuple[str, ...], *, context: str) -> list[dict]:
    if isinstance(payload, dict):
        raise FmpResponseError(f"{context}: FMP returned an error payload: {payload}")
    if not isinstance(payload, list):
        raise FmpResponseError(f"{context}: expected a JSON list, got {type(payload)}")
    for row in payload:
        missing = [f for f in required_fields if f not in row]
        if missing:
            raise FmpResponseError(f"{context}: row missing required fields {missing}: {row}")
    return payload


class FmpClient:
    def __init__(self, config: FmpClientConfig | None = None) -> None:
        self.config = config or FmpClientConfig.from_env()
        self._client = httpx.Client(base_url=self.config.base_url, timeout=self.config.timeout_seconds)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "FmpClient":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def _get(self, path: str, params: dict[str, str]) -> Any:
        @retry(
            reraise=True,
            stop=stop_after_attempt(self.config.max_retries),
            wait=wait_exponential_jitter(initial=1, max=30),
            retry=retry_if_exception_type((httpx.TransportError, FmpRateLimitError, httpx.HTTPStatusError)),
        )
        def _do_request() -> Any:
            resp = self._client.get(path, params={**params, "apikey": self.config.api_key})
            if resp.status_code == 429:
                raise FmpRateLimitError(f"429 from FMP for {path} {params}")
            if resp.status_code >= 500:
                resp.raise_for_status()
            if resp.status_code != 200:
                raise FmpResponseError(
                    f"GET {path} {params} -> HTTP {resp.status_code}: {resp.text[:500]}"
                )
            return resp.json()

        return _do_request()

    def get_intraday_chunk(
        self, symbol: str, interval: IntradayInterval, from_date: date, to_date: date
    ) -> list[dict]:
        """Fetch one chunk. Caller MUST ensure (from_date, to_date) spans at most
        MAX_TRADING_DAYS_PER_INTRADAY_REQUEST trading days, or data will be silently
        truncated by FMP (confirmed behavior)."""
        payload = self._get(
            f"/historical-chart/{interval}",
            {"symbol": symbol, "from": from_date.isoformat(), "to": to_date.isoformat()},
        )
        return _validate_list_response(
            payload, REQUIRED_INTRADAY_FIELDS, context=f"intraday {symbol} {interval} {from_date}..{to_date}"
        )

    def get_daily(self, symbol: str, from_date: date, to_date: date) -> list[dict]:
        payload = self._get(
            "/historical-price-eod/full",
            {"symbol": symbol, "from": from_date.isoformat(), "to": to_date.isoformat()},
        )
        return _validate_list_response(
            payload, REQUIRED_DAILY_FIELDS, context=f"daily {symbol} {from_date}..{to_date}"
        )

    def get_splits(self, symbol: str) -> list[dict]:
        payload = self._get("/splits", {"symbol": symbol})
        return _validate_list_response(payload, ("date", "numerator", "denominator"), context=f"splits {symbol}")
