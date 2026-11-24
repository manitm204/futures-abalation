"""Re-run frozen wick-entry picks with both-edges bars settled on 1-minute bars.

A wick entry is a stop order resting at a box edge. When one 15-minute bar trades through BOTH
edges, the 15-minute backtest cannot tell which filled first, so it skips the setup -- and those
are mostly losing trades in real life (the order fills, then the far side stops it out). This
script runs each frozen pick twice on the same data, with nothing re-chosen:

  original  : the published engine (both-edges bars skipped)
  minute    : CBData.attach_minutes -- the bar's own 1-minute bars decide which edge broke
              first; the trade is taken if the strategy's filters allow that side, and the rest
              of the entry bar is walked minute by minute (stop before target). Both edges in a
              single minute: the strategy's side is assumed and checked against its stop.

Every window (development, validation, holdout) comes from one continuous simulation, exactly
like the funnel's final-test. Reading holdout bars is logged in the access ledger.

  PYTHONPATH=. python scripts/run_cb_minute_resolve.py --confirm-holdout-access \\
      --pick configs/funnel/cb_nr_funnel_nq_v4_15m.yaml:runs/funnel/cb_nr_nq_v4_15m/holdout_selection_29_47.json:29
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import typer

import scripts.run_cb_funnel as cbf
from src.data.aggregation import aggregate_bars
from src.experiments.data_access import authorize_holdout_access, load_phase_bars, read_ledger, DEFAULT_LEDGER
from src.experiments.funnel_config import load_funnel_config
from src.experiments.funnel_prep import Job, run_job
from src.strategies.compression_breakout.backtest import CBData, setups
from src.utils.serialization import atomic_write_json

app = typer.Typer(add_completion=False)
KEEP = ("net_return", "cagr", "sharpe", "max_drawdown", "profit_factor", "win_rate", "exposure",
        "n_completed_trades", "n_profitable_years")


def _both_edges_stats(data: CBData, sim_new, p, windows: dict) -> dict:
    """What the 1-minute settling found, per window: setups that broke both edges, which side
    broke first, how many became trades and what those trades made."""
    st = setups(data, p)
    k = st["k"]
    both = st["first_min"] >= 0
    traded_new = set(int(x) for x in sim_new.signal_idx)
    out = {}
    for name, (a, b) in windows.items():
        d = data.session_date[k]
        w = both & (d >= np.datetime64(a)) & (d <= np.datetime64(b))
        tw = np.array([int(x) in traded_new for x in k[w]], dtype=bool)
        sd = data.session_date[sim_new.signal_idx] if len(sim_new.signal_idx) else np.array([], "datetime64[D]")
        inw = (sd >= np.datetime64(a)) & (sd <= np.datetime64(b))
        both_sig = set(int(x) for x in k[both])
        is_b = np.array([int(x) in both_sig for x in sim_new.signal_idx], dtype=bool)
        sel = inw & is_b
        pnl = sim_new.realized_pnl[sel]
        out[name] = {
            "both_edge_setups": int(w.sum()),
            "up_first": int(((st["side"] > 0) & ~st["same_min"] & w).sum()),
            "down_first": int(((st["side"] < 0) & ~st["same_min"] & w).sum()),
            "same_minute": int(st["same_min"][w].sum()),
            "now_traded": int(tw.sum()),
            "trades": int(sel.sum()),
            "wins": int((pnl > 0).sum()),
            "stopped_on_entry_bar": int(((sim_new.exit_reason[sel] == "stop_exit")
                                         & (sim_new.exit_idx[sel] == sim_new.entry_idx[sel])).sum()),
            "pnl": float(pnl.sum()),
        }
    return out


@app.command()
def main(
    pick: list[str] = typer.Option(..., help="funnel_yaml:selection_manifest:dev_order (repeatable)"),
    confirm_holdout_access: bool = typer.Option(False, "--confirm-holdout-access"),
) -> None:
    for spec in pick:
        cfg_path, man_path, order = spec.split(":")
        order = int(order)
        sel = json.loads(Path(man_path).read_text())
        fcfg = load_funnel_config(Path(cfg_path))
        cbf._select_space(fcfg)
        if fcfg.config_sha256() != sel["config_sha256"]:
            raise typer.BadParameter(f"{cfg_path}: config changed since {man_path} was frozen.")
        cand = next(c for c in sel["candidates"] if c["dev_order"] == order)
        p = cbf._params(cand["params"])
        ec = cbf.load_execution_config(fcfg)
        prior = [e for e in read_ledger(DEFAULT_LEDGER) if e.get("phase") == "holdout" and e.get("symbol") == fcfg.symbol]
        exp = f"{sel['experiment_id']}#{order} 1min both-edges check"
        auth = authorize_holdout_access(manifest_sha256=cbf._sha(sel), confirm=confirm_holdout_access,
                                        command="minute_resolve_check")
        bars, info = load_phase_bars(fcfg, fcfg.symbol, "holdout", command="minute_resolve_check",
                                     experiment_id=exp, authorization=auth)
        f15 = aggregate_bars(bars, timeframe=p.timeframe)
        orig = CBData(f15)
        mins = CBData(f15)
        mins.attach_minutes(bars)
        dd, vv, hh = fcfg.data.development, fcfg.data.validation, fcfg.data.holdout
        end = date.fromisoformat(info["actual_last_session"])
        windows = {"development": (dd.start, dd.end), "validation": (vv.start, vv.end), "holdout": (hh.start, end)}
        res: dict = {"original": {}, "minute": {}}
        for label, data in (("original", orig), ("minute", mins)):
            for w, (a, b) in windows.items():
                r = run_job(Job(f"{label}|{w}", p, a, b), data, fcfg=fcfg, exec_config=ec)
                res[label][w] = {**{k: r["metrics"][k] for k in KEEP}, "integrity_issues": r["integrity_issues"]}
        from src.strategies.compression_breakout.backtest import simulate_compression_breakout
        sim_new = simulate_compression_breakout(mins, p, exec_config=ec, starting_equity=ec.starting_equity)
        both = _both_edges_stats(mins, sim_new, p, windows)
        out = {"experiment_id": sel["experiment_id"], "dev_order": order, "config_id": cand["config_id"],
               "symbol": fcfg.symbol, "params": cand["params"], "windows": {k: [str(a), str(b)] for k, (a, b) in windows.items()},
               "data_access": info, "prior_holdout_accesses_for_symbol": len(prior),
               "label": "holdout previously inspected -- NOT an untouched test (frozen pick re-run, nothing re-chosen)",
               "method": __doc__.split("\n\n")[1], "results": res, "both_edge_setups": both}
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        dest = Path(man_path).parent / f"minute_resolve_{order}_{stamp}.json"
        atomic_write_json(dest, out)
        typer.echo(f"== {fcfg.symbol} #{order} -> {dest}")
        for w in windows:
            o, m = res["original"][w], res["minute"][w]
            typer.echo(f"  {w:<11} sharpe {o['sharpe']:6.2f} -> {m['sharpe']:6.2f} | cagr {o['cagr']:7.2%} -> {m['cagr']:7.2%}"
                       f" | dd {o['max_drawdown']:7.2%} -> {m['max_drawdown']:7.2%} | pf {o['profit_factor']:.2f} -> {m['profit_factor']:.2f}"
                       f" | trades {o['n_completed_trades']} -> {m['n_completed_trades']} | integrity {len(m['integrity_issues'])}")
            typer.echo(f"              both-edge: {both[w]}")


if __name__ == "__main__":
    app()
