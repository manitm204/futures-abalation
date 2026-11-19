"""Export a finished EMRT spread funnel run (a futures PAIR) to the JSON format the shared results
site renders (../futures-results/), the same shape as the convexity / squeeze exporters write.

One file per (pair, version): futures-results/data/<A-B>/emrt_spread_<version>.json.
Re-running overwrites that file only. Then rebuild the pages:  python ../futures-results/build.py
(runs go to "futures-results/emrt spread/index.html").

Works after `develop` alone (validation columns are then empty and stage 8 shows "not run") and
again after `validate`. Reads only development and validation outputs; holdout data is never touched.

Usage:
  PYTHONPATH=. python scripts/export_results_json.py --experiment-id emrt_esnq_v1 \
      --config configs/funnel/emrt_funnel_esnq_v1.yaml
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
from src.experiments.emrt_grid import AXES_EMRT_V1, AXES_EMRT_V2
from src.strategies.emrt_spread.config import split_pair
from src.experiments.funnel_config import load_execution_config, load_funnel_config

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = PROJECT_ROOT.parent / "futures-results"
app = typer.Typer(add_completion=False)

# strategy -> (axes, file-key prefix, tab label prefix, heat-map axes (rows, cols))
SPACES = {
    "emrt_spread_v1": (AXES_EMRT_V1, "emrt_spread", "EMRT spread", ("formation", "entry_z")),
    "emrt_spread_v2": (AXES_EMRT_V2, "emrt_spread", "EMRT spread", ("formation", "entry_z")),
}
MARKET_NAMES = {"ES": "E-mini S&P 500", "NQ": "E-mini Nasdaq-100", "YM": "E-mini Dow", "RTY": "E-mini Russell 2000",
                "CL": "Crude oil", "GC": "Gold", "6E": "Euro FX", "6J": "Japanese yen", "ZN": "10-year T-note",
                "ZB": "30-year T-bond"}
LABELS = {
    "timeframe": "Bar size", "formation": "Formation window (months)", "hedge": "Hedge ratio",
    "z_mode": "z-score basis", "entry_z": "Entry |z|", "exit": "Exit", "stop": "Stop (z beyond entry)",
    "time_stop": "Time stop", "side": "Side", "overnight": "Overnight", "first_entry": "First entry",
}
SHORT = {"timeframe": "Bar", "formation": "Form", "hedge": "Hedge", "z_mode": "z", "entry_z": "Entry",
         "exit": "Exit", "stop": "Stop", "time_stop": "Time", "side": "Side", "overnight": "Night",
         "first_entry": "1st"}
MOVES = {"formation": "Formation", "entry_z": "Entry z", "stop_z": "Stop", "emrt_c": "EMRT C",
         "z_window": "z window", "time_stop_mult": "Time stop"}


def _val(axis: str, v) -> str:
    if axis == "hedge":
        return {"ols": "OLS (control)", "notional": "1:1 (control)"}.get(v, f"EMRT C={v[6:]}" if str(v).startswith("emrt_c") else v)
    if axis == "z_mode":
        if v == "formation":
            return "formation"
        return f"time of day {str(v)[4:]}" if str(v).startswith("tod_") else f"rolling {str(v)[8:]}"
    if axis == "first_entry":
        return "at open" if int(v) == 0 else f"+{int(v)} min"
    if axis == "formation":
        return f"{int(v)} mo"
    if axis == "exit":
        return {"mean": "at mean", "half": "half-way"}.get(v, v)
    if axis == "stop":
        return "none" if v == "none" else f"+{float(v):g} z"
    if axis == "time_stop":
        return {"none": "none", "3emrt": "3 × EMRT"}.get(v, v)
    if axis == "side":
        return {"both": "both", "long": "long spread", "short": "short spread"}.get(v, v)
    if axis == "overnight":
        return {"flat": "flat at close", "hold": "hold"}.get(v, v)
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
        raise typer.BadParameter(f"exporter knows the EMRT spaces {sorted(SPACES)} only")
    axes, key_prefix, label_prefix, (heat_r, heat_c) = SPACES[fcfg.strategy]
    axes = {"timeframe": axes["timeframe"], **axes}  # bar size first, as on the other families' pages
    sym = fcfg.symbol
    leg_a, leg_b = split_pair(sym)
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
    nudges = (f"the formation window and a rolling z window by ±{lo.int_rel:.0%} (rounded, at least one month / bar), "
              f"the entry |z| by ±{lo.entry_z_abs:g}, a stop by ±{lo.stop_z_abs:g} z, an EMRT hedge's C by "
              f"±{lo.emrt_c_abs:g} and a time stop by ±{lo.time_stop_mult_abs:g} × EMRT (\"none\" has nothing to nudge)")
    funnel = [
        {"name": "Start", "sub": "every combination", "n": n,
         "why": f"All {n:,} versions backtested once on {dev_w.start.year}–{dev_w.end.year} data."},
        {"name": "1 · Integrity", "sub": "no cheating", "n": st["1"]["passed"],
         "why": f"Per-trade checks on every version: the spread's z was recomputed by a separate route, each hedge "
                f"was fit only on months before the trade, each entry was a fresh cross on an allowed side, no "
                f"qualifying signal was skipped while flat, both legs filled at the next open no better than the "
                f"market, exits fired at the first bar a rule did, and P&L, roll costs and sizing add up. Plus "
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

    # ---- random-entry ("luck") benchmark, if a random_benchmark.json exists (no pair version of that script yet) ----
    luck_path = exp / "random_benchmark.json"
    luck_raw = json.loads(luck_path.read_text()) if luck_path.exists() and val else None
    luck_by_id = {f["config_id"]: f for f in luck_raw["finalists"]} if luck_raw else {}
    luck = None
    if luck_raw:
        def _match(g):  # the finalists this curve is for (only axes the settings show)
            return {ax: _val(ax, luck_raw["groups"][g][ax]) for ax in ("timeframe", "side") if len(axes[ax]) > 1}

        def _glabel(g):
            meta = luck_raw["groups"][g]
            side = {"long": "long only", "short": "short only"}.get(
                meta["side"], f"long + short ({meta['p_long']:.0%} long)")
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
            "exits": {"target": d["full_n_target_exits"], "stop": d["full_n_stop_exits"], "time": d["full_n_time_exits"],
                      "eod": d["full_n_eod_exits"]},
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
        "market": sym, "market_name": market_name or f"{MARKET_NAMES.get(leg_a, leg_a)} vs {MARKET_NAMES.get(leg_b, leg_b)}",
        "strategy_key": key, "strategy_name": label,
        "variant": variant or None, "variant_label": (variant_label or variant) or None,
        "stability_mode": ps.mode,
        "validation_rules": fcfg.validation.model_dump(),
        "run_id": experiment_id, "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "periods": {"dev": [str(dev_w.start), str(dev_w.end)], "val": [str(val_w.start), str(val_w.end)]},
        "strategy": {
            "summary": (f"Trade the spread between {leg_a} and {leg_b}: long one leg, short the other, betting the gap "
                        "snaps back. The hedge ratio comes from Ning & Lee (Purdue Statistics, 2024): instead of a "
                        "regression, pick the ratio that makes the spread revert to its mean FASTEST (the empirical "
                        "mean-reversion time, EMRT). The paper used daily stock pairs; everything here is intraday "
                        "futures, so it is an extrapolation. Two plain ratios run alongside as controls: the OLS "
                        "regression slope and 1:1 dollar-neutral. If EMRT doesn't beat them, it adds nothing."),
            "formula": f"spread = ({leg_a} move ÷ {leg_a} price) − β × ({leg_b} move ÷ {leg_b} price); β = argmin EMRT",
            "rules": [
                {"label": "Hedge", "text": f"At each month start, fit β on the previous {_words([str(f) for f in axes['formation']], 'or')} "
                                           "months only. EMRT: mark every swing of at least C × the spread's sd (an "
                                           "'important extremum'), time how long each takes to get back to the mean, "
                                           f"and pick the β from 0.20 to 3.00 with the shortest average (C = "
                                           f"{_words([h[6:] for h in axes['hedge'] if h.startswith('emrt_c')], 'or')}), "
                                           "as long as the spread's variance is at most 2× the OLS spread's. Controls: "
                                           "OLS slope; β = 1."},
                {"label": "Enter", "text": "z = the spread against the formation window's mean and sd, or a rolling "
                                           f"{_words([z[8:] for z in axes['z_mode'] if z != 'formation'], 'or')}-bar window. "
                                           "A fresh cross below −entry buys the spread (long "
                                           f"{leg_a}, short β × {leg_b}); above +entry sells it. Both legs fill at the "
                                           "next bar's open. No entries in the last 30 minutes; a signal while a "
                                           "position is open is dropped."},
                {"label": "Exit", "text": "Close when z gets back to 0 (at mean) or half-way to it; optional stop once z "
                                          "runs a further 1.5 or 2.5 past the entry level; optional time stop after "
                                          "3 × the spread's EMRT. Either flat at the session's last close, or held "
                                          "across sessions (a contract roll while held costs a round turn). The open "
                                          "position keeps its entry month's hedge."},
                {"label": "Size", "text": f"Both / long spread / short spread; one position at a time. Whole {leg_a} and "
                                          f"{leg_b} contracts, the two legs' full contract value together no more than "
                                          f"the account (no leverage), starting from ${ec.starting_equity:,.0f} so the "
                                          "ratio is carried by tens of contracts."},
            ],
            "axes": [{"label": LABELS[ax], "values": [_val(ax, v) for v in vals]} for ax, vals in axes.items()],
            "grid_size": n,
            "length_note": "Formation is in months; z windows, EMRT and time stops are in bars of the chosen bar size.",
        },
        "funnel": funnel,
        "stable": {"n": s4.height, "axes": stable, "by_timeframe": stable_by_tf},
        "ablation": ablation,
        "length_map": length_map,
        "luck": luck,
        "finalists": finalists,
        "short_labels": SHORT,
        "exit_labels": [["target", "target", "z target"], ["stop", "stop", "stop"], ["time", "time", "time stop"],
                        ["eod", "close", "session close"]],
        "local_moves": [[k, v] for k, v in MOVES.items()],
        "benchmark": {"label": f"Holding {leg_a} (rolled, unlevered)", **_buy_and_hold(fcfg, leg_a)},
        "transfer_symbol": fcfg.confidence.transfer_symbol,
        "dsr": {"effective_trials": dsr["effective_trials"]["li_ji"], "raw_trials": dsr["trial_count_options"]["raw"]},
        "assumptions": [
            f"Data: Databento CME continuous front month ({leg_a}.v.0 and {leg_b}.v.0), 1-minute bars aggregated to "
            f"{_words([t.replace('min', ' minutes').replace('1h', '1 hour') for t in fcfg.data.timeframes], 'and')} and "
            "joined on bar time (a bar missing in either leg is dropped from both). Rolls are back-adjusted per leg; "
            "the spread uses only real point moves scaled by real prices.",
            f"Day session only: {session_spec(leg_a).label} for both legs, on NYSE trading days.",
            f"Costs on EACH leg: {ec.slippage_ticks_market:g} tick slippage per side (stops too) and "
            f"${ec.commission_per_contract:.2f} commission per contract per side; holding over a roll costs that leg a "
            "round turn.",
            "Unlevered across both legs, so returns are small next to a single-market strategy; a market-neutral book "
            "would normally run levered. Sharpe doesn't depend on that choice; return and drawdown scale with it.",
            "The paper tested daily stock pairs with a reinforcement-learning trader. Here a plain z band trades the "
            "spread on intraday futures bars, so the whole grid is an extrapolation of the paper.",
            "Decisions use both legs' bar closes and fill at the next bar's open on both legs.",
            "Sharpe uses daily mark-to-market returns (√252) of both legs, with idle cash earning 0%. Time in market is "
            "the share of bars with an open position.",
            f"Benchmark row: holding {leg_a} alone, for scale; the spread is roughly market-neutral and not trying to beat it.",
            *(["Other strategy families were already selected on these legs' 2023–2024 data, so 2023–2024 is "
               "not untouched; only the 2025+ holdout is (and single-market picks were already scored on it)."]
              if fcfg.data_history.validation_previously_used_for_selection else []),
            holdout_line,
        ],
        "source": f"emrt-spread-backtest/runs/funnel/{experiment_id}/ · {config.as_posix()}",
    }
    if fcfg.strategy == "emrt_spread_v2":  # session-anchored, intraday-only round
        st_ = out["strategy"]
        st_["summary"] = (f"Trade the INTRADAY spread between {leg_a} and {leg_b}, flat by the close every day (no overnight "
                          f"holds). Each leg is measured from that day's open, so the spread starts at 0 each session; when "
                          f"{leg_a} runs ahead of or behind β × {leg_b} by an unusual amount, bet on the gap closing before "
                          "the close. β comes from Ning & Lee (Purdue Statistics, 2024): the ratio whose spread reverts "
                          "fastest (the empirical mean-reversion time, EMRT), fit monthly on these intraday spreads. The "
                          "OLS slope and 1:1 run alongside as controls. Designed after v1, whose flat-at-close versions all "
                          "failed because its multi-day spread rarely reverted within the day.")
        st_["formula"] = (f"spread = ({leg_a} − today's {leg_a} open) ÷ open − β × ({leg_b} − today's {leg_b} open) ÷ open; "
                          "β = argmin EMRT")
        st_["rules"][0]["text"] = st_["rules"][0]["text"].replace(
            "time how long each takes to get back to the mean,",
            "time how long each takes to get back to the mean within the same session (a swing still open at the close "
            "counts until the close),")
        st_["rules"][1]["text"] = ("z = the spread against the formation window's mean and sd, or by time of day: against "
                                   f"the same bar of the last {_words([z[4:] for z in axes['z_mode'] if z.startswith('tod_')], 'or')} "
                                   "sessions. A fresh cross below −entry buys the spread (long "
                                   f"{leg_a}, short β × {leg_b}); above +entry sells it. Both legs fill at the next bar's "
                                   "open. Optionally no entries in the first 30 minutes; none in the last 30; a signal "
                                   "while a position is open is dropped.")
        st_["rules"][2]["text"] = ("Close when z gets back to 0 (at mean) or half-way to it; optional stop once z runs a "
                                   "further 1.5 past the entry level; optional time stop after 3 × the spread's EMRT. "
                                   "Anything still open is closed at the session's last close: never held overnight.")
        st_["length_note"] = "Formation is in months; time-of-day windows are in sessions; EMRT and time stops are in bars."
        out["assumptions"] = [a.replace("The paper tested daily stock pairs with a reinforcement-learning trader. Here a plain z band trades the spread on intraday futures bars,",
                                        "The paper tested daily stock pairs with a reinforcement-learning trader. Here a plain z band trades a session-anchored intraday spread,")
                              for a in out["assumptions"]]
        out["assumptions"].insert(3, "Every position is closed at the session's last close, so nothing is held overnight "
                                     "and no trade crosses a contract roll (prop-firm compatible).")
    path = out_root / sym / (f"{key}__{variant}.json" if variant else f"{key}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1))
    typer.echo(f"wrote {path}")


if __name__ == "__main__":
    app()
