"""Run frozen price-path-convexity settings on other markets over 2018 to the data end, year by year.

No retuning: the settings of a frozen candidate are used unchanged on each market (only the symbol,
and therefore the contract spec and costs, change). Reads the holdout bars of every market, so it
needs --confirm-holdout-access and is logged (command: pc_transfer_allyears).

  PYTHONPATH=. .venv/bin/python scripts/run_pc_transfer_allyears.py --experiment-id pc_nq_v5_15m \
      --config configs/funnel/pc_funnel_nq_v5_15m.yaml --manifest runs/funnel/pc_nq_v5_15m/holdout_selection_46_36_21.json \
      --dev-order 46 --symbols NQ,ES,RTY,YM --out OUT.json --confirm-holdout-access
"""
from __future__ import annotations

import json
from pathlib import Path

import typer

from scripts.run_pc_funnel import PROJECT_ROOT, _frames, _params, _select_space, _sha
from src.analysis.daily_performance import daily_equity, window_metrics
from src.experiments.data_access import authorize_holdout_access
from src.experiments.funnel_config import load_execution_config, load_funnel_config
from src.experiments.funnel_prep import _metric_kwargs
from src.strategies.path_convexity.backtest import PCData, simulate_path_convexity

app = typer.Typer(add_completion=False)
KEEP = ("net_return", "sharpe", "max_drawdown", "profit_factor", "n_completed_trades", "win_rate")


@app.command()
def main(experiment_id: str = typer.Option(...), config: Path = typer.Option(...), manifest: Path = typer.Option(...),
         dev_order: int = typer.Option(...), symbols: str = typer.Option("NQ,ES,RTY,YM"), out: Path = typer.Option(...),
         confirm_holdout_access: bool = typer.Option(False)) -> None:
    sel = json.loads(manifest.read_text())
    auth = authorize_holdout_access(manifest_sha256=_sha(sel), confirm=confirm_holdout_access, command="pc_transfer_allyears")
    fcfg = load_funnel_config(config)
    _select_space(fcfg)
    ec = load_execution_config(fcfg)
    cand = next(c for c in sel["candidates"] if c["dev_order"] == dev_order)
    res = {"experiment_id": experiment_id, "dev_order": dev_order, "settings": cand["params"], "markets": {}}
    for sym in symbols.split(","):
        frames, info = _frames(fcfg, sym, "holdout", command="pc_transfer_allyears", experiment_id=experiment_id,
                               authorization=auth)
        data = PCData(frames[f"{sym}|15min"])
        p = _params({**cand["params"], "symbol": sym})
        sim = simulate_path_convexity(data, p, exec_config=ec, starting_equity=ec.starting_equity)
        eq = daily_equity(sim, data, ec.starting_equity)
        end = info["actual_last_session"]
        wins = {str(y): (f"{y}-01-01", f"{y}-12-31" if y < 2026 else end) for y in range(2018, 2027)}
        wins |= {"dev 2018-22": ("2018-01-01", "2022-12-31"), "val 2023-24": ("2023-01-01", "2024-12-31"),
                 "holdout 2025+": ("2025-01-01", end), "all": ("2018-01-01", end)}
        rows = {}
        for k, (a, b) in wins.items():
            m, _ = window_metrics(sim, data, eq, start=a, end=b, starting_equity=ec.starting_equity, **_metric_kwargs(fcfg))
            rows[k] = {x: (float(m[x]) if m[x] is not None else None) for x in KEEP}
        res["markets"][sym] = {"end": end, "windows": rows}
        a = rows["all"]
        typer.echo(f"{sym} #{dev_order}: all sharpe {a['sharpe']:.2f} ret {a['net_return']:+.3f} pf {a['profit_factor']:.2f} n {int(a['n_completed_trades'])}")
    out.write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    app()
