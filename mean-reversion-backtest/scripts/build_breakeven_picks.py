"""Pick the top 3 finalists of each latest run (one market x bar size) by training break-even cost
multiple, and look at how they did in validation (2023-24) against random-entry timing.

Ranking (training only): break-even cost multiple (finalists still profitable beyond 25x count as
25x), ties broken by return with a 1-bar entry delay, then the funnel's own order. Validation
return / Sharpe / PF and the luck % (share of random-entry runs at the same time in market whose
Sharpe / return it beat) are read from each run's validation_results.json and random_benchmark.json;
nothing is re-run and the holdout is not read. Baselines: the funnel's own top 3, the average
finalist, and holding the market.

Writes runs/funnel/selection_model_v1/breakeven_picks.json.

Usage:
  PYTHONPATH=. python scripts/build_breakeven_picks.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUNS = PROJECT_ROOT / "runs" / "funnel"
SITE = PROJECT_ROOT.parent / "futures-results" / "data"
LATEST = ["mr_es_v6_15m", "mr_es_v6_1h", "mr_nq_v7_15m", "mr_nq_v7_1h", "mr_ym_v7_15m", "mr_ym_v7_1h",
          "mr_rty_v7_15m", "mr_rty_v7_1h", "mr_cl_v7", "mr_gc_v6_15m", "mr_gc_v6_1h", "mr_6e_v6"]
K = 3


def _bench(run: str, mkt: str) -> dict | None:
    for f in (SITE / mkt).glob("*.json"):
        d = json.loads(f.read_text())
        if d.get("run_id") == run and "benchmark" in d:
            return d["benchmark"]["val"]
    return None


def _rand_median(rb: dict, tf: str, lvl: int) -> float | None:
    for c in rb["curves"].get(tf, []):
        if c["exposure_pct"] == lvl:
            return c["median_sharpe"]
    return None


def main() -> None:
    out, allp = [], {"breakeven": [], "funnel": [], "all": []}
    for run in LATEST:
        d = RUNS / run
        reps = {r["config_id"]: r for r in json.loads((d / "representatives.json").read_text())}
        frozen = json.loads((d / "frozen_representatives.json").read_text())
        val = {r["config_id"]: r for r in json.loads((d / "validation_results.json").read_text())["results"]}
        rb = json.loads((d / "random_benchmark.json").read_text())
        luck = {f["config_id"]: f for f in rb["finalists"]}
        rows = []
        for c in frozen["candidates"]:
            r, v, lk = reps[c["config_id"]], val[c["config_id"]], luck[c["config_id"]]
            be = 25.0 if str(r.get("breakeven_status", "")).startswith("profitable_beyond") else r["breakeven_cost_multiplier"]
            m = v["metrics"]
            rows.append({"order": c["dev_order"], "params": c["params"], "be": be,
                         "delay": r.get("stress_delay_net_return"), "dev_sharpe": r["dev_sharpe"],
                         "dev_return": r["dev_net_return"], "dev_pf": r["dev_profit_factor"],
                         "val_return": m["net_return"], "val_sharpe": m["sharpe"], "val_pf": m["profit_factor"],
                         "val_trades": m["n_completed_trades"], "passed": v["status"] == "pass",
                         "luck_sharpe": lk["luck_pct_sharpe"], "luck_return": lk["luck_pct_return"],
                         "rand_median_sharpe": _rand_median(rb, lk["timeframe"], lk["exposure_level"])})
        key = lambda x: (-(x["be"] if x["be"] is not None else -1), -(x["delay"] or -9), x["order"])  # noqa: E731
        picks = sorted(rows, key=key)[:K]
        funnel = sorted(rows, key=lambda x: x["order"])[:K]
        n_capped = sum(x["be"] == 25.0 for x in rows)
        agg = lambda xs: {k: float(np.mean([x[k] for x in xs])) for k in  # noqa: E731
                          ("val_return", "val_sharpe", "luck_sharpe", "luck_return")} | {
            "val_pf_median": float(np.median([x["val_pf"] for x in xs])), "passed": float(np.mean([x["passed"] for x in xs]))}
        out.append({"run": run, "market": frozen["symbol"], "timeframe": rows[0]["params"]["timeframe"],
                    "n_finalists": len(rows), "n_capped_25x": n_capped, "picks": picks,
                    "picks_avg": agg(picks), "funnel_top3_avg": agg(funnel), "all_avg": agg(rows),
                    "hold_market": _bench(run, frozen["symbol"])})
        allp["breakeven"] += picks
        allp["funnel"] += funnel
        allp["all"] += rows
    pooled = {k: {"n": len(v), **{m: float(np.mean([x[m] for x in v])) for m in
                                  ("val_return", "val_sharpe", "luck_sharpe", "luck_return")},
                  "val_pf_median": float(np.median([x["val_pf"] for x in v])),
                  "passed": float(np.mean([x["passed"] for x in v])),
                  "beat_luck_median": float(np.mean([x["luck_sharpe"] > 0.5 for x in v]))} for k, v in allp.items()}
    (RUNS / "selection_model_v1" / "breakeven_picks.json").write_text(json.dumps({"runs": out, "pooled": pooled}, default=str))

    for r in out:
        h = r["hold_market"] or {}
        print(f"\n{r['run']} ({r['market']} {r['timeframe']}): {r['n_finalists']} finalists, {r['n_capped_25x']} capped at 25x;"
              f" hold market val {h.get('net_return', float('nan')):+.1%} Sharpe {h.get('sharpe', float('nan')):.2f}")
        for p in r["picks"]:
            s = p["params"]
            print(f"  #{p['order']:<4d} BE {p['be']:5.1f}x  dev Sh {p['dev_sharpe']:.2f} | val {p['val_return']:+.1%} Sh {p['val_sharpe']:+.2f} "
                  f"PF {p['val_pf']:.2f} n{p['val_trades']} luck(Sh) {p['luck_sharpe']:.0%} luck(ret) {p['luck_return']:.0%} rand-med Sh {p['rand_median_sharpe']:+.2f} "
                  f"{'PASS' if p['passed'] else 'fail'}  {s['mean_type']} {s['mean_lookback']}/{s['std_lookback']} e{s['entry_z']} x{s['exit_z']} h{s['max_holding_bars']} stop {s['stop_atr_multiple']} {s['entry_confirmation']}")
        for lab in ("picks_avg", "funnel_top3_avg", "all_avg"):
            a = r[lab]
            print(f"  {lab:16s} val {a['val_return']:+.1%} Sh {a['val_sharpe']:+.2f} PF {a['val_pf_median']:.2f} luck {a['luck_sharpe']:.0%} passed {a['passed']:.0%}")
    print()
    for k, v in pooled.items():
        print(f"POOLED {k:10s} n{v['n']:5d} val {v['val_return']:+.2%} Sh {v['val_sharpe']:+.2f} PF {v['val_pf_median']:.2f} "
              f"luck(Sh) {v['luck_sharpe']:.0%} luck(ret) {v['luck_return']:.0%} beat-median {v['beat_luck_median']:.0%} passed {v['passed']:.0%}")


if __name__ == "__main__":
    main()
