# Ablation (development only) -- mr_zn_v5

- Symbol ZN, strategy `mean_reversion_v5`, 41,472 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 30,743 configs (74.1%).
- Grid-wide: 1.4% profitable, median dev Sharpe -1.67, 0 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 41472 | 41472 |  |
| 1 backtest integrity | 41472 | 41472 |  |
| 2 trade count & coverage | 41472 | 30743 |  |
| 3 performance & risk | 30743 | 0 |  |
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
| timeframe | 3.393 |
| std_lookback | 1.190 |
| stop_atr_multiple | 0.867 |
| entry_confirmation | 0.683 |
| entry_z | 0.679 |
| mean_lookback | 0.449 |
| max_holding_bars | 0.310 |
| mean_type | 0.105 |
| exit_z | 0.021 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 5min | 13824 | 0.0% | -4.22 | -2.34 | 0.0% | 95.7% | -4.30 | 1020 | 0 | 0 | 0.00 |
| timeframe | 15min | 13824 | 1.7% | -1.69 | -0.69 | 0.0% | 80.6% | -1.89 | 370 | 0 | 0 | 0.15 |
| timeframe | 1h | 13824 | 2.6% | -0.82 | -0.29 | 0.0% | 46.0% | -1.00 | 89 | 0 | 0 | 2.85 |
| mean_type | sma | 20736 | 1.4% | -1.73 | -0.49 | 0.0% | 76.9% | -2.40 | 306 | 0 | 0 | 1.74 |
| mean_type | ema | 20736 | 1.4% | -1.62 | -0.55 | 0.0% | 71.3% | -2.35 | 247 | 0 | 0 | 0.26 |
| mean_lookback | 20 | 6912 | 3.8% | -1.40 | -0.31 | 0.0% | 53.5% | -2.56 | 122 | 0 | 0 | 0.00 |
| mean_lookback | 30 | 6912 | 2.4% | -1.56 | -0.41 | 0.0% | 65.7% | -2.51 | 206 | 0 | 0 | 1.26 |
| mean_lookback | 40 | 6912 | 1.6% | -1.65 | -0.48 | 0.0% | 75.7% | -2.39 | 277 | 0 | 0 | 1.14 |
| mean_lookback | 50 | 6912 | 0.5% | -1.76 | -0.57 | 0.0% | 80.2% | -2.32 | 347 | 0 | 0 | 1.14 |
| mean_lookback | 60 | 6912 | 0.2% | -1.79 | -0.69 | 0.0% | 83.2% | -2.27 | 399 | 0 | 0 | 0.66 |
| mean_lookback | 80 | 6912 | 0.1% | -1.85 | -0.76 | 0.0% | 86.5% | -2.24 | 443 | 0 | 0 | 1.80 |
| std_lookback | 10 | 5184 | 0.1% | -2.51 | -0.75 | 0.0% | 96.9% | -2.64 | 660 | 0 | 0 | 3.44 |
| std_lookback | 15 | 5184 | 0.9% | -1.91 | -0.62 | 0.0% | 88.1% | -2.29 | 517 | 0 | 0 | 2.08 |
| std_lookback | 20 | 5184 | 1.9% | -1.78 | -0.52 | 0.0% | 83.5% | -2.13 | 436 | 0 | 0 | 1.04 |
| std_lookback | 25 | 5184 | 2.3% | -1.56 | -0.48 | 0.0% | 77.4% | -2.16 | 340 | 0 | 0 | 0.48 |
| std_lookback | 30 | 5184 | 1.4% | -1.61 | -0.45 | 0.0% | 72.7% | -2.32 | 264 | 0 | 0 | 0.16 |
| std_lookback | 40 | 5184 | 0.2% | -1.56 | -0.60 | 0.0% | 65.7% | -2.41 | 187 | 0 | 0 | 0.32 |
| std_lookback | 60 | 5184 | 1.9% | -1.51 | -0.36 | 0.0% | 58.1% | -2.47 | 139 | 0 | 0 | 0.48 |
| std_lookback | 80 | 5184 | 2.7% | -1.32 | -0.43 | 0.0% | 50.6% | -2.49 | 101 | 0 | 0 | 0.00 |
| entry_z | -2.0 | 13824 | 0.4% | -2.04 | -0.65 | 0.0% | 87.1% | -2.44 | 441 | 0 | 0 | 1.53 |
| entry_z | -2.5 | 13824 | 1.1% | -1.65 | -0.53 | 0.0% | 73.5% | -2.42 | 267 | 0 | 0 | 0.75 |
| entry_z | -3.0 | 13824 | 2.8% | -1.37 | -0.41 | 0.0% | 61.8% | -2.29 | 161 | 0 | 0 | 0.72 |
| exit_z | -1.0 | 10368 | 1.4% | -1.69 | -0.52 | 0.0% | 74.2% | -2.45 | 276 | 0 | 0 | 0.92 |
| exit_z | -0.5 | 10368 | 1.5% | -1.67 | -0.52 | 0.0% | 74.2% | -2.38 | 275 | 0 | 0 | 0.92 |
| exit_z | 0.0 | 10368 | 1.3% | -1.67 | -0.53 | 0.0% | 74.1% | -2.35 | 274 | 0 | 0 | 1.00 |
| exit_z | 0.5 | 10368 | 1.5% | -1.67 | -0.51 | 0.0% | 74.1% | -2.34 | 274 | 0 | 0 | 1.16 |
| max_holding_bars | 5 | 20736 | 1.4% | -1.83 | -0.59 | 0.0% | 74.4% | -2.62 | 273 | 0 | 0 | 0.86 |
| max_holding_bars | 10 | 20736 | 1.5% | -1.52 | -0.45 | 0.0% | 73.8% | -2.18 | 277 | 0 | 0 | 1.14 |
| entry_confirmation | none | 20736 | 0.5% | -2.01 | -0.74 | 0.0% | 85.1% | -2.43 | 494 | 0 | 0 | 0.78 |
| entry_confirmation | positive_bar_return | 20736 | 2.4% | -1.33 | -0.38 | 0.0% | 63.1% | -2.32 | 164 | 0 | 0 | 1.22 |
| stop_atr_multiple | none | 13824 | 1.8% | -1.39 | -0.42 | 0.0% | 70.3% | -2.01 | 222 | 0 | 0 | 2.22 |
| stop_atr_multiple | 1.0 | 13824 | 1.2% | -2.26 | -0.63 | 0.0% | 77.3% | -2.89 | 328 | 0 | 0 | 0.27 |
| stop_atr_multiple | 2.0 | 13824 | 1.3% | -1.63 | -0.54 | 0.0% | 74.7% | -2.21 | 258 | 0 | 0 | 0.51 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 1h | sma | 60 | 15 | -2.0 | -1.0 | 10 | positive_bar_return | none | 103 | 2.6% | 0.38 | -1.3% | s3 hard_reject |
| 2 | 1h | sma | 60 | 15 | -2.0 | 0.5 | 10 | positive_bar_return | none | 101 | 2.0% | 0.28 | -1.3% | s3 hard_reject |
| 3 | 1h | sma | 60 | 15 | -2.0 | 0.0 | 10 | positive_bar_return | none | 101 | 1.7% | 0.24 | -1.3% | s3 hard_reject |
| 4 | 1h | sma | 60 | 15 | -2.0 | -0.5 | 10 | positive_bar_return | none | 101 | 1.3% | 0.18 | -1.6% | s3 hard_reject |
| 5 | 1h | sma | 50 | 15 | -2.0 | -1.0 | 10 | positive_bar_return | none | 112 | 1.3% | 0.18 | -1.5% | s3 hard_reject |
| 6 | 1h | sma | 50 | 15 | -2.0 | 0.5 | 10 | positive_bar_return | none | 108 | 0.8% | 0.10 | -2.6% | s3 hard_reject |
| 7 | 1h | sma | 50 | 15 | -2.0 | -0.5 | 10 | positive_bar_return | none | 108 | 0.6% | 0.09 | -1.8% | s3 hard_reject |
| 8 | 15min | ema | 30 | 40 | -2.0 | 0.5 | 10 | positive_bar_return | 1.0 | 126 | 0.3% | 0.09 | -2.4% | s3 hard_reject |
| 9 | 1h | sma | 50 | 15 | -2.0 | 0.0 | 10 | positive_bar_return | none | 108 | 0.5% | 0.07 | -2.2% | s3 hard_reject |
| 10 | 1h | sma | 40 | 10 | -3.0 | -0.5 | 10 | positive_bar_return | none | 111 | 0.4% | 0.05 | -4.1% | s3 hard_reject |
| 11 | 1h | sma | 40 | 10 | -3.0 | 0.0 | 10 | positive_bar_return | none | 111 | 0.4% | 0.05 | -4.3% | s3 hard_reject |
| 12 | 1h | sma | 40 | 10 | -3.0 | 0.5 | 10 | positive_bar_return | none | 111 | 0.4% | 0.05 | -3.8% | s3 hard_reject |
| 13 | 1h | ema | 80 | 10 | -2.0 | 0.5 | 5 | positive_bar_return | none | 105 | 0.2% | 0.04 | -2.4% | s3 hard_reject |
| 14 | 1h | sma | 50 | 15 | -2.0 | 0.5 | 10 | none | none | 169 | -0.1% | -0.00 | -3.1% | s3 hard_reject |
| 15 | 15min | ema | 30 | 40 | -2.0 | 0.0 | 10 | positive_bar_return | 1.0 | 126 | -0.1% | -0.02 | -2.6% | s3 hard_reject |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
