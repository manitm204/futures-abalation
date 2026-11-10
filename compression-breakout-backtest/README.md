# Volatility-Compression Breakout Screening Funnel

Intraday futures breakouts that only trade **out of a volatility squeeze**. Same funnel,
thresholds, data splits and costs as the mean-reversion study (`../mean-reversion-backtest/`)
and the noise-band study (`../noise-band-backtest/`); only the base strategy
(`src/strategies/compression_breakout/`) and its grid (`src/experiments/cb_grid.py`) differ.

**This is a research tool.** Nothing here establishes or implies that any strategy is
profitable. Its purpose is to determine what does and does not survive rigorous, causal,
out-of-sample testing.

## The idea

Volatility clusters: quiet stretches tend to end in a sharp move, but the quiet itself
says nothing about direction. So the strategy splits the job in two:

- **Compression decides when.** The market has gone unusually quiet.
- **The breakout decides which way.** Trade the side price escapes the compression box on.

The question the ablation answers: are breakouts out of compression better than the plain
breakouts that failed on SPY (Donchian, channel breakout)?

## Rules (v1)

1. **Compression**, decided at each bar close from data through that bar only:
   - `bbkc`: TTM-style squeeze. Bollinger Bands (SMA(L) ± 2 sd) sit inside the Keltner
     Channel (SMA(L) ± `kc_mult` × ATR(L)), i.e. 2·sd(L) < `kc_mult`·ATR(L).
   - `nr`: NR-N. The bar's high−low range is the narrowest of the last N bars (ties count).
2. **Box**: a run is a stretch of consecutive compression bars inside one session (a run
   never continues across the open). The box is the run's high / low.
3. **Setup**: at bar k, the run holding the last compression bar r ≤ k−1 of the session is
   live for `setup_expiry_bars` bars after r, if it is at least `min_squeeze_bars` long.
   The box never includes the decision bar.
4. **Entry**:
   - `close`: a close beyond the box, filled at the next bar's open.
   - `wick`: a stop order resting at the box edge, filled intrabar at the worse of the
     bar's open and the edge (stop slippage). A bar through both edges is not traded.
   The **first breakout of a run consumes it**, traded or not (wrong direction, trend
   filter, too late, already in a position), so one setup is one decision.
5. **Filters**: `direction` long / short / both; `trend_filter` none / EMA(50) (longs
   above, shorts below); `min_box_atr` (a box narrower than this × ATR(14) is not a live
   setup and does not consume its run); no entries in the last 30 minutes of the session.
6. **Exits**: stop at the far side of the box or entry ∓ 1.0 / 2.0 × ATR(14) (ATR known
   before the fill); target at 1R / 2R / 3R / none; everything closed at the session's last
   close. Stop and target are live intrabar; a bar touching both counts as the stop, and
   on a wick entry's own bar only the stop is checked (both conservative).

Long and short, unlevered whole contracts, the same sizing as the other families.
`src/strategies/compression_breakout/backtest.py` has the full execution rules.

## Strategy lines and versions

Each compression type is its own **strategy line** with its own rounds. The lines share
one backtester and the same breakout axes. Versions work as for the other families: a new
round of a line tries new values or one new axis on *that* line only.

| | Squeeze (BB inside KC) | NR-N |
|---|---|---|
| `strategy` key | `compression_breakout_bbkc` | `compression_breakout_nr` |
| Run ids | `cb_bbkc_<market>_v1`, `_v2`, ... | `cb_nr_<market>_v1`, `_v2`, ... |
| Configs | `configs/funnel/cb_bbkc_funnel_<market>_v1.yaml` | `configs/funnel/cb_nr_funnel_<market>_v1.yaml` |
| v1 configs per market | 20,736 | 16,128 |

A further compression type (e.g. bandwidth percentile) would be a third line with its
own v1. Both v1 grids were fixed together, before any result was seen; each line's
YAML lists the other as a sibling trial in `research_history`.

## v1 grids

Compression axes, per line:

| Line | Axis | Values |
|---|---|---|
| squeeze | `squeeze_length` | 10, 20, 30 bars |
| squeeze | `kc_mult` | 1.0, 1.5, 2.0 |
| squeeze | `min_squeeze_bars` | 1, 4 |
| NR | `nr_lookback` | 3, 4, 5, 7, 10, 14, 20 |
| NR | `inside_bar` | off, on (the NR bar must also sit inside the previous bar: Crabel's NR4/ID) |

Shared breakout axes (1,152 combinations):

| Axis | Values |
|---|---|
| `timeframe` | 5min, 15min |
| `entry_type` | close, wick |
| `setup_expiry_bars` | 3, 6 |
| `stop` | box, 1.0 ATR, 2.0 ATR |
| `target_r` | 1.0, 2.0, 3.0, none |
| `direction` | long, short, both |
| `trend_filter` | none, ema50 |
| `min_box_atr` | 0, 0.5 (skip boxes narrower than 0.5 × ATR(14), where costs swamp R) |

Squeeze: 18 × 1,152 = 20,736. NR: 14 × 1,152 = 16,128. Both grids were widened before
any run (the 6,912 / 1,152 drafts were never run) so that a rare setting can show up;
stage 4's local test is what separates a genuinely unusual setting from a lucky island.

Stage 4 (local perturbation) moves one setting at a time: bar counts ×0.8 / ×1.2
(squeeze length and min squeeze bars, or NR-N; setup expiry), Keltner multiple ±0.25
(squeeze only), ATR stop ±0.25, target ±0.5R, minimum box width ±0.25 ATR.

## Running

One funnel YAML per line and market (ES, NQ, YM, RTY, CL, GC, 6E, 6J, ZN). `data` and
`.venv` are symlinks to `../mean-reversion-backtest/`, like the noise-band folder.
Squeeze on ES:

```bash
PYTHONPATH=. .venv/bin/python scripts/run_cb_funnel.py develop  --experiment-id cb_bbkc_es_v1 --config configs/funnel/cb_bbkc_funnel_es_v1.yaml --n-workers 12
PYTHONPATH=. .venv/bin/python scripts/run_cb_funnel.py validate --experiment-id cb_bbkc_es_v1 --config configs/funnel/cb_bbkc_funnel_es_v1.yaml
PYTHONPATH=. .venv/bin/python scripts/run_cb_funnel.py final-test --manifest runs/funnel/cb_bbkc_es_v1/selection_manifest.json \
    --config configs/funnel/cb_bbkc_funnel_es_v1.yaml --confirm-holdout-access
```

`develop` reads 2018–2022 only and freezes the representatives; `validate` scores the
frozen set on 2023–2024; `final-test` touches 2025+ only with explicit confirmation, and
every data access is recorded in `runs/funnel/data_access_ledger.jsonl`. For NR, swap
`bbkc` for `nr` in the experiment id and config path.

## Tests

```bash
PYTHONPATH=. .venv/bin/python -m pytest -q tests
```

`tests/unit/test_compression_breakout.py` covers compression flags and runs, box causality,
every entry and exit rule on scripted bars, the stress knobs, the integrity checks (and
that they catch tampered trades), look-ahead truncation, the grid, lattice, perturbations
and the market configs. The rest is the shared framework suite.
