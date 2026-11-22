"""Print a coverage/quality summary for cleaned data already on disk, and
optionally compare internally aggregated bars against FMP-native bars for a
sampled date (requires both --interval 1min and the native --compare-interval
to have been downloaded/cleaned already).

Usage:
  python scripts/validate_data.py --symbol SPY --timeframe 1min
  python scripts/validate_data.py --symbol SPY --timeframe 5min --compare-native --sample-date 2024-01-02
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import polars as pl
import typer

from src.data.aggregation import aggregate_bars
from src.data.quality import compare_native_vs_aggregated
from src.utils.logging import configure_logging, get_logger

PROJECT_ROOT = Path(__file__).resolve().parents[1]
app = typer.Typer()
logger = get_logger(__name__)


def _load_clean(clean_root: Path, symbol: str, timeframe: str) -> pl.DataFrame:
    base = clean_root / f"symbol={symbol}" / f"timeframe={timeframe}"
    if not base.exists():
        return pl.DataFrame()
    return pl.concat([pl.read_parquet(p) for p in sorted(base.rglob("*.parquet"))])


@app.command()
def main(
    symbol: str = typer.Option(...),
    timeframe: str = typer.Option("1min"),
    clean_root: Path = typer.Option(PROJECT_ROOT / "data" / "clean"),
    compare_native: bool = typer.Option(False),
    sample_date: str = typer.Option(None),
) -> None:
    configure_logging()
    df = _load_clean(clean_root, symbol, timeframe)
    if df.is_empty():
        logger.error("no_clean_data_found", symbol=symbol, timeframe=timeframe)
        raise typer.Exit(code=1)

    logger.info(
        "coverage_summary",
        symbol=symbol, timeframe=timeframe, rows=df.height,
        first_date=str(df["session_date_ny"].min()), last_date=str(df["session_date_ny"].max()),
        distinct_sessions=df["session_date_ny"].n_unique(),
    )

    if compare_native:
        native = df
        df_1min = _load_clean(clean_root, symbol, "1min")
        if sample_date:
            d = datetime.strptime(sample_date, "%Y-%m-%d").date()
            df_1min = df_1min.filter(pl.col("session_date_ny") == d)
            native = native.filter(pl.col("session_date_ny") == d)
        aggregated = aggregate_bars(df_1min, timeframe=timeframe)
        result = compare_native_vs_aggregated(native, aggregated)
        logger.info("native_vs_aggregated", **result)


if __name__ == "__main__":
    app()
