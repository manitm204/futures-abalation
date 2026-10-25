"""Build canonical clean 1-minute bars for Databento continuous futures.

Reads the combined Databento parquet (test-dabento/futures_ohlcv_1m.parquet),
back-adjusts each root across rolls and flags the NYSE regular session (see
src/data/futures.py), then writes data/clean/symbol=<ROOT>/timeframe=1min/
year=YYYY/month=MM/part-0.parquet plus data/metadata/manifest_<ROOT>_1min.json.

Usage:
  PYTHONPATH=. python scripts/build_futures_data.py --symbols ES,NQ
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import typer

from src.data.calendars import TradingCalendar
from src.data.futures import (ADJUSTMENT_STATUS, back_adjust, contract_spec, coverage, load_databento_symbol,
                               session_spec, to_clean, illiquid_sessions, drop_sessions)
from src.utils.serialization import atomic_write_json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = PROJECT_ROOT.parent / "test-dabento" / "futures_ohlcv_1m.parquet"
app = typer.Typer(add_completion=False)


@app.command()
def main(
    symbols: str = typer.Option("ES,NQ", help="Comma-separated roots, e.g. ES,NQ,CL"),
    source: Path = typer.Option(DEFAULT_SOURCE, exists=True),
    clean_root: Path = typer.Option(PROJECT_ROOT / "data" / "clean"),
    metadata_root: Path = typer.Option(PROJECT_ROOT / "data" / "metadata"),
    min_volume_frac: float = typer.Option(0.05, help="Drop day sessions with volume below this x the trailing "
                                          "20-session median (stale expiring-contract days); 0 disables"),
) -> None:
    cal = TradingCalendar()
    src_sha = hashlib.sha256(f"{source.resolve()}|{source.stat().st_size}|{source.stat().st_mtime_ns}".encode()).hexdigest()
    for sym in [s.strip() for s in symbols.split(",") if s.strip()]:
        spec = contract_spec(sym)
        raw = load_databento_symbol(source, sym)
        adj, rolls = back_adjust(raw)
        clean = to_clean(adj, sym, calendar=cal)
        illiquid = illiquid_sessions(clean, min_volume_frac=min_volume_frac) if min_volume_frac > 0 else None
        dropped = [] if illiquid is None else illiquid["session_date_ny"].to_list()
        clean = drop_sessions(clean, dropped)
        base = clean_root / f"symbol={sym}" / "timeframe=1min"
        if base.exists():
            for p in base.rglob("*.parquet"):
                p.unlink()
        clean = clean.with_columns(clean["session_date_ny"].dt.year().alias("_y"),
                                   clean["session_date_ny"].dt.month().alias("_m"))
        n_files = 0
        for (y, m), part in clean.group_by(["_y", "_m"], maintain_order=True):
            out = base / f"year={y:04d}" / f"month={m:02d}"
            out.mkdir(parents=True, exist_ok=True)
            part.drop("_y", "_m").write_parquet(out / "part-0.parquet")
            n_files += 1
        cov = coverage(clean)
        manifest = {
            "provider": "databento", "dataset": "GLBX.MDP3", "schema": "ohlcv-1m", "stype_in": "continuous",
            "source_symbol": f"{sym}.v.0", "symbol": sym, "interval": "1min",
            "source_file": str(source.resolve()), "source_fingerprint": src_sha,
            "cleaning_version": clean["cleaning_version"][0], "schema_version": clean["schema_version"][0],
            "download_timestamp": datetime.fromtimestamp(source.stat().st_mtime, timezone.utc).isoformat(),
            "adjustment_status": ADJUSTMENT_STATUS,
            "contract_multiplier": spec.multiplier, "tick_size": spec.tick_size,
            "session_definition": f"{session_spec(sym).label} (trading days per NYSE calendar, ending no later than the NYSE close)",
            "illiquid_session_rule": f"session volume < {min_volume_frac} x median of previous 20 sessions -> not traded",
            "illiquid_sessions_dropped": [str(d) for d in dropped],
            "n_rolls": len(rolls), "rolls": rolls, "n_partitions": n_files, **cov,
        }
        atomic_write_json(metadata_root / f"manifest_{sym}_1min.json", manifest)
        typer.echo(f"{sym}: {cov['row_count']:,} rows ({cov['rth_rows']:,} RTH, {cov['rth_sessions']} sessions, "
                   f"{cov['rth_sessions_under_300_bars']} short), {len(rolls)} rolls, {len(dropped)} illiquid sessions dropped, "
                   f"{cov['actual_coverage_start']}..{cov['actual_coverage_end']}")


if __name__ == "__main__":
    app()
