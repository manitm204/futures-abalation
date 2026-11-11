# Screening funnel -- cb_bbkc_cl_v4_15m (development stages only)

- Code: `36bde5f6ce84` (dirty working tree: True, diff sha256 `99d2740b6266`)
- Config: `configs/funnel/cb_bbkc_funnel_cl_v4_15m.yaml` sha256 `eb757bc495f4704f`; seed 20261112
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'CL': '2026-10-16'}
- Frozen manifest sha256: `1daffde3fd0dcc79` (50 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **False** -- No compression-breakout strategy has been selected or scored on CL 2023-2024. This grid was chosen after reading ES, NQ and YM squeeze results on 2023-2024 and 2025+. Other families were validated there (mean-reversion: combined_test, combined_v1, mr_cl_v5, mr_cl_v6, mr_cl_v7, trades_v1), so the period has been looked at by the researcher, but not for this strategy.
- Holdout 2025+ previously inspected: **False** -- No compression-breakout metrics have been computed on CL 2025+. CL 2025+ bars were read for mean-reversion holdout scoring (combined_v1, mr_cl_v7, trades_v1) per those families' data-access ledgers: different strategy families, so this is still the first test of this strategy, but the researcher has seen how that period treated them.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 3840 | 3840 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 3840 | 3840 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 3840 | 3336 | 504 | 0 |  | 2823 | 86.88 | 86.88 |  |
| 3 performance & risk | hard_gate | 3336 | 88 | 3248 | 0 |  | 0 | 2.29 | 2.64 |  |
| 4 parameter stability | hard_gate | 88 | 80 | 8 | 0 |  | 0 | 2.08 | 90.91 |  |
| 5 time stability | hard_gate | 80 | 80 | 0 | 0 |  | 79 | 2.08 | 100.00 |  |
| 6 deduplication | dedup | 80 | 50 |  |  | 30 |  | 1.30 | 62.50 | best 2 per cluster |
| 7 execution stress | hard_gate | 50 | 50 | 0 | 0 |  | 5 | 1.30 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 50 |  |  |  |  |  |  |  | diagnostic only: unverified: 50 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 504 |
| s2:hard_reject:years_with_>=10_trades | 270 |
| s3:hard_reject:max_drawdown | 1147 |
| s3:hard_reject:net_return | 1894 |
| s3:hard_reject:sharpe | 3248 |
| s4:hard_reject:local_median_sharpe | 8 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | target/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | transfer dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_49e5` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=long, trend_filter=ema50, min_box_atr=0.0 | 5/84/20 | 109 | 30.4% | 5.5% | 1.01 | -3.6% | 194 | 1.82 | 5.2% | 16.8 | 7/7 | 0.86 | 0.81 | 0.20 | 5 | 20.6% | 0.32 | 0.62 | 26.8% | 24.1% | 21.0% | 26.6%/21.7% | 6.8 (interpolated) | pass | 0.269 (unverified) | n/a |
| 2 | `cfg_c1d4` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=4, stop=1.5, target_r=2.5, direction=long, trend_filter=ema50, min_box_atr=0.0 | 12/78/33 | 123 | 31.7% | 5.7% | 0.99 | -3.9% | 292 | 1.83 | 4.2% | 18.9 | 7/7 | 0.86 | 0.59 | 0.40 | 4 | 10.5% | 0.65 | 0.74 | 27.9% | 24.8% | 14.1% | 28.0%/23.3% | 6.5 (interpolated) | pass | 0.222 (unverified) | n/a |
| 3 | `cfg_b2ae` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=2.5, direction=long, trend_filter=ema50, min_box_atr=0.0 | 14/58/37 | 109 | 31.6% | 5.7% | 1.00 | -3.4% | 208 | 1.84 | 4.2% | 16.6 | 7/7 | 1.00 | 0.55 | 0.45 | 5 | 18.4% | 0.38 | 0.66 | 28.5% | 25.7% | 16.9% | 29.7%/23.6% | 7.1 (interpolated) | pass | 0.243 (unverified) | n/a |
| 4 | `cfg_ac55` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.0 | 0/89/20 | 109 | 38.5% | 6.7% | 0.91 | -3.6% | 194 | 2.00 | 5.3% | 16.6 | 6/6 | 1.00 | 0.67 | 0.23 | 5 | 19.4% | 0.44 | 0.71 | 35.7% | 32.1% | 30.6% | 35.8%/24.4% | 8.3 (interpolated) | pass | 0.112 (unverified) | n/a |
| 5 | `cfg_1ea5` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=4, stop=box, target_r=2.5, direction=long, trend_filter=ema50, min_box_atr=0.0 | 4/106/13 | 123 | 29.9% | 5.4% | 0.91 | -5.1% | 425 | 1.80 | 5.2% | 19.0 | 7/7 | 0.86 | 0.62 | 0.29 | 3 | 8.3% | 0.68 | 0.77 | 26.3% | 23.6% | 12.5% | 27.8%/21.4% | 6.2 (interpolated) | pass | 0.158 (unverified) | n/a |
| 6 | `cfg_e92e` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=1, stop=1.5, target_r=2.5, direction=long, trend_filter=ema50, min_box_atr=0.0 | 15/101/48 | 164 | 36.4% | 6.4% | 1.01 | -4.5% | 469 | 1.67 | 5.7% | 25.1 | 7/7 | 1.00 | 0.74 | 0.26 | 5 | 16.1% | 0.52 | 0.68 | 31.6% | 27.2% | 22.0% | 32.8%/24.7% | 5.6 (interpolated) | pass | 0.260 (unverified) | n/a |
| 7 | `cfg_9c99` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.0 | 0/72/37 | 109 | 36.7% | 6.5% | 0.88 | -3.3% | 208 | 1.95 | 4.7% | 16.5 | 6/6 | 1.00 | 0.51 | 0.37 | 5 | 18.6% | 0.45 | 0.75 | 34.2% | 30.9% | 22.6% | 34.2%/25.2% | 8.0 (interpolated) | pass | 0.092 (unverified) | n/a |
| 8 | `cfg_4bc5` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0 | 581/344/458 | 1383 | 147.8% | 19.9% | 1.11 | -13.2% | 166 | 1.19 | 31.6% | 218.1 | 6/6 | 0.50 | 0.30 | 0.81 | 5 | 57.6% | 0.46 | 0.41 | 85.7% | 38.5% | 10.4% | 131.3%/98.6% | 2.6 (interpolated) | pass | 0.378 (unverified) | n/a |
| 9 | `cfg_8e07` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/578/697 | 1275 | 171.9% | 22.2% | 1.12 | -21.7% | 308 | 1.20 | 43.9% | 206.7 | 6/6 | 0.67 | 0.44 | 0.68 | 5 | 112.4% | 0.35 | 0.46 | 105.2% | 57.7% | 50.6% | 146.6%/106.4% | 2.9 (interpolated) | pass | 0.380 (unverified) | n/a |
| 10 | `cfg_7a1a` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.5, direction=both, trend_filter=none, min_box_atr=0.0 | 169/600/513 | 1282 | 152.1% | 20.4% | 0.99 | -18.5% | 229 | 1.18 | 45.1% | 209.7 | 7/7 | 0.71 | 0.58 | 0.41 | 5 | 76.0% | 0.50 | 0.43 | 92.8% | 45.9% | 27.5% | 125.0%/85.9% | 2.7 (interpolated) | pass | 0.275 (unverified) | n/a |
| 11 | `cfg_c6c3` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=1, stop=box, target_r=2.5, direction=long, trend_filter=ema50, min_box_atr=0.0 | 5/136/23 | 164 | 36.5% | 6.4% | 0.93 | -5.4% | 234 | 1.66 | 7.0% | 25.1 | 7/7 | 0.86 | 0.66 | 0.27 | 4 | 8.9% | 0.70 | 0.73 | 32.4% | 27.2% | 18.1% | 32.9%/25.8% | 5.6 (interpolated) | pass | 0.203 (unverified) | n/a |
| 12 | `cfg_d03e` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 15/156/56 | 227 | 42.9% | 7.4% | 0.92 | -10.1% | 272 | 1.45 | 10.5% | 35.4 | 7/7 | 0.86 | 0.93 | -0.01 | 5 | 29.8% | 0.30 | 0.51 | 36.7% | 29.6% | 20.6% | 38.6%/29.2% | 4.8 (interpolated) | pass | 0.237 (unverified) | n/a |
| 13 | `cfg_9f98` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=1, stop=1.5, target_r=2.5, direction=long, trend_filter=ema50, min_box_atr=0.0 | 11/71/32 | 114 | 21.6% | 4.0% | 0.84 | -3.9% | 292 | 1.61 | 3.9% | 17.7 | 7/7 | 1.00 | 0.56 | 0.28 | 4 | 9.7% | 0.53 | 0.83 | 18.8% | 16.1% | 17.7% | 20.4%/16.1% | 5.2 (interpolated) | pass | 0.145 (unverified) | n/a |
| 14 | `cfg_fcc6` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.5, direction=both, trend_filter=none, min_box_atr=0.0 | 291/346/694 | 1331 | 151.2% | 20.3% | 1.15 | -13.2% | 139 | 1.20 | 35.9% | 213.0 | 7/7 | 0.57 | 0.49 | 0.66 | 5 | 87.2% | 0.42 | 0.36 | 87.6% | 40.5% | 24.5% | 121.0%/89.1% | 2.7 (interpolated) | pass | 0.412 (unverified) | n/a |
| 15 | `cfg_72d6` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.5, direction=long, trend_filter=ema50, min_box_atr=0.0 | 7/112/30 | 149 | 36.7% | 6.5% | 1.04 | -5.6% | 223 | 1.68 | 7.3% | 22.8 | 7/7 | 0.86 | 0.81 | 0.23 | 5 | 19.3% | 0.42 | 0.59 | 32.8% | 28.3% | 26.8% | 31.9%/25.4% | 6.1 (interpolated) | pass | 0.302 (unverified) | n/a |
| 16 | `cfg_2706` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=1, stop=1.5, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 17/117/60 | 194 | 35.0% | 6.2% | 0.88 | -10.3% | 341 | 1.50 | 7.0% | 29.3 | 7/7 | 0.86 | 0.54 | 0.34 | 4 | 15.2% | 0.51 | 0.71 | 30.1% | 24.6% | 23.4% | 30.6%/21.7% | 4.7 (interpolated) | pass | 0.177 (unverified) | n/a |
| 17 | `cfg_c28b` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=long, trend_filter=ema50, min_box_atr=0.0 | 7/115/32 | 154 | 29.7% | 5.4% | 0.81 | -7.6% | 233 | 1.51 | 7.6% | 23.2 | 7/7 | 0.86 | 0.83 | -0.02 | 5 | 20.6% | 0.29 | 0.69 | 25.9% | 21.6% | 16.8% | 26.8%/20.3% | 5.1 (interpolated) | pass | 0.165 (unverified) | n/a |
| 18 | `cfg_2ab4` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 15/152/54 | 221 | 47.0% | 8.0% | 1.05 | -8.8% | 260 | 1.52 | 10.2% | 34.5 | 7/7 | 0.86 | 0.85 | 0.20 | 5 | 26.7% | 0.38 | 0.49 | 40.7% | 34.0% | 27.3% | 42.0%/32.0% | 5.2 (interpolated) | pass | 0.325 (unverified) | n/a |
| 19 | `cfg_e074` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 38/52/19 | 109 | 20.4% | 3.8% | 0.92 | -3.6% | 144 | 1.61 | 4.1% | 16.7 | 6/6 | 0.83 | 0.66 | 0.26 | 5 | 11.1% | 0.46 | 0.47 | 17.8% | 14.9% | 16.0% | 18.1%/14.2% | 5.2 (interpolated) | pass | 0.228 (unverified) | n/a |
| 20 | `cfg_fe24` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.0 | 0/122/32 | 154 | 40.4% | 7.0% | 0.83 | -7.4% | 194 | 1.66 | 7.7% | 23.0 | 6/6 | 0.83 | 0.76 | 0.07 | 5 | 20.0% | 0.45 | 0.76 | 36.5% | 31.8% | 27.4% | 37.5%/25.5% | 6.2 (interpolated) | pass | 0.118 (unverified) | n/a |
| 21 | `cfg_c676` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=1, stop=box, target_r=2.5, direction=long, trend_filter=ema50, min_box_atr=0.0 | 3/98/13 | 114 | 18.3% | 3.4% | 0.76 | -5.2% | 454 | 1.53 | 4.8% | 17.8 | 7/7 | 0.86 | 0.76 | 0.00 | 4 | 7.5% | 0.56 | 0.82 | 15.2% | 12.3% | 16.3% | 16.2%/11.8% | 4.6 (interpolated) | pass | 0.125 (unverified) | n/a |
| 22 | `cfg_5beb` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 58/67/29 | 154 | 32.8% | 5.8% | 1.10 | -5.0% | 153 | 1.66 | 5.9% | 23.2 | 6/6 | 1.00 | 0.78 | 0.31 | 5 | 16.6% | 0.44 | 0.43 | 28.7% | 24.3% | 10.4% | 29.7%/24.2% | 5.4 (interpolated) | pass | 0.362 (unverified) | n/a |
| 23 | `cfg_2793` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=1, stop=box, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 6/155/33 | 194 | 34.9% | 6.2% | 0.83 | -8.6% | 454 | 1.49 | 8.5% | 29.2 | 7/7 | 0.86 | 0.61 | 0.22 | 4 | 8.4% | 0.70 | 0.77 | 28.8% | 24.3% | 16.7% | 31.1%/23.0% | 4.7 (interpolated) | pass | 0.148 (unverified) | n/a |
| 24 | `cfg_0ca8` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/589/718 | 1307 | 130.8% | 18.2% | 0.95 | -21.9% | 276 | 1.17 | 45.7% | 214.3 | 6/6 | 0.67 | 0.34 | 0.61 | 5 | 87.1% | 0.33 | 0.51 | 75.1% | 32.2% | 27.4% | 110.1%/81.5% | 2.6 (interpolated) | pass | 0.242 (unverified) | n/a |
| 25 | `cfg_1042` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=1, stop=1.5, target_r=2.5, direction=both, trend_filter=none, min_box_atr=0.0 | 36/205/143 | 384 | 49.6% | 8.4% | 0.82 | -9.3% | 484 | 1.29 | 13.0% | 56.5 | 7/7 | 1.00 | 0.53 | 0.30 | 5 | 26.9% | 0.40 | 0.64 | 36.7% | 26.7% | 27.1% | 42.7%/29.6% | 3.5 (interpolated) | pass | 0.152 (unverified) | n/a |
| 26 | `cfg_a284` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 83/92/53 | 228 | 37.8% | 6.6% | 1.02 | -7.4% | 208 | 1.45 | 8.4% | 35.3 | 6/6 | 1.00 | 0.67 | 0.34 | 5 | 21.4% | 0.38 | 0.40 | 32.6% | 25.7% | 19.0% | 33.3%/25.3% | 4.4 (interpolated) | pass | 0.304 (unverified) | n/a |
| 27 | `cfg_b9ea` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/736/513 | 1249 | 151.0% | 20.2% | 0.96 | -20.3% | 228 | 1.17 | 49.8% | 204.7 | 6/6 | 0.67 | 0.44 | 0.53 | 5 | 86.4% | 0.43 | 0.47 | 92.7% | 47.3% | 52.6% | 133.6%/89.1% | 2.8 (interpolated) | pass | 0.256 (unverified) | n/a |
| 28 | `cfg_12af` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=1, stop=box, target_r=1.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 38/104/22 | 164 | 29.2% | 5.3% | 1.00 | -5.9% | 215 | 1.55 | 6.3% | 25.3 | 6/6 | 0.83 | 0.61 | 0.39 | 4 | 11.1% | 0.58 | 0.46 | 25.5% | 21.7% | 9.3% | 27.1%/22.4% | 4.9 (interpolated) | pass | 0.301 (unverified) | n/a |
| 29 | `cfg_e918` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 56/65/28 | 149 | 24.9% | 4.6% | 0.98 | -5.0% | 153 | 1.52 | 5.7% | 22.8 | 6/6 | 0.83 | 0.80 | 0.18 | 5 | 15.7% | 0.34 | 0.40 | 20.7% | 17.5% | 19.7% | 22.3%/18.0% | 4.6 (interpolated) | pass | 0.281 (unverified) | n/a |
| 30 | `cfg_f244` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.0 | 0/155/44 | 199 | 39.0% | 6.8% | 0.75 | -10.8% | 192 | 1.48 | 9.5% | 30.6 | 5/5 | 0.80 | 0.68 | 0.07 | 5 | 20.8% | 0.40 | 0.77 | 32.7% | 28.0% | 22.8% | 35.2%/22.9% | 5.0 (interpolated) | pass | 0.094 (unverified) | n/a |
| 31 | `cfg_c1ef` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=both, trend_filter=none, min_box_atr=0.0 | 294/357/716 | 1367 | 131.0% | 18.3% | 1.04 | -13.4% | 159 | 1.17 | 37.6% | 220.5 | 7/7 | 0.57 | 0.31 | 0.73 | 5 | 78.6% | 0.40 | 0.38 | 72.3% | 29.3% | 6.8% | 110.8%/82.7% | 2.5 (interpolated) | pass | 0.314 (unverified) | n/a |
| 32 | `cfg_4733` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 64/98/44 | 206 | 25.4% | 4.6% | 0.76 | -7.8% | 160 | 1.36 | 7.7% | 31.4 | 5/5 | 0.80 | 0.63 | 0.13 | 4 | 13.3% | 0.42 | 0.53 | 19.9% | 15.3% | -1.2% | 23.0%/16.5% | 3.6 (interpolated) | pass | 0.136 (unverified) | n/a |
| 33 | `cfg_8a05` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=4, stop=box, target_r=1.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 25/86/12 | 123 | 22.1% | 4.1% | 0.95 | -5.2% | 312 | 1.62 | 4.6% | 19.1 | 6/6 | 0.83 | 0.55 | 0.40 | 3 | 7.5% | 0.64 | 0.52 | 18.8% | 15.9% | 11.0% | 18.8%/15.0% | 4.9 (interpolated) | pass | 0.249 (unverified) | n/a |
| 34 | `cfg_b74c` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=4, stop=1.5, target_r=2.5, direction=both, trend_filter=none, min_box_atr=0.0 | 39/216/150 | 405 | 48.4% | 8.2% | 0.76 | -11.3% | 360 | 1.26 | 13.8% | 59.7 | 7/7 | 0.86 | 0.53 | 0.23 | 5 | 32.6% | 0.33 | 0.62 | 36.2% | 24.1% | 24.1% | 41.7%/29.0% | 3.3 (interpolated) | pass | 0.128 (unverified) | n/a |
| 35 | `cfg_66e4` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=1, stop=box, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 46/116/32 | 194 | 27.4% | 5.0% | 0.85 | -6.2% | 463 | 1.41 | 7.5% | 29.4 | 6/6 | 0.83 | 0.50 | 0.35 | 5 | 11.1% | 0.54 | 0.48 | 21.7% | 16.7% | 3.9% | 24.2%/18.9% | 4.0 (interpolated) | pass | 0.206 (unverified) | n/a |
| 36 | `cfg_7e70` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=1, stop=box, target_r=1.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 24/78/12 | 114 | 16.3% | 3.1% | 0.78 | -5.3% | 454 | 1.49 | 4.3% | 17.8 | 6/6 | 0.83 | 0.66 | 0.12 | 3 | 6.4% | 0.59 | 0.57 | 13.6% | 10.8% | 14.2% | 14.4%/10.5% | 4.3 (interpolated) | pass | 0.153 (unverified) | n/a |
| 37 | `cfg_1a6f` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 62/96/41 | 199 | 25.5% | 4.7% | 0.78 | -7.1% | 153 | 1.37 | 7.5% | 30.5 | 5/5 | 0.60 | 0.68 | 0.10 | 4 | 12.9% | 0.44 | 0.53 | 20.5% | 15.5% | -0.0% | 23.1%/17.9% | 3.8 (interpolated) | pass | 0.142 (unverified) | n/a |
| 38 | `cfg_43f4` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 48/70/32 | 150 | 22.2% | 4.1% | 0.84 | -5.5% | 284 | 1.44 | 5.6% | 23.7 | 6/6 | 0.83 | 0.80 | 0.04 | 5 | 11.9% | 0.47 | 0.48 | 18.8% | 14.9% | 14.5% | 20.7%/16.6% | 4.3 (interpolated) | pass | 0.182 (unverified) | n/a |
| 39 | `cfg_5a5b` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=none, direction=both, trend_filter=ema50, min_box_atr=0.0 | 0/392/283 | 675 | 75.8% | 12.0% | 0.79 | -18.7% | 349 | 1.22 | 25.9% | 108.3 | 6/6 | 0.83 | 0.58 | 0.21 | 4 | 34.9% | 0.54 | 0.58 | 51.9% | 30.6% | 42.5% | 66.9%/46.8% | 3.0 (interpolated) | pass | 0.144 (unverified) | n/a |
| 40 | `cfg_1f3f` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=1.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 57/21/31 | 109 | 16.2% | 3.0% | 0.86 | -3.0% | 195 | 1.54 | 2.7% | 16.5 | 6/6 | 0.83 | 0.33 | 0.53 | 5 | 8.2% | 0.49 | 0.55 | 13.4% | 10.7% | 4.7% | 15.1%/11.2% | 4.3 (interpolated) | pass | 0.195 (unverified) | n/a |
| 41 | `cfg_5952` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.5, direction=both, trend_filter=ema50, min_box_atr=0.0 | 86/314/284 | 684 | 70.4% | 11.3% | 0.77 | -20.1% | 378 | 1.21 | 23.1% | 109.5 | 7/7 | 0.71 | 0.61 | 0.16 | 4 | 25.3% | 0.64 | 0.56 | 46.7% | 27.6% | 27.3% | 61.1%/39.4% | 2.9 (interpolated) | pass | 0.133 (unverified) | n/a |
| 42 | `cfg_71dc` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=both, trend_filter=ema50, min_box_atr=0.0 | 67/86/44 | 197 | 25.0% | 4.6% | 0.76 | -6.8% | 335 | 1.33 | 6.6% | 27.6 | 6/6 | 1.00 | 0.58 | 0.18 | 5 | 16.5% | 0.34 | 0.51 | 19.3% | 14.1% | 9.8% | 22.7%/15.7% | 3.5 (interpolated) | pass | 0.136 (unverified) | n/a |
| 43 | `cfg_b05a` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 363/68/272 | 703 | 61.3% | 10.0% | 1.13 | -9.2% | 143 | 1.27 | 11.8% | 112.8 | 6/6 | 0.67 | 0.10 | 1.03 | 4 | 35.1% | 0.34 | 0.37 | 39.1% | 20.5% | -3.5% | 54.2%/40.9% | 2.7 (interpolated) | pass | 0.397 (unverified) | n/a |
| 44 | `cfg_2dd7` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0 | 603/345/484 | 1432 | 125.6% | 17.7% | 0.99 | -15.0% | 138 | 1.16 | 32.6% | 226.6 | 6/6 | 0.67 | 0.34 | 0.65 | 5 | 49.2% | 0.47 | 0.46 | 66.6% | 23.8% | -6.3% | 110.8%/79.4% | 2.4 (interpolated) | pass | 0.284 (unverified) | n/a |
| 45 | `cfg_937a` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 282/191/219 | 692 | 81.0% | 12.6% | 0.94 | -13.4% | 196 | 1.26 | 16.5% | 111.5 | 6/6 | 0.83 | 0.23 | 0.71 | 5 | 25.7% | 0.58 | 0.50 | 56.7% | 35.6% | 3.0% | 70.8%/53.1% | 3.0 (interpolated) | pass | 0.214 (unverified) | n/a |
| 46 | `cfg_ae5f` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=none, direction=long, trend_filter=none, min_box_atr=0.0 | 0/225/140 | 365 | 41.0% | 7.1% | 0.82 | -17.4% | 624 | 1.29 | 14.8% | 59.1 | 7/7 | 0.86 | 0.53 | 0.29 | 3 | 18.5% | 0.55 | 0.52 | 30.9% | 21.7% | 8.2% | 36.6%/25.7% | 3.3 (interpolated) | pass | 0.159 (unverified) | n/a |
| 47 | `cfg_2885` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 54/19/31 | 104 | 13.8% | 2.6% | 0.76 | -3.0% | 232 | 1.47 | 2.5% | 15.6 | 6/6 | 1.00 | 0.50 | 0.26 | 5 | 7.0% | 0.50 | 0.63 | 11.2% | 8.9% | 3.6% | 12.0%/8.3% | 4.0 (interpolated) | pass | 0.142 (unverified) | n/a |
| 48 | `cfg_8d13` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 80/90/52 | 222 | 27.8% | 5.0% | 0.85 | -7.3% | 183 | 1.35 | 8.2% | 34.8 | 6/6 | 0.83 | 0.75 | 0.10 | 5 | 18.6% | 0.30 | 0.40 | 22.2% | 16.0% | 26.6% | 24.0%/17.4% | 3.6 (interpolated) | pass | 0.199 (unverified) | n/a |
| 49 | `cfg_f175` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0 | 759/111/591 | 1461 | 91.9% | 13.9% | 1.07 | -15.6% | 326 | 1.17 | 23.8% | 235.0 | 6/6 | 0.50 | 0.12 | 0.96 | 5 | 50.3% | 0.45 | 0.31 | 39.8% | 3.2% | -9.9% | 78.9%/62.5% | 2.1 (interpolated) | pass | 0.349 (unverified) | n/a |
| 50 | `cfg_a154` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 79/21/49 | 149 | 16.5% | 3.1% | 0.75 | -4.4% | 195 | 1.36 | 3.6% | 22.7 | 6/6 | 0.67 | 0.47 | 0.28 | 5 | 10.9% | 0.34 | 0.55 | 12.7% | 9.8% | 15.9% | 15.4%/10.2% | 3.4 (interpolated) | pass | 0.135 (unverified) | n/a |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 4.2% / 1.14 / 18 | 2.3% / 0.55 / 25 | 8.1% / 0.97 / 21 | 4.7% / 1.15 / 28 | 8.1% / 1.52 / 17 |
| 2 | 1.9% / 0.49 / 29 | 4.8% / 1.04 / 25 | 19.2% / 1.89 / 23 | -1.9% / -0.55 / 27 | 5.5% / 1.07 / 19 |
| 3 | 3.7% / 1.13 / 18 | 4.4% / 1.05 / 25 | 11.2% / 1.14 / 21 | 0.9% / 0.27 / 28 | 8.4% / 1.69 / 17 |
| 4 | 3.7% / 1.08 / 18 | 2.3% / 0.54 / 25 | 16.0% / 1.10 / 21 | 4.4% / 1.09 / 28 | 7.8% / 1.51 / 17 |
| 5 | -0.1% / -0.00 / 29 | 2.3% / 0.73 / 25 | 20.0% / 1.81 / 23 | -0.3% / -0.07 / 27 | 6.3% / 1.17 / 19 |
| 6 | 2.9% / 0.64 / 37 | 5.4% / 1.08 / 35 | 17.5% / 1.57 / 34 | 0.6% / 0.18 / 32 | 6.5% / 1.13 / 26 |
| 7 | 3.7% / 1.08 / 18 | 3.7% / 0.96 / 25 | 15.2% / 1.05 / 21 | 1.6% / 0.43 / 28 | 8.5% / 1.70 / 17 |
| 8 | 19.0% / 1.73 / 278 | 0.3% / 0.08 / 282 | 57.2% / 1.63 / 272 | 0.8% / 0.12 / 276 | 31.0% / 1.71 / 275 |
| 9 | 19.1% / 1.32 / 253 | 13.9% / 0.95 / 256 | 28.5% / 1.00 / 252 | 21.8% / 1.42 / 259 | 28.0% / 1.27 / 255 |
| 10 | 21.3% / 1.49 / 254 | 4.2% / 0.37 / 258 | 31.5% / 0.98 / 251 | 5.9% / 0.48 / 263 | 43.3% / 1.74 / 256 |
| 11 | -0.8% / -0.15 / 37 | 2.2% / 0.59 / 35 | 25.3% / 1.92 / 34 | 1.7% / 0.44 / 32 | 5.7% / 0.94 / 26 |
| 12 | 7.3% / 1.16 / 47 | 1.9% / 0.33 / 55 | 9.4% / 0.78 / 47 | 8.4% / 1.44 / 42 | 10.1% / 1.30 / 36 |
| 13 | 2.5% / 0.64 / 28 | 4.2% / 0.93 / 23 | 10.8% / 1.62 / 21 | -1.9% / -0.57 / 25 | 4.7% / 0.95 / 17 |
| 14 | 13.4% / 1.20 / 269 | 8.6% / 0.74 / 266 | 36.5% / 1.29 / 264 | 11.4% / 0.91 / 266 | 34.2% / 1.66 / 266 |
| 15 | 6.0% / 1.29 / 28 | 0.7% / 0.17 / 37 | 14.6% / 1.46 / 31 | 7.0% / 1.55 / 30 | 4.5% / 0.79 / 23 |
| 16 | 5.2% / 1.01 / 42 | -0.2% / -0.01 / 43 | 17.1% / 1.38 / 44 | 2.9% / 0.69 / 37 | 6.8% / 1.12 / 28 |
| 17 | 5.2% / 1.11 / 29 | 0.8% / 0.18 / 37 | 7.8% / 0.72 / 32 | 7.6% / 1.67 / 31 | 5.5% / 0.95 / 25 |
| 18 | 8.1% / 1.28 / 46 | 2.0% / 0.34 / 55 | 16.0% / 1.40 / 46 | 8.0% / 1.37 / 41 | 6.3% / 0.89 / 33 |
| 19 | 1.1% / 0.49 / 18 | 2.1% / 0.56 / 25 | 3.4% / 0.63 / 21 | 4.2% / 1.12 / 28 | 8.4% / 1.70 / 17 |
| 20 | 5.0% / 1.08 / 29 | 0.7% / 0.17 / 37 | 17.1% / 1.02 / 32 | 7.5% / 1.67 / 31 | 5.5% / 0.95 / 25 |
| 21 | 0.2% / 0.07 / 28 | 1.7% / 0.56 / 23 | 10.0% / 1.67 / 21 | -0.2% / -0.04 / 25 | 5.7% / 1.08 / 17 |
| 22 | 2.1% / 0.68 / 29 | 1.8% / 0.41 / 37 | 13.9% / 1.65 / 32 | 6.6% / 1.66 / 31 | 5.3% / 0.96 / 25 |
| 23 | 1.2% / 0.24 / 42 | -1.6% / -0.31 / 43 | 24.4% / 1.74 / 44 | 2.3% / 0.50 / 37 | 6.4% / 1.01 / 28 |
| 24 | 14.2% / 1.01 / 261 | 8.0% / 0.59 / 265 | 20.3% / 0.78 / 255 | 26.2% / 1.63 / 264 | 23.4% / 1.09 / 262 |
| 25 | 8.1% / 1.06 / 87 | 1.7% / 0.26 / 82 | 17.9% / 1.06 / 89 | 6.1% / 0.88 / 69 | 8.8% / 0.91 / 57 |
| 26 | 1.2% / 0.29 / 47 | 4.3% / 0.73 / 55 | 13.5% / 1.45 / 47 | 5.5% / 1.15 / 43 | 9.0% / 1.24 / 36 |
| 27 | 22.8% / 1.43 / 245 | 5.4% / 0.43 / 253 | 28.8% / 0.92 / 246 | 11.8% / 0.80 / 256 | 34.6% / 1.42 / 249 |
| 28 | -1.3% / -0.24 / 37 | 4.7% / 1.11 / 35 | 16.4% / 2.18 / 34 | 3.3% / 0.79 / 32 | 4.0% / 0.73 / 26 |
| 29 | 2.8% / 0.93 / 28 | 1.8% / 0.41 / 37 | 8.0% / 1.32 / 31 | 6.0% / 1.53 / 30 | 4.4% / 0.82 / 23 |
| 30 | 1.8% / 0.41 / 39 | 1.4% / 0.27 / 43 | 15.1% / 0.90 / 37 | 9.2% / 1.42 / 44 | 7.1% / 1.09 / 36 |
| 31 | 8.7% / 0.82 / 277 | 7.1% / 0.61 / 278 | 34.5% / 1.21 / 267 | 14.1% / 1.08 / 271 | 29.3% / 1.43 / 274 |
| 32 | -0.0% / 0.01 / 39 | 0.2% / 0.07 / 44 | 10.7% / 1.13 / 39 | 7.1% / 1.26 / 47 | 5.5% / 0.95 / 37 |
| 33 | -0.4% / -0.08 / 29 | 4.3% / 1.26 / 25 | 13.6% / 2.27 / 23 | -0.3% / -0.05 / 27 | 3.7% / 0.87 / 19 |
| 34 | 9.5% / 1.20 / 90 | 1.8% / 0.26 / 83 | 10.1% / 0.60 / 96 | 8.1% / 1.15 / 73 | 11.9% / 1.17 / 63 |
| 35 | 0.3% / 0.09 / 42 | 1.3% / 0.29 / 43 | 14.7% / 1.78 / 44 | 4.4% / 0.89 / 37 | 4.7% / 0.81 / 28 |
| 36 | -0.0% / 0.01 / 28 | 3.7% / 1.10 / 23 | 9.3% / 1.98 / 21 | -0.5% / -0.10 / 25 | 3.1% / 0.74 / 17 |
| 37 | -0.0% / 0.01 / 39 | 1.0% / 0.22 / 43 | 11.1% / 1.20 / 37 | 6.4% / 1.16 / 44 | 5.2% / 0.89 / 36 |
| 38 | 2.7% / 0.94 / 29 | 4.1% / 0.79 / 37 | 0.5% / 0.11 / 27 | 4.1% / 0.97 / 33 | 9.3% / 1.59 / 24 |
| 39 | 12.5% / 1.14 / 138 | -11.7% / -1.08 / 135 | 21.9% / 0.94 / 135 | 11.3% / 0.98 / 138 | 30.3% / 1.63 / 129 |
| 40 | 1.4% / 0.66 / 18 | 3.6% / 1.25 / 25 | 1.6% / 0.33 / 21 | 1.4% / 0.45 / 28 | 7.4% / 1.97 / 17 |
| 41 | 11.4% / 1.13 / 142 | -13.8% / -1.44 / 137 | 21.6% / 0.91 / 136 | 7.2% / 0.72 / 139 | 36.0% / 1.98 / 130 |
| 42 | 0.7% / 0.18 / 35 | 2.1% / 0.45 / 39 | 6.5% / 0.76 / 53 | 6.3% / 1.25 / 41 | 7.3% / 1.13 / 29 |
| 43 | -1.0% / -0.18 / 136 | 9.0% / 1.53 / 145 | 19.4% / 1.39 / 136 | 14.4% / 2.07 / 143 | 9.5% / 0.94 / 143 |
| 44 | 13.5% / 1.25 / 287 | 2.1% / 0.24 / 298 | 51.2% / 1.48 / 277 | 0.6% / 0.11 / 286 | 27.9% / 1.52 / 284 |
| 45 | 5.1% / 0.71 / 134 | 2.3% / 0.34 / 143 | 44.1% / 1.58 / 133 | 10.0% / 1.31 / 142 | 6.3% / 0.59 / 140 |
| 46 | -1.6% / -0.23 / 70 | -0.3% / 0.01 / 87 | 12.4% / 1.15 / 71 | 7.5% / 1.07 / 71 | 19.0% / 1.57 / 66 |
| 47 | 1.7% / 0.84 / 17 | 2.9% / 1.04 / 23 | 1.7% / 0.34 / 21 | 0.6% / 0.19 / 27 | 6.4% / 1.76 / 16 |
| 48 | 1.9% / 0.45 / 46 | 4.3% / 0.73 / 55 | 7.8% / 1.08 / 46 | 5.1% / 1.07 / 42 | 6.1% / 0.90 / 33 |
| 49 | 2.2% / 0.32 / 295 | 4.6% / 0.53 / 299 | 17.5% / 0.95 / 289 | 19.7% / 1.89 / 288 | 27.7% / 1.67 / 290 |
| 50 | 2.5% / 0.98 / 28 | 3.3% / 0.90 / 37 | 2.1% / 0.37 / 31 | 2.6% / 0.74 / 30 | 5.1% / 1.15 / 23 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_2706` | 7 | 0.84 | 0.80/0.87 | 0.49/0.66 |
| 1 | `cfg_ac55` | 6 | 0.91 | 0.93/0.98 | 0.72/0.82 |
| 2 | `cfg_8e07` | 2 | 0.95 | 0.96/0.96 | 0.95/0.95 |
| 3 | `cfg_12af` | 3 | 0.81 | 0.85/0.87 | 0.61/0.72 |
| 4 | `cfg_1042` | 2 | 0.91 | 0.92/0.92 | 0.94/0.94 |
| 5 | `cfg_4733` | 2 | 0.99 | 0.98/0.98 | 0.98/0.98 |
| 6 | `cfg_c1d4` | 7 | 0.89 | 0.89/0.93 | 0.69/0.79 |
| 7 | `cfg_1f3f` | 2 | 0.98 | 0.98/0.98 | 0.93/0.93 |
| 8 | `cfg_9f98` | 3 | 0.95 | 0.92/0.92 | 0.79/0.79 |
| 9 | `cfg_7a1a` | 4 | 0.87 | 0.91/0.95 | 0.86/0.89 |
| 10 | `cfg_d03e` | 4 | 0.87 | 0.84/0.93 | 0.70/0.95 |
| 11 | `cfg_4bc5` | 2 | 0.94 | 0.95/0.95 | 0.96/0.96 |
| 12 | `cfg_8a05` | 3 | 0.85 | 0.92/0.92 | 0.88/0.90 |
| 13 | `cfg_e074` | 3 | 0.81 | 0.84/0.91 | 0.73/0.84 |
| 14 | `cfg_49e5` | 7 | 0.82 | 0.85/0.91 | 0.61/0.74 |
| 15 | `cfg_e92e` | 4 | 0.94 | 0.91/0.93 | 0.79/0.80 |
| 16 | `cfg_5a5b` | 2 | 0.95 | 0.95/0.95 | 0.88/0.88 |
| 17 | `cfg_5beb` | 2 | 0.88 | 0.88/0.88 | 0.97/0.97 |
| 18 | `cfg_71dc` | 1 | n/a | n/a/n/a | n/a/n/a |
| 19 | `cfg_72d6` | 3 | 0.93 | 0.89/0.91 | 0.94/0.96 |
| 20 | `cfg_a284` | 2 | 0.90 | 0.91/0.91 | 0.98/0.98 |
| 21 | `cfg_b05a` | 2 | 0.81 | 0.68/0.68 | 0.55/0.55 |
| 22 | `cfg_a154` | 1 | n/a | n/a/n/a | n/a/n/a |
| 23 | `cfg_ae5f` | 1 | n/a | n/a/n/a | n/a/n/a |
| 24 | `cfg_fcc6` | 2 | 0.95 | 0.97/0.97 | 0.95/0.95 |
| 25 | `cfg_c28b` | 2 | 0.88 | 0.85/0.85 | 0.74/0.74 |
| 26 | `cfg_f175` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 6.691e-04 over 3840 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 462.0, participation ratio 19.4, 95%-variance components 178 (rank bound T = 1258); raw grid 3840; raw + known prior 777744
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
None results are unchanged rules on the development period: supporting evidence, not an independent replication.

## Integrity audit

- Compression at bar k uses bars through k only: bbkc = 2 x population sd(close, L) < kc_mult x Wilder ATR(L) (Bollinger 2 sd inside a Keltner channel, both centred on SMA(L)); nr = the bar's high-low range is the narrowest of the last N bars (ties count), and with inside_bar also inside the previous bar's range. Indicators run over the RTH bar series across sessions.
- A run is a maximal stretch of consecutive compression bars inside one session (never continued across the open); its box through bar r is [min low, max high] of its bars up to r. The decision at bar k uses the run holding the last compression bar r <= k-1 of k's session, live when k - r <= setup_expiry_bars, the run is at least min_squeeze_bars long (NR: 1) and the box is at least min_box_atr x ATR(14)[r] wide, so the box never includes the decision bar. A box too narrow to be live never consumes its run.
- Breakout: close entries need close_k beyond the box and fill at the NEXT bar's open (market slippage); wick entries are a stop order at the box edge, filled on bar k at the worse of its open and the edge (stop slippage); a wick bar through both edges is ambiguous and not traded. The fill bar must be in the decision's session.
- The FIRST breakout of a run decides and consumes it, traded or not (wrong direction, trend filter, inside the last 30 minutes, a position already open, a missed entry). Each setup is one decision.
- Filters known at the decision: ema50 needs close > EMA(50) for a long / < for a short (close entries at bar k, wick entries at bar k-1); no decision on the session's last bar or less than 30 minutes before its last close.
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
