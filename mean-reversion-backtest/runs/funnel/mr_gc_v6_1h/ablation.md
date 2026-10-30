# Ablation (development only) -- mr_gc_v6_1h

- Symbol GC, strategy `mean_reversion_v20`, 17,280 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 10,945 configs (63.3%).
- Grid-wide: 82.7% profitable, median dev Sharpe 0.34, 1714 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 17280 | 17280 |  |
| 1 backtest integrity | 17280 | 17280 |  |
| 2 trade count & coverage | 17280 | 10945 |  |
| 3 performance & risk | 10945 | 838 |  |
| 4 parameter stability | 838 | 808 |  |
| 5 time stability | 808 | 805 |  |
| 6 deduplication | 805 | 282 | best 2 per cluster |
| 7 execution stress | 282 | 282 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 282 |  | diagnostic only: unverified: 282 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| std_lookback | 0.325 |
| mean_lookback | 0.247 |
| max_holding_bars | 0.190 |
| stop_atr_multiple | 0.175 |
| entry_z | 0.118 |
| entry_confirmation | 0.101 |
| exit_z | 0.053 |
| mean_type | 0.036 |
| timeframe | 0.000 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 1h | 17280 | 82.7% | 0.34 | 0.75 | 9.9% | 63.3% | 0.29 | 119 | 838 | 282 | 1.00 |
| mean_type | sma | 8640 | 79.6% | 0.32 | 0.75 | 10.1% | 70.5% | 0.28 | 127 | 532 | 163 | 1.30 |
| mean_type | ema | 8640 | 85.8% | 0.36 | 0.75 | 9.8% | 56.2% | 0.30 | 110 | 306 | 119 | 0.70 |
| mean_lookback | 30 | 3456 | 81.2% | 0.32 | 0.72 | 8.0% | 47.8% | 0.27 | 95 | 87 | 32 | 0.55 |
| mean_lookback | 40 | 3456 | 89.9% | 0.45 | 0.83 | 16.2% | 60.0% | 0.45 | 116 | 319 | 105 | 2.00 |
| mean_lookback | 50 | 3456 | 87.8% | 0.41 | 0.79 | 12.2% | 66.0% | 0.36 | 122 | 248 | 80 | 1.95 |
| mean_lookback | 60 | 3456 | 80.5% | 0.34 | 0.74 | 9.4% | 69.4% | 0.27 | 123 | 138 | 46 | 0.25 |
| mean_lookback | 80 | 3456 | 74.1% | 0.21 | 0.60 | 3.7% | 73.4% | 0.17 | 128 | 46 | 19 | 0.25 |
| std_lookback | 12 | 2880 | 59.2% | 0.09 | 0.46 | 1.5% | 81.1% | 0.07 | 143 | 27 | 11 | 0.18 |
| std_lookback | 15 | 2880 | 81.1% | 0.27 | 0.68 | 6.2% | 73.8% | 0.26 | 134 | 119 | 50 | 1.32 |
| std_lookback | 18 | 2880 | 90.5% | 0.42 | 0.83 | 15.1% | 67.8% | 0.37 | 123 | 237 | 77 | 1.50 |
| std_lookback | 20 | 2880 | 88.0% | 0.42 | 0.79 | 13.3% | 59.5% | 0.37 | 115 | 205 | 54 | 1.68 |
| std_lookback | 22 | 2880 | 89.2% | 0.42 | 0.76 | 10.9% | 53.7% | 0.39 | 106 | 139 | 52 | 0.66 |
| std_lookback | 25 | 2880 | 88.0% | 0.41 | 0.79 | 12.5% | 44.1% | 0.37 | 91 | 111 | 38 | 0.66 |
| entry_z | -2.0 | 5760 | 79.7% | 0.28 | 0.68 | 6.4% | 85.3% | 0.25 | 149 | 238 | 98 | 0.69 |
| entry_z | -2.5 | 5760 | 85.8% | 0.39 | 0.77 | 11.3% | 64.6% | 0.36 | 118 | 331 | 112 | 1.38 |
| entry_z | -3.0 | 5760 | 82.6% | 0.35 | 0.78 | 12.1% | 40.1% | 0.29 | 87 | 269 | 72 | 0.93 |
| exit_z | -0.5 | 5760 | 80.2% | 0.31 | 0.72 | 8.2% | 63.6% | 0.25 | 120 | 208 | 32 | 0.54 |
| exit_z | 0.0 | 5760 | 83.1% | 0.34 | 0.75 | 9.8% | 63.3% | 0.29 | 119 | 276 | 67 | 0.93 |
| exit_z | 0.5 | 5760 | 84.7% | 0.37 | 0.78 | 11.8% | 63.1% | 0.33 | 118 | 354 | 183 | 1.53 |
| max_holding_bars | 5 | 4320 | 67.2% | 0.21 | 0.64 | 4.9% | 65.0% | 0.12 | 121 | 82 | 32 | 0.24 |
| max_holding_bars | 8 | 4320 | 86.3% | 0.35 | 0.75 | 9.9% | 64.3% | 0.33 | 121 | 285 | 72 | 1.60 |
| max_holding_bars | 10 | 4320 | 87.8% | 0.38 | 0.80 | 13.1% | 63.1% | 0.34 | 119 | 256 | 95 | 1.48 |
| max_holding_bars | 14 | 4320 | 89.4% | 0.39 | 0.78 | 11.8% | 61.0% | 0.35 | 115 | 215 | 83 | 0.68 |
| entry_confirmation | none | 8640 | 77.2% | 0.29 | 0.71 | 8.3% | 87.8% | 0.30 | 160 | 675 | 217 | 1.52 |
| entry_confirmation | positive_bar_return | 8640 | 88.1% | 0.39 | 0.78 | 11.5% | 38.9% | 0.28 | 88 | 163 | 65 | 0.48 |
| stop_atr_multiple | none | 4320 | 79.0% | 0.35 | 0.80 | 13.1% | 41.8% | 0.21 | 91 | 145 | 55 | 0.84 |
| stop_atr_multiple | 1.0 | 4320 | 79.1% | 0.24 | 0.59 | 2.8% | 76.7% | 0.23 | 152 | 101 | 10 | 0.24 |
| stop_atr_multiple | 1.5 | 4320 | 88.6% | 0.42 | 0.79 | 12.7% | 70.4% | 0.39 | 128 | 349 | 157 | 1.96 |
| stop_atr_multiple | 2.0 | 4320 | 84.0% | 0.37 | 0.76 | 11.1% | 64.5% | 0.32 | 117 | 243 | 60 | 0.96 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 1h | sma | 40 | 15 | -3.0 | 0.5 | 14 | none | 1.5 | 154 | 42.9% | 1.26 | -10.0% | s7 pass |
| 2 | 1h | sma | 40 | 18 | -2.0 | 0.5 | 10 | positive_bar_return | none | 106 | 36.3% | 1.20 | -7.4% | s7 pass |
| 3 | 1h | sma | 50 | 15 | -3.0 | 0.5 | 10 | none | 1.5 | 156 | 36.4% | 1.20 | -6.2% | s7 pass |
| 4 | 1h | sma | 30 | 25 | -2.5 | 0.5 | 8 | none | 1.5 | 121 | 29.3% | 1.20 | -4.6% | s7 pass |
| 5 | 1h | ema | 40 | 18 | -2.0 | 0.5 | 8 | positive_bar_return | 2.0 | 107 | 28.5% | 1.19 | -5.5% | s7 pass |
| 6 | 1h | sma | 40 | 15 | -2.5 | 0.0 | 10 | positive_bar_return | 2.0 | 105 | 34.8% | 1.19 | -5.4% | s6 deduplicated |
| 7 | 1h | sma | 60 | 15 | -3.0 | -0.5 | 10 | none | 1.5 | 153 | 34.6% | 1.19 | -6.1% | s7 pass |
| 8 | 1h | sma | 40 | 18 | -2.0 | 0.0 | 10 | positive_bar_return | none | 106 | 34.7% | 1.18 | -7.5% | s7 pass |
| 9 | 1h | sma | 40 | 15 | -3.0 | 0.0 | 14 | none | 1.5 | 154 | 39.1% | 1.18 | -10.1% | s6 deduplicated |
| 10 | 1h | sma | 30 | 25 | -2.5 | 0.5 | 8 | none | 2.0 | 113 | 29.0% | 1.17 | -4.4% | s7 pass |
| 11 | 1h | ema | 50 | 20 | -2.5 | 0.5 | 10 | none | none | 118 | 36.8% | 1.17 | -6.4% | s7 pass |
| 12 | 1h | ema | 50 | 20 | -2.5 | 0.5 | 8 | none | 2.0 | 149 | 34.9% | 1.16 | -5.8% | s7 pass |
| 13 | 1h | ema | 50 | 20 | -2.5 | 0.5 | 10 | none | 2.0 | 144 | 36.2% | 1.16 | -7.6% | s7 pass |
| 14 | 1h | sma | 60 | 15 | -3.0 | 0.5 | 10 | none | 1.5 | 151 | 34.9% | 1.16 | -6.5% | s7 pass |
| 15 | 1h | ema | 40 | 18 | -2.0 | 0.5 | 8 | positive_bar_return | 1.5 | 113 | 28.0% | 1.16 | -5.3% | s7 pass |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
