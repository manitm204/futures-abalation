# Ablation (development only) -- mr_ym_v7_1h

- Symbol YM, strategy `mean_reversion_v15`, 23,328 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 14,506 configs (62.2%).
- Grid-wide: 62.5% profitable, median dev Sharpe 0.17, 1245 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 23328 | 23328 |  |
| 1 backtest integrity | 23328 | 23328 |  |
| 2 trade count & coverage | 23328 | 14506 |  |
| 3 performance & risk | 14506 | 634 |  |
| 4 parameter stability | 634 | 626 |  |
| 5 time stability | 626 | 626 |  |
| 6 deduplication | 626 | 324 | best 2 per cluster |
| 7 execution stress | 324 | 324 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 324 |  | diagnostic only: unverified: 324 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| entry_confirmation | 0.316 |
| mean_lookback | 0.285 |
| std_lookback | 0.180 |
| max_holding_bars | 0.115 |
| entry_z | 0.060 |
| mean_type | 0.055 |
| stop_atr_multiple | 0.053 |
| exit_z | 0.035 |
| timeframe | 0.000 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 1h | 23328 | 62.5% | 0.17 | 0.64 | 5.3% | 62.2% | 0.08 | 126 | 634 | 324 | 1.00 |
| mean_type | sma | 11664 | 60.3% | 0.15 | 0.62 | 4.8% | 67.4% | 0.08 | 135 | 310 | 161 | 0.80 |
| mean_type | ema | 11664 | 64.7% | 0.20 | 0.66 | 5.9% | 57.0% | 0.09 | 116 | 324 | 163 | 1.20 |
| mean_lookback | 15 | 2592 | 53.9% | 0.11 | 0.55 | 2.4% | 32.0% | -0.02 | 46 | 3 | 1 | 0.00 |
| mean_lookback | 25 | 2592 | 75.7% | 0.34 | 0.73 | 8.7% | 46.4% | 0.24 | 89 | 100 | 66 | 0.63 |
| mean_lookback | 35 | 2592 | 75.4% | 0.32 | 0.70 | 6.7% | 56.3% | 0.19 | 118 | 47 | 30 | 0.36 |
| mean_lookback | 45 | 2592 | 72.6% | 0.29 | 0.71 | 7.7% | 63.3% | 0.15 | 134 | 89 | 50 | 1.44 |
| mean_lookback | 75 | 2592 | 63.6% | 0.17 | 0.63 | 4.9% | 72.6% | 0.11 | 143 | 93 | 52 | 2.52 |
| mean_lookback | 85 | 2592 | 58.2% | 0.13 | 0.64 | 6.1% | 73.7% | 0.08 | 141 | 109 | 57 | 1.71 |
| mean_lookback | 95 | 2592 | 56.8% | 0.11 | 0.61 | 5.4% | 72.9% | 0.05 | 138 | 97 | 31 | 1.35 |
| mean_lookback | 105 | 2592 | 54.1% | 0.07 | 0.54 | 2.9% | 72.0% | 0.04 | 135 | 57 | 21 | 0.36 |
| mean_lookback | 115 | 2592 | 52.1% | 0.05 | 0.52 | 3.3% | 70.5% | 0.01 | 133 | 39 | 16 | 0.63 |
| std_lookback | 12 | 3888 | 56.6% | 0.12 | 0.61 | 4.9% | 83.8% | 0.09 | 177 | 153 | 90 | 1.86 |
| std_lookback | 17 | 3888 | 61.4% | 0.19 | 0.71 | 8.6% | 78.4% | 0.12 | 158 | 205 | 98 | 2.34 |
| std_lookback | 22 | 3888 | 53.1% | 0.08 | 0.58 | 3.2% | 74.8% | 0.03 | 149 | 92 | 40 | 0.78 |
| std_lookback | 50 | 3888 | 57.6% | 0.12 | 0.61 | 4.1% | 52.9% | 0.00 | 105 | 63 | 39 | 0.48 |
| std_lookback | 60 | 3888 | 70.3% | 0.24 | 0.66 | 5.0% | 45.5% | 0.10 | 92 | 58 | 33 | 0.18 |
| std_lookback | 80 | 3888 | 75.8% | 0.26 | 0.67 | 6.3% | 37.7% | 0.16 | 78 | 63 | 24 | 0.36 |
| entry_z | -1.5 | 7776 | 60.0% | 0.14 | 0.63 | 5.5% | 84.3% | 0.11 | 170 | 327 | 164 | 1.65 |
| entry_z | -2.0 | 7776 | 62.9% | 0.18 | 0.65 | 5.5% | 61.6% | 0.07 | 123 | 206 | 112 | 0.69 |
| entry_z | -2.5 | 7776 | 64.6% | 0.20 | 0.65 | 5.0% | 40.6% | 0.04 | 81 | 101 | 48 | 0.66 |
| exit_z | -1.0 | 7776 | 64.0% | 0.19 | 0.66 | 5.7% | 63.1% | 0.11 | 129 | 248 | 142 | 1.56 |
| exit_z | -0.5 | 7776 | 62.5% | 0.17 | 0.64 | 5.4% | 62.0% | 0.08 | 125 | 208 | 101 | 0.87 |
| exit_z | 0.0 | 7776 | 61.0% | 0.16 | 0.63 | 4.9% | 61.4% | 0.06 | 123 | 178 | 81 | 0.57 |
| max_holding_bars | 3 | 5832 | 54.1% | 0.09 | 0.67 | 6.0% | 63.9% | -0.10 | 126 | 142 | 66 | 0.32 |
| max_holding_bars | 5 | 5832 | 62.4% | 0.21 | 0.74 | 9.3% | 63.0% | 0.07 | 127 | 369 | 191 | 3.32 |
| max_holding_bars | 8 | 5832 | 64.7% | 0.18 | 0.62 | 4.3% | 61.7% | 0.09 | 126 | 76 | 35 | 0.28 |
| max_holding_bars | 12 | 5832 | 68.8% | 0.19 | 0.54 | 1.7% | 60.2% | 0.18 | 123 | 47 | 32 | 0.08 |
| entry_confirmation | none | 11664 | 46.5% | 0.01 | 0.50 | 1.7% | 81.8% | -0.05 | 180 | 82 | 56 | 0.08 |
| entry_confirmation | positive_bar_return | 11664 | 78.4% | 0.32 | 0.73 | 9.0% | 42.6% | 0.34 | 88 | 552 | 268 | 1.92 |
| stop_atr_multiple | none | 7776 | 59.5% | 0.15 | 0.64 | 4.6% | 44.8% | -0.01 | 93 | 75 | 36 | 0.27 |
| stop_atr_multiple | 0.75 | 7776 | 62.7% | 0.17 | 0.62 | 5.4% | 74.5% | 0.11 | 183 | 307 | 157 | 1.32 |
| stop_atr_multiple | 1.5 | 7776 | 65.2% | 0.20 | 0.67 | 6.1% | 67.3% | 0.11 | 133 | 252 | 131 | 1.41 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 1h | ema | 85 | 12 | -2.5 | -1.0 | 5 | positive_bar_return | 1.5 | 111 | 44.9% | 1.51 | -3.5% | s7 pass |
| 2 | 1h | ema | 95 | 12 | -2.5 | 0.0 | 5 | positive_bar_return | 1.5 | 106 | 45.4% | 1.45 | -3.3% | s7 pass |
| 3 | 1h | ema | 95 | 12 | -2.5 | -1.0 | 5 | positive_bar_return | 1.5 | 110 | 43.2% | 1.44 | -4.3% | s7 pass |
| 4 | 1h | ema | 85 | 12 | -2.5 | 0.0 | 5 | positive_bar_return | 1.5 | 108 | 43.2% | 1.42 | -3.4% | s7 pass |
| 5 | 1h | ema | 85 | 12 | -2.5 | -0.5 | 5 | positive_bar_return | 1.5 | 108 | 42.8% | 1.41 | -3.4% | s6 deduplicated |
| 6 | 1h | ema | 95 | 12 | -2.5 | -0.5 | 5 | positive_bar_return | 1.5 | 106 | 39.9% | 1.38 | -4.2% | s6 deduplicated |
| 7 | 1h | sma | 25 | 12 | -2.0 | -0.5 | 5 | positive_bar_return | 0.75 | 172 | 42.6% | 1.31 | -3.6% | s7 pass |
| 8 | 1h | ema | 75 | 12 | -2.5 | -1.0 | 5 | positive_bar_return | 1.5 | 111 | 38.3% | 1.28 | -4.2% | s7 pass |
| 9 | 1h | ema | 75 | 12 | -2.5 | 0.0 | 5 | positive_bar_return | 1.5 | 110 | 39.0% | 1.27 | -4.1% | s7 pass |
| 10 | 1h | sma | 25 | 12 | -2.0 | 0.0 | 5 | positive_bar_return | 0.75 | 171 | 44.1% | 1.27 | -3.6% | s7 pass |
| 11 | 1h | ema | 75 | 12 | -2.5 | -0.5 | 5 | positive_bar_return | 1.5 | 110 | 38.7% | 1.26 | -4.1% | s6 deduplicated |
| 12 | 1h | ema | 75 | 12 | -2.0 | -1.0 | 5 | positive_bar_return | 1.5 | 145 | 43.4% | 1.26 | -4.7% | s7 pass |
| 13 | 1h | sma | 75 | 17 | -1.5 | -1.0 | 5 | positive_bar_return | 1.5 | 147 | 35.4% | 1.25 | -5.9% | s7 pass |
| 14 | 1h | sma | 45 | 22 | -2.0 | -0.5 | 5 | positive_bar_return | 0.75 | 171 | 49.3% | 1.23 | -6.1% | s7 pass |
| 15 | 1h | ema | 105 | 12 | -2.5 | -1.0 | 5 | positive_bar_return | 1.5 | 110 | 34.2% | 1.22 | -2.9% | s7 pass |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
