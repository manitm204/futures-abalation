# Screening funnel -- sb_nq_v1 (development stages only)

- Code: `41e65188b543` (dirty working tree: True, diff sha256 `e7dc91a3d623`)
- Config: `configs/funnel/sb_funnel_nq_v1.yaml` sha256 `ed48e4a948f05ed2`; seed 20261127
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'NQ': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `68d9fa883f82d7ba` (0 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No Silver Bullet strategy has been scored on NQ 2023-2024, but the noise-band, mean-reversion, squeeze, convexity, EMRT, last-half-hour and NY-open sweep families were selected there and the researcher has read those results.
- Holdout 2025+ previously inspected: **True** -- No Silver Bullet metrics have been computed on NQ 2025+. Noise-band NQ picks, the month-end #7 transfer check, last-half-hour #49/#56 and NY-open sweep #64/#195 were scored there, so the researcher has seen how that period treated intraday NQ strategies.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 1728 | 1728 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 1728 | 1728 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 1728 | 1728 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 3 performance & risk | hard_gate | 1728 | 0 | 1728 | 0 |  | 0 | 0.00 | 0.00 |  |
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
| s3:hard_reject:net_return | 1608 |
| s3:hard_reject:sharpe | 1728 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/stop/target exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
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
- Trial-Sharpe variance (per period): 1.241e-03 over 1728 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 382.0, participation ratio 48.0, 95%-variance components 219 (rank bound T = 1292); raw grid 1728; raw + known prior 339556
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
ES results are unchanged rules on the development period: supporting evidence, not an independent replication.

## Integrity audit

- Bars: each session's Globex 1-minute bars from 18:00 ET the evening before to 16:00 ET (sb_bars; bars from 18:00 carry the next session date). A trade lives inside one window interval of one session.
- ATR = 14-bar simple mean of 1-minute true range (the session's first bar uses high - low); undefined for a session's first 13 bars. All size and displacement tests use the ATR of the FVG's first bar, i.e. before the displacement.
- Swings (length 5): a high strictly above the 5 bars before and at least the 5 after, same session; known from the close of the 5th bar after. A swing's first penetration is the first later bar of the session beyond it. Sweep: a close back inside within 3 bars of the penetration (it counts); extreme = the most extreme price of those bars.
- FVG: three consecutive 1-minute bars of one session (bar 3 opens 2 minutes after bar 1) with high[1] < low[3] (bullish) or low[1] > high[3] (bearish); all three open inside one window interval. Size >= fvg_min x ATR and > 0; the middle bar's true range >= disp x ATR. sweep=yes needs the most recent same-direction sweep confirmed at or before bar m-3 (before bar 1 opens), in the session, within 60 minutes.
- Order: a limit at the gap's near edge or midpoint, live from the bar after bar 3 for at most 30 bars, only on bars inside the interval; filled when a bar trades 1 tick through it, at the better of the limit and the bar's open (no slippage). While it rests later setups are ignored; after an unfilled expiry the next setup may arm. One trade per session.
- Stop: fvg = the gap's far edge -/+ 2 ticks; struct = the setup's sweep extreme -/+ 2 ticks (no qualifying sweep: the extreme of the 10 bars ending with bar 1); at least 1.0 x ATR from the limit; live from the fill bar, stop first, filled at the worse of the bar's open and the stop with stop slippage. A struct reference on the wrong side of the limit skips the setup.
- Target: R x the stop distance from the limit; liq = the nearest swing high (long) / low (short) of the session beyond the limit, confirmed by bar 3 and not penetrated through it (none: skip the setup); a limit filled at the target only when a bar after the fill bar trades 1 tick through it; a bar touching both is a stop. Otherwise out at the CLOSE of the last bar opening inside the interval (market slippage).
- Every setup, fill, stop, target and exit is recomputed per config with plain loops (sb_integrity.independent_plan) and must match the backtester exactly.
- Sizing is the other families' (as many whole contracts as equity covers at full contract value, unlevered, compounding).
- Development backtests run on data physically truncated at the development end; a trade still open at the last development bar is closed there and flagged forced (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC). Log returns use back-adjusted prices; the adjustment is constant within a session, so 1-minute returns are distorted only by the level shift (tiny for ES).
- Session: each root's day session only (src/data/futures.py SESSIONS), on NYSE trading days; overnight Globex bars are not traded or used in any statistic.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side plus commission per contract per side, from the execution YAML; cost stress scales both. ES ticks are 0.25 point ($12.50), NQ 0.25 point ($5.00).
- Session: the 03:00-04:00 window trades overnight Globex bars; the others trade 08:30-16:00 ET. Databento rolls at 00:00 UTC (19:00/20:00 ET), before any window; swings and sweeps use back-adjusted prices, so they stay comparable across the roll.

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- ICT never published rules; every definition here (swing length 5, 3-bar sweep reclaim, 60-minute sweep lookback, displacement as the middle bar's true range, 30-bar order life, the 1-ATR stop floor, window boundaries) is one fixed reading of community sources, chosen before the run (reports/ICT strategies to backtest.md). Each such choice is a hidden trial not counted in the grid; stage 4 nudges the swing length and order life to see how much they matter.
- Entry and target fills assume a resting limit is filled at its price once a bar trades a tick through it; cost stress scales slippage on market and stop fills only, not on limit fills. Queue position is ignored.
- Bars carry no intrabar order: a bar touching both stop and target counts as a stop (stop_first), which understates target-heavy configs.
- Databento ohlcv-1m has no bar for a minute without trades; an FVG needs three bars in three consecutive minutes, so thin overnight minutes (03:00-04:00) form fewer gaps.
- The placebo control is built into the grid: the 11:00-12:00 and 12:30-13:30 windows use identical rules at hours ICT does not name.
- Sizing ignores volatility and stop distance (full equity per trade, as in the other families).
