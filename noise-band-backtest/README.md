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

## Noise-band breakout screening funnel (this folder)

Intraday momentum on futures, after Zarattini, Aziz & Barbon (2024), "Beat the
Market: An Effective Intraday Momentum Strategy for S&P500 ETF (SPY)". Same funnel,
thresholds, data splits and costs as the mean-reversion study
(`../mean-reversion-backtest/`); only the base strategy (`src/strategies/noise_band/`)
and its grid (`src/experiments/nb_grid.py`) differ.

**Rules.** Each session's *noise area* is the average absolute move from the open, at
the same time of day, over the previous N sessions. At check times (bar closes a fixed
number of minutes after the open) a close above the upper band goes long and a close
below the lower band goes short, filled at the next bar's open. The position trails out
at a check close back through the band, the session VWAP, or the tighter of the two.
An optional ATR stop is live intrabar, and everything is closed at the session's last
close (nothing is held overnight). Long and short; unlevered whole contracts, the same
sizing as mean reversion.

**v1 grid** (`noise_band`, 8,100 configs per market): `timeframe` (5min/15min),
`band_lookback` (7/10/14/20/30 sessions), `band_mult` (0.75/1/1.25/1.5/2), `check_minutes`
(15/30/60), `first_entry_minutes` (15/30/60 after the open), `anchor` (open / open + prior
close gap adjustment), `trail` (band / vwap / band_vwap), `direction` (long/short/both),
`stop_atr_multiple` (none; stops are supported for later rounds).

One funnel YAML per market: `configs/funnel/nb_funnel_<market>_v1.yaml` (ES, NQ, YM,
RTY, CL, GC, 6E, 6J, ZN). Run ids follow the mean-reversion naming: `nb_<market>_v<n>`.

```bash
PYTHONPATH=. python scripts/run_nb_funnel.py develop  --experiment-id nb_es_v1 --config configs/funnel/nb_funnel_es_v1.yaml --n-workers 12
PYTHONPATH=. python scripts/run_nb_funnel.py validate --experiment-id nb_es_v1 --config configs/funnel/nb_funnel_es_v1.yaml
PYTHONPATH=. python scripts/run_nb_funnel.py final-test --manifest runs/funnel/nb_es_v1/selection_manifest.json \
    --config configs/funnel/nb_funnel_es_v1.yaml --confirm-holdout-access
```

**Later rounds on the same market** (like mean reversion's v5 -> v6 -> v7 15m/1h):
add `NoiseBandV<n>Config` (narrowed `Literal` values) to `src/strategies/noise_band/config.py`,
an `AXES_V<n>` + `nb_grid_v<n>` to `src/experiments/nb_grid.py`, a `LATTICE_NB_V<n>` to
`src/analysis/neighborhood.py`, a `noise_band_v<n>` entry in `SPACES` in
`scripts/run_nb_funnel.py`, and a `configs/funnel/nb_funnel_<market>_v<n>.yaml` that sets
`strategy: noise_band_v<n>`, records what was read beforehand under `data_history`, and
appends the previous round to `research_history`.

`data/` and `.venv/` are symlinks to `../mean-reversion-backtest/` (same Databento
futures bars, same environment). This folder keeps its own data-access ledger at
`runs/funnel/data_access_ledger.jsonl`.

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
