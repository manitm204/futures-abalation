# Ablation (development only) -- mr_6e_v5

- Symbol 6E, strategy `mean_reversion_v5`, 41,472 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 32,101 configs (77.4%).
- Grid-wide: 4.9% profitable, median dev Sharpe -0.88, 39 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 41472 | 41472 |  |
| 1 backtest integrity | 41472 | 41472 |  |
| 2 trade count & coverage | 41472 | 32101 |  |
| 3 performance & risk | 32101 | 6 |  |
| 4 parameter stability | 6 | 6 |  |
| 5 time stability | 6 | 6 |  |
| 6 deduplication | 6 | 2 | best 2 per cluster |
| 7 execution stress | 2 | 2 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 2 |  | diagnostic only: unverified: 2 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| timeframe | 1.083 |
| std_lookback | 0.442 |
| mean_lookback | 0.393 |
| entry_z | 0.290 |
| stop_atr_multiple | 0.271 |
| max_holding_bars | 0.157 |
| exit_z | 0.098 |
| entry_confirmation | 0.089 |
| mean_type | 0.050 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 5min | 13824 | 0.2% | -1.66 | -0.87 | 0.1% | 98.3% | -1.67 | 1225 | 0 | 0 | 0.00 |
| timeframe | 15min | 13824 | 6.5% | -0.73 | -0.11 | 0.1% | 83.9% | -0.81 | 433 | 0 | 0 | 1.23 |
| timeframe | 1h | 13824 | 8.0% | -0.58 | -0.05 | 0.2% | 50.1% | -0.72 | 100 | 6 | 2 | 1.77 |
| mean_type | sma | 20736 | 3.7% | -0.91 | -0.22 | 0.0% | 79.7% | -1.04 | 365 | 6 | 2 | 1.34 |
| mean_type | ema | 20736 | 6.0% | -0.86 | -0.14 | 0.2% | 75.1% | -1.05 | 306 | 0 | 0 | 0.66 |
| mean_lookback | 20 | 6912 | 9.9% | -0.63 | 0.01 | 0.3% | 58.1% | -0.91 | 159 | 0 | 0 | 0.00 |
| mean_lookback | 30 | 6912 | 5.5% | -0.73 | -0.14 | 0.0% | 71.6% | -0.93 | 261 | 0 | 0 | 0.78 |
| mean_lookback | 40 | 6912 | 4.8% | -0.89 | -0.18 | 0.0% | 78.0% | -1.06 | 343 | 0 | 0 | 0.24 |
| mean_lookback | 50 | 6912 | 3.8% | -0.98 | -0.28 | 0.2% | 82.7% | -1.09 | 421 | 0 | 0 | 0.42 |
| mean_lookback | 60 | 6912 | 3.3% | -1.02 | -0.31 | 0.0% | 85.6% | -1.10 | 465 | 0 | 0 | 2.52 |
| mean_lookback | 80 | 6912 | 1.9% | -1.02 | -0.35 | 0.1% | 88.4% | -1.10 | 503 | 6 | 2 | 2.04 |
| std_lookback | 10 | 5184 | 2.4% | -1.03 | -0.35 | 0.1% | 98.6% | -1.05 | 722 | 6 | 2 | 4.16 |
| std_lookback | 15 | 5184 | 2.7% | -1.06 | -0.43 | 0.0% | 90.6% | -1.14 | 613 | 0 | 0 | 0.40 |
| std_lookback | 20 | 5184 | 3.3% | -1.07 | -0.26 | 0.2% | 87.6% | -1.16 | 524 | 0 | 0 | 0.64 |
| std_lookback | 25 | 5184 | 4.2% | -0.88 | -0.23 | 0.0% | 83.0% | -1.01 | 427 | 0 | 0 | 0.00 |
| std_lookback | 30 | 5184 | 5.3% | -0.89 | -0.22 | 0.0% | 77.4% | -1.08 | 336 | 0 | 0 | 0.00 |
| std_lookback | 40 | 5184 | 11.5% | -0.63 | 0.04 | 0.5% | 68.2% | -0.96 | 227 | 0 | 0 | 2.80 |
| std_lookback | 60 | 5184 | 6.2% | -0.73 | -0.11 | 0.0% | 60.0% | -0.98 | 153 | 0 | 0 | 0.00 |
| std_lookback | 80 | 5184 | 3.5% | -0.78 | -0.19 | 0.0% | 53.8% | -0.96 | 116 | 0 | 0 | 0.00 |
| entry_z | -2.0 | 13824 | 2.5% | -1.05 | -0.34 | 0.1% | 88.9% | -1.13 | 528 | 6 | 2 | 1.17 |
| entry_z | -2.5 | 13824 | 4.6% | -0.85 | -0.18 | 0.0% | 77.3% | -1.02 | 329 | 0 | 0 | 0.81 |
| entry_z | -3.0 | 13824 | 7.6% | -0.76 | -0.07 | 0.2% | 66.0% | -0.99 | 203 | 0 | 0 | 1.02 |
| exit_z | -1.0 | 10368 | 5.0% | -0.93 | -0.20 | 0.1% | 77.5% | -1.11 | 337 | 1 | 1 | 0.96 |
| exit_z | -0.5 | 10368 | 4.7% | -0.89 | -0.20 | 0.1% | 77.4% | -1.07 | 335 | 2 | 1 | 0.72 |
| exit_z | 0.0 | 10368 | 4.7% | -0.87 | -0.19 | 0.1% | 77.4% | -1.03 | 333 | 2 | 0 | 1.04 |
| exit_z | 0.5 | 10368 | 5.2% | -0.84 | -0.16 | 0.1% | 77.4% | -0.98 | 333 | 1 | 0 | 1.28 |
| max_holding_bars | 5 | 20736 | 4.9% | -0.96 | -0.21 | 0.1% | 77.5% | -1.13 | 329 | 6 | 2 | 0.96 |
| max_holding_bars | 10 | 20736 | 4.9% | -0.80 | -0.16 | 0.1% | 77.3% | -0.96 | 338 | 0 | 0 | 1.04 |
| entry_confirmation | none | 20736 | 2.0% | -0.92 | -0.31 | 0.0% | 86.2% | -1.02 | 538 | 6 | 2 | 1.66 |
| entry_confirmation | positive_bar_return | 20736 | 7.8% | -0.83 | -0.06 | 0.2% | 68.6% | -1.08 | 212 | 0 | 0 | 0.34 |
| stop_atr_multiple | none | 13824 | 6.1% | -0.75 | -0.12 | 0.1% | 74.2% | -0.88 | 268 | 4 | 2 | 1.98 |
| stop_atr_multiple | 1.0 | 13824 | 4.4% | -1.02 | -0.23 | 0.0% | 80.3% | -1.18 | 402 | 0 | 0 | 0.18 |
| stop_atr_multiple | 2.0 | 13824 | 4.1% | -0.91 | -0.22 | 0.1% | 77.7% | -1.08 | 316 | 2 | 0 | 0.84 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 1h | sma | 80 | 10 | -2.0 | 0.0 | 5 | none | none | 187 | 11.2% | 1.09 | -2.6% | s6 deduplicated |
| 2 | 1h | sma | 80 | 10 | -2.0 | -0.5 | 5 | none | none | 189 | 11.0% | 1.08 | -2.9% | s7 pass |
| 3 | 1h | sma | 80 | 10 | -2.0 | -1.0 | 5 | none | none | 192 | 10.1% | 1.01 | -3.0% | s7 pass |
| 4 | 1h | sma | 80 | 10 | -2.0 | 0.5 | 5 | none | none | 182 | 10.2% | 0.99 | -2.6% | s6 deduplicated |
| 5 | 1h | sma | 80 | 10 | -2.0 | 0.0 | 5 | none | 2.0 | 209 | 8.2% | 0.80 | -3.6% | s6 deduplicated |
| 6 | 1h | sma | 80 | 10 | -2.0 | -0.5 | 5 | none | 2.0 | 211 | 8.1% | 0.79 | -3.9% | s6 deduplicated |
| 7 | 1h | sma | 80 | 10 | -3.0 | -1.0 | 5 | none | none | 161 | 6.6% | 0.72 | -2.6% | s3 hard_reject |
| 8 | 1h | sma | 60 | 10 | -2.0 | -1.0 | 5 | none | none | 186 | 8.0% | 0.72 | -3.6% | s3 hard_reject |
| 9 | 1h | sma | 80 | 10 | -2.0 | -1.0 | 5 | none | 2.0 | 216 | 7.1% | 0.71 | -4.1% | s3 hard_reject |
| 10 | 1h | sma | 60 | 10 | -2.0 | -0.5 | 5 | none | none | 183 | 7.6% | 0.70 | -3.5% | s3 hard_reject |
| 11 | 1h | sma | 80 | 10 | -2.0 | 0.0 | 10 | none | none | 166 | 9.3% | 0.69 | -4.8% | s3 hard_reject |
| 12 | 1h | sma | 60 | 10 | -2.0 | -1.0 | 5 | none | 2.0 | 216 | 7.4% | 0.66 | -4.3% | s3 hard_reject |
| 13 | 1h | sma | 80 | 10 | -2.0 | 0.5 | 10 | none | none | 162 | 8.5% | 0.63 | -4.8% | s3 hard_reject |
| 14 | 1h | sma | 60 | 10 | -2.0 | -0.5 | 5 | none | 2.0 | 213 | 6.9% | 0.63 | -4.5% | s3 hard_reject |
| 15 | 1h | sma | 80 | 10 | -2.5 | 0.0 | 5 | none | none | 169 | 6.0% | 0.63 | -3.0% | s3 hard_reject |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
