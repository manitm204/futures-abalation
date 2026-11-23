# FVG After Displacement Screening Funnel

An equity-index-futures strategy (NQ primary, ES transfer) that tests ICT's **fair value gap**
on its own: a displacement leg leaves a three-candle gap, price comes back to it, and (ICT says)
continues. It was picked from the research survey (`../reports/ICT strategies to backtest.md`,
rank 4). Setups are 09:45-15:30 ET and every position is closed by 16:00.

It uses the same funnel, thresholds, data splits and costs as the other families. It was cloned
from `../silver-bullet-backtest/` on 2026-11-23 and reuses its fast gap / ATR features. What is new:
- the base strategy (`src/strategies/fvg/`), long and short, with and against the gap
- its grid (`src/experiments/fv_grid.py`)
- its integrity check (`src/experiments/fv_integrity.py`): every setup, fill, stop, target and
  exit is re-derived per config with plain Python loops and must match exactly

This project has its own configs (`configs/funnel/fv_funnel_*.yaml`), runs and data-access ledger.

**This is a research tool.** Nothing here establishes or implies that any strategy is
profitable. Its purpose is to determine what does and does not survive rigorous, causal,
out-of-sample testing.

## The idea

A placebo-controlled study found real FVGs no better than random zones of the same size, and a
random-walk simulation reproduces the famous 70-80% "fill rates". So every setting runs twice:
`with` the gap (ICT: buy the retrace into a bullish gap with a limit) and `against` it (sell the
same retrace with a stop order). If only noise is there, the two modes lose about the same
(costs); an edge in one mode should show up as the other mode losing more than costs.

## Rules (v1)

1. **ATR** = 14-bar mean of 1-minute true range at the gap's first bar (before the displacement).
2. **Gap**: three consecutive 1-minute bars, all opening inside the window, with
   `high[1] < low[3]` (bullish) or `low[1] > high[3]` (bearish); gap ≥ `fvg_min` × ATR; the middle
   bar's true range ≥ `disp` × ATR. Optional **VWAP gate**: the trade direction must agree with
   bar 3's close vs the session VWAP.
3. **Entry**: `with` = a limit at the gap's near edge or midpoint (1-tick trade-through); `against`
   = a stop order at the same level (a touch, stop slippage); or `mkt` at the next bar's open.
   Orders rest `wait` bars inside the window. One trade per session.
4. **Stop**: beyond the three bars' extreme (2 ticks), or 1.5 / 3.0 ATR; never closer than 1 ATR.
5. **Target**: 1R, 2R, 3R or none (limit, 1-tick trade-through, not on the fill bar).
6. **Exit**: otherwise after `hold` minutes (15 / 30 / 60), and by 16:00.
7. **Size**: as many whole contracts as equity covers (unlevered), as in every family.

## v1 grid (24,192 configs per contract)

| Axis | Values |
|---|---|
| `window` | am 09:45-12:00, pm 12:00-15:30, rth 09:45-15:30 |
| `mode` | with (ICT), against (control) |
| `disp` | 1.0, 1.5, 2.0, 3.0 × ATR |
| `fvg_min` | 0, 0.5 × ATR |
| `vwap` | off, on |
| `entry` × `wait` | prox or ce resting 5 / 15 / 30 bars, or mkt |
| `stop` | struct, a1.5, a3.0 |
| `target` | 1R, 2R, 3R, none |
| `hold` | 15, 30, 60 min |

The report's 216-cell design was widened to 24,192 at the user's request before any run. Stage 4
moves one setting at a time: displacement ±0.25 ATR, gap minimum ±0.25 ATR, wait ±5 bars, ATR stop
±0.5, R target ±0.5, hold ±5 minutes.

## Commands

```bash
# full NQ run (develop -> validate), as its own unit so memory pressure can't kill the terminal
systemd-run --user --unit=fv_nq_v1 --working-directory=$PWD --setenv=PYTHONPATH=. \
    -p StandardOutput=file:$PWD/runs/fv_nq_v1.log -p StandardError=file:$PWD/runs/fv_nq_v1.log \
    runs/funnel/run_fv_nq_v1.sh
# tests
PYTHONPATH=. .venv/bin/python -m pytest tests -q
```

The holdout (2025+) runs only through `final-test --confirm-holdout-access`, and every access is
written to `runs/funnel/data_access_ledger.jsonl`.

## Results (NQ v1, `runs/funnel/fv_nq_v1/`)

No usable edge. 24,192 configs → 23,436 with enough trades → 86 profitable (stage 3) → 83 stable
→ 52 frozen → 5 passed validation (Sharpe 0.33-0.43, PF 1.05-1.07), all with a negative ES dev
Sharpe. Across the grid 23% of `with` configs were profitable (median PF 0.92) against 8.5% of
`against` (median PF 0.84), a gap mostly explained by the stop-order slippage `against` pays.

Random-entry benchmark (`scripts/run_fv_random_benchmark.py`, 500 runs per finalist, same window,
fill kind, stop, target, hold and trade count at random minutes with coin-flip direction): the
median finalist beat 42% of random runs, none reached 90%; the 5 validation passes beat 79-86%.

Holdout (2025-01-01..2026-10-19), #11 only (with, 09:45-12:00, mkt; picked by the user after
validation, `selection_manifest_11.json`): return −2.2%, Sharpe −0.41, PF 0.92, max DD −3.9%,
397 trades (2025 Sharpe −0.07, 2026 −1.03). Fails the stated bar.
