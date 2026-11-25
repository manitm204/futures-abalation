"""Export a finished NY-open sweep funnel run to the JSON format the shared results site renders
(../futures-results/), the same shape as the drift-burst, FX-fix and convexity exporters write.

One file per (market, version): futures-results/data/<MARKET>/open_sweep_<version>.json.
Re-running overwrites that file only. Then rebuild the pages:  python ../futures-results/build.py
(runs go to "futures-results/ny open sweep/index.html").

Works after `develop` alone (validation columns are then empty and stage 8 shows "not run") and
again after `validate`. Reads only development and validation outputs; holdout data is never touched.

Usage:
  PYTHONPATH=. python scripts/export_results_json.py --experiment-id os_nq_v1 \
      --config configs/funnel/os_funnel_nq_v1.yaml
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import polars as pl
import typer

from src.experiments.os_grid import AXES_OS_GC_V2, AXES_OS_V1
from src.experiments.funnel_config import load_execution_config, load_funnel_config

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = PROJECT_ROOT.parent / "futures-results"
app = typer.Typer(add_completion=False)

# strategy -> (axes, file-key prefix, tab label prefix, heat-map axes (rows, cols))
SPACES = {
    "open_sweep_v1": (AXES_OS_V1, "open_sweep", "NY-open sweep", ("level", "mode")),
    "open_sweep_gc_v2": (AXES_OS_GC_V2, "open_sweep_gc", "NY-open sweep", ("level", "side")),
}
MARKET_NAMES = {"ES": "E-mini S&P 500", "NQ": "E-mini Nasdaq-100", "YM": "E-mini Dow", "RTY": "E-mini Russell 2000",
                "CL": "Crude oil", "GC": "Gold", "6E": "Euro FX", "6J": "Japanese yen", "ZN": "10-year T-note",
                "ZB": "30-year T-bond"}
LABELS = {
    "timeframe": "Bar size", "level": "Level swept", "side": "Side", "window": "Window after 09:30 (min)",
    "pen": "Penetration (× dATR)", "confirm": "Confirm bars", "mode": "Mode", "stop": "Stop",
    "target": "Target", "exit": "Time exit (ET)",
}
SHORT = {"timeframe": "Bar", "level": "Level", "side": "Side", "window": "Win", "pen": "Pen", "confirm": "Conf",
         "mode": "Mode", "stop": "Stop", "target": "Target", "exit": "Exit"}
MOVES = {"window": "Window", "exit": "Exit", "pen": "Pen", "confirm": "Confirm", "stop": "Stop", "target": "Target"}


def _val(axis: str, v) -> str:
    if axis == "level":
        return {"onh": "overnight", "asia": "Asia", "lon": "London", "box": "08:00 box",
                "pdr": "prior day"}.get(v, v)
    if axis == "mode":
        return {"fade": "fade (ICT)", "cont": "continuation"}.get(v, v)
    if axis == "stop":
        return "structure" if v == "struct" else f"{float(v[1:]):g} dATR"
    if axis == "pen":
        return f"{float(v):g}"
    if axis == "timeframe":
        return "1 min"
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
    back-adjusted close / previous raw (unadjusted) close. Closes of the strategy's 09:30-16:00 ET window."""
    base = PROJECT_ROOT / fcfg.data.clean_root / f"symbol={symbol}" / "timeframe=1min"
    last_year = fcfg.data.validation.end.year
    files = [p for p in base.rglob("*.parquet") if int(p.parts[-3].split("=")[1]) <= last_year]
    ny = pl.col("bar_open_ts_ny")
    df = (pl.concat([pl.read_parquet(p, columns=["session_date_ny", "bar_open_ts", "bar_open_ts_ny", "close",
                                                   "price_adjustment"]) for p in files])
          .filter((ny.dt.hour().cast(pl.Int32) * 60 + ny.dt.minute().cast(pl.Int32) >= 570) & (ny.dt.hour() < 16)
                  & (ny.dt.date() == pl.col("session_date_ny")))
          .sort("bar_open_ts")
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
    key: str = typer.Option("", help="File name / tab id under data/<MARKET>/ (default: open_sweep_<version>)"),
    label: str = typer.Option("", help="Strategy tab label (default: NY-open sweep · <version>)"),
    variant: str = typer.Option("", help="Optional variant id (e.g. 15m) when one strategy tab holds several runs"),
    variant_label: str = typer.Option("", help="Button text for the variant (default: the variant id)"),
    out_root: Path = typer.Option(SITE_ROOT / "data"),
    note: str = typer.Option("", help="Extra first line for the page's assumptions (e.g. a diagnostic-only run)"),
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
        raise typer.BadParameter(f"exporter knows the open-sweep spaces {sorted(SPACES)} only")
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
    nudges = (f"the window by ±{lo.entry_shift_abs} minutes, the time exit by ±{lo.exit_shift_abs} minutes "
              f"(never after 16:00), the penetration by ±{lo.threshold_abs:g} dATR, confirm by ±1 bar, a dATR stop by "
              f"±{lo.stop_pct_abs:g} and an R target by ±{lo.target_r_abs:g}R (structural stops and none/range "
              "targets have nothing to nudge)")
    funnel = [
        {"name": "Start", "sub": "every combination", "n": n,
         "why": f"All {n:,} versions backtested once on {dev_w.start.year}–{dev_w.end.year} data."},
        {"name": "1 · Integrity", "sub": "no cheating", "n": st["1"]["passed"],
         "why": f"Per-trade checks on every version: every pre-open level (overnight, Asia, London, 08:00 box) was "
                f"recomputed from the raw Globex bars with plain loops, and the prior day's range and dATR independently; "
                f"each trade's sweep, trigger, side, entry bar, stop, target and exit were re-derived; fills were never "
                f"better than the market; one trade a session; nothing held overnight. Plus "
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

    # ---- random-entry ("luck") benchmark, if run (scripts/run_me_random_benchmark.py) ----
    luck_path = exp / "random_benchmark.json"
    luck_raw = json.loads(luck_path.read_text()) if luck_path.exists() and val else None
    luck_by_id = {f["config_id"]: f for f in luck_raw["finalists"]} if luck_raw else {}
    luck = None
    if luck_raw:
        def _split(g):
            w, stop = g.split("|")[1].rsplit("-", 1)
            return w, stop

        def _match(g):  # the finalists this curve is for (only axes the settings show)
            w, stop = _split(g)
            return {"window": _val("window", w), "stop": _val("stop", stop)}

        def _glabel(g):
            w, stop = _split(g)
            return f"{_val('window', w)} · stop {_val('stop', stop)}"
        luck = {
            "n_sims": luck_raw["n_sims"], "levels": luck_raw["levels"], "method": luck_raw["method"],
            "curves": [{"timeframe": _glabel(g), "match": _match(g), "rows": rows,
                        "trade_bars": [luck_raw["groups"][g]["median_trade_bars"], luck_raw["groups"][g]["mean_trade_bars"]],
                        "p_long": luck_raw["groups"][g]["p_long"]}
                       for g, rows in luck_raw["curves"].items()],
            "text": (f"For every whole-percent time in market in each group's {val_w.start.year}–{val_w.end.year} "
                     f"range, {luck_raw['n_sims']} random runs trade {sym} in the same window with the same stop, "
                     "but on random days and long or short by a coin flip. So they test whether the signal (which "
                     "days to trade and which way) beats chance at the same hours. Each group is one trade window and "
                     "stop setting. They pay the same costs and use the same sizing and Sharpe math as the strategy."),
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
            "exits": {"time": d["full_n_time_exits"], "eod": d["full_n_eod_exits"], "stop": d["full_n_stop_exits"],
                      "target": d["full_n_target_exits"]},
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
            "summary": ("ICT's NY-open liquidity sweep (the Judas swing, the 2025 \"Venom\" model): in the first "
                        "minutes after 09:30, price runs through an obvious pool of resting stops above or below a "
                        "level set before the open, then reverses. ICT trades the reversal (fade). Independent tests "
                        "disagree on direction (a walk-forward FX study found swept levels predicted continuation in 65 "
                        "of 66 folds), so every setting also runs as a continuation trade with the break, as a control. "
                        "Picked as rank 1 of the ICT research survey (reports/ICT strategies to backtest.md)."),
            "formula": "sweep of a pre-open high/low after 09:30 → fade: close back inside, trade against it; "
                       "continuation: N closes beyond, trade with it",
            "rules": [
                {"label": "Level", "text": "A range known before 09:30: overnight (18:00–09:30), Asia (20:00–00:00), "
                                           "London (02:00–05:00), the 08:00–09:30 box, or the prior day's 09:30–16:00 "
                                           "high/low. Each pre-open range needs bars for at least half its minutes."},
                {"label": "Sweep", "text": "Within 15, 30 or 60 minutes of 09:30 a bar trades beyond the high (or low) by "
                                           "more than 0 or 0.05 × dATR (dATR = average 09:30–16:00 range of the previous "
                                           "14 days). The 09:30 open must be inside the range on that side. Side: high "
                                           "only, low only, or whichever triggers first."},
                {"label": "Trigger", "text": "Fade: the first close back inside within 1, 3 or 5 bars → trade against "
                                             "the sweep. Continuation: 1, 3 or 5 straight closes beyond the level → "
                                             "trade with the break."},
                {"label": "Enter", "text": "At the open of the next 1-minute bar, one trade a session."},
                {"label": "Exit", "text": "Stop beyond the sweep's extreme (+2 ticks) or 0.1 / 0.2 dATR away, never "
                                          "closer than 0.03 dATR, checked first within a bar. Target none, 1R, 2R, 3R or "
                                          "the range (a limit needing a 1-tick trade-through). Otherwise out at 11:00, "
                                          "12:30 or 16:00."},
                {"label": "Size", "text": f"Never held overnight. As many whole {sym} contracts as the account covers "
                                          f"at full contract value (no leverage), starting from ${ec.starting_equity:,.0f}."},
            ],
            "axes": [{"label": LABELS[ax], "values": [_val(ax, v) for v in vals]} for ax, vals in axes.items()],
            "grid_size": n,
            "length_note": "Times are New York clock times. Levels use the full Globex 1-minute bars; trading uses 09:30–16:00 ET.",
        },
        "funnel": funnel,
        "stable": {"n": s4.height, "axes": stable, "by_timeframe": stable_by_tf},
        "ablation": ablation,
        "length_map": length_map,
        "luck": luck,
        "finalists": finalists,
        "short_labels": SHORT,
        "exit_labels": [["time", "time", "time exit"], ["eod", "close", "16:00 close"], ["stop", "stop", "stop"],
                        ["target", "target", "target"]],
        "local_moves": [[k, MOVES[k]] for k in ("window", "exit", "pen", "confirm", "stop", "target")],
        "benchmark": {"label": f"Holding {sym} (rolled, unlevered)", **_buy_and_hold(fcfg, sym)},
        "transfer_symbol": fcfg.confidence.transfer_symbol,
        "dsr": {"effective_trials": dsr["effective_trials"]["li_ji"], "raw_trials": dsr["trial_count_options"]["raw"]},
        "assumptions": [
            *([note] if note else []),
            f"Data: Databento CME continuous front month ({sym}.v.0), 1-minute bars from 09:30 to 16:00 ET only. "
            "Rolls are back-adjusted; positions never cross a session. The previous close is the last regular-session "
            "bar's close, not the 17:00 settlement.",
            f"Costs: {ec.slippage_ticks_market:g} tick slippage per side and ${ec.commission_per_contract:.2f} "
            "commission per contract per side.",
            "Levels come from the full 24-hour Globex bars (the session's evening bars from 18:00 belong to the "
            "next day's session). The prior day's range uses 09:30–16:00 only. A level with bars for under half its "
            "minutes is skipped for that day.",
            "ICT definitions vary between teachers; these rules are one mechanical reading fixed before the run. "
            "The report's 432-cell grid was widened to 24,300 before any run, which makes the deflated-Sharpe "
            "correction larger.",
            "Close to the noise-band strategy in spirit (continuation of an opening break), so what matters for adding "
            "it is its daily profit correlation with the noise-band picks, not only its own Sharpe. Measured after "
            "validation: median correlation about 0.12 (2018–2022) and 0.14 (2023–2024).",
            "Each trade uses the whole account in whole contracts with no leverage, the same as the other families.",
            "Sharpe uses daily mark-to-market returns (√252), with idle cash earning 0%. Time in market is the share "
            "of 1-minute bars with an open position.",
            *(["Other strategy families were already selected on this market's 2023–2024 data, so 2023–2024 is "
               "not untouched; only the 2025+ holdout is."]
              if fcfg.data_history.validation_previously_used_for_selection else []),
            holdout_line,
        ],
        "source": f"ny-open-sweep-backtest/runs/funnel/{experiment_id}/ · {config.as_posix()}",
    }
    path = out_root / sym / (f"{key}__{variant}.json" if variant else f"{key}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1))
    typer.echo(f"wrote {path}")


if __name__ == "__main__":
    app()
