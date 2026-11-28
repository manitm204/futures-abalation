"""Export a finished drift-burst funnel run to the JSON format the shared results site renders
(../futures-results/), the same shape as the FX-fix, convexity and squeeze exporters write.

One file per (market, version): futures-results/data/<MARKET>/drift_burst_<version>.json.
Re-running overwrites that file only. Then rebuild the pages:  python ../futures-results/build.py
(runs go to "futures-results/drift burst/index.html").

Works after `develop` alone (validation columns are then empty and stage 8 shows "not run") and
again after `validate`. Reads only development and validation outputs; holdout data is never touched.

Usage:
  PYTHONPATH=. python scripts/export_results_json.py --experiment-id db_es_v1 \
      --config configs/funnel/db_funnel_es_v1.yaml
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
from src.experiments.db_grid import AXES_DB_V1, AXES_DB_V2, AXES_DB_V3
from src.experiments.funnel_config import load_execution_config, load_funnel_config

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = PROJECT_ROOT.parent / "futures-results"
app = typer.Typer(add_completion=False)

# strategy -> (axes, file-key prefix, tab label prefix, heat-map axes (rows, cols))
SPACES = {
    "drift_burst_v1": (AXES_DB_V1, "drift_burst", "Drift burst", ("threshold", "vol_gate")),
    "drift_burst_v2": (AXES_DB_V2, "drift_burst", "Drift burst", ("threshold", "vol_gate")),
    "drift_burst_v3": (AXES_DB_V3, "drift_burst", "Drift burst", ("threshold", "vol_gate")),
}
MARKET_NAMES = {"ES": "E-mini S&P 500", "NQ": "E-mini Nasdaq-100", "YM": "E-mini Dow", "RTY": "E-mini Russell 2000",
                "CL": "Crude oil", "GC": "Gold", "6E": "Euro FX", "6J": "Japanese yen", "ZN": "10-year T-note",
                "ZB": "30-year T-bond"}
LABELS = {
    "timeframe": "Bar size", "burst_window": "Burst window (min)", "threshold": "Burst threshold |T|",
    "vol_gate": "Volume gate (× normal)", "side": "Side", "hold": "Hold (min)", "news_filter": "News filter",
    "entry_mode": "Entry timing", "target": "Target (× burst move)", "stop": "Stop (× burst move)",
    "max_trades": "Max trades a day",
}
SHORT = {"timeframe": "Bar", "burst_window": "k", "threshold": "|T|", "vol_gate": "Vol", "side": "Side",
         "hold": "Hold", "news_filter": "News", "entry_mode": "Entry", "target": "Tgt", "stop": "Stop",
         "max_trades": "Max/day"}
MOVES = {"burst_window": "Window", "hold": "Hold", "threshold": "Threshold", "vol_gate": "Vol gate",
         "target": "Target", "stop": "Stop", "max_trades": "Max/day"}


def _val(axis: str, v) -> str:
    if axis == "vol_gate":
        return "none" if v == "none" else f"≥{float(v):g}×"
    if axis == "side":
        return {"both": "fade both", "long_only": "buy drops only"}.get(v, v)
    if axis == "news_filter":
        return {"off": "off", "on": "skip news"}.get(v, v)
    if axis == "entry_mode":
        return {"cross": "on the cross", "peak": "after the peak", "confirm": "after 2 falling bars"}.get(v, v)
    if axis in ("target", "stop"):
        return "none" if v == "none" else f"{float(v):g}×"
    if axis == "max_trades":
        return f"{int(v)} a day"
    if axis in ("burst_window", "hold"):
        return f"{int(v)} min"
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
    key: str = typer.Option("", help="File name / tab id under data/<MARKET>/ (default: drift_burst_<version>)"),
    label: str = typer.Option("", help="Strategy tab label (default: Drift burst · <version>)"),
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
        raise typer.BadParameter(f"exporter knows the drift-burst spaces {sorted(SPACES)} only")
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
    nudges = (f"the burst window and the hold by ±{lo.int_rel:.0%} (rounded, at least one minute), the threshold "
              f"by ±{lo.threshold_abs:g} and a volume gate by ±{lo.vol_gate_abs:g}× (\"no gate\" has nothing to nudge)")
    funnel = [
        {"name": "Start", "sub": "every combination", "n": n,
         "why": f"All {n:,} versions backtested once on {dev_w.start.year}–{dev_w.end.year} data."},
        {"name": "1 · Integrity", "sub": "no cheating", "n": st["1"]["passed"],
         "why": f"Per-trade checks on every version: the burst statistic, the time-of-day volume norm and the "
                f"news windows were recomputed independently; each trade followed a burst peak above the threshold "
                f"on the fade side with every filter met, at most one a day; no qualifying burst was skipped while "
                f"flat; fills were never better than the market; nothing was held overnight. Plus "
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

    # ---- random-entry ("luck") benchmark, if run (scripts/run_db_random_benchmark.py) ----
    luck_path = exp / "random_benchmark.json"
    luck_raw = json.loads(luck_path.read_text()) if luck_path.exists() and val else None
    luck_by_id = {f["config_id"]: f for f in luck_raw["finalists"]} if luck_raw else {}
    luck = None
    if luck_raw:
        def _match(g):  # the finalists this curve is for (only axes the settings show)
            meta = luck_raw["groups"][g]
            return {"side": _val("side", meta["direction"])}

        def _glabel(g):
            meta = luck_raw["groups"][g]
            side = {"long_only": "long only"}.get(meta["direction"], f"long + short ({meta['p_long']:.0%} long)")
            return f"{_val('side', meta['direction'])} · {side}"
        luck = {
            "n_sims": luck_raw["n_sims"], "levels": luck_raw["levels"], "method": luck_raw["method"],
            "curves": [{"timeframe": _glabel(g), "match": _match(g), "rows": rows,
                        "trade_bars": [luck_raw["groups"][g]["median_trade_bars"], luck_raw["groups"][g]["mean_trade_bars"]],
                        "p_long": luck_raw["groups"][g]["p_long"]}
                       for g, rows in luck_raw["curves"].items()],
            "text": (f"For every whole-percent time in market in each group's {val_w.start.year}–{val_w.end.year} "
                     f"range, {luck_raw['n_sims']} random runs trade {sym} at random times of the day session "
                     "on random days, so they test whether the burst trigger matters. Each group is one side setting. Like the strategy, the random trades are "
                     "intraday only, never overlap, and are always closed by the session's last bar. Their lengths "
                     "are drawn from that group's own finalist trades, so trade counts and costs match. Buy-drops-only "
                     "groups trade long; fade-both groups go long with the same "
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
            "exits": {"time": d["full_n_time_exits"], "eod": d["full_n_eod_exits"], "stop": d["full_n_stop_exits"],
                      **({"target": d["full_n_target_exits"]} if "full_n_target_exits" in d else {})},
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
            "summary": ("Fade sudden, outsized moves a few minutes after they peak, day session only. Christensen, "
                        "Oomen & Renò (\"The drift burst hypothesis\") find that short bursts of extreme drift in "
                        "futures (about one a week in ES at their settings) mostly reverse within minutes: about 71% "
                        "reverse over the next 5 minutes, drops more than spikes, and bursts on heavy volume for the "
                        "time of day reverse most. Their study used tick data to 2017, mid-quotes and no costs; this "
                        "is a simplified 1-minute version on traded prices."),
            "formula": "T = k-minute log return ÷ (local volatility × √k); fade when |T| peaks above the threshold",
            "rules": [
                {"label": "Signal", "text": "Over the last k minutes ("
                                            f"{_words([str(k) for k in axes['burst_window']], 'or')}): the log return, "
                                            "divided by the volatility of the 5k one-minute returns just before it "
                                            "(scaled by √k). Everything stays inside one day session."},
                {"label": "Enter", "text": "When |T| has been above the threshold ("
                                           f"{_words([f'{c:g}' for c in axes['threshold']], 'or')}) and stops rising, "
                                           "trade against the burst at the next bar's open. Optional filters: the "
                                           "burst window's volume must be at least "
                                           f"{_words([f'{float(g):g}×' for g in axes['vol_gate'] if g != 'none'], 'or')} "
                                           "the normal volume for those minutes of the day (20-day average); buy "
                                           "drops only; skip bursts around 08:30 and 10:00 ET releases and on "
                                           "Wednesdays 14:00–15:00 ET. At most one trade per day."},
                {"label": "Exit", "text": f"After {_words([str(h) for h in axes['hold']], 'or')} minutes at that "
                                          "bar's close, or at the session's last close if sooner. No stop."},
                *([{"label": "v2 additions", "text": "Entry timing: fade as soon as |T| crosses the threshold, "
                                                    "one bar after it peaks (v1), or after two falling bars. "
                                                    "Optional profit target at 0.5× or 1.0× the burst move "
                                                    "back from the entry, and optional stop 1.0× the burst move "
                                                    "beyond it (a bar touching both counts as the stop). Up to "
                                                    "1 or 3 trades a day."}] if "entry_mode" in axes else []),
                {"label": "Size", "text": f"One position at a time, never held overnight. As many whole {sym} "
                                          f"contracts as the account covers at full contract value (no leverage), "
                                          f"starting from ${ec.starting_equity:,.0f}."},
            ],
            "axes": [{"label": LABELS[ax], "values": [_val(ax, v) for v in vals]} for ax, vals in axes.items()],
            "grid_size": n,
            "length_note": "Windows and holds are in 1-minute bars of the day session.",
        },
        "funnel": funnel,
        "stable": {"n": s4.height, "axes": stable, "by_timeframe": stable_by_tf},
        "ablation": ablation,
        "length_map": length_map,
        "luck": luck,
        "finalists": finalists,
        "short_labels": SHORT,
        "exit_labels": [["time", "time", "time exit"], ["eod", "close", "session close"], ["stop", "stop", "stop"],
                        *([["target", "target", "target"]] if "entry_mode" in axes else [])],
        "local_moves": [[k, MOVES[k]] for k in ("burst_window", "hold", "threshold", "vol_gate", "target", "stop",
                                                  "max_trades")],
        "benchmark": {"label": f"Holding {sym} (rolled, unlevered)", **_buy_and_hold(fcfg, sym)},
        "transfer_symbol": fcfg.confidence.transfer_symbol,
        "dsr": {"effective_trials": dsr["effective_trials"]["li_ji"], "raw_trials": dsr["trial_count_options"]["raw"]},
        "assumptions": [
            f"Data: Databento CME continuous front month ({sym}.v.0), 1-minute bars of the day session only "
            f"({session_spec(sym).label}). Rolls are back-adjusted; positions never cross a session.",
            f"Costs: {ec.slippage_ticks_market:g} tick slippage per side and ${ec.commission_per_contract:.2f} "
            "commission per contract per side. Entries come right after a violent minute, so real slippage may "
            "be worse than one tick.",
            "The paper used a kernel-smoothed drift estimator on tick data (2010/2012–2017), measured mid-quote "
            "returns and reported no trading costs. This 1-minute version is a simplification on traded prices.",
            "The volume gate is a fixed multiple of normal time-of-day volume; the paper sorted events into volume "
            "quartiles after the fact, which needs hindsight.",
            "The first 6k minutes of each session cannot produce a burst (the volatility window needs them).",
            "Fading bursts is the same direction of bet as the mean-reversion family; check the daily P&L "
            "correlation with those finalists before adding a survivor.",
            "Each trade uses the whole account in whole contracts with no leverage, the same as the other families.",
            "Sharpe uses daily mark-to-market returns (√252), with idle cash earning 0%. Time in market is the share "
            "of 1-minute bars with an open position.",
            *(["Other strategy families were already selected on this market's 2023–2024 data, so 2023–2024 is "
               "not untouched; only the 2025+ holdout is."]
              if fcfg.data_history.validation_previously_used_for_selection else []),
            holdout_line,
        ],
        "source": f"drift-burst-backtest/runs/funnel/{experiment_id}/ · {config.as_posix()}",
    }
    path = out_root / sym / (f"{key}__{variant}.json" if variant else f"{key}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1))
    typer.echo(f"wrote {path}")


if __name__ == "__main__":
    app()
