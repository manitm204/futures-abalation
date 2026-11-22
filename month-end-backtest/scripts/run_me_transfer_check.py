"""Frozen picks, unchanged rules, on another market: development, validation and holdout.

A no-search robustness check. Takes a frozen holdout selection manifest (e.g.
runs/funnel/me_es_v2/selection_manifest_1_7_17.json), swaps only the symbol, and scores every
pick on the other market's development (2018-2022), validation (2023-2024) and holdout (2025+)
windows with the same costs, sizing and metric code. No parameter is re-chosen and no pick is
re-ranked. The holdout needs --confirm-holdout-access and goes through
`authorize_holdout_access` (manifest hash); every access is ledgered (command
`transfer_check`). Acceptance per window uses the YAML's validation / holdout rules.

Output: runs/funnel/<experiment>/transfer_check_<SYMBOL>_<stamp>.json

Usage:
  PYTHONPATH=. python scripts/run_me_transfer_check.py --manifest runs/funnel/me_es_v2/selection_manifest_1_7_17.json \
      --config configs/funnel/me_funnel_es_v2.yaml --symbol RTY --confirm-holdout-access
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path

import typer

from scripts.run_me_funnel import _frames, _params, _select_space, _sha
from src.experiments.data_access import authorize_holdout_access, read_ledger, DEFAULT_LEDGER
from src.experiments.funnel_config import load_execution_config, load_funnel_config
from src.experiments.funnel_prep import Job, run_jobs
from src.utils.serialization import atomic_write_json

app = typer.Typer(add_completion=False)


def _ok(m: dict, acc) -> bool:
    return (m["net_return"] > acc.min_net_return and m["sharpe"] is not None and m["sharpe"] >= acc.min_sharpe
            and (acc.max_drawdown is None or m["max_drawdown"] >= acc.max_drawdown)
            and (acc.min_completed_trades is None or m["n_completed_trades"] >= acc.min_completed_trades))


@app.command()
def main(
    manifest: Path = typer.Option(..., exists=True),
    config: Path = typer.Option(...),
    symbol: str = typer.Option(...),
    confirm_holdout_access: bool = typer.Option(False, "--confirm-holdout-access"),
) -> None:
    sel = json.loads(manifest.read_text())
    sel_sha = _sha(sel)
    fcfg = load_funnel_config(config)
    _select_space(fcfg)
    if fcfg.config_sha256() != sel["config_sha256"]:
        raise typer.BadParameter("Config changed since the manifest was frozen.")
    if symbol == fcfg.symbol:
        raise typer.BadParameter("Pick a different market than the one the picks were chosen on.")
    ec = load_execution_config(fcfg)
    auth = authorize_holdout_access(manifest_sha256=sel_sha, confirm=confirm_holdout_access, command="transfer_check")
    prior = [e for e in read_ledger(DEFAULT_LEDGER) if e.get("phase") == "holdout" and e.get("symbol") == symbol]
    exp = sel["experiment_id"]
    windows = {}
    for phase, w in (("development", fcfg.data.development), ("validation", fcfg.data.validation),
                     ("holdout", fcfg.data.holdout)):
        frames, info = _frames(fcfg, symbol, phase, command="transfer_check", experiment_id=f"{exp} -> {symbol}",
                               authorization=auth if phase == "holdout" else None)
        end = date.fromisoformat(info["actual_last_session"]) if phase == "holdout" else w.end
        jobs = [Job(c["config_id"], _params(c["params"], symbol), w.start, end) for c in sel["candidates"]]
        res = run_jobs(jobs, frames, fcfg=fcfg, exec_config=ec, n_workers=1)
        acc = {"development": fcfg.performance, "validation": fcfg.validation, "holdout": fcfg.holdout.acceptance}[phase]
        windows[phase] = {"window": [str(w.start), str(end)], "data_access": info, "results": [
            {"dev_order": c["dev_order"], "config_id": c["config_id"], "metrics": res[c["config_id"]]["metrics"],
             "integrity_issues": res[c["config_id"]]["integrity_issues"],
             "accepted": None if phase == "development" else _ok(res[c["config_id"]]["metrics"], acc)}
            for c in sel["candidates"]]}
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = {"manifest": str(manifest), "manifest_sha256": sel_sha, "source_symbol": fcfg.symbol, "symbol": symbol,
           "prior_holdout_accesses_for_symbol": len(prior),
           "note": "Frozen picks with unchanged rules; only the symbol is swapped. Nothing re-chosen or re-ranked.",
           "windows": windows}
    path = manifest.parent / f"transfer_check_{symbol}_{stamp}.json"
    atomic_write_json(path, out)
    typer.echo(f"wrote {path}")
    for phase, wd in windows.items():
        for r in wd["results"]:
            m = r["metrics"]
            typer.echo(f"{symbol} {phase:11s} #{r['dev_order']:<3d} ret {m['net_return']:+.2%} Sharpe "
                       f"{m['sharpe'] if m['sharpe'] is None else round(m['sharpe'], 2)} PF "
                       f"{m['profit_factor'] if m['profit_factor'] is None else round(m['profit_factor'], 2)} "
                       f"DD {m['max_drawdown']:.1%} trades {m['n_completed_trades']} accepted {r['accepted']}"
                       f"{' ISSUES ' + ';'.join(r['integrity_issues']) if r['integrity_issues'] else ''}")


if __name__ == "__main__":
    app()
