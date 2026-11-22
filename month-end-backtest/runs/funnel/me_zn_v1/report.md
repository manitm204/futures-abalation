# Screening funnel -- me_zn_v1 (development stages only)

- Code: `d7cd024716c8` (dirty working tree: True, diff sha256 `d5d1bad97e31`)
- Config: `configs/funnel/me_funnel_zn_v1.yaml` sha256 `3fab5b581b7c7cd2`; seed 20261122
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ZN': '2026-10-16', 'ZB': '2026-10-16'}
- Frozen manifest sha256: `45c18f294c2586d9` (2 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No month-end strategy has been scored on ZN 2023-2024, but BB/KC squeeze, NR squeeze, noise-band, mean-reversion and convexity strategies were selected there and the researcher has read those results. Treated as used for selection.
- Holdout 2025+ previously inspected: **False** -- No month-end metrics have been computed on this project's ZN 2025+ data. But the family was chosen partly on a practitioner futures test (ohlcv.io) that runs to Sep 2026 and reports a positive close-to-close month-end effect over the whole span, so the choice of family is not blind to the holdout period.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 972 | 972 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 972 | 972 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 972 | 756 | 216 | 0 |  | 0 | 77.78 | 77.78 |  |
| 3 performance & risk | hard_gate | 756 | 10 | 746 | 0 |  | 0 | 1.03 | 1.32 |  |
| 4 parameter stability | hard_gate | 10 | 10 | 0 | 0 |  | 0 | 1.03 | 100.00 |  |
| 5 time stability | hard_gate | 10 | 10 | 0 | 0 |  | 10 | 1.03 | 100.00 |  |
| 6 deduplication | dedup | 10 | 2 |  |  | 8 |  | 0.21 | 20.00 | best 2 per cluster |
| 7 execution stress | hard_gate | 2 | 2 | 0 | 0 |  | 0 | 0.21 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 2 |  |  |  |  |  |  |  | diagnostic only: unverified: 2 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 216 |
| s3:hard_reject:net_return | 520 |
| s3:hard_reject:sharpe | 746 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ZB dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_f419` | timeframe=1min, window=3, entry=09:00, exit=strike, event_filter=skip_fomc_auction, stop=none | 111/4/0 | 115 | 4.2% | 0.8% | 0.92 | -1.1% | 151 | 1.78 | 6.2% | 42.4 | 7/7 | 1.00 | 0.85 | 0.07 | 5 | 2.6% | 0.39 | 0.66 | 2.6% | 1.0% | 4.4% | 4.0%/3.2% | 2.3 (interpolated) | pass | 0.011 (unverified) | 0.84 |
| 2 | `cfg_e583` | timeframe=1min, window=3, entry=09:00, exit=15:00, event_filter=skip_fomc_auction, stop=none | 111/4/0 | 115 | 3.7% | 0.7% | 0.85 | -0.9% | 300 | 1.68 | 5.9% | 42.4 | 6/6 | 1.00 | 0.79 | 0.06 | 5 | 1.8% | 0.51 | 0.69 | 2.0% | 0.5% | 3.8% | 3.4%/2.7% | 2.2 (interpolated) | pass | 0.009 (unverified) | 0.58 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 0.5% / 0.50 / 25 | 0.9% / 1.42 / 21 | 0.2% / 0.44 / 23 | 1.0% / 1.31 / 23 | 1.6% / 1.15 / 23 |
| 2 | 0.5% / 0.50 / 25 | 0.9% / 1.42 / 21 | 0.2% / 0.44 / 23 | 0.2% / 0.33 / 23 | 1.8% / 1.45 / 23 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_f419` | 10 | 0.86 | 0.88/0.94 | 0.83/0.91 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 2.206e-03 over 972 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 74.0, participation ratio 3.7, 95%-variance components 23 (rank bound T = 1291); raw grid 972; raw + known prior 155724
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
ZB results are unchanged rules on the development period: supporting evidence, not an independent replication.

## Integrity audit

- Bars: 1-minute bars with NY open time in [08:00, 17:00) only (me_day_bars); each NY date is one session, so the session's last bar is the last bar before 17:00 ET and no position can be held overnight.
- Month-end rank per session date: the number of NYSE trading days in its calendar month on or after it (1 = the last). Taken from the NYSE calendar (published in advance), never from later bars; recomputed month by month in the integrity check.
- Eligible day: 1 <= rank <= window, and the event filter allows it (skip_fomc: not a scheduled FOMC statement day; skip_fomc_auction: also no fixed-rate Treasury note/bond auction that day, from configs/calendars/coupon_auctions.csv).
- Entry: LONG at the OPEN of the first bar opening at/after the entry time with market slippage; skipped when that bar opens more than 5 minutes late (a gap in the bars) or is not before the exit.
- Exit at the CLOSE of the last bar opening before the exit target (15:00, 16:00, or the index strike: 15:00 ET on month-ends before 14 Jan 2021, 16:00 ET from then on), with market slippage; when the bars stop earlier (early closes) the trade closes at the session's last bar. Stop (optional) = entry open x (1 - stop%), live intrabar from the entry bar, filled at the worse of the bar's open and the stop with stop slippage.
- One trade per eligible day; long only; sizing is the other families' (as many whole contracts as equity covers at full contract value, unlevered, compounding).
- Development backtests run on data physically truncated at the development end; the final session's trade is closed at the last development bar and flagged forced (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC). Log returns use back-adjusted prices; the adjustment is constant within a session, so 1-minute returns are distorted only by the level shift (tiny for ES).
- Session: each root's day session only (src/data/futures.py SESSIONS), on NYSE trading days; overnight Globex bars are not traded or used in any statistic.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side plus commission per contract per side, from the execution YAML; cost stress scales both. ZN ticks are 1/64 point ($15.625), ZB 1/32 ($31.25).
- Session: 08:00-17:00 ET of each NY date with data (NOT the 08:20-15:00 pit session the src/data/futures.py table gives ZN / ZB), so the post-2021 16:00 ET strike is inside the window. Globex bars before 08:00 and after 17:00 are never loaded into the strategy.

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Every published month-end number (Hartley & Schwarz; the ohlcv.io futures test) is close-to-close and includes the overnight session. This run measures only the 08:00-17:00 ET part; a failure says the day-session share is too small, not that the month-end effect is gone.
- Month-end days come from the NYSE calendar. The index month-end follows the bond market (SIFMA) calendar; the two differ at month-end only when Good Friday is the month's last weekday (Mar 2018, Mar 2024), where this run treats the Thursday as the last day.
- The strike switch date (14 Jan 2021, 15:00 -> 16:00 ET) is taken from the NY Fed's Liberty Street note (Sep 2026); before it the strike and the 15:00 exit coincide.
- Windows of 1-2 days give about 12-24 trades a year; window 1 (about 60 development trades) cannot pass the 100-trade stage-2 gate by design and is kept as an ablation level.
- FOMC days come from a hard-coded list of statement dates (src/strategies/month_end/config.py); auction days from the Treasury Fiscal Data API (auctions_query), fixed-rate notes and bonds including TIPS, FRNs excluded.
- Long only and on a calendar: ZN / ZB rallied in 2018-2020 and sold off in 2021-2022, so the long bias of the market is part of every config's P&L; the placebo benchmark (random non-month-end days, same clock) separates the calendar from that drift.
- Sizing ignores volatility (full equity per trade, as in the other families).
