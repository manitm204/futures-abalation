# Screening funnel -- cb_nr_cl_v4_15m (development stages only)

- Code: `278b87465dd4` (dirty working tree: True, diff sha256 `05994d444c0f`)
- Config: `configs/funnel/cb_nr_funnel_cl_v4_15m.yaml` sha256 `2e91f81a06367876`; seed 20261118
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'CL': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `f985e9525d69d933` (73 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- CL 2023-2024 was used to select BB/KC squeeze strategies (cb_bbkc_cl_v4_15m) and mean-reversion strategies; no NR-N strategy has been selected on CL. This grid was chosen after reading NR v2/v3 on ES; it was run on CL after its NQ / YM v4 results were seen.
- Holdout 2025+ previously inspected: **True** -- CL 2025+ was read for BB/KC squeeze holdout scoring (cb_bbkc_cl_v4_15m) and mean-reversion holdout scoring per the data-access ledgers. No NR-N metrics have been computed on CL 2025+.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 2304 | 2304 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 2304 | 792 | 1512 | 0 |  | 0 | 34.38 | 34.38 |  |
| 2 trade count & coverage | hard_gate | 792 | 696 | 96 | 0 |  | 732 | 30.21 | 87.88 |  |
| 3 performance & risk | hard_gate | 696 | 352 | 344 | 0 |  | 0 | 15.28 | 50.57 |  |
| 4 parameter stability | hard_gate | 352 | 352 | 0 | 0 |  | 141 | 15.28 | 100.00 |  |
| 5 time stability | hard_gate | 352 | 346 | 6 | 0 |  | 352 | 15.02 | 98.30 |  |
| 6 deduplication | dedup | 346 | 73 |  |  | 273 |  | 3.17 | 21.10 | best 2 per cluster |
| 7 execution stress | hard_gate | 73 | 73 | 0 | 0 |  | 56 | 3.17 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 73 |  |  |  |  |  |  |  | diagnostic only: unverified: 73 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s1:hard_reject:integrity:box_not_from_prior_compression_run | 1512 |
| s1:hard_reject:integrity:entry_fill_better_than_market | 1488 |
| s1:hard_reject:integrity:entry_signal_condition_not_met | 432 |
| s1:hard_reject:integrity:eod_exit_not_at_session_close | 126 |
| s1:hard_reject:integrity:exit_not_at_first_touch | 216 |
| s1:hard_reject:integrity:not_first_breakout_of_run | 1056 |
| s1:hard_reject:integrity:stop_exit_without_touch | 138 |
| s1:hard_reject:integrity:stop_fill_better_than_rule | 282 |
| s1:hard_reject:integrity:stop_not_per_rule | 1376 |
| s1:hard_reject:integrity:target_not_per_rule | 1134 |
| s1:hard_reject:integrity:target_taken_when_stop_touched | 12 |
| s2:hard_reject:completed_trades | 96 |
| s3:hard_reject:max_drawdown | 24 |
| s3:hard_reject:net_return | 4 |
| s3:hard_reject:sharpe | 342 |
| s5:hard_reject:profitable_years | 6 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | target/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_4490` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 396/3/253 | 652 | 64.5% | 10.5% | 1.73 | -3.2% | 144 | 1.60 | 5.4% | 84.4 | 4/4 | 1.00 | 1.49 | 0.24 | 5 | 17.4% | 0.68 | 0.37 | 41.5% | 22.0% | -42.7% | 56.3%/47.8% | 2.7 (interpolated) | pass | 0.977 (unverified) | -0.14 |
| 2 | `cfg_3060` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 384/3/246 | 633 | 61.1% | 10.0% | 1.70 | -3.1% | 150 | 1.59 | 5.3% | 82.6 | 4/4 | 1.00 | 1.47 | 0.23 | 5 | 16.1% | 0.69 | 0.39 | 39.7% | 21.0% | -41.2% | 54.8%/46.2% | 2.7 (interpolated) | pass | 0.969 (unverified) | -0.20 |
| 3 | `cfg_a4ed` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0, max_range_atr=off, max_hold_bars=0 | 1394/96/1070 | 2560 | 146.8% | 19.8% | 1.45 | -23.2% | 454 | 1.17 | 30.1% | 382.4 | 4/4 | 1.00 | 1.55 | -0.09 | 5 | 95.7% | 0.35 | 0.33 | 43.5% | -16.8% | -81.8% | 120.4%/94.5% | 1.9 (interpolated) | pass | 0.799 (unverified) | 0.97 |
| 4 | `cfg_7309` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 1386/96/1064 | 2546 | 144.6% | 19.6% | 1.45 | -23.1% | 454 | 1.17 | 30.0% | 381.7 | 4/4 | 1.00 | 1.55 | -0.10 | 5 | 95.0% | 0.34 | 0.34 | 42.0% | -17.7% | -81.3% | 119.0%/94.7% | 1.9 (interpolated) | pass | 0.798 (unverified) | 0.96 |
| 5 | `cfg_da0c` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 127/2/71 | 200 | 12.3% | 2.3% | 1.23 | -1.6% | 223 | 1.69 | 1.7% | 30.8 | 5/5 | 1.00 | 1.23 | -0.00 | 5 | 6.1% | 0.49 | 0.36 | 7.7% | 3.4% | -4.5% | 11.1%/9.2% | 2.4 (interpolated) | pass | 0.682 (unverified) | -0.20 |
| 6 | `cfg_eced` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 124/2/69 | 195 | 12.1% | 2.3% | 1.24 | -1.6% | 223 | 1.69 | 1.6% | 30.2 | 5/5 | 1.00 | 1.21 | 0.02 | 5 | 6.0% | 0.49 | 0.36 | 7.7% | 3.5% | -3.7% | 11.1%/9.5% | 2.4 (interpolated) | pass | 0.687 (unverified) | -0.36 |
| 7 | `cfg_8e68` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 448/222/309 | 979 | 120.9% | 17.2% | 1.27 | -10.2% | 139 | 1.36 | 17.4% | 141.8 | 5/5 | 1.00 | 1.19 | 0.08 | 4 | 29.5% | 0.61 | 0.34 | 78.7% | 45.4% | -43.5% | 101.9%/82.8% | 2.9 (interpolated) | pass | 0.688 (unverified) | 0.90 |
| 8 | `cfg_a09a` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.0, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 89/10/92 | 191 | 15.3% | 2.9% | 1.20 | -2.5% | 302 | 1.65 | 2.1% | 29.7 | 6/6 | 1.00 | 1.17 | 0.03 | 5 | 5.6% | 0.61 | 0.44 | 10.7% | 6.6% | 2.6% | 13.9%/11.8% | 2.8 (interpolated) | pass | 0.651 (unverified) | -0.59 |
| 9 | `cfg_5ce8` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 453/227/312 | 992 | 119.9% | 17.1% | 1.26 | -10.2% | 119 | 1.35 | 17.6% | 143.3 | 5/5 | 1.00 | 1.17 | 0.09 | 4 | 28.0% | 0.62 | 0.34 | 77.3% | 41.4% | -44.4% | 107.5%/84.7% | 2.8 (interpolated) | pass | 0.682 (unverified) | 0.70 |
| 10 | `cfg_386a` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 145/58/85 | 288 | 44.9% | 7.7% | 1.30 | -8.0% | 206 | 1.60 | 4.8% | 39.8 | 5/5 | 1.00 | 1.17 | 0.13 | 4 | 10.0% | 0.76 | 0.44 | 36.1% | 28.1% | -10.5% | 39.5%/34.1% | 3.9 (interpolated) | pass | 0.698 (unverified) | -0.01 |
| 11 | `cfg_ab75` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.0, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 92/11/94 | 197 | 15.9% | 3.0% | 1.23 | -2.6% | 301 | 1.66 | 2.1% | 30.6 | 6/6 | 1.00 | 1.19 | 0.04 | 5 | 6.7% | 0.56 | 0.42 | 11.5% | 7.0% | 3.3% | 14.8%/12.2% | 2.9 (interpolated) | pass | 0.680 (unverified) | -0.50 |
| 12 | `cfg_ef38` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=3.5, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 14/110/56 | 180 | 33.4% | 5.9% | 1.16 | -5.5% | 206 | 1.81 | 4.4% | 28.1 | 6/6 | 1.00 | 1.08 | 0.08 | 4 | 11.3% | 0.63 | 0.57 | 29.2% | 23.8% | 15.5% | 31.4%/26.8% | 5.0 (interpolated) | pass | 0.618 (unverified) | 0.06 |
| 13 | `cfg_1025` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=3.5, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 14/106/56 | 176 | 32.4% | 5.8% | 1.13 | -5.5% | 206 | 1.79 | 4.3% | 27.3 | 6/6 | 1.00 | 1.03 | 0.10 | 4 | 10.5% | 0.65 | 0.58 | 28.2% | 22.9% | 14.8% | 30.0%/23.1% | 5.0 (interpolated) | pass | 0.586 (unverified) | 0.09 |
| 14 | `cfg_7be4` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 149/61/86 | 296 | 42.7% | 7.4% | 1.18 | -7.1% | 206 | 1.53 | 5.0% | 40.1 | 5/5 | 1.00 | 1.01 | 0.17 | 4 | 13.0% | 0.67 | 0.48 | 33.0% | 25.0% | -12.9% | 37.8%/31.2% | 3.7 (interpolated) | pass | 0.603 (unverified) | -0.04 |
| 15 | `cfg_6253` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 25/210/55 | 290 | 54.8% | 9.1% | 1.14 | -6.4% | 206 | 1.54 | 7.6% | 40.2 | 6/6 | 1.00 | 0.97 | 0.17 | 4 | 16.0% | 0.67 | 0.53 | 44.2% | 35.2% | 2.6% | 49.4%/37.8% | 4.4 (interpolated) | pass | 0.585 (unverified) | 0.58 |
| 16 | `cfg_6354` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 24/202/54 | 280 | 56.4% | 9.4% | 1.12 | -7.3% | 206 | 1.58 | 7.5% | 38.5 | 6/6 | 1.00 | 0.98 | 0.15 | 4 | 11.5% | 0.76 | 0.52 | 47.6% | 38.1% | 4.9% | 51.4%/41.3% | 4.7 (interpolated) | pass | 0.570 (unverified) | 0.64 |
| 17 | `cfg_a45f` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 95/44/47 | 186 | 19.2% | 3.6% | 1.11 | -4.2% | 269 | 1.59 | 3.2% | 28.8 | 5/5 | 1.00 | 1.08 | 0.04 | 4 | 7.9% | 0.58 | 0.42 | 14.5% | 10.5% | 0.8% | 17.3%/13.6% | 3.3 (interpolated) | pass | 0.557 (unverified) | -0.20 |
| 18 | `cfg_704d` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 93/42/47 | 182 | 18.8% | 3.5% | 1.09 | -4.2% | 269 | 1.58 | 3.1% | 28.0 | 5/5 | 1.00 | 0.97 | 0.13 | 4 | 7.5% | 0.59 | 0.43 | 14.1% | 10.2% | 0.1% | 16.5%/13.2% | 3.3 (interpolated) | pass | 0.540 (unverified) | -0.16 |
| 19 | `cfg_d758` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=3.5, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 19/178/109 | 306 | 47.2% | 8.1% | 1.04 | -7.1% | 206 | 1.46 | 7.3% | 42.1 | 5/5 | 1.00 | 1.01 | 0.03 | 4 | 11.3% | 0.74 | 0.60 | 37.0% | 28.5% | -5.6% | 44.0%/33.0% | 3.9 (interpolated) | pass | 0.488 (unverified) | -0.15 |
| 20 | `cfg_e095` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=3.5, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 19/170/104 | 293 | 45.3% | 7.8% | 1.03 | -8.1% | 206 | 1.47 | 7.1% | 40.8 | 6/6 | 1.00 | 0.98 | 0.04 | 4 | 10.9% | 0.74 | 0.63 | 36.2% | 27.1% | -4.6% | 41.5%/28.9% | 3.9 (interpolated) | pass | 0.475 (unverified) | -0.17 |
| 21 | `cfg_d765` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=3.5, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 75/38/180 | 293 | 34.8% | 6.2% | 1.06 | -7.1% | 364 | 1.51 | 4.3% | 40.1 | 6/6 | 1.00 | 0.92 | 0.14 | 3 | 2.2% | 0.95 | 0.68 | 26.0% | 18.1% | -9.9% | 32.1%/25.2% | 3.3 (interpolated) | pass | 0.515 (unverified) | 0.23 |
| 22 | `cfg_af69` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=3.5, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 18/163/102 | 283 | 45.3% | 7.8% | 1.00 | -8.8% | 206 | 1.49 | 6.9% | 39.2 | 6/6 | 1.00 | 0.96 | 0.03 | 4 | 6.5% | 0.85 | 0.63 | 36.3% | 27.8% | -4.5% | 42.2%/33.7% | 3.9 (interpolated) | pass | 0.443 (unverified) | -0.10 |
| 23 | `cfg_346f` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0, max_range_atr=off, max_hold_bars=0 | 197/1/127 | 325 | 15.6% | 3.0% | 1.10 | -2.2% | 318 | 1.41 | 2.8% | 49.7 | 5/5 | 1.00 | 0.86 | 0.24 | 4 | 6.1% | 0.59 | 0.40 | 8.0% | 0.8% | -23.6% | 14.0%/11.3% | 2.1 (interpolated) | pass | 0.551 (unverified) | -0.16 |
| 24 | `cfg_eb42` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=3.5, direction=both, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 77/39/186 | 302 | 33.6% | 6.0% | 1.02 | -6.5% | 364 | 1.48 | 4.4% | 40.6 | 6/6 | 1.00 | 0.90 | 0.12 | 3 | 2.9% | 0.92 | 0.70 | 24.9% | 16.6% | -9.8% | 30.4%/23.1% | 3.2 (interpolated) | pass | 0.471 (unverified) | 0.31 |
| 25 | `cfg_564c` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=none, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 0/180/102 | 282 | 45.3% | 7.8% | 0.98 | -8.8% | 206 | 1.49 | 7.2% | 38.8 | 5/5 | 1.00 | 0.95 | 0.02 | 4 | 8.5% | 0.80 | 0.63 | 36.0% | 27.2% | -4.8% | 40.6%/32.3% | 4.0 (interpolated) | pass | 0.422 (unverified) | -0.08 |
| 26 | `cfg_3f34` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 462/413/345 | 1220 | 111.3% | 16.2% | 1.01 | -17.8% | 210 | 1.16 | 30.6% | 187.2 | 4/4 | 1.00 | 0.93 | 0.07 | 4 | 34.3% | 0.62 | 0.48 | 62.6% | 25.3% | -17.0% | 95.7%/77.6% | 2.5 (interpolated) | pass | 0.463 (unverified) | 1.29 |
| 27 | `cfg_7556` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=2.0, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 36/91/55 | 182 | 22.0% | 4.1% | 0.97 | -5.5% | 301 | 1.56 | 4.0% | 28.2 | 6/6 | 1.00 | 0.93 | 0.04 | 3 | 4.5% | 0.79 | 0.60 | 17.5% | 13.0% | 10.2% | 20.0%/16.5% | 3.7 (interpolated) | pass | 0.416 (unverified) | 0.02 |
| 28 | `cfg_6df0` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=3.5, direction=both, trend_filter=none, min_box_atr=0.0, max_range_atr=off, max_hold_bars=0 | 329/478/1156 | 1963 | 112.3% | 16.3% | 0.88 | -25.8% | 470 | 1.12 | 45.5% | 299.5 | 5/5 | 1.00 | 1.04 | -0.16 | 4 | 62.6% | 0.33 | 0.61 | 39.2% | -8.7% | -48.8% | 100.1%/61.5% | 1.9 (interpolated) | pass | 0.362 (unverified) | 0.90 |
| 29 | `cfg_8485` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 195/1/125 | 321 | 15.7% | 3.0% | 1.11 | -2.2% | 318 | 1.41 | 2.8% | 49.2 | 5/5 | 1.00 | 0.86 | 0.25 | 4 | 6.3% | 0.58 | 0.40 | 8.3% | 1.3% | -23.2% | 14.8%/12.0% | 2.1 (interpolated) | pass | 0.561 (unverified) | -0.29 |
| 30 | `cfg_16e5` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 0/199/392 | 591 | 58.2% | 9.6% | 0.95 | -9.2% | 360 | 1.36 | 10.8% | 80.8 | 4/4 | 1.00 | 0.95 | 0.01 | 4 | 5.0% | 0.91 | 0.72 | 39.8% | 23.1% | -14.8% | 55.1%/38.7% | 2.8 (interpolated) | pass | 0.400 (unverified) | 0.31 |
| 31 | `cfg_28f0` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 235/836/550 | 1621 | 143.0% | 19.5% | 0.95 | -22.7% | 170 | 1.13 | 56.3% | 257.3 | 5/5 | 1.00 | 0.72 | 0.23 | 5 | 69.4% | 0.42 | 0.61 | 74.2% | 23.4% | -58.9% | 126.0%/73.8% | 2.4 (interpolated) | pass | 0.418 (unverified) | 1.14 |
| 32 | `cfg_0582` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.0, direction=both, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 25/207/55 | 287 | 53.0% | 8.9% | 1.00 | -7.3% | 206 | 1.50 | 7.6% | 38.7 | 6/6 | 1.00 | 0.85 | 0.15 | 4 | 16.7% | 0.65 | 0.57 | 43.0% | 34.0% | 1.5% | 46.1%/37.7% | 4.3 (interpolated) | pass | 0.450 (unverified) | 0.71 |
| 33 | `cfg_438f` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 0/196/380 | 576 | 58.7% | 9.7% | 0.98 | -7.8% | 360 | 1.37 | 10.6% | 79.1 | 4/4 | 1.00 | 0.94 | 0.04 | 4 | 5.5% | 0.89 | 0.71 | 39.8% | 23.6% | -13.7% | 53.2%/37.5% | 2.8 (interpolated) | pass | 0.420 (unverified) | 0.24 |
| 34 | `cfg_5281` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.0, max_range_atr=off, max_hold_bars=0 | 464/417/346 | 1227 | 101.5% | 15.1% | 0.94 | -16.4% | 210 | 1.15 | 30.7% | 188.1 | 4/4 | 1.00 | 0.87 | 0.07 | 4 | 37.4% | 0.56 | 0.52 | 54.8% | 20.5% | -19.8% | 92.8%/67.3% | 2.4 (interpolated) | pass | 0.400 (unverified) | 1.33 |
| 35 | `cfg_8596` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.0, direction=both, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 25/215/56 | 296 | 46.6% | 8.0% | 0.94 | -7.3% | 206 | 1.43 | 7.7% | 40.5 | 6/6 | 1.00 | 0.88 | 0.06 | 4 | 17.9% | 0.58 | 0.62 | 37.5% | 28.4% | -2.3% | 42.8%/30.3% | 3.9 (interpolated) | pass | 0.398 (unverified) | 0.65 |
| 36 | `cfg_5f7d` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=2.0, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 36/87/55 | 178 | 21.0% | 3.9% | 0.93 | -5.5% | 439 | 1.54 | 4.0% | 27.5 | 6/6 | 1.00 | 0.90 | 0.03 | 3 | 3.6% | 0.82 | 0.62 | 16.6% | 12.3% | 9.7% | 19.7%/14.6% | 3.6 (interpolated) | pass | 0.380 (unverified) | 0.05 |
| 37 | `cfg_7e4f` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=3.5, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 328/479/1149 | 1956 | 120.7% | 17.2% | 0.92 | -24.6% | 431 | 1.13 | 45.4% | 299.2 | 5/5 | 1.00 | 1.11 | -0.18 | 4 | 67.8% | 0.32 | 0.58 | 42.6% | -4.6% | -47.7% | 106.3%/69.7% | 2.0 (interpolated) | pass | 0.396 (unverified) | 0.84 |
| 38 | `cfg_edf3` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.0, direction=both, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 25/224/60 | 309 | 47.6% | 8.1% | 0.93 | -7.3% | 206 | 1.42 | 8.0% | 42.0 | 5/5 | 1.00 | 0.89 | 0.04 | 4 | 17.9% | 0.58 | 0.60 | 37.7% | 28.2% | -5.1% | 41.4%/32.0% | 3.8 (interpolated) | pass | 0.392 (unverified) | 0.60 |
| 39 | `cfg_a8c4` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=2.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 299/381/553 | 1233 | 104.9% | 15.4% | 0.92 | -21.5% | 251 | 1.16 | 30.0% | 187.7 | 5/5 | 1.00 | 0.89 | 0.03 | 4 | 35.9% | 0.58 | 0.65 | 57.5% | 22.4% | -34.2% | 87.7%/63.6% | 2.5 (interpolated) | pass | 0.386 (unverified) | 1.05 |
| 40 | `cfg_7e65` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 0/71/117 | 188 | 24.3% | 4.4% | 0.98 | -4.8% | 350 | 1.78 | 3.6% | 29.3 | 5/5 | 1.00 | 0.91 | 0.06 | 4 | 3.7% | 0.83 | 0.80 | 19.5% | 14.7% | 7.8% | 22.6%/19.2% | 3.8 (interpolated) | pass | 0.405 (unverified) | 0.20 |
| 41 | `cfg_bfea` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.0, direction=both, trend_filter=none, min_box_atr=0.0, max_range_atr=off, max_hold_bars=0 | 235/839/551 | 1625 | 144.4% | 19.6% | 0.96 | -22.7% | 170 | 1.13 | 56.4% | 257.8 | 5/5 | 1.00 | 0.73 | 0.23 | 5 | 70.3% | 0.42 | 0.61 | 74.0% | 23.8% | -58.7% | 136.8%/87.0% | 2.4 (interpolated) | pass | 0.422 (unverified) | 1.20 |
| 42 | `cfg_b7f2` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.0, max_range_atr=off, max_hold_bars=0 | 807/52/618 | 1477 | 67.7% | 10.9% | 0.99 | -14.9% | 288 | 1.17 | 16.9% | 218.9 | 4/4 | 1.00 | 1.10 | -0.11 | 4 | 37.5% | 0.37 | 0.55 | 22.1% | -10.9% | -64.2% | 60.3%/41.9% | 1.8 (interpolated) | pass | 0.449 (unverified) | 1.22 |
| 43 | `cfg_81e6` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=2.0, direction=both, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 177/423/332 | 932 | 79.4% | 12.4% | 0.97 | -15.8% | 234 | 1.24 | 21.5% | 140.8 | 6/6 | 1.00 | 0.90 | 0.07 | 4 | 50.7% | 0.32 | 0.45 | 45.8% | 18.5% | -32.6% | 74.4%/50.0% | 2.5 (interpolated) | pass | 0.429 (unverified) | 1.06 |
| 44 | `cfg_c3ab` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=3.5, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 48/30/109 | 187 | 14.7% | 2.8% | 0.95 | -4.1% | 439 | 1.52 | 2.8% | 29.3 | 6/6 | 1.00 | 0.89 | 0.05 | 3 | 0.2% | 0.98 | 0.62 | 10.4% | 6.4% | 7.8% | 13.8%/11.8% | 2.8 (interpolated) | pass | 0.393 (unverified) | -0.18 |
| 45 | `cfg_8249` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 0/114/202 | 316 | 36.5% | 6.4% | 0.94 | -5.0% | 312 | 1.45 | 5.8% | 42.0 | 4/4 | 1.00 | 0.88 | 0.06 | 4 | 6.5% | 0.82 | 0.75 | 27.4% | 17.9% | -10.0% | 34.6%/27.2% | 3.2 (interpolated) | pass | 0.388 (unverified) | 0.07 |
| 46 | `cfg_d02d` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 679/184/517 | 1380 | 61.5% | 10.1% | 0.83 | -20.5% | 327 | 1.12 | 22.5% | 208.0 | 4/4 | 1.00 | 0.95 | -0.12 | 4 | 28.3% | 0.62 | 0.62 | 20.3% | -9.9% | -45.5% | 54.1%/39.6% | 1.8 (interpolated) | pass | 0.336 (unverified) | 1.17 |
| 47 | `cfg_1169` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=2.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 174/416/329 | 919 | 78.6% | 12.3% | 0.97 | -16.3% | 235 | 1.24 | 21.3% | 138.8 | 6/6 | 1.00 | 0.91 | 0.06 | 4 | 48.5% | 0.34 | 0.45 | 45.2% | 18.5% | -32.4% | 73.9%/52.7% | 2.5 (interpolated) | pass | 0.427 (unverified) | 1.15 |
| 48 | `cfg_65cd` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.0, max_range_atr=off, max_hold_bars=0 | 682/186/518 | 1386 | 57.5% | 9.5% | 0.78 | -20.0% | 325 | 1.11 | 22.6% | 208.7 | 4/4 | 1.00 | 0.90 | -0.12 | 4 | 25.1% | 0.64 | 0.65 | 16.8% | -12.4% | -47.8% | 54.5%/36.2% | 1.8 (interpolated) | pass | 0.294 (unverified) | 1.16 |
| 49 | `cfg_204a` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=3.5, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 48/31/112 | 191 | 13.9% | 2.6% | 0.91 | -4.0% | 439 | 1.49 | 2.9% | 29.8 | 6/6 | 1.00 | 0.90 | 0.00 | 3 | -0.4% | 1.02 | 0.64 | 9.5% | 5.2% | 5.6% | 13.0%/10.9% | 2.7 (interpolated) | pass | 0.353 (unverified) | -0.13 |
| 50 | `cfg_c241` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 0/71/114 | 185 | 24.3% | 4.4% | 0.99 | -4.8% | 488 | 1.79 | 3.5% | 29.0 | 5/5 | 1.00 | 0.93 | 0.06 | 4 | 3.5% | 0.84 | 0.78 | 19.5% | 14.8% | 7.7% | 23.2%/18.8% | 3.9 (interpolated) | pass | 0.426 (unverified) | 0.25 |
| 51 | `cfg_db35` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 0/102/189 | 291 | 33.3% | 5.9% | 0.92 | -6.7% | 464 | 1.48 | 5.4% | 39.8 | 5/5 | 1.00 | 0.86 | 0.06 | 4 | 0.4% | 1.01 | 0.81 | 24.6% | 17.0% | -9.3% | 29.7%/22.2% | 3.2 (interpolated) | pass | 0.357 (unverified) | 0.11 |
| 52 | `cfg_6d4a` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 0/568/335 | 903 | 70.2% | 11.2% | 0.86 | -15.6% | 117 | 1.22 | 23.8% | 136.3 | 5/5 | 1.00 | 0.81 | 0.04 | 5 | 49.8% | 0.29 | 0.58 | 40.5% | 15.2% | -23.0% | 63.6%/44.8% | 2.4 (interpolated) | pass | 0.322 (unverified) | 1.07 |
| 53 | `cfg_63ee` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.0, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=off, max_hold_bars=0 | 84/12/107 | 203 | 12.4% | 2.4% | 0.90 | -2.7% | 439 | 1.42 | 2.3% | 30.1 | 6/6 | 0.83 | 0.72 | 0.18 | 3 | 1.8% | 0.85 | 0.67 | 7.8% | 3.3% | 0.5% | 11.6%/8.3% | 2.4 (interpolated) | pass | 0.361 (unverified) | -0.88 |
| 54 | `cfg_25a6` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0, max_range_atr=off, max_hold_bars=0 | 260/142/188 | 590 | 32.2% | 5.7% | 0.82 | -6.3% | 184 | 1.21 | 10.0% | 86.6 | 5/5 | 1.00 | 0.71 | 0.10 | 4 | 7.0% | 0.73 | 0.60 | 15.4% | 1.9% | -42.5% | 28.6%/18.9% | 2.1 (interpolated) | pass | 0.314 (unverified) | 0.36 |
| 55 | `cfg_39a1` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.0, direction=long, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 138/13/162 | 313 | 24.2% | 4.4% | 0.86 | -4.8% | 183 | 1.43 | 3.6% | 45.7 | 6/6 | 1.00 | 0.84 | 0.01 | 4 | 4.3% | 0.82 | 0.79 | 16.0% | 8.4% | -7.0% | 22.0%/14.4% | 2.6 (interpolated) | pass | 0.327 (unverified) | -0.25 |
| 56 | `cfg_3147` | timeframe=15min, compression=nr, nr_lookback=8, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.0, direction=both, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 20/201/50 | 271 | 38.0% | 6.7% | 0.80 | -7.3% | 206 | 1.40 | 7.0% | 37.5 | 6/6 | 1.00 | 0.81 | -0.01 | 4 | 13.8% | 0.61 | 0.76 | 29.7% | 22.1% | -3.2% | 33.5%/25.7% | 3.7 (interpolated) | pass | 0.286 (unverified) | 0.60 |
| 57 | `cfg_d6f5` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.0, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 82/12/105 | 199 | 12.4% | 2.4% | 0.90 | -2.5% | 439 | 1.42 | 2.3% | 29.7 | 6/6 | 0.83 | 0.74 | 0.16 | 3 | 2.2% | 0.82 | 0.68 | 7.8% | 3.4% | 1.1% | 10.9%/8.2% | 2.4 (interpolated) | pass | 0.363 (unverified) | -0.88 |
| 58 | `cfg_9b12` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=2.0, direction=both, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 110/265/193 | 568 | 61.9% | 10.1% | 0.92 | -13.4% | 336 | 1.30 | 12.7% | 80.7 | 5/5 | 1.00 | 0.88 | 0.04 | 3 | 16.4% | 0.68 | 0.57 | 41.5% | 25.2% | -21.6% | 53.5%/37.2% | 2.9 (interpolated) | pass | 0.374 (unverified) | 0.17 |
| 59 | `cfg_6bf6` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 270/447/184 | 901 | 86.5% | 13.3% | 0.84 | -18.5% | 173 | 1.25 | 21.9% | 133.7 | 5/5 | 1.00 | 0.77 | 0.08 | 5 | 51.7% | 0.32 | 0.53 | 52.7% | 27.0% | -48.0% | 82.0%/60.4% | 2.6 (interpolated) | pass | 0.288 (unverified) | 0.96 |
| 60 | `cfg_df72` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=3.5, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 46/519/334 | 899 | 57.7% | 9.5% | 0.79 | -14.2% | 140 | 1.19 | 23.0% | 136.3 | 6/6 | 1.00 | 0.85 | -0.05 | 4 | 33.9% | 0.37 | 0.57 | 29.9% | 7.3% | -28.2% | 56.8%/39.5% | 2.2 (interpolated) | pass | 0.278 (unverified) | 1.12 |
| 61 | `cfg_5b64` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.0, direction=long, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 135/13/160 | 308 | 23.5% | 4.3% | 0.84 | -4.8% | 183 | 1.42 | 3.6% | 45.3 | 6/6 | 1.00 | 0.85 | -0.01 | 4 | 4.1% | 0.82 | 0.81 | 15.7% | 8.3% | -7.5% | 21.1%/15.7% | 2.6 (interpolated) | pass | 0.311 (unverified) | -0.32 |
| 62 | `cfg_5df1` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=none, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 0/269/142 | 411 | 52.9% | 8.9% | 0.88 | -8.8% | 314 | 1.38 | 9.7% | 56.3 | 5/5 | 1.00 | 0.75 | 0.13 | 3 | 6.0% | 0.87 | 0.78 | 39.5% | 27.0% | -12.2% | 46.3%/28.7% | 3.4 (interpolated) | pass | 0.321 (unverified) | 0.25 |
| 63 | `cfg_44b4` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 254/136/185 | 575 | 35.4% | 6.3% | 0.92 | -6.4% | 272 | 1.23 | 9.8% | 84.9 | 5/5 | 1.00 | 0.78 | 0.14 | 4 | 5.6% | 0.80 | 0.54 | 20.2% | 6.2% | -39.9% | 33.0%/23.2% | 2.3 (interpolated) | pass | 0.398 (unverified) | 0.35 |
| 64 | `cfg_6666` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 272/452/186 | 910 | 84.6% | 13.1% | 0.83 | -18.5% | 155 | 1.24 | 22.1% | 134.5 | 5/5 | 1.00 | 0.75 | 0.08 | 5 | 48.7% | 0.35 | 0.54 | 51.7% | 25.2% | -48.5% | 84.1%/56.7% | 2.6 (interpolated) | pass | 0.275 (unverified) | 0.81 |
| 65 | `cfg_b47f` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.0, direction=long, trend_filter=none, min_box_atr=0.0, max_range_atr=off, max_hold_bars=0 | 129/20/172 | 321 | 15.9% | 3.0% | 0.86 | -4.1% | 364 | 1.29 | 3.8% | 48.9 | 6/6 | 1.00 | 0.67 | 0.19 | 4 | 1.2% | 0.93 | 0.73 | 8.1% | 1.1% | -11.7% | 14.2%/9.8% | 2.1 (interpolated) | pass | 0.335 (unverified) | 0.15 |
| 66 | `cfg_1bbf` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=2.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 107/257/191 | 555 | 56.9% | 9.4% | 0.87 | -13.2% | 336 | 1.29 | 12.4% | 78.6 | 5/5 | 1.00 | 0.92 | -0.05 | 3 | 14.5% | 0.70 | 0.62 | 39.2% | 22.9% | -22.0% | 50.9%/37.2% | 2.9 (interpolated) | pass | 0.327 (unverified) | 0.12 |
| 67 | `cfg_4400` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=3.5, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 18/251/142 | 411 | 43.3% | 7.5% | 0.82 | -8.7% | 364 | 1.33 | 9.5% | 57.0 | 6/6 | 1.00 | 0.74 | 0.08 | 3 | 3.9% | 0.88 | 0.81 | 30.5% | 19.3% | -16.1% | 37.3%/23.7% | 3.0 (interpolated) | pass | 0.276 (unverified) | 0.06 |
| 68 | `cfg_d1c9` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=3.5, direction=both, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 33/330/198 | 561 | 47.4% | 8.1% | 0.77 | -13.1% | 211 | 1.24 | 13.8% | 80.5 | 5/5 | 1.00 | 0.77 | 0.00 | 4 | 18.1% | 0.58 | 0.67 | 30.1% | 14.9% | -10.8% | 41.1%/29.0% | 2.6 (interpolated) | pass | 0.262 (unverified) | 0.11 |
| 69 | `cfg_572c` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=3.5, direction=both, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 33/321/192 | 546 | 46.3% | 7.9% | 0.77 | -13.1% | 211 | 1.24 | 13.5% | 78.6 | 6/6 | 1.00 | 0.75 | 0.02 | 4 | 18.1% | 0.57 | 0.68 | 29.6% | 15.3% | -8.9% | 40.2%/25.8% | 2.6 (interpolated) | pass | 0.258 (unverified) | 0.06 |
| 70 | `cfg_b1a8` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.0, direction=long, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 127/20/170 | 317 | 15.8% | 3.0% | 0.86 | -4.1% | 364 | 1.29 | 3.8% | 48.5 | 6/6 | 1.00 | 0.68 | 0.18 | 4 | 1.5% | 0.91 | 0.74 | 8.2% | 1.1% | -11.2% | 14.3%/11.4% | 2.1 (interpolated) | pass | 0.332 (unverified) | 0.12 |
| 71 | `cfg_afa2` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=3.5, direction=long, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 4/224/53 | 281 | 36.1% | 6.4% | 0.77 | -10.1% | 206 | 1.39 | 8.4% | 41.0 | 6/6 | 0.83 | 0.67 | 0.11 | 4 | 15.3% | 0.57 | 0.81 | 27.9% | 20.4% | -8.1% | 33.6%/24.9% | 3.6 (interpolated) | pass | 0.247 (unverified) | 0.70 |
| 72 | `cfg_ec6e` | timeframe=15min, compression=nr, nr_lookback=4, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.0, direction=long, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 26/205/53 | 284 | 36.1% | 6.4% | 0.79 | -10.0% | 206 | 1.39 | 7.9% | 41.5 | 6/6 | 0.83 | 0.69 | 0.10 | 4 | 13.9% | 0.61 | 0.76 | 27.8% | 20.0% | -10.5% | 32.2%/20.3% | 3.5 (interpolated) | pass | 0.261 (unverified) | 0.65 |
| 73 | `cfg_f2dc` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=long, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/118/194 | 312 | 26.1% | 4.8% | 0.75 | -8.3% | 470 | 1.39 | 5.5% | 48.0 | 5/5 | 1.00 | 0.62 | 0.13 | 3 | -6.8% | 1.31 | 1.00 | 18.2% | 10.8% | -1.8% | 23.1%/16.0% | 2.8 (interpolated) | pass | 0.193 (unverified) | 0.77 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 7.3% / 2.52 / 146 | 2.5% / 0.79 / 147 | 40.0% / 3.00 / 142 | 3.1% / 1.04 / 127 | 3.6% / 1.07 / 90 |
| 2 | 6.6% / 2.33 / 140 | 2.4% / 0.79 / 144 | 38.7% / 2.98 / 137 | 3.4% / 1.14 / 125 | 2.8% / 0.89 / 87 |
| 3 | 0.5% / 0.10 / 549 | 31.7% / 3.04 / 533 | 28.6% / 1.30 / 507 | 15.0% / 1.61 / 494 | 26.1% / 1.93 / 477 |
| 4 | 0.6% / 0.11 / 545 | 31.6% / 3.05 / 530 | 27.8% / 1.27 / 503 | 15.2% / 1.63 / 493 | 25.4% / 1.89 / 475 |
| 5 | 2.0% / 1.61 / 44 | 1.7% / 0.90 / 47 | 5.9% / 2.02 / 37 | 1.3% / 0.94 / 45 | 1.0% / 0.57 / 27 |
| 6 | 2.1% / 1.73 / 43 | 1.5% / 0.89 / 45 | 5.7% / 1.98 / 35 | 1.3% / 0.95 / 45 | 1.0% / 0.56 / 27 |
| 7 | 4.3% / 0.72 / 203 | -0.1% / 0.02 / 222 | 70.6% / 2.19 / 207 | 12.6% / 1.92 / 194 | 10.3% / 1.23 / 153 |
| 8 | 2.1% / 1.28 / 41 | 0.2% / 0.11 / 46 | 9.1% / 2.49 / 35 | 3.0% / 1.75 / 42 | 0.2% / 0.08 / 27 |
| 9 | 4.2% / 0.71 / 207 | -0.0% / 0.03 / 226 | 71.8% / 2.21 / 210 | 11.2% / 1.74 / 195 | 10.4% / 1.24 / 154 |
| 10 | 5.2% / 1.48 / 65 | 1.9% / 0.51 / 67 | 31.8% / 2.65 / 60 | 8.4% / 2.38 / 56 | -5.4% / -1.31 / 40 |
| 11 | 2.4% / 1.44 / 44 | 0.9% / 0.36 / 47 | 8.7% / 2.40 / 36 | 3.1% / 1.76 / 43 | 0.2% / 0.10 / 27 |
| 12 | 5.3% / 1.65 / 40 | 1.2% / 0.27 / 40 | 19.8% / 2.21 / 33 | 6.2% / 1.94 / 41 | -1.7% / -0.40 / 26 |
| 13 | 4.7% / 1.46 / 37 | 1.2% / 0.27 / 40 | 19.9% / 2.21 / 33 | 6.2% / 1.93 / 40 | -1.8% / -0.43 / 26 |
| 14 | 5.9% / 1.66 / 67 | 3.0% / 0.75 / 68 | 26.2% / 2.07 / 63 | 8.6% / 2.41 / 56 | -4.5% / -1.07 / 42 |
| 15 | 6.4% / 1.49 / 66 | 3.0% / 0.48 / 66 | 33.4% / 2.08 / 61 | 10.0% / 2.08 / 57 | -3.7% / -0.70 / 40 |
| 16 | 5.7% / 1.35 / 63 | 0.8% / 0.16 / 64 | 40.3% / 2.27 / 59 | 9.8% / 2.07 / 55 | -4.8% / -0.92 / 39 |
| 17 | 3.7% / 1.71 / 41 | 2.2% / 0.70 / 42 | 10.5% / 2.19 / 35 | 3.4% / 1.59 / 41 | -1.5% / -0.42 / 27 |
| 18 | 3.3% / 1.54 / 38 | 2.2% / 0.72 / 42 | 10.6% / 2.21 / 35 | 3.3% / 1.57 / 40 | -1.4% / -0.41 / 27 |
| 19 | 4.8% / 1.08 / 69 | 3.4% / 0.53 / 72 | 32.3% / 2.10 / 63 | 6.3% / 1.51 / 61 | -3.4% / -0.66 / 41 |
| 20 | 4.5% / 1.03 / 67 | 4.1% / 0.63 / 67 | 31.0% / 2.08 / 61 | 6.6% / 1.60 / 58 | -4.4% / -0.89 / 40 |
| 21 | 5.4% / 1.50 / 67 | -1.5% / -0.45 / 69 | 32.0% / 2.54 / 61 | 3.9% / 1.27 / 57 | -5.3% / -2.05 / 39 |
| 22 | 3.7% / 0.87 / 64 | 1.5% / 0.28 / 65 | 36.4% / 2.23 / 59 | 6.5% / 1.58 / 56 | -5.1% / -1.05 / 39 |
| 23 | 2.5% / 1.30 / 75 | 0.4% / 0.23 / 71 | 9.0% / 2.06 / 62 | -1.2% / -0.67 / 65 | 4.3% / 1.63 / 52 |
| 24 | 4.9% / 1.39 / 69 | -0.9% / -0.25 / 71 | 29.8% / 2.37 / 64 | 4.0% / 1.28 / 57 | -4.8% / -1.79 / 41 |
| 25 | 2.1% / 0.54 / 64 | 5.3% / 0.70 / 65 | 33.9% / 2.14 / 59 | 5.5% / 1.42 / 56 | -4.3% / -0.82 / 38 |
| 26 | 14.4% / 1.36 / 255 | 5.5% / 0.57 / 266 | 57.4% / 1.80 / 239 | 22.7% / 2.04 / 234 | -9.4% / -0.56 / 226 |
| 27 | 4.8% / 1.76 / 40 | -1.2% / -0.30 / 40 | 16.7% / 2.26 / 35 | 4.9% / 1.80 / 41 | -3.8% / -1.20 / 26 |
| 28 | 22.3% / 1.78 / 428 | 30.6% / 2.09 / 402 | -3.7% / 0.05 / 385 | 16.4% / 1.24 / 381 | 18.7% / 1.02 / 367 |
| 29 | 2.6% / 1.38 / 74 | 0.6% / 0.31 / 70 | 8.8% / 2.03 / 60 | -1.2% / -0.67 / 65 | 4.2% / 1.62 / 52 |
| 30 | 4.0% / 0.94 / 135 | 0.5% / 0.10 / 134 | 50.7% / 2.18 / 123 | 3.4% / 0.70 / 116 | -2.8% / -0.51 / 83 |
| 31 | 21.4% / 1.56 / 348 | 14.7% / 0.99 / 340 | 43.4% / 1.23 / 309 | 16.0% / 1.06 / 315 | 4.9% / 0.33 / 309 |
| 32 | 6.3% / 1.47 / 65 | 3.5% / 0.54 / 65 | 31.0% / 1.68 / 61 | 9.9% / 2.08 / 55 | -3.5% / -0.65 / 41 |
| 33 | 3.8% / 0.91 / 129 | 0.3% / 0.08 / 132 | 50.5% / 2.21 / 120 | 3.8% / 0.77 / 114 | -2.4% / -0.42 / 81 |
| 34 | 15.1% / 1.41 / 257 | 5.7% / 0.58 / 266 | 46.6% / 1.50 / 242 | 22.6% / 2.03 / 234 | -7.8% / -0.45 / 228 |
| 35 | 6.9% / 1.60 / 68 | 3.3% / 0.52 / 66 | 24.3% / 1.45 / 63 | 10.0% / 2.10 / 57 | -3.0% / -0.55 / 42 |
| 36 | 4.0% / 1.51 / 37 | -1.3% / -0.32 / 40 | 16.8% / 2.25 / 35 | 4.9% / 1.80 / 40 | -3.8% / -1.20 / 26 |
| 37 | 22.8% / 1.83 / 426 | 31.6% / 2.14 / 400 | -2.1% / 0.10 / 384 | 16.6% / 1.26 / 380 | 19.6% / 1.07 / 366 |
| 38 | 7.1% / 1.62 / 70 | 2.0% / 0.33 / 71 | 25.2% / 1.45 / 65 | 9.9% / 2.06 / 60 | -1.9% / -0.32 / 43 |
| 39 | 13.2% / 1.35 / 260 | 6.8% / 0.68 / 260 | 50.7% / 1.47 / 247 | 26.1% / 2.28 / 234 | -10.8% / -0.76 / 232 |
| 40 | 1.2% / 0.57 / 43 | 0.7% / 0.16 / 45 | 19.8% / 2.41 / 33 | 4.6% / 1.69 / 42 | -2.7% / -0.92 / 25 |
| 41 | 22.0% / 1.60 / 349 | 14.8% / 0.99 / 341 | 43.5% / 1.23 / 309 | 15.1% / 1.01 / 316 | 5.6% / 0.37 / 310 |
| 42 | -1.0% / -0.12 / 309 | 14.8% / 1.92 / 308 | 22.0% / 1.12 / 302 | 17.8% / 2.59 / 278 | 2.7% / 0.32 / 280 |
| 43 | 12.5% / 1.66 / 197 | -2.7% / -0.27 / 213 | 23.4% / 1.02 / 195 | 19.0% / 2.28 / 184 | 11.6% / 1.14 / 143 |
| 44 | 1.6% / 0.84 / 42 | -1.6% / -0.62 / 44 | 14.4% / 2.76 / 33 | 3.8% / 1.73 / 42 | -3.6% / -2.02 / 26 |
| 45 | 3.0% / 0.91 / 72 | 3.5% / 0.58 / 77 | 28.1% / 2.04 / 65 | 3.0% / 0.89 / 62 | -3.1% / -0.81 / 40 |
| 46 | 2.1% / 0.29 / 290 | 20.7% / 2.27 / 294 | 19.4% / 0.93 / 273 | 25.9% / 2.98 / 259 | -12.8% / -1.18 / 264 |
| 47 | 12.5% / 1.66 / 193 | -3.4% / -0.39 / 209 | 22.3% / 0.98 / 192 | 20.3% / 2.43 / 183 | 11.8% / 1.17 / 142 |
| 48 | 2.7% / 0.37 / 292 | 20.9% / 2.28 / 294 | 13.8% / 0.70 / 275 | 25.9% / 2.99 / 259 | -11.5% / -1.04 / 266 |
| 49 | 1.5% / 0.77 / 43 | -2.1% / -0.87 / 45 | 14.3% / 2.72 / 35 | 3.8% / 1.73 / 42 | -3.5% / -2.00 / 26 |
| 50 | 1.3% / 0.63 / 42 | 0.4% / 0.11 / 44 | 20.1% / 2.43 / 32 | 4.6% / 1.69 / 42 | -2.7% / -0.92 / 25 |
| 51 | 2.0% / 0.61 / 67 | 0.3% / 0.08 / 69 | 32.8% / 2.38 / 60 | 3.1% / 0.92 / 57 | -4.7% / -1.38 / 38 |
| 52 | 9.3% / 1.19 / 191 | 1.7% / 0.21 / 207 | 16.7% / 0.77 / 185 | 15.4% / 1.88 / 182 | 13.6% / 1.22 / 138 |
| 53 | 2.8% / 1.76 / 36 | -1.5% / -0.71 / 44 | 10.4% / 2.24 / 45 | 1.2% / 0.66 / 45 | -0.6% / -0.27 / 33 |
| 54 | -1.4% / -0.27 / 133 | 2.0% / 0.46 / 117 | 23.5% / 1.78 / 126 | 0.9% / 0.24 / 103 | 5.5% / 0.87 / 111 |
| 55 | 2.6% / 1.05 / 82 | 1.4% / 0.48 / 73 | 19.1% / 1.75 / 56 | 3.3% / 1.25 / 62 | -2.9% / -1.02 / 40 |
| 56 | 5.5% / 1.34 / 61 | 2.4% / 0.44 / 59 | 21.3% / 1.28 / 58 | 9.3% / 2.06 / 53 | -3.7% / -0.70 / 40 |
| 57 | 2.9% / 1.85 / 35 | -1.2% / -0.60 / 43 | 10.1% / 2.17 / 43 | 1.2% / 0.66 / 45 | -0.6% / -0.27 / 33 |
| 58 | 9.1% / 1.64 / 128 | -0.8% / -0.09 / 127 | 39.1% / 1.62 / 120 | 11.8% / 2.05 / 110 | -3.8% / -0.55 / 83 |
| 59 | 19.5% / 2.37 / 191 | 2.4% / 0.32 / 200 | 22.9% / 0.79 / 189 | 9.8% / 1.31 / 180 | 13.0% / 1.35 / 141 |
| 60 | 12.0% / 1.46 / 189 | -1.5% / -0.13 / 205 | 9.6% / 0.53 / 185 | 17.8% / 2.14 / 182 | 10.7% / 1.03 / 138 |
| 61 | 2.7% / 1.10 / 81 | 1.1% / 0.38 / 71 | 18.7% / 1.72 / 54 | 3.4% / 1.26 / 62 | -3.0% / -1.03 / 40 |
| 62 | -0.7% / -0.13 / 93 | 4.3% / 0.57 / 94 | 44.3% / 1.95 / 91 | 5.8% / 1.39 / 73 | -3.3% / -0.53 / 60 |
| 63 | -2.1% / -0.40 / 127 | 2.2% / 0.51 / 116 | 28.2% / 2.24 / 122 | 1.4% / 0.36 / 102 | 4.0% / 0.65 / 108 |
| 64 | 18.2% / 2.24 / 193 | 3.4% / 0.42 / 202 | 24.2% / 0.82 / 192 | 7.8% / 1.04 / 181 | 12.8% / 1.34 / 142 |
| 65 | 1.1% / 0.47 / 75 | 0.4% / 0.15 / 70 | 14.5% / 2.43 / 62 | -0.7% / -0.31 / 62 | 0.5% / 0.15 / 52 |
| 66 | 7.6% / 1.41 / 122 | -0.4% / -0.04 / 126 | 37.1% / 1.56 / 117 | 12.1% / 2.11 / 109 | -4.7% / -0.70 / 81 |
| 67 | -0.1% / 0.00 / 93 | 0.7% / 0.15 / 94 | 37.9% / 1.89 / 91 | 6.7% / 1.52 / 73 | -3.3% / -0.55 / 60 |
| 68 | 6.4% / 1.18 / 127 | 3.9% / 0.52 / 126 | 24.7% / 1.20 / 117 | 12.9% / 1.96 / 109 | -5.3% / -0.77 / 82 |
| 69 | 6.2% / 1.16 / 125 | 4.8% / 0.63 / 121 | 23.9% / 1.19 / 114 | 13.0% / 1.97 / 106 | -6.1% / -0.91 / 80 |
| 70 | 1.2% / 0.52 / 74 | 0.5% / 0.21 / 69 | 14.1% / 2.37 / 60 | -0.7% / -0.31 / 62 | 0.5% / 0.16 / 52 |
| 71 | 6.6% / 1.45 / 73 | 6.4% / 0.88 / 64 | 18.0% / 1.17 / 51 | 5.3% / 1.26 / 56 | -3.4% / -0.55 / 37 |
| 72 | 7.5% / 1.62 / 74 | 5.6% / 0.92 / 64 | 19.5% / 1.24 / 52 | 6.3% / 1.40 / 56 | -5.6% / -1.09 / 38 |
| 73 | 0.2% / 0.08 / 72 | -3.0% / -0.89 / 69 | 35.3% / 2.42 / 57 | 0.6% / 0.21 / 62 | -4.7% / -1.30 / 52 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_ef38` | 44 | 0.83 | 0.84/0.94 | 0.74/0.85 |
| 1 | `cfg_8249` | 8 | 0.86 | 0.83/0.92 | 0.84/0.93 |
| 2 | `cfg_c3ab` | 13 | 0.86 | 0.66/0.96 | 0.48/0.92 |
| 3 | `cfg_386a` | 16 | 0.80 | 0.36/0.75 | 0.31/0.72 |
| 4 | `cfg_5df1` | 6 | 0.92 | 0.89/0.96 | 0.87/0.91 |
| 5 | `cfg_0582` | 3 | 0.93 | 0.94/0.94 | 0.83/0.87 |
| 6 | `cfg_6d4a` | 6 | 0.88 | 0.85/0.96 | 0.84/0.96 |
| 7 | `cfg_4490` | 58 | 0.81 | 0.50/0.74 | 0.23/0.52 |
| 8 | `cfg_af69` | 12 | 0.84 | 0.87/0.92 | 0.88/0.92 |
| 9 | `cfg_39a1` | 6 | 0.96 | 0.96/0.99 | 0.90/0.95 |
| 10 | `cfg_a09a` | 10 | 0.89 | 0.87/0.98 | 0.73/0.93 |
| 11 | `cfg_25a6` | 4 | 0.87 | 0.83/0.89 | 0.71/0.73 |
| 12 | `cfg_81e6` | 6 | 0.93 | 0.98/0.98 | 0.97/0.98 |
| 13 | `cfg_6253` | 12 | 0.88 | 0.83/0.89 | 0.78/0.88 |
| 14 | `cfg_7556` | 12 | 0.88 | 0.75/0.95 | 0.56/0.92 |
| 15 | `cfg_16e5` | 14 | 0.80 | 0.52/0.87 | 0.51/0.82 |
| 16 | `cfg_da0c` | 9 | 0.83 | 0.85/0.95 | 0.73/0.93 |
| 17 | `cfg_a4ed` | 8 | 0.87 | 0.54/0.67 | 0.47/0.62 |
| 18 | `cfg_9b12` | 5 | 0.92 | 0.55/0.98 | 0.78/0.97 |
| 19 | `cfg_d765` | 8 | 0.91 | 0.87/0.93 | 0.91/0.94 |
| 20 | `cfg_d758` | 8 | 0.93 | 0.91/0.95 | 0.82/0.86 |
| 21 | `cfg_a45f` | 8 | 0.95 | 0.96/0.99 | 0.92/0.97 |
| 22 | `cfg_28f0` | 3 | 0.94 | 0.87/0.93 | 0.84/0.92 |
| 23 | `cfg_8596` | 8 | 0.86 | 0.90/0.92 | 0.90/0.92 |
| 24 | `cfg_8e68` | 21 | 0.81 | 0.40/0.81 | 0.24/0.52 |
| 25 | `cfg_346f` | 4 | 0.84 | 0.82/0.82 | 0.70/0.71 |
| 26 | `cfg_3f34` | 4 | 0.86 | 0.88/0.89 | 0.77/0.77 |
| 27 | `cfg_d1c9` | 4 | 0.91 | 0.94/0.96 | 0.94/0.96 |
| 28 | `cfg_7e65` | 5 | 0.99 | 1.00/1.00 | 0.97/0.98 |
| 29 | `cfg_63ee` | 3 | 0.85 | 0.83/0.91 | 0.62/0.80 |
| 30 | `cfg_d02d` | 2 | 0.99 | 0.99/0.99 | 1.00/1.00 |
| 31 | `cfg_6bf6` | 2 | 1.00 | 1.00/1.00 | 0.99/0.99 |
| 32 | `cfg_6df0` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 33 | `cfg_a8c4` | 7 | 0.88 | 0.77/0.85 | 0.43/0.65 |
| 34 | `cfg_afa2` | 2 | 0.96 | 0.98/0.98 | 0.93/0.93 |
| 35 | `cfg_b47f` | 2 | 1.00 | 1.00/1.00 | 0.99/0.99 |
| 36 | `cfg_f2dc` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 5.521e-04 over 2304 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 234.0, participation ratio 11.3, 95%-variance components 80 (rank bound T = 1258); raw grid 2304; raw + known prior 604032
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

- Compression at bar k uses bars through k only: bbkc = 2 x population sd(close, L) < kc_mult x Wilder ATR(L) (Bollinger 2 sd inside a Keltner channel, both centred on SMA(L)); nr = the bar's high-low range is the narrowest of the last N bars (ties count), and with inside_bar also inside the previous bar's range. Indicators run over the RTH bar series across sessions.
- A run is a maximal stretch of consecutive compression bars inside one session (never continued across the open); its box through bar r is [min low, max high] of its bars up to r. The decision at bar k uses the run holding the last compression bar r <= k-1 of k's session, live when k - r <= setup_expiry_bars, the run is at least min_squeeze_bars long (NR: min_nr_bars, 1 unless the round sets it) and the box is at least min_box_atr x ATR(14)[r] wide, so the box never includes the decision bar. A box too narrow to be live never consumes its run.
- Breakout: close entries need close_k beyond the box and fill at the NEXT bar's open (market slippage); wick entries are a stop order at the box edge, filled on bar k at the worse of its open and the edge (stop slippage); a wick bar through both edges is ambiguous and not traded. The fill bar must be in the decision's session.
- The FIRST breakout of a run decides and consumes it, traded or not (wrong direction, trend filter, inside the last 30 minutes, a position already open, a missed entry). Each setup is one decision.
- Filters known at the decision: emaN (ema20 / ema50 / ema200) needs close > EMA(N) for a long / < for a short (close entries at bar k, wick entries at bar k-1); no decision on the session's last bar or less than 30 minutes before its last close.
- Stop = the far side of the box, or entry price -/+ k x ATR(14) using the ATR known before the fill bar; R = entry price (before slippage) to stop; target = entry +/- target_r x R. Stop and target are live intrabar from the entry bar; a bar touching both counts as the stop; on a wick entry's own bar only the stop is checked, and a touch there counts (conservative). Stops fill at the worse of open and stop, targets at the better of open and target (a gap through it), each with slippage.
- Every position still open on the session's last bar is closed at that bar's CLOSE (market-on-close with the same slippage); nothing is held overnight. Stop and target take precedence over the close.
- Long and short: P&L = side x (exit fill - entry fill) x quantity - commissions; sizing is the mean-reversion funnel's (as many whole contracts as equity covers at full contract value, unlevered, compounding).
- Development backtests run on data physically truncated at the development end; the final session's trade is closed at the last development bar and flagged forced (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC; the 1-minute step there is taken as the roll spread). Point moves are preserved; pre-roll price levels are not real traded prices.
- Session: each root's day session only (src/data/futures.py SESSIONS: NYSE 09:30-16:00 NY for equity indexes, 09:00-14:30 NY for crude, 08:20-13:30 NY for gold, 08:20-15:00 NY for FX; sessions under 5% of normal volume are skipped), on NYSE trading days; overnight Globex bars are not traded or used in indicators.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side (stops too) plus commission per contract per side, from the execution YAML; cost stress scales both.
- Rolls happen outside the day session (Databento rolls at 00:00 UTC) and every position is flat by the session close, so no trade straddles a roll; compression, box, stop and target are all point distances, so back-adjustment does not change them.

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Whole-contract granularity: at ~$1M equity the position is a handful of ES contracts, so position size steps with price; results are sensitive to starting equity at small sizes.
- All lengths (BB/KC length, NR-N, ATR(14), EMA(50), min squeeze bars, setup expiry) count bars of the config's timeframe and run across sessions over RTH bars only, so the overnight gap enters the first bars of each session: it widens sd and ATR there (bbkc) and can make the first bar's range look normal (nr). Runs and boxes themselves never span sessions.
- Bar data cannot order events inside a bar: a stop and a target in the same bar count as the stop, and a wick entry's own bar checks only the stop. Both choices are conservative; a target is never credited on the entry bar of a wick entry even when it was reached after the fill.
- Targets fill as if they were market orders at the target (with slippage), not as resting limits that may or may not be filled at the touch.
- Sizing ignores the stop distance (full equity per trade, as in the other families), so the box stop and the ATR stops change the exit, not the position size.
- Squeeze (BB inside KC) and NR-N are separate strategy lines with their own runs; a breakout is never compared across lines inside one run, so stage-6 dedup does not merge a squeeze config with an NR config that trades the same days.
