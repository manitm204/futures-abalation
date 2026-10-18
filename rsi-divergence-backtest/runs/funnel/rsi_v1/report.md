# Screening funnel -- rsi_v1 (development stages only)

- Code: `737d995cb21f` (dirty working tree: True, diff sha256 `965ab665384a`)
- Config: `/home/manit/Desktop/fun_projects/abalation_backtest/rsi-divergence-backtest/configs/funnel/rsi_funnel.yaml` sha256 `b52a22567b28b759`; seed 20261016
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'SPY': '2026-08-18', 'QQQ': '2026-08-18'}
- Frozen manifest sha256: `8cb7d9806dd2d46f` (33 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No RSI-divergence config has been evaluated on 2023-2024, but the same slice gated the mean-reversion funnels (mr_v1, mr_v2), the channel-breakout funnels and the Donchian ablation, so it is not untouched SPY data.
- Holdout 2025+ previously inspected: **True** -- SPY 2025-2026 holdout metrics were computed and inspected for the Donchian ablation and the channel-breakout funnels (funnel_v1..v3 records.parquet). The holdout is NOT an untouched test of SPY.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 98304 | 98304 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 98304 | 98304 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 98304 | 31156 | 67148 | 0 |  | 50473 | 31.69 | 31.69 |  |
| 3 performance & risk | hard_gate | 31156 | 194 | 30962 | 0 |  | 0 | 0.20 | 0.62 |  |
| 4 parameter stability | hard_gate | 194 | 191 | 3 | 0 |  | 194 | 0.19 | 98.45 |  |
| 5 time stability | hard_gate | 191 | 188 | 3 | 0 |  | 182 | 0.19 | 98.43 |  |
| 6 deduplication | dedup | 188 | 33 |  |  | 155 |  | 0.03 | 17.55 |  |
| 7 execution stress | hard_gate | 33 | 33 | 0 | 0 |  | 1 | 0.03 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 33 |  |  |  |  |  |  |  | diagnostic only: unverified: 33 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 67148 |
| s2:hard_reject:years_with_>=10_trades | 47401 |
| s3:hard_reject:max_drawdown | 25 |
| s3:hard_reject:net_return | 23337 |
| s3:hard_reject:sharpe | 30962 |
| s4:hard_reject:neighbor_frac_profitable | 2 |
| s4:hard_reject:neighbor_median_sharpe | 1 |
| s5:hard_reject:profitable_years | 3 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | stop/target/time exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | QQQ dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_7c9f` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=2.0, max_hold=48 | 103/84/11 | 198 | 23.0% | 4.2% | 1.25 | -3.8% | 229 | 1.73 | 2.8% | 79.2 | 14/14 | 0.93 | 0.92 | 0.33 | 4 | 7.9% | 0.61 | 0.47 | 20.8% | 18.6% | 17.0% | 20.5%/16.7% | 6.6 (interpolated) | pass | 0.278 (unverified) | -0.06 |
| 2 | `cfg_a790` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=2.0, target_r=1.5, max_hold=6 | 31/17/153 | 201 | 16.6% | 3.1% | 1.14 | -2.1% | 247 | 1.92 | 1.3% | 80.4 | 13/13 | 0.85 | 0.86 | 0.28 | 4 | 2.3% | 0.84 | 0.59 | 14.0% | 11.5% | 9.2% | 15.0%/11.3% | 4.5 (interpolated) | pass | 0.185 (unverified) | -0.08 |
| 3 | `cfg_1d99` | timeframe=5min, rsi_lookback=14, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=3.0, stop_atr=1.5, target_r=2.0, max_hold=48 | 104/85/10 | 199 | 22.6% | 4.2% | 1.16 | -3.5% | 227 | 1.63 | 2.9% | 80.1 | 14/14 | 0.93 | 0.82 | 0.33 | 5 | 8.0% | 0.61 | 0.52 | 20.3% | 18.1% | 14.9% | 20.1%/15.6% | 6.5 (interpolated) | pass | 0.219 (unverified) | -0.31 |
| 4 | `cfg_e535` | timeframe=15min, rsi_lookback=14, pivot_left=8, pivot_right=1, max_pivot_gap=48, min_rsi_diff=0.0, stop_atr=2.0, target_r=1.5, max_hold=12 | 51/47/67 | 165 | 27.3% | 5.0% | 0.95 | -5.9% | 354 | 1.53 | 4.4% | 66.3 | 15/15 | 0.93 | 0.77 | 0.18 | 4 | 16.8% | 0.36 | 0.59 | 25.2% | 23.1% | 15.3% | 24.9%/19.8% | 8.3 (interpolated) | pass | 0.103 (unverified) | 0.77 |
| 5 | `cfg_69b2` | timeframe=15min, rsi_lookback=7, pivot_left=8, pivot_right=1, max_pivot_gap=48, min_rsi_diff=3.0, stop_atr=2.0, target_r=1.5, max_hold=24 | 67/75/24 | 166 | 35.0% | 6.2% | 0.96 | -8.1% | 167 | 1.48 | 6.0% | 67.1 | 15/15 | 0.93 | 0.76 | 0.20 | 4 | 16.3% | 0.53 | 0.50 | 32.9% | 30.9% | 14.0% | 32.5%/25.7% | 10.7 (interpolated) | pass | 0.115 (unverified) | 1.01 |
| 6 | `cfg_1d3a` | timeframe=15min, rsi_lookback=10, pivot_left=8, pivot_right=1, max_pivot_gap=48, min_rsi_diff=0.0, stop_atr=2.0, target_r=1.5, max_hold=24 | 83/88/25 | 196 | 36.3% | 6.4% | 0.97 | -6.3% | 155 | 1.44 | 7.1% | 79.6 | 15/15 | 0.80 | 0.76 | 0.21 | 5 | 13.5% | 0.61 | 0.47 | 33.9% | 31.4% | 15.8% | 32.1%/25.6% | 9.5 (interpolated) | pass | 0.120 (unverified) | 0.46 |
| 7 | `cfg_0376` | timeframe=5min, rsi_lookback=14, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=3.0, stop_atr=1.5, target_r=2.0, max_hold=48 | 167/112/23 | 302 | 24.6% | 4.5% | 1.03 | -3.8% | 528 | 1.44 | 4.5% | 122.0 | 13/13 | 0.85 | 0.73 | 0.30 | 4 | 11.1% | 0.55 | 0.54 | 21.0% | 17.6% | 15.1% | 22.3%/17.7% | 4.8 (interpolated) | pass | 0.117 (unverified) | -0.80 |
| 8 | `cfg_7413` | timeframe=5min, rsi_lookback=14, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=2.0, max_hold=48 | 91/64/18 | 173 | 18.7% | 3.5% | 1.04 | -2.3% | 528 | 1.64 | 2.8% | 69.5 | 13/13 | 1.00 | 0.72 | 0.31 | 4 | 7.3% | 0.61 | 0.55 | 16.7% | 14.8% | 10.8% | 17.4%/14.3% | 6.2 (interpolated) | pass | 0.103 (unverified) | -1.12 |
| 9 | `cfg_0588` | timeframe=15min, rsi_lookback=7, pivot_left=12, pivot_right=1, max_pivot_gap=78, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=24 | 80/14/78 | 172 | 41.3% | 7.2% | 0.92 | -9.0% | 248 | 1.53 | 8.6% | 69.1 | 11/11 | 0.82 | 0.71 | 0.21 | 3 | 17.2% | 0.56 | 0.64 | 38.7% | 36.0% | 22.7% | 36.3%/27.4% | 10.1 (interpolated) | pass | 0.073 (unverified) | 0.91 |
| 10 | `cfg_8ec2` | timeframe=15min, rsi_lookback=7, pivot_left=8, pivot_right=1, max_pivot_gap=48, min_rsi_diff=3.0, stop_atr=2.0, target_r=1.5, max_hold=12 | 49/53/69 | 171 | 30.3% | 5.4% | 0.98 | -5.8% | 179 | 1.55 | 4.6% | 69.1 | 15/15 | 0.93 | 0.70 | 0.28 | 4 | 17.0% | 0.44 | 0.57 | 28.1% | 25.9% | 10.7% | 26.7%/21.6% | 8.8 (interpolated) | pass | 0.106 (unverified) | 0.88 |
| 11 | `cfg_a079` | timeframe=5min, rsi_lookback=10, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=2.0, max_hold=48 | 164/103/22 | 289 | 19.9% | 3.7% | 0.91 | -4.9% | 528 | 1.39 | 4.4% | 116.5 | 13/13 | 0.85 | 0.70 | 0.21 | 4 | 9.2% | 0.54 | 0.62 | 16.6% | 13.4% | 11.4% | 17.6%/13.4% | 4.3 (interpolated) | pass | 0.065 (unverified) | -0.87 |
| 12 | `cfg_8525` | timeframe=15min, rsi_lookback=14, pivot_left=3, pivot_right=3, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=48 | 122/40/34 | 196 | 48.5% | 8.2% | 0.90 | -9.6% | 404 | 1.43 | 14.0% | 78.8 | 11/11 | 0.82 | 0.69 | 0.21 | 4 | 18.2% | 0.59 | 0.67 | 45.5% | 42.6% | 54.5% | 43.3%/32.8% | 10.7 (interpolated) | pass | 0.070 (unverified) | 0.46 |
| 13 | `cfg_b356` | timeframe=15min, rsi_lookback=14, pivot_left=3, pivot_right=3, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=3.0, max_hold=24 | 118/46/47 | 211 | 39.6% | 6.9% | 0.96 | -5.9% | 286 | 1.49 | 8.6% | 84.9 | 13/13 | 0.77 | 0.66 | 0.29 | 5 | 18.8% | 0.48 | 0.57 | 36.6% | 33.6% | 17.6% | 34.9%/24.7% | 8.6 (interpolated) | pass | 0.089 (unverified) | 0.37 |
| 14 | `cfg_0c30` | timeframe=5min, rsi_lookback=7, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=2.0, max_hold=24 | 165/109/47 | 321 | 17.1% | 3.2% | 0.83 | -5.5% | 528 | 1.33 | 3.7% | 129.0 | 14/14 | 0.93 | 0.66 | 0.17 | 4 | 6.1% | 0.59 | 0.66 | 13.4% | 9.9% | 9.0% | 15.6%/10.6% | 3.5 (interpolated) | pass | 0.066 (unverified) | 0.20 |
| 15 | `cfg_9030` | timeframe=15min, rsi_lookback=7, pivot_left=8, pivot_right=1, max_pivot_gap=48, min_rsi_diff=0.0, stop_atr=2.0, target_r=1.5, max_hold=24 | 89/91/30 | 210 | 35.5% | 6.3% | 0.93 | -6.8% | 388 | 1.38 | 7.6% | 84.8 | 14/14 | 0.93 | 0.64 | 0.30 | 3 | 12.8% | 0.66 | 0.51 | 32.9% | 30.3% | 9.9% | 32.3%/22.8% | 8.8 (interpolated) | pass | 0.103 (unverified) | 0.53 |
| 16 | `cfg_5aae` | timeframe=15min, rsi_lookback=10, pivot_left=5, pivot_right=3, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=3.0, max_hold=48 | 93/44/13 | 150 | 40.1% | 7.0% | 1.02 | -8.9% | 393 | 1.58 | 7.5% | 60.0 | 13/13 | 0.92 | 0.63 | 0.39 | 4 | 14.1% | 0.62 | 0.61 | 38.0% | 35.9% | 29.5% | 35.9%/26.3% | 12.2 (interpolated) | pass | 0.106 (unverified) | 0.04 |
| 17 | `cfg_7b4b` | timeframe=15min, rsi_lookback=7, pivot_left=12, pivot_right=1, max_pivot_gap=48, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=12 | 60/6/110 | 176 | 26.4% | 4.8% | 0.79 | -9.4% | 419 | 1.46 | 5.5% | 70.6 | 12/12 | 0.83 | 0.62 | 0.17 | 4 | 14.5% | 0.43 | 0.82 | 23.9% | 21.4% | 19.4% | 24.0%/17.7% | 6.9 (interpolated) | pass | 0.036 (unverified) | 0.79 |
| 18 | `cfg_07ea` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=1.0, max_hold=48 | 83/112/3 | 198 | 8.5% | 1.6% | 0.77 | -2.6% | 513 | 1.36 | 1.5% | 79.2 | 13/13 | 0.85 | 0.61 | 0.16 | 3 | 0.7% | 0.90 | 0.65 | 6.6% | 4.8% | 11.2% | 7.4%/6.0% | 3.4 (interpolated) | pass | 0.071 (unverified) | -0.23 |
| 19 | `cfg_12a3` | timeframe=15min, rsi_lookback=14, pivot_left=8, pivot_right=1, max_pivot_gap=48, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=24 | 75/17/66 | 158 | 40.3% | 7.0% | 0.84 | -15.2% | 345 | 1.54 | 7.9% | 63.6 | 14/14 | 0.93 | 0.60 | 0.24 | 4 | 18.2% | 0.55 | 0.63 | 38.0% | 35.6% | 47.1% | 36.6%/24.6% | 10.8 (interpolated) | pass | 0.081 (unverified) | 0.70 |
| 20 | `cfg_b79e` | timeframe=15min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=2.0, max_hold=24 | 98/63/17 | 178 | 26.3% | 4.8% | 0.83 | -7.2% | 415 | 1.40 | 5.7% | 71.6 | 15/15 | 0.93 | 0.60 | 0.23 | 3 | -0.3% | 1.00 | 0.66 | 24.2% | 22.0% | 33.9% | 23.2%/17.9% | 7.7 (interpolated) | pass | 0.062 (unverified) | 0.36 |
| 21 | `cfg_b4ba` | timeframe=15min, rsi_lookback=10, pivot_left=8, pivot_right=1, max_pivot_gap=48, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=24 | 93/22/81 | 196 | 40.5% | 7.0% | 0.81 | -15.2% | 150 | 1.41 | 9.8% | 79.9 | 14/14 | 0.93 | 0.60 | 0.21 | 5 | 23.6% | 0.35 | 0.65 | 37.4% | 34.5% | 40.9% | 37.8%/26.4% | 8.9 (interpolated) | pass | 0.073 (unverified) | 0.40 |
| 22 | `cfg_25bb` | timeframe=15min, rsi_lookback=10, pivot_left=3, pivot_right=3, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=3.0, max_hold=48 | 161/71/18 | 250 | 42.9% | 7.4% | 0.91 | -14.1% | 238 | 1.35 | 12.8% | 102.4 | 12/12 | 0.83 | 0.59 | 0.32 | 4 | 11.3% | 0.72 | 0.58 | 39.3% | 35.8% | 28.9% | 37.4%/29.0% | 8.1 (interpolated) | pass | 0.079 (unverified) | 0.32 |
| 23 | `cfg_7095` | timeframe=5min, rsi_lookback=21, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=3.0, max_hold=48 | 235/101/50 | 386 | 27.1% | 4.9% | 0.88 | -6.2% | 250 | 1.33 | 7.3% | 155.3 | 11/11 | 0.91 | 0.57 | 0.30 | 4 | 8.8% | 0.62 | 0.66 | 22.3% | 17.5% | 9.2% | 23.8%/17.5% | 4.1 (interpolated) | pass | 0.083 (unverified) | 0.29 |
| 24 | `cfg_7554` | timeframe=5min, rsi_lookback=21, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=2.0, max_hold=24 | 200/122/70 | 392 | 18.7% | 3.5% | 0.83 | -4.6% | 272 | 1.29 | 4.7% | 157.6 | 13/13 | 0.92 | 0.56 | 0.27 | 3 | 4.2% | 0.72 | 0.61 | 14.1% | 9.8% | 11.0% | 16.2%/11.9% | 3.2 (interpolated) | pass | 0.067 (unverified) | 0.21 |
| 25 | `cfg_4cd6` | timeframe=15min, rsi_lookback=7, pivot_left=5, pivot_right=3, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=48 | 105/35/33 | 173 | 36.4% | 6.4% | 0.76 | -12.8% | 455 | 1.38 | 12.0% | 69.4 | 11/11 | 0.91 | 0.56 | 0.20 | 4 | 7.3% | 0.75 | 0.79 | 34.0% | 31.6% | 43.7% | 33.9%/24.3% | 9.6 (interpolated) | pass | 0.037 (unverified) | 0.42 |
| 26 | `cfg_6d8e` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=3, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=0.75, target_r=2.0, max_hold=24 | 100/77/0 | 177 | 7.0% | 1.4% | 0.82 | -2.3% | 438 | 1.45 | 0.8% | 70.8 | 14/14 | 0.93 | 0.53 | 0.29 | 3 | 1.0% | 0.85 | 0.72 | 5.3% | 3.6% | -11.2% | 6.7%/5.2% | 3.1 (interpolated) | pass | 0.045 (unverified) | -0.10 |
| 27 | `cfg_6944` | timeframe=15min, rsi_lookback=21, pivot_left=8, pivot_right=1, max_pivot_gap=48, min_rsi_diff=0.0, stop_atr=2.0, target_r=1.5, max_hold=6 | 34/21/96 | 151 | 18.9% | 3.5% | 0.85 | -5.3% | 368 | 1.60 | 2.7% | 60.7 | 13/13 | 0.77 | 0.53 | 0.32 | 4 | 9.9% | 0.48 | 0.66 | 17.0% | 15.1% | 6.8% | 17.3%/13.7% | 6.3 (interpolated) | pass | 0.051 (unverified) | 0.66 |
| 28 | `cfg_9c75` | timeframe=15min, rsi_lookback=14, pivot_left=3, pivot_right=3, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=3.0, max_hold=12 | 93/18/104 | 215 | 21.8% | 4.0% | 0.82 | -5.5% | 395 | 1.39 | 6.2% | 86.3 | 13/13 | 0.77 | 0.51 | 0.31 | 4 | 8.6% | 0.60 | 0.53 | 18.9% | 16.1% | 8.8% | 18.8%/12.6% | 5.2 (interpolated) | pass | 0.056 (unverified) | -0.12 |
| 29 | `cfg_bfa7` | timeframe=15min, rsi_lookback=10, pivot_left=3, pivot_right=3, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.0, target_r=2.0, max_hold=48 | 139/86/15 | 240 | 36.1% | 6.4% | 0.78 | -9.9% | 363 | 1.28 | 13.0% | 97.7 | 12/12 | 0.83 | 0.49 | 0.29 | 5 | 14.4% | 0.59 | 0.64 | 33.0% | 29.9% | 38.5% | 32.7%/20.9% | 7.6 (interpolated) | pass | 0.049 (unverified) | 0.04 |
| 30 | `cfg_7769` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=48, min_rsi_diff=8.0, stop_atr=1.5, target_r=3.0, max_hold=48 | 123/51/38 | 212 | 14.7% | 2.8% | 0.78 | -4.7% | 347 | 1.37 | 4.2% | 84.8 | 13/13 | 0.77 | 0.48 | 0.30 | 4 | 6.1% | 0.54 | 0.61 | 12.2% | 9.8% | 19.6% | 13.5%/9.6% | 4.1 (interpolated) | pass | 0.047 (unverified) | -0.37 |
| 31 | `cfg_d6a1` | timeframe=5min, rsi_lookback=14, pivot_left=3, pivot_right=3, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=2.0, target_r=2.0, max_hold=48 | 79/53/30 | 162 | 17.6% | 3.3% | 0.76 | -4.3% | 246 | 1.49 | 3.6% | 64.8 | 12/12 | 1.00 | 0.48 | 0.28 | 4 | 8.2% | 0.53 | 0.71 | 15.7% | 13.9% | 6.8% | 16.5%/12.0% | 6.1 (interpolated) | pass | 0.032 (unverified) | -0.25 |
| 32 | `cfg_982a` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.0, target_r=2.0, max_hold=6 | 99/30/420 | 549 | 18.1% | 3.4% | 0.76 | -5.5% | 250 | 1.29 | 3.5% | 220.0 | 12/12 | 0.75 | 0.44 | 0.31 | 4 | 3.7% | 0.76 | 0.80 | 11.0% | 4.4% | 0.7% | 16.3%/12.1% | 2.4 (interpolated) | pass | 0.042 (unverified) | 0.01 |
| 33 | `cfg_bc45` | timeframe=15min, rsi_lookback=14, pivot_left=3, pivot_right=3, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.0, target_r=2.0, max_hold=48 | 130/85/14 | 229 | 34.5% | 6.1% | 0.77 | -8.2% | 401 | 1.29 | 12.7% | 91.6 | 13/13 | 0.77 | 0.41 | 0.36 | 5 | 21.6% | 0.35 | 0.66 | 31.5% | 28.7% | 34.5% | 30.6%/21.8% | 7.7 (interpolated) | pass | 0.044 (unverified) | 0.12 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | -0.8% / -0.29 / 37 | 0.4% / 0.21 / 47 | 14.1% / 2.58 / 25 | 5.3% / 2.30 / 43 | 2.7% / 0.78 / 46 |
| 2 | 0.2% / 0.09 / 37 | -0.3% / -0.23 / 47 | 14.0% / 2.77 / 25 | 1.8% / 1.13 / 45 | 0.7% / 0.32 / 47 |
| 3 | 1.3% / 0.46 / 38 | 0.0% / 0.02 / 40 | 13.5% / 2.36 / 28 | 3.9% / 1.65 / 42 | 2.7% / 0.66 / 51 |
| 4 | 5.4% / 1.18 / 32 | 4.4% / 1.53 / 27 | 9.0% / 1.11 / 27 | -0.3% / -0.11 / 22 | 6.5% / 1.08 / 57 |
| 5 | 2.8% / 0.53 / 36 | 13.0% / 3.29 / 25 | 16.1% / 1.61 / 29 | -0.8% / -0.17 / 24 | 0.9% / 0.15 / 52 |
| 6 | 0.5% / 0.12 / 40 | 9.3% / 2.02 / 32 | 20.1% / 2.02 / 32 | 0.8% / 0.23 / 28 | 2.4% / 0.34 / 64 |
| 7 | -3.3% / -1.28 / 55 | 2.3% / 1.12 / 45 | 10.0% / 1.34 / 54 | 2.1% / 0.81 / 72 | 12.2% / 2.36 / 76 |
| 8 | -1.5% / -0.91 / 26 | 0.9% / 0.60 / 28 | 6.8% / 1.12 / 36 | 1.0% / 0.57 / 39 | 10.6% / 2.91 / 44 |
| 9 | -3.1% / -0.59 / 32 | 17.0% / 2.95 / 30 | 20.5% / 1.54 / 31 | -2.1% / -0.41 / 31 | 5.7% / 0.71 / 48 |
| 10 | 3.4% / 0.76 / 37 | 12.5% / 3.86 / 26 | 11.4% / 1.31 / 29 | 1.5% / 0.50 / 24 | -0.9% / -0.10 / 55 |
| 11 | -4.5% / -2.12 / 48 | 1.3% / 0.64 / 50 | 9.6% / 1.33 / 50 | 2.9% / 1.14 / 66 | 9.8% / 2.19 / 75 |
| 12 | 5.0% / 0.63 / 44 | 6.3% / 1.35 / 32 | 25.7% / 1.75 / 35 | -1.1% / -0.18 / 33 | 7.0% / 0.66 / 52 |
| 13 | 4.4% / 0.67 / 51 | 3.7% / 1.06 / 33 | 17.5% / 1.65 / 35 | 3.5% / 0.84 / 36 | 6.0% / 0.68 / 56 |
| 14 | -2.9% / -1.15 / 55 | 0.2% / 0.09 / 69 | 10.3% / 1.64 / 50 | 5.7% / 2.11 / 70 | 3.3% / 0.75 / 77 |
| 15 | 4.6% / 0.82 / 41 | 11.2% / 2.22 / 36 | 20.2% / 2.00 / 34 | -0.0% / 0.02 / 32 | -3.1% / -0.36 / 67 |
| 16 | 5.8% / 1.00 / 33 | 3.7% / 0.95 / 28 | 22.8% / 1.99 / 33 | -1.1% / -0.39 / 19 | 5.2% / 0.66 / 37 |
| 17 | 0.9% / 0.23 / 32 | 9.5% / 1.94 / 31 | 10.4% / 1.10 / 30 | -1.1% / -0.29 / 32 | 4.8% / 0.70 / 51 |
| 18 | -0.4% / -0.22 / 37 | -0.6% / -0.38 / 47 | 7.7% / 2.77 / 25 | 1.5% / 1.05 / 43 | 0.2% / 0.09 / 46 |
| 19 | 6.2% / 1.05 / 32 | 10.3% / 1.94 / 26 | 4.2% / 0.36 / 25 | -3.2% / -0.83 / 21 | 18.7% / 1.89 / 54 |
| 20 | -4.4% / -1.04 / 37 | 2.9% / 0.97 / 31 | 26.6% / 2.52 / 36 | -0.2% / -0.07 / 22 | 1.6% / 0.26 / 52 |
| 21 | 3.3% / 0.54 / 40 | 13.6% / 2.39 / 32 | 8.0% / 0.60 / 32 | 2.6% / 0.53 / 28 | 8.1% / 0.85 / 64 |
| 22 | 3.6% / 0.55 / 51 | 4.7% / 1.11 / 38 | 28.4% / 2.22 / 45 | 2.7% / 0.58 / 42 | -0.1% / 0.05 / 74 |
| 23 | -2.2% / -0.45 / 81 | 2.6% / 0.80 / 73 | 16.9% / 1.92 / 61 | 8.0% / 1.93 / 78 | 0.3% / 0.08 / 93 |
| 24 | -1.7% / -0.45 / 81 | -1.1% / -0.42 / 75 | 13.9% / 2.30 / 62 | 2.6% / 0.83 / 79 | 4.4% / 0.85 / 95 |
| 25 | -3.5% / -0.45 / 36 | 4.1% / 0.94 / 30 | 27.2% / 1.85 / 38 | 1.0% / 0.28 / 24 | 5.7% / 0.59 / 45 |
| 26 | -0.4% / -0.23 / 32 | 0.0% / 0.06 / 37 | 6.0% / 2.19 / 25 | -0.0% / -0.01 / 46 | 1.3% / 0.83 / 37 |
| 27 | 1.1% / 0.37 / 29 | 1.2% / 0.59 / 23 | 8.2% / 1.24 / 25 | -0.7% / -0.32 / 20 | 8.2% / 1.53 / 54 |
| 28 | -0.6% / -0.10 / 51 | 3.9% / 1.63 / 34 | 3.2% / 0.51 / 36 | 2.0% / 0.67 / 37 | 12.1% / 1.71 / 57 |
| 29 | 5.8% / 0.84 / 48 | 5.4% / 1.17 / 37 | 19.0% / 1.58 / 45 | 1.1% / 0.24 / 40 | 1.5% / 0.19 / 70 |
| 30 | -3.0% / -0.72 / 41 | 1.0% / 0.39 / 47 | 8.1% / 1.90 / 32 | 2.9% / 1.19 / 45 | 5.2% / 1.22 / 47 |
| 31 | -0.2% / -0.05 / 26 | 1.2% / 0.57 / 28 | 3.3% / 0.46 / 39 | 3.8% / 1.53 / 35 | 8.7% / 2.15 / 34 |
| 32 | -1.2% / -0.36 / 112 | 0.1% / 0.08 / 107 | 13.9% / 1.74 / 88 | 4.7% / 1.63 / 115 | 0.1% / 0.05 / 127 |
| 33 | 3.6% / 0.49 / 54 | 11.2% / 2.25 / 39 | 10.6% / 1.00 / 40 | 0.0% / 0.03 / 36 | 5.5% / 0.56 / 60 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_69b2` | 8 | 0.80 | 0.76/0.80 | 0.82/0.88 |
| 1 | `cfg_0376` | 2 | 0.97 | 0.97/0.97 | 0.86/0.86 |
| 2 | `cfg_a079` | 10 | 0.83 | 0.72/0.89 | 0.35/0.54 |
| 3 | `cfg_7c9f` | 23 | 0.85 | 0.74/0.85 | 0.42/0.58 |
| 4 | `cfg_0588` | 4 | 0.97 | 0.95/0.95 | 0.93/0.95 |
| 5 | `cfg_1d99` | 15 | 0.83 | 0.84/0.87 | 0.46/0.59 |
| 6 | `cfg_a790` | 21 | 0.81 | 0.81/0.89 | 0.56/0.76 |
| 7 | `cfg_07ea` | 4 | 0.88 | 0.83/0.87 | 0.38/0.49 |
| 8 | `cfg_b4ba` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 9 | `cfg_0c30` | 5 | 0.82 | 0.75/0.82 | 0.43/0.62 |
| 10 | `cfg_e535` | 12 | 0.81 | 0.82/0.87 | 0.56/0.60 |
| 11 | `cfg_7095` | 6 | 0.81 | 0.71/0.73 | 0.23/0.27 |
| 12 | `cfg_12a3` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 13 | `cfg_6944` | 4 | 0.94 | 0.75/0.75 | 0.64/0.64 |
| 14 | `cfg_1d3a` | 10 | 0.81 | 0.86/0.90 | 0.60/0.68 |
| 15 | `cfg_7413` | 6 | 0.81 | 0.90/0.94 | 0.68/0.80 |
| 16 | `cfg_25bb` | 2 | 0.90 | 0.93/0.93 | 0.80/0.80 |
| 17 | `cfg_8525` | 4 | 0.84 | 0.83/0.87 | 0.69/0.75 |
| 18 | `cfg_b356` | 4 | 0.87 | 0.90/0.92 | 0.76/0.80 |
| 19 | `cfg_9030` | 8 | 0.87 | 0.85/0.95 | 0.64/0.90 |
| 20 | `cfg_8ec2` | 9 | 0.84 | 0.78/0.83 | 0.80/0.86 |
| 21 | `cfg_4cd6` | 1 | n/a | n/a/n/a | n/a/n/a |
| 22 | `cfg_7769` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 23 | `cfg_5aae` | 3 | 0.92 | 0.89/0.91 | 0.72/0.77 |
| 24 | `cfg_b79e` | 4 | 0.82 | 0.79/0.89 | 0.51/0.71 |
| 25 | `cfg_9c75` | 2 | 0.95 | 0.96/0.96 | 0.90/0.90 |
| 26 | `cfg_6d8e` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 27 | `cfg_7b4b` | 4 | 0.86 | 0.87/0.87 | 0.50/0.50 |
| 28 | `cfg_7554` | 3 | 0.93 | 0.89/0.90 | 0.61/0.66 |
| 29 | `cfg_bc45` | 3 | 0.99 | 0.99/0.99 | 0.97/0.97 |
| 30 | `cfg_982a` | 1 | n/a | n/a/n/a | n/a/n/a |
| 31 | `cfg_bfa7` | 1 | n/a | n/a/n/a | n/a/n/a |
| 32 | `cfg_d6a1` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 8.113e-04 over 91712 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1203.0, participation ratio 26.9, 95%-variance components 236 (rank bound T = 1259); raw grid 98304; raw + known prior 441768
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Drawdown limit -30% is reused from the channel-breakout funnel (src/experiments/validation.py); that approval was given for 0.25%-risk stop-based sizing, while this strategy invests full equity per trade (the ATR stop bounds the per-trade loss, but not as a fixed % of equity) -- it has not been separately approved for this sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0: Sharpe vs. cash is overstated in high-rate years (2023-2024 ~5%).
- Variable cost stress scales per-share commission and slippage bps; the $1 per-order minimum commission is treated as fixed. Baseline limit (target) slippage is 0 bps, so cost stress does not touch target fills.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Prices are split-adjusted but NOT dividend-adjusted: SPY's ~1.5%/yr dividend is not credited while long, and an ex-dividend drop can create a spurious price lower low.
- Long-only regular bullish divergence; bearish / hidden divergences and short trades are not tested.
- Pivots are detected on RSI (TradingView built-in convention) and price is compared at those same bars; a price-pivot-based definition would select different signals.
- Neighbor lattice: every axis is ordered (timeframe, RSI period, pivot left/right, max pivot gap, min RSI diff, stop ATR, target R, max hold); only symbol is held fixed.
- All lookbacks, pivot widths, gaps and holding periods are counted in bars of the config's timeframe, so the same values span very different clock time on 5min vs 1h bars.

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
QQQ results are unchanged rules on the development period: supporting evidence, not an independent replication.

## Integrity audit

- RSI = Wilder RSI(rsi_lookback) of closes (bars of the config's timeframe), seeded with the simple average of the first N gains/losses; RSI_t uses closes up to and including bar t.
- An RSI pivot low at bar p (RSI_p < the pivot_left RSIs before it and <= the pivot_right RSIs after it) is only known at the close of bar p + pivot_right; that confirmation bar is the signal bar, and the entry fills at the NEXT bar's open.
- Bullish divergence: between two CONSECUTIVE confirmed RSI pivot lows q < p with p - q <= max_pivot_gap, RSI_p - RSI_q > 0 and >= min_rsi_diff (RSI higher low) and low_p < low_q (price lower low at the pivot bars).
- 1R = stop_atr x ATR(14) using the ATR known before the entry fill; stop = entry-bar open - 1R, target = entry-bar open + target_r x R, both live from the entry bar.
- Stop touch exits at the worse of the bar's open and the stop; target touch exits AT the target (a gap above it is not credited); a bar touching both is treated as a stop exit (conservative).
- Otherwise the position exits at the next bar's open after max_hold bars, so a time exit fills exactly max_hold bars after entry. Sizing: as many whole shares as current equity affords (no leverage), as in the mean-reversion funnels.
- Signals confirmed while a position is open are ignored; missed-entry stress drops whole signals (each divergence is a single-bar event), never re-entering one bar later.
- Adverse slippage + commission on every fill; a fill at a session's first bar bears the full overnight gap.
- Development backtests run on data physically truncated at the development end; open positions are force-closed at the last development bar and flagged (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Positions are held overnight (no session-end flattening), as in the other families; RSI, pivots and ATR run continuously across sessions over RTH bars only.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Unresolved assumptions

- Drawdown limit -30% is reused from the channel-breakout funnel (src/experiments/validation.py); that approval was given for 0.25%-risk stop-based sizing, while this strategy invests full equity per trade -- it has not been separately approved for this sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0: Sharpe vs. cash is overstated in high-rate years (2023-2024 ~5%).
- Variable cost stress scales per-share commission and slippage bps; the $1 per-order minimum commission is treated as fixed.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Prices are split-adjusted but NOT dividend-adjusted: SPY's ~1.5%/yr dividend is not credited while long, and each ex-dividend drop slightly lowers z (a small bias toward entries on ex-div dates).
- Neighbor lattice: v1 orders timeframe, mean/std lookback, entry/exit z and max hold; v2 orders timeframe, mean lookback, entry/exit z, max holding bars, cooldown and ATR stop (1.0 < 1.5 < 2.0 < 3.0 < none). mean_type, trend_filter (and v2 entry_confirmation) are held fixed (categorical).
- All lookbacks, trend SMAs and holding periods are counted in bars of the config's timeframe (e.g. sma200 on 5min bars spans ~2.6 sessions), not in trading days.
