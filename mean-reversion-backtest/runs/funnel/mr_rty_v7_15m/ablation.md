# Ablation (development only) -- mr_rty_v7_15m

- Symbol RTY, strategy `mean_reversion_v16`, 13,608 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 9,711 configs (71.4%).
- Grid-wide: 41.6% profitable, median dev Sharpe -0.08, 804 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 13608 | 13608 |  |
| 1 backtest integrity | 13608 | 13608 |  |
| 2 trade count & coverage | 13608 | 9711 |  |
| 3 performance & risk | 9711 | 498 |  |
| 4 parameter stability | 498 | 473 |  |
| 5 time stability | 473 | 460 |  |
| 6 deduplication | 460 | 154 | best 2 per cluster |
| 7 execution stress | 154 | 154 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 154 |  | diagnostic only: unverified: 154 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| std_lookback | 0.451 |
| entry_confirmation | 0.438 |
| entry_z | 0.090 |
| max_holding_bars | 0.065 |
| mean_lookback | 0.063 |
| stop_atr_multiple | 0.052 |
| mean_type | 0.043 |
| exit_z | 0.041 |
| timeframe | 0.000 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 15min | 13608 | 41.6% | -0.08 | 0.62 | 5.9% | 71.4% | -0.03 | 189 | 498 | 154 | 1.00 |
| mean_type | sma | 6804 | 39.5% | -0.10 | 0.60 | 5.5% | 78.0% | -0.04 | 224 | 291 | 94 | 1.18 |
| mean_type | ema | 6804 | 43.6% | -0.06 | 0.64 | 6.4% | 64.8% | -0.01 | 158 | 207 | 60 | 0.82 |
| mean_lookback | 35 | 1512 | 44.4% | -0.06 | 0.76 | 10.6% | 53.0% | 0.06 | 108 | 106 | 32 | 2.61 |
| mean_lookback | 45 | 1512 | 43.4% | -0.07 | 0.69 | 8.5% | 58.1% | 0.05 | 127 | 90 | 21 | 2.43 |
| mean_lookback | 55 | 1512 | 42.9% | -0.08 | 0.68 | 7.7% | 64.1% | 0.02 | 149 | 93 | 32 | 1.44 |
| mean_lookback | 65 | 1512 | 42.3% | -0.08 | 0.62 | 4.5% | 69.6% | -0.01 | 168 | 43 | 15 | 0.63 |
| mean_lookback | 75 | 1512 | 40.3% | -0.10 | 0.54 | 4.2% | 71.8% | -0.05 | 190 | 30 | 8 | 0.36 |
| mean_lookback | 85 | 1512 | 38.8% | -0.09 | 0.52 | 4.6% | 76.0% | -0.06 | 207 | 23 | 10 | 0.54 |
| mean_lookback | 95 | 1512 | 42.1% | -0.08 | 0.57 | 5.0% | 79.2% | -0.04 | 234 | 40 | 11 | 0.09 |
| mean_lookback | 105 | 1512 | 38.2% | -0.11 | 0.51 | 4.8% | 83.5% | -0.09 | 254 | 37 | 16 | 0.90 |
| mean_lookback | 115 | 1512 | 41.9% | -0.04 | 0.57 | 3.4% | 86.9% | -0.02 | 271 | 36 | 9 | 0.00 |
| std_lookback | 15 | 1944 | 16.3% | -0.29 | 0.16 | 0.3% | 100.0% | -0.29 | 562 | 5 | 4 | 0.00 |
| std_lookback | 55 | 1944 | 33.5% | -0.14 | 0.45 | 3.3% | 83.6% | -0.12 | 239 | 53 | 14 | 0.70 |
| std_lookback | 65 | 1944 | 30.3% | -0.16 | 0.32 | 2.3% | 72.5% | -0.10 | 192 | 24 | 8 | 0.42 |
| std_lookback | 75 | 1944 | 35.2% | -0.13 | 0.42 | 2.5% | 70.1% | -0.06 | 164 | 10 | 3 | 0.00 |
| std_lookback | 85 | 1944 | 56.7% | 0.12 | 0.84 | 13.8% | 63.7% | 0.26 | 140 | 186 | 58 | 3.85 |
| std_lookback | 95 | 1944 | 59.2% | 0.16 | 0.76 | 10.4% | 57.6% | 0.32 | 118 | 119 | 31 | 1.12 |
| std_lookback | 105 | 1944 | 59.9% | 0.16 | 0.72 | 8.8% | 52.1% | 0.30 | 106 | 101 | 36 | 0.91 |
| entry_z | -2.0 | 4536 | 36.8% | -0.11 | 0.45 | 3.1% | 97.4% | -0.10 | 335 | 140 | 38 | 0.87 |
| entry_z | -2.5 | 4536 | 45.9% | -0.02 | 0.56 | 3.9% | 75.3% | 0.03 | 177 | 164 | 53 | 0.96 |
| entry_z | -3.0 | 4536 | 42.1% | -0.11 | 0.77 | 10.7% | 41.4% | 0.10 | 80 | 194 | 63 | 1.17 |
| exit_z | -1.0 | 4536 | 43.1% | -0.05 | 0.63 | 6.3% | 71.4% | -0.00 | 189 | 173 | 65 | 1.02 |
| exit_z | 0.0 | 4536 | 40.7% | -0.10 | 0.61 | 5.7% | 71.3% | -0.04 | 189 | 165 | 50 | 1.02 |
| exit_z | 1.0 | 4536 | 40.9% | -0.08 | 0.61 | 5.7% | 71.3% | -0.04 | 189 | 160 | 39 | 0.96 |
| max_holding_bars | 3 | 4536 | 43.4% | -0.06 | 0.71 | 8.8% | 71.5% | -0.03 | 193 | 221 | 62 | 1.77 |
| max_holding_bars | 5 | 4536 | 43.6% | -0.06 | 0.63 | 5.6% | 71.6% | 0.01 | 190 | 183 | 52 | 0.78 |
| max_holding_bars | 8 | 4536 | 37.8% | -0.12 | 0.53 | 3.4% | 71.0% | -0.06 | 185 | 94 | 40 | 0.45 |
| entry_confirmation | none | 6804 | 62.7% | 0.19 | 0.78 | 11.5% | 86.6% | 0.13 | 271 | 481 | 150 | 2.00 |
| entry_confirmation | positive_bar_return | 6804 | 20.5% | -0.25 | 0.21 | 0.3% | 56.2% | -0.17 | 120 | 17 | 4 | 0.00 |
| stop_atr_multiple | none | 6804 | 44.1% | -0.05 | 0.67 | 7.4% | 67.4% | -0.00 | 165 | 263 | 84 | 0.94 |
| stop_atr_multiple | 1.5 | 6804 | 39.0% | -0.10 | 0.56 | 4.4% | 75.3% | -0.05 | 223 | 235 | 70 | 1.06 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 15min | sma | 45 | 55 | -3.0 | -1.0 | 3 | none | none | 133 | 21.3% | 1.41 | -2.2% | s6 deduplicated |
| 2 | 15min | sma | 45 | 55 | -3.0 | 0.0 | 3 | none | none | 133 | 21.2% | 1.40 | -2.2% | s6 deduplicated |
| 3 | 15min | sma | 45 | 55 | -3.0 | 1.0 | 3 | none | none | 133 | 21.2% | 1.40 | -2.2% | s6 deduplicated |
| 4 | 15min | ema | 35 | 85 | -2.0 | 1.0 | 3 | none | 1.5 | 262 | 26.0% | 1.40 | -2.7% | s7 pass |
| 5 | 15min | ema | 35 | 85 | -2.0 | 0.0 | 3 | none | 1.5 | 262 | 25.7% | 1.40 | -2.7% | s7 pass |
| 6 | 15min | ema | 35 | 85 | -2.0 | -1.0 | 3 | none | 1.5 | 262 | 24.5% | 1.37 | -2.6% | s6 deduplicated |
| 7 | 15min | sma | 45 | 55 | -3.0 | -1.0 | 3 | none | 1.5 | 163 | 19.4% | 1.25 | -2.9% | s6 deduplicated |
| 8 | 15min | sma | 45 | 55 | -3.0 | 0.0 | 3 | none | 1.5 | 163 | 19.1% | 1.24 | -2.9% | s7 pass |
| 9 | 15min | sma | 45 | 55 | -3.0 | 1.0 | 3 | none | 1.5 | 163 | 19.1% | 1.24 | -2.9% | s7 pass |
| 10 | 15min | sma | 55 | 55 | -3.0 | -1.0 | 8 | none | none | 137 | 25.7% | 1.21 | -3.9% | s7 pass |
| 11 | 15min | sma | 45 | 85 | -2.5 | 1.0 | 3 | none | 1.5 | 218 | 20.3% | 1.19 | -3.2% | s6 deduplicated |
| 12 | 15min | ema | 45 | 95 | -2.0 | 0.0 | 3 | none | 1.5 | 265 | 20.9% | 1.19 | -3.4% | s6 deduplicated |
| 13 | 15min | ema | 45 | 95 | -2.0 | 1.0 | 3 | none | 1.5 | 265 | 20.9% | 1.19 | -3.4% | s6 deduplicated |
| 14 | 15min | sma | 45 | 85 | -2.5 | -1.0 | 3 | none | 1.5 | 218 | 20.1% | 1.19 | -3.2% | s6 deduplicated |
| 15 | 15min | sma | 45 | 85 | -2.5 | 0.0 | 3 | none | 1.5 | 218 | 20.0% | 1.18 | -3.2% | s6 deduplicated |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
