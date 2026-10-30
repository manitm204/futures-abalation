"""Export a finished mean-reversion funnel run (develop + validate) to the JSON
format the shared results site renders (../futures-results/).

One file per (market, strategy): futures-results/data/<MARKET>/<strategy>.json.
Re-running overwrites that file only, so markets and strategies accumulate.
Then rebuild the pages:  python ../futures-results/build.py  (writes futures-results/mean reversion/index.html)

Reads only development and validation outputs; holdout data is never touched.

Usage:
  PYTHONPATH=. python scripts/export_results_json.py --experiment-id mr_es_v3 \
      --config configs/funnel/mr_funnel_es_v3.yaml
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import polars as pl
import typer

from src.data.futures import session_spec
from src.experiments.funnel_config import load_execution_config, load_funnel_config
from src.experiments.mr_grid import AXES_V3, AXES_V5, AXES_V6, AXES_V7, AXES_V8, AXES_V9, AXES_V10, AXES_V11, AXES_V12, AXES_V13, AXES_V14, AXES_V15, AXES_V16, AXES_V17, AXES_V18, AXES_V19, AXES_V20, AXES_V21

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = PROJECT_ROOT.parent / "futures-results"
app = typer.Typer(add_completion=False)

LABELS = {
    "timeframe": "Bar size", "mean_type": "Average type", "mean_lookback": "Average length",
    "std_lookback": "Volatility length", "entry_z": "Entry z", "exit_z": "Exit z",
    "max_holding_bars": "Max hold (bars)", "entry_confirmation": "Confirmation", "stop_atr_multiple": "Stop (× ATR)",
}
SHORT = {"timeframe": "Bar", "mean_type": "Avg", "mean_lookback": "Len", "std_lookback": "Vol",
         "entry_z": "Entry", "exit_z": "Exit", "max_holding_bars": "Hold", "entry_confirmation": "Conf",
         "stop_atr_multiple": "Stop"}


def _fmt_z(x: float) -> str:
    return f"{x:g}".replace("-", "−")


def _val(axis: str, v) -> str:
    if axis == "entry_confirmation":
        return {"none": "none", "positive_bar_return": "up bar"}[v]
    if axis == "stop_atr_multiple":
        return "none" if v == "none" else f"{float(v):g}"
    if axis == "mean_type":
        return str(v).upper()
    if isinstance(v, float):
        return f"{v:g}"
    return str(v)


def _num(x):
    if x is None:
        return None
    x = float(x)
    return x if np.isfinite(x) else None


def _metrics(get) -> dict:
    return {k: _num(get(k)) for k in ("net_return", "cagr", "sharpe", "max_drawdown", "exposure",
                                         "win_rate", "profit_factor", "n_completed_trades", "turnover_annual")}


def _buy_and_hold(fcfg, symbol: str) -> dict:
    """Unlevered, continuously rolled long position: daily return = change in the
    back-adjusted close / previous raw (unadjusted) close. RTH session closes."""
    base = PROJECT_ROOT / fcfg.data.clean_root / f"symbol={symbol}" / "timeframe=1min"
    last_year = fcfg.data.validation.end.year
    files = [p for p in base.rglob("*.parquet") if int(p.parts[-3].split("=")[1]) <= last_year]
    df = (pl.concat([pl.read_parquet(p, columns=["session_date_ny", "bar_open_ts", "close", "price_adjustment",
                                                   "is_regular_session"]) for p in files])
          .filter("is_regular_session").sort("bar_open_ts")
          .group_by("session_date_ny", maintain_order=True).last())
    adj, raw = df["close"].to_numpy(), (df["close"] - df["price_adjustment"]).to_numpy()
    days = df["session_date_ny"].to_numpy().astype("datetime64[D]")
    r = np.diff(adj) / raw[:-1]
    out = {}
    for name, w in (("dev", fcfg.data.development), ("val", fcfg.data.validation)):
        m = (days[1:] >= np.datetime64(w.start)) & (days[1:] <= np.datetime64(w.end))
        x = r[m]
        eq = np.cumprod(1 + x)
        out[name] = {"net_return": float(eq[-1] - 1), "sharpe": float(x.mean() / x.std(ddof=1) * np.sqrt(252)),
                     "max_drawdown": float((eq / np.maximum.accumulate(eq) - 1).min())}
    return out


@app.command()
def main(
    experiment_id: str = typer.Option(...),
    config: Path = typer.Option(...),
    market_name: str = typer.Option("E-mini S&P 500"),
    key: str = typer.Option("mean_reversion", help="File name / tab id under data/<MARKET>/"),
    label: str = typer.Option("Mean reversion (z-score dip buying)", help="Strategy tab label"),
    variant: str = typer.Option("", help="Optional variant id (e.g. 15m) when one strategy tab holds several runs "
                                "shown side by side; written to data/<MARKET>/<key>__<variant>.json"),
    variant_label: str = typer.Option("", help="Button text for the variant (default: the variant id)"),
    out_root: Path = typer.Option(SITE_ROOT / "data"),
) -> None:
    fcfg = load_funnel_config(config)
    ec = load_execution_config(fcfg)
    axes = {"mean_reversion_v3": AXES_V3, "mean_reversion_v5": AXES_V5, "mean_reversion_v6": AXES_V6, "mean_reversion_v7": AXES_V7, "mean_reversion_v8": AXES_V8, "mean_reversion_v9": AXES_V9, "mean_reversion_v10": AXES_V10, "mean_reversion_v11": AXES_V11, "mean_reversion_v12": AXES_V12, "mean_reversion_v13": AXES_V13, "mean_reversion_v14": AXES_V14, "mean_reversion_v15": AXES_V15, "mean_reversion_v16": AXES_V16, "mean_reversion_v17": AXES_V17, "mean_reversion_v18": AXES_V18, "mean_reversion_v19": AXES_V19, "mean_reversion_v20": AXES_V20, "mean_reversion_v21": AXES_V21}.get(fcfg.strategy)
    if axes is None:
        raise typer.BadParameter("exporter knows the futures mean-reversion grids (v3, v5-v21) only")
    exp = PROJECT_ROOT / "runs" / "funnel" / experiment_id
    summary = json.loads((exp / "summary.json").read_text())
    val = json.loads((exp / "validation_results.json").read_text())
    df = pl.read_parquet(exp / "config_status.parquet")
    by_id = {r["config_id"]: r for r in df.filter(pl.col("s6_status").is_not_null()
                                                   & (pl.col("s6_status") == "pass")).to_dicts()}
    sym = fcfg.symbol
    n = df.height

    # ---- funnel: per stage, what was removed and on which bar sizes ----
    def removed_by_tf(stage: int) -> str:
        c = Counter(df.filter(pl.col(f"s{stage}_status").is_in(["hard_reject", "insufficient_evidence"]))["timeframe"])
        return ", ".join(f"{c[t]:,} on {t}" for t in fcfg.data.timeframes if c[t])
    rej = summary["rejection_reason_counts"]
    tc, pf, ps = fcfg.trade_count, fcfg.performance, fcfg.parameter_stability
    st = {r["stage"].split(" ")[0]: r for r in summary["survivor_table"]}
    n_val_pass = sum(r["status"] == "pass" for r in val["results"])
    funnel = [
        {"name": "Start", "sub": "every combination", "n": n,
         "why": f"All {n:,} versions backtested once on {fcfg.data.development.start.year}–{fcfg.data.development.end.year} data."},
        {"name": "1 · Integrity", "sub": "no cheating", "n": st["1"]["passed"],
         "why": f"Per-trade checks for look-ahead and impossible fills on every version, plus "
                f"{summary['integrity']['truncation_sample']} random versions re-run on cut-off data. "
                f"{n - st['1']['passed']:,} failed."},
        {"name": "2 · Enough trades", "sub": f"≥{tc.min_completed_trades} trades, spread out", "n": st["2"]["passed"],
         "why": f"Needs ≥{tc.min_completed_trades} completed trades and ≥{tc.min_trades_per_year} a year in "
                f"≥{tc.min_years_meeting_floor} of the 5 years. Removed {st['1']['passed'] - st['2']['passed']:,} "
                f"({removed_by_tf(2)})."},
        {"name": "3 · Profit", "sub": f"net > 0, Sharpe ≥ {pf.min_sharpe}", "n": st["3"]["passed"],
         "why": f"Needs a net profit, Sharpe ≥ {pf.min_sharpe} and drawdown no worse than {abs(pf.max_drawdown):.0%}. "
                f"Removed {st['2']['passed'] - st['3']['passed']:,} ({removed_by_tf(3)}); "
                f"{rej.get('s3:hard_reject:net_return', 0):,} of them lost money."},
        {"name": "4 · Stable settings", "sub": "neighbors also work", "n": st["4"]["passed"],
         "why": (f"Moving any one setting a single step must keep ≥{ps.min_frac_profitable:.0%} of neighbors "
                 f"profitable with median Sharpe ≥ {ps.min_median_sharpe}. Removed "
                 f"{st['3']['passed'] - st['4']['passed']} lone peaks.") if ps.mode == "grid_neighbors" else
                (f"Each setting is nudged one at a time, down and up: average length, volatility length and max hold "
                 f"by ±{ps.local.int_rel:.0%} (rounded), entry and exit z by ±{ps.local.entry_z_abs:g}, a numeric ATR "
                 f"stop by ±{ps.local.stop_atr_abs:g}. At least {ps.min_frac_profitable:.0%} of the 10–12 nudged "
                 f"versions must be profitable, with median Sharpe ≥ {ps.min_median_sharpe}. Removed "
                 f"{st['3']['passed'] - st['4']['passed']}.")},
        {"name": "5 · Time stability", "sub": f"≥{fcfg.time_stability.min_profitable_years} profitable years",
         "n": st["5"]["passed"], "why": f"Removed {st['4']['passed'] - st['5']['passed']}."},
        {"name": "6 · Remove duplicates", "sub": f"best {fcfg.dedup.reps_per_cluster} per group", "n": st["6"]["passed"],
         "why": f"Versions whose monthly returns correlate ≥ {fcfg.dedup.corr_threshold} form a group; the best "
                f"{fcfg.dedup.reps_per_cluster} of each go on (a group of one keeps its one). "
                f"{st['5']['passed']} versions formed {st['6']['n_clusters']} groups."},
        {"name": "7 · Cost stress", "sub": f"profitable at {fcfg.execution_stress.gate_cost_multiplier}× costs",
         "n": st["7"]["passed"], "why": f"Removed {st['6']['passed'] - st['7']['passed']}."},
        {"name": "8 · Validation", "sub": f"{fcfg.data.validation.start.year}–{fcfg.data.validation.end.year}, new data",
         "n": n_val_pass,
         "why": f"Frozen finalists run once on unseen data: needs net > 0, Sharpe ≥ {fcfg.validation.min_sharpe}, "
                f"drawdown no worse than {abs(fcfg.validation.max_drawdown):.0%} and ≥{fcfg.validation.min_completed_trades} trades."},
    ]

    # ---- settings of the versions that passed the stable-settings test ----
    s4 = df.filter(pl.col("s4_status") == "pass")

    def _breakdown(sub: pl.DataFrame, skip: tuple[str, ...] = ()) -> list[dict]:
        out = []
        for ax, vals in axes.items():
            if ax in skip:
                continue
            c = Counter(sub[ax].to_list())
            med = {v: sub.filter(pl.col(ax) == v)["dev_sharpe"].median() for v in vals if c.get(v)}
            out.append({"axis": ax, "label": LABELS[ax],
                        "values": [{"v": _val(ax, v), "n": c.get(v, 0), "median_sharpe": med.get(v)} for v in vals]})
        return out

    stable = _breakdown(s4)
    # Same breakdown within each bar size, so per-timeframe preferences are visible.
    stable_by_tf = [{"timeframe": _val("timeframe", tf), "n": sub.height, "axes": _breakdown(sub, skip=("timeframe",))}
                    for tf in axes["timeframe"] if (sub := s4.filter(pl.col("timeframe") == tf)).height]

    # ---- random-entry ("luck") benchmark, if run (scripts/run_random_benchmark.py) ----
    luck_path = exp / "random_benchmark.json"
    luck_raw = json.loads(luck_path.read_text()) if luck_path.exists() else None
    luck_by_id = {f["config_id"]: f for f in luck_raw["finalists"]} if luck_raw else {}
    luck = None if not luck_raw else {
        "n_sims": luck_raw["n_sims"], "hold_bars": luck_raw["hold_bars"], "levels": luck_raw["levels"],
        "method": luck_raw["method"],
        "curves": [{"timeframe": _val("timeframe", tf), "rows": rows} for tf, rows in luck_raw["curves"].items()],
    }

    # ---- finalists: dev vs validation ----
    finalists = []
    for r in val["results"]:
        d = by_id[r["config_id"]]
        finalists.append({
            "order": r["dev_order"], "group": d["dedup_cluster"], "config_id": r["config_id"][:8],
            "settings": {ax: _val(ax, d[ax]) for ax in axes},
            "dev": _metrics(lambda k: d.get(f"dev_{k}")),
            "val": _metrics(lambda k: r["metrics"].get(k)),
            "status": r["status"], "reasons": r["reasons"],
            "exits": {"z": d["full_n_z_exits"], "time": d["full_n_time_exits"], "stop": d["full_n_stop_exits"]},
            "stress_1_5x": _num(d.get("stress_cost_1.5x_net_return")),
            "breakeven_cost_x": _num(d.get("breakeven_cost_multiplier")),
            "transfer_sharpe": _num(d.get("qqq_dev_sharpe")),
            "neighbor_median_sharpe": _num(d.get("neighbor_median_sharpe")),
            "local_frac_profitable": _num(d.get("local_frac_profitable")),
            "local_median_sharpe": _num(d.get("local_median_sharpe")),
            "local_detail": json.loads(d["local_detail"]) if d.get("local_detail") else None,
            "dsr": _num(d.get("dsr_li_ji")),
            "luck": None if r["config_id"] not in luck_by_id else {
                k: luck_by_id[r["config_id"]][k] for k in ("exposure_level", "luck_pct_sharpe", "luck_pct_return")},
        })

    # ---- ablation (development only): per axis value, from build_mr_ablation_report.py ----
    abl_path = exp / "ablation_summary.json"
    ablation = None
    if abl_path.exists():
        abl = json.loads(abl_path.read_text())
        ablation = [{"axis": a, "label": LABELS[a],
                     "values": [{"v": _val(a, type(axes[a][0])(r["value"]) if not isinstance(axes[a][0], str) else r["value"]),
                                 "n": r["n"], "pct_profitable": r["pct_profitable"], "median_sharpe": r["median_sharpe"],
                                 "p90_sharpe": r["p90_sharpe"], "n_stage3": r["n_stage3"], "n_survivors": r["n_survivors"]}
                                for r in abl["axes"] if r["axis"] == a]} for a in axes]

    # ---- average x volatility length map around the top finalist (validation passer if any) ----
    # (no finalists: the version with the best development Sharpe)
    top = next((f for f in val["results"] if f["status"] == "pass"), val["results"][0] if val["results"] else None)
    if top is not None:
        c, top_order = by_id[top["config_id"]], top["dev_order"]
    else:
        c, top_order = df.sort("dev_sharpe", descending=True, nulls_last=True).row(0, named=True), None
    others = [a for a in axes if a not in ("mean_lookback", "std_lookback")]
    sub = df.filter(pl.all_horizontal([pl.col(a) == c[a] for a in others]))
    cell = {(r["mean_lookback"], r["std_lookback"]): r for r in sub.iter_rows(named=True)}
    length_map = {
        "order": top_order, "fixed": {LABELS[a]: _val(a, c[a]) for a in others},
        "center": [c["mean_lookback"], c["std_lookback"]],
        "rows": list(axes["mean_lookback"]), "cols": list(axes["std_lookback"]),
        "sharpe": [[_num(cell[(m, v)]["dev_sharpe"]) if (m, v) in cell else None for v in axes["std_lookback"]]
                   for m in axes["mean_lookback"]],
        "trades": [[cell[(m, v)]["dev_n_completed_trades"] if (m, v) in cell else None for v in axes["std_lookback"]]
                   for m in axes["mean_lookback"]],
    }

    dsr = summary["dsr"]
    out = {
        "market": sym, "market_name": market_name,
        "strategy_key": key, "strategy_name": label,
        "variant": variant or None, "variant_label": (variant_label or variant) or None,
        "stability_mode": ps.mode,
        "validation_rules": fcfg.validation.model_dump(),
        "run_id": experiment_id, "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "periods": {"dev": [str(fcfg.data.development.start), str(fcfg.data.development.end)],
                    "val": [str(fcfg.data.validation.start), str(fcfg.data.validation.end)]},
        "strategy": {
            "summary": ("Buy a sharp dip and sell when the price snaps back. Each bar the strategy measures how far the "
                        "close sits below its moving average, in units of recent volatility (a z-score). When that "
                        "z-score falls to the entry level it buys at the next bar's open, and it sells once the "
                        "z-score recovers to the exit level, after a maximum number of bars, or at an optional stop."),
            "formula": "z = (close − average of the last N closes) ÷ standard deviation of the last M closes",
            "rules": [
                {"label": "Buy", "text": f"When z closes at or below the entry level ({_fmt_z(max(axes['entry_z']))} to {_fmt_z(min(axes['entry_z']))}). With confirmation on, "
                                         "the signal bar must also close above the previous bar's close. The order fills at the next bar's open."},
                {"label": "Sell", "text": "At the next open after z closes at or above the exit level, or once the "
                                          "position has been held the max number of bars. An optional stop sits "
                                          "k × ATR(14) below the entry and fills the moment it is touched."},
                {"label": "Size", "text": f"Long only, one position at a time. As many whole {sym} contracts as the "
                                          f"account covers at full contract value (no leverage), starting from "
                                          f"${ec.starting_equity:,.0f}."},
            ],
            "axes": [{"label": LABELS[ax], "values": [_val(ax, v) for v in vals]} for ax, vals in axes.items()],
            "grid_size": n,
        },
        "funnel": funnel,
        "stable": {"n": s4.height, "axes": stable, "by_timeframe": stable_by_tf},
        "ablation": ablation,
        "length_map": length_map,
        "luck": luck,
        "finalists": finalists,
        "short_labels": SHORT,
        "benchmark": {"label": f"Holding {sym} (rolled, unlevered)", **_buy_and_hold(fcfg, sym)},
        "transfer_symbol": fcfg.confidence.transfer_symbol,
        "dsr": {"effective_trials": dsr["effective_trials"]["li_ji"], "raw_trials": dsr["trial_count_options"]["raw"]},
        "assumptions": [
            f"Data: Databento CME continuous front month ({sym}.v.0), 1-minute bars aggregated to 5/15/60 minutes. "
            "Rolls are back-adjusted so the roll gap is not treated as a price move.",
            f"Day session only: {session_spec(sym).label} on NYSE trading days (ending no later than the NYSE "
            "close). Overnight Globex trading is not used; positions can be held overnight.",
            f"Costs: {ec.slippage_ticks_market:g} tick slippage per side and ${ec.commission_per_contract:.2f} "
            "commission per contract per side. Positions that span a roll are assumed to roll for free.",
            "Lengths and holding periods are counted in bars of the chosen bar size.",
            "Sharpe uses daily mark-to-market returns (√252), with idle cash earning 0%. Time in market is the share "
            "of bars with an open position.",
            "Holdout (2025 onward) has not been run. It is a one-time final test and needs an explicit go-ahead.",
        ],
        "source": f"mean-reversion-backtest/runs/funnel/{experiment_id}/ · {config.as_posix()}",
    }
    path = out_root / sym / (f"{key}__{variant}.json" if variant else f"{key}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1))
    typer.echo(f"wrote {path}")


if __name__ == "__main__":
    app()
