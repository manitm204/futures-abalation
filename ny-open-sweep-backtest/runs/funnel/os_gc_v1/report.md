# Screening funnel -- os_gc_v1 (development stages only)

- Code: `46ee6e771bde` (dirty working tree: True, diff sha256 `a37524e7e045`)
- Config: `configs/funnel/os_funnel_gc_v1.yaml` sha256 `7bddbf8067cf23f0`; seed 20261125
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'GC': '2026-10-16'}
- Frozen manifest sha256: `0a2ab73b95ec52fb` (0 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- GC 2023-2024 was read on 2026-11-25 when the 210 NQ open-sweep survivors were run unchanged on GC, and this grid is centred on the settings that did well there. Mean-reversion, BB/KC squeeze, NR-N and convexity GC funnels were also selected on it. Validation is therefore NOT an independent test for this run.
- Holdout 2025+ previously inspected: **True** -- No open-sweep metrics have been computed on GC 2025+. GC mean-reversion v6 (#17 + #15) and BB/KC squeeze v4 #6 were scored there, so the researcher has seen how that period treated intraday GC strategies.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 648 | 648 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 648 | 648 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 648 | 328 | 320 | 0 |  | 0 | 50.62 | 50.62 |  |
| 3 performance & risk | hard_gate | 328 | 0 | 328 | 0 |  | 0 | 0.00 | 0.00 |  |
| 4 parameter stability | hard_gate | 0 | 0 | 0 | 0 |  | 0 | 0.00 |  |  |
| 5 time stability | hard_gate | 0 | 0 | 0 | 0 |  | 0 | 0.00 |  |  |
| 6 deduplication | dedup | 0 | 0 |  |  | 0 |  | 0.00 |  | best 2 per cluster |
| 7 execution stress | hard_gate | 0 | 0 | 0 | 0 |  | 0 | 0.00 |  |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 0 |  |  |  |  |  |  |  | diagnostic only:  |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 320 |
| s2:hard_reject:years_with_>=10_trades | 128 |
| s3:hard_reject:net_return | 197 |
| s3:hard_reject:sharpe | 328 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop/target exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | transfer dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 5.058e-04 over 648 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 131.0, participation ratio 15.8, 95%-variance components 68 (rank bound T = 1291); raw grid 648; raw + known prior 215238
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
None results are unchanged rules on the development period: supporting evidence, not an independent replication.

## Integrity audit

- Bars: the full Globex 1-minute bars are loaded only to measure the pre-open ranges (os_day_bars); trading uses 1-minute bars with NY open time in [09:30, 16:00) on their own session date. Each NY date is one session and no position can be held overnight.
- Levels per session date D: onh = 18:00 (D-1) to 09:30; asia = 20:00 to 00:00 (D-1 evening); lon = 02:00-05:00; box = 08:00-09:30; each needs bars for >= 50% of its minutes. pdr = the previous RTH session's high/low. Every pre-open level is recomputed from the raw Globex bars with plain loops (check_levels) and must match exactly.
- dATR = mean RTH high-low range of the previous 14 sessions; the 09:30 open must come from a bar opening by 09:32.
- Trigger (high side; the low side mirrors it): only if the 09:30 open is at or below H; p = first bar opening before 09:30 + window with high > H + pen x dATR. fade: first close < H within `confirm` bars from p (p counts, all in the window) -> short; cont: `confirm` consecutive closes > H from p, all in the window -> long. side=both takes the earlier trigger; a same-bar tie trades nothing. Recomputed with plain loops in the per-config integrity check.
- Entry at the OPEN of the bar after the trigger (opening within 2 minutes of it, same session) with market slippage.
- Stop: struct = beyond the extreme of bars p..t by 2 ticks; dX = X x dATR; never closer than 0.03 x dATR; live intrabar from the entry bar, filled at the worse of the bar's open and the stop with stop slippage. Target: R x the stop distance, or the opposite side of the range (fade) / one range height beyond the broken level (cont); a limit filled at the target only when a bar trades 1 tick through it; a bar touching both is a stop. A range target on the wrong side of the entry skips the trade.
- Time exit at the CLOSE of the last bar opening before the exit time with market slippage; a 16:00 exit is the session's last bar.
- One trade per session; sizing is the other families' (as many whole contracts as equity covers at full contract value, unlevered, compounding).
- Development backtests run on data physically truncated at the development end; the final session's trade is closed at the last development bar and flagged forced (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC). Log returns use back-adjusted prices; the adjustment is constant within a session, so 1-minute returns are distorted only by the level shift (tiny for ES).
- Session: each root's day session only (src/data/futures.py SESSIONS), on NYSE trading days; overnight Globex bars are not traded or used in any statistic.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side plus commission per contract per side, from the execution YAML; cost stress scales both. ES ticks are 0.25 point ($12.50), NQ 0.25 point ($5.00).
- Session: trades only 09:30-16:00 ET of each NY date; Globex bars before 09:30 (from 18:00 the evening before) are read only to measure the pre-open ranges. Databento rolls at 00:00 UTC, inside the overnight session; ranges use back-adjusted prices, so they stay comparable across the roll.

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- ICT never published rules; every definition here (level windows, penetration, reclaim, stop and target) is one fixed reading of community sources, chosen before the run (reports/ICT strategies to backtest.md). Each such choice is a hidden trial not counted in the grid.
- Target fills assume a resting limit is filled at the target once a bar trades a tick through it; cost stress scales slippage on market and stop fills only, not on target fills.
- Bars carry no intrabar order: a bar touching both stop and target counts as a stop (stop_first), which understates target-heavy configs.
- Databento ohlcv-1m has no bar for a minute without trades; overnight ranges can be thin on holidays (a level needs >= 50% minute coverage).
- No placebo-level control runs inside the funnel; scripts/run_os_placebo_benchmark.py runs it on the finalists afterwards.
- Sizing ignores volatility and stop distance (full equity per trade, as in the other families).
