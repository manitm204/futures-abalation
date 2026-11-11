"""Phase-gated bar loading with an append-only access ledger.

Every read of clean bars for the funnel goes through `load_phase_bars`, which
  * reads only the year partitions that can contain the phase's dates (holdout
    partitions are never even opened for development / validation),
  * filters rows to `session_date_ny <= phase end` and asserts it,
  * refuses the holdout phase unless given a `HoldoutAuthorization`, which only
    `authorize_holdout_access` creates -- and that requires an explicit
    confirmation flag and a frozen selection-manifest hash,
  * appends a line to the access ledger (phase, endpoint, rows, command) so the
    full history of who touched which slice is preserved.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Literal

import polars as pl

from src.experiments.funnel_config import PROJECT_ROOT, FunnelConfig

Phase = Literal["development", "validation", "holdout"]
DEFAULT_LEDGER = PROJECT_ROOT / "runs" / "funnel" / "data_access_ledger.jsonl"


class HoldoutAccessError(PermissionError):
    """Raised on any attempt to read holdout bars without explicit authorization."""


_AUTH_TOKEN = object()  # module-private: authorizations can't be forged by construction


@dataclass(frozen=True)
class HoldoutAuthorization:
    manifest_sha256: str
    command: str
    granted_at: str
    _token: object

    def __post_init__(self) -> None:
        if self._token is not _AUTH_TOKEN:
            raise HoldoutAccessError("HoldoutAuthorization must come from authorize_holdout_access()")


def authorize_holdout_access(*, manifest_sha256: str, confirm: bool, command: str) -> HoldoutAuthorization:
    if not confirm:
        raise HoldoutAccessError(
            "Holdout access requires explicit confirmation (final-test --confirm-holdout-access)."
        )
    if not manifest_sha256:
        raise HoldoutAccessError("Holdout access requires a frozen selection-manifest hash.")
    return HoldoutAuthorization(manifest_sha256, command, datetime.now(timezone.utc).isoformat(), _AUTH_TOKEN)


def phase_end(cfg: FunnelConfig, phase: Phase) -> date | None:
    return getattr(cfg.data, phase).end


def _partition_year(p: Path) -> int | None:
    for part in p.parts:
        if part.startswith("year="):
            return int(part.split("=", 1)[1])
    return None


def append_ledger(entry: dict, ledger_path: Path = DEFAULT_LEDGER) -> None:
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with open(ledger_path, "a") as f:
        f.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), **entry}, default=str) + "\n")


def read_ledger(ledger_path: Path = DEFAULT_LEDGER) -> list[dict]:
    if not ledger_path.exists():
        return []
    return [json.loads(line) for line in ledger_path.read_text().splitlines() if line.strip()]


def load_phase_bars(
    cfg: FunnelConfig,
    symbol: str,
    phase: Phase,
    *,
    command: str,
    experiment_id: str,
    clean_root: Path | None = None,
    authorization: HoldoutAuthorization | None = None,
    ledger_path: Path = DEFAULT_LEDGER,
) -> tuple[pl.DataFrame, dict]:
    """1-minute clean bars for `symbol` from the start of data through the END of
    `phase` (continuous history, so indicators warm up and positions carry over
    naturally). Returns (bars, access_info)."""
    if phase == "holdout" and not isinstance(authorization, HoldoutAuthorization):
        raise HoldoutAccessError(
            "Holdout bars can only be loaded by the explicit final-test command with a frozen manifest."
        )
    root = Path(clean_root or cfg.data.clean_root)
    if not root.is_absolute():
        root = PROJECT_ROOT / root
    end = phase_end(cfg, phase)
    base = root / f"symbol={symbol}" / "timeframe=1min"
    files = sorted(base.rglob("*.parquet"))
    if end is not None:
        files = [f for f in files if (y := _partition_year(f)) is None or y <= end.year]
    if not files:
        raise FileNotFoundError(f"No clean 1min partitions for {symbol} under {base}")
    df = pl.concat([pl.read_parquet(f) for f in files]).sort("bar_open_ts")
    if end is not None:
        df = df.filter(pl.col("session_date_ny") <= end)
    max_date = df["session_date_ny"].max()
    if end is not None and max_date is not None and max_date > end:  # defensive; filter above guarantees it
        raise HoldoutAccessError(f"Loaded data past phase end {end}: {max_date}")

    h = hashlib.sha256()
    for f in files:
        h.update(f.relative_to(root).as_posix().encode())
        h.update(str(f.stat().st_size).encode())
    info = {
        "symbol": symbol, "phase": phase, "phase_end": str(end) if end else None,
        "actual_last_session": str(max_date), "first_session": str(df["session_date_ny"].min()),
        "rows": df.height, "n_partitions": len(files), "partition_fingerprint": h.hexdigest()[:16],
        "command": command, "experiment_id": experiment_id,
        "manifest_sha256": authorization.manifest_sha256 if authorization else None,
    }
    append_ledger(info, ledger_path)
    return df, info
