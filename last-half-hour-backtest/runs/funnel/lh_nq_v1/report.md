# Screening funnel -- lh_nq_v1 (development stages only)

- Code: `85258bebd6f4` (dirty working tree: True, diff sha256 `e7dc91a3d623`)
- Config: `configs/funnel/lh_funnel_nq_v1.yaml` sha256 `329d3c57bb773af7`; seed 20261124
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'NQ': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `cc1cb451abd485ad` (56 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No last-half-hour strategy has been scored on NQ 2023-2024, but the noise-band, mean-reversion, squeeze, convexity and EMRT families were selected there and the researcher has read those results.
- Holdout 2025+ previously inspected: **True** -- No last-half-hour metrics have been computed on NQ 2025+. Noise-band NQ picks and the month-end #7 transfer check were scored there, so the researcher has seen how that period treated intraday NQ strategies.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 500 | 500 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 500 | 500 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 500 | 500 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 3 performance & risk | hard_gate | 500 | 116 | 384 | 0 |  | 0 | 23.20 | 23.20 |  |
| 4 parameter stability | hard_gate | 116 | 113 | 3 | 0 |  | 0 | 22.60 | 97.41 |  |
| 5 time stability | hard_gate | 113 | 110 | 3 | 0 |  | 112 | 22.00 | 97.35 |  |
| 6 deduplication | dedup | 110 | 56 |  |  | 54 |  | 11.20 | 50.91 | best 2 per cluster |
| 7 execution stress | hard_gate | 56 | 56 | 0 | 0 |  | 0 | 11.20 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 56 |  |  |  |  |  |  |  | diagnostic only: unverified: 56 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s3:hard_reject:net_return | 136 |
| s3:hard_reject:sharpe | 384 |
| s4:hard_reject:local_frac_profitable | 3 |
| s5:hard_reject:profitable_years | 3 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_588f` | timeframe=1min, signal=open, agree=off, window=15:50-16:00, filter=rv_high, stop=0.10 | 0/305/255 | 560 | 30.1% | 5.3% | 1.68 | -2.0% | 288 | 1.73 | 0.8% | 274.9 | 2/2 | 1.00 | 1.22 | 0.45 | 4 | 11.8% | 0.55 | 0.36 | 27.7% | 25.5% | 15.5% | 27.2%/24.1% | 8.1 (interpolated) | pass | 0.869 (unverified) | 0.80 |
| 2 | `cfg_651f` | timeframe=1min, signal=open, agree=off, window=15:50-16:00, filter=rv_high, stop=0.20 | 0/437/123 | 560 | 31.2% | 5.4% | 1.52 | -2.2% | 285 | 1.61 | 1.0% | 276.1 | 3/3 | 1.00 | 1.43 | 0.09 | 4 | 10.2% | 0.61 | 0.42 | 28.9% | 26.4% | 19.3% | 27.0%/23.5% | 8.6 (interpolated) | pass | 0.744 (unverified) | 0.68 |
| 3 | `cfg_11c8` | timeframe=1min, signal=open, agree=off, window=15:45-16:00, filter=rv_high, stop=0.40 | 0/515/45 | 560 | 25.8% | 4.6% | 1.15 | -4.6% | 313 | 1.42 | 1.6% | 277.2 | 4/4 | 1.00 | 1.08 | 0.07 | 4 | 15.2% | 0.41 | 0.45 | 22.9% | 20.9% | 31.2% | 22.7%/18.3% | 6.9 (interpolated) | pass | 0.360 (unverified) | 0.52 |
| 4 | `cfg_baae` | timeframe=1min, signal=prev_close, agree=off, window=15:30-16:00, filter=rv_high, stop=0.40 | 0/482/78 | 560 | 29.9% | 5.2% | 1.16 | -3.7% | 329 | 1.38 | 3.2% | 275.0 | 4/4 | 1.00 | 0.80 | 0.37 | 4 | 12.0% | 0.54 | 0.42 | 27.5% | 25.7% | 19.3% | 26.6%/20.8% | 8.0 (interpolated) | pass | 0.384 (unverified) | 0.58 |
| 5 | `cfg_143d` | timeframe=1min, signal=open, agree=off, window=15:50-16:00, filter=none, stop=0.10 | 0/765/483 | 1248 | 28.3% | 5.0% | 1.39 | -3.0% | 275 | 1.34 | 1.9% | 610.3 | 2/2 | 1.00 | 0.93 | 0.46 | 4 | 9.8% | 0.60 | 0.39 | 23.2% | 16.4% | 11.7% | 24.9%/20.8% | 3.7 (interpolated) | pass | 0.614 (unverified) | 0.20 |
| 6 | `cfg_5ec9` | timeframe=1min, signal=prev_close, agree=off, window=15:45-16:00, filter=rv_high, stop=0.40 | 0/513/47 | 560 | 26.7% | 4.7% | 1.15 | -4.0% | 320 | 1.43 | 1.6% | 276.2 | 4/4 | 1.00 | 0.92 | 0.23 | 3 | 8.1% | 0.63 | 0.48 | 24.8% | 22.0% | 28.6% | 24.2%/19.6% | 7.3 (interpolated) | pass | 0.374 (unverified) | 0.58 |
| 7 | `cfg_10b3` | timeframe=1min, signal=open, agree=on, window=15:00-16:00, filter=rv_high, stop=none | 0/337/0 | 337 | 32.1% | 5.6% | 1.11 | -5.4% | 305 | 1.55 | 4.1% | 165.8 | 2/2 | 1.00 | 0.46 | 0.65 | 3 | 16.1% | 0.50 | 0.46 | 31.0% | 28.9% | 34.7% | 28.6%/22.2% | 13.2 (interpolated) | pass | 0.338 (unverified) | -0.00 |
| 8 | `cfg_b495` | timeframe=1min, signal=prev_close, agree=off, window=15:00-16:00, filter=z1.0, stop=none | 0/408/0 | 408 | 43.3% | 7.3% | 1.24 | -8.1% | 533 | 1.61 | 4.9% | 200.4 | 2/2 | 1.00 | 0.77 | 0.48 | 3 | 22.2% | 0.49 | 0.46 | 41.0% | 37.5% | 45.8% | 37.9%/31.3% | 13.2 (interpolated) | pass | 0.471 (unverified) | 0.18 |
| 9 | `cfg_a6da` | timeframe=1min, signal=prev_close, agree=off, window=15:50-16:00, filter=none, stop=0.10 | 0/773/473 | 1246 | 28.1% | 5.0% | 1.41 | -3.1% | 274 | 1.34 | 1.9% | 608.6 | 2/2 | 1.00 | 0.75 | 0.65 | 4 | 6.9% | 0.72 | 0.40 | 22.7% | 17.4% | 6.9% | 24.4%/21.7% | 3.7 (interpolated) | pass | 0.628 (unverified) | -0.11 |
| 10 | `cfg_114c` | timeframe=1min, signal=prev_close, agree=off, window=15:00-16:00, filter=rv_high, stop=none | 0/560/0 | 560 | 49.0% | 8.1% | 1.15 | -5.5% | 350 | 1.41 | 6.8% | 279.4 | 2/2 | 1.00 | 0.73 | 0.42 | 4 | 24.2% | 0.51 | 0.42 | 47.4% | 44.9% | 50.6% | 43.1%/34.0% | 11.0 (interpolated) | pass | 0.385 (unverified) | 0.46 |
| 11 | `cfg_1998` | timeframe=1min, signal=open, agree=off, window=15:45-16:00, filter=z1.0, stop=0.40 | 0/352/26 | 378 | 19.4% | 3.5% | 1.05 | -4.9% | 305 | 1.48 | 1.1% | 184.4 | 4/4 | 1.00 | 0.96 | 0.08 | 5 | 7.5% | 0.60 | 0.54 | 18.2% | 16.2% | 21.0% | 17.2%/12.9% | 7.8 (interpolated) | pass | 0.255 (unverified) | 0.50 |
| 12 | `cfg_29c4` | timeframe=1min, signal=open, agree=off, window=15:45-16:00, filter=z0.5, stop=0.40 | 0/706/39 | 745 | 26.0% | 4.6% | 1.14 | -4.7% | 271 | 1.36 | 2.2% | 363.7 | 4/4 | 1.00 | 1.12 | 0.02 | 5 | 11.3% | 0.53 | 0.46 | 23.1% | 20.3% | 32.6% | 23.6%/20.5% | 5.4 (interpolated) | pass | 0.366 (unverified) | 0.28 |
| 13 | `cfg_c545` | timeframe=1min, signal=open, agree=off, window=15:50-16:00, filter=z0.5, stop=0.40 | 0/721/27 | 748 | 19.6% | 3.6% | 1.05 | -4.4% | 459 | 1.31 | 1.5% | 366.2 | 3/3 | 1.00 | 1.04 | 0.01 | 5 | 8.4% | 0.55 | 0.54 | 16.8% | 13.7% | 14.8% | 17.4%/14.5% | 4.4 (interpolated) | pass | 0.289 (unverified) | 0.33 |
| 14 | `cfg_29d9` | timeframe=1min, signal=prev_close, agree=off, window=15:45-16:00, filter=z0.5, stop=0.40 | 0/692/35 | 727 | 24.2% | 4.3% | 1.05 | -4.0% | 344 | 1.34 | 2.2% | 355.6 | 4/4 | 1.00 | 0.82 | 0.24 | 3 | 5.8% | 0.73 | 0.53 | 21.7% | 18.5% | 25.2% | 22.5%/17.3% | 5.3 (interpolated) | pass | 0.300 (unverified) | 0.17 |
| 15 | `cfg_21f8` | timeframe=1min, signal=prev_close, agree=off, window=15:00-16:00, filter=rv_high, stop=0.40 | 0/440/120 | 560 | 29.8% | 5.2% | 1.06 | -6.4% | 487 | 1.31 | 6.1% | 274.4 | 3/3 | 1.00 | 0.89 | 0.17 | 4 | 7.9% | 0.74 | 0.36 | 27.7% | 25.0% | 36.8% | 27.1%/21.2% | 7.8 (interpolated) | pass | 0.294 (unverified) | 0.37 |
| 16 | `cfg_87f1` | timeframe=1min, signal=open, agree=off, window=15:45-16:00, filter=rv_high, stop=0.20 | 0/406/154 | 560 | 21.3% | 3.8% | 1.06 | -4.5% | 317 | 1.37 | 1.5% | 276.5 | 4/4 | 1.00 | 1.03 | 0.02 | 4 | 12.0% | 0.39 | 0.51 | 19.1% | 16.0% | 22.3% | 19.2%/14.9% | 5.8 (interpolated) | pass | 0.263 (unverified) | 0.32 |
| 17 | `cfg_109e` | timeframe=1min, signal=open, agree=off, window=15:45-16:00, filter=z1.0, stop=0.20 | 0/290/88 | 378 | 17.2% | 3.2% | 1.02 | -3.3% | 171 | 1.49 | 1.0% | 184.7 | 4/4 | 1.00 | 0.94 | 0.09 | 5 | 9.0% | 0.46 | 0.57 | 15.7% | 14.1% | 16.9% | 16.1%/13.0% | 7.0 (interpolated) | pass | 0.217 (unverified) | 0.35 |
| 18 | `cfg_1906` | timeframe=1min, signal=open, agree=off, window=15:00-16:00, filter=rv_high, stop=0.40 | 0/438/122 | 560 | 31.6% | 5.5% | 1.11 | -12.3% | 789 | 1.34 | 6.1% | 275.8 | 3/3 | 1.00 | 0.85 | 0.26 | 3 | 7.2% | 0.77 | 0.31 | 29.7% | 27.6% | 36.1% | 28.2%/22.1% | 8.3 (interpolated) | pass | 0.344 (unverified) | 0.16 |
| 19 | `cfg_d1e3` | timeframe=1min, signal=prev_close, agree=off, window=15:30-16:00, filter=down_only, stop=0.40 | 0/478/62 | 540 | 24.8% | 4.4% | 1.03 | -5.0% | 327 | 1.36 | 3.1% | 265.9 | 4/4 | 1.00 | 0.57 | 0.46 | 4 | 12.4% | 0.46 | 0.52 | 22.7% | 19.2% | 15.8% | 21.6%/17.7% | 6.6 (interpolated) | pass | 0.264 (unverified) | 0.66 |
| 20 | `cfg_36e3` | timeframe=1min, signal=open, agree=off, window=15:30-16:00, filter=rv_high, stop=0.40 | 0/484/76 | 560 | 28.4% | 5.0% | 1.10 | -5.6% | 298 | 1.36 | 3.2% | 275.4 | 4/4 | 1.00 | 0.52 | 0.58 | 4 | 15.2% | 0.47 | 0.46 | 26.2% | 24.5% | 21.7% | 25.6%/19.2% | 7.6 (interpolated) | pass | 0.340 (unverified) | 0.53 |
| 21 | `cfg_55ca` | timeframe=1min, signal=prev_close, agree=off, window=15:30-16:00, filter=none, stop=0.40 | 0/1133/115 | 1248 | 30.4% | 5.3% | 1.00 | -6.6% | 496 | 1.21 | 7.3% | 607.9 | 4/4 | 0.75 | 0.67 | 0.32 | 4 | 12.8% | 0.53 | 0.44 | 23.2% | 18.0% | 21.7% | 26.1%/18.5% | 3.8 (interpolated) | pass | 0.260 (unverified) | 0.24 |
| 22 | `cfg_0660` | timeframe=1min, signal=open, agree=off, window=15:45-16:00, filter=none, stop=0.40 | 0/1191/56 | 1247 | 23.7% | 4.2% | 0.93 | -5.5% | 315 | 1.21 | 3.7% | 615.1 | 4/4 | 1.00 | 0.89 | 0.04 | 4 | 11.8% | 0.46 | 0.50 | 18.9% | 13.7% | 26.9% | 20.7%/15.6% | 3.3 (interpolated) | pass | 0.192 (unverified) | 0.12 |
| 23 | `cfg_3276` | timeframe=1min, signal=open, agree=off, window=15:00-16:00, filter=rv_high, stop=none | 0/560/0 | 560 | 40.0% | 6.8% | 0.98 | -10.3% | 565 | 1.35 | 6.8% | 275.5 | 2/2 | 1.00 | 0.58 | 0.40 | 4 | 14.4% | 0.64 | 0.37 | 37.7% | 36.0% | 44.0% | 34.5%/27.4% | 10.0 (interpolated) | pass | 0.259 (unverified) | 0.06 |
| 24 | `cfg_569b` | timeframe=1min, signal=prev_close, agree=off, window=15:45-16:00, filter=down_only, stop=0.40 | 0/504/41 | 545 | 20.5% | 3.7% | 1.01 | -5.2% | 355 | 1.37 | 1.6% | 267.8 | 4/4 | 1.00 | 0.80 | 0.21 | 4 | 7.3% | 0.60 | 0.49 | 18.2% | 15.9% | 19.2% | 18.4%/15.2% | 5.8 (interpolated) | pass | 0.239 (unverified) | 0.67 |
| 25 | `cfg_49e0` | timeframe=1min, signal=prev_close, agree=off, window=15:00-16:00, filter=z0.5, stop=none | 0/729/0 | 729 | 44.1% | 7.4% | 1.08 | -9.0% | 365 | 1.35 | 8.8% | 358.6 | 2/2 | 1.00 | 0.53 | 0.55 | 3 | 22.4% | 0.49 | 0.46 | 40.9% | 38.6% | 48.9% | 39.1%/28.4% | 7.9 (interpolated) | pass | 0.333 (unverified) | 0.25 |
| 26 | `cfg_f08a` | timeframe=1min, signal=open, agree=off, window=15:00-16:00, filter=none, stop=0.40 | 0/1073/176 | 1249 | 36.3% | 6.2% | 1.02 | -13.7% | 766 | 1.21 | 14.1% | 611.5 | 3/3 | 0.67 | 0.81 | 0.21 | 4 | 14.5% | 0.60 | 0.31 | 30.9% | 25.7% | 36.6% | 31.3%/25.5% | 4.4 (interpolated) | pass | 0.270 (unverified) | -0.19 |
| 27 | `cfg_2b1a` | timeframe=1min, signal=prev_close, agree=on, window=15:00-16:00, filter=z1.0, stop=none | 0/367/0 | 367 | 33.4% | 5.8% | 1.03 | -7.3% | 429 | 1.53 | 4.4% | 179.4 | 2/2 | 1.00 | 0.49 | 0.54 | 3 | 12.0% | 0.60 | 0.59 | 31.7% | 29.7% | 35.4% | 30.6%/24.0% | 12.2 (interpolated) | pass | 0.300 (unverified) | 0.01 |
| 28 | `cfg_e687` | timeframe=1min, signal=open, agree=off, window=15:45-16:00, filter=rv_high, stop=none | 0/560/0 | 560 | 21.3% | 3.8% | 0.80 | -7.0% | 451 | 1.33 | 1.7% | 274.1 | 3/3 | 1.00 | 1.15 | -0.35 | 4 | 8.9% | 0.58 | 0.56 | 19.1% | 15.6% | 24.2% | 18.3%/12.4% | 5.6 (interpolated) | pass | 0.144 (unverified) | 0.15 |
| 29 | `cfg_6a36` | timeframe=1min, signal=open, agree=off, window=15:45-16:00, filter=down_only, stop=0.40 | 0/535/33 | 568 | 17.9% | 3.3% | 0.94 | -4.5% | 321 | 1.34 | 1.7% | 279.0 | 4/4 | 1.00 | 0.72 | 0.22 | 4 | 10.3% | 0.40 | 0.53 | 15.2% | 13.4% | 19.6% | 16.6%/13.2% | 5.0 (interpolated) | pass | 0.175 (unverified) | 0.68 |
| 30 | `cfg_f492` | timeframe=1min, signal=open, agree=on, window=15:45-16:00, filter=down_only, stop=0.40 | 0/286/19 | 305 | 14.4% | 2.7% | 0.90 | -2.6% | 321 | 1.49 | 0.9% | 149.5 | 4/4 | 1.00 | 0.74 | 0.16 | 3 | 5.2% | 0.63 | 0.65 | 13.3% | 11.7% | 13.2% | 13.4%/10.1% | 6.9 (interpolated) | pass | 0.136 (unverified) | 0.29 |
| 31 | `cfg_0a74` | timeframe=1min, signal=prev_close, agree=off, window=15:00-16:00, filter=z1.0, stop=0.40 | 0/342/66 | 408 | 23.1% | 4.1% | 0.97 | -9.4% | 548 | 1.37 | 4.6% | 201.3 | 3/3 | 1.00 | 1.02 | -0.05 | 3 | 5.1% | 0.78 | 0.48 | 21.3% | 18.7% | 31.2% | 20.8%/14.7% | 8.2 (interpolated) | pass | 0.223 (unverified) | -0.11 |
| 32 | `cfg_89e5` | timeframe=1min, signal=prev_close, agree=off, window=15:00-16:00, filter=none, stop=none | 0/1245/0 | 1245 | 42.6% | 7.2% | 0.91 | -9.2% | 312 | 1.20 | 15.1% | 613.4 | 2/2 | 1.00 | 0.50 | 0.41 | 4 | 18.9% | 0.50 | 0.48 | 40.3% | 33.1% | 48.4% | 38.5%/27.9% | 5.2 (interpolated) | pass | 0.206 (unverified) | 0.24 |
| 33 | `cfg_19e9` | timeframe=1min, signal=open, agree=off, window=15:30-16:00, filter=none, stop=0.40 | 0/1133/115 | 1248 | 25.6% | 4.5% | 0.85 | -7.8% | 324 | 1.18 | 7.3% | 616.1 | 4/4 | 0.75 | 0.36 | 0.49 | 3 | 12.1% | 0.53 | 0.51 | 17.6% | 13.4% | 18.5% | 21.6%/15.9% | 3.4 (interpolated) | pass | 0.176 (unverified) | 0.13 |
| 34 | `cfg_fe2c` | timeframe=1min, signal=open, agree=off, window=15:00-16:00, filter=none, stop=none | 0/1248/0 | 1248 | 39.8% | 6.8% | 0.85 | -11.9% | 466 | 1.19 | 15.1% | 614.7 | 2/2 | 0.50 | 0.45 | 0.40 | 4 | 21.5% | 0.46 | 0.40 | 35.3% | 32.1% | 44.9% | 37.6%/28.9% | 4.9 (interpolated) | pass | 0.171 (unverified) | -0.02 |
| 35 | `cfg_462d` | timeframe=1min, signal=prev_close, agree=off, window=15:30-16:00, filter=rv_high, stop=none | 0/560/0 | 560 | 25.7% | 4.6% | 0.81 | -7.5% | 329 | 1.29 | 3.4% | 276.2 | 3/3 | 1.00 | 0.80 | 0.01 | 4 | 12.6% | 0.46 | 0.59 | 23.7% | 20.7% | 23.7% | 23.2%/18.1% | 7.4 (interpolated) | pass | 0.157 (unverified) | 0.46 |
| 36 | `cfg_f83a` | timeframe=1min, signal=open, agree=off, window=15:45-16:00, filter=none, stop=0.20 | 0/1009/238 | 1247 | 21.9% | 3.9% | 0.93 | -5.0% | 319 | 1.20 | 3.4% | 614.2 | 4/4 | 1.00 | 0.82 | 0.11 | 4 | 10.8% | 0.47 | 0.53 | 15.6% | 11.5% | 19.1% | 19.4%/15.2% | 3.1 (interpolated) | pass | 0.183 (unverified) | -0.13 |
| 37 | `cfg_18df` | timeframe=1min, signal=prev_close, agree=off, window=15:00-16:00, filter=none, stop=0.40 | 0/1068/178 | 1246 | 28.4% | 5.0% | 0.84 | -7.5% | 565 | 1.16 | 14.1% | 609.3 | 3/3 | 0.67 | 0.60 | 0.24 | 4 | 9.6% | 0.66 | 0.38 | 20.8% | 14.2% | 39.8% | 25.0%/15.2% | 3.6 (interpolated) | pass | 0.152 (unverified) | -0.19 |
| 38 | `cfg_29a0` | timeframe=1min, signal=open, agree=off, window=15:00-16:00, filter=z0.5, stop=none | 0/744/0 | 744 | 35.2% | 6.1% | 0.92 | -8.9% | 564 | 1.28 | 9.0% | 365.3 | 2/2 | 0.50 | 0.35 | 0.57 | 4 | 17.6% | 0.43 | 0.41 | 32.5% | 28.9% | 38.8% | 30.7%/22.6% | 6.4 (interpolated) | pass | 0.213 (unverified) | 0.36 |
| 39 | `cfg_7432` | timeframe=1min, signal=open, agree=off, window=15:30-16:00, filter=z0.5, stop=0.40 | 0/668/82 | 750 | 20.7% | 3.7% | 0.81 | -5.7% | 323 | 1.22 | 4.3% | 369.3 | 4/4 | 0.75 | 0.51 | 0.30 | 3 | 10.1% | 0.50 | 0.65 | 17.7% | 14.9% | 13.4% | 18.6%/15.4% | 4.7 (interpolated) | pass | 0.148 (unverified) | 0.42 |
| 40 | `cfg_5ce0` | timeframe=1min, signal=open, agree=off, window=15:50-16:00, filter=down_only, stop=0.10 | 0/340/244 | 584 | 12.4% | 2.3% | 0.93 | -3.8% | 330 | 1.32 | 0.9% | 284.4 | 2/2 | 1.00 | 0.75 | 0.18 | 4 | 5.9% | 0.50 | 0.61 | 9.8% | 7.7% | 4.8% | 11.6%/8.9% | 3.7 (interpolated) | pass | 0.164 (unverified) | 0.10 |
| 41 | `cfg_8267` | timeframe=1min, signal=prev_close, agree=off, window=15:00-16:00, filter=rv_high, stop=0.20 | 0/293/267 | 560 | 20.7% | 3.7% | 0.89 | -4.5% | 456 | 1.26 | 4.9% | 273.0 | 3/3 | 1.00 | 0.27 | 0.62 | 4 | 6.9% | 0.67 | 0.49 | 19.5% | 16.8% | 24.7% | 19.0%/14.1% | 6.0 (interpolated) | pass | 0.167 (unverified) | 0.32 |
| 42 | `cfg_635b` | timeframe=1min, signal=open, agree=off, window=15:30-16:00, filter=down_only, stop=0.40 | 0/507/61 | 568 | 17.2% | 3.2% | 0.78 | -6.5% | 756 | 1.25 | 3.3% | 279.0 | 4/4 | 1.00 | 0.39 | 0.38 | 4 | 8.8% | 0.45 | 0.68 | 14.0% | 12.4% | 10.9% | 15.4%/12.2% | 4.8 (interpolated) | pass | 0.106 (unverified) | 0.40 |
| 43 | `cfg_f49c` | timeframe=1min, signal=open, agree=off, window=15:00-16:00, filter=z1.0, stop=0.20 | 0/225/145 | 370 | 18.4% | 3.3% | 1.03 | -8.7% | 840 | 1.39 | 3.5% | 181.6 | 3/3 | 0.67 | 0.54 | 0.49 | 3 | 3.7% | 0.77 | 0.49 | 16.5% | 15.2% | 11.3% | 16.3%/12.5% | 6.9 (interpolated) | pass | 0.265 (unverified) | 0.27 |
| 44 | `cfg_8321` | timeframe=1min, signal=prev_close, agree=off, window=15:00-16:00, filter=z1.0, stop=0.20 | 0/256/152 | 408 | 20.9% | 3.8% | 1.02 | -6.8% | 515 | 1.40 | 3.9% | 200.5 | 3/3 | 0.67 | 0.23 | 0.78 | 3 | 6.8% | 0.68 | 0.52 | 19.5% | 16.7% | 16.1% | 18.3%/14.5% | 7.5 (interpolated) | pass | 0.247 (unverified) | -0.30 |
| 45 | `cfg_f5b8` | timeframe=1min, signal=prev_close, agree=off, window=15:50-16:00, filter=down_only, stop=0.10 | 0/321/238 | 559 | 13.1% | 2.4% | 0.93 | -3.7% | 326 | 1.35 | 0.8% | 273.1 | 2/2 | 1.00 | 0.68 | 0.25 | 4 | 4.3% | 0.65 | 0.64 | 10.8% | 8.3% | 5.2% | 12.0%/8.8% | 4.0 (interpolated) | pass | 0.151 (unverified) | -0.03 |
| 46 | `cfg_3807` | timeframe=1min, signal=open, agree=on, window=15:50-16:00, filter=down_only, stop=0.10 | 0/168/137 | 305 | 8.9% | 1.7% | 0.76 | -2.5% | 350 | 1.43 | 0.4% | 148.0 | 2/2 | 1.00 | 0.67 | 0.09 | 3 | 2.1% | 0.76 | 0.85 | 7.3% | 6.1% | 4.6% | 8.2%/6.4% | 4.7 (interpolated) | pass | 0.051 (unverified) | -0.13 |
| 47 | `cfg_02aa` | timeframe=1min, signal=open, agree=off, window=15:00-16:00, filter=z0.5, stop=0.20 | 0/459/285 | 744 | 17.9% | 3.3% | 0.78 | -11.1% | 790 | 1.20 | 7.1% | 364.2 | 3/3 | 0.67 | 0.26 | 0.52 | 3 | 7.3% | 0.59 | 0.53 | 15.0% | 11.7% | 12.2% | 15.8%/12.0% | 4.1 (interpolated) | pass | 0.115 (unverified) | -0.00 |
| 48 | `cfg_585c` | timeframe=1min, signal=open, agree=on, window=15:00-16:00, filter=rv_high, stop=0.40 | 0/266/71 | 337 | 17.2% | 3.1% | 0.84 | -4.0% | 303 | 1.32 | 3.7% | 162.0 | 3/3 | 0.67 | 0.68 | 0.16 | 3 | 7.2% | 0.58 | 0.61 | 15.8% | 14.3% | 21.9% | 15.1%/11.2% | 7.9 (interpolated) | pass | 0.139 (unverified) | -0.43 |
| 49 | `cfg_2366` | timeframe=1min, signal=prev_close, agree=off, window=15:00-16:00, filter=z0.5, stop=0.20 | 0/454/276 | 730 | 20.2% | 3.7% | 0.85 | -6.4% | 517 | 1.23 | 6.9% | 355.8 | 3/3 | 0.67 | 0.15 | 0.70 | 3 | 4.1% | 0.80 | 0.54 | 15.6% | 12.4% | 16.2% | 17.3%/12.0% | 4.5 (interpolated) | pass | 0.143 (unverified) | -0.08 |
| 50 | `cfg_dcb8` | timeframe=1min, signal=open, agree=on, window=15:45-16:00, filter=down_only, stop=0.20 | 0/236/69 | 305 | 13.2% | 2.5% | 0.88 | -3.2% | 321 | 1.50 | 0.8% | 149.4 | 4/4 | 1.00 | 0.67 | 0.21 | 4 | 5.5% | 0.57 | 0.68 | 11.3% | 10.2% | 8.5% | 11.5%/9.5% | 6.4 (interpolated) | pass | 0.103 (unverified) | -0.11 |
| 51 | `cfg_067e` | timeframe=1min, signal=open, agree=off, window=15:00-16:00, filter=z1.0, stop=none | 0/370/0 | 370 | 25.4% | 4.5% | 0.92 | -7.2% | 504 | 1.39 | 4.5% | 182.0 | 2/2 | 1.00 | 0.52 | 0.40 | 3 | 5.0% | 0.76 | 0.39 | 23.6% | 22.5% | 28.2% | 22.3%/18.1% | 9.7 (interpolated) | pass | 0.239 (unverified) | 0.40 |
| 52 | `cfg_7351` | timeframe=1min, signal=open, agree=off, window=15:00-16:00, filter=rv_high, stop=0.20 | 0/295/265 | 560 | 19.6% | 3.6% | 0.85 | -9.2% | 766 | 1.25 | 4.8% | 274.3 | 3/3 | 0.67 | 0.26 | 0.59 | 4 | 6.3% | 0.68 | 0.50 | 17.3% | 15.1% | 20.0% | 17.5%/13.5% | 5.5 (interpolated) | pass | 0.144 (unverified) | 0.02 |
| 53 | `cfg_9ab6` | timeframe=1min, signal=open, agree=on, window=15:00-16:00, filter=down_only, stop=none | 0/310/0 | 310 | 20.6% | 3.7% | 0.81 | -6.9% | 313 | 1.39 | 3.8% | 153.5 | 2/2 | 1.00 | 0.41 | 0.40 | 4 | 6.7% | 0.65 | 0.65 | 19.0% | 15.7% | 24.1% | 18.5%/14.5% | 9.7 (interpolated) | pass | 0.123 (unverified) | 0.18 |
| 54 | `cfg_3ead` | timeframe=1min, signal=open, agree=off, window=15:00-16:00, filter=none, stop=0.20 | 0/798/451 | 1249 | 23.7% | 4.2% | 0.81 | -11.8% | 756 | 1.16 | 12.1% | 610.9 | 3/3 | 0.67 | 0.20 | 0.61 | 4 | 10.3% | 0.57 | 0.44 | 16.8% | 10.7% | 20.4% | 20.5%/14.3% | 3.1 (interpolated) | pass | 0.131 (unverified) | -0.37 |
| 55 | `cfg_455e` | timeframe=1min, signal=prev_close, agree=on, window=15:00-16:00, filter=z1.0, stop=0.40 | 0/307/60 | 367 | 16.0% | 2.9% | 0.75 | -7.9% | 624 | 1.28 | 4.1% | 180.1 | 3/3 | 0.67 | 0.75 | 0.00 | 3 | 4.4% | 0.69 | 0.68 | 14.5% | 13.7% | 23.0% | 15.4%/12.2% | 6.9 (interpolated) | pass | 0.097 (unverified) | -0.28 |
| 56 | `cfg_7ae0` | timeframe=1min, signal=prev_close, agree=off, window=15:00-16:00, filter=down_only, stop=none | 0/540/0 | 540 | 26.6% | 4.7% | 0.81 | -7.4% | 313 | 1.27 | 6.5% | 266.6 | 2/2 | 1.00 | 0.54 | 0.27 | 4 | 14.2% | 0.43 | 0.52 | 23.4% | 21.7% | 31.3% | 23.8%/16.5% | 7.1 (interpolated) | pass | 0.137 (unverified) | 0.34 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 1.6% / 1.01 / 53 | -0.7% / -0.66 / 80 | 16.3% / 2.61 / 151 | 2.8% / 1.60 / 101 | 7.9% / 2.60 / 175 |
| 2 | 1.1% / 0.63 / 53 | -0.7% / -0.59 / 80 | 19.1% / 2.62 / 151 | 3.4% / 1.77 / 101 | 6.2% / 1.85 / 175 |
| 3 | 0.5% / 0.21 / 53 | -1.8% / -1.28 / 80 | 10.6% / 1.44 / 151 | 5.5% / 2.40 / 101 | 9.2% / 2.07 / 175 |
| 4 | 2.4% / 0.77 / 53 | -0.8% / -0.48 / 80 | 16.0% / 1.93 / 151 | 1.3% / 0.58 / 101 | 8.8% / 1.70 / 175 |
| 5 | 1.8% / 0.64 / 248 | -1.2% / -0.65 / 249 | 16.8% / 2.59 / 251 | 2.1% / 0.93 / 251 | 6.9% / 1.98 / 249 |
| 6 | -1.2% / -0.47 / 53 | -0.8% / -0.54 / 80 | 17.2% / 2.10 / 151 | 2.7% / 1.21 / 101 | 7.3% / 1.79 / 175 |
| 7 | 4.1% / 0.96 / 25 | -1.6% / -0.93 / 49 | 15.2% / 1.73 / 95 | -1.6% / -0.59 / 58 | 13.8% / 2.25 / 110 |
| 8 | 13.0% / 2.09 / 84 | -4.8% / -2.15 / 72 | 18.7% / 1.81 / 82 | -4.2% / -1.50 / 85 | 17.2% / 2.90 / 85 |
| 9 | 2.5% / 0.89 / 245 | -0.9% / -0.46 / 249 | 19.8% / 3.02 / 251 | 1.1% / 0.52 / 251 | 4.1% / 1.26 / 250 |
| 10 | 5.1% / 1.05 / 53 | -0.2% / -0.09 / 80 | 18.0% / 1.43 / 151 | 0.4% / 0.12 / 101 | 20.0% / 2.27 / 175 |
| 11 | 2.8% / 0.94 / 67 | 2.2% / 1.63 / 62 | 11.1% / 1.79 / 79 | 1.2% / 0.57 / 86 | 1.2% / 0.41 / 84 |
| 12 | 3.2% / 0.97 / 119 | 0.2% / 0.11 / 142 | 13.2% / 1.83 / 155 | 1.6% / 0.62 / 163 | 5.9% / 1.49 / 166 |
| 13 | 4.3% / 1.57 / 121 | 0.1% / 0.05 / 139 | 10.3% / 1.72 / 155 | 0.9% / 0.39 / 168 | 2.9% / 0.93 / 165 |
| 14 | 1.8% / 0.52 / 134 | -0.0% / -0.02 / 136 | 17.3% / 2.21 / 151 | -1.0% / -0.39 / 148 | 5.1% / 1.41 / 158 |
| 15 | 6.1% / 1.45 / 53 | -1.1% / -0.47 / 80 | 1.4% / 0.23 / 151 | 1.4% / 0.38 / 101 | 20.3% / 2.93 / 175 |
| 16 | 0.9% / 0.41 / 53 | -1.6% / -1.18 / 80 | 8.3% / 1.27 / 151 | 5.4% / 2.32 / 101 | 7.0% / 1.73 / 175 |
| 17 | 2.8% / 1.03 / 67 | 2.3% / 1.82 / 62 | 7.5% / 1.35 / 79 | 1.9% / 0.94 / 86 | 1.8% / 0.69 / 84 |
| 18 | 8.1% / 1.90 / 53 | -5.4% / -2.33 / 80 | -0.4% / -0.02 / 151 | 5.2% / 1.36 / 101 | 22.7% / 3.17 / 175 |
| 19 | 6.2% / 1.44 / 105 | -2.1% / -0.98 / 101 | 11.0% / 1.54 / 97 | 2.7% / 1.13 / 102 | 5.3% / 1.19 / 135 |
| 20 | 6.1% / 1.80 / 53 | -3.8% / -2.24 / 80 | 10.5% / 1.33 / 151 | 2.2% / 0.91 / 101 | 11.5% / 2.08 / 175 |
| 21 | 6.3% / 1.18 / 247 | -2.8% / -0.94 / 249 | 15.6% / 1.79 / 251 | 0.9% / 0.28 / 251 | 8.2% / 1.41 / 250 |
| 22 | 3.9% / 0.98 / 247 | -2.0% / -0.86 / 249 | 10.7% / 1.40 / 251 | 2.6% / 0.82 / 251 | 7.0% / 1.41 / 249 |
| 23 | 6.5% / 1.30 / 53 | -4.6% / -2.08 / 80 | 8.0% / 0.70 / 151 | 4.3% / 1.14 / 101 | 22.4% / 2.50 / 175 |
| 24 | 2.7% / 0.83 / 107 | -1.5% / -0.84 / 101 | 12.2% / 1.92 / 92 | 3.4% / 1.49 / 107 | 2.5% / 0.70 / 138 |
| 25 | 11.2% / 1.65 / 133 | -4.9% / -1.73 / 139 | 20.1% / 1.75 / 147 | -3.6% / -1.06 / 146 | 17.7% / 2.09 / 164 |
| 26 | 12.8% / 1.85 / 248 | -7.4% / -2.11 / 249 | 2.0% / 0.29 / 251 | 7.4% / 1.51 / 251 | 19.0% / 2.43 / 250 |
| 27 | 10.2% / 1.74 / 74 | -4.3% / -2.02 / 65 | 19.1% / 1.83 / 78 | -3.8% / -1.37 / 76 | 10.4% / 2.07 / 74 |
| 28 | 0.5% / 0.19 / 53 | -1.8% / -1.28 / 80 | 4.7% / 0.52 / 151 | 5.5% / 2.30 / 101 | 11.4% / 2.73 / 175 |
| 29 | 4.3% / 1.27 / 119 | -1.5% / -0.81 / 113 | 6.9% / 1.17 / 107 | 3.5% / 1.52 / 107 | 3.6% / 1.12 / 122 |
| 30 | 5.1% / 1.79 / 66 | -1.1% / -0.89 / 58 | 8.8% / 1.66 / 49 | -0.0% / -0.01 / 53 | 1.2% / 0.44 / 79 |
| 31 | 13.5% / 2.34 / 84 | -5.2% / -2.34 / 72 | 1.5% / 0.30 / 82 | -3.7% / -1.42 / 85 | 17.1% / 3.31 / 85 |
| 32 | 11.5% / 1.55 / 247 | -5.3% / -1.50 / 247 | 20.0% / 1.50 / 251 | 0.1% / 0.03 / 251 | 12.5% / 1.30 / 249 |
| 33 | 9.8% / 1.78 / 248 | -5.5% / -1.90 / 249 | 8.4% / 1.03 / 251 | -0.4% / -0.08 / 251 | 12.0% / 1.92 / 249 |
| 34 | 12.3% / 1.65 / 248 | -6.6% / -1.89 / 249 | 10.1% / 0.82 / 251 | 5.1% / 1.02 / 251 | 15.1% / 1.53 / 249 |
| 35 | 2.3% / 0.71 / 53 | -0.6% / -0.35 / 80 | 11.7% / 1.05 / 151 | 1.3% / 0.55 / 101 | 9.3% / 1.62 / 175 |
| 36 | 3.3% / 0.92 / 247 | -1.3% / -0.58 / 249 | 10.0% / 1.42 / 251 | 3.2% / 1.09 / 251 | 5.2% / 1.15 / 249 |
| 37 | 9.9% / 1.47 / 247 | -6.2% / -1.75 / 247 | 3.7% / 0.51 / 251 | 2.5% / 0.53 / 251 | 17.2% / 2.26 / 250 |
| 38 | 15.0% / 2.27 / 139 | -6.2% / -2.13 / 138 | 5.6% / 0.56 / 153 | 6.1% / 1.47 / 153 | 11.9% / 1.58 / 161 |
| 39 | 9.5% / 2.03 / 129 | -2.6% / -1.10 / 140 | 9.7% / 1.26 / 151 | -1.6% / -0.56 / 156 | 4.9% / 1.02 / 174 |
| 40 | 3.1% / 1.27 / 121 | -1.8% / -1.43 / 118 | 6.1% / 1.45 / 110 | 2.5% / 1.43 / 106 | 2.1% / 0.96 / 129 |
| 41 | 4.8% / 1.24 / 53 | -1.9% / -0.89 / 80 | 0.8% / 0.16 / 151 | 3.2% / 0.90 / 101 | 13.0% / 2.20 / 175 |
| 42 | 7.7% / 1.72 / 117 | -3.4% / -1.53 / 115 | 3.7% / 0.60 / 107 | 2.3% / 0.91 / 106 | 6.1% / 1.50 / 123 |
| 43 | 14.1% / 2.86 / 68 | -1.6% / -0.87 / 65 | -6.2% / -2.67 / 74 | 2.8% / 0.98 / 86 | 9.2% / 2.26 / 77 |
| 44 | 12.0% / 2.43 / 84 | -4.3% / -2.30 / 72 | 1.6% / 0.36 / 82 | -1.9% / -0.86 / 85 | 13.3% / 2.86 / 85 |
| 45 | 2.6% / 1.13 / 112 | -1.9% / -1.55 / 104 | 8.4% / 1.78 / 98 | 1.7% / 1.03 / 106 | 1.9% / 0.80 / 139 |
| 46 | 2.5% / 1.22 / 64 | -1.3% / -1.42 / 59 | 6.7% / 1.61 / 49 | -0.2% / -0.15 / 50 | 1.1% / 0.65 / 83 |
| 47 | 9.8% / 1.84 / 139 | -6.3% / -2.46 / 138 | -3.5% / -0.78 / 153 | 8.1% / 2.11 / 153 | 9.8% / 1.89 / 161 |
| 48 | 6.2% / 1.80 / 25 | -2.0% / -1.11 / 49 | 3.9% / 0.70 / 95 | -0.9% / -0.32 / 58 | 9.3% / 1.95 / 110 |
| 49 | 8.5% / 1.61 / 133 | -5.1% / -2.05 / 139 | 1.8% / 0.37 / 147 | -0.7% / -0.24 / 146 | 15.5% / 2.71 / 165 |
| 50 | 4.4% / 1.64 / 66 | -0.9% / -0.79 / 58 | 7.3% / 1.44 / 49 | 0.2% / 0.18 / 53 | 1.7% / 0.71 / 79 |
| 51 | 19.4% / 3.52 / 68 | -1.9% / -0.90 / 65 | -0.4% / -0.01 / 74 | 0.8% / 0.27 / 86 | 6.7% / 1.29 / 77 |
| 52 | 5.1% / 1.31 / 53 | -5.2% / -2.65 / 80 | 1.3% / 0.26 / 151 | 5.3% / 1.50 / 101 | 12.5% / 2.14 / 175 |
| 53 | 7.3% / 1.49 / 64 | -4.1% / -1.84 / 60 | 13.1% / 1.79 / 49 | 1.7% / 0.66 / 54 | 1.9% / 0.37 / 83 |
| 54 | 6.7% / 1.15 / 248 | -7.7% / -2.38 / 249 | 2.7% / 0.43 / 251 | 9.0% / 2.00 / 251 | 12.2% / 1.87 / 250 |
| 55 | 11.0% / 2.08 / 74 | -4.4% / -2.06 / 65 | 2.9% / 0.55 / 78 | -3.0% / -1.18 / 76 | 9.5% / 2.31 / 74 |
| 56 | 10.1% / 1.74 / 105 | -4.4% / -1.62 / 101 | 10.9% / 1.21 / 99 | 4.2% / 1.15 / 102 | 4.1% / 0.60 / 133 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_02aa` | 2 | 0.88 | 0.80/0.80 | 0.58/0.58 |
| 1 | `cfg_143d` | 11 | 0.83 | 0.58/0.73 | 0.23/0.46 |
| 2 | `cfg_0660` | 2 | 0.96 | 0.92/0.92 | 0.92/0.92 |
| 3 | `cfg_f49c` | 2 | 0.85 | 0.62/0.62 | 0.77/0.77 |
| 4 | `cfg_588f` | 16 | 0.86 | 0.64/0.77 | 0.26/0.58 |
| 5 | `cfg_0a74` | 2 | 0.94 | 0.94/0.94 | 0.90/0.90 |
| 6 | `cfg_1998` | 4 | 0.92 | 0.82/0.90 | 0.70/0.90 |
| 7 | `cfg_10b3` | 4 | 0.88 | 0.69/0.71 | 0.21/0.60 |
| 8 | `cfg_11c8` | 3 | 0.92 | 0.83/0.87 | 0.65/0.77 |
| 9 | `cfg_18df` | 1 | n/a | n/a/n/a | n/a/n/a |
| 10 | `cfg_5ec9` | 10 | 0.83 | 0.67/0.80 | 0.24/0.40 |
| 11 | `cfg_1906` | 2 | 0.82 | 0.68/0.68 | 0.89/0.89 |
| 12 | `cfg_19e9` | 2 | 0.90 | 0.87/0.87 | 0.59/0.59 |
| 13 | `cfg_21f8` | 1 | n/a | n/a/n/a | n/a/n/a |
| 14 | `cfg_8321` | 2 | 0.90 | 0.86/0.86 | 0.56/0.56 |
| 15 | `cfg_b495` | 4 | 0.88 | 0.56/0.70 | 0.12/0.18 |
| 16 | `cfg_569b` | 6 | 0.84 | 0.75/0.82 | 0.47/0.64 |
| 17 | `cfg_29a0` | 1 | n/a | n/a/n/a | n/a/n/a |
| 18 | `cfg_29c4` | 7 | 0.87 | 0.77/0.84 | 0.55/0.65 |
| 19 | `cfg_36e3` | 1 | n/a | n/a/n/a | n/a/n/a |
| 20 | `cfg_f5b8` | 3 | 0.93 | 0.84/0.88 | 0.51/0.61 |
| 21 | `cfg_baae` | 3 | 0.84 | 0.71/0.75 | 0.84/0.89 |
| 22 | `cfg_49e0` | 4 | 0.85 | 0.68/0.77 | 0.55/0.59 |
| 23 | `cfg_f492` | 4 | 0.91 | 0.86/0.87 | 0.71/0.91 |
| 24 | `cfg_d1e3` | 3 | 0.86 | 0.67/0.73 | 0.41/0.42 |
| 25 | `cfg_585c` | 1 | n/a | n/a/n/a | n/a/n/a |
| 26 | `cfg_5ce0` | 1 | n/a | n/a/n/a | n/a/n/a |
| 27 | `cfg_635b` | 1 | n/a | n/a/n/a | n/a/n/a |
| 28 | `cfg_7351` | 1 | n/a | n/a/n/a | n/a/n/a |
| 29 | `cfg_9ab6` | 2 | 0.89 | 0.78/0.78 | 0.54/0.54 |
| 30 | `cfg_8267` | 1 | n/a | n/a/n/a | n/a/n/a |
| 31 | `cfg_e687` | 1 | n/a | n/a/n/a | n/a/n/a |
| 32 | `cfg_f08a` | 2 | 0.85 | 0.74/0.74 | 0.93/0.93 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.037e-03 over 500 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 92.0, participation ratio 6.7, 95%-variance components 52 (rank bound T = 1290); raw grid 500; raw + known prior 313128
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

- Bars: 1-minute bars with NY open time in [09:30, 16:00) on their own session date only (lh_day_bars); each NY date is one session and no position can be held overnight.
- Signal per session: prev_close = close of the last bar opening before the entry time / the previous session's last close - 1; open = the same over today's first bar's open (bar opening by 09:35); first_half = close of the last bar opening before 10:00 / previous close - 1. The decision bar must open within 3 minutes of the entry time; the entry is the bar right after it.
- Filters: z = |signal| above z x the std (ddof 1) of the same signal over the previous 20 sessions (>= 15 defined); rv_high = std of the previous 20 daily close-to-close returns above its median over the previous 120 sessions (>= 60 defined); down_only = signal < 0. Agreement: the first-half-hour return has the signal's sign. All recomputed with plain loops in the integrity check.
- Entry: in the signal's direction (long > 0, short < 0) at the OPEN of the first bar opening at/after the entry time with market slippage; skipped when that bar opens more than 2 minutes late.
- Exit at the CLOSE of the last bar opening before the exit time with market slippage; a 16:00 exit (and any early close) is the session's last bar. Stop (optional) = entry open x (1 -/+ stop%) against the position, live intrabar from the entry bar, filled at the worse of the bar's open and the stop with stop slippage.
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
- Session: 09:30-16:00 ET of each NY date with data; Globex bars outside it are never loaded, so the previous close is the last RTH bar's close (09:30-16:00), not the 17:00 settlement.

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- The paper's effect is strongest on days dealers are short gamma; the bars cannot see dealer positioning, so z, rv_high and down_only are bar-observable stand-ins chosen before the run, not measured gamma.
- Post-2013 replications find the unconditional slope near zero in SPY / SPX; the 2018-2026 sample sits entirely in that decayed period.
- The 16:00 exit fills at the close of the 15:59 bar (the last RTH bar), not the 16:00 settlement or closing auction price; the 16:00-16:15 ES/NQ trading is never used.
- Early-close days (13:00 / 13:15 ET) have no 15:00+ bars, so no trade is taken on them.
- Sizing ignores volatility (full equity per trade, as in the other families).
