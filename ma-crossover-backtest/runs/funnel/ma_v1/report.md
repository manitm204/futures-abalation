# Screening funnel -- ma_v1 (development stages only)

- Code: `43fc6aa6d0a5` (dirty working tree: False, diff sha256 `e3b0c44298fc`)
- Config: `/home/manit/Desktop/fun_projects/abalation_backtest/ma-crossover-backtest/configs/funnel/ma_funnel.yaml` sha256 `0bac2ecba8f40312`; seed 20261016
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'SPY': '2026-08-18', 'QQQ': '2026-08-18'}
- Frozen manifest sha256: `4477e02e3e209988` (141 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- The same SPY 2023-2024 slice gated the RSI-divergence funnels (rsi_v1: 33 frozen / 8 passed; rsi_v2: 91 / 35; rsi_v3: 172 / 51), the mean-reversion funnels, the channel-breakout funnels and the Donchian ablation. The MA crossover grid was specified before any MA-crossover result was seen.
- Holdout 2025+ previously inspected: **True** -- SPY 2025-2026 holdout metrics were computed and inspected for the Donchian ablation and the channel-breakout funnels (funnel_v1..v3 records.parquet). The holdout is NOT an untouched test of SPY.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 60000 | 60000 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 60000 | 60000 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 60000 | 38075 | 21925 | 0 |  | 36110 | 63.46 | 63.46 |  |
| 3 performance & risk | hard_gate | 38075 | 6965 | 31110 | 0 |  | 0 | 11.61 | 18.29 |  |
| 4 parameter stability | hard_gate | 6965 | 6965 | 0 | 0 |  | 6965 | 11.61 | 100.00 |  |
| 5 time stability | hard_gate | 6965 | 6965 | 0 | 0 |  | 6965 | 11.61 | 100.00 |  |
| 6 deduplication | dedup | 6965 | 141 |  |  | 6824 |  | 0.23 | 2.02 |  |
| 7 execution stress | hard_gate | 141 | 141 | 0 | 0 |  | 0 | 0.23 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 141 |  |  |  |  |  |  |  | diagnostic only: unverified: 141 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 21925 |
| s2:hard_reject:years_with_>=10_trades | 6710 |
| s3:hard_reject:max_drawdown | 2225 |
| s3:hard_reject:net_return | 7697 |
| s3:hard_reject:sharpe | 31110 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | stop/cross exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | QQQ dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_2c7e` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=100, confirm_bars=2, buffer_atr=0.2, stop_atr=None, slope_filter=False | 0/239 | 239 | 84.6% | 13.1% | 1.08 | -8.1% | 95 | 1.56 | 59.7% | 97.2 | 12/12 | 1.00 | 1.04 | 0.04 | 4 | 40.8% | 0.46 | 0.59 | 79.5% | 74.7% | 83.3% | 75.2%/59.1% | 12.3 (interpolated) | pass | 0.478 (unverified) | 0.97 |
| 2 | `cfg_4181` | timeframe=5min, ma_pair=EMA/SMA, fast_length=16, slow_length=150, confirm_bars=2, buffer_atr=0.1, stop_atr=2.0, slope_filter=True | 267/136 | 403 | 63.3% | 10.3% | 1.13 | -8.5% | 87 | 1.49 | 33.8% | 161.0 | 11/11 | 0.91 | 1.04 | 0.09 | 5 | 38.4% | 0.39 | 0.46 | 55.9% | 48.8% | 51.7% | 55.7%/44.0% | 6.3 (interpolated) | pass | 0.525 (unverified) | 1.04 |
| 3 | `cfg_668f` | timeframe=5min, ma_pair=EMA/EMA, fast_length=12, slow_length=150, confirm_bars=3, buffer_atr=0.5, stop_atr=None, slope_filter=True | 0/461 | 461 | 85.4% | 13.1% | 1.08 | -11.9% | 112 | 1.42 | 57.0% | 182.0 | 9/9 | 1.00 | 1.03 | 0.05 | 5 | 42.4% | 0.40 | 0.50 | 75.8% | 66.7% | 76.4% | 75.3%/59.5% | 6.9 (interpolated) | pass | 0.479 (unverified) | 1.05 |
| 4 | `cfg_226a` | timeframe=5min, ma_pair=EMA/EMA, fast_length=16, slow_length=150, confirm_bars=2, buffer_atr=0.35, stop_atr=None, slope_filter=True | 0/424 | 424 | 93.6% | 14.1% | 1.15 | -8.0% | 117 | 1.45 | 57.8% | 167.0 | 10/10 | 1.00 | 1.03 | 0.12 | 5 | 40.8% | 0.46 | 0.50 | 84.4% | 75.6% | 79.7% | 81.8%/60.3% | 7.8 (interpolated) | pass | 0.540 (unverified) | 1.06 |
| 5 | `cfg_e628` | timeframe=5min, ma_pair=SMA/SMA, fast_length=5, slow_length=150, confirm_bars=1, buffer_atr=0.1, stop_atr=None, slope_filter=True | 0/588 | 588 | 89.2% | 13.6% | 1.16 | -8.2% | 103 | 1.39 | 51.4% | 234.5 | 8/8 | 1.00 | 1.03 | 0.13 | 5 | 43.3% | 0.45 | 0.42 | 76.8% | 65.3% | 77.7% | 75.9%/61.0% | 5.8 (interpolated) | pass | 0.550 (unverified) | 0.71 |
| 6 | `cfg_d41a` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=60, confirm_bars=2, buffer_atr=0.2, stop_atr=1.5, slope_filter=False | 208/129 | 337 | 74.6% | 11.8% | 1.16 | -8.9% | 113 | 1.49 | 46.5% | 134.4 | 12/12 | 0.92 | 1.02 | 0.13 | 5 | 49.3% | 0.33 | 0.55 | 68.0% | 61.6% | 62.1% | 65.8%/51.5% | 8.2 (interpolated) | pass | 0.549 (unverified) | 0.68 |
| 7 | `cfg_8508` | timeframe=15min, ma_pair=SMA/EMA, fast_length=8, slow_length=100, confirm_bars=3, buffer_atr=0.1, stop_atr=2.0, slope_filter=True | 120/135 | 255 | 70.3% | 11.3% | 1.04 | -8.3% | 121 | 1.57 | 49.5% | 103.0 | 13/13 | 1.00 | 1.02 | 0.02 | 5 | 42.7% | 0.34 | 0.62 | 65.4% | 60.6% | 67.9% | 61.5%/46.4% | 10.2 (interpolated) | pass | 0.438 (unverified) | 0.90 |
| 8 | `cfg_3421` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=100, confirm_bars=3, buffer_atr=0.1, stop_atr=2.0, slope_filter=False | 113/127 | 240 | 74.2% | 11.7% | 1.08 | -8.3% | 117 | 1.61 | 48.4% | 97.3 | 13/13 | 1.00 | 1.02 | 0.06 | 5 | 34.2% | 0.48 | 0.61 | 69.5% | 64.8% | 72.3% | 65.2%/51.2% | 11.1 (interpolated) | pass | 0.476 (unverified) | 0.76 |
| 9 | `cfg_9274` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=60, confirm_bars=3, buffer_atr=0.35, stop_atr=1.5, slope_filter=False | 190/118 | 308 | 78.3% | 12.3% | 1.20 | -7.0% | 158 | 1.60 | 42.9% | 122.9 | 12/12 | 1.00 | 1.02 | 0.18 | 5 | 38.0% | 0.42 | 0.53 | 72.0% | 66.1% | 56.5% | 71.7%/54.3% | 9.2 (interpolated) | pass | 0.583 (unverified) | 1.16 |
| 10 | `cfg_456b` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=150, confirm_bars=2, buffer_atr=0.1, stop_atr=None, slope_filter=False | 0/195 | 195 | 81.0% | 12.6% | 1.07 | -10.3% | 131 | 1.64 | 60.7% | 78.9 | 11/11 | 1.00 | 1.01 | 0.06 | 4 | 37.3% | 0.51 | 0.59 | 77.0% | 73.1% | 72.3% | 72.1%/58.3% | 14.3 (interpolated) | pass | 0.471 (unverified) | 0.79 |
| 11 | `cfg_6d8a` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=100, confirm_bars=2, buffer_atr=0.35, stop_atr=None, slope_filter=True | 0/223 | 223 | 82.0% | 12.7% | 1.07 | -8.1% | 95 | 1.58 | 59.0% | 90.4 | 12/12 | 1.00 | 1.00 | 0.06 | 5 | 42.1% | 0.44 | 0.59 | 77.4% | 72.9% | 83.0% | 74.0%/59.5% | 12.8 (interpolated) | pass | 0.466 (unverified) | 0.92 |
| 12 | `cfg_c2e4` | timeframe=15min, ma_pair=SMA/EMA, fast_length=8, slow_length=100, confirm_bars=2, buffer_atr=0.0, stop_atr=1.5, slope_filter=True | 157/108 | 265 | 52.1% | 8.8% | 0.89 | -12.5% | 229 | 1.48 | 43.8% | 106.4 | 11/11 | 1.00 | 1.00 | -0.11 | 4 | 23.8% | 0.52 | 0.63 | 47.6% | 43.1% | 58.5% | 45.7%/33.0% | 7.9 (interpolated) | pass | 0.312 (unverified) | 0.87 |
| 13 | `cfg_e43e` | timeframe=5min, ma_pair=EMA/SMA, fast_length=16, slow_length=150, confirm_bars=4, buffer_atr=0.1, stop_atr=1.5, slope_filter=True | 300/100 | 400 | 47.2% | 8.0% | 0.98 | -7.2% | 387 | 1.45 | 27.6% | 159.8 | 9/9 | 1.00 | 0.98 | 0.00 | 5 | 27.6% | 0.42 | 0.56 | 40.6% | 34.3% | 23.2% | 41.9%/31.6% | 5.3 (interpolated) | pass | 0.392 (unverified) | 1.22 |
| 14 | `cfg_8a80` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=100, confirm_bars=2, buffer_atr=0.1, stop_atr=2.0, slope_filter=True | 112/139 | 251 | 68.5% | 11.0% | 1.03 | -7.9% | 104 | 1.56 | 50.8% | 101.6 | 13/13 | 1.00 | 0.98 | 0.05 | 5 | 41.7% | 0.34 | 0.62 | 63.8% | 59.1% | 71.5% | 61.4%/43.6% | 10.1 (interpolated) | pass | 0.433 (unverified) | 0.83 |
| 15 | `cfg_44c6` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=60, confirm_bars=4, buffer_atr=0.5, stop_atr=1.5, slope_filter=False | 188/106 | 294 | 71.0% | 11.3% | 1.13 | -6.5% | 148 | 1.56 | 40.4% | 117.9 | 10/10 | 1.00 | 0.98 | 0.15 | 4 | 27.3% | 0.54 | 0.55 | 65.3% | 59.8% | 61.2% | 64.2%/48.3% | 9.0 (interpolated) | pass | 0.523 (unverified) | 1.09 |
| 16 | `cfg_d13e` | timeframe=5min, ma_pair=SMA/SMA, fast_length=5, slow_length=150, confirm_bars=1, buffer_atr=0.2, stop_atr=3.0, slope_filter=True | 201/370 | 571 | 66.6% | 10.8% | 0.99 | -8.0% | 230 | 1.33 | 44.2% | 228.6 | 9/9 | 0.89 | 0.98 | 0.02 | 5 | 36.6% | 0.41 | 0.50 | 56.1% | 46.2% | 54.8% | 58.2%/42.7% | 5.0 (interpolated) | pass | 0.400 (unverified) | 0.66 |
| 17 | `cfg_dfb9` | timeframe=15min, ma_pair=SMA/EMA, fast_length=5, slow_length=80, confirm_bars=2, buffer_atr=0.35, stop_atr=1.5, slope_filter=False | 192/137 | 329 | 61.3% | 10.0% | 0.98 | -7.8% | 117 | 1.47 | 46.5% | 131.4 | 11/11 | 1.00 | 0.97 | 0.00 | 5 | 39.5% | 0.30 | 0.53 | 55.4% | 49.7% | 61.7% | 53.6%/41.2% | 7.4 (interpolated) | pass | 0.386 (unverified) | 0.71 |
| 18 | `cfg_1bcd` | timeframe=5min, ma_pair=EMA/EMA, fast_length=5, slow_length=150, confirm_bars=3, buffer_atr=0.5, stop_atr=None, slope_filter=False | 0/620 | 620 | 79.4% | 12.4% | 1.00 | -17.7% | 100 | 1.36 | 56.9% | 245.3 | 8/8 | 1.00 | 0.97 | 0.03 | 5 | 51.6% | 0.32 | 0.49 | 67.0% | 55.5% | 80.6% | 71.5%/49.8% | 5.2 (interpolated) | pass | 0.408 (unverified) | 0.96 |
| 19 | `cfg_0c6f` | timeframe=15min, ma_pair=SMA/SMA, fast_length=5, slow_length=80, confirm_bars=1, buffer_atr=0.0, stop_atr=1.5, slope_filter=False | 208/156 | 364 | 65.0% | 10.5% | 1.01 | -9.7% | 134 | 1.46 | 44.6% | 144.5 | 9/9 | 0.89 | 0.97 | 0.04 | 5 | 44.1% | 0.29 | 0.54 | 58.2% | 51.7% | 71.8% | 58.2%/41.1% | 7.0 (interpolated) | pass | 0.415 (unverified) | 0.63 |
| 20 | `cfg_50c7` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=100, confirm_bars=2, buffer_atr=0.1, stop_atr=1.5, slope_filter=True | 152/99 | 251 | 62.6% | 10.2% | 1.02 | -7.8% | 95 | 1.58 | 45.3% | 101.6 | 12/12 | 1.00 | 0.97 | 0.05 | 5 | 33.1% | 0.42 | 0.63 | 57.9% | 53.5% | 62.5% | 55.4%/42.9% | 9.5 (interpolated) | pass | 0.424 (unverified) | 0.93 |
| 21 | `cfg_52e8` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=60, confirm_bars=4, buffer_atr=0.5, stop_atr=2.0, slope_filter=True | 160/134 | 294 | 73.5% | 11.7% | 1.10 | -7.0% | 94 | 1.49 | 46.9% | 117.9 | 11/11 | 1.00 | 0.97 | 0.13 | 5 | 28.8% | 0.54 | 0.57 | 67.8% | 62.1% | 71.7% | 65.1%/53.1% | 9.2 (interpolated) | pass | 0.496 (unverified) | 1.15 |
| 22 | `cfg_1a38` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=60, confirm_bars=4, buffer_atr=0.35, stop_atr=2.0, slope_filter=False | 158/147 | 305 | 68.9% | 11.1% | 1.04 | -7.0% | 103 | 1.45 | 48.0% | 121.7 | 12/12 | 1.00 | 0.97 | 0.07 | 5 | 32.9% | 0.45 | 0.59 | 63.1% | 57.5% | 61.1% | 59.2%/44.8% | 8.5 (interpolated) | pass | 0.441 (unverified) | 0.98 |
| 23 | `cfg_8735` | timeframe=15min, ma_pair=EMA/EMA, fast_length=5, slow_length=60, confirm_bars=2, buffer_atr=0.2, stop_atr=1.5, slope_filter=True | 219/179 | 398 | 66.8% | 10.8% | 1.02 | -7.0% | 103 | 1.42 | 48.3% | 158.1 | 11/11 | 0.91 | 0.96 | 0.06 | 5 | 31.1% | 0.47 | 0.62 | 59.3% | 52.2% | 69.1% | 60.5%/47.0% | 6.6 (interpolated) | pass | 0.423 (unverified) | 0.79 |
| 24 | `cfg_d23c` | timeframe=15min, ma_pair=SMA/EMA, fast_length=5, slow_length=100, confirm_bars=3, buffer_atr=0.0, stop_atr=2.0, slope_filter=True | 118/193 | 311 | 74.3% | 11.8% | 1.06 | -7.6% | 89 | 1.53 | 51.7% | 125.1 | 11/11 | 0.91 | 0.96 | 0.10 | 4 | 34.7% | 0.48 | 0.57 | 68.2% | 62.3% | 55.8% | 64.0%/50.8% | 8.8 (interpolated) | pass | 0.460 (unverified) | 0.55 |
| 25 | `cfg_c62f` | timeframe=15min, ma_pair=SMA/EMA, fast_length=5, slow_length=60, confirm_bars=2, buffer_atr=0.0, stop_atr=1.5, slope_filter=False | 222/223 | 445 | 65.2% | 10.6% | 1.03 | -7.1% | 117 | 1.40 | 47.8% | 176.9 | 10/10 | 0.90 | 0.95 | 0.08 | 5 | 27.8% | 0.49 | 0.64 | 57.0% | 49.2% | 56.8% | 57.7%/44.3% | 5.9 (interpolated) | pass | 0.431 (unverified) | 0.52 |
| 26 | `cfg_472f` | timeframe=5min, ma_pair=EMA/SMA, fast_length=16, slow_length=150, confirm_bars=2, buffer_atr=0.1, stop_atr=1.5, slope_filter=True | 297/106 | 403 | 52.0% | 8.7% | 1.05 | -7.4% | 389 | 1.50 | 28.4% | 161.0 | 10/10 | 1.00 | 0.95 | 0.10 | 5 | 29.0% | 0.44 | 0.51 | 45.2% | 38.6% | 30.6% | 45.2%/35.7% | 5.6 (interpolated) | pass | 0.448 (unverified) | 1.14 |
| 27 | `cfg_3f62` | timeframe=15min, ma_pair=SMA/EMA, fast_length=5, slow_length=80, confirm_bars=3, buffer_atr=0.35, stop_atr=1.5, slope_filter=True | 182/141 | 323 | 62.9% | 10.3% | 0.99 | -7.2% | 158 | 1.49 | 44.5% | 129.0 | 11/11 | 0.91 | 0.94 | 0.05 | 5 | 31.5% | 0.43 | 0.55 | 57.0% | 51.3% | 53.9% | 53.4%/41.5% | 7.6 (interpolated) | pass | 0.397 (unverified) | 0.81 |
| 28 | `cfg_1a20` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=100, confirm_bars=3, buffer_atr=0.1, stop_atr=1.5, slope_filter=False | 144/96 | 240 | 65.1% | 10.6% | 1.02 | -7.7% | 182 | 1.61 | 43.6% | 97.2 | 12/12 | 1.00 | 0.94 | 0.08 | 5 | 24.7% | 0.58 | 0.63 | 60.6% | 56.2% | 60.6% | 58.3%/45.0% | 10.2 (interpolated) | pass | 0.420 (unverified) | 0.76 |
| 29 | `cfg_b70b` | timeframe=15min, ma_pair=EMA/SMA, fast_length=20, slow_length=60, confirm_bars=4, buffer_atr=0.2, stop_atr=2.0, slope_filter=False | 166/105 | 271 | 64.0% | 10.4% | 1.03 | -9.6% | 164 | 1.46 | 39.5% | 108.0 | 11/11 | 0.91 | 0.94 | 0.09 | 5 | 39.5% | 0.33 | 0.54 | 58.9% | 54.0% | 43.5% | 56.6%/45.4% | 9.0 (interpolated) | pass | 0.429 (unverified) | 0.90 |
| 30 | `cfg_1a6a` | timeframe=15min, ma_pair=SMA/EMA, fast_length=8, slow_length=150, confirm_bars=4, buffer_atr=0.5, stop_atr=None, slope_filter=True | 0/175 | 175 | 68.4% | 11.0% | 0.96 | -12.1% | 229 | 1.59 | 59.2% | 70.4 | 9/9 | 1.00 | 0.93 | 0.02 | 4 | 23.5% | 0.65 | 0.64 | 65.0% | 61.7% | 64.9% | 58.9%/46.4% | 14.0 (interpolated) | pass | 0.372 (unverified) | 0.82 |
| 31 | `cfg_2253` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=40, confirm_bars=4, buffer_atr=0.5, stop_atr=2.0, slope_filter=True | 180/170 | 350 | 62.0% | 10.1% | 0.97 | -8.0% | 191 | 1.38 | 44.5% | 139.6 | 10/10 | 0.90 | 0.93 | 0.04 | 4 | 18.8% | 0.64 | 0.60 | 55.7% | 49.5% | 58.3% | 56.1%/41.5% | 7.0 (interpolated) | pass | 0.375 (unverified) | 1.02 |
| 32 | `cfg_747e` | timeframe=15min, ma_pair=SMA/SMA, fast_length=5, slow_length=80, confirm_bars=1, buffer_atr=0.5, stop_atr=2.0, slope_filter=True | 144/112 | 256 | 55.1% | 9.2% | 0.95 | -8.1% | 243 | 1.44 | 41.0% | 102.5 | 10/10 | 1.00 | 0.92 | 0.02 | 5 | 21.7% | 0.56 | 0.66 | 50.6% | 46.2% | 43.8% | 47.8%/39.3% | 8.5 (interpolated) | pass | 0.359 (unverified) | 0.92 |
| 33 | `cfg_0631` | timeframe=15min, ma_pair=SMA/SMA, fast_length=5, slow_length=80, confirm_bars=1, buffer_atr=0.5, stop_atr=1.5, slope_filter=True | 167/89 | 256 | 52.2% | 8.8% | 0.97 | -8.1% | 158 | 1.48 | 36.3% | 102.6 | 9/9 | 1.00 | 0.92 | 0.05 | 4 | 15.1% | 0.68 | 0.67 | 47.8% | 43.4% | 60.2% | 44.9%/34.2% | 8.1 (interpolated) | pass | 0.380 (unverified) | 0.96 |
| 34 | `cfg_54a0` | timeframe=15min, ma_pair=SMA/EMA, fast_length=12, slow_length=100, confirm_bars=2, buffer_atr=0.2, stop_atr=2.0, slope_filter=True | 120/91 | 211 | 65.2% | 10.6% | 0.98 | -9.7% | 224 | 1.57 | 47.3% | 85.6 | 13/13 | 0.92 | 0.92 | 0.06 | 4 | 34.9% | 0.43 | 0.71 | 61.3% | 57.5% | 42.0% | 57.4%/43.9% | 11.4 (interpolated) | pass | 0.384 (unverified) | 0.66 |
| 35 | `cfg_dc01` | timeframe=15min, ma_pair=EMA/EMA, fast_length=12, slow_length=40, confirm_bars=4, buffer_atr=0.5, stop_atr=2.0, slope_filter=True | 164/132 | 296 | 67.2% | 10.8% | 1.05 | -7.3% | 140 | 1.47 | 42.6% | 118.3 | 10/10 | 1.00 | 0.92 | 0.13 | 5 | 28.2% | 0.50 | 0.58 | 61.6% | 56.2% | 49.4% | 58.5%/39.4% | 8.6 (interpolated) | pass | 0.451 (unverified) | 0.97 |
| 36 | `cfg_fcef` | timeframe=15min, ma_pair=EMA/SMA, fast_length=20, slow_length=60, confirm_bars=4, buffer_atr=0.35, stop_atr=2.0, slope_filter=False | 165/100 | 265 | 60.4% | 9.9% | 0.98 | -8.4% | 157 | 1.43 | 39.4% | 105.5 | 11/11 | 0.91 | 0.90 | 0.07 | 5 | 40.7% | 0.33 | 0.57 | 55.5% | 50.8% | 40.9% | 55.7%/43.7% | 8.8 (interpolated) | pass | 0.387 (unverified) | 0.88 |
| 37 | `cfg_f8ee` | timeframe=15min, ma_pair=EMA/SMA, fast_length=5, slow_length=60, confirm_bars=2, buffer_atr=0.2, stop_atr=None, slope_filter=True | 0/327 | 327 | 73.0% | 11.6% | 1.02 | -6.7% | 103 | 1.43 | 51.3% | 130.7 | 11/11 | 1.00 | 0.90 | 0.12 | 5 | 31.5% | 0.53 | 0.48 | 66.5% | 60.5% | 57.9% | 64.5%/50.5% | 8.3 (interpolated) | pass | 0.424 (unverified) | 1.05 |
| 38 | `cfg_7852` | timeframe=15min, ma_pair=SMA/SMA, fast_length=5, slow_length=80, confirm_bars=2, buffer_atr=0.35, stop_atr=1.5, slope_filter=True | 168/94 | 262 | 57.6% | 9.5% | 1.04 | -6.8% | 158 | 1.52 | 37.0% | 105.1 | 11/11 | 1.00 | 0.90 | 0.14 | 5 | 20.4% | 0.59 | 0.64 | 52.9% | 48.4% | 54.5% | 51.5%/39.2% | 8.6 (interpolated) | pass | 0.441 (unverified) | 0.92 |
| 39 | `cfg_bd92` | timeframe=5min, ma_pair=SMA/SMA, fast_length=5, slow_length=150, confirm_bars=4, buffer_atr=0.2, stop_atr=2.0, slope_filter=True | 292/259 | 551 | 62.3% | 10.2% | 1.04 | -9.9% | 132 | 1.37 | 38.4% | 220.8 | 9/9 | 1.00 | 0.90 | 0.14 | 5 | 37.9% | 0.28 | 0.46 | 52.3% | 43.0% | 36.3% | 54.3%/40.0% | 4.9 (interpolated) | pass | 0.439 (unverified) | 0.72 |
| 40 | `cfg_9e52` | timeframe=15min, ma_pair=EMA/EMA, fast_length=5, slow_length=60, confirm_bars=1, buffer_atr=0.1, stop_atr=3.0, slope_filter=True | 80/339 | 419 | 62.5% | 10.2% | 0.87 | -8.4% | 206 | 1.33 | 55.9% | 165.9 | 11/11 | 0.91 | 0.89 | -0.02 | 5 | 36.9% | 0.40 | 0.63 | 54.9% | 47.5% | 54.0% | 58.5%/39.6% | 6.0 (interpolated) | pass | 0.302 (unverified) | 0.87 |
| 41 | `cfg_475c` | timeframe=15min, ma_pair=EMA/SMA, fast_length=5, slow_length=80, confirm_bars=2, buffer_atr=0.2, stop_atr=None, slope_filter=False | 0/318 | 318 | 78.1% | 12.2% | 1.00 | -9.1% | 185 | 1.42 | 57.7% | 126.5 | 11/11 | 1.00 | 0.89 | 0.11 | 5 | 35.4% | 0.48 | 0.51 | 71.6% | 65.5% | 70.5% | 71.8%/56.5% | 9.0 (interpolated) | pass | 0.407 (unverified) | 1.00 |
| 42 | `cfg_d99e` | timeframe=15min, ma_pair=SMA/EMA, fast_length=12, slow_length=100, confirm_bars=2, buffer_atr=0.0, stop_atr=1.5, slope_filter=True | 143/82 | 225 | 60.8% | 10.0% | 1.01 | -8.4% | 120 | 1.59 | 42.6% | 91.5 | 11/11 | 1.00 | 0.89 | 0.12 | 5 | 37.1% | 0.35 | 0.71 | 56.7% | 52.7% | 44.8% | 55.9%/41.2% | 10.3 (interpolated) | pass | 0.420 (unverified) | 0.77 |
| 43 | `cfg_0959` | timeframe=5min, ma_pair=SMA/SMA, fast_length=16, slow_length=150, confirm_bars=2, buffer_atr=0.0, stop_atr=1.5, slope_filter=True | 308/114 | 422 | 49.0% | 8.3% | 0.99 | -9.0% | 329 | 1.45 | 28.2% | 168.7 | 9/9 | 1.00 | 0.89 | 0.10 | 4 | 30.6% | 0.38 | 0.52 | 42.0% | 35.2% | 22.6% | 43.9%/33.0% | 5.2 (interpolated) | pass | 0.399 (unverified) | 0.99 |
| 44 | `cfg_02d8` | timeframe=15min, ma_pair=EMA/EMA, fast_length=12, slow_length=40, confirm_bars=4, buffer_atr=0.5, stop_atr=1.5, slope_filter=False | 193/103 | 296 | 60.2% | 9.9% | 1.02 | -8.7% | 194 | 1.50 | 37.6% | 118.3 | 9/9 | 0.89 | 0.89 | 0.13 | 5 | 27.7% | 0.47 | 0.53 | 54.9% | 49.7% | 40.5% | 53.0%/43.0% | 7.9 (interpolated) | pass | 0.424 (unverified) | 0.85 |
| 45 | `cfg_5e60` | timeframe=15min, ma_pair=EMA/SMA, fast_length=8, slow_length=100, confirm_bars=4, buffer_atr=0.2, stop_atr=1.5, slope_filter=False | 154/76 | 230 | 60.2% | 9.9% | 1.08 | -6.2% | 235 | 1.59 | 38.9% | 93.4 | 11/11 | 0.91 | 0.89 | 0.20 | 3 | 28.2% | 0.46 | 0.69 | 56.0% | 52.0% | 43.3% | 54.9%/43.7% | 10.0 (interpolated) | pass | 0.483 (unverified) | 0.47 |
| 46 | `cfg_c564` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=60, confirm_bars=2, buffer_atr=0.5, stop_atr=None, slope_filter=True | 0/299 | 299 | 64.8% | 10.5% | 0.92 | -7.5% | 182 | 1.37 | 56.7% | 119.5 | 11/11 | 1.00 | 0.88 | 0.03 | 4 | 27.6% | 0.53 | 0.64 | 59.3% | 53.9% | 56.9% | 56.2%/40.7% | 8.3 (interpolated) | pass | 0.335 (unverified) | 1.11 |
| 47 | `cfg_d8d5` | timeframe=15min, ma_pair=EMA/SMA, fast_length=5, slow_length=80, confirm_bars=2, buffer_atr=0.2, stop_atr=1.5, slope_filter=False | 197/121 | 318 | 66.5% | 10.7% | 1.06 | -9.8% | 118 | 1.48 | 43.4% | 126.6 | 11/11 | 0.91 | 0.88 | 0.18 | 5 | 44.0% | 0.25 | 0.50 | 60.5% | 54.8% | 43.7% | 58.4%/43.1% | 8.0 (interpolated) | pass | 0.459 (unverified) | 0.61 |
| 48 | `cfg_67fd` | timeframe=15min, ma_pair=EMA/EMA, fast_length=20, slow_length=40, confirm_bars=3, buffer_atr=0.1, stop_atr=2.0, slope_filter=False | 167/111 | 278 | 59.5% | 9.8% | 0.91 | -9.2% | 140 | 1.42 | 44.3% | 111.2 | 11/11 | 1.00 | 0.88 | 0.04 | 5 | 30.6% | 0.43 | 0.53 | 54.5% | 49.7% | 56.3% | 51.0%/40.8% | 8.3 (interpolated) | pass | 0.332 (unverified) | 0.95 |
| 49 | `cfg_87fc` | timeframe=15min, ma_pair=EMA/SMA, fast_length=8, slow_length=100, confirm_bars=4, buffer_atr=0.2, stop_atr=2.0, slope_filter=False | 133/97 | 230 | 68.6% | 11.0% | 1.06 | -7.0% | 113 | 1.55 | 44.2% | 93.6 | 12/12 | 1.00 | 0.88 | 0.19 | 4 | 27.0% | 0.55 | 0.67 | 64.1% | 59.9% | 45.6% | 63.2%/45.8% | 10.9 (interpolated) | pass | 0.463 (unverified) | 0.70 |
| 50 | `cfg_e6b0` | timeframe=15min, ma_pair=EMA/SMA, fast_length=5, slow_length=100, confirm_bars=4, buffer_atr=0.5, stop_atr=2.0, slope_filter=False | 132/108 | 240 | 59.2% | 9.8% | 0.94 | -6.8% | 138 | 1.47 | 43.1% | 97.7 | 10/10 | 1.00 | 0.88 | 0.06 | 4 | 22.6% | 0.58 | 0.69 | 54.9% | 50.7% | 47.7% | 56.2%/41.5% | 9.5 (interpolated) | pass | 0.353 (unverified) | 0.72 |
| 51 | `cfg_502c` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=100, confirm_bars=1, buffer_atr=0.1, stop_atr=1.5, slope_filter=False | 155/99 | 254 | 56.4% | 9.4% | 0.92 | -12.5% | 229 | 1.51 | 45.7% | 102.6 | 11/11 | 1.00 | 0.88 | 0.05 | 4 | 33.8% | 0.41 | 0.65 | 51.8% | 47.5% | 58.4% | 49.5%/39.7% | 8.7 (interpolated) | pass | 0.340 (unverified) | 0.98 |
| 52 | `cfg_3226` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=80, confirm_bars=2, buffer_atr=0.35, stop_atr=1.5, slope_filter=False | 170/98 | 268 | 55.1% | 9.2% | 0.92 | -12.0% | 229 | 1.47 | 43.6% | 107.8 | 12/12 | 1.00 | 0.87 | 0.05 | 4 | 34.8% | 0.38 | 0.57 | 50.4% | 45.9% | 45.7% | 50.0%/36.3% | 8.2 (interpolated) | pass | 0.337 (unverified) | 1.01 |
| 53 | `cfg_bb7e` | timeframe=15min, ma_pair=EMA/SMA, fast_length=20, slow_length=60, confirm_bars=4, buffer_atr=0.1, stop_atr=3.0, slope_filter=False | 122/155 | 277 | 61.9% | 10.1% | 0.91 | -12.0% | 191 | 1.37 | 47.9% | 110.6 | 11/11 | 0.91 | 0.87 | 0.05 | 4 | 28.4% | 0.50 | 0.64 | 56.9% | 51.9% | 62.4% | 52.2%/40.7% | 8.6 (interpolated) | pass | 0.333 (unverified) | 0.90 |
| 54 | `cfg_36ec` | timeframe=15min, ma_pair=EMA/EMA, fast_length=12, slow_length=60, confirm_bars=4, buffer_atr=0.5, stop_atr=1.5, slope_filter=True | 166/91 | 257 | 50.5% | 8.5% | 0.89 | -7.0% | 261 | 1.46 | 38.4% | 103.3 | 10/10 | 0.90 | 0.86 | 0.02 | 5 | 25.6% | 0.45 | 0.58 | 46.1% | 41.9% | 36.6% | 45.3%/36.3% | 7.9 (interpolated) | pass | 0.309 (unverified) | 0.74 |
| 55 | `cfg_3379` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=40, confirm_bars=1, buffer_atr=0.5, stop_atr=2.5, slope_filter=True | 149/205 | 354 | 59.6% | 9.8% | 0.92 | -7.6% | 117 | 1.34 | 48.5% | 141.0 | 10/10 | 0.90 | 0.86 | 0.05 | 5 | 24.6% | 0.52 | 0.59 | 53.3% | 47.2% | 42.1% | 54.6%/37.0% | 6.8 (interpolated) | pass | 0.335 (unverified) | 1.12 |
| 56 | `cfg_abbb` | timeframe=15min, ma_pair=EMA/EMA, fast_length=12, slow_length=40, confirm_bars=4, buffer_atr=0.35, stop_atr=1.5, slope_filter=True | 211/105 | 316 | 47.8% | 8.1% | 0.85 | -8.3% | 158 | 1.38 | 38.6% | 125.9 | 10/10 | 1.00 | 0.86 | -0.01 | 5 | 30.8% | 0.33 | 0.68 | 42.5% | 37.4% | 29.0% | 41.9%/32.2% | 6.4 (interpolated) | pass | 0.278 (unverified) | 0.74 |
| 57 | `cfg_ff8b` | timeframe=15min, ma_pair=SMA/SMA, fast_length=8, slow_length=80, confirm_bars=3, buffer_atr=0.35, stop_atr=1.5, slope_filter=False | 176/95 | 271 | 50.8% | 8.6% | 0.90 | -8.0% | 165 | 1.43 | 39.1% | 108.4 | 12/12 | 0.92 | 0.86 | 0.04 | 5 | 24.1% | 0.48 | 0.60 | 46.2% | 41.7% | 43.9% | 46.4%/36.1% | 7.6 (interpolated) | pass | 0.322 (unverified) | 0.72 |
| 58 | `cfg_3f06` | timeframe=15min, ma_pair=SMA/EMA, fast_length=20, slow_length=40, confirm_bars=2, buffer_atr=0.35, stop_atr=2.0, slope_filter=True | 160/98 | 258 | 54.2% | 9.1% | 0.93 | -7.7% | 191 | 1.41 | 39.0% | 103.5 | 11/11 | 0.91 | 0.86 | 0.07 | 4 | 23.3% | 0.52 | 0.73 | 49.7% | 45.3% | 58.9% | 46.1%/35.3% | 8.3 (interpolated) | pass | 0.350 (unverified) | 0.30 |
| 59 | `cfg_e2e2` | timeframe=15min, ma_pair=EMA/SMA, fast_length=16, slow_length=60, confirm_bars=4, buffer_atr=0.1, stop_atr=1.5, slope_filter=False | 193/92 | 285 | 46.1% | 7.9% | 0.92 | -11.3% | 191 | 1.38 | 36.3% | 113.9 | 11/11 | 0.82 | 0.86 | 0.06 | 4 | 27.5% | 0.38 | 0.64 | 41.4% | 36.9% | 52.6% | 38.0%/28.0% | 6.8 (interpolated) | pass | 0.344 (unverified) | 0.87 |
| 60 | `cfg_606a` | timeframe=15min, ma_pair=EMA/SMA, fast_length=8, slow_length=100, confirm_bars=1, buffer_atr=0.35, stop_atr=2.0, slope_filter=False | 132/99 | 231 | 61.8% | 10.1% | 0.99 | -9.5% | 83 | 1.49 | 45.7% | 93.8 | 12/12 | 0.92 | 0.86 | 0.14 | 4 | 33.6% | 0.42 | 0.68 | 57.6% | 53.5% | 48.3% | 54.5%/42.3% | 10.1 (interpolated) | pass | 0.399 (unverified) | 0.80 |
| 61 | `cfg_533d` | timeframe=15min, ma_pair=EMA/SMA, fast_length=5, slow_length=80, confirm_bars=2, buffer_atr=0.35, stop_atr=1.5, slope_filter=True | 164/89 | 253 | 56.1% | 9.3% | 1.02 | -6.8% | 128 | 1.53 | 37.1% | 101.5 | 11/11 | 1.00 | 0.85 | 0.17 | 5 | 26.5% | 0.47 | 0.58 | 51.7% | 47.3% | 44.9% | 50.3%/37.2% | 8.7 (interpolated) | pass | 0.427 (unverified) | 0.90 |
| 62 | `cfg_c7d1` | timeframe=15min, ma_pair=EMA/SMA, fast_length=12, slow_length=100, confirm_bars=2, buffer_atr=0.1, stop_atr=2.0, slope_filter=False | 133/93 | 226 | 61.0% | 10.0% | 0.96 | -8.0% | 191 | 1.49 | 45.0% | 91.5 | 13/13 | 1.00 | 0.85 | 0.11 | 4 | 36.5% | 0.37 | 0.75 | 56.8% | 52.8% | 49.8% | 53.3%/40.4% | 10.2 (interpolated) | pass | 0.374 (unverified) | 0.73 |
| 63 | `cfg_5e7f` | timeframe=15min, ma_pair=SMA/SMA, fast_length=5, slow_length=60, confirm_bars=2, buffer_atr=0.35, stop_atr=None, slope_filter=False | 0/379 | 379 | 67.1% | 10.8% | 0.91 | -7.6% | 195 | 1.34 | 56.6% | 150.9 | 11/11 | 1.00 | 0.85 | 0.06 | 5 | 29.1% | 0.50 | 0.55 | 60.0% | 53.2% | 68.8% | 60.0%/40.5% | 6.9 (interpolated) | pass | 0.331 (unverified) | 0.94 |
| 64 | `cfg_a27f` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=150, confirm_bars=3, buffer_atr=0.5, stop_atr=2.0, slope_filter=True | 98/69 | 167 | 61.9% | 10.1% | 1.00 | -9.3% | 224 | 1.69 | 49.7% | 66.9 | 11/11 | 1.00 | 0.85 | 0.15 | 4 | 30.9% | 0.48 | 0.70 | 58.9% | 55.8% | 28.7% | 55.3%/43.5% | 13.6 (interpolated) | pass | 0.402 (unverified) | 0.71 |
| 65 | `cfg_62e7` | timeframe=15min, ma_pair=SMA/SMA, fast_length=8, slow_length=80, confirm_bars=4, buffer_atr=0.2, stop_atr=1.5, slope_filter=False | 183/89 | 272 | 44.0% | 7.6% | 0.85 | -9.2% | 214 | 1.37 | 37.4% | 108.7 | 11/11 | 0.91 | 0.85 | 0.00 | 5 | 29.0% | 0.31 | 0.71 | 39.5% | 35.2% | 37.3% | 39.5%/30.0% | 6.9 (interpolated) | pass | 0.296 (unverified) | 0.85 |
| 66 | `cfg_e023` | timeframe=15min, ma_pair=EMA/EMA, fast_length=12, slow_length=100, confirm_bars=2, buffer_atr=0.0, stop_atr=1.5, slope_filter=False | 131/88 | 219 | 53.4% | 8.9% | 0.96 | -8.4% | 257 | 1.55 | 43.6% | 88.3 | 11/11 | 1.00 | 0.84 | 0.11 | 5 | 27.3% | 0.39 | 0.77 | 49.5% | 45.9% | 46.5% | 46.7%/37.9% | 9.6 (interpolated) | pass | 0.369 (unverified) | 0.80 |
| 67 | `cfg_876a` | timeframe=15min, ma_pair=SMA/EMA, fast_length=20, slow_length=60, confirm_bars=3, buffer_atr=0.35, stop_atr=2.0, slope_filter=False | 141/82 | 223 | 66.0% | 10.7% | 1.04 | -9.0% | 191 | 1.53 | 40.4% | 89.8 | 12/12 | 0.92 | 0.84 | 0.21 | 4 | 28.7% | 0.52 | 0.68 | 61.9% | 57.8% | 28.8% | 56.8%/45.3% | 10.9 (interpolated) | pass | 0.444 (unverified) | 0.60 |
| 68 | `cfg_c821` | timeframe=5min, ma_pair=SMA/SMA, fast_length=5, slow_length=150, confirm_bars=3, buffer_atr=0.1, stop_atr=3.0, slope_filter=True | 209/360 | 569 | 51.8% | 8.7% | 0.83 | -8.0% | 265 | 1.27 | 43.4% | 227.8 | 10/10 | 1.00 | 0.84 | -0.01 | 5 | 30.7% | 0.31 | 0.56 | 42.2% | 33.2% | 44.5% | 44.1%/34.5% | 4.2 (interpolated) | pass | 0.267 (unverified) | 0.56 |
| 69 | `cfg_1760` | timeframe=15min, ma_pair=EMA/EMA, fast_length=5, slow_length=60, confirm_bars=1, buffer_atr=0.0, stop_atr=3.0, slope_filter=False | 77/396 | 473 | 55.1% | 9.2% | 0.76 | -16.8% | 97 | 1.27 | 57.6% | 187.2 | 10/10 | 0.90 | 0.83 | -0.07 | 5 | 33.5% | 0.39 | 0.71 | 46.9% | 39.1% | 56.0% | 46.2%/34.9% | 5.1 (interpolated) | pass | 0.224 (unverified) | 0.91 |
| 70 | `cfg_a905` | timeframe=15min, ma_pair=EMA/SMA, fast_length=8, slow_length=80, confirm_bars=4, buffer_atr=0.5, stop_atr=2.5, slope_filter=False | 125/132 | 257 | 62.7% | 10.2% | 0.93 | -10.1% | 191 | 1.42 | 46.6% | 103.1 | 11/11 | 0.91 | 0.83 | 0.10 | 4 | 28.2% | 0.52 | 0.61 | 57.9% | 53.4% | 52.8% | 54.9%/41.3% | 9.3 (interpolated) | pass | 0.348 (unverified) | 0.78 |
| 71 | `cfg_b887` | timeframe=15min, ma_pair=EMA/SMA, fast_length=5, slow_length=80, confirm_bars=1, buffer_atr=0.5, stop_atr=1.5, slope_filter=False | 193/97 | 290 | 57.6% | 9.5% | 0.99 | -11.5% | 179 | 1.46 | 40.4% | 115.9 | 9/9 | 1.00 | 0.83 | 0.16 | 5 | 38.6% | 0.33 | 0.54 | 52.4% | 47.4% | 42.3% | 52.8%/39.4% | 7.8 (interpolated) | pass | 0.399 (unverified) | 0.77 |
| 72 | `cfg_1455` | timeframe=15min, ma_pair=EMA/SMA, fast_length=8, slow_length=60, confirm_bars=4, buffer_atr=0.0, stop_atr=1.5, slope_filter=False | 218/116 | 334 | 42.3% | 7.3% | 0.78 | -8.6% | 207 | 1.32 | 39.4% | 133.5 | 10/10 | 0.90 | 0.83 | -0.05 | 4 | 24.9% | 0.38 | 0.66 | 36.9% | 31.8% | 39.7% | 38.8%/28.7% | 5.6 (interpolated) | pass | 0.233 (unverified) | 0.68 |
| 73 | `cfg_145f` | timeframe=15min, ma_pair=SMA/EMA, fast_length=5, slow_length=80, confirm_bars=1, buffer_atr=0.0, stop_atr=2.5, slope_filter=True | 104/297 | 401 | 61.0% | 10.0% | 0.88 | -9.3% | 89 | 1.36 | 56.6% | 159.0 | 10/10 | 1.00 | 0.83 | 0.06 | 5 | 37.4% | 0.38 | 0.56 | 53.7% | 46.8% | 57.5% | 54.9%/41.4% | 6.2 (interpolated) | pass | 0.307 (unverified) | 1.03 |
| 74 | `cfg_6791` | timeframe=15min, ma_pair=SMA/EMA, fast_length=12, slow_length=80, confirm_bars=2, buffer_atr=0.2, stop_atr=1.5, slope_filter=True | 157/91 | 248 | 57.4% | 9.5% | 0.98 | -7.3% | 121 | 1.51 | 43.0% | 100.2 | 12/12 | 0.92 | 0.82 | 0.16 | 5 | 37.2% | 0.35 | 0.72 | 52.9% | 48.7% | 39.1% | 48.3%/36.2% | 9.0 (interpolated) | pass | 0.395 (unverified) | 1.08 |
| 75 | `cfg_5f16` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=100, confirm_bars=2, buffer_atr=0.35, stop_atr=2.0, slope_filter=True | 117/106 | 223 | 58.5% | 9.7% | 0.93 | -9.0% | 196 | 1.52 | 46.8% | 90.0 | 13/13 | 1.00 | 0.82 | 0.11 | 5 | 39.4% | 0.29 | 0.68 | 54.5% | 50.6% | 69.3% | 53.3%/39.3% | 10.1 (interpolated) | pass | 0.344 (unverified) | 0.79 |
| 76 | `cfg_6f73` | timeframe=15min, ma_pair=SMA/EMA, fast_length=12, slow_length=100, confirm_bars=3, buffer_atr=0.0, stop_atr=2.0, slope_filter=False | 119/106 | 225 | 48.0% | 8.2% | 0.82 | -7.2% | 181 | 1.44 | 46.2% | 91.3 | 12/12 | 1.00 | 0.82 | 0.00 | 4 | 27.6% | 0.41 | 0.88 | 44.1% | 40.5% | 48.7% | 42.5%/28.5% | 8.6 (interpolated) | pass | 0.265 (unverified) | 0.67 |
| 77 | `cfg_aca4` | timeframe=15min, ma_pair=SMA/EMA, fast_length=12, slow_length=80, confirm_bars=2, buffer_atr=0.0, stop_atr=2.0, slope_filter=False | 138/135 | 273 | 59.5% | 9.8% | 0.89 | -8.7% | 216 | 1.45 | 49.0% | 110.0 | 12/12 | 1.00 | 0.82 | 0.07 | 4 | 34.5% | 0.38 | 0.71 | 54.7% | 49.9% | 46.5% | 52.5%/41.5% | 8.5 (interpolated) | pass | 0.314 (unverified) | 1.07 |
| 78 | `cfg_984d` | timeframe=15min, ma_pair=SMA/EMA, fast_length=8, slow_length=80, confirm_bars=2, buffer_atr=0.0, stop_atr=2.0, slope_filter=True | 159/158 | 317 | 52.7% | 8.8% | 0.80 | -7.5% | 112 | 1.35 | 50.3% | 126.3 | 12/12 | 0.92 | 0.82 | -0.02 | 4 | 24.0% | 0.48 | 0.74 | 47.3% | 41.9% | 37.8% | 47.1%/32.9% | 6.8 (interpolated) | pass | 0.248 (unverified) | 0.80 |
| 79 | `cfg_a42a` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=100, confirm_bars=2, buffer_atr=0.35, stop_atr=1.5, slope_filter=False | 147/76 | 223 | 50.3% | 8.5% | 0.88 | -11.7% | 329 | 1.51 | 41.0% | 89.9 | 12/12 | 1.00 | 0.82 | 0.06 | 5 | 30.7% | 0.37 | 0.73 | 46.5% | 42.8% | 49.5% | 44.6%/35.3% | 9.0 (interpolated) | pass | 0.301 (unverified) | 1.00 |
| 80 | `cfg_42f0` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=80, confirm_bars=3, buffer_atr=0.5, stop_atr=2.0, slope_filter=False | 139/113 | 252 | 58.9% | 9.7% | 0.92 | -7.4% | 126 | 1.45 | 46.5% | 101.8 | 12/12 | 1.00 | 0.82 | 0.10 | 4 | 39.5% | 0.33 | 0.67 | 54.3% | 50.0% | 50.0% | 53.2%/36.1% | 9.1 (interpolated) | pass | 0.337 (unverified) | 0.91 |
| 81 | `cfg_48b4` | timeframe=5min, ma_pair=EMA/EMA, fast_length=12, slow_length=150, confirm_bars=4, buffer_atr=0.2, stop_atr=2.0, slope_filter=False | 316/185 | 501 | 56.3% | 9.3% | 0.88 | -8.7% | 198 | 1.35 | 42.4% | 198.7 | 10/10 | 1.00 | 0.82 | 0.07 | 5 | 33.3% | 0.36 | 0.71 | 47.5% | 39.2% | 57.0% | 49.6%/35.2% | 4.9 (interpolated) | pass | 0.306 (unverified) | 0.94 |
| 82 | `cfg_6f38` | timeframe=15min, ma_pair=EMA/EMA, fast_length=12, slow_length=80, confirm_bars=2, buffer_atr=0.2, stop_atr=1.5, slope_filter=True | 152/80 | 232 | 40.4% | 7.0% | 0.75 | -9.7% | 330 | 1.39 | 40.6% | 93.7 | 12/12 | 1.00 | 0.81 | -0.06 | 4 | 15.6% | 0.55 | 0.85 | 36.7% | 33.1% | 44.0% | 36.7%/26.2% | 7.4 (interpolated) | pass | 0.211 (unverified) | 0.99 |
| 83 | `cfg_0b15` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=150, confirm_bars=2, buffer_atr=0.1, stop_atr=2.0, slope_filter=True | 100/93 | 193 | 57.4% | 9.5% | 0.92 | -9.0% | 131 | 1.57 | 50.4% | 77.8 | 12/12 | 1.00 | 0.81 | 0.11 | 4 | 34.4% | 0.38 | 0.70 | 53.9% | 50.5% | 55.9% | 51.3%/40.3% | 11.3 (interpolated) | pass | 0.339 (unverified) | 0.59 |
| 84 | `cfg_fd20` | timeframe=15min, ma_pair=EMA/SMA, fast_length=16, slow_length=60, confirm_bars=3, buffer_atr=0.0, stop_atr=1.5, slope_filter=False | 193/106 | 299 | 48.5% | 8.2% | 0.87 | -7.1% | 191 | 1.39 | 37.4% | 119.9 | 11/11 | 0.91 | 0.81 | 0.07 | 4 | 24.2% | 0.46 | 0.66 | 43.5% | 38.7% | 42.4% | 43.7%/33.6% | 6.8 (interpolated) | pass | 0.300 (unverified) | 1.02 |
| 85 | `cfg_8314` | timeframe=15min, ma_pair=EMA/SMA, fast_length=8, slow_length=100, confirm_bars=2, buffer_atr=0.1, stop_atr=None, slope_filter=True | 0/208 | 208 | 56.8% | 9.4% | 0.87 | -7.5% | 141 | 1.45 | 52.6% | 83.5 | 12/12 | 1.00 | 0.81 | 0.06 | 5 | 22.3% | 0.57 | 0.67 | 53.0% | 49.4% | 54.5% | 51.0%/33.8% | 10.4 (interpolated) | pass | 0.298 (unverified) | 0.88 |
| 86 | `cfg_3778` | timeframe=15min, ma_pair=EMA/SMA, fast_length=5, slow_length=60, confirm_bars=4, buffer_atr=0.0, stop_atr=1.5, slope_filter=True | 195/128 | 323 | 43.2% | 7.5% | 0.83 | -9.0% | 320 | 1.38 | 36.4% | 128.8 | 9/9 | 0.89 | 0.81 | 0.03 | 4 | 17.9% | 0.55 | 0.59 | 38.0% | 33.0% | 22.2% | 39.0%/27.1% | 5.9 (interpolated) | pass | 0.267 (unverified) | 0.63 |
| 87 | `cfg_6bb3` | timeframe=15min, ma_pair=EMA/EMA, fast_length=20, slow_length=40, confirm_bars=2, buffer_atr=0.1, stop_atr=1.5, slope_filter=False | 191/88 | 279 | 41.8% | 7.2% | 0.78 | -11.8% | 229 | 1.37 | 37.2% | 111.6 | 10/10 | 1.00 | 0.81 | -0.03 | 4 | 20.4% | 0.48 | 0.58 | 37.3% | 33.0% | 51.8% | 36.7%/27.1% | 6.5 (interpolated) | pass | 0.227 (unverified) | 1.27 |
| 88 | `cfg_846e` | timeframe=15min, ma_pair=EMA/EMA, fast_length=5, slow_length=40, confirm_bars=4, buffer_atr=0.5, stop_atr=3.0, slope_filter=False | 100/306 | 406 | 52.8% | 8.9% | 0.81 | -8.6% | 102 | 1.27 | 49.5% | 162.2 | 9/9 | 0.89 | 0.80 | 0.00 | 4 | 22.9% | 0.52 | 0.70 | 45.8% | 39.2% | 54.4% | 46.7%/33.7% | 5.6 (interpolated) | pass | 0.249 (unverified) | 1.12 |
| 89 | `cfg_5d0b` | timeframe=15min, ma_pair=EMA/SMA, fast_length=16, slow_length=60, confirm_bars=1, buffer_atr=0.1, stop_atr=1.5, slope_filter=False | 207/93 | 300 | 54.9% | 9.1% | 0.95 | -8.1% | 180 | 1.42 | 37.3% | 120.2 | 11/11 | 0.91 | 0.80 | 0.15 | 5 | 31.6% | 0.37 | 0.56 | 49.7% | 44.6% | 44.1% | 49.3%/37.4% | 7.4 (interpolated) | pass | 0.365 (unverified) | 0.91 |
| 90 | `cfg_3c65` | timeframe=15min, ma_pair=EMA/EMA, fast_length=16, slow_length=40, confirm_bars=4, buffer_atr=0.35, stop_atr=1.5, slope_filter=True | 185/93 | 278 | 42.9% | 7.4% | 0.79 | -10.4% | 191 | 1.37 | 36.9% | 111.0 | 10/10 | 1.00 | 0.80 | -0.01 | 4 | 16.0% | 0.59 | 0.69 | 38.4% | 34.1% | 43.4% | 39.9%/29.7% | 6.6 (interpolated) | pass | 0.239 (unverified) | 1.26 |
| 91 | `cfg_514d` | timeframe=15min, ma_pair=EMA/EMA, fast_length=16, slow_length=40, confirm_bars=3, buffer_atr=0.5, stop_atr=1.5, slope_filter=True | 166/92 | 258 | 45.6% | 7.8% | 0.88 | -8.7% | 165 | 1.45 | 35.0% | 103.4 | 10/10 | 1.00 | 0.80 | 0.08 | 5 | 21.6% | 0.48 | 0.65 | 41.4% | 37.3% | 18.5% | 40.9%/27.6% | 7.4 (interpolated) | pass | 0.301 (unverified) | 1.00 |
| 92 | `cfg_e12a` | timeframe=15min, ma_pair=EMA/SMA, fast_length=12, slow_length=60, confirm_bars=2, buffer_atr=0.35, stop_atr=1.5, slope_filter=False | 204/95 | 299 | 47.5% | 8.1% | 0.87 | -10.5% | 169 | 1.38 | 37.7% | 119.5 | 12/12 | 0.92 | 0.80 | 0.07 | 5 | 29.6% | 0.37 | 0.61 | 42.4% | 37.6% | 41.1% | 42.7%/34.2% | 6.7 (interpolated) | pass | 0.296 (unverified) | 0.95 |
| 93 | `cfg_6e2e` | timeframe=15min, ma_pair=EMA/EMA, fast_length=12, slow_length=100, confirm_bars=4, buffer_atr=0.0, stop_atr=3.0, slope_filter=False | 67/141 | 208 | 58.1% | 9.6% | 0.85 | -8.5% | 184 | 1.49 | 52.7% | 84.3 | 11/11 | 1.00 | 0.80 | 0.06 | 4 | 29.0% | 0.48 | 0.77 | 54.4% | 50.8% | 58.6% | 52.2%/42.6% | 10.6 (interpolated) | pass | 0.286 (unverified) | 0.63 |
| 94 | `cfg_92d4` | timeframe=5min, ma_pair=EMA/EMA, fast_length=16, slow_length=150, confirm_bars=3, buffer_atr=0.0, stop_atr=2.0, slope_filter=True | 296/174 | 470 | 56.8% | 9.4% | 0.87 | -14.9% | 112 | 1.36 | 42.2% | 186.2 | 10/10 | 1.00 | 0.79 | 0.08 | 5 | 38.5% | 0.31 | 0.71 | 48.6% | 40.8% | 67.9% | 51.5%/39.4% | 5.2 (interpolated) | pass | 0.300 (unverified) | 1.10 |
| 95 | `cfg_7fc7` | timeframe=15min, ma_pair=SMA/EMA, fast_length=8, slow_length=150, confirm_bars=2, buffer_atr=0.2, stop_atr=2.0, slope_filter=False | 106/87 | 193 | 62.0% | 10.1% | 1.00 | -7.9% | 126 | 1.61 | 51.4% | 77.8 | 12/12 | 1.00 | 0.79 | 0.21 | 5 | 37.5% | 0.36 | 0.67 | 58.4% | 55.0% | 29.4% | 55.3%/41.6% | 12.0 (interpolated) | pass | 0.407 (unverified) | 0.51 |
| 96 | `cfg_d685` | timeframe=15min, ma_pair=SMA/EMA, fast_length=20, slow_length=60, confirm_bars=3, buffer_atr=0.2, stop_atr=1.5, slope_filter=True | 165/61 | 226 | 48.7% | 8.3% | 0.87 | -10.8% | 242 | 1.46 | 35.2% | 91.2 | 11/11 | 1.00 | 0.79 | 0.08 | 4 | 10.4% | 0.79 | 0.83 | 45.0% | 41.3% | 47.7% | 44.5%/33.3% | 8.7 (interpolated) | pass | 0.293 (unverified) | 0.41 |
| 97 | `cfg_3d61` | timeframe=15min, ma_pair=EMA/SMA, fast_length=5, slow_length=60, confirm_bars=1, buffer_atr=0.1, stop_atr=2.5, slope_filter=True | 133/200 | 333 | 53.7% | 9.0% | 0.86 | -9.0% | 256 | 1.35 | 45.3% | 133.2 | 11/11 | 0.91 | 0.79 | 0.07 | 5 | 23.9% | 0.54 | 0.59 | 48.0% | 42.4% | 31.3% | 47.6%/37.5% | 6.7 (interpolated) | pass | 0.288 (unverified) | 0.77 |
| 98 | `cfg_c201` | timeframe=5min, ma_pair=EMA/EMA, fast_length=16, slow_length=150, confirm_bars=4, buffer_atr=0.1, stop_atr=1.5, slope_filter=True | 336/122 | 458 | 39.6% | 6.9% | 0.75 | -7.1% | 174 | 1.33 | 33.7% | 181.6 | 9/9 | 1.00 | 0.79 | -0.04 | 4 | 23.3% | 0.35 | 0.82 | 32.4% | 25.7% | 33.9% | 35.9%/26.0% | 4.2 (interpolated) | pass | 0.206 (unverified) | 0.77 |
| 99 | `cfg_d709` | timeframe=15min, ma_pair=EMA/EMA, fast_length=5, slow_length=150, confirm_bars=4, buffer_atr=0.35, stop_atr=2.0, slope_filter=False | 90/106 | 196 | 53.0% | 8.9% | 0.88 | -12.4% | 260 | 1.56 | 49.9% | 78.7 | 10/10 | 1.00 | 0.78 | 0.10 | 4 | 25.8% | 0.51 | 0.75 | 49.7% | 46.3% | 15.8% | 48.5%/37.4% | 10.5 (interpolated) | pass | 0.305 (unverified) | 0.74 |
| 100 | `cfg_2ac6` | timeframe=5min, ma_pair=EMA/EMA, fast_length=16, slow_length=80, confirm_bars=2, buffer_atr=0.35, stop_atr=None, slope_filter=True | 0/595 | 595 | 76.6% | 12.1% | 0.90 | -17.1% | 190 | 1.29 | 55.0% | 238.9 | 11/11 | 1.00 | 0.78 | 0.12 | 4 | 40.0% | 0.43 | 0.50 | 64.9% | 54.0% | 65.5% | 68.4%/49.4% | 5.2 (interpolated) | pass | 0.334 (unverified) | 0.71 |
| 101 | `cfg_561b` | timeframe=15min, ma_pair=EMA/EMA, fast_length=12, slow_length=60, confirm_bars=3, buffer_atr=0.35, stop_atr=1.5, slope_filter=True | 172/99 | 271 | 41.9% | 7.3% | 0.76 | -12.6% | 256 | 1.36 | 40.2% | 108.8 | 12/12 | 1.00 | 0.78 | -0.02 | 4 | 17.5% | 0.57 | 0.65 | 37.6% | 33.4% | 41.2% | 36.3%/28.4% | 6.7 (interpolated) | pass | 0.215 (unverified) | 0.94 |
| 102 | `cfg_b254` | timeframe=15min, ma_pair=EMA/EMA, fast_length=12, slow_length=100, confirm_bars=1, buffer_atr=0.1, stop_atr=1.5, slope_filter=False | 136/75 | 211 | 45.4% | 7.8% | 0.86 | -9.9% | 328 | 1.49 | 42.0% | 85.0 | 11/11 | 1.00 | 0.78 | 0.08 | 5 | 25.8% | 0.42 | 0.85 | 41.9% | 38.5% | 56.6% | 40.0%/28.2% | 8.8 (interpolated) | pass | 0.287 (unverified) | 0.99 |
| 103 | `cfg_1b7c` | timeframe=15min, ma_pair=SMA/SMA, fast_length=5, slow_length=60, confirm_bars=1, buffer_atr=0.35, stop_atr=2.5, slope_filter=False | 146/234 | 380 | 60.7% | 10.0% | 0.88 | -9.5% | 134 | 1.33 | 51.6% | 151.5 | 11/11 | 0.91 | 0.77 | 0.10 | 5 | 32.6% | 0.40 | 0.58 | 53.8% | 47.2% | 37.2% | 53.5%/37.3% | 6.5 (interpolated) | pass | 0.303 (unverified) | 0.95 |
| 104 | `cfg_6e04` | timeframe=15min, ma_pair=EMA/SMA, fast_length=5, slow_length=60, confirm_bars=2, buffer_atr=0.2, stop_atr=1.5, slope_filter=False | 234/147 | 381 | 55.5% | 9.2% | 0.88 | -8.6% | 109 | 1.37 | 43.5% | 152.2 | 11/11 | 0.91 | 0.77 | 0.12 | 5 | 37.3% | 0.28 | 0.54 | 48.8% | 42.5% | 38.2% | 50.6%/38.1% | 6.0 (interpolated) | pass | 0.308 (unverified) | 0.84 |
| 105 | `cfg_cde6` | timeframe=5min, ma_pair=EMA/EMA, fast_length=16, slow_length=150, confirm_bars=3, buffer_atr=0.5, stop_atr=1.5, slope_filter=True | 315/93 | 408 | 49.4% | 8.4% | 0.91 | -8.7% | 197 | 1.45 | 32.2% | 161.7 | 9/9 | 0.89 | 0.77 | 0.14 | 5 | 23.7% | 0.45 | 0.76 | 42.6% | 36.1% | 33.1% | 44.9%/32.8% | 5.3 (interpolated) | pass | 0.325 (unverified) | 0.61 |
| 106 | `cfg_1813` | timeframe=15min, ma_pair=SMA/SMA, fast_length=5, slow_length=150, confirm_bars=3, buffer_atr=0.5, stop_atr=1.5, slope_filter=True | 110/45 | 155 | 34.7% | 6.1% | 0.78 | -8.5% | 264 | 1.64 | 31.3% | 62.0 | 9/9 | 1.00 | 0.76 | 0.01 | 4 | 15.0% | 0.50 | 1.01 | 32.3% | 30.0% | 24.4% | 30.6%/21.4% | 9.4 (interpolated) | pass | 0.226 (unverified) | 0.76 |
| 107 | `cfg_438c` | timeframe=15min, ma_pair=SMA/EMA, fast_length=20, slow_length=60, confirm_bars=3, buffer_atr=0.35, stop_atr=1.5, slope_filter=False | 163/60 | 223 | 45.3% | 7.8% | 0.83 | -12.8% | 191 | 1.45 | 33.1% | 89.8 | 11/11 | 1.00 | 0.76 | 0.07 | 4 | 12.2% | 0.71 | 0.86 | 41.6% | 38.0% | 22.9% | 41.3%/29.2% | 8.3 (interpolated) | pass | 0.263 (unverified) | 0.44 |
| 108 | `cfg_9d61` | timeframe=15min, ma_pair=SMA/EMA, fast_length=20, slow_length=40, confirm_bars=2, buffer_atr=0.35, stop_atr=1.5, slope_filter=True | 180/78 | 258 | 51.0% | 8.6% | 1.00 | -9.8% | 294 | 1.49 | 33.5% | 103.5 | 10/10 | 0.90 | 0.76 | 0.24 | 4 | 16.8% | 0.60 | 0.74 | 46.5% | 42.2% | 32.3% | 45.6%/35.0% | 8.0 (interpolated) | pass | 0.406 (unverified) | 0.36 |
| 109 | `cfg_3258` | timeframe=15min, ma_pair=SMA/EMA, fast_length=12, slow_length=40, confirm_bars=3, buffer_atr=0.35, stop_atr=2.5, slope_filter=False | 156/174 | 330 | 47.0% | 8.0% | 0.76 | -9.5% | 218 | 1.29 | 46.8% | 132.0 | 12/12 | 0.83 | 0.75 | 0.01 | 5 | 27.3% | 0.38 | 0.62 | 41.5% | 36.2% | 44.7% | 41.1%/30.8% | 6.1 (interpolated) | pass | 0.221 (unverified) | 1.11 |
| 110 | `cfg_9444` | timeframe=15min, ma_pair=SMA/SMA, fast_length=12, slow_length=80, confirm_bars=3, buffer_atr=0.1, stop_atr=1.5, slope_filter=True | 153/71 | 224 | 36.9% | 6.5% | 0.75 | -8.5% | 330 | 1.41 | 33.6% | 89.9 | 12/12 | 1.00 | 0.75 | 0.01 | 4 | 15.4% | 0.52 | 0.84 | 33.4% | 30.0% | 27.8% | 34.2%/23.6% | 7.1 (interpolated) | pass | 0.211 (unverified) | 0.73 |
| 111 | `cfg_2f1d` | timeframe=15min, ma_pair=EMA/SMA, fast_length=5, slow_length=60, confirm_bars=2, buffer_atr=0.0, stop_atr=1.5, slope_filter=True | 192/145 | 337 | 46.6% | 8.0% | 0.88 | -9.3% | 366 | 1.39 | 38.1% | 134.4 | 10/10 | 0.80 | 0.75 | 0.14 | 5 | 28.8% | 0.35 | 0.53 | 41.0% | 35.7% | 23.5% | 41.4%/32.0% | 6.0 (interpolated) | pass | 0.307 (unverified) | 0.52 |
| 112 | `cfg_d004` | timeframe=15min, ma_pair=EMA/SMA, fast_length=5, slow_length=60, confirm_bars=4, buffer_atr=0.2, stop_atr=1.5, slope_filter=False | 221/140 | 361 | 56.6% | 9.4% | 0.93 | -7.7% | 167 | 1.41 | 41.3% | 143.8 | 10/10 | 0.90 | 0.74 | 0.19 | 5 | 28.3% | 0.42 | 0.54 | 50.3% | 44.2% | 30.1% | 49.4%/40.2% | 6.4 (interpolated) | pass | 0.347 (unverified) | 0.68 |
| 113 | `cfg_c12f` | timeframe=15min, ma_pair=EMA/SMA, fast_length=12, slow_length=40, confirm_bars=2, buffer_atr=0.1, stop_atr=None, slope_filter=False | 0/421 | 421 | 60.2% | 9.9% | 0.78 | -14.9% | 191 | 1.27 | 55.8% | 168.5 | 11/11 | 1.00 | 0.74 | 0.04 | 5 | 38.5% | 0.32 | 0.56 | 52.6% | 45.4% | 57.4% | 53.4%/37.8% | 5.9 (interpolated) | pass | 0.238 (unverified) | 0.79 |
| 114 | `cfg_8e9f` | timeframe=15min, ma_pair=EMA/SMA, fast_length=8, slow_length=60, confirm_bars=2, buffer_atr=0.35, stop_atr=1.5, slope_filter=False | 220/101 | 321 | 44.8% | 7.7% | 0.80 | -8.4% | 183 | 1.35 | 39.4% | 128.2 | 12/12 | 0.92 | 0.73 | 0.07 | 5 | 25.9% | 0.39 | 0.63 | 39.5% | 34.5% | 39.3% | 41.5%/30.1% | 6.0 (interpolated) | pass | 0.246 (unverified) | 0.87 |
| 115 | `cfg_0500` | timeframe=5min, ma_pair=SMA/EMA, fast_length=20, slow_length=150, confirm_bars=2, buffer_atr=0.1, stop_atr=2.0, slope_filter=True | 294/126 | 420 | 54.0% | 9.0% | 0.88 | -12.5% | 97 | 1.35 | 39.8% | 167.4 | 10/10 | 1.00 | 0.73 | 0.15 | 5 | 28.5% | 0.43 | 0.73 | 46.7% | 39.8% | 39.3% | 46.9%/38.4% | 5.5 (interpolated) | pass | 0.305 (unverified) | 0.72 |
| 116 | `cfg_5ee2` | timeframe=15min, ma_pair=EMA/SMA, fast_length=8, slow_length=100, confirm_bars=1, buffer_atr=0.1, stop_atr=3.0, slope_filter=True | 77/132 | 209 | 47.1% | 8.0% | 0.79 | -10.1% | 278 | 1.41 | 45.4% | 84.0 | 12/12 | 1.00 | 0.73 | 0.06 | 4 | 11.0% | 0.79 | 0.80 | 43.6% | 40.2% | 35.2% | 43.1%/31.1% | 9.1 (interpolated) | pass | 0.238 (unverified) | 0.58 |
| 117 | `cfg_77ad` | timeframe=15min, ma_pair=SMA/EMA, fast_length=20, slow_length=40, confirm_bars=2, buffer_atr=0.1, stop_atr=1.5, slope_filter=True | 201/90 | 291 | 41.9% | 7.3% | 0.81 | -9.8% | 191 | 1.35 | 36.0% | 116.4 | 10/10 | 0.90 | 0.73 | 0.09 | 4 | 18.7% | 0.50 | 0.80 | 37.2% | 32.7% | 41.6% | 37.9%/28.9% | 6.2 (interpolated) | pass | 0.265 (unverified) | 0.53 |
| 118 | `cfg_6e85` | timeframe=15min, ma_pair=SMA/SMA, fast_length=20, slow_length=60, confirm_bars=1, buffer_atr=0.2, stop_atr=2.0, slope_filter=False | 179/103 | 282 | 45.6% | 7.8% | 0.80 | -14.0% | 191 | 1.33 | 39.1% | 112.6 | 11/11 | 0.91 | 0.73 | 0.07 | 5 | 25.1% | 0.41 | 0.72 | 41.0% | 36.5% | 51.8% | 41.2%/28.5% | 6.8 (interpolated) | pass | 0.244 (unverified) | 0.88 |
| 119 | `cfg_b3d5` | timeframe=15min, ma_pair=EMA/SMA, fast_length=20, slow_length=40, confirm_bars=3, buffer_atr=0.5, stop_atr=1.5, slope_filter=False | 227/127 | 354 | 42.1% | 7.3% | 0.81 | -11.4% | 203 | 1.32 | 34.2% | 141.6 | 9/9 | 0.78 | 0.72 | 0.09 | 5 | 25.2% | 0.37 | 0.69 | 36.5% | 31.0% | 48.4% | 36.6%/27.2% | 5.4 (interpolated) | pass | 0.252 (unverified) | 0.99 |
| 120 | `cfg_7792` | timeframe=15min, ma_pair=SMA/SMA, fast_length=20, slow_length=60, confirm_bars=4, buffer_atr=0.5, stop_atr=1.5, slope_filter=True | 176/74 | 250 | 44.8% | 7.7% | 0.85 | -7.6% | 277 | 1.43 | 30.0% | 100.0 | 9/9 | 0.89 | 0.72 | 0.13 | 4 | 8.7% | 0.80 | 0.82 | 40.8% | 36.7% | 33.7% | 40.6%/30.3% | 7.5 (interpolated) | pass | 0.281 (unverified) | 0.40 |
| 121 | `cfg_38ce` | timeframe=15min, ma_pair=EMA/SMA, fast_length=20, slow_length=60, confirm_bars=4, buffer_atr=0.0, stop_atr=1.5, slope_filter=True | 174/83 | 257 | 37.9% | 6.6% | 0.80 | -13.4% | 330 | 1.34 | 32.6% | 102.8 | 9/9 | 0.89 | 0.72 | 0.08 | 4 | 18.9% | 0.51 | 0.78 | 33.8% | 30.0% | 12.9% | 33.6%/23.0% | 6.5 (interpolated) | pass | 0.242 (unverified) | 0.58 |
| 122 | `cfg_5846` | timeframe=15min, ma_pair=SMA/SMA, fast_length=12, slow_length=60, confirm_bars=3, buffer_atr=0.1, stop_atr=1.5, slope_filter=False | 212/106 | 318 | 44.0% | 7.6% | 0.83 | -11.0% | 178 | 1.34 | 38.1% | 127.3 | 12/12 | 0.92 | 0.72 | 0.11 | 5 | 26.3% | 0.39 | 0.63 | 38.8% | 33.8% | 31.7% | 39.6%/28.0% | 6.0 (interpolated) | pass | 0.268 (unverified) | 0.72 |
| 123 | `cfg_133c` | timeframe=15min, ma_pair=SMA/SMA, fast_length=5, slow_length=150, confirm_bars=3, buffer_atr=0.5, stop_atr=2.0, slope_filter=False | 106/77 | 183 | 45.0% | 7.7% | 0.76 | -10.5% | 290 | 1.47 | 43.4% | 73.2 | 10/10 | 1.00 | 0.71 | 0.05 | 4 | 21.8% | 0.49 | 0.89 | 41.9% | 39.0% | 27.9% | 39.9%/29.2% | 9.9 (interpolated) | pass | 0.218 (unverified) | 0.78 |
| 124 | `cfg_3f80` | timeframe=15min, ma_pair=EMA/EMA, fast_length=16, slow_length=60, confirm_bars=4, buffer_atr=0.35, stop_atr=1.5, slope_filter=True | 155/74 | 229 | 41.0% | 7.1% | 0.84 | -7.8% | 222 | 1.41 | 37.2% | 92.3 | 11/11 | 0.91 | 0.71 | 0.14 | 4 | 23.2% | 0.36 | 0.77 | 37.4% | 33.9% | 36.7% | 36.8%/25.6% | 7.6 (interpolated) | pass | 0.286 (unverified) | 0.88 |
| 125 | `cfg_2505` | timeframe=15min, ma_pair=EMA/SMA, fast_length=12, slow_length=100, confirm_bars=2, buffer_atr=0.1, stop_atr=1.5, slope_filter=False | 155/71 | 226 | 53.3% | 8.9% | 0.99 | -7.1% | 192 | 1.52 | 39.7% | 91.4 | 12/12 | 0.92 | 0.71 | 0.28 | 4 | 34.4% | 0.36 | 0.79 | 49.4% | 45.6% | 31.9% | 46.8%/35.3% | 9.3 (interpolated) | pass | 0.395 (unverified) | 0.48 |
| 126 | `cfg_6aca` | timeframe=15min, ma_pair=SMA/EMA, fast_length=12, slow_length=40, confirm_bars=4, buffer_atr=0.1, stop_atr=2.5, slope_filter=True | 156/196 | 352 | 49.1% | 8.3% | 0.76 | -12.1% | 194 | 1.30 | 47.8% | 140.8 | 11/11 | 0.91 | 0.70 | 0.05 | 5 | 26.7% | 0.40 | 0.62 | 43.2% | 37.6% | 49.1% | 43.5%/31.1% | 6.0 (interpolated) | pass | 0.220 (unverified) | 0.86 |
| 127 | `cfg_ec3a` | timeframe=15min, ma_pair=SMA/SMA, fast_length=12, slow_length=60, confirm_bars=4, buffer_atr=0.5, stop_atr=2.0, slope_filter=False | 174/117 | 291 | 44.6% | 7.7% | 0.77 | -8.9% | 165 | 1.33 | 40.0% | 116.1 | 11/11 | 0.82 | 0.70 | 0.07 | 5 | 26.0% | 0.37 | 0.65 | 39.8% | 35.2% | 37.8% | 41.9%/28.0% | 6.5 (interpolated) | pass | 0.224 (unverified) | 1.03 |
| 128 | `cfg_9d7d` | timeframe=15min, ma_pair=EMA/SMA, fast_length=8, slow_length=150, confirm_bars=4, buffer_atr=0.2, stop_atr=1.5, slope_filter=False | 111/55 | 166 | 43.0% | 7.4% | 0.79 | -9.8% | 328 | 1.61 | 35.3% | 66.3 | 10/10 | 1.00 | 0.68 | 0.11 | 4 | 12.2% | 0.71 | 0.91 | 40.2% | 37.6% | 21.2% | 39.2%/28.0% | 10.4 (interpolated) | pass | 0.239 (unverified) | 0.54 |
| 129 | `cfg_4876` | timeframe=15min, ma_pair=EMA/SMA, fast_length=16, slow_length=100, confirm_bars=2, buffer_atr=0.2, stop_atr=1.5, slope_filter=False | 143/58 | 201 | 38.3% | 6.7% | 0.83 | -11.4% | 229 | 1.41 | 35.8% | 81.3 | 12/12 | 0.92 | 0.68 | 0.15 | 4 | 15.4% | 0.62 | 1.13 | 35.2% | 32.1% | 27.6% | 34.8%/23.8% | 8.1 (interpolated) | pass | 0.269 (unverified) | 0.60 |
| 130 | `cfg_6ce9` | timeframe=15min, ma_pair=EMA/SMA, fast_length=16, slow_length=40, confirm_bars=3, buffer_atr=0.5, stop_atr=2.5, slope_filter=False | 164/197 | 361 | 51.6% | 8.7% | 0.82 | -8.4% | 188 | 1.30 | 43.1% | 144.2 | 11/11 | 0.91 | 0.68 | 0.14 | 5 | 28.2% | 0.38 | 0.61 | 45.4% | 39.5% | 48.7% | 45.0%/34.6% | 6.0 (interpolated) | pass | 0.261 (unverified) | 0.84 |
| 131 | `cfg_92bd` | timeframe=15min, ma_pair=EMA/EMA, fast_length=16, slow_length=40, confirm_bars=2, buffer_atr=0.1, stop_atr=1.5, slope_filter=True | 203/109 | 312 | 58.7% | 9.7% | 0.98 | -8.0% | 134 | 1.45 | 41.2% | 124.8 | 11/11 | 1.00 | 0.68 | 0.30 | 4 | 32.1% | 0.44 | 0.57 | 53.1% | 47.7% | 46.2% | 52.9%/40.9% | 7.5 (interpolated) | pass | 0.387 (unverified) | 0.94 |
| 132 | `cfg_051b` | timeframe=15min, ma_pair=EMA/EMA, fast_length=8, slow_length=150, confirm_bars=2, buffer_atr=0.35, stop_atr=1.5, slope_filter=True | 124/56 | 180 | 39.1% | 6.8% | 0.76 | -8.5% | 214 | 1.49 | 42.4% | 72.2 | 11/11 | 1.00 | 0.68 | 0.09 | 4 | 25.4% | 0.36 | 0.92 | 36.2% | 33.4% | 32.9% | 34.4%/25.4% | 9.0 (interpolated) | pass | 0.219 (unverified) | 0.65 |
| 133 | `cfg_4ffe` | timeframe=15min, ma_pair=SMA/SMA, fast_length=20, slow_length=80, confirm_bars=4, buffer_atr=0.1, stop_atr=1.5, slope_filter=True | 137/63 | 200 | 42.0% | 7.3% | 0.86 | -9.2% | 311 | 1.49 | 31.9% | 80.8 | 10/10 | 0.90 | 0.68 | 0.19 | 4 | 11.3% | 0.71 | 0.89 | 38.7% | 35.6% | 52.5% | 37.1%/26.8% | 8.7 (interpolated) | pass | 0.287 (unverified) | 0.53 |
| 134 | `cfg_f951` | timeframe=15min, ma_pair=SMA/EMA, fast_length=20, slow_length=60, confirm_bars=1, buffer_atr=0.0, stop_atr=2.0, slope_filter=False | 153/105 | 258 | 52.4% | 8.8% | 0.85 | -13.7% | 229 | 1.36 | 44.7% | 103.8 | 10/10 | 1.00 | 0.67 | 0.18 | 4 | 23.6% | 0.56 | 0.86 | 48.1% | 43.7% | 42.8% | 46.2%/34.9% | 8.1 (interpolated) | pass | 0.281 (unverified) | 0.79 |
| 135 | `cfg_baf9` | timeframe=5min, ma_pair=SMA/SMA, fast_length=20, slow_length=150, confirm_bars=2, buffer_atr=0.1, stop_atr=2.0, slope_filter=False | 309/129 | 438 | 44.9% | 7.7% | 0.79 | -10.3% | 257 | 1.33 | 36.1% | 174.6 | 10/10 | 1.00 | 0.66 | 0.13 | 5 | 29.9% | 0.29 | 0.66 | 37.8% | 31.0% | 37.4% | 39.6%/28.6% | 4.7 (interpolated) | pass | 0.239 (unverified) | 0.68 |
| 136 | `cfg_e1c8` | timeframe=15min, ma_pair=SMA/SMA, fast_length=16, slow_length=60, confirm_bars=3, buffer_atr=0.35, stop_atr=2.0, slope_filter=False | 170/115 | 285 | 43.3% | 7.5% | 0.76 | -16.0% | 137 | 1.32 | 40.0% | 113.7 | 13/13 | 0.92 | 0.62 | 0.13 | 5 | 31.0% | 0.27 | 0.63 | 38.6% | 34.2% | 37.6% | 40.1%/27.6% | 6.5 (interpolated) | pass | 0.218 (unverified) | 0.99 |
| 137 | `cfg_a570` | timeframe=15min, ma_pair=SMA/SMA, fast_length=12, slow_length=100, confirm_bars=4, buffer_atr=0.1, stop_atr=2.0, slope_filter=False | 139/83 | 222 | 42.9% | 7.4% | 0.82 | -7.0% | 168 | 1.38 | 41.0% | 89.7 | 12/12 | 1.00 | 0.61 | 0.20 | 4 | 24.3% | 0.40 | 0.92 | 39.3% | 35.8% | 34.4% | 37.6%/25.6% | 8.0 (interpolated) | pass | 0.268 (unverified) | 0.64 |
| 138 | `cfg_1d30` | timeframe=5min, ma_pair=EMA/SMA, fast_length=16, slow_length=150, confirm_bars=4, buffer_atr=0.2, stop_atr=2.0, slope_filter=False | 302/140 | 442 | 46.0% | 7.9% | 0.80 | -10.2% | 258 | 1.33 | 37.2% | 176.5 | 10/10 | 1.00 | 0.61 | 0.19 | 5 | 34.7% | 0.24 | 0.65 | 38.7% | 31.8% | 49.7% | 40.9%/29.5% | 4.8 (interpolated) | pass | 0.245 (unverified) | 0.93 |
| 139 | `cfg_42b2` | timeframe=15min, ma_pair=EMA/SMA, fast_length=20, slow_length=40, confirm_bars=3, buffer_atr=0.5, stop_atr=1.5, slope_filter=True | 223/120 | 343 | 40.8% | 7.1% | 0.81 | -10.8% | 200 | 1.33 | 32.4% | 136.9 | 9/9 | 0.78 | 0.59 | 0.22 | 5 | 17.2% | 0.53 | 0.73 | 35.3% | 30.1% | 45.6% | 36.3%/27.1% | 5.4 (interpolated) | pass | 0.252 (unverified) | 0.93 |
| 140 | `cfg_5fc5` | timeframe=15min, ma_pair=SMA/SMA, fast_length=20, slow_length=40, confirm_bars=1, buffer_atr=0.0, stop_atr=1.5, slope_filter=False | 263/155 | 418 | 47.1% | 8.0% | 0.76 | -14.9% | 191 | 1.29 | 40.1% | 166.9 | 8/8 | 0.88 | 0.56 | 0.20 | 5 | 29.9% | 0.35 | 0.67 | 40.2% | 33.7% | 27.0% | 42.3%/28.7% | 5.1 (interpolated) | pass | 0.225 (unverified) | 0.97 |
| 141 | `cfg_63db` | timeframe=15min, ma_pair=SMA/SMA, fast_length=12, slow_length=40, confirm_bars=2, buffer_atr=0.2, stop_atr=1.5, slope_filter=False | 262/154 | 416 | 44.4% | 7.6% | 0.75 | -12.8% | 126 | 1.28 | 39.2% | 166.1 | 11/11 | 0.91 | 0.42 | 0.33 | 5 | 29.5% | 0.32 | 0.67 | 37.6% | 31.2% | 27.3% | 40.2%/26.9% | 4.9 (interpolated) | pass | 0.216 (unverified) | 0.60 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 7.2% / 0.88 / 42 | 17.7% / 1.94 / 47 | 31.1% / 1.68 / 44 | 13.6% / 1.50 / 47 | -1.7% / -0.05 / 59 |
| 2 | 9.9% / 1.46 / 73 | 7.8% / 1.12 / 87 | 10.3% / 0.92 / 80 | 5.9% / 0.89 / 87 | 18.0% / 1.44 / 76 |
| 3 | 5.6% / 0.67 / 89 | 6.6% / 0.78 / 102 | 30.2% / 1.61 / 95 | 18.5% / 2.00 / 89 | 6.6% / 0.52 / 86 |
| 4 | 5.2% / 0.62 / 84 | 8.3% / 0.95 / 94 | 37.5% / 1.93 / 87 | 18.7% / 2.03 / 80 | 4.1% / 0.35 / 79 |
| 5 | 11.0% / 1.31 / 106 | 13.4% / 1.51 / 123 | 32.0% / 1.83 / 127 | 10.4% / 1.23 / 130 | 3.1% / 0.29 / 102 |
| 6 | 6.3% / 0.90 / 67 | 14.3% / 1.74 / 71 | 20.0% / 1.41 / 64 | 16.9% / 2.14 / 63 | 2.4% / 0.25 / 72 |
| 7 | 5.6% / 0.76 / 47 | 18.4% / 2.26 / 50 | 19.4% / 1.19 / 47 | 12.5% / 1.52 / 51 | 1.5% / 0.18 / 60 |
| 8 | 4.6% / 0.69 / 43 | 13.1% / 1.65 / 48 | 29.8% / 1.71 / 43 | 11.9% / 1.47 / 47 | 1.4% / 0.17 / 59 |
| 9 | 4.7% / 0.70 / 63 | 7.5% / 1.02 / 63 | 29.2% / 1.82 / 57 | 13.8% / 1.86 / 62 | 7.7% / 0.68 / 63 |
| 10 | 6.7% / 0.82 / 36 | 21.6% / 2.35 / 36 | 31.9% / 1.77 / 37 | 8.8% / 1.01 / 43 | -2.7% / -0.12 / 43 |
| 11 | 8.0% / 0.98 / 39 | 17.9% / 1.97 / 43 | 28.1% / 1.55 / 43 | 10.5% / 1.19 / 46 | 1.1% / 0.15 / 52 |
| 12 | 3.2% / 0.51 / 49 | 15.5% / 2.06 / 56 | 22.9% / 1.44 / 48 | 9.3% / 1.33 / 52 | -4.9% / -0.39 / 60 |
| 13 | 7.8% / 1.30 / 72 | 6.5% / 1.13 / 86 | 9.4% / 0.90 / 80 | 1.6% / 0.32 / 87 | 15.4% / 1.33 / 75 |
| 14 | 3.5% / 0.53 / 44 | 17.6% / 2.10 / 52 | 18.9% / 1.26 / 45 | 14.7% / 1.76 / 49 | 1.6% / 0.18 / 61 |
| 15 | -0.1% / 0.01 / 57 | 11.9% / 1.69 / 60 | 34.3% / 2.03 / 55 | 7.2% / 1.06 / 60 | 6.3% / 0.59 / 62 |
| 16 | 15.9% / 1.95 / 101 | 7.1% / 0.91 / 118 | 22.0% / 1.37 / 123 | 1.9% / 0.28 / 128 | 8.0% / 0.64 / 101 |
| 17 | 5.6% / 0.80 / 65 | 10.1% / 1.25 / 71 | 15.6% / 1.10 / 62 | 13.4% / 1.76 / 59 | 5.8% / 0.50 / 72 |
| 18 | 13.6% / 1.51 / 119 | 6.1% / 0.72 / 129 | 13.8% / 0.79 / 136 | 18.3% / 2.04 / 124 | 10.5% / 0.76 / 112 |
| 19 | 5.9% / 0.79 / 77 | 10.5% / 1.36 / 75 | 11.0% / 0.79 / 71 | 14.5% / 1.80 / 71 | 11.0% / 0.88 / 70 |
| 20 | 3.0% / 0.49 / 44 | 14.8% / 2.01 / 52 | 22.2% / 1.46 / 45 | 10.6% / 1.44 / 49 | 1.7% / 0.20 / 61 |
| 21 | 4.0% / 0.55 / 57 | 9.6% / 1.23 / 60 | 34.7% / 2.02 / 55 | 10.2% / 1.32 / 60 | 2.6% / 0.27 / 62 |
| 22 | 4.8% / 0.64 / 62 | 9.6% / 1.23 / 62 | 27.1% / 1.61 / 57 | 11.1% / 1.44 / 62 | 4.2% / 0.40 / 62 |
| 23 | 6.8% / 0.92 / 77 | 8.7% / 1.09 / 86 | 27.2% / 1.66 / 80 | 9.2% / 1.22 / 76 | 3.4% / 0.33 / 79 |
| 24 | 4.8% / 0.63 / 60 | 14.8% / 1.83 / 66 | 29.4% / 1.69 / 53 | 13.6% / 1.66 / 57 | -1.4% / -0.04 / 75 |
| 25 | 3.2% / 0.47 / 84 | 6.7% / 0.89 / 97 | 29.2% / 1.83 / 93 | 11.3% / 1.45 / 83 | 4.2% / 0.40 / 88 |
| 26 | 6.7% / 1.14 / 73 | 7.5% / 1.20 / 87 | 12.2% / 1.12 / 80 | 0.2% / 0.06 / 87 | 17.8% / 1.51 / 76 |
| 27 | 3.1% / 0.47 / 63 | 9.5% / 1.27 / 70 | 23.9% / 1.47 / 62 | 11.9% / 1.59 / 59 | 4.1% / 0.39 / 69 |
| 28 | 1.6% / 0.27 / 43 | 14.6% / 1.95 / 48 | 32.4% / 1.85 / 43 | 4.6% / 0.69 / 47 | 2.4% / 0.25 / 59 |
| 29 | 7.5% / 0.91 / 56 | 13.1% / 1.82 / 56 | 17.6% / 1.23 / 49 | 13.4% / 1.84 / 55 | 1.2% / 0.16 / 55 |
| 30 | 3.2% / 0.43 / 34 | 19.0% / 2.06 / 34 | 36.3% / 2.00 / 33 | 6.8% / 0.81 / 38 | -5.9% / -0.37 / 36 |
| 31 | 1.2% / 0.20 / 69 | 7.6% / 0.96 / 74 | 36.4% / 2.11 / 65 | 10.6% / 1.31 / 78 | -1.3% / -0.05 / 64 |
| 32 | 8.5% / 1.12 / 47 | 3.5% / 0.53 / 55 | 27.5% / 1.83 / 49 | 4.2% / 0.64 / 55 | 4.0% / 0.39 / 50 |
| 33 | 4.3% / 0.68 / 47 | 5.9% / 0.93 / 55 | 32.3% / 2.14 / 49 | 4.9% / 0.81 / 55 | -0.7% / -0.01 / 50 |
| 34 | 6.7% / 0.87 / 37 | 18.3% / 2.23 / 40 | 22.5% / 1.35 / 40 | 8.0% / 1.03 / 44 | -1.1% / -0.02 / 50 |
| 35 | 2.6% / 0.39 / 58 | 8.0% / 1.06 / 62 | 30.5% / 1.86 / 56 | 11.2% / 1.48 / 62 | 4.0% / 0.39 / 58 |
| 36 | 10.1% / 1.17 / 55 | 12.9% / 1.81 / 55 | 12.9% / 0.93 / 48 | 14.0% / 1.92 / 53 | 0.3% / 0.08 / 54 |
| 37 | 10.2% / 1.18 / 60 | 11.5% / 1.46 / 71 | 31.6% / 1.82 / 63 | 3.8% / 0.50 / 72 | 3.1% / 0.29 / 61 |
| 38 | 4.1% / 0.66 / 48 | 5.4% / 0.86 / 56 | 31.0% / 2.06 / 50 | 4.6% / 0.76 / 57 | 4.8% / 0.49 / 51 |
| 39 | 17.7% / 2.26 / 98 | 7.2% / 0.95 / 111 | 12.1% / 0.97 / 119 | 3.6% / 0.52 / 124 | 10.8% / 0.87 / 99 |
| 40 | 3.9% / 0.47 / 81 | 6.9% / 0.80 / 89 | 21.3% / 1.24 / 91 | 18.7% / 2.05 / 78 | 1.6% / 0.18 / 80 |
| 41 | 5.0% / 0.57 / 68 | 13.5% / 1.54 / 63 | 31.5% / 1.67 / 59 | 10.9% / 1.24 / 64 | 2.5% / 0.24 / 64 |
| 42 | 3.3% / 0.49 / 39 | 19.6% / 2.46 / 43 | 17.3% / 1.27 / 41 | 10.9% / 1.44 / 48 | 0.0% / 0.06 / 54 |
| 43 | 5.5% / 0.95 / 76 | 9.4% / 1.52 / 86 | 13.6% / 1.19 / 92 | -0.4% / -0.05 / 89 | 14.1% / 1.24 / 79 |
| 44 | 4.5% / 0.68 / 58 | 5.1% / 0.76 / 62 | 25.5% / 1.65 / 56 | 14.5% / 1.95 / 62 | 1.5% / 0.19 / 58 |
| 45 | -1.2% / -0.17 / 37 | 11.1% / 1.70 / 46 | 25.0% / 1.89 / 46 | 16.9% / 2.16 / 47 | -0.2% / 0.04 / 54 |
| 46 | 4.4% / 0.55 / 59 | 12.3% / 1.41 / 62 | 29.2% / 1.67 / 56 | 11.2% / 1.28 / 60 | -2.1% / -0.08 / 62 |
| 47 | 7.2% / 0.95 / 68 | 15.6% / 1.88 / 63 | 9.0% / 0.72 / 59 | 11.5% / 1.50 / 64 | 10.5% / 0.85 / 64 |
| 48 | 7.0% / 0.87 / 53 | 7.0% / 0.92 / 60 | 22.2% / 1.40 / 51 | 10.1% / 1.33 / 57 | 3.7% / 0.33 / 57 |
| 49 | 4.3% / 0.66 / 37 | 10.8% / 1.49 / 46 | 32.7% / 1.98 / 46 | 14.9% / 1.85 / 47 | -4.3% / -0.28 / 54 |
| 50 | 3.4% / 0.54 / 37 | 11.6% / 1.57 / 48 | 29.9% / 1.76 / 50 | 7.9% / 1.07 / 50 | -1.6% / -0.06 / 55 |
| 51 | 5.7% / 0.84 / 45 | 9.0% / 1.18 / 53 | 19.7% / 1.33 / 45 | 16.9% / 2.05 / 49 | -3.0% / -0.18 / 62 |
| 52 | 7.9% / 1.16 / 49 | 17.5% / 2.30 / 52 | 9.9% / 0.71 / 53 | 15.1% / 1.92 / 51 | -3.3% / -0.23 / 63 |
| 53 | 5.7% / 0.67 / 56 | 12.4% / 1.58 / 57 | 26.0% / 1.54 / 50 | 13.1% / 1.70 / 58 | -4.5% / -0.26 / 56 |
| 54 | 2.7% / 0.44 / 47 | 11.8% / 1.75 / 51 | 19.8% / 1.32 / 51 | 6.4% / 0.95 / 50 | 2.8% / 0.30 / 58 |
| 55 | 2.4% / 0.34 / 70 | 6.7% / 0.83 / 75 | 28.1% / 1.74 / 66 | 10.7% / 1.29 / 78 | 2.9% / 0.29 / 65 |
| 56 | 2.0% / 0.31 / 63 | 6.1% / 0.84 / 68 | 13.3% / 0.97 / 58 | 13.0% / 1.82 / 66 | 6.6% / 0.61 / 61 |
| 57 | 2.4% / 0.38 / 52 | 11.9% / 1.60 / 59 | 21.5% / 1.50 / 49 | 7.0% / 1.05 / 55 | 1.3% / 0.17 / 56 |
| 58 | 5.4% / 0.70 / 48 | 6.4% / 1.07 / 53 | 25.1% / 1.57 / 51 | 12.2% / 1.64 / 55 | -2.0% / -0.14 / 51 |
| 59 | 4.5% / 0.66 / 57 | 14.0% / 2.05 / 57 | 14.5% / 1.24 / 52 | 10.0% / 1.50 / 61 | -2.6% / -0.20 / 58 |
| 60 | 9.1% / 1.20 / 38 | 13.4% / 1.67 / 45 | 21.1% / 1.49 / 47 | 10.8% / 1.40 / 46 | -2.5% / -0.13 / 55 |
| 61 | 5.3% / 0.83 / 46 | 7.6% / 1.17 / 53 | 23.5% / 1.67 / 47 | 5.1% / 0.84 / 56 | 6.2% / 0.60 / 51 |
| 62 | 8.9% / 1.14 / 39 | 14.0% / 1.79 / 45 | 18.0% / 1.22 / 43 | 15.2% / 1.88 / 46 | -4.5% / -0.29 / 53 |
| 63 | 4.3% / 0.50 / 69 | 8.9% / 1.05 / 82 | 29.4% / 1.62 / 76 | 11.6% / 1.31 / 81 | 1.8% / 0.19 / 71 |
| 64 | 3.9% / 0.61 / 33 | 21.0% / 2.50 / 32 | 23.8% / 1.49 / 32 | 5.4% / 0.75 / 35 | -1.2% / -0.05 / 35 |
| 65 | 10.4% / 1.27 / 53 | 7.7% / 1.12 / 59 | 11.6% / 1.05 / 50 | 8.0% / 1.18 / 54 | 0.4% / 0.09 / 56 |
| 66 | 2.6% / 0.39 / 38 | 20.5% / 2.58 / 45 | 13.8% / 1.15 / 40 | 6.8% / 0.96 / 46 | 2.0% / 0.22 / 50 |
| 67 | 10.5% / 1.25 / 42 | 6.7% / 1.06 / 43 | 29.0% / 1.70 / 44 | 16.1% / 2.10 / 45 | -6.0% / -0.52 / 49 |
| 68 | 16.1% / 1.98 / 100 | 6.4% / 0.82 / 116 | 11.6% / 0.80 / 125 | 2.5% / 0.36 / 127 | 7.4% / 0.61 / 101 |
| 69 | 3.7% / 0.44 / 94 | 9.2% / 1.04 / 102 | 15.8% / 0.90 / 99 | 16.2% / 1.74 / 90 | 1.7% / 0.19 / 88 |
| 70 | 7.9% / 0.97 / 47 | 12.5% / 1.59 / 56 | 26.9% / 1.59 / 47 | 8.9% / 1.18 / 52 | -3.0% / -0.15 / 55 |
| 71 | 8.0% / 1.14 / 57 | 12.9% / 1.66 / 61 | 12.7% / 0.99 / 52 | 13.6% / 1.80 / 62 | 0.9% / 0.14 / 58 |
| 72 | 5.8% / 0.83 / 65 | 9.4% / 1.30 / 70 | 14.0% / 1.03 / 62 | 10.5% / 1.48 / 69 | -2.4% / -0.16 / 68 |
| 73 | 5.4% / 0.64 / 86 | 7.8% / 0.89 / 85 | 17.3% / 1.08 / 79 | 17.2% / 1.92 / 66 | 3.1% / 0.29 / 85 |
| 74 | 2.8% / 0.45 / 43 | 19.0% / 2.49 / 49 | 12.0% / 0.94 / 51 | 14.7% / 1.84 / 48 | 0.1% / 0.07 / 57 |
| 75 | 7.8% / 1.03 / 39 | 15.6% / 1.95 / 43 | 13.7% / 0.97 / 43 | 7.3% / 0.95 / 46 | 4.2% / 0.38 / 52 |
| 76 | 4.4% / 0.61 / 39 | 17.2% / 2.06 / 42 | 16.0% / 1.14 / 41 | 6.5% / 0.84 / 49 | -2.0% / -0.11 / 54 |
| 77 | 1.1% / 0.20 / 52 | 20.0% / 2.39 / 53 | 18.6% / 1.10 / 53 | 11.2% / 1.33 / 51 | -0.3% / 0.05 / 64 |
| 78 | 0.6% / 0.12 / 61 | 9.5% / 1.16 / 71 | 23.2% / 1.32 / 60 | 13.7% / 1.63 / 53 | -1.0% / -0.01 / 72 |
| 79 | 5.1% / 0.73 / 39 | 17.5% / 2.39 / 43 | 15.0% / 1.07 / 43 | 1.4% / 0.25 / 46 | 4.3% / 0.41 / 52 |
| 80 | 4.7% / 0.71 / 45 | 18.0% / 2.19 / 47 | 13.0% / 0.86 / 52 | 13.9% / 1.72 / 48 | -0.1% / 0.06 / 60 |
| 81 | 5.9% / 0.81 / 98 | 9.5% / 1.16 / 108 | 17.2% / 1.08 / 104 | 8.3% / 1.18 / 96 | 6.1% / 0.54 / 95 |
| 82 | 3.1% / 0.51 / 38 | 21.5% / 2.78 / 45 | 6.5% / 0.52 / 49 | 5.8% / 0.88 / 44 | -0.5% / 0.02 / 56 |
| 83 | 6.4% / 0.85 / 35 | 18.6% / 2.25 / 36 | 17.1% / 1.21 / 36 | 7.2% / 0.92 / 43 | -0.7% / 0.01 / 43 |
| 84 | 2.6% / 0.41 / 58 | 11.8% / 1.64 / 60 | 19.6% / 1.45 / 55 | 8.9% / 1.32 / 62 | -0.6% / 0.01 / 64 |
| 85 | 9.0% / 1.13 / 33 | 5.6% / 0.77 / 47 | 28.2% / 1.65 / 42 | 5.6% / 0.72 / 42 | 0.6% / 0.11 / 44 |
| 86 | 6.9% / 1.04 / 59 | 3.1% / 0.49 / 71 | 21.5% / 1.63 / 63 | -1.5% / -0.25 / 70 | 8.6% / 0.75 / 60 |
| 87 | 3.6% / 0.56 / 53 | 8.6% / 1.30 / 60 | 17.8% / 1.23 / 51 | 8.8% / 1.31 / 57 | -1.6% / -0.09 / 58 |
| 88 | 4.8% / 0.59 / 77 | 8.2% / 0.98 / 80 | 24.3% / 1.48 / 85 | 8.6% / 1.02 / 88 | -0.2% / 0.05 / 76 |
| 89 | 4.0% / 0.61 / 57 | 9.7% / 1.38 / 60 | 17.7% / 1.28 / 57 | 9.4% / 1.34 / 62 | 5.5% / 0.50 / 64 |
| 90 | 1.6% / 0.28 / 54 | 7.8% / 1.17 / 58 | 23.3% / 1.51 / 54 | 7.8% / 1.14 / 56 | -1.7% / -0.11 / 56 |
| 91 | 2.6% / 0.45 / 49 | 8.4% / 1.35 / 52 | 19.7% / 1.41 / 51 | 9.3% / 1.42 / 53 | 0.1% / 0.06 / 53 |
| 92 | 5.1% / 0.74 / 57 | 6.9% / 1.00 / 63 | 12.2% / 0.94 / 57 | 13.8% / 1.87 / 60 | 2.9% / 0.31 / 62 |
| 93 | 3.5% / 0.48 / 35 | 18.6% / 2.18 / 40 | 22.5% / 1.32 / 40 | 7.5% / 0.93 / 44 | -2.2% / -0.09 / 49 |
| 94 | 3.9% / 0.58 / 93 | 10.6% / 1.36 / 104 | 14.3% / 0.86 / 95 | 13.2% / 1.68 / 87 | 5.5% / 0.49 / 91 |
| 95 | 5.0% / 0.67 / 34 | 20.0% / 2.35 / 37 | 17.8% / 1.33 / 38 | 8.6% / 1.12 / 43 | 0.5% / 0.10 / 41 |
| 96 | 3.0% / 0.48 / 42 | 8.2% / 1.28 / 44 | 34.8% / 1.98 / 45 | 6.5% / 0.99 / 45 | -6.9% / -0.68 / 50 |
| 97 | 14.1% / 1.66 / 60 | 5.7% / 0.79 / 72 | 24.0% / 1.52 / 64 | 1.3% / 0.22 / 75 | 1.5% / 0.18 / 62 |
| 98 | -0.0% / 0.03 / 91 | 3.4% / 0.55 / 102 | 13.2% / 0.95 / 93 | 8.7% / 1.28 / 86 | 9.8% / 0.87 / 86 |
| 99 | 5.8% / 0.77 / 39 | 18.5% / 2.18 / 35 | 21.6% / 1.39 / 37 | 5.2% / 0.75 / 44 | -4.6% / -0.35 / 41 |
| 100 | 18.7% / 1.99 / 107 | 5.0% / 0.59 / 128 | 26.1% / 1.19 / 116 | 15.3% / 1.66 / 127 | -2.6% / -0.09 / 117 |
| 101 | 3.3% / 0.50 / 49 | 11.1% / 1.53 / 55 | 20.8% / 1.37 / 52 | 7.4% / 1.05 / 54 | -4.7% / -0.37 / 61 |
| 102 | 4.5% / 0.62 / 38 | 17.3% / 2.39 / 40 | 15.6% / 1.29 / 40 | 1.1% / 0.20 / 44 | 1.6% / 0.19 / 49 |
| 103 | 5.9% / 0.70 / 69 | 8.6% / 1.03 / 83 | 21.2% / 1.28 / 76 | 11.6% / 1.38 / 81 | 3.3% / 0.29 / 71 |
| 104 | 4.7% / 0.65 / 70 | 11.3% / 1.45 / 81 | 13.3% / 0.89 / 74 | 8.0% / 1.06 / 81 | 9.1% / 0.75 / 75 |
| 105 | 1.2% / 0.22 / 81 | 5.1% / 0.79 / 89 | 20.8% / 1.41 / 84 | 10.6% / 1.61 / 79 | 5.2% / 0.53 / 75 |
| 106 | -4.5% / -1.02 / 24 | 6.8% / 1.21 / 36 | 17.2% / 1.45 / 30 | 8.0% / 1.32 / 34 | 4.4% / 0.46 / 31 |
| 107 | 8.0% / 1.08 / 42 | 1.5% / 0.29 / 43 | 29.5% / 1.76 / 44 | 12.5% / 1.84 / 45 | -9.0% / -0.93 / 49 |
| 108 | 3.1% / 0.53 / 48 | 1.7% / 0.33 / 53 | 29.3% / 2.03 / 51 | 12.5% / 1.77 / 55 | -1.0% / -0.06 / 51 |
| 109 | 7.5% / 0.89 / 61 | 7.8% / 0.97 / 70 | 15.5% / 1.03 / 63 | 9.6% / 1.21 / 72 | 0.3% / 0.08 / 64 |
| 110 | -2.5% / -0.39 / 42 | 5.9% / 1.03 / 46 | 18.6% / 1.36 / 41 | 11.0% / 1.73 / 46 | 0.8% / 0.12 / 49 |
| 111 | 9.9% / 1.42 / 61 | 6.2% / 0.90 / 74 | 13.8% / 1.16 / 65 | 0.0% / 0.03 / 74 | 10.4% / 0.87 / 63 |
| 112 | 0.7% / 0.14 / 69 | 6.1% / 0.82 / 79 | 22.1% / 1.40 / 68 | 12.7% / 1.74 / 75 | 6.6% / 0.60 / 70 |
| 113 | 5.1% / 0.58 / 76 | 15.3% / 1.67 / 89 | 15.7% / 0.82 / 87 | 11.8% / 1.24 / 87 | 2.2% / 0.22 / 82 |
| 114 | 0.2% / 0.06 / 63 | 2.8% / 0.44 / 67 | 13.2% / 0.99 / 59 | 15.0% / 1.99 / 66 | 8.0% / 0.67 / 66 |
| 115 | 5.9% / 0.86 / 80 | 9.7% / 1.38 / 92 | 19.9% / 1.19 / 82 | 10.2% / 1.40 / 81 | 0.3% / 0.08 / 85 |
| 116 | 7.2% / 0.95 / 33 | 6.5% / 0.93 / 47 | 32.6% / 1.91 / 42 | 1.5% / 0.24 / 43 | -4.2% / -0.28 / 44 |
| 117 | 1.4% / 0.22 / 52 | 4.9% / 0.83 / 65 | 19.6% / 1.39 / 55 | 14.0% / 1.85 / 62 | -2.1% / -0.17 / 57 |
| 118 | 6.0% / 0.73 / 54 | 7.9% / 1.16 / 60 | 16.4% / 1.14 / 54 | 7.4% / 1.04 / 59 | 1.8% / 0.21 / 55 |
| 119 | 7.4% / 1.09 / 65 | 8.1% / 1.24 / 75 | 13.5% / 1.02 / 75 | 4.2% / 0.63 / 75 | 3.4% / 0.37 / 64 |
| 120 | 5.6% / 0.81 / 45 | 1.5% / 0.29 / 56 | 33.3% / 2.17 / 49 | 3.9% / 0.70 / 48 | -2.4% / -0.17 / 52 |
| 121 | 14.4% / 1.81 / 50 | 5.9% / 0.94 / 53 | 15.9% / 1.39 / 46 | 5.6% / 0.99 / 53 | -7.0% / -0.65 / 55 |
| 122 | 4.5% / 0.63 / 59 | 11.9% / 1.61 / 66 | 5.1% / 0.47 / 60 | 14.0% / 1.89 / 67 | 2.8% / 0.29 / 66 |
| 123 | 8.3% / 1.04 / 32 | 8.0% / 1.12 / 39 | 19.0% / 1.19 / 36 | 6.0% / 0.93 / 36 | -1.7% / -0.08 / 40 |
| 124 | 2.3% / 0.39 / 40 | 14.5% / 2.11 / 45 | 12.2% / 1.12 / 47 | 8.9% / 1.23 / 44 | -1.4% / -0.08 / 53 |
| 125 | 5.0% / 0.78 / 39 | 12.4% / 1.73 / 45 | 14.8% / 1.26 / 43 | 14.1% / 1.93 / 46 | -0.8% / -0.01 / 53 |
| 126 | 6.8% / 0.78 / 65 | 5.0% / 0.65 / 77 | 17.7% / 1.03 / 65 | 9.3% / 1.14 / 76 | 3.3% / 0.33 / 69 |
| 127 | 3.0% / 0.41 / 56 | 10.0% / 1.39 / 62 | 14.7% / 1.02 / 56 | 8.5% / 1.19 / 60 | 2.5% / 0.26 / 57 |
| 128 | 0.5% / 0.10 / 32 | 10.6% / 1.64 / 34 | 27.4% / 1.64 / 32 | 2.9% / 0.58 / 32 | -1.8% / -0.12 / 36 |
| 129 | 4.4% / 0.72 / 33 | 13.7% / 1.86 / 40 | 19.9% / 1.73 / 41 | 5.6% / 0.87 / 40 | -7.9% / -0.80 / 47 |
| 130 | 0.1% / 0.06 / 65 | 8.3% / 1.09 / 75 | 18.2% / 1.15 / 80 | 9.5% / 1.18 / 75 | 8.0% / 0.67 / 66 |
| 131 | -0.1% / 0.02 / 60 | 9.0% / 1.24 / 65 | 17.7% / 1.26 / 60 | 20.1% / 2.51 / 62 | 3.1% / 0.31 / 65 |
| 132 | 4.4% / 0.62 / 35 | 11.4% / 1.58 / 34 | 11.4% / 0.92 / 34 | 10.9% / 1.40 / 37 | -3.3% / -0.27 / 40 |
| 133 | 0.4% / 0.09 / 34 | 7.7% / 1.33 / 41 | 27.6% / 1.84 / 38 | 12.1% / 2.06 / 41 | -8.2% / -0.91 / 46 |
| 134 | 9.7% / 1.12 / 49 | 15.6% / 2.11 / 49 | 23.3% / 1.38 / 51 | 9.8% / 1.24 / 51 | -11.2% / -1.05 / 58 |
| 135 | 6.0% / 0.89 / 83 | 6.0% / 0.91 / 93 | 11.5% / 0.84 / 87 | 7.8% / 1.09 / 95 | 7.3% / 0.62 / 80 |
| 136 | 8.2% / 0.99 / 55 | 8.4% / 1.20 / 62 | 6.5% / 0.52 / 54 | 9.4% / 1.26 / 59 | 4.8% / 0.44 / 55 |
| 137 | 5.9% / 0.80 / 37 | 8.8% / 1.24 / 44 | 14.9% / 1.26 / 44 | 12.6% / 1.59 / 46 | -4.2% / -0.31 / 51 |
| 138 | 7.0% / 1.02 / 79 | 8.1% / 1.15 / 97 | 7.8% / 0.60 / 87 | 8.1% / 1.19 / 95 | 8.4% / 0.68 / 84 |
| 139 | 1.1% / 0.21 / 63 | 6.3% / 1.01 / 74 | 20.1% / 1.47 / 73 | 7.2% / 1.05 / 71 | 1.8% / 0.22 / 62 |
| 140 | 11.5% / 1.37 / 76 | 8.7% / 1.25 / 92 | 1.1% / 0.15 / 86 | 13.3% / 1.62 / 84 | 5.9% / 0.56 / 80 |
| 141 | 2.2% / 0.32 / 77 | 9.7% / 1.31 / 87 | 11.3% / 0.75 / 88 | 11.5% / 1.48 / 87 | 3.7% / 0.37 / 77 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_1a6a` | 224 | 0.83 | 0.89/0.94 | 0.86/0.92 |
| 1 | `cfg_6f38` | 24 | 0.84 | 0.88/0.92 | 0.80/0.85 |
| 2 | `cfg_6e04` | 7 | 0.88 | 0.91/0.96 | 0.84/0.96 |
| 3 | `cfg_668f` | 290 | 0.82 | 0.88/0.95 | 0.90/0.95 |
| 4 | `cfg_226a` | 133 | 0.83 | 0.84/0.95 | 0.80/0.95 |
| 5 | `cfg_8508` | 110 | 0.85 | 0.89/0.91 | 0.83/0.89 |
| 6 | `cfg_54a0` | 182 | 0.84 | 0.88/0.93 | 0.83/0.87 |
| 7 | `cfg_475c` | 243 | 0.81 | 0.84/0.94 | 0.72/0.91 |
| 8 | `cfg_bd92` | 97 | 0.87 | 0.92/0.94 | 0.83/0.90 |
| 9 | `cfg_42f0` | 65 | 0.86 | 0.89/0.95 | 0.85/0.89 |
| 10 | `cfg_5e7f` | 74 | 0.83 | 0.85/0.96 | 0.77/0.95 |
| 11 | `cfg_1bcd` | 245 | 0.80 | 0.80/0.88 | 0.76/0.90 |
| 12 | `cfg_d41a` | 100 | 0.82 | 0.87/0.91 | 0.79/0.89 |
| 13 | `cfg_f8ee` | 177 | 0.81 | 0.82/0.97 | 0.72/0.94 |
| 14 | `cfg_5d0b` | 23 | 0.82 | 0.87/0.91 | 0.81/0.86 |
| 15 | `cfg_456b` | 140 | 0.91 | 0.97/0.98 | 0.97/0.98 |
| 16 | `cfg_2ac6` | 62 | 0.85 | 0.94/0.98 | 0.91/0.97 |
| 17 | `cfg_bb7e` | 114 | 0.80 | 0.82/0.93 | 0.75/0.84 |
| 18 | `cfg_4181` | 211 | 0.81 | 0.90/0.95 | 0.78/0.87 |
| 19 | `cfg_747e` | 167 | 0.84 | 0.86/0.95 | 0.75/0.87 |
| 20 | `cfg_36ec` | 40 | 0.85 | 0.88/0.90 | 0.73/0.80 |
| 21 | `cfg_3f62` | 58 | 0.80 | 0.75/0.84 | 0.65/0.79 |
| 22 | `cfg_aca4` | 62 | 0.87 | 0.90/0.94 | 0.85/0.90 |
| 23 | `cfg_4ffe` | 10 | 0.82 | 0.80/0.96 | 0.69/0.90 |
| 24 | `cfg_133c` | 23 | 0.81 | 0.89/0.92 | 0.83/0.86 |
| 25 | `cfg_c564` | 86 | 0.85 | 0.90/0.95 | 0.88/0.95 |
| 26 | `cfg_2253` | 18 | 0.82 | 0.87/0.92 | 0.87/0.93 |
| 27 | `cfg_0500` | 27 | 0.84 | 0.79/0.93 | 0.74/0.85 |
| 28 | `cfg_87fc` | 60 | 0.85 | 0.90/0.93 | 0.85/0.90 |
| 29 | `cfg_d99e` | 57 | 0.84 | 0.84/0.92 | 0.76/0.86 |
| 30 | `cfg_8a80` | 156 | 0.82 | 0.87/0.92 | 0.82/0.91 |
| 31 | `cfg_9274` | 41 | 0.81 | 0.80/0.97 | 0.72/0.90 |
| 32 | `cfg_d685` | 15 | 0.84 | 0.92/0.96 | 0.84/0.93 |
| 33 | `cfg_533d` | 83 | 0.84 | 0.89/0.94 | 0.81/0.89 |
| 34 | `cfg_6d8a` | 230 | 0.80 | 0.87/0.97 | 0.80/0.95 |
| 35 | `cfg_8735` | 68 | 0.85 | 0.85/0.88 | 0.71/0.77 |
| 36 | `cfg_ff8b` | 21 | 0.83 | 0.85/0.86 | 0.79/0.82 |
| 37 | `cfg_0b15` | 43 | 0.83 | 0.94/0.97 | 0.90/0.93 |
| 38 | `cfg_d13e` | 56 | 0.82 | 0.87/0.94 | 0.83/0.94 |
| 39 | `cfg_7792` | 13 | 0.84 | 0.84/0.94 | 0.76/0.87 |
| 40 | `cfg_e628` | 200 | 0.87 | 0.93/0.96 | 0.90/0.94 |
| 41 | `cfg_0c6f` | 152 | 0.81 | 0.74/0.84 | 0.69/0.80 |
| 42 | `cfg_38ce` | 11 | 0.85 | 0.89/0.92 | 0.85/0.89 |
| 43 | `cfg_02d8` | 24 | 0.81 | 0.81/0.84 | 0.71/0.75 |
| 44 | `cfg_606a` | 45 | 0.82 | 0.87/0.92 | 0.80/0.89 |
| 45 | `cfg_3d61` | 34 | 0.86 | 0.86/0.99 | 0.83/0.96 |
| 46 | `cfg_0959` | 13 | 0.86 | 0.82/0.87 | 0.68/0.75 |
| 47 | `cfg_876a` | 35 | 0.85 | 0.90/0.94 | 0.84/0.90 |
| 48 | `cfg_472f` | 65 | 0.84 | 0.88/0.93 | 0.75/0.82 |
| 49 | `cfg_9e52` | 156 | 0.80 | 0.78/0.90 | 0.79/0.91 |
| 50 | `cfg_c62f` | 76 | 0.82 | 0.87/0.91 | 0.77/0.85 |
| 51 | `cfg_1a38` | 146 | 0.84 | 0.80/0.88 | 0.75/0.82 |
| 52 | `cfg_2c7e` | 282 | 0.82 | 0.92/0.96 | 0.85/0.93 |
| 53 | `cfg_6e2e` | 37 | 0.84 | 0.86/0.96 | 0.80/0.94 |
| 54 | `cfg_dfb9` | 63 | 0.80 | 0.89/0.94 | 0.79/0.87 |
| 55 | `cfg_dc01` | 68 | 0.83 | 0.86/0.89 | 0.77/0.84 |
| 56 | `cfg_a42a` | 8 | 0.82 | 0.86/0.87 | 0.80/0.81 |
| 57 | `cfg_051b` | 9 | 0.96 | 0.96/0.97 | 0.94/0.96 |
| 58 | `cfg_145f` | 39 | 0.81 | 0.87/0.92 | 0.87/0.91 |
| 59 | `cfg_fcef` | 49 | 0.83 | 0.75/0.85 | 0.68/0.77 |
| 60 | `cfg_5f16` | 38 | 0.85 | 0.90/0.95 | 0.86/0.88 |
| 61 | `cfg_e6b0` | 36 | 0.86 | 0.87/0.93 | 0.80/0.89 |
| 62 | `cfg_a27f` | 73 | 0.83 | 0.92/0.94 | 0.88/0.93 |
| 63 | `cfg_c201` | 8 | 0.87 | 0.89/0.99 | 0.82/0.99 |
| 64 | `cfg_0631` | 15 | 0.87 | 0.94/0.96 | 0.89/0.95 |
| 65 | `cfg_6791` | 58 | 0.82 | 0.82/0.90 | 0.77/0.86 |
| 66 | `cfg_5846` | 5 | 0.85 | 0.78/0.82 | 0.60/0.69 |
| 67 | `cfg_c821` | 69 | 0.82 | 0.88/0.91 | 0.78/0.84 |
| 68 | `cfg_48b4` | 20 | 0.86 | 0.93/0.94 | 0.83/0.87 |
| 69 | `cfg_e43e` | 49 | 0.85 | 0.86/0.91 | 0.72/0.80 |
| 70 | `cfg_1760` | 19 | 0.90 | 0.86/0.89 | 0.75/0.79 |
| 71 | `cfg_d23c` | 74 | 0.86 | 0.91/0.96 | 0.84/0.93 |
| 72 | `cfg_92bd` | 11 | 0.82 | 0.85/0.93 | 0.78/0.88 |
| 73 | `cfg_62e7` | 16 | 0.87 | 0.87/0.92 | 0.82/0.87 |
| 74 | `cfg_92d4` | 32 | 0.81 | 0.81/0.94 | 0.74/0.86 |
| 75 | `cfg_1813` | 41 | 0.83 | 0.76/0.97 | 0.66/0.93 |
| 76 | `cfg_6e85` | 9 | 0.87 | 0.84/0.92 | 0.78/0.85 |
| 77 | `cfg_52e8` | 42 | 0.82 | 0.82/0.88 | 0.75/0.80 |
| 78 | `cfg_3f80` | 9 | 0.86 | 0.81/0.84 | 0.74/0.78 |
| 79 | `cfg_c2e4` | 6 | 0.97 | 0.97/0.98 | 0.95/0.97 |
| 80 | `cfg_e2e2` | 28 | 0.82 | 0.61/0.86 | 0.62/0.79 |
| 81 | `cfg_c7d1` | 26 | 0.82 | 0.88/0.92 | 0.80/0.88 |
| 82 | `cfg_8314` | 52 | 0.93 | 0.98/0.99 | 0.97/0.98 |
| 83 | `cfg_50c7` | 16 | 0.89 | 0.89/0.89 | 0.84/0.86 |
| 84 | `cfg_561b` | 12 | 0.84 | 0.91/0.96 | 0.84/0.94 |
| 85 | `cfg_3226` | 16 | 0.85 | 0.89/0.91 | 0.80/0.82 |
| 86 | `cfg_9d61` | 13 | 0.82 | 0.85/0.97 | 0.80/0.96 |
| 87 | `cfg_e023` | 12 | 0.85 | 0.91/0.91 | 0.80/0.83 |
| 88 | `cfg_fd20` | 11 | 0.87 | 0.82/0.96 | 0.78/0.90 |
| 89 | `cfg_b887` | 7 | 0.88 | 0.90/0.92 | 0.84/0.91 |
| 90 | `cfg_9444` | 18 | 0.93 | 0.93/0.96 | 0.83/0.92 |
| 91 | `cfg_984d` | 53 | 0.85 | 0.85/0.93 | 0.75/0.88 |
| 92 | `cfg_846e` | 6 | 0.95 | 0.94/0.99 | 0.87/0.96 |
| 93 | `cfg_d8d5` | 38 | 0.80 | 0.78/0.89 | 0.67/0.85 |
| 94 | `cfg_3421` | 54 | 0.84 | 0.90/0.94 | 0.83/0.88 |
| 95 | `cfg_a905` | 15 | 0.85 | 0.83/0.94 | 0.66/0.84 |
| 96 | `cfg_67fd` | 45 | 0.83 | 0.83/0.88 | 0.72/0.84 |
| 97 | `cfg_3379` | 62 | 0.80 | 0.80/0.83 | 0.76/0.81 |
| 98 | `cfg_5ee2` | 20 | 0.86 | 0.88/0.92 | 0.81/0.86 |
| 99 | `cfg_d004` | 9 | 0.91 | 0.92/0.97 | 0.87/0.94 |
| 100 | `cfg_7fc7` | 20 | 0.88 | 0.91/0.96 | 0.92/0.96 |
| 101 | `cfg_1b7c` | 18 | 0.81 | 0.82/0.97 | 0.72/0.94 |
| 102 | `cfg_a570` | 8 | 0.92 | 0.92/0.94 | 0.88/0.89 |
| 103 | `cfg_77ad` | 2 | 0.96 | 0.94/0.94 | 0.94/0.94 |
| 104 | `cfg_1455` | 10 | 0.85 | 0.84/0.85 | 0.76/0.76 |
| 105 | `cfg_1d30` | 2 | 0.96 | 0.95/0.95 | 0.86/0.86 |
| 106 | `cfg_3f06` | 40 | 0.80 | 0.85/0.91 | 0.75/0.85 |
| 107 | `cfg_44c6` | 20 | 0.87 | 0.91/0.93 | 0.80/0.83 |
| 108 | `cfg_514d` | 8 | 0.92 | 0.96/0.96 | 0.98/0.99 |
| 109 | `cfg_1a20` | 22 | 0.86 | 0.90/0.93 | 0.80/0.81 |
| 110 | `cfg_cde6` | 10 | 0.91 | 0.90/0.99 | 0.79/0.93 |
| 111 | `cfg_6f73` | 38 | 0.82 | 0.81/0.92 | 0.71/0.87 |
| 112 | `cfg_f951` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 113 | `cfg_baf9` | 4 | 0.91 | 0.92/0.95 | 0.84/0.87 |
| 114 | `cfg_3778` | 12 | 0.83 | 0.91/0.94 | 0.87/0.90 |
| 115 | `cfg_7852` | 16 | 0.97 | 0.95/0.98 | 0.94/0.97 |
| 116 | `cfg_e12a` | 25 | 0.83 | 0.81/0.89 | 0.74/0.83 |
| 117 | `cfg_c12f` | 13 | 0.90 | 0.96/0.98 | 0.94/0.96 |
| 118 | `cfg_8e9f` | 7 | 0.88 | 0.86/0.96 | 0.82/0.93 |
| 119 | `cfg_2505` | 4 | 0.83 | 0.92/0.95 | 0.93/0.93 |
| 120 | `cfg_6ce9` | 7 | 0.86 | 0.91/0.91 | 0.84/0.84 |
| 121 | `cfg_ec3a` | 8 | 0.93 | 0.93/0.95 | 0.90/0.91 |
| 122 | `cfg_3258` | 16 | 0.80 | 0.80/0.89 | 0.78/0.90 |
| 123 | `cfg_b70b` | 26 | 0.84 | 0.91/0.93 | 0.82/0.85 |
| 124 | `cfg_4876` | 9 | 0.86 | 0.90/0.93 | 0.85/0.90 |
| 125 | `cfg_d709` | 20 | 0.91 | 0.93/0.96 | 0.92/0.93 |
| 126 | `cfg_9d7d` | 4 | 1.00 | 1.00/1.00 | 0.98/0.98 |
| 127 | `cfg_2f1d` | 8 | 0.95 | 0.95/0.99 | 0.94/0.97 |
| 128 | `cfg_502c` | 10 | 0.82 | 0.89/0.95 | 0.84/0.93 |
| 129 | `cfg_438c` | 10 | 0.90 | 0.93/0.99 | 0.85/0.99 |
| 130 | `cfg_6aca` | 12 | 0.81 | 0.68/0.91 | 0.59/0.86 |
| 131 | `cfg_b3d5` | 5 | 0.86 | 0.90/0.91 | 0.85/0.86 |
| 132 | `cfg_6bb3` | 6 | 0.90 | 0.84/0.98 | 0.76/0.96 |
| 133 | `cfg_5fc5` | 3 | 0.91 | 0.86/0.88 | 0.83/0.85 |
| 134 | `cfg_3c65` | 7 | 0.84 | 0.87/0.93 | 0.76/0.86 |
| 135 | `cfg_42b2` | 1 | n/a | n/a/n/a | n/a/n/a |
| 136 | `cfg_5e60` | 10 | 0.86 | 0.92/0.95 | 0.90/0.92 |
| 137 | `cfg_63db` | 1 | n/a | n/a/n/a | n/a/n/a |
| 138 | `cfg_abbb` | 6 | 0.89 | 0.91/0.94 | 0.83/0.90 |
| 139 | `cfg_b254` | 3 | 0.96 | 0.97/0.99 | 0.92/0.96 |
| 140 | `cfg_e1c8` | 2 | 0.87 | 0.60/0.60 | 0.70/0.70 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 4.524e-04 over 60000 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1058.0, participation ratio 3.2, 95%-variance components 95 (rank bound T = 1259); raw grid 60000; raw + known prior 820584
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Drawdown limit -30% is reused from the channel-breakout funnel (src/experiments/validation.py); that approval was given for 0.25%-risk stop-based sizing, while this strategy invests full equity per trade (and may run with no stop at all) -- it has not been separately approved for this sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0: Sharpe vs. cash is overstated in high-rate years (2023-2024 ~5%).
- Variable cost stress scales per-share commission and slippage bps; the $1 per-order minimum commission is treated as fixed.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Prices are split-adjusted but NOT dividend-adjusted: SPY's ~1.5%/yr dividend is not credited while long.
- Long-only: bearish crossovers only exit; short trades are not tested (the slope filter's short side is unused).
- Neighbor lattice: timeframe, fast length, slow length, confirm bars, ATR buffer, stop (1.5 < 2.0 < 2.5 < 3.0 < off) and slope filter (off < on) are ordered; ma_pair is categorical and held fixed.
- All MA lengths, confirmation bars and the 5-bar slope lookback are counted in bars of the config's timeframe, so the same values span very different clock time on 5min vs 1h bars.

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
QQQ results are unchanged rules on the development period: supporting evidence, not an independent replication.

## Integrity audit

- Fast / slow MAs are SMA or EMA (per ma_pair, fast type first) of closes on bars of the config's timeframe; SMA_t is the mean of the last n closes through t, EMA (alpha 2/(n+1)) is seeded with the SMA of the first n closes. Both use closes up to and including bar t.
- A bullish run starts at the crossover bar k (fast > slow at k, fast <= slow with both MAs defined at k-1) and lasts while fast > slow. The entry signal is the FIRST bar c of the run where the run has lasted >= confirm_bars bars, fast - slow >= buffer_atr x ATR(14)_c, and (slope filter on) slow_c > slow_{c-5}; the entry fills at the NEXT bar's open. Each run is traded at most once.
- Initial stop (if on) = entry-bar open - stop_atr x ATR(14) using the ATR known before the entry fill, live from the entry bar; a touch exits at the worse of the bar's open and the stop.
- Crossover exit: at the close of the first bar after the signal with fast <= slow (raw cross: no confirmation or buffer), filled at the next bar's open; a stop touched on that same bar fills first. There is no profit target and no time limit.
- Sizing: as many whole shares as current equity affords (no leverage), as in the RSI-divergence and mean-reversion funnels.
- Signals while a position is open are ignored; missed-entry stress drops whole signals (that bullish run is not traded), never re-entering one bar later. Under entry-delay stress, a cross before the delayed fill is acted on at the entry bar's close.
- Adverse slippage + commission on every fill; a fill at a session's first bar bears the full overnight gap.
- Development backtests run on data physically truncated at the development end; open positions are force-closed at the last development bar and flagged (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Positions are held overnight (no session-end flattening), as in the other families; MAs, slope and ATR run continuously across sessions over RTH bars only.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Unresolved assumptions

- Drawdown limit -30% is reused from the channel-breakout funnel (src/experiments/validation.py); that approval was given for 0.25%-risk stop-based sizing, while this strategy invests full equity per trade -- it has not been separately approved for this sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0: Sharpe vs. cash is overstated in high-rate years (2023-2024 ~5%).
- Variable cost stress scales per-share commission and slippage bps; the $1 per-order minimum commission is treated as fixed.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Prices are split-adjusted but NOT dividend-adjusted: SPY's ~1.5%/yr dividend is not credited while long.
- Long-only crossover; bearish crossovers only exit, and the short side of the slope filter is unused.
- One entry per bullish run: after a stop-out the strategy waits for the next fresh crossover, even if the fast MA is still above the slow MA.
- Neighbor lattice: every axis is ordered except ma_pair (categorical, held fixed); stop runs 1.5 < 2.0 < 2.5 < 3.0 < off, slope filter off < on.
- All MA lengths and bar counts are in bars of the config's timeframe, not in trading days.
