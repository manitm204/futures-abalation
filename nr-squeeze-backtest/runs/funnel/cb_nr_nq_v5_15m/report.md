# Screening funnel -- cb_nr_nq_v5_15m (development stages only)

- Code: `46ee6e771bde` (dirty working tree: True, diff sha256 `2f40f72eed73`)
- Config: `configs/funnel/cb_nr_funnel_nq_v5_15m.yaml` sha256 `616fb32ef6af6097`; seed 2026112520
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'NQ': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `4099fddd34955719` (38 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- NQ 2023-2024 was read for other families and for NR v2-v4; this grid is largely in-sample for this line.
- Holdout 2025+ previously inspected: **False** -- No NR-N metrics have been computed on NQ 2025+ for this grid; other families were scored there.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 400 | 400 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 400 | 400 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 400 | 400 | 0 | 0 |  | 400 | 100.00 | 100.00 |  |
| 3 performance & risk | hard_gate | 400 | 60 | 340 | 0 |  | 0 | 15.00 | 15.00 |  |
| 4 parameter stability | hard_gate | 60 | 60 | 0 | 0 |  | 0 | 15.00 | 100.00 |  |
| 5 time stability | hard_gate | 60 | 60 | 0 | 0 |  | 60 | 15.00 | 100.00 |  |
| 6 deduplication | dedup | 60 | 38 |  |  | 22 |  | 9.50 | 63.33 | best 2 per cluster |
| 7 execution stress | hard_gate | 38 | 38 | 0 | 0 |  | 0 | 9.50 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 38 |  |  |  |  |  |  |  | diagnostic only: unverified: 38 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s3:hard_reject:max_drawdown | 1 |
| s3:hard_reject:net_return | 89 |
| s3:hard_reject:sharpe | 340 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | target/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_4fce` | timeframe=15min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/943/1016 | 1959 | 99.7% | 14.8% | 1.17 | -16.5% | 186 | 1.17 | 62.6% | 1003.9 | 3/3 | 1.00 | 0.92 | 0.26 | 5 | 65.6% | 0.34 | 0.31 | 88.6% | 72.7% | 71.1% | 85.2%/66.1% | 5.8 (interpolated) | pass | 0.706 (unverified) | -0.03 |
| 2 | `cfg_0f95` | timeframe=15min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/938/1118 | 2056 | 90.1% | 13.7% | 1.10 | -16.9% | 201 | 1.16 | 61.9% | 1045.3 | 3/3 | 1.00 | 0.95 | 0.15 | 4 | 55.5% | 0.38 | 0.28 | 78.8% | 62.5% | 40.7% | 79.6%/57.1% | 5.3 (interpolated) | pass | 0.648 (unverified) | 0.09 |
| 3 | `cfg_042c` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/1056/1461 | 2517 | 99.5% | 14.8% | 1.05 | -23.1% | 437 | 1.14 | 76.3% | 1284.8 | 2/2 | 1.00 | 0.97 | 0.08 | 3 | 47.5% | 0.52 | 0.32 | 85.3% | 67.2% | 58.5% | 89.6%/64.2% | 4.9 (interpolated) | pass | 0.602 (unverified) | 0.56 |
| 4 | `cfg_6a30` | timeframe=15min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=2.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 379/445/878 | 1702 | 56.6% | 9.4% | 1.03 | -13.0% | 229 | 1.16 | 40.0% | 860.0 | 4/4 | 1.00 | 0.69 | 0.34 | 3 | 16.8% | 0.70 | 0.25 | 46.8% | 38.6% | 52.5% | 48.8%/41.6% | 4.6 (interpolated) | pass | 0.592 (unverified) | 0.61 |
| 5 | `cfg_e5a4` | timeframe=15min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=4.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 122/849/1161 | 2132 | 80.3% | 12.5% | 1.04 | -16.9% | 201 | 1.14 | 60.6% | 1082.8 | 4/4 | 1.00 | 0.90 | 0.14 | 5 | 53.0% | 0.34 | 0.27 | 69.9% | 58.3% | 30.0% | 70.5%/45.6% | 5.0 (interpolated) | pass | 0.594 (unverified) | -0.11 |
| 6 | `cfg_4027` | timeframe=15min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=4.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 109/870/1034 | 2013 | 74.4% | 11.8% | 1.01 | -16.1% | 199 | 1.14 | 61.5% | 1022.7 | 4/4 | 1.00 | 0.86 | 0.14 | 5 | 42.3% | 0.36 | 0.27 | 62.0% | 47.4% | 66.9% | 62.1%/41.6% | 4.9 (interpolated) | pass | 0.565 (unverified) | -0.06 |
| 7 | `cfg_97f7` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 1089/352/995 | 2436 | 57.8% | 9.6% | 1.03 | -8.0% | 314 | 1.12 | 43.5% | 1240.3 | 3/3 | 1.00 | 0.84 | 0.19 | 4 | 25.0% | 0.57 | 0.18 | 43.5% | 32.2% | 48.4% | 52.8%/38.5% | 3.5 (interpolated) | pass | 0.587 (unverified) | -0.34 |
| 8 | `cfg_74e4` | timeframe=15min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=2.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 373/463/845 | 1681 | 56.6% | 9.4% | 1.06 | -10.7% | 388 | 1.16 | 40.5% | 850.7 | 4/4 | 1.00 | 0.89 | 0.16 | 3 | 22.4% | 0.60 | 0.28 | 48.8% | 41.2% | 53.1% | 50.3%/40.3% | 5.0 (interpolated) | pass | 0.611 (unverified) | 0.25 |
| 9 | `cfg_01bf` | timeframe=15min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=3.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 171/593/831 | 1595 | 56.2% | 9.3% | 0.97 | -9.8% | 262 | 1.15 | 43.8% | 807.3 | 4/4 | 1.00 | 0.92 | 0.04 | 3 | 27.8% | 0.51 | 0.37 | 49.1% | 40.1% | 46.0% | 51.5%/42.9% | 5.0 (interpolated) | pass | 0.533 (unverified) | 0.68 |
| 10 | `cfg_178b` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=4.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 165/975/1553 | 2693 | 90.0% | 13.7% | 0.99 | -22.7% | 395 | 1.12 | 75.2% | 1373.3 | 3/3 | 1.00 | 0.96 | 0.03 | 4 | 43.6% | 0.52 | 0.27 | 68.4% | 50.4% | 46.8% | 76.8%/61.6% | 4.3 (interpolated) | pass | 0.553 (unverified) | 0.47 |
| 11 | `cfg_fd56` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=2.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 375/637/940 | 1952 | 60.6% | 9.9% | 0.94 | -13.3% | 588 | 1.14 | 52.5% | 983.9 | 4/4 | 1.00 | 0.98 | -0.04 | 4 | 9.7% | 0.84 | 0.28 | 38.9% | 33.4% | 67.4% | 49.7%/36.3% | 4.1 (interpolated) | pass | 0.507 (unverified) | 0.02 |
| 12 | `cfg_a96f` | timeframe=15min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=4.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 58/683/836 | 1577 | 54.2% | 9.0% | 0.91 | -12.6% | 342 | 1.15 | 44.6% | 795.1 | 4/4 | 1.00 | 0.86 | 0.05 | 4 | 23.1% | 0.57 | 0.36 | 47.0% | 41.5% | 38.5% | 50.1%/42.5% | 5.0 (interpolated) | pass | 0.484 (unverified) | 0.68 |
| 13 | `cfg_6563` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/1018/1334 | 2352 | 74.7% | 11.8% | 0.95 | -11.8% | 290 | 1.13 | 71.3% | 1189.9 | 3/3 | 1.00 | 1.05 | -0.10 | 5 | 29.8% | 0.60 | 0.30 | 61.4% | 46.9% | 90.0% | 62.7%/44.9% | 3.9 (interpolated) | pass | 0.517 (unverified) | 0.21 |
| 14 | `cfg_3bff` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=3.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 155/759/899 | 1813 | 61.3% | 10.0% | 0.93 | -15.6% | 796 | 1.15 | 55.4% | 911.7 | 4/4 | 1.00 | 0.85 | 0.08 | 4 | 8.4% | 0.86 | 0.30 | 45.7% | 35.4% | 62.0% | 52.1%/34.7% | 4.4 (interpolated) | pass | 0.499 (unverified) | 0.35 |
| 15 | `cfg_4a82` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=4.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 137/938/1396 | 2471 | 75.9% | 12.0% | 0.96 | -12.3% | 269 | 1.12 | 70.0% | 1248.5 | 4/4 | 1.00 | 0.97 | -0.01 | 5 | 29.8% | 0.61 | 0.29 | 59.9% | 44.7% | 66.9% | 65.9%/43.6% | 3.9 (interpolated) | pass | 0.528 (unverified) | 0.16 |
| 16 | `cfg_ffe0` | timeframe=15min, compression=nr, nr_lookback=8, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/796/1048 | 1844 | 61.3% | 10.0% | 0.92 | -11.5% | 294 | 1.13 | 50.8% | 938.9 | 3/3 | 1.00 | 0.92 | -0.01 | 4 | 22.3% | 0.60 | 0.47 | 49.7% | 42.6% | 53.4% | 53.8%/38.6% | 4.7 (interpolated) | pass | 0.486 (unverified) | 0.15 |
| 17 | `cfg_deea` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=2.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 495/520/1136 | 2151 | 51.6% | 8.7% | 0.90 | -13.7% | 683 | 1.12 | 48.5% | 1082.6 | 4/4 | 1.00 | 0.80 | 0.10 | 3 | 5.2% | 0.90 | 0.27 | 35.1% | 24.9% | 64.5% | 45.3%/29.7% | 3.5 (interpolated) | pass | 0.472 (unverified) | 0.19 |
| 18 | `cfg_4ce2` | timeframe=15min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=2.0, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 190/326/486 | 1002 | 25.0% | 4.6% | 0.92 | -6.3% | 533 | 1.18 | 26.2% | 496.0 | 4/4 | 1.00 | 0.78 | 0.13 | 3 | 11.3% | 0.55 | 0.40 | 21.7% | 19.4% | 22.6% | 24.1%/19.9% | 4.4 (interpolated) | pass | 0.486 (unverified) | 0.66 |
| 19 | `cfg_bc78` | timeframe=15min, compression=nr, nr_lookback=8, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/815/987 | 1802 | 62.2% | 10.2% | 0.93 | -13.7% | 247 | 1.13 | 51.8% | 918.9 | 3/3 | 1.00 | 0.84 | 0.09 | 5 | 18.4% | 0.68 | 0.44 | 52.6% | 40.4% | 31.1% | 49.9%/33.3% | 4.7 (interpolated) | pass | 0.497 (unverified) | 0.24 |
| 20 | `cfg_9cc7` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=4.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 73/781/1034 | 1888 | 56.1% | 9.3% | 0.87 | -12.8% | 501 | 1.14 | 53.8% | 944.4 | 4/4 | 1.00 | 0.86 | 0.01 | 4 | 12.0% | 0.79 | 0.36 | 50.4% | 35.8% | 50.8% | 51.1%/36.4% | 4.3 (interpolated) | pass | 0.444 (unverified) | 0.53 |
| 21 | `cfg_f8ee` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/621/836 | 1457 | 45.8% | 7.8% | 0.92 | -12.5% | 152 | 1.17 | 31.5% | 739.5 | 2/2 | 1.00 | 0.89 | 0.03 | 5 | 29.4% | 0.30 | 0.45 | 37.7% | 32.0% | 33.3% | 40.1%/31.1% | 4.7 (interpolated) | pass | 0.493 (unverified) | 0.10 |
| 22 | `cfg_be71` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=3.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 197/927/1085 | 2209 | 73.9% | 11.7% | 0.90 | -19.6% | 475 | 1.13 | 71.6% | 1116.6 | 4/4 | 1.00 | 0.72 | 0.18 | 5 | 21.0% | 0.72 | 0.29 | 61.7% | 54.5% | 57.4% | 60.7%/42.2% | 4.6 (interpolated) | pass | 0.473 (unverified) | 0.29 |
| 23 | `cfg_5a92` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/896/1165 | 2061 | 55.3% | 9.2% | 0.80 | -13.4% | 773 | 1.11 | 60.5% | 1037.5 | 2/2 | 1.00 | 0.82 | -0.03 | 4 | 18.5% | 0.67 | 0.44 | 44.2% | 31.6% | 53.8% | 50.4%/42.0% | 3.8 (interpolated) | pass | 0.379 (unverified) | 0.41 |
| 24 | `cfg_0ea1` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=4.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 60/353/512 | 925 | 34.9% | 6.2% | 0.96 | -7.8% | 297 | 1.23 | 19.2% | 464.0 | 3/3 | 1.00 | 0.89 | 0.07 | 4 | 15.8% | 0.55 | 0.40 | 28.5% | 24.1% | 19.8% | 29.3%/23.1% | 5.4 (interpolated) | pass | 0.530 (unverified) | -0.04 |
| 25 | `cfg_456d` | timeframe=15min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 919/229/859 | 2007 | 34.4% | 6.1% | 0.84 | -10.3% | 476 | 1.10 | 31.6% | 1018.0 | 3/3 | 1.00 | 1.03 | -0.19 | 4 | 18.0% | 0.47 | 0.26 | 22.0% | 14.5% | 38.8% | 31.5%/22.1% | 2.9 (interpolated) | pass | 0.420 (unverified) | -0.05 |
| 26 | `cfg_3eb2` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=none, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/1035/1026 | 2061 | 70.5% | 11.3% | 0.88 | -19.4% | 300 | 1.13 | 73.1% | 1046.3 | 3/3 | 1.00 | 0.81 | 0.07 | 4 | 18.1% | 0.74 | 0.33 | 58.1% | 49.9% | 59.7% | 60.5%/39.8% | 4.5 (interpolated) | pass | 0.456 (unverified) | 0.25 |
| 27 | `cfg_d166` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=3.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 216/435/838 | 1489 | 43.3% | 7.5% | 0.94 | -12.9% | 170 | 1.15 | 28.9% | 759.0 | 3/3 | 1.00 | 0.77 | 0.17 | 5 | 27.1% | 0.34 | 0.40 | 36.5% | 28.3% | 28.4% | 36.6%/25.1% | 4.3 (interpolated) | pass | 0.510 (unverified) | -0.19 |
| 28 | `cfg_de14` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=3.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 137/285/508 | 930 | 36.3% | 6.4% | 1.01 | -8.3% | 296 | 1.23 | 18.3% | 466.5 | 3/3 | 1.00 | 0.76 | 0.25 | 4 | 17.4% | 0.52 | 0.40 | 30.9% | 26.8% | 21.1% | 31.8%/23.5% | 5.6 (interpolated) | pass | 0.572 (unverified) | -0.08 |
| 29 | `cfg_3e39` | timeframe=15min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=2.0, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 204/320/488 | 1012 | 23.3% | 4.3% | 0.86 | -5.6% | 322 | 1.17 | 25.9% | 505.8 | 4/4 | 1.00 | 0.66 | 0.20 | 3 | 5.4% | 0.77 | 0.41 | 19.9% | 15.7% | 20.5% | 21.5%/16.8% | 3.7 (interpolated) | pass | 0.435 (unverified) | 0.46 |
| 30 | `cfg_ed07` | timeframe=15min, compression=nr, nr_lookback=8, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=2.0, direction=long, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 309/307/685 | 1301 | 33.5% | 5.9% | 0.82 | -6.7% | 351 | 1.14 | 28.9% | 657.7 | 4/4 | 1.00 | 0.60 | 0.22 | 4 | 19.7% | 0.39 | 0.45 | 25.5% | 20.1% | 22.3% | 28.9%/20.3% | 3.9 (interpolated) | pass | 0.397 (unverified) | 0.26 |
| 31 | `cfg_f5e7` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=2.0, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 251/377/631 | 1259 | 23.7% | 4.4% | 0.78 | -7.9% | 568 | 1.13 | 31.9% | 629.1 | 4/4 | 1.00 | 0.71 | 0.07 | 4 | 7.4% | 0.69 | 0.42 | 17.6% | 11.2% | 24.2% | 20.6%/14.0% | 3.1 (interpolated) | pass | 0.366 (unverified) | 0.40 |
| 32 | `cfg_21c9` | timeframe=15min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=none, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/469/471 | 940 | 23.4% | 4.3% | 0.79 | -5.5% | 283 | 1.18 | 28.5% | 469.2 | 3/3 | 1.00 | 0.72 | 0.07 | 4 | 5.5% | 0.76 | 0.56 | 19.9% | 15.9% | 20.1% | 21.0%/15.9% | 3.8 (interpolated) | pass | 0.367 (unverified) | 0.55 |
| 33 | `cfg_dc20` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/540/590 | 1130 | 24.5% | 4.5% | 0.76 | -6.3% | 484 | 1.15 | 34.6% | 560.5 | 3/3 | 1.00 | 0.72 | 0.04 | 5 | 6.8% | 0.72 | 0.47 | 20.3% | 15.8% | 14.2% | 22.6%/17.4% | 3.6 (interpolated) | pass | 0.344 (unverified) | 0.37 |
| 34 | `cfg_ed88` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 1292/229/1197 | 2718 | 32.3% | 5.8% | 0.75 | -11.7% | 526 | 1.07 | 38.6% | 1369.0 | 3/3 | 1.00 | 0.53 | 0.22 | 3 | 7.6% | 0.76 | 0.29 | 22.0% | 11.1% | 58.7% | 28.9%/20.5% | 2.5 (interpolated) | pass | 0.342 (unverified) | -0.38 |
| 35 | `cfg_9c85` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=2.0, direction=long, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 213/211/449 | 873 | 23.1% | 4.3% | 0.83 | -9.6% | 164 | 1.18 | 15.7% | 436.5 | 3/3 | 1.00 | 0.60 | 0.23 | 5 | 15.1% | 0.31 | 0.42 | 18.8% | 14.7% | 13.9% | 19.7%/14.6% | 4.3 (interpolated) | pass | 0.410 (unverified) | -0.05 |
| 36 | `cfg_a972` | timeframe=15min, compression=nr, nr_lookback=5, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=3.0, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 85/398/478 | 961 | 21.6% | 4.0% | 0.76 | -6.2% | 514 | 1.16 | 27.7% | 480.4 | 4/4 | 1.00 | 0.65 | 0.10 | 3 | 5.3% | 0.75 | 0.60 | 16.9% | 13.1% | 16.7% | 19.9%/14.9% | 3.7 (interpolated) | pass | 0.341 (unverified) | 0.64 |
| 37 | `cfg_0da9` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=2.0, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 136/149/290 | 575 | 12.4% | 2.4% | 0.81 | -6.1% | 686 | 1.22 | 10.4% | 286.5 | 3/3 | 1.00 | 0.62 | 0.19 | 4 | 4.1% | 0.67 | 0.57 | 10.7% | 8.6% | 11.1% | 10.8%/7.5% | 4.1 (interpolated) | pass | 0.389 (unverified) | 0.18 |
| 38 | `cfg_dede` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=False, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 635/264/586 | 1485 | 22.9% | 4.2% | 0.81 | -7.0% | 572 | 1.12 | 28.5% | 745.9 | 3/3 | 1.00 | 0.51 | 0.30 | 4 | 4.5% | 0.80 | 0.32 | 13.2% | 8.3% | 18.2% | 19.0%/11.8% | 2.9 (interpolated) | pass | 0.394 (unverified) | -0.13 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 23.9% / 1.85 / 382 | 0.9% / 0.16 / 371 | 24.3% / 1.46 / 394 | 6.6% / 0.77 / 403 | 20.6% / 1.23 / 409 |
| 2 | 21.1% / 1.65 / 399 | -1.0% / -0.13 / 393 | 15.4% / 0.98 / 408 | 12.3% / 1.40 / 430 | 22.3% / 1.35 / 426 |
| 3 | 26.1% / 1.72 / 490 | -0.7% / -0.04 / 487 | -1.5% / 0.01 / 523 | 19.5% / 2.26 / 500 | 35.3% / 1.76 / 517 |
| 4 | 5.6% / 0.63 / 342 | -1.7% / -0.33 / 319 | 16.3% / 1.32 / 342 | -3.2% / -0.53 / 359 | 34.1% / 2.70 / 340 |
| 5 | 18.9% / 1.58 / 422 | 0.2% / 0.06 / 406 | 17.3% / 1.07 / 417 | 9.5% / 1.13 / 448 | 17.9% / 1.17 / 439 |
| 6 | 18.8% / 1.58 / 396 | 0.2% / 0.06 / 379 | 22.5% / 1.41 / 403 | 5.5% / 0.68 / 414 | 13.4% / 0.92 / 421 |
| 7 | 14.6% / 1.33 / 498 | -2.3% / -0.38 / 453 | 10.0% / 0.91 / 523 | 1.5% / 0.29 / 465 | 26.2% / 2.10 / 497 |
| 8 | 11.0% / 1.13 / 337 | -1.7% / -0.33 / 318 | 19.3% / 1.61 / 347 | -5.9% / -1.05 / 342 | 27.9% / 2.37 / 337 |
| 9 | 12.9% / 1.20 / 322 | -2.9% / -0.56 / 295 | 19.2% / 1.43 / 329 | -2.2% / -0.31 / 330 | 22.2% / 1.84 / 319 |
| 10 | 19.7% / 1.43 / 532 | 0.2% / 0.07 / 523 | -1.9% / -0.01 / 559 | 22.0% / 2.40 / 536 | 32.3% / 1.65 / 543 |
| 11 | 7.0% / 0.64 / 392 | -5.6% / -0.91 / 380 | 8.2% / 0.63 / 408 | 0.4% / 0.09 / 390 | 46.5% / 3.13 / 382 |
| 12 | 8.8% / 0.85 / 319 | -3.5% / -0.68 / 297 | 16.0% / 1.16 / 314 | 1.0% / 0.19 / 336 | 25.2% / 1.99 / 311 |
| 13 | 12.4% / 0.92 / 474 | 3.2% / 0.49 / 447 | 11.1% / 0.76 / 479 | 0.7% / 0.13 / 492 | 34.6% / 1.96 / 460 |
| 14 | 10.7% / 0.88 / 367 | -6.6% / -1.06 / 353 | 2.6% / 0.26 / 370 | 2.2% / 0.35 / 374 | 48.8% / 2.99 / 349 |
| 15 | 9.0% / 0.72 / 508 | 4.8% / 0.71 / 473 | 12.0% / 0.81 / 497 | 1.4% / 0.21 / 516 | 35.5% / 1.97 / 477 |
| 16 | 17.0% / 1.55 / 360 | -0.6% / -0.08 / 349 | 31.8% / 1.89 / 360 | 5.1% / 0.67 / 385 | 0.2% / 0.08 / 390 |
| 17 | 3.0% / 0.35 / 436 | -4.6% / -0.84 / 412 | 7.4% / 0.65 / 439 | -0.3% / -0.01 / 433 | 44.0% / 3.00 / 431 |
| 18 | -1.2% / -0.25 / 181 | 4.0% / 1.13 / 224 | 9.1% / 1.35 / 237 | -0.7% / -0.17 / 222 | 12.3% / 1.93 / 138 |
| 19 | 14.0% / 1.28 / 353 | 0.6% / 0.14 / 342 | 37.1% / 2.20 / 352 | 0.9% / 0.15 / 378 | 2.3% / 0.24 / 377 |
| 20 | 6.5% / 0.60 / 376 | -6.8% / -1.17 / 370 | 10.0% / 0.75 / 383 | 2.6% / 0.39 / 393 | 39.4% / 2.57 / 366 |
| 21 | 7.8% / 1.04 / 271 | 1.7% / 0.37 / 292 | 12.6% / 1.12 / 287 | 8.4% / 1.41 / 293 | 8.9% / 0.81 / 314 |
| 22 | 17.9% / 1.24 / 467 | 1.0% / 0.18 / 429 | 0.5% / 0.11 / 434 | 1.1% / 0.17 / 449 | 43.7% / 2.23 / 430 |
| 23 | 17.1% / 1.25 / 394 | -7.4% / -1.18 / 411 | 5.5% / 0.42 / 421 | 3.7% / 0.55 / 419 | 31.0% / 1.97 / 416 |
| 24 | 6.8% / 1.01 / 172 | -2.5% / -0.89 / 177 | 6.0% / 0.76 / 192 | 5.0% / 1.23 / 179 | 16.5% / 1.83 / 205 |
| 25 | 14.5% / 1.69 / 397 | 0.9% / 0.22 / 381 | 13.9% / 1.49 / 415 | -6.2% / -1.23 / 398 | 8.9% / 1.03 / 416 |
| 26 | 16.4% / 1.20 / 425 | 1.0% / 0.17 / 394 | 2.3% / 0.22 / 412 | -1.8% / -0.18 / 423 | 44.4% / 2.30 / 407 |
| 27 | 13.0% / 1.67 / 280 | 0.9% / 0.24 / 298 | 12.8% / 1.16 / 297 | 5.9% / 1.13 / 298 | 5.2% / 0.56 / 316 |
| 28 | 6.3% / 0.93 / 173 | -1.8% / -0.65 / 178 | 8.1% / 1.00 / 195 | 4.1% / 1.08 / 179 | 16.1% / 1.86 / 205 |
| 29 | -1.9% / -0.41 / 184 | 2.4% / 0.67 / 224 | 6.4% / 1.02 / 246 | -1.4% / -0.37 / 220 | 16.9% / 2.52 / 138 |
| 30 | 4.8% / 0.69 / 234 | 7.4% / 1.62 / 248 | 11.5% / 1.20 / 273 | -2.2% / -0.42 / 271 | 8.8% / 0.95 / 275 |
| 31 | 2.0% / 0.43 / 229 | 3.5% / 0.91 / 280 | 2.2% / 0.32 / 295 | -0.4% / -0.07 / 274 | 15.2% / 2.09 / 181 |
| 32 | -2.6% / -0.48 / 173 | 3.2% / 0.82 / 207 | 4.9% / 0.71 / 222 | 0.1% / 0.03 / 212 | 17.0% / 2.29 / 126 |
| 33 | 0.1% / 0.05 / 200 | 3.1% / 0.75 / 250 | 2.9% / 0.40 / 265 | 0.6% / 0.15 / 258 | 16.6% / 2.18 / 157 |
| 34 | 8.1% / 0.94 / 543 | -5.1% / -1.09 / 519 | 10.6% / 1.17 / 576 | -5.3% / -1.02 / 522 | 22.9% / 2.10 / 558 |
| 35 | 2.9% / 0.60 / 151 | 7.0% / 2.10 / 184 | 3.8% / 0.60 / 180 | 1.9% / 0.59 / 173 | 5.7% / 0.87 / 185 |
| 36 | -3.4% / -0.72 / 178 | 3.0% / 0.83 / 210 | 5.9% / 0.86 / 231 | -0.1% / -0.02 / 213 | 15.5% / 2.16 / 129 |
| 37 | -1.8% / -0.71 / 98 | 0.6% / 0.30 / 142 | 3.7% / 1.02 / 135 | 1.6% / 0.84 / 124 | 8.0% / 2.01 / 76 |
| 38 | 1.9% / 0.45 / 279 | 3.2% / 0.88 / 320 | 0.8% / 0.15 / 367 | -1.4% / -0.32 / 309 | 17.6% / 2.37 / 210 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_01bf` | 6 | 0.84 | 0.87/0.87 | 0.85/0.85 |
| 1 | `cfg_be71` | 3 | 0.95 | 0.93/0.93 | 0.97/0.97 |
| 2 | `cfg_042c` | 2 | 0.96 | 0.96/0.96 | 0.97/0.97 |
| 3 | `cfg_fd56` | 4 | 0.88 | 0.92/0.92 | 0.90/0.90 |
| 4 | `cfg_0da9` | 1 | n/a | n/a/n/a | n/a/n/a |
| 5 | `cfg_0ea1` | 4 | 0.87 | 0.89/0.96 | 0.82/0.94 |
| 6 | `cfg_0f95` | 2 | 0.95 | 0.98/0.98 | 0.97/0.97 |
| 7 | `cfg_4fce` | 4 | 0.81 | 0.83/0.91 | 0.87/0.95 |
| 8 | `cfg_21c9` | 2 | 0.96 | 0.97/0.97 | 0.97/0.97 |
| 9 | `cfg_6563` | 3 | 0.90 | 0.92/0.94 | 0.95/0.96 |
| 10 | `cfg_4ce2` | 6 | 0.82 | 0.85/0.91 | 0.69/0.91 |
| 11 | `cfg_74e4` | 2 | 0.83 | 0.81/0.81 | 0.69/0.69 |
| 12 | `cfg_9cc7` | 5 | 0.84 | 0.88/0.93 | 0.81/0.89 |
| 13 | `cfg_f8ee` | 4 | 0.85 | 0.86/0.93 | 0.80/0.90 |
| 14 | `cfg_6a30` | 2 | 0.90 | 0.80/0.80 | 0.73/0.73 |
| 15 | `cfg_97f7` | 1 | n/a | n/a/n/a | n/a/n/a |
| 16 | `cfg_9c85` | 1 | n/a | n/a/n/a | n/a/n/a |
| 17 | `cfg_ffe0` | 3 | 0.84 | 0.87/0.89 | 0.85/0.87 |
| 18 | `cfg_f5e7` | 2 | 0.92 | 0.92/0.92 | 0.90/0.90 |
| 19 | `cfg_dede` | 1 | n/a | n/a/n/a | n/a/n/a |
| 20 | `cfg_ed07` | 1 | n/a | n/a/n/a | n/a/n/a |
| 21 | `cfg_ed88` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 5.600e-04 over 400 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 87.0, participation ratio 7.9, 95%-variance components 54 (rank bound T = 1259); raw grid 400; raw + known prior 606736
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
