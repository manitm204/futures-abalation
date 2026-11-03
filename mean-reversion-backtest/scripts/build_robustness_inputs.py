"""Deeper look at parameter robustness: ~30 ways to measure how a finalist's training
(2018-22) results hold up when its settings move, each tested against validation (2023-24)
with the same within-market method as build_selection_model.py.

Sources, all training-period only:
  - local moves: the funnel's stage-4 test (each numeric setting moved one step down and up,
    one at a time; `local_detail` in representatives.json)
  - the full grid of the finalist's run (records.parquet): one step on every numeric axis at
    once ("cube"), two steps ("wide cube"), and the same settings with the other mean type /
    entry confirmation ("twins"). Grid versions with no trades count as Sharpe 0.
  - the funnel's random nudges (perturb_*).

Needs runs/funnel/selection_model_v1/finalists.parquet (from build_selection_model.py).
Writes runs/funnel/selection_model_v1/robustness.{parquet,json}.

Usage:
  PYTHONPATH=. python scripts/build_robustness_inputs.py [--n-boot 500]
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import typer

import scripts.build_selection_model as sm

RUNS = sm.RUNS
OUT = sm.OUT
app = typer.Typer(add_completion=False)

NUM_AXES = ["mean_lookback", "std_lookback", "entry_z", "exit_z", "max_holding_bars", "stop_atr_multiple"]
CAT_AXES = ["timeframe", "mean_type", "entry_confirmation", "has_stop"]
AXIS_OF = {"mean_lookback": "lookback", "std_lookback": "lookback", "entry_z": "entry", "exit_z": "exit",
           "max_hold": "exit", "stop_atr": "stop"}

G_LOCAL, G_SHAPE, G_GRID, G_TWIN, G_NUDGE = ("One-step moves (funnel's test)", "Shape of the peak",
                                            "Full grid around it", "Other-variant twins", "Random nudges")
INPUTS = [
    ("local_median_sharpe", "Median Sharpe of one-step moves (funnel's ranking)", G_LOCAL),
    ("local_min_sharpe", "Worst one-step move's Sharpe", G_LOCAL),
    ("local_max_sharpe", "Best one-step move's Sharpe", G_LOCAL),
    ("local_sd_sharpe", "Spread (std) of one-step moves' Sharpe", G_LOCAL),
    ("local_frac_profitable", "Share of one-step moves profitable", G_LOCAL),
    ("local_frac_075", "Share of one-step moves with Sharpe >= 0.75", G_LOCAL),
    ("local_retention", "Moves' median Sharpe / own Sharpe", G_LOCAL),
    ("local_min_return", "Worst one-step move's return", G_LOCAL),
    ("worst_axis_sharpe", "Worst setting: mean of its down/up moves", G_LOCAL),
    ("trades_sensitivity", "How much trade count shifts across moves", G_LOCAL),
    ("lookback_moves_sharpe", "Mean Sharpe when lookbacks move", G_LOCAL),
    ("entry_moves_sharpe", "Mean Sharpe when entry z moves", G_LOCAL),
    ("exit_moves_sharpe", "Mean Sharpe when exit z / max hold move", G_LOCAL),
    ("stop_moves_sharpe", "Mean Sharpe when the stop moves (stop strategies)", G_LOCAL),
    ("local_peak", "Own Sharpe minus moves' median (peakiness)", G_SHAPE),
    ("share_moves_better", "Share of moves better than itself (not at the top)", G_SHAPE),
    ("local_slope", "Steepness: avg |up - down| gap per setting", G_SHAPE),
    ("local_curvature", "Curvature: own minus avg of down/up, per setting", G_SHAPE),
    ("neighbor_median_sharpe", "Grid one-step neighbours: median Sharpe", G_GRID),
    ("neighbor_frac_profitable", "Grid one-step neighbours: share profitable", G_GRID),
    ("cube_median_sharpe", "Grid cube (all settings +-1 step): median Sharpe", G_GRID),
    ("cube_p10_sharpe", "Grid cube: 10th-percentile Sharpe", G_GRID),
    ("cube_frac_profitable", "Grid cube: share profitable", G_GRID),
    ("cube_frac_075", "Grid cube: share with Sharpe >= 0.75", G_GRID),
    ("cube_own_pct", "Own Sharpe's percentile inside the cube", G_GRID),
    ("wide_median_sharpe", "Wide grid cube (+-2 steps): median Sharpe", G_GRID),
    ("twin_mean_type_sharpe", "Same settings, other mean type (SMA/EMA): Sharpe", G_TWIN),
    ("twin_confirm_sharpe", "Same settings, other entry confirmation: Sharpe", G_TWIN),
    ("perturb_median_sharpe", "Random nudges: median Sharpe", G_NUDGE),
    ("perturb_p10_sharpe", "Random nudges: 10th-percentile Sharpe", G_NUDGE),
    ("perturb_frac_profitable", "Random nudges: share profitable", G_NUDGE),
]


def _local(own: float, own_trades: float, detail: list[dict]) -> dict:
    s = np.array([d["sharpe"] if d["sharpe"] is not None else 0.0 for d in detail], float)
    if not len(s):
        return {}
    ret = np.array([d["net_return"] or 0.0 for d in detail], float)
    tr = np.array([d["trades"] or 0 for d in detail], float)
    by_axis, by_set = {}, {}
    for d, v in zip(detail, s):
        name = d["move"].split("=")[0]
        by_set.setdefault(name, []).append(v)
        by_axis.setdefault(AXIS_OF.get(name, name), []).append(v)
    pairs = [v for v in by_set.values() if len(v) == 2]
    med = float(np.median(s))
    return {
        "local_median_sharpe": med, "local_min_sharpe": float(s.min()), "local_max_sharpe": float(s.max()),
        "local_sd_sharpe": float(s.std()), "local_frac_profitable": float(np.mean(ret > 0)),
        "local_frac_075": float(np.mean(s >= 0.75)), "local_retention": med / own if own else np.nan,
        "local_min_return": float(ret.min()),
        "worst_axis_sharpe": float(min(np.mean(v) for v in by_set.values())),
        "trades_sensitivity": float(tr.std() / own_trades) if own_trades else np.nan,
        "lookback_moves_sharpe": float(np.mean(by_axis["lookback"])) if "lookback" in by_axis else np.nan,
        "entry_moves_sharpe": float(np.mean(by_axis["entry"])) if "entry" in by_axis else np.nan,
        "exit_moves_sharpe": float(np.mean(by_axis["exit"])) if "exit" in by_axis else np.nan,
        "stop_moves_sharpe": float(np.mean(by_axis["stop"])) if "stop" in by_axis else np.nan,
        "local_peak": own - med, "share_moves_better": float(np.mean(s > own)),
        "local_slope": float(np.mean([abs(a - b) for a, b in pairs])) if pairs else np.nan,
        "local_curvature": float(np.mean([own - (a + b) / 2 for a, b in pairs])) if pairs else np.nan,
    }


def _grid_inputs(run: str, cids: list[str]) -> dict[str, dict]:
    rec = pd.read_parquet(RUNS / run / "records.parquet")
    rec = rec.assign(has_stop=rec["stop_atr_multiple"].astype(str).str.lower() != "none",
                     sh=rec["dev_sharpe"].fillna(0.0).to_numpy(float))
    # index of each version's value along every numeric axis ("none" stop -> -1, matches only itself)
    idx = {}
    for a in NUM_AXES:
        vals = rec[a].astype(str)
        num = pd.to_numeric(vals, errors="coerce")
        order = {v: i for i, v in enumerate(sorted(num.dropna().unique()))}
        idx[a] = np.array([order[x] if np.isfinite(x) else -1 for x in num])
    I = np.column_stack([idx[a] for a in NUM_AXES])
    cat = rec[CAT_AXES].astype(str).agg("|".join, axis=1).to_numpy()
    sh = rec["sh"].to_numpy()
    pos = {c: i for i, c in enumerate(rec["config_id"])}
    other = {"mean_type": {"sma": "ema", "ema": "sma"},
             "entry_confirmation": {"none": "positive_bar_return", "positive_bar_return": "none"}}
    key = rec[["timeframe", "mean_type", "entry_confirmation"] + NUM_AXES].astype(str).agg("|".join, axis=1)
    by_key = dict(zip(key, sh))
    out = {}
    for cid in cids:
        i = pos[cid]
        same = cat == cat[i]
        d = np.abs(I - I[i])
        cube = same & (d.max(axis=1) <= 1)
        cube[i] = False
        wide = same & (d.max(axis=1) <= 2)
        wide[i] = False
        c = sh[cube]
        row = rec.iloc[i]
        tw = {}
        for ax, col in (("mean_type", "twin_mean_type_sharpe"), ("entry_confirmation", "twin_confirm_sharpe")):
            parts = {k: str(row[k]) for k in ["timeframe", "mean_type", "entry_confirmation"] + NUM_AXES}
            if parts[ax] in other[ax]:
                parts[ax] = other[ax][parts[ax]]
            tw[col] = by_key.get("|".join(parts[k] for k in ["timeframe", "mean_type", "entry_confirmation"] + NUM_AXES),
                                 np.nan)
        out[cid] = {"cube_median_sharpe": float(np.median(c)) if len(c) else np.nan,
                    "cube_p10_sharpe": float(np.quantile(c, 0.1)) if len(c) else np.nan,
                    "cube_frac_profitable": float(np.mean(c > 0)) if len(c) else np.nan,
                    "cube_frac_075": float(np.mean(c >= 0.75)) if len(c) else np.nan,
                    "cube_own_pct": float(np.mean(c < sh[i])) if len(c) else np.nan,
                    "cube_n": int(len(c)),
                    "wide_median_sharpe": float(np.median(sh[wide])) if wide.any() else np.nan, **tw}
    return out


@app.command()
def main(n_boot: int = typer.Option(500), seed: int = typer.Option(11)) -> None:
    df = pd.read_parquet(OUT / "finalists.parquet")
    rows = []
    for run, g in df.groupby("run"):
        reps = {r["config_id"]: r for r in json.loads((RUNS / run / "representatives.json").read_text())}
        grid = _grid_inputs(run, list(g["config_id"]))
        for i, r in g.iterrows():
            rp = reps[r["config_id"]]
            ld = rp.get("local_detail") or []
            ld = json.loads(ld) if isinstance(ld, str) else ld
            rows.append({"_i": i, **_local(r["dev_sharpe"], r["dev_n_completed_trades"], ld), **grid[r["config_id"]],
                         **{k: rp.get(k) for k in ("neighbor_median_sharpe", "neighbor_frac_profitable",
                                                   "perturb_median_sharpe", "perturb_p10_sharpe",
                                                   "perturb_frac_profitable")}})
        typer.echo(f"{run}: {len(g)} finalists")
    X = pd.DataFrame(rows).set_index("_i").sort_index()
    cols = [c for c, _, _ in INPUTS]
    df = df.drop(columns=[c for c in cols if c in df.columns]).join(X)
    df.to_parquet(OUT / "robustness.parquet")

    sm.FEATURES = INPUTS  # reuse the same within-market scoring
    R = sm._rank_within(df, cols)
    uni = sm._univariate(df, R, n_boot, np.random.default_rng(seed))
    cover = {c: float(df[c].notna().mean()) for c in cols}
    for u in uni:
        u["coverage"] = cover[u["feature"]]
    (OUT / "robustness.json").write_text(json.dumps({"inputs": uni, "cube_n_median": float(df["cube_n"].median())},
                                                    default=lambda o: None))
    for u in sorted(uni, key=lambda u: -u["ic"]):
        typer.echo(f"{u['label'][:55]:55s} {u['ic']:+.3f} {u['n_pos']}/{u['n_mkts']} cov {u['coverage']:.0%} "
                   f"top PF {u['top20']['pf']:.2f} bot PF {u['bot20']['pf']:.2f} "
                   f"top Sh {u['top20']['sharpe']:+.2f} bot Sh {u['bot20']['sharpe']:+.2f} "
                   f"pass {u['top20']['pass']:.0%}/{u['bot20']['pass']:.0%}")


if __name__ == "__main__":
    app()
