# Screening funnel -- lh_nq_v2 (development stages only)

- Code: `acf4e9adf0bf` (dirty working tree: True, diff sha256 `a14cc2c094ef`)
- Config: `configs/funnel/lh_funnel_nq_v2.yaml` sha256 `50542a2682a16bb6`; seed 20261126
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'NQ': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `c34027b5d5cfb211` (74 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No last-half-hour strategy has been scored on NQ 2023-2024, but the noise-band, mean-reversion, squeeze, convexity and EMRT families were selected there and the researcher has read those results.
- Holdout 2025+ previously inspected: **True** -- No last-half-hour metrics have been computed on NQ 2025+. Noise-band NQ picks and the month-end #7 transfer check were scored there, so the researcher has seen how that period treated intraday NQ strategies.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 1296 | 1296 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 1296 | 1296 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 1296 | 656 | 640 | 0 |  | 0 | 50.62 | 50.62 |  |
| 3 performance & risk | hard_gate | 656 | 104 | 552 | 0 |  | 0 | 8.02 | 15.85 |  |
| 4 parameter stability | hard_gate | 104 | 102 | 2 | 0 |  | 0 | 7.87 | 98.08 |  |
| 5 time stability | hard_gate | 102 | 102 | 0 | 0 |  | 102 | 7.87 | 100.00 |  |
| 6 deduplication | dedup | 102 | 74 |  |  | 28 |  | 5.71 | 72.55 | best 2 per cluster |
| 7 execution stress | hard_gate | 74 | 74 | 0 | 0 |  | 0 | 5.71 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 74 |  |  |  |  |  |  |  | diagnostic only: unverified: 74 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 640 |
| s2:hard_reject:years_with_>=10_trades | 368 |
| s3:hard_reject:max_drawdown | 14 |
| s3:hard_reject:net_return | 333 |
| s3:hard_reject:sharpe | 552 |
| s4:hard_reject:local_median_sharpe | 2 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_6e0d` | timeframe=1min, signal=prev_close, window=15:30-16:00, filter=none, fh_rel=any, late_rel=same, vol_gate=none, direction=follow, stop=none | 0/771/0 | 771 | 40.6% | 6.9% | 1.30 | -4.0% | 370 | 1.43 | 4.7% | 379.7 | 2/2 | 1.00 | 0.75 | 0.55 | 4 | 25.0% | 0.38 | 0.40 | 37.5% | 32.2% | 38.4% | 36.3%/27.7% | 7.1 (interpolated) | pass | 0.084 (unverified) | 0.78 |
| 2 | `cfg_6d2a` | timeframe=1min, signal=prev_close, window=15:30-16:00, filter=z0.5, fh_rel=any, late_rel=same, vol_gate=none, direction=follow, stop=none | 0/485/0 | 485 | 27.2% | 4.8% | 1.03 | -4.2% | 375 | 1.43 | 2.9% | 239.0 | 2/2 | 1.00 | 0.87 | 0.15 | 3 | 16.1% | 0.38 | 0.57 | 25.5% | 24.3% | 26.5% | 25.4%/19.9% | 8.1 (interpolated) | pass | 0.029 (unverified) | 0.65 |
| 3 | `cfg_d200` | timeframe=1min, signal=prev_close, window=15:30-16:00, filter=none, fh_rel=opp, late_rel=any, vol_gate=1.0, direction=follow, stop=none | 0/134/0 | 134 | 13.3% | 2.5% | 1.30 | -1.5% | 214 | 2.11 | 0.8% | 64.9 | 2/2 | 1.00 | 0.87 | 0.43 | 5 | 5.9% | 0.56 | 0.39 | 12.7% | 12.1% | 12.3% | 12.0%/10.0% | 14.4 (interpolated) | pass | 0.090 (unverified) | 1.31 |
| 4 | `cfg_64dd` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=z1.0, fh_rel=any, late_rel=any, vol_gate=none, direction=follow, stop=none | 0/408/0 | 408 | 43.3% | 7.3% | 1.24 | -8.1% | 533 | 1.61 | 4.9% | 200.4 | 2/2 | 1.00 | 0.82 | 0.43 | 3 | 22.2% | 0.49 | 0.46 | 41.0% | 37.5% | 45.8% | 36.7%/29.6% | 13.2 (interpolated) | pass | 0.087 (unverified) | 0.18 |
| 5 | `cfg_1708` | timeframe=1min, signal=prev_close, window=15:30-16:00, filter=none, fh_rel=any, late_rel=same, vol_gate=1.0, direction=follow, stop=none | 0/316/0 | 316 | 19.4% | 3.5% | 1.01 | -3.6% | 344 | 1.45 | 1.9% | 155.6 | 2/2 | 1.00 | 0.81 | 0.20 | 5 | 10.7% | 0.45 | 0.45 | 17.8% | 16.7% | 18.8% | 17.5%/12.8% | 8.4 (interpolated) | pass | 0.024 (unverified) | 0.82 |
| 6 | `cfg_8c22` | timeframe=1min, signal=open, window=15:30-16:00, filter=none, fh_rel=any, late_rel=same, vol_gate=1.0, direction=follow, stop=none | 0/332/0 | 332 | 24.6% | 4.4% | 1.23 | -2.9% | 298 | 1.54 | 2.0% | 164.0 | 2/2 | 1.00 | 0.87 | 0.36 | 4 | 12.8% | 0.48 | 0.37 | 23.0% | 21.6% | 23.7% | 21.4%/18.0% | 10.0 (interpolated) | pass | 0.077 (unverified) | 1.03 |
| 7 | `cfg_0d42` | timeframe=1min, signal=open, window=15:30-16:00, filter=z0.5, fh_rel=opp, late_rel=any, vol_gate=1.0, direction=follow, stop=none | 0/144/0 | 144 | 16.0% | 2.9% | 1.31 | -1.2% | 264 | 2.21 | 0.9% | 69.8 | 2/2 | 1.00 | 0.88 | 0.42 | 5 | 7.8% | 0.51 | 0.45 | 15.6% | 15.0% | 14.8% | 15.0%/12.8% | 15.7 (interpolated) | pass | 0.062 (unverified) | 1.16 |
| 8 | `cfg_a474` | timeframe=1min, signal=open, window=15:30-16:00, filter=z0.5, fh_rel=any, late_rel=same, vol_gate=none, direction=follow, stop=none | 0/515/0 | 515 | 23.0% | 4.1% | 0.94 | -3.8% | 305 | 1.34 | 3.1% | 253.9 | 2/2 | 1.00 | 0.76 | 0.19 | 3 | 12.5% | 0.40 | 0.52 | 21.5% | 19.3% | 20.3% | 21.0%/16.3% | 6.8 (interpolated) | pass | 0.012 (unverified) | 0.85 |
| 9 | `cfg_d2c7` | timeframe=1min, signal=prev_close, window=15:30-16:00, filter=none, fh_rel=any, late_rel=same, vol_gate=1.0, direction=follow, stop=0.20 | 0/206/110 | 316 | 16.7% | 3.1% | 1.07 | -2.8% | 328 | 1.46 | 1.6% | 154.9 | 2/2 | 1.00 | 0.87 | 0.21 | 5 | 10.2% | 0.35 | 0.52 | 15.5% | 14.3% | 13.7% | 15.2%/11.8% | 7.2 (interpolated) | pass | 0.021 (unverified) | 0.76 |
| 10 | `cfg_239d` | timeframe=1min, signal=open, window=15:30-16:00, filter=none, fh_rel=any, late_rel=same, vol_gate=none, direction=follow, stop=none | 0/793/0 | 793 | 34.2% | 5.9% | 1.18 | -5.2% | 337 | 1.36 | 4.8% | 390.9 | 2/2 | 1.00 | 0.68 | 0.50 | 4 | 15.5% | 0.55 | 0.36 | 29.6% | 26.6% | 31.6% | 29.0%/24.3% | 6.0 (interpolated) | pass | 0.048 (unverified) | 0.65 |
| 11 | `cfg_0bc2` | timeframe=1min, signal=open, window=15:30-16:00, filter=none, fh_rel=any, late_rel=any, vol_gate=1.0, direction=follow, stop=none | 0/497/0 | 497 | 25.1% | 4.5% | 1.07 | -3.4% | 301 | 1.36 | 3.0% | 244.3 | 2/2 | 1.00 | 0.80 | 0.27 | 4 | 13.9% | 0.45 | 0.41 | 23.0% | 20.2% | 24.2% | 21.9%/16.6% | 6.8 (interpolated) | pass | 0.055 (unverified) | 0.28 |
| 12 | `cfg_4874` | timeframe=1min, signal=open, window=15:30-16:00, filter=z0.5, fh_rel=opp, late_rel=same, vol_gate=1.0, direction=follow, stop=none | 0/101/0 | 101 | 9.4% | 1.8% | 1.11 | -2.0% | 630 | 2.11 | 0.6% | 48.8 | 2/2 | 1.00 | 0.80 | 0.31 | 4 | 2.1% | 0.78 | 0.50 | 9.0% | 8.7% | 8.5% | 8.3%/6.9% | 14.0 (interpolated) | pass | 0.028 (unverified) | 1.48 |
| 13 | `cfg_a3e7` | timeframe=1min, signal=open, window=15:00-16:00, filter=z1.0, fh_rel=any, late_rel=same, vol_gate=none, direction=follow, stop=0.20 | 0/157/103 | 260 | 17.3% | 3.2% | 1.10 | -8.0% | 810 | 1.53 | 2.4% | 127.3 | 2/2 | 1.00 | 0.76 | 0.34 | 3 | 4.1% | 0.73 | 0.51 | 16.3% | 15.0% | 11.8% | 15.3%/12.2% | 9.8 (interpolated) | pass | 0.020 (unverified) | 0.52 |
| 14 | `cfg_71bd` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=z0.5, fh_rel=any, late_rel=any, vol_gate=none, direction=follow, stop=none | 0/729/0 | 729 | 44.1% | 7.4% | 1.08 | -9.0% | 365 | 1.35 | 8.8% | 358.6 | 2/2 | 1.00 | 0.75 | 0.33 | 3 | 22.4% | 0.49 | 0.46 | 40.9% | 38.6% | 48.9% | 39.8%/28.7% | 7.9 (interpolated) | pass | 0.043 (unverified) | 0.25 |
| 15 | `cfg_6b90` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=z1.0, fh_rel=any, late_rel=same, vol_gate=none, direction=follow, stop=none | 0/273/0 | 273 | 21.7% | 3.9% | 1.00 | -5.6% | 839 | 1.49 | 3.3% | 135.4 | 2/2 | 1.00 | 0.89 | 0.12 | 3 | 3.9% | 0.79 | 0.46 | 21.4% | 20.1% | 24.0% | 19.9%/15.7% | 10.8 (interpolated) | pass | 0.021 (unverified) | 0.02 |
| 16 | `cfg_5add` | timeframe=1min, signal=open, window=15:30-16:00, filter=z0.5, fh_rel=any, late_rel=any, vol_gate=1.0, direction=follow, stop=none | 0/346/0 | 346 | 22.1% | 4.0% | 1.13 | -3.4% | 309 | 1.48 | 2.1% | 168.5 | 2/2 | 1.00 | 0.81 | 0.32 | 3 | 11.4% | 0.47 | 0.44 | 20.8% | 19.6% | 20.0% | 20.1%/16.1% | 8.9 (interpolated) | pass | 0.063 (unverified) | 0.47 |
| 17 | `cfg_eb8b` | timeframe=1min, signal=open, window=15:00-16:00, filter=z0.5, fh_rel=any, late_rel=any, vol_gate=1.5, direction=follow, stop=none | 0/124/0 | 124 | 19.8% | 3.6% | 1.09 | -2.7% | 177 | 1.94 | 1.5% | 60.7 | 2/2 | 1.00 | 0.93 | 0.16 | 4 | 10.7% | 0.43 | 0.50 | 19.3% | 18.8% | 18.9% | 17.9%/14.4% | 19.7 (interpolated) | pass | 0.042 (unverified) | 0.64 |
| 18 | `cfg_d966` | timeframe=1min, signal=open, window=15:30-16:00, filter=none, fh_rel=same, late_rel=same, vol_gate=none, direction=follow, stop=none | 0/471/0 | 471 | 17.3% | 3.2% | 0.81 | -4.9% | 393 | 1.29 | 2.8% | 232.4 | 2/2 | 1.00 | 0.50 | 0.31 | 3 | 5.2% | 0.67 | 0.67 | 15.9% | 14.1% | 16.6% | 16.0%/12.8% | 5.5 (interpolated) | pass | 0.005 (unverified) | 0.28 |
| 19 | `cfg_256e` | timeframe=1min, signal=open, window=15:30-16:00, filter=none, fh_rel=any, late_rel=same, vol_gate=1.0, direction=follow, stop=0.20 | 0/214/118 | 332 | 16.3% | 3.0% | 1.02 | -3.0% | 323 | 1.43 | 1.6% | 161.6 | 2/2 | 1.00 | 1.05 | -0.03 | 5 | 10.2% | 0.37 | 0.53 | 15.1% | 13.1% | 14.3% | 15.0%/11.7% | 7.2 (interpolated) | pass | 0.014 (unverified) | 0.70 |
| 20 | `cfg_dd5a` | timeframe=1min, signal=open, window=15:00-16:00, filter=none, fh_rel=opp, late_rel=same, vol_gate=1.0, direction=follow, stop=0.20 | 0/89/47 | 136 | 14.8% | 2.7% | 1.17 | -1.6% | 152 | 1.99 | 1.3% | 66.3 | 2/2 | 1.00 | 0.81 | 0.37 | 5 | 9.4% | 0.36 | 0.58 | 14.3% | 13.7% | 10.4% | 13.5%/10.2% | 15.5 (interpolated) | pass | 0.020 (unverified) | 1.34 |
| 21 | `cfg_21fa` | timeframe=1min, signal=open, window=15:00-16:00, filter=z1.0, fh_rel=any, late_rel=same, vol_gate=1.0, direction=follow, stop=0.20 | 0/79/65 | 144 | 11.2% | 2.1% | 0.86 | -6.4% | 799 | 1.57 | 1.3% | 70.6 | 2/2 | 1.00 | 0.68 | 0.18 | 3 | 2.8% | 0.73 | 0.76 | 10.8% | 10.4% | 7.0% | 10.2%/7.3% | 11.4 (interpolated) | pass | 0.003 (unverified) | 0.42 |
| 22 | `cfg_12b2` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=none, fh_rel=opp, late_rel=any, vol_gate=1.0, direction=follow, stop=0.20 | 0/72/46 | 118 | 11.4% | 2.1% | 1.03 | -2.2% | 841 | 1.84 | 1.1% | 57.8 | 2/2 | 1.00 | 0.87 | 0.16 | 5 | 6.2% | 0.44 | 0.64 | 11.0% | 10.5% | 10.6% | 10.4%/8.6% | 13.4 (interpolated) | pass | 0.009 (unverified) | 0.99 |
| 23 | `cfg_818a` | timeframe=1min, signal=open, window=15:00-16:00, filter=z1.0, fh_rel=opp, late_rel=any, vol_gate=none, direction=follow, stop=0.20 | 0/76/47 | 123 | 11.1% | 2.1% | 1.09 | -3.0% | 753 | 1.83 | 1.1% | 59.8 | 2/2 | 1.00 | 0.51 | 0.58 | 3 | 4.9% | 0.53 | 0.57 | 10.6% | 10.2% | 7.2% | 9.9%/7.8% | 12.7 (interpolated) | pass | 0.015 (unverified) | 0.59 |
| 24 | `cfg_77ef` | timeframe=1min, signal=open, window=15:00-16:00, filter=none, fh_rel=any, late_rel=any, vol_gate=none, direction=follow, stop=none | 0/1248/0 | 1248 | 39.8% | 6.8% | 0.85 | -11.9% | 466 | 1.19 | 15.1% | 614.7 | 2/2 | 1.00 | 0.62 | 0.24 | 4 | 21.5% | 0.46 | 0.40 | 35.3% | 32.1% | 44.9% | 37.1%/28.9% | 4.9 (interpolated) | pass | 0.011 (unverified) | -0.02 |
| 25 | `cfg_a0d4` | timeframe=1min, signal=open, window=15:00-16:00, filter=z0.5, fh_rel=opp, late_rel=same, vol_gate=none, direction=follow, stop=0.20 | 0/121/68 | 189 | 13.5% | 2.5% | 1.00 | -4.1% | 825 | 1.63 | 1.8% | 93.2 | 2/2 | 1.00 | 0.51 | 0.50 | 4 | 7.1% | 0.48 | 0.63 | 12.4% | 11.6% | 9.7% | 11.7%/9.5% | 9.9 (interpolated) | pass | 0.008 (unverified) | 0.84 |
| 26 | `cfg_6180` | timeframe=1min, signal=prev_close, window=15:30-16:00, filter=none, fh_rel=any, late_rel=any, vol_gate=1.0, direction=follow, stop=0.20 | 0/322/175 | 497 | 15.0% | 2.8% | 0.85 | -4.4% | 574 | 1.26 | 2.4% | 243.5 | 2/2 | 1.00 | 0.74 | 0.12 | 4 | 8.2% | 0.44 | 0.57 | 13.1% | 10.7% | 13.3% | 14.0%/9.4% | 4.3 (interpolated) | pass | 0.010 (unverified) | 0.08 |
| 27 | `cfg_8b39` | timeframe=1min, signal=open, window=15:00-16:00, filter=z0.5, fh_rel=any, late_rel=same, vol_gate=none, direction=follow, stop=0.20 | 0/312/190 | 502 | 20.7% | 3.7% | 1.02 | -10.9% | 790 | 1.33 | 4.8% | 248.0 | 2/2 | 1.00 | 0.76 | 0.26 | 3 | 7.4% | 0.60 | 0.46 | 18.8% | 17.0% | 15.5% | 18.8%/14.1% | 6.2 (interpolated) | pass | 0.015 (unverified) | 0.36 |
| 28 | `cfg_3dcf` | timeframe=1min, signal=open, window=15:30-16:00, filter=z1.0, fh_rel=any, late_rel=same, vol_gate=1.0, direction=follow, stop=none | 0/158/0 | 158 | 12.0% | 2.2% | 0.86 | -2.7% | 310 | 1.54 | 1.0% | 78.2 | 2/2 | 1.00 | 0.68 | 0.18 | 3 | 5.0% | 0.56 | 0.69 | 11.6% | 10.5% | 11.2% | 10.7%/7.8% | 10.1 (interpolated) | pass | 0.007 (unverified) | 1.07 |
| 29 | `cfg_d42d` | timeframe=1min, signal=open, window=15:00-16:00, filter=none, fh_rel=any, late_rel=same, vol_gate=1.5, direction=follow, stop=0.20 | 0/61/54 | 115 | 12.6% | 2.3% | 0.92 | -2.5% | 417 | 1.78 | 0.9% | 56.3 | 2/2 | 1.00 | 0.82 | 0.10 | 4 | 7.4% | 0.41 | 0.71 | 12.1% | 11.6% | 6.1% | 11.5%/8.3% | 14.4 (interpolated) | pass | 0.003 (unverified) | 0.64 |
| 30 | `cfg_47a4` | timeframe=1min, signal=open, window=15:30-16:00, filter=none, fh_rel=opp, late_rel=same, vol_gate=1.0, direction=follow, stop=none | 0/150/0 | 150 | 12.8% | 2.4% | 1.15 | -1.9% | 393 | 1.88 | 0.9% | 72.3 | 2/2 | 1.00 | 0.81 | 0.34 | 5 | 3.3% | 0.75 | 0.44 | 12.3% | 11.8% | 12.6% | 11.8%/10.2% | 13.1 (interpolated) | pass | 0.041 (unverified) | 1.43 |
| 31 | `cfg_74f0` | timeframe=1min, signal=open, window=15:30-16:00, filter=none, fh_rel=opp, late_rel=any, vol_gate=1.0, direction=follow, stop=none | 0/220/0 | 220 | 17.0% | 3.1% | 1.15 | -1.9% | 284 | 1.71 | 1.3% | 106.2 | 2/2 | 1.00 | 0.76 | 0.39 | 4 | 8.0% | 0.53 | 0.45 | 16.5% | 15.7% | 15.9% | 15.9%/13.4% | 11.5 (interpolated) | pass | 0.037 (unverified) | 1.01 |
| 32 | `cfg_f052` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=z0.5, fh_rel=any, late_rel=same, vol_gate=none, direction=follow, stop=none | 0/479/0 | 479 | 28.7% | 5.0% | 1.01 | -7.1% | 417 | 1.36 | 5.8% | 238.1 | 2/2 | 1.00 | 0.99 | 0.03 | 3 | 10.1% | 0.59 | 0.36 | 26.2% | 24.6% | 31.1% | 25.8%/21.2% | 8.6 (interpolated) | pass | 0.028 (unverified) | 0.22 |
| 33 | `cfg_1082` | timeframe=1min, signal=open, window=15:00-16:00, filter=z0.5, fh_rel=any, late_rel=any, vol_gate=none, direction=follow, stop=none | 0/744/0 | 744 | 35.2% | 6.1% | 0.92 | -8.9% | 564 | 1.28 | 9.0% | 365.3 | 2/2 | 1.00 | 0.62 | 0.30 | 4 | 17.6% | 0.43 | 0.41 | 32.5% | 28.9% | 38.8% | 31.5%/24.5% | 6.4 (interpolated) | pass | 0.017 (unverified) | 0.36 |
| 34 | `cfg_f1c0` | timeframe=1min, signal=open, window=15:00-16:00, filter=z1.0, fh_rel=any, late_rel=same, vol_gate=none, direction=follow, stop=none | 0/260/0 | 260 | 24.2% | 4.3% | 0.95 | -6.7% | 294 | 1.50 | 3.1% | 128.3 | 2/2 | 1.00 | 1.07 | -0.12 | 4 | 6.1% | 0.70 | 0.39 | 23.4% | 22.4% | 26.8% | 21.9%/15.4% | 12.7 (interpolated) | pass | 0.034 (unverified) | 0.51 |
| 35 | `cfg_ee3d` | timeframe=1min, signal=open, window=15:00-16:00, filter=none, fh_rel=any, late_rel=any, vol_gate=1.5, direction=follow, stop=none | 0/166/0 | 166 | 20.8% | 3.8% | 1.01 | -3.1% | 214 | 1.70 | 2.0% | 81.1 | 2/2 | 1.00 | 0.75 | 0.26 | 4 | 10.9% | 0.44 | 0.47 | 19.7% | 19.8% | 20.4% | 19.1%/15.6% | 17.1 (interpolated) | pass | 0.035 (unverified) | 0.68 |
| 36 | `cfg_b477` | timeframe=1min, signal=open, window=15:30-16:00, filter=z0.5, fh_rel=any, late_rel=same, vol_gate=1.0, direction=follow, stop=0.20 | 0/151/88 | 239 | 12.4% | 2.3% | 0.90 | -3.3% | 349 | 1.45 | 1.2% | 115.9 | 2/2 | 1.00 | 0.97 | -0.07 | 4 | 6.3% | 0.46 | 0.68 | 11.5% | 10.1% | 10.0% | 10.8%/8.0% | 7.6 (interpolated) | pass | 0.005 (unverified) | 0.72 |
| 37 | `cfg_6b57` | timeframe=1min, signal=open, window=15:00-16:00, filter=z1.0, fh_rel=any, late_rel=same, vol_gate=1.0, direction=follow, stop=none | 0/144/0 | 144 | 14.5% | 2.7% | 0.84 | -4.2% | 548 | 1.53 | 1.7% | 71.6 | 2/2 | 1.00 | 0.86 | -0.02 | 4 | 2.5% | 0.81 | 0.63 | 13.9% | 13.4% | 14.0% | 13.1%/10.9% | 13.6 (interpolated) | pass | 0.008 (unverified) | 0.51 |
| 38 | `cfg_e6c4` | timeframe=1min, signal=prev_close, window=15:30-16:00, filter=none, fh_rel=opp, late_rel=any, vol_gate=1.0, direction=follow, stop=0.20 | 0/93/41 | 134 | 7.4% | 1.4% | 0.88 | -2.2% | 402 | 1.59 | 0.7% | 65.1 | 2/2 | 1.00 | 1.17 | -0.28 | 4 | 1.9% | 0.74 | 0.64 | 6.9% | 6.5% | 7.7% | 7.0%/4.9% | 8.9 (interpolated) | pass | 0.012 (unverified) | 0.91 |
| 39 | `cfg_eb27` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=z1.0, fh_rel=any, late_rel=any, vol_gate=1.0, direction=follow, stop=0.20 | 0/114/89 | 203 | 18.0% | 3.3% | 1.02 | -3.1% | 286 | 1.63 | 1.8% | 99.2 | 2/2 | 1.00 | 0.57 | 0.45 | 4 | 7.9% | 0.56 | 0.60 | 16.7% | 16.0% | 10.8% | 16.4%/12.4% | 11.4 (interpolated) | pass | 0.008 (unverified) | -0.27 |
| 40 | `cfg_5e30` | timeframe=1min, signal=open, window=15:00-16:00, filter=z0.5, fh_rel=any, late_rel=any, vol_gate=1.5, direction=follow, stop=0.20 | 0/68/56 | 124 | 13.7% | 2.5% | 0.98 | -3.8% | 292 | 1.79 | 1.0% | 61.0 | 2/2 | 1.00 | 0.92 | 0.05 | 4 | 8.9% | 0.35 | 0.66 | 13.2% | 12.5% | 7.3% | 12.4%/9.3% | 14.2 (interpolated) | pass | 0.005 (unverified) | 0.08 |
| 41 | `cfg_bf03` | timeframe=1min, signal=open, window=15:00-16:00, filter=z0.5, fh_rel=same, late_rel=same, vol_gate=none, direction=follow, stop=none | 0/313/0 | 313 | 18.7% | 3.4% | 0.87 | -7.2% | 406 | 1.38 | 3.8% | 154.2 | 2/2 | 1.00 | 0.66 | 0.21 | 4 | 5.2% | 0.69 | 0.53 | 17.0% | 15.5% | 22.9% | 16.4%/12.3% | 8.1 (interpolated) | pass | 0.012 (unverified) | 0.25 |
| 42 | `cfg_b724` | timeframe=1min, signal=open, window=15:00-16:00, filter=z1.0, fh_rel=any, late_rel=any, vol_gate=none, direction=follow, stop=0.20 | 0/225/145 | 370 | 18.4% | 3.3% | 1.03 | -8.7% | 840 | 1.39 | 3.5% | 181.6 | 2/2 | 1.00 | 0.70 | 0.33 | 3 | 3.7% | 0.77 | 0.49 | 16.5% | 15.2% | 11.3% | 16.5%/13.6% | 6.9 (interpolated) | pass | 0.016 (unverified) | 0.27 |
| 43 | `cfg_e5f7` | timeframe=1min, signal=open, window=15:30-16:00, filter=z0.5, fh_rel=same, late_rel=same, vol_gate=none, direction=follow, stop=none | 0/327/0 | 327 | 15.7% | 2.9% | 0.81 | -4.8% | 610 | 1.35 | 2.0% | 160.2 | 2/2 | 1.00 | 0.63 | 0.18 | 3 | 4.4% | 0.69 | 0.73 | 14.8% | 14.0% | 14.2% | 14.9%/11.5% | 7.1 (interpolated) | pass | 0.003 (unverified) | 0.44 |
| 44 | `cfg_5956` | timeframe=1min, signal=open, window=15:30-16:00, filter=none, fh_rel=any, late_rel=same, vol_gate=1.5, direction=follow, stop=0.20 | 0/67/43 | 110 | 8.3% | 1.6% | 0.78 | -1.7% | 324 | 1.64 | 0.5% | 53.8 | 2/2 | 1.00 | 0.83 | -0.05 | 4 | 4.6% | 0.45 | 0.92 | 7.5% | 7.1% | 5.4% | 7.5%/5.4% | 11.0 (interpolated) | pass | 0.001 (unverified) | 1.05 |
| 45 | `cfg_12ad` | timeframe=1min, signal=prev_close, window=15:30-16:00, filter=z0.5, fh_rel=opp, late_rel=any, vol_gate=none, direction=follow, stop=none | 0/107/0 | 107 | 7.2% | 1.4% | 0.92 | -1.6% | 392 | 1.83 | 0.6% | 51.5 | 2/2 | 1.00 | 0.96 | -0.04 | 5 | 1.4% | 0.81 | 0.59 | 6.8% | 6.4% | 5.8% | 6.4%/5.1% | 10.6 (interpolated) | pass | 0.018 (unverified) | 1.04 |
| 46 | `cfg_e4b6` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=z1.0, fh_rel=same, late_rel=same, vol_gate=none, direction=follow, stop=none | 0/242/0 | 242 | 16.0% | 2.9% | 0.83 | -5.0% | 844 | 1.41 | 2.9% | 119.6 | 2/2 | 1.00 | 0.69 | 0.13 | 3 | 1.3% | 0.91 | 0.61 | 14.8% | 13.7% | 17.3% | 14.0%/10.4% | 9.3 (interpolated) | pass | 0.007 (unverified) | -0.21 |
| 47 | `cfg_acf8` | timeframe=1min, signal=open, window=15:00-16:00, filter=z0.5, fh_rel=any, late_rel=same, vol_gate=none, direction=follow, stop=none | 0/502/0 | 502 | 27.9% | 4.9% | 0.88 | -10.9% | 765 | 1.32 | 6.1% | 249.2 | 2/2 | 1.00 | 0.98 | -0.10 | 4 | 9.8% | 0.59 | 0.38 | 25.7% | 24.0% | 34.2% | 24.7%/19.7% | 7.8 (interpolated) | pass | 0.020 (unverified) | 0.40 |
| 48 | `cfg_d55d` | timeframe=1min, signal=open, window=15:00-16:00, filter=none, fh_rel=any, late_rel=any, vol_gate=1.0, direction=follow, stop=none | 0/484/0 | 484 | 30.4% | 5.3% | 0.96 | -8.3% | 285 | 1.33 | 5.9% | 236.7 | 2/2 | 1.00 | 0.99 | -0.03 | 4 | 18.1% | 0.34 | 0.40 | 28.2% | 26.5% | 30.7% | 26.1%/20.3% | 8.6 (interpolated) | pass | 0.024 (unverified) | 0.29 |
| 49 | `cfg_0f17` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=z1.0, fh_rel=any, late_rel=any, vol_gate=none, direction=follow, stop=0.20 | 0/256/152 | 408 | 20.9% | 3.8% | 1.02 | -6.8% | 515 | 1.40 | 3.9% | 200.5 | 2/2 | 1.00 | 0.78 | 0.24 | 3 | 6.8% | 0.68 | 0.52 | 19.5% | 16.7% | 16.1% | 18.9%/15.0% | 7.5 (interpolated) | pass | 0.012 (unverified) | -0.30 |
| 50 | `cfg_6295` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=none, fh_rel=opp, late_rel=any, vol_gate=none, direction=follow, stop=0.20 | 0/190/102 | 292 | 13.4% | 2.5% | 0.95 | -4.9% | 898 | 1.41 | 2.8% | 143.0 | 2/2 | 1.00 | 0.74 | 0.20 | 3 | 5.3% | 0.57 | 0.56 | 12.3% | 11.4% | 14.1% | 11.7%/9.7% | 6.8 (interpolated) | pass | 0.009 (unverified) | 0.76 |
| 51 | `cfg_424e` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=none, fh_rel=opp, late_rel=same, vol_gate=none, direction=follow, stop=none | 0/202/0 | 202 | 13.9% | 2.6% | 0.88 | -3.4% | 213 | 1.52 | 2.4% | 98.9 | 2/2 | 1.00 | 0.94 | -0.07 | 5 | 8.7% | 0.37 | 0.58 | 13.1% | 12.7% | 13.3% | 12.8%/10.1% | 9.6 (interpolated) | pass | 0.012 (unverified) | 0.62 |
| 52 | `cfg_87a1` | timeframe=1min, signal=open, window=15:00-16:00, filter=z0.5, fh_rel=any, late_rel=any, vol_gate=none, direction=follow, stop=0.20 | 0/459/285 | 744 | 17.9% | 3.3% | 0.78 | -11.1% | 790 | 1.20 | 7.1% | 364.2 | 2/2 | 1.00 | 0.74 | 0.04 | 3 | 7.3% | 0.59 | 0.53 | 15.0% | 11.7% | 12.2% | 15.7%/12.2% | 4.1 (interpolated) | pass | 0.004 (unverified) | -0.00 |
| 53 | `cfg_5669` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=z1.0, fh_rel=any, late_rel=same, vol_gate=none, direction=follow, stop=0.20 | 0/165/108 | 273 | 13.7% | 2.5% | 0.86 | -8.0% | 1010 | 1.39 | 2.6% | 134.3 | 2/2 | 1.00 | 0.75 | 0.11 | 3 | -0.2% | 1.02 | 0.70 | 12.7% | 11.5% | 8.7% | 12.4%/9.4% | 7.4 (interpolated) | pass | 0.005 (unverified) | -0.07 |
| 54 | `cfg_910e` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=none, fh_rel=opp, late_rel=any, vol_gate=none, direction=follow, stop=none | 0/292/0 | 292 | 16.5% | 3.0% | 0.86 | -5.9% | 380 | 1.41 | 3.5% | 142.8 | 2/2 | 1.00 | 0.89 | -0.03 | 3 | 8.7% | 0.45 | 0.49 | 15.6% | 14.7% | 16.0% | 15.3%/11.0% | 8.1 (interpolated) | pass | 0.013 (unverified) | 0.87 |
| 55 | `cfg_fbcd` | timeframe=1min, signal=open, window=15:00-16:00, filter=none, fh_rel=opp, late_rel=same, vol_gate=1.0, direction=follow, stop=none | 0/136/0 | 136 | 13.8% | 2.6% | 0.85 | -3.2% | 212 | 1.62 | 1.6% | 66.2 | 2/2 | 1.00 | 1.16 | -0.31 | 5 | 8.9% | 0.33 | 0.64 | 13.1% | 12.6% | 13.1% | 12.6%/10.0% | 15.0 (interpolated) | pass | 0.010 (unverified) | 1.11 |
| 56 | `cfg_e919` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=z0.5, fh_rel=any, late_rel=same, vol_gate=none, direction=follow, stop=0.20 | 0/303/177 | 480 | 17.9% | 3.3% | 0.95 | -8.4% | 842 | 1.31 | 4.6% | 234.7 | 2/2 | 1.00 | 0.87 | 0.08 | 3 | 4.2% | 0.74 | 0.53 | 16.0% | 13.2% | 12.1% | 16.0%/12.0% | 5.7 (interpolated) | pass | 0.010 (unverified) | 0.13 |
| 57 | `cfg_e831` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=none, fh_rel=opp, late_rel=any, vol_gate=1.0, direction=follow, stop=none | 0/118/0 | 118 | 12.0% | 2.2% | 0.86 | -2.7% | 272 | 1.68 | 1.4% | 57.4 | 2/2 | 1.00 | 1.17 | -0.31 | 4 | 6.3% | 0.47 | 0.64 | 11.5% | 11.0% | 12.0% | 10.8%/8.7% | 13.5 (interpolated) | pass | 0.012 (unverified) | 0.95 |
| 58 | `cfg_57b4` | timeframe=1min, signal=open, window=15:00-16:00, filter=z0.5, fh_rel=any, late_rel=same, vol_gate=1.0, direction=follow, stop=0.20 | 0/121/103 | 224 | 12.6% | 2.3% | 0.78 | -6.2% | 739 | 1.40 | 2.0% | 110.2 | 2/2 | 1.00 | 0.87 | -0.09 | 3 | 5.9% | 0.51 | 0.74 | 11.8% | 11.5% | 9.7% | 11.4%/7.9% | 8.1 (interpolated) | pass | 0.002 (unverified) | 0.30 |
| 59 | `cfg_6c55` | timeframe=1min, signal=prev_close, window=15:30-16:00, filter=none, fh_rel=any, late_rel=same, vol_gate=none, direction=follow, stop=0.20 | 0/549/222 | 771 | 14.9% | 2.7% | 0.78 | -5.2% | 495 | 1.19 | 4.0% | 375.7 | 2/2 | 1.00 | 0.96 | -0.18 | 4 | 8.1% | 0.46 | 0.59 | 12.0% | 7.5% | 14.2% | 13.6%/9.0% | 3.5 (interpolated) | pass | 0.005 (unverified) | 0.48 |
| 60 | `cfg_ff8c` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=z0.5, fh_rel=any, late_rel=any, vol_gate=none, direction=follow, stop=0.20 | 0/454/276 | 730 | 20.2% | 3.7% | 0.85 | -6.4% | 517 | 1.23 | 6.9% | 355.8 | 2/2 | 1.00 | 0.77 | 0.07 | 3 | 4.1% | 0.80 | 0.54 | 15.6% | 12.4% | 16.2% | 16.8%/12.3% | 4.5 (interpolated) | pass | 0.005 (unverified) | -0.08 |
| 61 | `cfg_f401` | timeframe=1min, signal=open, window=15:00-16:00, filter=z1.0, fh_rel=any, late_rel=any, vol_gate=none, direction=follow, stop=none | 0/370/0 | 370 | 25.4% | 4.5% | 0.92 | -7.2% | 504 | 1.39 | 4.5% | 182.0 | 2/2 | 1.00 | 0.83 | 0.09 | 3 | 5.0% | 0.76 | 0.39 | 23.6% | 22.5% | 28.2% | 23.0%/18.4% | 9.7 (interpolated) | pass | 0.030 (unverified) | 0.40 |
| 62 | `cfg_fa95` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=z0.5, fh_rel=any, late_rel=same, vol_gate=1.0, direction=follow, stop=0.20 | 0/114/98 | 212 | 12.2% | 2.3% | 0.82 | -4.3% | 548 | 1.41 | 1.9% | 103.8 | 2/2 | 1.00 | 0.74 | 0.07 | 4 | 3.7% | 0.67 | 0.74 | 11.4% | 10.4% | 5.3% | 11.3%/9.1% | 8.0 (interpolated) | pass | 0.003 (unverified) | 0.06 |
| 63 | `cfg_7ade` | timeframe=1min, signal=open, window=15:30-16:00, filter=z0.5, fh_rel=any, late_rel=any, vol_gate=1.5, direction=follow, stop=none | 0/123/0 | 123 | 11.4% | 2.1% | 0.89 | -2.6% | 325 | 1.68 | 0.7% | 60.5 | 2/2 | 1.00 | 0.92 | -0.03 | 3 | 5.8% | 0.48 | 0.71 | 10.4% | 10.0% | 8.6% | 10.0%/7.1% | 12.5 (interpolated) | pass | 0.014 (unverified) | 0.96 |
| 64 | `cfg_e117` | timeframe=1min, signal=open, window=15:00-16:00, filter=none, fh_rel=any, late_rel=same, vol_gate=1.0, direction=follow, stop=0.20 | 0/179/144 | 323 | 15.8% | 2.9% | 0.86 | -5.0% | 423 | 1.35 | 2.9% | 158.6 | 2/2 | 1.00 | 0.87 | -0.01 | 4 | 8.5% | 0.43 | 0.59 | 15.0% | 13.4% | 10.1% | 14.3%/11.3% | 7.4 (interpolated) | pass | 0.005 (unverified) | 0.65 |
| 65 | `cfg_c452` | timeframe=1min, signal=open, window=15:30-16:00, filter=z0.5, fh_rel=opp, late_rel=any, vol_gate=1.0, direction=follow, stop=0.20 | 0/101/43 | 144 | 10.3% | 1.9% | 0.97 | -1.9% | 316 | 1.76 | 0.7% | 69.8 | 2/2 | 1.00 | 1.07 | -0.10 | 4 | 3.8% | 0.63 | 0.63 | 9.7% | 9.2% | 7.9% | 9.2%/7.3% | 10.4 (interpolated) | pass | 0.007 (unverified) | 0.67 |
| 66 | `cfg_30a1` | timeframe=1min, signal=open, window=15:30-16:00, filter=z0.5, fh_rel=any, late_rel=any, vol_gate=1.0, direction=follow, stop=0.20 | 0/218/128 | 346 | 13.7% | 2.5% | 0.83 | -5.9% | 574 | 1.33 | 1.7% | 168.6 | 2/2 | 1.00 | 0.83 | -0.01 | 3 | 6.4% | 0.53 | 0.70 | 12.5% | 10.9% | 8.2% | 12.7%/8.8% | 5.7 (interpolated) | pass | 0.017 (unverified) | 0.11 |
| 67 | `cfg_f7e4` | timeframe=1min, signal=open, window=15:00-16:00, filter=none, fh_rel=any, late_rel=any, vol_gate=none, direction=follow, stop=0.20 | 0/798/451 | 1249 | 23.7% | 4.2% | 0.81 | -11.8% | 756 | 1.16 | 12.1% | 610.9 | 2/2 | 1.00 | 0.58 | 0.24 | 4 | 10.3% | 0.57 | 0.44 | 16.8% | 10.7% | 20.4% | 20.1%/14.9% | 3.1 (interpolated) | pass | 0.005 (unverified) | -0.37 |
| 68 | `cfg_e50f` | timeframe=1min, signal=prev_close, window=15:30-16:00, filter=none, fh_rel=opp, late_rel=any, vol_gate=none, direction=follow, stop=none | 0/304/0 | 304 | 12.4% | 2.3% | 0.83 | -4.6% | 416 | 1.42 | 1.8% | 148.6 | 2/2 | 1.00 | 0.74 | 0.09 | 3 | 4.4% | 0.64 | 0.53 | 11.3% | 9.5% | 10.8% | 11.2%/9.1% | 6.3 (interpolated) | pass | 0.011 (unverified) | 1.00 |
| 69 | `cfg_8ef8` | timeframe=1min, signal=open, window=15:00-16:00, filter=z0.5, fh_rel=opp, late_rel=any, vol_gate=1.0, direction=follow, stop=none | 0/142/0 | 142 | 13.1% | 2.4% | 0.80 | -3.1% | 272 | 1.57 | 1.7% | 69.3 | 2/2 | 1.00 | 1.07 | -0.27 | 5 | 8.1% | 0.36 | 0.67 | 12.5% | 12.5% | 12.7% | 12.2%/9.0% | 13.4 (interpolated) | pass | 0.006 (unverified) | 0.72 |
| 70 | `cfg_112d` | timeframe=1min, signal=prev_close, window=15:00-16:00, filter=none, fh_rel=any, late_rel=any, vol_gate=1.0, direction=follow, stop=0.20 | 0/263/221 | 484 | 17.0% | 3.1% | 0.77 | -4.9% | 352 | 1.25 | 4.3% | 237.0 | 2/2 | 1.00 | 0.73 | 0.05 | 4 | 10.7% | 0.35 | 0.60 | 15.1% | 13.7% | 15.4% | 15.5%/11.7% | 5.2 (interpolated) | pass | 0.003 (unverified) | -0.02 |
| 71 | `cfg_846e` | timeframe=1min, signal=open, window=15:00-16:00, filter=z1.0, fh_rel=any, late_rel=any, vol_gate=1.0, direction=follow, stop=0.20 | 0/112/92 | 204 | 11.4% | 2.1% | 0.78 | -6.7% | 799 | 1.41 | 1.8% | 99.7 | 2/2 | 1.00 | 0.53 | 0.25 | 3 | 2.6% | 0.75 | 0.75 | 10.8% | 10.1% | 6.9% | 10.5%/7.4% | 7.9 (interpolated) | pass | 0.003 (unverified) | 0.22 |
| 72 | `cfg_21f7` | timeframe=1min, signal=open, window=15:00-16:00, filter=none, fh_rel=any, late_rel=any, vol_gate=1.0, direction=follow, stop=0.20 | 0/269/215 | 484 | 20.5% | 3.7% | 0.90 | -4.3% | 428 | 1.30 | 4.3% | 236.9 | 2/2 | 1.00 | 0.80 | 0.09 | 4 | 11.5% | 0.41 | 0.51 | 18.6% | 16.7% | 15.9% | 18.7%/14.8% | 6.3 (interpolated) | pass | 0.007 (unverified) | 0.15 |
| 73 | `cfg_8dfb` | timeframe=1min, signal=open, window=15:30-16:00, filter=none, fh_rel=opp, late_rel=same, vol_gate=1.0, direction=follow, stop=0.20 | 0/104/46 | 150 | 6.7% | 1.3% | 0.77 | -3.1% | 987 | 1.47 | 0.8% | 73.1 | 2/2 | 1.00 | 1.16 | -0.39 | 4 | -0.3% | 1.05 | 0.65 | 6.2% | 5.6% | 9.6% | 6.0%/4.1% | 8.0 (interpolated) | pass | 0.005 (unverified) | 0.89 |
| 74 | `cfg_4f3f` | timeframe=1min, signal=prev_close, window=15:30-16:00, filter=none, fh_rel=opp, late_rel=same, vol_gate=none, direction=follow, stop=none | 0/210/0 | 210 | 11.2% | 2.1% | 0.98 | -4.3% | 819 | 1.64 | 1.3% | 102.7 | 2/2 | 1.00 | 0.74 | 0.24 | 3 | 2.9% | 0.75 | 0.52 | 10.5% | 9.4% | 10.2% | 9.8%/8.1% | 8.4 (interpolated) | pass | 0.018 (unverified) | 0.79 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 9.7% / 2.08 / 153 | -1.9% / -0.83 / 131 | 13.6% / 1.41 / 164 | 2.2% / 0.84 / 144 | 12.5% / 2.49 / 179 |
| 2 | 9.6% / 2.22 / 90 | -0.6% / -0.32 / 75 | 9.6% / 1.11 / 101 | -1.4% / -0.62 / 93 | 8.1% / 1.95 / 126 |
| 3 | 1.2% / 0.67 / 25 | 0.1% / 0.11 / 22 | 1.6% / 0.74 / 28 | 2.9% / 1.73 / 30 | 7.0% / 2.56 / 29 |
| 4 | 13.0% / 2.09 / 84 | -4.8% / -2.15 / 72 | 18.7% / 1.81 / 82 | -4.2% / -1.50 / 85 | 17.2% / 2.90 / 85 |
| 5 | 7.1% / 1.77 / 66 | 0.5% / 0.34 / 46 | 1.2% / 0.25 / 68 | 1.7% / 0.73 / 63 | 7.8% / 2.02 / 73 |
| 6 | 9.0% / 2.13 / 68 | -0.2% / -0.11 / 53 | 2.4% / 0.54 / 67 | 1.3% / 0.57 / 68 | 10.5% / 2.28 / 76 |
| 7 | 1.3% / 0.72 / 26 | 0.3% / 0.25 / 27 | 5.6% / 1.65 / 29 | 0.6% / 0.36 / 31 | 7.5% / 2.59 / 31 |
| 8 | 9.3% / 2.21 / 94 | -2.5% / -1.19 / 80 | 8.5% / 1.11 / 102 | -0.8% / -0.38 / 104 | 7.3% / 1.65 / 135 |
| 9 | 5.9% / 1.51 / 66 | 1.1% / 0.76 / 46 | 4.5% / 1.27 / 68 | 0.6% / 0.31 / 63 | 3.7% / 1.22 / 73 |
| 10 | 11.7% / 2.42 / 154 | -3.4% / -1.41 / 141 | 5.2% / 0.66 / 162 | 1.8% / 0.64 / 154 | 16.1% / 2.86 / 182 |
| 11 | 10.4% / 2.14 / 109 | -1.6% / -0.85 / 82 | 4.9% / 0.86 / 97 | 0.0% / 0.03 / 105 | 9.8% / 1.95 / 104 |
| 12 | -1.3% / -0.99 / 17 | 0.5% / 0.46 / 19 | 2.8% / 1.41 / 20 | 0.1% / 0.12 / 19 | 7.1% / 3.09 / 26 |
| 13 | 12.7% / 2.82 / 48 | -2.6% / -1.94 / 40 | -4.9% / -2.53 / 52 | 3.5% / 1.40 / 53 | 8.6% / 2.37 / 67 |
| 14 | 11.2% / 1.65 / 133 | -4.9% / -1.73 / 139 | 20.1% / 1.75 / 147 | -3.6% / -1.06 / 146 | 17.7% / 2.09 / 164 |
| 15 | 17.2% / 3.15 / 60 | -4.7% / -2.81 / 42 | 0.8% / 0.19 / 54 | -0.9% / -0.39 / 50 | 9.2% / 1.84 / 67 |
| 16 | 8.1% / 2.00 / 67 | -1.1% / -0.66 / 61 | 9.7% / 1.89 / 65 | -1.6% / -0.64 / 77 | 5.8% / 1.43 / 76 |
| 17 | 4.4% / 1.18 / 29 | -1.4% / -0.79 / 25 | 8.2% / 2.03 / 29 | 2.8% / 1.01 / 28 | 4.6% / 1.14 / 13 |
| 18 | 11.5% / 2.72 / 89 | -1.6% / -0.91 / 74 | 7.0% / 1.08 / 100 | -1.9% / -0.88 / 90 | 1.9% / 0.49 / 118 |
| 19 | 5.8% / 1.47 / 68 | 0.4% / 0.30 / 53 | 3.4% / 0.95 / 67 | 0.3% / 0.15 / 68 | 5.5% / 1.68 / 76 |
| 20 | 2.1% / 1.02 / 30 | 0.4% / 0.32 / 24 | 3.0% / 1.07 / 27 | 3.7% / 1.55 / 23 | 4.9% / 1.58 / 32 |
| 21 | 8.2% / 2.09 / 32 | -2.9% / -2.54 / 25 | -3.3% / -2.66 / 25 | 4.4% / 1.88 / 26 | 4.9% / 1.63 / 36 |
| 22 | 1.7% / 0.85 / 26 | 0.1% / 0.14 / 19 | 0.1% / 0.08 / 26 | 4.9% / 1.78 / 21 | 4.2% / 1.50 / 26 |
| 23 | 5.9% / 2.49 / 26 | -0.6% / -0.59 / 21 | -2.2% / -1.44 / 26 | 3.2% / 1.64 / 23 | 4.5% / 1.74 / 27 |
| 24 | 12.3% / 1.65 / 248 | -6.6% / -1.89 / 249 | 10.1% / 0.82 / 251 | 5.1% / 1.02 / 251 | 15.1% / 1.53 / 249 |
| 25 | 3.3% / 1.41 / 36 | -1.6% / -1.07 / 38 | 0.5% / 0.20 / 41 | 4.8% / 1.87 / 34 | 6.0% / 1.86 / 40 |
| 26 | 5.6% / 1.32 / 109 | 0.3% / 0.18 / 82 | 6.3% / 1.51 / 97 | -1.2% / -0.46 / 105 | 3.4% / 0.98 / 104 |
| 27 | 12.4% / 2.51 / 98 | -6.2% / -3.12 / 86 | -2.9% / -0.79 / 107 | 7.3% / 2.23 / 87 | 10.0% / 2.15 / 124 |
| 28 | 6.6% / 1.79 / 36 | -0.3% / -0.23 / 29 | 1.5% / 0.50 / 28 | -0.4% / -0.26 / 29 | 4.2% / 1.42 / 36 |
| 29 | 3.3% / 1.04 / 25 | -1.3% / -0.90 / 23 | 2.1% / 0.77 / 24 | 3.1% / 1.22 / 22 | 4.8% / 1.75 / 21 |
| 30 | 0.1% / 0.04 / 27 | 0.2% / 0.20 / 26 | 0.8% / 0.31 / 33 | 2.2% / 1.46 / 31 | 9.3% / 3.01 / 33 |
| 31 | 3.0% / 1.12 / 43 | -0.6% / -0.50 / 39 | 2.8% / 0.76 / 47 | 2.6% / 1.41 / 47 | 8.3% / 2.30 / 44 |
| 32 | 16.9% / 2.76 / 94 | -5.7% / -2.46 / 79 | 7.8% / 1.31 / 97 | -0.0% / 0.01 / 89 | 8.3% / 1.17 / 120 |
| 33 | 15.0% / 2.27 / 139 | -6.2% / -2.13 / 138 | 5.6% / 0.56 / 153 | 6.1% / 1.47 / 153 | 11.9% / 1.58 / 161 |
| 34 | 17.0% / 3.31 / 48 | -3.1% / -1.78 / 40 | 1.5% / 0.24 / 52 | 1.3% / 0.48 / 53 | 6.6% / 1.32 / 67 |
| 35 | 3.6% / 0.96 / 41 | -1.3% / -0.63 / 30 | 8.9% / 2.25 / 36 | 3.6% / 1.11 / 35 | 4.7% / 0.87 / 24 |
| 36 | 5.7% / 1.60 / 45 | 0.1% / 0.09 / 42 | 3.4% / 1.01 / 46 | -1.6% / -1.11 / 47 | 4.4% / 1.62 / 59 |
| 37 | 11.7% / 2.59 / 32 | -3.6% / -2.24 / 25 | 0.9% / 0.37 / 25 | 2.9% / 1.13 / 26 | 2.2% / 0.54 / 36 |
| 38 | -0.6% / -0.39 / 25 | 0.2% / 0.17 / 22 | 0.5% / 0.35 / 28 | 1.8% / 1.14 / 30 | 5.4% / 2.36 / 29 |
| 39 | 7.5% / 1.77 / 45 | -3.1% / -2.11 / 35 | 3.3% / 0.81 / 41 | 0.3% / 0.15 / 45 | 9.4% / 2.34 / 37 |
| 40 | 3.7% / 1.08 / 29 | -1.2% / -0.80 / 25 | 1.9% / 0.69 / 29 | 4.4% / 1.60 / 28 | 4.4% / 1.71 / 13 |
| 41 | 12.8% / 2.44 / 62 | -5.4% / -2.84 / 48 | 4.6% / 1.01 / 66 | 1.5% / 0.61 / 53 | 4.7% / 0.95 / 84 |
| 42 | 14.1% / 2.86 / 68 | -1.6% / -0.87 / 65 | -6.2% / -2.67 / 74 | 2.8% / 0.98 / 86 | 9.2% / 2.26 / 77 |
| 43 | 10.9% / 2.70 / 56 | -2.1% / -1.36 / 48 | 8.5% / 1.38 / 67 | -1.9% / -1.02 / 66 | 0.1% / 0.05 / 90 |
| 44 | 2.3% / 0.82 / 22 | 0.8% / 0.59 / 25 | 3.6% / 1.24 / 27 | -0.2% / -0.20 / 21 | 1.7% / 1.06 / 15 |
| 45 | 0.1% / 0.08 / 21 | 0.4% / 0.50 / 15 | 0.3% / 0.22 / 18 | 0.5% / 0.47 / 22 | 5.7% / 2.39 / 31 |
| 46 | 14.5% / 2.91 / 52 | -4.5% / -2.81 / 37 | 1.7% / 0.40 / 51 | -0.5% / -0.22 / 43 | 4.8% / 1.20 / 59 |
| 47 | 16.5% / 2.77 / 98 | -6.4% / -2.63 / 86 | 2.4% / 0.32 / 107 | 6.3% / 1.83 / 87 | 7.8% / 1.15 / 124 |
| 48 | 10.5% / 1.82 / 107 | -2.5% / -1.00 / 78 | 8.8% / 1.24 / 105 | 5.5% / 1.30 / 97 | 5.6% / 0.74 / 97 |
| 49 | 12.0% / 2.43 / 84 | -4.3% / -2.30 / 72 | 1.6% / 0.36 / 82 | -1.9% / -0.86 / 85 | 13.3% / 2.86 / 85 |
| 50 | 1.8% / 0.69 / 63 | -2.1% / -1.32 / 56 | -0.5% / -0.20 / 54 | 7.7% / 2.49 / 57 | 6.2% / 1.74 / 62 |
| 51 | 2.9% / 1.20 / 45 | 0.3% / 0.24 / 38 | 2.8% / 0.80 / 37 | 4.8% / 1.89 / 37 | 2.5% / 0.57 / 45 |
| 52 | 9.8% / 1.84 / 139 | -6.3% / -2.46 / 138 | -3.5% / -0.78 / 153 | 8.1% / 2.11 / 153 | 9.8% / 1.89 / 161 |
| 53 | 13.9% / 2.91 / 60 | -4.7% / -3.54 / 42 | -3.2% / -1.19 / 54 | 0.7% / 0.35 / 50 | 7.5% / 2.10 / 67 |
| 54 | 4.3% / 1.61 / 63 | -0.8% / -0.54 / 56 | -0.1% / 0.01 / 54 | 7.2% / 2.35 / 57 | 5.1% / 1.01 / 62 |
| 55 | 1.9% / 0.92 / 30 | 1.2% / 1.06 / 24 | 4.5% / 1.23 / 27 | 4.2% / 1.77 / 23 | 1.3% / 0.28 / 32 |
| 56 | 13.2% / 2.61 / 94 | -5.8% / -3.20 / 79 | -0.7% / -0.18 / 97 | 2.2% / 0.89 / 89 | 9.1% / 2.12 / 121 |
| 57 | 3.5% / 1.62 / 26 | 1.0% / 1.10 / 19 | -0.4% / -0.15 / 26 | 5.4% / 1.97 / 21 | 2.1% / 0.52 / 26 |
| 58 | 6.3% / 1.52 / 49 | -3.0% / -1.93 / 38 | -1.2% / -0.40 / 46 | 6.3% / 2.13 / 38 | 4.0% / 1.13 / 53 |
| 59 | 6.5% / 1.45 / 153 | -1.6% / -0.76 / 131 | 2.1% / 0.47 / 164 | 1.0% / 0.41 / 144 | 6.3% / 1.56 / 179 |
| 60 | 8.5% / 1.61 / 133 | -5.1% / -2.05 / 139 | 1.8% / 0.37 / 147 | -0.7% / -0.24 / 146 | 15.5% / 2.71 / 165 |
| 61 | 19.4% / 3.52 / 68 | -1.9% / -0.90 / 65 | -0.4% / -0.01 / 74 | 0.8% / 0.27 / 86 | 6.7% / 1.29 / 77 |
| 62 | 8.2% / 1.93 / 46 | -3.3% / -2.26 / 35 | 0.4% / 0.15 / 45 | 3.3% / 1.59 / 42 | 3.4% / 1.11 / 44 |
| 63 | 4.3% / 1.41 / 25 | -0.6% / -0.39 / 29 | 5.3% / 1.50 / 29 | -1.6% / -0.97 / 25 | 3.7% / 1.73 / 15 |
| 64 | 6.7% / 1.50 / 73 | -2.2% / -1.25 / 52 | 1.7% / 0.46 / 66 | 6.2% / 1.98 / 59 | 2.8% / 0.74 / 73 |
| 65 | 0.2% / 0.13 / 26 | 0.4% / 0.35 / 27 | 3.5% / 1.14 / 29 | -0.4% / -0.25 / 31 | 6.3% / 2.65 / 31 |
| 66 | 6.9% / 1.77 / 67 | -0.7% / -0.49 / 61 | 6.9% / 1.51 / 65 | -3.7% / -1.89 / 77 | 4.2% / 1.38 / 76 |
| 67 | 6.7% / 1.15 / 248 | -7.7% / -2.38 / 249 | 2.7% / 0.43 / 251 | 9.0% / 2.00 / 251 | 12.2% / 1.87 / 250 |
| 68 | 0.9% / 0.45 / 67 | -0.6% / -0.41 / 57 | -0.3% / -0.04 / 54 | 4.4% / 2.31 / 65 | 7.6% / 2.42 / 61 |
| 69 | 1.5% / 0.56 / 31 | 0.9% / 0.77 / 23 | 1.9% / 0.52 / 33 | 4.6% / 1.67 / 26 | 3.6% / 0.84 / 29 |
| 70 | 5.0% / 1.05 / 107 | -2.3% / -1.10 / 78 | 3.1% / 0.65 / 105 | 5.6% / 1.47 / 97 | 4.8% / 1.01 / 97 |
| 71 | 8.5% / 2.03 / 46 | -2.2% / -1.52 / 35 | -3.8% / -2.22 / 39 | 3.8% / 1.52 / 43 | 5.2% / 1.53 / 41 |
| 72 | 3.8% / 0.82 / 107 | -2.0% / -0.90 / 78 | 3.0% / 0.59 / 105 | 8.0% / 2.09 / 97 | 6.5% / 1.33 / 97 |
| 73 | -2.0% / -1.34 / 27 | 0.5% / 0.42 / 26 | 0.0% / 0.02 / 33 | 1.2% / 0.90 / 31 | 7.1% / 2.82 / 33 |
| 74 | -2.2% / -1.55 / 47 | -0.9% / -0.65 / 36 | 2.1% / 0.61 / 38 | 4.0% / 2.63 / 42 | 8.2% / 3.28 / 47 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_0bc2` | 2 | 0.91 | 0.85/0.85 | 0.70/0.70 |
| 1 | `cfg_0d42` | 2 | 0.90 | 0.84/0.84 | 0.82/0.82 |
| 2 | `cfg_0f17` | 2 | 0.90 | 0.86/0.86 | 0.56/0.56 |
| 3 | `cfg_1082` | 4 | 0.81 | 0.61/0.68 | 0.30/0.45 |
| 4 | `cfg_112d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 5 | `cfg_5956` | 3 | 0.84 | 0.78/0.82 | 0.46/0.53 |
| 6 | `cfg_6e0d` | 8 | 0.82 | 0.68/0.82 | 0.31/0.51 |
| 7 | `cfg_12ad` | 1 | n/a | n/a/n/a | n/a/n/a |
| 8 | `cfg_dd5a` | 4 | 0.80 | 0.67/0.83 | 0.44/0.53 |
| 9 | `cfg_1708` | 3 | 0.85 | 0.80/0.82 | 0.64/0.69 |
| 10 | `cfg_f7e4` | 2 | 0.85 | 0.79/0.79 | 0.36/0.36 |
| 11 | `cfg_21fa` | 2 | 0.92 | 0.90/0.90 | 0.71/0.71 |
| 12 | `cfg_a474` | 2 | 0.92 | 0.89/0.89 | 0.65/0.65 |
| 13 | `cfg_d2c7` | 4 | 0.83 | 0.88/0.88 | 0.68/0.68 |
| 14 | `cfg_b477` | 2 | 0.88 | 0.84/0.84 | 0.70/0.70 |
| 15 | `cfg_3dcf` | 1 | n/a | n/a/n/a | n/a/n/a |
| 16 | `cfg_a0d4` | 5 | 0.80 | 0.63/0.81 | 0.40/0.57 |
| 17 | `cfg_424e` | 2 | 0.83 | 0.84/0.84 | 0.69/0.69 |
| 18 | `cfg_4874` | 2 | 0.90 | 0.76/0.76 | 0.67/0.67 |
| 19 | `cfg_fbcd` | 3 | 0.85 | 0.79/0.82 | 0.53/0.60 |
| 20 | `cfg_6b57` | 4 | 0.83 | 0.46/0.60 | 0.24/0.39 |
| 21 | `cfg_4f3f` | 1 | n/a | n/a/n/a | n/a/n/a |
| 22 | `cfg_5669` | 2 | 0.87 | 0.86/0.86 | 0.56/0.56 |
| 23 | `cfg_57b4` | 2 | 0.89 | 0.89/0.89 | 0.69/0.69 |
| 24 | `cfg_d42d` | 3 | 0.90 | 0.90/0.90 | 0.56/0.62 |
| 25 | `cfg_6180` | 1 | n/a | n/a/n/a | n/a/n/a |
| 26 | `cfg_64dd` | 6 | 0.80 | 0.62/0.73 | 0.33/0.53 |
| 27 | `cfg_6b90` | 3 | 0.88 | 0.73/0.83 | 0.40/0.65 |
| 28 | `cfg_6c55` | 1 | n/a | n/a/n/a | n/a/n/a |
| 29 | `cfg_74f0` | 1 | n/a | n/a/n/a | n/a/n/a |
| 30 | `cfg_77ef` | 2 | 0.82 | 0.69/0.69 | 0.39/0.39 |
| 31 | `cfg_818a` | 1 | n/a | n/a/n/a | n/a/n/a |
| 32 | `cfg_8b39` | 2 | 0.92 | 0.87/0.87 | 0.68/0.68 |
| 33 | `cfg_8dfb` | 1 | n/a | n/a/n/a | n/a/n/a |
| 34 | `cfg_eb8b` | 3 | 0.89 | 0.87/0.88 | 0.57/0.66 |
| 35 | `cfg_a3e7` | 2 | 0.95 | 0.90/0.90 | 0.70/0.70 |
| 36 | `cfg_eb27` | 3 | 0.81 | 0.71/0.81 | 0.48/0.56 |
| 37 | `cfg_d200` | 2 | 0.87 | 0.74/0.74 | 0.82/0.82 |
| 38 | `cfg_d966` | 2 | 0.95 | 0.92/0.92 | 0.69/0.69 |
| 39 | `cfg_e50f` | 1 | n/a | n/a/n/a | n/a/n/a |
| 40 | `cfg_e831` | 1 | n/a | n/a/n/a | n/a/n/a |
| 41 | `cfg_f052` | 1 | n/a | n/a/n/a | n/a/n/a |
| 42 | `cfg_f1c0` | 2 | 0.95 | 0.95/0.95 | 0.70/0.70 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.843e-03 over 1296 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 193.0, participation ratio 18.3, 95%-variance components 85 (rank bound T = 1290); raw grid 1296; raw + known prior 314424
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
