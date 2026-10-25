# Ablation (development only) -- mr_nq_v7_15m

- Symbol NQ, strategy `mean_reversion_v12`, 1,152 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 586 configs (50.9%).
- Grid-wide: 36.3% profitable, median dev Sharpe -0.12, 14 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 1152 | 1152 |  |
| 1 backtest integrity | 1152 | 1152 |  |
| 2 trade count & coverage | 1152 | 586 |  |
| 3 performance & risk | 586 | 12 |  |
| 4 parameter stability | 12 | 11 |  |
| 5 time stability | 11 | 11 |  |
| 6 deduplication | 11 | 8 | best 2 per cluster |
| 7 execution stress | 8 | 8 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 8 |  | diagnostic only: unverified: 8 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| std_lookback | 0.434 |
| max_holding_bars | 0.349 |
| entry_z | 0.226 |
| mean_lookback | 0.197 |
| mean_type | 0.004 |
| exit_z | 0.004 |
| timeframe | 0.000 |
| entry_confirmation | 0.000 |
| stop_atr_multiple | 0.000 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 15min | 1152 | 36.3% | -0.12 | 0.41 | 1.2% | 50.9% | -0.03 | 103 | 12 | 8 | 1.00 |
| mean_type | sma | 576 | 35.9% | -0.12 | 0.42 | 1.9% | 61.5% | -0.04 | 121 | 11 | 8 | 1.14 |
| mean_type | ema | 576 | 36.6% | -0.12 | 0.41 | 0.5% | 40.3% | -0.02 | 79 | 1 | 0 | 0.86 |
| mean_lookback | 40 | 192 | 35.4% | -0.11 | 0.45 | 1.6% | 27.1% | -0.04 | 49 | 1 | 0 | 0.42 |
| mean_lookback | 50 | 192 | 26.6% | -0.18 | 0.33 | 0.0% | 39.6% | -0.15 | 68 | 0 | 0 | 0.36 |
| mean_lookback | 60 | 192 | 30.7% | -0.21 | 0.40 | 2.1% | 46.9% | -0.11 | 97 | 4 | 2 | 0.84 |
| mean_lookback | 70 | 192 | 33.9% | -0.12 | 0.42 | 3.1% | 56.2% | -0.04 | 128 | 6 | 6 | 1.56 |
| mean_lookback | 80 | 192 | 45.3% | -0.05 | 0.38 | 0.5% | 64.6% | 0.04 | 154 | 1 | 0 | 1.38 |
| mean_lookback | 90 | 192 | 45.8% | -0.01 | 0.41 | 0.0% | 70.8% | 0.04 | 177 | 0 | 0 | 1.44 |
| std_lookback | 18 | 144 | 28.5% | -0.09 | 0.37 | 2.1% | 97.2% | -0.10 | 297 | 1 | 0 | 0.96 |
| std_lookback | 23 | 144 | 67.4% | 0.17 | 0.54 | 6.2% | 86.1% | 0.21 | 230 | 9 | 6 | 3.36 |
| std_lookback | 28 | 144 | 47.9% | 0.01 | 0.40 | 1.4% | 63.9% | -0.13 | 154 | 2 | 2 | 1.20 |
| std_lookback | 33 | 144 | 32.6% | -0.15 | 0.37 | 0.0% | 52.8% | -0.13 | 110 | 0 | 0 | 0.48 |
| std_lookback | 38 | 144 | 36.1% | -0.18 | 0.42 | 0.0% | 41.7% | -0.15 | 71 | 0 | 0 | 0.80 |
| std_lookback | 43 | 144 | 32.6% | -0.25 | 0.39 | 0.0% | 33.3% | -0.14 | 63 | 0 | 0 | 0.64 |
| std_lookback | 60 | 144 | 16.7% | -0.26 | 0.13 | 0.0% | 22.2% | -0.09 | 39 | 0 | 0 | 0.24 |
| std_lookback | 80 | 144 | 28.5% | -0.20 | 0.36 | 0.0% | 9.7% | 0.09 | 42 | 0 | 0 | 0.32 |
| entry_z | -2.5 | 384 | 45.3% | -0.03 | 0.45 | 1.8% | 80.7% | -0.00 | 184 | 7 | 4 | 2.04 |
| entry_z | -3.0 | 384 | 35.7% | -0.12 | 0.33 | 1.3% | 44.8% | -0.08 | 86 | 5 | 4 | 0.60 |
| entry_z | -3.5 | 384 | 27.9% | -0.25 | 0.35 | 0.5% | 27.1% | -0.02 | 37 | 0 | 0 | 0.36 |
| exit_z | -1.0 | 576 | 35.9% | -0.12 | 0.42 | 1.4% | 50.9% | -0.04 | 103 | 7 | 4 | 1.00 |
| exit_z | -0.5 | 576 | 36.6% | -0.12 | 0.41 | 1.0% | 50.9% | -0.03 | 103 | 5 | 4 | 1.00 |
| max_holding_bars | 3 | 576 | 19.6% | -0.31 | 0.20 | 0.0% | 51.0% | -0.23 | 103 | 0 | 0 | 0.34 |
| max_holding_bars | 5 | 576 | 53.0% | 0.04 | 0.47 | 2.4% | 50.7% | 0.14 | 103 | 12 | 8 | 1.66 |
| entry_confirmation | positive_bar_return | 1152 | 36.3% | -0.12 | 0.41 | 1.2% | 50.9% | -0.03 | 103 | 12 | 8 | 1.00 |
| stop_atr_multiple | none | 1152 | 36.3% | -0.12 | 0.41 | 1.2% | 50.9% | -0.03 | 103 | 12 | 8 | 1.00 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 15min | sma | 70 | 23 | -2.5 | -1.0 | 5 | positive_bar_return | none | 338 | 42.0% | 1.07 | -11.6% | s7 pass |
| 2 | 15min | sma | 70 | 23 | -2.5 | -0.5 | 5 | positive_bar_return | none | 337 | 40.4% | 1.04 | -12.4% | s7 pass |
| 3 | 15min | sma | 60 | 23 | -2.5 | -0.5 | 5 | positive_bar_return | none | 326 | 45.4% | 1.03 | -13.3% | s6 deduplicated |
| 4 | 15min | sma | 60 | 23 | -2.5 | -1.0 | 5 | positive_bar_return | none | 326 | 45.3% | 1.02 | -13.0% | s6 deduplicated |
| 5 | 15min | sma | 70 | 28 | -2.5 | -1.0 | 5 | positive_bar_return | none | 297 | 32.1% | 0.96 | -13.4% | s7 pass |
| 6 | 15min | sma | 70 | 28 | -2.5 | -0.5 | 5 | positive_bar_return | none | 297 | 32.3% | 0.95 | -14.6% | s7 pass |
| 7 | 15min | sma | 60 | 23 | -3.0 | -1.0 | 5 | positive_bar_return | none | 257 | 32.2% | 0.91 | -6.3% | s7 pass |
| 8 | 15min | sma | 80 | 23 | -2.5 | -1.0 | 5 | positive_bar_return | none | 357 | 34.5% | 0.90 | -12.9% | s6 deduplicated |
| 9 | 15min | sma | 60 | 23 | -3.0 | -0.5 | 5 | positive_bar_return | none | 257 | 30.6% | 0.87 | -7.0% | s7 pass |
| 10 | 15min | sma | 70 | 23 | -3.0 | -1.0 | 5 | positive_bar_return | none | 282 | 29.2% | 0.81 | -11.5% | s7 pass |
| 11 | 15min | sma | 70 | 23 | -3.0 | -0.5 | 5 | positive_bar_return | none | 282 | 28.2% | 0.79 | -12.1% | s7 pass |
| 12 | 15min | ema | 40 | 18 | -3.0 | -1.0 | 5 | positive_bar_return | none | 134 | 17.0% | 0.76 | -4.8% | s4 hard_reject |
| 13 | 15min | sma | 80 | 23 | -2.5 | -0.5 | 5 | positive_bar_return | none | 356 | 30.0% | 0.72 | -13.6% | s3 hard_reject |
| 14 | 15min | sma | 90 | 43 | -2.5 | -0.5 | 5 | positive_bar_return | none | 241 | 19.3% | 0.70 | -7.2% | s3 hard_reject |
| 15 | 15min | ema | 40 | 18 | -3.0 | -0.5 | 5 | positive_bar_return | none | 134 | 15.6% | 0.69 | -6.1% | s3 hard_reject |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
