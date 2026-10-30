# Ablation (development only) -- mr_gc_v5

- Symbol GC, strategy `mean_reversion_v5`, 41,472 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 29,344 configs (70.8%).
- Grid-wide: 27.8% profitable, median dev Sharpe -0.32, 581 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 41472 | 41472 |  |
| 1 backtest integrity | 41472 | 41472 |  |
| 2 trade count & coverage | 41472 | 29344 |  |
| 3 performance & risk | 29344 | 177 |  |
| 4 parameter stability | 177 | 162 |  |
| 5 time stability | 162 | 162 |  |
| 6 deduplication | 162 | 89 | best 2 per cluster |
| 7 execution stress | 89 | 89 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 89 |  | diagnostic only: unverified: 89 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| timeframe | 0.845 |
| entry_confirmation | 0.198 |
| std_lookback | 0.176 |
| stop_atr_multiple | 0.134 |
| max_holding_bars | 0.126 |
| entry_z | 0.125 |
| mean_lookback | 0.123 |
| exit_z | 0.085 |
| mean_type | 0.071 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 5min | 13824 | 6.3% | -0.71 | -0.12 | 0.1% | 95.7% | -0.73 | 856 | 11 | 5 | 0.12 |
| timeframe | 15min | 13824 | 16.6% | -0.38 | 0.15 | 0.6% | 80.2% | -0.43 | 293 | 49 | 26 | 1.14 |
| timeframe | 1h | 13824 | 60.6% | 0.14 | 0.58 | 3.5% | 36.3% | 0.12 | 72 | 117 | 58 | 1.74 |
| mean_type | sma | 20736 | 26.3% | -0.36 | 0.36 | 1.4% | 73.7% | -0.51 | 254 | 103 | 49 | 1.10 |
| mean_type | ema | 20736 | 29.3% | -0.29 | 0.38 | 1.4% | 67.8% | -0.47 | 208 | 74 | 40 | 0.90 |
| mean_lookback | 20 | 6912 | 24.8% | -0.32 | 0.32 | 1.3% | 53.7% | -0.48 | 118 | 29 | 16 | 1.08 |
| mean_lookback | 30 | 6912 | 27.4% | -0.32 | 0.36 | 1.0% | 64.3% | -0.49 | 186 | 27 | 16 | 0.84 |
| mean_lookback | 40 | 6912 | 28.1% | -0.34 | 0.39 | 1.5% | 72.7% | -0.49 | 235 | 35 | 17 | 0.84 |
| mean_lookback | 50 | 6912 | 30.3% | -0.27 | 0.41 | 1.8% | 75.4% | -0.43 | 279 | 46 | 20 | 1.92 |
| mean_lookback | 60 | 6912 | 30.3% | -0.30 | 0.38 | 1.5% | 77.7% | -0.48 | 315 | 25 | 12 | 0.78 |
| mean_lookback | 80 | 6912 | 25.9% | -0.40 | 0.34 | 1.2% | 80.7% | -0.53 | 341 | 15 | 8 | 0.54 |
| std_lookback | 10 | 5184 | 20.0% | -0.39 | 0.21 | 0.5% | 93.7% | -0.43 | 509 | 26 | 14 | 1.36 |
| std_lookback | 15 | 5184 | 34.0% | -0.26 | 0.43 | 2.0% | 86.1% | -0.38 | 435 | 45 | 25 | 2.64 |
| std_lookback | 20 | 5184 | 37.2% | -0.22 | 0.52 | 3.0% | 80.0% | -0.39 | 351 | 57 | 24 | 2.32 |
| std_lookback | 25 | 5184 | 30.0% | -0.40 | 0.51 | 3.2% | 72.2% | -0.58 | 271 | 28 | 16 | 0.72 |
| std_lookback | 30 | 5184 | 25.0% | -0.37 | 0.31 | 0.6% | 68.8% | -0.51 | 231 | 8 | 4 | 0.08 |
| std_lookback | 40 | 5184 | 27.2% | -0.28 | 0.29 | 0.4% | 63.6% | -0.40 | 185 | 13 | 6 | 0.88 |
| std_lookback | 60 | 5184 | 20.6% | -0.34 | 0.18 | 0.1% | 55.0% | -0.56 | 116 | 0 | 0 | 0.00 |
| std_lookback | 80 | 5184 | 28.5% | -0.28 | 0.38 | 1.4% | 46.8% | -0.71 | 86 | 0 | 0 | 0.00 |
| entry_z | -2.0 | 13824 | 25.4% | -0.40 | 0.34 | 1.1% | 83.7% | -0.52 | 373 | 46 | 27 | 0.84 |
| entry_z | -2.5 | 13824 | 28.9% | -0.30 | 0.37 | 1.7% | 70.7% | -0.47 | 232 | 67 | 35 | 1.17 |
| entry_z | -3.0 | 13824 | 29.0% | -0.28 | 0.39 | 1.4% | 57.9% | -0.45 | 139 | 64 | 27 | 0.99 |
| exit_z | -1.0 | 10368 | 25.5% | -0.37 | 0.34 | 1.2% | 70.9% | -0.54 | 235 | 28 | 14 | 0.64 |
| exit_z | -0.5 | 10368 | 27.3% | -0.33 | 0.36 | 1.3% | 70.7% | -0.49 | 233 | 39 | 10 | 0.88 |
| exit_z | 0.0 | 10368 | 29.0% | -0.30 | 0.38 | 1.4% | 70.7% | -0.46 | 233 | 49 | 30 | 1.04 |
| exit_z | 0.5 | 10368 | 29.4% | -0.29 | 0.39 | 1.6% | 70.7% | -0.45 | 233 | 61 | 35 | 1.44 |
| max_holding_bars | 5 | 20736 | 24.5% | -0.39 | 0.32 | 1.0% | 71.0% | -0.55 | 232 | 54 | 21 | 0.60 |
| max_holding_bars | 10 | 20736 | 31.1% | -0.26 | 0.41 | 1.8% | 70.5% | -0.42 | 235 | 123 | 68 | 1.40 |
| entry_confirmation | none | 20736 | 21.3% | -0.42 | 0.24 | 0.5% | 82.4% | -0.52 | 376 | 92 | 43 | 0.80 |
| entry_confirmation | positive_bar_return | 20736 | 34.3% | -0.22 | 0.47 | 2.3% | 59.1% | -0.44 | 141 | 85 | 46 | 1.20 |
| stop_atr_multiple | none | 13824 | 29.5% | -0.26 | 0.41 | 1.9% | 66.0% | -0.39 | 189 | 56 | 22 | 1.08 |
| stop_atr_multiple | 1.0 | 13824 | 24.2% | -0.40 | 0.29 | 0.5% | 75.3% | -0.54 | 277 | 33 | 13 | 0.51 |
| stop_atr_multiple | 2.0 | 13824 | 29.7% | -0.35 | 0.41 | 1.9% | 71.0% | -0.53 | 224 | 88 | 54 | 1.41 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 1h | sma | 40 | 15 | -2.5 | 0.0 | 10 | positive_bar_return | 2.0 | 105 | 34.8% | 1.19 | -5.4% | s7 pass |
| 2 | 1h | ema | 50 | 20 | -2.5 | 0.5 | 10 | none | none | 118 | 36.8% | 1.17 | -6.4% | s6 deduplicated |
| 3 | 1h | ema | 50 | 20 | -2.5 | 0.5 | 10 | none | 2.0 | 144 | 36.2% | 1.16 | -7.6% | s7 pass |
| 4 | 15min | ema | 60 | 10 | -3.0 | 0.5 | 5 | positive_bar_return | none | 363 | 22.1% | 1.16 | -2.9% | s7 pass |
| 5 | 1h | sma | 40 | 15 | -2.5 | 0.5 | 10 | positive_bar_return | 2.0 | 105 | 34.0% | 1.15 | -5.4% | s7 pass |
| 6 | 1h | sma | 80 | 40 | -2.0 | 0.5 | 10 | positive_bar_return | 2.0 | 107 | 39.0% | 1.13 | -6.4% | s7 pass |
| 7 | 15min | ema | 60 | 10 | -3.0 | 0.0 | 5 | positive_bar_return | none | 363 | 21.1% | 1.11 | -2.8% | s7 pass |
| 8 | 15min | sma | 50 | 15 | -3.0 | 0.0 | 10 | positive_bar_return | none | 280 | 29.1% | 1.10 | -5.1% | s6 deduplicated |
| 9 | 1h | ema | 50 | 20 | -2.5 | 0.0 | 10 | none | none | 119 | 33.0% | 1.10 | -6.5% | s6 deduplicated |
| 10 | 1h | sma | 80 | 40 | -2.0 | 0.0 | 10 | positive_bar_return | 2.0 | 107 | 36.6% | 1.08 | -6.4% | s7 pass |
| 11 | 1h | ema | 50 | 20 | -2.5 | 0.0 | 5 | none | 2.0 | 146 | 23.7% | 1.06 | -3.8% | s7 pass |
| 12 | 1h | ema | 50 | 20 | -2.5 | -0.5 | 10 | none | none | 121 | 30.7% | 1.05 | -6.4% | s6 deduplicated |
| 13 | 1h | ema | 50 | 20 | -2.5 | 0.5 | 5 | none | 2.0 | 146 | 23.3% | 1.04 | -3.8% | s7 pass |
| 14 | 1h | ema | 50 | 20 | -2.5 | 0.0 | 10 | none | 2.0 | 146 | 30.8% | 1.04 | -7.7% | s7 pass |
| 15 | 1h | sma | 60 | 15 | -3.0 | 0.5 | 10 | none | 2.0 | 137 | 29.4% | 1.04 | -5.2% | s7 pass |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
