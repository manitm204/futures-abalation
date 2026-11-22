# Screening funnel -- os_nq_v1 (development stages only)

- Code: `3593f49ab5a1` (dirty working tree: True, diff sha256 `e7dc91a3d623`)
- Config: `configs/funnel/os_funnel_nq_v1.yaml` sha256 `1adefd472d7ad95b`; seed 20261126
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'NQ': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `ddb64c95eb9c4733` (580 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No open-sweep strategy has been scored on NQ 2023-2024, but the noise-band, mean-reversion, squeeze, convexity, EMRT and last-half-hour families were selected there and the researcher has read those results.
- Holdout 2025+ previously inspected: **True** -- No open-sweep metrics have been computed on NQ 2025+. Noise-band NQ picks, the month-end #7 transfer check and last-half-hour #49/#56 were scored there, so the researcher has seen how that period treated intraday NQ strategies.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 24300 | 24300 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 24300 | 24300 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 24300 | 17802 | 6498 | 0 |  | 0 | 73.26 | 73.26 |  |
| 3 performance & risk | hard_gate | 17802 | 1371 | 16431 | 0 |  | 0 | 5.64 | 7.70 |  |
| 4 parameter stability | hard_gate | 1371 | 1370 | 1 | 0 |  | 0 | 5.64 | 99.93 |  |
| 5 time stability | hard_gate | 1370 | 1368 | 2 | 0 |  | 1011 | 5.63 | 99.85 |  |
| 6 deduplication | dedup | 1368 | 580 |  |  | 788 |  | 2.39 | 42.40 | best 2 per cluster |
| 7 execution stress | hard_gate | 580 | 580 | 0 | 0 |  | 0 | 2.39 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 580 |  |  |  |  |  |  |  | diagnostic only: unverified: 580 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 6498 |
| s2:hard_reject:years_with_>=10_trades | 2709 |
| s3:hard_reject:net_return | 8840 |
| s3:hard_reject:sharpe | 16431 |
| s4:hard_reject:local_median_sharpe | 1 |
| s5:hard_reject:profitable_years | 2 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop/target exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_8182` | timeframe=1min, level=box, side=both, window=60, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=16:00 | 0/202/572/0 | 774 | 77.0% | 11.8% | 1.49 | -5.7% | 138 | 1.49 | 19.9% | 381.6 | 6/6 | 0.83 | 1.20 | 0.29 | 5 | 36.8% | 0.52 | 0.32 | 72.7% | 68.3% | 69.3% | 69.2%/60.3% | 11.2 (interpolated) | pass | 0.320 (unverified) | 0.25 |
| 2 | `cfg_b395` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 91/0/102/0 | 193 | 36.3% | 6.2% | 1.61 | -2.8% | 345 | 2.12 | 3.9% | 94.8 | 7/7 | 1.00 | 1.44 | 0.17 | 5 | 21.1% | 0.42 | 0.35 | 35.7% | 34.6% | 31.5% | 33.0%/28.6% | 23.8 (interpolated) | pass | 0.430 (unverified) | 0.73 |
| 3 | `cfg_ddfe` | timeframe=1min, level=box, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=16:00 | 0/181/497/0 | 678 | 70.6% | 11.0% | 1.46 | -5.0% | 133 | 1.52 | 18.0% | 335.7 | 7/7 | 0.86 | 1.31 | 0.16 | 5 | 36.1% | 0.49 | 0.34 | 67.4% | 64.5% | 64.5% | 62.8%/50.4% | 11.8 (interpolated) | pass | 0.292 (unverified) | 0.54 |
| 4 | `cfg_db87` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=12:30 | 55/0/100/38 | 193 | 31.7% | 5.5% | 1.58 | -3.7% | 347 | 2.01 | 3.1% | 94.8 | 8/8 | 1.00 | 1.33 | 0.25 | 4 | 18.9% | 0.40 | 0.30 | 30.9% | 29.7% | 24.8% | 27.6%/23.1% | 22.4 (interpolated) | pass | 0.403 (unverified) | 0.65 |
| 5 | `cfg_0612` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=16:00 | 0/80/306/0 | 386 | 46.0% | 7.7% | 1.39 | -3.7% | 139 | 1.78 | 8.3% | 191.5 | 6/6 | 1.00 | 1.29 | 0.09 | 5 | 29.1% | 0.37 | 0.39 | 44.6% | 43.1% | 41.9% | 41.9%/33.9% | 14.5 (interpolated) | pass | 0.209 (unverified) | 0.25 |
| 6 | `cfg_89ab` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 167/0/202/0 | 369 | 41.2% | 7.0% | 1.42 | -3.7% | 188 | 1.58 | 7.1% | 182.2 | 8/8 | 1.00 | 1.34 | 0.08 | 5 | 23.8% | 0.42 | 0.33 | 40.0% | 38.5% | 35.1% | 36.6%/32.0% | 13.9 (interpolated) | pass | 0.263 (unverified) | 1.11 |
| 7 | `cfg_3266` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=range, exit=12:30 | 33/0/97/62 | 192 | 27.0% | 4.8% | 1.50 | -3.3% | 347 | 1.93 | 2.5% | 93.6 | 8/8 | 1.00 | 1.31 | 0.19 | 4 | 15.6% | 0.42 | 0.30 | 26.2% | 25.6% | 23.5% | 24.3%/20.6% | 21.0 (interpolated) | pass | 0.327 (unverified) | 0.79 |
| 8 | `cfg_6aec` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/132/237/0 | 369 | 52.2% | 8.6% | 1.39 | -4.0% | 217 | 1.62 | 13.4% | 183.1 | 7/7 | 1.00 | 1.42 | -0.03 | 4 | 25.3% | 0.52 | 0.34 | 50.8% | 50.0% | 48.9% | 46.6%/38.1% | 16.4 (interpolated) | pass | 0.228 (unverified) | 0.88 |
| 9 | `cfg_bf97` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 149/0/147/0 | 296 | 31.3% | 5.5% | 1.45 | -3.0% | 208 | 1.65 | 6.0% | 145.3 | 7/7 | 1.00 | 1.24 | 0.20 | 5 | 21.0% | 0.31 | 0.32 | 30.4% | 29.0% | 29.2% | 29.3%/23.8% | 13.7 (interpolated) | pass | 0.283 (unverified) | 0.78 |
| 10 | `cfg_5cdc` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 155/0/185/0 | 340 | 40.7% | 6.9% | 1.43 | -5.0% | 191 | 1.61 | 6.5% | 166.5 | 7/7 | 0.86 | 1.29 | 0.14 | 5 | 26.8% | 0.34 | 0.32 | 39.1% | 37.7% | 28.9% | 35.1%/30.8% | 15.3 (interpolated) | pass | 0.267 (unverified) | 0.53 |
| 11 | `cfg_7304` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/81/288/0 | 369 | 46.9% | 7.8% | 1.48 | -2.5% | 168 | 1.91 | 8.0% | 181.3 | 8/8 | 1.00 | 1.30 | 0.19 | 5 | 19.1% | 0.59 | 0.37 | 44.1% | 40.8% | 24.5% | 40.3%/31.2% | 14.9 (interpolated) | pass | 0.292 (unverified) | 1.00 |
| 12 | `cfg_aafc` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/120/176/0 | 296 | 43.0% | 7.2% | 1.46 | -4.9% | 224 | 1.72 | 11.7% | 145.3 | 6/6 | 1.00 | 1.19 | 0.26 | 4 | 27.2% | 0.37 | 0.35 | 41.3% | 40.4% | 41.8% | 37.9%/32.8% | 17.9 (interpolated) | pass | 0.281 (unverified) | 0.52 |
| 13 | `cfg_7423` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=none, exit=12:30 | 97/0/243/0 | 340 | 33.0% | 5.7% | 1.39 | -4.3% | 142 | 1.76 | 4.3% | 167.0 | 8/8 | 1.00 | 1.25 | 0.14 | 5 | 20.1% | 0.39 | 0.39 | 32.0% | 29.8% | 16.5% | 30.4%/25.6% | 12.5 (interpolated) | pass | 0.218 (unverified) | 0.34 |
| 14 | `cfg_a2a3` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=struct, target=none, exit=12:30 | 152/0/275/0 | 427 | 41.3% | 7.0% | 1.37 | -4.1% | 111 | 1.52 | 6.7% | 210.2 | 8/8 | 0.88 | 1.22 | 0.15 | 5 | 27.5% | 0.27 | 0.34 | 39.5% | 37.7% | 39.5% | 37.9%/32.3% | 12.7 (interpolated) | pass | 0.222 (unverified) | 0.49 |
| 15 | `cfg_020a` | timeframe=1min, level=onh, side=both, window=15, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/95/161/0 | 256 | 47.8% | 7.9% | 1.50 | -4.4% | 281 | 1.94 | 9.4% | 126.3 | 6/6 | 1.00 | 1.40 | 0.11 | 5 | 18.2% | 0.62 | 0.34 | 46.3% | 44.5% | 44.8% | 41.3%/34.5% | 21.7 (interpolated) | pass | 0.323 (unverified) | 0.77 |
| 16 | `cfg_9cd6` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/106/354/0 | 460 | 49.8% | 8.2% | 1.39 | -4.9% | 127 | 1.69 | 10.3% | 227.7 | 8/8 | 1.00 | 1.21 | 0.18 | 5 | 27.6% | 0.37 | 0.42 | 46.0% | 43.7% | 41.6% | 43.4%/37.6% | 12.9 (interpolated) | pass | 0.206 (unverified) | 0.50 |
| 17 | `cfg_1cbe` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=16:00 | 0/93/388/0 | 481 | 47.4% | 7.9% | 1.35 | -3.1% | 143 | 1.64 | 9.7% | 237.1 | 7/7 | 1.00 | 1.19 | 0.15 | 5 | 29.1% | 0.39 | 0.39 | 46.0% | 43.8% | 43.6% | 43.8%/38.2% | 12.7 (interpolated) | pass | 0.183 (unverified) | 0.32 |
| 18 | `cfg_fd8e` | timeframe=1min, level=onh, side=both, window=15, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 115/0/141/0 | 256 | 38.5% | 6.6% | 1.57 | -3.6% | 264 | 1.89 | 4.9% | 126.5 | 7/7 | 1.00 | 1.33 | 0.24 | 5 | 18.4% | 0.52 | 0.33 | 37.3% | 35.3% | 32.7% | 32.8%/27.3% | 18.6 (interpolated) | pass | 0.390 (unverified) | 0.89 |
| 19 | `cfg_a800` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=none, exit=12:30 | 106/0/140/0 | 246 | 33.8% | 5.8% | 1.37 | -2.9% | 215 | 1.74 | 4.7% | 120.4 | 8/8 | 1.00 | 1.21 | 0.17 | 5 | 19.5% | 0.42 | 0.38 | 33.0% | 32.0% | 27.8% | 30.3%/25.6% | 17.6 (interpolated) | pass | 0.214 (unverified) | 0.44 |
| 20 | `cfg_d063` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=3R, exit=12:30 | 116/0/146/34 | 296 | 29.2% | 5.1% | 1.41 | -2.9% | 175 | 1.62 | 5.5% | 144.5 | 8/8 | 1.00 | 1.16 | 0.26 | 5 | 19.0% | 0.33 | 0.32 | 28.0% | 26.9% | 26.9% | 25.8%/21.1% | 13.1 (interpolated) | pass | 0.254 (unverified) | 0.72 |
| 21 | `cfg_b773` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=12:30 | 95/0/291/0 | 386 | 34.3% | 5.9% | 1.34 | -3.1% | 181 | 1.65 | 4.6% | 189.3 | 7/7 | 1.00 | 1.20 | 0.13 | 5 | 24.1% | 0.30 | 0.40 | 32.3% | 30.0% | 31.4% | 31.0%/24.5% | 11.3 (interpolated) | pass | 0.179 (unverified) | 0.42 |
| 22 | `cfg_439a` | timeframe=1min, level=box, side=both, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/276/498/0 | 774 | 79.9% | 12.2% | 1.37 | -6.3% | 177 | 1.39 | 26.8% | 385.6 | 6/6 | 0.83 | 1.19 | 0.18 | 5 | 36.1% | 0.55 | 0.31 | 76.9% | 72.1% | 54.5% | 72.3%/55.7% | 11.0 (interpolated) | pass | 0.222 (unverified) | 0.07 |
| 23 | `cfg_ce32` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=struct, target=none, exit=16:00 | 0/72/174/0 | 246 | 36.7% | 6.3% | 1.28 | -2.6% | 219 | 1.82 | 7.1% | 120.9 | 7/7 | 1.00 | 1.30 | -0.02 | 5 | 22.5% | 0.39 | 0.45 | 35.4% | 33.6% | 35.4% | 33.1%/24.3% | 18.2 (interpolated) | pass | 0.129 (unverified) | 0.36 |
| 24 | `cfg_1672` | timeframe=1min, level=onh, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=struct, target=none, exit=16:00 | 0/82/250/0 | 332 | 38.7% | 6.6% | 1.30 | -4.2% | 222 | 1.77 | 7.8% | 163.1 | 7/7 | 1.00 | 1.20 | 0.10 | 5 | 20.7% | 0.46 | 0.43 | 37.2% | 36.2% | 37.6% | 35.5%/29.4% | 14.5 (interpolated) | pass | 0.148 (unverified) | 0.77 |
| 25 | `cfg_8ac6` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/84/290/0 | 374 | 39.9% | 6.8% | 1.38 | -3.3% | 186 | 1.74 | 8.7% | 184.3 | 8/8 | 1.00 | 1.24 | 0.14 | 5 | 27.3% | 0.32 | 0.41 | 38.5% | 36.6% | 29.5% | 35.6%/28.3% | 13.1 (interpolated) | pass | 0.201 (unverified) | 0.36 |
| 26 | `cfg_ff7f` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/78/308/0 | 386 | 38.8% | 6.6% | 1.31 | -2.7% | 194 | 1.73 | 8.1% | 188.8 | 7/7 | 1.00 | 1.22 | 0.09 | 5 | 19.6% | 0.49 | 0.39 | 36.5% | 33.1% | 28.6% | 33.6%/26.4% | 12.6 (interpolated) | pass | 0.156 (unverified) | 0.36 |
| 27 | `cfg_4b4e` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=3, mode=cont, stop=struct, target=none, exit=16:00 | 0/83/213/0 | 296 | 41.7% | 7.0% | 1.32 | -2.9% | 215 | 1.76 | 8.2% | 146.1 | 8/8 | 1.00 | 1.20 | 0.12 | 5 | 23.4% | 0.44 | 0.42 | 40.6% | 38.7% | 41.2% | 36.6%/28.4% | 17.2 (interpolated) | pass | 0.162 (unverified) | 0.50 |
| 28 | `cfg_c1bf` | timeframe=1min, level=onh, side=both, window=15, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=16:00 | 0/78/178/0 | 256 | 39.0% | 6.6% | 1.40 | -3.5% | 222 | 1.96 | 7.2% | 126.0 | 6/6 | 1.00 | 1.25 | 0.15 | 5 | 17.8% | 0.54 | 0.40 | 38.0% | 36.8% | 38.1% | 34.2%/29.6% | 18.8 (interpolated) | pass | 0.220 (unverified) | 0.69 |
| 29 | `cfg_221d` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/94/387/0 | 481 | 44.2% | 7.4% | 1.33 | -3.6% | 122 | 1.63 | 9.7% | 236.3 | 8/8 | 1.00 | 1.20 | 0.13 | 5 | 21.3% | 0.52 | 0.38 | 42.6% | 39.8% | 37.4% | 38.6%/29.4% | 11.6 (interpolated) | pass | 0.178 (unverified) | 0.45 |
| 30 | `cfg_aab7` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=16:00 | 0/108/266/0 | 374 | 46.3% | 7.7% | 1.39 | -4.8% | 163 | 1.73 | 10.6% | 183.0 | 7/7 | 1.00 | 1.14 | 0.25 | 4 | 25.7% | 0.45 | 0.42 | 43.1% | 41.8% | 41.6% | 40.4%/33.6% | 14.8 (interpolated) | pass | 0.214 (unverified) | 0.81 |
| 31 | `cfg_2dec` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=12:30 | 105/0/269/0 | 374 | 29.7% | 5.2% | 1.37 | -2.9% | 126 | 1.61 | 4.8% | 185.7 | 9/9 | 1.00 | 1.14 | 0.23 | 5 | 22.2% | 0.25 | 0.37 | 27.1% | 25.2% | 20.6% | 26.0%/22.1% | 10.2 (interpolated) | pass | 0.209 (unverified) | 0.20 |
| 32 | `cfg_1bdb` | timeframe=1min, level=box, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/96/315/0 | 411 | 43.2% | 7.3% | 1.35 | -5.9% | 159 | 1.68 | 9.4% | 204.8 | 7/7 | 1.00 | 1.03 | 0.31 | 5 | 24.7% | 0.36 | 0.43 | 41.5% | 39.7% | 36.8% | 39.0%/33.7% | 13.0 (interpolated) | pass | 0.182 (unverified) | 0.59 |
| 33 | `cfg_a548` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/139/558/0 | 697 | 52.6% | 8.6% | 1.23 | -7.5% | 293 | 1.46 | 13.8% | 344.9 | 7/7 | 0.86 | 1.10 | 0.14 | 4 | 34.7% | 0.34 | 0.45 | 48.0% | 43.5% | 44.0% | 47.1%/36.3% | 9.3 (interpolated) | pass | 0.114 (unverified) | 0.24 |
| 34 | `cfg_1061` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=range, exit=16:00 | 0/14/289/83 | 386 | 29.6% | 5.2% | 1.28 | -3.9% | 199 | 1.58 | 3.9% | 188.3 | 7/7 | 1.00 | 1.11 | 0.17 | 5 | 19.5% | 0.34 | 0.39 | 26.6% | 25.9% | 24.4% | 26.2%/22.0% | 10.4 (interpolated) | pass | 0.146 (unverified) | 0.28 |
| 35 | `cfg_1d8d` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/72/121/0 | 193 | 40.4% | 6.8% | 1.44 | -3.2% | 345 | 2.02 | 7.4% | 94.9 | 6/6 | 1.00 | 1.27 | 0.17 | 5 | 20.9% | 0.48 | 0.38 | 39.5% | 38.9% | 35.1% | 36.3%/30.7% | n/a (profitable_beyond_25.0x) | pass | 0.255 (unverified) | 0.40 |
| 36 | `cfg_f1b7` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/163/284/0 | 447 | 54.8% | 8.9% | 1.35 | -5.6% | 162 | 1.52 | 16.2% | 217.8 | 8/8 | 1.00 | 1.17 | 0.17 | 5 | 31.4% | 0.43 | 0.37 | 51.9% | 50.0% | 50.7% | 49.2%/41.0% | 14.7 (interpolated) | pass | 0.196 (unverified) | 0.55 |
| 37 | `cfg_c1e7` | timeframe=1min, level=box, side=both, window=60, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=16:00 | 0/159/662/0 | 821 | 61.7% | 9.8% | 1.30 | -4.5% | 108 | 1.45 | 16.1% | 402.0 | 6/6 | 0.83 | 1.23 | 0.06 | 5 | 38.9% | 0.37 | 0.40 | 58.6% | 53.9% | 58.7% | 56.0%/46.4% | 9.2 (interpolated) | pass | 0.155 (unverified) | 0.27 |
| 38 | `cfg_5e18` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/70/226/0 | 296 | 32.1% | 5.6% | 1.32 | -3.3% | 268 | 1.83 | 7.1% | 144.2 | 7/7 | 1.00 | 1.19 | 0.13 | 4 | 20.3% | 0.37 | 0.44 | 30.9% | 29.2% | 18.1% | 29.1%/23.0% | 13.9 (interpolated) | pass | 0.158 (unverified) | 0.68 |
| 39 | `cfg_603b` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=16:00 | 0/139/558/0 | 697 | 53.3% | 8.7% | 1.22 | -3.8% | 201 | 1.46 | 13.9% | 341.5 | 6/6 | 0.83 | 1.24 | -0.03 | 5 | 36.7% | 0.31 | 0.46 | 50.4% | 44.7% | 53.3% | 47.4%/39.3% | 9.7 (interpolated) | pass | 0.106 (unverified) | 0.38 |
| 40 | `cfg_d2cb` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 64/0/182/0 | 246 | 26.6% | 4.7% | 1.29 | -2.3% | 209 | 1.88 | 2.9% | 120.4 | 9/9 | 1.00 | 1.22 | 0.07 | 5 | 18.1% | 0.30 | 0.46 | 25.8% | 24.7% | 11.3% | 24.3%/20.4% | 14.0 (interpolated) | pass | 0.132 (unverified) | 0.37 |
| 41 | `cfg_4852` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/52/194/0 | 246 | 33.4% | 5.8% | 1.30 | -2.8% | 219 | 2.00 | 5.4% | 120.7 | 8/8 | 1.00 | 1.27 | 0.03 | 5 | 21.2% | 0.36 | 0.46 | 31.8% | 31.0% | 17.5% | 29.4%/24.1% | 16.7 (interpolated) | pass | 0.130 (unverified) | 0.12 |
| 42 | `cfg_b9ec` | timeframe=1min, level=box, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=12:30 | 113/0/298/0 | 411 | 31.2% | 5.4% | 1.29 | -6.0% | 161 | 1.53 | 5.1% | 204.8 | 8/8 | 1.00 | 1.00 | 0.28 | 5 | 16.0% | 0.44 | 0.41 | 29.8% | 28.3% | 26.7% | 27.8%/21.8% | 9.9 (interpolated) | pass | 0.161 (unverified) | 0.39 |
| 43 | `cfg_0658` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/96/351/0 | 447 | 41.1% | 7.0% | 1.33 | -4.1% | 164 | 1.63 | 10.1% | 218.5 | 9/9 | 1.00 | 1.16 | 0.17 | 4 | 25.1% | 0.31 | 0.41 | 39.4% | 36.4% | 48.5% | 36.8%/30.4% | 11.7 (interpolated) | pass | 0.167 (unverified) | 0.41 |
| 44 | `cfg_cbf2` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=struct, target=none, exit=16:00 | 0/107/340/0 | 447 | 42.0% | 7.1% | 1.26 | -5.3% | 265 | 1.61 | 10.6% | 218.8 | 8/8 | 0.88 | 1.13 | 0.13 | 4 | 25.1% | 0.40 | 0.48 | 40.1% | 38.6% | 43.8% | 36.7%/30.5% | 11.9 (interpolated) | pass | 0.125 (unverified) | 0.86 |
| 45 | `cfg_a55a` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/156/616/0 | 772 | 57.0% | 9.2% | 1.28 | -7.7% | 180 | 1.45 | 15.4% | 380.4 | 8/8 | 0.88 | 1.13 | 0.15 | 4 | 37.3% | 0.35 | 0.42 | 54.2% | 51.2% | 52.2% | 50.2%/41.9% | 9.0 (interpolated) | pass | 0.145 (unverified) | 0.33 |
| 46 | `cfg_cee8` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=12:30 | 164/0/533/0 | 697 | 40.5% | 6.9% | 1.21 | -3.9% | 189 | 1.38 | 7.6% | 343.1 | 7/7 | 0.86 | 1.10 | 0.12 | 5 | 23.5% | 0.34 | 0.36 | 37.1% | 34.2% | 41.4% | 35.0%/29.1% | 7.7 (interpolated) | pass | 0.121 (unverified) | 0.35 |
| 47 | `cfg_41f5` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=struct, target=none, exit=12:30 | 140/0/200/0 | 340 | 33.8% | 5.8% | 1.23 | -5.1% | 147 | 1.51 | 6.0% | 167.0 | 7/7 | 0.86 | 1.18 | 0.05 | 5 | 24.6% | 0.27 | 0.38 | 32.1% | 31.2% | 31.2% | 30.3%/24.3% | 13.1 (interpolated) | pass | 0.134 (unverified) | 0.64 |
| 48 | `cfg_1cbe` | timeframe=1min, level=box, side=both, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/154/620/0 | 774 | 52.3% | 8.6% | 1.27 | -5.3% | 130 | 1.43 | 15.8% | 383.9 | 7/7 | 0.86 | 1.24 | 0.03 | 5 | 25.3% | 0.52 | 0.38 | 48.0% | 41.2% | 41.1% | 44.8%/37.5% | 8.1 (interpolated) | pass | 0.146 (unverified) | 0.04 |
| 49 | `cfg_073a` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=range, exit=12:30 | 31/0/281/74 | 386 | 25.6% | 4.6% | 1.25 | -3.3% | 199 | 1.53 | 3.0% | 188.0 | 8/8 | 1.00 | 1.07 | 0.18 | 5 | 17.8% | 0.31 | 0.34 | 24.4% | 22.8% | 22.6% | 22.8%/19.4% | 9.7 (interpolated) | pass | 0.134 (unverified) | 0.42 |
| 50 | `cfg_a544` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=struct, target=none, exit=16:00 | 0/127/300/0 | 427 | 52.4% | 8.6% | 1.31 | -4.7% | 245 | 1.57 | 12.5% | 210.9 | 7/7 | 0.86 | 1.22 | 0.09 | 5 | 34.5% | 0.34 | 0.45 | 50.1% | 46.2% | 50.4% | 46.5%/39.3% | 15.3 (interpolated) | pass | 0.155 (unverified) | 0.49 |
| 51 | `cfg_19e3` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=none, exit=12:30 | 181/0/246/0 | 427 | 41.3% | 7.0% | 1.29 | -5.8% | 159 | 1.45 | 7.9% | 210.2 | 8/8 | 0.88 | 1.03 | 0.27 | 5 | 29.2% | 0.29 | 0.33 | 39.5% | 37.5% | 36.8% | 37.2%/29.3% | 12.7 (interpolated) | pass | 0.173 (unverified) | 0.15 |
| 52 | `cfg_58c2` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/128/482/0 | 610 | 41.6% | 7.0% | 1.25 | -4.9% | 206 | 1.46 | 12.9% | 299.5 | 8/8 | 0.88 | 1.02 | 0.23 | 4 | 20.5% | 0.41 | 0.38 | 39.4% | 35.1% | 34.9% | 37.7%/31.7% | 9.0 (interpolated) | pass | 0.133 (unverified) | 0.46 |
| 53 | `cfg_59df` | timeframe=1min, level=box, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/237/441/0 | 678 | 71.1% | 11.1% | 1.31 | -6.6% | 191 | 1.41 | 23.5% | 334.8 | 7/7 | 0.86 | 1.25 | 0.06 | 5 | 31.4% | 0.56 | 0.34 | 64.5% | 59.5% | 49.5% | 59.1%/49.3% | 11.7 (interpolated) | pass | 0.178 (unverified) | 0.27 |
| 54 | `cfg_4a9a` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=11:00 | 128/0/108/0 | 236 | 25.4% | 4.5% | 1.36 | -2.5% | 264 | 1.71 | 2.5% | 115.1 | 7/7 | 1.00 | 1.26 | 0.10 | 5 | 16.6% | 0.35 | 0.35 | 24.3% | 23.2% | 21.4% | 23.1%/19.1% | 14.5 (interpolated) | pass | 0.206 (unverified) | 0.72 |
| 55 | `cfg_df23` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=12:30 | 182/0/350/0 | 532 | 40.1% | 6.8% | 1.30 | -4.0% | 156 | 1.45 | 8.0% | 260.3 | 7/7 | 0.86 | 1.10 | 0.19 | 5 | 24.5% | 0.39 | 0.33 | 37.4% | 34.7% | 33.7% | 35.1%/28.2% | 9.7 (interpolated) | pass | 0.172 (unverified) | 0.22 |
| 56 | `cfg_4cec` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/224/448/0 | 672 | 69.4% | 10.8% | 1.26 | -9.4% | 273 | 1.38 | 22.7% | 334.3 | 7/7 | 0.86 | 1.16 | 0.10 | 4 | 30.1% | 0.57 | 0.37 | 62.9% | 59.9% | 65.0% | 57.8%/46.7% | 11.7 (interpolated) | pass | 0.146 (unverified) | 0.37 |
| 57 | `cfg_2cdb` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/79/267/0 | 346 | 33.7% | 5.8% | 1.32 | -5.7% | 399 | 1.74 | 8.2% | 169.2 | 8/8 | 1.00 | 1.10 | 0.22 | 4 | 20.1% | 0.35 | 0.43 | 32.0% | 30.3% | 26.1% | 30.7%/25.8% | 12.5 (interpolated) | pass | 0.156 (unverified) | 0.78 |
| 58 | `cfg_83b8` | timeframe=1min, level=box, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/133/545/0 | 678 | 51.8% | 8.5% | 1.31 | -4.6% | 219 | 1.49 | 14.0% | 334.7 | 8/8 | 0.88 | 1.19 | 0.11 | 5 | 24.4% | 0.53 | 0.37 | 45.8% | 40.6% | 39.1% | 43.3%/35.7% | 8.8 (interpolated) | pass | 0.166 (unverified) | 0.22 |
| 59 | `cfg_3cc0` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=12:30 | 277/0/395/0 | 672 | 50.3% | 8.3% | 1.23 | -6.4% | 160 | 1.33 | 12.3% | 335.4 | 8/8 | 0.88 | 1.00 | 0.24 | 4 | 28.9% | 0.43 | 0.30 | 48.2% | 43.3% | 50.1% | 45.1%/35.8% | 9.4 (interpolated) | pass | 0.145 (unverified) | 0.37 |
| 60 | `cfg_ef9e` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/124/548/0 | 672 | 43.8% | 7.4% | 1.16 | -4.8% | 160 | 1.43 | 13.4% | 328.8 | 8/8 | 0.88 | 1.16 | -0.00 | 5 | 21.6% | 0.51 | 0.42 | 42.0% | 37.9% | 51.4% | 40.0%/30.9% | 8.6 (interpolated) | pass | 0.088 (unverified) | 0.20 |
| 61 | `cfg_3194` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/103/429/0 | 532 | 37.4% | 6.4% | 1.16 | -3.5% | 130 | 1.48 | 11.0% | 260.9 | 7/7 | 0.86 | 1.25 | -0.10 | 5 | 19.4% | 0.48 | 0.43 | 35.7% | 33.8% | 28.0% | 34.7%/27.2% | 9.6 (interpolated) | pass | 0.085 (unverified) | 0.30 |
| 62 | `cfg_8689` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=16:00 | 0/97/272/0 | 369 | 38.9% | 6.6% | 1.28 | -3.6% | 230 | 1.66 | 9.5% | 181.8 | 7/7 | 1.00 | 1.19 | 0.09 | 5 | 16.8% | 0.57 | 0.40 | 36.1% | 33.2% | 38.0% | 32.4%/26.6% | 13.2 (interpolated) | pass | 0.141 (unverified) | 0.94 |
| 63 | `cfg_4ba2` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=3, mode=cont, stop=struct, target=none, exit=16:00 | 0/101/350/0 | 451 | 38.3% | 6.5% | 1.20 | -4.6% | 230 | 1.56 | 9.9% | 222.0 | 8/8 | 1.00 | 1.22 | -0.01 | 5 | 17.2% | 0.55 | 0.41 | 35.5% | 32.7% | 39.2% | 33.9%/25.9% | 11.1 (interpolated) | pass | 0.105 (unverified) | 0.94 |
| 64 | `cfg_b90a` | timeframe=1min, level=onh, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/66/266/0 | 332 | 35.9% | 6.2% | 1.27 | -4.4% | 284 | 1.82 | 7.0% | 162.4 | 8/8 | 1.00 | 1.24 | 0.02 | 4 | 15.3% | 0.57 | 0.46 | 34.2% | 31.8% | 20.8% | 32.5%/25.8% | 14.0 (interpolated) | pass | 0.124 (unverified) | 0.71 |
| 65 | `cfg_6263` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=12:30 | 94/0/292/0 | 386 | 29.3% | 5.2% | 1.22 | -3.1% | 178 | 1.59 | 4.4% | 188.6 | 8/8 | 1.00 | 1.11 | 0.11 | 5 | 18.7% | 0.36 | 0.45 | 27.2% | 25.4% | 22.7% | 25.3%/20.7% | 10.4 (interpolated) | pass | 0.110 (unverified) | 0.42 |
| 66 | `cfg_78f7` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=3R, exit=12:30 | 3/0/119/72 | 194 | 13.9% | 2.6% | 1.30 | -1.9% | 169 | 1.68 | 1.0% | 93.9 | 10/10 | 1.00 | 0.99 | 0.32 | 5 | 8.6% | 0.36 | 0.32 | 13.2% | 12.5% | 9.3% | 12.3%/10.0% | 12.3 (interpolated) | pass | 0.172 (unverified) | 0.49 |
| 67 | `cfg_8222` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/129/211/0 | 340 | 48.7% | 8.1% | 1.30 | -5.3% | 254 | 1.61 | 12.4% | 167.5 | 6/6 | 0.83 | 1.25 | 0.05 | 5 | 29.2% | 0.40 | 0.44 | 47.7% | 46.8% | 30.5% | 44.0%/36.4% | 17.7 (interpolated) | pass | 0.153 (unverified) | 0.30 |
| 68 | `cfg_0847` | timeframe=1min, level=box, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=12:30 | 219/0/459/0 | 678 | 45.8% | 7.6% | 1.31 | -5.0% | 123 | 1.40 | 9.6% | 334.7 | 8/8 | 0.88 | 1.15 | 0.16 | 5 | 26.7% | 0.42 | 0.32 | 40.3% | 33.9% | 39.3% | 37.6%/31.4% | 8.6 (interpolated) | pass | 0.186 (unverified) | 0.25 |
| 69 | `cfg_789f` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=11:00 | 105/0/88/0 | 193 | 24.8% | 4.4% | 1.42 | -3.3% | 274 | 1.89 | 2.1% | 94.1 | 6/6 | 1.00 | 1.34 | 0.08 | 5 | 15.7% | 0.37 | 0.35 | 24.0% | 23.4% | 22.2% | 22.6%/18.4% | 17.2 (interpolated) | pass | 0.251 (unverified) | 0.49 |
| 70 | `cfg_8025` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=struct, target=none, exit=16:00 | 0/116/224/0 | 340 | 42.1% | 7.1% | 1.18 | -5.8% | 191 | 1.56 | 11.3% | 166.8 | 6/6 | 0.83 | 1.24 | -0.06 | 5 | 26.8% | 0.36 | 0.51 | 39.0% | 36.9% | 38.0% | 34.9%/28.4% | 15.2 (interpolated) | pass | 0.090 (unverified) | 0.63 |
| 71 | `cfg_becf` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=12:30 | 89/0/183/68 | 340 | 33.3% | 5.8% | 1.33 | -5.3% | 265 | 1.51 | 5.2% | 167.2 | 8/8 | 0.88 | 1.11 | 0.22 | 5 | 23.2% | 0.30 | 0.30 | 31.3% | 30.5% | 22.5% | 30.1%/26.0% | 14.0 (interpolated) | pass | 0.196 (unverified) | 0.65 |
| 72 | `cfg_4749` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=12:30 | 124/0/336/0 | 460 | 33.8% | 5.9% | 1.31 | -5.0% | 159 | 1.51 | 5.6% | 228.0 | 9/9 | 1.00 | 1.11 | 0.20 | 5 | 16.5% | 0.46 | 0.38 | 31.0% | 29.2% | 31.0% | 30.1%/24.7% | 9.5 (interpolated) | pass | 0.175 (unverified) | 0.36 |
| 73 | `cfg_a260` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=12:30 | 197/0/250/0 | 447 | 36.7% | 6.3% | 1.26 | -3.5% | 140 | 1.41 | 8.7% | 219.1 | 9/9 | 1.00 | 1.15 | 0.11 | 5 | 22.0% | 0.34 | 0.32 | 34.9% | 33.3% | 34.5% | 31.7%/26.1% | 10.4 (interpolated) | pass | 0.157 (unverified) | 0.49 |
| 74 | `cfg_e2b0` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/61/235/0 | 296 | 37.1% | 6.4% | 1.33 | -3.0% | 148 | 1.90 | 6.4% | 145.5 | 9/9 | 1.00 | 1.22 | 0.11 | 5 | 20.8% | 0.44 | 0.44 | 35.9% | 34.5% | 22.4% | 33.1%/25.8% | 15.8 (interpolated) | pass | 0.155 (unverified) | 0.23 |
| 75 | `cfg_d2e7` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/120/266/0 | 386 | 33.7% | 5.8% | 0.96 | -5.9% | 363 | 1.39 | 12.5% | 186.3 | 6/6 | 1.00 | 1.03 | -0.08 | 4 | 16.7% | 0.50 | 0.51 | 32.1% | 30.4% | 33.4% | 28.6%/22.5% | 11.9 (interpolated) | pass | 0.034 (unverified) | -0.30 |
| 76 | `cfg_f878` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=12:30 | 97/0/272/0 | 369 | 29.9% | 5.2% | 1.29 | -3.4% | 438 | 1.65 | 4.3% | 180.3 | 9/9 | 1.00 | 1.15 | 0.14 | 5 | 13.1% | 0.56 | 0.42 | 27.6% | 25.8% | 18.0% | 26.3%/22.4% | 10.7 (interpolated) | pass | 0.147 (unverified) | 0.95 |
| 77 | `cfg_248d` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=12:30 | 88/0/208/0 | 296 | 22.8% | 4.1% | 1.27 | -3.1% | 208 | 1.66 | 3.8% | 144.8 | 8/8 | 1.00 | 1.21 | 0.06 | 5 | 16.2% | 0.29 | 0.42 | 21.8% | 20.7% | 14.0% | 20.5%/17.4% | 10.6 (interpolated) | pass | 0.136 (unverified) | 0.75 |
| 78 | `cfg_36cb` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/74/266/0 | 340 | 37.8% | 6.5% | 1.25 | -4.3% | 162 | 1.79 | 7.9% | 167.0 | 7/7 | 1.00 | 1.22 | 0.04 | 5 | 19.9% | 0.47 | 0.51 | 36.1% | 34.6% | 14.3% | 35.0%/26.8% | 14.6 (interpolated) | pass | 0.103 (unverified) | 0.22 |
| 79 | `cfg_975b` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/86/160/0 | 246 | 36.2% | 6.2% | 1.19 | -4.3% | 227 | 1.67 | 8.8% | 120.6 | 7/7 | 1.00 | 1.15 | 0.03 | 5 | 19.2% | 0.47 | 0.44 | 34.6% | 32.2% | 28.3% | 30.6%/24.4% | 18.7 (interpolated) | pass | 0.095 (unverified) | 0.05 |
| 80 | `cfg_a446` | timeframe=1min, level=onh, side=both, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/99/392/0 | 491 | 42.4% | 7.1% | 1.30 | -3.5% | 271 | 1.61 | 10.1% | 240.9 | 7/7 | 1.00 | 1.09 | 0.21 | 5 | 19.1% | 0.55 | 0.41 | 40.2% | 37.0% | 21.1% | 36.5%/29.7% | 11.0 (interpolated) | pass | 0.154 (unverified) | 0.75 |
| 81 | `cfg_7fd4` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=12:30 | 179/0/593/0 | 772 | 43.6% | 7.3% | 1.23 | -3.9% | 206 | 1.37 | 8.4% | 379.5 | 8/8 | 0.88 | 1.18 | 0.05 | 4 | 23.7% | 0.37 | 0.38 | 38.7% | 35.0% | 42.0% | 39.1%/30.9% | 7.5 (interpolated) | pass | 0.129 (unverified) | 0.21 |
| 82 | `cfg_a559` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=none, exit=12:30 | 68/0/156/0 | 224 | 22.4% | 4.0% | 1.29 | -2.2% | 136 | 1.84 | 3.0% | 109.4 | 9/9 | 1.00 | 1.12 | 0.17 | 5 | 16.4% | 0.27 | 0.44 | 21.6% | 20.6% | 13.2% | 20.8%/17.4% | 14.1 (interpolated) | pass | 0.141 (unverified) | 0.23 |
| 83 | `cfg_c66e` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=range, exit=16:00 | 0/12/109/71 | 192 | 24.0% | 4.3% | 1.22 | -3.7% | 347 | 1.72 | 3.5% | 93.8 | 7/7 | 1.00 | 1.22 | 0.01 | 4 | 12.7% | 0.42 | 0.42 | 23.4% | 22.8% | 20.9% | 21.4%/17.8% | 19.3 (interpolated) | pass | 0.121 (unverified) | 0.54 |
| 84 | `cfg_f160` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 114/0/337/0 | 451 | 32.7% | 5.7% | 1.28 | -2.6% | 177 | 1.56 | 5.2% | 220.8 | 10/10 | 1.00 | 1.14 | 0.13 | 5 | 17.3% | 0.47 | 0.38 | 30.5% | 27.0% | 19.7% | 28.1%/22.1% | 9.5 (interpolated) | pass | 0.144 (unverified) | 0.89 |
| 85 | `cfg_7f53` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=none, exit=11:00 | 126/0/120/0 | 246 | 23.8% | 4.3% | 1.25 | -2.8% | 210 | 1.61 | 2.6% | 120.1 | 7/7 | 1.00 | 1.23 | 0.02 | 5 | 16.2% | 0.32 | 0.39 | 22.7% | 21.4% | 17.6% | 20.8%/15.6% | 13.0 (interpolated) | pass | 0.134 (unverified) | 0.19 |
| 86 | `cfg_9993` | timeframe=1min, level=box, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/193/335/0 | 528 | 52.4% | 8.6% | 1.23 | -6.0% | 155 | 1.41 | 19.1% | 259.5 | 7/7 | 1.00 | 1.07 | 0.16 | 4 | 30.1% | 0.43 | 0.40 | 50.2% | 49.3% | 48.0% | 48.2%/40.9% | 12.3 (interpolated) | pass | 0.130 (unverified) | 0.29 |
| 87 | `cfg_f754` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=3R, exit=16:00 | 0/63/175/58 | 296 | 32.4% | 5.6% | 1.26 | -5.0% | 394 | 1.57 | 9.4% | 144.7 | 7/7 | 1.00 | 1.07 | 0.19 | 4 | 20.5% | 0.37 | 0.36 | 30.9% | 29.6% | 33.3% | 28.7%/21.8% | 14.1 (interpolated) | pass | 0.147 (unverified) | 0.67 |
| 88 | `cfg_6765` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/55/169/0 | 224 | 32.0% | 5.6% | 1.25 | -2.4% | 136 | 2.09 | 5.5% | 108.8 | 8/8 | 1.00 | 1.08 | 0.17 | 4 | 17.4% | 0.46 | 0.55 | 31.2% | 30.5% | 11.9% | 29.7%/24.2% | 18.4 (interpolated) | pass | 0.088 (unverified) | 0.40 |
| 89 | `cfg_1be4` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=none, exit=12:30 | 124/0/172/0 | 296 | 31.0% | 5.4% | 1.21 | -3.1% | 345 | 1.56 | 5.5% | 144.6 | 9/9 | 1.00 | 1.02 | 0.19 | 5 | 16.9% | 0.46 | 0.41 | 29.0% | 27.6% | 27.5% | 26.9%/21.6% | 14.1 (interpolated) | pass | 0.117 (unverified) | 0.77 |
| 90 | `cfg_fdc7` | timeframe=1min, level=onh, side=both, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/115/469/0 | 584 | 45.2% | 7.6% | 1.29 | -3.4% | 212 | 1.54 | 12.0% | 286.8 | 8/8 | 1.00 | 1.04 | 0.25 | 4 | 22.2% | 0.51 | 0.39 | 43.1% | 40.0% | 34.0% | 40.4%/32.7% | 9.9 (interpolated) | pass | 0.152 (unverified) | 0.71 |
| 91 | `cfg_9be7` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/119/508/0 | 627 | 44.6% | 7.5% | 1.23 | -4.5% | 208 | 1.49 | 12.2% | 307.5 | 8/8 | 1.00 | 1.08 | 0.15 | 5 | 18.0% | 0.60 | 0.40 | 42.7% | 39.3% | 36.4% | 40.6%/32.8% | 9.3 (interpolated) | pass | 0.119 (unverified) | 0.67 |
| 92 | `cfg_31b3` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/88/339/0 | 427 | 38.6% | 6.6% | 1.26 | -5.2% | 160 | 1.59 | 9.1% | 210.4 | 8/8 | 0.88 | 1.20 | 0.06 | 5 | 25.0% | 0.29 | 0.42 | 36.7% | 34.7% | 25.4% | 35.9%/28.8% | 11.9 (interpolated) | pass | 0.128 (unverified) | 0.20 |
| 93 | `cfg_3982` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/96/341/0 | 437 | 29.8% | 5.2% | 1.17 | -6.0% | 350 | 1.52 | 9.9% | 212.0 | 7/7 | 1.00 | 1.11 | 0.06 | 4 | 15.7% | 0.39 | 0.46 | 28.0% | 25.3% | 29.6% | 25.6%/21.9% | 9.3 (interpolated) | pass | 0.089 (unverified) | 0.63 |
| 94 | `cfg_4285` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=none, exit=12:30 | 112/0/295/0 | 407 | 31.3% | 5.5% | 1.29 | -4.2% | 142 | 1.60 | 5.0% | 197.1 | 9/9 | 0.89 | 1.17 | 0.12 | 5 | 17.8% | 0.43 | 0.40 | 29.6% | 28.0% | 15.5% | 28.1%/23.8% | 10.9 (interpolated) | pass | 0.153 (unverified) | 0.21 |
| 95 | `cfg_cb68` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=12:30 | 79/0/194/0 | 273 | 22.3% | 4.0% | 1.23 | -2.9% | 188 | 1.66 | 3.5% | 133.1 | 9/9 | 1.00 | 1.07 | 0.16 | 4 | 15.7% | 0.30 | 0.42 | 21.6% | 20.4% | 17.0% | 20.5%/16.8% | 11.6 (interpolated) | pass | 0.123 (unverified) | 0.85 |
| 96 | `cfg_1ba2` | timeframe=1min, level=onh, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 83/0/85/0 | 168 | 20.8% | 3.8% | 1.24 | -3.0% | 181 | 1.81 | 3.5% | 82.0 | 7/7 | 1.00 | 1.19 | 0.06 | 5 | 14.2% | 0.32 | 0.45 | 20.1% | 19.2% | 19.0% | 18.2%/15.5% | 17.0 (interpolated) | pass | 0.131 (unverified) | 0.82 |
| 97 | `cfg_cfa4` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=1, mode=cont, stop=struct, target=range, exit=16:00 | 0/19/370/92 | 481 | 28.4% | 5.0% | 1.15 | -3.8% | 206 | 1.44 | 5.0% | 234.6 | 8/8 | 1.00 | 1.04 | 0.12 | 4 | 19.1% | 0.33 | 0.40 | 25.2% | 23.5% | 22.6% | 25.0%/20.1% | 8.1 (interpolated) | pass | 0.089 (unverified) | 0.33 |
| 98 | `cfg_41ed` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 109/0/318/0 | 427 | 34.1% | 5.9% | 1.31 | -4.7% | 153 | 1.57 | 5.0% | 210.4 | 9/9 | 0.89 | 1.17 | 0.13 | 5 | 21.3% | 0.32 | 0.39 | 32.2% | 30.9% | 24.5% | 30.4%/25.9% | 10.6 (interpolated) | pass | 0.162 (unverified) | 0.28 |
| 99 | `cfg_4955` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 102/0/244/0 | 346 | 23.3% | 4.2% | 1.23 | -4.8% | 314 | 1.58 | 4.4% | 169.4 | 9/9 | 1.00 | 1.08 | 0.15 | 4 | 15.2% | 0.31 | 0.43 | 22.1% | 21.0% | 18.7% | 20.8%/17.8% | 9.5 (interpolated) | pass | 0.116 (unverified) | 0.83 |
| 100 | `cfg_e2e3` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=12:30 | 131/0/401/0 | 532 | 28.6% | 5.0% | 1.10 | -3.3% | 283 | 1.41 | 6.2% | 260.2 | 8/8 | 0.88 | 1.16 | -0.06 | 5 | 16.2% | 0.44 | 0.45 | 26.1% | 24.6% | 19.7% | 26.4%/20.1% | 7.6 (interpolated) | pass | 0.070 (unverified) | 0.23 |
| 101 | `cfg_387c` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 73/0/173/0 | 246 | 20.7% | 3.7% | 1.23 | -2.3% | 186 | 1.73 | 1.7% | 120.4 | 8/8 | 1.00 | 1.11 | 0.12 | 5 | 14.0% | 0.31 | 0.45 | 19.4% | 18.7% | 8.4% | 18.4%/14.7% | 11.2 (interpolated) | pass | 0.110 (unverified) | 0.13 |
| 102 | `cfg_e2b9` | timeframe=1min, level=box, side=both, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/172/736/0 | 908 | 55.3% | 9.0% | 1.24 | -6.5% | 168 | 1.39 | 17.9% | 445.2 | 8/8 | 0.88 | 1.10 | 0.13 | 5 | 23.4% | 0.58 | 0.36 | 48.8% | 44.1% | 62.2% | 48.5%/36.8% | 7.7 (interpolated) | pass | 0.130 (unverified) | 0.01 |
| 103 | `cfg_8d79` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=struct, target=none, exit=12:30 | 83/0/163/0 | 246 | 25.5% | 4.5% | 1.16 | -2.6% | 215 | 1.63 | 3.8% | 120.0 | 8/8 | 1.00 | 1.12 | 0.04 | 5 | 17.2% | 0.33 | 0.48 | 24.0% | 23.4% | 23.9% | 22.3%/18.1% | 13.9 (interpolated) | pass | 0.082 (unverified) | 0.52 |
| 104 | `cfg_43f5` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=12:30 | 64/0/160/0 | 224 | 20.1% | 3.6% | 1.19 | -2.4% | 189 | 1.75 | 3.0% | 108.3 | 8/8 | 1.00 | 1.02 | 0.17 | 5 | 12.1% | 0.40 | 0.47 | 19.4% | 17.7% | 14.6% | 18.3%/14.7% | 12.3 (interpolated) | pass | 0.097 (unverified) | 0.61 |
| 105 | `cfg_6dcc` | timeframe=1min, level=onh, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 82/0/250/0 | 332 | 26.1% | 4.6% | 1.19 | -3.6% | 222 | 1.66 | 3.8% | 160.6 | 9/9 | 1.00 | 1.14 | 0.05 | 4 | 11.5% | 0.56 | 0.46 | 24.4% | 23.0% | 12.9% | 23.5%/18.9% | 10.8 (interpolated) | pass | 0.091 (unverified) | 0.75 |
| 106 | `cfg_0b0e` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=12:30 | 101/0/222/84 | 407 | 33.5% | 5.8% | 1.25 | -5.8% | 245 | 1.42 | 6.1% | 199.0 | 9/9 | 0.89 | 1.07 | 0.17 | 5 | 22.4% | 0.31 | 0.29 | 31.1% | 29.9% | 19.3% | 29.6%/22.3% | 11.8 (interpolated) | pass | 0.151 (unverified) | 0.48 |
| 107 | `cfg_c073` | timeframe=1min, level=onh, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/44/124/0 | 168 | 22.3% | 4.0% | 1.19 | -2.8% | 401 | 2.12 | 4.3% | 81.5 | 7/7 | 1.00 | 1.14 | 0.05 | 4 | 11.6% | 0.48 | 0.56 | 21.6% | 20.7% | 12.4% | 20.0%/14.0% | 17.8 (interpolated) | pass | 0.072 (unverified) | 0.35 |
| 108 | `cfg_81e1` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=range, exit=12:30 | 43/0/200/52 | 295 | 18.7% | 3.4% | 1.20 | -2.4% | 177 | 1.57 | 2.8% | 144.1 | 9/9 | 1.00 | 1.11 | 0.09 | 4 | 12.5% | 0.31 | 0.42 | 17.6% | 16.8% | 12.0% | 16.6%/13.5% | 9.5 (interpolated) | pass | 0.105 (unverified) | 0.78 |
| 109 | `cfg_4119` | timeframe=1min, level=box, side=both, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/268/548/0 | 816 | 66.7% | 10.5% | 1.16 | -7.0% | 237 | 1.31 | 27.1% | 405.1 | 8/8 | 0.88 | 1.03 | 0.14 | 4 | 26.6% | 0.60 | 0.35 | 60.9% | 53.5% | 65.4% | 56.9%/44.0% | 9.2 (interpolated) | pass | 0.104 (unverified) | 0.32 |
| 110 | `cfg_9a9f` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 71/0/73/0 | 144 | 19.9% | 3.6% | 1.22 | -3.3% | 216 | 1.90 | 3.1% | 70.4 | 8/8 | 1.00 | 1.12 | 0.10 | 4 | 13.0% | 0.35 | 0.47 | 19.2% | 18.7% | 18.0% | 17.8%/13.6% | 18.9 (interpolated) | pass | 0.119 (unverified) | 0.90 |
| 111 | `cfg_413e` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=none, exit=12:30 | 148/0/238/0 | 386 | 30.7% | 5.4% | 1.06 | -4.6% | 186 | 1.40 | 6.9% | 187.3 | 7/7 | 1.00 | 0.89 | 0.17 | 5 | 19.8% | 0.36 | 0.45 | 28.5% | 25.3% | 29.8% | 26.2%/19.7% | 10.6 (interpolated) | pass | 0.063 (unverified) | 0.14 |
| 112 | `cfg_9b4a` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=3R, exit=12:30 | 131/0/246/70 | 447 | 33.6% | 5.8% | 1.20 | -3.4% | 138 | 1.38 | 7.5% | 221.5 | 10/10 | 1.00 | 1.07 | 0.13 | 5 | 23.5% | 0.30 | 0.32 | 31.6% | 29.3% | 31.4% | 29.6%/24.0% | 10.2 (interpolated) | pass | 0.126 (unverified) | 0.49 |
| 113 | `cfg_3a9a` | timeframe=1min, level=box, side=both, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/92/351/0 | 443 | 37.9% | 6.5% | 1.19 | -5.2% | 206 | 1.60 | 9.6% | 214.5 | 7/7 | 0.86 | 1.22 | -0.03 | 5 | 17.8% | 0.53 | 0.49 | 36.8% | 34.9% | 16.7% | 34.3%/28.1% | 11.1 (interpolated) | pass | 0.085 (unverified) | 0.10 |
| 114 | `cfg_3bfd` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 167/0/207/0 | 374 | 31.6% | 5.5% | 1.21 | -4.0% | 171 | 1.44 | 7.2% | 185.8 | 8/8 | 0.88 | 1.01 | 0.20 | 5 | 23.4% | 0.26 | 0.35 | 30.0% | 28.3% | 29.8% | 27.4%/22.4% | 10.9 (interpolated) | pass | 0.124 (unverified) | 0.45 |
| 115 | `cfg_d91b` | timeframe=1min, level=onh, side=both, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/190/394/0 | 584 | 40.4% | 6.9% | 0.99 | -6.1% | 200 | 1.30 | 19.1% | 285.6 | 7/7 | 1.00 | 0.91 | 0.08 | 4 | 21.5% | 0.47 | 0.43 | 37.8% | 35.7% | 49.0% | 36.3%/30.0% | 9.0 (interpolated) | pass | 0.047 (unverified) | 0.47 |
| 116 | `cfg_35a5` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/157/280/0 | 437 | 38.2% | 6.5% | 1.14 | -6.1% | 149 | 1.39 | 15.6% | 214.4 | 6/6 | 1.00 | 1.03 | 0.11 | 4 | 23.1% | 0.34 | 0.42 | 35.9% | 33.0% | 32.9% | 33.9%/25.8% | 11.2 (interpolated) | pass | 0.087 (unverified) | 0.56 |
| 117 | `cfg_6fa6` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/64/209/0 | 273 | 27.1% | 4.8% | 1.24 | -3.9% | 183 | 1.75 | 6.6% | 132.5 | 8/8 | 1.00 | 1.07 | 0.17 | 4 | 14.8% | 0.45 | 0.44 | 25.2% | 23.6% | 17.9% | 23.7%/19.1% | 13.5 (interpolated) | pass | 0.117 (unverified) | 0.72 |
| 118 | `cfg_beff` | timeframe=1min, level=onh, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=12:30 | 60/0/84/24 | 168 | 19.0% | 3.4% | 1.19 | -3.0% | 305 | 1.74 | 3.1% | 82.3 | 8/8 | 1.00 | 1.11 | 0.09 | 5 | 12.8% | 0.33 | 0.45 | 18.3% | 17.2% | 17.6% | 17.0%/13.6% | 16.7 (interpolated) | pass | 0.109 (unverified) | 0.75 |
| 119 | `cfg_fbc4` | timeframe=1min, level=onh, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/107/225/0 | 332 | 35.4% | 6.1% | 1.07 | -5.8% | 281 | 1.49 | 10.8% | 162.7 | 7/7 | 1.00 | 1.02 | 0.05 | 5 | 16.3% | 0.54 | 0.46 | 32.6% | 30.4% | 37.1% | 31.1%/23.6% | 13.6 (interpolated) | pass | 0.059 (unverified) | 0.70 |
| 120 | `cfg_9cd3` | timeframe=1min, level=box, side=both, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/163/280/0 | 443 | 53.0% | 8.7% | 1.24 | -7.0% | 252 | 1.50 | 15.6% | 218.5 | 6/6 | 0.83 | 1.22 | 0.03 | 5 | 28.8% | 0.46 | 0.43 | 48.1% | 45.9% | 28.6% | 47.1%/37.9% | 14.5 (interpolated) | pass | 0.126 (unverified) | 0.30 |
| 121 | `cfg_46e9` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=range, exit=16:00 | 0/15/293/78 | 386 | 21.8% | 3.9% | 1.07 | -3.5% | 221 | 1.46 | 3.9% | 186.5 | 8/8 | 1.00 | 1.03 | 0.04 | 5 | 11.8% | 0.46 | 0.42 | 19.3% | 17.7% | 16.4% | 18.9%/15.0% | 8.6 (interpolated) | pass | 0.069 (unverified) | 0.29 |
| 122 | `cfg_664f` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 182/0/225/0 | 407 | 39.6% | 6.7% | 1.32 | -5.6% | 183 | 1.49 | 7.7% | 198.7 | 8/8 | 0.88 | 1.22 | 0.10 | 5 | 26.5% | 0.33 | 0.33 | 35.0% | 33.0% | 23.7% | 34.0%/28.5% | 12.2 (interpolated) | pass | 0.187 (unverified) | 0.40 |
| 123 | `cfg_72af` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=12:30 | 40/0/62/20 | 122 | 17.2% | 3.1% | 1.18 | -3.3% | 378 | 1.93 | 2.2% | 58.7 | 8/8 | 1.00 | 1.03 | 0.16 | 4 | 9.1% | 0.47 | 0.50 | 16.6% | 15.9% | 15.5% | 15.9%/12.9% | 20.5 (interpolated) | pass | 0.097 (unverified) | 0.63 |
| 124 | `cfg_148f` | timeframe=1min, level=box, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 291/0/387/0 | 678 | 44.8% | 7.5% | 1.16 | -5.7% | 270 | 1.32 | 12.5% | 331.4 | 8/8 | 0.88 | 1.13 | 0.03 | 4 | 21.2% | 0.53 | 0.33 | 40.2% | 37.5% | 35.6% | 39.5%/30.2% | 8.4 (interpolated) | pass | 0.108 (unverified) | 0.28 |
| 125 | `cfg_ce54` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=12:30 | 185/0/587/0 | 772 | 38.5% | 6.6% | 1.15 | -7.7% | 147 | 1.34 | 8.5% | 380.9 | 9/9 | 0.89 | 1.10 | 0.05 | 5 | 20.2% | 0.40 | 0.38 | 35.1% | 32.8% | 34.2% | 33.6%/27.7% | 6.9 (interpolated) | pass | 0.091 (unverified) | 0.21 |
| 126 | `cfg_0b4b` | timeframe=1min, level=onh, side=both, window=15, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=12:30 | 87/0/169/0 | 256 | 26.2% | 4.7% | 1.22 | -4.6% | 241 | 1.73 | 3.7% | 124.6 | 7/7 | 1.00 | 1.14 | 0.09 | 5 | 11.2% | 0.57 | 0.45 | 25.1% | 23.3% | 25.1% | 23.5%/18.7% | 13.6 (interpolated) | pass | 0.110 (unverified) | 0.59 |
| 127 | `cfg_40b4` | timeframe=1min, level=box, side=high, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=none, exit=12:30 | 57/0/138/0 | 195 | 18.2% | 3.3% | 1.14 | -2.2% | 206 | 1.80 | 2.6% | 95.1 | 8/8 | 1.00 | 0.98 | 0.16 | 5 | 12.2% | 0.33 | 0.54 | 17.7% | 16.6% | 9.1% | 16.3%/13.6% | 13.0 (interpolated) | pass | 0.066 (unverified) | 0.35 |
| 128 | `cfg_ccca` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=1, mode=cont, stop=d0.10, target=none, exit=12:30 | 121/0/316/0 | 437 | 24.3% | 4.3% | 1.18 | -4.6% | 264 | 1.46 | 5.3% | 212.5 | 8/8 | 1.00 | 1.10 | 0.08 | 4 | 11.0% | 0.48 | 0.40 | 22.7% | 21.1% | 24.8% | 21.1%/17.8% | 7.8 (interpolated) | pass | 0.102 (unverified) | 0.71 |
| 129 | `cfg_a301` | timeframe=1min, level=box, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/56/186/0 | 242 | 29.9% | 5.2% | 1.15 | -2.6% | 170 | 1.92 | 5.8% | 117.8 | 7/7 | 1.00 | 1.02 | 0.13 | 4 | 16.4% | 0.45 | 0.59 | 28.0% | 26.8% | 9.7% | 26.1%/21.2% | 16.0 (interpolated) | pass | 0.056 (unverified) | 0.29 |
| 130 | `cfg_e38c` | timeframe=1min, level=lon, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=2R, exit=12:30 | 0/0/87/77 | 164 | 8.7% | 1.6% | 1.18 | -1.2% | 153 | 1.61 | 0.4% | 79.7 | 9/9 | 1.00 | 0.77 | 0.40 | 5 | 5.1% | 0.41 | 0.32 | 8.2% | 7.6% | 7.1% | 8.0%/6.5% | 9.8 (interpolated) | pass | 0.115 (unverified) | -0.12 |
| 131 | `cfg_6f6a` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=12:30 | 164/0/533/0 | 697 | 34.8% | 6.0% | 1.10 | -7.5% | 144 | 1.34 | 7.6% | 344.4 | 8/8 | 0.88 | 0.95 | 0.15 | 5 | 19.6% | 0.38 | 0.41 | 32.8% | 30.5% | 28.7% | 32.3%/26.4% | 7.1 (interpolated) | pass | 0.072 (unverified) | 0.23 |
| 132 | `cfg_6317` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=struct, target=none, exit=12:30 | 96/0/177/0 | 273 | 24.0% | 4.3% | 1.11 | -2.8% | 159 | 1.52 | 4.4% | 132.9 | 9/9 | 1.00 | 1.00 | 0.12 | 5 | 15.2% | 0.32 | 0.46 | 22.9% | 20.3% | 21.8% | 21.1%/16.9% | 12.1 (interpolated) | pass | 0.076 (unverified) | 0.57 |
| 133 | `cfg_632d` | timeframe=1min, level=onh, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/66/102/0 | 168 | 27.2% | 4.8% | 1.21 | -4.1% | 376 | 1.84 | 6.7% | 82.1 | 6/6 | 1.00 | 1.14 | 0.07 | 4 | 15.2% | 0.44 | 0.48 | 25.4% | 24.3% | 24.0% | 24.2%/20.5% | 20.9 (interpolated) | pass | 0.098 (unverified) | 0.49 |
| 134 | `cfg_798e` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=12:30 | 59/0/135/0 | 194 | 19.8% | 3.6% | 1.25 | -2.7% | 98 | 1.84 | 2.7% | 93.6 | 9/9 | 1.00 | 0.94 | 0.31 | 5 | 11.2% | 0.39 | 0.48 | 19.1% | 17.9% | 13.7% | 18.2%/14.2% | 14.7 (interpolated) | pass | 0.113 (unverified) | 0.62 |
| 135 | `cfg_a217` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=range, exit=12:30 | 57/0/236/53 | 346 | 20.0% | 3.6% | 1.20 | -4.0% | 254 | 1.52 | 3.5% | 169.4 | 10/10 | 1.00 | 1.06 | 0.14 | 4 | 12.0% | 0.37 | 0.40 | 18.6% | 17.5% | 17.1% | 17.7%/13.9% | 8.7 (interpolated) | pass | 0.104 (unverified) | 0.84 |
| 136 | `cfg_f8d5` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/136/238/0 | 374 | 44.6% | 7.5% | 1.23 | -4.2% | 171 | 1.52 | 13.5% | 183.6 | 7/7 | 0.86 | 1.09 | 0.13 | 5 | 25.4% | 0.43 | 0.44 | 42.9% | 40.6% | 43.6% | 38.6%/30.7% | 14.1 (interpolated) | pass | 0.117 (unverified) | 0.38 |
| 137 | `cfg_c23c` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 155/0/517/0 | 672 | 33.3% | 5.8% | 1.09 | -4.7% | 152 | 1.36 | 7.5% | 328.0 | 9/9 | 0.89 | 1.10 | -0.01 | 4 | 19.4% | 0.42 | 0.40 | 30.3% | 27.4% | 38.0% | 30.1%/22.4% | 6.9 (interpolated) | pass | 0.070 (unverified) | 0.15 |
| 138 | `cfg_5c8f` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=none, exit=12:30 | 198/0/239/0 | 437 | 30.2% | 5.3% | 1.16 | -4.2% | 158 | 1.37 | 8.2% | 214.8 | 7/7 | 1.00 | 0.96 | 0.21 | 4 | 20.0% | 0.33 | 0.36 | 28.2% | 26.8% | 26.0% | 27.3%/20.7% | 9.2 (interpolated) | pass | 0.107 (unverified) | 0.59 |
| 139 | `cfg_1965` | timeframe=1min, level=lon, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=2R, exit=16:00 | 0/0/87/77 | 164 | 8.7% | 1.6% | 1.18 | -1.2% | 153 | 1.61 | 0.4% | 79.7 | 8/8 | 1.00 | 0.75 | 0.43 | 5 | 5.1% | 0.41 | 0.32 | 8.2% | 7.6% | 7.1% | 7.8%/6.4% | 9.8 (interpolated) | pass | 0.115 (unverified) | -0.13 |
| 140 | `cfg_a5a7` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/99/197/0 | 296 | 38.2% | 6.5% | 1.15 | -3.6% | 345 | 1.57 | 10.2% | 144.8 | 8/8 | 1.00 | 1.07 | 0.08 | 5 | 16.2% | 0.58 | 0.43 | 37.6% | 36.0% | 34.0% | 31.9%/24.4% | 16.2 (interpolated) | pass | 0.085 (unverified) | 0.43 |
| 141 | `cfg_5f2d` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/52/184/0 | 236 | 26.6% | 4.7% | 1.17 | -2.7% | 495 | 1.91 | 5.1% | 113.7 | 8/8 | 1.00 | 1.20 | -0.03 | 4 | 9.4% | 0.65 | 0.53 | 25.3% | 24.6% | 16.4% | 24.3%/20.6% | 15.5 (interpolated) | pass | 0.067 (unverified) | 0.41 |
| 142 | `cfg_6bbb` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=12:30 | 117/0/252/0 | 369 | 27.4% | 4.8% | 1.16 | -4.8% | 327 | 1.53 | 5.0% | 180.2 | 8/8 | 1.00 | 1.03 | 0.13 | 5 | 12.4% | 0.55 | 0.43 | 25.8% | 23.7% | 27.0% | 24.4%/19.4% | 10.2 (interpolated) | pass | 0.089 (unverified) | 0.79 |
| 143 | `cfg_6745` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=11:00 | 198/0/171/0 | 369 | 28.4% | 5.0% | 1.26 | -3.4% | 202 | 1.48 | 3.8% | 181.1 | 7/7 | 1.00 | 1.04 | 0.22 | 4 | 16.5% | 0.42 | 0.34 | 26.5% | 23.7% | 18.9% | 25.3%/18.5% | 10.2 (interpolated) | pass | 0.152 (unverified) | 0.95 |
| 144 | `cfg_d7c4` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=3, mode=cont, stop=struct, target=none, exit=12:30 | 97/0/199/0 | 296 | 25.4% | 4.5% | 1.09 | -2.5% | 211 | 1.53 | 4.4% | 145.0 | 9/9 | 1.00 | 1.06 | 0.03 | 5 | 17.2% | 0.32 | 0.49 | 23.3% | 22.2% | 24.0% | 22.5%/18.2% | 11.6 (interpolated) | pass | 0.064 (unverified) | 0.70 |
| 145 | `cfg_1e60` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/144/307/0 | 451 | 33.5% | 5.8% | 0.91 | -6.1% | 265 | 1.32 | 14.6% | 221.6 | 8/8 | 1.00 | 1.06 | -0.15 | 5 | 16.8% | 0.50 | 0.49 | 32.0% | 27.8% | 37.8% | 29.8%/22.5% | 10.0 (interpolated) | pass | 0.029 (unverified) | 0.82 |
| 146 | `cfg_2bd4` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=12:30 | 111/0/349/0 | 460 | 28.0% | 4.9% | 1.11 | -4.1% | 120 | 1.42 | 5.3% | 228.0 | 8/8 | 0.88 | 1.05 | 0.05 | 4 | 12.2% | 0.50 | 0.45 | 26.7% | 24.3% | 31.1% | 25.4%/18.5% | 8.5 (interpolated) | pass | 0.078 (unverified) | 0.67 |
| 147 | `cfg_47c6` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=16:00 | 0/96/364/0 | 460 | 39.1% | 6.7% | 1.17 | -4.8% | 185 | 1.55 | 9.6% | 228.4 | 7/7 | 0.86 | 1.11 | 0.06 | 4 | 19.8% | 0.40 | 0.52 | 37.7% | 36.2% | 42.8% | 35.5%/29.7% | 11.1 (interpolated) | pass | 0.082 (unverified) | 0.71 |
| 148 | `cfg_7f1d` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=3R, exit=12:30 | 103/0/243/81 | 427 | 31.4% | 5.5% | 1.13 | -5.7% | 179 | 1.35 | 6.3% | 211.3 | 9/9 | 0.89 | 0.76 | 0.37 | 5 | 22.5% | 0.28 | 0.33 | 30.0% | 28.2% | 31.7% | 28.1%/22.7% | 11.0 (interpolated) | pass | 0.094 (unverified) | 0.16 |
| 149 | `cfg_1afd` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=struct, target=range, exit=16:00 | 0/14/161/71 | 246 | 22.3% | 4.0% | 1.11 | -3.0% | 215 | 1.58 | 3.3% | 119.9 | 8/8 | 1.00 | 1.07 | 0.04 | 5 | 14.5% | 0.35 | 0.47 | 21.5% | 21.0% | 21.3% | 19.8%/16.8% | 13.3 (interpolated) | pass | 0.068 (unverified) | 0.36 |
| 150 | `cfg_310f` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=struct, target=none, exit=12:30 | 74/0/119/0 | 193 | 22.2% | 4.0% | 1.10 | -2.9% | 227 | 1.69 | 3.2% | 93.7 | 7/7 | 1.00 | 1.12 | -0.02 | 5 | 13.5% | 0.39 | 0.52 | 21.6% | 21.0% | 23.1% | 19.9%/15.3% | 15.7 (interpolated) | pass | 0.063 (unverified) | 0.60 |
| 151 | `cfg_ba63` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 87/0/209/0 | 296 | 20.8% | 3.8% | 1.17 | -2.7% | 138 | 1.59 | 2.0% | 144.8 | 9/9 | 1.00 | 1.02 | 0.15 | 5 | 14.3% | 0.31 | 0.45 | 19.8% | 18.4% | 8.6% | 18.6%/15.6% | 9.6 (interpolated) | pass | 0.089 (unverified) | 0.29 |
| 152 | `cfg_0856` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=struct, target=3R, exit=12:30 | 62/0/195/83 | 340 | 28.3% | 5.0% | 1.15 | -4.4% | 178 | 1.44 | 4.2% | 167.0 | 8/8 | 0.88 | 0.96 | 0.18 | 5 | 20.4% | 0.28 | 0.40 | 26.0% | 24.7% | 21.5% | 24.7%/20.7% | 12.3 (interpolated) | pass | 0.097 (unverified) | 0.49 |
| 153 | `cfg_90e7` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 118/0/329/0 | 447 | 26.5% | 4.7% | 1.16 | -3.1% | 123 | 1.45 | 5.6% | 219.9 | 10/10 | 0.90 | 0.96 | 0.20 | 5 | 12.2% | 0.48 | 0.44 | 23.6% | 21.3% | 31.8% | 22.8%/18.6% | 8.3 (interpolated) | pass | 0.088 (unverified) | 0.18 |
| 154 | `cfg_8f3e` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/44/149/0 | 193 | 26.2% | 4.7% | 1.21 | -3.0% | 229 | 2.13 | 4.3% | 92.6 | 7/7 | 1.00 | 1.21 | 0.00 | 4 | 9.8% | 0.63 | 0.54 | 25.6% | 24.8% | 20.4% | 24.1%/18.8% | 18.4 (interpolated) | pass | 0.079 (unverified) | 0.34 |
| 155 | `cfg_dfce` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=12:30 | 51/0/72/21 | 144 | 17.4% | 3.2% | 1.15 | -3.3% | 376 | 1.79 | 2.7% | 70.2 | 9/9 | 1.00 | 1.09 | 0.05 | 4 | 11.2% | 0.36 | 0.49 | 17.2% | 16.7% | 16.4% | 16.1%/12.6% | 18.4 (interpolated) | pass | 0.088 (unverified) | 0.86 |
| 156 | `cfg_f610` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=12:30 | 160/0/186/0 | 346 | 22.6% | 4.1% | 1.03 | -5.3% | 208 | 1.38 | 6.6% | 169.4 | 8/8 | 1.00 | 1.00 | 0.03 | 4 | 13.5% | 0.39 | 0.44 | 21.5% | 20.0% | 25.8% | 20.8%/16.4% | 9.3 (interpolated) | pass | 0.057 (unverified) | 0.66 |
| 157 | `cfg_0e56` | timeframe=1min, level=onh, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=12:30 | 129/0/203/0 | 332 | 26.4% | 4.7% | 1.02 | -5.3% | 264 | 1.42 | 5.8% | 162.9 | 8/8 | 1.00 | 0.98 | 0.03 | 5 | 13.8% | 0.48 | 0.45 | 23.9% | 22.1% | 26.8% | 22.2%/17.5% | 10.9 (interpolated) | pass | 0.050 (unverified) | 0.91 |
| 158 | `cfg_d9ce` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=struct, target=none, exit=12:30 | 125/0/322/0 | 447 | 26.1% | 4.6% | 1.10 | -4.3% | 235 | 1.43 | 5.7% | 219.3 | 9/9 | 0.89 | 1.06 | 0.04 | 4 | 11.7% | 0.49 | 0.44 | 22.9% | 21.0% | 25.6% | 23.0%/17.3% | 8.3 (interpolated) | pass | 0.072 (unverified) | 0.45 |
| 159 | `cfg_9bee` | timeframe=1min, level=lon, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=3R, exit=12:30 | 2/0/100/62 | 164 | 10.3% | 1.9% | 1.12 | -1.4% | 165 | 1.62 | 0.9% | 79.7 | 9/9 | 1.00 | 0.96 | 0.15 | 4 | 7.4% | 0.28 | 0.38 | 9.8% | 9.3% | 7.1% | 9.3%/7.7% | 11.1 (interpolated) | pass | 0.080 (unverified) | 0.27 |
| 160 | `cfg_f691` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=5, mode=cont, stop=struct, target=3R, exit=12:30 | 75/0/328/129 | 532 | 31.3% | 5.5% | 1.21 | -3.7% | 140 | 1.38 | 5.3% | 259.2 | 8/8 | 0.88 | 0.71 | 0.50 | 5 | 17.7% | 0.43 | 0.34 | 28.3% | 27.0% | 25.3% | 27.8%/22.8% | 8.8 (interpolated) | pass | 0.130 (unverified) | 0.09 |
| 161 | `cfg_699b` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=struct, target=none, exit=16:00 | 0/84/189/0 | 273 | 32.8% | 5.7% | 1.13 | -3.5% | 181 | 1.66 | 8.2% | 132.2 | 8/8 | 1.00 | 1.07 | 0.06 | 4 | 20.6% | 0.37 | 0.56 | 31.7% | 30.3% | 31.8% | 29.0%/24.1% | 16.0 (interpolated) | pass | 0.062 (unverified) | 0.72 |
| 162 | `cfg_8866` | timeframe=1min, level=box, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=12:30 | 239/0/289/0 | 528 | 33.4% | 5.8% | 1.12 | -4.9% | 163 | 1.31 | 10.1% | 261.2 | 8/8 | 0.88 | 0.88 | 0.24 | 5 | 16.0% | 0.45 | 0.36 | 31.9% | 29.9% | 29.5% | 29.8%/24.4% | 8.5 (interpolated) | pass | 0.089 (unverified) | 0.04 |
| 163 | `cfg_ca39` | timeframe=1min, level=onh, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=range, exit=16:00 | 0/9/115/43 | 167 | 15.5% | 2.9% | 1.11 | -1.8% | 225 | 1.84 | 2.1% | 81.4 | 8/8 | 1.00 | 1.03 | 0.08 | 5 | 9.1% | 0.39 | 0.56 | 15.1% | 13.9% | 8.8% | 14.1%/10.4% | 13.7 (interpolated) | pass | 0.055 (unverified) | 0.17 |
| 164 | `cfg_7b19` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=1, mode=cont, stop=d0.10, target=none, exit=12:30 | 145/0/482/0 | 627 | 31.4% | 5.5% | 1.11 | -4.2% | 217 | 1.37 | 6.6% | 306.6 | 9/9 | 1.00 | 0.88 | 0.23 | 5 | 16.9% | 0.46 | 0.42 | 28.5% | 24.9% | 24.4% | 28.5%/21.8% | 7.0 (interpolated) | pass | 0.074 (unverified) | 0.60 |
| 165 | `cfg_adad` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=struct, target=none, exit=12:30 | 187/0/485/0 | 672 | 35.5% | 6.1% | 1.10 | -5.4% | 242 | 1.33 | 8.5% | 331.2 | 8/8 | 0.88 | 1.07 | 0.03 | 4 | 18.2% | 0.42 | 0.37 | 33.0% | 30.3% | 42.4% | 32.4%/26.5% | 7.7 (interpolated) | pass | 0.077 (unverified) | 0.06 |
| 166 | `cfg_14a1` | timeframe=1min, level=box, side=high, window=15, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=16:00 | 0/89/208/0 | 297 | 33.6% | 5.8% | 1.17 | -4.3% | 292 | 1.69 | 8.7% | 143.9 | 6/6 | 1.00 | 0.95 | 0.22 | 4 | 13.6% | 0.60 | 0.51 | 31.9% | 31.0% | 28.3% | 29.1%/22.0% | 14.6 (interpolated) | pass | 0.080 (unverified) | 0.92 |
| 167 | `cfg_f099` | timeframe=1min, level=onh, side=both, window=15, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/154/331/0 | 485 | 38.8% | 6.6% | 1.00 | -6.0% | 363 | 1.35 | 15.4% | 235.9 | 6/6 | 1.00 | 1.00 | 0.01 | 5 | 17.4% | 0.55 | 0.44 | 35.7% | 33.1% | 37.9% | 34.3%/28.2% | 10.9 (interpolated) | pass | 0.047 (unverified) | 0.01 |
| 168 | `cfg_77ea` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/38/106/0 | 144 | 20.8% | 3.8% | 1.15 | -2.7% | 554 | 2.24 | 3.7% | 69.3 | 8/8 | 1.00 | 1.11 | 0.04 | 4 | 9.7% | 0.54 | 0.60 | 20.0% | 19.3% | 9.8% | 18.7%/13.0% | 19.2 (interpolated) | pass | 0.053 (unverified) | 0.40 |
| 169 | `cfg_9880` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=11:00 | 91/0/182/0 | 273 | 18.1% | 3.3% | 1.19 | -2.4% | 183 | 1.58 | 2.0% | 132.7 | 8/8 | 1.00 | 1.01 | 0.17 | 4 | 11.3% | 0.33 | 0.41 | 16.6% | 15.6% | 11.1% | 15.7%/12.5% | 9.6 (interpolated) | pass | 0.101 (unverified) | 0.66 |
| 170 | `cfg_45b2` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=12:30 | 127/0/247/0 | 374 | 25.8% | 4.6% | 1.14 | -3.2% | 183 | 1.47 | 5.6% | 182.9 | 8/8 | 0.88 | 0.95 | 0.19 | 4 | 14.2% | 0.39 | 0.41 | 23.3% | 21.6% | 22.8% | 22.4%/17.0% | 9.9 (interpolated) | pass | 0.089 (unverified) | 0.55 |
| 171 | `cfg_0f38` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/201/426/0 | 627 | 47.3% | 7.9% | 1.05 | -6.3% | 185 | 1.31 | 20.0% | 308.2 | 7/7 | 1.00 | 0.95 | 0.09 | 5 | 24.9% | 0.47 | 0.40 | 45.6% | 43.1% | 44.8% | 42.6%/30.7% | 9.8 (interpolated) | pass | 0.061 (unverified) | 0.26 |
| 172 | `cfg_ec66` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=3R, exit=11:00 | 163/0/169/37 | 369 | 24.0% | 4.3% | 1.16 | -3.4% | 202 | 1.42 | 3.6% | 180.4 | 8/8 | 1.00 | 0.93 | 0.23 | 4 | 13.9% | 0.42 | 0.35 | 22.0% | 20.3% | 16.2% | 21.9%/17.4% | 9.4 (interpolated) | pass | 0.108 (unverified) | 0.96 |
| 173 | `cfg_1444` | timeframe=1min, level=box, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=12:30 | 102/0/309/0 | 411 | 25.1% | 4.5% | 1.05 | -3.7% | 159 | 1.43 | 4.7% | 203.0 | 7/7 | 0.86 | 1.05 | 0.00 | 4 | 11.6% | 0.48 | 0.49 | 22.1% | 20.5% | 28.4% | 22.6%/18.4% | 8.6 (interpolated) | pass | 0.055 (unverified) | 0.72 |
| 174 | `cfg_9b7a` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 59/0/63/0 | 122 | 19.6% | 3.6% | 1.25 | -3.3% | 376 | 2.05 | 2.6% | 58.9 | 7/7 | 1.00 | 1.13 | 0.12 | 4 | 10.9% | 0.44 | 0.48 | 19.1% | 18.7% | 17.8% | 17.2%/13.7% | 22.0 (interpolated) | pass | 0.127 (unverified) | 0.66 |
| 175 | `cfg_a938` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=range, exit=16:00 | 0/19/213/63 | 295 | 19.5% | 3.5% | 1.11 | -2.3% | 133 | 1.55 | 4.1% | 144.6 | 8/8 | 1.00 | 1.10 | 0.01 | 5 | 12.6% | 0.33 | 0.51 | 18.6% | 17.5% | 12.8% | 17.7%/14.3% | 10.0 (interpolated) | pass | 0.063 (unverified) | 0.64 |
| 176 | `cfg_ca9a` | timeframe=1min, level=box, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=struct, target=3R, exit=12:30 | 87/0/428/163 | 678 | 34.8% | 6.0% | 1.22 | -3.8% | 166 | 1.34 | 6.3% | 332.3 | 9/9 | 0.89 | 0.77 | 0.44 | 4 | 18.0% | 0.48 | 0.31 | 31.2% | 27.8% | 30.4% | 30.9%/25.4% | 8.1 (interpolated) | pass | 0.135 (unverified) | 0.16 |
| 177 | `cfg_6556` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=11:00 | 86/0/58/0 | 144 | 13.8% | 2.6% | 1.11 | -2.8% | 302 | 1.72 | 1.7% | 69.3 | 7/7 | 1.00 | 1.03 | 0.08 | 4 | 9.6% | 0.30 | 0.46 | 13.2% | 12.5% | 12.0% | 12.1%/10.1% | 15.3 (interpolated) | pass | 0.087 (unverified) | 0.76 |
| 178 | `cfg_dd4a` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=struct, target=3R, exit=12:30 | 66/0/239/102 | 407 | 29.7% | 5.2% | 1.14 | -4.5% | 144 | 1.39 | 4.9% | 198.8 | 9/9 | 0.89 | 0.94 | 0.20 | 5 | 20.2% | 0.30 | 0.37 | 28.1% | 26.8% | 21.5% | 27.2%/21.0% | 11.1 (interpolated) | pass | 0.097 (unverified) | 0.20 |
| 179 | `cfg_a37e` | timeframe=1min, level=onh, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=range, exit=12:30 | 19/0/110/38 | 167 | 12.9% | 2.4% | 1.10 | -1.8% | 225 | 1.74 | 1.5% | 81.3 | 9/9 | 1.00 | 1.10 | 0.00 | 4 | 8.3% | 0.34 | 0.53 | 12.3% | 11.6% | 7.7% | 11.5%/9.0% | 12.2 (interpolated) | pass | 0.062 (unverified) | 0.54 |
| 180 | `cfg_c4ff` | timeframe=1min, level=box, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=12:30 | 158/0/206/0 | 364 | 30.4% | 5.3% | 1.15 | -4.0% | 140 | 1.43 | 7.0% | 179.1 | 8/8 | 1.00 | 0.93 | 0.22 | 5 | 18.2% | 0.35 | 0.39 | 28.8% | 27.1% | 27.5% | 27.7%/21.3% | 11.0 (interpolated) | pass | 0.097 (unverified) | 0.71 |
| 181 | `cfg_0305` | timeframe=1min, level=box, side=both, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 340/0/434/0 | 774 | 43.4% | 7.3% | 1.10 | -6.1% | 191 | 1.27 | 14.3% | 378.0 | 7/7 | 0.86 | 1.05 | 0.05 | 4 | 22.3% | 0.49 | 0.34 | 39.5% | 35.1% | 33.2% | 40.5%/30.6% | 7.5 (interpolated) | pass | 0.083 (unverified) | -0.06 |
| 182 | `cfg_2dde` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=3R, exit=11:00 | 205/0/202/40 | 447 | 25.3% | 4.5% | 1.12 | -3.5% | 152 | 1.35 | 4.5% | 218.9 | 9/9 | 1.00 | 0.80 | 0.31 | 5 | 14.5% | 0.38 | 0.33 | 23.7% | 21.4% | 19.3% | 22.4%/17.7% | 8.3 (interpolated) | pass | 0.092 (unverified) | 0.13 |
| 183 | `cfg_6e6a` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=struct, target=none, exit=12:30 | 88/0/148/0 | 236 | 22.6% | 4.1% | 1.06 | -2.3% | 211 | 1.57 | 3.9% | 115.2 | 8/8 | 1.00 | 1.07 | -0.00 | 5 | 14.7% | 0.35 | 0.51 | 21.3% | 20.6% | 22.7% | 20.7%/16.4% | 13.1 (interpolated) | pass | 0.055 (unverified) | 0.84 |
| 184 | `cfg_ec46` | timeframe=1min, level=onh, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=11:00 | 103/0/65/0 | 168 | 15.5% | 2.9% | 1.19 | -2.7% | 302 | 1.73 | 1.8% | 81.4 | 6/6 | 1.00 | 1.11 | 0.07 | 4 | 10.1% | 0.33 | 0.43 | 14.1% | 13.4% | 13.1% | 13.3%/10.4% | 13.6 (interpolated) | pass | 0.114 (unverified) | 0.73 |
| 185 | `cfg_973e` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=struct, target=range, exit=12:30 | 28/0/155/63 | 246 | 19.4% | 3.5% | 1.08 | -2.8% | 229 | 1.53 | 2.4% | 119.5 | 9/9 | 1.00 | 1.00 | 0.08 | 5 | 12.5% | 0.36 | 0.43 | 18.5% | 17.8% | 18.4% | 18.0%/14.1% | 11.7 (interpolated) | pass | 0.065 (unverified) | 0.52 |
| 186 | `cfg_936a` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=3R, exit=16:00 | 0/2/235/109 | 346 | 16.6% | 3.0% | 1.15 | -4.8% | 444 | 1.44 | 2.7% | 168.9 | 9/9 | 1.00 | 0.84 | 0.31 | 4 | 9.3% | 0.41 | 0.38 | 15.2% | 14.1% | 13.7% | 14.7%/12.0% | 7.7 (interpolated) | pass | 0.093 (unverified) | 0.63 |
| 187 | `cfg_4acc` | timeframe=1min, level=box, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=16:00 | 0/88/323/0 | 411 | 33.8% | 5.9% | 1.08 | -4.3% | 159 | 1.54 | 8.7% | 202.5 | 6/6 | 0.83 | 1.10 | -0.01 | 4 | 18.3% | 0.38 | 0.57 | 31.7% | 29.8% | 39.0% | 30.6%/22.6% | 10.8 (interpolated) | pass | 0.051 (unverified) | 0.84 |
| 188 | `cfg_cd97` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=11:00 | 136/0/345/0 | 481 | 24.6% | 4.4% | 1.12 | -3.3% | 201 | 1.41 | 3.2% | 235.2 | 7/7 | 1.00 | 1.01 | 0.11 | 5 | 16.2% | 0.29 | 0.43 | 22.1% | 19.9% | 20.3% | 21.8%/17.7% | 7.1 (interpolated) | pass | 0.077 (unverified) | -0.03 |
| 189 | `cfg_eae0` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=1, mode=cont, stop=struct, target=range, exit=12:30 | 43/0/359/79 | 481 | 22.8% | 4.1% | 1.05 | -3.6% | 202 | 1.38 | 3.6% | 234.5 | 9/9 | 1.00 | 0.96 | 0.10 | 5 | 15.9% | 0.30 | 0.39 | 20.7% | 19.2% | 19.8% | 20.4%/16.2% | 7.0 (interpolated) | pass | 0.060 (unverified) | 0.52 |
| 190 | `cfg_2462` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/53/171/0 | 224 | 22.6% | 4.1% | 1.14 | -2.8% | 183 | 1.80 | 5.4% | 107.5 | 7/7 | 1.00 | 1.04 | 0.10 | 3 | 8.6% | 0.62 | 0.52 | 21.6% | 20.8% | 15.6% | 20.6%/16.8% | 14.6 (interpolated) | pass | 0.070 (unverified) | 0.58 |
| 191 | `cfg_d56d` | timeframe=1min, level=box, side=low, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=12:30 | 37/0/74/35 | 146 | 18.0% | 3.3% | 1.15 | -3.4% | 186 | 1.72 | 2.1% | 70.3 | 8/8 | 0.88 | 0.82 | 0.33 | 5 | 12.1% | 0.33 | 0.45 | 17.5% | 17.1% | 10.8% | 15.9%/12.4% | 18.8 (interpolated) | pass | 0.091 (unverified) | -0.01 |
| 192 | `cfg_0236` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=11:00 | 243/0/204/0 | 447 | 27.5% | 4.9% | 1.15 | -2.9% | 152 | 1.37 | 4.8% | 219.6 | 8/8 | 1.00 | 0.88 | 0.27 | 5 | 14.0% | 0.43 | 0.34 | 24.0% | 22.3% | 20.7% | 23.6%/18.2% | 8.4 (interpolated) | pass | 0.104 (unverified) | 0.17 |
| 193 | `cfg_5dcb` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=fade, stop=struct, target=2R, exit=11:00 | 6/0/91/66 | 163 | 9.2% | 1.7% | 1.16 | -2.5% | 682 | 1.69 | 0.4% | 78.2 | 7/7 | 1.00 | 0.91 | 0.25 | 4 | 2.9% | 0.69 | 0.39 | 8.7% | 8.2% | 6.4% | 8.3%/7.0% | 9.9 (interpolated) | pass | 0.099 (unverified) | -0.71 |
| 194 | `cfg_a83f` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=fade, stop=struct, target=2R, exit=12:30 | 3/0/92/68 | 163 | 9.4% | 1.8% | 1.18 | -2.6% | 682 | 1.70 | 0.5% | 78.1 | 8/8 | 1.00 | 0.90 | 0.28 | 4 | 3.1% | 0.67 | 0.38 | 8.9% | 8.4% | 6.8% | 8.6%/7.3% | 10.3 (interpolated) | pass | 0.108 (unverified) | -0.80 |
| 195 | `cfg_2f78` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=3R, exit=16:00 | 0/0/121/73 | 194 | 13.0% | 2.4% | 1.23 | -1.8% | 169 | 1.64 | 1.1% | 93.5 | 9/9 | 1.00 | 0.93 | 0.30 | 5 | 7.9% | 0.38 | 0.34 | 12.2% | 11.3% | 8.3% | 11.7%/9.7% | 11.6 (interpolated) | pass | 0.128 (unverified) | 0.39 |
| 196 | `cfg_20b1` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=range, exit=16:00 | 0/47/164/84 | 295 | 26.0% | 4.6% | 1.18 | -3.9% | 224 | 1.48 | 7.5% | 144.1 | 7/7 | 1.00 | 1.11 | 0.07 | 4 | 15.7% | 0.38 | 0.39 | 24.6% | 23.2% | 25.0% | 22.6%/18.7% | 12.8 (interpolated) | pass | 0.106 (unverified) | 0.53 |
| 197 | `cfg_8567` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=11:00 | 85/0/188/0 | 273 | 17.0% | 3.1% | 1.15 | -3.3% | 209 | 1.57 | 1.9% | 132.5 | 7/7 | 1.00 | 1.07 | 0.08 | 4 | 8.7% | 0.44 | 0.44 | 16.1% | 14.9% | 14.8% | 15.6%/12.8% | 9.3 (interpolated) | pass | 0.091 (unverified) | 0.75 |
| 198 | `cfg_1e90` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=3R, exit=11:00 | 167/0/113/16 | 296 | 16.1% | 3.0% | 1.05 | -3.6% | 448 | 1.43 | 3.0% | 143.6 | 7/7 | 1.00 | 0.97 | 0.08 | 4 | 8.6% | 0.47 | 0.43 | 14.6% | 13.5% | 13.4% | 15.0%/12.0% | 9.0 (interpolated) | pass | 0.066 (unverified) | 0.97 |
| 199 | `cfg_a340` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=16:00 | 0/49/175/0 | 224 | 22.9% | 4.1% | 1.09 | -3.1% | 191 | 1.83 | 5.0% | 107.7 | 6/6 | 1.00 | 1.01 | 0.09 | 4 | 11.2% | 0.51 | 0.57 | 22.1% | 20.4% | 20.2% | 21.1%/15.9% | 13.5 (interpolated) | pass | 0.050 (unverified) | 0.55 |
| 200 | `cfg_90cc` | timeframe=1min, level=asia, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=3R, exit=11:00 | 7/0/59/36 | 102 | 9.5% | 1.8% | 1.14 | -1.2% | 211 | 2.01 | 0.5% | 49.9 | 9/9 | 1.00 | 0.96 | 0.18 | 5 | 5.8% | 0.39 | 0.55 | 9.2% | 8.8% | 5.7% | 8.6%/7.0% | 15.1 (interpolated) | pass | 0.062 (unverified) | 0.43 |
| 201 | `cfg_5e3a` | timeframe=1min, level=box, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/107/421/0 | 528 | 34.0% | 5.9% | 1.10 | -4.4% | 253 | 1.44 | 11.4% | 258.9 | 8/8 | 0.88 | 1.03 | 0.06 | 4 | 17.7% | 0.39 | 0.48 | 31.0% | 28.7% | 38.9% | 30.4%/24.9% | 8.8 (interpolated) | pass | 0.062 (unverified) | 0.22 |
| 202 | `cfg_0e3d` | timeframe=1min, level=box, side=high, window=15, pen=0.00, confirm=3, mode=cont, stop=struct, target=none, exit=12:30 | 88/0/155/0 | 243 | 21.7% | 3.9% | 1.05 | -3.2% | 161 | 1.51 | 4.0% | 119.6 | 8/8 | 1.00 | 0.96 | 0.09 | 5 | 12.8% | 0.37 | 0.51 | 20.5% | 19.2% | 20.8% | 19.3%/14.7% | 12.3 (interpolated) | pass | 0.055 (unverified) | 0.72 |
| 203 | `cfg_5bf4` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=struct, target=none, exit=16:00 | 0/80/144/0 | 224 | 29.7% | 5.2% | 1.06 | -3.6% | 159 | 1.66 | 7.7% | 108.6 | 7/7 | 1.00 | 1.00 | 0.07 | 4 | 16.9% | 0.43 | 0.59 | 28.8% | 27.6% | 27.5% | 26.8%/21.6% | 17.4 (interpolated) | pass | 0.043 (unverified) | 0.79 |
| 204 | `cfg_0063` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=1, mode=cont, stop=d0.10, target=none, exit=12:30 | 154/0/456/0 | 610 | 25.0% | 4.5% | 0.98 | -4.3% | 213 | 1.30 | 7.1% | 299.4 | 9/9 | 0.89 | 0.81 | 0.18 | 4 | 9.5% | 0.56 | 0.46 | 21.7% | 18.7% | 26.0% | 22.7%/17.0% | 6.2 (interpolated) | pass | 0.042 (unverified) | 0.24 |
| 205 | `cfg_5db4` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=12:30 | 67/0/206/0 | 273 | 18.9% | 3.4% | 1.07 | -4.1% | 232 | 1.58 | 3.2% | 132.9 | 8/8 | 1.00 | 1.03 | 0.04 | 4 | 10.5% | 0.39 | 0.51 | 17.5% | 16.6% | 17.2% | 16.9%/13.4% | 9.9 (interpolated) | pass | 0.058 (unverified) | 0.95 |
| 206 | `cfg_343e` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=1, mode=cont, stop=struct, target=none, exit=12:30 | 189/0/746/0 | 935 | 35.6% | 6.1% | 1.05 | -5.5% | 237 | 1.29 | 8.9% | 461.1 | 7/7 | 0.86 | 0.96 | 0.08 | 3 | 17.6% | 0.43 | 0.39 | 31.3% | 27.7% | 38.7% | 30.8%/24.3% | 5.8 (interpolated) | pass | 0.060 (unverified) | -0.44 |
| 207 | `cfg_2291` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 120/0/374/0 | 494 | 30.4% | 5.3% | 1.13 | -5.0% | 191 | 1.45 | 5.6% | 241.9 | 10/10 | 0.90 | 1.08 | 0.06 | 4 | 19.1% | 0.31 | 0.44 | 27.2% | 24.6% | 19.8% | 27.0%/21.5% | 8.4 (interpolated) | pass | 0.078 (unverified) | 0.05 |
| 208 | `cfg_758f` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/168/767/0 | 935 | 43.0% | 7.2% | 1.01 | -10.1% | 500 | 1.30 | 17.4% | 458.4 | 7/7 | 0.86 | 1.07 | -0.06 | 4 | 17.2% | 0.60 | 0.43 | 38.2% | 31.7% | 42.7% | 38.5%/29.3% | 6.5 (interpolated) | pass | 0.048 (unverified) | 0.08 |
| 209 | `cfg_0d4e` | timeframe=1min, level=lon, side=high, window=60, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=12:30 | 66/0/165/0 | 231 | 18.3% | 3.3% | 1.11 | -3.2% | 118 | 1.62 | 3.0% | 112.1 | 8/8 | 1.00 | 0.92 | 0.19 | 5 | 8.4% | 0.50 | 0.52 | 16.7% | 15.5% | 12.2% | 16.2%/13.5% | 11.5 (interpolated) | pass | 0.062 (unverified) | 0.53 |
| 210 | `cfg_80a1` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=12:30 | 56/0/168/0 | 224 | 18.0% | 3.3% | 1.07 | -3.2% | 209 | 1.68 | 2.7% | 108.1 | 7/7 | 1.00 | 1.07 | 0.00 | 4 | 11.3% | 0.37 | 0.54 | 17.4% | 16.7% | 16.7% | 16.3%/11.8% | 11.2 (interpolated) | pass | 0.055 (unverified) | 0.72 |
| 211 | `cfg_ec29` | timeframe=1min, level=onh, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=16:00 | 0/30/101/37 | 168 | 21.2% | 3.8% | 1.07 | -4.2% | 376 | 1.66 | 5.1% | 82.0 | 7/7 | 1.00 | 0.98 | 0.10 | 4 | 12.3% | 0.38 | 0.51 | 20.5% | 20.0% | 20.8% | 19.4%/15.5% | 18.9 (interpolated) | pass | 0.055 (unverified) | 0.68 |
| 212 | `cfg_fbac` | timeframe=1min, level=box, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/129/235/0 | 364 | 40.2% | 6.8% | 1.12 | -4.1% | 273 | 1.49 | 13.0% | 178.2 | 7/7 | 1.00 | 0.85 | 0.28 | 4 | 18.9% | 0.53 | 0.50 | 39.5% | 37.4% | 36.3% | 37.4%/29.8% | 13.6 (interpolated) | pass | 0.071 (unverified) | 0.83 |
| 213 | `cfg_1849` | timeframe=1min, level=box, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/163/285/0 | 448 | 40.1% | 6.8% | 1.07 | -5.5% | 187 | 1.39 | 16.1% | 221.2 | 6/6 | 0.83 | 1.04 | 0.03 | 4 | 25.0% | 0.38 | 0.48 | 35.8% | 32.5% | 37.5% | 35.0%/24.6% | 10.9 (interpolated) | pass | 0.062 (unverified) | 0.06 |
| 214 | `cfg_b54f` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=11:00 | 183/0/113/0 | 296 | 17.5% | 3.2% | 1.11 | -3.7% | 394 | 1.47 | 3.1% | 143.8 | 6/6 | 1.00 | 1.01 | 0.10 | 4 | 10.2% | 0.42 | 0.39 | 15.1% | 13.9% | 13.7% | 15.5%/11.9% | 9.2 (interpolated) | pass | 0.088 (unverified) | 1.01 |
| 215 | `cfg_de6c` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=16:00 | 0/57/216/0 | 273 | 23.9% | 4.3% | 1.09 | -3.9% | 210 | 1.69 | 5.9% | 132.9 | 7/7 | 1.00 | 0.94 | 0.15 | 4 | 15.2% | 0.36 | 0.55 | 22.5% | 21.3% | 21.0% | 21.7%/17.2% | 11.9 (interpolated) | pass | 0.052 (unverified) | 0.71 |
| 216 | `cfg_6221` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=struct, target=3R, exit=12:30 | 32/0/117/44 | 193 | 19.3% | 3.5% | 1.05 | -2.6% | 227 | 1.61 | 2.4% | 93.7 | 8/8 | 1.00 | 0.89 | 0.16 | 5 | 13.0% | 0.31 | 0.53 | 18.3% | 17.3% | 17.5% | 16.9%/12.9% | 14.5 (interpolated) | pass | 0.051 (unverified) | 0.39 |
| 217 | `cfg_fd7c` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/97/397/0 | 494 | 35.0% | 6.0% | 1.12 | -5.5% | 213 | 1.48 | 10.0% | 241.1 | 9/9 | 0.89 | 1.17 | -0.05 | 4 | 23.3% | 0.32 | 0.46 | 31.6% | 29.1% | 22.6% | 30.8%/24.1% | 9.5 (interpolated) | pass | 0.068 (unverified) | 0.08 |
| 218 | `cfg_ceb0` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=3R, exit=12:30 | 16/0/229/101 | 346 | 15.7% | 2.9% | 1.14 | -4.3% | 371 | 1.43 | 2.4% | 168.9 | 10/10 | 1.00 | 0.84 | 0.30 | 4 | 9.5% | 0.36 | 0.37 | 14.6% | 13.0% | 11.7% | 13.9%/11.0% | 7.3 (interpolated) | pass | 0.089 (unverified) | 0.46 |
| 219 | `cfg_cb5f` | timeframe=1min, level=onh, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=range, exit=11:00 | 41/0/101/25 | 167 | 10.2% | 1.9% | 1.04 | -1.8% | 264 | 1.64 | 1.0% | 81.2 | 8/8 | 1.00 | 0.99 | 0.05 | 4 | 7.0% | 0.30 | 0.54 | 9.5% | 9.1% | 5.9% | 9.3%/7.7% | 10.0 (interpolated) | pass | 0.048 (unverified) | 0.50 |
| 220 | `cfg_6277` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=range, exit=11:00 | 60/0/181/32 | 273 | 15.4% | 2.8% | 1.11 | -2.4% | 144 | 1.51 | 1.7% | 131.6 | 9/9 | 1.00 | 0.89 | 0.22 | 5 | 10.1% | 0.32 | 0.41 | 14.6% | 12.5% | 9.5% | 14.6%/10.7% | 8.6 (interpolated) | pass | 0.080 (unverified) | 0.63 |
| 221 | `cfg_506c` | timeframe=1min, level=box, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/72/292/0 | 364 | 25.6% | 4.6% | 1.01 | -4.1% | 251 | 1.52 | 7.9% | 177.4 | 8/8 | 0.88 | 1.02 | -0.00 | 4 | 14.4% | 0.44 | 0.56 | 24.6% | 22.0% | 31.1% | 23.0%/17.1% | 9.9 (interpolated) | pass | 0.037 (unverified) | 0.58 |
| 222 | `cfg_80fc` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=16:00 | 0/47/205/88 | 340 | 31.1% | 5.4% | 1.09 | -5.2% | 315 | 1.44 | 8.0% | 166.7 | 7/7 | 0.86 | 0.92 | 0.17 | 4 | 17.9% | 0.42 | 0.40 | 29.8% | 28.8% | 17.6% | 28.1%/21.6% | 13.2 (interpolated) | pass | 0.072 (unverified) | 0.53 |
| 223 | `cfg_6504` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=16:00 | 0/54/246/107 | 407 | 33.0% | 5.7% | 1.07 | -6.2% | 514 | 1.38 | 9.2% | 197.7 | 8/8 | 0.88 | 0.87 | 0.21 | 4 | 19.4% | 0.41 | 0.37 | 31.7% | 29.6% | 16.6% | 30.0%/22.8% | 12.1 (interpolated) | pass | 0.069 (unverified) | 0.48 |
| 224 | `cfg_45e6` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/86/138/0 | 224 | 31.4% | 5.5% | 1.09 | -4.6% | 161 | 1.66 | 8.2% | 109.0 | 7/7 | 1.00 | 1.01 | 0.08 | 4 | 17.1% | 0.46 | 0.56 | 30.7% | 29.7% | 21.8% | 28.3%/22.4% | 18.5 (interpolated) | pass | 0.051 (unverified) | 0.68 |
| 225 | `cfg_3dc2` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/58/215/0 | 273 | 23.7% | 4.2% | 1.02 | -3.0% | 179 | 1.63 | 5.9% | 133.1 | 9/9 | 1.00 | 0.97 | 0.05 | 4 | 13.5% | 0.37 | 0.60 | 22.7% | 20.4% | 18.8% | 20.6%/16.4% | 12.4 (interpolated) | pass | 0.037 (unverified) | 0.36 |
| 226 | `cfg_b6e1` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=11:00 | 208/0/199/0 | 407 | 29.5% | 5.2% | 1.20 | -5.9% | 183 | 1.42 | 4.2% | 197.1 | 7/7 | 0.86 | 1.12 | 0.08 | 4 | 19.2% | 0.35 | 0.34 | 27.7% | 26.1% | 17.3% | 26.0%/20.6% | 10.3 (interpolated) | pass | 0.122 (unverified) | 0.01 |
| 227 | `cfg_21ae` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=2R, exit=12:30 | 54/0/214/139 | 407 | 25.4% | 4.5% | 1.09 | -5.8% | 368 | 1.35 | 4.6% | 197.5 | 9/9 | 1.00 | 0.83 | 0.27 | 5 | 14.8% | 0.42 | 0.30 | 24.4% | 22.4% | 19.0% | 23.0%/18.7% | 9.8 (interpolated) | pass | 0.085 (unverified) | 0.34 |
| 228 | `cfg_1063` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=11:00 | 156/0/197/54 | 407 | 25.5% | 4.5% | 1.12 | -5.8% | 273 | 1.38 | 3.9% | 197.0 | 8/8 | 0.88 | 0.87 | 0.25 | 4 | 16.6% | 0.35 | 0.33 | 24.2% | 21.3% | 14.2% | 22.3%/17.0% | 9.1 (interpolated) | pass | 0.094 (unverified) | 0.03 |
| 229 | `cfg_5371` | timeframe=1min, level=onh, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=none, exit=11:00 | 65/0/103/0 | 168 | 10.6% | 2.0% | 1.02 | -2.5% | 327 | 1.65 | 1.2% | 81.6 | 7/7 | 1.00 | 1.00 | 0.02 | 4 | 7.2% | 0.32 | 0.60 | 10.2% | 9.6% | 6.0% | 9.9%/7.5% | 10.2 (interpolated) | pass | 0.040 (unverified) | 0.50 |
| 230 | `cfg_fe96` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=struct, target=range, exit=11:00 | 53/0/187/33 | 273 | 15.1% | 2.8% | 1.11 | -3.3% | 256 | 1.51 | 1.6% | 132.4 | 8/8 | 1.00 | 0.94 | 0.17 | 4 | 8.1% | 0.42 | 0.42 | 14.2% | 13.3% | 12.4% | 13.1%/11.0% | 8.5 (interpolated) | pass | 0.084 (unverified) | 0.74 |
| 231 | `cfg_de5a` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=none, exit=11:00 | 148/0/148/0 | 296 | 20.5% | 3.7% | 1.02 | -3.1% | 283 | 1.42 | 3.0% | 144.7 | 8/8 | 1.00 | 1.06 | -0.04 | 5 | 12.9% | 0.37 | 0.46 | 19.5% | 17.7% | 15.2% | 17.6%/13.2% | 10.5 (interpolated) | pass | 0.053 (unverified) | 0.45 |
| 232 | `cfg_782c` | timeframe=1min, level=box, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=struct, target=3R, exit=16:00 | 0/49/449/180 | 678 | 32.6% | 5.7% | 1.09 | -5.1% | 320 | 1.30 | 9.1% | 330.9 | 8/8 | 0.88 | 0.73 | 0.36 | 3 | 15.3% | 0.53 | 0.34 | 28.4% | 25.0% | 32.8% | 27.8%/21.6% | 7.4 (interpolated) | pass | 0.081 (unverified) | 0.34 |
| 233 | `cfg_b384` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=2R, exit=12:30 | 64/0/194/111 | 369 | 23.1% | 4.2% | 1.07 | -3.3% | 362 | 1.36 | 4.8% | 179.7 | 9/9 | 1.00 | 0.92 | 0.15 | 5 | 11.9% | 0.44 | 0.31 | 22.0% | 20.7% | 19.2% | 20.9%/16.9% | 9.8 (interpolated) | pass | 0.076 (unverified) | 0.91 |
| 234 | `cfg_6a0c` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=3R, exit=12:30 | 111/0/207/56 | 374 | 26.9% | 4.8% | 1.09 | -4.0% | 171 | 1.39 | 6.3% | 183.7 | 9/9 | 0.89 | 0.88 | 0.21 | 5 | 17.8% | 0.34 | 0.37 | 24.3% | 23.5% | 24.0% | 23.8%/18.5% | 10.2 (interpolated) | pass | 0.078 (unverified) | 0.50 |
| 235 | `cfg_a5e6` | timeframe=1min, level=onh, side=high, window=15, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/37/121/0 | 158 | 19.4% | 3.5% | 1.07 | -2.7% | 554 | 2.06 | 3.7% | 76.1 | 7/7 | 1.00 | 1.00 | 0.07 | 4 | 7.8% | 0.60 | 0.65 | 18.7% | 17.8% | 8.3% | 17.3%/13.3% | 16.0 (interpolated) | pass | 0.035 (unverified) | 0.50 |
| 236 | `cfg_675a` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/303/632/0 | 935 | 64.3% | 10.2% | 1.07 | -8.8% | 391 | 1.25 | 30.2% | 463.9 | 6/6 | 0.83 | 0.86 | 0.21 | 4 | 29.7% | 0.54 | 0.37 | 56.9% | 51.5% | 52.4% | 54.2%/45.0% | 8.1 (interpolated) | pass | 0.071 (unverified) | -0.03 |
| 237 | `cfg_4e3b` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=3R, exit=16:00 | 0/64/277/106 | 447 | 36.5% | 6.3% | 1.11 | -4.9% | 192 | 1.37 | 11.5% | 219.4 | 9/9 | 1.00 | 0.79 | 0.31 | 4 | 22.8% | 0.37 | 0.37 | 32.4% | 30.3% | 31.6% | 30.8%/23.2% | 11.0 (interpolated) | pass | 0.080 (unverified) | 0.47 |
| 238 | `cfg_2ce0` | timeframe=1min, level=asia, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=2R, exit=11:00 | 1/0/52/49 | 102 | 7.4% | 1.4% | 1.17 | -0.9% | 188 | 1.91 | 0.3% | 50.0 | 9/9 | 1.00 | 0.84 | 0.33 | 5 | 5.2% | 0.30 | 0.47 | 6.9% | 6.6% | 5.4% | 6.6%/5.4% | 12.5 (interpolated) | pass | 0.097 (unverified) | 0.20 |
| 239 | `cfg_7ecf` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=struct, target=none, exit=12:30 | 92/0/132/0 | 224 | 19.9% | 3.6% | 1.00 | -3.2% | 152 | 1.49 | 4.1% | 109.2 | 8/8 | 1.00 | 0.96 | 0.04 | 5 | 12.9% | 0.31 | 0.50 | 19.3% | 18.6% | 18.1% | 17.4%/14.1% | 13.0 (interpolated) | pass | 0.047 (unverified) | 0.67 |
| 240 | `cfg_236d` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=3R, exit=12:30 | 149/0/236/52 | 437 | 25.6% | 4.6% | 1.07 | -4.2% | 159 | 1.32 | 7.3% | 214.1 | 8/8 | 1.00 | 0.83 | 0.24 | 4 | 16.3% | 0.36 | 0.37 | 23.9% | 20.5% | 18.3% | 21.8%/17.8% | 8.4 (interpolated) | pass | 0.073 (unverified) | 0.65 |
| 241 | `cfg_42a1` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=struct, target=3R, exit=12:30 | 55/0/266/106 | 427 | 22.8% | 4.1% | 1.01 | -4.0% | 152 | 1.32 | 4.3% | 208.4 | 9/9 | 0.78 | 0.74 | 0.27 | 5 | 16.0% | 0.26 | 0.40 | 21.1% | 19.1% | 22.6% | 20.4%/16.2% | 8.6 (interpolated) | pass | 0.054 (unverified) | 0.23 |
| 242 | `cfg_7f16` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=3R, exit=12:30 | 8/0/143/73 | 224 | 12.2% | 2.3% | 1.06 | -3.3% | 434 | 1.53 | 1.3% | 108.6 | 10/10 | 1.00 | 0.92 | 0.13 | 5 | 6.5% | 0.47 | 0.44 | 11.6% | 10.9% | 7.7% | 10.9%/8.7% | 9.5 (interpolated) | pass | 0.058 (unverified) | -0.16 |
| 243 | `cfg_ec11` | timeframe=1min, level=box, side=low, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 70/0/76/0 | 146 | 20.3% | 3.7% | 1.11 | -3.4% | 186 | 1.81 | 2.8% | 70.1 | 7/7 | 0.86 | 0.87 | 0.24 | 5 | 12.0% | 0.41 | 0.57 | 19.9% | 19.4% | 13.7% | 18.1%/15.0% | 19.4 (interpolated) | pass | 0.060 (unverified) | -0.02 |
| 244 | `cfg_ccec` | timeframe=1min, level=asia, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=2R, exit=12:30 | 0/0/52/50 | 102 | 7.5% | 1.4% | 1.18 | -0.9% | 188 | 1.92 | 0.3% | 50.0 | 10/10 | 1.00 | 0.85 | 0.33 | 5 | 5.3% | 0.29 | 0.47 | 7.0% | 6.7% | 5.4% | 6.6%/5.3% | 12.7 (interpolated) | pass | 0.102 (unverified) | 0.12 |
| 245 | `cfg_3194` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=1, mode=cont, stop=struct, target=range, exit=11:00 | 77/0/343/61 | 481 | 21.1% | 3.8% | 1.05 | -3.8% | 202 | 1.36 | 2.6% | 233.6 | 8/8 | 1.00 | 0.92 | 0.13 | 5 | 14.2% | 0.33 | 0.39 | 19.0% | 17.1% | 17.2% | 18.9%/14.6% | 6.7 (interpolated) | pass | 0.060 (unverified) | 0.16 |
| 246 | `cfg_28c4` | timeframe=1min, level=box, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=3R, exit=12:30 | 102/0/203/59 | 364 | 27.3% | 4.8% | 1.09 | -4.3% | 226 | 1.40 | 6.0% | 179.0 | 9/9 | 1.00 | 0.83 | 0.26 | 5 | 18.0% | 0.34 | 0.37 | 25.5% | 22.5% | 23.3% | 23.5%/19.4% | 10.2 (interpolated) | pass | 0.077 (unverified) | 0.70 |
| 247 | `cfg_704d` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=11:00 | 57/0/51/14 | 122 | 11.5% | 2.1% | 1.02 | -2.8% | 378 | 1.72 | 1.3% | 58.6 | 7/7 | 1.00 | 0.92 | 0.11 | 4 | 5.7% | 0.51 | 0.54 | 11.1% | 10.7% | 10.0% | 10.5%/8.9% | 15.8 (interpolated) | pass | 0.054 (unverified) | 0.42 |
| 248 | `cfg_248a` | timeframe=1min, level=box, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=3R, exit=12:30 | 169/0/285/74 | 528 | 31.8% | 5.5% | 1.10 | -5.0% | 233 | 1.30 | 8.9% | 262.0 | 9/9 | 0.89 | 0.86 | 0.24 | 5 | 17.1% | 0.40 | 0.34 | 28.8% | 27.2% | 26.9% | 27.6%/22.0% | 8.1 (interpolated) | pass | 0.085 (unverified) | 0.05 |
| 249 | `cfg_f48e` | timeframe=1min, level=lon, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=3R, exit=11:00 | 13/0/97/54 | 164 | 9.4% | 1.8% | 1.06 | -1.4% | 165 | 1.58 | 0.7% | 79.9 | 8/8 | 1.00 | 0.93 | 0.13 | 4 | 6.7% | 0.27 | 0.42 | 9.0% | 8.5% | 6.3% | 8.5%/6.8% | 10.3 (interpolated) | pass | 0.062 (unverified) | 0.19 |
| 250 | `cfg_db98` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=3R, exit=12:30 | 8/0/223/109 | 340 | 14.1% | 2.6% | 1.02 | -3.4% | 482 | 1.38 | 1.6% | 164.8 | 9/9 | 1.00 | 0.86 | 0.17 | 5 | 7.3% | 0.48 | 0.39 | 12.7% | 11.6% | 5.1% | 12.7%/10.0% | 7.5 (interpolated) | pass | 0.054 (unverified) | -0.20 |
| 251 | `cfg_1f35` | timeframe=1min, level=box, side=high, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 86/0/109/0 | 195 | 17.4% | 3.2% | 0.93 | -3.9% | 293 | 1.49 | 3.8% | 95.2 | 7/7 | 1.00 | 0.94 | -0.00 | 5 | 12.4% | 0.26 | 0.57 | 16.3% | 15.7% | 13.2% | 15.3%/11.4% | 12.8 (interpolated) | pass | 0.031 (unverified) | 0.71 |
| 252 | `cfg_56ed` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=range, exit=12:30 | 48/0/358/75 | 481 | 19.1% | 3.5% | 0.93 | -4.2% | 230 | 1.33 | 3.7% | 231.7 | 10/10 | 1.00 | 0.98 | -0.05 | 5 | 10.3% | 0.46 | 0.43 | 17.7% | 16.3% | 16.3% | 17.5%/11.9% | 6.6 (interpolated) | pass | 0.036 (unverified) | 0.56 |
| 253 | `cfg_9db7` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=range, exit=16:00 | 0/22/370/89 | 481 | 22.5% | 4.1% | 1.02 | -3.7% | 224 | 1.36 | 5.2% | 233.8 | 9/9 | 1.00 | 0.93 | 0.08 | 5 | 12.8% | 0.43 | 0.39 | 20.8% | 18.6% | 18.0% | 20.0%/17.0% | 7.6 (interpolated) | pass | 0.051 (unverified) | 0.41 |
| 254 | `cfg_726a` | timeframe=1min, level=onh, side=both, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=12:30 | 124/0/367/0 | 491 | 26.1% | 4.6% | 1.09 | -4.5% | 350 | 1.42 | 5.5% | 240.1 | 8/8 | 1.00 | 1.03 | 0.05 | 4 | 11.8% | 0.55 | 0.46 | 23.5% | 21.7% | 12.2% | 23.1%/19.0% | 7.6 (interpolated) | pass | 0.064 (unverified) | 0.65 |
| 255 | `cfg_422b` | timeframe=1min, level=box, side=both, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=2R, exit=12:30 | 62/0/234/147 | 443 | 26.4% | 4.7% | 1.09 | -5.4% | 368 | 1.33 | 5.0% | 215.1 | 8/8 | 1.00 | 0.77 | 0.32 | 4 | 15.3% | 0.42 | 0.29 | 25.2% | 23.9% | 19.0% | 23.9%/18.0% | 9.5 (interpolated) | pass | 0.084 (unverified) | 0.14 |
| 256 | `cfg_1645` | timeframe=1min, level=onh, side=both, window=15, pen=0.05, confirm=1, mode=cont, stop=struct, target=none, exit=12:30 | 93/0/392/0 | 485 | 23.4% | 4.2% | 0.97 | -4.7% | 199 | 1.42 | 4.3% | 235.4 | 7/7 | 1.00 | 1.05 | -0.08 | 5 | 13.7% | 0.41 | 0.54 | 21.5% | 19.1% | 30.1% | 19.3%/13.4% | 7.0 (interpolated) | pass | 0.034 (unverified) | 0.19 |
| 257 | `cfg_5932` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=5, mode=cont, stop=struct, target=3R, exit=16:00 | 0/47/344/141 | 532 | 29.7% | 5.2% | 1.10 | -5.5% | 320 | 1.34 | 7.8% | 259.3 | 7/7 | 0.86 | 0.67 | 0.44 | 4 | 15.3% | 0.49 | 0.36 | 26.8% | 24.1% | 30.4% | 25.8%/20.3% | 8.7 (interpolated) | pass | 0.084 (unverified) | 0.27 |
| 258 | `cfg_869f` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=struct, target=range, exit=16:00 | 0/10/118/64 | 192 | 14.9% | 2.7% | 0.89 | -2.3% | 345 | 1.49 | 2.7% | 92.4 | 7/7 | 1.00 | 1.08 | -0.19 | 4 | 8.9% | 0.40 | 0.59 | 14.3% | 13.8% | 17.0% | 14.0%/10.6% | 12.7 (interpolated) | pass | 0.026 (unverified) | 0.50 |
| 259 | `cfg_fe2b` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=struct, target=range, exit=12:30 | 21/0/113/58 | 192 | 14.5% | 2.7% | 0.94 | -2.4% | 357 | 1.50 | 1.9% | 92.4 | 8/8 | 1.00 | 1.02 | -0.08 | 5 | 8.3% | 0.43 | 0.51 | 13.7% | 12.4% | 15.8% | 12.9%/10.1% | 12.5 (interpolated) | pass | 0.036 (unverified) | 0.65 |
| 260 | `cfg_937b` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=3R, exit=12:30 | 162/0/391/119 | 672 | 37.6% | 6.4% | 1.05 | -6.2% | 235 | 1.26 | 10.0% | 332.4 | 9/9 | 0.89 | 0.69 | 0.37 | 4 | 18.7% | 0.50 | 0.31 | 32.4% | 28.2% | 40.2% | 32.4%/26.1% | 8.2 (interpolated) | pass | 0.071 (unverified) | 0.44 |
| 261 | `cfg_d3e2` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=2R, exit=12:30 | 69/0/236/142 | 447 | 24.9% | 4.4% | 1.06 | -4.4% | 253 | 1.31 | 5.8% | 219.0 | 10/10 | 1.00 | 0.82 | 0.24 | 5 | 15.7% | 0.37 | 0.32 | 23.4% | 20.5% | 23.5% | 22.2%/17.3% | 8.6 (interpolated) | pass | 0.072 (unverified) | 0.41 |
| 262 | `cfg_9b97` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/34/114/0 | 148 | 19.0% | 3.5% | 1.04 | -2.9% | 394 | 2.07 | 3.5% | 70.8 | 8/8 | 1.00 | 0.92 | 0.12 | 4 | 9.2% | 0.51 | 0.69 | 18.5% | 17.8% | 11.3% | 17.6%/12.6% | 17.2 (interpolated) | pass | 0.027 (unverified) | 0.28 |
| 263 | `cfg_4031` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=struct, target=none, exit=11:00 | 171/0/256/0 | 427 | 23.1% | 4.1% | 0.97 | -3.8% | 205 | 1.34 | 3.8% | 207.3 | 7/7 | 0.86 | 0.85 | 0.12 | 5 | 13.6% | 0.36 | 0.46 | 21.2% | 18.5% | 20.4% | 20.7%/15.3% | 7.8 (interpolated) | pass | 0.043 (unverified) | 0.21 |
| 264 | `cfg_d658` | timeframe=1min, level=onh, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 94/0/238/0 | 332 | 18.1% | 3.3% | 1.04 | -3.2% | 222 | 1.48 | 2.3% | 159.8 | 8/8 | 1.00 | 0.90 | 0.14 | 4 | 10.8% | 0.40 | 0.50 | 16.1% | 15.0% | 6.8% | 16.1%/12.9% | 8.1 (interpolated) | pass | 0.047 (unverified) | 0.55 |
| 265 | `cfg_eec0` | timeframe=1min, level=lon, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=11:00 | 63/0/101/0 | 164 | 13.4% | 2.5% | 1.14 | -1.4% | 131 | 1.80 | 1.3% | 79.0 | 7/7 | 1.00 | 0.88 | 0.26 | 4 | 7.0% | 0.45 | 0.53 | 12.8% | 11.9% | 9.5% | 11.8%/9.6% | 12.5 (interpolated) | pass | 0.069 (unverified) | 0.37 |
| 266 | `cfg_be38` | timeframe=1min, level=box, side=high, window=15, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=12:30 | 78/0/219/0 | 297 | 18.2% | 3.3% | 1.04 | -2.6% | 200 | 1.51 | 3.7% | 144.7 | 8/8 | 1.00 | 0.91 | 0.13 | 5 | 11.4% | 0.38 | 0.52 | 16.3% | 14.6% | 10.2% | 16.1%/12.7% | 8.5 (interpolated) | pass | 0.047 (unverified) | 0.29 |
| 267 | `cfg_983e` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=16:00 | 0/77/219/0 | 296 | 22.0% | 4.0% | 0.98 | -5.9% | 554 | 1.56 | 7.4% | 144.0 | 6/6 | 1.00 | 0.82 | 0.16 | 4 | 9.0% | 0.59 | 0.57 | 21.3% | 19.6% | 22.4% | 20.2%/17.1% | 10.3 (interpolated) | pass | 0.038 (unverified) | 0.67 |
| 268 | `cfg_1d26` | timeframe=1min, level=onh, side=both, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=2R, exit=12:30 | 98/0/255/138 | 491 | 27.3% | 4.8% | 1.12 | -3.8% | 196 | 1.32 | 6.5% | 240.4 | 8/8 | 1.00 | 0.86 | 0.26 | 4 | 15.6% | 0.40 | 0.27 | 24.3% | 21.1% | 21.7% | 23.7%/17.7% | 8.1 (interpolated) | pass | 0.095 (unverified) | 0.57 |
| 269 | `cfg_6aca` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=11:00 | 73/0/121/0 | 194 | 14.3% | 2.7% | 1.14 | -1.9% | 124 | 1.69 | 1.5% | 94.3 | 8/8 | 1.00 | 0.90 | 0.24 | 5 | 8.1% | 0.41 | 0.50 | 13.9% | 13.0% | 9.2% | 13.3%/11.1% | 11.5 (interpolated) | pass | 0.072 (unverified) | 0.52 |
| 270 | `cfg_1c18` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/40/132/0 | 172 | 19.9% | 3.6% | 1.05 | -3.1% | 394 | 1.95 | 4.1% | 82.5 | 9/9 | 1.00 | 0.99 | 0.07 | 4 | 11.1% | 0.44 | 0.66 | 19.1% | 18.3% | 14.1% | 17.7%/14.1% | 15.7 (interpolated) | pass | 0.031 (unverified) | 0.39 |
| 271 | `cfg_36c6` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=struct, target=3R, exit=16:00 | 0/20/162/64 | 246 | 16.7% | 3.1% | 0.96 | -2.8% | 208 | 1.43 | 3.5% | 119.5 | 8/8 | 1.00 | 0.87 | 0.09 | 5 | 11.0% | 0.33 | 0.47 | 15.8% | 14.4% | 17.9% | 14.5%/11.1% | 10.0 (interpolated) | pass | 0.037 (unverified) | 0.29 |
| 272 | `cfg_6db2` | timeframe=1min, level=box, side=high, window=15, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/61/236/0 | 297 | 22.3% | 4.0% | 1.00 | -2.9% | 203 | 1.57 | 6.6% | 144.5 | 7/7 | 1.00 | 1.03 | -0.03 | 5 | 11.4% | 0.49 | 0.58 | 20.7% | 19.0% | 11.2% | 19.1%/14.8% | 10.6 (interpolated) | pass | 0.032 (unverified) | 0.44 |
| 273 | `cfg_84ef` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=range, exit=12:30 | 55/0/168/73 | 296 | 20.2% | 3.7% | 0.96 | -3.9% | 362 | 1.39 | 3.8% | 143.4 | 10/10 | 1.00 | 0.97 | -0.01 | 4 | 9.3% | 0.54 | 0.40 | 19.6% | 18.6% | 18.8% | 18.5%/14.8% | 11.4 (interpolated) | pass | 0.042 (unverified) | 0.83 |
| 274 | `cfg_0dcb` | timeframe=1min, level=onh, side=high, window=30, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/121/224/0 | 345 | 28.4% | 5.0% | 0.96 | -4.6% | 292 | 1.37 | 12.1% | 167.8 | 7/7 | 1.00 | 0.84 | 0.12 | 4 | 16.4% | 0.38 | 0.54 | 25.2% | 23.6% | 21.2% | 24.5%/17.5% | 11.4 (interpolated) | pass | 0.035 (unverified) | 0.58 |
| 275 | `cfg_ac8a` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=3R, exit=12:30 | 4/0/91/50 | 145 | 9.9% | 1.9% | 1.04 | -1.7% | 367 | 1.68 | 0.9% | 69.9 | 11/11 | 1.00 | 0.90 | 0.14 | 5 | 6.5% | 0.33 | 0.55 | 9.5% | 9.0% | 6.9% | 8.9%/7.6% | 11.5 (interpolated) | pass | 0.045 (unverified) | 0.14 |
| 276 | `cfg_d144` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/221/476/0 | 697 | 45.2% | 7.6% | 0.87 | -9.7% | 322 | 1.24 | 21.8% | 347.0 | 6/6 | 0.83 | 0.96 | -0.09 | 4 | 30.7% | 0.32 | 0.53 | 42.8% | 37.7% | 29.2% | 40.3%/30.1% | 8.6 (interpolated) | pass | 0.023 (unverified) | -0.20 |
| 277 | `cfg_6bb5` | timeframe=1min, level=box, side=high, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 63/0/180/0 | 243 | 16.7% | 3.1% | 0.96 | -2.5% | 172 | 1.53 | 3.0% | 119.6 | 9/9 | 1.00 | 0.94 | 0.02 | 4 | 6.9% | 0.55 | 0.64 | 15.6% | 14.7% | 12.4% | 15.0%/12.1% | 10.2 (interpolated) | pass | 0.028 (unverified) | 0.35 |
| 278 | `cfg_7a38` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=struct, target=3R, exit=16:00 | 0/23/123/47 | 193 | 18.4% | 3.4% | 0.98 | -3.0% | 219 | 1.55 | 3.5% | 93.2 | 7/7 | 1.00 | 0.89 | 0.09 | 5 | 10.1% | 0.43 | 0.54 | 17.8% | 17.0% | 20.7% | 16.1%/11.8% | 14.6 (interpolated) | pass | 0.038 (unverified) | 0.38 |
| 279 | `cfg_1228` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 99/0/125/0 | 224 | 20.2% | 3.7% | 1.01 | -4.1% | 184 | 1.48 | 4.4% | 109.0 | 8/8 | 1.00 | 0.96 | 0.05 | 5 | 14.1% | 0.28 | 0.49 | 19.2% | 18.2% | 15.8% | 17.9%/14.1% | 13.2 (interpolated) | pass | 0.048 (unverified) | 0.63 |
| 280 | `cfg_c2fb` | timeframe=1min, level=onh, side=high, window=15, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=12:30 | 43/0/115/0 | 158 | 13.0% | 2.4% | 0.98 | -2.4% | 271 | 1.76 | 2.0% | 76.6 | 8/8 | 1.00 | 0.94 | 0.04 | 4 | 5.4% | 0.59 | 0.66 | 12.5% | 12.0% | 5.9% | 12.1%/8.7% | 12.1 (interpolated) | pass | 0.028 (unverified) | 0.45 |
| 281 | `cfg_ad4b` | timeframe=1min, level=onh, side=high, window=15, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/59/99/0 | 158 | 20.7% | 3.7% | 1.00 | -4.6% | 554 | 1.72 | 5.8% | 76.2 | 6/6 | 1.00 | 1.02 | -0.02 | 4 | 6.0% | 0.71 | 0.61 | 20.1% | 19.2% | 20.2% | 18.4%/14.2% | 18.7 (interpolated) | pass | 0.037 (unverified) | 0.66 |
| 282 | `cfg_68b4` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=none, exit=12:30 | 116/0/157/0 | 273 | 20.2% | 3.7% | 0.94 | -6.0% | 221 | 1.39 | 5.2% | 132.6 | 8/8 | 1.00 | 0.91 | 0.03 | 4 | 11.1% | 0.43 | 0.48 | 18.8% | 17.7% | 19.0% | 17.9%/13.8% | 11.1 (interpolated) | pass | 0.040 (unverified) | 0.69 |
| 283 | `cfg_87f4` | timeframe=1min, level=asia, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 37/0/65/0 | 102 | 11.1% | 2.1% | 1.11 | -1.4% | 352 | 2.07 | 0.8% | 49.8 | 8/8 | 1.00 | 0.84 | 0.26 | 4 | 6.7% | 0.37 | 0.58 | 10.7% | 10.4% | 7.8% | 10.3%/8.5% | 16.0 (interpolated) | pass | 0.050 (unverified) | 0.60 |
| 284 | `cfg_0b17` | timeframe=1min, level=asia, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=2R, exit=12:30 | 0/0/121/82 | 203 | 9.1% | 1.7% | 0.97 | -1.7% | 237 | 1.49 | 0.5% | 98.1 | 8/8 | 1.00 | 0.65 | 0.33 | 4 | 4.1% | 0.55 | 0.59 | 8.6% | 8.0% | 5.3% | 8.5%/6.6% | 8.3 (interpolated) | pass | 0.034 (unverified) | 0.18 |
| 285 | `cfg_c8fc` | timeframe=1min, level=box, side=both, window=30, pen=0.05, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/187/864/0 | 1051 | 38.8% | 6.6% | 0.91 | -9.4% | 534 | 1.25 | 19.3% | 512.4 | 8/8 | 0.88 | 0.98 | -0.07 | 3 | 13.2% | 0.66 | 0.46 | 33.7% | 30.3% | 47.1% | 34.4%/26.3% | 5.4 (interpolated) | pass | 0.029 (unverified) | 0.24 |
| 286 | `cfg_20bc` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=3R, exit=16:00 | 0/0/168/78 | 246 | 12.0% | 2.2% | 0.99 | -1.8% | 345 | 1.45 | 1.0% | 118.7 | 9/9 | 1.00 | 0.84 | 0.15 | 5 | 8.0% | 0.34 | 0.45 | 10.9% | 9.6% | 4.8% | 10.3%/8.1% | 7.9 (interpolated) | pass | 0.041 (unverified) | -0.03 |
| 287 | `cfg_0b2e` | timeframe=1min, level=onh, side=low, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=16:00 | 0/31/132/0 | 163 | 19.1% | 3.5% | 0.90 | -2.5% | 363 | 1.77 | 3.3% | 80.1 | 6/6 | 1.00 | 0.84 | 0.06 | 5 | 10.3% | 0.42 | 0.75 | 18.6% | 18.2% | 17.6% | 17.7%/13.1% | 16.0 (interpolated) | pass | 0.013 (unverified) | -0.24 |
| 288 | `cfg_0045` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 47/0/125/0 | 172 | 14.1% | 2.6% | 0.99 | -3.0% | 327 | 1.72 | 2.2% | 82.5 | 10/10 | 1.00 | 0.98 | 0.01 | 4 | 9.3% | 0.32 | 0.65 | 12.6% | 12.0% | 8.4% | 12.1%/9.5% | 11.9 (interpolated) | pass | 0.031 (unverified) | 0.69 |
| 289 | `cfg_9cd0` | timeframe=1min, level=onh, side=high, window=15, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 68/0/90/0 | 158 | 15.7% | 2.9% | 0.99 | -3.4% | 376 | 1.63 | 3.1% | 76.0 | 7/7 | 1.00 | 0.98 | 0.01 | 4 | 6.2% | 0.61 | 0.57 | 14.7% | 14.1% | 14.0% | 13.7%/11.2% | 14.4 (interpolated) | pass | 0.045 (unverified) | 0.77 |
| 290 | `cfg_e42a` | timeframe=1min, level=onh, side=low, window=15, pen=0.05, confirm=3, mode=cont, stop=struct, target=none, exit=16:00 | 0/34/99/0 | 133 | 19.2% | 3.5% | 1.00 | -3.5% | 170 | 1.88 | 3.3% | 65.0 | 7/7 | 1.00 | 0.94 | 0.06 | 5 | 10.6% | 0.40 | 0.68 | 18.7% | 18.2% | 18.4% | 18.3%/14.6% | 18.8 (interpolated) | pass | 0.025 (unverified) | 0.22 |
| 291 | `cfg_b223` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=none, exit=11:00 | 142/0/131/0 | 273 | 17.9% | 3.3% | 0.99 | -4.9% | 221 | 1.40 | 2.9% | 131.9 | 7/7 | 1.00 | 0.86 | 0.13 | 4 | 10.3% | 0.41 | 0.41 | 16.2% | 14.5% | 13.0% | 15.7%/12.5% | 10.0 (interpolated) | pass | 0.055 (unverified) | 0.28 |
| 292 | `cfg_3d26` | timeframe=1min, level=box, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/92/150/0 | 242 | 29.6% | 5.2% | 1.02 | -4.9% | 230 | 1.57 | 8.8% | 118.1 | 6/6 | 1.00 | 1.03 | -0.01 | 4 | 16.9% | 0.43 | 0.59 | 29.0% | 27.6% | 19.9% | 27.2%/20.9% | 16.4 (interpolated) | pass | 0.036 (unverified) | 0.49 |
| 293 | `cfg_0bb9` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=struct, target=3R, exit=12:30 | 52/0/231/91 | 374 | 20.0% | 3.6% | 1.01 | -3.5% | 233 | 1.40 | 3.8% | 181.8 | 9/9 | 0.89 | 0.79 | 0.22 | 3 | 10.9% | 0.46 | 0.48 | 18.6% | 17.0% | 19.5% | 18.6%/14.5% | 8.9 (interpolated) | pass | 0.052 (unverified) | 0.49 |
| 294 | `cfg_b765` | timeframe=1min, level=asia, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=2R, exit=16:00 | 0/0/121/82 | 203 | 9.1% | 1.7% | 0.97 | -1.7% | 237 | 1.49 | 0.5% | 98.1 | 7/7 | 1.00 | 0.57 | 0.40 | 4 | 4.1% | 0.55 | 0.59 | 8.6% | 8.0% | 5.5% | 8.6%/7.1% | 8.3 (interpolated) | pass | 0.034 (unverified) | 0.17 |
| 295 | `cfg_c7bc` | timeframe=1min, level=onh, side=low, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=12:30 | 53/0/80/0 | 133 | 16.8% | 3.1% | 0.92 | -4.7% | 274 | 1.64 | 2.2% | 64.3 | 8/8 | 1.00 | 0.77 | 0.15 | 5 | 9.8% | 0.41 | 0.66 | 16.1% | 15.3% | 16.4% | 14.9%/11.9% | 17.5 (interpolated) | pass | 0.023 (unverified) | 0.44 |
| 296 | `cfg_9295` | timeframe=1min, level=onh, side=low, window=30, pen=0.00, confirm=3, mode=cont, stop=struct, target=none, exit=16:00 | 0/33/91/0 | 124 | 20.3% | 3.7% | 0.98 | -2.1% | 166 | 1.89 | 3.4% | 60.5 | 8/8 | 1.00 | 0.79 | 0.19 | 5 | 12.5% | 0.38 | 0.68 | 19.9% | 18.9% | 20.2% | 18.8%/14.0% | 20.2 (interpolated) | pass | 0.023 (unverified) | 0.16 |
| 297 | `cfg_506e` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=none, exit=11:00 | 61/0/132/0 | 193 | 13.2% | 2.5% | 1.03 | -2.0% | 203 | 1.65 | 1.3% | 92.9 | 7/7 | 1.00 | 1.01 | 0.02 | 4 | 6.9% | 0.48 | 0.55 | 12.6% | 11.7% | 8.5% | 12.7%/10.7% | 11.0 (interpolated) | pass | 0.040 (unverified) | 0.22 |
| 298 | `cfg_8e89` | timeframe=1min, level=box, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 108/0/134/0 | 242 | 20.0% | 3.6% | 0.98 | -4.2% | 167 | 1.44 | 4.7% | 118.5 | 7/7 | 1.00 | 1.01 | -0.02 | 5 | 13.2% | 0.32 | 0.50 | 18.5% | 17.6% | 15.6% | 17.8%/14.4% | 11.9 (interpolated) | pass | 0.042 (unverified) | 0.43 |
| 299 | `cfg_d35b` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=none, exit=12:30 | 92/0/132/0 | 224 | 17.3% | 3.2% | 0.87 | -4.7% | 216 | 1.41 | 4.3% | 107.9 | 7/7 | 1.00 | 0.76 | 0.11 | 4 | 8.6% | 0.48 | 0.56 | 16.0% | 15.5% | 16.9% | 15.8%/10.9% | 12.0 (interpolated) | pass | 0.028 (unverified) | 0.40 |
| 300 | `cfg_2e5b` | timeframe=1min, level=lon, side=high, window=60, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/50/181/0 | 231 | 19.6% | 3.6% | 1.01 | -2.8% | 187 | 1.61 | 5.5% | 112.1 | 7/7 | 1.00 | 0.79 | 0.21 | 4 | 9.5% | 0.46 | 0.56 | 18.8% | 17.4% | 13.0% | 18.1%/12.5% | 12.6 (interpolated) | pass | 0.035 (unverified) | 0.63 |
| 301 | `cfg_aaba` | timeframe=1min, level=box, side=both, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 187/0/629/0 | 816 | 30.9% | 5.4% | 0.98 | -5.3% | 153 | 1.28 | 9.0% | 396.4 | 10/10 | 0.90 | 0.91 | 0.07 | 3 | 15.3% | 0.51 | 0.42 | 25.7% | 20.5% | 38.2% | 27.6%/20.0% | 5.4 (interpolated) | pass | 0.042 (unverified) | 0.02 |
| 302 | `cfg_7b61` | timeframe=1min, level=lon, side=both, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/135/264/0 | 399 | 32.4% | 5.6% | 0.93 | -5.6% | 367 | 1.32 | 14.0% | 197.0 | 6/6 | 1.00 | 0.68 | 0.26 | 4 | 20.9% | 0.35 | 0.49 | 30.7% | 27.6% | 30.6% | 28.4%/21.9% | 10.5 (interpolated) | pass | 0.033 (unverified) | -0.10 |
| 303 | `cfg_58d7` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=struct, target=3R, exit=12:30 | 28/0/158/60 | 246 | 15.9% | 2.9% | 0.95 | -2.6% | 219 | 1.42 | 2.5% | 119.3 | 9/9 | 1.00 | 0.89 | 0.05 | 5 | 11.5% | 0.28 | 0.49 | 15.1% | 13.6% | 16.4% | 13.8%/9.8% | 9.8 (interpolated) | pass | 0.036 (unverified) | 0.46 |
| 304 | `cfg_2832` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=3R, exit=11:00 | 22/0/137/65 | 224 | 10.3% | 1.9% | 0.96 | -2.5% | 434 | 1.47 | 1.0% | 108.9 | 9/9 | 1.00 | 0.77 | 0.19 | 5 | 5.4% | 0.48 | 0.52 | 9.7% | 8.9% | 5.5% | 9.4%/7.6% | 8.0 (interpolated) | pass | 0.035 (unverified) | -0.22 |
| 305 | `cfg_8763` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=none, exit=12:30 | 200/0/294/0 | 494 | 30.4% | 5.3% | 0.96 | -5.5% | 139 | 1.30 | 8.9% | 239.5 | 9/9 | 0.89 | 0.91 | 0.05 | 5 | 17.2% | 0.43 | 0.43 | 28.6% | 26.2% | 23.5% | 27.4%/19.2% | 8.8 (interpolated) | pass | 0.043 (unverified) | 0.06 |
| 306 | `cfg_7ac7` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=3R, exit=11:00 | 10/0/164/72 | 246 | 11.6% | 2.2% | 0.98 | -1.8% | 345 | 1.45 | 0.9% | 118.8 | 9/9 | 1.00 | 0.79 | 0.19 | 4 | 7.8% | 0.33 | 0.46 | 10.3% | 9.4% | 3.7% | 10.2%/8.1% | 7.8 (interpolated) | pass | 0.041 (unverified) | 0.12 |
| 307 | `cfg_0051` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=3, mode=cont, stop=struct, target=3R, exit=12:30 | 57/0/315/122 | 494 | 22.4% | 4.0% | 0.94 | -4.0% | 220 | 1.27 | 4.8% | 241.4 | 10/10 | 0.80 | 0.61 | 0.33 | 5 | 15.7% | 0.29 | 0.42 | 19.7% | 17.8% | 21.6% | 19.7%/15.4% | 7.6 (interpolated) | pass | 0.039 (unverified) | 0.03 |
| 308 | `cfg_5857` | timeframe=1min, level=box, side=low, window=15, pen=0.00, confirm=5, mode=cont, stop=struct, target=none, exit=12:30 | 61/0/85/0 | 146 | 16.3% | 3.0% | 0.93 | -3.4% | 186 | 1.66 | 2.5% | 70.1 | 7/7 | 0.86 | 0.77 | 0.17 | 5 | 10.8% | 0.34 | 0.71 | 15.7% | 15.3% | 16.3% | 14.3%/10.6% | 14.8 (interpolated) | pass | 0.022 (unverified) | -0.01 |
| 309 | `cfg_d8d3` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=struct, target=none, exit=11:00 | 98/0/148/0 | 246 | 16.6% | 3.0% | 0.94 | -2.8% | 219 | 1.46 | 2.2% | 119.7 | 7/7 | 1.00 | 1.00 | -0.06 | 5 | 12.0% | 0.27 | 0.56 | 15.8% | 15.1% | 15.7% | 14.5%/11.6% | 9.5 (interpolated) | pass | 0.031 (unverified) | 0.22 |
| 310 | `cfg_9510` | timeframe=1min, level=box, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 91/0/273/0 | 364 | 17.8% | 3.3% | 0.91 | -3.4% | 187 | 1.39 | 4.5% | 177.7 | 9/9 | 0.89 | 0.96 | -0.05 | 3 | 6.1% | 0.61 | 0.60 | 16.0% | 14.5% | 20.2% | 16.1%/12.2% | 7.4 (interpolated) | pass | 0.024 (unverified) | 0.40 |
| 311 | `cfg_57be` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/44/150/0 | 194 | 19.4% | 3.5% | 1.07 | -2.2% | 176 | 1.74 | 4.9% | 94.1 | 8/8 | 1.00 | 0.85 | 0.22 | 4 | 10.9% | 0.39 | 0.54 | 18.4% | 17.7% | 13.0% | 17.5%/14.3% | 15.3 (interpolated) | pass | 0.046 (unverified) | 0.59 |
| 312 | `cfg_d20a` | timeframe=1min, level=onh, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=3R, exit=12:30 | 4/0/108/56 | 168 | 9.3% | 1.8% | 0.95 | -2.6% | 487 | 1.55 | 1.0% | 81.8 | 9/9 | 1.00 | 0.92 | 0.03 | 4 | 4.9% | 0.48 | 0.53 | 8.9% | 8.4% | 4.2% | 8.9%/6.6% | 9.8 (interpolated) | pass | 0.032 (unverified) | 0.25 |
| 313 | `cfg_9301` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=struct, target=none, exit=11:00 | 116/0/157/0 | 273 | 16.2% | 3.0% | 0.93 | -2.8% | 159 | 1.41 | 2.5% | 132.4 | 8/8 | 1.00 | 0.82 | 0.10 | 4 | 8.0% | 0.46 | 0.55 | 15.5% | 14.0% | 14.5% | 14.9%/11.6% | 9.1 (interpolated) | pass | 0.033 (unverified) | 0.25 |
| 314 | `cfg_2739` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=range, exit=11:00 | 30/0/129/33 | 192 | 11.6% | 2.2% | 1.01 | -1.8% | 211 | 1.60 | 1.0% | 92.8 | 8/8 | 1.00 | 0.93 | 0.08 | 4 | 4.6% | 0.61 | 0.52 | 10.8% | 10.2% | 6.8% | 10.2%/8.3% | 10.0 (interpolated) | pass | 0.044 (unverified) | 0.42 |
| 315 | `cfg_8794` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=range, exit=11:00 | 25/0/74/22 | 121 | 9.4% | 1.8% | 1.06 | -1.3% | 182 | 1.83 | 0.7% | 58.4 | 8/8 | 1.00 | 0.94 | 0.13 | 4 | 5.5% | 0.42 | 0.56 | 9.0% | 8.7% | 5.2% | 8.6%/7.1% | 12.4 (interpolated) | pass | 0.055 (unverified) | 0.08 |
| 316 | `cfg_96c2` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=2R, exit=12:30 | 68/0/295/169 | 532 | 24.1% | 4.3% | 0.92 | -7.4% | 373 | 1.25 | 6.1% | 259.1 | 8/8 | 0.75 | 0.75 | 0.18 | 4 | 10.7% | 0.56 | 0.33 | 22.3% | 19.1% | 21.0% | 20.4%/15.4% | 7.3 (interpolated) | pass | 0.040 (unverified) | 0.10 |
| 317 | `cfg_8d63` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=2R, exit=12:30 | 38/0/103/66 | 207 | 15.4% | 2.8% | 1.00 | -2.2% | 234 | 1.47 | 2.6% | 99.7 | 9/9 | 1.00 | 0.76 | 0.25 | 4 | 9.6% | 0.35 | 0.44 | 14.5% | 14.0% | 14.1% | 13.2%/10.3% | 12.1 (interpolated) | pass | 0.051 (unverified) | 0.10 |
| 318 | `cfg_66ee` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=3, mode=cont, stop=struct, target=none, exit=11:00 | 194/0/300/0 | 494 | 21.2% | 3.8% | 0.87 | -3.8% | 205 | 1.27 | 4.2% | 239.8 | 8/8 | 0.88 | 0.85 | 0.02 | 4 | 12.7% | 0.36 | 0.50 | 18.3% | 16.6% | 18.4% | 18.1%/13.7% | 6.7 (interpolated) | pass | 0.027 (unverified) | -0.06 |
| 319 | `cfg_dd42` | timeframe=1min, level=onh, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=3R, exit=11:00 | 21/0/100/47 | 168 | 9.1% | 1.7% | 0.97 | -2.4% | 549 | 1.57 | 0.8% | 81.8 | 8/8 | 1.00 | 0.83 | 0.14 | 4 | 5.5% | 0.40 | 0.55 | 8.5% | 8.0% | 3.9% | 8.4%/7.0% | 9.3 (interpolated) | pass | 0.035 (unverified) | 0.34 |
| 320 | `cfg_a2b7` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=range, exit=11:00 | 95/0/147/54 | 296 | 17.2% | 3.2% | 0.95 | -2.8% | 362 | 1.37 | 2.5% | 143.0 | 9/9 | 1.00 | 0.96 | -0.01 | 4 | 8.2% | 0.52 | 0.41 | 16.5% | 15.0% | 14.0% | 16.4%/13.3% | 10.1 (interpolated) | pass | 0.040 (unverified) | 0.62 |
| 321 | `cfg_abb1` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=none, exit=11:00 | 46/0/76/0 | 122 | 9.8% | 1.8% | 1.03 | -1.9% | 378 | 1.82 | 1.0% | 58.9 | 7/7 | 1.00 | 1.00 | 0.03 | 4 | 5.7% | 0.42 | 0.62 | 9.5% | 9.1% | 5.1% | 9.0%/7.6% | 12.4 (interpolated) | pass | 0.040 (unverified) | 0.10 |
| 322 | `cfg_a64e` | timeframe=1min, level=box, side=high, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=none, exit=12:30 | 103/0/140/0 | 243 | 20.3% | 3.7% | 0.94 | -4.3% | 170 | 1.42 | 4.6% | 119.2 | 8/8 | 1.00 | 0.84 | 0.09 | 5 | 12.5% | 0.35 | 0.54 | 18.8% | 16.8% | 15.3% | 18.2%/13.4% | 11.7 (interpolated) | pass | 0.033 (unverified) | 0.33 |
| 323 | `cfg_22cc` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=struct, target=none, exit=11:00 | 103/0/133/0 | 236 | 15.9% | 2.9% | 0.93 | -2.6% | 211 | 1.45 | 2.1% | 114.5 | 7/7 | 1.00 | 0.92 | 0.01 | 4 | 11.1% | 0.29 | 0.55 | 15.2% | 13.1% | 16.0% | 13.5%/9.2% | 9.5 (interpolated) | pass | 0.030 (unverified) | 0.61 |
| 324 | `cfg_8a73` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 125/0/221/0 | 346 | 14.1% | 2.6% | 1.00 | -4.7% | 317 | 1.41 | 2.4% | 167.6 | 8/8 | 1.00 | 0.91 | 0.09 | 4 | 7.0% | 0.45 | 0.49 | 12.7% | 11.6% | 9.7% | 12.8%/10.0% | 6.6 (interpolated) | pass | 0.042 (unverified) | 0.92 |
| 325 | `cfg_c262` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=11:00 | 263/0/269/0 | 532 | 26.4% | 4.7% | 0.96 | -6.8% | 315 | 1.28 | 5.5% | 258.7 | 6/6 | 0.83 | 0.83 | 0.14 | 5 | 12.8% | 0.52 | 0.38 | 24.2% | 20.5% | 15.6% | 22.4%/16.2% | 7.1 (interpolated) | pass | 0.045 (unverified) | -0.11 |
| 326 | `cfg_f704` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=range, exit=12:30 | 67/0/231/88 | 386 | 18.7% | 3.4% | 0.79 | -4.6% | 363 | 1.26 | 4.9% | 186.1 | 8/8 | 1.00 | 0.78 | 0.01 | 4 | 10.2% | 0.45 | 0.47 | 17.7% | 16.5% | 17.3% | 18.2%/11.9% | 7.7 (interpolated) | pass | 0.019 (unverified) | 0.17 |
| 327 | `cfg_72f4` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 40/0/108/0 | 148 | 13.1% | 2.4% | 0.97 | -2.8% | 327 | 1.79 | 1.9% | 71.1 | 9/9 | 1.00 | 0.95 | 0.01 | 4 | 7.9% | 0.40 | 0.70 | 11.9% | 11.4% | 7.3% | 11.6%/8.9% | 13.0 (interpolated) | pass | 0.025 (unverified) | 0.51 |
| 328 | `cfg_73b8` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 35/0/89/0 | 124 | 11.0% | 2.1% | 0.88 | -2.5% | 430 | 1.73 | 1.6% | 59.8 | 10/10 | 1.00 | 0.77 | 0.12 | 4 | 3.0% | 0.71 | 0.78 | 10.4% | 9.9% | 6.1% | 10.0%/7.7% | 13.8 (interpolated) | pass | 0.012 (unverified) | 0.82 |
| 329 | `cfg_9450` | timeframe=1min, level=box, side=low, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=2R, exit=12:30 | 17/0/73/56 | 146 | 16.0% | 2.9% | 1.13 | -3.4% | 220 | 1.67 | 1.5% | 70.1 | 8/8 | 1.00 | 0.72 | 0.41 | 5 | 9.9% | 0.38 | 0.39 | 15.5% | 14.9% | 10.4% | 14.3%/11.2% | 17.1 (interpolated) | pass | 0.089 (unverified) | -0.03 |
| 330 | `cfg_86ae` | timeframe=1min, level=asia, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=struct, target=2R, exit=11:00 | 11/0/52/39 | 102 | 8.1% | 1.5% | 0.98 | -1.7% | 352 | 1.81 | 0.5% | 49.8 | 8/8 | 1.00 | 0.87 | 0.11 | 5 | 4.5% | 0.43 | 0.62 | 7.8% | 7.4% | 4.8% | 7.4%/5.8% | 13.5 (interpolated) | pass | 0.037 (unverified) | 0.43 |
| 331 | `cfg_7664` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=2R, exit=16:00 | 0/12/76/57 | 145 | 12.7% | 2.4% | 0.89 | -2.9% | 322 | 1.51 | 2.9% | 70.0 | 9/9 | 1.00 | 0.86 | 0.03 | 4 | 7.4% | 0.39 | 0.61 | 11.9% | 11.4% | 14.2% | 10.7%/8.0% | 14.7 (interpolated) | pass | 0.024 (unverified) | 0.25 |
| 332 | `cfg_0acd` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=struct, target=3R, exit=11:00 | 61/0/155/57 | 273 | 14.9% | 2.7% | 0.89 | -2.8% | 133 | 1.38 | 2.1% | 132.5 | 9/9 | 1.00 | 0.69 | 0.21 | 5 | 8.5% | 0.40 | 0.58 | 14.3% | 12.1% | 8.7% | 12.6%/9.9% | 8.7 (interpolated) | pass | 0.028 (unverified) | 0.16 |
| 333 | `cfg_abc9` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 148/0/299/0 | 447 | 16.0% | 2.9% | 0.93 | -2.7% | 330 | 1.32 | 3.2% | 217.1 | 9/9 | 0.89 | 0.82 | 0.11 | 3 | 4.0% | 0.71 | 0.47 | 14.3% | 12.2% | 17.3% | 13.7%/10.9% | 5.8 (interpolated) | pass | 0.032 (unverified) | 0.15 |
| 334 | `cfg_0a51` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=3R, exit=12:30 | 52/0/72/21 | 145 | 12.8% | 2.4% | 0.89 | -2.8% | 367 | 1.55 | 2.5% | 69.6 | 10/10 | 1.00 | 0.80 | 0.09 | 4 | 8.5% | 0.31 | 0.66 | 12.3% | 11.8% | 14.7% | 11.2%/9.2% | 14.0 (interpolated) | pass | 0.023 (unverified) | 0.37 |
| 335 | `cfg_33d8` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=struct, target=3R, exit=12:30 | 38/0/128/58 | 224 | 19.1% | 3.5% | 0.99 | -2.7% | 167 | 1.48 | 2.9% | 109.1 | 9/9 | 1.00 | 0.79 | 0.20 | 5 | 11.8% | 0.37 | 0.54 | 18.5% | 17.3% | 16.5% | 17.5%/13.5% | 13.3 (interpolated) | pass | 0.045 (unverified) | 0.46 |
| 336 | `cfg_9639` | timeframe=1min, level=lon, side=high, window=60, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 42/0/108/0 | 150 | 12.7% | 2.4% | 0.93 | -2.6% | 430 | 1.67 | 1.9% | 72.9 | 9/9 | 1.00 | 0.79 | 0.14 | 4 | 3.5% | 0.70 | 0.72 | 11.6% | 10.9% | 6.8% | 11.4%/8.3% | 12.3 (interpolated) | pass | 0.019 (unverified) | 0.75 |
| 337 | `cfg_69ce` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=1, mode=cont, stop=struct, target=none, exit=12:30 | 119/0/508/0 | 627 | 22.3% | 4.0% | 0.88 | -6.0% | 353 | 1.31 | 5.5% | 304.2 | 8/8 | 1.00 | 0.98 | -0.11 | 5 | 12.5% | 0.44 | 0.57 | 19.5% | 16.9% | 29.1% | 20.5%/14.0% | 5.4 (interpolated) | pass | 0.022 (unverified) | 0.06 |
| 338 | `cfg_aaa1` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=struct, target=2R, exit=11:00 | 17/0/78/50 | 145 | 8.3% | 1.6% | 0.94 | -2.3% | 212 | 1.61 | 0.6% | 69.8 | 9/9 | 1.00 | 0.76 | 0.17 | 5 | 4.6% | 0.43 | 0.61 | 7.9% | 7.4% | 5.4% | 7.4%/5.7% | 10.4 (interpolated) | pass | 0.033 (unverified) | 0.13 |
| 339 | `cfg_faa5` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=3R, exit=12:30 | 2/0/79/46 | 127 | 9.3% | 1.8% | 1.02 | -1.3% | 173 | 1.73 | 0.8% | 61.4 | 10/10 | 1.00 | 0.78 | 0.24 | 5 | 5.9% | 0.36 | 0.59 | 8.9% | 8.5% | 4.6% | 8.6%/6.4% | 12.6 (interpolated) | pass | 0.038 (unverified) | 0.35 |
| 340 | `cfg_1d09` | timeframe=1min, level=box, side=both, window=60, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/364/765/0 | 1129 | 54.8% | 8.9% | 0.89 | -12.2% | 546 | 1.18 | 35.9% | 561.7 | 6/6 | 0.83 | 0.87 | 0.03 | 4 | 26.6% | 0.51 | 0.42 | 49.9% | 44.2% | 41.9% | 49.5%/37.0% | 6.7 (interpolated) | pass | 0.031 (unverified) | 0.03 |
| 341 | `cfg_7be9` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/74/150/0 | 224 | 18.3% | 3.3% | 0.76 | -5.4% | 392 | 1.39 | 7.8% | 108.2 | 6/6 | 1.00 | 0.85 | -0.09 | 4 | 8.0% | 0.56 | 0.72 | 17.5% | 16.8% | 17.9% | 17.1%/11.7% | 11.3 (interpolated) | pass | 0.012 (unverified) | 0.19 |
| 342 | `cfg_390b` | timeframe=1min, level=box, side=high, window=15, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=12:30 | 103/0/194/0 | 297 | 17.3% | 3.2% | 0.90 | -3.4% | 314 | 1.40 | 4.6% | 143.3 | 7/7 | 0.86 | 0.96 | -0.05 | 3 | 9.1% | 0.47 | 0.55 | 16.3% | 15.4% | 13.0% | 16.1%/12.1% | 9.1 (interpolated) | pass | 0.028 (unverified) | 0.58 |
| 343 | `cfg_5728` | timeframe=1min, level=onh, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=16:00 | 0/59/166/0 | 225 | 17.1% | 3.1% | 0.87 | -4.5% | 554 | 1.57 | 5.8% | 109.1 | 7/7 | 1.00 | 0.87 | 0.00 | 4 | 6.5% | 0.62 | 0.72 | 16.4% | 14.8% | 16.3% | 15.8%/11.7% | 10.3 (interpolated) | pass | 0.017 (unverified) | 0.96 |
| 344 | `cfg_913e` | timeframe=1min, level=onh, side=low, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/43/90/0 | 133 | 19.4% | 3.5% | 0.89 | -5.8% | 222 | 1.64 | 4.2% | 64.7 | 7/7 | 1.00 | 0.80 | 0.08 | 4 | 10.7% | 0.41 | 0.74 | 19.0% | 18.6% | 19.3% | 17.8%/14.1% | 19.7 (interpolated) | pass | 0.017 (unverified) | 0.39 |
| 345 | `cfg_a1d6` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=3, mode=fade, stop=struct, target=2R, exit=12:30 | 1/0/66/48 | 115 | 5.7% | 1.1% | 0.92 | -2.2% | 758 | 1.64 | 0.3% | 55.7 | 9/9 | 1.00 | 0.88 | 0.05 | 4 | 0.5% | 0.91 | 0.58 | 5.4% | 5.1% | 2.4% | 5.2%/4.3% | 8.7 (interpolated) | pass | 0.028 (unverified) | -0.62 |
| 346 | `cfg_4ecb` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 53/0/92/0 | 145 | 10.1% | 1.9% | 0.96 | -1.5% | 309 | 1.68 | 1.1% | 69.9 | 9/9 | 1.00 | 0.82 | 0.14 | 4 | 5.5% | 0.43 | 0.64 | 9.6% | 9.1% | 6.9% | 9.1%/7.4% | 10.9 (interpolated) | pass | 0.026 (unverified) | 0.59 |
| 347 | `cfg_8102` | timeframe=1min, level=lon, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=12:30 | 65/0/159/0 | 224 | 12.3% | 2.3% | 0.84 | -3.5% | 167 | 1.43 | 2.8% | 108.6 | 8/8 | 1.00 | 0.66 | 0.18 | 5 | 3.8% | 0.67 | 0.68 | 11.3% | 10.2% | 12.3% | 11.2%/8.6% | 8.7 (interpolated) | pass | 0.015 (unverified) | 0.58 |
| 348 | `cfg_5a80` | timeframe=1min, level=onh, side=both, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 130/0/321/0 | 451 | 20.4% | 3.7% | 1.03 | -3.1% | 268 | 1.38 | 3.0% | 219.5 | 9/9 | 1.00 | 0.90 | 0.13 | 4 | 12.8% | 0.35 | 0.44 | 17.8% | 15.4% | 10.3% | 18.0%/13.8% | 6.8 (interpolated) | pass | 0.052 (unverified) | 0.71 |
| 349 | `cfg_97e6` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 85/0/188/0 | 273 | 11.7% | 2.2% | 0.84 | -2.2% | 183 | 1.38 | 1.9% | 131.4 | 9/9 | 1.00 | 0.91 | -0.07 | 4 | 2.7% | 0.74 | 0.61 | 10.5% | 9.4% | 7.9% | 10.9%/8.5% | 7.2 (interpolated) | pass | 0.019 (unverified) | 0.05 |
| 350 | `cfg_0e49` | timeframe=1min, level=onh, side=low, window=30, pen=0.00, confirm=3, mode=cont, stop=struct, target=range, exit=16:00 | 0/6/83/35 | 124 | 12.3% | 2.3% | 0.87 | -2.2% | 207 | 1.64 | 1.5% | 60.7 | 9/9 | 1.00 | 0.69 | 0.18 | 4 | 5.6% | 0.54 | 0.64 | 12.1% | 10.9% | 12.4% | 10.7%/8.6% | 15.1 (interpolated) | pass | 0.017 (unverified) | 0.37 |
| 351 | `cfg_5274` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=3, mode=fade, stop=struct, target=2R, exit=11:00 | 2/0/66/47 | 115 | 5.6% | 1.1% | 0.91 | -2.2% | 822 | 1.63 | 0.2% | 55.7 | 8/8 | 1.00 | 0.86 | 0.06 | 4 | 0.4% | 0.92 | 0.59 | 5.3% | 4.9% | 2.7% | 5.2%/4.2% | 8.6 (interpolated) | pass | 0.026 (unverified) | -0.53 |
| 352 | `cfg_4cbc` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=11:00 | 320/0/352/0 | 672 | 26.3% | 4.7% | 0.85 | -6.9% | 404 | 1.21 | 6.9% | 327.0 | 7/7 | 0.86 | 0.85 | -0.00 | 4 | 12.3% | 0.53 | 0.40 | 21.4% | 19.3% | 23.2% | 22.1%/16.6% | 6.3 (interpolated) | pass | 0.026 (unverified) | -0.04 |
| 353 | `cfg_a367` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=range, exit=11:00 | 96/0/217/33 | 346 | 12.7% | 2.4% | 0.97 | -3.9% | 314 | 1.38 | 2.1% | 167.7 | 9/9 | 1.00 | 0.86 | 0.10 | 4 | 7.0% | 0.41 | 0.50 | 11.6% | 9.9% | 9.6% | 11.6%/8.7% | 6.1 (interpolated) | pass | 0.038 (unverified) | 0.90 |
| 354 | `cfg_fc5c` | timeframe=1min, level=asia, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=none, exit=11:00 | 59/0/55/0 | 114 | 12.6% | 2.3% | 0.97 | -2.1% | 183 | 1.71 | 1.2% | 55.8 | 6/6 | 1.00 | 0.79 | 0.19 | 4 | 7.2% | 0.40 | 0.60 | 12.1% | 11.3% | 10.9% | 10.9%/8.9% | 15.2 (interpolated) | pass | 0.034 (unverified) | 0.55 |
| 355 | `cfg_2ef2` | timeframe=1min, level=onh, side=low, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/27/106/0 | 133 | 18.2% | 3.3% | 0.97 | -2.5% | 403 | 2.02 | 2.7% | 64.6 | 8/8 | 1.00 | 0.85 | 0.11 | 5 | 8.9% | 0.51 | 0.79 | 17.9% | 17.4% | 11.3% | 16.9%/13.9% | 19.0 (interpolated) | pass | 0.015 (unverified) | 0.34 |
| 356 | `cfg_306b` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=fade, stop=struct, target=1R, exit=12:30 | 0/0/69/94 | 163 | 4.5% | 0.9% | 0.88 | -1.9% | 759 | 1.44 | 0.2% | 78.8 | 7/7 | 1.00 | 0.85 | 0.04 | 3 | 1.4% | 0.70 | 0.41 | 4.1% | 3.7% | 5.9% | 4.0%/3.2% | 5.7 (interpolated) | pass | 0.036 (unverified) | -1.16 |
| 357 | `cfg_c603` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=fade, stop=struct, target=1R, exit=16:00 | 0/0/69/94 | 163 | 4.5% | 0.9% | 0.88 | -1.9% | 759 | 1.44 | 0.2% | 78.8 | 6/6 | 1.00 | 0.79 | 0.09 | 3 | 1.4% | 0.70 | 0.41 | 4.1% | 3.7% | 5.7% | 4.1%/3.3% | 5.7 (interpolated) | pass | 0.036 (unverified) | -1.16 |
| 358 | `cfg_76d9` | timeframe=1min, level=lon, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=12:30 | 50/0/119/0 | 169 | 12.1% | 2.3% | 0.90 | -2.9% | 179 | 1.59 | 2.2% | 81.3 | 9/9 | 1.00 | 0.74 | 0.16 | 4 | 3.9% | 0.66 | 0.69 | 11.0% | 10.4% | 10.9% | 11.1%/7.9% | 11.1 (interpolated) | pass | 0.018 (unverified) | 0.65 |
| 359 | `cfg_4901` | timeframe=1min, level=lon, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=2R, exit=16:00 | 0/0/163/124 | 287 | 8.3% | 1.6% | 0.89 | -2.0% | 192 | 1.31 | 0.7% | 139.0 | 8/8 | 1.00 | 0.60 | 0.29 | 5 | 5.8% | 0.29 | 0.33 | 7.2% | 6.5% | 6.4% | 7.5%/5.7% | 5.8 (interpolated) | pass | 0.035 (unverified) | -0.23 |
| 360 | `cfg_7639` | timeframe=1min, level=box, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=3R, exit=16:00 | 0/85/328/115 | 528 | 30.7% | 5.4% | 0.93 | -6.5% | 179 | 1.26 | 14.0% | 258.8 | 8/8 | 1.00 | 0.72 | 0.22 | 4 | 16.9% | 0.37 | 0.39 | 27.7% | 25.1% | 25.1% | 27.2%/20.3% | 8.6 (interpolated) | pass | 0.037 (unverified) | 0.20 |
| 361 | `cfg_c741` | timeframe=1min, level=box, side=both, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/246/526/0 | 772 | 45.7% | 7.6% | 0.85 | -10.8% | 330 | 1.22 | 24.0% | 384.9 | 7/7 | 0.86 | 0.87 | -0.02 | 4 | 30.5% | 0.33 | 0.55 | 42.3% | 37.4% | 28.6% | 38.0%/29.3% | 8.0 (interpolated) | pass | 0.022 (unverified) | -0.10 |
| 362 | `cfg_b78f` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 57/0/115/0 | 172 | 10.1% | 1.9% | 0.90 | -1.8% | 331 | 1.56 | 1.3% | 82.8 | 9/9 | 1.00 | 0.89 | 0.01 | 4 | 6.3% | 0.35 | 0.67 | 9.5% | 8.9% | 6.3% | 9.1%/7.1% | 9.3 (interpolated) | pass | 0.020 (unverified) | 0.69 |
| 363 | `cfg_abc2` | timeframe=1min, level=box, side=high, window=15, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/102/195/0 | 297 | 24.7% | 4.4% | 0.84 | -5.2% | 282 | 1.40 | 10.4% | 142.9 | 6/6 | 0.83 | 0.98 | -0.14 | 3 | 7.5% | 0.70 | 0.67 | 23.7% | 22.7% | 24.1% | 23.0%/16.9% | 12.0 (interpolated) | pass | 0.014 (unverified) | 0.49 |
| 364 | `cfg_a546` | timeframe=1min, level=onh, side=low, window=30, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=16:00 | 0/36/177/0 | 213 | 19.9% | 3.6% | 0.85 | -2.2% | 363 | 1.61 | 3.9% | 104.3 | 7/7 | 1.00 | 0.66 | 0.19 | 5 | 11.3% | 0.39 | 0.76 | 18.7% | 18.1% | 18.8% | 18.0%/11.7% | 11.8 (interpolated) | pass | 0.011 (unverified) | -0.34 |
| 365 | `cfg_1301` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=3R, exit=11:00 | 114/0/130/29 | 273 | 14.7% | 2.7% | 0.88 | -4.9% | 381 | 1.34 | 2.7% | 131.7 | 8/8 | 1.00 | 0.79 | 0.09 | 4 | 8.6% | 0.40 | 0.44 | 13.7% | 12.3% | 10.8% | 12.7%/10.2% | 9.5 (interpolated) | pass | 0.034 (unverified) | 0.18 |
| 366 | `cfg_156b` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=3R, exit=11:00 | 22/0/217/101 | 340 | 12.4% | 2.3% | 0.94 | -3.2% | 482 | 1.35 | 1.4% | 164.4 | 8/8 | 0.88 | 0.74 | 0.21 | 5 | 6.1% | 0.51 | 0.44 | 11.3% | 10.2% | 3.5% | 11.6%/8.6% | 6.8 (interpolated) | pass | 0.036 (unverified) | -0.24 |
| 367 | `cfg_91ea` | timeframe=1min, level=lon, side=high, window=30, pen=0.05, confirm=1, mode=cont, stop=d0.10, target=none, exit=12:30 | 72/0/203/0 | 275 | 15.6% | 2.9% | 0.94 | -4.0% | 386 | 1.45 | 3.3% | 133.3 | 9/9 | 1.00 | 0.74 | 0.19 | 4 | 5.4% | 0.63 | 0.61 | 14.4% | 13.3% | 10.1% | 13.4%/10.6% | 8.7 (interpolated) | pass | 0.026 (unverified) | 0.67 |
| 368 | `cfg_b788` | timeframe=1min, level=asia, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=3R, exit=16:00 | 0/2/124/67 | 193 | 10.6% | 2.0% | 0.98 | -1.5% | 190 | 1.51 | 1.4% | 93.1 | 9/9 | 1.00 | 0.69 | 0.30 | 5 | 7.4% | 0.29 | 0.54 | 10.1% | 9.5% | 7.9% | 9.9%/7.9% | 9.7 (interpolated) | pass | 0.038 (unverified) | -0.13 |
| 369 | `cfg_dcd9` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=struct, target=3R, exit=11:00 | 30/0/82/33 | 145 | 9.4% | 1.8% | 0.93 | -2.3% | 382 | 1.64 | 0.8% | 69.8 | 9/9 | 1.00 | 0.80 | 0.14 | 4 | 4.6% | 0.49 | 0.64 | 8.9% | 8.4% | 8.9% | 8.6%/7.1% | 10.9 (interpolated) | pass | 0.031 (unverified) | 0.08 |
| 370 | `cfg_ccad` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=fade, stop=struct, target=3R, exit=11:00 | 18/0/104/41 | 163 | 8.7% | 1.6% | 0.91 | -3.8% | 871 | 1.58 | 0.7% | 78.7 | 7/7 | 1.00 | 0.72 | 0.20 | 3 | 1.4% | 0.84 | 0.59 | 8.1% | 7.5% | 5.2% | 7.9%/5.2% | 8.6 (interpolated) | pass | 0.025 (unverified) | -0.53 |
| 371 | `cfg_eb11` | timeframe=1min, level=onh, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=range, exit=16:00 | 0/11/161/52 | 224 | 15.4% | 2.8% | 1.00 | -1.9% | 268 | 1.60 | 2.8% | 108.6 | 9/9 | 1.00 | 0.89 | 0.12 | 5 | 10.0% | 0.33 | 0.62 | 14.0% | 13.0% | 7.6% | 13.6%/11.1% | 10.3 (interpolated) | pass | 0.032 (unverified) | 0.72 |
| 372 | `cfg_bfdd` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=11:00 | 71/0/51/0 | 122 | 11.8% | 2.2% | 1.03 | -2.8% | 373 | 1.73 | 1.4% | 58.5 | 6/6 | 1.00 | 1.01 | 0.02 | 4 | 6.5% | 0.45 | 0.53 | 11.3% | 11.0% | 10.4% | 10.8%/9.1% | 15.6 (interpolated) | pass | 0.057 (unverified) | 0.51 |
| 373 | `cfg_348f` | timeframe=1min, level=asia, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=struct, target=3R, exit=11:00 | 19/0/56/27 | 102 | 9.4% | 1.8% | 0.98 | -1.9% | 382 | 1.85 | 0.6% | 49.7 | 8/8 | 1.00 | 0.78 | 0.20 | 4 | 4.7% | 0.47 | 0.64 | 9.1% | 8.7% | 8.7% | 8.5%/6.4% | 14.7 (interpolated) | pass | 0.036 (unverified) | 0.37 |
| 374 | `cfg_ca69` | timeframe=1min, level=onh, side=low, window=15, pen=0.05, confirm=3, mode=cont, stop=struct, target=none, exit=12:30 | 41/0/92/0 | 133 | 15.1% | 2.8% | 0.94 | -3.1% | 170 | 1.77 | 1.7% | 64.4 | 8/8 | 1.00 | 0.77 | 0.17 | 5 | 8.2% | 0.42 | 0.73 | 14.8% | 14.3% | 14.5% | 14.1%/10.1% | 15.7 (interpolated) | pass | 0.019 (unverified) | -0.07 |
| 375 | `cfg_0a30` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=3R, exit=16:00 | 0/1/79/47 | 127 | 9.5% | 1.8% | 1.03 | -1.3% | 173 | 1.74 | 0.8% | 61.4 | 9/9 | 1.00 | 0.76 | 0.26 | 5 | 5.9% | 0.37 | 0.60 | 9.1% | 8.7% | 4.9% | 8.7%/7.4% | 13.0 (interpolated) | pass | 0.038 (unverified) | 0.38 |
| 376 | `cfg_7536` | timeframe=1min, level=lon, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=2R, exit=11:00 | 3/0/162/122 | 287 | 8.1% | 1.5% | 0.87 | -2.0% | 193 | 1.30 | 0.7% | 138.9 | 8/8 | 1.00 | 0.61 | 0.26 | 5 | 5.6% | 0.29 | 0.34 | 7.0% | 6.3% | 6.4% | 7.2%/5.6% | 5.7 (interpolated) | pass | 0.033 (unverified) | -0.29 |
| 377 | `cfg_8e7c` | timeframe=1min, level=box, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 116/0/248/0 | 364 | 12.6% | 2.3% | 0.82 | -3.7% | 385 | 1.31 | 2.6% | 176.6 | 8/8 | 0.88 | 0.79 | 0.03 | 3 | 1.6% | 0.83 | 0.55 | 11.2% | 9.7% | 14.2% | 11.8%/8.2% | 5.9 (interpolated) | pass | 0.017 (unverified) | 0.33 |
| 378 | `cfg_1dee` | timeframe=1min, level=lon, side=low, window=60, pen=0.05, confirm=5, mode=fade, stop=d0.10, target=range, exit=16:00 | 0/1/106/51 | 158 | 9.4% | 1.8% | 0.90 | -2.3% | 341 | 1.58 | 0.7% | 76.9 | 8/8 | 1.00 | 0.69 | 0.20 | 4 | 3.0% | 0.67 | 0.67 | 8.9% | 8.5% | 3.2% | 8.5%/6.5% | 10.4 (interpolated) | pass | 0.018 (unverified) | -0.41 |
| 379 | `cfg_5915` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=range, exit=11:00 | 38/0/113/21 | 172 | 9.0% | 1.7% | 0.87 | -1.9% | 253 | 1.51 | 1.1% | 82.9 | 10/10 | 1.00 | 0.83 | 0.04 | 4 | 6.1% | 0.31 | 0.64 | 8.5% | 7.7% | 6.8% | 8.2%/6.3% | 8.4 (interpolated) | pass | 0.019 (unverified) | 0.63 |
| 380 | `cfg_3ad9` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=3R, exit=16:00 | 0/0/181/92 | 273 | 10.4% | 1.9% | 0.87 | -2.7% | 280 | 1.34 | 1.6% | 131.8 | 9/9 | 1.00 | 0.72 | 0.15 | 5 | 5.7% | 0.45 | 0.43 | 9.6% | 9.0% | 5.9% | 9.7%/7.7% | 7.1 (interpolated) | pass | 0.027 (unverified) | 0.62 |
| 381 | `cfg_b42f` | timeframe=1min, level=box, side=low, window=15, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/84/152/0 | 236 | 23.9% | 4.3% | 0.87 | -4.0% | 354 | 1.43 | 8.1% | 115.8 | 6/6 | 0.83 | 0.69 | 0.18 | 4 | 15.2% | 0.36 | 0.65 | 22.9% | 22.6% | 13.7% | 21.4%/16.0% | 13.1 (interpolated) | pass | 0.019 (unverified) | -0.18 |
| 382 | `cfg_3d30` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=2R, exit=12:30 | 93/0/229/115 | 437 | 20.1% | 3.6% | 0.95 | -4.5% | 214 | 1.27 | 6.0% | 212.8 | 8/8 | 1.00 | 0.67 | 0.28 | 4 | 12.7% | 0.36 | 0.35 | 18.1% | 16.2% | 16.1% | 17.5%/13.2% | 7.3 (interpolated) | pass | 0.044 (unverified) | 0.38 |
| 383 | `cfg_58c9` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=3R, exit=16:00 | 0/6/306/148 | 460 | 14.6% | 2.7% | 0.93 | -4.9% | 167 | 1.27 | 2.3% | 224.3 | 9/9 | 1.00 | 0.52 | 0.40 | 5 | 10.1% | 0.29 | 0.36 | 13.1% | 10.7% | 8.6% | 12.9%/9.5% | 5.8 (interpolated) | pass | 0.040 (unverified) | -0.07 |
| 384 | `cfg_fa33` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=3R, exit=12:30 | 12/0/249/113 | 374 | 12.3% | 2.3% | 0.89 | -2.8% | 246 | 1.30 | 2.2% | 182.1 | 10/10 | 1.00 | 0.81 | 0.08 | 5 | 8.1% | 0.34 | 0.46 | 10.9% | 9.5% | 8.8% | 10.8%/8.6% | 5.9 (interpolated) | pass | 0.028 (unverified) | -0.06 |
| 385 | `cfg_32de` | timeframe=1min, level=onh, side=both, window=15, pen=0.05, confirm=5, mode=cont, stop=struct, target=3R, exit=16:00 | 0/26/169/61 | 256 | 14.9% | 2.8% | 0.85 | -4.6% | 386 | 1.41 | 3.8% | 123.8 | 7/7 | 1.00 | 0.84 | 0.01 | 4 | 8.2% | 0.45 | 0.60 | 13.7% | 12.8% | 20.5% | 13.2%/10.0% | 9.6 (interpolated) | pass | 0.019 (unverified) | 0.47 |
| 386 | `cfg_40bd` | timeframe=1min, level=onh, side=low, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 34/0/99/0 | 133 | 15.2% | 2.8% | 0.97 | -2.4% | 368 | 1.92 | 1.5% | 64.1 | 9/9 | 1.00 | 0.81 | 0.16 | 4 | 7.1% | 0.53 | 0.73 | 14.7% | 14.3% | 8.1% | 12.9%/9.9% | 15.9 (interpolated) | pass | 0.019 (unverified) | 0.29 |
| 387 | `cfg_c65e` | timeframe=1min, level=box, side=high, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 76/0/167/0 | 243 | 11.8% | 2.2% | 0.87 | -2.2% | 192 | 1.43 | 1.8% | 117.6 | 8/8 | 1.00 | 0.83 | 0.05 | 4 | 2.8% | 0.74 | 0.62 | 10.4% | 9.4% | 8.2% | 10.2%/7.8% | 7.6 (interpolated) | pass | 0.023 (unverified) | 0.21 |
| 388 | `cfg_4688` | timeframe=1min, level=box, side=both, window=60, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=none, exit=12:30 | 218/0/323/0 | 541 | 29.4% | 5.2% | 0.91 | -5.2% | 160 | 1.27 | 9.6% | 262.5 | 8/8 | 0.88 | 0.89 | 0.03 | 5 | 16.1% | 0.45 | 0.45 | 26.7% | 23.3% | 26.9% | 26.3%/20.2% | 8.0 (interpolated) | pass | 0.033 (unverified) | -0.23 |
| 389 | `cfg_b5b4` | timeframe=1min, level=lon, side=high, window=60, pen=0.05, confirm=1, mode=cont, stop=d0.10, target=none, exit=12:30 | 91/0/253/0 | 344 | 16.6% | 3.0% | 0.92 | -4.1% | 395 | 1.37 | 4.0% | 167.6 | 8/8 | 1.00 | 0.67 | 0.24 | 4 | 3.4% | 0.77 | 0.57 | 14.9% | 13.8% | 10.8% | 14.8%/11.5% | 7.4 (interpolated) | pass | 0.027 (unverified) | 0.57 |
| 390 | `cfg_fad8` | timeframe=1min, level=onh, side=high, window=30, pen=0.05, confirm=1, mode=cont, stop=d0.10, target=none, exit=11:00 | 109/0/236/0 | 345 | 14.2% | 2.6% | 0.94 | -3.5% | 353 | 1.38 | 2.4% | 166.2 | 8/8 | 1.00 | 0.88 | 0.06 | 4 | 4.8% | 0.61 | 0.49 | 12.8% | 11.1% | 12.6% | 12.5%/9.1% | 6.4 (interpolated) | pass | 0.034 (unverified) | 0.73 |
| 391 | `cfg_ca4d` | timeframe=1min, level=asia, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=2R, exit=11:00 | 3/0/66/45 | 114 | 5.9% | 1.1% | 0.86 | -1.0% | 139 | 1.57 | 0.3% | 56.4 | 7/7 | 1.00 | 0.49 | 0.36 | 5 | 3.7% | 0.36 | 0.64 | 5.5% | 5.1% | 6.5% | 5.3%/3.9% | 8.9 (interpolated) | pass | 0.018 (unverified) | 0.64 |
| 392 | `cfg_1aa1` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=2R, exit=12:30 | 26/0/59/42 | 127 | 11.7% | 2.2% | 0.94 | -2.5% | 265 | 1.60 | 1.8% | 61.7 | 9/9 | 1.00 | 0.69 | 0.25 | 4 | 7.4% | 0.36 | 0.57 | 11.3% | 10.9% | 10.2% | 10.5%/8.5% | 15.5 (interpolated) | pass | 0.031 (unverified) | 0.34 |
| 393 | `cfg_312d` | timeframe=1min, level=box, side=low, window=15, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=12:30 | 79/0/157/0 | 236 | 18.7% | 3.4% | 0.92 | -4.9% | 213 | 1.50 | 3.4% | 113.8 | 7/7 | 0.86 | 0.63 | 0.29 | 5 | 12.3% | 0.34 | 0.64 | 17.9% | 16.6% | 17.5% | 16.7%/12.2% | 10.9 (interpolated) | pass | 0.024 (unverified) | -0.43 |
| 394 | `cfg_555e` | timeframe=1min, level=asia, side=both, window=15, pen=0.05, confirm=1, mode=cont, stop=struct, target=2R, exit=16:00 | 0/0/175/111 | 286 | 8.5% | 1.6% | 0.89 | -2.2% | 338 | 1.38 | 0.6% | 139.2 | 7/7 | 1.00 | 0.53 | 0.37 | 5 | 6.2% | 0.27 | 0.61 | 7.7% | 6.9% | 6.1% | 7.6%/6.0% | 5.8 (interpolated) | pass | 0.023 (unverified) | 0.01 |
| 395 | `cfg_8895` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=3R, exit=12:30 | 77/0/154/42 | 273 | 16.6% | 3.0% | 0.84 | -5.9% | 381 | 1.33 | 4.4% | 132.3 | 9/9 | 1.00 | 0.79 | 0.05 | 4 | 8.9% | 0.45 | 0.51 | 15.1% | 14.0% | 12.1% | 14.8%/10.5% | 10.2 (interpolated) | pass | 0.026 (unverified) | 0.67 |
| 396 | `cfg_ec28` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=fade, stop=struct, target=3R, exit=16:00 | 0/4/112/47 | 163 | 9.2% | 1.7% | 0.90 | -2.0% | 739 | 1.56 | 1.1% | 78.6 | 7/7 | 1.00 | 0.78 | 0.12 | 4 | 2.3% | 0.75 | 0.56 | 8.8% | 8.3% | 5.2% | 8.3%/6.5% | 9.3 (interpolated) | pass | 0.024 (unverified) | -0.72 |
| 397 | `cfg_adb1` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=1R, exit=12:30 | 8/0/56/80 | 144 | 8.3% | 1.6% | 0.91 | -2.6% | 347 | 1.49 | 1.1% | 69.5 | 8/8 | 1.00 | 0.80 | 0.10 | 3 | 4.6% | 0.42 | 0.47 | 7.9% | 7.4% | 8.8% | 7.4%/6.3% | 11.4 (interpolated) | pass | 0.043 (unverified) | 0.52 |
| 398 | `cfg_7ea7` | timeframe=1min, level=lon, side=high, window=60, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=range, exit=16:00 | 0/2/144/82 | 228 | 9.9% | 1.9% | 0.87 | -2.9% | 107 | 1.40 | 1.3% | 110.3 | 8/8 | 1.00 | 0.74 | 0.14 | 3 | 5.0% | 0.46 | 0.56 | 9.0% | 8.3% | 6.5% | 8.9%/6.7% | 7.9 (interpolated) | pass | 0.024 (unverified) | 0.38 |
| 399 | `cfg_be23` | timeframe=1min, level=onh, side=low, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=range, exit=16:00 | 0/6/124/33 | 163 | 12.3% | 2.3% | 0.83 | -2.8% | 199 | 1.57 | 1.6% | 78.6 | 7/7 | 1.00 | 0.59 | 0.24 | 5 | 8.0% | 0.35 | 0.69 | 11.8% | 11.1% | 10.7% | 11.6%/8.1% | 12.3 (interpolated) | pass | 0.012 (unverified) | -0.19 |
| 400 | `cfg_fa75` | timeframe=1min, level=asia, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/44/123/0 | 167 | 15.4% | 2.8% | 0.92 | -3.1% | 294 | 1.71 | 4.2% | 81.1 | 7/7 | 1.00 | 0.71 | 0.21 | 4 | 7.6% | 0.49 | 0.76 | 14.8% | 14.3% | 9.1% | 14.4%/11.9% | 14.5 (interpolated) | pass | 0.013 (unverified) | 0.04 |
| 401 | `cfg_758b` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=16:00 | 0/32/136/56 | 224 | 19.8% | 3.6% | 0.88 | -4.2% | 390 | 1.44 | 5.6% | 108.9 | 8/8 | 1.00 | 0.78 | 0.10 | 4 | 10.7% | 0.42 | 0.59 | 19.0% | 18.1% | 14.7% | 17.8%/13.5% | 14.3 (interpolated) | pass | 0.021 (unverified) | 0.78 |
| 402 | `cfg_ceea` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=11:00 | 49/0/78/0 | 127 | 9.0% | 1.7% | 0.92 | -1.8% | 360 | 1.69 | 1.0% | 61.5 | 8/8 | 1.00 | 0.85 | 0.07 | 4 | 4.9% | 0.43 | 0.68 | 8.5% | 8.1% | 6.0% | 8.3%/6.8% | 11.0 (interpolated) | pass | 0.020 (unverified) | 0.73 |
| 403 | `cfg_b654` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=11:00 | 115/0/181/0 | 296 | 11.3% | 2.1% | 0.87 | -5.6% | 556 | 1.39 | 2.2% | 145.4 | 6/6 | 1.00 | 0.79 | 0.08 | 4 | 3.9% | 0.65 | 0.57 | 10.4% | 9.2% | 10.4% | 10.2%/7.9% | 6.2 (interpolated) | pass | 0.031 (unverified) | 0.80 |
| 404 | `cfg_d120` | timeframe=1min, level=asia, side=both, window=15, pen=0.05, confirm=1, mode=cont, stop=struct, target=2R, exit=12:30 | 1/0/175/110 | 286 | 8.3% | 1.6% | 0.87 | -2.2% | 338 | 1.37 | 0.5% | 139.2 | 8/8 | 1.00 | 0.59 | 0.28 | 5 | 5.9% | 0.28 | 0.62 | 7.4% | 6.6% | 5.5% | 7.5%/6.0% | 5.7 (interpolated) | pass | 0.020 (unverified) | 0.06 |
| 405 | `cfg_4977` | timeframe=1min, level=box, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=2R, exit=12:30 | 97/0/275/156 | 528 | 22.4% | 4.0% | 0.91 | -6.5% | 338 | 1.23 | 7.0% | 258.8 | 9/9 | 1.00 | 0.63 | 0.28 | 4 | 11.6% | 0.44 | 0.36 | 19.9% | 16.5% | 18.0% | 19.2%/13.7% | 6.6 (interpolated) | pass | 0.038 (unverified) | -0.01 |
| 406 | `cfg_101d` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=2R, exit=16:00 | 0/12/112/83 | 207 | 15.9% | 2.9% | 0.96 | -3.6% | 367 | 1.44 | 3.6% | 100.0 | 8/8 | 1.00 | 0.64 | 0.32 | 4 | 7.9% | 0.48 | 0.49 | 15.5% | 14.8% | 14.8% | 14.6%/12.3% | 13.4 (interpolated) | pass | 0.039 (unverified) | 0.17 |
| 407 | `cfg_78ab` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=11:00 | 199/0/175/0 | 374 | 16.6% | 3.0% | 0.85 | -3.7% | 192 | 1.29 | 4.0% | 181.8 | 7/7 | 0.86 | 0.87 | -0.01 | 4 | 9.4% | 0.44 | 0.46 | 14.5% | 12.2% | 14.8% | 14.9%/10.9% | 7.0 (interpolated) | pass | 0.026 (unverified) | 0.18 |
| 408 | `cfg_e212` | timeframe=1min, level=lon, side=both, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/100/204/0 | 304 | 24.4% | 4.4% | 0.83 | -4.4% | 121 | 1.33 | 10.5% | 150.7 | 7/7 | 1.00 | 0.52 | 0.31 | 5 | 13.9% | 0.38 | 0.60 | 23.1% | 22.5% | 21.3% | 21.7%/16.2% | 11.3 (interpolated) | pass | 0.018 (unverified) | -0.27 |
| 409 | `cfg_5588` | timeframe=1min, level=box, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 135/0/393/0 | 528 | 17.7% | 3.2% | 0.80 | -4.4% | 148 | 1.26 | 6.4% | 258.5 | 9/9 | 0.89 | 0.80 | 0.01 | 4 | 4.2% | 0.72 | 0.60 | 15.8% | 13.6% | 23.2% | 15.9%/11.0% | 5.5 (interpolated) | pass | 0.016 (unverified) | -0.16 |
| 410 | `cfg_51f6` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=3R, exit=12:30 | 10/0/177/86 | 273 | 9.9% | 1.9% | 0.86 | -2.1% | 245 | 1.34 | 1.4% | 131.7 | 10/10 | 1.00 | 0.77 | 0.09 | 5 | 5.1% | 0.48 | 0.45 | 9.1% | 8.3% | 5.2% | 8.9%/7.5% | 6.7 (interpolated) | pass | 0.025 (unverified) | 0.58 |
| 411 | `cfg_ecda` | timeframe=1min, level=asia, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=3R, exit=11:00 | 48/0/42/12 | 102 | 9.3% | 1.8% | 0.85 | -2.2% | 413 | 1.62 | 1.1% | 50.2 | 8/8 | 1.00 | 0.76 | 0.09 | 4 | 5.6% | 0.40 | 0.69 | 8.9% | 8.7% | 11.2% | 8.6%/6.5% | 14.0 (interpolated) | pass | 0.019 (unverified) | 0.77 |
| 412 | `cfg_333b` | timeframe=1min, level=asia, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=12:30 | 52/0/115/0 | 167 | 12.1% | 2.3% | 0.94 | -1.5% | 155 | 1.62 | 2.3% | 80.3 | 8/8 | 1.00 | 0.77 | 0.17 | 5 | 7.5% | 0.36 | 0.69 | 11.5% | 10.9% | 7.8% | 11.0%/8.7% | 11.4 (interpolated) | pass | 0.023 (unverified) | 0.26 |
| 413 | `cfg_9522` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=none, exit=11:00 | 140/0/133/0 | 273 | 14.5% | 2.7% | 0.79 | -2.9% | 184 | 1.31 | 2.9% | 132.5 | 8/8 | 0.88 | 0.78 | 0.01 | 4 | 6.7% | 0.50 | 0.59 | 13.0% | 11.6% | 9.0% | 12.5%/9.2% | 8.4 (interpolated) | pass | 0.017 (unverified) | -0.13 |
| 414 | `cfg_58d2` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=3R, exit=16:00 | 0/2/253/119 | 374 | 12.0% | 2.2% | 0.85 | -3.4% | 417 | 1.29 | 2.4% | 182.6 | 9/9 | 1.00 | 0.79 | 0.06 | 5 | 8.1% | 0.33 | 0.49 | 10.6% | 9.3% | 9.5% | 10.8%/8.0% | 6.0 (interpolated) | pass | 0.023 (unverified) | 0.07 |
| 415 | `cfg_c55a` | timeframe=1min, level=box, side=low, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=16:00 | 0/20/84/42 | 146 | 15.8% | 2.9% | 0.94 | -3.4% | 322 | 1.57 | 3.2% | 70.1 | 7/7 | 0.86 | 0.66 | 0.28 | 4 | 9.9% | 0.36 | 0.56 | 15.3% | 14.7% | 5.7% | 13.6%/9.9% | 16.1 (interpolated) | pass | 0.030 (unverified) | -0.27 |
| 416 | `cfg_531f` | timeframe=1min, level=pdr, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=struct, target=1R, exit=16:00 | 0/2/47/51 | 100 | 3.9% | 0.7% | 0.83 | -0.7% | 286 | 1.57 | 0.4% | 49.1 | 6/6 | 0.83 | 0.24 | 0.59 | 5 | 2.8% | 0.27 | 0.64 | 3.6% | 3.2% | 3.5% | 3.4%/2.6% | 7.1 (interpolated) | pass | 0.022 (unverified) | 0.51 |
| 417 | `cfg_a213` | timeframe=1min, level=box, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=none, exit=11:00 | 295/0/233/0 | 528 | 21.5% | 3.9% | 0.92 | -4.5% | 161 | 1.26 | 5.4% | 257.5 | 7/7 | 0.86 | 0.67 | 0.24 | 3 | 7.9% | 0.57 | 0.42 | 17.9% | 14.8% | 12.9% | 18.0%/12.5% | 6.1 (interpolated) | pass | 0.037 (unverified) | 0.03 |
| 418 | `cfg_75b0` | timeframe=1min, level=lon, side=both, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/124/236/0 | 360 | 26.1% | 4.6% | 0.83 | -5.1% | 237 | 1.31 | 12.3% | 174.5 | 7/7 | 1.00 | 0.63 | 0.20 | 4 | 11.1% | 0.53 | 0.56 | 25.1% | 24.2% | 22.5% | 23.8%/16.7% | 10.2 (interpolated) | pass | 0.019 (unverified) | -0.59 |
| 419 | `cfg_8b86` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=none, exit=12:30 | 57/0/67/0 | 124 | 13.4% | 2.5% | 0.92 | -2.3% | 165 | 1.61 | 2.5% | 59.5 | 9/9 | 1.00 | 0.79 | 0.13 | 4 | 5.1% | 0.58 | 0.64 | 12.5% | 12.2% | 10.5% | 11.6%/9.4% | 16.5 (interpolated) | pass | 0.025 (unverified) | 0.69 |
| 420 | `cfg_2a6c` | timeframe=1min, level=onh, side=both, window=15, pen=0.05, confirm=5, mode=cont, stop=struct, target=3R, exit=12:30 | 38/0/163/55 | 256 | 14.0% | 2.6% | 0.85 | -4.5% | 478 | 1.41 | 2.5% | 123.8 | 8/8 | 1.00 | 0.72 | 0.13 | 4 | 7.2% | 0.49 | 0.60 | 12.9% | 11.8% | 15.4% | 13.0%/9.6% | 9.1 (interpolated) | pass | 0.019 (unverified) | 0.46 |
| 421 | `cfg_fbc8` | timeframe=1min, level=box, side=high, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=3R, exit=12:30 | 5/0/161/77 | 243 | 9.8% | 1.8% | 0.85 | -2.2% | 229 | 1.37 | 1.2% | 117.9 | 10/10 | 1.00 | 0.77 | 0.09 | 5 | 6.9% | 0.29 | 0.55 | 9.0% | 8.3% | 8.4% | 8.9%/7.4% | 7.1 (interpolated) | pass | 0.022 (unverified) | -0.11 |
| 422 | `cfg_3fe4` | timeframe=1min, level=lon, side=both, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/68/292/0 | 360 | 21.0% | 3.8% | 0.88 | -3.2% | 194 | 1.41 | 7.5% | 174.3 | 8/8 | 1.00 | 0.69 | 0.19 | 5 | 15.0% | 0.29 | 0.60 | 19.7% | 17.8% | 16.9% | 18.5%/12.9% | 8.8 (interpolated) | pass | 0.019 (unverified) | -0.09 |
| 423 | `cfg_258d` | timeframe=1min, level=box, side=low, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/57/89/0 | 146 | 19.7% | 3.6% | 0.91 | -4.5% | 229 | 1.64 | 5.4% | 71.0 | 6/6 | 0.83 | 0.72 | 0.19 | 4 | 11.3% | 0.38 | 0.70 | 19.5% | 19.0% | 9.3% | 18.1%/13.6% | 17.9 (interpolated) | pass | 0.018 (unverified) | -0.46 |
| 424 | `cfg_c668` | timeframe=1min, level=asia, side=high, window=15, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=none, exit=11:00 | 79/0/73/0 | 152 | 11.9% | 2.2% | 0.86 | -1.7% | 392 | 1.50 | 1.6% | 74.4 | 6/6 | 1.00 | 0.81 | 0.05 | 4 | 6.2% | 0.47 | 0.61 | 10.9% | 10.3% | 8.5% | 10.2%/7.8% | 11.1 (interpolated) | pass | 0.021 (unverified) | 0.35 |
| 425 | `cfg_eb2d` | timeframe=1min, level=onh, side=low, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=none, exit=12:30 | 39/0/124/0 | 163 | 12.8% | 2.4% | 0.77 | -2.3% | 363 | 1.57 | 1.8% | 78.8 | 7/7 | 1.00 | 0.69 | 0.08 | 5 | 7.4% | 0.39 | 0.92 | 12.3% | 11.7% | 11.5% | 12.0%/9.3% | 11.3 (interpolated) | pass | 0.006 (unverified) | -0.20 |
| 426 | `cfg_b74b` | timeframe=1min, level=pdr, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=struct, target=1R, exit=12:30 | 2/0/47/51 | 100 | 3.9% | 0.7% | 0.83 | -0.7% | 286 | 1.57 | 0.3% | 49.1 | 7/7 | 0.86 | 0.25 | 0.58 | 5 | 2.8% | 0.27 | 0.64 | 3.6% | 3.2% | 3.8% | 3.4%/2.7% | 7.1 (interpolated) | pass | 0.022 (unverified) | 0.38 |
| 427 | `cfg_0a9f` | timeframe=1min, level=box, side=low, window=15, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=16:00 | 0/64/172/0 | 236 | 22.0% | 4.0% | 0.88 | -6.4% | 232 | 1.50 | 6.4% | 115.4 | 6/6 | 0.83 | 0.68 | 0.21 | 5 | 12.6% | 0.38 | 0.71 | 20.7% | 19.8% | 20.9% | 19.6%/15.5% | 12.3 (interpolated) | pass | 0.018 (unverified) | -0.38 |
| 428 | `cfg_a0b8` | timeframe=1min, level=lon, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=3R, exit=12:30 | 6/0/103/55 | 164 | 8.7% | 1.6% | 0.96 | -1.9% | 362 | 1.52 | 0.9% | 79.7 | 8/8 | 1.00 | 0.77 | 0.20 | 4 | 5.6% | 0.34 | 0.48 | 8.2% | 7.6% | 7.2% | 7.8%/6.2% | 9.5 (interpolated) | pass | 0.039 (unverified) | 0.47 |
| 429 | `cfg_c236` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=1, mode=cont, stop=d0.10, target=none, exit=11:00 | 150/0/287/0 | 437 | 14.7% | 2.7% | 0.92 | -4.7% | 360 | 1.32 | 3.0% | 211.0 | 7/7 | 1.00 | 0.94 | -0.03 | 4 | 4.6% | 0.63 | 0.48 | 12.5% | 10.7% | 13.8% | 12.7%/10.3% | 5.4 (interpolated) | pass | 0.030 (unverified) | 0.61 |
| 430 | `cfg_1960` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=2R, exit=12:30 | 22/0/62/40 | 124 | 10.4% | 1.9% | 0.87 | -2.0% | 187 | 1.50 | 1.8% | 60.0 | 10/10 | 1.00 | 0.75 | 0.12 | 4 | 5.7% | 0.43 | 0.56 | 10.0% | 9.4% | 8.7% | 9.4%/7.0% | 15.1 (interpolated) | pass | 0.025 (unverified) | 0.63 |
| 431 | `cfg_aa82` | timeframe=1min, level=asia, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=2R, exit=16:00 | 0/0/68/46 | 114 | 6.1% | 1.2% | 0.81 | -1.0% | 139 | 1.58 | 0.3% | 56.3 | 7/7 | 1.00 | 0.54 | 0.27 | 5 | 3.6% | 0.40 | 0.74 | 5.8% | 5.4% | 6.4% | 5.6%/3.9% | 9.3 (interpolated) | pass | 0.009 (unverified) | 0.64 |
| 432 | `cfg_1428` | timeframe=1min, level=box, side=low, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=12:30 | 44/0/102/44 | 190 | 15.4% | 2.8% | 0.92 | -3.4% | 200 | 1.46 | 2.5% | 91.7 | 9/9 | 0.89 | 0.67 | 0.25 | 5 | 9.9% | 0.36 | 0.50 | 14.3% | 13.7% | 5.3% | 14.0%/10.8% | 12.7 (interpolated) | pass | 0.032 (unverified) | -0.22 |
| 433 | `cfg_7ca1` | timeframe=1min, level=asia, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=1R, exit=12:30 | 0/0/39/63 | 102 | 3.4% | 0.7% | 0.89 | -0.8% | 214 | 1.58 | 0.1% | 49.9 | 9/9 | 0.89 | 0.58 | 0.31 | 5 | 1.9% | 0.44 | 0.50 | 3.1% | 2.8% | 3.0% | 3.1%/2.2% | 6.8 (interpolated) | pass | 0.038 (unverified) | -0.48 |
| 434 | `cfg_e690` | timeframe=1min, level=onh, side=low, window=30, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=12:30 | 48/0/98/0 | 146 | 13.6% | 2.5% | 0.81 | -2.9% | 392 | 1.60 | 1.9% | 70.7 | 8/8 | 1.00 | 0.67 | 0.15 | 5 | 6.3% | 0.53 | 0.78 | 12.7% | 12.2% | 14.0% | 12.6%/8.4% | 12.0 (interpolated) | pass | 0.010 (unverified) | -0.02 |
| 435 | `cfg_7eed` | timeframe=1min, level=box, side=low, window=15, pen=0.00, confirm=5, mode=cont, stop=struct, target=none, exit=16:00 | 0/48/98/0 | 146 | 15.5% | 2.9% | 0.77 | -3.9% | 251 | 1.53 | 4.7% | 70.8 | 6/6 | 0.83 | 0.75 | 0.01 | 4 | 7.2% | 0.50 | 0.87 | 15.2% | 13.9% | 15.3% | 13.2%/9.2% | 13.6 (interpolated) | pass | 0.007 (unverified) | -0.38 |
| 436 | `cfg_8a63` | timeframe=1min, level=box, side=low, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=11:00 | 49/0/72/25 | 146 | 12.2% | 2.3% | 0.89 | -3.3% | 274 | 1.52 | 1.3% | 70.4 | 7/7 | 0.86 | 0.46 | 0.43 | 4 | 7.9% | 0.35 | 0.58 | 11.6% | 11.0% | 8.1% | 11.1%/7.9% | 13.2 (interpolated) | pass | 0.026 (unverified) | 0.04 |
| 437 | `cfg_e936` | timeframe=1min, level=asia, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=2R, exit=12:30 | 12/0/61/41 | 114 | 9.9% | 1.9% | 0.82 | -1.9% | 265 | 1.53 | 1.2% | 56.7 | 8/8 | 1.00 | 0.76 | 0.06 | 4 | 5.0% | 0.48 | 0.66 | 9.7% | 8.8% | 11.6% | 9.0%/6.0% | 13.4 (interpolated) | pass | 0.016 (unverified) | 0.54 |
| 438 | `cfg_0561` | timeframe=1min, level=lon, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=range, exit=11:00 | 12/0/93/58 | 163 | 7.6% | 1.4% | 0.94 | -1.3% | 193 | 1.50 | 0.7% | 79.2 | 8/8 | 1.00 | 0.68 | 0.26 | 4 | 5.0% | 0.32 | 0.54 | 7.1% | 6.6% | 5.9% | 7.0%/5.5% | 8.5 (interpolated) | pass | 0.034 (unverified) | 0.24 |
| 439 | `cfg_d70a` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=3R, exit=12:30 | 18/0/300/129 | 447 | 12.8% | 2.4% | 0.86 | -2.7% | 244 | 1.26 | 2.6% | 216.9 | 11/11 | 0.91 | 0.70 | 0.16 | 4 | 6.9% | 0.43 | 0.44 | 10.7% | 9.0% | 15.7% | 11.8%/8.3% | 5.3 (interpolated) | pass | 0.025 (unverified) | -0.08 |
| 440 | `cfg_2afc` | timeframe=1min, level=box, side=low, window=15, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 101/0/135/0 | 236 | 19.3% | 3.5% | 0.85 | -3.9% | 301 | 1.41 | 4.3% | 114.3 | 7/7 | 0.86 | 0.61 | 0.24 | 5 | 9.9% | 0.48 | 0.66 | 18.5% | 18.0% | 12.1% | 17.1%/12.8% | 11.5 (interpolated) | pass | 0.019 (unverified) | -0.07 |
| 441 | `cfg_57f3` | timeframe=1min, level=lon, side=low, window=60, pen=0.05, confirm=5, mode=fade, stop=d0.10, target=range, exit=12:30 | 5/0/106/47 | 158 | 8.4% | 1.6% | 0.83 | -2.2% | 341 | 1.52 | 0.6% | 77.0 | 9/9 | 1.00 | 0.71 | 0.12 | 4 | 2.9% | 0.64 | 0.75 | 7.9% | 7.5% | 2.6% | 7.9%/6.2% | 9.3 (interpolated) | pass | 0.013 (unverified) | -0.36 |
| 442 | `cfg_aee1` | timeframe=1min, level=box, side=low, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=none, exit=12:30 | 41/0/105/0 | 146 | 12.9% | 2.4% | 0.87 | -3.0% | 251 | 1.74 | 1.8% | 70.1 | 8/8 | 0.88 | 0.70 | 0.16 | 5 | 7.2% | 0.44 | 0.84 | 12.4% | 11.9% | 7.3% | 11.9%/8.5% | 12.5 (interpolated) | pass | 0.009 (unverified) | 0.13 |
| 443 | `cfg_ade2` | timeframe=1min, level=asia, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=1R, exit=11:00 | 0/0/39/63 | 102 | 3.4% | 0.7% | 0.89 | -0.8% | 214 | 1.58 | 0.1% | 49.9 | 8/8 | 0.88 | 0.56 | 0.33 | 5 | 1.9% | 0.44 | 0.50 | 3.1% | 2.8% | 3.0% | 3.1%/2.5% | 6.8 (interpolated) | pass | 0.038 (unverified) | -0.48 |
| 444 | `cfg_2555` | timeframe=1min, level=asia, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=3R, exit=16:00 | 0/1/107/59 | 167 | 9.6% | 1.8% | 0.93 | -1.3% | 175 | 1.53 | 1.1% | 81.1 | 8/8 | 1.00 | 0.62 | 0.30 | 5 | 6.7% | 0.28 | 0.60 | 9.1% | 8.6% | 5.2% | 8.7%/6.6% | 10.1 (interpolated) | pass | 0.027 (unverified) | 0.10 |
| 445 | `cfg_20e1` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=3, mode=fade, stop=d0.20, target=3R, exit=16:00 | 0/16/72/27 | 115 | 10.9% | 2.0% | 0.78 | -3.0% | 752 | 1.57 | 2.4% | 55.5 | 8/8 | 1.00 | 0.69 | 0.09 | 3 | 0.6% | 0.94 | 0.73 | 10.6% | 10.3% | 10.4% | 9.9%/7.8% | 15.0 (interpolated) | pass | 0.011 (unverified) | -0.50 |
| 446 | `cfg_4a2a` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=3R, exit=12:30 | 2/0/130/61 | 193 | 8.4% | 1.6% | 0.81 | -1.8% | 345 | 1.42 | 0.9% | 93.2 | 9/9 | 1.00 | 0.84 | -0.03 | 3 | 3.2% | 0.61 | 0.60 | 7.8% | 7.1% | 3.8% | 7.8%/6.0% | 7.9 (interpolated) | pass | 0.015 (unverified) | 0.18 |
| 447 | `cfg_7d0d` | timeframe=1min, level=onh, side=low, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/47/99/0 | 146 | 19.7% | 3.6% | 0.87 | -3.5% | 534 | 1.60 | 4.8% | 70.5 | 7/7 | 1.00 | 0.68 | 0.19 | 3 | 8.0% | 0.60 | 0.69 | 19.2% | 18.8% | 17.1% | 17.5%/13.2% | 16.5 (interpolated) | pass | 0.016 (unverified) | 0.55 |
| 448 | `cfg_b835` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 50/0/57/0 | 107 | 10.6% | 2.0% | 0.82 | -2.1% | 163 | 1.57 | 2.1% | 51.3 | 8/8 | 1.00 | 0.75 | 0.07 | 4 | 3.9% | 0.60 | 0.74 | 10.3% | 9.9% | 10.3% | 9.7%/7.1% | 16.0 (interpolated) | pass | 0.014 (unverified) | 0.99 |
| 449 | `cfg_c0ff` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=3R, exit=11:00 | 24/0/256/106 | 386 | 11.3% | 2.1% | 0.82 | -2.8% | 199 | 1.27 | 1.5% | 186.2 | 7/7 | 0.86 | 0.79 | 0.03 | 5 | 7.0% | 0.38 | 0.43 | 10.0% | 8.9% | 13.9% | 10.2%/8.3% | 5.4 (interpolated) | pass | 0.021 (unverified) | -0.27 |
| 450 | `cfg_fc55` | timeframe=1min, level=lon, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=3R, exit=12:30 | 2/0/190/95 | 287 | 10.3% | 1.9% | 0.88 | -2.6% | 193 | 1.33 | 1.3% | 139.1 | 9/9 | 1.00 | 0.73 | 0.15 | 5 | 7.1% | 0.30 | 0.39 | 9.2% | 8.3% | 9.4% | 9.3%/7.0% | 6.6 (interpolated) | pass | 0.033 (unverified) | -0.01 |
| 451 | `cfg_90fc` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=3R, exit=16:00 | 0/1/264/121 | 386 | 10.9% | 2.0% | 0.80 | -4.2% | 792 | 1.26 | 1.7% | 186.4 | 8/8 | 1.00 | 0.68 | 0.12 | 3 | 5.1% | 0.53 | 0.41 | 9.7% | 8.7% | 8.0% | 10.1%/7.3% | 5.5 (interpolated) | pass | 0.025 (unverified) | -0.34 |
| 452 | `cfg_75ee` | timeframe=1min, level=lon, side=both, window=60, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/78/345/0 | 423 | 19.2% | 3.5% | 0.76 | -4.2% | 194 | 1.31 | 8.5% | 205.4 | 7/7 | 1.00 | 0.58 | 0.18 | 4 | 11.6% | 0.36 | 0.65 | 17.2% | 15.3% | 15.1% | 17.8%/13.6% | 7.0 (interpolated) | pass | 0.011 (unverified) | -0.06 |
| 453 | `cfg_bf1f` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 47/0/101/0 | 148 | 8.9% | 1.7% | 0.85 | -1.9% | 338 | 1.58 | 1.1% | 71.2 | 8/8 | 1.00 | 0.87 | -0.02 | 4 | 5.5% | 0.37 | 0.75 | 8.3% | 7.8% | 5.5% | 7.9%/6.2% | 9.3 (interpolated) | pass | 0.014 (unverified) | 0.45 |
| 454 | `cfg_15a0` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 63/0/64/0 | 127 | 10.5% | 2.0% | 0.78 | -3.0% | 294 | 1.51 | 2.6% | 61.3 | 8/8 | 1.00 | 0.63 | 0.15 | 4 | 5.2% | 0.50 | 0.79 | 10.0% | 9.6% | 9.4% | 9.5%/7.0% | 13.1 (interpolated) | pass | 0.011 (unverified) | 0.40 |
| 455 | `cfg_17de` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=11:00 | 120/0/104/0 | 224 | 13.8% | 2.6% | 0.87 | -3.6% | 216 | 1.39 | 2.4% | 108.4 | 7/7 | 1.00 | 0.79 | 0.08 | 4 | 9.0% | 0.32 | 0.53 | 12.5% | 11.5% | 10.0% | 11.9%/9.6% | 10.0 (interpolated) | pass | 0.025 (unverified) | 0.17 |
| 456 | `cfg_af0f` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=struct, target=none, exit=11:00 | 55/0/90/0 | 145 | 8.7% | 1.6% | 0.82 | -2.3% | 392 | 1.56 | 1.1% | 69.8 | 8/8 | 1.00 | 0.75 | 0.08 | 4 | 3.1% | 0.61 | 0.75 | 8.1% | 7.6% | 7.7% | 7.9%/6.2% | 9.8 (interpolated) | pass | 0.016 (unverified) | 0.44 |
| 457 | `cfg_8814` | timeframe=1min, level=onh, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=11:00 | 87/0/138/0 | 225 | 9.7% | 1.8% | 0.81 | -4.1% | 554 | 1.41 | 1.8% | 109.6 | 7/7 | 1.00 | 0.75 | 0.06 | 4 | 4.8% | 0.50 | 0.66 | 9.0% | 8.2% | 8.7% | 8.7%/6.8% | 7.1 (interpolated) | pass | 0.022 (unverified) | 1.03 |
| 458 | `cfg_5629` | timeframe=1min, level=lon, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=1R, exit=16:00 | 0/2/120/165 | 287 | 10.3% | 1.9% | 0.79 | -2.6% | 463 | 1.27 | 1.5% | 139.1 | 6/6 | 1.00 | 0.64 | 0.15 | 4 | 5.2% | 0.50 | 0.34 | 9.5% | 8.5% | 10.1% | 9.5%/7.4% | 7.9 (interpolated) | pass | 0.025 (unverified) | -0.35 |
| 459 | `cfg_2a8b` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=3R, exit=11:00 | 72/0/59/14 | 145 | 9.5% | 1.8% | 0.79 | -2.2% | 405 | 1.45 | 1.4% | 70.4 | 9/9 | 1.00 | 0.82 | -0.03 | 4 | 5.7% | 0.37 | 0.67 | 9.2% | 8.7% | 11.9% | 9.2%/7.1% | 10.7 (interpolated) | pass | 0.016 (unverified) | 0.67 |
| 460 | `cfg_868c` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=range, exit=11:00 | 29/0/99/20 | 148 | 7.9% | 1.5% | 0.82 | -1.7% | 268 | 1.53 | 0.9% | 71.2 | 9/9 | 1.00 | 0.85 | -0.03 | 4 | 5.2% | 0.33 | 0.72 | 7.4% | 7.0% | 6.3% | 7.2%/5.4% | 8.7 (interpolated) | pass | 0.015 (unverified) | 0.40 |
| 461 | `cfg_230e` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=3R, exit=16:00 | 0/35/171/67 | 273 | 18.5% | 3.4% | 0.77 | -4.6% | 312 | 1.32 | 6.4% | 132.5 | 9/9 | 1.00 | 0.68 | 0.09 | 4 | 11.7% | 0.37 | 0.64 | 16.9% | 16.7% | 15.2% | 15.6%/11.4% | 11.4 (interpolated) | pass | 0.013 (unverified) | 0.09 |
| 462 | `cfg_031f` | timeframe=1min, level=asia, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=struct, target=1R, exit=11:00 | 0/0/42/60 | 102 | 4.4% | 0.9% | 0.80 | -1.5% | 196 | 1.56 | 0.2% | 50.1 | 7/7 | 0.86 | 0.75 | 0.05 | 5 | 2.5% | 0.43 | 0.60 | 4.1% | 3.8% | 4.4% | 3.9%/3.0% | 8.7 (interpolated) | pass | 0.025 (unverified) | -0.12 |
| 463 | `cfg_1b29` | timeframe=1min, level=asia, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=struct, target=1R, exit=12:30 | 0/0/42/60 | 102 | 4.4% | 0.9% | 0.80 | -1.5% | 196 | 1.56 | 0.2% | 50.1 | 8/8 | 0.88 | 0.67 | 0.14 | 5 | 2.5% | 0.43 | 0.60 | 4.1% | 3.8% | 3.4% | 3.9%/2.8% | 8.7 (interpolated) | pass | 0.025 (unverified) | -0.10 |
| 464 | `cfg_25f9` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=3R, exit=11:00 | 63/0/51/13 | 127 | 9.3% | 1.8% | 0.82 | -2.7% | 340 | 1.52 | 1.3% | 61.9 | 8/8 | 1.00 | 0.76 | 0.06 | 4 | 5.8% | 0.38 | 0.66 | 8.9% | 8.6% | 7.5% | 8.9%/6.9% | 11.6 (interpolated) | pass | 0.020 (unverified) | 0.63 |
| 465 | `cfg_ee3e` | timeframe=1min, level=asia, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=3R, exit=11:00 | 45/0/55/14 | 114 | 9.7% | 1.8% | 0.83 | -2.2% | 233 | 1.55 | 1.1% | 56.4 | 7/7 | 1.00 | 0.73 | 0.10 | 4 | 5.6% | 0.42 | 0.66 | 9.4% | 9.0% | 10.3% | 9.0%/7.0% | 12.8 (interpolated) | pass | 0.018 (unverified) | 0.55 |
| 466 | `cfg_0b0c` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=3R, exit=12:30 | 13/0/262/111 | 386 | 12.4% | 2.3% | 0.85 | -2.8% | 199 | 1.29 | 1.8% | 186.7 | 8/8 | 0.88 | 0.75 | 0.10 | 4 | 6.9% | 0.44 | 0.46 | 10.7% | 9.6% | 14.5% | 10.9%/9.0% | 5.6 (interpolated) | pass | 0.023 (unverified) | -0.01 |
| 467 | `cfg_a5bf` | timeframe=1min, level=lon, side=high, window=60, pen=0.00, confirm=5, mode=fade, stop=d0.20, target=1R, exit=12:30 | 11/0/134/157 | 302 | 11.0% | 2.1% | 0.84 | -3.2% | 461 | 1.27 | 2.0% | 147.7 | 7/7 | 0.86 | 0.60 | 0.25 | 3 | 5.4% | 0.51 | 0.37 | 10.0% | 9.0% | 3.5% | 10.0%/7.8% | 6.9 (interpolated) | pass | 0.037 (unverified) | 0.02 |
| 468 | `cfg_e2ad` | timeframe=1min, level=box, side=low, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=2R, exit=12:30 | 22/0/98/70 | 190 | 13.7% | 2.5% | 0.90 | -3.7% | 205 | 1.42 | 1.9% | 91.6 | 9/9 | 0.89 | 0.61 | 0.29 | 5 | 8.4% | 0.39 | 0.45 | 13.2% | 12.5% | 8.0% | 12.4%/9.3% | 12.2 (interpolated) | pass | 0.032 (unverified) | -0.33 |
| 469 | `cfg_8a21` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=1R, exit=11:00 | 23/0/91/122 | 236 | 10.2% | 1.9% | 0.90 | -3.2% | 362 | 1.36 | 1.2% | 114.8 | 7/7 | 0.86 | 0.86 | 0.05 | 3 | 5.4% | 0.47 | 0.41 | 9.3% | 8.8% | 9.5% | 9.3%/7.6% | 8.0 (interpolated) | pass | 0.038 (unverified) | 0.39 |
| 470 | `cfg_bda7` | timeframe=1min, level=onh, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=3R, exit=11:00 | 16/0/259/111 | 386 | 10.5% | 2.0% | 0.79 | -3.7% | 739 | 1.26 | 1.4% | 186.6 | 8/8 | 1.00 | 0.70 | 0.09 | 3 | 4.7% | 0.55 | 0.43 | 9.3% | 8.1% | 7.0% | 9.7%/7.8% | 5.4 (interpolated) | pass | 0.022 (unverified) | -0.42 |
| 471 | `cfg_bbd4` | timeframe=1min, level=lon, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/36/133/0 | 169 | 11.6% | 2.2% | 0.76 | -2.8% | 417 | 1.52 | 3.9% | 81.3 | 8/8 | 1.00 | 0.55 | 0.21 | 3 | 3.8% | 0.65 | 0.84 | 11.1% | 10.5% | 12.0% | 10.8%/8.1% | 11.1 (interpolated) | pass | 0.008 (unverified) | 0.53 |
| 472 | `cfg_b8d7` | timeframe=1min, level=pdr, side=high, window=30, pen=0.05, confirm=1, mode=cont, stop=struct, target=3R, exit=12:30 | 4/0/83/34 | 121 | 6.0% | 1.1% | 0.82 | -0.8% | 248 | 1.64 | 0.5% | 59.0 | 9/9 | 1.00 | 0.61 | 0.21 | 4 | 2.9% | 0.50 | 0.73 | 5.6% | 5.3% | 3.7% | 5.4%/3.9% | 9.0 (interpolated) | pass | 0.010 (unverified) | 0.57 |
| 473 | `cfg_46a7` | timeframe=1min, level=lon, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=1R, exit=11:00 | 14/0/116/157 | 287 | 9.5% | 1.8% | 0.75 | -2.3% | 449 | 1.26 | 1.2% | 139.1 | 6/6 | 1.00 | 0.65 | 0.11 | 4 | 4.0% | 0.58 | 0.37 | 8.5% | 7.8% | 9.2% | 8.2%/5.8% | 7.4 (interpolated) | pass | 0.020 (unverified) | -0.37 |
| 474 | `cfg_9e25` | timeframe=1min, level=onh, side=low, window=30, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=16:00 | 0/38/108/0 | 146 | 16.7% | 3.1% | 0.85 | -2.8% | 380 | 1.65 | 3.8% | 71.0 | 7/7 | 1.00 | 0.79 | 0.06 | 4 | 7.9% | 0.52 | 0.74 | 16.1% | 15.6% | 17.7% | 14.5%/10.2% | 14.7 (interpolated) | pass | 0.012 (unverified) | 0.29 |
| 475 | `cfg_f928` | timeframe=1min, level=onh, side=high, window=15, pen=0.05, confirm=5, mode=cont, stop=struct, target=none, exit=12:30 | 51/0/107/0 | 158 | 11.8% | 2.2% | 0.86 | -3.0% | 394 | 1.60 | 2.3% | 76.4 | 7/7 | 1.00 | 0.79 | 0.07 | 4 | 4.0% | 0.66 | 0.73 | 11.3% | 10.8% | 10.4% | 10.5%/7.4% | 11.1 (interpolated) | pass | 0.021 (unverified) | 0.74 |
| 476 | `cfg_cdd7` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=2R, exit=12:30 | 0/0/70/54 | 124 | 5.3% | 1.0% | 0.81 | -1.5% | 444 | 1.45 | 0.4% | 60.5 | 11/11 | 1.00 | 0.71 | 0.10 | 5 | 2.8% | 0.46 | 0.52 | 4.9% | 4.5% | 2.3% | 4.9%/3.8% | 8.4 (interpolated) | pass | 0.023 (unverified) | 0.54 |
| 477 | `cfg_dccc` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=range, exit=12:30 | 5/0/119/69 | 193 | 8.9% | 1.7% | 0.92 | -2.3% | 218 | 1.45 | 1.0% | 93.1 | 10/10 | 1.00 | 0.76 | 0.16 | 5 | 5.6% | 0.37 | 0.50 | 8.3% | 7.8% | 6.5% | 8.2%/6.1% | 8.6 (interpolated) | pass | 0.034 (unverified) | 0.68 |
| 478 | `cfg_17f6` | timeframe=1min, level=asia, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=3R, exit=12:30 | 32/0/53/17 | 102 | 10.2% | 1.9% | 0.79 | -2.8% | 443 | 1.60 | 1.7% | 50.0 | 9/9 | 1.00 | 0.67 | 0.12 | 4 | 6.2% | 0.39 | 0.83 | 9.8% | 9.4% | 11.3% | 9.4%/6.9% | 15.7 (interpolated) | pass | 0.011 (unverified) | 0.57 |
| 479 | `cfg_6e04` | timeframe=1min, level=lon, side=low, window=60, pen=0.05, confirm=5, mode=fade, stop=d0.10, target=3R, exit=11:00 | 12/0/102/44 | 158 | 9.3% | 1.8% | 0.98 | -2.0% | 326 | 1.61 | 0.5% | 77.3 | 8/8 | 1.00 | 0.66 | 0.32 | 3 | 1.9% | 0.77 | 0.57 | 8.9% | 8.4% | 2.0% | 8.8%/6.0% | 9.7 (interpolated) | pass | 0.034 (unverified) | -0.19 |
| 480 | `cfg_7019` | timeframe=1min, level=lon, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=3R, exit=11:00 | 16/0/99/49 | 164 | 7.8% | 1.5% | 0.92 | -1.9% | 362 | 1.49 | 0.7% | 79.7 | 7/7 | 0.86 | 0.66 | 0.26 | 4 | 4.1% | 0.46 | 0.52 | 7.2% | 6.6% | 7.0% | 6.9%/5.1% | 8.6 (interpolated) | pass | 0.031 (unverified) | 0.47 |
| 481 | `cfg_5d8a` | timeframe=1min, level=lon, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 77/0/92/0 | 169 | 12.1% | 2.3% | 0.78 | -3.7% | 171 | 1.40 | 3.3% | 81.1 | 8/8 | 1.00 | 0.72 | 0.06 | 3 | 4.3% | 0.61 | 0.68 | 11.7% | 11.1% | 14.2% | 11.3%/8.2% | 11.8 (interpolated) | pass | 0.013 (unverified) | 0.84 |
| 482 | `cfg_39bc` | timeframe=1min, level=box, side=high, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=3R, exit=11:00 | 18/0/157/68 | 243 | 8.7% | 1.6% | 0.79 | -2.2% | 183 | 1.34 | 1.1% | 117.6 | 9/9 | 1.00 | 0.70 | 0.09 | 5 | 6.1% | 0.29 | 0.61 | 8.1% | 7.3% | 6.9% | 7.9%/6.1% | 6.5 (interpolated) | pass | 0.015 (unverified) | -0.01 |
| 483 | `cfg_35d2` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=fade, stop=struct, target=range, exit=12:30 | 15/0/120/28 | 163 | 11.2% | 2.1% | 0.81 | -2.8% | 717 | 1.61 | 1.3% | 78.4 | 8/8 | 1.00 | 0.63 | 0.18 | 4 | 4.1% | 0.64 | 0.79 | 10.7% | 10.2% | 10.5% | 10.0%/7.5% | 10.3 (interpolated) | pass | 0.010 (unverified) | -0.38 |
| 484 | `cfg_c617` | timeframe=1min, level=box, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=2R, exit=12:30 | 80/0/375/217 | 672 | 23.4% | 4.2% | 0.81 | -6.4% | 441 | 1.18 | 7.6% | 326.9 | 9/9 | 0.78 | 0.50 | 0.31 | 4 | 7.4% | 0.68 | 0.34 | 21.2% | 18.1% | 24.6% | 19.8%/13.7% | 6.3 (interpolated) | pass | 0.023 (unverified) | 0.24 |
| 485 | `cfg_680d` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 44/0/80/0 | 124 | 7.7% | 1.5% | 0.79 | -2.5% | 444 | 1.58 | 0.9% | 60.1 | 9/9 | 1.00 | 0.77 | 0.02 | 4 | 1.8% | 0.76 | 0.87 | 7.4% | 6.9% | 4.7% | 7.4%/5.1% | 10.0 (interpolated) | pass | 0.009 (unverified) | 0.80 |
| 486 | `cfg_5a0b` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/33/112/0 | 145 | 14.0% | 2.6% | 0.84 | -3.3% | 453 | 1.78 | 3.5% | 70.0 | 9/9 | 1.00 | 0.80 | 0.04 | 4 | 6.0% | 0.54 | 0.90 | 13.5% | 13.1% | 11.0% | 13.3%/9.5% | 15.3 (interpolated) | pass | 0.006 (unverified) | 0.42 |
| 487 | `cfg_e180` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=3R, exit=11:00 | 15/0/110/47 | 172 | 7.7% | 1.5% | 0.81 | -1.2% | 236 | 1.45 | 0.8% | 82.9 | 10/10 | 1.00 | 0.79 | 0.03 | 4 | 5.1% | 0.32 | 0.66 | 7.1% | 6.6% | 5.3% | 7.0%/5.3% | 7.9 (interpolated) | pass | 0.014 (unverified) | 0.53 |
| 488 | `cfg_2905` | timeframe=1min, level=pdr, side=high, window=30, pen=0.05, confirm=1, mode=cont, stop=struct, target=none, exit=11:00 | 34/0/87/0 | 121 | 6.7% | 1.3% | 0.84 | -1.1% | 319 | 1.69 | 0.7% | 58.9 | 7/7 | 1.00 | 0.61 | 0.22 | 4 | 2.6% | 0.59 | 0.71 | 6.3% | 5.9% | 4.9% | 6.2%/4.7% | 8.9 (interpolated) | pass | 0.012 (unverified) | 0.50 |
| 489 | `cfg_5de6` | timeframe=1min, level=lon, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=3R, exit=12:30 | 2/0/82/45 | 129 | 7.8% | 1.5% | 0.88 | -2.3% | 239 | 1.54 | 0.7% | 62.7 | 9/9 | 1.00 | 0.67 | 0.20 | 5 | 3.5% | 0.54 | 0.54 | 7.4% | 6.9% | 7.5% | 7.0%/4.8% | 11.0 (interpolated) | pass | 0.024 (unverified) | 0.22 |
| 490 | `cfg_4ad2` | timeframe=1min, level=box, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=3R, exit=11:00 | 24/0/266/121 | 411 | 10.9% | 2.0% | 0.79 | -4.7% | 201 | 1.24 | 1.6% | 199.2 | 8/8 | 0.88 | 0.37 | 0.41 | 5 | 7.4% | 0.32 | 0.43 | 9.4% | 8.3% | 8.7% | 10.0%/8.0% | 5.2 (interpolated) | pass | 0.024 (unverified) | -0.21 |
| 491 | `cfg_ec9b` | timeframe=1min, level=asia, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=2R, exit=11:00 | 25/0/54/35 | 114 | 8.7% | 1.6% | 0.80 | -1.8% | 265 | 1.52 | 0.9% | 56.3 | 7/7 | 1.00 | 0.75 | 0.05 | 5 | 5.1% | 0.40 | 0.65 | 8.3% | 7.9% | 11.2% | 7.7%/5.8% | 11.8 (interpolated) | pass | 0.016 (unverified) | 0.66 |
| 492 | `cfg_0367` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=3, mode=fade, stop=d0.20, target=range, exit=16:00 | 0/15/72/28 | 115 | 12.6% | 2.3% | 0.86 | -3.6% | 748 | 1.67 | 2.5% | 55.3 | 8/8 | 1.00 | 0.77 | 0.09 | 3 | 1.8% | 0.85 | 0.70 | 12.2% | 11.9% | 10.1% | 11.7%/9.1% | 16.4 (interpolated) | pass | 0.015 (unverified) | -0.14 |
| 493 | `cfg_243d` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=fade, stop=d0.20, target=2R, exit=11:00 | 44/0/96/59 | 199 | 12.6% | 2.4% | 0.86 | -2.4% | 468 | 1.39 | 1.5% | 95.6 | 9/9 | 0.89 | 0.61 | 0.24 | 3 | 4.4% | 0.62 | 0.49 | 11.9% | 11.1% | 11.9% | 11.3%/8.6% | 11.4 (interpolated) | pass | 0.026 (unverified) | 0.39 |
| 494 | `cfg_adb2` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=none, exit=12:30 | 97/0/110/0 | 207 | 13.0% | 2.4% | 0.79 | -3.9% | 400 | 1.37 | 4.1% | 99.9 | 8/8 | 1.00 | 0.63 | 0.16 | 3 | 6.4% | 0.51 | 0.67 | 12.4% | 11.9% | 8.8% | 12.0%/9.1% | 10.2 (interpolated) | pass | 0.015 (unverified) | 0.12 |
| 495 | `cfg_3bbe` | timeframe=1min, level=box, side=high, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=2R, exit=12:30 | 32/0/130/81 | 243 | 12.9% | 2.4% | 0.76 | -4.1% | 385 | 1.30 | 2.9% | 117.8 | 9/9 | 0.89 | 0.65 | 0.11 | 5 | 7.9% | 0.39 | 0.59 | 12.4% | 11.5% | 9.5% | 11.1%/8.8% | 9.7 (interpolated) | pass | 0.015 (unverified) | 0.10 |
| 496 | `cfg_798c` | timeframe=1min, level=onh, side=high, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=1R, exit=12:30 | 10/0/67/91 | 168 | 8.1% | 1.5% | 0.85 | -2.3% | 347 | 1.40 | 1.3% | 81.7 | 7/7 | 1.00 | 0.74 | 0.11 | 5 | 5.5% | 0.31 | 0.48 | 7.7% | 7.2% | 8.8% | 7.3%/5.9% | 10.0 (interpolated) | pass | 0.032 (unverified) | 0.21 |
| 497 | `cfg_50db` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=3R, exit=12:30 | 71/0/109/27 | 207 | 12.4% | 2.3% | 0.78 | -4.0% | 474 | 1.36 | 3.5% | 99.7 | 9/9 | 1.00 | 0.63 | 0.15 | 4 | 6.8% | 0.43 | 0.69 | 11.1% | 10.4% | 10.9% | 10.5%/7.8% | 9.6 (interpolated) | pass | 0.015 (unverified) | 0.07 |
| 498 | `cfg_2584` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=fade, stop=d0.20, target=1R, exit=11:00 | 16/0/65/82 | 163 | 6.5% | 1.2% | 0.78 | -3.3% | 790 | 1.37 | 0.7% | 78.8 | 6/6 | 1.00 | 0.65 | 0.13 | 3 | 0.1% | 0.99 | 0.45 | 5.9% | 5.5% | 7.1% | 5.8%/4.6% | 7.8 (interpolated) | pass | 0.024 (unverified) | -0.59 |
| 499 | `cfg_024e` | timeframe=1min, level=lon, side=high, window=60, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/32/118/0 | 150 | 12.1% | 2.3% | 0.79 | -3.1% | 430 | 1.59 | 3.5% | 72.4 | 8/8 | 1.00 | 0.71 | 0.07 | 3 | 2.9% | 0.72 | 0.82 | 11.6% | 10.6% | 7.1% | 11.0%/8.2% | 11.9 (interpolated) | pass | 0.008 (unverified) | 0.63 |
| 500 | `cfg_edd6` | timeframe=1min, level=lon, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=3R, exit=11:00 | 16/0/185/86 | 287 | 9.6% | 1.8% | 0.84 | -2.6% | 193 | 1.32 | 1.1% | 139.0 | 8/8 | 1.00 | 0.61 | 0.23 | 5 | 6.6% | 0.29 | 0.42 | 8.8% | 8.1% | 9.2% | 8.8%/6.8% | 6.3 (interpolated) | pass | 0.026 (unverified) | -0.11 |
| 501 | `cfg_de8e` | timeframe=1min, level=lon, side=high, window=60, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/82/142/0 | 224 | 17.0% | 3.1% | 0.75 | -4.1% | 241 | 1.33 | 8.3% | 109.1 | 6/6 | 1.00 | 0.66 | 0.09 | 5 | 6.2% | 0.60 | 0.66 | 15.5% | 13.8% | 19.5% | 14.3%/10.3% | 10.8 (interpolated) | pass | 0.012 (unverified) | 0.55 |
| 502 | `cfg_9821` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/33/94/0 | 127 | 12.2% | 2.3% | 0.80 | -3.0% | 453 | 1.80 | 3.2% | 61.2 | 8/8 | 1.00 | 0.73 | 0.07 | 4 | 4.5% | 0.61 | 0.97 | 11.7% | 11.3% | 6.2% | 11.3%/8.8% | 15.2 (interpolated) | pass | 0.004 (unverified) | 0.24 |
| 503 | `cfg_a63c` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=3R, exit=16:00 | 0/4/306/137 | 447 | 11.9% | 2.2% | 0.79 | -3.7% | 353 | 1.24 | 3.0% | 217.2 | 10/10 | 1.00 | 0.57 | 0.22 | 4 | 5.6% | 0.49 | 0.50 | 10.0% | 8.8% | 15.6% | 10.2%/7.5% | 5.2 (interpolated) | pass | 0.017 (unverified) | 0.04 |
| 504 | `cfg_88f8` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=2R, exit=12:30 | 18/0/54/35 | 107 | 8.5% | 1.6% | 0.76 | -2.1% | 267 | 1.47 | 1.5% | 51.7 | 9/9 | 1.00 | 0.61 | 0.15 | 4 | 3.9% | 0.51 | 0.67 | 8.1% | 7.9% | 8.5% | 7.6%/6.0% | 14.3 (interpolated) | pass | 0.013 (unverified) | 0.89 |
| 505 | `cfg_4858` | timeframe=1min, level=lon, side=high, window=60, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/56/94/0 | 150 | 15.5% | 2.9% | 0.81 | -4.0% | 267 | 1.48 | 5.6% | 72.5 | 7/7 | 1.00 | 0.71 | 0.09 | 4 | 5.2% | 0.61 | 0.68 | 14.8% | 13.8% | 13.0% | 14.3%/9.7% | 15.7 (interpolated) | pass | 0.014 (unverified) | 0.16 |
| 506 | `cfg_da66` | timeframe=1min, level=lon, side=both, window=60, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/52/225/0 | 277 | 15.8% | 2.9% | 0.77 | -3.6% | 400 | 1.41 | 5.7% | 134.3 | 8/8 | 1.00 | 0.50 | 0.27 | 3 | 7.0% | 0.52 | 0.74 | 13.5% | 12.7% | 7.3% | 14.5%/9.9% | 8.3 (interpolated) | pass | 0.010 (unverified) | 0.37 |
| 507 | `cfg_1ada` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=fade, stop=d0.20, target=range, exit=12:30 | 35/0/94/34 | 163 | 12.8% | 2.4% | 0.78 | -4.4% | 748 | 1.48 | 2.2% | 78.4 | 8/8 | 1.00 | 0.65 | 0.13 | 3 | 0.8% | 0.94 | 0.71 | 12.3% | 11.9% | 13.3% | 12.2%/8.6% | 12.5 (interpolated) | pass | 0.011 (unverified) | -0.36 |
| 508 | `cfg_c522` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=fade, stop=d0.20, target=1R, exit=12:30 | 2/0/82/115 | 199 | 10.1% | 1.9% | 0.92 | -2.8% | 715 | 1.39 | 0.9% | 95.1 | 9/9 | 1.00 | 0.70 | 0.22 | 3 | 3.6% | 0.64 | 0.34 | 9.4% | 8.9% | 9.4% | 9.0%/7.6% | 10.0 (interpolated) | pass | 0.046 (unverified) | 0.10 |
| 509 | `cfg_d4bc` | timeframe=1min, level=lon, side=high, window=60, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 55/0/95/0 | 150 | 8.2% | 1.5% | 0.77 | -2.6% | 430 | 1.49 | 1.1% | 73.0 | 8/8 | 1.00 | 0.71 | 0.06 | 3 | 0.9% | 0.88 | 0.85 | 7.4% | 6.9% | 5.2% | 7.3%/5.1% | 8.5 (interpolated) | pass | 0.009 (unverified) | 0.67 |
| 510 | `cfg_d6ef` | timeframe=1min, level=onh, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=3R, exit=12:30 | 3/0/160/73 | 236 | 8.7% | 1.6% | 0.77 | -1.6% | 495 | 1.34 | 1.1% | 114.5 | 10/10 | 1.00 | 0.79 | -0.02 | 4 | 2.9% | 0.66 | 0.58 | 7.8% | 7.0% | 2.5% | 7.8%/5.8% | 6.9 (interpolated) | pass | 0.013 (unverified) | 0.50 |
| 511 | `cfg_7aa8` | timeframe=1min, level=lon, side=low, window=60, pen=0.05, confirm=5, mode=fade, stop=d0.10, target=3R, exit=12:30 | 3/0/109/46 | 158 | 8.1% | 1.5% | 0.84 | -2.4% | 341 | 1.50 | 0.6% | 77.3 | 9/9 | 1.00 | 0.64 | 0.20 | 4 | 0.8% | 0.88 | 0.66 | 7.6% | 7.0% | 1.1% | 7.1%/5.4% | 8.5 (interpolated) | pass | 0.015 (unverified) | -0.12 |
| 512 | `cfg_d8db` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=3R, exit=11:00 | 10/0/96/42 | 148 | 7.4% | 1.4% | 0.81 | -1.3% | 467 | 1.50 | 0.7% | 71.4 | 9/9 | 1.00 | 0.80 | 0.01 | 4 | 4.4% | 0.41 | 0.69 | 6.9% | 6.4% | 4.7% | 6.9%/5.0% | 8.5 (interpolated) | pass | 0.014 (unverified) | 0.29 |
| 513 | `cfg_0e6e` | timeframe=1min, level=box, side=high, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=2R, exit=12:30 | 35/0/147/91 | 273 | 14.4% | 2.7% | 0.79 | -4.4% | 421 | 1.30 | 3.2% | 132.1 | 10/10 | 0.90 | 0.70 | 0.09 | 5 | 6.8% | 0.53 | 0.53 | 13.8% | 11.9% | 9.0% | 12.8%/9.5% | 9.4 (interpolated) | pass | 0.018 (unverified) | -0.05 |
| 514 | `cfg_f787` | timeframe=1min, level=box, side=high, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.20, target=3R, exit=16:00 | 0/49/229/86 | 364 | 22.1% | 4.0% | 0.83 | -4.4% | 268 | 1.29 | 9.1% | 177.1 | 8/8 | 1.00 | 0.62 | 0.21 | 3 | 10.5% | 0.53 | 0.49 | 21.2% | 19.6% | 18.1% | 20.2%/14.8% | 9.9 (interpolated) | pass | 0.020 (unverified) | 0.65 |
| 515 | `cfg_4e90` | timeframe=1min, level=onh, side=both, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=1R, exit=11:00 | 35/0/108/141 | 284 | 10.2% | 1.9% | 0.86 | -3.1% | 357 | 1.30 | 1.4% | 138.4 | 6/6 | 0.83 | 0.62 | 0.23 | 3 | 4.5% | 0.56 | 0.40 | 9.6% | 9.1% | 9.5% | 9.3%/7.9% | 7.4 (interpolated) | pass | 0.031 (unverified) | 0.42 |
| 516 | `cfg_bc2b` | timeframe=1min, level=lon, side=low, window=60, pen=0.05, confirm=5, mode=fade, stop=d0.10, target=none, exit=11:00 | 52/0/106/0 | 158 | 9.0% | 1.7% | 0.81 | -2.4% | 371 | 1.55 | 0.9% | 77.7 | 7/7 | 1.00 | 0.54 | 0.27 | 4 | 4.0% | 0.53 | 0.78 | 8.5% | 8.0% | 2.8% | 8.4%/6.1% | 9.0 (interpolated) | pass | 0.013 (unverified) | -0.75 |
| 517 | `cfg_c7a7` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=fade, stop=struct, target=range, exit=16:00 | 0/7/126/30 | 163 | 10.2% | 1.9% | 0.75 | -2.8% | 361 | 1.54 | 1.8% | 78.8 | 7/7 | 1.00 | 0.56 | 0.19 | 4 | 3.9% | 0.62 | 0.79 | 10.0% | 9.5% | 9.7% | 9.7%/7.1% | 9.5 (interpolated) | pass | 0.008 (unverified) | -0.17 |
| 518 | `cfg_bb47` | timeframe=1min, level=lon, side=high, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=1R, exit=11:00 | 7/0/37/59 | 103 | 6.6% | 1.3% | 0.86 | -1.6% | 212 | 1.55 | 0.5% | 50.3 | 7/7 | 1.00 | 0.60 | 0.27 | 4 | 4.2% | 0.35 | 0.49 | 6.3% | 6.0% | 2.9% | 6.0%/4.6% | 13.0 (interpolated) | pass | 0.031 (unverified) | 0.06 |
| 519 | `cfg_8634` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=none, exit=11:00 | 112/0/95/0 | 207 | 12.6% | 2.3% | 0.85 | -2.2% | 182 | 1.41 | 2.2% | 99.8 | 7/7 | 1.00 | 0.76 | 0.09 | 4 | 6.6% | 0.44 | 0.58 | 11.6% | 10.7% | 9.1% | 11.0%/9.0% | 9.2 (interpolated) | pass | 0.022 (unverified) | 0.21 |
| 520 | `cfg_407e` | timeframe=1min, level=box, side=low, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=3R, exit=12:30 | 49/0/123/49 | 221 | 16.4% | 3.0% | 0.88 | -3.1% | 457 | 1.40 | 2.9% | 106.5 | 8/8 | 0.88 | 0.48 | 0.41 | 4 | 7.3% | 0.55 | 0.50 | 15.9% | 14.7% | 6.3% | 14.8%/10.4% | 11.8 (interpolated) | pass | 0.027 (unverified) | -0.33 |
| 521 | `cfg_66e3` | timeframe=1min, level=onh, side=low, window=30, pen=0.05, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 61/0/85/0 | 146 | 14.7% | 2.7% | 0.80 | -3.2% | 388 | 1.50 | 2.5% | 70.6 | 8/8 | 1.00 | 0.59 | 0.21 | 4 | 6.7% | 0.55 | 0.74 | 14.3% | 13.8% | 10.4% | 13.5%/9.5% | 12.9 (interpolated) | pass | 0.012 (unverified) | 0.50 |
| 522 | `cfg_53d5` | timeframe=1min, level=asia, side=high, window=15, pen=0.05, confirm=1, mode=cont, stop=d0.10, target=none, exit=11:00 | 46/0/106/0 | 152 | 9.3% | 1.7% | 0.82 | -2.6% | 474 | 1.55 | 1.1% | 74.8 | 7/7 | 1.00 | 0.70 | 0.12 | 3 | 4.1% | 0.54 | 0.71 | 8.7% | 8.0% | 7.1% | 8.4%/5.8% | 9.0 (interpolated) | pass | 0.013 (unverified) | 0.74 |
| 523 | `cfg_a3b3` | timeframe=1min, level=onh, side=low, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 36/0/97/0 | 133 | 10.2% | 1.9% | 0.81 | -3.0% | 170 | 1.64 | 0.8% | 64.2 | 8/8 | 1.00 | 0.64 | 0.17 | 5 | 5.9% | 0.39 | 0.81 | 9.3% | 9.0% | 4.2% | 9.3%/7.0% | 11.0 (interpolated) | pass | 0.009 (unverified) | 0.01 |
| 524 | `cfg_e912` | timeframe=1min, level=lon, side=high, window=60, pen=0.00, confirm=5, mode=fade, stop=d0.20, target=1R, exit=16:00 | 0/3/140/159 | 302 | 10.7% | 2.0% | 0.82 | -3.4% | 511 | 1.26 | 2.2% | 147.8 | 6/6 | 0.83 | 0.59 | 0.23 | 3 | 4.8% | 0.55 | 0.39 | 9.6% | 8.7% | 3.4% | 9.9%/7.9% | 6.6 (interpolated) | pass | 0.033 (unverified) | -0.02 |
| 525 | `cfg_0bf0` | timeframe=1min, level=lon, side=high, window=60, pen=0.05, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/66/278/0 | 344 | 16.6% | 3.0% | 0.79 | -5.2% | 395 | 1.34 | 7.3% | 167.5 | 7/7 | 1.00 | 0.52 | 0.28 | 3 | 3.1% | 0.78 | 0.62 | 15.6% | 14.2% | 11.9% | 14.7%/11.4% | 7.8 (interpolated) | pass | 0.013 (unverified) | 0.70 |
| 526 | `cfg_7a46` | timeframe=1min, level=box, side=low, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 48/0/143/0 | 191 | 15.0% | 2.8% | 0.88 | -2.7% | 205 | 1.63 | 2.1% | 91.8 | 9/9 | 0.89 | 0.77 | 0.11 | 5 | 9.9% | 0.34 | 0.77 | 14.4% | 13.4% | 10.3% | 13.5%/9.3% | 11.3 (interpolated) | pass | 0.013 (unverified) | -0.01 |
| 527 | `cfg_7022` | timeframe=1min, level=onh, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=struct, target=3R, exit=11:00 | 17/0/144/63 | 224 | 8.0% | 1.5% | 0.80 | -2.6% | 386 | 1.36 | 0.9% | 108.1 | 7/7 | 1.00 | 0.76 | 0.05 | 4 | 5.0% | 0.37 | 0.57 | 7.2% | 6.6% | 7.7% | 7.4%/5.4% | 6.1 (interpolated) | pass | 0.018 (unverified) | 0.40 |
| 528 | `cfg_bd40` | timeframe=1min, level=asia, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=1R, exit=12:30 | 2/0/47/65 | 114 | 6.3% | 1.2% | 0.78 | -2.1% | 351 | 1.45 | 0.5% | 56.8 | 7/7 | 0.86 | 0.72 | 0.06 | 3 | 2.4% | 0.60 | 0.55 | 5.9% | 5.6% | 5.9% | 5.8%/4.6% | 9.3 (interpolated) | pass | 0.021 (unverified) | 0.36 |
| 529 | `cfg_66c4` | timeframe=1min, level=onh, side=high, window=60, pen=0.00, confirm=5, mode=fade, stop=d0.20, target=range, exit=12:30 | 82/0/217/77 | 376 | 18.1% | 3.3% | 0.75 | -5.2% | 373 | 1.26 | 5.1% | 182.7 | 8/8 | 1.00 | 0.60 | 0.15 | 4 | 6.6% | 0.64 | 0.56 | 16.8% | 15.7% | 17.9% | 16.2%/11.3% | 7.6 (interpolated) | pass | 0.013 (unverified) | -0.63 |
| 530 | `cfg_f995` | timeframe=1min, level=pdr, side=high, window=30, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=3R, exit=12:30 | 47/0/61/13 | 121 | 10.3% | 1.9% | 0.79 | -2.0% | 245 | 1.52 | 2.2% | 58.9 | 9/9 | 1.00 | 0.69 | 0.10 | 5 | 6.5% | 0.37 | 0.74 | 9.9% | 9.4% | 4.2% | 9.3%/6.7% | 13.8 (interpolated) | pass | 0.013 (unverified) | 0.59 |
| 531 | `cfg_d52d` | timeframe=1min, level=asia, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=3R, exit=11:00 | 3/0/84/42 | 129 | 7.1% | 1.3% | 0.83 | -1.8% | 278 | 1.55 | 0.4% | 62.4 | 9/9 | 1.00 | 0.42 | 0.40 | 4 | 4.1% | 0.42 | 0.71 | 6.7% | 6.3% | 1.9% | 6.3%/5.1% | 9.0 (interpolated) | pass | 0.012 (unverified) | 0.27 |
| 532 | `cfg_d6a1` | timeframe=1min, level=onh, side=high, window=30, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=none, exit=11:00 | 179/0/166/0 | 345 | 13.9% | 2.6% | 0.77 | -3.8% | 354 | 1.26 | 3.6% | 166.5 | 7/7 | 1.00 | 0.69 | 0.08 | 4 | 6.0% | 0.52 | 0.50 | 12.8% | 11.6% | 10.6% | 12.6%/9.0% | 6.6 (interpolated) | pass | 0.017 (unverified) | 0.49 |
| 533 | `cfg_0815` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=none, exit=12:30 | 80/0/114/0 | 194 | 13.1% | 2.4% | 0.75 | -3.5% | 216 | 1.35 | 3.7% | 93.8 | 8/8 | 1.00 | 0.55 | 0.20 | 3 | 4.2% | 0.68 | 0.70 | 12.2% | 11.5% | 12.5% | 12.9%/9.1% | 10.2 (interpolated) | pass | 0.011 (unverified) | 0.58 |
| 534 | `cfg_e47d` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=fade, stop=d0.10, target=3R, exit=12:30 | 3/0/113/47 | 163 | 6.8% | 1.3% | 0.79 | -2.4% | 759 | 1.44 | 0.6% | 78.6 | 9/9 | 1.00 | 0.70 | 0.10 | 3 | 2.5% | 0.64 | 0.63 | 6.4% | 5.9% | 4.1% | 6.0%/4.8% | 7.4 (interpolated) | pass | 0.013 (unverified) | -0.67 |
| 535 | `cfg_9107` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=fade, stop=d0.20, target=range, exit=16:00 | 0/20/102/41 | 163 | 13.4% | 2.5% | 0.80 | -4.4% | 743 | 1.48 | 3.4% | 78.4 | 7/7 | 1.00 | 0.68 | 0.13 | 3 | 2.3% | 0.83 | 0.65 | 13.0% | 11.9% | 15.5% | 12.2%/8.4% | 12.6 (interpolated) | pass | 0.014 (unverified) | -0.21 |
| 536 | `cfg_ce07` | timeframe=1min, level=asia, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/45/148/0 | 193 | 16.7% | 3.1% | 0.90 | -2.7% | 260 | 1.67 | 4.6% | 93.1 | 8/8 | 1.00 | 0.77 | 0.14 | 4 | 10.4% | 0.36 | 0.79 | 15.4% | 14.9% | 13.3% | 15.6%/12.0% | 13.3 (interpolated) | pass | 0.013 (unverified) | 0.30 |
| 537 | `cfg_65d3` | timeframe=1min, level=asia, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 39/0/90/0 | 129 | 9.0% | 1.7% | 0.82 | -1.7% | 183 | 1.64 | 0.8% | 62.0 | 8/8 | 1.00 | 0.51 | 0.32 | 4 | 4.8% | 0.46 | 0.83 | 8.5% | 8.1% | 2.1% | 8.2%/5.4% | 10.5 (interpolated) | pass | 0.009 (unverified) | 0.50 |
| 538 | `cfg_656c` | timeframe=1min, level=asia, side=high, window=60, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=12:30 | 55/0/138/0 | 193 | 11.6% | 2.2% | 0.85 | -1.8% | 190 | 1.51 | 2.5% | 93.0 | 9/9 | 1.00 | 0.72 | 0.12 | 5 | 6.9% | 0.38 | 0.75 | 10.8% | 10.2% | 9.6% | 10.3%/7.4% | 9.6 (interpolated) | pass | 0.013 (unverified) | 0.11 |
| 539 | `cfg_13cb` | timeframe=1min, level=pdr, side=high, window=30, pen=0.05, confirm=1, mode=cont, stop=struct, target=range, exit=12:30 | 22/0/93/6 | 121 | 7.6% | 1.4% | 0.81 | -1.3% | 309 | 1.74 | 1.1% | 59.1 | 9/9 | 1.00 | 0.74 | 0.07 | 3 | 3.9% | 0.48 | 0.85 | 7.1% | 6.8% | 5.5% | 7.2%/5.5% | 10.2 (interpolated) | pass | 0.007 (unverified) | 0.66 |
| 540 | `cfg_89c9` | timeframe=1min, level=onh, side=low, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=range, exit=12:30 | 7/0/97/29 | 133 | 9.4% | 1.8% | 0.81 | -2.6% | 221 | 1.60 | 0.8% | 64.1 | 10/10 | 1.00 | 0.65 | 0.17 | 5 | 5.1% | 0.46 | 0.75 | 8.8% | 8.4% | 5.1% | 8.8%/6.9% | 11.4 (interpolated) | pass | 0.015 (unverified) | 0.44 |
| 541 | `cfg_c372` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=2R, exit=12:30 | 21/0/106/67 | 194 | 11.3% | 2.1% | 0.76 | -4.8% | 363 | 1.32 | 2.4% | 93.8 | 9/9 | 1.00 | 0.52 | 0.23 | 4 | 3.8% | 0.64 | 0.56 | 10.4% | 9.8% | 11.8% | 10.2%/6.5% | 10.5 (interpolated) | pass | 0.015 (unverified) | 0.55 |
| 542 | `cfg_7456` | timeframe=1min, level=box, side=low, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 86/0/104/0 | 190 | 16.1% | 3.0% | 0.84 | -3.4% | 200 | 1.47 | 3.4% | 91.8 | 8/8 | 0.88 | 0.66 | 0.18 | 5 | 7.9% | 0.51 | 0.70 | 14.7% | 14.0% | 6.8% | 14.7%/9.4% | 12.4 (interpolated) | pass | 0.016 (unverified) | -0.19 |
| 543 | `cfg_f68e` | timeframe=1min, level=lon, side=high, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.20, target=1R, exit=12:30 | 1/0/40/62 | 103 | 6.8% | 1.3% | 0.87 | -1.4% | 214 | 1.54 | 0.5% | 50.3 | 8/8 | 1.00 | 0.67 | 0.20 | 4 | 4.4% | 0.33 | 0.48 | 6.5% | 6.2% | 3.3% | 6.0%/4.7% | 13.5 (interpolated) | pass | 0.031 (unverified) | 0.15 |
| 544 | `cfg_497d` | timeframe=1min, level=asia, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.20, target=range, exit=11:00 | 15/0/47/49 | 111 | 7.3% | 1.4% | 0.80 | -2.1% | 351 | 1.52 | 0.6% | 55.5 | 7/7 | 1.00 | 0.64 | 0.15 | 3 | 3.4% | 0.54 | 0.65 | 6.9% | 6.7% | 6.5% | 6.7%/5.1% | 11.0 (interpolated) | pass | 0.019 (unverified) | 0.73 |
| 545 | `cfg_8c23` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=5, mode=fade, stop=d0.10, target=2R, exit=12:30 | 1/0/102/60 | 163 | 5.2% | 1.0% | 0.76 | -3.0% | 850 | 1.39 | 0.4% | 78.8 | 9/9 | 1.00 | 0.71 | 0.06 | 3 | -0.3% | 1.06 | 0.57 | 4.5% | 3.8% | 4.4% | 4.7%/3.6% | 5.6 (interpolated) | pass | 0.015 (unverified) | -0.54 |
| 546 | `cfg_4e72` | timeframe=1min, level=lon, side=high, window=15, pen=0.05, confirm=1, mode=cont, stop=d0.10, target=none, exit=12:30 | 53/0/156/0 | 209 | 10.9% | 2.0% | 0.77 | -2.8% | 351 | 1.42 | 2.6% | 100.7 | 8/8 | 1.00 | 0.61 | 0.16 | 3 | 1.3% | 0.87 | 0.77 | 10.0% | 9.4% | 6.7% | 10.0%/7.4% | 8.6 (interpolated) | pass | 0.009 (unverified) | 0.43 |
| 547 | `cfg_63af` | timeframe=1min, level=lon, side=both, window=60, pen=0.05, confirm=3, mode=fade, stop=d0.10, target=range, exit=12:30 | 6/0/132/57 | 195 | 8.2% | 1.5% | 0.78 | -2.6% | 524 | 1.42 | 0.7% | 94.4 | 10/10 | 1.00 | 0.61 | 0.16 | 4 | 4.6% | 0.44 | 0.75 | 7.6% | 6.9% | 3.0% | 7.4%/4.9% | 7.9 (interpolated) | pass | 0.010 (unverified) | 0.30 |
| 548 | `cfg_f496` | timeframe=1min, level=onh, side=high, window=60, pen=0.05, confirm=1, mode=cont, stop=d0.20, target=2R, exit=16:00 | 0/27/261/149 | 437 | 17.3% | 3.2% | 0.75 | -6.0% | 269 | 1.21 | 8.4% | 212.0 | 7/7 | 1.00 | 0.59 | 0.16 | 4 | 6.9% | 0.57 | 0.46 | 15.1% | 12.4% | 15.6% | 14.8%/10.6% | 6.8 (interpolated) | pass | 0.016 (unverified) | 0.54 |
| 549 | `cfg_b82e` | timeframe=1min, level=onh, side=high, window=15, pen=0.05, confirm=5, mode=cont, stop=struct, target=range, exit=12:30 | 19/0/101/37 | 157 | 9.0% | 1.7% | 0.79 | -2.9% | 384 | 1.49 | 1.5% | 75.9 | 8/8 | 1.00 | 0.73 | 0.06 | 4 | 3.6% | 0.60 | 0.73 | 8.5% | 8.0% | 7.6% | 8.1%/5.9% | 9.1 (interpolated) | pass | 0.017 (unverified) | 0.73 |
| 550 | `cfg_cbc7` | timeframe=1min, level=lon, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=12:30 | 71/0/216/0 | 287 | 13.0% | 2.4% | 0.78 | -2.7% | 170 | 1.36 | 3.5% | 137.8 | 8/8 | 1.00 | 0.55 | 0.23 | 5 | 4.6% | 0.62 | 0.70 | 12.1% | 11.2% | 9.6% | 12.4%/9.7% | 7.8 (interpolated) | pass | 0.011 (unverified) | -0.17 |
| 551 | `cfg_e627` | timeframe=1min, level=lon, side=both, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=2R, exit=12:30 | 26/0/99/67 | 192 | 11.2% | 2.1% | 0.78 | -2.7% | 347 | 1.33 | 2.4% | 92.1 | 9/9 | 1.00 | 0.61 | 0.17 | 5 | 4.1% | 0.61 | 0.52 | 10.7% | 10.2% | 8.6% | 10.5%/8.8% | 11.9 (interpolated) | pass | 0.017 (unverified) | 0.34 |
| 552 | `cfg_ecc0` | timeframe=1min, level=lon, side=high, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=range, exit=12:30 | 2/0/100/61 | 163 | 6.4% | 1.2% | 0.77 | -1.8% | 247 | 1.39 | 0.8% | 79.5 | 9/9 | 1.00 | 0.81 | -0.04 | 4 | 3.6% | 0.42 | 0.65 | 5.9% | 5.2% | 4.7% | 6.1%/4.5% | 7.4 (interpolated) | pass | 0.014 (unverified) | 0.26 |
| 553 | `cfg_dd13` | timeframe=1min, level=onh, side=low, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/21/103/0 | 124 | 13.5% | 2.5% | 0.79 | -3.1% | 389 | 1.81 | 2.3% | 60.3 | 9/9 | 1.00 | 0.68 | 0.11 | 4 | 8.4% | 0.38 | 0.92 | 12.9% | 12.5% | 8.1% | 12.3%/8.1% | 14.5 (interpolated) | pass | 0.005 (unverified) | -0.23 |
| 554 | `cfg_2c80` | timeframe=1min, level=box, side=low, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=16:00 | 0/78/143/0 | 221 | 21.4% | 3.9% | 0.81 | -4.7% | 354 | 1.44 | 7.3% | 106.5 | 6/6 | 0.83 | 0.62 | 0.19 | 3 | 10.1% | 0.53 | 0.68 | 19.3% | 18.6% | 9.4% | 19.1%/13.6% | 13.1 (interpolated) | pass | 0.013 (unverified) | -0.33 |
| 555 | `cfg_9aa6` | timeframe=1min, level=box, side=low, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=2R, exit=12:30 | 23/0/117/81 | 221 | 16.4% | 3.0% | 0.97 | -2.8% | 354 | 1.42 | 2.1% | 107.0 | 8/8 | 0.88 | 0.45 | 0.51 | 4 | 7.7% | 0.53 | 0.39 | 15.2% | 14.4% | 8.2% | 14.7%/10.6% | 12.1 (interpolated) | pass | 0.045 (unverified) | -0.43 |
| 556 | `cfg_9645` | timeframe=1min, level=pdr, side=high, window=30, pen=0.05, confirm=1, mode=cont, stop=struct, target=3R, exit=11:00 | 9/0/82/30 | 121 | 5.2% | 1.0% | 0.76 | -0.8% | 220 | 1.57 | 0.4% | 58.8 | 8/8 | 1.00 | 0.50 | 0.26 | 4 | 2.1% | 0.59 | 0.78 | 4.9% | 4.6% | 1.7% | 5.0%/3.7% | 7.9 (interpolated) | pass | 0.007 (unverified) | 0.45 |
| 557 | `cfg_f817` | timeframe=1min, level=asia, side=high, window=30, pen=0.05, confirm=5, mode=cont, stop=struct, target=1R, exit=11:00 | 6/0/52/69 | 127 | 5.3% | 1.0% | 0.76 | -1.9% | 194 | 1.47 | 0.4% | 61.7 | 7/7 | 1.00 | 0.61 | 0.16 | 4 | 2.6% | 0.50 | 0.68 | 4.8% | 4.5% | 4.6% | 4.6%/3.1% | 8.2 (interpolated) | pass | 0.018 (unverified) | -0.08 |
| 558 | `cfg_3055` | timeframe=1min, level=onh, side=high, window=30, pen=0.00, confirm=1, mode=cont, stop=struct, target=3R, exit=11:00 | 20/0/177/76 | 273 | 8.1% | 1.5% | 0.76 | -3.1% | 348 | 1.30 | 1.1% | 131.7 | 8/8 | 1.00 | 0.70 | 0.07 | 4 | 4.5% | 0.43 | 0.59 | 7.3% | 6.4% | 7.8% | 7.6%/5.4% | 5.6 (interpolated) | pass | 0.018 (unverified) | 0.63 |
| 559 | `cfg_7b7c` | timeframe=1min, level=box, side=high, window=30, pen=0.05, confirm=3, mode=fade, stop=d0.20, target=1R, exit=11:00 | 11/0/79/109 | 199 | 9.4% | 1.8% | 0.88 | -2.5% | 752 | 1.38 | 0.8% | 95.3 | 8/8 | 1.00 | 0.60 | 0.28 | 3 | 2.9% | 0.69 | 0.37 | 8.8% | 8.2% | 8.3% | 8.5%/6.6% | 9.4 (interpolated) | pass | 0.038 (unverified) | 0.08 |
| 560 | `cfg_3a57` | timeframe=1min, level=asia, side=both, window=30, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=3R, exit=12:30 | 1/0/106/52 | 159 | 7.8% | 1.5% | 0.82 | -2.0% | 191 | 1.47 | 0.6% | 76.9 | 11/11 | 1.00 | 0.51 | 0.30 | 4 | 3.2% | 0.57 | 0.68 | 7.3% | 6.8% | 3.0% | 6.9%/5.1% | 8.3 (interpolated) | pass | 0.013 (unverified) | -0.02 |
| 561 | `cfg_5fa7` | timeframe=1min, level=lon, side=high, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=2R, exit=12:30 | 0/0/57/46 | 103 | 4.5% | 0.9% | 0.77 | -1.5% | 501 | 1.48 | 0.3% | 50.6 | 10/10 | 1.00 | 0.62 | 0.15 | 4 | 2.0% | 0.55 | 0.59 | 4.2% | 3.9% | 2.1% | 4.2%/3.4% | 8.4 (interpolated) | pass | 0.016 (unverified) | 0.27 |
| 562 | `cfg_6000` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=5, mode=cont, stop=d0.10, target=3R, exit=12:30 | 2/0/68/37 | 107 | 7.0% | 1.3% | 0.89 | -1.8% | 177 | 1.62 | 0.6% | 51.4 | 10/10 | 1.00 | 0.66 | 0.23 | 5 | 4.1% | 0.41 | 0.57 | 6.5% | 6.2% | 6.4% | 6.2%/4.7% | 11.8 (interpolated) | pass | 0.022 (unverified) | 0.52 |
| 563 | `cfg_2ce2` | timeframe=1min, level=box, side=low, window=15, pen=0.00, confirm=3, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/38/153/0 | 191 | 14.7% | 2.7% | 0.80 | -3.1% | 170 | 1.57 | 3.8% | 91.9 | 8/8 | 0.88 | 0.65 | 0.15 | 5 | 9.3% | 0.36 | 0.83 | 14.1% | 13.5% | 8.7% | 13.8%/8.8% | 10.5 (interpolated) | pass | 0.008 (unverified) | -0.49 |
| 564 | `cfg_edd6` | timeframe=1min, level=lon, side=high, window=30, pen=0.00, confirm=1, mode=fade, stop=d0.20, target=1R, exit=12:30 | 3/0/72/88 | 163 | 7.0% | 1.3% | 0.75 | -2.7% | 460 | 1.34 | 0.9% | 80.5 | 8/8 | 0.88 | 0.50 | 0.25 | 3 | 3.1% | 0.56 | 0.49 | 6.5% | 6.0% | 3.9% | 6.0%/4.5% | 8.2 (interpolated) | pass | 0.017 (unverified) | -0.12 |
| 565 | `cfg_3566` | timeframe=1min, level=asia, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=3R, exit=11:00 | 9/0/131/58 | 198 | 8.3% | 1.6% | 0.82 | -1.9% | 381 | 1.41 | 0.8% | 96.4 | 9/9 | 1.00 | 0.47 | 0.35 | 5 | 5.3% | 0.35 | 0.64 | 7.6% | 6.8% | 0.6% | 7.7%/5.9% | 7.3 (interpolated) | pass | 0.015 (unverified) | -0.34 |
| 566 | `cfg_4bf0` | timeframe=1min, level=box, side=low, window=15, pen=0.05, confirm=5, mode=cont, stop=struct, target=3R, exit=16:00 | 0/18/155/63 | 236 | 13.0% | 2.4% | 0.77 | -2.7% | 244 | 1.34 | 3.1% | 113.6 | 7/7 | 0.57 | 0.49 | 0.27 | 4 | 6.3% | 0.49 | 0.64 | 11.1% | 10.2% | 9.6% | 11.2%/7.9% | 8.6 (interpolated) | pass | 0.013 (unverified) | -0.40 |
| 567 | `cfg_d710` | timeframe=1min, level=asia, side=high, window=60, pen=0.05, confirm=5, mode=fade, stop=d0.20, target=none, exit=16:00 | 0/34/86/0 | 120 | 18.7% | 3.4% | 0.75 | -3.9% | 327 | 1.72 | 3.4% | 58.3 | 6/6 | 1.00 | 0.31 | 0.45 | 3 | 9.3% | 0.50 | 0.99 | 18.3% | 17.8% | 17.7% | 16.8%/11.6% | 19.1 (interpolated) | pass | 0.007 (unverified) | -0.16 |
| 568 | `cfg_5d59` | timeframe=1min, level=onh, side=both, window=15, pen=0.05, confirm=5, mode=cont, stop=struct, target=2R, exit=16:00 | 0/11/151/94 | 256 | 12.1% | 2.3% | 0.84 | -2.8% | 241 | 1.36 | 2.4% | 124.2 | 7/7 | 1.00 | 0.62 | 0.23 | 5 | 5.9% | 0.51 | 0.53 | 11.2% | 10.1% | 10.8% | 10.8%/8.1% | 8.8 (interpolated) | pass | 0.023 (unverified) | 0.26 |
| 569 | `cfg_1ff1` | timeframe=1min, level=lon, side=both, window=60, pen=0.05, confirm=3, mode=fade, stop=d0.10, target=range, exit=16:00 | 0/0/134/61 | 195 | 8.2% | 1.5% | 0.75 | -2.6% | 384 | 1.41 | 0.7% | 94.2 | 9/9 | 0.89 | 0.58 | 0.17 | 4 | 4.7% | 0.41 | 0.75 | 7.5% | 7.0% | 3.0% | 7.5%/5.6% | 7.9 (interpolated) | pass | 0.009 (unverified) | 0.20 |
| 570 | `cfg_0a52` | timeframe=1min, level=asia, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=3R, exit=12:30 | 2/0/133/63 | 198 | 8.5% | 1.6% | 0.83 | -1.9% | 381 | 1.41 | 0.8% | 96.5 | 10/10 | 1.00 | 0.53 | 0.29 | 5 | 5.4% | 0.35 | 0.62 | 7.8% | 7.1% | 1.1% | 7.6%/6.0% | 7.6 (interpolated) | pass | 0.016 (unverified) | -0.46 |
| 571 | `cfg_93b1` | timeframe=1min, level=lon, side=low, window=60, pen=0.05, confirm=5, mode=fade, stop=d0.10, target=none, exit=12:30 | 38/0/120/0 | 158 | 9.6% | 1.8% | 0.76 | -2.9% | 388 | 1.53 | 1.7% | 77.7 | 8/8 | 1.00 | 0.52 | 0.24 | 4 | 3.7% | 0.59 | 0.87 | 9.1% | 8.7% | 2.9% | 9.1%/6.8% | 9.3 (interpolated) | pass | 0.007 (unverified) | -0.39 |
| 572 | `cfg_7cc8` | timeframe=1min, level=box, side=low, window=15, pen=0.05, confirm=5, mode=cont, stop=struct, target=3R, exit=12:30 | 31/0/147/58 | 236 | 13.5% | 2.5% | 0.85 | -2.7% | 185 | 1.38 | 2.1% | 113.7 | 8/8 | 0.88 | 0.47 | 0.38 | 5 | 8.3% | 0.36 | 0.57 | 12.7% | 11.5% | 9.5% | 11.9%/9.0% | 9.2 (interpolated) | pass | 0.022 (unverified) | -0.53 |
| 573 | `cfg_d88f` | timeframe=1min, level=lon, side=both, window=15, pen=0.00, confirm=1, mode=cont, stop=d0.10, target=none, exit=16:00 | 0/55/232/0 | 287 | 15.6% | 2.9% | 0.78 | -3.8% | 169 | 1.40 | 6.2% | 138.7 | 7/7 | 1.00 | 0.47 | 0.31 | 5 | 8.1% | 0.45 | 0.73 | 14.5% | 12.6% | 11.2% | 13.7%/10.5% | 8.5 (interpolated) | pass | 0.010 (unverified) | -0.30 |
| 574 | `cfg_6999` | timeframe=1min, level=lon, side=both, window=60, pen=0.05, confirm=3, mode=fade, stop=d0.10, target=3R, exit=11:00 | 8/0/132/55 | 195 | 7.7% | 1.5% | 0.80 | -2.5% | 344 | 1.40 | 0.6% | 94.4 | 9/9 | 1.00 | 0.54 | 0.26 | 4 | 3.6% | 0.51 | 0.59 | 7.1% | 6.6% | 2.0% | 6.9%/5.3% | 7.3 (interpolated) | pass | 0.015 (unverified) | 0.37 |
| 575 | `cfg_eded` | timeframe=1min, level=box, side=high, window=15, pen=0.05, confirm=3, mode=fade, stop=d0.20, target=2R, exit=11:00 | 37/0/89/54 | 180 | 10.5% | 2.0% | 0.76 | -2.4% | 468 | 1.36 | 1.3% | 86.0 | 8/8 | 0.88 | 0.45 | 0.32 | 3 | 3.7% | 0.63 | 0.58 | 9.6% | 9.1% | 10.2% | 9.3%/7.5% | 10.5 (interpolated) | pass | 0.015 (unverified) | 0.40 |
| 576 | `cfg_9af6` | timeframe=1min, level=lon, side=both, window=15, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=2R, exit=12:30 | 20/0/75/52 | 147 | 9.3% | 1.7% | 0.75 | -2.0% | 242 | 1.39 | 1.9% | 70.0 | 8/8 | 1.00 | 0.52 | 0.23 | 5 | 4.7% | 0.47 | 0.62 | 8.8% | 8.4% | 6.3% | 8.5%/6.0% | 11.5 (interpolated) | pass | 0.014 (unverified) | -0.20 |
| 577 | `cfg_76a4` | timeframe=1min, level=box, side=low, window=60, pen=0.00, confirm=5, mode=cont, stop=d0.20, target=none, exit=12:30 | 96/0/125/0 | 221 | 17.8% | 3.2% | 0.86 | -2.9% | 354 | 1.44 | 3.8% | 106.5 | 7/7 | 0.86 | 0.58 | 0.28 | 5 | 5.2% | 0.71 | 0.61 | 16.8% | 14.9% | 8.4% | 15.0%/11.1% | 11.4 (interpolated) | pass | 0.019 (unverified) | -0.36 |
| 578 | `cfg_dd21` | timeframe=1min, level=box, side=both, window=15, pen=0.00, confirm=3, mode=cont, stop=struct, target=2R, exit=16:00 | 0/10/256/161 | 427 | 15.1% | 2.8% | 0.79 | -4.4% | 219 | 1.23 | 3.7% | 207.3 | 8/8 | 0.62 | 0.53 | 0.27 | 4 | 9.3% | 0.37 | 0.48 | 13.0% | 10.9% | 12.7% | 13.5%/9.4% | 6.4 (interpolated) | pass | 0.019 (unverified) | -0.08 |
| 579 | `cfg_7ecf` | timeframe=1min, level=asia, side=both, window=15, pen=0.05, confirm=3, mode=cont, stop=d0.10, target=none, exit=11:00 | 55/0/143/0 | 198 | 10.2% | 1.9% | 0.79 | -2.2% | 221 | 1.46 | 1.3% | 95.9 | 8/8 | 1.00 | 0.60 | 0.19 | 4 | 5.4% | 0.46 | 0.74 | 9.2% | 8.5% | 4.0% | 9.5%/7.1% | 8.2 (interpolated) | pass | 0.010 (unverified) | -0.09 |
| 580 | `cfg_6faf` | timeframe=1min, level=box, side=low, window=15, pen=0.00, confirm=5, mode=cont, stop=struct, target=2R, exit=16:00 | 0/3/84/59 | 146 | 9.8% | 1.8% | 0.75 | -4.9% | 422 | 1.41 | 1.6% | 70.0 | 7/7 | 1.00 | 0.51 | 0.25 | 4 | 4.7% | 0.50 | 0.72 | 8.9% | 8.6% | 4.1% | 8.0%/5.7% | 10.6 (interpolated) | pass | 0.012 (unverified) | -0.28 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 3.3% / 0.48 / 152 | 17.2% / 2.65 / 158 | 1.1% / 0.18 / 156 | 11.8% / 1.94 / 153 | 29.4% / 2.35 / 155 |
| 2 | 2.8% / 1.02 / 35 | 1.0% / 0.35 / 43 | 8.1% / 1.97 / 28 | 7.9% / 2.12 / 48 | 12.5% / 2.16 / 39 |
| 3 | 2.6% / 0.41 / 130 | 15.0% / 2.45 / 138 | 2.6% / 0.37 / 142 | 12.5% / 2.05 / 139 | 25.4% / 2.22 / 129 |
| 4 | 2.8% / 1.00 / 35 | -0.3% / -0.11 / 43 | 8.5% / 2.05 / 28 | 6.9% / 2.16 / 48 | 10.7% / 2.15 / 39 |
| 5 | 6.2% / 1.08 / 85 | 4.7% / 1.31 / 74 | 5.6% / 0.98 / 61 | 9.8% / 1.98 / 87 | 13.1% / 1.73 / 79 |
| 6 | 3.1% / 0.76 / 75 | 3.8% / 0.92 / 79 | 4.3% / 0.94 / 56 | 11.0% / 2.60 / 71 | 14.1% / 1.88 / 88 |
| 7 | 1.6% / 0.70 / 35 | -0.5% / -0.23 / 42 | 8.4% / 2.03 / 28 | 5.5% / 1.90 / 48 | 9.9% / 2.28 / 39 |
| 8 | -0.1% / 0.01 / 75 | 3.6% / 0.82 / 79 | 4.5% / 0.72 / 56 | 15.9% / 2.93 / 71 | 21.5% / 2.17 / 88 |
| 9 | 0.9% / 0.29 / 62 | 5.3% / 1.41 / 65 | 6.8% / 1.71 / 56 | 8.6% / 2.60 / 56 | 6.7% / 1.34 / 57 |
| 10 | 3.3% / 1.01 / 60 | 5.6% / 1.40 / 68 | 8.2% / 1.31 / 77 | 7.5% / 1.69 / 77 | 11.0% / 1.77 / 58 |
| 11 | 0.2% / 0.07 / 75 | 3.1% / 0.89 / 79 | 6.5% / 1.16 / 56 | 8.2% / 2.16 / 71 | 23.3% / 2.57 / 88 |
| 12 | -2.5% / -0.64 / 62 | 7.1% / 1.61 / 65 | 10.2% / 1.69 / 56 | 10.5% / 2.78 / 56 | 12.4% / 1.79 / 57 |
| 13 | 1.4% / 0.55 / 60 | 6.7% / 1.85 / 68 | 5.3% / 1.08 / 77 | 5.4% / 1.49 / 77 | 10.8% / 1.87 / 58 |
| 14 | 4.1% / 1.02 / 78 | 10.8% / 2.35 / 85 | 5.5% / 0.93 / 93 | 7.5% / 1.58 / 92 | 8.1% / 1.26 / 79 |
| 15 | 0.4% / 0.13 / 50 | 1.5% / 0.44 / 57 | 3.0% / 0.57 / 40 | 12.6% / 2.63 / 55 | 25.0% / 2.87 / 54 |
| 16 | 4.7% / 0.97 / 95 | 17.4% / 2.82 / 95 | 2.8% / 0.54 / 90 | 5.3% / 1.42 / 95 | 12.5% / 1.39 / 85 |
| 17 | 5.4% / 0.90 / 104 | 7.3% / 1.66 / 94 | 5.9% / 0.97 / 80 | 7.8% / 1.60 / 107 | 14.2% / 1.76 / 96 |
| 18 | 1.4% / 0.43 / 50 | 2.0% / 0.61 / 57 | 4.4% / 1.08 / 40 | 9.8% / 2.48 / 55 | 17.0% / 2.61 / 54 |
| 19 | 4.1% / 1.16 / 52 | 1.5% / 0.48 / 48 | 5.9% / 1.28 / 37 | 6.8% / 1.72 / 56 | 12.0% / 1.95 / 53 |
| 20 | 0.3% / 0.11 / 62 | 4.5% / 1.34 / 65 | 6.5% / 1.67 / 56 | 8.6% / 2.61 / 56 | 6.6% / 1.36 / 57 |
| 21 | 3.2% / 0.78 / 85 | 5.8% / 1.59 / 74 | 5.8% / 1.28 / 61 | 7.5% / 1.79 / 87 | 8.2% / 1.37 / 79 |
| 22 | 4.4% / 0.59 / 152 | 10.1% / 1.51 / 158 | 0.5% / 0.10 / 156 | 17.7% / 2.52 / 153 | 32.2% / 2.29 / 155 |
| 23 | 3.1% / 0.74 / 52 | 3.5% / 1.09 / 48 | 6.3% / 1.08 / 37 | 8.0% / 1.80 / 56 | 11.6% / 1.68 / 53 |
| 24 | 2.7% / 0.62 / 69 | 4.8% / 1.43 / 68 | 3.4% / 0.62 / 50 | 8.5% / 1.88 / 72 | 14.9% / 2.00 / 73 |
| 25 | 3.6% / 0.90 / 77 | 7.6% / 1.67 / 81 | 8.8% / 1.35 / 75 | 4.9% / 1.48 / 78 | 9.9% / 1.62 / 63 |
| 26 | 4.5% / 1.01 / 85 | 2.2% / 0.69 / 74 | 1.7% / 0.38 / 61 | 10.1% / 2.07 / 87 | 16.1% / 2.03 / 79 |
| 27 | 3.5% / 0.75 / 61 | 4.8% / 1.27 / 57 | 7.3% / 1.19 / 51 | 6.1% / 1.40 / 67 | 14.8% / 1.91 / 60 |
| 28 | 1.7% / 0.50 / 50 | 3.6% / 1.19 / 57 | 4.0% / 0.77 / 40 | 7.5% / 1.79 / 55 | 18.0% / 2.43 / 54 |
| 29 | 3.4% / 0.70 / 104 | 4.2% / 1.07 / 94 | 3.9% / 0.77 / 80 | 8.3% / 1.71 / 107 | 18.9% / 2.14 / 96 |
| 30 | -3.1% / -0.79 / 77 | 12.7% / 2.58 / 81 | 5.6% / 0.89 / 75 | 8.9% / 2.06 / 78 | 16.4% / 1.99 / 63 |
| 31 | 5.9% / 1.68 / 77 | 6.3% / 1.66 / 81 | 4.5% / 1.00 / 75 | 3.8% / 1.38 / 78 | 6.1% / 1.33 / 63 |
| 32 | 6.1% / 1.26 / 86 | 14.8% / 2.59 / 86 | 0.1% / 0.05 / 82 | 6.4% / 1.69 / 83 | 10.4% / 1.30 / 74 |
| 33 | 9.5% / 1.27 / 145 | 13.6% / 2.26 / 133 | -0.9% / -0.12 / 149 | 9.3% / 1.79 / 142 | 13.3% / 1.33 / 128 |
| 34 | 1.8% / 0.53 / 85 | 4.1% / 1.45 / 74 | 6.5% / 1.34 / 61 | 5.8% / 1.53 / 87 | 8.5% / 1.56 / 79 |
| 35 | 3.4% / 0.93 / 35 | 0.5% / 0.18 / 43 | 8.1% / 1.45 / 28 | 7.5% / 1.83 / 48 | 16.1% / 2.25 / 39 |
| 36 | 0.2% / 0.07 / 98 | 13.9% / 2.29 / 89 | 7.3% / 0.97 / 86 | 7.3% / 1.56 / 96 | 17.8% / 1.85 / 78 |
| 37 | 3.9% / 0.55 / 171 | 17.7% / 2.52 / 160 | 2.9% / 0.42 / 168 | 10.5% / 1.82 / 164 | 16.4% / 1.51 / 158 |
| 38 | -0.4% / -0.14 / 62 | 4.8% / 1.34 / 65 | 8.0% / 1.46 / 56 | 6.8% / 2.15 / 56 | 9.7% / 1.69 / 57 |
| 39 | 5.9% / 0.82 / 145 | 14.2% / 2.27 / 133 | 1.3% / 0.21 / 149 | 11.7% / 2.03 / 142 | 12.2% / 1.23 / 128 |
| 40 | 0.9% / 0.32 / 52 | 3.0% / 1.10 / 48 | 6.6% / 1.62 / 37 | 7.2% / 1.97 / 56 | 6.6% / 1.32 / 53 |
| 41 | 1.2% / 0.35 / 52 | 2.9% / 1.02 / 48 | 7.7% / 1.40 / 37 | 8.1% / 1.99 / 56 | 10.0% / 1.61 / 53 |
| 42 | 5.9% / 1.54 / 86 | 13.1% / 2.54 / 86 | 1.7% / 0.42 / 82 | 5.3% / 1.65 / 83 | 2.2% / 0.46 / 74 |
| 43 | -1.7% / -0.43 / 98 | 12.8% / 2.50 / 89 | 10.2% / 1.46 / 86 | 5.6% / 1.56 / 96 | 9.3% / 1.39 / 78 |
| 44 | -4.0% / -1.08 / 98 | 15.7% / 2.95 / 89 | 3.3% / 0.55 / 86 | 9.1% / 2.03 / 96 | 13.5% / 1.63 / 78 |
| 45 | 7.8% / 1.06 / 161 | 16.8% / 2.51 / 151 | -0.1% / 0.01 / 158 | 9.2% / 1.76 / 156 | 14.3% / 1.39 / 146 |
| 46 | 1.2% / 0.27 / 145 | 13.7% / 2.38 / 133 | 4.7% / 0.77 / 149 | 9.4% / 1.85 / 142 | 6.5% / 0.95 / 128 |
| 47 | 2.2% / 0.66 / 60 | 7.4% / 1.88 / 68 | 6.5% / 1.12 / 77 | 6.6% / 1.42 / 77 | 7.4% / 1.23 / 58 |
| 48 | 5.6% / 0.96 / 152 | 7.6% / 1.44 / 158 | 1.4% / 0.23 / 156 | 8.7% / 1.72 / 153 | 21.6% / 2.08 / 155 |
| 49 | 2.0% / 0.58 / 85 | 3.8% / 1.42 / 74 | 5.7% / 1.34 / 61 | 5.2% / 1.55 / 87 | 6.6% / 1.42 / 79 |
| 50 | 6.9% / 1.12 / 78 | 11.4% / 2.19 / 85 | 2.6% / 0.39 / 93 | 10.1% / 1.89 / 92 | 13.3% / 1.43 / 79 |
| 51 | 5.7% / 1.40 / 78 | 8.8% / 1.84 / 85 | 5.4% / 0.82 / 93 | 6.5% / 1.38 / 92 | 9.3% / 1.37 / 79 |
| 52 | -2.2% / -0.51 / 127 | 17.5% / 2.85 / 124 | 4.6% / 0.76 / 121 | 4.9% / 1.16 / 136 | 12.4% / 1.60 / 102 |
| 53 | 2.6% / 0.39 / 130 | 7.6% / 1.23 / 138 | 0.4% / 0.09 / 142 | 18.5% / 2.63 / 139 | 30.2% / 2.31 / 129 |
| 54 | 0.4% / 0.18 / 47 | 2.8% / 0.94 / 50 | 6.7% / 1.81 / 38 | 5.9% / 1.95 / 54 | 7.6% / 1.64 / 47 |
| 55 | 0.8% / 0.22 / 96 | 9.4% / 2.23 / 110 | 3.9% / 0.68 / 114 | 8.7% / 1.58 / 114 | 12.5% / 1.79 / 98 |
| 56 | 11.1% / 1.35 / 126 | 9.5% / 1.52 / 135 | -4.4% / -0.47 / 139 | 11.9% / 1.82 / 139 | 30.2% / 2.19 / 133 |
| 57 | -4.6% / -1.76 / 74 | 8.0% / 1.97 / 71 | 11.4% / 1.91 / 66 | 6.5% / 1.96 / 69 | 9.4% / 1.56 / 66 |
| 58 | 4.5% / 0.85 / 130 | 5.7% / 1.17 / 138 | 3.2% / 0.47 / 142 | 9.1% / 1.80 / 139 | 22.0% / 2.22 / 129 |
| 59 | 7.3% / 1.25 / 126 | 10.1% / 1.79 / 135 | -2.2% / -0.26 / 139 | 11.6% / 1.88 / 139 | 16.6% / 1.78 / 133 |
| 60 | 0.1% / 0.04 / 126 | 10.0% / 1.85 / 135 | 0.3% / 0.08 / 139 | 10.2% / 1.88 / 139 | 18.2% / 1.91 / 133 |
| 61 | 3.2% / 0.75 / 96 | 4.4% / 1.05 / 110 | 1.0% / 0.19 / 114 | 9.6% / 1.94 / 114 | 15.1% / 1.84 / 98 |
| 62 | 1.8% / 0.44 / 75 | 2.5% / 0.75 / 79 | 3.1% / 0.58 / 56 | 8.6% / 1.94 / 71 | 18.9% / 2.28 / 88 |
| 63 | 2.3% / 0.49 / 93 | 3.9% / 1.07 / 90 | 1.7% / 0.33 / 73 | 8.4% / 1.79 / 90 | 18.0% / 2.12 / 105 |
| 64 | -0.8% / -0.20 / 69 | 3.6% / 1.13 / 68 | 3.3% / 0.66 / 50 | 8.6% / 2.08 / 72 | 17.9% / 2.24 / 73 |
| 65 | 3.7% / 0.97 / 85 | 3.9% / 1.14 / 74 | 2.3% / 0.58 / 61 | 7.7% / 1.96 / 87 | 9.0% / 1.48 / 79 |
| 66 | 1.6% / 0.83 / 35 | 2.6% / 1.51 / 36 | 4.8% / 2.11 / 41 | 1.9% / 1.27 / 41 | 2.3% / 0.91 / 41 |
| 67 | 5.2% / 0.97 / 60 | 5.7% / 1.22 / 68 | 6.0% / 0.82 / 77 | 9.6% / 1.93 / 77 | 15.1% / 1.75 / 58 |
| 68 | 0.6% / 0.15 / 130 | 12.4% / 2.42 / 138 | 3.5% / 0.58 / 142 | 8.3% / 1.49 / 139 | 15.1% / 1.90 / 129 |
| 69 | 0.7% / 0.35 / 35 | 1.6% / 0.59 / 43 | 6.6% / 1.96 / 28 | 6.0% / 2.05 / 48 | 7.9% / 1.79 / 39 |
| 70 | 4.4% / 0.81 / 60 | 7.7% / 1.67 / 68 | 3.2% / 0.49 / 77 | 9.3% / 1.80 / 77 | 12.0% / 1.45 / 58 |
| 71 | 4.6% / 1.29 / 60 | 3.4% / 0.97 / 68 | 7.2% / 1.25 / 77 | 6.3% / 1.75 / 77 | 8.2% / 1.51 / 58 |
| 72 | 4.5% / 1.16 / 95 | 14.9% / 2.73 / 95 | 3.6% / 0.77 / 90 | 4.3% / 1.33 / 95 | 3.2% / 0.61 / 85 |
| 73 | 2.6% / 0.61 / 98 | 12.1% / 2.31 / 89 | 4.5% / 0.80 / 86 | 6.7% / 1.61 / 96 | 6.7% / 1.11 / 78 |
| 74 | 1.4% / 0.38 / 61 | 2.0% / 0.71 / 57 | 8.9% / 1.54 / 51 | 7.1% / 1.75 / 67 | 13.5% / 1.91 / 60 |
| 75 | 4.3% / 0.69 / 85 | -0.8% / -0.19 / 74 | 2.6% / 0.42 / 61 | 10.0% / 1.91 / 87 | 14.6% / 1.62 / 79 |
| 76 | 0.6% / 0.18 / 75 | 3.1% / 0.94 / 79 | 3.3% / 0.92 / 56 | 5.6% / 1.81 / 71 | 14.9% / 2.21 / 88 |
| 77 | 0.2% / 0.07 / 62 | 4.6% / 1.43 / 65 | 5.4% / 1.51 / 56 | 5.3% / 2.02 / 56 | 5.6% / 1.33 / 57 |
| 78 | 0.5% / 0.18 / 60 | 6.9% / 1.63 / 68 | 3.9% / 0.66 / 77 | 7.4% / 1.78 / 77 | 15.0% / 1.88 / 58 |
| 79 | 3.6% / 0.80 / 52 | 1.5% / 0.46 / 48 | 6.0% / 1.01 / 37 | 7.0% / 1.56 / 56 | 14.2% / 1.82 / 53 |
| 80 | 0.3% / 0.08 / 101 | 4.8% / 1.20 / 101 | 5.6% / 0.95 / 88 | 7.4% / 1.86 / 92 | 19.6% / 2.18 / 109 |
| 81 | -0.7% / -0.11 / 161 | 16.1% / 2.61 / 151 | 6.0% / 0.93 / 158 | 10.6% / 2.03 / 156 | 6.2% / 0.83 / 146 |
| 82 | 1.5% / 0.68 / 44 | 5.2% / 1.64 / 47 | 5.2% / 1.38 / 43 | 3.6% / 1.45 / 52 | 5.2% / 1.30 / 38 |
| 83 | 1.6% / 0.67 / 35 | -1.1% / -0.46 / 42 | 10.0% / 1.97 / 28 | 4.0% / 1.30 / 48 | 7.8% / 1.75 / 39 |
| 84 | 1.2% / 0.32 / 93 | 4.7% / 1.25 / 90 | 3.0% / 0.78 / 73 | 7.5% / 1.88 / 90 | 13.1% / 1.92 / 105 |
| 85 | 2.1% / 0.83 / 52 | 1.8% / 0.60 / 48 | 5.7% / 1.53 / 37 | 5.7% / 1.77 / 56 | 6.6% / 1.40 / 53 |
| 86 | -0.9% / -0.14 / 113 | 15.9% / 2.55 / 104 | 4.1% / 0.56 / 106 | 8.8% / 1.76 / 111 | 17.1% / 1.66 / 94 |
| 87 | -4.0% / -1.17 / 62 | 4.5% / 1.25 / 65 | 8.5% / 1.54 / 56 | 10.8% / 2.78 / 56 | 9.9% / 1.62 / 57 |
| 88 | -0.5% / -0.20 / 44 | 5.6% / 1.54 / 47 | 7.1% / 1.35 / 43 | 4.2% / 1.47 / 52 | 12.5% / 1.72 / 38 |
| 89 | 3.3% / 0.83 / 61 | 0.8% / 0.26 / 57 | 6.6% / 1.30 / 51 | 5.3% / 1.32 / 67 | 12.1% / 1.95 / 60 |
| 90 | -0.8% / -0.15 / 121 | 6.4% / 1.46 / 118 | 7.7% / 1.22 / 105 | 7.5% / 1.63 / 116 | 18.8% / 2.06 / 124 |
| 91 | 0.4% / 0.11 / 132 | 9.3% / 1.92 / 116 | 2.3% / 0.45 / 105 | 5.1% / 1.08 / 131 | 22.5% / 2.19 / 143 |
| 92 | 2.3% / 0.56 / 78 | 10.9% / 2.22 / 85 | 7.0% / 1.01 / 93 | 9.1% / 1.99 / 92 | 4.7% / 0.82 / 79 |
| 93 | -4.9% / -1.85 / 89 | 12.2% / 2.64 / 87 | 6.8% / 1.36 / 83 | 5.2% / 1.42 / 97 | 8.3% / 1.29 / 81 |
| 94 | 0.4% / 0.15 / 73 | 6.8% / 1.82 / 79 | 3.6% / 0.76 / 91 | 6.1% / 1.58 / 95 | 11.5% / 1.90 / 69 |
| 95 | -0.1% / -0.05 / 53 | 6.6% / 1.95 / 56 | 2.9% / 0.95 / 46 | 5.6% / 1.82 / 65 | 5.7% / 1.25 / 53 |
| 96 | 0.1% / 0.06 / 33 | 2.9% / 1.04 / 38 | 5.1% / 1.45 / 28 | 5.4% / 1.96 / 39 | 5.8% / 1.45 / 30 |
| 97 | -0.0% / 0.02 / 104 | 5.8% / 1.70 / 94 | 7.5% / 1.41 / 80 | 4.7% / 1.22 / 107 | 7.8% / 1.38 / 96 |
| 98 | 2.6% / 0.78 / 78 | 10.5% / 2.39 / 85 | 6.4% / 1.14 / 93 | 6.9% / 1.70 / 92 | 4.1% / 0.77 / 79 |
| 99 | -3.3% / -1.35 / 74 | 7.5% / 2.06 / 71 | 7.0% / 1.84 / 66 | 6.0% / 2.00 / 69 | 4.5% / 1.04 / 66 |
| 100 | 3.1% / 0.87 / 96 | 4.2% / 1.18 / 110 | 0.9% / 0.21 / 114 | 7.1% / 1.63 / 114 | 10.8% / 1.61 / 98 |
| 101 | 1.3% / 0.61 / 52 | 3.3% / 1.24 / 48 | 5.6% / 1.56 / 37 | 5.9% / 1.96 / 56 | 3.2% / 0.82 / 53 |
| 102 | 0.6% / 0.12 / 180 | 10.8% / 1.80 / 184 | 2.2% / 0.31 / 183 | 8.4% / 1.51 / 181 | 25.8% / 2.28 / 180 |
| 103 | 2.6% / 0.74 / 52 | 3.2% / 1.08 / 48 | 5.0% / 1.24 / 37 | 5.4% / 1.43 / 56 | 7.1% / 1.30 / 53 |
| 104 | 0.1% / 0.08 / 48 | 5.2% / 1.65 / 47 | 0.5% / 0.19 / 35 | 5.9% / 2.03 / 54 | 7.1% / 1.60 / 40 |
| 105 | -0.6% / -0.17 / 69 | 3.6% / 1.17 / 68 | 1.3% / 0.40 / 50 | 6.9% / 1.92 / 72 | 13.1% / 2.11 / 73 |
| 106 | 2.3% / 0.62 / 73 | 4.2% / 1.14 / 79 | 6.4% / 1.07 / 91 | 9.0% / 2.21 / 95 | 7.8% / 1.37 / 69 |
| 107 | -1.0% / -0.50 / 33 | 2.7% / 1.08 / 38 | 6.3% / 1.37 / 28 | 3.3% / 1.39 / 39 | 9.6% / 1.95 / 30 |
| 108 | -0.2% / -0.08 / 62 | 4.1% / 1.45 / 64 | 5.5% / 1.55 / 56 | 4.6% / 1.91 / 56 | 3.5% / 1.08 / 57 |
| 109 | 5.4% / 0.65 / 162 | 10.5% / 1.51 / 162 | -1.9% / -0.15 / 168 | 10.8% / 1.56 / 167 | 31.6% / 2.24 / 157 |
| 110 | -0.8% / -0.43 / 26 | 2.3% / 0.87 / 34 | 6.1% / 1.73 / 22 | 4.9% / 1.82 / 34 | 6.1% / 1.53 / 28 |
| 111 | 3.1% / 0.69 / 85 | 1.6% / 0.43 / 74 | 4.2% / 0.83 / 61 | 9.7% / 2.03 / 87 | 9.1% / 1.27 / 79 |
| 112 | 3.1% / 0.76 / 98 | 9.2% / 2.03 / 89 | 3.6% / 0.66 / 86 | 5.9% / 1.52 / 96 | 8.2% / 1.28 / 78 |
| 113 | 2.0% / 0.49 / 79 | 5.0% / 1.18 / 88 | 1.4% / 0.26 / 95 | 8.6% / 1.93 / 98 | 17.1% / 1.97 / 83 |
| 114 | 4.0% / 1.00 / 77 | 6.5% / 1.44 / 81 | 4.1% / 0.78 / 75 | 7.0% / 1.83 / 78 | 6.7% / 1.21 / 63 |
| 115 | -0.4% / -0.03 / 121 | 5.4% / 1.04 / 118 | 7.8% / 1.04 / 105 | 7.4% / 1.34 / 116 | 15.6% / 1.50 / 124 |
| 116 | -2.6% / -0.54 / 89 | 10.2% / 2.00 / 87 | 12.2% / 1.76 / 83 | 9.5% / 2.02 / 97 | 4.8% / 0.65 / 81 |
| 117 | -1.0% / -0.39 / 53 | 5.9% / 1.69 / 56 | 3.2% / 0.87 / 46 | 6.1% / 1.71 / 65 | 10.7% / 1.78 / 53 |
| 118 | 0.0% / 0.03 / 33 | 2.3% / 0.95 / 38 | 5.1% / 1.42 / 28 | 4.9% / 1.85 / 39 | 5.5% / 1.45 / 30 |
| 119 | 2.0% / 0.43 / 69 | 2.0% / 0.53 / 68 | 0.6% / 0.13 / 50 | 11.1% / 2.11 / 72 | 16.4% / 1.84 / 73 |
| 120 | 4.0% / 0.66 / 79 | 5.3% / 1.05 / 88 | 3.5% / 0.49 / 95 | 13.6% / 2.38 / 98 | 18.8% / 1.80 / 83 |
| 121 | 3.5% / 1.04 / 85 | 1.0% / 0.40 / 74 | 1.9% / 0.49 / 61 | 4.9% / 1.51 / 87 | 9.0% / 1.70 / 79 |
| 122 | 0.7% / 0.21 / 73 | 6.7% / 1.55 / 79 | 7.4% / 1.14 / 91 | 9.6% / 1.98 / 95 | 10.4% / 1.62 / 69 |
| 123 | -0.5% / -0.28 / 22 | 0.9% / 0.42 / 30 | 4.3% / 1.34 / 16 | 4.3% / 1.73 / 31 | 7.4% / 1.99 / 23 |
| 124 | 1.6% / 0.31 / 130 | 6.2% / 1.21 / 138 | -1.7% / -0.21 / 142 | 14.2% / 2.35 / 139 | 19.5% / 2.05 / 129 |
| 125 | 1.9% / 0.40 / 161 | 15.2% / 2.49 / 151 | 4.6% / 0.73 / 158 | 6.9% / 1.50 / 156 | 5.6% / 0.80 / 146 |
| 126 | 1.2% / 0.40 / 50 | 3.1% / 1.09 / 57 | 3.2% / 0.84 / 40 | 3.2% / 1.02 / 55 | 13.5% / 2.27 / 54 |
| 127 | 0.3% / 0.16 / 38 | 4.7% / 1.49 / 45 | 3.6% / 1.05 / 38 | 3.3% / 1.39 / 42 | 5.3% / 1.38 / 32 |
| 128 | -3.5% / -1.39 / 89 | 12.0% / 2.88 / 87 | 6.5% / 1.65 / 83 | 3.6% / 1.21 / 97 | 4.2% / 0.87 / 81 |
| 129 | -0.1% / -0.01 / 47 | 5.3% / 1.40 / 52 | 6.2% / 1.17 / 47 | 4.2% / 1.45 / 53 | 11.5% / 1.58 / 43 |
| 130 | 0.7% / 0.52 / 28 | 1.9% / 1.49 / 35 | 1.3% / 0.84 / 31 | 1.2% / 1.12 / 35 | 3.4% / 1.81 / 35 |
| 131 | 3.4% / 0.71 / 145 | 12.7% / 2.25 / 133 | 2.7% / 0.46 / 149 | 6.8% / 1.51 / 142 | 5.5% / 0.82 / 128 |
| 132 | 0.3% / 0.11 / 55 | 7.6% / 2.00 / 54 | 4.3% / 0.95 / 54 | 6.5% / 1.90 / 61 | 3.5% / 0.72 / 49 |
| 133 | -0.4% / -0.10 / 33 | 3.0% / 1.00 / 38 | 7.5% / 1.47 / 28 | 4.5% / 1.47 / 39 | 10.3% / 1.84 / 30 |
| 134 | 1.1% / 0.51 / 35 | 7.7% / 2.06 / 36 | 6.0% / 1.85 / 41 | 1.5% / 0.87 / 41 | 2.3% / 0.67 / 41 |
| 135 | -3.2% / -1.48 / 74 | 5.9% / 1.89 / 71 | 7.2% / 1.90 / 66 | 5.9% / 2.05 / 69 | 3.2% / 0.91 / 66 |
| 136 | 0.9% / 0.22 / 77 | 7.9% / 1.51 / 81 | 6.2% / 0.84 / 75 | 8.5% / 1.88 / 78 | 15.3% / 1.77 / 63 |
| 137 | 0.4% / 0.12 / 126 | 10.0% / 2.08 / 135 | -1.8% / -0.30 / 139 | 10.0% / 1.86 / 139 | 11.7% / 1.58 / 133 |
| 138 | -0.3% / -0.06 / 89 | 9.4% / 2.04 / 87 | 8.7% / 1.74 / 83 | 8.5% / 2.13 / 97 | 1.2% / 0.24 / 81 |
| 139 | 0.7% / 0.52 / 28 | 1.9% / 1.49 / 35 | 1.3% / 0.84 / 31 | 1.2% / 1.12 / 35 | 3.4% / 1.81 / 35 |
| 140 | 2.5% / 0.51 / 61 | 0.6% / 0.20 / 57 | 7.7% / 1.18 / 51 | 4.7% / 1.05 / 67 | 18.9% / 2.14 / 60 |
| 141 | -0.5% / -0.17 / 47 | 0.9% / 0.38 / 50 | 5.2% / 1.06 / 38 | 3.6% / 1.32 / 54 | 15.8% / 2.40 / 47 |
| 142 | 1.3% / 0.37 / 75 | 2.9% / 0.91 / 79 | 3.1% / 0.76 / 56 | 4.6% / 1.31 / 71 | 13.4% / 2.05 / 88 |
| 143 | -0.6% / -0.17 / 75 | 4.5% / 1.27 / 79 | 3.7% / 0.96 / 56 | 8.2% / 2.54 / 71 | 10.3% / 1.70 / 88 |
| 144 | 2.7% / 0.70 / 61 | 4.3% / 1.29 / 57 | 5.0% / 1.13 / 51 | 4.2% / 1.12 / 67 | 6.9% / 1.27 / 60 |
| 145 | 0.2% / 0.06 / 93 | 3.2% / 0.70 / 90 | 3.4% / 0.54 / 73 | 9.3% / 1.72 / 90 | 14.2% / 1.44 / 105 |
| 146 | -1.2% / -0.36 / 95 | 14.1% / 2.64 / 95 | 4.1% / 0.86 / 90 | 6.7% / 1.76 / 95 | 2.2% / 0.42 / 85 |
| 147 | -2.6% / -0.75 / 95 | 16.2% / 2.66 / 95 | 4.7% / 0.77 / 90 | 6.9% / 1.59 / 95 | 9.9% / 1.20 / 85 |
| 148 | 7.0% / 1.71 / 78 | 6.9% / 1.65 / 85 | 3.7% / 0.60 / 93 | 3.3% / 0.90 / 92 | 7.2% / 1.18 / 79 |
| 149 | 1.3% / 0.44 / 52 | 1.9% / 0.81 / 48 | 6.5% / 1.37 / 37 | 4.1% / 1.29 / 56 | 6.8% / 1.45 / 53 |
| 150 | 0.6% / 0.24 / 35 | 2.4% / 0.86 / 43 | 4.7% / 1.22 / 28 | 5.2% / 1.55 / 48 | 7.7% / 1.45 / 39 |
| 151 | 1.4% / 0.59 / 61 | 3.4% / 1.21 / 57 | 5.6% / 1.47 / 51 | 5.7% / 1.87 / 67 | 3.2% / 0.79 / 60 |
| 152 | 3.5% / 0.91 / 60 | 5.5% / 1.49 / 68 | 4.4% / 0.85 / 77 | 5.6% / 1.40 / 77 | 6.6% / 1.23 / 58 |
| 153 | 0.0% / 0.02 / 98 | 12.8% / 2.73 / 89 | 3.4% / 0.74 / 86 | 3.9% / 1.24 / 96 | 4.5% / 0.90 / 78 |
| 154 | -0.6% / -0.24 / 35 | 1.6% / 0.64 / 43 | 4.6% / 0.99 / 28 | 4.0% / 1.49 / 48 | 14.9% / 2.34 / 39 |
| 155 | -0.9% / -0.48 / 26 | 1.4% / 0.64 / 34 | 6.1% / 1.72 / 22 | 4.2% / 1.66 / 34 | 5.6% / 1.51 / 28 |
| 156 | -2.4% / -0.69 / 74 | 8.1% / 2.02 / 71 | 5.0% / 1.21 / 66 | 8.0% / 2.25 / 69 | 2.4% / 0.49 / 66 |
| 157 | 1.4% / 0.35 / 69 | 2.3% / 0.65 / 68 | 1.3% / 0.33 / 50 | 8.3% / 1.87 / 72 | 11.1% / 1.61 / 73 |
| 158 | -2.0% / -0.60 / 98 | 13.0% / 2.85 / 89 | 1.4% / 0.32 / 86 | 5.3% / 1.47 / 96 | 6.7% / 1.23 / 78 |
| 159 | -0.2% / -0.15 / 28 | 2.6% / 1.61 / 35 | 2.4% / 1.26 / 31 | 2.4% / 1.72 / 35 | 2.7% / 1.13 / 35 |
| 160 | 0.9% / 0.24 / 96 | 9.0% / 2.38 / 110 | 0.1% / 0.04 / 114 | 7.0% / 1.59 / 114 | 11.6% / 1.89 / 98 |
| 161 | -1.5% / -0.44 / 55 | 9.0% / 2.08 / 54 | 5.3% / 0.89 / 54 | 6.7% / 1.73 / 61 | 10.2% / 1.36 / 49 |
| 162 | 1.3% / 0.30 / 113 | 15.0% / 2.74 / 104 | 1.9% / 0.35 / 106 | 8.1% / 1.84 / 111 | 4.0% / 0.65 / 94 |
| 163 | 0.2% / 0.13 / 33 | 2.2% / 1.18 / 37 | 5.9% / 1.50 / 28 | 2.6% / 1.23 / 39 | 3.8% / 1.33 / 30 |
| 164 | 2.5% / 0.57 / 132 | 9.4% / 2.04 / 116 | 1.5% / 0.36 / 105 | 2.7% / 0.71 / 131 | 12.4% / 1.64 / 143 |
| 165 | 1.5% / 0.35 / 126 | 14.6% / 2.75 / 135 | -1.7% / -0.27 / 139 | 8.7% / 1.52 / 139 | 9.0% / 1.26 / 133 |
| 166 | -3.9% / -1.19 / 58 | 9.3% / 2.17 / 68 | 0.6% / 0.14 / 63 | 7.5% / 1.96 / 62 | 17.7% / 2.14 / 46 |
| 167 | 5.9% / 0.90 / 101 | 0.1% / 0.04 / 85 | 1.6% / 0.28 / 76 | 9.1% / 1.54 / 109 | 18.2% / 1.75 / 114 |
| 168 | -2.1% / -1.66 / 26 | 2.0% / 0.84 / 34 | 6.7% / 1.46 / 22 | 3.0% / 1.38 / 34 | 10.2% / 2.04 / 28 |
| 169 | -0.3% / -0.13 / 53 | 6.1% / 1.91 / 56 | 1.7% / 0.70 / 46 | 5.6% / 1.93 / 65 | 3.9% / 1.09 / 53 |
| 170 | -0.8% / -0.23 / 77 | 10.1% / 2.40 / 81 | 2.1% / 0.50 / 75 | 5.1% / 1.46 / 78 | 7.3% / 1.43 / 63 |
| 171 | 3.9% / 0.57 / 132 | 6.6% / 1.15 / 116 | 4.2% / 0.60 / 105 | 8.2% / 1.41 / 131 | 18.0% / 1.53 / 143 |
| 172 | -0.9% / -0.28 / 75 | 2.9% / 0.94 / 79 | 2.6% / 0.75 / 56 | 8.9% / 2.96 / 71 | 8.9% / 1.56 / 88 |
| 173 | -0.1% / -0.03 / 86 | 12.1% / 2.31 / 86 | 2.7% / 0.63 / 82 | 6.2% / 1.70 / 83 | 2.5% / 0.49 / 74 |
| 174 | -0.4% / -0.23 / 22 | 1.8% / 0.69 / 30 | 4.2% / 1.30 / 16 | 5.0% / 1.90 / 31 | 7.8% / 1.97 / 23 |
| 175 | 0.3% / 0.14 / 62 | 3.7% / 1.23 / 64 | 6.1% / 1.39 / 56 | 4.6% / 1.74 / 56 | 3.5% / 1.00 / 57 |
| 176 | 0.6% / 0.16 / 130 | 10.2% / 2.41 / 138 | -0.3% / -0.03 / 142 | 6.7% / 1.48 / 139 | 14.3% / 2.07 / 129 |
| 177 | -1.3% / -0.92 / 26 | 2.8% / 1.14 / 34 | 3.9% / 1.68 / 22 | 3.9% / 1.83 / 34 | 3.8% / 1.23 / 28 |
| 178 | 3.2% / 0.77 / 73 | 5.8% / 1.50 / 79 | 3.4% / 0.65 / 91 | 7.9% / 1.82 / 95 | 6.5% / 1.17 / 69 |
| 179 | -0.7% / -0.40 / 33 | 3.0% / 1.55 / 37 | 4.3% / 1.44 / 28 | 2.4% / 1.42 / 39 | 3.3% / 1.25 / 30 |
| 180 | 1.3% / 0.38 / 75 | 10.4% / 2.13 / 79 | 1.2% / 0.26 / 75 | 7.8% / 1.96 / 73 | 6.8% / 1.18 / 62 |
| 181 | 1.2% / 0.24 / 152 | 8.0% / 1.46 / 158 | -2.6% / -0.34 / 156 | 14.9% / 2.41 / 153 | 17.3% / 1.76 / 155 |
| 182 | 1.5% / 0.50 / 98 | 9.5% / 2.32 / 89 | 0.5% / 0.14 / 86 | 4.7% / 1.37 / 96 | 7.2% / 1.26 / 78 |
| 183 | 0.7% / 0.22 / 47 | 3.7% / 1.20 / 50 | 4.9% / 1.20 / 38 | 4.8% / 1.36 / 54 | 6.9% / 1.29 / 47 |
| 184 | -1.1% / -0.66 / 33 | 3.4% / 1.34 / 38 | 3.2% / 1.35 / 28 | 4.9% / 2.12 / 39 | 4.3% / 1.32 / 30 |
| 185 | 1.6% / 0.53 / 52 | 2.0% / 0.87 / 48 | 5.5% / 1.36 / 37 | 3.0% / 1.05 / 56 | 6.2% / 1.46 / 53 |
| 186 | -3.1% / -1.44 / 74 | 4.4% / 1.99 / 71 | 6.7% / 1.90 / 66 | 3.7% / 1.72 / 69 | 4.2% / 1.26 / 66 |
| 187 | -1.5% / -0.43 / 86 | 13.1% / 2.28 / 86 | 2.5% / 0.48 / 82 | 6.6% / 1.62 / 83 | 9.9% / 1.22 / 74 |
| 188 | 0.5% / 0.15 / 104 | 7.2% / 1.95 / 94 | 4.3% / 1.01 / 80 | 6.3% / 1.64 / 107 | 4.3% / 0.91 / 96 |
| 189 | 0.2% / 0.06 / 104 | 5.3% / 1.68 / 94 | 5.3% / 1.15 / 80 | 4.4% / 1.29 / 107 | 5.9% / 1.21 / 96 |
| 190 | -0.0% / -0.01 / 48 | 3.7% / 1.24 / 47 | -1.2% / -0.44 / 35 | 6.0% / 1.95 / 54 | 12.9% / 2.10 / 40 |
| 191 | 4.6% / 1.65 / 23 | 1.0% / 0.55 / 23 | 2.2% / 0.62 / 39 | 3.9% / 1.62 / 35 | 5.2% / 1.42 / 26 |
| 192 | 0.2% / 0.08 / 98 | 11.9% / 2.58 / 89 | 1.1% / 0.28 / 86 | 4.4% / 1.27 / 96 | 7.8% / 1.30 / 78 |
| 193 | 0.9% / 0.65 / 29 | -1.5% / -2.27 / 27 | 0.3% / 0.19 / 32 | 3.2% / 2.07 / 48 | 6.2% / 2.81 / 27 |
| 194 | 1.4% / 0.93 / 29 | -1.7% / -2.57 / 27 | 0.3% / 0.22 / 32 | 3.1% / 1.97 / 48 | 6.1% / 2.81 / 27 |
| 195 | 0.9% / 0.48 / 35 | 2.6% / 1.51 / 36 | 4.8% / 2.04 / 41 | 2.0% / 1.32 / 41 | 2.2% / 0.88 / 41 |
| 196 | -1.1% / -0.31 / 62 | 4.2% / 1.16 / 64 | 8.4% / 1.67 / 56 | 8.8% / 2.58 / 56 | 3.7% / 0.81 / 57 |
| 197 | -1.3% / -0.73 / 53 | 7.7% / 2.43 / 56 | 2.7% / 1.05 / 46 | 5.0% / 1.75 / 65 | 2.1% / 0.63 / 53 |
| 198 | -2.8% / -1.27 / 62 | 4.3% / 1.48 / 65 | 1.7% / 0.62 / 56 | 5.3% / 2.39 / 56 | 7.0% / 1.69 / 57 |
| 199 | -1.6% / -0.74 / 48 | 4.4% / 1.44 / 47 | 3.1% / 0.71 / 35 | 5.0% / 1.52 / 54 | 10.6% / 1.84 / 40 |
| 200 | 0.2% / 0.18 / 21 | 1.6% / 1.33 / 23 | 1.8% / 0.95 / 14 | 2.1% / 1.66 / 24 | 3.5% / 1.58 / 20 |
| 201 | -3.5% / -0.88 / 113 | 13.9% / 2.58 / 104 | 7.7% / 1.09 / 106 | 5.1% / 1.38 / 111 | 7.7% / 1.13 / 94 |
| 202 | 1.3% / 0.48 / 48 | 7.8% / 2.00 / 53 | 3.5% / 0.79 / 47 | 5.1% / 1.61 / 50 | 2.4% / 0.54 / 45 |
| 203 | -1.7% / -0.49 / 44 | 7.3% / 1.79 / 47 | 4.7% / 0.86 / 43 | 5.9% / 1.57 / 52 | 11.0% / 1.45 / 38 |
| 204 | -0.7% / -0.19 / 127 | 14.2% / 2.70 / 124 | 3.2% / 0.66 / 121 | 1.5% / 0.45 / 136 | 5.3% / 0.91 / 102 |
| 205 | -2.4% / -1.18 / 53 | 7.6% / 2.26 / 56 | 4.5% / 1.32 / 46 | 4.3% / 1.41 / 65 | 3.9% / 0.90 / 53 |
| 206 | -0.1% / 0.00 / 180 | 15.3% / 2.63 / 176 | -1.5% / -0.23 / 200 | 8.6% / 1.49 / 197 | 10.1% / 1.31 / 182 |
| 207 | -0.1% / -0.02 / 94 | 9.4% / 2.20 / 95 | 6.6% / 1.10 / 108 | 6.9% / 1.65 / 110 | 4.6% / 0.82 / 87 |
| 208 | 1.5% / 0.25 / 180 | 14.8% / 2.26 / 176 | -7.5% / -1.18 / 200 | 8.6% / 1.44 / 197 | 22.0% / 2.00 / 182 |
| 209 | 0.0% / 0.02 / 49 | 9.1% / 2.36 / 40 | 5.6% / 1.63 / 50 | 1.6% / 0.90 / 45 | 1.0% / 0.31 / 47 |
| 210 | -1.7% / -0.86 / 48 | 5.2% / 1.69 / 47 | 2.9% / 0.95 / 35 | 4.6% / 1.57 / 54 | 6.0% / 1.39 / 40 |
| 211 | -1.1% / -0.38 / 33 | 2.3% / 0.92 / 38 | 7.9% / 1.56 / 28 | 3.6% / 1.28 / 39 | 7.1% / 1.55 / 30 |
| 212 | -1.1% / -0.23 / 75 | 11.0% / 2.04 / 79 | 0.1% / 0.05 / 75 | 8.1% / 1.79 / 73 | 17.9% / 1.88 / 62 |
| 213 | -0.5% / -0.07 / 93 | 10.0% / 1.80 / 95 | 4.0% / 0.54 / 92 | 9.8% / 2.03 / 91 | 12.1% / 1.37 / 77 |
| 214 | -2.9% / -1.31 / 62 | 5.2% / 1.62 / 65 | 1.6% / 0.62 / 56 | 6.1% / 2.53 / 56 | 6.6% / 1.66 / 57 |
| 215 | -2.2% / -1.04 / 53 | 7.1% / 2.01 / 56 | 5.4% / 1.14 / 46 | 4.4% / 1.28 / 65 | 7.5% / 1.35 / 53 |
| 216 | 0.3% / 0.10 / 35 | 1.7% / 0.70 / 43 | 5.8% / 1.39 / 28 | 5.6% / 1.79 / 48 | 4.7% / 1.13 / 39 |
| 217 | -0.7% / -0.15 / 94 | 9.3% / 1.99 / 95 | 6.7% / 0.93 / 108 | 9.5% / 1.98 / 110 | 6.5% / 1.03 / 87 |
| 218 | -2.8% / -1.39 / 74 | 4.4% / 2.00 / 71 | 5.6% / 1.76 / 66 | 4.0% / 1.90 / 69 | 3.7% / 1.15 / 66 |
| 219 | -1.1% / -0.77 / 33 | 2.6% / 1.50 / 37 | 2.7% / 1.33 / 28 | 3.0% / 1.70 / 39 | 2.7% / 1.11 / 30 |
| 220 | 0.2% / 0.11 / 53 | 4.9% / 1.88 / 56 | 1.4% / 0.59 / 46 | 4.4% / 1.70 / 65 | 3.7% / 1.08 / 53 |
| 221 | -4.1% / -1.39 / 75 | 10.9% / 2.31 / 79 | 1.8% / 0.36 / 75 | 5.8% / 1.62 / 73 | 9.8% / 1.57 / 62 |
| 222 | -0.5% / -0.12 / 60 | 2.2% / 0.65 / 68 | 8.4% / 1.20 / 77 | 7.0% / 1.69 / 77 | 11.1% / 1.68 / 58 |
| 223 | -2.7% / -0.72 / 73 | 3.4% / 0.90 / 79 | 8.2% / 1.09 / 91 | 9.8% / 2.18 / 95 | 11.3% / 1.62 / 69 |
| 224 | -0.7% / -0.21 / 44 | 5.7% / 1.38 / 47 | 6.2% / 1.05 / 43 | 5.1% / 1.40 / 52 | 12.2% / 1.57 / 38 |
| 225 | -2.6% / -1.10 / 55 | 9.0% / 2.18 / 54 | 7.5% / 1.26 / 54 | 4.2% / 1.39 / 61 | 4.1% / 0.82 / 49 |
| 226 | -1.0% / -0.34 / 73 | 4.7% / 1.22 / 79 | 7.7% / 1.38 / 91 | 6.9% / 1.84 / 95 | 8.6% / 1.52 / 69 |
| 227 | 3.1% / 0.88 / 73 | 0.7% / 0.25 / 79 | 4.5% / 0.83 / 91 | 5.9% / 1.78 / 95 | 9.2% / 1.70 / 69 |
| 228 | -1.1% / -0.36 / 73 | 2.3% / 0.72 / 79 | 6.9% / 1.31 / 91 | 7.8% / 2.18 / 95 | 7.7% / 1.43 / 69 |
| 229 | -1.7% / -1.38 / 33 | 3.1% / 1.47 / 38 | 2.8% / 1.32 / 28 | 3.2% / 1.77 / 39 | 2.9% / 1.15 / 30 |
| 230 | -0.7% / -0.34 / 53 | 6.4% / 2.46 / 56 | 2.6% / 1.07 / 46 | 4.0% / 1.53 / 65 | 2.0% / 0.63 / 53 |
| 231 | 1.2% / 0.42 / 61 | 1.8% / 0.58 / 57 | 5.1% / 1.22 / 51 | 4.3% / 1.32 / 67 | 6.8% / 1.38 / 60 |
| 232 | -0.4% / -0.05 / 130 | 9.5% / 2.23 / 138 | -3.5% / -0.64 / 142 | 9.5% / 1.87 / 139 | 15.0% / 2.07 / 129 |
| 233 | 0.5% / 0.16 / 75 | 0.2% / 0.09 / 79 | 2.1% / 0.54 / 56 | 10.0% / 3.11 / 71 | 8.9% / 1.50 / 88 |
| 234 | 2.4% / 0.69 / 77 | 4.9% / 1.19 / 81 | 2.9% / 0.61 / 75 | 6.6% / 1.74 / 78 | 7.7% / 1.34 / 63 |
| 235 | -2.1% / -1.34 / 30 | 1.6% / 0.68 / 38 | 4.1% / 0.93 / 26 | 4.1% / 1.75 / 35 | 10.7% / 2.11 / 29 |
| 236 | 12.9% / 1.26 / 180 | 9.4% / 1.33 / 176 | -5.3% / -0.52 / 200 | 10.9% / 1.49 / 197 | 26.7% / 1.86 / 182 |
| 237 | -1.3% / -0.28 / 98 | 9.9% / 2.12 / 89 | 6.7% / 0.92 / 86 | 6.1% / 1.40 / 96 | 11.1% / 1.48 / 78 |
| 238 | 1.3% / 1.14 / 21 | 1.4% / 1.50 / 23 | 1.2% / 0.87 / 14 | 1.2% / 1.24 / 24 | 2.1% / 1.31 / 20 |
| 239 | 0.0% / 0.02 / 44 | 6.3% / 1.76 / 47 | 4.0% / 0.95 / 43 | 5.6% / 1.70 / 52 | 2.8% / 0.64 / 38 |
| 240 | -0.3% / -0.07 / 89 | 7.1% / 1.84 / 87 | 8.0% / 1.67 / 83 | 8.0% / 2.10 / 97 | 0.8% / 0.18 / 81 |
| 241 | 3.1% / 0.84 / 78 | 5.8% / 1.65 / 85 | 2.1% / 0.47 / 93 | 5.0% / 1.37 / 92 | 5.0% / 0.97 / 79 |
| 242 | 0.8% / 0.49 / 44 | 0.2% / 0.13 / 47 | 3.0% / 1.05 / 43 | 2.3% / 1.43 / 52 | 5.3% / 1.91 / 38 |
| 243 | 3.4% / 1.41 / 23 | 1.4% / 0.72 / 23 | 2.5% / 0.66 / 39 | 4.1% / 1.21 / 35 | 7.5% / 1.60 / 26 |
| 244 | 1.4% / 1.21 / 21 | 1.4% / 1.50 / 23 | 1.2% / 0.87 / 14 | 1.2% / 1.24 / 24 | 2.1% / 1.31 / 20 |
| 245 | 1.1% / 0.34 / 104 | 4.7% / 1.62 / 94 | 3.3% / 0.86 / 80 | 4.4% / 1.30 / 107 | 6.1% / 1.28 / 96 |
| 246 | 1.3% / 0.39 / 75 | 8.2% / 1.91 / 79 | 0.2% / 0.07 / 75 | 7.4% / 1.95 / 73 | 7.9% / 1.34 / 62 |
| 247 | -1.2% / -0.84 / 22 | 1.0% / 0.50 / 30 | 2.3% / 1.21 / 16 | 3.5% / 1.83 / 31 | 5.5% / 1.73 / 23 |
| 248 | 1.8% / 0.45 / 113 | 12.6% / 2.58 / 104 | 1.1% / 0.22 / 106 | 7.8% / 1.88 / 111 | 5.4% / 0.84 / 94 |
| 249 | -0.4% / -0.32 / 28 | 2.5% / 1.55 / 35 | 2.5% / 1.39 / 31 | 2.2% / 1.57 / 35 | 2.4% / 1.03 / 35 |
| 250 | 2.3% / 1.03 / 60 | 0.1% / 0.06 / 68 | 1.4% / 0.43 / 77 | 3.3% / 1.65 / 77 | 6.3% / 1.87 / 58 |
| 251 | 0.5% / 0.23 / 38 | 4.5% / 1.27 / 45 | 4.3% / 1.01 / 38 | 3.5% / 1.20 / 42 | 3.7% / 0.87 / 32 |
| 252 | 1.2% / 0.35 / 104 | 2.4% / 0.80 / 94 | 2.5% / 0.64 / 80 | 4.0% / 1.29 / 107 | 7.9% / 1.49 / 96 |
| 253 | 1.6% / 0.45 / 104 | 2.1% / 0.70 / 94 | 4.6% / 1.03 / 80 | 4.0% / 1.16 / 107 | 8.7% / 1.55 / 96 |
| 254 | -0.1% / 0.00 / 101 | 4.4% / 1.23 / 101 | 1.8% / 0.47 / 88 | 5.2% / 1.64 / 92 | 12.8% / 1.90 / 109 |
| 255 | 3.6% / 0.97 / 79 | -0.2% / -0.07 / 88 | 5.0% / 0.90 / 95 | 6.3% / 1.88 / 98 | 9.6% / 1.64 / 83 |
| 256 | 0.7% / 0.18 / 101 | 5.3% / 1.55 / 85 | 3.5% / 0.85 / 76 | 3.6% / 0.92 / 109 | 8.5% / 1.38 / 114 |
| 257 | 1.0% / 0.25 / 96 | 8.0% / 2.10 / 110 | -4.4% / -0.94 / 114 | 10.5% / 2.12 / 114 | 12.5% / 1.94 / 98 |
| 258 | -0.3% / -0.10 / 35 | 0.6% / 0.30 / 42 | 5.2% / 1.21 / 28 | 3.2% / 1.21 / 48 | 5.5% / 1.39 / 39 |
| 259 | 0.0% / 0.02 / 35 | 0.9% / 0.45 / 42 | 4.6% / 1.25 / 28 | 2.6% / 1.09 / 48 | 5.8% / 1.49 / 39 |
| 260 | 5.8% / 1.13 / 126 | 7.9% / 1.55 / 135 | -3.2% / -0.43 / 139 | 7.4% / 1.52 / 139 | 15.9% / 1.79 / 133 |
| 261 | 2.7% / 0.72 / 98 | 7.1% / 1.94 / 89 | 1.1% / 0.23 / 86 | 4.2% / 1.26 / 96 | 7.9% / 1.44 / 78 |
| 262 | -2.3% / -1.67 / 29 | 3.6% / 1.36 / 31 | 3.9% / 0.89 / 22 | 3.8% / 1.60 / 37 | 8.9% / 1.79 / 29 |
| 263 | 0.2% / 0.09 / 78 | 8.4% / 2.11 / 85 | 2.7% / 0.54 / 93 | 4.2% / 1.11 / 92 | 6.0% / 1.05 / 79 |
| 264 | -0.2% / -0.07 / 69 | 4.1% / 1.42 / 68 | 0.6% / 0.22 / 50 | 6.0% / 2.08 / 72 | 6.6% / 1.40 / 73 |
| 265 | -0.5% / -0.34 / 28 | 6.0% / 2.01 / 35 | 2.2% / 1.15 / 31 | 2.5% / 1.47 / 35 | 2.6% / 0.94 / 35 |
| 266 | 1.9% / 0.69 / 58 | 3.6% / 1.20 / 68 | 1.0% / 0.28 / 63 | 4.5% / 1.59 / 62 | 6.2% / 1.53 / 46 |
| 267 | -4.4% / -1.90 / 62 | 4.1% / 1.25 / 65 | 4.3% / 0.78 / 56 | 4.9% / 1.78 / 56 | 12.0% / 2.06 / 57 |
| 268 | -0.9% / -0.21 / 101 | 3.2% / 0.97 / 101 | 4.9% / 1.05 / 88 | 10.1% / 2.82 / 92 | 7.7% / 1.23 / 109 |
| 269 | 0.2% / 0.12 / 35 | 5.8% / 1.94 / 36 | 3.7% / 1.55 / 41 | 1.9% / 1.08 / 41 | 2.1% / 0.72 / 41 |
| 270 | -2.5% / -1.84 / 31 | 3.1% / 1.17 / 36 | 6.3% / 1.31 / 30 | 4.0% / 1.53 / 42 | 7.9% / 1.60 / 33 |
| 271 | 1.8% / 0.59 / 52 | 2.2% / 0.84 / 48 | 2.5% / 0.77 / 37 | 5.2% / 1.60 / 56 | 4.0% / 1.00 / 53 |
| 272 | 0.1% / 0.05 / 58 | 4.2% / 1.14 / 68 | 2.1% / 0.45 / 63 | 4.6% / 1.45 / 62 | 9.7% / 1.79 / 46 |
| 273 | 1.0% / 0.32 / 61 | -1.0% / -0.39 / 57 | 6.4% / 1.28 / 51 | 2.8% / 0.90 / 67 | 10.0% / 1.95 / 60 |
| 274 | -3.2% / -0.82 / 67 | 8.9% / 1.89 / 67 | 10.3% / 1.63 / 62 | 6.7% / 1.58 / 83 | 3.5% / 0.51 / 66 |
| 275 | 0.4% / 0.24 / 26 | 2.1% / 1.62 / 30 | 3.2% / 1.36 / 25 | 1.9% / 1.38 / 37 | 1.9% / 0.84 / 27 |
| 276 | 13.0% / 1.27 / 145 | 9.6% / 1.42 / 133 | -5.9% / -0.64 / 149 | 12.2% / 1.80 / 142 | 11.1% / 0.95 / 128 |
| 277 | 0.4% / 0.21 / 48 | 9.2% / 2.38 / 53 | 3.4% / 0.83 / 47 | 3.1% / 1.26 / 50 | -0.1% / -0.01 / 45 |
| 278 | 0.0% / 0.02 / 35 | 1.6% / 0.65 / 43 | 3.2% / 0.82 / 28 | 7.6% / 2.16 / 48 | 4.9% / 1.14 / 39 |
| 279 | 1.2% / 0.47 / 44 | 5.1% / 1.40 / 47 | 5.4% / 1.19 / 43 | 3.8% / 1.24 / 52 | 3.4% / 0.76 / 38 |
| 280 | -1.8% / -1.27 / 30 | 1.6% / 0.69 / 38 | 2.3% / 0.84 / 26 | 3.3% / 1.63 / 35 | 7.2% / 1.93 / 29 |
| 281 | -3.4% / -1.53 / 30 | 1.8% / 0.61 / 38 | 1.2% / 0.28 / 26 | 6.5% / 2.29 / 35 | 13.9% / 2.36 / 29 |
| 282 | -2.7% / -0.92 / 53 | 5.0% / 1.32 / 56 | 4.2% / 0.99 / 46 | 8.2% / 2.16 / 65 | 4.4% / 0.86 / 53 |
| 283 | -0.5% / -0.49 / 21 | 4.2% / 1.79 / 23 | 1.3% / 0.75 / 14 | 2.4% / 1.45 / 24 | 3.4% / 1.33 / 20 |
| 284 | 2.3% / 1.11 / 48 | 1.5% / 1.18 / 42 | 4.9% / 2.09 / 26 | 1.0% / 0.63 / 49 | -0.8% / -0.48 / 38 |
| 285 | -1.4% / -0.17 / 207 | 14.4% / 2.16 / 213 | -6.1% / -0.87 / 216 | 6.8% / 1.18 / 214 | 22.6% / 2.00 / 201 |
| 286 | 1.8% / 0.82 / 52 | 0.1% / 0.10 / 48 | 3.5% / 1.28 / 37 | 2.3% / 1.28 / 56 | 3.7% / 1.22 / 53 |
| 287 | 8.0% / 1.48 / 37 | 0.5% / 0.25 / 27 | 2.4% / 0.69 / 26 | 5.3% / 1.39 / 33 | 1.8% / 0.43 / 40 |
| 288 | -2.2% / -1.66 / 31 | 3.6% / 1.43 / 36 | 4.4% / 1.34 / 30 | 3.9% / 1.52 / 42 | 3.8% / 1.11 / 33 |
| 289 | -2.1% / -1.09 / 30 | 1.3% / 0.46 / 38 | 1.3% / 0.44 / 26 | 5.7% / 2.21 / 35 | 9.0% / 2.11 / 29 |
| 290 | 7.7% / 1.88 / 26 | 1.7% / 0.85 / 25 | 1.3% / 0.44 / 19 | 2.8% / 0.87 / 26 | 4.4% / 0.91 / 37 |
| 291 | -2.3% / -0.93 / 53 | 4.7% / 1.34 / 56 | 2.7% / 0.86 / 46 | 6.9% / 2.14 / 65 | 4.9% / 1.11 / 53 |
| 292 | -0.6% / -0.17 / 47 | 5.2% / 1.27 / 52 | 6.6% / 1.11 / 47 | 4.8% / 1.31 / 53 | 10.9% / 1.38 / 43 |
| 293 | -2.3% / -0.85 / 77 | 8.6% / 2.46 / 81 | -0.7% / -0.18 / 75 | 5.4% / 1.60 / 78 | 8.2% / 1.64 / 63 |
| 294 | 2.3% / 1.11 / 48 | 1.5% / 1.18 / 42 | 4.9% / 2.09 / 26 | 1.0% / 0.63 / 49 | -0.8% / -0.48 / 38 |
| 295 | 6.9% / 1.98 / 26 | 0.8% / 0.42 / 25 | 1.1% / 0.36 / 19 | 0.9% / 0.32 / 26 | 6.3% / 1.22 / 37 |
| 296 | 6.0% / 1.40 / 30 | 1.1% / 0.47 / 21 | 1.2% / 0.36 / 21 | 3.8% / 1.08 / 25 | 6.9% / 1.32 / 27 |
| 297 | -0.2% / -0.14 / 35 | 2.0% / 0.90 / 43 | 1.0% / 0.48 / 28 | 3.9% / 1.70 / 48 | 6.0% / 1.68 / 39 |
| 298 | 1.6% / 0.59 / 47 | 5.0% / 1.39 / 52 | 6.0% / 1.29 / 47 | 3.7% / 1.21 / 53 | 2.2% / 0.51 / 43 |
| 299 | -1.7% / -0.62 / 48 | 3.2% / 0.95 / 47 | 2.4% / 0.62 / 35 | 8.0% / 2.32 / 54 | 4.5% / 0.94 / 40 |
| 300 | -2.3% / -0.79 / 49 | 9.2% / 2.24 / 40 | 7.2% / 1.73 / 50 | 0.8% / 0.35 / 45 | 3.7% / 0.84 / 47 |
| 301 | -1.0% / -0.20 / 162 | 8.6% / 1.77 / 162 | -1.5% / -0.24 / 168 | 8.9% / 1.63 / 167 | 13.6% / 1.70 / 157 |
| 302 | 10.3% / 1.50 / 73 | 5.7% / 1.23 / 85 | 4.2% / 0.63 / 87 | -0.4% / -0.10 / 78 | 9.5% / 1.16 / 76 |
| 303 | 1.8% / 0.59 / 52 | 2.2% / 0.87 / 48 | 3.8% / 1.14 / 37 | 3.3% / 1.19 / 56 | 3.9% / 0.99 / 53 |
| 304 | 0.3% / 0.25 / 44 | 0.3% / 0.19 / 47 | 2.3% / 0.86 / 43 | 2.4% / 1.45 / 52 | 4.7% / 1.73 / 38 |
| 305 | 1.2% / 0.29 / 94 | 6.8% / 1.47 / 95 | 1.7% / 0.28 / 108 | 6.7% / 1.36 / 110 | 11.2% / 1.53 / 87 |
| 306 | 1.9% / 0.91 / 52 | -0.0% / -0.01 / 48 | 3.5% / 1.29 / 37 | 2.3% / 1.28 / 56 | 3.6% / 1.18 / 53 |
| 307 | 3.7% / 0.96 / 94 | 5.8% / 1.51 / 95 | 0.3% / 0.08 / 108 | 5.8% / 1.49 / 110 | 5.1% / 0.95 / 87 |
| 308 | 3.5% / 1.52 / 23 | 2.0% / 1.06 / 23 | 2.7% / 0.76 / 39 | 2.2% / 0.65 / 35 | 4.9% / 1.09 / 26 |
| 309 | 0.6% / 0.23 / 52 | 4.1% / 1.43 / 48 | 4.2% / 1.16 / 37 | 4.1% / 1.32 / 56 | 2.7% / 0.65 / 53 |
| 310 | -2.3% / -0.89 / 75 | 11.0% / 2.65 / 79 | -0.6% / -0.12 / 75 | 5.1% / 1.60 / 73 | 3.9% / 0.89 / 62 |
| 311 | -1.6% / -0.67 / 35 | 7.6% / 1.97 / 36 | 6.4% / 1.79 / 41 | 0.8% / 0.35 / 41 | 5.2% / 1.15 / 41 |
| 312 | -1.3% / -0.96 / 33 | 1.2% / 0.77 / 38 | 3.0% / 1.22 / 28 | 2.0% / 1.43 / 39 | 4.3% / 1.72 / 30 |
| 313 | -1.0% / -0.46 / 55 | 7.6% / 2.17 / 54 | 1.5% / 0.45 / 54 | 4.9% / 1.74 / 61 | 2.5% / 0.60 / 49 |
| 314 | -0.1% / -0.04 / 35 | 0.7% / 0.45 / 42 | 0.7% / 0.36 / 28 | 3.2% / 1.52 / 48 | 6.7% / 2.01 / 39 |
| 315 | -0.6% / -0.49 / 22 | 1.5% / 0.99 / 29 | 1.8% / 1.04 / 16 | 2.7% / 1.69 / 31 | 3.7% / 1.55 / 23 |
| 316 | 2.0% / 0.52 / 96 | 1.6% / 0.48 / 110 | -0.7% / -0.10 / 114 | 7.6% / 1.96 / 114 | 12.2% / 1.83 / 98 |
| 317 | -0.0% / 0.00 / 43 | 3.3% / 1.59 / 41 | 5.2% / 1.59 / 37 | 3.6% / 1.49 / 52 | 2.4% / 0.65 / 34 |
| 318 | -0.5% / -0.13 / 94 | 7.6% / 1.90 / 95 | 2.0% / 0.41 / 108 | 4.9% / 1.24 / 110 | 5.7% / 0.98 / 87 |
| 319 | -1.5% / -1.28 / 33 | 1.1% / 0.81 / 38 | 3.6% / 1.49 / 28 | 2.2% / 1.60 / 39 | 3.4% / 1.48 / 30 |
| 320 | 1.8% / 0.59 / 61 | -0.2% / -0.06 / 57 | 4.0% / 1.08 / 51 | 2.4% / 0.85 / 67 | 8.3% / 1.77 / 60 |
| 321 | -1.2% / -1.16 / 22 | 1.9% / 1.00 / 30 | 1.7% / 0.97 / 16 | 3.2% / 1.80 / 31 | 3.9% / 1.56 / 23 |
| 322 | 2.2% / 0.80 / 48 | 6.9% / 1.71 / 53 | 5.0% / 0.98 / 47 | 3.1% / 1.02 / 50 | 1.7% / 0.38 / 45 |
| 323 | -0.5% / -0.20 / 47 | 4.3% / 1.54 / 50 | 3.8% / 1.04 / 38 | 4.3% / 1.51 / 54 | 3.2% / 0.77 / 47 |
| 324 | -4.0% / -2.40 / 74 | 6.6% / 2.14 / 71 | 2.7% / 1.07 / 66 | 4.8% / 1.99 / 69 | 3.6% / 1.04 / 66 |
| 325 | 0.1% / 0.05 / 96 | 3.8% / 0.93 / 110 | 1.2% / 0.24 / 114 | 7.2% / 1.69 / 114 | 12.1% / 1.71 / 98 |
| 326 | 1.0% / 0.26 / 85 | -0.3% / -0.08 / 74 | 3.2% / 0.66 / 61 | 6.1% / 1.69 / 87 | 7.7% / 1.26 / 79 |
| 327 | -2.0% / -1.50 / 29 | 3.3% / 1.37 / 31 | 2.9% / 0.97 / 22 | 3.5% / 1.55 / 37 | 4.8% / 1.39 / 29 |
| 328 | 0.7% / 0.43 / 24 | 7.8% / 2.27 / 22 | 2.9% / 1.17 / 28 | -0.7% / -0.71 / 25 | 0.0% / 0.03 / 25 |
| 329 | 4.2% / 1.67 / 23 | 0.4% / 0.30 / 23 | 1.9% / 0.58 / 39 | 3.0% / 1.45 / 35 | 5.5% / 1.61 / 26 |
| 330 | 0.8% / 0.48 / 21 | 3.5% / 2.30 / 23 | 0.7% / 0.49 / 14 | 1.4% / 0.98 / 24 | 1.5% / 0.80 / 20 |
| 331 | -1.5% / -0.67 / 26 | 3.7% / 1.79 / 30 | 4.9% / 1.37 / 25 | 2.1% / 1.05 / 37 | 3.0% / 0.88 / 27 |
| 332 | 0.2% / 0.11 / 55 | 5.9% / 1.85 / 54 | 0.8% / 0.25 / 54 | 5.0% / 1.81 / 61 | 2.3% / 0.59 / 49 |
| 333 | -2.0% / -0.98 / 98 | 11.5% / 2.98 / 89 | -1.4% / -0.43 / 86 | 4.3% / 1.49 / 96 | 3.2% / 0.81 / 78 |
| 334 | -1.2% / -0.58 / 26 | 4.0% / 1.83 / 30 | 3.1% / 1.01 / 25 | 3.4% / 1.62 / 37 | 2.9% / 0.76 / 27 |
| 335 | 0.0% / 0.02 / 44 | 5.7% / 1.62 / 47 | 2.0% / 0.54 / 43 | 6.5% / 1.94 / 52 | 3.7% / 0.84 / 38 |
| 336 | 0.3% / 0.14 / 34 | 8.9% / 2.52 / 24 | 3.7% / 1.19 / 37 | -0.9% / -0.87 / 27 | 0.4% / 0.17 / 28 |
| 337 | 0.5% / 0.14 / 132 | 5.7% / 1.48 / 116 | 2.0% / 0.48 / 105 | 3.8% / 0.97 / 131 | 8.7% / 1.31 / 143 |
| 338 | 1.1% / 0.61 / 26 | 3.6% / 2.26 / 30 | 1.6% / 1.06 / 25 | 0.9% / 0.63 / 37 | 0.9% / 0.42 / 27 |
| 339 | 0.3% / 0.19 / 23 | 2.5% / 1.86 / 27 | 3.2% / 1.39 / 21 | 1.6% / 1.21 / 31 | 1.5% / 0.68 / 25 |
| 340 | 10.8% / 0.99 / 226 | 13.5% / 1.67 / 229 | -6.8% / -0.64 / 228 | 8.0% / 1.09 / 225 | 22.3% / 1.51 / 221 |
| 341 | -3.8% / -1.20 / 48 | 1.2% / 0.38 / 47 | 3.0% / 0.58 / 35 | 7.7% / 2.08 / 54 | 9.5% / 1.45 / 40 |
| 342 | -2.7% / -0.98 / 58 | 7.4% / 2.08 / 68 | -0.0% / 0.02 / 63 | 4.4% / 1.43 / 62 | 7.5% / 1.64 / 46 |
| 343 | -3.2% / -1.67 / 44 | 1.4% / 0.51 / 54 | 3.0% / 0.67 / 37 | 5.3% / 1.95 / 44 | 10.0% / 1.79 / 46 |
| 344 | 7.9% / 1.89 / 26 | 0.4% / 0.20 / 25 | -0.2% / -0.03 / 19 | 3.2% / 0.90 / 26 | 7.0% / 1.13 / 37 |
| 345 | 0.0% / 0.06 / 18 | -1.3% / -2.24 / 21 | 0.7% / 0.56 / 23 | 1.1% / 1.01 / 34 | 5.2% / 2.72 / 19 |
| 346 | -0.6% / -0.50 / 26 | 4.4% / 1.83 / 30 | 1.5% / 0.80 / 25 | 2.6% / 1.42 / 37 | 1.9% / 0.74 / 27 |
| 347 | 1.0% / 0.37 / 47 | 8.1% / 2.27 / 43 | 1.2% / 0.43 / 49 | 0.7% / 0.42 / 45 | 0.9% / 0.32 / 40 |
| 348 | -0.8% / -0.27 / 93 | 5.5% / 1.62 / 90 | 1.9% / 0.58 / 73 | 6.8% / 2.08 / 90 | 5.8% / 1.12 / 105 |
| 349 | -1.0% / -0.64 / 55 | 8.7% / 2.55 / 54 | 0.5% / 0.19 / 54 | 2.8% / 1.23 / 61 | 0.4% / 0.14 / 49 |
| 350 | 2.3% / 0.90 / 30 | -0.2% / -0.10 / 21 | 2.0% / 0.68 / 21 | 1.4% / 0.66 / 25 | 6.3% / 1.64 / 27 |
| 351 | 0.0% / 0.03 / 18 | -1.3% / -2.24 / 21 | 0.7% / 0.52 / 23 | 1.1% / 1.01 / 34 | 5.2% / 2.72 / 19 |
| 352 | 0.5% / 0.13 / 126 | 8.3% / 1.67 / 135 | -3.1% / -0.50 / 139 | 6.5% / 1.35 / 139 | 12.5% / 1.55 / 133 |
| 353 | -3.2% / -1.83 / 74 | 5.4% / 2.07 / 71 | 2.9% / 1.18 / 66 | 4.1% / 1.86 / 69 | 3.2% / 0.97 / 66 |
| 354 | -0.2% / -0.09 / 30 | 5.0% / 1.74 / 26 | 3.5% / 1.89 / 14 | 2.2% / 1.05 / 23 | 1.6% / 0.52 / 21 |
| 355 | 5.7% / 1.63 / 26 | 0.2% / 0.14 / 25 | 0.3% / 0.13 / 19 | 2.5% / 0.87 / 26 | 8.5% / 1.46 / 37 |
| 356 | 1.3% / 1.37 / 29 | -1.0% / -1.47 / 27 | -0.1% / -0.12 / 32 | 1.2% / 1.25 / 48 | 3.1% / 2.35 / 27 |
| 357 | 1.3% / 1.37 / 29 | -1.0% / -1.47 / 27 | -0.1% / -0.12 / 32 | 1.2% / 1.25 / 48 | 3.1% / 2.35 / 27 |
| 358 | 0.8% / 0.34 / 34 | 7.9% / 2.25 / 36 | 2.9% / 1.12 / 33 | 0.4% / 0.33 / 33 | -0.2% / -0.06 / 33 |
| 359 | 0.7% / 0.40 / 52 | 2.4% / 1.66 / 54 | 1.0% / 0.51 / 54 | 2.2% / 1.48 / 64 | 1.9% / 0.80 / 63 |
| 360 | -2.4% / -0.48 / 113 | 11.8% / 2.36 / 104 | 2.6% / 0.39 / 106 | 7.5% / 1.58 / 111 | 8.6% / 1.14 / 94 |
| 361 | 11.8% / 1.14 / 161 | 11.7% / 1.58 / 151 | -6.0% / -0.63 / 158 | 11.2% / 1.63 / 156 | 11.7% / 0.96 / 146 |
| 362 | -0.9% / -0.81 / 31 | 3.5% / 1.51 / 36 | 2.3% / 0.99 / 30 | 3.3% / 1.61 / 42 | 1.5% / 0.57 / 33 |
| 363 | -2.7% / -0.68 / 58 | 5.0% / 1.17 / 68 | -0.8% / -0.11 / 63 | 6.0% / 1.61 / 62 | 16.0% / 1.90 / 46 |
| 364 | 7.8% / 1.35 / 51 | 0.3% / 0.14 / 39 | 0.5% / 0.14 / 35 | 4.7% / 1.22 / 42 | 5.4% / 1.00 / 46 |
| 365 | -2.1% / -0.84 / 53 | 2.6% / 0.91 / 56 | 2.9% / 0.91 / 46 | 5.6% / 2.02 / 65 | 5.0% / 1.15 / 53 |
| 366 | 1.6% / 0.84 / 60 | 0.3% / 0.19 / 68 | 1.2% / 0.37 / 77 | 2.9% / 1.53 / 77 | 5.9% / 1.78 / 58 |
| 367 | 1.3% / 0.51 / 53 | 9.7% / 2.36 / 58 | 3.6% / 1.12 / 54 | -0.3% / -0.13 / 57 | 0.7% / 0.20 / 53 |
| 368 | 1.3% / 0.68 / 37 | 3.1% / 2.05 / 35 | 2.3% / 0.84 / 40 | 1.1% / 0.78 / 46 | 2.4% / 0.98 / 35 |
| 369 | -0.8% / -0.56 / 26 | 4.6% / 2.28 / 30 | 2.0% / 1.03 / 25 | 1.9% / 1.10 / 37 | 1.5% / 0.61 / 27 |
| 370 | 0.2% / 0.14 / 29 | -1.5% / -2.06 / 27 | -0.7% / -0.45 / 32 | 3.4% / 1.71 / 48 | 7.3% / 2.41 / 27 |
| 371 | 0.1% / 0.04 / 44 | 2.2% / 0.81 / 53 | 4.9% / 1.26 / 37 | 4.1% / 1.71 / 44 | 3.4% / 1.05 / 46 |
| 372 | -1.3% / -0.90 / 22 | 1.8% / 0.75 / 30 | 2.3% / 1.21 / 16 | 3.6% / 1.82 / 31 | 5.0% / 1.66 / 23 |
| 373 | -1.1% / -0.77 / 21 | 4.5% / 2.29 / 23 | 1.2% / 0.67 / 14 | 2.3% / 1.38 / 24 | 2.3% / 0.98 / 20 |
| 374 | 6.4% / 1.91 / 26 | 1.3% / 0.75 / 25 | 1.7% / 0.64 / 19 | 0.7% / 0.27 / 26 | 4.3% / 0.99 / 37 |
| 375 | 0.3% / 0.19 / 23 | 2.5% / 1.86 / 27 | 3.4% / 1.42 / 21 | 1.5% / 1.19 / 31 | 1.5% / 0.68 / 25 |
| 376 | 0.5% / 0.32 / 52 | 2.3% / 1.62 / 54 | 1.0% / 0.51 / 54 | 2.2% / 1.52 / 64 | 1.8% / 0.77 / 63 |
| 377 | -2.9% / -1.78 / 75 | 10.8% / 2.93 / 79 | -3.4% / -1.27 / 75 | 3.8% / 1.49 / 73 | 4.3% / 1.14 / 62 |
| 378 | 2.4% / 1.03 / 36 | -1.7% / -1.99 / 26 | 6.3% / 2.22 / 34 | 2.0% / 1.18 / 33 | 0.3% / 0.14 / 29 |
| 379 | -0.3% / -0.22 / 31 | 2.7% / 1.49 / 36 | 2.2% / 0.98 / 30 | 2.7% / 1.44 / 42 | 1.4% / 0.54 / 33 |
| 380 | 1.0% / 0.45 / 53 | 1.9% / 1.06 / 56 | 1.1% / 0.48 / 46 | 1.6% / 0.92 / 65 | 4.4% / 1.39 / 53 |
| 381 | 6.9% / 1.34 / 38 | -0.5% / -0.19 / 42 | 1.1% / 0.21 / 51 | 7.2% / 1.61 / 53 | 7.6% / 1.12 / 52 |
| 382 | -2.4% / -0.72 / 89 | 5.6% / 1.68 / 87 | 6.8% / 1.59 / 83 | 6.5% / 1.95 / 97 | 2.4% / 0.48 / 81 |
| 383 | 3.8% / 1.26 / 95 | 4.1% / 1.67 / 95 | 0.9% / 0.27 / 90 | 2.5% / 1.17 / 95 | 2.6% / 0.71 / 85 |
| 384 | 2.1% / 0.89 / 77 | 1.9% / 0.86 / 81 | 1.3% / 0.42 / 75 | 2.6% / 1.28 / 78 | 3.9% / 1.20 / 63 |
| 385 | -0.0% / 0.00 / 50 | 3.1% / 1.16 / 57 | 0.9% / 0.26 / 40 | 4.0% / 1.31 / 55 | 6.3% / 1.49 / 54 |
| 386 | 5.0% / 1.62 / 26 | 0.4% / 0.28 / 25 | -0.4% / -0.23 / 19 | 2.0% / 0.79 / 26 | 7.6% / 1.56 / 37 |
| 387 | -0.8% / -0.52 / 48 | 8.8% / 2.57 / 53 | 0.3% / 0.12 / 47 | 3.1% / 1.37 / 50 | 0.1% / 0.06 / 45 |
| 388 | 2.4% / 0.55 / 99 | 5.3% / 1.14 / 108 | 1.0% / 0.17 / 115 | 6.7% / 1.35 / 116 | 11.4% / 1.48 / 103 |
| 389 | 0.7% / 0.25 / 67 | 12.7% / 2.86 / 69 | 3.0% / 0.85 / 71 | -1.2% / -0.62 / 72 | 1.0% / 0.27 / 65 |
| 390 | -2.9% / -1.76 / 67 | 9.0% / 2.58 / 67 | 1.8% / 0.73 / 62 | 3.9% / 1.39 / 83 | 1.9% / 0.56 / 66 |
| 391 | 1.7% / 0.93 / 30 | 1.2% / 0.98 / 26 | 2.0% / 1.61 / 14 | 0.4% / 0.41 / 23 | 0.4% / 0.33 / 21 |
| 392 | -1.0% / -0.53 / 23 | 3.5% / 1.91 / 27 | 1.9% / 0.70 / 21 | 4.0% / 2.16 / 31 | 2.9% / 0.87 / 25 |
| 393 | 3.8% / 1.28 / 38 | 2.0% / 0.97 / 42 | 2.9% / 0.74 / 51 | 3.1% / 0.75 / 53 | 5.7% / 1.09 / 52 |
| 394 | 1.6% / 0.82 / 65 | 2.2% / 1.63 / 60 | 2.2% / 1.02 / 42 | 1.7% / 0.99 / 64 | 0.6% / 0.30 / 55 |
| 395 | -3.2% / -1.18 / 53 | 3.5% / 1.11 / 56 | 4.7% / 1.12 / 46 | 7.1% / 2.07 / 65 | 3.8% / 0.78 / 53 |
| 396 | 1.0% / 0.57 / 29 | -1.5% / -1.82 / 27 | 0.6% / 0.31 / 32 | 2.2% / 1.12 / 48 | 6.8% / 2.28 / 27 |
| 397 | -0.2% / -0.16 / 26 | -0.0% / 0.01 / 34 | 3.5% / 1.66 / 22 | 2.4% / 1.84 / 34 | 2.4% / 1.07 / 28 |
| 398 | -0.6% / -0.30 / 49 | 4.6% / 1.99 / 39 | 4.0% / 1.52 / 49 | 1.9% / 1.25 / 44 | -0.3% / -0.11 / 47 |
| 399 | 2.6% / 0.92 / 37 | 0.3% / 0.17 / 27 | 3.1% / 1.02 / 26 | 1.9% / 0.82 / 33 | 3.9% / 1.02 / 40 |
| 400 | -0.1% / -0.01 / 33 | 3.7% / 1.58 / 29 | 7.2% / 1.44 / 35 | 2.7% / 1.25 / 39 | 1.1% / 0.35 / 31 |
| 401 | -1.9% / -0.70 / 44 | 3.2% / 1.03 / 47 | 8.2% / 1.33 / 43 | 2.5% / 0.82 / 52 | 6.6% / 1.29 / 38 |
| 402 | -0.7% / -0.55 / 23 | 3.9% / 1.76 / 27 | 2.0% / 1.18 / 21 | 2.3% / 1.39 / 31 | 1.2% / 0.50 / 25 |
| 403 | -4.2% / -2.54 / 62 | 3.8% / 1.51 / 65 | 1.0% / 0.39 / 56 | 3.4% / 1.65 / 56 | 7.0% / 2.07 / 57 |
| 404 | 1.6% / 0.82 / 65 | 1.9% / 1.48 / 60 | 2.2% / 1.02 / 42 | 1.8% / 1.02 / 64 | 0.6% / 0.30 / 55 |
| 405 | 1.3% / 0.34 / 113 | 9.6% / 2.46 / 104 | -1.3% / -0.23 / 106 | 6.2% / 1.75 / 111 | 5.1% / 0.90 / 94 |
| 406 | -2.1% / -0.74 / 43 | 4.3% / 1.86 / 41 | 7.5% / 1.86 / 37 | 3.5% / 1.38 / 52 | 2.1% / 0.57 / 34 |
| 407 | -0.1% / -0.04 / 77 | 5.7% / 1.48 / 81 | 0.6% / 0.17 / 75 | 3.1% / 1.03 / 78 | 6.6% / 1.34 / 63 |
| 408 | 9.2% / 1.44 / 58 | 5.1% / 1.18 / 67 | 4.1% / 0.73 / 58 | 2.0% / 0.59 / 61 | 2.1% / 0.35 / 60 |
| 409 | -1.8% / -0.53 / 113 | 13.1% / 2.82 / 104 | 1.4% / 0.32 / 106 | 4.0% / 1.22 / 111 | 0.5% / 0.14 / 94 |
| 410 | 0.6% / 0.29 / 53 | 1.7% / 0.94 / 56 | 1.0% / 0.44 / 46 | 1.9% / 1.09 / 65 | 4.5% / 1.42 / 53 |
| 411 | -0.6% / -0.36 / 21 | 2.8% / 1.52 / 23 | 0.5% / 0.27 / 14 | 2.7% / 1.56 / 24 | 3.5% / 1.14 / 20 |
| 412 | 0.8% / 0.41 / 33 | 4.3% / 1.78 / 29 | 2.3% / 0.83 / 35 | 2.1% / 1.20 / 39 | 2.0% / 0.67 / 31 |
| 413 | -0.2% / -0.07 / 55 | 7.3% / 1.93 / 54 | 1.6% / 0.44 / 54 | 2.7% / 1.00 / 61 | 2.4% / 0.54 / 49 |
| 414 | 1.4% / 0.56 / 77 | 2.3% / 0.98 / 81 | 1.8% / 0.55 / 75 | 2.4% / 1.21 / 78 | 3.7% / 1.14 / 63 |
| 415 | 3.2% / 1.22 / 23 | -0.1% / -0.05 / 23 | 3.0% / 0.72 / 39 | 5.3% / 1.83 / 35 | 3.5% / 0.93 / 26 |
| 416 | 1.0% / 1.17 / 21 | 0.9% / 0.91 / 20 | 1.0% / 1.05 / 21 | 0.3% / 0.47 / 15 | 0.6% / 0.57 / 23 |
| 417 | -2.1% / -0.64 / 113 | 12.6% / 2.77 / 104 | -1.4% / -0.31 / 106 | 4.9% / 1.37 / 111 | 6.6% / 1.10 / 94 |
| 418 | -2.5% / -0.48 / 69 | 5.5% / 1.22 / 63 | 13.5% / 1.81 / 75 | 4.1% / 0.93 / 80 | 3.7% / 0.54 / 73 |
| 419 | -0.9% / -0.41 / 24 | 7.9% / 2.30 / 22 | 3.7% / 1.18 / 28 | 1.9% / 1.03 / 25 | 0.4% / 0.16 / 25 |
| 420 | -0.4% / -0.12 / 50 | 3.1% / 1.17 / 57 | 2.8% / 0.81 / 40 | 1.6% / 0.60 / 55 | 6.3% / 1.58 / 54 |
| 421 | 2.2% / 1.10 / 48 | 2.5% / 1.39 / 53 | 0.4% / 0.17 / 47 | 2.7% / 1.62 / 50 | 1.6% / 0.60 / 45 |
| 422 | 3.0% / 0.69 / 69 | 5.5% / 1.36 / 63 | 5.2% / 1.11 / 75 | 0.6% / 0.19 / 80 | 5.3% / 0.93 / 73 |
| 423 | 7.5% / 1.59 / 23 | -0.1% / -0.04 / 23 | 1.3% / 0.29 / 39 | 6.4% / 1.67 / 35 | 3.4% / 0.78 / 26 |
| 424 | -0.5% / -0.24 / 38 | 3.9% / 1.41 / 31 | 1.3% / 0.61 / 21 | 5.3% / 2.04 / 35 | 1.5% / 0.43 / 27 |
| 425 | 5.0% / 1.38 / 37 | 0.2% / 0.15 / 27 | 2.4% / 0.79 / 26 | 2.7% / 0.95 / 33 | 1.9% / 0.47 / 40 |
| 426 | 1.0% / 1.17 / 21 | 0.9% / 0.91 / 20 | 1.0% / 1.05 / 21 | 0.3% / 0.47 / 15 | 0.6% / 0.57 / 23 |
| 427 | 8.3% / 1.59 / 38 | 1.2% / 0.51 / 42 | 0.8% / 0.19 / 51 | 5.1% / 1.18 / 53 | 5.1% / 0.87 / 52 |
| 428 | -1.0% / -0.75 / 28 | 3.0% / 1.71 / 35 | 2.7% / 1.42 / 31 | 2.5% / 1.65 / 35 | 1.3% / 0.63 / 35 |
| 429 | -4.1% / -2.15 / 89 | 9.6% / 2.67 / 87 | 1.6% / 0.62 / 83 | 3.8% / 1.32 / 97 | 3.4% / 0.89 / 81 |
| 430 | -0.1% / -0.04 / 24 | 4.5% / 2.08 / 22 | 3.3% / 1.19 / 28 | 1.7% / 1.20 / 25 | 0.7% / 0.26 / 25 |
| 431 | 1.7% / 0.93 / 30 | 1.2% / 0.98 / 26 | 2.4% / 1.25 / 14 | 0.4% / 0.41 / 23 | 0.3% / 0.26 / 21 |
| 432 | 1.5% / 0.53 / 32 | 0.8% / 0.42 / 33 | 2.6% / 0.64 / 49 | 4.7% / 1.78 / 45 | 5.0% / 1.32 / 31 |
| 433 | 0.3% / 0.44 / 21 | 0.8% / 1.38 / 23 | 0.2% / 0.28 / 14 | 0.6% / 0.98 / 24 | 1.5% / 1.52 / 20 |
| 434 | 4.2% / 1.29 / 31 | 0.7% / 0.42 / 25 | 0.7% / 0.26 / 20 | 0.6% / 0.26 / 27 | 6.8% / 1.39 / 43 |
| 435 | 7.7% / 1.64 / 23 | 0.6% / 0.33 / 23 | -0.1% / -0.01 / 39 | 5.2% / 1.34 / 35 | 1.4% / 0.35 / 26 |
| 436 | 1.7% / 0.87 / 23 | -0.1% / -0.08 / 23 | 3.0% / 0.83 / 39 | 3.1% / 1.44 / 35 | 4.0% / 1.22 / 26 |
| 437 | -0.5% / -0.19 / 30 | 1.5% / 0.82 / 26 | 4.7% / 1.83 / 14 | 1.4% / 0.85 / 23 | 2.5% / 0.81 / 21 |
| 438 | -0.6% / -0.53 / 28 | 2.5% / 1.68 / 34 | 1.6% / 0.98 / 31 | 2.0% / 1.42 / 35 | 1.9% / 0.91 / 35 |
| 439 | -0.2% / -0.07 / 98 | 5.5% / 2.25 / 89 | 0.8% / 0.24 / 86 | 3.0% / 1.31 / 96 | 3.2% / 0.92 / 78 |
| 440 | 2.9% / 0.94 / 38 | 0.8% / 0.36 / 42 | 0.9% / 0.22 / 51 | 5.1% / 1.21 / 53 | 8.5% / 1.34 / 52 |
| 441 | 2.4% / 1.03 / 36 | -1.5% / -1.71 / 26 | 5.3% / 2.07 / 34 | 1.7% / 1.08 / 33 | 0.3% / 0.18 / 29 |
| 442 | 1.8% / 0.97 / 23 | 2.1% / 1.13 / 23 | 0.8% / 0.28 / 39 | 2.4% / 0.83 / 35 | 5.3% / 1.27 / 26 |
| 443 | 0.3% / 0.44 / 21 | 0.8% / 1.38 / 23 | 0.2% / 0.28 / 14 | 0.6% / 0.98 / 24 | 1.5% / 1.52 / 20 |
| 444 | 0.5% / 0.32 / 33 | 2.7% / 1.94 / 29 | 2.4% / 0.88 / 35 | 1.3% / 0.92 / 39 | 2.4% / 0.99 / 31 |
| 445 | 2.0% / 0.85 / 18 | -0.1% / -0.04 / 21 | 0.3% / 0.14 / 23 | -1.6% / -0.87 / 34 | 10.3% / 2.25 / 19 |
| 446 | -0.4% / -0.23 / 35 | -0.2% / -0.14 / 43 | 1.4% / 0.59 / 28 | 2.4% / 1.51 / 48 | 5.0% / 1.76 / 39 |
| 447 | 3.8% / 1.06 / 31 | -0.5% / -0.20 / 25 | -0.9% / -0.26 / 20 | 5.4% / 1.48 / 27 | 10.9% / 1.54 / 43 |
| 448 | -1.2% / -0.66 / 19 | 6.5% / 2.14 / 18 | 3.9% / 1.29 / 26 | 0.7% / 0.48 / 23 | 0.6% / 0.22 / 21 |
| 449 | 0.0% / 0.03 / 85 | 2.8% / 1.33 / 74 | 1.0% / 0.40 / 61 | 3.0% / 1.25 / 87 | 4.0% / 1.16 / 79 |
| 450 | 0.3% / 0.14 / 52 | 2.9% / 1.61 / 54 | 1.7% / 0.69 / 54 | 2.9% / 1.53 / 64 | 2.1% / 0.71 / 63 |
| 451 | 3.7% / 1.32 / 85 | -0.6% / -0.31 / 74 | -1.3% / -0.52 / 61 | 3.3% / 1.56 / 87 | 5.5% / 1.48 / 79 |
| 452 | 1.6% / 0.35 / 86 | 6.8% / 1.57 / 75 | 5.0% / 1.03 / 89 | -0.2% / -0.05 / 89 | 4.8% / 0.81 / 84 |
| 453 | -1.2% / -1.06 / 29 | 3.0% / 1.35 / 31 | 1.1% / 0.59 / 22 | 3.2% / 1.62 / 37 | 2.5% / 0.95 / 29 |
| 454 | -1.2% / -0.67 / 23 | 4.4% / 1.76 / 27 | 2.0% / 0.71 / 21 | 5.0% / 2.23 / 31 | 0.0% / 0.02 / 25 |
| 455 | -0.5% / -0.25 / 44 | 4.4% / 1.35 / 47 | 3.1% / 0.94 / 43 | 3.0% / 1.20 / 52 | 3.1% / 0.82 / 38 |
| 456 | -1.4% / -0.99 / 26 | 5.4% / 2.20 / 30 | 2.0% / 1.06 / 25 | 2.3% / 1.17 / 37 | 0.3% / 0.14 / 27 |
| 457 | -3.0% / -2.07 / 44 | 3.1% / 1.30 / 54 | 1.0% / 0.45 / 37 | 3.7% / 1.82 / 44 | 4.7% / 1.49 / 46 |
| 458 | -0.5% / -0.20 / 52 | 0.2% / 0.15 / 54 | 2.9% / 0.95 / 54 | 2.5% / 1.32 / 64 | 4.9% / 1.46 / 63 |
| 459 | -0.5% / -0.30 / 26 | 3.6% / 1.81 / 30 | 1.4% / 0.61 / 25 | 2.2% / 1.14 / 37 | 2.5% / 0.77 / 27 |
| 460 | -0.5% / -0.41 / 29 | 2.2% / 1.30 / 31 | 1.1% / 0.60 / 22 | 2.5% / 1.46 / 37 | 2.3% / 0.92 / 29 |
| 461 | -1.6% / -0.52 / 55 | 4.9% / 1.44 / 54 | 6.4% / 1.01 / 54 | 1.7% / 0.53 / 61 | 6.1% / 1.07 / 49 |
| 462 | 0.8% / 0.74 / 21 | 1.9% / 2.02 / 23 | 0.4% / 0.43 / 14 | 0.8% / 0.69 / 24 | 0.5% / 0.36 / 20 |
| 463 | 0.8% / 0.74 / 21 | 1.9% / 2.02 / 23 | 0.4% / 0.43 / 14 | 0.8% / 0.69 / 24 | 0.5% / 0.36 / 20 |
| 464 | -0.6% / -0.38 / 23 | 3.4% / 1.82 / 27 | 0.7% / 0.32 / 21 | 3.4% / 1.74 / 31 | 2.2% / 0.69 / 25 |
| 465 | -0.2% / -0.10 / 30 | 2.9% / 1.36 / 26 | 3.9% / 1.96 / 14 | 1.6% / 0.85 / 23 | 1.3% / 0.43 / 21 |
| 466 | -0.3% / -0.10 / 85 | 1.4% / 0.72 / 74 | 2.4% / 0.77 / 61 | 3.2% / 1.36 / 87 | 5.1% / 1.39 / 79 |
| 467 | 5.1% / 2.03 / 58 | -2.2% / -1.17 / 72 | 3.0% / 1.18 / 51 | -0.4% / -0.23 / 58 | 5.3% / 1.50 / 63 |
| 468 | 3.0% / 1.08 / 32 | 0.7% / 0.43 / 33 | 1.4% / 0.39 / 49 | 2.9% / 1.32 / 45 | 5.0% / 1.40 / 31 |
| 469 | -0.5% / -0.28 / 47 | -0.7% / -0.40 / 50 | 3.8% / 1.54 / 38 | 2.8% / 1.70 / 54 | 4.6% / 1.54 / 47 |
| 470 | 2.8% / 1.11 / 85 | -0.8% / -0.48 / 74 | -0.3% / -0.11 / 61 | 2.9% / 1.43 / 87 | 5.5% / 1.49 / 79 |
| 471 | -0.1% / -0.01 / 34 | 7.5% / 2.15 / 36 | 1.7% / 0.62 / 33 | -0.3% / -0.20 / 33 | 2.5% / 0.66 / 33 |
| 472 | -0.1% / -0.07 / 25 | 3.0% / 1.63 / 21 | 1.5% / 1.01 / 24 | 0.5% / 0.52 / 23 | 1.0% / 0.60 / 28 |
| 473 | -0.7% / -0.33 / 52 | 0.5% / 0.30 / 54 | 2.1% / 0.70 / 54 | 2.1% / 1.14 / 64 | 5.3% / 1.60 / 63 |
| 474 | 5.1% / 1.36 / 31 | 1.2% / 0.57 / 25 | -0.3% / -0.07 / 20 | 1.8% / 0.63 / 27 | 8.1% / 1.42 / 43 |
| 475 | -2.4% / -1.53 / 30 | 2.6% / 1.05 / 38 | 1.1% / 0.41 / 26 | 2.7% / 1.28 / 35 | 7.5% / 1.97 / 29 |
| 476 | 2.2% / 1.50 / 24 | 2.4% / 2.06 / 22 | 0.4% / 0.29 / 28 | 0.1% / 0.15 / 25 | 0.1% / 0.08 / 25 |
| 477 | 0.4% / 0.22 / 35 | 2.5% / 1.64 / 35 | 3.2% / 1.42 / 41 | 1.7% / 1.15 / 41 | 0.9% / 0.41 / 41 |
| 478 | -1.6% / -0.98 / 21 | 3.0% / 1.47 / 23 | 1.4% / 0.51 / 14 | 3.3% / 1.75 / 24 | 3.7% / 1.04 / 20 |
| 479 | -0.0% / -0.00 / 36 | -1.3% / -1.70 / 26 | 7.3% / 2.64 / 34 | 1.5% / 1.06 / 33 | 1.8% / 0.85 / 29 |
| 480 | -1.0% / -0.74 / 28 | 3.6% / 2.08 / 35 | 2.4% / 1.33 / 31 | 1.9% / 1.37 / 35 | 0.7% / 0.38 / 35 |
| 481 | -0.7% / -0.22 / 34 | 7.5% / 2.12 / 36 | 3.5% / 1.07 / 33 | 1.8% / 0.88 / 33 | -0.3% / -0.07 / 33 |
| 482 | 1.4% / 0.81 / 48 | 2.3% / 1.30 / 53 | 0.6% / 0.24 / 47 | 2.4% / 1.50 / 50 | 1.7% / 0.63 / 45 |
| 483 | 1.6% / 0.65 / 29 | -1.9% / -2.55 / 27 | 0.8% / 0.33 / 32 | 3.6% / 1.44 / 48 | 6.8% / 1.66 / 27 |
| 484 | 3.7% / 0.84 / 126 | 4.2% / 1.05 / 135 | -4.4% / -0.68 / 139 | 4.1% / 1.02 / 139 | 14.9% / 1.97 / 133 |
| 485 | 0.3% / 0.22 / 24 | 5.9% / 2.18 / 22 | 1.9% / 0.91 / 28 | -0.6% / -0.58 / 25 | 0.2% / 0.09 / 25 |
| 486 | -3.3% / -3.14 / 26 | 4.3% / 1.63 / 30 | 7.5% / 1.50 / 25 | 2.6% / 1.18 / 37 | 2.4% / 0.65 / 27 |
| 487 | -0.3% / -0.19 / 31 | 1.1% / 0.78 / 36 | 2.5% / 1.06 / 30 | 2.2% / 1.44 / 42 | 2.0% / 0.85 / 33 |
| 488 | -0.9% / -1.13 / 25 | 4.0% / 2.01 / 21 | 1.1% / 0.83 / 24 | 0.2% / 0.18 / 23 | 2.2% / 1.01 / 28 |
| 489 | 0.5% / 0.29 / 27 | 4.2% / 2.36 / 20 | 1.8% / 0.84 / 34 | 0.7% / 0.60 / 25 | 0.5% / 0.29 / 23 |
| 490 | 2.4% / 0.92 / 86 | 3.3% / 1.46 / 86 | 1.4% / 0.46 / 82 | 3.2% / 1.53 / 83 | 0.2% / 0.08 / 74 |
| 491 | 0.3% / 0.13 / 30 | 1.3% / 0.80 / 26 | 3.4% / 1.83 / 14 | 1.0% / 0.59 / 23 | 2.4% / 0.85 / 21 |
| 492 | 2.3% / 0.88 / 18 | -0.2% / -0.11 / 21 | -0.5% / -0.20 / 23 | 0.2% / 0.11 / 34 | 10.5% / 2.36 / 19 |
| 493 | 7.9% / 2.43 / 34 | -0.7% / -0.45 / 32 | 0.1% / 0.04 / 46 | -0.6% / -0.31 / 49 | 5.7% / 1.45 / 38 |
| 494 | -2.5% / -0.98 / 43 | 5.2% / 1.68 / 41 | 4.6% / 1.41 / 37 | 6.2% / 2.04 / 52 | -0.8% / -0.18 / 34 |
| 495 | 2.5% / 1.02 / 48 | 2.1% / 0.80 / 53 | 1.9% / 0.47 / 47 | 1.2% / 0.54 / 50 | 4.6% / 1.10 / 45 |
| 496 | 0.7% / 0.43 / 33 | 0.1% / 0.07 / 38 | 2.2% / 1.02 / 28 | 2.5% / 1.78 / 39 | 2.4% / 1.05 / 30 |
| 497 | -2.8% / -1.15 / 43 | 4.1% / 1.68 / 41 | 5.3% / 1.55 / 37 | 5.0% / 1.83 / 52 | 0.5% / 0.15 / 34 |
| 498 | 1.8% / 1.22 / 29 | -1.3% / -1.20 / 27 | -1.3% / -0.78 / 32 | 0.9% / 0.59 / 48 | 6.4% / 2.84 / 27 |
| 499 | -2.5% / -1.17 / 34 | 9.0% / 2.39 / 24 | 4.6% / 1.29 / 37 | -1.0% / -0.69 / 27 | 1.9% / 0.57 / 28 |
| 500 | 0.3% / 0.20 / 52 | 2.8% / 1.55 / 54 | 1.8% / 0.76 / 54 | 2.7% / 1.44 / 64 | 1.6% / 0.57 / 63 |
| 501 | 0.3% / 0.10 / 47 | 10.1% / 2.36 / 43 | 3.2% / 0.67 / 49 | 0.6% / 0.25 / 45 | 1.9% / 0.39 / 40 |
| 502 | -2.5% / -2.47 / 23 | 3.4% / 1.44 / 27 | 7.4% / 1.53 / 21 | 2.9% / 1.37 / 31 | 0.8% / 0.27 / 25 |
| 503 | -2.1% / -0.85 / 98 | 5.9% / 2.38 / 89 | 1.4% / 0.40 / 86 | 3.3% / 1.45 / 96 | 3.1% / 0.88 / 78 |
| 504 | -0.7% / -0.34 / 19 | 4.4% / 2.18 / 18 | 2.5% / 0.97 / 26 | 0.6% / 0.49 / 23 | 1.4% / 0.54 / 21 |
| 505 | -3.0% / -0.95 / 34 | 9.8% / 2.44 / 24 | 4.5% / 1.01 / 37 | 0.4% / 0.21 / 27 | 3.3% / 0.80 / 28 |
| 506 | -0.8% / -0.24 / 55 | 8.3% / 2.09 / 50 | 5.5% / 1.23 / 62 | -0.2% / -0.05 / 58 | 2.4% / 0.51 / 52 |
| 507 | 2.2% / 0.77 / 29 | -1.5% / -1.16 / 27 | -0.6% / -0.19 / 32 | 0.7% / 0.30 / 48 | 11.8% / 2.30 / 27 |
| 508 | 4.6% / 2.33 / 34 | -0.8% / -0.57 / 32 | -1.0% / -0.43 / 46 | 0.9% / 0.57 / 49 | 6.2% / 2.12 / 38 |
| 509 | -0.0% / -0.00 / 34 | 7.2% / 2.46 / 24 | 1.1% / 0.49 / 37 | -0.7% / -0.75 / 27 | 0.6% / 0.28 / 28 |
| 510 | -1.0% / -0.54 / 47 | 0.4% / 0.23 / 50 | 1.3% / 0.51 / 38 | 2.2% / 1.34 / 54 | 5.5% / 1.84 / 47 |
| 511 | 0.0% / 0.03 / 36 | -1.8% / -2.27 / 26 | 7.2% / 2.57 / 34 | 1.5% / 1.04 / 33 | 1.0% / 0.50 / 29 |
| 512 | -0.5% / -0.41 / 29 | 0.7% / 0.54 / 31 | 1.9% / 0.90 / 22 | 2.2% / 1.51 / 37 | 2.9% / 1.23 / 29 |
| 513 | 2.0% / 0.77 / 55 | 2.0% / 0.77 / 54 | 1.9% / 0.43 / 54 | 0.8% / 0.34 / 61 | 7.1% / 1.57 / 49 |
| 514 | -2.8% / -0.78 / 75 | 8.0% / 1.87 / 79 | -1.1% / -0.17 / 75 | 6.5% / 1.55 / 73 | 10.5% / 1.61 / 62 |
| 515 | -0.1% / -0.02 / 59 | -0.3% / -0.17 / 58 | 2.2% / 0.85 / 51 | 2.6% / 1.40 / 65 | 5.5% / 1.83 / 51 |
| 516 | 1.0% / 0.50 / 36 | -1.8% / -2.71 / 26 | 4.8% / 1.96 / 34 | 1.5% / 0.86 / 33 | 3.2% / 1.06 / 29 |
| 517 | 0.9% / 0.38 / 29 | -1.8% / -1.92 / 27 | 1.2% / 0.45 / 32 | 3.6% / 1.38 / 48 | 6.1% / 1.60 / 27 |
| 518 | -1.2% / -0.82 / 19 | 2.3% / 1.85 / 22 | 1.8% / 1.02 / 19 | 1.8% / 1.54 / 23 | 1.9% / 1.04 / 20 |
| 519 | -0.4% / -0.20 / 43 | 5.6% / 1.93 / 41 | 2.2% / 0.92 / 37 | 3.6% / 1.33 / 52 | 1.1% / 0.32 / 34 |
| 520 | 1.2% / 0.37 / 37 | -0.4% / -0.18 / 38 | 1.7% / 0.43 / 53 | 4.7% / 1.72 / 50 | 8.4% / 1.75 / 43 |
| 521 | 3.7% / 1.11 / 31 | 0.2% / 0.09 / 25 | -0.3% / -0.11 / 20 | 3.1% / 1.16 / 27 | 7.5% / 1.32 / 43 |
| 522 | -0.5% / -0.31 / 38 | 5.0% / 1.89 / 31 | -1.6% / -1.21 / 21 | 3.2% / 1.49 / 35 | 3.0% / 1.05 / 27 |
| 523 | 4.0% / 1.74 / 26 | 0.9% / 0.55 / 25 | 0.5% / 0.23 / 19 | 1.1% / 0.61 / 26 | 3.4% / 0.93 / 37 |
| 524 | 5.0% / 1.98 / 58 | -2.5% / -1.31 / 72 | 2.7% / 1.01 / 51 | -0.3% / -0.14 / 58 | 5.6% / 1.61 / 63 |
| 525 | -1.0% / -0.29 / 67 | 13.1% / 2.78 / 69 | 2.7% / 0.67 / 71 | -0.9% / -0.33 / 72 | 2.3% / 0.50 / 65 |
| 526 | 2.7% / 0.99 / 33 | 1.2% / 0.62 / 33 | 2.3% / 0.66 / 48 | 3.4% / 1.06 / 43 | 4.6% / 1.06 / 34 |
| 527 | -1.4% / -0.93 / 48 | 2.7% / 1.52 / 47 | 1.1% / 0.57 / 35 | 2.6% / 1.50 / 54 | 2.8% / 1.10 / 40 |
| 528 | -1.0% / -0.53 / 30 | -0.1% / -0.05 / 26 | 3.8% / 2.34 / 14 | 0.6% / 0.50 / 23 | 2.9% / 1.44 / 21 |
| 529 | 4.1% / 0.98 / 71 | -3.4% / -1.46 / 71 | 1.6% / 0.35 / 82 | 4.2% / 1.25 / 82 | 10.8% / 1.59 / 70 |
| 530 | 0.5% / 0.31 / 25 | 3.3% / 1.51 / 21 | 1.4% / 0.59 / 24 | 1.1% / 0.66 / 23 | 3.6% / 0.91 / 28 |
| 531 | 1.2% / 0.80 / 25 | 0.8% / 0.69 / 25 | 2.9% / 1.32 / 21 | 2.0% / 1.35 / 35 | -0.0% / 0.00 / 23 |
| 532 | -2.9% / -1.20 / 67 | 7.5% / 2.00 / 67 | 3.2% / 1.04 / 62 | 5.7% / 1.69 / 83 | 0.0% / 0.03 / 66 |
| 533 | -1.8% / -0.66 / 35 | 5.5% / 1.45 / 36 | 8.6% / 2.19 / 41 | 1.4% / 0.67 / 41 | -0.9% / -0.20 / 41 |
| 534 | 2.3% / 1.39 / 29 | -1.6% / -2.09 / 27 | -0.1% / -0.04 / 32 | 1.8% / 1.20 / 48 | 4.3% / 1.67 / 27 |
| 535 | 2.3% / 0.73 / 29 | -1.2% / -0.81 / 27 | -0.3% / -0.10 / 32 | 1.6% / 0.58 / 48 | 10.9% / 2.27 / 27 |
| 536 | -0.6% / -0.22 / 37 | 4.7% / 1.77 / 35 | 5.7% / 1.13 / 40 | 1.9% / 0.87 / 46 | 4.0% / 0.95 / 35 |
| 537 | 0.2% / 0.19 / 25 | 3.5% / 1.49 / 25 | 4.0% / 1.42 / 21 | 2.2% / 1.13 / 35 | -1.2% / -0.60 / 23 |
| 538 | 0.2% / 0.11 / 37 | 4.4% / 1.70 / 35 | 1.8% / 0.62 / 40 | 1.9% / 1.00 / 46 | 2.9% / 0.85 / 35 |
| 539 | -1.1% / -1.17 / 25 | 3.0% / 1.77 / 21 | 2.1% / 1.20 / 24 | -0.1% / -0.09 / 23 | 3.5% / 1.18 / 28 |
| 540 | 3.8% / 1.56 / 26 | 0.3% / 0.23 / 25 | 0.3% / 0.15 / 19 | 0.7% / 0.40 / 26 | 4.1% / 1.28 / 37 |
| 541 | -0.9% / -0.33 / 35 | 1.8% / 0.78 / 36 | 7.2% / 2.03 / 41 | 2.5% / 1.27 / 41 | 0.4% / 0.12 / 41 |
| 542 | 0.4% / 0.15 / 32 | 1.2% / 0.53 / 33 | 1.9% / 0.46 / 49 | 4.2% / 1.20 / 45 | 7.6% / 1.56 / 31 |
| 543 | -1.1% / -0.67 / 19 | 2.3% / 1.80 / 22 | 1.8% / 1.00 / 19 | 1.8% / 1.57 / 23 | 1.9% / 1.04 / 20 |
| 544 | -0.5% / -0.25 / 30 | 0.7% / 0.47 / 26 | 3.8% / 2.25 / 13 | -0.6% / -0.46 / 21 | 3.8% / 1.60 / 21 |
| 545 | 1.4% / 1.12 / 29 | -1.4% / -2.08 / 27 | -0.9% / -0.79 / 32 | 0.7% / 0.56 / 48 | 5.5% / 2.66 / 27 |
| 546 | -0.3% / -0.12 / 37 | 9.4% / 2.44 / 51 | 1.9% / 0.75 / 37 | 0.1% / 0.06 / 43 | -0.4% / -0.11 / 41 |
| 547 | 3.3% / 1.47 / 35 | -2.2% / -2.37 / 38 | 2.3% / 1.12 / 37 | 1.2% / 0.72 / 42 | 3.4% / 1.20 / 43 |
| 548 | -4.9% / -1.27 / 89 | 5.8% / 1.65 / 87 | 9.8% / 1.88 / 83 | 5.3% / 1.47 / 97 | 0.9% / 0.18 / 81 |
| 549 | -1.6% / -1.04 / 30 | 1.7% / 0.95 / 37 | 1.0% / 0.37 / 26 | 2.5% / 1.36 / 35 | 5.2% / 1.78 / 29 |
| 550 | 1.2% / 0.45 / 52 | 8.0% / 2.04 / 54 | 1.4% / 0.46 / 54 | 1.3% / 0.57 / 64 | 0.7% / 0.19 / 63 |
| 551 | 0.5% / 0.22 / 33 | 6.8% / 2.83 / 33 | 0.7% / 0.22 / 43 | 1.3% / 0.63 / 45 | 1.6% / 0.48 / 38 |
| 552 | -1.2% / -1.13 / 28 | 2.7% / 1.76 / 34 | 1.5% / 0.83 / 31 | 2.1% / 1.47 / 35 | 1.2% / 0.57 / 35 |
| 553 | 4.0% / 1.07 / 30 | -1.1% / -0.94 / 21 | 2.7% / 0.83 / 21 | 2.6% / 0.90 / 25 | 4.8% / 1.07 / 27 |
| 554 | 5.3% / 1.00 / 37 | -0.6% / -0.22 / 38 | -1.0% / -0.16 / 53 | 6.3% / 1.57 / 50 | 10.3% / 1.57 / 43 |
| 555 | 2.4% / 0.81 / 37 | -0.4% / -0.20 / 38 | 1.7% / 0.45 / 53 | 3.8% / 1.56 / 50 | 8.1% / 1.85 / 43 |
| 556 | -0.3% / -0.35 / 25 | 3.1% / 1.64 / 21 | 1.2% / 0.87 / 24 | 0.6% / 0.66 / 23 | 0.6% / 0.43 / 28 |
| 557 | 1.9% / 1.25 / 23 | 2.6% / 2.24 / 27 | 0.3% / 0.27 / 21 | 1.4% / 1.07 / 31 | -1.0% / -0.61 / 25 |
| 558 | -1.2% / -0.75 / 53 | 3.5% / 1.89 / 56 | 1.3% / 0.62 / 46 | 2.2% / 1.22 / 65 | 2.2% / 0.76 / 53 |
| 559 | 4.4% / 2.24 / 34 | -0.8% / -0.61 / 32 | -0.9% / -0.39 / 46 | 0.4% / 0.26 / 49 | 6.3% / 2.20 / 38 |
| 560 | -0.3% / -0.17 / 32 | 1.0% / 0.80 / 29 | 4.4% / 1.73 / 28 | 2.2% / 1.41 / 41 | 0.2% / 0.13 / 29 |
| 561 | 0.7% / 0.61 / 19 | 2.5% / 2.12 / 22 | -0.1% / -0.08 / 19 | 0.4% / 0.42 / 23 | 1.0% / 0.73 / 20 |
| 562 | 0.7% / 0.45 / 19 | 2.8% / 1.97 / 18 | 2.5% / 1.35 / 26 | 0.5% / 0.48 / 23 | 0.3% / 0.19 / 21 |
| 563 | 4.4% / 1.23 / 33 | 1.1% / 0.57 / 33 | 1.2% / 0.31 / 48 | 4.9% / 1.37 / 43 | 2.3% / 0.59 / 34 |
| 564 | 2.8% / 1.59 / 30 | -1.4% / -1.00 / 42 | 1.6% / 0.99 / 28 | -0.0% / -0.00 / 28 | 3.8% / 1.40 / 35 |
| 565 | 0.5% / 0.30 / 43 | 0.3% / 0.23 / 40 | 2.5% / 1.09 / 28 | 2.8% / 1.59 / 50 | 2.0% / 0.77 / 37 |
| 566 | 6.4% / 1.73 / 38 | 0.8% / 0.46 / 42 | -0.8% / -0.24 / 51 | 3.1% / 0.89 / 53 | 3.1% / 0.82 / 52 |
| 567 | 8.6% / 1.28 / 31 | -0.7% / -0.38 / 24 | -0.6% / -0.17 / 20 | 2.0% / 0.60 / 27 | 8.6% / 1.31 / 18 |
| 568 | 0.7% / 0.28 / 50 | 2.6% / 1.19 / 57 | 0.1% / 0.05 / 40 | 2.4% / 0.92 / 55 | 5.8% / 1.68 / 54 |
| 569 | 3.3% / 1.47 / 35 | -2.2% / -2.37 / 38 | 3.2% / 1.39 / 37 | 1.5% / 0.86 / 42 | 2.1% / 0.77 / 43 |
| 570 | 0.2% / 0.16 / 43 | 0.0% / 0.04 / 40 | 2.8% / 1.18 / 28 | 2.9% / 1.62 / 50 | 2.3% / 0.87 / 37 |
| 571 | 1.5% / 0.57 / 36 | -2.2% / -3.01 / 26 | 5.8% / 1.95 / 34 | 2.4% / 1.19 / 33 | 2.0% / 0.65 / 29 |
| 572 | 4.8% / 1.56 / 38 | 1.7% / 0.97 / 42 | 1.7% / 0.55 / 51 | 1.0% / 0.35 / 53 | 3.5% / 0.95 / 52 |
| 573 | 0.6% / 0.21 / 52 | 6.9% / 1.70 / 54 | 1.9% / 0.53 / 54 | 1.7% / 0.54 / 64 | 3.7% / 0.77 / 63 |
| 574 | 1.7% / 0.92 / 35 | -2.1% / -2.30 / 38 | 3.9% / 1.84 / 37 | 0.7% / 0.48 / 42 | 3.3% / 1.29 / 43 |
| 575 | 6.6% / 2.22 / 29 | -0.6% / -0.39 / 29 | 0.2% / 0.08 / 42 | -0.6% / -0.33 / 47 | 4.7% / 1.28 / 33 |
| 576 | 0.3% / 0.13 / 22 | 4.4% / 2.27 / 29 | 1.0% / 0.39 / 29 | 0.3% / 0.17 / 37 | 3.1% / 0.96 / 30 |
| 577 | 0.1% / 0.04 / 37 | 0.1% / 0.07 / 38 | 1.1% / 0.27 / 53 | 3.9% / 1.19 / 50 | 11.9% / 2.00 / 43 |
| 578 | 3.4% / 0.99 / 78 | 3.4% / 1.25 / 85 | -0.3% / -0.06 / 93 | 5.3% / 1.45 / 92 | 2.5% / 0.60 / 79 |
| 579 | -0.2% / -0.10 / 43 | 2.5% / 1.04 / 40 | 2.6% / 0.93 / 28 | 4.5% / 1.66 / 50 | 0.5% / 0.20 / 37 |
| 580 | 4.9% / 1.99 / 23 | -0.3% / -0.23 / 23 | 0.9% / 0.34 / 39 | 3.3% / 1.09 / 35 | 0.6% / 0.23 / 26 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_0045` | 3 | 0.92 | 0.96/0.96 | 0.85/0.86 |
| 1 | `cfg_42a1` | 4 | 0.88 | 0.92/0.94 | 0.70/0.85 |
| 2 | `cfg_58c2` | 5 | 0.81 | 0.82/0.90 | 0.46/0.69 |
| 3 | `cfg_5db4` | 6 | 0.80 | 0.87/0.93 | 0.48/0.70 |
| 4 | `cfg_a5e6` | 7 | 0.87 | 0.88/0.92 | 0.34/0.59 |
| 5 | `cfg_0b0e` | 4 | 0.89 | 0.91/0.94 | 0.74/0.79 |
| 6 | `cfg_020a` | 12 | 0.82 | 0.77/0.83 | 0.22/0.34 |
| 7 | `cfg_2dde` | 6 | 0.82 | 0.89/0.92 | 0.70/0.82 |
| 8 | `cfg_024e` | 3 | 0.88 | 0.78/0.79 | 0.63/0.63 |
| 9 | `cfg_148f` | 6 | 0.88 | 0.81/0.91 | 0.50/0.73 |
| 10 | `cfg_031f` | 4 | 0.92 | 0.91/1.00 | 0.66/1.00 |
| 11 | `cfg_20e1` | 3 | 0.84 | 0.82/0.86 | 0.62/0.66 |
| 12 | `cfg_0b4b` | 13 | 0.81 | 0.76/0.86 | 0.36/0.55 |
| 13 | `cfg_cb5f` | 7 | 0.81 | 0.75/0.85 | 0.47/0.62 |
| 14 | `cfg_8182` | 9 | 0.80 | 0.81/0.88 | 0.70/0.78 |
| 15 | `cfg_ff7f` | 5 | 0.84 | 0.83/0.87 | 0.45/0.61 |
| 16 | `cfg_387c` | 6 | 0.82 | 0.84/0.92 | 0.61/0.76 |
| 17 | `cfg_0561` | 3 | 0.94 | 0.95/0.95 | 0.80/0.83 |
| 18 | `cfg_1e90` | 8 | 0.88 | 0.90/0.93 | 0.71/0.80 |
| 19 | `cfg_90cc` | 6 | 0.84 | 0.85/0.94 | 0.49/0.68 |
| 20 | `cfg_0612` | 4 | 0.82 | 0.75/0.79 | 0.45/0.53 |
| 21 | `cfg_0658` | 2 | 0.97 | 0.97/0.97 | 0.88/0.88 |
| 22 | `cfg_9301` | 8 | 0.84 | 0.90/0.93 | 0.75/0.82 |
| 23 | `cfg_1061` | 4 | 0.87 | 0.83/0.90 | 0.48/0.55 |
| 24 | `cfg_b395` | 15 | 0.82 | 0.78/0.86 | 0.37/0.55 |
| 25 | `cfg_78ab` | 4 | 0.84 | 0.85/0.86 | 0.66/0.69 |
| 26 | `cfg_d2cb` | 10 | 0.81 | 0.81/0.87 | 0.40/0.52 |
| 27 | `cfg_3266` | 6 | 0.90 | 0.84/0.91 | 0.43/0.65 |
| 28 | `cfg_0815` | 2 | 0.87 | 0.89/0.89 | 0.65/0.65 |
| 29 | `cfg_df23` | 6 | 0.85 | 0.82/0.89 | 0.48/0.56 |
| 30 | `cfg_3982` | 8 | 0.82 | 0.78/0.84 | 0.31/0.46 |
| 31 | `cfg_0856` | 6 | 0.83 | 0.85/0.90 | 0.57/0.67 |
| 32 | `cfg_a544` | 6 | 0.88 | 0.88/0.93 | 0.78/0.86 |
| 33 | `cfg_faa5` | 3 | 0.92 | 0.95/0.98 | 0.82/0.90 |
| 34 | `cfg_7664` | 4 | 0.85 | 0.88/0.91 | 0.59/0.65 |
| 35 | `cfg_3566` | 3 | 0.99 | 0.99/0.99 | 0.85/0.87 |
| 36 | `cfg_b42f` | 2 | 0.89 | 0.87/0.87 | 0.70/0.70 |
| 37 | `cfg_d9ce` | 9 | 0.80 | 0.84/0.92 | 0.43/0.85 |
| 38 | `cfg_fa33` | 3 | 0.95 | 0.93/0.96 | 0.80/0.85 |
| 39 | `cfg_c0ff` | 3 | 0.91 | 0.91/0.94 | 0.65/0.73 |
| 40 | `cfg_0b17` | 3 | 0.97 | 0.97/0.99 | 0.95/0.97 |
| 41 | `cfg_0b2e` | 2 | 0.93 | 0.90/0.90 | 0.55/0.55 |
| 42 | `cfg_632d` | 12 | 0.84 | 0.83/0.86 | 0.32/0.47 |
| 43 | `cfg_0bb9` | 5 | 0.85 | 0.85/0.89 | 0.59/0.64 |
| 44 | `cfg_6745` | 8 | 0.87 | 0.85/0.93 | 0.67/0.81 |
| 45 | `cfg_b5b4` | 2 | 0.90 | 0.86/0.86 | 0.55/0.55 |
| 46 | `cfg_ec11` | 5 | 0.80 | 0.80/0.88 | 0.55/0.73 |
| 47 | `cfg_3bfd` | 5 | 0.81 | 0.87/0.91 | 0.66/0.74 |
| 48 | `cfg_7ea7` | 5 | 0.86 | 0.81/0.88 | 0.63/0.80 |
| 49 | `cfg_f8d5` | 4 | 0.84 | 0.88/0.93 | 0.63/0.73 |
| 50 | `cfg_4a9a` | 12 | 0.84 | 0.86/0.92 | 0.66/0.81 |
| 51 | `cfg_798e` | 7 | 0.84 | 0.75/0.88 | 0.59/0.77 |
| 52 | `cfg_a260` | 4 | 0.85 | 0.85/0.88 | 0.61/0.71 |
| 53 | `cfg_35a5` | 4 | 0.82 | 0.89/0.91 | 0.66/0.77 |
| 54 | `cfg_6263` | 9 | 0.82 | 0.78/0.87 | 0.40/0.51 |
| 55 | `cfg_6317` | 6 | 0.82 | 0.86/0.90 | 0.52/0.66 |
| 56 | `cfg_0e49` | 3 | 0.81 | 0.71/0.80 | 0.48/0.62 |
| 57 | `cfg_fbc4` | 3 | 0.93 | 0.90/0.90 | 0.44/0.49 |
| 58 | `cfg_1672` | 7 | 0.84 | 0.74/0.76 | 0.18/0.27 |
| 59 | `cfg_3bbe` | 2 | 0.95 | 0.94/0.94 | 0.89/0.89 |
| 60 | `cfg_bf97` | 8 | 0.88 | 0.86/0.92 | 0.56/0.76 |
| 61 | `cfg_6556` | 13 | 0.83 | 0.82/0.93 | 0.61/0.81 |
| 62 | `cfg_32de` | 3 | 0.91 | 0.85/0.90 | 0.54/0.60 |
| 63 | `cfg_f099` | 4 | 0.83 | 0.82/0.88 | 0.54/0.61 |
| 64 | `cfg_cb68` | 8 | 0.84 | 0.85/0.90 | 0.48/0.54 |
| 65 | `cfg_c4ff` | 3 | 0.86 | 0.90/0.94 | 0.64/0.74 |
| 66 | `cfg_a0b8` | 6 | 0.90 | 0.90/0.95 | 0.70/0.77 |
| 67 | `cfg_8d63` | 3 | 0.87 | 0.94/0.95 | 0.66/0.69 |
| 68 | `cfg_b6e1` | 6 | 0.88 | 0.88/0.94 | 0.73/0.87 |
| 69 | `cfg_f610` | 9 | 0.83 | 0.74/0.89 | 0.38/0.67 |
| 70 | `cfg_58c9` | 8 | 0.86 | 0.89/0.95 | 0.67/0.81 |
| 71 | `cfg_d8d3` | 7 | 0.84 | 0.85/0.90 | 0.63/0.76 |
| 72 | `cfg_1228` | 8 | 0.80 | 0.86/0.93 | 0.63/0.78 |
| 73 | `cfg_47c6` | 3 | 0.89 | 0.94/0.96 | 0.91/0.93 |
| 74 | `cfg_6e04` | 3 | 0.98 | 0.97/0.97 | 0.77/0.79 |
| 75 | `cfg_e38c` | 9 | 0.87 | 0.82/0.90 | 0.64/0.78 |
| 76 | `cfg_b223` | 4 | 0.83 | 0.86/0.97 | 0.58/0.87 |
| 77 | `cfg_2905` | 4 | 0.84 | 0.89/0.91 | 0.57/0.58 |
| 78 | `cfg_983e` | 9 | 0.83 | 0.76/0.88 | 0.38/0.74 |
| 79 | `cfg_5f2d` | 12 | 0.84 | 0.80/0.86 | 0.26/0.45 |
| 80 | `cfg_1428` | 2 | 0.92 | 0.91/0.91 | 0.74/0.74 |
| 81 | `cfg_2bd4` | 4 | 0.85 | 0.91/0.95 | 0.58/0.90 |
| 82 | `cfg_a2a3` | 6 | 0.86 | 0.88/0.93 | 0.77/0.85 |
| 83 | `cfg_d20a` | 10 | 0.82 | 0.80/0.92 | 0.34/0.69 |
| 84 | `cfg_14a1` | 2 | 0.88 | 0.90/0.90 | 0.72/0.72 |
| 85 | `cfg_936a` | 7 | 0.87 | 0.82/0.87 | 0.49/0.63 |
| 86 | `cfg_89ab` | 12 | 0.83 | 0.75/0.87 | 0.39/0.55 |
| 87 | `cfg_f1b7` | 3 | 0.84 | 0.89/0.92 | 0.77/0.81 |
| 88 | `cfg_db98` | 7 | 0.86 | 0.90/0.93 | 0.72/0.80 |
| 89 | `cfg_1aa1` | 4 | 0.83 | 0.87/0.89 | 0.68/0.71 |
| 90 | `cfg_78f7` | 6 | 0.85 | 0.89/0.93 | 0.74/0.84 |
| 91 | `cfg_1645` | 3 | 0.91 | 0.87/0.90 | 0.51/0.64 |
| 92 | `cfg_9be7` | 9 | 0.81 | 0.80/0.85 | 0.31/0.50 |
| 93 | `cfg_8d79` | 3 | 0.89 | 0.82/0.89 | 0.55/0.71 |
| 94 | `cfg_b9ec` | 6 | 0.84 | 0.85/0.90 | 0.52/0.57 |
| 95 | `cfg_9522` | 3 | 0.84 | 0.90/0.90 | 0.77/0.78 |
| 96 | `cfg_ecda` | 3 | 0.86 | 0.92/0.94 | 0.60/0.76 |
| 97 | `cfg_c073` | 12 | 0.85 | 0.80/0.91 | 0.25/0.60 |
| 98 | `cfg_8222` | 6 | 0.83 | 0.83/0.91 | 0.65/0.78 |
| 99 | `cfg_1960` | 2 | 0.92 | 0.90/0.90 | 0.75/0.75 |
| 100 | `cfg_4031` | 10 | 0.81 | 0.81/0.89 | 0.66/0.80 |
| 101 | `cfg_7f16` | 9 | 0.84 | 0.90/0.94 | 0.69/0.82 |
| 102 | `cfg_9a9f` | 16 | 0.81 | 0.75/0.86 | 0.22/0.51 |
| 103 | `cfg_19e3` | 5 | 0.85 | 0.85/0.90 | 0.51/0.58 |
| 104 | `cfg_704d` | 8 | 0.89 | 0.88/0.93 | 0.68/0.79 |
| 105 | `cfg_f691` | 5 | 0.85 | 0.86/0.90 | 0.60/0.72 |
| 106 | `cfg_1ada` | 2 | 0.93 | 0.92/0.92 | 0.65/0.65 |
| 107 | `cfg_8567` | 6 | 0.81 | 0.88/0.93 | 0.69/0.83 |
| 108 | `cfg_a800` | 9 | 0.81 | 0.86/0.90 | 0.44/0.54 |
| 109 | `cfg_1afd` | 7 | 0.84 | 0.82/0.90 | 0.41/0.56 |
| 110 | `cfg_ad4b` | 6 | 0.87 | 0.82/0.92 | 0.30/0.46 |
| 111 | `cfg_1ba2` | 4 | 0.88 | 0.82/0.94 | 0.59/0.84 |
| 112 | `cfg_9cd6` | 3 | 0.93 | 0.94/0.96 | 0.91/0.92 |
| 113 | `cfg_1be4` | 6 | 0.84 | 0.86/0.89 | 0.54/0.64 |
| 114 | `cfg_b788` | 4 | 0.80 | 0.88/0.88 | 0.58/0.61 |
| 115 | `cfg_9b97` | 4 | 0.88 | 0.94/0.94 | 0.70/0.75 |
| 116 | `cfg_eec0` | 6 | 0.83 | 0.82/0.88 | 0.67/0.80 |
| 117 | `cfg_c522` | 6 | 0.92 | 0.93/0.94 | 0.76/0.86 |
| 118 | `cfg_1cbe` | 4 | 0.89 | 0.84/0.89 | 0.49/0.56 |
| 119 | `cfg_1cbe` | 5 | 0.83 | 0.84/0.87 | 0.47/0.53 |
| 120 | `cfg_675a` | 4 | 0.85 | 0.87/0.93 | 0.54/0.84 |
| 121 | `cfg_b384` | 4 | 0.90 | 0.84/0.90 | 0.53/0.74 |
| 122 | `cfg_4cec` | 3 | 0.89 | 0.90/0.91 | 0.76/0.80 |
| 123 | `cfg_1d8d` | 4 | 0.87 | 0.87/0.92 | 0.51/0.66 |
| 124 | `cfg_8ac6` | 5 | 0.84 | 0.79/0.87 | 0.31/0.53 |
| 125 | `cfg_1dee` | 5 | 0.87 | 0.75/0.85 | 0.29/0.51 |
| 126 | `cfg_d91b` | 5 | 0.82 | 0.73/0.85 | 0.35/0.47 |
| 127 | `cfg_cee8` | 5 | 0.88 | 0.88/0.92 | 0.54/0.71 |
| 128 | `cfg_1f35` | 4 | 0.86 | 0.87/0.92 | 0.66/0.79 |
| 129 | `cfg_f160` | 8 | 0.84 | 0.78/0.85 | 0.42/0.55 |
| 130 | `cfg_ceea` | 6 | 0.80 | 0.85/0.87 | 0.58/0.69 |
| 131 | `cfg_782c` | 3 | 0.92 | 0.92/0.94 | 0.86/0.88 |
| 132 | `cfg_63af` | 2 | 0.98 | 0.97/0.97 | 0.90/0.90 |
| 133 | `cfg_20bc` | 5 | 0.90 | 0.93/0.96 | 0.75/0.83 |
| 134 | `cfg_8a21` | 7 | 0.84 | 0.88/0.92 | 0.60/0.73 |
| 135 | `cfg_72af` | 9 | 0.85 | 0.81/0.93 | 0.28/0.53 |
| 136 | `cfg_87f4` | 5 | 0.84 | 0.82/0.90 | 0.35/0.50 |
| 137 | `cfg_7ecf` | 6 | 0.84 | 0.90/0.94 | 0.63/0.72 |
| 138 | `cfg_21ae` | 4 | 0.91 | 0.91/0.95 | 0.69/0.76 |
| 139 | `cfg_41ed` | 6 | 0.82 | 0.86/0.92 | 0.52/0.57 |
| 140 | `cfg_8689` | 7 | 0.87 | 0.81/0.88 | 0.65/0.77 |
| 141 | `cfg_758b` | 3 | 0.85 | 0.91/0.94 | 0.77/0.84 |
| 142 | `cfg_43f5` | 4 | 0.90 | 0.91/0.92 | 0.54/0.54 |
| 143 | `cfg_5c8f` | 5 | 0.88 | 0.90/0.93 | 0.69/0.80 |
| 144 | `cfg_bd40` | 3 | 0.88 | 0.86/0.93 | 0.52/0.71 |
| 145 | `cfg_fbc8` | 3 | 0.92 | 0.95/0.96 | 0.87/0.87 |
| 146 | `cfg_243d` | 2 | 0.94 | 0.94/0.94 | 0.88/0.88 |
| 147 | `cfg_9b4a` | 2 | 0.92 | 0.96/0.96 | 0.84/0.84 |
| 148 | `cfg_248d` | 13 | 0.81 | 0.81/0.86 | 0.29/0.47 |
| 149 | `cfg_2584` | 1 | n/a | n/a/n/a | n/a/n/a |
| 150 | `cfg_258d` | 3 | 0.84 | 0.82/0.87 | 0.72/0.76 |
| 151 | `cfg_2a8b` | 5 | 0.81 | 0.84/0.88 | 0.69/0.77 |
| 152 | `cfg_b90a` | 4 | 0.91 | 0.86/0.86 | 0.35/0.45 |
| 153 | `cfg_506e` | 6 | 0.86 | 0.80/0.89 | 0.57/0.74 |
| 154 | `cfg_7304` | 6 | 0.85 | 0.78/0.84 | 0.31/0.39 |
| 155 | `cfg_adb1` | 5 | 0.92 | 0.95/0.96 | 0.71/0.82 |
| 156 | `cfg_312d` | 2 | 0.87 | 0.86/0.86 | 0.70/0.70 |
| 157 | `cfg_80fc` | 3 | 0.91 | 0.90/0.92 | 0.80/0.84 |
| 158 | `cfg_2c80` | 1 | n/a | n/a/n/a | n/a/n/a |
| 159 | `cfg_aafc` | 7 | 0.86 | 0.84/0.89 | 0.57/0.70 |
| 160 | `cfg_5e18` | 4 | 0.84 | 0.83/0.89 | 0.59/0.72 |
| 161 | `cfg_2ce0` | 6 | 0.86 | 0.87/0.91 | 0.48/0.59 |
| 162 | `cfg_7a46` | 2 | 0.92 | 0.89/0.89 | 0.54/0.54 |
| 163 | `cfg_e180` | 5 | 0.90 | 0.94/0.95 | 0.74/0.79 |
| 164 | `cfg_2e5b` | 3 | 0.88 | 0.85/0.89 | 0.76/0.83 |
| 165 | `cfg_869f` | 9 | 0.82 | 0.78/0.85 | 0.37/0.58 |
| 166 | `cfg_4955` | 6 | 0.82 | 0.80/0.86 | 0.47/0.57 |
| 167 | `cfg_2ef2` | 4 | 0.85 | 0.76/0.92 | 0.53/0.56 |
| 168 | `cfg_97e6` | 3 | 0.94 | 0.95/0.97 | 0.91/0.92 |
| 169 | `cfg_7022` | 3 | 0.89 | 0.94/0.95 | 0.80/0.84 |
| 170 | `cfg_306b` | 6 | 0.80 | 0.76/0.76 | 0.59/0.59 |
| 171 | `cfg_310f` | 4 | 0.90 | 0.83/0.90 | 0.38/0.73 |
| 172 | `cfg_680d` | 4 | 0.87 | 0.86/0.92 | 0.60/0.66 |
| 173 | `cfg_cd97` | 4 | 0.88 | 0.90/0.94 | 0.72/0.82 |
| 174 | `cfg_3194` | 3 | 0.80 | 0.82/0.86 | 0.32/0.44 |
| 175 | `cfg_31b3` | 3 | 0.94 | 0.93/0.95 | 0.85/0.88 |
| 176 | `cfg_dcd9` | 5 | 0.86 | 0.88/0.94 | 0.65/0.74 |
| 177 | `cfg_d3e2` | 4 | 0.85 | 0.87/0.94 | 0.60/0.74 |
| 178 | `cfg_333b` | 3 | 0.87 | 0.85/0.89 | 0.44/0.60 |
| 179 | `cfg_adad` | 6 | 0.89 | 0.87/0.92 | 0.74/0.81 |
| 180 | `cfg_35d2` | 2 | 0.96 | 0.96/0.96 | 0.71/0.71 |
| 181 | `cfg_36c6` | 4 | 0.90 | 0.91/0.94 | 0.62/0.69 |
| 182 | `cfg_36cb` | 3 | 0.93 | 0.92/0.94 | 0.82/0.84 |
| 183 | `cfg_73b8` | 4 | 0.90 | 0.87/0.93 | 0.60/0.69 |
| 184 | `cfg_d52d` | 6 | 0.88 | 0.89/0.95 | 0.67/0.75 |
| 185 | `cfg_f878` | 5 | 0.89 | 0.83/0.89 | 0.42/0.52 |
| 186 | `cfg_3ad9` | 6 | 0.82 | 0.86/0.90 | 0.58/0.71 |
| 187 | `cfg_e47d` | 5 | 0.88 | 0.84/0.91 | 0.55/0.73 |
| 188 | `cfg_3cc0` | 4 | 0.87 | 0.91/0.94 | 0.76/0.81 |
| 189 | `cfg_45e6` | 6 | 0.84 | 0.91/0.94 | 0.76/0.83 |
| 190 | `cfg_3d30` | 2 | 0.92 | 0.91/0.91 | 0.71/0.71 |
| 191 | `cfg_3dc2` | 6 | 0.82 | 0.86/0.91 | 0.50/0.56 |
| 192 | `cfg_ca39` | 11 | 0.81 | 0.80/0.90 | 0.39/0.61 |
| 193 | `cfg_a1d6` | 4 | 0.89 | 0.86/1.00 | 0.48/0.85 |
| 194 | `cfg_cfa4` | 3 | 0.90 | 0.93/0.94 | 0.72/0.78 |
| 195 | `cfg_758f` | 4 | 0.90 | 0.89/0.93 | 0.56/0.83 |
| 196 | `cfg_3fe4` | 3 | 0.81 | 0.83/0.89 | 0.56/0.72 |
| 197 | `cfg_8b86` | 9 | 0.83 | 0.82/0.91 | 0.44/0.63 |
| 198 | `cfg_407e` | 2 | 0.90 | 0.93/0.93 | 0.75/0.75 |
| 199 | `cfg_a559` | 6 | 0.80 | 0.86/0.92 | 0.49/0.56 |
| 200 | `cfg_413e` | 6 | 0.87 | 0.87/0.92 | 0.49/0.71 |
| 201 | `cfg_439a` | 6 | 0.82 | 0.71/0.76 | 0.30/0.45 |
| 202 | `cfg_7423` | 6 | 0.84 | 0.86/0.92 | 0.50/0.56 |
| 203 | `cfg_d56d` | 5 | 0.84 | 0.83/0.85 | 0.52/0.58 |
| 204 | `cfg_aab7` | 8 | 0.87 | 0.87/0.93 | 0.78/0.85 |
| 205 | `cfg_e42a` | 4 | 0.80 | 0.86/0.90 | 0.50/0.80 |
| 206 | `cfg_8763` | 3 | 0.89 | 0.95/0.96 | 0.79/0.86 |
| 207 | `cfg_6221` | 4 | 0.92 | 0.91/0.95 | 0.57/0.66 |
| 208 | `cfg_5629` | 2 | 0.97 | 0.98/0.98 | 0.84/0.84 |
| 209 | `cfg_d658` | 4 | 0.85 | 0.85/0.90 | 0.62/0.76 |
| 210 | `cfg_ce32` | 4 | 0.86 | 0.88/0.90 | 0.72/0.81 |
| 211 | `cfg_4901` | 3 | 1.00 | 0.99/0.99 | 0.98/0.99 |
| 212 | `cfg_4a2a` | 5 | 0.87 | 0.91/0.94 | 0.74/0.84 |
| 213 | `cfg_5cdc` | 7 | 0.84 | 0.82/0.87 | 0.41/0.52 |
| 214 | `cfg_4b4e` | 4 | 0.87 | 0.84/0.89 | 0.63/0.73 |
| 215 | `cfg_a340` | 4 | 0.90 | 0.88/0.90 | 0.36/0.47 |
| 216 | `cfg_4bf0` | 2 | 0.92 | 0.92/0.92 | 0.69/0.69 |
| 217 | `cfg_4cbc` | 2 | 0.92 | 0.85/0.85 | 0.59/0.59 |
| 218 | `cfg_9880` | 6 | 0.83 | 0.87/0.92 | 0.71/0.84 |
| 219 | `cfg_4e3b` | 2 | 0.92 | 0.94/0.94 | 0.82/0.82 |
| 220 | `cfg_91ea` | 3 | 0.85 | 0.88/0.89 | 0.57/0.67 |
| 221 | `cfg_506c` | 2 | 0.88 | 0.91/0.91 | 0.56/0.56 |
| 222 | `cfg_adb2` | 2 | 0.95 | 0.96/0.96 | 0.86/0.86 |
| 223 | `cfg_bb47` | 7 | 0.83 | 0.79/0.89 | 0.58/0.76 |
| 224 | `cfg_531f` | 2 | 1.00 | 1.00/1.00 | 0.78/0.78 |
| 225 | `cfg_53d5` | 1 | n/a | n/a/n/a | n/a/n/a |
| 226 | `cfg_a5bf` | 3 | 0.97 | 0.96/0.98 | 0.89/0.91 |
| 227 | `cfg_fc55` | 4 | 0.86 | 0.89/0.97 | 0.79/0.90 |
| 228 | `cfg_555e` | 3 | 0.98 | 0.98/0.99 | 0.90/0.93 |
| 229 | `cfg_90e7` | 2 | 0.96 | 0.97/0.97 | 0.87/0.87 |
| 230 | `cfg_56ed` | 4 | 0.92 | 0.91/0.95 | 0.59/0.72 |
| 231 | `cfg_c7bc` | 6 | 0.85 | 0.76/0.84 | 0.33/0.52 |
| 232 | `cfg_5915` | 2 | 0.94 | 0.94/0.94 | 0.85/0.85 |
| 233 | `cfg_5a0b` | 3 | 0.82 | 0.89/0.90 | 0.73/0.75 |
| 234 | `cfg_699b` | 7 | 0.83 | 0.86/0.96 | 0.51/0.91 |
| 235 | `cfg_d35b` | 4 | 0.90 | 0.85/0.90 | 0.44/0.55 |
| 236 | `cfg_f928` | 3 | 0.86 | 0.82/0.86 | 0.35/0.50 |
| 237 | `cfg_5d59` | 1 | n/a | n/a/n/a | n/a/n/a |
| 238 | `cfg_5d8a` | 1 | n/a | n/a/n/a | n/a/n/a |
| 239 | `cfg_5dcb` | 6 | 0.93 | 0.90/0.90 | 0.66/0.74 |
| 240 | `cfg_5de6` | 4 | 0.92 | 0.90/0.90 | 0.80/0.84 |
| 241 | `cfg_ce54` | 5 | 0.90 | 0.90/0.94 | 0.56/0.73 |
| 242 | `cfg_cdd7` | 4 | 0.94 | 0.90/0.90 | 0.77/0.77 |
| 243 | `cfg_c1e7` | 3 | 0.95 | 0.94/0.96 | 0.87/0.91 |
| 244 | `cfg_65d3` | 1 | n/a | n/a/n/a | n/a/n/a |
| 245 | `cfg_66c4` | 1 | n/a | n/a/n/a | n/a/n/a |
| 246 | `cfg_7d0d` | 2 | 0.92 | 0.89/0.89 | 0.52/0.52 |
| 247 | `cfg_6765` | 3 | 0.92 | 0.94/0.97 | 0.85/0.90 |
| 248 | `cfg_68b4` | 3 | 0.90 | 0.95/0.96 | 0.84/0.86 |
| 249 | `cfg_6999` | 1 | n/a | n/a/n/a | n/a/n/a |
| 250 | `cfg_96c2` | 6 | 0.82 | 0.75/0.85 | 0.46/0.59 |
| 251 | `cfg_be38` | 2 | 0.88 | 0.90/0.90 | 0.56/0.56 |
| 252 | `cfg_7ca1` | 3 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 253 | `cfg_6faf` | 1 | n/a | n/a/n/a | n/a/n/a |
| 254 | `cfg_c23c` | 4 | 0.87 | 0.90/0.91 | 0.58/0.75 |
| 255 | `cfg_75b0` | 1 | n/a | n/a/n/a | n/a/n/a |
| 256 | `cfg_8102` | 2 | 0.91 | 0.92/0.92 | 0.79/0.79 |
| 257 | `cfg_e936` | 4 | 0.85 | 0.91/0.95 | 0.75/0.81 |
| 258 | `cfg_7b61` | 2 | 0.83 | 0.87/0.87 | 0.75/0.75 |
| 259 | `cfg_7ecf` | 1 | n/a | n/a/n/a | n/a/n/a |
| 260 | `cfg_8794` | 5 | 0.88 | 0.86/0.88 | 0.57/0.63 |
| 261 | `cfg_c668` | 2 | 0.91 | 0.93/0.93 | 0.75/0.75 |
| 262 | `cfg_86ae` | 3 | 0.89 | 0.88/0.90 | 0.59/0.66 |
| 263 | `cfg_b654` | 5 | 0.86 | 0.87/0.93 | 0.62/0.82 |
| 264 | `cfg_a3b3` | 2 | 0.91 | 0.84/0.84 | 0.59/0.59 |
| 265 | `cfg_c55a` | 3 | 0.86 | 0.83/0.86 | 0.39/0.40 |
| 266 | `cfg_8a73` | 4 | 0.90 | 0.89/0.94 | 0.69/0.80 |
| 267 | `cfg_ca4d` | 3 | 0.97 | 0.97/0.97 | 0.94/0.94 |
| 268 | `cfg_abc9` | 2 | 0.91 | 0.92/0.92 | 0.82/0.82 |
| 269 | `cfg_90fc` | 2 | 0.95 | 0.97/0.97 | 0.80/0.80 |
| 270 | `cfg_9295` | 4 | 0.86 | 0.86/0.91 | 0.52/0.87 |
| 271 | `cfg_bc2b` | 2 | 0.91 | 0.87/0.87 | 0.53/0.53 |
| 272 | `cfg_b8d7` | 2 | 0.97 | 0.98/0.98 | 0.77/0.77 |
| 273 | `cfg_fad8` | 4 | 0.92 | 0.90/0.95 | 0.70/0.81 |
| 274 | `cfg_9bee` | 3 | 0.95 | 0.96/0.97 | 0.86/0.91 |
| 275 | `cfg_e2ad` | 2 | 0.85 | 0.91/0.91 | 0.90/0.90 |
| 276 | `cfg_e627` | 2 | 0.89 | 0.85/0.85 | 0.79/0.79 |
| 277 | `cfg_e690` | 2 | 0.92 | 0.89/0.89 | 0.51/0.51 |
| 278 | `cfg_b78f` | 3 | 0.87 | 0.94/0.95 | 0.87/0.87 |
| 279 | `cfg_de5a` | 3 | 0.92 | 0.92/0.95 | 0.83/0.88 |
| 280 | `cfg_a548` | 3 | 0.95 | 0.94/0.95 | 0.85/0.87 |
| 281 | `cfg_d70a` | 2 | 0.96 | 0.97/0.97 | 0.86/0.86 |
| 282 | `cfg_a938` | 2 | 0.90 | 0.88/0.88 | 0.68/0.68 |
| 283 | `cfg_aee1` | 1 | n/a | n/a/n/a | n/a/n/a |
| 284 | `cfg_bbd4` | 2 | 0.83 | 0.70/0.70 | 0.47/0.47 |
| 285 | `cfg_ef9e` | 3 | 0.93 | 0.89/0.91 | 0.75/0.79 |
| 286 | `cfg_d144` | 3 | 0.95 | 0.94/0.96 | 0.86/0.88 |
| 287 | `cfg_ccad` | 3 | 0.94 | 0.94/0.96 | 0.58/0.67 |
| 288 | `cfg_cbc7` | 2 | 0.88 | 0.88/0.88 | 0.56/0.56 |
| 289 | `cfg_fa75` | 2 | 0.86 | 0.91/0.91 | 0.76/0.76 |
| 290 | `cfg_fc5c` | 3 | 0.92 | 0.95/0.96 | 0.86/0.88 |
| 291 | `cfg_d6a1` | 1 | n/a | n/a/n/a | n/a/n/a |
| 292 | `cfg_d710` | 1 | n/a | n/a/n/a | n/a/n/a |
| 293 | `cfg_da66` | 1 | n/a | n/a/n/a | n/a/n/a |
| 294 | `cfg_dd13` | 1 | n/a | n/a/n/a | n/a/n/a |
| 295 | `cfg_dd21` | 1 | n/a | n/a/n/a | n/a/n/a |
| 296 | `cfg_edd6` | 1 | n/a | n/a/n/a | n/a/n/a |
| 297 | `cfg_fbac` | 2 | 0.86 | 0.90/0.90 | 0.70/0.70 |
| 298 | `cfg_f817` | 1 | n/a | n/a/n/a | n/a/n/a |
| 299 | `cfg_f995` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 9.874e-04 over 24300 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1364.0, participation ratio 59.1, 95%-variance components 409 (rank bound T = 1290); raw grid 24300; raw + known prior 337828
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

- Bars: the full Globex 1-minute bars are loaded only to measure the pre-open ranges (os_day_bars); trading uses 1-minute bars with NY open time in [09:30, 16:00) on their own session date. Each NY date is one session and no position can be held overnight.
- Levels per session date D: onh = 18:00 (D-1) to 09:30; asia = 20:00 to 00:00 (D-1 evening); lon = 02:00-05:00; box = 08:00-09:30; each needs bars for >= 50% of its minutes. pdr = the previous RTH session's high/low. Every pre-open level is recomputed from the raw Globex bars with plain loops (check_levels) and must match exactly.
- dATR = mean RTH high-low range of the previous 14 sessions; the 09:30 open must come from a bar opening by 09:32.
- Trigger (high side; the low side mirrors it): only if the 09:30 open is at or below H; p = first bar opening before 09:30 + window with high > H + pen x dATR. fade: first close < H within `confirm` bars from p (p counts, all in the window) -> short; cont: `confirm` consecutive closes > H from p, all in the window -> long. side=both takes the earlier trigger; a same-bar tie trades nothing. Recomputed with plain loops in the per-config integrity check.
- Entry at the OPEN of the bar after the trigger (opening within 2 minutes of it, same session) with market slippage.
- Stop: struct = beyond the extreme of bars p..t by 2 ticks; dX = X x dATR; never closer than 0.03 x dATR; live intrabar from the entry bar, filled at the worse of the bar's open and the stop with stop slippage. Target: R x the stop distance, or the opposite side of the range (fade) / one range height beyond the broken level (cont); a limit filled at the target only when a bar trades 1 tick through it; a bar touching both is a stop. A range target on the wrong side of the entry skips the trade.
- Time exit at the CLOSE of the last bar opening before the exit time with market slippage; a 16:00 exit is the session's last bar.
- One trade per session; sizing is the other families' (as many whole contracts as equity covers at full contract value, unlevered, compounding).
- Development backtests run on data physically truncated at the development end; the final session's trade is closed at the last development bar and flagged forced (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC). Log returns use back-adjusted prices; the adjustment is constant within a session, so 1-minute returns are distorted only by the level shift (tiny for ES).
- Session: each root's day session only (src/data/futures.py SESSIONS), on NYSE trading days; overnight Globex bars are not traded or used in any statistic.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side plus commission per contract per side, from the execution YAML; cost stress scales both. ES ticks are 0.25 point ($12.50), NQ 0.25 point ($5.00).
- Session: trades only 09:30-16:00 ET of each NY date; Globex bars before 09:30 (from 18:00 the evening before) are read only to measure the pre-open ranges. Databento rolls at 00:00 UTC, inside the overnight session; ranges use back-adjusted prices, so they stay comparable across the roll.

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- ICT never published rules; every definition here (level windows, penetration, reclaim, stop and target) is one fixed reading of community sources, chosen before the run (reports/ICT strategies to backtest.md). Each such choice is a hidden trial not counted in the grid.
- Target fills assume a resting limit is filled at the target once a bar trades a tick through it; cost stress scales slippage on market and stop fills only, not on target fills.
- Bars carry no intrabar order: a bar touching both stop and target counts as a stop (stop_first), which understates target-heavy configs.
- Databento ohlcv-1m has no bar for a minute without trades; overnight ranges can be thin on holidays (a level needs >= 50% minute coverage).
- No placebo-level control runs inside the funnel; scripts/run_os_placebo_benchmark.py runs it on the finalists afterwards.
- Sizing ignores volatility and stop distance (full equity per trade, as in the other families).
