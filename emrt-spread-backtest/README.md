# EMRT Spread Screening Funnel (futures pairs)

A two-leg futures spread trade built on the **empirical mean-reversion time (EMRT)** from Boming
Ning and Kiseop Lee (Purdue Statistics), "Advanced Statistical Arbitrage with Reinforcement
Learning" (arXiv 2403.12180). It was picked from the Purdue research survey
(`../reports/Purdue trading strategy research.md`, Pick 3) after the convexity line
(`../price-path-convexity-backtest/`) was retired.

It uses the same funnel, gates, data splits and per-contract costs as the earlier families. It was
cloned from `../price-path-convexity-backtest/` on 2026-11-18. It is the first family that trades
**two instruments at once**, so the pieces below are new or changed for pairs.

**This is a research tool.** Nothing here establishes or implies that any strategy is
profitable. Its purpose is to determine what does and does not survive rigorous, causal,
out-of-sample testing.

## The idea

For a pair (A, B), the spread is S = a − β·b in notional terms (per $1 of A, short $β of B). The
paper chooses β not by regression but by making the spread **revert as fast as possible**: EMRT
is the average time from each "important extremum" (a swing of at least C × sd on both sides)
back to the spread's mean, and β is the value in 0.20–3.00 that minimises it, subject to a
variance cap. The paper's reinforcement-learning trading layer is not used here; a plain σ band
trades the spread. The controls are the OLS ratio and 1:1 notional. If EMRT doesn't beat them,
the Purdue part adds nothing.

## What changed for pairs

| Piece | Where | What it does |
|---|---|---|
| Pair as the "symbol" | `configs/funnel/emrt_funnel_*.yaml` | `symbol: ES-NQ` (leg A first); the transfer check is another pair |
| Data | `scripts/run_emrt_funnel.py:_frames`, `src/strategies/emrt_spread/backtest.py:pair_frame` | each leg loaded through the phase-gated, ledgered loader, aggregated, inner-joined on bar time |
| Hedge refits | `src/strategies/emrt_spread/hedge.py` | monthly refit on the previous 3/6/12 months only; EMRT via zigzag important extrema |
| Simulator | `src/strategies/emrt_spread/backtest.py` | two legs filled at the next open, costs on both legs, whole contracts with gross notional ≤ equity, optional overnight holding with roll costs |
| Mark-to-market | `pair_daily_equity` | both legs marked at each session close |
| Integrity | `src/experiments/emrt_integrity.py` | z recomputed by an independent route; fills, exits, P&L, roll costs, sizing, fit timing; truncation look-ahead test |
| Execution | `configs/execution/futures_pairs.yaml` | same per-leg costs, $10M starting equity so β is carried by tens of contracts |
| 30-minute bars | `src/data/aggregation.py` | `30min` added |

## Grid (v1, 51,840 configs per pair)

Bar size 15m/30m/1h · formation 3/6/12 months · hedge EMRT at C = 1.5/2.0/2.5, OLS, 1:1 ·
z from the formation window or a rolling 50/100/250 bars · entry ±1.0/1.5/2.0/2.5 σ · exit at
the mean or half-way · stop none/+1.5/+2.5 σ · time stop none/3 × EMRT · both/long/short spread ·
flat at the close or held overnight. See `src/strategies/emrt_spread/config.py`.

## Commands

    PYTHONPATH=. .venv/bin/python scripts/run_emrt_funnel.py develop --experiment-id emrt_esnq_v1 \
        --config configs/funnel/emrt_funnel_esnq_v1.yaml --n-workers 12
    PYTHONPATH=. .venv/bin/python scripts/run_emrt_funnel.py validate --experiment-id emrt_esnq_v1 \
        --config configs/funnel/emrt_funnel_esnq_v1.yaml
    PYTHONPATH=. .venv/bin/python scripts/run_emrt_funnel.py final-test --manifest <selection manifest> \
        --config configs/funnel/emrt_funnel_esnq_v1.yaml --confirm-holdout-access

Run long commands as their own systemd unit (`systemd-run --user ...`; write shell variables in
the command as `$${p}`, because systemd expands `${p}` itself). Export a run to the results site with
`scripts/export_results_json.py --experiment-id <id> --config <yaml>`, then `python ../futures-results/build.py`.

Rounds so far: v1 (`emrt_funnel_esnq_v1.yaml`, 51,840 configs, positions may be held overnight)
and v2 (`emrt_funnel_es{nq,rty}_v2.yaml`, 13,824 configs: legs measured from each day's open,
z by time of day, always flat by the close).

Tests: `tests/unit/test_emrt_spread.py`.
