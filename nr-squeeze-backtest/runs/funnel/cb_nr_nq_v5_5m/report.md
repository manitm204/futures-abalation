# Screening funnel -- cb_nr_nq_v5_5m (development stages only)

- Code: `46ee6e771bde` (dirty working tree: True, diff sha256 `b83fa813a0b4`)
- Config: `configs/funnel/cb_nr_funnel_nq_v5_5m.yaml` sha256 `4680a1679f87e328`; seed 2026112525
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'NQ': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `4a4ed57aec887fe9` (18 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- NQ 2023-2024 was read for other families and for NR v2-v4; this grid is largely in-sample for this line.
- Holdout 2025+ previously inspected: **False** -- No NR-N metrics have been computed on NQ 2025+ for this grid; other families were scored there.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 120 | 120 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 120 | 120 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 120 | 120 | 0 | 0 |  | 120 | 100.00 | 100.00 |  |
| 3 performance & risk | hard_gate | 120 | 20 | 100 | 0 |  | 0 | 16.67 | 16.67 |  |
| 4 parameter stability | hard_gate | 20 | 20 | 0 | 0 |  | 0 | 16.67 | 100.00 |  |
| 5 time stability | hard_gate | 20 | 20 | 0 | 0 |  | 20 | 16.67 | 100.00 |  |
| 6 deduplication | dedup | 20 | 18 |  |  | 2 |  | 15.00 | 90.00 | best 2 per cluster |
| 7 execution stress | hard_gate | 18 | 18 | 0 | 0 |  | 0 | 15.00 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 18 |  |  |  |  |  |  |  | diagnostic only: unverified: 18 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s3:hard_reject:max_drawdown | 28 |
| s3:hard_reject:net_return | 65 |
| s3:hard_reject:sharpe | 100 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | target/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_94e6` | timeframe=5min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=none, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/568/1179 | 1747 | 64.2% | 10.4% | 1.31 | -8.1% | 278 | 1.22 | 41.7% | 879.2 | 3/3 | 1.00 | 1.00 | 0.30 | 5 | 37.0% | 0.42 | 0.30 | 53.1% | 41.4% | 65.5% | 55.8%/49.4% | 4.8 (interpolated) | pass | 0.028 (unverified) | -0.27 |
| 2 | `cfg_6c1f` | timeframe=5min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=none, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/630/1191 | 1821 | 63.1% | 10.3% | 1.17 | -6.0% | 270 | 1.19 | 47.4% | 908.2 | 2/2 | 1.00 | 1.12 | 0.04 | 5 | 34.4% | 0.45 | 0.29 | 51.5% | 41.7% | 74.1% | 60.4%/49.4% | 4.7 (interpolated) | pass | 0.014 (unverified) | 0.15 |
| 3 | `cfg_5dac` | timeframe=5min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/542/1292 | 1834 | 55.6% | 9.3% | 1.17 | -6.5% | 301 | 1.20 | 40.6% | 915.3 | 3/3 | 1.00 | 1.08 | 0.08 | 5 | 29.2% | 0.47 | 0.34 | 47.5% | 35.3% | 46.8% | 51.2%/45.7% | 4.5 (interpolated) | pass | 0.013 (unverified) | -0.04 |
| 4 | `cfg_f86b` | timeframe=5min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=none, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/1000/2163 | 3163 | 95.2% | 14.3% | 1.04 | -18.5% | 739 | 1.13 | 77.6% | 1605.8 | 2/2 | 1.00 | 0.88 | 0.16 | 4 | 25.1% | 0.74 | 0.32 | 65.0% | 49.8% | 108.5% | 91.2%/73.5% | 3.7 (interpolated) | pass | 0.008 (unverified) | 0.12 |
| 5 | `cfg_6001` | timeframe=5min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/957/2655 | 3612 | 110.6% | 16.1% | 1.18 | -19.6% | 731 | 1.16 | 74.7% | 1819.7 | 2/2 | 1.00 | 0.71 | 0.46 | 4 | 24.5% | 0.78 | 0.26 | 78.6% | 60.7% | 109.9% | 107.1%/86.9% | 3.7 (interpolated) | pass | 0.017 (unverified) | 0.02 |
| 6 | `cfg_55d6` | timeframe=5min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=2.5, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 617/268/1557 | 2442 | 39.6% | 6.9% | 1.00 | -8.5% | 346 | 1.12 | 34.1% | 1223.1 | 4/4 | 0.75 | 0.81 | 0.19 | 5 | 22.6% | 0.37 | 0.27 | 28.4% | 16.0% | 47.2% | 35.8%/29.7% | 2.9 (interpolated) | pass | 0.005 (unverified) | -1.06 |
| 7 | `cfg_6d83` | timeframe=5min, compression=nr, nr_lookback=10, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/451/1073 | 1524 | 45.1% | 7.7% | 1.08 | -6.6% | 366 | 1.21 | 32.8% | 768.8 | 3/3 | 1.00 | 0.85 | 0.24 | 4 | 22.9% | 0.49 | 0.39 | 34.2% | 27.0% | 25.7% | 41.7%/32.3% | 4.2 (interpolated) | pass | 0.006 (unverified) | -0.01 |
| 8 | `cfg_5e45` | timeframe=5min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/595/1462 | 2057 | 62.8% | 10.3% | 1.20 | -6.2% | 223 | 1.20 | 45.2% | 1019.8 | 2/2 | 1.00 | 1.02 | 0.18 | 4 | 29.8% | 0.53 | 0.28 | 50.0% | 40.0% | 72.5% | 57.3%/51.6% | 4.1 (interpolated) | pass | 0.016 (unverified) | 0.18 |
| 9 | `cfg_095b` | timeframe=5min, compression=nr, nr_lookback=10, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=none, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/443/1127 | 1570 | 34.4% | 6.1% | 0.91 | -7.4% | 392 | 1.17 | 32.0% | 787.0 | 3/3 | 1.00 | 0.76 | 0.16 | 4 | 19.0% | 0.45 | 0.45 | 27.7% | 22.4% | 39.9% | 32.1%/26.4% | 3.6 (interpolated) | pass | 0.002 (unverified) | -0.51 |
| 10 | `cfg_cb90` | timeframe=5min, compression=nr, nr_lookback=10, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/721/1922 | 2643 | 71.3% | 11.4% | 1.00 | -11.9% | 366 | 1.15 | 52.9% | 1331.8 | 3/3 | 1.00 | 0.84 | 0.16 | 3 | 23.2% | 0.68 | 0.36 | 51.6% | 41.7% | 61.8% | 69.0%/50.4% | 3.8 (interpolated) | pass | 0.004 (unverified) | -0.20 |
| 11 | `cfg_5b02` | timeframe=5min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=2.5, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 607/372/1575 | 2554 | 44.5% | 7.6% | 0.94 | -7.1% | 286 | 1.12 | 42.2% | 1278.2 | 3/3 | 1.00 | 1.00 | -0.06 | 4 | 24.5% | 0.45 | 0.24 | 32.1% | 20.3% | 64.4% | 37.9%/32.0% | 3.0 (interpolated) | pass | 0.004 (unverified) | -0.25 |
| 12 | `cfg_2af2` | timeframe=5min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=2.5, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 856/205/2038 | 3099 | 35.7% | 6.3% | 0.87 | -9.4% | 515 | 1.10 | 37.8% | 1539.3 | 3/3 | 0.67 | 0.80 | 0.06 | 4 | 15.2% | 0.58 | 0.26 | 19.6% | 7.8% | 52.5% | 33.8%/24.1% | 2.3 (interpolated) | pass | 0.002 (unverified) | -0.64 |
| 13 | `cfg_4a21` | timeframe=5min, compression=nr, nr_lookback=10, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=none, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/710/1979 | 2689 | 57.3% | 9.5% | 0.87 | -13.8% | 384 | 1.13 | 52.0% | 1359.8 | 3/3 | 1.00 | 0.71 | 0.15 | 3 | 13.1% | 0.77 | 0.40 | 49.5% | 34.7% | 75.8% | 56.4%/44.7% | 3.3 (interpolated) | pass | 0.002 (unverified) | -0.43 |
| 14 | `cfg_bc52` | timeframe=5min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/976/2810 | 3786 | 81.1% | 12.6% | 0.90 | -19.6% | 500 | 1.11 | 79.5% | 1901.1 | 3/3 | 0.67 | 0.63 | 0.27 | 4 | 23.7% | 0.71 | 0.35 | 59.5% | 39.9% | 46.6% | 75.0%/48.4% | 3.0 (interpolated) | pass | 0.003 (unverified) | -0.00 |
| 15 | `cfg_1939` | timeframe=5min, compression=nr, nr_lookback=16, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/596/1594 | 2190 | 49.7% | 8.4% | 0.84 | -12.0% | 330 | 1.13 | 43.4% | 1107.8 | 3/3 | 1.00 | 0.62 | 0.22 | 4 | 20.6% | 0.59 | 0.48 | 44.0% | 30.2% | 57.0% | 49.5%/37.6% | 3.6 (interpolated) | pass | 0.001 (unverified) | -0.38 |
| 16 | `cfg_1015` | timeframe=5min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=2.5, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 705/173/1701 | 2579 | 29.3% | 5.3% | 0.80 | -7.5% | 450 | 1.10 | 32.4% | 1288.3 | 4/4 | 0.75 | 0.74 | 0.06 | 5 | 16.1% | 0.45 | 0.36 | 16.4% | 7.0% | 27.2% | 27.3%/18.4% | 2.4 (interpolated) | pass | 0.001 (unverified) | -1.00 |
| 17 | `cfg_93dc` | timeframe=5min, compression=nr, nr_lookback=16, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/371/901 | 1272 | 29.0% | 5.2% | 0.85 | -6.5% | 288 | 1.18 | 27.0% | 634.8 | 3/3 | 1.00 | 0.40 | 0.44 | 4 | 13.6% | 0.53 | 0.54 | 22.1% | 18.6% | 30.8% | 26.2%/20.2% | 3.7 (interpolated) | pass | 0.001 (unverified) | -0.15 |
| 18 | `cfg_6465` | timeframe=5min, compression=nr, nr_lookback=16, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=none, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/353/983 | 1336 | 23.8% | 4.4% | 0.76 | -6.3% | 366 | 1.16 | 25.2% | 671.4 | 3/3 | 1.00 | 0.42 | 0.34 | 4 | 11.8% | 0.46 | 0.60 | 19.9% | 13.6% | 17.9% | 23.0%/18.7% | 3.3 (interpolated) | pass | 0.001 (unverified) | -0.75 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 5.6% / 0.79 / 346 | 5.9% / 1.11 / 382 | 14.3% / 1.38 / 399 | 7.1% / 1.21 / 358 | 19.9% / 1.95 / 262 |
| 2 | 1.9% / 0.29 / 371 | 1.9% / 0.35 / 395 | 13.3% / 1.13 / 418 | 14.2% / 2.16 / 347 | 21.4% / 1.89 / 290 |
| 3 | 4.1% / 0.57 / 362 | 3.8% / 0.75 / 396 | 13.1% / 1.25 / 414 | 5.8% / 1.03 / 377 | 20.4% / 2.01 / 285 |
| 4 | 22.5% / 1.52 / 644 | -9.2% / -1.07 / 654 | 3.5% / 0.29 / 657 | 8.6% / 0.94 / 595 | 56.0% / 2.75 / 613 |
| 5 | 18.6% / 1.29 / 739 | -7.4% / -0.86 / 739 | 2.5% / 0.23 / 746 | 10.6% / 1.16 / 687 | 69.1% / 3.30 / 701 |
| 6 | 1.8% / 0.33 / 483 | 4.4% / 0.95 / 538 | 13.9% / 1.44 / 567 | 4.6% / 0.90 / 484 | 10.3% / 1.22 / 370 |
| 7 | 5.9% / 0.94 / 288 | -0.1% / -0.01 / 357 | 15.1% / 1.53 / 326 | 0.9% / 0.23 / 313 | 18.1% / 1.91 / 240 |
| 8 | -0.6% / -0.03 / 415 | 1.6% / 0.33 / 454 | 13.0% / 1.15 / 471 | 13.7% / 2.19 / 394 | 25.4% / 2.25 / 323 |
| 9 | 6.0% / 1.03 / 298 | -1.7% / -0.35 / 378 | 12.8% / 1.38 / 334 | 1.3% / 0.31 / 313 | 12.9% / 1.51 / 247 |
| 10 | 13.7% / 1.15 / 539 | -6.7% / -1.09 / 545 | 20.0% / 1.27 / 502 | -3.2% / -0.41 / 530 | 39.1% / 2.46 / 527 |
| 11 | -2.8% / -0.39 / 517 | 0.5% / 0.11 / 536 | 16.2% / 1.39 / 603 | 9.7% / 1.72 / 476 | 16.0% / 1.54 / 422 |
| 12 | -6.8% / -1.15 / 622 | 0.5% / 0.13 / 675 | 11.7% / 1.13 / 725 | 10.1% / 1.81 / 592 | 17.9% / 1.91 / 485 |
| 13 | 12.7% / 1.10 / 549 | -8.5% / -1.41 / 567 | 11.6% / 0.82 / 517 | -1.6% / -0.17 / 532 | 39.1% / 2.54 / 524 |
| 14 | 9.8% / 0.72 / 790 | 7.6% / 0.90 / 708 | -8.6% / -0.40 / 801 | 14.4% / 1.61 / 725 | 46.4% / 2.14 / 762 |
| 15 | 16.1% / 1.46 / 427 | -8.8% / -1.71 / 467 | 13.4% / 0.99 / 423 | 0.4% / 0.09 / 431 | 24.1% / 1.84 / 442 |
| 16 | 0.6% / 0.13 / 506 | 0.1% / 0.06 / 568 | 10.1% / 1.08 / 595 | 4.8% / 0.89 / 512 | 11.3% / 1.48 / 398 |
| 17 | 6.7% / 1.13 / 239 | -3.2% / -0.81 / 308 | 7.1% / 0.86 / 275 | 2.7% / 0.69 / 255 | 13.5% / 1.70 / 195 |
| 18 | 7.0% / 1.29 / 250 | -4.8% / -1.31 / 331 | 10.7% / 1.38 / 286 | 3.1% / 0.82 / 263 | 6.5% / 0.87 / 206 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_6d83` | 2 | 0.92 | 0.93/0.93 | 0.89/0.89 |
| 1 | `cfg_55d6` | 2 | 0.81 | 0.79/0.79 | 0.74/0.74 |
| 2 | `cfg_1939` | 1 | n/a | n/a/n/a | n/a/n/a |
| 3 | `cfg_5b02` | 2 | 0.86 | 0.84/0.84 | 0.76/0.76 |
| 4 | `cfg_cb90` | 2 | 0.92 | 0.93/0.93 | 0.88/0.88 |
| 5 | `cfg_94e6` | 2 | 0.94 | 0.94/0.94 | 0.92/0.92 |
| 6 | `cfg_6c1f` | 2 | 0.95 | 0.95/0.95 | 0.92/0.92 |
| 7 | `cfg_f86b` | 4 | 0.82 | 0.84/0.88 | 0.80/0.84 |
| 8 | `cfg_93dc` | 2 | 0.90 | 0.92/0.92 | 0.87/0.87 |
| 9 | `cfg_bc52` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 3.653e-03 over 120 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 42.0, participation ratio 6.9, 95%-variance components 39 (rank bound T = 1259); raw grid 120; raw + known prior 606456
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
