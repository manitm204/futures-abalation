# Ablation (development only) -- mr_es_v6_1h

- Symbol ES, strategy `mean_reversion_v11`, 6,804 configs, development 2018-01-01..2022-12-31. Validation and holdout are NOT used here.
- Eligible = passes stage 2 (>= 100 completed trades, >= 10/yr in >= 4 years): 3,991 configs (58.7%).
- Grid-wide: 51.9% profitable, median dev Sharpe 0.05, 218 configs with Sharpe >= 0.75.

## Funnel survival

| Stage | Evaluated | Passed | Note |
|---|---:|---:|---|
| 0 universe | 6804 | 6804 |  |
| 1 backtest integrity | 6804 | 6804 |  |
| 2 trade count & coverage | 6804 | 3991 |  |
| 3 performance & risk | 3991 | 66 |  |
| 4 parameter stability | 66 | 60 |  |
| 5 time stability | 60 | 60 |  |
| 6 deduplication | 60 | 39 | best 2 per cluster |
| 7 execution stress | 39 | 39 |  |
| 8 frozen validation |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | 39 |  | diagnostic only: unverified: 39 |
| 10 final holdout |  |  | not run; `final-test` command only |

## Which axes matter (range of per-value median dev Sharpe)

| Axis | Median-Sharpe range |
|---|---:|
| std_lookback | 0.250 |
| mean_lookback | 0.224 |
| entry_z | 0.128 |
| max_holding_bars | 0.121 |
| entry_confirmation | 0.115 |
| stop_atr_multiple | 0.082 |
| exit_z | 0.030 |
| timeframe | 0.000 |
| mean_type | 0.000 |

## Per-axis ablation

Top cohort = best 100 eligible configs by dev Sharpe; lift = share in top cohort / share of grid.

| Axis | Value | Configs | % profitable | Median SR | p90 SR | % SR>=bar | % eligible | Eligible median SR | Median trades | Stage-3 pass | Survivors | Top lift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| timeframe | 1h | 6804 | 51.9% | 0.05 | 0.54 | 3.2% | 58.7% | -0.04 | 116 | 66 | 39 | 1.00 |
| mean_type | sma | 6804 | 51.9% | 0.05 | 0.54 | 3.2% | 58.7% | -0.04 | 116 | 66 | 39 | 1.00 |
| mean_lookback | 28 | 972 | 54.6% | 0.08 | 0.57 | 3.7% | 47.1% | 0.02 | 92 | 5 | 4 | 0.56 |
| mean_lookback | 34 | 972 | 62.4% | 0.17 | 0.66 | 5.5% | 52.9% | -0.02 | 107 | 8 | 5 | 1.12 |
| mean_lookback | 40 | 972 | 61.9% | 0.16 | 0.61 | 5.0% | 57.4% | 0.05 | 116 | 13 | 11 | 1.26 |
| mean_lookback | 46 | 972 | 55.6% | 0.12 | 0.60 | 3.7% | 60.1% | 0.00 | 125 | 6 | 3 | 0.77 |
| mean_lookback | 80 | 972 | 41.7% | -0.05 | 0.44 | 2.2% | 65.9% | -0.12 | 126 | 21 | 10 | 1.54 |
| mean_lookback | 90 | 972 | 46.6% | 0.00 | 0.44 | 1.4% | 65.3% | -0.02 | 120 | 8 | 2 | 1.05 |
| mean_lookback | 100 | 972 | 40.3% | -0.05 | 0.39 | 0.9% | 61.8% | -0.12 | 115 | 5 | 4 | 0.70 |
| std_lookback | 12 | 1134 | 40.3% | -0.09 | 0.43 | 1.4% | 88.7% | -0.15 | 171 | 8 | 7 | 0.96 |
| std_lookback | 17 | 1134 | 47.1% | 0.00 | 0.49 | 1.4% | 83.8% | -0.08 | 163 | 6 | 4 | 0.78 |
| std_lookback | 22 | 1134 | 42.2% | -0.04 | 0.45 | 0.9% | 78.4% | -0.11 | 154 | 2 | 2 | 0.24 |
| std_lookback | 80 | 1134 | 58.6% | 0.12 | 0.66 | 7.0% | 38.2% | 0.03 | 83 | 32 | 16 | 2.34 |
| std_lookback | 90 | 1134 | 59.4% | 0.13 | 0.60 | 4.6% | 34.3% | 0.14 | 75 | 6 | 3 | 0.60 |
| std_lookback | 100 | 1134 | 63.7% | 0.16 | 0.59 | 4.0% | 28.6% | 0.22 | 68 | 12 | 7 | 1.08 |
| entry_z | -1.5 | 2268 | 47.2% | 0.00 | 0.43 | 0.3% | 81.7% | -0.07 | 159 | 5 | 4 | 0.39 |
| entry_z | -2.0 | 2268 | 59.5% | 0.13 | 0.65 | 6.2% | 58.8% | 0.03 | 113 | 54 | 30 | 2.34 |
| entry_z | -2.5 | 2268 | 49.0% | 0.02 | 0.53 | 3.1% | 35.4% | -0.12 | 72 | 7 | 5 | 0.27 |
| exit_z | -1.0 | 2268 | 50.4% | 0.03 | 0.54 | 3.3% | 59.2% | -0.05 | 117 | 27 | 15 | 1.08 |
| exit_z | -0.5 | 2268 | 52.1% | 0.05 | 0.55 | 3.3% | 58.4% | -0.04 | 116 | 20 | 10 | 0.99 |
| exit_z | 0.0 | 2268 | 53.1% | 0.06 | 0.53 | 3.0% | 58.4% | -0.02 | 115 | 19 | 14 | 0.93 |
| max_holding_bars | 3 | 2268 | 46.4% | -0.02 | 0.58 | 5.2% | 58.5% | -0.15 | 116 | 36 | 16 | 1.35 |
| max_holding_bars | 5 | 2268 | 52.1% | 0.06 | 0.57 | 3.0% | 58.9% | -0.02 | 117 | 19 | 15 | 1.08 |
| max_holding_bars | 8 | 2268 | 57.1% | 0.10 | 0.50 | 1.5% | 58.6% | 0.06 | 115 | 11 | 8 | 0.57 |
| entry_confirmation | none | 3402 | 45.4% | -0.02 | 0.61 | 5.2% | 76.2% | -0.18 | 159 | 52 | 27 | 1.40 |
| entry_confirmation | positive_bar_return | 3402 | 58.3% | 0.09 | 0.48 | 1.2% | 41.1% | 0.14 | 89 | 14 | 12 | 0.60 |
| stop_atr_multiple | none | 2268 | 52.8% | 0.06 | 0.61 | 4.9% | 44.6% | -0.11 | 93 | 17 | 7 | 0.69 |
| stop_atr_multiple | 1.0 | 2268 | 47.8% | 0.01 | 0.49 | 2.2% | 72.1% | 0.01 | 162 | 28 | 18 | 1.14 |
| stop_atr_multiple | 2.0 | 2268 | 55.0% | 0.09 | 0.54 | 2.5% | 59.3% | -0.03 | 116 | 21 | 14 | 1.17 |

## Best eligible configs by dev Sharpe (in-sample, before stability/dedup/stress)

| # | timeframe | mean_type | mean_lookback | std_lookback | entry_z | exit_z | max_holding_bars | entry_confirmation | stop_atr_multiple | trades | net ret | Sharpe | maxDD | final stage status |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | 1h | sma | 80 | 80 | -2.0 | 0.0 | 3 | none | none | 115 | 26.5% | 1.16 | -3.0% | s7 pass |
| 2 | 1h | sma | 40 | 80 | -2.0 | -0.5 | 3 | none | 1.0 | 126 | 21.6% | 1.15 | -5.1% | s7 pass |
| 3 | 1h | sma | 80 | 80 | -2.0 | -0.5 | 3 | none | none | 115 | 26.2% | 1.15 | -3.0% | s7 pass |
| 4 | 1h | sma | 40 | 80 | -2.0 | -1.0 | 3 | none | 1.0 | 126 | 21.0% | 1.14 | -5.1% | s6 deduplicated |
| 5 | 1h | sma | 40 | 80 | -2.0 | 0.0 | 3 | none | 1.0 | 126 | 21.1% | 1.13 | -5.1% | s7 pass |
| 6 | 1h | sma | 80 | 80 | -2.0 | -1.0 | 3 | none | none | 115 | 23.7% | 1.10 | -3.0% | s6 deduplicated |
| 7 | 1h | sma | 80 | 12 | -2.5 | -1.0 | 5 | positive_bar_return | 2.0 | 110 | 28.2% | 1.10 | -3.9% | s7 pass |
| 8 | 1h | sma | 80 | 90 | -2.0 | -0.5 | 3 | none | none | 102 | 22.8% | 1.10 | -2.8% | s7 pass |
| 9 | 1h | sma | 80 | 90 | -2.0 | 0.0 | 3 | none | none | 102 | 22.9% | 1.09 | -3.0% | s7 pass |
| 10 | 1h | sma | 34 | 80 | -2.0 | -0.5 | 3 | none | 1.0 | 127 | 18.8% | 1.07 | -5.7% | s6 deduplicated |
| 11 | 1h | sma | 34 | 80 | -2.0 | -1.0 | 3 | none | 1.0 | 127 | 18.5% | 1.06 | -5.7% | s6 deduplicated |
| 12 | 1h | sma | 80 | 12 | -2.5 | 0.0 | 5 | positive_bar_return | 2.0 | 109 | 28.0% | 1.06 | -3.9% | s7 pass |
| 13 | 1h | sma | 80 | 90 | -2.0 | -1.0 | 3 | none | none | 102 | 20.4% | 1.05 | -2.9% | s6 deduplicated |
| 14 | 1h | sma | 34 | 80 | -2.0 | 0.0 | 3 | none | 1.0 | 127 | 17.9% | 1.03 | -5.7% | s6 deduplicated |
| 15 | 1h | sma | 46 | 100 | -2.0 | 0.0 | 3 | none | 1.0 | 108 | 19.0% | 1.01 | -3.2% | s7 pass |

All figures are in-sample development results across a large search; the best rows are expected to look good by chance alone. Out-of-sample evidence comes only from `validate`.
