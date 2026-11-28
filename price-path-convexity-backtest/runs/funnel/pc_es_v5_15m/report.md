# Screening funnel -- pc_es_v5_15m (development stages only)

- Code: `acf4e9adf0bf` (dirty working tree: True, diff sha256 `8569fce853d9`)
- Config: `configs/funnel/pc_funnel_es_v5_15m.yaml` sha256 `9cbcc5c8917938ac`; seed 20261126
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'NQ': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `548a83a5581f4d36` (13 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- ES 2023-2024 was used to select v2 picks and by other families; the researcher has read those results. Treated as used for selection.
- Holdout 2025+ previously inspected: **True** -- ES v2 #115 was scored on ES 2025+ (lost). This run does not open the holdout.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 8640 | 8640 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 8640 | 8640 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 8640 | 8538 | 102 | 0 |  | 8553 | 98.82 | 98.82 |  |
| 3 performance & risk | hard_gate | 8538 | 29 | 8509 | 0 |  | 0 | 0.34 | 0.34 |  |
| 4 parameter stability | hard_gate | 29 | 19 | 10 | 0 |  | 0 | 0.22 | 65.52 |  |
| 5 time stability | hard_gate | 19 | 17 | 2 | 0 |  | 19 | 0.20 | 89.47 |  |
| 6 deduplication | dedup | 17 | 13 |  |  | 4 |  | 0.15 | 76.47 | best 2 per cluster |
| 7 execution stress | hard_gate | 13 | 13 | 0 | 0 |  | 0 | 0.15 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 13 |  |  |  |  |  |  |  | diagnostic only: unverified: 13 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 102 |
| s3:hard_reject:max_drawdown | 575 |
| s3:hard_reject:net_return | 7033 |
| s3:hard_reject:sharpe | 8509 |
| s4:hard_reject:local_frac_profitable | 1 |
| s4:hard_reject:local_median_sharpe | 9 |
| s5:hard_reject:profitable_years | 2 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | NQ dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_b684` | timeframe=15min, lookback=26, signal_form=reversal, z_lookback=100, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=long, hold=b8, stop=3.0, trend_filter=none, regime=dtrend50, window=mid | 136/36/17 | 189 | 8.4% | 1.6% | 0.77 | -4.7% | 478 | 1.41 | 4.3% | 85.9 | 7/7 | 0.71 | 0.42 | 0.35 | 4 | 1.7% | 0.79 | 0.52 | 6.5% | 4.9% | 6.1% | 8.1%/6.2% | 3.6 (interpolated) | pass | 0.085 (unverified) | 0.52 |
| 2 | `cfg_a223` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=100, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=3.0, trend_filter=none, regime=none, window=mid | 355/106/27 | 488 | 22.3% | 4.1% | 1.10 | -5.2% | 435 | 1.41 | 11.2% | 225.7 | 6/6 | 0.67 | 0.80 | 0.30 | 4 | 6.4% | 0.67 | 0.44 | 17.5% | 12.4% | 19.7% | 20.5%/16.6% | 3.4 (interpolated) | pass | 0.240 (unverified) | 0.74 |
| 3 | `cfg_e389` | timeframe=15min, lookback=78, signal_form=reversal, z_lookback=100, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=both, hold=b16, stop=2.0, trend_filter=none, regime=dtrend50, window=mid | 56/72/61 | 189 | 23.0% | 4.2% | 0.99 | -3.8% | 295 | 1.62 | 5.9% | 88.3 | 8/8 | 0.50 | 0.18 | 0.81 | 4 | 7.1% | 0.66 | 0.65 | 20.5% | 18.5% | 21.4% | 20.7%/15.6% | 7.4 (interpolated) | pass | 0.187 (unverified) | 0.26 |
| 4 | `cfg_cc58` | timeframe=15min, lookback=78, signal_form=reversal, z_lookback=100, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=both, hold=b16, stop=2.0, trend_filter=none, regime=dtrend50, window=mid | 70/85/77 | 232 | 30.5% | 5.5% | 1.06 | -4.5% | 295 | 1.62 | 7.4% | 108.1 | 8/8 | 0.62 | 0.29 | 0.77 | 4 | 11.4% | 0.58 | 0.61 | 28.9% | 26.0% | 22.1% | 28.4%/20.1% | 8.0 (interpolated) | pass | 0.211 (unverified) | 0.30 |
| 5 | `cfg_85ff` | timeframe=15min, lookback=26, signal_form=reversal, z_lookback=100, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=long, hold=b8, stop=2.0, trend_filter=none, regime=dtrend50, window=mid | 120/32/39 | 191 | 8.8% | 1.7% | 0.81 | -4.0% | 428 | 1.43 | 4.0% | 86.7 | 7/7 | 0.71 | 0.43 | 0.38 | 4 | 2.9% | 0.66 | 0.54 | 6.5% | 5.0% | 7.3% | 8.6%/6.3% | 3.6 (interpolated) | pass | 0.091 (unverified) | 0.28 |
| 6 | `cfg_2afe` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=100, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=3.0, trend_filter=none, regime=volhi, window=mid | 145/39/11 | 195 | 16.3% | 3.1% | 0.80 | -3.6% | 462 | 1.55 | 4.4% | 89.6 | 6/6 | 1.00 | 0.52 | 0.27 | 4 | 3.2% | 0.78 | 0.83 | 14.4% | 12.1% | 8.4% | 14.8%/9.7% | 5.7 (interpolated) | pass | 0.062 (unverified) | 0.25 |
| 7 | `cfg_d9e3` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=3.0, trend_filter=none, regime=none, window=mid | 398/123/35 | 556 | 21.9% | 4.0% | 0.92 | -5.2% | 494 | 1.33 | 12.7% | 257.0 | 6/6 | 1.00 | 0.64 | 0.29 | 3 | 12.3% | 0.44 | 0.46 | 16.7% | 10.7% | 5.8% | 19.1%/15.3% | 3.1 (interpolated) | pass | 0.142 (unverified) | 0.71 |
| 8 | `cfg_be1a` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=long, hold=b16, stop=2.0, trend_filter=none, regime=none, window=mid | 137/380/191 | 708 | 28.4% | 5.1% | 0.83 | -7.8% | 408 | 1.24 | 22.5% | 328.7 | 7/7 | 0.86 | 0.64 | 0.19 | 3 | 7.9% | 0.65 | 0.56 | 22.0% | 14.1% | 13.2% | 26.2%/19.8% | 3.1 (interpolated) | pass | 0.087 (unverified) | 1.00 |
| 9 | `cfg_8aa3` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=2.0, trend_filter=none, regime=none, window=mid | 355/110/93 | 558 | 20.2% | 3.8% | 0.88 | -5.2% | 503 | 1.30 | 12.2% | 256.1 | 6/6 | 1.00 | 0.64 | 0.24 | 3 | 9.8% | 0.52 | 0.50 | 13.7% | 8.5% | 7.5% | 17.5%/12.7% | 2.9 (interpolated) | pass | 0.117 (unverified) | 0.78 |
| 10 | `cfg_abcb` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=both, hold=b8, stop=2.0, trend_filter=none, regime=volhi, window=mid | 292/76/71 | 439 | 20.7% | 3.8% | 0.77 | -7.1% | 573 | 1.25 | 9.6% | 203.7 | 6/6 | 0.67 | 0.32 | 0.45 | 3 | 2.2% | 0.87 | 0.66 | 17.6% | 13.4% | 9.7% | 19.6%/13.2% | 3.6 (interpolated) | pass | 0.070 (unverified) | 0.71 |
| 11 | `cfg_bd2a` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=100, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=2.0, trend_filter=none, regime=none, window=mid | 326/95/68 | 489 | 18.0% | 3.4% | 0.90 | -4.4% | 435 | 1.32 | 10.8% | 226.4 | 6/6 | 0.83 | 0.55 | 0.35 | 3 | 4.8% | 0.69 | 0.53 | 12.2% | 6.8% | 17.0% | 17.2%/12.6% | 3.0 (interpolated) | pass | 0.121 (unverified) | 0.69 |
| 12 | `cfg_94c4` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=both, hold=b8, stop=2.0, trend_filter=none, regime=none, window=mid | 578/175/152 | 905 | 26.8% | 4.9% | 0.80 | -6.8% | 484 | 1.20 | 19.8% | 418.7 | 6/6 | 1.00 | 0.64 | 0.16 | 4 | 9.6% | 0.57 | 0.50 | 18.0% | 8.3% | 16.8% | 22.6%/17.2% | 2.6 (interpolated) | pass | 0.098 (unverified) | 0.85 |
| 13 | `cfg_0e02` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=both, hold=b8, stop=3.0, trend_filter=none, regime=none, window=mid | 652/198/51 | 901 | 28.8% | 5.2% | 0.80 | -6.6% | 481 | 1.20 | 20.6% | 419.1 | 6/6 | 1.00 | 0.48 | 0.31 | 4 | 12.7% | 0.50 | 0.49 | 18.7% | 10.3% | 13.4% | 24.2%/18.3% | 2.6 (interpolated) | pass | 0.097 (unverified) | 0.51 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 0.4% / 0.32 / 26 | 1.6% / 0.92 / 50 | -1.3% / -0.38 / 32 | 6.6% / 2.96 / 58 | 1.0% / 0.63 / 23 |
| 2 | -0.8% / -0.22 / 94 | 0.0% / 0.01 / 102 | 15.0% / 2.93 / 100 | 2.6% / 0.93 / 109 | 4.5% / 0.93 / 83 |
| 3 | 2.8% / 0.67 / 36 | -0.9% / -0.40 / 36 | 14.8% / 1.98 / 39 | 4.5% / 1.77 / 39 | 0.6% / 0.20 / 39 |
| 4 | 4.2% / 0.88 / 42 | -1.0% / -0.40 / 43 | 17.2% / 1.87 / 51 | 5.6% / 2.00 / 48 | 2.2% / 0.51 / 48 |
| 5 | 0.3% / 0.23 / 27 | 1.7% / 0.98 / 50 | -0.2% / -0.06 / 33 | 5.7% / 2.45 / 58 | 1.1% / 0.75 / 23 |
| 6 | -1.9% / -0.77 / 36 | 2.4% / 1.05 / 44 | 12.7% / 1.89 / 39 | 2.6% / 1.09 / 41 | 0.2% / 0.06 / 35 |
| 7 | -0.7% / -0.13 / 114 | -0.3% / -0.09 / 111 | 9.4% / 1.56 / 121 | 3.7% / 1.27 / 121 | 8.5% / 1.58 / 89 |
| 8 | 2.7% / 0.41 / 141 | -4.8% / -1.45 / 142 | 19.0% / 2.14 / 149 | -1.6% / -0.42 / 152 | 12.1% / 1.64 / 124 |
| 9 | -1.3% / -0.28 / 114 | -2.2% / -0.85 / 111 | 10.6% / 1.85 / 121 | 2.9% / 1.01 / 123 | 9.5% / 1.80 / 89 |
| 10 | 0.1% / 0.05 / 80 | -1.2% / -0.46 / 81 | 18.1% / 2.16 / 87 | -1.0% / -0.35 / 93 | 4.4% / 0.75 / 98 |
| 11 | -0.4% / -0.11 / 95 | -1.1% / -0.50 / 102 | 12.7% / 2.38 / 100 | 1.4% / 0.54 / 109 | 4.9% / 1.04 / 83 |
| 12 | 1.7% / 0.31 / 184 | -3.6% / -1.08 / 174 | 15.7% / 1.63 / 190 | 0.3% / 0.10 / 181 | 11.5% / 1.67 / 176 |
| 13 | 3.1% / 0.53 / 183 | -1.9% / -0.54 / 174 | 14.3% / 1.36 / 189 | 0.1% / 0.05 / 179 | 11.3% / 1.52 / 176 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_94c4` | 2 | 0.97 | 0.97/0.97 | 0.95/0.95 |
| 1 | `cfg_2afe` | 3 | 0.84 | 0.30/0.38 | 0.21/0.23 |
| 2 | `cfg_b684` | 2 | 0.95 | 0.96/0.96 | 0.93/0.93 |
| 3 | `cfg_d9e3` | 2 | 0.95 | 0.97/0.97 | 0.96/0.96 |
| 4 | `cfg_a223` | 2 | 0.95 | 0.95/0.95 | 0.96/0.96 |
| 5 | `cfg_be1a` | 1 | n/a | n/a/n/a | n/a/n/a |
| 6 | `cfg_e389` | 5 | 0.86 | 0.83/0.89 | 0.70/0.80 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 7.392e-04 over 8640 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 860.0, participation ratio 47.8, 95%-variance components 306 (rank bound T = 1259); raw grid 8640; raw + known prior 1743444
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
NQ results are unchanged rules on the development period: supporting evidence, not an independent replication.

## Integrity audit

- Signal at bar k from the closes of bars k-N+1..k only (N = lookback, over the RTH bar series across sessions): paper = (midpoint - mean) / midpoint, midpoint = (P1 + PN) / 2 (Gulen & Woeppel's convexity); atr = (midpoint - mean) / ATR(14)[k]; maxgap = the signed line-minus-path gap of largest magnitude / ATR(14)[k]; reversal (control) = (PN - P1) / ATR(14)[k].
- z_k = (S_k - mean(S over the last z_lookback bars, k included)) / population sd of the same; NaN during warm-up.
- Decision at bar k's close: short on a fresh cross z_k >= entry_z (z_{k-1} was not), long on a fresh cross z_k <= -entry_z. A HIGH signal always fades to SHORT. A signal while a position is open is dropped, never queued.
- Filters known at bar k: quadrant late = only against the window's net move PN - P1, early = only with it; |PN - P1| >= min_move_atr x ATR(14)[k]; direction; emaN needs close_k > EMA(N)_k for a long, < for a short; no decision on the session's last bar or less than 30 minutes before its last close.
- Entry fills at the NEXT bar's open with market slippage; the fill bar must be in the decision's session.
- Stop (optional) = open -/+ stop x ATR(14) of the bar before the fill, live intrabar from the entry bar, filled at the worse of the bar's open and the stop with stop slippage. Hold half = ceil(N/2) bars, full = N bars: closed at the close of bar entry + H - 1; session = the session's last close. Every position still open on the session's last bar is closed at that bar's CLOSE; nothing is held overnight.
- Long and short: P&L = side x (exit fill - entry fill) x quantity - commissions; sizing is the mean-reversion funnel's (as many whole contracts as equity covers at full contract value, unlevered, compounding).
- Development backtests run on data physically truncated at the development end; the final session's trade is closed at the last development bar and flagged forced (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC; the 1-minute step there is taken as the roll spread). Point moves are preserved; pre-roll price levels are not real traded prices.
- Session: each root's day session only (src/data/futures.py SESSIONS), on NYSE trading days; overnight Globex bars are not traded or used in indicators.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side (stops too) plus commission per contract per side, from the execution YAML; cost stress scales both.
- Every position is flat by the session close, so no trade straddles a roll. The atr / maxgap / reversal signals are point distances and unaffected by back-adjustment; the paper form divides by a back-adjusted price level, so its scale drifts slightly with the cumulative roll adjustment (the rolling z-score absorbs most of it).

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- The paper tested convexity on DAILY closes with 5- to 21-day holds; every look-back here is intraday, so this whole grid is untested extrapolation of the paper.
- Windows (N up to 96 bars) and the z-score history (250 / 500 bars) run across sessions over RTH bars, so the overnight gap enters the path: a window spanning the open sees the gap as a jump between two adjacent closes.
- The paper form divides by a price level; on a contract whose back-adjusted price nears zero (e.g. CL in April 2020) it is undefined or explodes. The atr form is the same gap without that problem.
- The reversal control has no convex/concave split: its z is extreme almost only in the direction of the net move, so its quadrant=late configs nearly duplicate quadrant=all and its quadrant=early configs trade rarely. They stay in the full factorial (and the raw trial count) so every axis has the same values.
- hold=full equals hold=session whenever N exceeds the bars left in the session (most of N = 48 / 64 / 96 on 15m bars).
- COVID (March-April 2020) falls inside the development period; the paper found the signal much weaker with those months included.
- Sizing ignores the stop distance (full equity per trade, as in the other families), so the ATR stops change the exit, not the position size.
