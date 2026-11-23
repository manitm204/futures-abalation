# Screening funnel -- fv_nq_v1 (development stages only)

- Code: `5e2c41f3de6e` (dirty working tree: True, diff sha256 `e7dc91a3d623`)
- Config: `configs/funnel/fv_funnel_nq_v1.yaml` sha256 `7b012984e34bbe77`; seed 20261128
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ES': '2026-10-16', 'NQ': '2026-10-16'}
- Frozen manifest sha256: `6e03ffe1ea13f3ff` (52 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No FVG strategy has been scored on NQ 2023-2024, but the noise-band, mean-reversion, squeeze, convexity, EMRT, last-half-hour and NY-open sweep families were selected there (the Silver Bullet run loaded it with nothing to score) and the researcher has read those results.
- Holdout 2025+ previously inspected: **True** -- No FVG metrics have been computed on NQ 2025+. Noise-band NQ picks, the month-end #7 transfer check, last-half-hour #49/#56 and NY-open sweep #64/#195 were scored there, so the researcher has seen how that period treated intraday NQ strategies.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 24192 | 24192 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 24192 | 24192 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 24192 | 23436 | 756 | 0 |  | 0 | 96.88 | 96.88 |  |
| 3 performance & risk | hard_gate | 23436 | 86 | 23350 | 0 |  | 0 | 0.36 | 0.37 |  |
| 4 parameter stability | hard_gate | 86 | 83 | 3 | 0 |  | 0 | 0.34 | 96.51 |  |
| 5 time stability | hard_gate | 83 | 83 | 0 | 0 |  | 81 | 0.34 | 100.00 |  |
| 6 deduplication | dedup | 83 | 52 |  |  | 31 |  | 0.21 | 62.65 | best 2 per cluster |
| 7 execution stress | hard_gate | 52 | 52 | 0 | 0 |  | 0 | 0.21 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 52 |  |  |  |  |  |  |  | diagnostic only: unverified: 52 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 756 |
| s2:hard_reject:years_with_>=10_trades | 540 |
| s3:hard_reject:max_drawdown | 47 |
| s3:hard_reject:net_return | 19757 |
| s3:hard_reject:sharpe | 23350 |
| s4:hard_reject:local_median_sharpe | 3 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/stop/target exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_2656` | timeframe=1min, window=pm, mode=against, disp=2.0, fvg_min=0.0, vwap=off, entry=ce, wait=15, stop=a3.0, target=3R, hold=60 | 454/641/115 | 1210 | 24.3% | 4.3% | 1.05 | -4.2% | 495 | 1.22 | 2.6% | 588.0 | 9/9 | 0.78 | 0.59 | 0.46 | 4 | 9.4% | 0.61 | 0.34 | 19.0% | 14.3% | 17.3% | 22.8%/16.3% | 3.7 (interpolated) | pass | 0.002 (unverified) | -0.23 |
| 2 | `cfg_9828` | timeframe=1min, window=am, mode=with, disp=2.0, fvg_min=0.0, vwap=on, entry=mkt, wait=0, stop=a1.5, target=3R, hold=30 | 188/598/199 | 985 | 18.3% | 3.3% | 1.09 | -2.8% | 138 | 1.23 | 0.8% | 480.9 | 9/10 | 1.00 | 0.74 | 0.35 | 5 | 11.2% | 0.39 | 0.29 | 14.2% | 10.0% | 15.1% | 16.6%/13.2% | 3.5 (interpolated) | pass | 0.003 (unverified) | -1.01 |
| 3 | `cfg_3651` | timeframe=1min, window=pm, mode=against, disp=2.0, fvg_min=0.0, vwap=off, entry=ce, wait=15, stop=a3.0, target=2R, hold=60 | 273/632/305 | 1210 | 23.2% | 4.2% | 1.08 | -2.9% | 298 | 1.21 | 2.3% | 587.1 | 9/9 | 0.78 | 0.51 | 0.57 | 4 | 9.3% | 0.60 | 0.27 | 18.5% | 14.3% | 16.4% | 20.7%/16.0% | 3.7 (interpolated) | pass | 0.004 (unverified) | -0.48 |
| 4 | `cfg_6840` | timeframe=1min, window=rth, mode=with, disp=2.0, fvg_min=0.0, vwap=on, entry=mkt, wait=0, stop=a3.0, target=3R, hold=60 | 493/634/128 | 1255 | 30.1% | 5.3% | 0.95 | -4.5% | 365 | 1.18 | 2.8% | 616.1 | 7/8 | 0.71 | 0.79 | 0.16 | 4 | 16.2% | 0.42 | 0.35 | 24.8% | 18.2% | 30.4% | 26.6%/19.8% | 4.1 (interpolated) | pass | 0.001 (unverified) | -0.52 |
| 5 | `cfg_d899` | timeframe=1min, window=rth, mode=with, disp=2.0, fvg_min=0.0, vwap=on, entry=mkt, wait=0, stop=a3.0, target=2R, hold=60 | 328/627/300 | 1255 | 27.6% | 4.9% | 0.94 | -7.1% | 456 | 1.16 | 2.5% | 619.3 | 7/8 | 1.00 | 0.45 | 0.49 | 4 | 14.7% | 0.45 | 0.37 | 22.5% | 16.0% | 27.0% | 25.3%/19.7% | 4.0 (interpolated) | pass | 0.001 (unverified) | -0.62 |
| 6 | `cfg_c48d` | timeframe=1min, window=pm, mode=against, disp=1.5, fvg_min=0.5, vwap=off, entry=ce, wait=30, stop=a3.0, target=1R, hold=60 | 79/553/635 | 1267 | 16.7% | 3.1% | 1.01 | -4.3% | 427 | 1.17 | 1.6% | 616.0 | 7/7 | 0.86 | 0.47 | 0.54 | 4 | 8.8% | 0.47 | 0.24 | 11.7% | 7.6% | 12.9% | 14.8%/11.5% | 3.0 (interpolated) | pass | 0.003 (unverified) | -1.18 |
| 7 | `cfg_1c71` | timeframe=1min, window=pm, mode=against, disp=2.0, fvg_min=0.0, vwap=off, entry=ce, wait=15, stop=a3.0, target=none, hold=60 | 563/647/0 | 1210 | 22.1% | 4.0% | 0.95 | -5.3% | 434 | 1.20 | 2.8% | 589.1 | 8/8 | 0.62 | 0.43 | 0.52 | 3 | 6.8% | 0.69 | 0.37 | 17.1% | 12.0% | 15.4% | 19.2%/15.2% | 3.4 (interpolated) | pass | 0.001 (unverified) | -0.26 |
| 8 | `cfg_7da8` | timeframe=1min, window=am, mode=against, disp=2.0, fvg_min=0.5, vwap=on, entry=prox, wait=15, stop=a3.0, target=1R, hold=60 | 25/120/170 | 315 | 8.6% | 1.6% | 0.90 | -2.4% | 320 | 1.31 | 0.4% | 151.8 | 8/8 | 0.75 | 0.43 | 0.47 | 4 | 5.3% | 0.37 | 0.37 | 7.7% | 6.8% | 7.2% | 7.7%/6.3% | 5.5 (interpolated) | pass | 0.002 (unverified) | -0.53 |
| 9 | `cfg_3400` | timeframe=1min, window=am, mode=with, disp=2.0, fvg_min=0.0, vwap=on, entry=prox, wait=15, stop=struct, target=3R, hold=30 | 318/416/99 | 833 | 16.8% | 3.1% | 0.99 | -3.4% | 391 | 1.22 | 0.9% | 405.7 | 10/10 | 1.00 | 0.64 | 0.35 | 5 | 9.3% | 0.44 | 0.32 | 14.7% | 11.8% | 7.4% | 15.1%/12.1% | 5.1 (interpolated) | pass | 0.002 (unverified) | -0.81 |
| 10 | `cfg_c406` | timeframe=1min, window=am, mode=with, disp=2.0, fvg_min=0.0, vwap=on, entry=mkt, wait=0, stop=a1.5, target=3R, hold=60 | 58/665/262 | 985 | 14.6% | 2.7% | 0.83 | -3.3% | 230 | 1.17 | 1.0% | 479.2 | 8/9 | 0.75 | 0.54 | 0.30 | 4 | 8.0% | 0.45 | 0.39 | 10.9% | 7.4% | 12.1% | 13.6%/9.8% | 3.2 (interpolated) | pass | 0.000 (unverified) | -0.89 |
| 11 | `cfg_fa42` | timeframe=1min, window=am, mode=with, disp=2.0, fvg_min=0.0, vwap=off, entry=mkt, wait=0, stop=a1.5, target=3R, hold=60 | 63/761/297 | 1121 | 15.4% | 2.8% | 0.80 | -3.8% | 239 | 1.15 | 1.1% | 544.4 | 8/9 | 0.75 | 0.48 | 0.32 | 4 | 8.1% | 0.47 | 0.39 | 11.4% | 7.6% | 8.0% | 14.1%/11.0% | 3.2 (interpolated) | pass | 0.000 (unverified) | -0.92 |
| 12 | `cfg_3327` | timeframe=1min, window=am, mode=against, disp=2.0, fvg_min=0.5, vwap=on, entry=prox, wait=5, stop=a3.0, target=1R, hold=60 | 23/112/159 | 294 | 8.3% | 1.6% | 0.90 | -1.8% | 372 | 1.33 | 0.4% | 142.3 | 7/8 | 0.71 | 0.27 | 0.63 | 4 | 5.5% | 0.33 | 0.38 | 7.5% | 6.6% | 5.9% | 7.7%/5.7% | 5.5 (interpolated) | pass | 0.002 (unverified) | -0.45 |
| 13 | `cfg_8397` | timeframe=1min, window=am, mode=with, disp=2.0, fvg_min=0.0, vwap=on, entry=prox, wait=15, stop=struct, target=none, hold=30 | 414/419/0 | 833 | 16.0% | 2.9% | 0.94 | -2.2% | 229 | 1.22 | 1.0% | 404.7 | 9/9 | 1.00 | 0.60 | 0.34 | 5 | 10.2% | 0.34 | 0.38 | 12.9% | 10.7% | 6.5% | 13.8%/10.5% | 4.8 (interpolated) | pass | 0.001 (unverified) | -0.87 |
| 14 | `cfg_27e8` | timeframe=1min, window=am, mode=with, disp=2.0, fvg_min=0.0, vwap=off, entry=mkt, wait=0, stop=a1.5, target=3R, hold=30 | 204/692/225 | 1121 | 17.7% | 3.2% | 0.97 | -3.1% | 142 | 1.19 | 0.9% | 547.2 | 9/10 | 1.00 | 0.68 | 0.29 | 5 | 11.3% | 0.36 | 0.30 | 13.4% | 9.2% | 9.5% | 16.2%/13.5% | 3.3 (interpolated) | pass | 0.001 (unverified) | -1.09 |
| 15 | `cfg_9229` | timeframe=1min, window=am, mode=with, disp=2.0, fvg_min=0.0, vwap=on, entry=prox, wait=15, stop=a1.5, target=none, hold=30 | 317/516/0 | 833 | 14.1% | 2.6% | 0.90 | -2.5% | 186 | 1.22 | 0.8% | 403.4 | 10/10 | 1.00 | 0.58 | 0.32 | 5 | 10.8% | 0.24 | 0.42 | 12.1% | 9.9% | 4.9% | 12.6%/10.2% | 4.4 (interpolated) | pass | 0.001 (unverified) | -0.99 |
| 16 | `cfg_5c35` | timeframe=1min, window=rth, mode=with, disp=2.0, fvg_min=0.0, vwap=on, entry=mkt, wait=0, stop=a3.0, target=2R, hold=30 | 619/469/167 | 1255 | 22.2% | 4.0% | 0.91 | -5.1% | 421 | 1.16 | 1.6% | 618.0 | 8/9 | 1.00 | 0.45 | 0.46 | 4 | 14.6% | 0.33 | 0.35 | 16.6% | 12.0% | 25.1% | 19.8%/15.4% | 3.3 (interpolated) | pass | 0.001 (unverified) | -0.79 |
| 17 | `cfg_89cb` | timeframe=1min, window=rth, mode=with, disp=2.0, fvg_min=0.0, vwap=on, entry=mkt, wait=0, stop=struct, target=3R, hold=30 | 658/509/88 | 1255 | 18.9% | 3.4% | 0.80 | -4.7% | 234 | 1.15 | 1.6% | 614.6 | 8/9 | 1.00 | 0.61 | 0.20 | 5 | 13.1% | 0.28 | 0.40 | 14.2% | 8.7% | 11.2% | 16.8%/12.2% | 2.9 (interpolated) | pass | 0.000 (unverified) | -1.35 |
| 18 | `cfg_591f` | timeframe=1min, window=am, mode=against, disp=2.0, fvg_min=0.0, vwap=on, entry=prox, wait=15, stop=a3.0, target=1R, hold=60 | 36/179/235 | 450 | 10.8% | 2.0% | 0.91 | -2.4% | 402 | 1.26 | 0.6% | 216.3 | 8/8 | 0.62 | 0.51 | 0.40 | 5 | 6.6% | 0.38 | 0.36 | 9.3% | 8.3% | 7.7% | 9.4%/7.7% | 5.1 (interpolated) | pass | 0.002 (unverified) | -0.76 |
| 19 | `cfg_02b5` | timeframe=1min, window=rth, mode=with, disp=2.0, fvg_min=0.5, vwap=on, entry=mkt, wait=0, stop=a3.0, target=3R, hold=60 | 459/630/130 | 1219 | 24.2% | 4.3% | 0.81 | -7.7% | 507 | 1.16 | 2.7% | 595.5 | 7/8 | 0.71 | 0.57 | 0.24 | 4 | 10.3% | 0.52 | 0.44 | 17.3% | 13.9% | 16.2% | 21.0%/14.6% | 3.5 (interpolated) | pass | 0.000 (unverified) | -0.49 |
| 20 | `cfg_3a70` | timeframe=1min, window=am, mode=with, disp=2.0, fvg_min=0.0, vwap=on, entry=mkt, wait=0, stop=struct, target=3R, hold=30 | 538/377/70 | 985 | 20.3% | 3.7% | 0.96 | -2.9% | 193 | 1.20 | 1.3% | 482.8 | 8/9 | 1.00 | 0.60 | 0.36 | 5 | 14.4% | 0.29 | 0.34 | 16.3% | 12.2% | 13.8% | 18.2%/13.3% | 3.8 (interpolated) | pass | 0.001 (unverified) | -1.06 |
| 21 | `cfg_e024` | timeframe=1min, window=am, mode=with, disp=2.0, fvg_min=0.0, vwap=on, entry=prox, wait=15, stop=a1.5, target=3R, hold=60 | 43/564/226 | 833 | 14.7% | 2.7% | 0.91 | -1.9% | 229 | 1.20 | 0.9% | 407.8 | 10/10 | 0.90 | 0.49 | 0.42 | 5 | 10.0% | 0.29 | 0.37 | 12.7% | 10.1% | 7.9% | 13.3%/9.9% | 5.0 (interpolated) | pass | 0.001 (unverified) | -0.73 |
| 22 | `cfg_e3b4` | timeframe=1min, window=rth, mode=against, disp=2.0, fvg_min=0.0, vwap=on, entry=prox, wait=15, stop=a3.0, target=1R, hold=60 | 58/468/550 | 1076 | 17.8% | 3.2% | 1.05 | -3.6% | 397 | 1.19 | 1.3% | 525.5 | 8/8 | 0.62 | 0.48 | 0.57 | 5 | 11.4% | 0.34 | 0.26 | 13.5% | 9.8% | 12.9% | 15.4%/11.7% | 3.6 (interpolated) | pass | 0.006 (unverified) | -0.71 |
| 23 | `cfg_771e` | timeframe=1min, window=am, mode=against, disp=2.0, fvg_min=0.0, vwap=on, entry=mkt, wait=0, stop=a3.0, target=1R, hold=60 | 36/217/273 | 526 | 10.2% | 1.9% | 0.79 | -2.6% | 235 | 1.20 | 0.7% | 254.9 | 6/7 | 0.67 | 0.33 | 0.46 | 4 | 5.6% | 0.45 | 0.37 | 8.7% | 7.1% | 8.8% | 9.3%/6.4% | 4.0 (interpolated) | pass | 0.001 (unverified) | 0.00 |
| 24 | `cfg_094e` | timeframe=1min, window=am, mode=against, disp=2.0, fvg_min=0.0, vwap=on, entry=mkt, wait=0, stop=a3.0, target=none, hold=15 | 418/108/0 | 526 | 9.1% | 1.7% | 0.82 | -3.1% | 369 | 1.26 | 0.4% | 255.4 | 6/7 | 0.67 | 0.53 | 0.29 | 4 | 4.4% | 0.49 | 0.47 | 7.2% | 5.0% | 5.7% | 7.9%/6.0% | 3.3 (interpolated) | pass | 0.001 (unverified) | -0.32 |
| 25 | `cfg_f28a` | timeframe=1min, window=pm, mode=against, disp=2.0, fvg_min=0.0, vwap=off, entry=ce, wait=15, stop=a3.0, target=2R, hold=30 | 574/479/157 | 1210 | 14.3% | 2.6% | 0.82 | -3.6% | 361 | 1.16 | 1.6% | 587.9 | 10/10 | 0.80 | 0.37 | 0.46 | 4 | 4.7% | 0.67 | 0.35 | 10.4% | 5.7% | 7.8% | 12.6%/10.4% | 2.7 (interpolated) | pass | 0.001 (unverified) | -0.95 |
| 26 | `cfg_38dc` | timeframe=1min, window=am, mode=with, disp=2.0, fvg_min=0.0, vwap=on, entry=mkt, wait=0, stop=a3.0, target=3R, hold=30 | 600/346/39 | 985 | 18.2% | 3.3% | 0.84 | -3.2% | 218 | 1.18 | 1.4% | 479.0 | 8/9 | 1.00 | 0.58 | 0.26 | 5 | 11.5% | 0.37 | 0.39 | 14.5% | 10.0% | 19.7% | 16.0%/12.4% | 3.4 (interpolated) | pass | 0.001 (unverified) | -0.61 |
| 27 | `cfg_fb7c` | timeframe=1min, window=am, mode=against, disp=2.0, fvg_min=0.5, vwap=on, entry=mkt, wait=0, stop=a3.0, target=1R, hold=60 | 26/153/205 | 384 | 8.7% | 1.6% | 0.81 | -2.2% | 260 | 1.25 | 0.5% | 185.5 | 6/7 | 0.83 | 0.23 | 0.59 | 4 | 4.9% | 0.42 | 0.38 | 7.4% | 6.2% | 9.8% | 7.9%/5.7% | 4.3 (interpolated) | pass | 0.001 (unverified) | 0.04 |
| 28 | `cfg_7410` | timeframe=1min, window=am, mode=against, disp=2.0, fvg_min=0.0, vwap=on, entry=prox, wait=15, stop=a3.0, target=1R, hold=15 | 231/89/130 | 450 | 7.5% | 1.4% | 0.80 | -2.2% | 341 | 1.26 | 0.3% | 217.7 | 8/8 | 0.62 | 0.65 | 0.15 | 4 | 3.1% | 0.57 | 0.47 | 5.9% | 4.4% | 6.0% | 6.9%/5.0% | 3.5 (interpolated) | pass | 0.001 (unverified) | -0.70 |
| 29 | `cfg_8a67` | timeframe=1min, window=am, mode=against, disp=2.0, fvg_min=0.0, vwap=on, entry=prox, wait=5, stop=a3.0, target=1R, hold=60 | 33/171/222 | 426 | 10.5% | 2.0% | 0.90 | -2.3% | 409 | 1.26 | 0.5% | 205.3 | 7/8 | 0.71 | 0.44 | 0.45 | 5 | 6.3% | 0.39 | 0.36 | 9.3% | 8.2% | 7.5% | 9.3%/7.6% | 5.2 (interpolated) | pass | 0.002 (unverified) | -0.54 |
| 30 | `cfg_693e` | timeframe=1min, window=am, mode=against, disp=2.0, fvg_min=0.0, vwap=on, entry=prox, wait=15, stop=a3.0, target=none, hold=15 | 361/89/0 | 450 | 7.6% | 1.4% | 0.79 | -2.2% | 309 | 1.26 | 0.4% | 217.8 | 8/8 | 0.75 | 0.49 | 0.30 | 4 | 3.7% | 0.50 | 0.51 | 5.9% | 4.3% | 3.9% | 6.9%/5.0% | 3.3 (interpolated) | pass | 0.001 (unverified) | -0.93 |
| 31 | `cfg_a905` | timeframe=1min, window=rth, mode=against, disp=2.0, fvg_min=0.0, vwap=on, entry=prox, wait=15, stop=a3.0, target=1R, hold=15 | 524/237/315 | 1076 | 11.8% | 2.2% | 0.89 | -3.4% | 339 | 1.18 | 0.7% | 521.9 | 8/8 | 0.62 | 0.43 | 0.46 | 4 | 6.5% | 0.43 | 0.35 | 8.2% | 4.2% | 10.8% | 10.5%/8.3% | 2.6 (interpolated) | pass | 0.003 (unverified) | -0.95 |
| 32 | `cfg_57cb` | timeframe=1min, window=rth, mode=with, disp=2.0, fvg_min=0.5, vwap=on, entry=mkt, wait=0, stop=a3.0, target=2R, hold=60 | 302/620/297 | 1219 | 20.6% | 3.7% | 0.76 | -6.2% | 537 | 1.14 | 2.3% | 595.3 | 7/8 | 0.57 | 0.16 | 0.61 | 3 | 8.6% | 0.55 | 0.44 | 14.4% | 10.4% | 14.0% | 17.2%/12.5% | 3.3 (interpolated) | pass | 0.000 (unverified) | -0.53 |
| 33 | `cfg_8b80` | timeframe=1min, window=rth, mode=with, disp=2.0, fvg_min=0.0, vwap=off, entry=mkt, wait=0, stop=struct, target=3R, hold=30 | 650/545/92 | 1287 | 19.2% | 3.5% | 0.80 | -5.0% | 419 | 1.14 | 1.6% | 628.5 | 8/9 | 1.00 | 0.56 | 0.23 | 4 | 12.9% | 0.33 | 0.44 | 14.1% | 8.6% | 12.3% | 17.2%/12.2% | 3.0 (interpolated) | pass | 0.000 (unverified) | -1.19 |
| 34 | `cfg_47ff` | timeframe=1min, window=am, mode=with, disp=2.0, fvg_min=0.0, vwap=off, entry=mkt, wait=0, stop=a1.5, target=none, hold=30 | 424/697/0 | 1121 | 17.0% | 3.1% | 0.87 | -3.3% | 282 | 1.18 | 1.1% | 546.6 | 8/9 | 0.88 | 0.66 | 0.21 | 5 | 10.1% | 0.41 | 0.39 | 12.8% | 8.6% | 10.9% | 15.3%/12.0% | 3.1 (interpolated) | pass | 0.001 (unverified) | -0.99 |
| 35 | `cfg_07a6` | timeframe=1min, window=am, mode=against, disp=2.0, fvg_min=0.0, vwap=on, entry=prox, wait=5, stop=a3.0, target=none, hold=60 | 226/200/0 | 426 | 12.1% | 2.3% | 0.79 | -3.4% | 388 | 1.25 | 1.1% | 204.8 | 7/8 | 0.86 | 0.47 | 0.31 | 5 | 6.2% | 0.46 | 0.49 | 9.8% | 8.9% | 9.9% | 10.3%/7.8% | 4.9 (interpolated) | pass | 0.000 (unverified) | -0.37 |
| 36 | `cfg_21e4` | timeframe=1min, window=am, mode=with, disp=2.0, fvg_min=0.0, vwap=off, entry=mkt, wait=0, stop=struct, target=3R, hold=30 | 578/462/81 | 1121 | 17.4% | 3.2% | 0.79 | -4.2% | 235 | 1.15 | 1.4% | 547.3 | 8/9 | 1.00 | 0.56 | 0.23 | 5 | 11.4% | 0.33 | 0.40 | 13.3% | 8.8% | 10.8% | 15.7%/12.4% | 3.1 (interpolated) | pass | 0.000 (unverified) | -1.11 |
| 37 | `cfg_2aa7` | timeframe=1min, window=am, mode=against, disp=2.0, fvg_min=0.5, vwap=on, entry=mkt, wait=0, stop=a3.0, target=1R, hold=15 | 196/78/110 | 384 | 6.4% | 1.2% | 0.77 | -1.8% | 345 | 1.27 | 0.3% | 186.8 | 6/7 | 0.67 | 0.35 | 0.42 | 5 | 4.1% | 0.35 | 0.50 | 4.9% | 3.6% | 5.9% | 5.7%/3.9% | 3.3 (interpolated) | pass | 0.000 (unverified) | -0.28 |
| 38 | `cfg_5184` | timeframe=1min, window=rth, mode=with, disp=2.0, fvg_min=0.0, vwap=off, entry=mkt, wait=0, stop=a3.0, target=3R, hold=60 | 508/652/127 | 1287 | 26.0% | 4.6% | 0.80 | -4.9% | 351 | 1.15 | 2.9% | 629.2 | 7/8 | 0.86 | 0.60 | 0.20 | 4 | 13.3% | 0.45 | 0.47 | 19.8% | 12.8% | 21.8% | 23.1%/15.6% | 3.6 (interpolated) | pass | 0.000 (unverified) | -0.37 |
| 39 | `cfg_b358` | timeframe=1min, window=am, mode=with, disp=2.0, fvg_min=0.0, vwap=on, entry=prox, wait=15, stop=a1.5, target=3R, hold=30 | 160/512/161 | 833 | 13.8% | 2.6% | 0.94 | -2.1% | 229 | 1.21 | 0.7% | 406.5 | 11/11 | 0.91 | 0.52 | 0.42 | 5 | 9.4% | 0.31 | 0.34 | 11.7% | 9.5% | 5.5% | 12.0%/9.5% | 4.6 (interpolated) | pass | 0.001 (unverified) | -0.72 |
| 40 | `cfg_4934` | timeframe=1min, window=rth, mode=against, disp=2.0, fvg_min=0.0, vwap=on, entry=prox, wait=15, stop=a3.0, target=1R, hold=30 | 225/380/471 | 1076 | 12.7% | 2.4% | 0.81 | -4.1% | 289 | 1.15 | 1.1% | 521.0 | 9/9 | 0.67 | 0.45 | 0.36 | 5 | 6.1% | 0.50 | 0.36 | 9.2% | 6.0% | 8.2% | 11.4%/9.0% | 2.9 (interpolated) | pass | 0.001 (unverified) | -0.75 |
| 41 | `cfg_9f0e` | timeframe=1min, window=am, mode=against, disp=2.0, fvg_min=0.0, vwap=on, entry=mkt, wait=0, stop=a3.0, target=none, hold=60 | 272/254/0 | 526 | 13.3% | 2.5% | 0.78 | -3.6% | 304 | 1.22 | 1.3% | 253.5 | 6/7 | 0.83 | 0.35 | 0.44 | 5 | 9.6% | 0.27 | 0.44 | 10.8% | 9.0% | 6.8% | 11.2%/8.8% | 4.4 (interpolated) | pass | 0.000 (unverified) | 0.09 |
| 42 | `cfg_dbc4` | timeframe=1min, window=rth, mode=against, disp=2.0, fvg_min=0.5, vwap=on, entry=mkt, wait=0, stop=a3.0, target=1R, hold=60 | 48/451/531 | 1030 | 12.2% | 2.3% | 0.77 | -4.4% | 566 | 1.14 | 1.2% | 500.6 | 6/7 | 0.50 | 0.18 | 0.59 | 4 | 4.1% | 0.63 | 0.34 | 9.0% | 5.9% | 6.8% | 11.0%/8.5% | 2.8 (interpolated) | pass | 0.000 (unverified) | -0.41 |
| 43 | `cfg_5c92` | timeframe=1min, window=am, mode=with, disp=1.5, fvg_min=0.0, vwap=off, entry=prox, wait=15, stop=struct, target=3R, hold=30 | 341/756/185 | 1282 | 18.2% | 3.3% | 0.81 | -5.9% | 561 | 1.14 | 1.2% | 625.5 | 10/10 | 0.90 | 0.55 | 0.27 | 4 | 4.8% | 0.74 | 0.44 | 15.3% | 10.4% | 8.0% | 17.3%/12.1% | 4.1 (interpolated) | pass | 0.001 (unverified) | -0.94 |
| 44 | `cfg_8457` | timeframe=1min, window=rth, mode=with, disp=1.5, fvg_min=0.0, vwap=off, entry=prox, wait=15, stop=struct, target=3R, hold=30 | 344/760/186 | 1290 | 18.4% | 3.4% | 0.82 | -5.9% | 561 | 1.15 | 1.2% | 629.2 | 10/10 | 0.90 | 0.45 | 0.37 | 4 | 4.8% | 0.74 | 0.43 | 15.3% | 10.2% | 7.7% | 15.8%/10.6% | 4.0 (interpolated) | pass | 0.001 (unverified) | -0.95 |
| 45 | `cfg_fef0` | timeframe=1min, window=am, mode=with, disp=2.0, fvg_min=0.0, vwap=on, entry=mkt, wait=0, stop=a1.5, target=none, hold=30 | 380/605/0 | 985 | 14.2% | 2.6% | 0.82 | -3.2% | 446 | 1.18 | 1.0% | 480.7 | 8/9 | 0.75 | 0.54 | 0.28 | 5 | 7.8% | 0.45 | 0.46 | 10.7% | 6.8% | 13.1% | 12.5%/9.2% | 2.9 (interpolated) | pass | 0.000 (unverified) | -0.99 |
| 46 | `cfg_2aab` | timeframe=1min, window=am, mode=with, disp=1.5, fvg_min=0.5, vwap=off, entry=ce, wait=30, stop=a3.0, target=2R, hold=60 | 364/559/227 | 1150 | 22.7% | 4.1% | 0.76 | -7.1% | 556 | 1.14 | 2.5% | 561.6 | 8/8 | 0.88 | 0.35 | 0.41 | 4 | 9.4% | 0.58 | 0.35 | 19.5% | 17.1% | 21.4% | 20.5%/14.8% | 5.3 (interpolated) | pass | 0.001 (unverified) | 0.11 |
| 47 | `cfg_8184` | timeframe=1min, window=am, mode=against, disp=2.0, fvg_min=0.5, vwap=on, entry=ce, wait=5, stop=a3.0, target=1R, hold=60 | 15/73/113 | 201 | 5.9% | 1.1% | 0.76 | -1.7% | 397 | 1.34 | 0.3% | 98.6 | 7/8 | 0.86 | 0.29 | 0.46 | 3 | 3.4% | 0.42 | 0.50 | 5.1% | 4.4% | 5.3% | 5.3%/3.6% | 5.6 (interpolated) | pass | 0.000 (unverified) | -0.88 |
| 48 | `cfg_77b6` | timeframe=1min, window=am, mode=with, disp=1.5, fvg_min=0.0, vwap=off, entry=ce, wait=15, stop=struct, target=3R, hold=60 | 66/892/308 | 1266 | 17.7% | 3.2% | 0.82 | -3.9% | 208 | 1.15 | 1.1% | 617.6 | 9/9 | 0.78 | 0.47 | 0.35 | 5 | 8.7% | 0.48 | 0.44 | 15.0% | 11.5% | 8.6% | 16.1%/12.2% | 4.0 (interpolated) | pass | 0.001 (unverified) | -0.81 |
| 49 | `cfg_1864` | timeframe=1min, window=am, mode=with, disp=2.0, fvg_min=0.0, vwap=on, entry=prox, wait=30, stop=a1.5, target=none, hold=30 | 324/530/0 | 854 | 11.9% | 2.2% | 0.76 | -2.9% | 385 | 1.18 | 0.9% | 415.5 | 9/9 | 1.00 | 0.46 | 0.30 | 4 | 7.3% | 0.39 | 0.50 | 9.7% | 7.9% | 2.7% | 10.6%/8.2% | 3.9 (interpolated) | pass | 0.000 (unverified) | -0.75 |
| 50 | `cfg_142f` | timeframe=1min, window=rth, mode=with, disp=1.5, fvg_min=0.0, vwap=off, entry=ce, wait=15, stop=struct, target=3R, hold=60 | 68/908/314 | 1290 | 17.7% | 3.2% | 0.82 | -3.7% | 208 | 1.15 | 1.1% | 629.2 | 9/9 | 0.78 | 0.37 | 0.45 | 5 | 8.8% | 0.47 | 0.44 | 15.0% | 11.1% | 7.6% | 16.1%/11.2% | 3.9 (interpolated) | pass | 0.001 (unverified) | -0.89 |
| 51 | `cfg_168f` | timeframe=1min, window=rth, mode=against, disp=2.0, fvg_min=0.0, vwap=on, entry=prox, wait=5, stop=a3.0, target=1R, hold=15 | 496/231/300 | 1027 | 10.1% | 1.9% | 0.78 | -3.1% | 339 | 1.16 | 0.7% | 497.5 | 7/8 | 0.57 | 0.29 | 0.49 | 4 | 3.8% | 0.60 | 0.41 | 6.6% | 2.9% | 8.8% | 9.2%/6.6% | 2.4 (interpolated) | pass | 0.001 (unverified) | -0.74 |
| 52 | `cfg_77fb` | timeframe=1min, window=am, mode=with, disp=1.5, fvg_min=0.5, vwap=off, entry=ce, wait=15, stop=a3.0, target=2R, hold=60 | 356/550/220 | 1126 | 24.1% | 4.3% | 0.82 | -6.3% | 556 | 1.15 | 2.4% | 554.6 | 9/9 | 0.89 | 0.50 | 0.32 | 4 | 11.9% | 0.51 | 0.34 | 19.7% | 17.1% | 12.0% | 20.0%/14.5% | 5.3 (interpolated) | pass | 0.001 (unverified) | -0.07 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 0.0% / 0.02 / 243 | -1.9% / -0.85 / 239 | 8.0% / 1.36 / 243 | 3.4% / 1.26 / 247 | 13.6% / 2.44 / 238 |
| 2 | 2.5% / 0.85 / 210 | 2.4% / 0.99 / 221 | 3.5% / 1.08 / 181 | 2.3% / 0.88 / 200 | 6.4% / 1.54 / 173 |
| 3 | 2.2% / 0.56 / 243 | -1.6% / -0.76 / 239 | 4.2% / 0.86 / 243 | 4.3% / 1.56 / 247 | 12.7% / 2.45 / 238 |
| 4 | 4.1% / 0.76 / 254 | 2.3% / 0.66 / 257 | 12.0% / 1.64 / 247 | -0.6% / -0.12 / 254 | 9.7% / 1.31 / 243 |
| 5 | 5.7% / 1.09 / 254 | 4.6% / 1.29 / 257 | 11.2% / 1.67 / 247 | -3.7% / -1.01 / 254 | 7.8% / 1.12 / 243 |
| 6 | 4.5% / 1.42 / 252 | 0.7% / 0.37 / 252 | -1.9% / -0.44 / 254 | 5.5% / 2.38 / 255 | 7.2% / 1.93 / 254 |
| 7 | -0.1% / -0.01 / 243 | -2.5% / -1.07 / 239 | 6.3% / 1.11 / 243 | 3.2% / 1.21 / 247 | 14.3% / 2.47 / 238 |
| 8 | 1.9% / 0.99 / 64 | -0.0% / -0.00 / 56 | 3.1% / 1.71 / 57 | 2.8% / 1.55 / 75 | 0.5% / 0.22 / 63 |
| 9 | 1.9% / 0.63 / 178 | 5.1% / 2.12 / 186 | 6.9% / 2.00 / 155 | 0.3% / 0.14 / 168 | 1.6% / 0.41 / 146 |
| 10 | 2.6% / 0.78 / 210 | 3.3% / 1.24 / 221 | 2.8% / 0.79 / 181 | -0.8% / -0.27 / 200 | 6.1% / 1.42 / 173 |
| 11 | 1.4% / 0.41 / 235 | 3.6% / 1.35 / 236 | 3.5% / 0.85 / 220 | -0.6% / -0.21 / 221 | 6.7% / 1.41 / 209 |
| 12 | 2.0% / 1.08 / 59 | -0.5% / -0.42 / 56 | 2.4% / 1.36 / 55 | 2.6% / 1.49 / 70 | 1.4% / 0.65 / 54 |
| 13 | 1.1% / 0.36 / 178 | 5.4% / 2.14 / 186 | 4.9% / 1.56 / 155 | 1.3% / 0.48 / 168 | 2.6% / 0.60 / 146 |
| 14 | 2.0% / 0.62 / 235 | 2.4% / 0.97 / 236 | 4.3% / 1.15 / 220 | 2.1% / 0.76 / 221 | 5.8% / 1.28 / 209 |
| 15 | 2.1% / 0.72 / 178 | 3.2% / 1.44 / 186 | 2.6% / 0.92 / 155 | 2.4% / 0.94 / 168 | 3.0% / 0.76 / 146 |
| 16 | 6.5% / 1.42 / 254 | 4.5% / 1.48 / 257 | 6.6% / 1.24 / 247 | -1.1% / -0.31 / 254 | 4.1% / 0.72 / 243 |
| 17 | 4.4% / 1.03 / 254 | 5.1% / 1.67 / 257 | 3.8% / 0.78 / 247 | 0.7% / 0.21 / 254 | 3.6% / 0.65 / 243 |
| 18 | 3.4% / 1.58 / 90 | 0.5% / 0.39 / 77 | 4.0% / 1.55 / 78 | 0.9% / 0.44 / 102 | 1.6% / 0.54 / 103 |
| 19 | -1.9% / -0.35 / 251 | 1.9% / 0.55 / 254 | 12.6% / 1.75 / 238 | 1.2% / 0.32 / 250 | 9.0% / 1.27 / 226 |
| 20 | 1.8% / 0.50 / 210 | 4.8% / 1.66 / 221 | 5.3% / 1.28 / 181 | 1.8% / 0.53 / 200 | 5.1% / 0.98 / 173 |
| 21 | 4.3% / 1.38 / 178 | 3.8% / 1.58 / 186 | 3.8% / 1.18 / 155 | 0.8% / 0.31 / 168 | 1.3% / 0.35 / 146 |
| 22 | 5.9% / 1.89 / 221 | 0.8% / 0.41 / 204 | 5.7% / 1.46 / 211 | 1.0% / 0.41 / 224 | 3.3% / 0.84 / 216 |
| 23 | -0.7% / -0.26 / 113 | 0.3% / 0.23 / 92 | 4.6% / 1.62 / 93 | 1.3% / 0.62 / 116 | 4.4% / 1.32 / 112 |
| 24 | 0.1% / 0.05 / 113 | -0.8% / -0.69 / 92 | 4.5% / 1.72 / 93 | 1.0% / 0.60 / 116 | 4.1% / 1.43 / 112 |
| 25 | 1.3% / 0.39 / 243 | -1.4% / -0.75 / 239 | 2.7% / 0.65 / 243 | 2.0% / 0.88 / 247 | 9.2% / 2.19 / 238 |
| 26 | 0.5% / 0.16 / 210 | 3.3% / 1.21 / 221 | 4.2% / 1.02 / 181 | 3.0% / 0.81 / 200 | 6.0% / 1.08 / 173 |
| 27 | -0.3% / -0.12 / 85 | 0.8% / 0.64 / 65 | 3.6% / 1.63 / 70 | 2.3% / 1.18 / 92 | 2.1% / 0.81 / 72 |
| 28 | 0.4% / 0.23 / 90 | -0.2% / -0.16 / 77 | 4.2% / 1.94 / 78 | 1.4% / 0.92 / 102 | 1.4% / 0.60 / 103 |
| 29 | 3.6% / 1.67 / 84 | 0.1% / 0.07 / 77 | 4.0% / 1.55 / 78 | 0.8% / 0.40 / 94 | 1.7% / 0.60 / 93 |
| 30 | 1.2% / 0.65 / 90 | -0.3% / -0.29 / 77 | 3.8% / 1.76 / 78 | 1.2% / 0.77 / 102 | 1.5% / 0.61 / 103 |
| 31 | 1.9% / 0.78 / 221 | -0.9% / -0.62 / 204 | 5.0% / 1.46 / 211 | 2.5% / 1.28 / 224 | 2.9% / 0.95 / 216 |
| 32 | -0.1% / -0.01 / 251 | 3.4% / 1.00 / 254 | 11.0% / 1.72 / 238 | -1.8% / -0.48 / 250 | 7.2% / 1.11 / 226 |
| 33 | 2.6% / 0.63 / 257 | 4.7% / 1.54 / 258 | 5.3% / 0.98 / 258 | -0.1% / -0.02 / 258 | 5.5% / 0.96 / 256 |
| 34 | 1.1% / 0.34 / 235 | 1.0% / 0.44 / 236 | 2.5% / 0.64 / 220 | 5.1% / 1.49 / 221 | 6.3% / 1.27 / 209 |
| 35 | 5.5% / 1.67 / 84 | 1.6% / 0.81 / 77 | 0.9% / 0.32 / 78 | 1.9% / 0.68 / 94 | 1.7% / 0.49 / 93 |
| 36 | 1.9% / 0.51 / 235 | 3.6% / 1.25 / 236 | 5.4% / 1.16 / 220 | 1.1% / 0.32 / 221 | 4.2% / 0.79 / 209 |
| 37 | 0.2% / 0.11 / 85 | 0.6% / 0.63 / 65 | 2.3% / 1.25 / 70 | 1.3% / 0.84 / 92 | 2.0% / 0.96 / 72 |
| 38 | 2.6% / 0.50 / 257 | 2.4% / 0.68 / 258 | 11.2% / 1.40 / 258 | -1.3% / -0.27 / 258 | 9.2% / 1.20 / 256 |
| 39 | 3.2% / 1.12 / 178 | 3.6% / 1.62 / 186 | 4.0% / 1.43 / 155 | 0.7% / 0.31 / 168 | 1.6% / 0.45 / 146 |
| 40 | 3.2% / 1.07 / 221 | 0.3% / 0.18 / 204 | 6.2% / 1.61 / 211 | 1.1% / 0.49 / 224 | 1.4% / 0.40 / 216 |
| 41 | 2.3% / 0.68 / 113 | 1.7% / 0.76 / 92 | 2.8% / 0.87 / 93 | 3.3% / 1.08 / 116 | 2.6% / 0.64 / 112 |
| 42 | -1.0% / -0.30 / 220 | 0.4% / 0.22 / 192 | 7.7% / 2.01 / 201 | 2.8% / 1.15 / 214 | 1.9% / 0.53 / 203 |
| 43 | 3.9% / 1.00 / 256 | 0.9% / 0.34 / 257 | 12.9% / 2.23 / 257 | -0.8% / -0.28 / 258 | 0.8% / 0.17 / 254 |
| 44 | 3.9% / 0.99 / 257 | 1.0% / 0.40 / 258 | 13.0% / 2.25 / 259 | -0.8% / -0.28 / 258 | 0.7% / 0.15 / 258 |
| 45 | 1.0% / 0.35 / 210 | 0.9% / 0.40 / 221 | 1.1% / 0.34 / 181 | 4.6% / 1.43 / 200 | 5.9% / 1.35 / 173 |
| 46 | 4.6% / 0.83 / 232 | 2.3% / 0.66 / 229 | -0.8% / -0.09 / 230 | 3.0% / 0.71 / 235 | 12.1% / 1.65 / 224 |
| 47 | -0.3% / -0.19 / 45 | -0.1% / -0.16 / 38 | 1.4% / 0.91 / 39 | 2.5% / 1.90 / 41 | 2.4% / 1.25 / 38 |
| 48 | 0.7% / 0.22 / 252 | 1.4% / 0.55 / 252 | 8.3% / 1.53 / 255 | 2.4% / 0.78 / 256 | 3.9% / 0.79 / 251 |
| 49 | 1.1% / 0.39 / 181 | 3.1% / 1.38 / 190 | 2.9% / 1.01 / 162 | -0.0% / -0.01 / 174 | 4.3% / 1.05 / 147 |
| 50 | 0.5% / 0.16 / 257 | 1.4% / 0.56 / 258 | 8.2% / 1.51 / 259 | 2.4% / 0.77 / 258 | 4.3% / 0.85 / 258 |
| 51 | 1.1% / 0.48 / 208 | -0.7% / -0.49 / 192 | 6.0% / 1.73 / 206 | 1.9% / 0.97 / 213 | 1.5% / 0.52 / 208 |
| 52 | 7.4% / 1.33 / 222 | 3.5% / 1.00 / 226 | 1.1% / 0.20 / 219 | -0.4% / -0.07 / 233 | 10.9% / 1.52 / 226 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_02b5` | 2 | 0.94 | 0.93/0.93 | 0.87/0.87 |
| 1 | `cfg_77b6` | 5 | 0.90 | 0.86/0.94 | 0.68/0.81 |
| 2 | `cfg_e024` | 4 | 0.82 | 0.86/0.92 | 0.73/0.81 |
| 3 | `cfg_07a6` | 3 | 0.86 | 0.82/0.83 | 0.70/0.72 |
| 4 | `cfg_771e` | 3 | 0.82 | 0.73/0.74 | 0.48/0.48 |
| 5 | `cfg_8b80` | 5 | 0.90 | 0.89/0.92 | 0.81/0.86 |
| 6 | `cfg_5c92` | 6 | 0.92 | 0.86/0.91 | 0.71/0.84 |
| 7 | `cfg_a905` | 2 | 0.95 | 0.94/0.94 | 0.81/0.81 |
| 8 | `cfg_9229` | 2 | 0.93 | 0.94/0.94 | 0.90/0.90 |
| 9 | `cfg_591f` | 3 | 0.98 | 0.97/0.98 | 0.89/0.93 |
| 10 | `cfg_2656` | 3 | 0.82 | 0.87/0.91 | 0.80/0.87 |
| 11 | `cfg_5c35` | 4 | 0.84 | 0.90/0.91 | 0.80/0.82 |
| 12 | `cfg_6840` | 3 | 0.88 | 0.93/0.95 | 0.87/0.91 |
| 13 | `cfg_fa42` | 3 | 0.89 | 0.87/0.89 | 0.73/0.77 |
| 14 | `cfg_fb7c` | 2 | 0.86 | 0.80/0.80 | 0.52/0.52 |
| 15 | `cfg_2aab` | 1 | n/a | n/a/n/a | n/a/n/a |
| 16 | `cfg_7da8` | 3 | 0.95 | 0.95/0.97 | 0.87/0.91 |
| 17 | `cfg_3400` | 3 | 0.87 | 0.93/0.94 | 0.89/0.91 |
| 18 | `cfg_3651` | 3 | 0.84 | 0.84/0.85 | 0.66/0.67 |
| 19 | `cfg_3a70` | 6 | 0.86 | 0.93/0.94 | 0.83/0.84 |
| 20 | `cfg_47ff` | 2 | 0.84 | 0.84/0.84 | 0.73/0.73 |
| 21 | `cfg_e3b4` | 3 | 0.92 | 0.93/0.93 | 0.82/0.82 |
| 22 | `cfg_5184` | 1 | n/a | n/a/n/a | n/a/n/a |
| 23 | `cfg_7410` | 4 | 0.93 | 0.93/0.93 | 0.85/0.86 |
| 24 | `cfg_9828` | 3 | 0.84 | 0.90/0.91 | 0.80/0.81 |
| 25 | `cfg_77fb` | 1 | n/a | n/a/n/a | n/a/n/a |
| 26 | `cfg_8184` | 1 | n/a | n/a/n/a | n/a/n/a |
| 27 | `cfg_c48d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 28 | `cfg_dbc4` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.768e-03 over 24192 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1408.0, participation ratio 56.6, 95%-variance components 408 (rank bound T = 1292); raw grid 24192; raw + known prior 363748
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

- Bars: each session's Globex 1-minute bars from 18:00 ET the evening before to 16:00 ET (fv_bars); ATR warms up overnight. Setups and entries are inside the window (am 09:45-12:00, pm 12:00-15:30, rth 09:45-15:30); a position is closed after `hold` minutes or at 16:00.
- ATR = 14-bar simple mean of 1-minute true range (the session's first bar uses high - low), taken at the gap's first bar, i.e. before the displacement. VWAP = volume-weighted typical price of the session's bars from 09:30.
- Gap: three consecutive 1-minute bars of one session (bar 3 opens 2 minutes after bar 1), all opening inside the window, high[1] < low[3] (bullish) or low[1] > high[3] (bearish); size >= fvg_min x ATR and > 0; the middle bar's true range >= disp x ATR. vwap=on: the trade direction must agree with bar 3's close vs VWAP.
- mode=with trades the gap's direction (ICT) with a LIMIT at the near edge or midpoint (1-tick trade-through, filled at the better of the level and the bar's open, no slippage); mode=against trades the opposite way with a STOP order at the same level (a touch, filled at the worse of the level and the bar's open, stop slippage). mkt = market at the open of the bar after bar 3 (within 2 minutes), market slippage. Orders rest `wait` bars inside the window; while one rests later setups are ignored. One trade per session.
- Stop from the entry reference (the level, or the market bar's open): struct = 2 ticks beyond the three bars' extreme on the stop side (wrong side -> skip); aK = K x ATR; at least 1 ATR; live from the fill bar, stop first, filled at the worse of the bar's open and the stop with stop slippage. Target: R x the stop distance, a limit filled at the target only when a bar after the fill bar trades 1 tick through it; a bar touching both is a stop. Otherwise out at the CLOSE of the last bar opening within `hold` minutes of the fill bar (and before 16:00), market slippage.
- Every setup, fill, stop, target and exit is recomputed per config with plain loops (fv_integrity.independent_plan) and must match the backtester exactly.
- Sizing is the other families' (as many whole contracts as equity covers at full contract value, unlevered, compounding).
- Development backtests run on data physically truncated at the development end; a trade still open at the last development bar is closed there and flagged forced (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC). Log returns use back-adjusted prices; the adjustment is constant within a session, so 1-minute returns are distorted only by the level shift (tiny for ES).
- Session: each root's day session only (src/data/futures.py SESSIONS), on NYSE trading days; overnight Globex bars are not traded or used in any statistic.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side plus commission per contract per side, from the execution YAML; cost stress scales both. ES ticks are 0.25 point ($12.50), NQ 0.25 point ($5.00).
- Session: setups and trades 09:45-16:00 ET; overnight Globex bars only warm up ATR. Databento rolls at 00:00 UTC (19:00/20:00 ET), before any trading.

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- ICT never published rules; every definition here (the three-bar gap on 1-minute bars, displacement as the middle bar's true range, the 1-ATR stop floor, the VWAP gate, one trade per session) is one fixed reading of community sources, chosen before the run (reports/ICT strategies to backtest.md). Each such choice is a hidden trial not counted in the grid.
- Entry and target fills assume a resting limit is filled at its price once a bar trades a tick through it; cost stress scales slippage on market and stop fills only, not on limit fills. Queue position is ignored.
- Bars carry no intrabar order: a bar touching both stop and target counts as a stop (stop_first), which understates target-heavy configs.
- Databento ohlcv-1m has no bar for a minute without trades; a gap needs three bars in three consecutive minutes (always true in RTH for NQ/ES).
- The control is built into the grid: mode=against trades every setting the opposite way. No placebo-zone (random gap) benchmark runs inside the funnel.
- Sizing ignores volatility and stop distance (full equity per trade, as in the other families).
