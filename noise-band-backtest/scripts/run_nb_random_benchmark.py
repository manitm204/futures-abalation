"""Random-entry ("luck") benchmark for a noise-band funnel run's validation finalists.

The noise-band counterpart of mean-reversion-backtest/scripts/run_random_benchmark.py.
Finalists are grouped by bar size and direction setting (long-only vs both). For each
group, every whole-percent time in market between the group's lowest and highest
validation exposure gets `--n-sims` random runs on the same validation window, costs
and sizing (src/experiments/nb_random_entry.py): random INTRADAY trades that never
overlap, with lengths drawn from the group's own validation trades, long with the
group's actual long share of trades (1.0 for long-only), otherwise short.

Each finalist is placed against its group's random runs at its own (rounded) time in
market: `luck_pct_sharpe` is the share of random runs whose Sharpe it beat (likewise
for return). ~50% = no better than random entries.

The finalists are re-run on the validation window to get their trades; the script
checks those re-runs reproduce validation_results.json exactly. Validation data only
(the window `validate` already used); logged to the data-access ledger as command
`random_benchmark`. Output: runs/funnel/<experiment>/random_benchmark.json (read by
export_results_json.py).

Usage:
  PYTHONPATH=. python scripts/run_nb_random_benchmark.py --experiment-id nb_es_v4 \
      --config configs/funnel/nb_funnel_es_v4.yaml
"""

from __future__ import annotations

import json
import zlib
from pathlib import Path

import numpy as np
import typer

from scripts.run_nb_funnel import _frames, _params, _select_space
from src.analysis.daily_performance import daily_equity, window_metrics
from src.experiments.funnel_config import load_execution_config, load_funnel_config
from src.experiments.funnel_prep import _metric_kwargs
from src.experiments.nb_random_entry import simulate_random_intraday
from src.strategies.noise_band.backtest import NBData, simulate_noise_band
from src.utils.serialization import atomic_write_json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TF_ORDER = ["5min", "15min"]
app = typer.Typer(add_completion=False)


def _q(a: np.ndarray, q: float) -> float | None:
    a = a[np.isfinite(a)]
    return float(np.quantile(a, q)) if len(a) else None


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
    datas = {tf: NBData(frames[f"{fcfg.symbol}|{tf}"]) for tf in {p["timeframe"] for p in params_of.values()}}
    s64, e64 = np.datetime64(v.start, "D"), np.datetime64(v.end, "D")

    # ---- re-run finalists on validation: trade lengths and sides per group ----
    fins, pool = [], {}
    for r in val["results"]:
        prm = params_of[r["config_id"]]
        tf, data = prm["timeframe"], datas[prm["timeframe"]]
        sim = simulate_noise_band(data, _params(prm), exec_config=ec, starting_equity=eq0)
        m, _ = window_metrics(sim, data, daily_equity(sim, data, eq0), start=v.start, end=v.end,
                              starting_equity=eq0, **mk)
        for k in ("sharpe", "net_return", "exposure", "n_completed_trades"):
            if m[k] != r["metrics"][k]:
                raise RuntimeError(f"{r['config_id']}: re-run {k} {m[k]} != validation {r['metrics'][k]}")
        inwin = (data.session_date[sim.entry_idx] >= s64) & (data.session_date[sim.entry_idx] <= e64)
        g = f"{tf}|{prm['direction']}"
        lens, sides = pool.setdefault(g, ([], []))
        lens.extend((sim.exit_idx[inwin] - sim.entry_idx[inwin] + 1).tolist())
        sides.extend(sim.side[inwin].tolist())
        fins.append({"config_id": r["config_id"], "dev_order": r["dev_order"], "status": r["status"], "group": g,
                     "timeframe": tf, "direction": prm["direction"],
                     **{k: r["metrics"][k] for k in ("exposure", "net_return", "sharpe")}})
    typer.echo(f"{experiment_id}: {len(fins)} finalists re-run on validation and matched exactly")

    groups = sorted(pool, key=lambda g: (TF_ORDER.index(g.split("|")[0]), g.split("|")[1] != "long"))
    curves, raw, meta, levels_of = {}, {}, {}, {}
    for g in groups:
        tf, direction = g.split("|")
        data = datas[tf]
        lens = np.asarray(pool[g][0], dtype=np.int64)
        p_long = float(np.mean(np.asarray(pool[g][1]) > 0))
        exps = [f["exposure"] for f in fins if f["group"] == g and f["exposure"] is not None]
        lo, hi = max(1, round(100 * min(exps))), max(1, round(100 * max(exps)))
        levels_of[g] = list(range(lo, hi + 1))
        meta[g] = {"timeframe": tf, "direction": direction, "p_long": p_long, "n_pool_trades": int(len(lens)),
                   "median_trade_bars": float(np.median(lens)), "mean_trade_bars": float(np.mean(lens))}
        rows = []
        for lvl in levels_of[g]:
            rng = np.random.default_rng([fcfg.seed, zlib.crc32(g.encode()), lvl])
            sh, ret, ex, nt = [], [], [], []
            for _ in range(n_sims):
                sim = simulate_random_intraday(data, fcfg.symbol, exec_config=ec, starting_equity=eq0,
                                               window_start=v.start, window_end=v.end, exposure=lvl / 100,
                                               length_pool=lens, p_long=p_long, rng=rng)
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
        typer.echo(f"{experiment_id} {g}: {len(rows)} levels x {n_sims} sims (long share {p_long:.2f}, "
                   f"median trade {meta[g]['median_trade_bars']:.0f} bars)")

    for f in fins:
        lv = levels_of[f["group"]]
        lvl = min(max(round(100 * (f["exposure"] or 0)), lv[0]), lv[-1])
        sh, ret = raw[(f["group"], lvl)]
        f["exposure_level"] = lvl
        f["luck_pct_sharpe"] = None if f["sharpe"] is None else float(np.mean(np.nan_to_num(sh, nan=-np.inf) < f["sharpe"]))
        f["luck_pct_return"] = float(np.mean(ret < f["net_return"]))
    atomic_write_json(exp / "random_benchmark.json", {
        "experiment_id": experiment_id, "window": [str(v.start), str(v.end)], "n_sims": n_sims,
        "levels": sorted({x for lv in levels_of.values() for x in lv}), "groups": meta, "group_levels": levels_of,
        "curves": curves, "finalists": fins, "data_access": info,
        "method": ("Per bar size and direction setting: random intraday trades on random sessions at random times, "
                   "never overlapping and always closed by the session's last bar, covering the target share of the "
                   "validation window's bars. Trade lengths are drawn from that group's own validation trades; each "
                   "trade is long with the group's actual long share (1.0 for long-only), else short. Same fills, "
                   "slippage, commission and whole-contract sizing as the strategy; scored with the same daily-Sharpe "
                   "and time-in-market code."),
    })
    typer.echo(f"wrote {exp / 'random_benchmark.json'}")


if __name__ == "__main__":
    app()
