# Screening funnel -- mr_cl_v6 (development stages only)

- Code: `5342a94cdc84` (dirty working tree: True, diff sha256 `6a1ad0bc76ed`)
- Config: `configs/funnel/mr_funnel_cl_v6.yaml` sha256 `958ac99497cbe231`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'CL': '2026-10-16'}
- Frozen manifest sha256: `fb798fb2c27be597` (82 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_cl_v5 gated 75 CL candidates on 2023-2024 (7 passed, all 15min) and this grid was written after reading those results, so CL 2023-2024 is partly in-sample here.
- Holdout 2025+ previously inspected: **False** -- No CL strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 17280 | 17280 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 17280 | 17280 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 17280 | 15777 | 1503 | 0 |  | 16520 | 91.30 | 91.30 |  |
| 3 performance & risk | hard_gate | 15777 | 674 | 15103 | 0 |  | 0 | 3.90 | 4.27 |  |
| 4 parameter stability | hard_gate | 674 | 658 | 16 | 0 |  | 0 | 3.81 | 97.63 |  |
| 5 time stability | hard_gate | 658 | 648 | 10 | 0 |  | 600 | 3.75 | 98.48 |  |
| 6 deduplication | dedup | 648 | 82 |  |  | 566 |  | 0.47 | 12.65 | best 2 per cluster |
| 7 execution stress | hard_gate | 82 | 82 | 0 | 0 |  | 2 | 0.47 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 82 |  |  |  |  |  |  |  | diagnostic only: unverified: 82 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 1503 |
| s2:hard_reject:years_with_>=10_trades | 912 |
| s3:hard_reject:max_drawdown | 8559 |
| s3:hard_reject:net_return | 8634 |
| s3:hard_reject:sharpe | 15079 |
| s4:hard_reject:local_median_sharpe | 16 |
| s5:hard_reject:profitable_years | 10 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | transfer dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_f1d8` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 35/158/42 | 235 | 251.9% | 28.7% | 1.38 | -12.5% | 243 | 2.15 | 4.5% | 34.4 | 10/10 | 1.00 | 0.98 | 0.39 | 4 | 34.8% | 0.71 | 0.59 | 231.7% | 213.3% | 103.7% | 216.0%/124.5% | 12.5 (interpolated) | pass | 0.473 (unverified) | n/a |
| 2 | `cfg_a4b4` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=20, entry_z=-3.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 18/174/43 | 235 | 249.8% | 28.5% | 1.37 | -12.6% | 243 | 2.14 | 4.6% | 34.6 | 10/10 | 1.00 | 0.98 | 0.39 | 4 | 37.0% | 0.69 | 0.59 | 229.1% | 211.1% | 102.9% | 215.9%/111.1% | 12.4 (interpolated) | pass | 0.469 (unverified) | n/a |
| 3 | `cfg_b3df` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=20, entry_z=-3.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 23/128/166 | 317 | 198.1% | 24.5% | 1.27 | -13.9% | 215 | 1.78 | 6.4% | 45.7 | 8/8 | 1.00 | 1.07 | 0.20 | 5 | 46.4% | 0.58 | 0.60 | 177.7% | 158.1% | 80.3% | 178.1%/124.5% | 8.5 (interpolated) | pass | 0.385 (unverified) | n/a |
| 4 | `cfg_ba6e` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 51/102/164 | 317 | 193.3% | 24.1% | 1.25 | -14.0% | 256 | 1.78 | 6.1% | 45.6 | 8/8 | 1.00 | 1.04 | 0.22 | 5 | 44.1% | 0.58 | 0.59 | 174.3% | 154.1% | 99.8% | 186.5%/125.2% | 8.4 (interpolated) | pass | 0.374 (unverified) | n/a |
| 5 | `cfg_39ee` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 26/195/52 | 273 | 155.3% | 20.6% | 1.09 | -13.5% | 263 | 1.79 | 5.3% | 39.5 | 12/12 | 0.92 | 0.92 | 0.17 | 4 | 41.7% | 0.53 | 0.60 | 139.4% | 124.6% | 66.9% | 137.3%/88.8% | 8.3 (interpolated) | pass | 0.152 (unverified) | n/a |
| 6 | `cfg_5bc0` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 44/178/51 | 273 | 154.7% | 20.6% | 1.09 | -13.5% | 263 | 1.80 | 5.2% | 39.3 | 11/11 | 0.91 | 0.86 | 0.22 | 4 | 39.7% | 0.54 | 0.60 | 139.2% | 123.3% | 66.9% | 137.3%/74.9% | 8.2 (interpolated) | pass | 0.150 (unverified) | n/a |
| 7 | `cfg_baf9` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 44/148/157 | 349 | 141.2% | 19.3% | 1.08 | -9.5% | 269 | 1.68 | 5.3% | 49.9 | 10/10 | 1.00 | 0.99 | 0.09 | 4 | 38.7% | 0.53 | 0.66 | 124.5% | 106.4% | 73.7% | 129.2%/82.2% | 6.5 (interpolated) | pass | 0.138 (unverified) | n/a |
| 8 | `cfg_df3c` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 25/166/158 | 349 | 143.8% | 19.5% | 1.09 | -9.6% | 255 | 1.69 | 5.4% | 50.1 | 11/11 | 1.00 | 0.99 | 0.10 | 4 | 42.1% | 0.51 | 0.65 | 126.8% | 109.3% | 70.1% | 129.1%/65.3% | 6.6 (interpolated) | pass | 0.147 (unverified) | n/a |
| 9 | `cfg_bb70` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 33/301/87 | 421 | 225.8% | 26.7% | 1.10 | -20.5% | 478 | 1.65 | 8.1% | 63.3 | 10/10 | 0.90 | 0.84 | 0.26 | 4 | 54.2% | 0.51 | 0.56 | 193.8% | 166.2% | 57.0% | 188.9%/88.2% | 7.1 (interpolated) | pass | 0.233 (unverified) | n/a |
| 10 | `cfg_7388` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 105/233/85 | 423 | 237.7% | 27.6% | 1.10 | -19.5% | 334 | 1.66 | 7.7% | 63.1 | 10/10 | 1.00 | 0.82 | 0.28 | 4 | 49.5% | 0.56 | 0.58 | 208.3% | 177.4% | 59.2% | 212.1%/120.4% | 7.3 (interpolated) | pass | 0.225 (unverified) | n/a |
| 11 | `cfg_8b81` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=30, entry_z=-3.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 13/88/82 | 183 | 77.8% | 12.2% | 1.19 | -8.2% | 340 | 1.85 | 4.1% | 21.8 | 7/7 | 1.00 | 0.66 | 0.53 | 5 | 30.9% | 0.48 | 0.54 | 69.2% | 61.2% | 36.1% | 64.9%/43.8% | 7.2 (interpolated) | pass | 0.280 (unverified) | n/a |
| 12 | `cfg_b062` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=30, entry_z=-3.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 3/98/82 | 183 | 77.5% | 12.2% | 1.18 | -9.3% | 340 | 1.86 | 4.2% | 21.8 | 6/6 | 1.00 | 0.62 | 0.56 | 4 | 30.7% | 0.47 | 0.55 | 68.8% | 60.8% | 34.1% | 65.2%/48.0% | 7.2 (interpolated) | pass | 0.271 (unverified) | n/a |
| 13 | `cfg_fa04` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 26/209/27 | 262 | 104.5% | 15.4% | 1.05 | -14.7% | 339 | 1.76 | 3.6% | 37.4 | 10/10 | 0.90 | 0.73 | 0.32 | 4 | 32.9% | 0.51 | 0.69 | 91.9% | 82.0% | 51.7% | 94.3%/71.2% | 6.9 (interpolated) | pass | 0.136 (unverified) | n/a |
| 14 | `cfg_9384` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 18/216/28 | 262 | 104.1% | 15.4% | 1.05 | -14.5% | 400 | 1.76 | 3.6% | 37.4 | 11/11 | 0.91 | 0.82 | 0.23 | 4 | 32.5% | 0.52 | 0.69 | 91.7% | 81.1% | 52.6% | 91.3%/68.1% | 6.9 (interpolated) | pass | 0.134 (unverified) | n/a |
| 15 | `cfg_fe55` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=25, entry_z=-3.0, exit_z=0.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 4/144/15 | 163 | 40.3% | 7.0% | 1.04 | -6.6% | 319 | 1.72 | 2.3% | 25.1 | 10/10 | 1.00 | 0.74 | 0.30 | 4 | 24.4% | 0.40 | 0.60 | 35.2% | 30.3% | 13.2% | 38.2%/29.9% | 5.6 (interpolated) | pass | 0.185 (unverified) | n/a |
| 16 | `cfg_cb6e` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 10/58/37 | 105 | 28.6% | 5.2% | 1.03 | -6.1% | 337 | 1.77 | 1.7% | 14.7 | 9/9 | 1.00 | 0.79 | 0.24 | 5 | 11.4% | 0.60 | 0.66 | 25.1% | 22.1% | 28.6% | 27.0%/18.9% | 6.0 (interpolated) | pass | 0.177 (unverified) | n/a |
| 17 | `cfg_2f25` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=25, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 7/141/15 | 163 | 40.3% | 7.0% | 1.04 | -6.6% | 319 | 1.71 | 2.3% | 25.1 | 11/11 | 1.00 | 0.85 | 0.19 | 4 | 24.3% | 0.40 | 0.60 | 35.2% | 30.3% | 13.4% | 37.0%/27.9% | 5.6 (interpolated) | pass | 0.185 (unverified) | n/a |
| 18 | `cfg_e686` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 6/62/37 | 105 | 28.7% | 5.2% | 1.03 | -6.2% | 338 | 1.77 | 1.7% | 14.7 | 10/10 | 1.00 | 0.79 | 0.24 | 5 | 11.5% | 0.60 | 0.66 | 25.1% | 22.2% | 27.0% | 25.7%/19.9% | 6.0 (interpolated) | pass | 0.178 (unverified) | n/a |
| 19 | `cfg_5f93` | timeframe=15min, mean_type=sma, mean_lookback=100, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 31/253/60 | 344 | 88.0% | 13.5% | 1.02 | -14.1% | 483 | 1.49 | 6.7% | 54.6 | 9/9 | 0.89 | 0.57 | 0.45 | 4 | 43.6% | 0.48 | 0.54 | 74.8% | 60.7% | 55.8% | 76.9%/50.2% | 5.3 (interpolated) | pass | 0.180 (unverified) | n/a |
| 20 | `cfg_f8ad` | timeframe=15min, mean_type=sma, mean_lookback=100, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 37/247/60 | 344 | 85.4% | 13.2% | 1.01 | -14.3% | 483 | 1.48 | 6.7% | 54.5 | 10/10 | 0.90 | 0.62 | 0.38 | 4 | 42.9% | 0.47 | 0.55 | 71.3% | 58.3% | 53.8% | 74.6%/46.7% | 5.2 (interpolated) | pass | 0.169 (unverified) | n/a |
| 21 | `cfg_0055` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 101/197/322 | 620 | 122.2% | 17.3% | 0.89 | -13.8% | 220 | 1.26 | 12.3% | 92.2 | 9/9 | 1.00 | 0.82 | 0.07 | 5 | 44.0% | 0.52 | 0.80 | 93.7% | 67.9% | 20.6% | 108.7%/68.1% | 3.9 (interpolated) | pass | 0.073 (unverified) | n/a |
| 22 | `cfg_1166` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 61/286/280 | 627 | 125.8% | 17.7% | 0.91 | -14.1% | 291 | 1.30 | 9.7% | 89.9 | 10/10 | 1.00 | 0.84 | 0.07 | 4 | 29.6% | 0.66 | 0.82 | 95.1% | 69.0% | 18.4% | 106.5%/72.5% | 3.9 (interpolated) | pass | 0.074 (unverified) | n/a |
| 23 | `cfg_8a27` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 47/300/280 | 627 | 126.3% | 17.8% | 0.91 | -14.4% | 291 | 1.31 | 9.8% | 90.1 | 9/9 | 1.00 | 0.82 | 0.09 | 5 | 29.8% | 0.65 | 0.80 | 96.1% | 69.3% | 17.9% | 112.8%/55.0% | 3.9 (interpolated) | pass | 0.074 (unverified) | n/a |
| 24 | `cfg_7f8d` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=0.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 1/101/5 | 107 | 30.9% | 5.5% | 1.14 | -4.4% | 316 | 1.98 | 1.5% | 13.5 | 10/10 | 0.90 | 0.72 | 0.42 | 4 | 12.4% | 0.55 | 0.61 | 27.4% | 24.1% | 6.3% | 27.8%/20.9% | 6.1 (interpolated) | pass | 0.276 (unverified) | n/a |
| 25 | `cfg_b397` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 100/53/140 | 293 | 89.3% | 13.6% | 0.92 | -20.0% | 226 | 1.55 | 5.2% | 45.8 | 8/8 | 1.00 | 0.76 | 0.16 | 4 | 53.5% | 0.40 | 0.73 | 77.8% | 66.7% | 0.9% | 83.0%/57.7% | 5.8 (interpolated) | pass | 0.143 (unverified) | n/a |
| 26 | `cfg_5255` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 3/99/5 | 107 | 30.4% | 5.5% | 1.13 | -4.4% | 316 | 1.97 | 1.5% | 13.4 | 11/11 | 0.91 | 0.75 | 0.38 | 4 | 12.3% | 0.54 | 0.61 | 26.9% | 23.4% | 8.4% | 28.3%/21.7% | 6.1 (interpolated) | pass | 0.274 (unverified) | n/a |
| 27 | `cfg_07b0` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 63/104/129 | 296 | 90.9% | 13.8% | 0.93 | -13.2% | 225 | 1.62 | 4.3% | 45.5 | 9/9 | 1.00 | 0.82 | 0.11 | 5 | 36.1% | 0.46 | 0.74 | 78.2% | 67.6% | 7.5% | 84.9%/61.0% | 5.9 (interpolated) | pass | 0.147 (unverified) | n/a |
| 28 | `cfg_8f06` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 75/221/323 | 619 | 107.4% | 15.7% | 0.82 | -13.9% | 220 | 1.23 | 12.6% | 91.0 | 8/8 | 1.00 | 0.84 | -0.02 | 5 | 35.9% | 0.57 | 0.88 | 81.6% | 57.5% | 15.9% | 97.9%/72.2% | 3.7 (interpolated) | pass | 0.052 (unverified) | n/a |
| 29 | `cfg_2ca6` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=25, entry_z=-3.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 11/129/125 | 265 | 52.6% | 8.8% | 0.85 | -15.5% | 360 | 1.38 | 5.8% | 41.7 | 9/9 | 0.89 | 0.83 | 0.02 | 5 | 13.7% | 0.74 | 0.69 | 44.2% | 36.0% | 31.4% | 48.3%/34.0% | 4.6 (interpolated) | pass | 0.121 (unverified) | n/a |
| 30 | `cfg_18c9` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=25, entry_z=-3.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 15/125/125 | 265 | 52.3% | 8.8% | 0.85 | -15.5% | 360 | 1.38 | 5.8% | 41.7 | 9/9 | 0.89 | 0.82 | 0.02 | 5 | 13.4% | 0.74 | 0.71 | 43.7% | 35.2% | 30.7% | 50.0%/35.3% | 4.6 (interpolated) | pass | 0.119 (unverified) | n/a |
| 31 | `cfg_3fcb` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 124/138/216 | 478 | 89.4% | 13.7% | 0.81 | -27.6% | 234 | 1.36 | 6.7% | 71.1 | 9/9 | 0.89 | 0.81 | -0.00 | 5 | 54.3% | 0.39 | 0.76 | 69.1% | 50.4% | 33.6% | 85.0%/35.4% | 3.9 (interpolated) | pass | 0.070 (unverified) | n/a |
| 32 | `cfg_e30b` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 78/141/231 | 450 | 121.2% | 17.2% | 0.89 | -20.3% | 248 | 1.39 | 8.6% | 66.0 | 7/7 | 1.00 | 0.77 | 0.12 | 5 | 48.2% | 0.45 | 0.79 | 100.1% | 79.9% | 22.4% | 105.2%/49.6% | 5.0 (interpolated) | pass | 0.063 (unverified) | n/a |
| 33 | `cfg_3590` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 48/208/222 | 478 | 106.8% | 15.7% | 0.84 | -27.8% | 252 | 1.41 | 7.2% | 71.1 | 10/10 | 0.90 | 0.81 | 0.03 | 5 | 67.6% | 0.37 | 0.71 | 84.1% | 64.8% | 52.2% | 101.3%/58.3% | 4.3 (interpolated) | pass | 0.067 (unverified) | n/a |
| 34 | `cfg_7223` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 21/105/75 | 201 | 32.1% | 5.7% | 0.80 | -15.3% | 562 | 1.39 | 3.3% | 29.8 | 10/10 | 1.00 | 0.51 | 0.29 | 3 | 12.7% | 0.61 | 0.77 | 26.1% | 19.8% | 16.1% | 29.1%/20.0% | 4.0 (interpolated) | pass | 0.098 (unverified) | n/a |
| 35 | `cfg_ce65` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 28/134/102 | 264 | 40.6% | 7.1% | 0.91 | -9.1% | 451 | 1.41 | 4.3% | 40.1 | 9/9 | 1.00 | 0.62 | 0.29 | 4 | 17.8% | 0.56 | 0.66 | 32.8% | 25.4% | 16.0% | 38.8%/29.8% | 3.9 (interpolated) | pass | 0.144 (unverified) | n/a |
| 36 | `cfg_fd85` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 13/148/103 | 264 | 41.6% | 7.2% | 0.92 | -10.6% | 451 | 1.42 | 4.3% | 40.1 | 10/10 | 1.00 | 0.74 | 0.18 | 4 | 16.6% | 0.60 | 0.67 | 33.9% | 25.7% | 17.7% | 43.2%/30.3% | 4.0 (interpolated) | pass | 0.147 (unverified) | n/a |
| 37 | `cfg_0a51` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 48/193/208 | 449 | 99.8% | 14.9% | 0.84 | -19.1% | 248 | 1.37 | 6.8% | 64.2 | 8/8 | 1.00 | 0.81 | 0.03 | 5 | 33.2% | 0.54 | 0.93 | 81.5% | 63.2% | 33.9% | 92.6%/49.9% | 4.5 (interpolated) | pass | 0.060 (unverified) | n/a |
| 38 | `cfg_22be` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 12/114/75 | 201 | 32.5% | 5.8% | 0.81 | -15.3% | 562 | 1.39 | 3.4% | 29.8 | 11/11 | 1.00 | 0.52 | 0.30 | 3 | 13.2% | 0.59 | 0.76 | 26.9% | 20.7% | 16.5% | 29.3%/21.7% | 4.0 (interpolated) | pass | 0.101 (unverified) | n/a |
| 39 | `cfg_4509` | timeframe=15min, mean_type=sma, mean_lookback=100, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 30/233/213 | 476 | 68.3% | 11.0% | 0.92 | -10.5% | 351 | 1.31 | 7.6% | 77.5 | 8/8 | 1.00 | 0.68 | 0.24 | 4 | 27.5% | 0.54 | 0.67 | 52.8% | 38.2% | 64.5% | 63.3%/39.7% | 3.6 (interpolated) | pass | 0.119 (unverified) | n/a |
| 40 | `cfg_a8cc` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=25, entry_z=-2.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 17/113/14 | 144 | 26.3% | 4.8% | 0.85 | -9.7% | 328 | 1.55 | 2.0% | 19.8 | 10/10 | 0.90 | 0.65 | 0.20 | 4 | 10.6% | 0.53 | 0.65 | 22.0% | 17.9% | 1.4% | 23.3%/17.2% | 4.5 (interpolated) | pass | 0.122 (unverified) | n/a |
| 41 | `cfg_0729` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 14/106/87 | 207 | 35.8% | 6.3% | 0.91 | -9.9% | 334 | 1.45 | 3.3% | 29.5 | 8/8 | 0.88 | 0.68 | 0.23 | 4 | 21.1% | 0.41 | 0.62 | 29.8% | 24.0% | 9.5% | 33.0%/24.8% | 4.3 (interpolated) | pass | 0.144 (unverified) | n/a |
| 42 | `cfg_9db1` | timeframe=15min, mean_type=ema, mean_lookback=80, std_lookback=25, entry_z=-3.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 11/94/89 | 194 | 83.5% | 12.9% | 0.86 | -9.3% | 171 | 1.73 | 4.3% | 25.8 | 9/9 | 0.89 | 0.72 | 0.15 | 5 | 21.8% | 0.65 | 0.77 | 74.2% | 66.0% | 5.0% | 74.2%/39.8% | 7.5 (interpolated) | pass | 0.021 (unverified) | n/a |
| 43 | `cfg_22b5` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 75/153/249 | 477 | 101.0% | 15.0% | 0.81 | -23.6% | 266 | 1.34 | 9.2% | 70.9 | 9/9 | 1.00 | 0.79 | 0.01 | 5 | 55.3% | 0.45 | 0.75 | 79.5% | 60.3% | 24.6% | 99.6%/57.8% | 4.1 (interpolated) | pass | 0.047 (unverified) | n/a |
| 44 | `cfg_7a28` | timeframe=15min, mean_type=ema, mean_lookback=80, std_lookback=25, entry_z=-3.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 6/99/89 | 194 | 82.9% | 12.9% | 0.86 | -9.3% | 302 | 1.73 | 4.3% | 25.9 | 8/8 | 0.88 | 0.65 | 0.21 | 5 | 21.3% | 0.65 | 0.78 | 75.0% | 66.8% | 4.4% | 76.0%/38.9% | 7.5 (interpolated) | pass | 0.021 (unverified) | n/a |
| 45 | `cfg_b50e` | timeframe=15min, mean_type=sma, mean_lookback=100, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 38/225/213 | 476 | 66.5% | 10.8% | 0.91 | -10.5% | 350 | 1.31 | 7.5% | 77.3 | 9/9 | 1.00 | 0.76 | 0.15 | 4 | 27.2% | 0.53 | 0.68 | 51.5% | 35.3% | 61.9% | 59.0%/38.4% | 3.6 (interpolated) | pass | 0.112 (unverified) | n/a |
| 46 | `cfg_869a` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=30, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 33/210/170 | 413 | 43.7% | 7.5% | 0.85 | -11.9% | 351 | 1.28 | 6.6% | 66.5 | 9/9 | 1.00 | 0.70 | 0.15 | 4 | 18.0% | 0.59 | 0.56 | 31.4% | 20.6% | 22.0% | 39.8%/30.1% | 3.0 (interpolated) | pass | 0.105 (unverified) | n/a |
| 47 | `cfg_0149` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 35/165/74 | 274 | 95.5% | 14.4% | 0.78 | -21.6% | 241 | 1.45 | 7.2% | 41.1 | 11/11 | 1.00 | 0.79 | -0.01 | 4 | 33.9% | 0.48 | 0.76 | 84.2% | 72.2% | 31.6% | 87.8%/57.4% | 6.3 (interpolated) | pass | 0.042 (unverified) | n/a |
| 48 | `cfg_7fd1` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 51/149/74 | 274 | 97.2% | 14.6% | 0.79 | -21.4% | 241 | 1.46 | 7.0% | 41.2 | 11/11 | 1.00 | 0.78 | 0.01 | 4 | 34.4% | 0.48 | 0.75 | 84.3% | 72.5% | 31.8% | 87.5%/64.0% | 6.3 (interpolated) | pass | 0.043 (unverified) | n/a |
| 49 | `cfg_801a` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=30, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 23/220/170 | 413 | 43.9% | 7.6% | 0.85 | -11.7% | 351 | 1.28 | 6.6% | 66.5 | 8/8 | 1.00 | 0.67 | 0.19 | 4 | 17.4% | 0.60 | 0.57 | 31.9% | 21.7% | 21.7% | 38.6%/27.5% | 3.0 (interpolated) | pass | 0.104 (unverified) | n/a |
| 50 | `cfg_7c5b` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=25, entry_z=-3.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 3/130/126 | 259 | 51.2% | 8.6% | 0.77 | -15.6% | 495 | 1.34 | 5.7% | 35.8 | 7/7 | 1.00 | 0.78 | -0.01 | 4 | 21.8% | 0.57 | 0.76 | 42.0% | 32.9% | 30.1% | 43.1%/28.1% | 4.3 (interpolated) | pass | 0.077 (unverified) | n/a |
| 51 | `cfg_bde6` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=30, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 22/64/60 | 146 | 22.9% | 4.2% | 0.85 | -7.8% | 486 | 1.48 | 2.2% | 19.6 | 9/9 | 1.00 | 0.68 | 0.17 | 3 | 8.6% | 0.58 | 0.63 | 19.1% | 14.8% | 2.6% | 21.0%/16.6% | 4.0 (interpolated) | pass | 0.112 (unverified) | n/a |
| 52 | `cfg_f251` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=25, entry_z=-3.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 8/125/126 | 259 | 52.1% | 8.8% | 0.78 | -15.6% | 495 | 1.34 | 5.7% | 35.8 | 8/8 | 1.00 | 0.77 | 0.01 | 4 | 22.0% | 0.58 | 0.75 | 42.8% | 34.3% | 31.1% | 45.3%/29.4% | 4.3 (interpolated) | pass | 0.080 (unverified) | n/a |
| 53 | `cfg_b4f0` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=25, entry_z=-2.5, exit_z=-0.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 10/119/14 | 143 | 24.8% | 4.5% | 0.81 | -9.7% | 328 | 1.52 | 2.0% | 19.5 | 11/11 | 0.91 | 0.61 | 0.20 | 4 | 9.3% | 0.56 | 0.69 | 20.9% | 16.8% | 0.0% | 22.2%/18.1% | 4.3 (interpolated) | pass | 0.106 (unverified) | n/a |
| 54 | `cfg_c606` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=25, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 32/88/87 | 207 | 34.4% | 6.1% | 0.89 | -10.0% | 329 | 1.43 | 3.2% | 29.5 | 9/9 | 0.89 | 0.69 | 0.19 | 4 | 17.9% | 0.42 | 0.64 | 27.8% | 22.4% | 10.0% | 30.3%/22.3% | 4.1 (interpolated) | pass | 0.135 (unverified) | n/a |
| 55 | `cfg_8990` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=30, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 12/74/60 | 146 | 22.1% | 4.1% | 0.83 | -7.7% | 491 | 1.47 | 2.3% | 19.6 | 10/10 | 1.00 | 0.76 | 0.06 | 3 | 7.7% | 0.61 | 0.65 | 18.4% | 14.2% | 2.1% | 19.5%/15.0% | 4.0 (interpolated) | pass | 0.103 (unverified) | n/a |
| 56 | `cfg_c0df` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 55/173/249 | 477 | 98.5% | 14.7% | 0.79 | -25.0% | 267 | 1.34 | 9.4% | 71.1 | 8/8 | 1.00 | 0.70 | 0.09 | 5 | 54.3% | 0.45 | 0.75 | 77.6% | 59.3% | 28.9% | 93.1%/41.4% | 4.0 (interpolated) | pass | 0.044 (unverified) | n/a |
| 57 | `cfg_e9f1` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 71/196/105 | 372 | 103.2% | 15.3% | 0.80 | -20.2% | 241 | 1.34 | 9.6% | 55.6 | 11/11 | 0.82 | 0.63 | 0.16 | 4 | 30.9% | 0.58 | 0.84 | 84.8% | 70.9% | 13.8% | 95.3%/62.0% | 5.3 (interpolated) | pass | 0.047 (unverified) | n/a |
| 58 | `cfg_9513` | timeframe=15min, mean_type=sma, mean_lookback=100, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 49/188/256 | 493 | 50.5% | 8.5% | 0.80 | -15.1% | 299 | 1.22 | 10.0% | 80.7 | 8/8 | 1.00 | 0.65 | 0.15 | 4 | 16.2% | 0.58 | 0.64 | 36.2% | 21.9% | 53.8% | 47.2%/29.0% | 2.9 (interpolated) | pass | 0.089 (unverified) | n/a |
| 59 | `cfg_e1d3` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 39/231/249 | 519 | 64.3% | 10.5% | 0.86 | -23.6% | 532 | 1.26 | 11.4% | 83.4 | 7/7 | 1.00 | 0.67 | 0.19 | 4 | 28.5% | 0.56 | 0.56 | 46.6% | 29.8% | 0.1% | 51.1%/28.3% | 3.2 (interpolated) | pass | 0.106 (unverified) | n/a |
| 60 | `cfg_6df8` | timeframe=15min, mean_type=sma, mean_lookback=100, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 43/193/256 | 492 | 53.5% | 9.0% | 0.83 | -15.3% | 298 | 1.23 | 10.1% | 80.6 | 7/7 | 1.00 | 0.59 | 0.24 | 4 | 17.2% | 0.58 | 0.63 | 38.8% | 25.3% | 55.8% | 52.2%/30.7% | 3.1 (interpolated) | pass | 0.099 (unverified) | n/a |
| 61 | `cfg_c487` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=30, entry_z=-3.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 8/96/93 | 197 | 44.3% | 7.6% | 0.88 | -13.4% | 227 | 1.46 | 4.4% | 31.1 | 8/8 | 1.00 | 0.72 | 0.16 | 4 | 18.6% | 0.58 | 0.68 | 39.1% | 33.3% | 34.4% | 41.2%/28.4% | 5.3 (interpolated) | pass | 0.116 (unverified) | n/a |
| 62 | `cfg_3748` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 55/35/82 | 172 | 60.6% | 10.0% | 0.75 | -14.9% | 224 | 1.63 | 3.1% | 25.7 | 9/9 | 0.78 | 0.71 | 0.05 | 5 | 34.9% | 0.42 | 0.95 | 54.3% | 48.6% | -11.3% | 57.7%/38.7% | 7.1 (interpolated) | pass | 0.072 (unverified) | n/a |
| 63 | `cfg_2a7b` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=30, entry_z=-3.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 13/91/93 | 197 | 45.7% | 7.8% | 0.89 | -13.4% | 227 | 1.47 | 4.4% | 31.2 | 8/8 | 1.00 | 0.71 | 0.19 | 4 | 19.4% | 0.58 | 0.68 | 39.2% | 33.7% | 33.7% | 39.4%/29.6% | 5.3 (interpolated) | pass | 0.118 (unverified) | n/a |
| 64 | `cfg_9a32` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.0 | 43/148/219 | 410 | 77.9% | 12.2% | 0.78 | -21.5% | 248 | 1.30 | 7.9% | 58.4 | 8/8 | 1.00 | 0.53 | 0.25 | 4 | 47.2% | 0.39 | 0.91 | 62.0% | 46.6% | 74.8% | 61.9%/26.1% | 4.0 (interpolated) | pass | 0.058 (unverified) | n/a |
| 65 | `cfg_653d` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 75/219/312 | 606 | 122.2% | 17.3% | 0.84 | -25.0% | 129 | 1.28 | 12.6% | 95.4 | 8/8 | 0.88 | 0.63 | 0.21 | 5 | 78.1% | 0.36 | 0.62 | 95.0% | 69.1% | 87.9% | 105.9%/62.0% | 4.0 (interpolated) | pass | 0.062 (unverified) | n/a |
| 66 | `cfg_e0c0` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 37/230/105 | 372 | 96.9% | 14.5% | 0.77 | -20.0% | 241 | 1.33 | 9.9% | 55.6 | 10/10 | 0.70 | 0.57 | 0.20 | 4 | 29.1% | 0.58 | 0.87 | 80.9% | 65.1% | 8.9% | 84.5%/50.7% | 5.1 (interpolated) | pass | 0.041 (unverified) | n/a |
| 67 | `cfg_55f7` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=30, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 11/134/137 | 282 | 68.5% | 11.0% | 0.83 | -17.3% | 372 | 1.49 | 6.3% | 43.9 | 9/9 | 0.89 | 0.78 | 0.05 | 4 | 25.0% | 0.64 | 0.66 | 58.1% | 48.5% | 29.5% | 59.0%/36.7% | 5.2 (interpolated) | pass | 0.057 (unverified) | n/a |
| 68 | `cfg_4fa7` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 189/35/213 | 437 | 70.2% | 11.2% | 0.76 | -22.4% | 260 | 1.28 | 6.9% | 64.7 | 7/7 | 0.86 | 0.63 | 0.13 | 4 | 33.8% | 0.52 | 0.83 | 53.2% | 39.0% | 11.4% | 66.1%/41.5% | 3.6 (interpolated) | pass | 0.058 (unverified) | n/a |
| 69 | `cfg_54e8` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 58/99/196 | 353 | 100.4% | 14.9% | 0.77 | -24.7% | 220 | 1.37 | 7.0% | 45.4 | 10/10 | 1.00 | 0.61 | 0.16 | 5 | 48.8% | 0.37 | 0.90 | 81.7% | 67.4% | 30.7% | 95.4%/72.0% | 5.0 (interpolated) | pass | 0.083 (unverified) | n/a |
| 70 | `cfg_2c94` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 18/82/10 | 110 | 23.5% | 4.3% | 0.77 | -7.8% | 242 | 1.54 | 2.2% | 13.7 | 11/11 | 0.91 | 0.56 | 0.21 | 5 | 13.8% | 0.38 | 0.80 | 20.3% | 17.0% | 13.5% | 21.4%/14.0% | 4.8 (interpolated) | pass | 0.101 (unverified) | n/a |
| 71 | `cfg_d575` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.0 | 109/216/423 | 748 | 169.1% | 21.9% | 1.08 | -20.0% | 255 | 1.30 | 13.4% | 118.5 | 8/8 | 1.00 | 0.59 | 0.49 | 3 | 45.0% | 0.49 | 0.56 | 126.9% | 93.2% | 65.2% | 140.4%/64.8% | 4.0 (interpolated) | pass | 0.210 (unverified) | n/a |
| 72 | `cfg_f026` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.0 | 70/124/216 | 410 | 77.3% | 12.1% | 0.77 | -20.8% | 248 | 1.29 | 7.7% | 58.1 | 9/9 | 1.00 | 0.66 | 0.12 | 5 | 47.3% | 0.39 | 0.94 | 61.1% | 46.7% | 72.2% | 66.7%/27.0% | 4.0 (interpolated) | pass | 0.057 (unverified) | n/a |
| 73 | `cfg_8f4d` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=30, entry_z=-3.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 16/129/137 | 282 | 68.9% | 11.1% | 0.83 | -17.1% | 372 | 1.49 | 6.2% | 43.9 | 9/9 | 0.89 | 0.77 | 0.06 | 4 | 25.4% | 0.63 | 0.66 | 58.0% | 49.6% | 28.2% | 62.0%/43.3% | 5.2 (interpolated) | pass | 0.058 (unverified) | n/a |
| 74 | `cfg_cc63` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 74/285/387 | 746 | 141.5% | 19.3% | 0.88 | -22.9% | 477 | 1.27 | 10.6% | 113.3 | 9/9 | 0.78 | 0.53 | 0.36 | 4 | 12.6% | 0.73 | 0.80 | 103.1% | 72.6% | 82.8% | 120.6%/62.1% | 3.7 (interpolated) | pass | 0.097 (unverified) | n/a |
| 75 | `cfg_6646` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 50/220/249 | 519 | 57.9% | 9.6% | 0.80 | -24.6% | 532 | 1.24 | 11.3% | 83.4 | 8/8 | 1.00 | 0.69 | 0.12 | 4 | 26.4% | 0.54 | 0.60 | 41.3% | 24.4% | -0.9% | 44.8%/28.6% | 3.0 (interpolated) | pass | 0.083 (unverified) | n/a |
| 76 | `cfg_031e` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 93/202/311 | 606 | 113.0% | 16.4% | 0.80 | -24.2% | 129 | 1.27 | 12.2% | 94.9 | 9/9 | 0.89 | 0.62 | 0.18 | 5 | 69.0% | 0.39 | 0.67 | 88.8% | 62.6% | 79.5% | 96.1%/61.0% | 3.8 (interpolated) | pass | 0.051 (unverified) | n/a |
| 77 | `cfg_ed83` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 7/93/10 | 110 | 23.7% | 4.3% | 0.77 | -8.7% | 245 | 1.55 | 2.2% | 13.8 | 12/12 | 0.92 | 0.51 | 0.26 | 5 | 15.3% | 0.32 | 0.79 | 20.4% | 17.4% | 11.4% | 22.2%/14.5% | 4.9 (interpolated) | pass | 0.101 (unverified) | n/a |
| 78 | `cfg_253d` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.0 | 185/148/415 | 748 | 136.0% | 18.8% | 0.93 | -17.6% | 238 | 1.26 | 12.4% | 116.2 | 9/9 | 0.78 | 0.57 | 0.37 | 4 | 39.1% | 0.51 | 0.71 | 101.2% | 67.7% | 44.7% | 117.8%/69.4% | 3.6 (interpolated) | pass | 0.119 (unverified) | n/a |
| 79 | `cfg_6ec6` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 25/114/125 | 264 | 43.1% | 7.4% | 0.78 | -18.0% | 446 | 1.36 | 5.8% | 39.2 | 9/9 | 1.00 | 0.66 | 0.12 | 4 | 11.3% | 0.74 | 0.70 | 34.5% | 26.8% | 10.0% | 41.7%/27.8% | 4.0 (interpolated) | pass | 0.080 (unverified) | n/a |
| 80 | `cfg_0ec3` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 19/120/125 | 264 | 45.1% | 7.7% | 0.81 | -17.8% | 446 | 1.37 | 5.9% | 39.3 | 8/8 | 1.00 | 0.59 | 0.21 | 4 | 10.3% | 0.77 | 0.67 | 35.9% | 28.5% | 10.5% | 40.6%/28.9% | 4.1 (interpolated) | pass | 0.085 (unverified) | n/a |
| 81 | `cfg_2c0c` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.0 | 257/88/409 | 754 | 94.4% | 14.2% | 0.79 | -19.0% | 478 | 1.20 | 11.5% | 116.6 | 8/8 | 0.75 | 0.41 | 0.38 | 4 | 30.8% | 0.50 | 0.85 | 64.1% | 37.3% | 27.0% | 81.6%/30.1% | 3.0 (interpolated) | pass | 0.072 (unverified) | n/a |
| 82 | `cfg_b28f` | timeframe=15min, mean_type=sma, mean_lookback=100, std_lookback=20, entry_z=-2.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 51/180/246 | 477 | 49.0% | 8.3% | 0.77 | -11.6% | 378 | 1.22 | 9.7% | 82.1 | 9/9 | 0.78 | 0.54 | 0.23 | 4 | 22.9% | 0.53 | 0.65 | 34.8% | 22.1% | 41.6% | 43.5%/24.7% | 3.1 (interpolated) | pass | 0.078 (unverified) | n/a |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | -0.5% / -0.08 / 46 | 11.2% / 1.62 / 43 | 161.0% / 2.56 / 59 | 19.5% / 2.31 / 38 | 2.0% / 0.23 / 49 |
| 2 | -0.5% / -0.08 / 46 | 12.1% / 1.63 / 43 | 155.3% / 2.51 / 59 | 20.9% / 2.41 / 38 | 1.6% / 0.20 / 49 |
| 3 | 2.4% / 0.47 / 66 | 8.2% / 1.15 / 56 | 103.6% / 2.07 / 84 | 15.2% / 1.94 / 46 | 14.7% / 1.16 / 65 |
| 4 | 2.0% / 0.40 / 66 | 6.6% / 0.96 / 56 | 103.5% / 2.07 / 84 | 13.5% / 1.76 / 46 | 16.8% / 1.32 / 65 |
| 5 | -3.3% / -0.56 / 58 | 5.8% / 0.87 / 48 | 80.1% / 1.70 / 71 | 22.1% / 2.54 / 43 | 13.5% / 1.20 / 53 |
| 6 | -4.3% / -0.74 / 58 | 6.4% / 0.94 / 48 | 82.3% / 1.73 / 71 | 21.9% / 2.55 / 43 | 12.5% / 1.13 / 53 |
| 7 | -3.3% / -0.64 / 73 | 5.4% / 0.79 / 61 | 73.9% / 1.71 / 93 | 15.9% / 1.94 / 53 | 17.4% / 1.47 / 69 |
| 8 | -2.2% / -0.41 / 73 | 4.9% / 0.72 / 61 | 71.6% / 1.67 / 93 | 17.1% / 2.06 / 53 | 18.3% / 1.53 / 69 |
| 9 | -1.8% / -0.14 / 95 | 4.7% / 0.60 / 78 | 111.3% / 1.76 / 102 | 14.1% / 1.44 / 64 | 31.4% / 1.91 / 82 |
| 10 | -2.3% / -0.19 / 97 | 7.3% / 0.89 / 78 | 125.9% / 1.84 / 102 | 9.7% / 1.08 / 64 | 29.9% / 1.85 / 82 |
| 11 | 0.5% / 0.12 / 56 | 2.6% / 0.59 / 30 | 35.9% / 1.77 / 56 | 8.2% / 1.27 / 14 | 17.2% / 1.79 / 27 |
| 12 | -0.2% / -0.01 / 56 | 2.1% / 0.49 / 30 | 35.8% / 1.77 / 56 | 8.7% / 1.29 / 14 | 18.0% / 1.82 / 27 |
| 13 | -3.6% / -0.70 / 55 | 3.5% / 0.52 / 51 | 53.8% / 1.60 / 64 | 20.6% / 2.72 / 41 | 10.4% / 1.23 / 51 |
| 14 | -3.7% / -0.72 / 55 | 3.4% / 0.50 / 51 | 54.0% / 1.61 / 64 | 20.2% / 2.64 / 41 | 10.7% / 1.26 / 51 |
| 15 | 2.1% / 0.39 / 42 | -0.3% / -0.06 / 26 | 10.5% / 1.19 / 40 | 10.6% / 2.88 / 16 | 12.8% / 1.35 / 39 |
| 16 | 4.0% / 1.20 / 23 | 0.2% / 0.07 / 15 | 3.2% / 0.57 / 28 | 3.6% / 1.62 / 12 | 15.4% / 1.79 / 27 |
| 17 | 2.1% / 0.39 / 42 | -0.4% / -0.07 / 26 | 10.5% / 1.19 / 40 | 10.6% / 2.88 / 16 | 12.8% / 1.35 / 39 |
| 18 | 4.2% / 1.24 / 23 | 0.2% / 0.09 / 15 | 3.0% / 0.54 / 28 | 3.6% / 1.62 / 12 | 15.4% / 1.79 / 27 |
| 19 | -4.6% / -0.53 / 84 | 5.1% / 0.74 / 68 | 35.4% / 1.42 / 72 | 30.9% / 3.03 / 55 | 5.7% / 0.54 / 65 |
| 20 | -4.3% / -0.50 / 84 | 5.9% / 0.83 / 68 | 33.3% / 1.36 / 72 | 29.7% / 2.98 / 55 | 5.8% / 0.55 / 65 |
| 21 | 13.5% / 1.41 / 140 | 3.0% / 0.40 / 106 | 54.2% / 1.30 / 142 | 12.8% / 1.09 / 104 | 9.2% / 0.62 / 128 |
| 22 | 8.6% / 1.01 / 144 | 3.0% / 0.39 / 110 | 74.3% / 1.61 / 149 | 16.2% / 1.38 / 102 | -0.4% / 0.05 / 122 |
| 23 | 7.6% / 0.90 / 144 | 3.0% / 0.38 / 110 | 74.4% / 1.61 / 149 | 17.0% / 1.44 / 102 | 0.1% / 0.08 / 122 |
| 24 | 4.8% / 1.40 / 28 | -2.3% / -0.88 / 18 | 16.4% / 2.04 / 29 | 7.4% / 2.25 / 9 | 2.2% / 0.42 / 23 |
| 25 | 6.5% / 1.14 / 67 | -0.5% / -0.06 / 53 | 29.3% / 0.99 / 68 | 12.1% / 1.74 / 41 | 23.3% / 2.00 / 64 |
| 26 | 4.8% / 1.40 / 28 | -2.3% / -0.88 / 18 | 16.1% / 2.04 / 29 | 7.4% / 2.25 / 9 | 2.1% / 0.41 / 23 |
| 27 | 1.3% / 0.27 / 66 | 1.7% / 0.34 / 55 | 40.2% / 1.25 / 68 | 10.3% / 1.44 / 42 | 19.8% / 1.87 / 65 |
| 28 | 12.7% / 1.36 / 140 | 2.5% / 0.34 / 106 | 52.6% / 1.28 / 142 | 13.4% / 1.13 / 104 | 3.8% / 0.31 / 127 |
| 29 | 3.9% / 0.71 / 57 | 0.8% / 0.19 / 44 | 1.8% / 0.19 / 67 | 6.7% / 1.53 / 33 | 34.1% / 2.53 / 64 |
| 30 | 3.9% / 0.71 / 57 | 0.8% / 0.19 / 44 | 1.8% / 0.19 / 67 | 6.4% / 1.49 / 33 | 34.3% / 2.53 / 64 |
| 31 | 4.3% / 0.63 / 106 | 4.7% / 0.70 / 89 | 15.4% / 0.57 / 127 | 22.4% / 2.52 / 65 | 22.7% / 1.71 / 91 |
| 32 | 8.0% / 1.05 / 99 | 2.9% / 0.48 / 80 | 49.2% / 1.19 / 112 | 14.0% / 1.30 / 68 | 17.0% / 1.22 / 91 |
| 33 | 5.6% / 0.74 / 106 | 3.8% / 0.57 / 89 | 24.8% / 0.75 / 127 | 22.6% / 2.42 / 65 | 23.4% / 1.67 / 91 |
| 34 | 8.0% / 2.02 / 42 | -0.6% / -0.13 / 33 | -2.4% / -0.15 / 55 | 7.5% / 1.97 / 24 | 17.3% / 1.76 / 47 |
| 35 | 1.5% / 0.32 / 55 | 1.7% / 0.38 / 51 | 14.4% / 1.26 / 64 | -0.2% / 0.00 / 36 | 19.3% / 1.90 / 58 |
| 36 | 2.1% / 0.42 / 55 | 1.9% / 0.41 / 51 | 12.3% / 1.10 / 64 | -0.1% / 0.01 / 36 | 21.5% / 2.01 / 58 |
| 37 | 4.1% / 0.61 / 100 | 3.5% / 0.65 / 80 | 49.9% / 1.27 / 114 | 19.1% / 1.80 / 67 | 3.8% / 0.37 / 88 |
| 38 | 8.6% / 2.07 / 42 | -0.9% / -0.20 / 33 | -2.4% / -0.15 / 55 | 7.7% / 2.00 / 24 | 17.0% / 1.74 / 47 |
| 39 | -3.6% / -0.46 / 118 | 10.6% / 1.63 / 86 | 7.9% / 0.48 / 103 | 32.0% / 3.11 / 72 | 10.9% / 0.88 / 97 |
| 40 | 3.3% / 0.97 / 33 | -4.7% / -1.27 / 23 | 14.2% / 1.53 / 40 | 6.1% / 1.49 / 19 | 5.8% / 0.93 / 29 |
| 41 | 5.5% / 1.17 / 48 | -1.8% / -0.38 / 42 | 13.6% / 1.26 / 52 | 2.8% / 0.69 / 26 | 12.1% / 1.35 / 39 |
| 42 | 2.8% / 0.52 / 52 | 4.8% / 0.98 / 31 | 50.6% / 1.43 / 57 | 2.8% / 1.12 / 10 | 10.0% / 1.02 / 44 |
| 43 | 12.9% / 1.47 / 108 | 2.1% / 0.31 / 91 | 12.6% / 0.48 / 124 | 19.6% / 2.03 / 65 | 29.4% / 1.91 / 89 |
| 44 | 2.7% / 0.50 / 52 | 4.0% / 0.86 / 31 | 50.8% / 1.43 / 57 | 2.8% / 1.12 / 10 | 10.5% / 1.05 / 44 |
| 45 | -3.5% / -0.45 / 118 | 11.4% / 1.74 / 86 | 6.1% / 0.40 / 103 | 31.0% / 3.07 / 72 | 11.4% / 0.91 / 97 |
| 46 | 7.2% / 0.97 / 86 | 2.3% / 0.39 / 84 | -0.3% / 0.03 / 91 | 8.0% / 1.23 / 57 | 21.8% / 1.64 / 95 |
| 47 | -1.9% / -0.24 / 60 | 2.6% / 0.39 / 50 | 46.0% / 1.14 / 67 | 23.8% / 2.61 / 41 | 7.5% / 0.63 / 56 |
| 48 | -2.2% / -0.28 / 60 | 3.1% / 0.46 / 50 | 46.7% / 1.15 / 67 | 23.2% / 2.57 / 41 | 8.1% / 0.67 / 56 |
| 49 | 6.1% / 0.84 / 86 | 2.7% / 0.45 / 84 | -0.2% / 0.04 / 91 | 7.9% / 1.22 / 57 | 22.5% / 1.67 / 95 |
| 50 | 10.2% / 1.58 / 63 | -3.6% / -0.64 / 46 | 10.3% / 0.58 / 77 | 3.9% / 0.64 / 21 | 24.2% / 1.85 / 52 |
| 51 | 5.5% / 1.47 / 32 | -5.0% / -1.56 / 29 | 13.2% / 1.80 / 39 | -0.5% / -0.15 / 21 | 8.9% / 1.37 / 25 |
| 52 | 10.2% / 1.58 / 63 | -3.4% / -0.60 / 46 | 10.4% / 0.58 / 77 | 3.8% / 0.63 / 21 | 24.7% / 1.86 / 52 |
| 53 | 3.3% / 0.97 / 33 | -4.7% / -1.27 / 23 | 14.2% / 1.53 / 40 | 6.6% / 1.56 / 19 | 4.1% / 0.69 / 28 |
| 54 | 5.8% / 1.25 / 48 | -2.1% / -0.48 / 42 | 13.9% / 1.29 / 52 | 2.9% / 0.70 / 26 | 10.7% / 1.24 / 39 |
| 55 | 4.8% / 1.31 / 32 | -4.4% / -1.28 / 29 | 13.4% / 1.82 / 39 | -1.0% / -0.31 / 21 | 8.6% / 1.34 / 25 |
| 56 | 11.9% / 1.39 / 108 | 0.9% / 0.16 / 91 | 12.4% / 0.48 / 124 | 21.6% / 2.20 / 65 | 28.6% / 1.88 / 89 |
| 57 | 10.3% / 1.07 / 87 | -2.1% / -0.23 / 70 | 55.2% / 1.31 / 81 | 4.7% / 0.48 / 62 | 15.8% / 1.03 / 72 |
| 58 | 3.9% / 0.50 / 119 | 3.0% / 0.45 / 88 | -8.0% / -0.52 / 104 | 29.6% / 2.55 / 79 | 18.0% / 1.29 / 103 |
| 59 | 3.6% / 0.46 / 111 | -2.0% / -0.20 / 103 | 11.6% / 0.68 / 117 | 13.4% / 1.40 / 85 | 27.8% / 1.91 / 103 |
| 60 | 4.5% / 0.57 / 119 | 2.5% / 0.38 / 87 | -6.2% / -0.37 / 104 | 31.0% / 2.61 / 79 | 16.6% / 1.21 / 103 |
| 61 | -2.5% / -0.35 / 52 | 11.0% / 2.05 / 29 | 1.4% / 0.17 / 49 | 8.1% / 1.47 / 24 | 21.6% / 1.87 / 43 |
| 62 | 1.5% / 0.38 / 33 | 2.4% / 0.58 / 27 | 20.2% / 0.78 / 43 | 7.9% / 1.22 / 29 | 19.1% / 1.97 / 40 |
| 63 | -2.3% / -0.32 / 52 | 11.2% / 2.07 / 29 | 1.7% / 0.20 / 49 | 8.1% / 1.47 / 24 | 22.0% / 1.84 / 43 |
| 64 | -0.8% / -0.07 / 79 | 4.1% / 0.64 / 65 | 23.2% / 0.83 / 106 | 15.7% / 1.84 / 70 | 20.9% / 1.23 / 90 |
| 65 | 6.2% / 0.64 / 139 | 15.1% / 1.55 / 95 | 19.5% / 0.62 / 142 | 21.9% / 1.78 / 96 | 24.8% / 1.28 / 134 |
| 66 | 9.1% / 0.99 / 87 | -1.5% / -0.14 / 70 | 52.6% / 1.27 / 81 | 4.8% / 0.50 / 62 | 14.5% / 0.95 / 72 |
| 67 | -1.9% / -0.30 / 67 | 3.3% / 0.65 / 44 | 19.4% / 0.81 / 69 | 3.3% / 0.43 / 45 | 34.9% / 2.62 / 57 |
| 68 | 8.2% / 1.20 / 96 | -2.5% / -0.28 / 75 | 6.8% / 0.36 / 115 | 18.8% / 2.20 / 64 | 27.2% / 1.86 / 87 |
| 69 | 5.0% / 0.75 / 81 | 3.1% / 0.31 / 66 | 34.7% / 0.91 / 99 | 13.7% / 1.71 / 40 | 20.9% / 1.50 / 67 |
| 70 | 3.9% / 1.19 / 28 | 0.4% / 0.13 / 19 | 8.5% / 0.93 / 31 | 5.7% / 1.95 / 9 | 3.2% / 0.49 / 23 |
| 71 | -3.6% / -0.29 / 152 | -0.4% / 0.01 / 122 | 85.6% / 1.91 / 179 | 21.0% / 1.61 / 132 | 24.7% / 1.22 / 163 |
| 72 | 0.3% / 0.08 / 79 | 2.8% / 0.45 / 65 | 24.8% / 0.87 / 106 | 14.4% / 1.77 / 70 | 20.3% / 1.20 / 90 |
| 73 | -1.9% / -0.30 / 67 | 3.6% / 0.71 / 44 | 19.4% / 0.81 / 69 | 3.2% / 0.43 / 45 | 34.7% / 2.59 / 57 |
| 74 | -9.9% / -1.18 / 142 | 0.5% / 0.10 / 127 | 114.6% / 1.94 / 180 | 20.9% / 1.81 / 133 | 2.9% / 0.24 / 164 |
| 75 | 3.0% / 0.39 / 111 | -3.0% / -0.32 / 103 | 13.3% / 0.75 / 117 | 11.6% / 1.25 / 85 | 24.9% / 1.79 / 103 |
| 76 | 5.3% / 0.56 / 139 | 13.2% / 1.45 / 95 | 21.9% / 0.67 / 142 | 16.5% / 1.45 / 96 | 26.0% / 1.33 / 134 |
| 77 | 4.0% / 1.14 / 28 | 0.5% / 0.19 / 19 | 7.2% / 0.80 / 31 | 6.1% / 1.96 / 9 | 4.0% / 0.59 / 23 |
| 78 | -1.5% / -0.10 / 152 | 0.2% / 0.07 / 122 | 69.6% / 1.59 / 179 | 19.2% / 1.58 / 132 | 18.2% / 0.96 / 163 |
| 79 | 4.7% / 0.76 / 57 | -2.4% / -0.39 / 49 | 7.7% / 0.56 / 70 | 1.1% / 0.19 / 37 | 28.6% / 2.46 / 51 |
| 80 | 4.9% / 0.79 / 57 | -2.1% / -0.32 / 49 | 6.0% / 0.46 / 70 | 1.2% / 0.20 / 37 | 31.5% / 2.54 / 51 |
| 81 | -3.8% / -0.36 / 152 | 1.6% / 0.21 / 124 | 48.6% / 1.32 / 181 | 20.4% / 1.78 / 134 | 11.2% / 0.66 / 163 |
| 82 | 1.5% / 0.21 / 119 | -0.8% / -0.07 / 85 | 1.1% / 0.15 / 89 | 20.8% / 1.83 / 82 | 21.2% / 1.42 / 102 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_0055` | 3 | 0.97 | 0.99/0.99 | 0.98/0.98 |
| 1 | `cfg_bb70` | 133 | 0.80 | 0.09/0.60 | 0.02/0.30 |
| 2 | `cfg_f1d8` | 274 | 0.83 | 0.06/0.66 | 0.00/0.41 |
| 3 | `cfg_c487` | 4 | 0.99 | 1.00/1.00 | 0.95/0.99 |
| 4 | `cfg_0149` | 3 | 0.98 | 0.99/1.00 | 0.99/0.99 |
| 5 | `cfg_b397` | 15 | 0.91 | 0.82/0.93 | 0.57/0.74 |
| 6 | `cfg_9513` | 4 | 0.95 | 0.97/0.99 | 0.94/0.99 |
| 7 | `cfg_b3df` | 16 | 0.88 | 0.80/0.82 | 0.63/0.65 |
| 8 | `cfg_653d` | 2 | 0.99 | 1.00/1.00 | 0.99/0.99 |
| 9 | `cfg_7f8d` | 8 | 0.97 | 0.96/0.97 | 0.98/0.98 |
| 10 | `cfg_e30b` | 10 | 0.80 | 0.85/0.94 | 0.56/0.72 |
| 11 | `cfg_ce65` | 4 | 0.98 | 0.98/0.99 | 0.99/0.99 |
| 12 | `cfg_fe55` | 8 | 0.95 | 0.95/0.96 | 0.93/0.93 |
| 13 | `cfg_0729` | 4 | 0.98 | 0.97/0.99 | 0.95/0.99 |
| 14 | `cfg_5f93` | 12 | 0.84 | 0.37/0.92 | 0.21/0.87 |
| 15 | `cfg_8b81` | 12 | 0.84 | 0.54/0.55 | 0.22/0.23 |
| 16 | `cfg_cb6e` | 4 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 17 | `cfg_6ec6` | 3 | 0.98 | 0.99/0.99 | 0.97/0.98 |
| 18 | `cfg_baf9` | 25 | 0.84 | 0.78/0.86 | 0.49/0.52 |
| 19 | `cfg_a8cc` | 7 | 0.89 | 0.91/0.97 | 0.71/0.98 |
| 20 | `cfg_1166` | 8 | 0.92 | 0.89/0.89 | 0.75/0.76 |
| 21 | `cfg_7223` | 5 | 0.85 | 0.84/0.99 | 0.69/0.99 |
| 22 | `cfg_3fcb` | 8 | 0.91 | 0.83/0.83 | 0.71/0.74 |
| 23 | `cfg_39ee` | 8 | 0.87 | 0.90/0.91 | 0.56/0.57 |
| 24 | `cfg_2ca6` | 4 | 0.99 | 1.00/1.00 | 0.95/1.00 |
| 25 | `cfg_d575` | 10 | 0.90 | 0.86/0.92 | 0.68/0.82 |
| 26 | `cfg_22b5` | 2 | 0.99 | 1.00/1.00 | 0.98/0.98 |
| 27 | `cfg_253d` | 2 | 0.95 | 0.98/0.98 | 0.93/0.93 |
| 28 | `cfg_2c94` | 6 | 0.88 | 0.91/0.93 | 0.80/0.82 |
| 29 | `cfg_3748` | 1 | n/a | n/a/n/a | n/a/n/a |
| 30 | `cfg_bde6` | 4 | 0.99 | 0.99/0.99 | 0.98/0.99 |
| 31 | `cfg_4509` | 7 | 0.81 | 0.74/0.86 | 0.49/0.72 |
| 32 | `cfg_4fa7` | 1 | n/a | n/a/n/a | n/a/n/a |
| 33 | `cfg_9db1` | 5 | 0.83 | 0.17/0.97 | 0.27/0.98 |
| 34 | `cfg_54e8` | 1 | n/a | n/a/n/a | n/a/n/a |
| 35 | `cfg_55f7` | 5 | 0.80 | 0.36/1.00 | 0.56/0.97 |
| 36 | `cfg_e1d3` | 3 | 0.99 | 0.99/0.99 | 0.97/0.98 |
| 37 | `cfg_7c5b` | 3 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 38 | `cfg_869a` | 3 | 0.99 | 0.99/1.00 | 1.00/1.00 |
| 39 | `cfg_e9f1` | 3 | 1.00 | 1.00/1.00 | 0.99/1.00 |
| 40 | `cfg_fa04` | 4 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 41 | `cfg_9a32` | 3 | 0.99 | 1.00/1.00 | 0.99/0.99 |
| 42 | `cfg_b28f` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 7.824e-04 over 17136 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 733.0, participation ratio 13.0, 95%-variance components 160 (rank bound T = 1258); raw grid 17280; raw + known prior 833928
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
