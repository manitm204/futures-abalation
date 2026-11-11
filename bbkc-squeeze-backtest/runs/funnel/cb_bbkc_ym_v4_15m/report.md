# Screening funnel -- cb_bbkc_ym_v4_15m (development stages only)

- Code: `36bde5f6ce84` (dirty working tree: True, diff sha256 `a1777363ebd7`)
- Config: `configs/funnel/cb_bbkc_funnel_ym_v4_15m.yaml` sha256 `54897bd6b434d834`; seed 20261112
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ES': '2026-10-16', 'YM': '2026-10-16'}
- Frozen manifest sha256: `18c335981be0724a` (59 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **False** -- No compression-breakout strategy has been selected or scored on YM 2023-2024. This grid was chosen after reading ES and NQ squeeze results on 2023-2024 and 2025+. Other families were validated there (mean-reversion: combined_test, combined_v1, mr_ym_v5, mr_ym_v6, mr_ym_v7_15m, mr_ym_v7_1h, trades_v1), so the period has been looked at by the researcher, but not for this strategy.
- Holdout 2025+ previously inspected: **False** -- No compression-breakout metrics have been computed on YM 2025+. YM 2025+ bars were read for mean-reversion holdout scoring (combined_v1, trades_v1, mr_ym_v7_15m+mr_ym_v7_1h) per those families' data-access ledgers: different strategy families, so this is still the first test of this strategy, but the researcher has seen how that period treated them.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 3840 | 3840 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 3840 | 3840 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 3840 | 3414 | 426 | 0 |  | 3293 | 88.91 | 88.91 |  |
| 3 performance & risk | hard_gate | 3414 | 140 | 3274 | 0 |  | 0 | 3.65 | 4.10 |  |
| 4 parameter stability | hard_gate | 140 | 140 | 0 | 0 |  | 0 | 3.65 | 100.00 |  |
| 5 time stability | hard_gate | 140 | 140 | 0 | 0 |  | 79 | 3.65 | 100.00 |  |
| 6 deduplication | dedup | 140 | 59 |  |  | 81 |  | 1.54 | 42.14 | best 2 per cluster |
| 7 execution stress | hard_gate | 59 | 59 | 0 | 0 |  | 0 | 1.54 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 59 |  |  |  |  |  |  |  | diagnostic only: unverified: 59 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 426 |
| s2:hard_reject:years_with_>=10_trades | 282 |
| s3:hard_reject:max_drawdown | 93 |
| s3:hard_reject:net_return | 1652 |
| s3:hard_reject:sharpe | 3274 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | target/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_7a89` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 147/240/392 | 779 | 47.0% | 8.0% | 1.27 | -6.2% | 402 | 1.36 | 24.9% | 343.4 | 7/7 | 1.00 | 0.90 | 0.37 | 4 | 25.3% | 0.38 | 0.33 | 41.9% | 37.6% | 17.8% | 42.8%/35.3% | 6.2 (interpolated) | pass | 0.533 (unverified) | 1.34 |
| 2 | `cfg_53b2` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=long, trend_filter=none, min_box_atr=0.0 | 0/364/402 | 766 | 54.2% | 9.1% | 1.30 | -6.6% | 172 | 1.38 | 27.5% | 339.0 | 6/6 | 1.00 | 0.75 | 0.54 | 5 | 29.0% | 0.38 | 0.34 | 48.1% | 41.4% | 31.5% | 49.7%/38.3% | 6.8 (interpolated) | pass | 0.556 (unverified) | 1.31 |
| 3 | `cfg_8ee3` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.0, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=4, stop=box, target_r=2.5, direction=both, trend_filter=none, min_box_atr=0.0 | 8/232/62 | 302 | 30.5% | 5.5% | 1.15 | -4.0% | 294 | 1.65 | 10.0% | 133.7 | 8/8 | 0.88 | 0.89 | 0.27 | 3 | 13.1% | 0.53 | 0.56 | 28.7% | 27.5% | 27.6% | 27.5%/21.9% | 10.1 (interpolated) | pass | 0.398 (unverified) | 1.09 |
| 4 | `cfg_158c` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 74/369/326 | 769 | 47.7% | 8.1% | 1.15 | -5.5% | 246 | 1.31 | 27.5% | 340.4 | 7/7 | 1.00 | 0.87 | 0.29 | 5 | 29.8% | 0.38 | 0.37 | 41.3% | 35.7% | 24.4% | 42.6%/33.8% | 6.0 (interpolated) | pass | 0.419 (unverified) | 0.94 |
| 5 | `cfg_5a28` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.0, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=4, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0 | 33/96/22 | 151 | 14.1% | 2.7% | 1.12 | -2.8% | 387 | 1.84 | 4.4% | 66.6 | 6/6 | 1.00 | 0.94 | 0.19 | 4 | 6.1% | 0.55 | 0.57 | 13.4% | 12.6% | 12.7% | 13.2%/10.5% | 9.8 (interpolated) | pass | 0.378 (unverified) | 0.78 |
| 6 | `cfg_da57` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.0, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=4, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/240/62 | 302 | 32.0% | 5.7% | 1.18 | -4.0% | 342 | 1.68 | 10.1% | 133.7 | 7/7 | 0.86 | 0.77 | 0.41 | 4 | 14.8% | 0.49 | 0.57 | 30.4% | 28.3% | 29.1% | 29.2%/23.8% | 10.5 (interpolated) | pass | 0.434 (unverified) | 1.10 |
| 7 | `cfg_5d34` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.0, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=1, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0 | 32/91/21 | 144 | 14.6% | 2.8% | 1.18 | -2.1% | 387 | 1.94 | 4.2% | 63.4 | 6/6 | 1.00 | 1.02 | 0.15 | 4 | 6.9% | 0.51 | 0.55 | 14.0% | 13.2% | 13.9% | 13.4%/11.5% | 10.6 (interpolated) | pass | 0.435 (unverified) | 0.52 |
| 8 | `cfg_f37a` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 418/74/324 | 816 | 27.5% | 5.0% | 1.11 | -7.1% | 402 | 1.25 | 15.7% | 362.1 | 6/6 | 1.00 | 0.63 | 0.49 | 5 | 15.3% | 0.41 | 0.28 | 23.1% | 18.0% | 10.1% | 25.4%/20.0% | 4.1 (interpolated) | pass | 0.394 (unverified) | 1.11 |
| 9 | `cfg_fc71` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=none, direction=long, trend_filter=none, min_box_atr=0.0 | 0/436/327 | 763 | 51.3% | 8.6% | 1.17 | -5.3% | 165 | 1.32 | 29.1% | 339.5 | 6/6 | 1.00 | 0.64 | 0.52 | 5 | 30.7% | 0.40 | 0.39 | 44.7% | 39.0% | 29.2% | 43.8%/35.4% | 6.3 (interpolated) | pass | 0.431 (unverified) | 0.85 |
| 10 | `cfg_3880` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=both, trend_filter=ema50, min_box_atr=0.0 | 42/60/30 | 132 | 11.2% | 2.2% | 1.00 | -1.8% | 314 | 1.76 | 3.5% | 58.2 | 6/6 | 1.00 | 0.67 | 0.33 | 3 | 4.2% | 0.61 | 0.62 | 10.5% | 9.6% | 9.3% | 9.7%/7.7% | 9.2 (interpolated) | pass | 0.285 (unverified) | 0.70 |
| 11 | `cfg_f51f` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 60/239/265 | 564 | 32.2% | 5.7% | 0.95 | -9.4% | 490 | 1.27 | 22.1% | 249.7 | 8/8 | 0.88 | 0.87 | 0.08 | 4 | 12.2% | 0.58 | 0.50 | 28.6% | 26.0% | 14.3% | 29.0%/22.5% | 6.2 (interpolated) | pass | 0.247 (unverified) | 0.75 |
| 12 | `cfg_ecd5` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=1.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 145/164/348 | 657 | 26.2% | 4.8% | 0.97 | -7.0% | 526 | 1.29 | 16.6% | 292.3 | 6/6 | 1.00 | 0.80 | 0.17 | 4 | 9.8% | 0.63 | 0.46 | 21.4% | 17.4% | 7.1% | 24.7%/19.3% | 4.6 (interpolated) | pass | 0.262 (unverified) | 0.57 |
| 13 | `cfg_bea0` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=both, trend_filter=ema50, min_box_atr=0.0 | 41/58/29 | 128 | 11.3% | 2.2% | 1.01 | -1.8% | 364 | 1.79 | 3.3% | 56.4 | 6/6 | 1.00 | 0.72 | 0.29 | 3 | 4.6% | 0.58 | 0.62 | 10.6% | 9.8% | 9.2% | 10.2%/8.1% | 9.4 (interpolated) | pass | 0.297 (unverified) | 0.63 |
| 14 | `cfg_ecb8` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 70/290/295 | 655 | 32.6% | 5.8% | 0.92 | -7.6% | 279 | 1.25 | 26.5% | 288.6 | 8/8 | 1.00 | 0.85 | 0.06 | 4 | 22.2% | 0.32 | 0.46 | 27.8% | 23.8% | 12.5% | 28.8%/20.7% | 5.5 (interpolated) | pass | 0.226 (unverified) | 0.70 |
| 15 | `cfg_bc7d` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 76/289/307 | 672 | 35.4% | 6.3% | 0.95 | -7.1% | 369 | 1.25 | 27.8% | 299.7 | 7/7 | 1.00 | 0.69 | 0.26 | 5 | 20.1% | 0.39 | 0.45 | 32.0% | 26.0% | 20.9% | 30.3%/22.9% | 5.5 (interpolated) | pass | 0.249 (unverified) | 0.83 |
| 16 | `cfg_404a` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 60/231/259 | 550 | 28.5% | 5.1% | 0.88 | -9.4% | 490 | 1.25 | 21.4% | 244.8 | 8/8 | 0.88 | 0.77 | 0.11 | 4 | 12.2% | 0.53 | 0.52 | 25.3% | 22.1% | 11.4% | 25.1%/18.0% | 5.9 (interpolated) | pass | 0.198 (unverified) | 0.79 |
| 17 | `cfg_67f0` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=both, trend_filter=none, min_box_atr=0.0 | 295/403/776 | 1474 | 55.8% | 9.3% | 1.01 | -15.1% | 338 | 1.20 | 45.5% | 654.6 | 7/7 | 1.00 | 0.61 | 0.40 | 5 | 27.9% | 0.50 | 0.30 | 45.3% | 33.7% | 9.0% | 49.9%/38.0% | 4.1 (interpolated) | pass | 0.310 (unverified) | 1.25 |
| 18 | `cfg_c1a9` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=1.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 143/174/355 | 672 | 24.7% | 4.5% | 0.90 | -8.8% | 531 | 1.26 | 17.4% | 298.4 | 6/6 | 1.00 | 0.73 | 0.17 | 4 | 9.5% | 0.62 | 0.47 | 19.5% | 16.1% | 7.0% | 22.0%/16.9% | 4.3 (interpolated) | pass | 0.217 (unverified) | 0.45 |
| 19 | `cfg_a196` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 70/285/290 | 645 | 31.5% | 5.6% | 0.89 | -7.4% | 279 | 1.24 | 26.1% | 284.5 | 8/8 | 1.00 | 0.80 | 0.09 | 4 | 19.9% | 0.32 | 0.48 | 26.8% | 22.6% | 11.7% | 28.4%/19.9% | 5.4 (interpolated) | pass | 0.210 (unverified) | 0.75 |
| 20 | `cfg_35a3` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=2.5, direction=both, trend_filter=none, min_box_atr=0.0 | 178/630/646 | 1454 | 53.5% | 9.0% | 0.93 | -18.6% | 550 | 1.17 | 50.9% | 643.2 | 7/7 | 0.86 | 0.54 | 0.39 | 3 | 22.9% | 0.57 | 0.32 | 41.0% | 31.5% | 40.9% | 47.9%/34.8% | 4.0 (interpolated) | pass | 0.251 (unverified) | 0.81 |
| 21 | `cfg_ed1e` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 76/286/304 | 666 | 35.5% | 6.3% | 0.95 | -7.1% | 369 | 1.25 | 27.5% | 296.9 | 7/7 | 1.00 | 0.68 | 0.28 | 5 | 20.6% | 0.38 | 0.45 | 32.0% | 26.4% | 21.7% | 30.4%/25.0% | 5.6 (interpolated) | pass | 0.251 (unverified) | 0.85 |
| 22 | `cfg_2021` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 48/192/200 | 440 | 23.9% | 4.4% | 0.87 | -4.9% | 233 | 1.28 | 16.8% | 194.3 | 8/8 | 1.00 | 0.72 | 0.14 | 4 | 12.1% | 0.47 | 0.56 | 21.5% | 19.0% | 12.2% | 21.9%/14.1% | 6.0 (interpolated) | pass | 0.190 (unverified) | 0.95 |
| 23 | `cfg_216a` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.0, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=4, stop=1.5, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 66/45/48 | 159 | 10.1% | 1.9% | 0.93 | -1.8% | 355 | 1.58 | 3.5% | 70.1 | 7/7 | 1.00 | 0.49 | 0.44 | 4 | 4.3% | 0.57 | 0.66 | 9.3% | 8.7% | 8.3% | 9.4%/6.6% | 7.5 (interpolated) | pass | 0.206 (unverified) | 0.38 |
| 24 | `cfg_faaf` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=3.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 234/56/170 | 460 | 13.7% | 2.6% | 0.85 | -4.6% | 215 | 1.24 | 11.6% | 201.6 | 6/6 | 0.83 | 0.62 | 0.23 | 5 | 7.8% | 0.42 | 0.43 | 11.6% | 9.1% | 10.9% | 12.3%/10.4% | 4.0 (interpolated) | pass | 0.194 (unverified) | 1.39 |
| 25 | `cfg_5755` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 405/71/320 | 796 | 22.0% | 4.1% | 0.93 | -7.2% | 405 | 1.21 | 15.0% | 352.2 | 6/6 | 1.00 | 0.52 | 0.41 | 5 | 12.8% | 0.39 | 0.33 | 17.3% | 12.9% | 3.7% | 18.9%/14.0% | 3.6 (interpolated) | pass | 0.252 (unverified) | 1.14 |
| 26 | `cfg_c276` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 195/62/163 | 420 | 13.8% | 2.6% | 0.79 | -4.4% | 524 | 1.24 | 10.9% | 185.6 | 6/6 | 1.00 | 0.67 | 0.12 | 4 | 7.2% | 0.45 | 0.52 | 12.0% | 9.5% | 13.1% | 12.4%/8.3% | 4.2 (interpolated) | pass | 0.165 (unverified) | 1.24 |
| 27 | `cfg_f8ea` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 361/155/295 | 811 | 29.0% | 5.2% | 0.96 | -4.6% | 207 | 1.22 | 19.3% | 358.4 | 6/6 | 1.00 | 0.40 | 0.56 | 5 | 16.4% | 0.43 | 0.38 | 23.0% | 18.5% | 5.1% | 25.0%/19.6% | 4.1 (interpolated) | pass | 0.268 (unverified) | 0.59 |
| 28 | `cfg_d620` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=none, direction=long, trend_filter=none, min_box_atr=0.0 | 0/269/224 | 493 | 28.0% | 5.1% | 0.83 | -6.3% | 409 | 1.29 | 20.5% | 217.2 | 5/5 | 0.80 | 0.63 | 0.20 | 5 | 16.7% | 0.40 | 0.68 | 24.1% | 22.0% | 10.5% | 25.1%/17.8% | 6.0 (interpolated) | pass | 0.159 (unverified) | 0.50 |
| 29 | `cfg_5680` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=1.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 197/63/166 | 426 | 14.1% | 2.7% | 0.80 | -4.4% | 524 | 1.24 | 11.1% | 188.3 | 6/6 | 1.00 | 0.69 | 0.11 | 4 | 7.0% | 0.47 | 0.50 | 12.1% | 9.7% | 13.2% | 12.8%/9.4% | 4.1 (interpolated) | pass | 0.172 (unverified) | 1.17 |
| 30 | `cfg_4d03` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 53/218/222 | 493 | 26.9% | 4.9% | 0.85 | -6.2% | 365 | 1.28 | 19.3% | 216.7 | 6/6 | 0.83 | 0.51 | 0.34 | 5 | 15.9% | 0.38 | 0.60 | 22.8% | 19.8% | 8.5% | 22.2%/15.9% | 5.7 (interpolated) | pass | 0.174 (unverified) | 0.40 |
| 31 | `cfg_5c7d` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/499/440 | 939 | 39.1% | 6.8% | 0.80 | -19.2% | 543 | 1.20 | 39.3% | 416.8 | 5/5 | 1.00 | 0.27 | 0.54 | 4 | 15.2% | 0.61 | 0.52 | 32.5% | 27.9% | 21.0% | 36.3%/26.5% | 4.5 (interpolated) | pass | 0.175 (unverified) | 0.21 |
| 32 | `cfg_f668` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 294/69/212 | 575 | 22.9% | 4.2% | 0.98 | -8.0% | 373 | 1.26 | 13.6% | 255.1 | 7/7 | 0.71 | 0.59 | 0.39 | 3 | 8.0% | 0.64 | 0.37 | 19.5% | 16.2% | 11.6% | 20.5%/16.0% | 4.8 (interpolated) | pass | 0.287 (unverified) | 0.67 |
| 33 | `cfg_5896` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=long, trend_filter=none, min_box_atr=0.0 | 0/224/217 | 441 | 21.6% | 4.0% | 0.80 | -7.4% | 239 | 1.26 | 18.3% | 196.7 | 7/7 | 0.86 | 0.61 | 0.19 | 4 | 8.7% | 0.59 | 0.67 | 18.0% | 16.3% | 11.4% | 18.5%/12.3% | 5.3 (interpolated) | pass | 0.148 (unverified) | 0.88 |
| 34 | `cfg_11b0` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=3.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 80/319/342 | 741 | 31.8% | 5.7% | 0.84 | -9.8% | 296 | 1.21 | 30.8% | 326.2 | 7/7 | 1.00 | 0.61 | 0.22 | 4 | 16.2% | 0.49 | 0.46 | 26.9% | 23.3% | 11.1% | 26.9%/21.8% | 4.8 (interpolated) | pass | 0.178 (unverified) | 0.34 |
| 35 | `cfg_a470` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=3.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/509/447 | 956 | 38.4% | 6.7% | 0.78 | -19.4% | 552 | 1.19 | 40.1% | 424.2 | 5/5 | 1.00 | 0.23 | 0.55 | 4 | 12.3% | 0.68 | 0.52 | 32.3% | 25.3% | 21.1% | 33.5%/22.7% | 4.4 (interpolated) | pass | 0.163 (unverified) | 0.19 |
| 36 | `cfg_c527` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.0, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 63/41/46 | 150 | 9.4% | 1.8% | 0.88 | -1.9% | 355 | 1.56 | 3.3% | 65.7 | 7/7 | 1.00 | 0.44 | 0.44 | 4 | 4.0% | 0.56 | 0.72 | 8.8% | 8.0% | 7.6% | 8.7%/6.6% | 7.5 (interpolated) | pass | 0.169 (unverified) | 0.57 |
| 37 | `cfg_9b02` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 272/75/230 | 577 | 22.5% | 4.1% | 0.87 | -4.8% | 305 | 1.22 | 13.6% | 255.8 | 7/7 | 1.00 | 0.43 | 0.44 | 3 | 9.4% | 0.56 | 0.53 | 18.6% | 15.8% | 7.6% | 20.4%/16.7% | 4.6 (interpolated) | pass | 0.202 (unverified) | 0.47 |
| 38 | `cfg_27b6` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=3.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 123/261/366 | 750 | 29.8% | 5.4% | 0.82 | -12.0% | 265 | 1.21 | 29.8% | 330.7 | 7/7 | 1.00 | 0.65 | 0.17 | 5 | 19.9% | 0.33 | 0.46 | 25.0% | 22.1% | 12.6% | 25.9%/19.5% | 4.5 (interpolated) | pass | 0.175 (unverified) | 0.52 |
| 39 | `cfg_b970` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/203/274 | 477 | 22.3% | 4.1% | 0.76 | -9.0% | 436 | 1.28 | 16.3% | 212.3 | 7/7 | 1.00 | 0.49 | 0.27 | 3 | 10.1% | 0.50 | 0.63 | 19.3% | 16.4% | 15.0% | 20.9%/16.6% | 5.3 (interpolated) | pass | 0.137 (unverified) | 0.85 |
| 40 | `cfg_eb11` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0 | 810/128/671 | 1609 | 31.5% | 5.6% | 0.83 | -9.8% | 193 | 1.13 | 29.2% | 710.9 | 6/6 | 0.83 | 0.46 | 0.37 | 5 | 19.9% | 0.37 | 0.36 | 21.6% | 11.8% | 5.1% | 25.8%/19.1% | 2.7 (interpolated) | pass | 0.185 (unverified) | 1.12 |
| 41 | `cfg_d812` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/201/268 | 469 | 23.4% | 4.3% | 0.80 | -9.0% | 438 | 1.30 | 15.8% | 208.6 | 7/7 | 1.00 | 0.46 | 0.34 | 3 | 11.1% | 0.47 | 0.60 | 20.4% | 17.4% | 16.8% | 22.1%/15.4% | 5.5 (interpolated) | pass | 0.159 (unverified) | 0.81 |
| 42 | `cfg_7900` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=1.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 41/63/118 | 222 | 12.3% | 2.3% | 0.76 | -3.9% | 266 | 1.38 | 6.8% | 97.8 | 7/7 | 0.86 | 0.63 | 0.13 | 4 | 2.2% | 0.84 | 0.81 | 11.2% | 10.1% | 4.9% | 11.1%/9.0% | 6.8 (interpolated) | pass | 0.099 (unverified) | 1.19 |
| 43 | `cfg_50cb` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=long, trend_filter=none, min_box_atr=0.0 | 0/343/313 | 656 | 30.4% | 5.5% | 0.83 | -8.0% | 241 | 1.23 | 28.6% | 292.8 | 7/7 | 1.00 | 0.81 | 0.02 | 5 | 17.1% | 0.41 | 0.60 | 26.8% | 21.7% | 11.5% | 27.0%/19.4% | 5.3 (interpolated) | pass | 0.168 (unverified) | 1.04 |
| 44 | `cfg_0f3c` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=1.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.5, direction=long, trend_filter=ema50, min_box_atr=0.0 | 80/95/204 | 379 | 13.9% | 2.6% | 0.76 | -5.1% | 406 | 1.30 | 9.8% | 167.3 | 6/6 | 0.67 | 0.46 | 0.30 | 5 | 6.5% | 0.53 | 0.77 | 12.1% | 9.9% | 0.6% | 13.2%/10.3% | 4.5 (interpolated) | pass | 0.122 (unverified) | 0.55 |
| 45 | `cfg_aaeb` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=3.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 26/268/199 | 493 | 22.0% | 4.1% | 0.79 | -5.1% | 479 | 1.26 | 20.2% | 217.5 | 7/7 | 1.00 | 0.60 | 0.18 | 4 | 8.7% | 0.60 | 0.54 | 19.7% | 16.3% | 17.2% | 19.2%/14.8% | 5.1 (interpolated) | pass | 0.149 (unverified) | 1.04 |
| 46 | `cfg_36ee` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=1.5, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=1, stop=1.5, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 11/229/104 | 344 | 13.4% | 2.5% | 0.78 | -3.3% | 333 | 1.30 | 8.0% | 152.2 | 6/6 | 1.00 | 0.65 | 0.13 | 4 | 7.3% | 0.44 | 0.65 | 11.6% | 9.6% | 4.0% | 12.0%/8.6% | 4.6 (interpolated) | pass | 0.145 (unverified) | -0.08 |
| 47 | `cfg_aa7f` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0 | 715/280/602 | 1597 | 32.5% | 5.8% | 0.75 | -13.3% | 569 | 1.11 | 36.0% | 701.4 | 6/6 | 0.50 | 0.06 | 0.69 | 4 | 15.7% | 0.45 | 0.40 | 22.1% | 14.1% | 13.6% | 29.5%/20.8% | 2.8 (interpolated) | pass | 0.146 (unverified) | 0.35 |
| 48 | `cfg_3b79` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=both, trend_filter=ema50, min_box_atr=0.0 | 118/65/105 | 288 | 11.8% | 2.3% | 0.84 | -3.7% | 298 | 1.31 | 5.6% | 127.0 | 6/6 | 0.67 | 0.49 | 0.36 | 4 | 1.1% | 0.88 | 0.67 | 10.2% | 8.5% | 7.6% | 10.5%/7.5% | 4.8 (interpolated) | pass | 0.197 (unverified) | 0.76 |
| 49 | `cfg_ed65` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=1.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 25/284/128 | 437 | 16.5% | 3.1% | 0.76 | -4.7% | 362 | 1.26 | 12.4% | 193.1 | 6/6 | 1.00 | 0.65 | 0.11 | 4 | 7.2% | 0.56 | 0.58 | 13.8% | 10.9% | 11.9% | 14.1%/11.2% | 4.4 (interpolated) | pass | 0.141 (unverified) | 0.10 |
| 50 | `cfg_bc71` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=long, trend_filter=none, min_box_atr=0.0 | 0/337/309 | 646 | 29.6% | 5.3% | 0.81 | -8.1% | 241 | 1.23 | 28.2% | 288.5 | 7/7 | 0.86 | 0.82 | -0.00 | 5 | 16.0% | 0.43 | 0.62 | 25.5% | 22.1% | 10.7% | 26.3%/19.6% | 5.2 (interpolated) | pass | 0.158 (unverified) | 1.10 |
| 51 | `cfg_58e0` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=1.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 25/275/126 | 426 | 16.8% | 3.2% | 0.77 | -5.0% | 365 | 1.27 | 12.0% | 188.7 | 6/6 | 1.00 | 0.69 | 0.09 | 4 | 7.7% | 0.54 | 0.57 | 14.3% | 12.3% | 12.3% | 15.3%/10.8% | 4.7 (interpolated) | pass | 0.150 (unverified) | 0.18 |
| 52 | `cfg_2cbd` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=3.0, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=1, stop=1.5, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/363/260 | 623 | 27.9% | 5.0% | 0.81 | -8.8% | 507 | 1.23 | 20.8% | 275.7 | 7/7 | 1.00 | 0.48 | 0.33 | 4 | 13.9% | 0.44 | 0.60 | 24.0% | 20.4% | 25.3% | 25.2%/19.4% | 5.1 (interpolated) | pass | 0.156 (unverified) | 0.42 |
| 53 | `cfg_3b0e` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 264/73/226 | 563 | 18.9% | 3.5% | 0.78 | -4.9% | 427 | 1.20 | 13.0% | 248.1 | 7/7 | 1.00 | 0.30 | 0.48 | 4 | 8.4% | 0.53 | 0.56 | 14.6% | 11.6% | 4.9% | 16.3%/11.4% | 4.2 (interpolated) | pass | 0.148 (unverified) | 0.51 |
| 54 | `cfg_44fc` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=1.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 25/92/105 | 222 | 15.6% | 2.9% | 0.77 | -3.3% | 339 | 1.43 | 7.8% | 98.0 | 7/7 | 0.86 | 0.56 | 0.22 | 5 | 4.2% | 0.73 | 0.82 | 14.1% | 13.1% | 6.3% | 14.6%/9.8% | 7.7 (interpolated) | pass | 0.092 (unverified) | 0.92 |
| 55 | `cfg_3f95` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 286/66/209 | 561 | 19.0% | 3.5% | 0.84 | -8.1% | 462 | 1.22 | 13.0% | 249.3 | 7/7 | 0.71 | 0.54 | 0.30 | 3 | 6.1% | 0.66 | 0.41 | 15.8% | 12.5% | 8.9% | 17.2%/13.1% | 4.2 (interpolated) | pass | 0.194 (unverified) | 0.80 |
| 56 | `cfg_361a` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=3.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0 | 289/388/239 | 916 | 30.6% | 5.5% | 0.76 | -10.5% | 343 | 1.17 | 35.7% | 405.9 | 6/6 | 0.83 | 0.28 | 0.48 | 3 | 11.3% | 0.63 | 0.41 | 24.1% | 17.1% | 11.9% | 26.2%/17.8% | 3.9 (interpolated) | pass | 0.158 (unverified) | 0.80 |
| 57 | `cfg_eb29` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=3.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0 | 279/381/232 | 892 | 29.8% | 5.4% | 0.77 | -9.8% | 342 | 1.17 | 34.8% | 395.3 | 6/6 | 0.83 | 0.33 | 0.44 | 3 | 12.0% | 0.60 | 0.40 | 24.2% | 18.5% | 12.7% | 26.8%/19.9% | 3.9 (interpolated) | pass | 0.166 (unverified) | 0.71 |
| 58 | `cfg_d38c` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=3.0, min_squeeze_bars=4, entry_type=close, setup_expiry_bars=1, stop=1.5, target_r=none, direction=long, trend_filter=none, min_box_atr=0.0 | 0/216/124 | 340 | 19.1% | 3.6% | 0.77 | -6.2% | 333 | 1.35 | 11.6% | 149.8 | 7/7 | 1.00 | 0.41 | 0.37 | 4 | 12.0% | 0.37 | 0.78 | 17.2% | 15.7% | 14.4% | 16.9%/12.7% | 6.2 (interpolated) | pass | 0.129 (unverified) | 0.59 |
| 59 | `cfg_1c12` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 210/90/185 | 485 | 17.0% | 3.2% | 0.76 | -5.1% | 310 | 1.22 | 14.8% | 214.5 | 7/7 | 1.00 | 0.40 | 0.36 | 3 | 8.7% | 0.48 | 0.53 | 14.4% | 12.0% | 4.5% | 14.7%/12.2% | 4.2 (interpolated) | pass | 0.145 (unverified) | 0.20 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | -2.5% / -0.44 / 161 | 5.6% / 1.48 / 154 | 17.3% / 1.79 / 157 | 8.1% / 2.18 / 144 | 12.6% / 1.70 / 163 |
| 2 | 0.7% / 0.14 / 157 | 5.7% / 1.42 / 150 | 19.5% / 1.84 / 156 | 6.7% / 1.89 / 144 | 13.5% / 1.66 / 159 |
| 3 | 4.8% / 1.52 / 54 | -0.3% / -0.15 / 58 | 15.4% / 1.72 / 63 | -0.1% / -0.02 / 66 | 8.4% / 1.87 / 61 |
| 4 | 1.5% / 0.28 / 157 | 8.0% / 1.87 / 153 | 11.3% / 1.03 / 155 | 6.4% / 1.78 / 146 | 13.8% / 1.74 / 158 |
| 5 | 2.1% / 0.99 / 23 | 0.4% / 0.19 / 37 | 7.5% / 2.01 / 29 | -0.6% / -0.44 / 39 | 4.2% / 2.02 / 23 |
| 6 | 4.7% / 1.51 / 54 | 0.3% / 0.14 / 58 | 15.0% / 1.69 / 63 | -0.1% / -0.03 / 66 | 9.4% / 1.93 / 61 |
| 7 | 2.1% / 0.99 / 23 | 1.1% / 0.55 / 35 | 7.2% / 1.97 / 26 | -0.6% / -0.41 / 37 | 4.2% / 2.02 / 23 |
| 8 | 0.9% / 0.22 / 167 | 4.7% / 1.75 / 159 | 10.6% / 1.61 / 164 | 6.4% / 2.30 / 154 | 2.5% / 0.53 / 172 |
| 9 | 4.0% / 0.56 / 156 | 7.7% / 1.77 / 151 | 9.8% / 0.92 / 154 | 6.4% / 1.74 / 145 | 15.8% / 1.84 / 157 |
| 10 | 3.0% / 2.19 / 19 | -0.9% / -0.67 / 31 | 6.7% / 1.70 / 30 | -0.3% / -0.22 / 36 | 2.4% / 1.54 / 16 |
| 11 | -3.0% / -0.52 / 111 | 7.3% / 1.88 / 110 | 17.9% / 1.89 / 109 | 6.3% / 1.77 / 110 | 1.4% / 0.23 / 124 |
| 12 | -1.7% / -0.40 / 119 | 3.5% / 1.18 / 129 | 6.4% / 0.90 / 140 | 1.4% / 0.44 / 129 | 14.9% / 2.38 / 140 |
| 13 | 3.0% / 2.19 / 19 | -0.6% / -0.43 / 30 | 6.3% / 1.61 / 28 | -0.2% / -0.14 / 35 | 2.4% / 1.54 / 16 |
| 14 | -1.8% / -0.31 / 122 | 8.5% / 2.01 / 123 | 9.5% / 0.99 / 135 | 4.8% / 1.38 / 141 | 8.5% / 1.16 / 134 |
| 15 | 0.3% / 0.07 / 129 | 7.5% / 1.77 / 130 | 12.8% / 1.29 / 139 | 4.0% / 1.08 / 132 | 7.1% / 0.96 / 142 |
| 16 | -2.6% / -0.46 / 107 | 6.4% / 1.67 / 107 | 14.5% / 1.67 / 106 | 6.3% / 1.73 / 107 | 1.9% / 0.31 / 123 |
| 17 | 9.1% / 1.15 / 310 | 0.9% / 0.20 / 291 | 5.1% / 0.42 / 286 | 10.5% / 1.86 / 284 | 21.8% / 2.00 / 303 |
| 18 | -1.9% / -0.47 / 120 | 2.9% / 0.95 / 134 | 6.8% / 0.90 / 146 | 1.6% / 0.51 / 130 | 13.9% / 2.26 / 142 |
| 19 | -1.6% / -0.28 / 121 | 7.5% / 1.85 / 120 | 9.6% / 1.00 / 134 | 5.2% / 1.50 / 137 | 7.8% / 1.07 / 133 |
| 20 | 12.4% / 1.48 / 297 | -1.6% / -0.26 / 289 | -1.1% / -0.00 / 280 | 12.3% / 2.09 / 297 | 24.9% / 2.13 / 291 |
| 21 | 0.3% / 0.07 / 129 | 8.1% / 1.91 / 128 | 12.3% / 1.25 / 138 | 3.9% / 1.04 / 129 | 7.1% / 0.96 / 142 |
| 22 | 2.5% / 0.54 / 82 | 4.1% / 1.25 / 97 | 10.5% / 1.37 / 87 | 5.5% / 1.62 / 81 | -0.4% / -0.05 / 93 |
| 23 | 1.3% / 0.82 / 28 | 1.5% / 1.32 / 27 | 5.6% / 1.57 / 33 | -1.4% / -1.16 / 41 | 2.8% / 1.36 / 30 |
| 24 | 0.4% / 0.17 / 94 | 3.3% / 1.66 / 92 | 2.8% / 0.68 / 90 | 5.4% / 2.23 / 97 | 1.2% / 0.34 / 87 |
| 25 | 0.7% / 0.19 / 163 | 4.6% / 1.71 / 155 | 8.1% / 1.29 / 158 | 5.6% / 2.10 / 151 | 1.4% / 0.31 / 169 |
| 26 | -2.5% / -0.84 / 82 | 2.0% / 0.90 / 87 | 6.2% / 1.28 / 84 | 2.6% / 1.20 / 87 | 5.0% / 1.29 / 80 |
| 27 | 3.9% / 0.80 / 164 | 5.3% / 1.61 / 159 | 2.5% / 0.33 / 162 | 3.7% / 1.33 / 157 | 10.8% / 1.89 / 169 |
| 28 | 3.0% / 0.59 / 102 | 3.9% / 1.17 / 98 | 7.6% / 0.84 / 99 | 1.3% / 0.56 / 96 | 9.6% / 1.22 / 98 |
| 29 | -2.5% / -0.84 / 82 | 1.4% / 0.66 / 89 | 6.7% / 1.37 / 85 | 2.9% / 1.31 / 90 | 5.1% / 1.30 / 80 |
| 30 | 3.6% / 0.71 / 102 | 4.3% / 1.27 / 98 | 9.5% / 1.02 / 99 | 1.9% / 0.75 / 96 | 5.3% / 0.86 / 98 |
| 31 | 12.1% / 1.53 / 181 | 3.6% / 0.75 / 195 | -5.0% / -0.33 / 193 | 4.5% / 1.01 / 183 | 20.7% / 1.91 / 187 |
| 32 | -1.4% / -0.38 / 116 | 6.5% / 2.40 / 113 | 13.9% / 2.14 / 112 | 7.4% / 2.53 / 107 | -4.3% / -0.82 / 127 |
| 33 | 5.4% / 1.09 / 83 | 2.7% / 0.81 / 97 | 11.8% / 1.56 / 87 | 4.3% / 1.28 / 81 | -3.7% / -0.73 / 93 |
| 34 | -1.4% / -0.20 / 148 | 9.9% / 2.17 / 144 | 0.9% / 0.14 / 145 | 6.2% / 1.50 / 147 | 13.4% / 1.65 / 157 |
| 35 | 10.5% / 1.33 / 184 | 3.5% / 0.72 / 198 | -5.9% / -0.40 / 198 | 4.5% / 0.99 / 187 | 23.2% / 2.06 / 189 |
| 36 | 1.4% / 0.89 / 27 | 1.4% / 1.19 / 26 | 5.2% / 1.46 / 32 | -1.2% / -0.99 / 36 | 2.4% / 1.17 / 29 |
| 37 | -0.5% / -0.10 / 115 | 4.6% / 1.56 / 114 | 12.0% / 1.57 / 110 | 5.7% / 2.01 / 112 | -0.6% / -0.10 / 126 |
| 38 | 1.1% / 0.23 / 148 | 9.2% / 2.20 / 147 | 1.1% / 0.16 / 149 | 7.5% / 1.78 / 146 | 8.3% / 1.10 / 160 |
| 39 | 11.0% / 1.90 / 84 | -1.4% / -0.37 / 111 | 5.5% / 0.70 / 95 | -2.6% / -0.93 / 97 | 8.7% / 1.51 / 90 |
| 40 | 8.3% / 1.40 / 331 | 3.9% / 0.94 / 318 | 6.5% / 0.63 / 319 | 9.7% / 2.33 / 317 | 0.0% / 0.03 / 324 |
| 41 | 11.0% / 1.90 / 84 | -1.5% / -0.38 / 107 | 5.5% / 0.70 / 95 | -2.4% / -0.90 / 93 | 9.5% / 1.68 / 90 |
| 42 | 0.5% / 0.32 / 32 | 4.7% / 1.97 / 53 | 9.8% / 1.78 / 47 | 0.3% / 0.16 / 49 | -3.1% / -1.14 / 41 |
| 43 | 0.1% / 0.05 / 123 | 9.1% / 2.12 / 123 | 11.3% / 1.17 / 136 | 3.4% / 0.91 / 138 | 3.7% / 0.49 / 136 |
| 44 | 2.8% / 1.05 / 62 | 0.9% / 0.47 / 85 | 1.6% / 0.33 / 79 | 1.0% / 0.46 / 81 | 6.9% / 1.68 / 72 |
| 45 | -0.1% / -0.01 / 107 | 2.5% / 0.77 / 97 | 4.9% / 0.62 / 96 | 1.3% / 0.47 / 93 | 12.2% / 2.15 / 100 |
| 46 | 3.5% / 1.27 / 67 | 0.7% / 0.40 / 76 | 5.7% / 1.13 / 74 | -1.5% / -0.87 / 58 | 4.5% / 1.16 / 69 |
| 47 | 14.5% / 1.97 / 323 | 2.2% / 0.48 / 315 | -5.6% / -0.39 / 309 | 8.0% / 1.81 / 330 | 11.0% / 1.40 / 320 |
| 48 | 1.4% / 0.59 / 53 | -2.9% / -1.49 / 67 | 10.6% / 2.58 / 58 | 0.5% / 0.32 / 58 | 2.2% / 0.79 / 52 |
| 49 | 4.0% / 1.37 / 76 | 0.5% / 0.20 / 94 | 5.0% / 0.76 / 103 | -2.2% / -0.88 / 82 | 8.7% / 1.81 / 82 |
| 50 | 0.0% / 0.04 / 122 | 8.3% / 1.98 / 120 | 11.7% / 1.20 / 135 | 4.1% / 1.15 / 134 | 2.9% / 0.40 / 135 |
| 51 | 4.2% / 1.45 / 75 | 0.8% / 0.35 / 93 | 5.3% / 0.81 / 101 | -2.6% / -1.08 / 77 | 8.4% / 1.78 / 80 |
| 52 | 12.3% / 1.79 / 132 | -1.9% / -0.53 / 123 | 6.1% / 0.68 / 121 | 0.1% / 0.05 / 107 | 9.3% / 1.29 / 140 |
| 53 | -1.0% / -0.22 / 111 | 3.7% / 1.29 / 111 | 9.7% / 1.37 / 107 | 5.2% / 1.91 / 109 | 0.3% / 0.08 / 125 |
| 54 | 0.8% / 0.42 / 32 | 3.2% / 1.27 / 53 | 10.9% / 1.56 / 46 | 0.1% / 0.05 / 49 | 0.1% / 0.05 / 42 |
| 55 | -2.3% / -0.67 / 112 | 5.8% / 2.16 / 110 | 12.1% / 1.95 / 109 | 7.1% / 2.45 / 104 | -4.1% / -0.76 / 126 |
| 56 | 7.8% / 1.30 / 188 | -0.7% / -0.16 / 184 | 4.8% / 0.46 / 180 | -0.8% / -0.16 / 174 | 17.3% / 2.04 / 190 |
| 57 | 6.9% / 1.18 / 182 | -0.5% / -0.10 / 177 | 5.9% / 0.57 / 177 | -0.6% / -0.12 / 168 | 15.9% / 1.91 / 188 |
| 58 | 3.7% / 0.88 / 78 | 1.5% / 0.65 / 69 | 6.5% / 0.88 / 61 | -0.1% / -0.03 / 59 | 6.3% / 1.20 / 73 |
| 59 | 3.8% / 1.08 / 95 | -0.7% / -0.26 / 99 | 7.5% / 1.07 / 96 | -1.9% / -0.73 / 96 | 7.6% / 1.82 / 99 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_8ee3` | 19 | 0.82 | 0.66/0.86 | 0.53/0.81 |
| 1 | `cfg_5a28` | 24 | 0.85 | 0.81/0.89 | 0.49/0.75 |
| 2 | `cfg_3880` | 6 | 0.90 | 0.90/0.90 | 0.71/0.74 |
| 3 | `cfg_0f3c` | 1 | n/a | n/a/n/a | n/a/n/a |
| 4 | `cfg_11b0` | 6 | 0.81 | 0.87/0.90 | 0.76/0.78 |
| 5 | `cfg_158c` | 4 | 0.91 | 0.95/0.97 | 0.91/0.94 |
| 6 | `cfg_1c12` | 1 | n/a | n/a/n/a | n/a/n/a |
| 7 | `cfg_2021` | 5 | 0.83 | 0.90/0.93 | 0.75/0.85 |
| 8 | `cfg_216a` | 5 | 0.93 | 0.85/0.87 | 0.63/0.70 |
| 9 | `cfg_bc7d` | 8 | 0.83 | 0.87/0.88 | 0.74/0.77 |
| 10 | `cfg_5c7d` | 4 | 0.95 | 0.95/0.95 | 0.86/0.88 |
| 11 | `cfg_f51f` | 8 | 0.83 | 0.86/0.91 | 0.71/0.77 |
| 12 | `cfg_2cbd` | 1 | n/a | n/a/n/a | n/a/n/a |
| 13 | `cfg_67f0` | 4 | 0.84 | 0.81/0.84 | 0.70/0.72 |
| 14 | `cfg_361a` | 2 | 0.99 | 0.96/0.96 | 0.97/0.97 |
| 15 | `cfg_36ee` | 1 | n/a | n/a/n/a | n/a/n/a |
| 16 | `cfg_9b02` | 2 | 0.98 | 0.97/0.97 | 0.96/0.96 |
| 17 | `cfg_3b79` | 1 | n/a | n/a/n/a | n/a/n/a |
| 18 | `cfg_f668` | 2 | 0.98 | 0.98/0.98 | 0.96/0.96 |
| 19 | `cfg_7900` | 2 | 0.91 | 0.90/0.90 | 0.66/0.66 |
| 20 | `cfg_d620` | 4 | 0.96 | 0.96/0.96 | 0.92/0.93 |
| 21 | `cfg_7a89` | 4 | 0.87 | 0.91/0.94 | 0.86/0.90 |
| 22 | `cfg_ecd5` | 3 | 0.91 | 0.95/0.96 | 0.85/0.90 |
| 23 | `cfg_50cb` | 2 | 1.00 | 1.00/1.00 | 0.99/0.99 |
| 24 | `cfg_ecb8` | 5 | 0.85 | 0.82/0.96 | 0.57/0.93 |
| 25 | `cfg_c276` | 4 | 0.89 | 0.83/0.84 | 0.58/0.59 |
| 26 | `cfg_f37a` | 2 | 0.97 | 0.97/0.97 | 0.95/0.95 |
| 27 | `cfg_ed65` | 2 | 0.99 | 0.99/0.99 | 0.97/0.97 |
| 28 | `cfg_aa7f` | 1 | n/a | n/a/n/a | n/a/n/a |
| 29 | `cfg_aaeb` | 1 | n/a | n/a/n/a | n/a/n/a |
| 30 | `cfg_b970` | 2 | 0.99 | 0.99/0.99 | 0.97/0.97 |
| 31 | `cfg_d38c` | 1 | n/a | n/a/n/a | n/a/n/a |
| 32 | `cfg_eb11` | 1 | n/a | n/a/n/a | n/a/n/a |
| 33 | `cfg_f8ea` | 1 | n/a | n/a/n/a | n/a/n/a |
| 34 | `cfg_faaf` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 6.713e-04 over 3840 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 435.0, participation ratio 12.9, 95%-variance components 163 (rank bound T = 1259); raw grid 3840; raw + known prior 848880
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
