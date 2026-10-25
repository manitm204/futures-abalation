# Screening funnel -- mr_nq_v7_15m (development stages only)

- Code: `5342a94cdc84` (dirty working tree: True, diff sha256 `7d2faef5babc`)
- Config: `configs/funnel/mr_funnel_nq_v7_15m.yaml` sha256 `b86bf7da00c509b6`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ES': '2026-10-16', 'NQ': '2026-10-16'}
- Frozen manifest sha256: `f7635b7a0c95995d` (8 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_nq_v5 gated 93 NQ candidates on 2023-2024 (38 passed), mr_nq_v6 was narrowed around those survivors, and this v7 grid was chosen after reading both, so NQ 2023-2024 is largely in-sample for v7. The grid, the stage-4 test and the 40-trade rule were also shaped by ES 2023-2024 (mr_es_v3..v5).
- Holdout 2025+ previously inspected: **False** -- No NQ strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection), and two ES strategies (mr_es_v6_1h #8, #15; a correlated index) were scored on the ES 2025+ holdout on 2026-10-24. The holdout is the only untouched test for this run.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 1152 | 1152 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 1152 | 1152 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 1152 | 586 | 566 | 0 |  | 758 | 50.87 | 50.87 |  |
| 3 performance & risk | hard_gate | 586 | 12 | 574 | 0 |  | 0 | 1.04 | 2.05 |  |
| 4 parameter stability | hard_gate | 12 | 11 | 1 | 0 |  | 0 | 0.95 | 91.67 |  |
| 5 time stability | hard_gate | 11 | 11 | 0 | 0 |  | 11 | 0.95 | 100.00 |  |
| 6 deduplication | dedup | 11 | 8 |  |  | 3 |  | 0.69 | 72.73 | best 2 per cluster |
| 7 execution stress | hard_gate | 8 | 8 | 0 | 0 |  | 1 | 0.69 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 8 |  |  |  |  |  |  |  | diagnostic only: unverified: 8 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 566 |
| s2:hard_reject:years_with_>=10_trades | 432 |
| s3:hard_reject:net_return | 326 |
| s3:hard_reject:sharpe | 574 |
| s4:hard_reject:local_median_sharpe | 1 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_bfe6` | timeframe=15min, mean_type=sma, mean_lookback=70, std_lookback=23, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 56/282/0 | 338 | 42.0% | 7.3% | 1.07 | -11.6% | 277 | 1.43 | 6.0% | 171.2 | 7/7 | 1.00 | 0.90 | 0.16 | 4 | 13.9% | 0.67 | 0.51 | 40.9% | 39.1% | 20.2% | 36.4%/26.1% | 15.1 (interpolated) | pass | 0.470 (unverified) | 0.70 |
| 2 | `cfg_57d6` | timeframe=15min, mean_type=sma, mean_lookback=70, std_lookback=23, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 28/309/0 | 337 | 40.4% | 7.0% | 1.04 | -12.4% | 277 | 1.42 | 6.1% | 170.4 | 7/7 | 1.00 | 0.79 | 0.25 | 4 | 12.8% | 0.69 | 0.53 | 38.4% | 35.8% | 24.4% | 34.3%/24.8% | 14.3 (interpolated) | pass | 0.439 (unverified) | 0.70 |
| 3 | `cfg_5f96` | timeframe=15min, mean_type=sma, mean_lookback=70, std_lookback=23, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 22/260/0 | 282 | 28.2% | 5.1% | 0.79 | -12.1% | 277 | 1.33 | 5.1% | 141.9 | 8/8 | 0.75 | 0.47 | 0.32 | 4 | 9.4% | 0.71 | 0.57 | 27.7% | 25.7% | 21.5% | 24.9%/17.2% | 13.0 (interpolated) | pass | 0.236 (unverified) | 0.02 |
| 4 | `cfg_024c` | timeframe=15min, mean_type=sma, mean_lookback=70, std_lookback=23, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 38/244/0 | 282 | 29.2% | 5.3% | 0.81 | -11.5% | 277 | 1.34 | 5.0% | 141.8 | 8/8 | 0.75 | 0.47 | 0.34 | 4 | 10.4% | 0.68 | 0.55 | 28.6% | 27.3% | 19.3% | 24.8%/17.4% | 13.6 (interpolated) | pass | 0.252 (unverified) | 0.04 |
| 5 | `cfg_5f3f` | timeframe=15min, mean_type=sma, mean_lookback=70, std_lookback=28, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 33/264/0 | 297 | 32.1% | 5.7% | 0.96 | -13.4% | 271 | 1.42 | 5.3% | 148.7 | 7/7 | 0.86 | 0.52 | 0.44 | 3 | 3.5% | 0.93 | 0.54 | 30.7% | 29.5% | -0.2% | 28.7%/18.9% | 13.9 (interpolated) | pass | 0.368 (unverified) | -0.04 |
| 6 | `cfg_29c7` | timeframe=15min, mean_type=sma, mean_lookback=70, std_lookback=28, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 18/279/0 | 297 | 32.3% | 5.8% | 0.95 | -14.6% | 271 | 1.42 | 5.4% | 148.6 | 7/7 | 0.86 | 0.43 | 0.52 | 3 | 2.8% | 0.96 | 0.56 | 31.5% | 30.1% | 2.9% | 28.8%/21.8% | 14.3 (interpolated) | pass | 0.357 (unverified) | 0.01 |
| 7 | `cfg_80bb` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=23, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 44/213/0 | 257 | 32.2% | 5.8% | 0.91 | -6.3% | 277 | 1.43 | 4.6% | 130.5 | 8/8 | 0.88 | 0.35 | 0.55 | 4 | 14.3% | 0.50 | 0.37 | 30.6% | 28.1% | 25.3% | 27.5%/19.1% | 15.8 (interpolated) | pass | 0.328 (unverified) | 0.74 |
| 8 | `cfg_2bfd` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=23, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 30/227/0 | 257 | 30.6% | 5.5% | 0.87 | -7.0% | 277 | 1.41 | 4.6% | 130.5 | 8/8 | 0.88 | 0.35 | 0.52 | 4 | 12.9% | 0.52 | 0.39 | 29.2% | 26.3% | 23.5% | 25.6%/17.9% | 15.3 (interpolated) | pass | 0.299 (unverified) | 0.74 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 1.8% / 0.37 / 74 | 12.0% / 2.85 / 59 | 24.7% / 2.33 / 56 | 5.9% / 1.32 / 62 | -5.7% / -0.64 / 87 |
| 2 | 1.4% / 0.30 / 73 | 12.0% / 2.84 / 59 | 24.5% / 2.32 / 56 | 6.0% / 1.35 / 62 | -6.4% / -0.72 / 87 |
| 3 | 1.1% / 0.22 / 62 | 15.5% / 3.27 / 51 | 17.2% / 1.77 / 46 | 2.9% / 0.71 / 44 | -9.0% / -1.18 / 79 |
| 4 | 1.3% / 0.24 / 62 | 15.5% / 3.28 / 51 | 17.0% / 1.76 / 46 | 3.0% / 0.73 / 44 | -8.4% / -1.11 / 79 |
| 5 | -0.2% / -0.02 / 59 | 8.4% / 2.54 / 54 | 27.7% / 2.83 / 49 | 4.5% / 1.12 / 53 | -8.5% / -1.28 / 82 |
| 6 | -0.4% / -0.05 / 59 | 8.5% / 2.54 / 54 | 28.8% / 2.84 / 49 | 5.4% / 1.31 / 53 | -9.7% / -1.46 / 82 |
| 7 | 2.3% / 0.43 / 45 | 15.7% / 3.37 / 49 | 9.4% / 1.09 / 41 | 3.8% / 0.89 / 41 | -1.6% / -0.16 / 81 |
| 8 | 2.3% / 0.44 / 45 | 15.7% / 3.37 / 49 | 9.2% / 1.07 / 41 | 3.6% / 0.86 / 41 | -2.5% / -0.28 / 81 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_5f96` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 1 | `cfg_5f3f` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 2 | `cfg_80bb` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 3 | `cfg_bfe6` | 5 | 0.85 | 0.77/0.84 | 0.69/0.70 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 6.253e-04 over 1144 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 203.0, participation ratio 13.1, 95%-variance components 100 (rank bound T = 1259); raw grid 1152; raw + known prior 585852
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

- z = (close - mean) / std with mean = SMA/EMA of the last N closes and std = rolling sample std of the last M closes (bars of the config's timeframe), both INCLUDING the signal bar's close; the signal is decided at that close and the entry fills at the NEXT bar's open.
- Exits are decided at a close on or after the entry bar (z >= exit_z, or held max_hold bars) and fill at the next bar's open, so a time exit fills exactly max_hold bars after entry.
- Trend filter compares the signal bar's close to the SMA(100/150/200 bars) of closes up to that bar; warm-up bars (SMA undefined) never signal.
- No profit target exists. v1 has no stop; v2's optional ATR stop is entry fill - k x ATR(14) using the ATR known before the fill, live from the entry bar, filled at the worse of open and stop. Sizing (v1 and v2): as many whole shares as current equity affords (no leverage).
- v2 only: the z-score std uses the same window as the mean; positive_bar_return requires the signal bar's close above the previous close; cooldown_bars = N requires the next signal bar to be >= N bars after the previous exit.
- After a time exit the setup re-arms only once z closes above entry_z, so the holding cap cannot be undone by an immediate re-entry.
- Missed-entry stress skips a whole signal episode (contiguous signal bars), never re-entering one bar later.
- Adverse slippage + commission on every fill; a fill at a session's first bar bears the full overnight gap.
- Development backtests run on data physically truncated at the development end; open positions are force-closed at the last development bar and flagged (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Positions are held overnight (no session-end flattening), as in the channel family; rolling windows run continuously across sessions over RTH bars only.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC; the 1-minute step there is taken as the roll spread). Point moves are preserved; pre-roll price levels are not real traded prices.
- Session: each root's day session only (src/data/futures.py SESSIONS: NYSE 09:30-16:00 NY for equity indexes, 09:00-14:30 NY for crude, 08:20-13:30 NY for gold, 08:20-15:00 NY for FX; sessions under 5% of normal volume are skipped), on NYSE trading days; overnight Globex bars are not traded or used in indicators.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side (stops too) plus commission per contract per side, from the execution YAML; cost stress scales both.
- Positions that straddle a roll are treated as if rolled for free at the adjusted spread (no extra roll commission/slippage).

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Whole-contract granularity: at ~$1M equity the position is a handful of ES contracts, so position size steps with price; results are sensitive to starting equity at small sizes.
- All lookbacks and holding periods are counted in bars of the config's timeframe (RTH bars only), not in trading days.
- entry_confirmation = positive_bar_return means the signal bar closed above the previous bar's close (the 'directional bar' option).
