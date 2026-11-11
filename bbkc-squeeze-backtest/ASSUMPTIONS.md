# Assumptions and verification status

This file tracks every load-bearing assumption in the framework, whether it has
been empirically/documentation-verified, and where it is isolated in configuration.
Per project policy: nothing here is silently assumed inside code — every item below
has a corresponding config knob so it can be corrected without a rewrite.

## FMP API (`configs/data/fmp.yaml`)

| Item | Status | Finding | Config key |
|---|---|---|---|
| Intraday endpoint | **Verified** (live query, 2026-08-19) | `GET https://financialmodelingprep.com/stable/historical-chart/{interval}?symbol=&from=&to=&apikey=` for `1min`/`5min`/`15min`. Daily EOD is a **different path**: `GET /stable/historical-price-eod/full?symbol=&from=&to=&apikey=` | `base_url`, `interval` |
| Intraday response fields | **Verified** | `date, open, high, low, close, volume` only (no vwap/change on intraday) | `RAW_FMP_INTRADAY_SCHEMA` in `src/data/schemas.py` |
| Daily EOD response fields | **Verified** | `symbol, date, open, high, low, close, volume, change, changePercent, vwap` — note: **no separate adjusted-vs-raw field**; see adjustment finding below | to be added to `schemas.py` when daily ingestion is implemented |
| Bar-label convention (open vs close) | **Verified**, live query SPY 2024-01-02 1min | Bars are **open-labeled**. First RTH bar = `09:30:00`, last = `15:59:00`; exactly 390 one-minute bars covering [09:30, 16:00) NY time. Confirms half-open `[bar_open_ts, bar_close_ts)` with `bar_close_ts = bar_open_ts + interval`. | `normalization.bar_label_convention = "open"` |
| Timezone of `date` | **Verified**, consistent with RTH 09:30–16:00 boundaries on the query date | America/New_York **naive wall-clock** string (e.g. `"2024-01-02 09:30:00"`), must be localized via IANA rules (not a fixed offset) — `src/utils/time.localize_ny` is the sanctioned localizer | `normalization.source_timezone = "America/New_York"` |
| Adjustment status (splits) | **Verified**, live query AAPL around its confirmed 2020-08-31 4:1 split (cross-checked against FMP's own `/stable/splits?symbol=AAPL` endpoint, which lists that exact split) | Both **intraday (1min) and daily EOD data are split-adjusted (back-adjusted)** — price series is continuous across the split date with no 4x discontinuity, on both endpoints. **This reverses the earlier "assumed raw" placeholder.** | `normalization.adjustment_status = "split_adjusted"` |
| Max date range per request / pagination (1min) | **Verified and corrected**, live queries including a real download run that exposed the first hypothesis as wrong | The `1min` endpoint hard-caps at the **3 CALENDAR days ending at `to`** (not 3 trading days), filtered to whatever trading days fall in that window — silently ignoring `from` beyond that. A request spanning a weekend/holiday within that 3-calendar-day window silently drops the earlier trading day(s): e.g. `from=2024-01-05&to=2024-01-08` (Fri+Mon, 2 trading days) returned **only Jan 8**, dropping Jan 5, because calendar days Jan 6–8 contain just one trading day. This was caught during an actual sample download (build produced `missing_sessions: 1`), not just synthetic verification. **Downloader now requests exactly one trading day per call** (`MAX_TRADING_DAYS_PER_INTRADAY_REQUEST = 1` in `src/data/fmp_client.py`) — the only chunking granularity confirmed safe in every test performed, including across weekends. This trades request volume for correctness per the project's "accuracy over speed" priority. | `downloader` chunks via `TradingCalendar.chunk_trading_days(..., chunk_size=1)` |
| Historical depth | **Verified**, live query | SPY 1min data is available at least back to 2008-06-16 (spot-checked; likely further). 2018 start date is comfortably covered. | n/a |
| Rate limits | Still unmeasured empirically (no 429 hit yet in ~15 light requests) | Conservative exponential backoff + retry on 429/5xx, configurable requests/sec ceiling, tightened if 429s are observed during the full download | `downloader.rate_limit` |

All of the above were confirmed via direct live API calls on 2026-08-19 using the
user-supplied key (see `scripts/download_data.py` / `src/data/fmp_client.py` for the
production implementation of these confirmed behaviors).

## Data coverage limitation: no extended-hours / pre-market bars (blocks London window)

**Verified, live query, 2026-08-19**: FMP's `stable/historical-chart/1min` endpoint
returns exactly 390 bars for a full SPY trading day (09:30:00–15:59:00 NY), zero
bars before 09:30. Direct check of 2024-01-02 confirms 0 premarket bars. No
extended-hours or premarket query parameter was found in accessible FMP
documentation or examples.

**Consequence**: the **London Silver Bullet window (03:00–04:00 America/New_York)
cannot be populated or tested with this data source** — it falls entirely before
the regular session and no bars exist there. Confirmed directly: labeling real
downloaded SPY bars against all three configured windows produced signals in
`ny_am` and `ny_pm` only; `london` never appears.

**Decision (user-confirmed 2026-08-19)**: proceed with **NY AM and NY PM only**
for this study. The `london` window definition remains in
`src/utils/config_models.py` / `configs/strategies/` for forward compatibility
(e.g. a future data vendor with premarket coverage), but the current experiment,
validation funnel, and final report will explicitly disclose that London coverage
is zero and no London-window claims are made. This must be stated in the final
report's "Data coverage and limitations" section, not silently omitted.

## Observed real data-quality issue: partial-day gaps

**Found during Phase 6 QQQ smoke test (2026-08-19)**: QQQ's 2024-01-26 session
has only **4 of the expected 390 one-minute bars** in FMP's raw response
(09:30-09:33 only, then nothing). This is a genuine gap in FMP's own data, not
a bug in this framework's download/normalization — confirmed by inspecting the
raw JSON chunk file directly.

This exposed a real gap in `src/data/quality.py`: the original implementation
only detected (a) entire sessions missing outright, and (b) gaps between two
present bars. A session that has *some* bars and then simply stops (no later
bar in the same session to reveal a gap against) was invisible to both checks.
Fixed by adding `incomplete_session_dates` to `QualityReport` — compares each
present session's actual bar count against the calendar-derived expected count
(accounting for early closes) and flags any session below a configurable
completeness tolerance (default 99%). Covered by
`tests/unit/test_quality_completeness.py`, using this exact QQQ gap as the
motivating case.

**Consequence for the full study**: expect a small number of similar partial-day
gaps across 2018-2026 for both symbols. These will be surfaced in each symbol's
coverage report rather than silently producing under-counted sessions in
feature/signal generation.

## Performance fix: feature-layer algorithmic complexity (Phase 7)

**Found during Phase 7 experiment-runner smoke test (2026-08-19)**: 30 sampled
configs against 2 months of SPY 1-min data (~16,000 bars) took ~200 seconds.
Profiling (`cProfile`) identified three compounding causes, all fixed:

1. `sweeps.py`'s `detect_sweeps` scanned every eligible liquidity level against
   **every bar for the rest of the dataset** (no availability-cutoff bisect, no
   age limit despite `max_level_age_bars` existing in config but never being
   enforced). O(levels × bars), unbounded. Fixed: bisect to the level's
   availability index, bounded by `max_level_age_bars` (new default: 500 bars,
   configurable/unboundable via `None`), and numpy-vectorized penetration
   candidate filtering instead of a per-bar Python loop.
2. `liquidity.py`'s `prior_session_extremes` called `calendar.session_for()`
   once per session date; each call passed a different single-day range to
   `TradingCalendar.sessions()`, whose cache is keyed by the exact `(start,
   end)` tuple — so every call missed the cache and re-triggered
   `pandas_market_calendars`' expensive holiday/schedule computation. Fixed:
   one batched `calendar.sessions(min_date, max_date)` call, plus replacing an
   O(n²) "find the next session" scan with an O(n) group-by.
3. `market_structure.py`'s `detect_market_structure_shifts` ran a fresh Polars
   `.filter()` + `.sort()` per sweep to find the reference swing, and a linear
   scan from bar 0 to locate each sweep's confirmation bar. Fixed: swings
   pre-sorted and bisected per sweep; confirmation bar located via bisect
   instead of linear scan.

**Combined effect**: the same 30-config/16k-bar benchmark dropped from ~200s
to ~51s (~4x), and per-config feature computation alone dropped from ~8.5s to
~0.9-1.3s (~7-9x) on the profiled single config. All fixes are covered by new
regression tests (`test_level_goes_stale_after_max_level_age_bars`,
`test_max_level_age_bars_none_means_unbounded`, existing liquidity/MSS suites
re-verified for correctness, not just speed).

**Honest scaling caveat for Phase 9**: the full study needs ~786,000 bars per
symbol (8 years × ~252 days × 390 bars), ~49x this benchmark's data volume.
Naive linear extrapolation from the ~1s/config single-config profile suggests
roughly 50-100s/config on the full history; 10,000 configs would then be on
the order of **150-300 hours single-threaded**, or roughly **10-30 hours**
with process-pool parallelism across a typical multi-core machine (untested at
that scale). This is a projection, not a measurement — the actual full-history
runtime has not been benchmarked, and further optimization or a reduced
initial config count may be warranted before committing to the full 10,000-
config run. This must be reviewed before launching Phase 9, per the project's
explicit instruction not to launch an expensive full run without reviewing
expected cost/runtime.

## Full 2018-2026 download and quality results (Phase 9 pilot, 2026-08-19)

Downloaded and cleaned the complete requested history for both symbols:
SPY 842,209 rows, QQQ 841,838 rows, 2018-01-02 through 2026-08-18, **zero
download failures, zero duplicate bars, zero invalid OHLC bars, zero missing
sessions, zero large intraday gaps** for either symbol.

`incomplete_session_dates` correctly surfaced real historical events, not
data-pipeline bugs: **2020-03-09, 03-12, 03-16, and 03-18 show an identical
376-of-390-bar shortfall on both SPY and QQQ** -- these are the NYSE
market-wide circuit-breaker trading-halt days during the March 2020 COVID
crash, a known real-world event, not a gap in FMP's data or this framework's
normalization. Also flagged: 2019-08-12 and 2021-05-05 (SPY only, minor
shortfalls, cause not investigated) and the previously-documented QQQ
2024-01-26 gap. `zero_volume_bar_count` is 163 (SPY) / 454 (QQQ) out of
~842k bars each (<0.06%) -- plausible for genuinely illiquid 1-min bars at
this scale, not investigated further.

## Critical bug: parallel search hung for hours (fork + Polars thread pool deadlock)

**Found running the real 400-config SPY pilot against full 8-year data
(2026-08-20)**: launched with `n_workers=6`, checked back later, and found
**zero configs completed after 4.5 hours** despite worker processes showing as
alive and consuming CPU. This was not "just slow" -- it was a genuine deadlock.

Root cause, confirmed via a minimal isolated repro: `ProcessPoolExecutor`
defaults to the `fork` start method on Linux. Polars maintains a native (Rust)
thread pool that comes alive the moment it's imported/used in the parent
process. `fork()` only duplicates the *calling* thread, not other threads --
a forked worker inherits a half-copied, permanently-deadlocked version of that
thread pool, so **any** Polars operation in the child (even `pl.read_parquet`)
hangs forever waiting on a mutex whose owning thread doesn't exist in the
child. Reproduced directly: a `ProcessPoolExecutor` with a Polars-reading
initializer hung indefinitely under `fork`, and completed instantly once
switched to `mp_context=multiprocessing.get_context("spawn")`.

**Also fixed en route**: the original parallel path passed the full bars
`DataFrame` as a per-task argument to `executor.submit(...)`, which re-pickles
and pipes a full copy of it for *every* task (400 times for this pilot) --
wasteful even before the deadlock is considered. Workers now load the data
**once** via the pool's `initializer` instead.

**Fix location**: `src/experiments/runner.py` -- `run_experiment`'s parallel
branch now uses `spawn` context + a module-level `_WORKER_BARS` populated once
per worker via `_init_worker`. Regression-tested
(`test_parallel_execution_produces_same_results_as_sequential`, which
reproduces the same class of hang at small scale and asserts sequential vs.
parallel execution produce identical config statuses).

**Why this wasn't caught earlier**: every prior parallel-execution test used
tiny synthetic data (5 trading days) and never actually exercised the
multi-worker code path with real timing pressure -- the bug is a genuine
deadlock, not a slowdown, so it doesn't manifest until something is slow
enough (or the process count high enough) to make the race condition bite.
This is a reminder that "tests pass" and "runs correctly at real scale" are
different claims; both matter.

## Known gap: daily-bar bias modes not wired end-to-end

**Found during Phase 7 experiment-runner smoke test (2026-08-19)**: running a
30-config sample against real SPY data, 17/30 configs crashed with
`AttributeError: 'NoneType' object has no attribute 'filter'`. Root cause:
`src/features/bias.py`'s daily-bar-dependent modes (`prior_daily_direction`,
`prior_day_close_vs_open`, `daily_ma20_slope`, `price_vs_daily_ma20`) are
implemented and unit-tested (Phase 4), but no daily OHLC data is actually
downloaded/normalized/passed through anywhere in the data or strategy layers —
`SilverBulletStrategy.generate_signals` always calls `resolve_bias(...,
daily_df=None)`. FMP's daily EOD endpoint (`historical-price-eod/full`) is
wrapped in `downloader.download_daily`, but `normalization.py` only handles
intraday schemas, so there's no path from raw daily JSON to a usable `daily_df`.

**Fixes applied**:
1. `resolve_bias` now returns `None` (→ signal rejected as `bias_unresolvable`)
   for daily-dependent modes when `daily_df is None`, instead of crashing.
   Regression-tested in `tests/unit/test_bias.py`.
2. `DEFAULT_SILVER_BULLET_SPACE.bias_mode` restricted to `("none",)` so the
   search doesn't burn budget on guaranteed-rejection configs.

**Remaining work before bias modes can be sampled**: build daily-bar
normalization (raw EOD JSON → `bar_open_ts`/`bar_close_ts`/OHLCV, this is a
different schema than intraday — no time component, includes `vwap`/`change`)
and wire a `daily_df` into `SilverBulletStrategy.compute_features` /
`generate_signals`. Not done yet; flagging rather than silently shipping a
narrower default.

## Donchian breakout ablation study (base-strategy conventions)

The ablation study's base strategy (`src/strategies/donchian_breakout/`) makes
the following deliberate, documented choices — each is a knob or a stated
limitation, not a silent assumption:

| Item | Status | Convention |
|---|---|---|
| Channel | Explicit | Breakout above the highest high / below the lowest low of the prior `channel_lookback` bars; the **current bar is excluded** from the channel (`.shift(1)` after the rolling window), so detection at bar *t* never uses *t*'s own extreme relative to the channel. |
| Breakout confirmation price | Ablation axis | `close` (bar close), `wick` (bar high/low extreme), or `typical` ((H+L+C)/3) must clear the channel. |
| Entry timing (no look-ahead) | Structural | A breakout confirmed at bar *t*'s close has `submission_ts = t.bar_close_ts`; the engine fills it at the **next** bar's open. Verified in `tests/unit/test_donchian_signals.py`. |
| Intraday-only | Explicit | Every position is closed by the session close in **both** `time_exit` modes — positions are never held across the overnight gap, which RTH-only data (see FMP coverage above) cannot see. Breakouts on the final bar of a session are dropped (no intraday entry possible). |
| `time_exit = max_120min` | Explicit | Caps the hold at 120 minutes = 8 bars (15min) / 2 bars (1h); still bounded by the session close. |
| Chronological splits | Explicit, verified against coverage | development 2018-01→2022-12, validation 2023-01→2024-12, holdout 2025-01→2026-12 (data ends 2026-08). Reuses `validation.DEFAULT_SPLIT`. A trade is attributed to a split by its **entry** timestamp; each split's metrics are computed from a single whole-period backtest (one backtest, three metric sets). |
| Activity gate | Config (`--min-trades-per-year`, default 100) | A variant must trade ≥ N times/year in development to be "eligible"; keeps the study on statistically meaningful variants, per the ~100-trades/year requirement. |

**Finding (donchian_v1, full run 2026-10-12)**: 3,888 variants, 0 failures, 4m12s
on 10 cores. The single dominant axis is `direction` — `long_only` is enriched
×2.26 in the top cohort (median validation Sharpe 0.96 vs −0.12 for `both`);
shorting these indices intraday is the primary performance killer. Even the
best variants degrade sharply on the 2025–2026 holdout, so no robust edge is
claimed — the ablation's value here is precisely in refusing to over-sell a
curve-fit result. See `runs/reports/ablation.md`.

## Strategy conventions

| Item | Status | Assumption |
|---|---|---|
| Silver Bullet windows | Documented per user spec, categorical (not optimized) | London 03:00–04:00, NY AM 10:00–11:00, NY PM 14:00–15:00, America/New_York, half-open `[start, end)` |
| Same-bar stop/target ambiguity | Configurable, documented | Default `stop_first`; trade flagged `intrabar_ambiguous=True` |
| FVG confirmation | Structural, not assumed | A 3-bar FVG cannot exist/be signaled until bar 3 closes |

## Execution defaults

See `configs/execution/default.yaml` for the full conservative default set
(starting equity $100,000; risk 0.25%/trade; commission $0.005/share, $1.00
minimum; 1bp adverse slippage on market/stop fills; no leverage; whole shares
only; one open position per symbol, no pyramiding).

## Channel-breakout screening funnel (configs/funnel/channel_funnel.yaml)

All funnel thresholds live in `configs/funnel/channel_funnel.yaml`; the loaded
config is hashed into every run. Commands are separate and explicit:
`develop` (stages 1-7 + stage-9 diagnostics, development data only),
`validate` (stage 8, frozen manifest), `final-test` (holdout, requires
`--confirm-holdout-access`). Every bar load is appended to
`runs/funnel/data_access_ledger.jsonl`.

**Data history.** Validation (2023-24) and holdout (2025+) are NOT untouched:
funnel_v1..v3 gated on validation and stored holdout metrics for every config,
and the Donchian ablation report discussed holdout degradation. Recorded in
`data_history` and printed in every report.

**Backtester integrity fixes (2026-10-16)** in
`src/strategies/channel_breakout/backtest.py`, verified by a truncation
look-ahead test (`src/experiments/integrity.py`):
1. The initial ATR stop and position size used the *entry* bar's ATR (which
   includes that bar's unseen high/low/close). Now uses the last ATR known
   before the fill.
2. The stop was first checked on the bar after entry. It is now live on the
   entry bar (conservative; intrabar order unknown).
3. A "missed entry" stress re-entered on the next signal bar. It now skips the
   whole breakout episode.
These change results for anything using `run_channel_backtest`
(`run_channel_ablation.py`, earlier funnel runs are not comparable).

**Sharpe.** Earlier funnel Sharpe came from an equity curve with a point only
at trade exits (flat days and open-position swings missing). The funnel now
uses daily session-close mark-to-market returns over every trading day,
`sqrt(252)` annualization, rf = 0 with idle cash earning 0
(`src/analysis/daily_performance.py`).

**Drawdown limit.** -30% reused from
`src/experiments/validation.py::FunnelThresholds.max_dev_drawdown_pct`.
**Approved by the user on 2026-10-16**, together with 0.25% risk per trade.
The approval is recorded here rather than in the funnel YAML so the
funnel_v4_dev frozen manifest's config hash stays valid. Setting it to `null` flags risk
approval as incomplete instead of passing silently.

**DSR.** Diagnostic only and labelled `unverified` until
`confidence.dsr_calibration_verified` is set after review. Trial-Sharpe
variance is measured over the full grid; effective trials estimated from the
correlation eigen-spectrum (Li-Ji primary; participation ratio, raw and
raw+known-prior reported). The ICT search's trial count is unknown.

**Trend-filter-only comparison (2026-10-16, funnel_v4_dev).** Holding SPY
whenever a candidate's own trend filter is on (same bar size, next-bar-open
fills, baseline costs) beat or matched the breakout candidates on Sharpe in
both development and validation; the candidates' alpha over their own filter
was ~0-1%/yr with t < 2 (except the 5min/ema50 candidate, whose filter alone
loses money). The 15min EMA200 filter-only rule switches ~92 times/yr and is
cost-sensitive: development Sharpe 1.00 at baseline costs, 0.81 at 2x, 0.63 at
3x. It is a product of the same search (trend filters were chosen because they
survived), not an independent finding. Details:
`runs/funnel/funnel_v4_dev/trend_rule_comparison.json`.

## Mean-reversion strategy + funnel (this folder, 2026-10-16)

This folder was copied from `channel-breakout-backtest/`. The screening funnel
(stages 1-10, every threshold, DSR, dedup, data-access ledger) is unchanged;
only the base strategy was swapped. Config: `configs/funnel/mr_funnel.yaml`;
runner: `scripts/run_mr_funnel.py`; strategy: `src/strategies/mean_reversion/`;
grid: `src/experiments/mr_grid.py` (75,000 configs = 3 timeframes x 25,000).
The channel-breakout strategy code is still present (`run_channel_ablation.py`
uses it) but the funnel modules now target mean reversion.

| Item | Status | Convention |
|---|---|---|
| Bars / units | User-specified (5min, 15min, 1h) | Every lookback, trend SMA and `max_hold` is a count of bars of the config's timeframe, the same convention as the channel grid. "100-day SMA" in the spec is implemented as a 100-**bar** SMA. |
| z-score | Explicit | `z = (close - mean) / std`; mean = SMA or EMA(adjust=False) of the last N closes, std = rolling sample std (ddof=1) of the last M closes, both including the signal bar. Zero std -> no signal. |
| Entry / exit timing | Structural, verified by truncation test | Signal at bar *i*'s close, fill at bar *i+1*'s open. Exit decided at a close on/after the entry bar (z >= exit_z or `max_hold` bars held), filled at the next open -> a time exit fills exactly `max_hold` bars after entry. |
| Overnight | Explicit | Rolling windows run across sessions (RTH bars only); positions may be held overnight, as in the channel family. |
| Stops / targets | None (per spec) | No stop loss, no profit target. |
| Sizing | Explicit, differs from channel | Risk-based sizing needs a stop distance, so each entry buys as many whole shares as current equity affords (no leverage). The -30% drawdown limit was approved for 0.25%-risk stop sizing and has **not** been re-approved for full-equity sizing. |
| Re-arm after time exit | Explicit design choice | After a time exit, a new entry needs z to close above `entry_z` first, so the holding cap can't be undone by an immediate re-entry. |
| Dividends | Known limitation | Split-adjusted, not dividend-adjusted prices. |
| Data history | Recorded in YAML | No MR config has been selected on validation; the SPY holdout was inspected in earlier studies, so it is not untouched. |

### v2 parameter space (mr_v2, `configs/funnel/mr_funnel_v2.yaml`)

| Item | Convention |
|---|---|
| Std window | No separate axis: the z-score std uses the same window as the mean. |
| `positive_bar_return` | The signal bar's close must be above the previous bar's close. |
| `cooldown_bars = N` | After an exit at bar *x*, the next signal bar must be >= *x + N*. The v1 re-arm rule after time exits is kept. |
| ATR stop | `stop = entry open - k * ATR(14)`, ATR from the bar BEFORE the fill. Live from the entry bar; a touch exits that bar at min(open, stop) minus stop slippage and takes precedence over a z/time exit decided at that close. Signals during ATR warm-up are skipped. |
| Sizing | Unchanged from v1 (full equity, whole shares), so the stop changes exits, not position size. |
| Data history | Validation is marked previously used: mr_v1 gated on it and v2 was designed after reading v1's results. Research history adds mr_v1 (75,000). |
| v1 reproducibility | v1 config hash unchanged; v1 backtests reproduce exactly (sampled regression check). |
