"""Equal-weight SPY portfolio of the #1 strategy from each family's latest funnel.

Sleeves (configs/portfolio/portfolio_v1.yaml): candidates[0] of the mean-reversion
v2, RSI-divergence v3 and MA-crossover v2 selection manifests. Each sleeve is
simulated exactly as its funnel did; the portfolio splits capital equally on the
window's first day and never rebalances. SPY buy-and-hold over the same days is
the benchmark.

Usage:
  PYTHONPATH=. .venv/bin/python scripts/run_portfolio.py --window validation
  PYTHONPATH=. .venv/bin/python scripts/run_portfolio.py --window holdout --confirm-holdout-access

`validation` (2023-2024) was used to pick the sleeves, so it is in-sample context.
`holdout` (2025+) is the out-of-sample test; reading it is ledgered.
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import polars as pl
import typer

from src.data.aggregation import aggregate_bars
from src.experiments.data_access import (
    append_ledger,
    authorize_holdout_access,
    load_phase_bars,
    read_ledger,
)
from src.experiments.funnel_config import PROJECT_ROOT
from src.portfolio.metrics import (
    combine_sleeves,
    equity_curve,
    interval_mask,
    monthly_returns,
    relative_to_benchmark,
    series_metrics,
)
from src.portfolio.sleeves import load_portfolio_config, load_sleeve, sha, simulate_sleeve, trade_stats
from src.utils.logging import configure_logging
from src.utils.serialization import atomic_write_json

app = typer.Typer(add_completion=False)
OUT_ROOT = PROJECT_ROOT / "runs" / "portfolio"
LEDGER = OUT_ROOT / "data_access_ledger.jsonl"
DEFAULT_CONFIG = PROJECT_ROOT / "configs" / "portfolio" / "portfolio_v1.yaml"
GRID_TF = "5min"  # common grid for portfolio-level time in market


def _pct(x, nd=1):
    return "n/a" if x is None else f"{100 * x:.{nd}f}%"


def _num(x, nd=2):
    return "n/a" if x is None else f"{x:.{nd}f}"


@app.command()
def main(
    window: str = typer.Option("holdout", help="validation | holdout"),
    config: Path = typer.Option(DEFAULT_CONFIG, exists=True),
    confirm_holdout_access: bool = typer.Option(False, "--confirm-holdout-access"),
) -> None:
    configure_logging()
    pcfg = load_portfolio_config(config)
    if window not in pcfg.windows:
        raise typer.BadParameter(f"window must be one of {sorted(pcfg.windows)}")
    sleeves = [load_sleeve(s) for s in pcfg.sleeves]
    f0 = sleeves[0].fcfg
    for s in sleeves:
        d = s.fcfg.data
        if (s.fcfg.symbol, d.clean_root, d.validation, d.holdout) != (f0.symbol, f0.data.clean_root,
                                                                        f0.data.validation, f0.data.holdout):
            raise ValueError(f"{s.spec.name}: data windows differ from {sleeves[0].spec.name}")

    portfolio_manifest = {
        "portfolio_config_sha256": pcfg.config_sha256(),
        "sleeves": [{"name": s.spec.name, "manifest_sha256": s.manifest_sha256,
                     "config_id": s.candidate["config_id"], "weight": s.spec.weight} for s in sleeves],
    }
    psha = sha(portfolio_manifest)
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    auth = None
    if window == "holdout":
        auth = authorize_holdout_access(manifest_sha256=psha, confirm=confirm_holdout_access,
                                        command="portfolio-test")
    prior = [e for e in read_ledger(LEDGER) if e.get("phase") == "holdout"] if LEDGER.exists() else []
    bars, info = load_phase_bars(f0, pcfg.symbol, window, command="portfolio-test",
                                 experiment_id=pcfg.name, authorization=auth, ledger_path=LEDGER)
    w = pcfg.windows[window]
    start = w.start
    end = w.end or date.fromisoformat(info["actual_last_session"])

    tfs = sorted({s.timeframe for s in sleeves} | {GRID_TF})
    frames = {tf: aggregate_bars(bars, timeframe=tf) for tf in tfs}
    runs = [simulate_sleeve(s, frames[s.timeframe], start=start, end=end) for s in sleeves]
    days = runs[0].days
    for r in runs[1:]:
        if not np.array_equal(r.days, days):
            raise RuntimeError("Sleeves disagree on the window's trading days")
    n_days = len(days)
    years = n_days / 252

    # SPY buy-and-hold: close-to-close from the session before the window.
    g = frames[GRID_TF].sort("bar_open_ts")
    daily = g.group_by("session_date_ny", maintain_order=True).agg(pl.col("close").last())
    dd = daily["session_date_ny"].to_numpy().astype("datetime64[D]")
    closes = daily["close"].to_numpy()
    i0 = int(np.searchsorted(dd, days[0]))
    if not np.array_equal(dd[i0:i0 + n_days], days):
        raise RuntimeError("SPY daily closes misaligned with the sleeves' days")
    spy_px = closes[i0 - 1:i0 + n_days]
    spy_rets = spy_px[1:] / spy_px[:-1] - 1.0

    # Portfolio.
    weights = np.array([s.spec.weight for s in sleeves])
    R = np.vstack([r.rets for r in runs])
    port_rets, values = combine_sleeves(R, weights)

    # Time in market on a common 5-minute grid (regular session bars in the window).
    gts = g["bar_open_ts"].dt.replace_time_zone(None).to_numpy().astype("datetime64[us]")
    gsd = g["session_date_ny"].to_numpy().astype("datetime64[D]")
    gmask = (gsd >= days[0]) & (gsd <= days[-1])
    grid = gts[gmask]
    in_mkt = np.vstack([interval_mask(grid, r.starts, r.ends) for r in runs])
    any_in = in_mkt.any(axis=0)
    n_in = in_mkt.sum(axis=0)

    out_sleeves = []
    for s, r, k in zip(sleeves, runs, range(len(runs))):
        sm = series_metrics(r.rets)
        fm = r.funnel_metrics
        exp = float(in_mkt[k].mean())
        ts_ = trade_stats(r.trades)
        out_sleeves.append({
            "name": s.spec.name, "label": s.spec.label, "weight": s.spec.weight,
            "config_id": s.candidate["config_id"], "experiment_id": s.manifest["experiment_id"],
            "params": s.candidate["params"], "timeframe": s.timeframe,
            "dev_sharpe": s.candidate["dev_sharpe"], "dev_net_return": s.candidate["dev_net_return"],
            "metrics": sm, "trades": ts_,
            "exposure": exp, "years_in_market": exp * years,
            "return_per_year_in_market": (sm["total_return"] / (exp * years)) if exp > 0 else None,
            "funnel_exposure": fm["exposure"], "funnel_net_return": fm["net_return"],
            "funnel_sharpe": fm["sharpe"], "funnel_n_trades": fm["n_trades"],
            "contribution": float(values[k, -1] - values[k, 0]),
            "vs_spy": relative_to_benchmark(r.rets, spy_rets),
            "monthly": monthly_returns(days, r.rets),
        })

    all_trades = pl.concat([r.trades for r in runs]).sort("entry_ts")
    pm = series_metrics(port_rets)
    port = {
        "metrics": pm, "n_trades": all_trades.height,
        "exposure_any_sleeve": float(any_in.mean()), "years_in_market_any": float(any_in.mean()) * years,
        "capital_deployed_avg": float(sum(w_ * in_mkt[k].mean() for k, w_ in enumerate(weights))),
        "frac_time_n_sleeves_in": {str(n): float((n_in == n).mean()) for n in range(len(runs) + 1)},
        "vs_spy": relative_to_benchmark(port_rets, spy_rets),
        "monthly": monthly_returns(days, port_rets),
        "sleeve_correlation": np.corrcoef(R).round(4).tolist(),
    }
    spy = {"metrics": series_metrics(spy_rets), "exposure": 1.0, "years_in_market": years,
           "monthly": monthly_returns(days, spy_rets)}

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = OUT_ROOT / f"{pcfg.name}_{window}"
    out_dir.mkdir(parents=True, exist_ok=True)
    holdout_label = None
    if window == "holdout":
        holdout_label = ("holdout previously inspected -- NOT an untouched test"
                         if f0.data_history.holdout_previously_inspected or prior
                         else "first recorded holdout access")
    result = {
        "portfolio": pcfg.name, "window": window, "window_dates": [str(start), str(end)],
        "n_days": n_days, "years": years, "generated_at": stamp,
        "portfolio_manifest": portfolio_manifest, "portfolio_manifest_sha256": psha,
        "data_access": info, "prior_portfolio_holdout_accesses": len(prior), "holdout_label": holdout_label,
        "construction": "equal capital per sleeve on the window's first day, no rebalancing; "
                        "SPY buy-and-hold close-to-close, no costs",
        "sleeves": out_sleeves, "portfolio_result": port, "spy": spy,
    }
    atomic_write_json(out_dir / "results.json", result)
    eq_cols = {"date": [str(days[0] - 1)] + [str(d) for d in days]}
    eq_cols["date"][0] = "start"
    for s, k in zip(sleeves, range(len(runs))):
        eq_cols[s.spec.name] = values[k] * pcfg.starting_equity
    eq_cols["portfolio"] = values.sum(axis=0) * pcfg.starting_equity
    eq_cols["spy"] = equity_curve(spy_rets, pcfg.starting_equity)
    pl.DataFrame(eq_cols).write_csv(out_dir / "daily_equity.csv")
    all_trades.write_csv(out_dir / "trades.csv")
    append_ledger({"event": "portfolio_run", "portfolio": pcfg.name, "window": window,
                   "portfolio_manifest_sha256": psha, "out_dir": str(out_dir.relative_to(PROJECT_ROOT))}, LEDGER)
    (out_dir / "report.md").write_text(_report(result))
    typer.echo((out_dir / "report.md").read_text())


def _report(res: dict) -> str:
    S, P, B = res["sleeves"], res["portfolio_result"], res["spy"]
    cols = [s["label"] for s in S] + ["Portfolio", "SPY B&H"]
    ms = [s["metrics"] for s in S] + [P["metrics"], B["metrics"]]
    rows = [
        ("Total return", [_pct(m["total_return"]) for m in ms]),
        ("CAGR", [_pct(m["cagr"]) for m in ms]),
        ("Sharpe", [_num(m["sharpe"]) for m in ms]),
        ("Sortino", [_num(m["sortino"]) for m in ms]),
        ("Ann. volatility", [_pct(m["ann_vol"]) for m in ms]),
        ("Max drawdown", [_pct(m["max_drawdown"]) for m in ms]),
        ("Longest drawdown (days)", [str(m["max_dd_duration_days"]) for m in ms]),
        ("Calmar", [_num(m["calmar"]) for m in ms]),
        ("Trades", [str(s["trades"]["n_trades"]) for s in S] + [str(P["n_trades"]), "1"]),
        ("Win rate", [_pct(s["trades"].get("win_rate")) for s in S] + ["", ""]),
        ("Avg trade", [_pct(s["trades"].get("avg_trade_return"), 2) for s in S] + ["", ""]),
        ("Profit factor", [_num(s["trades"].get("profit_factor")) for s in S] + ["", ""]),
        ("Avg hold (session hours)", [_num(s["trades"].get("avg_hold_hours"), 1) for s in S] + ["", ""]),
        ("Time in market", [_pct(s["exposure"]) for s in S] + [_pct(P["exposure_any_sleeve"]) + " (any)", "100%"]),
        ("Years in market", [_num(s["years_in_market"]) for s in S]
         + [_num(P["years_in_market_any"]), _num(B["years_in_market"])]),
        ("Beta to SPY", [_num(s["vs_spy"]["beta"]) for s in S] + [_num(P["vs_spy"]["beta"]), "1.00"]),
        ("Correlation to SPY", [_num(s["vs_spy"]["correlation"]) for s in S]
         + [_num(P["vs_spy"]["correlation"]), "1.00"]),
    ]
    lines = [f"# {res['portfolio']} -- {res['window']} {res['window_dates'][0]} to {res['window_dates'][1]}",
             "", f"{res['n_days']} trading days ({res['years']:.2f} years). {res['construction']}.", ""]
    if res["holdout_label"]:
        lines += [f"**{res['holdout_label']}**", ""]
    lines += ["| Metric | " + " | ".join(cols) + " |", "|---" * (len(cols) + 1) + "|"]
    lines += [f"| {name} | " + " | ".join(v) + " |" for name, v in rows]
    lines += ["", "Sleeves:"]
    for s in S:
        lines.append(f"- {s['label']}: `{s['config_id']}` ({s['experiment_id']}, {s['timeframe']}) "
                     f"{json.dumps(s['params'])}")
    lines += ["", f"Capital deployed on average: {_pct(P['capital_deployed_avg'])}; "
              f"share of time with 0/1/2/3 sleeves in: "
              + " / ".join(_pct(v) for v in P["frac_time_n_sleeves_in"].values()),
              f"Sleeve daily-return correlations: {P['sleeve_correlation']}", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    app()
