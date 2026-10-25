# Ablation (development only) -- mr_es_v3

- Symbol ES, strategy `mean_reversion_v3`, 46,080 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 22,842 configs (49.6%).
- Grid-wide: 16.1% profitable, median dev Sharpe -0.45, 198 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 46080 | 46080 |  |
| 1 backtest integrity | 46080 | 46080 |  |
| 2 trade count & coverage | 46080 | 22842 |  |
| 3 performance & risk | 22842 | 57 |  |
| 4 parameter stability | 57 | 24 |  |
| 5 time stability | 24 | 24 |  |
| 6 deduplication | 24 | 11 | best 2 per cluster |
| 7 execution stress | 11 | 11 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 11 |  | diagnostic only: unverified: 11 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| timeframe | 0.834 |
| entry_z | 0.309 |
| stop_atr_multiple | 0.235 |
| max_holding_bars | 0.102 |
| std_lookback | 0.074 |
| mean_type | 0.050 |
| entry_confirmation | 0.044 |
| exit_z | 0.031 |
| mean_lookback | 0.025 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 5min | 15360 | 5.3% | -0.92 | -0.15 | 0.1% | 69.8% | -1.03 | 334 | 0 | 0 | 0.12 |
| timeframe | 15min | 15360 | 13.8% | -0.42 | 0.17 | 0.4% | 52.9% | -0.54 | 117 | 33 | 2 | 1.47 |
| timeframe | 1h | 15360 | 29.1% | -0.08 | 0.42 | 0.8% | 26.1% | -0.06 | 24 | 24 | 9 | 1.41 |
| mean_type | sma | 23040 | 17.6% | -0.48 | 0.28 | 0.4% | 53.8% | -0.72 | 117 | 47 | 9 | 1.48 |
| mean_type | ema | 23040 | 14.6% | -0.43 | 0.23 | 0.4% | 45.4% | -0.62 | 69 | 10 | 2 | 0.52 |
| mean_lookback | 5 | 15360 | 10.0% | -0.45 | 0.18 | 0.1% | 23.6% | -0.82 | 5 | 0 | 0 | 0.09 |
| mean_lookback | 12 | 15360 | 15.2% | -0.46 | 0.22 | 0.5% | 46.7% | -0.70 | 80 | 0 | 0 | 0.36 |
| mean_lookback | 40 | 15360 | 23.1% | -0.43 | 0.31 | 0.7% | 78.4% | -0.58 | 334 | 57 | 11 | 2.55 |
| std_lookback | 10 | 11520 | 17.4% | -0.44 | 0.36 | 0.5% | 53.1% | -0.70 | 136 | 8 | 2 | 0.80 |
| std_lookback | 20 | 11520 | 16.4% | -0.45 | 0.28 | 0.7% | 55.9% | -0.61 | 143 | 33 | 2 | 2.00 |
| std_lookback | 40 | 11520 | 13.0% | -0.50 | 0.16 | 0.1% | 49.4% | -0.71 | 94 | 0 | 0 | 0.16 |
| std_lookback | 80 | 11520 | 17.7% | -0.43 | 0.26 | 0.4% | 39.9% | -0.67 | 58 | 16 | 7 | 1.04 |
| entry_z | -1.5 | 11520 | 12.4% | -0.65 | 0.12 | 0.0% | 73.1% | -0.81 | 316 | 0 | 0 | 0.40 |
| entry_z | -2.0 | 11520 | 14.1% | -0.46 | 0.16 | 0.3% | 55.7% | -0.67 | 134 | 16 | 7 | 1.16 |
| entry_z | -2.5 | 11520 | 19.8% | -0.37 | 0.34 | 0.8% | 41.1% | -0.57 | 55 | 25 | 2 | 1.56 |
| entry_z | -3.0 | 11520 | 18.0% | -0.34 | 0.43 | 0.6% | 28.4% | -0.50 | 14 | 16 | 2 | 0.88 |
| exit_z | -1.0 | 11520 | 18.6% | -0.45 | 0.32 | 0.5% | 49.8% | -0.66 | 98 | 23 | 5 | 1.36 |
| exit_z | -0.5 | 11520 | 16.1% | -0.47 | 0.25 | 0.5% | 49.6% | -0.71 | 96 | 13 | 5 | 1.08 |
| exit_z | 0.0 | 11520 | 14.6% | -0.45 | 0.22 | 0.3% | 49.5% | -0.67 | 96 | 11 | 1 | 0.64 |
| exit_z | 0.5 | 11520 | 15.1% | -0.44 | 0.23 | 0.4% | 49.4% | -0.67 | 96 | 10 | 0 | 0.92 |
| max_holding_bars | 5 | 11520 | 15.5% | -0.51 | 0.28 | 0.9% | 49.7% | -0.78 | 98 | 34 | 3 | 1.68 |
| max_holding_bars | 10 | 11520 | 16.0% | -0.47 | 0.27 | 0.2% | 49.7% | -0.68 | 98 | 9 | 4 | 1.00 |
| max_holding_bars | 16 | 11520 | 16.4% | -0.44 | 0.26 | 0.3% | 49.5% | -0.64 | 96 | 10 | 4 | 0.92 |
| max_holding_bars | 30 | 11520 | 16.4% | -0.40 | 0.24 | 0.3% | 49.3% | -0.58 | 95 | 4 | 0 | 0.40 |
| entry_confirmation | none | 23040 | 16.8% | -0.47 | 0.20 | 0.3% | 68.1% | -0.65 | 220 | 16 | 7 | 0.70 |
| entry_confirmation | positive_bar_return | 23040 | 15.4% | -0.43 | 0.35 | 0.5% | 31.1% | -0.77 | 19 | 41 | 4 | 1.30 |
| stop_atr_multiple | none | 9216 | 19.4% | -0.34 | 0.32 | 0.7% | 46.8% | -0.48 | 85 | 21 | 2 | 1.65 |
| stop_atr_multiple | 1.0 | 9216 | 13.7% | -0.57 | 0.19 | 0.2% | 51.7% | -0.81 | 110 | 5 | 3 | 0.70 |
| stop_atr_multiple | 1.5 | 9216 | 15.3% | -0.51 | 0.25 | 0.4% | 50.5% | -0.80 | 103 | 8 | 2 | 1.05 |
| stop_atr_multiple | 2.0 | 9216 | 15.9% | -0.45 | 0.26 | 0.5% | 49.8% | -0.70 | 98 | 8 | 2 | 0.60 |
| stop_atr_multiple | 2.5 | 9216 | 16.3% | -0.43 | 0.27 | 0.4% | 49.1% | -0.64 | 92 | 15 | 2 | 1.00 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 15min | sma | 40 | 20 | -3.0 | -1.0 | 5 | positive_bar_return | 2.5 | 188 | 27.1% | 1.00 | -4.7% | s4 hard_reject |
| 2 | 15min | sma | 40 | 20 | -3.0 | 0.0 | 5 | positive_bar_return | 2.5 | 188 | 25.3% | 0.99 | -5.5% | s4 hard_reject |
| 3 | 15min | sma | 40 | 20 | -2.5 | -1.0 | 5 | positive_bar_return | none | 299 | 33.9% | 0.98 | -5.8% | s4 hard_reject |
| 4 | 15min | ema | 40 | 20 | -2.5 | -0.5 | 5 | positive_bar_return | none | 184 | 28.2% | 0.97 | -6.6% | s4 hard_reject |
| 5 | 15min | sma | 40 | 20 | -3.0 | -0.5 | 5 | positive_bar_return | 2.5 | 188 | 24.6% | 0.97 | -5.5% | s4 hard_reject |
| 6 | 15min | sma | 40 | 20 | -2.5 | -1.0 | 16 | positive_bar_return | none | 261 | 40.4% | 0.96 | -10.8% | s4 hard_reject |
| 7 | 15min | ema | 40 | 20 | -2.5 | 0.0 | 5 | positive_bar_return | none | 184 | 27.1% | 0.95 | -6.9% | s4 hard_reject |
| 8 | 15min | ema | 40 | 20 | -2.5 | 0.5 | 5 | positive_bar_return | none | 184 | 27.3% | 0.95 | -6.9% | s4 hard_reject |
| 9 | 1h | sma | 40 | 80 | -2.0 | -1.0 | 30 | none | 2.5 | 102 | 36.9% | 0.94 | -10.2% | s6 deduplicated |
| 10 | 15min | ema | 40 | 20 | -2.5 | -0.5 | 16 | positive_bar_return | none | 164 | 37.6% | 0.94 | -10.7% | s7 pass |
| 11 | 1h | sma | 40 | 80 | -2.0 | -1.0 | 30 | none | 2.0 | 110 | 36.3% | 0.94 | -11.0% | s6 deduplicated |
| 12 | 15min | ema | 40 | 20 | -2.5 | -0.5 | 5 | positive_bar_return | 2.5 | 195 | 29.2% | 0.93 | -7.1% | s4 hard_reject |
| 13 | 1h | sma | 40 | 10 | -3.0 | -0.5 | 5 | positive_bar_return | 2.0 | 103 | 36.2% | 0.93 | -7.4% | s7 pass |
| 14 | 15min | sma | 40 | 20 | -2.5 | -0.5 | 5 | positive_bar_return | none | 299 | 31.0% | 0.93 | -5.6% | s4 hard_reject |
| 15 | 15min | sma | 40 | 20 | -3.0 | 0.5 | 5 | positive_bar_return | 2.5 | 188 | 23.9% | 0.93 | -6.4% | s4 hard_reject |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
