# Screening funnel -- mr_nq_v5 (development stages only)

- Code: `3b70ca612d69` (dirty working tree: True, diff sha256 `3f5fdfb3ee59`)
- Config: `configs/funnel/mr_funnel_nq_v5.yaml` sha256 `3bda8634c9952c4c`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ES': '2026-10-16', 'NQ': '2026-10-16'}
- Frozen manifest sha256: `1286075dfbb8bf5b` (93 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **False** -- No strategy has been selected on NQ 2023-2024. But NQ is highly correlated with ES, and this v5 grid and the 40-trade validation rule were chosen after reading ES 2023-2024 results (mr_es_v3..v5); QQQ 2023-2024 was never used to gate. So the slice is not fully independent of earlier research.
- Holdout 2025+ previously inspected: **False** -- No NQ strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 41472 | 41472 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 41472 | 41472 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 41472 | 29508 | 11964 | 0 |  | 33604 | 71.15 | 71.15 |  |
| 3 performance & risk | hard_gate | 29508 | 190 | 29318 | 0 |  | 0 | 0.46 | 0.64 |  |
| 4 parameter stability | hard_gate | 190 | 166 | 24 | 0 |  | 0 | 0.40 | 87.37 |  |
| 5 time stability | hard_gate | 166 | 157 | 9 | 0 |  | 149 | 0.38 | 94.58 |  |
| 6 deduplication | dedup | 157 | 93 |  |  | 64 |  | 0.22 | 59.24 | best 2 per cluster |
| 7 execution stress | hard_gate | 93 | 93 | 0 | 0 |  | 0 | 0.22 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 93 |  |  |  |  |  |  |  | diagnostic only: unverified: 93 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 11956 |
| s2:hard_reject:years_with_>=10_trades | 8714 |
| s3:hard_reject:max_drawdown | 2622 |
| s3:hard_reject:net_return | 20765 |
| s3:hard_reject:sharpe | 29318 |
| s4:hard_reject:local_frac_profitable | 2 |
| s4:hard_reject:local_median_sharpe | 24 |
| s5:hard_reject:profitable_years | 9 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_1463` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 52/20/32 | 104 | 53.4% | 8.9% | 1.16 | -6.5% | 157 | 1.84 | 8.5% | 53.4 | 11/11 | 0.91 | 0.61 | 0.55 | 4 | 22.6% | 0.49 | 0.44 | 53.0% | 52.8% | 42.3% | 47.9%/37.1% | n/a (profitable_beyond_25.0x) | pass | 0.286 (unverified) | 1.11 |
| 2 | `cfg_612a` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=25, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 46/488/158 | 692 | 51.1% | 8.6% | 1.01 | -9.7% | 262 | 1.24 | 11.0% | 349.9 | 12/12 | 0.67 | 0.54 | 0.48 | 3 | 6.4% | 0.86 | 0.45 | 46.7% | 43.2% | 31.4% | 45.9%/32.6% | 9.1 (interpolated) | pass | 0.190 (unverified) | 0.01 |
| 3 | `cfg_80ed` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=25, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 109/432/163 | 704 | 47.1% | 8.0% | 0.94 | -10.9% | 409 | 1.22 | 10.9% | 357.3 | 11/11 | 0.64 | 0.56 | 0.38 | 3 | 4.9% | 0.88 | 0.48 | 43.3% | 40.2% | 33.1% | 42.7%/30.4% | 8.4 (interpolated) | pass | 0.145 (unverified) | -0.00 |
| 4 | `cfg_efd8` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 40/43/37 | 120 | 53.2% | 8.9% | 0.90 | -7.7% | 236 | 1.58 | 10.7% | 62.4 | 9/9 | 0.89 | 0.68 | 0.22 | 5 | 30.3% | 0.35 | 0.46 | 52.2% | 51.7% | 36.0% | 51.5%/40.1% | n/a (profitable_beyond_25.0x) | pass | 0.127 (unverified) | 0.34 |
| 5 | `cfg_6457` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 51/32/37 | 120 | 50.3% | 8.5% | 0.89 | -7.4% | 174 | 1.55 | 9.9% | 63.2 | 10/10 | 0.90 | 0.78 | 0.11 | 5 | 30.7% | 0.33 | 0.50 | 50.3% | 50.3% | 46.9% | 48.3%/35.4% | n/a (profitable_beyond_25.0x) | pass | 0.122 (unverified) | 0.40 |
| 6 | `cfg_d3e5` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 22/60/73 | 155 | 47.3% | 8.1% | 0.98 | -9.2% | 345 | 1.58 | 7.3% | 80.3 | 8/8 | 1.00 | 0.60 | 0.38 | 4 | 29.3% | 0.31 | 0.53 | 46.9% | 46.7% | 24.1% | 42.0%/33.2% | n/a (profitable_beyond_25.0x) | pass | 0.170 (unverified) | 0.58 |
| 7 | `cfg_25e3` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 50/35/36 | 121 | 61.9% | 10.1% | 1.04 | -6.5% | 314 | 1.69 | 10.0% | 63.3 | 10/10 | 0.90 | 0.76 | 0.28 | 5 | 36.0% | 0.34 | 0.42 | 59.3% | 58.7% | 31.7% | 56.8%/42.3% | n/a (profitable_beyond_25.0x) | pass | 0.207 (unverified) | 0.58 |
| 8 | `cfg_d433` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 81/2/67 | 150 | 38.6% | 6.8% | 1.05 | -4.3% | 204 | 1.59 | 6.7% | 76.9 | 7/7 | 0.71 | 0.73 | 0.32 | 5 | 23.5% | 0.39 | 0.49 | 38.0% | 37.1% | 20.3% | 36.9%/29.2% | n/a (profitable_beyond_25.0x) | pass | 0.200 (unverified) | 0.50 |
| 9 | `cfg_4fa5` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 15/47/51 | 113 | 28.6% | 5.2% | 0.86 | -6.1% | 155 | 1.52 | 5.5% | 57.6 | 8/8 | 0.88 | 0.59 | 0.27 | 5 | 20.2% | 0.28 | 0.72 | 28.3% | 27.8% | 13.2% | 25.7%/14.5% | n/a (profitable_beyond_25.0x) | pass | 0.102 (unverified) | 1.02 |
| 10 | `cfg_39db` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 33/49/73 | 155 | 45.7% | 7.8% | 0.93 | -8.9% | 339 | 1.56 | 7.0% | 80.5 | 9/9 | 1.00 | 0.70 | 0.24 | 4 | 29.0% | 0.31 | 0.55 | 45.4% | 45.0% | 23.2% | 38.3%/29.2% | n/a (profitable_beyond_25.0x) | pass | 0.147 (unverified) | 0.54 |
| 11 | `cfg_a6d0` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 9/68/23 | 100 | 36.3% | 6.4% | 0.96 | -6.2% | 530 | 1.73 | 6.2% | 51.4 | 10/10 | 0.90 | 0.56 | 0.40 | 3 | 7.4% | 0.72 | 0.69 | 35.1% | 34.7% | 14.3% | 33.2%/25.7% | n/a (profitable_beyond_25.0x) | pass | 0.150 (unverified) | 0.97 |
| 12 | `cfg_98c3` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 20/42/51 | 113 | 29.0% | 5.2% | 0.86 | -6.0% | 155 | 1.52 | 5.4% | 57.7 | 9/9 | 0.89 | 0.82 | 0.04 | 5 | 19.0% | 0.29 | 0.72 | 27.9% | 27.7% | 13.0% | 25.4%/16.6% | n/a (profitable_beyond_25.0x) | pass | 0.101 (unverified) | 1.02 |
| 13 | `cfg_fd46` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 54/37/39 | 130 | 51.3% | 8.6% | 0.90 | -7.3% | 162 | 1.54 | 11.1% | 67.6 | 11/11 | 0.91 | 0.71 | 0.19 | 5 | 32.8% | 0.34 | 0.49 | 53.1% | 51.0% | 49.4% | 50.2%/39.8% | n/a (profitable_beyond_25.0x) | pass | 0.128 (unverified) | 0.27 |
| 14 | `cfg_e80c` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 40/31/33 | 104 | 50.0% | 8.5% | 1.05 | -6.5% | 308 | 1.74 | 9.3% | 53.9 | 11/11 | 0.91 | 0.52 | 0.53 | 4 | 21.5% | 0.48 | 0.52 | 49.6% | 49.1% | 32.8% | 43.7%/32.8% | n/a (profitable_beyond_25.0x) | pass | 0.197 (unverified) | 0.84 |
| 15 | `cfg_448e` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 29/59/74 | 162 | 39.8% | 6.9% | 0.89 | -7.2% | 237 | 1.49 | 7.7% | 83.1 | 10/10 | 0.90 | 0.66 | 0.23 | 5 | 30.0% | 0.25 | 0.53 | 38.4% | 37.6% | 13.3% | 36.1%/25.0% | n/a (profitable_beyond_25.0x) | pass | 0.127 (unverified) | 0.34 |
| 16 | `cfg_4de4` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 30/63/28 | 121 | 38.5% | 6.7% | 0.83 | -7.0% | 371 | 1.57 | 7.1% | 62.5 | 10/10 | 0.90 | 0.71 | 0.12 | 5 | 22.2% | 0.36 | 0.51 | 38.0% | 37.4% | 26.2% | 35.5%/29.6% | n/a (profitable_beyond_25.0x) | pass | 0.102 (unverified) | 0.93 |
| 17 | `cfg_6578` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 10/67/23 | 100 | 33.5% | 6.0% | 0.91 | -6.5% | 530 | 1.68 | 6.1% | 51.2 | 11/11 | 1.00 | 0.62 | 0.29 | 3 | 6.2% | 0.75 | 0.70 | 33.1% | 32.7% | 11.6% | 30.6%/22.9% | n/a (profitable_beyond_25.0x) | pass | 0.124 (unverified) | 0.97 |
| 18 | `cfg_8094` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 22/66/74 | 162 | 38.5% | 6.7% | 0.86 | -7.3% | 237 | 1.48 | 7.8% | 83.7 | 9/9 | 0.89 | 0.51 | 0.35 | 5 | 28.1% | 0.27 | 0.54 | 37.8% | 37.5% | 13.0% | 33.9%/26.8% | n/a (profitable_beyond_25.0x) | pass | 0.114 (unverified) | 0.34 |
| 19 | `cfg_50dd` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 23/59/72 | 154 | 37.2% | 6.5% | 0.82 | -10.5% | 266 | 1.48 | 7.3% | 79.1 | 9/9 | 0.89 | 0.69 | 0.13 | 5 | 24.5% | 0.29 | 0.52 | 36.1% | 35.8% | 33.5% | 33.5%/26.3% | n/a (profitable_beyond_25.0x) | pass | 0.096 (unverified) | 0.56 |
| 20 | `cfg_aafa` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 33/49/72 | 154 | 37.2% | 6.5% | 0.82 | -10.4% | 189 | 1.48 | 7.2% | 79.1 | 9/9 | 0.89 | 0.78 | 0.04 | 5 | 25.1% | 0.28 | 0.52 | 36.7% | 35.9% | 28.6% | 36.0%/26.1% | n/a (profitable_beyond_25.0x) | pass | 0.097 (unverified) | 0.60 |
| 21 | `cfg_4d88` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 34/71/0 | 105 | 21.4% | 4.0% | 0.92 | -4.6% | 198 | 1.75 | 1.8% | 52.8 | 10/10 | 0.80 | 0.59 | 0.33 | 5 | 15.1% | 0.29 | 0.52 | 21.0% | 20.7% | 3.8% | 18.0%/13.0% | n/a (profitable_beyond_25.0x) | pass | 0.114 (unverified) | 0.73 |
| 22 | `cfg_e52c` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 9/120/0 | 129 | 34.2% | 6.1% | 0.86 | -6.9% | 408 | 1.65 | 8.7% | 65.7 | 9/9 | 0.78 | 0.44 | 0.42 | 4 | 17.0% | 0.50 | 0.59 | 34.1% | 33.6% | 26.5% | 29.9%/23.7% | n/a (profitable_beyond_25.0x) | pass | 0.108 (unverified) | 0.13 |
| 23 | `cfg_fed6` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 20/73/28 | 121 | 38.3% | 6.7% | 0.83 | -7.5% | 371 | 1.57 | 7.2% | 62.7 | 10/10 | 0.90 | 0.67 | 0.16 | 5 | 21.5% | 0.38 | 0.51 | 37.9% | 37.6% | 28.9% | 35.5%/25.7% | n/a (profitable_beyond_25.0x) | pass | 0.099 (unverified) | 0.77 |
| 24 | `cfg_c390` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 56/29/36 | 121 | 49.6% | 8.4% | 0.90 | -6.9% | 201 | 1.59 | 9.5% | 63.0 | 9/9 | 0.89 | 0.68 | 0.22 | 5 | 26.5% | 0.39 | 0.45 | 49.1% | 47.9% | 31.0% | 44.3%/34.6% | n/a (profitable_beyond_25.0x) | pass | 0.129 (unverified) | 0.59 |
| 25 | `cfg_92d9` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 16/78/26 | 120 | 38.9% | 6.8% | 0.79 | -13.6% | 489 | 1.61 | 7.2% | 61.4 | 9/9 | 0.89 | 0.74 | 0.05 | 4 | 20.3% | 0.40 | 0.56 | 38.2% | 37.4% | 37.7% | 36.9%/27.1% | n/a (profitable_beyond_25.0x) | pass | 0.076 (unverified) | 0.80 |
| 26 | `cfg_033c` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 12/89/24 | 125 | 43.6% | 7.5% | 0.91 | -7.2% | 123 | 1.62 | 7.8% | 64.4 | 10/10 | 0.90 | 0.57 | 0.34 | 5 | 18.8% | 0.52 | 0.61 | 41.9% | 39.4% | 13.8% | 37.3%/28.0% | n/a (profitable_beyond_25.0x) | pass | 0.110 (unverified) | 1.01 |
| 27 | `cfg_702b` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 41/145/0 | 186 | 30.0% | 5.4% | 1.09 | -5.3% | 170 | 1.72 | 3.3% | 93.3 | 10/10 | 0.80 | 0.36 | 0.73 | 5 | 18.3% | 0.33 | 0.41 | 29.0% | 28.4% | 19.7% | 26.2%/20.1% | 19.3 (interpolated) | pass | 0.210 (unverified) | 0.91 |
| 28 | `cfg_6c5b` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 33/48/68 | 149 | 34.1% | 6.0% | 0.85 | -6.2% | 231 | 1.49 | 7.2% | 75.5 | 7/7 | 0.86 | 0.46 | 0.40 | 5 | 21.6% | 0.32 | 0.58 | 33.5% | 32.3% | 10.3% | 31.3%/22.3% | n/a (profitable_beyond_25.0x) | pass | 0.103 (unverified) | 0.56 |
| 29 | `cfg_846b` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 10/72/70 | 152 | 39.3% | 6.9% | 0.95 | -5.0% | 142 | 1.54 | 7.5% | 77.8 | 9/9 | 0.89 | 0.41 | 0.54 | 5 | 20.0% | 0.44 | 0.65 | 38.2% | 37.2% | 12.0% | 34.2%/24.7% | n/a (profitable_beyond_25.0x) | pass | 0.140 (unverified) | 0.82 |
| 30 | `cfg_7b73` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 57/43/47 | 147 | 53.1% | 8.9% | 0.88 | -13.0% | 145 | 1.48 | 12.4% | 76.2 | 11/11 | 0.91 | 0.56 | 0.32 | 5 | 33.3% | 0.33 | 0.45 | 51.7% | 51.2% | 47.6% | 49.2%/35.1% | n/a (profitable_beyond_25.0x) | pass | 0.122 (unverified) | 0.10 |
| 31 | `cfg_b13f` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 62/50/54 | 166 | 47.1% | 8.0% | 0.78 | -11.7% | 363 | 1.40 | 14.2% | 85.7 | 10/10 | 0.90 | 0.59 | 0.19 | 5 | 27.4% | 0.40 | 0.52 | 46.6% | 46.3% | 38.3% | 44.5%/34.9% | n/a (profitable_beyond_25.0x) | pass | 0.085 (unverified) | 0.45 |
| 32 | `cfg_bff5` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 29/65/26 | 120 | 37.1% | 6.5% | 0.76 | -13.0% | 489 | 1.58 | 7.1% | 61.8 | 10/10 | 0.90 | 0.72 | 0.04 | 4 | 19.4% | 0.41 | 0.58 | 37.1% | 36.2% | 34.9% | 34.3%/26.1% | n/a (profitable_beyond_25.0x) | pass | 0.067 (unverified) | 0.62 |
| 33 | `cfg_ebb8` | timeframe=5min, mean_type=ema, mean_lookback=40, std_lookback=60, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 108/159/171 | 438 | 19.2% | 3.6% | 0.77 | -7.4% | 375 | 1.22 | 3.3% | 220.5 | 11/11 | 0.91 | 0.49 | 0.28 | 3 | 0.1% | 1.00 | 0.70 | 18.3% | 16.2% | 7.2% | 17.7%/11.5% | 6.9 (interpolated) | pass | 0.065 (unverified) | -0.19 |
| 34 | `cfg_5b8f` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 67/19/63 | 149 | 33.6% | 6.0% | 0.98 | -5.1% | 200 | 1.56 | 6.2% | 75.5 | 7/7 | 0.71 | 0.63 | 0.35 | 5 | 20.7% | 0.39 | 0.52 | 33.0% | 31.8% | 18.3% | 30.6%/22.6% | n/a (profitable_beyond_25.0x) | pass | 0.156 (unverified) | 0.50 |
| 35 | `cfg_7a72` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 40/50/40 | 130 | 51.1% | 8.6% | 0.88 | -7.5% | 422 | 1.54 | 11.7% | 67.5 | 10/10 | 0.90 | 0.54 | 0.33 | 5 | 31.7% | 0.36 | 0.51 | 49.4% | 47.7% | 34.0% | 46.3%/35.0% | n/a (profitable_beyond_25.0x) | pass | 0.115 (unverified) | 0.17 |
| 36 | `cfg_476a` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 13/69/70 | 152 | 37.1% | 6.5% | 0.91 | -5.0% | 142 | 1.51 | 7.4% | 78.0 | 10/10 | 0.90 | 0.55 | 0.36 | 5 | 19.9% | 0.42 | 0.66 | 36.8% | 35.7% | 10.1% | 33.3%/24.6% | n/a (profitable_beyond_25.0x) | pass | 0.120 (unverified) | 0.84 |
| 37 | `cfg_ae33` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 16/85/24 | 125 | 41.3% | 7.2% | 0.88 | -7.5% | 162 | 1.59 | 7.7% | 64.5 | 11/11 | 0.91 | 0.64 | 0.24 | 5 | 18.2% | 0.51 | 0.61 | 38.6% | 38.0% | 11.9% | 35.2%/23.5% | n/a (profitable_beyond_25.0x) | pass | 0.097 (unverified) | 1.01 |
| 38 | `cfg_ca23` | timeframe=5min, mean_type=ema, mean_lookback=20, std_lookback=60, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 130/55/118 | 303 | 19.6% | 3.6% | 0.90 | -9.2% | 456 | 1.33 | 2.1% | 151.5 | 10/10 | 0.90 | 0.61 | 0.29 | 3 | -1.7% | 1.15 | 0.68 | 18.3% | 16.3% | 4.6% | 17.1%/12.7% | 9.8 (interpolated) | pass | 0.106 (unverified) | -0.11 |
| 39 | `cfg_183b` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=25, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 99/331/0 | 430 | 36.5% | 6.4% | 0.97 | -9.9% | 223 | 1.32 | 7.4% | 218.6 | 10/10 | 0.70 | 0.42 | 0.55 | 4 | 13.8% | 0.61 | 0.40 | 34.2% | 33.0% | 22.9% | 32.3%/24.4% | 11.2 (interpolated) | pass | 0.157 (unverified) | -0.21 |
| 40 | `cfg_9673` | timeframe=5min, mean_type=sma, mean_lookback=40, std_lookback=60, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 187/177/217 | 581 | 23.0% | 4.2% | 0.85 | -6.0% | 375 | 1.21 | 4.3% | 290.7 | 10/10 | 0.80 | 0.43 | 0.42 | 4 | 1.9% | 0.92 | 0.62 | 20.9% | 17.9% | 4.0% | 20.3%/15.0% | 6.1 (interpolated) | pass | 0.093 (unverified) | -0.11 |
| 41 | `cfg_15fd` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=25, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 76/357/0 | 433 | 45.5% | 7.8% | 0.90 | -6.5% | 472 | 1.29 | 7.5% | 221.1 | 10/10 | 0.70 | 0.47 | 0.43 | 4 | 11.6% | 0.74 | 0.51 | 42.6% | 39.9% | 3.9% | 37.2%/25.6% | 12.4 (interpolated) | pass | 0.125 (unverified) | 0.30 |
| 42 | `cfg_a8c4` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 39/42/68 | 149 | 29.4% | 5.3% | 0.79 | -6.2% | 231 | 1.43 | 7.0% | 75.3 | 8/8 | 0.88 | 0.53 | 0.26 | 5 | 20.0% | 0.32 | 0.61 | 28.9% | 28.6% | 5.4% | 25.9%/17.3% | n/a (profitable_beyond_25.0x) | pass | 0.083 (unverified) | 0.58 |
| 43 | `cfg_9879` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 25/44/34 | 103 | 39.4% | 6.9% | 0.79 | -6.6% | 166 | 1.60 | 9.7% | 53.0 | 10/10 | 0.90 | 0.34 | 0.45 | 5 | 23.1% | 0.34 | 0.61 | 39.0% | 39.0% | 27.8% | 33.5%/24.3% | n/a (profitable_beyond_25.0x) | pass | 0.085 (unverified) | 0.59 |
| 44 | `cfg_25bf` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=25, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 78/324/131 | 533 | 38.0% | 6.7% | 0.77 | -8.3% | 226 | 1.21 | 8.1% | 271.3 | 11/11 | 0.73 | 0.56 | 0.22 | 4 | 11.1% | 0.68 | 0.58 | 37.1% | 33.6% | 8.8% | 34.0%/24.1% | 9.7 (interpolated) | pass | 0.079 (unverified) | 0.25 |
| 45 | `cfg_56d2` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 12/117/0 | 129 | 31.4% | 5.6% | 0.81 | -6.9% | 456 | 1.61 | 8.6% | 65.7 | 10/10 | 0.80 | 0.49 | 0.32 | 4 | 14.9% | 0.53 | 0.63 | 30.1% | 29.7% | 25.2% | 28.0%/18.9% | n/a (profitable_beyond_25.0x) | pass | 0.091 (unverified) | 0.14 |
| 46 | `cfg_c2d9` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 39/223/0 | 262 | 25.1% | 4.6% | 0.77 | -8.6% | 437 | 1.37 | 4.6% | 131.0 | 10/10 | 0.70 | 0.45 | 0.31 | 3 | 12.0% | 0.49 | 0.55 | 23.4% | 22.8% | 26.1% | 20.7%/15.8% | 12.4 (interpolated) | pass | 0.065 (unverified) | 0.80 |
| 47 | `cfg_f5fd` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=25, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 178/274/246 | 698 | 47.7% | 8.1% | 0.82 | -25.1% | 318 | 1.15 | 16.1% | 353.6 | 11/11 | 0.64 | 0.32 | 0.50 | 3 | -0.1% | 1.13 | 0.59 | 43.9% | 43.4% | 44.5% | 47.1%/32.1% | 9.2 (interpolated) | pass | 0.107 (unverified) | 0.06 |
| 48 | `cfg_6737` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 27/78/0 | 105 | 22.1% | 4.1% | 0.94 | -5.4% | 198 | 1.76 | 1.8% | 52.6 | 11/11 | 0.91 | 0.57 | 0.37 | 5 | 16.6% | 0.25 | 0.51 | 21.5% | 21.1% | 4.6% | 18.1%/12.8% | n/a (profitable_beyond_25.0x) | pass | 0.125 (unverified) | 0.78 |
| 49 | `cfg_d573` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 14/246/0 | 260 | 24.9% | 4.6% | 0.75 | -9.9% | 437 | 1.36 | 4.7% | 130.3 | 10/10 | 0.70 | 0.42 | 0.34 | 3 | 12.3% | 0.49 | 0.55 | 24.0% | 22.0% | 26.3% | 21.5%/15.4% | 11.6 (interpolated) | pass | 0.061 (unverified) | 0.79 |
| 50 | `cfg_57a8` | timeframe=5min, mean_type=ema, mean_lookback=50, std_lookback=40, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 256/237/0 | 493 | 30.3% | 5.4% | 0.96 | -7.3% | 371 | 1.30 | 4.6% | 246.4 | 9/9 | 1.00 | 0.49 | 0.47 | 4 | 10.9% | 0.60 | 0.48 | 26.6% | 25.1% | 12.0% | 26.8%/20.7% | 8.5 (interpolated) | pass | 0.148 (unverified) | 0.54 |
| 51 | `cfg_ccdc` | timeframe=5min, mean_type=ema, mean_lookback=20, std_lookback=60, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 131/119/0 | 250 | 19.4% | 3.6% | 0.86 | -9.9% | 368 | 1.37 | 2.4% | 125.7 | 9/9 | 0.89 | 0.61 | 0.25 | 3 | -1.9% | 1.18 | 0.71 | 18.6% | 16.7% | 10.0% | 17.4%/13.1% | 11.5 (interpolated) | pass | 0.096 (unverified) | -0.04 |
| 52 | `cfg_6267` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=10, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 32/52/74 | 158 | 35.8% | 6.3% | 0.80 | -7.4% | 339 | 1.43 | 7.4% | 81.4 | 8/8 | 0.88 | 0.65 | 0.15 | 5 | 20.0% | 0.40 | 0.65 | 34.3% | 33.8% | 21.3% | 32.0%/24.3% | n/a (profitable_beyond_25.0x) | pass | 0.087 (unverified) | 0.06 |
| 53 | `cfg_d1c6` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 51/20/88 | 159 | 45.3% | 7.8% | 0.83 | -7.3% | 276 | 1.45 | 9.2% | 83.0 | 9/9 | 0.89 | 0.46 | 0.36 | 5 | 27.3% | 0.33 | 0.57 | 44.1% | 43.6% | 23.5% | 36.2%/28.1% | n/a (profitable_beyond_25.0x) | pass | 0.092 (unverified) | 0.46 |
| 54 | `cfg_7916` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 43/42/40 | 125 | 42.8% | 7.4% | 0.84 | -11.4% | 396 | 1.49 | 11.3% | 65.3 | 11/11 | 0.91 | 0.55 | 0.29 | 5 | 19.9% | 0.47 | 0.60 | 42.8% | 41.3% | 33.6% | 38.1%/25.3% | n/a (profitable_beyond_25.0x) | pass | 0.093 (unverified) | 0.90 |
| 55 | `cfg_7051` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 51/35/40 | 126 | 41.8% | 7.2% | 0.86 | -8.2% | 184 | 1.48 | 10.8% | 65.7 | 11/11 | 0.91 | 0.59 | 0.27 | 5 | 25.8% | 0.34 | 0.55 | 39.9% | 39.5% | 33.0% | 36.9%/25.8% | n/a (profitable_beyond_25.0x) | pass | 0.108 (unverified) | 0.88 |
| 56 | `cfg_c011` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 13/46/45 | 104 | 28.9% | 5.2% | 0.80 | -6.2% | 196 | 1.57 | 5.0% | 54.0 | 10/10 | 0.90 | 0.59 | 0.21 | 5 | 14.2% | 0.47 | 0.86 | 28.4% | 27.9% | 5.9% | 27.8%/18.2% | n/a (profitable_beyond_25.0x) | pass | 0.074 (unverified) | 0.41 |
| 57 | `cfg_56e3` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 125/292/0 | 417 | 31.1% | 5.6% | 0.76 | -7.4% | 198 | 1.30 | 7.0% | 210.4 | 10/10 | 0.90 | 0.42 | 0.34 | 4 | 18.6% | 0.34 | 0.50 | 29.2% | 27.9% | 8.9% | 29.9%/22.0% | 10.2 (interpolated) | pass | 0.082 (unverified) | 0.07 |
| 58 | `cfg_7c76` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 24/162/0 | 186 | 26.8% | 4.9% | 1.00 | -6.6% | 201 | 1.62 | 3.4% | 93.3 | 11/11 | 0.82 | 0.38 | 0.61 | 5 | 15.0% | 0.38 | 0.44 | 26.0% | 25.2% | 18.0% | 23.2%/16.7% | 17.7 (interpolated) | pass | 0.156 (unverified) | 0.91 |
| 59 | `cfg_02bd` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 7/52/45 | 104 | 28.5% | 5.1% | 0.79 | -6.3% | 194 | 1.56 | 5.2% | 54.0 | 11/11 | 1.00 | 0.67 | 0.12 | 5 | 15.9% | 0.40 | 0.86 | 28.1% | 27.9% | 7.2% | 25.6%/17.5% | n/a (profitable_beyond_25.0x) | pass | 0.070 (unverified) | 0.42 |
| 60 | `cfg_4bba` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 45/66/55 | 166 | 48.3% | 8.2% | 0.78 | -14.0% | 441 | 1.42 | 14.9% | 85.4 | 9/9 | 0.89 | 0.43 | 0.35 | 4 | 27.5% | 0.40 | 0.55 | 46.8% | 46.5% | 31.5% | 40.2%/30.0% | n/a (profitable_beyond_25.0x) | pass | 0.083 (unverified) | 0.35 |
| 61 | `cfg_5634` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 24/59/75 | 158 | 37.4% | 6.6% | 0.80 | -7.9% | 339 | 1.44 | 7.5% | 82.0 | 9/9 | 0.89 | 0.64 | 0.16 | 5 | 21.1% | 0.39 | 0.67 | 36.1% | 34.8% | 21.7% | 34.4%/25.9% | n/a (profitable_beyond_25.0x) | pass | 0.090 (unverified) | 0.02 |
| 62 | `cfg_e9cc` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 125/228/0 | 353 | 31.2% | 5.6% | 0.84 | -11.5% | 420 | 1.34 | 6.0% | 175.3 | 10/10 | 0.80 | 0.32 | 0.52 | 4 | 16.5% | 0.44 | 0.48 | 30.4% | 29.3% | 19.2% | 28.1%/18.4% | 12.2 (interpolated) | pass | 0.094 (unverified) | 0.51 |
| 63 | `cfg_517d` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=25, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 147/150/445 | 742 | 41.1% | 7.1% | 0.81 | -13.0% | 249 | 1.16 | 11.9% | 376.0 | 10/10 | 0.70 | 0.34 | 0.47 | 4 | 14.1% | 0.70 | 0.66 | 37.4% | 32.6% | 32.0% | 37.6%/22.7% | 7.6 (interpolated) | pass | 0.092 (unverified) | 0.04 |
| 64 | `cfg_c601` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 377/46/0 | 423 | 33.5% | 6.0% | 0.89 | -9.5% | 525 | 1.32 | 8.4% | 211.6 | 10/10 | 0.80 | 0.18 | 0.70 | 4 | 13.7% | 0.51 | 0.48 | 29.1% | 27.3% | 21.4% | 29.0%/22.1% | 10.0 (interpolated) | pass | 0.125 (unverified) | -0.15 |
| 65 | `cfg_7831` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=25, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 83/316/0 | 399 | 28.6% | 5.2% | 0.77 | -10.8% | 242 | 1.27 | 6.9% | 200.6 | 9/9 | 0.89 | 0.45 | 0.33 | 3 | 3.4% | 0.92 | 0.70 | 26.4% | 25.2% | 9.1% | 26.2%/17.4% | 10.1 (interpolated) | pass | 0.068 (unverified) | 0.20 |
| 66 | `cfg_fa6a` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=25, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 141/248/0 | 389 | 46.6% | 8.0% | 0.86 | -13.7% | 271 | 1.26 | 11.2% | 198.4 | 10/10 | 0.70 | 0.37 | 0.49 | 4 | 16.2% | 0.69 | 0.55 | 44.4% | 42.0% | 25.7% | 42.8%/30.2% | 15.1 (interpolated) | pass | 0.106 (unverified) | -0.06 |
| 67 | `cfg_46e9` | timeframe=5min, mean_type=ema, mean_lookback=50, std_lookback=40, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 144/344/0 | 488 | 30.7% | 5.5% | 0.96 | -7.2% | 374 | 1.29 | 4.9% | 245.0 | 10/10 | 0.90 | 0.52 | 0.44 | 4 | 13.8% | 0.51 | 0.48 | 27.0% | 25.2% | 10.7% | 27.9%/20.3% | 8.8 (interpolated) | pass | 0.148 (unverified) | 0.43 |
| 68 | `cfg_5af3` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=25, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 51/375/0 | 426 | 33.9% | 6.0% | 0.91 | -11.2% | 223 | 1.30 | 7.6% | 217.0 | 11/11 | 0.73 | 0.52 | 0.39 | 4 | 11.4% | 0.65 | 0.47 | 32.5% | 29.5% | 18.9% | 30.1%/19.3% | 10.5 (interpolated) | pass | 0.128 (unverified) | -0.27 |
| 69 | `cfg_87ba` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=30, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 57/46/120 | 223 | 21.0% | 3.9% | 0.83 | -5.1% | 239 | 1.36 | 4.0% | 110.3 | 11/11 | 0.73 | 0.25 | 0.57 | 4 | 8.1% | 0.61 | 0.63 | 20.4% | 19.9% | 3.4% | 19.5%/13.9% | 13.2 (interpolated) | pass | 0.089 (unverified) | 0.30 |
| 70 | `cfg_cd92` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=25, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 97/289/0 | 386 | 40.3% | 7.0% | 0.77 | -18.2% | 271 | 1.23 | 11.8% | 196.8 | 11/11 | 0.73 | 0.30 | 0.47 | 4 | 12.2% | 0.77 | 0.66 | 38.2% | 35.1% | 19.1% | 38.3%/26.5% | 13.6 (interpolated) | pass | 0.075 (unverified) | -0.05 |
| 71 | `cfg_9a22` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 19/379/0 | 398 | 34.7% | 6.1% | 0.89 | -12.6% | 185 | 1.31 | 7.2% | 200.2 | 9/9 | 0.89 | 0.59 | 0.29 | 3 | 4.1% | 0.92 | 0.71 | 31.6% | 29.7% | 10.8% | 30.1%/24.4% | 11.8 (interpolated) | pass | 0.119 (unverified) | 0.22 |
| 72 | `cfg_4bf6` | timeframe=5min, mean_type=ema, mean_lookback=20, std_lookback=30, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 795/300/0 | 1095 | 31.5% | 5.6% | 0.80 | -8.2% | 398 | 1.16 | 8.7% | 551.9 | 9/9 | 0.89 | 0.42 | 0.38 | 3 | -3.5% | 1.14 | 0.48 | 26.0% | 19.3% | 15.0% | 27.7%/17.1% | 4.4 (interpolated) | pass | 0.090 (unverified) | -0.11 |
| 73 | `cfg_194b` | timeframe=5min, mean_type=ema, mean_lookback=60, std_lookback=40, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 235/352/0 | 587 | 27.9% | 5.0% | 0.85 | -5.8% | 375 | 1.24 | 5.7% | 294.3 | 9/9 | 0.67 | 0.38 | 0.47 | 4 | 13.6% | 0.47 | 0.54 | 26.8% | 25.0% | 15.0% | 28.5%/23.3% | 7.3 (interpolated) | pass | 0.101 (unverified) | 0.18 |
| 74 | `cfg_b73c` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 112/59/0 | 171 | 24.7% | 4.5% | 0.79 | -7.4% | 245 | 1.46 | 4.4% | 85.6 | 11/11 | 0.82 | 0.19 | 0.59 | 5 | 16.3% | 0.34 | 0.53 | 23.4% | 22.6% | 26.6% | 22.0%/17.8% | 17.7 (interpolated) | pass | 0.078 (unverified) | -0.08 |
| 75 | `cfg_283f` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 221/129/0 | 350 | 34.1% | 6.1% | 0.87 | -9.7% | 406 | 1.32 | 8.9% | 176.2 | 10/10 | 0.80 | 0.20 | 0.67 | 4 | 20.0% | 0.41 | 0.49 | 33.1% | 29.7% | 19.4% | 29.0%/21.6% | 12.1 (interpolated) | pass | 0.104 (unverified) | -0.05 |
| 76 | `cfg_b6b2` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 114/224/0 | 338 | 32.4% | 5.8% | 0.78 | -11.9% | 405 | 1.28 | 10.2% | 170.4 | 11/11 | 0.64 | 0.16 | 0.62 | 4 | 17.8% | 0.39 | 0.54 | 28.8% | 27.8% | 14.5% | 28.7%/21.2% | 11.6 (interpolated) | pass | 0.073 (unverified) | -0.10 |
| 77 | `cfg_bd7b` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=25, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 167/316/0 | 483 | 49.2% | 8.3% | 0.85 | -16.8% | 278 | 1.24 | 13.9% | 244.3 | 10/10 | 0.70 | 0.30 | 0.54 | 3 | 7.5% | 0.87 | 0.52 | 45.7% | 43.8% | 26.9% | 44.3%/32.5% | 11.8 (interpolated) | pass | 0.103 (unverified) | 0.02 |
| 78 | `cfg_66c6` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 47/7/51 | 105 | 39.4% | 6.9% | 0.99 | -6.2% | 201 | 1.64 | 5.5% | 54.8 | 9/9 | 1.00 | 0.25 | 0.73 | 5 | 22.2% | 0.44 | 0.57 | 38.1% | 37.7% | 8.1% | 35.2%/26.5% | n/a (profitable_beyond_25.0x) | pass | 0.178 (unverified) | 0.40 |
| 79 | `cfg_a560` | timeframe=5min, mean_type=ema, mean_lookback=60, std_lookback=40, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 142/441/0 | 583 | 32.8% | 5.8% | 0.97 | -6.5% | 249 | 1.28 | 6.0% | 292.9 | 10/10 | 0.70 | 0.48 | 0.49 | 3 | 16.6% | 0.49 | 0.47 | 29.2% | 27.9% | 18.5% | 32.2%/25.6% | 7.9 (interpolated) | pass | 0.162 (unverified) | 0.08 |
| 80 | `cfg_536d` | timeframe=5min, mean_type=sma, mean_lookback=40, std_lookback=30, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 344/308/0 | 652 | 26.6% | 4.8% | 0.79 | -6.0% | 333 | 1.21 | 5.9% | 327.9 | 9/9 | 0.89 | 0.50 | 0.29 | 5 | 14.4% | 0.42 | 0.52 | 22.0% | 18.8% | 16.5% | 23.3%/17.6% | 5.9 (interpolated) | pass | 0.080 (unverified) | 0.36 |
| 81 | `cfg_4e88` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 59/41/0 | 100 | 38.3% | 6.7% | 0.79 | -9.6% | 211 | 1.74 | 9.4% | 51.4 | 8/8 | 0.75 | 0.19 | 0.60 | 5 | 19.3% | 0.44 | 0.56 | 37.9% | 37.3% | 21.7% | 32.4%/24.4% | n/a (profitable_beyond_25.0x) | pass | 0.078 (unverified) | 0.04 |
| 82 | `cfg_92a5` | timeframe=5min, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 419/444/0 | 863 | 29.5% | 5.3% | 0.79 | -9.2% | 585 | 1.18 | 8.0% | 435.5 | 9/9 | 1.00 | 0.55 | 0.25 | 5 | 18.8% | 0.31 | 0.59 | 25.3% | 22.2% | 16.0% | 25.8%/19.0% | 5.2 (interpolated) | pass | 0.083 (unverified) | 0.13 |
| 83 | `cfg_0c6f` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=30, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 62/104/0 | 166 | 23.6% | 4.3% | 0.80 | -7.3% | 199 | 1.47 | 4.8% | 83.1 | 11/11 | 0.82 | 0.31 | 0.49 | 5 | 7.5% | 0.68 | 0.54 | 22.5% | 22.2% | 17.5% | 22.0%/14.7% | 20.0 (interpolated) | pass | 0.084 (unverified) | 0.60 |
| 84 | `cfg_1b2f` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 80/221/107 | 408 | 25.4% | 4.6% | 0.76 | -6.7% | 227 | 1.23 | 6.1% | 206.8 | 12/12 | 0.58 | 0.27 | 0.49 | 4 | 15.1% | 0.38 | 0.64 | 22.5% | 20.7% | 5.1% | 20.8%/15.9% | 8.6 (interpolated) | pass | 0.085 (unverified) | -0.22 |
| 85 | `cfg_d3ee` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 54/211/0 | 265 | 26.2% | 4.8% | 0.84 | -9.5% | 253 | 1.37 | 4.7% | 132.7 | 11/11 | 0.91 | 0.41 | 0.43 | 4 | 12.6% | 0.46 | 0.44 | 25.3% | 24.3% | 23.3% | 22.4%/15.4% | 13.3 (interpolated) | pass | 0.094 (unverified) | 0.49 |
| 86 | `cfg_3088` | timeframe=5min, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 747/698/0 | 1445 | 35.6% | 6.3% | 0.79 | -8.4% | 435 | 1.13 | 12.9% | 730.1 | 10/10 | 0.80 | 0.48 | 0.31 | 4 | 10.1% | 0.65 | 0.50 | 28.4% | 23.0% | 27.6% | 34.3%/25.5% | 3.8 (interpolated) | pass | 0.078 (unverified) | -0.29 |
| 87 | `cfg_8dee` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 269/150/0 | 419 | 29.5% | 5.3% | 0.77 | -8.8% | 498 | 1.26 | 10.4% | 209.9 | 11/11 | 0.64 | 0.21 | 0.56 | 3 | 9.7% | 0.67 | 0.57 | 27.8% | 27.0% | 18.1% | 27.1%/20.7% | 9.3 (interpolated) | pass | 0.075 (unverified) | -0.12 |
| 88 | `cfg_4928` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 5/112/40 | 157 | 15.9% | 3.0% | 0.82 | -4.5% | 192 | 1.43 | 2.5% | 78.1 | 9/9 | 0.89 | 0.46 | 0.35 | 4 | 4.2% | 0.73 | 0.76 | 15.4% | 14.7% | 1.5% | 15.3%/11.0% | 13.7 (interpolated) | pass | 0.073 (unverified) | -0.08 |
| 89 | `cfg_960c` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 72/281/0 | 353 | 28.6% | 5.2% | 0.78 | -12.8% | 265 | 1.31 | 6.2% | 175.7 | 11/11 | 0.82 | 0.37 | 0.40 | 4 | 15.6% | 0.43 | 0.53 | 26.8% | 26.0% | 19.3% | 24.6%/17.2% | 10.8 (interpolated) | pass | 0.071 (unverified) | 0.59 |
| 90 | `cfg_3860` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 1/116/40 | 157 | 16.1% | 3.0% | 0.82 | -4.5% | 172 | 1.44 | 2.5% | 78.2 | 10/10 | 0.90 | 0.55 | 0.27 | 4 | 4.0% | 0.74 | 0.76 | 15.1% | 14.5% | 1.2% | 14.5%/10.0% | 13.5 (interpolated) | pass | 0.074 (unverified) | -0.08 |
| 91 | `cfg_4f7e` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=30, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 29/96/96 | 221 | 16.3% | 3.1% | 0.79 | -3.8% | 327 | 1.33 | 2.9% | 109.5 | 11/11 | 0.82 | 0.28 | 0.51 | 5 | 11.5% | 0.28 | 0.70 | 15.4% | 13.9% | 4.8% | 15.2%/9.2% | 10.6 (interpolated) | pass | 0.071 (unverified) | 0.44 |
| 92 | `cfg_d43b` | timeframe=5min, mean_type=ema, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 839/563/0 | 1402 | 34.3% | 6.1% | 0.82 | -13.8% | 170 | 1.14 | 11.8% | 704.4 | 9/9 | 0.56 | 0.17 | 0.66 | 4 | 15.9% | 0.56 | 0.37 | 29.1% | 22.6% | 17.4% | 31.5%/23.0% | 4.0 (interpolated) | pass | 0.097 (unverified) | -0.99 |
| 93 | `cfg_c19c` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 24/74/49 | 147 | 52.3% | 8.8% | 0.77 | -14.7% | 172 | 1.45 | 13.9% | 75.7 | 10/10 | 0.90 | 0.27 | 0.50 | 5 | 36.3% | 0.28 | 0.61 | 51.7% | 50.8% | 55.4% | 41.1%/25.0% | n/a (profitable_beyond_25.0x) | pass | 0.080 (unverified) | 0.46 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 4.4% / 0.60 / 25 | -0.6% / -0.11 / 14 | 25.2% / 2.21 / 18 | 12.6% / 3.10 / 14 | 4.9% / 0.56 / 33 |
| 2 | -2.6% / -0.30 / 157 | 7.1% / 1.40 / 121 | 42.0% / 3.03 / 119 | 7.6% / 1.28 / 143 | -5.2% / -0.48 / 152 |
| 3 | -4.5% / -0.55 / 162 | 7.5% / 1.47 / 122 | 40.3% / 2.87 / 119 | 8.7% / 1.50 / 146 | -6.0% / -0.55 / 155 |
| 4 | 0.8% / 0.13 / 30 | 5.8% / 1.14 / 15 | 17.6% / 1.38 / 19 | 14.2% / 2.62 / 14 | 7.0% / 0.58 / 42 |
| 5 | 4.7% / 0.47 / 30 | 4.7% / 0.98 / 15 | 15.0% / 1.18 / 19 | 12.0% / 2.26 / 14 | 6.6% / 0.58 / 42 |
| 6 | -1.6% / -0.15 / 41 | 8.8% / 2.66 / 15 | 13.9% / 1.27 / 21 | 8.7% / 2.35 / 17 | 11.1% / 0.98 / 61 |
| 7 | 5.7% / 0.59 / 30 | 3.4% / 0.70 / 19 | 19.0% / 1.38 / 19 | 10.7% / 2.04 / 14 | 12.3% / 1.05 / 39 |
| 8 | 4.1% / 0.63 / 30 | 8.0% / 2.19 / 24 | 7.8% / 1.30 / 23 | 1.9% / 0.58 / 21 | 12.2% / 1.19 / 52 |
| 9 | 7.8% / 1.04 / 29 | 4.6% / 1.46 / 12 | 7.0% / 1.17 / 16 | 2.3% / 0.92 / 10 | 4.3% / 0.52 / 46 |
| 10 | -0.4% / -0.00 / 41 | 8.7% / 2.65 / 15 | 12.9% / 1.11 / 21 | 8.5% / 2.32 / 17 | 9.8% / 0.89 / 61 |
| 11 | -0.3% / -0.01 / 25 | -2.0% / -0.58 / 12 | 26.9% / 2.70 / 16 | 5.1% / 1.71 / 14 | 4.6% / 0.55 / 33 |
| 12 | 8.4% / 1.10 / 29 | 4.4% / 1.48 / 12 | 7.3% / 1.13 / 16 | 2.2% / 0.87 / 10 | 4.0% / 0.49 / 46 |
| 13 | 5.3% / 0.57 / 27 | 3.4% / 0.69 / 22 | 14.3% / 1.10 / 19 | 13.9% / 2.36 / 18 | 6.7% / 0.58 / 44 |
| 14 | 2.6% / 0.34 / 25 | -0.9% / -0.17 / 14 | 23.5% / 2.16 / 18 | 9.7% / 2.04 / 14 | 8.9% / 0.89 / 33 |
| 15 | 8.7% / 1.11 / 35 | 5.6% / 1.36 / 26 | 6.3% / 0.65 / 21 | 6.5% / 1.72 / 21 | 7.6% / 0.73 / 59 |
| 16 | 1.4% / 0.19 / 33 | 3.6% / 0.92 / 18 | 13.3% / 1.15 / 19 | 7.3% / 2.01 / 13 | 8.4% / 0.90 / 38 |
| 17 | -0.3% / -0.01 / 25 | -2.0% / -0.58 / 12 | 25.7% / 2.67 / 16 | 4.9% / 1.68 / 14 | 3.6% / 0.45 / 33 |
| 18 | 7.8% / 1.01 / 35 | 5.5% / 1.30 / 26 | 6.2% / 0.64 / 21 | 6.1% / 1.77 / 21 | 8.1% / 0.77 / 59 |
| 19 | 4.1% / 0.49 / 42 | 3.1% / 0.75 / 22 | 10.2% / 0.92 / 22 | 7.7% / 2.02 / 18 | 7.7% / 0.81 / 50 |
| 20 | 4.9% / 0.58 / 42 | 3.0% / 0.73 / 22 | 9.6% / 0.88 / 22 | 7.6% / 2.02 / 18 | 7.7% / 0.81 / 50 |
| 21 | 4.7% / 1.09 / 20 | 0.2% / 0.09 / 13 | 4.3% / 0.82 / 14 | 5.1% / 1.84 / 13 | 5.4% / 0.97 / 45 |
| 22 | -3.6% / -0.44 / 29 | 5.7% / 1.20 / 16 | 7.5% / 0.84 / 19 | 6.8% / 1.21 / 20 | 14.8% / 1.82 / 45 |
| 23 | 0.8% / 0.13 / 33 | 3.5% / 0.90 / 18 | 13.8% / 1.18 / 19 | 7.3% / 2.01 / 13 | 8.5% / 0.90 / 38 |
| 24 | 4.2% / 0.44 / 30 | 3.0% / 0.62 / 19 | 18.2% / 1.37 / 19 | 10.0% / 1.91 / 14 | 7.2% / 0.68 / 39 |
| 25 | -6.6% / -0.73 / 31 | 7.5% / 2.36 / 13 | 15.5% / 1.13 / 18 | 7.4% / 2.15 / 14 | 11.4% / 1.10 / 44 |
| 26 | 3.7% / 0.55 / 29 | 4.0% / 1.19 / 14 | 20.8% / 1.69 / 20 | 5.3% / 1.58 / 19 | 4.6% / 0.44 / 43 |
| 27 | 1.6% / 0.36 / 41 | 9.9% / 2.71 / 36 | 7.1% / 1.13 / 24 | 0.7% / 0.25 / 26 | 8.0% / 1.25 / 59 |
| 28 | 6.5% / 0.87 / 30 | 10.2% / 2.55 / 24 | 3.9% / 0.48 / 23 | 1.6% / 0.51 / 21 | 8.1% / 0.84 / 51 |
| 29 | 3.8% / 0.59 / 35 | 4.6% / 1.33 / 20 | 16.1% / 1.76 / 23 | 3.8% / 1.33 / 24 | 6.5% / 0.63 / 50 |
| 30 | 5.0% / 0.49 / 34 | 8.4% / 1.51 / 23 | 3.7% / 0.33 / 26 | 14.9% / 2.33 / 22 | 12.9% / 1.09 / 42 |
| 31 | 3.8% / 0.39 / 35 | 6.9% / 1.20 / 29 | 8.7% / 0.69 / 25 | 15.5% / 2.45 / 26 | 5.6% / 0.47 / 51 |
| 32 | -6.0% / -0.66 / 31 | 7.9% / 2.44 / 13 | 14.8% / 1.11 / 18 | 7.6% / 2.19 / 14 | 9.3% / 0.91 / 44 |
| 33 | -3.2% / -0.95 / 76 | 3.9% / 1.28 / 112 | 19.1% / 2.51 / 74 | -1.6% / -0.45 / 102 | 1.0% / 0.22 / 74 |
| 34 | 1.4% / 0.25 / 30 | 7.4% / 2.14 / 24 | 8.4% / 1.37 / 23 | 2.3% / 0.68 / 21 | 10.7% / 1.14 / 51 |
| 35 | 0.7% / 0.12 / 27 | 5.4% / 0.99 / 22 | 17.0% / 1.38 / 19 | 14.7% / 2.44 / 18 | 6.0% / 0.50 / 44 |
| 36 | 4.2% / 0.64 / 35 | 4.4% / 1.28 / 20 | 14.4% / 1.63 / 23 | 3.4% / 1.25 / 24 | 6.5% / 0.62 / 50 |
| 37 | 4.1% / 0.61 / 29 | 4.1% / 1.20 / 14 | 19.6% / 1.63 / 20 | 5.3% / 1.58 / 19 | 3.5% / 0.35 / 43 |
| 38 | 0.9% / 0.37 / 49 | 3.3% / 1.26 / 76 | 21.6% / 3.12 / 47 | -2.8% / -0.88 / 78 | -3.0% / -0.68 / 53 |
| 39 | 2.3% / 0.39 / 89 | 9.4% / 1.95 / 80 | 19.9% / 2.12 / 73 | 6.2% / 1.31 / 87 | -4.2% / -0.51 / 101 |
| 40 | 0.2% / 0.08 / 107 | 2.4% / 0.69 / 139 | 20.7% / 2.60 / 113 | -1.0% / -0.28 / 128 | 0.4% / 0.09 / 94 |
| 41 | 4.0% / 0.55 / 92 | 7.1% / 1.61 / 75 | 30.4% / 2.19 / 71 | 0.4% / 0.11 / 75 | -0.2% / 0.03 / 120 |
| 42 | 4.9% / 0.72 / 30 | 8.7% / 2.34 / 24 | 3.7% / 0.50 / 23 | 1.5% / 0.47 / 21 | 7.8% / 0.81 / 51 |
| 43 | 2.2% / 0.29 / 25 | 0.2% / 0.07 / 14 | 13.2% / 1.07 / 17 | 9.5% / 2.00 / 14 | 9.8% / 0.91 / 33 |
| 44 | -1.3% / -0.12 / 118 | 8.3% / 1.87 / 88 | 24.3% / 1.78 / 79 | 3.9% / 0.71 / 97 | 0.0% / 0.05 / 151 |
| 45 | -4.2% / -0.52 / 29 | 5.0% / 1.07 / 16 | 7.1% / 0.80 / 19 | 6.6% / 1.20 / 20 | 14.4% / 1.84 / 45 |
| 46 | -1.2% / -0.22 / 49 | 7.0% / 1.80 / 49 | 11.7% / 1.36 / 41 | -3.2% / -0.93 / 41 | 9.5% / 1.19 / 82 |
| 47 | -1.9% / -0.19 / 165 | 14.4% / 2.22 / 115 | 47.9% / 2.85 / 109 | 12.1% / 1.74 / 142 | -20.5% / -1.83 / 167 |
| 48 | 5.4% / 1.23 / 20 | 1.0% / 0.40 / 13 | 4.3% / 0.83 / 14 | 4.9% / 1.76 / 13 | 4.7% / 0.83 / 45 |
| 49 | -0.8% / -0.14 / 49 | 9.0% / 2.04 / 49 | 11.3% / 1.29 / 40 | -3.2% / -0.95 / 41 | 7.3% / 0.95 / 81 |
| 50 | 0.2% / 0.07 / 94 | 3.6% / 1.11 / 108 | 17.5% / 2.17 / 84 | -1.2% / -0.31 / 87 | 8.1% / 1.18 / 120 |
| 51 | 1.5% / 0.57 / 43 | 3.8% / 1.48 / 62 | 21.7% / 3.06 / 44 | -0.7% / -0.19 / 58 | -6.3% / -1.35 / 43 |
| 52 | 2.6% / 0.35 / 42 | 4.7% / 1.58 / 17 | 13.2% / 1.13 / 23 | 10.0% / 2.29 / 17 | 1.5% / 0.20 / 59 |
| 53 | 0.4% / 0.09 / 43 | 6.7% / 2.07 / 15 | 14.1% / 1.11 / 23 | 8.9% / 1.85 / 17 | 9.0% / 0.75 / 61 |
| 54 | 1.4% / 0.20 / 29 | 3.2% / 0.71 / 15 | 19.1% / 1.68 / 21 | 10.4% / 2.02 / 17 | 3.8% / 0.36 / 43 |
| 55 | 8.3% / 0.96 / 30 | 3.9% / 0.91 / 15 | 12.7% / 1.19 / 21 | 10.6% / 2.11 / 17 | 1.1% / 0.15 / 43 |
| 56 | 3.0% / 0.45 / 29 | 2.4% / 0.85 / 12 | 12.8% / 1.39 / 14 | 1.5% / 0.65 / 7 | 6.7% / 0.79 / 42 |
| 57 | -0.9% / -0.12 / 85 | 10.5% / 2.64 / 70 | 7.9% / 0.74 / 64 | 3.7% / 0.87 / 70 | 7.0% / 0.76 / 128 |
| 58 | 0.4% / 0.10 / 41 | 10.2% / 2.80 / 36 | 6.3% / 1.08 / 24 | 1.0% / 0.33 / 26 | 6.7% / 1.06 / 59 |
| 59 | 2.8% / 0.43 / 29 | 2.6% / 0.89 / 12 | 10.9% / 1.24 / 14 | 1.2% / 0.52 / 7 | 8.5% / 0.94 / 42 |
| 60 | -0.7% / -0.00 / 35 | 8.1% / 1.27 / 29 | 10.0% / 0.83 / 25 | 16.3% / 2.42 / 26 | 7.9% / 0.60 / 51 |
| 61 | 1.8% / 0.26 / 42 | 5.2% / 1.66 / 17 | 13.5% / 1.09 / 23 | 10.3% / 2.29 / 17 | 2.5% / 0.29 / 59 |
| 62 | -2.8% / -0.41 / 72 | 11.1% / 2.84 / 56 | 12.6% / 1.43 / 52 | 1.0% / 0.28 / 58 | 6.7% / 0.76 / 115 |
| 63 | 9.4% / 1.16 / 168 | 10.6% / 1.87 / 120 | 23.7% / 1.77 / 102 | 3.7% / 0.67 / 120 | -9.1% / -0.78 / 232 |
| 64 | -8.1% / -1.25 / 81 | 6.7% / 1.65 / 93 | 17.4% / 2.28 / 63 | 1.5% / 0.33 / 75 | 14.2% / 1.42 / 111 |
| 65 | -2.1% / -0.36 / 80 | 10.0% / 2.21 / 77 | 24.4% / 2.02 / 71 | 3.9% / 0.86 / 84 | -7.6% / -1.26 / 87 |
| 66 | 10.6% / 1.16 / 81 | 10.4% / 2.00 / 70 | 26.2% / 1.94 / 64 | 7.3% / 1.27 / 70 | -11.3% / -0.94 / 104 |
| 67 | 1.6% / 0.29 / 93 | 4.7% / 1.30 / 106 | 14.8% / 1.93 / 83 | -1.7% / -0.45 / 86 | 8.9% / 1.26 / 120 |
| 68 | 0.8% / 0.16 / 88 | 8.7% / 1.80 / 79 | 20.2% / 2.12 / 73 | 7.0% / 1.43 / 87 | -5.0% / -0.64 / 99 |
| 69 | 3.1% / 0.74 / 39 | 3.2% / 1.45 / 25 | -0.1% / 0.01 / 27 | 1.7% / 0.60 / 34 | 11.9% / 1.67 / 98 |
| 70 | 10.7% / 1.17 / 81 | 11.6% / 2.05 / 70 | 25.0% / 1.93 / 64 | 8.3% / 1.32 / 70 | -16.1% / -1.41 / 101 |
| 71 | -1.4% / -0.24 / 79 | 10.6% / 2.24 / 77 | 29.4% / 2.32 / 71 | 5.4% / 1.13 / 84 | -9.4% / -1.54 / 87 |
| 72 | 2.8% / 0.55 / 234 | -3.4% / -0.73 / 212 | 36.3% / 3.17 / 221 | -6.1% / -1.00 / 210 | 3.5% / 0.45 / 218 |
| 73 | 0.7% / 0.15 / 114 | 4.0% / 1.20 / 121 | 12.6% / 1.63 / 91 | -2.8% / -0.55 / 106 | 11.5% / 1.53 / 155 |
| 74 | 4.0% / 0.85 / 35 | 4.2% / 1.03 / 29 | 3.7% / 0.64 / 22 | 3.5% / 1.05 / 26 | 7.2% / 0.80 / 59 |
| 75 | -5.2% / -0.73 / 70 | 7.0% / 1.52 / 63 | 11.0% / 1.50 / 47 | 6.5% / 1.34 / 65 | 11.8% / 1.13 / 105 |
| 76 | -6.9% / -0.88 / 68 | 9.4% / 1.90 / 61 | 12.5% / 1.55 / 46 | 5.8% / 1.14 / 62 | 9.2% / 0.86 / 101 |
| 77 | -2.3% / -0.24 / 107 | 13.3% / 2.13 / 85 | 38.8% / 2.26 / 83 | 11.8% / 1.92 / 100 | -13.2% / -1.15 / 108 |
| 78 | 5.9% / 0.86 / 26 | 0.6% / 0.23 / 11 | 13.2% / 1.35 / 16 | 1.3% / 0.51 / 11 | 14.1% / 1.43 / 41 |
| 79 | -0.1% / 0.01 / 113 | 4.7% / 1.31 / 119 | 13.6% / 1.80 / 91 | -1.8% / -0.35 / 106 | 13.9% / 1.76 / 154 |
| 80 | 3.6% / 0.78 / 125 | 1.4% / 0.34 / 142 | 10.7% / 1.12 / 118 | 3.4% / 0.81 / 124 | 5.5% / 0.80 / 143 |
| 81 | 3.8% / 0.46 / 24 | 2.1% / 0.53 / 10 | 15.9% / 1.27 / 16 | 12.0% / 2.13 / 15 | 0.6% / 0.11 / 35 |
| 82 | 9.0% / 1.61 / 182 | 4.7% / 1.00 / 174 | 2.6% / 0.33 / 138 | 4.8% / 1.05 / 165 | 5.4% / 0.64 / 204 |
| 83 | 0.4% / 0.10 / 31 | 2.4% / 1.04 / 21 | 2.6% / 0.48 / 20 | 1.9% / 0.59 / 27 | 15.1% / 1.90 / 67 |
| 84 | -0.5% / -0.05 / 83 | 9.0% / 2.13 / 86 | 8.9% / 1.08 / 70 | 4.1% / 0.99 / 72 | 1.9% / 0.29 / 97 |
| 85 | -0.7% / -0.12 / 52 | 12.1% / 3.17 / 41 | 8.8% / 1.16 / 38 | 0.1% / 0.04 / 40 | 4.2% / 0.59 / 94 |
| 86 | -2.6% / -0.36 / 294 | 2.0% / 0.38 / 272 | 23.2% / 2.11 / 270 | 4.0% / 0.62 / 268 | 6.5% / 0.65 / 341 |
| 87 | -7.6% / -1.12 / 79 | 7.7% / 1.61 / 93 | 11.5% / 1.45 / 62 | -1.1% / -0.18 / 75 | 18.0% / 1.75 / 110 |
| 88 | 1.6% / 0.43 / 37 | 1.3% / 0.62 / 33 | 11.3% / 2.06 / 34 | 2.1% / 0.63 / 35 | -0.8% / -0.23 / 18 |
| 89 | -2.1% / -0.30 / 72 | 11.9% / 2.95 / 56 | 11.2% / 1.30 / 52 | 0.1% / 0.05 / 58 | 5.4% / 0.61 / 115 |
| 90 | 1.8% / 0.47 / 37 | 1.4% / 0.66 / 33 | 11.5% / 2.10 / 34 | 1.7% / 0.51 / 35 | -0.8% / -0.23 / 18 |
| 91 | 3.1% / 0.82 / 40 | 3.6% / 1.97 / 24 | 4.3% / 0.93 / 26 | 1.7% / 0.64 / 34 | 2.7% / 0.51 / 97 |
| 92 | 2.3% / 0.31 / 288 | 1.5% / 0.37 / 260 | 17.9% / 1.97 / 230 | 15.8% / 2.79 / 266 | -5.3% / -0.52 / 358 |
| 93 | 8.1% / 0.92 / 30 | 4.8% / 0.88 / 17 | 10.9% / 0.65 / 23 | 11.8% / 1.42 / 27 | 8.4% / 0.67 / 50 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_c011` | 4 | 0.99 | 0.99/0.99 | 0.97/0.97 |
| 1 | `cfg_d3e5` | 4 | 0.89 | 0.95/0.98 | 0.83/0.96 |
| 2 | `cfg_033c` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 3 | `cfg_612a` | 12 | 0.86 | 0.65/0.90 | 0.45/0.85 |
| 4 | `cfg_0c6f` | 1 | n/a | n/a/n/a | n/a/n/a |
| 5 | `cfg_183b` | 4 | 0.98 | 0.97/0.98 | 0.99/0.99 |
| 6 | `cfg_50dd` | 4 | 0.96 | 0.99/0.99 | 0.97/0.99 |
| 7 | `cfg_1463` | 3 | 0.92 | 0.91/0.93 | 0.88/0.90 |
| 8 | `cfg_15fd` | 7 | 0.90 | 0.90/0.95 | 0.91/0.96 |
| 9 | `cfg_194b` | 4 | 0.95 | 0.93/0.94 | 0.88/0.90 |
| 10 | `cfg_1b2f` | 1 | n/a | n/a/n/a | n/a/n/a |
| 11 | `cfg_7831` | 5 | 0.83 | 0.66/0.98 | 0.33/0.98 |
| 12 | `cfg_25e3` | 4 | 0.91 | 0.95/0.97 | 0.90/0.94 |
| 13 | `cfg_efd8` | 4 | 0.85 | 0.77/0.95 | 0.61/0.90 |
| 14 | `cfg_283f` | 2 | 0.87 | 0.89/0.89 | 0.87/0.87 |
| 15 | `cfg_ebb8` | 4 | 0.86 | 0.86/0.86 | 0.57/0.66 |
| 16 | `cfg_3088` | 1 | n/a | n/a/n/a | n/a/n/a |
| 17 | `cfg_4928` | 4 | 1.00 | 1.00/1.00 | 0.96/0.96 |
| 18 | `cfg_702b` | 5 | 0.83 | 0.92/0.98 | 0.88/0.95 |
| 19 | `cfg_fd46` | 3 | 0.94 | 0.97/0.98 | 0.94/0.95 |
| 20 | `cfg_448e` | 3 | 0.83 | 0.88/0.94 | 0.73/0.86 |
| 21 | `cfg_a6d0` | 6 | 0.90 | 0.85/0.89 | 0.75/0.80 |
| 22 | `cfg_57a8` | 6 | 0.87 | 0.72/0.76 | 0.44/0.47 |
| 23 | `cfg_846b` | 3 | 0.94 | 0.97/0.98 | 0.94/0.97 |
| 24 | `cfg_b13f` | 2 | 0.94 | 0.97/0.97 | 0.95/0.95 |
| 25 | `cfg_4bf6` | 2 | 0.84 | 0.62/0.62 | 0.48/0.48 |
| 26 | `cfg_4d88` | 3 | 0.91 | 0.97/0.98 | 0.96/0.96 |
| 27 | `cfg_4de4` | 3 | 0.96 | 0.99/0.99 | 0.98/0.99 |
| 28 | `cfg_4e88` | 1 | n/a | n/a/n/a | n/a/n/a |
| 29 | `cfg_4f7e` | 1 | n/a | n/a/n/a | n/a/n/a |
| 30 | `cfg_4fa5` | 3 | 0.99 | 1.00/1.00 | 0.99/0.99 |
| 31 | `cfg_517d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 32 | `cfg_f5fd` | 3 | 0.89 | 0.88/0.88 | 0.82/0.88 |
| 33 | `cfg_6267` | 2 | 1.00 | 0.99/0.99 | 1.00/1.00 |
| 34 | `cfg_e52c` | 4 | 0.96 | 0.98/0.99 | 0.96/0.99 |
| 35 | `cfg_56e3` | 1 | n/a | n/a/n/a | n/a/n/a |
| 36 | `cfg_6c5b` | 3 | 0.92 | 0.95/0.96 | 0.92/0.96 |
| 37 | `cfg_d433` | 3 | 0.89 | 0.90/0.93 | 0.77/0.87 |
| 38 | `cfg_92d9` | 3 | 0.92 | 0.95/0.97 | 0.84/0.91 |
| 39 | `cfg_66c6` | 1 | n/a | n/a/n/a | n/a/n/a |
| 40 | `cfg_7916` | 3 | 0.83 | 0.92/0.93 | 0.86/0.90 |
| 41 | `cfg_7b73` | 1 | n/a | n/a/n/a | n/a/n/a |
| 42 | `cfg_87ba` | 1 | n/a | n/a/n/a | n/a/n/a |
| 43 | `cfg_c601` | 3 | 0.83 | 0.80/0.83 | 0.73/0.78 |
| 44 | `cfg_92a5` | 1 | n/a | n/a/n/a | n/a/n/a |
| 45 | `cfg_e9cc` | 2 | 0.99 | 0.99/0.99 | 0.98/0.98 |
| 46 | `cfg_9879` | 1 | n/a | n/a/n/a | n/a/n/a |
| 47 | `cfg_ca23` | 4 | 0.89 | 0.84/0.85 | 0.87/0.87 |
| 48 | `cfg_b73c` | 1 | n/a | n/a/n/a | n/a/n/a |
| 49 | `cfg_c19c` | 1 | n/a | n/a/n/a | n/a/n/a |
| 50 | `cfg_c2d9` | 2 | 0.99 | 0.99/0.99 | 0.98/0.98 |
| 51 | `cfg_fa6a` | 2 | 0.95 | 0.98/0.98 | 0.98/0.98 |
| 52 | `cfg_d1c6` | 1 | n/a | n/a/n/a | n/a/n/a |
| 53 | `cfg_d3ee` | 1 | n/a | n/a/n/a | n/a/n/a |
| 54 | `cfg_d43b` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 7.242e-04 over 40752 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1230.0, participation ratio 22.2, 95%-variance components 309 (rank bound T = 1259); raw grid 41472; raw + known prior 472488
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
