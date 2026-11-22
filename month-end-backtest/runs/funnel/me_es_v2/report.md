# Screening funnel -- me_es_v2 (development stages only)

- Code: `d7cd024716c8` (dirty working tree: True, diff sha256 `d5d1bad97e31`)
- Config: `configs/funnel/me_funnel_es_v2.yaml` sha256 `556b7b5394695edd`; seed 20261123
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'NQ': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `c0267757901125e7` (38 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No month-end strategy has been scored on ES 2023-2024, but the mean-reversion, noise-band, BB/KC squeeze, NR-N, convexity and drift-burst families were selected there and the researcher has read those results. Treated as used for selection.
- Holdout 2025+ previously inspected: **False** -- No month-end metrics have been computed on ES 2025+. Other families (mean reversion, noise band, BB/KC squeeze, NR-N, convexity, EMRT ES-RTY) were scored there, so the researcher has seen how that period treated intraday ES strategies.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 4864 | 4864 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 4864 | 4864 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 4864 | 4352 | 512 | 0 |  | 0 | 89.47 | 89.47 |  |
| 3 performance & risk | hard_gate | 4352 | 70 | 4282 | 0 |  | 0 | 1.44 | 1.61 |  |
| 4 parameter stability | hard_gate | 70 | 65 | 5 | 0 |  | 0 | 1.34 | 92.86 |  |
| 5 time stability | hard_gate | 65 | 65 | 0 | 0 |  | 56 | 1.34 | 100.00 |  |
| 6 deduplication | dedup | 65 | 38 |  |  | 27 |  | 0.78 | 58.46 | best 2 per cluster |
| 7 execution stress | hard_gate | 38 | 38 | 0 | 0 |  | 0 | 0.78 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 38 |  |  |  |  |  |  |  | diagnostic only: unverified: 38 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 512 |
| s3:hard_reject:net_return | 2231 |
| s3:hard_reject:sharpe | 4282 |
| s4:hard_reject:local_median_sharpe | 5 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | NQ dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_1c8e` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 112/0/2 | 114 | 14.8% | 2.7% | 1.31 | -1.4% | 175 | 2.33 | 2.0% | 51.0 | 8/8 | 1.00 | 0.84 | 0.47 | 4 | 7.4% | 0.50 | 0.49 | 13.7% | 12.5% | 15.1% | 13.2%/11.5% | 8.3 (interpolated) | pass | 0.725 (unverified) | 1.40 |
| 2 | `cfg_7cfd` | timeframe=1min, window=4, first_days=3, entry=11:00, exit=15:30, event_filter=none, stop=0.50 | 319/4/97 | 420 | 28.0% | 4.9% | 0.94 | -4.6% | 341 | 1.33 | 14.5% | 190.8 | 8/8 | 1.00 | 0.72 | 0.22 | 3 | 14.5% | 0.44 | 0.53 | 24.2% | 20.4% | 26.6% | 25.7%/21.2% | 4.6 (interpolated) | pass | 0.366 (unverified) | 1.08 |
| 3 | `cfg_a380` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=0.50 | 261/3/96 | 360 | 26.1% | 4.6% | 0.86 | -5.5% | 383 | 1.34 | 13.6% | 161.2 | 8/8 | 1.00 | 0.72 | 0.14 | 3 | 5.5% | 0.79 | 0.61 | 21.6% | 17.0% | 22.7% | 21.0%/14.4% | 4.8 (interpolated) | pass | 0.297 (unverified) | 1.15 |
| 4 | `cfg_c45c` | timeframe=1min, window=4, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=0.50 | 304/4/112 | 420 | 32.0% | 5.6% | 0.92 | -5.9% | 412 | 1.32 | 15.9% | 189.9 | 7/7 | 1.00 | 0.77 | 0.15 | 4 | 18.4% | 0.43 | 0.59 | 27.1% | 23.2% | 28.3% | 29.2%/21.9% | 5.1 (interpolated) | pass | 0.345 (unverified) | 1.11 |
| 5 | `cfg_94b4` | timeframe=1min, window=4, first_days=3, entry=11:00, exit=15:00, event_filter=none, stop=0.50 | 328/4/88 | 420 | 23.2% | 4.2% | 0.89 | -5.4% | 320 | 1.29 | 13.1% | 191.2 | 8/8 | 1.00 | 0.59 | 0.29 | 4 | 13.5% | 0.39 | 0.52 | 19.3% | 15.2% | 22.6% | 20.7%/16.5% | 4.0 (interpolated) | pass | 0.323 (unverified) | 1.08 |
| 6 | `cfg_c3f4` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=none | 114/0/0 | 114 | 14.9% | 2.7% | 1.30 | -1.8% | 175 | 2.33 | 2.0% | 51.2 | 7/7 | 1.00 | 0.85 | 0.45 | 4 | 7.5% | 0.50 | 0.49 | 13.6% | 12.5% | 15.2% | 13.3%/10.7% | 8.2 (interpolated) | pass | 0.713 (unverified) | 1.37 |
| 7 | `cfg_fd44` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=15:00, event_filter=none, stop=0.50 | 282/3/75 | 360 | 23.1% | 4.1% | 0.96 | -3.9% | 277 | 1.36 | 11.2% | 162.5 | 9/9 | 1.00 | 0.71 | 0.25 | 5 | 9.7% | 0.58 | 0.47 | 18.1% | 14.5% | 21.3% | 19.5%/14.8% | 4.4 (interpolated) | pass | 0.385 (unverified) | 1.19 |
| 8 | `cfg_a3bb` | timeframe=1min, window=2, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 214/3/71 | 288 | 26.4% | 4.7% | 0.98 | -4.6% | 451 | 1.44 | 11.0% | 130.8 | 8/8 | 1.00 | 0.71 | 0.27 | 4 | 11.3% | 0.57 | 0.57 | 22.3% | 17.6% | 22.4% | 22.2%/16.6% | 5.6 (interpolated) | pass | 0.403 (unverified) | 1.11 |
| 9 | `cfg_573f` | timeframe=1min, window=4, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 292/4/104 | 400 | 29.8% | 5.2% | 0.90 | -5.2% | 365 | 1.32 | 15.1% | 181.0 | 7/7 | 1.00 | 0.79 | 0.11 | 4 | 16.4% | 0.43 | 0.60 | 26.6% | 22.7% | 27.6% | 26.6%/20.5% | 5.1 (interpolated) | pass | 0.330 (unverified) | 1.10 |
| 10 | `cfg_877c` | timeframe=1min, window=2, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=0.50 | 221/3/76 | 300 | 27.0% | 4.8% | 0.97 | -4.7% | 383 | 1.43 | 11.4% | 135.4 | 8/8 | 1.00 | 0.76 | 0.21 | 4 | 9.3% | 0.66 | 0.57 | 23.4% | 19.8% | 23.3% | 24.5%/18.6% | 5.9 (interpolated) | pass | 0.394 (unverified) | 1.15 |
| 11 | `cfg_716d` | timeframe=1min, window=2, first_days=3, entry=11:00, exit=15:00, event_filter=none, stop=0.50 | 238/3/59 | 300 | 20.1% | 3.6% | 0.95 | -3.5% | 323 | 1.40 | 9.4% | 135.2 | 9/9 | 1.00 | 0.69 | 0.26 | 5 | 9.1% | 0.55 | 0.51 | 16.4% | 13.4% | 17.8% | 18.1%/13.2% | 4.6 (interpolated) | pass | 0.375 (unverified) | 1.12 |
| 12 | `cfg_dec7` | timeframe=1min, window=2, first_days=3, entry=11:00, exit=15:30, event_filter=none, stop=0.50 | 231/3/66 | 300 | 17.8% | 3.2% | 0.78 | -3.9% | 383 | 1.33 | 10.4% | 134.5 | 9/9 | 1.00 | 0.58 | 0.20 | 5 | 4.3% | 0.76 | 0.66 | 14.6% | 12.4% | 15.8% | 16.2%/11.9% | 4.4 (interpolated) | pass | 0.237 (unverified) | 0.99 |
| 13 | `cfg_0865` | timeframe=1min, window=0, first_days=3, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=1.00 | 167/0/4 | 171 | 13.3% | 2.5% | 0.96 | -4.3% | 472 | 1.62 | 3.0% | 77.3 | 7/7 | 1.00 | 0.47 | 0.49 | 4 | 6.9% | 0.47 | 0.56 | 11.8% | 10.2% | 13.5% | 11.8%/8.8% | 5.3 (interpolated) | pass | 0.398 (unverified) | 1.11 |
| 14 | `cfg_899c` | timeframe=1min, window=0, first_days=3, entry=12:00, exit=16:00, event_filter=none, stop=0.25 | 106/1/73 | 180 | 15.7% | 2.9% | 0.96 | -2.7% | 540 | 1.60 | 4.8% | 80.6 | 6/6 | 1.00 | 0.61 | 0.35 | 4 | 6.6% | 0.58 | 0.68 | 14.3% | 12.0% | 15.4% | 14.4%/10.7% | 6.1 (interpolated) | pass | 0.371 (unverified) | 0.97 |
| 15 | `cfg_e4e4` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 172/2/167 | 341 | 19.3% | 3.5% | 0.82 | -4.9% | 518 | 1.33 | 10.0% | 153.0 | 7/7 | 1.00 | 0.71 | 0.11 | 4 | 7.3% | 0.62 | 0.67 | 16.1% | 13.2% | 13.1% | 17.7%/12.7% | 4.4 (interpolated) | pass | 0.256 (unverified) | 0.85 |
| 16 | `cfg_f66d` | timeframe=1min, window=3, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=0.25 | 179/2/179 | 360 | 19.1% | 3.5% | 0.79 | -4.7% | 473 | 1.31 | 10.5% | 161.0 | 7/7 | 1.00 | 0.73 | 0.06 | 4 | 6.5% | 0.66 | 0.68 | 16.0% | 12.5% | 12.1% | 16.8%/12.5% | 4.1 (interpolated) | pass | 0.236 (unverified) | 0.83 |
| 17 | `cfg_ced4` | timeframe=1min, window=0, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 90/1/82 | 173 | 16.7% | 3.1% | 0.92 | -3.7% | 582 | 1.59 | 5.1% | 77.8 | 6/6 | 1.00 | 0.76 | 0.17 | 5 | 10.0% | 0.40 | 0.73 | 15.0% | 12.5% | 8.4% | 15.6%/11.2% | 6.3 (interpolated) | pass | 0.329 (unverified) | 0.84 |
| 18 | `cfg_6c94` | timeframe=1min, window=4, first_days=3, entry=11:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 199/3/198 | 400 | 22.1% | 4.0% | 0.79 | -5.8% | 456 | 1.30 | 11.5% | 181.0 | 6/6 | 1.00 | 0.62 | 0.17 | 4 | 12.2% | 0.45 | 0.80 | 17.1% | 13.0% | 16.8% | 19.1%/14.1% | 3.9 (interpolated) | pass | 0.225 (unverified) | 0.90 |
| 19 | `cfg_9775` | timeframe=1min, window=0, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=0.25 | 91/1/88 | 180 | 15.1% | 2.8% | 0.83 | -3.7% | 582 | 1.50 | 5.3% | 80.7 | 6/6 | 1.00 | 0.67 | 0.16 | 5 | 9.4% | 0.38 | 0.80 | 12.8% | 10.9% | 7.4% | 12.9%/8.9% | 5.7 (interpolated) | pass | 0.248 (unverified) | 0.77 |
| 20 | `cfg_4467` | timeframe=1min, window=4, first_days=3, entry=11:00, exit=16:00, event_filter=none, stop=0.25 | 206/3/211 | 420 | 21.7% | 3.9% | 0.77 | -6.0% | 472 | 1.28 | 12.1% | 189.5 | 6/6 | 1.00 | 0.62 | 0.15 | 4 | 11.8% | 0.46 | 0.81 | 16.8% | 12.1% | 15.6% | 19.3%/12.7% | 3.7 (interpolated) | pass | 0.208 (unverified) | 0.87 |
| 21 | `cfg_c84e` | timeframe=1min, window=0, first_days=3, entry=12:00, exit=15:30, event_filter=none, stop=0.25 | 112/1/67 | 180 | 12.5% | 2.3% | 0.91 | -2.3% | 560 | 1.55 | 4.3% | 80.6 | 7/7 | 1.00 | 0.56 | 0.36 | 4 | 3.6% | 0.71 | 0.66 | 10.7% | 9.2% | 11.5% | 11.3%/8.7% | 5.0 (interpolated) | pass | 0.331 (unverified) | 0.74 |
| 22 | `cfg_f63b` | timeframe=1min, window=0, first_days=3, entry=12:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 103/1/69 | 173 | 13.6% | 2.5% | 0.94 | -3.2% | 584 | 1.55 | 4.6% | 77.3 | 6/6 | 1.00 | 0.66 | 0.28 | 4 | 7.5% | 0.45 | 0.66 | 11.5% | 9.9% | 12.5% | 11.9%/9.6% | 5.4 (interpolated) | pass | 0.355 (unverified) | 0.90 |
| 23 | `cfg_b985` | timeframe=1min, window=0, first_days=3, entry=14:00, exit=16:00, event_filter=none, stop=1.00 | 173/0/5 | 178 | 14.3% | 2.6% | 0.92 | -3.8% | 386 | 1.60 | 3.1% | 79.6 | 7/7 | 1.00 | 0.46 | 0.47 | 4 | 7.6% | 0.47 | 0.63 | 12.4% | 11.0% | 14.2% | 12.9%/10.0% | 5.4 (interpolated) | pass | 0.355 (unverified) | 0.88 |
| 24 | `cfg_4895` | timeframe=1min, window=2, first_days=3, entry=10:30, exit=16:00, event_filter=skip_fomc, stop=1.00 | 253/4/31 | 288 | 26.5% | 4.7% | 0.81 | -8.3% | 474 | 1.36 | 13.3% | 130.5 | 8/8 | 1.00 | 0.64 | 0.17 | 4 | 8.2% | 0.69 | 0.63 | 24.2% | 17.4% | 21.1% | 21.3%/14.3% | 6.0 (interpolated) | pass | 0.263 (unverified) | 0.88 |
| 25 | `cfg_6f1f` | timeframe=1min, window=2, first_days=0, entry=10:30, exit=12:00, event_filter=none, stop=1.00 | 119/0/1 | 120 | 9.5% | 1.8% | 0.83 | -2.9% | 387 | 1.67 | 1.6% | 53.8 | 8/8 | 1.00 | 0.55 | 0.28 | 3 | 1.7% | 0.82 | 0.71 | 8.5% | 7.2% | 7.3% | 8.5%/6.0% | 5.8 (interpolated) | pass | 0.287 (unverified) | 1.00 |
| 26 | `cfg_4890` | timeframe=1min, window=2, first_days=0, entry=11:00, exit=12:00, event_filter=skip_fomc, stop=1.00 | 115/0/0 | 115 | 5.9% | 1.1% | 0.91 | -2.2% | 365 | 1.68 | 1.0% | 51.6 | 7/8 | 1.00 | 0.66 | 0.25 | 4 | 1.5% | 0.75 | 0.57 | 4.7% | 3.7% | 5.1% | 5.3%/4.1% | 3.9 (interpolated) | pass | 0.347 (unverified) | 1.15 |
| 27 | `cfg_8819` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=15:30, event_filter=skip_fomc, stop=1.00 | 113/0/1 | 114 | 6.7% | 1.3% | 0.86 | -2.0% | 493 | 1.74 | 1.5% | 51.3 | 9/9 | 0.89 | 0.47 | 0.39 | 3 | 1.0% | 0.86 | 0.60 | 5.5% | 4.5% | 6.9% | 5.7%/4.4% | 4.3 (interpolated) | pass | 0.323 (unverified) | 1.01 |
| 28 | `cfg_8139` | timeframe=1min, window=2, first_days=0, entry=11:00, exit=15:00, event_filter=none, stop=0.50 | 99/2/19 | 120 | 9.9% | 1.9% | 0.76 | -2.4% | 303 | 1.55 | 3.9% | 53.8 | 9/9 | 0.78 | 0.55 | 0.21 | 4 | 5.6% | 0.44 | 0.85 | 8.3% | 7.2% | 8.7% | 8.6%/6.3% | 5.5 (interpolated) | pass | 0.206 (unverified) | 0.92 |
| 29 | `cfg_85bd` | timeframe=1min, window=2, first_days=0, entry=11:00, exit=12:00, event_filter=none, stop=1.00 | 120/0/0 | 120 | 6.2% | 1.2% | 0.96 | -2.1% | 365 | 1.70 | 1.1% | 53.8 | 7/8 | 1.00 | 0.64 | 0.32 | 4 | 1.9% | 0.70 | 0.54 | 5.0% | 3.9% | 5.5% | 5.6%/4.5% | 4.0 (interpolated) | pass | 0.389 (unverified) | 1.17 |
| 30 | `cfg_c2dc` | timeframe=1min, window=0, first_days=3, entry=12:00, exit=15:30, event_filter=skip_fomc, stop=0.25 | 108/1/64 | 173 | 10.3% | 1.9% | 0.83 | -2.8% | 582 | 1.47 | 4.1% | 77.8 | 7/7 | 1.00 | 0.50 | 0.33 | 3 | 3.8% | 0.63 | 0.69 | 8.6% | 7.1% | 9.3% | 9.5%/7.1% | 4.5 (interpolated) | pass | 0.277 (unverified) | 0.60 |
| 31 | `cfg_66a8` | timeframe=1min, window=2, first_days=3, entry=10:30, exit=16:00, event_filter=none, stop=0.50 | 207/3/90 | 300 | 22.9% | 4.1% | 0.76 | -6.6% | 430 | 1.33 | 11.8% | 134.4 | 8/8 | 1.00 | 0.58 | 0.18 | 3 | 3.6% | 0.84 | 0.77 | 17.4% | 14.3% | 20.1% | 20.7%/13.5% | 5.0 (interpolated) | pass | 0.225 (unverified) | 0.96 |
| 32 | `cfg_8e89` | timeframe=1min, window=0, first_days=3, entry=11:00, exit=15:00, event_filter=skip_fomc, stop=0.25 | 97/1/75 | 173 | 10.5% | 2.0% | 0.82 | -2.4% | 386 | 1.43 | 4.3% | 77.3 | 7/7 | 1.00 | 0.50 | 0.32 | 4 | 5.8% | 0.45 | 0.65 | 9.0% | 7.4% | 7.8% | 9.5%/7.2% | 4.7 (interpolated) | pass | 0.256 (unverified) | 0.54 |
| 33 | `cfg_7f79` | timeframe=1min, window=2, first_days=0, entry=10:30, exit=12:00, event_filter=skip_fomc, stop=1.00 | 114/0/1 | 115 | 9.2% | 1.7% | 0.81 | -2.9% | 387 | 1.66 | 1.5% | 51.5 | 8/8 | 1.00 | 0.54 | 0.27 | 3 | 1.3% | 0.85 | 0.73 | 7.8% | 6.9% | 6.7% | 8.4%/6.4% | 5.9 (interpolated) | pass | 0.269 (unverified) | 1.01 |
| 34 | `cfg_bafe` | timeframe=1min, window=0, first_days=3, entry=11:00, exit=15:30, event_filter=skip_fomc, stop=0.25 | 95/1/77 | 173 | 11.5% | 2.2% | 0.80 | -2.7% | 561 | 1.45 | 4.7% | 77.4 | 7/7 | 1.00 | 0.56 | 0.25 | 4 | 5.8% | 0.49 | 0.72 | 10.1% | 8.8% | 6.9% | 10.5%/7.5% | 5.1 (interpolated) | pass | 0.242 (unverified) | 0.60 |
| 35 | `cfg_049d` | timeframe=1min, window=0, first_days=2, entry=13:00, exit=16:00, event_filter=skip_fomc, stop=none | 114/1/0 | 115 | 11.4% | 2.1% | 0.85 | -2.3% | 150 | 1.71 | 3.0% | 51.5 | 7/7 | 1.00 | 0.55 | 0.30 | 4 | 4.0% | 0.65 | 0.65 | 10.4% | 9.3% | 11.9% | 10.3%/8.1% | 6.8 (interpolated) | pass | 0.306 (unverified) | 0.94 |
| 36 | `cfg_a9c0` | timeframe=1min, window=0, first_days=2, entry=13:00, exit=16:00, event_filter=skip_fomc, stop=0.25 | 75/1/39 | 115 | 8.1% | 1.5% | 0.83 | -2.0% | 260 | 1.59 | 2.4% | 51.7 | 7/7 | 1.00 | 0.55 | 0.29 | 3 | 2.2% | 0.73 | 0.74 | 7.1% | 6.2% | 7.4% | 7.5%/5.9% | 5.3 (interpolated) | pass | 0.276 (unverified) | 0.93 |
| 37 | `cfg_4cc0` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=15:00, event_filter=skip_fomc, stop=1.00 | 114/0/0 | 114 | 5.1% | 1.0% | 0.93 | -2.3% | 475 | 1.77 | 1.0% | 51.1 | 7/9 | 1.00 | 0.52 | 0.41 | 4 | 1.3% | 0.74 | 0.53 | 4.1% | 3.2% | 5.3% | 4.6%/3.5% | 3.6 (interpolated) | pass | 0.379 (unverified) | 1.25 |
| 38 | `cfg_bbc2` | timeframe=1min, window=0, first_days=2, entry=14:00, exit=16:00, event_filter=skip_fomc, stop=0.50 | 101/0/13 | 114 | 7.3% | 1.4% | 0.82 | -2.4% | 473 | 1.57 | 1.9% | 51.2 | 8/8 | 1.00 | 0.52 | 0.29 | 4 | 2.7% | 0.63 | 0.62 | 6.3% | 5.3% | 8.8% | 6.3%/5.0% | 4.8 (interpolated) | pass | 0.298 (unverified) | 1.08 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 2.1% / 1.19 / 21 | 1.5% / 1.23 / 23 | 4.3% / 1.39 / 23 | -0.6% / -0.42 / 24 | 6.9% / 2.69 / 23 |
| 2 | 6.0% / 1.02 / 84 | -1.2% / -0.37 / 84 | 11.8% / 1.94 / 84 | -0.3% / -0.06 / 84 | 9.7% / 1.27 / 84 |
| 3 | -1.2% / -0.23 / 72 | 2.7% / 0.81 / 72 | 6.8% / 1.08 / 72 | -2.6% / -0.80 / 72 | 19.5% / 2.22 / 72 |
| 4 | 7.8% / 1.10 / 84 | 1.4% / 0.40 / 84 | 11.5% / 1.55 / 84 | -2.9% / -0.75 / 84 | 11.6% / 1.38 / 84 |
| 5 | 6.6% / 1.22 / 84 | -1.1% / -0.31 / 84 | 8.6% / 1.78 / 84 | 1.9% / 0.58 / 84 | 5.6% / 0.85 / 84 |
| 6 | 2.1% / 1.19 / 21 | 1.5% / 1.23 / 23 | 4.9% / 1.67 / 23 | -1.2% / -0.59 / 24 | 6.9% / 2.69 / 23 |
| 7 | 1.1% / 0.27 / 72 | 0.0% / 0.03 / 72 | 5.4% / 1.20 / 72 | 2.9% / 0.95 / 72 | 12.2% / 1.83 / 72 |
| 8 | 1.7% / 0.44 / 57 | 3.1% / 1.06 / 56 | 8.8% / 1.39 / 58 | -2.5% / -0.81 / 59 | 13.6% / 1.89 / 58 |
| 9 | 9.3% / 1.32 / 80 | 1.3% / 0.41 / 80 | 11.6% / 1.57 / 80 | -2.7% / -0.75 / 80 | 8.0% / 1.07 / 80 |
| 10 | 0.6% / 0.16 / 60 | 3.0% / 0.93 / 60 | 7.6% / 1.28 / 60 | -1.9% / -0.63 / 60 | 16.2% / 2.04 / 60 |
| 11 | 2.5% / 0.68 / 60 | 0.6% / 0.23 / 60 | 3.1% / 0.82 / 60 | 2.6% / 1.00 / 60 | 10.1% / 1.65 / 60 |
| 12 | 0.3% / 0.09 / 60 | 0.3% / 0.14 / 60 | 3.3% / 0.75 / 60 | 0.3% / 0.13 / 60 | 12.9% / 1.90 / 60 |
| 13 | 3.3% / 1.21 / 33 | 1.7% / 1.31 / 34 | 5.9% / 1.63 / 35 | -2.7% / -1.37 / 35 | 4.7% / 1.57 / 34 |
| 14 | 5.3% / 1.68 / 36 | 1.0% / 0.50 / 36 | 0.9% / 0.30 / 36 | -0.6% / -0.33 / 36 | 8.5% / 1.77 / 36 |
| 15 | 1.3% / 0.34 / 68 | 1.2% / 0.42 / 68 | 5.8% / 1.04 / 68 | -1.1% / -0.42 / 68 | 11.3% / 1.83 / 69 |
| 16 | 0.1% / 0.04 / 72 | 1.7% / 0.59 / 72 | 5.8% / 1.03 / 72 | -1.1% / -0.42 / 72 | 11.8% / 1.87 / 72 |
| 17 | 3.2% / 1.09 / 34 | 1.4% / 0.61 / 35 | 4.0% / 0.83 / 35 | 1.0% / 0.48 / 35 | 6.1% / 1.51 / 34 |
| 18 | 7.0% / 1.10 / 80 | 0.1% / 0.06 / 80 | 7.4% / 1.19 / 80 | -2.5% / -0.87 / 80 | 8.8% / 1.36 / 80 |
| 19 | 2.6% / 0.86 / 36 | 1.3% / 0.54 / 36 | 3.7% / 0.77 / 36 | 1.5% / 0.67 / 36 | 5.3% / 1.30 / 36 |
| 20 | 5.8% / 0.91 / 84 | 0.9% / 0.28 / 84 | 7.4% / 1.18 / 84 | -2.5% / -0.84 / 84 | 8.8% / 1.34 / 84 |
| 21 | 3.7% / 1.42 / 36 | -0.8% / -0.48 / 36 | 0.4% / 0.17 / 36 | 0.3% / 0.22 / 36 | 8.6% / 2.05 / 36 |
| 22 | 5.7% / 1.81 / 34 | 1.3% / 0.68 / 35 | 1.7% / 0.53 / 35 | -1.3% / -0.75 / 35 | 5.7% / 1.65 / 34 |
| 23 | 2.7% / 0.98 / 35 | 0.9% / 0.64 / 35 | 6.1% / 1.66 / 36 | -2.1% / -1.02 / 36 | 6.2% / 1.52 / 36 |
| 24 | 1.2% / 0.24 / 57 | 0.8% / 0.24 / 56 | 11.1% / 1.38 / 58 | -4.5% / -1.15 / 59 | 16.9% / 2.06 / 58 |
| 25 | -0.7% / -0.44 / 24 | 0.5% / 0.49 / 24 | 3.5% / 1.24 / 24 | -1.5% / -0.64 / 24 | 7.7% / 2.68 / 24 |
| 26 | 0.5% / 0.44 / 23 | 0.2% / 0.30 / 21 | 2.2% / 1.51 / 23 | -1.4% / -1.23 / 24 | 4.3% / 2.63 / 24 |
| 27 | 0.7% / 0.55 / 21 | -0.3% / -0.22 / 23 | 1.8% / 1.02 / 23 | -1.3% / -1.02 / 24 | 5.7% / 3.04 / 23 |
| 28 | 2.4% / 0.99 / 24 | 1.3% / 0.78 / 24 | 2.9% / 1.16 / 24 | -1.1% / -0.77 / 24 | 4.1% / 1.04 / 24 |
| 29 | 0.3% / 0.31 / 24 | 0.6% / 0.67 / 24 | 2.4% / 1.60 / 24 | -1.4% / -1.23 / 24 | 4.3% / 2.63 / 24 |
| 30 | 3.8% / 1.46 / 34 | -0.5% / -0.29 / 35 | 0.6% / 0.24 / 35 | -0.1% / -0.08 / 35 | 6.3% / 1.84 / 34 |
| 31 | -0.2% / -0.03 / 60 | 0.9% / 0.27 / 60 | 5.3% / 0.76 / 60 | -2.3% / -0.76 / 60 | 18.7% / 2.19 / 60 |
| 32 | 2.0% / 0.82 / 34 | -0.0% / -0.01 / 35 | 0.8% / 0.39 / 35 | 2.8% / 1.32 / 35 | 4.5% / 1.29 / 34 |
| 33 | -0.4% / -0.23 / 23 | 0.0% / 0.06 / 21 | 3.2% / 1.15 / 23 | -1.5% / -0.64 / 24 | 7.8% / 2.69 / 24 |
| 34 | 2.3% / 0.84 / 34 | -0.0% / 0.01 / 35 | 1.5% / 0.52 / 35 | 2.0% / 0.93 / 35 | 5.4% / 1.44 / 34 |
| 35 | 0.3% / 0.16 / 22 | 1.0% / 0.44 / 23 | 3.2% / 1.41 / 23 | -0.6% / -0.24 / 24 | 7.1% / 2.03 / 23 |
| 36 | -0.0% / -0.02 / 22 | 2.2% / 1.49 / 23 | -0.4% / -0.24 / 23 | 0.5% / 0.34 / 24 | 5.8% / 1.94 / 23 |
| 37 | 0.5% / 0.63 / 21 | -0.9% / -0.96 / 23 | 1.1% / 0.75 / 23 | 0.7% / 1.07 / 24 | 3.7% / 2.80 / 23 |
| 38 | 2.2% / 1.32 / 21 | 0.4% / 0.30 / 23 | 0.3% / 0.15 / 23 | -0.3% / -0.23 / 24 | 4.4% / 2.03 / 23 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_049d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 1 | `cfg_0865` | 2 | 0.91 | 0.89/0.89 | 0.96/0.96 |
| 2 | `cfg_6f1f` | 4 | 0.99 | 0.99/0.99 | 0.95/0.96 |
| 3 | `cfg_4890` | 4 | 0.99 | 0.99/0.99 | 0.96/0.96 |
| 4 | `cfg_a380` | 7 | 0.80 | 0.81/0.86 | 0.78/0.84 |
| 5 | `cfg_1c8e` | 4 | 0.90 | 0.90/0.96 | 0.95/0.96 |
| 6 | `cfg_c45c` | 6 | 0.85 | 0.82/0.90 | 0.74/0.81 |
| 7 | `cfg_6c94` | 2 | 0.98 | 0.98/0.98 | 0.95/0.95 |
| 8 | `cfg_4895` | 2 | 0.86 | 0.84/0.84 | 0.82/0.82 |
| 9 | `cfg_4cc0` | 1 | n/a | n/a/n/a | n/a/n/a |
| 10 | `cfg_716d` | 3 | 0.90 | 0.95/0.95 | 0.90/0.93 |
| 11 | `cfg_e4e4` | 6 | 0.83 | 0.80/0.92 | 0.70/0.83 |
| 12 | `cfg_7cfd` | 4 | 0.92 | 0.91/0.95 | 0.86/0.90 |
| 13 | `cfg_8139` | 1 | n/a | n/a/n/a | n/a/n/a |
| 14 | `cfg_a3bb` | 4 | 0.89 | 0.88/0.89 | 0.77/0.80 |
| 15 | `cfg_8819` | 1 | n/a | n/a/n/a | n/a/n/a |
| 16 | `cfg_899c` | 3 | 0.87 | 0.89/0.92 | 0.79/0.84 |
| 17 | `cfg_8e89` | 2 | 0.95 | 0.96/0.96 | 0.91/0.91 |
| 18 | `cfg_ced4` | 3 | 0.93 | 0.92/0.96 | 0.79/0.88 |
| 19 | `cfg_a9c0` | 1 | n/a | n/a/n/a | n/a/n/a |
| 20 | `cfg_bbc2` | 1 | n/a | n/a/n/a | n/a/n/a |
| 21 | `cfg_f63b` | 3 | 0.89 | 0.88/0.91 | 0.79/0.84 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 5.825e-04 over 4864 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 230.0, participation ratio 10.4, 95%-variance components 60 (rank bound T = 1292); raw grid 4864; raw + known prior 1647904
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
NQ results are unchanged rules on the development period: supporting evidence, not an independent replication.

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
