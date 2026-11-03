"""Which of the inputs that lined up with validation are really separate signals?

Takes the strongest candidates from build_selection_model.py / build_robustness_inputs.py, measures
how they correlate with each other (Spearman inside each market, averaged), what each adds once
break-even cost multiple is known, and scores simple equal-weight combinations (average of
within-market percentile ranks; nothing fitted) plus a ridge on the same few inputs scored leave
one market out.

Needs runs/funnel/selection_model_v1/robustness.parquet. Writes .../combos.json.

Usage:
  PYTHONPATH=. python scripts/build_input_combos.py
"""

from __future__ import annotations

import itertools
import json

import numpy as np
import pandas as pd
from scipy.stats import rankdata

import scripts.build_selection_model as sm

CANDS = {
    "breakeven_cost_multiplier": "Break-even cost multiple",
    "dev_avg_trade": "Average trade ($)",
    "dev_net_return": "Total return",
    "stress_cost_1.5x_net_return": "Return at 1.5x costs",
    "stress_missed_p10_net_return": "Return with missed trades",
    "stress_delay_net_return": "Return with 1-bar delay",
    "dev_profit_factor": "Profit factor",
    "worst_year_sharpe": "Worst-year Sharpe",
    "local_sd_sharpe": "Spread of one-step moves' Sharpe",
    "dev_exposure": "Time in market",
    "dev_sharpe": "Sharpe",
    "dev_n_completed_trades": "Trades",
    "dev_win_rate": "Win rate",
}


def ic(x, y):
    return float(np.corrcoef(rankdata(x), rankdata(y))[0, 1]) if np.std(x) and np.std(y) else np.nan


def main() -> None:
    df = pd.read_parquet(sm.OUT / "robustness.parquet")
    cols = list(CANDS)
    R = df.groupby("market")[cols].rank(pct=True).fillna(0.5)
    mk = {m: g.index for m, g in df.groupby("market")}
    y = df["val_sharpe"]

    # 1. correlation between inputs, within market, averaged over markets
    C = sum(R.loc[idx, cols].corr(method="spearman") for idx in mk.values()) / len(mk)

    # 2. what each input adds after break-even cost multiple: residual of its rank on break-even's rank
    def partial(f, base="breakeven_cost_multiplier"):
        out = []
        for idx in mk.values():
            x, b = R.loc[idx, f].to_numpy(), R.loc[idx, base].to_numpy()
            res = x - np.polyval(np.polyfit(b, x, 1), b)
            out.append(ic(res, y.loc[idx].to_numpy()))
        return float(np.nanmean(out)), int(sum(v > 0 for v in out))

    def score(s: pd.Series) -> dict:
        per, top, bot = [], [], []
        for m, idx in mk.items():
            v = s.loc[idx].to_numpy()
            per.append(ic(v, y.loc[idx].to_numpy()))
            g = df.loc[idx]
            hi, lo = sm.top_bottom(v)
            top.append(g.iloc[hi])
            bot.append(g.iloc[lo])
        top, bot = pd.concat(top), pd.concat(bot)
        return {"ic": float(np.nanmean(per)), "n_pos": int(sum(p > 0 for p in per)),
                "per_market": dict(zip(mk, [round(p, 3) for p in per])),
                "top": {"pf": float(top["val_pf"].median()), "sharpe": float(top["val_sharpe"].mean()),
                        "pass": float(top["val_pass"].mean())},
                "bot": {"pf": float(bot["val_pf"].median()), "sharpe": float(bot["val_sharpe"].mean()),
                        "pass": float(bot["val_pass"].mean())}}

    single = {f: score(R[f]) for f in cols}
    part = {f: partial(f) for f in cols if f != "breakeven_cost_multiplier"}

    # 3. equal-weight combinations of 2-4 inputs taken from different families
    fam = {"breakeven_cost_multiplier": "per-trade edge", "dev_avg_trade": "per-trade edge",
           "dev_net_return": "total profit", "stress_cost_1.5x_net_return": "total profit",
           "stress_missed_p10_net_return": "total profit", "stress_delay_net_return": "total profit",
           "dev_profit_factor": "win/loss shape", "dev_win_rate": "win/loss shape",
           "worst_year_sharpe": "consistency", "dev_sharpe": "consistency",
           "local_sd_sharpe": "parameter sensitivity", "dev_exposure": "activity", "dev_n_completed_trades": "activity"}
    combos = {}
    for k in (2, 3, 4):
        for c in itertools.combinations(cols, k):
            if len({fam[f] for f in c}) < k:
                continue
            combos[c] = score(R[list(c)].mean(axis=1))

    # 4. ridge on a chosen few, leave one market out (weights fitted on the other 6 markets)
    from sklearn.linear_model import Ridge
    def lomo(fs):
        X = R[list(fs)].to_numpy() - 0.5
        yr = df.groupby("market")["val_sharpe"].rank(pct=True).to_numpy()
        pred = pd.Series(np.nan, index=df.index)
        for m in mk:
            te = (df["market"] == m).to_numpy()
            pred[te] = Ridge(alpha=10.0).fit(X[~te], yr[~te]).predict(X[te])
        return score(pred)

    best = sorted(combos.items(), key=lambda kv: -kv[1]["ic"])
    out = {"corr": C.round(3).to_dict(), "single": single, "partial_after_breakeven": part,
           "combos_top": [{"inputs": list(c), **s} for c, s in best[:25]],
           "n_combos": len(combos)}
    picks = [("breakeven_cost_multiplier", "worst_year_sharpe"),
             ("breakeven_cost_multiplier", "worst_year_sharpe", "dev_exposure"),
             ("breakeven_cost_multiplier", "worst_year_sharpe", "local_sd_sharpe"),
             ("breakeven_cost_multiplier", "dev_net_return", "worst_year_sharpe", "local_sd_sharpe")]
    out["ridge_lomo"] = {"+".join(p): lomo(p) for p in picks}
    (sm.OUT / "combos.json").write_text(json.dumps(out, default=float))

    pd.set_option("display.width", 250)
    lab = {f: CANDS[f][:14] for f in cols}
    print(C.rename(index=lab, columns=lab).round(2))
    print("\nsingle / partial after break-even")
    for f in cols:
        s = single[f]; p = part.get(f, (np.nan, 0))
        print(f"{CANDS[f]:35s} ic {s['ic']:+.3f} {s['n_pos']}/7  PF {s['top']['pf']:.2f}/{s['bot']['pf']:.2f}  partial {p[0]:+.3f} {p[1]}/7")
    print(f"\n{len(combos)} combos; top 15")
    for c, s in best[:15]:
        print(f"{' + '.join(CANDS[f] for f in c):95s} {s['ic']:+.3f} {s['n_pos']}/7 PF {s['top']['pf']:.2f}/{s['bot']['pf']:.2f} Sh {s['top']['sharpe']:+.2f}/{s['bot']['sharpe']:+.2f} pass {s['top']['pass']:.0%}/{s['bot']['pass']:.0%}")
    for c in picks:
        s = combos.get(c) or score(R[list(c)].mean(axis=1)); r = out["ridge_lomo"]["+".join(c)]
        print(f"PICK {' + '.join(CANDS[f] for f in c):90s} eq {s['ic']:+.3f} {s['n_pos']}/7 PF {s['top']['pf']:.2f}/{s['bot']['pf']:.2f} pass {s['top']['pass']:.0%}/{s['bot']['pass']:.0%} {s['per_market']} | ridge {r['ic']:+.3f} {r['n_pos']}/7 PF {r['top']['pf']:.2f}/{r['bot']['pf']:.2f}")


if __name__ == "__main__":
    main()
