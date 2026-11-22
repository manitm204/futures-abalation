# Screening funnel -- me_nq_v2 (development stages only)

- Code: `d7cd024716c8` (dirty working tree: True, diff sha256 `cb637a176976`)
- Config: `configs/funnel/me_funnel_nq_v2.yaml` sha256 `d4c43714e09800d0`; seed 20261123
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ES': '2026-10-16', 'NQ': '2026-10-16'}
- Frozen manifest sha256: `5123c46c33db3f30` (130 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- Diagnostic run (development only). NQ 2023-2024 was already scored for ES pick #7 with unchanged rules, and other families were selected there.
- Holdout 2025+ previously inspected: **True** -- NQ 2025+ was already scored for ES pick #7 (unchanged-rules check, 2026-11-22) and for the combined #7 page. This run never reads it.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 4864 | 4864 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 4864 | 4864 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 4864 | 4352 | 512 | 0 |  | 0 | 89.47 | 89.47 |  |
| 3 performance & risk | hard_gate | 4352 | 247 | 4105 | 0 |  | 0 | 5.08 | 5.68 |  |
| 4 parameter stability | hard_gate | 247 | 247 | 0 | 0 |  | 0 | 5.08 | 100.00 |  |
| 5 time stability | hard_gate | 247 | 244 | 3 | 0 |  | 174 | 5.02 | 98.79 |  |
| 6 deduplication | dedup | 244 | 130 |  |  | 114 |  | 2.67 | 53.28 | best 2 per cluster |
| 7 execution stress | hard_gate | 130 | 130 | 0 | 0 |  | 0 | 2.67 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 130 |  |  |  |  |  |  |  | diagnostic only: unverified: 130 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 512 |
| s3:hard_reject:net_return | 1120 |
| s3:hard_reject:sharpe | 4105 |
| s5:hard_reject:profitable_years | 3 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_20eb` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 112/0/2 | 114 | 18.7% | 3.4% | 1.40 | -1.8% | 299 | 2.50 | 2.0% | 55.3 | 8/8 | 1.00 | 0.98 | 0.42 | 5 | 8.8% | 0.53 | 0.44 | 18.5% | 17.9% | 18.9% | 17.0%/14.6% | 24.0 (interpolated) | pass | 0.816 (unverified) | 1.31 |
| 2 | `cfg_ff31` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=0.50 | 254/3/103 | 360 | 46.2% | 7.7% | 1.15 | -5.1% | 366 | 1.48 | 13.1% | 177.8 | 8/8 | 1.00 | 0.92 | 0.23 | 4 | 16.8% | 0.64 | 0.48 | 44.6% | 42.6% | 42.9% | 40.2%/33.7% | 15.5 (interpolated) | pass | 0.607 (unverified) | 0.86 |
| 3 | `cfg_1b7e` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=15:00, event_filter=none, stop=0.50 | 269/3/88 | 360 | 37.3% | 6.4% | 1.19 | -4.0% | 194 | 1.46 | 10.8% | 177.6 | 9/9 | 1.00 | 0.89 | 0.29 | 5 | 19.8% | 0.47 | 0.41 | 35.7% | 34.0% | 34.6% | 33.5%/28.3% | 13.7 (interpolated) | pass | 0.637 (unverified) | 0.96 |
| 4 | `cfg_8faf` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=15:30, event_filter=none, stop=0.50 | 264/3/93 | 360 | 40.2% | 6.8% | 1.16 | -3.5% | 235 | 1.47 | 12.0% | 175.9 | 9/9 | 1.00 | 0.94 | 0.22 | 4 | 15.8% | 0.61 | 0.44 | 37.6% | 35.8% | 38.5% | 35.1%/29.9% | 14.6 (interpolated) | pass | 0.616 (unverified) | 0.92 |
| 5 | `cfg_e5fa` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 241/3/97 | 341 | 40.8% | 6.9% | 1.11 | -4.3% | 242 | 1.45 | 12.4% | 168.2 | 8/8 | 1.00 | 0.94 | 0.18 | 4 | 18.5% | 0.55 | 0.46 | 38.4% | 37.3% | 37.0% | 35.1%/28.2% | 15.3 (interpolated) | pass | 0.566 (unverified) | 0.86 |
| 6 | `cfg_0639` | timeframe=1min, window=4, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=0.50 | 291/4/125 | 420 | 50.5% | 8.3% | 1.11 | -7.2% | 348 | 1.41 | 15.2% | 208.2 | 7/7 | 1.00 | 0.90 | 0.21 | 4 | 28.6% | 0.43 | 0.52 | 48.2% | 44.0% | 44.5% | 42.7%/33.6% | 14.4 (interpolated) | pass | 0.570 (unverified) | 0.92 |
| 7 | `cfg_2895` | timeframe=1min, window=4, first_days=3, entry=11:00, exit=15:30, event_filter=none, stop=0.50 | 302/4/114 | 420 | 40.9% | 6.9% | 1.08 | -5.7% | 348 | 1.38 | 13.8% | 206.7 | 8/8 | 1.00 | 0.84 | 0.24 | 4 | 24.7% | 0.40 | 0.48 | 39.3% | 35.9% | 39.1% | 36.2%/27.9% | 12.3 (interpolated) | pass | 0.538 (unverified) | 0.94 |
| 8 | `cfg_e471` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=none | 114/0/0 | 114 | 18.6% | 3.4% | 1.37 | -1.9% | 299 | 2.45 | 2.0% | 55.3 | 7/7 | 1.00 | 0.94 | 0.43 | 4 | 8.6% | 0.54 | 0.44 | 18.2% | 17.8% | 18.7% | 16.7%/14.3% | 23.5 (interpolated) | pass | 0.783 (unverified) | 1.30 |
| 9 | `cfg_6604` | timeframe=1min, window=2, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=0.50 | 211/3/86 | 300 | 40.1% | 6.8% | 1.15 | -6.2% | 366 | 1.52 | 10.9% | 147.5 | 8/8 | 1.00 | 0.91 | 0.24 | 4 | 17.8% | 0.56 | 0.49 | 38.7% | 38.0% | 38.1% | 36.2%/27.7% | 16.6 (interpolated) | pass | 0.604 (unverified) | 0.97 |
| 10 | `cfg_aff8` | timeframe=1min, window=2, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 203/3/82 | 288 | 35.8% | 6.1% | 1.11 | -6.2% | 452 | 1.49 | 10.5% | 141.3 | 8/8 | 1.00 | 0.90 | 0.21 | 4 | 17.7% | 0.51 | 0.49 | 34.7% | 32.8% | 33.1% | 32.1%/25.5% | 16.1 (interpolated) | pass | 0.563 (unverified) | 0.98 |
| 11 | `cfg_a38e` | timeframe=1min, window=3, first_days=2, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 202/2/79 | 283 | 32.9% | 5.7% | 1.02 | -5.8% | 279 | 1.48 | 10.4% | 137.8 | 9/9 | 1.00 | 0.83 | 0.19 | 4 | 9.7% | 0.70 | 0.55 | 31.2% | 30.4% | 31.3% | 29.4%/21.8% | 15.3 (interpolated) | pass | 0.471 (unverified) | 0.78 |
| 12 | `cfg_e6ea` | timeframe=1min, window=2, first_days=3, entry=11:00, exit=15:00, event_filter=none, stop=0.50 | 226/3/71 | 300 | 30.9% | 5.4% | 1.12 | -3.9% | 213 | 1.48 | 9.0% | 147.2 | 9/9 | 1.00 | 0.69 | 0.43 | 5 | 17.7% | 0.43 | 0.48 | 29.1% | 28.0% | 28.0% | 26.6%/22.2% | 13.4 (interpolated) | pass | 0.572 (unverified) | 0.95 |
| 13 | `cfg_e87c` | timeframe=1min, window=2, first_days=3, entry=11:00, exit=15:00, event_filter=skip_fomc, stop=0.50 | 217/3/68 | 288 | 26.9% | 4.8% | 1.04 | -4.2% | 275 | 1.44 | 8.6% | 141.1 | 9/9 | 1.00 | 0.72 | 0.33 | 5 | 16.1% | 0.40 | 0.51 | 25.9% | 24.8% | 24.6% | 24.7%/19.2% | 12.5 (interpolated) | pass | 0.495 (unverified) | 0.87 |
| 14 | `cfg_9883` | timeframe=1min, window=0, first_days=3, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 165/0/6 | 171 | 18.5% | 3.4% | 1.11 | -3.6% | 387 | 1.77 | 3.0% | 83.5 | 7/7 | 1.00 | 0.86 | 0.25 | 4 | 10.0% | 0.44 | 0.49 | 17.9% | 17.1% | 18.9% | 16.4%/13.6% | 15.5 (interpolated) | pass | 0.559 (unverified) | 0.96 |
| 15 | `cfg_3d0c` | timeframe=1min, window=3, first_days=3, entry=10:30, exit=16:00, event_filter=skip_fomc, stop=0.50 | 213/3/125 | 341 | 33.2% | 5.8% | 0.85 | -6.7% | 403 | 1.34 | 12.4% | 167.4 | 8/8 | 1.00 | 0.78 | 0.07 | 4 | 8.1% | 0.76 | 0.64 | 32.3% | 31.5% | 30.7% | 29.7%/23.2% | 12.7 (interpolated) | pass | 0.327 (unverified) | 0.55 |
| 16 | `cfg_4f1f` | timeframe=1min, window=3, first_days=3, entry=10:30, exit=16:00, event_filter=none, stop=0.50 | 224/3/133 | 360 | 37.6% | 6.4% | 0.90 | -6.5% | 403 | 1.36 | 13.1% | 176.7 | 8/8 | 1.00 | 0.82 | 0.09 | 4 | 6.8% | 0.82 | 0.60 | 36.5% | 34.7% | 34.6% | 33.0%/26.5% | 13.5 (interpolated) | pass | 0.367 (unverified) | 0.57 |
| 17 | `cfg_3f57` | timeframe=1min, window=3, first_days=0, entry=11:00, exit=15:00, event_filter=none, stop=0.50 | 138/2/40 | 180 | 21.8% | 3.9% | 1.01 | -3.2% | 257 | 1.62 | 5.5% | 88.3 | 9/9 | 1.00 | 0.83 | 0.18 | 5 | 11.5% | 0.47 | 0.61 | 21.3% | 20.8% | 20.7% | 20.3%/15.0% | 16.0 (interpolated) | pass | 0.460 (unverified) | 0.74 |
| 18 | `cfg_819b` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 100/0/14 | 114 | 12.9% | 2.4% | 1.08 | -2.1% | 341 | 1.93 | 1.9% | 55.6 | 8/8 | 1.00 | 0.78 | 0.31 | 5 | 3.8% | 0.70 | 0.53 | 12.4% | 11.9% | 12.8% | 11.5%/9.4% | 16.0 (interpolated) | pass | 0.538 (unverified) | 0.82 |
| 19 | `cfg_3932` | timeframe=1min, window=2, first_days=3, entry=10:30, exit=16:00, event_filter=none, stop=0.50 | 189/3/108 | 300 | 35.9% | 6.2% | 0.96 | -7.3% | 451 | 1.42 | 11.1% | 147.7 | 8/8 | 1.00 | 0.85 | 0.11 | 4 | 11.0% | 0.69 | 0.58 | 34.9% | 33.9% | 33.0% | 33.0%/26.9% | 16.0 (interpolated) | pass | 0.413 (unverified) | 0.76 |
| 20 | `cfg_95c0` | timeframe=1min, window=4, first_days=2, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 239/3/100 | 342 | 37.7% | 6.4% | 1.00 | -4.5% | 241 | 1.41 | 12.4% | 167.3 | 8/8 | 1.00 | 0.84 | 0.16 | 4 | 21.2% | 0.44 | 0.57 | 35.6% | 33.9% | 35.3% | 34.2%/25.5% | 13.8 (interpolated) | pass | 0.451 (unverified) | 0.86 |
| 21 | `cfg_3865` | timeframe=1min, window=2, first_days=0, entry=11:00, exit=12:00, event_filter=skip_fomc, stop=1.00 | 115/0/0 | 115 | 9.7% | 1.8% | 1.15 | -2.0% | 322 | 1.96 | 1.0% | 56.2 | 7/8 | 1.00 | 0.99 | 0.16 | 4 | 4.6% | 0.52 | 0.41 | 9.5% | 9.0% | 9.6% | 8.9%/7.3% | 12.8 (interpolated) | pass | 0.598 (unverified) | 0.91 |
| 22 | `cfg_091c` | timeframe=1min, window=2, first_days=3, entry=10:30, exit=16:00, event_filter=skip_fomc, stop=0.50 | 183/3/102 | 288 | 32.4% | 5.6% | 0.93 | -7.9% | 493 | 1.40 | 10.6% | 140.7 | 8/8 | 1.00 | 0.82 | 0.10 | 4 | 11.5% | 0.65 | 0.60 | 31.4% | 30.6% | 29.3% | 30.5%/23.9% | 15.6 (interpolated) | pass | 0.387 (unverified) | 0.71 |
| 23 | `cfg_b565` | timeframe=1min, window=1, first_days=2, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 165/0/6 | 171 | 17.7% | 3.2% | 0.96 | -2.8% | 325 | 1.63 | 3.0% | 83.0 | 9/9 | 1.00 | 0.80 | 0.17 | 3 | 8.7% | 0.51 | 0.60 | 17.1% | 16.5% | 19.6% | 16.1%/12.6% | 15.6 (interpolated) | pass | 0.422 (unverified) | 0.68 |
| 24 | `cfg_0efe` | timeframe=1min, window=4, first_days=3, entry=10:30, exit=16:00, event_filter=none, stop=0.50 | 260/4/156 | 420 | 41.3% | 7.0% | 0.91 | -7.5% | 235 | 1.32 | 15.3% | 205.1 | 7/7 | 1.00 | 0.84 | 0.07 | 4 | 16.3% | 0.60 | 0.58 | 39.1% | 35.8% | 36.0% | 35.3%/27.6% | 12.3 (interpolated) | pass | 0.367 (unverified) | 0.63 |
| 25 | `cfg_8880` | timeframe=1min, window=2, first_days=0, entry=11:00, exit=12:00, event_filter=none, stop=1.00 | 120/0/0 | 120 | 9.7% | 1.8% | 1.17 | -1.7% | 303 | 1.93 | 1.1% | 58.7 | 7/8 | 1.00 | 0.86 | 0.31 | 4 | 4.6% | 0.52 | 0.41 | 9.3% | 8.7% | 9.5% | 8.9%/7.5% | 11.7 (interpolated) | pass | 0.617 (unverified) | 0.96 |
| 26 | `cfg_7db7` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=15:30, event_filter=skip_fomc, stop=1.00 | 113/0/1 | 114 | 9.4% | 1.8% | 1.01 | -2.7% | 557 | 1.89 | 1.5% | 55.8 | 9/9 | 1.00 | 0.61 | 0.39 | 3 | 2.0% | 0.79 | 0.52 | 9.1% | 8.7% | 9.5% | 8.6%/6.5% | 12.6 (interpolated) | pass | 0.463 (unverified) | 0.86 |
| 27 | `cfg_c8da` | timeframe=1min, window=2, first_days=3, entry=10:30, exit=15:00, event_filter=none, stop=0.50 | 199/3/98 | 300 | 28.8% | 5.1% | 0.92 | -5.3% | 257 | 1.38 | 9.3% | 147.2 | 9/9 | 1.00 | 0.81 | 0.12 | 5 | 11.7% | 0.59 | 0.52 | 28.1% | 27.3% | 28.4% | 26.8%/21.5% | 12.9 (interpolated) | pass | 0.381 (unverified) | 0.72 |
| 28 | `cfg_bb2d` | timeframe=1min, window=3, first_days=2, entry=11:00, exit=16:00, event_filter=none, stop=0.50 | 213/2/85 | 300 | 31.0% | 5.4% | 0.95 | -6.7% | 278 | 1.42 | 11.0% | 146.7 | 9/9 | 1.00 | 0.81 | 0.14 | 3 | 7.6% | 0.75 | 0.59 | 30.0% | 29.1% | 29.7% | 27.3%/21.8% | 13.2 (interpolated) | pass | 0.398 (unverified) | 0.65 |
| 29 | `cfg_986a` | timeframe=1min, window=4, first_days=3, entry=10:30, exit=15:30, event_filter=none, stop=0.50 | 269/4/147 | 420 | 33.5% | 5.8% | 0.85 | -6.3% | 259 | 1.28 | 14.1% | 205.7 | 8/8 | 1.00 | 0.80 | 0.05 | 3 | 12.8% | 0.62 | 0.56 | 31.7% | 29.9% | 32.3% | 28.9%/23.2% | 10.7 (interpolated) | pass | 0.320 (unverified) | 0.60 |
| 30 | `cfg_89b1` | timeframe=1min, window=1, first_days=3, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 218/0/10 | 228 | 17.9% | 3.3% | 0.86 | -5.2% | 495 | 1.45 | 4.0% | 111.5 | 8/8 | 1.00 | 0.71 | 0.15 | 4 | 5.0% | 0.71 | 0.62 | 17.1% | 16.1% | 18.9% | 16.1%/12.9% | 11.2 (interpolated) | pass | 0.335 (unverified) | 0.57 |
| 31 | `cfg_c52c` | timeframe=1min, window=2, first_days=2, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 164/2/64 | 230 | 28.0% | 4.9% | 1.01 | -4.0% | 321 | 1.53 | 8.4% | 111.8 | 9/9 | 1.00 | 0.75 | 0.26 | 3 | 8.5% | 0.70 | 0.59 | 26.8% | 25.9% | 27.0% | 24.9%/18.4% | 16.1 (interpolated) | pass | 0.464 (unverified) | 0.87 |
| 32 | `cfg_8b30` | timeframe=1min, window=3, first_days=2, entry=10:30, exit=16:00, event_filter=skip_fomc, stop=0.50 | 175/2/106 | 283 | 28.2% | 5.0% | 0.80 | -4.8% | 320 | 1.36 | 10.2% | 137.5 | 9/9 | 1.00 | 0.76 | 0.04 | 3 | 3.3% | 0.88 | 0.71 | 26.7% | 25.2% | 22.1% | 25.6%/16.2% | 14.1 (interpolated) | pass | 0.276 (unverified) | 0.56 |
| 33 | `cfg_7b8d` | timeframe=1min, window=3, first_days=0, entry=11:00, exit=15:00, event_filter=skip_fomc, stop=0.50 | 129/2/37 | 168 | 19.9% | 3.6% | 0.96 | -3.5% | 258 | 1.62 | 5.2% | 82.4 | 9/9 | 1.00 | 0.78 | 0.18 | 5 | 10.7% | 0.46 | 0.67 | 19.5% | 19.2% | 18.7% | 18.9%/14.1% | 15.5 (interpolated) | pass | 0.409 (unverified) | 0.66 |
| 34 | `cfg_611f` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=15:00, event_filter=skip_fomc, stop=1.00 | 114/0/0 | 114 | 8.1% | 1.5% | 1.25 | -2.2% | 558 | 2.15 | 1.0% | 55.9 | 7/9 | 1.00 | 0.82 | 0.43 | 4 | 2.7% | 0.67 | 0.38 | 7.7% | 7.3% | 8.2% | 7.4%/6.1% | 11.0 (interpolated) | pass | 0.661 (unverified) | 0.93 |
| 35 | `cfg_7ee8` | timeframe=1min, window=2, first_days=0, entry=10:30, exit=12:00, event_filter=none, stop=1.00 | 117/0/3 | 120 | 14.9% | 2.8% | 1.00 | -3.0% | 323 | 1.84 | 1.6% | 58.7 | 8/8 | 1.00 | 0.71 | 0.29 | 4 | 5.3% | 0.65 | 0.62 | 14.0% | 13.6% | 12.5% | 13.2%/10.4% | 16.9 (interpolated) | pass | 0.457 (unverified) | 0.83 |
| 36 | `cfg_7110` | timeframe=1min, window=4, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 179/3/218 | 400 | 29.1% | 5.1% | 0.90 | -5.8% | 627 | 1.35 | 10.2% | 194.9 | 6/6 | 1.00 | 0.78 | 0.12 | 4 | 15.7% | 0.40 | 0.69 | 27.8% | 26.0% | 33.2% | 27.0%/20.8% | 10.3 (interpolated) | pass | 0.352 (unverified) | 0.79 |
| 37 | `cfg_2c88` | timeframe=1min, window=4, first_days=3, entry=10:30, exit=16:00, event_filter=skip_fomc, stop=1.00 | 341/6/53 | 400 | 43.4% | 7.3% | 0.87 | -8.3% | 257 | 1.29 | 18.0% | 197.6 | 7/7 | 1.00 | 0.75 | 0.12 | 3 | 24.8% | 0.43 | 0.53 | 41.6% | 40.1% | 40.8% | 39.1%/29.1% | 14.4 (interpolated) | pass | 0.344 (unverified) | 0.75 |
| 38 | `cfg_3f5b` | timeframe=1min, window=2, first_days=3, entry=10:30, exit=15:30, event_filter=none, stop=0.50 | 195/3/102 | 300 | 28.4% | 5.0% | 0.87 | -5.4% | 452 | 1.37 | 10.2% | 146.7 | 9/9 | 1.00 | 0.71 | 0.15 | 5 | 6.0% | 0.79 | 0.61 | 26.9% | 24.0% | 26.0% | 24.1%/16.2% | 11.9 (interpolated) | pass | 0.326 (unverified) | 0.58 |
| 39 | `cfg_f18d` | timeframe=1min, window=2, first_days=0, entry=10:30, exit=12:00, event_filter=skip_fomc, stop=1.00 | 112/0/3 | 115 | 15.1% | 2.8% | 1.01 | -3.1% | 324 | 1.87 | 1.5% | 56.3 | 8/8 | 1.00 | 0.72 | 0.28 | 4 | 5.4% | 0.64 | 0.62 | 14.7% | 14.0% | 13.0% | 13.5%/10.5% | 18.1 (interpolated) | pass | 0.461 (unverified) | 0.81 |
| 40 | `cfg_08ec` | timeframe=1min, window=2, first_days=3, entry=09:30, exit=16:00, event_filter=skip_fomc, stop=0.50 | 161/3/124 | 288 | 37.7% | 6.4% | 0.96 | -6.1% | 388 | 1.38 | 10.8% | 141.8 | 7/7 | 1.00 | 0.73 | 0.23 | 4 | 18.3% | 0.48 | 0.52 | 36.7% | 34.9% | 16.1% | 33.0%/26.5% | 16.5 (interpolated) | pass | 0.413 (unverified) | 0.10 |
| 41 | `cfg_d407` | timeframe=1min, window=2, first_days=0, entry=11:00, exit=15:00, event_filter=none, stop=0.50 | 95/2/23 | 120 | 14.9% | 2.8% | 0.92 | -2.6% | 302 | 1.72 | 3.7% | 58.3 | 9/9 | 1.00 | 0.79 | 0.13 | 4 | 9.4% | 0.37 | 0.73 | 14.5% | 14.2% | 14.2% | 13.8%/10.3% | 16.9 (interpolated) | pass | 0.364 (unverified) | 0.76 |
| 42 | `cfg_1914` | timeframe=1min, window=3, first_days=1, entry=11:00, exit=15:00, event_filter=none, stop=0.50 | 182/2/56 | 240 | 22.6% | 4.1% | 0.95 | -5.4% | 323 | 1.46 | 7.3% | 117.4 | 10/10 | 1.00 | 0.77 | 0.17 | 5 | 12.2% | 0.46 | 0.59 | 21.4% | 20.5% | 20.7% | 20.2%/15.9% | 11.8 (interpolated) | pass | 0.399 (unverified) | 0.62 |
| 43 | `cfg_bdb3` | timeframe=1min, window=0, first_days=3, entry=14:00, exit=15:00, event_filter=skip_fomc, stop=1.00 | 170/0/1 | 171 | 7.8% | 1.5% | 0.85 | -2.5% | 491 | 1.55 | 1.5% | 84.0 | 6/8 | 1.00 | 0.62 | 0.23 | 3 | 2.4% | 0.70 | 0.48 | 7.2% | 6.4% | 8.0% | 6.8%/5.6% | 7.3 (interpolated) | pass | 0.356 (unverified) | 0.52 |
| 44 | `cfg_4487` | timeframe=1min, window=4, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=0.25 | 184/3/233 | 420 | 28.7% | 5.0% | 0.87 | -5.7% | 602 | 1.32 | 10.7% | 205.1 | 6/6 | 1.00 | 0.75 | 0.13 | 4 | 17.9% | 0.38 | 0.70 | 26.8% | 25.6% | 33.0% | 26.1%/20.1% | 9.3 (interpolated) | pass | 0.323 (unverified) | 0.77 |
| 45 | `cfg_044b` | timeframe=1min, window=3, first_days=0, entry=11:00, exit=12:00, event_filter=skip_fomc, stop=1.00 | 167/0/1 | 168 | 10.3% | 1.9% | 0.99 | -2.2% | 305 | 1.60 | 1.5% | 82.1 | 7/8 | 1.00 | 0.84 | 0.15 | 3 | 4.6% | 0.55 | 0.40 | 9.9% | 9.1% | 9.8% | 9.1%/7.6% | 9.1 (interpolated) | pass | 0.453 (unverified) | 0.67 |
| 46 | `cfg_2175` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 152/2/187 | 341 | 24.1% | 4.3% | 0.85 | -5.4% | 583 | 1.35 | 8.8% | 167.5 | 7/7 | 1.00 | 0.68 | 0.17 | 4 | 10.9% | 0.55 | 0.72 | 23.0% | 22.2% | 25.5% | 22.9%/15.9% | 9.5 (interpolated) | pass | 0.304 (unverified) | 0.82 |
| 47 | `cfg_d8e1` | timeframe=1min, window=4, first_days=2, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 297/5/40 | 342 | 35.5% | 6.1% | 0.84 | -5.6% | 235 | 1.33 | 14.2% | 168.2 | 8/8 | 1.00 | 0.69 | 0.15 | 4 | 21.9% | 0.38 | 0.60 | 33.3% | 32.3% | 34.6% | 30.7%/21.6% | 13.1 (interpolated) | pass | 0.311 (unverified) | 0.71 |
| 48 | `cfg_e87a` | timeframe=1min, window=0, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=0.50 | 122/1/57 | 180 | 24.1% | 4.3% | 0.90 | -3.7% | 431 | 1.51 | 6.4% | 88.3 | 7/7 | 1.00 | 0.65 | 0.24 | 5 | 14.0% | 0.42 | 0.69 | 23.0% | 22.8% | 24.2% | 21.0%/16.8% | 17.2 (interpolated) | pass | 0.347 (unverified) | 0.73 |
| 49 | `cfg_24ad` | timeframe=1min, window=2, first_days=2, entry=11:00, exit=16:00, event_filter=none, stop=0.50 | 170/2/68 | 240 | 26.3% | 4.7% | 0.94 | -4.1% | 321 | 1.47 | 8.8% | 117.2 | 9/9 | 1.00 | 0.69 | 0.25 | 3 | 7.8% | 0.70 | 0.62 | 25.3% | 23.9% | 25.7% | 24.1%/18.2% | 14.5 (interpolated) | pass | 0.393 (unverified) | 0.77 |
| 50 | `cfg_3d5b` | timeframe=1min, window=4, first_days=2, entry=10:30, exit=16:00, event_filter=skip_fomc, stop=1.00 | 293/5/44 | 342 | 39.6% | 6.7% | 0.85 | -7.8% | 317 | 1.33 | 15.4% | 167.4 | 8/8 | 1.00 | 0.72 | 0.14 | 3 | 17.8% | 0.55 | 0.58 | 39.1% | 38.3% | 37.2% | 36.3%/26.5% | 14.9 (interpolated) | pass | 0.324 (unverified) | 0.73 |
| 51 | `cfg_9bd0` | timeframe=1min, window=2, first_days=0, entry=10:30, exit=15:00, event_filter=none, stop=0.50 | 83/2/35 | 120 | 17.1% | 3.1% | 0.85 | -3.0% | 259 | 1.63 | 3.8% | 58.8 | 9/9 | 1.00 | 0.74 | 0.11 | 5 | 7.6% | 0.55 | 0.71 | 16.3% | 16.0% | 15.1% | 15.5%/12.4% | 19.1 (interpolated) | pass | 0.308 (unverified) | 0.66 |
| 52 | `cfg_f3ff` | timeframe=1min, window=3, first_days=1, entry=11:00, exit=15:30, event_filter=none, stop=0.50 | 179/2/59 | 240 | 23.5% | 4.2% | 0.91 | -5.2% | 280 | 1.46 | 8.1% | 117.2 | 10/10 | 1.00 | 0.73 | 0.18 | 4 | 9.5% | 0.60 | 0.63 | 22.2% | 21.6% | 22.8% | 21.4%/14.5% | 12.2 (interpolated) | pass | 0.368 (unverified) | 0.56 |
| 53 | `cfg_33c5` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=15:00, event_filter=skip_fomc, stop=none | 114/0/0 | 114 | 8.1% | 1.5% | 1.25 | -2.2% | 558 | 2.15 | 1.0% | 55.9 | 6/8 | 1.00 | 0.83 | 0.42 | 4 | 2.7% | 0.67 | 0.38 | 7.7% | 7.3% | 8.2% | 7.4%/6.3% | 11.0 (interpolated) | pass | 0.661 (unverified) | 0.93 |
| 54 | `cfg_8f73` | timeframe=1min, window=0, first_days=3, entry=12:00, exit=16:00, event_filter=none, stop=0.25 | 93/1/86 | 180 | 19.0% | 3.5% | 0.97 | -3.4% | 540 | 1.61 | 4.3% | 88.2 | 6/6 | 1.00 | 0.70 | 0.27 | 4 | 8.1% | 0.57 | 0.68 | 18.5% | 17.5% | 19.4% | 17.3%/14.5% | 14.3 (interpolated) | pass | 0.407 (unverified) | 0.96 |
| 55 | `cfg_5691` | timeframe=1min, window=1, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 160/2/69 | 231 | 24.0% | 4.3% | 0.85 | -5.2% | 585 | 1.41 | 8.3% | 113.2 | 8/8 | 1.00 | 0.68 | 0.17 | 4 | 13.2% | 0.45 | 0.69 | 23.1% | 22.4% | 22.9% | 22.9%/17.7% | 14.5 (interpolated) | pass | 0.311 (unverified) | 0.70 |
| 56 | `cfg_bfaf` | timeframe=1min, window=2, first_days=0, entry=11:00, exit=15:00, event_filter=skip_fomc, stop=0.50 | 91/2/22 | 115 | 13.6% | 2.5% | 0.88 | -2.5% | 302 | 1.71 | 3.6% | 55.9 | 9/9 | 1.00 | 0.75 | 0.13 | 4 | 8.0% | 0.41 | 0.77 | 13.2% | 12.8% | 12.6% | 12.5%/9.9% | 16.2 (interpolated) | pass | 0.323 (unverified) | 0.69 |
| 57 | `cfg_f3be` | timeframe=1min, window=4, first_days=2, entry=10:30, exit=16:00, event_filter=skip_fomc, stop=0.50 | 211/3/128 | 342 | 35.0% | 6.0% | 0.85 | -6.3% | 299 | 1.34 | 12.4% | 168.1 | 8/8 | 1.00 | 0.80 | 0.05 | 3 | 14.8% | 0.58 | 0.66 | 32.4% | 29.4% | 29.1% | 31.3%/25.0% | 13.0 (interpolated) | pass | 0.316 (unverified) | 0.58 |
| 58 | `cfg_7cbc` | timeframe=1min, window=3, first_days=1, entry=10:30, exit=16:00, event_filter=skip_fomc, stop=0.50 | 141/2/83 | 226 | 24.3% | 4.3% | 0.76 | -6.0% | 539 | 1.39 | 8.2% | 110.1 | 9/9 | 1.00 | 0.61 | 0.15 | 3 | 4.4% | 0.82 | 0.81 | 23.2% | 22.5% | 17.7% | 23.0%/14.0% | 15.0 (interpolated) | pass | 0.258 (unverified) | 0.42 |
| 59 | `cfg_7345` | timeframe=1min, window=4, first_days=1, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 199/3/83 | 285 | 26.9% | 4.8% | 0.80 | -5.4% | 283 | 1.35 | 10.3% | 139.6 | 8/8 | 0.88 | 0.74 | 0.06 | 3 | 13.0% | 0.49 | 0.79 | 26.1% | 25.1% | 25.3% | 25.6%/19.5% | 12.8 (interpolated) | pass | 0.264 (unverified) | 0.67 |
| 60 | `cfg_86d1` | timeframe=1min, window=2, first_days=0, entry=10:30, exit=15:00, event_filter=skip_fomc, stop=1.00 | 105/2/8 | 115 | 20.4% | 3.7% | 0.96 | -3.3% | 194 | 1.81 | 4.4% | 56.5 | 9/9 | 1.00 | 0.79 | 0.17 | 4 | 10.5% | 0.49 | 0.64 | 19.9% | 19.5% | 15.6% | 17.0%/13.8% | 22.3 (interpolated) | pass | 0.411 (unverified) | 0.71 |
| 61 | `cfg_14a4` | timeframe=1min, window=4, first_days=0, entry=11:00, exit=15:30, event_filter=none, stop=0.50 | 174/3/63 | 240 | 22.5% | 4.0% | 0.84 | -4.1% | 367 | 1.40 | 8.0% | 118.1 | 8/8 | 1.00 | 0.73 | 0.11 | 4 | 11.7% | 0.47 | 0.74 | 21.9% | 21.3% | 22.2% | 21.3%/15.6% | 13.1 (interpolated) | pass | 0.296 (unverified) | 0.74 |
| 62 | `cfg_8371` | timeframe=1min, window=1, first_days=3, entry=09:30, exit=16:00, event_filter=skip_fomc, stop=0.50 | 127/2/102 | 231 | 30.3% | 5.3% | 0.86 | -6.7% | 325 | 1.38 | 8.6% | 113.6 | 7/7 | 1.00 | 0.63 | 0.23 | 4 | 16.8% | 0.42 | 0.62 | 29.3% | 28.4% | 12.6% | 28.2%/22.2% | 17.4 (interpolated) | pass | 0.320 (unverified) | 0.16 |
| 63 | `cfg_83bd` | timeframe=1min, window=4, first_days=1, entry=11:00, exit=15:30, event_filter=none, stop=0.50 | 217/3/80 | 300 | 24.2% | 4.3% | 0.83 | -5.6% | 261 | 1.34 | 10.0% | 146.3 | 9/9 | 1.00 | 0.78 | 0.05 | 3 | 10.6% | 0.54 | 0.69 | 22.9% | 21.4% | 22.8% | 21.1%/14.3% | 10.6 (interpolated) | pass | 0.297 (unverified) | 0.65 |
| 64 | `cfg_e8df` | timeframe=1min, window=1, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=0.50 | 165/2/73 | 240 | 27.1% | 4.8% | 0.88 | -4.4% | 541 | 1.44 | 8.6% | 118.0 | 8/8 | 1.00 | 0.61 | 0.27 | 4 | 11.4% | 0.58 | 0.71 | 26.3% | 25.6% | 26.4% | 24.8%/17.1% | 15.0 (interpolated) | pass | 0.332 (unverified) | 0.62 |
| 65 | `cfg_e440` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=0.25 | 157/2/201 | 360 | 24.2% | 4.3% | 0.83 | -5.5% | 562 | 1.33 | 9.2% | 176.5 | 7/7 | 1.00 | 0.68 | 0.15 | 5 | 10.0% | 0.59 | 0.72 | 23.1% | 21.8% | 24.3% | 21.4%/14.7% | 9.0 (interpolated) | pass | 0.287 (unverified) | 0.79 |
| 66 | `cfg_b740` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 79/0/35 | 114 | 8.4% | 1.6% | 0.92 | -2.0% | 277 | 1.66 | 1.6% | 55.6 | 7/7 | 1.00 | 0.66 | 0.26 | 5 | 4.9% | 0.42 | 0.64 | 8.0% | 7.5% | 9.8% | 7.7%/6.2% | 11.2 (interpolated) | pass | 0.368 (unverified) | 0.79 |
| 67 | `cfg_efcc` | timeframe=1min, window=2, first_days=3, entry=09:30, exit=16:00, event_filter=none, stop=0.50 | 166/3/131 | 300 | 36.9% | 6.3% | 0.92 | -6.0% | 215 | 1.35 | 11.3% | 148.2 | 7/7 | 1.00 | 0.71 | 0.21 | 5 | 17.0% | 0.50 | 0.53 | 34.9% | 33.4% | 15.2% | 31.6%/25.0% | 15.7 (interpolated) | pass | 0.380 (unverified) | 0.01 |
| 68 | `cfg_e4e6` | timeframe=1min, window=3, first_days=0, entry=10:30, exit=15:30, event_filter=none, stop=1.00 | 156/3/21 | 180 | 21.3% | 3.8% | 0.76 | -5.6% | 346 | 1.44 | 7.5% | 88.0 | 9/9 | 1.00 | 0.71 | 0.05 | 4 | 5.3% | 0.75 | 0.69 | 20.3% | 19.1% | 17.6% | 18.7%/11.9% | 14.6 (interpolated) | pass | 0.247 (unverified) | 0.48 |
| 69 | `cfg_b500` | timeframe=1min, window=2, first_days=1, entry=10:30, exit=16:00, event_filter=skip_fomc, stop=0.50 | 111/2/60 | 173 | 24.4% | 4.3% | 0.88 | -4.0% | 324 | 1.54 | 6.4% | 84.4 | 9/9 | 1.00 | 0.66 | 0.22 | 3 | 8.8% | 0.64 | 0.73 | 23.5% | 22.8% | 19.9% | 19.8%/14.7% | 18.9 (interpolated) | pass | 0.347 (unverified) | 0.56 |
| 70 | `cfg_4831` | timeframe=1min, window=4, first_days=0, entry=10:30, exit=15:30, event_filter=none, stop=1.00 | 209/4/27 | 240 | 27.8% | 4.9% | 0.83 | -6.0% | 348 | 1.38 | 10.0% | 117.5 | 8/8 | 1.00 | 0.73 | 0.10 | 3 | 15.3% | 0.41 | 0.62 | 27.4% | 26.5% | 25.2% | 23.8%/17.4% | 15.3 (interpolated) | pass | 0.310 (unverified) | 0.60 |
| 71 | `cfg_7542` | timeframe=1min, window=3, first_days=3, entry=10:30, exit=15:00, event_filter=none, stop=0.25 | 155/2/203 | 360 | 20.6% | 3.7% | 0.78 | -5.9% | 518 | 1.28 | 7.9% | 177.2 | 8/8 | 0.88 | 0.71 | 0.07 | 4 | 11.8% | 0.43 | 0.61 | 18.7% | 17.3% | 25.4% | 19.4%/14.4% | 7.8 (interpolated) | pass | 0.256 (unverified) | 0.50 |
| 72 | `cfg_a7f0` | timeframe=1min, window=0, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 118/1/54 | 173 | 21.6% | 3.9% | 0.89 | -3.6% | 475 | 1.48 | 6.1% | 84.7 | 7/7 | 1.00 | 0.62 | 0.27 | 4 | 14.3% | 0.32 | 0.66 | 20.8% | 20.0% | 21.4% | 18.9%/14.9% | 16.1 (interpolated) | pass | 0.346 (unverified) | 0.78 |
| 73 | `cfg_0916` | timeframe=1min, window=4, first_days=0, entry=11:00, exit=15:00, event_filter=none, stop=0.50 | 177/3/60 | 240 | 20.8% | 3.7% | 0.83 | -3.9% | 344 | 1.39 | 7.2% | 118.3 | 8/8 | 1.00 | 0.67 | 0.16 | 4 | 10.8% | 0.48 | 0.73 | 19.8% | 18.8% | 19.4% | 18.6%/13.4% | 12.0 (interpolated) | pass | 0.295 (unverified) | 0.67 |
| 74 | `cfg_f82e` | timeframe=1min, window=2, first_days=1, entry=10:30, exit=16:00, event_filter=none, stop=0.50 | 114/2/64 | 180 | 23.0% | 4.1% | 0.82 | -5.3% | 324 | 1.48 | 6.7% | 88.2 | 9/9 | 1.00 | 0.62 | 0.20 | 3 | 7.7% | 0.67 | 0.77 | 20.3% | 19.2% | 18.3% | 19.6%/16.3% | 17.8 (interpolated) | pass | 0.298 (unverified) | 0.53 |
| 75 | `cfg_d2aa` | timeframe=1min, window=2, first_days=0, entry=10:30, exit=16:00, event_filter=none, stop=0.50 | 78/2/40 | 120 | 18.6% | 3.4% | 0.82 | -3.8% | 368 | 1.63 | 4.5% | 58.6 | 8/8 | 1.00 | 0.72 | 0.10 | 3 | 4.8% | 0.74 | 0.84 | 18.2% | 17.6% | 14.5% | 16.5%/11.4% | 20.2 (interpolated) | pass | 0.269 (unverified) | 0.53 |
| 76 | `cfg_c078` | timeframe=1min, window=4, first_days=1, entry=10:30, exit=16:00, event_filter=skip_fomc, stop=0.50 | 177/3/105 | 285 | 30.3% | 5.3% | 0.80 | -6.4% | 281 | 1.35 | 10.3% | 140.3 | 8/8 | 1.00 | 0.72 | 0.09 | 3 | 13.0% | 0.51 | 0.76 | 29.4% | 27.7% | 28.5% | 27.0%/17.5% | 13.6 (interpolated) | pass | 0.283 (unverified) | 0.45 |
| 77 | `cfg_b748` | timeframe=1min, window=0, first_days=3, entry=09:30, exit=16:00, event_filter=skip_fomc, stop=0.50 | 94/1/78 | 173 | 23.1% | 4.1% | 0.80 | -8.6% | 432 | 1.39 | 6.4% | 85.1 | 6/6 | 1.00 | 0.67 | 0.14 | 4 | 12.4% | 0.46 | 0.66 | 22.4% | 21.7% | 12.3% | 20.5%/15.2% | 18.4 (interpolated) | pass | 0.270 (unverified) | 0.27 |
| 78 | `cfg_7b2f` | timeframe=1min, window=2, first_days=2, entry=09:30, exit=16:00, event_filter=skip_fomc, stop=0.50 | 130/2/98 | 230 | 32.0% | 5.6% | 0.91 | -5.6% | 214 | 1.44 | 8.7% | 111.9 | 8/8 | 1.00 | 0.65 | 0.26 | 5 | 15.9% | 0.45 | 0.61 | 30.7% | 29.2% | 11.9% | 28.5%/19.9% | 17.4 (interpolated) | pass | 0.368 (unverified) | 0.12 |
| 79 | `cfg_dbeb` | timeframe=1min, window=3, first_days=0, entry=11:00, exit=12:00, event_filter=skip_fomc, stop=0.50 | 158/0/10 | 168 | 9.7% | 1.8% | 0.98 | -2.6% | 325 | 1.57 | 1.5% | 82.3 | 7/8 | 1.00 | 0.74 | 0.24 | 4 | 3.4% | 0.65 | 0.42 | 9.1% | 8.5% | 7.2% | 8.6%/7.1% | 8.8 (interpolated) | pass | 0.441 (unverified) | 0.56 |
| 80 | `cfg_124e` | timeframe=1min, window=2, first_days=0, entry=11:00, exit=15:30, event_filter=none, stop=0.50 | 93/2/25 | 120 | 12.1% | 2.3% | 0.76 | -2.7% | 343 | 1.55 | 4.2% | 59.2 | 9/9 | 0.89 | 0.69 | 0.07 | 4 | 4.8% | 0.61 | 0.81 | 11.7% | 11.5% | 11.8% | 11.9%/8.3% | 14.4 (interpolated) | pass | 0.226 (unverified) | 0.57 |
| 81 | `cfg_d1ba` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=15:00, event_filter=skip_fomc, stop=0.25 | 164/2/175 | 341 | 17.2% | 3.1% | 0.76 | -3.8% | 275 | 1.28 | 7.4% | 167.1 | 8/8 | 1.00 | 0.69 | 0.07 | 5 | 8.6% | 0.50 | 0.71 | 14.6% | 13.2% | 19.1% | 13.8%/9.0% | 7.2 (interpolated) | pass | 0.239 (unverified) | 0.73 |
| 82 | `cfg_905f` | timeframe=1min, window=3, first_days=0, entry=10:30, exit=15:00, event_filter=none, stop=0.50 | 119/2/59 | 180 | 20.7% | 3.7% | 0.83 | -4.3% | 260 | 1.48 | 5.5% | 88.1 | 9/9 | 1.00 | 0.73 | 0.10 | 4 | 5.8% | 0.72 | 0.69 | 18.6% | 17.6% | 16.7% | 16.8%/11.0% | 13.9 (interpolated) | pass | 0.291 (unverified) | 0.53 |
| 83 | `cfg_dea4` | timeframe=1min, window=4, first_days=0, entry=10:30, exit=16:00, event_filter=skip_fomc, stop=1.00 | 196/4/27 | 227 | 29.1% | 5.1% | 0.77 | -6.3% | 299 | 1.37 | 10.4% | 112.0 | 7/7 | 1.00 | 0.70 | 0.07 | 3 | 16.1% | 0.44 | 0.75 | 28.6% | 27.9% | 26.7% | 26.4%/19.8% | 16.6 (interpolated) | pass | 0.250 (unverified) | 0.55 |
| 84 | `cfg_31f7` | timeframe=1min, window=4, first_days=3, entry=09:30, exit=16:00, event_filter=skip_fomc, stop=0.50 | 214/4/182 | 400 | 44.6% | 7.5% | 0.88 | -10.6% | 340 | 1.29 | 14.5% | 197.9 | 6/6 | 1.00 | 0.65 | 0.23 | 3 | 22.4% | 0.45 | 0.60 | 42.0% | 40.1% | 7.1% | 39.6%/28.8% | 13.5 (interpolated) | pass | 0.334 (unverified) | 0.10 |
| 85 | `cfg_1a0d` | timeframe=1min, window=3, first_days=0, entry=10:30, exit=15:00, event_filter=none, stop=0.25 | 83/1/96 | 180 | 16.3% | 3.0% | 0.83 | -3.0% | 347 | 1.49 | 4.1% | 88.0 | 8/8 | 0.88 | 0.66 | 0.17 | 5 | 8.8% | 0.46 | 0.71 | 15.5% | 14.5% | 13.8% | 14.4%/10.4% | 12.0 (interpolated) | pass | 0.285 (unverified) | 0.62 |
| 86 | `cfg_66f1` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=15:00, event_filter=none, stop=0.25 | 171/2/187 | 360 | 18.3% | 3.3% | 0.77 | -3.7% | 240 | 1.28 | 7.8% | 176.5 | 8/8 | 1.00 | 0.68 | 0.09 | 5 | 8.3% | 0.55 | 0.69 | 14.6% | 13.5% | 19.5% | 15.4%/10.1% | 7.2 (interpolated) | pass | 0.244 (unverified) | 0.75 |
| 87 | `cfg_995e` | timeframe=1min, window=2, first_days=3, entry=10:30, exit=15:00, event_filter=skip_fomc, stop=0.25 | 125/2/161 | 288 | 19.5% | 3.5% | 0.81 | -4.3% | 259 | 1.34 | 6.3% | 141.4 | 8/8 | 1.00 | 0.68 | 0.13 | 4 | 11.5% | 0.41 | 0.65 | 18.0% | 16.9% | 16.1% | 16.8%/12.9% | 9.4 (interpolated) | pass | 0.270 (unverified) | 0.46 |
| 88 | `cfg_9a4e` | timeframe=1min, window=2, first_days=1, entry=11:00, exit=15:00, event_filter=none, stop=0.50 | 139/2/39 | 180 | 15.8% | 2.9% | 0.84 | -5.4% | 388 | 1.46 | 5.5% | 87.4 | 10/10 | 1.00 | 0.54 | 0.30 | 5 | 10.5% | 0.34 | 0.70 | 14.9% | 14.5% | 14.0% | 14.1%/9.8% | 11.6 (interpolated) | pass | 0.299 (unverified) | 0.57 |
| 89 | `cfg_6792` | timeframe=1min, window=0, first_days=3, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 146/0/25 | 171 | 12.6% | 2.3% | 0.89 | -2.7% | 279 | 1.54 | 2.8% | 83.1 | 7/7 | 1.00 | 0.70 | 0.19 | 4 | 4.8% | 0.61 | 0.60 | 11.9% | 11.4% | 12.5% | 11.5%/8.4% | 11.1 (interpolated) | pass | 0.352 (unverified) | 0.43 |
| 90 | `cfg_fd37` | timeframe=1min, window=2, first_days=2, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 218/0/9 | 227 | 16.1% | 2.9% | 0.80 | -3.4% | 516 | 1.42 | 4.0% | 110.4 | 9/9 | 1.00 | 0.55 | 0.25 | 3 | 3.0% | 0.81 | 0.64 | 15.0% | 14.4% | 14.1% | 14.5%/11.8% | 11.0 (interpolated) | pass | 0.284 (unverified) | 0.52 |
| 91 | `cfg_0d75` | timeframe=1min, window=2, first_days=0, entry=11:00, exit=16:00, event_filter=none, stop=0.50 | 89/2/29 | 120 | 13.8% | 2.6% | 0.75 | -4.1% | 280 | 1.57 | 4.6% | 59.2 | 8/8 | 0.88 | 0.71 | 0.04 | 4 | 3.3% | 0.76 | 0.84 | 13.5% | 12.5% | 12.2% | 12.5%/8.7% | 15.5 (interpolated) | pass | 0.217 (unverified) | 0.60 |
| 92 | `cfg_e56f` | timeframe=1min, window=2, first_days=2, entry=11:00, exit=15:00, event_filter=skip_fomc, stop=0.50 | 175/2/53 | 230 | 19.9% | 3.6% | 0.90 | -4.2% | 322 | 1.44 | 6.9% | 112.3 | 10/10 | 1.00 | 0.58 | 0.32 | 4 | 8.9% | 0.56 | 0.60 | 18.7% | 16.9% | 17.3% | 17.4%/12.5% | 11.4 (interpolated) | pass | 0.362 (unverified) | 0.75 |
| 93 | `cfg_e2f8` | timeframe=1min, window=4, first_days=3, entry=09:30, exit=16:00, event_filter=none, stop=0.50 | 223/4/193 | 420 | 42.2% | 7.1% | 0.82 | -11.7% | 384 | 1.27 | 15.2% | 207.4 | 6/6 | 1.00 | 0.63 | 0.20 | 3 | 20.2% | 0.48 | 0.64 | 41.4% | 39.1% | 6.5% | 38.4%/25.9% | 12.7 (interpolated) | pass | 0.289 (unverified) | -0.02 |
| 94 | `cfg_9fb7` | timeframe=1min, window=2, first_days=0, entry=10:30, exit=16:00, event_filter=none, stop=1.00 | 107/2/11 | 120 | 19.8% | 3.6% | 0.81 | -3.4% | 346 | 1.63 | 5.6% | 58.6 | 8/8 | 1.00 | 0.62 | 0.19 | 3 | 4.8% | 0.76 | 0.79 | 19.1% | 18.7% | 16.2% | 17.9%/13.0% | 22.5 (interpolated) | pass | 0.276 (unverified) | 0.57 |
| 95 | `cfg_7b5c` | timeframe=1min, window=1, first_days=2, entry=09:30, exit=16:00, event_filter=skip_fomc, stop=0.50 | 96/1/76 | 173 | 25.3% | 4.5% | 0.84 | -4.4% | 322 | 1.45 | 6.5% | 84.3 | 8/8 | 1.00 | 0.54 | 0.29 | 5 | 13.6% | 0.46 | 0.69 | 24.8% | 24.1% | 8.2% | 22.9%/16.0% | 18.6 (interpolated) | pass | 0.294 (unverified) | 0.18 |
| 96 | `cfg_2914` | timeframe=1min, window=0, first_days=3, entry=14:00, exit=16:00, event_filter=none, stop=1.00 | 170/0/8 | 178 | 15.2% | 2.8% | 0.88 | -3.4% | 387 | 1.53 | 3.1% | 87.1 | 7/7 | 1.00 | 0.63 | 0.25 | 4 | 6.8% | 0.54 | 0.60 | 14.4% | 13.8% | 15.4% | 13.7%/11.1% | 12.6 (interpolated) | pass | 0.351 (unverified) | 0.92 |
| 97 | `cfg_c3ef` | timeframe=1min, window=0, first_days=2, entry=13:00, exit=16:00, event_filter=skip_fomc, stop=none | 114/1/0 | 115 | 15.4% | 2.8% | 0.94 | -2.8% | 319 | 1.78 | 3.0% | 56.1 | 7/7 | 1.00 | 0.64 | 0.30 | 5 | 5.4% | 0.65 | 0.57 | 15.0% | 14.5% | 15.7% | 14.0%/11.2% | 19.8 (interpolated) | pass | 0.406 (unverified) | 0.85 |
| 98 | `cfg_d23b` | timeframe=1min, window=1, first_days=2, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 147/0/24 | 171 | 12.3% | 2.3% | 0.80 | -4.1% | 644 | 1.47 | 2.8% | 83.7 | 9/9 | 1.00 | 0.53 | 0.27 | 4 | 2.5% | 0.79 | 0.70 | 11.6% | 11.2% | 15.4% | 10.6%/7.6% | 10.5 (interpolated) | pass | 0.271 (unverified) | 0.39 |
| 99 | `cfg_b70d` | timeframe=1min, window=0, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 75/1/97 | 173 | 16.8% | 3.1% | 0.84 | -4.7% | 626 | 1.48 | 4.3% | 84.3 | 6/6 | 1.00 | 0.66 | 0.18 | 4 | 11.5% | 0.32 | 0.80 | 16.1% | 15.0% | 14.7% | 15.2%/10.6% | 13.3 (interpolated) | pass | 0.289 (unverified) | 0.92 |
| 100 | `cfg_9684` | timeframe=1min, window=2, first_days=0, entry=10:00, exit=12:00, event_filter=none, stop=none | 120/0/0 | 120 | 13.9% | 2.6% | 0.84 | -2.9% | 322 | 1.66 | 2.1% | 58.5 | 7/7 | 1.00 | 0.58 | 0.26 | 3 | 4.9% | 0.65 | 0.66 | 13.3% | 12.8% | 14.4% | 12.3%/9.1% | 16.5 (interpolated) | pass | 0.323 (unverified) | 0.54 |
| 101 | `cfg_55f1` | timeframe=1min, window=0, first_days=3, entry=12:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 89/1/83 | 173 | 14.8% | 2.7% | 0.90 | -4.2% | 584 | 1.50 | 4.1% | 85.0 | 6/6 | 1.00 | 0.60 | 0.30 | 4 | 7.9% | 0.47 | 0.67 | 13.7% | 13.2% | 15.6% | 13.6%/10.4% | 12.3 (interpolated) | pass | 0.350 (unverified) | 0.94 |
| 102 | `cfg_a377` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=16:00, event_filter=none, stop=0.50 | 102/0/17 | 119 | 10.4% | 2.0% | 0.85 | -3.3% | 707 | 1.64 | 2.0% | 58.5 | 8/8 | 1.00 | 0.63 | 0.23 | 4 | 2.0% | 0.81 | 0.66 | 9.9% | 9.5% | 10.1% | 9.3%/7.0% | 12.5 (interpolated) | pass | 0.320 (unverified) | 0.53 |
| 103 | `cfg_abbe` | timeframe=1min, window=1, first_days=2, entry=14:00, exit=15:00, event_filter=skip_fomc, stop=1.00 | 171/0/0 | 171 | 6.9% | 1.3% | 0.81 | -2.9% | 584 | 1.50 | 1.5% | 83.4 | 8/10 | 1.00 | 0.57 | 0.24 | 4 | 3.0% | 0.57 | 0.56 | 6.3% | 5.7% | 8.2% | 6.2%/5.2% | 6.8 (interpolated) | pass | 0.298 (unverified) | 0.47 |
| 104 | `cfg_1ca2` | timeframe=1min, window=0, first_days=2, entry=15:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 113/0/1 | 114 | 9.5% | 1.8% | 0.86 | -1.8% | 408 | 1.85 | 1.0% | 55.6 | 7/7 | 1.00 | 0.68 | 0.18 | 4 | 5.2% | 0.45 | 0.78 | 9.1% | 8.7% | 9.6% | 9.1%/6.8% | 12.4 (interpolated) | pass | 0.297 (unverified) | 0.73 |
| 105 | `cfg_9050` | timeframe=1min, window=2, first_days=2, entry=09:30, exit=16:00, event_filter=none, stop=0.50 | 134/2/104 | 240 | 30.3% | 5.3% | 0.86 | -6.3% | 215 | 1.39 | 9.1% | 117.2 | 8/8 | 1.00 | 0.60 | 0.26 | 5 | 13.9% | 0.48 | 0.64 | 28.8% | 28.1% | 7.9% | 27.8%/18.6% | 15.8 (interpolated) | pass | 0.317 (unverified) | 0.01 |
| 106 | `cfg_bb90` | timeframe=1min, window=1, first_days=2, entry=14:00, exit=15:00, event_filter=skip_fomc, stop=none | 171/0/0 | 171 | 6.9% | 1.3% | 0.81 | -2.9% | 584 | 1.50 | 1.5% | 83.4 | 7/9 | 1.00 | 0.63 | 0.18 | 4 | 3.0% | 0.57 | 0.56 | 6.3% | 5.7% | 8.2% | 6.4%/4.6% | 6.8 (interpolated) | pass | 0.298 (unverified) | 0.47 |
| 107 | `cfg_295b` | timeframe=1min, window=4, first_days=0, entry=11:00, exit=12:00, event_filter=skip_fomc, stop=1.00 | 226/0/1 | 227 | 11.2% | 2.1% | 0.84 | -2.9% | 324 | 1.42 | 2.0% | 110.4 | 6/7 | 1.00 | 0.70 | 0.14 | 3 | 4.4% | 0.60 | 0.55 | 10.2% | 9.3% | 10.0% | 10.3%/8.2% | 7.8 (interpolated) | pass | 0.317 (unverified) | 0.59 |
| 108 | `cfg_4e6b` | timeframe=1min, window=0, first_days=2, entry=13:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 68/1/46 | 115 | 11.0% | 2.0% | 0.93 | -2.3% | 211 | 1.68 | 2.2% | 56.1 | 7/7 | 1.00 | 0.66 | 0.27 | 4 | 3.8% | 0.66 | 0.66 | 10.6% | 10.2% | 11.6% | 10.2%/7.6% | 13.6 (interpolated) | pass | 0.389 (unverified) | 0.83 |
| 109 | `cfg_81bc` | timeframe=1min, window=2, first_days=0, entry=10:30, exit=15:00, event_filter=none, stop=0.25 | 58/1/61 | 120 | 15.1% | 2.8% | 0.88 | -2.7% | 259 | 1.70 | 2.8% | 58.8 | 8/8 | 1.00 | 0.66 | 0.22 | 5 | 9.4% | 0.38 | 0.76 | 14.5% | 14.1% | 6.5% | 13.7%/10.3% | 16.4 (interpolated) | pass | 0.317 (unverified) | 0.64 |
| 110 | `cfg_86da` | timeframe=1min, window=2, first_days=0, entry=09:30, exit=12:00, event_filter=skip_fomc, stop=none | 115/0/0 | 115 | 14.5% | 2.7% | 0.77 | -3.6% | 322 | 1.54 | 2.6% | 55.7 | 6/6 | 1.00 | 0.50 | 0.27 | 3 | 7.6% | 0.48 | 0.65 | 14.0% | 13.6% | 9.9% | 13.3%/8.7% | 18.3 (interpolated) | pass | 0.273 (unverified) | 0.44 |
| 111 | `cfg_994d` | timeframe=1min, window=2, first_days=0, entry=11:00, exit=13:00, event_filter=none, stop=0.50 | 103/0/17 | 120 | 8.6% | 1.6% | 0.79 | -1.8% | 279 | 1.53 | 2.0% | 58.9 | 9/9 | 0.78 | 0.65 | 0.15 | 4 | 5.7% | 0.34 | 0.68 | 8.2% | 7.1% | 5.9% | 7.9%/5.7% | 10.4 (interpolated) | pass | 0.271 (unverified) | 0.53 |
| 112 | `cfg_f5fe` | timeframe=1min, window=1, first_days=2, entry=13:00, exit=16:00, event_filter=skip_fomc, stop=none | 171/2/0 | 173 | 17.0% | 3.1% | 0.80 | -3.9% | 515 | 1.50 | 4.6% | 84.0 | 8/8 | 1.00 | 0.55 | 0.25 | 3 | 6.6% | 0.61 | 0.68 | 16.5% | 15.7% | 17.2% | 15.8%/12.3% | 15.4 (interpolated) | pass | 0.280 (unverified) | 0.55 |
| 113 | `cfg_1961` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=16:00, event_filter=none, stop=0.25 | 80/0/39 | 119 | 7.2% | 1.4% | 0.77 | -2.0% | 321 | 1.51 | 1.7% | 58.2 | 7/7 | 1.00 | 0.53 | 0.24 | 5 | 4.0% | 0.44 | 0.74 | 6.6% | 6.2% | 8.7% | 6.6%/4.6% | 9.2 (interpolated) | pass | 0.246 (unverified) | 0.64 |
| 114 | `cfg_957e` | timeframe=1min, window=0, first_days=2, entry=12:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 62/0/53 | 115 | 12.0% | 2.2% | 0.92 | -1.9% | 387 | 1.65 | 2.7% | 56.0 | 7/7 | 1.00 | 0.66 | 0.27 | 5 | 5.9% | 0.51 | 0.66 | 11.3% | 11.0% | 12.1% | 10.6%/8.3% | 14.7 (interpolated) | pass | 0.371 (unverified) | 0.67 |
| 115 | `cfg_fcec` | timeframe=1min, window=0, first_days=3, entry=14:00, exit=15:00, event_filter=skip_fomc, stop=none | 171/0/0 | 171 | 7.8% | 1.5% | 0.85 | -2.5% | 491 | 1.55 | 1.5% | 84.0 | 5/7 | 1.00 | 0.63 | 0.22 | 3 | 2.4% | 0.70 | 0.48 | 7.2% | 6.4% | 8.1% | 7.0%/5.3% | 7.3 (interpolated) | pass | 0.357 (unverified) | 0.48 |
| 116 | `cfg_ad26` | timeframe=1min, window=3, first_days=0, entry=11:00, exit=13:00, event_filter=skip_fomc, stop=0.50 | 141/0/27 | 168 | 10.7% | 2.0% | 0.78 | -3.3% | 191 | 1.43 | 2.8% | 82.4 | 9/9 | 0.89 | 0.50 | 0.28 | 5 | 5.6% | 0.48 | 0.65 | 10.2% | 9.5% | 7.4% | 9.5%/7.4% | 9.3 (interpolated) | pass | 0.260 (unverified) | 0.50 |
| 117 | `cfg_f82b` | timeframe=1min, window=0, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=0.25 | 76/1/103 | 180 | 15.5% | 2.9% | 0.77 | -4.7% | 626 | 1.42 | 4.4% | 88.3 | 6/6 | 1.00 | 0.55 | 0.22 | 5 | 11.0% | 0.29 | 0.86 | 14.3% | 13.9% | 13.5% | 14.6%/11.3% | 11.8 (interpolated) | pass | 0.231 (unverified) | 0.83 |
| 118 | `cfg_6360` | timeframe=1min, window=0, first_days=3, entry=12:00, exit=15:00, event_filter=skip_fomc, stop=0.25 | 99/1/73 | 173 | 9.5% | 1.8% | 0.76 | -3.1% | 453 | 1.38 | 3.3% | 84.6 | 7/7 | 1.00 | 0.47 | 0.29 | 4 | 3.7% | 0.61 | 0.70 | 8.9% | 8.2% | 10.1% | 7.9%/5.8% | 8.5 (interpolated) | pass | 0.238 (unverified) | 0.90 |
| 119 | `cfg_cb08` | timeframe=1min, window=0, first_days=2, entry=15:00, exit=16:00, event_filter=skip_fomc, stop=none | 114/0/0 | 114 | 9.2% | 1.7% | 0.81 | -2.2% | 408 | 1.79 | 1.0% | 55.6 | 6/6 | 1.00 | 0.63 | 0.18 | 4 | 4.9% | 0.47 | 0.81 | 8.8% | 8.4% | 9.3% | 8.1%/5.7% | 11.9 (interpolated) | pass | 0.263 (unverified) | 0.69 |
| 120 | `cfg_1fd4` | timeframe=1min, window=0, first_days=3, entry=09:30, exit=15:00, event_filter=skip_fomc, stop=0.50 | 95/1/77 | 173 | 19.6% | 3.6% | 0.75 | -8.0% | 369 | 1.35 | 5.5% | 84.4 | 7/7 | 1.00 | 0.57 | 0.18 | 5 | 9.4% | 0.51 | 0.64 | 18.4% | 17.3% | 8.3% | 18.1%/12.8% | 15.2 (interpolated) | pass | 0.238 (unverified) | 0.25 |
| 121 | `cfg_983a` | timeframe=1min, window=3, first_days=0, entry=11:00, exit=13:00, event_filter=none, stop=0.50 | 152/0/28 | 180 | 10.7% | 2.0% | 0.77 | -3.2% | 301 | 1.41 | 3.0% | 88.3 | 9/9 | 0.89 | 0.48 | 0.29 | 5 | 5.6% | 0.48 | 0.64 | 9.6% | 8.8% | 7.2% | 8.9%/6.4% | 8.7 (interpolated) | pass | 0.253 (unverified) | 0.49 |
| 122 | `cfg_5fc7` | timeframe=1min, window=0, first_days=2, entry=09:30, exit=16:00, event_filter=skip_fomc, stop=0.50 | 63/0/52 | 115 | 18.5% | 3.4% | 0.81 | -5.5% | 368 | 1.51 | 4.3% | 55.6 | 7/7 | 1.00 | 0.58 | 0.22 | 5 | 10.9% | 0.39 | 0.72 | 18.0% | 17.4% | 7.7% | 16.6%/12.4% | 20.4 (interpolated) | pass | 0.271 (unverified) | 0.35 |
| 123 | `cfg_972d` | timeframe=1min, window=4, first_days=2, entry=13:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 190/5/147 | 342 | 16.8% | 3.1% | 0.77 | -5.1% | 258 | 1.31 | 6.5% | 166.8 | 7/7 | 1.00 | 0.50 | 0.26 | 4 | 5.6% | 0.67 | 0.80 | 15.1% | 13.7% | 15.7% | 14.4%/10.3% | 8.1 (interpolated) | pass | 0.241 (unverified) | 0.30 |
| 124 | `cfg_ff0b` | timeframe=1min, window=0, first_days=2, entry=12:00, exit=16:00, event_filter=none, stop=0.25 | 64/0/56 | 120 | 10.8% | 2.0% | 0.84 | -1.9% | 387 | 1.55 | 2.8% | 58.2 | 7/7 | 1.00 | 0.56 | 0.27 | 5 | 5.2% | 0.52 | 0.73 | 10.5% | 10.0% | 10.9% | 9.6%/6.9% | 13.0 (interpolated) | pass | 0.292 (unverified) | 0.55 |
| 125 | `cfg_865b` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=15:30, event_filter=skip_fomc, stop=none | 114/0/0 | 114 | 9.3% | 1.7% | 0.98 | -2.7% | 557 | 1.87 | 1.5% | 55.7 | 8/8 | 1.00 | 0.56 | 0.41 | 3 | 1.8% | 0.81 | 0.52 | 8.9% | 8.4% | 9.3% | 8.0%/6.3% | 12.4 (interpolated) | pass | 0.441 (unverified) | 0.87 |
| 126 | `cfg_49f0` | timeframe=1min, window=4, first_days=0, entry=11:00, exit=12:00, event_filter=skip_fomc, stop=none | 227/0/0 | 227 | 11.0% | 2.1% | 0.83 | -2.9% | 324 | 1.41 | 2.0% | 110.4 | 5/6 | 1.00 | 0.66 | 0.17 | 3 | 4.3% | 0.61 | 0.56 | 10.0% | 9.1% | 9.9% | 9.6%/7.0% | 7.7 (interpolated) | pass | 0.304 (unverified) | 0.59 |
| 127 | `cfg_1dbd` | timeframe=1min, window=0, first_days=3, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 112/0/59 | 171 | 8.9% | 1.7% | 0.78 | -2.4% | 280 | 1.42 | 2.4% | 83.3 | 6/6 | 1.00 | 0.57 | 0.22 | 5 | 6.0% | 0.31 | 0.70 | 8.3% | 7.7% | 9.7% | 8.3%/6.8% | 8.4 (interpolated) | pass | 0.257 (unverified) | 0.48 |
| 128 | `cfg_2b5f` | timeframe=1min, window=2, first_days=0, entry=10:30, exit=13:00, event_filter=skip_fomc, stop=0.25 | 63/0/52 | 115 | 12.1% | 2.2% | 0.81 | -2.1% | 238 | 1.66 | 1.6% | 55.9 | 8/8 | 1.00 | 0.55 | 0.26 | 4 | 6.4% | 0.47 | 0.86 | 11.7% | 11.3% | 6.1% | 11.0%/7.7% | 13.5 (interpolated) | pass | 0.256 (unverified) | 0.48 |
| 129 | `cfg_7f97` | timeframe=1min, window=2, first_days=0, entry=10:30, exit=13:00, event_filter=none, stop=0.25 | 67/0/53 | 120 | 12.3% | 2.3% | 0.82 | -2.2% | 259 | 1.65 | 1.7% | 58.5 | 8/8 | 1.00 | 0.53 | 0.29 | 4 | 6.6% | 0.46 | 0.85 | 11.8% | 11.5% | 5.9% | 10.9%/8.3% | 13.2 (interpolated) | pass | 0.265 (unverified) | 0.56 |
| 130 | `cfg_c2ee` | timeframe=1min, window=0, first_days=2, entry=13:00, exit=16:00, event_filter=none, stop=0.25 | 69/1/50 | 120 | 9.8% | 1.8% | 0.83 | -2.3% | 385 | 1.56 | 2.3% | 58.7 | 7/7 | 1.00 | 0.52 | 0.31 | 3 | 2.8% | 0.71 | 0.74 | 9.3% | 8.5% | 10.4% | 8.7%/6.3% | 11.5 (interpolated) | pass | 0.298 (unverified) | 0.70 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 2.2% / 0.99 / 21 | 1.3% / 0.90 / 23 | 4.5% / 1.40 / 23 | 0.6% / 0.32 / 24 | 9.1% / 2.85 / 23 |
| 2 | 5.7% / 0.86 / 72 | 4.3% / 1.05 / 72 | 9.1% / 1.29 / 72 | -2.9% / -0.73 / 72 | 25.2% / 2.25 / 72 |
| 3 | 6.8% / 1.17 / 72 | 2.2% / 0.58 / 72 | 7.7% / 1.48 / 72 | 2.0% / 0.57 / 72 | 14.5% / 1.76 / 72 |
| 4 | 5.6% / 0.94 / 72 | 1.8% / 0.50 / 72 | 8.5% / 1.42 / 72 | -0.7% / -0.17 / 72 | 21.0% / 2.18 / 72 |
| 5 | 6.8% / 1.02 / 68 | 4.1% / 1.08 / 68 | 9.3% / 1.34 / 68 | -2.4% / -0.62 / 68 | 18.8% / 1.96 / 69 |
| 6 | 14.5% / 1.57 / 84 | 3.5% / 0.77 / 84 | 14.2% / 1.82 / 84 | -5.0% / -1.09 / 84 | 17.0% / 1.55 / 84 |
| 7 | 12.0% / 1.56 / 84 | 1.0% / 0.26 / 84 | 13.3% / 2.04 / 84 | -2.7% / -0.69 / 84 | 13.0% / 1.38 / 84 |
| 8 | 2.2% / 0.99 / 21 | 1.3% / 0.90 / 23 | 5.0% / 1.69 / 23 | -0.1% / -0.02 / 24 | 9.1% / 2.85 / 23 |
| 9 | 6.7% / 1.17 / 60 | 4.5% / 1.11 / 60 | 9.1% / 1.43 / 60 | -3.1% / -0.89 / 60 | 18.9% / 1.96 / 60 |
| 10 | 7.6% / 1.32 / 57 | 4.1% / 1.15 / 56 | 9.2% / 1.47 / 58 | -3.9% / -1.16 / 59 | 15.4% / 1.80 / 58 |
| 11 | -0.5% / -0.06 / 56 | 1.9% / 0.59 / 56 | 7.1% / 1.19 / 56 | 1.0% / 0.28 / 57 | 21.1% / 2.27 / 58 |
| 12 | 7.9% / 1.55 / 60 | 2.5% / 0.70 / 60 | 5.1% / 1.18 / 60 | 1.2% / 0.38 / 60 | 11.2% / 1.49 / 60 |
| 13 | 8.5% / 1.67 / 57 | 1.4% / 0.47 / 56 | 4.9% / 1.17 / 58 | 0.6% / 0.19 / 59 | 9.3% / 1.33 / 58 |
| 14 | 3.8% / 1.16 / 33 | 1.7% / 1.13 / 34 | 7.8% / 1.94 / 35 | -2.4% / -0.88 / 35 | 6.8% / 1.86 / 34 |
| 15 | 3.0% / 0.46 / 68 | 1.8% / 0.44 / 68 | 4.9% / 0.66 / 68 | -1.7% / -0.35 / 68 | 23.2% / 2.13 / 69 |
| 16 | 0.7% / 0.13 / 72 | 2.1% / 0.46 / 72 | 5.5% / 0.74 / 72 | -1.6% / -0.32 / 72 | 28.9% / 2.40 / 72 |
| 17 | 3.6% / 0.87 / 36 | 1.6% / 0.65 / 36 | 5.7% / 1.42 / 36 | 0.2% / 0.09 / 36 | 9.2% / 1.53 / 36 |
| 18 | 0.8% / 0.37 / 21 | 0.5% / 0.32 / 23 | 1.0% / 0.49 / 23 | 1.5% / 0.98 / 24 | 8.7% / 2.54 / 23 |
| 19 | 2.0% / 0.35 / 60 | 3.8% / 0.87 / 60 | 7.8% / 1.07 / 60 | -2.8% / -0.67 / 60 | 22.4% / 2.15 / 60 |
| 20 | 7.7% / 0.97 / 68 | 0.8% / 0.23 / 68 | 13.4% / 1.78 / 68 | -1.5% / -0.38 / 69 | 13.7% / 1.52 / 69 |
| 21 | 1.5% / 0.81 / 23 | 0.6% / 0.61 / 21 | 3.6% / 2.36 / 23 | -1.0% / -0.63 / 24 | 4.9% / 2.37 / 24 |
| 22 | 3.8% / 0.65 / 57 | 3.3% / 0.84 / 56 | 7.8% / 1.08 / 58 | -3.6% / -0.93 / 59 | 18.8% / 2.00 / 58 |
| 23 | -0.2% / -0.07 / 32 | 1.2% / 0.74 / 33 | 8.6% / 1.78 / 35 | -0.8% / -0.35 / 36 | 8.3% / 1.74 / 35 |
| 24 | 7.2% / 0.84 / 84 | 1.5% / 0.32 / 84 | 11.9% / 1.37 / 84 | -4.4% / -0.97 / 84 | 21.4% / 1.81 / 84 |
| 25 | 1.1% / 0.59 / 24 | 0.8% / 0.74 / 24 | 3.5% / 2.33 / 24 | -0.8% / -0.52 / 24 | 4.9% / 2.37 / 24 |
| 26 | 0.9% / 0.58 / 21 | -0.2% / -0.15 / 23 | 1.9% / 1.06 / 23 | -0.6% / -0.43 / 24 | 7.2% / 2.92 / 23 |
| 27 | 3.0% / 0.51 / 60 | 1.4% / 0.37 / 60 | 4.1% / 0.87 / 60 | 2.7% / 0.66 / 60 | 15.4% / 1.80 / 60 |
| 28 | -1.6% / -0.27 / 60 | 2.3% / 0.62 / 60 | 7.2% / 1.19 / 60 | -0.2% / -0.04 / 60 | 21.7% / 2.28 / 60 |
| 29 | 5.2% / 0.69 / 84 | -0.6% / -0.11 / 84 | 9.5% / 1.39 / 84 | -1.5% / -0.30 / 84 | 18.4% / 1.72 / 84 |
| 30 | 1.6% / 0.44 / 44 | 1.6% / 0.94 / 44 | 12.2% / 2.21 / 47 | -3.8% / -1.34 / 47 | 5.8% / 1.16 / 46 |
| 31 | -0.1% / 0.01 / 45 | 1.8% / 0.60 / 44 | 7.1% / 1.34 / 46 | -0.4% / -0.11 / 48 | 18.0% / 2.19 / 47 |
| 32 | -0.9% / -0.13 / 56 | -1.7% / -0.44 / 56 | 4.9% / 0.72 / 56 | 1.1% / 0.28 / 57 | 24.1% / 2.26 / 58 |
| 33 | 3.6% / 0.87 / 34 | 0.5% / 0.28 / 33 | 5.0% / 1.27 / 33 | 1.3% / 0.60 / 33 | 8.3% / 1.40 / 35 |
| 34 | 1.1% / 1.26 / 21 | -0.9% / -0.78 / 23 | 1.1% / 0.76 / 23 | 1.3% / 1.39 / 24 | 5.3% / 3.23 / 23 |
| 35 | 0.1% / 0.04 / 24 | 1.0% / 0.87 / 24 | 4.6% / 1.53 / 24 | -0.5% / -0.15 / 24 | 9.2% / 2.35 / 24 |
| 36 | 11.6% / 1.47 / 80 | 2.2% / 0.59 / 80 | 6.0% / 1.04 / 80 | -1.6% / -0.46 / 80 | 8.5% / 1.16 / 80 |
| 37 | 16.1% / 1.53 / 80 | -1.7% / -0.28 / 80 | 12.8% / 1.31 / 80 | -3.0% / -0.52 / 80 | 14.9% / 1.31 / 80 |
| 38 | 1.5% / 0.28 / 60 | 0.9% / 0.24 / 60 | 3.5% / 0.70 / 60 | 0.0% / 0.03 / 60 | 21.1% / 2.14 / 60 |
| 39 | 0.5% / 0.24 / 23 | 0.7% / 0.65 / 21 | 4.8% / 1.59 / 23 | -0.7% / -0.20 / 24 | 9.2% / 2.35 / 24 |
| 40 | 6.8% / 0.93 / 57 | 3.3% / 0.62 / 56 | 16.4% / 2.12 / 58 | -0.0% / 0.02 / 59 | 7.2% / 0.82 / 58 |
| 41 | 4.4% / 1.45 / 24 | 2.0% / 0.89 / 24 | 3.2% / 1.09 / 24 | -0.4% / -0.21 / 24 | 5.0% / 1.06 / 24 |
| 42 | 2.7% / 0.62 / 48 | 0.0% / 0.03 / 48 | 7.3% / 1.67 / 48 | 1.8% / 0.59 / 48 | 9.2% / 1.43 / 48 |
| 43 | 1.1% / 0.53 / 33 | -1.3% / -0.95 / 34 | 2.5% / 1.39 / 35 | -0.0% / 0.00 / 35 | 5.3% / 2.34 / 34 |
| 44 | 10.2% / 1.29 / 84 | 2.7% / 0.68 / 84 | 6.1% / 1.03 / 84 | -1.8% / -0.50 / 84 | 9.2% / 1.21 / 84 |
| 45 | 0.6% / 0.30 / 34 | -0.4% / -0.26 / 33 | 4.6% / 2.38 / 33 | -0.2% / -0.15 / 33 | 5.4% / 2.09 / 35 |
| 46 | 4.1% / 0.78 / 68 | 1.9% / 0.57 / 68 | 4.6% / 0.83 / 68 | -0.1% / -0.02 / 68 | 12.0% / 1.58 / 69 |
| 47 | 9.6% / 1.03 / 68 | 0.4% / 0.12 / 68 | 11.4% / 1.34 / 68 | -0.6% / -0.12 / 69 | 11.2% / 1.16 / 69 |
| 48 | 6.2% / 1.19 / 36 | 1.8% / 0.57 / 36 | 5.4% / 1.03 / 36 | 0.0% / 0.03 / 36 | 8.9% / 1.25 / 36 |
| 49 | -0.8% / -0.18 / 48 | 2.1% / 0.60 / 48 | 6.9% / 1.29 / 48 | -0.4% / -0.11 / 48 | 17.1% / 2.10 / 48 |
| 50 | 9.9% / 1.06 / 68 | -4.1% / -0.82 / 68 | 12.5% / 1.31 / 68 | -0.7% / -0.10 / 69 | 18.5% / 1.66 / 69 |
| 51 | 0.5% / 0.13 / 24 | 1.1% / 0.47 / 24 | 4.5% / 1.29 / 24 | 1.4% / 0.50 / 24 | 8.8% / 1.57 / 24 |
| 52 | 1.3% / 0.31 / 48 | -0.7% / -0.24 / 48 | 8.2% / 1.68 / 48 | 0.6% / 0.20 / 48 | 12.8% / 1.72 / 48 |
| 53 | 1.1% / 1.26 / 21 | -0.9% / -0.78 / 23 | 1.1% / 0.76 / 23 | 1.3% / 1.39 / 24 | 5.3% / 3.23 / 23 |
| 54 | 5.3% / 1.55 / 36 | 2.6% / 1.10 / 36 | 0.8% / 0.25 / 36 | -0.8% / -0.36 / 36 | 10.1% / 1.67 / 36 |
| 55 | 6.2% / 1.14 / 45 | 3.7% / 1.08 / 46 | 5.4% / 0.95 / 47 | -2.4% / -0.75 / 47 | 9.6% / 1.30 / 46 |
| 56 | 4.8% / 1.58 / 23 | 0.9% / 0.67 / 21 | 2.6% / 0.93 / 23 | -0.4% / -0.21 / 24 | 5.2% / 1.09 / 24 |
| 57 | 5.8% / 0.76 / 68 | -2.3% / -0.51 / 68 | 13.0% / 1.49 / 68 | -1.7% / -0.38 / 69 | 17.5% / 1.66 / 69 |
| 58 | -1.8% / -0.34 / 45 | -2.0% / -0.64 / 44 | 6.7% / 0.99 / 45 | 1.7% / 0.48 / 45 | 19.0% / 1.99 / 47 |
| 59 | 8.7% / 1.16 / 57 | -0.6% / -0.18 / 56 | 12.3% / 1.74 / 57 | -3.1% / -0.91 / 57 | 8.0% / 0.98 / 58 |
| 60 | 3.7% / 0.97 / 23 | -0.0% / -0.02 / 21 | 5.8% / 1.57 / 23 | 0.8% / 0.27 / 24 | 8.9% / 1.44 / 24 |
| 61 | 8.2% / 1.39 / 48 | 0.6% / 0.23 / 48 | 9.7% / 1.84 / 48 | -2.6% / -0.96 / 48 | 5.2% / 0.76 / 48 |
| 62 | 7.0% / 1.04 / 45 | 3.1% / 0.59 / 46 | 11.6% / 1.71 / 47 | -1.0% / -0.23 / 47 | 6.9% / 0.85 / 46 |
| 63 | 7.4% / 1.20 / 60 | -1.2% / -0.33 / 60 | 12.4% / 2.12 / 60 | -1.5% / -0.44 / 60 | 5.7% / 0.80 / 60 |
| 64 | 5.3% / 0.97 / 48 | 2.2% / 0.64 / 48 | 5.2% / 0.90 / 48 | -1.5% / -0.45 / 48 | 14.1% / 1.60 / 48 |
| 65 | 2.7% / 0.51 / 72 | 2.3% / 0.63 / 72 | 4.4% / 0.77 / 72 | 0.4% / 0.12 / 72 | 12.9% / 1.66 / 72 |
| 66 | 0.7% / 0.39 / 21 | 1.7% / 1.34 / 23 | 1.0% / 0.59 / 23 | 1.4% / 1.02 / 24 | 3.3% / 1.39 / 23 |
| 67 | 5.5% / 0.76 / 60 | 3.4% / 0.60 / 60 | 17.0% / 2.14 / 60 | 1.0% / 0.24 / 60 | 6.1% / 0.70 / 60 |
| 68 | 0.7% / 0.15 / 36 | -1.7% / -0.50 / 36 | 5.6% / 1.19 / 36 | 0.8% / 0.24 / 36 | 15.1% / 1.82 / 36 |
| 69 | -1.2% / -0.30 / 34 | -0.7% / -0.23 / 32 | 10.8% / 1.62 / 35 | 0.0% / 0.02 / 36 | 14.4% / 1.83 / 36 |
| 70 | 8.6% / 1.27 / 48 | -2.4% / -0.60 / 48 | 10.9% / 1.84 / 48 | -0.1% / 0.01 / 48 | 8.8% / 1.01 / 48 |
| 71 | 6.5% / 1.11 / 72 | 2.2% / 0.58 / 72 | -2.7% / -0.66 / 72 | 5.6% / 1.38 / 72 | 7.9% / 1.21 / 72 |
| 72 | 6.8% / 1.32 / 34 | 2.6% / 0.81 / 35 | 6.4% / 1.22 / 35 | -0.8% / -0.27 / 35 | 5.1% / 0.94 / 34 |
| 73 | 9.0% / 1.56 / 48 | 1.1% / 0.35 / 48 | 9.0% / 1.85 / 48 | -1.9% / -0.76 / 48 | 2.5% / 0.43 / 48 |
| 74 | -2.9% / -0.74 / 36 | -0.3% / -0.09 / 36 | 11.2% / 1.66 / 36 | 0.0% / 0.02 / 36 | 14.2% / 1.80 / 36 |
| 75 | -2.0% / -0.65 / 24 | 1.6% / 0.66 / 24 | 6.7% / 1.26 / 24 | -1.3% / -0.52 / 24 | 13.1% / 1.91 / 24 |
| 76 | 4.8% / 0.66 / 57 | -2.8% / -0.72 / 56 | 15.3% / 1.75 / 57 | -0.8% / -0.19 / 57 | 11.9% / 1.28 / 58 |
| 77 | 8.3% / 1.28 / 34 | 3.0% / 0.60 / 35 | 9.5% / 1.84 / 35 | -0.5% / -0.11 / 35 | 1.2% / 0.22 / 34 |
| 78 | 1.9% / 0.36 / 45 | 0.5% / 0.12 / 44 | 14.0% / 1.88 / 46 | 1.4% / 0.35 / 48 | 11.7% / 1.29 / 47 |
| 79 | 0.9% / 0.42 / 34 | -0.6% / -0.38 / 33 | 3.1% / 1.62 / 33 | 0.0% / 0.01 / 33 | 6.1% / 2.51 / 35 |
| 80 | 2.8% / 1.16 / 24 | 1.3% / 0.65 / 24 | 2.1% / 0.72 / 24 | -1.5% / -0.86 / 24 | 7.0% / 1.38 / 24 |
| 81 | 3.4% / 0.69 / 68 | 0.5% / 0.17 / 68 | 1.8% / 0.52 / 68 | 2.7% / 0.87 / 68 | 7.9% / 1.31 / 69 |
| 82 | -0.4% / -0.06 / 36 | 0.0% / 0.03 / 36 | 4.1% / 0.98 / 36 | 2.1% / 0.66 / 36 | 14.0% / 1.92 / 36 |
| 83 | 10.6% / 1.27 / 46 | -1.7% / -0.50 / 45 | 9.3% / 1.23 / 45 | -2.2% / -0.51 / 45 | 11.1% / 1.16 / 46 |
| 84 | 15.7% / 1.57 / 80 | -3.7% / -0.57 / 80 | 18.1% / 1.82 / 80 | -3.3% / -0.58 / 80 | 13.7% / 1.14 / 80 |
| 85 | 3.6% / 0.84 / 36 | 0.5% / 0.20 / 36 | 0.0% / 0.03 / 36 | 4.4% / 1.58 / 36 | 7.0% / 1.36 / 36 |
| 86 | 2.0% / 0.42 / 72 | 1.3% / 0.41 / 72 | 2.2% / 0.61 / 72 | 2.5% / 0.80 / 72 | 9.2% / 1.42 / 72 |
| 87 | 7.0% / 1.27 / 57 | 1.1% / 0.36 / 56 | -0.5% / -0.11 / 58 | 3.6% / 0.98 / 59 | 7.2% / 1.18 / 58 |
| 88 | 3.8% / 1.09 / 36 | 0.4% / 0.15 / 36 | 4.7% / 1.40 / 36 | 1.4% / 0.52 / 36 | 4.8% / 0.93 / 36 |
| 89 | 1.7% / 0.56 / 33 | 1.0% / 0.60 / 34 | 2.8% / 1.06 / 35 | -0.7% / -0.33 / 35 | 7.4% / 2.00 / 34 |
| 90 | -1.4% / -0.40 / 44 | 1.0% / 0.61 / 43 | 6.6% / 1.28 / 45 | -3.0% / -1.20 / 48 | 12.7% / 2.38 / 47 |
| 91 | 0.7% / 0.29 / 24 | 2.6% / 1.19 / 24 | 3.3% / 0.98 / 24 | -3.3% / -1.54 / 24 | 10.3% / 1.67 / 24 |
| 92 | 2.3% / 0.58 / 45 | -0.4% / -0.15 / 44 | 3.8% / 1.05 / 46 | 3.0% / 1.00 / 48 | 10.2% / 1.58 / 47 |
| 93 | 14.0% / 1.40 / 84 | -3.6% / -0.51 / 84 | 18.2% / 1.84 / 84 | -4.6% / -0.84 / 84 | 14.6% / 1.17 / 84 |
| 94 | -0.9% / -0.25 / 24 | 1.1% / 0.41 / 24 | 8.1% / 1.49 / 24 | -3.3% / -1.03 / 24 | 14.3% / 1.99 / 24 |
| 95 | 2.7% / 0.55 / 33 | 0.1% / 0.05 / 34 | 9.2% / 1.45 / 35 | 1.1% / 0.32 / 36 | 10.3% / 1.32 / 35 |
| 96 | 3.4% / 1.04 / 35 | 0.7% / 0.41 / 35 | 7.9% / 1.94 / 36 | -1.6% / -0.53 / 36 | 4.2% / 1.04 / 36 |
| 97 | 0.4% / 0.15 / 22 | 0.6% / 0.22 / 23 | 3.9% / 1.57 / 23 | 0.4% / 0.16 / 24 | 9.5% / 2.25 / 23 |
| 98 | -1.0% / -0.37 / 32 | 0.7% / 0.37 / 33 | 2.9% / 0.92 / 35 | 0.0% / 0.02 / 36 | 9.5% / 2.04 / 35 |
| 99 | 4.8% / 1.18 / 34 | 2.4% / 0.87 / 35 | 4.0% / 0.86 / 35 | -0.2% / -0.07 / 35 | 4.7% / 1.09 / 34 |
| 100 | -0.7% / -0.30 / 24 | 0.3% / 0.19 / 24 | 5.7% / 1.50 / 24 | -0.3% / -0.10 / 24 | 8.6% / 1.83 / 24 |
| 101 | 5.3% / 1.56 / 34 | 3.0% / 1.25 / 35 | 1.1% / 0.34 / 35 | -1.6% / -0.82 / 35 | 6.4% / 1.54 / 34 |
| 102 | 0.5% / 0.20 / 23 | -0.2% / -0.11 / 24 | 0.4% / 0.18 / 24 | 1.4% / 0.92 / 24 | 8.3% / 2.34 / 24 |
| 103 | 0.5% / 0.41 / 32 | -1.6% / -1.31 / 33 | 2.7% / 1.38 / 35 | 1.4% / 1.37 / 36 | 3.8% / 1.54 / 35 |
| 104 | 0.9% / 0.59 / 21 | 2.0% / 1.87 / 23 | 3.8% / 1.23 / 23 | -1.5% / -0.91 / 24 | 4.1% / 1.48 / 23 |
| 105 | 0.6% / 0.13 / 48 | 0.7% / 0.16 / 48 | 14.4% / 1.92 / 48 | 1.2% / 0.32 / 48 | 11.1% / 1.22 / 48 |
| 106 | 0.5% / 0.41 / 32 | -1.6% / -1.31 / 33 | 2.7% / 1.38 / 35 | 1.4% / 1.37 / 36 | 3.8% / 1.54 / 35 |
| 107 | 4.7% / 1.38 / 46 | -0.8% / -0.45 / 45 | 6.4% / 2.88 / 45 | -1.7% / -0.81 / 45 | 2.2% / 0.73 / 46 |
| 108 | -0.6% / -0.26 / 22 | 2.5% / 1.40 / 23 | 0.2% / 0.12 / 23 | 1.6% / 0.96 / 24 | 6.9% / 1.98 / 23 |
| 109 | 2.6% / 0.73 / 24 | 1.1% / 0.51 / 24 | 2.3% / 0.75 / 24 | 3.1% / 1.24 / 24 | 5.2% / 1.17 / 24 |
| 110 | -0.0% / 0.00 / 23 | -0.6% / -0.28 / 21 | 6.5% / 1.36 / 23 | 1.6% / 0.51 / 24 | 6.4% / 1.42 / 24 |
| 111 | 1.8% / 0.98 / 24 | 1.5% / 1.04 / 24 | 2.5% / 1.12 / 24 | -0.2% / -0.09 / 24 | 2.8% / 0.94 / 24 |
| 112 | -0.9% / -0.27 / 33 | 0.9% / 0.30 / 34 | 7.7% / 2.22 / 35 | -0.9% / -0.29 / 36 | 9.7% / 1.51 / 35 |
| 113 | 0.6% / 0.29 / 23 | 1.3% / 0.99 / 24 | 0.7% / 0.40 / 24 | 1.4% / 1.02 / 24 | 3.1% / 1.26 / 24 |
| 114 | 2.3% / 0.89 / 22 | 2.3% / 1.16 / 23 | 0.8% / 0.36 / 23 | 0.4% / 0.24 / 24 | 5.8% / 1.57 / 23 |
| 115 | 1.1% / 0.54 / 33 | -1.3% / -0.95 / 34 | 2.5% / 1.39 / 35 | -0.0% / 0.00 / 35 | 5.3% / 2.34 / 34 |
| 116 | 0.9% / 0.32 / 34 | 1.0% / 0.61 / 33 | 3.1% / 1.11 / 33 | 0.6% / 0.27 / 33 | 4.9% / 1.38 / 35 |
| 117 | 4.1% / 0.99 / 36 | 2.0% / 0.71 / 36 | 3.8% / 0.80 / 36 | 0.7% / 0.29 / 36 | 4.1% / 0.94 / 36 |
| 118 | 2.3% / 0.92 / 34 | 1.0% / 0.52 / 35 | 0.6% / 0.29 / 35 | -0.2% / -0.15 / 35 | 5.6% / 1.56 / 34 |
| 119 | 0.9% / 0.59 / 21 | 2.0% / 1.87 / 23 | 3.8% / 1.23 / 23 | -1.8% / -0.96 / 24 | 4.1% / 1.48 / 23 |
| 120 | 5.7% / 1.04 / 34 | 0.8% / 0.20 / 35 | 9.4% / 2.00 / 35 | 1.2% / 0.33 / 35 | 1.3% / 0.27 / 34 |
| 121 | 1.0% / 0.35 / 36 | 1.1% / 0.67 / 36 | 3.4% / 1.21 / 36 | 0.0% / 0.01 / 36 | 4.9% / 1.38 / 36 |
| 122 | 4.2% / 0.90 / 22 | 0.3% / 0.09 / 23 | 6.8% / 1.59 / 23 | 1.7% / 0.53 / 24 | 4.4% / 0.85 / 23 |
| 123 | -0.6% / -0.14 / 68 | 2.6% / 1.01 / 68 | 0.4% / 0.12 / 68 | 3.2% / 0.96 / 69 | 10.7% / 1.62 / 69 |
| 124 | 2.2% / 0.87 / 24 | 2.0% / 0.97 / 24 | 0.5% / 0.22 / 24 | 0.4% / 0.29 / 24 | 5.3% / 1.46 / 24 |
| 125 | 0.9% / 0.58 / 21 | -0.2% / -0.15 / 23 | 1.9% / 1.06 / 23 | -0.8% / -0.51 / 24 | 7.4% / 2.97 / 23 |
| 126 | 4.7% / 1.38 / 46 | -0.8% / -0.45 / 45 | 6.4% / 2.88 / 45 | -1.7% / -0.81 / 45 | 2.1% / 0.67 / 46 |
| 127 | 1.8% / 0.69 / 33 | 1.4% / 1.01 / 34 | 2.7% / 1.11 / 35 | 0.4% / 0.24 / 35 | 2.3% / 0.90 / 34 |
| 128 | -0.3% / -0.12 / 23 | 0.2% / 0.15 / 21 | 2.9% / 0.78 / 23 | 3.5% / 1.40 / 24 | 5.3% / 1.40 / 24 |
| 129 | -0.7% / -0.30 / 24 | 0.6% / 0.42 / 24 | 3.1% / 0.82 / 24 | 3.5% / 1.40 / 24 | 5.3% / 1.40 / 24 |
| 130 | -0.8% / -0.36 / 24 | 2.1% / 1.17 / 24 | -0.1% / -0.06 / 24 | 1.7% / 0.96 / 24 | 6.8% / 1.93 / 24 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_0639` | 8 | 0.82 | 0.83/0.89 | 0.78/0.87 |
| 1 | `cfg_044b` | 6 | 0.89 | 0.91/0.97 | 0.91/0.93 |
| 2 | `cfg_9684` | 3 | 0.88 | 0.79/0.79 | 0.77/0.79 |
| 3 | `cfg_c8da` | 6 | 0.86 | 0.87/0.93 | 0.80/0.88 |
| 4 | `cfg_1914` | 6 | 0.88 | 0.83/0.93 | 0.78/0.85 |
| 5 | `cfg_08ec` | 6 | 0.92 | 0.94/0.95 | 0.83/0.89 |
| 6 | `cfg_14a4` | 4 | 0.92 | 0.93/0.96 | 0.85/0.90 |
| 7 | `cfg_3932` | 5 | 0.84 | 0.85/0.89 | 0.78/0.81 |
| 8 | `cfg_9883` | 3 | 0.92 | 0.95/0.96 | 0.97/0.98 |
| 9 | `cfg_124e` | 2 | 0.92 | 0.93/0.93 | 0.91/0.91 |
| 10 | `cfg_3d0c` | 6 | 0.90 | 0.87/0.91 | 0.80/0.87 |
| 11 | `cfg_0efe` | 6 | 0.89 | 0.88/0.91 | 0.80/0.87 |
| 12 | `cfg_611f` | 5 | 0.89 | 0.87/0.96 | 0.96/0.96 |
| 13 | `cfg_3865` | 6 | 0.88 | 0.89/0.99 | 0.93/0.96 |
| 14 | `cfg_d2aa` | 4 | 0.88 | 0.91/0.92 | 0.78/0.82 |
| 15 | `cfg_b740` | 2 | 0.98 | 0.99/0.99 | 0.98/0.98 |
| 16 | `cfg_3f57` | 5 | 0.82 | 0.88/0.94 | 0.81/0.87 |
| 17 | `cfg_1a0d` | 3 | 0.87 | 0.86/0.87 | 0.65/0.67 |
| 18 | `cfg_9bd0` | 8 | 0.80 | 0.86/0.91 | 0.71/0.79 |
| 19 | `cfg_1b7e` | 4 | 0.88 | 0.91/0.95 | 0.86/0.90 |
| 20 | `cfg_1ca2` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 21 | `cfg_1dbd` | 1 | n/a | n/a/n/a | n/a/n/a |
| 22 | `cfg_b748` | 2 | 0.97 | 0.97/0.97 | 0.87/0.87 |
| 23 | `cfg_20eb` | 4 | 0.87 | 0.87/0.95 | 0.95/0.96 |
| 24 | `cfg_2175` | 4 | 0.90 | 0.92/0.93 | 0.82/0.84 |
| 25 | `cfg_c52c` | 5 | 0.82 | 0.85/0.88 | 0.73/0.82 |
| 26 | `cfg_6604` | 4 | 0.87 | 0.85/0.91 | 0.84/0.88 |
| 27 | `cfg_295b` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 28 | `cfg_2b5f` | 2 | 0.99 | 0.99/0.99 | 0.94/0.94 |
| 29 | `cfg_2c88` | 5 | 0.81 | 0.87/0.91 | 0.81/0.87 |
| 30 | `cfg_31f7` | 4 | 0.84 | 0.91/0.93 | 0.82/0.86 |
| 31 | `cfg_7ee8` | 6 | 0.89 | 0.88/0.99 | 0.59/0.95 |
| 32 | `cfg_7110` | 6 | 0.83 | 0.92/0.94 | 0.84/0.88 |
| 33 | `cfg_95c0` | 7 | 0.82 | 0.86/0.90 | 0.79/0.87 |
| 34 | `cfg_ff31` | 4 | 0.86 | 0.85/0.90 | 0.84/0.88 |
| 35 | `cfg_7345` | 6 | 0.88 | 0.85/0.90 | 0.78/0.87 |
| 36 | `cfg_4831` | 5 | 0.85 | 0.89/0.95 | 0.86/0.89 |
| 37 | `cfg_7db7` | 3 | 0.93 | 0.92/0.96 | 0.96/0.98 |
| 38 | `cfg_4e6b` | 2 | 0.99 | 0.99/0.99 | 0.96/0.96 |
| 39 | `cfg_9a4e` | 4 | 0.82 | 0.85/0.87 | 0.73/0.76 |
| 40 | `cfg_55f1` | 3 | 0.85 | 0.84/0.88 | 0.77/0.78 |
| 41 | `cfg_5691` | 2 | 0.91 | 0.92/0.92 | 0.96/0.96 |
| 42 | `cfg_8371` | 3 | 0.83 | 0.87/0.93 | 0.76/0.86 |
| 43 | `cfg_5fc7` | 1 | n/a | n/a/n/a | n/a/n/a |
| 44 | `cfg_d1ba` | 2 | 0.95 | 0.97/0.97 | 0.95/0.95 |
| 45 | `cfg_6792` | 1 | n/a | n/a/n/a | n/a/n/a |
| 46 | `cfg_7542` | 4 | 0.90 | 0.91/0.94 | 0.81/0.84 |
| 47 | `cfg_b565` | 3 | 0.87 | 0.89/0.94 | 0.75/0.87 |
| 48 | `cfg_d407` | 4 | 0.86 | 0.90/0.94 | 0.86/0.90 |
| 49 | `cfg_7b2f` | 4 | 0.93 | 0.94/0.95 | 0.83/0.86 |
| 50 | `cfg_8b30` | 2 | 0.91 | 0.91/0.91 | 0.80/0.80 |
| 51 | `cfg_819b` | 2 | 0.97 | 0.97/0.97 | 0.97/0.97 |
| 52 | `cfg_a38e` | 6 | 0.88 | 0.85/0.90 | 0.78/0.86 |
| 53 | `cfg_8f73` | 1 | n/a | n/a/n/a | n/a/n/a |
| 54 | `cfg_e4e6` | 2 | 0.88 | 0.87/0.87 | 0.74/0.74 |
| 55 | `cfg_957e` | 2 | 0.99 | 0.99/0.99 | 0.97/0.97 |
| 56 | `cfg_972d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 57 | `cfg_ad26` | 2 | 0.99 | 0.99/0.99 | 0.93/0.93 |
| 58 | `cfg_994d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 59 | `cfg_bdb3` | 3 | 0.95 | 0.93/0.97 | 0.96/0.98 |
| 60 | `cfg_e87a` | 2 | 0.89 | 0.91/0.91 | 0.96/0.96 |
| 61 | `cfg_abbe` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 62 | `cfg_b500` | 2 | 0.99 | 0.98/0.98 | 0.95/0.95 |
| 63 | `cfg_b70d` | 2 | 0.99 | 0.99/0.99 | 0.98/0.98 |
| 64 | `cfg_f3be` | 3 | 0.92 | 0.91/0.92 | 0.80/0.82 |
| 65 | `cfg_c3ef` | 1 | n/a | n/a/n/a | n/a/n/a |
| 66 | `cfg_d23b` | 1 | n/a | n/a/n/a | n/a/n/a |
| 67 | `cfg_e6ea` | 4 | 0.89 | 0.90/0.94 | 0.87/0.90 |
| 68 | `cfg_f5fe` | 1 | n/a | n/a/n/a | n/a/n/a |
| 69 | `cfg_fd37` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 5.407e-04 over 4864 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 248.0, participation ratio 10.5, 95%-variance components 64 (rank bound T = 1292); raw grid 4864; raw + known prior 1652768
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
