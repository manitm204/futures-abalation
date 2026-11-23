"""Random-entry ("luck") benchmark for an FVG funnel run's validation finalists.

The question is whether the SIGNAL matters (the gap: which bar to trade, and which way). So each
finalist keeps everything else: its window, fill kind (limit / stop order / market, so the same
costs), stop rule, target and hold. The gap is replaced by a random bar. Each random run:
  - picks as many validation-window sessions as the finalist traded (one trade a session);
  - on each one, picks a random 1-minute bar m inside the window (bars m-2..m+1 contiguous and in
    the window, like a gap's three bars plus the entry bar);
  - goes long or short by a fair coin at the next bar's open;
  - places the stop and target from the same rule (struct uses bars m-2..m; ATR at bar m-2), with
    a fresh random bar if a struct stop lands on the wrong side;
  - exits on the stop, the target or after `hold` minutes (by 16:00), as the strategy does.
`luck_pct_sharpe` is the share of a finalist's random runs whose validation Sharpe it beat
(likewise for return). ~50% = no better than random bars and coin-flip direction.

For the page's chart, finalists are grouped by window; each finalist's random runs sit at its own
time in market (0.1% steps), merged when two finalists share a step.

The finalists are re-run on validation first and must reproduce validation_results.json exactly.
Validation data only (the window `validate` already used); logged to the data-access ledger as
command `random_benchmark`. Output: runs/funnel/<experiment>/random_benchmark.json.

Usage:
  PYTHONPATH=. python scripts/run_fv_random_benchmark.py --experiment-id fv_nq_v1 \\
      --config configs/funnel/fv_funnel_nq_v1.yaml
"""

from __future__ import annotations

import json
import zlib
from pathlib import Path

import numpy as np
import typer

from scripts.run_fv_funnel import _frames, _params, _select_space
from src.analysis.daily_performance import daily_equity, window_metrics
from src.strategies.mean_reversion.backtest import CostModel
from src.experiments.funnel_config import load_execution_config, load_funnel_config
from src.experiments.funnel_prep import _metric_kwargs
from src.strategies.fvg.backtest import (MAX_ENTRY_GAP_MIN, FVData, exit_bar, simulate_fvg,
                                         stop_and_target)
from src.strategies.fvg.config import WINDOWS
from src.utils.serialization import atomic_write_json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
app = typer.Typer(add_completion=False)
WIN_LABEL = {"am": "09:45–12:00", "pm": "12:00–15:30", "rth": "09:45–15:30"}


def _q(a: np.ndarray, q: float) -> float | None:
    a = a[np.isfinite(a)]
    return float(np.quantile(a, q)) if len(a) else None


def _kind(prm: dict) -> int:
    if prm["entry"] == "mkt":
        return 2
    return 0 if prm["mode"] == "with" else 1


def _candidates(data: FVData, window: str, in_win: np.ndarray) -> dict[int, np.ndarray]:
    """Bars m that can stand in for a gap's third bar: m-2..m contiguous, all in the window, the
    entry bar m+1 in the window and the same session, ATR known, session in the validation window."""
    a, b = WINDOWS[window]
    m = np.arange(2, data.n - 1)
    ok = ((data.sess[m - 2] == data.sess[m + 1]) & (data.minute[m] - data.minute[m - 2] == 2)
          & (data.tod[m - 2] >= a) & (data.tod[m] < b) & (data.tod[m + 1] < b) & (data.tod[m] >= data.tod[m - 2])
          & (data.minute[m + 1] - data.minute[m] <= MAX_ENTRY_GAP_MIN) & np.isfinite(data.atr[m - 2])
          & in_win[data.sess[m]])
    m = m[ok]
    s = data.sess[m]
    cuts = np.flatnonzero(np.diff(s)) + 1
    return {int(g[0]): g_m for g, g_m in zip(np.split(s, cuts), np.split(m, cuts)) if len(g)}


def _random_plan(data: FVData, p, kind: int, cand: dict[int, np.ndarray], n_tr: int, tick: float,
                 rng: np.random.Generator) -> dict[str, np.ndarray]:
    sess = np.array(sorted(cand))
    pick = np.sort(rng.choice(sess, size=min(n_tr, len(sess)), replace=False))
    rows = []
    for s_id in pick.tolist():
        bars = cand[s_id]
        for _ in range(20):
            mi = int(bars[rng.integers(len(bars))])
            sd = 1 if rng.random() < 0.5 else -1
            e = mi + 1
            base = float(data.open[e])
            lo3 = float(data.low[mi - 2:mi + 1].min())
            hi3 = float(data.high[mi - 2:mi + 1].max())
            sl = stop_and_target(p, base, sd, lo3, hi3, float(data.atr[mi - 2]), tick)
            if sl is not None:
                rows.append((mi, e, exit_bar(data, e, p.hold), sd, base, kind, sl[0], sl[1]))
                break
    cols = list(zip(*rows)) if rows else [()] * 8
    i64, f64 = (lambda v: np.asarray(v, dtype=np.int64)), (lambda v: np.asarray(v, dtype=float))
    return {"m": i64(cols[0]), "e": i64(cols[1]), "x": i64(cols[2]), "side": i64(cols[3]), "base": f64(cols[4]),
            "kind": i64(cols[5]), "stop": f64(cols[6]), "tgt": f64(cols[7])}


@app.command()
def main(
    experiment_id: str = typer.Option(...),
    config: Path = typer.Option(...),
    n_sims: int = typer.Option(200, help="Random runs per finalist"),
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
    data = FVData(frames[f"{fcfg.symbol}|1min"])
    tick = CostModel.for_symbol(ec, fcfg.symbol).tick
    s64, e64 = np.datetime64(v.start, "D"), np.datetime64(v.end, "D")
    sess_ids, first = np.unique(data.sess, return_index=True)
    assert (sess_ids == np.arange(len(sess_ids))).all()
    sess_day = data.session_date[first]
    in_win = (sess_day >= s64) & (sess_day <= e64)
    cands = {w: _candidates(data, w, in_win) for w in WINDOWS}

    def _score(sim):
        m, _ = window_metrics(sim, data, daily_equity(sim, data, eq0), start=v.start, end=v.end,
                              starting_equity=eq0, **mk)
        return m

    fins, sims_at, pool = [], {}, {}
    for r in val.get("results", []):
        prm = params_of[r["config_id"]]
        p = _params(prm)
        sim = simulate_fvg(data, p, exec_config=ec, starting_equity=eq0)
        m = _score(sim)
        for k in ("sharpe", "net_return", "exposure", "n_completed_trades"):
            if m[k] != r["metrics"][k]:
                raise RuntimeError(f"{r['config_id']}: re-run {k} {m[k]} != validation {r['metrics'][k]}")
        inwin = (data.session_date[sim.entry_idx] >= s64) & (data.session_date[sim.entry_idx] <= e64)
        n_tr = int(inwin.sum())
        rng = np.random.default_rng([fcfg.seed, zlib.crc32(r["config_id"].encode())])
        sh, ret, ex, nt = [], [], [], []
        lens, longs = pool.setdefault(prm["window"], ([], []))
        for _ in range(n_sims):
            plan = _random_plan(data, p, _kind(prm), cands[prm["window"]], n_tr, tick, rng)
            rs = simulate_fvg(data, p, exec_config=ec, starting_equity=eq0, plan=plan)
            rm = _score(rs)
            sh.append(np.nan if rm["sharpe"] is None else rm["sharpe"])
            ret.append(rm["net_return"]); ex.append(rm["exposure"] or 0.0); nt.append(rm["n_completed_trades"])
            lens.extend((rs.exit_idx - rs.entry_idx + 1).tolist()); longs.extend((rs.side > 0).tolist())
        sh, ret = np.array(sh), np.array(ret)
        lvl = round(100 * (m["exposure"] or 0.0), 1)
        acc = sims_at.setdefault((prm["window"], lvl), [[], [], [], []])
        for lst, x in zip(acc, (sh, ret, ex, nt)):
            lst.extend(list(x))
        fins.append({
            "config_id": r["config_id"], "dev_order": r["dev_order"], "status": r["status"],
            "group": prm["window"], "n_trades": n_tr,
            **{k: r["metrics"][k] for k in ("exposure", "net_return", "sharpe")},
            "exposure_level": lvl, "random_mean_exposure": float(np.mean(ex)),
            "random_median_sharpe": _q(sh, 0.5), "random_mean_trades": float(np.mean(nt)),
            "luck_pct_sharpe": None if m["sharpe"] is None
            else float(np.mean(np.nan_to_num(sh, nan=-np.inf) < m["sharpe"])),
            "luck_pct_return": float(np.mean(ret < m["net_return"])),
        })
        f = fins[-1]
        typer.echo(f"#{r['dev_order']:>3} {prm['window']:>3} {prm['mode']:>7} {prm['entry']:>4} {r['status']:>4}: "
                   f"Sharpe {m['sharpe']:+.2f} vs random median {f['random_median_sharpe']:+.2f} -> beats "
                   f"{f['luck_pct_sharpe']:.0%}")

    curves, levels_of, meta = {}, {}, {}
    for w in WINDOWS:
        lv = sorted(l for (ww, l) in sims_at if ww == w)
        if not lv:
            continue
        rows = []
        for l in lv:
            sh, ret, ex, nt = (np.asarray(x, dtype=float) for x in sims_at[(w, l)])
            rows.append({"exposure_pct": l, "actual_exposure": float(np.mean(ex)), "mean_trades": float(np.mean(nt)),
                         "mean_return": float(np.mean(ret)), "median_return": _q(ret, 0.5),
                         "p10_return": _q(ret, 0.1), "p90_return": _q(ret, 0.9),
                         "mean_sharpe": float(np.nanmean(sh)), "median_sharpe": _q(sh, 0.5),
                         "p10_sharpe": _q(sh, 0.1), "p90_sharpe": _q(sh, 0.9),
                         "frac_profitable": float(np.mean(ret > 0))})
        curves[w], levels_of[w] = rows, lv
        lens = np.asarray(pool[w][0])
        meta[w] = {"label": WIN_LABEL[w], "p_long": float(np.mean(pool[w][1])),
                   "median_trade_bars": float(np.median(lens)), "mean_trade_bars": float(np.mean(lens))}
    atomic_write_json(exp / "random_benchmark.json", {
        "experiment_id": experiment_id, "window": [str(v.start), str(v.end)], "n_sims": n_sims,
        "levels": sorted({x for lv in levels_of.values() for x in lv}), "groups": meta, "group_levels": levels_of,
        "curves": curves, "finalists": fins, "data_access": info,
        "method": ("Per finalist: the same window, fill kind, stop rule, target and hold, and as many trades, but "
                   "each on a random validation-window session at a random bar in the window, long or short by a "
                   "fair coin. Same fills, slippage, commission and whole-contract sizing as the strategy; scored "
                   "with the same daily-Sharpe and time-in-market code."),
    })
    typer.echo(f"wrote {exp / 'random_benchmark.json'}")


if __name__ == "__main__":
    app()
