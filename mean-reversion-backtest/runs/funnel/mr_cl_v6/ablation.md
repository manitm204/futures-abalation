# Ablation (development only) -- mr_cl_v6

- Symbol CL, strategy `mean_reversion_v9`, 17,280 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 15,777 configs (91.3%).
- Grid-wide: 46.9% profitable, median dev Sharpe 0.05, 930 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 17280 | 17280 |  |
| 1 backtest integrity | 17280 | 17280 |  |
| 2 trade count & coverage | 17280 | 15777 |  |
| 3 performance & risk | 15777 | 674 |  |
| 4 parameter stability | 674 | 658 |  |
| 5 time stability | 658 | 648 |  |
| 6 deduplication | 648 | 82 | best 2 per cluster |
| 7 execution stress | 82 | 82 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 82 |  | diagnostic only: unverified: 82 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| std_lookback | 0.606 |
| mean_lookback | 0.326 |
| stop_atr_multiple | 0.309 |
| entry_confirmation | 0.163 |
| entry_z | 0.132 |
| mean_type | 0.066 |
| max_holding_bars | 0.056 |
| exit_z | 0.026 |
| timeframe | 0.000 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 15min | 17280 | 46.9% | 0.05 | 0.62 | 5.4% | 91.3% | 0.03 | 393 | 674 | 82 | 1.00 |
| mean_type | sma | 8640 | 44.1% | 0.02 | 0.59 | 5.3% | 92.7% | 0.01 | 411 | 356 | 54 | 1.10 |
| mean_type | ema | 8640 | 49.6% | 0.08 | 0.63 | 5.5% | 89.9% | 0.06 | 365 | 318 | 28 | 0.90 |
| mean_lookback | 30 | 2880 | 47.9% | 0.07 | 0.66 | 6.5% | 72.7% | 0.00 | 263 | 55 | 12 | 0.06 |
| mean_lookback | 40 | 2880 | 51.6% | 0.10 | 0.68 | 6.5% | 86.0% | 0.05 | 366 | 110 | 16 | 0.00 |
| mean_lookback | 50 | 2880 | 50.7% | 0.09 | 0.69 | 7.7% | 93.2% | 0.08 | 409 | 194 | 29 | 2.04 |
| mean_lookback | 60 | 2880 | 56.7% | 0.15 | 0.63 | 6.0% | 96.2% | 0.16 | 431 | 157 | 6 | 2.40 |
| mean_lookback | 80 | 2880 | 45.4% | 0.03 | 0.56 | 3.6% | 99.7% | 0.02 | 420 | 103 | 8 | 1.02 |
| mean_lookback | 100 | 2880 | 28.9% | -0.17 | 0.41 | 1.9% | 100.0% | -0.17 | 398 | 55 | 11 | 0.48 |
| std_lookback | 10 | 3456 | 13.3% | -0.27 | 0.14 | 0.0% | 100.0% | -0.27 | 511 | 0 | 0 | 0.00 |
| std_lookback | 15 | 3456 | 36.3% | -0.05 | 0.47 | 1.1% | 98.6% | -0.04 | 448 | 33 | 4 | 0.40 |
| std_lookback | 20 | 3456 | 67.7% | 0.33 | 0.80 | 13.3% | 93.7% | 0.35 | 394 | 438 | 42 | 3.55 |
| std_lookback | 25 | 3456 | 61.3% | 0.17 | 0.63 | 5.6% | 85.3% | 0.16 | 309 | 122 | 18 | 0.55 |
| std_lookback | 30 | 3456 | 55.8% | 0.13 | 0.66 | 6.9% | 78.9% | 0.08 | 256 | 81 | 18 | 0.50 |
| entry_z | -2.0 | 4320 | 37.4% | -0.03 | 0.53 | 3.6% | 100.0% | -0.03 | 521 | 152 | 29 | 0.16 |
| entry_z | -2.5 | 4320 | 47.2% | 0.06 | 0.59 | 4.5% | 95.4% | 0.04 | 425 | 141 | 16 | 0.40 |
| entry_z | -3.0 | 4320 | 52.4% | 0.10 | 0.63 | 6.2% | 89.8% | 0.08 | 341 | 182 | 21 | 1.48 |
| entry_z | -3.5 | 4320 | 50.4% | 0.09 | 0.69 | 7.2% | 80.0% | 0.07 | 263 | 199 | 16 | 1.96 |
| exit_z | -1.0 | 4320 | 45.5% | 0.03 | 0.61 | 5.5% | 91.3% | 0.02 | 394 | 169 | 15 | 0.92 |
| exit_z | -0.5 | 4320 | 46.7% | 0.05 | 0.62 | 5.4% | 91.3% | 0.03 | 392 | 171 | 17 | 1.04 |
| exit_z | 0.0 | 4320 | 47.7% | 0.06 | 0.62 | 5.3% | 91.3% | 0.04 | 392 | 165 | 25 | 1.04 |
| exit_z | 0.5 | 4320 | 47.6% | 0.06 | 0.62 | 5.4% | 91.3% | 0.04 | 392 | 169 | 25 | 1.00 |
| max_holding_bars | 3 | 5760 | 44.8% | 0.01 | 0.62 | 5.2% | 91.3% | -0.02 | 394 | 164 | 8 | 0.81 |
| max_holding_bars | 5 | 5760 | 47.8% | 0.06 | 0.65 | 6.9% | 91.4% | 0.04 | 395 | 312 | 33 | 1.41 |
| max_holding_bars | 8 | 5760 | 48.0% | 0.07 | 0.60 | 4.1% | 91.2% | 0.06 | 388 | 198 | 41 | 0.78 |
| entry_confirmation | none | 8640 | 39.0% | -0.02 | 0.45 | 1.8% | 97.9% | -0.03 | 523 | 75 | 6 | 0.02 |
| entry_confirmation | positive_bar_return | 8640 | 54.7% | 0.14 | 0.73 | 9.0% | 84.7% | 0.13 | 301 | 599 | 76 | 1.98 |
| stop_atr_multiple | none | 5760 | 31.5% | -0.12 | 0.47 | 2.3% | 90.3% | -0.14 | 329 | 74 | 0 | 0.24 |
| stop_atr_multiple | 1.0 | 5760 | 59.4% | 0.19 | 0.72 | 8.7% | 92.2% | 0.18 | 494 | 402 | 60 | 1.35 |
| stop_atr_multiple | 2.0 | 5760 | 49.7% | 0.08 | 0.60 | 5.2% | 91.3% | 0.06 | 385 | 198 | 22 | 1.41 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 15min | sma | 60 | 20 | -3.5 | -1.0 | 5 | positive_bar_return | 2.0 | 235 | 251.9% | 1.38 | -12.5% | s7 pass |
| 2 | 15min | sma | 60 | 20 | -3.5 | 0.5 | 5 | positive_bar_return | 2.0 | 235 | 249.8% | 1.37 | -12.6% | s7 pass |
| 3 | 15min | sma | 60 | 20 | -3.5 | -0.5 | 5 | positive_bar_return | 2.0 | 235 | 242.6% | 1.35 | -12.5% | s6 deduplicated |
| 4 | 15min | sma | 60 | 20 | -3.5 | 0.0 | 5 | positive_bar_return | 2.0 | 235 | 241.9% | 1.35 | -12.5% | s6 deduplicated |
| 5 | 15min | sma | 60 | 20 | -3.5 | 0.5 | 8 | positive_bar_return | 1.0 | 317 | 198.1% | 1.27 | -13.9% | s7 pass |
| 6 | 15min | sma | 60 | 20 | -3.5 | -1.0 | 8 | positive_bar_return | 1.0 | 317 | 193.3% | 1.25 | -14.0% | s7 pass |
| 7 | 15min | sma | 60 | 20 | -3.5 | -0.5 | 8 | positive_bar_return | 1.0 | 317 | 189.0% | 1.24 | -14.0% | s6 deduplicated |
| 8 | 15min | sma | 60 | 20 | -3.5 | 0.0 | 8 | positive_bar_return | 1.0 | 317 | 186.9% | 1.23 | -14.0% | s6 deduplicated |
| 9 | 15min | sma | 60 | 20 | -3.5 | -0.5 | 3 | positive_bar_return | 2.0 | 231 | 157.7% | 1.23 | -10.7% | s6 deduplicated |
| 10 | 15min | sma | 60 | 20 | -3.5 | -1.0 | 3 | positive_bar_return | 2.0 | 231 | 157.0% | 1.22 | -10.7% | s6 deduplicated |
| 11 | 15min | sma | 60 | 20 | -3.5 | -1.0 | 8 | positive_bar_return | 2.0 | 242 | 198.1% | 1.22 | -15.3% | s6 deduplicated |
| 12 | 15min | sma | 60 | 20 | -3.5 | 0.0 | 3 | positive_bar_return | 2.0 | 231 | 155.4% | 1.21 | -10.7% | s6 deduplicated |
| 13 | 15min | sma | 60 | 20 | -3.5 | 0.5 | 8 | positive_bar_return | 2.0 | 242 | 195.4% | 1.21 | -15.4% | s6 deduplicated |
| 14 | 15min | sma | 60 | 20 | -3.5 | 0.5 | 3 | positive_bar_return | 2.0 | 231 | 155.3% | 1.21 | -10.7% | s6 deduplicated |
| 15 | 15min | sma | 60 | 20 | -3.5 | 0.5 | 5 | positive_bar_return | 1.0 | 314 | 185.9% | 1.20 | -12.3% | s6 deduplicated |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
