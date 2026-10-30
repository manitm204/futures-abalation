# Screening funnel -- mr_rty_v6 (development stages only)

- Code: `5342a94cdc84` (dirty working tree: True, diff sha256 `8c4bf865eb35`)
- Config: `configs/funnel/mr_funnel_rty_v6.yaml` sha256 `19079a94cf5daf90`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'RTY': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `f9ff35ff3ac74eb4` (108 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_rty_v5 gated 27 RTY candidates on 2023-2024 (5 passed) and this grid was written after reading those results, so RTY 2023-2024 is partly in-sample here. The stage-4 test and 40-trade rule were also shaped by ES 2023-2024.
- Holdout 2025+ previously inspected: **False** -- No RTY strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection). The holdout is the only untouched test for this run.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 84672 | 84672 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 84672 | 84672 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 84672 | 29283 | 55389 | 0 |  | 48584 | 34.58 | 34.58 |  |
| 3 performance & risk | hard_gate | 29283 | 477 | 28806 | 0 |  | 0 | 0.56 | 1.63 |  |
| 4 parameter stability | hard_gate | 477 | 433 | 44 | 0 |  | 0 | 0.51 | 90.78 |  |
| 5 time stability | hard_gate | 433 | 410 | 23 | 0 |  | 415 | 0.48 | 94.69 |  |
| 6 deduplication | dedup | 410 | 108 |  |  | 302 |  | 0.13 | 26.34 | best 2 per cluster |
| 7 execution stress | hard_gate | 108 | 108 | 0 | 0 |  | 20 | 0.13 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 108 |  |  |  |  |  |  |  | diagnostic only: unverified: 108 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 55389 |
| s2:hard_reject:years_with_>=10_trades | 47923 |
| s3:hard_reject:max_drawdown | 3376 |
| s3:hard_reject:net_return | 19325 |
| s3:hard_reject:sharpe | 28806 |
| s4:hard_reject:local_median_sharpe | 44 |
| s5:hard_reject:profitable_years | 23 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_5087` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=60, entry_z=-3.0, exit_z=-1.25, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.0 | 8/110/13 | 131 | 19.0% | 3.6% | 1.21 | -3.5% | 415 | 1.84 | 1.5% | 59.7 | 11/11 | 0.82 | 0.87 | 0.33 | 3 | 8.8% | 0.54 | 0.51 | 17.7% | 16.2% | 10.1% | 17.2%/13.8% | 9.0 (interpolated) | pass | 0.282 (unverified) | -0.32 |
| 2 | `cfg_fece` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=60, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.0 | 3/115/13 | 131 | 19.0% | 3.6% | 1.21 | -3.5% | 415 | 1.84 | 1.5% | 59.7 | 12/12 | 0.83 | 0.87 | 0.34 | 3 | 8.8% | 0.54 | 0.51 | 17.7% | 16.2% | 10.6% | 17.0%/14.0% | 9.0 (interpolated) | pass | 0.282 (unverified) | -0.33 |
| 3 | `cfg_9583` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=80, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 2/114/0 | 116 | 16.7% | 3.1% | 1.09 | -4.6% | 380 | 1.77 | 1.4% | 52.3 | 10/10 | 1.00 | 0.96 | 0.13 | 3 | 9.4% | 0.44 | 0.51 | 15.6% | 14.4% | 9.7% | 15.3%/13.0% | 8.8 (interpolated) | pass | 0.219 (unverified) | 0.20 |
| 4 | `cfg_4311` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=80, entry_z=-3.0, exit_z=-1.25, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 3/113/0 | 116 | 16.7% | 3.1% | 1.09 | -4.6% | 380 | 1.77 | 1.4% | 52.3 | 9/9 | 1.00 | 0.91 | 0.17 | 3 | 9.4% | 0.44 | 0.51 | 15.6% | 14.4% | 9.7% | 15.2%/12.9% | 8.8 (interpolated) | pass | 0.219 (unverified) | 0.16 |
| 5 | `cfg_5936` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=80, entry_z=-2.5, exit_z=-1.25, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 17/83/0 | 100 | 13.2% | 2.5% | 1.00 | -2.4% | 324 | 1.80 | 1.2% | 45.4 | 9/9 | 1.00 | 0.88 | 0.12 | 3 | 6.2% | 0.50 | 0.56 | 12.5% | 11.5% | 2.5% | 12.4%/10.1% | 8.3 (interpolated) | pass | 0.163 (unverified) | -0.21 |
| 6 | `cfg_405b` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=80, entry_z=-2.5, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 2/98/0 | 100 | 12.5% | 2.4% | 0.96 | -3.1% | 324 | 1.75 | 1.2% | 45.5 | 10/10 | 1.00 | 0.90 | 0.06 | 4 | 6.1% | 0.52 | 0.59 | 11.9% | 11.0% | 1.8% | 12.2%/9.4% | 8.0 (interpolated) | pass | 0.142 (unverified) | -0.20 |
| 7 | `cfg_4471` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=80, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 2/101/0 | 103 | 15.4% | 2.9% | 1.09 | -3.5% | 324 | 1.82 | 1.3% | 46.6 | 11/11 | 0.91 | 0.80 | 0.29 | 3 | 6.4% | 0.60 | 0.48 | 14.6% | 13.6% | 6.5% | 14.3%/11.8% | 9.4 (interpolated) | pass | 0.213 (unverified) | -0.11 |
| 8 | `cfg_f9e1` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=80, entry_z=-3.0, exit_z=-1.25, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 3/100/0 | 103 | 15.4% | 2.9% | 1.09 | -3.5% | 324 | 1.82 | 1.3% | 46.6 | 10/10 | 0.90 | 0.78 | 0.32 | 3 | 6.4% | 0.60 | 0.48 | 14.6% | 13.6% | 6.4% | 14.5%/11.8% | 9.4 (interpolated) | pass | 0.213 (unverified) | -0.10 |
| 9 | `cfg_8b81` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=60, entry_z=-3.0, exit_z=-1.25, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 9/101/60 | 170 | 18.9% | 3.5% | 1.19 | -3.4% | 325 | 1.60 | 1.6% | 76.8 | 10/10 | 0.80 | 0.65 | 0.54 | 4 | 7.2% | 0.61 | 0.52 | 17.5% | 15.8% | 2.2% | 16.6%/12.9% | 7.3 (interpolated) | pass | 0.272 (unverified) | -0.47 |
| 10 | `cfg_6a6f` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=100, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 36/102/42 | 180 | 26.8% | 4.9% | 1.10 | -5.3% | 515 | 1.54 | 4.1% | 80.7 | 11/11 | 1.00 | 0.71 | 0.39 | 4 | 9.7% | 0.61 | 0.53 | 25.2% | 23.3% | 7.5% | 23.0%/18.2% | 8.9 (interpolated) | pass | 0.224 (unverified) | -0.04 |
| 11 | `cfg_87e7` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=60, entry_z=-3.0, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 1/109/60 | 170 | 19.1% | 3.6% | 1.20 | -3.4% | 325 | 1.60 | 1.6% | 76.7 | 11/11 | 0.82 | 0.73 | 0.46 | 4 | 7.5% | 0.60 | 0.52 | 17.7% | 16.1% | 2.2% | 16.6%/12.6% | 7.3 (interpolated) | pass | 0.281 (unverified) | -0.47 |
| 12 | `cfg_98a3` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=60, entry_z=-3.0, exit_z=-1.25, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 7/99/0 | 106 | 12.8% | 2.4% | 0.90 | -3.5% | 415 | 1.75 | 1.3% | 48.0 | 10/10 | 1.00 | 0.87 | 0.03 | 5 | 6.9% | 0.44 | 0.73 | 12.0% | 11.2% | 7.5% | 12.1%/9.3% | 7.9 (interpolated) | pass | 0.095 (unverified) | -0.37 |
| 13 | `cfg_076f` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=100, entry_z=-2.5, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 3/97/0 | 100 | 12.3% | 2.3% | 0.93 | -4.0% | 318 | 1.67 | 1.2% | 45.0 | 10/10 | 1.00 | 0.68 | 0.26 | 3 | 5.1% | 0.61 | 0.67 | 11.3% | 10.3% | 2.2% | 11.0%/8.4% | 7.7 (interpolated) | pass | 0.135 (unverified) | -0.18 |
| 14 | `cfg_cac3` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 4/118/0 | 122 | 15.3% | 2.9% | 0.87 | -4.1% | 347 | 1.61 | 2.2% | 55.0 | 12/12 | 0.83 | 0.77 | 0.10 | 3 | 7.3% | 0.50 | 0.65 | 14.5% | 13.3% | 5.4% | 14.5%/10.8% | 8.0 (interpolated) | pass | 0.094 (unverified) | 0.01 |
| 15 | `cfg_8a17` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-3.0, exit_z=-1.25, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 9/113/0 | 122 | 15.2% | 2.9% | 0.87 | -4.1% | 347 | 1.61 | 2.2% | 55.0 | 11/11 | 0.82 | 0.75 | 0.12 | 3 | 7.2% | 0.51 | 0.66 | 14.2% | 13.1% | 5.4% | 14.6%/12.0% | 7.9 (interpolated) | pass | 0.092 (unverified) | -0.02 |
| 16 | `cfg_450a` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=60, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 3/103/0 | 106 | 11.9% | 2.3% | 0.86 | -3.5% | 415 | 1.70 | 1.3% | 48.0 | 11/11 | 1.00 | 0.87 | -0.01 | 4 | 6.1% | 0.47 | 0.77 | 11.1% | 10.3% | 7.1% | 11.4%/8.6% | 7.5 (interpolated) | pass | 0.081 (unverified) | -0.39 |
| 17 | `cfg_2f2b` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=100, entry_z=-2.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 1/99/0 | 100 | 12.2% | 2.3% | 0.93 | -4.0% | 318 | 1.67 | 1.2% | 45.0 | 10/10 | 1.00 | 0.69 | 0.24 | 3 | 5.1% | 0.60 | 0.68 | 11.2% | 10.2% | 1.9% | 10.9%/7.7% | 7.7 (interpolated) | pass | 0.133 (unverified) | -0.18 |
| 18 | `cfg_1ecb` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=80, entry_z=-3.0, exit_z=-1.25, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 3/105/67 | 175 | 12.5% | 2.4% | 0.84 | -3.8% | 380 | 1.35 | 1.6% | 79.2 | 9/9 | 1.00 | 0.68 | 0.16 | 4 | 4.5% | 0.64 | 0.79 | 11.1% | 9.2% | 1.4% | 9.7%/6.0% | 5.1 (interpolated) | pass | 0.091 (unverified) | 0.44 |
| 19 | `cfg_e19a` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=60, entry_z=-2.5, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 5/125/0 | 130 | 11.7% | 2.2% | 0.94 | -3.4% | 379 | 1.61 | 1.6% | 59.0 | 10/10 | 0.90 | 0.86 | 0.09 | 4 | 4.5% | 0.59 | 0.61 | 10.4% | 9.3% | 4.4% | 10.4%/7.4% | 6.0 (interpolated) | pass | 0.125 (unverified) | -0.62 |
| 20 | `cfg_140b` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=80, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 2/106/67 | 175 | 12.5% | 2.4% | 0.84 | -3.8% | 380 | 1.35 | 1.6% | 79.2 | 10/10 | 1.00 | 0.76 | 0.08 | 4 | 4.5% | 0.64 | 0.79 | 11.1% | 9.2% | 1.4% | 10.5%/6.7% | 5.1 (interpolated) | pass | 0.091 (unverified) | 0.47 |
| 21 | `cfg_a48b` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=60, entry_z=-2.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 2/128/0 | 130 | 11.8% | 2.3% | 0.95 | -3.4% | 368 | 1.61 | 1.6% | 59.0 | 10/10 | 0.90 | 0.85 | 0.10 | 4 | 4.6% | 0.59 | 0.60 | 10.6% | 9.4% | 4.3% | 10.5%/8.8% | 6.1 (interpolated) | pass | 0.128 (unverified) | -0.63 |
| 22 | `cfg_4d5e` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 6/77/20 | 103 | 28.2% | 5.1% | 0.85 | -11.1% | 624 | 1.60 | 6.2% | 47.4 | 12/12 | 0.92 | 0.54 | 0.31 | 4 | 15.4% | 0.45 | 0.69 | 27.3% | 26.5% | 32.5% | 26.6%/19.3% | 15.3 (interpolated) | pass | 0.109 (unverified) | 0.27 |
| 23 | `cfg_b2f5` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-3.0, exit_z=-1.25, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 23/92/0 | 115 | 21.6% | 4.0% | 1.08 | -4.9% | 315 | 1.82 | 3.0% | 51.9 | 10/10 | 1.00 | 0.77 | 0.31 | 3 | 10.2% | 0.53 | 0.50 | 20.4% | 19.0% | 7.3% | 19.8%/16.0% | 10.8 (interpolated) | pass | 0.211 (unverified) | -0.17 |
| 24 | `cfg_a2c0` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 12/103/0 | 115 | 21.2% | 3.9% | 1.07 | -4.9% | 315 | 1.80 | 3.1% | 51.8 | 11/11 | 1.00 | 0.78 | 0.29 | 3 | 10.4% | 0.51 | 0.50 | 19.9% | 18.5% | 7.4% | 19.5%/15.4% | 10.7 (interpolated) | pass | 0.205 (unverified) | -0.16 |
| 25 | `cfg_0e47` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=60, entry_z=-3.0, exit_z=-1.25, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 8/75/46 | 129 | 10.9% | 2.1% | 0.88 | -3.4% | 443 | 1.51 | 1.2% | 57.9 | 10/10 | 0.90 | 0.83 | 0.05 | 3 | 3.7% | 0.63 | 0.71 | 9.9% | 8.5% | -4.6% | 10.1%/7.3% | 5.8 (interpolated) | pass | 0.104 (unverified) | -0.84 |
| 26 | `cfg_435a` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=60, entry_z=-3.0, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 2/81/46 | 129 | 9.8% | 1.9% | 0.82 | -3.4% | 443 | 1.46 | 1.2% | 57.8 | 11/11 | 0.91 | 0.80 | 0.02 | 3 | 3.1% | 0.65 | 0.73 | 8.6% | 7.4% | -5.3% | 8.6%/6.5% | 5.4 (interpolated) | pass | 0.086 (unverified) | -0.87 |
| 27 | `cfg_55e3` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=100, entry_z=-2.5, exit_z=-1.25, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 50/89/41 | 180 | 24.3% | 4.4% | 1.07 | -4.9% | 450 | 1.49 | 3.9% | 80.8 | 10/10 | 1.00 | 0.68 | 0.39 | 4 | 7.7% | 0.67 | 0.50 | 22.5% | 21.2% | 4.2% | 21.4%/16.4% | 8.1 (interpolated) | pass | 0.211 (unverified) | -0.14 |
| 28 | `cfg_4be8` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=100, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 0/147/30 | 177 | 17.7% | 3.3% | 0.85 | -3.8% | 310 | 1.42 | 3.0% | 79.6 | 12/12 | 0.92 | 0.77 | 0.09 | 4 | 7.4% | 0.57 | 0.62 | 16.0% | 14.2% | 8.7% | 14.3%/9.9% | 6.6 (interpolated) | pass | 0.090 (unverified) | 0.07 |
| 29 | `cfg_9242` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=100, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 1/146/30 | 177 | 17.7% | 3.3% | 0.85 | -3.8% | 310 | 1.42 | 3.0% | 79.6 | 12/12 | 0.92 | 0.77 | 0.09 | 4 | 7.4% | 0.57 | 0.62 | 16.0% | 14.2% | 8.6% | 14.2%/10.5% | 6.6 (interpolated) | pass | 0.090 (unverified) | 0.07 |
| 30 | `cfg_c52c` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 4/86/23 | 113 | 29.9% | 5.4% | 0.86 | -10.3% | 194 | 1.51 | 6.9% | 51.9 | 11/11 | 0.91 | 0.72 | 0.14 | 5 | 14.9% | 0.45 | 0.84 | 28.7% | 28.2% | 35.6% | 28.9%/21.2% | 14.7 (interpolated) | pass | 0.100 (unverified) | 0.43 |
| 31 | `cfg_6955` | timeframe=15min, mean_type=sma, mean_lookback=100, std_lookback=100, entry_z=-3.0, exit_z=-1.25, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 15/75/26 | 116 | 21.2% | 3.9% | 1.02 | -3.5% | 440 | 1.63 | 2.7% | 52.0 | 10/10 | 1.00 | 0.73 | 0.29 | 4 | 8.2% | 0.62 | 0.62 | 19.8% | 18.6% | 5.6% | 18.4%/13.6% | 10.5 (interpolated) | pass | 0.175 (unverified) | -0.10 |
| 32 | `cfg_455a` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=80, entry_z=-2.5, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 1/106/0 | 107 | 12.0% | 2.3% | 0.87 | -2.5% | 253 | 1.64 | 1.3% | 48.3 | 8/8 | 1.00 | 0.77 | 0.10 | 5 | 6.2% | 0.48 | 0.77 | 11.1% | 10.1% | 8.3% | 10.9%/8.8% | 7.3 (interpolated) | pass | 0.091 (unverified) | -0.58 |
| 33 | `cfg_5b6e` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=80, entry_z=-2.5, exit_z=0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 2/105/0 | 107 | 12.0% | 2.3% | 0.87 | -2.5% | 253 | 1.64 | 1.3% | 48.3 | 9/9 | 1.00 | 0.84 | 0.03 | 5 | 6.2% | 0.48 | 0.77 | 11.1% | 10.1% | 8.5% | 11.0%/7.9% | 7.3 (interpolated) | pass | 0.091 (unverified) | -0.58 |
| 34 | `cfg_2d69` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 2/88/23 | 113 | 29.7% | 5.3% | 0.85 | -10.4% | 194 | 1.51 | 7.0% | 52.0 | 10/10 | 0.90 | 0.62 | 0.23 | 5 | 14.7% | 0.46 | 0.85 | 29.0% | 27.8% | 36.4% | 27.3%/19.7% | 14.6 (interpolated) | pass | 0.097 (unverified) | 0.43 |
| 35 | `cfg_d21a` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 4/79/20 | 103 | 27.8% | 5.0% | 0.83 | -11.1% | 624 | 1.59 | 6.2% | 47.3 | 12/12 | 0.92 | 0.54 | 0.29 | 4 | 15.7% | 0.44 | 0.71 | 27.0% | 26.2% | 31.7% | 27.4%/19.6% | 15.1 (interpolated) | pass | 0.098 (unverified) | 0.27 |
| 36 | `cfg_a840` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=80, entry_z=-2.5, exit_z=-1.25, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 40/73/0 | 113 | 15.8% | 3.0% | 0.90 | -4.2% | 318 | 1.62 | 1.9% | 51.1 | 10/10 | 1.00 | 0.70 | 0.20 | 3 | 7.0% | 0.53 | 0.62 | 14.8% | 13.6% | -4.6% | 13.6%/10.4% | 8.9 (interpolated) | pass | 0.108 (unverified) | -0.10 |
| 37 | `cfg_366e` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=100, entry_z=-3.0, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 0/74/41 | 115 | 13.4% | 2.5% | 0.99 | -2.6% | 314 | 1.60 | 1.1% | 51.8 | 10/10 | 1.00 | 0.63 | 0.35 | 4 | 7.0% | 0.47 | 0.64 | 12.2% | 11.5% | 3.9% | 11.3%/9.0% | 7.4 (interpolated) | pass | 0.155 (unverified) | 0.38 |
| 38 | `cfg_4bc6` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=100, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 0/74/41 | 115 | 13.4% | 2.5% | 0.99 | -2.6% | 314 | 1.60 | 1.1% | 51.8 | 10/10 | 1.00 | 0.63 | 0.35 | 4 | 7.0% | 0.47 | 0.64 | 12.2% | 11.5% | 3.9% | 11.7%/9.6% | 7.4 (interpolated) | pass | 0.155 (unverified) | 0.38 |
| 39 | `cfg_28e7` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 25/91/53 | 169 | 53.9% | 9.0% | 0.93 | -8.7% | 220 | 1.48 | 14.2% | 76.7 | 12/12 | 0.83 | 0.37 | 0.56 | 4 | 35.8% | 0.31 | 0.62 | 51.5% | 49.5% | 38.0% | 47.9%/35.8% | 16.0 (interpolated) | pass | 0.128 (unverified) | -0.02 |
| 40 | `cfg_84db` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 10/97/52 | 159 | 48.2% | 8.2% | 0.88 | -9.9% | 159 | 1.42 | 13.6% | 72.7 | 11/11 | 0.73 | 0.58 | 0.30 | 5 | 30.6% | 0.31 | 0.66 | 46.8% | 45.8% | 56.3% | 41.6%/28.6% | 15.8 (interpolated) | pass | 0.111 (unverified) | 0.04 |
| 41 | `cfg_ef5d` | timeframe=15min, mean_type=sma, mean_lookback=100, std_lookback=100, entry_z=-3.0, exit_z=-1.25, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 5/93/18 | 116 | 17.6% | 3.3% | 0.97 | -4.0% | 347 | 1.62 | 1.9% | 52.5 | 11/11 | 1.00 | 0.65 | 0.32 | 4 | 9.0% | 0.47 | 0.60 | 16.2% | 15.1% | 7.4% | 15.5%/12.0% | 9.1 (interpolated) | pass | 0.142 (unverified) | 0.02 |
| 42 | `cfg_c920` | timeframe=15min, mean_type=sma, mean_lookback=100, std_lookback=100, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 5/93/18 | 116 | 17.8% | 3.3% | 0.98 | -4.0% | 347 | 1.62 | 2.0% | 52.4 | 12/12 | 1.00 | 0.66 | 0.32 | 4 | 9.2% | 0.47 | 0.59 | 16.3% | 15.3% | 7.4% | 16.1%/11.8% | 9.2 (interpolated) | pass | 0.146 (unverified) | 0.10 |
| 43 | `cfg_0bf1` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=80, entry_z=-2.5, exit_z=-1.25, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 18/135/0 | 153 | 13.6% | 2.6% | 0.95 | -2.6% | 318 | 1.54 | 1.8% | 69.3 | 9/9 | 1.00 | 0.66 | 0.29 | 3 | 7.6% | 0.44 | 0.58 | 12.6% | 11.1% | -1.0% | 12.4%/8.7% | 5.9 (interpolated) | pass | 0.138 (unverified) | -0.21 |
| 44 | `cfg_2909` | timeframe=15min, mean_type=sma, mean_lookback=100, std_lookback=100, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 8/82/26 | 116 | 20.5% | 3.8% | 1.00 | -3.5% | 440 | 1.61 | 2.7% | 52.1 | 11/11 | 1.00 | 0.74 | 0.26 | 4 | 8.6% | 0.59 | 0.65 | 19.1% | 17.6% | 5.5% | 18.1%/14.2% | 10.2 (interpolated) | pass | 0.163 (unverified) | -0.08 |
| 45 | `cfg_8eb6` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=80, entry_z=-2.5, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 0/153/0 | 153 | 12.8% | 2.4% | 0.90 | -3.4% | 318 | 1.50 | 1.9% | 69.4 | 9/9 | 1.00 | 0.70 | 0.20 | 3 | 6.9% | 0.46 | 0.65 | 11.8% | 10.4% | 0.0% | 12.1%/8.8% | 5.6 (interpolated) | pass | 0.119 (unverified) | -0.17 |
| 46 | `cfg_3791` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 7/100/52 | 159 | 47.8% | 8.1% | 0.88 | -9.9% | 159 | 1.41 | 13.7% | 72.6 | 10/10 | 0.70 | 0.48 | 0.39 | 5 | 30.4% | 0.31 | 0.64 | 45.6% | 44.1% | 56.6% | 40.8%/28.1% | 15.5 (interpolated) | pass | 0.106 (unverified) | 0.02 |
| 47 | `cfg_6b3b` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=60, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 19/117/51 | 187 | 31.6% | 5.6% | 0.97 | -5.4% | 308 | 1.50 | 4.2% | 85.3 | 11/11 | 0.73 | 0.56 | 0.41 | 4 | 8.7% | 0.66 | 0.75 | 29.7% | 28.1% | 21.4% | 29.4%/23.9% | 9.7 (interpolated) | pass | 0.149 (unverified) | -0.31 |
| 48 | `cfg_8587` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=60, entry_z=-3.0, exit_z=-1.25, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 32/104/51 | 187 | 32.9% | 5.9% | 1.01 | -5.5% | 308 | 1.51 | 4.2% | 85.2 | 10/10 | 0.70 | 0.36 | 0.66 | 4 | 10.7% | 0.61 | 0.71 | 30.3% | 28.8% | 23.6% | 29.2%/22.7% | 10.0 (interpolated) | pass | 0.173 (unverified) | -0.30 |
| 49 | `cfg_f567` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=80, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 21/92/0 | 113 | 14.0% | 2.7% | 0.81 | -4.3% | 318 | 1.56 | 2.0% | 51.2 | 11/11 | 1.00 | 0.74 | 0.06 | 3 | 6.9% | 0.52 | 0.71 | 13.3% | 12.4% | -4.1% | 12.9%/10.0% | 8.0 (interpolated) | pass | 0.073 (unverified) | -0.14 |
| 50 | `cfg_bf02` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 17/99/53 | 169 | 56.6% | 9.4% | 0.97 | -8.8% | 220 | 1.49 | 14.4% | 76.9 | 12/12 | 0.83 | 0.37 | 0.59 | 4 | 35.1% | 0.31 | 0.59 | 53.2% | 51.5% | 42.3% | 49.9%/32.4% | 16.8 (interpolated) | pass | 0.145 (unverified) | -0.03 |
| 51 | `cfg_35ac` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=80, entry_z=-3.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 1/104/0 | 105 | 15.6% | 2.9% | 0.76 | -6.3% | 329 | 1.55 | 2.9% | 47.6 | 9/9 | 1.00 | 0.70 | 0.06 | 4 | 5.2% | 0.65 | 0.86 | 14.7% | 13.2% | 10.5% | 14.5%/9.8% | 9.1 (interpolated) | pass | 0.063 (unverified) | 0.37 |
| 52 | `cfg_cccd` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=80, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 14/91/0 | 105 | 15.1% | 2.8% | 0.77 | -6.4% | 329 | 1.53 | 2.8% | 47.6 | 10/10 | 1.00 | 0.73 | 0.04 | 4 | 4.2% | 0.72 | 0.81 | 14.1% | 13.3% | 9.8% | 14.0%/10.1% | 8.9 (interpolated) | pass | 0.073 (unverified) | 0.35 |
| 53 | `cfg_c4f3` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=80, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 32/70/0 | 102 | 15.9% | 3.0% | 0.88 | -3.1% | 284 | 1.66 | 1.8% | 46.5 | 10/10 | 1.00 | 0.57 | 0.31 | 5 | 9.5% | 0.37 | 0.69 | 15.0% | 13.8% | 2.8% | 15.0%/11.0% | 9.6 (interpolated) | pass | 0.097 (unverified) | -0.58 |
| 54 | `cfg_3ae7` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=100, entry_z=-2.5, exit_z=-1.25, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 23/107/0 | 130 | 13.9% | 2.6% | 0.75 | -3.5% | 301 | 1.48 | 2.3% | 58.4 | 10/10 | 1.00 | 0.65 | 0.10 | 4 | 4.8% | 0.67 | 0.81 | 12.6% | 11.3% | 1.6% | 12.4%/9.3% | 6.9 (interpolated) | pass | 0.057 (unverified) | 0.18 |
| 55 | `cfg_b00f` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=20, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 1/79/24 | 104 | 30.5% | 5.5% | 0.78 | -8.3% | 382 | 1.58 | 6.4% | 47.7 | 10/10 | 0.80 | 0.40 | 0.38 | 4 | 18.1% | 0.37 | 0.73 | 29.1% | 27.3% | 46.4% | 28.6%/18.9% | 15.7 (interpolated) | pass | 0.061 (unverified) | 0.78 |
| 56 | `cfg_d4d4` | timeframe=15min, mean_type=sma, mean_lookback=100, std_lookback=80, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 12/124/0 | 136 | 15.8% | 3.0% | 0.75 | -5.0% | 278 | 1.44 | 3.6% | 61.0 | 10/10 | 0.80 | 0.69 | 0.06 | 3 | 9.0% | 0.43 | 0.73 | 14.6% | 13.1% | 15.4% | 14.4%/10.5% | 7.3 (interpolated) | pass | 0.068 (unverified) | -0.24 |
| 57 | `cfg_53f1` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-3.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 4/106/0 | 110 | 32.6% | 5.8% | 0.76 | -10.4% | 538 | 1.42 | 11.1% | 50.4 | 10/10 | 0.80 | 0.57 | 0.19 | 3 | 14.0% | 0.58 | 0.87 | 30.9% | 30.1% | 55.2% | 30.9%/22.8% | 16.1 (interpolated) | pass | 0.083 (unverified) | 0.12 |
| 58 | `cfg_0e64` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=100, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 12/118/0 | 130 | 14.2% | 2.7% | 0.76 | -3.5% | 301 | 1.49 | 2.4% | 58.4 | 11/11 | 1.00 | 0.72 | 0.05 | 4 | 5.2% | 0.64 | 0.82 | 13.0% | 11.9% | 3.3% | 11.8%/8.6% | 7.0 (interpolated) | pass | 0.059 (unverified) | 0.15 |
| 59 | `cfg_3ccc` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=80, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 14/88/0 | 102 | 15.4% | 2.9% | 0.86 | -3.1% | 284 | 1.64 | 1.8% | 46.4 | 10/10 | 1.00 | 0.57 | 0.29 | 5 | 9.2% | 0.40 | 0.71 | 14.7% | 13.7% | 2.9% | 14.2%/10.2% | 9.4 (interpolated) | pass | 0.089 (unverified) | -0.58 |
| 60 | `cfg_3387` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 12/107/0 | 119 | 37.8% | 6.6% | 0.77 | -11.5% | 220 | 1.46 | 11.8% | 54.4 | 10/10 | 0.90 | 0.53 | 0.24 | 3 | 15.3% | 0.53 | 0.78 | 37.1% | 33.7% | 56.9% | 32.3%/23.1% | 16.5 (interpolated) | pass | 0.075 (unverified) | 0.01 |
| 61 | `cfg_956a` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-3.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 3/107/0 | 110 | 32.6% | 5.8% | 0.76 | -10.4% | 538 | 1.42 | 11.1% | 50.4 | 9/9 | 0.78 | 0.46 | 0.29 | 3 | 14.0% | 0.58 | 0.87 | 30.9% | 30.1% | 55.3% | 29.9%/20.5% | 16.1 (interpolated) | pass | 0.083 (unverified) | 0.12 |
| 62 | `cfg_e14a` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 7/111/0 | 118 | 37.8% | 6.6% | 0.77 | -11.6% | 215 | 1.46 | 11.9% | 53.9 | 9/9 | 0.89 | 0.50 | 0.28 | 3 | 15.4% | 0.53 | 0.78 | 37.1% | 33.6% | 55.7% | 32.6%/21.8% | 16.7 (interpolated) | pass | 0.075 (unverified) | -0.00 |
| 63 | `cfg_018b` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 4/76/25 | 105 | 29.6% | 5.3% | 0.76 | -8.3% | 382 | 1.53 | 6.4% | 48.3 | 11/11 | 0.82 | 0.49 | 0.27 | 4 | 17.3% | 0.39 | 0.76 | 28.2% | 26.7% | 52.8% | 27.1%/17.1% | 15.2 (interpolated) | pass | 0.057 (unverified) | 0.78 |
| 64 | `cfg_5cb3` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=80, entry_z=-2.5, exit_z=-1.25, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 21/87/68 | 176 | 12.5% | 2.4% | 0.86 | -3.3% | 332 | 1.37 | 1.6% | 79.6 | 9/9 | 0.89 | 0.72 | 0.14 | 3 | 6.2% | 0.51 | 0.66 | 10.9% | 9.1% | -6.6% | 10.4%/7.5% | 5.1 (interpolated) | pass | 0.103 (unverified) | 0.07 |
| 65 | `cfg_ad36` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-3.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 41/345/86 | 472 | 37.8% | 6.6% | 0.87 | -14.1% | 548 | 1.30 | 7.8% | 213.9 | 13/13 | 0.77 | 0.34 | 0.53 | 4 | 11.2% | 0.57 | 0.63 | 32.1% | 27.1% | 10.2% | 32.2%/20.8% | 5.0 (interpolated) | pass | 0.092 (unverified) | -0.27 |
| 66 | `cfg_76a5` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 13/104/53 | 170 | 37.9% | 6.6% | 0.76 | -9.1% | 317 | 1.33 | 14.5% | 78.1 | 10/10 | 0.90 | 0.49 | 0.26 | 5 | 17.3% | 0.48 | 0.73 | 36.7% | 35.0% | 32.3% | 32.3%/20.4% | 12.4 (interpolated) | pass | 0.074 (unverified) | -0.41 |
| 67 | `cfg_055b` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=80, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 1/192/0 | 193 | 17.8% | 3.3% | 0.75 | -5.2% | 520 | 1.42 | 3.5% | 87.1 | 11/11 | 1.00 | 0.71 | 0.04 | 4 | 7.8% | 0.56 | 0.80 | 15.8% | 14.5% | 12.2% | 16.4%/11.1% | 6.0 (interpolated) | pass | 0.049 (unverified) | 0.01 |
| 68 | `cfg_d1d8` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=80, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 1/192/0 | 193 | 17.8% | 3.3% | 0.75 | -5.2% | 520 | 1.42 | 3.5% | 87.1 | 10/10 | 1.00 | 0.70 | 0.05 | 4 | 7.8% | 0.56 | 0.80 | 15.8% | 14.5% | 12.2% | 15.8%/12.0% | 6.0 (interpolated) | pass | 0.049 (unverified) | 0.01 |
| 69 | `cfg_683a` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=80, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 43/140/0 | 183 | 21.9% | 4.0% | 0.86 | -6.5% | 309 | 1.49 | 4.7% | 82.7 | 10/10 | 0.90 | 0.67 | 0.20 | 4 | 9.8% | 0.54 | 0.67 | 20.0% | 18.5% | 9.7% | 19.1%/13.4% | 7.5 (interpolated) | pass | 0.088 (unverified) | -0.05 |
| 70 | `cfg_da50` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=80, entry_z=-2.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 10/98/68 | 176 | 12.0% | 2.3% | 0.83 | -3.4% | 332 | 1.35 | 1.6% | 79.5 | 10/10 | 0.90 | 0.70 | 0.12 | 3 | 5.5% | 0.54 | 0.69 | 10.6% | 8.8% | -6.4% | 10.8%/7.7% | 4.9 (interpolated) | pass | 0.092 (unverified) | 0.08 |
| 71 | `cfg_fd17` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-3.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 28/358/85 | 471 | 35.0% | 6.2% | 0.84 | -14.4% | 555 | 1.28 | 7.8% | 213.2 | 13/13 | 0.77 | 0.31 | 0.54 | 4 | 15.1% | 0.57 | 0.62 | 30.3% | 24.8% | 11.8% | 31.6%/22.3% | 4.7 (interpolated) | pass | 0.091 (unverified) | -0.20 |
| 72 | `cfg_8d16` | timeframe=15min, mean_type=sma, mean_lookback=100, std_lookback=100, entry_z=-2.5, exit_z=-1.25, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 46/134/69 | 249 | 22.2% | 4.1% | 0.80 | -6.2% | 358 | 1.29 | 5.4% | 111.5 | 9/9 | 1.00 | 0.64 | 0.16 | 3 | 3.2% | 0.88 | 0.59 | 20.0% | 17.9% | 22.0% | 18.4%/11.8% | 5.8 (interpolated) | pass | 0.093 (unverified) | -0.09 |
| 73 | `cfg_42be` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-3.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 33/82/57 | 172 | 37.9% | 6.6% | 0.77 | -8.2% | 227 | 1.35 | 13.8% | 78.5 | 10/10 | 0.80 | 0.58 | 0.19 | 4 | 17.6% | 0.54 | 0.60 | 36.4% | 34.5% | 24.0% | 34.5%/24.0% | 12.4 (interpolated) | pass | 0.073 (unverified) | -0.25 |
| 74 | `cfg_e5b3` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=80, entry_z=-2.5, exit_z=-1.25, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 66/117/0 | 183 | 19.9% | 3.7% | 0.82 | -6.4% | 309 | 1.45 | 4.6% | 82.4 | 9/9 | 1.00 | 0.62 | 0.20 | 4 | 9.0% | 0.53 | 0.67 | 17.9% | 16.5% | 11.0% | 17.8%/14.4% | 7.0 (interpolated) | pass | 0.078 (unverified) | -0.23 |
| 75 | `cfg_31dd` | timeframe=15min, mean_type=sma, mean_lookback=100, std_lookback=100, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 28/152/69 | 249 | 23.1% | 4.3% | 0.82 | -6.0% | 358 | 1.30 | 5.5% | 111.4 | 10/10 | 1.00 | 0.65 | 0.17 | 3 | 4.8% | 0.81 | 0.60 | 20.9% | 18.6% | 24.3% | 18.6%/12.1% | 6.0 (interpolated) | pass | 0.103 (unverified) | -0.09 |
| 76 | `cfg_b78b` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-4.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 40/378/0 | 418 | 41.3% | 7.2% | 0.86 | -11.2% | 379 | 1.38 | 7.5% | 189.1 | 11/11 | 0.82 | 0.42 | 0.44 | 3 | 18.9% | 0.54 | 0.71 | 36.7% | 31.7% | 20.8% | 37.4%/27.7% | 5.9 (interpolated) | pass | 0.094 (unverified) | -0.00 |
| 77 | `cfg_0373` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-4.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 49/369/0 | 418 | 40.7% | 7.1% | 0.83 | -11.2% | 379 | 1.37 | 7.4% | 189.0 | 11/11 | 0.82 | 0.40 | 0.42 | 3 | 13.4% | 0.59 | 0.78 | 34.8% | 31.0% | 17.7% | 35.3%/26.0% | 5.7 (interpolated) | pass | 0.078 (unverified) | 0.03 |
| 78 | `cfg_2699` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=80, entry_z=-2.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 10/146/98 | 254 | 13.1% | 2.5% | 0.86 | -4.5% | 515 | 1.28 | 2.4% | 113.8 | 10/10 | 0.90 | 0.74 | 0.12 | 4 | 4.3% | 0.67 | 0.65 | 11.0% | 8.5% | -0.3% | 10.0%/6.9% | 3.9 (interpolated) | pass | 0.104 (unverified) | 0.13 |
| 79 | `cfg_ce7c` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=80, entry_z=-2.5, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 0/156/98 | 254 | 13.4% | 2.6% | 0.86 | -4.5% | 515 | 1.28 | 2.4% | 114.0 | 9/9 | 0.89 | 0.72 | 0.14 | 4 | 4.6% | 0.65 | 0.69 | 11.5% | 8.9% | -1.1% | 10.1%/6.1% | 4.0 (interpolated) | pass | 0.105 (unverified) | 0.15 |
| 80 | `cfg_8639` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 20/61/32 | 113 | 37.0% | 6.5% | 0.85 | -9.1% | 180 | 1.49 | 9.4% | 52.1 | 10/10 | 0.90 | 0.58 | 0.28 | 4 | 19.9% | 0.41 | 0.72 | 35.5% | 34.7% | 35.1% | 34.6%/27.0% | 17.5 (interpolated) | pass | 0.108 (unverified) | 0.11 |
| 81 | `cfg_eb90` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 12/69/32 | 113 | 36.0% | 6.3% | 0.83 | -8.9% | 180 | 1.48 | 9.5% | 52.1 | 10/10 | 0.90 | 0.58 | 0.26 | 4 | 18.9% | 0.42 | 0.74 | 35.1% | 34.0% | 34.8% | 33.1%/19.7% | 17.3 (interpolated) | pass | 0.099 (unverified) | 0.06 |
| 82 | `cfg_8130` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=80, entry_z=-2.5, exit_z=-1.25, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.0 | 14/152/24 | 190 | 13.6% | 2.6% | 0.82 | -3.5% | 318 | 1.36 | 2.2% | 85.9 | 10/10 | 1.00 | 0.60 | 0.22 | 3 | 7.4% | 0.43 | 0.69 | 12.0% | 10.6% | 5.2% | 11.8%/7.9% | 5.0 (interpolated) | pass | 0.084 (unverified) | -0.02 |
| 83 | `cfg_186c` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=80, entry_z=-2.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.0 | 9/157/24 | 190 | 13.8% | 2.6% | 0.83 | -3.5% | 318 | 1.36 | 2.2% | 85.9 | 11/11 | 1.00 | 0.66 | 0.17 | 3 | 7.5% | 0.43 | 0.69 | 12.1% | 10.6% | 5.1% | 11.9%/8.7% | 5.1 (interpolated) | pass | 0.086 (unverified) | -0.02 |
| 84 | `cfg_f0c4` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=60, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 12/64/56 | 132 | 13.6% | 2.6% | 0.85 | -4.2% | 365 | 1.50 | 1.7% | 59.7 | 12/12 | 0.92 | 0.59 | 0.26 | 3 | 6.0% | 0.57 | 0.80 | 12.4% | 10.7% | -5.4% | 12.7%/8.8% | 6.8 (interpolated) | pass | 0.082 (unverified) | -0.88 |
| 85 | `cfg_cc4b` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-4.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 47/305/0 | 352 | 35.2% | 6.2% | 0.80 | -17.4% | 388 | 1.39 | 9.3% | 160.9 | 9/9 | 0.89 | 0.28 | 0.52 | 3 | 7.3% | 0.66 | 0.80 | 32.1% | 28.8% | -2.1% | 33.3%/23.0% | 6.3 (interpolated) | pass | 0.067 (unverified) | -0.42 |
| 86 | `cfg_7dd4` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=100, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 27/114/54 | 195 | 23.1% | 4.3% | 0.85 | -4.7% | 207 | 1.39 | 4.4% | 87.4 | 10/10 | 1.00 | 0.60 | 0.25 | 5 | 8.8% | 0.61 | 0.72 | 20.7% | 18.8% | 7.3% | 20.5%/15.1% | 7.1 (interpolated) | pass | 0.081 (unverified) | -0.24 |
| 87 | `cfg_1781` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=60, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 3/73/56 | 132 | 13.5% | 2.6% | 0.85 | -4.2% | 365 | 1.50 | 1.7% | 59.8 | 12/12 | 0.92 | 0.57 | 0.27 | 3 | 5.9% | 0.57 | 0.80 | 12.1% | 10.5% | -5.6% | 12.0%/9.2% | 6.8 (interpolated) | pass | 0.080 (unverified) | -0.90 |
| 88 | `cfg_1b20` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 49/319/0 | 368 | 51.3% | 8.6% | 0.80 | -13.6% | 267 | 1.32 | 9.8% | 167.1 | 10/10 | 1.00 | 0.46 | 0.34 | 5 | 26.8% | 0.48 | 0.54 | 45.8% | 41.2% | 41.3% | 42.5%/31.2% | 7.4 (interpolated) | pass | 0.089 (unverified) | 0.83 |
| 89 | `cfg_6b02` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=80, entry_z=-2.5, exit_z=0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 0/195/130 | 325 | 14.9% | 2.8% | 0.83 | -6.4% | 548 | 1.25 | 3.0% | 145.5 | 10/10 | 0.80 | 0.64 | 0.19 | 3 | 5.5% | 0.62 | 0.65 | 11.4% | 8.4% | -1.6% | 11.2%/7.2% | 3.5 (interpolated) | pass | 0.087 (unverified) | -0.01 |
| 90 | `cfg_ad60` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=80, entry_z=-2.5, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 0/195/130 | 325 | 14.9% | 2.8% | 0.83 | -6.4% | 548 | 1.25 | 3.0% | 145.5 | 9/9 | 0.78 | 0.60 | 0.22 | 3 | 5.5% | 0.62 | 0.65 | 11.4% | 8.4% | -1.6% | 11.5%/7.6% | 3.5 (interpolated) | pass | 0.087 (unverified) | -0.01 |
| 91 | `cfg_0b51` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=80, entry_z=-3.0, exit_z=-1.25, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 12/52/41 | 105 | 13.2% | 2.5% | 0.82 | -3.8% | 324 | 1.56 | 1.4% | 47.7 | 11/11 | 1.00 | 0.55 | 0.27 | 4 | 7.2% | 0.44 | 0.82 | 12.0% | 11.2% | -6.5% | 12.4%/8.8% | 8.2 (interpolated) | pass | 0.073 (unverified) | -0.13 |
| 92 | `cfg_ad11` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=80, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 7/57/41 | 105 | 12.2% | 2.3% | 0.78 | -3.8% | 324 | 1.52 | 1.4% | 47.6 | 12/12 | 1.00 | 0.53 | 0.25 | 4 | 6.4% | 0.46 | 0.88 | 11.3% | 10.2% | -6.0% | 11.3%/7.4% | 7.8 (interpolated) | pass | 0.062 (unverified) | -0.13 |
| 93 | `cfg_f092` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=100, entry_z=-2.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.0 | 3/157/23 | 183 | 12.9% | 2.5% | 0.80 | -4.2% | 415 | 1.36 | 2.1% | 82.9 | 11/11 | 1.00 | 0.69 | 0.11 | 3 | 4.8% | 0.61 | 0.69 | 10.9% | 9.2% | 3.8% | 10.3%/6.8% | 4.9 (interpolated) | pass | 0.079 (unverified) | -0.22 |
| 94 | `cfg_9306` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=100, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 2/139/54 | 195 | 21.9% | 4.0% | 0.82 | -4.8% | 207 | 1.37 | 4.5% | 87.8 | 9/9 | 1.00 | 0.52 | 0.30 | 4 | 7.4% | 0.65 | 0.76 | 19.8% | 17.0% | 8.1% | 18.9%/14.2% | 6.9 (interpolated) | pass | 0.075 (unverified) | -0.22 |
| 95 | `cfg_9d8a` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=100, entry_z=-2.5, exit_z=-1.25, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.0 | 8/152/23 | 183 | 12.9% | 2.5% | 0.80 | -4.2% | 415 | 1.36 | 2.1% | 82.9 | 10/10 | 1.00 | 0.66 | 0.14 | 3 | 4.8% | 0.61 | 0.69 | 10.9% | 9.2% | 3.7% | 10.0%/6.4% | 4.9 (interpolated) | pass | 0.079 (unverified) | -0.29 |
| 96 | `cfg_822c` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 36/105/0 | 141 | 38.4% | 6.7% | 0.75 | -12.4% | 428 | 1.47 | 13.6% | 64.1 | 10/10 | 0.70 | 0.44 | 0.31 | 4 | 15.3% | 0.50 | 0.71 | 36.8% | 35.8% | 36.1% | 36.2%/26.8% | 14.7 (interpolated) | pass | 0.059 (unverified) | -0.31 |
| 97 | `cfg_ce0c` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 21/120/0 | 141 | 40.9% | 7.1% | 0.79 | -12.1% | 428 | 1.48 | 14.0% | 64.4 | 10/10 | 0.80 | 0.46 | 0.33 | 4 | 17.6% | 0.48 | 0.70 | 39.2% | 36.8% | 39.8% | 39.0%/27.7% | 14.8 (interpolated) | pass | 0.069 (unverified) | -0.26 |
| 98 | `cfg_3b74` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-4.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 72/280/0 | 352 | 34.6% | 6.1% | 0.80 | -16.9% | 435 | 1.39 | 9.1% | 160.3 | 9/9 | 0.89 | 0.25 | 0.55 | 3 | 9.8% | 0.59 | 0.75 | 31.0% | 27.2% | 1.7% | 32.7%/23.3% | 6.0 (interpolated) | pass | 0.066 (unverified) | -0.37 |
| 99 | `cfg_9c3c` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-4.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 16/65/35 | 116 | 33.6% | 6.0% | 0.78 | -9.7% | 220 | 1.42 | 9.6% | 53.2 | 9/9 | 0.78 | 0.60 | 0.18 | 5 | 19.8% | 0.37 | 0.90 | 31.6% | 30.5% | 36.4% | 32.8%/23.0% | 15.7 (interpolated) | pass | 0.085 (unverified) | -0.19 |
| 100 | `cfg_35c5` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=15, entry_z=-2.5, exit_z=-0.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 36/366/194 | 596 | 24.6% | 4.5% | 0.80 | -9.3% | 376 | 1.23 | 6.0% | 270.3 | 10/10 | 0.80 | 0.34 | 0.46 | 4 | 6.0% | 0.72 | 0.73 | 18.4% | 12.2% | -10.5% | 22.1%/13.1% | 3.1 (interpolated) | pass | 0.076 (unverified) | -1.31 |
| 101 | `cfg_c5fb` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=15, entry_z=-2.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 49/354/194 | 597 | 24.7% | 4.5% | 0.81 | -9.8% | 376 | 1.24 | 6.0% | 271.0 | 10/10 | 0.80 | 0.38 | 0.42 | 4 | 5.9% | 0.72 | 0.73 | 18.0% | 12.2% | -10.0% | 21.1%/12.3% | 3.1 (interpolated) | pass | 0.078 (unverified) | -1.27 |
| 102 | `cfg_57c7` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 135/330/197 | 662 | 46.1% | 7.9% | 0.77 | -19.6% | 557 | 1.22 | 14.1% | 299.7 | 12/12 | 0.83 | 0.19 | 0.58 | 4 | 15.9% | 0.53 | 0.61 | 38.8% | 28.1% | 37.7% | 36.0%/26.6% | 4.3 (interpolated) | pass | 0.074 (unverified) | 0.05 |
| 103 | `cfg_b27b` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 187/374/0 | 561 | 47.6% | 8.1% | 0.87 | -9.5% | 536 | 1.28 | 13.5% | 254.1 | 11/11 | 0.73 | 0.42 | 0.45 | 4 | 16.0% | 0.55 | 0.55 | 41.0% | 33.7% | 32.2% | 39.5%/30.1% | 5.1 (interpolated) | pass | 0.097 (unverified) | 0.09 |
| 104 | `cfg_6376` | timeframe=15min, mean_type=ema, mean_lookback=80, std_lookback=20, entry_z=-4.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 12/138/0 | 150 | 36.3% | 6.4% | 0.76 | -12.5% | 265 | 1.54 | 4.1% | 69.3 | 9/9 | 0.78 | 0.39 | 0.37 | 4 | 13.7% | 0.63 | 0.46 | 34.8% | 34.3% | 21.2% | 30.9%/24.4% | 13.4 (interpolated) | pass | 0.100 (unverified) | 0.41 |
| 105 | `cfg_2fd7` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 21/514/0 | 535 | 31.4% | 5.6% | 0.77 | -12.0% | 252 | 1.28 | 6.5% | 243.1 | 11/11 | 0.64 | 0.38 | 0.39 | 3 | 9.9% | 0.65 | 0.80 | 26.6% | 20.2% | -7.5% | 29.2%/19.3% | 4.0 (interpolated) | pass | 0.054 (unverified) | 0.32 |
| 106 | `cfg_6fb7` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=15, entry_z=-3.0, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 15/520/0 | 535 | 30.3% | 5.4% | 0.76 | -12.0% | 252 | 1.27 | 6.5% | 242.8 | 10/10 | 0.60 | 0.31 | 0.45 | 3 | 9.9% | 0.63 | 0.80 | 25.2% | 19.0% | -8.8% | 29.7%/19.7% | 3.9 (interpolated) | pass | 0.053 (unverified) | 0.32 |
| 107 | `cfg_18de` | timeframe=15min, mean_type=ema, mean_lookback=80, std_lookback=80, entry_z=-2.5, exit_z=0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 2/184/122 | 308 | 14.6% | 2.8% | 0.82 | -4.6% | 440 | 1.24 | 2.9% | 138.5 | 10/10 | 0.90 | 0.57 | 0.25 | 4 | 6.9% | 0.52 | 0.79 | 11.6% | 8.3% | 0.1% | 11.6%/6.5% | 3.7 (interpolated) | pass | 0.087 (unverified) | 0.07 |
| 108 | `cfg_352e` | timeframe=15min, mean_type=ema, mean_lookback=80, std_lookback=80, entry_z=-2.5, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 2/184/122 | 308 | 14.6% | 2.8% | 0.82 | -4.6% | 440 | 1.24 | 2.9% | 138.5 | 9/9 | 0.89 | 0.53 | 0.29 | 4 | 6.9% | 0.52 | 0.79 | 11.6% | 8.3% | 0.1% | 10.0%/5.5% | 3.7 (interpolated) | pass | 0.087 (unverified) | 0.07 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 1.0% / 0.55 / 18 | -0.9% / -0.54 / 21 | 9.5% / 2.23 / 31 | 9.4% / 2.31 / 36 | -0.7% / -0.33 / 25 |
| 2 | 1.0% / 0.55 / 18 | -0.9% / -0.54 / 21 | 9.5% / 2.23 / 31 | 9.4% / 2.31 / 36 | -0.7% / -0.33 / 25 |
| 3 | 6.5% / 1.93 / 36 | -0.9% / -0.69 / 15 | 4.7% / 1.72 / 19 | 6.7% / 1.76 / 28 | -1.0% / -0.35 / 18 |
| 4 | 6.5% / 1.93 / 36 | -0.9% / -0.69 / 15 | 4.7% / 1.72 / 19 | 6.7% / 1.76 / 28 | -1.0% / -0.35 / 18 |
| 5 | 1.5% / 0.88 / 15 | -0.1% / -0.06 / 17 | 6.6% / 2.13 / 26 | 6.2% / 2.03 / 27 | -1.3% / -0.46 / 15 |
| 6 | 2.1% / 0.99 / 15 | 0.0% / 0.02 / 17 | 6.1% / 2.03 / 26 | 6.1% / 2.01 / 27 | -2.1% / -0.82 / 15 |
| 7 | 3.7% / 1.79 / 20 | -0.0% / -0.02 / 16 | 4.5% / 1.72 / 21 | 8.5% / 2.16 / 30 | -1.8% / -0.64 / 16 |
| 8 | 3.7% / 1.79 / 20 | -0.0% / -0.02 / 16 | 4.5% / 1.72 / 21 | 8.5% / 2.16 / 30 | -1.8% / -0.64 / 16 |
| 9 | 0.2% / 0.12 / 26 | -1.7% / -0.92 / 29 | 7.5% / 1.71 / 37 | 10.9% / 2.99 / 46 | 1.2% / 0.51 / 32 |
| 10 | 3.4% / 1.11 / 39 | -1.8% / -0.58 / 30 | 3.9% / 0.92 / 40 | 15.6% / 2.70 / 46 | 4.0% / 0.74 / 25 |
| 11 | 0.2% / 0.12 / 26 | -1.7% / -0.92 / 29 | 7.8% / 1.76 / 37 | 10.8% / 2.98 / 46 | 1.2% / 0.51 / 32 |
| 12 | 2.1% / 0.97 / 18 | 0.3% / 0.19 / 19 | 5.5% / 1.32 / 21 | 4.3% / 1.44 / 30 | 0.1% / 0.06 / 18 |
| 13 | 4.4% / 1.68 / 22 | -1.3% / -0.98 / 18 | 5.7% / 2.30 / 24 | 6.8% / 2.15 / 26 | -3.5% / -1.29 / 10 |
| 14 | 3.5% / 1.37 / 26 | -0.1% / -0.03 / 21 | 7.5% / 1.85 / 24 | 5.5% / 1.41 / 35 | -1.7% / -0.40 / 16 |
| 15 | 3.5% / 1.36 / 26 | -0.3% / -0.15 / 21 | 7.5% / 1.85 / 24 | 5.5% / 1.41 / 35 | -1.5% / -0.38 / 16 |
| 16 | 2.1% / 0.97 / 18 | 0.3% / 0.19 / 19 | 5.5% / 1.32 / 21 | 4.3% / 1.44 / 30 | -0.7% / -0.39 / 18 |
| 17 | 4.4% / 1.68 / 22 | -1.3% / -0.98 / 18 | 5.7% / 2.30 / 24 | 6.7% / 2.14 / 26 | -3.5% / -1.29 / 10 |
| 18 | 1.4% / 0.48 / 52 | -0.5% / -0.38 / 20 | 3.3% / 1.10 / 26 | 7.7% / 2.07 / 45 | 0.2% / 0.10 / 32 |
| 19 | 0.2% / 0.11 / 19 | 1.0% / 0.78 / 26 | 6.8% / 2.04 / 30 | 4.7% / 1.48 / 35 | -1.3% / -0.68 / 20 |
| 20 | 1.4% / 0.48 / 52 | -0.5% / -0.38 / 20 | 3.3% / 1.10 / 26 | 7.7% / 2.07 / 45 | 0.2% / 0.10 / 32 |
| 21 | 0.2% / 0.11 / 19 | 1.1% / 0.84 / 26 | 6.8% / 2.04 / 30 | 4.7% / 1.48 / 35 | -1.3% / -0.68 / 20 |
| 22 | -0.6% / -0.09 / 30 | 0.1% / 0.05 / 14 | 3.8% / 0.53 / 13 | 11.7% / 2.13 / 16 | 11.1% / 1.37 / 30 |
| 23 | 3.3% / 1.17 / 24 | -0.8% / -0.40 / 18 | 8.0% / 1.92 / 24 | 10.4% / 2.21 / 34 | -0.6% / -0.11 / 15 |
| 24 | 3.4% / 1.18 / 24 | -0.6% / -0.28 / 18 | 8.0% / 1.92 / 24 | 9.8% / 2.15 / 34 | -0.6% / -0.11 / 15 |
| 25 | 0.7% / 0.53 / 17 | -1.9% / -1.05 / 29 | 6.9% / 2.11 / 29 | 5.1% / 1.98 / 35 | -0.0% / -0.00 / 19 |
| 26 | 0.8% / 0.60 / 17 | -1.9% / -1.05 / 29 | 6.5% / 2.03 / 29 | 5.1% / 1.99 / 35 | -0.8% / -0.33 / 19 |
| 27 | 3.1% / 1.04 / 39 | -1.4% / -0.46 / 30 | 4.1% / 0.97 / 40 | 15.4% / 2.84 / 46 | 1.8% / 0.38 / 25 |
| 28 | 1.2% / 0.46 / 40 | -0.9% / -0.36 / 28 | 5.5% / 1.32 / 39 | 9.6% / 1.92 / 45 | 1.5% / 0.33 / 25 |
| 29 | 1.2% / 0.46 / 40 | -0.9% / -0.36 / 28 | 5.5% / 1.32 / 39 | 9.6% / 1.92 / 45 | 1.5% / 0.33 / 25 |
| 30 | 2.2% / 0.50 / 24 | 2.1% / 0.53 / 20 | 13.0% / 1.70 / 12 | 9.3% / 1.33 / 24 | 0.9% / 0.15 / 33 |
| 31 | 4.5% / 1.37 / 27 | 0.2% / 0.09 / 18 | 3.9% / 0.99 / 26 | 12.0% / 2.40 / 30 | -0.6% / -0.12 / 15 |
| 32 | 1.9% / 0.79 / 18 | 0.6% / 0.35 / 19 | 2.0% / 0.64 / 26 | 5.5% / 1.90 / 24 | 1.6% / 0.54 / 20 |
| 33 | 1.9% / 0.79 / 18 | 0.6% / 0.35 / 19 | 2.0% / 0.64 / 26 | 5.5% / 1.90 / 24 | 1.6% / 0.54 / 20 |
| 34 | 1.9% / 0.45 / 24 | 2.1% / 0.53 / 20 | 13.1% / 1.70 / 12 | 9.3% / 1.33 / 24 | 0.9% / 0.15 / 33 |
| 35 | -0.6% / -0.09 / 30 | 0.1% / 0.05 / 14 | 4.1% / 0.57 / 13 | 11.6% / 2.13 / 16 | 10.5% / 1.26 / 30 |
| 36 | 3.1% / 1.37 / 23 | -0.8% / -0.46 / 18 | 8.2% / 1.91 / 26 | 6.3% / 1.89 / 27 | -1.5% / -0.32 / 19 |
| 37 | 2.3% / 1.13 / 26 | -0.4% / -0.29 / 16 | 4.4% / 1.38 / 24 | 6.0% / 1.89 / 28 | 0.5% / 0.20 / 21 |
| 38 | 2.3% / 1.13 / 26 | -0.4% / -0.29 / 16 | 4.4% / 1.38 / 24 | 6.0% / 1.89 / 28 | 0.5% / 0.20 / 21 |
| 39 | -1.1% / -0.08 / 44 | 9.6% / 1.57 / 26 | 14.8% / 1.16 / 27 | 13.3% / 1.52 / 29 | 9.1% / 0.84 / 43 |
| 40 | 0.5% / 0.10 / 37 | 11.6% / 1.87 / 23 | 13.4% / 1.12 / 24 | 9.9% / 1.19 / 28 | 5.9% / 0.57 / 47 |
| 41 | 5.4% / 1.95 / 26 | 0.1% / 0.04 / 18 | 7.9% / 1.82 / 26 | 4.3% / 1.09 / 31 | -0.9% / -0.21 / 15 |
| 42 | 5.4% / 1.95 / 26 | 0.2% / 0.13 / 18 | 7.9% / 1.82 / 26 | 4.3% / 1.09 / 31 | -0.9% / -0.21 / 15 |
| 43 | 3.9% / 1.68 / 31 | -1.6% / -0.96 / 27 | 5.7% / 1.78 / 33 | 5.5% / 1.71 / 39 | -0.4% / -0.12 / 23 |
| 44 | 4.7% / 1.36 / 27 | 0.4% / 0.16 / 18 | 4.0% / 1.02 / 26 | 11.0% / 2.31 / 30 | -0.6% / -0.12 / 15 |
| 45 | 4.7% / 1.78 / 31 | -1.8% / -1.07 / 27 | 5.2% / 1.66 / 33 | 5.5% / 1.69 / 39 | -1.2% / -0.42 / 23 |
| 46 | 0.7% / 0.12 / 37 | 12.2% / 1.93 / 23 | 13.3% / 1.12 / 24 | 10.3% / 1.23 / 28 | 4.7% / 0.47 / 47 |
| 47 | 0.6% / 0.14 / 43 | -1.2% / -0.48 / 22 | 21.0% / 2.13 / 36 | 8.5% / 1.82 / 48 | 0.9% / 0.18 / 38 |
| 48 | 2.0% / 0.41 / 43 | -1.4% / -0.54 / 22 | 20.0% / 2.10 / 36 | 8.6% / 1.84 / 48 | 1.4% / 0.26 / 38 |
| 49 | 2.0% / 1.09 / 23 | -0.7% / -0.35 / 18 | 6.7% / 1.68 / 26 | 6.7% / 1.80 / 27 | -1.2% / -0.25 / 19 |
| 50 | -0.5% / -0.01 / 44 | 10.0% / 1.61 / 26 | 15.9% / 1.22 / 27 | 13.3% / 1.51 / 29 | 9.0% / 0.84 / 43 |
| 51 | 1.1% / 0.43 / 31 | -0.7% / -0.34 / 14 | 3.2% / 0.84 / 18 | 9.8% / 2.00 / 25 | 1.6% / 0.33 / 17 |
| 52 | 1.5% / 0.56 / 31 | -0.7% / -0.33 / 14 | 3.2% / 0.84 / 18 | 10.4% / 2.05 / 25 | 0.2% / 0.08 / 17 |
| 53 | 1.6% / 0.73 / 17 | 0.5% / 0.22 / 19 | 5.8% / 1.44 / 24 | 5.4% / 1.38 / 22 | 1.8% / 0.44 / 20 |
| 54 | 0.4% / 0.17 / 28 | 0.7% / 0.36 / 24 | 4.9% / 1.22 / 33 | 8.7% / 1.88 / 30 | -1.2% / -0.30 / 15 |
| 55 | -0.7% / -0.12 / 25 | 2.9% / 0.68 / 18 | 6.6% / 0.70 / 11 | 10.5% / 1.54 / 20 | 8.4% / 0.97 / 30 |
| 56 | 3.5% / 0.85 / 39 | -0.2% / -0.07 / 18 | 6.1% / 1.50 / 28 | 6.2% / 1.34 / 34 | -0.6% / -0.12 / 17 |
| 57 | -6.4% / -1.06 / 26 | 7.0% / 1.17 / 19 | 16.4% / 1.66 / 16 | 16.3% / 2.11 / 18 | -2.2% / -0.18 / 31 |
| 58 | 0.5% / 0.21 / 28 | 0.9% / 0.42 / 24 | 4.4% / 1.13 / 33 | 8.6% / 1.87 / 30 | -0.6% / -0.14 / 15 |
| 59 | 2.1% / 0.93 / 17 | 0.7% / 0.28 / 19 | 4.8% / 1.24 / 24 | 5.7% / 1.42 / 22 | 1.4% / 0.36 / 20 |
| 60 | -5.2% / -0.86 / 25 | 8.1% / 1.19 / 20 | 19.6% / 1.73 / 20 | 13.5% / 1.76 / 19 | -0.9% / -0.02 / 35 |
| 61 | -6.4% / -1.06 / 26 | 7.0% / 1.17 / 19 | 16.4% / 1.66 / 16 | 16.3% / 2.11 / 18 | -2.2% / -0.18 / 31 |
| 62 | -5.6% / -0.95 / 24 | 8.9% / 1.27 / 20 | 19.5% / 1.72 / 20 | 13.5% / 1.76 / 19 | -1.1% / -0.03 / 35 |
| 63 | -0.7% / -0.12 / 25 | 2.9% / 0.68 / 18 | 6.6% / 0.70 / 11 | 10.5% / 1.54 / 20 | 7.7% / 0.89 / 31 |
| 64 | 2.5% / 0.95 / 35 | -0.9% / -0.48 / 30 | 4.9% / 1.45 / 36 | 6.0% / 2.21 / 42 | -0.4% / -0.10 / 33 |
| 65 | -10.5% / -1.66 / 106 | 0.2% / 0.06 / 77 | 23.8% / 1.86 / 85 | 5.7% / 0.91 / 93 | 17.4% / 2.17 / 111 |
| 66 | 0.5% / 0.10 / 37 | 2.8% / 0.51 / 27 | 17.6% / 1.76 / 25 | 5.0% / 0.59 / 36 | 8.1% / 0.76 / 45 |
| 67 | -2.4% / -0.81 / 41 | 1.0% / 0.51 / 32 | 8.9% / 1.32 / 44 | 9.3% / 1.99 / 46 | 0.3% / 0.10 / 30 |
| 68 | -2.4% / -0.81 / 41 | 1.0% / 0.51 / 32 | 8.9% / 1.32 / 44 | 9.3% / 1.99 / 46 | 0.3% / 0.10 / 30 |
| 69 | -0.0% / 0.00 / 38 | 0.6% / 0.30 / 30 | 6.8% / 0.99 / 42 | 11.0% / 2.27 / 44 | 2.3% / 0.45 / 29 |
| 70 | 2.2% / 0.89 / 35 | -0.8% / -0.47 / 30 | 4.5% / 1.35 / 36 | 6.1% / 2.22 / 42 | -0.4% / -0.10 / 33 |
| 71 | -11.1% / -1.76 / 106 | 0.5% / 0.14 / 76 | 21.0% / 1.82 / 85 | 6.5% / 1.01 / 93 | 17.3% / 2.16 / 111 |
| 72 | 5.6% / 1.04 / 59 | -2.5% / -0.64 / 47 | 3.3% / 0.78 / 48 | 18.5% / 2.79 / 56 | -3.0% / -0.48 / 39 |
| 73 | -2.2% / -0.19 / 44 | 9.2% / 1.56 / 24 | 1.2% / 0.19 / 24 | 8.8% / 1.04 / 32 | 17.2% / 1.42 / 48 |
| 74 | -0.8% / -0.25 / 38 | 0.4% / 0.25 / 30 | 7.6% / 1.13 / 42 | 9.9% / 2.12 / 44 | 1.7% / 0.36 / 29 |
| 75 | 6.7% / 1.16 / 59 | -2.6% / -0.64 / 47 | 3.6% / 0.85 / 48 | 17.4% / 2.69 / 56 | -2.6% / -0.42 / 39 |
| 76 | -4.5% / -0.76 / 83 | 5.0% / 1.55 / 75 | 21.1% / 1.38 / 79 | -2.1% / -0.32 / 87 | 18.9% / 2.21 / 94 |
| 77 | -4.7% / -0.81 / 83 | 5.0% / 1.58 / 75 | 24.0% / 1.46 / 79 | -2.3% / -0.36 / 87 | 16.0% / 2.01 / 94 |
| 78 | 1.7% / 0.58 / 57 | -2.0% / -0.88 / 47 | 4.3% / 1.34 / 46 | 8.5% / 2.78 / 67 | 0.4% / 0.13 / 37 |
| 79 | 2.4% / 0.75 / 57 | -1.9% / -0.86 / 47 | 3.8% / 1.21 / 46 | 8.4% / 2.78 / 67 | 0.4% / 0.13 / 37 |
| 80 | -3.4% / -0.63 / 23 | 9.4% / 1.49 / 19 | 14.3% / 1.64 / 14 | 1.5% / 0.21 / 27 | 11.7% / 1.25 / 30 |
| 81 | -3.5% / -0.64 / 23 | 9.8% / 1.54 / 19 | 14.4% / 1.65 / 14 | 1.7% / 0.23 / 27 | 10.3% / 1.10 / 30 |
| 82 | 5.9% / 1.66 / 41 | -2.0% / -0.76 / 34 | 5.2% / 1.87 / 38 | 4.4% / 1.28 / 50 | -0.4% / -0.09 / 27 |
| 83 | 5.9% / 1.66 / 41 | -2.0% / -0.76 / 34 | 5.4% / 1.89 / 38 | 4.4% / 1.28 / 50 | -0.4% / -0.09 / 27 |
| 84 | 1.2% / 0.83 / 17 | -0.6% / -0.30 / 29 | 7.5% / 1.74 / 29 | 7.1% / 2.04 / 36 | -1.9% / -0.55 / 21 |
| 85 | -8.5% / -1.65 / 63 | -1.8% / -0.34 / 66 | 26.0% / 1.90 / 64 | 8.6% / 1.43 / 63 | 10.0% / 1.21 / 96 |
| 86 | 1.6% / 0.41 / 50 | 0.2% / 0.06 / 33 | 5.2% / 0.82 / 42 | 13.2% / 2.39 / 42 | 1.6% / 0.32 / 28 |
| 87 | 1.0% / 0.72 / 17 | -0.6% / -0.28 / 29 | 7.5% / 1.74 / 29 | 7.1% / 2.04 / 36 | -1.9% / -0.55 / 21 |
| 88 | 3.8% / 0.59 / 73 | 7.3% / 1.55 / 73 | 13.9% / 0.78 / 68 | 19.3% / 2.07 / 75 | 0.0% / 0.06 / 79 |
| 89 | -1.5% / -0.47 / 76 | -3.1% / -1.47 / 59 | 9.2% / 1.95 / 66 | 8.9% / 2.73 / 75 | 1.2% / 0.35 / 49 |
| 90 | -1.5% / -0.47 / 76 | -3.1% / -1.47 / 59 | 9.2% / 1.95 / 66 | 8.9% / 2.73 / 75 | 1.2% / 0.35 / 49 |
| 91 | 2.4% / 1.20 / 15 | 0.5% / 0.40 / 16 | 5.6% / 1.36 / 18 | 5.2% / 1.61 / 31 | -1.1% / -0.26 / 25 |
| 92 | 1.6% / 1.10 / 15 | 0.7% / 0.49 / 16 | 5.5% / 1.33 / 18 | 5.2% / 1.60 / 31 | -1.1% / -0.28 / 25 |
| 93 | 3.7% / 1.11 / 40 | -2.3% / -1.08 / 32 | 7.8% / 2.69 / 42 | 4.7% / 1.31 / 45 | -1.2% / -0.34 / 24 |
| 94 | 1.2% / 0.31 / 50 | -0.3% / -0.05 / 33 | 3.6% / 0.70 / 42 | 13.6% / 2.38 / 42 | 2.7% / 0.46 / 28 |
| 95 | 3.7% / 1.11 / 40 | -2.3% / -1.08 / 32 | 7.8% / 2.69 / 42 | 4.7% / 1.31 / 45 | -1.2% / -0.34 / 24 |
| 96 | 2.2% / 0.30 / 37 | -5.3% / -1.22 / 22 | 20.0% / 1.77 / 24 | 6.4% / 0.85 / 23 | 12.0% / 0.95 / 35 |
| 97 | 4.0% / 0.50 / 37 | -5.2% / -1.20 / 22 | 19.8% / 1.78 / 24 | 7.4% / 0.93 / 23 | 11.1% / 0.89 / 35 |
| 98 | -8.1% / -1.54 / 63 | -1.8% / -0.34 / 66 | 22.6% / 1.74 / 64 | 8.3% / 1.42 / 63 | 12.4% / 1.46 / 96 |
| 99 | 3.0% / 0.54 / 28 | 5.7% / 1.37 / 17 | 11.6% / 1.16 / 17 | 0.8% / 0.14 / 23 | 9.1% / 0.95 / 31 |
| 100 | 1.8% / 0.52 / 123 | -1.1% / -0.48 / 107 | 17.6% / 1.76 / 107 | 4.3% / 1.17 / 121 | 0.9% / 0.17 / 138 |
| 101 | 1.6% / 0.47 / 123 | -1.2% / -0.54 / 107 | 17.8% / 1.78 / 107 | 5.3% / 1.39 / 122 | 0.1% / 0.05 / 138 |
| 102 | -8.4% / -1.22 / 137 | 2.3% / 0.47 / 117 | 26.0% / 1.43 / 117 | 16.7% / 1.74 / 154 | 6.1% / 0.61 / 137 |
| 103 | -7.3% / -1.05 / 107 | 3.9% / 0.77 / 105 | 27.3% / 1.70 / 105 | 13.9% / 1.53 / 127 | 5.8% / 0.70 / 117 |
| 104 | 0.5% / 0.14 / 29 | 9.1% / 2.25 / 24 | 5.5% / 0.42 / 26 | 19.9% / 2.94 / 31 | -1.7% / -0.18 / 40 |
| 105 | -0.2% / -0.02 / 109 | 3.5% / 1.02 / 87 | 19.6% / 1.38 / 96 | -0.8% / -0.13 / 117 | 7.3% / 1.39 / 126 |
| 106 | -0.2% / -0.02 / 109 | 3.6% / 1.05 / 87 | 18.5% / 1.35 / 96 | -0.7% / -0.10 / 117 | 7.1% / 1.37 / 126 |
| 107 | 2.4% / 0.63 / 84 | -1.6% / -0.83 / 47 | 4.8% / 1.32 / 58 | 7.2% / 2.25 / 69 | 1.2% / 0.32 / 50 |
| 108 | 2.4% / 0.63 / 84 | -1.6% / -0.83 / 47 | 4.8% / 1.32 / 58 | 7.2% / 2.25 / 69 | 1.2% / 0.32 / 50 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_6b02` | 6 | 1.00 | 1.00/1.00 | 0.99/1.00 |
| 1 | `cfg_98a3` | 18 | 0.84 | 0.79/0.92 | 0.49/0.94 |
| 2 | `cfg_5936` | 19 | 0.84 | 0.82/0.95 | 0.75/0.87 |
| 3 | `cfg_b00f` | 4 | 1.00 | 0.97/0.97 | 0.98/0.98 |
| 4 | `cfg_4471` | 20 | 0.85 | 0.75/0.87 | 0.64/0.69 |
| 5 | `cfg_a840` | 6 | 0.97 | 0.97/0.97 | 0.87/0.87 |
| 6 | `cfg_5087` | 35 | 0.81 | 0.66/0.85 | 0.35/0.54 |
| 7 | `cfg_b78b` | 8 | 0.95 | 0.91/0.99 | 0.82/0.97 |
| 8 | `cfg_28e7` | 9 | 0.86 | 0.85/0.87 | 0.77/0.79 |
| 9 | `cfg_055b` | 3 | 0.84 | 0.64/0.82 | 0.25/0.62 |
| 10 | `cfg_9583` | 12 | 0.97 | 0.97/0.97 | 0.94/0.95 |
| 11 | `cfg_076f` | 12 | 0.96 | 0.95/0.97 | 0.83/0.83 |
| 12 | `cfg_5cb3` | 6 | 0.99 | 1.00/1.00 | 0.99/0.99 |
| 13 | `cfg_683a` | 4 | 0.95 | 0.96/0.96 | 0.93/0.93 |
| 14 | `cfg_6a6f` | 7 | 0.91 | 0.91/0.96 | 0.79/0.95 |
| 15 | `cfg_cc4b` | 3 | 0.93 | 0.95/0.96 | 0.94/0.96 |
| 16 | `cfg_0b51` | 2 | 0.99 | 0.99/0.99 | 0.99/0.99 |
| 17 | `cfg_f092` | 6 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 18 | `cfg_0bf1` | 6 | 0.98 | 0.98/0.98 | 0.99/0.99 |
| 19 | `cfg_0e47` | 12 | 0.87 | 0.86/0.87 | 0.57/0.58 |
| 20 | `cfg_f0c4` | 6 | 0.98 | 0.99/1.00 | 0.98/0.98 |
| 21 | `cfg_3ae7` | 4 | 0.96 | 0.96/0.96 | 0.81/0.82 |
| 22 | `cfg_455a` | 12 | 0.82 | 0.84/0.87 | 0.78/0.80 |
| 23 | `cfg_1ecb` | 6 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 24 | `cfg_8d16` | 8 | 0.93 | 0.89/0.97 | 0.65/0.92 |
| 25 | `cfg_4be8` | 18 | 0.84 | 0.80/0.93 | 0.75/0.80 |
| 26 | `cfg_c4f3` | 7 | 0.89 | 0.90/0.99 | 0.78/0.96 |
| 27 | `cfg_8130` | 6 | 0.99 | 0.99/0.99 | 1.00/1.00 |
| 28 | `cfg_18de` | 4 | 0.99 | 0.99/1.00 | 0.99/1.00 |
| 29 | `cfg_e19a` | 12 | 0.96 | 0.95/0.97 | 0.92/0.94 |
| 30 | `cfg_1b20` | 1 | n/a | n/a/n/a | n/a/n/a |
| 31 | `cfg_cac3` | 12 | 0.86 | 0.83/0.83 | 0.66/0.66 |
| 32 | `cfg_57c7` | 6 | 0.81 | 0.82/0.87 | 0.75/0.79 |
| 33 | `cfg_2699` | 6 | 0.99 | 0.99/0.99 | 1.00/1.00 |
| 34 | `cfg_6955` | 6 | 0.98 | 0.98/0.99 | 0.98/0.98 |
| 35 | `cfg_ef5d` | 12 | 0.87 | 0.88/0.88 | 0.56/0.57 |
| 36 | `cfg_6b3b` | 8 | 0.91 | 0.80/0.95 | 0.60/0.84 |
| 37 | `cfg_7dd4` | 6 | 0.98 | 0.98/0.98 | 0.97/0.99 |
| 38 | `cfg_c52c` | 4 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 39 | `cfg_2fd7` | 3 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 40 | `cfg_ad36` | 4 | 0.97 | 0.96/0.99 | 0.95/1.00 |
| 41 | `cfg_3387` | 4 | 0.97 | 0.97/0.99 | 0.97/0.97 |
| 42 | `cfg_366e` | 6 | 1.00 | 1.00/1.00 | 0.99/1.00 |
| 43 | `cfg_35ac` | 2 | 0.99 | 0.99/0.99 | 0.98/0.98 |
| 44 | `cfg_35c5` | 3 | 0.99 | 0.99/0.99 | 0.99/1.00 |
| 45 | `cfg_84db` | 6 | 0.92 | 0.94/0.98 | 0.93/0.98 |
| 46 | `cfg_b2f5` | 13 | 0.84 | 0.80/0.94 | 0.44/0.92 |
| 47 | `cfg_42be` | 1 | n/a | n/a/n/a | n/a/n/a |
| 48 | `cfg_4d5e` | 6 | 0.95 | 0.95/0.98 | 0.97/0.99 |
| 49 | `cfg_53f1` | 3 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 50 | `cfg_6376` | 1 | n/a | n/a/n/a | n/a/n/a |
| 51 | `cfg_76a5` | 1 | n/a | n/a/n/a | n/a/n/a |
| 52 | `cfg_8b81` | 6 | 1.00 | 1.00/1.00 | 0.99/0.99 |
| 53 | `cfg_822c` | 3 | 0.99 | 1.00/1.00 | 0.97/0.98 |
| 54 | `cfg_8639` | 4 | 0.99 | 0.99/1.00 | 0.98/0.99 |
| 55 | `cfg_9c3c` | 1 | n/a | n/a/n/a | n/a/n/a |
| 56 | `cfg_d4d4` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 7.519e-04 over 78894 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1063.0, participation ratio 30.0, 95%-variance components 202 (rank bound T = 1259); raw grid 84672; raw + known prior 858120
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
ES results are unchanged rules on the development period: supporting evidence, not an independent replication.

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
- Session: each root's day session only (src/data/futures.py SESSIONS: NYSE 09:30-16:00 NY for equity indexes, 09:00-14:30 NY for crude, 08:20-13:30 NY for gold, 08:20-15:00 NY for FX; sessions under 5% of normal volume are skipped), on NYSE trading days; overnight Globex bars are not traded or used in indicators.
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
