# Screening funnel -- cb_bbkc_es_v1 (development stages only)

- Code: `8a83056f1ab9` (dirty working tree: False, diff sha256 `e3b0c44298fc`)
- Config: `configs/funnel/cb_bbkc_funnel_es_v1.yaml` sha256 `ac223d8d0b3a7fe9`; seed 20261110
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'NQ': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `a044b7365df020ce` (63 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **False** -- No compression-breakout strategy has been selected or scored on ES 2023-2024. Other families were validated there (mean-reversion: combined_test, combined_v1, mr_es_v3, mr_es_v4, mr_es_v5, mr_es_v6_15m, mr_es_v6_1h, trades_v1; noise-band: nb_es_v1, nb_es_v1-v4, nb_es_v2, nb_es_v3, nb_es_v4), so the period has been looked at by the researcher, but not for this strategy.
- Holdout 2025+ previously inspected: **False** -- No compression-breakout metrics have been computed on ES 2025+. ES 2025+ bars were read for mean-reversion holdout scoring (combined_v1, mr_es_v6_1h, trades_v1); noise-band holdout scoring (nb_es_v4) per those families' data-access ledgers: different strategy families, so this is still the first test of this strategy, but the researcher has seen how that period treated them.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 20736 | 20736 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 20736 | 20736 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 20736 | 17317 | 3419 | 0 |  | 18122 | 83.51 | 83.51 |  |
| 3 performance & risk | hard_gate | 17317 | 254 | 17063 | 0 |  | 0 | 1.22 | 1.47 |  |
| 4 parameter stability | hard_gate | 254 | 240 | 14 | 0 |  | 0 | 1.16 | 94.49 |  |
| 5 time stability | hard_gate | 240 | 240 | 0 | 0 |  | 207 | 1.16 | 100.00 |  |
| 6 deduplication | dedup | 240 | 63 |  |  | 177 |  | 0.30 | 26.25 | best 2 per cluster |
| 7 execution stress | hard_gate | 63 | 63 | 0 | 0 |  | 2 | 0.30 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 63 |  |  |  |  |  |  |  | diagnostic only: unverified: 63 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 3419 |
| s2:hard_reject:years_with_>=10_trades | 2328 |
| s3:hard_reject:max_drawdown | 1298 |
| s3:hard_reject:net_return | 11553 |
| s3:hard_reject:sharpe | 17063 |
| s4:hard_reject:local_median_sharpe | 14 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | target/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | NQ dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_1532` | timeframe=15min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=box, target_r=1.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 293/32/200 | 525 | 29.9% | 5.4% | 1.83 | -2.7% | 513 | 1.60 | 10.4% | 244.3 | 7/7 | 0.71 | 0.71 | 1.12 | 4 | 15.7% | 0.42 | 0.23 | 24.3% | 18.1% | 14.3% | 26.2%/23.5% | 3.9 (interpolated) | pass | 0.473 (unverified) | 0.52 |
| 2 | `cfg_1445` | timeframe=15min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=box, target_r=1.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 293/32/200 | 525 | 29.9% | 5.4% | 1.83 | -2.7% | 513 | 1.60 | 10.4% | 244.3 | 7/7 | 0.71 | 0.69 | 1.14 | 4 | 15.7% | 0.42 | 0.23 | 24.2% | 18.1% | 14.3% | 26.9%/23.6% | 3.9 (interpolated) | pass | 0.470 (unverified) | 0.52 |
| 3 | `cfg_289a` | timeframe=15min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=box, target_r=2.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 137/122/242 | 501 | 41.2% | 7.2% | 1.78 | -3.4% | 221 | 1.65 | 16.5% | 230.9 | 8/8 | 0.75 | 1.26 | 0.52 | 5 | 22.1% | 0.39 | 0.29 | 35.2% | 30.1% | 22.7% | 36.2%/31.3% | 5.1 (interpolated) | pass | 0.424 (unverified) | 0.79 |
| 4 | `cfg_efa5` | timeframe=15min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=box, target_r=2.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 137/122/242 | 501 | 41.1% | 7.1% | 1.77 | -3.4% | 221 | 1.65 | 16.5% | 230.9 | 8/8 | 0.75 | 1.26 | 0.52 | 5 | 22.0% | 0.39 | 0.29 | 35.1% | 30.0% | 22.7% | 36.2%/32.2% | 5.1 (interpolated) | pass | 0.421 (unverified) | 0.79 |
| 5 | `cfg_0d6a` | timeframe=15min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=box, target_r=3.0, direction=long, trend_filter=none, min_box_atr=0.0 | 114/279/428 | 821 | 47.7% | 8.1% | 1.23 | -9.1% | 217 | 1.31 | 29.9% | 385.5 | 8/8 | 0.88 | 0.90 | 0.33 | 5 | 28.1% | 0.40 | 0.34 | 39.7% | 29.1% | 10.6% | 43.1%/34.2% | 3.9 (interpolated) | pass | 0.072 (unverified) | 0.39 |
| 6 | `cfg_f925` | timeframe=15min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=box, target_r=3.0, direction=long, trend_filter=none, min_box_atr=0.0 | 113/280/428 | 821 | 47.8% | 8.1% | 1.24 | -9.1% | 217 | 1.31 | 30.0% | 385.3 | 8/8 | 0.88 | 0.90 | 0.34 | 5 | 28.2% | 0.40 | 0.33 | 39.6% | 29.1% | 10.7% | 42.6%/34.2% | 3.9 (interpolated) | pass | 0.074 (unverified) | 0.39 |
| 7 | `cfg_ec8f` | timeframe=15min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=box, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 481/56/347 | 884 | 34.1% | 6.0% | 1.29 | -6.4% | 296 | 1.29 | 16.5% | 407.2 | 7/7 | 0.86 | 0.28 | 1.01 | 4 | 18.2% | 0.41 | 0.27 | 24.8% | 15.5% | 1.6% | 30.9%/25.4% | 3.0 (interpolated) | pass | 0.104 (unverified) | -0.21 |
| 8 | `cfg_034d` | timeframe=15min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=box, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0 | 480/56/348 | 884 | 33.6% | 6.0% | 1.27 | -6.4% | 298 | 1.29 | 16.6% | 407.7 | 7/7 | 0.86 | 0.27 | 1.00 | 4 | 17.7% | 0.42 | 0.28 | 24.2% | 15.0% | 1.5% | 29.6%/24.3% | 3.0 (interpolated) | pass | 0.097 (unverified) | -0.19 |
| 9 | `cfg_ce0e` | timeframe=5min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=3, stop=box, target_r=3.0, direction=both, trend_filter=ema50, min_box_atr=0.5 | 159/473/693 | 1325 | 58.8% | 9.7% | 1.15 | -8.2% | 373 | 1.20 | 40.9% | 620.4 | 8/8 | 0.75 | 0.77 | 0.38 | 4 | 31.4% | 0.47 | 0.34 | 42.2% | 25.8% | 55.9% | 50.0%/41.7% | 3.0 (interpolated) | pass | 0.049 (unverified) | 0.45 |
| 10 | `cfg_8f18` | timeframe=5min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=6, stop=box, target_r=3.0, direction=both, trend_filter=ema50, min_box_atr=0.5 | 158/474/694 | 1326 | 59.3% | 9.8% | 1.16 | -8.3% | 373 | 1.20 | 41.0% | 619.8 | 8/8 | 0.75 | 0.78 | 0.37 | 3 | 31.0% | 0.48 | 0.33 | 42.5% | 26.3% | 57.3% | 52.6%/41.1% | 3.1 (interpolated) | pass | 0.050 (unverified) | 0.44 |
| 11 | `cfg_8e84` | timeframe=15min, compression=bbkc, squeeze_length=20, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=box, target_r=3.0, direction=long, trend_filter=ema50, min_box_atr=0.0 | 62/160/253 | 475 | 21.8% | 4.0% | 0.97 | -4.2% | 296 | 1.34 | 15.0% | 219.3 | 9/9 | 0.89 | 0.81 | 0.16 | 4 | 13.2% | 0.39 | 0.49 | 17.0% | 11.6% | 10.6% | 20.2%/16.5% | 3.5 (interpolated) | pass | 0.016 (unverified) | 0.96 |
| 12 | `cfg_a4d4` | timeframe=5min, compression=bbkc, squeeze_length=10, kc_mult=1.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=2.0, target_r=none, direction=both, trend_filter=ema50, min_box_atr=0.0 | 0/677/729 | 1406 | 58.8% | 9.7% | 1.13 | -8.1% | 445 | 1.20 | 45.1% | 653.2 | 7/7 | 0.86 | 0.68 | 0.45 | 3 | 23.5% | 0.54 | 0.36 | 41.1% | 25.8% | 26.1% | 52.3%/43.4% | 3.0 (interpolated) | pass | 0.041 (unverified) | 1.10 |
| 13 | `cfg_404d` | timeframe=5min, compression=bbkc, squeeze_length=10, kc_mult=1.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=2.0, target_r=none, direction=both, trend_filter=ema50, min_box_atr=0.0 | 0/678/734 | 1412 | 56.9% | 9.4% | 1.10 | -8.7% | 457 | 1.19 | 45.2% | 657.9 | 7/7 | 0.86 | 0.64 | 0.46 | 3 | 22.9% | 0.54 | 0.37 | 39.0% | 23.6% | 23.9% | 49.0%/41.2% | 2.9 (interpolated) | pass | 0.035 (unverified) | 1.10 |
| 14 | `cfg_450b` | timeframe=15min, compression=bbkc, squeeze_length=20, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=box, target_r=3.0, direction=long, trend_filter=ema50, min_box_atr=0.5 | 61/164/250 | 475 | 22.0% | 4.1% | 0.96 | -4.0% | 296 | 1.34 | 15.1% | 220.0 | 9/9 | 0.89 | 0.86 | 0.11 | 4 | 13.5% | 0.39 | 0.48 | 17.4% | 11.9% | 12.4% | 20.5%/16.8% | 3.5 (interpolated) | pass | 0.017 (unverified) | 1.04 |
| 15 | `cfg_c898` | timeframe=5min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=6, stop=2.0, target_r=3.0, direction=both, trend_filter=ema50, min_box_atr=0.5 | 145/490/696 | 1331 | 50.7% | 8.6% | 1.00 | -10.3% | 481 | 1.18 | 41.4% | 620.5 | 8/8 | 0.88 | 0.75 | 0.25 | 4 | 20.7% | 0.59 | 0.39 | 35.9% | 22.9% | 31.5% | 44.1%/32.3% | 2.9 (interpolated) | pass | 0.023 (unverified) | 0.43 |
| 16 | `cfg_742a` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/286/367 | 653 | 37.7% | 6.6% | 0.99 | -8.5% | 561 | 1.29 | 25.1% | 306.3 | 7/7 | 0.86 | 0.47 | 0.52 | 4 | 22.2% | 0.41 | 0.43 | 30.8% | 22.5% | 13.9% | 35.8%/27.9% | 3.9 (interpolated) | pass | 0.020 (unverified) | 1.16 |
| 17 | `cfg_51bf` | timeframe=5min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=3, stop=2.0, target_r=3.0, direction=both, trend_filter=ema50, min_box_atr=0.5 | 146/489/694 | 1329 | 52.0% | 8.7% | 1.01 | -10.0% | 481 | 1.18 | 41.4% | 620.4 | 8/8 | 0.88 | 0.74 | 0.27 | 4 | 22.0% | 0.58 | 0.38 | 34.8% | 22.5% | 30.9% | 47.5%/32.6% | 2.9 (interpolated) | pass | 0.025 (unverified) | 0.41 |
| 18 | `cfg_c8cf` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=box, target_r=3.0, direction=both, trend_filter=none, min_box_atr=0.0 | 112/180/363 | 655 | 35.6% | 6.3% | 0.95 | -7.0% | 142 | 1.28 | 21.7% | 303.9 | 8/8 | 0.88 | 0.49 | 0.46 | 5 | 24.4% | 0.31 | 0.48 | 28.8% | 20.1% | 9.3% | 32.9%/25.4% | 3.7 (interpolated) | pass | 0.014 (unverified) | 1.50 |
| 19 | `cfg_0f1f` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/287/370 | 657 | 36.9% | 6.5% | 0.97 | -8.6% | 561 | 1.28 | 25.3% | 308.3 | 7/7 | 0.86 | 0.47 | 0.50 | 4 | 21.6% | 0.41 | 0.44 | 30.4% | 21.8% | 13.5% | 33.4%/27.5% | 3.9 (interpolated) | pass | 0.018 (unverified) | 1.09 |
| 20 | `cfg_e41c` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=box, target_r=3.0, direction=both, trend_filter=none, min_box_atr=0.0 | 112/181/366 | 659 | 35.1% | 6.2% | 0.94 | -7.0% | 147 | 1.28 | 21.9% | 306.3 | 8/8 | 0.88 | 0.48 | 0.46 | 5 | 23.7% | 0.32 | 0.48 | 28.5% | 19.0% | 9.0% | 31.1%/24.8% | 3.6 (interpolated) | pass | 0.014 (unverified) | 1.43 |
| 21 | `cfg_8a64` | timeframe=5min, compression=bbkc, squeeze_length=10, kc_mult=1.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=2.0, target_r=none, direction=short, trend_filter=ema50, min_box_atr=0.0 | 0/279/328 | 607 | 39.4% | 6.9% | 1.00 | -6.6% | 286 | 1.29 | 18.3% | 282.7 | 7/7 | 0.86 | 0.71 | 0.29 | 3 | 13.5% | 0.62 | 0.48 | 32.4% | 25.0% | 21.4% | 34.1%/28.5% | 4.3 (interpolated) | pass | 0.017 (unverified) | 0.62 |
| 22 | `cfg_307b` | timeframe=5min, compression=bbkc, squeeze_length=10, kc_mult=1.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=2.0, target_r=none, direction=short, trend_filter=ema50, min_box_atr=0.0 | 0/278/327 | 605 | 40.1% | 7.0% | 1.01 | -6.3% | 286 | 1.30 | 18.2% | 281.9 | 7/7 | 0.86 | 0.71 | 0.30 | 3 | 13.9% | 0.62 | 0.47 | 33.1% | 25.3% | 21.5% | 35.1%/27.9% | 4.4 (interpolated) | pass | 0.019 (unverified) | 0.62 |
| 23 | `cfg_4c71` | timeframe=5min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=3, stop=2.0, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.5 | 0/372/351 | 723 | 29.6% | 5.3% | 0.90 | -5.6% | 378 | 1.24 | 25.7% | 337.0 | 7/7 | 0.86 | 0.56 | 0.34 | 5 | 14.5% | 0.45 | 0.62 | 21.0% | 14.7% | 31.0% | 27.1%/19.6% | 3.2 (interpolated) | pass | 0.008 (unverified) | 0.74 |
| 24 | `cfg_5efa` | timeframe=5min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=6, stop=2.0, target_r=none, direction=long, trend_filter=ema50, min_box_atr=0.0 | 0/372/351 | 723 | 29.6% | 5.3% | 0.90 | -5.6% | 378 | 1.24 | 25.7% | 337.0 | 7/7 | 0.86 | 0.55 | 0.35 | 5 | 14.5% | 0.45 | 0.62 | 21.0% | 14.7% | 31.0% | 26.7%/19.0% | 3.2 (interpolated) | pass | 0.008 (unverified) | 0.72 |
| 25 | `cfg_458e` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=close, setup_expiry_bars=3, stop=2.0, target_r=none, direction=short, trend_filter=ema50, min_box_atr=0.0 | 0/128/56 | 184 | 26.1% | 4.8% | 0.99 | -8.1% | 545 | 1.59 | 8.0% | 85.9 | 7/7 | 0.71 | 0.52 | 0.47 | 4 | 12.7% | 0.51 | 0.48 | 23.8% | 21.8% | 16.8% | 23.8%/19.5% | 8.4 (interpolated) | pass | 0.024 (unverified) | 0.69 |
| 26 | `cfg_b47e` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=close, setup_expiry_bars=3, stop=2.0, target_r=3.0, direction=short, trend_filter=ema50, min_box_atr=0.0 | 13/115/56 | 184 | 24.1% | 4.4% | 0.95 | -8.3% | 471 | 1.55 | 7.8% | 85.7 | 8/8 | 0.75 | 0.66 | 0.29 | 4 | 12.0% | 0.50 | 0.48 | 22.1% | 20.5% | 13.8% | 21.9%/17.6% | 8.2 (interpolated) | pass | 0.021 (unverified) | 0.74 |
| 27 | `cfg_de6e` | timeframe=5min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=2.0, target_r=none, direction=both, trend_filter=ema50, min_box_atr=0.0 | 0/558/685 | 1243 | 48.5% | 8.2% | 0.90 | -10.0% | 730 | 1.17 | 43.3% | 579.4 | 7/7 | 1.00 | 0.73 | 0.17 | 4 | 23.6% | 0.51 | 0.39 | 34.3% | 22.0% | 13.1% | 41.7%/32.3% | 2.8 (interpolated) | pass | 0.013 (unverified) | 0.70 |
| 28 | `cfg_213d` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=both, trend_filter=none, min_box_atr=0.5 | 0/265/394 | 659 | 26.5% | 4.8% | 0.82 | -7.6% | 520 | 1.22 | 20.0% | 308.8 | 7/7 | 0.71 | 0.48 | 0.34 | 3 | 8.2% | 0.64 | 0.58 | 20.1% | 13.9% | 15.5% | 24.2%/16.4% | 3.1 (interpolated) | pass | 0.006 (unverified) | 0.76 |
| 29 | `cfg_e3a1` | timeframe=5min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=2.0, target_r=none, direction=both, trend_filter=ema50, min_box_atr=0.0 | 0/558/684 | 1242 | 48.8% | 8.3% | 0.90 | -10.0% | 729 | 1.18 | 43.3% | 579.0 | 7/7 | 1.00 | 0.72 | 0.18 | 4 | 23.8% | 0.51 | 0.39 | 34.3% | 22.2% | 13.2% | 42.9%/34.2% | 2.8 (interpolated) | pass | 0.013 (unverified) | 0.70 |
| 30 | `cfg_4e49` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=box, target_r=3.0, direction=long, trend_filter=none, min_box_atr=0.0 | 49/121/188 | 358 | 23.8% | 4.4% | 0.94 | -6.7% | 265 | 1.40 | 12.9% | 167.4 | 8/8 | 0.88 | 0.69 | 0.26 | 4 | 11.0% | 0.52 | 0.63 | 19.1% | 15.3% | 8.8% | 21.8%/17.0% | 4.6 (interpolated) | pass | 0.011 (unverified) | 1.05 |
| 31 | `cfg_f6c8` | timeframe=5min, compression=bbkc, squeeze_length=10, kc_mult=1.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=2.0, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/857/992 | 1849 | 61.1% | 10.0% | 0.91 | -10.0% | 277 | 1.14 | 63.9% | 863.8 | 7/7 | 0.71 | 0.47 | 0.44 | 4 | 17.3% | 0.67 | 0.44 | 39.9% | 19.2% | 19.6% | 59.7%/41.4% | 2.6 (interpolated) | pass | 0.013 (unverified) | 0.65 |
| 32 | `cfg_24c9` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=box, target_r=3.0, direction=long, trend_filter=none, min_box_atr=0.0 | 49/122/190 | 361 | 23.8% | 4.4% | 0.95 | -6.5% | 265 | 1.40 | 13.0% | 168.7 | 8/8 | 0.88 | 0.67 | 0.28 | 4 | 11.0% | 0.52 | 0.62 | 18.6% | 15.1% | 8.8% | 21.1%/17.2% | 4.5 (interpolated) | pass | 0.011 (unverified) | 1.05 |
| 33 | `cfg_d06d` | timeframe=5min, compression=bbkc, squeeze_length=10, kc_mult=1.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=2.0, target_r=none, direction=both, trend_filter=none, min_box_atr=0.5 | 0/861/992 | 1853 | 60.7% | 10.0% | 0.91 | -12.5% | 292 | 1.14 | 64.0% | 865.2 | 7/7 | 0.71 | 0.56 | 0.35 | 4 | 15.2% | 0.69 | 0.44 | 36.7% | 20.1% | 18.1% | 53.0%/36.3% | 2.6 (interpolated) | pass | 0.013 (unverified) | 0.64 |
| 34 | `cfg_c973` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=3.0, direction=both, trend_filter=none, min_box_atr=0.5 | 111/162/388 | 661 | 22.9% | 4.2% | 0.77 | -5.7% | 332 | 1.20 | 17.3% | 306.4 | 8/8 | 0.88 | 0.55 | 0.22 | 4 | 14.1% | 0.38 | 0.63 | 15.9% | 10.2% | 14.2% | 20.8%/15.0% | 2.9 (interpolated) | pass | 0.005 (unverified) | 0.67 |
| 35 | `cfg_dcbd` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=close, setup_expiry_bars=3, stop=2.0, target_r=3.0, direction=short, trend_filter=none, min_box_atr=0.0 | 21/174/104 | 299 | 25.0% | 4.6% | 0.88 | -6.6% | 470 | 1.38 | 13.0% | 138.4 | 8/8 | 0.75 | 0.63 | 0.26 | 4 | 9.2% | 0.63 | 0.48 | 22.2% | 18.2% | 16.2% | 23.1%/16.6% | 5.5 (interpolated) | pass | 0.014 (unverified) | 0.75 |
| 36 | `cfg_12bd` | timeframe=15min, compression=bbkc, squeeze_length=20, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=box, target_r=3.0, direction=long, trend_filter=none, min_box_atr=0.0 | 94/225/381 | 700 | 23.8% | 4.4% | 0.80 | -6.4% | 244 | 1.21 | 21.9% | 326.0 | 9/9 | 0.89 | 0.65 | 0.15 | 5 | 13.0% | 0.41 | 0.51 | 16.2% | 10.2% | 3.9% | 21.9%/16.9% | 2.8 (interpolated) | pass | 0.007 (unverified) | 0.75 |
| 37 | `cfg_e6ff` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=close, setup_expiry_bars=3, stop=2.0, target_r=none, direction=short, trend_filter=none, min_box_atr=0.5 | 0/193/104 | 297 | 23.7% | 4.3% | 0.84 | -9.1% | 591 | 1.36 | 13.3% | 137.4 | 7/7 | 0.71 | 0.54 | 0.30 | 3 | 5.8% | 0.76 | 0.53 | 18.9% | 16.2% | 14.0% | 20.7%/15.3% | 5.2 (interpolated) | pass | 0.010 (unverified) | 0.60 |
| 38 | `cfg_24a6` | timeframe=15min, compression=bbkc, squeeze_length=20, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=box, target_r=3.0, direction=long, trend_filter=none, min_box_atr=0.0 | 94/226/382 | 702 | 23.8% | 4.4% | 0.79 | -6.4% | 257 | 1.21 | 22.0% | 326.9 | 9/9 | 0.89 | 0.65 | 0.15 | 5 | 13.0% | 0.41 | 0.51 | 16.2% | 10.2% | 3.9% | 21.5%/16.5% | 2.8 (interpolated) | pass | 0.007 (unverified) | 0.75 |
| 39 | `cfg_91b0` | timeframe=15min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=box, target_r=2.0, direction=both, trend_filter=ema50, min_box_atr=0.5 | 253/170/459 | 882 | 33.7% | 6.0% | 0.88 | -7.8% | 300 | 1.21 | 26.1% | 413.3 | 8/8 | 0.75 | 0.52 | 0.36 | 4 | 20.4% | 0.39 | 0.42 | 22.5% | 12.6% | 10.2% | 30.6%/21.5% | 2.9 (interpolated) | pass | 0.013 (unverified) | 0.21 |
| 40 | `cfg_b0ad` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=box, target_r=3.0, direction=both, trend_filter=ema50, min_box_atr=0.5 | 63/116/213 | 392 | 20.8% | 3.8% | 0.80 | -5.2% | 212 | 1.29 | 13.2% | 182.9 | 8/8 | 0.75 | 0.42 | 0.38 | 5 | 12.0% | 0.38 | 0.71 | 16.1% | 12.5% | 6.0% | 19.1%/14.8% | 4.0 (interpolated) | pass | 0.005 (unverified) | 1.47 |
| 41 | `cfg_f198` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=box, target_r=3.0, direction=both, trend_filter=ema50, min_box_atr=0.5 | 63/117/215 | 395 | 20.7% | 3.8% | 0.79 | -5.7% | 214 | 1.29 | 13.4% | 184.4 | 8/8 | 0.75 | 0.41 | 0.38 | 5 | 11.9% | 0.39 | 0.71 | 15.7% | 12.4% | 4.8% | 18.7%/13.1% | 3.9 (interpolated) | pass | 0.005 (unverified) | 1.43 |
| 42 | `cfg_b52e` | timeframe=15min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=box, target_r=2.0, direction=both, trend_filter=ema50, min_box_atr=0.5 | 253/170/458 | 881 | 33.7% | 6.0% | 0.89 | -7.9% | 300 | 1.21 | 26.0% | 413.0 | 8/8 | 0.75 | 0.52 | 0.37 | 4 | 20.4% | 0.39 | 0.42 | 22.4% | 12.7% | 10.6% | 29.5%/23.2% | 2.9 (interpolated) | pass | 0.013 (unverified) | 0.21 |
| 43 | `cfg_a588` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=close, setup_expiry_bars=3, stop=2.0, target_r=2.0, direction=both, trend_filter=ema50, min_box_atr=0.5 | 47/277/158 | 482 | 27.3% | 5.0% | 0.85 | -7.3% | 250 | 1.27 | 20.0% | 223.7 | 8/8 | 0.75 | 0.51 | 0.34 | 4 | 16.2% | 0.41 | 0.50 | 22.8% | 18.4% | 8.1% | 24.2%/18.2% | 4.1 (interpolated) | pass | 0.010 (unverified) | 0.70 |
| 44 | `cfg_d258` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=close, setup_expiry_bars=3, stop=2.0, target_r=2.0, direction=both, trend_filter=ema50, min_box_atr=0.0 | 47/281/156 | 484 | 30.9% | 5.5% | 0.93 | -5.1% | 222 | 1.30 | 20.2% | 225.2 | 8/8 | 0.75 | 0.55 | 0.37 | 5 | 19.4% | 0.37 | 0.48 | 25.5% | 21.1% | 10.8% | 27.2%/20.4% | 4.3 (interpolated) | pass | 0.015 (unverified) | 0.73 |
| 45 | `cfg_40fa` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=close, setup_expiry_bars=3, stop=2.0, target_r=none, direction=both, trend_filter=ema50, min_box_atr=0.5 | 0/323/159 | 482 | 27.0% | 4.9% | 0.85 | -8.0% | 561 | 1.27 | 20.8% | 223.5 | 7/7 | 0.57 | 0.41 | 0.44 | 4 | 15.4% | 0.43 | 0.46 | 22.5% | 18.0% | 9.8% | 24.6%/18.5% | 4.1 (interpolated) | pass | 0.012 (unverified) | 0.65 |
| 46 | `cfg_59ca` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=close, setup_expiry_bars=3, stop=2.0, target_r=3.0, direction=both, trend_filter=ema50, min_box_atr=0.5 | 17/306/159 | 482 | 25.7% | 4.7% | 0.83 | -7.4% | 561 | 1.26 | 20.5% | 223.2 | 8/8 | 0.62 | 0.52 | 0.31 | 4 | 14.7% | 0.43 | 0.44 | 21.2% | 17.0% | 8.1% | 24.8%/18.0% | 3.8 (interpolated) | pass | 0.011 (unverified) | 0.79 |
| 47 | `cfg_08df` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=close, setup_expiry_bars=3, stop=2.0, target_r=3.0, direction=both, trend_filter=none, min_box_atr=0.0 | 27/394/218 | 639 | 30.0% | 5.4% | 0.79 | -7.0% | 310 | 1.21 | 28.1% | 297.1 | 8/8 | 0.75 | 0.53 | 0.26 | 5 | 18.2% | 0.39 | 0.50 | 23.2% | 16.3% | 16.2% | 26.7%/20.7% | 3.5 (interpolated) | pass | 0.008 (unverified) | 0.89 |
| 48 | `cfg_f249` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=close, setup_expiry_bars=3, stop=2.0, target_r=1.0, direction=short, trend_filter=ema50, min_box_atr=0.0 | 82/53/51 | 186 | 18.6% | 3.5% | 0.83 | -3.6% | 242 | 1.48 | 5.5% | 86.7 | 7/7 | 0.57 | 0.57 | 0.26 | 5 | 10.9% | 0.41 | 0.65 | 16.3% | 14.3% | 9.3% | 17.4%/11.7% | 6.5 (interpolated) | pass | 0.010 (unverified) | 0.61 |
| 49 | `cfg_f1f2` | timeframe=5min, compression=bbkc, squeeze_length=20, kc_mult=1.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=1.0, target_r=none, direction=short, trend_filter=ema50, min_box_atr=0.0 | 0/37/102 | 139 | 10.5% | 2.0% | 0.78 | -2.0% | 380 | 1.71 | 2.3% | 64.1 | 8/8 | 0.62 | 0.45 | 0.32 | 4 | 4.2% | 0.58 | 0.98 | 9.4% | 7.8% | 10.7% | 9.5%/6.6% | 5.1 (interpolated) | pass | 0.001 (unverified) | 0.56 |
| 50 | `cfg_8230` | timeframe=15min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=1.0, target_r=2.0, direction=long, trend_filter=ema50, min_box_atr=0.5 | 144/90/289 | 523 | 16.1% | 3.0% | 0.82 | -4.9% | 513 | 1.24 | 14.3% | 241.8 | 8/8 | 0.75 | 0.45 | 0.36 | 4 | 7.3% | 0.53 | 0.65 | 11.2% | 5.9% | 15.0% | 14.4%/10.3% | 2.6 (interpolated) | pass | 0.012 (unverified) | -0.05 |
| 51 | `cfg_c10e` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=close, setup_expiry_bars=3, stop=2.0, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/421/218 | 639 | 31.0% | 5.5% | 0.79 | -7.4% | 310 | 1.21 | 28.6% | 298.4 | 7/7 | 0.71 | 0.42 | 0.37 | 3 | 17.2% | 0.44 | 0.50 | 23.5% | 17.9% | 18.1% | 27.5%/22.6% | 3.5 (interpolated) | pass | 0.008 (unverified) | 0.85 |
| 52 | `cfg_c387` | timeframe=5min, compression=bbkc, squeeze_length=10, kc_mult=1.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=1.0, target_r=none, direction=both, trend_filter=ema50, min_box_atr=0.0 | 0/467/1232 | 1699 | 35.1% | 6.2% | 0.86 | -11.3% | 358 | 1.15 | 34.1% | 791.8 | 7/7 | 0.86 | 0.40 | 0.46 | 3 | 13.8% | 0.56 | 0.49 | 17.2% | -0.2% | 4.6% | 31.6%/25.1% | 2.0 (interpolated) | pass | 0.009 (unverified) | 1.10 |
| 53 | `cfg_f58b` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=both, trend_filter=ema50, min_box_atr=0.5 | 0/211/282 | 493 | 19.5% | 3.6% | 0.76 | -9.3% | 610 | 1.23 | 15.0% | 228.3 | 7/7 | 0.71 | 0.45 | 0.30 | 4 | 5.9% | 0.66 | 0.60 | 14.2% | 10.1% | 10.6% | 17.4%/12.2% | 3.3 (interpolated) | pass | 0.005 (unverified) | 0.88 |
| 54 | `cfg_ce73` | timeframe=5min, compression=bbkc, squeeze_length=20, kc_mult=1.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=box, target_r=none, direction=short, trend_filter=ema50, min_box_atr=0.5 | 0/42/95 | 137 | 11.1% | 2.1% | 0.83 | -1.6% | 325 | 1.79 | 2.2% | 63.1 | 8/8 | 0.75 | 0.46 | 0.37 | 4 | 6.2% | 0.42 | 0.90 | 10.0% | 8.5% | 7.1% | 10.4%/7.9% | 5.5 (interpolated) | pass | 0.001 (unverified) | 0.56 |
| 55 | `cfg_a6fa` | timeframe=5min, compression=bbkc, squeeze_length=10, kc_mult=1.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=1.0, target_r=none, direction=both, trend_filter=ema50, min_box_atr=0.0 | 0/468/1236 | 1704 | 32.5% | 5.8% | 0.82 | -11.5% | 367 | 1.14 | 34.2% | 794.1 | 7/7 | 0.86 | 0.38 | 0.43 | 3 | 13.3% | 0.54 | 0.53 | 16.8% | -1.6% | 2.5% | 28.8%/20.9% | 2.0 (interpolated) | pass | 0.007 (unverified) | 1.12 |
| 56 | `cfg_e9ae` | timeframe=5min, compression=bbkc, squeeze_length=20, kc_mult=1.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=6, stop=box, target_r=2.0, direction=both, trend_filter=ema50, min_box_atr=0.5 | 78/33/126 | 237 | 8.3% | 1.6% | 0.81 | -2.0% | 399 | 1.42 | 3.7% | 107.9 | 9/9 | 0.67 | 0.20 | 0.61 | 4 | 4.0% | 0.50 | 0.69 | 6.0% | 3.9% | 5.7% | 7.6%/5.9% | 3.1 (interpolated) | pass | 0.003 (unverified) | 0.84 |
| 57 | `cfg_4363` | timeframe=5min, compression=bbkc, squeeze_length=20, kc_mult=1.0, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=3, stop=box, target_r=3.0, direction=both, trend_filter=ema50, min_box_atr=0.5 | 43/54/131 | 228 | 9.0% | 1.7% | 0.77 | -2.3% | 394 | 1.44 | 4.1% | 103.8 | 9/9 | 0.78 | 0.31 | 0.45 | 4 | 3.6% | 0.58 | 0.82 | 7.0% | 4.7% | 6.8% | 8.8%/6.1% | 3.3 (interpolated) | pass | 0.001 (unverified) | 0.74 |
| 58 | `cfg_2eb7` | timeframe=15min, compression=bbkc, squeeze_length=10, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=1.0, target_r=2.0, direction=long, trend_filter=ema50, min_box_atr=0.5 | 144/90/288 | 522 | 16.1% | 3.0% | 0.82 | -4.9% | 513 | 1.24 | 14.3% | 241.4 | 8/8 | 0.75 | 0.46 | 0.36 | 4 | 7.4% | 0.53 | 0.65 | 11.3% | 6.0% | 15.0% | 14.7%/9.9% | 2.6 (interpolated) | pass | 0.012 (unverified) | -0.05 |
| 59 | `cfg_0ced` | timeframe=15min, compression=bbkc, squeeze_length=10, kc_mult=1.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=6, stop=box, target_r=2.0, direction=short, trend_filter=ema50, min_box_atr=0.5 | 82/37/135 | 254 | 14.9% | 2.8% | 0.79 | -4.9% | 651 | 1.33 | 4.7% | 117.9 | 8/8 | 0.88 | 0.32 | 0.47 | 3 | 6.9% | 0.51 | 0.70 | 13.0% | 10.7% | 2.5% | 13.4%/9.9% | 4.5 (interpolated) | pass | 0.005 (unverified) | 0.55 |
| 60 | `cfg_1c02` | timeframe=15min, compression=bbkc, squeeze_length=10, kc_mult=1.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=3, stop=box, target_r=2.0, direction=short, trend_filter=ema50, min_box_atr=0.5 | 82/37/135 | 254 | 14.9% | 2.8% | 0.79 | -4.9% | 651 | 1.33 | 4.7% | 117.9 | 8/8 | 0.88 | 0.32 | 0.47 | 3 | 6.9% | 0.51 | 0.70 | 13.0% | 10.7% | 2.5% | 13.4%/9.6% | 4.5 (interpolated) | pass | 0.005 (unverified) | 0.55 |
| 61 | `cfg_d5a4` | timeframe=15min, compression=bbkc, squeeze_length=30, kc_mult=2.0, min_squeeze_bars=1, entry_type=close, setup_expiry_bars=3, stop=2.0, target_r=1.0, direction=both, trend_filter=ema50, min_box_atr=0.0 | 165/173/149 | 487 | 24.4% | 4.5% | 0.81 | -4.8% | 225 | 1.26 | 16.6% | 227.9 | 7/7 | 0.57 | 0.49 | 0.32 | 4 | 10.5% | 0.54 | 0.56 | 17.9% | 12.9% | 8.5% | 20.5%/14.2% | 3.5 (interpolated) | pass | 0.010 (unverified) | 0.65 |
| 62 | `cfg_9d4f` | timeframe=15min, compression=bbkc, squeeze_length=20, kc_mult=1.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=6, stop=1.0, target_r=3.0, direction=long, trend_filter=none, min_box_atr=0.5 | 34/90/151 | 275 | 18.0% | 3.4% | 0.89 | -4.1% | 224 | 1.46 | 6.4% | 127.9 | 10/10 | 0.70 | 0.25 | 0.64 | 5 | 10.4% | 0.40 | 0.68 | 15.1% | 11.7% | 13.9% | 15.8%/9.6% | 4.5 (interpolated) | pass | 0.003 (unverified) | 0.21 |
| 63 | `cfg_9597` | timeframe=15min, compression=bbkc, squeeze_length=20, kc_mult=1.5, min_squeeze_bars=4, entry_type=wick, setup_expiry_bars=3, stop=1.0, target_r=3.0, direction=long, trend_filter=none, min_box_atr=0.5 | 34/88/149 | 271 | 17.4% | 3.3% | 0.87 | -4.1% | 224 | 1.45 | 6.3% | 125.9 | 10/10 | 0.70 | 0.31 | 0.56 | 5 | 10.0% | 0.41 | 0.69 | 14.8% | 12.3% | 13.2% | 15.6%/10.9% | 4.5 (interpolated) | pass | 0.003 (unverified) | 0.18 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 2.0% / 0.94 / 99 | -0.3% / -0.13 / 111 | 12.3% / 2.96 / 104 | 7.1% / 2.98 / 126 | 6.2% / 1.76 / 85 |
| 2 | 2.0% / 0.94 / 99 | -0.3% / -0.15 / 111 | 12.3% / 2.96 / 104 | 7.1% / 2.98 / 126 | 6.2% / 1.76 / 85 |
| 3 | 2.7% / 0.95 / 96 | 0.7% / 0.26 / 106 | 15.7% / 2.53 / 97 | 7.5% / 2.58 / 119 | 9.8% / 2.14 / 83 |
| 4 | 2.7% / 0.95 / 96 | 0.6% / 0.23 / 106 | 15.7% / 2.53 / 97 | 7.4% / 2.56 / 119 | 9.9% / 2.15 / 83 |
| 5 | 2.2% / 0.43 / 166 | 7.0% / 1.63 / 164 | 15.0% / 1.54 / 157 | 15.3% / 3.27 / 169 | 1.9% / 0.29 / 165 |
| 6 | 2.2% / 0.43 / 166 | 6.8% / 1.59 / 164 | 15.3% / 1.59 / 157 | 15.3% / 3.27 / 169 | 1.9% / 0.29 / 165 |
| 7 | -0.3% / -0.06 / 176 | 5.0% / 1.83 / 176 | 13.4% / 1.88 / 171 | 11.1% / 3.58 / 189 | 1.6% / 0.30 / 172 |
| 8 | -0.3% / -0.06 / 176 | 4.7% / 1.68 / 176 | 13.5% / 1.88 / 171 | 11.1% / 3.57 / 189 | 1.5% / 0.29 / 172 |
| 9 | 15.7% / 1.78 / 271 | -2.2% / -0.46 / 249 | 16.2% / 1.46 / 258 | 0.0% / 0.03 / 262 | 20.9% / 1.82 / 285 |
| 10 | 15.1% / 1.72 / 271 | -2.1% / -0.43 / 249 | 16.3% / 1.47 / 258 | -0.1% / 0.01 / 262 | 21.6% / 1.88 / 286 |
| 11 | 1.2% / 0.39 / 84 | -0.4% / -0.13 / 105 | 5.4% / 0.94 / 97 | 6.6% / 2.35 / 113 | 7.6% / 1.42 / 76 |
| 12 | 15.6% / 1.77 / 269 | -4.0% / -0.89 / 297 | 28.6% / 2.08 / 280 | -2.8% / -0.54 / 273 | 14.5% / 1.44 / 287 |
| 13 | 15.6% / 1.77 / 269 | -4.1% / -0.92 / 298 | 27.7% / 2.02 / 282 | -3.2% / -0.62 / 275 | 14.6% / 1.44 / 288 |
| 14 | 1.4% / 0.44 / 85 | -0.4% / -0.15 / 105 | 5.7% / 0.98 / 97 | 6.4% / 2.32 / 111 | 7.5% / 1.34 / 77 |
| 15 | 6.1% / 0.78 / 278 | 0.4% / 0.10 / 241 | 18.3% / 1.40 / 256 | -4.2% / -0.81 / 266 | 24.9% / 2.28 / 290 |
| 16 | 14.1% / 1.99 / 131 | 8.3% / 1.86 / 137 | -2.1% / -0.18 / 131 | 0.9% / 0.28 / 130 | 12.7% / 1.59 / 124 |
| 17 | 6.4% / 0.82 / 278 | 0.5% / 0.12 / 241 | 18.5% / 1.42 / 256 | -3.8% / -0.71 / 265 | 24.6% / 2.23 / 289 |
| 18 | 5.3% / 1.13 / 131 | 7.7% / 1.96 / 137 | 6.2% / 0.60 / 132 | 3.3% / 0.90 / 131 | 9.0% / 1.26 / 124 |
| 19 | 13.6% / 1.91 / 133 | 8.0% / 1.78 / 138 | -2.0% / -0.16 / 131 | 1.2% / 0.35 / 131 | 12.6% / 1.57 / 124 |
| 20 | 4.8% / 1.03 / 133 | 7.4% / 1.88 / 138 | 6.2% / 0.60 / 132 | 3.4% / 0.94 / 132 | 9.2% / 1.28 / 124 |
| 21 | 11.9% / 1.67 / 120 | -4.0% / -1.23 / 119 | 22.8% / 2.05 / 110 | -2.6% / -0.65 / 114 | 8.5% / 1.10 / 144 |
| 22 | 11.9% / 1.67 / 120 | -3.9% / -1.19 / 118 | 23.0% / 2.07 / 109 | -2.6% / -0.65 / 114 | 8.7% / 1.13 / 144 |
| 23 | 0.8% / 0.19 / 137 | 1.0% / 0.31 / 143 | 13.2% / 1.41 / 142 | 4.7% / 1.35 / 156 | 7.4% / 1.04 / 145 |
| 24 | 0.8% / 0.19 / 137 | 1.0% / 0.31 / 143 | 13.2% / 1.41 / 142 | 4.7% / 1.35 / 156 | 7.4% / 1.04 / 145 |
| 25 | 10.1% / 1.73 / 37 | 3.5% / 1.37 / 33 | -3.7% / -0.53 / 36 | 2.7% / 1.24 / 30 | 11.9% / 2.16 / 48 |
| 26 | 8.6% / 1.61 / 37 | 3.4% / 1.35 / 33 | -2.9% / -0.41 / 36 | 2.7% / 1.25 / 30 | 10.7% / 2.10 / 48 |
| 27 | 9.3% / 0.95 / 272 | -0.0% / 0.03 / 219 | 2.7% / 0.28 / 238 | 10.1% / 1.66 / 244 | 20.1% / 1.73 / 270 |
| 28 | 17.0% / 2.39 / 131 | 3.7% / 1.07 / 135 | -4.6% / -0.54 / 139 | -1.0% / -0.39 / 123 | 10.5% / 1.45 / 131 |
| 29 | 9.3% / 0.95 / 272 | -0.0% / 0.03 / 219 | 3.0% / 0.30 / 237 | 9.9% / 1.64 / 244 | 20.2% / 1.74 / 270 |
| 30 | 1.1% / 0.35 / 71 | 7.0% / 2.39 / 73 | 11.5% / 1.41 / 81 | 3.7% / 1.51 / 68 | -1.0% / -0.21 / 65 |
| 31 | 13.2% / 1.23 / 362 | -3.2% / -0.53 / 382 | 37.3% / 1.99 / 359 | 3.0% / 0.47 / 364 | 4.0% / 0.37 / 382 |
| 32 | 0.9% / 0.30 / 72 | 6.7% / 2.29 / 74 | 11.5% / 1.40 / 81 | 4.0% / 1.60 / 69 | -0.8% / -0.17 / 65 |
| 33 | 9.8% / 0.96 / 362 | -3.0% / -0.48 / 384 | 39.5% / 2.11 / 356 | 4.0% / 0.63 / 365 | 4.0% / 0.37 / 386 |
| 34 | 8.3% / 1.73 / 131 | 4.8% / 1.38 / 135 | -0.3% / 0.01 / 139 | 0.9% / 0.35 / 125 | 7.7% / 1.22 / 131 |
| 35 | 9.1% / 1.57 / 60 | 1.0% / 0.36 / 59 | -1.3% / -0.14 / 61 | 0.4% / 0.16 / 58 | 14.4% / 2.28 / 61 |
| 36 | 1.0% / 0.23 / 128 | 1.0% / 0.28 / 151 | 9.5% / 1.25 / 136 | 6.2% / 1.78 / 153 | 4.4% / 0.64 / 132 |
| 37 | 10.2% / 1.65 / 60 | 0.9% / 0.32 / 59 | -4.4% / -0.63 / 60 | -0.5% / -0.21 / 57 | 17.0% / 2.49 / 61 |
| 38 | 1.0% / 0.23 / 128 | 0.9% / 0.26 / 153 | 9.5% / 1.25 / 136 | 6.2% / 1.78 / 153 | 4.5% / 0.64 / 132 |
| 39 | 3.7% / 0.70 / 177 | -2.4% / -0.58 / 177 | 12.9% / 1.16 / 166 | 5.4% / 1.28 / 183 | 11.0% / 1.52 / 179 |
| 40 | 1.9% / 0.58 / 74 | 7.8% / 2.53 / 76 | 5.0% / 0.67 / 78 | 1.5% / 0.56 / 85 | 3.2% / 0.59 / 79 |
| 41 | 1.4% / 0.44 / 76 | 7.9% / 2.54 / 76 | 5.0% / 0.67 / 78 | 1.8% / 0.67 / 86 | 3.2% / 0.59 / 79 |
| 42 | 3.9% / 0.74 / 176 | -2.6% / -0.61 / 177 | 12.9% / 1.17 / 166 | 5.3% / 1.26 / 183 | 11.0% / 1.52 / 179 |
| 43 | 6.5% / 1.21 / 99 | 7.0% / 2.09 / 89 | -0.3% / 0.01 / 101 | 2.3% / 0.81 / 94 | 9.6% / 1.38 / 99 |
| 44 | 6.6% / 1.23 / 99 | 7.2% / 2.17 / 90 | 1.9% / 0.25 / 101 | 2.5% / 0.85 / 95 | 9.6% / 1.40 / 99 |
| 45 | 9.2% / 1.41 / 99 | 6.9% / 2.09 / 89 | -3.6% / -0.43 / 101 | 2.6% / 0.87 / 94 | 10.1% / 1.41 / 99 |
| 46 | 7.5% / 1.25 / 99 | 6.8% / 2.09 / 89 | -2.7% / -0.31 / 101 | 2.6% / 0.89 / 94 | 9.6% / 1.39 / 99 |
| 47 | 10.1% / 1.45 / 126 | 6.9% / 1.73 / 132 | 0.1% / 0.06 / 134 | 0.3% / 0.11 / 121 | 10.0% / 1.27 / 126 |
| 48 | 2.2% / 0.67 / 37 | 2.1% / 1.08 / 34 | 3.8% / 0.55 / 36 | 2.4% / 1.56 / 30 | 6.9% / 1.64 / 49 |
| 49 | -0.3% / -0.20 / 21 | 0.4% / 0.33 / 32 | 6.1% / 1.43 / 23 | 0.5% / 0.33 / 28 | 3.7% / 1.12 / 35 |
| 50 | -1.3% / -0.45 / 99 | 1.2% / 0.47 / 114 | 5.6% / 0.98 / 107 | 8.1% / 2.67 / 119 | 1.7% / 0.48 / 84 |
| 51 | 11.5% / 1.55 / 126 | 6.9% / 1.70 / 132 | -1.5% / -0.09 / 134 | -0.2% / -0.04 / 121 | 11.8% / 1.42 / 126 |
| 52 | 13.1% / 1.65 / 315 | -7.6% / -2.00 / 361 | 18.7% / 1.75 / 338 | -2.4% / -0.50 / 339 | 11.5% / 1.35 / 346 |
| 53 | 12.9% / 2.08 / 101 | 3.0% / 1.08 / 90 | -6.3% / -1.02 / 105 | 2.1% / 0.96 / 94 | 7.4% / 1.27 / 103 |
| 54 | -0.2% / -0.13 / 20 | 1.3% / 1.12 / 33 | 4.6% / 1.21 / 22 | 1.2% / 0.80 / 28 | 3.9% / 1.09 / 34 |
| 55 | 13.1% / 1.65 / 315 | -7.8% / -2.04 / 363 | 16.9% / 1.62 / 340 | -2.3% / -0.49 / 339 | 11.2% / 1.34 / 347 |
| 56 | 0.9% / 0.63 / 34 | -0.7% / -0.67 / 73 | 4.1% / 1.34 / 42 | 0.4% / 0.36 / 43 | 3.4% / 1.40 / 45 |
| 57 | 0.5% / 0.37 / 33 | -0.3% / -0.19 / 71 | 5.2% / 1.34 / 41 | 0.2% / 0.18 / 41 | 3.1% / 1.24 / 42 |
| 58 | -1.3% / -0.45 / 99 | 1.3% / 0.51 / 113 | 5.6% / 0.98 / 107 | 8.1% / 2.67 / 119 | 1.7% / 0.46 / 84 |
| 59 | 7.5% / 2.38 / 50 | -0.8% / -0.44 / 48 | 3.9% / 0.76 / 44 | -0.5% / -0.28 / 42 | 4.2% / 0.89 / 70 |
| 60 | 7.5% / 2.38 / 50 | -0.8% / -0.44 / 48 | 3.9% / 0.76 / 44 | -0.5% / -0.28 / 42 | 4.2% / 0.89 / 70 |
| 61 | -0.1% / -0.01 / 99 | 4.5% / 1.72 / 91 | 12.6% / 1.28 / 102 | 2.4% / 0.92 / 95 | 3.4% / 0.60 / 100 |
| 62 | 3.9% / 1.11 / 60 | 1.3% / 0.86 / 52 | 6.8% / 1.08 / 63 | 4.1% / 1.84 / 52 | 0.8% / 0.22 / 48 |
| 63 | 3.9% / 1.11 / 60 | 1.4% / 0.96 / 51 | 6.7% / 1.07 / 61 | 3.4% / 1.71 / 51 | 0.9% / 0.26 / 48 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_8e84` | 15 | 0.83 | 0.89/0.95 | 0.73/0.89 |
| 1 | `cfg_ec8f` | 4 | 0.92 | 0.93/0.98 | 0.93/0.94 |
| 2 | `cfg_a4d4` | 14 | 0.86 | 0.32/0.96 | 0.26/0.92 |
| 3 | `cfg_8a64` | 12 | 0.93 | 0.85/0.97 | 0.81/0.91 |
| 4 | `cfg_ce0e` | 16 | 0.85 | 0.81/0.90 | 0.80/0.88 |
| 5 | `cfg_0d6a` | 12 | 0.82 | 0.90/0.94 | 0.83/0.91 |
| 6 | `cfg_f6c8` | 10 | 0.82 | 0.71/0.90 | 0.71/0.95 |
| 7 | `cfg_08df` | 2 | 0.99 | 0.99/0.99 | 0.98/0.98 |
| 8 | `cfg_458e` | 11 | 0.91 | 0.88/0.96 | 0.77/0.93 |
| 9 | `cfg_4c71` | 16 | 0.85 | 0.75/0.79 | 0.82/0.86 |
| 10 | `cfg_0ced` | 6 | 0.81 | 0.84/0.98 | 0.34/0.94 |
| 11 | `cfg_742a` | 10 | 0.87 | 0.89/0.90 | 0.73/0.74 |
| 12 | `cfg_12bd` | 4 | 0.96 | 0.97/0.97 | 0.92/0.92 |
| 13 | `cfg_1532` | 6 | 0.87 | 0.53/0.97 | 0.61/0.93 |
| 14 | `cfg_f1f2` | 5 | 0.81 | 0.72/0.90 | 0.30/0.75 |
| 15 | `cfg_c8cf` | 4 | 0.97 | 0.99/0.99 | 0.98/0.98 |
| 16 | `cfg_213d` | 4 | 0.83 | 0.91/0.97 | 0.85/0.97 |
| 17 | `cfg_4e49` | 10 | 0.83 | 0.65/0.80 | 0.49/0.69 |
| 18 | `cfg_289a` | 28 | 0.84 | 0.74/0.78 | 0.62/0.65 |
| 19 | `cfg_8230` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 20 | `cfg_c898` | 8 | 0.96 | 0.92/0.92 | 0.88/0.88 |
| 21 | `cfg_c387` | 8 | 0.84 | 0.79/0.79 | 0.36/0.37 |
| 22 | `cfg_40fa` | 7 | 0.85 | 0.88/0.97 | 0.85/0.96 |
| 23 | `cfg_e9ae` | 4 | 0.95 | 0.92/0.92 | 0.82/0.82 |
| 24 | `cfg_dcbd` | 6 | 0.97 | 0.97/0.98 | 0.93/0.96 |
| 25 | `cfg_de6e` | 4 | 0.99 | 0.99/0.99 | 0.97/0.97 |
| 26 | `cfg_91b0` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 27 | `cfg_9d4f` | 2 | 1.00 | 1.00/1.00 | 0.98/0.98 |
| 28 | `cfg_a588` | 3 | 0.96 | 0.98/0.98 | 0.96/0.97 |
| 29 | `cfg_b0ad` | 2 | 1.00 | 1.00/1.00 | 0.99/0.99 |
| 30 | `cfg_d5a4` | 1 | n/a | n/a/n/a | n/a/n/a |
| 31 | `cfg_f249` | 1 | n/a | n/a/n/a | n/a/n/a |
| 32 | `cfg_f58b` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.264e-03 over 20736 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1166.0, participation ratio 37.4, 95%-variance components 322 (rank bound T = 1259); raw grid 20736; raw + known prior 561684
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
NQ results are unchanged rules on the development period: supporting evidence, not an independent replication.

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
