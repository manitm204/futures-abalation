# NY-Open Liquidity Sweep Screening Funnel

An equity-index-futures strategy (NQ primary, ES transfer) that tests ICT's best-supported idea:
the **liquidity sweep at the New York open** (the Judas swing, the 2025 "Venom" model, the NY-open
reversal). It was picked from the research survey (`../reports/ICT strategies to backtest.md`,
rank 1). It trades only 09:30–16:00 ET and is flat every night.

It uses the same funnel, thresholds, data splits and costs as the other families. It was cloned
from `../last-half-hour-backtest/` on 2026-11-22. What is new:
- the base strategy (`src/strategies/open_sweep/`), long and short
- its grid (`src/experiments/os_grid.py`)
- its integrity checks (`src/experiments/os_integrity.py`), including a plain-loop recomputation
  of every pre-open level from the raw Globex bars
- its bars: the full Globex 1-minute bars are read only to measure the pre-open ranges; trading
  uses the 09:30–16:00 ET bars (`os_day_bars`)

This project has its own configs (`configs/funnel/os_funnel_*.yaml`), runs and data-access ledger.

**This is a research tool.** Nothing here establishes or implies that any strategy is
profitable. Its purpose is to determine what does and does not survive rigorous, causal,
out-of-sample testing.

## The idea

ICT teaches that after 09:30 price runs through an obvious pool of resting stops (the overnight
high or low, yesterday's high or low, the London range, the 08:00–09:30 box) and then reverses.
Independent tests disagree on the direction: a 25k-config ES/NQ Silver Bullet study found that
requiring a sweep was the one rule that added edge, while a walk-forward FX study found swept
levels predicted **continuation** in 65 of 66 folds. So every setting runs in both modes: `fade`
(ICT's reading) and `cont` (the control). If only `cont` survives, the "sweep" framing adds
nothing beyond the NQ open momentum the noise-band family already trades.

## Rules (v1)

1. **Range** `[L, H]` per session, known before 09:30: `onh` overnight 18:00–09:30, `asia`
   20:00–00:00, `lon` 02:00–05:00, `box` 08:00–09:30 (each needs bars for ≥ 50% of its minutes),
   or `pdr` the prior RTH session's high/low.
2. **Penetration.** Within `window` minutes of 09:30, the first bar whose high exceeds
   `H + pen × dATR` (low side mirrors). The 09:30 open must be inside the range on that side.
   dATR = mean RTH range of the previous 14 sessions.
3. **Trigger.** `fade`: the first close back inside within `confirm` bars (the penetration bar
   counts) → trade against the sweep. `cont`: `confirm` consecutive closes beyond the level →
   trade with the break. `side = both` takes whichever side triggers first.
4. **Entry** at the open of the next bar (market, 1 tick slippage).
5. **Stop.** `struct`: beyond the extreme of the sweep / break by 2 ticks; `d0.10`/`d0.20`:
   that many dATR. Never closer than 0.03 × dATR (the cost wall). Live intrabar, stop first.
6. **Target.** none, 1R/2R/3R, or `range` (the far side of the range for fade; one range height
   beyond the broken level for cont). Limit fill only on a 1-tick trade-through.
7. **Time exit** 11:00, 12:30 or 16:00 (the session's last bar). One trade per session.
8. **Size.** As many whole contracts as equity covers (unlevered), as in every family.

## v1 grid (24,300 configs per contract)

| Axis | Values |
|---|---|
| `level` | onh, asia, lon, box, pdr |
| `side` | both, high, low |
| `window` | 15, 30, 60 min after 09:30 |
| `pen` | 0.00, 0.05 × dATR |
| `confirm` | 1, 3, 5 bars |
| `mode` | fade, cont |
| `stop` | struct, d0.10, d0.20 |
| `target` | none, 1R, 2R, 3R, range |
| `exit` | 11:00, 12:30, 16:00 |

The report's 432-cell design was widened to ~25k at the user's request before any run. Stage 4
moves one setting at a time: window ±5 min, exit ±15 min, pen ±0.025 dATR, confirm ±1 bar,
dATR stop ±0.05, R target ±0.5.

## Commands

```bash
# full NQ run (develop -> validate), as its own unit so memory pressure can't kill the terminal
systemd-run --user --unit=os_nq_v1 --working-directory=$PWD --setenv=PYTHONPATH=. \
    -p StandardOutput=file:$PWD/runs/os_nq_v1.log -p StandardError=file:$PWD/runs/os_nq_v1.log \
    runs/funnel/run_os_nq_v1.sh
# tests
PYTHONPATH=. .venv/bin/python -m pytest tests -q
```

The holdout (2025+) runs only through `final-test --confirm-holdout-access`, and every access is
written to `runs/funnel/data_access_ledger.jsonl`.

## Results (v1, NQ)

24,300 → 1,371 pass the profit gate → 580 frozen → **210 pass 2023–2024** (206 continuation, 4 fade).
The ICT fade loses on 2018–2022 (median PF 0.97); continuation is the real effect (median PF 1.07).

Holdout (2025-01-01 .. 2026-10-19) on two picks chosen after validation (`selection_manifest_64_195.json`):

| Pick | Val Sharpe / PF | Holdout return | Sharpe | PF | Max DD |
|---|---|---|---|---|---|
| #64 overnight, both, 15 min, 3-bar cont, 0.1 dATR stop, 16:00 | 1.40 / 1.86 | +4.9% | 0.84 | 1.47 | −2.4% |
| #195 London high, 30 min, 1-bar cont, 0.1 dATR stop, 3R, 16:00 | 1.13 / 1.61 | +0.7% | 0.25 | 1.11 | −1.8% |

#64 unchanged on other markets (`scripts/run_os_transfer_check.py`): positive on ES/YM/RTY in 2018–2022 but
negative on all three in 2023–2024 (Sharpe −1.27 / −0.64 / −0.20) and 0.19 / −0.76 / −0.57 on 2025+. The edge
after 2022 is NQ-only, so #64 is unproven; the family is not tuned further. Pages:
`../futures-results/ny open sweep/index.html` (`scripts/build_os_portfolio.py` builds the pick tabs).
