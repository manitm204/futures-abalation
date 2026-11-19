"""Chosen EMRT spread strategies (futures PAIRS), individually and together, vs random entries
(2018 .. validation end, or the holdout with --holdout).

The pair counterpart of ../price-path-convexity-backtest/scripts/build_pc_portfolio.py: same page ("portfolio" kind on the results
site), same period switcher and the same kind of random-entry luck benchmark, adapted for two legs:
  * each leg (`--leg RUN:ORDER`, config configs/funnel/emrt_funnel_<pair>_<ver>.yaml) is simulated
    with the pair backtester and marked to market on both legs at every session close;
  * random entries: random INTRADAY spread trades (never overlapping, closed by the session's last
    bar), lengths drawn from that strategy's own trades, long-spread share = the strategy's, the
    SAME month's hedge ratio, whole-contract sizing and per-leg costs as the strategy;
  * together = the account split equally between the strategies (each runs its own half; each trade
    uses its half), so the page's sizing rule is per trade 1/n of the account, cap 1x.

Holdout mode (`--holdout --confirm-holdout-access`) scores the same frozen strategies on the 2025+
holdout only, needs the run's frozen manifest (`--manifest`, unchanged config), goes through
`authorize_holdout_access`, is ledgered as `portfolio_holdout` and writes `<key>_holdout.json`.

Usage:
  PYTHONPATH=. python scripts/build_emrt_portfolio.py --leg emrt_esrty_v2:2 --leg emrt_esrty_v2:10 \\
      --manifest runs/funnel/emrt_esrty_v2/selection_manifest_2_10.json \\
      --key emrt_spread_portfolio_esrty_v2 --label "Holdout · v2 #2 + #10" --holdout --confirm-holdout-access
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import replace
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import typer

from src.analysis.daily_performance import _drawdown, _sharpe
from src.strategies.emrt_spread.backtest import (
    PairData,
    SimResult,
    _legs,
    _slip,
    pair_daily_equity,
    simulate_emrt_spread,
    size_pair,
)
from src.strategies.emrt_spread.config import split_pair

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = PROJECT_ROOT.parent / "futures-results"
app = typer.Typer(add_completion=False)
QS = (0.05, 0.10, 0.50, 0.90, 0.95)
NAMES = {"ES": "E-mini S&P 500", "NQ": "E-mini Nasdaq-100", "YM": "E-mini Dow", "RTY": "E-mini Russell 2000",
         "ZN": "10-year T-note", "ZB": "30-year T-bond"}


def _occupancy(sim, n: int) -> np.ndarray:
    occ = np.zeros(n, dtype=bool)
    for a, b in zip(sim.entry_idx, sim.exit_idx):
        occ[a:b + 1] = True
    return occ


def _stats(eq: np.ndarray, pnl: np.ndarray, n_completed: int, in_mkt: float, ppy: int = 252) -> dict:
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
    out = {f"p{int(q * 100)}": np.round(np.quantile(curves, q, axis=0), 4).tolist() for q in QS}
    out["mean"] = np.round(curves.mean(axis=0), 4).tolist()
    return out


def _settings_text(p: dict, a: str, b: str) -> str:
    hedge = {"ols": "OLS hedge ratio (control)", "notional": "1:1 dollar-neutral hedge (control)"}.get(
        p["hedge"], f"EMRT hedge ratio (C = {p['hedge'][6:]})")
    z = ("z against the formation window" if p["z_mode"] == "formation"
         else f"z by time of day (same bar, last {p['z_mode'][4:]} sessions)")
    side = {"both": "long + short spread", "long": f"long spread only (long {a}, short {b})",
            "short": f"short spread only (short {a}, long {b})"}[p["side"]]
    ex = {"mean": "exit at the mean", "half": "exit half-way back"}[p["exit"]]
    stop = "no stop" if p["stop"] == "none" else f"stop +{float(p['stop']):g} z"
    ts = "no time stop" if p["time_stop"] == "none" else "time stop 3 × EMRT"
    fe = "" if not int(p.get("first_entry", 0)) else f", no entries in the first {int(p['first_entry'])} min"
    return (f"{p['timeframe'].replace('min', 'm')} bars, {a} vs {b} measured from each day's open, {hedge} refit monthly "
            f"on {p['formation']} month(s), {z}, enter at |z| {float(p['entry_z']):g}, {ex}, {stop}, {ts}, {side}{fe}, "
            "flat at the close")


def random_pair_trades(data: PairData, bp: dict, pair: str, *, exec_config, starting_equity: float, start: date,
                       end: date, exposure: float, length_pool: np.ndarray, p_long: float, rng) -> SimResult:
    """Random intraday spread trades covering ~`exposure` of the window's bars: random sessions and
    start bars, never overlapping, closed by the session's last close; entry at a bar's open, exit at
    the close of the bar `length - 1` later (or the session's last bar). Same month's beta, sizing,
    per-leg slippage and commissions as the strategy."""
    la, lb = _legs(pair)
    ec = exec_config
    com, tk = ec.commission_per_contract, ec.slippage_ticks_market
    s64, e64 = np.datetime64(start, "D"), np.datetime64(end, "D")
    win = np.flatnonzero((data.session_date >= s64) & (data.session_date <= e64))
    target = int(round(exposure * len(win)))
    sess_ids = np.unique(data.sess[win])
    busy = np.zeros(data.n, dtype=bool)
    trades = []
    used, tries = 0, 0
    while used < target and tries < 50 * max(1, target):
        tries += 1
        L = int(rng.choice(length_pool)) if len(length_pool) else 1
        s = int(rng.choice(sess_ids))
        a0, a1 = int(data.day_start_idx[s]), int(data.day_end_idx[s])
        if a1 - a0 < 1:
            continue
        e = int(rng.integers(a0 + 1, a1 + 1))     # entry fills at the open of bar e (a decision at e-1's close)
        x = min(e + L - 1, a1)
        if busy[e:x + 1].any() or not np.isfinite(bp["beta"][e - 1]):
            continue
        busy[e:x + 1] = True
        used += x - e + 1
        trades.append((e - 1, e, x, 1 if rng.random() < p_long else -1))
    trades.sort()
    rows, equity = [], starting_equity
    oA, cA, oB, cB, adjA, adjB = data.open, data.close, data.b_open, data.b_close, data.price_adj, data.b_price_adj
    for k, e, x, d in trades:
        beta = float(bp["beta"][k])
        qa, qb = size_pair(equity, (oA[e] - adjA[e]) * la.mult, (oB[e] - adjB[e]) * lb.mult, beta, com)
        if qa < 1:
            continue
        a_in, b_in = _slip(oA[e], d > 0, tk, la), _slip(oB[e], d < 0, tk, lb)
        a_out, b_out = _slip(cA[x], d < 0, tk, la), _slip(cB[x], d > 0, tk, lb)
        pnl = d * qa * la.mult * (a_out - a_in) - d * qb * lb.mult * (b_out - b_in) - 2 * com * (qa + qb)
        rows.append((k, e, x, d, qa, qb, beta, a_in, a_out, b_in, b_out, com * (qa + qb), pnl, equity))
        equity += pnl
    c = list(zip(*rows)) if rows else [()] * 14
    f, i = (lambda v: np.asarray(v, dtype=float)), (lambda v: np.asarray(v, dtype=np.int64))
    z = np.zeros(len(rows))
    return SimResult(trades=[], equity_curve=[], signal_idx=i(c[0]), entry_idx=i(c[1]), exit_idx=i(c[2]),
                     decision_idx=i(c[2]), side=i(c[3]), qa=i(c[4]), qb=i(c[5]), beta=f(c[6]),
                     month=np.zeros(len(rows), np.int64), a_entry=f(c[7]), a_exit=f(c[8]), b_entry=f(c[9]),
                     b_exit=f(c[10]), a_entry_base=f(c[7]), b_entry_base=f(c[9]), entry_commission=f(c[11]),
                     roll_cost=z, n_rolls=np.zeros(len(rows), np.int64), hold_limit=np.full(len(rows), -1),
                     realized_pnl=f(c[12]), forced_close=np.zeros(len(rows), bool),
                     exit_reason=np.array(["eod_exit"] * len(rows), dtype=object), quantity=np.ones(len(rows)),
                     entry_px=z, exit_px=z, equity_before=f(c[13]))


def _notes(pair: str, holdout: bool, prior_access, n_sims: int, n_legs: int, manifest_note: str | None) -> dict:
    a, b = split_pair(pair)
    one = n_legs == 1
    random = (f"{'It is' if one else 'Each is'} compared with {n_sims} random-entry runs at its own time in market: "
              f"random intraday {a}–{b} spread trades on random days and times, never overlapping and closed by the "
              "session's last bar, with lengths drawn from that strategy's own trades, the same share of long-spread "
              "trades and the same month's hedge ratio, paying the same costs on both legs.")
    val = ("<b>Not a clean test.</b> These were picked from the EMRT finalists using their 2023–2024 results "
           "(one of them despite failing the 40-trade validation minimum), so 2023–2024 is in-sample for the choice. "
           "The untouched test is the 2025+ holdout tab.")
    pick = f" {manifest_note}" if manifest_note else ""
    hold = ((f"<b>First EMRT look at the {pair} holdout.</b> No pair strategy had been scored on 2025 onward before "
             "(apart from the final-test of these same frozen picks), and only these, frozen beforehand, were run, so "
             f"there's no selection among holdout results. But single-market strategies were already scored on {a} "
             f"2025+ (and {b} for some families), and the two picks were chosen after seeing validation.{pick}")
            if not prior_access else
            (f"<b>Not a clean test: the {pair} holdout was used {prior_access} time(s) before this run.</b> Treat "
             "these numbers as a check, not independent proof."))
    return {"random": random, "val": val, "holdout": hold, "unseen": "no pair-strategy research had seen"}


@app.command()
def main(
    leg: list[str] = typer.Option(..., help="RUN:ORDER, e.g. emrt_esrty_v2:2 (repeat for each strategy)"),
    manifest: Path = typer.Option(None, help="Holdout: the frozen manifest the final-test used"),
    n_sims: int = typer.Option(200, help="Random-entry runs per luck band"),
    key: str = typer.Option(..., help="File / tab id; must start with emrt_spread"),
    label: str = typer.Option(..., help="Tab label"),
    market_name: str = typer.Option("", help="Default: '<A name> vs <B name>'"),
    holdout: bool = typer.Option(False, "--holdout"),
    confirm_holdout_access: bool = typer.Option(False, "--confirm-holdout-access"),
    runs_root: Path = typer.Option(PROJECT_ROOT / "runs" / "funnel"),
) -> None:
    from scripts.run_emrt_funnel import _frames, _params, _prefit, _select_space, _sha
    from src.experiments.data_access import DEFAULT_LEDGER, authorize_holdout_access, read_ledger
    from src.experiments.funnel_config import load_execution_config, load_funnel_config

    if not key.startswith("emrt_spread"):
        raise typer.BadParameter("key must start with emrt_spread so the EMRT page picks it up")
    specs = []
    for spec in leg:
        run_id, order = spec.split(":")
        rest = run_id.split("_", 1)[1]                     # emrt_esrty_v2 -> esrty_v2
        cfg_path = PROJECT_ROOT / "configs" / "funnel" / f"emrt_funnel_{rest}.yaml"
        fc = load_funnel_config(cfg_path)
        _select_space(fc)
        cands = {c["dev_order"]: c for c in json.loads((runs_root / run_id / "frozen_representatives.json").read_text())["candidates"]}
        c = cands[int(order)]
        specs.append({"run": run_id, "config": cfg_path, "fcfg": fc, "cand": c, "order": c["dev_order"],
                      "params": _params(c["params"]), "tf": c["params"]["timeframe"]})
    fcfg = specs[0]["fcfg"]
    pair = fcfg.symbol
    if any(sp["fcfg"].symbol != pair for sp in specs):
        raise typer.BadParameter("all legs must trade the same pair")
    a_sym, b_sym = split_pair(pair)
    market_name = market_name or f"{NAMES.get(a_sym, a_sym)} vs {NAMES.get(b_sym, b_sym)}"
    tfs = sorted({sp["tf"] for sp in specs}, key=["5min", "15min", "30min", "1h"].index)
    multi_tf = len(tfs) > 1
    for sp in specs:
        sp["name"] = f"{sp['tf'].replace('min', 'm')} #{sp['order']}" if multi_tf else f"#{sp['order']}"
    runs = sorted({sp["run"] for sp in specs})
    ec = load_execution_config(fcfg)

    prior_access, manifest_note = None, None
    if holdout:
        if manifest is None:
            raise typer.BadParameter("--holdout needs --manifest (the frozen manifest the final-test used)")
        sel = json.loads(manifest.read_text())
        manifest_note = sel.get("holdout_selection_note")
        if fcfg.config_sha256() != sel["config_sha256"]:
            raise typer.BadParameter("config changed since the manifest was frozen")
        for run_id in runs:
            fr = runs_root / run_id / "frozen_representatives"
            if _sha(json.loads(fr.with_suffix(".json").read_text())) != fr.with_suffix(".sha256").read_text().split()[0]:
                raise typer.BadParameter(f"{run_id}: frozen_representatives.json changed since it was frozen")
        want = {sp["cand"]["config_id"] for sp in specs}
        if not want <= {c["config_id"] for c in sel["candidates"]}:
            raise typer.BadParameter("every leg must be in the manifest")
        prior_access = sum(e.get("phase") == "holdout" and e.get("symbol") == pair
                           and not (e.get("command") == "final-test" and e.get("experiment_id") in runs)
                           for e in read_ledger(DEFAULT_LEDGER))
        auth = authorize_holdout_access(manifest_sha256=_sha(sel), confirm=confirm_holdout_access,
                                        command="portfolio_holdout")
        frames, info = _frames(fcfg, pair, "holdout", command="portfolio_holdout",
                               experiment_id="+".join(runs), authorization=auth)
        start, end = fcfg.data.holdout.start, date.fromisoformat(info["actual_last_session"])
        key, label = f"{key}_holdout", f"{label} · holdout"
    else:
        frames, info = _frames(fcfg, pair, "validation", command="portfolio", experiment_id="+".join(runs))
        start, end = fcfg.data.development.start, fcfg.data.validation.end
    exp = runs_root / runs[0]
    _prefit(exp, frames, [sp["params"] for sp in specs], n_workers=min(4, len(specs)))
    datas = {tf: PairData(frames[f"{pair}|{tf}"]) for tf in tfs}
    ref = datas[tfs[0]]
    for d in datas.values():
        if not np.array_equal(d.days, ref.days):
            raise typer.BadParameter("bar sizes disagree on the trading days")
    for sp in specs:
        sp["data"] = datas[sp["tf"]]
        sp["bp"] = sp["data"].bar_params(sp["params"].formation, sp["params"].hedge, sp["params"].anchor)
    s64, e64 = np.datetime64(start, "D"), np.datetime64(end, "D")
    dmask = (ref.days >= s64) & (ref.days <= e64)
    days = ref.days[dmask]
    prior = np.flatnonzero(ref.days < s64)
    eq0 = ec.starting_equity
    n_legs = len(specs)
    half = eq0 / n_legs

    dev_end = np.datetime64(fcfg.data.development.end, "D")
    n_dev = int((days <= dev_end).sum())
    periods = {"all": (0, len(days) - 1), "dev": (0, n_dev - 1), "val": (n_dev, len(days) - 1)}
    labels = {"all": f"{start.year}–{end.year}", "dev": f"Development {start.year}–{fcfg.data.development.end.year}",
              "val": f"Validation {fcfg.data.validation.start.year}–{end.year}"}
    if holdout:
        periods, labels = {"holdout": (0, len(days) - 1)}, {"holdout": f"Holdout {start.isoformat()} to {end.isoformat()}"}

    def same_days(d):  # bars of another timeframe -> reference session days (identical sets checked above)
        return d

    pbar = {k: (ref.session_date >= days[a]) & (ref.session_date <= days[b]) for k, (a, b) in periods.items()}

    def daily(sim, data, equity):
        eq = pair_daily_equity(sim, data, equity)
        e0 = float(eq[prior[-1]]) if len(prior) else equity
        return np.concatenate([[e0], eq[dmask]])

    def on_ref(occ, d):
        if d is ref:
            return occ
        j = np.searchsorted(d.bar_open, ref.bar_open, side="right") - 1
        ok = (j >= 0) & (d.session_date[np.clip(j, 0, None)] == ref.session_date)
        return ok & occ[np.clip(j, 0, None)]

    def pstats(eq, pairs, k):
        a, b = periods[k]
        lo_d, hi_d = days[a], days[b]
        pnl, n_c = [], 0
        for sm, d in pairs:
            ent = d.session_date[sm.entry_idx] if len(sm.entry_idx) else np.array([], dtype="datetime64[D]")
            t = (ent >= lo_d) & (ent <= hi_d)
            pnl.append(sm.realized_pnl[t]); n_c += int((~sm.forced_close[t]).sum())
        occ = np.logical_or.reduce([on_ref(_occupancy(sm, d.n), d) for sm, d in pairs]) & pbar[k]
        return _stats(eq[a:b + 2], np.concatenate(pnl), n_c, occ.sum() / pbar[k].sum())

    def block(name, eq, pairs, rand_runs, extra=None):
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
                "band": _band(seg), "pct_sharpe": float(np.mean(sh < (st["sharpe"] if st["sharpe"] is not None else -np.inf))),
                "pct_return": float(np.mean(rt < st["net_return"])),
                "mean_stats": {m: float(np.mean([x[m] for x in rs if x[m] is not None])) if any(x[m] is not None for x in rs) else None
                               for m in ("net_return", "cagr", "sharpe", "max_drawdown", "n_completed_trades",
                                         "win_rate", "profit_factor", "exposure")}}}
        out = {"name": name, "equity": np.round(eq / eq[0], 6).tolist(), "periods": per, "years": _years(days, eq),
               "random_years_mean": {y: float(np.mean([yy[y] for yy in r_years])) for y in r_years[0]}}
        return {**out, **(extra or {})}

    def rand(sp, exposure, equity, rng):
        sim = random_pair_trades(sp["data"], sp["bp"], pair, exec_config=ec, starting_equity=equity, start=start,
                                 end=end, exposure=exposure, length_pool=sp["pool"], p_long=sp["p_long"], rng=rng)
        return sim, daily(sim, sp["data"], equity)

    legs = []
    for sp in specs:
        d = sp["data"]
        sim = simulate_emrt_spread(d, sp["params"], exec_config=ec, starting_equity=eq0)
        eq = daily(sim, d, eq0)
        win = (d.session_date >= s64) & (d.session_date <= e64)
        exposure = float((_occupancy(sim, d.n) & win).sum() / win.sum())
        inwin = (d.session_date[sim.entry_idx] >= s64) & (d.session_date[sim.entry_idx] <= e64)
        sp["pool"] = (sim.exit_idx[inwin] - sim.entry_idx[inwin] + 1).astype(np.int64)
        sp["p_long"] = float(np.mean(sim.side[inwin] > 0)) if inwin.any() else 0.5
        rng = np.random.default_rng([fcfg.seed, sp["order"]])
        rr = []
        for _ in range(n_sims):
            r_sim, r_eq = rand(sp, exposure, eq0, rng)
            rr.append(([(r_sim, d)], r_eq))
        s_sim = simulate_emrt_spread(d, sp["params"], exec_config=ec, starting_equity=half)
        sp.update(sim=sim, eq=eq, sleeve_sim=s_sim, sleeve_eq=daily(s_sim, d, half), exposure=exposure)
        legs.append(block(sp["name"], eq, [(sim, d)], rr,
                          {"order": sp["order"], "run_id": sp["run"], "config_id": sp["cand"]["config_id"],
                           "settings": sp["cand"]["params"],
                           "settings_text": _settings_text(sp["cand"]["params"], a_sym, b_sym),
                           "random": {"median_trade_bars": float(np.median(sp["pool"])) if len(sp["pool"]) else None,
                                      "p_long": sp["p_long"]}}))
        for k in periods:
            P = legs[-1]["periods"][k]
            typer.echo(f"{sp['name']} {k}: return {P['stats']['net_return']:+.2%}, Sharpe {P['stats']['sharpe']:.2f}, "
                       f"{P['stats']['n_completed_trades']} trades, beats {P['luck']['pct_sharpe']:.0%} of random on Sharpe")

    # Together: equal split of the account (each strategy trades its own 1/n).
    ceq = np.sum([sp["sleeve_eq"] for sp in specs], axis=0)
    rng = np.random.default_rng([fcfg.seed, 999])
    rr = []
    for _ in range(n_sims):
        parts = [rand(sp, sp["exposure"], half, rng) for sp in specs]
        rr.append(([(sm, sp["data"]) for (sm, _), sp in zip(parts, specs)], np.sum([q for _, q in parts], axis=0)))
    sizing = {"per_trade": 1 / n_legs, "cap": 1.0, "periods": {}}
    for k, (a, b) in periods.items():
        legs_sz = []
        for sp in specs:
            ent = sp["data"].session_date[sp["sleeve_sim"].entry_idx]
            t = (ent >= days[a]) & (ent <= days[b])
            legs_sz.append({"order": sp["order"], "name": sp["name"], "signals": int(t.sum()), "full": int(t.sum()),
                            "trimmed": 0, "skipped": 0,
                            "mean_contracts": float((sp["sleeve_sim"].qa[t] + sp["sleeve_sim"].qb[t]).mean()) if t.any() else None})
        sizing["periods"][k] = {"legs": legs_sz,
                                "sleeves": pstats(ceq, [(sp["sleeve_sim"], sp["data"]) for sp in specs], k)}
    rets = np.array([np.diff(sp["eq"]) / sp["eq"][:-1] for sp in specs])
    months = days.astype("datetime64[M]")

    def corr(x, y):
        return float(np.corrcoef(x, y)[0, 1]) if len(x) > 2 and x.std() > 0 and y.std() > 0 else None

    occs = [on_ref(_occupancy(sp["sim"], sp["data"].n), sp["data"]) for sp in specs]
    cor = {}
    for k, (a, b) in periods.items():
        if n_legs < 2:
            cor[k] = None
            continue
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
    win_ = 63
    roll = [None] * len(days)
    for t in range(win_ - 1, len(days)) if n_legs > 1 else ():
        roll[t] = corr(rets[0, t - win_ + 1:t + 1], rets[1, t - win_ + 1:t + 1])
    combined = block(" + ".join(sp["name"] for sp in specs), ceq, [(sp["sleeve_sim"], sp["data"]) for sp in specs], rr,
                     {"sizing": sizing, "sleeves_equity": np.round(ceq / ceq[0], 6).tolist(), "correlation": cor,
                      "rolling_corr": {"window": win_, "values": [None if v is None else round(v, 3) for v in roll]}})
    for k in periods:
        P = combined["periods"][k]
        typer.echo(f"together {k}: return {P['stats']['net_return']:+.2%}, Sharpe {P['stats']['sharpe']:.2f}, "
                   f"beats {P['luck']['pct_sharpe']:.0%}" + (f"; corr {cor[k]['daily']:.2f}" if cor[k] and cor[k]['daily'] is not None else ""))

    # Holding leg A alone (rolled, unlevered), for scale.
    e_idx = ref.day_end_idx[dmask]
    first = np.flatnonzero(dmask)[0]
    prev = ref.day_end_idx[first - 1] if first > 0 else e_idx[0]
    idx = np.concatenate([[prev], e_idx])
    adj, raw = ref.close[idx], ref.close[idx] - ref.price_adj[idx]
    heq = np.concatenate([[1.0], np.cumprod(1 + np.diff(adj) / raw[:-1])])
    hold = {"name": f"Holding {a_sym}", "equity": np.round(heq, 5).tolist(), "years": _years(days, heq),
            "periods": {k: {"stats": _stats(heq[a:b + 2] * eq0, np.array([]), 0, 1.0)} for k, (a, b) in periods.items()}}

    out = {
        "kind": "portfolio", "market": pair, "market_name": market_name,
        "strategy_key": key, "strategy_name": label, "run_id": " + ".join(runs),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "period": [str(start), str(end)], "validation_start": str(fcfg.data.validation.start),
        "holdout": holdout, "prior_holdout_accesses": prior_access,
        "timeframe": " / ".join(tfs), "starting_equity": eq0, "n_sims": n_sims, "hold_bars": None,
        "notes": _notes(pair, holdout, prior_access, n_sims, n_legs, manifest_note),
        "config_change_accepted": None,
        "days": [str(d) for d in days], "periods": {k: {"range": list(v), "label": labels[k]} for k, v in periods.items()},
        "legs": legs, "combined": combined, "hold": hold,
        "data_access": info,
        "source": " · ".join([f"{PROJECT_ROOT.name}/runs/funnel/{r}/" for r in runs]
                             + sorted({sp["config"].relative_to(PROJECT_ROOT).as_posix() for sp in specs})
                             + ["scripts/build_emrt_portfolio.py"]),
    }
    path = SITE_ROOT / "data" / pair / f"{key}.json"
    path.write_text(json.dumps(out))
    typer.echo(f"wrote {path}")


if __name__ == "__main__":
    app()
