# Ablation (development only) -- mr_nq_v7_1h

- Symbol NQ, strategy `mean_reversion_v13`, 3,456 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 901 configs (26.1%).
- Grid-wide: 54.3% profitable, median dev Sharpe 0.16, 321 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 3456 | 3456 |  |
| 1 backtest integrity | 3456 | 3456 |  |
| 2 trade count & coverage | 3456 | 901 |  |
| 3 performance & risk | 901 | 214 |  |
| 4 parameter stability | 214 | 214 |  |
| 5 time stability | 214 | 214 |  |
| 6 deduplication | 214 | 153 | best 2 per cluster |
| 7 execution stress | 153 | 153 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 153 |  | diagnostic only: unverified: 153 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| std_lookback | 1.036 |
| entry_z | 0.229 |
| mean_type | 0.227 |
| stop_atr_multiple | 0.191 |
| mean_lookback | 0.172 |
| max_holding_bars | 0.059 |
| exit_z | 0.048 |
| timeframe | 0.000 |
| entry_confirmation | 0.000 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 1h | 3456 | 54.3% | 0.16 | 0.75 | 9.3% | 26.1% | 0.57 | 41 | 214 | 153 | 1.00 |
| mean_type | sma | 1728 | 63.5% | 0.26 | 0.77 | 10.6% | 32.2% | 0.57 | 56 | 133 | 94 | 1.10 |
| mean_type | ema | 1728 | 45.1% | 0.04 | 0.72 | 8.0% | 20.0% | 0.56 | 27 | 81 | 59 | 0.90 |
| mean_lookback | 23 | 864 | 43.3% | 0.04 | 0.67 | 4.7% | 18.4% | 0.52 | 20 | 31 | 20 | 0.44 |
| mean_lookback | 28 | 864 | 53.5% | 0.18 | 0.81 | 11.7% | 24.2% | 0.59 | 39 | 50 | 39 | 0.88 |
| mean_lookback | 32 | 864 | 57.9% | 0.21 | 0.82 | 12.8% | 29.4% | 0.63 | 48 | 82 | 59 | 1.68 |
| mean_lookback | 37 | 864 | 62.7% | 0.21 | 0.71 | 7.9% | 32.3% | 0.51 | 63 | 51 | 35 | 1.00 |
| std_lookback | 6 | 432 | 89.1% | 0.49 | 0.84 | 14.8% | 98.6% | 0.50 | 167 | 64 | 53 | 1.76 |
| std_lookback | 9 | 432 | 95.1% | 0.56 | 0.95 | 26.2% | 60.9% | 0.65 | 113 | 89 | 55 | 4.16 |
| std_lookback | 12 | 432 | 75.9% | 0.41 | 0.87 | 17.6% | 28.5% | 0.61 | 72 | 40 | 30 | 1.52 |
| std_lookback | 15 | 432 | 73.1% | 0.30 | 0.75 | 10.2% | 13.9% | 0.50 | 45 | 10 | 9 | 0.40 |
| std_lookback | 20 | 432 | 44.7% | 0.03 | 0.61 | 5.6% | 6.7% | 0.69 | 21 | 11 | 6 | 0.16 |
| std_lookback | 30 | 432 | 19.9% | -0.23 | 0.26 | 0.0% | 0.0% | n/a | 6 | 0 | 0 | 0.00 |
| std_lookback | 50 | 432 | 22.2% | -0.47 | 0.26 | 0.0% | 0.0% | n/a | 8 | 0 | 0 | 0.00 |
| std_lookback | 70 | 432 | 14.6% | -0.32 | 0.11 | 0.0% | 0.0% | n/a | 9 | 0 | 0 | 0.00 |
| entry_z | -2.0 | 1152 | 72.7% | 0.28 | 0.81 | 13.2% | 41.1% | 0.55 | 81 | 101 | 73 | 1.41 |
| entry_z | -2.5 | 1152 | 50.7% | 0.07 | 0.74 | 9.4% | 22.0% | 0.63 | 26 | 77 | 56 | 1.02 |
| entry_z | -3.0 | 1152 | 39.7% | 0.05 | 0.67 | 5.3% | 15.1% | 0.50 | 13 | 36 | 24 | 0.57 |
| exit_z | -1.0 | 1728 | 53.8% | 0.14 | 0.70 | 6.4% | 26.2% | 0.54 | 41 | 73 | 35 | 0.50 |
| exit_z | 0.0 | 1728 | 54.9% | 0.18 | 0.82 | 12.2% | 25.9% | 0.61 | 41 | 141 | 118 | 1.50 |
| max_holding_bars | 5 | 1152 | 53.2% | 0.13 | 0.74 | 8.5% | 26.8% | 0.47 | 42 | 58 | 37 | 0.93 |
| max_holding_bars | 8 | 1152 | 54.1% | 0.16 | 0.75 | 9.0% | 26.0% | 0.56 | 41 | 69 | 49 | 0.99 |
| max_holding_bars | 12 | 1152 | 55.7% | 0.19 | 0.77 | 10.3% | 25.3% | 0.63 | 41 | 87 | 67 | 1.08 |
| entry_confirmation | positive_bar_return | 3456 | 54.3% | 0.16 | 0.75 | 9.3% | 26.1% | 0.57 | 41 | 214 | 153 | 1.00 |
| stop_atr_multiple | none | 1152 | 48.2% | 0.05 | 0.57 | 3.1% | 20.9% | 0.28 | 37 | 2 | 2 | 0.06 |
| stop_atr_multiple | 1.5 | 1152 | 57.4% | 0.24 | 0.84 | 13.7% | 29.2% | 0.67 | 44 | 119 | 90 | 1.68 |
| stop_atr_multiple | 2.0 | 1152 | 57.5% | 0.23 | 0.78 | 11.0% | 28.1% | 0.63 | 43 | 93 | 61 | 1.26 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 1h | ema | 32 | 12 | -2.0 | 0.0 | 5 | positive_bar_return | 1.5 | 114 | 65.5% | 1.31 | -6.0% | s7 pass |
| 2 | 1h | sma | 32 | 9 | -3.0 | 0.0 | 8 | positive_bar_return | 1.5 | 120 | 59.3% | 1.24 | -8.6% | s7 pass |
| 3 | 1h | sma | 28 | 9 | -2.5 | 0.0 | 5 | positive_bar_return | 1.5 | 142 | 59.0% | 1.22 | -5.4% | s7 pass |
| 4 | 1h | sma | 37 | 9 | -3.0 | 0.0 | 8 | positive_bar_return | 1.5 | 145 | 72.1% | 1.22 | -7.2% | s7 pass |
| 5 | 1h | sma | 28 | 9 | -2.5 | -1.0 | 5 | positive_bar_return | 1.5 | 142 | 54.7% | 1.18 | -5.5% | s7 pass |
| 6 | 1h | ema | 32 | 12 | -2.0 | 0.0 | 8 | positive_bar_return | 1.5 | 114 | 64.6% | 1.17 | -9.3% | s7 pass |
| 7 | 1h | sma | 32 | 12 | -2.5 | 0.0 | 5 | positive_bar_return | 1.5 | 108 | 50.9% | 1.15 | -7.7% | s7 pass |
| 8 | 1h | ema | 28 | 9 | -2.0 | 0.0 | 8 | positive_bar_return | 1.5 | 148 | 66.5% | 1.14 | -6.6% | s7 pass |
| 9 | 1h | ema | 32 | 9 | -2.5 | 0.0 | 8 | positive_bar_return | 1.5 | 112 | 54.3% | 1.14 | -5.9% | s7 pass |
| 10 | 1h | sma | 37 | 9 | -3.0 | -1.0 | 8 | positive_bar_return | 1.5 | 145 | 61.8% | 1.14 | -7.2% | s7 pass |
| 11 | 1h | sma | 28 | 9 | -2.5 | 0.0 | 8 | positive_bar_return | 1.5 | 148 | 55.5% | 1.13 | -6.1% | s7 pass |
| 12 | 1h | ema | 32 | 9 | -2.0 | 0.0 | 8 | positive_bar_return | 1.5 | 159 | 64.9% | 1.13 | -6.9% | s7 pass |
| 13 | 1h | ema | 32 | 12 | -2.0 | -1.0 | 5 | positive_bar_return | 1.5 | 115 | 49.4% | 1.12 | -6.1% | s7 pass |
| 14 | 1h | sma | 23 | 12 | -2.0 | -1.0 | 5 | positive_bar_return | 1.5 | 124 | 39.7% | 1.12 | -6.5% | s7 pass |
| 15 | 1h | sma | 32 | 9 | -3.0 | 0.0 | 5 | positive_bar_return | 1.5 | 117 | 44.8% | 1.11 | -5.6% | s7 pass |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
