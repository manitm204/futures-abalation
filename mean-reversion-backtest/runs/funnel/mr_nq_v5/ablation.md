# Ablation (development only) -- mr_nq_v5

- Symbol NQ, strategy `mean_reversion_v5`, 41,472 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 29,508 configs (71.2%).
- Grid-wide: 31.4% profitable, median dev Sharpe -0.16, 256 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 41472 | 41472 |  |
| 1 backtest integrity | 41472 | 41472 |  |
| 2 trade count & coverage | 41472 | 29508 |  |
| 3 performance & risk | 29508 | 190 |  |
| 4 parameter stability | 190 | 166 |  |
| 5 time stability | 166 | 157 |  |
| 6 deduplication | 157 | 93 | best 2 per cluster |
| 7 execution stress | 93 | 93 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 93 |  | diagnostic only: unverified: 93 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| timeframe | 0.339 |
| std_lookback | 0.200 |
| stop_atr_multiple | 0.156 |
| mean_lookback | 0.117 |
| entry_z | 0.114 |
| entry_confirmation | 0.033 |
| mean_type | 0.030 |
| max_holding_bars | 0.027 |
| exit_z | 0.011 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 5min | 13824 | 19.6% | -0.38 | 0.23 | 0.3% | 94.5% | -0.38 | 976 | 35 | 13 | 0.48 |
| timeframe | 15min | 13824 | 34.6% | -0.12 | 0.33 | 0.6% | 81.3% | -0.13 | 326 | 78 | 34 | 1.23 |
| timeframe | 1h | 13824 | 40.1% | -0.04 | 0.41 | 1.0% | 37.7% | 0.01 | 71 | 77 | 46 | 1.29 |
| mean_type | sma | 20736 | 30.6% | -0.18 | 0.33 | 0.8% | 75.1% | -0.21 | 292 | 137 | 61 | 1.52 |
| mean_type | ema | 20736 | 32.3% | -0.15 | 0.33 | 0.5% | 67.2% | -0.18 | 216 | 53 | 32 | 0.48 |
| mean_lookback | 20 | 6912 | 25.6% | -0.23 | 0.29 | 0.4% | 52.3% | -0.22 | 114 | 20 | 10 | 0.72 |
| mean_lookback | 30 | 6912 | 28.0% | -0.19 | 0.31 | 1.0% | 64.2% | -0.23 | 190 | 48 | 31 | 1.68 |
| mean_lookback | 40 | 6912 | 34.3% | -0.13 | 0.38 | 0.8% | 72.5% | -0.14 | 258 | 36 | 21 | 1.08 |
| mean_lookback | 50 | 6912 | 34.9% | -0.11 | 0.33 | 0.4% | 76.9% | -0.15 | 317 | 25 | 11 | 0.54 |
| mean_lookback | 60 | 6912 | 34.6% | -0.14 | 0.34 | 0.5% | 78.8% | -0.20 | 347 | 27 | 12 | 0.96 |
| mean_lookback | 80 | 6912 | 31.1% | -0.17 | 0.32 | 0.5% | 82.2% | -0.25 | 390 | 34 | 8 | 1.02 |
| std_lookback | 10 | 5184 | 24.9% | -0.27 | 0.33 | 1.5% | 93.1% | -0.32 | 577 | 49 | 30 | 2.16 |
| std_lookback | 15 | 5184 | 33.6% | -0.15 | 0.32 | 0.4% | 83.4% | -0.19 | 436 | 19 | 14 | 0.80 |
| std_lookback | 20 | 5184 | 34.8% | -0.13 | 0.36 | 1.0% | 76.8% | -0.15 | 365 | 31 | 19 | 1.44 |
| std_lookback | 25 | 5184 | 36.3% | -0.12 | 0.39 | 1.1% | 72.3% | -0.19 | 289 | 47 | 15 | 2.32 |
| std_lookback | 30 | 5184 | 28.1% | -0.19 | 0.31 | 0.1% | 68.2% | -0.21 | 227 | 5 | 5 | 0.08 |
| std_lookback | 40 | 5184 | 27.4% | -0.20 | 0.32 | 0.3% | 64.1% | -0.25 | 180 | 14 | 4 | 0.72 |
| std_lookback | 60 | 5184 | 28.7% | -0.19 | 0.31 | 0.3% | 58.6% | -0.12 | 140 | 16 | 4 | 0.48 |
| std_lookback | 80 | 5184 | 37.7% | -0.08 | 0.31 | 0.2% | 52.6% | -0.09 | 112 | 9 | 2 | 0.00 |
| entry_z | -2.0 | 13824 | 27.6% | -0.22 | 0.29 | 0.5% | 85.6% | -0.27 | 437 | 56 | 34 | 0.99 |
| entry_z | -2.5 | 13824 | 31.9% | -0.16 | 0.34 | 0.5% | 70.8% | -0.19 | 252 | 46 | 20 | 0.90 |
| entry_z | -3.0 | 13824 | 34.8% | -0.11 | 0.36 | 0.9% | 57.1% | -0.11 | 137 | 88 | 39 | 1.11 |
| exit_z | -1.0 | 10368 | 32.1% | -0.16 | 0.34 | 0.8% | 71.3% | -0.19 | 254 | 58 | 35 | 1.20 |
| exit_z | -0.5 | 10368 | 31.3% | -0.17 | 0.33 | 0.6% | 71.2% | -0.20 | 252 | 45 | 22 | 0.96 |
| exit_z | 0.0 | 10368 | 30.8% | -0.17 | 0.32 | 0.6% | 71.1% | -0.20 | 251 | 47 | 20 | 0.96 |
| exit_z | 0.5 | 10368 | 31.4% | -0.17 | 0.33 | 0.5% | 71.1% | -0.20 | 251 | 40 | 16 | 0.88 |
| max_holding_bars | 5 | 20736 | 30.7% | -0.18 | 0.33 | 0.7% | 71.6% | -0.23 | 253 | 113 | 49 | 1.18 |
| max_holding_bars | 10 | 20736 | 32.2% | -0.15 | 0.33 | 0.5% | 70.7% | -0.17 | 251 | 77 | 44 | 0.82 |
| entry_confirmation | none | 20736 | 31.6% | -0.15 | 0.32 | 0.5% | 84.1% | -0.15 | 436 | 86 | 32 | 0.78 |
| entry_confirmation | positive_bar_return | 20736 | 31.3% | -0.18 | 0.35 | 0.8% | 58.2% | -0.29 | 141 | 104 | 61 | 1.22 |
| stop_atr_multiple | none | 13824 | 36.9% | -0.09 | 0.39 | 0.7% | 66.6% | -0.09 | 198 | 74 | 37 | 1.26 |
| stop_atr_multiple | 1.0 | 13824 | 26.3% | -0.25 | 0.27 | 0.4% | 75.1% | -0.28 | 313 | 41 | 23 | 0.54 |
| stop_atr_multiple | 2.0 | 13824 | 31.1% | -0.16 | 0.32 | 0.7% | 71.7% | -0.22 | 240 | 75 | 33 | 1.20 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 1h | sma | 30 | 20 | -2.0 | -0.5 | 10 | positive_bar_return | 2.0 | 104 | 53.4% | 1.16 | -6.5% | s7 pass |
| 2 | 15min | sma | 80 | 25 | -2.5 | -1.0 | 5 | positive_bar_return | none | 345 | 43.4% | 1.09 | -10.4% | s4 hard_reject |
| 3 | 15min | sma | 40 | 20 | -3.0 | -1.0 | 5 | positive_bar_return | none | 186 | 30.0% | 1.09 | -5.3% | s7 pass |
| 4 | 5min | sma | 50 | 40 | -3.0 | -0.5 | 10 | none | none | 584 | 36.8% | 1.06 | -7.5% | s6 deduplicated |
| 5 | 1h | sma | 20 | 10 | -2.0 | -1.0 | 10 | positive_bar_return | 1.0 | 150 | 38.6% | 1.05 | -4.3% | s7 pass |
| 6 | 5min | sma | 50 | 40 | -3.0 | 0.0 | 10 | none | none | 583 | 36.0% | 1.05 | -7.5% | s6 deduplicated |
| 7 | 1h | sma | 30 | 20 | -2.0 | 0.0 | 10 | positive_bar_return | 2.0 | 104 | 50.0% | 1.05 | -6.5% | s7 pass |
| 8 | 1h | sma | 40 | 10 | -3.0 | -0.5 | 10 | positive_bar_return | 2.0 | 121 | 61.9% | 1.04 | -6.5% | s7 pass |
| 9 | 15min | sma | 80 | 25 | -2.5 | 0.0 | 5 | none | none | 545 | 50.3% | 1.03 | -7.8% | s6 deduplicated |
| 10 | 15min | sma | 80 | 25 | -2.5 | 0.0 | 5 | none | 2.0 | 692 | 51.1% | 1.01 | -9.7% | s7 pass |
| 11 | 15min | sma | 80 | 25 | -2.5 | 0.5 | 5 | none | none | 544 | 48.6% | 1.00 | -8.2% | s6 deduplicated |
| 12 | 15min | sma | 40 | 20 | -3.0 | 0.0 | 5 | positive_bar_return | none | 186 | 26.8% | 1.00 | -6.6% | s7 pass |
| 13 | 1h | ema | 40 | 20 | -2.0 | -1.0 | 10 | positive_bar_return | 1.0 | 105 | 39.4% | 0.99 | -6.2% | s7 pass |
| 14 | 15min | sma | 80 | 25 | -2.5 | -1.0 | 5 | none | none | 554 | 47.7% | 0.98 | -8.2% | s6 deduplicated |
| 15 | 1h | ema | 30 | 10 | -2.0 | 0.5 | 5 | positive_bar_return | 1.0 | 155 | 47.3% | 0.98 | -9.2% | s7 pass |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
