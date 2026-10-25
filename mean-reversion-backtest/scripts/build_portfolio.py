"""Chosen strategies, individually and run together, vs random entries (2018 .. validation end).

Picks finalists by development order from one or more funnel runs' frozen
manifests (`--leg RUN:ORDER`, repeated; each run's config is
configs/funnel/mr_funnel_<run minus "mr_">.yaml), runs each over development +
validation (one continuous backtest on its own bar size, no re-tuning), and
writes a "portfolio" page for the results site. All legs must share one market
and the same data windows.

  * each strategy alone on the full starting equity;
  * the strategies together in one account (src/experiments/shared_account.py):
    each trade is sized at `--per-trade` x the account balance (default 0.75),
    and the open positions together may not exceed `--cap` x the balance
    (default 1.0), so a trade opening while another is open gets what is left
    (the remaining 0.25). Whole contracts; a trade that can't afford one is
    skipped. The old equal-split sleeves are kept as a reference line;
  * a luck benchmark for each: `--n-sims` random-entry runs
    (src/experiments/random_entry.py) at the strategy's own 2018-2024 time in
    market, 3-10 bar holds, same costs and sizing. The combined luck run uses one
    random trade stream per strategy at that strategy's time in market, sized
    through the same shared account.

Uses data through the validation end only (never the holdout); logged to the
data-access ledger as command `portfolio`.

`--holdout --confirm-holdout-access` instead scores the same strategies on the
2025+ holdout only (positions and indicators still warm up on earlier data).
It needs every leg's frozen selection manifest (config unchanged since it was
frozen), goes through `authorize_holdout_access`, is ledgered as command
`portfolio_holdout`, and writes `<key>_holdout.json`. Luck runs are matched to
each strategy's holdout time in market.

Usage:
  PYTHONPATH=. python scripts/build_portfolio.py --leg mr_es_v6_1h:8 --leg mr_es_v6_1h:15
  PYTHONPATH=. python scripts/build_portfolio.py --leg mr_nq_v7_15m:1 --leg mr_nq_v7_1h:119 \
      --key portfolio_v7 --label "Portfolio · v7 15m #1 + 1h #119" --market-name "E-mini Nasdaq-100"
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import typer

from src.analysis.daily_performance import _drawdown, _sharpe, daily_equity
from src.data.aggregation import AGG_INTERVAL_MINUTES, aggregate_bars
from src.experiments.data_access import load_phase_bars
from src.experiments.funnel_config import load_funnel_config
from src.experiments.random_entry import simulate_random_entries
from src.experiments.shared_account import share_account
from src.strategies.mean_reversion.backtest import CostModel, MRData, SimResult, simulate_mean_reversion

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = PROJECT_ROOT.parent / "futures-results"
app = typer.Typer(add_completion=False)
QS = (0.05, 0.10, 0.50, 0.90, 0.95)


def _occupancy(sim: SimResult, data: MRData) -> np.ndarray:
    """Bars with an open position, counted entry bar through exit bar."""
    occ = np.zeros(data.n, dtype=bool)
    for a, b in zip(sim.entry_idx, sim.exit_idx):
        occ[a:b + 1] = True
    return occ


def _on_ref(occ: np.ndarray, data: MRData, ref: MRData) -> np.ndarray:
    """Occupancy of `data`'s bars carried onto the (finer or equal) reference bars:
    a reference bar is occupied if the bar of `data` it falls in is."""
    if data is ref:
        return occ
    j = np.searchsorted(data.bar_open, ref.bar_open, side="right") - 1
    ok = (j >= 0) & (data.session_date[np.clip(j, 0, None)] == ref.session_date)
    return ok & occ[np.clip(j, 0, None)]


def _stats(eq: np.ndarray, pnl: np.ndarray, n_completed: int, in_mkt: float, ppy: int = 252) -> dict:
    """eq[0] = equity before the first window day, eq[1:] = each session close."""
    rets = eq[1:] / eq[:-1] - 1.0
    n = len(rets)
    sharpe, _ = _sharpe(rets, ppy, 0.0)
    dd, dd_days, _ = _drawdown(eq)
    wins, losses = pnl[pnl > 0], pnl[pnl < 0]
    return {"net_return": float(eq[-1] / eq[0] - 1), "cagr": float((eq[-1] / eq[0]) ** (ppy / n) - 1) if n else None,
            "sharpe": sharpe, "max_drawdown": float(dd), "max_dd_days": int(dd_days),
            "n_completed_trades": int(n_completed), "win_rate": float((pnl > 0).mean()) if len(pnl) else None,
            "profit_factor": float(wins.sum() / -losses.sum()) if len(losses) else None,
            "exposure": float(in_mkt), "vol": float(rets.std(ddof=1) * np.sqrt(ppy)) if n > 1 else None}


def _years(days: np.ndarray, eq: np.ndarray) -> dict:
    out, prev = {}, eq[0]
    years = days.astype("datetime64[Y]").astype(int) + 1970
    for y in np.unique(years):
        last = eq[1:][years == y][-1]
        out[str(y)] = float(last / prev - 1)
        prev = last
    return out


def _band(curves: np.ndarray) -> dict:
    """Per-day quantiles / mean of normalized random equity curves (rows = sims)."""
    out = {f"p{int(q * 100)}": np.round(np.quantile(curves, q, axis=0), 4).tolist() for q in QS}
    out["mean"] = np.round(curves.mean(axis=0), 4).tolist()
    return out


@app.command()
def main(
    leg: list[str] = typer.Option(..., help="RUN:ORDER, e.g. mr_nq_v7_1h:119 (repeat for each strategy)"),
    n_sims: int = typer.Option(200, help="Random-entry runs per luck band"),
    key: str = typer.Option("portfolio_v6_1h"),
    label: str = typer.Option("Portfolio · v6 1h #8 + #15"),
    market_name: str = typer.Option("E-mini S&P 500"),
    hold_lo: int = typer.Option(3), hold_hi: int = typer.Option(10),
    holdout: bool = typer.Option(False, "--holdout", help="Score on the 2025+ holdout instead of 2018..validation end"),
    confirm_holdout_access: bool = typer.Option(False, "--confirm-holdout-access"),
    per_trade: float = typer.Option(0.75, help="Each trade's size as a share of the account balance"),
    cap: float = typer.Option(1.0, help="Most the open positions together may use, as a share of the balance"),
    runs_root: Path = typer.Option(PROJECT_ROOT / "runs" / "funnel"),
) -> None:
    import hashlib

    from scripts.run_mr_funnel import _params, _select_space, _sha, load_execution_config
    from src.experiments.data_access import DEFAULT_LEDGER, authorize_holdout_access, read_ledger

    # ---- Legs: (run, order) -> frozen candidate, its run's config, built params ----
    specs = []
    for spec in leg:
        run_id, order = spec.split(":")
        cfg_path = PROJECT_ROOT / "configs" / "funnel" / f"mr_funnel_{run_id.removeprefix('mr_')}.yaml"
        fc = load_funnel_config(cfg_path)
        _select_space(fc)  # _params builds configs of this run's grid
        cands = {c["dev_order"]: c for c in json.loads((runs_root / run_id / "frozen_representatives.json").read_text())["candidates"]}
        c = cands[int(order)]
        specs.append({"run": run_id, "config": cfg_path, "fcfg": fc, "cand": c, "order": c["dev_order"],
                      "params": _params(c["params"]), "tf": c["params"]["timeframe"]})
    fcfg = specs[0]["fcfg"]
    for sp in specs[1:]:
        if sp["fcfg"].symbol != fcfg.symbol or sp["fcfg"].data != fcfg.data:
            raise typer.BadParameter("all legs must share one market and the same data windows")
    tfs = sorted({sp["tf"] for sp in specs}, key=AGG_INTERVAL_MINUTES.get)
    multi_tf = len(tfs) > 1
    for sp in specs:
        sp["name"] = f"{sp['tf'].replace('min', 'm')} #{sp['order']}" if multi_tf else f"#{sp['order']}"
    runs = sorted({sp["run"] for sp in specs})
    ec = load_execution_config(fcfg)

    prior_access = None
    if holdout:
        prior_access = sum(e.get("phase") == "holdout" and e.get("symbol") == fcfg.symbol for e in read_ledger(DEFAULT_LEDGER))
        shas = []
        for run_id in runs:
            sp = next(x for x in specs if x["run"] == run_id)
            sel = json.loads((runs_root / run_id / "selection_manifest.json").read_text())
            if sp["fcfg"].config_sha256() != sel["config_sha256"]:
                raise typer.BadParameter(f"{run_id}: config changed since the manifest was frozen.")
            shas.append(_sha(sel))
        auth = authorize_holdout_access(manifest_sha256=hashlib.sha256("".join(shas).encode()).hexdigest(),
                                        confirm=confirm_holdout_access, command="portfolio_holdout")
        bars, info = load_phase_bars(fcfg, fcfg.symbol, "holdout", command="portfolio_holdout",
                                     experiment_id="+".join(runs), authorization=auth)
        start, end = fcfg.data.holdout.start, date.fromisoformat(info["actual_last_session"])
        key = f"{key}_holdout"
        label = f"{label} · holdout"
    else:
        start, end = fcfg.data.development.start, fcfg.data.validation.end
        bars, info = load_phase_bars(fcfg, fcfg.symbol, "validation", command="portfolio", experiment_id="+".join(runs))
    datas = {tf: MRData(aggregate_bars(bars, timeframe=tf)) for tf in tfs}
    ref = datas[tfs[0]]  # finest bar size: shared clock for "in the market"
    for d in datas.values():
        if not np.array_equal(d.days, ref.days):
            raise typer.BadParameter("bar sizes disagree on the trading days")
    for sp in specs:
        sp["data"] = datas[sp["tf"]]
    s64, e64 = np.datetime64(start, "D"), np.datetime64(end, "D")
    dmask = (ref.days >= s64) & (ref.days <= e64)
    days = ref.days[dmask]
    prior = np.flatnonzero(ref.days < s64)
    eq0 = ec.starting_equity
    share = eq0 / len(specs)
    costs = CostModel.for_symbol(ec, fcfg.symbol)

    # Periods the page can switch between: index ranges into `days` (inclusive).
    dev_end = np.datetime64(fcfg.data.development.end, "D")
    n_dev = int((days <= dev_end).sum())
    periods = {"all": (0, len(days) - 1), "dev": (0, n_dev - 1), "val": (n_dev, len(days) - 1)}
    labels = {"all": f"{start.year}–{end.year}", "dev": f"Development {start.year}–{fcfg.data.development.end.year}",
              "val": f"Validation {fcfg.data.validation.start.year}–{end.year}"}
    if holdout:
        periods, labels = {"holdout": (0, len(days) - 1)}, {"holdout": f"Holdout {start.isoformat()} to {end.isoformat()}"}

    def bars_in(d, k):
        a, b = periods[k]
        return (d.session_date >= days[a]) & (d.session_date <= days[b])

    window = {tf: (d.session_date >= s64) & (d.session_date <= e64) for tf, d in datas.items()}
    pbar = {k: bars_in(ref, k) for k in periods}

    def daily(sim, data, equity):
        eq = daily_equity(sim, data, equity)
        e0 = float(eq[prior[-1]]) if len(prior) else equity
        return np.concatenate([[e0], eq[dmask]])

    def run(sp, equity):
        sim = simulate_mean_reversion(sp["data"], sp["params"], exec_config=ec, starting_equity=equity)
        return sim, daily(sim, sp["data"], equity)

    def rand(sp, exposure, equity, rng):
        sim = simulate_random_entries(sp["data"], fcfg.symbol, exec_config=ec, starting_equity=equity, window_start=start,
                                      window_end=end, exposure=exposure, rng=rng, hold_lo=hold_lo, hold_hi=hold_hi)
        return sim, np.concatenate([[equity], daily_equity(sim, sp["data"], equity)[dmask]])

    ds = [sp["data"] for sp in specs]
    mins = [AGG_INTERVAL_MINUTES[sp["tf"]] for sp in specs]

    def account(sims):
        """One shared account: re-size the trade lists, equity = start + every strategy's P&L."""
        sa = share_account(sims, ds, costs, eq0, bar_minutes=mins, per_trade=per_trade, cap=cap)
        eq = eq0 + np.sum([daily_equity(sm, d, 0.0) for sm, d in zip(sa.sims, ds)], axis=0)
        e0 = float(eq[prior[-1]]) if len(prior) else eq0
        return sa, np.concatenate([[e0], eq[dmask]])

    def pstats(eq, pairs, k):
        """Stats over period k for (sim, data) pairs: eq[a] is the close before its first day; trades by
        entry session; time in market = share of reference bars with any position open."""
        a, b = periods[k]
        lo_d, hi_d = days[a], days[b]
        pnl, n_c = [], 0
        for sm, d in pairs:
            ent = d.session_date[sm.entry_idx] if len(sm.entry_idx) else np.array([], dtype="datetime64[D]")
            t = (ent >= lo_d) & (ent <= hi_d)
            pnl.append(sm.realized_pnl[t]); n_c += int((~sm.forced_close[t]).sum())
        occ = np.logical_or.reduce([_on_ref(_occupancy(sm, d), d, ref) for sm, d in pairs]) & pbar[k]
        return _stats(eq[a:b + 2], np.concatenate(pnl), n_c, occ.sum() / pbar[k].sum())

    def block(name, eq, pairs, rand_runs, extra=None):
        """rand_runs: list of (pairs, eq) random runs matching this block."""
        curves = np.array([q / q[0] for _, q in rand_runs])
        r_years = [_years(days, c) for c in curves]
        per = {}
        for k, (a, b) in periods.items():
            st = pstats(eq, pairs, k)
            rs = [pstats(q, rp, k) for rp, q in rand_runs]
            sh = np.array([x["sharpe"] if x["sharpe"] is not None else -np.inf for x in rs])
            rt = np.array([x["net_return"] for x in rs])
            seg = curves[:, a:b + 2] / curves[:, a:a + 1]
            per[k] = {"stats": st, "luck": {
                "band": _band(seg), "pct_sharpe": float(np.mean(sh < st["sharpe"])),
                "pct_return": float(np.mean(rt < st["net_return"])),
                "mean_stats": {m: float(np.mean([x[m] for x in rs if x[m] is not None]))
                               for m in ("net_return", "cagr", "sharpe", "max_drawdown", "n_completed_trades",
                                         "win_rate", "profit_factor", "exposure")}}}
        out = {"name": name, "equity": np.round(eq / eq[0], 5).tolist(), "periods": per, "years": _years(days, eq),
               "random_years_mean": {y: float(np.mean([yy[y] for yy in r_years])) for y in r_years[0]}}
        return {**out, **(extra or {})}

    legs = []
    for sp in specs:
        d = sp["data"]
        sim, eq = run(sp, eq0)
        exposure = (_occupancy(sim, d) & window[sp["tf"]]).sum() / window[sp["tf"]].sum()
        rng = np.random.default_rng([fcfg.seed, sp["order"]])
        rr = []
        for _ in range(n_sims):
            r_sim, r_eq = rand(sp, exposure, eq0, rng)
            rr.append(([(r_sim, d)], r_eq))
        s_sim, s_eq = run(sp, share)  # equal-split sleeve, kept as a reference line
        sp.update(sim=sim, eq=eq, sleeve_sim=s_sim, sleeve_eq=s_eq, exposure=exposure)
        legs.append(block(sp["name"], eq, [(sim, d)], rr,
                          {"order": sp["order"], "run_id": sp["run"], "config_id": sp["cand"]["config_id"],
                           "settings": sp["cand"]["params"]}))
        for k in periods:
            P = legs[-1]["periods"][k]
            typer.echo(f"{sp['name']} {k}: return {P['stats']['net_return']:+.1%}, Sharpe {P['stats']['sharpe']:.2f}, "
                       f"beats {P['luck']['pct_sharpe']:.0%} of random on Sharpe")

    # Combined: one shared account; random = one random trade stream per strategy, same account rules.
    sa, ceq = account([sp["sim"] for sp in specs])
    rng = np.random.default_rng([fcfg.seed, 999])
    rr = []
    for _ in range(n_sims):
        r_sa, r_eq = account([rand(sp, sp["exposure"], eq0, rng)[0] for sp in specs])
        rr.append((list(zip(r_sa.sims, ds)), r_eq))

    # How the sizing rule played out, per period (trades by entry session).
    sleq = np.sum([sp["sleeve_eq"] for sp in specs], axis=0)
    sizing = {"per_trade": per_trade, "cap": cap, "periods": {}}
    for k, (a, b) in periods.items():
        legs_sz = []
        for sp, n_c, tr in zip(specs, sa.contracts, sa.trimmed):
            ent = sp["data"].session_date[sp["sim"].entry_idx]
            t = (ent >= days[a]) & (ent <= days[b])
            kk = n_c[t]
            legs_sz.append({"order": sp["order"], "name": sp["name"], "signals": int(t.sum()),
                            "full": int(((kk > 0) & ~tr[t]).sum()), "trimmed": int(((kk > 0) & tr[t]).sum()),
                            "skipped": int((kk == 0).sum()),
                            "mean_contracts": float(kk[kk > 0].mean()) if (kk > 0).any() else None})
        sizing["periods"][k] = {"legs": legs_sz, "sleeves": pstats(sleq, [(sp["sleeve_sim"], sp["data"]) for sp in specs], k)}
    sleeve_curve = np.round(sleq / sleq[0], 5).tolist()

    # Correlation between the two strategies (each alone on the full account), per period.
    rets = np.array([np.diff(sp["eq"]) / sp["eq"][:-1] for sp in specs])
    occs = [_on_ref(_occupancy(sp["sim"], sp["data"]), sp["data"], ref) for sp in specs]
    months = days.astype("datetime64[M]")

    def corr(x, y):
        return float(np.corrcoef(x, y)[0, 1]) if len(x) > 2 and x.std() > 0 and y.std() > 0 else None

    cor = {}
    for k, (a, b) in periods.items():
        x, y = rets[0, a:b + 1], rets[1, a:b + 1]
        act = (x != 0) | (y != 0)
        mk = months[a:b + 1]
        um = np.unique(mk)
        mx = np.array([np.prod(1 + x[mk == m]) - 1 for m in um]); my = np.array([np.prod(1 + y[mk == m]) - 1 for m in um])
        o0, o1 = occs[0] & pbar[k], occs[1] & pbar[k]
        either = (o0 | o1).sum()
        cor[k] = {"daily": corr(x, y), "daily_active": corr(x[act], y[act]), "monthly": corr(mx, my),
                  "overlap_frac": float((o0 & o1).sum() / either) if either else None,
                  "both_down_days": int(((x < 0) & (y < 0)).sum()), "either_down_days": int(((x < 0) | (y < 0)).sum()),
                  "both_up_days": int(((x > 0) & (y > 0)).sum()), "active_days": int(act.sum())}
    win = 63
    roll = [None] * len(days)
    for t in range(win - 1, len(days)):
        roll[t] = corr(rets[0, t - win + 1:t + 1], rets[1, t - win + 1:t + 1])
    combined = block(" + ".join(sp["name"] for sp in specs), ceq, list(zip(sa.sims, ds)), rr,
                     {"sizing": sizing, "sleeves_equity": sleeve_curve, "correlation": cor,
                      "rolling_corr": {"window": win, "values": [None if v is None else round(v, 3) for v in roll]}})
    for k in periods:
        P = combined["periods"][k]
        typer.echo(f"combined {k}: return {P['stats']['net_return']:+.1%}, Sharpe {P['stats']['sharpe']:.2f}, "
                   f"beats {P['luck']['pct_sharpe']:.0%}; corr {cor[k]['daily']:.2f}")

    # Holding the market (rolled, unlevered): session-close returns of the back-adjusted price / raw price.
    e_idx = ref.day_end_idx[dmask]
    prev = ref.day_end_idx[np.flatnonzero(dmask)[0] - 1] if np.flatnonzero(dmask)[0] > 0 else e_idx[0]
    idx = np.concatenate([[prev], e_idx])
    adj, raw = ref.close[idx], ref.close[idx] - ref.price_adj[idx]
    heq = np.concatenate([[1.0], np.cumprod(1 + np.diff(adj) / raw[:-1])])
    hold = {"name": f"Holding {fcfg.symbol}", "equity": np.round(heq, 5).tolist(), "years": _years(days, heq),
            "periods": {k: {"stats": _stats(heq[a:b + 2] * eq0, np.array([]), 0, 1.0)} for k, (a, b) in periods.items()}}

    out = {
        "kind": "portfolio", "market": fcfg.symbol, "market_name": market_name,
        "strategy_key": key, "strategy_name": label, "run_id": " + ".join(runs),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "period": [str(start), str(end)], "validation_start": str(fcfg.data.validation.start),
        "holdout": holdout, "prior_holdout_accesses": prior_access,
        "timeframe": " / ".join(tfs), "starting_equity": eq0, "n_sims": n_sims, "hold_bars": [hold_lo, hold_hi],
        "days": [str(d) for d in days], "periods": {k: {"range": list(v), "label": labels[k]} for k, v in periods.items()},
        "legs": legs, "combined": combined, "hold": hold,
        "data_access": info,
        "source": " · ".join([f"mean-reversion-backtest/runs/funnel/{r}/" for r in runs]
                             + sorted({sp["config"].relative_to(PROJECT_ROOT).as_posix() for sp in specs})
                             + ["scripts/build_portfolio.py"]),
    }
    path = SITE_ROOT / "data" / fcfg.symbol / f"{key}.json"
    path.write_text(json.dumps(out))
    typer.echo(f"wrote {path}")


if __name__ == "__main__":
    app()
