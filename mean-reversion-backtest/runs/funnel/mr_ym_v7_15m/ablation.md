# Ablation (development only) -- mr_ym_v7_15m

- Symbol YM, strategy `mean_reversion_v14`, 17,280 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 10,644 configs (61.6%).
- Grid-wide: 45.2% profitable, median dev Sharpe -0.02, 464 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 17280 | 17280 |  |
| 1 backtest integrity | 17280 | 17280 |  |
| 2 trade count & coverage | 17280 | 10644 |  |
| 3 performance & risk | 10644 | 377 |  |
| 4 parameter stability | 377 | 347 |  |
| 5 time stability | 347 | 340 |  |
| 6 deduplication | 340 | 156 | best 2 per cluster |
| 7 execution stress | 156 | 156 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 156 |  | diagnostic only: unverified: 156 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| std_lookback | 0.623 |
| entry_z | 0.233 |
| mean_lookback | 0.152 |
| entry_confirmation | 0.142 |
| max_holding_bars | 0.104 |
| stop_atr_multiple | 0.064 |
| exit_z | 0.039 |
| mean_type | 0.034 |
| timeframe | 0.000 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 15min | 17280 | 45.2% | -0.02 | 0.51 | 2.7% | 61.6% | 0.06 | 160 | 377 | 156 | 1.00 |
| mean_type | sma | 8640 | 47.3% | -0.01 | 0.52 | 2.9% | 67.6% | 0.07 | 201 | 232 | 90 | 1.44 |
| mean_type | ema | 8640 | 43.2% | -0.04 | 0.49 | 2.5% | 55.6% | 0.05 | 127 | 145 | 66 | 0.56 |
| mean_lookback | 32 | 3456 | 36.3% | -0.11 | 0.45 | 1.8% | 50.5% | -0.03 | 102 | 44 | 18 | 0.90 |
| mean_lookback | 37 | 3456 | 44.2% | -0.04 | 0.57 | 4.5% | 57.2% | 0.06 | 135 | 144 | 65 | 2.20 |
| mean_lookback | 42 | 3456 | 50.3% | 0.04 | 0.58 | 4.1% | 63.2% | 0.13 | 173 | 123 | 47 | 1.50 |
| mean_lookback | 47 | 3456 | 49.9% | 0.03 | 0.51 | 2.1% | 67.4% | 0.09 | 200 | 49 | 20 | 0.40 |
| mean_lookback | 52 | 3456 | 45.5% | -0.02 | 0.46 | 0.9% | 69.6% | 0.04 | 215 | 17 | 6 | 0.00 |
| std_lookback | 12 | 2880 | 36.5% | -0.10 | 0.38 | 1.1% | 99.8% | -0.10 | 413 | 31 | 20 | 0.30 |
| std_lookback | 17 | 2880 | 69.4% | 0.22 | 0.67 | 6.5% | 87.3% | 0.22 | 300 | 139 | 72 | 2.40 |
| std_lookback | 22 | 2880 | 83.2% | 0.35 | 0.72 | 8.4% | 69.1% | 0.35 | 193 | 203 | 62 | 3.30 |
| std_lookback | 27 | 2880 | 38.0% | -0.08 | 0.33 | 0.1% | 52.8% | 0.06 | 110 | 4 | 2 | 0.00 |
| std_lookback | 50 | 2880 | 20.1% | -0.28 | 0.20 | 0.0% | 35.7% | -0.31 | 58 | 0 | 0 | 0.00 |
| std_lookback | 75 | 2880 | 24.4% | -0.25 | 0.24 | 0.0% | 24.9% | -0.29 | 47 | 0 | 0 | 0.00 |
| entry_z | -2.5 | 4320 | 34.8% | -0.14 | 0.39 | 0.9% | 86.0% | -0.09 | 334 | 38 | 13 | 0.16 |
| entry_z | -3.0 | 4320 | 48.0% | -0.00 | 0.50 | 2.2% | 70.3% | 0.10 | 202 | 83 | 39 | 0.56 |
| entry_z | -3.5 | 4320 | 47.2% | -0.02 | 0.54 | 3.4% | 53.3% | 0.13 | 112 | 110 | 44 | 1.44 |
| entry_z | -4.0 | 4320 | 51.0% | 0.09 | 0.60 | 4.2% | 36.8% | 0.20 | 54 | 146 | 60 | 1.84 |
| exit_z | -1.5 | 5760 | 46.3% | -0.01 | 0.56 | 3.4% | 61.6% | 0.10 | 161 | 165 | 75 | 1.23 |
| exit_z | -1.0 | 5760 | 46.7% | -0.01 | 0.52 | 2.9% | 61.6% | 0.08 | 161 | 140 | 58 | 1.29 |
| exit_z | 0.0 | 5760 | 42.7% | -0.05 | 0.45 | 1.7% | 61.6% | 0.01 | 160 | 72 | 23 | 0.48 |
| max_holding_bars | 3 | 4320 | 46.9% | -0.01 | 0.48 | 1.9% | 61.7% | 0.05 | 161 | 80 | 22 | 0.72 |
| max_holding_bars | 5 | 4320 | 39.8% | -0.07 | 0.46 | 2.7% | 61.7% | -0.03 | 162 | 84 | 29 | 1.08 |
| max_holding_bars | 8 | 4320 | 45.3% | -0.02 | 0.54 | 3.0% | 61.5% | 0.07 | 161 | 96 | 44 | 0.92 |
| max_holding_bars | 12 | 4320 | 49.0% | 0.03 | 0.55 | 3.2% | 61.5% | 0.15 | 159 | 117 | 61 | 1.28 |
| entry_confirmation | none | 8640 | 51.1% | 0.03 | 0.48 | 2.4% | 79.7% | 0.03 | 277 | 204 | 74 | 1.20 |
| entry_confirmation | positive_bar_return | 8640 | 39.4% | -0.11 | 0.53 | 3.0% | 43.5% | 0.12 | 78 | 173 | 82 | 0.80 |
| stop_atr_multiple | none | 5760 | 47.9% | 0.01 | 0.52 | 2.3% | 58.1% | 0.12 | 140 | 118 | 53 | 0.84 |
| stop_atr_multiple | 1.3 | 5760 | 45.5% | -0.02 | 0.55 | 4.2% | 64.1% | 0.06 | 182 | 192 | 84 | 1.80 |
| stop_atr_multiple | 1.8 | 5760 | 42.4% | -0.06 | 0.45 | 1.6% | 62.7% | 0.00 | 166 | 67 | 19 | 0.36 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 15min | sma | 37 | 17 | -3.5 | -1.5 | 12 | positive_bar_return | 1.3 | 180 | 24.7% | 1.28 | -4.2% | s7 pass |
| 2 | 15min | sma | 32 | 17 | -4.0 | 0.0 | 12 | none | 1.3 | 198 | 28.2% | 1.20 | -4.7% | s7 pass |
| 3 | 15min | sma | 42 | 22 | -3.5 | -1.5 | 5 | none | 1.3 | 381 | 33.4% | 1.19 | -5.1% | s7 pass |
| 4 | 15min | sma | 42 | 22 | -4.0 | -1.0 | 3 | none | none | 199 | 23.3% | 1.18 | -2.9% | s6 deduplicated |
| 5 | 15min | ema | 47 | 17 | -4.0 | -1.5 | 12 | positive_bar_return | 1.3 | 102 | 19.2% | 1.17 | -3.4% | s7 pass |
| 6 | 15min | sma | 42 | 22 | -4.0 | 0.0 | 3 | none | none | 197 | 24.5% | 1.16 | -3.0% | s6 deduplicated |
| 7 | 15min | sma | 32 | 17 | -4.0 | -1.0 | 12 | none | 1.3 | 199 | 25.0% | 1.14 | -4.3% | s6 deduplicated |
| 8 | 15min | sma | 37 | 22 | -3.5 | -1.0 | 8 | none | none | 243 | 34.8% | 1.14 | -6.3% | s7 pass |
| 9 | 15min | sma | 37 | 17 | -3.5 | -1.5 | 8 | positive_bar_return | 1.3 | 178 | 20.9% | 1.14 | -4.2% | s7 pass |
| 10 | 15min | sma | 37 | 22 | -3.5 | -1.5 | 8 | none | none | 246 | 33.0% | 1.13 | -5.0% | s6 deduplicated |
| 11 | 15min | sma | 42 | 22 | -4.0 | -1.5 | 3 | none | none | 199 | 22.1% | 1.13 | -2.9% | s7 pass |
| 12 | 15min | sma | 37 | 17 | -3.5 | -1.0 | 12 | positive_bar_return | 1.3 | 180 | 23.2% | 1.11 | -4.2% | s7 pass |
| 13 | 15min | sma | 37 | 22 | -3.5 | -1.5 | 3 | none | 1.3 | 305 | 23.0% | 1.11 | -4.2% | s7 pass |
| 14 | 15min | sma | 32 | 17 | -4.0 | 0.0 | 12 | none | 1.8 | 181 | 26.6% | 1.10 | -6.5% | s7 pass |
| 15 | 15min | sma | 32 | 17 | -4.0 | -1.0 | 12 | none | 1.8 | 182 | 24.4% | 1.09 | -5.2% | s6 deduplicated |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
