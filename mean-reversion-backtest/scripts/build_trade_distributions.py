"""Per-trade % returns of every chosen strategy, 2018 .. validation end vs the holdout.

Each strategy runs alone with its frozen funnel settings (full contracts, baseline
costs, $1M). A trade's return is its net P&L (after commissions and slippage) divided
by the contract value it bought at entry (raw, un-back-adjusted price x multiplier x
contracts), so it does not depend on account size or on the combined account's caps.
Force-closed trades (still open when the data ends) are left out.

The holdout is read through the same authorization as the other holdout scripts and
ledgered per market as `trade_distribution` (diagnostic only, no selection).

Each trade also records the previous trade's exit reason and the bar gap from that exit
bar to this entry (1 = the signal formed on the bar the last trade ended), for the
back-to-back re-entry analysis.

Writes futures-results/data/ALL/trades_v1.json, trades.html and reentries.html
(futures-results/<page>_template.html with the data inlined).

Usage:
  PYTHONPATH=. python scripts/build_trade_distributions.py --confirm-holdout-access
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import typer

from scripts.build_combined_portfolio import DEFAULT_LEGS
from src.data.aggregation import aggregate_bars
from src.experiments.data_access import load_phase_bars
from src.experiments.funnel_config import load_funnel_config
from src.strategies.mean_reversion.backtest import MRData, simulate_mean_reversion

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = PROJECT_ROOT.parent / "futures-results"
app = typer.Typer(add_completion=False)


NY = ZoneInfo("America/New_York")


def _ny(t) -> str:
    """Bar-open time in New York, e.g. 2025-04-04 10:30."""
    return (t.astimezone(NY) if getattr(t, "tzinfo", None) else t).strftime("%Y-%m-%d %H:%M")


def _trades(sim, d: MRData, s64, e64) -> list[dict]:
    out = []
    for k in range(len(sim.entry_idx)):
        a, b = int(sim.entry_idx[k]), int(sim.exit_idx[k])
        day = d.session_date[a]
        if sim.forced_close[k] or not (s64 <= day <= e64):
            continue
        raw = sim.entry_px[k] - d.price_adj[a]
        # Link to the previous trade (even one entered before the window): how it ended and how
        # many bars after its exit bar this one entered (1 = signal on the bar the last trade ended).
        prev = str(sim.exit_reason[k - 1]) if k else None
        gap = a - int(sim.exit_idx[k - 1]) if k else None
        out.append({"r": round(float(sim.realized_pnl[k] / (sim.quantity[k] * raw)) * 100, 4),
                    "pnl": round(float(sim.realized_pnl[k]), 2), "d": str(day), "x": str(sim.exit_reason[k]),
                    "bars": b - a, "px": round(float(raw), 4),
                    "et": _ny(d.ts[a]), "xt": _ny(d.ts[b]), "prev": prev, "gap": gap})
    return out


@app.command()
def main(
    leg: list[str] = typer.Option(DEFAULT_LEGS, help="RUN:ORDER (repeat)"),
    confirm_holdout_access: bool = typer.Option(False, "--confirm-holdout-access"),
    runs_root: Path = typer.Option(PROJECT_ROOT / "runs" / "funnel"),
) -> None:
    from scripts.run_mr_funnel import _params, _select_space, _sha, load_execution_config
    from src.experiments.data_access import authorize_holdout_access

    specs = []
    for spec in leg:
        run_id, order = spec.split(":")
        cfg_path = PROJECT_ROOT / "configs" / "funnel" / f"mr_funnel_{run_id.removeprefix('mr_')}.yaml"
        fc = load_funnel_config(cfg_path)
        _select_space(fc)
        cands = {c["dev_order"]: c for c in json.loads((runs_root / run_id / "frozen_representatives.json").read_text())["candidates"]}
        c = cands[int(order)]
        sel = json.loads((runs_root / run_id / "selection_manifest.json").read_text())
        if fc.config_sha256() != sel["config_sha256"]:
            raise typer.BadParameter(f"{run_id}: config changed since the manifest was frozen.")
        specs.append({"run": run_id, "fcfg": fc, "order": c["dev_order"], "sym": fc.symbol, "settings": c["params"],
                      "params": _params(c["params"]), "tf": c["params"]["timeframe"], "sha": _sha(sel)})
    base = specs[0]["fcfg"]
    ec = load_execution_config(base)
    syms = list(dict.fromkeys(sp["sym"] for sp in specs))

    bars = {"is": {}, "ho": {}}
    for s in syms:
        fc = next(sp["fcfg"] for sp in specs if sp["sym"] == s)
        bars["is"][s], _ = load_phase_bars(fc, s, "validation", command="trade_distribution", experiment_id="trades_v1")
        shas = "".join(dict.fromkeys(sp["sha"] for sp in specs if sp["sym"] == s))
        auth = authorize_holdout_access(manifest_sha256=hashlib.sha256(shas.encode()).hexdigest(),
                                        confirm=confirm_holdout_access, command="trade_distribution")
        bars["ho"][s], _ = load_phase_bars(fc, s, "holdout", command="trade_distribution", experiment_id="trades_v1",
                                           authorization=auth)
    windows = {"is": (base.data.development.start, base.data.validation.end),
               "ho": (base.data.holdout.start, None)}  # None: to the end of the data

    out, last = [], None
    for sp in specs:
        row = {"name": f"{sp['sym']} {sp['tf'].replace('min', 'm')} #{sp['order']}", "market": sp["sym"],
               "run_id": sp["run"], "order": sp["order"], "timeframe": sp["tf"], "settings": sp["settings"]}
        for k, (s, e) in windows.items():
            d = MRData(aggregate_bars(bars[k][sp["sym"]], timeframe=sp["tf"]))
            sim = simulate_mean_reversion(d, sp["params"], exec_config=ec, starting_equity=1e6)
            row[k] = _trades(sim, d, np.datetime64(s, "D"), d.days[-1] if e is None else np.datetime64(e, "D"))
            if e is None:
                last = d.days[-1] if last is None else max(last, d.days[-1])
        out.append(row)
        print(f"{row['name']:16s} 2018-24 {len(row['is']):4d} trades  holdout {len(row['ho']):4d}")

    doc = {"generated_at": datetime.now(timezone.utc).isoformat(),
           "periods": {"is": f"{windows['is'][0]} to {windows['is'][1]}", "ho": f"{windows['ho'][0]} to {last}"},
           "costs": "baseline futures costs: $2.50/contract/side + 1 tick slippage/side",
           "strategies": out}
    js = SITE_ROOT / "data" / "ALL" / "trades_v1.json"
    js.write_text(json.dumps(doc, separators=(",", ":")))
    blob = json.dumps(doc, separators=(",", ":"))
    for page in ("trades", "reentries"):
        tpl = (SITE_ROOT / f"{page}_template.html").read_text()
        (SITE_ROOT / f"{page}.html").write_text(tpl.replace("/*__DATA__*/null", blob))
    print(f"wrote {js}, {SITE_ROOT / 'trades.html'} and {SITE_ROOT / 'reentries.html'}")


if __name__ == "__main__":
    app()
