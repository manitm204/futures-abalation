# Screening funnel -- mr_cl_v5 (development stages only)

- Code: `5342a94cdc84` (dirty working tree: True, diff sha256 `11095209c92a`)
- Config: `configs/funnel/mr_funnel_cl_v5.yaml` sha256 `072bebe0312d3a37`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'CL': '2026-10-16'}
- Frozen manifest sha256: `7045f0b6b821c067` (75 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **False** -- No strategy has been tested on CL before. The v5 grid, the stage-4 test and the 40-trade rule were chosen after reading ES (and NQ/YM/RTY) results, a different asset class, so CL 2023-2024 is close to a fresh check.
- Holdout 2025+ previously inspected: **False** -- No CL strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 41472 | 41472 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 41472 | 41472 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 41472 | 28617 | 12855 | 0 |  | 32689 | 69.00 | 69.00 |  |
| 3 performance & risk | hard_gate | 28617 | 377 | 28240 | 0 |  | 0 | 0.91 | 1.32 |  |
| 4 parameter stability | hard_gate | 377 | 360 | 17 | 0 |  | 0 | 0.87 | 95.49 |  |
| 5 time stability | hard_gate | 360 | 356 | 4 | 0 |  | 305 | 0.86 | 98.89 |  |
| 6 deduplication | dedup | 356 | 75 |  |  | 281 |  | 0.18 | 21.07 | best 2 per cluster |
| 7 execution stress | hard_gate | 75 | 75 | 0 | 0 |  | 9 | 0.18 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 75 |  |  |  |  |  |  |  | diagnostic only: unverified: 75 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 12855 |
| s2:hard_reject:years_with_>=10_trades | 8678 |
| s3:hard_reject:max_drawdown | 18607 |
| s3:hard_reject:net_return | 20826 |
| s3:hard_reject:sharpe | 28222 |
| s4:hard_reject:local_median_sharpe | 17 |
| s5:hard_reject:profitable_years | 4 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | transfer dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_2258` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 44/137/224 | 405 | 190.2% | 23.8% | 1.08 | -23.4% | 135 | 1.57 | 9.6% | 60.6 | 11/11 | 0.82 | 0.77 | 0.30 | 5 | 60.1% | 0.48 | 0.64 | 163.1% | 140.7% | 15.1% | 166.0%/94.8% | 6.8 (interpolated) | pass | 0.099 (unverified) | n/a |
| 2 | `cfg_f9a8` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 72/88/192 | 352 | 157.7% | 20.9% | 1.22 | -14.7% | 171 | 1.60 | 7.7% | 51.5 | 11/11 | 0.82 | 0.82 | 0.40 | 5 | 65.1% | 0.41 | 0.58 | 138.5% | 119.8% | 41.8% | 144.7%/85.3% | 7.0 (interpolated) | pass | 0.157 (unverified) | n/a |
| 3 | `cfg_acfe` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 55/105/192 | 352 | 155.8% | 20.7% | 1.22 | -14.7% | 135 | 1.60 | 8.0% | 51.6 | 11/11 | 0.82 | 0.84 | 0.38 | 5 | 67.4% | 0.39 | 0.57 | 136.1% | 118.6% | 42.6% | 137.6%/105.0% | 6.9 (interpolated) | pass | 0.161 (unverified) | n/a |
| 4 | `cfg_103b` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 33/148/224 | 405 | 200.8% | 24.7% | 1.11 | -23.3% | 171 | 1.59 | 9.8% | 60.8 | 10/10 | 0.80 | 0.70 | 0.40 | 5 | 66.2% | 0.47 | 0.62 | 173.4% | 147.3% | 20.3% | 173.1%/102.3% | 7.0 (interpolated) | pass | 0.112 (unverified) | n/a |
| 5 | `cfg_c64c` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 2/165/96 | 263 | 53.9% | 9.0% | 1.30 | -5.9% | 326 | 1.57 | 4.5% | 40.6 | 8/8 | 0.75 | 0.37 | 0.93 | 5 | 28.4% | 0.42 | 0.44 | 45.4% | 37.1% | 14.0% | 49.1%/38.0% | 4.7 (interpolated) | pass | 0.257 (unverified) | n/a |
| 6 | `cfg_fff2` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 3/164/96 | 263 | 53.9% | 9.0% | 1.30 | -5.9% | 326 | 1.57 | 4.5% | 40.6 | 9/9 | 0.78 | 0.40 | 0.90 | 5 | 28.4% | 0.42 | 0.44 | 45.4% | 37.1% | 14.1% | 49.4%/39.4% | 4.7 (interpolated) | pass | 0.257 (unverified) | n/a |
| 7 | `cfg_39ee` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 26/195/52 | 273 | 155.3% | 20.6% | 1.09 | -13.5% | 263 | 1.79 | 5.3% | 39.5 | 12/12 | 0.75 | 0.85 | 0.23 | 4 | 41.7% | 0.53 | 0.60 | 139.4% | 124.6% | 66.9% | 137.3%/88.8% | 8.3 (interpolated) | pass | 0.062 (unverified) | n/a |
| 8 | `cfg_5bc0` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 44/178/51 | 273 | 154.7% | 20.6% | 1.09 | -13.5% | 263 | 1.80 | 5.2% | 39.3 | 11/11 | 0.73 | 0.82 | 0.26 | 4 | 39.7% | 0.54 | 0.60 | 139.2% | 123.3% | 66.9% | 137.3%/74.9% | 8.2 (interpolated) | pass | 0.061 (unverified) | n/a |
| 9 | `cfg_2a9c` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 34/100/167 | 301 | 147.4% | 19.9% | 1.11 | -20.0% | 206 | 1.64 | 6.9% | 41.0 | 11/11 | 0.91 | 0.92 | 0.19 | 5 | 46.7% | 0.52 | 0.68 | 130.3% | 114.2% | 35.0% | 135.7%/66.1% | 7.4 (interpolated) | pass | 0.178 (unverified) | n/a |
| 10 | `cfg_7b3b` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=20, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 48/87/166 | 301 | 152.7% | 20.4% | 1.13 | -20.0% | 206 | 1.66 | 6.7% | 40.8 | 11/11 | 0.91 | 0.94 | 0.18 | 5 | 45.0% | 0.53 | 0.67 | 135.2% | 119.2% | 39.7% | 135.5%/96.2% | 7.5 (interpolated) | pass | 0.184 (unverified) | n/a |
| 11 | `cfg_cb6e` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 10/58/37 | 105 | 28.6% | 5.2% | 1.03 | -6.1% | 337 | 1.77 | 1.7% | 14.7 | 10/10 | 0.80 | 0.78 | 0.25 | 5 | 11.4% | 0.60 | 0.66 | 25.1% | 22.1% | 28.6% | 27.0%/18.9% | 6.0 (interpolated) | pass | 0.094 (unverified) | n/a |
| 12 | `cfg_430b` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=80, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 9/131/84 | 224 | 36.6% | 6.4% | 1.01 | -9.5% | 584 | 1.50 | 3.8% | 32.2 | 10/10 | 0.90 | 0.65 | 0.36 | 3 | 12.7% | 0.59 | 0.58 | 30.9% | 23.6% | 17.0% | 31.7%/20.1% | 4.1 (interpolated) | pass | 0.085 (unverified) | n/a |
| 13 | `cfg_8096` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=80, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 5/135/84 | 224 | 36.7% | 6.5% | 1.02 | -9.5% | 584 | 1.50 | 3.8% | 32.3 | 10/10 | 0.90 | 0.70 | 0.32 | 3 | 12.9% | 0.59 | 0.58 | 30.9% | 23.6% | 17.8% | 32.2%/20.8% | 4.1 (interpolated) | pass | 0.086 (unverified) | n/a |
| 14 | `cfg_e686` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 6/62/37 | 105 | 28.7% | 5.2% | 1.03 | -6.2% | 338 | 1.77 | 1.7% | 14.7 | 11/11 | 0.82 | 0.78 | 0.25 | 5 | 11.5% | 0.60 | 0.66 | 25.1% | 22.2% | 27.0% | 25.7%/19.9% | 6.0 (interpolated) | pass | 0.095 (unverified) | n/a |
| 15 | `cfg_92a1` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 113/34/147 | 294 | 102.0% | 15.1% | 1.01 | -18.6% | 226 | 1.60 | 5.5% | 45.2 | 11/11 | 0.82 | 0.66 | 0.35 | 5 | 57.2% | 0.44 | 0.66 | 88.2% | 76.5% | 7.8% | 93.8%/64.0% | 6.3 (interpolated) | pass | 0.109 (unverified) | n/a |
| 16 | `cfg_b8e8` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 35/114/33 | 182 | 129.3% | 18.1% | 0.91 | -12.5% | 239 | 2.05 | 3.4% | 23.0 | 11/11 | 0.82 | 0.76 | 0.15 | 4 | 18.3% | 0.73 | 0.81 | 119.0% | 109.1% | 41.1% | 116.8%/55.3% | 10.2 (interpolated) | pass | 0.042 (unverified) | n/a |
| 17 | `cfg_1166` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 61/286/280 | 627 | 125.8% | 17.7% | 0.91 | -14.1% | 291 | 1.30 | 9.7% | 89.9 | 11/11 | 0.82 | 0.81 | 0.09 | 4 | 29.6% | 0.66 | 0.82 | 95.1% | 69.0% | 18.4% | 106.5%/72.5% | 3.9 (interpolated) | pass | 0.028 (unverified) | n/a |
| 18 | `cfg_8a27` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 47/300/280 | 627 | 126.3% | 17.8% | 0.91 | -14.4% | 291 | 1.31 | 9.8% | 90.1 | 10/10 | 0.80 | 0.82 | 0.09 | 5 | 29.8% | 0.65 | 0.80 | 96.1% | 69.3% | 17.9% | 112.8%/55.0% | 3.9 (interpolated) | pass | 0.028 (unverified) | n/a |
| 19 | `cfg_60d4` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 151/5/143 | 299 | 69.3% | 11.1% | 0.86 | -19.3% | 226 | 1.45 | 4.4% | 46.6 | 10/10 | 0.70 | 0.64 | 0.22 | 4 | 38.9% | 0.44 | 0.82 | 57.9% | 47.9% | -6.4% | 67.3%/41.7% | 5.0 (interpolated) | pass | 0.082 (unverified) | n/a |
| 20 | `cfg_4a55` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 95/174/322 | 591 | 156.3% | 20.7% | 0.95 | -21.5% | 141 | 1.29 | 13.7% | 92.7 | 10/10 | 0.70 | 0.77 | 0.18 | 5 | 112.3% | 0.28 | 0.66 | 121.5% | 95.4% | 84.8% | 132.1%/91.3% | 4.6 (interpolated) | pass | 0.075 (unverified) | n/a |
| 21 | `cfg_3fcb` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 124/138/216 | 478 | 89.4% | 13.7% | 0.81 | -27.6% | 234 | 1.36 | 6.7% | 71.1 | 10/10 | 0.70 | 0.76 | 0.05 | 5 | 54.3% | 0.39 | 0.76 | 69.1% | 50.4% | 33.6% | 85.0%/35.4% | 3.9 (interpolated) | pass | 0.031 (unverified) | n/a |
| 22 | `cfg_5a08` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 69/145/261 | 475 | 133.6% | 18.5% | 1.02 | -23.2% | 221 | 1.41 | 10.6% | 71.8 | 10/10 | 0.90 | 0.72 | 0.30 | 5 | 76.8% | 0.42 | 0.59 | 109.4% | 86.8% | 18.7% | 116.4%/75.1% | 5.0 (interpolated) | pass | 0.076 (unverified) | n/a |
| 23 | `cfg_3590` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 48/208/222 | 478 | 106.8% | 15.7% | 0.84 | -27.8% | 252 | 1.41 | 7.2% | 71.1 | 11/11 | 0.73 | 0.82 | 0.02 | 5 | 67.6% | 0.37 | 0.71 | 84.1% | 64.8% | 52.2% | 101.3%/58.3% | 4.3 (interpolated) | pass | 0.028 (unverified) | n/a |
| 24 | `cfg_7223` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 21/105/75 | 201 | 32.1% | 5.7% | 0.80 | -15.3% | 562 | 1.39 | 3.3% | 29.8 | 10/10 | 0.80 | 0.50 | 0.31 | 3 | 12.7% | 0.61 | 0.77 | 26.1% | 19.8% | 16.1% | 29.1%/20.0% | 4.0 (interpolated) | pass | 0.051 (unverified) | n/a |
| 25 | `cfg_cd10` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 88/126/261 | 475 | 122.9% | 17.4% | 0.97 | -23.4% | 221 | 1.39 | 10.2% | 71.8 | 11/11 | 0.91 | 0.78 | 0.19 | 5 | 68.6% | 0.44 | 0.62 | 100.3% | 79.6% | 12.2% | 112.8%/71.0% | 4.8 (interpolated) | pass | 0.061 (unverified) | n/a |
| 26 | `cfg_ce65` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 28/134/102 | 264 | 40.6% | 7.1% | 0.91 | -9.1% | 451 | 1.41 | 4.3% | 40.1 | 11/11 | 0.82 | 0.42 | 0.49 | 4 | 17.8% | 0.56 | 0.66 | 32.8% | 25.4% | 16.0% | 38.8%/29.8% | 3.9 (interpolated) | pass | 0.081 (unverified) | n/a |
| 27 | `cfg_fd85` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 13/148/103 | 264 | 41.6% | 7.2% | 0.92 | -10.6% | 451 | 1.42 | 4.3% | 40.1 | 12/12 | 0.83 | 0.57 | 0.35 | 4 | 16.6% | 0.60 | 0.67 | 33.9% | 25.7% | 17.7% | 43.2%/30.3% | 4.0 (interpolated) | pass | 0.082 (unverified) | n/a |
| 28 | `cfg_5c1e` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 136/73/252 | 461 | 164.2% | 21.5% | 0.90 | -29.9% | 221 | 1.41 | 9.7% | 67.2 | 11/11 | 0.82 | 0.71 | 0.19 | 5 | 67.4% | 0.38 | 0.70 | 137.7% | 111.5% | 50.2% | 159.4%/88.9% | 5.5 (interpolated) | pass | 0.031 (unverified) | n/a |
| 29 | `cfg_0a51` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 48/193/208 | 449 | 99.8% | 14.9% | 0.84 | -19.1% | 248 | 1.37 | 6.8% | 64.2 | 10/10 | 0.80 | 0.61 | 0.23 | 5 | 33.2% | 0.54 | 0.93 | 81.5% | 63.2% | 33.9% | 92.6%/49.9% | 4.5 (interpolated) | pass | 0.023 (unverified) | n/a |
| 30 | `cfg_22be` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 12/114/75 | 201 | 32.5% | 5.8% | 0.81 | -15.3% | 562 | 1.39 | 3.4% | 29.8 | 11/11 | 0.82 | 0.52 | 0.30 | 3 | 13.2% | 0.59 | 0.76 | 26.9% | 20.7% | 16.5% | 29.3%/21.7% | 4.0 (interpolated) | pass | 0.053 (unverified) | n/a |
| 31 | `cfg_508a` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 40/61/70 | 171 | 74.6% | 11.8% | 0.85 | -9.4% | 210 | 1.87 | 2.6% | 25.4 | 12/12 | 0.83 | 0.62 | 0.24 | 4 | 32.1% | 0.45 | 0.85 | 68.3% | 61.9% | -5.2% | 70.1%/51.0% | 8.2 (interpolated) | pass | 0.049 (unverified) | n/a |
| 32 | `cfg_9cd1` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 61/180/208 | 449 | 104.0% | 15.4% | 0.81 | -19.3% | 248 | 1.38 | 6.7% | 63.8 | 11/11 | 0.82 | 0.78 | 0.03 | 5 | 31.4% | 0.57 | 0.95 | 84.0% | 65.9% | 35.0% | 99.1%/56.4% | 4.6 (interpolated) | pass | 0.013 (unverified) | n/a |
| 33 | `cfg_e424` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 121/155/330 | 606 | 117.6% | 16.9% | 0.90 | -14.7% | 245 | 1.24 | 13.4% | 91.5 | 11/11 | 0.82 | 0.78 | 0.13 | 5 | 49.4% | 0.45 | 0.80 | 87.9% | 66.0% | -8.5% | 103.2%/46.3% | 3.9 (interpolated) | pass | 0.043 (unverified) | n/a |
| 34 | `cfg_0f01` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 114/160/319 | 593 | 152.0% | 20.3% | 0.93 | -21.7% | 111 | 1.29 | 13.3% | 93.0 | 11/11 | 0.82 | 0.76 | 0.17 | 5 | 106.3% | 0.30 | 0.67 | 119.7% | 93.3% | 79.4% | 134.3%/78.9% | 4.6 (interpolated) | pass | 0.072 (unverified) | n/a |
| 35 | `cfg_429c` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=80, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 4/151/28 | 183 | 29.6% | 5.3% | 0.81 | -10.9% | 686 | 1.46 | 3.7% | 25.9 | 11/11 | 0.91 | 0.60 | 0.22 | 4 | 12.9% | 0.57 | 0.67 | 24.6% | 19.1% | 24.8% | 24.2%/17.2% | 4.1 (interpolated) | pass | 0.037 (unverified) | n/a |
| 36 | `cfg_89b9` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=80, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 1/154/28 | 183 | 29.6% | 5.3% | 0.81 | -10.9% | 686 | 1.46 | 3.7% | 25.9 | 10/10 | 0.90 | 0.57 | 0.24 | 3 | 12.8% | 0.57 | 0.67 | 24.5% | 19.1% | 24.2% | 24.6%/13.1% | 4.1 (interpolated) | pass | 0.037 (unverified) | n/a |
| 37 | `cfg_0729` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 14/106/87 | 207 | 35.8% | 6.3% | 0.91 | -9.9% | 334 | 1.45 | 3.3% | 29.5 | 10/10 | 0.70 | 0.54 | 0.37 | 4 | 21.1% | 0.41 | 0.62 | 29.8% | 24.0% | 9.5% | 33.0%/24.8% | 4.3 (interpolated) | pass | 0.081 (unverified) | n/a |
| 38 | `cfg_087a` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 55/46/70 | 171 | 67.0% | 10.8% | 0.86 | -9.5% | 210 | 1.79 | 2.4% | 25.2 | 11/11 | 0.64 | 0.43 | 0.43 | 4 | 29.8% | 0.44 | 0.86 | 60.2% | 54.2% | -10.3% | 61.0%/49.0% | 7.6 (interpolated) | pass | 0.063 (unverified) | n/a |
| 39 | `cfg_53cc` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 61/170/63 | 294 | 102.4% | 15.2% | 0.79 | -17.3% | 140 | 1.46 | 5.4% | 41.1 | 12/12 | 0.83 | 0.65 | 0.14 | 5 | 40.2% | 0.51 | 0.90 | 88.8% | 75.7% | 37.4% | 90.2%/49.0% | 6.0 (interpolated) | pass | 0.008 (unverified) | n/a |
| 40 | `cfg_12d7` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 66/125/88 | 279 | 98.4% | 14.7% | 0.80 | -28.1% | 240 | 1.44 | 8.2% | 42.3 | 12/12 | 0.83 | 0.67 | 0.13 | 5 | 48.3% | 0.35 | 0.68 | 84.7% | 72.0% | 30.5% | 89.1%/34.0% | 6.2 (interpolated) | pass | 0.037 (unverified) | n/a |
| 41 | `cfg_869a` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=30, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 33/210/170 | 413 | 43.7% | 7.5% | 0.85 | -11.9% | 351 | 1.28 | 6.6% | 66.5 | 11/11 | 0.82 | 0.60 | 0.25 | 4 | 18.0% | 0.59 | 0.56 | 31.4% | 20.6% | 22.0% | 39.8%/30.1% | 3.0 (interpolated) | pass | 0.053 (unverified) | n/a |
| 42 | `cfg_23ca` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 95/179/332 | 606 | 116.0% | 16.7% | 0.89 | -16.1% | 245 | 1.24 | 13.8% | 91.2 | 10/10 | 0.90 | 0.72 | 0.17 | 5 | 49.3% | 0.46 | 0.82 | 87.7% | 64.5% | -7.3% | 99.2%/46.7% | 3.9 (interpolated) | pass | 0.042 (unverified) | n/a |
| 43 | `cfg_7b29` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 38/53/69 | 160 | 77.8% | 12.2% | 0.77 | -26.3% | 248 | 1.49 | 8.9% | 26.7 | 7/7 | 0.71 | 0.22 | 0.55 | 4 | 31.4% | 0.60 | 0.86 | 72.4% | 66.1% | 51.3% | 69.9%/48.5% | 9.4 (interpolated) | pass | 0.017 (unverified) | n/a |
| 44 | `cfg_107b` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 62/131/174 | 367 | 94.0% | 14.2% | 0.76 | -20.8% | 215 | 1.44 | 5.3% | 51.9 | 11/11 | 0.82 | 0.76 | -0.00 | 5 | 39.7% | 0.45 | 0.89 | 77.9% | 63.2% | 39.6% | 97.1%/69.9% | 5.0 (interpolated) | pass | 0.010 (unverified) | n/a |
| 45 | `cfg_801a` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=30, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 23/220/170 | 413 | 43.9% | 7.6% | 0.85 | -11.7% | 351 | 1.28 | 6.6% | 66.5 | 10/10 | 0.80 | 0.59 | 0.26 | 4 | 17.4% | 0.60 | 0.57 | 31.9% | 21.7% | 21.7% | 38.6%/27.5% | 3.0 (interpolated) | pass | 0.053 (unverified) | n/a |
| 46 | `cfg_0e4d` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 48/143/88 | 279 | 96.7% | 14.5% | 0.79 | -28.4% | 241 | 1.43 | 8.5% | 42.5 | 12/12 | 0.83 | 0.61 | 0.18 | 5 | 58.2% | 0.34 | 0.67 | 84.7% | 72.9% | 31.8% | 86.2%/52.2% | 6.3 (interpolated) | pass | 0.037 (unverified) | n/a |
| 47 | `cfg_bde6` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=30, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 22/64/60 | 146 | 22.9% | 4.2% | 0.85 | -7.8% | 486 | 1.48 | 2.2% | 19.6 | 11/11 | 0.73 | 0.61 | 0.24 | 3 | 8.6% | 0.58 | 0.63 | 19.1% | 14.8% | 2.6% | 21.0%/16.6% | 4.0 (interpolated) | pass | 0.059 (unverified) | n/a |
| 48 | `cfg_5484` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=20, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 58/144/267 | 469 | 103.2% | 15.3% | 0.81 | -18.8% | 304 | 1.30 | 10.8% | 69.8 | 10/10 | 0.80 | 0.71 | 0.11 | 5 | 64.7% | 0.37 | 0.91 | 82.0% | 64.4% | 3.1% | 91.7%/48.4% | 4.4 (interpolated) | pass | 0.035 (unverified) | n/a |
| 49 | `cfg_c606` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=25, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 32/88/87 | 207 | 34.4% | 6.1% | 0.89 | -10.0% | 329 | 1.43 | 3.2% | 29.5 | 11/11 | 0.73 | 0.66 | 0.23 | 4 | 17.9% | 0.42 | 0.64 | 27.8% | 22.4% | 10.0% | 30.3%/22.3% | 4.1 (interpolated) | pass | 0.075 (unverified) | n/a |
| 50 | `cfg_8990` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=30, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 12/74/60 | 146 | 22.1% | 4.1% | 0.83 | -7.7% | 491 | 1.47 | 2.3% | 19.6 | 12/12 | 0.75 | 0.72 | 0.10 | 3 | 7.7% | 0.61 | 0.65 | 18.4% | 14.2% | 2.1% | 19.5%/15.0% | 4.0 (interpolated) | pass | 0.054 (unverified) | n/a |
| 51 | `cfg_e515` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 28/213/0 | 241 | 99.4% | 14.8% | 0.84 | -25.9% | 249 | 1.63 | 5.1% | 36.5 | 11/11 | 0.82 | 0.58 | 0.26 | 4 | 46.0% | 0.38 | 0.57 | 91.3% | 79.2% | 154.0% | 86.6%/52.1% | 7.3 (interpolated) | pass | 0.054 (unverified) | n/a |
| 52 | `cfg_08e5` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 35/206/0 | 241 | 97.8% | 14.6% | 0.83 | -25.9% | 249 | 1.61 | 5.0% | 36.4 | 11/11 | 0.82 | 0.56 | 0.27 | 4 | 44.8% | 0.39 | 0.58 | 89.2% | 77.6% | 153.0% | 85.4%/60.0% | 7.2 (interpolated) | pass | 0.052 (unverified) | n/a |
| 53 | `cfg_094c` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 50/264/88 | 402 | 101.1% | 15.0% | 0.81 | -24.5% | 252 | 1.37 | 7.6% | 58.0 | 11/11 | 0.73 | 0.41 | 0.40 | 5 | 32.8% | 0.54 | 0.87 | 83.8% | 67.7% | 44.5% | 85.6%/53.4% | 4.9 (interpolated) | pass | 0.015 (unverified) | n/a |
| 54 | `cfg_d998` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 110/100/274 | 484 | 137.0% | 18.9% | 0.87 | -22.0% | 208 | 1.32 | 10.6% | 68.8 | 10/10 | 0.70 | 0.50 | 0.38 | 5 | 53.3% | 0.47 | 0.84 | 111.0% | 88.2% | 43.8% | 123.7%/68.4% | 4.9 (interpolated) | pass | 0.035 (unverified) | n/a |
| 55 | `cfg_a03f` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 94/222/86 | 402 | 83.0% | 12.9% | 0.77 | -23.7% | 252 | 1.33 | 7.3% | 57.7 | 12/12 | 0.75 | 0.49 | 0.29 | 5 | 31.4% | 0.51 | 0.92 | 66.3% | 52.3% | 24.7% | 73.4%/45.8% | 4.4 (interpolated) | pass | 0.018 (unverified) | n/a |
| 56 | `cfg_63e4` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 75/153/277 | 505 | 119.2% | 17.0% | 0.82 | -19.2% | 425 | 1.26 | 12.0% | 76.0 | 10/10 | 0.80 | 0.43 | 0.39 | 5 | 80.2% | 0.33 | 0.94 | 96.4% | 75.5% | 54.6% | 111.1%/71.4% | 4.5 (interpolated) | pass | 0.038 (unverified) | n/a |
| 57 | `cfg_dcd2` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 93/116/275 | 484 | 113.3% | 16.4% | 0.82 | -22.0% | 208 | 1.28 | 11.0% | 69.4 | 11/11 | 0.73 | 0.50 | 0.32 | 5 | 54.6% | 0.40 | 0.89 | 89.7% | 70.7% | 29.4% | 104.4%/59.4% | 4.4 (interpolated) | pass | 0.038 (unverified) | n/a |
| 58 | `cfg_d193` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 51/52/96 | 199 | 39.8% | 6.9% | 0.79 | -14.5% | 549 | 1.39 | 4.7% | 29.4 | 10/10 | 0.80 | 0.51 | 0.28 | 4 | 14.8% | 0.63 | 0.74 | 33.2% | 27.7% | 11.0% | 34.9%/22.8% | 4.7 (interpolated) | pass | 0.058 (unverified) | n/a |
| 59 | `cfg_1961` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 84/166/114 | 364 | 109.1% | 15.9% | 0.82 | -22.3% | 337 | 1.36 | 10.8% | 56.2 | 13/13 | 0.69 | 0.47 | 0.35 | 4 | 45.9% | 0.42 | 0.71 | 94.8% | 76.8% | -5.6% | 90.5%/46.9% | 5.6 (interpolated) | pass | 0.041 (unverified) | n/a |
| 60 | `cfg_efc3` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 61/139/258 | 458 | 98.8% | 14.8% | 0.75 | -29.9% | 263 | 1.27 | 10.9% | 66.4 | 11/11 | 0.82 | 0.65 | 0.10 | 5 | 52.0% | 0.41 | 0.89 | 78.5% | 61.5% | 26.6% | 94.8%/53.2% | 4.2 (interpolated) | pass | 0.036 (unverified) | n/a |
| 61 | `cfg_2c94` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 18/82/10 | 110 | 23.5% | 4.3% | 0.77 | -7.8% | 242 | 1.54 | 2.2% | 13.7 | 11/11 | 0.82 | 0.45 | 0.31 | 5 | 13.8% | 0.38 | 0.80 | 20.3% | 17.0% | 13.5% | 21.4%/14.0% | 4.8 (interpolated) | pass | 0.056 (unverified) | n/a |
| 62 | `cfg_a493` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 100/104/255 | 459 | 99.0% | 14.8% | 0.75 | -30.0% | 209 | 1.28 | 10.3% | 67.1 | 12/12 | 0.83 | 0.68 | 0.07 | 5 | 63.1% | 0.36 | 0.87 | 78.7% | 59.7% | 28.1% | 99.3%/60.8% | 4.2 (interpolated) | pass | 0.036 (unverified) | n/a |
| 63 | `cfg_cc63` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 74/285/387 | 746 | 141.5% | 19.3% | 0.88 | -22.9% | 477 | 1.27 | 10.6% | 113.3 | 11/11 | 0.55 | 0.30 | 0.58 | 4 | 12.6% | 0.73 | 0.80 | 103.1% | 72.6% | 82.8% | 120.6%/62.1% | 3.7 (interpolated) | pass | 0.045 (unverified) | n/a |
| 64 | `cfg_1c51` | timeframe=5min, mean_type=ema, mean_lookback=50, std_lookback=60, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 99/141/0 | 240 | 36.6% | 6.5% | 0.82 | -7.5% | 409 | 1.42 | 2.8% | 34.4 | 10/10 | 0.80 | 0.39 | 0.42 | 4 | 0.7% | 0.96 | 0.77 | 29.2% | 22.4% | 33.7% | 35.5%/27.3% | 3.9 (interpolated) | pass | 0.043 (unverified) | n/a |
| 65 | `cfg_ed83` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 7/93/10 | 110 | 23.7% | 4.3% | 0.77 | -8.7% | 245 | 1.55 | 2.2% | 13.8 | 12/12 | 0.83 | 0.39 | 0.37 | 5 | 15.3% | 0.32 | 0.79 | 20.4% | 17.4% | 11.4% | 22.2%/14.5% | 4.9 (interpolated) | pass | 0.056 (unverified) | n/a |
| 66 | `cfg_6d7c` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=15, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 122/151/314 | 587 | 95.9% | 14.4% | 0.76 | -21.4% | 148 | 1.20 | 13.0% | 94.1 | 11/11 | 0.91 | 0.50 | 0.26 | 5 | 63.3% | 0.32 | 0.99 | 72.8% | 51.9% | 29.2% | 82.1%/42.0% | 3.7 (interpolated) | pass | 0.029 (unverified) | n/a |
| 67 | `cfg_374e` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 57/170/278 | 505 | 111.7% | 16.2% | 0.78 | -19.2% | 425 | 1.25 | 12.2% | 75.8 | 10/10 | 0.80 | 0.39 | 0.39 | 5 | 77.3% | 0.31 | 0.96 | 87.2% | 66.6% | 48.5% | 102.6%/64.0% | 4.3 (interpolated) | pass | 0.032 (unverified) | n/a |
| 68 | `cfg_bb10` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 79/185/320 | 584 | 106.4% | 15.6% | 0.79 | -22.5% | 175 | 1.22 | 13.8% | 93.4 | 10/10 | 0.80 | 0.40 | 0.39 | 5 | 72.4% | 0.29 | 0.95 | 80.9% | 61.6% | 35.7% | 101.5%/56.8% | 3.9 (interpolated) | pass | 0.034 (unverified) | n/a |
| 69 | `cfg_0b1e` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 61/189/114 | 364 | 112.2% | 16.3% | 0.84 | -22.3% | 215 | 1.37 | 11.1% | 56.3 | 13/13 | 0.77 | 0.46 | 0.38 | 4 | 64.2% | 0.43 | 0.68 | 94.1% | 78.2% | -4.6% | 97.9%/52.4% | 5.6 (interpolated) | pass | 0.046 (unverified) | n/a |
| 70 | `cfg_bd13` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 121/68/83 | 272 | 68.6% | 11.0% | 0.75 | -27.1% | 230 | 1.38 | 6.9% | 42.2 | 12/12 | 0.75 | 0.57 | 0.19 | 4 | 30.5% | 0.56 | 0.81 | 58.5% | 48.2% | -3.1% | 65.4%/42.2% | 5.2 (interpolated) | pass | 0.021 (unverified) | n/a |
| 71 | `cfg_d7da` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 185/187/379 | 751 | 95.3% | 14.3% | 0.79 | -20.6% | 477 | 1.21 | 9.9% | 112.3 | 11/11 | 0.55 | 0.30 | 0.49 | 4 | 9.2% | 0.75 | 0.93 | 64.5% | 37.5% | 41.7% | 80.1%/36.8% | 3.0 (interpolated) | pass | 0.044 (unverified) | n/a |
| 72 | `cfg_8b4a` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=30, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 28/44/74 | 146 | 33.2% | 5.9% | 0.80 | -9.5% | 406 | 1.51 | 3.4% | 20.1 | 12/12 | 0.83 | 0.53 | 0.26 | 3 | 12.5% | 0.62 | 0.66 | 28.6% | 23.9% | -0.2% | 29.5%/20.4% | 5.2 (interpolated) | pass | 0.048 (unverified) | n/a |
| 73 | `cfg_1ec3` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 84/154/291 | 529 | 55.9% | 9.3% | 0.79 | -12.8% | 366 | 1.21 | 11.8% | 91.3 | 10/10 | 0.80 | 0.48 | 0.31 | 5 | 24.2% | 0.57 | 0.62 | 41.2% | 25.5% | 18.6% | 48.1%/23.8% | 3.0 (interpolated) | pass | 0.042 (unverified) | n/a |
| 74 | `cfg_5a81` | timeframe=5min, mean_type=ema, mean_lookback=80, std_lookback=60, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 5/190/0 | 195 | 35.1% | 6.2% | 0.91 | -7.0% | 212 | 1.68 | 1.4% | 29.1 | 8/8 | 0.62 | 0.36 | 0.56 | 3 | 7.0% | 0.73 | 0.72 | 29.2% | 23.9% | 40.2% | 32.4%/22.9% | 4.5 (interpolated) | pass | 0.036 (unverified) | n/a |
| 75 | `cfg_1126` | timeframe=5min, mean_type=ema, mean_lookback=80, std_lookback=60, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 11/184/0 | 195 | 34.9% | 6.2% | 0.91 | -6.9% | 212 | 1.68 | 1.4% | 29.0 | 9/9 | 0.67 | 0.44 | 0.47 | 3 | 6.7% | 0.74 | 0.72 | 29.0% | 23.7% | 40.3% | 32.0%/23.5% | 4.5 (interpolated) | pass | 0.035 (unverified) | n/a |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 6.0% / 0.78 / 88 | 7.0% / 0.90 / 68 | 81.3% / 1.54 / 101 | 23.1% / 1.99 / 64 | 14.6% / 1.11 / 84 |
| 2 | 4.8% / 0.85 / 76 | 10.1% / 1.27 / 62 | 56.0% / 1.52 / 91 | 18.0% / 1.87 / 54 | 21.3% / 1.63 / 69 |
| 3 | 4.6% / 0.80 / 76 | 10.1% / 1.28 / 62 | 52.8% / 1.48 / 91 | 20.9% / 2.01 / 54 | 20.2% / 1.58 / 69 |
| 4 | 6.4% / 0.82 / 88 | 8.8% / 1.07 / 68 | 81.0% / 1.54 / 101 | 23.3% / 1.99 / 64 | 16.4% / 1.22 / 84 |
| 5 | 2.4% / 0.45 / 64 | 3.4% / 0.73 / 58 | 8.9% / 1.11 / 56 | 19.8% / 2.48 / 39 | 11.4% / 1.43 / 46 |
| 6 | 2.4% / 0.45 / 64 | 3.4% / 0.73 / 58 | 8.9% / 1.11 / 56 | 19.8% / 2.48 / 39 | 11.4% / 1.43 / 46 |
| 7 | -3.3% / -0.56 / 58 | 5.8% / 0.87 / 48 | 80.1% / 1.70 / 71 | 22.1% / 2.54 / 43 | 13.5% / 1.20 / 53 |
| 8 | -4.3% / -0.74 / 58 | 6.4% / 0.94 / 48 | 82.3% / 1.73 / 71 | 21.9% / 2.55 / 43 | 12.5% / 1.13 / 53 |
| 9 | 8.1% / 1.16 / 69 | 2.9% / 0.42 / 57 | 68.7% / 1.64 / 82 | 18.3% / 1.91 / 35 | 11.4% / 1.05 / 58 |
| 10 | 7.4% / 1.07 / 69 | 1.9% / 0.29 / 57 | 74.3% / 1.72 / 82 | 17.2% / 1.86 / 35 | 13.1% / 1.17 / 58 |
| 11 | 4.0% / 1.20 / 23 | 0.2% / 0.07 / 15 | 3.2% / 0.57 / 28 | 3.6% / 1.62 / 12 | 15.4% / 1.79 / 27 |
| 12 | 4.3% / 0.78 / 57 | -1.5% / -0.41 / 48 | -1.2% / -0.14 / 52 | 21.2% / 2.55 / 38 | 11.0% / 1.49 / 29 |
| 13 | 4.5% / 0.80 / 57 | -1.5% / -0.41 / 48 | -1.2% / -0.15 / 52 | 21.1% / 2.55 / 38 | 11.0% / 1.49 / 29 |
| 14 | 4.2% / 1.24 / 23 | 0.2% / 0.09 / 15 | 3.0% / 0.54 / 28 | 3.6% / 1.62 / 12 | 15.4% / 1.79 / 27 |
| 15 | 6.5% / 1.15 / 67 | 1.0% / 0.19 / 55 | 33.1% / 1.10 / 68 | 9.8% / 1.35 / 42 | 28.5% / 2.44 / 62 |
| 16 | 2.9% / 0.63 / 38 | -2.3% / -0.50 / 33 | 93.8% / 1.73 / 52 | 16.5% / 2.12 / 21 | 1.0% / 0.15 / 38 |
| 17 | 8.6% / 1.01 / 144 | 3.0% / 0.39 / 110 | 74.3% / 1.61 / 149 | 16.2% / 1.38 / 102 | -0.4% / 0.05 / 122 |
| 18 | 7.6% / 0.90 / 144 | 3.0% / 0.38 / 110 | 74.4% / 1.61 / 149 | 17.0% / 1.44 / 102 | 0.1% / 0.08 / 122 |
| 19 | 4.5% / 0.88 / 67 | -1.4% / -0.23 / 55 | 23.4% / 0.93 / 68 | 9.3% / 1.34 / 43 | 21.9% / 2.05 / 66 |
| 20 | 10.9% / 1.07 / 129 | 21.3% / 1.99 / 97 | 26.9% / 0.76 / 138 | 24.4% / 1.76 / 93 | 20.7% / 1.10 / 134 |
| 21 | 4.3% / 0.63 / 106 | 4.7% / 0.70 / 89 | 15.4% / 0.57 / 127 | 22.4% / 2.52 / 65 | 22.7% / 1.71 / 91 |
| 22 | 14.2% / 1.56 / 108 | 4.8% / 0.59 / 89 | 16.8% / 0.61 / 120 | 26.4% / 2.22 / 68 | 32.1% / 2.09 / 90 |
| 23 | 5.6% / 0.74 / 106 | 3.8% / 0.57 / 89 | 24.8% / 0.75 / 127 | 22.6% / 2.42 / 65 | 23.4% / 1.67 / 91 |
| 24 | 8.0% / 2.02 / 42 | -0.6% / -0.13 / 33 | -2.4% / -0.15 / 55 | 7.5% / 1.97 / 24 | 17.3% / 1.76 / 47 |
| 25 | 14.2% / 1.57 / 108 | 1.9% / 0.27 / 89 | 16.6% / 0.61 / 120 | 24.3% / 2.13 / 68 | 32.2% / 2.09 / 90 |
| 26 | 1.5% / 0.32 / 55 | 1.7% / 0.38 / 51 | 14.4% / 1.26 / 64 | -0.2% / 0.00 / 36 | 19.3% / 1.90 / 58 |
| 27 | 2.1% / 0.42 / 55 | 1.9% / 0.41 / 51 | 12.3% / 1.10 / 64 | -0.1% / 0.01 / 36 | 21.5% / 2.01 / 58 |
| 28 | 6.3% / 0.82 / 104 | 2.7% / 0.32 / 89 | 57.8% / 1.13 / 109 | 24.0% / 2.11 / 65 | 23.6% / 1.44 / 94 |
| 29 | 4.1% / 0.61 / 100 | 3.5% / 0.65 / 80 | 49.9% / 1.27 / 114 | 19.1% / 1.80 / 67 | 3.8% / 0.37 / 88 |
| 30 | 8.6% / 2.07 / 42 | -0.9% / -0.20 / 33 | -2.4% / -0.15 / 55 | 7.7% / 2.00 / 24 | 17.0% / 1.74 / 47 |
| 31 | -1.1% / -0.27 / 32 | 4.4% / 1.06 / 27 | 32.1% / 1.09 / 43 | 7.1% / 1.12 / 29 | 19.5% / 2.04 / 40 |
| 32 | 5.1% / 0.73 / 100 | 2.6% / 0.51 / 80 | 55.3% / 1.27 / 114 | 17.1% / 1.66 / 67 | 4.0% / 0.39 / 88 |
| 33 | 14.3% / 1.46 / 136 | 1.1% / 0.17 / 104 | 45.7% / 1.22 / 141 | 20.5% / 1.65 / 96 | 7.2% / 0.51 / 129 |
| 34 | 9.8% / 0.98 / 129 | 17.9% / 1.76 / 97 | 31.0% / 0.83 / 140 | 21.6% / 1.71 / 93 | 22.2% / 1.16 / 134 |
| 35 | 0.0% / 0.03 / 47 | -5.2% / -1.18 / 37 | 3.4% / 0.53 / 40 | 15.1% / 1.75 / 35 | 14.9% / 2.01 / 24 |
| 36 | -0.0% / 0.03 / 47 | -5.2% / -1.18 / 37 | 3.4% / 0.53 / 40 | 15.1% / 1.75 / 35 | 14.9% / 2.01 / 24 |
| 37 | 5.5% / 1.17 / 48 | -1.8% / -0.38 / 42 | 13.6% / 1.26 / 52 | 2.8% / 0.69 / 26 | 12.1% / 1.35 / 39 |
| 38 | -1.3% / -0.34 / 32 | 4.4% / 1.06 / 27 | 28.7% / 1.08 / 43 | 7.2% / 1.15 / 29 | 17.4% / 1.95 / 40 |
| 39 | 6.4% / 0.86 / 68 | 10.1% / 1.36 / 46 | 44.4% / 1.07 / 78 | 14.6% / 1.72 / 43 | 4.5% / 0.41 / 59 |
| 40 | 0.1% / 0.05 / 64 | 2.0% / 0.28 / 49 | 33.8% / 0.93 / 70 | 22.3% / 2.31 / 40 | 18.7% / 1.43 / 56 |
| 41 | 7.2% / 0.97 / 86 | 2.3% / 0.39 / 84 | -0.3% / 0.03 / 91 | 8.0% / 1.23 / 57 | 21.8% / 1.64 / 95 |
| 42 | 14.1% / 1.42 / 136 | 3.7% / 0.44 / 104 | 44.7% / 1.21 / 141 | 23.3% / 1.80 / 96 | 2.3% / 0.22 / 129 |
| 43 | -5.9% / -0.69 / 37 | 23.6% / 1.86 / 25 | 10.3% / 0.46 / 38 | 2.4% / 0.34 / 25 | 35.3% / 2.23 / 35 |
| 44 | 1.9% / 0.30 / 85 | 5.7% / 0.78 / 67 | 38.8% / 0.98 / 99 | 14.1% / 1.82 / 48 | 13.7% / 1.14 / 68 |
| 45 | 6.1% / 0.84 / 86 | 2.7% / 0.45 / 84 | -0.2% / 0.04 / 91 | 7.9% / 1.22 / 57 | 22.5% / 1.67 / 95 |
| 46 | 0.4% / 0.09 / 64 | 2.0% / 0.28 / 49 | 30.7% / 0.88 / 70 | 24.3% / 2.34 / 40 | 18.2% / 1.40 / 56 |
| 47 | 5.5% / 1.47 / 32 | -5.0% / -1.56 / 29 | 13.2% / 1.80 / 39 | -0.5% / -0.15 / 21 | 8.9% / 1.37 / 25 |
| 48 | 3.3% / 0.45 / 104 | 3.6% / 0.45 / 81 | 35.3% / 0.97 / 111 | 13.7% / 1.15 / 77 | 23.4% / 1.55 / 96 |
| 49 | 5.8% / 1.25 / 48 | -2.1% / -0.48 / 42 | 13.9% / 1.29 / 52 | 2.9% / 0.70 / 26 | 10.7% / 1.24 / 39 |
| 50 | 4.8% / 1.31 / 32 | -4.4% / -1.28 / 29 | 13.4% / 1.82 / 39 | -1.0% / -0.31 / 21 | 8.6% / 1.34 / 25 |
| 51 | -1.6% / -0.25 / 48 | 5.2% / 0.64 / 44 | 36.6% / 1.01 / 61 | 24.5% / 2.85 / 40 | 13.3% / 1.19 / 48 |
| 52 | -2.1% / -0.33 / 48 | 5.7% / 0.68 / 44 | 36.6% / 1.01 / 61 | 23.7% / 2.76 / 40 | 13.1% / 1.16 / 48 |
| 53 | 4.7% / 0.57 / 89 | 1.8% / 0.30 / 73 | 51.4% / 1.26 / 100 | 19.5% / 1.73 / 65 | 4.3% / 0.37 / 75 |
| 54 | 11.7% / 1.32 / 97 | 6.5% / 0.71 / 92 | 54.6% / 1.17 / 120 | 11.6% / 1.14 / 77 | 15.5% / 1.04 / 98 |
| 55 | 5.9% / 0.70 / 89 | 0.8% / 0.16 / 73 | 39.2% / 1.15 / 100 | 17.4% / 1.63 / 65 | 4.8% / 0.41 / 75 |
| 56 | 13.9% / 1.42 / 114 | 11.1% / 1.18 / 87 | 23.5% / 0.69 / 111 | 15.4% / 1.29 / 77 | 21.6% / 1.22 / 116 |
| 57 | 12.2% / 1.38 / 97 | 6.5% / 0.69 / 92 | 38.0% / 0.97 / 120 | 15.2% / 1.41 / 77 | 12.3% / 0.85 / 98 |
| 58 | 10.9% / 2.27 / 44 | -1.6% / -0.30 / 35 | 0.3% / 0.10 / 51 | 4.9% / 1.07 / 24 | 21.8% / 2.02 / 45 |
| 59 | 9.5% / 1.06 / 84 | -2.6% / -0.24 / 70 | 43.4% / 1.11 / 77 | 6.7% / 0.64 / 61 | 28.1% / 1.58 / 72 |
| 60 | 9.8% / 1.11 / 103 | 6.0% / 0.63 / 89 | 12.5% / 0.48 / 108 | 30.8% / 2.46 / 65 | 16.2% / 1.04 / 93 |
| 61 | 3.9% / 1.19 / 28 | 0.4% / 0.13 / 19 | 8.5% / 0.93 / 31 | 5.7% / 1.95 / 9 | 3.2% / 0.49 / 23 |
| 62 | 8.4% / 1.02 / 103 | 1.4% / 0.19 / 89 | 17.5% / 0.58 / 108 | 26.3% / 2.26 / 65 | 22.0% / 1.34 / 94 |
| 63 | -9.9% / -1.18 / 142 | 0.5% / 0.10 / 127 | 114.6% / 1.94 / 180 | 20.9% / 1.81 / 133 | 2.9% / 0.24 / 164 |
| 64 | 2.5% / 0.64 / 54 | -3.9% / -0.59 / 53 | 35.7% / 2.29 / 53 | 1.9% / 0.39 / 35 | 0.3% / 0.08 / 45 |
| 65 | 4.0% / 1.14 / 28 | 0.5% / 0.19 / 19 | 7.2% / 0.80 / 31 | 6.1% / 1.96 / 9 | 4.0% / 0.59 / 23 |
| 66 | 12.2% / 1.19 / 133 | 14.2% / 1.56 / 91 | 20.3% / 0.66 / 130 | 20.0% / 1.75 / 93 | 5.9% / 0.42 / 140 |
| 67 | 10.9% / 1.10 / 114 | 10.9% / 1.16 / 87 | 24.5% / 0.71 / 111 | 15.8% / 1.29 / 77 | 19.4% / 1.12 / 116 |
| 68 | 10.8% / 1.06 / 132 | 19.8% / 1.96 / 91 | 18.5% / 0.61 / 128 | 19.7% / 1.41 / 93 | 9.7% / 0.61 / 140 |
| 69 | 9.6% / 1.05 / 84 | -1.6% / -0.12 / 70 | 40.0% / 1.06 / 77 | 8.7% / 0.77 / 61 | 29.3% / 1.62 / 72 |
| 70 | 7.5% / 1.05 / 64 | -8.2% / -1.08 / 52 | 19.5% / 0.74 / 61 | 10.5% / 1.30 / 38 | 29.2% / 2.18 / 57 |
| 71 | -10.5% / -1.26 / 144 | 1.1% / 0.17 / 129 | 78.9% / 1.84 / 180 | 19.0% / 1.75 / 134 | 1.4% / 0.17 / 164 |
| 72 | 9.5% / 1.99 / 32 | -3.1% / -0.71 / 29 | 8.2% / 0.69 / 39 | -2.0% / -0.53 / 21 | 18.4% / 2.04 / 25 |
| 73 | 0.8% / 0.14 / 102 | 1.9% / 0.27 / 97 | 0.1% / 0.08 / 107 | 20.8% / 1.73 / 90 | 25.6% / 1.50 / 133 |
| 74 | 0.2% / 0.07 / 40 | -2.1% / -0.44 / 39 | 26.3% / 1.97 / 45 | -1.3% / -0.39 / 26 | 10.6% / 1.55 / 45 |
| 75 | 0.2% / 0.07 / 40 | -2.5% / -0.53 / 39 | 26.4% / 1.98 / 45 | -1.3% / -0.39 / 26 | 10.7% / 1.57 / 45 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_2258` | 128 | 0.83 | 0.41/0.65 | 0.09/0.39 |
| 1 | `cfg_92a1` | 58 | 0.81 | 0.03/0.82 | 0.10/0.36 |
| 2 | `cfg_ce65` | 4 | 0.98 | 0.98/0.99 | 0.99/0.99 |
| 3 | `cfg_0729` | 4 | 0.98 | 0.97/0.99 | 0.95/0.99 |
| 4 | `cfg_f9a8` | 8 | 0.83 | 0.90/0.91 | 0.62/0.62 |
| 5 | `cfg_508a` | 6 | 0.90 | 0.95/0.98 | 0.92/0.97 |
| 6 | `cfg_e515` | 4 | 1.00 | 1.00/1.00 | 0.99/1.00 |
| 7 | `cfg_094c` | 3 | 0.96 | 0.99/0.99 | 0.99/0.99 |
| 8 | `cfg_0a51` | 6 | 0.88 | 0.92/0.93 | 0.67/0.70 |
| 9 | `cfg_1961` | 4 | 0.95 | 0.98/0.99 | 0.97/0.98 |
| 10 | `cfg_cb6e` | 4 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 11 | `cfg_2a9c` | 12 | 0.88 | 0.67/0.88 | 0.45/0.70 |
| 12 | `cfg_12d7` | 3 | 0.92 | 0.98/0.99 | 0.99/0.99 |
| 13 | `cfg_4a55` | 3 | 0.96 | 0.98/0.99 | 0.93/0.96 |
| 14 | `cfg_53cc` | 5 | 0.92 | 0.89/0.99 | 0.78/0.99 |
| 15 | `cfg_5a81` | 3 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 16 | `cfg_1166` | 9 | 0.81 | 0.28/0.89 | 0.07/0.76 |
| 17 | `cfg_c64c` | 8 | 0.82 | 0.88/0.88 | 0.67/0.68 |
| 18 | `cfg_39ee` | 12 | 0.86 | 0.85/0.90 | 0.56/0.59 |
| 19 | `cfg_7223` | 4 | 0.98 | 0.99/1.00 | 0.99/1.00 |
| 20 | `cfg_3fcb` | 8 | 0.91 | 0.83/0.83 | 0.71/0.74 |
| 21 | `cfg_429c` | 4 | 1.00 | 1.00/1.00 | 0.99/1.00 |
| 22 | `cfg_1c51` | 1 | n/a | n/a/n/a | n/a/n/a |
| 23 | `cfg_1ec3` | 1 | n/a | n/a/n/a | n/a/n/a |
| 24 | `cfg_cc63` | 6 | 0.85 | 0.90/0.95 | 0.76/0.95 |
| 25 | `cfg_e424` | 3 | 0.97 | 0.98/0.99 | 0.98/0.99 |
| 26 | `cfg_430b` | 11 | 0.83 | 0.85/0.89 | 0.68/0.81 |
| 27 | `cfg_2c94` | 6 | 0.88 | 0.91/0.93 | 0.80/0.82 |
| 28 | `cfg_63e4` | 2 | 0.99 | 1.00/1.00 | 0.99/0.99 |
| 29 | `cfg_bde6` | 4 | 0.99 | 0.99/0.99 | 0.98/0.99 |
| 30 | `cfg_5c1e` | 3 | 0.85 | 0.70/0.71 | 0.52/0.52 |
| 31 | `cfg_5a08` | 2 | 0.99 | 1.00/1.00 | 0.99/0.99 |
| 32 | `cfg_60d4` | 2 | 0.94 | 0.88/0.88 | 0.62/0.62 |
| 33 | `cfg_6d7c` | 3 | 0.99 | 0.98/0.98 | 0.96/0.96 |
| 34 | `cfg_7b29` | 1 | n/a | n/a/n/a | n/a/n/a |
| 35 | `cfg_869a` | 3 | 0.99 | 0.99/1.00 | 1.00/1.00 |
| 36 | `cfg_8b4a` | 1 | n/a | n/a/n/a | n/a/n/a |
| 37 | `cfg_efc3` | 2 | 0.96 | 0.99/0.99 | 0.95/0.95 |
| 38 | `cfg_d193` | 1 | n/a | n/a/n/a | n/a/n/a |
| 39 | `cfg_d998` | 4 | 0.82 | 0.97/0.97 | 0.94/0.94 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 8.965e-04 over 40944 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1130.0, participation ratio 16.3, 95%-variance components 221 (rank bound T = 1258); raw grid 41472; raw + known prior 649032
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
None results are unchanged rules on the development period: supporting evidence, not an independent replication.

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
- Session: each root's day session only (src/data/futures.py SESSIONS: NYSE 09:30-16:00 NY for equity indexes, 09:00-14:30 NY for crude), on NYSE trading days; overnight Globex bars are not traded or used in indicators.
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
