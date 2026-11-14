# Price-Path Convexity Screening Funnel

An intraday futures fade built on **price-path convexity**, from Huseyin Gulen (Purdue Daniels)
and Michael Woeppel, "Price-Path Convexity and Short-Horizon Return Predictability", JFQA
(accepted 2025). It was picked from the Purdue research survey
(`../reports/Purdue trading strategy research.md`, Pick 1).

It uses the same funnel, thresholds, data splits and costs as the mean-reversion, noise-band and
squeeze studies. It was cloned from `../nr-squeeze-backtest/` on 2026-11-16. Only the base
strategy (`src/strategies/path_convexity/`) and its grid (`src/experiments/pc_grid.py`) are new.
This project has its own configs (`configs/funnel/pc_funnel_*.yaml`), runs and data-access
ledger. No convexity run has been made yet.

**This is a research tool.** Nothing here establishes or implies that any strategy is
profitable. Its purpose is to determine what does and does not survive rigorous, causal,
out-of-sample testing.

## The idea

Convexity measures *when* a move happened inside a window, not how big it was. Over N closes
P1..PN:

    convexity = [ (P1 + PN)/2 − mean(P1..PN) ] / [ (P1 + PN)/2 ]

That is the average gap between the straight line joining the end points and the actual path.
A positive value (convex) means the path sagged below the line: an up-move came late, or a
down-move came early and then flattened. A negative value (concave) is the reverse. The paper
finds that **high convexity predicts lower returns**, because investors over-extrapolate late,
accelerating moves. Two windows with the same net return can give opposite signals, which is
why this is a new conditioning variable for the suite.

The paper's evidence is daily: S&P 500 index 1963–2022, and stock sorts with 5-, 10- and 21-day
look-backs and holds. **Every look-back in this grid is intraday, so the whole grid is untested
extrapolation.** The key question is whether the paper form beats its own control, a plain
N-bar return reversal run with the same exits. If it doesn't, convexity adds nothing here.

## Rules (v1)

1. **Signal**, at each bar close k, from the closes of bars k−N+1..k only:
   - `paper`: the formula above.
   - `atr`: the same average line-minus-path gap, divided by ATR(14).
   - `maxgap`: the largest single line-minus-path gap (signed), divided by ATR(14).
   - `reversal` (**control**): (PN − P1) / ATR(14), the plain N-bar return.
2. **z-score** of the signal over the last `z_lookback` bars (rolling mean and population sd).
3. **Entry**: a *fresh cross* of z ≥ +`entry_z` goes **short**; a fresh cross of z ≤ −`entry_z`
   goes **long**. The order fills at the next bar's open. A high signal always fades.
4. **Filters**, all known at bar k:
   - `quadrant`: `all` trades both cases, as the paper does. `late` only fades the window's net
     move (a convex up-move goes short, a concave down-move goes long). `early` only trades
     with it.
   - `min_move_atr`: requires |PN − P1| ≥ x × ATR(14).
   - `direction`: long, short or both.
   - `trend_filter`: `emaN` takes longs only above EMA(N) and shorts only below it.
   - No entries in the last 30 minutes of the session.
   - A signal that arrives while a position is open is dropped.
5. **Exits**:
   - Time exit after `hold` bars: `half` = ⌈N/2⌉, `full` = N.
   - `session`: hold until the session's last close.
   - Optional stop at ±1.5 or ±2.5 × ATR(14), live intrabar.
   - Everything is flat at the session close.

`src/strategies/path_convexity/backtest.py` has the full execution rules.

## v1 grid (186,624 configs per bar size)

| Axis | Values |
|---|---|
| `lookback` N | 8, 12, 16, 24, 32, 48, 64, 96 bars |
| `signal_form` | paper, atr, maxgap, reversal (control) |
| `z_lookback` | 250, 500 bars |
| `entry_z` | 0.5, 1.0, 1.5, 2.0 |
| `quadrant` | all, late, early |
| `min_move_atr` | 0, 1, 2 |
| `direction` | long, short, both |
| `hold` | half, full, session |
| `stop` | none, 1.5 ATR, 2.5 ATR |
| `trend_filter` | none, ema50, ema200 |

There is one grid per bar size, so v1 is two runs: `path_convexity_v1_15m` and
`path_convexity_v1_5m`.

Stage 4 (local perturbation) moves one setting at a time:
- N and the z look-back by ×0.8 / ×1.2
- entry z by ±0.25
- ATR stop by ±0.25
- minimum net move by ±0.5 ATR

Two known redundancies stay in the full factorial:
- The reversal control is extreme almost only in the direction of its own move. For it,
  `late` ≈ `all` and `early` rarely trades.
- `hold=full` equals `session` once N exceeds the bars left in the session.

## Running

`data` and `.venv` are symlinks to `../mean-reversion-backtest/`. Large runs should go through
`systemd-run --user` so memory pressure can't take the terminal down.

ES on 15-minute bars:

```bash
PYTHONPATH=. .venv/bin/python scripts/run_pc_funnel.py develop  --experiment-id pc_es_v1_15m --config configs/funnel/pc_funnel_es_v1_15m.yaml --n-workers 12
PYTHONPATH=. .venv/bin/python scripts/run_pc_funnel.py validate --experiment-id pc_es_v1_15m --config configs/funnel/pc_funnel_es_v1_15m.yaml
PYTHONPATH=. .venv/bin/python scripts/run_pc_funnel.py final-test --manifest runs/funnel/pc_es_v1_15m/selection_manifest.json \
    --config configs/funnel/pc_funnel_es_v1_15m.yaml --confirm-holdout-access
```

- `develop` reads 2018–2022 only and freezes the representatives.
- `validate` scores the frozen set on 2023–2024.
- `final-test` touches 2025+ only with explicit confirmation.
- Every data access is recorded in `runs/funnel/data_access_ledger.jsonl`.
- For 5-minute bars, use `pc_funnel_es_v1_5m.yaml` and the experiment id `pc_es_v1_5m`.

## Tests

```bash
PYTHONPATH=. .venv/bin/python -m pytest -q tests
```

`tests/unit/test_path_convexity.py` covers:
- the four signal forms against hand calculations and an independent implementation
- causality
- the fresh-cross, quadrant and filter rules
- time, stop and session exits
- the stress knobs
- the integrity checks, including that they catch tampered trades
- look-ahead truncation
- the grid, lattice, local moves and market configs

The rest is the shared framework suite. The squeeze family's tests live in
`../nr-squeeze-backtest/`.
