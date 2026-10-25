# Screening funnel -- mr_es_v5 (development stages only)

- Code: `3b70ca612d69` (dirty working tree: True, diff sha256 `c1dce3a60aeb`)
- Config: `configs/funnel/mr_funnel_es_v5.yaml` sha256 `5a601c732c1fd6e9`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'NQ': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `b7f0e34a2ff627e4` (45 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_es_v3 and mr_es_v4 gated 11 and 18 ES candidates on 2023-2024, and both the v4 stage-4 change and this v5 grid were chosen after reading those results. Also, ES and SPY track the same index, and SPY 2023-2024 gated the mr_v1/mr_v2 (and channel/Donchian) candidates, and this v3 grid was written after those results -- so the slice is not fully independent of earlier research.
- Holdout 2025+ previously inspected: **False** -- No ES strategy metrics have been computed on 2025+. SPY 2025-2026 holdout metrics were inspected in earlier SPY studies, and the futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no strategy selection).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 41472 | 41472 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 41472 | 41472 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 41472 | 29426 | 12046 | 0 |  | 33617 | 70.95 | 70.95 |  |
| 3 performance & risk | hard_gate | 29426 | 88 | 29338 | 0 |  | 0 | 0.21 | 0.30 |  |
| 4 parameter stability | hard_gate | 88 | 80 | 8 | 0 |  | 0 | 0.19 | 90.91 |  |
| 5 time stability | hard_gate | 80 | 80 | 0 | 0 |  | 50 | 0.19 | 100.00 |  |
| 6 deduplication | dedup | 80 | 45 |  |  | 35 |  | 0.11 | 56.25 | best 2 per cluster |
| 7 execution stress | hard_gate | 45 | 45 | 0 | 0 |  | 0 | 0.11 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 45 |  |  |  |  |  |  |  | diagnostic only: unverified: 45 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 12027 |
| s2:hard_reject:years_with_>=10_trades | 8840 |
| s3:hard_reject:max_drawdown | 5352 |
| s3:hard_reject:net_return | 25363 |
| s3:hard_reject:sharpe | 29338 |
| s4:hard_reject:local_median_sharpe | 8 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | NQ dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_b544` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 11/91/23 | 125 | 45.2% | 7.8% | 1.01 | -6.5% | 356 | 1.92 | 7.6% | 59.3 | 10/10 | 0.90 | 0.78 | 0.22 | 5 | 13.1% | 0.64 | 0.57 | 44.6% | 43.0% | 32.3% | 40.7%/29.6% | 18.9 (interpolated) | pass | 0.004 (unverified) | 0.91 |
| 2 | `cfg_8fd9` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 23/79/23 | 125 | 45.0% | 7.7% | 1.01 | -6.2% | 356 | 1.91 | 7.5% | 59.6 | 11/11 | 0.91 | 0.76 | 0.25 | 5 | 12.9% | 0.64 | 0.57 | 44.1% | 43.1% | 33.5% | 41.0%/28.6% | 18.7 (interpolated) | pass | 0.004 (unverified) | 0.88 |
| 3 | `cfg_af41` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 33/141/0 | 174 | 22.5% | 4.2% | 0.91 | -4.4% | 320 | 1.60 | 3.1% | 82.0 | 11/11 | 0.82 | 0.58 | 0.33 | 4 | 13.4% | 0.35 | 0.42 | 20.3% | 18.8% | 20.1% | 20.4%/14.8% | 7.7 (interpolated) | pass | 0.007 (unverified) | 1.00 |
| 4 | `cfg_6385` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 61/113/0 | 174 | 23.4% | 4.3% | 0.91 | -5.0% | 325 | 1.63 | 3.0% | 82.1 | 10/10 | 0.80 | 0.61 | 0.30 | 4 | 14.6% | 0.32 | 0.45 | 21.2% | 19.4% | 17.9% | 18.9%/13.2% | 7.9 (interpolated) | pass | 0.006 (unverified) | 1.09 |
| 5 | `cfg_cbd2` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 30/134/0 | 164 | 32.6% | 5.8% | 1.20 | -2.9% | 158 | 2.02 | 2.9% | 77.5 | 11/11 | 0.82 | 0.64 | 0.56 | 5 | 14.8% | 0.50 | 0.47 | 30.5% | 28.8% | 23.7% | 29.0%/22.9% | 11.5 (interpolated) | pass | 0.015 (unverified) | 0.41 |
| 6 | `cfg_7cd1` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 18/146/0 | 164 | 29.9% | 5.4% | 1.11 | -3.8% | 176 | 1.92 | 2.9% | 77.5 | 11/11 | 0.82 | 0.56 | 0.55 | 4 | 12.8% | 0.53 | 0.48 | 28.3% | 26.5% | 23.6% | 27.2%/22.3% | 10.7 (interpolated) | pass | 0.009 (unverified) | 0.40 |
| 7 | `cfg_605b` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 48/197/0 | 245 | 24.8% | 4.5% | 0.80 | -8.5% | 367 | 1.48 | 4.3% | 115.4 | 10/10 | 0.80 | 0.39 | 0.41 | 4 | 14.8% | 0.38 | 0.62 | 22.5% | 19.6% | 22.7% | 22.6%/15.6% | 6.6 (interpolated) | pass | 0.003 (unverified) | 0.77 |
| 8 | `cfg_f6e0` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 22/32/47 | 101 | 31.4% | 5.6% | 0.91 | -6.0% | 260 | 1.75 | 4.6% | 47.1 | 10/10 | 0.80 | 0.64 | 0.27 | 4 | 12.1% | 0.56 | 0.81 | 30.4% | 29.6% | 16.7% | 29.2%/19.3% | 16.7 (interpolated) | pass | 0.004 (unverified) | 0.77 |
| 9 | `cfg_b913` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 37/207/0 | 244 | 24.7% | 4.5% | 0.80 | -8.2% | 367 | 1.48 | 4.3% | 115.0 | 11/11 | 0.82 | 0.59 | 0.21 | 4 | 14.2% | 0.41 | 0.62 | 22.0% | 18.8% | 24.6% | 22.9%/14.1% | 6.2 (interpolated) | pass | 0.003 (unverified) | 0.72 |
| 10 | `cfg_6248` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 43/5/59 | 107 | 37.8% | 6.6% | 0.99 | -4.9% | 313 | 1.73 | 5.8% | 50.4 | 10/10 | 0.80 | 0.60 | 0.40 | 4 | 15.1% | 0.53 | 0.69 | 36.7% | 35.2% | 22.5% | 34.3%/25.9% | 18.3 (interpolated) | pass | 0.009 (unverified) | 0.71 |
| 11 | `cfg_73ab` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 61/26/43 | 130 | 41.1% | 7.1% | 0.88 | -11.2% | 327 | 1.60 | 10.2% | 61.1 | 11/11 | 0.91 | 0.61 | 0.27 | 4 | 18.7% | 0.46 | 0.58 | 39.8% | 37.9% | 30.0% | 37.0%/27.3% | 16.2 (interpolated) | pass | 0.005 (unverified) | 0.86 |
| 12 | `cfg_5575` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 58/13/39 | 110 | 30.7% | 5.5% | 0.83 | -11.2% | 358 | 1.60 | 8.2% | 50.6 | 9/9 | 0.89 | 0.72 | 0.11 | 4 | 13.4% | 0.53 | 0.54 | 28.6% | 27.8% | 24.1% | 28.6%/21.3% | 15.5 (interpolated) | pass | 0.005 (unverified) | -0.12 |
| 13 | `cfg_76c7` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 49/38/43 | 130 | 42.6% | 7.4% | 0.90 | -11.3% | 327 | 1.61 | 11.0% | 61.1 | 11/11 | 0.91 | 0.68 | 0.22 | 4 | 21.3% | 0.42 | 0.59 | 39.8% | 38.2% | 27.9% | 37.7%/27.4% | 17.3 (interpolated) | pass | 0.006 (unverified) | 0.84 |
| 14 | `cfg_bfd0` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 53/21/44 | 118 | 32.5% | 5.8% | 0.81 | -9.4% | 286 | 1.56 | 9.2% | 54.2 | 9/9 | 0.89 | 0.67 | 0.14 | 4 | 16.0% | 0.49 | 0.60 | 31.2% | 30.2% | 31.4% | 28.3%/21.8% | 14.8 (interpolated) | pass | 0.004 (unverified) | 0.12 |
| 15 | `cfg_e6f5` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 58/8/89 | 155 | 29.5% | 5.3% | 0.86 | -6.0% | 314 | 1.47 | 8.0% | 71.4 | 8/8 | 0.88 | 0.61 | 0.25 | 4 | 14.9% | 0.47 | 0.58 | 26.6% | 25.7% | 16.7% | 26.4%/17.8% | 11.2 (interpolated) | pass | 0.005 (unverified) | 0.05 |
| 16 | `cfg_bed1` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 23/53/25 | 101 | 19.9% | 3.7% | 0.84 | -9.7% | 330 | 1.63 | 5.8% | 46.3 | 9/9 | 0.89 | 0.54 | 0.29 | 4 | 11.2% | 0.41 | 0.63 | 18.9% | 18.3% | 18.9% | 18.6%/13.8% | 11.7 (interpolated) | pass | 0.008 (unverified) | -0.08 |
| 17 | `cfg_cb04` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 37/24/88 | 149 | 28.3% | 5.1% | 0.79 | -6.0% | 235 | 1.45 | 9.0% | 68.8 | 9/9 | 0.89 | 0.63 | 0.16 | 4 | 12.9% | 0.51 | 0.73 | 25.6% | 24.1% | 18.4% | 24.2%/12.9% | 11.0 (interpolated) | pass | 0.003 (unverified) | -0.04 |
| 18 | `cfg_5d8b` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 20/60/23 | 103 | 36.2% | 6.4% | 0.93 | -7.4% | 356 | 1.90 | 6.1% | 48.5 | 10/10 | 0.90 | 0.60 | 0.34 | 4 | 20.0% | 0.45 | 0.54 | 35.0% | 33.4% | 18.5% | 30.0%/22.1% | 18.4 (interpolated) | pass | 0.010 (unverified) | 0.83 |
| 19 | `cfg_2cb1` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 12/71/58 | 141 | 29.8% | 5.4% | 0.82 | -6.3% | 318 | 1.56 | 7.0% | 66.0 | 9/9 | 0.78 | 0.47 | 0.35 | 3 | 14.2% | 0.52 | 0.81 | 28.9% | 27.4% | 27.0% | 26.9%/17.2% | 12.0 (interpolated) | pass | 0.001 (unverified) | 0.95 |
| 20 | `cfg_4f28` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 31/49/23 | 103 | 35.1% | 6.2% | 0.91 | -7.4% | 356 | 1.87 | 6.0% | 48.8 | 9/9 | 0.89 | 0.59 | 0.32 | 4 | 19.1% | 0.46 | 0.55 | 34.3% | 32.7% | 18.5% | 30.9%/22.5% | 18.1 (interpolated) | pass | 0.009 (unverified) | 0.76 |
| 21 | `cfg_4d49` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 21/62/58 | 141 | 30.2% | 5.4% | 0.84 | -5.8% | 318 | 1.56 | 6.8% | 66.2 | 10/10 | 0.80 | 0.57 | 0.26 | 4 | 15.5% | 0.49 | 0.81 | 28.0% | 27.5% | 27.6% | 27.3%/18.3% | 12.0 (interpolated) | pass | 0.002 (unverified) | 0.91 |
| 22 | `cfg_b545` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 31/40/77 | 148 | 18.7% | 3.5% | 0.77 | -8.5% | 330 | 1.42 | 6.3% | 67.6 | 8/8 | 0.88 | 0.54 | 0.23 | 4 | 8.7% | 0.51 | 0.69 | 17.3% | 15.4% | 12.8% | 17.3%/10.5% | 7.9 (interpolated) | pass | 0.003 (unverified) | -0.15 |
| 23 | `cfg_b484` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 72/40/0 | 112 | 44.7% | 7.7% | 0.94 | -10.3% | 197 | 1.85 | 10.9% | 52.6 | 10/10 | 0.80 | 0.45 | 0.49 | 5 | 24.4% | 0.42 | 0.48 | 42.6% | 42.0% | 31.9% | 40.4%/32.1% | 20.2 (interpolated) | pass | 0.007 (unverified) | 0.19 |
| 24 | `cfg_5378` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 56/25/66 | 147 | 21.7% | 4.0% | 0.77 | -5.1% | 312 | 1.42 | 6.2% | 68.5 | 8/8 | 0.75 | 0.52 | 0.25 | 4 | 10.6% | 0.48 | 0.67 | 19.0% | 17.5% | 8.8% | 18.5%/13.1% | 8.6 (interpolated) | pass | 0.002 (unverified) | 0.83 |
| 25 | `cfg_d0dd` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 20/74/25 | 119 | 39.5% | 6.9% | 0.80 | -11.5% | 286 | 1.73 | 7.2% | 56.3 | 9/9 | 0.89 | 0.57 | 0.23 | 4 | 19.8% | 0.50 | 0.59 | 38.1% | 37.0% | 24.8% | 31.8%/25.0% | 17.6 (interpolated) | pass | 0.002 (unverified) | 0.79 |
| 26 | `cfg_9dd2` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 29/268/0 | 297 | 30.3% | 5.4% | 0.91 | -5.7% | 344 | 1.49 | 5.3% | 139.8 | 11/11 | 0.73 | 0.46 | 0.45 | 4 | 17.1% | 0.38 | 0.56 | 27.2% | 23.5% | 24.2% | 28.8%/22.3% | 6.2 (interpolated) | pass | 0.004 (unverified) | 0.50 |
| 27 | `cfg_3104` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=25, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 23/95/0 | 118 | 20.8% | 3.8% | 0.77 | -4.5% | 199 | 1.71 | 2.1% | 55.7 | 10/10 | 0.80 | 0.54 | 0.24 | 4 | 5.4% | 0.73 | 0.82 | 19.6% | 18.5% | 12.5% | 19.7%/15.1% | 10.6 (interpolated) | pass | 0.001 (unverified) | 0.02 |
| 28 | `cfg_1c9b` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 11/72/51 | 134 | 41.8% | 7.2% | 0.78 | -11.3% | 263 | 1.52 | 12.6% | 61.7 | 10/10 | 0.90 | 0.51 | 0.27 | 4 | 22.8% | 0.39 | 0.60 | 39.3% | 37.9% | 49.0% | 36.0%/23.9% | 15.0 (interpolated) | pass | 0.003 (unverified) | 0.10 |
| 29 | `cfg_6849` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 2/100/26 | 128 | 26.8% | 4.9% | 0.76 | -7.1% | 317 | 1.49 | 7.9% | 59.9 | 10/10 | 0.90 | 0.48 | 0.28 | 4 | 9.8% | 0.59 | 0.66 | 25.3% | 24.0% | 8.6% | 27.1%/18.9% | 11.9 (interpolated) | pass | 0.001 (unverified) | -0.14 |
| 30 | `cfg_809b` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=40, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 78/50/0 | 128 | 37.7% | 6.6% | 0.81 | -11.1% | 163 | 1.54 | 12.3% | 60.4 | 9/9 | 0.78 | 0.39 | 0.42 | 4 | 16.8% | 0.58 | 0.65 | 35.3% | 33.7% | 38.5% | 34.5%/26.5% | 16.1 (interpolated) | pass | 0.003 (unverified) | 0.44 |
| 31 | `cfg_22a9` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 44/254/0 | 298 | 30.1% | 5.4% | 0.91 | -5.6% | 344 | 1.48 | 5.3% | 140.3 | 12/12 | 0.75 | 0.47 | 0.43 | 4 | 16.9% | 0.39 | 0.56 | 27.0% | 23.3% | 23.4% | 27.4%/20.7% | 6.2 (interpolated) | pass | 0.004 (unverified) | 0.50 |
| 32 | `cfg_313f` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 82/197/0 | 279 | 42.7% | 7.4% | 0.86 | -13.8% | 249 | 1.42 | 8.6% | 129.4 | 11/11 | 0.82 | 0.35 | 0.51 | 4 | 17.8% | 0.56 | 0.65 | 40.2% | 38.4% | 28.2% | 39.5%/27.9% | 8.3 (interpolated) | pass | 0.005 (unverified) | 0.18 |
| 33 | `cfg_a53b` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 4/104/0 | 108 | 31.1% | 5.6% | 0.81 | -6.8% | 308 | 1.82 | 7.3% | 50.6 | 8/8 | 0.62 | 0.61 | 0.20 | 4 | 17.6% | 0.43 | 0.59 | 30.2% | 29.1% | 37.9% | 28.4%/21.2% | 16.0 (interpolated) | pass | 0.003 (unverified) | 0.11 |
| 34 | `cfg_e811` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 1/107/0 | 108 | 31.3% | 5.6% | 0.81 | -6.8% | 308 | 1.83 | 7.4% | 50.5 | 7/7 | 0.57 | 0.55 | 0.26 | 4 | 17.7% | 0.43 | 0.58 | 30.2% | 29.2% | 38.7% | 27.9%/21.0% | 16.3 (interpolated) | pass | 0.003 (unverified) | 0.12 |
| 35 | `cfg_3e84` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 16/88/27 | 131 | 27.0% | 4.9% | 0.77 | -7.6% | 317 | 1.48 | 7.9% | 61.2 | 11/11 | 0.91 | 0.53 | 0.23 | 4 | 8.2% | 0.66 | 0.67 | 25.9% | 24.0% | 13.9% | 26.8%/17.9% | 11.9 (interpolated) | pass | 0.001 (unverified) | -0.01 |
| 36 | `cfg_c538` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 136/125/0 | 261 | 19.0% | 3.5% | 0.75 | -6.4% | 378 | 1.43 | 4.1% | 121.5 | 10/10 | 0.90 | 0.33 | 0.43 | 4 | 8.1% | 0.54 | 0.50 | 15.7% | 12.8% | 16.2% | 16.3%/11.7% | 4.9 (interpolated) | pass | 0.002 (unverified) | 0.12 |
| 37 | `cfg_3845` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 55/44/30 | 129 | 26.5% | 4.8% | 0.78 | -7.3% | 464 | 1.54 | 7.0% | 60.8 | 9/9 | 0.89 | 0.63 | 0.14 | 4 | 9.0% | 0.61 | 0.53 | 25.0% | 23.5% | 15.6% | 24.7%/19.1% | 11.7 (interpolated) | pass | 0.002 (unverified) | 0.59 |
| 38 | `cfg_3a2c` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=25, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 6/111/0 | 117 | 19.9% | 3.7% | 0.75 | -5.4% | 307 | 1.66 | 2.1% | 55.3 | 10/10 | 0.80 | 0.52 | 0.23 | 4 | 5.4% | 0.73 | 0.87 | 18.8% | 17.6% | 11.2% | 18.6%/12.9% | 10.5 (interpolated) | pass | 0.001 (unverified) | -0.09 |
| 39 | `cfg_103b` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 104/177/0 | 281 | 40.3% | 7.0% | 0.83 | -13.1% | 249 | 1.40 | 8.3% | 131.2 | 12/12 | 0.75 | 0.31 | 0.52 | 4 | 20.3% | 0.47 | 0.62 | 38.3% | 31.3% | 26.0% | 34.1%/27.4% | 7.8 (interpolated) | pass | 0.005 (unverified) | 0.11 |
| 40 | `cfg_5249` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 23/61/50 | 134 | 39.9% | 7.0% | 0.76 | -11.2% | 245 | 1.51 | 12.3% | 61.6 | 11/11 | 0.91 | 0.52 | 0.24 | 4 | 21.3% | 0.41 | 0.63 | 36.6% | 34.8% | 45.9% | 32.4%/21.7% | 14.8 (interpolated) | pass | 0.003 (unverified) | 0.09 |
| 41 | `cfg_a41f` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 33/224/0 | 257 | 24.5% | 4.5% | 0.91 | -7.0% | 330 | 1.48 | 4.6% | 119.8 | 10/10 | 0.90 | 0.51 | 0.40 | 4 | 12.6% | 0.45 | 0.43 | 21.6% | 18.1% | 22.7% | 21.3%/14.7% | 5.9 (interpolated) | pass | 0.007 (unverified) | 0.16 |
| 42 | `cfg_2edc` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 39/42/36 | 117 | 34.5% | 6.1% | 0.77 | -14.9% | 590 | 1.52 | 10.2% | 55.7 | 11/11 | 0.91 | 0.55 | 0.23 | 4 | 15.9% | 0.49 | 0.63 | 33.3% | 32.6% | 27.9% | 31.2%/21.8% | 16.0 (interpolated) | pass | 0.002 (unverified) | 0.54 |
| 43 | `cfg_6238` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 32/72/27 | 131 | 25.3% | 4.6% | 0.79 | -5.4% | 172 | 1.48 | 7.7% | 61.7 | 8/8 | 0.75 | 0.47 | 0.32 | 5 | 13.6% | 0.43 | 0.61 | 23.9% | 23.0% | 22.6% | 22.4%/16.8% | 11.2 (interpolated) | pass | 0.003 (unverified) | -0.06 |
| 44 | `cfg_8dce` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 17/90/0 | 107 | 45.0% | 7.7% | 0.87 | -9.9% | 163 | 1.82 | 12.9% | 50.5 | 10/10 | 0.90 | 0.42 | 0.45 | 5 | 24.6% | 0.42 | 0.56 | 45.3% | 43.8% | 24.4% | 38.5%/29.1% | 21.6 (interpolated) | pass | 0.003 (unverified) | 0.05 |
| 45 | `cfg_6b22` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 53/18/103 | 174 | 26.5% | 4.8% | 0.81 | -4.4% | 273 | 1.36 | 10.0% | 81.2 | 10/10 | 0.70 | 0.27 | 0.53 | 5 | 16.3% | 0.38 | 0.84 | 23.7% | 21.9% | 25.4% | 21.3%/14.8% | 8.8 (interpolated) | pass | 0.004 (unverified) | -0.04 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 0.6% / 0.13 / 35 | 0.5% / 0.17 / 14 | 28.4% / 2.00 / 19 | 3.4% / 0.98 / 21 | 8.1% / 0.98 / 36 |
| 2 | 1.0% / 0.20 / 35 | 0.5% / 0.18 / 14 | 28.4% / 2.02 / 19 | 3.6% / 1.00 / 21 | 7.3% / 0.90 / 36 |
| 3 | -2.4% / -0.55 / 32 | 8.1% / 2.60 / 36 | 5.8% / 0.79 / 39 | 6.6% / 2.30 / 19 | 3.0% / 0.79 / 48 |
| 4 | -3.1% / -0.75 / 32 | 7.7% / 2.46 / 36 | 7.0% / 0.88 / 39 | 6.5% / 2.25 / 19 | 3.9% / 0.97 / 48 |
| 5 | 0.2% / 0.06 / 30 | 4.4% / 2.09 / 26 | 15.5% / 1.80 / 33 | 4.4% / 1.64 / 17 | 5.2% / 1.23 / 58 |
| 6 | -0.1% / 0.01 / 30 | 4.4% / 2.10 / 26 | 15.2% / 1.77 / 33 | 4.2% / 1.59 / 17 | 3.8% / 0.88 / 58 |
| 7 | -3.7% / -0.71 / 55 | 3.6% / 1.19 / 41 | 9.0% / 0.96 / 51 | 8.8% / 2.95 / 33 | 5.5% / 0.97 / 65 |
| 8 | 5.0% / 0.90 / 32 | -2.8% / -2.12 / 9 | 17.2% / 1.56 / 14 | 3.3% / 1.35 / 17 | 6.4% / 0.98 / 29 |
| 9 | -3.0% / -0.58 / 54 | 3.5% / 1.16 / 41 | 8.7% / 0.94 / 51 | 9.2% / 3.00 / 33 | 4.6% / 0.82 / 65 |
| 10 | 3.8% / 0.63 / 33 | -2.6% / -1.85 / 9 | 19.7% / 1.71 / 16 | 6.3% / 2.00 / 18 | 7.1% / 0.96 / 31 |
| 11 | -1.3% / -0.12 / 39 | 1.5% / 0.48 / 15 | 18.9% / 1.39 / 21 | 8.8% / 1.99 / 21 | 8.9% / 1.08 / 34 |
| 12 | 6.1% / 0.73 / 32 | -1.2% / -0.30 / 17 | 2.4% / 0.33 / 17 | 15.3% / 2.82 / 25 | 5.8% / 0.86 / 19 |
| 13 | -1.0% / -0.07 / 39 | 2.1% / 0.67 / 15 | 17.5% / 1.32 / 21 | 9.5% / 1.98 / 21 | 9.5% / 1.09 / 34 |
| 14 | 7.4% / 0.78 / 35 | -1.4% / -0.32 / 22 | 5.1% / 0.64 / 16 | 14.3% / 2.55 / 24 | 4.1% / 0.60 / 21 |
| 15 | 6.2% / 0.90 / 44 | -0.0% / 0.01 / 20 | 2.9% / 0.41 / 22 | 12.7% / 2.51 / 42 | 5.2% / 0.76 / 27 |
| 16 | -1.9% / -0.23 / 31 | 2.1% / 1.13 / 15 | 3.6% / 1.02 / 14 | 7.8% / 2.01 / 25 | 7.1% / 1.62 / 16 |
| 17 | 4.1% / 0.58 / 44 | 2.3% / 0.57 / 20 | -1.1% / -0.11 / 18 | 13.6% / 2.34 / 40 | 7.2% / 0.97 / 27 |
| 18 | -2.3% / -0.32 / 29 | 3.6% / 1.22 / 15 | 13.7% / 1.15 / 20 | 4.3% / 2.03 / 6 | 13.5% / 1.98 / 33 |
| 19 | -0.2% / -0.01 / 39 | -0.4% / -0.15 / 19 | 12.2% / 1.15 / 22 | 2.4% / 0.84 / 22 | 13.6% / 1.66 / 39 |
| 20 | -2.3% / -0.32 / 29 | 3.8% / 1.29 / 15 | 12.5% / 1.07 / 20 | 4.4% / 2.03 / 6 | 13.5% / 1.97 / 33 |
| 21 | 0.2% / 0.07 / 39 | -0.5% / -0.18 / 19 | 12.4% / 1.18 / 22 | 3.0% / 1.01 / 22 | 12.8% / 1.60 / 39 |
| 22 | -1.1% / -0.16 / 44 | 2.7% / 1.47 / 18 | 2.1% / 0.45 / 21 | 9.3% / 2.21 / 41 | 4.7% / 0.90 / 24 |
| 23 | 7.3% / 0.91 / 25 | 1.6% / 0.42 / 17 | 5.8% / 0.49 / 18 | 16.3% / 3.40 / 25 | 7.9% / 1.01 / 27 |
| 24 | -0.7% / -0.10 / 38 | 4.4% / 1.71 / 25 | 10.0% / 1.63 / 22 | 0.6% / 0.26 / 16 | 6.1% / 0.77 / 46 |
| 25 | -0.9% / -0.08 / 36 | 2.6% / 0.96 / 13 | 14.1% / 0.89 / 23 | 3.2% / 1.03 / 11 | 16.4% / 2.00 / 36 |
| 26 | -2.0% / -0.36 / 69 | 5.0% / 1.54 / 53 | 11.3% / 1.11 / 55 | 7.4% / 2.09 / 39 | 6.1% / 1.13 / 81 |
| 27 | 3.9% / 1.44 / 18 | 0.8% / 0.31 / 18 | 14.5% / 1.49 / 28 | 2.8% / 1.42 / 11 | -2.1% / -0.46 / 43 |
| 28 | -0.2% / 0.04 / 43 | 5.0% / 1.15 / 18 | 15.5% / 1.02 / 23 | 5.9% / 1.40 / 13 | 10.6% / 1.22 / 37 |
| 29 | 4.2% / 0.60 / 40 | -2.4% / -0.77 / 15 | 15.5% / 1.55 / 19 | 5.6% / 1.56 / 18 | 2.1% / 0.35 / 36 |
| 30 | 6.5% / 0.87 / 30 | 3.7% / 0.94 / 20 | 11.3% / 0.93 / 22 | 18.0% / 2.90 / 29 | -4.9% / -0.49 / 27 |
| 31 | -2.0% / -0.34 / 70 | 4.9% / 1.52 / 53 | 11.4% / 1.11 / 55 | 7.2% / 2.10 / 39 | 6.1% / 1.13 / 81 |
| 32 | 4.9% / 0.77 / 65 | 8.4% / 2.14 / 52 | 21.1% / 1.33 / 53 | 11.9% / 2.74 / 38 | -7.5% / -0.89 / 71 |
| 33 | -0.1% / 0.01 / 23 | 0.5% / 0.19 / 16 | 10.4% / 0.89 / 17 | 6.1% / 1.32 / 23 | 11.5% / 1.70 / 29 |
| 34 | -0.1% / 0.01 / 23 | 0.5% / 0.19 / 16 | 10.6% / 0.90 / 17 | 6.0% / 1.31 / 23 | 11.5% / 1.70 / 29 |
| 35 | 4.2% / 0.60 / 40 | -2.3% / -0.75 / 15 | 17.4% / 1.75 / 19 | 4.6% / 1.24 / 21 | 1.5% / 0.26 / 36 |
| 36 | -2.5% / -0.56 / 53 | 4.7% / 1.87 / 50 | 10.1% / 1.30 / 47 | 5.3% / 1.94 / 39 | 0.7% / 0.16 / 72 |
| 37 | -4.7% / -0.74 / 32 | 5.4% / 1.94 / 21 | 16.0% / 1.79 / 21 | 1.6% / 0.51 / 16 | 6.8% / 0.84 / 39 |
| 38 | 3.9% / 1.44 / 18 | 1.1% / 0.41 / 18 | 13.7% / 1.45 / 28 | 3.5% / 1.54 / 11 | -3.1% / -0.68 / 42 |
| 39 | 5.6% / 0.87 / 66 | 8.1% / 2.08 / 52 | 16.6% / 1.10 / 54 | 11.8% / 2.73 / 38 | -5.7% / -0.67 / 71 |
| 40 | -0.5% / 0.01 / 43 | 6.0% / 1.40 / 18 | 15.4% / 1.01 / 23 | 5.4% / 1.32 / 13 | 9.0% / 1.15 / 37 |
| 41 | -1.1% / -0.22 / 53 | 5.4% / 1.81 / 48 | 10.6% / 1.38 / 47 | 5.7% / 1.63 / 38 | 2.2% / 0.44 / 71 |
| 42 | 6.6% / 0.80 / 32 | -3.5% / -0.91 / 13 | 2.8% / 0.30 / 18 | 16.1% / 2.81 / 20 | 9.6% / 1.01 / 34 |
| 43 | 4.7% / 0.73 / 37 | 1.4% / 0.36 / 21 | 10.3% / 1.41 / 18 | 5.5% / 1.44 / 18 | 1.6% / 0.25 / 37 |
| 44 | 5.6% / 0.62 / 24 | 2.5% / 0.62 / 17 | 5.9% / 0.48 / 17 | 16.4% / 2.75 / 22 | 8.7% / 1.02 / 27 |
| 45 | 4.4% / 0.74 / 45 | 2.9% / 0.78 / 23 | 7.0% / 0.84 / 29 | 8.7% / 2.14 / 35 | 1.2% / 0.21 / 42 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_cbd2` | 12 | 0.87 | 0.85/0.91 | 0.80/0.86 |
| 1 | `cfg_605b` | 4 | 0.99 | 0.99/0.99 | 0.96/0.96 |
| 2 | `cfg_c538` | 3 | 0.92 | 0.92/0.93 | 0.81/0.81 |
| 3 | `cfg_313f` | 3 | 0.97 | 0.97/0.98 | 0.91/0.94 |
| 4 | `cfg_73ab` | 3 | 0.92 | 0.96/0.98 | 0.90/0.93 |
| 5 | `cfg_1c9b` | 2 | 0.96 | 0.99/0.99 | 0.98/0.98 |
| 6 | `cfg_9dd2` | 4 | 0.99 | 0.99/1.00 | 0.93/0.95 |
| 7 | `cfg_2cb1` | 3 | 0.99 | 0.99/0.99 | 0.95/0.95 |
| 8 | `cfg_2edc` | 1 | n/a | n/a/n/a | n/a/n/a |
| 9 | `cfg_3104` | 3 | 0.86 | 0.70/0.85 | 0.47/0.73 |
| 10 | `cfg_3845` | 1 | n/a | n/a/n/a | n/a/n/a |
| 11 | `cfg_6849` | 3 | 0.99 | 0.99/0.99 | 0.95/0.98 |
| 12 | `cfg_f6e0` | 7 | 0.82 | 0.80/0.95 | 0.74/0.86 |
| 13 | `cfg_5d8b` | 4 | 0.93 | 0.97/0.98 | 0.96/0.96 |
| 14 | `cfg_5378` | 1 | n/a | n/a/n/a | n/a/n/a |
| 15 | `cfg_5575` | 2 | 0.95 | 0.92/0.92 | 0.78/0.78 |
| 16 | `cfg_6238` | 1 | n/a | n/a/n/a | n/a/n/a |
| 17 | `cfg_af41` | 4 | 0.97 | 0.99/0.99 | 0.96/0.97 |
| 18 | `cfg_a53b` | 6 | 0.85 | 0.84/0.84 | 0.54/0.55 |
| 19 | `cfg_6b22` | 1 | n/a | n/a/n/a | n/a/n/a |
| 20 | `cfg_809b` | 1 | n/a | n/a/n/a | n/a/n/a |
| 21 | `cfg_b484` | 2 | 0.91 | 0.93/0.93 | 0.77/0.77 |
| 22 | `cfg_b544` | 4 | 0.95 | 0.94/0.95 | 0.82/0.83 |
| 23 | `cfg_bed1` | 2 | 0.91 | 0.83/0.83 | 0.61/0.61 |
| 24 | `cfg_e6f5` | 2 | 0.86 | 0.92/0.92 | 0.82/0.82 |
| 25 | `cfg_d0dd` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.472e-03 over 41040 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1181.0, participation ratio 21.4, 95%-variance components 273 (rank bound T = 1259); raw grid 41472; raw + known prior 431016
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
NQ results are unchanged rules on the development period: supporting evidence, not an independent replication.

## Integrity audit

- z = (close - mean) / std with mean = SMA/EMA of the last N closes and std = rolling sample std of the last M closes (bars of the config's timeframe), both INCLUDING the signal bar's close; the signal is decided at that close and the entry fills at the NEXT bar's open.
- Exits are decided at a close on or after the entry bar (z >= exit_z, or held max_hold bars) and fill at the next bar's open, so a time exit fills exactly max_hold bars after entry.
- Trend filter compares the signal bar's close to the SMA(100/150/200 bars) of closes up to that bar; warm-up bars (SMA undefined) never signal.
- No profit target exists. v1 has no stop; v2's optional ATR stop is entry fill - k x ATR(14) using the ATR known before the fill, live from the entry bar, filled at the worse of open and stop. Sizing (v1 and v2): as many whole shares as current equity affords (no leverage).
- v2 only: the z-score std uses the same window as the mean; positive_bar_return requires the signal bar's close above the previous close; cooldown_bars = N requires the next signal bar to be >= N bars after the previous exit.
- After a time exit the setup re-arms only once z closes above entry_z, so the holding cap cannot be undone by an immediate re-entry.
- Missed-entry stress skips a whole signal episode (contiguous signal bars), never re-entering one bar later.
- Adverse slippage + commission on every fill; a fill at a session's first bar bears the full overnight gap.
- Development backtests run on data physically truncated at the development end; open positions are force-closed at the last development bar and flagged (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Positions are held overnight (no session-end flattening), as in the channel family; rolling windows run continuously across sessions over RTH bars only.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC; the 1-minute step there is taken as the roll spread). Point moves are preserved; pre-roll price levels are not real traded prices.
- Session: NYSE regular session only (09:30-16:00 NY, NYSE early closes/holidays), matching the SPY studies; overnight Globex bars are not traded or used in indicators.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side (stops too) plus commission per contract per side, from the execution YAML; cost stress scales both.
- Positions that straddle a roll are treated as if rolled for free at the adjusted spread (no extra roll commission/slippage).

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Whole-contract granularity: at ~$1M equity the position is a handful of ES contracts, so position size steps with price; results are sensitive to starting equity at small sizes.
- All lookbacks and holding periods are counted in bars of the config's timeframe (RTH bars only), not in trading days.
- entry_confirmation = positive_bar_return means the signal bar closed above the previous bar's close (the 'directional bar' option).
