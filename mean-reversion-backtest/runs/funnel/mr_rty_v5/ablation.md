# Ablation (development only) -- mr_rty_v5

- Symbol RTY, strategy `mean_reversion_v5`, 41,472 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 29,848 configs (72.0%).
- Grid-wide: 23.8% profitable, median dev Sharpe -0.26, 164 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 41472 | 41472 |  |
| 1 backtest integrity | 41472 | 41472 |  |
| 2 trade count & coverage | 41472 | 29848 |  |
| 3 performance & risk | 29848 | 69 |  |
| 4 parameter stability | 69 | 63 |  |
| 5 time stability | 63 | 61 |  |
| 6 deduplication | 61 | 27 | best 2 per cluster |
| 7 execution stress | 27 | 27 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 27 |  | diagnostic only: unverified: 27 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| timeframe | 0.421 |
| stop_atr_multiple | 0.211 |
| entry_z | 0.179 |
| std_lookback | 0.162 |
| entry_confirmation | 0.084 |
| mean_lookback | 0.066 |
| max_holding_bars | 0.053 |
| mean_type | 0.033 |
| exit_z | 0.013 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 5min | 13824 | 8.2% | -0.53 | -0.01 | 0.0% | 92.5% | -0.55 | 1016 | 0 | 0 | 0.06 |
| timeframe | 15min | 13824 | 30.6% | -0.17 | 0.32 | 0.7% | 79.3% | -0.17 | 346 | 57 | 21 | 2.40 |
| timeframe | 1h | 13824 | 32.6% | -0.11 | 0.33 | 0.5% | 44.1% | -0.10 | 84 | 12 | 6 | 0.54 |
| mean_type | sma | 20736 | 22.7% | -0.28 | 0.24 | 0.4% | 76.4% | -0.30 | 310 | 52 | 20 | 1.36 |
| mean_type | ema | 20736 | 24.8% | -0.25 | 0.26 | 0.4% | 67.5% | -0.28 | 220 | 17 | 7 | 0.64 |
| mean_lookback | 20 | 6912 | 21.9% | -0.29 | 0.25 | 0.5% | 50.0% | -0.35 | 99 | 11 | 4 | 0.84 |
| mean_lookback | 30 | 6912 | 23.6% | -0.26 | 0.26 | 0.4% | 63.9% | -0.30 | 191 | 12 | 5 | 0.90 |
| mean_lookback | 40 | 6912 | 26.5% | -0.23 | 0.27 | 0.3% | 72.3% | -0.26 | 264 | 5 | 3 | 0.48 |
| mean_lookback | 50 | 6912 | 27.0% | -0.25 | 0.28 | 0.5% | 78.2% | -0.29 | 331 | 18 | 7 | 1.56 |
| mean_lookback | 60 | 6912 | 21.9% | -0.25 | 0.21 | 0.3% | 81.7% | -0.27 | 373 | 5 | 1 | 0.60 |
| mean_lookback | 80 | 6912 | 21.6% | -0.28 | 0.22 | 0.4% | 85.7% | -0.30 | 419 | 18 | 7 | 1.62 |
| std_lookback | 10 | 5184 | 13.7% | -0.37 | 0.11 | 0.0% | 95.2% | -0.40 | 626 | 0 | 0 | 0.00 |
| std_lookback | 15 | 5184 | 24.7% | -0.26 | 0.28 | 0.4% | 85.9% | -0.31 | 471 | 13 | 8 | 1.28 |
| std_lookback | 20 | 5184 | 23.2% | -0.23 | 0.23 | 0.1% | 79.9% | -0.28 | 377 | 1 | 1 | 0.24 |
| std_lookback | 25 | 5184 | 21.7% | -0.25 | 0.19 | 0.0% | 73.9% | -0.28 | 305 | 0 | 0 | 0.08 |
| std_lookback | 30 | 5184 | 23.0% | -0.28 | 0.24 | 0.1% | 69.0% | -0.32 | 237 | 4 | 2 | 0.32 |
| std_lookback | 40 | 5184 | 23.9% | -0.25 | 0.24 | 0.1% | 64.1% | -0.28 | 182 | 4 | 0 | 0.64 |
| std_lookback | 60 | 5184 | 27.2% | -0.25 | 0.30 | 0.7% | 57.0% | -0.21 | 129 | 20 | 4 | 2.16 |
| std_lookback | 80 | 5184 | 32.6% | -0.21 | 0.43 | 1.7% | 50.8% | -0.18 | 103 | 27 | 12 | 3.28 |
| entry_z | -2.0 | 13824 | 15.9% | -0.36 | 0.14 | 0.1% | 87.8% | -0.36 | 460 | 7 | 5 | 0.39 |
| entry_z | -2.5 | 13824 | 24.9% | -0.24 | 0.25 | 0.3% | 71.8% | -0.27 | 250 | 19 | 7 | 0.84 |
| entry_z | -3.0 | 13824 | 30.5% | -0.18 | 0.35 | 0.7% | 56.3% | -0.21 | 135 | 43 | 15 | 1.77 |
| exit_z | -1.0 | 10368 | 24.4% | -0.25 | 0.26 | 0.4% | 72.1% | -0.28 | 261 | 21 | 12 | 1.28 |
| exit_z | -0.5 | 10368 | 23.9% | -0.26 | 0.25 | 0.4% | 72.0% | -0.29 | 259 | 15 | 6 | 0.88 |
| exit_z | 0.0 | 10368 | 23.4% | -0.26 | 0.24 | 0.4% | 71.9% | -0.29 | 258 | 15 | 5 | 0.84 |
| exit_z | 0.5 | 10368 | 23.4% | -0.27 | 0.25 | 0.4% | 71.9% | -0.30 | 257 | 18 | 4 | 1.00 |
| max_holding_bars | 5 | 20736 | 24.8% | -0.29 | 0.30 | 0.6% | 72.3% | -0.36 | 261 | 49 | 19 | 1.44 |
| max_holding_bars | 10 | 20736 | 22.7% | -0.24 | 0.21 | 0.2% | 71.6% | -0.23 | 256 | 20 | 8 | 0.56 |
| entry_confirmation | none | 20736 | 25.9% | -0.22 | 0.29 | 0.7% | 85.0% | -0.26 | 452 | 68 | 26 | 1.90 |
| entry_confirmation | positive_bar_return | 20736 | 21.6% | -0.31 | 0.21 | 0.1% | 59.0% | -0.34 | 143 | 1 | 1 | 0.10 |
| stop_atr_multiple | none | 13824 | 31.5% | -0.16 | 0.34 | 0.8% | 68.2% | -0.21 | 201 | 52 | 23 | 2.07 |
| stop_atr_multiple | 1.0 | 13824 | 16.5% | -0.37 | 0.15 | 0.1% | 75.6% | -0.37 | 331 | 10 | 3 | 0.54 |
| stop_atr_multiple | 2.0 | 13824 | 23.3% | -0.26 | 0.24 | 0.3% | 72.1% | -0.30 | 247 | 7 | 1 | 0.39 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 15min | sma | 50 | 60 | -3.0 | -1.0 | 5 | none | none | 116 | 26.5% | 1.21 | -5.7% | s7 pass |
| 2 | 15min | sma | 50 | 60 | -3.0 | -0.5 | 5 | none | none | 116 | 25.6% | 1.18 | -5.7% | s7 pass |
| 3 | 15min | sma | 50 | 60 | -3.0 | 0.0 | 5 | none | none | 116 | 25.6% | 1.18 | -5.7% | s6 deduplicated |
| 4 | 15min | sma | 50 | 60 | -3.0 | 0.5 | 5 | none | none | 116 | 25.6% | 1.18 | -5.7% | s6 deduplicated |
| 5 | 1h | ema | 80 | 15 | -3.0 | 0.5 | 10 | none | none | 118 | 56.5% | 0.98 | -11.2% | s7 pass |
| 6 | 1h | sma | 80 | 15 | -3.0 | 0.5 | 10 | none | none | 126 | 50.6% | 0.91 | -8.3% | s7 pass |
| 7 | 1h | ema | 80 | 15 | -3.0 | 0.0 | 10 | none | none | 118 | 50.7% | 0.91 | -11.3% | s7 pass |
| 8 | 15min | sma | 20 | 80 | -2.5 | -1.0 | 5 | none | none | 102 | 15.9% | 0.88 | -3.1% | s7 pass |
| 9 | 1h | sma | 80 | 15 | -3.0 | 0.0 | 10 | none | none | 126 | 47.8% | 0.88 | -8.4% | s7 pass |
| 10 | 15min | sma | 60 | 80 | -3.0 | -1.0 | 5 | none | none | 101 | 15.4% | 0.88 | -3.8% | s6 deduplicated |
| 11 | 1h | sma | 80 | 15 | -3.0 | 0.5 | 10 | none | 2.0 | 171 | 53.8% | 0.87 | -12.2% | s6 deduplicated |
| 12 | 15min | sma | 80 | 80 | -3.0 | -1.0 | 5 | none | none | 122 | 15.3% | 0.87 | -4.1% | s7 pass |
| 13 | 15min | sma | 50 | 15 | -2.0 | -1.0 | 5 | positive_bar_return | none | 511 | 36.7% | 0.86 | -10.3% | s7 pass |
| 14 | 15min | sma | 20 | 80 | -2.5 | -0.5 | 5 | none | none | 102 | 15.4% | 0.86 | -3.1% | s7 pass |
| 15 | 15min | sma | 30 | 60 | -3.0 | -1.0 | 5 | none | 1.0 | 132 | 13.6% | 0.85 | -4.2% | s7 pass |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
