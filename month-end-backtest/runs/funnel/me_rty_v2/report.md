# Screening funnel -- me_rty_v2 (development stages only)

- Code: `d7cd024716c8` (dirty working tree: True, diff sha256 `cb637a176976`)
- Config: `configs/funnel/me_funnel_rty_v2.yaml` sha256 `2da17adc133bac0b`; seed 20261123
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'RTY': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `33383339084e77b9` (65 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- Diagnostic run (development only). RTY 2023-2024 was already scored for ES pick #7 with unchanged rules, and other families were selected there.
- Holdout 2025+ previously inspected: **True** -- RTY 2025+ was already scored for ES pick #7 (unchanged-rules check, 2026-11-22) and for the combined #7 page. This run never reads it.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 4864 | 4864 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 4864 | 4864 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 4864 | 4352 | 512 | 0 |  | 0 | 89.47 | 89.47 |  |
| 3 performance & risk | hard_gate | 4352 | 130 | 4222 | 0 |  | 0 | 2.67 | 2.99 |  |
| 4 parameter stability | hard_gate | 130 | 125 | 5 | 0 |  | 0 | 2.57 | 96.15 |  |
| 5 time stability | hard_gate | 125 | 120 | 5 | 0 |  | 95 | 2.47 | 96.00 |  |
| 6 deduplication | dedup | 120 | 65 |  |  | 55 |  | 1.34 | 54.17 | best 2 per cluster |
| 7 execution stress | hard_gate | 65 | 65 | 0 | 0 |  | 0 | 1.34 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 65 |  |  |  |  |  |  |  | diagnostic only: unverified: 65 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 512 |
| s3:hard_reject:max_drawdown | 4 |
| s3:hard_reject:net_return | 2539 |
| s3:hard_reject:sharpe | 4222 |
| s4:hard_reject:local_median_sharpe | 5 |
| s5:hard_reject:profitable_years | 5 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_d615` | timeframe=1min, window=0, first_days=2, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 100/1/14 | 115 | 27.0% | 4.8% | 1.27 | -3.7% | 193 | 2.06 | 4.8% | 50.6 | 8/8 | 1.00 | 0.94 | 0.33 | 5 | 16.5% | 0.36 | 0.40 | 26.1% | 24.8% | 27.4% | 24.5%/21.0% | 13.4 (interpolated) | pass | 0.479 (unverified) | 0.44 |
| 2 | `cfg_9ec2` | timeframe=1min, window=0, first_days=3, entry=12:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 88/2/83 | 173 | 20.3% | 3.7% | 1.24 | -3.5% | 150 | 1.72 | 3.9% | 76.6 | 6/6 | 1.00 | 0.96 | 0.28 | 5 | 12.8% | 0.33 | 0.45 | 18.7% | 17.2% | 21.5% | 18.7%/15.4% | 7.4 (interpolated) | pass | 0.445 (unverified) | 0.94 |
| 3 | `cfg_2950` | timeframe=1min, window=0, first_days=2, entry=12:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 85/1/29 | 115 | 19.2% | 3.5% | 1.23 | -2.8% | 172 | 1.90 | 3.4% | 50.7 | 8/8 | 1.00 | 1.03 | 0.20 | 5 | 12.9% | 0.33 | 0.42 | 17.8% | 16.9% | 20.1% | 16.9%/14.1% | 10.0 (interpolated) | pass | 0.436 (unverified) | 0.63 |
| 4 | `cfg_d50a` | timeframe=1min, window=0, first_days=3, entry=12:00, exit=16:00, event_filter=none, stop=0.50 | 127/2/51 | 180 | 26.2% | 4.6% | 1.19 | -4.1% | 131 | 1.68 | 5.3% | 79.4 | 7/7 | 1.00 | 0.93 | 0.26 | 5 | 16.8% | 0.36 | 0.48 | 24.2% | 22.2% | 27.8% | 23.7%/19.8% | 8.7 (interpolated) | pass | 0.394 (unverified) | 0.66 |
| 5 | `cfg_400f` | timeframe=1min, window=0, first_days=3, entry=12:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 123/2/48 | 173 | 22.6% | 4.1% | 1.17 | -4.1% | 131 | 1.62 | 5.1% | 76.4 | 7/7 | 1.00 | 0.97 | 0.21 | 5 | 15.0% | 0.29 | 0.40 | 21.0% | 19.3% | 24.2% | 20.4%/17.1% | 8.1 (interpolated) | pass | 0.382 (unverified) | 0.64 |
| 6 | `cfg_0214` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 109/0/5 | 114 | 16.3% | 3.0% | 1.16 | -2.5% | 239 | 1.99 | 2.0% | 49.9 | 8/8 | 1.00 | 0.86 | 0.29 | 4 | 8.4% | 0.48 | 0.48 | 14.8% | 13.7% | 17.6% | 14.0%/11.4% | 8.8 (interpolated) | pass | 0.378 (unverified) | 1.31 |
| 7 | `cfg_dcce` | timeframe=1min, window=0, first_days=2, entry=12:00, exit=15:00, event_filter=skip_fomc, stop=0.50 | 91/1/23 | 115 | 14.3% | 2.6% | 1.10 | -4.5% | 430 | 1.80 | 2.7% | 50.8 | 9/9 | 0.89 | 0.87 | 0.23 | 4 | 8.0% | 0.44 | 0.46 | 13.1% | 11.7% | 15.6% | 12.9%/11.0% | 7.9 (interpolated) | pass | 0.316 (unverified) | 0.38 |
| 8 | `cfg_7655` | timeframe=1min, window=0, first_days=3, entry=12:00, exit=15:00, event_filter=none, stop=0.50 | 140/2/38 | 180 | 20.0% | 3.6% | 1.15 | -3.8% | 389 | 1.64 | 4.1% | 79.2 | 8/8 | 1.00 | 0.67 | 0.47 | 4 | 10.9% | 0.46 | 0.44 | 18.4% | 16.6% | 21.8% | 18.1%/15.3% | 7.0 (interpolated) | pass | 0.357 (unverified) | 0.54 |
| 9 | `cfg_0717` | timeframe=1min, window=0, first_days=2, entry=12:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 103/1/11 | 115 | 21.9% | 3.9% | 1.25 | -4.4% | 303 | 2.01 | 3.8% | 50.7 | 8/8 | 1.00 | 0.93 | 0.32 | 5 | 13.5% | 0.38 | 0.37 | 20.8% | 19.5% | 25.8% | 19.3%/16.7% | 11.3 (interpolated) | pass | 0.463 (unverified) | 0.40 |
| 10 | `cfg_b923` | timeframe=1min, window=0, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 147/2/24 | 173 | 29.7% | 5.2% | 1.12 | -6.4% | 153 | 1.62 | 7.1% | 76.2 | 7/7 | 1.00 | 0.83 | 0.29 | 5 | 20.9% | 0.28 | 0.41 | 28.1% | 26.2% | 29.4% | 26.4%/21.9% | 9.8 (interpolated) | pass | 0.340 (unverified) | 0.47 |
| 11 | `cfg_ae0c` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=15:00, event_filter=none, stop=1.00 | 314/5/41 | 360 | 37.2% | 6.4% | 1.05 | -6.2% | 305 | 1.40 | 12.1% | 158.3 | 9/9 | 1.00 | 0.77 | 0.28 | 4 | 22.1% | 0.41 | 0.36 | 33.5% | 29.0% | 35.3% | 33.2%/27.3% | 6.2 (interpolated) | pass | 0.280 (unverified) | 0.48 |
| 12 | `cfg_f52b` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=none | 114/0/0 | 114 | 18.9% | 3.4% | 1.31 | -2.5% | 214 | 2.23 | 2.0% | 50.2 | 7/7 | 1.00 | 0.89 | 0.42 | 4 | 10.2% | 0.46 | 0.43 | 17.9% | 16.8% | 19.3% | 17.2%/14.5% | 10.2 (interpolated) | pass | 0.516 (unverified) | 1.30 |
| 13 | `cfg_0267` | timeframe=1min, window=0, first_days=2, entry=12:00, exit=15:00, event_filter=skip_fomc, stop=0.25 | 64/1/50 | 115 | 11.9% | 2.2% | 1.04 | -4.1% | 515 | 1.74 | 2.0% | 50.7 | 8/8 | 1.00 | 0.77 | 0.27 | 4 | 7.4% | 0.38 | 0.54 | 10.9% | 9.9% | 13.4% | 10.9%/8.9% | 6.9 (interpolated) | pass | 0.258 (unverified) | 0.56 |
| 14 | `cfg_7f87` | timeframe=1min, window=0, first_days=3, entry=12:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 151/2/20 | 173 | 21.1% | 3.8% | 0.97 | -4.5% | 152 | 1.52 | 5.8% | 76.4 | 7/7 | 1.00 | 0.69 | 0.28 | 5 | 14.6% | 0.31 | 0.43 | 19.6% | 17.7% | 24.8% | 18.7%/14.5% | 7.6 (interpolated) | pass | 0.239 (unverified) | 0.35 |
| 15 | `cfg_dd38` | timeframe=1min, window=0, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=1.00 | 152/2/26 | 180 | 30.6% | 5.3% | 1.08 | -6.3% | 153 | 1.60 | 7.4% | 79.3 | 7/7 | 1.00 | 0.72 | 0.36 | 5 | 21.2% | 0.31 | 0.46 | 28.3% | 26.5% | 29.6% | 27.2%/21.2% | 9.6 (interpolated) | pass | 0.305 (unverified) | 0.40 |
| 16 | `cfg_d81b` | timeframe=1min, window=2, first_days=2, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 197/3/30 | 230 | 35.9% | 6.2% | 1.12 | -6.1% | 257 | 1.58 | 9.5% | 101.2 | 9/9 | 1.00 | 0.88 | 0.24 | 4 | 13.4% | 0.63 | 0.41 | 34.2% | 31.9% | 33.4% | 32.0%/26.4% | 9.2 (interpolated) | pass | 0.342 (unverified) | 0.59 |
| 17 | `cfg_4ee1` | timeframe=1min, window=0, first_days=2, entry=12:00, exit=16:00, event_filter=none, stop=0.25 | 62/1/57 | 120 | 15.1% | 2.8% | 1.13 | -3.7% | 325 | 1.81 | 2.7% | 52.8 | 7/7 | 1.00 | 0.92 | 0.21 | 4 | 9.6% | 0.33 | 0.52 | 14.0% | 12.8% | 16.8% | 13.6%/11.5% | 7.9 (interpolated) | pass | 0.329 (unverified) | 0.55 |
| 18 | `cfg_217c` | timeframe=1min, window=2, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=1.00 | 253/4/43 | 300 | 39.8% | 6.8% | 1.05 | -7.3% | 241 | 1.44 | 12.4% | 132.0 | 8/8 | 1.00 | 0.74 | 0.31 | 5 | 16.6% | 0.58 | 0.42 | 35.5% | 33.2% | 35.0% | 35.0%/27.9% | 7.6 (interpolated) | pass | 0.284 (unverified) | 0.56 |
| 19 | `cfg_95b1` | timeframe=1min, window=0, first_days=2, entry=11:00, exit=16:00, event_filter=none, stop=1.00 | 103/1/16 | 120 | 23.4% | 4.2% | 1.10 | -4.7% | 384 | 1.82 | 4.9% | 52.7 | 8/8 | 1.00 | 0.77 | 0.33 | 4 | 13.2% | 0.41 | 0.45 | 22.2% | 21.1% | 23.6% | 20.7%/16.7% | 11.1 (interpolated) | pass | 0.320 (unverified) | 0.22 |
| 20 | `cfg_806d` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 95/0/19 | 114 | 15.2% | 2.8% | 1.21 | -2.1% | 259 | 1.98 | 1.9% | 50.0 | 8/8 | 1.00 | 0.87 | 0.34 | 5 | 7.8% | 0.49 | 0.48 | 14.1% | 13.0% | 14.9% | 14.4%/11.5% | 8.4 (interpolated) | pass | 0.423 (unverified) | 0.82 |
| 21 | `cfg_4a86` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=15:00, event_filter=skip_fomc, stop=1.00 | 299/5/37 | 341 | 32.4% | 5.6% | 0.97 | -5.8% | 215 | 1.37 | 11.4% | 150.2 | 9/9 | 1.00 | 0.74 | 0.23 | 4 | 19.7% | 0.39 | 0.40 | 28.8% | 25.2% | 31.0% | 28.9%/22.7% | 5.9 (interpolated) | pass | 0.225 (unverified) | 0.48 |
| 22 | `cfg_20de` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 289/5/47 | 341 | 38.0% | 6.5% | 0.95 | -6.2% | 259 | 1.36 | 14.1% | 150.0 | 8/8 | 1.00 | 0.72 | 0.23 | 4 | 17.4% | 0.54 | 0.46 | 34.1% | 29.7% | 32.3% | 34.0%/27.2% | 6.7 (interpolated) | pass | 0.207 (unverified) | 0.66 |
| 23 | `cfg_a5bf` | timeframe=1min, window=2, first_days=3, entry=11:00, exit=15:00, event_filter=none, stop=1.00 | 262/4/34 | 300 | 30.0% | 5.3% | 0.97 | -6.8% | 369 | 1.40 | 10.1% | 132.1 | 9/9 | 1.00 | 0.70 | 0.27 | 4 | 17.0% | 0.44 | 0.41 | 26.3% | 23.5% | 28.8% | 28.1%/21.8% | 6.1 (interpolated) | pass | 0.229 (unverified) | 0.53 |
| 24 | `cfg_0486` | timeframe=1min, window=2, first_days=3, entry=11:00, exit=15:00, event_filter=skip_fomc, stop=1.00 | 253/4/31 | 288 | 27.9% | 4.9% | 0.95 | -7.5% | 197 | 1.40 | 9.7% | 126.9 | 9/9 | 1.00 | 0.69 | 0.27 | 4 | 16.0% | 0.42 | 0.42 | 24.2% | 21.9% | 25.9% | 24.2%/18.7% | 6.0 (interpolated) | pass | 0.216 (unverified) | 0.52 |
| 25 | `cfg_3b84` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=1.00 | 304/5/51 | 360 | 39.7% | 6.7% | 0.95 | -5.8% | 259 | 1.36 | 14.8% | 158.6 | 8/8 | 1.00 | 0.68 | 0.27 | 4 | 14.7% | 0.63 | 0.46 | 35.9% | 32.6% | 34.4% | 36.1%/28.4% | 6.6 (interpolated) | pass | 0.204 (unverified) | 0.47 |
| 26 | `cfg_7ec0` | timeframe=1min, window=0, first_days=3, entry=12:00, exit=16:00, event_filter=none, stop=1.00 | 156/2/22 | 180 | 22.5% | 4.0% | 0.93 | -5.4% | 325 | 1.51 | 6.0% | 79.2 | 7/7 | 1.00 | 0.71 | 0.22 | 5 | 12.9% | 0.42 | 0.53 | 20.3% | 18.7% | 26.7% | 20.7%/17.1% | 7.7 (interpolated) | pass | 0.201 (unverified) | 0.31 |
| 27 | `cfg_bdf0` | timeframe=1min, window=3, first_days=2, entry=11:00, exit=15:00, event_filter=skip_fomc, stop=1.00 | 249/4/30 | 283 | 28.3% | 5.0% | 0.94 | -7.0% | 348 | 1.43 | 9.5% | 124.2 | 10/10 | 1.00 | 0.66 | 0.29 | 3 | 14.8% | 0.48 | 0.43 | 25.6% | 22.0% | 27.2% | 25.0%/20.0% | 6.3 (interpolated) | pass | 0.205 (unverified) | 0.39 |
| 28 | `cfg_70ba` | timeframe=1min, window=3, first_days=2, entry=11:00, exit=15:00, event_filter=none, stop=1.00 | 262/4/34 | 300 | 29.5% | 5.2% | 0.94 | -8.4% | 327 | 1.41 | 10.1% | 131.3 | 10/10 | 1.00 | 0.67 | 0.28 | 3 | 16.1% | 0.45 | 0.42 | 26.3% | 23.6% | 28.2% | 27.2%/20.0% | 6.2 (interpolated) | pass | 0.203 (unverified) | 0.29 |
| 29 | `cfg_3ddd` | timeframe=1min, window=0, first_days=2, entry=11:00, exit=15:30, event_filter=skip_fomc, stop=1.00 | 102/1/12 | 115 | 20.6% | 3.7% | 1.10 | -6.1% | 559 | 1.91 | 4.3% | 50.6 | 9/9 | 1.00 | 0.78 | 0.33 | 4 | 10.3% | 0.47 | 0.44 | 19.0% | 18.2% | 20.1% | 18.5%/14.6% | 10.6 (interpolated) | pass | 0.326 (unverified) | 0.18 |
| 30 | `cfg_e2b0` | timeframe=1min, window=0, first_days=2, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 73/1/41 | 115 | 18.7% | 3.4% | 1.00 | -5.5% | 621 | 1.70 | 3.7% | 50.4 | 8/8 | 1.00 | 0.74 | 0.25 | 4 | 8.4% | 0.53 | 0.54 | 17.6% | 16.6% | 17.5% | 17.3%/13.5% | 9.9 (interpolated) | pass | 0.223 (unverified) | 0.68 |
| 31 | `cfg_50f9` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=15:00, event_filter=skip_fomc, stop=none | 114/0/0 | 114 | 8.2% | 1.6% | 1.10 | -3.3% | 539 | 1.87 | 1.0% | 50.5 | 6/8 | 1.00 | 0.69 | 0.42 | 4 | 3.4% | 0.58 | 0.41 | 7.1% | 6.0% | 8.5% | 7.3%/6.0% | 5.1 (interpolated) | pass | 0.354 (unverified) | 0.93 |
| 32 | `cfg_3086` | timeframe=1min, window=2, first_days=2, entry=11:00, exit=15:00, event_filter=skip_fomc, stop=1.00 | 203/3/24 | 230 | 23.6% | 4.2% | 0.92 | -9.3% | 474 | 1.46 | 7.7% | 101.4 | 10/10 | 1.00 | 0.65 | 0.27 | 4 | 11.5% | 0.51 | 0.47 | 21.3% | 19.1% | 22.8% | 21.2%/16.4% | 6.5 (interpolated) | pass | 0.195 (unverified) | 0.41 |
| 33 | `cfg_8c68` | timeframe=1min, window=0, first_days=2, entry=12:00, exit=16:00, event_filter=none, stop=1.00 | 106/1/13 | 120 | 18.2% | 3.3% | 1.01 | -5.6% | 345 | 1.72 | 4.0% | 52.8 | 8/8 | 1.00 | 0.73 | 0.28 | 4 | 11.3% | 0.38 | 0.44 | 17.2% | 15.9% | 21.9% | 16.6%/13.3% | 9.2 (interpolated) | pass | 0.266 (unverified) | 0.15 |
| 34 | `cfg_c78f` | timeframe=1min, window=0, first_days=2, entry=13:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 85/1/29 | 115 | 13.5% | 2.5% | 0.96 | -2.4% | 153 | 1.66 | 2.6% | 50.6 | 8/8 | 1.00 | 0.77 | 0.19 | 5 | 8.4% | 0.38 | 0.59 | 12.5% | 11.4% | 13.2% | 12.2%/9.3% | 7.5 (interpolated) | pass | 0.211 (unverified) | 0.52 |
| 35 | `cfg_3102` | timeframe=1min, window=0, first_days=2, entry=11:00, exit=15:00, event_filter=skip_fomc, stop=1.00 | 103/1/11 | 115 | 17.9% | 3.3% | 1.05 | -7.6% | 621 | 1.84 | 3.9% | 50.5 | 9/9 | 1.00 | 0.63 | 0.41 | 4 | 6.7% | 0.58 | 0.44 | 16.8% | 15.8% | 18.1% | 15.8%/12.7% | 9.4 (interpolated) | pass | 0.283 (unverified) | 0.08 |
| 36 | `cfg_8642` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=16:00, event_filter=none, stop=0.50 | 97/0/22 | 119 | 13.2% | 2.4% | 1.03 | -2.6% | 323 | 1.75 | 1.9% | 52.2 | 8/8 | 1.00 | 0.77 | 0.26 | 5 | 6.5% | 0.50 | 0.55 | 12.0% | 11.0% | 12.9% | 11.9%/9.2% | 7.2 (interpolated) | pass | 0.281 (unverified) | 0.53 |
| 37 | `cfg_2bcd` | timeframe=1min, window=0, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 101/2/70 | 173 | 18.9% | 3.4% | 0.83 | -7.5% | 643 | 1.41 | 5.5% | 75.8 | 7/7 | 1.00 | 0.72 | 0.12 | 4 | 10.3% | 0.44 | 0.59 | 17.5% | 16.0% | 17.5% | 17.4%/12.8% | 7.0 (interpolated) | pass | 0.129 (unverified) | 0.78 |
| 38 | `cfg_ca15` | timeframe=1min, window=0, first_days=2, entry=13:00, exit=16:00, event_filter=skip_fomc, stop=none | 114/1/0 | 115 | 18.3% | 3.3% | 1.07 | -2.9% | 193 | 1.90 | 3.1% | 50.4 | 7/7 | 1.00 | 0.77 | 0.30 | 5 | 8.9% | 0.51 | 0.47 | 17.4% | 16.6% | 18.7% | 16.7%/13.7% | 9.9 (interpolated) | pass | 0.318 (unverified) | 0.85 |
| 39 | `cfg_4459` | timeframe=1min, window=0, first_days=2, entry=13:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 104/1/10 | 115 | 15.2% | 2.8% | 0.93 | -2.9% | 193 | 1.70 | 2.9% | 50.5 | 8/8 | 1.00 | 0.79 | 0.14 | 5 | 7.0% | 0.54 | 0.57 | 13.9% | 12.7% | 16.2% | 13.4%/10.1% | 8.2 (interpolated) | pass | 0.202 (unverified) | 0.57 |
| 40 | `cfg_dd7e` | timeframe=1min, window=2, first_days=2, entry=11:00, exit=15:00, event_filter=none, stop=1.00 | 210/3/27 | 240 | 22.4% | 4.0% | 0.85 | -9.5% | 475 | 1.40 | 8.0% | 105.4 | 10/10 | 1.00 | 0.58 | 0.27 | 4 | 11.6% | 0.48 | 0.49 | 20.3% | 18.0% | 21.3% | 20.1%/16.5% | 6.1 (interpolated) | pass | 0.153 (unverified) | 0.32 |
| 41 | `cfg_8cc7` | timeframe=1min, window=4, first_days=3, entry=11:00, exit=15:30, event_filter=none, stop=1.00 | 358/6/56 | 420 | 32.5% | 5.6% | 0.80 | -7.5% | 384 | 1.26 | 15.7% | 184.9 | 8/8 | 1.00 | 0.55 | 0.24 | 4 | 16.4% | 0.45 | 0.53 | 27.1% | 22.9% | 32.4% | 27.6%/19.7% | 4.9 (interpolated) | pass | 0.121 (unverified) | 0.64 |
| 42 | `cfg_4779` | timeframe=1min, window=4, first_days=3, entry=11:00, exit=15:00, event_filter=none, stop=1.00 | 365/6/49 | 420 | 30.9% | 5.4% | 0.82 | -8.5% | 308 | 1.26 | 14.1% | 185.3 | 8/8 | 1.00 | 0.53 | 0.30 | 4 | 18.5% | 0.37 | 0.48 | 26.3% | 21.3% | 30.6% | 26.9%/19.3% | 4.8 (interpolated) | pass | 0.136 (unverified) | 0.54 |
| 43 | `cfg_e716` | timeframe=1min, window=1, first_days=2, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 148/2/23 | 173 | 22.1% | 4.0% | 0.88 | -6.0% | 277 | 1.51 | 7.2% | 75.5 | 9/9 | 1.00 | 0.59 | 0.29 | 3 | 12.2% | 0.45 | 0.57 | 19.9% | 18.5% | 18.2% | 18.5%/15.1% | 7.8 (interpolated) | pass | 0.163 (unverified) | 0.40 |
| 44 | `cfg_beec` | timeframe=1min, window=1, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 195/3/33 | 231 | 23.5% | 4.2% | 0.80 | -7.3% | 198 | 1.35 | 9.5% | 102.1 | 8/8 | 1.00 | 0.55 | 0.24 | 5 | 16.1% | 0.31 | 0.57 | 21.3% | 18.8% | 19.9% | 20.8%/15.7% | 6.5 (interpolated) | pass | 0.126 (unverified) | 0.42 |
| 45 | `cfg_51de` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 199/4/138 | 341 | 26.1% | 4.6% | 0.77 | -6.9% | 381 | 1.28 | 11.1% | 149.6 | 8/8 | 1.00 | 0.56 | 0.21 | 4 | 9.8% | 0.62 | 0.61 | 22.6% | 18.6% | 18.9% | 23.9%/16.9% | 5.0 (interpolated) | pass | 0.100 (unverified) | 0.86 |
| 46 | `cfg_0175` | timeframe=1min, window=2, first_days=2, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 141/3/86 | 230 | 25.4% | 4.5% | 0.94 | -4.9% | 409 | 1.44 | 7.6% | 100.9 | 9/9 | 1.00 | 0.68 | 0.26 | 4 | 8.9% | 0.65 | 0.53 | 23.4% | 20.9% | 19.5% | 22.8%/17.0% | 7.0 (interpolated) | pass | 0.187 (unverified) | 0.87 |
| 47 | `cfg_8b5a` | timeframe=1min, window=3, first_days=2, entry=11:00, exit=15:00, event_filter=none, stop=0.50 | 193/3/104 | 300 | 22.4% | 4.0% | 0.81 | -10.0% | 450 | 1.32 | 8.2% | 131.8 | 10/10 | 1.00 | 0.55 | 0.26 | 4 | 10.1% | 0.55 | 0.53 | 19.0% | 16.6% | 18.0% | 20.4%/14.6% | 5.1 (interpolated) | pass | 0.120 (unverified) | 0.71 |
| 48 | `cfg_f8eb` | timeframe=1min, window=2, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 169/4/115 | 288 | 26.5% | 4.7% | 0.88 | -5.8% | 386 | 1.34 | 9.3% | 126.7 | 8/8 | 1.00 | 0.62 | 0.26 | 4 | 10.9% | 0.59 | 0.51 | 23.8% | 20.3% | 19.5% | 23.4%/18.7% | 5.7 (interpolated) | pass | 0.154 (unverified) | 0.98 |
| 49 | `cfg_ccf7` | timeframe=1min, window=2, first_days=0, entry=11:00, exit=12:00, event_filter=none, stop=1.00 | 118/0/2 | 120 | 8.1% | 1.5% | 0.78 | -3.4% | 366 | 1.58 | 1.1% | 52.7 | 7/8 | 1.00 | 0.58 | 0.21 | 3 | 1.3% | 0.84 | 0.64 | 7.0% | 5.8% | 7.0% | 7.3%/5.1% | 4.7 (interpolated) | pass | 0.123 (unverified) | 0.96 |
| 50 | `cfg_6411` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=15:00, event_filter=none, stop=none | 119/0/0 | 119 | 8.3% | 1.6% | 1.08 | -2.8% | 539 | 1.81 | 1.1% | 52.7 | 6/8 | 1.00 | 0.72 | 0.35 | 4 | 4.2% | 0.49 | 0.41 | 7.2% | 6.0% | 8.1% | 7.6%/6.0% | 4.9 (interpolated) | pass | 0.331 (unverified) | 0.75 |
| 51 | `cfg_d905` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=15:00, event_filter=none, stop=0.50 | 227/4/129 | 360 | 23.1% | 4.1% | 0.77 | -6.8% | 388 | 1.26 | 9.8% | 158.7 | 9/9 | 1.00 | 0.62 | 0.15 | 4 | 13.2% | 0.43 | 0.53 | 19.3% | 15.1% | 18.9% | 21.1%/14.3% | 4.4 (interpolated) | pass | 0.104 (unverified) | 0.96 |
| 52 | `cfg_9ec4` | timeframe=1min, window=2, first_days=0, entry=11:00, exit=12:00, event_filter=none, stop=none | 120/0/0 | 120 | 9.2% | 1.7% | 0.92 | -2.3% | 300 | 1.71 | 1.1% | 52.8 | 6/7 | 1.00 | 0.61 | 0.31 | 3 | 2.5% | 0.73 | 0.57 | 8.1% | 7.0% | 8.2% | 8.1%/6.1% | 5.3 (interpolated) | pass | 0.180 (unverified) | 0.96 |
| 53 | `cfg_078d` | timeframe=1min, window=0, first_days=2, entry=12:00, exit=16:00, event_filter=skip_fomc, stop=none | 114/1/0 | 115 | 18.8% | 3.4% | 0.91 | -4.1% | 303 | 1.73 | 4.1% | 50.6 | 7/7 | 1.00 | 0.68 | 0.23 | 4 | 10.0% | 0.47 | 0.43 | 17.8% | 16.5% | 20.1% | 16.4%/13.1% | 10.1 (interpolated) | pass | 0.219 (unverified) | 0.54 |
| 54 | `cfg_45f6` | timeframe=1min, window=0, first_days=2, entry=13:00, exit=16:00, event_filter=none, stop=0.50 | 87/1/32 | 120 | 12.1% | 2.2% | 0.84 | -2.8% | 278 | 1.53 | 2.7% | 52.9 | 8/8 | 1.00 | 0.68 | 0.16 | 4 | 7.6% | 0.37 | 0.66 | 10.8% | 9.8% | 11.7% | 10.9%/7.9% | 6.6 (interpolated) | pass | 0.145 (unverified) | 0.33 |
| 55 | `cfg_8cae` | timeframe=1min, window=2, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=0.50 | 173/4/123 | 300 | 22.9% | 4.1% | 0.76 | -6.2% | 404 | 1.28 | 9.7% | 131.7 | 8/8 | 1.00 | 0.55 | 0.21 | 4 | 8.8% | 0.62 | 0.59 | 19.4% | 16.0% | 15.9% | 20.4%/13.6% | 5.0 (interpolated) | pass | 0.099 (unverified) | 0.97 |
| 56 | `cfg_baf6` | timeframe=1min, window=0, first_days=2, entry=13:00, exit=16:00, event_filter=none, stop=0.25 | 62/1/57 | 120 | 10.2% | 1.9% | 0.85 | -4.0% | 645 | 1.55 | 2.1% | 53.3 | 7/7 | 1.00 | 0.73 | 0.12 | 4 | 4.2% | 0.59 | 0.70 | 8.9% | 7.9% | 10.5% | 9.1%/7.0% | 5.8 (interpolated) | pass | 0.127 (unverified) | 0.70 |
| 57 | `cfg_b443` | timeframe=1min, window=0, first_days=2, entry=13:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 61/1/53 | 115 | 10.8% | 2.0% | 0.92 | -3.7% | 624 | 1.63 | 2.1% | 51.0 | 7/7 | 1.00 | 0.76 | 0.15 | 4 | 4.4% | 0.59 | 0.67 | 9.5% | 8.5% | 11.0% | 10.0%/7.3% | 6.3 (interpolated) | pass | 0.159 (unverified) | 0.83 |
| 58 | `cfg_882b` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 71/0/43 | 114 | 10.5% | 2.0% | 1.01 | -1.6% | 238 | 1.73 | 1.5% | 50.1 | 7/7 | 1.00 | 0.63 | 0.38 | 4 | 6.0% | 0.41 | 0.60 | 9.4% | 8.5% | 9.1% | 9.3%/7.5% | 6.1 (interpolated) | pass | 0.243 (unverified) | 0.79 |
| 59 | `cfg_b267` | timeframe=1min, window=0, first_days=2, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=none | 114/1/0 | 115 | 21.4% | 3.8% | 0.87 | -4.8% | 537 | 1.71 | 5.1% | 50.4 | 7/7 | 1.00 | 0.63 | 0.24 | 4 | 11.5% | 0.46 | 0.49 | 20.4% | 19.2% | 23.4% | 19.4%/15.0% | 11.0 (interpolated) | pass | 0.194 (unverified) | 0.53 |
| 60 | `cfg_ac74` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=16:00, event_filter=none, stop=0.25 | 72/0/47 | 119 | 9.6% | 1.8% | 0.92 | -1.6% | 239 | 1.61 | 1.6% | 52.3 | 7/7 | 1.00 | 0.62 | 0.30 | 4 | 5.5% | 0.42 | 0.64 | 8.5% | 7.5% | 8.2% | 8.7%/6.5% | 5.5 (interpolated) | pass | 0.182 (unverified) | 0.64 |
| 61 | `cfg_834b` | timeframe=1min, window=2, first_days=2, entry=11:00, exit=15:00, event_filter=none, stop=0.50 | 154/3/83 | 240 | 17.8% | 3.2% | 0.75 | -8.3% | 514 | 1.32 | 6.6% | 105.7 | 10/10 | 1.00 | 0.48 | 0.27 | 4 | 7.7% | 0.56 | 0.60 | 15.5% | 12.9% | 14.7% | 15.9%/12.5% | 5.1 (interpolated) | pass | 0.097 (unverified) | 0.69 |
| 62 | `cfg_3afc` | timeframe=1min, window=2, first_days=2, entry=11:00, exit=15:00, event_filter=skip_fomc, stop=0.50 | 149/3/78 | 230 | 17.7% | 3.2% | 0.77 | -9.1% | 536 | 1.34 | 6.3% | 101.7 | 10/10 | 1.00 | 0.47 | 0.30 | 4 | 7.0% | 0.60 | 0.61 | 15.3% | 12.9% | 14.6% | 16.3%/11.6% | 5.2 (interpolated) | pass | 0.102 (unverified) | 0.75 |
| 63 | `cfg_a0b9` | timeframe=1min, window=1, first_days=2, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=none | 171/0/0 | 171 | 13.8% | 2.6% | 0.80 | -4.7% | 518 | 1.45 | 3.1% | 74.8 | 8/8 | 1.00 | 0.45 | 0.34 | 4 | 3.0% | 0.77 | 0.58 | 12.5% | 11.2% | 14.6% | 13.0%/9.8% | 5.7 (interpolated) | pass | 0.129 (unverified) | 0.73 |
| 64 | `cfg_2214` | timeframe=1min, window=2, first_days=0, entry=10:30, exit=12:00, event_filter=none, stop=1.00 | 115/0/5 | 120 | 12.3% | 2.3% | 0.78 | -4.5% | 536 | 1.59 | 1.6% | 52.8 | 8/8 | 0.88 | 0.45 | 0.34 | 3 | 1.2% | 0.91 | 0.73 | 11.0% | 9.9% | 9.7% | 11.0%/8.5% | 6.5 (interpolated) | pass | 0.114 (unverified) | 0.83 |
| 65 | `cfg_6639` | timeframe=1min, window=2, first_days=0, entry=10:30, exit=12:00, event_filter=none, stop=none | 120/0/0 | 120 | 12.6% | 2.3% | 0.81 | -4.0% | 536 | 1.61 | 1.6% | 52.9 | 7/7 | 1.00 | 0.51 | 0.30 | 3 | 1.5% | 0.88 | 0.71 | 11.5% | 10.2% | 9.7% | 11.2%/8.6% | 6.7 (interpolated) | pass | 0.119 (unverified) | 0.83 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 2.0% / 0.57 / 22 | 0.3% / 0.13 / 23 | 5.7% / 1.31 / 23 | 8.9% / 2.24 / 24 | 7.7% / 1.77 / 23 |
| 2 | 6.7% / 2.17 / 34 | 0.3% / 0.13 / 35 | 5.4% / 1.56 / 35 | 1.6% / 0.68 / 35 | 5.1% / 1.37 / 34 |
| 3 | 3.3% / 1.13 / 22 | 1.9% / 0.83 / 23 | 2.7% / 0.94 / 23 | 4.4% / 1.82 / 24 | 5.6% / 1.47 / 23 |
| 4 | 6.9% / 1.84 / 36 | 2.7% / 0.98 / 36 | 2.7% / 0.66 / 36 | 3.5% / 1.21 / 36 | 8.1% / 1.39 / 36 |
| 5 | 6.6% / 1.79 / 34 | 3.3% / 1.23 / 35 | 3.3% / 0.81 / 35 | 2.9% / 1.02 / 35 | 4.7% / 1.13 / 34 |
| 6 | 2.2% / 1.01 / 21 | 1.9% / 1.22 / 23 | 5.0% / 1.38 / 23 | -0.8% / -0.44 / 24 | 7.3% / 2.10 / 23 |
| 7 | 1.8% / 0.75 / 22 | -2.0% / -1.07 / 23 | 2.3% / 0.91 / 23 | 5.8% / 2.57 / 24 | 5.9% / 1.82 / 23 |
| 8 | 4.6% / 1.54 / 36 | -0.8% / -0.34 / 36 | 1.8% / 0.56 / 36 | 5.0% / 1.81 / 36 | 8.3% / 1.83 / 36 |
| 9 | 3.0% / 0.94 / 22 | 1.0% / 0.37 / 23 | 3.8% / 1.07 / 23 | 5.1% / 2.02 / 24 | 7.4% / 1.89 / 23 |
| 10 | 7.1% / 1.50 / 34 | 1.3% / 0.40 / 35 | 5.9% / 1.05 / 35 | 7.3% / 1.59 / 35 | 5.2% / 1.00 / 34 |
| 11 | 3.2% / 0.55 / 72 | -0.6% / -0.13 / 72 | 11.6% / 1.58 / 72 | 6.8% / 1.20 / 72 | 12.3% / 1.54 / 72 |
| 12 | 2.5% / 1.21 / 21 | 1.9% / 1.23 / 23 | 7.8% / 2.21 / 23 | -2.1% / -0.78 / 24 | 7.9% / 2.45 / 23 |
| 13 | 2.8% / 1.31 / 22 | -2.6% / -1.76 / 23 | 3.2% / 1.54 / 23 | 3.9% / 1.92 / 24 | 4.2% / 1.43 / 23 |
| 14 | 6.5% / 1.60 / 34 | 1.9% / 0.59 / 35 | 2.7% / 0.57 / 35 | 2.7% / 0.85 / 35 | 5.7% / 1.25 / 34 |
| 15 | 6.9% / 1.45 / 36 | 0.7% / 0.21 / 36 | 4.7% / 0.82 / 36 | 7.6% / 1.66 / 36 | 7.7% / 1.21 / 36 |
| 16 | -0.2% / -0.02 / 45 | 1.3% / 0.39 / 44 | 10.0% / 1.53 / 46 | 1.9% / 0.42 / 48 | 19.9% / 2.43 / 47 |
| 17 | 5.0% / 1.87 / 24 | -0.5% / -0.25 / 24 | 2.7% / 1.16 / 24 | 3.0% / 1.44 / 24 | 4.2% / 1.25 / 24 |
| 18 | 4.0% / 0.72 / 60 | 1.5% / 0.36 / 60 | 9.9% / 1.31 / 60 | 0.5% / 0.12 / 60 | 19.9% / 2.07 / 60 |
| 19 | 1.8% / 0.51 / 24 | -0.2% / -0.05 / 24 | 4.7% / 1.04 / 24 | 9.0% / 2.25 / 24 | 6.5% / 1.44 / 24 |
| 20 | 2.7% / 1.38 / 21 | 1.1% / 0.64 / 23 | 3.7% / 1.22 / 23 | 0.1% / 0.09 / 24 | 6.9% / 2.11 / 23 |
| 21 | 3.6% / 0.63 / 68 | -1.0% / -0.25 / 68 | 10.7% / 1.53 / 68 | 5.4% / 1.03 / 68 | 10.6% / 1.40 / 69 |
| 22 | 2.3% / 0.38 / 68 | 1.7% / 0.41 / 68 | 13.2% / 1.53 / 68 | -0.4% / -0.04 / 68 | 17.6% / 1.81 / 69 |
| 23 | 5.8% / 1.16 / 60 | -0.7% / -0.16 / 60 | 5.4% / 0.94 / 60 | 5.6% / 1.07 / 60 | 11.2% / 1.51 / 60 |
| 24 | 6.4% / 1.27 / 57 | -1.0% / -0.25 / 56 | 4.9% / 0.91 / 58 | 5.0% / 0.97 / 59 | 10.2% / 1.46 / 58 |
| 25 | 0.5% / 0.10 / 72 | 0.6% / 0.16 / 72 | 13.7% / 1.56 / 72 | -0.2% / -0.01 / 72 | 21.8% / 2.04 / 72 |
| 26 | 6.9% / 1.67 / 36 | 0.8% / 0.24 / 36 | 1.4% / 0.30 / 36 | 3.4% / 1.05 / 36 | 8.4% / 1.41 / 36 |
| 27 | -0.4% / -0.06 / 56 | -2.2% / -0.65 / 56 | 9.5% / 1.52 / 56 | 7.7% / 1.53 / 57 | 11.8% / 1.67 / 58 |
| 28 | -1.0% / -0.15 / 60 | -2.0% / -0.52 / 60 | 10.3% / 1.55 / 60 | 8.4% / 1.55 / 60 | 11.5% / 1.61 / 60 |
| 29 | 1.1% / 0.33 / 22 | -2.0% / -0.76 / 23 | 4.5% / 1.28 / 23 | 9.3% / 2.32 / 24 | 6.6% / 1.74 / 23 |
| 30 | 1.4% / 0.45 / 22 | -2.0% / -0.76 / 23 | 3.9% / 0.95 / 23 | 9.5% / 2.69 / 24 | 5.0% / 1.24 / 23 |
| 31 | 1.2% / 1.09 / 21 | -1.3% / -1.24 / 23 | 2.7% / 1.30 / 23 | 0.8% / 0.73 / 24 | 4.6% / 2.80 / 23 |
| 32 | 2.5% / 0.59 / 45 | -2.5% / -0.75 / 44 | 4.0% / 0.86 / 46 | 7.2% / 1.53 / 48 | 10.9% / 1.72 / 47 |
| 33 | 3.4% / 1.04 / 24 | -0.2% / -0.06 / 24 | 2.6% / 0.71 / 24 | 5.1% / 2.01 / 24 | 6.2% / 1.51 / 24 |
| 34 | 1.1% / 0.46 / 22 | 3.5% / 1.86 / 23 | 0.6% / 0.21 / 23 | 3.1% / 1.55 / 24 | 4.8% / 1.25 / 23 |
| 35 | 0.2% / 0.09 / 22 | -3.0% / -1.21 / 23 | 2.8% / 0.88 / 23 | 10.5% / 2.77 / 24 | 6.8% / 1.93 / 23 |
| 36 | 2.7% / 1.32 / 23 | 0.5% / 0.27 / 24 | 3.1% / 1.02 / 24 | 0.1% / 0.10 / 24 | 6.2% / 1.89 / 24 |
| 37 | 3.7% / 0.94 / 34 | -2.5% / -0.73 / 35 | 5.0% / 0.99 / 35 | 7.8% / 1.86 / 35 | 3.9% / 0.83 / 34 |
| 38 | 1.8% / 0.78 / 22 | 1.0% / 0.34 / 23 | 5.5% / 1.90 / 23 | 0.4% / 0.12 / 24 | 8.6% / 2.11 / 23 |
| 39 | 0.1% / 0.06 / 22 | 2.0% / 0.83 / 23 | 2.4% / 0.77 / 23 | 2.3% / 1.03 / 24 | 7.6% / 1.75 / 23 |
| 40 | 1.8% / 0.43 / 48 | -2.2% / -0.60 / 48 | 4.6% / 0.90 / 48 | 7.2% / 1.53 / 48 | 9.7% / 1.51 / 48 |
| 41 | 9.8% / 1.29 / 84 | -3.6% / -0.76 / 84 | 13.8% / 1.56 / 84 | 0.5% / 0.12 / 84 | 9.4% / 1.02 / 84 |
| 42 | 10.1% / 1.39 / 84 | -2.1% / -0.43 / 84 | 10.5% / 1.35 / 84 | 2.8% / 0.48 / 84 | 6.9% / 0.87 / 84 |
| 43 | -0.6% / -0.13 / 33 | -0.0% / 0.00 / 34 | 5.5% / 1.02 / 35 | 7.1% / 1.69 / 36 | 8.8% / 1.44 / 35 |
| 44 | 4.3% / 0.84 / 45 | 0.9% / 0.27 / 46 | 5.4% / 0.84 / 47 | 4.7% / 1.00 / 47 | 6.3% / 0.93 / 46 |
| 45 | 3.1% / 0.57 / 68 | -5.2% / -1.24 / 68 | 10.3% / 1.34 / 68 | 1.8% / 0.39 / 68 | 14.9% / 1.73 / 69 |
| 46 | 1.1% / 0.28 / 45 | -3.1% / -0.89 / 44 | 6.6% / 1.16 / 46 | 4.3% / 1.07 / 48 | 15.1% / 2.10 / 47 |
| 47 | 0.3% / 0.08 / 60 | -4.3% / -1.24 / 60 | 6.5% / 1.13 / 60 | 7.7% / 1.56 / 60 | 11.2% / 1.69 / 60 |
| 48 | 3.6% / 0.77 / 57 | -3.4% / -0.83 / 56 | 7.8% / 1.20 / 58 | 2.8% / 0.63 / 59 | 14.1% / 1.84 / 58 |
| 49 | -0.1% / -0.05 / 24 | 0.1% / 0.09 / 24 | 3.9% / 1.51 / 24 | -2.5% / -1.15 / 24 | 6.7% / 2.91 / 24 |
| 50 | 1.5% / 1.33 / 23 | -1.3% / -1.31 / 24 | 3.3% / 1.51 / 24 | 0.8% / 0.73 / 24 | 3.9% / 2.23 / 24 |
| 51 | 2.7% / 0.51 / 72 | -4.2% / -1.06 / 72 | 9.1% / 1.43 / 72 | 5.5% / 1.03 / 72 | 8.8% / 1.27 / 72 |
| 52 | -0.1% / -0.05 / 24 | 0.1% / 0.09 / 24 | 3.9% / 1.51 / 24 | -1.4% / -0.78 / 24 | 6.5% / 2.88 / 24 |
| 53 | 2.3% / 0.65 / 22 | -0.8% / -0.21 / 23 | 5.8% / 1.49 / 23 | 2.5% / 0.60 / 24 | 8.1% / 1.93 / 23 |
| 54 | 1.5% / 0.63 / 24 | 2.9% / 1.48 / 24 | -0.0% / 0.01 / 24 | 3.0% / 1.53 / 24 | 4.2% / 1.08 / 24 |
| 55 | 2.1% / 0.46 / 60 | -3.7% / -0.87 / 60 | 8.2% / 1.24 / 60 | 2.2% / 0.50 / 60 | 13.0% / 1.69 / 60 |
| 56 | 3.0% / 1.38 / 24 | 2.1% / 1.22 / 24 | -1.8% / -1.02 / 24 | 0.9% / 0.50 / 24 | 5.8% / 1.60 / 24 |
| 57 | 2.6% / 1.28 / 22 | 2.5% / 1.42 / 23 | -1.5% / -0.87 / 23 | 0.9% / 0.50 / 24 | 6.1% / 1.70 / 23 |
| 58 | 1.6% / 0.93 / 21 | 1.5% / 1.04 / 23 | 4.2% / 1.58 / 23 | -0.6% / -0.45 / 24 | 3.5% / 1.37 / 23 |
| 59 | 1.0% / 0.25 / 22 | -0.4% / -0.11 / 23 | 5.3% / 1.08 / 23 | 5.3% / 0.91 / 24 | 8.9% / 2.04 / 23 |
| 60 | 1.6% / 0.94 / 23 | 1.2% / 0.83 / 24 | 3.9% / 1.45 / 24 | -0.6% / -0.43 / 24 | 3.1% / 1.23 / 24 |
| 61 | 1.1% / 0.28 / 48 | -3.5% / -1.08 / 48 | 3.0% / 0.69 / 48 | 7.3% / 1.63 / 48 | 9.3% / 1.56 / 48 |
| 62 | 2.2% / 0.56 / 45 | -4.3% / -1.43 / 44 | 1.9% / 0.49 / 46 | 7.3% / 1.63 / 48 | 10.0% / 1.67 / 47 |
| 63 | 0.2% / 0.08 / 32 | 1.2% / 0.66 / 33 | 10.5% / 2.46 / 35 | -4.4% / -1.53 / 36 | 6.3% / 1.48 / 35 |
| 64 | -1.8% / -0.91 / 24 | 0.4% / 0.24 / 24 | 5.0% / 1.33 / 24 | -2.3% / -0.68 / 24 | 11.0% / 2.99 / 24 |
| 65 | -1.8% / -0.90 / 24 | 0.4% / 0.24 / 24 | 5.0% / 1.33 / 24 | -2.0% / -0.61 / 24 | 11.0% / 2.99 / 24 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_51de` | 5 | 0.83 | 0.78/0.85 | 0.67/0.74 |
| 1 | `cfg_0214` | 4 | 0.83 | 0.83/0.90 | 0.94/0.96 |
| 2 | `cfg_0267` | 6 | 0.89 | 0.88/0.95 | 0.76/0.85 |
| 3 | `cfg_a5bf` | 4 | 0.92 | 0.91/0.95 | 0.86/0.90 |
| 4 | `cfg_0717` | 5 | 0.86 | 0.87/0.91 | 0.74/0.82 |
| 5 | `cfg_078d` | 2 | 0.88 | 0.88/0.88 | 0.80/0.80 |
| 6 | `cfg_3ddd` | 4 | 0.92 | 0.94/0.96 | 0.86/0.89 |
| 7 | `cfg_20de` | 4 | 0.85 | 0.89/0.92 | 0.79/0.83 |
| 8 | `cfg_d81b` | 4 | 0.87 | 0.85/0.89 | 0.77/0.80 |
| 9 | `cfg_2214` | 2 | 1.00 | 1.00/1.00 | 0.99/0.99 |
| 10 | `cfg_2950` | 6 | 0.85 | 0.86/0.91 | 0.75/0.86 |
| 11 | `cfg_e2b0` | 4 | 0.81 | 0.82/0.95 | 0.68/0.91 |
| 12 | `cfg_3086` | 4 | 0.91 | 0.93/0.96 | 0.86/0.89 |
| 13 | `cfg_ca15` | 3 | 0.88 | 0.88/0.91 | 0.96/0.96 |
| 14 | `cfg_834b` | 2 | 0.97 | 0.97/0.97 | 0.96/0.96 |
| 15 | `cfg_9ec2` | 9 | 0.81 | 0.80/0.91 | 0.63/0.78 |
| 16 | `cfg_c78f` | 2 | 0.98 | 0.98/0.98 | 0.96/0.96 |
| 17 | `cfg_8cc7` | 4 | 0.84 | 0.88/0.91 | 0.81/0.85 |
| 18 | `cfg_806d` | 4 | 0.84 | 0.81/0.87 | 0.73/0.76 |
| 19 | `cfg_ae0c` | 4 | 0.90 | 0.91/0.95 | 0.85/0.90 |
| 20 | `cfg_50f9` | 3 | 0.96 | 0.96/0.97 | 0.96/0.96 |
| 21 | `cfg_b923` | 6 | 0.85 | 0.87/0.90 | 0.79/0.88 |
| 22 | `cfg_bdf0` | 4 | 0.90 | 0.92/0.96 | 0.84/0.89 |
| 23 | `cfg_d50a` | 3 | 0.87 | 0.90/0.92 | 0.78/0.83 |
| 24 | `cfg_7f87` | 4 | 0.82 | 0.84/0.90 | 0.74/0.76 |
| 25 | `cfg_882b` | 2 | 0.99 | 0.99/0.99 | 0.97/0.97 |
| 26 | `cfg_8b5a` | 2 | 0.91 | 0.92/0.92 | 0.84/0.84 |
| 27 | `cfg_f8eb` | 3 | 0.88 | 0.90/0.95 | 0.83/0.90 |
| 28 | `cfg_d615` | 3 | 0.83 | 0.84/0.91 | 0.82/0.89 |
| 29 | `cfg_ccf7` | 3 | 0.95 | 0.96/0.97 | 0.95/0.97 |
| 30 | `cfg_a0b9` | 1 | n/a | n/a/n/a | n/a/n/a |
| 31 | `cfg_baf6` | 2 | 0.99 | 0.98/0.98 | 0.96/0.96 |
| 32 | `cfg_e716` | 2 | 0.87 | 0.86/0.86 | 0.75/0.75 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 8.138e-04 over 4864 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 268.0, participation ratio 12.1, 95%-variance components 73 (rank bound T = 1292); raw grid 4864; raw + known prior 1652768
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

- Bars: 1-minute bars with NY open time in [08:00, 17:00) only (me_day_bars); each NY date is one session, so the session's last bar is the last bar before 17:00 ET and no position can be held overnight.
- Month-end rank per session date: the number of NYSE trading days in its calendar month on or after it (1 = the last). Taken from the NYSE calendar (published in advance), never from later bars; recomputed month by month in the integrity check.
- Eligible day: 1 <= rank <= window, and the event filter allows it (skip_fomc: not a scheduled FOMC statement day; skip_fomc_auction: also no fixed-rate Treasury note/bond auction that day, from configs/calendars/coupon_auctions.csv).
- Entry: LONG at the OPEN of the first bar opening at/after the entry time with market slippage; skipped when that bar opens more than 5 minutes late (a gap in the bars) or is not before the exit.
- Exit at the CLOSE of the last bar opening before the exit target (15:00, 16:00, or the index strike: 15:00 ET on month-ends before 14 Jan 2021, 16:00 ET from then on), with market slippage; when the bars stop earlier (early closes) the trade closes at the session's last bar. Stop (optional) = entry open x (1 - stop%), live intrabar from the entry bar, filled at the worse of the bar's open and the stop with stop slippage.
- One trade per eligible day; long only; sizing is the other families' (as many whole contracts as equity covers at full contract value, unlevered, compounding).
- Development backtests run on data physically truncated at the development end; the final session's trade is closed at the last development bar and flagged forced (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC). Log returns use back-adjusted prices; the adjustment is constant within a session, so 1-minute returns are distorted only by the level shift (tiny for ES).
- Session: each root's day session only (src/data/futures.py SESSIONS), on NYSE trading days; overnight Globex bars are not traded or used in any statistic.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side plus commission per contract per side, from the execution YAML; cost stress scales both. ZN ticks are 1/64 point ($15.625), ZB 1/32 ($31.25).
- Session: 08:00-17:00 ET of each NY date with data (NOT the 08:20-15:00 pit session the src/data/futures.py table gives ZN / ZB), so the post-2021 16:00 ET strike is inside the window. Globex bars before 08:00 and after 17:00 are never loaded into the strategy.

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Every published month-end number (Hartley & Schwarz; the ohlcv.io futures test) is close-to-close and includes the overnight session. This run measures only the 08:00-17:00 ET part; a failure says the day-session share is too small, not that the month-end effect is gone.
- Month-end days come from the NYSE calendar. The index month-end follows the bond market (SIFMA) calendar; the two differ at month-end only when Good Friday is the month's last weekday (Mar 2018, Mar 2024), where this run treats the Thursday as the last day.
- The strike switch date (14 Jan 2021, 15:00 -> 16:00 ET) is taken from the NY Fed's Liberty Street note (Sep 2026); before it the strike and the 15:00 exit coincide.
- Windows of 1-2 days give about 12-24 trades a year; window 1 (about 60 development trades) cannot pass the 100-trade stage-2 gate by design and is kept as an ablation level.
- FOMC days come from a hard-coded list of statement dates (src/strategies/month_end/config.py); auction days from the Treasury Fiscal Data API (auctions_query), fixed-rate notes and bonds including TIPS, FRNs excluded.
- Long only and on a calendar: ZN / ZB rallied in 2018-2020 and sold off in 2021-2022, so the long bias of the market is part of every config's P&L; the placebo benchmark (random non-month-end days, same clock) separates the calendar from that drift.
- Sizing ignores volatility (full equity per trade, as in the other families).
