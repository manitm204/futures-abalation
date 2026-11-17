"""Export a finished price-path convexity funnel run to the JSON format the shared results
site renders (../futures-results/), the same shape as the squeeze and noise-band exporters write.

One file per (market, version, bar size): futures-results/data/<MARKET>/path_convexity_<version>.json.
Re-running overwrites that file only. Then rebuild the pages:  python ../futures-results/build.py
(runs go to "futures-results/price-path convexity/index.html").

Works after `develop` alone (validation columns are then empty and stage 8 shows "not run") and
again after `validate`. Reads only development and validation outputs; holdout data is never touched.

Usage:
  PYTHONPATH=. python scripts/export_results_json.py --experiment-id pc_es_v1_15m \
      --config configs/funnel/pc_funnel_es_v1_15m.yaml --variant 15m
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
from src.experiments.pc_grid import AXES_PC_V1_5M, AXES_PC_V1_15M, AXES_PC_V2_15M, AXES_PC_V3_15M
from src.experiments.funnel_config import load_execution_config, load_funnel_config

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = PROJECT_ROOT.parent / "futures-results"
app = typer.Typer(add_completion=False)

# strategy -> (axes, file-key prefix, tab label prefix, heat-map axes (rows, cols))
SPACES = {
    "path_convexity_v1_15m": (AXES_PC_V1_15M, "path_convexity", "Price-path convexity", ("lookback", "entry_z")),
    "path_convexity_v1_5m": (AXES_PC_V1_5M, "path_convexity", "Price-path convexity", ("lookback", "entry_z")),
    "path_convexity_v2_15m": (AXES_PC_V2_15M, "path_convexity", "Price-path convexity", ("lookback", "entry_z")),
    "path_convexity_v3_15m": (AXES_PC_V3_15M, "path_convexity", "Price-path convexity", ("lookback", "entry_z")),
}
MARKET_NAMES = {"ES": "E-mini S&P 500", "NQ": "E-mini Nasdaq-100", "YM": "E-mini Dow", "RTY": "E-mini Russell 2000",
                "CL": "Crude oil", "GC": "Gold", "6E": "Euro FX", "6J": "Japanese yen", "ZN": "10-year T-note",
                "ZB": "30-year T-bond"}
LABELS = {
    "timeframe": "Bar size", "lookback": "Look-back N (bars)", "signal_form": "Signal form",
    "z_lookback": "z-score history (bars)", "entry_z": "Entry |z|", "quadrant": "Quadrant",
    "min_move_atr": "Min net move (× ATR)", "direction": "Direction", "hold": "Hold", "stop": "Stop",
    "trend_filter": "Trend filter",
}
SHORT = {"timeframe": "Bar", "lookback": "N", "signal_form": "Form", "z_lookback": "zHist", "entry_z": "z",
         "quadrant": "Quad", "min_move_atr": "Move", "direction": "Side", "hold": "Hold", "stop": "Stop",
         "trend_filter": "Trend"}
MOVES = {"lookback": "N", "z_lookback": "z hist", "entry_z": "Entry z", "stop_atr": "Stop", "min_move_atr": "Min move"}
FORM_NAMES = {"paper": "paper", "atr": "ATR gap", "maxgap": "max gap", "reversal": "control"}


def _val(axis: str, v) -> str:
    if axis == "stop":
        return "none" if v == "none" else f"{float(v):g} ATR"
    if axis == "min_move_atr":
        return "any" if float(v) == 0 else f"{float(v):g} ATR"
    if axis == "trend_filter":
        return "none" if v == "none" else f"EMA {v[3:]}"
    if axis == "signal_form":
        return FORM_NAMES.get(v, v)
    if axis == "hold":
        return {"half": "N/2 bars", "full": "N bars", "1.5n": "1.5N bars", "session": "to close"}.get(v, v)
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
    market_name: str = typer.Option("", help="Default: the market's usual name"),
    key: str = typer.Option("", help="File name / tab id under data/<MARKET>/ (default: path_convexity_<version>)"),
    label: str = typer.Option("", help="Strategy tab label (default: Price-path convexity · <version>)"),
    variant: str = typer.Option("", help="Optional variant id (e.g. 15m) when one strategy tab holds several runs"),
    variant_label: str = typer.Option("", help="Button text for the variant (default: the variant id)"),
    out_root: Path = typer.Option(SITE_ROOT / "data"),
) -> None:
    fcfg = load_funnel_config(config)
    ec = load_execution_config(fcfg)
    run_dir = PROJECT_ROOT / "runs" / "funnel" / experiment_id
    hfiles = sorted(run_dir.glob("holdout_results_*.json"))
    picks = sorted({c.get("dev_order") for hf in hfiles for c in json.loads(hf.read_text()).get("results", [])})
    holdout_line = (f"Holdout (2025 onward) was run once for {', '.join(f'#{o}' for o in picks)}; the results are on "
                    "this market's separate holdout tab." if picks else
                    "Holdout (2025 onward) has not been run. It is a one-time final test and needs an explicit go-ahead.")
    if fcfg.strategy not in SPACES:
        raise typer.BadParameter(f"exporter knows the convexity spaces {sorted(SPACES)} only")
    axes, key_prefix, label_prefix, (heat_r, heat_c) = SPACES[fcfg.strategy]
    axes = {"timeframe": axes["timeframe"], **axes}  # bar size first, as on the other families' pages
    sym = fcfg.symbol
    version = next(x for x in experiment_id.split("_") if x.startswith("v") and x[1:].isdigit())
    key = key or f"{key_prefix}_{version}"
    label = label or f"{label_prefix} · {version}"
    exp = PROJECT_ROOT / "runs" / "funnel" / experiment_id
    summary = json.loads((exp / "summary.json").read_text())
    frozen = json.loads((exp / "frozen_representatives.json").read_text())
    val_path = exp / "validation_results.json"
    val = json.loads(val_path.read_text()) if val_path.exists() else None
    val_by_id = {r["config_id"]: r for r in val["results"]} if val else {}
    df = pl.read_parquet(exp / "config_status.parquet")
    # Text axes (stop, target) may spell a number differently ("1" vs "1.0"): use the axis spelling.
    for ax, vals in axes.items():
        if df.schema.get(ax) == pl.Utf8:
            def _canon(x):
                try:
                    return repr(float(x))
                except ValueError:
                    return x
            spell = {_canon(v): v for v in vals}
            df = df.with_columns(pl.col(ax).map_elements(lambda x, sp=spell: sp.get(_canon(x), x),
                                                         return_dtype=pl.Utf8))
    by_id = {r["config_id"]: r for r in df.filter(pl.col("s7_status") == "pass").to_dicts()}
    n = df.height
    dev_w, val_w = fcfg.data.development, fcfg.data.validation

    # ---- funnel ----
    def removed_by_tf(stage: int) -> str:
        c = Counter(df.filter(pl.col(f"s{stage}_status").is_in(["hard_reject", "insufficient_evidence"]))["timeframe"])
        return ", ".join(f"{c[t]:,} on {t}" for t in fcfg.data.timeframes if c[t]) or "none"
    rej = summary["rejection_reason_counts"]
    tc, pf, ps = fcfg.trade_count, fcfg.performance, fcfg.parameter_stability
    st = {r["stage"].split(" ")[0]: r for r in summary["survivor_table"]}
    n_val_pass = sum(r["status"] == "pass" for r in val["results"]) if val else None
    distinct = len({(r["dev_n_completed_trades"], round(r["dev_net_return"], 10), round(r["dev_sharpe"], 10))
                    for r in by_id.values()})
    lo = ps.local
    nudges = (f"look-back N and the z-score history by ±{lo.int_rel:.0%} (rounded, at least one bar), the entry "
              f"|z| by ±{lo.entry_z_abs:g}, an ATR stop by ±{lo.stop_atr_abs:g} and the minimum net move by "
              f"±{lo.min_move_atr_abs:g} ATR (\"no stop\" has nothing to nudge)")
    funnel = [
        {"name": "Start", "sub": "every combination", "n": n,
         "why": f"All {n:,} versions backtested once on {dev_w.start.year}–{dev_w.end.year} data."},
        {"name": "1 · Integrity", "sub": "no cheating", "n": st["1"]["passed"],
         "why": f"Per-trade checks on every version: the signal was recomputed independently and each entry was a "
                f"fresh cross on the right side with every filter met, no qualifying signal was skipped while flat, "
                f"fills were never better than the market, nothing was held overnight. Plus "
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
        *([{"name": "Prescreen", "sub": f"best {ps.prescreen.per_cluster} per group", "n": st["4a"]["passed"],
            "why": f"More than {ps.prescreen.max_configs:,} versions passed the profit test, so they were grouped first "
                   f"(monthly returns correlating ≥ {fcfg.dedup.corr_threshold}) and only the best "
                   f"{ps.prescreen.per_cluster} of each of the {st['4a']['n_clusters']:,} groups by 2018–2022 Sharpe "
                   "went on to the stable-settings test. This rule was set before the run."}] if "4a" in st else []),
        {"name": "4 · Stable settings", "sub": "nudged settings also work", "n": st["4"]["passed"],
         "why": f"Each setting is nudged one at a time, down and up: {nudges}. At least {ps.min_frac_profitable:.0%} "
                f"of the nudged versions must be profitable, with median Sharpe ≥ {ps.min_median_sharpe}. "
                f"Removed {st['4a' if '4a' in st else '3']['passed'] - st['4']['passed']}."},
        {"name": "5 · Time stability", "sub": f"≥{fcfg.time_stability.min_profitable_years} profitable years",
         "n": st["5"]["passed"], "why": f"Removed {st['4']['passed'] - st['5']['passed']}."},
        {"name": "6 · Remove duplicates", "sub": f"best {fcfg.dedup.reps_per_cluster} per group", "n": st["6"]["passed"],
         "why": f"Versions whose monthly returns correlate ≥ {fcfg.dedup.corr_threshold} form a group; the best "
                f"{fcfg.dedup.reps_per_cluster} of each go on (a group of one keeps its one). "
                f"{st['5']['passed']:,} versions formed {st['6']['n_clusters']} groups; {distinct} of the "
                f"{st['6']['passed']} picks are distinct backtests."},
        {"name": "7 · Cost stress", "sub": f"profitable at {fcfg.execution_stress.gate_cost_multiplier}× costs",
         "n": st["7"]["passed"], "why": f"Removed {st['6']['passed'] - st['7']['passed']}."},
        {"name": "8 · Validation", "sub": f"{val_w.start.year}–{val_w.end.year}, new data", "n": n_val_pass,
         "why": (f"Frozen finalists run once on unseen data: needs net > 0, Sharpe ≥ {fcfg.validation.min_sharpe}, "
                 f"drawdown no worse than {abs(fcfg.validation.max_drawdown):.0%} and ≥{fcfg.validation.min_completed_trades} trades.")
                + ("" if val else " Not run yet: the finalists are frozen and waiting for this step.")},
    ]

    # ---- settings of the versions that passed the stable-settings test ----
    s4 = df.filter(pl.col("s4_status") == "pass")

    def _breakdown(sub: pl.DataFrame, skip: tuple[str, ...] = ()) -> list[dict]:
        out = []
        for ax, vals in axes.items():
            if ax in skip or len(vals) < 2:
                continue
            c = Counter(sub[ax].to_list())
            med = {v: sub.filter(pl.col(ax) == v)["dev_sharpe"].median() for v in vals if c.get(v)}
            out.append({"axis": ax, "label": LABELS[ax],
                        "values": [{"v": _val(ax, v), "n": c.get(v, 0), "median_sharpe": med.get(v)} for v in vals]})
        return out

    stable = _breakdown(s4)
    stable_by_tf = [{"timeframe": _val("timeframe", tf), "n": sub.height, "axes": _breakdown(sub, skip=("timeframe",))}
                    for tf in axes["timeframe"] if (sub := s4.filter(pl.col("timeframe") == tf)).height]

    # ---- ablation (development only): every value of every setting across the full grid ----
    ablation = []
    for ax, vals in axes.items():
        if len(vals) < 2:
            continue
        rows = []
        for v in vals:
            g = df.filter(pl.col(ax) == v)
            rows.append({"v": _val(ax, v), "n": g.height,
                         "pct_profitable": float((g["dev_net_return"] > 0).mean()),
                         "median_sharpe": _num(g["dev_sharpe"].median()),
                         "p90_sharpe": _num(g["dev_sharpe"].quantile(0.9)),
                         "n_stage3": int((g["s3_status"] == "pass").sum()),
                         "n_survivors": int((g["s7_status"] == "pass").sum())})
        ablation.append({"axis": ax, "label": LABELS[ax], "values": rows})

    # ---- random-entry ("luck") benchmark, if run (scripts/run_pc_random_benchmark.py) ----
    luck_path = exp / "random_benchmark.json"
    luck_raw = json.loads(luck_path.read_text()) if luck_path.exists() and val else None
    luck_by_id = {f["config_id"]: f for f in luck_raw["finalists"]} if luck_raw else {}
    luck = None
    if luck_raw:
        def _match(g):  # the finalists this curve is for (only axes the settings show)
            return {ax: _val(ax, luck_raw["groups"][g][ax]) for ax in ("timeframe", "direction") if len(axes[ax]) > 1}

        def _glabel(g):
            meta = luck_raw["groups"][g]
            side = {"long": "long only", "short": "short only"}.get(
                meta["direction"], f"long + short ({meta['p_long']:.0%} long)")
            return f"{_val('timeframe', meta['timeframe'])} · {side}"
        luck = {
            "n_sims": luck_raw["n_sims"], "levels": luck_raw["levels"], "method": luck_raw["method"],
            "curves": [{"timeframe": _glabel(g), "match": _match(g), "rows": rows,
                        "trade_bars": [luck_raw["groups"][g]["median_trade_bars"], luck_raw["groups"][g]["mean_trade_bars"]],
                        "p_long": luck_raw["groups"][g]["p_long"]}
                       for g, rows in luck_raw["curves"].items()],
            "text": (f"For every whole-percent time in market in each group's {val_w.start.year}–{val_w.end.year} "
                     f"range, {luck_raw['n_sims']} random runs trade {sym} at random times on random days. Each "
                     "group is one bar size and direction setting. Like the strategy, the random trades are "
                     "intraday only, never overlap, and are always closed by the session's last bar. Their lengths "
                     "are drawn from that group's own finalist trades, so trade counts and costs match. Long-only "
                     "groups trade long and short-only groups short; long-and-short groups go long with the same "
                     "share of trades their finalists did. They pay the same costs and use the same sizing and "
                     "Sharpe math as the strategy."),
        }

    # ---- finalists: frozen development order; validation filled in once it has run ----
    finalists = []
    for c in frozen["candidates"]:
        d = by_id[c["config_id"]]
        v = val_by_id.get(c["config_id"])
        finalists.append({
            "order": c["dev_order"], "group": d["dedup_cluster"], "config_id": c["config_id"][:8],
            "settings": {ax: _val(ax, d[ax]) for ax in axes if len(axes[ax]) > 1},
            "dev": _metrics(lambda k: d.get(f"dev_{k}")),
            "val": _metrics(lambda k: v["metrics"].get(k)) if v else None,
            "status": v["status"] if v else "pending", "reasons": v["reasons"] if v else [],
            "exits": {"time": d["full_n_time_exits"], "eod": d["full_n_eod_exits"], "stop": d["full_n_stop_exits"]},
            "stress_1_5x": _num(d.get("stress_cost_1.5x_net_return")),
            "breakeven_cost_x": _num(d.get("breakeven_cost_multiplier")),
            "transfer_sharpe": _num(d.get("qqq_dev_sharpe")),
            "neighbor_median_sharpe": _num(d.get("neighbor_median_sharpe")),
            "local_frac_profitable": _num(d.get("local_frac_profitable")),
            "local_median_sharpe": _num(d.get("local_median_sharpe")),
            "local_detail": json.loads(d["local_detail"]) if d.get("local_detail") else None,
            "dsr": _num(d.get("dsr_li_ji")),
            "luck": None if c["config_id"] not in luck_by_id else {
                k: luck_by_id[c["config_id"]][k] for k in ("exposure_level", "luck_pct_sharpe", "luck_pct_return")},
        })

    # ---- heat map of the line's two main settings around the top finalist (validation passer if any) ----
    top = next((f for f in finalists if f["status"] == "pass"), finalists[0] if finalists else None)
    if top is not None:
        cfg_top = by_id[next(c["config_id"] for c in frozen["candidates"] if c["dev_order"] == top["order"])]
        top_order = top["order"]
    else:
        cfg_top, top_order = df.sort("dev_sharpe", descending=True, nulls_last=True).row(0, named=True), None
    others = [a for a in axes if a not in (heat_r, heat_c)]
    sub = df.filter(pl.all_horizontal([pl.col(a) == cfg_top[a] for a in others]))
    cell = {(r[heat_r], r[heat_c]): r for r in sub.iter_rows(named=True)}
    rows_, cols_ = list(axes[heat_r]), list(axes[heat_c])
    length_map = {
        "title": f"{LABELS[heat_r]} × {LABELS[heat_c]}",
        "pair_text": f"{LABELS[heat_r].split(' (')[0].lower()} and {LABELS[heat_c].split(' (')[0].lower()}",
        "corner": f"{SHORT[heat_r]} ↓ · {SHORT[heat_c]} →", "row_short": SHORT[heat_r].lower(),
        "col_short": SHORT[heat_c].lower(),
        "order": top_order, "fixed": {LABELS[a]: _val(a, cfg_top[a]) for a in others if len(axes[a]) > 1},
        "center": [_val(heat_r, cfg_top[heat_r]), _val(heat_c, cfg_top[heat_c])],
        "rows": [_val(heat_r, x) for x in rows_], "cols": [_val(heat_c, x) for x in cols_],
        "sharpe": [[_num(cell[(m, b)]["dev_sharpe"]) if (m, b) in cell else None for b in cols_] for m in rows_],
        "trades": [[cell[(m, b)]["dev_n_completed_trades"] if (m, b) in cell else None for b in cols_] for m in rows_],
    }

    def _words(xs: list[str], last: str = "or") -> str:
        return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + f" {last} " + xs[-1]
    sides = "Long, short or both"
    dsr = summary["dsr"]
    out = {
        "market": sym, "market_name": market_name or MARKET_NAMES.get(sym, sym),
        "strategy_key": key, "strategy_name": label,
        "variant": variant or None, "variant_label": (variant_label or variant) or None,
        "stability_mode": ps.mode,
        "validation_rules": fcfg.validation.model_dump(),
        "run_id": experiment_id, "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "periods": {"dev": [str(dev_w.start), str(dev_w.end)], "val": [str(val_w.start), str(val_w.end)]},
        "strategy": {
            "summary": ("Fade (or follow) the shape of the recent move, flat by the close. Price-path convexity "
                        "(Gulen & Woeppel, JFQA 2025, Purdue) measures when a move happened inside a window: draw a "
                        "straight line from the window's first close to its last, and see whether the path sagged "
                        "below it (convex: an up-move came late) or bulged above it (concave: it came early). The "
                        "paper finds high convexity predicts lower returns on daily data; everything here is "
                        "intraday, so it is an extrapolation. A plain N-bar reversal runs alongside as the control."),
            "formula": "convexity = ((P1 + PN)/2 − mean(P1..PN)) / ((P1 + PN)/2); high z → short, low z → long",
            "rules": [
                {"label": "Signal", "text": "Over the last N closes: " + "; ".join(
                    {"paper": "paper = the formula above",
                     "atr": "ATR gap = the same average line-minus-path gap ÷ ATR(14)",
                     "maxgap": "max gap = the single largest line-minus-path gap ÷ ATR(14)",
                     "reversal": "control = (PN − P1) ÷ ATR(14), the plain N-bar return"}[f]
                    for f in axes["signal_form"])
                    + f". Each is turned into a z-score against its own last "
                      f"{_words([str(z) for z in axes['z_lookback']], 'or')} bars."},
                {"label": "Enter", "text": "A fresh cross of z above +entry goes short; below −entry goes long, "
                                           "filled at the next bar's open. Quadrant: all = every signal (the paper); "
                                           "late = only fades of the window's net move; early = only trades with it. "
                                           f"Optional: the net move must be at least {_words([f'{m:g}' for m in axes['min_move_atr'] if m], 'or')} × ATR(14); "
                                           f"an {_words(['EMA(' + t[3:] + ')' for t in axes['trend_filter'] if t != 'none'], 'or')} "
                                           "trend filter (longs above, shorts below). No entries in the last "
                                           "30 minutes; a signal while a position is open is dropped."},
                {"label": "Exit", "text": f"Time exit after {_words([_val('hold', h).replace(' bars', '') for h in axes['hold'] if h != 'session'], 'or')} bars at that bar's close"
                                          f"{', or hold to the session close' if 'session' in axes['hold'] else ''}; "
                                          f"optional stop {_words([s_ for s_ in axes['stop'] if s_ != 'none'], 'or')} × ATR(14) from the entry, live inside "
                                          "each bar. Anything still open is closed at the session's last close."},
                {"label": "Size", "text": f"{sides}; one position at a time, never held overnight. As many "
                                          f"whole {sym} contracts as the account covers at full contract value (no "
                                          f"leverage), starting from ${ec.starting_equity:,.0f}."},
            ],
            "axes": [{"label": LABELS[ax], "values": [_val(ax, v) for v in vals]} for ax, vals in axes.items()],
            "grid_size": n,
            "length_note": "All lengths are in bars of the chosen bar size; the move and stop are in ATR(14).",
        },
        "funnel": funnel,
        "stable": {"n": s4.height, "axes": stable, "by_timeframe": stable_by_tf},
        "ablation": ablation,
        "length_map": length_map,
        "luck": luck,
        "finalists": finalists,
        "short_labels": SHORT,
        "exit_labels": [["time", "time", "time exit"], ["eod", "close", "session close"], ["stop", "stop", "stop"]],
        "local_moves": [[k, MOVES[k]] for k in ("lookback", "z_lookback", "entry_z", "stop_atr", "min_move_atr")],
        "benchmark": {"label": f"Holding {sym} (rolled, unlevered)", **_buy_and_hold(fcfg, sym)},
        "transfer_symbol": fcfg.confidence.transfer_symbol,
        "dsr": {"effective_trials": dsr["effective_trials"]["li_ji"], "raw_trials": dsr["trial_count_options"]["raw"]},
        "assumptions": [
            f"Data: Databento CME continuous front month ({sym}.v.0), 1-minute bars aggregated to "
            f"{_words([t.replace('min', ' minutes') for t in fcfg.data.timeframes], 'and')}. "
            "Rolls are back-adjusted so the roll gap is not treated as a price move. The ATR gap, max gap and "
            "reversal signals are point distances; the paper form divides by a back-adjusted price level, so its "
            "scale drifts slightly with the roll adjustment (the rolling z-score absorbs most of it).",
            f"Day session only: {session_spec(sym).label} on NYSE trading days. Overnight Globex trading is not used "
            "and nothing is held overnight.",
            f"Costs: {ec.slippage_ticks_market:g} tick slippage per side (stops and wick entries too) and "
            f"${ec.commission_per_contract:.2f} commission per contract per side, including the session-close exit.",
            "Windows (up to 96 bars) and the z-score history run over the day-session bars across days, so the "
            "overnight gap shows up as a jump between two closes inside a window. Positions never cross sessions.",
            "The paper tested convexity on daily closes with 5- to 21-day holds. Every look-back here is intraday, "
            "so the whole grid is an extrapolation of the paper.",
            "The reversal control is extreme almost only in the direction of its own move, so for it quadrant "
            "\"late\" nearly equals \"all\" and \"early\" rarely trades. Hold \"N bars\" equals \"to close\" once N "
            "exceeds the bars left in the session.",
            "Each trade uses the whole account in whole contracts with no leverage, the same as the other families; "
            "the stop changes where the trade exits, not how big it is.",
            "Sharpe uses daily mark-to-market returns (√252), with idle cash earning 0%. Time in market is the share "
            "of bars with an open position.",
            *(["Other strategy families were already selected on this market's 2023–2024 data, so 2023–2024 is "
               "not untouched; only the 2025+ holdout is."]
              if fcfg.data_history.validation_previously_used_for_selection else []),
            holdout_line,
        ],
        "source": f"price-path-convexity-backtest/runs/funnel/{experiment_id}/ · {config.as_posix()}",
    }
    path = out_root / sym / (f"{key}__{variant}.json" if variant else f"{key}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1))
    typer.echo(f"wrote {path}")


if __name__ == "__main__":
    app()
