# Ablation (development only) -- mr_cl_v7

- Symbol CL, strategy `mean_reversion_v18`, 16,128 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 12,149 configs (75.3%).
- Grid-wide: 70.0% profitable, median dev Sharpe 0.35, 2266 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 16128 | 16128 |  |
| 1 backtest integrity | 16128 | 16128 |  |
| 2 trade count & coverage | 16128 | 12149 |  |
| 3 performance & risk | 12149 | 1925 |  |
| 4 parameter stability | 1925 | 1905 |  |
| 5 time stability | 1905 | 1809 |  |
| 6 deduplication | 1809 | 150 | best 2 per cluster |
| 7 execution stress | 150 | 150 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 150 |  | diagnostic only: unverified: 150 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| std_lookback | 0.786 |
| stop_atr_multiple | 0.415 |
| mean_lookback | 0.321 |
| entry_z | 0.110 |
| mean_type | 0.089 |
| max_holding_bars | 0.055 |
| exit_z | 0.019 |
| timeframe | 0.000 |
| entry_confirmation | 0.000 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 15min | 16128 | 70.0% | 0.35 | 0.81 | 14.1% | 75.3% | 0.42 | 238 | 1925 | 150 | 1.00 |
| mean_type | sma | 8064 | 66.9% | 0.31 | 0.80 | 12.7% | 79.8% | 0.37 | 277 | 920 | 95 | 1.22 |
| mean_type | ema | 8064 | 73.2% | 0.40 | 0.82 | 15.4% | 70.9% | 0.47 | 201 | 1005 | 55 | 0.78 |
| mean_lookback | 30 | 2016 | 50.0% | 0.11 | 0.77 | 10.4% | 39.7% | 0.35 | 70 | 110 | 15 | 0.00 |
| mean_lookback | 40 | 2016 | 71.7% | 0.35 | 0.77 | 11.8% | 63.5% | 0.42 | 158 | 163 | 21 | 0.00 |
| mean_lookback | 45 | 2016 | 71.7% | 0.36 | 0.81 | 13.1% | 73.1% | 0.40 | 203 | 187 | 23 | 0.16 |
| mean_lookback | 50 | 2016 | 71.4% | 0.37 | 0.84 | 17.9% | 77.8% | 0.47 | 239 | 322 | 33 | 1.52 |
| mean_lookback | 55 | 2016 | 79.2% | 0.41 | 0.86 | 18.6% | 83.2% | 0.45 | 260 | 348 | 26 | 1.52 |
| mean_lookback | 60 | 2016 | 76.8% | 0.43 | 0.86 | 16.7% | 85.3% | 0.48 | 280 | 319 | 18 | 3.12 |
| mean_lookback | 70 | 2016 | 74.6% | 0.41 | 0.80 | 14.0% | 89.0% | 0.46 | 306 | 275 | 4 | 1.20 |
| mean_lookback | 80 | 2016 | 65.0% | 0.25 | 0.76 | 10.1% | 91.1% | 0.31 | 309 | 201 | 10 | 0.48 |
| std_lookback | 15 | 2304 | 57.1% | 0.17 | 0.61 | 3.3% | 98.0% | 0.18 | 353 | 61 | 7 | 0.28 |
| std_lookback | 18 | 2304 | 73.2% | 0.37 | 0.82 | 15.5% | 92.2% | 0.41 | 316 | 355 | 48 | 0.56 |
| std_lookback | 20 | 2304 | 90.4% | 0.65 | 0.98 | 35.4% | 89.1% | 0.69 | 291 | 794 | 36 | 4.97 |
| std_lookback | 22 | 2304 | 80.6% | 0.52 | 0.83 | 18.4% | 84.1% | 0.58 | 259 | 419 | 6 | 0.42 |
| std_lookback | 25 | 2304 | 68.8% | 0.30 | 0.73 | 8.2% | 74.7% | 0.34 | 211 | 147 | 22 | 0.35 |
| std_lookback | 30 | 2304 | 78.9% | 0.38 | 0.83 | 13.8% | 60.7% | 0.36 | 146 | 115 | 21 | 0.42 |
| std_lookback | 75 | 2304 | 41.4% | -0.13 | 0.60 | 3.7% | 28.4% | 0.17 | 38 | 34 | 10 | 0.00 |
| entry_z | -2.0 | 4032 | 69.7% | 0.30 | 0.74 | 9.2% | 98.9% | 0.30 | 402 | 360 | 38 | 0.48 |
| entry_z | -2.5 | 4032 | 69.4% | 0.33 | 0.78 | 11.9% | 82.9% | 0.39 | 290 | 420 | 37 | 0.28 |
| entry_z | -3.0 | 4032 | 71.8% | 0.41 | 0.87 | 19.1% | 66.8% | 0.53 | 181 | 657 | 49 | 1.52 |
| entry_z | -3.5 | 4032 | 69.3% | 0.39 | 0.84 | 15.9% | 52.7% | 0.55 | 112 | 488 | 26 | 1.72 |
| exit_z | -1.0 | 5376 | 69.4% | 0.33 | 0.81 | 13.9% | 75.4% | 0.41 | 239 | 628 | 47 | 0.96 |
| exit_z | 0.0 | 5376 | 70.3% | 0.35 | 0.81 | 14.0% | 75.3% | 0.42 | 238 | 641 | 51 | 1.02 |
| exit_z | 0.5 | 5376 | 70.4% | 0.35 | 0.81 | 14.3% | 75.3% | 0.43 | 238 | 656 | 52 | 1.02 |
| max_holding_bars | 3 | 5376 | 68.3% | 0.32 | 0.76 | 10.3% | 75.3% | 0.38 | 235 | 432 | 16 | 0.45 |
| max_holding_bars | 5 | 5376 | 73.5% | 0.38 | 0.86 | 18.7% | 75.5% | 0.45 | 240 | 894 | 63 | 1.50 |
| max_holding_bars | 8 | 5376 | 68.3% | 0.34 | 0.79 | 13.2% | 75.2% | 0.44 | 240 | 599 | 71 | 1.05 |
| entry_confirmation | positive_bar_return | 16128 | 70.0% | 0.35 | 0.81 | 14.1% | 75.3% | 0.42 | 238 | 1925 | 150 | 1.00 |
| stop_atr_multiple | none | 4032 | 49.4% | 0.08 | 0.63 | 5.1% | 73.5% | 0.14 | 204 | 151 | 4 | 0.12 |
| stop_atr_multiple | 1.0 | 4032 | 81.7% | 0.49 | 0.86 | 20.6% | 76.6% | 0.56 | 281 | 721 | 78 | 1.00 |
| stop_atr_multiple | 1.5 | 4032 | 79.7% | 0.46 | 0.87 | 19.7% | 75.7% | 0.53 | 248 | 710 | 57 | 2.16 |
| stop_atr_multiple | 2.0 | 4032 | 69.4% | 0.32 | 0.76 | 10.7% | 75.5% | 0.39 | 231 | 343 | 11 | 0.72 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 15min | sma | 60 | 20 | -3.5 | -1.0 | 5 | positive_bar_return | 1.5 | 266 | 250.7% | 1.38 | -9.1% | s7 pass |
| 2 | 15min | sma | 60 | 20 | -3.5 | 0.5 | 5 | positive_bar_return | 1.5 | 266 | 249.5% | 1.38 | -9.2% | s7 pass |
| 3 | 15min | sma | 60 | 20 | -3.5 | -1.0 | 5 | positive_bar_return | 2.0 | 235 | 251.9% | 1.38 | -12.5% | s6 deduplicated |
| 4 | 15min | sma | 60 | 20 | -3.5 | 0.5 | 5 | positive_bar_return | 2.0 | 235 | 249.8% | 1.37 | -12.6% | s6 deduplicated |
| 5 | 15min | sma | 60 | 20 | -3.5 | 0.0 | 5 | positive_bar_return | 1.5 | 266 | 241.3% | 1.36 | -9.3% | s6 deduplicated |
| 6 | 15min | sma | 60 | 20 | -3.5 | 0.0 | 5 | positive_bar_return | 2.0 | 235 | 241.9% | 1.35 | -12.5% | s6 deduplicated |
| 7 | 15min | sma | 60 | 20 | -3.5 | 0.5 | 8 | positive_bar_return | 1.5 | 273 | 232.9% | 1.35 | -11.0% | s6 deduplicated |
| 8 | 15min | sma | 60 | 20 | -3.5 | -1.0 | 8 | positive_bar_return | 1.5 | 273 | 229.0% | 1.34 | -11.0% | s6 deduplicated |
| 9 | 15min | sma | 60 | 20 | -3.5 | -1.0 | 3 | positive_bar_return | 1.5 | 246 | 176.5% | 1.33 | -6.6% | s6 deduplicated |
| 10 | 15min | sma | 60 | 20 | -3.5 | 0.0 | 3 | positive_bar_return | 1.5 | 246 | 176.0% | 1.32 | -6.7% | s6 deduplicated |
| 11 | 15min | sma | 60 | 20 | -3.5 | 0.5 | 3 | positive_bar_return | 1.5 | 246 | 176.0% | 1.32 | -6.7% | s6 deduplicated |
| 12 | 15min | sma | 60 | 20 | -3.5 | 0.0 | 8 | positive_bar_return | 1.5 | 273 | 218.8% | 1.31 | -11.0% | s6 deduplicated |
| 13 | 15min | ema | 60 | 20 | -3.0 | -1.0 | 5 | positive_bar_return | 1.5 | 270 | 219.4% | 1.29 | -14.0% | s7 pass |
| 14 | 15min | sma | 60 | 20 | -3.5 | 0.5 | 8 | positive_bar_return | 1.0 | 317 | 198.1% | 1.27 | -13.9% | s7 pass |
| 15 | 15min | ema | 60 | 20 | -3.0 | 0.0 | 5 | positive_bar_return | 1.5 | 270 | 212.9% | 1.27 | -14.1% | s7 pass |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
