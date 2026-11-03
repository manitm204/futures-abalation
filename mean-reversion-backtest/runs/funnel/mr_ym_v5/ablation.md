# Ablation (development only) -- mr_ym_v5

- Symbol YM, strategy `mean_reversion_v5`, 41,472 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 29,921 configs (72.1%).
- Grid-wide: 30.7% profitable, median dev Sharpe -0.24, 661 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 41472 | 41472 |  |
| 1 backtest integrity | 41472 | 41472 |  |
| 2 trade count & coverage | 41472 | 29921 |  |
| 3 performance & risk | 29921 | 127 |  |
| 4 parameter stability | 127 | 122 |  |
| 5 time stability | 122 | 121 |  |
| 6 deduplication | 121 | 61 | best 2 per cluster |
| 7 execution stress | 61 | 61 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 61 |  | diagnostic only: unverified: 61 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| timeframe | 0.864 |
| std_lookback | 0.246 |
| max_holding_bars | 0.157 |
| entry_z | 0.148 |
| stop_atr_multiple | 0.148 |
| mean_lookback | 0.052 |
| mean_type | 0.042 |
| entry_confirmation | 0.031 |
| exit_z | 0.018 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 5min | 13824 | 7.0% | -0.70 | -0.06 | 0.0% | 95.1% | -0.70 | 1007 | 0 | 0 | 0.00 |
| timeframe | 15min | 13824 | 23.1% | -0.25 | 0.25 | 0.3% | 81.6% | -0.22 | 329 | 36 | 14 | 0.93 |
| timeframe | 1h | 13824 | 62.0% | 0.17 | 0.61 | 4.5% | 39.8% | 0.06 | 76 | 91 | 47 | 2.07 |
| mean_type | sma | 20736 | 30.2% | -0.26 | 0.40 | 1.8% | 76.2% | -0.37 | 301 | 73 | 35 | 1.14 |
| mean_type | ema | 20736 | 31.3% | -0.21 | 0.42 | 1.4% | 68.1% | -0.32 | 223 | 54 | 26 | 0.86 |
| mean_lookback | 20 | 6912 | 28.7% | -0.26 | 0.36 | 1.2% | 54.0% | -0.42 | 117 | 10 | 9 | 0.48 |
| mean_lookback | 30 | 6912 | 31.1% | -0.26 | 0.47 | 2.6% | 64.8% | -0.38 | 197 | 22 | 12 | 1.08 |
| mean_lookback | 40 | 6912 | 33.8% | -0.22 | 0.47 | 2.1% | 73.2% | -0.35 | 263 | 44 | 14 | 2.04 |
| mean_lookback | 50 | 6912 | 32.7% | -0.22 | 0.42 | 1.6% | 77.7% | -0.34 | 320 | 18 | 5 | 0.90 |
| mean_lookback | 60 | 6912 | 29.2% | -0.25 | 0.36 | 1.4% | 80.0% | -0.34 | 352 | 8 | 6 | 0.30 |
| mean_lookback | 80 | 6912 | 28.8% | -0.21 | 0.36 | 0.6% | 83.2% | -0.29 | 395 | 25 | 15 | 1.20 |
| std_lookback | 10 | 5184 | 22.8% | -0.29 | 0.25 | 0.4% | 93.2% | -0.33 | 597 | 12 | 8 | 0.48 |
| std_lookback | 15 | 5184 | 31.7% | -0.22 | 0.44 | 2.4% | 83.1% | -0.33 | 468 | 36 | 22 | 2.08 |
| std_lookback | 20 | 5184 | 38.3% | -0.12 | 0.46 | 2.6% | 78.7% | -0.20 | 375 | 53 | 19 | 3.84 |
| std_lookback | 25 | 5184 | 34.6% | -0.16 | 0.42 | 1.1% | 73.1% | -0.24 | 296 | 12 | 3 | 0.80 |
| std_lookback | 30 | 5184 | 22.6% | -0.32 | 0.30 | 0.9% | 69.0% | -0.43 | 238 | 2 | 0 | 0.00 |
| std_lookback | 40 | 5184 | 27.9% | -0.36 | 0.41 | 0.9% | 65.0% | -0.54 | 189 | 3 | 3 | 0.24 |
| std_lookback | 60 | 5184 | 36.5% | -0.19 | 0.49 | 2.4% | 59.5% | -0.35 | 142 | 7 | 5 | 0.56 |
| std_lookback | 80 | 5184 | 31.4% | -0.20 | 0.42 | 1.9% | 55.7% | -0.31 | 121 | 2 | 1 | 0.00 |
| entry_z | -2.0 | 13824 | 28.6% | -0.32 | 0.43 | 2.2% | 86.3% | -0.43 | 444 | 71 | 34 | 1.68 |
| entry_z | -2.5 | 13824 | 31.6% | -0.23 | 0.42 | 1.1% | 71.9% | -0.34 | 255 | 28 | 16 | 0.51 |
| entry_z | -3.0 | 13824 | 32.0% | -0.17 | 0.38 | 1.4% | 58.2% | -0.25 | 144 | 28 | 11 | 0.81 |
| exit_z | -1.0 | 10368 | 30.6% | -0.25 | 0.42 | 1.7% | 72.3% | -0.35 | 260 | 43 | 25 | 1.28 |
| exit_z | -0.5 | 10368 | 31.4% | -0.23 | 0.42 | 1.7% | 72.2% | -0.34 | 258 | 36 | 15 | 1.08 |
| exit_z | 0.0 | 10368 | 30.6% | -0.24 | 0.41 | 1.5% | 72.1% | -0.35 | 257 | 25 | 11 | 0.80 |
| exit_z | 0.5 | 10368 | 30.4% | -0.23 | 0.40 | 1.5% | 72.0% | -0.35 | 256 | 23 | 10 | 0.84 |
| max_holding_bars | 5 | 20736 | 27.8% | -0.32 | 0.42 | 2.1% | 72.4% | -0.44 | 260 | 92 | 37 | 1.54 |
| max_holding_bars | 10 | 20736 | 33.6% | -0.16 | 0.40 | 1.1% | 71.9% | -0.26 | 257 | 35 | 24 | 0.46 |
| entry_confirmation | none | 20736 | 29.2% | -0.22 | 0.35 | 0.8% | 85.9% | -0.31 | 437 | 27 | 23 | 0.34 |
| entry_confirmation | positive_bar_return | 20736 | 32.3% | -0.25 | 0.47 | 2.4% | 58.4% | -0.43 | 140 | 100 | 38 | 1.66 |
| stop_atr_multiple | none | 13824 | 33.9% | -0.17 | 0.44 | 2.0% | 67.6% | -0.26 | 203 | 25 | 13 | 0.66 |
| stop_atr_multiple | 1.0 | 13824 | 29.0% | -0.31 | 0.42 | 1.8% | 76.1% | -0.42 | 323 | 73 | 31 | 1.68 |
| stop_atr_multiple | 2.0 | 13824 | 29.2% | -0.26 | 0.37 | 1.0% | 72.7% | -0.37 | 247 | 29 | 17 | 0.66 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 1h | sma | 30 | 20 | -2.0 | -1.0 | 5 | positive_bar_return | 1.0 | 102 | 59.2% | 1.40 | -6.9% | s7 pass |
| 2 | 1h | sma | 30 | 20 | -2.0 | 0.0 | 5 | positive_bar_return | 1.0 | 102 | 56.3% | 1.38 | -7.1% | s6 deduplicated |
| 3 | 1h | sma | 30 | 20 | -2.0 | -0.5 | 5 | positive_bar_return | 1.0 | 102 | 55.2% | 1.37 | -7.1% | s6 deduplicated |
| 4 | 1h | sma | 30 | 20 | -2.0 | 0.5 | 5 | positive_bar_return | 1.0 | 102 | 54.3% | 1.34 | -7.1% | s6 deduplicated |
| 5 | 15min | ema | 40 | 20 | -3.0 | -1.0 | 5 | positive_bar_return | 2.0 | 111 | 22.8% | 1.27 | -2.7% | s7 pass |
| 6 | 1h | sma | 30 | 20 | -2.0 | -1.0 | 10 | positive_bar_return | 1.0 | 107 | 53.3% | 1.20 | -10.1% | s7 pass |
| 7 | 1h | ema | 40 | 20 | -2.0 | -1.0 | 5 | positive_bar_return | 1.0 | 105 | 44.8% | 1.19 | -5.4% | s6 deduplicated |
| 8 | 1h | ema | 40 | 20 | -2.0 | 0.5 | 5 | positive_bar_return | 1.0 | 102 | 45.9% | 1.19 | -5.2% | s6 deduplicated |
| 9 | 1h | ema | 40 | 20 | -2.0 | 0.0 | 5 | positive_bar_return | 1.0 | 102 | 45.2% | 1.18 | -5.3% | s6 deduplicated |
| 10 | 15min | ema | 40 | 20 | -3.0 | -1.0 | 5 | positive_bar_return | none | 102 | 21.8% | 1.17 | -3.1% | s6 deduplicated |
| 11 | 1h | ema | 40 | 20 | -2.0 | -0.5 | 5 | positive_bar_return | 1.0 | 103 | 45.8% | 1.17 | -5.4% | s7 pass |
| 12 | 15min | ema | 40 | 20 | -3.0 | -0.5 | 5 | positive_bar_return | 2.0 | 110 | 18.9% | 1.14 | -2.9% | s7 pass |
| 13 | 15min | ema | 40 | 20 | -3.0 | 0.5 | 5 | positive_bar_return | 2.0 | 110 | 17.9% | 1.13 | -3.0% | s6 deduplicated |
| 14 | 15min | ema | 40 | 20 | -3.0 | 0.0 | 5 | positive_bar_return | 2.0 | 110 | 17.7% | 1.11 | -2.8% | s6 deduplicated |
| 15 | 15min | ema | 40 | 20 | -3.0 | -1.0 | 5 | positive_bar_return | 1.0 | 121 | 13.5% | 1.08 | -2.0% | s7 pass |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
