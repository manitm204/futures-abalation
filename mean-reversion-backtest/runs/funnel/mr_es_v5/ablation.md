# Ablation (development only) -- mr_es_v5

- Symbol ES, strategy `mean_reversion_v5`, 41,472 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 29,426 configs (71.0%).
- Grid-wide: 20.6% profitable, median dev Sharpe -0.44, 262 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 41472 | 41472 |  |
| 1 backtest integrity | 41472 | 41472 |  |
| 2 trade count & coverage | 41472 | 29426 |  |
| 3 performance & risk | 29426 | 88 |  |
| 4 parameter stability | 88 | 80 |  |
| 5 time stability | 80 | 80 |  |
| 6 deduplication | 80 | 45 | best 2 per cluster |
| 7 execution stress | 45 | 45 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 45 |  | diagnostic only: unverified: 45 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| timeframe | 0.989 |
| std_lookback | 0.273 |
| stop_atr_multiple | 0.209 |
| entry_z | 0.179 |
| max_holding_bars | 0.064 |
| mean_lookback | 0.058 |
| mean_type | 0.036 |
| exit_z | 0.020 |
| entry_confirmation | 0.007 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 5min | 13824 | 2.9% | -0.99 | -0.30 | 0.0% | 93.8% | -1.01 | 955 | 0 | 0 | 0.00 |
| timeframe | 15min | 13824 | 13.8% | -0.45 | 0.11 | 0.3% | 80.9% | -0.47 | 316 | 36 | 14 | 1.26 |
| timeframe | 1h | 13824 | 45.3% | -0.00 | 0.47 | 1.6% | 38.2% | -0.02 | 74 | 52 | 31 | 1.74 |
| mean_type | sma | 20736 | 20.9% | -0.46 | 0.26 | 0.7% | 75.3% | -0.60 | 292 | 63 | 37 | 1.38 |
| mean_type | ema | 20736 | 20.4% | -0.43 | 0.26 | 0.5% | 66.6% | -0.58 | 208 | 25 | 8 | 0.62 |
| mean_lookback | 20 | 6912 | 14.8% | -0.47 | 0.16 | 0.5% | 52.3% | -0.64 | 111 | 3 | 3 | 0.18 |
| mean_lookback | 30 | 6912 | 21.1% | -0.46 | 0.32 | 1.2% | 63.7% | -0.62 | 183 | 23 | 11 | 1.44 |
| mean_lookback | 40 | 6912 | 25.1% | -0.41 | 0.37 | 1.0% | 71.6% | -0.59 | 248 | 27 | 15 | 1.62 |
| mean_lookback | 50 | 6912 | 23.7% | -0.42 | 0.33 | 0.9% | 76.9% | -0.56 | 309 | 24 | 11 | 1.74 |
| mean_lookback | 60 | 6912 | 21.2% | -0.43 | 0.23 | 0.1% | 79.2% | -0.56 | 341 | 2 | 2 | 0.30 |
| mean_lookback | 80 | 6912 | 18.0% | -0.45 | 0.16 | 0.1% | 82.1% | -0.58 | 371 | 9 | 3 | 0.72 |
| std_lookback | 10 | 5184 | 16.5% | -0.59 | 0.20 | 0.7% | 92.1% | -0.65 | 557 | 10 | 6 | 0.88 |
| std_lookback | 15 | 5184 | 20.6% | -0.45 | 0.27 | 0.5% | 82.2% | -0.56 | 426 | 11 | 7 | 0.96 |
| std_lookback | 20 | 5184 | 27.0% | -0.32 | 0.40 | 2.0% | 76.5% | -0.46 | 351 | 40 | 16 | 3.28 |
| std_lookback | 25 | 5184 | 21.7% | -0.36 | 0.29 | 0.3% | 72.4% | -0.46 | 286 | 12 | 6 | 1.44 |
| std_lookback | 30 | 5184 | 15.8% | -0.48 | 0.17 | 0.0% | 68.0% | -0.66 | 224 | 2 | 1 | 0.16 |
| std_lookback | 40 | 5184 | 22.3% | -0.48 | 0.27 | 0.4% | 63.7% | -0.68 | 185 | 1 | 1 | 0.08 |
| std_lookback | 60 | 5184 | 18.9% | -0.45 | 0.19 | 0.3% | 58.3% | -0.59 | 138 | 0 | 0 | 0.00 |
| std_lookback | 80 | 5184 | 22.2% | -0.40 | 0.30 | 0.9% | 54.5% | -0.61 | 117 | 12 | 8 | 1.20 |
| entry_z | -2.0 | 13824 | 19.1% | -0.56 | 0.26 | 0.7% | 85.9% | -0.67 | 425 | 45 | 26 | 1.53 |
| entry_z | -2.5 | 13824 | 20.4% | -0.42 | 0.23 | 0.5% | 71.1% | -0.56 | 245 | 19 | 7 | 0.60 |
| entry_z | -3.0 | 13824 | 22.4% | -0.38 | 0.29 | 0.7% | 56.0% | -0.51 | 133 | 24 | 12 | 0.87 |
| exit_z | -1.0 | 10368 | 20.7% | -0.45 | 0.26 | 0.7% | 71.1% | -0.59 | 250 | 21 | 13 | 0.92 |
| exit_z | -0.5 | 10368 | 20.4% | -0.45 | 0.26 | 0.7% | 71.0% | -0.60 | 247 | 22 | 11 | 1.12 |
| exit_z | 0.0 | 10368 | 20.7% | -0.44 | 0.26 | 0.6% | 70.9% | -0.59 | 247 | 21 | 10 | 0.96 |
| exit_z | 0.5 | 10368 | 20.7% | -0.43 | 0.26 | 0.5% | 70.8% | -0.58 | 246 | 24 | 11 | 1.00 |
| max_holding_bars | 5 | 20736 | 19.6% | -0.48 | 0.25 | 0.9% | 71.2% | -0.65 | 249 | 62 | 29 | 1.46 |
| max_holding_bars | 10 | 20736 | 21.7% | -0.41 | 0.27 | 0.4% | 70.7% | -0.53 | 247 | 26 | 16 | 0.54 |
| entry_confirmation | none | 20736 | 18.9% | -0.44 | 0.21 | 0.4% | 85.1% | -0.54 | 430 | 20 | 14 | 0.46 |
| entry_confirmation | positive_bar_return | 20736 | 22.4% | -0.45 | 0.31 | 0.9% | 56.8% | -0.72 | 133 | 68 | 31 | 1.54 |
| stop_atr_multiple | none | 13824 | 23.5% | -0.35 | 0.30 | 0.9% | 66.2% | -0.50 | 191 | 41 | 19 | 1.47 |
| stop_atr_multiple | 1.0 | 13824 | 17.0% | -0.56 | 0.20 | 0.3% | 75.2% | -0.69 | 312 | 19 | 9 | 0.60 |
| stop_atr_multiple | 2.0 | 13824 | 21.5% | -0.44 | 0.28 | 0.7% | 71.5% | -0.62 | 236 | 28 | 17 | 0.93 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 15min | ema | 50 | 20 | -3.0 | -0.5 | 5 | positive_bar_return | none | 164 | 32.6% | 1.20 | -2.9% | s7 pass |
| 2 | 15min | ema | 50 | 20 | -3.0 | -1.0 | 5 | positive_bar_return | none | 164 | 32.2% | 1.19 | -2.9% | s6 deduplicated |
| 3 | 15min | ema | 50 | 20 | -3.0 | 0.5 | 5 | positive_bar_return | none | 163 | 30.0% | 1.11 | -3.7% | s6 deduplicated |
| 4 | 15min | ema | 50 | 20 | -3.0 | 0.0 | 5 | positive_bar_return | none | 164 | 29.9% | 1.11 | -3.8% | s7 pass |
| 5 | 1h | sma | 30 | 15 | -2.0 | 0.0 | 5 | positive_bar_return | 2.0 | 125 | 45.0% | 1.01 | -6.2% | s7 pass |
| 6 | 1h | sma | 30 | 15 | -2.0 | 0.5 | 5 | positive_bar_return | 2.0 | 125 | 45.2% | 1.01 | -6.5% | s7 pass |
| 7 | 1h | sma | 30 | 20 | -2.0 | -0.5 | 10 | positive_bar_return | 1.0 | 107 | 37.8% | 0.99 | -4.9% | s7 pass |
| 8 | 15min | sma | 40 | 20 | -2.5 | -1.0 | 5 | positive_bar_return | none | 299 | 33.9% | 0.98 | -5.8% | s6 deduplicated |
| 9 | 15min | ema | 40 | 20 | -2.5 | -0.5 | 5 | positive_bar_return | none | 184 | 28.2% | 0.97 | -6.6% | s6 deduplicated |
| 10 | 15min | ema | 40 | 20 | -2.5 | 0.0 | 5 | positive_bar_return | none | 184 | 27.1% | 0.95 | -6.9% | s6 deduplicated |
| 11 | 15min | ema | 40 | 20 | -2.5 | 0.5 | 5 | positive_bar_return | none | 184 | 27.3% | 0.95 | -6.9% | s6 deduplicated |
| 12 | 1h | sma | 40 | 25 | -2.5 | -1.0 | 10 | none | none | 112 | 44.7% | 0.94 | -10.3% | s7 pass |
| 13 | 1h | sma | 30 | 15 | -2.0 | 0.5 | 5 | positive_bar_return | none | 110 | 40.3% | 0.94 | -8.4% | s6 deduplicated |
| 14 | 1h | sma | 40 | 10 | -3.0 | -0.5 | 5 | positive_bar_return | 2.0 | 103 | 36.2% | 0.93 | -7.4% | s7 pass |
| 15 | 15min | sma | 40 | 20 | -2.5 | -0.5 | 5 | positive_bar_return | none | 299 | 31.0% | 0.93 | -5.6% | s6 deduplicated |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
