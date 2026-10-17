# Screening funnel -- mr_v1 (development stages only)

- Code: `737d995cb21f` (dirty working tree: True, diff sha256 `69bec2df2078`)
- Config: `/home/manit/Desktop/fun_projects/abalation_backtest/mean-reversion-backtest/configs/funnel/mr_funnel.yaml` sha256 `b62843a01348ec87`; seed 20261016
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'QQQ': '2026-08-18', 'SPY': '2026-08-18'}
- Frozen manifest sha256: `91f73e59b0e55da8` (15 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **False** -- No mean-reversion configuration has been selected on 2023-2024 yet. The same SPY validation slice WAS used to gate the channel-breakout funnels (funnel_v1..v4) and the Donchian ablation, so the researcher has seen how SPY behaved in that period.
- Holdout 2025+ previously inspected: **True** -- SPY 2025-2026 holdout metrics were computed and inspected for the Donchian ablation and the channel-breakout funnels (funnel_v1..v3 records.parquet). The holdout is NOT an untouched test of SPY, even for this new strategy.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 75000 | 75000 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 75000 | 75000 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 75000 | 50453 | 24547 | 0 |  | 61535 | 67.27 | 67.27 |  |
| 3 performance & risk | hard_gate | 50453 | 68 | 50385 | 0 |  | 0 | 0.09 | 0.13 |  |
| 4 parameter stability | hard_gate | 68 | 59 | 9 | 0 |  | 66 | 0.08 | 86.76 |  |
| 5 time stability | hard_gate | 59 | 59 | 0 | 0 |  | 35 | 0.08 | 100.00 |  |
| 6 deduplication | dedup | 59 | 15 |  |  | 44 |  | 0.02 | 25.42 |  |
| 7 execution stress | hard_gate | 15 | 15 | 0 | 0 |  | 1 | 0.02 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 15 |  |  |  |  |  |  |  | diagnostic only: unverified: 15 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 24547 |
| s2:hard_reject:years_with_>=10_trades | 10667 |
| s3:hard_reject:max_drawdown | 8654 |
| s3:hard_reject:net_return | 45803 |
| s3:hard_reject:sharpe | 50385 |
| s4:hard_reject:neighbor_frac_profitable | 9 |
| s4:hard_reject:neighbor_median_sharpe | 1 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | tf | mean | std | entry z | exit z | max hold | trend | z/time exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | QQQ dev SR |
|---|---|---|---|---:|---:|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_1698` | 15min | ema5 | 15 | -1.75 | -0.25 | 7 | sma150 | 149/6 | 155 | 11.5% | 2.2% | 1.11 | -2.4% | 155 | 1.91 | 2.1% | 62.0 | 11/11 | 0.82 | 0.87 | 0.23 | 5 | 8.2% | 0.29 | 0.31 | 9.6% | 7.6% | 6.7% | 10.3%/8.8% | 4.1 (interpolated) | pass | 0.007 (unverified) | 0.33 |
| 2 | `cfg_b0d0` | 15min | sma5 | 20 | -2.0 | -0.25 | 7 | sma150 | 178/3 | 181 | 11.6% | 2.2% | 1.07 | -2.6% | 251 | 1.75 | 2.4% | 72.3 | 10/10 | 0.80 | 0.86 | 0.21 | 4 | 7.7% | 0.33 | 0.35 | 9.3% | 7.1% | 4.9% | 10.1%/8.5% | 3.7 (interpolated) | pass | 0.006 (unverified) | 0.53 |
| 3 | `cfg_98bf` | 15min | sma5 | 15 | -2.0 | -0.25 | 5 | sma150 | 193/21 | 214 | 10.4% | 2.0% | 0.91 | -3.2% | 307 | 1.51 | 2.7% | 85.6 | 10/10 | 0.70 | 0.70 | 0.21 | 5 | 6.5% | 0.38 | 0.42 | 7.7% | 5.1% | 5.0% | 9.1%/7.2% | 3.0 (interpolated) | pass | 0.002 (unverified) | 0.61 |
| 4 | `cfg_834a` | 15min | ema10 | 15 | -2.0 | -0.25 | 5 | sma150 | 115/89 | 204 | 12.7% | 2.4% | 0.94 | -3.5% | 183 | 1.55 | 3.0% | 81.4 | 11/11 | 0.73 | 0.68 | 0.27 | 4 | 8.7% | 0.32 | 0.49 | 10.1% | 7.6% | 3.9% | 10.9%/8.7% | 3.6 (interpolated) | pass | 0.002 (unverified) | 0.35 |
| 5 | `cfg_be5d` | 15min | ema5 | 20 | -1.75 | -0.5 | 7 | sma200 | 150/0 | 150 | 7.8% | 1.5% | 0.89 | -2.0% | 349 | 1.70 | 1.7% | 60.0 | 10/10 | 0.70 | 0.67 | 0.22 | 4 | 5.2% | 0.32 | 0.46 | 5.9% | 4.1% | 5.5% | 6.9%/5.4% | 3.2 (interpolated) | pass | 0.001 (unverified) | 0.74 |
| 6 | `cfg_4958` | 15min | sma5 | 15 | -2.0 | 0.25 | 5 | sma150 | 133/81 | 214 | 14.4% | 2.7% | 1.01 | -4.1% | 400 | 1.61 | 3.2% | 85.6 | 10/10 | 0.80 | 0.60 | 0.40 | 5 | 8.7% | 0.40 | 0.50 | 11.6% | 8.9% | 7.7% | 12.6%/10.2% | 3.7 (interpolated) | pass | 0.003 (unverified) | 0.65 |
| 7 | `cfg_12b5` | 5min | ema15 | 40 | -2.0 | 0.25 | 10 | sma150 | 123/116 | 239 | 13.0% | 2.5% | 0.90 | -3.4% | 443 | 1.48 | 2.2% | 95.8 | 9/9 | 0.89 | 0.60 | 0.29 | 4 | 5.7% | 0.53 | 0.45 | 9.9% | 6.9% | 3.0% | 11.4%/9.0% | 3.2 (interpolated) | pass | 0.001 (unverified) | 0.13 |
| 8 | `cfg_899e` | 15min | sma10 | 15 | -2.0 | -0.25 | 5 | sma150 | 194/168 | 362 | 14.9% | 2.8% | 0.77 | -4.2% | 424 | 1.33 | 5.5% | 144.6 | 11/11 | 0.82 | 0.58 | 0.19 | 4 | 8.4% | 0.41 | 0.54 | 10.2% | 5.7% | 10.4% | 14.0%/11.0% | 2.7 (interpolated) | pass | 0.001 (unverified) | 0.72 |
| 9 | `cfg_779c` | 15min | sma5 | 20 | -1.75 | -0.25 | 7 | sma150 | 264/4 | 268 | 11.5% | 2.2% | 0.89 | -2.9% | 257 | 1.48 | 3.5% | 106.7 | 11/11 | 0.82 | 0.56 | 0.33 | 4 | 6.6% | 0.40 | 0.37 | 8.1% | 4.8% | 6.1% | 10.9%/9.0% | 2.8 (interpolated) | pass | 0.002 (unverified) | 0.45 |
| 10 | `cfg_d6fe` | 5min | ema15 | 60 | -1.75 | 0.5 | 10 | sma150 | 67/110 | 177 | 9.5% | 1.8% | 0.80 | -3.0% | 343 | 1.50 | 1.7% | 71.0 | 8/8 | 1.00 | 0.46 | 0.34 | 3 | 1.4% | 0.84 | 0.60 | 7.3% | 5.1% | 3.2% | 8.6%/6.3% | 3.2 (interpolated) | pass | 0.001 (unverified) | -0.04 |
| 11 | `cfg_5eea` | 5min | ema10 | 40 | -2.0 | 0.5 | 10 | sma150 | 84/93 | 177 | 10.1% | 1.9% | 0.78 | -2.5% | 496 | 1.50 | 1.6% | 71.0 | 8/8 | 0.88 | 0.45 | 0.33 | 4 | 4.7% | 0.54 | 0.61 | 7.9% | 5.7% | 1.2% | 8.7%/6.7% | 3.4 (interpolated) | pass | 0.000 (unverified) | 0.07 |
| 12 | `cfg_26a9` | 15min | ema5 | 15 | -1.75 | 0.0 | 2 | sma200 | 40/126 | 166 | 6.6% | 1.3% | 0.89 | -1.7% | 236 | 1.56 | 1.5% | 66.3 | 10/10 | 0.80 | 0.42 | 0.48 | 4 | 4.0% | 0.39 | 0.52 | 4.6% | 2.6% | -2.1% | 5.7%/4.6% | 2.7 (interpolated) | pass | 0.001 (unverified) | 0.45 |
| 13 | `cfg_df25` | 15min | sma15 | 20 | -1.75 | -0.5 | 5 | sma150 | 221/204 | 425 | 17.5% | 3.3% | 0.83 | -6.9% | 418 | 1.32 | 6.4% | 169.5 | 11/11 | 0.82 | 0.40 | 0.42 | 5 | 10.8% | 0.35 | 0.44 | 11.9% | 6.6% | 4.1% | 15.6%/11.6% | 2.7 (interpolated) | pass | 0.001 (unverified) | 0.25 |
| 14 | `cfg_941a` | 15min | sma5 | 15 | -1.75 | -0.25 | 10 | sma150 | 343/1 | 344 | 12.1% | 2.3% | 0.81 | -4.4% | 359 | 1.38 | 4.6% | 137.6 | 10/10 | 0.80 | 0.40 | 0.41 | 5 | 7.8% | 0.36 | 0.34 | 7.8% | 3.6% | 7.2% | 10.5%/8.5% | 2.5 (interpolated) | pass | 0.002 (unverified) | 0.62 |
| 15 | `cfg_c611` | 15min | ema10 | 15 | -2.0 | -0.25 | 3 | sma150 | 71/133 | 204 | 9.4% | 1.8% | 0.80 | -3.1% | 400 | 1.45 | 2.3% | 81.5 | 11/11 | 0.73 | 0.39 | 0.42 | 5 | 6.9% | 0.26 | 0.66 | 6.9% | 4.4% | 5.3% | 8.0%/5.7% | 2.9 (interpolated) | pass | 0.001 (unverified) | 0.56 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 0.7% / 0.57 / 17 | 2.4% / 1.65 / 43 | 2.7% / 0.94 / 34 | 2.2% / 1.12 / 38 | 3.1% / 1.49 / 23 |
| 2 | -0.7% / -0.41 / 23 | 2.5% / 1.58 / 47 | 3.5% / 1.09 / 44 | 3.7% / 2.36 / 44 | 2.1% / 1.06 / 23 |
| 3 | 0.6% / 0.36 / 28 | 2.7% / 1.70 / 52 | 1.4% / 0.43 / 54 | 1.6% / 0.91 / 51 | 3.7% / 1.74 / 29 |
| 4 | -0.1% / -0.07 / 27 | 2.3% / 1.26 / 57 | 3.0% / 0.69 / 50 | 3.3% / 1.86 / 40 | 3.7% / 1.58 / 30 |
| 5 | -1.0% / -0.86 / 17 | 2.5% / 2.18 / 37 | 1.9% / 0.70 / 42 | 1.8% / 1.70 / 33 | 2.3% / 1.30 / 21 |
| 6 | 0.4% / 0.22 / 28 | 2.4% / 1.37 / 52 | 5.0% / 1.06 / 54 | 0.8% / 0.42 / 51 | 5.3% / 2.17 / 29 |
| 7 | 2.2% / 0.99 / 38 | -2.0% / -1.05 / 45 | 6.9% / 1.67 / 62 | 0.4% / 0.20 / 53 | 5.1% / 1.65 / 41 |
| 8 | -1.7% / -0.54 / 56 | 3.6% / 1.26 / 89 | 6.0% / 1.02 / 94 | 2.4% / 1.03 / 79 | 3.9% / 1.14 / 44 |
| 9 | -1.0% / -0.50 / 40 | 1.9% / 1.06 / 69 | 4.6% / 1.14 / 69 | 4.1% / 2.29 / 57 | 1.5% / 0.71 / 33 |
| 10 | -0.3% / -0.24 / 28 | 0.5% / 0.39 / 33 | 7.9% / 2.35 / 53 | -0.9% / -0.42 / 34 | 2.2% / 0.76 / 29 |
| 11 | 0.9% / 0.73 / 24 | -1.2% / -0.81 / 32 | 4.6% / 1.16 / 47 | 0.3% / 0.19 / 41 | 5.2% / 1.76 / 33 |
| 12 | -0.4% / -0.52 / 16 | 0.2% / 0.14 / 48 | 2.0% / 1.02 / 37 | 2.5% / 1.95 / 39 | 2.2% / 1.35 / 26 |
| 13 | 0.5% / 0.19 / 69 | 0.4% / 0.16 / 103 | 6.0% / 0.96 / 105 | 5.0% / 1.86 / 91 | 4.5% / 1.18 / 57 |
| 14 | 1.0% / 0.58 / 45 | 3.7% / 1.77 / 86 | 0.2% / 0.07 / 89 | 2.6% / 1.15 / 82 | 4.0% / 1.71 / 42 |
| 15 | 0.2% / 0.14 / 27 | 2.2% / 1.39 / 57 | 2.3% / 0.61 / 50 | 2.2% / 1.30 / 40 | 2.1% / 1.17 / 30 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_4958` | 2 | 0.92 | 0.91/0.91 | 0.86/0.86 |
| 1 | `cfg_1698` | 14 | 0.80 | 0.79/0.88 | 0.75/0.84 |
| 2 | `cfg_12b5` | 3 | 0.96 | 0.98/0.98 | 0.96/0.96 |
| 3 | `cfg_899e` | 4 | 0.90 | 0.87/0.89 | 0.70/0.75 |
| 4 | `cfg_b0d0` | 10 | 0.90 | 0.91/0.96 | 0.86/0.89 |
| 5 | `cfg_26a9` | 2 | 0.96 | 0.96/0.96 | 1.00/1.00 |
| 6 | `cfg_98bf` | 4 | 0.87 | 0.93/0.94 | 0.92/0.96 |
| 7 | `cfg_5eea` | 2 | 0.96 | 0.97/0.97 | 0.94/0.94 |
| 8 | `cfg_779c` | 5 | 0.85 | 0.81/0.89 | 0.55/0.76 |
| 9 | `cfg_834a` | 3 | 0.85 | 0.88/0.93 | 0.89/0.93 |
| 10 | `cfg_941a` | 2 | 0.99 | 0.99/0.99 | 1.00/1.00 |
| 11 | `cfg_d6fe` | 2 | 0.98 | 0.98/0.98 | 0.97/0.97 |
| 12 | `cfg_c611` | 2 | 0.98 | 0.98/0.98 | 0.98/0.98 |
| 13 | `cfg_be5d` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 14 | `cfg_df25` | 2 | 0.88 | 0.84/0.84 | 0.80/0.80 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.627e-03 over 74775 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1650.0, participation ratio 23.6, 95%-variance components 398 (rank bound T = 1259); raw grid 75000; raw + known prior 103464
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
QQQ results are unchanged rules on the development period: supporting evidence, not an independent replication.

## Integrity audit

- z = (close - mean) / std with mean = SMA/EMA of the last N closes and std = rolling sample std of the last M closes (bars of the config's timeframe), both INCLUDING the signal bar's close; the signal is decided at that close and the entry fills at the NEXT bar's open.
- Exits are decided at a close on or after the entry bar (z >= exit_z, or held max_hold bars) and fill at the next bar's open, so a time exit fills exactly max_hold bars after entry.
- Trend filter compares the signal bar's close to the SMA(100/150/200 bars) of closes up to that bar; warm-up bars (SMA undefined) never signal.
- No stop loss and no profit target exist, so no bar can touch both; checked per trade. Sizing: as many whole shares as current equity affords (no leverage), since risk-based sizing needs a stop distance.
- After a time exit the setup re-arms only once z closes above entry_z, so the holding cap cannot be undone by an immediate re-entry.
- Missed-entry stress skips a whole signal episode (contiguous signal bars), never re-entering one bar later.
- Adverse slippage + commission on every fill; a fill at a session's first bar bears the full overnight gap.
- Development backtests run on data physically truncated at the development end; open positions are force-closed at the last development bar and flagged (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Positions are held overnight (no session-end flattening), as in the channel family; rolling windows run continuously across sessions over RTH bars only.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Unresolved assumptions

- Drawdown limit -30% is reused from the channel-breakout funnel (src/experiments/validation.py); that approval was given for 0.25%-risk stop-based sizing, while this strategy invests full equity per trade -- it has not been separately approved for this sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0: Sharpe vs. cash is overstated in high-rate years (2023-2024 ~5%).
- Variable cost stress scales per-share commission and slippage bps; the $1 per-order minimum commission is treated as fixed.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Prices are split-adjusted but NOT dividend-adjusted: SPY's ~1.5%/yr dividend is not credited while long, and each ex-dividend drop slightly lowers z (a small bias toward entries on ex-div dates).
- Neighbor lattice treats timeframe, mean_lookback, std_lookback, entry_z, exit_z and max_hold as ordered axes; mean_type and trend_filter are held fixed (categorical).
- All lookbacks, trend SMAs and holding periods are counted in bars of the config's timeframe (e.g. sma200 on 5min bars spans ~2.6 sessions), not in trading days.
