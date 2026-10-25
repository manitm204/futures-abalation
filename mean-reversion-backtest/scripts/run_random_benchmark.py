"""Random-entry ("luck") benchmark for a funnel run's validation finalists.

Takes the finalists' validation time in market, rounds the lowest and highest to
whole percent, and for every whole percent in between (inclusive) runs
`--n-sims` random-entry simulations on the same validation window, bar size,
costs and sizing (src/experiments/random_entry.py): random long trades held 3-10
bars, covering that share of bars. Each bar size present among the finalists
gets its own curve, since a "bar" differs.

Each finalist is then placed against the random runs at its own (rounded) time in
market and bar size: `luck_pct_sharpe` is the share of random runs whose Sharpe
it beat (likewise for return). ~50% = no better than random entries.

Validation data only (the same window `validate` already used); logged to the
data-access ledger as command `random_benchmark`. Output:
runs/funnel/<experiment>/random_benchmark.json (read by export_results_json.py).

Usage:
  PYTHONPATH=. python scripts/run_random_benchmark.py --experiment-id mr_es_v5 \
      --config configs/funnel/mr_funnel_es_v5.yaml
"""

from __future__ import annotations

import json
import zlib
from pathlib import Path

import numpy as np
import typer

from src.analysis.daily_performance import daily_equity, window_metrics
from src.data.aggregation import aggregate_bars
from src.experiments.data_access import load_phase_bars
from src.experiments.funnel_config import load_funnel_config
from src.experiments.funnel_prep import _metric_kwargs
from src.experiments.random_entry import simulate_random_entries
from src.strategies.mean_reversion.backtest import MRData
from src.utils.serialization import atomic_write_json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
app = typer.Typer(add_completion=False)


def _q(a: np.ndarray, q: float) -> float | None:
    a = a[np.isfinite(a)]
    return float(np.quantile(a, q)) if len(a) else None


@app.command()
def main(
    experiment_id: str = typer.Option(...),
    config: Path = typer.Option(...),
    n_sims: int = typer.Option(100, help="Random runs per time-in-market level"),
    hold_lo: int = typer.Option(3), hold_hi: int = typer.Option(10),
    runs_root: Path = typer.Option(PROJECT_ROOT / "runs" / "funnel"),
) -> None:
    from scripts.run_mr_funnel import load_execution_config  # same execution config as develop/validate

    fcfg = load_funnel_config(config)
    ec = load_execution_config(fcfg)
    exp = runs_root / experiment_id
    val = json.loads((exp / "validation_results.json").read_text())
    tf_of = {c["config_id"]: c["params"]["timeframe"]
             for c in json.loads((exp / "frozen_representatives.json").read_text())["candidates"]}
    fins = [{"config_id": r["config_id"], "dev_order": r["dev_order"], "status": r["status"],
             "timeframe": tf_of[r["config_id"]], **{k: r["metrics"][k] for k in ("exposure", "net_return", "sharpe")}}
            for r in val["results"]]
    exps = [f["exposure"] for f in fins if f["exposure"] is not None]
    lo, hi = max(1, round(100 * min(exps))), max(1, round(100 * max(exps)))
    levels = list(range(lo, hi + 1))
    tfs = sorted({f["timeframe"] for f in fins}, key=["5min", "15min", "1h"].index)

    v = fcfg.data.validation
    bars, info = load_phase_bars(fcfg, fcfg.symbol, "validation", command="random_benchmark",
                                 experiment_id=experiment_id)
    eq0 = ec.starting_equity
    curves, raw = {}, {}
    for tf in tfs:
        data = MRData(aggregate_bars(bars, timeframe=tf))
        rows = []
        for lvl in levels:
            rng = np.random.default_rng([fcfg.seed, zlib.crc32(tf.encode()), lvl])
            sh, ret, ex, nt = [], [], [], []
            for _ in range(n_sims):
                sim = simulate_random_entries(data, fcfg.symbol, exec_config=ec, starting_equity=eq0,
                                              window_start=v.start, window_end=v.end, exposure=lvl / 100,
                                              rng=rng, hold_lo=hold_lo, hold_hi=hold_hi)
                m, _ = window_metrics(sim, data, daily_equity(sim, data, eq0), start=v.start, end=v.end,
                                      starting_equity=eq0, **_metric_kwargs(fcfg))
                sh.append(np.nan if m["sharpe"] is None else m["sharpe"])
                ret.append(m["net_return"]); ex.append(m["exposure"] or 0.0); nt.append(m["n_completed_trades"])
            sh, ret = np.array(sh), np.array(ret)
            raw[(tf, lvl)] = (sh, ret)
            rows.append({"exposure_pct": lvl, "actual_exposure": float(np.mean(ex)), "mean_trades": float(np.mean(nt)),
                         "mean_return": float(np.mean(ret)), "median_return": _q(ret, 0.5),
                         "p10_return": _q(ret, 0.1), "p90_return": _q(ret, 0.9),
                         "mean_sharpe": float(np.nanmean(sh)), "median_sharpe": _q(sh, 0.5),
                         "p10_sharpe": _q(sh, 0.1), "p90_sharpe": _q(sh, 0.9),
                         "frac_profitable": float(np.mean(ret > 0))})
        curves[tf] = rows
        typer.echo(f"{experiment_id} {tf}: {len(levels)} levels x {n_sims} sims")

    for f in fins:
        lvl = min(max(round(100 * (f["exposure"] or 0)), lo), hi)
        sh, ret = raw[(f["timeframe"], lvl)]
        f["exposure_level"] = lvl
        f["luck_pct_sharpe"] = None if f["sharpe"] is None else float(np.mean(np.nan_to_num(sh, nan=-np.inf) < f["sharpe"]))
        f["luck_pct_return"] = float(np.mean(ret < f["net_return"]))
    atomic_write_json(exp / "random_benchmark.json", {
        "experiment_id": experiment_id, "window": [str(v.start), str(v.end)], "n_sims": n_sims,
        "hold_bars": [hold_lo, hold_hi], "levels": levels, "curves": curves, "finalists": fins,
        "data_access": info,
        "method": ("Random long trades at uniformly random bars in the validation window, each held a random "
                   f"{hold_lo}-{hold_hi} bars and exited at the open, no overlap, covering the target share of "
                   "bars. Same fills, slippage, commission and whole-contract sizing as the strategy; scored with "
                   "the same daily-Sharpe and time-in-market code."),
    })
    typer.echo(f"wrote {exp / 'random_benchmark.json'}")


if __name__ == "__main__":
    app()
