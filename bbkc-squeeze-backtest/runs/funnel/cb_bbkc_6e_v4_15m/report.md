# Screening funnel -- cb_bbkc_6e_v4_15m (development stages only)

- Code: `36bde5f6ce84` (dirty working tree: True, diff sha256 `99d2740b6266`)
- Config: `configs/funnel/cb_bbkc_funnel_6e_v4_15m.yaml` sha256 `c20b5478dfdbf524`; seed 20261112
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'6E': '2026-10-16', '6J': '2026-10-16'}
- Frozen manifest sha256: `3e55893c24478d11` (23 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **False** -- No compression-breakout strategy has been selected or scored on 6E 2023-2024. This grid was chosen after reading ES, NQ and YM squeeze results on 2023-2024 and 2025+. Other families were validated there (mean-reversion: mr_6e_v5, mr_6e_v6), so the period has been looked at by the researcher, but not for this strategy.
- Holdout 2025+ previously inspected: **False** -- No metrics of any family have been computed on 6E 2025+ (no holdout reads in the mean-reversion or noise-band ledgers).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 3840 | 3840 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 3840 | 3840 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 3840 | 3264 | 576 | 0 |  | 3278 | 85.00 | 85.00 |  |
| 3 performance & risk | hard_gate | 3264 | 40 | 3224 | 0 |  | 0 | 1.04 | 1.23 |  |
| 4 parameter stability | hard_gate | 40 | 40 | 0 | 0 |  | 0 | 1.04 | 100.00 |  |
| 5 time stability | hard_gate | 40 | 40 | 0 | 0 |  | 37 | 1.04 | 100.00 |  |
| 6 deduplication | dedup | 40 | 23 |  |  | 17 |  | 0.60 | 57.50 | best 2 per cluster |
| 7 execution stress | hard_gate | 23 | 23 | 0 | 0 |  | 3 | 0.60 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 23 |  |  |  |  |  |  |  | diagnostic only: unverified: 23 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 576 |
| s2:hard_reject:years_with_>=10_trades | 401 |
| s3:hard_reject:net_return | 2187 |
| s3:hard_reject:sharpe | 3224 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | target/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | 6J dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_e6d8` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0 | 44/59/19 | 122 | 5.6% | 1.1% | 1.52 | -0.7% | 407 | 2.37 | 2.8% | 50.4 | 6/6 | 0.83 | 0.69 | 0.82 | 5 | 2.8% | 0.50 | 0.38 | 4.9% | 4.1% | 3.3% | 5.0%/4.4% | 4.8 (interpolated) | pass | 0.471 (unverified) | -0.36 |
| 2 | `cfg_50ed` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=both, trend_filter=none, min_box_atr=0.0 | 13/88/21 | 122 | 6.0% | 1.2% | 1.32 | -0.9% | 403 | 2.25 | 4.0% | 50.7 | 7/7 | 1.00 | 0.94 | 0.38 | 5 | 4.1% | 0.30 | 0.49 | 5.3% | 4.6% | 3.5% | 5.4%/4.5% | 5.1 (interpolated) | pass | 0.273 (unverified) | 0.07 |
| 3 | `cfg_4a4a` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0 | 44/57/19 | 120 | 5.1% | 1.0% | 1.44 | -0.7% | 435 | 2.27 | 2.7% | 49.6 | 6/6 | 0.83 | 0.72 | 0.72 | 5 | 2.9% | 0.44 | 0.41 | 4.4% | 3.7% | 3.5% | 4.6%/3.8% | 4.6 (interpolated) | pass | 0.386 (unverified) | -0.19 |
| 4 | `cfg_41ac` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=both, trend_filter=none, min_box_atr=0.0 | 61/398/205 | 664 | 14.2% | 2.7% | 1.15 | -2.6% | 471 | 1.29 | 27.8% | 275.9 | 8/8 | 0.88 | 0.67 | 0.48 | 4 | 8.5% | 0.41 | 0.29 | 9.7% | 5.5% | 7.2% | 12.8%/9.9% | 2.7 (interpolated) | pass | 0.179 (unverified) | 0.33 |
| 5 | `cfg_8cd1` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.5, direction=both, trend_filter=none, min_box_atr=0.0 | 13/87/20 | 120 | 6.2% | 1.2% | 1.41 | -0.9% | 423 | 2.43 | 3.9% | 49.9 | 7/7 | 1.00 | 0.94 | 0.46 | 5 | 4.3% | 0.32 | 0.47 | 5.5% | 4.8% | 3.8% | 5.5%/4.7% | 5.3 (interpolated) | pass | 0.348 (unverified) | 0.22 |
| 6 | `cfg_64da` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.5, direction=both, trend_filter=none, min_box_atr=0.0 | 59/386/199 | 644 | 13.7% | 2.6% | 1.13 | -2.9% | 474 | 1.29 | 26.9% | 267.5 | 8/8 | 0.88 | 0.64 | 0.49 | 4 | 8.6% | 0.37 | 0.30 | 9.2% | 5.5% | 7.3% | 12.2%/9.6% | 2.7 (interpolated) | pass | 0.166 (unverified) | 0.32 |
| 7 | `cfg_a3e8` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=both, trend_filter=ema50, min_box_atr=0.0 | 186/298/118 | 602 | 6.3% | 1.2% | 0.81 | -2.3% | 382 | 1.21 | 14.6% | 250.5 | 6/6 | 0.83 | 0.44 | 0.37 | 4 | 3.6% | 0.42 | 0.44 | 2.8% | -0.8% | -0.0% | 5.9%/4.4% | 1.9 (interpolated) | pass | 0.047 (unverified) | -0.58 |
| 8 | `cfg_39c2` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=both, trend_filter=ema50, min_box_atr=0.0 | 32/261/128 | 421 | 9.1% | 1.8% | 0.91 | -4.4% | 608 | 1.29 | 17.9% | 175.6 | 8/8 | 0.88 | 0.76 | 0.15 | 4 | 5.3% | 0.41 | 0.43 | 6.6% | 4.1% | 4.8% | 8.3%/6.3% | 2.8 (interpolated) | pass | 0.071 (unverified) | 0.18 |
| 9 | `cfg_c820` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=2.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.5, direction=both, trend_filter=ema50, min_box_atr=0.0 | 34/422/130 | 586 | 7.2% | 1.4% | 0.81 | -4.1% | 370 | 1.21 | 19.0% | 243.3 | 7/7 | 0.86 | 0.66 | 0.14 | 3 | 2.8% | 0.59 | 0.43 | 3.6% | 0.1% | 2.0% | 6.5%/5.1% | 2.0 (interpolated) | pass | 0.046 (unverified) | -0.43 |
| 10 | `cfg_c033` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.5, direction=both, trend_filter=ema50, min_box_atr=0.0 | 30/252/123 | 405 | 8.7% | 1.7% | 0.89 | -4.3% | 608 | 1.29 | 17.2% | 169.1 | 8/8 | 0.88 | 0.75 | 0.14 | 4 | 5.2% | 0.40 | 0.45 | 6.3% | 3.9% | 4.9% | 7.7%/5.7% | 2.9 (interpolated) | pass | 0.065 (unverified) | 0.15 |
| 11 | `cfg_99dd` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=1.0, direction=both, trend_filter=ema50, min_box_atr=0.0 | 198/193/141 | 532 | 8.0% | 1.6% | 0.84 | -4.3% | 479 | 1.23 | 15.8% | 219.8 | 7/7 | 0.86 | 0.48 | 0.35 | 3 | 1.1% | 0.86 | 0.40 | 4.8% | 1.9% | 4.2% | 7.2%/5.9% | 2.3 (interpolated) | pass | 0.066 (unverified) | -0.45 |
| 12 | `cfg_75fe` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=2.5, direction=long, trend_filter=none, min_box_atr=0.0 | 32/190/100 | 322 | 7.1% | 1.4% | 0.83 | -2.6% | 551 | 1.32 | 13.2% | 133.6 | 8/8 | 0.88 | 0.48 | 0.35 | 5 | 3.3% | 0.53 | 0.52 | 5.2% | 3.4% | 2.6% | 6.6%/5.2% | 2.8 (interpolated) | pass | 0.047 (unverified) | 0.10 |
| 13 | `cfg_82ce` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=3.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=both, trend_filter=ema50, min_box_atr=0.0 | 189/187/132 | 508 | 7.5% | 1.5% | 0.81 | -4.4% | 555 | 1.23 | 15.1% | 210.9 | 7/7 | 0.86 | 0.37 | 0.44 | 3 | 1.2% | 0.85 | 0.43 | 4.8% | 2.0% | 3.6% | 6.5%/4.8% | 2.3 (interpolated) | pass | 0.059 (unverified) | -0.53 |
| 14 | `cfg_534e` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=box, target_r=none, direction=long, trend_filter=none, min_box_atr=0.0 | 0/219/102 | 321 | 7.0% | 1.4% | 0.75 | -3.0% | 551 | 1.31 | 14.2% | 133.3 | 7/7 | 0.86 | 0.37 | 0.38 | 5 | 2.5% | 0.63 | 0.70 | 5.2% | 3.4% | 2.9% | 5.9%/4.6% | 2.8 (interpolated) | pass | 0.027 (unverified) | 0.09 |
| 15 | `cfg_f6e4` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=1.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=both, trend_filter=ema50, min_box_atr=0.0 | 47/51/26 | 124 | 2.6% | 0.5% | 0.82 | -0.7% | 428 | 1.49 | 3.6% | 50.9 | 6/6 | 0.83 | 0.44 | 0.38 | 5 | 1.8% | 0.30 | 0.53 | 1.9% | 1.2% | -0.8% | 2.4%/1.9% | 2.9 (interpolated) | pass | 0.050 (unverified) | -0.01 |
| 16 | `cfg_107f` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=2.5, direction=long, trend_filter=ema50, min_box_atr=0.0 | 33/75/83 | 191 | 4.6% | 0.9% | 0.77 | -2.0% | 569 | 1.38 | 5.9% | 79.4 | 8/8 | 1.00 | 0.57 | 0.21 | 3 | 2.6% | 0.43 | 0.67 | 3.5% | 2.5% | 2.0% | 4.3%/3.1% | 3.0 (interpolated) | pass | 0.034 (unverified) | -0.33 |
| 17 | `cfg_90f6` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=1.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.0 | 0/195/93 | 288 | 5.8% | 1.1% | 0.76 | -1.6% | 184 | 1.37 | 8.7% | 117.9 | 5/5 | 0.80 | 0.54 | 0.22 | 4 | 2.5% | 0.57 | 0.86 | 4.2% | 2.5% | 2.1% | 5.4%/4.0% | 2.7 (interpolated) | pass | 0.024 (unverified) | -0.16 |
| 18 | `cfg_f227` | timeframe=15min, compression=bbkc, squeeze_length=15, kc_mult=1.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=2.5, direction=long, trend_filter=ema50, min_box_atr=0.0 | 41/166/88 | 295 | 4.5% | 0.9% | 0.76 | -1.6% | 340 | 1.30 | 7.3% | 121.1 | 6/6 | 0.67 | 0.29 | 0.47 | 5 | 2.8% | 0.38 | 0.63 | 2.7% | 1.1% | 1.2% | 4.1%/3.2% | 2.3 (interpolated) | pass | 0.031 (unverified) | -0.27 |
| 19 | `cfg_2027` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.0 | 0/107/84 | 191 | 5.4% | 1.1% | 0.80 | -2.3% | 569 | 1.43 | 7.2% | 79.8 | 7/7 | 1.00 | 0.63 | 0.17 | 3 | 3.2% | 0.40 | 0.73 | 4.3% | 3.4% | 2.7% | 5.0%/3.9% | 3.4 (interpolated) | pass | 0.031 (unverified) | -0.03 |
| 20 | `cfg_93fd` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/340/264 | 604 | 8.6% | 1.7% | 0.76 | -2.5% | 455 | 1.21 | 23.7% | 251.8 | 7/7 | 0.71 | 0.19 | 0.57 | 5 | 3.8% | 0.56 | 0.65 | 5.3% | 1.9% | 0.3% | 7.7%/5.8% | 2.3 (interpolated) | pass | 0.029 (unverified) | 0.66 |
| 21 | `cfg_a788` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=1.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0 | 71/77/38 | 186 | 3.0% | 0.6% | 0.76 | -0.7% | 141 | 1.35 | 5.3% | 76.4 | 6/6 | 0.67 | 0.28 | 0.48 | 5 | 2.1% | 0.29 | 0.48 | 1.9% | 0.8% | -0.9% | 2.7%/1.9% | 2.4 (interpolated) | pass | 0.039 (unverified) | 0.15 |
| 22 | `cfg_6000` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/188/78 | 266 | 6.2% | 1.2% | 0.75 | -1.7% | 195 | 1.36 | 9.3% | 110.9 | 6/6 | 0.67 | 0.31 | 0.44 | 5 | 4.4% | 0.28 | 0.75 | 4.8% | 3.2% | 4.9% | 5.9%/4.2% | 3.0 (interpolated) | pass | 0.025 (unverified) | 0.20 |
| 23 | `cfg_4f16` | timeframe=15min, compression=bbkc, squeeze_length=35, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/336/260 | 596 | 8.8% | 1.7% | 0.77 | -2.4% | 455 | 1.22 | 23.4% | 248.4 | 7/7 | 0.71 | 0.14 | 0.63 | 5 | 4.0% | 0.55 | 0.64 | 5.6% | 2.2% | 0.5% | 8.1%/5.8% | 2.3 (interpolated) | pass | 0.031 (unverified) | 0.50 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 1.2% / 1.69 / 23 | 1.3% / 1.63 / 35 | 0.3% / 0.47 / 14 | 0.0% / 0.15 / 20 | 2.7% / 2.63 / 30 |
| 2 | 1.8% / 1.98 / 23 | 1.5% / 1.58 / 35 | 0.4% / 0.49 / 14 | 0.5% / 0.94 / 20 | 1.7% / 1.50 / 30 |
| 3 | 1.2% / 1.69 / 23 | 1.4% / 1.70 / 35 | 0.3% / 0.50 / 14 | 0.0% / 0.15 / 20 | 2.2% / 2.28 / 28 |
| 4 | 2.6% / 1.26 / 127 | 2.1% / 1.15 / 151 | 3.7% / 1.36 / 133 | -0.1% / -0.07 / 125 | 5.3% / 1.70 / 128 |
| 5 | 1.8% / 1.98 / 23 | 1.5% / 1.62 / 35 | 0.4% / 0.49 / 14 | 0.5% / 0.94 / 20 | 1.9% / 1.80 / 28 |
| 6 | 2.6% / 1.33 / 119 | 2.4% / 1.35 / 146 | 3.6% / 1.31 / 128 | -0.2% / -0.10 / 124 | 4.7% / 1.53 / 127 |
| 7 | 2.7% / 1.82 / 131 | 1.6% / 1.53 / 110 | 0.6% / 0.32 / 123 | -0.3% / -0.21 / 119 | 1.6% / 0.89 / 119 |
| 8 | 2.9% / 1.67 / 78 | 1.1% / 0.79 / 96 | 3.3% / 1.38 / 91 | -2.1% / -1.53 / 77 | 3.6% / 1.44 / 79 |
| 9 | 4.3% / 2.41 / 127 | 2.7% / 2.04 / 109 | 1.1% / 0.54 / 120 | -0.3% / -0.24 / 117 | -0.6% / -0.30 / 113 |
| 10 | 3.0% / 1.81 / 72 | 1.2% / 0.82 / 91 | 3.4% / 1.40 / 87 | -2.0% / -1.49 / 77 | 3.0% / 1.25 / 78 |
| 11 | 2.1% / 1.26 / 95 | -1.1% / -0.78 / 115 | 2.3% / 0.97 / 109 | -2.1% / -1.51 / 107 | 6.8% / 2.93 / 106 |
| 12 | 0.8% / 0.66 / 53 | 1.4% / 0.97 / 79 | 0.3% / 0.17 / 67 | 0.8% / 0.65 / 62 | 3.6% / 1.63 / 61 |
| 13 | 2.2% / 1.32 / 93 | -1.0% / -0.76 / 108 | 2.5% / 1.10 / 106 | -2.4% / -1.84 / 100 | 6.3% / 2.79 / 101 |
| 14 | 0.8% / 0.62 / 53 | 0.7% / 0.52 / 78 | 0.6% / 0.31 / 67 | 0.4% / 0.34 / 62 | 4.3% / 1.61 / 61 |
| 15 | 0.8% / 1.08 / 22 | 0.3% / 0.71 / 29 | 0.3% / 0.43 / 18 | 0.5% / 1.05 / 28 | 0.7% / 0.89 / 27 |
| 16 | 1.8% / 2.11 / 28 | -0.2% / -0.27 / 44 | 1.1% / 0.78 / 49 | -0.1% / -0.12 / 35 | 1.9% / 1.14 / 35 |
| 17 | -0.5% / -0.65 / 50 | 1.3% / 1.03 / 61 | 1.5% / 1.19 / 72 | 0.1% / 0.18 / 54 | 3.2% / 1.26 / 51 |
| 18 | 0.1% / 0.15 / 51 | 0.7% / 0.73 / 62 | 1.5% / 1.22 / 75 | 0.5% / 0.63 / 55 | 1.7% / 0.95 / 52 |
| 19 | 1.9% / 2.11 / 28 | -0.4% / -0.45 / 44 | 2.1% / 1.15 / 49 | -0.3% / -0.38 / 35 | 2.0% / 1.12 / 35 |
| 20 | 1.3% / 0.67 / 100 | 0.5% / 0.37 / 130 | 1.4% / 0.63 / 117 | 0.5% / 0.34 / 134 | 4.6% / 1.38 / 123 |
| 21 | 0.7% / 0.84 / 34 | 0.8% / 1.39 / 47 | 0.7% / 0.95 / 29 | 0.6% / 1.01 / 40 | 0.1% / 0.10 / 36 |
| 22 | 1.7% / 1.35 / 48 | 0.4% / 0.31 / 62 | 1.3% / 0.83 / 43 | 1.3% / 1.01 / 53 | 1.4% / 0.57 / 60 |
| 23 | 1.3% / 0.67 / 100 | 0.5% / 0.33 / 128 | 1.6% / 0.72 / 115 | 0.6% / 0.35 / 130 | 4.6% / 1.38 / 123 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_50ed` | 4 | 0.95 | 0.93/0.95 | 0.91/0.94 |
| 1 | `cfg_41ac` | 6 | 0.90 | 0.84/0.94 | 0.66/0.90 |
| 2 | `cfg_99dd` | 5 | 0.90 | 0.83/0.84 | 0.65/0.68 |
| 3 | `cfg_39c2` | 6 | 0.93 | 0.83/0.95 | 0.65/0.91 |
| 4 | `cfg_107f` | 3 | 0.95 | 0.92/0.94 | 0.76/0.78 |
| 5 | `cfg_75fe` | 4 | 0.93 | 0.92/0.95 | 0.89/0.93 |
| 6 | `cfg_e6d8` | 2 | 0.97 | 0.97/0.97 | 0.95/0.95 |
| 7 | `cfg_93fd` | 2 | 1.00 | 1.00/1.00 | 0.98/0.98 |
| 8 | `cfg_6000` | 1 | n/a | n/a/n/a | n/a/n/a |
| 9 | `cfg_90f6` | 2 | 0.89 | 0.86/0.86 | 0.82/0.82 |
| 10 | `cfg_a3e8` | 3 | 0.84 | 0.83/0.90 | 0.74/0.84 |
| 11 | `cfg_a788` | 1 | n/a | n/a/n/a | n/a/n/a |
| 12 | `cfg_f6e4` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.017e-03 over 3840 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 507.0, participation ratio 17.3, 95%-variance components 209 (rank bound T = 1259); raw grid 3840; raw + known prior 760656
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
