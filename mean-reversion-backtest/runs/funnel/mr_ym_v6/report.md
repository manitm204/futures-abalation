# Screening funnel -- mr_ym_v6 (development stages only)

- Code: `5342a94cdc84` (dirty working tree: True, diff sha256 `32f3b64dec90`)
- Config: `configs/funnel/mr_funnel_ym_v6.yaml` sha256 `4ab36546a7eb02d0`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'YM': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `3a3a16ff2d76b3fa` (267 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_ym_v5 gated 61 YM candidates on 2023-2024 (9 passed) and this grid was written after reading those results, so YM 2023-2024 is partly in-sample here. The stage-4 test and 40-trade rule were also shaped by ES 2023-2024.
- Holdout 2025+ previously inspected: **False** -- No YM strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection). The holdout is the only untouched test for this run.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 72000 | 72000 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 72000 | 72000 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 72000 | 54408 | 17592 | 0 |  | 59743 | 75.57 | 75.57 |  |
| 3 performance & risk | hard_gate | 54408 | 860 | 53548 | 0 |  | 0 | 1.19 | 1.58 |  |
| 4 parameter stability | hard_gate | 860 | 844 | 16 | 0 |  | 0 | 1.17 | 98.14 |  |
| 5 time stability | hard_gate | 844 | 843 | 1 | 0 |  | 651 | 1.17 | 99.88 |  |
| 6 deduplication | dedup | 843 | 267 |  |  | 576 |  | 0.37 | 31.67 | best 2 per cluster |
| 7 execution stress | hard_gate | 267 | 267 | 0 | 0 |  | 114 | 0.37 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 267 |  |  |  |  |  |  |  | diagnostic only: unverified: 267 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 17592 |
| s2:hard_reject:years_with_>=10_trades | 11909 |
| s3:hard_reject:max_drawdown | 5286 |
| s3:hard_reject:net_return | 32020 |
| s3:hard_reject:sharpe | 53548 |
| s4:hard_reject:local_median_sharpe | 16 |
| s5:hard_reject:profitable_years | 1 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_a1c3` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 58/62/35 | 155 | 48.5% | 8.2% | 1.45 | -4.6% | 220 | 1.89 | 8.4% | 68.6 | 9/9 | 0.89 | 0.98 | 0.47 | 5 | 34.5% | 0.25 | 0.37 | 47.7% | 46.9% | 9.4% | 41.3%/33.5% | n/a (profitable_beyond_25.0x) | pass | 0.657 (unverified) | 0.63 |
| 2 | `cfg_30bd` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 59/51/97 | 207 | 42.5% | 7.3% | 1.31 | -4.3% | 165 | 1.63 | 8.5% | 91.8 | 8/8 | 1.00 | 0.99 | 0.32 | 5 | 30.1% | 0.26 | 0.43 | 40.8% | 40.1% | 4.4% | 38.8%/31.1% | 18.0 (interpolated) | pass | 0.536 (unverified) | 0.70 |
| 3 | `cfg_7fa2` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 45/22/35 | 102 | 59.2% | 9.8% | 1.40 | -6.9% | 189 | 2.59 | 4.7% | 46.5 | 11/11 | 0.82 | 1.01 | 0.39 | 5 | 30.3% | 0.43 | 0.53 | 58.9% | 58.3% | 18.9% | 51.6%/41.3% | n/a (profitable_beyond_25.0x) | pass | 0.629 (unverified) | 0.81 |
| 4 | `cfg_c2b0` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 57/59/64 | 180 | 40.8% | 7.1% | 1.28 | -5.0% | 271 | 1.66 | 8.4% | 80.4 | 9/9 | 0.89 | 1.00 | 0.28 | 5 | 31.5% | 0.23 | 0.43 | 39.8% | 38.0% | 2.2% | 36.2%/27.9% | 19.5 (interpolated) | pass | 0.504 (unverified) | 0.57 |
| 5 | `cfg_49ca` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 30/60/18 | 108 | 21.6% | 4.0% | 1.22 | -5.4% | 241 | 2.16 | 1.7% | 48.3 | 10/10 | 0.90 | 0.82 | 0.40 | 4 | 9.7% | 0.54 | 0.44 | 21.0% | 20.6% | 6.5% | 18.1%/15.1% | 18.9 (interpolated) | pass | 0.440 (unverified) | 0.85 |
| 6 | `cfg_3366` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 42/16/50 | 108 | 53.1% | 8.9% | 1.42 | -4.0% | 189 | 2.56 | 4.3% | 48.8 | 10/10 | 0.80 | 0.95 | 0.47 | 5 | 26.7% | 0.44 | 0.55 | 52.4% | 51.8% | -2.9% | 47.3%/37.1% | n/a (profitable_beyond_25.0x) | pass | 0.650 (unverified) | 0.81 |
| 7 | `cfg_ecd5` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=15, entry_z=-1.75, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 49/57/0 | 106 | 63.7% | 10.4% | 1.41 | -7.3% | 147 | 2.42 | 11.4% | 47.2 | 10/10 | 0.90 | 0.98 | 0.43 | 5 | 32.1% | 0.42 | 0.47 | 62.4% | 62.5% | 35.4% | 56.4%/44.5% | n/a (profitable_beyond_25.0x) | pass | 0.648 (unverified) | 0.92 |
| 8 | `cfg_6969` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 50/54/95 | 199 | 39.7% | 6.9% | 1.22 | -5.7% | 184 | 1.56 | 8.3% | 87.6 | 9/9 | 1.00 | 0.95 | 0.27 | 5 | 25.5% | 0.28 | 0.45 | 38.7% | 37.2% | 1.9% | 35.5%/29.1% | 17.9 (interpolated) | pass | 0.451 (unverified) | 0.90 |
| 9 | `cfg_d9a8` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 40/61/30 | 131 | 36.0% | 6.3% | 1.20 | -4.6% | 255 | 1.79 | 7.4% | 57.7 | 10/10 | 1.00 | 0.91 | 0.29 | 5 | 24.5% | 0.29 | 0.47 | 34.7% | 34.3% | 1.0% | 31.3%/23.1% | 23.8 (interpolated) | pass | 0.432 (unverified) | 0.62 |
| 10 | `cfg_d8e5` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 30/63/33 | 126 | 40.0% | 7.0% | 1.27 | -3.9% | 163 | 1.82 | 7.2% | 55.0 | 11/11 | 1.00 | 0.98 | 0.29 | 5 | 23.7% | 0.33 | 0.50 | 39.1% | 38.1% | -0.5% | 34.3%/26.6% | n/a (profitable_beyond_25.0x) | pass | 0.494 (unverified) | 0.26 |
| 11 | `cfg_f1b1` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=15, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 17/77/31 | 125 | 46.8% | 8.0% | 1.15 | -5.9% | 300 | 1.99 | 7.5% | 55.6 | 10/10 | 0.90 | 0.96 | 0.19 | 5 | 26.9% | 0.36 | 0.52 | 45.9% | 43.7% | 20.8% | 41.2%/30.8% | n/a (profitable_beyond_25.0x) | pass | 0.383 (unverified) | 1.07 |
| 12 | `cfg_f526` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=15, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 16/63/47 | 126 | 43.5% | 7.5% | 1.14 | -5.9% | 168 | 2.01 | 6.7% | 56.5 | 10/10 | 0.90 | 0.91 | 0.22 | 5 | 27.6% | 0.31 | 0.56 | 42.5% | 41.8% | 19.0% | 36.9%/30.8% | n/a (profitable_beyond_25.0x) | pass | 0.368 (unverified) | 0.56 |
| 13 | `cfg_f2fb` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 14/78/54 | 146 | 32.4% | 5.8% | 1.08 | -5.4% | 372 | 1.64 | 7.6% | 64.6 | 11/11 | 1.00 | 1.02 | 0.06 | 5 | 20.4% | 0.33 | 0.60 | 31.7% | 30.7% | -3.7% | 29.0%/21.7% | 19.7 (interpolated) | pass | 0.324 (unverified) | 0.69 |
| 14 | `cfg_de5e` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 17/81/96 | 194 | 36.7% | 6.5% | 1.11 | -4.5% | 173 | 1.54 | 8.9% | 86.8 | 9/9 | 1.00 | 1.03 | 0.08 | 5 | 22.3% | 0.36 | 0.56 | 34.4% | 33.0% | -3.9% | 33.1%/25.2% | 17.1 (interpolated) | pass | 0.346 (unverified) | 0.65 |
| 15 | `cfg_5d7b` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=15, entry_z=-1.75, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 8/71/47 | 126 | 43.1% | 7.4% | 1.12 | -5.9% | 249 | 2.00 | 6.8% | 56.7 | 9/9 | 0.89 | 0.88 | 0.24 | 5 | 26.5% | 0.33 | 0.56 | 41.6% | 41.4% | 18.9% | 36.3%/29.8% | n/a (profitable_beyond_25.0x) | pass | 0.354 (unverified) | 0.54 |
| 16 | `cfg_69c0` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-1.75, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 5/74/92 | 171 | 40.9% | 7.1% | 1.04 | -6.9% | 311 | 1.74 | 7.7% | 76.0 | 9/9 | 1.00 | 0.88 | 0.16 | 4 | 26.5% | 0.32 | 0.61 | 40.0% | 38.8% | -21.5% | 35.7%/25.8% | 20.4 (interpolated) | pass | 0.276 (unverified) | 0.67 |
| 17 | `cfg_c4ea` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 8/90/96 | 194 | 39.5% | 6.9% | 1.18 | -4.4% | 202 | 1.58 | 9.1% | 86.6 | 9/9 | 0.89 | 0.99 | 0.19 | 5 | 24.6% | 0.34 | 0.53 | 37.9% | 35.4% | -3.8% | 33.9%/26.3% | 17.9 (interpolated) | pass | 0.410 (unverified) | 0.70 |
| 18 | `cfg_3014` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 10/69/92 | 171 | 41.4% | 7.2% | 1.05 | -7.1% | 311 | 1.74 | 7.6% | 76.1 | 10/10 | 1.00 | 0.94 | 0.11 | 4 | 24.7% | 0.33 | 0.61 | 40.6% | 39.6% | -21.2% | 36.1%/28.4% | 20.8 (interpolated) | pass | 0.281 (unverified) | 0.67 |
| 19 | `cfg_900b` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 38/59/55 | 152 | 33.5% | 6.0% | 1.14 | -5.6% | 328 | 1.65 | 7.4% | 67.3 | 10/10 | 1.00 | 0.90 | 0.24 | 5 | 21.7% | 0.32 | 0.52 | 33.0% | 31.4% | -7.0% | 29.9%/23.0% | 19.4 (interpolated) | pass | 0.379 (unverified) | 0.56 |
| 20 | `cfg_ce69` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 41/51/88 | 180 | 35.3% | 6.2% | 1.17 | -4.3% | 285 | 1.59 | 7.6% | 80.4 | 9/9 | 1.00 | 0.76 | 0.41 | 5 | 21.7% | 0.35 | 0.49 | 34.3% | 33.2% | -5.4% | 31.6%/24.0% | 18.2 (interpolated) | pass | 0.401 (unverified) | 0.56 |
| 21 | `cfg_95dd` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 12/77/19 | 108 | 20.9% | 3.9% | 1.22 | -5.6% | 241 | 2.12 | 1.8% | 48.5 | 11/11 | 0.91 | 0.83 | 0.39 | 4 | 10.4% | 0.49 | 0.40 | 20.3% | 19.5% | 4.1% | 18.0%/15.3% | 18.5 (interpolated) | pass | 0.442 (unverified) | 0.86 |
| 22 | `cfg_afcf` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 60/2/45 | 107 | 53.3% | 8.9% | 1.20 | -10.1% | 154 | 2.12 | 5.4% | 48.2 | 12/12 | 0.83 | 0.85 | 0.35 | 4 | 29.8% | 0.39 | 0.56 | 52.1% | 51.4% | 16.7% | 46.2%/37.3% | n/a (profitable_beyond_25.0x) | pass | 0.429 (unverified) | 0.86 |
| 23 | `cfg_1b41` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 34/61/63 | 158 | 44.0% | 7.6% | 0.99 | -10.8% | 311 | 1.74 | 7.9% | 70.0 | 11/11 | 0.91 | 0.81 | 0.18 | 4 | 26.3% | 0.33 | 0.57 | 42.7% | 41.8% | -0.2% | 38.2%/29.7% | 23.3 (interpolated) | pass | 0.250 (unverified) | 0.66 |
| 24 | `cfg_976c` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 23/88/35 | 146 | 38.4% | 6.7% | 1.23 | -5.0% | 290 | 1.71 | 8.6% | 65.5 | 10/10 | 0.90 | 0.87 | 0.36 | 5 | 27.6% | 0.25 | 0.45 | 37.8% | 36.3% | 4.2% | 32.6%/23.0% | 23.0 (interpolated) | pass | 0.466 (unverified) | 0.63 |
| 25 | `cfg_d882` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 14/72/85 | 171 | 33.9% | 6.0% | 1.10 | -4.4% | 282 | 1.59 | 7.8% | 76.4 | 10/10 | 1.00 | 0.94 | 0.16 | 5 | 19.8% | 0.38 | 0.59 | 33.3% | 31.9% | -2.6% | 31.8%/22.0% | 18.4 (interpolated) | pass | 0.333 (unverified) | 0.64 |
| 26 | `cfg_6669` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 13/80/36 | 129 | 40.5% | 7.0% | 1.24 | -4.4% | 141 | 1.79 | 7.6% | 56.2 | 12/12 | 0.92 | 0.89 | 0.34 | 5 | 25.4% | 0.34 | 0.56 | 40.0% | 39.7% | -2.5% | 35.4%/25.3% | n/a (profitable_beyond_25.0x) | pass | 0.464 (unverified) | 0.23 |
| 27 | `cfg_6de8` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 7/101/34 | 142 | 40.9% | 7.1% | 1.29 | -5.1% | 292 | 1.77 | 8.7% | 63.6 | 10/10 | 0.90 | 0.86 | 0.42 | 5 | 29.9% | 0.25 | 0.43 | 39.9% | 38.7% | 2.5% | 34.4%/25.6% | 24.4 (interpolated) | pass | 0.513 (unverified) | 0.69 |
| 28 | `cfg_902b` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 45/38/57 | 140 | 43.2% | 7.5% | 1.03 | -6.0% | 190 | 1.83 | 6.2% | 61.6 | 11/11 | 0.91 | 0.84 | 0.18 | 5 | 16.9% | 0.54 | 0.67 | 42.5% | 41.3% | 12.0% | 39.7%/28.7% | n/a (profitable_beyond_25.0x) | pass | 0.265 (unverified) | 0.72 |
| 29 | `cfg_12e6` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 32/51/33 | 116 | 22.3% | 4.1% | 1.20 | -3.3% | 248 | 2.24 | 1.6% | 52.2 | 11/11 | 0.73 | 0.59 | 0.61 | 4 | 9.5% | 0.57 | 0.45 | 21.2% | 20.6% | 13.0% | 18.6%/15.8% | 17.9 (interpolated) | pass | 0.419 (unverified) | 0.48 |
| 30 | `cfg_3e28` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 12/84/33 | 129 | 33.1% | 5.9% | 1.07 | -4.8% | 326 | 1.70 | 7.7% | 57.0 | 11/11 | 1.00 | 0.91 | 0.15 | 5 | 21.3% | 0.32 | 0.59 | 32.4% | 31.9% | -2.3% | 30.1%/20.9% | 22.9 (interpolated) | pass | 0.309 (unverified) | 0.78 |
| 31 | `cfg_0544` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 34/57/20 | 111 | 22.8% | 4.2% | 1.27 | -2.7% | 248 | 2.32 | 1.7% | 49.6 | 11/11 | 0.73 | 0.81 | 0.46 | 4 | 9.9% | 0.55 | 0.42 | 21.9% | 21.3% | 16.1% | 20.4%/16.8% | 19.0 (interpolated) | pass | 0.495 (unverified) | 0.52 |
| 32 | `cfg_d8bd` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 45/7/50 | 102 | 41.6% | 7.2% | 1.21 | -5.4% | 218 | 2.26 | 3.6% | 45.6 | 9/9 | 0.89 | 0.78 | 0.44 | 4 | 15.9% | 0.59 | 0.68 | 40.8% | 40.1% | -11.3% | 36.7%/28.4% | n/a (profitable_beyond_25.0x) | pass | 0.436 (unverified) | 0.40 |
| 33 | `cfg_8851` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 46/64/37 | 147 | 31.2% | 5.6% | 0.98 | -5.9% | 268 | 1.53 | 8.0% | 65.1 | 10/10 | 0.90 | 0.81 | 0.17 | 5 | 21.4% | 0.26 | 0.54 | 30.6% | 29.5% | 10.8% | 29.2%/21.0% | 19.0 (interpolated) | pass | 0.252 (unverified) | 0.66 |
| 34 | `cfg_eade` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 29/57/63 | 149 | 31.3% | 5.6% | 1.01 | -4.7% | 326 | 1.57 | 7.0% | 65.8 | 11/11 | 1.00 | 0.83 | 0.17 | 5 | 19.7% | 0.33 | 0.61 | 30.3% | 28.3% | -9.9% | 26.7%/21.0% | 19.0 (interpolated) | pass | 0.263 (unverified) | 0.06 |
| 35 | `cfg_c3f6` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 15/90/56 | 161 | 30.0% | 5.4% | 1.03 | -5.3% | 289 | 1.53 | 8.6% | 71.5 | 10/10 | 0.90 | 0.91 | 0.12 | 5 | 20.2% | 0.31 | 0.56 | 28.8% | 27.8% | -1.7% | 27.6%/19.5% | 17.2 (interpolated) | pass | 0.292 (unverified) | 0.58 |
| 36 | `cfg_0646` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 10/74/65 | 149 | 34.4% | 6.1% | 1.06 | -5.2% | 326 | 1.62 | 7.4% | 65.9 | 12/12 | 1.00 | 0.81 | 0.25 | 5 | 20.2% | 0.37 | 0.63 | 33.5% | 31.8% | -7.5% | 30.6%/21.7% | 20.8 (interpolated) | pass | 0.302 (unverified) | 0.09 |
| 37 | `cfg_f8d1` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 15/82/116 | 213 | 43.8% | 7.5% | 1.02 | -6.5% | 311 | 1.62 | 9.4% | 94.8 | 10/10 | 0.90 | 0.88 | 0.13 | 4 | 20.9% | 0.44 | 0.64 | 43.0% | 40.1% | -10.2% | 38.2%/30.3% | 17.5 (interpolated) | pass | 0.251 (unverified) | 0.62 |
| 38 | `cfg_69e3` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=15, entry_z=-3.5, exit_z=-1.0, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 66/6/67 | 139 | 17.4% | 3.3% | 0.96 | -4.1% | 208 | 1.53 | 3.0% | 61.1 | 10/10 | 0.80 | 0.55 | 0.41 | 4 | 10.4% | 0.41 | 0.54 | 16.9% | 15.9% | 20.7% | 17.0%/13.5% | 12.9 (interpolated) | pass | 0.224 (unverified) | 0.05 |
| 39 | `cfg_21fc` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 57/63/23 | 143 | 36.8% | 6.5% | 1.16 | -5.7% | 250 | 1.66 | 8.0% | 63.9 | 9/9 | 0.89 | 0.71 | 0.45 | 5 | 25.5% | 0.24 | 0.46 | 36.7% | 35.3% | 13.9% | 32.9%/23.6% | 22.5 (interpolated) | pass | 0.395 (unverified) | 0.83 |
| 40 | `cfg_aa56` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 3/72/33 | 108 | 33.1% | 5.9% | 1.02 | -3.7% | 188 | 1.72 | 6.4% | 47.4 | 11/11 | 1.00 | 0.79 | 0.23 | 4 | 20.6% | 0.36 | 0.66 | 32.2% | 31.6% | 4.4% | 31.3%/23.7% | n/a (profitable_beyond_25.0x) | pass | 0.260 (unverified) | 0.97 |
| 41 | `cfg_3bd2` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-1.75, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 10/87/116 | 213 | 45.0% | 7.7% | 1.04 | -6.4% | 301 | 1.64 | 9.5% | 94.8 | 9/9 | 0.89 | 0.88 | 0.16 | 4 | 21.3% | 0.44 | 0.64 | 43.1% | 40.8% | -10.2% | 40.0%/29.7% | 17.6 (interpolated) | pass | 0.267 (unverified) | 0.63 |
| 42 | `cfg_c982` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 3/72/33 | 108 | 33.1% | 5.9% | 1.02 | -3.7% | 188 | 1.72 | 6.4% | 47.4 | 11/11 | 1.00 | 0.80 | 0.22 | 4 | 20.6% | 0.36 | 0.66 | 32.2% | 31.6% | 4.4% | 30.3%/25.3% | n/a (profitable_beyond_25.0x) | pass | 0.260 (unverified) | 1.03 |
| 43 | `cfg_3c25` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 11/65/101 | 177 | 33.9% | 6.0% | 1.05 | -5.3% | 281 | 1.54 | 7.4% | 78.9 | 11/11 | 1.00 | 0.93 | 0.12 | 5 | 18.9% | 0.40 | 0.64 | 32.6% | 31.4% | -1.5% | 31.0%/23.3% | 17.6 (interpolated) | pass | 0.289 (unverified) | 0.52 |
| 44 | `cfg_a055` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 12/56/90 | 158 | 35.1% | 6.2% | 0.91 | -9.2% | 311 | 1.64 | 6.8% | 69.8 | 11/11 | 0.91 | 0.89 | 0.02 | 5 | 15.6% | 0.49 | 0.76 | 34.0% | 33.3% | -14.8% | 30.5%/22.8% | 19.6 (interpolated) | pass | 0.184 (unverified) | 0.91 |
| 45 | `cfg_8576` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 21/78/36 | 135 | 30.0% | 5.4% | 1.06 | -4.9% | 357 | 1.64 | 7.9% | 60.3 | 10/10 | 0.90 | 0.74 | 0.32 | 5 | 20.0% | 0.33 | 0.58 | 29.4% | 28.8% | 18.4% | 27.9%/19.9% | 20.0 (interpolated) | pass | 0.313 (unverified) | 0.39 |
| 46 | `cfg_9e7c` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 7/61/90 | 158 | 34.4% | 6.1% | 0.90 | -9.1% | 311 | 1.63 | 6.9% | 69.6 | 10/10 | 0.90 | 0.86 | 0.04 | 5 | 15.9% | 0.48 | 0.78 | 32.7% | 32.0% | -15.9% | 29.6%/21.1% | 19.3 (interpolated) | pass | 0.177 (unverified) | 0.93 |
| 47 | `cfg_2de6` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 19/58/100 | 177 | 33.7% | 6.0% | 1.05 | -5.3% | 281 | 1.54 | 7.3% | 79.0 | 11/11 | 1.00 | 0.93 | 0.12 | 5 | 18.3% | 0.42 | 0.64 | 32.1% | 31.2% | -3.5% | 30.2%/23.9% | 17.4 (interpolated) | pass | 0.290 (unverified) | 0.45 |
| 48 | `cfg_bfd9` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 35/58/91 | 184 | 29.0% | 5.2% | 0.95 | -5.7% | 328 | 1.45 | 8.0% | 82.2 | 8/8 | 0.75 | 0.79 | 0.16 | 4 | 17.8% | 0.33 | 0.58 | 27.2% | 26.5% | -6.8% | 26.2%/19.1% | 14.7 (interpolated) | pass | 0.220 (unverified) | 0.52 |
| 49 | `cfg_0b38` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=15, entry_z=-3.5, exit_z=-1.0, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 72/10/44 | 126 | 18.8% | 3.5% | 1.03 | -4.5% | 208 | 1.57 | 3.2% | 55.6 | 10/10 | 0.80 | 0.39 | 0.64 | 4 | 11.6% | 0.38 | 0.48 | 18.1% | 17.3% | 16.7% | 17.0%/13.9% | 14.8 (interpolated) | pass | 0.286 (unverified) | 0.10 |
| 50 | `cfg_50e5` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 31/31/65 | 127 | 16.1% | 3.0% | 1.33 | -1.3% | 237 | 1.95 | 1.4% | 56.3 | 10/10 | 0.90 | 0.61 | 0.72 | 5 | 10.0% | 0.34 | 0.49 | 15.4% | 14.7% | 11.5% | 14.2%/11.6% | 12.5 (interpolated) | pass | 0.563 (unverified) | 0.16 |
| 51 | `cfg_5fb1` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 3/102/56 | 161 | 32.0% | 5.7% | 1.09 | -5.3% | 289 | 1.56 | 8.7% | 71.4 | 9/9 | 0.89 | 0.73 | 0.36 | 5 | 21.4% | 0.31 | 0.53 | 31.1% | 29.7% | -2.9% | 27.9%/20.7% | 18.1 (interpolated) | pass | 0.340 (unverified) | 0.67 |
| 52 | `cfg_61c3` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 47/27/84 | 158 | 39.6% | 6.9% | 1.00 | -8.9% | 190 | 1.73 | 6.0% | 70.6 | 10/10 | 0.90 | 0.85 | 0.15 | 5 | 16.1% | 0.53 | 0.73 | 38.9% | 37.8% | -10.1% | 34.5%/24.6% | 21.1 (interpolated) | pass | 0.256 (unverified) | 0.71 |
| 53 | `cfg_7b2e` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 29/36/68 | 133 | 12.3% | 2.3% | 0.97 | -6.0% | 241 | 1.60 | 1.5% | 58.9 | 9/9 | 0.89 | 0.74 | 0.23 | 4 | 5.8% | 0.50 | 0.66 | 11.6% | 10.9% | 6.1% | 10.7%/8.8% | 9.8 (interpolated) | pass | 0.226 (unverified) | 0.18 |
| 54 | `cfg_18ee` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 29/20/53 | 102 | 41.4% | 7.2% | 1.19 | -4.4% | 218 | 2.19 | 4.2% | 45.6 | 10/10 | 0.90 | 0.80 | 0.39 | 4 | 18.9% | 0.50 | 0.62 | 40.8% | 40.1% | -16.1% | 36.9%/29.4% | n/a (profitable_beyond_25.0x) | pass | 0.405 (unverified) | 0.46 |
| 55 | `cfg_5cd8` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 32/64/40 | 136 | 31.9% | 5.7% | 1.03 | -5.7% | 276 | 1.58 | 7.4% | 60.6 | 10/10 | 0.90 | 0.60 | 0.43 | 5 | 20.6% | 0.33 | 0.53 | 30.7% | 29.9% | 9.9% | 28.7%/20.9% | 22.0 (interpolated) | pass | 0.287 (unverified) | 0.28 |
| 56 | `cfg_8728` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 30/61/39 | 130 | 17.2% | 3.2% | 0.96 | -5.1% | 241 | 1.79 | 1.9% | 56.8 | 10/10 | 0.90 | 0.61 | 0.35 | 4 | 4.4% | 0.76 | 0.58 | 16.0% | 15.2% | 11.1% | 15.2%/12.5% | 12.8 (interpolated) | pass | 0.211 (unverified) | 0.89 |
| 57 | `cfg_329a` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 30/69/26 | 125 | 15.9% | 3.0% | 0.89 | -5.0% | 241 | 1.70 | 1.9% | 54.6 | 10/10 | 0.90 | 0.62 | 0.27 | 4 | 3.6% | 0.78 | 0.59 | 15.3% | 14.5% | 13.2% | 14.6%/11.5% | 12.8 (interpolated) | pass | 0.173 (unverified) | 0.89 |
| 58 | `cfg_d8c7` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 23/39/68 | 130 | 34.0% | 6.0% | 0.94 | -7.2% | 242 | 1.73 | 5.7% | 58.1 | 10/10 | 1.00 | 0.88 | 0.06 | 5 | 22.0% | 0.35 | 0.63 | 32.5% | 32.2% | -11.2% | 30.7%/23.4% | 22.8 (interpolated) | pass | 0.220 (unverified) | 0.41 |
| 59 | `cfg_13d3` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 18/35/76 | 129 | 32.4% | 5.8% | 0.86 | -8.9% | 311 | 1.64 | 5.3% | 57.9 | 10/10 | 0.90 | 0.83 | 0.02 | 5 | 11.3% | 0.62 | 0.85 | 31.1% | 30.2% | -12.7% | 29.2%/20.1% | 22.0 (interpolated) | pass | 0.156 (unverified) | 0.81 |
| 60 | `cfg_237a` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 39/47/61 | 147 | 45.5% | 7.8% | 0.96 | -9.3% | 279 | 1.68 | 7.1% | 67.0 | 11/11 | 0.91 | 0.84 | 0.11 | 5 | 28.7% | 0.37 | 0.61 | 44.0% | 41.4% | 3.9% | 38.9%/30.1% | n/a (profitable_beyond_25.0x) | pass | 0.224 (unverified) | 0.54 |
| 61 | `cfg_68ad` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 30/35/52 | 117 | 33.8% | 6.0% | 0.88 | -8.0% | 141 | 1.65 | 5.4% | 52.7 | 11/11 | 0.91 | 0.84 | 0.04 | 4 | 12.8% | 0.60 | 0.78 | 33.1% | 32.3% | 2.0% | 29.9%/22.0% | n/a (profitable_beyond_25.0x) | pass | 0.160 (unverified) | 0.70 |
| 62 | `cfg_3a13` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 27/66/99 | 192 | 23.7% | 4.3% | 0.91 | -4.6% | 141 | 1.42 | 8.1% | 84.5 | 10/10 | 0.80 | 0.62 | 0.28 | 5 | 16.7% | 0.30 | 0.70 | 22.6% | 21.4% | -6.2% | 22.4%/15.7% | 12.1 (interpolated) | pass | 0.203 (unverified) | 0.35 |
| 63 | `cfg_e77b` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 13/77/90 | 180 | 29.3% | 5.3% | 0.93 | -6.0% | 375 | 1.46 | 8.2% | 80.3 | 9/9 | 0.89 | 0.86 | 0.08 | 4 | 19.2% | 0.31 | 0.65 | 28.4% | 27.4% | -6.1% | 26.2%/18.0% | 15.6 (interpolated) | pass | 0.210 (unverified) | 0.49 |
| 64 | `cfg_088e` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 24/74/107 | 205 | 46.9% | 8.0% | 0.96 | -6.8% | 238 | 1.61 | 9.1% | 91.5 | 9/9 | 0.89 | 0.83 | 0.13 | 5 | 19.0% | 0.53 | 0.58 | 45.7% | 44.3% | -8.0% | 40.1%/26.6% | 19.4 (interpolated) | pass | 0.234 (unverified) | 0.65 |
| 65 | `cfg_b4e2` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 11/89/34 | 134 | 24.7% | 4.5% | 0.86 | -7.0% | 757 | 1.46 | 7.9% | 60.4 | 9/9 | 0.89 | 0.79 | 0.07 | 4 | 15.7% | 0.34 | 0.64 | 23.9% | 22.7% | -8.1% | 22.7%/12.9% | 17.3 (interpolated) | pass | 0.181 (unverified) | 0.37 |
| 66 | `cfg_0ef9` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 28/155/0 | 183 | 25.4% | 4.6% | 0.97 | -4.0% | 207 | 1.72 | 3.3% | 81.1 | 10/10 | 0.90 | 0.52 | 0.45 | 4 | 9.7% | 0.58 | 0.59 | 24.5% | 23.6% | 19.8% | 22.6%/15.8% | 13.7 (interpolated) | pass | 0.206 (unverified) | 0.99 |
| 67 | `cfg_ed80` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 24/56/80 | 160 | 48.5% | 8.2% | 1.00 | -10.0% | 130 | 1.79 | 7.1% | 72.7 | 10/10 | 0.90 | 0.85 | 0.14 | 5 | 27.7% | 0.36 | 0.58 | 47.4% | 45.5% | -9.7% | 40.6%/31.8% | 24.2 (interpolated) | pass | 0.259 (unverified) | 0.72 |
| 68 | `cfg_3534` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 24/61/60 | 145 | 44.2% | 7.6% | 0.90 | -10.9% | 279 | 1.68 | 7.3% | 66.0 | 11/11 | 0.91 | 0.83 | 0.07 | 5 | 27.7% | 0.37 | 0.63 | 41.9% | 41.0% | 3.1% | 38.0%/29.9% | 24.9 (interpolated) | pass | 0.196 (unverified) | 0.58 |
| 69 | `cfg_b592` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-1.75, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 17/81/107 | 205 | 47.4% | 8.1% | 0.97 | -6.8% | 238 | 1.62 | 9.3% | 91.4 | 8/8 | 0.88 | 0.76 | 0.21 | 5 | 19.2% | 0.53 | 0.57 | 46.3% | 45.0% | -9.4% | 42.2%/30.0% | 19.7 (interpolated) | pass | 0.239 (unverified) | 0.58 |
| 70 | `cfg_49c6` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 48/46/55 | 149 | 38.3% | 6.7% | 0.90 | -5.8% | 273 | 1.47 | 12.8% | 66.5 | 12/12 | 0.83 | 0.60 | 0.30 | 4 | 22.4% | 0.39 | 0.74 | 38.2% | 36.8% | 35.7% | 35.1%/25.0% | 23.2 (interpolated) | pass | 0.197 (unverified) | 0.58 |
| 71 | `cfg_05cd` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 60/28/74 | 162 | 36.0% | 6.3% | 0.87 | -5.4% | 297 | 1.46 | 11.6% | 71.5 | 12/12 | 0.83 | 0.58 | 0.30 | 4 | 21.4% | 0.37 | 0.72 | 35.5% | 34.3% | 35.0% | 33.3%/23.1% | 19.6 (interpolated) | pass | 0.177 (unverified) | 0.81 |
| 72 | `cfg_854a` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-2.0, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 2/59/67 | 128 | 31.1% | 5.6% | 0.87 | -7.5% | 183 | 1.68 | 6.0% | 56.9 | 9/9 | 1.00 | 0.85 | 0.03 | 5 | 19.4% | 0.37 | 0.67 | 30.0% | 29.1% | -10.5% | 27.9%/20.4% | 20.9 (interpolated) | pass | 0.175 (unverified) | 0.45 |
| 73 | `cfg_ad5d` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=15, entry_z=-1.75, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 4/87/59 | 150 | 28.8% | 5.2% | 0.97 | -7.1% | 421 | 1.53 | 7.9% | 66.7 | 9/9 | 0.89 | 0.85 | 0.11 | 4 | 17.3% | 0.34 | 0.70 | 26.2% | 25.1% | -8.3% | 25.1%/16.3% | 17.1 (interpolated) | pass | 0.249 (unverified) | 0.68 |
| 74 | `cfg_1025` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=15, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 5/86/59 | 150 | 28.9% | 5.2% | 0.97 | -7.1% | 421 | 1.53 | 7.9% | 66.7 | 10/10 | 0.90 | 0.88 | 0.09 | 4 | 17.4% | 0.34 | 0.70 | 26.3% | 25.2% | -8.4% | 25.0%/18.7% | 17.2 (interpolated) | pass | 0.251 (unverified) | 0.67 |
| 75 | `cfg_7754` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 12/79/100 | 191 | 23.5% | 4.3% | 0.88 | -4.6% | 246 | 1.41 | 8.3% | 84.2 | 11/11 | 0.82 | 0.83 | 0.05 | 5 | 16.2% | 0.31 | 0.73 | 22.6% | 20.7% | -7.1% | 23.1%/15.7% | 12.2 (interpolated) | pass | 0.184 (unverified) | 0.44 |
| 76 | `cfg_44a9` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 47/4/49 | 100 | 14.9% | 2.8% | 0.91 | -4.3% | 208 | 1.64 | 2.2% | 44.1 | 12/12 | 0.83 | 0.36 | 0.55 | 3 | 5.9% | 0.60 | 0.65 | 14.3% | 13.8% | 14.8% | 13.7%/11.3% | 14.7 (interpolated) | pass | 0.182 (unverified) | -0.24 |
| 77 | `cfg_cb84` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 31/76/124 | 231 | 27.5% | 5.0% | 0.80 | -6.5% | 243 | 1.37 | 9.9% | 102.3 | 10/10 | 0.90 | 0.65 | 0.15 | 5 | 19.9% | 0.25 | 0.75 | 25.3% | 23.5% | -11.2% | 23.7%/15.4% | 11.2 (interpolated) | pass | 0.138 (unverified) | 0.70 |
| 78 | `cfg_bc34` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=15, entry_confirmation=none, stop_atr_multiple=1.5 | 112/17/130 | 259 | 26.3% | 4.8% | 0.92 | -4.6% | 345 | 1.40 | 4.9% | 115.5 | 10/10 | 1.00 | 0.43 | 0.49 | 3 | 3.7% | 0.84 | 0.62 | 25.1% | 23.9% | 19.4% | 22.8%/16.3% | 10.5 (interpolated) | pass | 0.232 (unverified) | 0.01 |
| 79 | `cfg_d889` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 34/57/103 | 194 | 33.3% | 5.9% | 0.89 | -7.1% | 311 | 1.50 | 8.5% | 86.7 | 9/9 | 1.00 | 0.75 | 0.14 | 4 | 18.5% | 0.40 | 0.65 | 32.1% | 31.2% | -13.6% | 30.8%/23.8% | 16.2 (interpolated) | pass | 0.174 (unverified) | 0.67 |
| 80 | `cfg_638d` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 37/146/0 | 183 | 24.1% | 4.4% | 0.93 | -4.0% | 207 | 1.69 | 3.2% | 80.9 | 9/9 | 0.89 | 0.47 | 0.46 | 4 | 8.3% | 0.62 | 0.62 | 23.3% | 22.3% | 17.8% | 21.4%/14.7% | 13.1 (interpolated) | pass | 0.179 (unverified) | 0.99 |
| 81 | `cfg_2ac6` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 43/10/53 | 106 | 48.1% | 8.2% | 1.02 | -10.9% | 311 | 1.90 | 6.8% | 47.5 | 13/13 | 0.92 | 0.79 | 0.23 | 4 | 28.0% | 0.33 | 0.61 | 47.2% | 46.7% | 16.6% | 43.0%/35.0% | n/a (profitable_beyond_25.0x) | pass | 0.272 (unverified) | 0.99 |
| 82 | `cfg_5130` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 21/43/69 | 133 | 12.2% | 2.3% | 0.97 | -6.0% | 241 | 1.60 | 1.6% | 58.9 | 10/10 | 0.90 | 0.66 | 0.30 | 4 | 5.8% | 0.49 | 0.66 | 11.5% | 10.8% | 5.2% | 10.9%/8.5% | 9.9 (interpolated) | pass | 0.227 (unverified) | 0.20 |
| 83 | `cfg_2d4a` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 21/82/35 | 138 | 21.4% | 4.0% | 0.79 | -6.4% | 804 | 1.40 | 7.9% | 62.3 | 9/9 | 0.89 | 0.79 | 0.00 | 4 | 12.5% | 0.37 | 0.60 | 20.8% | 20.2% | -5.2% | 20.2%/14.5% | 14.3 (interpolated) | pass | 0.149 (unverified) | 0.25 |
| 84 | `cfg_4707` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 40/7/65 | 112 | 44.2% | 7.6% | 1.03 | -8.0% | 311 | 1.91 | 5.9% | 50.6 | 12/12 | 0.83 | 0.74 | 0.29 | 4 | 26.2% | 0.32 | 0.64 | 43.2% | 42.9% | -2.5% | 39.2%/29.5% | n/a (profitable_beyond_25.0x) | pass | 0.275 (unverified) | 0.79 |
| 85 | `cfg_7f69` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 20/84/36 | 140 | 23.8% | 4.4% | 0.81 | -5.8% | 290 | 1.43 | 8.2% | 61.7 | 11/11 | 0.91 | 0.79 | 0.02 | 5 | 14.8% | 0.33 | 0.70 | 23.1% | 22.3% | 0.4% | 20.8%/12.9% | 15.8 (interpolated) | pass | 0.150 (unverified) | 0.66 |
| 86 | `cfg_f913` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=15, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 5/93/22 | 120 | 29.0% | 5.2% | 0.93 | -9.4% | 270 | 1.56 | 7.6% | 53.2 | 10/10 | 0.90 | 0.81 | 0.12 | 5 | 15.0% | 0.42 | 0.70 | 28.0% | 26.1% | 3.6% | 25.6%/19.3% | 21.5 (interpolated) | pass | 0.228 (unverified) | 1.04 |
| 87 | `cfg_98c9` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=15, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 7/91/22 | 120 | 27.8% | 5.0% | 0.90 | -9.4% | 270 | 1.54 | 7.6% | 53.3 | 10/10 | 0.90 | 0.77 | 0.12 | 5 | 13.9% | 0.44 | 0.71 | 26.5% | 25.3% | 2.9% | 24.6%/18.2% | 21.3 (interpolated) | pass | 0.206 (unverified) | 0.96 |
| 88 | `cfg_b861` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 28/64/16 | 108 | 32.9% | 5.9% | 0.91 | -11.1% | 408 | 1.72 | 6.6% | 48.6 | 10/10 | 0.90 | 0.58 | 0.33 | 4 | 16.9% | 0.42 | 0.57 | 31.1% | 31.3% | 12.7% | 30.3%/20.8% | n/a (profitable_beyond_25.0x) | pass | 0.232 (unverified) | 0.33 |
| 89 | `cfg_59a6` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 41/19/48 | 108 | 34.2% | 6.1% | 0.84 | -5.6% | 297 | 1.68 | 7.7% | 48.0 | 12/12 | 1.00 | 0.56 | 0.27 | 5 | 14.9% | 0.52 | 0.79 | 33.8% | 33.1% | 35.0% | 30.8%/23.1% | n/a (profitable_beyond_25.0x) | pass | 0.139 (unverified) | 0.52 |
| 90 | `cfg_3694` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 23/86/123 | 232 | 40.0% | 7.0% | 0.84 | -7.0% | 386 | 1.51 | 10.4% | 102.2 | 10/10 | 0.90 | 0.74 | 0.10 | 5 | 14.0% | 0.59 | 0.67 | 38.6% | 36.8% | -9.0% | 34.9%/25.1% | 15.3 (interpolated) | pass | 0.157 (unverified) | 0.35 |
| 91 | `cfg_1035` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 35/75/122 | 232 | 40.1% | 7.0% | 0.84 | -7.0% | 403 | 1.51 | 10.3% | 102.2 | 10/10 | 0.90 | 0.71 | 0.13 | 5 | 13.6% | 0.60 | 0.68 | 38.6% | 36.5% | -6.4% | 36.1%/25.5% | 15.5 (interpolated) | pass | 0.155 (unverified) | 0.27 |
| 92 | `cfg_f2a7` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 29/69/34 | 132 | 23.5% | 4.3% | 0.82 | -5.4% | 737 | 1.46 | 7.5% | 59.4 | 9/9 | 0.78 | 0.83 | -0.01 | 5 | 14.6% | 0.33 | 0.57 | 22.4% | 21.6% | -3.0% | 20.1%/13.1% | 16.4 (interpolated) | pass | 0.160 (unverified) | 0.29 |
| 93 | `cfg_30fc` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 16/74/103 | 193 | 31.9% | 5.7% | 0.86 | -7.7% | 311 | 1.48 | 8.8% | 85.7 | 9/9 | 1.00 | 0.75 | 0.11 | 4 | 18.3% | 0.38 | 0.70 | 30.5% | 29.7% | -16.0% | 29.9%/22.1% | 15.7 (interpolated) | pass | 0.155 (unverified) | 0.62 |
| 94 | `cfg_71e9` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 11/85/34 | 130 | 27.0% | 4.9% | 0.88 | -6.4% | 579 | 1.52 | 7.7% | 58.3 | 10/10 | 0.80 | 0.82 | 0.07 | 5 | 17.7% | 0.32 | 0.62 | 25.8% | 25.7% | -7.1% | 22.9%/15.2% | 18.8 (interpolated) | pass | 0.194 (unverified) | 0.43 |
| 95 | `cfg_4d18` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 40/41/82 | 163 | 41.1% | 7.1% | 0.86 | -12.9% | 161 | 1.64 | 6.9% | 73.4 | 10/10 | 0.90 | 0.83 | 0.04 | 5 | 25.9% | 0.37 | 0.64 | 39.9% | 37.6% | -10.4% | 35.4%/25.1% | 20.8 (interpolated) | pass | 0.175 (unverified) | 0.71 |
| 96 | `cfg_9566` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 1/55/71 | 127 | 29.0% | 5.2% | 0.91 | -6.2% | 157 | 1.62 | 5.6% | 56.7 | 9/9 | 0.78 | 0.60 | 0.31 | 5 | 17.6% | 0.34 | 0.66 | 27.9% | 27.2% | -6.0% | 26.0%/13.4% | 21.3 (interpolated) | pass | 0.190 (unverified) | 0.17 |
| 97 | `cfg_3497` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 33/82/36 | 151 | 21.6% | 4.0% | 0.81 | -6.1% | 321 | 1.42 | 8.6% | 67.3 | 9/9 | 0.89 | 0.62 | 0.18 | 4 | 12.5% | 0.38 | 0.70 | 20.5% | 19.8% | 10.3% | 21.1%/14.9% | 13.8 (interpolated) | pass | 0.153 (unverified) | 0.52 |
| 98 | `cfg_ea75` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=1.0, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 85/82/0 | 167 | 27.3% | 5.0% | 0.87 | -4.8% | 213 | 1.66 | 6.9% | 74.4 | 8/8 | 0.88 | 0.22 | 0.65 | 5 | 14.2% | 0.45 | 0.36 | 26.4% | 25.2% | 33.4% | 25.1%/20.2% | 15.5 (interpolated) | pass | 0.163 (unverified) | 0.42 |
| 99 | `cfg_a317` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 43/23/36 | 102 | 35.6% | 6.3% | 0.86 | -4.9% | 276 | 1.70 | 8.4% | 45.1 | 12/12 | 1.00 | 0.67 | 0.19 | 5 | 14.9% | 0.55 | 0.77 | 35.1% | 34.1% | 28.5% | 31.3%/22.1% | n/a (profitable_beyond_25.0x) | pass | 0.151 (unverified) | 0.39 |
| 100 | `cfg_89f3` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 63/10/63 | 136 | 18.9% | 3.5% | 0.89 | -6.1% | 241 | 1.59 | 2.7% | 60.6 | 10/10 | 1.00 | 0.60 | 0.29 | 4 | 4.7% | 0.78 | 0.58 | 18.1% | 17.4% | 12.7% | 17.3%/13.1% | 13.3 (interpolated) | pass | 0.166 (unverified) | 0.30 |
| 101 | `cfg_204e` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 21/81/64 | 166 | 23.2% | 4.3% | 0.77 | -6.4% | 290 | 1.37 | 8.5% | 73.5 | 11/11 | 0.91 | 0.72 | 0.04 | 4 | 13.9% | 0.35 | 0.71 | 22.3% | 20.5% | -10.0% | 21.3%/14.6% | 13.0 (interpolated) | pass | 0.131 (unverified) | 0.69 |
| 102 | `cfg_9737` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 3/53/71 | 127 | 28.9% | 5.2% | 0.91 | -6.2% | 157 | 1.62 | 5.6% | 56.7 | 10/10 | 0.90 | 0.70 | 0.21 | 5 | 17.5% | 0.34 | 0.65 | 27.9% | 27.1% | -5.1% | 25.2%/12.4% | 21.3 (interpolated) | pass | 0.190 (unverified) | 0.16 |
| 103 | `cfg_b5cc` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 31/83/0 | 114 | 15.4% | 2.9% | 0.89 | -3.4% | 241 | 1.83 | 2.0% | 50.2 | 9/9 | 0.78 | 0.71 | 0.19 | 4 | 6.8% | 0.54 | 0.53 | 14.8% | 14.0% | 16.8% | 13.0%/9.1% | 13.3 (interpolated) | pass | 0.188 (unverified) | 1.23 |
| 104 | `cfg_caff` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 3/44/54 | 101 | 37.2% | 6.5% | 1.04 | -7.7% | 194 | 2.01 | 4.4% | 44.9 | 10/10 | 0.90 | 0.69 | 0.34 | 5 | 17.1% | 0.52 | 0.79 | 36.7% | 36.1% | -8.8% | 33.2%/27.0% | n/a (profitable_beyond_25.0x) | pass | 0.278 (unverified) | 0.72 |
| 105 | `cfg_9693` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 3/44/54 | 101 | 37.2% | 6.5% | 1.04 | -7.7% | 194 | 2.01 | 4.4% | 44.9 | 11/11 | 0.91 | 0.72 | 0.32 | 5 | 17.1% | 0.52 | 0.79 | 36.7% | 36.1% | -8.8% | 34.4%/24.7% | n/a (profitable_beyond_25.0x) | pass | 0.278 (unverified) | 0.72 |
| 106 | `cfg_0364` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 25/68/34 | 127 | 25.8% | 4.7% | 0.93 | -4.8% | 305 | 1.53 | 7.3% | 55.8 | 9/9 | 0.89 | 0.69 | 0.24 | 5 | 14.1% | 0.40 | 0.54 | 25.2% | 24.4% | -0.9% | 22.6%/13.7% | 18.3 (interpolated) | pass | 0.221 (unverified) | 0.45 |
| 107 | `cfg_99db` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 17/75/34 | 126 | 26.5% | 4.8% | 0.94 | -4.9% | 305 | 1.54 | 7.4% | 55.8 | 10/10 | 0.80 | 0.78 | 0.16 | 4 | 14.7% | 0.44 | 0.52 | 25.8% | 24.5% | 0.8% | 22.7%/13.6% | 19.1 (interpolated) | pass | 0.230 (unverified) | 0.41 |
| 108 | `cfg_8625` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 27/76/30 | 133 | 21.8% | 4.0% | 0.83 | -6.7% | 185 | 1.46 | 7.7% | 59.1 | 10/10 | 0.90 | 0.68 | 0.16 | 4 | 11.6% | 0.42 | 0.69 | 21.2% | 19.9% | 8.6% | 21.5%/15.9% | 15.1 (interpolated) | pass | 0.171 (unverified) | 0.45 |
| 109 | `cfg_8e2a` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=20, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 35/50/100 | 185 | 27.2% | 4.9% | 0.92 | -6.6% | 282 | 1.43 | 7.4% | 81.3 | 8/8 | 0.88 | 0.76 | 0.16 | 4 | 16.4% | 0.34 | 0.62 | 25.2% | 24.2% | -7.0% | 24.4%/16.9% | 14.2 (interpolated) | pass | 0.213 (unverified) | 0.43 |
| 110 | `cfg_9032` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 10/80/94 | 184 | 24.0% | 4.4% | 0.86 | -5.6% | 321 | 1.39 | 8.2% | 82.1 | 8/8 | 0.75 | 0.80 | 0.06 | 5 | 16.4% | 0.27 | 0.70 | 22.6% | 21.7% | -6.3% | 22.2%/15.1% | 12.5 (interpolated) | pass | 0.169 (unverified) | 0.29 |
| 111 | `cfg_9bfa` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 46/63/133 | 242 | 35.7% | 6.3% | 0.85 | -8.0% | 510 | 1.44 | 10.0% | 107.2 | 10/10 | 0.90 | 0.61 | 0.24 | 4 | 13.3% | 0.56 | 0.73 | 34.1% | 31.5% | -15.1% | 32.6%/23.2% | 13.4 (interpolated) | pass | 0.142 (unverified) | 0.70 |
| 112 | `cfg_8214` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-1.75, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 93/45/0 | 138 | 37.8% | 6.6% | 0.97 | -6.7% | 268 | 1.80 | 12.2% | 61.1 | 9/9 | 0.89 | 0.64 | 0.33 | 4 | 21.4% | 0.36 | 0.38 | 36.9% | 36.0% | 12.5% | 32.2%/24.4% | 24.0 (interpolated) | pass | 0.246 (unverified) | 0.65 |
| 113 | `cfg_274c` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 27/75/35 | 137 | 26.6% | 4.8% | 0.97 | -5.2% | 260 | 1.54 | 8.0% | 61.3 | 9/9 | 0.89 | 0.76 | 0.20 | 5 | 17.4% | 0.29 | 0.63 | 25.6% | 24.7% | 6.6% | 23.8%/17.0% | 18.1 (interpolated) | pass | 0.241 (unverified) | 0.45 |
| 114 | `cfg_6f44` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 18/63/88 | 169 | 37.1% | 6.5% | 0.98 | -6.8% | 274 | 1.60 | 7.6% | 75.5 | 10/10 | 1.00 | 0.71 | 0.27 | 5 | 22.2% | 0.33 | 0.57 | 35.3% | 34.5% | -9.8% | 33.5%/22.4% | 20.3 (interpolated) | pass | 0.240 (unverified) | 0.91 |
| 115 | `cfg_6d0f` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 20/92/33 | 145 | 21.1% | 3.9% | 0.79 | -6.3% | 292 | 1.41 | 8.6% | 64.9 | 10/10 | 0.90 | 0.69 | 0.10 | 5 | 12.8% | 0.38 | 0.71 | 20.0% | 18.9% | 4.9% | 20.3%/14.3% | 14.5 (interpolated) | pass | 0.144 (unverified) | 0.58 |
| 116 | `cfg_05cd` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 35/54/100 | 189 | 28.1% | 5.1% | 0.91 | -6.8% | 279 | 1.40 | 8.0% | 84.7 | 9/9 | 0.89 | 0.69 | 0.22 | 4 | 15.7% | 0.44 | 0.64 | 27.1% | 25.8% | -4.1% | 25.1%/17.5% | 14.4 (interpolated) | pass | 0.195 (unverified) | 0.43 |
| 117 | `cfg_ba40` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 33/48/99 | 180 | 30.3% | 5.4% | 0.95 | -6.9% | 328 | 1.46 | 7.4% | 79.3 | 9/9 | 1.00 | 0.46 | 0.49 | 3 | 19.3% | 0.37 | 0.60 | 29.5% | 27.8% | -11.7% | 27.2%/18.6% | 16.1 (interpolated) | pass | 0.226 (unverified) | 0.21 |
| 118 | `cfg_96af` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 103/33/123 | 259 | 25.1% | 4.6% | 0.91 | -4.6% | 328 | 1.41 | 4.5% | 115.3 | 11/11 | 1.00 | 0.46 | 0.44 | 3 | 6.2% | 0.73 | 0.60 | 23.9% | 21.5% | 18.5% | 21.1%/16.0% | 9.9 (interpolated) | pass | 0.193 (unverified) | -0.15 |
| 119 | `cfg_f556` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 10/87/38 | 135 | 26.5% | 4.8% | 0.94 | -4.9% | 357 | 1.54 | 8.1% | 60.7 | 10/10 | 0.90 | 0.73 | 0.21 | 5 | 17.4% | 0.31 | 0.65 | 25.8% | 25.4% | 15.4% | 24.8%/18.9% | 18.1 (interpolated) | pass | 0.224 (unverified) | 0.35 |
| 120 | `cfg_0392` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-1.75, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 60/7/114 | 181 | 36.5% | 6.4% | 0.84 | -9.1% | 311 | 1.50 | 8.8% | 80.4 | 11/11 | 0.91 | 0.79 | 0.05 | 4 | 20.2% | 0.41 | 0.71 | 34.4% | 32.4% | -12.1% | 30.0%/21.3% | 17.7 (interpolated) | pass | 0.149 (unverified) | 0.54 |
| 121 | `cfg_f57c` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=0.5, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 108/59/0 | 167 | 25.1% | 4.6% | 0.89 | -4.8% | 357 | 1.68 | 6.4% | 74.2 | 9/9 | 1.00 | 0.31 | 0.57 | 5 | 12.7% | 0.46 | 0.33 | 24.3% | 23.3% | 29.5% | 22.9%/19.3% | 14.6 (interpolated) | pass | 0.186 (unverified) | 0.15 |
| 122 | `cfg_abdf` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=15, entry_z=-3.5, exit_z=-1.0, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 60/3/117 | 180 | 14.8% | 2.8% | 1.03 | -2.7% | 208 | 1.50 | 2.6% | 78.9 | 9/9 | 0.56 | 0.58 | 0.44 | 4 | 6.6% | 0.52 | 0.56 | 13.8% | 12.8% | 17.7% | 13.8%/10.8% | 8.3 (interpolated) | pass | 0.279 (unverified) | -0.31 |
| 123 | `cfg_75ff` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 54/18/50 | 122 | 18.4% | 3.4% | 0.98 | -4.7% | 248 | 1.73 | 2.2% | 54.7 | 12/12 | 0.83 | 0.55 | 0.43 | 4 | 7.8% | 0.58 | 0.52 | 17.5% | 16.5% | 14.3% | 16.4%/14.1% | 14.6 (interpolated) | pass | 0.225 (unverified) | 0.15 |
| 124 | `cfg_cfbb` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 26/69/40 | 135 | 41.2% | 7.1% | 0.83 | -13.2% | 243 | 1.63 | 7.7% | 60.2 | 11/11 | 0.91 | 0.77 | 0.06 | 5 | 25.0% | 0.39 | 0.64 | 39.2% | 37.5% | 14.6% | 35.6%/26.9% | 24.8 (interpolated) | pass | 0.166 (unverified) | 0.73 |
| 125 | `cfg_4a22` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 19/84/99 | 202 | 24.0% | 4.4% | 0.87 | -5.2% | 173 | 1.40 | 9.1% | 89.2 | 10/10 | 0.80 | 0.72 | 0.16 | 5 | 18.6% | 0.22 | 0.66 | 22.9% | 22.1% | -8.6% | 23.8%/15.9% | 11.9 (interpolated) | pass | 0.180 (unverified) | 0.41 |
| 126 | `cfg_f294` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 40/57/39 | 136 | 38.7% | 6.8% | 0.79 | -13.8% | 243 | 1.57 | 7.6% | 60.7 | 11/11 | 0.91 | 0.77 | 0.03 | 5 | 23.2% | 0.40 | 0.66 | 38.2% | 38.3% | 7.8% | 34.4%/27.4% | 24.8 (interpolated) | pass | 0.148 (unverified) | 0.59 |
| 127 | `cfg_be22` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 28/62/31 | 121 | 33.2% | 5.9% | 0.97 | -6.9% | 116 | 1.64 | 6.9% | 54.2 | 10/10 | 0.90 | 0.70 | 0.27 | 5 | 18.8% | 0.37 | 0.57 | 32.0% | 30.8% | -3.8% | 27.2%/19.0% | 24.1 (interpolated) | pass | 0.258 (unverified) | 0.25 |
| 128 | `cfg_f560` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 72/35/54 | 161 | 53.7% | 9.0% | 0.89 | -12.2% | 316 | 1.60 | 13.3% | 71.4 | 13/13 | 0.85 | 0.58 | 0.31 | 5 | 29.0% | 0.36 | 0.57 | 52.4% | 51.3% | 42.1% | 46.8%/36.6% | n/a (profitable_beyond_25.0x) | pass | 0.200 (unverified) | 0.42 |
| 129 | `cfg_474c` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 35/67/0 | 102 | 21.8% | 4.0% | 1.17 | -3.1% | 112 | 2.48 | 1.7% | 45.4 | 10/10 | 0.80 | 0.63 | 0.54 | 5 | 10.5% | 0.50 | 0.44 | 21.2% | 20.6% | 13.8% | 19.1%/15.9% | 20.0 (interpolated) | pass | 0.392 (unverified) | 0.73 |
| 130 | `cfg_732d` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 69/6/81 | 156 | 41.2% | 7.2% | 0.84 | -8.3% | 255 | 1.56 | 8.0% | 69.7 | 12/12 | 0.92 | 0.69 | 0.16 | 4 | 15.9% | 0.56 | 0.71 | 40.6% | 38.9% | 13.0% | 37.6%/26.3% | 23.4 (interpolated) | pass | 0.158 (unverified) | 0.46 |
| 131 | `cfg_fa98` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 19/58/31 | 108 | 37.8% | 6.6% | 0.81 | -11.9% | 153 | 1.68 | 6.3% | 48.5 | 11/11 | 0.91 | 0.81 | 0.00 | 5 | 19.3% | 0.45 | 0.74 | 36.7% | 35.9% | -0.9% | 33.2%/23.7% | n/a (profitable_beyond_25.0x) | pass | 0.157 (unverified) | 0.92 |
| 132 | `cfg_b85e` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 63/5/103 | 171 | 35.5% | 6.3% | 0.83 | -11.0% | 265 | 1.52 | 7.2% | 76.5 | 11/11 | 0.91 | 0.69 | 0.14 | 4 | 13.8% | 0.56 | 0.80 | 34.7% | 33.2% | -5.8% | 30.9%/24.0% | 18.1 (interpolated) | pass | 0.141 (unverified) | 0.39 |
| 133 | `cfg_cfc0` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 21/78/25 | 124 | 22.9% | 4.2% | 0.87 | -6.3% | 373 | 1.56 | 7.5% | 55.6 | 10/10 | 0.90 | 0.73 | 0.14 | 5 | 13.1% | 0.43 | 0.56 | 22.1% | 21.3% | 27.7% | 21.2%/14.1% | 17.2 (interpolated) | pass | 0.191 (unverified) | 0.60 |
| 134 | `cfg_ca76` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 117/28/0 | 145 | 37.5% | 6.6% | 1.01 | -5.5% | 194 | 1.87 | 11.2% | 64.2 | 8/8 | 0.88 | 0.55 | 0.47 | 4 | 21.8% | 0.35 | 0.34 | 36.6% | 35.6% | 15.6% | 33.5%/25.8% | 22.2 (interpolated) | pass | 0.278 (unverified) | 0.72 |
| 135 | `cfg_cee9` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 4/89/61 | 154 | 20.4% | 3.8% | 0.80 | -5.4% | 307 | 1.39 | 8.0% | 68.6 | 12/12 | 0.83 | 0.60 | 0.20 | 5 | 13.8% | 0.31 | 0.85 | 19.6% | 18.8% | -7.6% | 19.6%/14.2% | 13.5 (interpolated) | pass | 0.146 (unverified) | 0.26 |
| 136 | `cfg_a09d` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 66/51/80 | 197 | 25.6% | 4.7% | 0.80 | -6.5% | 529 | 1.41 | 9.1% | 86.9 | 9/9 | 0.89 | 0.64 | 0.16 | 4 | 16.6% | 0.35 | 0.57 | 24.5% | 22.8% | -6.4% | 21.6%/15.2% | 12.2 (interpolated) | pass | 0.143 (unverified) | 0.54 |
| 137 | `cfg_9d18` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 17/76/39 | 132 | 27.8% | 5.0% | 0.91 | -5.9% | 290 | 1.52 | 7.5% | 59.0 | 11/11 | 0.91 | 0.54 | 0.38 | 5 | 15.9% | 0.40 | 0.70 | 27.3% | 26.5% | 7.3% | 25.8%/17.5% | 19.9 (interpolated) | pass | 0.198 (unverified) | 0.19 |
| 138 | `cfg_aa38` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 8/106/0 | 114 | 13.9% | 2.6% | 0.79 | -3.6% | 241 | 1.70 | 2.1% | 50.6 | 9/9 | 0.89 | 0.65 | 0.14 | 4 | 5.5% | 0.59 | 0.62 | 13.0% | 12.5% | 17.8% | 12.5%/9.2% | 12.0 (interpolated) | pass | 0.127 (unverified) | 1.30 |
| 139 | `cfg_f17b` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 34/44/30 | 108 | 35.4% | 6.3% | 0.81 | -11.4% | 159 | 1.65 | 5.9% | 48.3 | 11/11 | 0.91 | 0.81 | -0.00 | 5 | 20.1% | 0.40 | 0.70 | 35.1% | 34.0% | 0.9% | 31.9%/23.3% | n/a (profitable_beyond_25.0x) | pass | 0.158 (unverified) | 0.89 |
| 140 | `cfg_5b5b` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 4/85/95 | 184 | 22.0% | 4.1% | 0.79 | -5.7% | 321 | 1.35 | 8.4% | 82.3 | 8/8 | 0.75 | 0.83 | -0.04 | 5 | 14.5% | 0.30 | 0.77 | 21.0% | 19.9% | -7.0% | 20.1%/13.2% | 11.8 (interpolated) | pass | 0.134 (unverified) | 0.36 |
| 141 | `cfg_c7c6` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=15, entry_z=-3.5, exit_z=-1.0, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 61/5/97 | 163 | 13.4% | 2.5% | 0.86 | -4.3% | 208 | 1.42 | 2.8% | 71.5 | 10/10 | 0.70 | 0.44 | 0.41 | 4 | 6.9% | 0.45 | 0.63 | 12.3% | 11.5% | 17.1% | 12.6%/9.8% | 8.6 (interpolated) | pass | 0.162 (unverified) | -0.15 |
| 142 | `cfg_1851` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 29/39/53 | 121 | 13.5% | 2.6% | 1.08 | -2.0% | 248 | 1.72 | 1.5% | 53.8 | 11/11 | 0.73 | 0.55 | 0.53 | 4 | 8.3% | 0.36 | 0.58 | 12.8% | 12.2% | 15.3% | 12.0%/8.6% | 10.9 (interpolated) | pass | 0.316 (unverified) | -0.24 |
| 143 | `cfg_132b` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 27/74/0 | 101 | 18.7% | 3.5% | 1.07 | -3.2% | 136 | 2.18 | 1.8% | 44.9 | 11/11 | 0.91 | 0.63 | 0.44 | 4 | 9.1% | 0.49 | 0.49 | 18.1% | 17.6% | 12.1% | 16.1%/12.5% | 17.8 (interpolated) | pass | 0.303 (unverified) | 0.78 |
| 144 | `cfg_9654` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 7/72/89 | 168 | 34.0% | 6.0% | 0.91 | -7.3% | 236 | 1.55 | 7.6% | 74.9 | 10/10 | 1.00 | 0.67 | 0.25 | 5 | 19.3% | 0.36 | 0.63 | 33.0% | 32.5% | -10.7% | 32.2%/24.7% | 18.6 (interpolated) | pass | 0.194 (unverified) | 0.81 |
| 145 | `cfg_42ce` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-1.75, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 47/4/51 | 102 | 37.2% | 6.5% | 0.86 | -10.7% | 317 | 1.74 | 5.7% | 45.5 | 12/12 | 0.92 | 0.75 | 0.11 | 4 | 20.6% | 0.40 | 0.70 | 36.6% | 35.7% | 8.5% | 33.1%/25.9% | n/a (profitable_beyond_25.0x) | pass | 0.162 (unverified) | 0.34 |
| 146 | `cfg_a5ef` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=0.75 | 41/20/128 | 189 | 28.6% | 5.2% | 0.82 | -6.3% | 158 | 1.41 | 9.4% | 83.6 | 11/11 | 0.82 | 0.58 | 0.24 | 5 | 17.1% | 0.34 | 0.94 | 27.7% | 26.2% | 26.2% | 24.9%/19.8% | 14.1 (interpolated) | pass | 0.143 (unverified) | 0.47 |
| 147 | `cfg_0631` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 46/28/105 | 179 | 30.3% | 5.4% | 0.81 | -8.6% | 183 | 1.38 | 11.1% | 79.2 | 12/12 | 0.83 | 0.53 | 0.28 | 5 | 18.4% | 0.33 | 0.89 | 29.3% | 28.4% | 31.4% | 26.7%/19.6% | 15.6 (interpolated) | pass | 0.142 (unverified) | 0.66 |
| 148 | `cfg_b527` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-1.75, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 12/92/134 | 238 | 31.2% | 5.6% | 0.76 | -8.2% | 459 | 1.39 | 10.4% | 105.4 | 9/9 | 0.89 | 0.61 | 0.14 | 4 | 10.7% | 0.60 | 0.86 | 29.2% | 27.7% | -13.9% | 28.1%/19.2% | 12.4 (interpolated) | pass | 0.100 (unverified) | 0.68 |
| 149 | `cfg_adad` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 24/82/103 | 209 | 19.9% | 3.7% | 0.75 | -5.5% | 247 | 1.32 | 9.4% | 92.9 | 9/9 | 1.00 | 0.67 | 0.08 | 5 | 12.8% | 0.35 | 0.79 | 18.5% | 17.7% | -5.8% | 20.2%/13.3% | 10.1 (interpolated) | pass | 0.118 (unverified) | 0.55 |
| 150 | `cfg_4d08` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=20, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 31/67/23 | 121 | 24.1% | 4.4% | 0.82 | -7.0% | 306 | 1.47 | 7.1% | 53.2 | 9/9 | 0.89 | 0.53 | 0.29 | 5 | 10.4% | 0.51 | 0.67 | 23.4% | 22.4% | 5.1% | 21.1%/16.2% | 18.4 (interpolated) | pass | 0.156 (unverified) | 0.69 |
| 151 | `cfg_0624` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-1.75, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 5/92/35 | 132 | 19.9% | 3.7% | 0.75 | -5.5% | 375 | 1.40 | 8.1% | 59.1 | 8/8 | 0.75 | 0.58 | 0.17 | 5 | 13.0% | 0.34 | 0.85 | 19.3% | 18.7% | 4.6% | 17.9%/13.4% | 14.8 (interpolated) | pass | 0.117 (unverified) | 0.46 |
| 152 | `cfg_1106` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=15, entry_z=-3.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 58/21/58 | 137 | 13.6% | 2.6% | 0.80 | -5.1% | 208 | 1.45 | 2.7% | 60.0 | 11/11 | 1.00 | 0.33 | 0.47 | 3 | 6.3% | 0.56 | 0.69 | 12.8% | 12.1% | 18.7% | 13.0%/10.2% | 10.4 (interpolated) | pass | 0.125 (unverified) | 0.12 |
| 153 | `cfg_55ca` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 55/39/63 | 157 | 20.4% | 3.8% | 0.82 | -6.0% | 369 | 1.43 | 7.4% | 69.7 | 10/10 | 0.80 | 0.68 | 0.14 | 4 | 9.4% | 0.54 | 0.65 | 19.6% | 19.0% | 0.8% | 17.5%/12.3% | 12.7 (interpolated) | pass | 0.158 (unverified) | 0.77 |
| 154 | `cfg_f2f6` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=20, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 30/60/69 | 159 | 22.5% | 4.2% | 0.79 | -6.2% | 285 | 1.38 | 7.4% | 70.3 | 9/9 | 1.00 | 0.70 | 0.10 | 5 | 12.0% | 0.42 | 0.74 | 20.9% | 20.1% | -7.9% | 21.1%/14.1% | 14.2 (interpolated) | pass | 0.132 (unverified) | 0.34 |
| 155 | `cfg_7027` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 71/31/74 | 176 | 46.4% | 7.9% | 0.79 | -15.8% | 400 | 1.49 | 13.0% | 77.1 | 13/13 | 0.85 | 0.56 | 0.23 | 4 | 22.0% | 0.43 | 0.62 | 46.1% | 44.9% | 38.1% | 40.9%/29.1% | 22.5 (interpolated) | pass | 0.148 (unverified) | 0.55 |
| 156 | `cfg_7e52` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=15, entry_confirmation=none, stop_atr_multiple=2.0 | 106/3/57 | 166 | 49.3% | 8.4% | 0.89 | -12.7% | 170 | 1.57 | 11.7% | 73.5 | 11/11 | 0.82 | 0.49 | 0.40 | 5 | 29.1% | 0.32 | 0.52 | 47.8% | 45.6% | 42.0% | 45.2%/32.8% | n/a (profitable_beyond_25.0x) | pass | 0.195 (unverified) | 0.43 |
| 157 | `cfg_487b` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 56/20/60 | 136 | 16.6% | 3.1% | 0.80 | -7.2% | 241 | 1.53 | 2.5% | 60.6 | 11/11 | 0.91 | 0.60 | 0.20 | 4 | 3.4% | 0.84 | 0.66 | 15.7% | 14.4% | 13.5% | 15.1%/11.1% | 11.6 (interpolated) | pass | 0.118 (unverified) | 0.34 |
| 158 | `cfg_d69e` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-1.75, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 6/81/116 | 203 | 31.7% | 5.7% | 0.86 | -6.0% | 238 | 1.42 | 8.7% | 90.5 | 9/9 | 0.89 | 0.71 | 0.15 | 5 | 15.8% | 0.48 | 0.76 | 30.8% | 29.7% | -11.9% | 27.6%/18.4% | 15.1 (interpolated) | pass | 0.159 (unverified) | 0.47 |
| 159 | `cfg_5d0b` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 5/48/63 | 116 | 28.2% | 5.1% | 0.90 | -6.5% | 157 | 1.68 | 5.1% | 51.1 | 11/11 | 1.00 | 0.46 | 0.44 | 4 | 15.8% | 0.44 | 0.63 | 27.5% | 27.1% | -10.0% | 25.3%/18.2% | 22.6 (interpolated) | pass | 0.184 (unverified) | 0.25 |
| 160 | `cfg_f133` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-1.75, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 41/2/62 | 105 | 34.0% | 6.0% | 0.85 | -8.0% | 158 | 1.77 | 4.9% | 46.9 | 11/11 | 0.91 | 0.72 | 0.13 | 4 | 21.0% | 0.34 | 0.77 | 33.1% | 32.5% | -11.7% | 31.7%/23.8% | n/a (profitable_beyond_25.0x) | pass | 0.157 (unverified) | 0.19 |
| 161 | `cfg_4a4e` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 100/7/73 | 180 | 43.6% | 7.5% | 0.82 | -14.1% | 170 | 1.48 | 11.1% | 79.1 | 12/12 | 0.83 | 0.55 | 0.27 | 5 | 20.6% | 0.44 | 0.58 | 42.4% | 41.2% | 38.4% | 39.2%/29.8% | 20.7 (interpolated) | pass | 0.157 (unverified) | 0.55 |
| 162 | `cfg_2d81` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-3.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 86/101/0 | 187 | 22.6% | 4.2% | 0.90 | -4.9% | 225 | 1.51 | 5.3% | 82.2 | 11/11 | 0.91 | 0.52 | 0.38 | 4 | 4.9% | 0.74 | 0.62 | 21.4% | 20.5% | 18.9% | 21.6%/15.4% | 12.6 (interpolated) | pass | 0.204 (unverified) | 0.04 |
| 163 | `cfg_b5fe` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 12/75/116 | 203 | 32.1% | 5.7% | 0.87 | -6.0% | 238 | 1.43 | 8.6% | 90.4 | 10/10 | 0.90 | 0.75 | 0.11 | 5 | 16.1% | 0.47 | 0.75 | 31.2% | 30.1% | -12.0% | 26.7%/15.7% | 15.0 (interpolated) | pass | 0.165 (unverified) | 0.52 |
| 164 | `cfg_316f` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 114/13/114 | 241 | 24.0% | 4.4% | 0.83 | -6.7% | 248 | 1.37 | 4.7% | 107.3 | 11/11 | 1.00 | 0.57 | 0.26 | 4 | 10.5% | 0.58 | 0.56 | 22.7% | 20.9% | 21.1% | 22.0%/17.7% | 9.5 (interpolated) | pass | 0.159 (unverified) | 0.46 |
| 165 | `cfg_433b` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 92/45/74 | 211 | 45.5% | 7.8% | 0.80 | -11.6% | 241 | 1.38 | 17.0% | 94.4 | 12/12 | 0.83 | 0.44 | 0.36 | 4 | 23.9% | 0.38 | 0.65 | 43.0% | 41.3% | 48.7% | 38.3%/26.6% | 18.4 (interpolated) | pass | 0.148 (unverified) | 0.61 |
| 166 | `cfg_968c` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 20/66/99 | 185 | 23.8% | 4.4% | 0.78 | -7.0% | 312 | 1.35 | 8.2% | 83.5 | 10/10 | 0.80 | 0.64 | 0.14 | 4 | 11.3% | 0.52 | 0.87 | 22.5% | 21.5% | -5.5% | 21.5%/14.0% | 12.8 (interpolated) | pass | 0.121 (unverified) | 0.27 |
| 167 | `cfg_05ec` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=15, entry_confirmation=none, stop_atr_multiple=0.75 | 58/0/130 | 188 | 27.1% | 4.9% | 0.78 | -6.5% | 203 | 1.39 | 9.1% | 83.0 | 10/10 | 0.80 | 0.46 | 0.31 | 5 | 18.9% | 0.28 | 0.93 | 26.2% | 25.5% | 24.5% | 25.0%/17.5% | 14.2 (interpolated) | pass | 0.122 (unverified) | 0.53 |
| 168 | `cfg_7768` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 3/50/63 | 116 | 27.3% | 4.9% | 0.87 | -6.5% | 157 | 1.66 | 5.2% | 51.2 | 11/11 | 1.00 | 0.43 | 0.44 | 4 | 15.8% | 0.42 | 0.65 | 26.3% | 25.8% | -10.7% | 24.4%/16.4% | 21.8 (interpolated) | pass | 0.166 (unverified) | 0.25 |
| 169 | `cfg_72f4` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 29/70/122 | 221 | 30.3% | 5.4% | 0.83 | -7.3% | 320 | 1.39 | 9.3% | 98.3 | 11/11 | 0.91 | 0.69 | 0.14 | 5 | 18.1% | 0.37 | 0.73 | 28.6% | 27.7% | -10.8% | 26.6%/16.0% | 13.0 (interpolated) | pass | 0.147 (unverified) | 0.97 |
| 170 | `cfg_3571` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 42/73/81 | 196 | 26.4% | 4.8% | 0.76 | -6.3% | 470 | 1.41 | 9.8% | 86.7 | 9/9 | 0.89 | 0.70 | 0.06 | 4 | 16.9% | 0.36 | 0.51 | 25.3% | 24.8% | -7.9% | 21.8%/14.7% | 12.7 (interpolated) | pass | 0.119 (unverified) | 0.53 |
| 171 | `cfg_7275` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 16/92/122 | 230 | 25.6% | 4.7% | 0.76 | -7.3% | 173 | 1.34 | 10.3% | 101.9 | 10/10 | 0.80 | 0.57 | 0.18 | 5 | 15.0% | 0.41 | 0.74 | 24.7% | 22.5% | -14.6% | 23.8%/12.7% | 11.1 (interpolated) | pass | 0.117 (unverified) | 0.60 |
| 172 | `cfg_b7a4` | timeframe=15min, mean_type=ema, mean_lookback=80, std_lookback=25, entry_z=-3.0, exit_z=1.0, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 11/120/99 | 230 | 36.2% | 6.4% | 0.82 | -10.6% | 241 | 1.44 | 7.6% | 103.7 | 10/10 | 0.80 | 0.43 | 0.39 | 4 | 21.6% | 0.39 | 0.59 | 33.3% | 32.0% | -0.3% | 32.6%/26.2% | 14.7 (interpolated) | pass | 0.184 (unverified) | 0.51 |
| 173 | `cfg_0cec` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 46/46/99 | 191 | 37.9% | 6.6% | 0.78 | -9.3% | 237 | 1.53 | 8.0% | 86.3 | 9/9 | 0.89 | 0.53 | 0.25 | 5 | 21.6% | 0.38 | 0.69 | 35.6% | 33.3% | -8.3% | 31.7%/25.2% | 17.0 (interpolated) | pass | 0.144 (unverified) | 0.45 |
| 174 | `cfg_f14f` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=15, entry_confirmation=none, stop_atr_multiple=1.0 | 68/2/107 | 177 | 28.2% | 5.1% | 0.75 | -9.8% | 166 | 1.36 | 10.8% | 78.4 | 11/11 | 0.82 | 0.48 | 0.27 | 5 | 18.8% | 0.32 | 0.89 | 27.1% | 25.7% | 23.8% | 24.9%/16.5% | 15.5 (interpolated) | pass | 0.116 (unverified) | 0.88 |
| 175 | `cfg_e163` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 2/63/80 | 145 | 32.0% | 5.7% | 0.93 | -6.1% | 278 | 1.56 | 6.3% | 64.2 | 10/10 | 0.90 | 0.77 | 0.16 | 5 | 13.5% | 0.51 | 0.72 | 31.5% | 30.5% | -1.3% | 28.3%/18.7% | 20.2 (interpolated) | pass | 0.202 (unverified) | 0.36 |
| 176 | `cfg_2506` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 46/48/32 | 126 | 33.1% | 5.9% | 0.88 | -7.0% | 312 | 1.78 | 7.0% | 56.0 | 10/10 | 0.90 | 0.61 | 0.27 | 4 | 13.8% | 0.58 | 0.54 | 32.3% | 30.7% | 10.5% | 27.4%/19.9% | 22.9 (interpolated) | pass | 0.207 (unverified) | 0.49 |
| 177 | `cfg_34e8` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 58/10/52 | 120 | 19.4% | 3.6% | 0.93 | -4.2% | 248 | 1.71 | 2.4% | 53.5 | 11/11 | 0.82 | 0.65 | 0.28 | 4 | 9.7% | 0.50 | 0.52 | 18.3% | 17.7% | 15.5% | 17.9%/14.4% | 16.0 (interpolated) | pass | 0.201 (unverified) | 0.18 |
| 178 | `cfg_2e02` | timeframe=15min, mean_type=ema, mean_lookback=80, std_lookback=25, entry_z=-3.0, exit_z=0.5, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 23/109/98 | 230 | 37.5% | 6.6% | 0.85 | -10.5% | 241 | 1.45 | 7.4% | 103.7 | 11/11 | 0.82 | 0.55 | 0.29 | 4 | 21.2% | 0.36 | 0.57 | 36.1% | 33.2% | 2.6% | 33.3%/23.0% | 14.9 (interpolated) | pass | 0.200 (unverified) | 0.52 |
| 179 | `cfg_2e7d` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 78/68/0 | 146 | 37.9% | 6.6% | 0.88 | -8.9% | 179 | 1.61 | 14.1% | 64.2 | 10/10 | 0.90 | 0.38 | 0.50 | 4 | 22.5% | 0.41 | 0.48 | 36.6% | 35.6% | 43.3% | 33.8%/27.4% | 22.9 (interpolated) | pass | 0.193 (unverified) | 0.10 |
| 180 | `cfg_c54f` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-3.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 73/37/153 | 263 | 18.5% | 3.5% | 0.88 | -3.3% | 359 | 1.36 | 4.2% | 116.3 | 12/12 | 0.92 | 0.59 | 0.30 | 4 | 3.8% | 0.79 | 0.83 | 16.7% | 15.2% | 15.6% | 16.3%/11.4% | 7.3 (interpolated) | pass | 0.176 (unverified) | -0.14 |
| 181 | `cfg_8fbb` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 47/31/78 | 156 | 30.4% | 5.5% | 0.83 | -8.5% | 278 | 1.63 | 6.6% | 69.7 | 9/9 | 0.89 | 0.72 | 0.10 | 5 | 14.3% | 0.53 | 0.66 | 28.5% | 27.6% | 2.8% | 27.3%/19.7% | 17.7 (interpolated) | pass | 0.165 (unverified) | 0.52 |
| 182 | `cfg_e8b9` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 6/59/80 | 145 | 31.7% | 5.7% | 0.92 | -6.1% | 278 | 1.56 | 6.2% | 64.1 | 11/11 | 0.91 | 0.84 | 0.08 | 5 | 13.2% | 0.52 | 0.73 | 31.2% | 30.2% | -1.6% | 30.1%/19.9% | 20.0 (interpolated) | pass | 0.198 (unverified) | 0.35 |
| 183 | `cfg_52bf` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 23/65/106 | 194 | 29.4% | 5.3% | 0.76 | -13.9% | 320 | 1.41 | 8.4% | 86.0 | 11/11 | 0.91 | 0.71 | 0.05 | 5 | 18.3% | 0.32 | 0.81 | 27.4% | 26.6% | -10.6% | 27.1%/15.0% | 13.7 (interpolated) | pass | 0.117 (unverified) | 0.73 |
| 184 | `cfg_d84f` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 25/62/87 | 174 | 20.3% | 3.8% | 0.83 | -6.9% | 384 | 1.39 | 7.7% | 77.2 | 8/8 | 1.00 | 0.53 | 0.30 | 4 | 8.4% | 0.54 | 0.66 | 19.2% | 18.4% | -1.8% | 19.5%/15.0% | 12.0 (interpolated) | pass | 0.154 (unverified) | 0.19 |
| 185 | `cfg_6ba2` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 56/45/46 | 147 | 20.3% | 3.8% | 0.78 | -6.5% | 434 | 1.42 | 7.8% | 65.7 | 10/10 | 0.90 | 0.65 | 0.12 | 4 | 10.1% | 0.50 | 0.66 | 19.8% | 19.1% | 2.9% | 18.6%/13.5% | 13.3 (interpolated) | pass | 0.134 (unverified) | 0.82 |
| 186 | `cfg_1aae` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=20, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 30/64/38 | 132 | 24.9% | 4.6% | 0.84 | -6.6% | 269 | 1.46 | 7.3% | 58.4 | 9/9 | 1.00 | 0.72 | 0.12 | 5 | 11.9% | 0.47 | 0.65 | 24.2% | 23.2% | -1.4% | 22.7%/15.0% | 17.8 (interpolated) | pass | 0.154 (unverified) | 0.46 |
| 187 | `cfg_b8d1` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 41/79/46 | 166 | 42.8% | 7.4% | 0.88 | -14.8% | 453 | 1.55 | 9.4% | 73.7 | 10/10 | 0.90 | 0.77 | 0.12 | 5 | 24.7% | 0.36 | 0.60 | 41.1% | 40.3% | 0.5% | 37.7%/27.5% | 21.8 (interpolated) | pass | 0.195 (unverified) | 0.25 |
| 188 | `cfg_7e85` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 51/3/46 | 100 | 13.4% | 2.5% | 0.86 | -4.1% | 212 | 1.60 | 2.1% | 44.4 | 12/12 | 0.83 | 0.34 | 0.52 | 4 | 5.3% | 0.60 | 0.65 | 12.9% | 12.5% | 12.6% | 12.0%/8.9% | 13.3 (interpolated) | pass | 0.156 (unverified) | -0.17 |
| 189 | `cfg_053f` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 69/56/46 | 171 | 38.3% | 6.7% | 0.82 | -15.4% | 327 | 1.52 | 9.0% | 75.4 | 10/10 | 0.90 | 0.68 | 0.14 | 4 | 23.0% | 0.37 | 0.69 | 36.5% | 34.7% | 0.1% | 35.2%/25.7% | 19.2 (interpolated) | pass | 0.162 (unverified) | 0.54 |
| 190 | `cfg_9559` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 66/41/0 | 107 | 32.0% | 5.7% | 0.88 | -5.1% | 286 | 1.73 | 13.2% | 47.8 | 8/8 | 0.88 | 0.48 | 0.40 | 5 | 19.9% | 0.36 | 0.48 | 31.5% | 30.9% | 31.5% | 31.5%/27.5% | n/a (profitable_beyond_25.0x) | pass | 0.195 (unverified) | -0.14 |
| 191 | `cfg_56a8` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 28/57/70 | 155 | 24.6% | 4.5% | 0.76 | -7.7% | 328 | 1.39 | 7.2% | 68.9 | 10/10 | 1.00 | 0.64 | 0.12 | 4 | 12.9% | 0.42 | 0.74 | 23.4% | 22.5% | -12.2% | 22.8%/16.2% | 15.1 (interpolated) | pass | 0.119 (unverified) | 0.13 |
| 192 | `cfg_dda7` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 8/96/110 | 214 | 16.2% | 3.0% | 0.79 | -2.9% | 141 | 1.50 | 2.6% | 94.0 | 9/9 | 1.00 | 0.53 | 0.26 | 4 | 7.3% | 0.54 | 0.93 | 14.9% | 13.8% | -1.6% | 14.6%/11.1% | 7.7 (interpolated) | pass | 0.096 (unverified) | 0.19 |
| 193 | `cfg_9067` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-0.5, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 99/24/117 | 240 | 23.1% | 4.2% | 0.81 | -6.1% | 248 | 1.35 | 5.1% | 107.2 | 12/12 | 1.00 | 0.50 | 0.31 | 4 | 10.3% | 0.56 | 0.54 | 21.5% | 19.8% | 11.1% | 21.0%/16.9% | 9.3 (interpolated) | pass | 0.151 (unverified) | 0.57 |
| 194 | `cfg_3ec5` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 2/82/90 | 174 | 20.1% | 3.7% | 0.77 | -6.1% | 377 | 1.36 | 8.2% | 77.4 | 8/8 | 1.00 | 0.46 | 0.31 | 4 | 9.6% | 0.48 | 0.82 | 18.7% | 17.6% | 0.2% | 19.1%/12.7% | 11.9 (interpolated) | pass | 0.120 (unverified) | 0.24 |
| 195 | `cfg_6974` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-1.75, exit_z=-1.0, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 69/12/176 | 257 | 33.9% | 6.0% | 0.77 | -6.7% | 178 | 1.31 | 14.9% | 114.3 | 9/9 | 0.78 | 0.40 | 0.37 | 4 | 20.4% | 0.33 | 0.77 | 31.1% | 29.9% | 7.2% | 30.8%/19.9% | 12.4 (interpolated) | pass | 0.129 (unverified) | -0.47 |
| 196 | `cfg_f575` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-1.75, exit_z=-0.5, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 64/1/116 | 181 | 35.6% | 6.3% | 0.81 | -9.6% | 320 | 1.49 | 9.0% | 80.6 | 10/10 | 0.90 | 0.60 | 0.22 | 4 | 18.5% | 0.45 | 0.70 | 34.6% | 34.0% | -12.3% | 31.8%/22.7% | 17.8 (interpolated) | pass | 0.137 (unverified) | 0.55 |
| 197 | `cfg_06e7` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 24/69/31 | 124 | 29.8% | 5.4% | 0.79 | -7.1% | 284 | 1.71 | 7.2% | 55.4 | 11/11 | 0.91 | 0.52 | 0.27 | 4 | 10.8% | 0.64 | 0.58 | 28.3% | 27.6% | 6.3% | 26.9%/19.6% | 20.9 (interpolated) | pass | 0.152 (unverified) | 0.40 |
| 198 | `cfg_9d59` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=25, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 25/52/86 | 163 | 23.3% | 4.3% | 0.80 | -9.7% | 388 | 1.42 | 7.1% | 72.4 | 9/9 | 0.89 | 0.62 | 0.18 | 4 | 15.6% | 0.33 | 0.60 | 22.5% | 21.4% | -17.4% | 21.6%/14.4% | 13.7 (interpolated) | pass | 0.157 (unverified) | 0.28 |
| 199 | `cfg_5a2f` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=25, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 6/69/88 | 163 | 22.4% | 4.1% | 0.77 | -10.2% | 444 | 1.39 | 7.4% | 72.5 | 9/9 | 0.89 | 0.59 | 0.17 | 4 | 13.6% | 0.34 | 0.60 | 21.6% | 20.4% | -20.4% | 19.4%/13.5% | 13.3 (interpolated) | pass | 0.137 (unverified) | 0.25 |
| 200 | `cfg_4bc2` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 51/18/147 | 216 | 34.9% | 6.2% | 0.82 | -7.8% | 357 | 1.39 | 13.3% | 95.9 | 8/8 | 0.62 | 0.50 | 0.31 | 3 | 18.2% | 0.48 | 0.73 | 33.9% | 32.5% | 4.7% | 35.5%/18.9% | 14.7 (interpolated) | pass | 0.155 (unverified) | -0.32 |
| 201 | `cfg_8db2` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 22/71/101 | 194 | 26.4% | 4.8% | 0.94 | -7.4% | 348 | 1.44 | 8.5% | 87.4 | 9/9 | 0.89 | 0.69 | 0.26 | 5 | 16.4% | 0.35 | 0.66 | 24.4% | 23.6% | 11.0% | 24.4%/19.0% | 13.0 (interpolated) | pass | 0.218 (unverified) | 0.16 |
| 202 | `cfg_f63d` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 101/61/0 | 162 | 24.4% | 4.5% | 0.88 | -9.2% | 238 | 1.50 | 6.1% | 71.7 | 11/11 | 1.00 | 0.74 | 0.14 | 4 | 5.7% | 0.78 | 0.47 | 23.9% | 23.1% | 21.4% | 23.3%/19.5% | 14.5 (interpolated) | pass | 0.192 (unverified) | 0.31 |
| 203 | `cfg_0bd4` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 26/63/21 | 110 | 17.9% | 3.4% | 0.79 | -3.2% | 163 | 1.49 | 6.6% | 49.3 | 10/10 | 1.00 | 0.68 | 0.11 | 4 | 10.3% | 0.39 | 0.65 | 17.0% | 16.3% | 10.5% | 15.7%/10.4% | 15.7 (interpolated) | pass | 0.138 (unverified) | 0.63 |
| 204 | `cfg_5889` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 11/87/79 | 177 | 31.5% | 5.6% | 0.81 | -6.0% | 243 | 1.43 | 8.7% | 79.1 | 11/11 | 0.91 | 0.55 | 0.26 | 5 | 16.0% | 0.46 | 0.76 | 30.8% | 29.8% | -14.1% | 26.8%/16.1% | 16.2 (interpolated) | pass | 0.139 (unverified) | 0.05 |
| 205 | `cfg_3c48` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 12/92/110 | 214 | 15.9% | 3.0% | 0.78 | -2.9% | 141 | 1.49 | 2.5% | 94.1 | 10/10 | 1.00 | 0.56 | 0.21 | 4 | 7.0% | 0.55 | 0.93 | 14.7% | 13.3% | -1.7% | 15.2%/9.3% | 7.6 (interpolated) | pass | 0.091 (unverified) | 0.19 |
| 206 | `cfg_563a` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-1.75, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 6/92/79 | 177 | 31.4% | 5.6% | 0.80 | -6.0% | 243 | 1.43 | 8.8% | 79.0 | 10/10 | 0.90 | 0.52 | 0.29 | 5 | 15.9% | 0.46 | 0.77 | 30.4% | 29.6% | -12.9% | 28.2%/17.6% | 15.7 (interpolated) | pass | 0.137 (unverified) | 0.05 |
| 207 | `cfg_c9de` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=20, entry_z=-3.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=0.75 | 69/174/547 | 790 | 51.8% | 8.7% | 0.95 | -10.3% | 240 | 1.26 | 11.9% | 356.6 | 10/10 | 0.80 | 0.42 | 0.53 | 5 | 23.6% | 0.49 | 0.59 | 41.6% | 37.7% | 26.1% | 31.2%/19.9% | 6.0 (interpolated) | pass | 0.247 (unverified) | -0.08 |
| 208 | `cfg_28c2` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 24/95/47 | 166 | 41.4% | 7.2% | 0.86 | -14.7% | 453 | 1.53 | 9.7% | 73.5 | 10/10 | 0.90 | 0.74 | 0.12 | 5 | 24.3% | 0.35 | 0.62 | 40.4% | 38.6% | 5.0% | 38.0%/22.8% | 21.0 (interpolated) | pass | 0.183 (unverified) | 0.50 |
| 209 | `cfg_5f6e` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-1.75, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 8/114/45 | 167 | 35.5% | 6.3% | 0.78 | -15.8% | 475 | 1.49 | 10.0% | 73.1 | 10/10 | 0.90 | 0.64 | 0.13 | 5 | 20.3% | 0.40 | 0.73 | 34.7% | 33.8% | -0.9% | 33.5%/24.8% | 19.1 (interpolated) | pass | 0.140 (unverified) | 0.74 |
| 210 | `cfg_f5d6` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 24/56/99 | 179 | 33.3% | 5.9% | 0.84 | -6.0% | 206 | 1.50 | 7.5% | 79.7 | 10/10 | 0.90 | 0.62 | 0.22 | 5 | 15.7% | 0.50 | 0.76 | 32.4% | 31.0% | -20.8% | 29.0%/19.7% | 16.8 (interpolated) | pass | 0.133 (unverified) | 0.62 |
| 211 | `cfg_27d8` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 81/42/92 | 215 | 52.1% | 8.8% | 0.90 | -13.9% | 228 | 1.43 | 16.5% | 95.5 | 13/13 | 1.00 | 0.57 | 0.34 | 5 | 33.8% | 0.31 | 0.58 | 51.3% | 49.8% | 35.3% | 41.5%/29.4% | 20.7 (interpolated) | pass | 0.205 (unverified) | 0.65 |
| 212 | `cfg_6ad1` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 18/177/0 | 195 | 21.5% | 4.0% | 0.89 | -4.1% | 172 | 1.59 | 3.6% | 85.5 | 10/10 | 0.90 | 0.55 | 0.34 | 4 | 12.6% | 0.39 | 0.47 | 20.4% | 19.2% | 29.0% | 19.3%/14.1% | 11.3 (interpolated) | pass | 0.197 (unverified) | 0.82 |
| 213 | `cfg_ffb5` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 56/139/0 | 195 | 19.0% | 3.5% | 0.81 | -4.1% | 241 | 1.53 | 3.4% | 85.2 | 10/10 | 0.90 | 0.58 | 0.23 | 4 | 10.0% | 0.45 | 0.52 | 17.9% | 16.8% | 31.0% | 16.8%/13.2% | 10.2 (interpolated) | pass | 0.156 (unverified) | 0.91 |
| 214 | `cfg_12e9` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-3.5, exit_z=-0.5, max_holding_bars=15, entry_confirmation=none, stop_atr_multiple=1.0 | 87/13/163 | 263 | 18.5% | 3.5% | 0.82 | -5.8% | 257 | 1.32 | 4.6% | 117.5 | 11/11 | 0.91 | 0.52 | 0.30 | 4 | 3.5% | 0.82 | 0.73 | 16.4% | 15.6% | 16.1% | 16.8%/11.5% | 7.4 (interpolated) | pass | 0.156 (unverified) | -0.19 |
| 215 | `cfg_4458` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 10/69/100 | 179 | 35.1% | 6.2% | 0.87 | -6.1% | 206 | 1.53 | 7.8% | 79.6 | 10/10 | 0.80 | 0.66 | 0.21 | 5 | 18.2% | 0.45 | 0.73 | 34.1% | 33.0% | -21.5% | 29.7%/18.5% | 17.5 (interpolated) | pass | 0.150 (unverified) | 0.60 |
| 216 | `cfg_9d94` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 3/84/22 | 109 | 19.2% | 3.6% | 0.79 | -3.7% | 173 | 1.50 | 7.0% | 48.5 | 11/11 | 1.00 | 0.56 | 0.23 | 5 | 10.6% | 0.40 | 0.78 | 18.6% | 18.5% | 13.9% | 18.1%/11.1% | 17.8 (interpolated) | pass | 0.133 (unverified) | 0.69 |
| 217 | `cfg_f14f` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 52/60/122 | 234 | 25.6% | 4.7% | 0.76 | -7.0% | 173 | 1.34 | 9.7% | 103.5 | 9/9 | 0.89 | 0.58 | 0.19 | 5 | 15.6% | 0.39 | 0.74 | 24.3% | 21.8% | -10.2% | 24.3%/15.1% | 10.4 (interpolated) | pass | 0.121 (unverified) | 0.59 |
| 218 | `cfg_8367` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=20, entry_z=-1.75, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 55/49/0 | 104 | 33.1% | 5.9% | 0.88 | -10.2% | 282 | 1.77 | 10.0% | 46.3 | 10/10 | 0.90 | 0.34 | 0.55 | 4 | 12.8% | 0.54 | 0.42 | 32.0% | 31.0% | 16.4% | 29.4%/23.0% | n/a (profitable_beyond_25.0x) | pass | 0.213 (unverified) | -0.22 |
| 219 | `cfg_c053` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 76/2/53 | 131 | 36.1% | 6.4% | 0.81 | -7.7% | 269 | 1.56 | 9.4% | 58.5 | 10/10 | 0.80 | 0.51 | 0.30 | 5 | 19.0% | 0.47 | 0.56 | 34.2% | 33.6% | 18.2% | 31.2%/24.7% | 23.6 (interpolated) | pass | 0.158 (unverified) | 0.28 |
| 220 | `cfg_0725` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=25, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 27/36/74 | 137 | 26.2% | 4.8% | 0.76 | -11.0% | 335 | 1.52 | 5.8% | 61.2 | 9/9 | 1.00 | 0.63 | 0.13 | 3 | 9.8% | 0.57 | 0.76 | 25.5% | 24.6% | -21.2% | 24.9%/16.8% | 17.8 (interpolated) | pass | 0.114 (unverified) | 0.27 |
| 221 | `cfg_d314` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-1.75, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 49/71/0 | 120 | 37.6% | 6.6% | 0.78 | -10.4% | 331 | 1.63 | 13.2% | 52.8 | 11/11 | 0.91 | 0.58 | 0.20 | 4 | 15.2% | 0.55 | 0.63 | 36.9% | 36.1% | 24.1% | 32.0%/23.3% | n/a (profitable_beyond_25.0x) | pass | 0.132 (unverified) | 0.26 |
| 222 | `cfg_cb21` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-3.5, exit_z=0.5, max_holding_bars=15, entry_confirmation=none, stop_atr_multiple=1.0 | 42/41/144 | 227 | 15.9% | 3.0% | 0.82 | -3.4% | 318 | 1.37 | 4.4% | 98.9 | 11/11 | 0.73 | 0.31 | 0.51 | 3 | 0.6% | 0.96 | 0.81 | 15.1% | 13.3% | 4.9% | 14.3%/10.5% | 8.0 (interpolated) | pass | 0.159 (unverified) | 0.49 |
| 223 | `cfg_e4c0` | timeframe=15min, mean_type=ema, mean_lookback=100, std_lookback=20, entry_z=-3.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=0.75 | 85/159/550 | 794 | 45.0% | 7.7% | 0.87 | -10.3% | 241 | 1.23 | 11.7% | 358.8 | 10/10 | 0.80 | 0.37 | 0.50 | 4 | 20.4% | 0.51 | 0.65 | 37.9% | 33.4% | 23.3% | 28.4%/15.5% | 5.6 (interpolated) | pass | 0.199 (unverified) | -0.10 |
| 224 | `cfg_f1c6` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-1.75, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 65/53/0 | 118 | 35.7% | 6.3% | 0.75 | -6.7% | 217 | 1.55 | 11.9% | 51.8 | 11/11 | 0.91 | 0.67 | 0.08 | 4 | 22.2% | 0.35 | 0.78 | 35.1% | 34.4% | 17.7% | 33.2%/25.7% | n/a (profitable_beyond_25.0x) | pass | 0.109 (unverified) | 0.73 |
| 225 | `cfg_5182` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=25, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 21/62/20 | 103 | 18.3% | 3.4% | 0.79 | -5.0% | 455 | 1.52 | 6.2% | 45.6 | 8/8 | 0.88 | 0.37 | 0.42 | 4 | 8.2% | 0.51 | 0.67 | 17.6% | 16.8% | 11.5% | 16.6%/12.1% | 16.6 (interpolated) | pass | 0.144 (unverified) | -0.05 |
| 226 | `cfg_e540` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 113/18/90 | 221 | 44.2% | 7.6% | 0.81 | -14.1% | 236 | 1.39 | 14.6% | 97.5 | 12/12 | 1.00 | 0.45 | 0.37 | 5 | 29.5% | 0.33 | 0.64 | 43.0% | 41.0% | 38.8% | 33.7%/22.9% | 18.0 (interpolated) | pass | 0.154 (unverified) | 0.55 |
| 227 | `cfg_6236` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 59/23/33 | 115 | 16.2% | 3.1% | 0.81 | -5.9% | 238 | 1.59 | 2.3% | 50.7 | 12/12 | 0.83 | 0.43 | 0.38 | 4 | 6.5% | 0.60 | 0.59 | 15.6% | 14.9% | 16.2% | 14.5%/11.6% | 14.3 (interpolated) | pass | 0.138 (unverified) | -0.09 |
| 228 | `cfg_9c9d` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-3.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 53/134/0 | 187 | 23.1% | 4.3% | 0.80 | -4.9% | 397 | 1.48 | 5.7% | 81.9 | 11/11 | 0.91 | 0.41 | 0.38 | 4 | 7.6% | 0.62 | 0.68 | 22.7% | 21.9% | 21.9% | 20.2%/15.6% | 11.9 (interpolated) | pass | 0.148 (unverified) | 0.18 |
| 229 | `cfg_c42d` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 122/16/86 | 224 | 22.3% | 4.1% | 0.78 | -8.1% | 248 | 1.34 | 5.0% | 98.9 | 11/11 | 1.00 | 0.41 | 0.36 | 3 | 5.5% | 0.77 | 0.56 | 20.7% | 19.4% | 24.0% | 19.9%/15.0% | 9.9 (interpolated) | pass | 0.128 (unverified) | 0.12 |
| 230 | `cfg_1474` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 7/84/102 | 193 | 22.2% | 4.1% | 0.80 | -7.2% | 348 | 1.36 | 8.8% | 87.2 | 9/9 | 0.89 | 0.64 | 0.16 | 5 | 13.0% | 0.39 | 0.77 | 21.1% | 19.8% | 11.6% | 19.8%/13.9% | 11.4 (interpolated) | pass | 0.137 (unverified) | 0.16 |
| 231 | `cfg_74e2` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 22/81/36 | 139 | 27.3% | 4.9% | 0.95 | -5.2% | 388 | 1.53 | 8.1% | 60.9 | 10/10 | 1.00 | 0.59 | 0.36 | 5 | 15.0% | 0.39 | 0.63 | 26.2% | 25.3% | -1.4% | 22.3%/15.0% | 17.6 (interpolated) | pass | 0.236 (unverified) | 0.42 |
| 232 | `cfg_1356` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-1.75, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 59/64/0 | 123 | 41.6% | 7.2% | 0.80 | -9.4% | 134 | 1.77 | 12.6% | 54.8 | 11/11 | 1.00 | 0.60 | 0.21 | 5 | 26.0% | 0.36 | 0.53 | 40.4% | 39.5% | 22.9% | 38.3%/31.1% | n/a (profitable_beyond_25.0x) | pass | 0.155 (unverified) | 0.46 |
| 233 | `cfg_8789` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 85/14/95 | 194 | 19.4% | 3.6% | 0.86 | -6.4% | 208 | 1.39 | 4.6% | 85.5 | 12/12 | 0.83 | 0.57 | 0.29 | 4 | 11.2% | 0.42 | 0.60 | 17.5% | 16.3% | 13.4% | 17.6%/13.2% | 9.8 (interpolated) | pass | 0.167 (unverified) | 0.33 |
| 234 | `cfg_e8be` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 330/180/0 | 510 | 40.5% | 7.0% | 0.76 | -10.3% | 331 | 1.29 | 12.8% | 226.7 | 11/11 | 1.00 | 0.46 | 0.29 | 3 | 6.7% | 0.77 | 0.52 | 38.2% | 35.4% | 30.7% | 36.5%/26.7% | 7.9 (interpolated) | pass | 0.139 (unverified) | 0.11 |
| 235 | `cfg_f45a` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 25/106/0 | 131 | 26.7% | 4.9% | 0.75 | -10.9% | 317 | 1.49 | 8.7% | 58.2 | 9/9 | 1.00 | 0.67 | 0.08 | 3 | 13.9% | 0.51 | 0.80 | 25.9% | 25.3% | 5.0% | 28.2%/21.1% | 19.2 (interpolated) | pass | 0.120 (unverified) | 0.58 |
| 236 | `cfg_a717` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=10, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 28/37/67 | 132 | 40.9% | 7.1% | 0.93 | -6.7% | 238 | 1.85 | 5.8% | 60.3 | 10/10 | 0.90 | 0.52 | 0.41 | 5 | 18.9% | 0.48 | 0.65 | 38.8% | 38.2% | -7.0% | 34.3%/26.1% | n/a (profitable_beyond_25.0x) | pass | 0.213 (unverified) | 0.27 |
| 237 | `cfg_f418` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 22/80/0 | 102 | 19.2% | 3.6% | 0.79 | -6.8% | 391 | 1.59 | 6.7% | 46.0 | 9/9 | 0.89 | 0.65 | 0.15 | 4 | 11.7% | 0.39 | 0.61 | 18.5% | 17.9% | 21.0% | 18.2%/13.6% | 18.0 (interpolated) | pass | 0.144 (unverified) | 0.10 |
| 238 | `cfg_391b` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 51/86/0 | 137 | 34.7% | 6.1% | 0.79 | -8.9% | 254 | 1.53 | 14.8% | 60.3 | 11/11 | 0.82 | 0.35 | 0.44 | 4 | 19.8% | 0.43 | 0.58 | 33.7% | 32.9% | 40.7% | 30.7%/22.6% | 22.2 (interpolated) | pass | 0.142 (unverified) | -0.05 |
| 239 | `cfg_d64a` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-3.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 36/53/138 | 227 | 15.8% | 3.0% | 0.81 | -4.1% | 348 | 1.38 | 3.7% | 98.8 | 12/12 | 0.92 | 0.45 | 0.36 | 3 | 1.3% | 0.92 | 0.89 | 14.4% | 12.8% | 4.6% | 14.0%/11.1% | 7.7 (interpolated) | pass | 0.137 (unverified) | 0.32 |
| 240 | `cfg_df4d` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 2/82/34 | 118 | 19.4% | 3.6% | 0.76 | -4.4% | 706 | 1.46 | 7.1% | 52.6 | 11/11 | 0.91 | 0.58 | 0.19 | 4 | 10.6% | 0.41 | 0.75 | 19.0% | 18.3% | 8.8% | 16.9%/8.5% | 15.6 (interpolated) | pass | 0.134 (unverified) | 0.48 |
| 241 | `cfg_9662` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-1.75, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 288/205/0 | 493 | 37.1% | 6.5% | 0.86 | -8.5% | 260 | 1.30 | 12.2% | 217.8 | 9/9 | 0.89 | 0.62 | 0.24 | 3 | 12.1% | 0.63 | 0.49 | 34.7% | 30.6% | 10.0% | 36.1%/27.3% | 7.3 (interpolated) | pass | 0.168 (unverified) | 0.12 |
| 242 | `cfg_8e3d` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 69/47/0 | 116 | 27.8% | 5.0% | 0.80 | -7.9% | 369 | 1.54 | 10.1% | 52.4 | 9/9 | 0.89 | 0.55 | 0.25 | 5 | 19.0% | 0.27 | 0.59 | 27.4% | 26.6% | 19.6% | 24.1%/17.2% | 21.9 (interpolated) | pass | 0.149 (unverified) | 0.36 |
| 243 | `cfg_aa8b` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=20, entry_z=-2.0, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 1/83/34 | 118 | 19.2% | 3.6% | 0.76 | -4.4% | 706 | 1.45 | 7.1% | 52.6 | 10/10 | 0.90 | 0.49 | 0.27 | 4 | 10.4% | 0.42 | 0.76 | 18.8% | 18.0% | 8.4% | 18.3%/11.4% | 15.5 (interpolated) | pass | 0.131 (unverified) | 0.48 |
| 244 | `cfg_a86e` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=25, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 78/85/0 | 163 | 35.7% | 6.3% | 0.75 | -11.3% | 163 | 1.42 | 17.1% | 71.9 | 11/11 | 0.91 | 0.50 | 0.25 | 3 | 18.0% | 0.51 | 0.71 | 34.8% | 34.2% | 33.1% | 35.2%/25.3% | 20.4 (interpolated) | pass | 0.115 (unverified) | 0.27 |
| 245 | `cfg_cd51` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=20, entry_z=-1.75, exit_z=1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 13/127/0 | 140 | 38.8% | 6.8% | 0.79 | -14.0% | 328 | 1.49 | 17.1% | 63.1 | 10/10 | 0.90 | 0.43 | 0.36 | 4 | 16.6% | 0.53 | 0.62 | 38.3% | 37.5% | 46.0% | 33.5%/24.8% | 22.7 (interpolated) | pass | 0.156 (unverified) | 0.47 |
| 246 | `cfg_30fd` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 14/89/36 | 139 | 25.5% | 4.6% | 0.88 | -5.3% | 361 | 1.49 | 8.3% | 61.3 | 11/11 | 0.91 | 0.62 | 0.26 | 5 | 15.1% | 0.36 | 0.67 | 24.7% | 24.2% | -2.3% | 22.5%/13.2% | 17.0 (interpolated) | pass | 0.193 (unverified) | 0.42 |
| 247 | `cfg_2443` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 12/89/0 | 101 | 28.0% | 5.1% | 0.82 | -12.4% | 791 | 1.54 | 12.3% | 45.4 | 9/9 | 0.78 | 0.51 | 0.30 | 5 | 16.1% | 0.40 | 0.57 | 28.0% | 27.6% | 35.7% | 24.6%/18.7% | 24.5 (interpolated) | pass | 0.164 (unverified) | 0.56 |
| 248 | `cfg_dbf4` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 15/48/69 | 132 | 42.7% | 7.4% | 0.97 | -6.6% | 238 | 1.88 | 5.9% | 60.1 | 10/10 | 0.90 | 0.48 | 0.49 | 5 | 19.6% | 0.49 | 0.62 | 41.6% | 40.5% | -10.0% | 36.7%/26.1% | n/a (profitable_beyond_25.0x) | pass | 0.243 (unverified) | 0.34 |
| 249 | `cfg_cfa0` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-2.5, exit_z=-0.5, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 37/24/150 | 211 | 34.2% | 6.1% | 0.78 | -7.8% | 285 | 1.36 | 14.0% | 94.4 | 9/9 | 0.67 | 0.51 | 0.27 | 4 | 17.5% | 0.46 | 0.78 | 32.9% | 31.5% | 5.9% | 33.3%/3.0% | 14.7 (interpolated) | pass | 0.135 (unverified) | -0.29 |
| 250 | `cfg_a8ab` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=25, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 21/62/29 | 112 | 18.4% | 3.4% | 0.79 | -5.9% | 423 | 1.48 | 6.5% | 50.1 | 8/8 | 1.00 | 0.35 | 0.44 | 4 | 8.9% | 0.47 | 0.66 | 17.5% | 16.9% | 6.3% | 17.4%/12.7% | 16.4 (interpolated) | pass | 0.142 (unverified) | -0.05 |
| 251 | `cfg_d18c` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 130/404/0 | 534 | 26.6% | 4.8% | 0.89 | -8.3% | 335 | 1.26 | 9.1% | 235.0 | 10/10 | 0.80 | 0.39 | 0.50 | 3 | 4.3% | 0.78 | 0.59 | 23.3% | 20.1% | 4.3% | 23.3%/16.5% | 5.6 (interpolated) | pass | 0.193 (unverified) | -0.13 |
| 252 | `cfg_08ce` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=25, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 32/52/100 | 184 | 22.5% | 4.2% | 0.78 | -6.7% | 170 | 1.34 | 7.6% | 82.2 | 7/7 | 0.86 | 0.54 | 0.24 | 5 | 14.5% | 0.31 | 0.63 | 21.4% | 20.2% | -16.5% | 19.4%/12.7% | 12.1 (interpolated) | pass | 0.133 (unverified) | -0.10 |
| 253 | `cfg_990c` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-1.75, exit_z=1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 25/95/0 | 120 | 41.8% | 7.2% | 0.83 | -10.2% | 297 | 1.67 | 14.0% | 53.5 | 10/10 | 0.80 | 0.48 | 0.35 | 4 | 17.3% | 0.54 | 0.62 | 40.8% | 39.8% | 25.9% | 34.1%/25.0% | n/a (profitable_beyond_25.0x) | pass | 0.146 (unverified) | 0.12 |
| 254 | `cfg_adf8` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=15, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 111/51/0 | 162 | 20.3% | 3.8% | 0.77 | -8.4% | 238 | 1.43 | 5.9% | 72.4 | 11/11 | 1.00 | 0.58 | 0.19 | 4 | 4.5% | 0.79 | 0.45 | 19.7% | 19.0% | 17.5% | 18.6%/14.6% | 12.3 (interpolated) | pass | 0.134 (unverified) | 0.27 |
| 255 | `cfg_f9bd` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 40/64/0 | 104 | 42.6% | 7.4% | 0.88 | -10.6% | 173 | 1.84 | 11.2% | 46.0 | 12/12 | 0.92 | 0.36 | 0.52 | 5 | 24.8% | 0.34 | 0.51 | 40.7% | 40.5% | 29.1% | 37.3%/26.2% | n/a (profitable_beyond_25.0x) | pass | 0.197 (unverified) | 0.33 |
| 256 | `cfg_2c21` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 22/70/101 | 193 | 21.2% | 3.9% | 0.76 | -7.0% | 205 | 1.32 | 8.8% | 85.4 | 9/9 | 0.78 | 0.51 | 0.25 | 4 | 12.6% | 0.40 | 0.79 | 20.2% | 18.8% | -8.5% | 19.2%/11.7% | 10.7 (interpolated) | pass | 0.118 (unverified) | 0.57 |
| 257 | `cfg_84c5` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 0/60/78 | 138 | 18.9% | 3.5% | 0.80 | -4.7% | 342 | 1.42 | 6.0% | 60.2 | 10/10 | 0.90 | 0.40 | 0.41 | 4 | 9.0% | 0.48 | 0.93 | 18.0% | 17.2% | -6.5% | 18.2%/11.5% | 14.5 (interpolated) | pass | 0.137 (unverified) | 0.26 |
| 258 | `cfg_de16` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 0/60/78 | 138 | 18.9% | 3.5% | 0.80 | -4.7% | 342 | 1.42 | 6.0% | 60.2 | 9/9 | 0.89 | 0.38 | 0.43 | 4 | 9.0% | 0.48 | 0.93 | 18.0% | 17.2% | -6.5% | 18.5%/11.9% | 14.5 (interpolated) | pass | 0.137 (unverified) | 0.26 |
| 259 | `cfg_3186` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 79/119/0 | 198 | 26.1% | 4.8% | 0.86 | -6.4% | 246 | 1.44 | 5.6% | 87.8 | 11/11 | 0.91 | 0.48 | 0.38 | 4 | 10.2% | 0.60 | 0.65 | 25.3% | 23.6% | 22.0% | 21.7%/14.7% | 12.2 (interpolated) | pass | 0.176 (unverified) | 0.24 |
| 260 | `cfg_a69a` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 33/63/99 | 195 | 28.3% | 5.1% | 0.79 | -8.3% | 209 | 1.38 | 8.4% | 87.2 | 10/10 | 1.00 | 0.57 | 0.21 | 5 | 18.3% | 0.33 | 0.69 | 27.7% | 26.4% | -8.6% | 26.4%/16.1% | 13.8 (interpolated) | pass | 0.128 (unverified) | 0.41 |
| 261 | `cfg_8d06` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=10, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=0.75 | 33/47/83 | 163 | 32.8% | 5.8% | 0.80 | -10.6% | 273 | 1.56 | 7.0% | 72.3 | 9/9 | 0.89 | 0.49 | 0.31 | 5 | 19.1% | 0.39 | 0.63 | 31.7% | 30.6% | -2.7% | 27.5%/20.5% | 18.6 (interpolated) | pass | 0.175 (unverified) | 0.37 |
| 262 | `cfg_e318` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 14/122/0 | 136 | 36.8% | 6.5% | 0.79 | -9.8% | 254 | 1.52 | 16.5% | 60.2 | 10/10 | 0.90 | 0.37 | 0.42 | 3 | 22.1% | 0.36 | 0.56 | 35.4% | 35.0% | 51.9% | 32.7%/24.0% | 23.6 (interpolated) | pass | 0.140 (unverified) | 0.01 |
| 263 | `cfg_ab05` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=25, entry_z=-2.5, exit_z=-0.5, max_holding_bars=15, entry_confirmation=none, stop_atr_multiple=1.5 | 220/82/301 | 603 | 31.5% | 5.6% | 0.80 | -12.3% | 534 | 1.21 | 13.4% | 266.2 | 11/11 | 0.82 | 0.41 | 0.39 | 4 | 3.1% | 0.80 | 0.65 | 26.6% | 23.1% | 23.5% | 28.4%/19.7% | 5.7 (interpolated) | pass | 0.159 (unverified) | 0.38 |
| 264 | `cfg_87f7` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 5/82/69 | 156 | 25.8% | 4.7% | 0.80 | -7.8% | 237 | 1.43 | 7.8% | 69.0 | 12/12 | 0.92 | 0.45 | 0.35 | 5 | 14.0% | 0.40 | 0.73 | 25.0% | 23.3% | -2.2% | 23.8%/15.5% | 15.9 (interpolated) | pass | 0.146 (unverified) | -0.34 |
| 265 | `cfg_05eb` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 95/436/0 | 531 | 23.8% | 4.4% | 0.83 | -8.7% | 344 | 1.23 | 9.3% | 234.6 | 11/11 | 0.73 | 0.46 | 0.37 | 3 | 4.7% | 0.75 | 0.63 | 20.6% | 17.7% | 2.1% | 20.5%/16.1% | 5.3 (interpolated) | pass | 0.159 (unverified) | -0.20 |
| 266 | `cfg_028b` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 2/85/69 | 156 | 25.6% | 4.7% | 0.80 | -7.8% | 237 | 1.43 | 7.9% | 68.8 | 11/11 | 0.91 | 0.43 | 0.37 | 5 | 13.5% | 0.42 | 0.73 | 25.0% | 23.6% | -1.4% | 23.3%/17.5% | 16.0 (interpolated) | pass | 0.145 (unverified) | -0.34 |
| 267 | `cfg_b1e5` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 15/55/51 | 121 | 15.8% | 3.0% | 0.84 | -8.1% | 248 | 1.58 | 2.8% | 54.3 | 12/12 | 0.83 | 0.40 | 0.45 | 4 | 6.3% | 0.61 | 0.60 | 15.0% | 13.9% | 9.0% | 14.1%/11.1% | 12.7 (interpolated) | pass | 0.142 (unverified) | 0.23 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 9.6% / 1.47 / 42 | 7.3% / 2.01 / 24 | 10.4% / 1.44 / 26 | 6.6% / 2.04 / 22 | 7.3% / 1.11 / 41 |
| 2 | 7.9% / 1.33 / 55 | 8.0% / 2.17 / 29 | 9.6% / 1.38 / 31 | 5.1% / 1.70 / 26 | 6.2% / 0.88 / 66 |
| 3 | 14.1% / 2.76 / 24 | 0.3% / 0.17 / 12 | 22.2% / 1.61 / 20 | 4.9% / 2.05 / 18 | 8.5% / 1.46 / 28 |
| 4 | 8.3% / 1.38 / 47 | 6.9% / 1.96 / 27 | 5.8% / 0.85 / 30 | 7.4% / 2.32 / 22 | 7.1% / 1.04 / 54 |
| 5 | 4.8% / 1.70 / 23 | 2.2% / 1.05 / 20 | 10.8% / 1.95 / 23 | 5.2% / 2.47 / 12 | -2.7% / -0.96 / 30 |
| 6 | 12.2% / 2.61 / 24 | 0.1% / 0.05 / 13 | 20.8% / 1.72 / 21 | 3.5% / 1.56 / 19 | 9.1% / 1.58 / 31 |
| 7 | 5.5% / 0.91 / 26 | 5.1% / 1.64 / 15 | 24.0% / 1.85 / 23 | 14.7% / 2.82 / 21 | 3.9% / 0.62 / 21 |
| 8 | 11.3% / 1.86 / 56 | 5.8% / 1.63 / 28 | 8.0% / 1.09 / 31 | 3.6% / 1.37 / 21 | 6.1% / 0.87 / 63 |
| 9 | 10.1% / 1.62 / 38 | 3.1% / 0.73 / 21 | 9.2% / 1.38 / 22 | 4.5% / 1.48 / 17 | 4.9% / 0.90 / 33 |
| 10 | 13.2% / 1.94 / 42 | 2.5% / 0.75 / 15 | 10.0% / 1.39 / 19 | 4.5% / 1.54 / 18 | 5.0% / 0.84 / 32 |
| 11 | 6.4% / 1.28 / 32 | 1.8% / 0.74 / 16 | 15.6% / 1.24 / 28 | 9.3% / 2.57 / 23 | 7.2% / 1.11 / 26 |
| 12 | 7.1% / 1.54 / 32 | 2.3% / 1.04 / 16 | 12.5% / 1.05 / 28 | 7.8% / 2.37 / 23 | 8.0% / 1.28 / 27 |
| 13 | 6.6% / 1.21 / 38 | 0.7% / 0.21 / 24 | 9.9% / 1.41 / 22 | 4.7% / 1.50 / 17 | 7.2% / 1.08 / 45 |
| 14 | 6.8% / 1.15 / 49 | 5.4% / 1.68 / 27 | 11.8% / 1.47 / 30 | 4.7% / 1.44 / 23 | 3.8% / 0.55 / 65 |
| 15 | 6.2% / 1.38 / 32 | 2.3% / 1.03 / 16 | 13.1% / 1.09 / 28 | 7.4% / 2.29 / 23 | 8.4% / 1.32 / 27 |
| 16 | 3.1% / 0.49 / 42 | -0.3% / -0.09 / 27 | 12.5% / 1.09 / 33 | 11.4% / 2.82 / 32 | 9.5% / 1.43 / 37 |
| 17 | 7.4% / 1.24 / 49 | 5.1% / 1.64 / 27 | 12.0% / 1.50 / 30 | 5.2% / 1.52 / 23 | 4.9% / 0.70 / 65 |
| 18 | 2.9% / 0.47 / 42 | -0.4% / -0.14 / 27 | 13.4% / 1.16 / 33 | 11.3% / 2.82 / 32 | 9.3% / 1.41 / 37 |
| 19 | 9.4% / 1.61 / 43 | 0.0% / 0.02 / 24 | 9.7% / 1.52 / 23 | 4.8% / 1.62 / 17 | 6.1% / 0.94 / 45 |
| 20 | 9.1% / 1.60 / 49 | 1.1% / 0.33 / 27 | 11.2% / 1.75 / 25 | 2.2% / 0.78 / 22 | 8.0% / 1.11 / 57 |
| 21 | 5.0% / 1.70 / 23 | 2.3% / 1.06 / 20 | 9.5% / 1.92 / 23 | 6.0% / 2.32 / 12 | -3.0% / -1.10 / 30 |
| 22 | 15.8% / 2.95 / 25 | -0.4% / -0.17 / 12 | 18.1% / 1.25 / 22 | 6.2% / 2.29 / 18 | 6.0% / 1.00 / 30 |
| 23 | 4.2% / 0.66 / 41 | -1.1% / -0.37 / 25 | 14.0% / 1.03 / 31 | 10.5% / 2.70 / 29 | 11.0% / 1.64 / 32 |
| 24 | 9.4% / 1.44 / 42 | 4.4% / 1.53 / 21 | 8.4% / 1.30 / 24 | 6.6% / 1.89 / 19 | 4.8% / 0.74 / 40 |
| 25 | 7.0% / 1.29 / 42 | 1.7% / 0.51 / 27 | 11.8% / 1.67 / 24 | 0.5% / 0.19 / 21 | 9.6% / 1.28 / 57 |
| 26 | 12.5% / 1.84 / 42 | 2.5% / 0.75 / 15 | 12.1% / 1.58 / 19 | 3.5% / 0.97 / 21 | 5.0% / 0.84 / 32 |
| 27 | 9.1% / 1.40 / 39 | 4.3% / 1.49 / 21 | 8.1% / 1.24 / 24 | 8.5% / 2.20 / 19 | 5.6% / 0.85 / 39 |
| 28 | 3.7% / 0.68 / 39 | 0.2% / 0.08 / 17 | 22.5% / 1.56 / 29 | 4.7% / 1.65 / 22 | 7.5% / 1.28 / 33 |
| 29 | 4.7% / 1.90 / 23 | 3.6% / 1.85 / 22 | 11.7% / 1.80 / 23 | 2.1% / 1.21 / 13 | -1.0% / -0.41 / 35 |
| 30 | 6.6% / 1.15 / 34 | 3.5% / 0.80 / 21 | 9.8% / 1.32 / 21 | 3.8% / 0.96 / 20 | 6.0% / 1.04 / 33 |
| 31 | 3.6% / 1.45 / 23 | 2.6% / 1.30 / 22 | 11.7% / 1.91 / 22 | 3.7% / 1.80 / 13 | -0.3% / -0.15 / 31 |
| 32 | 10.3% / 2.35 / 27 | -0.1% / -0.09 / 10 | 22.1% / 1.82 / 20 | 2.2% / 1.26 / 14 | 3.0% / 0.66 / 31 |
| 33 | 8.1% / 1.18 / 44 | 4.9% / 1.35 / 24 | 5.6% / 0.76 / 25 | 6.5% / 2.20 / 16 | 2.8% / 0.48 / 38 |
| 34 | 4.2% / 0.66 / 49 | 2.7% / 0.86 / 16 | 9.7% / 1.29 / 21 | 4.3% / 1.44 / 21 | 7.3% / 1.15 / 42 |
| 35 | 7.4% / 1.26 / 43 | 4.5% / 1.54 / 23 | 2.2% / 0.37 / 28 | 8.2% / 2.38 / 20 | 4.8% / 0.75 / 47 |
| 36 | 3.7% / 0.59 / 49 | 2.9% / 0.92 / 16 | 11.8% / 1.45 / 21 | 4.4% / 1.36 / 21 | 7.9% / 1.24 / 42 |
| 37 | 1.8% / 0.30 / 58 | -0.9% / -0.30 / 33 | 18.9% / 1.45 / 37 | 9.9% / 2.60 / 31 | 9.1% / 1.27 / 54 |
| 38 | 5.5% / 1.45 / 37 | 4.7% / 2.24 / 23 | 6.4% / 1.22 / 26 | 1.4% / 0.85 / 14 | -1.5% / -0.47 / 39 |
| 39 | 9.0% / 1.46 / 36 | 6.8% / 1.88 / 23 | 6.6% / 0.90 / 25 | 6.5% / 1.94 / 21 | 3.4% / 0.56 / 38 |
| 40 | 7.8% / 1.12 / 34 | 7.0% / 1.48 / 17 | 10.4% / 1.42 / 13 | 5.1% / 1.54 / 14 | -0.5% / -0.06 / 30 |
| 41 | 1.8% / 0.30 / 58 | -0.6% / -0.17 / 33 | 19.5% / 1.48 / 37 | 9.8% / 2.60 / 31 | 9.2% / 1.28 / 54 |
| 42 | 7.8% / 1.12 / 34 | 7.0% / 1.48 / 17 | 10.4% / 1.42 / 13 | 5.1% / 1.54 / 14 | -0.5% / -0.06 / 30 |
| 43 | 6.2% / 1.05 / 53 | 1.8% / 0.49 / 24 | 12.6% / 1.63 / 24 | 0.3% / 0.13 / 24 | 9.6% / 1.31 / 52 |
| 44 | 1.5% / 0.26 / 43 | 1.3% / 0.48 / 19 | 16.9% / 1.36 / 30 | 2.6% / 0.98 / 22 | 9.7% / 1.46 / 44 |
| 45 | 5.9% / 0.95 / 38 | 0.4% / 0.13 / 22 | 8.5% / 1.49 / 22 | 4.0% / 1.36 / 15 | 8.4% / 1.40 / 38 |
| 46 | 1.5% / 0.26 / 43 | 1.4% / 0.53 / 19 | 16.0% / 1.30 / 30 | 2.7% / 1.01 / 22 | 9.8% / 1.47 / 44 |
| 47 | 6.2% / 1.05 / 53 | 1.8% / 0.48 / 24 | 13.0% / 1.68 / 24 | 0.3% / 0.11 / 24 | 9.2% / 1.27 / 52 |
| 48 | 9.5% / 1.63 / 51 | -1.2% / -0.32 / 28 | 8.3% / 1.15 / 26 | 4.8% / 1.66 / 20 | 5.0% / 0.73 / 59 |
| 49 | 6.2% / 1.55 / 34 | 3.6% / 1.64 / 22 | 6.5% / 1.33 / 25 | 2.7% / 1.46 / 12 | -1.2% / -0.35 / 33 |
| 50 | 5.5% / 2.34 / 24 | 3.3% / 1.94 / 26 | 3.8% / 1.10 / 26 | 2.2% / 1.70 / 14 | 0.3% / 0.19 / 37 |
| 51 | 8.0% / 1.34 / 43 | 4.3% / 1.50 / 23 | 2.2% / 0.37 / 28 | 8.6% / 2.42 / 20 | 5.6% / 0.87 / 47 |
| 52 | 3.0% / 0.59 / 43 | 0.3% / 0.13 / 19 | 20.3% / 1.51 / 30 | 3.5% / 1.46 / 22 | 8.6% / 1.39 / 44 |
| 53 | 6.1% / 2.26 / 25 | 3.5% / 2.35 / 25 | 3.8% / 1.08 / 28 | 3.1% / 2.13 / 14 | -4.5% / -1.90 / 41 |
| 54 | 9.8% / 2.03 / 27 | -0.2% / -0.13 / 10 | 19.0% / 1.64 / 20 | 2.5% / 1.33 / 14 | 5.8% / 1.02 / 31 |
| 55 | 8.2% / 1.41 / 39 | 2.6% / 0.75 / 23 | 9.4% / 1.23 / 19 | 5.5% / 1.43 / 16 | 3.0% / 0.51 / 39 |
| 56 | 3.9% / 1.37 / 29 | 3.3% / 1.72 / 27 | 12.2% / 1.93 / 28 | 0.1% / 0.05 / 15 | -2.8% / -1.16 / 31 |
| 57 | 2.4% / 0.79 / 29 | 1.9% / 0.91 / 26 | 11.9% / 1.96 / 26 | 1.5% / 0.88 / 15 | -2.2% / -0.86 / 29 |
| 58 | 1.8% / 0.41 / 30 | 2.8% / 1.13 / 19 | 10.4% / 0.92 / 26 | 5.5% / 1.61 / 23 | 9.8% / 1.57 / 32 |
| 59 | 4.8% / 0.82 / 31 | 0.6% / 0.24 / 17 | 19.0% / 1.51 / 22 | 2.7% / 1.10 / 17 | 2.8% / 0.46 / 42 |
| 60 | 4.4% / 0.68 / 36 | 3.9% / 1.13 / 23 | 12.5% / 0.87 / 31 | 5.5% / 1.71 / 17 | 13.0% / 1.74 / 40 |
| 61 | 6.9% / 1.33 / 31 | 1.3% / 0.59 / 13 | 18.6% / 1.44 / 21 | 5.1% / 1.82 / 17 | -1.0% / -0.12 / 35 |
| 62 | 6.4% / 1.20 / 47 | 3.2% / 0.86 / 37 | 4.2% / 0.85 / 28 | 2.0% / 0.76 / 24 | 6.0% / 0.93 / 56 |
| 63 | 9.0% / 1.50 / 50 | -1.2% / -0.31 / 27 | 8.5% / 1.12 / 25 | 3.9% / 1.43 / 19 | 6.5% / 0.92 / 59 |
| 64 | 3.5% / 0.54 / 52 | 2.2% / 0.62 / 32 | 23.4% / 1.48 / 37 | 7.7% / 2.08 / 26 | 4.5% / 0.65 / 58 |
| 65 | 7.4% / 1.19 / 39 | 2.1% / 0.67 / 21 | -0.8% / -0.09 / 20 | 7.7% / 2.26 / 16 | 6.4% / 1.01 / 38 |
| 66 | -1.5% / -0.31 / 39 | 4.3% / 1.52 / 37 | 14.4% / 1.71 / 36 | 5.9% / 1.75 / 26 | 0.8% / 0.25 / 45 |
| 67 | 4.5% / 0.71 / 37 | 3.7% / 1.05 / 27 | 16.3% / 1.07 / 29 | 4.5% / 1.52 / 18 | 12.9% / 1.70 / 49 |
| 68 | 4.8% / 0.72 / 36 | 3.9% / 1.14 / 23 | 11.6% / 0.78 / 29 | 5.0% / 1.60 / 17 | 12.9% / 1.73 / 40 |
| 69 | 3.7% / 0.55 / 52 | 2.0% / 0.60 / 32 | 23.7% / 1.49 / 37 | 7.7% / 2.08 / 26 | 4.7% / 0.66 / 58 |
| 70 | 11.4% / 1.50 / 33 | 4.4% / 1.03 / 27 | 13.0% / 1.09 / 30 | 8.6% / 1.52 / 31 | -3.2% / -0.48 / 28 |
| 71 | 7.5% / 1.00 / 37 | 3.7% / 0.92 / 28 | 12.0% / 1.02 / 32 | 9.1% / 1.71 / 34 | -0.2% / 0.00 / 31 |
| 72 | 2.0% / 0.43 / 30 | 3.7% / 1.36 / 19 | 8.4% / 0.76 / 26 | 4.2% / 1.33 / 22 | 9.8% / 1.51 / 31 |
| 73 | 9.8% / 1.66 / 40 | -1.2% / -0.37 / 22 | 7.3% / 1.00 / 23 | 5.7% / 1.62 / 22 | 4.7% / 0.78 / 43 |
| 74 | 9.8% / 1.66 / 40 | -1.2% / -0.37 / 22 | 7.3% / 1.00 / 23 | 5.8% / 1.64 / 22 | 4.7% / 0.78 / 43 |
| 75 | 6.4% / 1.20 / 47 | 2.1% / 0.56 / 36 | 4.0% / 0.81 / 28 | 2.8% / 1.02 / 24 | 6.3% / 0.93 / 56 |
| 76 | -0.3% / -0.12 / 22 | 4.3% / 2.09 / 19 | 8.5% / 1.63 / 20 | 2.6% / 1.57 / 8 | -0.7% / -0.21 / 31 |
| 77 | 5.3% / 0.88 / 61 | 3.5% / 1.21 / 36 | 6.3% / 0.69 / 38 | 5.3% / 1.41 / 32 | 4.6% / 0.67 / 64 |
| 78 | -1.0% / -0.25 / 49 | 2.8% / 1.05 / 44 | 21.8% / 2.22 / 53 | 4.2% / 1.46 / 43 | -2.3% / -0.46 / 70 |
| 79 | 6.7% / 0.95 / 47 | -0.6% / -0.17 / 31 | 12.5% / 1.21 / 33 | 9.9% / 2.35 / 33 | 1.7% / 0.28 / 50 |
| 80 | -1.7% / -0.38 / 39 | 4.2% / 1.49 / 37 | 14.6% / 1.72 / 36 | 5.1% / 1.62 / 26 | 0.7% / 0.21 / 45 |
| 81 | 15.7% / 2.30 / 25 | -1.9% / -0.60 / 12 | 11.5% / 0.82 / 22 | 7.5% / 2.18 / 18 | 8.9% / 1.30 / 29 |
| 82 | 6.0% / 2.29 / 25 | 3.4% / 2.29 / 25 | 4.0% / 1.14 / 28 | 3.0% / 2.11 / 14 | -4.5% / -1.90 / 41 |
| 83 | 7.9% / 1.24 / 42 | 2.1% / 0.67 / 21 | -2.8% / -0.51 / 20 | 6.6% / 2.10 / 16 | 6.4% / 1.00 / 39 |
| 84 | 14.3% / 2.18 / 25 | -0.9% / -0.34 / 13 | 9.8% / 0.76 / 23 | 6.3% / 2.08 / 19 | 9.2% / 1.40 / 32 |
| 85 | 7.9% / 1.14 / 44 | 1.9% / 0.67 / 21 | 2.0% / 0.32 / 23 | 6.3% / 2.14 / 14 | 3.9% / 0.65 / 38 |
| 86 | 12.2% / 1.97 / 31 | 4.0% / 1.02 / 19 | 0.9% / 0.15 / 20 | 5.7% / 1.40 / 20 | 3.6% / 0.69 / 30 |
| 87 | 12.2% / 1.97 / 31 | 4.0% / 1.02 / 19 | 0.9% / 0.15 / 20 | 4.7% / 1.20 / 20 | 3.7% / 0.69 / 30 |
| 88 | 13.7% / 2.06 / 30 | 3.9% / 0.93 / 17 | -0.3% / 0.02 / 19 | 3.6% / 1.13 / 12 | 8.9% / 1.48 / 30 |
| 89 | 1.7% / 0.32 / 28 | 4.7% / 1.59 / 17 | 16.7% / 1.20 / 24 | 4.9% / 1.28 / 19 | 2.9% / 0.57 / 20 |
| 90 | 0.5% / 0.11 / 63 | 2.2% / 0.64 / 42 | 22.8% / 1.40 / 42 | 3.2% / 1.05 / 27 | 7.5% / 1.05 / 58 |
| 91 | 0.5% / 0.11 / 63 | 1.7% / 0.51 / 42 | 23.3% / 1.42 / 42 | 3.6% / 1.15 / 27 | 7.2% / 1.01 / 58 |
| 92 | 7.7% / 1.21 / 41 | 1.1% / 0.27 / 21 | 1.0% / 0.20 / 21 | 6.6% / 2.40 / 14 | 5.3% / 0.85 / 35 |
| 93 | 7.1% / 1.00 / 47 | -0.6% / -0.17 / 31 | 11.4% / 1.12 / 33 | 8.5% / 2.07 / 32 | 2.4% / 0.38 / 50 |
| 94 | 7.8% / 1.20 / 40 | 1.1% / 0.27 / 21 | 1.2% / 0.20 / 20 | 7.9% / 2.61 / 14 | 6.8% / 1.07 / 35 |
| 95 | 4.2% / 0.67 / 37 | 3.5% / 1.01 / 27 | 11.3% / 0.76 / 32 | 4.9% / 1.65 / 18 | 12.1% / 1.65 / 49 |
| 96 | 9.7% / 1.67 / 31 | 3.8% / 1.18 / 17 | 5.5% / 0.68 / 14 | 0.8% / 0.28 / 16 | 6.5% / 0.97 / 49 |
| 97 | 8.1% / 1.48 / 40 | 3.7% / 1.13 / 31 | -0.5% / -0.05 / 22 | 6.3% / 2.00 / 19 | 2.6% / 0.42 / 39 |
| 98 | 3.4% / 0.60 / 39 | 2.9% / 0.92 / 26 | 11.5% / 1.16 / 31 | 5.9% / 1.74 / 30 | 1.4% / 0.37 / 41 |
| 99 | 3.7% / 0.68 / 24 | 4.4% / 1.45 / 17 | 18.0% / 1.27 / 23 | 5.5% / 1.38 / 19 | 0.6% / 0.13 / 19 |
| 100 | 3.1% / 0.99 / 29 | 5.7% / 2.10 / 27 | 13.6% / 1.88 / 30 | 1.6% / 0.90 / 16 | -5.5% / -1.61 / 34 |
| 101 | 8.1% / 1.31 / 52 | 2.3% / 0.84 / 22 | -0.1% / 0.03 / 26 | 5.7% / 1.89 / 16 | 5.4% / 0.83 / 50 |
| 102 | 9.7% / 1.67 / 31 | 3.8% / 1.18 / 17 | 5.5% / 0.68 / 14 | 0.9% / 0.32 / 16 | 6.4% / 0.95 / 49 |
| 103 | 1.8% / 0.52 / 23 | 1.7% / 0.77 / 24 | 8.1% / 1.54 / 24 | 3.4% / 1.63 / 15 | -0.3% / -0.12 / 28 |
| 104 | 10.8% / 1.96 / 21 | 1.4% / 0.52 / 17 | 17.2% / 1.44 / 17 | 0.6% / 0.39 / 12 | 3.5% / 0.69 / 34 |
| 105 | 10.8% / 1.96 / 21 | 1.4% / 0.52 / 17 | 17.2% / 1.44 / 17 | 0.6% / 0.39 / 12 | 3.5% / 0.69 / 34 |
| 106 | 10.2% / 1.61 / 40 | 0.6% / 0.20 / 20 | 0.7% / 0.15 / 19 | 4.2% / 1.23 / 13 | 8.1% / 1.42 / 35 |
| 107 | 11.0% / 1.69 / 40 | 0.6% / 0.20 / 20 | -1.4% / -0.19 / 18 | 4.2% / 1.23 / 13 | 10.3% / 1.72 / 35 |
| 108 | 9.1% / 1.56 / 37 | 5.8% / 1.83 / 26 | 2.6% / 0.45 / 22 | 5.2% / 1.68 / 17 | -2.3% / -0.41 / 31 |
| 109 | 9.2% / 1.59 / 49 | 2.1% / 0.61 / 27 | 7.9% / 1.29 / 24 | -0.2% / -0.04 / 28 | 5.9% / 0.82 / 57 |
| 110 | 6.6% / 1.16 / 48 | 1.9% / 0.59 / 27 | 4.8% / 0.87 / 23 | 3.9% / 1.36 / 20 | 4.8% / 0.69 / 66 |
| 111 | -1.7% / -0.22 / 58 | 2.1% / 0.66 / 39 | 19.8% / 1.45 / 48 | 9.8% / 2.48 / 36 | 2.8% / 0.44 / 61 |
| 112 | -2.8% / -0.40 / 29 | 4.0% / 1.02 / 26 | 13.5% / 1.34 / 29 | 10.6% / 2.24 / 22 | 8.5% / 1.07 / 32 |
| 113 | 7.8% / 1.44 / 32 | 1.6% / 0.41 / 26 | 6.8% / 1.18 / 25 | 5.1% / 1.47 / 17 | 2.9% / 0.51 / 37 |
| 114 | 12.2% / 1.65 / 45 | 1.2% / 0.48 / 24 | 7.1% / 0.72 / 27 | 6.3% / 1.49 / 30 | 6.0% / 0.92 / 43 |
| 115 | 6.9% / 1.31 / 37 | 1.7% / 0.57 / 28 | 1.5% / 0.28 / 22 | 7.4% / 2.23 / 19 | 2.2% / 0.36 / 39 |
| 116 | 10.5% / 1.94 / 50 | 3.4% / 0.98 / 25 | 10.7% / 1.42 / 23 | 1.3% / 0.41 / 20 | -0.1% / 0.03 / 71 |
| 117 | 10.1% / 1.77 / 46 | -0.4% / -0.13 / 21 | 8.9% / 1.17 / 27 | -0.0% / 0.01 / 23 | 9.3% / 1.16 / 63 |
| 118 | -0.5% / -0.10 / 49 | 3.3% / 1.22 / 44 | 17.8% / 1.91 / 53 | 3.9% / 1.34 / 43 | -0.6% / -0.11 / 70 |
| 119 | 5.6% / 0.89 / 38 | 0.4% / 0.13 / 22 | 7.8% / 1.35 / 22 | 3.8% / 1.32 / 15 | 6.6% / 1.10 / 38 |
| 120 | 6.0% / 0.88 / 45 | -1.8% / -0.65 / 27 | 7.1% / 0.57 / 35 | 13.5% / 2.87 / 32 | 7.9% / 1.10 / 42 |
| 121 | 3.4% / 0.62 / 39 | 1.5% / 0.56 / 26 | 11.0% / 1.25 / 31 | 6.5% / 2.31 / 30 | 0.7% / 0.22 / 41 |
| 122 | 7.7% / 2.21 / 43 | 4.0% / 1.97 / 32 | 2.2% / 0.61 / 38 | 0.8% / 0.65 / 17 | -0.5% / -0.19 / 50 |
| 123 | 5.2% / 1.98 / 23 | 3.3% / 1.68 / 22 | 9.8% / 1.57 / 25 | 3.5% / 1.90 / 14 | -4.2% / -1.29 / 38 |
| 124 | 2.6% / 0.38 / 35 | 5.4% / 1.47 / 21 | 8.5% / 0.59 / 27 | 6.6% / 1.89 / 16 | 12.9% / 1.81 / 36 |
| 125 | 4.9% / 0.90 / 53 | 4.5% / 1.44 / 34 | 4.2% / 0.76 / 35 | 4.5% / 1.53 / 22 | 3.8% / 0.58 / 58 |
| 126 | 2.2% / 0.32 / 35 | 5.1% / 1.42 / 21 | 7.5% / 0.53 / 28 | 6.7% / 1.99 / 16 | 12.6% / 1.77 / 36 |
| 127 | 12.1% / 1.86 / 34 | 2.7% / 0.66 / 18 | 5.0% / 0.59 / 21 | 3.0% / 0.91 / 14 | 7.0% / 1.11 / 34 |
| 128 | 19.1% / 1.85 / 38 | 2.0% / 0.55 / 27 | 3.6% / 0.28 / 32 | 13.2% / 2.37 / 33 | 7.9% / 1.09 / 31 |
| 129 | 3.0% / 1.05 / 19 | 2.2% / 0.98 / 20 | 10.2% / 1.62 / 20 | 3.7% / 1.93 / 13 | 1.1% / 0.58 / 30 |
| 130 | 7.4% / 1.27 / 42 | -1.5% / -0.49 / 18 | 21.8% / 1.28 / 31 | 5.5% / 1.82 / 22 | 3.8% / 0.56 / 43 |
| 131 | 6.0% / 0.91 / 31 | 3.4% / 1.25 / 11 | 15.5% / 1.01 / 18 | 5.8% / 1.78 / 17 | 3.0% / 0.47 / 31 |
| 132 | 5.5% / 0.98 / 45 | -1.5% / -0.52 / 21 | 19.1% / 1.29 / 32 | 3.9% / 1.53 / 22 | 5.4% / 0.81 / 51 |
| 133 | 4.2% / 0.65 / 33 | 0.1% / 0.05 / 22 | 4.5% / 0.99 / 21 | 3.7% / 1.17 / 14 | 8.7% / 1.60 / 34 |
| 134 | -2.2% / -0.36 / 31 | 4.8% / 1.24 / 27 | 12.9% / 1.33 / 30 | 7.8% / 1.86 / 22 | 10.2% / 1.31 / 35 |
| 135 | 5.1% / 0.96 / 38 | 3.6% / 1.02 / 27 | 1.3% / 0.29 / 27 | 5.8% / 1.84 / 18 | 3.2% / 0.54 / 44 |
| 136 | -4.1% / -0.72 / 52 | 3.3% / 1.13 / 34 | 8.7% / 1.00 / 40 | 8.3% / 2.57 / 26 | 7.8% / 1.10 / 45 |
| 137 | 7.3% / 1.28 / 39 | 0.7% / 0.27 / 21 | 10.3% / 1.26 / 18 | 4.5% / 1.21 / 15 | 2.5% / 0.45 / 39 |
| 138 | 2.1% / 0.56 / 23 | 0.3% / 0.16 / 24 | 7.9% / 1.51 / 24 | 3.5% / 1.58 / 15 | -0.5% / -0.21 / 28 |
| 139 | 7.4% / 1.32 / 31 | 3.2% / 1.22 / 11 | 12.8% / 0.88 / 18 | 6.3% / 1.93 / 17 | 1.9% / 0.32 / 31 |
| 140 | 6.6% / 1.16 / 48 | 1.7% / 0.54 / 27 | 4.9% / 0.87 / 23 | 4.6% / 1.47 / 20 | 2.7% / 0.39 / 66 |
| 141 | 6.1% / 1.68 / 40 | 4.6% / 2.29 / 27 | 3.7% / 0.88 / 33 | 0.7% / 0.53 / 16 | -2.2% / -0.77 / 47 |
| 142 | 4.8% / 2.01 / 23 | 3.0% / 1.65 / 24 | 3.5% / 0.99 / 23 | 2.0% / 1.47 / 14 | -0.4% / -0.18 / 37 |
| 143 | 3.1% / 1.08 / 19 | 1.8% / 0.80 / 20 | 8.8% / 1.52 / 20 | 3.9% / 2.01 / 13 | -0.0% / -0.00 / 29 |
| 144 | 12.3% / 1.66 / 45 | 1.5% / 0.57 / 24 | 6.3% / 0.65 / 27 | 4.5% / 1.11 / 29 | 5.8% / 0.90 / 43 |
| 145 | 11.9% / 2.13 / 27 | -2.3% / -0.78 / 10 | 13.8% / 0.95 / 21 | 4.4% / 1.61 / 14 | 5.7% / 0.92 / 30 |
| 146 | 9.8% / 1.44 / 43 | 3.3% / 0.83 / 33 | 6.4% / 0.68 / 42 | 3.3% / 0.82 / 36 | 3.1% / 0.58 / 35 |
| 147 | 10.1% / 1.38 / 42 | 5.0% / 1.21 / 31 | 2.0% / 0.24 / 37 | 7.8% / 1.48 / 36 | 2.6% / 0.49 / 33 |
| 148 | -1.0% / -0.11 / 58 | 2.5% / 0.75 / 39 | 18.6% / 1.36 / 48 | 7.1% / 1.94 / 34 | 1.8% / 0.30 / 59 |
| 149 | 3.7% / 0.70 / 51 | 2.7% / 0.94 / 35 | 3.2% / 0.62 / 33 | 6.3% / 1.90 / 26 | 2.7% / 0.41 / 64 |
| 150 | 12.4% / 1.84 / 35 | 4.5% / 1.04 / 21 | 0.6% / 0.12 / 19 | 2.9% / 0.80 / 18 | 2.1% / 0.43 / 28 |
| 151 | 5.3% / 1.03 / 28 | 0.1% / 0.04 / 25 | 6.1% / 1.03 / 25 | 6.1% / 1.68 / 17 | 1.2% / 0.22 / 37 |
| 152 | 5.3% / 1.42 / 37 | 4.3% / 2.25 / 23 | 6.9% / 1.36 / 24 | -0.1% / -0.09 / 14 | -3.2% / -1.08 / 39 |
| 153 | -2.9% / -0.68 / 44 | 4.9% / 1.81 / 29 | 2.8% / 0.52 / 25 | 4.5% / 2.09 / 16 | 10.1% / 1.41 / 43 |
| 154 | 9.4% / 1.58 / 42 | 1.0% / 0.31 / 24 | 5.3% / 0.87 / 22 | 2.2% / 0.67 / 23 | 3.0% / 0.47 / 48 |
| 155 | 20.0% / 1.98 / 44 | 1.9% / 0.53 / 28 | -1.9% / -0.01 / 36 | 11.4% / 1.99 / 35 | 9.6% / 1.39 / 33 |
| 156 | 15.7% / 1.78 / 38 | 3.7% / 0.97 / 27 | 6.1% / 0.42 / 34 | 10.0% / 2.09 / 34 | 6.8% / 0.97 / 33 |
| 157 | 3.7% / 1.23 / 29 | 5.4% / 1.99 / 27 | 12.8% / 1.79 / 30 | 1.5% / 0.81 / 16 | -6.7% / -2.04 / 34 |
| 158 | 8.8% / 1.22 / 54 | 1.5% / 0.42 / 28 | 13.8% / 1.33 / 33 | 2.0% / 0.61 / 30 | 2.7% / 0.43 / 58 |
| 159 | 10.0% / 1.57 / 34 | 2.0% / 0.53 / 17 | 4.0% / 0.50 / 17 | -0.7% / -0.29 / 14 | 10.8% / 1.73 / 34 |
| 160 | 10.4% / 2.02 / 27 | -1.5% / -0.59 / 10 | 10.7% / 0.82 / 22 | 3.9% / 1.68 / 14 | 7.1% / 1.15 / 32 |
| 161 | 19.1% / 2.18 / 44 | 1.4% / 0.41 / 28 | 5.3% / 0.39 / 37 | 9.4% / 1.92 / 36 | 3.1% / 0.49 / 35 |
| 162 | -2.1% / -0.45 / 39 | 1.2% / 0.46 / 31 | 16.8% / 2.11 / 40 | 4.4% / 1.71 / 31 | 1.5% / 0.37 / 46 |
| 163 | 8.8% / 1.22 / 54 | 1.5% / 0.42 / 28 | 13.8% / 1.33 / 33 | 2.4% / 0.72 / 30 | 2.7% / 0.43 / 58 |
| 164 | 3.2% / 0.71 / 54 | 10.0% / 2.98 / 40 | 12.3% / 1.33 / 55 | 3.1% / 0.96 / 30 | -5.7% / -1.26 / 62 |
| 165 | 17.4% / 1.88 / 44 | 0.4% / 0.10 / 35 | 11.8% / 0.73 / 43 | 13.2% / 2.07 / 43 | -2.5% / -0.27 / 46 |
| 166 | 9.7% / 1.81 / 50 | 1.0% / 0.37 / 23 | 11.3% / 1.40 / 22 | 0.4% / 0.15 / 19 | -0.0% / 0.03 / 71 |
| 167 | 7.2% / 1.04 / 43 | 2.1% / 0.55 / 33 | 6.9% / 0.73 / 41 | 4.2% / 1.04 / 36 | 4.2% / 0.76 / 35 |
| 168 | 10.0% / 1.57 / 34 | 1.7% / 0.49 / 17 | 4.0% / 0.50 / 17 | -0.4% / -0.16 / 14 | 9.9% / 1.57 / 34 |
| 169 | 8.4% / 1.19 / 55 | 0.5% / 0.15 / 37 | 10.4% / 1.03 / 41 | 4.5% / 1.24 / 26 | 3.7% / 0.57 / 62 |
| 170 | -4.0% / -0.59 / 52 | 5.2% / 1.65 / 34 | 6.4% / 0.69 / 40 | 8.7% / 2.64 / 25 | 8.1% / 1.13 / 45 |
| 171 | 7.0% / 1.24 / 55 | 1.7% / 0.59 / 38 | 4.7% / 0.51 / 47 | 9.3% / 2.72 / 29 | 0.9% / 0.16 / 61 |
| 172 | 12.6% / 1.93 / 50 | 4.8% / 1.47 / 31 | 12.0% / 0.84 / 48 | 8.7% / 2.46 / 30 | -5.1% / -0.83 / 71 |
| 173 | 5.4% / 0.85 / 44 | 2.4% / 0.72 / 32 | 13.4% / 0.85 / 34 | 3.5% / 0.95 / 25 | 8.8% / 1.26 / 56 |
| 174 | 5.9% / 0.81 / 42 | 5.4% / 1.29 / 30 | 2.7% / 0.31 / 36 | 8.0% / 1.54 / 36 | 3.6% / 0.65 / 33 |
| 175 | 16.3% / 2.42 / 39 | 2.5% / 0.73 / 18 | 8.6% / 0.93 / 20 | 1.2% / 0.43 / 18 | 0.7% / 0.13 / 50 |
| 176 | -0.7% / -0.08 / 34 | 4.2% / 1.30 / 22 | 5.2% / 0.50 / 21 | 4.5% / 1.44 / 15 | 16.9% / 2.57 / 34 |
| 177 | 5.1% / 1.91 / 23 | 3.6% / 1.72 / 22 | 8.8% / 1.23 / 25 | 3.5% / 1.92 / 14 | -2.6% / -0.79 / 36 |
| 178 | 13.4% / 2.06 / 50 | 4.8% / 1.48 / 31 | 11.3% / 0.80 / 48 | 8.5% / 2.42 / 30 | -4.2% / -0.66 / 71 |
| 179 | -1.4% / -0.11 / 35 | 4.3% / 0.78 / 24 | 9.1% / 1.00 / 21 | 9.2% / 1.68 / 24 | 12.5% / 1.51 / 42 |
| 180 | 2.0% / 0.67 / 56 | 0.5% / 0.27 / 43 | 14.2% / 2.03 / 52 | -1.0% / -0.45 / 44 | 2.2% / 0.59 / 68 |
| 181 | 2.2% / 0.44 / 38 | 1.2% / 0.37 / 27 | 7.3% / 0.66 / 25 | 3.1% / 1.21 / 16 | 14.1% / 2.02 / 50 |
| 182 | 16.3% / 2.42 / 39 | 2.7% / 0.77 / 18 | 8.5% / 0.91 / 20 | 0.8% / 0.30 / 18 | 0.8% / 0.16 / 50 |
| 183 | 9.4% / 1.32 / 50 | 0.2% / 0.10 / 28 | 4.9% / 0.46 / 37 | 6.5% / 1.75 / 30 | 5.7% / 0.88 / 49 |
| 184 | 11.0% / 2.09 / 46 | -0.3% / -0.08 / 26 | 2.0% / 0.50 / 23 | 1.7% / 0.81 / 15 | 4.7% / 0.70 / 64 |
| 185 | -5.4% / -1.17 / 42 | 5.8% / 1.85 / 27 | 4.3% / 0.77 / 23 | 5.5% / 2.15 / 15 | 9.3% / 1.28 / 40 |
| 186 | 11.7% / 1.82 / 37 | 3.3% / 0.79 / 22 | 4.1% / 0.67 / 20 | 3.3% / 0.86 / 20 | 0.6% / 0.13 / 33 |
| 187 | 0.7% / 0.14 / 41 | 4.3% / 1.21 / 26 | 14.5% / 0.95 / 34 | 10.6% / 2.36 / 24 | 7.4% / 1.03 / 41 |
| 188 | 1.3% / 0.51 / 22 | 2.7% / 1.50 / 19 | 7.7% / 1.56 / 20 | 2.5% / 1.53 / 8 | -1.2% / -0.40 / 31 |
| 189 | 3.4% / 0.60 / 46 | -0.4% / -0.10 / 26 | 10.2% / 0.69 / 33 | 12.4% / 3.02 / 32 | 8.4% / 1.42 / 34 |
| 190 | 9.7% / 1.34 / 27 | 0.4% / 0.11 / 21 | 5.0% / 0.71 / 14 | 10.1% / 1.86 / 17 | 3.7% / 0.52 / 28 |
| 191 | 10.3% / 1.78 / 39 | -0.8% / -0.22 / 20 | 7.1% / 0.86 / 24 | 1.3% / 0.45 / 17 | 4.9% / 0.65 / 55 |
| 192 | 4.9% / 1.41 / 43 | 1.6% / 1.06 / 44 | 8.2% / 1.18 / 42 | 1.7% / 0.98 / 22 | -0.9% / -0.27 / 63 |
| 193 | 1.9% / 0.42 / 53 | 10.0% / 3.07 / 40 | 11.6% / 1.33 / 55 | 3.6% / 1.07 / 30 | -5.0% / -0.99 / 62 |
| 194 | 9.6% / 1.75 / 46 | -0.1% / -0.00 / 26 | 5.2% / 0.96 / 23 | 1.0% / 0.51 / 15 | 3.2% / 0.48 / 64 |
| 195 | 11.2% / 1.25 / 70 | 4.1% / 0.80 / 42 | 7.2% / 0.76 / 38 | -0.3% / -0.03 / 35 | 8.2% / 0.85 / 72 |
| 196 | 5.4% / 0.78 / 45 | -2.2% / -0.81 / 27 | 6.1% / 0.50 / 35 | 14.5% / 2.91 / 32 | 8.4% / 1.16 / 42 |
| 197 | -1.7% / -0.22 / 34 | 4.7% / 1.44 / 22 | 2.5% / 0.27 / 20 | 5.1% / 1.62 / 14 | 17.2% / 2.56 / 34 |
| 198 | 7.5% / 1.15 / 41 | 2.2% / 0.68 / 23 | -0.6% / -0.06 / 32 | 5.8% / 1.42 / 28 | 6.7% / 1.10 / 39 |
| 199 | 7.7% / 1.17 / 41 | 2.6% / 0.78 / 23 | -2.0% / -0.30 / 32 | 6.6% / 1.55 / 28 | 6.0% / 0.96 / 39 |
| 200 | 10.0% / 1.20 / 57 | -2.3% / -0.44 / 36 | 10.2% / 1.05 / 27 | -0.2% / -0.03 / 25 | 14.1% / 1.41 / 71 |
| 201 | 6.4% / 1.25 / 44 | 1.1% / 0.42 / 28 | 8.6% / 1.45 / 28 | 3.2% / 1.16 / 21 | 4.8% / 0.66 / 73 |
| 202 | 1.8% / 0.32 / 37 | 5.0% / 1.37 / 30 | 17.7% / 2.57 / 31 | 5.2% / 1.81 / 27 | -6.1% / -1.15 / 37 |
| 203 | 6.9% / 1.28 / 27 | 3.3% / 0.81 / 23 | -0.6% / -0.18 / 15 | 3.2% / 0.97 / 15 | 4.1% / 0.80 / 30 |
| 204 | 6.0% / 0.80 / 48 | 2.6% / 0.69 / 24 | 13.3% / 1.16 / 33 | 4.9% / 1.37 / 26 | 1.7% / 0.30 / 46 |
| 205 | 4.7% / 1.39 / 43 | 1.6% / 1.06 / 44 | 8.3% / 1.18 / 42 | 1.7% / 0.98 / 22 | -1.1% / -0.31 / 63 |
| 206 | 6.0% / 0.80 / 48 | 2.6% / 0.70 / 24 | 13.3% / 1.16 / 33 | 4.5% / 1.28 / 26 | 2.0% / 0.34 / 46 |
| 207 | 3.3% / 0.60 / 166 | 7.8% / 1.84 / 120 | 22.8% / 1.28 / 150 | 9.8% / 1.85 / 136 | 1.1% / 0.18 / 218 |
| 208 | 1.1% / 0.20 / 41 | 4.3% / 1.23 / 26 | 13.8% / 0.91 / 34 | 10.4% / 2.37 / 24 | 6.8% / 0.96 / 41 |
| 209 | 2.9% / 0.52 / 46 | 0.6% / 0.19 / 26 | 7.6% / 0.54 / 33 | 12.7% / 2.99 / 29 | 8.1% / 1.31 / 33 |
| 210 | 5.5% / 0.81 / 49 | 4.0% / 1.11 / 25 | 15.2% / 1.23 / 33 | 1.8% / 0.50 / 28 | 3.6% / 0.61 / 44 |
| 211 | 15.8% / 1.55 / 57 | 1.2% / 0.29 / 33 | 13.6% / 0.84 / 39 | 10.8% / 1.72 / 42 | 3.1% / 0.47 / 44 |
| 212 | -1.1% / -0.18 / 42 | 5.9% / 1.87 / 36 | 8.0% / 1.15 / 44 | 5.9% / 1.84 / 27 | 1.4% / 0.49 / 46 |
| 213 | -1.4% / -0.27 / 42 | 5.9% / 2.04 / 36 | 8.1% / 1.16 / 44 | 5.3% / 1.76 / 27 | 0.1% / 0.05 / 46 |
| 214 | 3.1% / 0.96 / 56 | 2.0% / 0.92 / 44 | 14.4% / 2.06 / 51 | 1.2% / 0.47 / 44 | -2.7% / -0.54 / 68 |
| 215 | 5.7% / 0.83 / 49 | 4.5% / 1.25 / 25 | 14.4% / 1.16 / 33 | 2.4% / 0.65 / 28 | 4.5% / 0.72 / 44 |
| 216 | 7.7% / 1.38 / 27 | 2.4% / 0.60 / 23 | 2.1% / 0.51 / 15 | 3.5% / 1.04 / 15 | 2.2% / 0.44 / 29 |
| 217 | 5.6% / 1.01 / 59 | 2.9% / 1.03 / 38 | 5.0% / 0.54 / 47 | 8.6% / 2.62 / 29 | 1.3% / 0.23 / 61 |
| 218 | 18.1% / 2.35 / 24 | 1.7% / 0.36 / 22 | -0.5% / -0.00 / 16 | 10.2% / 2.34 / 18 | 1.1% / 0.22 / 24 |
| 219 | 1.5% / 0.25 / 34 | 4.3% / 1.17 / 21 | 6.6% / 0.52 / 23 | 5.4% / 1.58 / 14 | 14.4% / 1.82 / 39 |
| 220 | -0.0% / 0.02 / 33 | -0.5% / -0.23 / 16 | 15.0% / 1.28 / 29 | 4.9% / 1.37 / 22 | 5.2% / 0.85 / 37 |
| 221 | 2.3% / 0.41 / 30 | 3.9% / 0.95 / 19 | 19.4% / 1.23 / 24 | 12.0% / 2.01 / 23 | -3.3% / -0.44 / 24 |
| 222 | -1.3% / -0.56 / 47 | 1.6% / 0.54 / 49 | 15.2% / 2.61 / 43 | -0.5% / -0.33 / 38 | 0.9% / 0.23 / 50 |
| 223 | 4.3% / 0.78 / 166 | 7.2% / 1.75 / 120 | 20.5% / 1.19 / 150 | 9.7% / 1.86 / 140 | -1.9% / -0.23 / 218 |
| 224 | 10.3% / 1.37 / 30 | 2.6% / 0.63 / 19 | 11.0% / 0.76 / 24 | 8.5% / 1.52 / 23 | -0.5% / -0.05 / 22 |
| 225 | 9.3% / 1.57 / 26 | 2.8% / 0.74 / 21 | -2.5% / -0.67 / 15 | 4.1% / 1.34 / 15 | 3.8% / 0.76 / 26 |
| 226 | 12.1% / 1.37 / 57 | 1.0% / 0.27 / 33 | 12.1% / 0.75 / 41 | 11.4% / 2.07 / 43 | 2.0% / 0.32 / 47 |
| 227 | 4.3% / 1.57 / 23 | 2.2% / 1.09 / 22 | 9.1% / 1.42 / 24 | 4.7% / 2.35 / 14 | -4.5% / -1.12 / 32 |
| 228 | -4.0% / -0.92 / 39 | 2.4% / 0.79 / 31 | 14.5% / 1.49 / 40 | 6.0% / 2.19 / 31 | 3.1% / 0.66 / 46 |
| 229 | -0.3% / -0.02 / 53 | 7.8% / 2.31 / 38 | 15.9% / 1.87 / 50 | 5.5% / 1.62 / 28 | -7.0% / -1.36 / 55 |
| 230 | 4.7% / 0.90 / 43 | 1.2% / 0.45 / 28 | 8.1% / 1.37 / 28 | 2.9% / 1.06 / 21 | 3.8% / 0.52 / 73 |
| 231 | 10.7% / 1.57 / 43 | 3.1% / 1.07 / 22 | 2.1% / 0.34 / 28 | 2.6% / 1.18 / 11 | 6.4% / 1.14 / 35 |
| 232 | 4.2% / 0.56 / 28 | 9.3% / 1.88 / 23 | 7.1% / 0.49 / 24 | 12.4% / 2.40 / 21 | 3.3% / 0.59 / 27 |
| 233 | 3.5% / 0.85 / 46 | 5.8% / 1.92 / 36 | 7.4% / 1.10 / 36 | 4.1% / 1.55 / 31 | -2.4% / -0.66 / 45 |
| 234 | -4.2% / -0.53 / 110 | 2.2% / 0.53 / 93 | 31.8% / 1.66 / 106 | 11.0% / 2.12 / 90 | -1.9% / -0.24 / 111 |
| 235 | 9.2% / 1.39 / 34 | -0.8% / -0.19 / 18 | 11.0% / 1.00 / 26 | 11.3% / 3.03 / 24 | -5.2% / -1.00 / 29 |
| 236 | 4.3% / 0.74 / 32 | 1.9% / 0.59 / 20 | 18.5% / 1.27 / 25 | 3.1% / 1.27 / 10 | 8.5% / 1.27 / 45 |
| 237 | 3.9% / 0.73 / 27 | -2.3% / -0.51 / 16 | 5.3% / 1.10 / 17 | 4.6% / 1.73 / 13 | 6.7% / 1.31 / 29 |
| 238 | -1.9% / -0.16 / 35 | 1.2% / 0.26 / 22 | 10.3% / 1.09 / 20 | 9.3% / 1.58 / 21 | 12.5% / 1.40 / 39 |
| 239 | 0.4% / 0.18 / 47 | 1.4% / 0.50 / 49 | 14.3% / 2.35 / 43 | -0.4% / -0.23 / 38 | -0.1% / -0.01 / 50 |
| 240 | 8.0% / 1.26 / 30 | 1.5% / 0.36 / 25 | -1.3% / -0.38 / 17 | 3.1% / 1.01 / 16 | 7.0% / 1.17 / 30 |
| 241 | -2.0% / -0.28 / 104 | 6.4% / 1.40 / 87 | 22.2% / 1.67 / 105 | 9.1% / 1.86 / 86 | -1.4% / -0.16 / 111 |
| 242 | 7.5% / 1.23 / 26 | 5.7% / 1.22 / 18 | 3.5% / 0.42 / 21 | 5.4% / 1.39 / 19 | 3.1% / 0.48 / 32 |
| 243 | 8.0% / 1.26 / 30 | 1.5% / 0.36 / 25 | -1.3% / -0.38 / 17 | 3.1% / 1.01 / 16 | 6.8% / 1.14 / 30 |
| 244 | 11.5% / 1.27 / 41 | -2.5% / -0.57 / 27 | 11.8% / 0.90 / 31 | 15.0% / 2.41 / 33 | -2.9% / -0.34 / 31 |
| 245 | -6.1% / -0.66 / 28 | 8.1% / 1.27 / 26 | 6.0% / 0.52 / 25 | 19.0% / 3.02 / 24 | 8.5% / 1.00 / 37 |
| 246 | 9.0% / 1.31 / 43 | 3.2% / 1.08 / 22 | 2.2% / 0.35 / 28 | 2.8% / 1.21 / 11 | 6.1% / 1.09 / 35 |
| 247 | 7.3% / 1.22 / 23 | 1.1% / 0.27 / 15 | 0.4% / 0.08 / 18 | 10.3% / 2.17 / 16 | 6.6% / 0.88 / 29 |
| 248 | 5.6% / 0.94 / 32 | 2.1% / 0.63 / 20 | 19.4% / 1.34 / 25 | 2.4% / 1.01 / 10 | 8.3% / 1.27 / 45 |
| 249 | 10.6% / 1.25 / 56 | -0.6% / -0.08 / 36 | 14.3% / 1.35 / 27 | 0.0% / 0.03 / 25 | 6.8% / 0.73 / 67 |
| 250 | 8.7% / 1.51 / 29 | 3.2% / 0.86 / 21 | -1.7% / -0.49 / 15 | 3.8% / 1.28 / 17 | 3.4% / 0.63 / 30 |
| 251 | -6.6% / -1.16 / 114 | 4.0% / 1.38 / 87 | 21.4% / 2.58 / 112 | -1.2% / -0.29 / 89 | 8.7% / 1.51 / 132 |
| 252 | 7.0% / 1.27 / 49 | 2.5% / 0.71 / 26 | 4.6% / 0.71 / 30 | 3.3% / 0.98 / 27 | 3.4% / 0.51 / 52 |
| 253 | 4.1% / 0.65 / 30 | 4.2% / 1.00 / 19 | 20.8% / 1.26 / 24 | 11.6% / 1.88 / 23 | -3.1% / -0.42 / 24 |
| 254 | 0.3% / 0.07 / 37 | 5.1% / 1.38 / 30 | 15.2% / 2.30 / 31 | 5.0% / 1.73 / 27 | -5.6% / -1.09 / 37 |
| 255 | 14.3% / 1.74 / 27 | 2.0% / 0.52 / 15 | 10.9% / 0.77 / 21 | 8.8% / 1.72 / 17 | 1.4% / 0.26 / 24 |
| 256 | 7.7% / 1.33 / 55 | 2.8% / 0.95 / 23 | 7.7% / 1.19 / 33 | -0.7% / -0.34 / 16 | 2.4% / 0.36 / 66 |
| 257 | 9.1% / 2.03 / 34 | 2.4% / 0.69 / 22 | 5.8% / 1.21 / 16 | -2.3% / -1.12 / 20 | 2.9% / 0.49 / 46 |
| 258 | 9.1% / 2.03 / 34 | 2.4% / 0.69 / 22 | 5.8% / 1.21 / 16 | -2.3% / -1.12 / 20 | 2.9% / 0.49 / 46 |
| 259 | 2.0% / 0.46 / 40 | 6.1% / 1.96 / 36 | 14.5% / 1.57 / 43 | 5.4% / 1.74 / 33 | -3.4% / -0.52 / 46 |
| 260 | 6.7% / 0.95 / 58 | 3.1% / 1.10 / 23 | 8.4% / 0.84 / 36 | 6.5% / 2.00 / 22 | 1.0% / 0.18 / 56 |
| 261 | 10.1% / 1.53 / 42 | 1.3% / 0.41 / 29 | 11.5% / 0.88 / 32 | 2.4% / 0.95 / 13 | 4.2% / 0.70 / 47 |
| 262 | -0.7% / -0.03 / 35 | -0.2% / 0.01 / 22 | 11.6% / 1.19 / 19 | 12.0% / 1.88 / 21 | 10.5% / 1.11 / 39 |
| 263 | -8.4% / -1.27 / 136 | 0.2% / 0.08 / 107 | 27.6% / 2.23 / 118 | 7.8% / 1.69 / 114 | 4.2% / 0.59 / 128 |
| 264 | 10.4% / 1.38 / 41 | 2.1% / 0.65 / 23 | 3.4% / 0.47 / 26 | 2.4% / 0.85 / 21 | 5.4% / 0.83 / 45 |
| 265 | -6.7% / -1.16 / 114 | 4.5% / 1.52 / 87 | 18.2% / 2.45 / 111 | -1.7% / -0.40 / 88 | 9.2% / 1.54 / 131 |
| 266 | 10.7% / 1.42 / 41 | 2.1% / 0.65 / 23 | 3.4% / 0.47 / 26 | 2.3% / 0.82 / 21 | 5.0% / 0.79 / 45 |
| 267 | 5.6% / 1.72 / 23 | 3.4% / 1.77 / 22 | 8.9% / 1.52 / 25 | 5.4% / 2.11 / 14 | -7.6% / -2.44 / 37 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_ad5d` | 9 | 0.83 | 0.82/0.90 | 0.68/0.82 |
| 1 | `cfg_42ce` | 7 | 0.90 | 0.89/0.93 | 0.64/0.72 |
| 2 | `cfg_ecd5` | 39 | 0.85 | 0.75/0.80 | 0.51/0.68 |
| 3 | `cfg_f526` | 19 | 0.91 | 0.85/0.93 | 0.66/0.77 |
| 4 | `cfg_d9a8` | 20 | 0.82 | 0.76/0.85 | 0.64/0.74 |
| 5 | `cfg_87f7` | 5 | 0.99 | 0.98/1.00 | 0.98/1.00 |
| 6 | `cfg_7b2e` | 11 | 0.83 | 0.81/0.89 | 0.53/0.67 |
| 7 | `cfg_3694` | 6 | 0.88 | 0.88/0.88 | 0.80/0.82 |
| 8 | `cfg_df4d` | 9 | 0.91 | 0.92/0.92 | 0.87/0.88 |
| 9 | `cfg_0364` | 5 | 0.90 | 0.93/0.94 | 0.93/0.93 |
| 10 | `cfg_0392` | 3 | 0.94 | 0.97/0.98 | 0.90/0.94 |
| 11 | `cfg_afcf` | 46 | 0.84 | 0.72/0.86 | 0.31/0.50 |
| 12 | `cfg_053f` | 5 | 0.95 | 0.97/0.97 | 0.91/0.93 |
| 13 | `cfg_12e6` | 10 | 0.86 | 0.91/0.96 | 0.85/0.88 |
| 14 | `cfg_6ad1` | 5 | 0.97 | 0.98/0.99 | 0.95/0.96 |
| 15 | `cfg_49c6` | 5 | 0.93 | 0.95/0.98 | 0.84/0.92 |
| 16 | `cfg_05cd` | 2 | 0.90 | 0.94/0.94 | 0.93/0.93 |
| 17 | `cfg_d18c` | 2 | 0.97 | 0.96/0.96 | 0.99/0.99 |
| 18 | `cfg_a5ef` | 4 | 0.92 | 0.96/0.96 | 0.86/0.88 |
| 19 | `cfg_274c` | 6 | 0.90 | 0.90/0.96 | 0.93/0.95 |
| 20 | `cfg_0631` | 3 | 0.92 | 0.96/0.96 | 0.86/0.86 |
| 21 | `cfg_69c0` | 13 | 0.82 | 0.79/0.86 | 0.46/0.60 |
| 22 | `cfg_d889` | 10 | 0.83 | 0.79/0.81 | 0.59/0.66 |
| 23 | `cfg_eade` | 5 | 0.95 | 0.96/0.96 | 0.97/0.97 |
| 24 | `cfg_d8e5` | 10 | 0.88 | 0.85/0.90 | 0.84/0.90 |
| 25 | `cfg_2506` | 3 | 0.97 | 0.98/0.98 | 0.92/0.94 |
| 26 | `cfg_49ca` | 10 | 0.89 | 0.92/0.94 | 0.89/0.91 |
| 27 | `cfg_0725` | 2 | 0.85 | 0.72/0.72 | 0.36/0.36 |
| 28 | `cfg_088e` | 8 | 0.84 | 0.82/0.86 | 0.75/0.85 |
| 29 | `cfg_0bd4` | 7 | 0.87 | 0.88/0.93 | 0.85/0.95 |
| 30 | `cfg_08ce` | 1 | n/a | n/a/n/a | n/a/n/a |
| 31 | `cfg_3a13` | 10 | 0.81 | 0.82/0.87 | 0.72/0.77 |
| 32 | `cfg_caff` | 5 | 1.00 | 1.00/1.00 | 0.99/0.99 |
| 33 | `cfg_0b38` | 1 | n/a | n/a/n/a | n/a/n/a |
| 34 | `cfg_d8c7` | 19 | 0.83 | 0.80/0.91 | 0.52/0.76 |
| 35 | `cfg_4a22` | 6 | 0.89 | 0.92/0.99 | 0.83/0.96 |
| 36 | `cfg_0cec` | 1 | n/a | n/a/n/a | n/a/n/a |
| 37 | `cfg_b4e2` | 10 | 0.84 | 0.83/0.88 | 0.66/0.76 |
| 38 | `cfg_d8bd` | 25 | 0.88 | 0.78/0.84 | 0.39/0.51 |
| 39 | `cfg_7e52` | 4 | 0.92 | 0.97/0.98 | 0.85/0.89 |
| 40 | `cfg_0ef9` | 23 | 0.80 | 0.23/0.77 | 0.14/0.43 |
| 41 | `cfg_a055` | 10 | 0.85 | 0.87/0.93 | 0.51/0.63 |
| 42 | `cfg_50e5` | 15 | 0.82 | 0.85/0.94 | 0.76/0.85 |
| 43 | `cfg_69e3` | 4 | 0.82 | 0.94/0.95 | 0.86/0.89 |
| 44 | `cfg_f63d` | 3 | 0.96 | 0.92/0.95 | 0.90/0.93 |
| 45 | `cfg_7fa2` | 10 | 0.93 | 0.89/0.93 | 0.61/0.75 |
| 46 | `cfg_c54f` | 2 | 0.88 | 0.91/0.91 | 0.80/0.80 |
| 47 | `cfg_474c` | 5 | 0.93 | 0.97/0.97 | 0.96/0.96 |
| 48 | `cfg_1356` | 1 | n/a | n/a/n/a | n/a/n/a |
| 49 | `cfg_b861` | 10 | 0.88 | 0.90/0.92 | 0.80/0.86 |
| 50 | `cfg_13d3` | 10 | 0.87 | 0.86/0.95 | 0.63/0.80 |
| 51 | `cfg_3c25` | 10 | 0.82 | 0.81/0.84 | 0.58/0.59 |
| 52 | `cfg_b8d1` | 5 | 0.91 | 0.94/0.98 | 0.83/0.94 |
| 53 | `cfg_8db2` | 4 | 0.97 | 0.98/0.98 | 0.96/0.96 |
| 54 | `cfg_de5e` | 8 | 0.88 | 0.86/0.87 | 0.76/0.79 |
| 55 | `cfg_b5cc` | 5 | 0.96 | 0.98/0.98 | 0.94/0.94 |
| 56 | `cfg_2ac6` | 9 | 0.87 | 0.89/0.93 | 0.69/0.78 |
| 57 | `cfg_9d59` | 4 | 0.99 | 0.99/0.99 | 0.98/0.98 |
| 58 | `cfg_f2fb` | 10 | 0.83 | 0.86/0.90 | 0.74/0.76 |
| 59 | `cfg_84c5` | 4 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 60 | `cfg_4d08` | 2 | 0.90 | 0.87/0.87 | 0.81/0.81 |
| 61 | `cfg_ce69` | 10 | 0.82 | 0.84/0.91 | 0.69/0.79 |
| 62 | `cfg_cb84` | 3 | 0.82 | 0.84/0.84 | 0.75/0.78 |
| 63 | `cfg_bc34` | 4 | 0.85 | 0.83/0.89 | 0.67/0.67 |
| 64 | `cfg_c9de` | 6 | 0.85 | 0.87/0.99 | 0.87/0.99 |
| 65 | `cfg_f5d6` | 4 | 0.99 | 1.00/1.00 | 0.98/0.98 |
| 66 | `cfg_8728` | 10 | 0.90 | 0.92/0.96 | 0.80/0.86 |
| 67 | `cfg_8214` | 5 | 0.83 | 0.88/0.94 | 0.84/0.87 |
| 68 | `cfg_7f69` | 4 | 0.89 | 0.89/0.99 | 0.81/0.95 |
| 69 | `cfg_a1c3` | 3 | 0.88 | 0.85/0.88 | 0.76/0.84 |
| 70 | `cfg_5889` | 5 | 0.89 | 0.94/0.99 | 0.86/0.97 |
| 71 | `cfg_f913` | 13 | 0.84 | 0.85/0.93 | 0.80/0.90 |
| 72 | `cfg_976c` | 8 | 0.91 | 0.89/0.91 | 0.88/0.94 |
| 73 | `cfg_237a` | 5 | 0.89 | 0.89/0.93 | 0.83/0.93 |
| 74 | `cfg_2443` | 1 | n/a | n/a/n/a | n/a/n/a |
| 75 | `cfg_e8be` | 3 | 0.83 | 0.57/0.62 | 0.39/0.41 |
| 76 | `cfg_27d8` | 3 | 0.87 | 0.96/0.97 | 0.87/0.90 |
| 77 | `cfg_5cd8` | 6 | 0.86 | 0.93/0.93 | 0.87/0.91 |
| 78 | `cfg_cfbb` | 4 | 0.97 | 0.80/0.82 | 0.88/0.95 |
| 79 | `cfg_ed80` | 4 | 0.89 | 0.95/0.98 | 0.92/0.97 |
| 80 | `cfg_8625` | 10 | 0.84 | 0.71/0.75 | 0.58/0.61 |
| 81 | `cfg_2c21` | 1 | n/a | n/a/n/a | n/a/n/a |
| 82 | `cfg_2d4a` | 4 | 0.87 | 0.87/0.89 | 0.77/0.78 |
| 83 | `cfg_2d81` | 4 | 0.81 | 0.75/0.77 | 0.80/0.81 |
| 84 | `cfg_8e2a` | 4 | 0.88 | 0.92/0.96 | 0.72/0.86 |
| 85 | `cfg_b7a4` | 3 | 0.94 | 0.98/0.99 | 0.97/0.98 |
| 86 | `cfg_2e7d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 87 | `cfg_30bd` | 2 | 0.91 | 0.91/0.91 | 0.81/0.81 |
| 88 | `cfg_74e2` | 5 | 0.98 | 0.99/0.99 | 0.98/0.98 |
| 89 | `cfg_316f` | 3 | 0.90 | 0.90/0.93 | 0.88/0.91 |
| 90 | `cfg_3186` | 1 | n/a | n/a/n/a | n/a/n/a |
| 91 | `cfg_d69e` | 4 | 0.99 | 0.99/1.00 | 0.96/0.98 |
| 92 | `cfg_3497` | 3 | 0.94 | 0.95/0.96 | 0.90/0.92 |
| 93 | `cfg_59a6` | 7 | 0.90 | 0.93/0.96 | 0.74/0.86 |
| 94 | `cfg_75ff` | 4 | 0.86 | 0.87/0.96 | 0.91/0.94 |
| 95 | `cfg_a09d` | 3 | 0.92 | 0.92/0.93 | 0.73/0.82 |
| 96 | `cfg_391b` | 2 | 0.93 | 0.94/0.94 | 0.81/0.81 |
| 97 | `cfg_e163` | 7 | 0.87 | 0.89/0.98 | 0.62/0.98 |
| 98 | `cfg_bfd9` | 5 | 0.90 | 0.93/0.94 | 0.91/0.92 |
| 99 | `cfg_f8d1` | 10 | 0.85 | 0.83/0.87 | 0.69/0.76 |
| 100 | `cfg_dda7` | 5 | 1.00 | 1.00/1.00 | 0.96/0.99 |
| 101 | `cfg_8576` | 5 | 0.91 | 0.94/0.98 | 0.96/0.96 |
| 102 | `cfg_d84f` | 5 | 0.87 | 0.93/0.94 | 0.95/0.95 |
| 103 | `cfg_9032` | 4 | 0.88 | 0.92/0.99 | 0.87/0.98 |
| 104 | `cfg_89f3` | 3 | 0.96 | 0.95/0.97 | 0.99/0.99 |
| 105 | `cfg_6f44` | 5 | 0.98 | 0.98/0.99 | 0.89/0.99 |
| 106 | `cfg_433b` | 1 | n/a | n/a/n/a | n/a/n/a |
| 107 | `cfg_44a9` | 6 | 0.82 | 0.93/0.96 | 0.80/0.82 |
| 108 | `cfg_9566` | 5 | 1.00 | 1.00/1.00 | 0.99/1.00 |
| 109 | `cfg_5d0b` | 5 | 0.96 | 0.99/1.00 | 0.94/1.00 |
| 110 | `cfg_ba40` | 6 | 0.88 | 0.93/0.97 | 0.70/0.89 |
| 111 | `cfg_4bc2` | 2 | 0.94 | 0.96/0.96 | 0.92/0.92 |
| 112 | `cfg_cb21` | 5 | 0.90 | 0.85/0.90 | 0.79/0.87 |
| 113 | `cfg_5182` | 2 | 0.93 | 0.94/0.94 | 0.90/0.90 |
| 114 | `cfg_52bf` | 1 | n/a | n/a/n/a | n/a/n/a |
| 115 | `cfg_55ca` | 3 | 0.87 | 0.91/0.93 | 0.84/0.85 |
| 116 | `cfg_a717` | 5 | 0.85 | 0.95/0.99 | 0.67/0.94 |
| 117 | `cfg_abdf` | 4 | 0.87 | 0.92/0.94 | 0.86/0.88 |
| 118 | `cfg_aa56` | 8 | 0.88 | 0.87/0.97 | 0.63/0.97 |
| 119 | `cfg_c3f6` | 4 | 0.97 | 0.96/0.99 | 0.96/0.98 |
| 120 | `cfg_902b` | 7 | 0.88 | 0.93/0.96 | 0.73/0.89 |
| 121 | `cfg_6236` | 2 | 0.85 | 0.85/0.85 | 0.73/0.73 |
| 122 | `cfg_6969` | 3 | 0.87 | 0.81/0.85 | 0.67/0.74 |
| 123 | `cfg_6974` | 1 | n/a | n/a/n/a | n/a/n/a |
| 124 | `cfg_f560` | 2 | 0.95 | 0.97/0.97 | 0.89/0.89 |
| 125 | `cfg_7275` | 2 | 0.98 | 0.98/0.98 | 0.89/0.89 |
| 126 | `cfg_732d` | 5 | 0.85 | 0.87/0.90 | 0.60/0.75 |
| 127 | `cfg_8367` | 1 | n/a | n/a/n/a | n/a/n/a |
| 128 | `cfg_8789` | 1 | n/a | n/a/n/a | n/a/n/a |
| 129 | `cfg_ea75` | 3 | 0.85 | 0.77/0.86 | 0.72/0.80 |
| 130 | `cfg_8d06` | 1 | n/a | n/a/n/a | n/a/n/a |
| 131 | `cfg_8e3d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 132 | `cfg_8fbb` | 1 | n/a | n/a/n/a | n/a/n/a |
| 133 | `cfg_9559` | 1 | n/a | n/a/n/a | n/a/n/a |
| 134 | `cfg_fa98` | 4 | 0.96 | 0.96/1.00 | 0.92/0.99 |
| 135 | `cfg_d314` | 3 | 0.99 | 0.99/0.99 | 0.94/0.95 |
| 136 | `cfg_9bfa` | 2 | 0.96 | 0.98/0.98 | 0.92/0.92 |
| 137 | `cfg_a69a` | 1 | n/a | n/a/n/a | n/a/n/a |
| 138 | `cfg_a86e` | 1 | n/a | n/a/n/a | n/a/n/a |
| 139 | `cfg_ab05` | 1 | n/a | n/a/n/a | n/a/n/a |
| 140 | `cfg_c053` | 1 | n/a | n/a/n/a | n/a/n/a |
| 141 | `cfg_c42d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 142 | `cfg_cd51` | 1 | n/a | n/a/n/a | n/a/n/a |
| 143 | `cfg_cfc0` | 2 | 0.94 | 0.86/0.86 | 0.77/0.77 |
| 144 | `cfg_f1c6` | 1 | n/a | n/a/n/a | n/a/n/a |
| 145 | `cfg_f9bd` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 5.928e-04 over 70421 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1152.0, participation ratio 10.0, 95%-variance components 213 (rank bound T = 1259); raw grid 72000; raw + known prior 649032
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
- Session: NYSE regular session only (09:30-16:00 NY, NYSE early closes/holidays), matching the SPY studies; overnight Globex bars are not traded or used in indicators.
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
