"""Placebo-day ("luck") benchmark for a month-end funnel run's validation finalists.

The month-end counterpart of the other families' random-entry benchmarks. Here the question is
whether the CALENDAR matters, so the random runs keep each finalist's clock (entry time and exit
rule), stop and direction (long) and move only the days: every random run trades on a random set of
validation-window NYSE trading days that are NOT among the month's last 5 or first 4 trading days. Finalists
are grouped by clock and stop (entry time x exit rule x stop). For each group, every whole-percent time in market
between the group's lowest and highest validation exposure gets `--n-sims` random runs on the same
validation window, costs and sizing; the number of placebo days is scaled from the group's
finalists so the time in market matches the level.

Each finalist is placed against its group's random runs at its own (rounded) time in market:
`luck_pct_sharpe` is the share of random runs whose Sharpe it beat (likewise for return).
~50% = no better than the same clock on ordinary days.

The finalists are re-run on the validation window; the script checks those re-runs reproduce
validation_results.json exactly. Validation data only (the window `validate` already used);
logged to the data-access ledger as command `random_benchmark`. Output:
runs/funnel/<experiment>/random_benchmark.json (read by export_results_json.py).

Usage:
  PYTHONPATH=. python scripts/run_me_random_benchmark.py --experiment-id me_zn_v1 \
      --config configs/funnel/me_funnel_zn_v1.yaml
"""

from __future__ import annotations

import json
import zlib
from datetime import date
from pathlib import Path

import numpy as np
import typer

from scripts.run_me_funnel import _frames, _params, _select_space
from src.analysis.daily_performance import daily_equity, window_metrics
from src.experiments.funnel_config import load_execution_config, load_funnel_config
from src.experiments.funnel_prep import _metric_kwargs
from src.strategies.month_end.backtest import MEData, simulate_month_end
from src.strategies.month_end.config import exit_minutes, hhmm_minutes
from src.utils.serialization import atomic_write_json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLACEBO_EXCLUDE_LAST = 5   # placebo days are never among the month's last 5 trading days
PLACEBO_EXCLUDE_FIRST = 4  # ... or its first 4 (v2 trades up to the first 3)
app = typer.Typer(add_completion=False)


def _q(a: np.ndarray, q: float) -> float | None:
    a = a[np.isfinite(a)]
    return float(np.quantile(a, q)) if len(a) else None


def _gkey(prm: dict) -> str:
    return f"{prm['timeframe']}|{prm['entry']}-{prm['exit']}-{prm['stop']}"


def _gorder(g: str) -> tuple:
    entry, exit_, stop = g.split("|")[1].split("-")
    return hhmm_minutes(entry), exit_minutes(exit_, date(2020, 1, 1)), -1.0 if stop == "none" else float(stop)


@app.command()
def main(
    experiment_id: str = typer.Option(...),
    config: Path = typer.Option(...),
    n_sims: int = typer.Option(100, help="Random runs per time-in-market level"),
    runs_root: Path = typer.Option(PROJECT_ROOT / "runs" / "funnel"),
) -> None:
    fcfg = load_funnel_config(config)
    _select_space(fcfg)
    ec = load_execution_config(fcfg)
    exp = runs_root / experiment_id
    val = json.loads((exp / "validation_results.json").read_text())
    params_of = {c["config_id"]: c["params"]
                 for c in json.loads((exp / "frozen_representatives.json").read_text())["candidates"]}
    v = fcfg.data.validation
    frames, info = _frames(fcfg, fcfg.symbol, "validation", command="random_benchmark", experiment_id=experiment_id)
    eq0, mk = ec.starting_equity, _metric_kwargs(fcfg)
    data = MEData(frames[f"{fcfg.symbol}|1min"])
    s64, e64 = np.datetime64(v.start, "D"), np.datetime64(v.end, "D")
    in_win = (data.days >= s64) & (data.days <= e64)
    placebo_pool = np.flatnonzero(in_win & (data.rank > PLACEBO_EXCLUDE_LAST)
                                  & (data.rank_start > PLACEBO_EXCLUDE_FIRST))

    # ---- re-run finalists on validation ----
    fins, pool = [], {}
    for r in val.get("results", []):
        prm = params_of[r["config_id"]]
        sim = simulate_month_end(data, _params(prm), exec_config=ec, starting_equity=eq0)
        m, _ = window_metrics(sim, data, daily_equity(sim, data, eq0), start=v.start, end=v.end,
                              starting_equity=eq0, **mk)
        for k in ("sharpe", "net_return", "exposure", "n_completed_trades"):
            if m[k] != r["metrics"][k]:
                raise RuntimeError(f"{r['config_id']}: re-run {k} {m[k]} != validation {r['metrics'][k]}")
        g = _gkey(prm)
        inwin = (data.session_date[sim.entry_idx] >= s64) & (data.session_date[sim.entry_idx] <= e64)
        lens, per_day = pool.setdefault(g, ([], []))
        lens.extend((sim.exit_idx[inwin] - sim.entry_idx[inwin] + 1).tolist())
        n_tr = int(inwin.sum())
        if n_tr and m["exposure"]:
            per_day.append(100 * m["exposure"] / n_tr)
        fins.append({"config_id": r["config_id"], "dev_order": r["dev_order"], "status": r["status"], "group": g,
                     "timeframe": prm["timeframe"], "direction": "long", "params": prm,
                     **{k: r["metrics"][k] for k in ("exposure", "net_return", "sharpe")}})
    typer.echo(f"{experiment_id}: {len(fins)} finalists re-run on validation and matched exactly")

    groups = sorted(pool, key=_gorder)
    curves, raw, meta, levels_of = {}, {}, {}, {}
    for g in groups:
        lens = np.asarray(pool[g][0], dtype=np.int64)
        pct_per_day = float(np.mean(pool[g][1])) if pool[g][1] else None
        exps = [f["exposure"] for f in fins if f["group"] == g and f["exposure"] is not None]
        if not exps or not pct_per_day:
            continue
        rep = next(f for f in fins if f["group"] == g)
        clock = _params(rep["params"])   # the day mask replaces its calendar
        lo, hi = max(1, round(100 * min(exps))), max(1, round(100 * max(exps)))
        levels_of[g] = list(range(lo, hi + 1))
        meta[g] = {"timeframe": "1min", "direction": "long", "p_long": 1.0, "n_pool_trades": int(len(lens)),
                   "median_trade_bars": float(np.median(lens)), "mean_trade_bars": float(np.mean(lens)),
                   "placebo_pool_days": int(len(placebo_pool))}
        rows = []
        for lvl in levels_of[g]:
            k = int(min(len(placebo_pool), max(1, round(lvl / pct_per_day))))
            rng = np.random.default_rng([fcfg.seed, zlib.crc32(g.encode()), lvl])
            sh, ret, ex, nt = [], [], [], []
            for _ in range(n_sims):
                mask = np.zeros(len(data.days), dtype=bool)
                mask[rng.choice(placebo_pool, size=k, replace=False)] = True
                sim = simulate_month_end(data, clock, exec_config=ec, starting_equity=eq0, day_mask=mask)
                m, _ = window_metrics(sim, data, daily_equity(sim, data, eq0), start=v.start, end=v.end,
                                      starting_equity=eq0, **mk)
                sh.append(np.nan if m["sharpe"] is None else m["sharpe"])
                ret.append(m["net_return"]); ex.append(m["exposure"] or 0.0); nt.append(m["n_completed_trades"])
            sh, ret = np.array(sh), np.array(ret)
            raw[(g, lvl)] = (sh, ret)
            rows.append({"exposure_pct": lvl, "actual_exposure": float(np.mean(ex)), "mean_trades": float(np.mean(nt)),
                         "mean_return": float(np.mean(ret)), "median_return": _q(ret, 0.5),
                         "p10_return": _q(ret, 0.1), "p90_return": _q(ret, 0.9),
                         "mean_sharpe": float(np.nanmean(sh)), "median_sharpe": _q(sh, 0.5),
                         "p10_sharpe": _q(sh, 0.1), "p90_sharpe": _q(sh, 0.9),
                         "frac_profitable": float(np.mean(ret > 0))})
        curves[g] = rows
        typer.echo(f"{experiment_id} {g}: {len(rows)} levels x {n_sims} sims "
                   f"(median trade {meta[g]['median_trade_bars']:.0f} bars, {len(placebo_pool)} placebo days)")

    for f in fins:
        lv = levels_of.get(f["group"])
        if not lv:
            f.update(exposure_level=None, luck_pct_sharpe=None, luck_pct_return=None)
            continue
        lvl = min(max(round(100 * (f["exposure"] or 0)), lv[0]), lv[-1])
        sh, ret = raw[(f["group"], lvl)]
        f["exposure_level"] = lvl
        f["luck_pct_sharpe"] = None if f["sharpe"] is None else float(np.mean(np.nan_to_num(sh, nan=-np.inf) < f["sharpe"]))
        f["luck_pct_return"] = float(np.mean(ret < f["net_return"]))
        f.pop("params", None)
    for f in fins:
        f.pop("params", None)
    atomic_write_json(exp / "random_benchmark.json", {
        "experiment_id": experiment_id, "window": [str(v.start), str(v.end)], "n_sims": n_sims,
        "levels": sorted({x for lv in levels_of.values() for x in lv}), "groups": meta, "group_levels": levels_of,
        "curves": curves, "finalists": fins, "data_access": info,
        "method": ("Per clock and stop (entry time x exit rule x stop): the same long trade at the same clock, but on random "
                   f"validation-window NYSE trading days that are not among the month's last {PLACEBO_EXCLUDE_LAST} "
                   f"or first {PLACEBO_EXCLUDE_FIRST} trading days. The number of days is scaled so the time in market matches each level. Same "
                   "fills, slippage, commission and whole-contract sizing as the strategy; scored with the same "
                   "daily-Sharpe and time-in-market code."),
    })
    typer.echo(f"wrote {exp / 'random_benchmark.json'}")


if __name__ == "__main__":
    app()
