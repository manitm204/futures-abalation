# Screening funnel -- cb_bbkc_gc_v4_15m (development stages only)

- Code: `36bde5f6ce84` (dirty working tree: True, diff sha256 `99d2740b6266`)
- Config: `configs/funnel/cb_bbkc_funnel_gc_v4_15m.yaml` sha256 `bdeb654f290810ba`; seed 20261112
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'GC': '2026-10-16'}
- Frozen manifest sha256: `d76e486f43011ade` (43 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **False** -- No compression-breakout strategy has been selected or scored on GC 2023-2024. This grid was chosen after reading ES, NQ and YM squeeze results on 2023-2024 and 2025+. Other families were validated there (mean-reversion: combined_test, combined_v1, mr_gc_v5, mr_gc_v6_15m, mr_gc_v6_1h, trades_v1), so the period has been looked at by the researcher, but not for this strategy.
- Holdout 2025+ previously inspected: **False** -- No compression-breakout metrics have been computed on GC 2025+. GC 2025+ bars were read for mean-reversion holdout scoring (combined_v1, trades_v1) per those families' data-access ledgers: different strategy families, so this is still the first test of this strategy, but the researcher has seen how that period treated them.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 3840 | 3840 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 3840 | 3840 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 3840 | 3216 | 624 | 0 |  | 2608 | 83.75 | 83.75 |  |
| 3 performance & risk | hard_gate | 3216 | 71 | 3145 | 0 |  | 0 | 1.85 | 2.21 |  |
| 4 parameter stability | hard_gate | 71 | 67 | 4 | 0 |  | 0 | 1.74 | 94.37 |  |
| 5 time stability | hard_gate | 67 | 67 | 0 | 0 |  | 42 | 1.74 | 100.00 |  |
| 6 deduplication | dedup | 67 | 43 |  |  | 24 |  | 1.12 | 64.18 | best 2 per cluster |
| 7 execution stress | hard_gate | 43 | 43 | 0 | 0 |  | 6 | 1.12 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 43 |  |  |  |  |  |  |  | diagnostic only: unverified: 43 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 624 |
| s2:hard_reject:years_with_>=10_trades | 348 |
| s3:hard_reject:max_drawdown | 6 |
| s3:hard_reject:net_return | 1829 |
| s3:hard_reject:sharpe | 3145 |
| s4:hard_reject:local_median_sharpe | 4 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | target/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | transfer dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_cf08` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.5, direction=both, trend_filter=none, min_box_atr=0.0 | 69/157/174 | 400 | 15.5% | 3.0% | 1.07 | -4.0% | 502 | 1.38 | 12.2% | 217.5 | 8/8 | 0.62 | 0.65 | 0.42 | 5 | 7.0% | 0.52 | 0.44 | 11.8% | 8.1% | 6.1% | 13.7%/11.3% | 3.4 (interpolated) | pass | 0.146 (unverified) | n/a |
| 2 | `cfg_4953` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=both, trend_filter=none, min_box_atr=0.0 | 70/164/181 | 415 | 14.7% | 2.8% | 0.97 | -4.1% | 500 | 1.34 | 12.8% | 226.5 | 8/8 | 0.62 | 0.67 | 0.30 | 4 | 5.1% | 0.62 | 0.51 | 11.3% | 7.8% | 5.5% | 13.3%/10.4% | 3.3 (interpolated) | pass | 0.097 (unverified) | n/a |
| 3 | `cfg_34e9` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.5, direction=both, trend_filter=ema50, min_box_atr=0.0 | 26/366/108 | 500 | 19.8% | 3.7% | 0.92 | -4.7% | 357 | 1.29 | 22.0% | 273.8 | 8/8 | 0.75 | 0.63 | 0.29 | 4 | 11.7% | 0.39 | 0.52 | 16.4% | 11.8% | 11.9% | 18.3%/14.2% | 3.6 (interpolated) | pass | 0.089 (unverified) | n/a |
| 4 | `cfg_6e71` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=both, trend_filter=ema50, min_box_atr=0.0 | 26/378/111 | 515 | 20.4% | 3.9% | 0.94 | -4.7% | 357 | 1.29 | 22.7% | 282.0 | 8/8 | 0.75 | 0.59 | 0.35 | 4 | 12.4% | 0.38 | 0.50 | 16.6% | 11.5% | 12.4% | 18.4%/14.6% | 3.6 (interpolated) | pass | 0.095 (unverified) | n/a |
| 5 | `cfg_a7ec` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/339/310 | 649 | 24.7% | 4.6% | 1.01 | -4.2% | 416 | 1.29 | 25.8% | 354.3 | 7/7 | 0.86 | 0.60 | 0.41 | 5 | 12.5% | 0.47 | 0.50 | 17.9% | 12.7% | 9.8% | 23.0%/17.8% | 3.2 (interpolated) | pass | 0.111 (unverified) | n/a |
| 6 | `cfg_a82c` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=both, trend_filter=ema50, min_box_atr=0.0 | 0/420/133 | 553 | 21.8% | 4.1% | 0.92 | -4.5% | 274 | 1.28 | 25.8% | 301.4 | 6/6 | 1.00 | 0.71 | 0.21 | 5 | 11.3% | 0.48 | 0.52 | 17.6% | 13.6% | 15.6% | 19.8%/14.8% | 3.5 (interpolated) | pass | 0.084 (unverified) | n/a |
| 7 | `cfg_0080` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.0 | 0/127/71 | 198 | 13.6% | 2.6% | 0.94 | -2.9% | 214 | 1.55 | 8.6% | 107.4 | 7/7 | 1.00 | 0.50 | 0.45 | 4 | 8.9% | 0.35 | 0.70 | 12.3% | 11.0% | 9.7% | 12.4%/9.5% | 5.7 (interpolated) | pass | 0.069 (unverified) | n/a |
| 8 | `cfg_5837` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=none, direction=both, trend_filter=ema50, min_box_atr=0.0 | 0/329/296 | 625 | 26.1% | 4.8% | 0.93 | -7.4% | 511 | 1.24 | 28.1% | 342.7 | 6/6 | 1.00 | 0.74 | 0.19 | 4 | 7.1% | 0.74 | 0.52 | 19.0% | 14.8% | 16.2% | 22.1%/17.7% | 3.5 (interpolated) | pass | 0.092 (unverified) | n/a |
| 9 | `cfg_2256` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=both, trend_filter=ema50, min_box_atr=0.0 | 0/410/129 | 539 | 19.4% | 3.7% | 0.85 | -4.8% | 275 | 1.26 | 25.2% | 294.1 | 6/6 | 0.83 | 0.70 | 0.14 | 4 | 9.4% | 0.52 | 0.57 | 15.8% | 11.8% | 14.0% | 17.1%/13.8% | 3.3 (interpolated) | pass | 0.061 (unverified) | n/a |
| 10 | `cfg_5540` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=long, trend_filter=none, min_box_atr=0.0 | 0/192/151 | 343 | 23.8% | 4.4% | 1.25 | -3.3% | 227 | 1.58 | 13.9% | 188.3 | 7/7 | 1.00 | 0.59 | 0.66 | 5 | 15.7% | 0.32 | 0.46 | 20.1% | 16.9% | 15.0% | 20.3%/17.4% | 5.2 (interpolated) | pass | 0.247 (unverified) | n/a |
| 11 | `cfg_0fb5` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=none, direction=both, trend_filter=ema50, min_box_atr=0.0 | 0/322/291 | 613 | 26.5% | 4.9% | 0.95 | -7.1% | 497 | 1.25 | 27.5% | 336.2 | 6/6 | 1.00 | 0.72 | 0.23 | 4 | 7.5% | 0.71 | 0.52 | 19.8% | 15.1% | 16.3% | 22.1%/16.6% | 3.6 (interpolated) | pass | 0.098 (unverified) | n/a |
| 12 | `cfg_a76d` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.0 | 0/229/67 | 296 | 13.7% | 2.6% | 0.82 | -3.9% | 432 | 1.36 | 14.1% | 159.0 | 6/6 | 1.00 | 0.63 | 0.19 | 3 | 4.7% | 0.65 | 0.65 | 12.0% | 9.8% | 11.4% | 12.7%/10.7% | 4.2 (interpolated) | pass | 0.051 (unverified) | n/a |
| 13 | `cfg_7e34` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=3.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=long, trend_filter=none, min_box_atr=0.0 | 0/270/253 | 523 | 18.3% | 3.5% | 0.82 | -5.9% | 310 | 1.25 | 21.5% | 286.5 | 6/6 | 1.00 | 0.58 | 0.24 | 4 | 9.0% | 0.51 | 0.63 | 13.7% | 9.3% | 6.3% | 17.0%/13.1% | 3.2 (interpolated) | pass | 0.049 (unverified) | n/a |
| 14 | `cfg_90b4` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=long, trend_filter=none, min_box_atr=0.0 | 0/175/185 | 360 | 15.8% | 3.0% | 0.80 | -5.5% | 444 | 1.29 | 15.8% | 197.4 | 5/5 | 1.00 | 0.60 | 0.20 | 4 | 8.2% | 0.47 | 0.68 | 12.5% | 10.2% | 6.5% | 14.5%/11.1% | 3.8 (interpolated) | pass | 0.042 (unverified) | n/a |
| 15 | `cfg_52b1` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0 | 203/65/151 | 419 | 10.5% | 2.1% | 0.96 | -2.6% | 481 | 1.30 | 8.4% | 226.2 | 7/7 | 0.71 | 0.15 | 0.81 | 5 | 5.9% | 0.41 | 0.44 | 7.6% | 4.4% | -1.5% | 9.4%/7.7% | 2.8 (interpolated) | pass | 0.112 (unverified) | n/a |
| 16 | `cfg_d0e4` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.0 | 0/224/66 | 290 | 14.1% | 2.7% | 0.85 | -3.9% | 432 | 1.38 | 13.8% | 155.6 | 6/6 | 1.00 | 0.66 | 0.19 | 3 | 4.7% | 0.66 | 0.63 | 12.4% | 10.3% | 11.7% | 12.9%/10.5% | 4.3 (interpolated) | pass | 0.058 (unverified) | n/a |
| 17 | `cfg_2fad` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.0 | 0/122/69 | 191 | 10.0% | 1.9% | 0.77 | -3.2% | 255 | 1.43 | 8.2% | 102.3 | 7/7 | 0.86 | 0.50 | 0.27 | 4 | 5.5% | 0.42 | 0.84 | 8.2% | 6.6% | 5.9% | 9.1%/6.7% | 4.4 (interpolated) | pass | 0.032 (unverified) | n/a |
| 18 | `cfg_b596` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/642/186 | 828 | 21.1% | 4.0% | 0.79 | -9.1% | 576 | 1.18 | 38.4% | 450.3 | 7/7 | 0.86 | 0.57 | 0.22 | 4 | 4.8% | 0.79 | 0.56 | 15.5% | 7.8% | 12.1% | 19.5%/14.7% | 2.7 (interpolated) | pass | 0.049 (unverified) | n/a |
| 19 | `cfg_eaee` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.0 | 0/139/107 | 246 | 13.4% | 2.6% | 0.82 | -3.0% | 382 | 1.39 | 10.5% | 132.3 | 7/7 | 1.00 | 0.60 | 0.22 | 5 | 8.1% | 0.40 | 0.72 | 11.5% | 9.9% | 8.9% | 12.0%/9.2% | 4.6 (interpolated) | pass | 0.045 (unverified) | n/a |
| 20 | `cfg_62de` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.0 | 0/146/109 | 255 | 14.1% | 2.7% | 0.85 | -3.1% | 186 | 1.39 | 10.9% | 137.9 | 7/7 | 1.00 | 0.49 | 0.36 | 5 | 9.0% | 0.36 | 0.68 | 11.8% | 10.5% | 8.6% | 12.4%/9.4% | 4.6 (interpolated) | pass | 0.053 (unverified) | n/a |
| 21 | `cfg_d8de` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0 | 200/58/145 | 403 | 12.3% | 2.4% | 1.15 | -2.0% | 318 | 1.37 | 7.9% | 217.5 | 7/7 | 0.71 | 0.16 | 0.99 | 5 | 7.4% | 0.39 | 0.37 | 8.7% | 5.9% | -0.3% | 11.2%/8.7% | 2.9 (interpolated) | pass | 0.208 (unverified) | n/a |
| 22 | `cfg_4b3c` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.5, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=4, stop=box, target_r=none, direction=both, trend_filter=ema50, min_box_atr=0.0 | 0/510/74 | 584 | 17.2% | 3.3% | 0.76 | -6.1% | 505 | 1.22 | 25.7% | 317.4 | 6/6 | 1.00 | 0.57 | 0.19 | 3 | 3.4% | 0.77 | 0.60 | 11.4% | 6.7% | 15.1% | 13.8%/10.4% | 2.9 (interpolated) | pass | 0.042 (unverified) | n/a |
| 23 | `cfg_c76a` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/343/306 | 649 | 17.2% | 3.3% | 0.76 | -8.1% | 382 | 1.21 | 25.0% | 354.5 | 7/7 | 1.00 | 0.60 | 0.16 | 5 | 7.0% | 0.58 | 0.59 | 12.4% | 5.8% | 6.1% | 15.9%/11.6% | 2.7 (interpolated) | pass | 0.039 (unverified) | n/a |
| 24 | `cfg_d8e0` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/331/300 | 631 | 17.9% | 3.4% | 0.79 | -8.1% | 382 | 1.22 | 24.1% | 343.8 | 7/7 | 1.00 | 0.59 | 0.21 | 5 | 7.4% | 0.58 | 0.58 | 12.7% | 7.3% | 7.0% | 15.6%/11.7% | 2.8 (interpolated) | pass | 0.045 (unverified) | n/a |
| 25 | `cfg_a3fc` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=long, trend_filter=none, min_box_atr=0.0 | 0/116/85 | 201 | 13.0% | 2.5% | 0.92 | -4.2% | 310 | 1.58 | 7.9% | 108.2 | 7/7 | 0.71 | 0.44 | 0.47 | 5 | 6.3% | 0.50 | 0.78 | 11.4% | 10.0% | 8.6% | 12.0%/9.2% | 5.2 (interpolated) | pass | 0.055 (unverified) | n/a |
| 26 | `cfg_2f56` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=none, direction=long, trend_filter=none, min_box_atr=0.0 | 0/217/126 | 343 | 15.9% | 3.1% | 0.89 | -3.8% | 262 | 1.36 | 14.8% | 187.6 | 7/7 | 0.86 | 0.48 | 0.40 | 4 | 7.9% | 0.48 | 0.63 | 12.9% | 10.5% | 12.3% | 13.7%/10.7% | 4.0 (interpolated) | pass | 0.062 (unverified) | n/a |
| 27 | `cfg_137e` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/332/301 | 633 | 22.2% | 4.2% | 0.96 | -5.2% | 446 | 1.28 | 25.1% | 346.9 | 7/7 | 0.86 | 0.59 | 0.37 | 5 | 11.8% | 0.45 | 0.51 | 15.8% | 10.5% | 6.9% | 19.9%/13.4% | 3.0 (interpolated) | pass | 0.090 (unverified) | n/a |
| 28 | `cfg_6ebd` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=2.5, direction=long, trend_filter=ema50, min_box_atr=0.0 | 27/100/71 | 198 | 9.3% | 1.8% | 0.80 | -3.8% | 448 | 1.40 | 7.4% | 105.3 | 8/8 | 0.75 | 0.36 | 0.44 | 4 | 5.9% | 0.37 | 0.70 | 7.6% | 6.3% | 6.1% | 8.3%/6.0% | 4.1 (interpolated) | pass | 0.041 (unverified) | n/a |
| 29 | `cfg_649e` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.0 | 0/115/83 | 198 | 17.0% | 3.3% | 1.17 | -1.9% | 145 | 1.75 | 8.1% | 107.7 | 7/7 | 1.00 | 0.63 | 0.53 | 5 | 11.8% | 0.31 | 0.56 | 15.4% | 13.6% | 11.5% | 15.2%/12.3% | 6.7 (interpolated) | pass | 0.174 (unverified) | n/a |
| 30 | `cfg_0d18` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 72/124/147 | 343 | 13.8% | 2.7% | 0.96 | -3.1% | 272 | 1.36 | 11.0% | 187.9 | 8/8 | 0.75 | 0.41 | 0.55 | 5 | 9.4% | 0.30 | 0.55 | 11.4% | 8.6% | 10.0% | 12.4%/9.8% | 3.7 (interpolated) | pass | 0.091 (unverified) | n/a |
| 31 | `cfg_2ad0` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.0 | 0/110/81 | 191 | 13.0% | 2.5% | 1.01 | -1.7% | 145 | 1.62 | 7.7% | 101.9 | 7/7 | 0.86 | 0.51 | 0.50 | 5 | 7.4% | 0.40 | 0.64 | 11.7% | 10.0% | 7.4% | 11.9%/9.1% | 5.5 (interpolated) | pass | 0.091 (unverified) | n/a |
| 32 | `cfg_d002` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 101/35/68 | 204 | 6.2% | 1.2% | 0.75 | -1.6% | 162 | 1.35 | 4.2% | 107.3 | 7/7 | 0.57 | 0.03 | 0.72 | 5 | 4.6% | 0.26 | 0.74 | 4.5% | 3.1% | -0.4% | 5.6%/4.0% | 3.1 (interpolated) | pass | 0.041 (unverified) | n/a |
| 33 | `cfg_91be` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=long, trend_filter=ema50, min_box_atr=0.0 | 44/72/82 | 198 | 10.5% | 2.1% | 0.94 | -2.1% | 445 | 1.49 | 6.3% | 105.8 | 8/8 | 0.88 | 0.24 | 0.70 | 5 | 6.2% | 0.38 | 0.65 | 8.8% | 7.3% | 7.3% | 9.2%/7.0% | 4.5 (interpolated) | pass | 0.073 (unverified) | n/a |
| 34 | `cfg_6ed2` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.0 | 0/180/98 | 278 | 11.2% | 2.2% | 0.76 | -3.7% | 370 | 1.34 | 10.9% | 148.2 | 7/7 | 1.00 | 0.49 | 0.27 | 4 | 6.3% | 0.44 | 0.79 | 9.3% | 7.7% | 7.1% | 10.0%/7.8% | 3.8 (interpolated) | pass | 0.034 (unverified) | n/a |
| 35 | `cfg_48cc` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 167/61/120 | 348 | 7.8% | 1.5% | 0.77 | -1.8% | 251 | 1.25 | 7.3% | 187.9 | 7/7 | 0.71 | 0.24 | 0.53 | 5 | 5.0% | 0.34 | 0.61 | 5.2% | 2.5% | -0.8% | 6.9%/5.1% | 2.5 (interpolated) | pass | 0.047 (unverified) | n/a |
| 36 | `cfg_5bef` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 69/122/143 | 334 | 11.5% | 2.2% | 0.87 | -3.1% | 272 | 1.32 | 10.7% | 181.8 | 8/8 | 0.88 | 0.45 | 0.43 | 5 | 7.2% | 0.36 | 0.57 | 9.2% | 6.2% | 7.8% | 10.5%/8.9% | 3.2 (interpolated) | pass | 0.063 (unverified) | n/a |
| 37 | `cfg_4b04` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=none, direction=both, trend_filter=ema50, min_box_atr=0.0 | 0/267/218 | 485 | 16.4% | 3.1% | 0.77 | -5.0% | 263 | 1.22 | 20.6% | 266.3 | 7/7 | 1.00 | 0.53 | 0.24 | 5 | 9.5% | 0.40 | 0.63 | 12.0% | 8.4% | 16.1% | 14.5%/10.3% | 3.1 (interpolated) | pass | 0.040 (unverified) | n/a |
| 38 | `cfg_303a` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 98/31/64 | 193 | 6.2% | 1.2% | 0.79 | -1.8% | 188 | 1.38 | 4.0% | 101.4 | 7/7 | 0.57 | 0.03 | 0.76 | 5 | 4.9% | 0.21 | 0.72 | 4.6% | 3.2% | 0.1% | 5.7%/4.0% | 3.2 (interpolated) | pass | 0.048 (unverified) | n/a |
| 39 | `cfg_6d5c` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/288/283 | 571 | 18.8% | 3.6% | 0.79 | -8.2% | 461 | 1.22 | 24.1% | 313.1 | 6/6 | 1.00 | 0.60 | 0.19 | 3 | 6.7% | 0.66 | 0.60 | 14.1% | 9.3% | 2.4% | 17.1%/13.2% | 3.0 (interpolated) | pass | 0.045 (unverified) | n/a |
| 40 | `cfg_9e06` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0 | 324/98/239 | 661 | 11.2% | 2.2% | 0.79 | -3.0% | 315 | 1.17 | 13.3% | 363.2 | 7/7 | 0.57 | 0.23 | 0.56 | 4 | 5.7% | 0.49 | 0.43 | 5.7% | 0.6% | -7.7% | 10.3%/8.0% | 2.1 (interpolated) | pass | 0.056 (unverified) | n/a |
| 41 | `cfg_0060` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/281/281 | 562 | 18.1% | 3.4% | 0.77 | -9.4% | 461 | 1.21 | 23.5% | 308.6 | 6/6 | 1.00 | 0.55 | 0.22 | 3 | 5.9% | 0.70 | 0.62 | 13.4% | 8.4% | 2.3% | 15.9%/11.0% | 3.0 (interpolated) | pass | 0.041 (unverified) | n/a |
| 42 | `cfg_4d5d` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=both, trend_filter=ema50, min_box_atr=0.0 | 0/198/173 | 371 | 13.7% | 2.6% | 0.76 | -4.2% | 565 | 1.29 | 14.9% | 201.8 | 7/7 | 0.86 | 0.59 | 0.17 | 5 | 8.7% | 0.35 | 0.82 | 11.0% | 8.4% | 5.8% | 12.5%/9.6% | 3.5 (interpolated) | pass | 0.032 (unverified) | n/a |
| 43 | `cfg_2acb` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0 | 196/50/135 | 381 | 11.4% | 2.2% | 0.95 | -2.6% | 266 | 1.29 | 8.1% | 209.4 | 6/6 | 0.67 | 0.09 | 0.86 | 4 | 4.8% | 0.57 | 0.38 | 7.8% | 5.3% | -2.7% | 9.9%/7.7% | 2.9 (interpolated) | pass | 0.109 (unverified) | n/a |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 0.8% / 0.37 / 76 | 0.0% / 0.02 / 84 | 8.0% / 2.31 / 71 | 5.7% / 1.67 / 93 | 0.5% / 0.19 / 76 |
| 2 | 0.1% / 0.04 / 80 | -0.5% / -0.26 / 88 | 9.2% / 2.27 / 74 | 4.9% / 1.46 / 95 | 0.7% / 0.28 / 78 |
| 3 | 1.7% / 0.61 / 94 | 6.0% / 2.11 / 101 | 7.3% / 1.30 / 98 | -1.6% / -0.36 / 100 | 5.3% / 1.24 / 107 |
| 4 | 2.0% / 0.73 / 95 | 5.8% / 1.97 / 109 | 7.2% / 1.29 / 98 | -1.4% / -0.32 / 103 | 5.6% / 1.29 / 110 |
| 5 | 2.6% / 0.84 / 130 | 3.6% / 1.15 / 126 | 10.9% / 1.63 / 130 | 2.0% / 0.52 / 137 | 3.7% / 0.78 / 126 |
| 6 | 0.4% / 0.15 / 105 | 3.0% / 0.97 / 124 | 6.7% / 1.15 / 103 | 0.9% / 0.21 / 109 | 9.5% / 1.90 / 112 |
| 7 | -0.4% / -0.27 / 35 | 4.2% / 2.07 / 29 | 4.1% / 1.05 / 50 | 0.7% / 0.29 / 45 | 4.4% / 1.33 / 39 |
| 8 | 5.9% / 1.71 / 111 | 2.1% / 0.56 / 123 | 17.8% / 2.22 / 128 | -4.9% / -1.14 / 134 | 4.1% / 0.76 / 129 |
| 9 | 1.1% / 0.39 / 100 | 3.0% / 0.97 / 122 | 6.3% / 1.09 / 102 | -1.1% / -0.23 / 107 | 9.2% / 1.86 / 108 |
| 10 | 1.8% / 0.74 / 70 | 6.1% / 2.40 / 53 | 7.0% / 1.41 / 72 | 2.3% / 0.78 / 77 | 4.8% / 1.18 / 71 |
| 11 | 4.9% / 1.50 / 108 | 1.9% / 0.51 / 120 | 17.6% / 2.19 / 127 | -4.5% / -1.06 / 132 | 5.4% / 1.00 / 126 |
| 12 | -0.8% / -0.34 / 51 | 3.4% / 1.48 / 68 | -0.4% / -0.06 / 67 | 2.6% / 0.92 / 54 | 8.5% / 2.31 / 56 |
| 13 | 3.4% / 1.16 / 95 | 4.7% / 1.54 / 95 | 8.6% / 1.42 / 121 | -1.5% / -0.44 / 98 | 2.2% / 0.47 / 114 |
| 14 | 2.6% / 0.96 / 66 | 3.7% / 1.44 / 63 | 7.0% / 1.40 / 72 | -3.5% / -1.03 / 83 | 5.4% / 1.16 / 76 |
| 15 | 0.1% / 0.10 / 81 | 0.2% / 0.16 / 88 | 4.3% / 1.80 / 75 | 3.8% / 1.43 / 95 | 1.7% / 0.79 / 80 |
| 16 | -0.8% / -0.33 / 49 | 3.4% / 1.48 / 68 | -0.4% / -0.06 / 67 | 2.5% / 0.90 / 53 | 9.0% / 2.44 / 53 |
| 17 | -0.4% / -0.32 / 34 | 4.2% / 2.07 / 29 | 1.8% / 0.57 / 49 | 0.5% / 0.24 / 43 | 3.6% / 1.12 / 36 |
| 18 | 1.7% / 0.54 / 158 | 5.4% / 1.50 / 170 | 15.5% / 1.98 / 167 | -4.6% / -1.01 / 164 | 2.5% / 0.49 / 169 |
| 19 | 1.8% / 1.03 / 41 | 2.2% / 1.03 / 38 | 3.8% / 0.78 / 69 | 0.0% / 0.03 / 51 | 5.0% / 1.47 / 47 |
| 20 | 1.8% / 1.03 / 41 | 2.3% / 1.07 / 40 | 4.1% / 0.84 / 70 | 0.6% / 0.23 / 55 | 4.7% / 1.38 / 49 |
| 21 | 0.5% / 0.34 / 77 | 0.8% / 0.51 / 84 | 4.3% / 1.95 / 72 | 4.6% / 1.71 / 93 | 1.6% / 0.78 / 77 |
| 22 | -0.8% / -0.29 / 96 | 0.4% / 0.14 / 121 | 13.3% / 2.09 / 125 | -1.8% / -0.39 / 111 | 5.8% / 1.24 / 131 |
| 23 | 1.3% / 0.44 / 118 | 4.2% / 1.18 / 135 | 9.5% / 1.60 / 119 | 1.4% / 0.32 / 148 | 0.1% / 0.05 / 129 |
| 24 | 1.1% / 0.38 / 116 | 4.8% / 1.36 / 130 | 9.8% / 1.64 / 115 | 1.0% / 0.25 / 143 | 0.4% / 0.11 / 127 |
| 25 | 1.4% / 0.75 / 31 | 2.2% / 1.38 / 33 | 6.3% / 1.48 / 42 | 0.4% / 0.16 / 51 | 2.3% / 0.83 / 44 |
| 26 | -1.4% / -0.69 / 70 | 5.0% / 1.82 / 53 | 7.4% / 1.50 / 72 | 1.0% / 0.36 / 77 | 3.2% / 0.83 / 71 |
| 27 | 3.1% / 0.99 / 128 | 4.2% / 1.33 / 123 | 9.3% / 1.54 / 127 | 1.6% / 0.43 / 135 | 2.4% / 0.53 / 120 |
| 28 | -0.2% / -0.12 / 35 | 3.4% / 2.15 / 29 | 2.3% / 0.71 / 50 | 0.4% / 0.18 / 45 | 3.2% / 1.25 / 39 |
| 29 | 0.2% / 0.14 / 35 | 5.2% / 2.60 / 29 | 3.3% / 0.88 / 50 | 2.7% / 1.05 / 45 | 4.7% / 1.41 / 39 |
| 30 | 1.4% / 0.63 / 70 | 4.1% / 2.28 / 53 | 3.8% / 1.01 / 72 | 1.3% / 0.54 / 77 | 2.6% / 0.86 / 71 |
| 31 | 0.1% / 0.10 / 34 | 5.2% / 2.60 / 29 | 1.0% / 0.33 / 49 | 2.2% / 0.95 / 43 | 4.0% / 1.25 / 36 |
| 32 | 1.4% / 1.17 / 31 | 1.1% / 1.44 / 33 | 1.2% / 0.63 / 43 | 0.8% / 0.39 / 51 | 1.5% / 0.89 / 46 |
| 33 | 0.4% / 0.32 / 35 | 4.0% / 2.91 / 29 | 1.8% / 0.56 / 50 | 1.0% / 0.53 / 45 | 2.9% / 1.20 / 39 |
| 34 | -1.0% / -0.47 / 47 | 3.6% / 1.66 / 58 | 2.8% / 0.71 / 63 | 0.9% / 0.41 / 50 | 4.6% / 1.39 / 60 |
| 35 | 1.8% / 1.11 / 71 | 2.6% / 1.96 / 55 | 0.5% / 0.21 / 73 | 2.3% / 1.03 / 77 | 0.4% / 0.21 / 72 |
| 36 | 1.4% / 0.60 / 69 | 4.1% / 2.29 / 53 | 2.3% / 0.71 / 70 | 1.0% / 0.43 / 75 | 2.4% / 0.83 / 67 |
| 37 | 3.1% / 1.18 / 90 | 3.0% / 0.96 / 89 | 6.2% / 1.08 / 107 | 0.7% / 0.19 / 108 | 2.4% / 0.62 / 91 |
| 38 | 1.3% / 1.09 / 28 | 1.2% / 1.52 / 32 | 1.1% / 0.70 / 40 | 1.2% / 0.60 / 49 | 1.2% / 0.72 / 44 |
| 39 | 3.6% / 1.02 / 114 | 5.2% / 1.53 / 112 | 11.4% / 1.77 / 113 | -0.6% / -0.11 / 127 | -1.6% / -0.33 / 105 |
| 40 | 2.1% / 1.04 / 132 | 2.2% / 1.08 / 130 | 5.2% / 1.54 / 132 | 2.5% / 0.83 / 139 | -1.3% / -0.46 / 128 |
| 41 | 3.7% / 1.06 / 112 | 5.5% / 1.60 / 111 | 11.6% / 1.80 / 110 | -2.0% / -0.48 / 124 | -1.3% / -0.26 / 105 |
| 42 | 0.9% / 0.43 / 73 | 3.5% / 1.57 / 62 | 4.6% / 0.90 / 77 | 0.8% / 0.27 / 85 | 3.3% / 0.87 / 74 |
| 43 | 0.5% / 0.36 / 80 | 2.9% / 1.60 / 78 | 6.3% / 2.35 / 70 | 3.0% / 1.08 / 81 | -1.6% / -0.58 / 72 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_34e9` | 10 | 0.83 | 0.87/0.88 | 0.73/0.78 |
| 1 | `cfg_6d5c` | 2 | 0.99 | 0.99/0.99 | 0.97/0.97 |
| 2 | `cfg_a76d` | 4 | 0.89 | 0.91/0.92 | 0.73/0.76 |
| 3 | `cfg_0080` | 2 | 0.91 | 0.93/0.93 | 0.85/0.85 |
| 4 | `cfg_5540` | 3 | 0.82 | 0.89/0.91 | 0.80/0.88 |
| 5 | `cfg_0d18` | 2 | 0.93 | 0.93/0.93 | 0.97/0.97 |
| 6 | `cfg_5837` | 4 | 0.94 | 0.92/0.93 | 0.83/0.85 |
| 7 | `cfg_b596` | 5 | 0.85 | 0.73/0.77 | 0.47/0.50 |
| 8 | `cfg_a7ec` | 4 | 0.86 | 0.84/0.90 | 0.75/0.78 |
| 9 | `cfg_cf08` | 4 | 0.88 | 0.84/0.89 | 0.76/0.79 |
| 10 | `cfg_a82c` | 6 | 0.89 | 0.90/0.95 | 0.80/0.93 |
| 11 | `cfg_2acb` | 1 | n/a | n/a/n/a | n/a/n/a |
| 12 | `cfg_2fad` | 2 | 0.87 | 0.89/0.89 | 0.80/0.80 |
| 13 | `cfg_d002` | 2 | 0.98 | 0.95/0.95 | 0.93/0.93 |
| 14 | `cfg_48cc` | 1 | n/a | n/a/n/a | n/a/n/a |
| 15 | `cfg_4b04` | 1 | n/a | n/a/n/a | n/a/n/a |
| 16 | `cfg_4d5d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 17 | `cfg_52b1` | 2 | 0.98 | 0.96/0.96 | 0.94/0.94 |
| 18 | `cfg_eaee` | 2 | 0.99 | 0.99/0.99 | 0.96/0.96 |
| 19 | `cfg_649e` | 2 | 0.83 | 0.90/0.90 | 0.75/0.75 |
| 20 | `cfg_6ed2` | 1 | n/a | n/a/n/a | n/a/n/a |
| 21 | `cfg_7e34` | 2 | 0.86 | 0.86/0.86 | 0.57/0.57 |
| 22 | `cfg_9e06` | 1 | n/a | n/a/n/a | n/a/n/a |
| 23 | `cfg_a3fc` | 1 | n/a | n/a/n/a | n/a/n/a |
| 24 | `cfg_c76a` | 2 | 0.99 | 0.99/0.99 | 0.96/0.96 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 9.733e-04 over 3840 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 471.0, participation ratio 13.8, 95%-variance components 186 (rank bound T = 1239); raw grid 3840; raw + known prior 775440
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
