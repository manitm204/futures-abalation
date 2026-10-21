"""Rolling 15m return correlation across the 10 futures markets.

Builds correlation_matrix.html (self-contained, data inlined) next to this script.

    python correlation.py

Each snapshot is the Pearson correlation of 15m log returns over the trailing
N CME sessions, taken at the last session of every week. Returns that span a
continuous-contract roll are dropped, since they are the roll gap and not a move.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
PARQUET = HERE / "futures_ohlcv_1m.parquet"
TEMPLATE = HERE / "correlation_template.html"
OUT = HERE / "correlation_matrix.html"

ORDER = ["ES", "NQ", "YM", "RTY", "CL", "GC", "6E", "6J", "ZN", "ZB"]
BAR = "15min"
WINDOWS = [20, 60, 120]  # trading sessions: ~1 month, ~1 quarter, ~half a year
MIN_BARS_PER_SESSION = 30  # a pair needs this many joint bars per session in the window


def load_returns(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path, columns=["close", "instrument_id", "symbol"])
    df["symbol"] = df["symbol"].str.replace(".v.0", "", regex=False)
    close = df.pivot_table(index=df.index, columns="symbol", values="close", aggfunc="last")[ORDER]
    inst = df.pivot_table(index=df.index, columns="symbol", values="instrument_id", aggfunc="last")[ORDER]
    close = close.resample(BAR, label="right", closed="right").last()
    inst = inst.resample(BAR, label="right", closed="right").last()
    r = np.log(close).diff()
    r[inst.ne(inst.shift())] = np.nan
    return r.dropna(how="all")


def session_dates(idx: pd.DatetimeIndex) -> pd.DatetimeIndex:
    # Globex opens 18:00 ET, so evening bars belong to the next day's session.
    et = idx.tz_convert("America/New_York")
    return (et + pd.Timedelta(hours=6)).normalize().tz_localize(None)


def main() -> None:
    r = load_returns(PARQUET)
    sess = session_dates(r.index)
    days = pd.DatetimeIndex(sess.unique()).sort_values()
    pos = days.get_indexer(sess)  # session ordinal of every bar, non-decreasing
    if (pos == len(days) - 1).sum() < 40:  # the download ended partway into a session
        keep = pos < len(days) - 1
        r, pos, days = r[keep], pos[keep], days[:-1]

    # One snapshot per week (its last session), plus the most recent session.
    week_last = pd.Series(np.arange(len(days)), index=days).groupby(days.to_period("W-FRI")).last()
    snaps = sorted(set(week_last.to_numpy().tolist()) | {len(days) - 1})

    iu = np.triu_indices(len(ORDER), 1)
    vals = r.to_numpy()

    def upper(block: np.ndarray, min_periods: int) -> list:
        c = pd.DataFrame(block).corr(min_periods=min_periods).to_numpy()[iu]
        return [None if np.isnan(x) else int(round(x * 100)) for x in c]

    windows = {}
    for w in WINDOWS:
        rows = []
        for s in snaps:
            if s < w - 1:
                rows.append(None)
                continue
            lo, hi = np.searchsorted(pos, [s - w + 1, s + 1])
            rows.append(upper(vals[lo:hi], w * MIN_BARS_PER_SESSION))
        windows[str(w)] = rows
        print(f"{w}-session window: {sum(x is not None for x in rows)} snapshots")

    data = {
        "markets": ORDER,
        "dates": [days[s].strftime("%Y-%m-%d") for s in snaps],
        "windows": windows,
        "full": upper(vals, 1000),
        "first": days[0].strftime("%Y-%m-%d"),
        "last": days[-1].strftime("%Y-%m-%d"),
        "bars": int(len(r)),
    }
    html = TEMPLATE.read_text().replace("__DATA__", json.dumps(data, separators=(",", ":")))
    OUT.write_text(html)
    print(f"Wrote {OUT} ({OUT.stat().st_size / 1e3:.0f} KB)")


if __name__ == "__main__":
    main()
