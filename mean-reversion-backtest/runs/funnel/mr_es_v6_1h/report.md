# Screening funnel -- mr_es_v6_1h (development stages only)

- Code: `5342a94cdc84` (dirty working tree: True, diff sha256 `aca36e65d581`)
- Config: `configs/funnel/mr_funnel_es_v6_1h.yaml` sha256 `cd720326f989f92b`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'NQ': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `3861e259b5b34035` (39 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_es_v3, v4 and v5 gated 11, 18 and 45 ES candidates on 2023-2024, and this grid was chosen after reading those results (and the per-bar-size breakdown of v5's development survivors). ES also tracks the same index as SPY, whose 2023-2024 gated earlier SPY studies. So ES 2023-2024 is largely in-sample here; the 2025+ holdout is the only untouched test.
- Holdout 2025+ previously inspected: **False** -- No ES strategy metrics have been computed on 2025+. SPY 2025-2026 holdout metrics were inspected in earlier SPY studies, and the futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no strategy selection).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 6804 | 6804 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 6804 | 6804 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 6804 | 3991 | 2813 | 0 |  | 5299 | 58.66 | 58.66 |  |
| 3 performance & risk | hard_gate | 3991 | 66 | 3925 | 0 |  | 0 | 0.97 | 1.65 |  |
| 4 parameter stability | hard_gate | 66 | 60 | 6 | 0 |  | 0 | 0.88 | 90.91 |  |
| 5 time stability | hard_gate | 60 | 60 | 0 | 0 |  | 57 | 0.88 | 100.00 |  |
| 6 deduplication | dedup | 60 | 39 |  |  | 21 |  | 0.57 | 65.00 | best 2 per cluster |
| 7 execution stress | hard_gate | 39 | 39 | 0 | 0 |  | 1 | 0.57 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 39 |  |  |  |  |  |  |  | diagnostic only: unverified: 39 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 2813 |
| s2:hard_reject:years_with_>=10_trades | 1525 |
| s3:hard_reject:max_drawdown | 283 |
| s3:hard_reject:net_return | 2275 |
| s3:hard_reject:sharpe | 3925 |
| s4:hard_reject:local_median_sharpe | 6 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | NQ dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_33bd` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 3/73/50 | 126 | 21.6% | 4.0% | 1.15 | -5.1% | 214 | 1.72 | 4.4% | 58.4 | 10/10 | 0.90 | 0.70 | 0.45 | 5 | 11.2% | 0.44 | 0.54 | 20.8% | 18.8% | 8.5% | 18.0%/15.2% | 9.9 (interpolated) | pass | 0.412 (unverified) | 0.21 |
| 2 | `cfg_0424` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 0/76/50 | 126 | 21.1% | 3.9% | 1.13 | -5.1% | 214 | 1.71 | 4.4% | 58.2 | 9/9 | 0.89 | 0.64 | 0.49 | 5 | 10.7% | 0.45 | 0.55 | 19.8% | 17.9% | 8.1% | 17.4%/11.8% | 9.6 (interpolated) | pass | 0.389 (unverified) | 0.24 |
| 3 | `cfg_dc4f` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 1/114/0 | 115 | 26.5% | 4.8% | 1.16 | -3.0% | 308 | 1.89 | 5.2% | 54.2 | 9/9 | 0.78 | 0.85 | 0.31 | 5 | 13.1% | 0.46 | 0.54 | 25.2% | 24.1% | 20.7% | 24.3%/17.6% | 13.4 (interpolated) | pass | 0.411 (unverified) | 0.57 |
| 4 | `cfg_892f` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-2.0, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 6/109/0 | 115 | 26.2% | 4.8% | 1.15 | -3.0% | 308 | 1.88 | 5.2% | 54.2 | 10/10 | 0.80 | 0.85 | 0.29 | 5 | 13.2% | 0.45 | 0.54 | 24.9% | 23.8% | 20.0% | 23.9%/19.4% | 13.3 (interpolated) | pass | 0.402 (unverified) | 0.57 |
| 5 | `cfg_5810` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 20/70/20 | 110 | 28.2% | 5.1% | 1.10 | -3.9% | 176 | 1.77 | 6.5% | 51.3 | 9/9 | 1.00 | 0.40 | 0.69 | 5 | 19.6% | 0.28 | 0.52 | 26.5% | 25.5% | 11.4% | 22.9%/16.8% | 14.3 (interpolated) | pass | 0.361 (unverified) | -0.19 |
| 6 | `cfg_8cb6` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=100, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 2/62/42 | 106 | 15.8% | 3.0% | 0.87 | -5.5% | 652 | 1.59 | 3.7% | 48.4 | 8/8 | 1.00 | 0.70 | 0.17 | 4 | 6.8% | 0.57 | 0.77 | 14.4% | 13.4% | 5.9% | 13.3%/9.8% | 9.2 (interpolated) | pass | 0.171 (unverified) | 0.99 |
| 7 | `cfg_29fb` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 6/82/21 | 109 | 28.0% | 5.1% | 1.06 | -3.9% | 174 | 1.75 | 6.8% | 50.9 | 9/9 | 1.00 | 0.42 | 0.64 | 5 | 20.1% | 0.28 | 0.55 | 26.9% | 25.9% | 10.5% | 23.6%/14.8% | 14.5 (interpolated) | pass | 0.329 (unverified) | -0.14 |
| 8 | `cfg_f91c` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=100, entry_z=-2.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.0 | 38/16/68 | 122 | 24.2% | 4.4% | 0.82 | -6.1% | 482 | 1.54 | 6.1% | 56.5 | 8/8 | 1.00 | 0.63 | 0.20 | 5 | 10.5% | 0.54 | 0.63 | 22.9% | 21.6% | 22.2% | 20.4%/15.4% | 11.3 (interpolated) | pass | 0.165 (unverified) | 0.46 |
| 9 | `cfg_1816` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=80, entry_z=-2.0, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 5/58/46 | 109 | 13.8% | 2.6% | 0.88 | -3.5% | 633 | 1.48 | 3.8% | 50.0 | 9/9 | 0.89 | 0.60 | 0.29 | 4 | 6.5% | 0.49 | 0.81 | 12.7% | 11.6% | 4.2% | 12.0%/7.5% | 8.4 (interpolated) | pass | 0.188 (unverified) | 0.34 |
| 10 | `cfg_ce00` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.0 | 53/16/86 | 155 | 30.8% | 5.5% | 0.90 | -5.6% | 286 | 1.50 | 7.8% | 71.9 | 9/9 | 0.89 | 0.65 | 0.26 | 4 | 16.0% | 0.46 | 0.56 | 29.1% | 27.3% | 20.7% | 25.5%/16.4% | 11.3 (interpolated) | pass | 0.217 (unverified) | 0.08 |
| 11 | `cfg_a11e` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=17, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 19/65/19 | 103 | 29.4% | 5.3% | 0.79 | -7.2% | 254 | 1.66 | 6.3% | 48.9 | 10/10 | 1.00 | 0.65 | 0.14 | 4 | 13.6% | 0.48 | 0.73 | 28.6% | 27.8% | 25.3% | 29.4%/22.6% | 16.4 (interpolated) | pass | 0.142 (unverified) | 0.47 |
| 12 | `cfg_b025` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=100, entry_z=-2.0, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 5/60/44 | 109 | 12.7% | 2.4% | 0.77 | -5.5% | 726 | 1.46 | 3.8% | 49.6 | 9/9 | 1.00 | 0.68 | 0.09 | 4 | 5.5% | 0.57 | 0.80 | 11.9% | 11.1% | 5.3% | 12.3%/7.4% | 7.7 (interpolated) | pass | 0.126 (unverified) | 0.98 |
| 13 | `cfg_0941` | timeframe=1h, mean_type=sma, mean_lookback=46, std_lookback=100, entry_z=-2.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.0 | 40/18/72 | 130 | 28.9% | 5.2% | 0.94 | -5.4% | 334 | 1.60 | 6.6% | 59.9 | 8/8 | 1.00 | 0.64 | 0.30 | 5 | 15.4% | 0.44 | 0.57 | 27.8% | 25.6% | 23.7% | 26.4%/19.8% | 12.1 (interpolated) | pass | 0.237 (unverified) | 0.42 |
| 14 | `cfg_5834` | timeframe=1h, mean_type=sma, mean_lookback=34, std_lookback=90, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 0/62/46 | 108 | 12.3% | 2.4% | 0.79 | -5.1% | 520 | 1.45 | 3.7% | 49.6 | 9/9 | 1.00 | 0.73 | 0.06 | 4 | 3.4% | 0.68 | 0.82 | 11.4% | 10.8% | -0.9% | 10.9%/7.1% | 7.4 (interpolated) | pass | 0.134 (unverified) | 1.00 |
| 15 | `cfg_7cda` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=17, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 26/58/19 | 103 | 30.9% | 5.5% | 0.83 | -7.2% | 254 | 1.69 | 6.2% | 48.8 | 11/11 | 1.00 | 0.68 | 0.15 | 4 | 14.6% | 0.47 | 0.70 | 29.8% | 29.0% | 28.0% | 28.4%/20.0% | 17.1 (interpolated) | pass | 0.163 (unverified) | 0.41 |
| 16 | `cfg_65d6` | timeframe=1h, mean_type=sma, mean_lookback=46, std_lookback=100, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 3/65/40 | 108 | 19.0% | 3.5% | 1.01 | -3.2% | 319 | 1.71 | 3.8% | 49.6 | 8/8 | 1.00 | 0.57 | 0.43 | 4 | 10.6% | 0.40 | 0.67 | 17.5% | 16.4% | 11.0% | 16.4%/12.1% | 10.6 (interpolated) | pass | 0.252 (unverified) | 0.36 |
| 17 | `cfg_ce0f` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=80, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 0/63/46 | 109 | 13.0% | 2.5% | 0.84 | -3.7% | 633 | 1.45 | 3.8% | 50.2 | 8/8 | 0.88 | 0.55 | 0.29 | 4 | 5.7% | 0.52 | 0.86 | 11.8% | 10.4% | 3.1% | 11.6%/6.6% | 7.9 (interpolated) | pass | 0.160 (unverified) | 0.36 |
| 18 | `cfg_bed1` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 23/53/25 | 101 | 19.9% | 3.7% | 0.84 | -9.7% | 330 | 1.63 | 5.8% | 46.3 | 11/11 | 0.82 | 0.64 | 0.19 | 4 | 11.2% | 0.41 | 0.63 | 18.9% | 18.3% | 18.9% | 18.6%/13.8% | 11.7 (interpolated) | pass | 0.200 (unverified) | -0.08 |
| 19 | `cfg_845b` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 1/110/67 | 178 | 22.0% | 4.1% | 0.87 | -6.5% | 308 | 1.42 | 6.4% | 83.6 | 9/9 | 0.67 | 0.69 | 0.18 | 4 | 6.7% | 0.65 | 0.71 | 19.3% | 17.4% | 3.2% | 18.3%/14.1% | 7.6 (interpolated) | pass | 0.207 (unverified) | -0.10 |
| 20 | `cfg_2acf` | timeframe=1h, mean_type=sma, mean_lookback=46, std_lookback=100, entry_z=-2.0, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 6/63/42 | 111 | 17.1% | 3.2% | 0.93 | -3.2% | 442 | 1.62 | 3.9% | 50.8 | 9/9 | 1.00 | 0.65 | 0.29 | 4 | 9.4% | 0.41 | 0.72 | 16.0% | 15.5% | 12.2% | 15.1%/11.1% | 9.6 (interpolated) | pass | 0.197 (unverified) | 0.33 |
| 21 | `cfg_52dd` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-2.0, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.0 | 5/106/67 | 178 | 20.7% | 3.8% | 0.83 | -6.6% | 308 | 1.39 | 6.4% | 83.4 | 10/10 | 0.70 | 0.70 | 0.13 | 4 | 5.9% | 0.67 | 0.72 | 19.1% | 17.1% | 2.7% | 18.4%/12.3% | 7.4 (interpolated) | pass | 0.188 (unverified) | -0.10 |
| 22 | `cfg_a600` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 50/22/36 | 108 | 28.9% | 5.2% | 0.82 | -7.5% | 358 | 1.61 | 7.6% | 49.7 | 10/10 | 0.90 | 0.71 | 0.11 | 4 | 12.0% | 0.56 | 0.58 | 27.6% | 26.9% | 17.4% | 26.1%/19.4% | 15.0 (interpolated) | pass | 0.173 (unverified) | -0.26 |
| 23 | `cfg_324a` | timeframe=1h, mean_type=sma, mean_lookback=34, std_lookback=12, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 25/59/17 | 101 | 29.9% | 5.4% | 0.76 | -6.8% | 443 | 1.85 | 6.0% | 47.7 | 10/10 | 1.00 | 0.54 | 0.23 | 5 | 12.6% | 0.58 | 0.47 | 29.3% | 28.2% | 11.0% | 26.6%/21.2% | 16.4 (interpolated) | pass | 0.136 (unverified) | 1.11 |
| 24 | `cfg_994a` | timeframe=1h, mean_type=sma, mean_lookback=34, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 34/51/17 | 102 | 29.2% | 5.3% | 0.75 | -7.7% | 469 | 1.84 | 5.9% | 47.9 | 9/9 | 1.00 | 0.47 | 0.28 | 5 | 12.7% | 0.57 | 0.48 | 28.5% | 27.6% | 7.8% | 26.6%/19.2% | 15.9 (interpolated) | pass | 0.131 (unverified) | 0.98 |
| 25 | `cfg_daef` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=17, entry_z=-1.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 6/80/24 | 110 | 23.5% | 4.3% | 0.89 | -4.0% | 322 | 1.58 | 6.6% | 51.2 | 9/9 | 1.00 | 0.65 | 0.25 | 4 | 12.6% | 0.41 | 0.65 | 22.6% | 21.8% | 21.6% | 20.6%/15.3% | 12.4 (interpolated) | pass | 0.209 (unverified) | -0.65 |
| 26 | `cfg_a8a3` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=12, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 30/63/22 | 115 | 21.2% | 3.9% | 0.78 | -7.1% | 706 | 1.49 | 6.6% | 54.1 | 10/10 | 1.00 | 0.57 | 0.21 | 3 | 10.8% | 0.45 | 0.63 | 19.8% | 18.6% | 6.6% | 17.5%/9.7% | 10.7 (interpolated) | pass | 0.154 (unverified) | -0.44 |
| 27 | `cfg_b545` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 31/40/77 | 148 | 18.7% | 3.5% | 0.77 | -8.5% | 330 | 1.42 | 6.3% | 67.6 | 10/10 | 0.90 | 0.54 | 0.23 | 4 | 8.7% | 0.51 | 0.69 | 17.3% | 15.4% | 12.8% | 17.3%/10.5% | 7.9 (interpolated) | pass | 0.141 (unverified) | -0.15 |
| 28 | `cfg_4392` | timeframe=1h, mean_type=sma, mean_lookback=34, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.0 | 53/11/85 | 149 | 23.8% | 4.4% | 0.77 | -5.3% | 286 | 1.41 | 7.2% | 69.0 | 9/9 | 1.00 | 0.56 | 0.21 | 5 | 11.4% | 0.51 | 0.71 | 21.9% | 20.5% | 16.0% | 20.3%/13.8% | 9.7 (interpolated) | pass | 0.136 (unverified) | 0.21 |
| 29 | `cfg_dfd4` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=17, entry_z=-1.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 12/74/24 | 110 | 22.6% | 4.2% | 0.87 | -4.0% | 322 | 1.56 | 6.5% | 51.3 | 10/10 | 1.00 | 0.66 | 0.21 | 4 | 12.3% | 0.40 | 0.67 | 21.8% | 20.8% | 20.1% | 20.4%/14.3% | 11.7 (interpolated) | pass | 0.195 (unverified) | -0.80 |
| 30 | `cfg_413c` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=12, entry_z=-1.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 21/65/22 | 108 | 19.0% | 3.5% | 0.80 | -5.6% | 551 | 1.53 | 6.3% | 50.9 | 8/8 | 1.00 | 0.50 | 0.30 | 4 | 10.2% | 0.45 | 0.62 | 17.9% | 16.3% | 20.8% | 16.3%/9.6% | 10.8 (interpolated) | pass | 0.156 (unverified) | -0.81 |
| 31 | `cfg_d654` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 31/61/23 | 115 | 25.7% | 4.7% | 0.81 | -5.7% | 317 | 1.65 | 6.8% | 54.1 | 11/11 | 0.91 | 0.48 | 0.33 | 4 | 11.6% | 0.49 | 0.69 | 24.5% | 23.2% | 14.3% | 23.1%/15.6% | 12.4 (interpolated) | pass | 0.132 (unverified) | 0.60 |
| 32 | `cfg_de5e` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=90, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 1/101/0 | 102 | 22.9% | 4.2% | 1.09 | -3.0% | 304 | 1.97 | 4.6% | 48.3 | 9/9 | 0.89 | 0.64 | 0.46 | 4 | 7.6% | 0.63 | 0.57 | 22.1% | 20.8% | 5.2% | 20.2%/16.1% | 13.4 (interpolated) | pass | 0.344 (unverified) | 0.73 |
| 33 | `cfg_980f` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=90, entry_z=-2.0, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 5/97/0 | 102 | 22.8% | 4.2% | 1.10 | -2.8% | 304 | 1.98 | 4.6% | 48.2 | 10/10 | 0.90 | 0.70 | 0.40 | 4 | 7.9% | 0.61 | 0.57 | 21.6% | 20.6% | 5.1% | 20.2%/16.2% | 13.1 (interpolated) | pass | 0.347 (unverified) | 0.73 |
| 34 | `cfg_a53b` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 4/104/0 | 108 | 31.1% | 5.6% | 0.81 | -6.8% | 308 | 1.82 | 7.3% | 50.6 | 10/10 | 0.70 | 0.59 | 0.21 | 4 | 17.6% | 0.43 | 0.59 | 30.2% | 29.1% | 37.9% | 28.4%/21.2% | 16.0 (interpolated) | pass | 0.153 (unverified) | 0.11 |
| 35 | `cfg_2f9d` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=100, entry_z=-1.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 63/39/0 | 102 | 21.8% | 4.0% | 0.76 | -4.6% | 136 | 1.54 | 8.1% | 47.9 | 7/7 | 1.00 | 0.56 | 0.20 | 4 | 10.7% | 0.51 | 0.65 | 20.2% | 19.4% | 17.0% | 19.2%/13.1% | 12.0 (interpolated) | pass | 0.140 (unverified) | 0.36 |
| 36 | `cfg_0eff` | timeframe=1h, mean_type=sma, mean_lookback=34, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 54/15/34 | 103 | 25.7% | 4.7% | 0.76 | -5.8% | 212 | 1.59 | 7.1% | 47.1 | 10/10 | 0.90 | 0.59 | 0.17 | 5 | 10.9% | 0.57 | 0.62 | 24.6% | 23.6% | 22.2% | 22.1%/15.5% | 13.8 (interpolated) | pass | 0.138 (unverified) | 0.20 |
| 37 | `cfg_7559` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 3/95/97 | 195 | 30.4% | 5.5% | 0.77 | -7.0% | 657 | 1.45 | 9.1% | 90.3 | 10/10 | 0.70 | 0.41 | 0.37 | 4 | 15.7% | 0.48 | 0.63 | 28.1% | 24.9% | 12.0% | 23.0%/15.7% | 8.7 (interpolated) | pass | 0.145 (unverified) | -0.11 |
| 38 | `cfg_cdc9` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=22, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 13/91/0 | 104 | 30.0% | 5.4% | 0.75 | -15.3% | 597 | 1.53 | 10.3% | 48.9 | 7/7 | 0.43 | 0.00 | 0.75 | 4 | 14.5% | 0.52 | 0.67 | 29.1% | 27.9% | 24.0% | 26.0%/16.2% | 16.4 (interpolated) | pass | 0.160 (unverified) | 0.03 |
| 39 | `cfg_cf9e` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=12, entry_z=-2.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 17/72/40 | 129 | 14.7% | 2.8% | 0.76 | -4.4% | 607 | 1.43 | 4.8% | 59.6 | 8/8 | 1.00 | 0.37 | 0.39 | 4 | 7.4% | 0.50 | 0.66 | 13.1% | 11.8% | 0.5% | 11.5%/6.6% | 7.5 (interpolated) | pass | 0.128 (unverified) | -0.34 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 0.2% / 0.06 / 38 | 2.3% / 1.21 / 15 | 9.4% / 2.59 / 16 | 3.1% / 0.85 / 36 | 5.2% / 1.34 / 21 |
| 2 | 0.2% / 0.06 / 38 | 2.2% / 1.20 / 15 | 9.4% / 2.59 / 16 | 2.7% / 0.74 / 36 | 5.3% / 1.34 / 21 |
| 3 | 1.7% / 0.47 / 24 | 0.6% / 0.37 / 16 | 11.8% / 2.54 / 19 | 3.1% / 0.79 / 24 | 7.2% / 1.23 / 32 |
| 4 | 1.7% / 0.47 / 24 | 0.6% / 0.37 / 16 | 11.5% / 2.52 / 19 | 3.1% / 0.79 / 24 | 7.2% / 1.23 / 32 |
| 5 | 5.9% / 1.20 / 28 | 2.3% / 0.86 / 18 | 7.2% / 1.26 / 19 | 3.8% / 1.20 / 12 | 6.4% / 1.08 / 33 |
| 6 | -3.9% / -1.09 / 29 | 2.0% / 1.14 / 13 | 4.4% / 1.49 / 15 | 4.3% / 1.18 / 32 | 8.4% / 1.78 / 17 |
| 7 | 6.7% / 1.35 / 28 | 1.7% / 0.60 / 17 | 5.7% / 0.98 / 19 | 4.8% / 1.34 / 12 | 6.6% / 1.10 / 33 |
| 8 | 0.3% / 0.08 / 34 | 0.2% / 0.08 / 21 | 5.7% / 1.04 / 16 | 12.4% / 2.48 / 34 | 4.0% / 0.63 / 17 |
| 9 | 0.6% / 0.20 / 25 | -1.4% / -0.69 / 18 | 6.8% / 2.36 / 16 | 3.4% / 1.05 / 32 | 3.8% / 1.14 / 18 |
| 10 | 5.7% / 0.83 / 44 | -0.0% / 0.02 / 20 | 4.6% / 0.66 / 22 | 12.8% / 2.48 / 42 | 4.9% / 0.71 / 27 |
| 11 | 3.5% / 0.67 / 27 | -1.7% / -0.78 / 10 | 13.9% / 1.14 / 18 | 2.6% / 1.02 / 16 | 8.9% / 1.27 / 32 |
| 12 | -3.9% / -1.09 / 29 | 1.0% / 0.57 / 16 | 4.2% / 1.44 / 15 | 4.3% / 1.17 / 32 | 6.8% / 1.83 / 17 |
| 13 | 1.5% / 0.26 / 37 | 0.2% / 0.06 / 21 | 6.9% / 1.21 / 17 | 11.7% / 2.25 / 36 | 6.3% / 0.93 / 19 |
| 14 | -3.3% / -1.12 / 27 | 1.3% / 0.77 / 14 | 8.6% / 2.46 / 15 | 1.6% / 0.47 / 33 | 3.9% / 1.23 / 19 |
| 15 | 3.6% / 0.69 / 27 | -1.7% / -0.78 / 10 | 14.2% / 1.16 / 18 | 2.6% / 1.02 / 16 | 9.7% / 1.43 / 32 |
| 16 | -0.5% / -0.16 / 27 | 1.5% / 0.97 / 14 | 7.6% / 1.70 / 14 | 3.8% / 0.99 / 35 | 5.5% / 1.34 / 18 |
| 17 | 0.6% / 0.20 / 25 | -1.5% / -0.78 / 18 | 6.8% / 2.36 / 16 | 2.8% / 0.87 / 32 | 3.8% / 1.14 / 18 |
| 18 | -1.9% / -0.23 / 31 | 2.1% / 1.13 / 15 | 3.6% / 1.02 / 14 | 7.8% / 2.01 / 25 | 7.1% / 1.62 / 16 |
| 19 | -1.6% / -0.36 / 40 | 1.1% / 0.67 / 22 | 14.3% / 3.02 / 22 | 2.6% / 0.63 / 43 | 4.5% / 0.66 / 51 |
| 20 | -0.5% / -0.16 / 27 | 0.5% / 0.35 / 17 | 7.1% / 1.70 / 14 | 3.4% / 0.91 / 35 | 5.8% / 1.38 / 18 |
| 21 | -1.6% / -0.36 / 40 | 1.1% / 0.67 / 22 | 14.0% / 3.00 / 22 | 2.5% / 0.61 / 43 | 3.9% / 0.58 / 51 |
| 22 | 5.6% / 0.68 / 32 | -1.3% / -0.31 / 17 | 2.4% / 0.35 / 16 | 15.1% / 3.03 / 24 | 4.9% / 0.77 / 19 |
| 23 | 1.0% / 0.19 / 29 | 3.9% / 1.39 / 12 | 3.5% / 0.34 / 18 | 3.6% / 1.51 / 11 | 15.4% / 2.02 / 31 |
| 24 | 1.6% / 0.30 / 29 | 4.9% / 1.73 / 13 | 1.8% / 0.20 / 18 | 3.8% / 1.62 / 11 | 14.7% / 1.97 / 31 |
| 25 | 9.7% / 1.99 / 27 | -1.4% / -0.43 / 20 | 5.5% / 1.14 / 12 | 7.5% / 1.53 / 22 | 0.6% / 0.13 / 29 |
| 26 | 9.4% / 2.07 / 25 | -2.1% / -0.60 / 21 | -1.9% / -0.32 / 16 | 8.0% / 2.10 / 17 | 6.8% / 0.93 / 36 |
| 27 | -1.1% / -0.16 / 44 | 2.7% / 1.47 / 18 | 2.1% / 0.45 / 21 | 9.3% / 2.21 / 41 | 4.7% / 0.90 / 24 |
| 28 | 4.7% / 0.73 / 41 | 0.3% / 0.10 / 22 | 4.6% / 0.68 / 23 | 11.2% / 2.42 / 39 | 1.5% / 0.25 / 24 |
| 29 | 9.2% / 1.92 / 27 | -1.4% / -0.43 / 20 | 5.6% / 1.14 / 12 | 7.5% / 1.57 / 22 | 0.4% / 0.09 / 29 |
| 30 | 7.5% / 1.90 / 25 | -4.0% / -1.24 / 21 | 3.1% / 0.88 / 11 | 8.0% / 1.83 / 21 | 3.5% / 0.55 / 30 |
| 31 | 0.2% / 0.07 / 33 | -0.3% / -0.08 / 16 | 12.7% / 1.33 / 18 | 6.1% / 1.98 / 18 | 5.2% / 0.96 / 30 |
| 32 | 1.6% / 0.63 / 18 | -0.5% / -0.31 / 14 | 14.2% / 2.82 / 20 | 1.0% / 0.28 / 21 | 5.4% / 1.06 / 29 |
| 33 | 1.6% / 0.63 / 18 | -0.5% / -0.31 / 14 | 13.8% / 2.80 / 20 | 1.0% / 0.28 / 21 | 5.6% / 1.11 / 29 |
| 34 | -0.1% / 0.01 / 23 | 0.5% / 0.19 / 16 | 10.4% / 0.89 / 17 | 6.1% / 1.32 / 23 | 11.5% / 1.70 / 29 |
| 35 | -0.0% / 0.02 / 21 | 1.1% / 0.39 / 17 | 9.2% / 1.47 / 15 | 10.0% / 2.04 / 24 | 0.3% / 0.08 / 25 |
| 36 | 3.2% / 0.43 / 31 | 0.6% / 0.17 / 18 | 5.3% / 0.67 / 16 | 13.3% / 3.03 / 21 | 1.5% / 0.28 / 17 |
| 37 | -3.4% / -0.50 / 57 | 2.0% / 0.65 / 27 | 5.7% / 0.54 / 26 | 11.0% / 2.24 / 42 | 12.6% / 1.68 / 43 |
| 38 | 6.1% / 1.05 / 22 | 3.8% / 0.73 / 20 | -4.7% / -0.40 / 18 | 9.0% / 2.07 / 14 | 13.6% / 1.48 / 30 |
| 39 | 2.1% / 0.65 / 26 | -1.8% / -0.71 / 23 | 0.2% / 0.07 / 20 | 6.9% / 2.17 / 19 | 6.8% / 1.25 / 41 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_33bd` | 6 | 0.85 | 0.90/0.91 | 0.86/0.88 |
| 1 | `cfg_f91c` | 3 | 0.91 | 0.90/0.93 | 0.75/0.81 |
| 2 | `cfg_5810` | 3 | 0.97 | 0.98/0.99 | 0.95/0.96 |
| 3 | `cfg_4392` | 2 | 0.86 | 0.87/0.87 | 0.72/0.72 |
| 4 | `cfg_dc4f` | 6 | 0.96 | 0.88/0.90 | 0.93/0.93 |
| 5 | `cfg_1816` | 3 | 0.98 | 0.99/0.99 | 0.98/0.98 |
| 6 | `cfg_de5e` | 6 | 0.87 | 0.61/0.64 | 0.46/0.46 |
| 7 | `cfg_65d6` | 3 | 0.96 | 0.98/0.99 | 0.96/0.96 |
| 8 | `cfg_2f9d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 9 | `cfg_324a` | 2 | 0.97 | 0.99/0.99 | 0.98/0.98 |
| 10 | `cfg_413c` | 1 | n/a | n/a/n/a | n/a/n/a |
| 11 | `cfg_845b` | 3 | 0.99 | 0.99/0.99 | 0.98/0.99 |
| 12 | `cfg_5834` | 1 | n/a | n/a/n/a | n/a/n/a |
| 13 | `cfg_a53b` | 4 | 0.85 | 0.84/0.84 | 0.54/0.55 |
| 14 | `cfg_ce00` | 3 | 0.86 | 0.91/0.93 | 0.75/0.80 |
| 15 | `cfg_daef` | 3 | 0.93 | 0.94/0.97 | 0.97/0.98 |
| 16 | `cfg_a11e` | 2 | 0.99 | 1.00/1.00 | 0.97/0.97 |
| 17 | `cfg_8cb6` | 2 | 0.98 | 0.99/0.99 | 0.96/0.96 |
| 18 | `cfg_a8a3` | 1 | n/a | n/a/n/a | n/a/n/a |
| 19 | `cfg_bed1` | 2 | 0.91 | 0.83/0.83 | 0.61/0.61 |
| 20 | `cfg_cdc9` | 1 | n/a | n/a/n/a | n/a/n/a |
| 21 | `cfg_cf9e` | 1 | n/a | n/a/n/a | n/a/n/a |
| 22 | `cfg_d654` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 6.815e-04 over 6804 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 447.0, participation ratio 11.6, 95%-variance components 131 (rank bound T = 1259); raw grid 6804; raw + known prior 865788
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

- z = (close - mean) / std with mean = SMA/EMA of the last N closes and std = rolling sample std of the last M closes (bars of the config's timeframe), both INCLUDING the signal bar's close; the signal is decided at that close and the entry fills at the NEXT bar's open.
- Exits are decided at a close on or after the entry bar (z >= exit_z, or held max_hold bars) and fill at the next bar's open, so a time exit fills exactly max_hold bars after entry.
- Trend filter compares the signal bar's close to the SMA(100/150/200 bars) of closes up to that bar; warm-up bars (SMA undefined) never signal.
- No profit target exists. v1 has no stop; v2's optional ATR stop is entry fill - k x ATR(14) using the ATR known before the fill, live from the entry bar, filled at the worse of open and stop. Sizing (v1 and v2): as many whole shares as current equity affords (no leverage).
- v2 only: the z-score std uses the same window as the mean; positive_bar_return requires the signal bar's close above the previous close; cooldown_bars = N requires the next signal bar to be >= N bars after the previous exit.
- After a time exit the setup re-arms only once z closes above entry_z, so the holding cap cannot be undone by an immediate re-entry.
- Missed-entry stress skips a whole signal episode (contiguous signal bars), never re-entering one bar later.
- Adverse slippage + commission on every fill; a fill at a session's first bar bears the full overnight gap.
- Development backtests run on data physically truncated at the development end; open positions are force-closed at the last development bar and flagged (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Positions are held overnight (no session-end flattening), as in the channel family; rolling windows run continuously across sessions over RTH bars only.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC; the 1-minute step there is taken as the roll spread). Point moves are preserved; pre-roll price levels are not real traded prices.
- Session: each root's day session only (src/data/futures.py SESSIONS: NYSE 09:30-16:00 NY for equity indexes, 09:00-14:30 NY for crude, 08:20-13:30 NY for gold, 08:20-15:00 NY for FX; sessions under 5% of normal volume are skipped), on NYSE trading days; overnight Globex bars are not traded or used in indicators.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side (stops too) plus commission per contract per side, from the execution YAML; cost stress scales both.
- Positions that straddle a roll are treated as if rolled for free at the adjusted spread (no extra roll commission/slippage).

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Whole-contract granularity: at ~$1M equity the position is a handful of ES contracts, so position size steps with price; results are sensitive to starting equity at small sizes.
- All lookbacks and holding periods are counted in bars of the config's timeframe (RTH bars only), not in trading days.
- entry_confirmation = positive_bar_return means the signal bar closed above the previous bar's close (the 'directional bar' option).
