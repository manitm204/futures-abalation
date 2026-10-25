# Ablation (development only) -- mr_nq_v6

- Symbol NQ, strategy `mean_reversion_v6`, 21,600 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 14,236 configs (65.9%).
- Grid-wide: 33.0% profitable, median dev Sharpe -0.21, 826 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 21600 | 21600 |  |
| 1 backtest integrity | 21600 | 21600 |  |
| 2 trade count & coverage | 21600 | 14236 |  |
| 3 performance & risk | 14236 | 394 |  |
| 4 parameter stability | 394 | 383 |  |
| 5 time stability | 383 | 383 |  |
| 6 deduplication | 383 | 201 | best 2 per cluster |
| 7 execution stress | 201 | 201 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 201 |  | diagnostic only: unverified: 201 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| timeframe | 0.907 |
| std_lookback | 0.182 |
| entry_z | 0.165 |
| mean_lookback | 0.133 |
| mean_type | 0.125 |
| stop_atr_multiple | 0.095 |
| max_holding_bars | 0.046 |
| exit_z | 0.034 |
| entry_confirmation | 0.000 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 5min | 7200 | 8.6% | -0.65 | -0.02 | 0.0% | 83.3% | -0.70 | 828 | 0 | 0 | 0.00 |
| timeframe | 15min | 7200 | 30.0% | -0.17 | 0.36 | 1.0% | 76.6% | -0.19 | 307 | 54 | 28 | 0.30 |
| timeframe | 1h | 7200 | 60.3% | 0.26 | 0.78 | 10.4% | 37.9% | 0.33 | 66 | 340 | 173 | 2.70 |
| mean_type | sma | 10800 | 30.5% | -0.28 | 0.51 | 3.5% | 70.1% | -0.39 | 220 | 219 | 111 | 1.24 |
| mean_type | ema | 10800 | 35.5% | -0.16 | 0.52 | 4.2% | 61.7% | -0.25 | 165 | 175 | 90 | 0.76 |
| mean_lookback | 20 | 4320 | 26.7% | -0.29 | 0.46 | 3.3% | 46.8% | -0.44 | 81 | 54 | 30 | 0.70 |
| mean_lookback | 25 | 4320 | 30.1% | -0.25 | 0.58 | 4.5% | 57.3% | -0.33 | 139 | 86 | 50 | 1.30 |
| mean_lookback | 30 | 4320 | 36.0% | -0.17 | 0.58 | 5.7% | 65.1% | -0.30 | 189 | 129 | 61 | 1.75 |
| mean_lookback | 40 | 4320 | 39.1% | -0.16 | 0.53 | 3.7% | 77.7% | -0.25 | 298 | 77 | 36 | 0.95 |
| mean_lookback | 50 | 4320 | 32.9% | -0.20 | 0.42 | 1.9% | 82.6% | -0.29 | 395 | 48 | 24 | 0.30 |
| std_lookback | 5 | 3600 | 31.6% | -0.27 | 0.50 | 2.7% | 99.9% | -0.27 | 605 | 95 | 49 | 0.36 |
| std_lookback | 8 | 3600 | 39.0% | -0.16 | 0.74 | 9.9% | 86.9% | -0.26 | 430 | 130 | 60 | 2.64 |
| std_lookback | 10 | 3600 | 34.5% | -0.31 | 0.61 | 5.6% | 77.6% | -0.46 | 297 | 88 | 44 | 1.86 |
| std_lookback | 15 | 3600 | 36.4% | -0.14 | 0.44 | 1.3% | 54.8% | -0.26 | 117 | 27 | 18 | 0.30 |
| std_lookback | 20 | 3600 | 34.9% | -0.13 | 0.52 | 2.8% | 42.2% | -0.14 | 63 | 52 | 28 | 0.84 |
| std_lookback | 25 | 3600 | 21.6% | -0.27 | 0.34 | 0.7% | 34.1% | -0.46 | 43 | 2 | 2 | 0.00 |
| entry_z | -2.0 | 5400 | 30.9% | -0.31 | 0.49 | 3.7% | 86.6% | -0.40 | 444 | 150 | 84 | 1.64 |
| entry_z | -2.5 | 5400 | 32.8% | -0.23 | 0.50 | 3.4% | 69.0% | -0.34 | 215 | 78 | 44 | 0.52 |
| entry_z | -3.0 | 5400 | 34.4% | -0.18 | 0.54 | 3.9% | 57.3% | -0.29 | 146 | 84 | 39 | 1.12 |
| entry_z | -3.5 | 5400 | 33.7% | -0.14 | 0.55 | 4.4% | 50.7% | -0.25 | 103 | 82 | 34 | 0.72 |
| exit_z | -1.25 | 4320 | 34.3% | -0.19 | 0.52 | 3.3% | 66.0% | -0.30 | 192 | 64 | 31 | 0.85 |
| exit_z | -1.0 | 4320 | 33.6% | -0.20 | 0.51 | 4.0% | 65.9% | -0.31 | 191 | 79 | 35 | 1.00 |
| exit_z | -0.5 | 4320 | 32.6% | -0.21 | 0.53 | 3.8% | 65.9% | -0.33 | 190 | 78 | 28 | 0.75 |
| exit_z | 0.0 | 4320 | 32.2% | -0.21 | 0.51 | 3.9% | 65.9% | -0.33 | 190 | 85 | 53 | 1.15 |
| exit_z | 0.5 | 4320 | 32.1% | -0.22 | 0.51 | 4.1% | 65.9% | -0.34 | 190 | 88 | 54 | 1.25 |
| max_holding_bars | 3 | 7200 | 32.1% | -0.24 | 0.45 | 2.9% | 66.5% | -0.36 | 191 | 58 | 20 | 0.42 |
| max_holding_bars | 5 | 7200 | 33.6% | -0.19 | 0.58 | 5.3% | 66.2% | -0.30 | 189 | 176 | 86 | 1.83 |
| max_holding_bars | 10 | 7200 | 33.3% | -0.20 | 0.52 | 3.3% | 65.0% | -0.31 | 192 | 160 | 95 | 0.75 |
| entry_confirmation | positive_bar_return | 21600 | 33.0% | -0.21 | 0.52 | 3.8% | 65.9% | -0.32 | 190 | 394 | 201 | 1.00 |
| stop_atr_multiple | none | 10800 | 34.6% | -0.17 | 0.50 | 3.0% | 64.0% | -0.26 | 173 | 98 | 49 | 0.26 |
| stop_atr_multiple | 1.5 | 10800 | 31.4% | -0.26 | 0.54 | 4.6% | 67.8% | -0.40 | 209 | 296 | 152 | 1.74 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 1h | sma | 30 | 8 | -3.5 | 0.5 | 3 | positive_bar_return | 1.5 | 102 | 41.2% | 1.47 | -2.8% | s6 deduplicated |
| 2 | 1h | sma | 30 | 8 | -3.5 | 0.0 | 3 | positive_bar_return | 1.5 | 102 | 40.4% | 1.45 | -2.8% | s6 deduplicated |
| 3 | 1h | ema | 25 | 10 | -2.0 | 0.5 | 5 | positive_bar_return | 1.5 | 109 | 71.4% | 1.45 | -5.6% | s7 pass |
| 4 | 1h | ema | 25 | 10 | -2.0 | -0.5 | 5 | positive_bar_return | 1.5 | 109 | 64.0% | 1.44 | -5.6% | s6 deduplicated |
| 5 | 1h | sma | 25 | 10 | -2.5 | -1.25 | 5 | positive_bar_return | 1.5 | 114 | 55.0% | 1.43 | -5.7% | s7 pass |
| 6 | 1h | sma | 30 | 8 | -3.5 | -0.5 | 3 | positive_bar_return | 1.5 | 102 | 38.7% | 1.43 | -2.8% | s6 deduplicated |
| 7 | 1h | sma | 30 | 8 | -3.5 | -1.0 | 3 | positive_bar_return | 1.5 | 102 | 37.9% | 1.40 | -2.8% | s6 deduplicated |
| 8 | 1h | sma | 30 | 8 | -3.5 | -1.25 | 3 | positive_bar_return | 1.5 | 102 | 36.3% | 1.37 | -2.9% | s6 deduplicated |
| 9 | 1h | ema | 25 | 10 | -2.0 | 0.0 | 5 | positive_bar_return | 1.5 | 109 | 64.3% | 1.36 | -5.6% | s7 pass |
| 10 | 1h | sma | 30 | 8 | -3.0 | 0.0 | 10 | positive_bar_return | 1.5 | 135 | 67.8% | 1.28 | -7.6% | s7 pass |
| 11 | 1h | ema | 25 | 10 | -2.0 | -1.25 | 5 | positive_bar_return | 1.5 | 111 | 49.8% | 1.28 | -6.8% | s6 deduplicated |
| 12 | 1h | sma | 25 | 10 | -2.5 | -1.0 | 5 | positive_bar_return | 1.5 | 111 | 47.1% | 1.27 | -4.0% | s7 pass |
| 13 | 1h | ema | 25 | 10 | -2.0 | -1.0 | 5 | positive_bar_return | 1.5 | 110 | 50.8% | 1.27 | -7.5% | s6 deduplicated |
| 14 | 1h | sma | 30 | 8 | -3.5 | 0.0 | 5 | positive_bar_return | 1.5 | 107 | 40.7% | 1.25 | -3.7% | s7 pass |
| 15 | 1h | sma | 30 | 8 | -3.0 | 0.0 | 10 | positive_bar_return | none | 102 | 63.4% | 1.24 | -5.6% | s7 pass |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
