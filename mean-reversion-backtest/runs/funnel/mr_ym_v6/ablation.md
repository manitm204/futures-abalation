# Ablation (development only) -- mr_ym_v6

- Symbol YM, strategy `mean_reversion_v7`, 72,000 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 54,408 configs (75.6%).
- Grid-wide: 44.7% profitable, median dev Sharpe 0.00, 1703 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 72000 | 72000 |  |
| 1 backtest integrity | 72000 | 72000 |  |
| 2 trade count & coverage | 72000 | 54408 |  |
| 3 performance & risk | 54408 | 860 |  |
| 4 parameter stability | 860 | 844 |  |
| 5 time stability | 844 | 843 |  |
| 6 deduplication | 843 | 267 | best 2 per cluster |
| 7 execution stress | 267 | 267 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 267 |  | diagnostic only: unverified: 267 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| timeframe | 0.212 |
| std_lookback | 0.195 |
| entry_z | 0.158 |
| entry_confirmation | 0.156 |
| mean_lookback | 0.120 |
| max_holding_bars | 0.075 |
| stop_atr_multiple | 0.074 |
| mean_type | 0.039 |
| exit_z | 0.030 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 15min | 36000 | 34.6% | -0.11 | 0.35 | 0.6% | 91.0% | -0.11 | 540 | 176 | 59 | 0.44 |
| timeframe | 1h | 36000 | 54.8% | 0.10 | 0.58 | 4.1% | 60.2% | 0.06 | 125 | 684 | 208 | 1.56 |
| mean_type | sma | 36000 | 43.2% | -0.02 | 0.46 | 2.4% | 79.6% | -0.05 | 268 | 436 | 129 | 0.70 |
| mean_type | ema | 36000 | 46.2% | 0.02 | 0.47 | 2.3% | 71.6% | -0.01 | 210 | 424 | 138 | 1.30 |
| mean_lookback | 20 | 12000 | 37.7% | -0.07 | 0.47 | 2.3% | 51.3% | -0.17 | 105 | 92 | 21 | 1.26 |
| mean_lookback | 30 | 12000 | 48.5% | 0.03 | 0.60 | 5.0% | 66.3% | -0.02 | 196 | 204 | 65 | 1.14 |
| mean_lookback | 40 | 12000 | 51.3% | 0.05 | 0.50 | 2.2% | 77.2% | 0.01 | 255 | 158 | 46 | 1.38 |
| mean_lookback | 50 | 12000 | 45.7% | 0.01 | 0.44 | 1.5% | 82.2% | -0.03 | 281 | 90 | 28 | 0.30 |
| mean_lookback | 80 | 12000 | 43.5% | -0.01 | 0.41 | 1.3% | 88.2% | -0.01 | 316 | 147 | 58 | 1.74 |
| mean_lookback | 100 | 12000 | 41.6% | -0.03 | 0.40 | 1.8% | 88.1% | -0.05 | 309 | 169 | 49 | 0.18 |
| std_lookback | 10 | 18000 | 33.2% | -0.11 | 0.34 | 1.1% | 88.7% | -0.12 | 338 | 176 | 84 | 0.64 |
| std_lookback | 15 | 18000 | 49.7% | 0.04 | 0.54 | 4.2% | 77.2% | -0.02 | 259 | 334 | 90 | 1.48 |
| std_lookback | 20 | 18000 | 53.1% | 0.09 | 0.54 | 3.4% | 71.4% | 0.04 | 209 | 291 | 73 | 1.88 |
| std_lookback | 25 | 18000 | 42.8% | -0.01 | 0.44 | 0.8% | 65.0% | -0.02 | 174 | 59 | 20 | 0.00 |
| entry_z | -1.75 | 14400 | 36.1% | -0.09 | 0.44 | 2.9% | 94.7% | -0.11 | 407 | 313 | 92 | 2.40 |
| entry_z | -2.0 | 14400 | 40.2% | -0.05 | 0.45 | 3.0% | 90.2% | -0.08 | 344 | 240 | 65 | 1.50 |
| entry_z | -2.5 | 14400 | 46.1% | 0.01 | 0.46 | 1.7% | 77.2% | -0.01 | 234 | 122 | 49 | 0.00 |
| entry_z | -3.0 | 14400 | 51.3% | 0.07 | 0.48 | 2.4% | 63.7% | 0.04 | 168 | 99 | 33 | 0.85 |
| entry_z | -3.5 | 14400 | 49.8% | 0.06 | 0.51 | 1.8% | 52.1% | 0.04 | 107 | 86 | 28 | 0.25 |
| exit_z | -1.0 | 14400 | 46.8% | 0.02 | 0.50 | 2.7% | 76.0% | -0.02 | 242 | 206 | 88 | 1.30 |
| exit_z | -0.5 | 14400 | 46.2% | 0.01 | 0.49 | 2.5% | 75.7% | -0.02 | 237 | 194 | 67 | 0.90 |
| exit_z | 0.0 | 14400 | 43.8% | -0.01 | 0.46 | 2.3% | 75.5% | -0.05 | 234 | 161 | 37 | 1.00 |
| exit_z | 0.5 | 14400 | 43.4% | -0.01 | 0.45 | 2.3% | 75.4% | -0.04 | 233 | 153 | 45 | 0.90 |
| exit_z | 1.0 | 14400 | 43.4% | -0.01 | 0.45 | 2.0% | 75.3% | -0.04 | 232 | 146 | 30 | 0.90 |
| max_holding_bars | 5 | 24000 | 42.0% | -0.04 | 0.58 | 4.5% | 76.3% | -0.11 | 236 | 644 | 185 | 2.46 |
| max_holding_bars | 10 | 24000 | 47.7% | 0.03 | 0.46 | 1.5% | 75.7% | 0.01 | 236 | 135 | 51 | 0.45 |
| max_holding_bars | 15 | 24000 | 44.4% | 0.01 | 0.40 | 1.0% | 74.7% | -0.01 | 234 | 81 | 31 | 0.09 |
| entry_confirmation | none | 36000 | 36.6% | -0.07 | 0.34 | 0.4% | 88.7% | -0.10 | 347 | 72 | 35 | 0.00 |
| entry_confirmation | positive_bar_return | 36000 | 52.8% | 0.09 | 0.59 | 4.4% | 62.5% | 0.06 | 145 | 788 | 232 | 2.00 |
| stop_atr_multiple | none | 14400 | 49.6% | 0.04 | 0.50 | 2.4% | 65.4% | 0.00 | 153 | 87 | 38 | 0.40 |
| stop_atr_multiple | 0.75 | 14400 | 42.5% | -0.02 | 0.46 | 2.8% | 80.3% | -0.05 | 333 | 290 | 97 | 1.40 |
| stop_atr_multiple | 1.0 | 14400 | 41.4% | -0.03 | 0.45 | 2.2% | 79.4% | -0.08 | 287 | 163 | 40 | 1.20 |
| stop_atr_multiple | 1.5 | 14400 | 45.9% | 0.02 | 0.48 | 2.6% | 77.2% | -0.01 | 232 | 203 | 71 | 1.30 |
| stop_atr_multiple | 2.0 | 14400 | 44.1% | 0.00 | 0.43 | 1.8% | 75.4% | -0.03 | 204 | 117 | 21 | 0.70 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 1h | ema | 80 | 10 | -1.75 | -1.0 | 5 | positive_bar_return | 1.5 | 155 | 48.5% | 1.45 | -4.6% | s7 pass |
| 2 | 1h | sma | 30 | 20 | -2.0 | -1.0 | 5 | positive_bar_return | 0.75 | 108 | 53.1% | 1.42 | -4.0% | s7 pass |
| 3 | 1h | sma | 20 | 15 | -1.75 | 0.5 | 10 | positive_bar_return | none | 106 | 63.7% | 1.41 | -7.3% | s7 pass |
| 4 | 1h | sma | 30 | 20 | -2.0 | -1.0 | 5 | positive_bar_return | 1.0 | 102 | 59.2% | 1.40 | -6.9% | s7 pass |
| 5 | 1h | sma | 30 | 20 | -2.0 | 0.0 | 5 | positive_bar_return | 0.75 | 108 | 53.2% | 1.40 | -4.9% | s6 deduplicated |
| 6 | 1h | sma | 30 | 20 | -2.0 | 0.0 | 5 | positive_bar_return | 1.0 | 102 | 56.3% | 1.38 | -7.1% | s6 deduplicated |
| 7 | 1h | sma | 30 | 20 | -2.0 | -0.5 | 5 | positive_bar_return | 0.75 | 108 | 51.7% | 1.37 | -4.9% | s6 deduplicated |
| 8 | 1h | sma | 30 | 20 | -2.0 | -0.5 | 5 | positive_bar_return | 1.0 | 102 | 55.2% | 1.37 | -7.1% | s6 deduplicated |
| 9 | 1h | sma | 30 | 20 | -2.0 | 0.5 | 5 | positive_bar_return | 0.75 | 108 | 51.1% | 1.34 | -4.9% | s6 deduplicated |
| 10 | 1h | sma | 30 | 20 | -2.0 | 0.5 | 5 | positive_bar_return | 1.0 | 102 | 54.3% | 1.34 | -7.1% | s6 deduplicated |
| 11 | 1h | sma | 30 | 20 | -2.0 | 1.0 | 5 | positive_bar_return | 0.75 | 108 | 50.6% | 1.34 | -4.9% | s6 deduplicated |
| 12 | 15min | ema | 40 | 20 | -3.0 | -1.0 | 5 | positive_bar_return | 0.75 | 127 | 16.1% | 1.33 | -1.3% | s7 pass |
| 13 | 1h | sma | 30 | 20 | -2.0 | 1.0 | 5 | positive_bar_return | 1.0 | 102 | 53.2% | 1.32 | -7.1% | s6 deduplicated |
| 14 | 1h | sma | 20 | 15 | -1.75 | 0.0 | 10 | positive_bar_return | none | 106 | 57.1% | 1.31 | -7.1% | s6 deduplicated |
| 15 | 1h | ema | 80 | 10 | -1.75 | -1.0 | 5 | positive_bar_return | 0.75 | 207 | 42.5% | 1.31 | -4.3% | s7 pass |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
