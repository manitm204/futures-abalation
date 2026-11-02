"""Dump frozen strategies' runs for the cross-family ES page (scripts/build_es_combined.py).

Family-neutral: run it from inside EITHER project (mean-reversion-backtest or
noise-band-backtest) with that project's venv and PYTHONPATH=. -- it imports that
project's own `src` / `scripts`:

  python ../noise-band-backtest/scripts/dump_family_runs.py FAMILY RUN PHASE OUT.npz ORDER [ORDER ...]

FAMILY mr | nb, RUN a funnel run id (configs/funnel/<mr|nb>_funnel_<run>.yaml),
PHASE full (development + validation, 2018 .. validation end) | holdout (2025+;
needs the run's frozen selection manifest, goes through authorize_holdout_access and
is ledgered as command `cross_family_holdout`).

Per strategy (full-account solo run, exactly as on its family's portfolio page):
daily equity over the window (first value = the close before it), in-market intervals
(entry bar open .. exit bar end), realized P&L and entry session per trade, and
`--n-sims` random-entry runs at the strategy's own window time in market with that
family's random method and the portfolio page's seed. Also the window's 5-minute bar
opens (shared clock for "in the market") and holding the market.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path

import numpy as np

N_SIMS = 200


def main(fam: str, run_id: str, phase: str, out: str, orders: list[int]) -> None:
    sys.path.insert(0, ".")
    from src.analysis.daily_performance import daily_equity
    from src.data.aggregation import AGG_INTERVAL_MINUTES, aggregate_bars
    from src.experiments.data_access import authorize_holdout_access, load_phase_bars
    from src.experiments.funnel_config import load_execution_config, load_funnel_config

    if fam == "mr":
        from scripts.run_mr_funnel import _params, _select_space, _sha
        from src.experiments.random_entry import simulate_random_entries
        from src.strategies.mean_reversion.backtest import MRData as Data
        from src.strategies.mean_reversion.backtest import simulate_mean_reversion as simulate
    else:
        from scripts.run_nb_funnel import _params, _select_space, _sha
        from src.experiments.nb_random_entry import simulate_random_intraday
        from src.strategies.noise_band.backtest import NBData as Data
        from src.strategies.noise_band.backtest import simulate_noise_band as simulate
    fcfg = load_funnel_config(Path(f"configs/funnel/{fam}_funnel_{run_id.removeprefix(fam + '_')}.yaml"))
    _select_space(fcfg)
    ec = load_execution_config(fcfg)
    exp = Path("runs/funnel") / run_id
    cands = {c["dev_order"]: c for c in json.loads((exp / "frozen_representatives.json").read_text())["candidates"]}
    tag = f"{run_id} (ES cross-family page)"
    if phase == "holdout":
        sel = json.loads((exp / "selection_manifest.json").read_text())
        if fcfg.config_sha256() != sel["config_sha256"]:
            raise SystemExit(f"{run_id}: config changed since the manifest was frozen")
        auth = authorize_holdout_access(manifest_sha256=hashlib.sha256(_sha(sel).encode()).hexdigest(), confirm=True,
                                        command="cross_family_holdout")
        bars, info = load_phase_bars(fcfg, fcfg.symbol, "holdout", command="cross_family_holdout", experiment_id=tag,
                                     authorization=auth)
        start, end = fcfg.data.holdout.start, date.fromisoformat(info["actual_last_session"])
    else:
        bars, info = load_phase_bars(fcfg, fcfg.symbol, "validation", command="cross_family", experiment_id=tag)
        start, end = fcfg.data.development.start, fcfg.data.validation.end
    s64, e64 = np.datetime64(start, "D"), np.datetime64(end, "D")
    eq0 = ec.starting_equity
    datas: dict = {}

    def window_eq(sim, d, equity):
        eq = daily_equity(sim, d, equity)
        dmask = (d.days >= s64) & (d.days <= e64)
        prior = np.flatnonzero(d.days < s64)
        return np.concatenate([[float(eq[prior[-1]]) if len(prior) else equity], eq[dmask]])

    arrays, meta = {}, {}
    for o in orders:
        c = cands[o]
        tf = c["params"]["timeframe"]
        d = datas.setdefault(tf, Data(aggregate_bars(bars, timeframe=tf)))
        sim = simulate(d, _params(c["params"]), exec_config=ec, starting_equity=eq0)
        win = (d.session_date >= s64) & (d.session_date <= e64)
        occ = np.zeros(d.n, dtype=bool)
        for a, b in zip(sim.entry_idx, sim.exit_idx):
            occ[a:b + 1] = True
        exposure = float((occ & win).sum() / win.sum())
        inw = (d.session_date[sim.entry_idx] >= s64) & (d.session_date[sim.entry_idx] <= e64)
        step = np.timedelta64(AGG_INTERVAL_MINUTES[tf], "m")
        rng = np.random.default_rng([fcfg.seed, o])  # the family portfolio page's seed for this strategy
        if fam == "nb":
            pool = (sim.exit_idx[inw] - sim.entry_idx[inw] + 1).astype(np.int64)
            p_long = float(np.mean(sim.side[inw] > 0))
        rand = []
        for _ in range(N_SIMS):
            if fam == "mr":
                rs = simulate_random_entries(d, fcfg.symbol, exec_config=ec, starting_equity=eq0, window_start=start,
                                             window_end=end, exposure=exposure, rng=rng, hold_lo=3, hold_hi=10)
            else:
                rs = simulate_random_intraday(d, fcfg.symbol, exec_config=ec, starting_equity=eq0, window_start=start,
                                              window_end=end, exposure=exposure, length_pool=pool, p_long=p_long, rng=rng)
            rand.append(window_eq(rs, d, eq0))
        k = f"{fam}{o}"
        arrays[f"{k}_eq"] = window_eq(sim, d, eq0)
        arrays[f"{k}_rand"] = np.asarray(rand, dtype=np.float64)
        arrays[f"{k}_iv0"] = d.bar_open[sim.entry_idx[inw]].astype("datetime64[m]")
        arrays[f"{k}_iv1"] = (d.bar_open[sim.exit_idx[inw]] + step).astype("datetime64[m]")
        arrays[f"{k}_pnl"] = sim.realized_pnl[inw]
        arrays[f"{k}_done"] = ~sim.forced_close[inw]
        arrays[f"{k}_entry_day"] = d.session_date[sim.entry_idx[inw]].astype("datetime64[D]")
        meta[k] = {"order": o, "run_id": run_id, "family": fam, "timeframe": tf, "exposure": exposure,
                   "config_id": c["config_id"], "params": c["params"]}
        print(f"{fam} #{o} {tf} {phase}: return {arrays[f'{k}_eq'][-1] / arrays[f'{k}_eq'][0] - 1:+.4f}, "
              f"time in market {exposure:.4f}")
    ref = Data(aggregate_bars(bars, timeframe="5min"))
    rmask = (ref.session_date >= s64) & (ref.session_date <= e64)
    dmask = (ref.days >= s64) & (ref.days <= e64)
    e_idx = ref.day_end_idx[dmask]
    first = int(np.flatnonzero(dmask)[0])
    idx = np.concatenate([[ref.day_end_idx[first - 1] if first > 0 else e_idx[0]], e_idx])
    adj, raw = ref.close[idx], ref.close[idx] - ref.price_adj[idx]
    hold = np.concatenate([[1.0], np.cumprod(1 + np.diff(adj) / raw[:-1])])
    np.savez_compressed(out, days=ref.days[dmask].astype("datetime64[D]"),
                        ref_bars=ref.bar_open[rmask].astype("datetime64[m]"), hold=hold, **arrays,
                        meta=json.dumps({"legs": meta, "phase": phase, "window": [str(start), str(end)],
                                         "starting_equity": eq0, "n_sims": N_SIMS, "data_access": info,
                                         "dev_end": str(fcfg.data.development.end)}))
    print(f"wrote {out}")


if __name__ == "__main__":
    fam_, run_, phase_, out_, *orders_ = sys.argv[1:]
    main(fam_, run_, phase_, out_, [int(x) for x in orders_])
