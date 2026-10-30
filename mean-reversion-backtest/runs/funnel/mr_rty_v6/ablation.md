# Ablation (development only) -- mr_rty_v6

- Symbol RTY, strategy `mean_reversion_v8`, 84,672 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 29,283 configs (34.6%).
- Grid-wide: 37.7% profitable, median dev Sharpe -0.09, 2027 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 84672 | 84672 |  |
| 1 backtest integrity | 84672 | 84672 |  |
| 2 trade count & coverage | 84672 | 29283 |  |
| 3 performance & risk | 29283 | 477 |  |
| 4 parameter stability | 477 | 433 |  |
| 5 time stability | 433 | 410 |  |
| 6 deduplication | 410 | 108 | best 2 per cluster |
| 7 execution stress | 108 | 108 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 108 |  | diagnostic only: unverified: 108 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| entry_confirmation | 0.330 |
| stop_atr_multiple | 0.188 |
| std_lookback | 0.157 |
| entry_z | 0.110 |
| mean_lookback | 0.092 |
| max_holding_bars | 0.068 |
| mean_type | 0.028 |
| timeframe | 0.025 |
| exit_z | 0.012 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 15min | 42336 | 39.3% | -0.11 | 0.53 | 3.4% | 47.0% | -0.12 | 82 | 428 | 87 | 1.92 |
| timeframe | 1h | 42336 | 36.1% | -0.08 | 0.45 | 1.4% | 22.2% | -0.10 | 17 | 49 | 21 | 0.08 |
| mean_type | sma | 42336 | 39.4% | -0.08 | 0.48 | 2.7% | 38.4% | -0.09 | 52 | 315 | 71 | 1.44 |
| mean_type | ema | 42336 | 36.0% | -0.11 | 0.49 | 2.1% | 30.8% | -0.15 | 31 | 162 | 37 | 0.56 |
| mean_lookback | 20 | 12096 | 36.4% | -0.04 | 0.53 | 2.5% | 12.6% | -0.25 | 7 | 24 | 4 | 0.00 |
| mean_lookback | 30 | 12096 | 38.3% | -0.09 | 0.49 | 2.7% | 24.8% | -0.15 | 21 | 66 | 14 | 0.63 |
| mean_lookback | 40 | 12096 | 39.3% | -0.08 | 0.47 | 2.0% | 32.7% | -0.10 | 39 | 56 | 10 | 0.63 |
| mean_lookback | 50 | 12096 | 39.5% | -0.07 | 0.46 | 2.7% | 37.6% | -0.05 | 52 | 107 | 17 | 2.10 |
| mean_lookback | 60 | 12096 | 36.5% | -0.11 | 0.44 | 2.0% | 41.2% | -0.12 | 63 | 66 | 16 | 0.70 |
| mean_lookback | 80 | 12096 | 36.4% | -0.13 | 0.47 | 2.2% | 45.6% | -0.12 | 80 | 52 | 11 | 0.70 |
| mean_lookback | 100 | 12096 | 37.5% | -0.11 | 0.51 | 2.6% | 47.6% | -0.12 | 92 | 106 | 36 | 2.24 |
| std_lookback | 10 | 12096 | 26.4% | -0.18 | 0.27 | 0.7% | 83.7% | -0.23 | 234 | 12 | 7 | 0.00 |
| std_lookback | 15 | 12096 | 32.6% | -0.11 | 0.38 | 1.1% | 66.5% | -0.13 | 164 | 86 | 24 | 0.49 |
| std_lookback | 20 | 12096 | 33.3% | -0.07 | 0.33 | 0.3% | 55.3% | -0.09 | 116 | 15 | 4 | 0.00 |
| std_lookback | 60 | 12096 | 40.1% | -0.08 | 0.55 | 3.2% | 15.3% | 0.12 | 17 | 113 | 14 | 2.80 |
| std_lookback | 80 | 12096 | 44.7% | -0.02 | 0.72 | 7.6% | 10.5% | 0.39 | 13 | 155 | 39 | 2.17 |
| std_lookback | 100 | 12096 | 42.5% | -0.03 | 0.54 | 2.6% | 6.5% | 0.40 | 9 | 96 | 20 | 1.54 |
| std_lookback | 120 | 12096 | 44.3% | -0.03 | 0.46 | 1.1% | 4.2% | 0.12 | 8 | 0 | 0 | 0.00 |
| entry_z | -2.5 | 21168 | 42.0% | -0.05 | 0.48 | 2.4% | 52.2% | -0.07 | 106 | 197 | 48 | 0.76 |
| entry_z | -3.0 | 21168 | 41.3% | -0.07 | 0.52 | 3.6% | 36.8% | -0.08 | 49 | 232 | 48 | 3.24 |
| entry_z | -3.5 | 21168 | 37.0% | -0.13 | 0.49 | 2.3% | 27.3% | -0.15 | 20 | 29 | 6 | 0.00 |
| entry_z | -4.0 | 21168 | 30.5% | -0.16 | 0.45 | 1.2% | 22.1% | -0.21 | 6 | 19 | 6 | 0.00 |
| exit_z | -1.25 | 14112 | 38.3% | -0.09 | 0.49 | 2.4% | 34.6% | -0.12 | 40 | 74 | 23 | 1.20 |
| exit_z | -1.0 | 14112 | 37.6% | -0.09 | 0.49 | 2.4% | 34.6% | -0.12 | 40 | 82 | 27 | 1.08 |
| exit_z | -0.5 | 14112 | 37.3% | -0.10 | 0.48 | 2.4% | 34.6% | -0.11 | 40 | 81 | 16 | 0.84 |
| exit_z | 0.0 | 14112 | 37.4% | -0.10 | 0.48 | 2.4% | 34.6% | -0.12 | 40 | 81 | 10 | 0.90 |
| exit_z | 0.5 | 14112 | 37.8% | -0.09 | 0.48 | 2.4% | 34.6% | -0.11 | 40 | 80 | 16 | 1.02 |
| exit_z | 1.0 | 14112 | 37.8% | -0.09 | 0.48 | 2.4% | 34.6% | -0.11 | 40 | 79 | 16 | 0.96 |
| max_holding_bars | 3 | 28224 | 38.5% | -0.09 | 0.56 | 4.3% | 34.8% | -0.15 | 40 | 234 | 42 | 1.71 |
| max_holding_bars | 5 | 28224 | 40.8% | -0.06 | 0.50 | 1.9% | 34.7% | -0.14 | 40 | 116 | 28 | 0.30 |
| max_holding_bars | 8 | 28224 | 33.9% | -0.13 | 0.39 | 0.9% | 34.3% | -0.07 | 39 | 127 | 38 | 0.99 |
| entry_confirmation | none | 42336 | 51.9% | 0.06 | 0.61 | 4.4% | 43.7% | -0.12 | 72 | 445 | 96 | 2.00 |
| entry_confirmation | positive_bar_return | 42336 | 23.5% | -0.27 | 0.29 | 0.4% | 25.5% | -0.11 | 17 | 32 | 12 | 0.00 |
| stop_atr_multiple | none | 28224 | 44.0% | -0.01 | 0.56 | 3.6% | 31.0% | -0.09 | 35 | 206 | 48 | 1.71 |
| stop_atr_multiple | 1.0 | 28224 | 29.0% | -0.20 | 0.35 | 0.9% | 38.4% | -0.13 | 47 | 90 | 22 | 0.36 |
| stop_atr_multiple | 2.0 | 28224 | 40.1% | -0.07 | 0.51 | 2.7% | 34.4% | -0.12 | 38 | 181 | 38 | 0.93 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 15min | sma | 50 | 60 | -3.0 | -0.5 | 3 | none | none | 119 | 20.7% | 1.32 | -3.7% | s6 deduplicated |
| 2 | 15min | sma | 50 | 60 | -3.0 | -1.25 | 3 | none | none | 119 | 20.5% | 1.32 | -3.7% | s6 deduplicated |
| 3 | 15min | sma | 50 | 60 | -3.0 | -1.0 | 3 | none | none | 119 | 20.5% | 1.32 | -3.7% | s6 deduplicated |
| 4 | 15min | sma | 50 | 60 | -3.0 | 0.0 | 3 | none | none | 119 | 20.4% | 1.31 | -3.7% | s6 deduplicated |
| 5 | 15min | sma | 50 | 60 | -3.0 | 0.5 | 3 | none | none | 119 | 20.4% | 1.31 | -3.7% | s6 deduplicated |
| 6 | 15min | sma | 50 | 60 | -3.0 | 1.0 | 3 | none | none | 119 | 20.4% | 1.31 | -3.7% | s6 deduplicated |
| 7 | 15min | sma | 50 | 60 | -3.0 | -1.25 | 5 | none | none | 117 | 26.5% | 1.26 | -5.7% | s6 deduplicated |
| 8 | 15min | sma | 50 | 60 | -3.0 | -0.5 | 3 | none | 2.0 | 131 | 19.3% | 1.22 | -3.5% | s6 deduplicated |
| 9 | 15min | sma | 50 | 60 | -3.0 | -1.0 | 8 | none | none | 114 | 29.6% | 1.22 | -4.3% | s6 deduplicated |
| 10 | 15min | sma | 50 | 60 | -3.0 | -1.0 | 5 | none | none | 116 | 26.5% | 1.21 | -5.7% | s6 deduplicated |
| 11 | 15min | sma | 50 | 60 | -3.0 | -1.25 | 3 | none | 2.0 | 131 | 19.0% | 1.21 | -3.5% | s7 pass |
| 12 | 15min | sma | 50 | 60 | -3.0 | -1.0 | 3 | none | 2.0 | 131 | 19.0% | 1.21 | -3.5% | s7 pass |
| 13 | 15min | sma | 50 | 60 | -3.0 | 0.0 | 3 | none | 2.0 | 131 | 18.9% | 1.20 | -3.5% | s6 deduplicated |
| 14 | 15min | sma | 50 | 60 | -3.0 | 0.5 | 3 | none | 2.0 | 131 | 18.9% | 1.20 | -3.5% | s6 deduplicated |
| 15 | 15min | sma | 50 | 60 | -3.0 | 1.0 | 3 | none | 2.0 | 131 | 18.9% | 1.20 | -3.5% | s6 deduplicated |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
