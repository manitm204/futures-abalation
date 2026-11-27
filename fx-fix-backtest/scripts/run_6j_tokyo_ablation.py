"""6J around the Tokyo fix (09:55 Tokyo = 19:55 ET in winter, 20:55 ET in US summer).

Krohn, Mueller and Whelan (JF 2024): the dollar rises into a fix and falls after it. 6J is USD per
yen, so: SHORT 6J before the fix, LONG 6J after it. Development 2018-22 showed both legs (t -4.7 and
+5.6) and validation 2023-24 kept the signs; costs ate the plain version.

Grid (all fixed before any run):
  side        short_pre | long_post | both
  pre leg     start fix-90/-75/-60/-45/-30 min (fix-120 is 17:55 ET in winter: before Topstep's 18:00 open), exit fix-10/-5/0
  post leg    start fix+0/+5/+10, exit fix+30/+45/+60/+90/+120
  stop        none | 1.0 | 2.0 x the trailing 60-day sd of that leg's move (prior days only)
  target      none | 0.5 | 1.0 x the same sd
  days        all | gotobi (5th/10th/15th/20th/25th/30th or month end, moved to the previous weekday) | non-gotobi
  both: if the pre exit and post entry are both at the fix, the position flips (3 fills, not 4)
Fills: entries/time exits at the minute's open, 1 tick slippage per side, $2.50/side commission
(one full 6J contract). Stop: fills at max(open, stop) + 1 tick (short) and is checked first in a bar;
target: a limit, filled only if the bar trades 1 tick through it.

Selection (stated before running): dev Sharpe >= 0.75, dev net > 0 at 1.5x costs, >= 100 dev trades,
median dev Sharpe of its timing neighbours (one step on each timing axis) >= 0.5; then validation
Sharpe >= 0.5 and net > 0. Up to 5 distinct finalists (best dev Sharpe first, at most one per
side x days x stop x target family) are frozen into selection_manifest.json, and only then is the
holdout read, once.

  PYTHONPATH=. .venv/bin/python scripts/run_6j_tokyo_ablation.py select runs/tokyo_6j_v1
  PYTHONPATH=. .venv/bin/python scripts/run_6j_tokyo_ablation.py holdout runs/tokyo_6j_v1
"""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from src.experiments.data_access import authorize_holdout_access, load_phase_bars
from src.experiments.funnel_config import load_funnel_config

ROOT = Path(__file__).resolve().parents[1]
MULT, TICK, COMM = 12_500_000.0, 0.0000005, 2.50
TV = MULT * TICK                       # $6.25 per tick
W0, W1 = -95, 125                      # fix-95 = 18:20 ET in winter (Topstep opens 18:00)                     # minute window around the fix
PRE_START, PRE_END = [-90, -75, -60, -45, -30], [-10, -5, 0]
POST_START, POST_END = [0, 5, 10], [30, 45, 60, 90, 120]
STOPS, TARGETS, DAYS = [None, 1.0, 2.0], [None, 0.5, 1.0], ["all", "gotobi", "non_gotobi"]
PH = {"dev": ("2018-01-01", "2022-12-31"), "val": ("2023-01-01", "2024-12-31"), "hold": ("2025-01-01", "2026-12-31"),
      "hold_2025": ("2025-01-01", "2025-12-31"), "hold_2026": ("2026-01-01", "2026-12-31")}


def fix_matrix(bars):
    """Per weekday: 1-min open/high/low on minutes fix-125 .. fix+125 (forward-filled), same contract."""
    df = bars.select("bar_open_ts", "open", "high", "low", "close", "instrument_id").to_pandas()
    ts = df.bar_open_ts.dt.tz_convert("UTC").dt.tz_localize(None).values.astype("datetime64[m]")
    o, h, l, c, iid = (df[k].values for k in ("open", "high", "low", "close", "instrument_id"))
    first, last = pd.Timestamp(ts[0]).date(), pd.Timestamp(ts[-1]).date()
    days = pd.bdate_range(first, last)
    fx = np.array([(pd.Timestamp(d.date()).tz_localize("Asia/Tokyo") + pd.Timedelta(hours=9, minutes=55))
                   .tz_convert("UTC").tz_localize(None).to_datetime64() for d in days]).astype("datetime64[m]")
    grid = fx[:, None] + np.arange(W0, W1 + 1).astype("timedelta64[m]")[None, :]
    idx = np.searchsorted(ts, grid.ravel()).reshape(grid.shape)
    idx = np.clip(idx, 0, len(ts) - 1)
    exact = ts[idx] == grid
    # forward fill missing minutes from the last known close (no trade in that minute)
    prev = np.clip(np.searchsorted(ts, grid.ravel(), side="right").reshape(grid.shape) - 1, 0, len(ts) - 1)
    O = np.where(exact, o[idx], c[prev]); H = np.where(exact, h[idx], c[prev]); L = np.where(exact, l[idx], c[prev])
    ok = exact[:, -W0] & (np.abs(ts[prev[:, 0]] - grid[:, 0]) < np.timedelta64(30, "m")) & (iid[prev[:, 0]] == iid[prev[:, -1]])
    return pd.DatetimeIndex(days)[ok], O[ok], H[ok], L[ok]


def gotobi(days: pd.DatetimeIndex) -> np.ndarray:
    out = np.zeros(len(days), bool)
    s = set(days.normalize())
    for y, m in sorted({(d.year, d.month) for d in days}):
        me = (pd.Timestamp(y, m, 1) + pd.offsets.MonthEnd(0))
        for dd in [5, 10, 15, 20, 25, 30, None]:
            t = me if dd is None or dd > me.day else pd.Timestamp(y, m, dd)
            while t.weekday() >= 5:
                t -= pd.Timedelta(days=1)
            if t in s:
                out[days.get_loc(t)] = True
    return out


def leg(O, H, L, side, a, b, stop_k, tgt_k, sd):
    """P&L in $ per contract per day, and whether it exited at the time exit."""
    ia, ib = a - W0, b - W0
    e = O[:, ia]
    sgn = 1.0 if side == "long" else -1.0
    exit_px = O[:, ib].copy()
    timed = np.ones(len(e), bool)
    done = np.zeros(len(e), bool)
    slip_exit = np.full(len(e), TICK)
    if stop_k is not None or tgt_k is not None:
        sdist = stop_k * sd if stop_k is not None else np.full(len(e), np.inf)
        tdist = tgt_k * sd if tgt_k is not None else np.full(len(e), np.inf)
        stp = e - sgn * sdist
        tgt = e + sgn * tdist
        for k in range(ia, ib):
            act = ~done
            if not act.any():
                break
            if sgn > 0:
                hit_s = act & (L[:, k] <= stp); hit_t = act & ~hit_s & (H[:, k] >= tgt + TICK)
                exit_px = np.where(hit_s, np.minimum(O[:, k], stp), exit_px)
            else:
                hit_s = act & (H[:, k] >= stp); hit_t = act & ~hit_s & (L[:, k] <= tgt - TICK)
                exit_px = np.where(hit_s, np.maximum(O[:, k], stp), exit_px)
            exit_px = np.where(hit_t, tgt, exit_px)
            slip_exit = np.where(hit_t, 0.0, slip_exit)
            done |= hit_s | hit_t
            timed &= ~(hit_s | hit_t)
    pnl = sgn * ((exit_px - sgn * slip_exit) - (e + sgn * TICK)) * MULT - 2 * COMM
    gross = sgn * (exit_px - e) * MULT
    return pnl, gross, timed


def trailing_sd(O, a, b):
    mv = pd.Series(O[:, b - W0] - O[:, a - W0])
    return mv.rolling(60, min_periods=40).std().shift(1).values


def metrics(p: pd.Series, n_trades: int) -> dict:
    g, l = p[p > 0].sum(), -p[p < 0].sum()
    eq = p.cumsum()
    return {"sharpe": round(float(p.mean() / p.std() * np.sqrt(252)), 3) if p.std() > 0 else 0.0,
            "pf": round(float(g / l), 3) if l > 0 else None, "net": round(float(p.sum())), "per_yr": round(float(p.mean() * 252)),
            "maxdd": round(float((eq - eq.cummax()).min())), "trades": int(n_trades)}


def evaluate(days, O, H, L, configs=None):
    got = gotobi(days)
    legs = {}
    for side, starts, ends in (("short", PRE_START, PRE_END), ("long", POST_START, POST_END)):
        for a, b in itertools.product(starts, ends):
            sd = trailing_sd(O, a, b)
            for s, t in itertools.product(STOPS, TARGETS):
                legs[(side, a, b, s, t)] = leg(O, H, L, side, a, b, s, t, sd) + (np.isfinite(sd) | (s is None and t is None),)
    rows = []
    def cfgs():
        for s, t, dsel in itertools.product(STOPS, TARGETS, DAYS):
            for a, b in itertools.product(PRE_START, PRE_END):
                yield ("short_pre", a, b, None, None, s, t, dsel)
            for a, b in itertools.product(POST_START, POST_END):
                yield ("long_post", None, None, a, b, s, t, dsel)
            for a, b, c, d in itertools.product(PRE_START, PRE_END, POST_START, POST_END):
                yield ("both", a, b, c, d, s, t, dsel)
    for cfg in (configs or cfgs()):
        side, a, b, c, d, s, t, dsel = cfg
        pnl = np.zeros(len(days)); gross = np.zeros(len(days)); n = np.zeros(len(days))
        valid = np.ones(len(days), bool)
        if side in ("short_pre", "both"):
            p1, g1, tm1, v1 = legs[("short", a, b, s, t)]; pnl += p1; gross += g1; n += 1; valid &= v1
        if side in ("long_post", "both"):
            p2, g2, tm2, v2 = legs[("long", c, d, s, t)]; pnl += p2; gross += g2; n += 1; valid &= v2
        if side == "both" and b == 0 and c == 0:
            pnl = pnl + np.where(tm1, TICK * MULT + COMM, 0.0)   # flip: one fill saved when the pre leg ran to the fix
        sel = valid & (got if dsel == "gotobi" else ~got if dsel == "non_gotobi" else True)
        daily = pd.Series(np.where(sel, pnl, 0.0), index=days)
        cost = np.where(sel, gross - pnl, 0.0)
        daily15 = pd.Series(np.where(sel, gross, 0.0) - 1.5 * cost, index=days)
        r = {"side": side, "pre_start": a, "pre_end": b, "post_start": c, "post_end": d, "stop": s, "target": t, "days": dsel}
        for ph, (x, y) in PH.items():
            dd = daily[x:y]
            if not len(dd):
                continue
            m = metrics(dd, int((sel[(days >= x) & (days <= y)] * n[(days >= x) & (days <= y)]).sum()))
            m["net_1p5x"] = round(float(daily15[x:y].sum()))
            m["gross_per_trade"] = round(float(np.where(sel, gross, 0)[(days >= x) & (days <= y)].sum() / max(m["trades"], 1)), 2)
            r[ph] = m
        rows.append(r)
    return rows


def neighbours(r, table):
    """Configs one step away on each timing axis (same side/stop/target/days)."""
    out = []
    axes = {"pre_start": PRE_START, "pre_end": PRE_END, "post_start": POST_START, "post_end": POST_END}
    for ax, vals in axes.items():
        v = r[ax]
        if v is None:
            continue
        i = vals.index(v)
        for j in (i - 1, i + 1):
            if 0 <= j < len(vals):
                k = dict(r); k[ax] = vals[j]
                key = tuple(k[x] for x in ("side", "pre_start", "pre_end", "post_start", "post_end", "stop", "target", "days"))
                if key in table:
                    out.append(table[key])
    return out


def main():
    stage, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    fcfg = load_funnel_config(ROOT / "configs/funnel/fx_funnel_6j_v1.yaml")
    if stage == "select":
        bars, _ = load_phase_bars(fcfg, "6J", "validation", command="tokyo_6j_v1_select",
                                  experiment_id="6J Tokyo-fix ablation v1: dev selection + validation")
        days, O, H, L = fix_matrix(bars)
        rows = evaluate(days, O, H, L)
        pd.DataFrame([{**{k: v for k, v in r.items() if k not in PH}, **{f"{ph}_{m}": v for ph in ("dev", "val") for m, v in r[ph].items()}}
                      for r in rows]).to_parquet(out / "grid.parquet")
        key = lambda r: tuple(r[x] for x in ("side", "pre_start", "pre_end", "post_start", "post_end", "stop", "target", "days"))
        table = {key(r): r for r in rows}
        passed_dev = [r for r in rows if r["dev"]["sharpe"] >= 0.75 and r["dev"]["net_1p5x"] > 0 and r["dev"]["trades"] >= 100]
        stable = [r for r in passed_dev if (nb := neighbours(r, table)) and np.median([x["dev"]["sharpe"] for x in nb]) >= 0.5]
        passed_val = [r for r in stable if r["val"]["sharpe"] >= 0.5 and r["val"]["net"] > 0]
        fam, finalists = set(), []
        for r in sorted(passed_val, key=lambda r: -r["dev"]["sharpe"]):
            f = (r["side"], r["days"], r["stop"], r["target"])
            if f in fam:
                continue
            fam.add(f); finalists.append(r)
            if len(finalists) == 5:
                break
        summ = {"n_configs": len(rows), "dev_profitable": sum(r["dev"]["net"] > 0 for r in rows),
                "val_profitable": sum(r["val"]["net"] > 0 for r in rows),
                "both_profitable": sum(r["dev"]["net"] > 0 and r["val"]["net"] > 0 for r in rows),
                "passed_dev": len(passed_dev), "stable": len(stable), "passed_val": len(passed_val),
                "dev_sharpe_q": np.percentile([r["dev"]["sharpe"] for r in rows], [10, 50, 90, 99]).round(2).tolist(),
                "val_sharpe_q": np.percentile([r["val"]["sharpe"] for r in rows], [10, 50, 90, 99]).round(2).tolist()}
        by = {}
        for dim in ("side", "stop", "target", "days"):
            g = pd.DataFrame([{dim: str(r[dim]), "dev": r["dev"]["sharpe"], "val": r["val"]["sharpe"],
                               "pos": r["dev"]["net"] > 0 and r["val"]["net"] > 0} for r in rows]).groupby(dim)
            by[dim] = g.agg(dev_median=("dev", "median"), val_median=("val", "median"), share_both_pos=("pos", "mean")).round(3).reset_index().to_dict("records")
        summ["by_dimension"] = by
        manifest = {"experiment": "tokyo_6j_v1", "selection_rule": __doc__.split("Selection")[1].strip(),
                    "finalists": [{k: r[k] for k in ("side", "pre_start", "pre_end", "post_start", "post_end", "stop", "target", "days")} for r in finalists]}
        (out / "selection_manifest.json").write_text(json.dumps(manifest, indent=1))
        (out / "selection_manifest.sha256").write_text(hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest())
        (out / "select_summary.json").write_text(json.dumps({"summary": summ, "finalists": finalists,
                                                              "top20_dev": sorted(rows, key=lambda r: -r["dev"]["sharpe"])[:20]}, indent=1, default=str))
        print(json.dumps(summ, indent=1, default=str))
        for r in finalists:
            print("FINALIST", {k: r[k] for k in ("side", "pre_start", "pre_end", "post_start", "post_end", "stop", "target", "days")}, "dev", r["dev"], "val", r["val"])
    else:
        manifest = json.loads((out / "selection_manifest.json").read_text())
        sha = (out / "selection_manifest.sha256").read_text().strip()
        assert sha == hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
        if not manifest["finalists"]:
            print("no finalists; holdout not read"); return
        auth = authorize_holdout_access(manifest_sha256=sha, confirm=True, command="tokyo_6j_v1_holdout")
        bars, info = load_phase_bars(fcfg, "6J", "holdout", command="tokyo_6j_v1_holdout", authorization=auth,
                                     experiment_id="6J Tokyo-fix ablation v1: frozen finalists, single holdout read")
        days, O, H, L = fix_matrix(bars)
        cf = [tuple(f[x] for x in ("side", "pre_start", "pre_end", "post_start", "post_end", "stop", "target", "days")) for f in manifest["finalists"]]
        rows = evaluate(days, O, H, L, configs=cf)
        (out / "holdout_results.json").write_text(json.dumps({"last_session": info["actual_last_session"], "rows": rows}, indent=1, default=str))
        for r in rows:
            print({k: r[k] for k in ("side", "pre_start", "pre_end", "post_start", "post_end", "stop", "target", "days")}, "\n  HOLD", r.get("hold"), "\n  2025", r.get("hold_2025"), "\n  2026", r.get("hold_2026"))


if __name__ == "__main__":
    main()
