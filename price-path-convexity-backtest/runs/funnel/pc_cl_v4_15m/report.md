# Screening funnel -- pc_cl_v4_15m (development stages only)

- Code: `26d90d38fa4c` (dirty working tree: True, diff sha256 `00638be347ae`)
- Config: `configs/funnel/pc_funnel_cl_v4_15m.yaml` sha256 `e4447c2f48e35bb1`; seed 20261116
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ES': '2026-10-16', 'CL': '2026-10-16'}
- Frozen manifest sha256: `7d88218e55f0affd` (13 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No convexity strategy has been scored on CL 2023-2024, but BB/KC squeeze, NR squeeze, noise-band and mean-reversion strategies were selected there and the researcher has read those results. Treated as used for selection.
- Holdout 2025+ previously inspected: **False** -- No convexity metrics have been computed on CL 2025+. Convexity picks were scored on ES and NQ 2025+ (all lost), so the researcher has seen how that period treated this line on index futures.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 10368 | 10368 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 10368 | 10368 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 10368 | 7844 | 2524 | 0 |  | 5530 | 75.66 | 75.66 |  |
| 3 performance & risk | hard_gate | 7844 | 42 | 7802 | 0 |  | 0 | 0.41 | 0.54 |  |
| 4 parameter stability | hard_gate | 42 | 34 | 8 | 0 |  | 0 | 0.33 | 80.95 |  |
| 5 time stability | hard_gate | 34 | 32 | 2 | 0 |  | 34 | 0.31 | 94.12 |  |
| 6 deduplication | dedup | 32 | 13 |  |  | 19 |  | 0.13 | 40.62 | best 2 per cluster |
| 7 execution stress | hard_gate | 13 | 13 | 0 | 0 |  | 0 | 0.13 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 13 |  |  |  |  |  |  |  | diagnostic only: unverified: 13 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 2524 |
| s2:hard_reject:years_with_>=10_trades | 2084 |
| s3:hard_reject:max_drawdown | 4860 |
| s3:hard_reject:net_return | 6081 |
| s3:hard_reject:sharpe | 7800 |
| s4:hard_reject:local_median_sharpe | 8 |
| s5:hard_reject:profitable_years | 2 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_4389` | timeframe=15min, lookback=50, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=early, min_move_atr=0.0, direction=long, hold=1.5n, stop=none, trend_filter=ema50 | 0/282/0 | 282 | 55.4% | 9.2% | 0.84 | -11.7% | 247 | 1.43 | 13.1% | 44.9 | 6/6 | 0.67 | 0.52 | 0.32 | 3 | 5.3% | 0.86 | 0.75 | 46.6% | 38.3% | 64.6% | 47.4%/35.4% | 4.8 (interpolated) | pass | 0.107 (unverified) | -0.56 |
| 2 | `cfg_95d4` | timeframe=15min, lookback=50, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=early, min_move_atr=0.0, direction=long, hold=full, stop=none, trend_filter=ema50 | 0/282/0 | 282 | 55.4% | 9.2% | 0.84 | -11.7% | 247 | 1.43 | 13.1% | 44.9 | 6/6 | 0.67 | 0.52 | 0.32 | 3 | 5.3% | 0.86 | 0.75 | 46.6% | 38.3% | 64.6% | 47.9%/36.1% | 4.8 (interpolated) | pass | 0.107 (unverified) | -0.56 |
| 3 | `cfg_9643` | timeframe=15min, lookback=20, signal_form=reversal, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=0.0, direction=long, hold=full, stop=none, trend_filter=ema50 | 31/282/0 | 313 | 54.1% | 9.0% | 0.93 | -13.7% | 215 | 1.51 | 12.4% | 52.3 | 7/7 | 0.57 | 0.47 | 0.46 | 3 | 21.5% | 0.45 | 0.58 | 43.5% | 35.3% | 55.9% | 51.0%/40.5% | 4.4 (interpolated) | pass | 0.135 (unverified) | -0.44 |
| 4 | `cfg_4413` | timeframe=15min, lookback=20, signal_form=reversal, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=0.0, direction=long, hold=1.5n, stop=none, trend_filter=ema50 | 0/313/0 | 313 | 52.3% | 8.8% | 0.90 | -13.6% | 215 | 1.49 | 12.5% | 52.3 | 7/7 | 0.57 | 0.48 | 0.42 | 3 | 21.1% | 0.44 | 0.61 | 42.9% | 34.3% | 55.9% | 46.2%/35.7% | 4.3 (interpolated) | pass | 0.122 (unverified) | -0.99 |
| 5 | `cfg_08bd` | timeframe=15min, lookback=50, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=early, min_move_atr=0.0, direction=both, hold=full, stop=none, trend_filter=none | 0/648/0 | 648 | 86.9% | 13.3% | 0.77 | -21.6% | 372 | 1.19 | 32.0% | 97.2 | 6/6 | 0.67 | 0.34 | 0.43 | 3 | 2.8% | 1.10 | 0.69 | 62.9% | 42.4% | 122.9% | 83.9%/55.5% | 3.3 (interpolated) | pass | 0.102 (unverified) | -0.52 |
| 6 | `cfg_ba82` | timeframe=15min, lookback=50, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=early, min_move_atr=0.0, direction=both, hold=1.5n, stop=none, trend_filter=none | 0/648/0 | 648 | 86.9% | 13.3% | 0.77 | -21.6% | 372 | 1.19 | 32.0% | 97.2 | 6/6 | 0.67 | 0.34 | 0.43 | 3 | 2.8% | 1.10 | 0.69 | 62.9% | 42.4% | 122.9% | 78.2%/54.3% | 3.3 (interpolated) | pass | 0.102 (unverified) | -0.52 |
| 7 | `cfg_0129` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=short, hold=full, stop=none, trend_filter=none | 43/167/0 | 210 | 57.2% | 9.5% | 0.78 | -8.5% | 369 | 1.51 | 8.3% | 29.8 | 7/7 | 0.71 | 0.30 | 0.48 | 4 | 1.8% | 0.92 | 1.00 | 49.7% | 43.1% | 43.3% | 53.1%/35.2% | 6.0 (interpolated) | pass | 0.060 (unverified) | -1.41 |
| 8 | `cfg_29dc` | timeframe=15min, lookback=50, signal_form=reversal, z_lookback=250, entry_z=0.5, quadrant=early, min_move_atr=0.0, direction=both, hold=full, stop=3.0, trend_filter=none | 0/110/20 | 130 | 43.7% | 7.5% | 0.98 | -7.8% | 206 | 1.68 | 6.2% | 17.3 | 6/6 | 0.33 | 0.05 | 0.93 | 3 | 6.3% | 0.82 | 0.59 | 39.3% | 34.4% | 48.8% | 39.1%/32.3% | 7.1 (interpolated) | pass | 0.208 (unverified) | -0.36 |
| 9 | `cfg_504d` | timeframe=15min, lookback=50, signal_form=reversal, z_lookback=250, entry_z=0.5, quadrant=early, min_move_atr=0.0, direction=both, hold=1.5n, stop=3.0, trend_filter=none | 0/110/20 | 130 | 43.7% | 7.5% | 0.98 | -7.8% | 206 | 1.68 | 6.2% | 17.3 | 6/6 | 0.33 | 0.06 | 0.92 | 3 | 6.3% | 0.82 | 0.59 | 39.3% | 34.4% | 48.8% | 39.3%/29.9% | 7.1 (interpolated) | pass | 0.208 (unverified) | -0.36 |
| 10 | `cfg_4ea9` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 0/210/0 | 210 | 56.3% | 9.4% | 0.76 | -10.2% | 346 | 1.50 | 8.4% | 29.9 | 7/7 | 0.71 | 0.26 | 0.50 | 4 | -0.2% | 0.94 | 1.00 | 49.2% | 42.2% | 43.3% | 53.6%/32.3% | 5.9 (interpolated) | pass | 0.057 (unverified) | -1.32 |
| 11 | `cfg_0443` | timeframe=15min, lookback=10, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=late, min_move_atr=0.0, direction=long, hold=1.5n, stop=3.0, trend_filter=ema50 | 38/88/12 | 138 | 26.8% | 4.9% | 0.90 | -7.1% | 188 | 1.59 | 5.1% | 16.7 | 8/8 | 0.88 | 0.67 | 0.23 | 5 | 17.0% | 0.33 | 0.57 | 22.8% | 19.0% | 15.6% | 23.3%/16.9% | 4.7 (interpolated) | pass | 0.147 (unverified) | -0.17 |
| 12 | `cfg_063f` | timeframe=15min, lookback=50, signal_form=reversal, z_lookback=250, entry_z=0.5, quadrant=all, min_move_atr=0.0, direction=both, hold=full, stop=3.0, trend_filter=ema50 | 0/187/26 | 213 | 46.6% | 8.0% | 0.92 | -7.8% | 327 | 1.56 | 9.5% | 31.8 | 6/6 | 0.67 | 0.36 | 0.56 | 4 | 22.3% | 0.41 | 0.66 | 39.9% | 34.2% | 53.5% | 41.4%/31.5% | 5.2 (interpolated) | pass | 0.141 (unverified) | -0.20 |
| 13 | `cfg_cfd2` | timeframe=15min, lookback=50, signal_form=reversal, z_lookback=250, entry_z=0.5, quadrant=all, min_move_atr=0.0, direction=both, hold=1.5n, stop=3.0, trend_filter=ema50 | 0/187/26 | 213 | 46.6% | 8.0% | 0.92 | -7.8% | 327 | 1.56 | 9.5% | 31.8 | 6/6 | 0.67 | 0.36 | 0.56 | 4 | 22.3% | 0.41 | 0.66 | 39.9% | 34.2% | 53.5% | 43.0%/31.8% | 5.2 (interpolated) | pass | 0.141 (unverified) | -0.20 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 7.8% / 1.33 / 48 | -6.6% / -0.80 / 61 | 47.5% / 2.02 / 56 | 5.4% / 0.91 / 59 | -0.8% / -0.04 / 58 |
| 2 | 7.8% / 1.33 / 48 | -6.6% / -0.80 / 61 | 47.5% / 2.02 / 56 | 5.4% / 0.91 / 59 | -0.8% / -0.04 / 58 |
| 3 | -0.5% / -0.06 / 53 | -9.6% / -1.01 / 64 | 26.8% / 1.65 / 54 | 16.9% / 2.27 / 71 | 15.6% / 1.59 / 71 |
| 4 | -1.0% / -0.17 / 53 | -9.5% / -1.00 / 64 | 25.7% / 1.61 / 54 | 17.5% / 2.28 / 71 | 15.1% / 1.50 / 71 |
| 5 | 15.3% / 1.46 / 122 | 1.6% / 0.20 / 125 | 81.8% / 2.02 / 128 | -7.9% / -0.57 / 134 | -4.7% / -0.20 / 139 |
| 6 | 15.3% / 1.46 / 122 | 1.6% / 0.20 / 125 | 81.8% / 2.02 / 128 | -7.9% / -0.57 / 134 | -4.7% / -0.20 / 139 |
| 7 | 1.3% / 0.32 / 42 | -5.1% / -0.55 / 43 | 54.5% / 1.96 / 45 | 1.7% / 0.26 / 38 | 4.2% / 0.48 / 42 |
| 8 | -1.5% / -0.19 / 43 | 3.1% / 0.81 / 15 | 35.2% / 2.71 / 28 | 6.6% / 0.99 / 28 | -1.9% / -0.22 / 16 |
| 9 | -1.5% / -0.19 / 43 | 3.1% / 0.81 / 15 | 35.2% / 2.71 / 28 | 6.6% / 0.99 / 28 | -1.9% / -0.22 / 16 |
| 10 | 0.9% / 0.22 / 42 | -7.3% / -0.75 / 43 | 56.6% / 2.02 / 45 | 2.2% / 0.32 / 38 | 4.4% / 0.49 / 42 |
| 11 | 5.1% / 1.10 / 19 | 1.4% / 0.42 / 24 | 8.4% / 0.98 / 45 | 6.5% / 1.74 / 26 | 3.1% / 0.61 / 24 |
| 12 | 2.7% / 0.40 / 51 | -5.6% / -1.00 / 38 | 19.9% / 1.43 / 49 | 11.5% / 1.82 / 41 | 13.2% / 1.42 / 34 |
| 13 | 2.7% / 0.40 / 51 | -5.6% / -1.00 / 38 | 19.9% / 1.43 / 49 | 11.5% / 1.82 / 41 | 13.2% / 1.42 / 34 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_0129` | 2 | 1.00 | 1.00/1.00 | 0.98/0.98 |
| 1 | `cfg_0443` | 1 | n/a | n/a/n/a | n/a/n/a |
| 2 | `cfg_063f` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 3 | `cfg_08bd` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 4 | `cfg_4389` | 12 | 0.88 | 0.77/0.97 | 0.51/0.95 |
| 5 | `cfg_9643` | 9 | 0.83 | 0.61/0.63 | 0.54/0.59 |
| 6 | `cfg_29dc` | 4 | 0.98 | 0.98/0.98 | 0.92/0.92 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 7.186e-04 over 9744 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 786.0, participation ratio 22.8, 95%-variance components 253 (rank bound T = 1258); raw grid 10368; raw + known prior 2056212
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
