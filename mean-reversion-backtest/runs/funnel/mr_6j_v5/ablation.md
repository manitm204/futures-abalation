# Ablation (development only) -- mr_6j_v5

- Symbol 6J, strategy `mean_reversion_v5`, 41,472 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 32,801 configs (79.1%).
- Grid-wide: 7.7% profitable, median dev Sharpe -1.24, 132 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 41472 | 41472 |  |
| 1 backtest integrity | 41472 | 41472 |  |
| 2 trade count & coverage | 41472 | 32801 |  |
| 3 performance & risk | 32801 | 0 |  |
| 4 parameter stability | 0 | 0 |  |
| 5 time stability | 0 | 0 |  |
| 6 deduplication | 0 | 0 | best 2 per cluster |
| 7 execution stress | 0 | 0 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 0 |  | diagnostic only:  |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| timeframe | 1.933 |
| std_lookback | 0.626 |
| entry_z | 0.326 |
| entry_confirmation | 0.311 |
| stop_atr_multiple | 0.273 |
| mean_lookback | 0.216 |
| max_holding_bars | 0.196 |
| exit_z | 0.108 |
| mean_type | 0.005 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 5min | 13824 | 0.2% | -2.34 | -1.30 | 0.0% | 98.7% | -2.35 | 1239 | 0 | 0 | 0.00 |
| timeframe | 15min | 13824 | 1.6% | -1.31 | -0.56 | 0.0% | 87.2% | -1.39 | 453 | 0 | 0 | 0.21 |
| timeframe | 1h | 13824 | 21.1% | -0.41 | 0.34 | 1.0% | 51.4% | -0.57 | 104 | 0 | 0 | 2.79 |
| mean_type | sma | 20736 | 7.6% | -1.24 | -0.09 | 0.2% | 81.1% | -1.48 | 377 | 0 | 0 | 1.70 |
| mean_type | ema | 20736 | 7.7% | -1.24 | -0.11 | 0.5% | 77.1% | -1.51 | 320 | 0 | 0 | 0.30 |
| mean_lookback | 20 | 6912 | 13.4% | -1.11 | 0.18 | 0.6% | 61.1% | -1.48 | 167 | 0 | 0 | 0.72 |
| mean_lookback | 30 | 6912 | 9.5% | -1.20 | -0.02 | 0.6% | 74.1% | -1.50 | 278 | 0 | 0 | 0.06 |
| mean_lookback | 40 | 6912 | 8.6% | -1.24 | -0.05 | 0.2% | 79.6% | -1.50 | 361 | 0 | 0 | 1.32 |
| mean_lookback | 50 | 6912 | 5.9% | -1.27 | -0.16 | 0.3% | 83.1% | -1.50 | 438 | 0 | 0 | 1.38 |
| mean_lookback | 60 | 6912 | 6.2% | -1.33 | -0.17 | 0.1% | 86.5% | -1.52 | 485 | 0 | 0 | 1.98 |
| mean_lookback | 80 | 6912 | 2.3% | -1.31 | -0.40 | 0.0% | 90.1% | -1.45 | 516 | 0 | 0 | 0.54 |
| std_lookback | 10 | 5184 | 1.8% | -1.55 | -0.37 | 0.0% | 98.6% | -1.58 | 748 | 0 | 0 | 1.44 |
| std_lookback | 15 | 5184 | 5.4% | -1.57 | -0.24 | 0.0% | 93.8% | -1.67 | 653 | 0 | 0 | 3.68 |
| std_lookback | 20 | 5184 | 3.6% | -1.30 | -0.23 | 0.0% | 88.4% | -1.47 | 548 | 0 | 0 | 0.96 |
| std_lookback | 25 | 5184 | 8.6% | -1.13 | -0.07 | 0.2% | 83.3% | -1.32 | 451 | 0 | 0 | 0.40 |
| std_lookback | 30 | 5184 | 12.4% | -1.37 | 0.12 | 1.2% | 79.0% | -1.63 | 344 | 0 | 0 | 0.88 |
| std_lookback | 40 | 5184 | 15.4% | -1.35 | 0.26 | 0.9% | 71.0% | -1.61 | 255 | 0 | 0 | 0.64 |
| std_lookback | 60 | 5184 | 10.7% | -1.07 | 0.03 | 0.3% | 62.9% | -1.34 | 175 | 0 | 0 | 0.00 |
| std_lookback | 80 | 5184 | 3.5% | -0.94 | -0.22 | 0.0% | 55.7% | -1.38 | 121 | 0 | 0 | 0.00 |
| entry_z | -2.0 | 13824 | 5.2% | -1.40 | -0.24 | 0.3% | 89.4% | -1.53 | 532 | 0 | 0 | 1.62 |
| entry_z | -2.5 | 13824 | 8.0% | -1.24 | -0.08 | 0.3% | 79.3% | -1.49 | 340 | 0 | 0 | 0.93 |
| entry_z | -3.0 | 13824 | 9.7% | -1.07 | 0.01 | 0.3% | 68.6% | -1.45 | 220 | 0 | 0 | 0.45 |
| exit_z | -1.0 | 10368 | 7.1% | -1.29 | -0.13 | 0.4% | 79.1% | -1.56 | 346 | 0 | 0 | 0.72 |
| exit_z | -0.5 | 10368 | 7.6% | -1.26 | -0.10 | 0.3% | 79.1% | -1.51 | 343 | 0 | 0 | 0.76 |
| exit_z | 0.0 | 10368 | 7.8% | -1.23 | -0.09 | 0.3% | 79.1% | -1.48 | 343 | 0 | 0 | 1.08 |
| exit_z | 0.5 | 10368 | 8.1% | -1.18 | -0.07 | 0.3% | 79.1% | -1.43 | 342 | 0 | 0 | 1.44 |
| max_holding_bars | 5 | 20736 | 6.9% | -1.33 | -0.16 | 0.3% | 79.2% | -1.60 | 341 | 0 | 0 | 1.08 |
| max_holding_bars | 10 | 20736 | 8.4% | -1.13 | -0.05 | 0.4% | 79.0% | -1.40 | 345 | 0 | 0 | 0.92 |
| entry_confirmation | none | 20736 | 2.9% | -1.40 | -0.34 | 0.0% | 87.3% | -1.58 | 550 | 0 | 0 | 0.54 |
| entry_confirmation | positive_bar_return | 20736 | 12.4% | -1.09 | 0.12 | 0.6% | 70.8% | -1.42 | 217 | 0 | 0 | 1.46 |
| stop_atr_multiple | none | 13824 | 8.0% | -1.13 | -0.07 | 0.3% | 76.1% | -1.40 | 286 | 0 | 0 | 1.80 |
| stop_atr_multiple | 1.0 | 13824 | 7.5% | -1.40 | -0.12 | 0.2% | 81.5% | -1.69 | 405 | 0 | 0 | 0.60 |
| stop_atr_multiple | 2.0 | 13824 | 7.5% | -1.22 | -0.10 | 0.4% | 79.7% | -1.45 | 331 | 0 | 0 | 0.60 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 1h | sma | 50 | 30 | -2.5 | 0.5 | 10 | positive_bar_return | 1.0 | 101 | 7.8% | 0.62 | -3.4% | s3 hard_reject |
| 2 | 1h | sma | 50 | 30 | -2.5 | 0.0 | 10 | positive_bar_return | 1.0 | 101 | 7.5% | 0.62 | -3.5% | s3 hard_reject |
| 3 | 1h | sma | 50 | 15 | -2.0 | -1.0 | 5 | positive_bar_return | none | 145 | 6.0% | 0.50 | -5.6% | s3 hard_reject |
| 4 | 1h | sma | 50 | 30 | -2.5 | -0.5 | 10 | positive_bar_return | 1.0 | 101 | 5.9% | 0.50 | -4.2% | s3 hard_reject |
| 5 | 1h | sma | 50 | 15 | -2.0 | 0.5 | 5 | positive_bar_return | none | 142 | 5.7% | 0.47 | -5.4% | s3 hard_reject |
| 6 | 1h | sma | 60 | 20 | -2.5 | 0.0 | 10 | positive_bar_return | none | 104 | 5.4% | 0.47 | -3.1% | s3 hard_reject |
| 7 | 1h | sma | 60 | 20 | -2.5 | -0.5 | 10 | positive_bar_return | none | 105 | 5.2% | 0.46 | -3.2% | s3 hard_reject |
| 8 | 1h | sma | 50 | 15 | -2.0 | 0.0 | 5 | positive_bar_return | none | 142 | 5.5% | 0.46 | -5.4% | s3 hard_reject |
| 9 | 1h | sma | 60 | 20 | -2.5 | 0.5 | 10 | positive_bar_return | none | 103 | 5.1% | 0.45 | -3.2% | s3 hard_reject |
| 10 | 1h | sma | 50 | 30 | -2.5 | -1.0 | 10 | positive_bar_return | 1.0 | 101 | 5.2% | 0.44 | -4.2% | s3 hard_reject |
| 11 | 1h | sma | 50 | 15 | -2.0 | -0.5 | 5 | positive_bar_return | none | 143 | 5.3% | 0.44 | -5.4% | s3 hard_reject |
| 12 | 15min | ema | 20 | 15 | -2.5 | -1.0 | 5 | positive_bar_return | none | 115 | 1.4% | 0.44 | -0.9% | s3 hard_reject |
| 13 | 1h | sma | 20 | 15 | -2.0 | 0.0 | 10 | positive_bar_return | 1.0 | 108 | 4.6% | 0.42 | -2.9% | s3 hard_reject |
| 14 | 1h | sma | 60 | 40 | -2.5 | 0.5 | 5 | none | none | 120 | 4.8% | 0.42 | -4.8% | s3 hard_reject |
| 15 | 1h | sma | 60 | 40 | -2.5 | -1.0 | 5 | none | none | 120 | 4.5% | 0.41 | -4.9% | s3 hard_reject |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
