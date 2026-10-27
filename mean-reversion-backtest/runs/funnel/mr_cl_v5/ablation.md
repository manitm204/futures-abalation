# Ablation (development only) -- mr_cl_v5

- Symbol CL, strategy `mean_reversion_v5`, 41,472 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 28,617 configs (69.0%).
- Grid-wide: 27.3% profitable, median dev Sharpe -0.18, 533 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 41472 | 41472 |  |
| 1 backtest integrity | 41472 | 41472 |  |
| 2 trade count & coverage | 41472 | 28617 |  |
| 3 performance & risk | 28617 | 377 |  |
| 4 parameter stability | 377 | 360 |  |
| 5 time stability | 360 | 356 |  |
| 6 deduplication | 356 | 75 | best 2 per cluster |
| 7 execution stress | 75 | 75 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 75 |  | diagnostic only: unverified: 75 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| timeframe | 0.539 |
| std_lookback | 0.230 |
| stop_atr_multiple | 0.096 |
| mean_lookback | 0.075 |
| mean_type | 0.043 |
| exit_z | 0.043 |
| max_holding_bars | 0.027 |
| entry_z | 0.023 |
| entry_confirmation | 0.003 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 5min | 13824 | 14.7% | -0.52 | 0.18 | 0.2% | 94.2% | -0.55 | 867 | 15 | 3 | 0.06 |
| timeframe | 15min | 13824 | 43.2% | 0.01 | 0.53 | 3.5% | 79.6% | 0.02 | 288 | 359 | 71 | 2.94 |
| timeframe | 1h | 13824 | 24.1% | -0.15 | 0.27 | 0.2% | 33.2% | -0.09 | 68 | 3 | 1 | 0.00 |
| mean_type | sma | 20736 | 27.8% | -0.16 | 0.36 | 1.3% | 72.0% | -0.17 | 252 | 196 | 49 | 1.06 |
| mean_type | ema | 20736 | 26.8% | -0.20 | 0.35 | 1.3% | 66.0% | -0.22 | 195 | 181 | 26 | 0.94 |
| mean_lookback | 20 | 6912 | 27.4% | -0.19 | 0.33 | 0.8% | 51.3% | -0.21 | 106 | 1 | 1 | 0.00 |
| mean_lookback | 30 | 6912 | 26.0% | -0.22 | 0.35 | 1.2% | 63.0% | -0.21 | 175 | 43 | 13 | 0.18 |
| mean_lookback | 40 | 6912 | 27.4% | -0.18 | 0.35 | 1.8% | 71.5% | -0.18 | 231 | 82 | 13 | 0.36 |
| mean_lookback | 50 | 6912 | 27.8% | -0.18 | 0.36 | 2.0% | 74.6% | -0.20 | 267 | 125 | 34 | 2.46 |
| mean_lookback | 60 | 6912 | 28.4% | -0.14 | 0.38 | 1.2% | 76.4% | -0.14 | 307 | 77 | 6 | 2.04 |
| mean_lookback | 80 | 6912 | 27.0% | -0.19 | 0.35 | 0.7% | 77.2% | -0.21 | 335 | 49 | 8 | 0.96 |
| std_lookback | 10 | 5184 | 23.3% | -0.20 | 0.29 | 0.6% | 91.2% | -0.23 | 526 | 7 | 1 | 0.16 |
| std_lookback | 15 | 5184 | 20.2% | -0.33 | 0.31 | 0.5% | 80.8% | -0.31 | 418 | 20 | 11 | 0.00 |
| std_lookback | 20 | 5184 | 30.8% | -0.21 | 0.54 | 5.0% | 76.5% | -0.20 | 339 | 241 | 38 | 6.56 |
| std_lookback | 25 | 5184 | 26.1% | -0.26 | 0.37 | 1.0% | 71.5% | -0.21 | 251 | 36 | 7 | 0.08 |
| std_lookback | 30 | 5184 | 24.8% | -0.21 | 0.34 | 1.5% | 67.6% | -0.17 | 215 | 32 | 9 | 0.32 |
| std_lookback | 40 | 5184 | 29.3% | -0.10 | 0.31 | 0.8% | 62.8% | -0.08 | 173 | 4 | 0 | 0.00 |
| std_lookback | 60 | 5184 | 31.7% | -0.10 | 0.33 | 0.3% | 54.7% | -0.14 | 121 | 11 | 3 | 0.00 |
| std_lookback | 80 | 5184 | 32.4% | -0.11 | 0.35 | 0.7% | 46.9% | -0.13 | 88 | 26 | 6 | 0.88 |
| entry_z | -2.0 | 13824 | 26.3% | -0.18 | 0.33 | 1.1% | 82.8% | -0.19 | 379 | 141 | 31 | 0.93 |
| entry_z | -2.5 | 13824 | 26.3% | -0.19 | 0.33 | 1.2% | 68.5% | -0.21 | 217 | 101 | 17 | 0.60 |
| entry_z | -3.0 | 13824 | 29.4% | -0.17 | 0.40 | 1.6% | 55.7% | -0.17 | 123 | 135 | 27 | 1.47 |
| exit_z | -1.0 | 10368 | 25.6% | -0.21 | 0.33 | 1.3% | 69.2% | -0.22 | 222 | 92 | 17 | 0.84 |
| exit_z | -0.5 | 10368 | 27.4% | -0.18 | 0.35 | 1.3% | 69.0% | -0.19 | 220 | 99 | 20 | 1.08 |
| exit_z | 0.0 | 10368 | 28.0% | -0.17 | 0.36 | 1.3% | 68.9% | -0.18 | 220 | 93 | 22 | 1.08 |
| exit_z | 0.5 | 10368 | 28.3% | -0.17 | 0.36 | 1.3% | 68.9% | -0.17 | 219 | 93 | 16 | 1.00 |
| max_holding_bars | 5 | 20736 | 28.2% | -0.20 | 0.37 | 1.8% | 69.3% | -0.22 | 221 | 267 | 42 | 1.26 |
| max_holding_bars | 10 | 20736 | 26.5% | -0.17 | 0.34 | 0.8% | 68.8% | -0.17 | 220 | 110 | 33 | 0.74 |
| entry_confirmation | none | 20736 | 23.7% | -0.18 | 0.27 | 0.1% | 82.0% | -0.18 | 377 | 19 | 2 | 0.00 |
| entry_confirmation | positive_bar_return | 20736 | 30.9% | -0.18 | 0.45 | 2.5% | 56.0% | -0.22 | 124 | 358 | 73 | 2.00 |
| stop_atr_multiple | none | 13824 | 22.1% | -0.24 | 0.29 | 0.6% | 63.3% | -0.28 | 180 | 45 | 5 | 0.06 |
| stop_atr_multiple | 1.0 | 13824 | 31.2% | -0.16 | 0.41 | 2.0% | 74.2% | -0.16 | 263 | 224 | 55 | 1.98 |
| stop_atr_multiple | 2.0 | 13824 | 28.7% | -0.14 | 0.35 | 1.3% | 69.5% | -0.15 | 210 | 108 | 15 | 0.96 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 5min | sma | 40 | 10 | -2.0 | -1.0 | 10 | positive_bar_return | none | 1235 | 207.6% | 1.34 | -12.1% | s6 deduplicated |
| 2 | 15min | sma | 80 | 80 | -2.0 | 0.0 | 5 | positive_bar_return | 1.0 | 263 | 53.9% | 1.30 | -5.9% | s7 pass |
| 3 | 15min | sma | 80 | 80 | -2.0 | 0.5 | 5 | positive_bar_return | 1.0 | 263 | 53.9% | 1.30 | -5.9% | s7 pass |
| 4 | 15min | sma | 80 | 80 | -2.0 | -0.5 | 5 | positive_bar_return | 1.0 | 263 | 53.8% | 1.30 | -6.2% | s6 deduplicated |
| 5 | 15min | sma | 50 | 20 | -3.0 | 0.0 | 10 | positive_bar_return | 1.0 | 352 | 155.8% | 1.22 | -14.7% | s7 pass |
| 6 | 15min | sma | 50 | 20 | -3.0 | -0.5 | 10 | positive_bar_return | 1.0 | 352 | 157.7% | 1.22 | -14.7% | s7 pass |
| 7 | 15min | sma | 80 | 80 | -2.0 | -1.0 | 5 | positive_bar_return | 1.0 | 263 | 46.6% | 1.18 | -6.4% | s6 deduplicated |
| 8 | 15min | ema | 60 | 20 | -3.0 | -0.5 | 10 | positive_bar_return | 2.0 | 238 | 166.5% | 1.18 | -15.7% | s6 deduplicated |
| 9 | 15min | sma | 50 | 20 | -3.0 | 0.5 | 10 | positive_bar_return | 1.0 | 352 | 146.2% | 1.18 | -14.7% | s6 deduplicated |
| 10 | 15min | ema | 60 | 20 | -3.0 | 0.0 | 10 | positive_bar_return | 2.0 | 238 | 162.9% | 1.18 | -15.4% | s6 deduplicated |
| 11 | 15min | ema | 60 | 20 | -3.0 | -0.5 | 5 | positive_bar_return | 2.0 | 244 | 190.2% | 1.17 | -12.2% | s6 deduplicated |
| 12 | 15min | ema | 60 | 20 | -3.0 | -1.0 | 5 | positive_bar_return | 2.0 | 244 | 190.4% | 1.17 | -12.3% | s6 deduplicated |
| 13 | 15min | ema | 60 | 20 | -3.0 | 0.0 | 5 | positive_bar_return | 2.0 | 244 | 183.9% | 1.15 | -12.3% | s6 deduplicated |
| 14 | 15min | ema | 60 | 20 | -3.0 | 0.5 | 10 | positive_bar_return | 2.0 | 238 | 161.5% | 1.15 | -15.3% | s6 deduplicated |
| 15 | 15min | sma | 50 | 20 | -3.0 | -1.0 | 10 | positive_bar_return | 1.0 | 353 | 172.8% | 1.15 | -14.8% | s6 deduplicated |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
