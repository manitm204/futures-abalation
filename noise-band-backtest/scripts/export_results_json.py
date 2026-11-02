"""Export a finished noise-band funnel run to the JSON format the shared results site
renders (../futures-results/), the same shape as
../mean-reversion-backtest/scripts/export_results_json.py writes.

One file per (market, strategy): futures-results/data/<MARKET>/<key>.json. Re-running
overwrites that file only. Then rebuild the pages:  python ../futures-results/build.py
(writes futures-results/noise-band breakout/index.html)

Works after `develop` alone (validation columns are then empty and stage 8 shows "not
run") and again after `validate`. Reads only development and validation outputs;
holdout data is never touched.

Usage:
  PYTHONPATH=. python scripts/export_results_json.py --experiment-id nb_es_v1 \
      --config configs/funnel/nb_funnel_es_v1.yaml
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
from src.experiments.nb_grid import AXES_V1, AXES_V2, AXES_V3, AXES_V4, AXES_V5, AXES_V6, AXES_V7, AXES_V8

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = PROJECT_ROOT.parent / "futures-results"
app = typer.Typer(add_completion=False)

SPACES = {"noise_band": AXES_V1, "noise_band_v2": AXES_V2, "noise_band_v3": AXES_V3, "noise_band_v4": AXES_V4, "noise_band_v5": AXES_V5, "noise_band_v6": AXES_V6, "noise_band_v7": AXES_V7, "noise_band_v8": AXES_V8}
MARKET_NAMES = {"ES": "E-mini S&P 500", "NQ": "E-mini Nasdaq-100", "YM": "E-mini Dow", "RTY": "E-mini Russell 2000",
                "CL": "Crude oil", "GC": "Gold", "6E": "Euro FX", "6J": "Japanese yen", "ZN": "10-year T-note",
                "ZB": "30-year T-bond"}
LABELS = {
    "timeframe": "Bar size", "band_lookback": "Band lookback (days)", "band_mult": "Band multiple",
    "check_minutes": "Check every (min)", "first_entry_minutes": "First entry (min)", "anchor": "Band anchor",
    "trail": "Trailing exit", "direction": "Direction", "stop_atr_multiple": "Stop (× ATR)",
    "max_entries_per_session": "Max entries / session",
    "last_entry_cutoff_minutes": "No entries in last (min)",
    "momentum_minutes": "Momentum filter (min)",
    "max_extension": "Max entry extension (× band)",
    "rel_volume": "Relative volume (×)",
}
SHORT = {"timeframe": "Bar", "band_lookback": "Days", "band_mult": "Band", "check_minutes": "Check",
         "first_entry_minutes": "1st", "anchor": "Anchor", "trail": "Exit", "direction": "Side",
         "stop_atr_multiple": "Stop", "max_entries_per_session": "Max", "last_entry_cutoff_minutes": "Cutoff", "momentum_minutes": "Mom", "max_extension": "Ext", "rel_volume": "RVol"}


def _val(axis: str, v) -> str:
    if axis == "anchor":
        return {"open": "open", "open_prev_close": "gap-adj"}[v]
    if axis == "trail":
        return {"band": "band", "vwap": "VWAP", "band_vwap": "closer"}[v]
    if axis == "stop_atr_multiple":
        return "none" if v == "none" else f"{float(v):g}"
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
    key: str = typer.Option("", help="File name / tab id under data/<MARKET>/ (default: noise_band_<version>)"),
    label: str = typer.Option("", help="Strategy tab label (default: Noise band - <version>)"),
    variant: str = typer.Option("", help="Optional variant id (e.g. 15m) when one strategy tab holds several runs"),
    variant_label: str = typer.Option("", help="Button text for the variant (default: the variant id)"),
    out_root: Path = typer.Option(SITE_ROOT / "data"),
) -> None:
    fcfg = load_funnel_config(config)
    ec = load_execution_config(fcfg)
    axes = SPACES.get(fcfg.strategy)
    if axes is None:
        raise typer.BadParameter(f"exporter knows the noise-band grids {sorted(SPACES)} only")
    sym = fcfg.symbol
    version = experiment_id.rsplit("_", 1)[-1]
    key = key or f"noise_band_{version}"
    label = label or f"Noise band · {version}"
    exp = PROJECT_ROOT / "runs" / "funnel" / experiment_id
    summary = json.loads((exp / "summary.json").read_text())
    frozen = json.loads((exp / "frozen_representatives.json").read_text())
    val_path = exp / "validation_results.json"
    val = json.loads(val_path.read_text()) if val_path.exists() else None
    val_by_id = {r["config_id"]: r for r in val["results"]} if val else {}
    df = pl.read_parquet(exp / "config_status.parquet")
    # Mixed int/"none" axes (max entries per session) are stored as text; match their values.
    axes = {ax: tuple(str(v) for v in vals) if df.schema.get(ax) == pl.Utf8 else vals for ax, vals in axes.items()}
    for ax, vals in axes.items():  # text cells may spell a float differently ("1" vs "1.0"): use the axis spelling
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
    funnel = [
        {"name": "Start", "sub": "every combination", "n": n,
         "why": f"All {n:,} versions backtested once on {dev_w.start.year}–{dev_w.end.year} data."},
        {"name": "1 · Integrity", "sub": "no cheating", "n": st["1"]["passed"],
         "why": f"Per-trade checks for look-ahead, impossible fills and overnight holds on every version, plus "
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
         "why": f"Each setting is nudged one at a time, down and up: band lookback by ±{ps.local.int_rel:.0%} "
                f"(rounded) and band multiple by ±{ps.local.band_mult_abs:g}"
                + (f", a numeric ATR stop by ±{ps.local.stop_atr_abs:g}" if any(v != "none" for v in axes["stop_atr_multiple"]) else "")
                + f". At least {ps.min_frac_profitable:.0%} of the nudged versions must be profitable, with median "
                  f"Sharpe ≥ {ps.min_median_sharpe}. Removed {st['4a' if '4a' in st else '3']['passed'] - st['4']['passed']}."},
        {"name": "5 · Time stability", "sub": f"≥{fcfg.time_stability.min_profitable_years} profitable years",
         "n": st["5"]["passed"], "why": f"Removed {st['4']['passed'] - st['5']['passed']}."},
        {"name": "6 · Remove duplicates", "sub": f"best {fcfg.dedup.reps_per_cluster} per group", "n": st["6"]["passed"],
         "why": f"Versions whose monthly returns correlate ≥ {fcfg.dedup.corr_threshold} form a group; the best "
                f"{fcfg.dedup.reps_per_cluster} of each go on (a group of one keeps its one). "
                f"{st['5']['passed']:,} versions formed {st['6']['n_clusters']} groups; {distinct} of the "
                f"{st['6']['passed']} picks are distinct backtests (first-entry times before the first check act alike)."},
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

    # ---- random-entry ("luck") benchmark, if run (scripts/run_nb_random_benchmark.py) ----
    luck_path = exp / "random_benchmark.json"
    luck_raw = json.loads(luck_path.read_text()) if luck_path.exists() and val else None
    luck_by_id = {f["config_id"]: f for f in luck_raw["finalists"]} if luck_raw else {}
    luck = None
    if luck_raw:
        def _match(g):  # the finalists this curve is for (only axes the settings show)
            return {ax: _val(ax, luck_raw["groups"][g][ax]) for ax in ("timeframe", "direction") if len(axes[ax]) > 1}

        def _glabel(g):
            meta = luck_raw["groups"][g]
            side = "long only" if meta["direction"] == "long" else f"long + short ({meta['p_long']:.0%} long)"
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
                     "groups trade long; long-and-short groups go long with the same share of trades their "
                     "finalists did. They pay the same costs and use the same sizing and Sharpe math as the "
                     "strategy."),
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
            "exits": {"trail": d["full_n_trail_exits"], "eod": d["full_n_eod_exits"], "stop": d["full_n_stop_exits"]},
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

    # ---- band lookback x band multiple map around the top finalist (validation passer if any) ----
    top = next((f for f in finalists if f["status"] == "pass"), finalists[0] if finalists else None)
    if top is not None:
        cfg_top = by_id[next(c["config_id"] for c in frozen["candidates"] if c["dev_order"] == top["order"])]
        top_order = top["order"]
    else:
        cfg_top, top_order = df.sort("dev_sharpe", descending=True, nulls_last=True).row(0, named=True), None
    others = [a for a in axes if a not in ("band_lookback", "band_mult")]
    sub = df.filter(pl.all_horizontal([pl.col(a) == cfg_top[a] for a in others]))
    cell = {(r["band_lookback"], r["band_mult"]): r for r in sub.iter_rows(named=True)}
    rows_, cols_ = list(axes["band_lookback"]), list(axes["band_mult"])
    length_map = {
        "title": "Band lookback × band multiple", "pair_text": "band lookback and band multiple",
        "corner": "Days ↓ · Band →", "row_short": "lookback", "col_short": "band",
        "order": top_order, "fixed": {LABELS[a]: _val(a, cfg_top[a]) for a in others if len(axes[a]) > 1},
        "center": [cfg_top["band_lookback"], _val("band_mult", cfg_top["band_mult"])],
        "rows": rows_, "cols": [_val("band_mult", c) for c in cols_],
        "sharpe": [[_num(cell[(m, b)]["dev_sharpe"]) if (m, b) in cell else None for b in cols_] for m in rows_],
        "trades": [[cell[(m, b)]["dev_n_completed_trades"] if (m, b) in cell else None for b in cols_] for m in rows_],
    }

    dsr = summary["dsr"]
    stop_on = any(v != "none" for v in axes["stop_atr_multiple"])
    out = {
        "market": sym, "market_name": market_name or MARKET_NAMES.get(sym, sym),
        "strategy_key": key, "strategy_name": label,
        "variant": variant or None, "variant_label": (variant_label or variant) or None,
        "stability_mode": ps.mode,
        "validation_rules": fcfg.validation.model_dump(),
        "run_id": experiment_id, "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "periods": {"dev": [str(dev_w.start), str(dev_w.end)], "val": [str(val_w.start), str(val_w.end)]},
        "strategy": {
            "summary": ("Trade breakouts from the day's normal range, flat by the close. For every time of day the "
                        "strategy averages how far price has been from that day's open over the last N sessions; "
                        "times the band multiple, that is the noise band around today's open. At each check time a "
                        "close above the band goes long and a close below it goes short, at the next bar's open. "
                        "The position trails out through the band, the session VWAP, or whichever is closer, and is "
                        "always closed at the session's last close. After Zarattini, Aziz & Barbon (2024)."),
            "formula": ("band = open ± multiple × average |close − open| ÷ open at this time of day over the last "
                        "N sessions (× today's open)"),
            "rules": [
                {"label": "Enter", "text": "At a check time (every 15, 30 or 60 minutes from the open, and not before "
                                           "the first-entry time), buy when the bar closes above the upper band and "
                                           "sell short when it closes below the lower band. The order fills at the "
                                           "next bar's open. The gap-adjusted anchor starts the upper band from the "
                                           "higher of the open and the prior close, the lower band from the lower."},
                {"label": "Exit", "text": "At a check time, exit when price closes back through the band, through "
                                          "the session VWAP, or through whichever of the two is closer, filled at "
                                          "the next open. Anything still open is closed at the session's last close."
                                          + (" An optional stop sits k × ATR(14) from the entry." if stop_on else
                                             " No stop loss in this round.")},
                {"label": "Size", "text": f"Long, short or both; one position at a time, never held overnight"
                                          + ("; optionally capped at 1 or 2 entries per session" if
                                             "max_entries_per_session" in axes else "")
                                          + ("; optionally no new entries in the last 60 or 120 minutes" if
                                             "last_entry_cutoff_minutes" in axes else "")
                                          + ("; optionally only when the last 30 or 60 minutes moved the same way"
                                             if "momentum_minutes" in axes else "")
                                          + ("; optionally skipping breakouts already far beyond the band"
                                             if "max_extension" in axes else "")
                                          + ("; optionally only on above-normal volume"
                                             if "rel_volume" in axes else "") + ". As "
                                          f"many whole {sym} contracts as the account covers at full contract value "
                                          f"(no leverage), starting from ${ec.starting_equity:,.0f}."},
            ],
            "axes": [{"label": LABELS[ax], "values": [_val(ax, v) for v in vals]} for ax, vals in axes.items()],
            "grid_size": n,
            "length_note": "The band lookback counts trading days; check and first-entry times are minutes after the open.",
        },
        "funnel": funnel,
        "stable": {"n": s4.height, "axes": stable, "by_timeframe": stable_by_tf},
        "ablation": ablation,
        "length_map": length_map,
        "luck": luck,
        "finalists": finalists,
        "short_labels": SHORT,
        "exit_labels": [["trail", "trail", "trailing exit"], ["eod", "close", "session close"], ["stop", "stop", "stop"]],
        "local_moves": [["band_lookback", "Lookback"], ["band_mult", "Band"]] + ([["stop_atr", "Stop"]] if stop_on else []),
        "benchmark": {"label": f"Holding {sym} (rolled, unlevered)", **_buy_and_hold(fcfg, sym)},
        "transfer_symbol": fcfg.confidence.transfer_symbol,
        "dsr": {"effective_trials": dsr["effective_trials"]["li_ji"], "raw_trials": dsr["trial_count_options"]["raw"]},
        "assumptions": [
            f"Data: Databento CME continuous front month ({sym}.v.0), 1-minute bars aggregated to 5 and 15 minutes. "
            "Rolls are back-adjusted so the roll gap is not treated as a price move; the band is scaled by the real "
            "(unadjusted) open.",
            f"Day session only: {session_spec(sym).label} on NYSE trading days. Overnight Globex trading is not used: "
            "\"the open\" is the day-session open and the prior close is the previous day-session close. Nothing is "
            "held overnight.",
            f"Costs: {ec.slippage_ticks_market:g} tick slippage per side and ${ec.commission_per_contract:.2f} "
            "commission per contract per side, including the session-close exit.",
            "The paper sizes by volatility with up to 4× leverage; here each trade uses the whole account in whole "
            "contracts with no leverage, the same as the mean-reversion runs.",
            "Session VWAP is built from the 5- or 15-minute bars' typical price and volume, not ticks.",
            "After an exit, a new entry in the same direction waits until price closes back inside the band at a "
            "check time; the opposite direction isn't blocked.",
            "With no stop, 5- and 15-minute bars decide at the same check times, and a first-entry time before the "
            "first check changes nothing, so the grid contains exact duplicates; they collapse in stage 6.",
            "Sharpe uses daily mark-to-market returns (√252), with idle cash earning 0%. Time in market is the share "
            "of bars with an open position.",
            "Holdout (2025 onward) has not been run. It is a one-time final test and needs an explicit go-ahead.",
        ],
        "source": f"noise-band-backtest/runs/funnel/{experiment_id}/ · {config.as_posix()}",
    }
    path = out_root / sym / (f"{key}__{variant}.json" if variant else f"{key}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1))
    typer.echo(f"wrote {path}")


if __name__ == "__main__":
    app()
