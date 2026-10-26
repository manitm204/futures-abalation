# Ablation (development only) -- mr_6e_v6

- Symbol 6E, strategy `mean_reversion_v21`, 24,000 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 24,000 configs (100.0%).
- Grid-wide: 50.5% profitable, median dev Sharpe 0.02, 1053 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 24000 | 24000 |  |
| 1 backtest integrity | 24000 | 24000 |  |
| 2 trade count & coverage | 24000 | 24000 |  |
| 3 performance & risk | 24000 | 1053 |  |
| 4 parameter stability | 1053 | 1018 |  |
| 5 time stability | 1018 | 970 |  |
| 6 deduplication | 970 | 252 | best 2 per cluster |
| 7 execution stress | 252 | 252 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 252 |  | diagnostic only: unverified: 252 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| max_holding_bars | 0.465 |
| mean_type | 0.436 |
| std_lookback | 0.378 |
| mean_lookback | 0.377 |
| entry_z | 0.358 |
| stop_atr_multiple | 0.342 |
| exit_z | 0.021 |
| timeframe | 0.000 |
| entry_confirmation | 0.000 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 1h | 24000 | 50.5% | 0.02 | 0.59 | 4.4% | 100.0% | 0.02 | 220 | 1053 | 252 | 1.00 |
| mean_type | sma | 12000 | 69.7% | 0.22 | 0.67 | 6.4% | 100.0% | 0.22 | 208 | 766 | 175 | 1.48 |
| mean_type | ema | 12000 | 31.2% | -0.22 | 0.40 | 2.4% | 100.0% | -0.22 | 231 | 287 | 77 | 0.52 |
| mean_lookback | 60 | 4000 | 30.8% | -0.23 | 0.37 | 0.5% | 100.0% | -0.23 | 231 | 21 | 6 | 0.00 |
| mean_lookback | 70 | 4000 | 49.4% | 0.00 | 0.62 | 4.5% | 100.0% | 0.00 | 225 | 179 | 44 | 0.30 |
| mean_lookback | 80 | 4000 | 55.9% | 0.11 | 0.78 | 11.3% | 100.0% | 0.11 | 222 | 454 | 70 | 4.14 |
| mean_lookback | 90 | 4000 | 50.4% | 0.02 | 0.51 | 1.9% | 100.0% | 0.02 | 219 | 78 | 29 | 0.00 |
| mean_lookback | 100 | 4000 | 60.7% | 0.15 | 0.61 | 4.1% | 100.0% | 0.15 | 217 | 164 | 54 | 1.08 |
| mean_lookback | 120 | 4000 | 55.8% | 0.07 | 0.57 | 3.9% | 100.0% | 0.07 | 205 | 157 | 49 | 0.48 |
| std_lookback | 6 | 4800 | 55.1% | 0.06 | 0.52 | 1.6% | 100.0% | 0.06 | 253 | 75 | 29 | 0.05 |
| std_lookback | 8 | 4800 | 56.8% | 0.10 | 0.61 | 5.5% | 100.0% | 0.10 | 221 | 262 | 59 | 1.25 |
| std_lookback | 10 | 4800 | 54.9% | 0.07 | 0.68 | 7.6% | 100.0% | 0.07 | 215 | 365 | 79 | 2.35 |
| std_lookback | 12 | 4800 | 53.8% | 0.07 | 0.67 | 6.8% | 100.0% | 0.07 | 214 | 325 | 76 | 1.35 |
| std_lookback | 15 | 4800 | 31.8% | -0.28 | 0.37 | 0.5% | 100.0% | -0.28 | 203 | 26 | 9 | 0.00 |
| entry_z | -1.5 | 4800 | 62.9% | 0.17 | 0.68 | 7.4% | 100.0% | 0.17 | 229 | 357 | 99 | 1.50 |
| entry_z | -1.75 | 4800 | 56.0% | 0.09 | 0.63 | 5.5% | 100.0% | 0.09 | 223 | 266 | 67 | 0.85 |
| entry_z | -2.0 | 4800 | 53.0% | 0.05 | 0.58 | 3.1% | 100.0% | 0.05 | 218 | 150 | 34 | 0.80 |
| entry_z | -2.25 | 4800 | 44.1% | -0.07 | 0.50 | 3.7% | 100.0% | -0.07 | 216 | 179 | 26 | 1.65 |
| entry_z | -2.5 | 4800 | 36.4% | -0.19 | 0.42 | 2.1% | 100.0% | -0.19 | 213 | 101 | 26 | 0.20 |
| exit_z | -1.0 | 6000 | 51.5% | 0.03 | 0.58 | 4.3% | 100.0% | 0.03 | 225 | 258 | 67 | 0.76 |
| exit_z | -0.5 | 6000 | 50.3% | 0.01 | 0.60 | 4.5% | 100.0% | 0.01 | 220 | 269 | 63 | 1.08 |
| exit_z | 0.0 | 6000 | 50.5% | 0.02 | 0.60 | 4.6% | 100.0% | 0.02 | 218 | 275 | 68 | 1.12 |
| exit_z | 0.5 | 6000 | 49.7% | 0.01 | 0.58 | 4.2% | 100.0% | 0.01 | 216 | 251 | 54 | 1.04 |
| max_holding_bars | 3 | 4800 | 53.4% | 0.05 | 0.57 | 3.1% | 100.0% | 0.05 | 224 | 147 | 33 | 0.50 |
| max_holding_bars | 4 | 4800 | 64.1% | 0.19 | 0.71 | 8.6% | 100.0% | 0.19 | 219 | 412 | 86 | 3.20 |
| max_holding_bars | 5 | 4800 | 62.6% | 0.15 | 0.69 | 7.7% | 100.0% | 0.15 | 215 | 368 | 78 | 1.10 |
| max_holding_bars | 6 | 4800 | 43.0% | -0.09 | 0.47 | 1.4% | 100.0% | -0.09 | 212 | 68 | 27 | 0.10 |
| max_holding_bars | 8 | 4800 | 29.2% | -0.28 | 0.37 | 1.2% | 100.0% | -0.28 | 234 | 58 | 28 | 0.10 |
| entry_confirmation | none | 24000 | 50.5% | 0.02 | 0.59 | 4.4% | 100.0% | 0.02 | 220 | 1053 | 252 | 1.00 |
| stop_atr_multiple | none | 6000 | 65.3% | 0.22 | 0.70 | 7.3% | 100.0% | 0.22 | 191 | 441 | 159 | 2.04 |
| stop_atr_multiple | 1.5 | 6000 | 39.5% | -0.12 | 0.44 | 2.3% | 100.0% | -0.12 | 257 | 139 | 14 | 0.04 |
| stop_atr_multiple | 2.0 | 6000 | 45.3% | -0.06 | 0.55 | 4.0% | 100.0% | -0.06 | 227 | 241 | 38 | 1.20 |
| stop_atr_multiple | 2.5 | 6000 | 51.8% | 0.03 | 0.56 | 3.9% | 100.0% | 0.03 | 211 | 232 | 41 | 0.72 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 1h | sma | 80 | 10 | -2.0 | 0.0 | 4 | none | none | 201 | 14.3% | 1.42 | -1.7% | s7 pass |
| 2 | 1h | sma | 80 | 10 | -2.0 | -0.5 | 4 | none | none | 202 | 13.6% | 1.38 | -1.7% | s7 pass |
| 3 | 1h | sma | 80 | 10 | -2.0 | 0.0 | 4 | none | 2.0 | 215 | 14.5% | 1.37 | -2.2% | s6 deduplicated |
| 4 | 1h | sma | 80 | 8 | -1.75 | -0.5 | 5 | none | none | 197 | 13.0% | 1.36 | -2.2% | s6 deduplicated |
| 5 | 1h | ema | 100 | 12 | -1.5 | 0.5 | 5 | none | none | 202 | 13.7% | 1.35 | -2.0% | s7 pass |
| 6 | 1h | sma | 80 | 8 | -1.75 | 0.5 | 5 | none | none | 190 | 13.0% | 1.35 | -2.5% | s6 deduplicated |
| 7 | 1h | sma | 80 | 10 | -2.0 | -0.5 | 4 | none | 2.0 | 216 | 13.9% | 1.34 | -2.1% | s6 deduplicated |
| 8 | 1h | ema | 120 | 12 | -1.5 | 0.0 | 4 | none | 2.5 | 212 | 12.1% | 1.33 | -1.4% | s7 pass |
| 9 | 1h | sma | 80 | 8 | -1.75 | 0.0 | 5 | none | none | 192 | 12.7% | 1.32 | -2.6% | s6 deduplicated |
| 10 | 1h | sma | 80 | 10 | -2.25 | -1.0 | 3 | none | none | 195 | 10.8% | 1.31 | -1.6% | s6 deduplicated |
| 11 | 1h | ema | 100 | 12 | -1.5 | 0.5 | 5 | none | 2.0 | 228 | 13.8% | 1.31 | -1.6% | s7 pass |
| 12 | 1h | sma | 80 | 10 | -1.75 | 0.0 | 4 | none | 2.0 | 226 | 14.8% | 1.30 | -1.9% | s6 deduplicated |
| 13 | 1h | ema | 120 | 12 | -1.5 | 0.5 | 4 | none | 2.5 | 211 | 11.9% | 1.29 | -1.4% | s7 pass |
| 14 | 1h | sma | 80 | 8 | -1.75 | -1.0 | 5 | none | none | 202 | 12.0% | 1.29 | -2.4% | s6 deduplicated |
| 15 | 1h | sma | 80 | 10 | -2.25 | 0.0 | 4 | none | none | 187 | 12.5% | 1.29 | -2.1% | s7 pass |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
