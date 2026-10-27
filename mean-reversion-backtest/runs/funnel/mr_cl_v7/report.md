# Screening funnel -- mr_cl_v7 (development stages only)

- Code: `7ba1d7ded49f` (dirty working tree: True, diff sha256 `0f1ba917fe4d`)
- Config: `configs/funnel/mr_funnel_cl_v7.yaml` sha256 `d2641c9a1fbb504b`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'CL': '2026-10-16'}
- Frozen manifest sha256: `3e62dd97718667cf` (150 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_cl_v5 gated 75 CL candidates on 2023-2024 (7 passed, all 15min) and mr_cl_v6 gated 82 (4 passed); this v7 grid was written after reading both, so CL 2023-2024 is largely in-sample here.
- Holdout 2025+ previously inspected: **False** -- No CL strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection). The ES/NQ/YM/RTY index holdouts have been scored (unrelated market).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 16128 | 16128 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 16128 | 16128 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 16128 | 12149 | 3979 | 0 |  | 14116 | 75.33 | 75.33 |  |
| 3 performance & risk | hard_gate | 12149 | 1925 | 10224 | 0 |  | 0 | 11.94 | 15.84 |  |
| 4 parameter stability | hard_gate | 1925 | 1905 | 20 | 0 |  | 0 | 11.81 | 98.96 |  |
| 5 time stability | hard_gate | 1905 | 1809 | 96 | 0 |  | 1779 | 11.22 | 94.96 |  |
| 6 deduplication | dedup | 1809 | 150 |  |  | 1659 |  | 0.93 | 8.29 | best 2 per cluster |
| 7 execution stress | hard_gate | 150 | 150 | 0 | 0 |  | 8 | 0.93 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 150 |  |  |  |  |  |  |  | diagnostic only: unverified: 150 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 3979 |
| s2:hard_reject:years_with_>=10_trades | 2707 |
| s3:hard_reject:max_drawdown | 3158 |
| s3:hard_reject:net_return | 2701 |
| s3:hard_reject:sharpe | 10184 |
| s4:hard_reject:local_frac_profitable | 4 |
| s4:hard_reject:local_median_sharpe | 18 |
| s5:hard_reject:profitable_years | 96 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | transfer dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_957d` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 36/151/79 | 266 | 250.7% | 28.6% | 1.38 | -9.1% | 255 | 2.04 | 4.7% | 40.6 | 10/10 | 1.00 | 1.17 | 0.22 | 4 | 26.9% | 0.74 | 0.60 | 230.3% | 210.3% | 87.3% | 222.3%/161.1% | 11.4 (interpolated) | pass | 0.486 (unverified) | n/a |
| 2 | `cfg_8dad` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=20, entry_z=-3.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 18/167/81 | 266 | 249.5% | 28.5% | 1.38 | -9.2% | 249 | 2.02 | 4.9% | 40.8 | 10/10 | 1.00 | 1.17 | 0.21 | 3 | 29.2% | 0.73 | 0.60 | 226.6% | 206.9% | 84.0% | 223.5%/149.4% | 11.3 (interpolated) | pass | 0.484 (unverified) | n/a |
| 3 | `cfg_11db` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 39/152/79 | 270 | 219.4% | 26.2% | 1.29 | -14.0% | 230 | 2.09 | 4.8% | 38.1 | 11/11 | 1.00 | 1.01 | 0.28 | 4 | 40.8% | 0.59 | 0.59 | 200.8% | 181.5% | 76.0% | 182.8%/113.6% | 10.3 (interpolated) | pass | 0.396 (unverified) | n/a |
| 4 | `cfg_51c6` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 18/172/80 | 270 | 212.9% | 25.7% | 1.27 | -14.1% | 238 | 2.07 | 4.9% | 38.3 | 12/12 | 1.00 | 1.02 | 0.25 | 4 | 42.7% | 0.58 | 0.60 | 193.9% | 175.4% | 70.7% | 184.2%/117.3% | 10.2 (interpolated) | pass | 0.381 (unverified) | n/a |
| 5 | `cfg_fc56` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 29/174/122 | 325 | 173.2% | 22.3% | 1.17 | -11.7% | 208 | 1.60 | 8.0% | 52.4 | 10/10 | 1.00 | 0.98 | 0.19 | 5 | 40.0% | 0.60 | 0.62 | 154.4% | 137.7% | 43.5% | 152.7%/103.9% | 7.9 (interpolated) | pass | 0.223 (unverified) | n/a |
| 6 | `cfg_21ef` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 65/138/122 | 325 | 169.3% | 21.9% | 1.16 | -11.0% | 182 | 1.60 | 7.6% | 52.2 | 10/10 | 1.00 | 0.98 | 0.18 | 5 | 39.3% | 0.60 | 0.61 | 150.5% | 132.1% | 42.9% | 145.5%/94.7% | 7.8 (interpolated) | pass | 0.215 (unverified) | n/a |
| 7 | `cfg_b3df` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=20, entry_z=-3.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 23/128/166 | 317 | 198.1% | 24.5% | 1.27 | -13.9% | 215 | 1.78 | 6.4% | 45.7 | 8/8 | 1.00 | 1.04 | 0.23 | 5 | 46.4% | 0.58 | 0.60 | 177.7% | 158.1% | 80.3% | 178.1%/124.5% | 8.5 (interpolated) | pass | 0.391 (unverified) | n/a |
| 8 | `cfg_8217` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 34/287/138 | 459 | 265.6% | 29.7% | 1.22 | -13.5% | 248 | 1.67 | 8.3% | 69.9 | 10/10 | 1.00 | 1.02 | 0.19 | 4 | 53.2% | 0.53 | 0.54 | 228.8% | 193.6% | 64.7% | 214.8%/144.5% | 7.2 (interpolated) | pass | 0.328 (unverified) | n/a |
| 9 | `cfg_ba6e` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 51/102/164 | 317 | 193.3% | 24.1% | 1.25 | -14.0% | 256 | 1.78 | 6.1% | 45.6 | 8/8 | 1.00 | 1.01 | 0.24 | 5 | 44.1% | 0.58 | 0.59 | 174.3% | 154.1% | 99.8% | 186.5%/125.2% | 8.4 (interpolated) | pass | 0.380 (unverified) | n/a |
| 10 | `cfg_ec79` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 46/276/137 | 459 | 271.2% | 30.0% | 1.23 | -13.5% | 248 | 1.67 | 8.2% | 69.6 | 11/11 | 1.00 | 1.05 | 0.18 | 4 | 49.0% | 0.56 | 0.55 | 234.3% | 199.9% | 65.7% | 231.7%/142.1% | 7.3 (interpolated) | pass | 0.335 (unverified) | n/a |
| 11 | `cfg_0212` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 35/280/132 | 447 | 155.0% | 20.6% | 1.07 | -16.4% | 248 | 1.52 | 8.1% | 68.6 | 10/10 | 1.00 | 0.94 | 0.12 | 5 | 67.1% | 0.36 | 0.58 | 129.1% | 108.4% | 102.3% | 145.2%/89.6% | 5.6 (interpolated) | pass | 0.155 (unverified) | n/a |
| 12 | `cfg_68bf` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 49/266/132 | 447 | 158.1% | 20.9% | 1.08 | -14.7% | 248 | 1.52 | 8.0% | 68.4 | 11/11 | 1.00 | 0.99 | 0.08 | 5 | 63.1% | 0.39 | 0.58 | 131.0% | 111.1% | 105.2% | 145.8%/95.9% | 5.7 (interpolated) | pass | 0.164 (unverified) | n/a |
| 13 | `cfg_6d61` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 33/253/124 | 410 | 176.9% | 22.6% | 1.16 | -12.8% | 229 | 1.59 | 7.4% | 64.4 | 12/12 | 1.00 | 0.99 | 0.17 | 5 | 38.7% | 0.59 | 0.63 | 151.2% | 130.3% | 44.0% | 158.0%/85.2% | 6.7 (interpolated) | pass | 0.220 (unverified) | n/a |
| 14 | `cfg_2703` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=18, entry_z=-3.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 25/135/174 | 334 | 144.3% | 19.6% | 1.09 | -12.3% | 256 | 1.59 | 7.0% | 46.8 | 8/8 | 1.00 | 0.94 | 0.15 | 5 | 62.0% | 0.40 | 0.68 | 126.0% | 107.8% | 46.8% | 130.4%/66.9% | 6.8 (interpolated) | pass | 0.160 (unverified) | n/a |
| 15 | `cfg_321b` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=15, entry_z=-3.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 39/160/238 | 437 | 263.9% | 29.5% | 1.17 | -16.2% | 155 | 1.61 | 9.2% | 63.6 | 7/7 | 1.00 | 0.95 | 0.22 | 5 | 82.1% | 0.45 | 0.57 | 225.5% | 195.3% | 68.5% | 227.2%/131.2% | 7.4 (interpolated) | pass | 0.240 (unverified) | n/a |
| 16 | `cfg_702f` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 63/225/122 | 410 | 169.1% | 21.9% | 1.14 | -13.9% | 234 | 1.57 | 7.2% | 64.3 | 11/11 | 1.00 | 1.01 | 0.12 | 5 | 32.7% | 0.62 | 0.65 | 145.8% | 124.8% | 43.1% | 147.9%/103.1% | 6.6 (interpolated) | pass | 0.199 (unverified) | n/a |
| 17 | `cfg_976c` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=18, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 62/99/173 | 334 | 137.5% | 18.9% | 1.06 | -11.7% | 261 | 1.58 | 6.6% | 46.2 | 8/8 | 1.00 | 0.94 | 0.13 | 5 | 58.3% | 0.41 | 0.70 | 119.1% | 102.2% | 57.0% | 129.4%/87.9% | 6.5 (interpolated) | pass | 0.143 (unverified) | n/a |
| 18 | `cfg_21e3` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=18, entry_z=-3.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 28/148/104 | 280 | 169.3% | 22.0% | 1.13 | -12.8% | 160 | 1.70 | 7.0% | 41.6 | 9/9 | 1.00 | 0.94 | 0.20 | 5 | 72.8% | 0.37 | 0.58 | 152.5% | 136.0% | 68.5% | 149.9%/105.1% | 8.7 (interpolated) | pass | 0.202 (unverified) | n/a |
| 19 | `cfg_09ec` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=18, entry_z=-3.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 33/143/104 | 280 | 156.8% | 20.8% | 1.09 | -12.7% | 208 | 1.67 | 6.9% | 41.4 | 10/10 | 1.00 | 0.97 | 0.12 | 5 | 67.5% | 0.38 | 0.60 | 139.4% | 123.6% | 69.1% | 142.7%/108.2% | 8.1 (interpolated) | pass | 0.164 (unverified) | n/a |
| 20 | `cfg_5b2b` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=15, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 70/132/235 | 437 | 240.9% | 27.8% | 1.13 | -16.2% | 209 | 1.58 | 8.9% | 63.1 | 7/7 | 1.00 | 0.92 | 0.20 | 5 | 75.5% | 0.45 | 0.59 | 209.4% | 177.7% | 63.3% | 228.8%/149.1% | 7.1 (interpolated) | pass | 0.199 (unverified) | n/a |
| 21 | `cfg_895e` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 106/53/146 | 305 | 167.3% | 21.8% | 1.05 | -19.2% | 134 | 1.76 | 5.6% | 44.2 | 9/9 | 1.00 | 0.82 | 0.23 | 5 | 91.6% | 0.45 | 0.55 | 148.3% | 129.9% | 54.5% | 148.4%/117.1% | 7.7 (interpolated) | pass | 0.102 (unverified) | n/a |
| 22 | `cfg_267a` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 36/228/128 | 392 | 175.5% | 22.5% | 1.10 | -12.6% | 151 | 1.50 | 7.1% | 56.7 | 11/11 | 1.00 | 0.78 | 0.32 | 5 | 23.5% | 0.75 | 0.68 | 152.4% | 128.9% | 58.2% | 155.2%/86.8% | 6.7 (interpolated) | pass | 0.175 (unverified) | n/a |
| 23 | `cfg_daa1` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 65/119/197 | 381 | 127.5% | 17.9% | 1.00 | -14.1% | 182 | 1.49 | 7.4% | 55.7 | 9/9 | 1.00 | 0.95 | 0.05 | 5 | 50.2% | 0.45 | 0.71 | 107.4% | 90.9% | 54.7% | 118.9%/52.4% | 5.7 (interpolated) | pass | 0.107 (unverified) | n/a |
| 24 | `cfg_b5ac` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 79/190/125 | 394 | 179.1% | 22.8% | 1.06 | -12.1% | 138 | 1.52 | 6.9% | 57.0 | 11/11 | 1.00 | 0.79 | 0.26 | 5 | 23.0% | 0.74 | 0.70 | 155.3% | 131.9% | 75.0% | 152.6%/89.0% | 6.8 (interpolated) | pass | 0.128 (unverified) | n/a |
| 25 | `cfg_ec85` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 54/117/174 | 345 | 134.9% | 18.7% | 1.04 | -14.5% | 182 | 1.56 | 6.9% | 52.4 | 7/7 | 1.00 | 0.87 | 0.17 | 5 | 54.0% | 0.43 | 0.65 | 115.8% | 100.4% | 43.1% | 124.3%/94.0% | 6.4 (interpolated) | pass | 0.119 (unverified) | n/a |
| 26 | `cfg_6ddc` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 70/120/116 | 306 | 136.2% | 18.8% | 1.01 | -14.9% | 234 | 1.56 | 7.0% | 48.2 | 10/10 | 1.00 | 0.97 | 0.04 | 4 | 39.7% | 0.53 | 0.64 | 119.7% | 104.4% | 33.3% | 128.6%/78.0% | 7.3 (interpolated) | pass | 0.108 (unverified) | n/a |
| 27 | `cfg_6599` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=18, entry_z=-3.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 28/158/127 | 313 | 186.3% | 23.5% | 1.17 | -13.1% | 94 | 1.63 | 7.6% | 48.8 | 9/9 | 1.00 | 1.08 | 0.09 | 5 | 60.1% | 0.47 | 0.59 | 167.9% | 148.8% | 42.9% | 161.6%/105.4% | 8.3 (interpolated) | pass | 0.284 (unverified) | n/a |
| 28 | `cfg_0f67` | timeframe=15min, mean_type=ema, mean_lookback=55, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 21/232/71 | 324 | 152.1% | 20.4% | 1.05 | -15.0% | 161 | 1.62 | 6.2% | 47.7 | 11/11 | 1.00 | 0.80 | 0.25 | 5 | 50.5% | 0.47 | 0.66 | 133.0% | 116.4% | 38.1% | 129.3%/78.2% | 7.2 (interpolated) | pass | 0.179 (unverified) | n/a |
| 29 | `cfg_882f` | timeframe=15min, mean_type=ema, mean_lookback=55, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 29/225/70 | 324 | 150.2% | 20.2% | 1.04 | -15.2% | 161 | 1.62 | 6.2% | 47.4 | 12/12 | 1.00 | 0.83 | 0.21 | 5 | 48.7% | 0.49 | 0.67 | 133.1% | 115.3% | 34.2% | 130.7%/81.3% | 7.2 (interpolated) | pass | 0.175 (unverified) | n/a |
| 30 | `cfg_5016` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=18, entry_z=-3.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 34/153/126 | 313 | 176.2% | 22.6% | 1.14 | -13.3% | 103 | 1.62 | 7.6% | 48.8 | 10/10 | 1.00 | 1.07 | 0.07 | 5 | 57.3% | 0.47 | 0.60 | 158.1% | 137.2% | 39.3% | 161.7%/85.9% | 8.0 (interpolated) | pass | 0.254 (unverified) | n/a |
| 31 | `cfg_0681` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 52/244/133 | 429 | 188.5% | 23.6% | 1.05 | -13.8% | 227 | 1.54 | 7.6% | 69.2 | 11/11 | 1.00 | 0.90 | 0.15 | 5 | 29.7% | 0.67 | 0.75 | 165.1% | 139.6% | 17.2% | 170.3%/104.5% | 6.7 (interpolated) | pass | 0.149 (unverified) | n/a |
| 32 | `cfg_372f` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 38/151/115 | 304 | 137.4% | 18.9% | 1.02 | -15.4% | 234 | 1.56 | 7.3% | 48.2 | 11/11 | 1.00 | 0.98 | 0.03 | 4 | 40.6% | 0.53 | 0.63 | 121.0% | 105.9% | 34.8% | 125.7%/61.4% | 7.4 (interpolated) | pass | 0.112 (unverified) | n/a |
| 33 | `cfg_6589` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 113/176/226 | 515 | 157.9% | 20.9% | 1.02 | -17.8% | 226 | 1.52 | 7.5% | 77.5 | 9/9 | 1.00 | 0.91 | 0.11 | 5 | 75.0% | 0.33 | 0.59 | 129.2% | 103.9% | 93.3% | 147.7%/103.6% | 5.1 (interpolated) | pass | 0.128 (unverified) | n/a |
| 34 | `cfg_02bc` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 70/101/181 | 352 | 126.3% | 17.8% | 1.00 | -14.1% | 229 | 1.54 | 6.7% | 51.0 | 9/9 | 1.00 | 0.96 | 0.03 | 5 | 55.0% | 0.40 | 0.67 | 107.0% | 92.4% | 57.3% | 125.5%/65.2% | 6.0 (interpolated) | pass | 0.104 (unverified) | n/a |
| 35 | `cfg_fa04` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 26/209/27 | 262 | 104.5% | 15.4% | 1.05 | -14.7% | 339 | 1.76 | 3.6% | 37.4 | 10/10 | 0.90 | 0.82 | 0.23 | 4 | 32.9% | 0.51 | 0.69 | 91.9% | 82.0% | 51.7% | 94.3%/71.2% | 6.9 (interpolated) | pass | 0.140 (unverified) | n/a |
| 36 | `cfg_7184` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=18, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 47/165/92 | 304 | 135.1% | 18.7% | 0.99 | -13.9% | 287 | 1.60 | 5.5% | 43.5 | 11/11 | 1.00 | 0.89 | 0.10 | 4 | 35.7% | 0.57 | 0.70 | 118.9% | 102.9% | 33.0% | 123.1%/68.9% | 7.1 (interpolated) | pass | 0.095 (unverified) | n/a |
| 37 | `cfg_8ddf` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=22, entry_z=-3.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 16/112/129 | 257 | 117.5% | 16.8% | 1.00 | -13.9% | 228 | 1.73 | 5.3% | 35.0 | 8/8 | 1.00 | 0.93 | 0.07 | 4 | 26.4% | 0.64 | 0.77 | 103.9% | 91.4% | 33.5% | 114.2%/72.2% | 7.4 (interpolated) | pass | 0.119 (unverified) | n/a |
| 38 | `cfg_e1b2` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=18, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 31/180/93 | 304 | 136.0% | 18.8% | 0.99 | -14.1% | 286 | 1.59 | 5.6% | 43.6 | 12/12 | 1.00 | 0.88 | 0.12 | 4 | 33.9% | 0.60 | 0.70 | 120.4% | 104.6% | 33.1% | 125.9%/93.6% | 7.1 (interpolated) | pass | 0.097 (unverified) | n/a |
| 39 | `cfg_9384` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 18/216/28 | 262 | 104.1% | 15.4% | 1.05 | -14.5% | 400 | 1.76 | 3.6% | 37.4 | 11/11 | 0.91 | 0.82 | 0.23 | 4 | 32.5% | 0.52 | 0.69 | 91.7% | 81.1% | 52.6% | 91.3%/68.1% | 6.9 (interpolated) | pass | 0.138 (unverified) | n/a |
| 40 | `cfg_973e` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=22, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 32/97/128 | 257 | 107.1% | 15.7% | 0.94 | -13.9% | 228 | 1.68 | 5.1% | 34.9 | 8/8 | 1.00 | 0.90 | 0.04 | 4 | 21.6% | 0.67 | 0.82 | 95.0% | 83.3% | 35.2% | 105.5%/77.5% | 7.0 (interpolated) | pass | 0.093 (unverified) | n/a |
| 41 | `cfg_fe55` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=25, entry_z=-3.0, exit_z=0.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 4/144/15 | 163 | 40.3% | 7.0% | 1.04 | -6.6% | 319 | 1.72 | 2.3% | 25.1 | 10/10 | 1.00 | 0.73 | 0.31 | 4 | 24.4% | 0.40 | 0.60 | 35.2% | 30.3% | 13.2% | 38.2%/29.9% | 5.6 (interpolated) | pass | 0.190 (unverified) | n/a |
| 42 | `cfg_cb6e` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 10/58/37 | 105 | 28.6% | 5.2% | 1.03 | -6.1% | 337 | 1.77 | 1.7% | 14.7 | 10/10 | 1.00 | 0.81 | 0.22 | 5 | 11.4% | 0.60 | 0.66 | 25.1% | 22.1% | 28.6% | 27.0%/18.9% | 6.0 (interpolated) | pass | 0.182 (unverified) | n/a |
| 43 | `cfg_2b82` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 52/100/152 | 304 | 120.8% | 17.2% | 0.97 | -14.3% | 172 | 1.58 | 6.1% | 44.1 | 10/10 | 1.00 | 0.79 | 0.18 | 5 | 59.5% | 0.51 | 0.64 | 103.3% | 89.4% | 38.7% | 110.9%/74.1% | 6.3 (interpolated) | pass | 0.088 (unverified) | n/a |
| 44 | `cfg_2f25` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=25, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 7/141/15 | 163 | 40.3% | 7.0% | 1.04 | -6.6% | 319 | 1.71 | 2.3% | 25.1 | 11/11 | 1.00 | 0.85 | 0.19 | 4 | 24.3% | 0.40 | 0.60 | 35.2% | 30.3% | 13.4% | 37.0%/27.9% | 5.6 (interpolated) | pass | 0.189 (unverified) | n/a |
| 45 | `cfg_3c40` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=18, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 50/55/34 | 139 | 69.0% | 11.1% | 1.02 | -5.5% | 209 | 1.89 | 2.4% | 17.7 | 10/10 | 0.90 | 0.83 | 0.19 | 5 | 24.1% | 0.54 | 0.86 | 63.4% | 57.9% | -4.6% | 63.6%/47.9% | 8.7 (interpolated) | pass | 0.094 (unverified) | n/a |
| 46 | `cfg_391d` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 4/64/37 | 105 | 28.7% | 5.2% | 1.03 | -6.2% | 338 | 1.77 | 1.7% | 14.7 | 11/11 | 1.00 | 0.84 | 0.19 | 5 | 11.5% | 0.60 | 0.66 | 25.1% | 22.2% | 26.4% | 25.7%/20.1% | 6.0 (interpolated) | pass | 0.182 (unverified) | n/a |
| 47 | `cfg_03d5` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=18, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 46/85/83 | 214 | 123.7% | 17.5% | 0.93 | -19.9% | 209 | 1.70 | 5.0% | 27.7 | 9/9 | 1.00 | 0.82 | 0.11 | 5 | 43.2% | 0.46 | 0.73 | 110.9% | 99.4% | 38.1% | 114.1%/71.8% | 8.5 (interpolated) | pass | 0.147 (unverified) | n/a |
| 48 | `cfg_f849` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=18, entry_z=-3.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 21/109/84 | 214 | 122.7% | 17.4% | 0.92 | -19.8% | 212 | 1.68 | 5.3% | 27.7 | 9/9 | 1.00 | 0.85 | 0.07 | 5 | 45.1% | 0.46 | 0.74 | 110.7% | 100.4% | 33.6% | 104.6%/51.5% | 8.6 (interpolated) | pass | 0.144 (unverified) | n/a |
| 49 | `cfg_994e` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 38/114/152 | 304 | 116.3% | 16.7% | 0.95 | -14.2% | 186 | 1.56 | 6.3% | 44.1 | 9/9 | 1.00 | 0.75 | 0.20 | 5 | 58.7% | 0.50 | 0.66 | 99.9% | 85.1% | 36.2% | 106.8%/85.7% | 6.2 (interpolated) | pass | 0.076 (unverified) | n/a |
| 50 | `cfg_3f35` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 35/171/132 | 338 | 138.9% | 19.1% | 0.99 | -21.2% | 247 | 1.52 | 8.3% | 53.4 | 10/10 | 1.00 | 0.83 | 0.16 | 4 | 80.5% | 0.42 | 0.60 | 120.9% | 105.7% | 42.2% | 126.9%/91.7% | 6.7 (interpolated) | pass | 0.109 (unverified) | n/a |
| 51 | `cfg_2cb4` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=18, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 75/133/133 | 341 | 135.7% | 18.7% | 0.97 | -21.9% | 247 | 1.51 | 8.0% | 53.4 | 10/10 | 1.00 | 0.82 | 0.16 | 4 | 72.1% | 0.47 | 0.60 | 118.3% | 101.8% | 47.9% | 128.2%/101.5% | 6.6 (interpolated) | pass | 0.103 (unverified) | n/a |
| 52 | `cfg_a21a` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 60/177/162 | 399 | 150.5% | 20.2% | 0.98 | -19.7% | 247 | 1.43 | 9.5% | 60.9 | 10/10 | 1.00 | 0.67 | 0.31 | 4 | 39.2% | 0.55 | 0.61 | 127.1% | 108.6% | 31.0% | 134.4%/88.2% | 6.0 (interpolated) | pass | 0.117 (unverified) | n/a |
| 53 | `cfg_9e8d` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 16/192/107 | 315 | 87.5% | 13.4% | 1.00 | -9.0% | 256 | 1.59 | 3.7% | 42.3 | 10/10 | 1.00 | 0.95 | 0.05 | 4 | 30.3% | 0.53 | 0.79 | 72.8% | 60.7% | 56.7% | 78.5%/53.9% | 5.3 (interpolated) | pass | 0.112 (unverified) | n/a |
| 54 | `cfg_9fda` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 24/185/106 | 315 | 87.0% | 13.4% | 0.99 | -9.0% | 256 | 1.59 | 3.7% | 42.2 | 9/9 | 1.00 | 0.90 | 0.10 | 4 | 29.8% | 0.53 | 0.79 | 73.0% | 60.3% | 56.4% | 79.7%/56.9% | 5.3 (interpolated) | pass | 0.111 (unverified) | n/a |
| 55 | `cfg_0bb7` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=22, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 25/132/164 | 321 | 101.5% | 15.1% | 0.88 | -20.0% | 350 | 1.55 | 6.5% | 47.0 | 10/10 | 1.00 | 0.84 | 0.04 | 4 | 20.7% | 0.64 | 0.77 | 87.0% | 73.9% | 20.1% | 101.2%/42.8% | 5.8 (interpolated) | pass | 0.082 (unverified) | n/a |
| 56 | `cfg_8052` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 48/67/119 | 234 | 116.8% | 16.8% | 0.97 | -14.4% | 283 | 1.61 | 4.7% | 36.0 | 8/8 | 0.88 | 0.81 | 0.16 | 5 | 39.0% | 0.51 | 0.77 | 105.4% | 93.7% | 28.2% | 106.7%/74.9% | 8.2 (interpolated) | pass | 0.074 (unverified) | n/a |
| 57 | `cfg_3022` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 77/161/161 | 399 | 157.0% | 20.8% | 1.00 | -18.4% | 247 | 1.44 | 9.3% | 61.1 | 11/11 | 1.00 | 0.72 | 0.28 | 5 | 45.6% | 0.52 | 0.60 | 135.4% | 112.3% | 34.2% | 140.1%/69.9% | 6.2 (interpolated) | pass | 0.129 (unverified) | n/a |
| 58 | `cfg_f689` | timeframe=15min, mean_type=sma, mean_lookback=70, std_lookback=75, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 5/152/102 | 259 | 35.6% | 6.3% | 0.92 | -8.3% | 349 | 1.40 | 4.3% | 40.8 | 9/9 | 1.00 | 0.77 | 0.15 | 3 | 15.2% | 0.52 | 0.58 | 27.2% | 20.7% | 5.4% | 31.9%/23.2% | 3.7 (interpolated) | pass | 0.126 (unverified) | n/a |
| 59 | `cfg_3bce` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=75, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 2/149/92 | 243 | 41.3% | 7.2% | 1.04 | -8.5% | 436 | 1.48 | 4.1% | 36.0 | 8/8 | 1.00 | 0.77 | 0.27 | 5 | 16.1% | 0.57 | 0.56 | 33.9% | 27.5% | 22.4% | 35.0%/26.3% | 4.3 (interpolated) | pass | 0.188 (unverified) | n/a |
| 60 | `cfg_645c` | timeframe=15min, mean_type=sma, mean_lookback=70, std_lookback=75, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 1/156/102 | 259 | 35.5% | 6.3% | 0.92 | -8.3% | 349 | 1.39 | 4.3% | 40.8 | 8/8 | 1.00 | 0.64 | 0.28 | 3 | 15.2% | 0.52 | 0.58 | 27.1% | 20.7% | 5.4% | 32.7%/24.0% | 3.7 (interpolated) | pass | 0.126 (unverified) | n/a |
| 61 | `cfg_c476` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=22, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 51/107/163 | 321 | 104.2% | 15.4% | 0.90 | -18.2% | 349 | 1.55 | 6.3% | 46.7 | 9/9 | 1.00 | 0.84 | 0.05 | 4 | 20.4% | 0.65 | 0.78 | 89.6% | 76.9% | 33.8% | 99.1%/65.7% | 5.9 (interpolated) | pass | 0.088 (unverified) | n/a |
| 62 | `cfg_dc49` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=75, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 7/144/92 | 243 | 41.0% | 7.1% | 1.03 | -8.5% | 436 | 1.48 | 4.1% | 36.1 | 9/9 | 1.00 | 0.80 | 0.23 | 5 | 15.8% | 0.58 | 0.56 | 33.5% | 27.2% | 22.0% | 34.1%/21.2% | 4.2 (interpolated) | pass | 0.185 (unverified) | n/a |
| 63 | `cfg_a07b` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 107/67/99 | 273 | 152.5% | 20.4% | 0.96 | -25.7% | 105 | 1.69 | 6.0% | 41.9 | 10/10 | 1.00 | 0.75 | 0.21 | 5 | 80.1% | 0.47 | 0.54 | 134.2% | 119.4% | 39.9% | 131.5%/70.1% | 8.0 (interpolated) | pass | 0.078 (unverified) | n/a |
| 64 | `cfg_0055` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 101/197/322 | 620 | 122.2% | 17.3% | 0.89 | -13.8% | 220 | 1.26 | 12.3% | 92.2 | 9/9 | 1.00 | 0.82 | 0.07 | 5 | 44.0% | 0.52 | 0.80 | 93.7% | 67.9% | 20.6% | 108.7%/68.1% | 3.9 (interpolated) | pass | 0.076 (unverified) | n/a |
| 65 | `cfg_220c` | timeframe=15min, mean_type=ema, mean_lookback=55, std_lookback=25, entry_z=-3.0, exit_z=0.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 3/124/10 | 137 | 35.1% | 6.2% | 0.99 | -10.4% | 245 | 1.75 | 1.9% | 19.2 | 10/10 | 1.00 | 0.87 | 0.12 | 4 | 19.7% | 0.38 | 0.64 | 30.6% | 26.9% | 13.2% | 31.4%/24.4% | 5.6 (interpolated) | pass | 0.165 (unverified) | n/a |
| 66 | `cfg_a598` | timeframe=15min, mean_type=ema, mean_lookback=55, std_lookback=25, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 5/122/10 | 137 | 34.9% | 6.2% | 0.99 | -10.4% | 245 | 1.74 | 1.9% | 19.2 | 11/11 | 1.00 | 0.88 | 0.11 | 4 | 19.6% | 0.38 | 0.64 | 30.8% | 26.9% | 12.9% | 30.2%/24.3% | 5.6 (interpolated) | pass | 0.163 (unverified) | n/a |
| 67 | `cfg_71ef` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=75, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 5/170/111 | 286 | 46.8% | 8.0% | 1.12 | -5.7% | 368 | 1.46 | 4.8% | 45.1 | 8/8 | 0.88 | 0.79 | 0.33 | 5 | 25.0% | 0.47 | 0.48 | 37.1% | 28.6% | 15.9% | 40.7%/31.4% | 4.0 (interpolated) | pass | 0.249 (unverified) | n/a |
| 68 | `cfg_40bc` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=75, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 2/173/111 | 286 | 46.8% | 8.0% | 1.12 | -5.7% | 368 | 1.46 | 4.8% | 45.1 | 7/7 | 0.86 | 0.74 | 0.37 | 5 | 25.0% | 0.47 | 0.48 | 37.1% | 28.6% | 15.5% | 41.3%/32.5% | 4.0 (interpolated) | pass | 0.249 (unverified) | n/a |
| 69 | `cfg_7f8d` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=0.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 1/101/5 | 107 | 30.9% | 5.5% | 1.14 | -4.4% | 316 | 1.98 | 1.5% | 13.5 | 10/10 | 0.90 | 0.91 | 0.23 | 4 | 12.4% | 0.55 | 0.61 | 27.4% | 24.1% | 6.3% | 27.8%/20.9% | 6.1 (interpolated) | pass | 0.281 (unverified) | n/a |
| 70 | `cfg_760c` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 11/88/10 | 109 | 26.5% | 4.8% | 1.00 | -3.9% | 317 | 1.81 | 1.5% | 13.8 | 10/10 | 0.90 | 0.77 | 0.23 | 4 | 11.8% | 0.50 | 0.67 | 22.9% | 19.9% | 7.7% | 24.0%/18.3% | 5.4 (interpolated) | pass | 0.197 (unverified) | n/a |
| 71 | `cfg_de23` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 51/239/132 | 422 | 123.7% | 17.5% | 0.94 | -16.4% | 260 | 1.41 | 7.4% | 62.8 | 9/9 | 1.00 | 0.84 | 0.10 | 5 | 28.2% | 0.63 | 0.80 | 102.1% | 85.3% | 53.7% | 113.5%/58.1% | 5.4 (interpolated) | pass | 0.077 (unverified) | n/a |
| 72 | `cfg_4515` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 18/86/34 | 138 | 84.6% | 13.1% | 0.93 | -5.3% | 215 | 2.04 | 2.5% | 17.7 | 10/10 | 0.90 | 0.82 | 0.10 | 5 | 28.5% | 0.54 | 0.83 | 78.4% | 73.9% | 11.2% | 80.1%/62.5% | 10.0 (interpolated) | pass | 0.020 (unverified) | n/a |
| 73 | `cfg_1668` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=30, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 32/97/79 | 208 | 34.7% | 6.2% | 0.98 | -8.1% | 407 | 1.48 | 3.3% | 31.2 | 10/10 | 1.00 | 0.79 | 0.19 | 4 | 11.9% | 0.66 | 0.56 | 28.8% | 22.6% | 11.0% | 32.4%/23.8% | 4.2 (interpolated) | pass | 0.160 (unverified) | n/a |
| 74 | `cfg_8f06` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 75/221/323 | 619 | 107.4% | 15.7% | 0.82 | -13.9% | 220 | 1.23 | 12.6% | 91.0 | 8/8 | 1.00 | 0.81 | 0.01 | 5 | 35.9% | 0.57 | 0.88 | 81.6% | 57.5% | 15.9% | 97.9%/72.2% | 3.7 (interpolated) | pass | 0.054 (unverified) | n/a |
| 75 | `cfg_fcbf` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=22, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 13/96/0 | 109 | 52.0% | 8.7% | 0.90 | -6.7% | 214 | 2.27 | 2.3% | 12.9 | 11/11 | 0.73 | 0.70 | 0.21 | 4 | 25.9% | 0.42 | 0.67 | 48.5% | 43.7% | 37.2% | 45.4%/26.9% | 8.7 (interpolated) | pass | 0.049 (unverified) | n/a |
| 76 | `cfg_f3e6` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 30/145/117 | 292 | 111.4% | 16.2% | 0.85 | -14.8% | 227 | 1.42 | 7.1% | 41.3 | 10/10 | 1.00 | 0.81 | 0.04 | 5 | 44.4% | 0.45 | 0.85 | 98.1% | 84.7% | -5.1% | 97.7%/46.0% | 6.5 (interpolated) | pass | 0.102 (unverified) | n/a |
| 77 | `cfg_d1c5` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=18, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 100/21/114 | 235 | 79.7% | 12.5% | 0.93 | -12.0% | 135 | 1.47 | 4.0% | 35.1 | 8/8 | 1.00 | 0.73 | 0.20 | 5 | 37.2% | 0.43 | 0.90 | 70.0% | 60.8% | 3.7% | 73.0%/45.5% | 6.5 (interpolated) | pass | 0.106 (unverified) | n/a |
| 78 | `cfg_fa11` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=30, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 9/119/80 | 208 | 36.4% | 6.4% | 0.99 | -9.4% | 340 | 1.50 | 3.4% | 31.5 | 10/10 | 1.00 | 0.80 | 0.19 | 4 | 10.6% | 0.71 | 0.56 | 30.3% | 24.2% | 13.1% | 34.2%/25.5% | 4.3 (interpolated) | pass | 0.169 (unverified) | n/a |
| 79 | `cfg_2ca6` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=25, entry_z=-3.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 11/129/125 | 265 | 52.6% | 8.8% | 0.85 | -15.5% | 360 | 1.38 | 5.8% | 41.7 | 8/8 | 1.00 | 0.81 | 0.04 | 5 | 13.7% | 0.74 | 0.69 | 44.2% | 36.0% | 31.4% | 48.3%/34.0% | 4.6 (interpolated) | pass | 0.124 (unverified) | n/a |
| 80 | `cfg_b0e1` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=18, entry_z=-3.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 33/123/105 | 261 | 104.9% | 15.5% | 0.85 | -17.7% | 221 | 1.47 | 6.2% | 38.0 | 10/10 | 1.00 | 0.83 | 0.03 | 5 | 29.7% | 0.60 | 0.83 | 92.2% | 81.4% | 52.0% | 97.0%/60.0% | 7.0 (interpolated) | pass | 0.048 (unverified) | n/a |
| 81 | `cfg_8ee9` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=18, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 52/78/87 | 217 | 102.3% | 15.2% | 0.87 | -14.1% | 182 | 1.54 | 4.9% | 31.8 | 9/9 | 1.00 | 0.81 | 0.06 | 5 | 37.7% | 0.51 | 0.86 | 92.7% | 83.2% | 27.6% | 92.2%/39.8% | 8.0 (interpolated) | pass | 0.046 (unverified) | n/a |
| 82 | `cfg_589d` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 31/166/229 | 426 | 87.3% | 13.4% | 0.77 | -17.9% | 204 | 1.31 | 8.8% | 63.6 | 9/9 | 1.00 | 0.83 | -0.06 | 5 | 60.3% | 0.31 | 0.91 | 69.8% | 54.4% | 37.5% | 83.3%/38.0% | 4.2 (interpolated) | pass | 0.032 (unverified) | n/a |
| 83 | `cfg_830e` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 37/186/91 | 314 | 87.1% | 13.4% | 0.86 | -10.9% | 224 | 1.46 | 5.7% | 47.0 | 9/9 | 1.00 | 0.80 | 0.07 | 4 | 36.0% | 0.44 | 0.79 | 73.3% | 61.4% | 51.2% | 78.0%/35.9% | 5.4 (interpolated) | pass | 0.038 (unverified) | n/a |
| 84 | `cfg_9f1f` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 59/58/117 | 234 | 116.0% | 16.7% | 0.93 | -14.5% | 240 | 1.61 | 4.6% | 35.6 | 9/9 | 0.89 | 0.78 | 0.15 | 5 | 40.1% | 0.51 | 0.81 | 104.0% | 92.4% | 25.9% | 108.6%/84.3% | 8.2 (interpolated) | pass | 0.049 (unverified) | n/a |
| 85 | `cfg_dadb` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=18, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 37/138/117 | 292 | 105.1% | 15.5% | 0.84 | -14.9% | 227 | 1.40 | 7.0% | 41.2 | 11/11 | 1.00 | 0.81 | 0.03 | 5 | 41.8% | 0.46 | 0.88 | 91.6% | 78.2% | -4.9% | 94.8%/50.8% | 6.2 (interpolated) | pass | 0.096 (unverified) | n/a |
| 86 | `cfg_e532` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=25, entry_z=-3.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 7/132/126 | 265 | 52.7% | 8.8% | 0.85 | -16.1% | 360 | 1.38 | 5.9% | 41.7 | 7/7 | 1.00 | 0.80 | 0.05 | 5 | 13.0% | 0.75 | 0.69 | 43.2% | 35.1% | 28.6% | 50.4%/32.5% | 4.5 (interpolated) | pass | 0.123 (unverified) | n/a |
| 87 | `cfg_2fd4` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 63/227/132 | 422 | 127.7% | 17.9% | 0.90 | -17.7% | 291 | 1.42 | 7.3% | 62.6 | 10/10 | 1.00 | 0.83 | 0.08 | 4 | 25.7% | 0.65 | 0.82 | 106.2% | 88.3% | 56.4% | 118.2%/72.8% | 5.4 (interpolated) | pass | 0.050 (unverified) | n/a |
| 88 | `cfg_77b8` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=22, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 24/85/0 | 109 | 50.0% | 8.5% | 0.88 | -6.8% | 213 | 2.25 | 2.2% | 13.0 | 10/10 | 0.80 | 0.62 | 0.26 | 4 | 23.1% | 0.45 | 0.69 | 46.4% | 41.8% | 39.2% | 44.1%/26.6% | 8.4 (interpolated) | pass | 0.042 (unverified) | n/a |
| 89 | `cfg_7e01` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=18, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 75/79/63 | 217 | 68.5% | 11.0% | 0.83 | -8.5% | 167 | 1.43 | 3.7% | 31.4 | 10/10 | 0.90 | 0.68 | 0.16 | 5 | 24.2% | 0.55 | 1.03 | 60.1% | 53.0% | 4.8% | 62.9%/37.0% | 6.2 (interpolated) | pass | 0.060 (unverified) | n/a |
| 90 | `cfg_6866` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=30, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 32/245/184 | 461 | 45.3% | 7.8% | 0.85 | -17.4% | 428 | 1.27 | 7.5% | 73.4 | 10/10 | 1.00 | 0.76 | 0.09 | 5 | 17.0% | 0.63 | 0.61 | 31.6% | 18.8% | 14.8% | 39.8%/24.7% | 2.9 (interpolated) | pass | 0.109 (unverified) | n/a |
| 91 | `cfg_265c` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=18, entry_z=-2.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 21/75/42 | 138 | 56.0% | 9.3% | 0.94 | -6.2% | 290 | 2.03 | 1.6% | 17.3 | 8/8 | 0.88 | 0.80 | 0.14 | 3 | 5.9% | 0.82 | 0.95 | 50.6% | 45.3% | -1.2% | 53.4%/39.5% | 7.6 (interpolated) | pass | 0.047 (unverified) | n/a |
| 92 | `cfg_7847` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=30, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 21/256/184 | 461 | 46.7% | 8.0% | 0.86 | -17.3% | 411 | 1.27 | 7.6% | 73.4 | 9/9 | 1.00 | 0.73 | 0.14 | 5 | 17.1% | 0.63 | 0.62 | 33.0% | 19.4% | 14.9% | 39.9%/24.7% | 2.9 (interpolated) | pass | 0.114 (unverified) | n/a |
| 93 | `cfg_2b32` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=18, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 65/133/228 | 426 | 84.6% | 13.1% | 0.75 | -18.0% | 204 | 1.31 | 8.4% | 63.2 | 9/9 | 1.00 | 0.82 | -0.07 | 5 | 55.8% | 0.34 | 0.92 | 67.3% | 50.9% | 38.1% | 79.7%/51.8% | 4.1 (interpolated) | pass | 0.029 (unverified) | n/a |
| 94 | `cfg_7223` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 21/105/75 | 201 | 32.1% | 5.7% | 0.80 | -15.3% | 562 | 1.39 | 3.3% | 29.8 | 10/10 | 1.00 | 0.61 | 0.19 | 3 | 12.7% | 0.61 | 0.77 | 26.1% | 19.8% | 16.1% | 29.1%/20.0% | 4.0 (interpolated) | pass | 0.101 (unverified) | n/a |
| 95 | `cfg_55a2` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 9/87/42 | 138 | 60.2% | 9.9% | 0.87 | -6.2% | 290 | 2.09 | 1.7% | 17.3 | 9/9 | 0.89 | 0.77 | 0.10 | 3 | 5.4% | 0.83 | 0.97 | 54.8% | 49.4% | 10.6% | 57.1%/42.1% | 8.0 (interpolated) | pass | 0.015 (unverified) | n/a |
| 96 | `cfg_6f32` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=18, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 71/99/186 | 356 | 99.6% | 14.8% | 0.84 | -14.4% | 274 | 1.40 | 7.0% | 49.9 | 9/9 | 1.00 | 0.81 | 0.03 | 5 | 40.5% | 0.46 | 0.84 | 80.0% | 67.8% | 39.9% | 92.4%/68.3% | 5.1 (interpolated) | pass | 0.046 (unverified) | n/a |
| 97 | `cfg_22be` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 12/114/75 | 201 | 32.5% | 5.8% | 0.81 | -15.3% | 562 | 1.39 | 3.4% | 29.8 | 11/11 | 1.00 | 0.60 | 0.22 | 3 | 13.2% | 0.59 | 0.76 | 26.9% | 20.7% | 16.5% | 29.3%/21.7% | 4.0 (interpolated) | pass | 0.104 (unverified) | n/a |
| 98 | `cfg_13a1` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=25, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 19/127/94 | 240 | 40.2% | 7.0% | 0.81 | -17.4% | 241 | 1.39 | 3.9% | 36.3 | 10/10 | 1.00 | 0.74 | 0.06 | 5 | 18.9% | 0.53 | 0.85 | 32.8% | 25.8% | 29.4% | 40.6%/26.2% | 4.1 (interpolated) | pass | 0.098 (unverified) | n/a |
| 99 | `cfg_0b7e` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 74/176/267 | 517 | 111.3% | 16.2% | 0.88 | -17.7% | 230 | 1.35 | 10.2% | 76.9 | 9/9 | 1.00 | 0.81 | 0.07 | 5 | 62.4% | 0.44 | 0.68 | 86.0% | 65.5% | 39.6% | 107.4%/76.5% | 4.1 (interpolated) | pass | 0.065 (unverified) | n/a |
| 100 | `cfg_0303` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 129/94/239 | 462 | 124.3% | 17.6% | 0.88 | -17.7% | 239 | 1.36 | 8.5% | 67.7 | 9/9 | 1.00 | 0.83 | 0.04 | 4 | 51.8% | 0.42 | 0.72 | 100.9% | 80.5% | 48.3% | 115.0%/73.5% | 4.8 (interpolated) | pass | 0.065 (unverified) | n/a |
| 101 | `cfg_10a2` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 53/196/266 | 515 | 111.8% | 16.2% | 0.88 | -18.0% | 230 | 1.36 | 10.5% | 77.0 | 8/8 | 1.00 | 0.80 | 0.08 | 5 | 60.9% | 0.46 | 0.69 | 88.3% | 66.4% | 42.1% | 107.4%/48.6% | 4.2 (interpolated) | pass | 0.066 (unverified) | n/a |
| 102 | `cfg_a8cc` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=25, entry_z=-2.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 17/113/14 | 144 | 26.3% | 4.8% | 0.85 | -9.7% | 328 | 1.55 | 2.0% | 19.8 | 10/10 | 0.90 | 0.74 | 0.11 | 4 | 10.6% | 0.53 | 0.65 | 22.0% | 17.9% | 1.4% | 23.3%/17.2% | 4.5 (interpolated) | pass | 0.125 (unverified) | n/a |
| 103 | `cfg_5ad6` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=25, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 7/139/94 | 240 | 37.0% | 6.5% | 0.77 | -17.5% | 241 | 1.36 | 4.0% | 36.4 | 11/11 | 1.00 | 0.74 | 0.03 | 4 | 15.9% | 0.57 | 0.83 | 29.9% | 22.9% | 24.8% | 36.3%/26.5% | 3.9 (interpolated) | pass | 0.081 (unverified) | n/a |
| 104 | `cfg_d186` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=30, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 5/83/52 | 140 | 35.6% | 6.3% | 1.03 | -8.8% | 241 | 1.69 | 2.3% | 21.6 | 10/10 | 0.90 | 0.75 | 0.28 | 4 | 12.6% | 0.65 | 0.67 | 30.9% | 27.1% | 35.0% | 34.8%/24.1% | 5.7 (interpolated) | pass | 0.184 (unverified) | n/a |
| 105 | `cfg_6fd3` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=30, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 5/83/52 | 140 | 35.5% | 6.3% | 1.03 | -8.8% | 241 | 1.69 | 2.3% | 21.6 | 11/11 | 0.91 | 0.76 | 0.27 | 4 | 12.1% | 0.66 | 0.67 | 30.2% | 26.7% | 34.5% | 32.8%/25.6% | 5.7 (interpolated) | pass | 0.182 (unverified) | n/a |
| 106 | `cfg_2c70` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 80/134/246 | 460 | 116.4% | 16.7% | 0.86 | -17.7% | 239 | 1.34 | 9.1% | 67.0 | 10/10 | 1.00 | 0.83 | 0.03 | 4 | 48.6% | 0.43 | 0.74 | 93.2% | 73.9% | 56.2% | 110.5%/67.0% | 4.7 (interpolated) | pass | 0.068 (unverified) | n/a |
| 107 | `cfg_0729` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 14/106/87 | 207 | 35.8% | 6.3% | 0.91 | -9.9% | 334 | 1.45 | 3.3% | 29.5 | 8/8 | 0.88 | 0.71 | 0.20 | 4 | 21.1% | 0.41 | 0.62 | 29.8% | 24.0% | 9.5% | 33.0%/24.8% | 4.3 (interpolated) | pass | 0.147 (unverified) | n/a |
| 108 | `cfg_0058` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=18, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 72/119/217 | 408 | 95.1% | 14.3% | 0.81 | -17.9% | 274 | 1.36 | 7.9% | 59.2 | 9/9 | 1.00 | 0.81 | -0.00 | 5 | 49.9% | 0.48 | 0.78 | 75.9% | 60.3% | 51.7% | 91.2%/56.2% | 4.5 (interpolated) | pass | 0.042 (unverified) | n/a |
| 109 | `cfg_6a97` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 31/156/218 | 405 | 87.8% | 13.5% | 0.77 | -19.2% | 256 | 1.34 | 8.2% | 59.3 | 9/9 | 1.00 | 0.79 | -0.02 | 5 | 50.3% | 0.43 | 0.82 | 71.6% | 56.4% | 37.5% | 83.2%/59.4% | 4.3 (interpolated) | pass | 0.033 (unverified) | n/a |
| 110 | `cfg_9f9a` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=18, entry_z=-3.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 11/206/40 | 257 | 66.2% | 10.7% | 0.82 | -9.0% | 533 | 1.56 | 3.4% | 35.6 | 10/10 | 1.00 | 0.82 | 0.00 | 4 | 12.6% | 0.70 | 1.01 | 56.3% | 46.9% | 54.7% | 57.9%/25.2% | 5.3 (interpolated) | pass | 0.028 (unverified) | n/a |
| 111 | `cfg_356d` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=18, entry_z=-3.5, exit_z=0.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 6/211/40 | 257 | 66.1% | 10.7% | 0.82 | -9.2% | 533 | 1.56 | 3.4% | 35.6 | 9/9 | 1.00 | 0.82 | -0.00 | 4 | 12.5% | 0.70 | 1.01 | 56.2% | 46.5% | 56.4% | 58.9%/29.8% | 5.3 (interpolated) | pass | 0.027 (unverified) | n/a |
| 112 | `cfg_a3e8` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 33/136/187 | 356 | 89.9% | 13.7% | 0.79 | -14.5% | 256 | 1.36 | 7.4% | 49.8 | 9/9 | 1.00 | 0.78 | 0.01 | 5 | 34.4% | 0.49 | 0.88 | 75.7% | 61.7% | 40.1% | 86.3%/60.4% | 5.0 (interpolated) | pass | 0.034 (unverified) | n/a |
| 113 | `cfg_e345` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 63/281/212 | 556 | 102.8% | 15.2% | 0.79 | -22.8% | 287 | 1.25 | 13.5% | 87.6 | 9/9 | 1.00 | 0.71 | 0.08 | 4 | 43.9% | 0.45 | 0.79 | 78.5% | 57.6% | -17.3% | 88.0%/60.1% | 3.9 (interpolated) | pass | 0.047 (unverified) | n/a |
| 114 | `cfg_affb` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=25, entry_z=-2.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 17/107/22 | 146 | 26.1% | 4.8% | 0.85 | -10.4% | 329 | 1.55 | 2.0% | 20.1 | 10/10 | 1.00 | 0.75 | 0.09 | 4 | 12.8% | 0.45 | 0.65 | 22.0% | 18.1% | 3.2% | 24.7%/16.7% | 4.4 (interpolated) | pass | 0.122 (unverified) | n/a |
| 115 | `cfg_1d65` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 63/206/178 | 447 | 105.3% | 15.5% | 0.78 | -20.1% | 349 | 1.31 | 10.5% | 67.7 | 9/9 | 1.00 | 0.76 | 0.03 | 5 | 59.6% | 0.43 | 0.73 | 85.2% | 65.3% | 28.3% | 92.6%/38.8% | 4.5 (interpolated) | pass | 0.050 (unverified) | n/a |
| 116 | `cfg_bde6` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=30, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 22/64/60 | 146 | 22.9% | 4.2% | 0.85 | -7.8% | 486 | 1.48 | 2.2% | 19.6 | 10/10 | 1.00 | 0.60 | 0.25 | 3 | 8.6% | 0.58 | 0.63 | 19.1% | 14.8% | 2.6% | 21.0%/16.6% | 4.0 (interpolated) | pass | 0.115 (unverified) | n/a |
| 117 | `cfg_50e6` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 99/195/305 | 599 | 163.9% | 21.5% | 0.97 | -28.5% | 117 | 1.37 | 12.1% | 94.1 | 8/8 | 1.00 | 0.76 | 0.21 | 5 | 78.5% | 0.52 | 0.50 | 132.3% | 100.6% | 40.5% | 137.6%/94.1% | 4.7 (interpolated) | pass | 0.122 (unverified) | n/a |
| 118 | `cfg_3500` | timeframe=15min, mean_type=sma, mean_lookback=70, std_lookback=25, entry_z=-3.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 8/122/110 | 240 | 75.5% | 11.9% | 0.76 | -22.9% | 121 | 1.50 | 5.5% | 33.5 | 8/8 | 1.00 | 0.73 | 0.04 | 5 | 40.3% | 0.47 | 0.78 | 65.7% | 55.8% | 22.9% | 62.9%/32.6% | 5.8 (interpolated) | pass | 0.034 (unverified) | n/a |
| 119 | `cfg_e930` | timeframe=15min, mean_type=sma, mean_lookback=70, std_lookback=25, entry_z=-3.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 12/118/110 | 240 | 75.8% | 12.0% | 0.77 | -22.9% | 121 | 1.50 | 5.5% | 33.5 | 9/9 | 1.00 | 0.75 | 0.01 | 5 | 40.6% | 0.46 | 0.78 | 65.8% | 57.4% | 25.5% | 72.5%/30.1% | 5.9 (interpolated) | pass | 0.034 (unverified) | n/a |
| 120 | `cfg_d09b` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 84/186/177 | 447 | 106.0% | 15.6% | 0.79 | -20.2% | 349 | 1.32 | 10.3% | 67.8 | 10/10 | 1.00 | 0.75 | 0.04 | 5 | 58.2% | 0.45 | 0.72 | 87.5% | 66.8% | 24.3% | 94.2%/49.2% | 4.6 (interpolated) | pass | 0.051 (unverified) | n/a |
| 121 | `cfg_b37e` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 44/172/137 | 353 | 108.6% | 15.9% | 0.78 | -27.9% | 216 | 1.36 | 8.7% | 50.9 | 9/9 | 1.00 | 0.70 | 0.09 | 4 | 53.5% | 0.37 | 0.81 | 90.1% | 76.9% | -5.2% | 92.9%/47.7% | 5.5 (interpolated) | pass | 0.083 (unverified) | n/a |
| 122 | `cfg_8e0e` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 57/246/142 | 445 | 96.0% | 14.4% | 0.75 | -26.8% | 157 | 1.33 | 7.9% | 67.2 | 11/11 | 1.00 | 0.74 | 0.01 | 4 | 62.6% | 0.35 | 0.78 | 77.2% | 59.9% | 62.8% | 89.5%/35.5% | 4.4 (interpolated) | pass | 0.039 (unverified) | n/a |
| 123 | `cfg_b5a1` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=30, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 8/78/60 | 146 | 23.4% | 4.3% | 0.86 | -7.8% | 486 | 1.49 | 2.3% | 19.6 | 11/11 | 1.00 | 0.69 | 0.18 | 3 | 8.7% | 0.58 | 0.63 | 19.3% | 15.0% | 1.3% | 20.9%/15.3% | 4.1 (interpolated) | pass | 0.118 (unverified) | n/a |
| 124 | `cfg_bbe8` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 37/217/0 | 254 | 97.7% | 14.6% | 0.84 | -28.1% | 191 | 1.55 | 5.3% | 38.8 | 10/10 | 0.80 | 0.72 | 0.12 | 5 | 36.3% | 0.50 | 0.64 | 87.3% | 74.9% | 106.6% | 84.5%/66.1% | 6.9 (interpolated) | pass | 0.109 (unverified) | n/a |
| 125 | `cfg_49fe` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=25, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 15/105/87 | 207 | 33.3% | 5.9% | 0.86 | -10.1% | 334 | 1.43 | 3.2% | 29.5 | 9/9 | 0.89 | 0.74 | 0.12 | 4 | 19.0% | 0.43 | 0.65 | 27.4% | 20.8% | 6.7% | 30.2%/21.0% | 4.1 (interpolated) | pass | 0.129 (unverified) | n/a |
| 126 | `cfg_2689` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=75, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 6/132/85 | 223 | 27.9% | 5.1% | 0.80 | -7.9% | 632 | 1.38 | 3.7% | 32.6 | 9/9 | 1.00 | 0.75 | 0.05 | 4 | 6.2% | 0.75 | 0.69 | 21.2% | 15.8% | 5.6% | 25.4%/13.0% | 3.5 (interpolated) | pass | 0.074 (unverified) | n/a |
| 127 | `cfg_6b3b` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 42/260/143 | 445 | 97.0% | 14.5% | 0.76 | -27.7% | 157 | 1.34 | 8.0% | 67.4 | 10/10 | 1.00 | 0.75 | 0.01 | 4 | 57.4% | 0.34 | 0.76 | 77.3% | 61.4% | 65.1% | 91.6%/42.1% | 4.4 (interpolated) | pass | 0.041 (unverified) | n/a |
| 128 | `cfg_e515` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 28/213/0 | 241 | 99.4% | 14.8% | 0.84 | -25.9% | 249 | 1.63 | 5.1% | 36.5 | 11/11 | 0.91 | 0.71 | 0.13 | 4 | 46.0% | 0.38 | 0.57 | 91.3% | 79.2% | 154.0% | 86.6%/52.1% | 7.3 (interpolated) | pass | 0.107 (unverified) | n/a |
| 129 | `cfg_0914` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 66/248/337 | 651 | 96.1% | 14.4% | 0.75 | -21.5% | 230 | 1.22 | 13.4% | 98.6 | 8/8 | 1.00 | 0.73 | 0.02 | 5 | 47.2% | 0.41 | 0.88 | 68.8% | 46.2% | -5.8% | 87.7%/52.7% | 3.4 (interpolated) | pass | 0.042 (unverified) | n/a |
| 130 | `cfg_d4f2` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=75, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 7/120/80 | 207 | 28.0% | 5.1% | 0.82 | -7.2% | 632 | 1.41 | 3.4% | 30.8 | 9/9 | 1.00 | 0.69 | 0.13 | 4 | 7.8% | 0.68 | 0.69 | 21.3% | 16.3% | 3.5% | 25.3%/16.7% | 3.6 (interpolated) | pass | 0.081 (unverified) | n/a |
| 131 | `cfg_175d` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=25, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 38/116/28 | 182 | 31.8% | 5.7% | 0.83 | -16.5% | 285 | 1.41 | 3.4% | 25.8 | 11/11 | 0.82 | 0.39 | 0.43 | 4 | 20.4% | 0.34 | 0.59 | 27.6% | 21.6% | 20.2% | 29.6%/19.9% | 4.3 (interpolated) | pass | 0.124 (unverified) | n/a |
| 132 | `cfg_e218` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=25, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 38/104/47 | 189 | 33.4% | 5.9% | 0.85 | -14.5% | 318 | 1.42 | 3.4% | 27.3 | 11/11 | 0.91 | 0.44 | 0.41 | 4 | 21.7% | 0.33 | 0.67 | 27.8% | 21.2% | 19.5% | 31.5%/20.9% | 4.2 (interpolated) | pass | 0.106 (unverified) | n/a |
| 133 | `cfg_327e` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 17/77/17 | 111 | 24.1% | 4.4% | 0.82 | -6.6% | 233 | 1.57 | 2.1% | 13.8 | 11/11 | 0.82 | 0.39 | 0.42 | 5 | 13.1% | 0.42 | 0.78 | 21.0% | 17.7% | 16.0% | 22.0%/14.1% | 4.9 (interpolated) | pass | 0.111 (unverified) | n/a |
| 134 | `cfg_e1d3` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 39/231/249 | 519 | 64.3% | 10.5% | 0.86 | -23.6% | 532 | 1.26 | 11.4% | 83.4 | 8/8 | 1.00 | 0.71 | 0.15 | 4 | 28.5% | 0.56 | 0.56 | 46.6% | 29.8% | 0.1% | 51.1%/28.3% | 3.2 (interpolated) | pass | 0.109 (unverified) | n/a |
| 135 | `cfg_c93a` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 41/136/120 | 297 | 113.5% | 16.4% | 0.82 | -20.1% | 216 | 1.44 | 7.2% | 39.3 | 10/10 | 1.00 | 0.73 | 0.09 | 4 | 51.2% | 0.38 | 0.79 | 98.8% | 85.7% | 21.2% | 104.9%/54.8% | 6.3 (interpolated) | pass | 0.111 (unverified) | n/a |
| 136 | `cfg_c487` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=30, entry_z=-3.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 8/96/93 | 197 | 44.3% | 7.6% | 0.88 | -13.4% | 227 | 1.46 | 4.4% | 31.1 | 8/8 | 0.88 | 0.76 | 0.13 | 4 | 18.6% | 0.58 | 0.68 | 39.1% | 33.3% | 34.4% | 41.2%/28.4% | 5.3 (interpolated) | pass | 0.119 (unverified) | n/a |
| 137 | `cfg_533d` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 7/87/17 | 111 | 24.6% | 4.5% | 0.83 | -7.4% | 233 | 1.59 | 2.2% | 13.9 | 12/12 | 0.83 | 0.49 | 0.34 | 5 | 14.8% | 0.36 | 0.76 | 21.3% | 18.2% | 13.7% | 21.9%/12.0% | 5.0 (interpolated) | pass | 0.116 (unverified) | n/a |
| 138 | `cfg_653d` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 75/219/312 | 606 | 122.2% | 17.3% | 0.84 | -25.0% | 129 | 1.28 | 12.6% | 95.4 | 7/7 | 1.00 | 0.80 | 0.04 | 5 | 78.1% | 0.36 | 0.62 | 95.0% | 69.1% | 87.9% | 105.9%/62.0% | 4.0 (interpolated) | pass | 0.065 (unverified) | n/a |
| 139 | `cfg_011a` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=30, entry_z=-3.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 4/99/94 | 197 | 43.3% | 7.5% | 0.86 | -13.4% | 227 | 1.45 | 4.4% | 31.1 | 7/7 | 0.86 | 0.66 | 0.20 | 4 | 16.3% | 0.62 | 0.71 | 36.5% | 30.4% | 30.1% | 40.2%/29.2% | 5.1 (interpolated) | pass | 0.109 (unverified) | n/a |
| 140 | `cfg_55f7` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=30, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 11/134/137 | 282 | 68.5% | 11.0% | 0.83 | -17.3% | 372 | 1.49 | 6.3% | 43.9 | 9/9 | 0.89 | 0.78 | 0.05 | 4 | 25.0% | 0.64 | 0.66 | 58.1% | 48.5% | 29.5% | 59.0%/36.7% | 5.2 (interpolated) | pass | 0.059 (unverified) | n/a |
| 141 | `cfg_4fa7` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 189/35/213 | 437 | 70.2% | 11.2% | 0.76 | -22.4% | 260 | 1.28 | 6.9% | 64.7 | 6/6 | 1.00 | 0.61 | 0.15 | 4 | 33.8% | 0.52 | 0.83 | 53.2% | 39.0% | 11.4% | 66.1%/41.5% | 3.6 (interpolated) | pass | 0.060 (unverified) | n/a |
| 142 | `cfg_fde5` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=30, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 7/137/138 | 282 | 65.5% | 10.6% | 0.80 | -17.9% | 372 | 1.48 | 6.3% | 43.6 | 8/8 | 0.88 | 0.72 | 0.09 | 4 | 22.5% | 0.66 | 0.67 | 56.2% | 45.4% | 28.0% | 56.8%/42.4% | 5.1 (interpolated) | pass | 0.051 (unverified) | n/a |
| 143 | `cfg_6646` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 50/220/249 | 519 | 57.9% | 9.6% | 0.80 | -24.6% | 532 | 1.24 | 11.3% | 83.4 | 9/9 | 1.00 | 0.70 | 0.10 | 4 | 26.4% | 0.54 | 0.60 | 41.3% | 24.4% | -0.9% | 44.8%/28.6% | 3.0 (interpolated) | pass | 0.086 (unverified) | n/a |
| 144 | `cfg_b578` | timeframe=15min, mean_type=ema, mean_lookback=55, std_lookback=30, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 25/95/80 | 200 | 37.1% | 6.5% | 0.91 | -7.6% | 459 | 1.49 | 3.1% | 29.5 | 10/10 | 0.90 | 0.35 | 0.57 | 4 | 14.9% | 0.60 | 0.66 | 30.3% | 24.8% | 31.3% | 31.7%/19.0% | 4.4 (interpolated) | pass | 0.140 (unverified) | n/a |
| 145 | `cfg_6ec6` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 25/114/125 | 264 | 43.1% | 7.4% | 0.78 | -18.0% | 446 | 1.36 | 5.8% | 39.2 | 10/10 | 0.90 | 0.63 | 0.16 | 4 | 11.3% | 0.74 | 0.70 | 34.5% | 26.8% | 10.0% | 41.7%/27.8% | 4.0 (interpolated) | pass | 0.083 (unverified) | n/a |
| 146 | `cfg_8885` | timeframe=15min, mean_type=ema, mean_lookback=55, std_lookback=30, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 24/111/49 | 184 | 31.2% | 5.6% | 0.76 | -9.2% | 422 | 1.44 | 3.3% | 26.6 | 11/11 | 0.91 | 0.56 | 0.20 | 4 | 10.8% | 0.65 | 0.79 | 26.6% | 20.9% | 23.3% | 30.9%/23.3% | 4.2 (interpolated) | pass | 0.081 (unverified) | n/a |
| 147 | `cfg_0ec3` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=30, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 19/120/125 | 264 | 45.1% | 7.7% | 0.81 | -17.8% | 446 | 1.37 | 5.9% | 39.3 | 9/9 | 0.89 | 0.63 | 0.18 | 4 | 10.3% | 0.77 | 0.67 | 35.9% | 28.5% | 10.5% | 40.6%/28.9% | 4.1 (interpolated) | pass | 0.088 (unverified) | n/a |
| 148 | `cfg_b618` | timeframe=15min, mean_type=ema, mean_lookback=80, std_lookback=75, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 2/145/54 | 201 | 26.6% | 4.8% | 0.76 | -8.6% | 475 | 1.34 | 3.8% | 27.2 | 9/9 | 0.89 | 0.46 | 0.30 | 4 | 11.0% | 0.57 | 0.68 | 20.9% | 16.0% | 9.7% | 20.8%/7.3% | 3.6 (interpolated) | pass | 0.064 (unverified) | n/a |
| 149 | `cfg_e59a` | timeframe=15min, mean_type=ema, mean_lookback=80, std_lookback=75, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 1/146/54 | 201 | 26.6% | 4.8% | 0.76 | -8.6% | 475 | 1.34 | 3.8% | 27.2 | 8/8 | 0.88 | 0.45 | 0.31 | 4 | 11.0% | 0.57 | 0.68 | 20.9% | 16.0% | 9.7% | 20.1%/6.5% | 3.6 (interpolated) | pass | 0.064 (unverified) | n/a |
| 150 | `cfg_523a` | timeframe=15min, mean_type=ema, mean_lookback=55, std_lookback=30, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 5/113/82 | 200 | 31.6% | 5.7% | 0.81 | -9.3% | 478 | 1.42 | 3.2% | 29.7 | 10/10 | 0.90 | 0.36 | 0.45 | 4 | 8.6% | 0.73 | 0.71 | 26.2% | 20.4% | 28.6% | 28.7%/20.0% | 4.0 (interpolated) | pass | 0.086 (unverified) | n/a |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | -1.8% / -0.34 / 53 | 7.4% / 1.03 / 48 | 176.3% / 2.74 / 63 | 19.7% / 2.30 / 45 | 0.6% / 0.11 / 57 |
| 2 | -1.8% / -0.34 / 53 | 8.9% / 1.16 / 48 | 170.5% / 2.70 / 63 | 20.9% / 2.39 / 45 | -0.0% / 0.05 / 57 |
| 3 | 3.0% / 0.52 / 63 | -0.6% / -0.05 / 48 | 126.8% / 2.26 / 69 | 16.1% / 1.99 / 32 | 18.4% / 1.32 / 58 |
| 4 | 4.7% / 0.74 / 63 | -0.7% / -0.06 / 48 | 119.3% / 2.19 / 69 | 16.4% / 2.05 / 32 | 17.9% / 1.29 / 58 |
| 5 | 3.2% / 0.42 / 69 | 6.3% / 0.91 / 61 | 95.1% / 2.00 / 72 | 19.8% / 2.25 / 47 | 6.6% / 0.51 / 76 |
| 6 | 0.5% / 0.10 / 69 | 7.6% / 1.09 / 61 | 93.4% / 1.98 / 72 | 18.5% / 2.12 / 47 | 8.7% / 0.65 / 76 |
| 7 | 2.4% / 0.47 / 66 | 8.2% / 1.15 / 56 | 103.6% / 2.07 / 84 | 15.2% / 1.94 / 46 | 14.7% / 1.16 / 65 |
| 8 | -0.6% / -0.04 / 104 | 3.1% / 0.39 / 84 | 138.6% / 2.04 / 109 | 18.0% / 1.79 / 71 | 26.7% / 1.66 / 91 |
| 9 | 2.0% / 0.40 / 66 | 6.6% / 0.96 / 56 | 103.5% / 2.07 / 84 | 13.5% / 1.76 / 46 | 16.8% / 1.32 / 65 |
| 10 | -0.9% / -0.07 / 104 | 3.3% / 0.42 / 84 | 149.1% / 2.12 / 109 | 14.3% / 1.50 / 71 | 27.2% / 1.67 / 91 |
| 11 | 4.3% / 0.54 / 106 | 3.0% / 0.38 / 80 | 52.7% / 1.30 / 103 | 28.0% / 2.79 / 73 | 21.5% / 1.45 / 85 |
| 12 | 4.0% / 0.51 / 106 | 2.5% / 0.33 / 80 | 58.2% / 1.39 / 103 | 25.2% / 2.62 / 73 | 22.2% / 1.47 / 85 |
| 13 | 1.8% / 0.27 / 97 | 2.7% / 0.35 / 77 | 99.6% / 2.06 / 84 | 13.9% / 1.29 / 70 | 16.6% / 1.09 / 82 |
| 14 | 9.2% / 1.43 / 71 | 4.2% / 0.60 / 62 | 50.8% / 1.32 / 89 | 16.8% / 2.00 / 48 | 21.9% / 1.52 / 64 |
| 15 | 9.2% / 1.07 / 91 | 8.4% / 0.66 / 80 | 99.9% / 1.64 / 110 | 16.5% / 1.65 / 69 | 32.1% / 1.92 / 87 |
| 16 | 0.2% / 0.06 / 97 | 1.7% / 0.25 / 77 | 102.7% / 2.12 / 84 | 13.0% / 1.22 / 70 | 15.3% / 1.02 / 82 |
| 17 | 9.2% / 1.47 / 71 | 3.7% / 0.56 / 62 | 50.0% / 1.31 / 89 | 14.7% / 1.81 / 48 | 21.9% / 1.59 / 64 |
| 18 | 6.0% / 0.92 / 60 | 6.8% / 0.94 / 50 | 55.8% / 1.36 / 71 | 17.2% / 1.99 / 43 | 30.3% / 1.80 / 56 |
| 19 | 5.5% / 0.86 / 60 | 5.3% / 0.79 / 50 | 53.3% / 1.31 / 71 | 17.1% / 1.98 / 43 | 28.7% / 1.78 / 56 |
| 20 | 10.4% / 1.19 / 91 | 4.9% / 0.44 / 80 | 94.3% / 1.58 / 110 | 13.7% / 1.41 / 69 | 33.3% / 2.01 / 87 |
| 21 | 9.8% / 1.53 / 68 | 7.8% / 1.08 / 56 | 38.8% / 0.96 / 81 | 16.6% / 2.25 / 37 | 39.5% / 2.48 / 63 |
| 22 | 4.7% / 0.57 / 87 | 1.7% / 0.25 / 66 | 123.0% / 2.25 / 92 | 8.5% / 0.80 / 69 | 6.9% / 0.50 / 78 |
| 23 | 4.3% / 0.68 / 80 | 6.9% / 0.98 / 70 | 51.5% / 1.32 / 98 | 18.5% / 2.16 / 54 | 13.7% / 1.06 / 79 |
| 24 | 3.1% / 0.39 / 88 | 1.6% / 0.24 / 66 | 127.0% / 2.13 / 92 | 10.2% / 0.95 / 69 | 6.5% / 0.48 / 79 |
| 25 | 7.1% / 1.04 / 77 | 3.7% / 0.55 / 60 | 52.5% / 1.37 / 85 | 10.7% / 1.46 / 48 | 25.2% / 1.60 / 75 |
| 26 | -1.1% / -0.15 / 63 | 5.2% / 0.75 / 54 | 69.1% / 1.58 / 75 | 16.7% / 1.97 / 46 | 15.1% / 1.10 / 68 |
| 27 | 2.0% / 0.33 / 66 | 8.4% / 1.10 / 56 | 78.9% / 1.69 / 73 | 16.9% / 1.87 / 49 | 23.8% / 1.47 / 69 |
| 28 | 0.9% / 0.15 / 81 | 5.6% / 0.76 / 54 | 67.5% / 1.54 / 77 | 17.1% / 1.91 / 47 | 20.6% / 1.34 / 65 |
| 29 | 0.9% / 0.15 / 81 | 5.9% / 0.79 / 54 | 68.3% / 1.55 / 77 | 15.6% / 1.79 / 47 | 20.4% / 1.33 / 65 |
| 30 | 1.2% / 0.22 / 66 | 7.3% / 1.00 / 56 | 75.5% / 1.64 / 73 | 16.5% / 1.84 / 49 | 24.4% / 1.49 / 69 |
| 31 | 0.6% / 0.11 / 96 | 2.2% / 0.30 / 74 | 122.5% / 1.97 / 90 | 10.7% / 1.14 / 75 | 13.9% / 1.00 / 94 |
| 32 | -0.1% / 0.02 / 63 | 5.3% / 0.77 / 54 | 68.9% / 1.58 / 73 | 19.2% / 2.17 / 46 | 12.0% / 0.90 / 68 |
| 33 | 4.4% / 0.61 / 120 | 5.5% / 0.71 / 92 | 47.4% / 1.12 / 127 | 27.4% / 2.90 / 78 | 24.7% / 1.73 / 98 |
| 34 | 4.3% / 0.81 / 75 | 5.3% / 0.77 / 61 | 46.0% / 1.21 / 95 | 15.0% / 1.83 / 51 | 22.7% / 1.71 / 70 |
| 35 | -3.6% / -0.70 / 55 | 3.5% / 0.52 / 51 | 53.8% / 1.60 / 64 | 20.6% / 2.72 / 41 | 10.4% / 1.23 / 51 |
| 36 | -2.1% / -0.38 / 59 | 8.1% / 1.08 / 52 | 73.3% / 1.62 / 79 | 11.3% / 1.16 / 53 | 15.2% / 1.16 / 61 |
| 37 | 4.9% / 1.02 / 55 | -0.9% / -0.15 / 47 | 72.0% / 1.70 / 72 | 4.7% / 1.08 / 29 | 16.2% / 1.38 / 54 |
| 38 | -1.6% / -0.28 / 59 | 8.1% / 1.07 / 52 | 76.3% / 1.66 / 79 | 10.1% / 1.04 / 53 | 14.3% / 1.10 / 61 |
| 39 | -3.7% / -0.72 / 55 | 3.4% / 0.50 / 51 | 54.0% / 1.61 / 64 | 20.2% / 2.64 / 41 | 10.7% / 1.26 / 51 |
| 40 | 4.9% / 1.03 / 55 | -2.9% / -0.61 / 47 | 70.3% / 1.67 / 72 | 2.7% / 0.68 / 29 | 16.2% / 1.40 / 54 |
| 41 | 2.1% / 0.39 / 42 | -0.3% / -0.06 / 26 | 10.5% / 1.19 / 40 | 10.6% / 2.88 / 16 | 12.8% / 1.35 / 39 |
| 42 | 4.0% / 1.20 / 23 | 0.2% / 0.07 / 15 | 3.2% / 0.57 / 28 | 3.6% / 1.62 / 12 | 15.4% / 1.79 / 27 |
| 43 | 8.9% / 1.30 / 68 | 5.5% / 0.78 / 56 | 22.6% / 0.74 / 80 | 13.3% / 1.84 / 37 | 38.4% / 2.33 / 63 |
| 44 | 2.1% / 0.39 / 42 | -0.4% / -0.07 / 26 | 10.5% / 1.19 / 40 | 10.6% / 2.88 / 16 | 12.8% / 1.35 / 39 |
| 45 | 2.3% / 0.63 / 29 | 0.2% / 0.06 / 24 | 36.2% / 1.53 / 39 | 12.0% / 1.83 / 21 | 8.0% / 1.18 / 26 |
| 46 | 4.2% / 1.24 / 23 | 0.2% / 0.09 / 15 | 3.0% / 0.54 / 28 | 3.6% / 1.62 / 12 | 15.4% / 1.79 / 27 |
| 47 | 0.3% / 0.08 / 49 | 1.8% / 0.31 / 42 | 56.2% / 1.32 / 61 | 12.4% / 2.00 / 19 | 24.8% / 1.70 / 43 |
| 48 | 2.8% / 0.45 / 49 | 2.8% / 0.46 / 42 | 53.5% / 1.27 / 61 | 12.6% / 2.00 / 19 | 21.9% / 1.56 / 43 |
| 49 | 8.8% / 1.29 / 68 | 5.0% / 0.73 / 56 | 22.4% / 0.73 / 80 | 13.5% / 1.87 / 37 | 36.3% / 2.25 / 63 |
| 50 | -0.3% / 0.01 / 70 | 3.5% / 0.50 / 61 | 51.6% / 1.28 / 80 | 15.3% / 1.59 / 58 | 32.4% / 1.84 / 69 |
| 51 | -0.8% / -0.05 / 70 | 3.0% / 0.44 / 61 | 49.6% / 1.24 / 82 | 12.6% / 1.37 / 58 | 37.0% / 2.04 / 70 |
| 52 | 3.9% / 0.48 / 88 | -0.5% / -0.02 / 65 | 79.9% / 1.68 / 94 | 4.1% / 0.42 / 68 | 29.5% / 1.47 / 84 |
| 53 | -0.4% / -0.07 / 67 | 5.7% / 0.92 / 53 | 43.9% / 1.47 / 84 | 13.0% / 1.72 / 54 | 9.5% / 1.19 / 57 |
| 54 | -0.3% / -0.04 / 67 | 5.7% / 0.92 / 53 | 44.1% / 1.47 / 84 | 12.9% / 1.70 / 54 | 9.1% / 1.15 / 57 |
| 55 | 2.0% / 0.39 / 68 | -5.4% / -1.05 / 59 | 67.0% / 1.58 / 84 | 8.7% / 1.50 / 45 | 15.0% / 1.26 / 65 |
| 56 | 6.5% / 1.24 / 46 | 0.4% / 0.11 / 36 | 56.0% / 1.42 / 61 | 14.5% / 1.75 / 32 | 13.4% / 1.02 / 59 |
| 57 | 5.6% / 0.65 / 88 | 0.8% / 0.13 / 65 | 76.5% / 1.63 / 94 | 4.5% / 0.46 / 68 | 30.9% / 1.52 / 84 |
| 58 | -0.4% / -0.04 / 61 | -0.3% / -0.04 / 59 | 4.8% / 0.62 / 53 | 17.7% / 2.23 / 39 | 10.7% / 1.33 / 47 |
| 59 | 6.2% / 1.07 / 60 | 0.8% / 0.19 / 55 | 1.8% / 0.27 / 53 | 21.7% / 2.58 / 39 | 6.5% / 0.84 / 36 |
| 60 | -0.4% / -0.04 / 61 | -0.3% / -0.04 / 59 | 4.8% / 0.62 / 53 | 17.7% / 2.23 / 39 | 10.7% / 1.33 / 47 |
| 61 | 2.4% / 0.48 / 68 | -4.6% / -0.87 / 59 | 69.6% / 1.62 / 84 | 6.8% / 1.24 / 45 | 15.3% / 1.30 / 65 |
| 62 | 6.3% / 1.07 / 60 | 0.8% / 0.19 / 55 | 1.5% / 0.23 / 53 | 21.8% / 2.58 / 39 | 6.5% / 0.84 / 36 |
| 63 | 7.7% / 1.09 / 60 | 5.8% / 0.78 / 53 | 29.0% / 0.77 / 66 | 22.5% / 2.77 / 35 | 40.2% / 2.32 / 59 |
| 64 | 13.5% / 1.41 / 140 | 3.0% / 0.40 / 106 | 54.2% / 1.30 / 142 | 12.8% / 1.09 / 104 | 9.2% / 0.62 / 128 |
| 65 | 8.5% / 1.97 / 35 | -4.5% / -1.02 / 26 | 12.8% / 1.42 / 36 | 7.7% / 2.34 / 11 | 7.3% / 0.87 / 29 |
| 66 | 8.5% / 1.97 / 35 | -4.5% / -1.03 / 26 | 12.8% / 1.42 / 36 | 7.7% / 2.34 / 11 | 7.1% / 0.86 / 29 |
| 67 | 0.5% / 0.12 / 74 | 3.7% / 0.72 / 61 | 5.1% / 0.63 / 59 | 14.0% / 1.96 / 42 | 17.5% / 1.98 / 50 |
| 68 | 0.5% / 0.12 / 74 | 3.7% / 0.72 / 61 | 5.1% / 0.63 / 59 | 14.0% / 1.96 / 42 | 17.5% / 1.98 / 50 |
| 69 | 4.8% / 1.40 / 28 | -2.3% / -0.88 / 18 | 16.4% / 2.04 / 29 | 7.4% / 2.25 / 9 | 2.2% / 0.42 / 23 |
| 70 | 3.1% / 1.10 / 28 | -1.8% / -0.72 / 19 | 13.2% / 1.59 / 30 | 7.4% / 2.26 / 9 | 2.8% / 0.54 / 23 |
| 71 | 3.7% / 0.51 / 92 | 0.3% / 0.08 / 76 | 74.5% / 1.68 / 102 | 21.9% / 1.97 / 67 | 1.2% / 0.15 / 85 |
| 72 | 3.6% / 0.91 / 29 | 0.6% / 0.16 / 23 | 43.7% / 1.36 / 39 | 12.2% / 1.81 / 21 | 9.7% / 1.35 / 26 |
| 73 | 4.0% / 0.93 / 46 | -2.2% / -0.57 / 37 | 8.7% / 1.05 / 51 | 1.1% / 0.30 / 30 | 20.4% / 2.11 / 44 |
| 74 | 12.7% / 1.36 / 140 | 2.5% / 0.34 / 106 | 52.6% / 1.28 / 142 | 13.4% / 1.13 / 104 | 3.8% / 0.31 / 127 |
| 75 | 6.7% / 1.56 / 26 | -0.5% / -0.11 / 19 | 20.7% / 1.05 / 31 | 5.4% / 1.80 / 11 | 12.7% / 1.82 / 22 |
| 76 | 5.2% / 0.72 / 67 | 3.9% / 0.53 / 56 | 46.3% / 1.16 / 72 | 9.6% / 1.29 / 34 | 20.6% / 1.24 / 63 |
| 77 | 6.0% / 1.26 / 46 | 4.0% / 0.67 / 36 | 30.9% / 1.19 / 62 | 11.6% / 1.53 / 32 | 11.5% / 0.90 / 59 |
| 78 | 4.4% / 0.96 / 46 | -2.1% / -0.56 / 37 | 6.9% / 0.85 / 51 | 1.3% / 0.34 / 30 | 23.3% / 2.28 / 44 |
| 79 | 3.9% / 0.71 / 57 | 0.8% / 0.19 / 44 | 1.8% / 0.19 / 67 | 6.7% / 1.53 / 33 | 34.1% / 2.53 / 64 |
| 80 | 6.2% / 0.99 / 54 | 1.5% / 0.25 / 45 | 58.0% / 1.39 / 67 | 9.3% / 1.25 / 38 | 10.1% / 0.74 / 57 |
| 81 | 3.9% / 0.72 / 42 | 7.7% / 1.08 / 40 | 46.9% / 1.23 / 52 | 12.8% / 1.71 / 33 | 9.2% / 0.72 / 50 |
| 82 | 3.6% / 0.51 / 94 | 4.6% / 0.63 / 74 | 24.4% / 0.77 / 100 | 18.8% / 2.02 / 68 | 16.8% / 1.13 / 90 |
| 83 | -0.4% / -0.04 / 68 | 3.0% / 0.42 / 57 | 37.6% / 1.19 / 76 | 17.3% / 1.95 / 47 | 13.0% / 1.01 / 66 |
| 84 | 9.0% / 1.62 / 46 | 0.2% / 0.07 / 36 | 54.2% / 1.33 / 61 | 13.2% / 1.65 / 32 | 13.3% / 1.02 / 59 |
| 85 | 5.1% / 0.71 / 67 | 3.8% / 0.53 / 56 | 44.6% / 1.15 / 72 | 9.1% / 1.24 / 34 | 19.2% / 1.19 / 63 |
| 86 | 3.7% / 0.70 / 57 | 0.6% / 0.15 / 44 | 1.5% / 0.18 / 67 | 6.6% / 1.54 / 33 | 35.2% / 2.56 / 64 |
| 87 | 4.4% / 0.60 / 92 | -1.4% / -0.20 / 76 | 81.2% / 1.64 / 102 | 20.2% / 1.84 / 67 | 1.6% / 0.18 / 85 |
| 88 | 4.7% / 1.29 / 26 | -0.7% / -0.16 / 19 | 21.9% / 1.09 / 31 | 6.1% / 1.92 / 11 | 11.7% / 1.73 / 22 |
| 89 | 1.9% / 0.43 / 39 | 2.7% / 0.46 / 35 | 35.7% / 1.34 / 58 | 11.4% / 1.38 / 31 | 6.5% / 0.53 / 54 |
| 90 | 5.1% / 0.72 / 95 | 1.0% / 0.19 / 93 | 1.0% / 0.15 / 103 | 9.1% / 1.35 / 71 | 24.2% / 1.84 / 99 |
| 91 | -1.1% / -0.37 / 29 | -2.5% / -0.91 / 25 | 47.4% / 1.98 / 38 | 7.5% / 1.41 / 21 | 2.1% / 0.47 / 25 |
| 92 | 4.1% / 0.59 / 95 | 1.1% / 0.21 / 93 | 1.7% / 0.20 / 103 | 9.4% / 1.39 / 71 | 25.3% / 1.87 / 99 |
| 93 | 3.3% / 0.47 / 94 | 3.6% / 0.51 / 74 | 24.7% / 0.78 / 100 | 16.8% / 1.85 / 68 | 18.5% / 1.25 / 90 |
| 94 | 8.0% / 2.02 / 42 | -0.6% / -0.13 / 33 | -2.4% / -0.15 / 55 | 7.5% / 1.97 / 24 | 17.3% / 1.76 / 47 |
| 95 | -1.1% / -0.38 / 29 | -2.5% / -0.91 / 25 | 52.0% / 1.84 / 38 | 6.8% / 1.27 / 21 | 2.5% / 0.52 / 25 |
| 96 | 4.4% / 0.80 / 75 | 4.1% / 0.60 / 57 | 42.0% / 1.13 / 93 | 6.4% / 0.73 / 57 | 21.6% / 1.48 / 74 |
| 97 | 8.6% / 2.07 / 42 | -0.9% / -0.20 / 33 | -2.4% / -0.15 / 55 | 7.7% / 2.00 / 24 | 17.0% / 1.74 / 47 |
| 98 | 4.9% / 1.00 / 53 | 0.1% / 0.04 / 43 | 7.7% / 0.56 / 60 | 5.1% / 1.77 / 25 | 18.0% / 1.68 / 59 |
| 99 | 9.2% / 1.08 / 119 | 1.2% / 0.19 / 96 | 24.4% / 0.76 / 129 | 18.0% / 1.96 / 75 | 30.1% / 1.86 / 98 |
| 100 | 12.3% / 1.46 / 105 | -2.6% / -0.27 / 74 | 47.8% / 1.15 / 113 | 12.3% / 1.20 / 75 | 23.5% / 1.39 / 95 |
| 101 | 8.1% / 0.98 / 119 | 2.8% / 0.36 / 96 | 20.3% / 0.67 / 127 | 20.4% / 2.15 / 75 | 31.7% / 1.92 / 98 |
| 102 | 3.3% / 0.97 / 33 | -4.7% / -1.27 / 23 | 14.2% / 1.53 / 40 | 6.1% / 1.49 / 19 | 5.8% / 0.93 / 29 |
| 103 | 5.3% / 1.07 / 53 | -0.3% / -0.04 / 43 | 4.6% / 0.38 / 60 | 5.5% / 1.81 / 25 | 18.2% / 1.70 / 59 |
| 104 | 2.2% / 0.58 / 30 | 3.5% / 1.00 / 22 | -0.7% / -0.07 / 36 | 7.2% / 1.55 / 18 | 20.5% / 1.98 / 34 |
| 105 | 2.2% / 0.58 / 30 | 3.5% / 1.00 / 22 | -1.1% / -0.14 / 36 | 7.2% / 1.54 / 18 | 20.9% / 2.01 / 34 |
| 106 | 13.9% / 1.58 / 104 | -3.5% / -0.41 / 74 | 45.7% / 1.14 / 113 | 8.1% / 0.81 / 74 | 25.1% / 1.43 / 95 |
| 107 | 5.5% / 1.17 / 48 | -1.8% / -0.38 / 42 | 13.6% / 1.26 / 52 | 2.8% / 0.69 / 26 | 12.1% / 1.35 / 39 |
| 108 | 5.7% / 0.86 / 86 | 0.1% / 0.05 / 71 | 24.7% / 0.77 / 105 | 13.6% / 1.55 / 66 | 30.2% / 1.92 / 80 |
| 109 | 5.9% / 0.88 / 86 | 0.1% / 0.06 / 71 | 20.4% / 0.67 / 103 | 17.7% / 1.89 / 66 | 25.0% / 1.66 / 79 |
| 110 | -3.2% / -0.60 / 57 | 0.3% / 0.08 / 48 | 47.6% / 1.56 / 63 | 10.6% / 1.57 / 41 | 4.9% / 0.66 / 48 |
| 111 | -3.4% / -0.63 / 57 | 0.2% / 0.07 / 48 | 47.7% / 1.56 / 63 | 10.6% / 1.57 / 41 | 4.9% / 0.66 / 48 |
| 112 | 5.7% / 0.97 / 75 | 1.2% / 0.21 / 57 | 41.3% / 1.12 / 93 | 7.1% / 0.81 / 57 | 17.2% / 1.23 / 74 |
| 113 | 13.8% / 1.27 / 122 | -1.4% / -0.09 / 99 | 40.9% / 1.09 / 124 | 11.6% / 0.99 / 92 | 14.8% / 0.84 / 119 |
| 114 | 3.1% / 0.92 / 33 | -3.6% / -1.05 / 24 | 11.9% / 1.25 / 41 | 6.5% / 1.61 / 19 | 6.5% / 1.09 / 29 |
| 115 | 2.5% / 0.29 / 106 | 5.3% / 0.63 / 81 | 24.5% / 0.73 / 107 | 18.7% / 1.83 / 67 | 28.6% / 1.42 / 86 |
| 116 | 5.5% / 1.47 / 32 | -5.0% / -1.56 / 29 | 13.2% / 1.80 / 39 | -0.5% / -0.15 / 21 | 8.9% / 1.37 / 25 |
| 117 | 10.9% / 1.07 / 135 | 22.9% / 1.67 / 96 | 12.5% / 0.47 / 147 | 16.4% / 1.46 / 96 | 47.9% / 2.37 / 125 |
| 118 | 5.7% / 1.07 / 48 | 6.1% / 1.07 / 41 | 17.0% / 0.62 / 72 | 6.9% / 1.68 / 26 | 25.1% / 2.13 / 53 |
| 119 | 5.7% / 1.07 / 48 | 6.3% / 1.10 / 41 | 16.9% / 0.61 / 72 | 7.1% / 1.69 / 26 | 25.0% / 2.13 / 53 |
| 120 | 3.4% / 0.36 / 106 | 5.6% / 0.65 / 81 | 24.3% / 0.73 / 107 | 16.7% / 1.66 / 67 | 30.2% / 1.47 / 86 |
| 121 | -0.3% / 0.00 / 83 | 13.8% / 1.06 / 68 | 35.9% / 0.93 / 85 | 12.3% / 1.45 / 48 | 20.5% / 1.12 / 69 |
| 122 | -1.9% / -0.17 / 100 | 8.0% / 0.95 / 81 | 24.9% / 0.74 / 109 | 22.9% / 2.33 / 69 | 20.5% / 1.24 / 86 |
| 123 | 5.2% / 1.38 / 32 | -4.4% / -1.29 / 29 | 13.6% / 1.83 / 39 | -1.1% / -0.36 / 21 | 9.3% / 1.42 / 25 |
| 124 | 1.8% / 0.26 / 54 | 6.7% / 0.80 / 46 | 45.1% / 1.21 / 62 | 24.1% / 2.65 / 41 | 1.1% / 0.15 / 51 |
| 125 | 4.2% / 0.96 / 48 | -1.7% / -0.37 / 42 | 13.3% / 1.24 / 52 | 2.6% / 0.65 / 26 | 12.0% / 1.35 / 39 |
| 126 | 0.6% / 0.16 / 52 | 2.2% / 0.51 / 51 | -0.8% / -0.07 / 51 | 20.5% / 2.48 / 39 | 4.1% / 0.60 / 30 |
| 127 | -1.9% / -0.17 / 100 | 6.9% / 0.83 / 81 | 25.0% / 0.74 / 109 | 25.1% / 2.48 / 69 | 20.0% / 1.22 / 86 |
| 128 | -1.6% / -0.25 / 48 | 5.2% / 0.64 / 44 | 36.6% / 1.01 / 61 | 24.5% / 2.85 / 40 | 13.3% / 1.19 / 48 |
| 129 | 17.4% / 1.62 / 143 | 1.5% / 0.22 / 110 | 33.2% / 0.91 / 153 | 12.7% / 1.11 / 104 | 9.7% / 0.64 / 141 |
| 130 | 1.4% / 0.35 / 51 | 0.5% / 0.13 / 48 | -0.1% / 0.02 / 43 | 18.7% / 2.39 / 39 | 5.9% / 0.87 / 26 |
| 131 | 9.0% / 1.94 / 41 | -0.8% / -0.13 / 33 | 5.6% / 0.55 / 48 | 9.5% / 2.06 / 25 | 5.4% / 0.72 / 35 |
| 132 | 7.2% / 1.54 / 42 | -1.5% / -0.27 / 35 | 8.5% / 0.84 / 49 | 9.6% / 2.13 / 25 | 6.2% / 0.71 / 38 |
| 133 | 3.1% / 0.98 / 28 | 0.5% / 0.16 / 19 | 9.7% / 1.11 / 32 | 5.7% / 1.95 / 9 | 3.2% / 0.51 / 23 |
| 134 | 3.6% / 0.46 / 111 | -2.0% / -0.20 / 103 | 11.6% / 0.68 / 117 | 13.4% / 1.40 / 85 | 27.8% / 1.91 / 103 |
| 135 | -7.4% / -0.88 / 73 | 14.5% / 1.14 / 52 | 41.1% / 1.04 / 79 | 18.1% / 2.06 / 37 | 20.8% / 1.18 / 56 |
| 136 | -2.5% / -0.35 / 52 | 11.0% / 2.05 / 29 | 1.4% / 0.17 / 49 | 8.1% / 1.47 / 24 | 21.6% / 1.87 / 43 |
| 137 | 3.2% / 0.96 / 28 | 0.7% / 0.23 / 19 | 8.6% / 1.01 / 32 | 6.0% / 1.96 / 9 | 4.2% / 0.62 / 23 |
| 138 | 6.2% / 0.64 / 139 | 15.1% / 1.55 / 95 | 19.5% / 0.62 / 142 | 21.9% / 1.78 / 96 | 24.8% / 1.28 / 134 |
| 139 | -3.9% / -0.56 / 52 | 10.5% / 2.02 / 29 | 1.5% / 0.18 / 49 | 8.0% / 1.47 / 24 | 23.2% / 1.95 / 43 |
| 140 | -1.9% / -0.30 / 67 | 3.3% / 0.65 / 44 | 19.4% / 0.81 / 69 | 3.3% / 0.43 / 45 | 34.9% / 2.62 / 57 |
| 141 | 8.2% / 1.20 / 96 | -2.5% / -0.28 / 75 | 6.8% / 0.36 / 115 | 18.8% / 2.20 / 64 | 27.2% / 1.86 / 87 |
| 142 | -3.3% / -0.56 / 67 | 2.6% / 0.54 / 44 | 19.8% / 0.82 / 69 | 3.0% / 0.41 / 45 | 35.1% / 2.65 / 57 |
| 143 | 3.0% / 0.39 / 111 | -3.0% / -0.32 / 103 | 13.3% / 0.75 / 117 | 11.6% / 1.25 / 85 | 24.9% / 1.79 / 103 |
| 144 | -1.5% / -0.28 / 49 | 2.9% / 0.65 / 38 | 6.6% / 0.69 / 51 | 6.3% / 1.28 / 20 | 19.3% / 1.93 / 42 |
| 145 | 4.7% / 0.76 / 57 | -2.4% / -0.39 / 49 | 7.7% / 0.56 / 70 | 1.1% / 0.19 / 37 | 28.6% / 2.46 / 51 |
| 146 | -1.7% / -0.29 / 47 | 0.4% / 0.10 / 38 | 10.5% / 1.08 / 44 | 1.5% / 0.44 / 19 | 18.4% / 1.62 / 36 |
| 147 | 4.9% / 0.79 / 57 | -2.1% / -0.32 / 49 | 6.0% / 0.46 / 70 | 1.2% / 0.20 / 37 | 31.5% / 2.54 / 51 |
| 148 | 0.9% / 0.17 / 60 | -3.7% / -0.83 / 40 | 11.8% / 1.51 / 46 | 14.0% / 1.75 / 33 | 2.3% / 0.39 / 22 |
| 149 | 0.9% / 0.17 / 60 | -3.7% / -0.83 / 40 | 11.8% / 1.51 / 46 | 14.0% / 1.75 / 33 | 2.3% / 0.39 / 22 |
| 150 | -1.5% / -0.28 / 49 | 1.8% / 0.40 / 38 | 2.5% / 0.31 / 51 | 5.7% / 1.19 / 20 | 21.2% / 2.03 / 42 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_2703` | 12 | 0.87 | 0.48/0.74 | 0.56/0.65 |
| 1 | `cfg_fc56` | 6 | 0.92 | 0.96/0.96 | 0.88/0.89 |
| 2 | `cfg_11db` | 634 | 0.83 | 0.09/0.69 | 0.09/0.32 |
| 3 | `cfg_0055` | 4 | 0.82 | 0.90/0.91 | 0.79/0.80 |
| 4 | `cfg_0058` | 3 | 0.97 | 0.99/0.99 | 0.99/0.99 |
| 5 | `cfg_321b` | 209 | 0.85 | 0.30/0.66 | 0.04/0.31 |
| 6 | `cfg_957d` | 72 | 0.84 | 0.68/0.78 | 0.31/0.71 |
| 7 | `cfg_0681` | 115 | 0.82 | 0.43/0.65 | 0.05/0.13 |
| 8 | `cfg_b3df` | 82 | 0.84 | 0.55/0.77 | 0.32/0.52 |
| 9 | `cfg_c487` | 3 | 0.99 | 1.00/1.00 | 0.95/0.97 |
| 10 | `cfg_6ddc` | 5 | 0.84 | 0.97/0.98 | 0.89/0.94 |
| 11 | `cfg_9e8d` | 21 | 0.85 | 0.50/0.87 | 0.24/0.55 |
| 12 | `cfg_de23` | 14 | 0.83 | 0.80/0.92 | 0.42/0.77 |
| 13 | `cfg_0212` | 26 | 0.83 | 0.79/0.86 | 0.61/0.70 |
| 14 | `cfg_895e` | 35 | 0.83 | 0.58/0.72 | 0.14/0.38 |
| 15 | `cfg_267a` | 15 | 0.82 | 0.84/0.89 | 0.57/0.68 |
| 16 | `cfg_21e3` | 9 | 0.85 | 0.76/0.90 | 0.59/0.65 |
| 17 | `cfg_daa1` | 13 | 0.85 | 0.72/0.85 | 0.52/0.61 |
| 18 | `cfg_7184` | 18 | 0.86 | 0.92/0.93 | 0.60/0.68 |
| 19 | `cfg_8217` | 108 | 0.83 | 0.50/0.87 | 0.29/0.58 |
| 20 | `cfg_0303` | 3 | 0.97 | 0.99/0.99 | 0.94/0.94 |
| 21 | `cfg_50e6` | 3 | 0.92 | 0.92/0.92 | 0.79/0.80 |
| 22 | `cfg_03d5` | 9 | 0.94 | 0.87/0.92 | 0.76/0.90 |
| 23 | `cfg_7f8d` | 9 | 0.94 | 0.96/0.97 | 0.98/0.98 |
| 24 | `cfg_8052` | 5 | 0.93 | 0.91/0.95 | 0.82/0.86 |
| 25 | `cfg_fe55` | 9 | 0.91 | 0.92/0.96 | 0.93/0.96 |
| 26 | `cfg_0729` | 4 | 0.95 | 0.96/0.97 | 0.74/0.95 |
| 27 | `cfg_e345` | 2 | 0.86 | 0.91/0.91 | 0.80/0.80 |
| 28 | `cfg_3bce` | 16 | 0.85 | 0.86/0.89 | 0.65/0.76 |
| 29 | `cfg_265c` | 16 | 0.84 | 0.71/0.85 | 0.20/0.39 |
| 30 | `cfg_0b7e` | 8 | 0.81 | 0.85/0.92 | 0.69/0.77 |
| 31 | `cfg_589d` | 5 | 0.87 | 0.82/0.82 | 0.78/0.78 |
| 32 | `cfg_0bb7` | 28 | 0.82 | 0.16/0.67 | 0.17/0.29 |
| 33 | `cfg_cb6e` | 6 | 0.85 | 0.85/0.85 | 0.47/0.47 |
| 34 | `cfg_6d61` | 21 | 0.83 | 0.67/0.93 | 0.59/0.76 |
| 35 | `cfg_f3e6` | 8 | 0.86 | 0.67/0.94 | 0.65/0.85 |
| 36 | `cfg_a8cc` | 17 | 0.84 | 0.81/0.89 | 0.47/0.65 |
| 37 | `cfg_2689` | 5 | 0.90 | 0.93/0.93 | 0.86/0.87 |
| 38 | `cfg_6ec6` | 2 | 0.99 | 1.00/1.00 | 1.00/1.00 |
| 39 | `cfg_0f67` | 22 | 0.91 | 0.74/0.87 | 0.61/0.78 |
| 40 | `cfg_6599` | 14 | 0.82 | 0.70/0.78 | 0.39/0.57 |
| 41 | `cfg_71ef` | 6 | 0.89 | 0.92/0.93 | 0.71/0.74 |
| 42 | `cfg_13a1` | 5 | 0.84 | 0.85/0.93 | 0.54/0.77 |
| 43 | `cfg_8ddf` | 25 | 0.84 | 0.14/0.90 | 0.25/0.42 |
| 44 | `cfg_d1c5` | 5 | 0.82 | 0.89/0.90 | 0.73/0.76 |
| 45 | `cfg_1668` | 9 | 0.84 | 0.78/0.94 | 0.59/0.83 |
| 46 | `cfg_7223` | 4 | 0.85 | 0.84/0.99 | 0.69/0.99 |
| 47 | `cfg_175d` | 6 | 0.85 | 0.88/0.91 | 0.82/0.92 |
| 48 | `cfg_2ca6` | 3 | 0.99 | 1.00/1.00 | 0.95/0.97 |
| 49 | `cfg_1d65` | 2 | 0.99 | 1.00/1.00 | 0.99/0.99 |
| 50 | `cfg_8e0e` | 7 | 0.86 | 0.60/0.66 | 0.54/0.60 |
| 51 | `cfg_220c` | 9 | 0.94 | 0.95/0.98 | 0.95/0.99 |
| 52 | `cfg_fcbf` | 6 | 0.90 | 0.93/0.94 | 0.82/0.82 |
| 53 | `cfg_b0e1` | 6 | 0.92 | 0.95/0.95 | 0.77/0.78 |
| 54 | `cfg_2b82` | 4 | 0.86 | 0.94/0.94 | 0.83/0.83 |
| 55 | `cfg_327e` | 8 | 0.84 | 0.92/0.96 | 0.78/0.82 |
| 56 | `cfg_3f35` | 6 | 0.88 | 0.95/0.95 | 0.81/0.81 |
| 57 | `cfg_a21a` | 3 | 0.97 | 0.99/0.99 | 0.94/0.97 |
| 58 | `cfg_a07b` | 7 | 0.86 | 0.74/0.79 | 0.62/0.68 |
| 59 | `cfg_3500` | 4 | 0.86 | 0.89/1.00 | 0.63/0.94 |
| 60 | `cfg_9f9a` | 6 | 0.95 | 0.98/0.98 | 0.97/0.97 |
| 61 | `cfg_3c40` | 8 | 0.86 | 0.89/0.97 | 0.66/0.89 |
| 62 | `cfg_bde6` | 3 | 0.99 | 0.99/0.99 | 0.98/0.98 |
| 63 | `cfg_bbe8` | 6 | 0.93 | 0.95/0.95 | 0.83/0.84 |
| 64 | `cfg_4fa7` | 1 | n/a | n/a/n/a | n/a/n/a |
| 65 | `cfg_b578` | 3 | 0.97 | 0.97/0.97 | 0.96/0.96 |
| 66 | `cfg_55f7` | 4 | 0.80 | 0.36/1.00 | 0.56/0.95 |
| 67 | `cfg_b37e` | 10 | 0.85 | 0.42/0.90 | 0.47/0.77 |
| 68 | `cfg_f689` | 5 | 0.93 | 0.94/0.96 | 0.91/0.93 |
| 69 | `cfg_e1d3` | 2 | 1.00 | 1.00/1.00 | 0.99/0.99 |
| 70 | `cfg_6866` | 5 | 0.81 | 0.89/0.94 | 0.67/0.82 |
| 71 | `cfg_6f32` | 3 | 0.98 | 0.99/0.99 | 0.99/0.99 |
| 72 | `cfg_d186` | 3 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 73 | `cfg_8885` | 1 | n/a | n/a/n/a | n/a/n/a |
| 74 | `cfg_fa04` | 6 | 0.89 | 0.94/0.94 | 0.77/0.78 |
| 75 | `cfg_b618` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 8.166e-04 over 15984 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 555.0, participation ratio 10.8, 95%-variance components 103 (rank bound T = 1258); raw grid 16128; raw + known prior 850056
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
