# Treasury Month-End Screening Funnel

A day-session-only ZN / ZB strategy built on the **month-end Treasury effect** from Hartley &
Schwarz, "Predictable End-of-Month Treasury Returns" (Federal Reserve working paper,
[PDF](https://www.kristaschwarz.com/EOM.pdf)). It was picked from the research survey
(`../reports/Futures papers with strong edges.md`, rank 1) and cut down to the day session,
because the user does not trade overnight.

It uses the same funnel, thresholds, data splits and costs as the other families. It was cloned
from `../drift-burst-backtest/` on 2026-11-22. What is new:
- the base strategy (`src/strategies/month_end/`)
- its grid (`src/experiments/me_grid.py`)
- its integrity checks (`src/experiments/me_integrity.py`)
- its bars: 1-minute bars from 08:00 to 17:00 ET
- an FOMC list and a Treasury auction calendar (`configs/calendars/coupon_auctions.csv`)
- a placebo-day luck benchmark (`scripts/run_me_random_benchmark.py`)

This project has its own configs (`configs/funnel/me_funnel_*.yaml`), runs and data-access ledger.
No month-end run has been made yet.

**This is a research tool.** Nothing here establishes or implies that any strategy is
profitable. Its purpose is to determine what does and does not survive rigorous, causal,
out-of-sample testing.

## The idea

Index funds and other holders benchmarked to Treasury indexes buy at each month's index
rebalance (the "strike"), when the index adds newly issued bonds and its duration jumps. In the
paper (1990–2018), coupon Treasuries earn positive, significant returns only over the last few
days of the month, Sharpe about 1. Ten-year futures: 9 / 14 / 17 / 22 bp over the last 1 / 2 / 3 / 5
days; 30-year: 15 / 21 / 27 / 33 bp. A practitioner futures test (2010–Sep 2026) still finds ZN
+5.2 bp a day over the last three days (t 4.1).

**Every one of those numbers is close-to-close and includes the overnight session.** This
project measures only the 08:00–17:00 ET part.

## Rules (v1)

1. **Days.** Each of the last `window` NYSE trading days of the calendar month, each its own
   trade.
2. **Entry.** Long at the open of the first 1-minute bar at or after `entry`, with market
   slippage. The day is skipped if that bar opens more than 5 minutes late.
3. **Exit.** At the close of the last bar opening before the exit time, with market slippage:
   15:00 ET, 16:00 ET, or `strike` (15:00 ET before 14 Jan 2021, 16:00 ET after, when Bloomberg
   moved its Treasury index pricing time). On early-close days the trade closes at the last bar.
   Optional stop 0.25% or 0.50% below the entry price, live intrabar, filled at the worse of the
   bar's open and the stop.
4. **Event filter.** Optionally skip FOMC statement days, or FOMC days and Treasury note/bond
   auction days.
5. **Size.** One position at a time, as many whole contracts as equity covers (unlevered).

## v1 grid (972 configs per contract)

| Axis | Values |
|---|---|
| `window` | last 1, 2, 3, 4, 5, 6 trading days |
| `entry` | 08:20, 09:00, 10:00, 11:00, 12:00, 14:00 ET |
| `exit` | 15:00, 16:00, strike |
| `event_filter` | none, skip_fomc, skip_fomc_auction |
| `stop` | none, 0.25%, 0.50% below the entry |

The grid started at 180 configs and was enlarged to 972 before any run, at the user's request.
Window 1 (~60 development trades) can't pass the 100-trade gate; it stays in as an ablation level.

Stage 4 (local perturbation) moves one setting at a time:
- the entry time by ±30 min
- the exit time by ±15 min
- the window by ±1 day
- a stop by ±0.10%

Stage 9 transfer symbol is ZB, where the paper's month-end effect is larger.

## Running

`data` and `.venv` are symlinks to `../mean-reversion-backtest/`. Large runs should go through
`systemd-run --user` so memory pressure can't take the terminal down; `runs/funnel/run_me_zn_v1.sh`
does develop → validate → placebo → export → page build.

```bash
PYTHONPATH=. .venv/bin/python scripts/run_me_funnel.py develop  --experiment-id me_zn_v1 --config configs/funnel/me_funnel_zn_v1.yaml --n-workers 8
PYTHONPATH=. .venv/bin/python scripts/run_me_funnel.py validate --experiment-id me_zn_v1 --config configs/funnel/me_funnel_zn_v1.yaml
PYTHONPATH=. .venv/bin/python scripts/run_me_random_benchmark.py --experiment-id me_zn_v1 --config configs/funnel/me_funnel_zn_v1.yaml
PYTHONPATH=. .venv/bin/python scripts/export_results_json.py --experiment-id me_zn_v1 --config configs/funnel/me_funnel_zn_v1.yaml
python ../futures-results/build.py        # writes ../futures-results/month end/index.html
PYTHONPATH=. .venv/bin/python scripts/run_me_funnel.py final-test --manifest runs/funnel/me_zn_v1/selection_manifest.json \
    --config configs/funnel/me_funnel_zn_v1.yaml --confirm-holdout-access
```

- `develop` reads 2018–2022 only and freezes the representatives.
- `validate` scores the frozen set on 2023–2024.
- The placebo benchmark ("luck" test) buys at the same clock on random ordinary days (never
  among the month's last 5 trading days). It asks whether the calendar matters.
- `final-test` touches 2025+ only with explicit confirmation.
- Every data access is recorded in `runs/funnel/data_access_ledger.jsonl`.
- `scripts/build_me_portfolio.py` combines chosen finalists into one account.

## Tests

```bash
PYTHONPATH=. .venv/bin/python -m pytest -q tests
```

`tests/unit/test_month_end.py` covers:
- the month-end day count against known dates (holidays, Good Friday month-ends, data ending
  mid-month)
- the strike-time switch
- entries, exits, windows and event filters
- early closes, gaps and non-NYSE days
- the placebo day mask and sizing
- the integrity checks, including that they catch tampered trades
- look-ahead truncation and the stress knobs
- the grid, lattice, local moves and funnel config

The rest is the shared framework suite.
