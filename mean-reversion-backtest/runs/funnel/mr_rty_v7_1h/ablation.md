# Ablation (development only) -- mr_rty_v7_1h

- Symbol RTY, strategy `mean_reversion_v17`, 8,640 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 7,171 configs (83.0%).
- Grid-wide: 68.4% profitable, median dev Sharpe 0.22, 470 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 8640 | 8640 |  |
| 1 backtest integrity | 8640 | 8640 |  |
| 2 trade count & coverage | 8640 | 7171 |  |
| 3 performance & risk | 7171 | 299 |  |
| 4 parameter stability | 299 | 280 |  |
| 5 time stability | 280 | 280 |  |
| 6 deduplication | 280 | 162 | best 2 per cluster |
| 7 execution stress | 162 | 162 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 162 |  | diagnostic only: unverified: 162 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| mean_lookback | 0.307 |
| std_lookback | 0.250 |
| max_holding_bars | 0.160 |
| entry_confirmation | 0.091 |
| mean_type | 0.090 |
| stop_atr_multiple | 0.086 |
| exit_z | 0.056 |
| entry_z | 0.044 |
| timeframe | 0.000 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 1h | 8640 | 68.4% | 0.22 | 0.66 | 5.4% | 83.0% | 0.20 | 135 | 299 | 162 | 1.00 |
| mean_type | sma | 4320 | 74.1% | 0.26 | 0.68 | 6.6% | 84.3% | 0.24 | 136 | 179 | 100 | 1.38 |
| mean_type | ema | 4320 | 62.7% | 0.17 | 0.63 | 4.3% | 81.7% | 0.16 | 134 | 120 | 62 | 0.62 |
| mean_lookback | 70 | 1440 | 45.3% | 0.01 | 0.47 | 3.3% | 84.1% | 0.01 | 142 | 30 | 19 | 0.66 |
| mean_lookback | 80 | 1440 | 62.4% | 0.17 | 0.66 | 5.6% | 84.9% | 0.18 | 139 | 58 | 28 | 1.56 |
| mean_lookback | 90 | 1440 | 73.5% | 0.31 | 0.71 | 8.1% | 84.7% | 0.29 | 137 | 69 | 42 | 1.44 |
| mean_lookback | 100 | 1440 | 80.1% | 0.32 | 0.73 | 8.5% | 82.2% | 0.29 | 134 | 58 | 33 | 0.84 |
| mean_lookback | 110 | 1440 | 77.7% | 0.28 | 0.68 | 5.6% | 81.5% | 0.25 | 132 | 69 | 34 | 1.26 |
| mean_lookback | 120 | 1440 | 71.4% | 0.21 | 0.54 | 1.6% | 80.6% | 0.17 | 129 | 15 | 6 | 0.24 |
| std_lookback | 10 | 1728 | 63.1% | 0.16 | 0.57 | 3.1% | 92.8% | 0.15 | 153 | 40 | 26 | 0.55 |
| std_lookback | 12 | 1728 | 78.5% | 0.31 | 0.69 | 6.3% | 89.9% | 0.29 | 144 | 89 | 60 | 1.50 |
| std_lookback | 15 | 1728 | 79.1% | 0.35 | 0.74 | 9.3% | 82.3% | 0.31 | 133 | 93 | 49 | 1.45 |
| std_lookback | 18 | 1728 | 64.4% | 0.20 | 0.67 | 5.6% | 76.6% | 0.18 | 125 | 48 | 15 | 0.95 |
| std_lookback | 20 | 1728 | 56.8% | 0.10 | 0.52 | 2.9% | 73.4% | 0.09 | 122 | 29 | 12 | 0.55 |
| entry_z | -2.5 | 4320 | 71.6% | 0.24 | 0.68 | 6.2% | 88.0% | 0.23 | 143 | 180 | 95 | 1.40 |
| entry_z | -3.0 | 4320 | 65.2% | 0.20 | 0.63 | 4.7% | 78.0% | 0.17 | 129 | 119 | 67 | 0.60 |
| exit_z | -1.0 | 2880 | 64.8% | 0.19 | 0.60 | 3.5% | 83.4% | 0.16 | 136 | 63 | 23 | 0.54 |
| exit_z | 0.0 | 2880 | 70.1% | 0.24 | 0.69 | 6.8% | 82.9% | 0.22 | 135 | 129 | 83 | 1.38 |
| exit_z | 1.0 | 2880 | 70.4% | 0.24 | 0.67 | 6.0% | 82.7% | 0.22 | 135 | 107 | 56 | 1.08 |
| max_holding_bars | 5 | 2880 | 58.0% | 0.11 | 0.59 | 4.2% | 85.1% | 0.09 | 136 | 72 | 30 | 0.72 |
| max_holding_bars | 8 | 2880 | 73.7% | 0.26 | 0.70 | 7.4% | 81.6% | 0.25 | 135 | 140 | 68 | 1.56 |
| max_holding_bars | 12 | 2880 | 73.6% | 0.27 | 0.66 | 4.7% | 82.3% | 0.25 | 134 | 87 | 64 | 0.72 |
| entry_confirmation | none | 4320 | 64.0% | 0.18 | 0.61 | 3.4% | 99.0% | 0.18 | 163 | 145 | 84 | 0.82 |
| entry_confirmation | positive_bar_return | 4320 | 72.8% | 0.27 | 0.70 | 7.4% | 67.0% | 0.24 | 111 | 154 | 78 | 1.18 |
| stop_atr_multiple | none | 2160 | 73.2% | 0.28 | 0.74 | 9.5% | 56.1% | 0.20 | 104 | 80 | 48 | 1.12 |
| stop_atr_multiple | 1.5 | 2160 | 66.9% | 0.19 | 0.57 | 1.9% | 98.2% | 0.20 | 169 | 42 | 23 | 0.64 |
| stop_atr_multiple | 2.0 | 2160 | 64.9% | 0.19 | 0.61 | 4.0% | 94.8% | 0.20 | 147 | 86 | 36 | 0.88 |
| stop_atr_multiple | 2.5 | 2160 | 68.6% | 0.23 | 0.68 | 6.3% | 82.9% | 0.20 | 133 | 91 | 55 | 1.36 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 1h | sma | 80 | 18 | -2.5 | 0.0 | 8 | positive_bar_return | 2.5 | 101 | 60.9% | 1.37 | -7.3% | s7 pass |
| 2 | 1h | sma | 80 | 18 | -2.5 | -1.0 | 8 | positive_bar_return | 2.5 | 102 | 53.7% | 1.27 | -7.9% | s6 deduplicated |
| 3 | 1h | sma | 90 | 10 | -2.5 | 0.0 | 12 | none | none | 118 | 72.5% | 1.21 | -7.8% | s7 pass |
| 4 | 1h | sma | 90 | 15 | -2.5 | 1.0 | 5 | positive_bar_return | 1.5 | 124 | 47.2% | 1.20 | -4.9% | s6 deduplicated |
| 5 | 1h | sma | 90 | 15 | -2.5 | 0.0 | 5 | positive_bar_return | 1.5 | 124 | 47.2% | 1.20 | -4.9% | s7 pass |
| 6 | 1h | sma | 80 | 18 | -2.5 | 1.0 | 8 | positive_bar_return | 2.5 | 101 | 52.9% | 1.18 | -7.2% | s7 pass |
| 7 | 1h | sma | 80 | 18 | -2.5 | 0.0 | 8 | positive_bar_return | 2.0 | 114 | 53.0% | 1.16 | -11.2% | s6 deduplicated |
| 8 | 1h | sma | 100 | 15 | -3.0 | 0.0 | 12 | none | none | 104 | 59.3% | 1.13 | -11.9% | s7 pass |
| 9 | 1h | sma | 80 | 12 | -3.0 | 0.0 | 8 | positive_bar_return | 2.5 | 117 | 52.9% | 1.12 | -7.4% | s7 pass |
| 10 | 1h | sma | 70 | 12 | -2.5 | 1.0 | 8 | positive_bar_return | none | 100 | 54.4% | 1.10 | -9.2% | s7 pass |
| 11 | 1h | sma | 110 | 15 | -3.0 | 0.0 | 12 | none | none | 100 | 54.8% | 1.09 | -8.7% | s7 pass |
| 12 | 1h | sma | 90 | 15 | -2.5 | 0.0 | 8 | positive_bar_return | 2.5 | 102 | 48.0% | 1.08 | -8.3% | s7 pass |
| 13 | 1h | ema | 110 | 12 | -2.5 | -1.0 | 8 | positive_bar_return | 2.5 | 110 | 47.5% | 1.07 | -7.9% | s7 pass |
| 14 | 1h | sma | 90 | 15 | -2.5 | 1.0 | 8 | positive_bar_return | 2.5 | 102 | 47.0% | 1.07 | -8.1% | s7 pass |
| 15 | 1h | sma | 80 | 15 | -3.0 | 0.0 | 8 | none | 2.5 | 153 | 61.4% | 1.07 | -9.6% | s7 pass |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
