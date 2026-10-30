# Screening funnel -- nb_es_v1 (development stages only)

- Code: `eb2334601b76` (dirty working tree: True, diff sha256 `833c5c08837e`)
- Config: `configs/funnel/nb_funnel_es_v1.yaml` sha256 `4aa1d55cfc423d2d`; seed 20261030
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'NQ': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `3648106644e6389d` (210 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **False** -- No noise-band strategy has been selected or scored on ES 2023-2024. The mean-reversion family was validated there (mr_es_v6_1h, mr_es_v6_15m, mr_es_v5, mr_es_v4, mr_es_v3), so the period has been looked at by the researcher, but not for this strategy.
- Holdout 2025+ previously inspected: **False** -- No noise-band metrics have been computed on ES 2025+. ES 2025+ bars were read for mean-reversion holdout scoring (combined_v1 via combined_portfolio_holdout on 2026-10-25; mr_es_v6_1h via portfolio_holdout on 2026-10-24; trades_v1 via trade_distribution on 2026-10-25) per the mean-reversion data-access ledger: a different strategy family, so this is still the first test of this strategy, but the researcher has seen how that period treated mean reversion.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 8100 | 8100 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 8100 | 8100 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 8100 | 8100 | 0 | 0 |  | 8100 | 100.00 | 100.00 |  |
| 3 performance & risk | hard_gate | 8100 | 1613 | 6487 | 0 |  | 0 | 19.91 | 19.91 |  |
| 4 parameter stability | hard_gate | 1613 | 1595 | 18 | 0 |  | 0 | 19.69 | 98.88 |  |
| 5 time stability | hard_gate | 1595 | 1567 | 28 | 0 |  | 1273 | 19.35 | 98.24 |  |
| 6 deduplication | dedup | 1567 | 210 |  |  | 1357 |  | 2.59 | 13.40 | best 2 per cluster |
| 7 execution stress | hard_gate | 210 | 210 | 0 | 0 |  | 0 | 2.59 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 210 |  |  |  |  |  |  |  | diagnostic only: unverified: 210 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s3:hard_reject:max_drawdown | 7 |
| s3:hard_reject:net_return | 697 |
| s3:hard_reject:sharpe | 6487 |
| s4:hard_reject:local_median_sharpe | 18 |
| s5:hard_reject:profitable_years | 28 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | trail/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | NQ dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_c665` | timeframe=5min, band_lookback=30, band_mult=1.0, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 172/227/0 | 399 | 36.1% | 6.4% | 1.34 | -3.7% | 223 | 1.56 | 15.0% | 186.4 | 8/8 | 1.00 | 1.32 | 0.01 | 5 | 22.0% | 0.39 | 0.38 | 30.9% | 28.2% | 29.5% | 32.6%/28.0% | 5.7 (interpolated) | pass | 0.827 (unverified) | 1.12 |
| 2 | `cfg_eae4` | timeframe=5min, band_lookback=30, band_mult=1.0, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 172/227/0 | 399 | 36.1% | 6.4% | 1.34 | -3.7% | 223 | 1.56 | 15.0% | 186.4 | 7/7 | 1.00 | 1.33 | 0.01 | 5 | 22.0% | 0.39 | 0.38 | 30.9% | 28.2% | 29.5% | 32.4%/28.1% | 5.7 (interpolated) | pass | 0.827 (unverified) | 1.12 |
| 3 | `cfg_0998` | timeframe=15min, band_lookback=30, band_mult=1.25, check_minutes=15, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 157/188/0 | 345 | 31.6% | 5.6% | 1.36 | -2.1% | 196 | 1.61 | 13.1% | 160.7 | 7/7 | 1.00 | 1.31 | 0.05 | 5 | 18.8% | 0.40 | 0.41 | 28.8% | 25.8% | 18.1% | 29.1%/23.9% | 5.7 (interpolated) | pass | 0.846 (unverified) | 1.14 |
| 4 | `cfg_ead3` | timeframe=5min, band_lookback=30, band_mult=1.0, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 125/226/0 | 351 | 31.0% | 5.5% | 1.28 | -3.7% | 169 | 1.57 | 13.8% | 163.6 | 7/7 | 1.00 | 1.26 | 0.01 | 5 | 16.9% | 0.45 | 0.42 | 27.7% | 23.9% | 26.5% | 28.7%/24.7% | 5.7 (interpolated) | pass | 0.787 (unverified) | 1.00 |
| 5 | `cfg_0d5d` | timeframe=5min, band_lookback=30, band_mult=1.25, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 119/188/0 | 307 | 33.2% | 5.9% | 1.38 | -2.6% | 123 | 1.70 | 12.3% | 142.9 | 7/7 | 1.00 | 1.32 | 0.07 | 5 | 21.4% | 0.36 | 0.40 | 30.8% | 28.0% | 27.7% | 30.4%/25.6% | 6.8 (interpolated) | pass | 0.865 (unverified) | 1.28 |
| 6 | `cfg_13ec` | timeframe=15min, band_lookback=30, band_mult=1.0, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 126/226/0 | 352 | 30.7% | 5.5% | 1.26 | -3.7% | 169 | 1.56 | 14.0% | 164.1 | 7/7 | 1.00 | 1.24 | 0.02 | 5 | 16.9% | 0.45 | 0.42 | 27.4% | 23.7% | 24.7% | 28.9%/25.1% | 5.6 (interpolated) | pass | 0.776 (unverified) | 1.01 |
| 7 | `cfg_b835` | timeframe=15min, band_lookback=14, band_mult=1.0, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 185/252/0 | 437 | 37.2% | 6.5% | 1.40 | -3.0% | 138 | 1.56 | 16.4% | 203.2 | 8/8 | 1.00 | 1.25 | 0.15 | 5 | 20.8% | 0.44 | 0.36 | 32.6% | 28.0% | 26.3% | 33.1%/28.8% | 5.3 (interpolated) | pass | 0.867 (unverified) | 1.31 |
| 8 | `cfg_d167` | timeframe=15min, band_lookback=14, band_mult=1.0, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 185/252/0 | 437 | 37.2% | 6.5% | 1.40 | -3.0% | 138 | 1.56 | 16.4% | 203.2 | 9/9 | 1.00 | 1.30 | 0.09 | 5 | 20.8% | 0.44 | 0.36 | 32.6% | 28.0% | 26.3% | 33.1%/28.9% | 5.3 (interpolated) | pass | 0.867 (unverified) | 1.31 |
| 9 | `cfg_0c6c` | timeframe=15min, band_lookback=30, band_mult=1.25, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 194/188/0 | 382 | 32.7% | 5.8% | 1.32 | -2.9% | 220 | 1.56 | 13.5% | 178.1 | 6/6 | 1.00 | 1.32 | -0.00 | 5 | 20.9% | 0.36 | 0.41 | 28.8% | 25.5% | 13.4% | 28.7%/24.4% | 5.3 (interpolated) | pass | 0.801 (unverified) | 1.15 |
| 10 | `cfg_a97e` | timeframe=5min, band_lookback=14, band_mult=1.0, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 443/441/0 | 884 | 71.6% | 11.4% | 1.41 | -6.2% | 295 | 1.36 | 29.3% | 414.3 | 9/9 | 1.00 | 1.26 | 0.15 | 4 | 46.1% | 0.36 | 0.26 | 63.5% | 49.8% | 45.3% | 66.6%/55.2% | 4.8 (interpolated) | pass | 0.859 (unverified) | 1.48 |
| 11 | `cfg_bf12` | timeframe=5min, band_lookback=14, band_mult=1.0, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 443/441/0 | 884 | 71.6% | 11.4% | 1.41 | -6.2% | 295 | 1.36 | 29.3% | 414.3 | 8/8 | 1.00 | 1.22 | 0.19 | 4 | 46.1% | 0.36 | 0.26 | 63.5% | 49.8% | 45.3% | 66.8%/56.9% | 4.8 (interpolated) | pass | 0.859 (unverified) | 1.48 |
| 12 | `cfg_81aa` | timeframe=5min, band_lookback=30, band_mult=1.25, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 192/188/0 | 380 | 32.5% | 5.8% | 1.32 | -2.9% | 196 | 1.56 | 13.2% | 177.3 | 6/6 | 1.00 | 1.33 | -0.01 | 5 | 20.1% | 0.38 | 0.40 | 28.6% | 25.6% | 26.3% | 28.9%/24.2% | 5.4 (interpolated) | pass | 0.799 (unverified) | 1.13 |
| 13 | `cfg_36e3` | timeframe=5min, band_lookback=20, band_mult=1.25, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 334/355/0 | 689 | 47.0% | 8.0% | 1.09 | -4.8% | 194 | 1.29 | 23.5% | 320.4 | 9/9 | 1.00 | 1.09 | 0.00 | 5 | 30.8% | 0.30 | 0.37 | 41.5% | 33.4% | 25.2% | 44.0%/36.2% | 4.6 (interpolated) | pass | 0.621 (unverified) | 1.64 |
| 14 | `cfg_d947` | timeframe=5min, band_lookback=20, band_mult=1.25, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 334/355/0 | 689 | 47.0% | 8.0% | 1.09 | -4.8% | 194 | 1.29 | 23.5% | 320.4 | 8/8 | 1.00 | 1.08 | 0.00 | 5 | 30.8% | 0.30 | 0.37 | 41.5% | 33.4% | 25.2% | 44.3%/37.8% | 4.6 (interpolated) | pass | 0.621 (unverified) | 1.64 |
| 15 | `cfg_920a` | timeframe=5min, band_lookback=14, band_mult=1.0, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 341/443/0 | 784 | 72.7% | 11.6% | 1.53 | -6.0% | 295 | 1.41 | 27.2% | 369.1 | 8/8 | 1.00 | 1.19 | 0.34 | 4 | 42.7% | 0.41 | 0.25 | 63.0% | 50.7% | 53.6% | 64.9%/54.9% | 5.2 (interpolated) | pass | 0.914 (unverified) | 1.54 |
| 16 | `cfg_a4ab` | timeframe=5min, band_lookback=20, band_mult=1.25, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 257/355/0 | 612 | 46.1% | 7.9% | 1.16 | -5.2% | 293 | 1.33 | 21.8% | 283.6 | 8/8 | 1.00 | 1.11 | 0.05 | 4 | 26.8% | 0.42 | 0.37 | 40.4% | 32.2% | 28.4% | 43.2%/35.3% | 4.8 (interpolated) | pass | 0.688 (unverified) | 1.71 |
| 17 | `cfg_1275` | timeframe=15min, band_lookback=20, band_mult=1.0, check_minutes=15, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 236/237/0 | 473 | 36.0% | 6.4% | 1.33 | -2.7% | 202 | 1.49 | 16.3% | 220.7 | 8/8 | 1.00 | 1.20 | 0.14 | 5 | 22.4% | 0.38 | 0.41 | 30.6% | 26.2% | 22.1% | 31.8%/27.5% | 4.9 (interpolated) | pass | 0.829 (unverified) | 1.08 |
| 18 | `cfg_9df7` | timeframe=5min, band_lookback=10, band_mult=1.0, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 360/455/0 | 815 | 58.5% | 9.7% | 1.31 | -7.3% | 297 | 1.32 | 27.7% | 382.8 | 8/8 | 1.00 | 1.17 | 0.14 | 4 | 36.5% | 0.38 | 0.31 | 45.6% | 36.8% | 40.9% | 52.0%/41.7% | 4.2 (interpolated) | pass | 0.801 (unverified) | 1.67 |
| 19 | `cfg_862a` | timeframe=15min, band_lookback=20, band_mult=1.25, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 258/356/0 | 614 | 45.7% | 7.8% | 1.16 | -5.1% | 293 | 1.33 | 22.2% | 284.9 | 8/8 | 1.00 | 1.12 | 0.04 | 4 | 26.4% | 0.42 | 0.38 | 39.7% | 32.0% | 22.4% | 41.5%/33.8% | 4.8 (interpolated) | pass | 0.683 (unverified) | 1.79 |
| 20 | `cfg_c6ab` | timeframe=5min, band_lookback=30, band_mult=0.75, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 181/276/0 | 457 | 38.3% | 6.7% | 1.36 | -2.8% | 126 | 1.51 | 17.1% | 214.2 | 6/6 | 1.00 | 1.20 | 0.15 | 5 | 22.4% | 0.41 | 0.34 | 32.9% | 28.3% | 28.8% | 33.4%/28.4% | 5.3 (interpolated) | pass | 0.833 (unverified) | 1.07 |
| 21 | `cfg_27d3` | timeframe=5min, band_lookback=30, band_mult=0.75, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 239/276/0 | 515 | 40.8% | 7.1% | 1.32 | -3.5% | 126 | 1.46 | 18.6% | 239.7 | 7/7 | 1.00 | 1.32 | 0.01 | 5 | 27.9% | 0.32 | 0.33 | 35.2% | 31.0% | 29.1% | 37.4%/31.1% | 5.0 (interpolated) | pass | 0.810 (unverified) | 1.17 |
| 22 | `cfg_b9d6` | timeframe=5min, band_lookback=30, band_mult=0.75, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 239/276/0 | 515 | 40.8% | 7.1% | 1.32 | -3.5% | 126 | 1.46 | 18.6% | 239.7 | 6/6 | 1.00 | 1.26 | 0.06 | 5 | 27.9% | 0.32 | 0.33 | 35.2% | 31.0% | 29.1% | 36.6%/32.8% | 5.0 (interpolated) | pass | 0.810 (unverified) | 1.17 |
| 23 | `cfg_4efe` | timeframe=15min, band_lookback=30, band_mult=1.0, check_minutes=15, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 171/231/0 | 402 | 30.4% | 5.4% | 1.19 | -3.3% | 182 | 1.46 | 14.7% | 187.6 | 6/6 | 1.00 | 1.16 | 0.02 | 5 | 17.2% | 0.43 | 0.48 | 26.7% | 22.6% | 24.3% | 27.5%/21.8% | 5.0 (interpolated) | pass | 0.713 (unverified) | 0.87 |
| 24 | `cfg_f60c` | timeframe=5min, band_lookback=20, band_mult=1.0, check_minutes=15, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 236/237/0 | 473 | 35.3% | 6.2% | 1.31 | -3.1% | 196 | 1.48 | 15.9% | 220.9 | 8/8 | 1.00 | 1.21 | 0.10 | 5 | 21.2% | 0.40 | 0.41 | 30.1% | 25.3% | 25.7% | 32.0%/25.8% | 4.8 (interpolated) | pass | 0.811 (unverified) | 1.04 |
| 25 | `cfg_954a` | timeframe=5min, band_lookback=20, band_mult=0.75, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 196/289/0 | 485 | 26.5% | 4.8% | 0.99 | -3.5% | 129 | 1.33 | 17.7% | 225.4 | 7/7 | 1.00 | 0.96 | 0.03 | 5 | 17.1% | 0.36 | 0.48 | 21.7% | 15.9% | 19.4% | 24.3%/18.7% | 3.9 (interpolated) | pass | 0.531 (unverified) | 1.10 |
| 26 | `cfg_86c5` | timeframe=15min, band_lookback=10, band_mult=1.25, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 232/212/0 | 444 | 24.5% | 4.5% | 1.01 | -3.3% | 161 | 1.37 | 14.5% | 206.7 | 7/7 | 1.00 | 0.97 | 0.04 | 5 | 14.3% | 0.42 | 0.52 | 18.8% | 14.4% | 11.8% | 20.7%/15.6% | 3.8 (interpolated) | pass | 0.555 (unverified) | 1.31 |
| 27 | `cfg_52c3` | timeframe=5min, band_lookback=7, band_mult=2.0, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 159/233/0 | 392 | 28.5% | 5.2% | 0.92 | -6.4% | 397 | 1.34 | 14.1% | 182.9 | 7/7 | 1.00 | 0.90 | 0.02 | 3 | 13.8% | 0.45 | 0.50 | 24.3% | 20.8% | 19.6% | 27.5%/22.1% | 5.0 (interpolated) | pass | 0.467 (unverified) | 1.30 |
| 28 | `cfg_b8af` | timeframe=5min, band_lookback=7, band_mult=2.0, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 159/233/0 | 392 | 28.5% | 5.2% | 0.92 | -6.4% | 397 | 1.34 | 14.1% | 182.9 | 6/6 | 1.00 | 0.89 | 0.04 | 3 | 13.8% | 0.45 | 0.50 | 24.3% | 20.8% | 19.6% | 26.9%/21.1% | 5.0 (interpolated) | pass | 0.467 (unverified) | 1.30 |
| 29 | `cfg_6b22` | timeframe=5min, band_lookback=30, band_mult=0.75, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 377/281/0 | 658 | 40.9% | 7.1% | 1.21 | -3.2% | 144 | 1.39 | 19.9% | 305.1 | 5/5 | 1.00 | 1.16 | 0.05 | 5 | 23.7% | 0.38 | 0.40 | 35.3% | 25.7% | 34.1% | 37.4%/30.7% | 4.1 (interpolated) | pass | 0.724 (unverified) | 1.00 |
| 30 | `cfg_5c08` | timeframe=15min, band_lookback=10, band_mult=1.25, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 358/379/0 | 737 | 39.0% | 6.8% | 0.95 | -5.4% | 379 | 1.25 | 25.2% | 341.1 | 8/8 | 1.00 | 0.97 | -0.02 | 3 | 24.5% | 0.37 | 0.42 | 28.4% | 22.1% | 16.0% | 32.3%/27.0% | 3.6 (interpolated) | pass | 0.496 (unverified) | 1.91 |
| 31 | `cfg_c597` | timeframe=15min, band_lookback=10, band_mult=1.25, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 358/379/0 | 737 | 39.0% | 6.8% | 0.95 | -5.4% | 379 | 1.25 | 25.2% | 341.1 | 9/9 | 1.00 | 0.95 | 0.00 | 3 | 24.5% | 0.37 | 0.42 | 28.4% | 22.1% | 16.0% | 34.6%/25.2% | 3.6 (interpolated) | pass | 0.496 (unverified) | 1.91 |
| 32 | `cfg_a9e0` | timeframe=15min, band_lookback=20, band_mult=1.25, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 209/191/0 | 400 | 23.9% | 4.4% | 0.98 | -4.8% | 336 | 1.39 | 13.7% | 185.8 | 7/7 | 1.00 | 1.07 | -0.09 | 4 | 11.7% | 0.51 | 0.54 | 19.4% | 14.9% | 11.8% | 21.1%/17.1% | 4.1 (interpolated) | pass | 0.524 (unverified) | 1.02 |
| 33 | `cfg_078b` | timeframe=5min, band_lookback=30, band_mult=0.75, check_minutes=15, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 322/281/0 | 603 | 36.1% | 6.4% | 1.15 | -3.3% | 293 | 1.37 | 19.2% | 280.6 | 6/6 | 1.00 | 1.17 | -0.02 | 5 | 23.3% | 0.36 | 0.43 | 29.5% | 22.9% | 27.1% | 33.5%/27.6% | 3.9 (interpolated) | pass | 0.681 (unverified) | 1.06 |
| 34 | `cfg_b907` | timeframe=5min, band_lookback=30, band_mult=1.0, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 503/182/0 | 685 | 33.4% | 5.9% | 1.20 | -4.9% | 302 | 1.46 | 13.6% | 319.1 | 6/6 | 1.00 | 1.08 | 0.12 | 5 | 17.5% | 0.47 | 0.49 | 26.9% | 17.6% | 29.3% | 30.6%/27.2% | 3.6 (interpolated) | pass | 0.724 (unverified) | 1.21 |
| 35 | `cfg_76b0` | timeframe=5min, band_lookback=20, band_mult=1.25, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 206/191/0 | 397 | 24.2% | 4.4% | 0.99 | -4.0% | 336 | 1.39 | 13.5% | 184.1 | 7/7 | 1.00 | 1.04 | -0.05 | 5 | 11.9% | 0.51 | 0.53 | 18.6% | 14.3% | 17.2% | 20.3%/13.8% | 4.1 (interpolated) | pass | 0.529 (unverified) | 1.00 |
| 36 | `cfg_3002` | timeframe=15min, band_lookback=20, band_mult=0.75, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 199/288/0 | 487 | 25.7% | 4.7% | 0.96 | -3.5% | 129 | 1.32 | 18.1% | 226.6 | 7/7 | 1.00 | 0.99 | -0.03 | 5 | 16.7% | 0.35 | 0.49 | 20.9% | 15.2% | 17.6% | 24.7%/17.3% | 3.7 (interpolated) | pass | 0.503 (unverified) | 1.16 |
| 37 | `cfg_1071` | timeframe=5min, band_lookback=10, band_mult=1.25, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 231/212/0 | 443 | 23.5% | 4.3% | 0.97 | -3.3% | 161 | 1.36 | 14.1% | 206.2 | 7/7 | 1.00 | 1.00 | -0.03 | 5 | 13.2% | 0.44 | 0.54 | 17.9% | 13.8% | 15.4% | 18.8%/14.3% | 3.8 (interpolated) | pass | 0.514 (unverified) | 1.23 |
| 38 | `cfg_ccc2` | timeframe=5min, band_lookback=14, band_mult=0.75, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 468/517/0 | 985 | 44.1% | 7.6% | 0.97 | -6.9% | 305 | 1.20 | 32.8% | 461.3 | 7/7 | 1.00 | 0.97 | -0.00 | 4 | 22.1% | 0.41 | 0.39 | 32.8% | 22.6% | 34.4% | 41.1%/31.6% | 3.2 (interpolated) | pass | 0.511 (unverified) | 1.45 |
| 39 | `cfg_1568` | timeframe=15min, band_lookback=30, band_mult=1.0, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 503/182/0 | 685 | 33.2% | 5.9% | 1.20 | -4.9% | 315 | 1.46 | 14.6% | 318.9 | 6/6 | 1.00 | 1.07 | 0.14 | 5 | 17.4% | 0.48 | 0.49 | 26.6% | 17.7% | 10.7% | 31.0%/24.1% | 3.6 (interpolated) | pass | 0.723 (unverified) | 1.30 |
| 40 | `cfg_03aa` | timeframe=15min, band_lookback=20, band_mult=1.0, check_minutes=60, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 258/414/0 | 672 | 47.5% | 8.1% | 1.10 | -7.4% | 481 | 1.30 | 25.6% | 314.0 | 8/8 | 1.00 | 1.08 | 0.02 | 5 | 21.1% | 0.55 | 0.36 | 40.9% | 31.8% | 30.9% | 42.8%/32.0% | 4.5 (interpolated) | pass | 0.630 (unverified) | 1.09 |
| 41 | `cfg_5aeb` | timeframe=15min, band_lookback=20, band_mult=1.0, check_minutes=60, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 258/414/0 | 672 | 47.5% | 8.1% | 1.10 | -7.4% | 481 | 1.30 | 25.6% | 314.0 | 7/7 | 1.00 | 1.08 | 0.02 | 5 | 21.1% | 0.55 | 0.36 | 40.9% | 31.8% | 30.9% | 41.8%/31.6% | 4.5 (interpolated) | pass | 0.630 (unverified) | 1.09 |
| 42 | `cfg_854e` | timeframe=5min, band_lookback=7, band_mult=0.75, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 506/547/0 | 1053 | 50.5% | 8.5% | 1.10 | -8.0% | 331 | 1.22 | 34.5% | 492.6 | 6/6 | 1.00 | 1.06 | 0.03 | 4 | 28.0% | 0.35 | 0.34 | 37.4% | 24.4% | 41.4% | 43.4%/34.1% | 3.3 (interpolated) | pass | 0.626 (unverified) | 1.51 |
| 43 | `cfg_b39f` | timeframe=5min, band_lookback=7, band_mult=1.5, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 205/329/0 | 534 | 36.0% | 6.4% | 0.98 | -8.5% | 534 | 1.30 | 18.8% | 250.9 | 7/7 | 1.00 | 0.94 | 0.04 | 3 | 12.4% | 0.58 | 0.43 | 30.1% | 24.3% | 24.6% | 32.2%/25.8% | 4.5 (interpolated) | pass | 0.524 (unverified) | 1.61 |
| 44 | `cfg_097c` | timeframe=5min, band_lookback=20, band_mult=0.75, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 406/292/0 | 698 | 33.3% | 5.9% | 1.06 | -3.8% | 207 | 1.31 | 20.6% | 324.0 | 6/6 | 1.00 | 1.04 | 0.02 | 4 | 15.8% | 0.49 | 0.44 | 22.9% | 15.4% | 25.6% | 30.4%/23.3% | 3.4 (interpolated) | pass | 0.592 (unverified) | 1.05 |
| 45 | `cfg_c745` | timeframe=15min, band_lookback=20, band_mult=1.0, check_minutes=15, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 579/428/0 | 1007 | 53.3% | 8.9% | 1.11 | -6.3% | 295 | 1.24 | 30.4% | 470.5 | 8/8 | 1.00 | 1.02 | 0.09 | 4 | 35.8% | 0.33 | 0.34 | 39.6% | 31.0% | 39.3% | 47.1%/37.5% | 3.6 (interpolated) | pass | 0.639 (unverified) | 1.33 |
| 46 | `cfg_b096` | timeframe=15min, band_lookback=30, band_mult=1.25, check_minutes=15, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 120/187/0 | 307 | 24.4% | 4.5% | 1.15 | -2.4% | 201 | 1.53 | 12.1% | 142.9 | 6/6 | 1.00 | 1.15 | -0.00 | 5 | 11.5% | 0.53 | 0.50 | 20.9% | 17.8% | 12.2% | 21.3%/16.4% | 5.2 (interpolated) | pass | 0.684 (unverified) | 0.93 |
| 47 | `cfg_6881` | timeframe=5min, band_lookback=7, band_mult=1.25, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 470/520/0 | 990 | 52.6% | 8.8% | 1.07 | -9.2% | 300 | 1.22 | 33.2% | 465.6 | 7/7 | 1.00 | 1.04 | 0.03 | 3 | 20.1% | 0.51 | 0.39 | 39.5% | 29.3% | 37.3% | 48.1%/38.6% | 3.6 (interpolated) | pass | 0.603 (unverified) | 1.86 |
| 48 | `cfg_f00d` | timeframe=15min, band_lookback=7, band_mult=1.5, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 205/330/0 | 535 | 35.0% | 6.2% | 0.96 | -8.5% | 534 | 1.29 | 19.2% | 250.9 | 7/7 | 1.00 | 0.95 | 0.01 | 3 | 11.5% | 0.60 | 0.44 | 28.9% | 23.2% | 20.7% | 31.8%/24.7% | 4.4 (interpolated) | pass | 0.501 (unverified) | 1.64 |
| 49 | `cfg_4d9e` | timeframe=15min, band_lookback=20, band_mult=1.0, check_minutes=15, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 447/429/0 | 876 | 44.1% | 7.6% | 1.03 | -6.7% | 320 | 1.23 | 27.8% | 409.2 | 7/7 | 1.00 | 1.07 | -0.04 | 4 | 21.8% | 0.42 | 0.40 | 34.4% | 26.5% | 38.8% | 39.3%/30.9% | 3.6 (interpolated) | pass | 0.565 (unverified) | 1.38 |
| 50 | `cfg_00ec` | timeframe=15min, band_lookback=30, band_mult=1.0, check_minutes=60, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 252/401/0 | 653 | 42.2% | 7.3% | 1.03 | -5.1% | 398 | 1.28 | 24.9% | 305.4 | 6/6 | 1.00 | 1.07 | -0.04 | 5 | 20.4% | 0.52 | 0.40 | 33.1% | 25.8% | 23.8% | 36.5%/28.9% | 4.1 (interpolated) | pass | 0.566 (unverified) | 0.97 |
| 51 | `cfg_9485` | timeframe=15min, band_lookback=30, band_mult=1.0, check_minutes=60, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 252/401/0 | 653 | 42.2% | 7.3% | 1.03 | -5.1% | 398 | 1.28 | 24.9% | 305.4 | 7/7 | 1.00 | 1.04 | -0.01 | 5 | 20.4% | 0.52 | 0.40 | 33.1% | 25.8% | 23.8% | 38.7%/28.5% | 4.1 (interpolated) | pass | 0.566 (unverified) | 0.97 |
| 52 | `cfg_7e4d` | timeframe=15min, band_lookback=20, band_mult=0.75, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 409/292/0 | 701 | 32.5% | 5.8% | 1.01 | -4.0% | 259 | 1.30 | 21.2% | 325.6 | 6/6 | 1.00 | 1.05 | -0.04 | 5 | 15.4% | 0.49 | 0.48 | 24.3% | 14.9% | 13.6% | 29.5%/22.1% | 3.3 (interpolated) | pass | 0.555 (unverified) | 1.12 |
| 53 | `cfg_10c0` | timeframe=15min, band_lookback=7, band_mult=1.25, check_minutes=15, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 145/222/0 | 367 | 22.5% | 4.1% | 1.04 | -2.7% | 196 | 1.40 | 13.4% | 170.4 | 6/6 | 1.00 | 0.94 | 0.09 | 4 | 11.0% | 0.51 | 0.56 | 19.1% | 14.3% | 14.9% | 19.5%/15.3% | 4.4 (interpolated) | pass | 0.577 (unverified) | 0.93 |
| 54 | `cfg_5a52` | timeframe=15min, band_lookback=10, band_mult=1.25, check_minutes=15, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 133/211/0 | 344 | 18.1% | 3.4% | 0.88 | -3.3% | 291 | 1.36 | 12.5% | 158.9 | 7/7 | 1.00 | 0.86 | 0.02 | 4 | 8.1% | 0.55 | 0.67 | 13.8% | 11.3% | 11.4% | 15.2%/10.9% | 3.9 (interpolated) | pass | 0.426 (unverified) | 1.14 |
| 55 | `cfg_7f54` | timeframe=5min, band_lookback=7, band_mult=1.5, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 353/436/0 | 789 | 47.7% | 8.1% | 1.06 | -8.9% | 323 | 1.25 | 26.9% | 369.9 | 7/7 | 1.00 | 0.91 | 0.15 | 4 | 15.4% | 0.59 | 0.39 | 38.4% | 28.1% | 37.8% | 42.7%/35.3% | 3.8 (interpolated) | pass | 0.590 (unverified) | 1.71 |
| 56 | `cfg_2219` | timeframe=15min, band_lookback=14, band_mult=1.5, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 243/298/0 | 541 | 40.1% | 7.0% | 1.04 | -8.8% | 496 | 1.33 | 19.7% | 251.3 | 9/9 | 1.00 | 1.03 | 0.01 | 5 | 26.4% | 0.34 | 0.40 | 33.0% | 28.0% | 17.9% | 38.3%/29.8% | 4.8 (interpolated) | pass | 0.576 (unverified) | 1.69 |
| 57 | `cfg_7a0b` | timeframe=15min, band_lookback=14, band_mult=1.5, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 243/298/0 | 541 | 40.1% | 7.0% | 1.04 | -8.8% | 496 | 1.33 | 19.7% | 251.3 | 8/8 | 1.00 | 1.03 | 0.01 | 5 | 26.4% | 0.34 | 0.40 | 33.0% | 28.0% | 17.9% | 37.6%/30.9% | 4.8 (interpolated) | pass | 0.576 (unverified) | 1.69 |
| 58 | `cfg_c67b` | timeframe=5min, band_lookback=30, band_mult=1.25, check_minutes=15, first_entry_minutes=60, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 120/187/0 | 307 | 24.0% | 4.4% | 1.13 | -2.3% | 201 | 1.52 | 11.8% | 142.8 | 6/6 | 1.00 | 1.15 | -0.03 | 5 | 10.8% | 0.55 | 0.51 | 20.4% | 16.9% | 15.9% | 21.0%/14.9% | 5.2 (interpolated) | pass | 0.664 (unverified) | 0.90 |
| 59 | `cfg_809c` | timeframe=5min, band_lookback=7, band_mult=1.25, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 374/392/0 | 766 | 41.6% | 7.2% | 0.97 | -5.3% | 391 | 1.24 | 25.6% | 357.0 | 8/8 | 1.00 | 0.97 | -0.00 | 4 | 19.3% | 0.45 | 0.40 | 30.9% | 23.1% | 21.7% | 40.3%/29.6% | 3.7 (interpolated) | pass | 0.511 (unverified) | 1.63 |
| 60 | `cfg_9bd3` | timeframe=5min, band_lookback=7, band_mult=1.25, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 374/392/0 | 766 | 41.6% | 7.2% | 0.97 | -5.3% | 391 | 1.24 | 25.6% | 357.0 | 7/7 | 1.00 | 0.97 | 0.00 | 4 | 19.3% | 0.45 | 0.40 | 30.9% | 23.1% | 21.7% | 38.9%/29.9% | 3.7 (interpolated) | pass | 0.511 (unverified) | 1.63 |
| 61 | `cfg_05b9` | timeframe=5min, band_lookback=30, band_mult=0.75, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 610/231/0 | 841 | 35.8% | 6.3% | 1.14 | -4.8% | 261 | 1.38 | 17.4% | 392.5 | 5/5 | 1.00 | 1.01 | 0.13 | 5 | 21.9% | 0.39 | 0.45 | 26.8% | 15.2% | 26.6% | 31.7%/25.4% | 3.1 (interpolated) | pass | 0.668 (unverified) | 1.24 |
| 62 | `cfg_b701` | timeframe=5min, band_lookback=14, band_mult=1.0, check_minutes=30, first_entry_minutes=30, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 749/583/0 | 1332 | 60.3% | 9.9% | 1.07 | -12.3% | 426 | 1.19 | 41.9% | 628.5 | 9/9 | 1.00 | 0.99 | 0.08 | 4 | 32.9% | 0.34 | 0.35 | 42.0% | 26.6% | 43.1% | 55.1%/40.0% | 3.0 (interpolated) | pass | 0.605 (unverified) | 1.33 |
| 63 | `cfg_d7c2` | timeframe=5min, band_lookback=14, band_mult=1.0, check_minutes=30, first_entry_minutes=15, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 749/583/0 | 1332 | 60.3% | 9.9% | 1.07 | -12.3% | 426 | 1.19 | 41.9% | 628.5 | 8/8 | 1.00 | 0.96 | 0.11 | 4 | 32.9% | 0.34 | 0.35 | 42.0% | 26.6% | 43.1% | 52.9%/40.8% | 3.0 (interpolated) | pass | 0.605 (unverified) | 1.33 |
| 64 | `cfg_0ed7` | timeframe=15min, band_lookback=7, band_mult=1.5, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 359/435/0 | 794 | 45.7% | 7.8% | 1.02 | -8.9% | 323 | 1.24 | 27.5% | 372.3 | 7/7 | 1.00 | 0.89 | 0.12 | 4 | 14.4% | 0.60 | 0.41 | 35.8% | 26.2% | 23.9% | 41.2%/32.8% | 3.7 (interpolated) | pass | 0.553 (unverified) | 1.73 |
| 65 | `cfg_1116` | timeframe=15min, band_lookback=30, band_mult=0.75, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 612/230/0 | 842 | 34.4% | 6.1% | 1.10 | -5.2% | 280 | 1.36 | 18.4% | 393.9 | 5/5 | 1.00 | 1.02 | 0.09 | 5 | 21.0% | 0.39 | 0.46 | 26.2% | 13.9% | 18.6% | 31.5%/25.8% | 3.0 (interpolated) | pass | 0.637 (unverified) | 1.25 |
| 66 | `cfg_41fe` | timeframe=15min, band_lookback=7, band_mult=1.25, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 477/518/0 | 995 | 50.4% | 8.5% | 1.04 | -9.0% | 258 | 1.21 | 34.0% | 467.7 | 7/7 | 1.00 | 1.02 | 0.02 | 3 | 19.0% | 0.52 | 0.40 | 37.7% | 25.6% | 27.0% | 46.9%/36.9% | 3.5 (interpolated) | pass | 0.573 (unverified) | 1.89 |
| 67 | `cfg_daac` | timeframe=5min, band_lookback=20, band_mult=0.75, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 669/431/0 | 1100 | 36.5% | 6.4% | 0.86 | -9.2% | 358 | 1.18 | 28.7% | 511.6 | 7/7 | 1.00 | 0.88 | -0.02 | 4 | 16.6% | 0.47 | 0.48 | 23.3% | 13.2% | 26.5% | 32.2%/22.7% | 2.7 (interpolated) | pass | 0.416 (unverified) | 1.52 |
| 68 | `cfg_8963` | timeframe=5min, band_lookback=7, band_mult=1.0, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 622/604/0 | 1226 | 55.6% | 9.2% | 1.06 | -6.4% | 368 | 1.20 | 39.9% | 575.1 | 7/7 | 1.00 | 0.98 | 0.07 | 4 | 26.1% | 0.42 | 0.38 | 39.8% | 25.1% | 38.5% | 48.9%/38.4% | 3.1 (interpolated) | pass | 0.593 (unverified) | 1.63 |
| 69 | `cfg_2731` | timeframe=5min, band_lookback=20, band_mult=0.75, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 803/430/0 | 1233 | 41.0% | 7.1% | 0.88 | -9.0% | 180 | 1.18 | 30.9% | 576.5 | 7/7 | 1.00 | 0.88 | 0.00 | 4 | 22.9% | 0.36 | 0.43 | 28.2% | 14.0% | 23.5% | 36.8%/26.7% | 2.7 (interpolated) | pass | 0.434 (unverified) | 1.52 |
| 70 | `cfg_73b2` | timeframe=5min, band_lookback=20, band_mult=0.75, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 803/430/0 | 1233 | 41.0% | 7.1% | 0.88 | -9.0% | 180 | 1.18 | 30.9% | 576.5 | 8/8 | 1.00 | 0.87 | 0.01 | 4 | 22.9% | 0.36 | 0.43 | 28.2% | 14.0% | 23.5% | 36.5%/28.5% | 2.7 (interpolated) | pass | 0.434 (unverified) | 1.52 |
| 71 | `cfg_5771` | timeframe=15min, band_lookback=20, band_mult=0.75, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 670/430/0 | 1100 | 36.0% | 6.3% | 0.85 | -9.2% | 347 | 1.17 | 29.9% | 512.1 | 7/7 | 1.00 | 0.86 | -0.01 | 4 | 16.1% | 0.48 | 0.48 | 22.4% | 12.5% | 25.9% | 31.8%/22.7% | 2.7 (interpolated) | pass | 0.408 (unverified) | 1.53 |
| 72 | `cfg_6022` | timeframe=5min, band_lookback=10, band_mult=1.0, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 609/596/0 | 1205 | 50.8% | 8.6% | 0.99 | -7.5% | 368 | 1.18 | 39.0% | 567.0 | 8/8 | 1.00 | 0.96 | 0.03 | 4 | 22.3% | 0.46 | 0.41 | 37.3% | 23.1% | 36.6% | 49.1%/38.2% | 3.1 (interpolated) | pass | 0.526 (unverified) | 1.47 |
| 73 | `cfg_123a` | timeframe=15min, band_lookback=30, band_mult=1.0, check_minutes=15, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 374/182/0 | 556 | 24.2% | 4.4% | 1.08 | -4.5% | 475 | 1.42 | 13.0% | 259.0 | 6/6 | 1.00 | 1.00 | 0.08 | 5 | 9.6% | 0.61 | 0.58 | 18.5% | 12.9% | 14.2% | 22.0%/16.4% | 3.4 (interpolated) | pass | 0.619 (unverified) | 1.15 |
| 74 | `cfg_14b4` | timeframe=5min, band_lookback=14, band_mult=0.75, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 761/679/0 | 1440 | 50.8% | 8.6% | 0.92 | -9.9% | 379 | 1.16 | 45.7% | 672.8 | 7/7 | 1.00 | 0.92 | 0.01 | 4 | 27.2% | 0.37 | 0.40 | 33.5% | 18.8% | 35.1% | 46.0%/35.2% | 2.8 (interpolated) | pass | 0.471 (unverified) | 1.25 |
| 75 | `cfg_c3e9` | timeframe=15min, band_lookback=14, band_mult=1.5, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 157/154/0 | 311 | 17.3% | 3.2% | 0.91 | -4.4% | 306 | 1.39 | 10.8% | 143.5 | 7/7 | 1.00 | 0.83 | 0.08 | 5 | 9.7% | 0.44 | 0.66 | 14.0% | 11.1% | 8.0% | 15.1%/10.9% | 4.0 (interpolated) | pass | 0.459 (unverified) | 1.21 |
| 76 | `cfg_35e4` | timeframe=5min, band_lookback=10, band_mult=0.75, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 275/310/0 | 585 | 34.3% | 6.1% | 1.15 | -3.7% | 128 | 1.36 | 20.2% | 272.1 | 8/8 | 1.00 | 1.11 | 0.04 | 4 | 20.2% | 0.35 | 0.39 | 29.1% | 22.4% | 25.5% | 31.4%/27.3% | 4.0 (interpolated) | pass | 0.675 (unverified) | 1.13 |
| 77 | `cfg_a339` | timeframe=5min, band_lookback=10, band_mult=0.75, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 275/310/0 | 585 | 34.3% | 6.1% | 1.15 | -3.7% | 128 | 1.36 | 20.2% | 272.1 | 7/7 | 1.00 | 1.12 | 0.03 | 4 | 20.2% | 0.35 | 0.39 | 29.1% | 22.4% | 25.5% | 32.0%/27.2% | 4.0 (interpolated) | pass | 0.675 (unverified) | 1.13 |
| 78 | `cfg_4d73` | timeframe=15min, band_lookback=20, band_mult=0.75, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 382/252/0 | 634 | 25.1% | 4.6% | 0.92 | -4.2% | 217 | 1.30 | 18.0% | 296.6 | 8/8 | 1.00 | 0.90 | 0.02 | 5 | 13.2% | 0.45 | 0.53 | 18.5% | 10.8% | 17.4% | 23.2%/16.5% | 3.0 (interpolated) | pass | 0.464 (unverified) | 1.23 |
| 79 | `cfg_d9c9` | timeframe=15min, band_lookback=20, band_mult=0.75, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 382/252/0 | 634 | 25.1% | 4.6% | 0.92 | -4.2% | 217 | 1.30 | 18.0% | 296.6 | 7/7 | 1.00 | 0.92 | 0.00 | 5 | 13.2% | 0.45 | 0.53 | 18.5% | 10.8% | 17.4% | 22.1%/17.6% | 3.0 (interpolated) | pass | 0.464 (unverified) | 1.23 |
| 80 | `cfg_7de1` | timeframe=5min, band_lookback=14, band_mult=1.25, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 430/489/0 | 919 | 56.8% | 9.4% | 1.17 | -7.4% | 227 | 1.26 | 31.3% | 432.2 | 8/8 | 1.00 | 0.93 | 0.24 | 4 | 24.1% | 0.46 | 0.35 | 41.9% | 33.4% | 38.4% | 47.8%/37.8% | 3.9 (interpolated) | pass | 0.688 (unverified) | 1.62 |
| 81 | `cfg_1b3c` | timeframe=15min, band_lookback=30, band_mult=0.75, check_minutes=15, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 445/232/0 | 677 | 26.7% | 4.8% | 1.02 | -4.2% | 315 | 1.35 | 16.5% | 315.7 | 5/5 | 1.00 | 1.01 | 0.01 | 5 | 13.8% | 0.48 | 0.54 | 20.5% | 12.8% | 18.5% | 24.6%/18.8% | 3.0 (interpolated) | pass | 0.564 (unverified) | 1.29 |
| 82 | `cfg_8e9c` | timeframe=5min, band_lookback=20, band_mult=1.25, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 426/471/0 | 897 | 38.0% | 6.7% | 0.82 | -9.7% | 429 | 1.18 | 30.5% | 418.7 | 8/8 | 1.00 | 0.82 | -0.00 | 4 | 13.2% | 0.58 | 0.53 | 27.3% | 17.9% | 26.8% | 36.1%/26.4% | 3.0 (interpolated) | pass | 0.384 (unverified) | 1.27 |
| 83 | `cfg_1f59` | timeframe=5min, band_lookback=7, band_mult=0.75, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 802/701/0 | 1503 | 50.7% | 8.6% | 0.93 | -11.9% | 388 | 1.15 | 47.2% | 704.5 | 6/6 | 1.00 | 0.86 | 0.07 | 4 | 22.0% | 0.47 | 0.44 | 31.4% | 15.7% | 39.4% | 44.6%/31.9% | 2.6 (interpolated) | pass | 0.478 (unverified) | 1.18 |
| 84 | `cfg_8310` | timeframe=5min, band_lookback=10, band_mult=1.0, check_minutes=30, first_entry_minutes=30, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 774/593/0 | 1367 | 51.4% | 8.6% | 0.93 | -8.8% | 192 | 1.17 | 42.4% | 643.5 | 9/9 | 1.00 | 0.93 | 0.00 | 4 | 26.9% | 0.38 | 0.40 | 35.9% | 19.5% | 31.4% | 45.7%/35.0% | 2.8 (interpolated) | pass | 0.481 (unverified) | 1.54 |
| 85 | `cfg_f2f4` | timeframe=5min, band_lookback=10, band_mult=1.0, check_minutes=30, first_entry_minutes=15, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 774/593/0 | 1367 | 51.4% | 8.6% | 0.93 | -8.8% | 192 | 1.17 | 42.4% | 643.5 | 8/8 | 1.00 | 0.92 | 0.02 | 4 | 26.9% | 0.38 | 0.40 | 35.9% | 19.5% | 31.4% | 45.7%/35.3% | 2.8 (interpolated) | pass | 0.481 (unverified) | 1.54 |
| 86 | `cfg_d3c2` | timeframe=5min, band_lookback=30, band_mult=1.0, check_minutes=15, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 374/182/0 | 556 | 24.0% | 4.4% | 1.07 | -4.6% | 457 | 1.42 | 12.2% | 258.2 | 6/6 | 1.00 | 0.99 | 0.07 | 5 | 9.1% | 0.62 | 0.59 | 17.9% | 12.4% | 21.1% | 21.9%/17.0% | 3.3 (interpolated) | pass | 0.606 (unverified) | 1.14 |
| 87 | `cfg_c8b3` | timeframe=15min, band_lookback=10, band_mult=1.25, check_minutes=15, first_entry_minutes=30, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 785/503/0 | 1288 | 42.3% | 7.3% | 0.85 | -12.7% | 402 | 1.16 | 37.8% | 598.3 | 8/8 | 1.00 | 0.86 | -0.01 | 4 | 19.1% | 0.46 | 0.44 | 28.3% | 16.5% | 24.4% | 39.4%/31.0% | 2.7 (interpolated) | pass | 0.404 (unverified) | 1.75 |
| 88 | `cfg_8079` | timeframe=15min, band_lookback=20, band_mult=1.25, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 430/470/0 | 900 | 37.7% | 6.6% | 0.82 | -9.7% | 429 | 1.17 | 31.2% | 419.7 | 8/8 | 1.00 | 0.84 | -0.02 | 4 | 12.3% | 0.60 | 0.54 | 27.4% | 18.2% | 24.4% | 33.5%/22.9% | 3.1 (interpolated) | pass | 0.380 (unverified) | 1.30 |
| 89 | `cfg_d623` | timeframe=5min, band_lookback=14, band_mult=1.5, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 158/154/0 | 312 | 14.8% | 2.8% | 0.79 | -5.4% | 319 | 1.32 | 10.6% | 143.1 | 7/7 | 1.00 | 0.77 | 0.01 | 4 | 7.9% | 0.47 | 0.77 | 12.4% | 8.6% | 11.7% | 13.0%/9.2% | 3.6 (interpolated) | pass | 0.344 (unverified) | 1.18 |
| 90 | `cfg_31e8` | timeframe=5min, band_lookback=30, band_mult=0.75, check_minutes=15, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 445/232/0 | 677 | 26.3% | 4.8% | 1.01 | -4.2% | 315 | 1.35 | 15.6% | 316.2 | 5/5 | 1.00 | 1.01 | 0.00 | 5 | 13.4% | 0.49 | 0.54 | 20.0% | 11.7% | 19.9% | 23.2%/17.9% | 3.0 (interpolated) | pass | 0.551 (unverified) | 1.28 |
| 91 | `cfg_3763` | timeframe=5min, band_lookback=7, band_mult=1.5, check_minutes=30, first_entry_minutes=30, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 463/438/0 | 901 | 45.0% | 7.7% | 0.98 | -10.3% | 242 | 1.22 | 29.8% | 421.0 | 8/8 | 1.00 | 0.91 | 0.07 | 5 | 18.5% | 0.50 | 0.41 | 33.9% | 25.2% | 32.6% | 40.1%/32.1% | 3.5 (interpolated) | pass | 0.520 (unverified) | 1.54 |
| 92 | `cfg_71c4` | timeframe=5min, band_lookback=7, band_mult=1.5, check_minutes=30, first_entry_minutes=15, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 463/438/0 | 901 | 45.0% | 7.7% | 0.98 | -10.3% | 242 | 1.22 | 29.8% | 421.0 | 7/7 | 1.00 | 0.91 | 0.07 | 5 | 18.5% | 0.50 | 0.41 | 33.9% | 25.2% | 32.6% | 41.7%/33.4% | 3.5 (interpolated) | pass | 0.520 (unverified) | 1.54 |
| 93 | `cfg_eb5c` | timeframe=15min, band_lookback=20, band_mult=0.75, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 311/252/0 | 563 | 21.9% | 4.1% | 0.89 | -4.3% | 295 | 1.30 | 16.6% | 263.1 | 7/7 | 1.00 | 0.89 | 0.00 | 5 | 12.6% | 0.43 | 0.58 | 16.2% | 10.2% | 12.4% | 19.8%/13.9% | 3.0 (interpolated) | pass | 0.438 (unverified) | 1.19 |
| 94 | `cfg_e55f` | timeframe=5min, band_lookback=20, band_mult=0.75, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 311/252/0 | 563 | 21.8% | 4.0% | 0.89 | -4.3% | 295 | 1.30 | 16.0% | 263.0 | 7/7 | 1.00 | 0.89 | -0.00 | 5 | 12.4% | 0.43 | 0.58 | 16.1% | 10.2% | 14.5% | 19.2%/14.1% | 3.0 (interpolated) | pass | 0.434 (unverified) | 1.17 |
| 95 | `cfg_e438` | timeframe=15min, band_lookback=14, band_mult=1.25, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 436/486/0 | 922 | 54.5% | 9.1% | 1.14 | -7.2% | 234 | 1.25 | 31.9% | 433.7 | 8/8 | 1.00 | 0.97 | 0.17 | 4 | 23.0% | 0.47 | 0.37 | 40.3% | 32.2% | 31.9% | 49.8%/39.7% | 3.8 (interpolated) | pass | 0.660 (unverified) | 1.65 |
| 96 | `cfg_29ae` | timeframe=15min, band_lookback=14, band_mult=1.0, check_minutes=60, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 452/587/0 | 1039 | 44.2% | 7.6% | 0.88 | -14.7% | 749 | 1.18 | 38.2% | 487.3 | 7/7 | 1.00 | 0.98 | -0.10 | 4 | 19.6% | 0.47 | 0.44 | 29.5% | 19.4% | 33.1% | 38.2%/26.7% | 3.0 (interpolated) | pass | 0.429 (unverified) | 1.20 |
| 97 | `cfg_4812` | timeframe=15min, band_lookback=14, band_mult=1.0, check_minutes=60, first_entry_minutes=15, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 452/587/0 | 1039 | 44.2% | 7.6% | 0.88 | -14.7% | 749 | 1.18 | 38.2% | 487.3 | 7/7 | 1.00 | 0.98 | -0.10 | 4 | 19.6% | 0.47 | 0.44 | 29.5% | 19.4% | 33.1% | 39.9%/27.8% | 3.0 (interpolated) | pass | 0.429 (unverified) | 1.20 |
| 98 | `cfg_40f8` | timeframe=15min, band_lookback=14, band_mult=1.25, check_minutes=60, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 205/356/0 | 561 | 30.6% | 5.5% | 0.83 | -7.6% | 500 | 1.24 | 21.1% | 260.7 | 8/8 | 1.00 | 0.83 | 0.00 | 3 | 14.2% | 0.54 | 0.50 | 25.5% | 19.3% | 18.3% | 27.9%/20.5% | 3.9 (interpolated) | pass | 0.390 (unverified) | 1.57 |
| 99 | `cfg_dbb8` | timeframe=15min, band_lookback=14, band_mult=1.25, check_minutes=60, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 205/356/0 | 561 | 30.6% | 5.5% | 0.83 | -7.6% | 500 | 1.24 | 21.1% | 260.7 | 7/7 | 1.00 | 0.83 | 0.00 | 3 | 14.2% | 0.54 | 0.50 | 25.5% | 19.3% | 18.3% | 27.9%/20.2% | 3.9 (interpolated) | pass | 0.390 (unverified) | 1.57 |
| 100 | `cfg_0617` | timeframe=15min, band_lookback=30, band_mult=0.75, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 357/231/0 | 588 | 29.3% | 5.3% | 1.00 | -6.1% | 126 | 1.35 | 17.3% | 274.8 | 6/6 | 1.00 | 0.99 | 0.01 | 5 | 17.7% | 0.38 | 0.47 | 23.8% | 17.4% | 19.6% | 26.2%/20.7% | 3.6 (interpolated) | pass | 0.540 (unverified) | 1.24 |
| 101 | `cfg_201b` | timeframe=15min, band_lookback=30, band_mult=0.75, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 357/231/0 | 588 | 29.3% | 5.3% | 1.00 | -6.1% | 126 | 1.35 | 17.3% | 274.8 | 7/7 | 1.00 | 0.98 | 0.02 | 5 | 17.7% | 0.38 | 0.47 | 23.8% | 17.4% | 19.6% | 25.0%/20.0% | 3.6 (interpolated) | pass | 0.540 (unverified) | 1.24 |
| 102 | `cfg_3e6a` | timeframe=5min, band_lookback=30, band_mult=0.75, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 761/407/0 | 1168 | 46.0% | 7.9% | 0.99 | -7.7% | 165 | 1.20 | 29.9% | 550.4 | 7/7 | 1.00 | 0.97 | 0.02 | 4 | 26.1% | 0.38 | 0.38 | 31.5% | 18.3% | 24.0% | 41.0%/30.7% | 2.9 (interpolated) | pass | 0.528 (unverified) | 1.37 |
| 103 | `cfg_a3a5` | timeframe=5min, band_lookback=30, band_mult=0.75, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 761/407/0 | 1168 | 46.0% | 7.9% | 0.99 | -7.7% | 165 | 1.20 | 29.9% | 550.4 | 6/6 | 1.00 | 0.98 | 0.01 | 4 | 26.1% | 0.38 | 0.38 | 31.5% | 18.3% | 24.0% | 39.4%/31.3% | 2.9 (interpolated) | pass | 0.528 (unverified) | 1.37 |
| 104 | `cfg_88cc` | timeframe=15min, band_lookback=7, band_mult=1.25, check_minutes=15, first_entry_minutes=60, anchor=open, trail=vwap, direction=short, stop_atr_multiple=none | 363/231/0 | 594 | 34.5% | 6.1% | 0.97 | -8.1% | 376 | 1.27 | 16.4% | 278.1 | 6/6 | 1.00 | 0.87 | 0.10 | 3 | 11.0% | 0.61 | 0.46 | 26.8% | 19.8% | 21.5% | 32.7%/26.0% | 3.9 (interpolated) | pass | 0.514 (unverified) | 1.52 |
| 105 | `cfg_69b1` | timeframe=5min, band_lookback=10, band_mult=1.25, check_minutes=15, first_entry_minutes=30, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 781/502/0 | 1283 | 41.5% | 7.2% | 0.82 | -15.8% | 423 | 1.16 | 36.5% | 596.2 | 8/8 | 1.00 | 0.84 | -0.02 | 4 | 18.3% | 0.47 | 0.44 | 27.3% | 15.2% | 34.0% | 38.3%/28.6% | 2.6 (interpolated) | pass | 0.383 (unverified) | 1.67 |
| 106 | `cfg_2908` | timeframe=5min, band_lookback=7, band_mult=1.25, check_minutes=15, first_entry_minutes=60, anchor=open, trail=vwap, direction=short, stop_atr_multiple=none | 363/229/0 | 592 | 34.6% | 6.1% | 0.97 | -8.0% | 376 | 1.27 | 15.8% | 276.7 | 6/6 | 1.00 | 0.87 | 0.11 | 3 | 11.3% | 0.61 | 0.45 | 26.4% | 20.0% | 25.2% | 31.2%/24.5% | 3.8 (interpolated) | pass | 0.516 (unverified) | 1.44 |
| 107 | `cfg_239e` | timeframe=5min, band_lookback=20, band_mult=1.25, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 517/355/0 | 872 | 38.0% | 6.7% | 0.85 | -11.7% | 596 | 1.21 | 25.4% | 409.2 | 7/7 | 1.00 | 0.91 | -0.07 | 5 | 18.4% | 0.52 | 0.46 | 25.4% | 20.1% | 24.6% | 33.1%/23.8% | 3.2 (interpolated) | pass | 0.402 (unverified) | 1.27 |
| 108 | `cfg_7721` | timeframe=5min, band_lookback=30, band_mult=1.25, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 510/266/0 | 776 | 34.2% | 6.1% | 0.92 | -7.9% | 237 | 1.25 | 19.3% | 362.5 | 8/8 | 1.00 | 0.84 | 0.08 | 5 | 21.9% | 0.36 | 0.48 | 25.5% | 19.1% | 18.5% | 31.4%/23.8% | 3.4 (interpolated) | pass | 0.467 (unverified) | 1.39 |
| 109 | `cfg_e6d3` | timeframe=5min, band_lookback=30, band_mult=1.25, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 510/266/0 | 776 | 34.2% | 6.1% | 0.92 | -7.9% | 237 | 1.25 | 19.3% | 362.5 | 7/7 | 1.00 | 0.82 | 0.10 | 5 | 21.9% | 0.36 | 0.48 | 25.5% | 19.1% | 18.5% | 31.9%/23.3% | 3.4 (interpolated) | pass | 0.467 (unverified) | 1.39 |
| 110 | `cfg_ee1c` | timeframe=5min, band_lookback=7, band_mult=1.5, check_minutes=15, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 472/455/0 | 927 | 35.7% | 6.3% | 0.81 | -15.6% | 676 | 1.18 | 28.5% | 434.1 | 6/6 | 1.00 | 0.79 | 0.02 | 3 | 9.9% | 0.66 | 0.48 | 23.7% | 15.0% | 29.2% | 32.5%/25.7% | 2.8 (interpolated) | pass | 0.372 (unverified) | 1.29 |
| 111 | `cfg_c4ed` | timeframe=15min, band_lookback=7, band_mult=1.5, check_minutes=15, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 474/458/0 | 932 | 35.6% | 6.3% | 0.81 | -15.3% | 676 | 1.17 | 29.4% | 436.5 | 6/6 | 1.00 | 0.78 | 0.02 | 3 | 9.5% | 0.67 | 0.48 | 24.5% | 15.6% | 23.6% | 32.6%/22.2% | 2.9 (interpolated) | pass | 0.370 (unverified) | 1.41 |
| 112 | `cfg_5237` | timeframe=5min, band_lookback=14, band_mult=1.0, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 693/445/0 | 1138 | 38.4% | 6.7% | 0.80 | -11.0% | 534 | 1.17 | 31.2% | 532.3 | 7/7 | 1.00 | 0.90 | -0.10 | 3 | 20.2% | 0.47 | 0.46 | 23.4% | 13.4% | 27.6% | 35.3%/24.3% | 2.7 (interpolated) | pass | 0.363 (unverified) | 0.96 |
| 113 | `cfg_4163` | timeframe=5min, band_lookback=10, band_mult=1.5, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 346/413/0 | 759 | 39.0% | 6.8% | 0.91 | -12.0% | 490 | 1.22 | 26.2% | 355.0 | 8/8 | 1.00 | 0.82 | 0.09 | 4 | 14.9% | 0.54 | 0.48 | 31.2% | 21.4% | 35.4% | 36.6%/28.0% | 3.6 (interpolated) | pass | 0.458 (unverified) | 1.65 |
| 114 | `cfg_de0e` | timeframe=15min, band_lookback=10, band_mult=1.5, check_minutes=15, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 364/321/0 | 685 | 35.0% | 6.2% | 0.93 | -6.7% | 397 | 1.25 | 22.0% | 319.2 | 8/8 | 1.00 | 0.87 | 0.07 | 4 | 18.4% | 0.47 | 0.44 | 28.5% | 20.9% | 22.2% | 31.4%/25.8% | 3.7 (interpolated) | pass | 0.477 (unverified) | 1.59 |
| 115 | `cfg_11bf` | timeframe=15min, band_lookback=30, band_mult=1.0, check_minutes=60, first_entry_minutes=30, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 416/538/0 | 954 | 39.4% | 6.9% | 0.76 | -12.1% | 425 | 1.17 | 35.3% | 447.5 | 7/7 | 1.00 | 0.76 | 0.00 | 4 | 21.0% | 0.47 | 0.49 | 25.8% | 16.6% | 24.8% | 32.0%/22.5% | 2.9 (interpolated) | pass | 0.342 (unverified) | 0.84 |
| 116 | `cfg_310d` | timeframe=15min, band_lookback=30, band_mult=1.0, check_minutes=60, first_entry_minutes=15, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 416/538/0 | 954 | 39.4% | 6.9% | 0.76 | -12.1% | 425 | 1.17 | 35.3% | 447.5 | 6/6 | 1.00 | 0.76 | 0.01 | 4 | 21.0% | 0.47 | 0.49 | 25.8% | 16.6% | 24.8% | 34.2%/24.6% | 2.9 (interpolated) | pass | 0.342 (unverified) | 0.84 |
| 117 | `cfg_32ed` | timeframe=5min, band_lookback=20, band_mult=1.25, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=short, stop_atr_multiple=none | 243/207/0 | 450 | 25.4% | 4.6% | 0.76 | -7.9% | 439 | 1.22 | 14.3% | 210.0 | 8/8 | 1.00 | 0.76 | -0.00 | 3 | 8.9% | 0.60 | 0.63 | 20.9% | 15.9% | 19.2% | 23.6%/16.9% | 4.0 (interpolated) | pass | 0.326 (unverified) | 1.17 |
| 118 | `cfg_73c6` | timeframe=5min, band_lookback=20, band_mult=1.0, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 669/426/0 | 1095 | 42.2% | 7.3% | 0.88 | -9.6% | 448 | 1.18 | 30.4% | 513.0 | 7/7 | 1.00 | 0.85 | 0.03 | 4 | 24.8% | 0.41 | 0.42 | 32.7% | 20.6% | 35.2% | 39.5%/32.2% | 3.0 (interpolated) | pass | 0.429 (unverified) | 1.24 |
| 119 | `cfg_a28c` | timeframe=15min, band_lookback=10, band_mult=1.5, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 351/411/0 | 762 | 38.1% | 6.7% | 0.89 | -12.0% | 490 | 1.21 | 26.7% | 356.2 | 8/8 | 1.00 | 0.83 | 0.07 | 4 | 14.7% | 0.54 | 0.49 | 29.9% | 20.2% | 21.1% | 34.8%/26.7% | 3.5 (interpolated) | pass | 0.442 (unverified) | 1.69 |
| 120 | `cfg_2be2` | timeframe=15min, band_lookback=30, band_mult=1.5, check_minutes=30, first_entry_minutes=15, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 397/367/0 | 764 | 37.0% | 6.5% | 0.84 | -8.7% | 202 | 1.19 | 26.8% | 356.0 | 7/7 | 1.00 | 0.84 | 0.00 | 5 | 23.0% | 0.31 | 0.55 | 26.5% | 19.2% | 22.6% | 30.6%/21.2% | 3.4 (interpolated) | pass | 0.399 (unverified) | 1.29 |
| 121 | `cfg_e42d` | timeframe=15min, band_lookback=30, band_mult=1.5, check_minutes=30, first_entry_minutes=30, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 397/367/0 | 764 | 37.0% | 6.5% | 0.84 | -8.7% | 202 | 1.19 | 26.8% | 356.0 | 8/8 | 1.00 | 0.84 | 0.00 | 5 | 23.0% | 0.31 | 0.55 | 26.5% | 19.2% | 22.6% | 31.0%/21.7% | 3.4 (interpolated) | pass | 0.399 (unverified) | 1.29 |
| 122 | `cfg_a9f5` | timeframe=5min, band_lookback=10, band_mult=1.25, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 558/382/0 | 940 | 37.2% | 6.5% | 0.84 | -9.8% | 538 | 1.20 | 26.5% | 439.0 | 7/7 | 1.00 | 0.89 | -0.05 | 4 | 17.7% | 0.52 | 0.45 | 25.4% | 15.7% | 28.1% | 32.5%/23.7% | 2.9 (interpolated) | pass | 0.398 (unverified) | 1.43 |
| 123 | `cfg_e8c9` | timeframe=15min, band_lookback=20, band_mult=1.5, check_minutes=15, first_entry_minutes=60, anchor=open, trail=band_vwap, direction=short, stop_atr_multiple=none | 434/144/0 | 578 | 25.5% | 4.6% | 0.89 | -6.1% | 387 | 1.28 | 10.9% | 270.9 | 7/7 | 1.00 | 0.75 | 0.15 | 3 | 13.8% | 0.46 | 0.60 | 19.0% | 14.0% | 14.3% | 23.6%/16.4% | 3.3 (interpolated) | pass | 0.440 (unverified) | 1.09 |
| 124 | `cfg_9cf2` | timeframe=15min, band_lookback=7, band_mult=0.75, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 448/260/0 | 708 | 23.8% | 4.4% | 0.91 | -4.3% | 148 | 1.26 | 19.2% | 330.6 | 6/6 | 1.00 | 0.86 | 0.05 | 5 | 14.5% | 0.36 | 0.53 | 16.4% | 9.3% | 14.1% | 19.9%/15.9% | 2.8 (interpolated) | pass | 0.457 (unverified) | 1.34 |
| 125 | `cfg_bb84` | timeframe=15min, band_lookback=7, band_mult=0.75, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 448/260/0 | 708 | 23.8% | 4.4% | 0.91 | -4.3% | 148 | 1.26 | 19.2% | 330.6 | 7/7 | 1.00 | 0.84 | 0.07 | 5 | 14.5% | 0.36 | 0.53 | 16.4% | 9.3% | 14.1% | 20.8%/15.6% | 2.8 (interpolated) | pass | 0.457 (unverified) | 1.34 |
| 126 | `cfg_942c` | timeframe=5min, band_lookback=10, band_mult=1.5, check_minutes=15, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 363/321/0 | 684 | 32.6% | 5.8% | 0.87 | -7.5% | 397 | 1.23 | 21.4% | 318.5 | 8/8 | 1.00 | 0.85 | 0.02 | 4 | 16.5% | 0.50 | 0.48 | 26.7% | 20.9% | 23.5% | 31.0%/23.4% | 3.6 (interpolated) | pass | 0.423 (unverified) | 1.48 |
| 127 | `cfg_10c2` | timeframe=5min, band_lookback=20, band_mult=1.5, check_minutes=15, first_entry_minutes=60, anchor=open, trail=band_vwap, direction=short, stop_atr_multiple=none | 433/145/0 | 578 | 26.0% | 4.7% | 0.91 | -6.1% | 387 | 1.29 | 10.0% | 270.8 | 7/7 | 1.00 | 0.74 | 0.17 | 3 | 14.5% | 0.44 | 0.58 | 19.8% | 14.6% | 23.2% | 22.7%/16.5% | 3.4 (interpolated) | pass | 0.456 (unverified) | 1.08 |
| 128 | `cfg_d527` | timeframe=5min, band_lookback=7, band_mult=2.0, check_minutes=60, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 87/220/0 | 307 | 22.2% | 4.1% | 0.80 | -8.2% | 784 | 1.35 | 11.6% | 141.6 | 5/5 | 1.00 | 0.78 | 0.02 | 3 | 5.5% | 0.71 | 0.58 | 18.5% | 16.5% | 17.9% | 20.5%/16.1% | 4.9 (interpolated) | pass | 0.361 (unverified) | 1.05 |
| 129 | `cfg_e378` | timeframe=5min, band_lookback=7, band_mult=2.0, check_minutes=60, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 87/220/0 | 307 | 22.2% | 4.1% | 0.80 | -8.2% | 784 | 1.35 | 11.6% | 141.6 | 6/6 | 1.00 | 0.79 | 0.01 | 3 | 5.5% | 0.71 | 0.58 | 18.5% | 16.5% | 17.9% | 20.2%/15.2% | 4.9 (interpolated) | pass | 0.361 (unverified) | 1.05 |
| 130 | `cfg_0fab` | timeframe=15min, band_lookback=20, band_mult=1.25, check_minutes=60, first_entry_minutes=30, anchor=open, trail=vwap, direction=short, stop_atr_multiple=none | 186/216/0 | 402 | 25.9% | 4.7% | 0.77 | -9.9% | 839 | 1.25 | 14.2% | 188.9 | 8/8 | 1.00 | 0.76 | 0.00 | 3 | 10.6% | 0.53 | 0.58 | 22.7% | 18.9% | 17.8% | 23.8%/18.0% | 4.5 (interpolated) | pass | 0.332 (unverified) | 1.00 |
| 131 | `cfg_22b9` | timeframe=15min, band_lookback=20, band_mult=1.25, check_minutes=60, first_entry_minutes=60, anchor=open, trail=vwap, direction=short, stop_atr_multiple=none | 186/216/0 | 402 | 25.9% | 4.7% | 0.77 | -9.9% | 839 | 1.25 | 14.2% | 188.9 | 7/7 | 1.00 | 0.77 | 0.00 | 3 | 10.6% | 0.53 | 0.58 | 22.7% | 18.9% | 17.8% | 23.9%/16.6% | 4.5 (interpolated) | pass | 0.332 (unverified) | 1.00 |
| 132 | `cfg_0da9` | timeframe=15min, band_lookback=20, band_mult=1.25, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=short, stop_atr_multiple=none | 244/208/0 | 452 | 25.7% | 4.7% | 0.77 | -7.7% | 430 | 1.23 | 14.7% | 210.9 | 8/8 | 1.00 | 0.76 | 0.01 | 3 | 9.2% | 0.59 | 0.62 | 20.6% | 15.8% | 17.2% | 24.1%/17.5% | 4.0 (interpolated) | pass | 0.333 (unverified) | 1.18 |
| 133 | `cfg_9f62` | timeframe=15min, band_lookback=7, band_mult=1.5, check_minutes=15, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 378/343/0 | 721 | 31.5% | 5.6% | 0.83 | -7.5% | 390 | 1.21 | 22.8% | 335.1 | 7/7 | 1.00 | 0.81 | 0.02 | 3 | 15.4% | 0.51 | 0.47 | 24.3% | 16.7% | 17.0% | 28.0%/20.4% | 3.3 (interpolated) | pass | 0.386 (unverified) | 1.31 |
| 134 | `cfg_b8a1` | timeframe=15min, band_lookback=20, band_mult=1.25, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 551/261/0 | 812 | 30.1% | 5.4% | 0.79 | -10.1% | 555 | 1.21 | 20.5% | 377.7 | 8/8 | 1.00 | 0.80 | -0.01 | 5 | 15.6% | 0.48 | 0.49 | 21.8% | 13.8% | 9.2% | 27.8%/20.6% | 3.0 (interpolated) | pass | 0.357 (unverified) | 1.53 |
| 135 | `cfg_cbf2` | timeframe=15min, band_lookback=20, band_mult=1.25, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 551/261/0 | 812 | 30.1% | 5.4% | 0.79 | -10.1% | 555 | 1.21 | 20.5% | 377.7 | 9/9 | 1.00 | 0.79 | 0.00 | 5 | 15.6% | 0.48 | 0.49 | 21.8% | 13.8% | 9.2% | 27.4%/20.1% | 3.0 (interpolated) | pass | 0.357 (unverified) | 1.53 |
| 136 | `cfg_11f5` | timeframe=5min, band_lookback=7, band_mult=1.25, check_minutes=15, first_entry_minutes=30, anchor=open, trail=vwap, direction=short, stop_atr_multiple=none | 459/229/0 | 688 | 31.6% | 5.6% | 0.83 | -8.6% | 428 | 1.22 | 17.3% | 320.8 | 7/7 | 1.00 | 0.82 | 0.01 | 3 | 9.9% | 0.63 | 0.51 | 23.0% | 15.4% | 24.2% | 30.8%/22.2% | 3.4 (interpolated) | pass | 0.383 (unverified) | 1.34 |
| 137 | `cfg_9d1b` | timeframe=5min, band_lookback=7, band_mult=1.25, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=short, stop_atr_multiple=none | 269/231/0 | 500 | 32.8% | 5.8% | 0.97 | -6.3% | 324 | 1.28 | 15.4% | 233.1 | 7/7 | 1.00 | 0.86 | 0.11 | 3 | 12.2% | 0.56 | 0.47 | 27.5% | 20.7% | 26.7% | 29.4%/20.1% | 4.3 (interpolated) | pass | 0.512 (unverified) | 1.60 |
| 138 | `cfg_c3c6` | timeframe=5min, band_lookback=30, band_mult=1.25, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 434/267/0 | 701 | 29.3% | 5.3% | 0.87 | -7.9% | 534 | 1.24 | 17.9% | 326.3 | 7/7 | 1.00 | 0.82 | 0.05 | 4 | 12.1% | 0.59 | 0.51 | 23.1% | 15.2% | 20.1% | 26.6%/18.8% | 3.2 (interpolated) | pass | 0.421 (unverified) | 1.38 |
| 139 | `cfg_2e11` | timeframe=5min, band_lookback=7, band_mult=1.5, check_minutes=15, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 378/342/0 | 720 | 30.3% | 5.4% | 0.81 | -7.9% | 391 | 1.21 | 22.1% | 333.8 | 7/7 | 1.00 | 0.83 | -0.02 | 3 | 14.1% | 0.53 | 0.47 | 23.7% | 16.6% | 20.5% | 28.6%/20.5% | 3.3 (interpolated) | pass | 0.365 (unverified) | 1.24 |
| 140 | `cfg_19d7` | timeframe=15min, band_lookback=7, band_mult=1.25, check_minutes=15, first_entry_minutes=30, anchor=open, trail=vwap, direction=short, stop_atr_multiple=none | 462/230/0 | 692 | 31.2% | 5.6% | 0.83 | -8.1% | 427 | 1.22 | 18.2% | 322.3 | 7/7 | 1.00 | 0.74 | 0.08 | 3 | 9.8% | 0.63 | 0.51 | 22.6% | 15.5% | 17.5% | 29.5%/22.1% | 3.3 (interpolated) | pass | 0.380 (unverified) | 1.44 |
| 141 | `cfg_0d1a` | timeframe=15min, band_lookback=30, band_mult=1.25, check_minutes=60, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 310/268/0 | 578 | 27.9% | 5.0% | 0.81 | -8.7% | 531 | 1.25 | 18.4% | 267.6 | 6/6 | 1.00 | 0.82 | -0.01 | 3 | 7.5% | 0.73 | 0.53 | 20.6% | 16.1% | 10.1% | 25.0%/18.0% | 3.6 (interpolated) | pass | 0.369 (unverified) | 1.34 |
| 142 | `cfg_0c8b` | timeframe=5min, band_lookback=7, band_mult=0.75, check_minutes=60, first_entry_minutes=30, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 525/457/0 | 982 | 41.2% | 7.2% | 0.94 | -8.4% | 474 | 1.20 | 30.3% | 460.3 | 6/6 | 1.00 | 0.90 | 0.04 | 4 | 17.0% | 0.50 | 0.42 | 31.6% | 19.5% | 26.8% | 36.3%/30.3% | 3.1 (interpolated) | pass | 0.482 (unverified) | 1.76 |
| 143 | `cfg_31f2` | timeframe=5min, band_lookback=7, band_mult=0.75, check_minutes=60, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 525/457/0 | 982 | 41.2% | 7.2% | 0.94 | -8.4% | 474 | 1.20 | 30.3% | 460.3 | 5/5 | 1.00 | 0.88 | 0.06 | 4 | 17.0% | 0.50 | 0.42 | 31.6% | 19.5% | 26.8% | 36.8%/27.4% | 3.1 (interpolated) | pass | 0.482 (unverified) | 1.76 |
| 144 | `cfg_1ae8` | timeframe=5min, band_lookback=7, band_mult=0.75, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 757/448/0 | 1205 | 36.5% | 6.4% | 0.88 | -7.7% | 305 | 1.17 | 30.2% | 560.2 | 6/6 | 1.00 | 0.86 | 0.01 | 4 | 15.6% | 0.50 | 0.46 | 23.2% | 13.5% | 29.0% | 33.3%/22.7% | 2.6 (interpolated) | pass | 0.429 (unverified) | 1.57 |
| 145 | `cfg_1d10` | timeframe=15min, band_lookback=7, band_mult=0.75, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 758/447/0 | 1205 | 35.8% | 6.3% | 0.87 | -7.7% | 305 | 1.17 | 31.6% | 560.2 | 6/6 | 1.00 | 0.84 | 0.02 | 4 | 14.9% | 0.51 | 0.47 | 22.2% | 12.9% | 21.6% | 32.1%/25.0% | 2.6 (interpolated) | pass | 0.418 (unverified) | 1.60 |
| 146 | `cfg_4d43` | timeframe=5min, band_lookback=7, band_mult=1.0, check_minutes=30, first_entry_minutes=60, anchor=open, trail=vwap, direction=short, stop_atr_multiple=none | 356/262/0 | 618 | 31.1% | 5.6% | 0.85 | -8.0% | 378 | 1.23 | 18.2% | 286.8 | 7/7 | 1.00 | 0.74 | 0.12 | 3 | 11.1% | 0.58 | 0.52 | 23.1% | 16.8% | 19.9% | 27.7%/19.6% | 3.5 (interpolated) | pass | 0.405 (unverified) | 1.37 |
| 147 | `cfg_80c8` | timeframe=5min, band_lookback=30, band_mult=2.0, check_minutes=15, first_entry_minutes=60, anchor=open, trail=band_vwap, direction=short, stop_atr_multiple=none | 298/100/0 | 398 | 22.5% | 4.2% | 0.95 | -5.7% | 372 | 1.38 | 6.8% | 183.4 | 5/5 | 1.00 | 0.74 | 0.22 | 4 | 8.9% | 0.60 | 0.59 | 18.8% | 15.1% | 17.3% | 20.3%/16.3% | 4.0 (interpolated) | pass | 0.498 (unverified) | 0.25 |
| 148 | `cfg_1392` | timeframe=15min, band_lookback=7, band_mult=1.25, check_minutes=60, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 374/516/0 | 890 | 43.0% | 7.4% | 0.91 | -14.8% | 601 | 1.20 | 32.6% | 414.2 | 6/6 | 1.00 | 0.90 | 0.01 | 3 | 12.5% | 0.63 | 0.44 | 33.1% | 21.2% | 32.0% | 35.9%/30.2% | 3.5 (interpolated) | pass | 0.460 (unverified) | 1.46 |
| 149 | `cfg_a69f` | timeframe=15min, band_lookback=7, band_mult=1.25, check_minutes=60, first_entry_minutes=30, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 374/516/0 | 890 | 43.0% | 7.4% | 0.91 | -14.8% | 601 | 1.20 | 32.6% | 414.2 | 7/7 | 1.00 | 0.88 | 0.03 | 3 | 12.5% | 0.63 | 0.44 | 33.1% | 21.2% | 32.0% | 39.5%/30.6% | 3.5 (interpolated) | pass | 0.460 (unverified) | 1.46 |
| 150 | `cfg_411e` | timeframe=5min, band_lookback=7, band_mult=1.5, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 179/184/0 | 363 | 15.0% | 2.8% | 0.76 | -5.0% | 480 | 1.29 | 11.9% | 165.8 | 6/6 | 1.00 | 0.75 | 0.01 | 4 | 6.2% | 0.59 | 0.69 | 12.0% | 8.9% | 11.2% | 12.5%/9.8% | 3.5 (interpolated) | pass | 0.328 (unverified) | 0.76 |
| 151 | `cfg_0ec4` | timeframe=15min, band_lookback=20, band_mult=1.0, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 305/185/0 | 490 | 22.6% | 4.2% | 1.01 | -4.3% | 288 | 1.38 | 13.7% | 228.1 | 8/8 | 1.00 | 0.90 | 0.11 | 5 | 12.1% | 0.47 | 0.55 | 18.0% | 12.3% | 13.4% | 20.7%/16.6% | 3.5 (interpolated) | pass | 0.552 (unverified) | 1.25 |
| 152 | `cfg_651a` | timeframe=15min, band_lookback=20, band_mult=1.0, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 305/185/0 | 490 | 22.6% | 4.2% | 1.01 | -4.3% | 288 | 1.38 | 13.7% | 228.1 | 9/9 | 1.00 | 0.92 | 0.09 | 5 | 12.1% | 0.47 | 0.55 | 18.0% | 12.3% | 13.4% | 20.9%/15.9% | 3.5 (interpolated) | pass | 0.552 (unverified) | 1.25 |
| 153 | `cfg_908a` | timeframe=15min, band_lookback=30, band_mult=2.0, check_minutes=15, first_entry_minutes=60, anchor=open, trail=band_vwap, direction=short, stop_atr_multiple=none | 298/100/0 | 398 | 22.5% | 4.2% | 0.95 | -5.7% | 372 | 1.38 | 7.4% | 183.4 | 5/5 | 1.00 | 0.74 | 0.22 | 4 | 8.9% | 0.60 | 0.59 | 18.8% | 15.1% | 3.1% | 19.9%/15.4% | 4.0 (interpolated) | pass | 0.498 (unverified) | 0.26 |
| 154 | `cfg_38af` | timeframe=15min, band_lookback=30, band_mult=1.0, check_minutes=15, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 787/335/0 | 1122 | 36.7% | 6.5% | 0.95 | -6.9% | 397 | 1.22 | 23.9% | 520.9 | 6/6 | 1.00 | 0.85 | 0.10 | 3 | 12.7% | 0.65 | 0.51 | 24.7% | 13.1% | 25.0% | 33.2%/24.9% | 2.7 (interpolated) | pass | 0.490 (unverified) | 1.47 |
| 155 | `cfg_67fd` | timeframe=15min, band_lookback=7, band_mult=1.5, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 110/169/0 | 279 | 15.2% | 2.9% | 0.75 | -5.3% | 333 | 1.36 | 10.8% | 127.8 | 8/8 | 1.00 | 0.71 | 0.04 | 5 | 8.3% | 0.45 | 0.76 | 12.0% | 9.5% | 10.3% | 14.0%/9.9% | 3.9 (interpolated) | pass | 0.313 (unverified) | 0.91 |
| 156 | `cfg_73c4` | timeframe=15min, band_lookback=7, band_mult=1.5, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=long, stop_atr_multiple=none | 110/169/0 | 279 | 15.2% | 2.9% | 0.75 | -5.3% | 333 | 1.36 | 10.8% | 127.8 | 7/7 | 1.00 | 0.74 | 0.01 | 5 | 8.3% | 0.45 | 0.76 | 12.0% | 9.5% | 10.3% | 13.8%/9.1% | 3.9 (interpolated) | pass | 0.313 (unverified) | 0.91 |
| 157 | `cfg_44b5` | timeframe=15min, band_lookback=10, band_mult=1.25, check_minutes=60, first_entry_minutes=15, anchor=open, trail=vwap, direction=short, stop_atr_multiple=none | 204/220/0 | 424 | 25.0% | 4.6% | 0.75 | -11.4% | 542 | 1.23 | 14.8% | 199.5 | 7/7 | 1.00 | 0.76 | -0.00 | 3 | 3.1% | 0.85 | 0.60 | 21.6% | 17.8% | 20.7% | 23.0%/16.5% | 4.2 (interpolated) | pass | 0.321 (unverified) | 1.49 |
| 158 | `cfg_4931` | timeframe=15min, band_lookback=10, band_mult=1.25, check_minutes=60, first_entry_minutes=30, anchor=open, trail=vwap, direction=short, stop_atr_multiple=none | 204/220/0 | 424 | 25.0% | 4.6% | 0.75 | -11.4% | 542 | 1.23 | 14.8% | 199.5 | 8/8 | 1.00 | 0.75 | -0.00 | 3 | 3.1% | 0.85 | 0.60 | 21.6% | 17.8% | 20.7% | 23.3%/18.1% | 4.2 (interpolated) | pass | 0.321 (unverified) | 1.49 |
| 159 | `cfg_9ec5` | timeframe=15min, band_lookback=20, band_mult=1.0, check_minutes=15, first_entry_minutes=30, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 465/194/0 | 659 | 19.3% | 3.6% | 0.78 | -7.9% | 488 | 1.28 | 14.3% | 302.6 | 8/8 | 1.00 | 0.74 | 0.04 | 4 | 6.9% | 0.64 | 0.72 | 11.8% | 5.7% | 10.6% | 16.3%/11.7% | 2.6 (interpolated) | pass | 0.350 (unverified) | 1.04 |
| 160 | `cfg_8934` | timeframe=15min, band_lookback=7, band_mult=1.25, check_minutes=60, first_entry_minutes=30, anchor=open, trail=band_vwap, direction=short, stop_atr_multiple=none | 274/196/0 | 470 | 27.3% | 4.9% | 0.84 | -5.9% | 362 | 1.27 | 13.9% | 218.3 | 7/7 | 1.00 | 0.77 | 0.07 | 3 | 9.0% | 0.61 | 0.55 | 22.1% | 17.1% | 20.1% | 25.1%/17.4% | 4.0 (interpolated) | pass | 0.394 (unverified) | 1.28 |
| 161 | `cfg_f023` | timeframe=15min, band_lookback=7, band_mult=1.25, check_minutes=60, first_entry_minutes=15, anchor=open, trail=band_vwap, direction=short, stop_atr_multiple=none | 274/196/0 | 470 | 27.3% | 4.9% | 0.84 | -5.9% | 362 | 1.27 | 13.9% | 218.3 | 6/6 | 1.00 | 0.77 | 0.07 | 3 | 9.0% | 0.61 | 0.55 | 22.1% | 17.1% | 20.1% | 23.2%/15.8% | 4.0 (interpolated) | pass | 0.394 (unverified) | 1.28 |
| 162 | `cfg_7d52` | timeframe=5min, band_lookback=30, band_mult=1.0, check_minutes=15, first_entry_minutes=30, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 956/335/0 | 1291 | 41.2% | 7.2% | 0.96 | -7.2% | 153 | 1.22 | 24.2% | 605.7 | 7/7 | 1.00 | 0.92 | 0.04 | 5 | 18.4% | 0.55 | 0.44 | 24.7% | 13.3% | 33.2% | 34.4%/27.9% | 2.6 (interpolated) | pass | 0.508 (unverified) | 1.48 |
| 163 | `cfg_6e82` | timeframe=15min, band_lookback=7, band_mult=1.25, check_minutes=60, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 223/386/0 | 609 | 29.1% | 5.2% | 0.78 | -9.6% | 541 | 1.21 | 22.3% | 284.1 | 7/7 | 1.00 | 0.78 | 0.00 | 3 | 8.5% | 0.65 | 0.54 | 22.8% | 16.9% | 18.6% | 26.0%/19.2% | 3.5 (interpolated) | pass | 0.341 (unverified) | 1.48 |
| 164 | `cfg_73b2` | timeframe=15min, band_lookback=7, band_mult=1.25, check_minutes=60, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 223/386/0 | 609 | 29.1% | 5.2% | 0.78 | -9.6% | 541 | 1.21 | 22.3% | 284.1 | 6/6 | 1.00 | 0.77 | 0.01 | 3 | 8.5% | 0.65 | 0.54 | 22.8% | 16.9% | 18.6% | 27.4%/19.6% | 3.5 (interpolated) | pass | 0.341 (unverified) | 1.48 |
| 165 | `cfg_fb79` | timeframe=15min, band_lookback=20, band_mult=0.75, check_minutes=15, first_entry_minutes=30, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 587/242/0 | 829 | 22.4% | 4.1% | 0.84 | -5.3% | 262 | 1.25 | 18.4% | 386.8 | 7/7 | 1.00 | 0.83 | 0.01 | 4 | 10.9% | 0.47 | 0.66 | 11.3% | 3.9% | 10.0% | 19.4%/13.0% | 2.3 (interpolated) | pass | 0.393 (unverified) | 1.25 |
| 166 | `cfg_264d` | timeframe=15min, band_lookback=30, band_mult=1.5, check_minutes=60, first_entry_minutes=60, anchor=open, trail=band_vwap, direction=short, stop_atr_multiple=none | 176/138/0 | 314 | 23.2% | 4.3% | 0.82 | -4.0% | 258 | 1.31 | 9.9% | 147.7 | 6/6 | 1.00 | 0.69 | 0.13 | 5 | 14.3% | 0.39 | 0.62 | 20.3% | 17.0% | 12.9% | 21.3%/16.3% | 4.9 (interpolated) | pass | 0.380 (unverified) | 0.89 |
| 167 | `cfg_d01c` | timeframe=15min, band_lookback=30, band_mult=1.5, check_minutes=60, first_entry_minutes=30, anchor=open, trail=band_vwap, direction=short, stop_atr_multiple=none | 176/138/0 | 314 | 23.2% | 4.3% | 0.82 | -4.0% | 258 | 1.31 | 9.9% | 147.7 | 7/7 | 1.00 | 0.75 | 0.08 | 5 | 14.3% | 0.39 | 0.62 | 20.3% | 17.0% | 12.9% | 20.7%/15.6% | 4.9 (interpolated) | pass | 0.380 (unverified) | 0.89 |
| 168 | `cfg_0a38` | timeframe=15min, band_lookback=10, band_mult=0.75, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 350/267/0 | 617 | 23.9% | 4.4% | 0.99 | -3.2% | 148 | 1.31 | 17.3% | 287.4 | 7/7 | 1.00 | 0.75 | 0.24 | 4 | 13.6% | 0.43 | 0.51 | 17.5% | 11.2% | 13.1% | 21.0%/14.8% | 3.1 (interpolated) | pass | 0.534 (unverified) | 1.34 |
| 169 | `cfg_d8eb` | timeframe=5min, band_lookback=10, band_mult=0.75, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 350/267/0 | 617 | 23.7% | 4.3% | 0.99 | -3.2% | 148 | 1.31 | 16.6% | 287.4 | 7/7 | 1.00 | 0.75 | 0.24 | 4 | 13.6% | 0.43 | 0.52 | 17.4% | 11.2% | 18.6% | 20.4%/16.7% | 3.1 (interpolated) | pass | 0.527 (unverified) | 1.35 |
| 170 | `cfg_1afa` | timeframe=5min, band_lookback=10, band_mult=2.0, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 145/214/0 | 359 | 24.8% | 4.5% | 0.87 | -4.1% | 285 | 1.34 | 12.9% | 167.6 | 8/8 | 1.00 | 0.80 | 0.07 | 4 | 15.5% | 0.35 | 0.52 | 21.3% | 17.5% | 15.1% | 23.2%/17.4% | 4.8 (interpolated) | pass | 0.421 (unverified) | 0.93 |
| 171 | `cfg_4fb7` | timeframe=5min, band_lookback=10, band_mult=2.0, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 145/214/0 | 359 | 24.8% | 4.5% | 0.87 | -4.1% | 285 | 1.34 | 12.9% | 167.6 | 7/7 | 1.00 | 0.86 | 0.01 | 4 | 15.5% | 0.35 | 0.52 | 21.3% | 17.5% | 15.1% | 23.6%/18.3% | 4.8 (interpolated) | pass | 0.421 (unverified) | 0.93 |
| 172 | `cfg_ad07` | timeframe=5min, band_lookback=30, band_mult=2.0, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 146/193/0 | 339 | 27.2% | 4.9% | 0.88 | -4.8% | 397 | 1.36 | 12.3% | 158.6 | 6/6 | 1.00 | 0.65 | 0.23 | 5 | 14.1% | 0.44 | 0.52 | 22.9% | 20.4% | 16.6% | 26.5%/20.6% | 5.1 (interpolated) | pass | 0.428 (unverified) | 1.02 |
| 173 | `cfg_e144` | timeframe=5min, band_lookback=30, band_mult=2.0, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 146/193/0 | 339 | 27.2% | 4.9% | 0.88 | -4.8% | 397 | 1.36 | 12.3% | 158.6 | 7/7 | 1.00 | 0.75 | 0.13 | 5 | 14.1% | 0.44 | 0.52 | 22.9% | 20.4% | 16.6% | 25.7%/20.7% | 5.1 (interpolated) | pass | 0.428 (unverified) | 1.02 |
| 174 | `cfg_0211` | timeframe=5min, band_lookback=7, band_mult=1.5, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=band, direction=long, stop_atr_multiple=none | 239/109/0 | 348 | 12.6% | 2.4% | 0.81 | -4.2% | 525 | 1.38 | 7.7% | 159.6 | 7/7 | 1.00 | 0.69 | 0.13 | 4 | 6.3% | 0.48 | 0.72 | 9.2% | 6.2% | 7.8% | 11.4%/7.7% | 3.0 (interpolated) | pass | 0.364 (unverified) | 0.56 |
| 175 | `cfg_60df` | timeframe=5min, band_lookback=7, band_mult=1.5, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=band, direction=long, stop_atr_multiple=none | 239/109/0 | 348 | 12.6% | 2.4% | 0.81 | -4.2% | 525 | 1.38 | 7.7% | 159.6 | 8/8 | 1.00 | 0.65 | 0.16 | 4 | 6.3% | 0.48 | 0.72 | 9.2% | 6.2% | 7.8% | 11.6%/8.6% | 3.0 (interpolated) | pass | 0.364 (unverified) | 0.56 |
| 176 | `cfg_21d1` | timeframe=5min, band_lookback=30, band_mult=0.75, check_minutes=15, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 742/490/0 | 1232 | 36.8% | 6.5% | 0.79 | -8.7% | 379 | 1.14 | 34.2% | 575.5 | 6/6 | 1.00 | 0.87 | -0.08 | 4 | 21.3% | 0.35 | 0.49 | 25.8% | 11.6% | 25.6% | 34.1%/26.0% | 2.6 (interpolated) | pass | 0.357 (unverified) | 1.22 |
| 177 | `cfg_c6ae` | timeframe=15min, band_lookback=7, band_mult=1.0, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 353/210/0 | 563 | 18.0% | 3.4% | 0.82 | -3.9% | 240 | 1.27 | 14.6% | 259.4 | 7/7 | 1.00 | 0.75 | 0.07 | 5 | 8.5% | 0.53 | 0.61 | 12.1% | 7.0% | 6.8% | 15.7%/11.8% | 2.7 (interpolated) | pass | 0.376 (unverified) | 1.31 |
| 178 | `cfg_c9a9` | timeframe=15min, band_lookback=7, band_mult=1.0, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 353/210/0 | 563 | 18.0% | 3.4% | 0.82 | -3.9% | 240 | 1.27 | 14.6% | 259.4 | 8/8 | 1.00 | 0.71 | 0.12 | 5 | 8.5% | 0.53 | 0.61 | 12.1% | 7.0% | 6.8% | 16.2%/11.5% | 2.7 (interpolated) | pass | 0.376 (unverified) | 1.31 |
| 179 | `cfg_37b9` | timeframe=5min, band_lookback=30, band_mult=1.0, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 1049/335/0 | 1384 | 42.1% | 7.3% | 0.92 | -11.3% | 538 | 1.22 | 25.1% | 645.0 | 6/6 | 1.00 | 0.75 | 0.18 | 4 | 13.6% | 0.68 | 0.46 | 25.5% | 9.2% | 41.1% | 38.1%/26.7% | 2.4 (interpolated) | pass | 0.471 (unverified) | 1.32 |
| 180 | `cfg_74c7` | timeframe=5min, band_lookback=20, band_mult=1.0, check_minutes=60, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=short, stop_atr_multiple=none | 189/160/0 | 349 | 27.0% | 4.9% | 0.84 | -6.0% | 302 | 1.30 | 10.7% | 163.8 | 7/7 | 1.00 | 0.74 | 0.10 | 3 | 12.3% | 0.49 | 0.59 | 22.4% | 19.1% | 21.8% | 24.4%/16.8% | 5.1 (interpolated) | pass | 0.391 (unverified) | 0.98 |
| 181 | `cfg_76b6` | timeframe=5min, band_lookback=20, band_mult=1.0, check_minutes=60, first_entry_minutes=30, anchor=open_prev_close, trail=band_vwap, direction=short, stop_atr_multiple=none | 189/160/0 | 349 | 27.0% | 4.9% | 0.84 | -6.0% | 302 | 1.30 | 10.7% | 163.8 | 8/8 | 1.00 | 0.74 | 0.10 | 3 | 12.3% | 0.49 | 0.59 | 22.4% | 19.1% | 21.8% | 23.1%/16.9% | 5.1 (interpolated) | pass | 0.391 (unverified) | 0.98 |
| 182 | `cfg_9083` | timeframe=15min, band_lookback=30, band_mult=0.75, check_minutes=15, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 741/491/0 | 1232 | 35.9% | 6.3% | 0.79 | -9.2% | 322 | 1.14 | 35.5% | 574.9 | 6/6 | 1.00 | 0.88 | -0.09 | 4 | 21.2% | 0.34 | 0.50 | 25.8% | 11.2% | 26.6% | 34.3%/25.8% | 2.6 (interpolated) | pass | 0.349 (unverified) | 1.24 |
| 183 | `cfg_af6d` | timeframe=15min, band_lookback=10, band_mult=1.0, check_minutes=30, first_entry_minutes=30, anchor=open, trail=vwap, direction=long, stop_atr_multiple=none | 346/336/0 | 682 | 25.5% | 4.7% | 0.77 | -6.0% | 210 | 1.21 | 23.9% | 317.5 | 9/9 | 1.00 | 0.70 | 0.08 | 5 | 17.0% | 0.32 | 0.62 | 17.7% | 11.8% | 14.0% | 24.0%/16.6% | 3.0 (interpolated) | pass | 0.334 (unverified) | 0.98 |
| 184 | `cfg_e848` | timeframe=15min, band_lookback=10, band_mult=1.0, check_minutes=30, first_entry_minutes=15, anchor=open, trail=vwap, direction=long, stop_atr_multiple=none | 346/336/0 | 682 | 25.5% | 4.7% | 0.77 | -6.0% | 210 | 1.21 | 23.9% | 317.5 | 8/8 | 1.00 | 0.72 | 0.05 | 5 | 17.0% | 0.32 | 0.62 | 17.7% | 11.8% | 14.0% | 24.6%/17.9% | 3.0 (interpolated) | pass | 0.334 (unverified) | 0.98 |
| 185 | `cfg_1c1e` | timeframe=15min, band_lookback=20, band_mult=0.75, check_minutes=15, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 479/243/0 | 722 | 19.8% | 3.7% | 0.83 | -5.4% | 456 | 1.26 | 17.0% | 335.6 | 6/6 | 1.00 | 0.84 | -0.01 | 4 | 8.0% | 0.59 | 0.69 | 11.7% | 5.5% | 8.4% | 17.3%/11.5% | 2.5 (interpolated) | pass | 0.382 (unverified) | 1.31 |
| 186 | `cfg_5e74` | timeframe=5min, band_lookback=20, band_mult=0.75, check_minutes=15, first_entry_minutes=30, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 587/242/0 | 829 | 21.2% | 3.9% | 0.80 | -5.1% | 262 | 1.24 | 17.3% | 386.3 | 7/7 | 1.00 | 0.84 | -0.04 | 4 | 9.8% | 0.50 | 0.68 | 10.9% | 3.4% | 11.0% | 19.0%/13.5% | 2.3 (interpolated) | pass | 0.361 (unverified) | 1.22 |
| 187 | `cfg_80b6` | timeframe=15min, band_lookback=14, band_mult=1.25, check_minutes=30, first_entry_minutes=30, anchor=open, trail=vwap, direction=long, stop_atr_multiple=none | 240/272/0 | 512 | 24.8% | 4.5% | 0.84 | -6.2% | 261 | 1.27 | 18.7% | 238.2 | 9/9 | 1.00 | 0.62 | 0.22 | 4 | 15.8% | 0.31 | 0.65 | 19.8% | 15.5% | 12.3% | 22.4%/16.7% | 3.7 (interpolated) | pass | 0.389 (unverified) | 0.86 |
| 188 | `cfg_f856` | timeframe=15min, band_lookback=14, band_mult=1.25, check_minutes=30, first_entry_minutes=15, anchor=open, trail=vwap, direction=long, stop_atr_multiple=none | 240/272/0 | 512 | 24.8% | 4.5% | 0.84 | -6.2% | 261 | 1.27 | 18.7% | 238.2 | 8/8 | 1.00 | 0.64 | 0.20 | 4 | 15.8% | 0.31 | 0.65 | 19.8% | 15.5% | 12.3% | 23.5%/17.5% | 3.7 (interpolated) | pass | 0.389 (unverified) | 0.86 |
| 189 | `cfg_77ed` | timeframe=5min, band_lookback=30, band_mult=1.5, check_minutes=60, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 242/207/0 | 449 | 24.7% | 4.5% | 0.80 | -9.6% | 536 | 1.28 | 13.8% | 206.2 | 6/6 | 0.83 | 0.77 | 0.04 | 4 | 6.5% | 0.74 | 0.58 | 18.0% | 14.2% | 11.0% | 19.9%/14.2% | 4.0 (interpolated) | pass | 0.361 (unverified) | 1.69 |
| 190 | `cfg_dbfe` | timeframe=5min, band_lookback=30, band_mult=1.5, check_minutes=60, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 242/207/0 | 449 | 24.7% | 4.5% | 0.80 | -9.6% | 536 | 1.28 | 13.8% | 206.2 | 6/6 | 0.83 | 0.72 | 0.08 | 4 | 6.5% | 0.74 | 0.58 | 18.0% | 14.2% | 11.0% | 21.7%/15.2% | 4.0 (interpolated) | pass | 0.361 (unverified) | 1.69 |
| 191 | `cfg_5a5f` | timeframe=5min, band_lookback=7, band_mult=2.0, check_minutes=60, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 158/306/0 | 464 | 24.9% | 4.5% | 0.76 | -15.3% | 544 | 1.25 | 17.3% | 213.6 | 5/5 | 1.00 | 0.76 | 0.00 | 4 | 7.7% | 0.69 | 0.56 | 18.7% | 14.6% | 22.9% | 22.1%/15.4% | 3.7 (interpolated) | pass | 0.327 (unverified) | 0.95 |
| 192 | `cfg_9225` | timeframe=5min, band_lookback=7, band_mult=2.0, check_minutes=60, first_entry_minutes=15, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 158/306/0 | 464 | 24.9% | 4.5% | 0.76 | -15.3% | 544 | 1.25 | 17.3% | 213.6 | 5/5 | 1.00 | 0.68 | 0.08 | 4 | 7.7% | 0.69 | 0.56 | 18.7% | 14.6% | 22.9% | 23.5%/15.4% | 3.7 (interpolated) | pass | 0.327 (unverified) | 0.95 |
| 193 | `cfg_1fc2` | timeframe=5min, band_lookback=30, band_mult=1.5, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 378/284/0 | 662 | 35.3% | 6.2% | 0.88 | -10.6% | 547 | 1.24 | 20.5% | 310.3 | 6/6 | 1.00 | 0.88 | 0.00 | 5 | 17.2% | 0.51 | 0.47 | 27.6% | 22.8% | 29.8% | 33.2%/26.3% | 3.8 (interpolated) | pass | 0.433 (unverified) | 1.30 |
| 194 | `cfg_56ed` | timeframe=15min, band_lookback=14, band_mult=0.75, check_minutes=15, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 505/249/0 | 754 | 19.9% | 3.7% | 0.83 | -5.1% | 346 | 1.25 | 17.3% | 349.4 | 6/6 | 1.00 | 0.74 | 0.10 | 3 | 7.2% | 0.64 | 0.67 | 11.7% | 4.7% | 12.3% | 16.8%/12.8% | 2.4 (interpolated) | pass | 0.385 (unverified) | 1.14 |
| 195 | `cfg_44da` | timeframe=15min, band_lookback=10, band_mult=1.25, check_minutes=30, first_entry_minutes=30, anchor=open, trail=vwap, direction=long, stop_atr_multiple=none | 257/274/0 | 531 | 22.1% | 4.1% | 0.75 | -7.7% | 271 | 1.24 | 19.2% | 246.5 | 9/9 | 1.00 | 0.68 | 0.07 | 5 | 15.1% | 0.30 | 0.68 | 17.7% | 12.9% | 8.7% | 20.5%/16.2% | 3.5 (interpolated) | pass | 0.313 (unverified) | 1.08 |
| 196 | `cfg_50cd` | timeframe=15min, band_lookback=10, band_mult=1.25, check_minutes=30, first_entry_minutes=15, anchor=open, trail=vwap, direction=long, stop_atr_multiple=none | 257/274/0 | 531 | 22.1% | 4.1% | 0.75 | -7.7% | 271 | 1.24 | 19.2% | 246.5 | 8/8 | 1.00 | 0.74 | 0.01 | 5 | 15.1% | 0.30 | 0.68 | 17.7% | 12.9% | 8.7% | 20.2%/15.8% | 3.5 (interpolated) | pass | 0.313 (unverified) | 1.08 |
| 197 | `cfg_2c1f` | timeframe=15min, band_lookback=30, band_mult=1.5, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=both, stop_atr_multiple=none | 382/285/0 | 667 | 33.7% | 6.0% | 0.84 | -10.2% | 547 | 1.23 | 21.1% | 312.4 | 6/6 | 1.00 | 0.87 | -0.02 | 5 | 16.0% | 0.52 | 0.50 | 25.9% | 20.5% | 27.5% | 30.8%/24.7% | 3.7 (interpolated) | pass | 0.400 (unverified) | 1.22 |
| 198 | `cfg_81a1` | timeframe=5min, band_lookback=14, band_mult=1.5, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=vwap, direction=short, stop_atr_multiple=none | 150/146/0 | 296 | 22.6% | 4.2% | 0.75 | -5.2% | 291 | 1.30 | 9.7% | 139.0 | 8/8 | 1.00 | 0.65 | 0.10 | 4 | 9.7% | 0.52 | 0.67 | 19.1% | 15.8% | 15.3% | 21.4%/15.2% | 5.1 (interpolated) | pass | 0.319 (unverified) | 1.01 |
| 199 | `cfg_e392` | timeframe=5min, band_lookback=14, band_mult=1.5, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=vwap, direction=short, stop_atr_multiple=none | 150/146/0 | 296 | 22.6% | 4.2% | 0.75 | -5.2% | 291 | 1.30 | 9.7% | 139.0 | 9/9 | 1.00 | 0.65 | 0.10 | 4 | 9.7% | 0.52 | 0.67 | 19.1% | 15.8% | 15.3% | 21.5%/15.1% | 5.1 (interpolated) | pass | 0.319 (unverified) | 1.01 |
| 200 | `cfg_15d9` | timeframe=15min, band_lookback=30, band_mult=2.0, check_minutes=15, first_entry_minutes=60, anchor=open, trail=vwap, direction=both, stop_atr_multiple=none | 238/264/0 | 502 | 28.1% | 5.1% | 0.77 | -6.5% | 354 | 1.23 | 16.9% | 233.9 | 5/5 | 1.00 | 0.67 | 0.09 | 5 | 13.9% | 0.50 | 0.57 | 22.9% | 18.0% | 7.4% | 25.7%/19.9% | 4.0 (interpolated) | pass | 0.334 (unverified) | 0.62 |
| 201 | `cfg_f8ac` | timeframe=5min, band_lookback=30, band_mult=1.0, check_minutes=30, first_entry_minutes=60, anchor=open, trail=band_vwap, direction=short, stop_atr_multiple=none | 416/198/0 | 614 | 25.3% | 4.6% | 0.76 | -5.6% | 371 | 1.21 | 14.3% | 287.9 | 7/7 | 1.00 | 0.63 | 0.13 | 3 | 13.8% | 0.44 | 0.66 | 16.9% | 12.3% | 15.2% | 23.0%/14.9% | 3.1 (interpolated) | pass | 0.322 (unverified) | 0.93 |
| 202 | `cfg_8ab4` | timeframe=15min, band_lookback=14, band_mult=1.0, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 269/197/0 | 466 | 15.4% | 2.9% | 0.79 | -4.9% | 598 | 1.28 | 13.0% | 214.9 | 8/8 | 1.00 | 0.73 | 0.06 | 3 | 6.8% | 0.56 | 0.67 | 11.2% | 7.2% | 7.1% | 13.8%/9.3% | 3.0 (interpolated) | pass | 0.347 (unverified) | 0.94 |
| 203 | `cfg_4c9a` | timeframe=5min, band_lookback=14, band_mult=1.0, check_minutes=30, first_entry_minutes=60, anchor=open_prev_close, trail=band_vwap, direction=long, stop_atr_multiple=none | 269/197/0 | 466 | 15.4% | 2.9% | 0.79 | -4.9% | 598 | 1.28 | 12.5% | 214.9 | 8/8 | 1.00 | 0.73 | 0.06 | 3 | 6.8% | 0.56 | 0.67 | 11.2% | 7.2% | 10.2% | 13.7%/9.3% | 3.0 (interpolated) | pass | 0.347 (unverified) | 0.92 |
| 204 | `cfg_1ae6` | timeframe=5min, band_lookback=7, band_mult=1.5, check_minutes=30, first_entry_minutes=15, anchor=open, trail=band, direction=long, stop_atr_multiple=none | 367/162/0 | 529 | 18.6% | 3.5% | 0.84 | -4.3% | 395 | 1.32 | 12.0% | 244.3 | 7/7 | 1.00 | 0.54 | 0.30 | 5 | 12.9% | 0.30 | 0.73 | 13.0% | 7.8% | 15.4% | 17.3%/11.5% | 3.0 (interpolated) | pass | 0.385 (unverified) | 0.80 |
| 205 | `cfg_86ff` | timeframe=15min, band_lookback=7, band_mult=1.5, check_minutes=30, first_entry_minutes=15, anchor=open, trail=band, direction=long, stop_atr_multiple=none | 367/162/0 | 529 | 18.6% | 3.5% | 0.84 | -4.3% | 395 | 1.32 | 12.8% | 244.3 | 7/7 | 1.00 | 0.54 | 0.30 | 5 | 12.9% | 0.30 | 0.73 | 13.0% | 7.8% | 10.1% | 15.8%/13.1% | 3.0 (interpolated) | pass | 0.385 (unverified) | 0.80 |
| 206 | `cfg_a223` | timeframe=15min, band_lookback=20, band_mult=0.75, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=band, direction=long, stop_atr_multiple=none | 629/268/0 | 897 | 25.4% | 4.6% | 0.85 | -6.0% | 303 | 1.25 | 20.3% | 416.4 | 6/6 | 1.00 | 0.80 | 0.05 | 3 | 11.6% | 0.49 | 0.61 | 14.1% | 7.5% | 6.2% | 23.3%/15.7% | 2.5 (interpolated) | pass | 0.398 (unverified) | 1.22 |
| 207 | `cfg_5908` | timeframe=5min, band_lookback=20, band_mult=0.75, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=band, direction=long, stop_atr_multiple=none | 629/268/0 | 897 | 23.3% | 4.3% | 0.81 | -6.2% | 329 | 1.23 | 19.0% | 413.4 | 6/6 | 1.00 | 0.80 | 0.01 | 3 | 10.8% | 0.53 | 0.61 | 13.6% | 6.6% | 17.6% | 21.6%/15.4% | 2.4 (interpolated) | pass | 0.365 (unverified) | 1.20 |
| 208 | `cfg_5b47` | timeframe=5min, band_lookback=30, band_mult=1.0, check_minutes=15, first_entry_minutes=15, anchor=open_prev_close, trail=band, direction=both, stop_atr_multiple=none | 1012/372/0 | 1384 | 33.8% | 6.0% | 0.76 | -11.9% | 538 | 1.17 | 26.9% | 639.6 | 6/6 | 1.00 | 0.63 | 0.13 | 4 | 11.1% | 0.67 | 0.57 | 20.9% | 6.8% | 32.1% | 30.7%/22.6% | 2.3 (interpolated) | pass | 0.330 (unverified) | 1.28 |
| 209 | `cfg_a464` | timeframe=15min, band_lookback=10, band_mult=1.5, check_minutes=30, first_entry_minutes=30, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 478/220/0 | 698 | 25.5% | 4.7% | 0.78 | -9.5% | 683 | 1.23 | 16.6% | 325.8 | 9/9 | 1.00 | 0.67 | 0.12 | 5 | 12.4% | 0.46 | 0.58 | 17.4% | 11.8% | 8.0% | 21.7%/16.5% | 2.9 (interpolated) | pass | 0.347 (unverified) | 1.18 |
| 210 | `cfg_dfe8` | timeframe=15min, band_lookback=10, band_mult=1.5, check_minutes=30, first_entry_minutes=15, anchor=open_prev_close, trail=band_vwap, direction=both, stop_atr_multiple=none | 478/220/0 | 698 | 25.5% | 4.7% | 0.78 | -9.5% | 683 | 1.23 | 16.6% | 325.8 | 8/8 | 1.00 | 0.64 | 0.14 | 5 | 12.4% | 0.46 | 0.58 | 17.4% | 11.8% | 8.0% | 21.9%/16.2% | 2.9 (interpolated) | pass | 0.347 (unverified) | 1.18 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 3.5% / 0.83 / 84 | 3.5% / 1.25 / 67 | 5.9% / 0.91 / 78 | 7.6% / 2.74 / 84 | 11.5% / 1.87 / 86 |
| 2 | 3.5% / 0.83 / 84 | 3.5% / 1.25 / 67 | 5.9% / 0.91 / 78 | 7.6% / 2.74 / 84 | 11.5% / 1.87 / 86 |
| 3 | 2.4% / 0.55 / 71 | 2.2% / 0.82 / 62 | 6.7% / 1.36 / 64 | 6.5% / 2.45 / 76 | 10.7% / 1.96 / 72 |
| 4 | 4.9% / 1.20 / 73 | 1.6% / 0.69 / 60 | 5.0% / 0.84 / 67 | 4.5% / 1.88 / 75 | 12.0% / 2.15 / 76 |
| 5 | 3.5% / 0.86 / 62 | 2.2% / 0.85 / 56 | 7.6% / 1.37 / 54 | 6.7% / 2.58 / 71 | 9.7% / 1.74 / 64 |
| 6 | 4.9% / 1.18 / 74 | 1.7% / 0.71 / 60 | 5.0% / 0.84 / 67 | 4.5% / 1.88 / 75 | 11.8% / 2.09 / 76 |
| 7 | 1.8% / 0.41 / 89 | 0.4% / 0.16 / 86 | 7.8% / 1.32 / 82 | 9.7% / 3.33 / 92 | 13.5% / 2.13 / 88 |
| 8 | 1.8% / 0.41 / 89 | 0.4% / 0.16 / 86 | 7.8% / 1.32 / 82 | 9.7% / 3.33 / 92 | 13.5% / 2.13 / 88 |
| 9 | 2.4% / 0.64 / 80 | 4.3% / 1.40 / 69 | 4.3% / 0.76 / 71 | 8.5% / 2.72 / 80 | 9.7% / 1.74 / 82 |
| 10 | 15.0% / 1.73 / 184 | -1.7% / -0.40 / 167 | 17.2% / 1.55 / 161 | 10.4% / 2.12 / 171 | 17.4% / 1.73 / 201 |
| 11 | 15.0% / 1.73 / 184 | -1.7% / -0.40 / 167 | 17.2% / 1.55 / 161 | 10.4% / 2.12 / 171 | 17.4% / 1.73 / 201 |
| 12 | 1.5% / 0.39 / 80 | 4.5% / 1.43 / 68 | 4.0% / 0.72 / 70 | 9.0% / 2.87 / 80 | 10.3% / 1.85 / 82 |
| 13 | 13.1% / 1.62 / 139 | 0.4% / 0.12 / 129 | 12.4% / 1.24 / 119 | 4.5% / 1.10 / 144 | 10.2% / 1.13 / 158 |
| 14 | 13.1% / 1.62 / 139 | 0.4% / 0.12 / 129 | 12.4% / 1.24 / 119 | 4.5% / 1.10 / 144 | 10.2% / 1.13 / 158 |
| 15 | 19.1% / 2.20 / 163 | -1.7% / -0.40 / 144 | 13.3% / 1.34 / 147 | 7.5% / 1.72 / 154 | 21.0% / 2.25 / 176 |
| 16 | 15.7% / 1.98 / 121 | -1.5% / -0.39 / 116 | 8.9% / 1.00 / 112 | 2.1% / 0.56 / 129 | 15.2% / 1.88 / 134 |
| 17 | 3.1% / 0.66 / 101 | 2.1% / 0.74 / 85 | 6.8% / 1.16 / 92 | 8.9% / 3.09 / 94 | 11.2% / 1.74 / 101 |
| 18 | 18.9% / 2.21 / 164 | -3.6% / -0.86 / 157 | 15.1% / 1.57 / 149 | 3.4% / 0.81 / 162 | 16.1% / 1.76 / 183 |
| 19 | 15.8% / 1.99 / 121 | -1.3% / -0.34 / 115 | 8.9% / 0.99 / 112 | 1.6% / 0.43 / 130 | 15.2% / 1.89 / 136 |
| 20 | 5.5% / 1.23 / 92 | 0.4% / 0.17 / 83 | 9.5% / 1.35 / 92 | 5.5% / 1.99 / 93 | 13.0% / 2.03 / 97 |
| 21 | 4.0% / 0.88 / 103 | 0.9% / 0.32 / 97 | 10.3% / 1.40 / 104 | 10.4% / 3.26 / 103 | 10.1% / 1.43 / 108 |
| 22 | 4.0% / 0.88 / 103 | 0.9% / 0.32 / 97 | 10.3% / 1.40 / 104 | 10.4% / 3.26 / 103 | 10.1% / 1.43 / 108 |
| 23 | 5.4% / 1.19 / 80 | 1.0% / 0.40 / 67 | 5.4% / 0.88 / 83 | 4.5% / 1.75 / 81 | 11.2% / 1.89 / 91 |
| 24 | 2.6% / 0.55 / 101 | 2.0% / 0.71 / 85 | 6.6% / 1.14 / 92 | 8.6% / 2.99 / 95 | 11.7% / 1.81 / 100 |
| 25 | 4.7% / 1.03 / 101 | 0.7% / 0.30 / 90 | 4.6% / 0.71 / 97 | 6.1% / 2.22 / 93 | 8.1% / 1.26 / 104 |
| 26 | 2.0% / 0.50 / 95 | 2.3% / 0.73 / 83 | 3.4% / 0.67 / 83 | 5.9% / 2.16 / 89 | 8.9% / 1.46 / 94 |
| 27 | 12.9% / 1.91 / 82 | -0.7% / -0.20 / 78 | 4.6% / 0.64 / 77 | -0.8% / -0.20 / 82 | 10.5% / 1.68 / 73 |
| 28 | 12.9% / 1.91 / 82 | -0.7% / -0.20 / 78 | 4.6% / 0.64 / 77 | -0.8% / -0.20 / 82 | 10.5% / 1.68 / 73 |
| 29 | 1.5% / 0.32 / 142 | 4.0% / 1.07 / 124 | 6.8% / 0.89 / 131 | 13.9% / 3.69 / 116 | 9.8% / 1.25 / 145 |
| 30 | 12.6% / 1.57 / 156 | -1.1% / -0.27 / 134 | 12.1% / 1.28 / 130 | -0.2% / -0.02 / 152 | 11.6% / 1.29 / 165 |
| 31 | 12.6% / 1.57 / 156 | -1.1% / -0.27 / 134 | 12.1% / 1.28 / 130 | -0.2% / -0.02 / 152 | 11.6% / 1.29 / 165 |
| 32 | 1.3% / 0.35 / 85 | 4.3% / 1.44 / 73 | -0.1% / 0.01 / 72 | 5.8% / 1.79 / 85 | 11.0% / 1.87 / 85 |
| 33 | 1.7% / 0.34 / 128 | 0.5% / 0.18 / 115 | 8.7% / 1.22 / 120 | 11.0% / 3.39 / 111 | 10.4% / 1.40 / 129 |
| 34 | 1.3% / 0.33 / 148 | 5.7% / 1.88 / 107 | 1.0% / 0.17 / 149 | 8.7% / 2.83 / 138 | 13.5% / 2.28 / 143 |
| 35 | 0.3% / 0.09 / 85 | 4.4% / 1.48 / 72 | 0.5% / 0.12 / 71 | 6.3% / 1.93 / 85 | 11.0% / 1.87 / 84 |
| 36 | 4.6% / 1.02 / 102 | 0.8% / 0.31 / 90 | 4.3% / 0.66 / 98 | 6.1% / 2.22 / 93 | 7.7% / 1.21 / 104 |
| 37 | 1.1% / 0.27 / 95 | 2.5% / 0.82 / 82 | 2.8% / 0.54 / 83 | 6.2% / 2.27 / 89 | 9.1% / 1.49 / 94 |
| 38 | 18.0% / 2.05 / 205 | -3.0% / -0.68 / 181 | 10.7% / 1.08 / 188 | 5.0% / 1.10 / 184 | 8.4% / 0.84 / 227 |
| 39 | 1.6% / 0.41 / 148 | 5.8% / 1.93 / 107 | 0.9% / 0.16 / 149 | 8.3% / 2.69 / 138 | 13.5% / 2.28 / 143 |
| 40 | 15.1% / 1.71 / 145 | 0.0% / 0.02 / 120 | 2.6% / 0.32 / 126 | 2.5% / 0.63 / 133 | 21.8% / 2.36 / 148 |
| 41 | 15.1% / 1.71 / 145 | 0.0% / 0.02 / 120 | 2.6% / 0.32 / 126 | 2.5% / 0.63 / 133 | 21.8% / 2.36 / 148 |
| 42 | 17.6% / 2.03 / 218 | -2.1% / -0.45 / 194 | 13.6% / 1.37 / 204 | 2.1% / 0.43 / 197 | 12.8% / 1.29 / 240 |
| 43 | 21.1% / 2.66 / 103 | 0.1% / 0.04 / 95 | -0.5% / -0.01 / 107 | -0.3% / -0.05 / 119 | 13.1% / 1.86 / 110 |
| 44 | -0.1% / 0.01 / 152 | 3.5% / 0.96 / 131 | 4.6% / 0.65 / 148 | 15.2% / 3.99 / 121 | 7.0% / 0.98 / 146 |
| 45 | 16.1% / 1.85 / 200 | -1.9% / -0.43 / 186 | 11.1% / 1.05 / 196 | 7.3% / 1.71 / 186 | 12.8% / 1.24 / 239 |
| 46 | 3.4% / 0.80 / 62 | 0.5% / 0.24 / 56 | 4.1% / 0.92 / 57 | 3.0% / 1.33 / 69 | 11.6% / 2.18 / 63 |
| 47 | 27.0% / 2.97 / 198 | -2.8% / -0.61 / 184 | 9.7% / 0.89 / 202 | -0.2% / -0.02 / 192 | 12.9% / 1.23 / 214 |
| 48 | 21.1% / 2.66 / 103 | 0.3% / 0.10 / 94 | -0.2% / 0.02 / 107 | -0.7% / -0.16 / 119 | 12.2% / 1.74 / 112 |
| 49 | 18.3% / 2.15 / 175 | -2.1% / -0.50 / 159 | 6.7% / 0.73 / 175 | 3.0% / 0.78 / 162 | 13.2% / 1.37 / 205 |
| 50 | 10.7% / 1.42 / 133 | 0.3% / 0.11 / 113 | 6.4% / 0.70 / 124 | 1.9% / 0.46 / 131 | 18.2% / 1.96 / 152 |
| 51 | 10.7% / 1.42 / 133 | 0.3% / 0.11 / 113 | 6.4% / 0.70 / 124 | 1.9% / 0.46 / 131 | 18.2% / 1.96 / 152 |
| 52 | 0.7% / 0.16 / 154 | 3.2% / 0.89 / 131 | 4.6% / 0.62 / 148 | 14.8% / 3.90 / 121 | 6.2% / 0.87 / 147 |
| 53 | 4.8% / 1.04 / 73 | -0.9% / -0.39 / 72 | 2.6% / 0.59 / 72 | 4.3% / 1.88 / 75 | 10.4% / 1.88 / 75 |
| 54 | 4.9% / 1.09 / 69 | -0.5% / -0.21 / 65 | 1.0% / 0.24 / 68 | 2.5% / 1.13 / 75 | 9.2% / 1.84 / 67 |
| 55 | 28.0% / 3.26 / 148 | -0.1% / -0.00 / 145 | 5.1% / 0.52 / 163 | 0.1% / 0.04 / 162 | 9.8% / 1.08 / 171 |
| 56 | 13.5% / 1.74 / 116 | 2.9% / 0.87 / 101 | 5.8% / 0.66 / 97 | 2.2% / 0.59 / 107 | 10.9% / 1.39 / 120 |
| 57 | 13.5% / 1.74 / 116 | 2.9% / 0.87 / 101 | 5.8% / 0.66 / 97 | 2.2% / 0.59 / 107 | 10.9% / 1.39 / 120 |
| 58 | 3.0% / 0.71 / 62 | 0.6% / 0.26 / 56 | 3.9% / 0.86 / 57 | 2.9% / 1.28 / 69 | 12.0% / 2.25 / 63 |
| 59 | 18.6% / 2.22 / 153 | -3.0% / -0.69 / 148 | 9.6% / 0.99 / 141 | 2.2% / 0.51 / 151 | 9.8% / 1.06 / 173 |
| 60 | 18.6% / 2.22 / 153 | -3.0% / -0.69 / 148 | 9.6% / 0.99 / 141 | 2.2% / 0.51 / 151 | 9.8% / 1.06 / 173 |
| 61 | 1.6% / 0.38 / 179 | 5.1% / 1.44 / 153 | 1.6% / 0.25 / 181 | 12.4% / 3.73 / 148 | 11.3% / 1.56 / 180 |
| 62 | 20.6% / 2.05 / 266 | -1.1% / -0.20 / 249 | 8.1% / 0.71 / 271 | 8.7% / 1.51 / 248 | 14.5% / 1.21 / 298 |
| 63 | 20.6% / 2.05 / 266 | -1.1% / -0.20 / 249 | 8.1% / 0.71 / 271 | 8.7% / 1.51 / 248 | 14.5% / 1.21 / 298 |
| 64 | 27.3% / 3.16 / 149 | 0.3% / 0.10 / 144 | 5.2% / 0.52 / 164 | -0.4% / -0.05 / 163 | 8.9% / 0.98 / 174 |
| 65 | 1.9% / 0.43 / 179 | 4.9% / 1.39 / 153 | 1.2% / 0.19 / 182 | 12.0% / 3.59 / 148 | 11.0% / 1.53 / 180 |
| 66 | 26.3% / 2.88 / 199 | -2.7% / -0.59 / 185 | 10.0% / 0.93 / 203 | -0.9% / -0.16 / 191 | 12.2% / 1.16 / 217 |
| 67 | 17.1% / 2.06 / 233 | -0.5% / -0.09 / 189 | 5.8% / 0.61 / 217 | 4.2% / 0.96 / 202 | 6.2% / 0.70 / 259 |
| 68 | 23.3% / 2.48 / 257 | -2.7% / -0.53 / 229 | 13.1% / 1.13 / 247 | 0.4% / 0.11 / 228 | 14.1% / 1.26 / 265 |
| 69 | 14.7% / 1.74 / 261 | -0.7% / -0.14 / 220 | 10.5% / 0.99 / 237 | 9.6% / 1.91 / 221 | 2.1% / 0.25 / 294 |
| 70 | 14.7% / 1.74 / 261 | -0.7% / -0.14 / 220 | 10.5% / 0.99 / 237 | 9.6% / 1.91 / 221 | 2.1% / 0.25 / 294 |
| 71 | 17.1% / 2.06 / 233 | -0.4% / -0.08 / 189 | 5.9% / 0.62 / 217 | 4.2% / 0.96 / 202 | 5.7% / 0.64 / 259 |
| 72 | 23.3% / 2.45 / 241 | -2.9% / -0.59 / 231 | 12.8% / 1.10 / 243 | 1.1% / 0.25 / 227 | 10.3% / 0.95 / 263 |
| 73 | 3.8% / 0.89 / 117 | 1.6% / 0.72 / 84 | 0.6% / 0.14 / 124 | 3.2% / 1.48 / 116 | 13.4% / 2.50 / 115 |
| 74 | 18.6% / 1.93 / 304 | -3.2% / -0.58 / 267 | 11.3% / 0.93 / 290 | 4.5% / 0.84 / 262 | 13.0% / 1.06 / 317 |
| 75 | 0.4% / 0.15 / 67 | 3.1% / 1.09 / 61 | 1.9% / 0.47 / 54 | 3.9% / 1.68 / 67 | 7.0% / 1.46 / 62 |
| 76 | 2.7% / 0.57 / 120 | -0.0% / 0.00 / 114 | 11.7% / 1.70 / 116 | 8.9% / 2.57 / 119 | 7.6% / 1.07 / 116 |
| 77 | 2.7% / 0.57 / 120 | -0.0% / 0.00 / 114 | 11.7% / 1.70 / 116 | 8.9% / 2.57 / 119 | 7.6% / 1.07 / 116 |
| 78 | 2.5% / 0.57 / 133 | 1.0% / 0.35 / 118 | 3.1% / 0.49 / 132 | 10.5% / 3.42 / 117 | 6.1% / 0.93 / 134 |
| 79 | 2.5% / 0.57 / 133 | 1.0% / 0.35 / 118 | 3.1% / 0.49 / 132 | 10.5% / 3.42 / 117 | 6.1% / 0.93 / 134 |
| 80 | 26.3% / 3.02 / 182 | -0.5% / -0.09 / 171 | 9.1% / 0.88 / 191 | 2.0% / 0.45 / 169 | 12.1% / 1.17 / 206 |
| 81 | 4.9% / 1.05 / 142 | 1.4% / 0.55 / 116 | 1.6% / 0.29 / 152 | 5.3% / 2.27 / 120 | 11.4% / 1.72 / 147 |
| 82 | 21.9% / 2.51 / 174 | -1.6% / -0.34 / 167 | 3.5% / 0.36 / 185 | 0.1% / 0.05 / 169 | 11.1% / 1.08 / 202 |
| 83 | 23.6% / 2.47 / 307 | -4.9% / -0.93 / 293 | 9.8% / 0.83 / 303 | 4.5% / 0.81 / 272 | 11.7% / 0.98 / 328 |
| 84 | 19.3% / 1.99 / 277 | -0.8% / -0.12 / 261 | 10.1% / 0.85 / 272 | 6.2% / 1.12 / 255 | 9.4% / 0.80 / 302 |
| 85 | 19.3% / 1.99 / 277 | -0.8% / -0.12 / 261 | 10.1% / 0.85 / 272 | 6.2% / 1.12 / 255 | 9.4% / 0.80 / 302 |
| 86 | 3.6% / 0.83 / 117 | 1.5% / 0.69 / 84 | 0.5% / 0.12 / 124 | 3.3% / 1.51 / 116 | 13.6% / 2.53 / 115 |
| 87 | 19.5% / 2.12 / 262 | -4.3% / -0.82 / 242 | 10.7% / 0.92 / 260 | 1.9% / 0.41 / 237 | 10.2% / 0.94 / 287 |
| 88 | 22.6% / 2.58 / 175 | -1.6% / -0.34 / 167 | 3.4% / 0.36 / 185 | 0.1% / 0.03 / 169 | 10.3% / 1.01 / 204 |
| 89 | -0.5% / -0.13 / 67 | 3.0% / 1.11 / 60 | 0.9% / 0.23 / 55 | 4.3% / 1.86 / 68 | 6.4% / 1.36 / 62 |
| 90 | 4.8% / 1.02 / 142 | 1.3% / 0.52 / 116 | 1.4% / 0.27 / 152 | 5.3% / 2.27 / 120 | 11.4% / 1.72 / 147 |
| 91 | 22.3% / 2.67 / 174 | 2.6% / 0.62 / 162 | 3.5% / 0.38 / 182 | 1.4% / 0.31 / 180 | 10.1% / 1.00 / 203 |
| 92 | 22.3% / 2.67 / 174 | 2.6% / 0.62 / 162 | 3.5% / 0.38 / 182 | 1.4% / 0.31 / 180 | 10.1% / 1.00 / 203 |
| 93 | 4.9% / 1.14 / 118 | 0.7% / 0.29 / 101 | 1.0% / 0.19 / 120 | 5.5% / 2.06 / 104 | 8.3% / 1.42 / 120 |
| 94 | 4.9% / 1.14 / 118 | 0.7% / 0.27 / 101 | 1.0% / 0.19 / 120 | 5.4% / 2.04 / 104 | 8.4% / 1.43 / 120 |
| 95 | 25.6% / 2.95 / 183 | -0.5% / -0.09 / 172 | 9.4% / 0.91 / 191 | 1.3% / 0.31 / 169 | 11.5% / 1.11 / 207 |
| 96 | 20.6% / 2.10 / 215 | -0.8% / -0.14 / 188 | 2.0% / 0.23 / 212 | 2.0% / 0.46 / 192 | 15.7% / 1.39 / 232 |
| 97 | 20.6% / 2.10 / 215 | -0.8% / -0.14 / 188 | 2.0% / 0.23 / 212 | 2.0% / 0.46 / 192 | 15.7% / 1.39 / 232 |
| 98 | 14.1% / 1.85 / 116 | -0.9% / -0.24 / 103 | -0.0% / 0.04 / 104 | 1.0% / 0.29 / 117 | 14.3% / 1.90 / 121 |
| 99 | 14.1% / 1.85 / 116 | -0.9% / -0.24 / 103 | -0.0% / 0.04 / 104 | 1.0% / 0.29 / 117 | 14.3% / 1.90 / 121 |
| 100 | 3.7% / 0.85 / 115 | 1.3% / 0.44 / 106 | 5.9% / 0.77 / 125 | 9.9% / 3.27 / 115 | 5.8% / 0.91 / 127 |
| 101 | 3.7% / 0.85 / 115 | 1.3% / 0.44 / 106 | 5.9% / 0.77 / 125 | 9.9% / 3.27 / 115 | 5.8% / 0.91 / 127 |
| 102 | 11.1% / 1.54 / 233 | -0.8% / -0.16 / 205 | 15.8% / 1.39 / 226 | 9.4% / 1.86 / 217 | 4.5% / 0.48 / 287 |
| 103 | 11.1% / 1.54 / 233 | -0.8% / -0.16 / 205 | 15.8% / 1.39 / 226 | 9.4% / 1.86 / 217 | 4.5% / 0.48 / 287 |
| 104 | 21.1% / 2.61 / 125 | -2.6% / -0.73 / 114 | 10.5% / 1.24 / 115 | -5.2% / -1.34 / 110 | 8.8% / 1.29 / 130 |
| 105 | 19.6% / 2.11 / 262 | -4.5% / -0.87 / 241 | 8.1% / 0.70 / 260 | 2.1% / 0.44 / 237 | 12.2% / 1.10 / 283 |
| 106 | 21.0% / 2.59 / 125 | -2.6% / -0.76 / 115 | 10.2% / 1.21 / 114 | -5.2% / -1.34 / 111 | 9.4% / 1.36 / 127 |
| 107 | 11.8% / 1.44 / 176 | 1.9% / 0.49 / 164 | 0.5% / 0.10 / 168 | 3.4% / 0.74 / 171 | 16.6% / 1.70 / 193 |
| 108 | 8.0% / 1.36 / 153 | 1.0% / 0.28 / 146 | 7.0% / 0.75 / 140 | 4.4% / 1.11 / 156 | 10.1% / 1.25 / 181 |
| 109 | 8.0% / 1.36 / 153 | 1.0% / 0.28 / 146 | 7.0% / 0.75 / 140 | 4.4% / 1.11 / 156 | 10.1% / 1.25 / 181 |
| 110 | 23.4% / 2.64 / 176 | -2.5% / -0.64 / 170 | 0.2% / 0.07 / 198 | -1.2% / -0.23 / 188 | 13.8% / 1.44 / 195 |
| 111 | 23.9% / 2.70 / 176 | -2.2% / -0.57 / 168 | 0.2% / 0.08 / 200 | -1.2% / -0.24 / 190 | 13.0% / 1.37 / 198 |
| 112 | 15.7% / 1.76 / 228 | -1.4% / -0.31 / 210 | -2.1% / -0.12 / 236 | 7.7% / 1.53 / 207 | 15.1% / 1.39 / 257 |
| 113 | 21.0% / 2.62 / 156 | 2.8% / 0.71 / 132 | -0.0% / 0.05 / 165 | 2.2% / 0.53 / 145 | 9.4% / 1.04 / 161 |
| 114 | 11.6% / 1.43 / 148 | 0.9% / 0.27 / 121 | 6.4% / 0.75 / 131 | -1.2% / -0.27 / 140 | 14.0% / 1.84 / 145 |
| 115 | 15.7% / 1.85 / 189 | -0.9% / -0.17 / 169 | 3.8% / 0.34 / 199 | 1.6% / 0.35 / 174 | 15.2% / 1.34 / 223 |
| 116 | 15.7% / 1.85 / 189 | -0.9% / -0.17 / 169 | 3.8% / 0.34 / 199 | 1.6% / 0.35 / 174 | 15.2% / 1.34 / 223 |
| 117 | 15.2% / 2.07 / 93 | -3.6% / -1.05 / 88 | 8.4% / 1.00 / 90 | -2.0% / -0.46 / 79 | 6.3% / 0.95 / 100 |
| 118 | 17.2% / 1.98 / 215 | 0.1% / 0.04 / 202 | -1.7% / -0.09 / 226 | 8.3% / 1.76 / 198 | 13.9% / 1.28 / 254 |
| 119 | 20.4% / 2.53 / 157 | 3.1% / 0.79 / 131 | -0.1% / 0.04 / 166 | 1.7% / 0.41 / 145 | 9.6% / 1.05 / 163 |
| 120 | 11.4% / 1.68 / 147 | 3.7% / 0.84 / 131 | 5.7% / 0.56 / 158 | 4.5% / 1.02 / 147 | 7.4% / 0.75 / 181 |
| 121 | 11.4% / 1.68 / 147 | 3.7% / 0.84 / 131 | 5.7% / 0.56 / 158 | 4.5% / 1.02 / 147 | 7.4% / 0.75 / 181 |
| 122 | 13.0% / 1.53 / 195 | -0.6% / -0.13 / 178 | 3.9% / 0.42 / 178 | 0.9% / 0.22 / 182 | 16.6% / 1.62 / 207 |
| 123 | 10.2% / 1.67 / 121 | -2.5% / -0.86 / 108 | 7.4% / 1.04 / 118 | -1.5% / -0.42 / 101 | 10.3% / 1.77 / 130 |
| 124 | 4.0% / 0.91 / 143 | 0.5% / 0.18 / 136 | 2.4% / 0.45 / 144 | 8.1% / 2.42 / 141 | 6.9% / 1.04 / 144 |
| 125 | 4.0% / 0.91 / 143 | 0.5% / 0.18 / 136 | 2.4% / 0.45 / 144 | 8.1% / 2.42 / 141 | 6.9% / 1.04 / 144 |
| 126 | 11.1% / 1.36 / 147 | 0.8% / 0.24 / 123 | 5.7% / 0.67 / 131 | -1.6% / -0.38 / 141 | 13.9% / 1.80 / 142 |
| 127 | 10.2% / 1.67 / 121 | -2.5% / -0.86 / 108 | 7.4% / 1.04 / 118 | -0.9% / -0.24 / 101 | 10.1% / 1.75 / 130 |
| 128 | 15.8% / 2.39 / 60 | -1.4% / -0.48 / 62 | -5.4% / -0.74 / 63 | 1.6% / 0.52 / 69 | 11.3% / 2.09 / 53 |
| 129 | 15.8% / 2.39 / 60 | -1.4% / -0.48 / 62 | -5.4% / -0.74 / 63 | 1.6% / 0.52 / 69 | 11.3% / 2.09 / 53 |
| 130 | 13.8% / 1.80 / 84 | -2.8% / -0.85 / 76 | 5.4% / 0.65 / 80 | -3.5% / -0.91 / 74 | 11.9% / 1.74 / 88 |
| 131 | 13.8% / 1.80 / 84 | -2.8% / -0.85 / 76 | 5.4% / 0.65 / 80 | -3.5% / -0.91 / 74 | 11.9% / 1.74 / 88 |
| 132 | 15.1% / 2.05 / 94 | -3.4% / -1.00 / 87 | 8.8% / 1.04 / 90 | -2.3% / -0.55 / 79 | 6.4% / 0.98 / 102 |
| 133 | 13.3% / 1.67 / 144 | -1.2% / -0.31 / 129 | 4.6% / 0.53 / 138 | -1.4% / -0.32 / 150 | 13.9% / 1.67 / 160 |
| 134 | 8.2% / 1.10 / 160 | 3.2% / 0.89 / 145 | 1.5% / 0.21 / 142 | 2.0% / 0.51 / 176 | 12.5% / 1.51 / 189 |
| 135 | 8.2% / 1.10 / 160 | 3.2% / 0.89 / 145 | 1.5% / 0.21 / 142 | 2.0% / 0.51 / 176 | 12.5% / 1.51 / 189 |
| 136 | 19.8% / 2.37 / 147 | -3.1% / -0.84 / 136 | 7.3% / 0.80 / 134 | -3.4% / -0.83 / 122 | 9.3% / 1.20 / 149 |
| 137 | 18.3% / 2.37 / 110 | -2.5% / -0.77 / 94 | 11.7% / 1.43 / 94 | -3.6% / -0.93 / 95 | 6.9% / 1.07 / 107 |
| 138 | 8.6% / 1.46 / 137 | -1.2% / -0.33 / 132 | 3.2% / 0.40 / 131 | 1.3% / 0.37 / 141 | 15.3% / 2.04 / 160 |
| 139 | 13.4% / 1.67 / 144 | -1.5% / -0.37 / 131 | 3.6% / 0.44 / 137 | -1.5% / -0.35 / 151 | 14.2% / 1.70 / 157 |
| 140 | 19.6% / 2.37 / 147 | -3.0% / -0.80 / 136 | 8.2% / 0.89 / 134 | -3.9% / -0.94 / 122 | 8.7% / 1.14 / 153 |
| 141 | 7.3% / 1.09 / 111 | -0.7% / -0.18 / 111 | -0.5% / -0.02 / 109 | 1.4% / 0.42 / 118 | 18.9% / 2.57 / 129 |
| 142 | 20.7% / 2.19 / 204 | -1.5% / -0.34 / 176 | 1.7% / 0.22 / 188 | 2.2% / 0.50 / 185 | 14.4% / 1.53 / 229 |
| 143 | 20.7% / 2.19 / 204 | -1.5% / -0.34 / 176 | 1.7% / 0.22 / 188 | 2.2% / 0.50 / 185 | 14.4% / 1.53 / 229 |
| 144 | 18.1% / 2.07 / 245 | -1.9% / -0.42 / 213 | 5.8% / 0.66 / 237 | 1.9% / 0.40 / 225 | 9.3% / 1.05 / 285 |
| 145 | 18.2% / 2.08 / 245 | -1.9% / -0.42 / 213 | 5.9% / 0.67 / 237 | 1.7% / 0.37 / 225 | 8.7% / 1.00 / 285 |
| 146 | 18.0% / 2.22 / 137 | -3.2% / -0.89 / 117 | 10.1% / 1.15 / 116 | -2.8% / -0.67 / 113 | 7.3% / 0.99 / 135 |
| 147 | 2.5% / 0.61 / 82 | -1.4% / -0.55 / 69 | 7.4% / 1.14 / 93 | 0.3% / 0.12 / 71 | 12.5% / 2.56 / 83 |
| 148 | 27.1% / 2.96 / 178 | -1.3% / -0.27 / 164 | -0.7% / -0.00 / 186 | 0.6% / 0.15 / 174 | 14.1% / 1.42 / 188 |
| 149 | 27.1% / 2.96 / 178 | -1.3% / -0.27 / 164 | -0.7% / -0.00 / 186 | 0.6% / 0.15 / 174 | 14.1% / 1.42 / 188 |
| 150 | 1.4% / 0.40 / 72 | 2.3% / 0.82 / 67 | -2.9% / -0.66 / 70 | 5.4% / 2.25 / 83 | 8.3% / 1.67 / 71 |
| 151 | 2.3% / 0.59 / 110 | 1.3% / 0.50 / 82 | 2.3% / 0.46 / 93 | 5.8% / 2.22 / 107 | 9.4% / 1.66 / 98 |
| 152 | 2.3% / 0.59 / 110 | 1.3% / 0.50 / 82 | 2.3% / 0.46 / 93 | 5.8% / 2.22 / 107 | 9.4% / 1.66 / 98 |
| 153 | 2.5% / 0.61 / 82 | -1.4% / -0.55 / 69 | 7.4% / 1.14 / 93 | 0.3% / 0.12 / 71 | 12.5% / 2.56 / 83 |
| 154 | 9.7% / 1.40 / 227 | -0.5% / -0.12 / 185 | 3.8% / 0.42 / 225 | -0.6% / -0.14 / 220 | 21.3% / 2.55 / 265 |
| 155 | 0.9% / 0.24 / 54 | 1.8% / 0.78 / 50 | 0.1% / 0.04 / 57 | 5.4% / 2.34 / 67 | 6.4% / 1.36 / 51 |
| 156 | 0.9% / 0.24 / 54 | 1.8% / 0.78 / 50 | 0.1% / 0.04 / 57 | 5.4% / 2.34 / 67 | 6.4% / 1.36 / 51 |
| 157 | 21.2% / 2.78 / 89 | -1.2% / -0.37 / 78 | 0.5% / 0.11 / 86 | -1.4% / -0.34 / 75 | 5.3% / 0.85 / 96 |
| 158 | 21.2% / 2.78 / 89 | -1.2% / -0.37 / 78 | 0.5% / 0.11 / 86 | -1.4% / -0.34 / 75 | 5.3% / 0.85 / 96 |
| 159 | 0.4% / 0.10 / 156 | 2.9% / 1.10 / 109 | -3.8% / -0.54 / 135 | 7.6% / 2.93 / 126 | 11.6% / 2.02 / 133 |
| 160 | 16.8% / 2.21 / 104 | -2.8% / -0.84 / 89 | 8.5% / 1.01 / 85 | -2.1% / -0.52 / 87 | 5.6% / 1.04 / 105 |
| 161 | 16.8% / 2.21 / 104 | -2.8% / -0.84 / 89 | 8.5% / 1.01 / 85 | -2.1% / -0.52 / 87 | 5.6% / 1.04 / 105 |
| 162 | 6.1% / 0.91 / 264 | 0.6% / 0.17 / 215 | 9.1% / 0.84 / 256 | 1.6% / 0.40 / 253 | 19.3% / 2.10 / 303 |
| 163 | 19.0% / 2.34 / 121 | -2.0% / -0.54 / 111 | -3.0% / -0.27 / 119 | 0.8% / 0.23 / 125 | 13.2% / 1.72 / 133 |
| 164 | 19.0% / 2.34 / 121 | -2.0% / -0.54 / 111 | -3.0% / -0.27 / 119 | 0.8% / 0.23 / 125 | 13.2% / 1.72 / 133 |
| 165 | 1.4% / 0.30 / 182 | 1.2% / 0.42 / 151 | -0.0% / 0.03 / 187 | 10.4% / 3.51 / 143 | 8.2% / 1.28 / 166 |
| 166 | 4.8% / 0.94 / 62 | 1.3% / 0.49 / 54 | 6.9% / 0.90 / 65 | 0.7% / 0.22 / 55 | 7.9% / 1.35 / 78 |
| 167 | 4.8% / 0.94 / 62 | 1.3% / 0.49 / 54 | 6.9% / 0.90 / 65 | 0.7% / 0.22 / 55 | 7.9% / 1.35 / 78 |
| 168 | 5.9% / 1.36 / 125 | -1.0% / -0.35 / 117 | 3.9% / 0.73 / 130 | 4.3% / 1.52 / 122 | 9.1% / 1.50 / 123 |
| 169 | 5.9% / 1.36 / 125 | -1.0% / -0.37 / 117 | 3.9% / 0.73 / 130 | 4.4% / 1.53 / 122 | 8.9% / 1.48 / 123 |
| 170 | 7.6% / 1.18 / 74 | -0.0% / 0.00 / 71 | 8.1% / 1.15 / 69 | 0.3% / 0.11 / 78 | 7.1% / 1.28 / 67 |
| 171 | 7.6% / 1.18 / 74 | -0.0% / 0.00 / 71 | 8.1% / 1.15 / 69 | 0.3% / 0.11 / 78 | 7.1% / 1.28 / 67 |
| 172 | 2.7% / 0.56 / 71 | 0.4% / 0.15 / 68 | 11.5% / 1.31 / 64 | 0.8% / 0.29 / 67 | 9.7% / 1.45 / 69 |
| 173 | 2.7% / 0.56 / 71 | 0.4% / 0.15 / 68 | 11.5% / 1.31 / 64 | 0.8% / 0.29 / 67 | 9.7% / 1.45 / 69 |
| 174 | 1.1% / 0.31 / 74 | 1.9% / 0.97 / 60 | -1.2% / -0.36 / 72 | 6.0% / 3.08 / 80 | 4.5% / 1.21 / 62 |
| 175 | 1.1% / 0.31 / 74 | 1.9% / 0.97 / 60 | -1.2% / -0.36 / 72 | 6.0% / 3.08 / 80 | 4.5% / 1.21 / 62 |
| 176 | 12.8% / 1.59 / 247 | -4.7% / -0.98 / 229 | 9.3% / 0.89 / 236 | 9.3% / 1.89 / 223 | 6.4% / 0.61 / 297 |
| 177 | 2.6% / 0.62 / 112 | 0.6% / 0.24 / 103 | 0.2% / 0.06 / 109 | 5.0% / 1.67 / 122 | 8.7% / 1.63 / 117 |
| 178 | 2.6% / 0.62 / 112 | 0.6% / 0.24 / 103 | 0.2% / 0.06 / 109 | 5.0% / 1.67 / 122 | 8.7% / 1.63 / 117 |
| 179 | 6.4% / 0.96 / 284 | 3.5% / 0.85 / 233 | -0.3% / 0.04 / 278 | 3.5% / 0.80 / 268 | 25.1% / 2.53 / 321 |
| 180 | 13.1% / 1.68 / 72 | -1.1% / -0.35 / 65 | 4.2% / 0.56 / 63 | -1.2% / -0.33 / 64 | 10.3% / 1.65 / 85 |
| 181 | 13.1% / 1.68 / 72 | -1.1% / -0.35 / 65 | 4.2% / 0.56 / 63 | -1.2% / -0.33 / 64 | 10.3% / 1.65 / 85 |
| 182 | 12.2% / 1.54 / 249 | -4.1% / -0.86 / 228 | 10.0% / 0.97 / 235 | 9.6% / 1.95 / 221 | 4.8% / 0.48 / 299 |
| 183 | 4.2% / 0.77 / 131 | 3.2% / 0.87 / 125 | 5.1% / 0.69 / 141 | 7.3% / 2.08 / 132 | 3.5% / 0.45 / 153 |
| 184 | 4.2% / 0.77 / 131 | 3.2% / 0.87 / 125 | 5.1% / 0.69 / 141 | 7.3% / 2.08 / 132 | 3.5% / 0.45 / 153 |
| 185 | 4.9% / 1.05 / 156 | 0.3% / 0.14 / 129 | -2.0% / -0.32 / 165 | 4.7% / 1.89 / 125 | 10.9% / 1.79 / 147 |
| 186 | 1.1% / 0.25 / 182 | 1.1% / 0.40 / 151 | -0.1% / 0.02 / 187 | 10.4% / 3.51 / 143 | 7.4% / 1.21 / 166 |
| 187 | 7.7% / 1.57 / 95 | 6.0% / 1.85 / 87 | -0.5% / -0.04 / 107 | 5.1% / 1.68 / 103 | 4.5% / 0.60 / 120 |
| 188 | 7.7% / 1.57 / 95 | 6.0% / 1.85 / 87 | -0.5% / -0.04 / 107 | 5.1% / 1.68 / 103 | 4.5% / 0.60 / 120 |
| 189 | 6.4% / 1.10 / 83 | 0.2% / 0.09 / 79 | -1.7% / -0.16 / 84 | 1.5% / 0.46 / 101 | 17.2% / 2.63 / 102 |
| 190 | 6.4% / 1.10 / 83 | 0.2% / 0.09 / 79 | -1.7% / -0.16 / 84 | 1.5% / 0.46 / 101 | 17.2% / 2.63 / 102 |
| 191 | 13.9% / 1.94 / 91 | 1.4% / 0.43 / 90 | -10.6% / -1.30 / 107 | 4.4% / 1.13 / 93 | 15.9% / 2.26 / 83 |
| 192 | 13.9% / 1.94 / 91 | 1.4% / 0.43 / 90 | -10.6% / -1.30 / 107 | 4.4% / 1.13 / 93 | 15.9% / 2.26 / 83 |
| 193 | 9.3% / 1.52 / 123 | 1.9% / 0.50 / 119 | 4.7% / 0.47 / 130 | 0.5% / 0.15 / 140 | 15.4% / 1.76 / 150 |
| 194 | 5.1% / 1.09 / 154 | -1.1% / -0.39 / 146 | -1.4% / -0.22 / 167 | 4.6% / 1.86 / 131 | 11.8% / 2.00 / 156 |
| 195 | 5.5% / 1.08 / 102 | 2.6% / 0.78 / 92 | 1.4% / 0.24 / 111 | 6.0% / 2.08 / 109 | 4.9% / 0.65 / 117 |
| 196 | 5.5% / 1.08 / 102 | 2.6% / 0.78 / 92 | 1.4% / 0.24 / 111 | 6.0% / 2.08 / 109 | 4.9% / 0.65 / 117 |
| 197 | 11.1% / 1.73 / 123 | 1.8% / 0.49 / 120 | 2.3% / 0.26 / 132 | 0.3% / 0.10 / 140 | 15.2% / 1.76 / 152 |
| 198 | 11.8% / 1.74 / 65 | 0.6% / 0.27 / 55 | 4.8% / 0.63 / 54 | -1.4% / -0.42 / 51 | 5.5% / 0.92 / 71 |
| 199 | 11.8% / 1.74 / 65 | 0.6% / 0.27 / 55 | 4.8% / 0.63 / 54 | -1.4% / -0.42 / 51 | 5.5% / 0.92 / 71 |
| 200 | 8.5% / 1.40 / 101 | 0.5% / 0.17 / 86 | 2.5% / 0.30 / 116 | 1.8% / 0.54 / 98 | 12.4% / 1.48 / 101 |
| 201 | 10.2% / 1.73 / 124 | -1.4% / -0.41 / 122 | 10.2% / 1.13 / 114 | -1.7% / -0.37 / 105 | 6.6% / 0.93 / 149 |
| 202 | 4.5% / 1.09 / 91 | -0.2% / -0.06 / 81 | -2.4% / -0.56 / 90 | 4.9% / 2.03 / 103 | 8.1% / 1.62 / 101 |
| 203 | 4.5% / 1.09 / 91 | -0.2% / -0.06 / 81 | -2.4% / -0.56 / 90 | 4.9% / 2.03 / 103 | 8.1% / 1.62 / 101 |
| 204 | 4.6% / 0.97 / 103 | 3.9% / 1.66 / 88 | 0.8% / 0.20 / 116 | 5.0% / 2.03 / 110 | 3.1% / 0.54 / 112 |
| 205 | 4.6% / 0.97 / 103 | 3.9% / 1.66 / 88 | 0.8% / 0.20 / 116 | 5.0% / 2.03 / 110 | 3.1% / 0.54 / 112 |
| 206 | -1.8% / -0.40 / 200 | 3.4% / 1.00 / 164 | -0.7% / -0.05 / 202 | 12.3% / 3.38 / 151 | 10.8% / 1.50 / 180 |
| 207 | -1.8% / -0.40 / 200 | 3.4% / 1.00 / 164 | -2.2% / -0.28 / 202 | 11.7% / 3.30 / 151 | 11.2% / 1.56 / 180 |
| 208 | 6.8% / 0.96 / 284 | 4.6% / 1.06 / 233 | -5.0% / -0.35 / 278 | 4.7% / 0.99 / 268 | 20.4% / 2.09 / 321 |
| 209 | 11.7% / 1.62 / 153 | 2.4% / 0.78 / 115 | 1.2% / 0.19 / 133 | 1.4% / 0.38 / 146 | 6.9% / 1.11 / 151 |
| 210 | 11.7% / 1.62 / 153 | 2.4% / 0.78 / 115 | 1.2% / 0.19 / 133 | 1.4% / 0.38 / 146 | 6.9% / 1.11 / 151 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_920a` | 22 | 0.83 | 0.82/0.91 | 0.69/0.79 |
| 1 | `cfg_03aa` | 100 | 0.81 | 0.83/0.92 | 0.64/0.77 |
| 2 | `cfg_d527` | 24 | 0.82 | 0.61/0.69 | 0.50/0.62 |
| 3 | `cfg_44da` | 3 | 0.83 | 0.87/0.94 | 0.82/0.91 |
| 4 | `cfg_1392` | 26 | 0.88 | 0.85/0.88 | 0.69/0.81 |
| 5 | `cfg_00ec` | 36 | 0.87 | 0.88/0.91 | 0.75/0.80 |
| 6 | `cfg_ead3` | 74 | 0.81 | 0.80/0.86 | 0.64/0.76 |
| 7 | `cfg_a97e` | 50 | 0.82 | 0.83/0.90 | 0.66/0.79 |
| 8 | `cfg_36e3` | 30 | 0.82 | 0.79/0.91 | 0.72/0.80 |
| 9 | `cfg_ad07` | 5 | 0.94 | 0.94/1.00 | 0.87/0.96 |
| 10 | `cfg_2731` | 28 | 0.81 | 0.88/0.93 | 0.72/0.82 |
| 11 | `cfg_1275` | 24 | 0.81 | 0.76/0.88 | 0.65/0.75 |
| 12 | `cfg_0211` | 8 | 1.00 | 1.00/1.00 | 0.95/0.97 |
| 13 | `cfg_c8b3` | 12 | 0.88 | 0.91/0.94 | 0.78/0.81 |
| 14 | `cfg_7de1` | 12 | 0.81 | 0.87/0.90 | 0.68/0.75 |
| 15 | `cfg_6e82` | 26 | 0.86 | 0.72/0.83 | 0.60/0.70 |
| 16 | `cfg_0fab` | 54 | 0.82 | 0.84/0.90 | 0.60/0.71 |
| 17 | `cfg_44b5` | 25 | 0.83 | 0.71/0.91 | 0.58/0.80 |
| 18 | `cfg_29ae` | 57 | 0.86 | 0.90/0.91 | 0.74/0.80 |
| 19 | `cfg_b701` | 34 | 0.81 | 0.80/0.89 | 0.60/0.76 |
| 20 | `cfg_1c1e` | 4 | 0.92 | 0.91/0.91 | 0.86/0.89 |
| 21 | `cfg_a4ab` | 16 | 0.82 | 0.81/0.86 | 0.65/0.75 |
| 22 | `cfg_2be2` | 8 | 0.90 | 0.91/0.92 | 0.77/0.80 |
| 23 | `cfg_0c8b` | 24 | 0.95 | 0.94/0.96 | 0.82/0.89 |
| 24 | `cfg_b835` | 30 | 0.81 | 0.82/0.91 | 0.66/0.77 |
| 25 | `cfg_123a` | 8 | 0.84 | 0.87/0.90 | 0.64/0.72 |
| 26 | `cfg_c3c6` | 16 | 0.87 | 0.87/0.87 | 0.80/0.83 |
| 27 | `cfg_4163` | 13 | 0.83 | 0.77/0.80 | 0.62/0.70 |
| 28 | `cfg_05b9` | 8 | 0.82 | 0.90/0.95 | 0.88/0.93 |
| 29 | `cfg_b907` | 16 | 0.90 | 0.88/0.88 | 0.80/0.84 |
| 30 | `cfg_0617` | 8 | 0.97 | 0.99/0.99 | 0.92/0.95 |
| 31 | `cfg_8310` | 18 | 0.85 | 0.89/0.90 | 0.77/0.81 |
| 32 | `cfg_38af` | 8 | 0.85 | 0.92/0.94 | 0.83/0.90 |
| 33 | `cfg_6b22` | 8 | 0.82 | 0.88/0.91 | 0.78/0.85 |
| 34 | `cfg_10c0` | 6 | 0.88 | 0.87/0.91 | 0.71/0.78 |
| 35 | `cfg_3763` | 18 | 0.81 | 0.77/0.83 | 0.58/0.73 |
| 36 | `cfg_097c` | 7 | 0.85 | 0.89/0.91 | 0.79/0.85 |
| 37 | `cfg_0998` | 34 | 0.80 | 0.79/0.85 | 0.61/0.72 |
| 38 | `cfg_264d` | 18 | 0.87 | 0.87/0.97 | 0.70/0.85 |
| 39 | `cfg_0a38` | 4 | 0.96 | 0.98/0.98 | 0.92/0.95 |
| 40 | `cfg_daac` | 17 | 0.81 | 0.85/0.92 | 0.79/0.85 |
| 41 | `cfg_809c` | 12 | 0.85 | 0.82/0.91 | 0.65/0.83 |
| 42 | `cfg_11f5` | 18 | 0.85 | 0.83/0.88 | 0.66/0.72 |
| 43 | `cfg_0c6c` | 8 | 0.86 | 0.83/0.87 | 0.68/0.74 |
| 44 | `cfg_9d1b` | 16 | 0.83 | 0.85/0.89 | 0.62/0.74 |
| 45 | `cfg_a464` | 4 | 1.00 | 1.00/1.00 | 0.97/0.97 |
| 46 | `cfg_32ed` | 11 | 0.87 | 0.81/0.88 | 0.60/0.76 |
| 47 | `cfg_0ec4` | 16 | 0.82 | 0.90/0.90 | 0.71/0.74 |
| 48 | `cfg_7f54` | 6 | 0.86 | 0.73/0.77 | 0.42/0.47 |
| 49 | `cfg_11bf` | 13 | 0.85 | 0.74/0.82 | 0.63/0.74 |
| 50 | `cfg_5237` | 5 | 0.83 | 0.87/0.91 | 0.78/0.83 |
| 51 | `cfg_eb5c` | 7 | 0.83 | 0.93/0.94 | 0.82/0.86 |
| 52 | `cfg_2219` | 18 | 0.83 | 0.84/0.92 | 0.66/0.82 |
| 53 | `cfg_9f62` | 7 | 0.84 | 0.77/0.77 | 0.66/0.67 |
| 54 | `cfg_86c5` | 4 | 0.93 | 0.95/0.96 | 0.92/0.95 |
| 55 | `cfg_e8c9` | 11 | 0.81 | 0.89/0.89 | 0.70/0.78 |
| 56 | `cfg_c745` | 8 | 0.86 | 0.76/0.80 | 0.67/0.71 |
| 57 | `cfg_c6ab` | 18 | 0.81 | 0.81/0.87 | 0.70/0.76 |
| 58 | `cfg_8963` | 10 | 0.85 | 0.90/0.93 | 0.76/0.83 |
| 59 | `cfg_6881` | 21 | 0.82 | 0.79/0.87 | 0.60/0.73 |
| 60 | `cfg_de0e` | 5 | 0.82 | 0.81/0.88 | 0.65/0.79 |
| 61 | `cfg_21d1` | 5 | 0.81 | 0.85/0.93 | 0.74/0.90 |
| 62 | `cfg_8e9c` | 20 | 0.84 | 0.85/0.88 | 0.63/0.73 |
| 63 | `cfg_5a5f` | 13 | 0.81 | 0.58/0.77 | 0.47/0.64 |
| 64 | `cfg_c665` | 8 | 0.89 | 0.88/0.91 | 0.82/0.89 |
| 65 | `cfg_14b4` | 12 | 0.84 | 0.88/0.91 | 0.70/0.79 |
| 66 | `cfg_35e4` | 18 | 0.86 | 0.92/0.93 | 0.80/0.85 |
| 67 | `cfg_15d9` | 1 | n/a | n/a/n/a | n/a/n/a |
| 68 | `cfg_ccc2` | 18 | 0.82 | 0.84/0.91 | 0.75/0.82 |
| 69 | `cfg_239e` | 8 | 0.88 | 0.88/0.93 | 0.74/0.80 |
| 70 | `cfg_1ae8` | 12 | 0.86 | 0.92/0.94 | 0.84/0.87 |
| 71 | `cfg_fb79` | 4 | 0.87 | 0.94/0.95 | 0.93/0.95 |
| 72 | `cfg_9cf2` | 6 | 0.83 | 0.93/1.00 | 0.89/0.96 |
| 73 | `cfg_1ae6` | 6 | 0.89 | 0.93/1.00 | 0.88/0.97 |
| 74 | `cfg_1afa` | 5 | 0.93 | 0.94/1.00 | 0.88/0.95 |
| 75 | `cfg_1b3c` | 4 | 0.92 | 0.94/0.94 | 0.91/0.95 |
| 76 | `cfg_74c7` | 22 | 0.81 | 0.81/0.98 | 0.67/0.92 |
| 77 | `cfg_954a` | 10 | 0.85 | 0.88/0.92 | 0.80/0.87 |
| 78 | `cfg_81a1` | 8 | 0.94 | 0.87/0.93 | 0.79/0.84 |
| 79 | `cfg_1fc2` | 4 | 0.88 | 0.85/0.85 | 0.70/0.72 |
| 80 | `cfg_7721` | 8 | 0.93 | 0.97/0.97 | 0.94/0.96 |
| 81 | `cfg_80c8` | 6 | 0.82 | 0.84/0.91 | 0.64/0.75 |
| 82 | `cfg_52c3` | 14 | 0.81 | 0.69/0.77 | 0.53/0.62 |
| 83 | `cfg_c6ae` | 16 | 0.80 | 0.88/0.91 | 0.73/0.81 |
| 84 | `cfg_5c08` | 12 | 0.88 | 0.81/0.82 | 0.66/0.67 |
| 85 | `cfg_40f8` | 15 | 0.92 | 0.93/0.94 | 0.76/0.83 |
| 86 | `cfg_27d3` | 12 | 0.87 | 0.93/0.95 | 0.81/0.86 |
| 87 | `cfg_8934` | 21 | 0.86 | 0.88/0.96 | 0.82/0.90 |
| 88 | `cfg_88cc` | 10 | 0.88 | 0.87/0.91 | 0.67/0.72 |
| 89 | `cfg_b8a1` | 13 | 0.81 | 0.90/0.93 | 0.70/0.74 |
| 90 | `cfg_b096` | 15 | 0.83 | 0.86/0.87 | 0.71/0.78 |
| 91 | `cfg_af6d` | 7 | 0.85 | 0.90/0.96 | 0.83/0.93 |
| 92 | `cfg_c3e9` | 7 | 0.81 | 0.83/0.91 | 0.79/0.87 |
| 93 | `cfg_37b9` | 3 | 0.93 | 0.96/0.97 | 0.93/0.94 |
| 94 | `cfg_3e6a` | 12 | 0.89 | 0.94/0.95 | 0.86/0.90 |
| 95 | `cfg_4d73` | 12 | 0.87 | 0.95/0.99 | 0.86/0.93 |
| 96 | `cfg_67fd` | 5 | 0.86 | 0.91/1.00 | 0.84/0.95 |
| 97 | `cfg_411e` | 1 | n/a | n/a/n/a | n/a/n/a |
| 98 | `cfg_80b6` | 4 | 0.99 | 1.00/1.00 | 0.95/0.95 |
| 99 | `cfg_ee1c` | 9 | 0.81 | 0.76/0.84 | 0.58/0.73 |
| 100 | `cfg_a9e0` | 6 | 0.86 | 0.89/0.92 | 0.78/0.81 |
| 101 | `cfg_8ab4` | 2 | 1.00 | 1.00/1.00 | 0.97/0.97 |
| 102 | `cfg_b39f` | 6 | 0.92 | 0.93/0.94 | 0.87/0.91 |
| 103 | `cfg_77ed` | 6 | 1.00 | 1.00/1.00 | 0.96/0.96 |
| 104 | `cfg_a223` | 2 | 0.99 | 0.99/0.99 | 0.97/0.97 |
| 105 | `cfg_9ec5` | 1 | n/a | n/a/n/a | n/a/n/a |
| 106 | `cfg_f8ac` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 4.113e-04 over 8100 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 382.0, participation ratio 4.3, 95%-variance components 65 (rank bound T = 1259); raw grid 8100; raw + known prior 486702
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

- Noise sigma at bar k = mean of |close - session open| / raw session open at the SAME time of day (bar-open minute, NY) over the previous band_lookback sessions that have a bar at that time; today's own move is never included, so sigma is known before the session starts.
- Bands: upper = hi + band_mult x sigma x raw open, lower = lo - band_mult x sigma x raw open, with hi = lo = session open (anchor=open) or hi/lo = max/min(open, previous session's last close) (anchor=open_prev_close). Session VWAP uses typical price x volume of the session's bars through bar k.
- Signals and trailing exits are evaluated only at check-bar closes (bar close a multiple of check_minutes after the session open) at least first_entry_minutes after the open; an entry is decided at that close and fills at the NEXT bar's open in the same session; the session's last bar never signals.
- Trailing exit (decided at a check close, filled at the next open): long below the upper band / VWAP / max of the two (trail = band / vwap / band_vwap), short above the lower band / VWAP / min of the two.
- Every position is closed at the session's last bar CLOSE (market-on-close with the same slippage); nothing is held overnight. This takes precedence over a trailing exit decided at the same close.
- Optional protective stop = entry-bar open -/+ k x ATR(14) using the ATR known before the fill, live from the entry bar, filled at the worse of open and stop; it takes precedence over close-based exits of the same bar.
- After a trailing or stop exit, a same-direction entry needs a check close back inside that side's band (at or after the exit decision, same session); each session starts armed. Missed-entry stress blocks the missed direction the same way, so a missed entry is never re-taken a bar later.
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
- Rolls happen outside the day session (Databento rolls at 00:00 UTC) and every position is flat by the session close, so no trade straddles a roll; the band is scaled by the RAW session open (adjusted - price_adjustment).

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Whole-contract granularity: at ~$1M equity the position is a handful of ES contracts, so position size steps with price; results are sensitive to starting equity at small sizes.
- band_lookback counts SESSIONS (per time-of-day slot); ATR(14) counts bars of the config's timeframe and runs across sessions (RTH bars only).
- The paper sizes by volatility targeting with up to 4x leverage; here sizing is unlevered full-equity whole contracts, identical to the mean-reversion funnel so results are comparable.
- Session VWAP is built from the aggregated bars' typical price, not tick data; a session's first bar opens at the day-session open (RTH only), so the paper's 'move from the open' is measured from that open, not the overnight Globex session.
- 5min and 15min bars with the same check interval decide at the same clock times (v1 has no stop), so they differ only in fill timing granularity; near-duplicates are expected and left to stage 6.
- first_entry_minutes below the first check time changes nothing (check 30: first entry 15 = 30; check 60: 15 = 30 = 60), so 2,700 of the 8,100 v1 configs repeat another config's backtest exactly; they count in the raw trial total and collapse in stage 6.
