# Screening funnel -- pc_nq_v5_15m (development stages only)

- Code: `acf4e9adf0bf` (dirty working tree: True, diff sha256 `dd3d18fe260d`)
- Config: `configs/funnel/pc_funnel_nq_v5_15m.yaml` sha256 `0cdb96235beff857`; seed 20261126
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'NQ': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `7628d98c6d203e97` (60 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- NQ 2023-2024 was used to select v3 picks and by the BB/KC, NR-N, mean-reversion and noise-band families; the researcher has read those results. Treated as used for selection.
- Holdout 2025+ previously inspected: **True** -- NQ v3 #32 and #38 were scored on NQ 2025+ (both lost). This run does not open the holdout.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 8640 | 8640 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 8640 | 8640 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 8640 | 8540 | 100 | 0 |  | 8546 | 98.84 | 98.84 |  |
| 3 performance & risk | hard_gate | 8540 | 111 | 8429 | 0 |  | 0 | 1.28 | 1.30 |  |
| 4 parameter stability | hard_gate | 111 | 97 | 14 | 0 |  | 0 | 1.12 | 87.39 |  |
| 5 time stability | hard_gate | 97 | 95 | 2 | 0 |  | 93 | 1.10 | 97.94 |  |
| 6 deduplication | dedup | 95 | 60 |  |  | 35 |  | 0.69 | 63.16 | best 2 per cluster |
| 7 execution stress | hard_gate | 60 | 60 | 0 | 0 |  | 0 | 0.69 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 60 |  |  |  |  |  |  |  | diagnostic only: unverified: 60 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 100 |
| s2:hard_reject:years_with_>=10_trades | 10 |
| s3:hard_reject:max_drawdown | 665 |
| s3:hard_reject:net_return | 5446 |
| s3:hard_reject:sharpe | 8429 |
| s4:hard_reject:local_frac_profitable | 2 |
| s4:hard_reject:local_median_sharpe | 14 |
| s5:hard_reject:profitable_years | 2 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_0fc2` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=2.0, trend_filter=none, regime=none, window=mid | 240/106/61 | 407 | 21.0% | 3.9% | 1.02 | -4.4% | 384 | 1.38 | 9.0% | 205.6 | 6/6 | 1.00 | 0.82 | 0.19 | 3 | 11.1% | 0.47 | 0.48 | 19.4% | 17.3% | 12.5% | 19.4%/15.0% | 7.4 (interpolated) | pass | 0.133 (unverified) | 0.51 |
| 2 | `cfg_c83a` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=3.0, trend_filter=none, regime=none, window=mid | 265/111/29 | 405 | 19.8% | 3.7% | 0.92 | -5.5% | 405 | 1.35 | 9.2% | 204.5 | 6/6 | 1.00 | 0.73 | 0.19 | 4 | 10.3% | 0.48 | 0.51 | 17.6% | 15.6% | 12.5% | 17.0%/12.7% | 7.2 (interpolated) | pass | 0.096 (unverified) | 0.63 |
| 3 | `cfg_7d92` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=long, hold=b16, stop=2.0, trend_filter=none, regime=none, window=mid | 132/405/175 | 712 | 42.5% | 7.3% | 1.00 | -9.0% | 315 | 1.28 | 22.1% | 357.8 | 7/7 | 1.00 | 0.81 | 0.19 | 3 | 15.9% | 0.56 | 0.51 | 37.0% | 32.7% | 47.0% | 37.6%/27.1% | 7.5 (interpolated) | pass | 0.113 (unverified) | 0.83 |
| 4 | `cfg_1e99` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=both, hold=b16, stop=2.0, trend_filter=none, regime=dtrend50, window=mid | 124/392/178 | 694 | 49.0% | 8.3% | 1.09 | -8.0% | 367 | 1.32 | 21.7% | 345.3 | 7/7 | 1.00 | 0.73 | 0.36 | 3 | 17.2% | 0.65 | 0.39 | 45.8% | 42.1% | 73.5% | 44.2%/35.5% | 9.5 (interpolated) | pass | 0.181 (unverified) | 0.33 |
| 5 | `cfg_b7e0` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=long, hold=b16, stop=2.0, trend_filter=none, regime=none, window=mid | 62/309/115 | 486 | 26.5% | 4.8% | 0.85 | -8.8% | 487 | 1.28 | 14.6% | 244.3 | 7/7 | 1.00 | 0.85 | -0.00 | 3 | 6.5% | 0.74 | 0.61 | 24.8% | 21.7% | 24.4% | 23.7%/16.4% | 8.0 (interpolated) | pass | 0.056 (unverified) | 0.25 |
| 6 | `cfg_b19b` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=both, hold=b16, stop=2.0, trend_filter=none, regime=none, window=mid | 247/593/274 | 1114 | 69.9% | 11.2% | 1.12 | -11.8% | 299 | 1.24 | 35.7% | 561.6 | 7/7 | 0.86 | 0.74 | 0.37 | 3 | 24.9% | 0.64 | 0.35 | 63.8% | 58.6% | 65.8% | 59.8%/43.0% | 7.3 (interpolated) | pass | 0.199 (unverified) | 0.84 |
| 7 | `cfg_e672` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=both, hold=b8, stop=2.0, trend_filter=none, regime=none, window=mid | 732/301/204 | 1237 | 58.1% | 9.6% | 1.09 | -8.4% | 309 | 1.22 | 26.6% | 630.6 | 6/6 | 1.00 | 0.89 | 0.20 | 4 | 32.8% | 0.44 | 0.37 | 50.1% | 41.9% | 46.7% | 45.7%/37.9% | 5.9 (interpolated) | pass | 0.172 (unverified) | 0.65 |
| 8 | `cfg_d1db` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=long, hold=b16, stop=3.0, trend_filter=none, regime=none, window=mid | 79/341/62 | 482 | 28.7% | 5.2% | 0.85 | -9.8% | 485 | 1.30 | 15.7% | 241.8 | 7/7 | 1.00 | 0.77 | 0.08 | 4 | 7.9% | 0.70 | 0.64 | 27.2% | 23.8% | 21.1% | 26.1%/20.4% | 8.5 (interpolated) | pass | 0.065 (unverified) | 0.22 |
| 9 | `cfg_d24b` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=long, hold=b16, stop=3.0, trend_filter=none, regime=none, window=mid | 164/447/90 | 701 | 44.1% | 7.6% | 0.98 | -9.4% | 322 | 1.30 | 23.9% | 349.9 | 7/7 | 0.86 | 0.71 | 0.27 | 3 | 18.6% | 0.58 | 0.53 | 39.7% | 35.4% | 47.1% | 39.7%/31.2% | 8.1 (interpolated) | pass | 0.112 (unverified) | 0.76 |
| 10 | `cfg_1c59` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=both, hold=b16, stop=3.0, trend_filter=none, regime=dtrend50, window=mid | 156/445/81 | 682 | 58.5% | 9.7% | 1.18 | -7.8% | 275 | 1.37 | 23.6% | 340.0 | 7/7 | 1.00 | 0.96 | 0.22 | 4 | 26.4% | 0.55 | 0.36 | 55.8% | 52.9% | 66.3% | 53.1%/46.2% | 10.3 (interpolated) | pass | 0.246 (unverified) | -0.06 |
| 11 | `cfg_ca5f` | timeframe=15min, lookback=130, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=long, hold=b8, stop=3.0, trend_filter=none, regime=dtrend50, window=mid | 251/102/36 | 389 | 13.2% | 2.5% | 0.82 | -3.6% | 482 | 1.26 | 8.5% | 191.1 | 6/6 | 1.00 | 0.50 | 0.32 | 5 | 5.2% | 0.60 | 0.40 | 11.9% | 10.6% | 10.9% | 12.4%/8.9% | 5.6 (interpolated) | pass | 0.071 (unverified) | 0.31 |
| 12 | `cfg_1e05` | timeframe=15min, lookback=26, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=3.0, trend_filter=none, regime=none, window=mid | 387/140/48 | 575 | 30.5% | 5.5% | 1.02 | -9.7% | 627 | 1.35 | 12.8% | 287.0 | 7/7 | 0.71 | 0.49 | 0.52 | 4 | 12.3% | 0.60 | 0.39 | 27.5% | 25.5% | 26.2% | 26.5%/21.5% | 7.3 (interpolated) | pass | 0.137 (unverified) | -0.13 |
| 13 | `cfg_9a6d` | timeframe=15min, lookback=130, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=long, hold=b8, stop=2.0, trend_filter=none, regime=dtrend50, window=mid | 221/89/79 | 389 | 12.7% | 2.4% | 0.86 | -3.0% | 296 | 1.26 | 8.0% | 190.1 | 6/6 | 1.00 | 0.56 | 0.30 | 5 | 5.1% | 0.58 | 0.40 | 11.1% | 9.7% | 11.2% | 12.2%/8.8% | 5.5 (interpolated) | pass | 0.075 (unverified) | 0.32 |
| 14 | `cfg_8baa` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=both, hold=b16, stop=2.0, trend_filter=none, regime=none, window=mid | 173/463/203 | 839 | 41.3% | 7.2% | 0.87 | -11.2% | 520 | 1.21 | 27.2% | 424.8 | 7/7 | 1.00 | 0.69 | 0.18 | 4 | 17.0% | 0.59 | 0.51 | 36.2% | 31.8% | 30.7% | 38.9%/29.3% | 6.5 (interpolated) | pass | 0.075 (unverified) | 0.61 |
| 15 | `cfg_5658` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=2.0, trend_filter=none, regime=none, window=all | 273/125/83 | 481 | 23.9% | 4.4% | 0.84 | -5.7% | 490 | 1.32 | 10.2% | 242.8 | 6/6 | 1.00 | 0.56 | 0.28 | 4 | 11.5% | 0.52 | 0.68 | 21.1% | 19.1% | 6.2% | 21.8%/17.4% | 6.7 (interpolated) | pass | 0.050 (unverified) | 0.22 |
| 16 | `cfg_35a6` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=long, hold=b16, stop=2.0, trend_filter=none, regime=none, window=all | 74/280/111 | 465 | 22.9% | 4.2% | 0.75 | -9.4% | 510 | 1.27 | 14.0% | 233.8 | 7/7 | 1.00 | 0.56 | 0.20 | 4 | 8.7% | 0.62 | 0.68 | 20.7% | 19.7% | 7.0% | 21.1%/13.7% | 7.0 (interpolated) | pass | 0.036 (unverified) | 0.17 |
| 17 | `cfg_f525` | timeframe=15min, lookback=26, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=2.0, trend_filter=none, regime=none, window=mid | 348/129/101 | 578 | 32.5% | 5.8% | 1.11 | -5.9% | 501 | 1.37 | 12.2% | 288.4 | 7/7 | 0.71 | 0.27 | 0.84 | 4 | 11.7% | 0.64 | 0.37 | 27.8% | 25.4% | 29.9% | 27.8%/23.4% | 7.6 (interpolated) | pass | 0.185 (unverified) | -0.20 |
| 18 | `cfg_3409` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=both, hold=b16, stop=2.0, trend_filter=none, regime=dtrend50, window=mid | 75/311/128 | 514 | 34.2% | 6.1% | 0.93 | -8.2% | 419 | 1.31 | 16.2% | 254.3 | 7/7 | 1.00 | 0.77 | 0.16 | 3 | 14.7% | 0.57 | 0.54 | 31.4% | 29.2% | 46.6% | 31.6%/24.3% | 9.4 (interpolated) | pass | 0.094 (unverified) | -0.03 |
| 19 | `cfg_3ed2` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=both, hold=b8, stop=2.0, trend_filter=none, regime=none, window=mid | 381/169/95 | 645 | 26.9% | 4.9% | 0.83 | -7.5% | 440 | 1.23 | 14.2% | 326.3 | 6/6 | 0.83 | 0.64 | 0.18 | 3 | 13.0% | 0.52 | 0.61 | 23.7% | 21.0% | 13.0% | 22.8%/17.7% | 6.1 (interpolated) | pass | 0.069 (unverified) | 0.70 |
| 20 | `cfg_f663` | timeframe=15min, lookback=52, signal_form=paper, z_lookback=100, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=3.0, trend_filter=none, regime=volhi, window=all | 121/28/16 | 165 | 24.6% | 4.5% | 0.87 | -4.5% | 188 | 1.58 | 3.6% | 81.3 | 7/7 | 0.86 | 0.42 | 0.45 | 3 | 7.2% | 0.65 | 0.80 | 24.0% | 23.8% | 17.4% | 23.3%/18.1% | 19.6 (interpolated) | pass | 0.051 (unverified) | 0.24 |
| 21 | `cfg_35d4` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=2.0, trend_filter=none, regime=none, window=mid | 335/134/92 | 561 | 21.1% | 3.9% | 0.78 | -5.7% | 326 | 1.25 | 12.2% | 280.0 | 6/6 | 1.00 | 0.70 | 0.08 | 4 | 11.1% | 0.48 | 0.63 | 19.3% | 16.2% | 15.6% | 19.4%/14.3% | 5.8 (interpolated) | pass | 0.060 (unverified) | 0.88 |
| 22 | `cfg_977c` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=both, hold=b16, stop=2.0, trend_filter=none, regime=dtrend50, window=mid | 140/387/174 | 701 | 31.3% | 5.6% | 0.78 | -6.7% | 262 | 1.21 | 21.9% | 348.2 | 7/7 | 1.00 | 0.50 | 0.28 | 3 | 12.2% | 0.61 | 0.52 | 28.0% | 25.4% | 49.6% | 26.2%/17.5% | 7.0 (interpolated) | pass | 0.053 (unverified) | 0.22 |
| 23 | `cfg_e287` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=both, hold=b8, stop=2.0, trend_filter=none, regime=volhi, window=mid | 383/117/88 | 588 | 38.4% | 6.7% | 0.92 | -6.2% | 228 | 1.28 | 12.9% | 291.3 | 6/6 | 1.00 | 0.66 | 0.26 | 5 | 15.7% | 0.52 | 0.51 | 37.1% | 34.5% | 25.6% | 34.4%/24.1% | 9.2 (interpolated) | pass | 0.088 (unverified) | 0.72 |
| 24 | `cfg_35b3` | timeframe=15min, lookback=26, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=3.0, trend_filter=none, regime=none, window=all | 449/191/68 | 708 | 31.5% | 5.6% | 0.86 | -13.8% | 637 | 1.26 | 14.9% | 354.1 | 7/7 | 0.71 | 0.40 | 0.46 | 3 | 10.4% | 0.67 | 0.54 | 29.2% | 25.1% | 17.0% | 28.1%/19.4% | 6.5 (interpolated) | pass | 0.069 (unverified) | -0.60 |
| 25 | `cfg_cde3` | timeframe=15min, lookback=78, signal_form=reversal, z_lookback=100, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=both, hold=session, stop=3.0, trend_filter=none, regime=volhi, window=mid | 0/210/36 | 246 | 35.3% | 6.2% | 0.76 | -7.6% | 301 | 1.38 | 11.5% | 122.9 | 7/7 | 0.71 | 0.05 | 0.71 | 4 | 17.6% | 0.45 | 0.83 | 34.5% | 34.0% | 25.6% | 34.0%/25.3% | 19.0 (interpolated) | pass | 0.036 (unverified) | 0.38 |
| 26 | `cfg_1847` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=both, hold=b8, stop=2.0, trend_filter=none, regime=none, window=mid | 478/222/131 | 831 | 39.9% | 7.0% | 0.97 | -13.4% | 457 | 1.25 | 18.1% | 420.0 | 6/6 | 0.83 | 0.67 | 0.30 | 3 | 18.2% | 0.54 | 0.53 | 35.4% | 28.7% | 28.9% | 34.0%/23.8% | 6.4 (interpolated) | pass | 0.134 (unverified) | 0.53 |
| 27 | `cfg_3b4c` | timeframe=15min, lookback=78, signal_form=reversal, z_lookback=100, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=2.0, trend_filter=none, regime=volhi, window=mid | 94/26/28 | 148 | 20.4% | 3.8% | 0.83 | -3.9% | 218 | 1.61 | 3.2% | 72.2 | 7/7 | 0.86 | 0.23 | 0.60 | 4 | 13.4% | 0.34 | 0.78 | 19.7% | 19.2% | 19.7% | 18.8%/13.2% | 19.0 (interpolated) | pass | 0.045 (unverified) | -0.29 |
| 28 | `cfg_8820` | timeframe=15min, lookback=78, signal_form=reversal, z_lookback=100, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=both, hold=session, stop=3.0, trend_filter=none, regime=volhi, window=mid | 0/184/28 | 212 | 36.9% | 6.5% | 0.82 | -9.4% | 299 | 1.45 | 10.0% | 106.5 | 7/7 | 0.43 | 0.03 | 0.79 | 3 | 17.0% | 0.48 | 0.79 | 36.2% | 35.3% | 31.9% | 35.1%/22.8% | 22.0 (interpolated) | pass | 0.047 (unverified) | 0.38 |
| 29 | `cfg_8f6a` | timeframe=15min, lookback=78, signal_form=reversal, z_lookback=100, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=long, hold=b8, stop=2.0, trend_filter=none, regime=volhi, window=mid | 106/29/33 | 168 | 19.3% | 3.6% | 0.78 | -3.9% | 246 | 1.51 | 3.6% | 82.1 | 7/7 | 0.86 | 0.40 | 0.37 | 4 | 12.7% | 0.31 | 0.83 | 18.7% | 18.1% | 20.3% | 18.9%/14.0% | 16.1 (interpolated) | pass | 0.035 (unverified) | -0.36 |
| 30 | `cfg_67aa` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=both, hold=b16, stop=2.0, trend_filter=none, regime=none, window=mid | 273/570/284 | 1127 | 46.2% | 7.9% | 0.83 | -15.2% | 508 | 1.16 | 36.8% | 566.2 | 7/7 | 1.00 | 0.67 | 0.17 | 4 | 21.3% | 0.54 | 0.54 | 43.0% | 35.3% | 48.3% | 41.1%/28.8% | 5.9 (interpolated) | pass | 0.084 (unverified) | 0.73 |
| 31 | `cfg_6558` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=both, hold=b8, stop=2.0, trend_filter=none, regime=none, window=mid | 547/210/142 | 899 | 34.2% | 6.1% | 0.85 | -9.4% | 299 | 1.20 | 19.5% | 454.0 | 6/6 | 1.00 | 0.57 | 0.28 | 4 | 17.3% | 0.49 | 0.44 | 28.5% | 23.9% | 20.3% | 27.8%/20.2% | 5.2 (interpolated) | pass | 0.073 (unverified) | 0.80 |
| 32 | `cfg_cebf` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=long, hold=b16, stop=2.0, trend_filter=none, regime=none, window=mid | 86/341/123 | 550 | 25.5% | 4.6% | 0.81 | -11.1% | 627 | 1.25 | 17.3% | 276.0 | 7/7 | 1.00 | 0.71 | 0.10 | 3 | 9.2% | 0.64 | 0.62 | 23.3% | 21.0% | 22.2% | 23.3%/17.1% | 7.0 (interpolated) | pass | 0.062 (unverified) | 0.65 |
| 33 | `cfg_b983` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=both, hold=b16, stop=3.0, trend_filter=none, regime=none, window=mid | 213/502/99 | 814 | 38.6% | 6.8% | 0.79 | -9.8% | 479 | 1.19 | 28.8% | 409.8 | 7/7 | 0.86 | 0.53 | 0.26 | 4 | 19.0% | 0.51 | 0.53 | 32.3% | 29.0% | 45.3% | 36.1%/27.3% | 6.4 (interpolated) | pass | 0.056 (unverified) | 0.45 |
| 34 | `cfg_e3ed` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=both, hold=b16, stop=3.0, trend_filter=none, regime=none, window=mid | 343/612/129 | 1084 | 48.0% | 8.2% | 0.82 | -16.6% | 487 | 1.17 | 39.0% | 543.7 | 7/7 | 1.00 | 0.67 | 0.15 | 4 | 19.0% | 0.50 | 0.51 | 40.7% | 36.1% | 46.9% | 44.5%/32.3% | 6.0 (interpolated) | pass | 0.082 (unverified) | 0.35 |
| 35 | `cfg_2483` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=100, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=both, hold=b8, stop=3.0, trend_filter=none, regime=volhi, window=mid | 190/67/18 | 275 | 20.4% | 3.8% | 0.76 | -5.8% | 495 | 1.36 | 6.3% | 136.2 | 6/6 | 1.00 | 0.65 | 0.12 | 3 | 1.8% | 0.86 | 0.63 | 19.4% | 18.4% | 32.6% | 19.0%/14.0% | 11.2 (interpolated) | pass | 0.044 (unverified) | 0.70 |
| 36 | `cfg_d775` | timeframe=15min, lookback=26, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=both, hold=b16, stop=3.0, trend_filter=none, regime=dtrend50, window=mid | 145/294/63 | 502 | 28.4% | 5.1% | 0.76 | -10.3% | 316 | 1.25 | 17.1% | 250.2 | 8/8 | 0.75 | 0.50 | 0.27 | 3 | 7.1% | 0.72 | 0.59 | 23.5% | 22.0% | 26.5% | 25.2%/17.6% | 8.4 (interpolated) | pass | 0.050 (unverified) | -0.08 |
| 37 | `cfg_782d` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=long, hold=b16, stop=3.0, trend_filter=none, regime=none, window=mid | 70/326/53 | 449 | 21.8% | 4.0% | 0.76 | -13.4% | 739 | 1.30 | 14.4% | 221.7 | 7/7 | 1.00 | 0.61 | 0.15 | 3 | 6.8% | 0.69 | 0.55 | 19.8% | 17.5% | 18.4% | 18.9%/12.6% | 6.5 (interpolated) | pass | 0.048 (unverified) | 0.17 |
| 38 | `cfg_9fff` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=both, hold=b8, stop=2.0, trend_filter=none, regime=none, window=all | 573/262/179 | 1014 | 41.8% | 7.2% | 0.85 | -12.1% | 482 | 1.20 | 21.3% | 512.9 | 6/6 | 0.83 | 0.61 | 0.24 | 3 | 15.1% | 0.64 | 0.63 | 35.8% | 29.4% | 17.6% | 35.3%/22.7% | 5.8 (interpolated) | pass | 0.077 (unverified) | 0.17 |
| 39 | `cfg_7483` | timeframe=15min, lookback=26, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=2.0, trend_filter=none, regime=none, window=all | 396/177/141 | 714 | 33.8% | 6.0% | 0.94 | -10.0% | 382 | 1.28 | 14.1% | 358.8 | 7/7 | 0.57 | 0.38 | 0.56 | 4 | 11.3% | 0.67 | 0.51 | 31.3% | 27.3% | 23.4% | 29.2%/23.9% | 6.9 (interpolated) | pass | 0.095 (unverified) | -0.72 |
| 40 | `cfg_2c46` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=both, hold=b16, stop=2.0, trend_filter=none, regime=none, window=mid | 85/390/140 | 615 | 31.4% | 5.6% | 0.81 | -9.4% | 489 | 1.22 | 18.9% | 310.0 | 7/7 | 1.00 | 0.53 | 0.28 | 3 | 14.6% | 0.54 | 0.61 | 26.8% | 24.3% | 14.0% | 27.3%/14.8% | 7.0 (interpolated) | pass | 0.057 (unverified) | 0.26 |
| 41 | `cfg_08bd` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=long, hold=b16, stop=2.0, trend_filter=none, regime=none, window=mid | 61/290/102 | 453 | 20.5% | 3.8% | 0.77 | -10.9% | 616 | 1.28 | 13.5% | 224.3 | 7/7 | 1.00 | 0.52 | 0.25 | 3 | 4.7% | 0.69 | 0.59 | 18.6% | 17.9% | 12.4% | 18.6%/14.2% | 6.6 (interpolated) | pass | 0.047 (unverified) | 0.18 |
| 42 | `cfg_f9d5` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=both, hold=b16, stop=3.0, trend_filter=none, regime=dtrend50, window=mid | 94/351/63 | 508 | 39.8% | 6.9% | 1.01 | -6.3% | 270 | 1.36 | 17.5% | 252.9 | 7/7 | 1.00 | 0.91 | 0.10 | 4 | 23.1% | 0.42 | 0.48 | 37.9% | 36.0% | 43.2% | 36.5%/28.7% | 10.3 (interpolated) | pass | 0.136 (unverified) | -0.33 |
| 43 | `cfg_7736` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=100, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=both, hold=session, stop=3.0, trend_filter=none, regime=volhi, window=mid | 0/217/27 | 244 | 26.6% | 4.8% | 0.84 | -10.8% | 501 | 1.44 | 9.3% | 120.2 | 6/6 | 1.00 | 0.46 | 0.38 | 3 | 6.2% | 0.67 | 0.64 | 26.1% | 24.0% | 33.8% | 24.9%/18.6% | 14.9 (interpolated) | pass | 0.057 (unverified) | 0.35 |
| 44 | `cfg_866b` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=both, hold=b16, stop=2.0, trend_filter=none, regime=none, window=all | 360/624/351 | 1335 | 55.8% | 9.3% | 0.87 | -15.2% | 488 | 1.16 | 41.5% | 670.7 | 7/7 | 0.71 | 0.56 | 0.31 | 3 | 13.7% | 0.75 | 0.48 | 47.9% | 41.2% | 24.9% | 49.1%/33.9% | 5.3 (interpolated) | pass | 0.085 (unverified) | -0.09 |
| 45 | `cfg_bccb` | timeframe=15min, lookback=130, signal_form=paper, z_lookback=100, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=3.0, trend_filter=none, regime=volhi, window=all | 137/28/15 | 180 | 20.5% | 3.8% | 0.80 | -5.6% | 269 | 1.48 | 4.0% | 89.6 | 6/6 | 1.00 | 0.12 | 0.68 | 4 | 6.8% | 0.63 | 0.77 | 19.8% | 19.0% | 9.3% | 19.1%/13.5% | 15.0 (interpolated) | pass | 0.039 (unverified) | -0.07 |
| 46 | `cfg_9fcf` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=both, hold=b16, stop=2.0, trend_filter=none, regime=dtrend50, window=mid | 56/286/96 | 438 | 24.0% | 4.4% | 0.77 | -4.2% | 206 | 1.29 | 13.0% | 217.4 | 7/7 | 1.00 | 0.60 | 0.17 | 4 | 10.3% | 0.52 | 0.70 | 23.2% | 20.7% | 20.5% | 22.0%/15.8% | 8.8 (interpolated) | pass | 0.044 (unverified) | -0.44 |
| 47 | `cfg_69fc` | timeframe=15min, lookback=52, signal_form=paper, z_lookback=100, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=2.0, trend_filter=none, regime=volhi, window=all | 105/27/37 | 169 | 23.0% | 4.2% | 0.82 | -4.3% | 314 | 1.53 | 3.5% | 83.0 | 7/7 | 0.57 | 0.41 | 0.41 | 3 | 10.1% | 0.50 | 0.85 | 21.6% | 21.2% | 18.4% | 20.5%/14.2% | 17.4 (interpolated) | pass | 0.040 (unverified) | 0.36 |
| 48 | `cfg_9c1c` | timeframe=15min, lookback=26, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=both, hold=b8, stop=2.0, trend_filter=none, regime=dtrend50, window=mid | 275/155/99 | 529 | 24.8% | 4.5% | 0.82 | -6.2% | 295 | 1.25 | 10.9% | 265.0 | 7/7 | 0.86 | 0.39 | 0.43 | 3 | 3.9% | 0.81 | 0.52 | 20.7% | 17.1% | 21.0% | 20.2%/14.3% | 6.8 (interpolated) | pass | 0.074 (unverified) | -0.02 |
| 49 | `cfg_075e` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=both, hold=session, stop=2.0, trend_filter=none, regime=volhi, window=mid | 0/388/141 | 529 | 42.2% | 7.3% | 0.85 | -8.6% | 488 | 1.26 | 20.2% | 261.3 | 6/6 | 0.67 | 0.24 | 0.61 | 3 | 9.8% | 0.67 | 0.52 | 39.1% | 35.3% | 31.3% | 30.9%/20.9% | 9.5 (interpolated) | pass | 0.069 (unverified) | 0.68 |
| 50 | `cfg_5107` | timeframe=15min, lookback=26, signal_form=maxgap, z_lookback=100, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=long, hold=session, stop=2.0, trend_filter=none, regime=none, window=mid | 0/173/51 | 224 | 15.4% | 2.9% | 0.84 | -4.0% | 307 | 1.49 | 6.2% | 111.4 | 7/7 | 0.86 | 0.44 | 0.40 | 3 | 6.0% | 0.61 | 0.72 | 14.4% | 13.6% | 9.5% | 14.3%/11.7% | 11.0 (interpolated) | pass | 0.050 (unverified) | 0.31 |
| 51 | `cfg_de84` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=both, hold=b8, stop=3.0, trend_filter=none, regime=none, window=mid | 653/190/62 | 905 | 31.8% | 5.7% | 0.76 | -8.0% | 233 | 1.17 | 20.7% | 457.3 | 6/6 | 1.00 | 0.64 | 0.12 | 4 | 17.9% | 0.41 | 0.51 | 28.6% | 25.7% | 42.4% | 29.3%/23.4% | 5.6 (interpolated) | pass | 0.050 (unverified) | 0.33 |
| 52 | `cfg_73e0` | timeframe=15min, lookback=20, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=both, hold=b8, stop=2.0, trend_filter=none, regime=volhi, window=mid | 409/109/111 | 629 | 34.1% | 6.0% | 0.80 | -7.4% | 239 | 1.21 | 13.7% | 314.1 | 6/6 | 1.00 | 0.69 | 0.11 | 5 | 10.3% | 0.65 | 0.62 | 32.4% | 29.4% | 45.6% | 30.5%/21.2% | 7.9 (interpolated) | pass | 0.076 (unverified) | 0.96 |
| 53 | `cfg_e997` | timeframe=15min, lookback=130, signal_form=paper, z_lookback=100, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=long, hold=session, stop=3.0, trend_filter=none, regime=dtrend50, window=mid | 0/172/32 | 204 | 15.0% | 2.8% | 0.92 | -2.5% | 305 | 1.47 | 8.5% | 99.4 | 6/6 | 0.83 | 0.46 | 0.47 | 4 | 3.0% | 0.80 | 0.50 | 14.1% | 13.5% | 13.6% | 14.2%/11.5% | 11.8 (interpolated) | pass | 0.096 (unverified) | -0.52 |
| 54 | `cfg_97d0` | timeframe=15min, lookback=26, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=both, hold=b8, stop=2.0, trend_filter=none, regime=dtrend50, window=mid | 362/181/115 | 658 | 25.3% | 4.6% | 0.77 | -8.3% | 317 | 1.21 | 13.7% | 328.0 | 7/7 | 0.86 | 0.50 | 0.27 | 4 | 8.9% | 0.65 | 0.54 | 21.8% | 16.4% | 34.3% | 22.6%/16.0% | 6.2 (interpolated) | pass | 0.051 (unverified) | -0.31 |
| 55 | `cfg_8f0d` | timeframe=15min, lookback=78, signal_form=maxgap, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=long, hold=b8, stop=2.0, trend_filter=none, regime=dtrend50, window=all | 245/163/112 | 520 | 15.1% | 2.9% | 0.75 | -7.3% | 502 | 1.22 | 9.7% | 254.8 | 7/7 | 0.86 | 0.59 | 0.16 | 4 | 6.7% | 0.56 | 0.54 | 13.2% | 11.3% | 9.4% | 12.9%/9.3% | 5.1 (interpolated) | pass | 0.042 (unverified) | -0.47 |
| 56 | `cfg_585c` | timeframe=15min, lookback=26, signal_form=paper, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=long, hold=session, stop=2.0, trend_filter=none, regime=none, window=all | 0/562/254 | 816 | 40.9% | 7.1% | 0.80 | -11.4% | 383 | 1.21 | 28.8% | 411.4 | 7/7 | 0.57 | 0.14 | 0.66 | 3 | 10.5% | 0.74 | 0.63 | 31.8% | 28.8% | 30.1% | 35.7%/24.3% | 6.7 (interpolated) | pass | 0.052 (unverified) | -0.48 |
| 57 | `cfg_abed` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=long, hold=b8, stop=2.0, trend_filter=none, regime=volhi, window=mid | 107/49/31 | 187 | 18.1% | 3.4% | 0.81 | -5.6% | 461 | 1.54 | 4.1% | 92.6 | 6/6 | 0.83 | 0.58 | 0.22 | 4 | 6.7% | 0.61 | 0.78 | 17.7% | 16.5% | 13.3% | 16.0%/10.8% | 13.1 (interpolated) | pass | 0.027 (unverified) | 0.03 |
| 58 | `cfg_c4f5` | timeframe=15min, lookback=78, signal_form=reversal, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=3.0, direction=long, hold=b8, stop=3.0, trend_filter=none, regime=dtrend50, window=mid | 235/78/28 | 341 | 14.2% | 2.7% | 0.78 | -3.2% | 333 | 1.31 | 7.6% | 166.8 | 7/7 | 0.71 | 0.50 | 0.28 | 3 | 5.4% | 0.60 | 0.63 | 13.0% | 11.7% | 11.0% | 13.1%/9.9% | 7.4 (interpolated) | pass | 0.046 (unverified) | -0.63 |
| 59 | `cfg_09d1` | timeframe=15min, lookback=26, signal_form=reversal, z_lookback=100, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=long, hold=session, stop=3.0, trend_filter=none, regime=dtrend50, window=mid | 0/92/16 | 108 | 9.9% | 1.9% | 0.80 | -2.9% | 199 | 1.47 | 4.5% | 53.1 | 7/7 | 1.00 | 0.62 | 0.18 | 4 | 6.0% | 0.37 | 0.91 | 9.5% | 9.1% | 10.8% | 9.7%/7.7% | 14.4 (interpolated) | pass | 0.055 (unverified) | 0.30 |
| 60 | `cfg_e1a9` | timeframe=15min, lookback=78, signal_form=reversal, z_lookback=25, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=long, hold=b8, stop=3.0, trend_filter=none, regime=dtrend50, window=mid | 267/90/35 | 392 | 14.6% | 2.8% | 0.76 | -4.4% | 388 | 1.27 | 8.7% | 191.9 | 7/7 | 0.57 | 0.44 | 0.32 | 3 | 2.3% | 0.83 | 0.62 | 13.4% | 11.8% | 16.8% | 14.0%/10.3% | 6.0 (interpolated) | pass | 0.045 (unverified) | -0.60 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 7.1% / 1.42 / 82 | -1.0% / -0.42 / 95 | 5.3% / 1.39 / 85 | -0.5% / -0.23 / 85 | 8.9% / 1.76 / 60 |
| 2 | 6.9% / 1.37 / 82 | 0.2% / 0.09 / 94 | 5.7% / 1.46 / 85 | -2.6% / -0.96 / 84 | 8.6% / 1.57 / 60 |
| 3 | 8.1% / 1.01 / 135 | -3.7% / -0.88 / 151 | 22.9% / 2.11 / 153 | -2.1% / -0.50 / 150 | 13.8% / 1.58 / 123 |
| 4 | 3.5% / 0.55 / 114 | -4.1% / -1.03 / 142 | 18.7% / 1.59 / 164 | -0.5% / -0.07 / 154 | 27.2% / 2.85 / 120 |
| 5 | 5.0% / 0.81 / 99 | -0.6% / -0.21 / 108 | 18.8% / 2.11 / 103 | -6.1% / -2.01 / 105 | 8.7% / 1.42 / 71 |
| 6 | 10.4% / 1.05 / 214 | -5.6% / -1.00 / 224 | 30.1% / 1.91 / 228 | -7.9% / -1.26 / 228 | 36.0% / 2.89 / 220 |
| 7 | 13.4% / 1.46 / 239 | -1.2% / -0.22 / 249 | 16.8% / 1.28 / 246 | 1.4% / 0.27 / 257 | 19.1% / 1.93 / 246 |
| 8 | 3.1% / 0.50 / 99 | 1.7% / 0.59 / 107 | 19.2% / 2.15 / 102 | -8.1% / -2.40 / 103 | 12.1% / 1.61 / 71 |
| 9 | 3.1% / 0.40 / 134 | -3.0% / -0.66 / 150 | 20.1% / 1.89 / 151 | -1.2% / -0.26 / 145 | 21.5% / 2.09 / 121 |
| 10 | 2.8% / 0.43 / 112 | -2.3% / -0.58 / 140 | 25.3% / 2.02 / 161 | 0.5% / 0.11 / 151 | 25.5% / 2.32 / 118 |
| 11 | 1.8% / 0.95 / 54 | 2.1% / 0.97 / 76 | 7.6% / 1.57 / 119 | 0.3% / 0.13 / 95 | 0.8% / 0.31 / 45 |
| 12 | -5.1% / -0.88 / 113 | 0.5% / 0.16 / 115 | 13.0% / 2.05 / 126 | 4.3% / 1.07 / 122 | 16.2% / 2.17 / 99 |
| 13 | 1.0% / 0.55 / 54 | 1.0% / 0.48 / 76 | 7.2% / 1.69 / 119 | 1.2% / 0.42 / 95 | 1.8% / 0.70 / 45 |
| 14 | 8.8% / 1.14 / 164 | -2.0% / -0.42 / 170 | 7.8% / 0.70 / 173 | 1.8% / 0.33 / 171 | 20.8% / 1.97 / 161 |
| 15 | 4.8% / 0.86 / 98 | -2.1% / -0.84 / 111 | 6.9% / 1.18 / 97 | 1.7% / 0.62 / 98 | 11.2% / 1.40 / 77 |
| 16 | 2.8% / 0.45 / 96 | 0.4% / 0.16 / 109 | 6.7% / 1.13 / 94 | -1.3% / -0.37 / 91 | 13.0% / 1.56 / 75 |
| 17 | 0.3% / 0.08 / 115 | -0.1% / -0.03 / 115 | 8.9% / 1.41 / 126 | 2.5% / 0.62 / 123 | 18.6% / 2.52 / 99 |
| 18 | 7.5% / 1.47 / 77 | -1.4% / -0.36 / 108 | 8.3% / 0.82 / 131 | -0.1% / 0.01 / 118 | 16.9% / 2.28 / 80 |
| 19 | 11.0% / 1.80 / 128 | -2.3% / -0.76 / 139 | 7.2% / 0.82 / 131 | -2.9% / -0.91 / 129 | 12.3% / 1.81 / 118 |
| 20 | -0.8% / -0.17 / 29 | -0.3% / -0.12 / 26 | 16.2% / 2.06 / 40 | 0.9% / 0.31 / 34 | 7.4% / 1.05 / 36 |
| 21 | 6.3% / 1.17 / 101 | -2.4% / -0.81 / 121 | 5.7% / 0.94 / 122 | 1.3% / 0.43 / 119 | 9.1% / 1.33 / 98 |
| 22 | 2.2% / 0.41 / 105 | -2.6% / -0.62 / 146 | 14.9% / 1.33 / 164 | -2.0% / -0.39 / 155 | 17.1% / 1.86 / 131 |
| 23 | 1.7% / 0.29 / 109 | 0.9% / 0.26 / 103 | 19.6% / 1.62 / 124 | 0.6% / 0.15 / 140 | 12.0% / 1.54 / 112 |
| 24 | -4.7% / -0.70 / 144 | -2.9% / -0.87 / 143 | 15.3% / 1.81 / 153 | 3.6% / 0.78 / 143 | 19.1% / 2.05 / 125 |
| 25 | 10.5% / 1.42 / 47 | -5.4% / -2.24 / 31 | 15.1% / 1.17 / 55 | 9.7% / 1.64 / 53 | 2.5% / 0.29 / 60 |
| 26 | 11.2% / 1.66 / 166 | -3.5% / -1.03 / 174 | 18.1% / 1.52 / 164 | -6.7% / -1.94 / 175 | 18.4% / 2.22 / 152 |
| 27 | 4.9% / 1.27 / 23 | -0.9% / -0.90 / 16 | 5.4% / 0.78 / 34 | 3.5% / 1.04 / 36 | 6.2% / 1.16 / 39 |
| 28 | 7.2% / 1.09 / 39 | -2.6% / -1.32 / 27 | 17.1% / 1.30 / 50 | 13.7% / 2.31 / 44 | -1.5% / -0.12 / 52 |
| 29 | 5.9% / 1.47 / 28 | -1.8% / -1.52 / 18 | 5.8% / 0.83 / 38 | 3.2% / 0.91 / 42 | 5.0% / 0.94 / 42 |
| 30 | 7.0% / 0.84 / 230 | -1.8% / -0.31 / 219 | 15.4% / 1.09 / 225 | 0.1% / 0.04 / 233 | 20.5% / 1.74 / 220 |
| 31 | 13.1% / 1.77 / 172 | -3.2% / -0.80 / 181 | 3.0% / 0.33 / 186 | 4.0% / 0.84 / 177 | 14.4% / 1.76 / 183 |
| 32 | 4.9% / 0.78 / 99 | -4.2% / -1.21 / 118 | 10.6% / 1.48 / 120 | -1.8% / -0.49 / 117 | 14.9% / 1.92 / 96 |
| 33 | 4.5% / 0.59 / 154 | -1.3% / -0.27 / 166 | 13.1% / 1.10 / 169 | 2.1% / 0.37 / 167 | 16.4% / 1.46 / 158 |
| 34 | 0.1% / 0.06 / 217 | -1.8% / -0.30 / 214 | 24.4% / 1.63 / 218 | 1.9% / 0.29 / 224 | 18.7% / 1.43 / 211 |
| 35 | -1.4% / -0.32 / 47 | -3.0% / -1.20 / 55 | 18.3% / 2.68 / 52 | 4.4% / 1.08 / 67 | 2.0% / 0.33 / 54 |
| 36 | 4.5% / 0.83 / 72 | -1.9% / -0.49 / 106 | 19.9% / 1.94 / 115 | -5.2% / -1.09 / 115 | 10.2% / 1.16 / 94 |
| 37 | -8.6% / -1.62 / 87 | -0.4% / -0.09 / 103 | 12.1% / 1.55 / 99 | 4.5% / 1.42 / 93 | 14.1% / 2.22 / 67 |
| 38 | 12.2% / 1.59 / 194 | -8.0% / -1.99 / 220 | 15.3% / 1.12 / 196 | -3.3% / -0.66 / 212 | 23.2% / 2.13 / 192 |
| 39 | 1.5% / 0.30 / 148 | -2.9% / -0.89 / 143 | 10.3% / 1.25 / 153 | 2.4% / 0.52 / 145 | 20.3% / 2.20 / 125 |
| 40 | 10.9% / 1.42 / 123 | -1.1% / -0.31 / 132 | 12.8% / 1.22 / 123 | -7.4% / -1.99 / 123 | 14.7% / 1.79 / 114 |
| 41 | -5.6% / -1.23 / 87 | -0.7% / -0.20 / 103 | 15.0% / 2.06 / 101 | 1.4% / 0.47 / 95 | 10.1% / 1.69 / 67 |
| 42 | 6.3% / 1.19 / 76 | -0.9% / -0.24 / 107 | 15.7% / 1.46 / 129 | 1.1% / 0.25 / 117 | 13.5% / 1.60 / 79 |
| 43 | -3.6% / -0.83 / 43 | -3.6% / -1.12 / 50 | 19.2% / 2.25 / 48 | 3.1% / 0.74 / 58 | 10.9% / 1.39 / 45 |
| 44 | 7.6% / 0.75 / 265 | -5.7% / -0.85 / 272 | 16.5% / 1.13 / 270 | -3.8% / -0.51 / 266 | 37.1% / 2.44 / 262 |
| 45 | 5.4% / 1.28 / 26 | -4.0% / -1.53 / 27 | 12.8% / 1.64 / 46 | 0.7% / 0.27 / 40 | 4.7% / 0.94 / 41 |
| 46 | -0.6% / -0.10 / 68 | 1.5% / 0.49 / 96 | 12.4% / 1.40 / 100 | 1.2% / 0.37 / 93 | 8.0% / 1.12 / 81 |
| 47 | -0.3% / -0.05 / 30 | -0.8% / -0.36 / 26 | 11.7% / 1.49 / 42 | 2.3% / 0.79 / 35 | 8.8% / 1.27 / 36 |
| 48 | 5.5% / 1.16 / 82 | -5.4% / -1.90 / 104 | 20.1% / 2.31 / 121 | -0.7% / -0.16 / 120 | 4.9% / 0.75 / 102 |
| 49 | 0.8% / 0.14 / 99 | -4.3% / -0.88 / 94 | 29.5% / 1.98 / 111 | -3.8% / -0.61 / 123 | 18.4% / 1.96 / 102 |
| 50 | 2.8% / 0.75 / 42 | -2.7% / -1.56 / 53 | 7.7% / 1.71 / 44 | -1.7% / -0.64 / 53 | 8.9% / 2.13 / 32 |
| 51 | 9.7% / 1.25 / 174 | -0.2% / -0.04 / 186 | 11.8% / 1.10 / 186 | 5.0% / 0.98 / 184 | 2.6% / 0.34 / 175 |
| 52 | 2.4% / 0.38 / 116 | 0.8% / 0.21 / 111 | 21.6% / 1.70 / 134 | 3.4% / 0.60 / 147 | 3.3% / 0.46 / 121 |
| 53 | 2.7% / 1.09 / 30 | 0.9% / 0.39 / 46 | 11.6% / 2.65 / 60 | -0.9% / -0.30 / 47 | 0.3% / 0.13 / 21 |
| 54 | 2.4% / 0.45 / 107 | -6.7% / -2.21 / 123 | 11.8% / 1.45 / 151 | 2.0% / 0.45 / 143 | 15.1% / 1.83 / 134 |
| 55 | 0.0% / 0.03 / 69 | -3.1% / -1.05 / 127 | 6.6% / 1.12 / 145 | 3.2% / 1.01 / 131 | 7.9% / 1.98 / 48 |
| 56 | -4.5% / -0.50 / 165 | 5.6% / 1.00 / 168 | 12.1% / 1.18 / 166 | -2.3% / -0.34 / 168 | 27.5% / 1.97 / 149 |
| 57 | 2.4% / 0.62 / 36 | 0.9% / 0.56 / 33 | 10.7% / 1.49 / 43 | -2.2% / -1.12 / 49 | 5.5% / 1.28 / 26 |
| 58 | -2.6% / -1.20 / 48 | 3.4% / 1.24 / 67 | 8.4% / 1.69 / 95 | -0.9% / -0.31 / 91 | 5.6% / 1.35 / 40 |
| 59 | 1.3% / 0.76 / 14 | 3.7% / 1.84 / 31 | 3.5% / 1.06 / 21 | 3.2% / 1.21 / 28 | -2.0% / -0.93 / 14 |
| 60 | -2.3% / -1.04 / 53 | 3.3% / 1.15 / 76 | 12.0% / 2.27 / 113 | -1.1% / -0.34 / 104 | 2.5% / 0.60 / 46 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_b7e0` | 8 | 0.81 | 0.74/0.89 | 0.63/0.84 |
| 1 | `cfg_b19b` | 5 | 0.82 | 0.80/0.88 | 0.64/0.79 |
| 2 | `cfg_cde3` | 7 | 0.86 | 0.38/0.42 | 0.35/0.49 |
| 3 | `cfg_e287` | 3 | 0.82 | 0.76/0.87 | 0.60/0.77 |
| 4 | `cfg_782d` | 2 | 0.92 | 0.91/0.91 | 0.92/0.92 |
| 5 | `cfg_09d1` | 1 | n/a | n/a/n/a | n/a/n/a |
| 6 | `cfg_0fc2` | 5 | 0.87 | 0.80/0.86 | 0.65/0.68 |
| 7 | `cfg_3b4c` | 4 | 0.89 | 0.88/0.90 | 0.51/0.60 |
| 8 | `cfg_1847` | 2 | 0.89 | 0.83/0.83 | 0.81/0.81 |
| 9 | `cfg_1e99` | 5 | 0.81 | 0.81/0.90 | 0.64/0.86 |
| 10 | `cfg_1e05` | 3 | 0.88 | 0.84/0.90 | 0.74/0.84 |
| 11 | `cfg_2483` | 3 | 0.89 | 0.72/0.75 | 0.63/0.65 |
| 12 | `cfg_3ed2` | 2 | 0.88 | 0.88/0.88 | 0.70/0.70 |
| 13 | `cfg_3409` | 5 | 0.81 | 0.87/0.91 | 0.67/0.87 |
| 14 | `cfg_7d92` | 4 | 0.88 | 0.89/0.92 | 0.83/0.90 |
| 15 | `cfg_5658` | 3 | 0.85 | 0.57/0.72 | 0.41/0.55 |
| 16 | `cfg_35b3` | 4 | 0.90 | 0.86/0.90 | 0.73/0.77 |
| 17 | `cfg_35d4` | 2 | 0.91 | 0.90/0.90 | 0.66/0.66 |
| 18 | `cfg_5107` | 1 | n/a | n/a/n/a | n/a/n/a |
| 19 | `cfg_585c` | 1 | n/a | n/a/n/a | n/a/n/a |
| 20 | `cfg_67aa` | 4 | 0.86 | 0.83/0.91 | 0.82/0.90 |
| 21 | `cfg_6558` | 1 | n/a | n/a/n/a | n/a/n/a |
| 22 | `cfg_f663` | 2 | 0.97 | 0.97/0.97 | 0.92/0.92 |
| 23 | `cfg_73e0` | 1 | n/a | n/a/n/a | n/a/n/a |
| 24 | `cfg_866b` | 1 | n/a | n/a/n/a | n/a/n/a |
| 25 | `cfg_8baa` | 2 | 0.94 | 0.92/0.92 | 0.91/0.91 |
| 26 | `cfg_8f0d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 27 | `cfg_977c` | 1 | n/a | n/a/n/a | n/a/n/a |
| 28 | `cfg_9c1c` | 2 | 0.87 | 0.89/0.89 | 0.78/0.78 |
| 29 | `cfg_ca5f` | 2 | 0.93 | 0.94/0.94 | 0.94/0.94 |
| 30 | `cfg_9fcf` | 1 | n/a | n/a/n/a | n/a/n/a |
| 31 | `cfg_abed` | 1 | n/a | n/a/n/a | n/a/n/a |
| 32 | `cfg_bccb` | 1 | n/a | n/a/n/a | n/a/n/a |
| 33 | `cfg_c4f5` | 2 | 0.94 | 0.94/0.94 | 0.86/0.86 |
| 34 | `cfg_d775` | 1 | n/a | n/a/n/a | n/a/n/a |
| 35 | `cfg_de84` | 1 | n/a | n/a/n/a | n/a/n/a |
| 36 | `cfg_e997` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 8.479e-04 over 8640 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 896.0, participation ratio 50.4, 95%-variance components 325 (rank bound T = 1259); raw grid 8640; raw + known prior 1826388
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

- Signal at bar k from the closes of bars k-N+1..k only (N = lookback, over the RTH bar series across sessions): paper = (midpoint - mean) / midpoint, midpoint = (P1 + PN) / 2 (Gulen & Woeppel's convexity); atr = (midpoint - mean) / ATR(14)[k]; maxgap = the signed line-minus-path gap of largest magnitude / ATR(14)[k]; reversal (control) = (PN - P1) / ATR(14)[k].
- z_k = (S_k - mean(S over the last z_lookback bars, k included)) / population sd of the same; NaN during warm-up.
- Decision at bar k's close: short on a fresh cross z_k >= entry_z (z_{k-1} was not), long on a fresh cross z_k <= -entry_z. A HIGH signal always fades to SHORT. A signal while a position is open is dropped, never queued.
- Filters known at bar k: quadrant late = only against the window's net move PN - P1, early = only with it; |PN - P1| >= min_move_atr x ATR(14)[k]; direction; emaN needs close_k > EMA(N)_k for a long, < for a short; no decision on the session's last bar or less than 30 minutes before its last close.
- Entry fills at the NEXT bar's open with market slippage; the fill bar must be in the decision's session.
- Stop (optional) = open -/+ stop x ATR(14) of the bar before the fill, live intrabar from the entry bar, filled at the worse of the bar's open and the stop with stop slippage. Hold half = ceil(N/2) bars, full = N bars: closed at the close of bar entry + H - 1; session = the session's last close. Every position still open on the session's last bar is closed at that bar's CLOSE; nothing is held overnight.
- Long and short: P&L = side x (exit fill - entry fill) x quantity - commissions; sizing is the mean-reversion funnel's (as many whole contracts as equity covers at full contract value, unlevered, compounding).
- Development backtests run on data physically truncated at the development end; the final session's trade is closed at the last development bar and flagged forced (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC; the 1-minute step there is taken as the roll spread). Point moves are preserved; pre-roll price levels are not real traded prices.
- Session: each root's day session only (src/data/futures.py SESSIONS), on NYSE trading days; overnight Globex bars are not traded or used in indicators.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side (stops too) plus commission per contract per side, from the execution YAML; cost stress scales both.
- Every position is flat by the session close, so no trade straddles a roll. The atr / maxgap / reversal signals are point distances and unaffected by back-adjustment; the paper form divides by a back-adjusted price level, so its scale drifts slightly with the cumulative roll adjustment (the rolling z-score absorbs most of it).

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- The paper tested convexity on DAILY closes with 5- to 21-day holds; every look-back here is intraday, so this whole grid is untested extrapolation of the paper.
- Windows (N up to 96 bars) and the z-score history (250 / 500 bars) run across sessions over RTH bars, so the overnight gap enters the path: a window spanning the open sees the gap as a jump between two adjacent closes.
- The paper form divides by a price level; on a contract whose back-adjusted price nears zero (e.g. CL in April 2020) it is undefined or explodes. The atr form is the same gap without that problem.
- The reversal control has no convex/concave split: its z is extreme almost only in the direction of the net move, so its quadrant=late configs nearly duplicate quadrant=all and its quadrant=early configs trade rarely. They stay in the full factorial (and the raw trial count) so every axis has the same values.
- hold=full equals hold=session whenever N exceeds the bars left in the session (most of N = 48 / 64 / 96 on 15m bars).
- COVID (March-April 2020) falls inside the development period; the paper found the signal much weaker with those months included.
- Sizing ignores the stop distance (full equity per trade, as in the other families), so the ATR stops change the exit, not the position size.
