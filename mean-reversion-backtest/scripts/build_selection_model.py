"""Do the funnel's training-period (2018-22) numbers predict which finalists do well in validation (2023-24)?

Population: every frozen finalist of every mean-reversion futures run that has validation results,
with identical settings on the same market kept once (the copy from the latest run is kept, since
its neighbour / DSR numbers come from the larger grid). The old SPY runs (mr_v1, mr_v2) are left out.

Inputs (fixed list, FEATURES below) are all training-period or funnel numbers; nothing from
validation or the holdout. One input is new: training-period luck %, the share of random-entry runs
on 2018-22 (same bar size, time in market, costs and sizing) whose Sharpe the finalist beat.

Targets: validation Sharpe (main), passed validation (yes/no), validation luck % (from
random_benchmark.json).

Everything is compared WITHIN a market (each input and the target are turned into percentile ranks
inside the market), because the market sets most of the validation result and the real choice is
between strategies on the same market.

  1. One input at a time: Spearman rank correlation with validation Sharpe in each market, averaged
     over markets, with a 95% interval from resampling whole dedup clusters inside each market
     (neighbouring finalists share most trades), the number of markets where it is positive, and
     the top-20% vs bottom-20% validation Sharpe / pass rate / PF.
  2. Models, leave one market out: fit on the other markets, rank the held-out market's finalists,
     score the ranking (rank correlation, top-10 and top-20% validation results). Ridge regression,
     logistic regression on pass/fail, and a shallow random forest, against baselines: random
     choice, training Sharpe, the funnel's own order, and the best single input picked on the
     training markets. A shuffle test (validation Sharpe shuffled across clusters inside each
     market) gives the chance distribution of the ridge model's score.

The holdout is not read. Validation (already used and seen) is the target, so a rule found here is
fitted to validation and would need fresh data to be confirmed.

Writes runs/funnel/selection_model_v1/{train_luck.json,finalists.parquet}, and
futures-results/data/ALL/selection_model_v1.json + selection_model.html (template with data inlined).

Usage:
  PYTHONPATH=. python scripts/build_selection_model.py [--n-sims 200] [--n-boot 1000] [--n-shuffle 300]
"""

from __future__ import annotations

import json
import re
import zlib
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import typer
from scipy.stats import rankdata

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = PROJECT_ROOT.parent / "futures-results"
RUNS = PROJECT_ROOT / "runs" / "funnel"
OUT = RUNS / "selection_model_v1"
SKIP = {"mr_v1", "mr_v2", "mr_v2_INVALID_stop_ignored"}
app = typer.Typer(add_completion=False)

# (column, label, group). Fixed before looking at any result.
FEATURES = [
    ("dev_sharpe", "Sharpe", "Training results"),
    ("dev_net_return", "Total return", "Training results"),
    ("dev_profit_factor", "Profit factor", "Training results"),
    ("dev_n_completed_trades", "Trades", "Training results"),
    ("dev_max_drawdown", "Max drawdown (less negative = higher)", "Training results"),
    ("dev_win_rate", "Win rate", "Training results"),
    ("dev_avg_trade", "Average trade ($)", "Training results"),
    ("dev_exposure", "Time in market", "Training results"),
    ("dev_skew", "Daily-return skew", "Training results"),
    ("dev_excess_kurtosis", "Daily-return kurtosis", "Training results"),
    ("train_luck_pct", "% of luck runs beaten (training)", "Training results"),
    ("dev_n_profitable_years", "Profitable years", "Time robustness"),
    ("worst_year_sharpe", "Worst-year Sharpe", "Time robustness"),
    ("dev_excl_best_year_sharpe", "Sharpe without best year", "Time robustness"),
    ("dev_top_k_trades_contribution", "Share of profit from top trades", "Time robustness"),
    ("local_median_sharpe", "Neighbour median Sharpe (funnel's ranking)", "Parameter robustness"),
    ("local_min_sharpe", "Neighbour min Sharpe", "Parameter robustness"),
    ("local_frac_profitable", "Share of neighbours profitable", "Parameter robustness"),
    ("neighbor_median_sharpe", "Wider-lattice neighbour median Sharpe", "Parameter robustness"),
    ("perturb_p10_sharpe", "Random-nudge 10th-pct Sharpe", "Parameter robustness"),
    ("neighbor_center_minus_median_sharpe", "Own Sharpe minus neighbours' (peakiness)", "Parameter robustness"),
    ("stress_cost_1.5x_net_return", "Return at 1.5x costs", "Funnel checks"),
    ("stress_delay_net_return", "Return with 1-bar entry delay", "Funnel checks"),
    ("stress_missed_p10_net_return", "Return with missed trades (10th pct)", "Funnel checks"),
    ("breakeven_cost_multiplier", "Break-even cost multiple", "Funnel checks"),
    ("qqq_dev_sharpe", "Sharpe on the related market", "Funnel checks"),
    ("dsr", "Deflated Sharpe", "Funnel checks"),
    ("is_1h", "1-hour bars (vs 15m)", "Strategy shape"),
    ("has_stop", "Has a stop", "Strategy shape"),
    ("entry_z", "Entry z (higher = shallower)", "Strategy shape"),
    ("exit_z", "Exit z", "Strategy shape"),
    ("max_holding_bars", "Max hold (bars)", "Strategy shape"),
]
FCOLS = [f for f, _, _ in FEATURES]


def _ver(run: str) -> tuple:
    m = re.search(r"_v(\d+)", run)
    return (int(m.group(1)) if m else 0, run)


def _collect() -> pd.DataFrame:
    rows = []
    for d in sorted(RUNS.glob("mr_*"), key=lambda p: _ver(p.name)):
        if d.name in SKIP or not (d / "validation_results.json").exists():
            continue
        reps = {r["config_id"]: r for r in json.loads((d / "representatives.json").read_text())}
        if not reps:
            continue
        frozen = json.loads((d / "frozen_representatives.json").read_text())
        val = {r["config_id"]: r for r in json.loads((d / "validation_results.json").read_text())["results"]}
        luck = {}
        if (d / "random_benchmark.json").exists():
            luck = {f["config_id"]: f for f in json.loads((d / "random_benchmark.json").read_text())["finalists"]}
        rec = pd.read_parquet(d / "records.parquet").set_index("config_id")
        for c in frozen["candidates"]:
            cid, r, v = c["config_id"], reps[c["config_id"]], val[c["config_id"]]["metrics"]
            p = c["params"]
            yr = [r[k] for k in r if k.startswith("dev_year_sharpe_") and r[k] is not None]
            ld = r.get("local_detail") or []
            loc = [x["sharpe"] for x in (json.loads(ld) if isinstance(ld, str) else ld) if x.get("sharpe") is not None]
            rr = rec.loc[cid]
            row = {k: r.get(k) for k in FCOLS if k in r}
            row.update({
                "run": d.name, "market": frozen["symbol"], "config_id": cid, "dev_order": c["dev_order"],
                "cluster": f"{d.name}:{r['dedup_cluster']}", "timeframe": p["timeframe"],
                "settings": json.dumps({k: str(x) for k, x in sorted(p.items())}),
                "dev_win_rate": rr["dev_win_rate"], "dev_skew": rr["dev_skew"],
                "dev_excess_kurtosis": rr["dev_excess_kurtosis"],
                "dev_avg_trade": rr["dev_net_pnl"] / max(rr["dev_n_completed_trades"], 1),
                "worst_year_sharpe": min(yr) if yr else None,
                "local_min_sharpe": min(loc) if loc else None,
                "breakeven_cost_multiplier": 25.0 if r.get("breakeven_status", "").startswith("profitable_beyond")
                else r.get("breakeven_cost_multiplier"),
                "is_1h": float(p["timeframe"] == "1h"),
                "has_stop": float(str(p.get("stop_atr_multiple", "none")).lower() not in ("none", "null", "")),
                "entry_z": float(p["entry_z"]), "exit_z": float(p["exit_z"]),
                "max_holding_bars": float(p["max_holding_bars"]),
                "val_sharpe": v["sharpe"], "val_return": v["net_return"], "val_pf": v["profit_factor"],
                "val_trades": v["n_completed_trades"], "val_pass": float(val[cid]["status"] == "pass"),
                "val_luck_pct": (luck.get(cid) or {}).get("luck_pct_sharpe"),
            })
            rows.append(row)
    df = pd.DataFrame(rows)
    n0 = len(df)
    df = df.drop_duplicates(["market", "settings"], keep="last").reset_index(drop=True)  # last = latest run
    typer.echo(f"{n0} finalists, {len(df)} with unique settings per market")
    df.attrs["n_before_dedup"] = n0
    return df


def _train_luck(df: pd.DataFrame, n_sims: int) -> pd.Series:
    """Training-period (2018-22) luck %: random-entry runs at the finalist's own training time in market."""
    from scripts.run_mr_funnel import load_execution_config
    from src.analysis.daily_performance import daily_equity, window_metrics
    from src.data.aggregation import aggregate_bars
    from src.experiments.data_access import load_phase_bars
    from src.experiments.funnel_config import load_funnel_config
    from src.experiments.funnel_prep import _metric_kwargs
    from src.experiments.random_entry import simulate_random_entries
    from src.strategies.mean_reversion.backtest import MRData

    cache_p = OUT / "train_luck.json"
    cache = json.loads(cache_p.read_text()) if cache_p.exists() else {"n_sims": n_sims, "dist": {}}
    if cache["n_sims"] != n_sims:
        cache = {"n_sims": n_sims, "dist": {}}
    df = df.assign(_lvl=np.maximum(1, np.round(100 * df["dev_exposure"].astype(float))).astype(int))
    for mkt, g in df.groupby("market"):
        need = {(tf, int(l)) for tf, l in zip(g["timeframe"], g["_lvl"]) if f"{mkt}|{tf}|{l}" not in cache["dist"]}
        if not need:
            continue
        fc = load_funnel_config(PROJECT_ROOT / "configs" / "funnel" / f"mr_funnel_{g['run'].iloc[-1].removeprefix('mr_')}.yaml")
        ec, dv = load_execution_config(fc), fc.data.development
        bars, _ = load_phase_bars(fc, mkt, "development", command="selection_model_train_luck",
                                  experiment_id="selection_model_v1")
        for tf in sorted({t for t, _ in need}):
            data = MRData(aggregate_bars(bars, timeframe=tf))
            for _, lvl in sorted(x for x in need if x[0] == tf):
                rng = np.random.default_rng([fc.seed, zlib.crc32(f"{mkt}{tf}".encode()), lvl])
                sh = []
                for _ in range(n_sims):
                    sim = simulate_random_entries(data, mkt, exec_config=ec, starting_equity=ec.starting_equity,
                                                  window_start=dv.start, window_end=dv.end, exposure=lvl / 100, rng=rng)
                    m, _ = window_metrics(sim, data, daily_equity(sim, data, ec.starting_equity), start=dv.start,
                                          end=dv.end, starting_equity=ec.starting_equity, **_metric_kwargs(fc))
                    sh.append(-1e9 if m["sharpe"] is None else m["sharpe"])
                cache["dist"][f"{mkt}|{tf}|{lvl}"] = sh
        typer.echo(f"training luck: {mkt} {len(need)} (bar size, time-in-market) levels x {n_sims} runs")
        cache_p.write_text(json.dumps(cache))
    return pd.Series([float(np.mean(np.array(cache["dist"][f"{m}|{tf}|{l}"]) < s))
                      for m, tf, l, s in zip(df["market"], df["timeframe"], df["_lvl"], df["dev_sharpe"])],
                     index=df.index)


def _rank_within(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Percentile rank (0..1, ties averaged) inside each market; missing -> the middle (0.5)."""
    return df.groupby("market")[cols].rank(pct=True).fillna(0.5)


def _ic(x: np.ndarray, y: np.ndarray) -> float:
    if np.std(x) == 0 or np.std(y) == 0:
        return np.nan
    return float(np.corrcoef(rankdata(x), rankdata(y))[0, 1])


def top_bottom(v: np.ndarray, frac: float = 0.2, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Positions of exactly round(frac * n) highest and lowest values; ties broken at random (fixed seed),
    so an input with many tied values (e.g. break-even capped at 25x) doesn't get a bigger group."""
    k = max(1, int(round(frac * len(v))))
    u = np.random.default_rng(seed).random(len(v))
    return np.lexsort((u, -v))[:k], np.lexsort((u, v))[:k]


def _pick(score: np.ndarray, g: pd.DataFrame, k: int) -> dict:
    """Validation results of the top-k by score (ties broken by the funnel's order)."""
    order = np.lexsort((g["dev_order"].to_numpy(), -score))[:k]
    s = g.iloc[order]
    return {"sharpe": float(s["val_sharpe"].mean()), "pass": float(s["val_pass"].mean()),
            "pf": float(s["val_pf"].median()), "ret": float(s["val_return"].mean())}


def _score_ranking(df: pd.DataFrame, score: pd.Series) -> dict:
    """Per market: rank correlation with validation Sharpe, top-10 and top-20% results; then averages."""
    per = {}
    for mkt, g in df.groupby("market"):
        s = score.loc[g.index].to_numpy(float)
        k20 = max(1, int(round(0.2 * len(g))))
        per[mkt] = {"n": len(g), "ic": _ic(s, g["val_sharpe"].to_numpy()),
                    "top10": _pick(s, g, min(10, len(g))), "top20": _pick(s, g, k20)}
    avg = lambda f: float(np.nanmean([f(v) for v in per.values()]))  # noqa: E731
    return {"per_market": per, "ic": avg(lambda v: v["ic"]),
            "top10_sharpe": avg(lambda v: v["top10"]["sharpe"]), "top10_pass": avg(lambda v: v["top10"]["pass"]),
            "top10_pf": avg(lambda v: v["top10"]["pf"]),
            "top20_sharpe": avg(lambda v: v["top20"]["sharpe"]), "top20_pass": avg(lambda v: v["top20"]["pass"]),
            "top20_pf": avg(lambda v: v["top20"]["pf"])}


def _univariate(df: pd.DataFrame, R: pd.DataFrame, n_boot: int, rng) -> list[dict]:
    mk = {m: g.index.to_numpy() for m, g in df.groupby("market")}
    cl = {m: [df.index[df["cluster"] == c].to_numpy() for c in df.loc[idx, "cluster"].unique()] for m, idx in mk.items()}
    y = df["val_sharpe"].to_numpy(float)
    out = []
    for f, label, grp in FEATURES:
        x = R[f].to_numpy(float)
        per = {m: _ic(x[idx], y[idx]) for m, idx in mk.items()}
        boots = []
        for _ in range(n_boot):
            vals = []
            for m in mk:
                pick = rng.integers(0, len(cl[m]), len(cl[m]))
                idx = np.concatenate([cl[m][i] for i in pick])
                vals.append(_ic(x[idx], y[idx]))
            boots.append(np.nanmean(vals))
        boots = np.array(boots)
        ic = float(np.nanmean(list(per.values())))
        p = float(min(1.0, 2 * min(np.mean(boots <= 0), np.mean(boots >= 0))))
        top, bot = [], []
        for m, idx in mk.items():
            g = df.loc[idx]
            q = x[idx]
            hi, lo = top_bottom(q)
            top.append(g.iloc[hi])
            bot.append(g.iloc[lo])
        top, bot = pd.concat(top), pd.concat(bot)
        out.append({"feature": f, "label": label, "group": grp, "ic": ic,
                    "ci": [float(np.nanquantile(boots, 0.025)), float(np.nanquantile(boots, 0.975))], "p": p,
                    "n_pos": int(sum(v > 0 for v in per.values() if np.isfinite(v))),
                    "n_mkts": int(sum(np.isfinite(v) for v in per.values())),
                    "per_market": {m: (None if not np.isfinite(v) else v) for m, v in per.items()},
                    "ic_pass": float(np.nanmean([_ic(x[idx], df.loc[idx, "val_pass"].to_numpy()) for idx in mk.values()])),
                    "ic_luck": float(np.nanmean([_ic(x[idx], df.loc[idx, "val_luck_pct"].to_numpy(float))
                                                 for idx in mk.values() if df.loc[idx, "val_luck_pct"].notna().all()])),
                    "top20": {"sharpe": float(top["val_sharpe"].mean()), "pass": float(top["val_pass"].mean()),
                              "pf": float(top["val_pf"].median())},
                    "bot20": {"sharpe": float(bot["val_sharpe"].mean()), "pass": float(bot["val_pass"].mean()),
                              "pf": float(bot["val_pf"].median())}})
    # Holm adjustment over the fixed list
    order = np.argsort([o["p"] for o in out])
    run_max = 0.0
    for rank, i in enumerate(order):
        run_max = max(run_max, min(1.0, (len(out) - rank) * out[i]["p"]))
        out[i]["p_holm"] = run_max
    return out


def _lomo(df: pd.DataFrame, R: pd.DataFrame, y_rank: pd.Series, kind: str, seed: int = 0) -> pd.Series:
    """Leave one market out: fit on the other markets, score the held-out one."""
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import LogisticRegression, Ridge

    pred = pd.Series(np.nan, index=df.index)
    X = R[FCOLS].to_numpy(float) - 0.5
    for mkt in df["market"].unique():
        te = (df["market"] == mkt).to_numpy()
        tr = ~te
        if kind == "ridge":
            # alpha picked by an inner leave-one-market-out over the training markets
            best, best_a = -np.inf, 10.0
            for a in (1.0, 10.0, 100.0, 1000.0):
                ics = []
                for m2 in df.loc[tr, "market"].unique():
                    t2 = tr & (df["market"] == m2).to_numpy()
                    f2 = tr & ~t2
                    mdl = Ridge(alpha=a).fit(X[f2], y_rank[f2])
                    ics.append(_ic(mdl.predict(X[t2]), df.loc[t2, "val_sharpe"].to_numpy()))
                if np.nanmean(ics) > best:
                    best, best_a = np.nanmean(ics), a
            pred[te] = Ridge(alpha=best_a).fit(X[tr], y_rank[tr]).predict(X[te])
        elif kind == "logit":
            mdl = LogisticRegression(C=0.1, max_iter=2000).fit(X[tr], df.loc[tr, "val_pass"])
            pred[te] = mdl.predict_proba(X[te])[:, 1]
        elif kind == "forest":
            mdl = RandomForestRegressor(n_estimators=300, max_depth=3, min_samples_leaf=20, random_state=seed,
                                        n_jobs=-1).fit(X[tr], y_rank[tr])
            pred[te] = mdl.predict(X[te])
        elif kind == "best_single":
            # the input with the highest average rank correlation on the training markets
            ics = {f: np.nanmean([_ic(R.loc[g.index, f].to_numpy(), g["val_sharpe"].to_numpy())
                                  for _, g in df[tr].groupby("market")]) for f in FCOLS}
            pred[te] = R.loc[te, max(ics, key=ics.get)].to_numpy()
    return pred


def _shuffle_y(df: pd.DataFrame, rng) -> pd.DataFrame:
    """Shuffle validation results across dedup clusters inside each market (each cluster's finalists
    receive another cluster's results, recycled to fit), keeping within-cluster similarity."""
    d = df.copy()
    for mkt, g in df.groupby("market"):
        cls = list(g["cluster"].unique())
        perm = rng.permutation(len(cls))
        for c, pc in zip(cls, perm):
            src = g[g["cluster"] == cls[pc]][["val_sharpe", "val_pass", "val_pf", "val_return"]].to_numpy()
            dst = g.index[g["cluster"] == c]
            d.loc[dst, ["val_sharpe", "val_pass", "val_pf", "val_return"]] = src[np.arange(len(dst)) % len(src)]
    return d


@app.command()
def main(n_sims: int = typer.Option(200), n_boot: int = typer.Option(1000), n_shuffle: int = typer.Option(300),
         seed: int = typer.Option(7)) -> None:
    from sklearn.linear_model import Ridge

    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    df = _collect()
    n_before = df.attrs["n_before_dedup"]
    df["train_luck_pct"] = _train_luck(df, n_sims)
    df.to_parquet(OUT / "finalists.parquet")
    R = _rank_within(df, FCOLS)
    y_rank = df.groupby("market")["val_sharpe"].rank(pct=True)

    uni = _univariate(df, R, n_boot, rng)
    typer.echo("univariate done")

    scores = {
        "Random choice": None,
        "Training Sharpe": R["dev_sharpe"],
        "Funnel's own order": -df["dev_order"].astype(float),
        "Best single input (picked on other markets)": _lomo(df, R, y_rank, "best_single"),
        "Ridge regression (all inputs)": _lomo(df, R, y_rank, "ridge"),
        "Logistic regression on pass/fail": _lomo(df, R, y_rank, "logit"),
        "Shallow random forest": _lomo(df, R, y_rank, "forest"),
    }
    models = {}
    for name, s in scores.items():
        if s is None:  # random: expected value = the market average; IC 0
            per = {}
            for mkt, g in df.groupby("market"):
                per[mkt] = {"n": len(g), "ic": 0.0,
                            **{k: {"sharpe": float(g["val_sharpe"].mean()), "pass": float(g["val_pass"].mean()),
                                   "pf": float(g["val_pf"].median()), "ret": float(g["val_return"].mean())}
                               for k in ("top10", "top20")}}
            avg = lambda f: float(np.mean([f(v) for v in per.values()]))  # noqa: E731
            models[name] = {"per_market": per, "ic": 0.0,
                            **{f"{k}_{m}": avg(lambda v, k=k, m=m: v[k][m]) for k in ("top10", "top20")
                               for m in ("sharpe", "pass", "pf")}}
        else:
            models[name] = _score_ranking(df, s)
        typer.echo(f"{name:45s} IC {models[name]['ic']:+.3f}  top10 Sharpe {models[name]['top10_sharpe']:+.2f} "
                   f"pass {models[name]['top10_pass']:.0%}  top20% Sharpe {models[name]['top20_sharpe']:+.2f}")

    # chance distribution of the ridge model's score (and of training Sharpe's), shuffling across clusters
    null_ridge, null_rand10 = [], []
    for i in range(n_shuffle):
        d = _shuffle_y(df, rng)
        yr = d.groupby("market")["val_sharpe"].rank(pct=True)
        X = R[FCOLS].to_numpy(float) - 0.5
        pred = pd.Series(np.nan, index=d.index)
        for mkt in d["market"].unique():
            te = (d["market"] == mkt).to_numpy()
            pred[te] = Ridge(alpha=100.0).fit(X[~te], yr[~te]).predict(X[te])
        sc = _score_ranking(d, pred)
        null_ridge.append([sc["ic"], sc["top10_sharpe"] - np.mean([g["val_sharpe"].mean() for _, g in d.groupby("market")])])
    null_ridge = np.array(null_ridge)
    base10 = models["Random choice"]["top10_sharpe"]
    shuffle = {"n": n_shuffle, "ic_p95": float(np.quantile(null_ridge[:, 0], 0.95)),
               "ic_p": float(np.mean(null_ridge[:, 0] >= models["Ridge regression (all inputs)"]["ic"])),
               "top10_gain_p95": float(np.quantile(null_ridge[:, 1], 0.95)),
               "top10_gain_p": float(np.mean(null_ridge[:, 1] >= models["Ridge regression (all inputs)"]["top10_sharpe"] - base10)),
               "note": "ridge alpha fixed at 100 in the shuffles"}
    for name in ("Training Sharpe", "Funnel's own order", "Best single input (picked on other markets)",
                 "Logistic regression on pass/fail", "Shallow random forest"):
        models[name]["shuffle_ic_p"] = float(np.mean(null_ridge[:, 0] >= models[name]["ic"]))
    models["Ridge regression (all inputs)"]["shuffle_ic_p"] = shuffle["ic_p"]

    # ridge on all markets, for the direction of each input (alpha 100), with a cluster bootstrap
    X = R[FCOLS].to_numpy(float) - 0.5
    coef = Ridge(alpha=100.0).fit(X, y_rank).coef_
    cl_idx = [df.index[df["cluster"] == c].to_numpy() for c in df["cluster"].unique()]
    bc = []
    for _ in range(300):
        idx = np.concatenate([cl_idx[i] for i in rng.integers(0, len(cl_idx), len(cl_idx))])
        bc.append(Ridge(alpha=100.0).fit(X[idx], y_rank.to_numpy()[idx]).coef_)
    bc = np.array(bc)
    coefs = [{"feature": f, "label": l, "coef": float(c), "ci": [float(np.quantile(bc[:, i], 0.025)),
                                                               float(np.quantile(bc[:, i], 0.975))]}
             for i, ((f, l, _), c) in enumerate(zip(FEATURES, coef))]

    mk = df.groupby("market").agg(n=("val_sharpe", "size"), clusters=("cluster", "nunique"),
                                  runs=("run", lambda s: sorted(set(s))), val_sharpe_mean=("val_sharpe", "mean"),
                                  val_pass=("val_pass", "mean"), val_pf_median=("val_pf", "median"))
    doc = {"generated_at": datetime.now(timezone.utc).isoformat(),
           "population": {"n_finalists_total": int(n_before),
                          "n": len(df), "n_clusters": int(df["cluster"].nunique()),
                          "markets": {m: {**{k: (v if not isinstance(v, (np.floating, np.integer)) else float(v))
                                             for k, v in r.items()}} for m, r in mk.to_dict("index").items()}},
           "features": [{"feature": f, "label": l, "group": g} for f, l, g in FEATURES],
           "univariate": uni, "models": models, "shuffle": shuffle, "coefs": coefs,
           "settings": {"n_sims_train_luck": n_sims, "n_boot": n_boot, "n_shuffle": n_shuffle, "seed": seed}}
    js = SITE_ROOT / "data" / "ALL" / "selection_model_v1.json"
    blob = json.dumps(doc, separators=(",", ":"), default=lambda o: None if o is None or (isinstance(o, float) and np.isnan(o)) else str(o))
    blob = blob.replace("NaN", "null")
    js.write_text(blob)
    tpl = SITE_ROOT / "selection_model_template.html"
    if tpl.exists():
        (SITE_ROOT / "selection_model.html").write_text(tpl.read_text().replace("/*__DATA__*/null", blob))
    typer.echo(f"wrote {js}")


if __name__ == "__main__":
    app()
