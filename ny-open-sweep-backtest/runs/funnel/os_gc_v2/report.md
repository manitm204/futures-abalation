# Screening funnel -- os_gc_v2 (development stages only)

- Code: `46ee6e771bde` (dirty working tree: True, diff sha256 `9d872acade0d`)
- Config: `configs/funnel/os_funnel_gc_v2.yaml` sha256 `694a06b21bd13a8d`; seed 20261125
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'GC': '2026-10-16'}
- Frozen manifest sha256: `59a79802f834be51` (14 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- GC 2023-2024 was read on 2026-11-25 when the 210 NQ open-sweep survivors were run unchanged on GC, and this grid is centred on the settings that did well there. Mean-reversion, BB/KC squeeze, NR-N and convexity GC funnels were also selected on it. Validation is therefore NOT an independent test for this run.
- Holdout 2025+ previously inspected: **True** -- No open-sweep metrics have been computed on GC 2025+. GC mean-reversion v6 (#17 + #15) and BB/KC squeeze v4 #6 were scored there, so the researcher has seen how that period treated intraday GC strategies.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 648 | 648 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 648 | 648 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 648 | 192 | 456 | 0 |  | 0 | 29.63 | 29.63 |  |
| 3 performance & risk | hard_gate | 192 | 14 | 178 | 0 |  | 0 | 2.16 | 7.29 |  |
| 4 parameter stability | hard_gate | 14 | 14 | 0 | 0 |  | 0 | 2.16 | 100.00 |  |
| 5 time stability | hard_gate | 14 | 14 | 0 | 0 |  | 6 | 2.16 | 100.00 |  |
| 6 deduplication | dedup | 14 | 14 |  |  | 0 |  | 2.16 | 100.00 | best 2 per cluster |
| 7 execution stress | hard_gate | 14 | 14 | 0 | 0 |  | 0 | 2.16 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 14 |  |  |  |  |  |  |  | diagnostic only: unverified: 14 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 456 |
| s2:hard_reject:years_with_>=10_trades | 264 |
| s3:hard_reject:net_return | 89 |
| s3:hard_reject:sharpe | 178 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop/target exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | transfer dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_a8d6` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.25, target=1R, exit=11:00 | 10/0/31/59 | 100 | 4.8% | 0.9% | 1.08 | -1.0% | 343 | 1.72 | 0.5% | 51.0 | 7/7 | 1.00 | 0.91 | 0.17 | 4 | 3.2% | 0.33 | 0.40 | 4.3% | 3.8% | 2.8% | 4.4%/3.6% | 5.4 (interpolated) | pass | 0.320 (unverified) | n/a |
| 2 | `cfg_34b2` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.25, target=none, exit=11:00 | 57/0/43/0 | 100 | 7.1% | 1.3% | 0.94 | -1.2% | 216 | 1.75 | 1.1% | 51.0 | 7/7 | 1.00 | 0.82 | 0.12 | 4 | 4.1% | 0.41 | 0.69 | 6.4% | 5.6% | 6.0% | 6.5%/4.7% | 5.7 (interpolated) | pass | 0.180 (unverified) | n/a |
| 3 | `cfg_16f8` | timeframe=1min, level=onh, side=high, window=60, pen=0.00, confirm=3, mode=cont, stop=d0.25, target=none, exit=16:00 | 0/46/56/0 | 102 | 9.5% | 1.8% | 0.91 | -1.7% | 174 | 1.80 | 4.1% | 52.4 | 5/5 | 1.00 | 0.57 | 0.35 | 4 | 5.9% | 0.36 | 0.73 | 8.2% | 7.5% | 11.1% | 8.3%/6.7% | 6.7 (interpolated) | pass | 0.152 (unverified) | n/a |
| 4 | `cfg_614d` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.15, target=none, exit=11:00 | 43/0/57/0 | 100 | 6.3% | 1.2% | 0.95 | -1.1% | 216 | 1.84 | 0.9% | 51.2 | 7/7 | 1.00 | 0.87 | 0.07 | 5 | 3.0% | 0.52 | 0.76 | 5.7% | 4.9% | 5.9% | 5.6%/4.4% | 5.4 (interpolated) | pass | 0.169 (unverified) | n/a |
| 5 | `cfg_73e3` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.25, target=1R, exit=16:00 | 0/0/38/62 | 100 | 4.3% | 0.8% | 0.91 | -1.1% | 345 | 1.55 | 0.6% | 51.1 | 7/7 | 1.00 | 0.74 | 0.17 | 4 | 2.7% | 0.37 | 0.45 | 3.7% | 3.1% | 2.9% | 3.9%/2.9% | 4.9 (interpolated) | pass | 0.199 (unverified) | n/a |
| 6 | `cfg_065e` | timeframe=1min, level=onh, side=both, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.25, target=none, exit=11:00 | 86/0/60/0 | 146 | 7.2% | 1.4% | 0.85 | -1.8% | 213 | 1.51 | 1.5% | 74.7 | 6/6 | 1.00 | 0.73 | 0.12 | 3 | 3.9% | 0.45 | 0.68 | 6.0% | 4.8% | 5.7% | 6.3%/5.1% | 4.0 (interpolated) | pass | 0.138 (unverified) | n/a |
| 7 | `cfg_b40e` | timeframe=1min, level=onh, side=both, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.15, target=none, exit=11:00 | 63/0/83/0 | 146 | 6.5% | 1.2% | 0.87 | -1.9% | 422 | 1.58 | 1.1% | 74.9 | 6/6 | 1.00 | 0.70 | 0.18 | 3 | 3.7% | 0.42 | 0.74 | 5.3% | 4.3% | 4.8% | 5.9%/4.4% | 3.9 (interpolated) | pass | 0.140 (unverified) | n/a |
| 8 | `cfg_77d9` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.25, target=none, exit=11:00 | 66/0/52/0 | 118 | 7.5% | 1.4% | 0.81 | -1.8% | 395 | 1.64 | 1.4% | 60.7 | 6/6 | 1.00 | 0.68 | 0.13 | 4 | 2.2% | 0.70 | 0.81 | 6.7% | 6.0% | 6.9% | 6.9%/5.2% | 5.5 (interpolated) | pass | 0.086 (unverified) | n/a |
| 9 | `cfg_9694` | timeframe=1min, level=onh, side=high, window=60, pen=0.00, confirm=3, mode=cont, stop=d0.15, target=none, exit=16:00 | 0/34/68/0 | 102 | 8.3% | 1.6% | 0.90 | -1.7% | 285 | 1.90 | 3.0% | 52.1 | 5/5 | 1.00 | 0.63 | 0.27 | 4 | 4.5% | 0.45 | 0.80 | 7.3% | 6.6% | 7.5% | 7.2%/5.4% | 6.2 (interpolated) | pass | 0.129 (unverified) | n/a |
| 10 | `cfg_5763` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.15, target=1R, exit=11:00 | 1/0/37/62 | 100 | 2.5% | 0.5% | 0.91 | -1.1% | 422 | 1.55 | 0.2% | 51.1 | 7/7 | 1.00 | 0.76 | 0.15 | 4 | 1.5% | 0.42 | 0.45 | 2.0% | 1.4% | 1.9% | 2.3%/1.7% | 3.3 (interpolated) | pass | 0.197 (unverified) | n/a |
| 11 | `cfg_11f1` | timeframe=1min, level=onh, side=both, window=60, pen=0.00, confirm=3, mode=cont, stop=d0.25, target=none, exit=16:00 | 0/80/107/0 | 187 | 9.6% | 1.8% | 0.78 | -2.4% | 212 | 1.41 | 7.2% | 97.5 | 5/5 | 1.00 | 0.58 | 0.19 | 4 | 5.5% | 0.42 | 0.73 | 8.1% | 6.6% | 10.5% | 8.6%/6.6% | 4.3 (interpolated) | pass | 0.099 (unverified) | n/a |
| 12 | `cfg_e31d` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.15, target=1R, exit=16:00 | 0/0/38/62 | 100 | 2.4% | 0.5% | 0.87 | -1.2% | 431 | 1.52 | 0.2% | 51.2 | 7/7 | 1.00 | 0.66 | 0.21 | 4 | 1.4% | 0.43 | 0.47 | 1.9% | 1.4% | 1.9% | 2.2%/1.7% | 3.2 (interpolated) | pass | 0.174 (unverified) | n/a |
| 13 | `cfg_03bd` | timeframe=1min, level=onh, side=both, window=60, pen=0.00, confirm=3, mode=cont, stop=d0.15, target=none, exit=16:00 | 0/55/132/0 | 187 | 8.1% | 1.5% | 0.75 | -2.6% | 270 | 1.46 | 5.0% | 95.5 | 5/5 | 0.80 | 0.67 | 0.08 | 4 | 5.0% | 0.38 | 0.82 | 6.8% | 5.4% | 7.5% | 7.6%/5.7% | 3.8 (interpolated) | pass | 0.081 (unverified) | n/a |
| 14 | `cfg_f35b` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.25, target=1R, exit=11:00 | 15/0/41/62 | 118 | 3.7% | 0.7% | 0.75 | -1.3% | 314 | 1.42 | 0.7% | 61.0 | 6/6 | 0.83 | 0.42 | 0.34 | 4 | 1.7% | 0.54 | 0.57 | 3.0% | 2.2% | 1.8% | 3.3%/2.3% | 3.6 (interpolated) | pass | 0.119 (unverified) | n/a |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 1.1% / 2.63 / 14 | -0.5% / -0.63 / 18 | 1.3% / 1.03 / 26 | 1.5% / 1.78 / 23 | 1.2% / 1.40 / 19 |
| 2 | 1.6% / 2.30 / 14 | 0.6% / 0.42 / 18 | 2.9% / 1.43 / 26 | -0.1% / -0.08 / 23 | 2.0% / 1.25 / 19 |
| 3 | 1.9% / 1.34 / 16 | -0.2% / -0.12 / 16 | 3.4% / 1.12 / 22 | 0.8% / 0.55 / 18 | 3.2% / 1.44 / 30 |
| 4 | 1.4% / 1.99 / 14 | 0.3% / 0.21 / 18 | 3.2% / 1.70 / 26 | 0.1% / 0.08 / 23 | 1.2% / 0.88 / 19 |
| 5 | 0.9% / 1.72 / 14 | -0.6% / -0.76 / 18 | 1.0% / 0.75 / 26 | 1.6% / 1.78 / 23 | 1.4% / 1.51 / 19 |
| 6 | 2.6% / 2.66 / 23 | -0.2% / -0.10 / 28 | 1.8% / 0.77 / 35 | -0.3% / -0.19 / 31 | 3.1% / 1.73 / 29 |
| 7 | 2.3% / 2.36 / 23 | -0.6% / -0.50 / 28 | 2.7% / 1.27 / 35 | -0.2% / -0.20 / 31 | 2.3% / 1.49 / 29 |
| 8 | 0.9% / 1.27 / 16 | 0.1% / 0.09 / 26 | 5.2% / 1.70 / 29 | -0.5% / -0.33 / 26 | 1.7% / 1.06 / 21 |
| 9 | 2.1% / 1.48 / 16 | -0.1% / -0.04 / 16 | 2.4% / 0.89 / 22 | 0.1% / 0.11 / 18 | 3.6% / 1.68 / 30 |
| 10 | 0.3% / 0.93 / 14 | -0.4% / -0.95 / 18 | 0.8% / 0.98 / 26 | 0.8% / 1.59 / 23 | 1.0% / 1.95 / 19 |
| 11 | 2.5% / 1.44 / 27 | 1.3% / 0.66 / 39 | 3.9% / 1.15 / 39 | -0.1% / -0.05 / 41 | 1.8% / 0.77 / 41 |
| 12 | 0.3% / 0.93 / 14 | -0.5% / -1.08 / 18 | 0.8% / 0.98 / 26 | 0.8% / 1.59 / 23 | 1.0% / 1.95 / 19 |
| 13 | 2.7% / 1.62 / 27 | -0.6% / -0.35 / 39 | 2.7% / 0.93 / 39 | 0.2% / 0.10 / 41 | 2.9% / 1.31 / 41 |
| 14 | 0.6% / 1.22 / 16 | -0.5% / -0.56 / 26 | 2.0% / 1.37 / 29 | 0.6% / 0.67 / 26 | 1.0% / 1.18 / 21 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_11f1` | 2 | 0.87 | 0.87/0.87 | 0.69/0.69 |
| 1 | `cfg_065e` | 2 | 0.87 | 0.88/0.88 | 0.76/0.76 |
| 2 | `cfg_16f8` | 2 | 0.88 | 0.87/0.87 | 0.74/0.74 |
| 3 | `cfg_34b2` | 2 | 0.87 | 0.87/0.87 | 0.77/0.77 |
| 4 | `cfg_5763` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 5 | `cfg_a8d6` | 2 | 0.96 | 0.97/0.97 | 0.88/0.88 |
| 6 | `cfg_77d9` | 1 | n/a | n/a/n/a | n/a/n/a |
| 7 | `cfg_f35b` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 9.486e-04 over 648 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 126.0, participation ratio 14.4, 95%-variance components 67 (rank bound T = 1291); raw grid 648; raw + known prior 215886
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
