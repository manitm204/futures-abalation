"""One market's chosen strategies together: its mean-reversion, noise-band and (ES)
squeeze-breakout legs, each strategy in its own fixed sleeve (`--market`, presets in PRESETS below):
  ES: mr_es_v6_1h #8 + #15, nb_es_v4 #17 + #104 and cb_bbkc_es_v2_15m #12 + #50, a third of the
      account per family (1/6 per strategy);
  NQ: mr_nq_v7_15m #1 + mr_nq_v7_1h #119, nb_nq_v2 #1 and cb_bbkc_nq_v3_15m #7 + cb_bbkc_nq_v3_5m #13,
      a third of the account per family (1/6 per MR or squeeze strategy, 1/3 for NB #1).

Writes futures-results/data/<MARKET>/combined_families_v1.json and
futures-results/<market>_combined.html (es_combined_template.html with the data inlined).
A standalone page, not a run tab.

Sleeves: each strategy gets its preset share of the $1M account for the whole-account
combination ("all"); within a family the legs split that family's money equally. Never
rebalanced. Each sleeve tracks its strategy's full-account
solo run scaled to the sleeve (as if sized in micro contracts: a $250k sleeve can't
hold one whole ES contract), so a combination's equity is the average of its strategies'
solo equity curves. Random-entry comparison: random run i of each strategy (that
family's own method, at the strategy's own time in market) combined the same way.

Any number of families: each gets its own group ("mr", "nb", "cb"), and the page shows
every pair of families' correlation and overlap.

Data: the per-family dumps from scripts/dump_family_runs.py, run inside each project
with its own venv. `full` (2018 .. validation end) is re-dumped on every run; the holdout
dump is re-made only with --refresh-holdout --confirm-holdout-access (ledgered in each
project as `cross_family_holdout`), else the cached one is reused.

Usage (from noise-band-backtest):
  PYTHONPATH=. python scripts/build_es_combined.py [--market NQ]
  PYTHONPATH=. python scripts/build_es_combined.py --market NQ --refresh-holdout --confirm-holdout-access
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import typer

from src.analysis.daily_performance import _drawdown, _sharpe

NB_ROOT = Path(__file__).resolve().parents[1]
ROOT = NB_ROOT.parent
MR_ROOT = ROOT / "mean-reversion-backtest"
CB_ROOT = ROOT / "bbkc-squeeze-backtest"
ROOTS = {"mr": MR_ROOT, "nb": NB_ROOT, "cb": CB_ROOT}
SITE = ROOT / "futures-results"
CACHE = NB_ROOT / "runs" / "cross_family"
DUMP = NB_ROOT / "scripts" / "dump_family_runs.py"
PRESETS = {
    "ES": {
        "legs": [("mr", "mr_es_v6_1h", 8), ("mr", "mr_es_v6_1h", 15), ("nb", "nb_es_v4", 17), ("nb", "nb_es_v4", 104),
                 ("cb", "cb_bbkc_es_v2_15m", 12), ("cb", "cb_bbkc_es_v2_15m", 50)],
        "weights": [1 / 6] * 6,
        "groups": {"mr": "Mean-reversion pair (#8 + #15)", "nb": "Noise-band pair (#17 + #104)",
                   "cb": "Squeeze pair (15m #12 + #50)", "all": "All 6 together"},
        "text": {"all_short": "All 6", "all_word": "all six", "count_word": "six", "mr_short": "MR pair",
                 "nb_short": "NB pair", "cb_short": "Squeeze pair", "mr_w": "50/50", "nb_w": "50/50", "cb_w": "50/50",
                 "all_w": "1/6 each (a third per family)",
                 "lede_legs": "The two chosen mean-reversion, two noise-band and two squeeze-breakout strategies",
                 "sleeve_desc": "$166,667 of a $1,000,000 account for all six together (a third per family), or half "
                                "the account each within a pair",
                 "sleeve_small": "a $166,667 sleeve can't hold one whole ES contract",
                 "holdout_caveat": "Each pair was frozen before its own holdout test and is unchanged here. But all three "
                                   "holdout results had been seen before this page combined them (the squeeze pair's "
                                   "#50 roughly broke even), so this view is a description, not a fresh test: don't use "
                                   "it to pick a mix.",
                 "val_caveat": "Not clean for any family: every pair was picked with its 2023–2024 results in view "
                               "(the noise-band and squeeze pairs directly on them). It shows how they held up, not proof."},
        "runs_src": "mean-reversion-backtest/runs/funnel/mr_es_v6_1h/ · noise-band-backtest/runs/funnel/nb_es_v4/ · "
                    "bbkc-squeeze-backtest/runs/funnel/cb_bbkc_es_v2_15m/",
        "out": "es_combined.html",
    },
    "NQ": {
        "legs": [("mr", "mr_nq_v7_15m", 1), ("mr", "mr_nq_v7_1h", 119), ("nb", "nb_nq_v2", 1),
                 ("cb", "cb_bbkc_nq_v3_15m", 7), ("cb", "cb_bbkc_nq_v3_5m", 13)],
        "weights": [1 / 6, 1 / 6, 1 / 3, 1 / 6, 1 / 6],
        "groups": {"mr": "Mean-reversion pair (15m #1 + 1h #119)", "nb": "Noise-band #1",
                   "cb": "Squeeze pair (15m #7 + 5m #13)", "all": "All 5 together"},
        "text": {"all_short": "All 5", "all_word": "all five", "count_word": "five", "mr_short": "MR pair",
                 "nb_short": "NB #1", "cb_short": "Squeeze pair", "mr_w": "50/50", "nb_w": "alone", "cb_w": "50/50",
                 "all_w": "a third per family (1/6 per MR or squeeze strategy, 1/3 for NB #1)",
                 "lede_legs": "The two chosen mean-reversion strategies, the chosen noise-band strategy and the two "
                              "chosen squeeze-breakout strategies",
                 "sleeve_desc": "a third of the $1,000,000 account per strategy family: $166,667 for each "
                                "mean-reversion and squeeze strategy and $333,333 for the noise-band strategy (a pair "
                                "alone splits 50/50)",
                 "sleeve_small": "a $166,667 sleeve can't hold one whole NQ contract",
                 "holdout_caveat": "Each family's strategies were frozen before their own holdout test and are unchanged "
                                   "here. But all three holdout results had been seen before this page combined them "
                                   "(the mean-reversion pair lost), and the third-per-family split was chosen "
                                   "afterwards, so this view is a description, not a fresh test: don't use it to pick a mix.",
                 "val_caveat": "Not clean for any family: every one was picked with its 2023–2024 results in view "
                               "(the noise-band and squeeze strategies directly on them). It shows how they held up, "
                               "not proof."},
        "runs_src": "mean-reversion-backtest/runs/funnel/mr_nq_v7_15m/ + mr_nq_v7_1h/ · noise-band-backtest/runs/funnel/nb_nq_v2/ · "
                    "bbkc-squeeze-backtest/runs/funnel/cb_bbkc_nq_v3_15m/ + cb_bbkc_nq_v3_5m/",
        "out": "nq_combined.html",
    },
}
LEGS: list = PRESETS["ES"]["legs"]
WEIGHTS: list = PRESETS["ES"]["weights"]
FAMILY = {"mr": "Mean reversion", "nb": "Noise-band breakout", "cb": "BB/KC squeeze"}
SHORT = {"mr": "MR", "nb": "NB", "cb": "SQ"}
QS = (0.05, 0.10, 0.50, 0.90, 0.95)
app = typer.Typer(add_completion=False)


def _dump(phase: str, only: set | None = None) -> None:
    """Dump every leg's run for `phase`, or only the runs in `only`."""
    CACHE.mkdir(parents=True, exist_ok=True)
    for fam, root in ROOTS.items():
        runs = sorted({r for f, r, _ in LEGS if f == fam and (only is None or r in only)})
        for run in runs:
            orders = [str(o) for f, r, o in LEGS if f == fam and r == run]
            out = CACHE / f"{phase}_{run}.npz"
            subprocess.run([str(root / ".venv" / "bin" / "python"), str(DUMP), fam, run, phase, str(out), *orders],
                           cwd=root, env={"PYTHONPATH": ".", "PATH": "/usr/bin:/bin"}, check=True)


def _load(phase: str) -> dict:
    z = {}
    meta = {"legs": {}}
    for run in sorted({r for _, r, _ in LEGS}):
        f = np.load(CACHE / f"{phase}_{run}.npz")
        m = json.loads(str(f["meta"]))
        for k in f.files:
            if k in ("days", "ref_bars", "hold"):
                if k in z and not np.array_equal(z[k], f[k]):
                    raise RuntimeError(f"{phase}: families disagree on {k}")
                z[k] = f[k]
            elif k != "meta":
                z[k] = f[k]
        meta["legs"].update(m["legs"])
        meta.update({k: v for k, v in m.items() if k != "legs"})
    return {"z": z, "meta": meta}


def _stats(c: np.ndarray) -> dict:
    r = c[1:] / c[:-1] - 1.0
    sh, _ = _sharpe(r, 252, 0.0)
    dd, dd_days, _ = _drawdown(c)
    n = len(r)
    return {"net_return": float(c[-1] / c[0] - 1), "cagr": float((c[-1] / c[0]) ** (252 / n) - 1) if n else None,
            "sharpe": sh, "max_drawdown": float(dd), "max_dd_days": int(dd_days),
            "vol": float(r.std(ddof=1) * np.sqrt(252)) if n > 1 else None}


def _years(days: np.ndarray, c: np.ndarray) -> dict:
    out, prev = {}, c[0]
    yrs = days.astype("datetime64[Y]").astype(int) + 1970
    for y in np.unique(yrs):
        last = c[1:][yrs == y][-1]
        out[str(y)] = float(last / prev - 1)
        prev = last
    return out


def _corr(x, y):
    return float(np.corrcoef(x, y)[0, 1]) if len(x) > 2 and x.std() > 0 and y.std() > 0 else None


def _build_phase(P: dict, periods: dict) -> dict:
    z, meta = P["z"], P["meta"]
    days, ref = z["days"], z["ref_bars"]
    keys = [f"{f}{o}" for f, _, o in LEGS]
    eq = {k: z[f"{k}_eq"] / z[f"{k}_eq"][0] for k in keys}
    rnd = {k: z[f"{k}_rand"] / z[f"{k}_rand"][:, :1] for k in keys}
    occ = {}
    for k in keys:
        m = np.zeros(len(ref), dtype=bool)
        for a, b in zip(z[f"{k}_iv0"], z[f"{k}_iv1"]):
            m[np.searchsorted(ref, a, "left"):np.searchsorted(ref, b, "left")] = True
        occ[k] = m
    ref_day = ref.astype("datetime64[D]")
    fams = _families()
    groups = {k: [k] for k in keys}
    groups.update({f: [k for k in keys if k.startswith(f)] for f in fams} | {"all": keys})
    wt = dict(zip(keys, WEIGHTS))

    def mix(src, ks):  # fixed sleeves: "all" uses the preset weights, a family splits its money equally
        w = np.array([wt[k] for k in ks]) if ks == keys else np.full(len(ks), 1.0 / len(ks))
        return sum(wi * src[k] for wi, k in zip(w / w.sum(), ks))
    curves = {g: mix(eq, ks) for g, ks in groups.items()}
    rcurves = {g: mix(rnd, ks) for g, ks in groups.items()}
    hold = z["hold"]
    rets = {k: eq[k][1:] / eq[k][:-1] - 1 for k in keys}
    gret = {g: curves[g][1:] / curves[g][:-1] - 1 for g in fams}
    months = days.astype("datetime64[M]")

    out_p = {}
    for pk, (a, b) in periods.items():
        lo, hi = days[a], days[b]
        bars = (ref_day >= lo) & (ref_day <= hi)
        per = {}
        for g, ks in groups.items():
            seg = curves[g][a:b + 2]
            st = _stats(seg)
            pnl = np.concatenate([z[f"{k}_pnl"][(z[f"{k}_entry_day"] >= lo) & (z[f"{k}_entry_day"] <= hi)] for k in ks])
            done = sum(int(z[f"{k}_done"][(z[f"{k}_entry_day"] >= lo) & (z[f"{k}_entry_day"] <= hi)].sum()) for k in ks)
            wins, losses = pnl[pnl > 0], pnl[pnl < 0]
            st.update(n_completed_trades=done, profit_factor=float(wins.sum() / -losses.sum()) if len(losses) else None,
                      win_rate=float((pnl > 0).mean()) if len(pnl) else None,
                      exposure=float((np.logical_or.reduce([occ[k] for k in ks]) & bars).sum() / bars.sum()),
                      sum_exposure=float(sum((occ[k] & bars).sum() for k in ks) / bars.sum()))
            rs = rcurves[g][:, a:b + 2]
            rs = rs / rs[:, :1]
            rst = [_stats(x) for x in rs]
            sh = np.array([x["sharpe"] if x["sharpe"] is not None else -np.inf for x in rst])
            rt = np.array([x["net_return"] for x in rst])
            per[g] = {"stats": st, "luck": {
                "pct_sharpe": float(np.mean(sh < st["sharpe"])), "pct_return": float(np.mean(rt < st["net_return"])),
                "mean_return": float(rt.mean()), "mean_sharpe": float(np.mean(sh[np.isfinite(sh)])),
                "mean_max_drawdown": float(np.mean([x["max_drawdown"] for x in rst])),
                "band": {f"p{int(q * 100)}": np.round(np.quantile(rs, q, axis=0), 4).tolist() for q in QS}
                        | {"mean": np.round(rs.mean(axis=0), 4).tolist()}}}
        of = {f: np.logical_or.reduce([occ[k] for k in groups[f]]) & bars for f in fams}
        n_fam = np.sum([of[f] for f in fams], axis=0)
        n_open = np.sum([occ[k] & bars for k in keys], axis=0)
        sl = slice(a, b + 1)
        mk = months[sl]
        um = np.unique(mk)
        mon = {g: np.array([np.prod(1 + gret[g][sl][mk == m]) - 1 for m in um]) for g in fams}
        out_p[pk] = {
            "groups": per,
            "hold": _stats(hold[a:b + 2]),
            # Family matrices in `fams` order; [i][j] of "while" = share of family i's time in market that j is in too.
            "corr": {"legs": [[_corr(rets[x][sl], rets[y][sl]) for y in keys] for x in keys],
                     "families_daily": [[_corr(gret[x][sl], gret[y][sl]) for y in fams] for x in fams],
                     "families_monthly": [[_corr(mon[x], mon[y]) for y in fams] for x in fams]},
            "overlap": {"multi_family": float((n_fam >= 2).sum() / bars.sum()),
                        "while": [[float((of[x] & of[y]).sum() / of[x].sum()) if of[x].any() else None for y in fams]
                                  for x in fams],
                        "pair_time": [[float((of[x] & of[y]).sum() / bars.sum()) for y in fams] for x in fams],
                        "open_count": [float(((n_open == i) & bars).sum() / bars.sum()) for i in range(len(keys) + 1)]},
        }
    return {
        "days": [str(d) for d in days],
        "curves": {g: np.round(c, 5).tolist() for g, c in curves.items()},
        "hold": np.round(hold, 5).tolist(),
        "years": {g: _years(days, c) for g, c in curves.items()} | {"hold": _years(days, hold)},
        "periods": out_p,
        "ranges": {k: list(v) for k, v in periods.items()},
        "window": meta["window"],
    }


def _families() -> list[str]:
    """Families in the order their legs are listed."""
    return list(dict.fromkeys(f for f, _, _ in LEGS))


@app.command()
def main(market: str = typer.Option("ES", help=f"One of {sorted(PRESETS)}"),
         refresh_holdout: bool = typer.Option(False, "--refresh-holdout"),
         confirm_holdout_access: bool = typer.Option(False, "--confirm-holdout-access")) -> None:
    global LEGS, WEIGHTS
    if market not in PRESETS:
        raise typer.BadParameter(f"--market must be one of {sorted(PRESETS)}")
    pre = PRESETS[market]
    LEGS, WEIGHTS = pre["legs"], pre["weights"]
    _dump("full")
    missing = {r for _, r, _ in LEGS if not (CACHE / f"holdout_{r}.npz").exists()}
    if refresh_holdout or missing:
        if not confirm_holdout_access:
            raise typer.BadParameter("The holdout dump needs --confirm-holdout-access (ledgered holdout read).")
        _dump("holdout", None if refresh_holdout else missing)  # only the uncached runs unless --refresh-holdout
    full, hol = _load("full"), _load("holdout")
    days = np.asarray(full["z"]["days"])
    n_dev = int((days <= np.datetime64(full["meta"]["dev_end"], "D")).sum())
    out_full = _build_phase(full, {"all": (0, len(days) - 1), "dev": (0, n_dev - 1), "val": (n_dev, len(days) - 1)})
    out_hold = _build_phase(hol, {"holdout": (0, len(hol["z"]["days"]) - 1)})
    legs = []
    for fam, run, o in LEGS:
        m = full["meta"]["legs"][f"{fam}{o}"]
        legs.append({"key": f"{fam}{o}", "family": FAMILY[fam], "family_key": fam, "run_id": run, "order": o,
                     "timeframe": m["timeframe"], "config_id": m["config_id"][:8], "params": m["params"],
                     "name": f"{SHORT[fam]} #{o} ({m['timeframe'].replace('min', 'm')})"})
    w = out_full["window"]
    doc = {
        "kind": "es_combined", "symbol": market, "name": f"{market} strategies together",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "starting_equity": full["meta"]["starting_equity"], "n_sims": full["meta"]["n_sims"],
        "legs": [{**leg, "weight": w} for leg, w in zip(legs, WEIGHTS)],
        "groups": pre["groups"],
        "families": [{"key": f, "label": FAMILY[f], "n": sum(x == f for x, _, _ in LEGS)} for f in _families()],
        "group_n": {f: sum(x == f for x, _, _ in LEGS) for f in _families()} | {"all": len(LEGS)},
        "text": pre["text"],
        "sleeves": {"all": min(WEIGHTS), "pair": 0.5},
        "phases": {
            "full": {**out_full, "labels": {"all": f"{w[0][:4]}–{w[1][:4]}", "dev": f"Development {w[0][:4]}–{full['meta']['dev_end'][:4]}",
                                            "val": f"Validation {int(full['meta']['dev_end'][:4]) + 1}–{w[1][:4]}"}},
            "holdout": {**out_hold, "labels": {"holdout": f"Holdout {out_hold['window'][0]} to {out_hold['window'][1]}"}},
        },
        "source": f"noise-band-backtest/scripts/build_es_combined.py --market {market} · scripts/dump_family_runs.py · {pre['runs_src']}",
    }
    js = SITE / "data" / market / "combined_families_v1.json"
    js.write_text(json.dumps(doc, separators=(",", ":")))
    tpl = (SITE / "es_combined_template.html").read_text()
    html = SITE / pre["out"]
    html.write_text(tpl.replace("/*__DATA__*/null", json.dumps(doc, separators=(",", ":")).replace("</", "<\\/")))
    for pk, P in [("all", out_full["periods"]["all"]), ("holdout", out_hold["periods"]["holdout"])]:
        s = P["groups"]["all"]
        fc = P["corr"]["families_daily"]
        pairs = ", ".join(f"{a}-{b} {fc[i][j]:.2f}" for i, a in enumerate(_families()) for j, b in enumerate(_families()) if i < j)
        typer.echo(f"{pre['text']['all_short']} {pk}: return {s['stats']['net_return']:+.1%}, Sharpe {s['stats']['sharpe']:.2f}, "
                   f"beats {s['luck']['pct_sharpe']:.0%} of random; family corr (daily) {pairs}")
    typer.echo(f"wrote {js} and {html}")


if __name__ == "__main__":
    app()
