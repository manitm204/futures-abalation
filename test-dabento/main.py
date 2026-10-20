import os
from pathlib import Path

import databento as db
from dotenv import load_dotenv

# Load .env from the same folder as this script.
load_dotenv(Path(__file__).resolve().parent / ".env")

api_key = os.getenv("DATABENTO_API_KEY")
if not api_key:
    raise ValueError("DATABENTO_API_KEY was not found in .env")
# Reads your DATABENTO_API_KEY environment variable.
client = db.Historical()

request = {
    "dataset": "GLBX.MDP3",
    "schema": "ohlcv-1m",
    "stype_in": "continuous",
    "symbols": [
        "NQ.v.0", "ES.v.0", "YM.v.0", "RTY.v.0",
        "CL.v.0", "GC.v.0", "6E.v.0", "6J.v.0",
        "ZN.v.0", "ZB.v.0",
    ],
    "start": "2018-01-01",
    "end": "2026-10-19",  # Exclusive; through October 18 UTC.
}

out_dir = Path(__file__).resolve().parent
dbn_path = out_dir / "futures_ohlcv_1m.dbn.zst"
parquet_path = out_dir / "futures_ohlcv_1m.parquet"

# Run this first to see the estimated download charge.
cost = client.metadata.get_cost(**request)
print(f"Estimated cost: ${cost:.2f}")

if input("Proceed with billable download? [y/N] ").strip().lower() != "y":
    raise SystemExit("Aborted; nothing downloaded.")

# This call downloads billable data and streams it straight to disk,
# so the raw file survives even if the conversion below fails.
print(f"Downloading to {dbn_path} (this can take a while; no progress bar)...")
data = client.timeseries.get_range(**request, path=dbn_path)

df = data.to_df()
df.to_parquet(parquet_path)
print(f"Saved {len(df):,} rows to {parquet_path}")
