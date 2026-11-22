# Last-Half-Hour Momentum Screening Funnel

An equity-index-futures strategy (NQ primary, ES transfer) built on **market intraday momentum**
from Baltussen, Da, Lammers & Martens, "Hedging demand and market intraday momentum" (Journal of
Financial Economics 2021, [PDF](https://academicweb.nd.edu/~zda/intramom.pdf)). It was picked from
the research survey (`../reports/Futures papers with strong edges.md`, rank 2). It trades only
the regular session and is flat every night.

It uses the same funnel, thresholds, data splits and costs as the other families. It was cloned
from `../month-end-backtest/` on 2026-11-22. What is new:
- the base strategy (`src/strategies/last_half_hour/`), long and short
- its grid (`src/experiments/lh_grid.py`)
- its integrity checks (`src/experiments/lh_integrity.py`)
- its bars: 1-minute bars from 09:30 to 16:00 ET
- a random-day, coin-flip-direction luck benchmark (`scripts/run_lh_random_benchmark.py`)

This project has its own configs (`configs/funnel/lh_funnel_*.yaml`), runs and data-access ledger.

**This is a research tool.** Nothing here establishes or implies that any strategy is
profitable. Its purpose is to determine what does and does not survive rigorous, causal,
out-of-sample testing.

## The idea

Across 60+ futures (1974–2020) the paper finds the move from the previous close to 30 minutes
before today's close predicts the last half hour. For equity index futures, "long the last half
hour if the day is up, else short" earned 6.86% a year before costs at 3.96% volatility
(Sharpe 1.73). The cause is dealers and leveraged ETFs hedging short gamma in the direction of
the day's move. Post-2013 replications find the unconditional slope near zero in SPY / SPX, but
still positive on days dealers are short gamma. Price bars cannot see dealer gamma, so the grid
tests bar-observable stand-ins (a large move, a high-volatility regime, down days only).

## Rules (v1)

1. **Signal** at the entry time, from the close of the last bar before it:
   - `prev_close`: previous session's last RTH close → now (the paper's rROD)
   - `open`: today's 09:30 open → now (no overnight gap)
   - `first_half`: previous close → 10:00 (Gao et al. 2018)
   - `agree = on`: the signal must have the same sign as the first-half-hour move
2. **Filter.** none; |signal| > 0.5σ or 1σ of the same signal over the previous 20 sessions;
   20-day RV of daily closes above its 120-day median; down days only.
3. **Entry.** At the open of the first 1-minute bar at or after the entry time, long if the
   signal is up and short if down. Skipped if that bar (or the decision bar before it) is more
   than 2 minutes off.
4. **Exit.** At the close of the last bar opening before the exit time; 16:00 = the session's
   last bar (15:59). Optional stop against the entry, live intrabar, filled at the worse of the
   bar's open and the stop. Early-close days have no afternoon bars and are not traded.
5. **Size.** One position at a time, as many whole contracts as equity covers (unlevered).

## v1 grid (500 configs per contract)

| Axis | Values |
|---|---|
| `signal` × `agree` | prev_close / open (agree off or on), first_half → 5 |
| `window` | 15:00–16:00, 15:30–15:50, 15:30–16:00, 15:45–16:00, 15:50–16:00 ET |
| `filter` | none, z0.5, z1.0, rv_high, down_only |
| `stop` | none, 0.10%, 0.20%, 0.40% against the entry |

Stage 4 moves one setting at a time: entry ±5 min, exit ±5 min (never after 16:00), z ±0.25,
stop ±0.05%.

## Commands

```bash
# full NQ run (develop -> validate), as its own unit so memory pressure can't kill the terminal
systemd-run --user --unit=lh_nq_v1 --working-directory=$PWD --setenv=PYTHONPATH=. \
    -p StandardOutput=file:$PWD/runs/lh_nq_v1.log -p StandardError=file:$PWD/runs/lh_nq_v1.log \
    runs/funnel/run_lh_nq_v1.sh
# luck benchmark on the validation finalists, then the dashboard
PYTHONPATH=. .venv/bin/python scripts/run_lh_random_benchmark.py --experiment-id lh_nq_v1 --config configs/funnel/lh_funnel_nq_v1.yaml
PYTHONPATH=. .venv/bin/python scripts/export_results_json.py --experiment-id lh_nq_v1 --config configs/funnel/lh_funnel_nq_v1.yaml
python3 ../futures-results/build.py
# tests
PYTHONPATH=. .venv/bin/python -m pytest tests -q
```

The holdout (2025+) runs only through `final-test --confirm-holdout-access`, and every access is
written to `runs/funnel/data_access_ledger.jsonl`.
