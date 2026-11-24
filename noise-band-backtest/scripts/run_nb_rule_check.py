"""One frozen entry-rule change to a frozen noise-band pick, checked once on the holdout.

The rule and its pass criteria are written to a manifest BEFORE this runs (e.g.
runs/funnel/nb_nq_v2/holdout_selection_1_minext010.json). This script runs the base pick and
the pick + rule on the same continuous history (2018 -> holdout end), reports development /
validation / holdout metrics with the funnel's own metric code, and a luck test on the holdout:
random intraday entries at the variant's own time in market (src/experiments/nb_random_entry).
Reading holdout bars is logged in the access ledger.

  PYTHONPATH=. python scripts/run_nb_rule_check.py --confirm-holdout-access \\
      --manifest runs/funnel/nb_nq_v2/holdout_selection_1_minext010.json
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import typer

import scripts.run_nb_funnel as nbf
import src.strategies.noise_band.backtest as bt
from src.analysis.daily_performance import daily_equity, window_metrics
from src.data.aggregation import aggregate_bars
from src.experiments.data_access import DEFAULT_LEDGER, authorize_holdout_access, load_phase_bars, read_ledger
from src.experiments.funnel_config import load_execution_config, load_funnel_config
from src.experiments.funnel_prep import Job, _metric_kwargs, run_job
from scripts.build_nb_portfolio import _occupancy
from src.experiments.nb_random_entry import simulate_random_intraday
from src.utils.serialization import atomic_write_json

app = typer.Typer(add_completion=False)
KEEP = ("net_return", "cagr", "sharpe", "max_drawdown", "profit_factor", "win_rate", "exposure", "n_completed_trades")


def min_extension_patch(m: float):
    """Entry needs the close at least m x the band half-width beyond the band."""
    orig = bt.signal_arrays

    def sa(data, p):
        s = orig(data, p)
        half = p.band_mult * data.sigma(p.band_lookback) * data.raw_sess_open
        s["entry_l"] = s["entry_l"] & ((data.close - s["upper"]) >= m * half)
        s["entry_s"] = s["entry_s"] & ((s["lower"] - data.close) >= m * half)
        return s
    return orig, sa


@app.command()
def main(manifest: Path = typer.Option(..., exists=True),
         config: Path = typer.Option(Path("configs/funnel/nb_funnel_nq_v2.yaml")),
         n_sims: int = typer.Option(200),
         confirm_holdout_access: bool = typer.Option(False, "--confirm-holdout-access")) -> None:
    man = json.loads(manifest.read_text())
    if man["rule"]["name"] != "min_extension":
        raise typer.BadParameter(f"unknown rule {man['rule']['name']}")
    fcfg = load_funnel_config(config)
    nbf._select_space(fcfg)
    if fcfg.config_sha256() != man["config_sha256"]:
        raise typer.BadParameter("config changed since the base pick was frozen")
    p = nbf._params(man["params"])
    ec = load_execution_config(fcfg)
    prior = [e for e in read_ledger(DEFAULT_LEDGER) if e.get("phase") == "holdout" and e.get("symbol") == fcfg.symbol]
    auth = authorize_holdout_access(manifest_sha256=nbf._sha(man), confirm=confirm_holdout_access,
                                    command="rule_check")
    bars, info = load_phase_bars(fcfg, fcfg.symbol, "holdout", command="rule_check",
                                 experiment_id=man["experiment_id"], authorization=auth)
    data = bt.NBData(aggregate_bars(bars, timeframe=p.timeframe))
    dd, vv, hh = fcfg.data.development, fcfg.data.validation, fcfg.data.holdout
    end = date.fromisoformat(info["actual_last_session"])
    windows = {"development": (dd.start, dd.end), "validation": (vv.start, vv.end), "holdout": (hh.start, end)}
    orig, patched = min_extension_patch(float(man["rule"]["value"]))

    res, sims = {}, {}
    for label in ("base", "variant"):
        bt.signal_arrays = patched if label == "variant" else orig
        try:
            res[label] = {w: {k: run_job(Job(f"{label}|{w}", p, a, b), data, fcfg=fcfg, exec_config=ec)["metrics"][k]
                              for k in KEEP} for w, (a, b) in windows.items()}
            sims[label] = bt.simulate_noise_band(data, p, exec_config=ec, starting_equity=ec.starting_equity)
        finally:
            bt.signal_arrays = orig

    # holdout extras: daily returns by year, without the best day, and what the rule removed
    a, b = windows["holdout"]
    extra = {}
    for label, sim in sims.items():
        eq = daily_equity(sim, data, ec.starting_equity)
        m = (data.days >= np.datetime64(a)) & (data.days <= np.datetime64(b))
        prev = np.flatnonzero(m)[0] - 1
        e = eq[np.r_[prev, np.flatnonzero(m)]]
        r = np.diff(e) / e[:-1]
        yrs = data.days[m].astype("datetime64[Y]").astype(int) + 1970
        best = int(np.argmax(r))
        extra[label] = {"by_year": {int(y): float(np.prod(1 + r[yrs == y]) - 1) for y in np.unique(yrs)},
                        "best_day": [str(data.days[m][best]), float(r[best])],
                        "net_return_ex_best_day": float(np.prod(1 + np.delete(r, best)) - 1)}
    ent = lambda s: {(int(k), int(d)) for k, d in zip(s.signal_idx, s.side)}
    hmask = lambda s: (data.session_date[s.signal_idx] >= np.datetime64(a))
    base_h = {(int(k), int(d)): float(x / q) for k, d, x, q, h in zip(sims["base"].signal_idx, sims["base"].side,
              sims["base"].realized_pnl, sims["base"].quantity, hmask(sims["base"])) if h}
    var_h = ent(sims["variant"])
    removed = [v for k, v in base_h.items() if k not in var_h]
    extra["removed_holdout_trades"] = {"n": len(removed), "points": float(np.sum(removed)),
                                       "wins": int(np.sum(np.array(removed) > 0))}

    # luck: random intraday entries at the variant's holdout time in market
    sv = sims["variant"]
    win = (data.session_date >= np.datetime64(a)) & (data.session_date <= np.datetime64(b))
    exposure = float((_occupancy(sv, data) & win).sum() / win.sum())
    inw = data.session_date[sv.entry_idx] >= np.datetime64(a)
    pool = (sv.exit_idx[inw] - sv.entry_idx[inw] + 1).astype(np.int64)
    p_long = float(np.mean(sv.side[inw] > 0))
    rng = np.random.default_rng([fcfg.seed, 1, 10])
    rs, rr = [], []
    for _ in range(n_sims):
        rsim = simulate_random_intraday(data, fcfg.symbol, exec_config=ec, starting_equity=ec.starting_equity,
                                        window_start=a, window_end=b, exposure=exposure, length_pool=pool,
                                        p_long=p_long, rng=rng)
        req = daily_equity(rsim, data, ec.starting_equity)
        mm, _ = window_metrics(rsim, data, req, start=a, end=b, starting_equity=ec.starting_equity, **_metric_kwargs(fcfg))
        rs.append(mm["sharpe"] if mm["sharpe"] is not None else -np.inf); rr.append(mm["net_return"])
    vh = res["variant"]["holdout"]
    luck = {"n_sims": n_sims, "exposure": exposure, "pct_sharpe": float(np.mean(np.array(rs) < vh["sharpe"])),
            "pct_return": float(np.mean(np.array(rr) < vh["net_return"])),
            "random_mean_sharpe": float(np.mean([x for x in rs if np.isfinite(x)]))}

    bh = res["base"]["holdout"]
    checks = {"sharpe_ge_base": vh["sharpe"] >= bh["sharpe"],
              "pf_ge_base": vh["profit_factor"] >= bh["profit_factor"],
              "acceptance": vh["net_return"] > 0 and vh["sharpe"] >= 0}
    out = {"manifest": str(manifest), "manifest_sha256": nbf._sha(man), "experiment_id": man["experiment_id"],
           "rule": man["rule"], "windows": {k: [str(x), str(y)] for k, (x, y) in windows.items()},
           "data_access": info, "prior_holdout_accesses_for_symbol": len(prior),
           "label": "holdout previously inspected for this pick -- NOT an untouched test",
           "results": res, "holdout_extra": extra, "luck_variant_holdout": luck,
           "preregistered_checks": checks, "passed": all(checks.values())}
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = manifest.parent / f"rule_check_results_{stamp}.json"
    atomic_write_json(dest, out)
    typer.echo(json.dumps({k: out[k] for k in ("results", "holdout_extra", "luck_variant_holdout",
                                                 "preregistered_checks", "passed")}, indent=1, default=str))
    typer.echo(f"-> {dest}")


if __name__ == "__main__":
    app()
