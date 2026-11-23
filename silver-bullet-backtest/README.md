# ICT Silver Bullet Screening Funnel

An equity-index-futures strategy (NQ primary, ES transfer) that tests ICT's most popular setups:
the **Silver Bullet** and the **2022 Model**, with **placebo windows** built into the grid. It
was picked from the research survey (`../reports/ICT strategies to backtest.md`, rank 2). Every
trade lives inside one window of one session; nothing is held overnight.

It uses the same funnel, thresholds, data splits and costs as the other families. It was cloned
from `../ny-open-sweep-backtest/` on 2026-11-22. What is new:
- the base strategy (`src/strategies/silver_bullet/`), long and short, a fast numpy rewrite of the
  causal ICT feature layer (swings, sweeps, FVGs) rather than the slow 2026-08 SPY pilot code
- its grid (`src/experiments/sb_grid.py`)
- its integrity check (`src/experiments/sb_integrity.py`): every setup, fill, stop, target and
  exit is re-derived per config with plain Python loops and must match exactly
- its bars: each session's Globex 1-minute bars from 18:00 the evening before to 16:00 ET
  (`sb_bars`), since the 03:00 window and the swing liquidity pools live overnight

This project has its own configs (`configs/funnel/sb_funnel_*.yaml`), runs and data-access ledger.

**This is a research tool.** Nothing here establishes or implies that any strategy is
profitable. Its purpose is to determine what does and does not survive rigorous, causal,
out-of-sample testing.

## The idea

Stripped of vocabulary, the Silver Bullet is: price sweeps liquidity (trades through a prior
swing high or low and closes back inside), a displacement leg leaves a three-candle fair value
gap, a limit order rests in the gap, the stop goes beyond the gap or the sweep. ICT says it works
in three hours: 03:00-04:00, 10:00-11:00 and 14:00-15:00 ET. The 2022 Model is the same sequence
in the wider killzones. Two independent studies found the hours are not special and only the
sweep requirement adds anything; a placebo-zone study found FVGs no better than random zones. So
the window axis includes two placebo hours with identical rules, and the sweep requirement is a
toggle.

## Rules (v1)

1. **ATR** = 14-bar mean of 1-minute true range, taken at the FVG's first bar (before the
   displacement).
2. **Swings** (length 5) and **sweeps**: a swing low is swept when a later bar trades below it and
   a close back above it comes within 3 bars; confirmed at that close. Highs mirror it.
3. **FVG**: three consecutive 1-minute bars with `high[1] < low[3]` (bullish) or `low[1] > high[3]`
   (bearish), all opening inside one window interval; gap ≥ `fvg_min` × ATR; the middle bar's
   true range ≥ `disp` × ATR. `sweep = yes` needs a same-direction sweep confirmed before bar 1
   opens, within 60 minutes.
4. **Entry**: a limit at the gap's near edge or midpoint, live for 30 bars inside the window;
   fills only when a bar trades 1 tick through it. One trade per session.
5. **Stop**: the gap's far edge or the swept extreme, 2 ticks beyond; never closer than 1 ATR.
   Live from the fill bar, stop first.
6. **Target**: 2R, 3R, the nearest unswept opposing swing (`liq`), or none. Limit, 1-tick
   trade-through, not on the fill bar.
7. **Exit**: otherwise at the close of the window's last bar.
8. **Size**: as many whole contracts as equity covers (unlevered), as in every family.

## v1 grid (1,728 configs per contract)

| Axis | Values |
|---|---|
| `window` | 10-11, 14-15, 03-04 (Silver Bullet), kz (08:30-11:00 + 13:30-16:00, 2022 Model), p11-12, p1230-1330 (placebo) |
| `sweep` | yes, no |
| `fvg_min` | 0, 0.5, 1.0 × ATR |
| `disp` | 1.0, 1.5, 2.0 × ATR |
| `entry` | prox (near edge), ce (midpoint) |
| `stop` | fvg (far edge), struct (swept extreme) |
| `target` | 2R, 3R, liq, none |

The report's 432-cell design was widened to 1,728 (displacement axis, 3R target) at the user's
request before any run. Stage 4 moves one setting at a time: FVG minimum ±0.25 ATR, displacement
±0.25 ATR, R target ±0.5, and the grid-fixed swing length ±1 bar and order life ±10 bars.

## Commands

```bash
# full NQ run (develop -> validate), as its own unit so memory pressure can't kill the terminal
systemd-run --user --unit=sb_nq_v1 --working-directory=$PWD --setenv=PYTHONPATH=. \
    -p StandardOutput=file:$PWD/runs/sb_nq_v1.log -p StandardError=file:$PWD/runs/sb_nq_v1.log \
    runs/funnel/run_sb_nq_v1.sh
# tests
PYTHONPATH=. .venv/bin/python -m pytest tests -q
```

The holdout (2025+) runs only through `final-test --confirm-holdout-access`, and every access is
written to `runs/funnel/data_access_ledger.jsonl`.
