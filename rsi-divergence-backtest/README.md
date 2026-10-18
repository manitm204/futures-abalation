# Strategy Ablation Backtest Framework

A reusable, extensible research backtesting framework built on a
data / feature / engine / experiment / analysis architecture, designed so new
strategies plug in without touching the data, portfolio, execution, experiment,
or analytics layers.

**This is a research tool.** Nothing here establishes or implies that any
strategy is profitable. Its purpose is to determine what does and does not
survive rigorous, causal, out-of-sample testing.

## Ablation study (primary workflow)

The headline use of this framework is an **ablation study**: take one simple,
legible **base strategy**, enumerate the **full factorial** of a small set of
discrete parameter axes (e.g. breakout confirmation = close / wick / typical
price), backtest **every** variant, and report which settings actually matter —
out-of-sample, after costs.

The shipped base strategy is a **Donchian channel breakout** (intraday, regular
trading hours) in `src/strategies/donchian_breakout/`. Its axes (see
`src/experiments/grid.py`): `timeframe` (15min/1h), `channel_lookback`,
`breakout_price` (close/wick/typical), `trend_filter`, `direction`, `stop`,
`target`, `time_exit` — 1,944 variants/symbol.

Each variant is backtested once over 2018–2026 and scored on three
chronological, non-overlapping splits: **development** (in-sample, 2018–2022),
**validation** (OOS, 2023–2024), and **holdout** (OOS, 2025–2026).

```bash
# 1) Run every variant for SPY + QQQ on 15min + 1h (resumable; ~4 min on 10 cores).
python scripts/run_ablation.py --experiment-id donchian_v1 --n-workers 10

# 2) Build the findings report (leaderboard, per-axis ablation, top-cohort
#    enrichment, dev->OOS rank stability, cross-symbol check, honest verdict).
python scripts/build_ablation_report.py --experiment-id donchian_v1 --min-trades-per-year 100
# -> runs/reports/ablation.md + runs/reports/ablation_summary.json
```

No data download is needed: cleaned 1-minute SPY/QQQ bars live under `data/clean/`
and are aggregated to 15min/1h on the fly (`src/data/aggregation.py`).

The whole study runs in **well under an hour** by design: it uses coarse
timeframes (15min ≈ 6.5k bars/yr, 1h ≈ 1.75k/yr), backtests each variant **once**
and slices the resulting trades into the three splits, and parallelizes across
cores with a spawn-based process pool.

## RSI-divergence screening funnel (this folder)

Same funnel and thresholds as the mean-reversion and channel-breakout studies,
applied to a long-only SPY **RSI divergence** base strategy
(`src/strategies/rsi_divergence/`): a regular bullish divergence between two
consecutive confirmed RSI pivot lows (price lower low, RSI higher low) signals
at the pivot's confirmation close; buy at the next bar's open with a stop at
`stop_atr` x ATR(14) below (1R), a target at `target_r` x R above, and a time exit
after `max_hold` bars. Axes (all lengths in bars; the same values on every
timeframe; 32,768 configs per timeframe, 98,304 total):
`timeframe` (5min/15min/1h), `rsi_lookback` (7/10/14/21), `pivot_left`
(3/5/8/12), `pivot_right` (1/3), `max_pivot_gap` (12/24/48/78), `min_rsi_diff`
(0/3/5/8 RSI points), `stop_atr` (0.75/1/1.5/2), `target_r` (1/1.5/2/3),
`max_hold` (6/12/24/48). Conventions: `ASSUMPTIONS.md` -> "RSI-divergence strategy".

```bash
PYTHONPATH=. python scripts/run_rsi_funnel.py develop --experiment-id rsi_v1 --n-workers 12   # stages 1-7 (+9 diagnostics), 2018-2022 only
PYTHONPATH=. python scripts/run_rsi_funnel.py validate --experiment-id rsi_v1                 # stage 8 on 2023-2024
PYTHONPATH=. python scripts/run_rsi_funnel.py final-test --manifest runs/funnel/rsi_v1/selection_manifest.json --confirm-holdout-access
```

Thresholds: `configs/funnel/rsi_funnel.yaml` (identical gates to `mr_funnel.yaml`).

## Mean-reversion screening funnel (inherited)

Same funnel as the channel-breakout study, applied to a long-only SPY
mean-reversion base strategy (`src/strategies/mean_reversion/`): buy at the next
bar's open when `z = (close - mean) / std` falls to the entry threshold, exit at
the next open once z recovers past the exit threshold or after a maximum
holding period. Axes (75,000 variants, all lengths in bars):
`timeframe` (5min/15min/1h), `mean_type` (SMA/EMA), `mean_lookback`
(5/10/15/20/40), `std_lookback` (10/15/20/40/60), `entry_z` (-1.0 .. -2.0),
`exit_z` (-0.5 .. 0.5), `max_hold` (2/3/5/7/10), `trend_filter`
(none / close above SMA100/150/200).

```bash
python scripts/run_mr_funnel.py develop --experiment-id mr_v1 --n-workers 12   # stages 1-7 (+9 diagnostics), 2018-2022 only
python scripts/run_mr_funnel.py validate --experiment-id mr_v1                 # stage 8 on 2023-2024
python scripts/run_mr_funnel.py final-test --manifest runs/funnel/mr_v1/selection_manifest.json --confirm-holdout-access
```

Thresholds: `configs/funnel/mr_funnel.yaml` (identical to the channel funnel's).

**v2 parameter space** (`configs/funnel/mr_funnel_v2.yaml`, same thresholds,
240,000 variants): `timeframe` (5min/15min/1h), `mean_type`, `mean_lookback`
(8/12/20/32/48; the z-score std uses the same window), `entry_z`, `exit_z`
(-0.25/0/0.25/0.5), `max_holding_bars` (2/4/8/16), `trend_filter`
(none / above SMA100), `entry_confirmation` (none / positive bar return),
`cooldown_bars` (0/1/2/4/8), `stop_atr_multiple` (none/1.0/1.5/2.0/3.0).

```bash
python scripts/run_mr_funnel.py develop --experiment-id mr_v2 --n-workers 12 --config configs/funnel/mr_funnel_v2.yaml
python scripts/run_mr_funnel.py validate --experiment-id mr_v2 --config configs/funnel/mr_funnel_v2.yaml
```

## Status

See `ASSUMPTIONS.md` for verified-vs-assumed FMP API behavior, the Donchian
base-strategy conventions, and other load-bearing assumptions, isolated behind
configuration.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # then fill in FMP_API_KEY
```

## Adding a new strategy

The engine only depends on the `Strategy` protocol in `src/strategies/base.py`:

`required_data()`, `validate_config()`, `compute_features()`,
`generate_signals()`, `create_entry_order()`, `update_trade_state()`,
`create_exit_order()`, `serialize_diagnostics()`.

To add a strategy:

1. Create `src/strategies/<your_strategy>/` with `config.py` (typed config),
   `features.py`, `signals.py`, `exits.py`, `strategy.py` implementing the protocol.
2. Register it in `src/strategies/registry.py`.
3. Add a config YAML under `configs/strategies/`.
4. Write unit tests under `tests/unit/` mirroring the ICT Silver Bullet tests.

No changes to `src/engine/`, `src/data/`, or `src/experiments/` are required —
those layers are strategy-agnostic by design.

## Project layout

See the directory tree in the architecture summary; source lives under `src/`,
one-off orchestration scripts under `scripts/`, tests under `tests/`, and all
generated artifacts (data, run outputs) under `data/` and `runs/` (gitignored).

## Running tests

```bash
pytest
```
