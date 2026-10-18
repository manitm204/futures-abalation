# Screening funnel -- rsi_v2 (development stages only)

- Code: `b13e04bc391f` (dirty working tree: True, diff sha256 `819a09c96490`)
- Config: `configs/funnel/rsi_funnel_v2.yaml` sha256 `97a7fe908fa83273`; seed 20261016
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'QQQ': '2026-08-18', 'SPY': '2026-08-18'}
- Frozen manifest sha256: `1350e2d099782575` (91 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- rsi_v1 evaluated 33 frozen RSI-divergence candidates on 2023-2024 (8 passed) and the v2 parameter space was designed after those results were read. The same slice also gated the mean-reversion funnels, the channel-breakout funnels and the Donchian ablation.
- Holdout 2025+ previously inspected: **True** -- SPY 2025-2026 holdout metrics were computed and inspected for the Donchian ablation and the channel-breakout funnels (funnel_v1..v3 records.parquet). The holdout is NOT an untouched test of SPY.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 69984 | 69984 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 69984 | 69984 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 69984 | 13645 | 56339 | 0 |  | 35873 | 19.50 | 19.50 |  |
| 3 performance & risk | hard_gate | 13645 | 674 | 12971 | 0 |  | 0 | 0.96 | 4.94 |  |
| 4 parameter stability | hard_gate | 674 | 674 | 0 | 0 |  | 674 | 0.96 | 100.00 |  |
| 5 time stability | hard_gate | 674 | 658 | 16 | 0 |  | 575 | 0.94 | 97.63 |  |
| 6 deduplication | dedup | 658 | 91 |  |  | 567 |  | 0.13 | 13.83 |  |
| 7 execution stress | hard_gate | 91 | 91 | 0 | 0 |  | 1 | 0.13 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 91 |  |  |  |  |  |  |  | diagnostic only: unverified: 91 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 56339 |
| s2:hard_reject:years_with_>=10_trades | 42536 |
| s3:hard_reject:max_drawdown | 115 |
| s3:hard_reject:net_return | 6254 |
| s3:hard_reject:sharpe | 12971 |
| s5:hard_reject:profitable_years | 16 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | stop/target/time exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | QQQ dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_4aef` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=2.0, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.0 | 97/83/10 | 190 | 24.6% | 4.5% | 1.33 | -3.8% | 219 | 1.81 | 2.7% | 76.2 | 16/16 | 1.00 | 1.10 | 0.23 | 5 | 9.1% | 0.58 | 0.44 | 22.4% | 20.2% | 18.0% | 22.1%/19.0% | 7.2 (interpolated) | pass | 0.461 (unverified) | -0.13 |
| 2 | `cfg_ae5b` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=2.5, target_r=1.5, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.0 | 71/74/30 | 175 | 29.2% | 5.3% | 1.37 | -4.0% | 201 | 1.80 | 4.1% | 70.3 | 14/14 | 1.00 | 1.03 | 0.34 | 5 | 13.6% | 0.49 | 0.40 | 27.1% | 25.1% | 20.2% | 26.3%/21.8% | 8.8 (interpolated) | pass | 0.500 (unverified) | 0.17 |
| 3 | `cfg_6e15` | timeframe=5min, rsi_lookback=10, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=2.5, target_r=1.5, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 94/87/40 | 221 | 27.9% | 5.1% | 1.16 | -4.9% | 518 | 1.60 | 5.3% | 89.3 | 14/14 | 0.93 | 1.02 | 0.14 | 4 | 13.7% | 0.51 | 0.41 | 25.3% | 22.7% | 21.3% | 25.0%/19.2% | 6.9 (interpolated) | pass | 0.297 (unverified) | -0.92 |
| 4 | `cfg_b271` | timeframe=15min, rsi_lookback=7, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.0, target_r=1.5, max_hold=24, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.25 | 82/88/25 | 195 | 46.9% | 8.0% | 1.22 | -7.7% | 262 | 1.57 | 7.5% | 79.0 | 14/14 | 0.93 | 1.02 | 0.20 | 5 | 16.8% | 0.60 | 0.41 | 44.2% | 41.6% | 35.8% | 42.2%/34.8% | 11.6 (interpolated) | pass | 0.361 (unverified) | -0.00 |
| 5 | `cfg_1c68` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=2.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.0 | 90/76/10 | 176 | 20.7% | 3.8% | 1.26 | -3.8% | 219 | 1.74 | 2.5% | 70.5 | 15/15 | 1.00 | 1.01 | 0.24 | 4 | 8.7% | 0.53 | 0.42 | 18.7% | 16.8% | 13.8% | 18.2%/15.3% | 6.7 (interpolated) | pass | 0.383 (unverified) | -0.09 |
| 6 | `cfg_2ad3` | timeframe=5min, rsi_lookback=10, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=2.5, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.25 | 82/21/84 | 187 | 32.4% | 5.8% | 1.21 | -4.3% | 531 | 1.78 | 6.1% | 75.4 | 14/14 | 0.93 | 1.01 | 0.20 | 4 | 14.4% | 0.56 | 0.47 | 29.7% | 27.1% | 22.8% | 28.6%/22.4% | 7.9 (interpolated) | pass | 0.336 (unverified) | -0.25 |
| 7 | `cfg_2720` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=2.5, target_r=2.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 73/46/41 | 160 | 23.7% | 4.4% | 1.15 | -5.5% | 229 | 1.64 | 4.3% | 64.3 | 16/16 | 0.94 | 1.00 | 0.15 | 4 | 10.0% | 0.54 | 0.47 | 21.7% | 19.8% | 24.9% | 21.1%/16.7% | 7.6 (interpolated) | pass | 0.285 (unverified) | 0.32 |
| 8 | `cfg_835a` | timeframe=15min, rsi_lookback=14, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.0, target_r=1.5, max_hold=24, rsi_extreme=off, adx_filter=off, min_price_div_atr=0.25 | 66/64/21 | 151 | 39.5% | 6.9% | 1.16 | -7.3% | 348 | 1.66 | 5.8% | 60.6 | 14/14 | 0.93 | 0.99 | 0.17 | 4 | 18.7% | 0.48 | 0.47 | 37.5% | 35.6% | 33.8% | 34.9%/28.2% | 12.7 (interpolated) | pass | 0.312 (unverified) | 0.43 |
| 9 | `cfg_9332` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=2.5, target_r=1.5, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 67/67/26 | 160 | 22.5% | 4.1% | 1.23 | -4.0% | 190 | 1.67 | 3.6% | 64.4 | 15/15 | 1.00 | 0.96 | 0.27 | 5 | 11.9% | 0.44 | 0.39 | 20.7% | 18.9% | 19.7% | 19.6%/16.9% | 7.8 (interpolated) | pass | 0.366 (unverified) | 0.10 |
| 10 | `cfg_a1c3` | timeframe=5min, rsi_lookback=10, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 132/55/35 | 222 | 24.7% | 4.5% | 1.03 | -5.7% | 531 | 1.61 | 4.5% | 89.8 | 14/14 | 0.93 | 0.95 | 0.08 | 4 | 13.6% | 0.45 | 0.53 | 22.0% | 19.2% | 27.3% | 23.0%/18.3% | 5.9 (interpolated) | pass | 0.165 (unverified) | -0.42 |
| 11 | `cfg_1f0e` | timeframe=5min, rsi_lookback=10, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=2.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 123/85/15 | 223 | 20.3% | 3.8% | 1.11 | -4.0% | 531 | 1.55 | 3.4% | 89.8 | 15/15 | 1.00 | 0.94 | 0.17 | 4 | 9.9% | 0.51 | 0.44 | 17.7% | 15.3% | 16.8% | 18.4%/14.8% | 5.4 (interpolated) | pass | 0.250 (unverified) | -1.03 |
| 12 | `cfg_82fa` | timeframe=5min, rsi_lookback=10, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=2.5, target_r=3.0, max_hold=24, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.25 | 60/9/118 | 187 | 28.1% | 5.1% | 1.19 | -3.6% | 244 | 1.85 | 3.7% | 75.4 | 14/14 | 1.00 | 0.94 | 0.25 | 4 | 14.3% | 0.49 | 0.56 | 25.5% | 22.9% | 17.9% | 25.9%/20.9% | 6.9 (interpolated) | pass | 0.297 (unverified) | -0.34 |
| 13 | `cfg_8f06` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=2.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 83/69/9 | 161 | 17.0% | 3.2% | 1.19 | -2.8% | 212 | 1.68 | 2.3% | 64.6 | 16/16 | 1.00 | 0.93 | 0.27 | 4 | 8.6% | 0.46 | 0.40 | 15.3% | 13.5% | 15.1% | 14.9%/12.5% | 6.2 (interpolated) | pass | 0.333 (unverified) | -0.23 |
| 14 | `cfg_1fb9` | timeframe=5min, rsi_lookback=14, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.5, target_r=2.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.25 | 119/79/75 | 273 | 35.1% | 6.2% | 1.11 | -5.6% | 197 | 1.48 | 7.5% | 111.0 | 14/14 | 1.00 | 0.92 | 0.19 | 4 | 20.7% | 0.41 | 0.37 | 31.4% | 27.8% | 29.1% | 32.6%/26.2% | 6.5 (interpolated) | pass | 0.270 (unverified) | -0.24 |
| 15 | `cfg_4104` | timeframe=15min, rsi_lookback=7, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=2.0, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.25 | 95/75/2 | 172 | 34.8% | 6.2% | 1.06 | -8.1% | 394 | 1.54 | 6.0% | 69.1 | 16/16 | 1.00 | 0.92 | 0.14 | 4 | 5.7% | 0.80 | 0.52 | 32.6% | 30.5% | 26.7% | 31.2%/24.6% | 10.3 (interpolated) | pass | 0.231 (unverified) | 0.12 |
| 16 | `cfg_b0bc` | timeframe=15min, rsi_lookback=14, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.0, target_r=2.0, max_hold=24, rsi_extreme=off, adx_filter=off, min_price_div_atr=0.25 | 70/44/36 | 150 | 42.4% | 7.3% | 1.09 | -7.4% | 384 | 1.65 | 6.5% | 60.2 | 15/15 | 0.93 | 0.91 | 0.18 | 5 | 23.7% | 0.40 | 0.57 | 40.2% | 38.1% | 44.6% | 36.9%/28.2% | 12.7 (interpolated) | pass | 0.252 (unverified) | 0.31 |
| 17 | `cfg_bcc8` | timeframe=15min, rsi_lookback=7, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.5, target_r=1.5, max_hold=24, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.25 | 75/63/51 | 189 | 45.4% | 7.8% | 1.05 | -9.5% | 356 | 1.49 | 9.1% | 76.5 | 13/13 | 0.92 | 0.91 | 0.14 | 5 | 20.9% | 0.52 | 0.55 | 42.7% | 40.0% | 43.9% | 42.1%/32.5% | 11.0 (interpolated) | pass | 0.229 (unverified) | 0.29 |
| 18 | `cfg_eb36` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 94/45/22 | 161 | 20.0% | 3.7% | 1.09 | -3.6% | 227 | 1.69 | 3.1% | 64.6 | 15/15 | 1.00 | 0.91 | 0.18 | 4 | 9.3% | 0.49 | 0.49 | 18.1% | 16.2% | 26.6% | 18.3%/15.2% | 6.6 (interpolated) | pass | 0.239 (unverified) | 0.06 |
| 19 | `cfg_8e6c` | timeframe=5min, rsi_lookback=14, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.25 | 144/55/77 | 276 | 29.8% | 5.4% | 0.96 | -4.7% | 517 | 1.44 | 7.2% | 112.1 | 14/14 | 1.00 | 0.89 | 0.07 | 4 | 13.3% | 0.55 | 0.46 | 26.1% | 22.6% | 17.7% | 26.6%/21.3% | 5.5 (interpolated) | pass | 0.167 (unverified) | 0.20 |
| 20 | `cfg_a8ed` | timeframe=5min, rsi_lookback=10, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=3.0, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.1 | 148/61/38 | 247 | 27.0% | 4.9% | 1.00 | -6.1% | 529 | 1.58 | 4.9% | 100.0 | 15/15 | 0.93 | 0.89 | 0.11 | 4 | 12.2% | 0.47 | 0.60 | 23.9% | 20.8% | 13.7% | 24.5%/18.3% | 5.8 (interpolated) | pass | 0.144 (unverified) | -0.32 |
| 21 | `cfg_ef0a` | timeframe=5min, rsi_lookback=10, pivot_left=3, pivot_right=1, max_pivot_gap=24, min_rsi_diff=5.0, stop_atr=2.5, target_r=2.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.5 | 70/39/45 | 154 | 22.1% | 4.1% | 1.17 | -3.1% | 264 | 1.72 | 4.3% | 62.0 | 13/13 | 0.92 | 0.88 | 0.29 | 4 | 13.5% | 0.39 | 0.43 | 20.2% | 18.3% | 16.1% | 20.2%/16.4% | 7.4 (interpolated) | pass | 0.305 (unverified) | -0.32 |
| 22 | `cfg_0422` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=5.0, stop_atr=2.5, target_r=2.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.5 | 83/45/66 | 194 | 21.0% | 3.9% | 1.04 | -6.5% | 517 | 1.49 | 5.6% | 77.7 | 14/14 | 0.86 | 0.88 | 0.16 | 4 | 9.7% | 0.48 | 0.43 | 18.6% | 16.2% | 14.2% | 19.4%/16.0% | 5.8 (interpolated) | pass | 0.226 (unverified) | -0.77 |
| 23 | `cfg_fdbc` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=2.5, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 76/19/64 | 159 | 24.6% | 4.5% | 1.13 | -3.8% | 215 | 1.63 | 4.9% | 64.3 | 15/15 | 0.93 | 0.88 | 0.26 | 5 | 12.2% | 0.46 | 0.50 | 22.5% | 20.4% | 21.8% | 21.8%/18.3% | 7.3 (interpolated) | pass | 0.273 (unverified) | 0.33 |
| 24 | `cfg_db0e` | timeframe=5min, rsi_lookback=14, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=2.0, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.0 | 88/64/16 | 168 | 19.7% | 3.7% | 1.09 | -2.0% | 528 | 1.70 | 2.7% | 67.7 | 14/14 | 1.00 | 0.87 | 0.22 | 4 | 8.2% | 0.59 | 0.53 | 17.8% | 15.9% | 12.1% | 18.0%/14.1% | 6.6 (interpolated) | pass | 0.218 (unverified) | -1.09 |
| 25 | `cfg_3280` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.0 | 205/95/50 | 350 | 28.9% | 5.2% | 1.04 | -6.4% | 252 | 1.40 | 6.9% | 140.4 | 14/14 | 1.00 | 0.87 | 0.17 | 4 | 15.1% | 0.46 | 0.50 | 24.4% | 20.0% | 25.7% | 25.9%/20.6% | 4.6 (interpolated) | pass | 0.213 (unverified) | -0.40 |
| 26 | `cfg_2765` | timeframe=5min, rsi_lookback=14, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 107/49/52 | 208 | 33.0% | 5.9% | 1.18 | -5.4% | 328 | 1.63 | 5.1% | 84.4 | 15/15 | 1.00 | 0.86 | 0.32 | 4 | 19.7% | 0.40 | 0.47 | 30.3% | 27.5% | 20.9% | 29.2%/22.3% | 7.7 (interpolated) | pass | 0.317 (unverified) | 0.46 |
| 27 | `cfg_4f07` | timeframe=5min, rsi_lookback=10, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=1.5, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 115/101/7 | 223 | 14.3% | 2.7% | 0.99 | -4.5% | 531 | 1.43 | 2.7% | 89.9 | 14/14 | 0.86 | 0.86 | 0.13 | 4 | 1.6% | 0.84 | 0.51 | 12.0% | 9.7% | 13.1% | 13.1%/10.3% | 4.3 (interpolated) | pass | 0.166 (unverified) | -0.89 |
| 28 | `cfg_cec0` | timeframe=15min, rsi_lookback=7, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=1.5, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.5 | 78/81/0 | 159 | 24.0% | 4.4% | 0.96 | -4.8% | 365 | 1.49 | 4.8% | 64.4 | 12/12 | 0.92 | 0.85 | 0.11 | 3 | 2.5% | 0.85 | 0.50 | 22.3% | 20.5% | 9.3% | 22.0%/16.0% | 8.5 (interpolated) | pass | 0.158 (unverified) | -0.32 |
| 29 | `cfg_4c9d` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=2.0, target_r=3.0, max_hold=24, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 75/19/66 | 160 | 19.9% | 3.7% | 0.99 | -2.9% | 215 | 1.64 | 2.7% | 64.1 | 16/16 | 0.94 | 0.85 | 0.15 | 5 | 5.6% | 0.70 | 0.67 | 17.8% | 15.8% | 15.7% | 18.1%/13.6% | 6.2 (interpolated) | pass | 0.153 (unverified) | 0.46 |
| 30 | `cfg_171c` | timeframe=5min, rsi_lookback=14, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.5, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.25 | 122/38/112 | 272 | 36.5% | 6.4% | 1.02 | -7.8% | 199 | 1.50 | 8.6% | 110.4 | 13/13 | 0.92 | 0.85 | 0.17 | 4 | 16.5% | 0.55 | 0.38 | 32.6% | 28.7% | 24.7% | 33.6%/27.1% | 6.3 (interpolated) | pass | 0.203 (unverified) | -0.10 |
| 31 | `cfg_4e6e` | timeframe=5min, rsi_lookback=10, pivot_left=3, pivot_right=1, max_pivot_gap=24, min_rsi_diff=5.0, stop_atr=2.5, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.5 | 72/15/67 | 154 | 21.8% | 4.0% | 1.09 | -3.1% | 293 | 1.69 | 4.9% | 61.9 | 12/12 | 0.92 | 0.84 | 0.25 | 4 | 10.0% | 0.54 | 0.51 | 19.8% | 17.8% | 18.2% | 19.5%/14.8% | 6.9 (interpolated) | pass | 0.239 (unverified) | -0.15 |
| 32 | `cfg_a3ee` | timeframe=15min, rsi_lookback=7, pivot_left=8, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.0, target_r=1.5, max_hold=24, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.25 | 69/72/22 | 163 | 31.0% | 5.6% | 0.92 | -8.8% | 229 | 1.43 | 5.7% | 65.7 | 14/14 | 0.93 | 0.83 | 0.09 | 4 | 7.7% | 0.80 | 0.59 | 29.0% | 27.1% | 12.5% | 28.6%/20.4% | 9.9 (interpolated) | pass | 0.149 (unverified) | 0.42 |
| 33 | `cfg_8bc2` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.5 | 133/56/62 | 251 | 33.5% | 6.0% | 1.16 | -4.8% | 251 | 1.54 | 6.2% | 100.8 | 15/15 | 1.00 | 0.82 | 0.34 | 4 | 19.9% | 0.41 | 0.41 | 30.0% | 26.7% | 14.5% | 29.1%/24.4% | 6.6 (interpolated) | pass | 0.297 (unverified) | -0.16 |
| 34 | `cfg_3ade` | timeframe=15min, rsi_lookback=7, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.0, target_r=2.0, max_hold=24, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.25 | 101/60/52 | 213 | 37.5% | 6.6% | 0.89 | -13.2% | 355 | 1.37 | 9.3% | 86.3 | 16/16 | 0.94 | 0.82 | 0.07 | 4 | 18.3% | 0.50 | 0.67 | 34.6% | 31.7% | 44.4% | 33.7%/25.8% | 8.4 (interpolated) | pass | 0.132 (unverified) | -0.12 |
| 35 | `cfg_e994` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=2.0, target_r=2.0, max_hold=24, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 74/37/49 | 160 | 15.3% | 2.9% | 0.92 | -2.9% | 215 | 1.51 | 2.5% | 64.2 | 17/17 | 0.94 | 0.81 | 0.11 | 4 | 4.3% | 0.70 | 0.57 | 13.4% | 11.5% | 14.3% | 13.3%/10.0% | 5.3 (interpolated) | pass | 0.134 (unverified) | 0.36 |
| 36 | `cfg_24f0` | timeframe=5min, rsi_lookback=14, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 186/78/52 | 316 | 24.3% | 4.4% | 0.95 | -6.3% | 548 | 1.38 | 6.4% | 128.6 | 13/13 | 1.00 | 0.81 | 0.14 | 4 | 10.0% | 0.59 | 0.44 | 20.3% | 16.5% | 20.6% | 22.0%/17.5% | 4.4 (interpolated) | pass | 0.157 (unverified) | -0.46 |
| 37 | `cfg_9579` | timeframe=5min, rsi_lookback=14, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.5, target_r=1.5, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 124/118/56 | 298 | 26.2% | 4.8% | 0.95 | -7.0% | 517 | 1.35 | 7.3% | 121.2 | 13/13 | 1.00 | 0.80 | 0.15 | 4 | 14.4% | 0.45 | 0.36 | 22.7% | 19.3% | 26.0% | 24.7%/20.1% | 5.2 (interpolated) | pass | 0.172 (unverified) | -0.53 |
| 38 | `cfg_71cf` | timeframe=5min, rsi_lookback=7, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=2.0, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.0 | 174/130/13 | 317 | 22.1% | 4.1% | 1.03 | -5.3% | 521 | 1.40 | 4.3% | 127.6 | 15/15 | 1.00 | 0.80 | 0.23 | 4 | 11.0% | 0.44 | 0.51 | 18.5% | 15.0% | 12.4% | 19.1%/14.7% | 4.4 (interpolated) | pass | 0.212 (unverified) | -0.08 |
| 39 | `cfg_d6ff` | timeframe=15min, rsi_lookback=7, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.0, target_r=2.0, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.25 | 92/67/6 | 165 | 39.9% | 7.0% | 0.89 | -11.3% | 389 | 1.46 | 8.5% | 66.1 | 17/17 | 1.00 | 0.79 | 0.10 | 5 | 14.2% | 0.61 | 0.64 | 37.8% | 35.6% | 38.9% | 36.3%/26.8% | 11.8 (interpolated) | pass | 0.111 (unverified) | 0.17 |
| 40 | `cfg_ea05` | timeframe=5min, rsi_lookback=14, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.5, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.5 | 114/28/104 | 246 | 23.0% | 4.2% | 0.78 | -6.6% | 517 | 1.36 | 7.8% | 99.6 | 12/12 | 0.92 | 0.79 | -0.01 | 4 | 9.4% | 0.59 | 0.52 | 19.8% | 16.6% | 15.9% | 21.4%/14.9% | 4.9 (interpolated) | pass | 0.078 (unverified) | -0.44 |
| 41 | `cfg_23e8` | timeframe=5min, rsi_lookback=10, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=2.0, target_r=1.5, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 112/92/19 | 223 | 17.0% | 3.2% | 0.89 | -5.9% | 531 | 1.40 | 3.9% | 89.9 | 15/15 | 1.00 | 0.79 | 0.10 | 4 | 7.0% | 0.59 | 0.51 | 14.6% | 12.2% | 12.2% | 15.0%/12.2% | 4.8 (interpolated) | pass | 0.127 (unverified) | -0.74 |
| 42 | `cfg_39dc` | timeframe=5min, rsi_lookback=14, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=3.0, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.0 | 95/41/31 | 167 | 19.3% | 3.6% | 0.83 | -2.3% | 528 | 1.60 | 3.5% | 67.5 | 13/13 | 0.92 | 0.78 | 0.05 | 4 | 9.4% | 0.47 | 0.78 | 17.3% | 15.3% | 14.5% | 17.8%/12.9% | 6.2 (interpolated) | pass | 0.058 (unverified) | -0.58 |
| 43 | `cfg_8dc3` | timeframe=5min, rsi_lookback=14, pivot_left=3, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.5 | 133/48/71 | 252 | 26.1% | 4.7% | 0.93 | -5.3% | 516 | 1.43 | 6.4% | 102.1 | 12/12 | 1.00 | 0.77 | 0.15 | 4 | 12.3% | 0.53 | 0.51 | 22.8% | 19.6% | 11.4% | 23.8%/18.2% | 5.4 (interpolated) | pass | 0.145 (unverified) | 0.45 |
| 44 | `cfg_2542` | timeframe=15min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.0, target_r=2.0, max_hold=24, rsi_extreme=off, adx_filter=off, min_price_div_atr=0.25 | 91/54/47 | 192 | 37.5% | 6.6% | 0.92 | -10.5% | 311 | 1.42 | 8.3% | 77.6 | 16/16 | 1.00 | 0.77 | 0.15 | 5 | 18.1% | 0.50 | 0.65 | 34.9% | 32.2% | 41.9% | 34.0%/24.3% | 9.2 (interpolated) | pass | 0.147 (unverified) | -0.21 |
| 45 | `cfg_ab93` | timeframe=5min, rsi_lookback=14, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.5 | 126/52/60 | 238 | 26.7% | 4.9% | 1.01 | -6.3% | 431 | 1.49 | 5.9% | 95.5 | 15/15 | 1.00 | 0.77 | 0.25 | 4 | 9.6% | 0.64 | 0.50 | 23.6% | 20.6% | 8.1% | 23.4%/18.7% | 5.8 (interpolated) | pass | 0.192 (unverified) | 0.25 |
| 46 | `cfg_8b94` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=5.0, stop_atr=2.5, target_r=1.5, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.0 | 135/125/62 | 322 | 35.1% | 6.2% | 1.19 | -5.8% | 527 | 1.46 | 7.8% | 129.4 | 14/14 | 0.86 | 0.77 | 0.43 | 4 | 11.4% | 0.59 | 0.39 | 31.1% | 27.1% | 1.0% | 31.4%/25.8% | 5.9 (interpolated) | pass | 0.344 (unverified) | -0.35 |
| 47 | `cfg_2854` | timeframe=5min, rsi_lookback=14, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.0 | 131/60/30 | 221 | 19.7% | 3.7% | 0.87 | -5.4% | 519 | 1.42 | 4.3% | 89.4 | 13/13 | 1.00 | 0.76 | 0.11 | 4 | 8.9% | 0.49 | 0.71 | 17.1% | 14.5% | 18.5% | 18.6%/13.3% | 5.1 (interpolated) | pass | 0.112 (unverified) | -0.14 |
| 48 | `cfg_c815` | timeframe=5min, rsi_lookback=10, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=2.5, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.0 | 114/28/104 | 246 | 26.5% | 4.8% | 0.91 | -5.9% | 269 | 1.44 | 7.8% | 99.4 | 13/13 | 0.92 | 0.76 | 0.15 | 4 | 8.7% | 0.67 | 0.56 | 23.2% | 19.9% | 20.6% | 23.7%/17.9% | 5.4 (interpolated) | pass | 0.155 (unverified) | -0.24 |
| 49 | `cfg_5959` | timeframe=15min, rsi_lookback=7, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.0, target_r=2.0, max_hold=24, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.25 | 81/47/38 | 166 | 30.2% | 5.4% | 0.80 | -9.0% | 302 | 1.42 | 7.1% | 66.7 | 17/17 | 1.00 | 0.76 | 0.04 | 4 | 11.1% | 0.60 | 0.77 | 28.1% | 25.9% | 37.3% | 27.2%/21.7% | 8.9 (interpolated) | pass | 0.092 (unverified) | -0.01 |
| 50 | `cfg_5608` | timeframe=5min, rsi_lookback=14, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.5, target_r=2.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.5 | 70/50/37 | 157 | 18.9% | 3.5% | 0.90 | -5.0% | 364 | 1.47 | 4.2% | 63.3 | 14/14 | 1.00 | 0.76 | 0.14 | 5 | 10.6% | 0.44 | 0.59 | 17.1% | 15.3% | 15.6% | 17.0%/12.7% | 6.6 (interpolated) | pass | 0.133 (unverified) | -0.35 |
| 51 | `cfg_7a34` | timeframe=5min, rsi_lookback=14, pivot_left=3, pivot_right=1, max_pivot_gap=24, min_rsi_diff=5.0, stop_atr=1.5, target_r=2.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 83/53/16 | 152 | 11.9% | 2.3% | 0.96 | -3.3% | 552 | 1.52 | 2.5% | 61.0 | 13/13 | 1.00 | 0.76 | 0.20 | 4 | 4.5% | 0.62 | 0.47 | 10.2% | 8.6% | 11.5% | 11.1%/9.2% | 4.8 (interpolated) | pass | 0.165 (unverified) | -1.16 |
| 52 | `cfg_abb2` | timeframe=15min, rsi_lookback=7, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=1.5, target_r=2.0, max_hold=24, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.5 | 97/63/13 | 173 | 24.8% | 4.5% | 0.78 | -8.0% | 415 | 1.38 | 5.8% | 70.0 | 14/14 | 1.00 | 0.75 | 0.02 | 4 | 1.6% | 0.92 | 0.69 | 22.7% | 20.6% | 22.9% | 23.2%/15.8% | 7.6 (interpolated) | pass | 0.079 (unverified) | 0.05 |
| 53 | `cfg_9561` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 173/68/82 | 323 | 38.7% | 6.8% | 1.17 | -6.9% | 317 | 1.47 | 8.0% | 129.8 | 16/16 | 1.00 | 0.74 | 0.43 | 4 | 22.0% | 0.41 | 0.41 | 34.1% | 29.7% | 19.0% | 34.5%/29.5% | 5.9 (interpolated) | pass | 0.312 (unverified) | 0.16 |
| 54 | `cfg_b18f` | timeframe=15min, rsi_lookback=7, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.0, target_r=2.0, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.25 | 120/85/7 | 212 | 43.0% | 7.4% | 0.87 | -13.4% | 401 | 1.37 | 11.0% | 85.6 | 16/16 | 1.00 | 0.74 | 0.13 | 5 | 20.0% | 0.52 | 0.63 | 40.2% | 37.3% | 41.9% | 39.2%/29.5% | 9.9 (interpolated) | pass | 0.111 (unverified) | -0.01 |
| 55 | `cfg_eb69` | timeframe=15min, rsi_lookback=7, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.0, target_r=1.5, max_hold=24, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.25 | 95/88/28 | 211 | 32.7% | 5.8% | 0.88 | -7.8% | 366 | 1.37 | 8.3% | 86.6 | 14/14 | 0.93 | 0.73 | 0.15 | 4 | 2.7% | 0.86 | 0.51 | 30.1% | 27.6% | 12.0% | 29.0%/22.5% | 8.1 (interpolated) | pass | 0.131 (unverified) | 0.26 |
| 56 | `cfg_7af9` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.5, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.5 | 170/43/149 | 362 | 29.2% | 5.3% | 0.81 | -7.8% | 517 | 1.30 | 11.3% | 146.0 | 13/13 | 0.92 | 0.73 | 0.07 | 4 | 14.0% | 0.47 | 0.43 | 24.2% | 19.4% | 25.3% | 26.6%/19.2% | 4.3 (interpolated) | pass | 0.096 (unverified) | -0.59 |
| 57 | `cfg_bcc3` | timeframe=15min, rsi_lookback=7, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.5, target_r=1.5, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.25 | 101/93/11 | 205 | 49.7% | 8.4% | 0.96 | -12.2% | 401 | 1.41 | 11.9% | 83.0 | 14/14 | 0.93 | 0.72 | 0.23 | 4 | 19.7% | 0.58 | 0.53 | 46.9% | 44.2% | 34.4% | 42.2%/33.6% | 11.7 (interpolated) | pass | 0.159 (unverified) | 0.15 |
| 58 | `cfg_d95a` | timeframe=5min, rsi_lookback=14, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.5, target_r=1.5, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.0 | 91/85/36 | 212 | 20.7% | 3.8% | 0.91 | -5.3% | 307 | 1.40 | 5.0% | 85.6 | 13/13 | 1.00 | 0.72 | 0.19 | 4 | 12.7% | 0.37 | 0.58 | 18.2% | 15.9% | 10.2% | 19.2%/15.4% | 5.7 (interpolated) | pass | 0.137 (unverified) | 0.09 |
| 59 | `cfg_99e1` | timeframe=5min, rsi_lookback=14, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.5, target_r=3.0, max_hold=24, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.25 | 95/19/158 | 272 | 21.0% | 3.9% | 0.81 | -6.0% | 518 | 1.35 | 5.3% | 109.8 | 13/13 | 1.00 | 0.71 | 0.09 | 4 | 8.2% | 0.61 | 0.56 | 17.4% | 13.9% | 13.5% | 20.0%/14.7% | 4.2 (interpolated) | pass | 0.106 (unverified) | -0.29 |
| 60 | `cfg_9f8d` | timeframe=15min, rsi_lookback=7, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=1.5, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.25 | 107/109/0 | 216 | 24.0% | 4.4% | 0.82 | -6.5% | 372 | 1.33 | 6.2% | 87.7 | 13/13 | 0.92 | 0.71 | 0.11 | 4 | 2.1% | 0.87 | 0.50 | 21.6% | 19.2% | 3.3% | 20.8%/14.4% | 6.5 (interpolated) | pass | 0.103 (unverified) | -0.04 |
| 61 | `cfg_1108` | timeframe=15min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=2.0, max_hold=48, rsi_extreme=off, adx_filter=off, min_price_div_atr=0.1 | 93/68/2 | 163 | 28.8% | 5.2% | 0.91 | -7.4% | 414 | 1.48 | 5.4% | 65.4 | 16/16 | 0.94 | 0.71 | 0.21 | 3 | 1.1% | 0.94 | 0.61 | 26.8% | 24.8% | 35.3% | 25.2%/19.8% | 9.3 (interpolated) | pass | 0.140 (unverified) | 0.31 |
| 62 | `cfg_982c` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=3.0, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.0 | 290/130/65 | 485 | 31.4% | 5.6% | 0.93 | -8.7% | 517 | 1.31 | 9.1% | 195.1 | 15/15 | 1.00 | 0.71 | 0.23 | 4 | 13.9% | 0.54 | 0.56 | 25.1% | 19.1% | 15.7% | 28.2%/21.5% | 3.8 (interpolated) | pass | 0.162 (unverified) | -0.22 |
| 63 | `cfg_190a` | timeframe=5min, rsi_lookback=14, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=3.0, max_hold=48, rsi_extreme=40/60, adx_filter=lt30, min_price_div_atr=0.1 | 90/41/24 | 155 | 15.0% | 2.8% | 0.77 | -2.9% | 279 | 1.53 | 2.8% | 62.0 | 16/16 | 0.94 | 0.70 | 0.07 | 5 | 11.0% | 0.25 | 0.79 | 13.2% | 11.4% | -0.7% | 14.1%/10.4% | 5.4 (interpolated) | pass | 0.057 (unverified) | 0.07 |
| 64 | `cfg_e58c` | timeframe=5min, rsi_lookback=14, pivot_left=3, pivot_right=1, max_pivot_gap=8, min_rsi_diff=0.0, stop_atr=2.5, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.25 | 91/31/83 | 205 | 30.8% | 5.5% | 0.96 | -6.5% | 448 | 1.56 | 6.4% | 82.9 | 12/12 | 0.92 | 0.69 | 0.26 | 4 | 12.6% | 0.59 | 0.44 | 28.0% | 25.2% | 18.2% | 28.1%/22.4% | 7.2 (interpolated) | pass | 0.159 (unverified) | 0.14 |
| 65 | `cfg_6065` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=5.0, stop_atr=2.5, target_r=1.5, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 121/104/57 | 282 | 22.6% | 4.2% | 0.94 | -6.8% | 527 | 1.34 | 6.9% | 113.3 | 14/14 | 0.86 | 0.69 | 0.25 | 4 | 9.1% | 0.53 | 0.38 | 19.3% | 16.1% | 12.4% | 19.9%/15.3% | 4.8 (interpolated) | pass | 0.169 (unverified) | -0.58 |
| 66 | `cfg_827b` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=3.0, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.1 | 272/123/60 | 455 | 27.2% | 4.9% | 0.89 | -7.6% | 517 | 1.30 | 8.5% | 182.7 | 16/16 | 1.00 | 0.69 | 0.20 | 4 | 10.4% | 0.59 | 0.55 | 21.5% | 16.0% | 18.0% | 23.3%/17.9% | 3.6 (interpolated) | pass | 0.123 (unverified) | -0.27 |
| 67 | `cfg_1fcf` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=24, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.5 | 116/33/103 | 252 | 18.3% | 3.4% | 0.84 | -4.4% | 317 | 1.35 | 4.2% | 100.9 | 15/15 | 1.00 | 0.69 | 0.15 | 4 | 10.4% | 0.39 | 0.60 | 15.1% | 12.0% | 9.6% | 17.1%/12.5% | 4.1 (interpolated) | pass | 0.101 (unverified) | -0.14 |
| 68 | `cfg_5aff` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 199/90/46 | 335 | 21.7% | 4.0% | 0.88 | -6.5% | 255 | 1.32 | 6.5% | 134.4 | 15/15 | 1.00 | 0.68 | 0.19 | 4 | 9.2% | 0.56 | 0.53 | 17.6% | 13.7% | 26.4% | 19.5%/15.5% | 3.9 (interpolated) | pass | 0.132 (unverified) | -0.49 |
| 69 | `cfg_faf2` | timeframe=15min, rsi_lookback=14, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=2.0, max_hold=24, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.25 | 83/57/12 | 152 | 23.7% | 4.3% | 0.79 | -5.3% | 400 | 1.41 | 4.8% | 61.5 | 15/15 | 0.93 | 0.67 | 0.12 | 4 | 5.6% | 0.73 | 0.71 | 21.9% | 20.1% | 18.6% | 21.6%/16.4% | 8.2 (interpolated) | pass | 0.089 (unverified) | 0.22 |
| 70 | `cfg_3cff` | timeframe=5min, rsi_lookback=14, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=2.0, max_hold=24, rsi_extreme=40/60, adx_filter=lt30, min_price_div_atr=0.0 | 83/59/30 | 172 | 14.3% | 2.7% | 0.89 | -2.0% | 318 | 1.55 | 1.9% | 69.0 | 16/16 | 0.88 | 0.66 | 0.23 | 5 | 6.9% | 0.50 | 0.69 | 12.4% | 10.6% | 5.3% | 12.9%/9.5% | 5.0 (interpolated) | pass | 0.143 (unverified) | -0.05 |
| 71 | `cfg_4134` | timeframe=5min, rsi_lookback=7, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=3.0, max_hold=24, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.0 | 166/55/79 | 300 | 21.1% | 3.9% | 0.82 | -6.1% | 265 | 1.38 | 4.0% | 120.8 | 13/13 | 1.00 | 0.66 | 0.16 | 4 | 6.9% | 0.63 | 0.76 | 17.3% | 13.6% | 1.5% | 19.3%/14.8% | 4.0 (interpolated) | pass | 0.102 (unverified) | 0.66 |
| 72 | `cfg_08e2` | timeframe=5min, rsi_lookback=7, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=2.0, target_r=1.5, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.0 | 150/144/17 | 311 | 18.2% | 3.4% | 0.79 | -5.3% | 521 | 1.29 | 5.0% | 125.1 | 15/15 | 1.00 | 0.65 | 0.14 | 4 | 8.7% | 0.47 | 0.62 | 14.9% | 11.7% | 5.6% | 16.6%/11.8% | 3.9 (interpolated) | pass | 0.092 (unverified) | -0.07 |
| 73 | `cfg_d0ec` | timeframe=15min, rsi_lookback=7, pivot_left=8, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.5, target_r=2.0, max_hold=24, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.25 | 62/30/65 | 157 | 34.1% | 6.1% | 0.75 | -10.6% | 164 | 1.40 | 8.0% | 63.3 | 14/14 | 0.93 | 0.65 | 0.11 | 5 | 22.1% | 0.35 | 0.78 | 31.9% | 29.8% | 21.8% | 31.5%/22.4% | 9.9 (interpolated) | pass | 0.104 (unverified) | 0.62 |
| 74 | `cfg_b816` | timeframe=5min, rsi_lookback=14, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=24, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 97/29/82 | 208 | 18.8% | 3.5% | 0.84 | -4.4% | 384 | 1.42 | 3.4% | 83.8 | 15/15 | 1.00 | 0.64 | 0.20 | 4 | 9.0% | 0.48 | 0.68 | 16.1% | 13.6% | 14.6% | 17.6%/12.9% | 4.9 (interpolated) | pass | 0.095 (unverified) | 0.24 |
| 75 | `cfg_7b54` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=5.0, stop_atr=2.5, target_r=2.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.25 | 112/58/80 | 250 | 21.4% | 4.0% | 0.89 | -7.0% | 527 | 1.36 | 7.2% | 100.5 | 15/15 | 0.87 | 0.64 | 0.25 | 3 | 4.3% | 0.74 | 0.48 | 18.3% | 15.3% | 14.9% | 18.9%/15.4% | 4.8 (interpolated) | pass | 0.139 (unverified) | -0.47 |
| 76 | `cfg_6cb1` | timeframe=5min, rsi_lookback=14, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.5, target_r=2.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 142/84/87 | 313 | 26.7% | 4.8% | 0.93 | -10.3% | 527 | 1.33 | 8.6% | 126.9 | 14/14 | 1.00 | 0.63 | 0.30 | 4 | 13.1% | 0.51 | 0.46 | 22.7% | 18.9% | 24.6% | 24.5%/20.1% | 4.8 (interpolated) | pass | 0.169 (unverified) | -0.36 |
| 77 | `cfg_d958` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.5, target_r=3.0, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.5 | 143/40/111 | 294 | 24.7% | 4.5% | 0.76 | -7.2% | 397 | 1.31 | 8.8% | 117.6 | 15/15 | 1.00 | 0.63 | 0.13 | 3 | 10.6% | 0.53 | 0.51 | 20.8% | 17.0% | 19.1% | 22.6%/15.5% | 4.5 (interpolated) | pass | 0.079 (unverified) | 0.03 |
| 78 | `cfg_9b46` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=3.0, max_hold=48, rsi_extreme=40/60, adx_filter=lt30, min_price_div_atr=0.1 | 127/60/28 | 215 | 15.9% | 3.0% | 0.76 | -4.4% | 445 | 1.41 | 3.7% | 86.1 | 17/17 | 0.94 | 0.62 | 0.13 | 4 | 10.5% | 0.33 | 0.75 | 13.4% | 11.0% | 1.1% | 13.9%/10.0% | 4.4 (interpolated) | pass | 0.060 (unverified) | 0.17 |
| 79 | `cfg_f5c2` | timeframe=15min, rsi_lookback=10, pivot_left=8, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.5, target_r=2.0, max_hold=24, rsi_extreme=off, adx_filter=off, min_price_div_atr=0.1 | 61/32/68 | 161 | 36.2% | 6.4% | 0.79 | -13.8% | 163 | 1.45 | 8.2% | 65.5 | 14/14 | 0.93 | 0.62 | 0.17 | 5 | 24.5% | 0.32 | 0.68 | 33.9% | 31.6% | 30.3% | 32.5%/24.4% | 10.1 (interpolated) | pass | 0.120 (unverified) | 0.58 |
| 80 | `cfg_606d` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=48, rsi_extreme=off, adx_filter=lt30, min_price_div_atr=0.5 | 88/37/42 | 167 | 16.5% | 3.1% | 0.89 | -4.0% | 273 | 1.45 | 4.1% | 67.2 | 15/15 | 0.93 | 0.61 | 0.28 | 3 | 8.1% | 0.51 | 0.59 | 14.5% | 12.5% | 10.9% | 14.9%/10.5% | 5.4 (interpolated) | pass | 0.124 (unverified) | 0.33 |
| 81 | `cfg_84bf` | timeframe=5min, rsi_lookback=14, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.5 | 182/62/83 | 327 | 24.1% | 4.4% | 0.77 | -8.4% | 469 | 1.30 | 8.1% | 131.1 | 14/14 | 1.00 | 0.61 | 0.16 | 3 | 6.0% | 0.75 | 0.55 | 19.9% | 15.9% | 10.6% | 21.6%/16.0% | 4.1 (interpolated) | pass | 0.080 (unverified) | -0.00 |
| 82 | `cfg_d497` | timeframe=15min, rsi_lookback=7, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=2.0, target_r=1.5, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.5 | 88/83/3 | 174 | 24.8% | 4.5% | 0.76 | -5.8% | 478 | 1.32 | 7.8% | 70.4 | 14/14 | 0.86 | 0.60 | 0.16 | 3 | -0.7% | 1.02 | 0.63 | 22.8% | 20.9% | 12.6% | 21.1%/13.6% | 7.9 (interpolated) | pass | 0.083 (unverified) | 0.17 |
| 83 | `cfg_50ea` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=5.0, stop_atr=1.5, target_r=3.0, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.0 | 205/75/48 | 328 | 20.6% | 3.8% | 0.75 | -10.8% | 529 | 1.31 | 6.2% | 131.2 | 14/14 | 0.86 | 0.59 | 0.16 | 3 | -0.9% | 0.97 | 0.73 | 16.5% | 12.7% | 12.6% | 20.2%/13.4% | 3.8 (interpolated) | pass | 0.095 (unverified) | -0.40 |
| 84 | `cfg_8ce9` | timeframe=5min, rsi_lookback=14, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=5.0, stop_atr=2.5, target_r=2.0, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.1 | 82/43/68 | 193 | 17.4% | 3.3% | 0.84 | -7.0% | 530 | 1.39 | 5.8% | 77.1 | 15/15 | 0.87 | 0.58 | 0.26 | 4 | 6.8% | 0.55 | 0.57 | 15.1% | 12.8% | 15.7% | 15.2%/11.7% | 5.0 (interpolated) | pass | 0.122 (unverified) | -0.34 |
| 85 | `cfg_bbc3` | timeframe=5min, rsi_lookback=14, pivot_left=3, pivot_right=1, max_pivot_gap=12, min_rsi_diff=0.0, stop_atr=1.5, target_r=3.0, max_hold=48, rsi_extreme=40/60, adx_filter=lt30, min_price_div_atr=0.25 | 104/45/20 | 169 | 18.0% | 3.4% | 0.76 | -6.0% | 588 | 1.55 | 2.9% | 67.7 | 15/15 | 0.93 | 0.58 | 0.18 | 4 | 7.1% | 0.60 | 0.87 | 16.0% | 14.0% | 4.0% | 17.2%/12.7% | 5.8 (interpolated) | pass | 0.039 (unverified) | -0.34 |
| 86 | `cfg_4c07` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=8, min_rsi_diff=0.0, stop_atr=2.0, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.1 | 86/35/43 | 164 | 17.3% | 3.3% | 0.75 | -4.8% | 217 | 1.44 | 4.0% | 65.8 | 15/15 | 0.93 | 0.56 | 0.19 | 5 | 10.7% | 0.35 | 0.81 | 15.4% | 13.4% | 6.9% | 15.7%/10.8% | 5.7 (interpolated) | pass | 0.061 (unverified) | 0.12 |
| 87 | `cfg_ab9a` | timeframe=5min, rsi_lookback=10, pivot_left=5, pivot_right=1, max_pivot_gap=24, min_rsi_diff=0.0, stop_atr=2.5, target_r=1.5, max_hold=48, rsi_extreme=30/70, adx_filter=lt30, min_price_div_atr=0.0 | 73/76/31 | 180 | 16.9% | 3.2% | 0.76 | -4.8% | 440 | 1.38 | 4.0% | 72.8 | 14/14 | 0.86 | 0.52 | 0.25 | 5 | 8.5% | 0.50 | 0.59 | 14.9% | 13.0% | 7.3% | 16.0%/10.8% | 5.6 (interpolated) | pass | 0.078 (unverified) | -0.24 |
| 88 | `cfg_73e5` | timeframe=5min, rsi_lookback=7, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=2.5, target_r=3.0, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.5 | 88/31/62 | 181 | 22.0% | 4.1% | 0.84 | -5.3% | 266 | 1.46 | 5.2% | 72.8 | 14/14 | 1.00 | 0.51 | 0.33 | 4 | 12.3% | 0.42 | 0.55 | 19.7% | 17.5% | 11.8% | 19.6%/15.9% | 6.2 (interpolated) | pass | 0.097 (unverified) | -0.04 |
| 89 | `cfg_5484` | timeframe=5min, rsi_lookback=7, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=1.5, target_r=2.0, max_hold=48, rsi_extreme=off, adx_filter=lt30, min_price_div_atr=0.0 | 85/61/5 | 151 | 11.8% | 2.3% | 0.77 | -3.4% | 543 | 1.51 | 1.9% | 60.5 | 15/15 | 0.87 | 0.50 | 0.27 | 4 | 6.7% | 0.43 | 0.81 | 10.2% | 8.6% | 2.8% | 10.5%/6.6% | 4.9 (interpolated) | pass | 0.078 (unverified) | 0.25 |
| 90 | `cfg_43ac` | timeframe=5min, rsi_lookback=7, pivot_left=5, pivot_right=1, max_pivot_gap=12, min_rsi_diff=5.0, stop_atr=2.5, target_r=1.5, max_hold=48, rsi_extreme=40/60, adx_filter=off, min_price_div_atr=0.0 | 138/125/44 | 307 | 25.4% | 4.6% | 0.87 | -9.4% | 392 | 1.35 | 6.7% | 123.7 | 14/14 | 1.00 | 0.50 | 0.37 | 4 | 14.2% | 0.42 | 0.58 | 21.8% | 18.3% | 4.4% | 23.5%/17.5% | 4.9 (interpolated) | pass | 0.118 (unverified) | -0.07 |
| 91 | `cfg_aadf` | timeframe=5min, rsi_lookback=7, pivot_left=3, pivot_right=1, max_pivot_gap=24, min_rsi_diff=5.0, stop_atr=2.0, target_r=3.0, max_hold=48, rsi_extreme=30/70, adx_filter=off, min_price_div_atr=0.5 | 150/51/55 | 256 | 22.4% | 4.1% | 0.78 | -7.8% | 349 | 1.36 | 5.9% | 102.7 | 12/12 | 0.92 | 0.40 | 0.38 | 4 | 9.4% | 0.58 | 0.60 | 19.1% | 16.0% | 7.9% | 18.9%/13.7% | 4.8 (interpolated) | pass | 0.084 (unverified) | 0.27 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 0.3% / 0.13 / 34 | 0.1% / 0.04 / 44 | 14.2% / 2.60 / 24 | 5.3% / 2.30 / 43 | 3.2% / 0.90 / 45 |
| 2 | 3.3% / 1.05 / 33 | 0.3% / 0.12 / 40 | 13.7% / 2.53 / 22 | 7.6% / 2.54 / 38 | 2.0% / 0.46 / 42 |
| 3 | -3.1% / -1.21 / 37 | 1.7% / 0.68 / 40 | 10.1% / 1.42 / 39 | 4.9% / 1.63 / 47 | 12.5% / 2.44 / 58 |
| 4 | 0.0% / 0.04 / 43 | 9.5% / 2.38 / 36 | 25.7% / 2.59 / 31 | 1.6% / 0.51 / 27 | 5.0% / 0.64 / 58 |
| 5 | 0.4% / 0.17 / 33 | -0.1% / -0.04 / 41 | 11.0% / 2.53 / 22 | 4.9% / 2.13 / 38 | 3.4% / 0.97 / 42 |
| 6 | -3.3% / -1.56 / 30 | 1.4% / 0.44 / 35 | 11.9% / 1.61 / 35 | 4.2% / 1.39 / 41 | 15.8% / 2.44 / 46 |
| 7 | 1.1% / 0.36 / 30 | 2.1% / 0.67 / 35 | 12.5% / 2.47 / 20 | 8.6% / 2.75 / 35 | -1.8% / -0.38 / 40 |
| 8 | 1.2% / 0.22 / 39 | 7.4% / 2.00 / 24 | 17.5% / 1.85 / 26 | -0.7% / -0.25 / 20 | 10.0% / 1.65 / 42 |
| 9 | 2.8% / 0.89 / 30 | 1.5% / 0.59 / 35 | 9.5% / 2.42 / 20 | 6.8% / 2.44 / 35 | 0.4% / 0.12 / 40 |
| 10 | -5.3% / -2.90 / 37 | 2.5% / 0.96 / 40 | 11.1% / 1.47 / 39 | 5.3% / 1.88 / 48 | 9.8% / 1.95 / 58 |
| 11 | -3.6% / -1.93 / 37 | 1.7% / 0.86 / 40 | 9.1% / 1.65 / 40 | 2.8% / 1.23 / 48 | 9.4% / 2.37 / 58 |
| 12 | -2.0% / -1.00 / 30 | 2.3% / 0.96 / 35 | 13.4% / 1.77 / 35 | 0.7% / 0.33 / 41 | 12.0% / 2.36 / 46 |
| 13 | -0.0% / 0.00 / 30 | 1.0% / 0.47 / 36 | 7.7% / 2.41 / 20 | 4.7% / 2.20 / 35 | 2.7% / 0.85 / 40 |
| 14 | -1.0% / -0.20 / 53 | 1.9% / 0.68 / 40 | 11.4% / 1.55 / 44 | 7.4% / 1.93 / 59 | 11.9% / 1.49 / 77 |
| 15 | -1.7% / -0.36 / 39 | 2.9% / 1.01 / 30 | 27.6% / 2.71 / 32 | 0.6% / 0.30 / 22 | 3.8% / 0.57 / 49 |
| 16 | 3.6% / 0.56 / 39 | 8.6% / 2.08 / 24 | 15.1% / 1.52 / 26 | 1.1% / 0.36 / 20 | 8.7% / 1.12 / 41 |
| 17 | 2.2% / 0.35 / 42 | 13.2% / 2.32 / 33 | 20.3% / 1.88 / 31 | 3.0% / 0.81 / 27 | 1.4% / 0.20 / 56 |
| 18 | -0.3% / -0.06 / 30 | 0.6% / 0.23 / 36 | 9.8% / 2.22 / 20 | 6.5% / 2.57 / 35 | 2.3% / 0.59 / 40 |
| 19 | -4.0% / -0.88 / 54 | 1.9% / 0.70 / 40 | 7.9% / 1.21 / 43 | 7.4% / 2.04 / 61 | 14.5% / 1.63 / 78 |
| 20 | -5.6% / -3.06 / 39 | 2.6% / 0.99 / 45 | 13.2% / 1.46 / 43 | 5.4% / 1.83 / 57 | 10.0% / 1.91 / 63 |
| 21 | -1.8% / -0.99 / 24 | 2.0% / 0.69 / 32 | 8.4% / 1.68 / 28 | 4.5% / 1.65 / 36 | 7.6% / 1.83 / 34 |
| 22 | -6.4% / -2.15 / 34 | 4.6% / 1.46 / 43 | 10.3% / 2.15 / 35 | 7.6% / 2.51 / 42 | 4.2% / 0.92 / 40 |
| 23 | 0.8% / 0.22 / 30 | 1.9% / 0.59 / 35 | 11.1% / 2.54 / 20 | 7.6% / 2.46 / 35 | 1.5% / 0.33 / 39 |
| 24 | -1.4% / -0.95 / 23 | 0.9% / 0.60 / 28 | 7.3% / 1.20 / 35 | 1.3% / 0.74 / 38 | 10.6% / 2.91 / 44 |
| 25 | -2.9% / -0.66 / 78 | 2.1% / 0.66 / 66 | 11.8% / 1.67 / 51 | 11.9% / 3.26 / 72 | 3.8% / 0.65 / 83 |
| 26 | -3.4% / -0.80 / 39 | 3.8% / 1.35 / 37 | 9.8% / 1.57 / 29 | 8.7% / 2.68 / 49 | 11.2% / 1.56 / 54 |
| 27 | -4.0% / -2.29 / 37 | 0.4% / 0.24 / 40 | 12.5% / 2.82 / 40 | 0.7% / 0.37 / 48 | 4.8% / 1.46 / 58 |
| 28 | -1.9% / -0.51 / 34 | -0.2% / -0.05 / 30 | 21.0% / 2.87 / 23 | 4.1% / 1.72 / 28 | 0.6% / 0.13 / 44 |
| 29 | 0.1% / 0.05 / 30 | 2.4% / 0.87 / 35 | 13.6% / 2.43 / 20 | 1.9% / 0.91 / 35 | 1.1% / 0.28 / 40 |
| 30 | -3.3% / -0.61 / 53 | 2.9% / 0.91 / 40 | 8.5% / 1.21 / 43 | 7.9% / 1.96 / 59 | 17.1% / 1.66 / 77 |
| 31 | -2.8% / -1.54 / 24 | 2.6% / 0.77 / 32 | 7.3% / 1.54 / 28 | 2.9% / 1.09 / 36 | 10.7% / 2.07 / 34 |
| 32 | 5.1% / 0.95 / 35 | 8.2% / 1.87 / 28 | 21.7% / 2.35 / 25 | 0.2% / 0.06 / 22 | -5.5% / -0.78 / 53 |
| 33 | -2.7% / -0.57 / 54 | 5.1% / 1.46 / 47 | 7.0% / 1.16 / 42 | 9.6% / 2.62 / 50 | 11.3% / 1.57 / 58 |
| 34 | 3.5% / 0.51 / 47 | 11.5% / 2.41 / 38 | 16.3% / 1.55 / 34 | 3.3% / 0.90 / 30 | -0.7% / -0.02 / 64 |
| 35 | -0.3% / -0.08 / 30 | 1.1% / 0.48 / 35 | 10.5% / 2.62 / 20 | 2.6% / 1.14 / 35 | 0.8% / 0.23 / 40 |
| 36 | -5.4% / -1.64 / 59 | 2.9% / 1.19 / 45 | 5.4% / 0.89 / 52 | 7.2% / 2.05 / 70 | 13.0% / 1.86 / 90 |
| 37 | -3.4% / -0.77 / 56 | 2.5% / 1.00 / 43 | 7.6% / 1.18 / 49 | 7.5% / 2.15 / 64 | 10.3% / 1.42 / 86 |
| 38 | -3.1% / -1.15 / 52 | 1.1% / 0.45 / 68 | 10.0% / 1.63 / 50 | 7.6% / 2.60 / 70 | 5.2% / 1.12 / 77 |
| 39 | 0.5% / 0.12 / 38 | 7.1% / 1.84 / 29 | 22.5% / 1.67 / 30 | 0.6% / 0.21 / 21 | 5.4% / 0.60 / 47 |
| 40 | -5.1% / -0.98 / 48 | 1.0% / 0.38 / 39 | 5.1% / 0.83 / 37 | 8.7% / 2.31 / 59 | 12.4% / 1.49 / 63 |
| 41 | -5.6% / -2.50 / 37 | 0.8% / 0.38 / 40 | 9.7% / 1.66 / 40 | 2.4% / 1.04 / 48 | 9.3% / 2.21 / 58 |
| 42 | -1.4% / -0.96 / 23 | 1.3% / 0.65 / 28 | 9.1% / 1.10 / 34 | 2.7% / 1.25 / 38 | 6.6% / 1.55 / 44 |
| 43 | -4.6% / -1.05 / 52 | 3.4% / 1.28 / 35 | 6.1% / 1.06 / 38 | 7.3% / 2.03 / 60 | 12.3% / 1.53 / 67 |
| 44 | 1.8% / 0.30 / 44 | 10.8% / 2.68 / 31 | 16.5% / 1.58 / 33 | 1.8% / 0.54 / 28 | 2.7% / 0.34 / 56 |
| 45 | -2.5% / -0.62 / 44 | 4.6% / 1.40 / 44 | 0.3% / 0.09 / 41 | 7.1% / 2.12 / 54 | 15.7% / 2.12 / 55 |
| 46 | -5.1% / -1.21 / 62 | 3.1% / 0.92 / 71 | 21.3% / 2.78 / 47 | 11.5% / 3.27 / 64 | 2.1% / 0.36 / 78 |
| 47 | -3.0% / -1.01 / 41 | 0.2% / 0.08 / 40 | 9.9% / 1.53 / 31 | 8.0% / 2.62 / 53 | 3.8% / 0.74 / 56 |
| 48 | -3.5% / -1.49 / 41 | 1.0% / 0.30 / 44 | 5.4% / 0.68 / 43 | 5.8% / 1.76 / 53 | 16.4% / 2.29 / 65 |
| 49 | -0.3% / -0.01 / 38 | 5.5% / 1.51 / 29 | 17.2% / 1.66 / 30 | 1.9% / 0.71 / 21 | 3.7% / 0.45 / 48 |
| 50 | 0.7% / 0.21 / 27 | 1.9% / 0.81 / 27 | 2.1% / 0.51 / 25 | 5.5% / 1.99 / 38 | 7.6% / 1.27 / 40 |
| 51 | -2.6% / -1.59 / 24 | 0.3% / 0.20 / 27 | 5.1% / 1.57 / 30 | 1.8% / 1.02 / 33 | 7.0% / 2.18 / 38 |
| 52 | -4.2% / -0.90 / 40 | 3.8% / 1.15 / 29 | 22.8% / 2.35 / 31 | 0.4% / 0.16 / 25 | 1.9% / 0.28 / 48 |
| 53 | -4.4% / -0.88 / 72 | 6.0% / 1.55 / 60 | 13.3% / 1.80 / 47 | 13.7% / 3.24 / 65 | 6.3% / 0.84 / 79 |
| 54 | 3.8% / 0.55 / 47 | 11.4% / 2.30 / 38 | 19.2% / 1.42 / 34 | 0.5% / 0.13 / 30 | 3.3% / 0.36 / 63 |
| 55 | -5.4% / -0.92 / 45 | 1.5% / 0.42 / 33 | 29.3% / 2.85 / 28 | 4.0% / 1.02 / 36 | 2.8% / 0.36 / 69 |
| 56 | -7.7% / -1.28 / 77 | 3.7% / 0.99 / 65 | 7.1% / 0.89 / 63 | 13.3% / 2.88 / 73 | 11.2% / 1.23 / 84 |
| 57 | 4.6% / 0.65 / 45 | 10.9% / 1.87 / 35 | 25.1% / 1.80 / 34 | -0.7% / -0.15 / 30 | 4.0% / 0.41 / 61 |
| 58 | -0.7% / -0.16 / 39 | 0.6% / 0.25 / 38 | 7.5% / 1.31 / 30 | 7.1% / 2.25 / 51 | 5.0% / 0.95 / 54 |
| 59 | -4.2% / -0.96 / 53 | 4.1% / 1.72 / 40 | 3.3% / 0.62 / 43 | 5.1% / 1.61 / 59 | 11.8% / 1.57 / 77 |
| 60 | -2.3% / -0.50 / 46 | 0.1% / 0.05 / 34 | 21.4% / 2.54 / 29 | 0.9% / 0.33 / 36 | 3.5% / 0.52 / 71 |
| 61 | -4.4% / -1.05 / 35 | 3.7% / 1.19 / 29 | 27.3% / 2.59 / 31 | -1.4% / -0.80 / 20 | 3.5% / 0.57 / 48 |
| 62 | -4.6% / -0.93 / 98 | 2.6% / 0.77 / 91 | 12.2% / 1.32 / 81 | 15.4% / 3.55 / 106 | 3.7% / 0.56 / 109 |
| 63 | 2.8% / 0.79 / 33 | 2.6% / 1.20 / 26 | 3.6% / 0.69 / 19 | 2.0% / 1.01 / 33 | 3.2% / 0.73 / 44 |
| 64 | -2.7% / -0.59 / 44 | 5.5% / 1.82 / 26 | 6.2% / 0.95 / 30 | 3.3% / 0.95 / 43 | 16.2% / 1.68 / 62 |
| 65 | -6.2% / -1.51 / 54 | 2.6% / 0.81 / 61 | 12.3% / 2.44 / 42 | 9.6% / 2.90 / 55 | 3.5% / 0.61 / 70 |
| 66 | -5.1% / -1.02 / 94 | 3.3% / 0.96 / 86 | 6.9% / 0.91 / 75 | 15.2% / 3.73 / 97 | 5.3% / 0.80 / 103 |
| 67 | -4.0% / -1.03 / 55 | 4.6% / 1.53 / 47 | 7.1% / 1.37 / 42 | 4.5% / 1.67 / 50 | 5.3% / 1.00 / 58 |
| 68 | -3.5% / -0.81 / 75 | 2.7% / 0.82 / 62 | 6.4% / 1.18 / 48 | 11.5% / 3.26 / 69 | 3.5% / 0.61 / 81 |
| 69 | -1.7% / -0.40 / 35 | 3.6% / 1.20 / 23 | 17.1% / 1.79 / 22 | 0.3% / 0.12 / 24 | 3.5% / 0.58 / 48 |
| 70 | 1.5% / 0.58 / 36 | 1.1% / 0.75 / 30 | 6.9% / 1.45 / 22 | 0.1% / 0.06 / 34 | 4.1% / 1.12 / 50 |
| 71 | -1.7% / -0.57 / 50 | 0.8% / 0.28 / 63 | 13.3% / 1.59 / 47 | 5.2% / 1.90 / 66 | 2.5% / 0.52 / 74 |
| 72 | -3.9% / -1.22 / 51 | 2.5% / 0.97 / 66 | 8.8% / 1.37 / 50 | 6.5% / 2.08 / 69 | 3.7% / 0.70 / 75 |
| 73 | 8.8% / 1.38 / 35 | 10.8% / 1.94 / 27 | 9.8% / 0.78 / 25 | 1.2% / 0.26 / 22 | 0.2% / 0.06 / 48 |
| 74 | -3.0% / -0.75 / 39 | 3.2% / 1.24 / 37 | 9.0% / 1.54 / 29 | 2.7% / 1.13 / 49 | 6.0% / 1.11 / 54 |
| 75 | -6.5% / -2.00 / 42 | 2.6% / 0.74 / 55 | 16.4% / 2.75 / 42 | 9.7% / 2.87 / 50 | -0.9% / -0.13 / 61 |
| 76 | -9.6% / -1.91 / 62 | 1.9% / 0.57 / 54 | 9.0% / 1.36 / 45 | 12.6% / 3.30 / 70 | 12.0% / 1.78 / 82 |
| 77 | -1.9% / -0.34 / 61 | 6.4% / 1.61 / 54 | -2.0% / -0.25 / 54 | 12.8% / 2.92 / 61 | 8.1% / 0.95 / 64 |
| 78 | 2.6% / 0.71 / 43 | 4.5% / 1.83 / 41 | -0.0% / 0.03 / 32 | 4.9% / 1.86 / 46 | 3.0% / 0.67 / 53 |
| 79 | 5.2% / 0.87 / 36 | 8.5% / 1.69 / 26 | 4.9% / 0.42 / 25 | 4.0% / 0.81 / 23 | 9.4% / 1.03 / 51 |
| 80 | -1.4% / -0.64 / 31 | 5.8% / 1.92 / 26 | -0.0% / 0.01 / 33 | 3.6% / 1.27 / 33 | 7.8% / 1.51 / 44 |
| 81 | -0.9% / -0.14 / 64 | 4.7% / 1.33 / 49 | -2.9% / -0.43 / 58 | 5.2% / 1.39 / 72 | 17.1% / 1.87 / 84 |
| 82 | -4.4% / -0.86 / 38 | 3.6% / 0.97 / 32 | 25.7% / 2.92 / 26 | 4.6% / 1.15 / 31 | -4.1% / -0.49 / 47 |
| 83 | -6.3% / -1.46 / 63 | -1.8% / -0.54 / 75 | 21.6% / 2.53 / 47 | 6.4% / 2.06 / 64 | 1.3% / 0.26 / 79 |
| 84 | -4.8% / -1.28 / 37 | 1.8% / 0.60 / 41 | 9.9% / 1.87 / 36 | 6.3% / 2.50 / 39 | 3.8% / 0.85 / 40 |
| 85 | 0.7% / 0.27 / 31 | 2.2% / 1.04 / 24 | 5.9% / 0.75 / 31 | -1.7% / -0.87 / 35 | 10.1% / 2.28 / 48 |
| 86 | 0.2% / 0.07 / 35 | 1.5% / 0.78 / 28 | 6.0% / 1.01 / 24 | 5.5% / 1.79 / 41 | 3.1% / 0.56 / 36 |
| 87 | 0.1% / 0.05 / 35 | 3.2% / 1.33 / 34 | 2.5% / 0.47 / 21 | 2.5% / 1.09 / 31 | 7.7% / 1.28 / 59 |
| 88 | -0.6% / -0.14 / 27 | 5.2% / 1.57 / 37 | 1.9% / 0.38 / 34 | 8.7% / 2.43 / 41 | 5.4% / 0.73 / 42 |
| 89 | -0.1% / -0.06 / 27 | 1.9% / 1.14 / 36 | 3.1% / 0.67 / 17 | 1.7% / 1.05 / 30 | 4.8% / 1.43 / 41 |
| 90 | -1.7% / -0.44 / 51 | 2.3% / 0.76 / 65 | 7.1% / 0.88 / 48 | 9.8% / 2.69 / 68 | 6.1% / 0.93 / 75 |
| 91 | -3.3% / -0.74 / 43 | 6.6% / 1.82 / 47 | 1.3% / 0.22 / 54 | 4.8% / 1.34 / 55 | 11.8% / 1.69 / 57 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_1c68` | 13 | 0.83 | 0.73/0.84 | 0.51/0.54 |
| 1 | `cfg_82fa` | 21 | 0.82 | 0.74/0.90 | 0.49/0.67 |
| 2 | `cfg_a3ee` | 24 | 0.81 | 0.84/0.89 | 0.69/0.78 |
| 3 | `cfg_39dc` | 3 | 0.95 | 0.96/0.98 | 0.70/0.84 |
| 4 | `cfg_4aef` | 31 | 0.82 | 0.73/0.85 | 0.38/0.65 |
| 5 | `cfg_a1c3` | 15 | 0.81 | 0.73/0.82 | 0.35/0.43 |
| 6 | `cfg_3cff` | 3 | 0.84 | 0.90/0.92 | 0.40/0.57 |
| 7 | `cfg_23e8` | 6 | 0.87 | 0.89/0.90 | 0.75/0.82 |
| 8 | `cfg_bcc3` | 6 | 0.85 | 0.92/0.93 | 0.77/0.82 |
| 9 | `cfg_b271` | 21 | 0.84 | 0.86/0.90 | 0.68/0.76 |
| 10 | `cfg_0422` | 8 | 0.88 | 0.88/0.91 | 0.67/0.80 |
| 11 | `cfg_2ad3` | 13 | 0.84 | 0.83/0.89 | 0.61/0.74 |
| 12 | `cfg_e58c` | 5 | 0.82 | 0.85/0.89 | 0.65/0.80 |
| 13 | `cfg_6e15` | 35 | 0.82 | 0.71/0.81 | 0.46/0.64 |
| 14 | `cfg_171c` | 6 | 0.87 | 0.86/0.94 | 0.73/0.81 |
| 15 | `cfg_cec0` | 16 | 0.82 | 0.60/0.82 | 0.55/0.64 |
| 16 | `cfg_4134` | 8 | 0.86 | 0.83/0.91 | 0.62/0.63 |
| 17 | `cfg_982c` | 4 | 0.85 | 0.83/0.85 | 0.50/0.57 |
| 18 | `cfg_08e2` | 6 | 0.86 | 0.80/0.87 | 0.59/0.61 |
| 19 | `cfg_e994` | 3 | 0.85 | 0.85/0.88 | 0.73/0.76 |
| 20 | `cfg_4f07` | 10 | 0.86 | 0.82/0.89 | 0.75/0.84 |
| 21 | `cfg_5959` | 6 | 0.83 | 0.86/0.94 | 0.62/0.84 |
| 22 | `cfg_7b54` | 5 | 0.83 | 0.84/0.87 | 0.67/0.74 |
| 23 | `cfg_835a` | 8 | 0.86 | 0.87/0.89 | 0.62/0.72 |
| 24 | `cfg_1f0e` | 18 | 0.87 | 0.78/0.86 | 0.53/0.72 |
| 25 | `cfg_24f0` | 8 | 0.81 | 0.89/0.92 | 0.56/0.84 |
| 26 | `cfg_3280` | 7 | 0.81 | 0.71/0.83 | 0.46/0.54 |
| 27 | `cfg_abb2` | 12 | 0.80 | 0.78/0.88 | 0.45/0.71 |
| 28 | `cfg_1108` | 8 | 0.94 | 0.96/0.97 | 0.80/0.84 |
| 29 | `cfg_71cf` | 9 | 0.87 | 0.91/0.95 | 0.85/0.89 |
| 30 | `cfg_2542` | 4 | 0.92 | 0.93/0.94 | 0.87/0.89 |
| 31 | `cfg_827b` | 4 | 0.86 | 0.81/0.88 | 0.68/0.71 |
| 32 | `cfg_43ac` | 4 | 0.90 | 0.92/0.98 | 0.92/0.95 |
| 33 | `cfg_aadf` | 3 | 1.00 | 1.00/1.00 | 0.96/0.97 |
| 34 | `cfg_190a` | 5 | 0.82 | 0.75/0.79 | 0.35/0.52 |
| 35 | `cfg_ae5b` | 14 | 0.87 | 0.59/0.78 | 0.39/0.59 |
| 36 | `cfg_4104` | 22 | 0.88 | 0.85/0.94 | 0.57/0.81 |
| 37 | `cfg_faf2` | 4 | 0.84 | 0.84/0.86 | 0.66/0.73 |
| 38 | `cfg_8ce9` | 4 | 0.93 | 0.79/0.79 | 0.60/0.65 |
| 39 | `cfg_1fcf` | 4 | 0.85 | 0.83/0.85 | 0.75/0.78 |
| 40 | `cfg_7af9` | 6 | 0.87 | 0.83/0.86 | 0.67/0.78 |
| 41 | `cfg_1fb9` | 8 | 0.85 | 0.84/0.90 | 0.60/0.78 |
| 42 | `cfg_ab93` | 7 | 0.82 | 0.88/0.91 | 0.60/0.75 |
| 43 | `cfg_4c9d` | 6 | 0.87 | 0.91/0.94 | 0.77/0.85 |
| 44 | `cfg_606d` | 4 | 0.93 | 0.91/0.92 | 0.84/0.87 |
| 45 | `cfg_84bf` | 3 | 0.96 | 0.96/0.96 | 0.87/0.90 |
| 46 | `cfg_a8ed` | 21 | 0.88 | 0.73/0.92 | 0.47/0.72 |
| 47 | `cfg_9561` | 3 | 0.96 | 0.98/0.98 | 0.94/0.95 |
| 48 | `cfg_3ade` | 10 | 0.85 | 0.86/0.92 | 0.70/0.82 |
| 49 | `cfg_9579` | 9 | 0.83 | 0.85/0.92 | 0.65/0.77 |
| 50 | `cfg_db0e` | 12 | 0.84 | 0.91/0.95 | 0.47/0.83 |
| 51 | `cfg_2720` | 4 | 0.84 | 0.90/0.94 | 0.75/0.82 |
| 52 | `cfg_2765` | 8 | 0.80 | 0.77/0.92 | 0.62/0.79 |
| 53 | `cfg_2854` | 2 | 0.95 | 0.92/0.92 | 0.61/0.61 |
| 54 | `cfg_bcc8` | 12 | 0.84 | 0.86/0.92 | 0.68/0.81 |
| 55 | `cfg_c815` | 8 | 0.82 | 0.83/0.90 | 0.53/0.77 |
| 56 | `cfg_73e5` | 6 | 0.87 | 0.89/0.89 | 0.69/0.72 |
| 57 | `cfg_8b94` | 5 | 0.96 | 0.93/0.93 | 0.86/0.90 |
| 58 | `cfg_d0ec` | 5 | 0.89 | 0.94/0.98 | 0.87/0.94 |
| 59 | `cfg_4e6e` | 9 | 0.81 | 0.74/0.84 | 0.41/0.66 |
| 60 | `cfg_8e6c` | 5 | 0.85 | 0.89/0.95 | 0.79/0.86 |
| 61 | `cfg_6065` | 6 | 0.85 | 0.77/0.81 | 0.62/0.68 |
| 62 | `cfg_9332` | 2 | 0.94 | 0.94/0.94 | 0.75/0.75 |
| 63 | `cfg_7a34` | 8 | 0.84 | 0.76/0.85 | 0.50/0.81 |
| 64 | `cfg_fdbc` | 2 | 0.94 | 0.95/0.95 | 0.91/0.91 |
| 65 | `cfg_ef0a` | 9 | 0.84 | 0.79/0.88 | 0.55/0.68 |
| 66 | `cfg_d6ff` | 4 | 0.92 | 0.93/0.93 | 0.81/0.83 |
| 67 | `cfg_b18f` | 7 | 0.83 | 0.91/0.93 | 0.74/0.83 |
| 68 | `cfg_4c07` | 1 | n/a | n/a/n/a | n/a/n/a |
| 69 | `cfg_99e1` | 2 | 0.95 | 0.90/0.90 | 0.76/0.76 |
| 70 | `cfg_50ea` | 1 | n/a | n/a/n/a | n/a/n/a |
| 71 | `cfg_8bc2` | 5 | 0.91 | 0.88/0.93 | 0.78/0.79 |
| 72 | `cfg_5484` | 1 | n/a | n/a/n/a | n/a/n/a |
| 73 | `cfg_6cb1` | 4 | 0.90 | 0.90/0.92 | 0.75/0.81 |
| 74 | `cfg_5608` | 2 | 0.96 | 0.93/0.93 | 0.74/0.74 |
| 75 | `cfg_5aff` | 2 | 0.93 | 0.92/0.92 | 0.68/0.68 |
| 76 | `cfg_9f8d` | 2 | 0.91 | 0.89/0.89 | 0.69/0.69 |
| 77 | `cfg_ea05` | 9 | 0.81 | 0.79/0.81 | 0.50/0.62 |
| 78 | `cfg_8dc3` | 4 | 0.88 | 0.89/0.93 | 0.76/0.83 |
| 79 | `cfg_eb36` | 2 | 0.91 | 0.92/0.92 | 0.78/0.78 |
| 80 | `cfg_d497` | 2 | 1.00 | 1.00/1.00 | 0.94/0.94 |
| 81 | `cfg_8f06` | 4 | 0.88 | 0.93/0.94 | 0.74/0.75 |
| 82 | `cfg_eb69` | 5 | 0.91 | 0.92/0.95 | 0.86/0.89 |
| 83 | `cfg_f5c2` | 4 | 0.98 | 0.99/0.99 | 0.96/0.96 |
| 84 | `cfg_9b46` | 1 | n/a | n/a/n/a | n/a/n/a |
| 85 | `cfg_d958` | 2 | 0.86 | 0.63/0.63 | 0.59/0.59 |
| 86 | `cfg_ab9a` | 1 | n/a | n/a/n/a | n/a/n/a |
| 87 | `cfg_b0bc` | 2 | 0.92 | 0.95/0.95 | 0.91/0.91 |
| 88 | `cfg_b816` | 1 | n/a | n/a/n/a | n/a/n/a |
| 89 | `cfg_bbc3` | 1 | n/a | n/a/n/a | n/a/n/a |
| 90 | `cfg_d95a` | 3 | 0.87 | 0.92/0.92 | 0.74/0.86 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 7.022e-04 over 62136 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1011.0, participation ratio 26.4, 95%-variance components 169 (rank bound T = 1259); raw grid 69984; raw + known prior 511752
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
- Neighbor lattice: v1 orders every axis (timeframe, RSI period, pivot left/right, max pivot gap, min RSI diff, stop ATR, target R, max hold; only symbol fixed); v2 also orders rsi_extreme (off < 40/60 < 30/70), adx_filter (off < 30 < 20) and min_price_div_atr, and holds pivot_right (single value) fixed.
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
- v2 filters (off = v1 rule): rsi_extreme requires the FIRST pivot's RSI_q <= 40 / 30 (long-only, so only the bullish lower threshold applies); adx_filter requires Wilder ADX(14) at the confirmation close c < 30 / < 20 (TradingView ta.dmi convention; NaN during warm-up rejects the signal); min_price_div_atr requires low_q - low_p >= k x ATR(14) at the second pivot p (known at c >= p; k = 0 keeps the strict lower low).
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Unresolved assumptions

- Drawdown limit -30% is reused from the channel-breakout funnel (src/experiments/validation.py); that approval was given for 0.25%-risk stop-based sizing, while this strategy invests full equity per trade -- it has not been separately approved for this sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0: Sharpe vs. cash is overstated in high-rate years (2023-2024 ~5%).
- Variable cost stress scales per-share commission and slippage bps; the $1 per-order minimum commission is treated as fixed.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Prices are split-adjusted but NOT dividend-adjusted: SPY's ~1.5%/yr dividend is not credited while long, and an ex-dividend drop can create a spurious price lower low.
- Long-only regular bullish divergence; bearish / hidden divergences and short trades are not tested (the v2 RSI-extreme filter's upper threshold is therefore unused).
- Neighbor lattice: v1 orders every axis (only symbol fixed); v2 orders every axis except pivot_right (a single value, held fixed), with the filters ordered loosest to strictest: rsi_extreme off < 40/60 < 30/70, adx_filter off < 30 < 20, min_price_div_atr 0 < 0.1 < 0.25 < 0.5.
- All lookbacks, pivot widths, gaps and holding periods are counted in bars of the config's timeframe, not in trading days.
