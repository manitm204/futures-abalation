"""One month-end pick on several markets, in one account (2018 .. validation end, or the holdout).

The month-end copy of ../mean-reversion-backtest/scripts/build_combined_portfolio.py ("combined"
page kind on the results site, market tab "ALL"). Legs are frozen funnel picks with their rules
unchanged, optionally on another market (`--leg RUN:ORDER@SYMBOL`, e.g. me_es_v2:7@RTY); only
the symbol and the sizing change.

Deployment rules (fixed before looking at the combined result):
  * micro contracts (1/10 of the full contract: MES, MNQ, M2K, ...), same prices and tick
    slippage, `--micro-commission` per micro per side;
  * each trade is sized at `--per-trade` x the account balance (contract value at entry);
  * open positions in one market may not exceed `--market-cap` x the balance;
  * open positions in the US stock-index futures together (ES, NQ, YM, RTY) may not exceed
    `--group-cap` x the balance; everything open together may not exceed `--total-cap`;
  * a trade that hits a cap gets what is left in whole contracts, and is skipped if that is
    less than one (src/experiments/shared_account.py::share_account_multi).

Luck benchmark: placebo days, as in scripts/run_me_random_benchmark.py. Each random run moves
every leg to the same number of random ordinary days in the window (never among the month's last
5 or first 4 trading days), same clock, same stop, through the same account rules. "Holding" is
the legs' markets equally weighted, rebalanced daily, unlevered.

`--holdout --confirm-holdout-access` scores the 2025+ holdout instead; the legs' frozen holdout
manifest (`--manifest`) is checked, access is authorized and ledgered per market as
`combined_portfolio_holdout`, and the output is `<key>_holdout.json`.

Usage:
  PYTHONPATH=. python scripts/build_me_combined.py --leg me_es_v2:7@ES --leg me_es_v2:7@NQ --leg me_es_v2:7@RTY \
      --manifest runs/funnel/me_es_v2/selection_manifest_1_7_17.json --key month_end_combined_7 \
      --label "#7 on ES + NQ + RTY"
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import typer

from scripts.build_me_portfolio import _band, _occupancy, _stats, _years
from src.analysis.daily_performance import daily_equity
from src.experiments.data_access import load_phase_bars
from src.experiments.funnel_config import load_funnel_config
from src.experiments.shared_account import share_account_multi
from src.strategies.month_end.backtest import CostModel, MEData, SimResult, me_day_bars, simulate_month_end

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = PROJECT_ROOT.parent / "futures-results"
app = typer.Typer(add_completion=False)

INDEX_GROUP = ("ES", "NQ", "YM", "RTY")
MICRO = {"ES": "MES", "NQ": "MNQ", "YM": "MYM", "RTY": "M2K", "CL": "MCL", "GC": "MGC", "ZN": "ZN", "ZB": "ZB"}
PLACEBO_EXCLUDE_LAST, PLACEBO_EXCLUDE_FIRST = 5, 4


def _take_window(sim: SimResult, data: MEData, s64, e64) -> SimResult:
    """Only the trades entering inside [s64, e64] (by session date)."""
    ent = data.session_date[sim.entry_idx] if len(sim.entry_idx) else np.array([], dtype="datetime64[D]")
    k = (ent >= s64) & (ent <= e64)
    return dataclasses.replace(sim, trades=[], equity_curve=[], signal_idx=sim.signal_idx[k], entry_idx=sim.entry_idx[k],
                               exit_idx=sim.exit_idx[k], decision_idx=sim.decision_idx[k], quantity=sim.quantity[k],
                               entry_px=sim.entry_px[k], exit_px=sim.exit_px[k], entry_commission=sim.entry_commission[k],
                               realized_pnl=sim.realized_pnl[k], forced_close=sim.forced_close[k],
                               exit_reason=sim.exit_reason[k], stop_level=sim.stop_level[k],
                               entry_base=sim.entry_base[k], side=sim.side[k])


def _on_days(values: np.ndarray, own_days: np.ndarray, days: np.ndarray, before: float = 0.0) -> np.ndarray:
    """A per-session-close series carried onto `days` (last known value; `before` ahead of its first day)."""
    j = np.searchsorted(own_days, days, side="right") - 1
    return np.where(j >= 0, values[np.clip(j, 0, None)], before)


def _pf(pnl: np.ndarray) -> float | None:
    loss = -pnl[pnl < 0].sum()
    return float(pnl[pnl > 0].sum() / loss) if loss > 0 else None


def _texts(syms, eq0, n_sims, holdout, prior_access) -> dict:
    """Page text for the month-end combined page (the template's defaults describe mean reversion)."""
    mk = ", ".join(syms)
    prior = sum((prior_access or {}).values())
    return {
        "luck_label": "placebo days",
        "lede": (f"One turn-of-month pick, frozen on ES and run unchanged on {mk}, traded together in one "
                 f"${eq0:,.0f} account under fixed deployment rules. Compared with {n_sims} placebo runs (the same "
                 "trades on random ordinary days, never near the month turn, through the same rules) and with "
                 f"holding all {len(syms)} markets equally."),
        "insample_note": ("In-sample on ES: the pick was chosen from 4,864 versions on ES 2018–2022 and checked on ES "
                          "2023–2024. NQ and RTY use the same rules unchanged, but they move closely with ES and trade "
                          "the same days. The holdout tab is the real check."),
        "holdout_caveat": (("First holdout test of this combination. ES 2025+ had already been scored for this pick "
                            "(its final test) and NQ / RTY 2025+ for the unchanged-rules check, so these are not new "
                            "results per market; this page only adds the shared account. "
                            f"Recorded holdout accesses on these markets before this run: {prior}.")
                           if holdout else None),
        "contracts_note": ("Micro contracts trade at the same prices as the full contracts. MES, MNQ and M2K have "
                           "existed only since May 2019, so earlier years are a stand-in for what they would have done."),
    }


@app.command()
def main(
    leg: list[str] = typer.Option(..., help="RUN:ORDER@SYMBOL (repeat), e.g. me_es_v2:7@RTY"),
    manifest: Path = typer.Option(..., exists=True, help="Frozen selection manifest holding every leg's pick"),
    n_sims: int = typer.Option(200, help="Placebo runs for the luck band"),
    key: str = typer.Option(..., help="File / tab id; must start with month_end"),
    label: str = typer.Option(...),
    per_trade: float = typer.Option(0.33), market_cap: float = typer.Option(0.40),
    group_cap: float = typer.Option(1.00), total_cap: float = typer.Option(1.00),
    micro_commission: float = typer.Option(1.00, help="$ per micro contract per side, all-in"),
    holdout: bool = typer.Option(False, "--holdout"),
    confirm_holdout_access: bool = typer.Option(False, "--confirm-holdout-access"),
    runs_root: Path = typer.Option(PROJECT_ROOT / "runs" / "funnel"),
) -> None:
    from scripts.run_me_funnel import _params, _select_space, _sha, load_execution_config
    from src.experiments.data_access import DEFAULT_LEDGER, authorize_holdout_access, read_ledger

    if not key.startswith("month_end"):
        raise typer.BadParameter("key must start with month_end so the month-end page picks it up")
    sel = json.loads(manifest.read_text())
    sel_by_order = {c["dev_order"]: c for c in sel["candidates"]}

    # ---- Legs ----
    specs = []
    for spec in leg:
        run_order, sym = spec.split("@")
        run_id, order = run_order.split(":")
        if run_id != sel["experiment_id"] or int(order) not in sel_by_order:
            raise typer.BadParameter(f"{spec}: not in the frozen manifest {manifest}")
        line, rest = run_id.split("_", 1)
        cfg_path = PROJECT_ROOT / "configs" / "funnel" / f"{line}_funnel_{rest}.yaml"
        fc = load_funnel_config(cfg_path)
        _select_space(fc)
        if fc.config_sha256() != sel["config_sha256"]:
            raise typer.BadParameter(f"{run_id}: config changed since the manifest was frozen.")
        c = sel_by_order[int(order)]
        specs.append({"run": run_id, "fcfg": fc, "cand": c, "order": c["dev_order"], "sym": sym,
                      "params": _params(c["params"], sym), "name": f"{sym} #{c['dev_order']}"})
    syms = list(dict.fromkeys(sp["sym"] for sp in specs))
    base = specs[0]["fcfg"]
    runs = list(dict.fromkeys(sp["run"] for sp in specs))
    ec = load_execution_config(base)
    ec_micro = ec.model_copy(update={"commission_per_contract": micro_commission})

    # ---- Data (per market), holdout authorization per market ----
    bars, info, prior_access = {}, {}, None
    if holdout:
        ledger = read_ledger(DEFAULT_LEDGER)
        prior_access = {s: sum(e.get("phase") == "holdout" and e.get("symbol") == s for e in ledger) for s in syms}
        sha = hashlib.sha256(_sha(sel).encode()).hexdigest()
        for s in syms:
            auth = authorize_holdout_access(manifest_sha256=sha, confirm=confirm_holdout_access,
                                            command="combined_portfolio_holdout")
            bars[s], info[s] = load_phase_bars(base, s, "holdout", command="combined_portfolio_holdout",
                                               experiment_id=key, authorization=auth)
        start = base.data.holdout.start
        end = min(date.fromisoformat(i["actual_last_session"]) for i in info.values())
        key, label = f"{key}_holdout", f"{label} · holdout"
    else:
        for s in syms:
            bars[s], info[s] = load_phase_bars(base, s, "validation", command="combined_portfolio", experiment_id=key)
        start, end = base.data.development.start, base.data.validation.end
    s64, e64 = np.datetime64(start, "D"), np.datetime64(end, "D")
    datas = {s: MEData(me_day_bars(bars[s])) for s in syms}
    for sp in specs:
        sp["data"] = datas[sp["sym"]]

    # Trading days: every session close in the window on any market; clock: every 1-minute bar.
    days = np.unique(np.concatenate([d.days[(d.days >= s64) & (d.days <= e64)] for d in datas.values()]))
    clock = np.unique(np.concatenate([d.bar_open[(d.session_date >= s64) & (d.session_date <= e64)] for d in datas.values()]))
    clock_sd = {}
    for d in datas.values():
        m = (d.session_date >= s64) & (d.session_date <= e64)
        clock_sd.update(zip(d.bar_open[m].tolist(), d.session_date[m].tolist()))
    clock_day = np.array([clock_sd[t] for t in clock.tolist()], dtype="datetime64[D]")

    dev_end = np.datetime64(base.data.development.end, "D")
    n_dev = int((days <= dev_end).sum())
    periods = {"all": (0, len(days) - 1), "dev": (0, n_dev - 1), "val": (n_dev, len(days) - 1)}
    labels = {"all": f"{start.year}–{end.year}", "dev": f"Development {start.year}–{base.data.development.end.year}",
              "val": f"Validation {base.data.validation.start.year}–{end.year}"}
    if holdout:
        periods, labels = {"holdout": (0, len(days) - 1)}, {"holdout": f"Holdout {start.isoformat()} to {end.isoformat()}"}
    pclock = {k: (clock_day >= days[a]) & (clock_day <= days[b]) for k, (a, b) in periods.items()}

    eq0 = ec.starting_equity
    costs = []
    for sp in specs:
        full = CostModel.for_symbol(ec, sp["sym"])
        costs.append(dataclasses.replace(full, ec=ec_micro, multiplier=full.multiplier / 10))
    mins = [1 for _ in specs]
    mkts = [sp["sym"] for sp in specs]
    grps = ["US stock index" if sp["sym"] in INDEX_GROUP else None for sp in specs]
    ds = [sp["data"] for sp in specs]

    def account(sims):
        return share_account_multi(sims, ds, costs, eq0, bar_minutes=mins, per_trade=per_trade, total_cap=total_cap,
                                   market=mkts, market_cap=market_cap, group=grps, group_cap=group_cap,
                                   end_of_bar_extra=("time_exit",))  # a month-end time exit fills at its bar's close

    def leg_pnl(sim, d):
        return _on_days(daily_equity(sim, d, 0.0), d.days, days)

    def equity(sa):
        cum = np.sum([leg_pnl(sm, d) for sm, d in zip(sa.sims, ds)], axis=0)
        return np.concatenate([[eq0], eq0 + cum])

    def occupancy(sim, d):
        occ = np.zeros(len(clock), dtype=bool)
        if len(sim.entry_idx):
            a = np.searchsorted(clock, d.bar_open[sim.entry_idx])
            b = np.searchsorted(clock, d.bar_open[sim.exit_idx])
            for x, y in zip(a, b):
                occ[x:y + 1] = True
        return occ

    def pstats(eq, pairs, k):
        a, b = periods[k]
        lo_d, hi_d = days[a], days[b]
        pnl, n_c = [], 0
        for sm, d in pairs:
            ent = d.session_date[sm.entry_idx] if len(sm.entry_idx) else np.array([], dtype="datetime64[D]")
            t = (ent >= lo_d) & (ent <= hi_d)
            pnl.append(sm.realized_pnl[t]); n_c += int((~sm.forced_close[t]).sum())
        occ = np.logical_or.reduce([occupancy(sm, d) for sm, d in pairs]) & pclock[k]
        return _stats(eq[a:b + 2], np.concatenate(pnl), n_c, occ.sum() / pclock[k].sum())

    # ---- The picks' own trade lists (full-size run; only entries/exits/prices are used) ----
    for sp in specs:
        d = sp["data"]
        sim = simulate_month_end(d, sp["params"], exec_config=ec, starting_equity=eq0)
        sp["sim"] = _take_window(sim, d, s64, e64)
        win = (d.session_date >= s64) & (d.session_date <= e64)
        sp["exposure"] = (_occupancy(sp["sim"], d) & win).sum() / win.sum()
        in_win = (d.days >= s64) & (d.days <= e64)
        sp["pool"] = np.flatnonzero(in_win & (d.rank > PLACEBO_EXCLUDE_LAST) & (d.rank_start > PLACEBO_EXCLUDE_FIRST))
        sp["n_days"] = int(len(np.unique(d.sess[sp["sim"].entry_idx])))
    sa = account([sp["sim"] for sp in specs])
    ceq = equity(sa)
    pairs = list(zip(sa.sims, ds))

    # ---- Luck: placebo days per leg (same clock and stop), same account rules ----
    rng = np.random.default_rng([base.seed, 7777])
    rand = []
    for i in range(n_sims):
        rs = []
        for sp in specs:
            d = sp["data"]
            mask = np.zeros(len(d.days), dtype=bool)
            mask[rng.choice(sp["pool"], size=min(sp["n_days"], len(sp["pool"])), replace=False)] = True
            r = simulate_month_end(d, sp["params"], exec_config=ec, starting_equity=eq0, day_mask=mask)
            rs.append(_take_window(r, d, s64, e64))
        r_sa = account(rs)
        rand.append((list(zip(r_sa.sims, ds)), equity(r_sa)))
        if (i + 1) % 50 == 0:
            typer.echo(f"  placebo {i + 1}/{n_sims}")
    curves = np.array([q / q[0] for _, q in rand])
    r_years = [_years(days, c) for c in curves]
    per = {}
    for k, (a, b) in periods.items():
        st = pstats(ceq, pairs, k)
        rs = [pstats(q, rp, k) for rp, q in rand]
        sh = np.array([x["sharpe"] if x["sharpe"] is not None else -np.inf for x in rs])
        rt = np.array([x["net_return"] for x in rs])
        seg = curves[:, a:b + 2] / curves[:, a:a + 1]
        per[k] = {"stats": st, "luck": {
            "band": _band(seg), "pct_sharpe": float(np.mean(sh < st["sharpe"])), "pct_return": float(np.mean(rt < st["net_return"])),
            "mean_stats": {m: float(np.mean([x[m] for x in rs if x[m] is not None]))
                           for m in ("net_return", "cagr", "sharpe", "max_drawdown", "n_completed_trades", "win_rate",
                                     "profit_factor", "exposure")}}}
        pf = st["profit_factor"]
        typer.echo(f"combined {k}: return {st['net_return']:+.1%}, Sharpe {st['sharpe']:.2f}, PF "
                   f"{'n/a' if pf is None else f'{pf:.2f}'}, DD {st['max_drawdown']:.1%}, "
                   f"beats {per[k]['luck']['pct_sharpe']:.0%} of placebo runs on Sharpe")
    combined = {"name": label, "equity": np.round(ceq / ceq[0], 5).tolist(), "periods": per,
                "years": _years(days, ceq), "random_years_mean": {y: float(np.mean([yy[y] for yy in r_years])) for y in r_years[0]},
                "peak": sa.peak}

    # ---- Per leg and per market: P&L, sizing, which cap bound ----
    def tally(idx, k):
        a, b = periods[k]
        out = {"pnl": 0.0, "trades": 0, "signals": 0, "full": 0, "trimmed": 0, "skipped": 0,
               "bound": {"market": 0, "group": 0, "total": 0}, "contracts": []}
        pnl = []
        for i in idx:
            sp, sm = specs[i], sa.sims[i]
            ent_all = sp["data"].session_date[sp["sim"].entry_idx]
            t = (ent_all >= days[a]) & (ent_all <= days[b])
            kk, tr, bd = sa.contracts[i][t], sa.trimmed[i][t], sa.bound[i][t]
            out["signals"] += int(t.sum()); out["skipped"] += int((kk == 0).sum())
            out["full"] += int(((kk > 0) & ~tr).sum()); out["trimmed"] += int(((kk > 0) & tr).sum())
            for c in ("market", "group", "total"):
                out["bound"][c] += int((bd == c).sum())
            out["contracts"] += kk[kk > 0].tolist()
            ent = sp["data"].session_date[sm.entry_idx]
            tt = (ent >= days[a]) & (ent <= days[b])
            pnl.append(sm.realized_pnl[tt])
        p = np.concatenate(pnl) if pnl else np.array([])
        out.update(pnl=float(p.sum()), trades=int(len(p)), win_rate=float((p > 0).mean()) if len(p) else None,
                   profit_factor=_pf(p), contrib=float(p.sum() / (ceq[a])),
                   mean_contracts=float(np.mean(out["contracts"])) if out["contracts"] else None)
        del out["contracts"]
        return out

    legs_out = [{"name": sp["name"], "market": sp["sym"], "micro": MICRO.get(sp["sym"], sp["sym"]), "run_id": sp["run"],
                 "order": sp["order"], "timeframe": "1min", "settings": {**sp["cand"]["params"], "symbol": sp["sym"]},
                 "exposure_alone": float(sp["exposure"]), "periods": {k: tally([i], k) for k in periods}}
                for i, sp in enumerate(specs)]
    mpnl = {s: np.sum([leg_pnl(sa.sims[i], ds[i]) for i, sp in enumerate(specs) if sp["sym"] == s], axis=0) for s in syms}
    markets_out = []
    yrs = days.astype("datetime64[Y]").astype(int) + 1970
    for s in syms:
        idx = [i for i, sp in enumerate(specs) if sp["sym"] == s]
        cum = np.concatenate([[0.0], mpnl[s]])
        myears = {}
        for y in np.unique(yrs):
            ii = np.flatnonzero(yrs == y)
            myears[str(y)] = float((cum[ii[-1] + 1] - cum[ii[0]]) / ceq[ii[0]])
        markets_out.append({"code": s, "micro": MICRO.get(s, s), "legs": [specs[i]["name"] for i in idx], "years": myears,
                            "pnl_curve": np.round(cum / eq0, 5).tolist(), "periods": {k: tally(idx, k) for k in periods}})

    acct = ceq[:-1]
    mret = {s: np.diff(np.concatenate([[0.0], mpnl[s]])) / acct for s in syms}
    corr = {}
    for k, (a, b) in periods.items():
        M = np.array([mret[s][a:b + 1] for s in syms])
        ok = M.std(axis=1) > 0
        C = np.full((len(syms), len(syms)), np.nan)
        C[np.ix_(ok, ok)] = np.corrcoef(M[ok]) if ok.sum() > 1 else np.nan
        corr[k] = [[None if np.isnan(v) else round(float(v), 3) for v in row] for row in C]
        typer.echo(f"daily P&L correlation {k}: " + ", ".join(
            f"{syms[i]}-{syms[j]} {C[i, j]:.2f}" for i in range(len(syms)) for j in range(i + 1, len(syms))))

    # ---- Holding: the legs' markets equally weighted, rebalanced daily, unlevered ----
    hr = []
    for s in syms:
        d = datas[s]
        e = d.day_end_idx
        adj, raw = d.close[e], d.close[e] - d.price_adj[e]
        r = np.concatenate([[0.0], np.diff(adj) / raw[:-1]])
        mask = np.isin(d.days, days)
        rr = np.zeros(len(days))
        rr[np.searchsorted(days, d.days[mask])] = r[mask]
        hr.append(rr)
    heq = np.concatenate([[1.0], np.cumprod(1 + np.mean(hr, axis=0))])
    hold = {"name": f"Holding {' + '.join(syms)} equally", "equity": np.round(heq, 5).tolist(), "years": _years(days, heq),
            "periods": {k: {"stats": _stats(heq[a:b + 2] * eq0, np.array([]), 0, 1.0)} for k, (a, b) in periods.items()}}

    out = {
        "kind": "combined", "market": "ALL", "market_name": "All markets", "strategy_key": key, "strategy_name": label,
        "run_id": " + ".join(runs), "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "period": [str(start), str(end)], "validation_start": str(base.data.validation.start),
        "holdout": holdout, "prior_holdout_accesses": prior_access,
        "rules": {"per_trade": per_trade, "market_cap": market_cap, "group_cap": group_cap, "group_name": "US stock index",
                  "group": list(INDEX_GROUP), "total_cap": total_cap, "contracts": "micro", "micro_commission": micro_commission,
                  "slippage_ticks": ec.slippage_ticks_market},
        "starting_equity": eq0, "n_sims": n_sims, "hold_bars": None, "markets_order": syms,
        **_texts(syms, eq0, n_sims, holdout, prior_access),
        "luck_method": ("Placebo days: each run moves every leg to the same number of random ordinary days (never among "
                        "the month's last 5 or first 4 trading days), same clock and stop, same account rules."),
        "selection_note": sel.get("holdout_selection_note"),
        "days": [str(d) for d in days], "periods": {k: {"range": list(v), "label": labels[k]} for k, v in periods.items()},
        "combined": combined, "markets": markets_out, "legs": legs_out, "corr": corr, "hold": hold,
        "data_access": info,
        "source": " · ".join([f"month-end-backtest/runs/funnel/{r}/" for r in runs] + ["scripts/build_me_combined.py"]),
    }
    path = SITE_ROOT / "data" / "ALL" / f"{key}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out))
    typer.echo(f"wrote {path}")


if __name__ == "__main__":
    app()
