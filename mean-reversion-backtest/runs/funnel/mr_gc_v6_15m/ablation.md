# Ablation (development only) -- mr_gc_v6_15m

- Symbol GC, strategy `mean_reversion_v19`, 21,504 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 15,700 configs (73.0%).
- Grid-wide: 46.0% profitable, median dev Sharpe 0.01, 1311 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 21504 | 21504 |  |
| 1 backtest integrity | 21504 | 21504 |  |
| 2 trade count & coverage | 21504 | 15700 |  |
| 3 performance & risk | 15700 | 739 |  |
| 4 parameter stability | 739 | 733 |  |
| 5 time stability | 733 | 732 |  |
| 6 deduplication | 732 | 221 | best 2 per cluster |
| 7 execution stress | 221 | 221 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 221 |  | diagnostic only: unverified: 221 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| std_lookback | 0.562 |
| mean_lookback | 0.552 |
| entry_z | 0.480 |
| max_holding_bars | 0.322 |
| mean_type | 0.207 |
| stop_atr_multiple | 0.121 |
| exit_z | 0.043 |
| timeframe | 0.000 |
| entry_confirmation | 0.000 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 15min | 21504 | 46.0% | 0.01 | 0.66 | 6.1% | 73.0% | -0.03 | 286 | 739 | 221 | 1.00 |
| mean_type | sma | 10752 | 39.0% | -0.10 | 0.63 | 5.0% | 75.4% | -0.11 | 332 | 389 | 112 | 1.24 |
| mean_type | ema | 10752 | 53.1% | 0.11 | 0.70 | 7.2% | 70.6% | 0.04 | 242 | 350 | 109 | 0.76 |
| mean_lookback | 12 | 3072 | 20.7% | -0.22 | 0.31 | 0.0% | 20.8% | -0.32 | 19 | 0 | 0 | 0.00 |
| mean_lookback | 16 | 3072 | 37.3% | -0.10 | 0.54 | 1.1% | 49.6% | -0.21 | 97 | 17 | 5 | 0.14 |
| mean_lookback | 20 | 3072 | 52.8% | 0.10 | 0.71 | 7.8% | 67.2% | -0.01 | 195 | 103 | 34 | 1.12 |
| mean_lookback | 25 | 3072 | 67.9% | 0.33 | 0.89 | 19.1% | 82.7% | 0.21 | 304 | 291 | 86 | 3.08 |
| mean_lookback | 30 | 3072 | 66.3% | 0.22 | 0.74 | 9.4% | 91.7% | 0.17 | 363 | 171 | 48 | 1.12 |
| mean_lookback | 40 | 3072 | 40.9% | -0.09 | 0.52 | 2.7% | 99.1% | -0.09 | 428 | 78 | 23 | 0.70 |
| mean_lookback | 50 | 3072 | 36.2% | -0.12 | 0.46 | 2.6% | 100.0% | -0.12 | 443 | 79 | 25 | 0.84 |
| std_lookback | 6 | 3584 | 19.9% | -0.26 | 0.18 | 0.0% | 100.0% | -0.26 | 508 | 1 | 1 | 0.00 |
| std_lookback | 8 | 3584 | 38.2% | -0.16 | 0.46 | 2.3% | 89.0% | -0.17 | 397 | 82 | 26 | 0.78 |
| std_lookback | 10 | 3584 | 42.2% | -0.08 | 0.56 | 4.1% | 77.2% | -0.04 | 312 | 148 | 51 | 2.46 |
| std_lookback | 12 | 3584 | 63.8% | 0.31 | 0.72 | 6.9% | 69.5% | 0.30 | 224 | 221 | 75 | 0.66 |
| std_lookback | 15 | 3584 | 58.5% | 0.26 | 0.84 | 11.7% | 55.4% | 0.29 | 130 | 175 | 39 | 1.80 |
| std_lookback | 18 | 3584 | 53.4% | 0.29 | 0.83 | 11.6% | 47.0% | 0.13 | 83 | 112 | 29 | 0.30 |
| entry_z | -2.0 | 5376 | 26.7% | -0.24 | 0.31 | 1.0% | 88.1% | -0.24 | 433 | 55 | 12 | 0.40 |
| entry_z | -2.5 | 5376 | 47.2% | 0.01 | 0.65 | 5.7% | 74.7% | -0.03 | 320 | 174 | 66 | 0.56 |
| entry_z | -3.0 | 5376 | 53.7% | 0.17 | 0.73 | 7.9% | 67.9% | 0.16 | 236 | 287 | 78 | 1.84 |
| entry_z | -3.5 | 5376 | 56.5% | 0.24 | 0.78 | 9.8% | 61.4% | 0.21 | 174 | 223 | 65 | 1.20 |
| exit_z | -1.0 | 5376 | 44.2% | -0.02 | 0.67 | 6.5% | 73.0% | -0.05 | 287 | 204 | 72 | 1.00 |
| exit_z | -0.5 | 5376 | 46.9% | 0.03 | 0.68 | 6.4% | 73.0% | -0.02 | 286 | 201 | 57 | 1.20 |
| exit_z | 0.0 | 5376 | 46.8% | 0.02 | 0.67 | 6.4% | 73.0% | -0.02 | 286 | 201 | 55 | 1.16 |
| exit_z | 0.5 | 5376 | 46.2% | 0.01 | 0.65 | 5.1% | 73.0% | -0.02 | 286 | 133 | 37 | 0.64 |
| max_holding_bars | 5 | 5376 | 36.2% | -0.17 | 0.58 | 3.7% | 73.1% | -0.21 | 292 | 69 | 20 | 0.16 |
| max_holding_bars | 8 | 5376 | 43.6% | -0.04 | 0.66 | 6.6% | 73.0% | -0.09 | 289 | 183 | 50 | 0.84 |
| max_holding_bars | 10 | 5376 | 46.9% | 0.03 | 0.68 | 6.1% | 73.0% | -0.03 | 285 | 205 | 56 | 0.68 |
| max_holding_bars | 14 | 5376 | 57.4% | 0.16 | 0.72 | 8.0% | 72.9% | 0.14 | 278 | 282 | 95 | 2.32 |
| entry_confirmation | positive_bar_return | 21504 | 46.0% | 0.01 | 0.66 | 6.1% | 73.0% | -0.03 | 286 | 739 | 221 | 1.00 |
| stop_atr_multiple | none | 5376 | 51.0% | 0.09 | 0.70 | 7.3% | 72.3% | 0.03 | 253 | 280 | 100 | 2.24 |
| stop_atr_multiple | 1.0 | 5376 | 42.9% | -0.03 | 0.59 | 4.5% | 73.5% | -0.07 | 350 | 83 | 19 | 0.44 |
| stop_atr_multiple | 1.5 | 5376 | 43.8% | -0.03 | 0.65 | 5.3% | 73.2% | -0.05 | 310 | 136 | 13 | 0.40 |
| stop_atr_multiple | 2.0 | 5376 | 46.5% | 0.02 | 0.71 | 7.3% | 73.0% | -0.03 | 288 | 240 | 89 | 0.92 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 15min | sma | 25 | 10 | -3.0 | 0.0 | 14 | positive_bar_return | 2.0 | 320 | 33.8% | 1.31 | -4.7% | s7 pass |
| 2 | 15min | sma | 25 | 10 | -3.0 | -0.5 | 14 | positive_bar_return | 2.0 | 320 | 31.1% | 1.27 | -4.5% | s7 pass |
| 3 | 15min | sma | 25 | 10 | -3.0 | 0.5 | 14 | positive_bar_return | none | 286 | 34.5% | 1.26 | -5.1% | s6 deduplicated |
| 4 | 15min | sma | 25 | 10 | -3.0 | 0.5 | 14 | positive_bar_return | 2.0 | 320 | 32.8% | 1.26 | -4.8% | s6 deduplicated |
| 5 | 15min | sma | 20 | 8 | -3.5 | 0.5 | 14 | positive_bar_return | none | 259 | 27.7% | 1.22 | -6.5% | s7 pass |
| 6 | 15min | sma | 25 | 10 | -3.0 | 0.0 | 14 | positive_bar_return | none | 288 | 33.0% | 1.21 | -4.9% | s7 pass |
| 7 | 15min | sma | 30 | 10 | -3.5 | -1.0 | 14 | positive_bar_return | none | 268 | 30.3% | 1.19 | -5.6% | s7 pass |
| 8 | 15min | sma | 25 | 10 | -3.0 | -0.5 | 14 | positive_bar_return | none | 288 | 30.2% | 1.17 | -5.5% | s6 deduplicated |
| 9 | 15min | sma | 30 | 10 | -3.5 | -0.5 | 14 | positive_bar_return | none | 267 | 29.8% | 1.14 | -5.6% | s6 deduplicated |
| 10 | 15min | ema | 25 | 8 | -3.5 | 0.0 | 14 | positive_bar_return | none | 242 | 27.9% | 1.13 | -5.9% | s7 pass |
| 11 | 15min | sma | 50 | 15 | -3.0 | 0.0 | 8 | positive_bar_return | none | 291 | 30.2% | 1.13 | -4.4% | s6 deduplicated |
| 12 | 15min | sma | 25 | 10 | -3.0 | 0.0 | 14 | positive_bar_return | 1.5 | 344 | 28.6% | 1.13 | -5.8% | s7 pass |
| 13 | 15min | sma | 40 | 10 | -3.5 | -0.5 | 14 | positive_bar_return | none | 302 | 30.6% | 1.12 | -6.3% | s7 pass |
| 14 | 15min | sma | 30 | 10 | -3.0 | -0.5 | 14 | positive_bar_return | none | 304 | 31.0% | 1.12 | -6.1% | s6 deduplicated |
| 15 | 15min | sma | 30 | 10 | -3.0 | -1.0 | 14 | positive_bar_return | none | 306 | 29.7% | 1.11 | -6.1% | s6 deduplicated |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
