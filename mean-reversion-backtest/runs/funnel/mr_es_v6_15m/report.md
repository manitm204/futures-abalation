# Screening funnel -- mr_es_v6_15m (development stages only)

- Code: `5342a94cdc84` (dirty working tree: True, diff sha256 `6677d242d984`)
- Config: `configs/funnel/mr_funnel_es_v6_15m.yaml` sha256 `b5f9ccf7d718f9d1`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ES': '2026-10-16', 'NQ': '2026-10-16'}
- Frozen manifest sha256: `8f437e36621fb58a` (7 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_es_v3, v4 and v5 gated 11, 18 and 45 ES candidates on 2023-2024, and this grid was chosen after reading those results (and the per-bar-size breakdown of v5's development survivors). ES also tracks the same index as SPY, whose 2023-2024 gated earlier SPY studies. So ES 2023-2024 is largely in-sample here; the 2025+ holdout is the only untouched test.
- Holdout 2025+ previously inspected: **False** -- No ES strategy metrics have been computed on 2025+. SPY 2025-2026 holdout metrics were inspected in earlier SPY studies, and the futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no strategy selection).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 864 | 864 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 864 | 864 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 864 | 700 | 164 | 0 |  | 819 | 81.02 | 81.02 |  |
| 3 performance & risk | hard_gate | 700 | 14 | 686 | 0 |  | 0 | 1.62 | 2.00 |  |
| 4 parameter stability | hard_gate | 14 | 11 | 3 | 0 |  | 0 | 1.27 | 78.57 |  |
| 5 time stability | hard_gate | 11 | 11 | 0 | 0 |  | 5 | 1.27 | 100.00 |  |
| 6 deduplication | dedup | 11 | 7 |  |  | 4 |  | 0.81 | 63.64 | best 2 per cluster |
| 7 execution stress | hard_gate | 7 | 7 | 0 | 0 |  | 0 | 0.81 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 7 |  |  |  |  |  |  |  | diagnostic only: unverified: 7 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 164 |
| s2:hard_reject:years_with_>=10_trades | 126 |
| s3:hard_reject:max_drawdown | 7 |
| s3:hard_reject:net_return | 385 |
| s3:hard_reject:sharpe | 686 |
| s4:hard_reject:local_median_sharpe | 3 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | NQ dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_7370` | timeframe=15min, mean_type=sma, mean_lookback=47, std_lookback=21, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 30/179/0 | 209 | 27.3% | 5.0% | 0.81 | -8.8% | 203 | 1.52 | 3.7% | 98.6 | 8/8 | 1.00 | 0.57 | 0.24 | 4 | 16.6% | 0.38 | 0.61 | 25.7% | 22.7% | 7.1% | 22.8%/14.4% | 7.6 (interpolated) | pass | 0.179 (unverified) | 0.77 |
| 2 | `cfg_ec72` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=21, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 52/248/0 | 300 | 33.7% | 6.0% | 0.88 | -9.9% | 187 | 1.47 | 5.3% | 139.9 | 8/8 | 1.00 | 0.64 | 0.25 | 5 | 24.7% | 0.25 | 0.53 | 31.6% | 29.2% | 27.7% | 32.0%/24.7% | 6.9 (interpolated) | pass | 0.225 (unverified) | 0.63 |
| 3 | `cfg_a858` | timeframe=15min, mean_type=sma, mean_lookback=57, std_lookback=21, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 71/287/0 | 358 | 27.8% | 5.0% | 0.86 | -7.6% | 362 | 1.40 | 6.3% | 168.9 | 7/7 | 0.86 | 0.60 | 0.26 | 4 | 15.4% | 0.39 | 0.48 | 24.4% | 20.7% | 33.0% | 25.4%/18.6% | 5.0 (interpolated) | pass | 0.207 (unverified) | 0.67 |
| 4 | `cfg_1fed` | timeframe=15min, mean_type=sma, mean_lookback=57, std_lookback=21, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 30/324/0 | 354 | 27.6% | 5.0% | 0.83 | -7.4% | 360 | 1.40 | 6.4% | 166.6 | 7/7 | 0.86 | 0.51 | 0.32 | 4 | 13.7% | 0.45 | 0.51 | 23.3% | 19.0% | 27.8% | 24.8%/17.4% | 4.9 (interpolated) | pass | 0.187 (unverified) | 0.63 |
| 5 | `cfg_0d08` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=27, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 4/101/0 | 105 | 11.4% | 2.2% | 0.88 | -2.9% | 138 | 1.69 | 1.9% | 48.7 | 7/7 | 1.00 | 0.48 | 0.39 | 5 | 6.7% | 0.39 | 0.63 | 10.5% | 9.7% | 12.7% | 10.4%/8.0% | 7.2 (interpolated) | pass | 0.219 (unverified) | 0.21 |
| 6 | `cfg_2e48` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=27, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 25/80/0 | 105 | 9.7% | 1.9% | 0.78 | -2.9% | 215 | 1.59 | 1.9% | 48.8 | 7/7 | 0.86 | 0.47 | 0.32 | 5 | 5.5% | 0.41 | 0.70 | 8.9% | 8.4% | 10.3% | 9.1%/7.0% | 6.3 (interpolated) | pass | 0.163 (unverified) | 0.13 |
| 7 | `cfg_e44a` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=21, entry_z=-2.5, exit_z=0.0, max_holding_bars=7, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 51/131/0 | 182 | 29.4% | 5.3% | 0.78 | -8.7% | 171 | 1.49 | 4.1% | 84.4 | 7/7 | 1.00 | 0.39 | 0.38 | 5 | 12.2% | 0.55 | 0.63 | 26.9% | 24.7% | 9.9% | 26.2%/19.2% | 9.2 (interpolated) | pass | 0.168 (unverified) | -0.01 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | -0.8% / -0.15 / 43 | 7.2% / 2.19 / 36 | 6.1% / 0.58 / 46 | 9.2% / 2.72 / 26 | 3.4% / 0.65 / 58 |
| 2 | 3.0% / 0.56 / 66 | 6.2% / 1.78 / 56 | 7.1% / 0.63 / 59 | 7.2% / 1.95 / 38 | 6.4% / 1.05 / 81 |
| 3 | -3.7% / -0.68 / 84 | 5.7% / 1.73 / 63 | 10.7% / 1.17 / 64 | 8.5% / 2.21 / 58 | 4.6% / 0.72 / 89 |
| 4 | -3.2% / -0.60 / 83 | 5.8% / 1.76 / 63 | 12.2% / 1.26 / 63 | 8.6% / 2.17 / 57 | 2.2% / 0.36 / 88 |
| 5 | 4.4% / 2.19 / 18 | 1.3% / 0.86 / 20 | 0.2% / 0.06 / 19 | 1.3% / 0.85 / 11 | 3.8% / 1.16 / 37 |
| 6 | 4.0% / 2.07 / 18 | 1.1% / 0.76 / 20 | 0.2% / 0.06 / 19 | 1.3% / 0.82 / 11 | 3.0% / 0.99 / 37 |
| 7 | 2.0% / 0.42 / 38 | 2.7% / 1.12 / 29 | 15.4% / 1.18 / 40 | 5.1% / 1.85 / 20 | 2.0% / 0.34 / 55 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_0d08` | 2 | 0.99 | 0.99/0.99 | 0.97/0.97 |
| 1 | `cfg_a858` | 2 | 0.98 | 0.97/0.97 | 0.96/0.96 |
| 2 | `cfg_7370` | 6 | 0.81 | 0.73/0.80 | 0.45/0.67 |
| 3 | `cfg_e44a` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 8.233e-04 over 864 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 145.0, participation ratio 7.9, 95%-variance components 71 (rank bound T = 1259); raw grid 864; raw + known prior 859848
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
