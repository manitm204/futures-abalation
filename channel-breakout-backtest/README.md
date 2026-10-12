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
