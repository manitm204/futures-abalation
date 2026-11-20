# Drift-Burst Fade Screening Funnel

An intraday futures fade built on the **drift burst hypothesis** of Christensen, Oomen & Renò
("The drift burst hypothesis", Journal of Econometrics; [arXiv 2601.08974](https://arxiv.org/abs/2601.08974)).
It was picked from the research survey (`../reports/Distinct futures strategy papers.md`, pick 3)
and runs in the day session only, because the user does not trade overnight.

It uses the same funnel, thresholds, data splits and costs as the mean-reversion, noise-band,
squeeze, convexity and FX-fix studies. It was cloned from `../fx-fix-backtest/` on 2026-11-20.
What is new:
- the base strategy (`src/strategies/drift_burst/`)
- its grid (`src/experiments/db_grid.py`)
- its integrity checks (`src/experiments/db_integrity.py`)
- its bars: the market's day session in 1-minute bars

This project has its own configs (`configs/funnel/db_funnel_*.yaml`), runs and data-access ledger.

**This is a research tool.** Nothing here establishes or implies that any strategy is
profitable. Its purpose is to determine what does and does not survive rigorous, causal,
out-of-sample testing.

## The idea

A drift burst is a short stretch where prices move far faster than local volatility explains.
The paper used tick data on ES, the 10-year note, 6E and CL from 2010/2012 to 2017. It found:
- about one burst a week in ES at a t-stat above 4.5;
- about 71% reverse over the next 5 minutes (regression slope −0.23);
- drops reverse more than spikes (+8.0 bps after −37.4 bps, against −5.4 bps after +36.4 bps);
- bursts on heavy volume for the time of day reverse most (+42.8 bps against +14.3 bps in the
  most-negative quartile).

The paper reports **no trading P&L, no costs and no out-of-sample test**, and it measured
mid-quotes. Across all ordinary 5-minute intervals the reversal is "present, but extremely
weak"; the edge, if any, is only in the extreme tail.

## Rules (v1)

1. **Statistic**, inside one session only. With k = burst window:

       T(t) = (log C_t − log C_{t−k}) / (s · √k)

   where s is the RMS of the 5k one-minute log returns before the burst window. The first 6k
   minutes of a session have no statistic.
2. **Peak**: |T| was above the threshold at bar p and stopped rising at bar p+1. The decision is
   made at p+1's close and fills at the next bar's open, **against** the burst.
3. **Filters**:
   - `side`: both, or long only (buy drops).
   - `vol_gate`: burst-window volume ÷ normal volume for those minutes of the day (mean of the
     prior 20 sessions) must be at least the gate.
   - `news_filter`: skip bursts touching 08:28–08:45 or 09:58–10:15 ET, or Wednesdays
     13:58–15:00 ET.
   - At most one trade per session; a signal while in a position is dropped.
4. **Exit**: after `hold` minutes at that bar's close, or at the session's last close. No stop.
   Nothing is held overnight.

`src/strategies/drift_burst/backtest.py` has the full execution rules.

## v1 grid (576 configs per market)

| Axis | Values |
|---|---|
| `burst_window` k | 3, 5 (paper), 10 min |
| `threshold` | 3.5, 4.0 (paper), 4.5 (paper), 5.0 |
| `vol_gate` | none, 1.5×, 2×, 3× normal |
| `side` | both, long_only |
| `hold` | 5 (paper), 15, 30 min |
| `news_filter` | off, on |

Stage 4 (local perturbation) moves one setting at a time:
- burst window and hold by ±20% (at least one minute)
- threshold by ±0.25
- a volume gate by ±0.25×

The stage-9 transfer symbol for ES is NQ.

## Running

`data` and `.venv` are symlinks to `../mean-reversion-backtest/`. Large runs should go through
`systemd-run --user` (see `runs/funnel/run_db_es_v1.sh`).

```bash
PYTHONPATH=. .venv/bin/python scripts/run_db_funnel.py develop  --experiment-id db_es_v1 --config configs/funnel/db_funnel_es_v1.yaml --n-workers 8
PYTHONPATH=. .venv/bin/python scripts/run_db_funnel.py validate --experiment-id db_es_v1 --config configs/funnel/db_funnel_es_v1.yaml
PYTHONPATH=. .venv/bin/python scripts/run_db_random_benchmark.py --experiment-id db_es_v1 --config configs/funnel/db_funnel_es_v1.yaml
PYTHONPATH=. .venv/bin/python scripts/export_results_json.py --experiment-id db_es_v1 --config configs/funnel/db_funnel_es_v1.yaml
python ../futures-results/build.py        # writes ../futures-results/drift burst/index.html
PYTHONPATH=. .venv/bin/python scripts/run_db_funnel.py final-test --manifest runs/funnel/db_es_v1/selection_manifest.json \
    --config configs/funnel/db_funnel_es_v1.yaml --confirm-holdout-access
```

- `develop` reads 2018–2022 only and freezes the representatives.
- `validate` scores the frozen set on 2023–2024.
- The random benchmark ("luck" test) places random trades of the same lengths at random times
  of the day. It asks whether the burst trigger matters.
- `final-test` touches 2025+ only with explicit confirmation.
- Every data access is recorded in `runs/funnel/data_access_ledger.jsonl`.
- `scripts/build_db_portfolio.py` combines chosen finalists into one account.

For another market, copy `db_funnel_es_v1.yaml` and change `symbol`, `transfer_symbol`,
`data_history` and `research_history`.

## Tests

```bash
PYTHONPATH=. .venv/bin/python -m pytest -q tests
```

`tests/unit/test_drift_burst.py` covers:
- the statistic and the volume norm against independent implementations and a hand calculation
- the day-session bars
- peak detection and the fade side
- the side, volume and news filters
- one trade a day, and time and session-close exits
- the integrity checks, including that they catch tampered trades
- look-ahead truncation
- the stress knobs
- the grid, lattice, local moves and funnel config

The rest is the shared framework suite. The FX-fix family's tests live in `../fx-fix-backtest/`.
