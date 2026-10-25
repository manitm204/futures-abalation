# Ablation (development only) -- mr_es_v6_15m

- Symbol ES, strategy `mean_reversion_v10`, 864 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 700 configs (81.0%).
- Grid-wide: 45.9% profitable, median dev Sharpe -0.01, 16 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 864 | 864 |  |
| 1 backtest integrity | 864 | 864 |  |
| 2 trade count & coverage | 864 | 700 |  |
| 3 performance & risk | 700 | 14 |  |
| 4 parameter stability | 14 | 11 |  |
| 5 time stability | 11 | 11 |  |
| 6 deduplication | 11 | 7 | best 2 per cluster |
| 7 execution stress | 7 | 7 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 7 |  | diagnostic only: unverified: 7 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| std_lookback | 0.925 |
| mean_lookback | 0.317 |
| max_holding_bars | 0.244 |
| entry_z | 0.078 |
| mean_type | 0.034 |
| exit_z | 0.018 |
| timeframe | 0.000 |
| entry_confirmation | 0.000 |
| stop_atr_multiple | 0.000 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 15min | 864 | 45.9% | -0.01 | 0.48 | 1.9% | 81.0% | -0.03 | 218 | 14 | 7 | 1.00 |
| mean_type | sma | 432 | 47.2% | -0.04 | 0.53 | 2.5% | 88.4% | 0.02 | 269 | 11 | 4 | 1.54 |
| mean_type | ema | 432 | 44.7% | -0.00 | 0.41 | 1.2% | 73.6% | -0.04 | 181 | 3 | 3 | 0.46 |
| mean_lookback | 32 | 144 | 27.8% | -0.24 | 0.20 | 1.4% | 54.2% | -0.31 | 111 | 0 | 0 | 0.12 |
| mean_lookback | 37 | 144 | 45.8% | -0.00 | 0.49 | 0.0% | 70.8% | -0.03 | 180 | 0 | 0 | 0.90 |
| mean_lookback | 42 | 144 | 54.9% | 0.08 | 0.53 | 4.2% | 81.9% | 0.04 | 215 | 6 | 4 | 1.14 |
| mean_lookback | 47 | 144 | 52.8% | 0.06 | 0.49 | 1.4% | 87.5% | 0.04 | 246 | 2 | 1 | 1.50 |
| mean_lookback | 52 | 144 | 46.5% | -0.00 | 0.45 | 2.8% | 95.8% | -0.05 | 271 | 4 | 0 | 1.02 |
| mean_lookback | 57 | 144 | 47.9% | 0.02 | 0.51 | 1.4% | 95.8% | 0.01 | 290 | 2 | 2 | 1.32 |
| std_lookback | 12 | 144 | 5.6% | -0.51 | -0.06 | 0.0% | 100.0% | -0.51 | 337 | 0 | 0 | 0.00 |
| std_lookback | 15 | 144 | 10.4% | -0.44 | 0.03 | 0.0% | 100.0% | -0.44 | 289 | 0 | 0 | 0.00 |
| std_lookback | 18 | 144 | 52.1% | 0.04 | 0.38 | 1.4% | 94.4% | 0.03 | 239 | 0 | 0 | 0.48 |
| std_lookback | 21 | 144 | 88.9% | 0.42 | 0.69 | 5.6% | 79.2% | 0.47 | 184 | 8 | 5 | 3.90 |
| std_lookback | 24 | 144 | 54.9% | 0.07 | 0.43 | 2.8% | 66.7% | 0.17 | 138 | 4 | 0 | 0.96 |
| std_lookback | 27 | 144 | 63.9% | 0.17 | 0.48 | 1.4% | 45.8% | 0.23 | 98 | 2 | 2 | 0.66 |
| entry_z | -2.5 | 432 | 49.3% | 0.02 | 0.50 | 2.8% | 92.1% | 0.02 | 268 | 12 | 6 | 1.22 |
| entry_z | -3.0 | 432 | 42.6% | -0.06 | 0.45 | 0.9% | 69.9% | -0.10 | 163 | 2 | 1 | 0.78 |
| exit_z | -1.0 | 432 | 47.2% | 0.00 | 0.48 | 1.9% | 81.2% | -0.02 | 219 | 7 | 2 | 1.04 |
| exit_z | 0.0 | 432 | 44.7% | -0.02 | 0.47 | 1.9% | 80.8% | -0.04 | 218 | 7 | 5 | 0.96 |
| max_holding_bars | 3 | 288 | 33.3% | -0.16 | 0.34 | 0.7% | 81.9% | -0.20 | 228 | 2 | 0 | 0.54 |
| max_holding_bars | 5 | 288 | 54.5% | 0.09 | 0.55 | 4.2% | 80.9% | 0.10 | 218 | 10 | 6 | 1.53 |
| max_holding_bars | 7 | 288 | 50.0% | 0.02 | 0.48 | 0.7% | 80.2% | 0.00 | 214 | 2 | 1 | 0.93 |
| entry_confirmation | positive_bar_return | 864 | 45.9% | -0.01 | 0.48 | 1.9% | 81.0% | -0.03 | 218 | 14 | 7 | 1.00 |
| stop_atr_multiple | none | 864 | 45.9% | -0.01 | 0.48 | 1.9% | 81.0% | -0.03 | 218 | 14 | 7 | 1.00 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 15min | sma | 42 | 21 | -2.5 | -1.0 | 5 | positive_bar_return | none | 302 | 36.3% | 0.93 | -9.1% | s6 deduplicated |
| 2 | 15min | sma | 42 | 21 | -2.5 | 0.0 | 5 | positive_bar_return | none | 300 | 33.7% | 0.88 | -9.9% | s7 pass |
| 3 | 15min | ema | 42 | 27 | -2.5 | 0.0 | 5 | positive_bar_return | none | 105 | 11.4% | 0.88 | -2.9% | s7 pass |
| 4 | 15min | sma | 57 | 21 | -2.5 | -1.0 | 5 | positive_bar_return | none | 358 | 27.8% | 0.86 | -7.6% | s7 pass |
| 5 | 15min | sma | 57 | 21 | -2.5 | 0.0 | 5 | positive_bar_return | none | 354 | 27.6% | 0.83 | -7.4% | s7 pass |
| 6 | 15min | sma | 52 | 24 | -2.5 | -1.0 | 3 | positive_bar_return | none | 315 | 28.4% | 0.82 | -7.5% | s4 hard_reject |
| 7 | 15min | sma | 52 | 24 | -2.5 | -1.0 | 5 | positive_bar_return | none | 304 | 30.4% | 0.82 | -11.2% | s6 deduplicated |
| 8 | 15min | sma | 52 | 24 | -2.5 | 0.0 | 3 | positive_bar_return | none | 313 | 28.0% | 0.81 | -7.6% | s4 hard_reject |
| 9 | 15min | sma | 47 | 21 | -3.0 | 0.0 | 5 | positive_bar_return | none | 209 | 27.3% | 0.81 | -8.8% | s7 pass |
| 10 | 15min | sma | 47 | 21 | -3.0 | -1.0 | 5 | positive_bar_return | none | 211 | 27.1% | 0.81 | -8.9% | s6 deduplicated |
| 11 | 15min | ema | 42 | 27 | -2.5 | -1.0 | 5 | positive_bar_return | none | 105 | 9.7% | 0.78 | -2.9% | s7 pass |
| 12 | 15min | ema | 42 | 21 | -2.5 | 0.0 | 7 | positive_bar_return | none | 182 | 29.4% | 0.78 | -8.7% | s7 pass |
| 13 | 15min | sma | 52 | 24 | -2.5 | 0.0 | 5 | positive_bar_return | none | 300 | 28.2% | 0.77 | -12.6% | s4 hard_reject |
| 14 | 15min | sma | 42 | 21 | -2.5 | -1.0 | 7 | positive_bar_return | none | 296 | 32.9% | 0.76 | -11.6% | s6 deduplicated |
| 15 | 15min | sma | 47 | 21 | -2.5 | -1.0 | 5 | positive_bar_return | none | 329 | 25.3% | 0.75 | -6.8% | s3 hard_reject |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
