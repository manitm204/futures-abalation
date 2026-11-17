# Screening funnel -- pc_6e_v3_15m (development stages only)

- Code: `a7616723a070` (dirty working tree: True, diff sha256 `85c8df8be5f7`)
- Config: `configs/funnel/pc_funnel_6e_v3_15m.yaml` sha256 `c02463b0f035e3d8`; seed 20261116
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'6J': '2026-10-16', '6E': '2026-10-16'}
- Frozen manifest sha256: `55100b8729817281` (74 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No convexity strategy has been scored on 6E 2023-2024, but BB/KC squeeze and mean-reversion strategies were selected there and the researcher has read those results. Treated as used for selection.
- Holdout 2025+ previously inspected: **False** -- No convexity metrics have been computed on 6E 2025+. Convexity picks were scored on ES and NQ 2025+ (all lost), so the researcher has seen how that period treated this line on index futures.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 103680 | 103680 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 103680 | 103680 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 103680 | 79155 | 24525 | 0 |  | 71533 | 76.35 | 76.35 |  |
| 3 performance & risk | hard_gate | 79155 | 223 | 78932 | 0 |  | 0 | 0.22 | 0.28 |  |
| 4 parameter stability | hard_gate | 223 | 201 | 22 | 0 |  | 0 | 0.19 | 90.13 |  |
| 5 time stability | hard_gate | 201 | 198 | 3 | 0 |  | 125 | 0.19 | 98.51 |  |
| 6 deduplication | dedup | 198 | 74 |  |  | 124 |  | 0.07 | 37.37 | best 2 per cluster |
| 7 execution stress | hard_gate | 74 | 74 | 0 | 0 |  | 2 | 0.07 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 74 |  |  |  |  |  |  |  | diagnostic only: unverified: 74 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 24525 |
| s2:hard_reject:years_with_>=10_trades | 21125 |
| s3:hard_reject:max_drawdown | 694 |
| s3:hard_reject:net_return | 70014 |
| s3:hard_reject:sharpe | 78932 |
| s4:hard_reject:local_frac_profitable | 3 |
| s4:hard_reject:local_median_sharpe | 19 |
| s5:hard_reject:profitable_years | 3 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | 6J dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_a9e1` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=short, hold=1.5n, stop=4.0, trend_filter=none | 148/236/19 | 403 | 14.3% | 2.7% | 1.25 | -1.7% | 242 | 1.48 | 21.1% | 167.5 | 9/9 | 1.00 | 0.91 | 0.34 | 5 | 9.3% | 0.32 | 0.39 | 12.0% | 9.3% | 13.8% | 13.4%/10.6% | 3.8 (interpolated) | pass | 0.050 (unverified) | -0.27 |
| 2 | `cfg_2f31` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=short, hold=1.5n, stop=3.0, trend_filter=none | 126/228/51 | 405 | 13.8% | 2.6% | 1.22 | -2.1% | 264 | 1.45 | 20.0% | 168.7 | 9/9 | 1.00 | 0.84 | 0.37 | 5 | 9.4% | 0.30 | 0.40 | 11.2% | 8.4% | 13.2% | 12.3%/10.0% | 3.7 (interpolated) | pass | 0.043 (unverified) | -0.39 |
| 3 | `cfg_a275` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=full, stop=4.0, trend_filter=none | 172/8/9 | 189 | 9.4% | 1.8% | 1.16 | -1.4% | 377 | 1.69 | 7.9% | 78.4 | 10/10 | 1.00 | 0.74 | 0.42 | 4 | 5.7% | 0.38 | 0.44 | 8.1% | 7.0% | 9.8% | 8.5%/7.1% | 5.2 (interpolated) | pass | 0.029 (unverified) | -0.60 |
| 4 | `cfg_a227` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=full, stop=none, trend_filter=none | 180/9/0 | 189 | 9.9% | 1.9% | 1.24 | -1.4% | 370 | 1.75 | 8.1% | 78.4 | 9/9 | 1.00 | 0.80 | 0.44 | 4 | 6.2% | 0.36 | 0.42 | 8.6% | 7.5% | 9.9% | 8.8%/7.0% | 5.4 (interpolated) | pass | 0.043 (unverified) | -0.60 |
| 5 | `cfg_d75d` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 156/32/0 | 188 | 11.2% | 2.1% | 1.18 | -1.5% | 235 | 1.71 | 12.2% | 78.5 | 8/8 | 1.00 | 0.98 | 0.20 | 4 | 7.4% | 0.33 | 0.45 | 10.0% | 8.7% | 11.0% | 10.2%/8.7% | 5.8 (interpolated) | pass | 0.032 (unverified) | -0.37 |
| 6 | `cfg_b51b` | timeframe=15min, lookback=15, signal_form=paper, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=short, hold=1.5n, stop=4.0, trend_filter=none | 174/323/29 | 526 | 14.2% | 2.7% | 1.16 | -2.1% | 367 | 1.37 | 26.4% | 218.1 | 9/9 | 0.89 | 0.89 | 0.26 | 4 | 8.1% | 0.41 | 0.37 | 10.9% | 6.8% | 10.5% | 12.9%/10.8% | 3.1 (interpolated) | pass | 0.038 (unverified) | -0.46 |
| 7 | `cfg_fa80` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=1.5n, stop=4.0, trend_filter=none | 147/29/12 | 188 | 11.1% | 2.1% | 1.19 | -1.4% | 259 | 1.70 | 11.8% | 78.5 | 9/9 | 1.00 | 0.93 | 0.25 | 4 | 7.3% | 0.33 | 0.45 | 9.8% | 8.5% | 11.3% | 10.3%/8.1% | 5.7 (interpolated) | pass | 0.031 (unverified) | -0.49 |
| 8 | `cfg_add8` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=short, hold=full, stop=4.0, trend_filter=none | 263/131/15 | 409 | 11.2% | 2.2% | 1.08 | -2.5% | 262 | 1.40 | 16.6% | 170.0 | 10/10 | 1.00 | 0.64 | 0.44 | 4 | 7.6% | 0.32 | 0.41 | 8.4% | 6.0% | 10.6% | 9.8%/7.7% | 3.2 (interpolated) | pass | 0.026 (unverified) | -0.50 |
| 9 | `cfg_3619` | timeframe=15min, lookback=15, signal_form=paper, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=short, hold=1.5n, stop=3.0, trend_filter=none | 150/311/69 | 530 | 12.6% | 2.4% | 1.03 | -2.6% | 380 | 1.32 | 25.1% | 221.4 | 9/9 | 0.89 | 0.81 | 0.22 | 4 | 7.2% | 0.41 | 0.41 | 9.1% | 5.6% | 10.9% | 11.1%/9.1% | 2.9 (interpolated) | pass | 0.018 (unverified) | -0.62 |
| 10 | `cfg_f60a` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=short, hold=full, stop=none, trend_filter=none | 275/134/0 | 409 | 10.9% | 2.1% | 1.04 | -2.8% | 268 | 1.38 | 16.8% | 169.7 | 9/9 | 1.00 | 0.65 | 0.39 | 4 | 7.2% | 0.32 | 0.42 | 8.1% | 5.7% | 10.1% | 9.9%/7.3% | 3.2 (interpolated) | pass | 0.023 (unverified) | -0.63 |
| 11 | `cfg_5cfe` | timeframe=15min, lookback=5, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=late, min_move_atr=0.0, direction=short, hold=1.5n, stop=2.0, trend_filter=ema50 | 79/4/22 | 105 | 3.7% | 0.7% | 1.00 | -0.8% | 806 | 1.84 | 2.2% | 43.3 | 6/6 | 1.00 | 0.53 | 0.47 | 4 | 0.9% | 0.75 | 0.61 | 3.1% | 2.5% | 3.1% | 3.3%/2.6% | 4.0 (interpolated) | pass | 0.010 (unverified) | -0.42 |
| 12 | `cfg_4798` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=1.5n, stop=4.0, trend_filter=none | 141/30/18 | 189 | 8.7% | 1.7% | 0.93 | -2.4% | 247 | 1.52 | 11.4% | 79.0 | 9/9 | 1.00 | 0.77 | 0.17 | 5 | 5.1% | 0.41 | 0.60 | 7.3% | 5.8% | 9.7% | 7.7%/5.3% | 4.7 (interpolated) | pass | 0.007 (unverified) | -0.47 |
| 13 | `cfg_2881` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=short, hold=1.5n, stop=2.0, trend_filter=none | 105/195/106 | 406 | 11.3% | 2.2% | 1.04 | -2.2% | 259 | 1.37 | 17.8% | 167.8 | 8/8 | 1.00 | 0.64 | 0.41 | 5 | 7.1% | 0.35 | 0.49 | 8.5% | 6.1% | 9.4% | 10.0%/7.6% | 3.3 (interpolated) | pass | 0.015 (unverified) | -0.59 |
| 14 | `cfg_5a0d` | timeframe=15min, lookback=50, signal_form=maxgap, z_lookback=250, entry_z=0.5, quadrant=all, min_move_atr=2.0, direction=short, hold=half, stop=4.0, trend_filter=none | 129/537/59 | 725 | 13.0% | 2.5% | 0.93 | -4.0% | 428 | 1.25 | 32.8% | 300.1 | 8/8 | 0.75 | 0.59 | 0.34 | 3 | 5.4% | 0.58 | 0.42 | 8.1% | 3.5% | 13.2% | 11.6%/9.2% | 2.4 (interpolated) | pass | 0.014 (unverified) | -0.35 |
| 15 | `cfg_a0e4` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=late, min_move_atr=3.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 200/8/0 | 208 | 7.2% | 1.4% | 0.87 | -1.7% | 377 | 1.47 | 9.0% | 85.3 | 7/7 | 0.86 | 0.67 | 0.21 | 4 | 5.1% | 0.28 | 0.57 | 5.7% | 4.6% | 7.1% | 6.3%/5.0% | 3.9 (interpolated) | pass | 0.007 (unverified) | -0.72 |
| 16 | `cfg_5d7d` | timeframe=15min, lookback=15, signal_form=paper, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=short, hold=1.5n, stop=4.0, trend_filter=none | 140/265/22 | 427 | 11.2% | 2.1% | 1.03 | -1.9% | 335 | 1.37 | 21.4% | 178.2 | 8/8 | 0.88 | 0.67 | 0.37 | 4 | 6.1% | 0.44 | 0.46 | 8.2% | 5.3% | 7.6% | 9.9%/8.2% | 3.1 (interpolated) | pass | 0.019 (unverified) | -0.24 |
| 17 | `cfg_3b89` | timeframe=15min, lookback=50, signal_form=maxgap, z_lookback=250, entry_z=0.5, quadrant=all, min_move_atr=2.0, direction=short, hold=full, stop=4.0, trend_filter=none | 0/665/60 | 725 | 12.1% | 2.3% | 0.88 | -4.1% | 482 | 1.24 | 33.2% | 300.1 | 9/9 | 0.78 | 0.65 | 0.22 | 3 | 4.3% | 0.64 | 0.42 | 7.2% | 2.7% | 13.2% | 11.2%/8.8% | 2.3 (interpolated) | pass | 0.012 (unverified) | -0.40 |
| 18 | `cfg_fffc` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 155/33/0 | 188 | 9.3% | 1.8% | 0.95 | -2.2% | 268 | 1.56 | 12.1% | 78.5 | 8/8 | 1.00 | 0.82 | 0.14 | 5 | 5.6% | 0.38 | 0.56 | 8.1% | 6.8% | 9.7% | 8.7%/6.9% | 5.1 (interpolated) | pass | 0.011 (unverified) | -0.27 |
| 19 | `cfg_c45b` | timeframe=15min, lookback=50, signal_form=maxgap, z_lookback=250, entry_z=0.5, quadrant=all, min_move_atr=2.0, direction=short, hold=full, stop=2.0, trend_filter=ema50 | 0/322/82 | 404 | 7.3% | 1.4% | 0.92 | -2.4% | 280 | 1.35 | 14.2% | 168.5 | 8/8 | 0.75 | 0.75 | 0.17 | 4 | 3.9% | 0.46 | 0.54 | 4.8% | 2.4% | 6.8% | 6.9%/5.7% | 2.5 (interpolated) | pass | 0.012 (unverified) | -0.41 |
| 20 | `cfg_de0f` | timeframe=15min, lookback=50, signal_form=maxgap, z_lookback=250, entry_z=0.5, quadrant=all, min_move_atr=2.0, direction=short, hold=1.5n, stop=2.0, trend_filter=ema50 | 0/322/82 | 404 | 7.3% | 1.4% | 0.92 | -2.4% | 280 | 1.35 | 14.2% | 168.5 | 7/7 | 0.71 | 0.65 | 0.27 | 4 | 3.9% | 0.46 | 0.54 | 4.8% | 2.4% | 6.8% | 6.9%/5.4% | 2.5 (interpolated) | pass | 0.012 (unverified) | -0.41 |
| 21 | `cfg_dda5` | timeframe=15min, lookback=15, signal_form=paper, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=short, hold=1.5n, stop=3.0, trend_filter=none | 119/255/53 | 427 | 9.7% | 1.9% | 0.91 | -1.8% | 386 | 1.31 | 20.3% | 178.3 | 8/8 | 0.88 | 0.52 | 0.39 | 4 | 5.3% | 0.44 | 0.51 | 7.0% | 4.4% | 7.9% | 9.0%/6.6% | 2.9 (interpolated) | pass | 0.009 (unverified) | -0.46 |
| 22 | `cfg_623c` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 159/384/0 | 543 | 11.5% | 2.2% | 0.92 | -2.7% | 173 | 1.29 | 27.7% | 225.2 | 8/8 | 1.00 | 0.63 | 0.28 | 5 | 8.3% | 0.27 | 0.45 | 8.0% | 4.7% | 12.2% | 10.0%/8.0% | 2.7 (interpolated) | pass | 0.011 (unverified) | -0.46 |
| 23 | `cfg_cfd9` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 461/43/0 | 504 | 11.2% | 2.1% | 0.96 | -1.6% | 190 | 1.30 | 21.6% | 208.7 | 7/7 | 0.86 | 0.58 | 0.38 | 5 | 7.3% | 0.33 | 0.37 | 7.9% | 4.6% | 10.7% | 10.0%/7.7% | 2.8 (interpolated) | pass | 0.014 (unverified) | -0.39 |
| 24 | `cfg_48c5` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 133/298/0 | 431 | 10.0% | 1.9% | 0.93 | -1.6% | 229 | 1.34 | 22.2% | 179.2 | 7/7 | 0.86 | 0.80 | 0.13 | 5 | 6.6% | 0.32 | 0.49 | 7.2% | 4.4% | 9.6% | 9.0%/7.2% | 2.9 (interpolated) | pass | 0.010 (unverified) | 0.07 |
| 25 | `cfg_5a04` | timeframe=15min, lookback=15, signal_form=paper, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=full, stop=4.0, trend_filter=none | 220/20/17 | 257 | 9.7% | 1.9% | 1.00 | -2.4% | 461 | 1.47 | 10.6% | 108.2 | 10/10 | 1.00 | 0.50 | 0.51 | 3 | 4.0% | 0.58 | 0.49 | 7.6% | 5.8% | 8.9% | 8.9%/6.8% | 4.0 (interpolated) | pass | 0.016 (unverified) | -1.00 |
| 26 | `cfg_602b` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=late, min_move_atr=1.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 325/21/0 | 346 | 10.1% | 2.0% | 0.89 | -3.3% | 242 | 1.35 | 14.8% | 143.1 | 8/8 | 1.00 | 0.75 | 0.14 | 5 | 6.8% | 0.33 | 0.48 | 7.9% | 5.6% | 11.2% | 9.2%/7.1% | 3.4 (interpolated) | pass | 0.009 (unverified) | -1.00 |
| 27 | `cfg_7458` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=1.0, direction=short, hold=full, stop=none, trend_filter=none | 119/19/0 | 138 | 5.9% | 1.2% | 0.82 | -1.0% | 245 | 1.55 | 7.8% | 56.4 | 9/9 | 0.89 | 0.64 | 0.17 | 4 | 2.7% | 0.55 | 0.77 | 5.1% | 4.3% | 6.2% | 5.4%/4.2% | 4.5 (interpolated) | pass | 0.003 (unverified) | -0.45 |
| 28 | `cfg_1133` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=1.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 281/14/0 | 295 | 9.6% | 1.8% | 0.91 | -2.4% | 268 | 1.39 | 12.7% | 122.3 | 8/8 | 0.88 | 0.80 | 0.11 | 5 | 6.4% | 0.32 | 0.50 | 7.4% | 5.4% | 10.4% | 8.4%/6.5% | 3.7 (interpolated) | pass | 0.010 (unverified) | -0.93 |
| 29 | `cfg_9eb7` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=1.5n, stop=3.0, trend_filter=none | 121/27/41 | 189 | 7.8% | 1.5% | 0.86 | -1.8% | 279 | 1.46 | 10.5% | 78.2 | 9/9 | 1.00 | 0.62 | 0.24 | 5 | 4.9% | 0.36 | 0.65 | 6.6% | 5.3% | 8.5% | 6.9%/5.4% | 4.5 (interpolated) | pass | 0.004 (unverified) | -0.53 |
| 30 | `cfg_0a9d` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=1.5n, stop=2.0, trend_filter=none | 105/21/65 | 191 | 8.5% | 1.7% | 0.97 | -1.6% | 148 | 1.51 | 9.4% | 78.6 | 8/8 | 1.00 | 0.54 | 0.43 | 5 | 5.2% | 0.37 | 0.58 | 7.4% | 6.3% | 7.8% | 7.8%/6.5% | 4.8 (interpolated) | pass | 0.007 (unverified) | -0.51 |
| 31 | `cfg_4bf5` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=short, hold=1.5n, stop=4.0, trend_filter=none | 144/364/37 | 545 | 10.0% | 1.9% | 0.82 | -3.3% | 257 | 1.25 | 26.6% | 226.6 | 9/9 | 1.00 | 0.66 | 0.16 | 4 | 6.6% | 0.33 | 0.52 | 6.5% | 3.2% | 11.9% | 9.3%/6.8% | 2.5 (interpolated) | pass | 0.005 (unverified) | -0.44 |
| 32 | `cfg_7190` | timeframe=15min, lookback=15, signal_form=paper, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=full, stop=none, trend_filter=none | 233/22/0 | 255 | 9.3% | 1.8% | 0.97 | -2.5% | 469 | 1.47 | 10.8% | 107.2 | 9/9 | 1.00 | 0.44 | 0.53 | 3 | 4.0% | 0.57 | 0.48 | 7.3% | 5.6% | 9.7% | 8.6%/6.4% | 3.9 (interpolated) | pass | 0.014 (unverified) | -0.88 |
| 33 | `cfg_826c` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 256/11/0 | 267 | 9.8% | 1.9% | 1.01 | -1.7% | 262 | 1.46 | 11.5% | 110.5 | 8/8 | 0.88 | 0.80 | 0.20 | 5 | 6.6% | 0.31 | 0.44 | 8.1% | 6.2% | 10.6% | 8.6%/6.4% | 4.0 (interpolated) | pass | 0.017 (unverified) | -0.90 |
| 34 | `cfg_92a0` | timeframe=15min, lookback=15, signal_form=paper, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=1.0, direction=short, hold=1.5n, stop=4.0, trend_filter=none | 199/371/40 | 610 | 12.2% | 2.3% | 0.89 | -3.0% | 266 | 1.25 | 30.4% | 254.5 | 9/9 | 1.00 | 0.46 | 0.44 | 4 | 7.1% | 0.40 | 0.45 | 7.6% | 4.0% | 8.9% | 11.6%/9.1% | 2.6 (interpolated) | pass | 0.010 (unverified) | -0.64 |
| 35 | `cfg_f351` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=late, min_move_atr=3.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 132/21/0 | 153 | 7.0% | 1.4% | 0.84 | -1.0% | 167 | 1.54 | 9.9% | 63.2 | 7/7 | 1.00 | 0.77 | 0.07 | 5 | 4.0% | 0.43 | 0.70 | 6.1% | 4.9% | 7.7% | 6.4%/4.8% | 4.9 (interpolated) | pass | 0.004 (unverified) | 0.14 |
| 36 | `cfg_8339` | timeframe=15min, lookback=15, signal_form=paper, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=1.0, direction=short, hold=1.5n, stop=3.0, trend_filter=none | 171/359/88 | 618 | 10.8% | 2.1% | 0.81 | -3.3% | 350 | 1.22 | 28.8% | 257.9 | 9/9 | 1.00 | 0.36 | 0.45 | 4 | 5.2% | 0.52 | 0.51 | 6.4% | 2.5% | 9.4% | 9.9%/7.7% | 2.4 (interpolated) | pass | 0.005 (unverified) | -0.86 |
| 37 | `cfg_499e` | timeframe=15min, lookback=5, signal_form=paper, z_lookback=25, entry_z=1.5, quadrant=late, min_move_atr=0.0, direction=short, hold=1.5n, stop=4.0, trend_filter=ema50 | 120/9/3 | 132 | 3.9% | 0.8% | 0.93 | -0.9% | 230 | 1.66 | 3.0% | 54.5 | 7/7 | 1.00 | 0.77 | 0.16 | 5 | 1.7% | 0.57 | 0.56 | 3.3% | 2.5% | 4.0% | 3.7%/3.0% | 3.7 (interpolated) | pass | 0.008 (unverified) | -0.83 |
| 38 | `cfg_e3c7` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 275/11/0 | 286 | 7.7% | 1.5% | 0.77 | -3.4% | 242 | 1.33 | 12.3% | 118.0 | 8/8 | 1.00 | 0.76 | 0.00 | 5 | 5.0% | 0.35 | 0.55 | 5.6% | 3.9% | 8.9% | 6.5%/4.9% | 3.2 (interpolated) | pass | 0.004 (unverified) | -0.92 |
| 39 | `cfg_3851` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=full, stop=none, trend_filter=none | 177/11/0 | 188 | 6.6% | 1.3% | 0.79 | -2.1% | 361 | 1.45 | 8.1% | 77.0 | 9/9 | 1.00 | 0.69 | 0.10 | 5 | 4.6% | 0.31 | 0.65 | 5.4% | 4.4% | 7.8% | 5.9%/4.7% | 4.0 (interpolated) | pass | 0.005 (unverified) | -0.56 |
| 40 | `cfg_93f0` | timeframe=15min, lookback=5, signal_form=paper, z_lookback=25, entry_z=1.5, quadrant=late, min_move_atr=0.0, direction=short, hold=1.5n, stop=2.0, trend_filter=ema50 | 101/8/24 | 133 | 3.8% | 0.8% | 0.92 | -1.0% | 194 | 1.62 | 2.8% | 54.8 | 6/6 | 0.83 | 0.67 | 0.25 | 5 | 2.1% | 0.46 | 0.58 | 3.0% | 2.3% | 3.5% | 3.3%/2.5% | 3.5 (interpolated) | pass | 0.007 (unverified) | -0.88 |
| 41 | `cfg_60a0` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=short, hold=1.5n, stop=4.0, trend_filter=none | 125/209/16 | 350 | 9.0% | 1.7% | 0.88 | -2.1% | 403 | 1.34 | 18.3% | 146.3 | 8/8 | 1.00 | 0.74 | 0.14 | 4 | 4.5% | 0.47 | 0.56 | 6.5% | 4.1% | 8.1% | 7.7%/5.2% | 3.0 (interpolated) | pass | 0.006 (unverified) | -0.03 |
| 42 | `cfg_89c9` | timeframe=15min, lookback=15, signal_form=paper, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=1.5n, stop=4.0, trend_filter=none | 173/63/21 | 257 | 9.9% | 1.9% | 0.96 | -2.6% | 472 | 1.43 | 15.4% | 108.1 | 9/9 | 0.89 | 0.50 | 0.46 | 3 | 4.0% | 0.59 | 0.52 | 8.0% | 5.8% | 8.8% | 8.7%/6.5% | 4.0 (interpolated) | pass | 0.011 (unverified) | -0.69 |
| 43 | `cfg_15ba` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=short, hold=1.5n, stop=4.0, trend_filter=none | 121/286/26 | 433 | 8.5% | 1.6% | 0.80 | -2.4% | 229 | 1.28 | 21.5% | 180.4 | 8/8 | 0.88 | 0.76 | 0.04 | 4 | 4.9% | 0.40 | 0.58 | 5.4% | 3.0% | 8.6% | 7.8%/5.7% | 2.6 (interpolated) | pass | 0.004 (unverified) | 0.19 |
| 44 | `cfg_b331` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=3.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 201/10/0 | 211 | 6.8% | 1.3% | 0.81 | -2.1% | 388 | 1.41 | 9.0% | 87.1 | 7/7 | 0.86 | 0.61 | 0.20 | 4 | 4.1% | 0.40 | 0.59 | 5.5% | 4.2% | 6.5% | 5.9%/4.3% | 3.8 (interpolated) | pass | 0.005 (unverified) | -0.92 |
| 45 | `cfg_0d10` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=late, min_move_atr=1.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 182/50/0 | 232 | 9.3% | 1.8% | 0.85 | -2.1% | 313 | 1.42 | 14.7% | 96.3 | 8/8 | 1.00 | 0.75 | 0.10 | 5 | 6.1% | 0.33 | 0.60 | 8.0% | 6.3% | 10.2% | 8.4%/5.7% | 4.4 (interpolated) | pass | 0.006 (unverified) | -0.34 |
| 46 | `cfg_709b` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=1.0, direction=short, hold=1.5n, stop=2.0, trend_filter=none | 113/219/123 | 455 | 9.9% | 1.9% | 0.87 | -2.4% | 259 | 1.28 | 19.7% | 187.7 | 8/8 | 1.00 | 0.69 | 0.18 | 4 | 6.1% | 0.38 | 0.59 | 7.4% | 4.5% | 7.1% | 8.9%/7.2% | 2.8 (interpolated) | pass | 0.005 (unverified) | -0.47 |
| 47 | `cfg_2352` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=1.5n, stop=3.0, trend_filter=none | 206/7/54 | 267 | 7.7% | 1.5% | 0.80 | -2.2% | 310 | 1.34 | 10.3% | 110.0 | 9/9 | 0.78 | 0.53 | 0.28 | 4 | 4.3% | 0.45 | 0.56 | 5.8% | 4.1% | 9.7% | 6.5%/4.9% | 3.4 (interpolated) | pass | 0.005 (unverified) | -1.18 |
| 48 | `cfg_2f32` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=late, min_move_atr=1.0, direction=short, hold=1.5n, stop=4.0, trend_filter=none | 162/45/26 | 233 | 8.4% | 1.6% | 0.80 | -2.2% | 313 | 1.38 | 13.8% | 96.7 | 9/9 | 1.00 | 0.73 | 0.07 | 5 | 5.6% | 0.33 | 0.65 | 7.1% | 5.4% | 9.7% | 7.9%/5.5% | 4.1 (interpolated) | pass | 0.004 (unverified) | -0.53 |
| 49 | `cfg_d63e` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=2.0, direction=short, hold=1.5n, stop=4.0, trend_filter=none | 466/30/39 | 535 | 11.4% | 2.2% | 0.91 | -2.5% | 213 | 1.27 | 22.3% | 221.9 | 9/9 | 0.89 | 0.70 | 0.21 | 4 | 6.5% | 0.44 | 0.42 | 8.2% | 4.1% | 13.0% | 10.1%/7.6% | 2.7 (interpolated) | pass | 0.010 (unverified) | -0.56 |
| 50 | `cfg_667e` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 407/21/0 | 428 | 8.6% | 1.7% | 0.78 | -2.8% | 290 | 1.26 | 18.5% | 177.7 | 7/7 | 0.86 | 0.70 | 0.08 | 5 | 5.5% | 0.36 | 0.48 | 5.8% | 3.2% | 8.6% | 7.6%/5.6% | 2.6 (interpolated) | pass | 0.005 (unverified) | -0.54 |
| 51 | `cfg_61e6` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=full, stop=2.0, trend_filter=none | 126/4/61 | 191 | 6.6% | 1.3% | 0.84 | -1.8% | 279 | 1.42 | 6.5% | 78.4 | 9/9 | 1.00 | 0.36 | 0.49 | 4 | 3.8% | 0.42 | 0.63 | 5.3% | 4.2% | 5.9% | 5.9%/4.7% | 3.8 (interpolated) | pass | 0.004 (unverified) | -0.75 |
| 52 | `cfg_5877` | timeframe=15min, lookback=15, signal_form=reversal, z_lookback=25, entry_z=1.5, quadrant=all, min_move_atr=0.0, direction=short, hold=full, stop=none, trend_filter=ema50 | 117/295/0 | 412 | 6.0% | 1.2% | 0.84 | -1.0% | 440 | 1.34 | 11.7% | 170.3 | 8/8 | 0.88 | 0.52 | 0.33 | 5 | 3.1% | 0.48 | 0.52 | 3.6% | 1.1% | 5.3% | 5.5%/4.4% | 2.2 (interpolated) | pass | 0.006 (unverified) | -0.56 |
| 53 | `cfg_0796` | timeframe=15min, lookback=20, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=full, stop=none, trend_filter=none | 111/15/0 | 126 | 5.7% | 1.1% | 0.79 | -1.2% | 370 | 1.57 | 7.1% | 51.4 | 9/9 | 0.89 | 0.70 | 0.09 | 4 | 2.5% | 0.56 | 0.81 | 4.8% | 4.1% | 6.3% | 5.3%/3.9% | 4.7 (interpolated) | pass | 0.003 (unverified) | -0.35 |
| 54 | `cfg_8778` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=1.0, direction=short, hold=1.5n, stop=2.0, trend_filter=none | 111/26/74 | 211 | 7.9% | 1.5% | 0.85 | -1.7% | 148 | 1.42 | 10.3% | 86.5 | 8/8 | 1.00 | 0.60 | 0.26 | 5 | 5.3% | 0.33 | 0.68 | 6.7% | 5.1% | 7.2% | 7.1%/4.7% | 4.0 (interpolated) | pass | 0.004 (unverified) | -0.43 |
| 55 | `cfg_f99c` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=late, min_move_atr=1.0, direction=short, hold=full, stop=none, trend_filter=none | 332/15/0 | 347 | 7.9% | 1.5% | 0.80 | -3.0% | 146 | 1.31 | 10.0% | 143.1 | 9/9 | 0.89 | 0.64 | 0.16 | 5 | 4.6% | 0.42 | 0.54 | 5.5% | 3.5% | 8.4% | 7.1%/5.1% | 2.9 (interpolated) | pass | 0.005 (unverified) | -1.36 |
| 56 | `cfg_c03b` | timeframe=15min, lookback=15, signal_form=reversal, z_lookback=25, entry_z=1.0, quadrant=early, min_move_atr=0.0, direction=short, hold=1.5n, stop=4.0, trend_filter=ema50 | 23/206/8 | 237 | 4.7% | 0.9% | 0.80 | -1.4% | 313 | 1.46 | 8.0% | 98.1 | 9/9 | 0.78 | 0.58 | 0.22 | 5 | 3.2% | 0.31 | 0.76 | 3.3% | 2.0% | 3.1% | 4.4%/3.7% | 2.7 (interpolated) | pass | 0.002 (unverified) | -0.24 |
| 57 | `cfg_9d3d` | timeframe=15min, lookback=15, signal_form=paper, z_lookback=250, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 249/487/0 | 736 | 11.7% | 2.2% | 0.79 | -3.1% | 190 | 1.20 | 38.0% | 305.2 | 9/9 | 0.89 | 0.50 | 0.29 | 5 | 7.3% | 0.36 | 0.47 | 6.5% | 2.3% | 11.7% | 10.0%/7.5% | 2.3 (interpolated) | pass | 0.005 (unverified) | -0.80 |
| 58 | `cfg_9464` | timeframe=15min, lookback=15, signal_form=paper, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=2.0, direction=short, hold=1.5n, stop=3.0, trend_filter=none | 149/59/51 | 259 | 8.3% | 1.6% | 0.82 | -2.4% | 413 | 1.35 | 14.2% | 108.4 | 9/9 | 0.89 | 0.49 | 0.32 | 3 | 3.3% | 0.59 | 0.61 | 6.3% | 4.8% | 9.2% | 7.5%/5.4% | 3.7 (interpolated) | pass | 0.004 (unverified) | -0.89 |
| 59 | `cfg_b336` | timeframe=15min, lookback=15, signal_form=paper, z_lookback=250, entry_z=0.75, quadrant=all, min_move_atr=2.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 265/562/0 | 827 | 13.5% | 2.6% | 0.86 | -3.3% | 190 | 1.21 | 42.3% | 342.4 | 9/9 | 0.89 | 0.50 | 0.35 | 5 | 8.1% | 0.37 | 0.41 | 7.7% | 2.6% | 14.3% | 12.5%/10.0% | 2.3 (interpolated) | pass | 0.008 (unverified) | -0.71 |
| 60 | `cfg_5f0d` | timeframe=15min, lookback=5, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=late, min_move_atr=0.0, direction=short, hold=half, stop=2.0, trend_filter=ema50 | 98/0/9 | 107 | 2.6% | 0.5% | 0.96 | -0.6% | 518 | 1.81 | 0.9% | 44.1 | 6/6 | 0.83 | 0.43 | 0.53 | 4 | 0.6% | 0.76 | 0.58 | 2.0% | 1.4% | 1.9% | 2.3%/1.9% | 3.1 (interpolated) | pass | 0.012 (unverified) | -0.53 |
| 61 | `cfg_c240` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=0.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 301/15/0 | 316 | 9.2% | 1.8% | 0.85 | -2.7% | 268 | 1.35 | 13.7% | 131.7 | 7/7 | 1.00 | 0.66 | 0.20 | 4 | 5.5% | 0.39 | 0.52 | 6.9% | 4.8% | 9.6% | 8.3%/5.8% | 3.4 (interpolated) | pass | 0.007 (unverified) | -1.12 |
| 62 | `cfg_5531` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=3.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 134/215/0 | 349 | 8.6% | 1.7% | 0.83 | -2.1% | 401 | 1.32 | 18.7% | 145.5 | 7/7 | 1.00 | 0.78 | 0.04 | 4 | 4.6% | 0.45 | 0.58 | 6.3% | 3.8% | 7.2% | 7.7%/5.7% | 2.9 (interpolated) | pass | 0.005 (unverified) | -0.16 |
| 63 | `cfg_2816` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=short, hold=1.5n, stop=4.0, trend_filter=none | 228/496/63 | 787 | 11.9% | 2.3% | 0.80 | -3.3% | 387 | 1.19 | 39.2% | 324.7 | 10/10 | 0.90 | 0.56 | 0.24 | 5 | 6.2% | 0.45 | 0.45 | 6.3% | 1.8% | 9.0% | 10.7%/8.1% | 2.2 (interpolated) | pass | 0.005 (unverified) | -0.65 |
| 64 | `cfg_2f04` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.0, quadrant=all, min_move_atr=2.0, direction=short, hold=1.5n, stop=3.0, trend_filter=none | 197/470/125 | 792 | 11.0% | 2.1% | 0.76 | -3.3% | 428 | 1.18 | 36.8% | 327.4 | 10/10 | 1.00 | 0.53 | 0.24 | 5 | 7.1% | 0.33 | 0.48 | 5.6% | 1.2% | 6.7% | 10.0%/7.6% | 2.1 (interpolated) | pass | 0.004 (unverified) | -0.66 |
| 65 | `cfg_9880` | timeframe=15min, lookback=15, signal_form=paper, z_lookback=250, entry_z=0.75, quadrant=all, min_move_atr=2.0, direction=short, hold=1.5n, stop=4.0, trend_filter=none | 228/543/68 | 839 | 11.6% | 2.2% | 0.75 | -2.9% | 210 | 1.18 | 40.6% | 347.1 | 10/10 | 0.90 | 0.47 | 0.28 | 5 | 6.2% | 0.44 | 0.48 | 6.0% | 1.1% | 13.5% | 10.8%/7.9% | 2.1 (interpolated) | pass | 0.004 (unverified) | -0.66 |
| 66 | `cfg_960d` | timeframe=15min, lookback=50, signal_form=paper, z_lookback=25, entry_z=0.75, quadrant=early, min_move_atr=3.0, direction=both, hold=half, stop=4.0, trend_filter=ema50 | 25/763/45 | 833 | 9.3% | 1.8% | 0.79 | -3.4% | 441 | 1.21 | 29.5% | 343.3 | 8/8 | 0.75 | 0.57 | 0.22 | 3 | 3.5% | 0.63 | 0.52 | 4.1% | -1.1% | 7.7% | 8.5%/6.9% | 1.9 (interpolated) | pass | 0.007 (unverified) | -0.56 |
| 67 | `cfg_d5aa` | timeframe=15min, lookback=50, signal_form=paper, z_lookback=25, entry_z=0.75, quadrant=all, min_move_atr=3.0, direction=both, hold=half, stop=4.0, trend_filter=ema50 | 25/763/45 | 833 | 9.3% | 1.8% | 0.79 | -3.4% | 441 | 1.21 | 29.5% | 343.3 | 8/8 | 0.75 | 0.57 | 0.22 | 3 | 3.5% | 0.63 | 0.52 | 4.1% | -1.1% | 7.7% | 8.8%/6.5% | 1.9 (interpolated) | pass | 0.007 (unverified) | -0.56 |
| 68 | `cfg_bbfa` | timeframe=15min, lookback=5, signal_form=maxgap, z_lookback=25, entry_z=1.5, quadrant=late, min_move_atr=0.0, direction=short, hold=full, stop=2.0, trend_filter=ema50 | 88/1/16 | 105 | 2.4% | 0.5% | 0.85 | -0.7% | 587 | 1.61 | 1.5% | 43.3 | 7/7 | 0.86 | 0.50 | 0.34 | 3 | 0.5% | 0.80 | 0.68 | 1.8% | 1.1% | 2.2% | 2.1%/1.6% | 2.9 (interpolated) | pass | 0.007 (unverified) | -0.41 |
| 69 | `cfg_5818` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=25, entry_z=0.5, quadrant=late, min_move_atr=0.0, direction=both, hold=1.5n, stop=none, trend_filter=ema50 | 214/215/0 | 429 | 7.3% | 1.4% | 0.80 | -1.8% | 229 | 1.31 | 14.9% | 178.9 | 7/7 | 0.71 | 0.54 | 0.25 | 5 | 4.1% | 0.44 | 0.65 | 4.9% | 2.4% | 5.6% | 6.4%/4.9% | 2.5 (interpolated) | pass | 0.004 (unverified) | -0.32 |
| 70 | `cfg_d8fb` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=all, min_move_atr=1.0, direction=short, hold=1.5n, stop=none, trend_filter=none | 548/42/0 | 590 | 11.7% | 2.2% | 0.86 | -3.3% | 251 | 1.25 | 25.4% | 245.2 | 8/8 | 0.75 | 0.62 | 0.24 | 5 | 7.5% | 0.36 | 0.44 | 7.3% | 3.5% | 13.4% | 9.9%/6.8% | 2.5 (interpolated) | pass | 0.009 (unverified) | -0.59 |
| 71 | `cfg_b6d6` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=250, entry_z=1.0, quadrant=late, min_move_atr=0.0, direction=short, hold=full, stop=none, trend_filter=ema50 | 85/17/0 | 102 | 3.1% | 0.6% | 0.80 | -1.2% | 553 | 1.63 | 2.8% | 42.2 | 9/9 | 0.89 | 0.36 | 0.43 | 4 | 0.9% | 0.70 | 0.79 | 2.6% | 1.9% | 1.8% | 2.8%/2.2% | 3.7 (interpolated) | pass | 0.002 (unverified) | -0.18 |
| 72 | `cfg_8e6f` | timeframe=15min, lookback=15, signal_form=maxgap, z_lookback=250, entry_z=1.5, quadrant=late, min_move_atr=1.0, direction=short, hold=full, stop=2.0, trend_filter=none | 137/6/68 | 211 | 6.3% | 1.2% | 0.76 | -1.9% | 284 | 1.36 | 7.2% | 86.9 | 9/9 | 1.00 | 0.39 | 0.37 | 4 | 3.4% | 0.45 | 0.70 | 5.0% | 3.7% | 5.1% | 5.8%/4.3% | 3.5 (interpolated) | pass | 0.002 (unverified) | -0.70 |
| 73 | `cfg_4ad3` | timeframe=15min, lookback=10, signal_form=paper, z_lookback=25, entry_z=0.75, quadrant=late, min_move_atr=0.0, direction=short, hold=1.5n, stop=none, trend_filter=ema50 | 76/83/0 | 159 | 4.2% | 0.8% | 0.80 | -1.5% | 333 | 1.54 | 5.7% | 65.5 | 8/8 | 0.88 | 0.47 | 0.33 | 4 | 2.6% | 0.39 | 0.69 | 3.4% | 2.4% | 3.9% | 3.7%/2.8% | 3.3 (interpolated) | pass | 0.005 (unverified) | -0.40 |
| 74 | `cfg_05f6` | timeframe=15min, lookback=15, signal_form=reversal, z_lookback=25, entry_z=1.0, quadrant=early, min_move_atr=0.0, direction=short, hold=1.5n, stop=none, trend_filter=ema50 | 26/211/0 | 237 | 4.7% | 0.9% | 0.79 | -1.6% | 313 | 1.46 | 8.3% | 98.1 | 8/8 | 0.75 | 0.36 | 0.43 | 5 | 3.3% | 0.28 | 0.77 | 3.3% | 2.0% | 3.1% | 4.4%/3.3% | 2.7 (interpolated) | pass | 0.002 (unverified) | -0.31 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 4.6% / 2.22 / 84 | 0.3% / 0.18 / 81 | 3.6% / 1.66 / 86 | 3.1% / 2.02 / 76 | 2.1% / 0.66 / 76 |
| 2 | 4.1% / 2.00 / 84 | 0.1% / 0.09 / 81 | 3.1% / 1.38 / 87 | 3.2% / 2.07 / 77 | 2.7% / 0.88 / 76 |
| 3 | 1.9% / 1.52 / 33 | -0.5% / -0.41 / 34 | 3.5% / 2.21 / 53 | 2.5% / 1.86 / 38 | 1.7% / 0.76 / 31 |
| 4 | 2.0% / 1.64 / 33 | -0.3% / -0.26 / 34 | 3.5% / 2.22 / 53 | 2.5% / 1.84 / 38 | 1.9% / 0.87 / 31 |
| 5 | 2.8% / 1.56 / 33 | -0.0% / -0.03 / 34 | 3.5% / 2.16 / 52 | 1.7% / 1.25 / 38 | 2.7% / 1.03 / 31 |
| 6 | 4.5% / 2.24 / 106 | -1.3% / -0.80 / 101 | 5.7% / 2.31 / 118 | 0.9% / 0.52 / 102 | 3.8% / 1.12 / 99 |
| 7 | 3.2% / 1.81 / 33 | -0.2% / -0.17 / 34 | 3.6% / 2.17 / 52 | 1.7% / 1.30 / 38 | 2.5% / 0.94 / 31 |
| 8 | 2.6% / 1.65 / 84 | -0.1% / -0.04 / 82 | 3.5% / 1.58 / 89 | 3.4% / 2.17 / 78 | 1.5% / 0.54 / 76 |
| 9 | 3.4% / 1.67 / 106 | -1.6% / -1.01 / 102 | 5.0% / 1.96 / 119 | 0.9% / 0.56 / 102 | 4.4% / 1.31 / 101 |
| 10 | 2.8% / 1.80 / 84 | -0.3% / -0.16 / 82 | 3.5% / 1.58 / 89 | 3.2% / 2.13 / 78 | 1.3% / 0.47 / 76 |
| 11 | 1.1% / 1.02 / 27 | -0.2% / -0.49 / 19 | 0.0% / 0.03 / 16 | 0.0% / 0.08 / 23 | 2.7% / 3.23 / 20 |
| 12 | 2.8% / 1.42 / 36 | 0.4% / 0.37 / 33 | 3.4% / 2.14 / 53 | 1.2% / 1.01 / 36 | 0.6% / 0.23 / 31 |
| 13 | 3.9% / 1.93 / 85 | 0.9% / 0.63 / 81 | 0.6% / 0.28 / 87 | 3.0% / 2.00 / 77 | 2.4% / 0.85 / 76 |
| 14 | 5.0% / 1.96 / 141 | -0.5% / -0.23 / 145 | 7.2% / 2.18 / 163 | -0.5% / -0.30 / 143 | 1.4% / 0.39 / 133 |
| 15 | 1.7% / 1.02 / 46 | -0.2% / -0.19 / 31 | 2.0% / 1.07 / 62 | 1.9% / 1.49 / 38 | 1.7% / 0.81 / 31 |
| 16 | 2.9% / 1.57 / 89 | -0.6% / -0.44 / 76 | 4.8% / 2.16 / 99 | 0.6% / 0.45 / 81 | 3.1% / 1.02 / 82 |
| 17 | 4.8% / 1.88 / 141 | -0.5% / -0.24 / 145 | 7.5% / 2.26 / 163 | -0.5% / -0.33 / 143 | 0.6% / 0.19 / 133 |
| 18 | 2.3% / 1.10 / 36 | 0.5% / 0.46 / 33 | 3.5% / 2.15 / 53 | 1.0% / 0.83 / 35 | 1.6% / 0.60 / 31 |
| 19 | 2.1% / 1.23 / 91 | -1.5% / -1.39 / 85 | 3.3% / 1.64 / 75 | 0.3% / 0.24 / 83 | 3.0% / 1.86 / 70 |
| 20 | 2.1% / 1.23 / 91 | -1.5% / -1.39 / 85 | 3.3% / 1.64 / 75 | 0.3% / 0.24 / 83 | 3.0% / 1.86 / 70 |
| 21 | 2.3% / 1.23 / 89 | -1.0% / -0.67 / 76 | 4.3% / 1.91 / 99 | 0.6% / 0.45 / 81 | 3.3% / 1.10 / 82 |
| 22 | 2.5% / 0.97 / 112 | 1.6% / 0.94 / 110 | 3.0% / 1.42 / 114 | 2.6% / 1.50 / 107 | 1.3% / 0.39 / 100 |
| 23 | 1.0% / 0.41 / 117 | 1.5% / 0.91 / 85 | 3.6% / 1.56 / 115 | 2.5% / 1.27 / 94 | 2.2% / 0.81 / 93 |
| 24 | 3.2% / 1.32 / 96 | 0.4% / 0.29 / 77 | 2.3% / 1.34 / 95 | 2.0% / 1.36 / 82 | 1.7% / 0.60 / 81 |
| 25 | 2.9% / 2.18 / 45 | -0.5% / -0.43 / 52 | 5.5% / 2.80 / 69 | -0.5% / -0.32 / 48 | 2.1% / 0.72 / 43 |
| 26 | 1.4% / 0.82 / 67 | 0.5% / 0.42 / 57 | 2.9% / 1.21 / 93 | 3.2% / 1.92 / 62 | 1.8% / 0.54 / 67 |
| 27 | 0.3% / 0.33 / 25 | -0.3% / -0.30 / 28 | 1.7% / 1.55 / 32 | 0.9% / 1.02 / 26 | 3.2% / 1.30 / 27 |
| 28 | 2.6% / 1.54 / 58 | 0.0% / 0.02 / 47 | 3.0% / 1.39 / 80 | 2.5% / 1.65 / 54 | 1.2% / 0.40 / 56 |
| 29 | 2.3% / 1.16 / 36 | 0.1% / 0.11 / 33 | 2.8% / 1.72 / 53 | 1.4% / 1.21 / 36 | 1.0% / 0.42 / 31 |
| 30 | 3.2% / 1.84 / 34 | 0.3% / 0.25 / 34 | 0.3% / 0.18 / 53 | 2.1% / 1.73 / 39 | 2.4% / 0.97 / 31 |
| 31 | 2.7% / 1.09 / 112 | 1.3% / 0.76 / 111 | 3.2% / 1.56 / 114 | 2.7% / 1.56 / 108 | -0.3% / -0.07 / 100 |
| 32 | 2.9% / 2.26 / 44 | -0.3% / -0.28 / 52 | 5.2% / 2.53 / 69 | -0.7% / -0.46 / 48 | 2.0% / 0.72 / 42 |
| 33 | 2.4% / 1.43 / 54 | 0.1% / 0.12 / 46 | 3.0% / 1.51 / 74 | 2.9% / 1.94 / 48 | 1.1% / 0.40 / 45 |
| 34 | 3.7% / 1.77 / 118 | -1.1% / -0.58 / 117 | 4.7% / 1.73 / 134 | 0.2% / 0.15 / 117 | 4.2% / 1.06 / 124 |
| 35 | 1.9% / 0.94 / 33 | 0.1% / 0.11 / 23 | 2.9% / 2.15 / 46 | 0.6% / 0.61 / 27 | 1.3% / 0.56 / 24 |
| 36 | 2.3% / 1.07 / 120 | -1.7% / -0.88 / 118 | 4.4% / 1.59 / 136 | 0.2% / 0.12 / 118 | 5.3% / 1.37 / 126 |
| 37 | 0.9% / 0.75 / 35 | 0.4% / 0.98 / 22 | 0.3% / 0.40 / 19 | 0.0% / 0.06 / 30 | 2.2% / 2.46 / 26 |
| 38 | 1.1% / 0.67 / 61 | 0.3% / 0.32 / 45 | 2.3% / 1.14 / 81 | 2.6% / 1.74 / 51 | 1.1% / 0.38 / 48 |
| 39 | 1.9% / 1.28 / 36 | 0.3% / 0.23 / 33 | 2.0% / 1.38 / 53 | 1.5% / 1.22 / 35 | 0.8% / 0.35 / 31 |
| 40 | 1.1% / 0.91 / 36 | 0.5% / 1.14 / 22 | 0.4% / 0.74 / 19 | 0.0% / 0.08 / 30 | 1.7% / 1.76 / 26 |
| 41 | 4.3% / 2.13 / 76 | -0.6% / -0.44 / 65 | 2.3% / 1.38 / 77 | 2.1% / 1.40 / 67 | 0.7% / 0.25 / 65 |
| 42 | 3.2% / 1.98 / 45 | -0.7% / -0.47 / 52 | 5.7% / 2.80 / 69 | -1.2% / -0.87 / 48 | 2.7% / 0.87 / 43 |
| 43 | 3.4% / 1.45 / 96 | 0.2% / 0.12 / 78 | 2.5% / 1.47 / 95 | 2.2% / 1.57 / 83 | -0.0% / 0.01 / 81 |
| 44 | 2.1% / 1.29 / 46 | -0.7% / -0.62 / 32 | 2.7% / 1.50 / 58 | 2.0% / 1.56 / 38 | 0.6% / 0.29 / 37 |
| 45 | 2.3% / 1.07 / 42 | 0.3% / 0.22 / 39 | 3.0% / 1.67 / 62 | 1.3% / 1.00 / 39 | 2.1% / 0.65 / 50 |
| 46 | 2.5% / 1.18 / 98 | 1.3% / 0.83 / 92 | -0.0% / 0.01 / 92 | 3.6% / 2.25 / 84 | 2.1% / 0.68 / 89 |
| 47 | 1.9% / 1.11 / 54 | -0.0% / -0.01 / 46 | 1.9% / 0.96 / 74 | 3.3% / 2.34 / 48 | 0.4% / 0.16 / 45 |
| 48 | 2.7% / 1.35 / 42 | 0.4% / 0.29 / 39 | 2.7% / 1.49 / 62 | 1.4% / 1.13 / 40 | 1.0% / 0.31 / 50 |
| 49 | 1.7% / 0.78 / 114 | 1.9% / 1.01 / 108 | 3.8% / 1.54 / 112 | 4.7% / 2.30 / 101 | -1.0% / -0.29 / 100 |
| 50 | 1.4% / 0.66 / 98 | 1.0% / 0.52 / 80 | 2.5% / 1.21 / 88 | 3.0% / 1.79 / 80 | 0.5% / 0.20 / 82 |
| 51 | 2.0% / 1.67 / 34 | -0.3% / -0.29 / 34 | 1.0% / 0.58 / 53 | 2.7% / 2.08 / 39 | 1.1% / 0.51 / 31 |
| 52 | 1.4% / 0.92 / 86 | 0.2% / 0.19 / 82 | 1.4% / 0.96 / 71 | 0.1% / 0.14 / 90 | 2.8% / 1.49 / 83 |
| 53 | 0.6% / 0.58 / 21 | -0.7% / -0.77 / 21 | 1.7% / 1.55 / 32 | 0.9% / 1.00 / 26 | 3.1% / 1.25 / 26 |
| 54 | 2.2% / 1.27 / 39 | 0.3% / 0.28 / 38 | 0.4% / 0.23 / 55 | 2.3% / 1.82 / 40 | 2.5% / 0.91 / 39 |
| 55 | 1.1% / 0.74 / 67 | 0.8% / 0.79 / 57 | 1.8% / 0.86 / 93 | 3.2% / 1.90 / 63 | 0.8% / 0.29 / 67 |
| 56 | 1.4% / 1.29 / 49 | 0.6% / 0.77 / 48 | 1.1% / 0.83 / 39 | 0.8% / 1.32 / 48 | 0.6% / 0.38 / 53 |
| 57 | 4.2% / 1.53 / 155 | 0.6% / 0.34 / 137 | 2.9% / 0.91 / 165 | 1.4% / 0.71 / 151 | 2.1% / 0.55 / 128 |
| 58 | 2.4% / 1.52 / 45 | -1.1% / -0.76 / 52 | 4.8% / 2.37 / 69 | -1.0% / -0.82 / 48 | 3.0% / 0.98 / 45 |
| 59 | 5.0% / 1.74 / 164 | 0.5% / 0.26 / 158 | 2.5% / 0.78 / 175 | 1.9% / 0.88 / 175 | 3.0% / 0.71 / 155 |
| 60 | 0.5% / 0.75 / 27 | 0.1% / 0.30 / 19 | 0.3% / 0.51 / 16 | -0.2% / -0.51 / 23 | 2.0% / 2.76 / 22 |
| 61 | 3.4% / 1.87 / 62 | -0.3% / -0.23 / 51 | 3.5% / 1.60 / 84 | 1.2% / 0.75 / 60 | 1.2% / 0.38 / 59 |
| 62 | 3.8% / 1.84 / 75 | -0.4% / -0.32 / 65 | 2.2% / 1.34 / 77 | 2.0% / 1.36 / 67 | 0.7% / 0.25 / 65 |
| 63 | 5.3% / 1.89 / 161 | 0.9% / 0.47 / 150 | 1.9% / 0.68 / 165 | 2.1% / 0.89 / 162 | 1.2% / 0.32 / 149 |
| 64 | 3.7% / 1.30 / 162 | 0.5% / 0.26 / 150 | 1.8% / 0.68 / 166 | 2.2% / 1.01 / 164 | 2.4% / 0.62 / 150 |
| 65 | 5.1% / 1.82 / 167 | 0.4% / 0.21 / 159 | 3.0% / 0.95 / 178 | 1.3% / 0.57 / 177 | 1.4% / 0.35 / 158 |
| 66 | 3.8% / 1.64 / 172 | -0.1% / -0.04 / 168 | -1.3% / -0.53 / 184 | 1.0% / 0.70 / 159 | 5.7% / 1.82 / 150 |
| 67 | 3.8% / 1.64 / 172 | -0.1% / -0.04 / 168 | -1.3% / -0.53 / 184 | 1.0% / 0.70 / 159 | 5.7% / 1.82 / 150 |
| 68 | 0.7% / 0.94 / 27 | 0.0% / 0.01 / 19 | -0.0% / -0.07 / 16 | -0.2% / -0.52 / 23 | 1.9% / 2.92 / 20 |
| 69 | 0.6% / 0.38 / 94 | 0.9% / 0.82 / 81 | 2.4% / 1.23 / 83 | 0.1% / 0.07 / 93 | 3.1% / 1.19 / 78 |
| 70 | 1.4% / 0.61 / 123 | 0.8% / 0.40 / 116 | 3.9% / 1.46 / 122 | 3.9% / 1.91 / 113 | 1.2% / 0.34 / 116 |
| 71 | 2.2% / 1.77 / 24 | 0.4% / 0.86 / 22 | 0.0% / 0.06 / 10 | -0.7% / -1.44 / 24 | 1.2% / 1.35 / 22 |
| 72 | 1.4% / 1.14 / 39 | -0.2% / -0.19 / 38 | 1.0% / 0.57 / 55 | 2.8% / 2.15 / 40 | 1.2% / 0.52 / 39 |
| 73 | 1.4% / 1.33 / 34 | 0.9% / 1.32 / 29 | 1.1% / 1.08 / 25 | -0.8% / -0.96 / 39 | 1.6% / 1.13 / 32 |
| 74 | 1.3% / 1.11 / 49 | 0.7% / 0.77 / 48 | 1.1% / 0.83 / 39 | 0.8% / 1.23 / 48 | 0.8% / 0.48 / 53 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_623c` | 3 | 0.92 | 0.94/0.95 | 0.90/0.93 |
| 1 | `cfg_5a04` | 4 | 0.90 | 0.91/0.97 | 0.82/0.94 |
| 2 | `cfg_c45b` | 55 | 0.82 | 0.86/0.93 | 0.75/0.81 |
| 3 | `cfg_add8` | 8 | 0.86 | 0.90/0.92 | 0.83/0.87 |
| 4 | `cfg_d75d` | 11 | 0.84 | 0.89/0.93 | 0.76/0.86 |
| 5 | `cfg_c03b` | 2 | 0.99 | 0.99/0.99 | 0.97/0.97 |
| 6 | `cfg_7458` | 2 | 0.98 | 0.98/0.98 | 0.92/0.92 |
| 7 | `cfg_0a9d` | 3 | 0.91 | 0.94/0.94 | 0.86/0.89 |
| 8 | `cfg_92a0` | 3 | 0.94 | 0.97/0.98 | 0.94/0.95 |
| 9 | `cfg_0d10` | 3 | 0.86 | 0.93/0.94 | 0.85/0.89 |
| 10 | `cfg_a9e1` | 9 | 0.85 | 0.90/0.92 | 0.80/0.86 |
| 11 | `cfg_1133` | 2 | 0.97 | 0.97/0.97 | 0.93/0.93 |
| 12 | `cfg_48c5` | 3 | 0.91 | 0.95/0.95 | 0.91/0.94 |
| 13 | `cfg_826c` | 5 | 0.81 | 0.86/0.93 | 0.60/0.77 |
| 14 | `cfg_2816` | 2 | 0.96 | 0.97/0.97 | 0.94/0.94 |
| 15 | `cfg_2881` | 2 | 0.94 | 0.95/0.95 | 0.90/0.90 |
| 16 | `cfg_960d` | 9 | 1.00 | 0.99/1.00 | 0.97/1.00 |
| 17 | `cfg_5a0d` | 9 | 0.87 | 0.89/0.95 | 0.83/0.92 |
| 18 | `cfg_b51b` | 7 | 0.81 | 0.90/0.92 | 0.76/0.81 |
| 19 | `cfg_fffc` | 2 | 0.91 | 0.90/0.90 | 0.65/0.65 |
| 20 | `cfg_a275` | 10 | 0.84 | 0.90/0.93 | 0.81/0.88 |
| 21 | `cfg_4798` | 3 | 0.86 | 0.89/0.93 | 0.82/0.87 |
| 22 | `cfg_499e` | 4 | 0.94 | 0.95/0.96 | 0.91/0.97 |
| 23 | `cfg_4ad3` | 1 | n/a | n/a/n/a | n/a/n/a |
| 24 | `cfg_60a0` | 3 | 0.93 | 0.98/0.98 | 0.93/0.95 |
| 25 | `cfg_5818` | 1 | n/a | n/a/n/a | n/a/n/a |
| 26 | `cfg_5877` | 1 | n/a | n/a/n/a | n/a/n/a |
| 27 | `cfg_5cfe` | 1 | n/a | n/a/n/a | n/a/n/a |
| 28 | `cfg_5d7d` | 3 | 0.89 | 0.97/0.97 | 0.94/0.96 |
| 29 | `cfg_5f0d` | 4 | 0.88 | 0.74/0.78 | 0.48/0.51 |
| 30 | `cfg_602b` | 3 | 0.88 | 0.90/0.93 | 0.83/0.86 |
| 31 | `cfg_61e6` | 2 | 0.92 | 0.95/0.95 | 0.91/0.91 |
| 32 | `cfg_667e` | 1 | n/a | n/a/n/a | n/a/n/a |
| 33 | `cfg_89c9` | 5 | 0.85 | 0.86/0.92 | 0.77/0.86 |
| 34 | `cfg_b336` | 2 | 0.93 | 0.97/0.97 | 0.95/0.95 |
| 35 | `cfg_9d3d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 36 | `cfg_a0e4` | 2 | 0.92 | 0.85/0.85 | 0.76/0.76 |
| 37 | `cfg_b6d6` | 1 | n/a | n/a/n/a | n/a/n/a |
| 38 | `cfg_cfd9` | 1 | n/a | n/a/n/a | n/a/n/a |
| 39 | `cfg_d63e` | 3 | 0.84 | 0.91/0.95 | 0.87/0.92 |
| 40 | `cfg_f351` | 1 | n/a | n/a/n/a | n/a/n/a |
| 41 | `cfg_f99c` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.272e-03 over 95724 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1792.0, participation ratio 30.1, 95%-variance components 454 (rank bound T = 1259); raw grid 103680; raw + known prior 1942164
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
6J results are unchanged rules on the development period: supporting evidence, not an independent replication.

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
