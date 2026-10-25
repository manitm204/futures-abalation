# Screening funnel -- mr_nq_v6 (development stages only)

- Code: `5342a94cdc84` (dirty working tree: True, diff sha256 `58ae07e01ce8`)
- Config: `configs/funnel/mr_funnel_nq_v6.yaml` sha256 `d5c74916440d405b`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'NQ': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `81186f48b08020ff` (201 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_nq_v5 gated 93 NQ candidates on 2023-2024 (38 passed) and this v6 grid was narrowed around those survivors, so NQ 2023-2024 is largely in-sample for v6. The grid, the stage-4 test and the 40-trade rule were also shaped by ES 2023-2024 (mr_es_v3..v5).
- Holdout 2025+ previously inspected: **False** -- No NQ strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection). The holdout is the only untouched test for this run.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 21600 | 21600 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 21600 | 21600 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 21600 | 14236 | 7364 | 0 |  | 15242 | 65.91 | 65.91 |  |
| 3 performance & risk | hard_gate | 14236 | 394 | 13842 | 0 |  | 0 | 1.82 | 2.77 |  |
| 4 parameter stability | hard_gate | 394 | 383 | 11 | 0 |  | 0 | 1.77 | 97.21 |  |
| 5 time stability | hard_gate | 383 | 383 | 0 | 0 |  | 275 | 1.77 | 100.00 |  |
| 6 deduplication | dedup | 383 | 201 |  |  | 182 |  | 0.93 | 52.48 | best 2 per cluster |
| 7 execution stress | hard_gate | 201 | 201 | 0 | 0 |  | 0 | 0.93 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 201 |  |  |  |  |  |  |  | diagnostic only: unverified: 201 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 7364 |
| s2:hard_reject:years_with_>=10_trades | 6315 |
| s3:hard_reject:max_drawdown | 1300 |
| s3:hard_reject:net_return | 10195 |
| s3:hard_reject:sharpe | 13842 |
| s4:hard_reject:local_median_sharpe | 11 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_7a6c` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 21/62/26 | 109 | 71.4% | 11.4% | 1.45 | -5.6% | 205 | 2.39 | 6.3% | 57.1 | 10/10 | 0.90 | 0.88 | 0.57 | 5 | 39.9% | 0.44 | 0.36 | 70.8% | 70.2% | 34.4% | 62.1%/52.1% | n/a (profitable_beyond_25.0x) | pass | 0.155 (unverified) | 1.08 |
| 2 | `cfg_e19e` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.5, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 48/39/27 | 114 | 55.0% | 9.2% | 1.43 | -5.7% | 260 | 2.11 | 5.9% | 59.0 | 11/11 | 0.91 | 0.83 | 0.60 | 5 | 35.8% | 0.35 | 0.40 | 54.7% | 53.8% | 17.8% | 46.4%/39.3% | n/a (profitable_beyond_25.0x) | pass | 0.153 (unverified) | 0.75 |
| 3 | `cfg_fa9e` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 33/50/26 | 109 | 64.3% | 10.4% | 1.36 | -5.6% | 205 | 2.27 | 6.1% | 56.8 | 11/11 | 0.91 | 0.91 | 0.45 | 5 | 38.6% | 0.40 | 0.37 | 64.3% | 63.8% | 30.9% | 54.8%/45.9% | n/a (profitable_beyond_25.0x) | pass | 0.110 (unverified) | 1.18 |
| 4 | `cfg_fb2f` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-3.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 22/58/27 | 107 | 40.7% | 7.1% | 1.25 | -3.7% | 159 | 1.87 | 5.9% | 55.0 | 11/11 | 0.91 | 0.98 | 0.27 | 5 | 26.7% | 0.34 | 0.49 | 40.2% | 40.2% | 30.4% | 36.7%/28.4% | n/a (profitable_beyond_25.0x) | pass | 0.079 (unverified) | 0.44 |
| 5 | `cfg_2406` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-3.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 30/50/27 | 107 | 38.2% | 6.7% | 1.21 | -3.7% | 159 | 1.83 | 5.8% | 54.8 | 11/11 | 0.91 | 1.04 | 0.18 | 5 | 25.5% | 0.33 | 0.51 | 37.4% | 36.5% | 27.2% | 34.1%/26.3% | n/a (profitable_beyond_25.0x) | pass | 0.066 (unverified) | 0.52 |
| 6 | `cfg_acb3` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 22/73/37 | 132 | 47.6% | 8.1% | 1.18 | -5.6% | 209 | 1.80 | 7.4% | 67.6 | 12/12 | 0.92 | 0.99 | 0.19 | 5 | 20.1% | 0.51 | 0.47 | 47.0% | 47.0% | 33.1% | 42.3%/32.9% | n/a (profitable_beyond_25.0x) | pass | 0.055 (unverified) | 0.58 |
| 7 | `cfg_b418` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 15/79/38 | 132 | 44.6% | 7.7% | 1.12 | -5.4% | 209 | 1.74 | 7.6% | 67.4 | 11/11 | 0.91 | 0.94 | 0.18 | 4 | 19.6% | 0.50 | 0.49 | 43.9% | 43.9% | 27.6% | 41.8%/34.2% | n/a (profitable_beyond_25.0x) | pass | 0.040 (unverified) | 0.55 |
| 8 | `cfg_632c` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 41/43/27 | 111 | 47.1% | 8.0% | 1.27 | -4.0% | 91 | 1.93 | 6.0% | 57.4 | 12/12 | 0.92 | 0.78 | 0.49 | 5 | 32.0% | 0.32 | 0.41 | 46.7% | 45.0% | 17.4% | 40.4%/32.1% | n/a (profitable_beyond_25.0x) | pass | 0.078 (unverified) | 0.72 |
| 9 | `cfg_cd73` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 56/26/53 | 135 | 67.8% | 10.9% | 1.28 | -7.6% | 197 | 1.74 | 10.4% | 70.7 | 11/11 | 0.91 | 0.85 | 0.44 | 5 | 32.4% | 0.44 | 0.40 | 67.1% | 66.7% | 45.8% | 57.7%/48.9% | n/a (profitable_beyond_25.0x) | pass | 0.094 (unverified) | 0.02 |
| 10 | `cfg_1223` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 18/74/37 | 129 | 61.9% | 10.1% | 1.16 | -10.7% | 486 | 1.93 | 7.3% | 68.0 | 10/10 | 0.90 | 0.89 | 0.27 | 4 | 36.5% | 0.41 | 0.40 | 61.0% | 59.5% | 35.2% | 54.8%/41.0% | n/a (profitable_beyond_25.0x) | pass | 0.054 (unverified) | 0.73 |
| 11 | `cfg_02d6` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 48/22/42 | 112 | 55.2% | 9.2% | 1.12 | -6.0% | 228 | 1.74 | 8.1% | 58.8 | 10/10 | 0.90 | 0.95 | 0.17 | 5 | 34.8% | 0.37 | 0.44 | 55.1% | 55.0% | 28.8% | 45.4%/36.0% | n/a (profitable_beyond_25.0x) | pass | 0.053 (unverified) | 1.05 |
| 12 | `cfg_248c` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 27/57/27 | 111 | 49.8% | 8.4% | 1.21 | -3.9% | 126 | 1.95 | 6.4% | 57.7 | 12/12 | 0.92 | 0.79 | 0.41 | 5 | 33.8% | 0.32 | 0.43 | 49.5% | 49.0% | 21.0% | 43.2%/34.5% | n/a (profitable_beyond_25.0x) | pass | 0.049 (unverified) | 0.60 |
| 13 | `cfg_b2f7` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 31/61/37 | 129 | 58.2% | 9.6% | 1.09 | -10.4% | 421 | 1.88 | 7.1% | 67.8 | 11/11 | 0.91 | 0.95 | 0.14 | 4 | 36.6% | 0.37 | 0.41 | 57.5% | 57.0% | 29.6% | 53.6%/42.0% | n/a (profitable_beyond_25.0x) | pass | 0.042 (unverified) | 0.59 |
| 14 | `cfg_2e66` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 40/29/43 | 112 | 57.2% | 9.5% | 1.10 | -6.0% | 218 | 1.76 | 8.9% | 58.7 | 9/9 | 0.89 | 0.91 | 0.19 | 5 | 35.0% | 0.39 | 0.43 | 56.7% | 56.2% | 28.5% | 49.4%/36.6% | n/a (profitable_beyond_25.0x) | pass | 0.044 (unverified) | 0.93 |
| 15 | `cfg_d6d2` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=8, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 35/44/27 | 106 | 41.9% | 7.3% | 1.16 | -4.8% | 253 | 2.01 | 5.7% | 54.8 | 10/10 | 0.90 | 0.89 | 0.27 | 5 | 21.2% | 0.50 | 0.43 | 41.5% | 41.3% | 10.4% | 38.0%/29.7% | n/a (profitable_beyond_25.0x) | pass | 0.049 (unverified) | 0.36 |
| 16 | `cfg_50b3` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 30/61/33 | 124 | 54.7% | 9.1% | 1.14 | -6.5% | 266 | 1.87 | 7.1% | 64.4 | 12/12 | 0.92 | 0.88 | 0.26 | 5 | 35.6% | 0.35 | 0.40 | 52.8% | 52.7% | 31.1% | 48.5%/37.1% | n/a (profitable_beyond_25.0x) | pass | 0.062 (unverified) | 0.92 |
| 17 | `cfg_12b9` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=8, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 24/55/27 | 106 | 44.7% | 7.7% | 1.14 | -4.8% | 262 | 2.06 | 6.0% | 54.8 | 9/9 | 0.89 | 0.97 | 0.18 | 4 | 23.3% | 0.48 | 0.43 | 44.2% | 43.8% | 17.5% | 38.6%/31.9% | n/a (profitable_beyond_25.0x) | pass | 0.038 (unverified) | 0.38 |
| 18 | `cfg_df5b` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 21/70/33 | 124 | 56.1% | 9.3% | 1.16 | -6.5% | 266 | 1.89 | 7.1% | 64.6 | 12/12 | 0.92 | 0.83 | 0.33 | 5 | 36.6% | 0.35 | 0.39 | 55.0% | 54.4% | 33.4% | 50.6%/39.7% | n/a (profitable_beyond_25.0x) | pass | 0.068 (unverified) | 0.80 |
| 19 | `cfg_0e11` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 59/23/53 | 135 | 52.0% | 8.7% | 1.12 | -8.1% | 172 | 1.59 | 9.8% | 70.4 | 11/11 | 0.91 | 0.78 | 0.34 | 5 | 24.3% | 0.46 | 0.45 | 49.8% | 49.5% | 32.9% | 47.3%/38.4% | n/a (profitable_beyond_25.0x) | pass | 0.050 (unverified) | 0.00 |
| 20 | `cfg_b3b8` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=8, entry_z=-3.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 10/84/37 | 131 | 37.4% | 6.6% | 0.99 | -4.5% | 187 | 1.60 | 7.5% | 66.9 | 10/10 | 0.90 | 0.83 | 0.16 | 5 | 17.6% | 0.47 | 0.52 | 37.4% | 36.9% | 36.4% | 34.3%/27.3% | n/a (profitable_beyond_25.0x) | pass | 0.024 (unverified) | 0.41 |
| 21 | `cfg_4398` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=8, entry_z=-3.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 15/79/37 | 131 | 36.9% | 6.5% | 0.98 | -4.5% | 187 | 1.59 | 7.4% | 66.9 | 11/11 | 0.91 | 0.83 | 0.15 | 5 | 16.6% | 0.49 | 0.53 | 36.9% | 36.7% | 35.8% | 34.1%/26.7% | n/a (profitable_beyond_25.0x) | pass | 0.022 (unverified) | 0.39 |
| 22 | `cfg_54bf` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=5, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 83/37/81 | 201 | 83.1% | 12.9% | 1.17 | -10.5% | 178 | 1.58 | 14.5% | 105.3 | 9/9 | 0.89 | 0.84 | 0.33 | 5 | 39.4% | 0.42 | 0.40 | 78.6% | 77.5% | 53.7% | 72.8%/58.2% | n/a (profitable_beyond_25.0x) | pass | 0.062 (unverified) | 0.27 |
| 23 | `cfg_c5fa` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=8, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 45/66/40 | 151 | 51.6% | 8.7% | 1.11 | -6.8% | 93 | 1.67 | 8.3% | 77.2 | 12/12 | 0.92 | 0.78 | 0.33 | 5 | 27.9% | 0.40 | 0.45 | 48.5% | 47.9% | 29.8% | 42.3%/33.3% | n/a (profitable_beyond_25.0x) | pass | 0.049 (unverified) | 0.61 |
| 24 | `cfg_4220` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 26/74/35 | 135 | 54.7% | 9.1% | 1.06 | -7.3% | 243 | 1.81 | 7.7% | 70.4 | 12/12 | 0.92 | 0.82 | 0.24 | 5 | 34.1% | 0.38 | 0.41 | 54.2% | 52.8% | 22.8% | 48.5%/38.5% | n/a (profitable_beyond_25.0x) | pass | 0.037 (unverified) | 0.40 |
| 25 | `cfg_17a2` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=5, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 95/31/90 | 216 | 79.8% | 12.5% | 1.11 | -8.1% | 164 | 1.51 | 15.1% | 113.4 | 7/7 | 0.86 | 0.84 | 0.27 | 5 | 34.6% | 0.45 | 0.42 | 78.4% | 77.8% | 52.9% | 73.6%/58.6% | n/a (profitable_beyond_25.0x) | pass | 0.049 (unverified) | 0.58 |
| 26 | `cfg_bebf` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=8, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 59/31/58 | 148 | 59.6% | 9.8% | 1.02 | -7.2% | 204 | 1.58 | 11.6% | 77.9 | 9/9 | 0.89 | 0.94 | 0.08 | 5 | 37.7% | 0.37 | 0.42 | 59.3% | 58.5% | 30.0% | 51.2%/37.9% | n/a (profitable_beyond_25.0x) | pass | 0.033 (unverified) | 0.31 |
| 27 | `cfg_56c7` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=8, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 33/76/42 | 151 | 49.3% | 8.4% | 1.06 | -6.9% | 140 | 1.63 | 8.5% | 76.9 | 12/12 | 0.92 | 0.82 | 0.24 | 5 | 26.3% | 0.41 | 0.45 | 48.5% | 48.2% | 27.3% | 47.9%/34.3% | n/a (profitable_beyond_25.0x) | pass | 0.039 (unverified) | 0.49 |
| 28 | `cfg_4f4e` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 48/54/0 | 102 | 63.4% | 10.3% | 1.24 | -5.6% | 237 | 1.97 | 10.5% | 52.9 | 11/11 | 0.91 | 0.80 | 0.44 | 5 | 25.8% | 0.51 | 0.43 | 61.7% | 60.8% | 42.9% | 55.4%/45.8% | n/a (profitable_beyond_25.0x) | pass | 0.085 (unverified) | -0.18 |
| 29 | `cfg_2e49` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 4/104/20 | 128 | 32.2% | 5.7% | 1.01 | -3.0% | 295 | 1.72 | 5.4% | 65.5 | 9/9 | 0.89 | 0.78 | 0.24 | 5 | 16.4% | 0.44 | 0.69 | 31.4% | 31.0% | 12.5% | 30.0%/23.7% | n/a (profitable_beyond_25.0x) | pass | 0.019 (unverified) | 0.51 |
| 30 | `cfg_5d8c` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 5/103/20 | 128 | 30.9% | 5.5% | 0.99 | -3.0% | 295 | 1.70 | 5.4% | 64.7 | 10/10 | 0.90 | 0.76 | 0.23 | 5 | 16.4% | 0.42 | 0.68 | 30.4% | 29.5% | 11.0% | 28.5%/22.6% | n/a (profitable_beyond_25.0x) | pass | 0.017 (unverified) | 0.51 |
| 31 | `cfg_27b7` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=8, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 47/18/41 | 106 | 43.4% | 7.5% | 1.05 | -6.5% | 295 | 1.65 | 7.9% | 55.2 | 8/8 | 0.88 | 0.78 | 0.28 | 5 | 28.6% | 0.34 | 0.48 | 43.0% | 42.5% | 15.2% | 39.7%/33.0% | n/a (profitable_beyond_25.0x) | pass | 0.036 (unverified) | 0.18 |
| 32 | `cfg_6421` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 54/29/50 | 133 | 68.6% | 11.0% | 1.12 | -6.8% | 138 | 1.73 | 10.2% | 69.5 | 11/11 | 0.91 | 0.88 | 0.24 | 5 | 40.6% | 0.32 | 0.38 | 68.1% | 67.5% | 28.2% | 61.8%/50.4% | n/a (profitable_beyond_25.0x) | pass | 0.059 (unverified) | 0.68 |
| 33 | `cfg_5849` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=8, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 22/65/13 | 100 | 25.9% | 4.7% | 1.05 | -3.0% | 262 | 1.93 | 4.1% | 51.0 | 9/9 | 0.89 | 0.83 | 0.22 | 5 | 13.3% | 0.49 | 0.57 | 25.5% | 25.1% | 10.6% | 23.9%/19.3% | n/a (profitable_beyond_25.0x) | pass | 0.030 (unverified) | 0.12 |
| 34 | `cfg_8359` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 54/26/57 | 137 | 54.8% | 9.1% | 0.96 | -6.2% | 212 | 1.54 | 9.9% | 72.4 | 10/10 | 0.90 | 0.88 | 0.07 | 5 | 32.6% | 0.33 | 0.49 | 53.4% | 53.1% | 33.1% | 50.7%/36.7% | n/a (profitable_beyond_25.0x) | pass | 0.025 (unverified) | 0.49 |
| 35 | `cfg_9067` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=5, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 76/30/73 | 179 | 62.0% | 10.1% | 0.97 | -7.8% | 182 | 1.50 | 12.5% | 94.0 | 10/10 | 0.90 | 0.81 | 0.17 | 5 | 32.0% | 0.38 | 0.44 | 61.4% | 59.7% | 29.3% | 57.2%/44.4% | n/a (profitable_beyond_25.0x) | pass | 0.024 (unverified) | 0.37 |
| 36 | `cfg_a9a6` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 20/80/35 | 135 | 51.1% | 8.6% | 1.01 | -7.4% | 243 | 1.76 | 7.8% | 69.8 | 11/11 | 0.91 | 0.74 | 0.27 | 5 | 32.1% | 0.37 | 0.41 | 50.4% | 50.3% | 21.9% | 46.8%/35.6% | n/a (profitable_beyond_25.0x) | pass | 0.029 (unverified) | 0.39 |
| 37 | `cfg_8db5` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=8, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 69/21/59 | 149 | 53.0% | 8.9% | 0.99 | -7.0% | 328 | 1.54 | 10.7% | 77.1 | 10/10 | 0.90 | 0.80 | 0.19 | 5 | 33.3% | 0.37 | 0.44 | 52.7% | 50.6% | 25.8% | 43.7%/35.6% | n/a (profitable_beyond_25.0x) | pass | 0.030 (unverified) | 0.34 |
| 38 | `cfg_7932` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 11/84/38 | 133 | 48.4% | 8.2% | 1.01 | -6.8% | 123 | 1.70 | 7.7% | 67.9 | 10/10 | 0.90 | 0.81 | 0.20 | 5 | 22.0% | 0.48 | 0.55 | 47.7% | 45.1% | 11.4% | 44.1%/31.1% | n/a (profitable_beyond_25.0x) | pass | 0.021 (unverified) | 1.08 |
| 39 | `cfg_4570` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 87/4/44 | 135 | 46.2% | 7.9% | 1.10 | -5.0% | 200 | 1.74 | 7.3% | 69.5 | 9/9 | 0.89 | 0.69 | 0.41 | 5 | 27.3% | 0.41 | 0.42 | 45.6% | 44.9% | 26.3% | 42.4%/36.1% | n/a (profitable_beyond_25.0x) | pass | 0.042 (unverified) | 0.52 |
| 40 | `cfg_cfe7` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=8, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 66/31/62 | 159 | 58.0% | 9.6% | 0.92 | -13.0% | 148 | 1.50 | 11.9% | 83.2 | 11/11 | 0.91 | 0.74 | 0.18 | 5 | 38.1% | 0.34 | 0.43 | 56.7% | 56.6% | 42.0% | 53.8%/36.9% | n/a (profitable_beyond_25.0x) | pass | 0.023 (unverified) | 0.15 |
| 41 | `cfg_3afa` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 3/82/17 | 102 | 29.8% | 5.4% | 1.05 | -4.7% | 317 | 1.99 | 4.3% | 51.8 | 9/9 | 0.78 | 0.67 | 0.39 | 4 | 13.1% | 0.50 | 0.72 | 29.4% | 29.0% | 8.1% | 25.8%/19.3% | n/a (profitable_beyond_25.0x) | pass | 0.036 (unverified) | 0.90 |
| 42 | `cfg_2437` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=8, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 24/82/37 | 143 | 48.8% | 8.3% | 1.07 | -6.9% | 185 | 1.72 | 8.2% | 73.5 | 10/10 | 0.90 | 0.94 | 0.13 | 4 | 21.2% | 0.49 | 0.42 | 48.4% | 47.3% | 23.9% | 43.1%/35.0% | n/a (profitable_beyond_25.0x) | pass | 0.030 (unverified) | 0.47 |
| 43 | `cfg_1fc3` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=8, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 50/65/49 | 164 | 46.7% | 8.0% | 0.96 | -8.5% | 322 | 1.53 | 8.8% | 83.4 | 11/11 | 0.73 | 0.75 | 0.21 | 4 | 6.8% | 0.83 | 0.55 | 46.3% | 45.2% | 25.6% | 45.0%/33.8% | n/a (profitable_beyond_25.0x) | pass | 0.019 (unverified) | 0.31 |
| 44 | `cfg_efa5` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=8, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 53/53/37 | 143 | 42.0% | 7.3% | 1.03 | -6.8% | 307 | 1.64 | 7.6% | 73.7 | 11/11 | 0.91 | 0.96 | 0.07 | 4 | 15.9% | 0.54 | 0.43 | 41.0% | 39.8% | 12.3% | 36.1%/27.3% | n/a (profitable_beyond_25.0x) | pass | 0.027 (unverified) | 0.51 |
| 45 | `cfg_61e1` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=5, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 63/41/74 | 178 | 61.1% | 10.0% | 0.95 | -7.5% | 362 | 1.49 | 13.4% | 92.9 | 9/9 | 0.89 | 0.76 | 0.20 | 5 | 32.3% | 0.37 | 0.46 | 59.2% | 58.4% | 19.7% | 55.9%/47.0% | n/a (profitable_beyond_25.0x) | pass | 0.021 (unverified) | 0.34 |
| 46 | `cfg_7f48` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=8, entry_z=-2.0, exit_z=0.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 14/73/13 | 100 | 27.0% | 4.9% | 1.07 | -3.3% | 262 | 1.96 | 4.2% | 51.0 | 8/8 | 0.88 | 0.77 | 0.30 | 5 | 14.3% | 0.47 | 0.59 | 26.5% | 26.1% | 10.4% | 25.7%/20.1% | n/a (profitable_beyond_25.0x) | pass | 0.032 (unverified) | 0.15 |
| 47 | `cfg_17a8` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 48/14/45 | 107 | 38.1% | 6.7% | 0.91 | -8.4% | 221 | 1.58 | 7.9% | 55.3 | 10/10 | 0.80 | 0.63 | 0.28 | 3 | 11.5% | 0.62 | 0.57 | 37.6% | 37.3% | 28.4% | 32.5%/24.4% | n/a (profitable_beyond_25.0x) | pass | 0.021 (unverified) | 1.07 |
| 48 | `cfg_503c` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.0, exit_z=-1.25, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 62/22/50 | 134 | 57.5% | 9.5% | 1.04 | -6.8% | 211 | 1.64 | 9.4% | 70.1 | 10/10 | 0.90 | 0.66 | 0.38 | 5 | 34.1% | 0.33 | 0.41 | 56.9% | 56.3% | 29.1% | 52.5%/42.3% | n/a (profitable_beyond_25.0x) | pass | 0.040 (unverified) | 0.72 |
| 49 | `cfg_8fa0` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 8/62/33 | 103 | 35.9% | 6.3% | 0.94 | -6.4% | 530 | 1.73 | 6.0% | 53.0 | 10/10 | 0.80 | 0.56 | 0.38 | 3 | 8.3% | 0.69 | 0.69 | 35.2% | 34.8% | 10.8% | 31.5%/21.7% | n/a (profitable_beyond_25.0x) | pass | 0.018 (unverified) | 0.96 |
| 50 | `cfg_52a1` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=5, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 88/36/86 | 210 | 63.1% | 10.3% | 0.86 | -10.2% | 172 | 1.40 | 15.0% | 110.4 | 10/10 | 0.90 | 0.71 | 0.15 | 5 | 41.5% | 0.31 | 0.46 | 61.4% | 59.6% | 36.1% | 57.7%/48.8% | n/a (profitable_beyond_25.0x) | pass | 0.015 (unverified) | 0.38 |
| 51 | `cfg_499d` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 44/35/58 | 137 | 53.7% | 9.0% | 0.91 | -7.2% | 272 | 1.53 | 10.8% | 71.8 | 9/9 | 0.89 | 0.91 | 0.00 | 5 | 29.8% | 0.36 | 0.49 | 53.5% | 50.9% | 21.5% | 49.8%/35.9% | n/a (profitable_beyond_25.0x) | pass | 0.019 (unverified) | 0.44 |
| 52 | `cfg_9020` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 55/32/56 | 143 | 54.4% | 9.1% | 0.95 | -7.1% | 220 | 1.53 | 11.1% | 75.5 | 11/11 | 0.91 | 0.78 | 0.17 | 5 | 33.7% | 0.35 | 0.47 | 54.0% | 53.5% | 39.4% | 50.9%/39.0% | n/a (profitable_beyond_25.0x) | pass | 0.023 (unverified) | 0.45 |
| 53 | `cfg_027d` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 14/81/38 | 133 | 46.4% | 7.9% | 0.98 | -6.9% | 123 | 1.67 | 7.6% | 68.4 | 11/11 | 0.91 | 0.80 | 0.18 | 5 | 21.5% | 0.48 | 0.55 | 44.1% | 43.3% | 6.4% | 40.8%/28.3% | n/a (profitable_beyond_25.0x) | pass | 0.018 (unverified) | 1.09 |
| 54 | `cfg_817f` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.0, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 79/51/42 | 172 | 56.1% | 9.3% | 1.11 | -7.7% | 284 | 1.74 | 8.6% | 89.5 | 10/10 | 0.90 | 0.68 | 0.43 | 4 | 28.4% | 0.39 | 0.39 | 56.2% | 55.6% | 20.1% | 51.6%/39.4% | n/a (profitable_beyond_25.0x) | pass | 0.054 (unverified) | 0.28 |
| 55 | `cfg_084a` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 53/49/0 | 102 | 45.4% | 7.8% | 1.00 | -6.4% | 327 | 1.72 | 10.0% | 52.6 | 11/11 | 0.91 | 0.63 | 0.37 | 4 | 15.3% | 0.60 | 0.49 | 45.1% | 44.7% | 29.5% | 41.7%/33.4% | n/a (profitable_beyond_25.0x) | pass | 0.030 (unverified) | -0.18 |
| 56 | `cfg_e550` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=8, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 58/36/65 | 159 | 56.4% | 9.4% | 1.00 | -7.1% | 149 | 1.47 | 12.8% | 83.3 | 10/10 | 0.90 | 0.70 | 0.30 | 5 | 39.3% | 0.26 | 0.48 | 55.2% | 54.5% | 35.5% | 50.3%/36.0% | n/a (profitable_beyond_25.0x) | pass | 0.029 (unverified) | 0.32 |
| 57 | `cfg_28ab` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=8, entry_z=-3.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 58/25/55 | 138 | 52.2% | 8.8% | 0.94 | -9.8% | 191 | 1.53 | 10.4% | 71.4 | 10/10 | 0.90 | 0.78 | 0.16 | 5 | 32.1% | 0.32 | 0.48 | 49.4% | 48.1% | 37.8% | 43.9%/34.4% | n/a (profitable_beyond_25.0x) | pass | 0.024 (unverified) | -0.13 |
| 58 | `cfg_ae93` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=5, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 114/20/79 | 213 | 63.7% | 10.4% | 0.95 | -13.0% | 186 | 1.41 | 13.0% | 111.5 | 10/10 | 0.90 | 0.77 | 0.18 | 4 | 20.9% | 0.61 | 0.49 | 64.0% | 63.3% | 33.0% | 61.5%/50.9% | n/a (profitable_beyond_25.0x) | pass | 0.023 (unverified) | 0.41 |
| 59 | `cfg_37e1` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 66/31/37 | 134 | 38.2% | 6.7% | 0.99 | -6.3% | 339 | 1.70 | 6.5% | 68.1 | 10/10 | 0.90 | 0.64 | 0.35 | 4 | 21.8% | 0.43 | 0.46 | 37.6% | 37.4% | 20.9% | 35.1%/28.0% | n/a (profitable_beyond_25.0x) | pass | 0.022 (unverified) | 0.63 |
| 60 | `cfg_5982` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=8, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 52/14/40 | 106 | 29.6% | 5.3% | 0.80 | -7.6% | 325 | 1.48 | 7.2% | 54.5 | 9/9 | 0.89 | 0.77 | 0.03 | 5 | 20.3% | 0.29 | 0.65 | 29.2% | 28.6% | 4.3% | 26.1%/21.0% | n/a (profitable_beyond_25.0x) | pass | 0.009 (unverified) | 0.27 |
| 61 | `cfg_3fc1` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 43/28/40 | 111 | 40.7% | 7.1% | 0.98 | -9.0% | 184 | 1.55 | 8.9% | 57.2 | 11/11 | 0.91 | 0.83 | 0.16 | 4 | 25.3% | 0.38 | 0.53 | 40.4% | 39.3% | 14.9% | 35.4%/28.8% | n/a (profitable_beyond_25.0x) | pass | 0.025 (unverified) | 0.47 |
| 62 | `cfg_51a4` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=8, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 37/57/65 | 159 | 53.1% | 8.9% | 0.81 | -14.6% | 140 | 1.44 | 13.5% | 83.4 | 10/10 | 0.90 | 0.72 | 0.09 | 5 | 36.0% | 0.32 | 0.51 | 51.1% | 49.3% | 33.3% | 46.4%/33.9% | n/a (profitable_beyond_25.0x) | pass | 0.013 (unverified) | 0.19 |
| 63 | `cfg_d5cb` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.5, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 33/148/0 | 181 | 29.3% | 5.3% | 1.07 | -6.6% | 138 | 1.70 | 3.2% | 91.3 | 10/10 | 0.70 | 0.36 | 0.71 | 5 | 19.7% | 0.31 | 0.37 | 28.6% | 27.9% | 20.1% | 26.8%/22.1% | 21.1 (interpolated) | pass | 0.037 (unverified) | 1.03 |
| 64 | `cfg_b3ff` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 55/131/0 | 186 | 32.2% | 5.7% | 1.16 | -5.1% | 170 | 1.76 | 3.2% | 93.9 | 12/12 | 0.83 | 0.58 | 0.58 | 5 | 20.0% | 0.32 | 0.38 | 31.0% | 30.6% | 23.9% | 29.2%/21.9% | 20.9 (interpolated) | pass | 0.047 (unverified) | 0.80 |
| 65 | `cfg_78ca` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 4/81/17 | 102 | 28.2% | 5.1% | 1.03 | -4.7% | 317 | 1.94 | 4.3% | 51.8 | 10/10 | 0.80 | 0.79 | 0.23 | 4 | 12.9% | 0.48 | 0.71 | 27.9% | 27.5% | 6.6% | 25.2%/19.8% | n/a (profitable_beyond_25.0x) | pass | 0.028 (unverified) | 0.90 |
| 66 | `cfg_3c6f` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=8, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 72/30/72 | 174 | 60.1% | 9.9% | 0.90 | -10.5% | 139 | 1.44 | 12.9% | 90.2 | 10/10 | 0.90 | 0.78 | 0.12 | 5 | 31.2% | 0.42 | 0.49 | 59.7% | 58.3% | 43.6% | 57.4%/44.4% | n/a (profitable_beyond_25.0x) | pass | 0.020 (unverified) | 0.31 |
| 67 | `cfg_26d7` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=8, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 13/74/35 | 122 | 33.8% | 6.0% | 0.84 | -4.9% | 205 | 1.58 | 6.9% | 62.3 | 11/11 | 0.91 | 0.84 | -0.01 | 5 | 12.8% | 0.57 | 0.58 | 33.6% | 33.0% | 21.1% | 30.1%/22.1% | n/a (profitable_beyond_25.0x) | pass | 0.007 (unverified) | 0.61 |
| 68 | `cfg_488c` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=8, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 25/62/35 | 122 | 32.0% | 5.7% | 0.81 | -4.9% | 205 | 1.56 | 6.7% | 61.7 | 12/12 | 0.92 | 0.81 | -0.01 | 5 | 12.1% | 0.58 | 0.62 | 31.3% | 31.1% | 20.3% | 28.7%/20.5% | n/a (profitable_beyond_25.0x) | pass | 0.006 (unverified) | 0.68 |
| 69 | `cfg_98ab` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=5, entry_z=-3.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 76/43/84 | 203 | 57.4% | 9.5% | 0.91 | -7.8% | 182 | 1.42 | 14.7% | 105.9 | 9/9 | 0.89 | 0.78 | 0.13 | 5 | 32.8% | 0.35 | 0.45 | 56.6% | 56.3% | 23.5% | 53.6%/41.5% | n/a (profitable_beyond_25.0x) | pass | 0.017 (unverified) | 0.55 |
| 70 | `cfg_cef5` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=5, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 76/47/87 | 210 | 65.8% | 10.6% | 0.87 | -10.2% | 164 | 1.42 | 16.1% | 110.8 | 9/9 | 0.89 | 0.66 | 0.21 | 5 | 45.2% | 0.31 | 0.46 | 64.0% | 61.7% | 23.7% | 60.6%/42.2% | n/a (profitable_beyond_25.0x) | pass | 0.016 (unverified) | 0.25 |
| 71 | `cfg_9aa3` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 13/91/18 | 122 | 26.8% | 4.9% | 0.92 | -3.4% | 198 | 1.64 | 5.1% | 62.4 | 11/11 | 1.00 | 0.66 | 0.26 | 5 | 15.8% | 0.41 | 0.74 | 25.4% | 24.3% | 8.8% | 25.6%/18.4% | n/a (profitable_beyond_25.0x) | pass | 0.012 (unverified) | 0.20 |
| 72 | `cfg_6564` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.5, exit_z=-1.25, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 28/65/12 | 105 | 26.4% | 4.8% | 0.96 | -6.8% | 342 | 1.77 | 4.3% | 54.0 | 10/10 | 0.90 | 0.50 | 0.46 | 4 | 15.6% | 0.41 | 0.63 | 26.3% | 25.9% | 5.5% | 24.3%/17.8% | n/a (profitable_beyond_25.0x) | pass | 0.019 (unverified) | 0.52 |
| 73 | `cfg_b73e` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=5, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 87/65/59 | 211 | 46.5% | 7.9% | 1.02 | -8.5% | 384 | 1.51 | 9.8% | 108.2 | 11/11 | 0.91 | 0.67 | 0.35 | 4 | 16.7% | 0.54 | 0.42 | 46.0% | 43.5% | 39.9% | 42.8%/31.0% | 24.9 (interpolated) | pass | 0.030 (unverified) | 0.60 |
| 74 | `cfg_bada` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.5, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 29/72/0 | 101 | 26.1% | 4.7% | 1.15 | -3.5% | 198 | 2.15 | 1.7% | 51.3 | 10/10 | 0.80 | 0.54 | 0.61 | 4 | 16.6% | 0.36 | 0.43 | 25.5% | 25.3% | 10.7% | 22.9%/17.5% | n/a (profitable_beyond_25.0x) | pass | 0.039 (unverified) | 0.97 |
| 75 | `cfg_d2a5` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-3.0, exit_z=-0.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 17/87/18 | 122 | 24.5% | 4.5% | 0.87 | -4.0% | 198 | 1.58 | 5.1% | 62.2 | 11/11 | 1.00 | 0.66 | 0.21 | 5 | 13.8% | 0.39 | 0.73 | 24.0% | 22.9% | 8.9% | 22.7%/18.2% | n/a (profitable_beyond_25.0x) | pass | 0.010 (unverified) | 0.19 |
| 76 | `cfg_4390` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 36/33/42 | 111 | 35.8% | 6.3% | 0.83 | -9.6% | 184 | 1.47 | 9.5% | 56.8 | 10/10 | 0.90 | 0.85 | -0.02 | 4 | 19.7% | 0.42 | 0.65 | 34.5% | 34.1% | 19.9% | 31.9%/24.3% | n/a (profitable_beyond_25.0x) | pass | 0.010 (unverified) | 0.49 |
| 77 | `cfg_e933` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=8, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 62/39/73 | 174 | 63.3% | 10.3% | 0.91 | -9.7% | 169 | 1.46 | 13.8% | 91.1 | 9/9 | 0.89 | 0.62 | 0.29 | 5 | 32.1% | 0.41 | 0.48 | 60.6% | 58.6% | 38.0% | 56.7%/47.1% | n/a (profitable_beyond_25.0x) | pass | 0.020 (unverified) | 0.15 |
| 78 | `cfg_21aa` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=10, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 25/52/36 | 113 | 35.4% | 6.3% | 0.77 | -8.1% | 421 | 1.59 | 6.2% | 58.5 | 12/12 | 1.00 | 0.62 | 0.16 | 5 | 18.5% | 0.42 | 0.52 | 34.9% | 35.1% | 18.3% | 33.4%/25.0% | n/a (profitable_beyond_25.0x) | pass | 0.008 (unverified) | 0.32 |
| 79 | `cfg_2a8c` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=5, entry_z=-3.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 65/52/86 | 203 | 54.8% | 9.1% | 0.89 | -7.5% | 230 | 1.42 | 15.5% | 104.4 | 8/8 | 0.88 | 0.71 | 0.17 | 4 | 34.5% | 0.37 | 0.46 | 53.8% | 51.7% | 12.0% | 48.2%/36.2% | n/a (profitable_beyond_25.0x) | pass | 0.015 (unverified) | 0.55 |
| 80 | `cfg_4c1b` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=8, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 33/81/50 | 164 | 43.8% | 7.5% | 0.92 | -7.5% | 322 | 1.49 | 9.1% | 83.2 | 11/11 | 0.73 | 0.81 | 0.11 | 4 | 7.6% | 0.81 | 0.60 | 43.0% | 42.7% | 16.8% | 42.7%/32.9% | n/a (profitable_beyond_25.0x) | pass | 0.015 (unverified) | 0.46 |
| 81 | `cfg_8130` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 43/39/52 | 134 | 48.3% | 8.2% | 0.94 | -8.3% | 384 | 1.57 | 11.0% | 70.3 | 10/10 | 0.90 | 0.76 | 0.18 | 5 | 25.2% | 0.41 | 0.53 | 48.3% | 47.9% | 22.3% | 43.2%/30.2% | n/a (profitable_beyond_25.0x) | pass | 0.021 (unverified) | 0.91 |
| 82 | `cfg_9ff3` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 58/43/70 | 171 | 51.1% | 8.6% | 0.85 | -8.3% | 216 | 1.44 | 14.0% | 89.1 | 9/9 | 0.89 | 0.77 | 0.08 | 5 | 27.3% | 0.43 | 0.52 | 50.7% | 50.5% | 22.2% | 45.3%/34.2% | n/a (profitable_beyond_25.0x) | pass | 0.015 (unverified) | 0.30 |
| 83 | `cfg_9edc` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=5, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 123/40/119 | 282 | 66.8% | 10.8% | 0.91 | -8.5% | 126 | 1.33 | 19.8% | 144.9 | 7/7 | 0.86 | 0.66 | 0.25 | 4 | 29.2% | 0.51 | 0.50 | 64.2% | 63.3% | 48.0% | 58.4%/44.5% | n/a (profitable_beyond_25.0x) | pass | 0.022 (unverified) | 0.60 |
| 84 | `cfg_76c6` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 25/95/43 | 163 | 44.8% | 7.7% | 0.87 | -7.9% | 284 | 1.59 | 9.5% | 83.9 | 10/10 | 0.80 | 0.77 | 0.10 | 5 | 26.4% | 0.41 | 0.47 | 43.4% | 41.9% | 15.0% | 39.3%/32.7% | n/a (profitable_beyond_25.0x) | pass | 0.015 (unverified) | 0.15 |
| 85 | `cfg_ebc0` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 9/82/12 | 103 | 23.7% | 4.4% | 0.89 | -6.6% | 601 | 1.69 | 4.3% | 52.6 | 11/11 | 0.91 | 0.57 | 0.32 | 4 | 14.0% | 0.41 | 0.69 | 23.5% | 23.1% | 6.8% | 22.4%/15.6% | n/a (profitable_beyond_25.0x) | pass | 0.014 (unverified) | 0.40 |
| 86 | `cfg_6aca` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=8, entry_z=-3.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 26/52/33 | 111 | 31.0% | 5.5% | 0.93 | -4.0% | 247 | 1.56 | 6.1% | 56.2 | 10/10 | 1.00 | 0.71 | 0.22 | 5 | 16.2% | 0.44 | 0.59 | 30.3% | 30.2% | 19.5% | 28.8%/19.9% | n/a (profitable_beyond_25.0x) | pass | 0.018 (unverified) | 0.45 |
| 87 | `cfg_5ec4` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=5, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 133/32/117 | 282 | 59.7% | 9.8% | 0.87 | -8.7% | 113 | 1.31 | 18.3% | 143.4 | 8/8 | 0.88 | 0.64 | 0.23 | 4 | 26.7% | 0.51 | 0.56 | 59.7% | 57.6% | 43.7% | 54.5%/39.9% | 23.6 (interpolated) | pass | 0.017 (unverified) | 0.76 |
| 88 | `cfg_f612` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=5, entry_z=-2.5, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 97/55/60 | 212 | 42.4% | 7.3% | 0.94 | -8.2% | 384 | 1.46 | 9.5% | 108.6 | 10/10 | 0.90 | 0.61 | 0.33 | 4 | 11.7% | 0.63 | 0.48 | 41.3% | 40.1% | 31.1% | 36.2%/27.0% | 23.4 (interpolated) | pass | 0.020 (unverified) | 0.64 |
| 89 | `cfg_fb90` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=8, entry_z=-3.5, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 29/49/33 | 111 | 30.2% | 5.4% | 0.92 | -4.3% | 247 | 1.54 | 6.1% | 56.3 | 9/9 | 1.00 | 0.65 | 0.26 | 5 | 15.2% | 0.46 | 0.60 | 30.0% | 29.9% | 18.4% | 27.3%/17.3% | n/a (profitable_beyond_25.0x) | pass | 0.016 (unverified) | 0.51 |
| 90 | `cfg_3e52` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 64/59/42 | 165 | 38.4% | 6.7% | 0.83 | -7.6% | 265 | 1.53 | 8.7% | 84.2 | 11/11 | 0.91 | 0.77 | 0.05 | 4 | 25.1% | 0.35 | 0.46 | 36.7% | 36.5% | 10.3% | 33.1%/27.0% | n/a (profitable_beyond_25.0x) | pass | 0.013 (unverified) | 0.27 |
| 91 | `cfg_b42e` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=5, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 103/46/104 | 253 | 58.5% | 9.7% | 0.85 | -9.5% | 186 | 1.33 | 17.4% | 128.4 | 10/10 | 0.90 | 0.63 | 0.22 | 5 | 22.4% | 0.56 | 0.51 | 56.6% | 56.0% | 39.0% | 56.7%/39.8% | n/a (profitable_beyond_25.0x) | pass | 0.014 (unverified) | 0.38 |
| 92 | `cfg_ea9b` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=5, entry_z=-2.5, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 87/65/57 | 209 | 48.3% | 8.2% | 0.88 | -10.1% | 527 | 1.46 | 9.8% | 108.5 | 10/10 | 0.90 | 0.74 | 0.14 | 4 | 10.3% | 0.70 | 0.51 | 47.9% | 46.6% | 22.7% | 46.7%/37.2% | n/a (profitable_beyond_25.0x) | pass | 0.016 (unverified) | 0.57 |
| 93 | `cfg_091a` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 15/62/36 | 113 | 36.0% | 6.3% | 0.78 | -8.1% | 421 | 1.60 | 6.3% | 58.7 | 12/12 | 1.00 | 0.71 | 0.07 | 5 | 19.9% | 0.39 | 0.52 | 35.5% | 35.3% | 23.3% | 35.0%/27.4% | n/a (profitable_beyond_25.0x) | pass | 0.008 (unverified) | 0.28 |
| 94 | `cfg_4541` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=5, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 110/53/62 | 225 | 51.2% | 8.6% | 1.01 | -9.5% | 533 | 1.52 | 10.0% | 116.0 | 9/9 | 0.89 | 0.70 | 0.31 | 4 | 13.0% | 0.64 | 0.47 | 50.4% | 49.8% | 32.9% | 45.2%/33.2% | n/a (profitable_beyond_25.0x) | pass | 0.029 (unverified) | 0.56 |
| 95 | `cfg_34a7` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 57/24/52 | 133 | 38.1% | 6.7% | 0.83 | -8.3% | 165 | 1.45 | 9.9% | 68.1 | 8/8 | 0.88 | 0.62 | 0.21 | 5 | 26.4% | 0.25 | 0.55 | 37.6% | 37.8% | 15.1% | 36.6%/29.3% | n/a (profitable_beyond_25.0x) | pass | 0.013 (unverified) | 0.71 |
| 96 | `cfg_c89b` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-3.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 43/21/43 | 107 | 31.3% | 5.6% | 0.79 | -7.4% | 197 | 1.44 | 8.1% | 54.6 | 10/10 | 0.90 | 0.78 | 0.01 | 5 | 21.0% | 0.31 | 0.69 | 30.3% | 29.8% | 16.8% | 27.5%/19.8% | n/a (profitable_beyond_25.0x) | pass | 0.009 (unverified) | 0.08 |
| 97 | `cfg_2d0e` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=8, entry_z=-3.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 45/37/56 | 138 | 42.9% | 7.4% | 0.78 | -8.3% | 250 | 1.44 | 11.3% | 70.9 | 10/10 | 0.90 | 0.77 | 0.02 | 5 | 21.0% | 0.44 | 0.55 | 41.9% | 41.7% | 34.1% | 37.7%/28.9% | n/a (profitable_beyond_25.0x) | pass | 0.010 (unverified) | -0.11 |
| 98 | `cfg_bb5a` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 66/42/81 | 189 | 45.9% | 7.9% | 0.76 | -11.5% | 234 | 1.35 | 14.5% | 98.7 | 10/10 | 0.90 | 0.62 | 0.15 | 5 | 24.2% | 0.46 | 0.55 | 44.4% | 41.7% | 38.0% | 42.2%/33.2% | n/a (profitable_beyond_25.0x) | pass | 0.009 (unverified) | 0.48 |
| 99 | `cfg_4d88` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 34/71/0 | 105 | 21.4% | 4.0% | 0.92 | -4.6% | 198 | 1.75 | 1.8% | 52.8 | 13/13 | 0.85 | 0.67 | 0.26 | 5 | 15.1% | 0.29 | 0.52 | 21.0% | 20.7% | 3.8% | 18.0%/13.0% | n/a (profitable_beyond_25.0x) | pass | 0.013 (unverified) | 0.73 |
| 100 | `cfg_2d2f` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=8, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 64/31/64 | 159 | 39.1% | 6.8% | 0.80 | -9.1% | 185 | 1.36 | 12.0% | 82.4 | 11/11 | 0.91 | 0.74 | 0.06 | 5 | 27.8% | 0.29 | 0.54 | 37.9% | 37.5% | 19.5% | 36.6%/27.4% | n/a (profitable_beyond_25.0x) | pass | 0.011 (unverified) | 0.25 |
| 101 | `cfg_7648` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 20/59/29 | 108 | 35.2% | 6.2% | 0.96 | -5.1% | 166 | 1.72 | 6.1% | 55.3 | 11/11 | 0.91 | 0.69 | 0.27 | 5 | 15.9% | 0.49 | 0.55 | 34.2% | 34.2% | 11.5% | 30.1%/21.4% | n/a (profitable_beyond_25.0x) | pass | 0.019 (unverified) | 0.99 |
| 102 | `cfg_ad33` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=5, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 76/25/70 | 171 | 45.2% | 7.8% | 0.84 | -10.6% | 186 | 1.42 | 11.8% | 89.5 | 8/8 | 0.88 | 0.67 | 0.17 | 5 | 27.9% | 0.37 | 0.51 | 44.3% | 42.6% | 13.2% | 40.3%/31.1% | n/a (profitable_beyond_25.0x) | pass | 0.011 (unverified) | 0.69 |
| 103 | `cfg_7e8f` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=5, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 85/50/93 | 228 | 59.9% | 9.8% | 0.86 | -9.4% | 99 | 1.37 | 16.7% | 118.9 | 10/10 | 0.90 | 0.69 | 0.16 | 5 | 36.5% | 0.32 | 0.46 | 58.4% | 57.7% | 24.6% | 55.3%/40.6% | n/a (profitable_beyond_25.0x) | pass | 0.015 (unverified) | 0.51 |
| 104 | `cfg_9b31` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 158/262/0 | 420 | 37.3% | 6.6% | 0.93 | -6.1% | 197 | 1.36 | 6.8% | 212.4 | 10/10 | 0.90 | 0.59 | 0.34 | 4 | 21.1% | 0.39 | 0.45 | 36.5% | 32.2% | 6.8% | 33.6%/25.1% | 11.0 (interpolated) | pass | 0.018 (unverified) | 0.14 |
| 105 | `cfg_9862` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=5, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 91/43/100 | 234 | 57.1% | 9.5% | 0.83 | -11.1% | 186 | 1.34 | 16.8% | 121.9 | 8/8 | 0.88 | 0.65 | 0.19 | 5 | 33.3% | 0.34 | 0.48 | 54.9% | 54.5% | 46.9% | 52.3%/40.2% | n/a (profitable_beyond_25.0x) | pass | 0.012 (unverified) | 0.35 |
| 106 | `cfg_e741` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.5, exit_z=-1.25, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 67/10/37 | 114 | 38.1% | 6.7% | 1.00 | -8.8% | 168 | 1.59 | 7.3% | 58.9 | 10/10 | 0.90 | 0.59 | 0.40 | 5 | 24.9% | 0.31 | 0.56 | 37.6% | 37.0% | 12.4% | 34.4%/27.4% | n/a (profitable_beyond_25.0x) | pass | 0.030 (unverified) | 0.58 |
| 107 | `cfg_d849` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=5, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 96/51/105 | 252 | 64.0% | 10.4% | 0.88 | -8.0% | 194 | 1.35 | 18.2% | 128.4 | 10/10 | 0.90 | 0.63 | 0.25 | 5 | 30.4% | 0.46 | 0.49 | 60.5% | 59.9% | 44.7% | 60.2%/49.3% | n/a (profitable_beyond_25.0x) | pass | 0.016 (unverified) | 0.59 |
| 108 | `cfg_c58e` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=5, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 92/30/81 | 203 | 57.7% | 9.5% | 0.84 | -14.4% | 218 | 1.38 | 13.0% | 105.1 | 10/10 | 0.90 | 0.70 | 0.13 | 5 | 27.5% | 0.45 | 0.49 | 56.6% | 56.3% | 27.1% | 55.6%/41.5% | n/a (profitable_beyond_25.0x) | pass | 0.013 (unverified) | 0.27 |
| 109 | `cfg_7030` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 12/66/30 | 108 | 35.7% | 6.3% | 0.96 | -5.0% | 241 | 1.70 | 6.2% | 55.4 | 10/10 | 0.90 | 0.58 | 0.38 | 5 | 14.4% | 0.54 | 0.59 | 35.2% | 34.9% | 14.8% | 31.2%/21.3% | n/a (profitable_beyond_25.0x) | pass | 0.018 (unverified) | 1.04 |
| 110 | `cfg_b8f1` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=5, entry_z=-3.0, exit_z=-1.25, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 100/25/80 | 205 | 51.3% | 8.6% | 0.79 | -13.9% | 218 | 1.35 | 12.6% | 105.4 | 9/9 | 0.89 | 0.61 | 0.17 | 4 | 24.6% | 0.47 | 0.54 | 50.5% | 50.1% | 24.0% | 50.2%/35.6% | n/a (profitable_beyond_25.0x) | pass | 0.010 (unverified) | 0.19 |
| 111 | `cfg_4d0d` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 20/81/0 | 101 | 24.0% | 4.4% | 1.11 | -4.1% | 198 | 2.03 | 1.8% | 51.2 | 11/11 | 0.82 | 0.52 | 0.59 | 5 | 16.1% | 0.33 | 0.44 | 23.7% | 22.9% | 9.6% | 20.4%/15.5% | n/a (profitable_beyond_25.0x) | pass | 0.036 (unverified) | 1.03 |
| 112 | `cfg_1d41` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=5, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 44/145/0 | 189 | 36.2% | 6.4% | 0.94 | -10.3% | 545 | 1.58 | 8.2% | 96.3 | 8/8 | 0.88 | 0.75 | 0.19 | 4 | 14.7% | 0.49 | 0.50 | 35.7% | 35.7% | 19.5% | 34.9%/23.7% | 24.3 (interpolated) | pass | 0.018 (unverified) | 0.29 |
| 113 | `cfg_702b` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 41/145/0 | 186 | 30.0% | 5.4% | 1.09 | -5.3% | 170 | 1.72 | 3.3% | 93.3 | 13/13 | 0.85 | 0.58 | 0.50 | 5 | 18.3% | 0.33 | 0.41 | 29.0% | 28.4% | 19.7% | 26.2%/20.1% | 19.3 (interpolated) | pass | 0.033 (unverified) | 0.91 |
| 114 | `cfg_352d` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 44/19/40 | 103 | 43.1% | 7.4% | 0.87 | -8.5% | 117 | 1.63 | 7.6% | 53.2 | 10/10 | 0.90 | 0.78 | 0.09 | 5 | 27.1% | 0.37 | 0.51 | 41.9% | 41.9% | 14.9% | 38.4%/31.4% | n/a (profitable_beyond_25.0x) | pass | 0.017 (unverified) | 0.34 |
| 115 | `cfg_f0ee` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=8, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 42/38/34 | 114 | 24.6% | 4.5% | 0.81 | -5.0% | 205 | 1.50 | 5.9% | 57.5 | 12/12 | 0.92 | 0.75 | 0.06 | 4 | 14.8% | 0.40 | 0.66 | 24.5% | 24.4% | 1.8% | 22.3%/15.1% | n/a (profitable_beyond_25.0x) | pass | 0.009 (unverified) | 0.30 |
| 116 | `cfg_eab5` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 28/90/46 | 164 | 36.6% | 6.4% | 0.84 | -7.1% | 317 | 1.47 | 9.2% | 82.9 | 12/12 | 0.92 | 0.71 | 0.13 | 4 | 14.9% | 0.54 | 0.55 | 37.4% | 35.6% | 15.5% | 36.1%/27.9% | n/a (profitable_beyond_25.0x) | pass | 0.013 (unverified) | 0.63 |
| 117 | `cfg_2637` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=5, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 84/71/65 | 220 | 41.2% | 7.2% | 0.88 | -10.5% | 541 | 1.44 | 10.3% | 113.0 | 9/9 | 0.89 | 0.71 | 0.17 | 4 | 7.7% | 0.71 | 0.49 | 39.6% | 38.7% | 38.0% | 37.8%/28.2% | 22.5 (interpolated) | pass | 0.014 (unverified) | 0.63 |
| 118 | `cfg_2f18` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 69/35/67 | 171 | 46.0% | 7.9% | 0.83 | -7.9% | 190 | 1.42 | 13.2% | 88.7 | 10/10 | 0.90 | 0.75 | 0.08 | 5 | 20.5% | 0.52 | 0.50 | 45.8% | 45.3% | 12.8% | 41.5%/30.5% | n/a (profitable_beyond_25.0x) | pass | 0.014 (unverified) | 0.32 |
| 119 | `cfg_9c5a` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 51/32/52 | 135 | 46.4% | 7.9% | 0.97 | -6.8% | 162 | 1.56 | 10.4% | 70.0 | 10/10 | 0.90 | 0.75 | 0.22 | 5 | 31.9% | 0.30 | 0.50 | 45.9% | 45.1% | 23.2% | 42.3%/30.6% | n/a (profitable_beyond_25.0x) | pass | 0.026 (unverified) | 0.84 |
| 120 | `cfg_7217` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-3.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 48/16/43 | 107 | 26.9% | 4.9% | 0.78 | -8.0% | 185 | 1.39 | 7.6% | 54.8 | 10/10 | 0.90 | 0.74 | 0.04 | 5 | 15.1% | 0.42 | 0.72 | 26.0% | 25.3% | 15.4% | 24.0%/15.8% | n/a (profitable_beyond_25.0x) | pass | 0.010 (unverified) | 0.21 |
| 121 | `cfg_2334` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=8, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 35/45/34 | 114 | 23.9% | 4.4% | 0.76 | -5.1% | 205 | 1.47 | 6.0% | 57.6 | 12/12 | 0.92 | 0.71 | 0.05 | 4 | 12.9% | 0.42 | 0.73 | 23.5% | 22.7% | 1.8% | 21.9%/15.4% | n/a (profitable_beyond_25.0x) | pass | 0.006 (unverified) | 0.27 |
| 122 | `cfg_064a` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 7/174/0 | 181 | 24.8% | 4.5% | 0.89 | -7.9% | 270 | 1.53 | 3.3% | 91.7 | 10/10 | 0.60 | 0.22 | 0.68 | 4 | 14.9% | 0.39 | 0.44 | 23.7% | 22.9% | 17.1% | 21.7%/17.2% | 18.7 (interpolated) | pass | 0.014 (unverified) | 0.99 |
| 123 | `cfg_6cca` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=5, entry_z=-2.0, exit_z=0.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 31/158/0 | 189 | 38.3% | 6.7% | 0.96 | -11.8% | 545 | 1.60 | 8.4% | 96.0 | 7/7 | 0.86 | 0.76 | 0.20 | 4 | 14.9% | 0.49 | 0.51 | 37.3% | 37.2% | 22.9% | 36.0%/25.8% | 24.9 (interpolated) | pass | 0.019 (unverified) | 0.36 |
| 124 | `cfg_6f20` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=5, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 34/110/63 | 207 | 37.4% | 6.6% | 0.81 | -11.2% | 531 | 1.40 | 10.9% | 104.5 | 10/10 | 0.90 | 0.63 | 0.18 | 4 | 14.8% | 0.50 | 0.62 | 35.8% | 35.0% | 56.1% | 35.8%/25.1% | 21.4 (interpolated) | pass | 0.010 (unverified) | 0.53 |
| 125 | `cfg_94af` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=5, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 77/73/57 | 207 | 43.3% | 7.5% | 0.81 | -9.5% | 527 | 1.43 | 10.0% | 106.6 | 11/11 | 0.91 | 0.72 | 0.09 | 4 | 11.4% | 0.65 | 0.58 | 42.9% | 42.8% | 29.4% | 43.3%/32.8% | n/a (profitable_beyond_25.0x) | pass | 0.011 (unverified) | 0.59 |
| 126 | `cfg_c580` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=10, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 30/59/39 | 128 | 35.5% | 6.3% | 0.80 | -9.1% | 341 | 1.51 | 7.1% | 65.8 | 11/11 | 0.91 | 0.68 | 0.12 | 5 | 18.2% | 0.44 | 0.57 | 34.7% | 34.4% | 25.2% | 34.3%/25.4% | n/a (profitable_beyond_25.0x) | pass | 0.011 (unverified) | 0.11 |
| 127 | `cfg_2b5f` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 40/26/43 | 109 | 32.1% | 5.7% | 0.83 | -6.8% | 184 | 1.54 | 8.3% | 55.7 | 10/10 | 0.90 | 0.78 | 0.05 | 5 | 17.4% | 0.41 | 0.59 | 31.7% | 31.6% | 7.9% | 26.7%/18.9% | n/a (profitable_beyond_25.0x) | pass | 0.011 (unverified) | 0.84 |
| 128 | `cfg_ea18` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 9/83/15 | 107 | 26.0% | 4.7% | 0.85 | -6.5% | 343 | 1.70 | 4.5% | 55.0 | 9/9 | 0.89 | 0.65 | 0.20 | 4 | 13.2% | 0.49 | 0.69 | 25.1% | 25.0% | 22.7% | 24.1%/19.0% | n/a (profitable_beyond_25.0x) | pass | 0.010 (unverified) | 0.48 |
| 129 | `cfg_8ed5` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 160/197/0 | 357 | 36.0% | 6.4% | 0.96 | -10.3% | 263 | 1.40 | 5.8% | 179.7 | 11/11 | 0.91 | 0.48 | 0.49 | 4 | 22.9% | 0.33 | 0.41 | 32.9% | 29.8% | 35.2% | 29.6%/23.0% | 12.6 (interpolated) | pass | 0.022 (unverified) | 0.88 |
| 130 | `cfg_2dc3` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 40/78/46 | 164 | 33.6% | 6.0% | 0.80 | -7.5% | 453 | 1.44 | 9.1% | 83.2 | 12/12 | 0.92 | 0.68 | 0.12 | 4 | 11.7% | 0.60 | 0.56 | 33.1% | 32.9% | 11.1% | 31.1%/23.3% | n/a (profitable_beyond_25.0x) | pass | 0.009 (unverified) | 0.62 |
| 131 | `cfg_bea6` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=5, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 57/33/65 | 155 | 39.8% | 6.9% | 0.76 | -7.9% | 164 | 1.41 | 11.5% | 80.3 | 9/9 | 0.89 | 0.78 | -0.02 | 4 | 23.6% | 0.37 | 0.54 | 37.9% | 37.3% | 15.4% | 36.7%/28.5% | n/a (profitable_beyond_25.0x) | pass | 0.006 (unverified) | 0.48 |
| 132 | `cfg_aaf9` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 47/16/40 | 103 | 38.3% | 6.7% | 0.83 | -6.1% | 118 | 1.58 | 7.1% | 52.8 | 10/10 | 0.90 | 0.76 | 0.06 | 5 | 25.8% | 0.33 | 0.56 | 37.9% | 38.1% | 15.9% | 34.2%/28.2% | n/a (profitable_beyond_25.0x) | pass | 0.013 (unverified) | 0.31 |
| 133 | `cfg_6646` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=8, entry_z=-3.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 12/82/42 | 136 | 33.1% | 5.9% | 0.83 | -4.1% | 218 | 1.45 | 7.9% | 69.7 | 10/10 | 0.90 | 0.65 | 0.18 | 5 | 16.7% | 0.45 | 0.61 | 32.7% | 32.6% | 12.4% | 29.8%/21.6% | n/a (profitable_beyond_25.0x) | pass | 0.010 (unverified) | 0.52 |
| 134 | `cfg_1484` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=5, entry_z=-3.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 74/59/0 | 133 | 40.8% | 7.1% | 0.82 | -7.9% | 216 | 1.54 | 13.2% | 67.5 | 7/7 | 0.71 | 0.55 | 0.28 | 4 | 27.6% | 0.31 | 0.45 | 40.3% | 40.2% | 45.9% | 36.3%/28.9% | n/a (profitable_beyond_25.0x) | pass | 0.012 (unverified) | 0.42 |
| 135 | `cfg_590f` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=10, entry_z=-3.5, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 32/49/31 | 112 | 37.6% | 6.6% | 0.81 | -11.1% | 142 | 1.55 | 6.2% | 57.8 | 9/9 | 0.89 | 0.62 | 0.19 | 5 | 22.4% | 0.33 | 0.55 | 37.4% | 36.9% | 12.7% | 33.9%/25.7% | n/a (profitable_beyond_25.0x) | pass | 0.013 (unverified) | 0.47 |
| 136 | `cfg_c73b` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=5, entry_z=-3.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 55/50/0 | 105 | 50.6% | 8.5% | 0.93 | -7.1% | 186 | 1.72 | 10.7% | 54.8 | 8/8 | 0.75 | 0.66 | 0.27 | 4 | 31.1% | 0.37 | 0.49 | 51.6% | 50.4% | 50.0% | 45.8%/33.6% | n/a (profitable_beyond_25.0x) | pass | 0.021 (unverified) | 1.05 |
| 137 | `cfg_3786` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=8, entry_z=-3.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 21/61/62 | 144 | 52.5% | 8.8% | 0.82 | -11.3% | 384 | 1.47 | 12.8% | 74.6 | 8/8 | 0.88 | 0.69 | 0.13 | 5 | 29.3% | 0.44 | 0.57 | 50.7% | 48.5% | 43.0% | 43.0%/31.1% | n/a (profitable_beyond_25.0x) | pass | 0.013 (unverified) | 0.39 |
| 138 | `cfg_133c` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=8, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 16/79/41 | 136 | 35.5% | 6.3% | 0.84 | -6.6% | 313 | 1.47 | 7.7% | 69.9 | 12/12 | 0.75 | 0.54 | 0.30 | 4 | 8.3% | 0.75 | 0.66 | 35.3% | 35.3% | 17.0% | 34.7%/25.4% | n/a (profitable_beyond_25.0x) | pass | 0.009 (unverified) | 0.36 |
| 139 | `cfg_485f` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=8, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 54/57/42 | 153 | 30.6% | 5.5% | 0.80 | -5.4% | 209 | 1.43 | 8.2% | 77.1 | 12/12 | 0.83 | 0.68 | 0.12 | 5 | 17.9% | 0.39 | 0.59 | 29.2% | 28.6% | 13.8% | 26.6%/18.4% | 24.4 (interpolated) | pass | 0.010 (unverified) | 0.56 |
| 140 | `cfg_e017` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=8, entry_z=-3.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 18/77/41 | 136 | 35.4% | 6.3% | 0.88 | -4.1% | 218 | 1.50 | 7.8% | 69.6 | 10/10 | 0.90 | 0.65 | 0.23 | 5 | 19.9% | 0.39 | 0.57 | 34.5% | 33.6% | 8.2% | 31.4%/21.7% | n/a (profitable_beyond_25.0x) | pass | 0.013 (unverified) | 0.55 |
| 141 | `cfg_31ed` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=8, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 44/61/0 | 105 | 49.2% | 8.3% | 0.94 | -7.6% | 301 | 1.76 | 11.0% | 54.2 | 9/9 | 0.89 | 0.64 | 0.30 | 5 | 21.4% | 0.49 | 0.44 | 49.3% | 47.6% | 36.2% | 47.4%/33.7% | n/a (profitable_beyond_25.0x) | pass | 0.026 (unverified) | 0.14 |
| 142 | `cfg_ed82` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=8, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 11/84/41 | 136 | 37.0% | 6.5% | 0.87 | -6.5% | 313 | 1.49 | 7.8% | 69.8 | 11/11 | 0.73 | 0.42 | 0.45 | 4 | 8.9% | 0.74 | 0.64 | 36.3% | 35.9% | 17.9% | 35.4%/24.1% | n/a (profitable_beyond_25.0x) | pass | 0.010 (unverified) | 0.22 |
| 143 | `cfg_3e55` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 52/9/39 | 100 | 40.7% | 7.1% | 0.99 | -7.0% | 201 | 1.62 | 6.1% | 52.1 | 10/10 | 1.00 | 0.38 | 0.61 | 4 | 21.1% | 0.41 | 0.53 | 40.5% | 40.0% | 23.9% | 37.1%/29.5% | n/a (profitable_beyond_25.0x) | pass | 0.032 (unverified) | 0.58 |
| 144 | `cfg_c2d9` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 39/223/0 | 262 | 25.1% | 4.6% | 0.77 | -8.6% | 437 | 1.37 | 4.6% | 131.0 | 12/12 | 0.75 | 0.45 | 0.31 | 3 | 12.0% | 0.49 | 0.55 | 23.4% | 22.8% | 26.1% | 20.7%/15.8% | 12.4 (interpolated) | pass | 0.006 (unverified) | 0.80 |
| 145 | `cfg_24e6` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 41/64/0 | 105 | 18.7% | 3.5% | 0.84 | -4.6% | 198 | 1.65 | 1.7% | 53.1 | 12/12 | 0.83 | 0.65 | 0.18 | 5 | 13.5% | 0.27 | 0.56 | 18.2% | 18.1% | 5.7% | 15.3%/10.9% | 24.5 (interpolated) | pass | 0.008 (unverified) | 0.72 |
| 146 | `cfg_1752` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=5, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 97/42/0 | 139 | 50.8% | 8.6% | 0.90 | -8.7% | 162 | 1.59 | 11.6% | 72.8 | 10/10 | 0.90 | 0.74 | 0.16 | 5 | 25.8% | 0.42 | 0.45 | 50.1% | 50.1% | 26.6% | 46.0%/36.9% | n/a (profitable_beyond_25.0x) | pass | 0.020 (unverified) | 0.61 |
| 147 | `cfg_eb2b` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=5, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 57/77/0 | 134 | 49.4% | 8.4% | 0.81 | -9.4% | 366 | 1.51 | 14.1% | 70.7 | 9/9 | 0.89 | 0.61 | 0.20 | 4 | 27.8% | 0.41 | 0.56 | 49.6% | 49.3% | 21.4% | 41.4%/29.6% | n/a (profitable_beyond_25.0x) | pass | 0.011 (unverified) | 0.38 |
| 148 | `cfg_e465` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=5, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 120/16/85 | 221 | 46.2% | 7.9% | 0.83 | -11.0% | 249 | 1.35 | 12.7% | 113.0 | 8/8 | 0.88 | 0.77 | 0.06 | 3 | 9.9% | 0.73 | 0.53 | 44.9% | 44.5% | 38.7% | 40.2%/30.2% | 24.6 (interpolated) | pass | 0.011 (unverified) | 0.83 |
| 149 | `cfg_b0ac` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 45/219/0 | 264 | 29.3% | 5.3% | 0.88 | -7.8% | 372 | 1.45 | 4.7% | 131.6 | 11/11 | 0.73 | 0.42 | 0.46 | 3 | 13.6% | 0.54 | 0.45 | 28.2% | 27.9% | 32.3% | 25.9%/19.1% | 14.6 (interpolated) | pass | 0.013 (unverified) | 0.92 |
| 150 | `cfg_5181` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 32/33/44 | 109 | 32.1% | 5.7% | 0.77 | -8.4% | 386 | 1.50 | 8.8% | 56.5 | 9/9 | 0.89 | 0.58 | 0.20 | 5 | 14.4% | 0.49 | 0.64 | 31.7% | 31.5% | 10.5% | 29.2%/21.2% | n/a (profitable_beyond_25.0x) | pass | 0.008 (unverified) | 0.88 |
| 151 | `cfg_808b` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=5, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 67/45/0 | 112 | 51.8% | 8.7% | 0.97 | -9.7% | 378 | 1.73 | 11.0% | 58.9 | 8/8 | 0.75 | 0.69 | 0.27 | 4 | 29.3% | 0.41 | 0.46 | 51.3% | 48.9% | 44.0% | 44.9%/34.9% | n/a (profitable_beyond_25.0x) | pass | 0.026 (unverified) | 0.87 |
| 152 | `cfg_448a` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 75/10/48 | 133 | 34.7% | 6.1% | 0.83 | -8.6% | 200 | 1.50 | 8.4% | 67.2 | 9/9 | 0.78 | 0.39 | 0.44 | 5 | 19.6% | 0.43 | 0.54 | 34.1% | 33.5% | 9.3% | 29.9%/23.7% | n/a (profitable_beyond_25.0x) | pass | 0.014 (unverified) | 0.77 |
| 153 | `cfg_e998` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=8, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 72/3/36 | 111 | 26.3% | 4.8% | 0.82 | -6.9% | 324 | 1.52 | 5.6% | 55.7 | 9/9 | 0.89 | 0.60 | 0.22 | 5 | 11.8% | 0.55 | 0.60 | 26.3% | 25.9% | 7.3% | 24.7%/17.7% | n/a (profitable_beyond_25.0x) | pass | 0.011 (unverified) | -0.16 |
| 154 | `cfg_9f87` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=5, entry_z=-2.0, exit_z=-1.25, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 163/15/107 | 285 | 48.0% | 8.2% | 0.81 | -9.1% | 187 | 1.30 | 15.3% | 144.5 | 7/7 | 0.86 | 0.54 | 0.28 | 4 | 15.1% | 0.64 | 0.53 | 46.5% | 43.7% | 48.9% | 45.9%/34.5% | 20.4 (interpolated) | pass | 0.013 (unverified) | 0.29 |
| 155 | `cfg_c00f` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.5, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 33/72/0 | 105 | 19.0% | 3.5% | 0.85 | -5.3% | 198 | 1.67 | 1.8% | 52.2 | 11/11 | 0.82 | 0.41 | 0.44 | 5 | 13.4% | 0.28 | 0.60 | 18.8% | 18.5% | 7.9% | 16.7%/12.0% | 24.8 (interpolated) | pass | 0.009 (unverified) | 1.14 |
| 156 | `cfg_d3f9` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.0, exit_z=-1.25, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 109/11/62 | 182 | 45.0% | 7.7% | 0.89 | -6.9% | 248 | 1.47 | 10.7% | 94.0 | 9/9 | 0.89 | 0.58 | 0.31 | 4 | 25.7% | 0.41 | 0.48 | 43.7% | 41.5% | 15.1% | 36.3%/31.0% | n/a (profitable_beyond_25.0x) | pass | 0.019 (unverified) | 0.27 |
| 157 | `cfg_6897` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=8, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 21/53/33 | 107 | 23.6% | 4.3% | 0.76 | -5.1% | 308 | 1.49 | 5.9% | 54.3 | 10/10 | 0.90 | 0.57 | 0.19 | 5 | 15.2% | 0.34 | 0.77 | 23.1% | 22.7% | 7.9% | 22.9%/16.1% | n/a (profitable_beyond_25.0x) | pass | 0.006 (unverified) | 0.32 |
| 158 | `cfg_ba7c` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 13/79/15 | 107 | 23.5% | 4.3% | 0.79 | -6.4% | 343 | 1.64 | 4.4% | 54.7 | 10/10 | 0.90 | 0.65 | 0.15 | 4 | 12.0% | 0.49 | 0.75 | 23.2% | 23.0% | 21.7% | 21.0%/14.4% | n/a (profitable_beyond_25.0x) | pass | 0.007 (unverified) | 0.45 |
| 159 | `cfg_ce78` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=5, entry_z=-3.0, exit_z=-1.25, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 102/39/0 | 141 | 43.1% | 7.4% | 0.82 | -8.8% | 353 | 1.53 | 11.2% | 72.5 | 9/9 | 0.89 | 0.64 | 0.17 | 4 | 18.0% | 0.52 | 0.49 | 42.0% | 42.0% | 18.3% | 37.9%/29.5% | n/a (profitable_beyond_25.0x) | pass | 0.012 (unverified) | 0.73 |
| 160 | `cfg_f328` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=5, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 88/70/0 | 158 | 60.9% | 10.0% | 0.93 | -10.4% | 412 | 1.55 | 15.4% | 83.0 | 7/7 | 0.86 | 0.75 | 0.18 | 4 | 24.4% | 0.48 | 0.50 | 58.3% | 56.4% | 47.9% | 50.2%/41.0% | n/a (profitable_beyond_25.0x) | pass | 0.020 (unverified) | 0.39 |
| 161 | `cfg_07f8` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=5, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 71/59/98 | 228 | 50.6% | 8.5% | 0.76 | -8.9% | 152 | 1.32 | 17.6% | 117.8 | 9/9 | 0.89 | 0.64 | 0.12 | 5 | 29.5% | 0.38 | 0.53 | 50.1% | 50.0% | 11.9% | 44.9%/33.6% | n/a (profitable_beyond_25.0x) | pass | 0.008 (unverified) | 0.50 |
| 162 | `cfg_56e3` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 125/292/0 | 417 | 31.1% | 5.6% | 0.76 | -7.4% | 198 | 1.30 | 7.0% | 210.4 | 11/11 | 0.91 | 0.47 | 0.29 | 4 | 18.6% | 0.34 | 0.50 | 29.2% | 27.9% | 8.9% | 29.9%/22.0% | 10.2 (interpolated) | pass | 0.011 (unverified) | 0.07 |
| 163 | `cfg_bf51` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=5, entry_z=-3.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 26/114/62 | 202 | 37.5% | 6.6% | 0.81 | -6.6% | 200 | 1.41 | 10.8% | 102.2 | 9/9 | 0.89 | 0.45 | 0.36 | 4 | 20.1% | 0.47 | 0.56 | 36.9% | 35.9% | 37.3% | 35.4%/25.6% | 22.0 (interpolated) | pass | 0.011 (unverified) | 0.60 |
| 164 | `cfg_aa57` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=5, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 135/11/83 | 229 | 41.8% | 7.2% | 0.80 | -10.1% | 388 | 1.34 | 11.8% | 117.1 | 8/8 | 0.88 | 0.71 | 0.09 | 4 | 9.5% | 0.70 | 0.59 | 40.1% | 38.2% | 31.0% | 35.5%/26.8% | 22.1 (interpolated) | pass | 0.009 (unverified) | 0.52 |
| 165 | `cfg_e9cc` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 125/228/0 | 353 | 31.2% | 5.6% | 0.84 | -11.5% | 420 | 1.34 | 6.0% | 175.3 | 12/12 | 0.83 | 0.41 | 0.44 | 4 | 16.5% | 0.44 | 0.48 | 30.4% | 29.3% | 19.2% | 28.1%/18.4% | 12.2 (interpolated) | pass | 0.011 (unverified) | 0.51 |
| 166 | `cfg_f012` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=5, entry_z=-2.0, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 116/74/80 | 270 | 41.8% | 7.2% | 0.78 | -10.6% | 398 | 1.33 | 12.3% | 137.2 | 8/8 | 0.88 | 0.54 | 0.24 | 4 | 5.3% | 0.86 | 0.57 | 39.8% | 38.7% | 33.2% | 39.5%/30.8% | 18.7 (interpolated) | pass | 0.010 (unverified) | 0.44 |
| 167 | `cfg_eb8f` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 32/49/53 | 134 | 42.9% | 7.4% | 0.83 | -9.7% | 383 | 1.51 | 11.5% | 70.0 | 9/9 | 0.89 | 0.60 | 0.23 | 5 | 22.6% | 0.41 | 0.62 | 42.2% | 41.6% | 14.2% | 39.0%/27.2% | n/a (profitable_beyond_25.0x) | pass | 0.011 (unverified) | 0.78 |
| 168 | `cfg_657a` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=5, entry_z=-3.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 76/32/77 | 185 | 49.3% | 8.4% | 0.78 | -11.0% | 184 | 1.37 | 12.8% | 96.6 | 9/9 | 0.89 | 0.67 | 0.12 | 5 | 21.5% | 0.49 | 0.55 | 48.0% | 47.4% | 15.8% | 41.4%/31.3% | n/a (profitable_beyond_25.0x) | pass | 0.009 (unverified) | 0.19 |
| 169 | `cfg_3b1b` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 66/19/52 | 137 | 39.7% | 6.9% | 0.89 | -6.4% | 204 | 1.52 | 9.3% | 70.1 | 10/10 | 0.90 | 0.61 | 0.28 | 5 | 22.7% | 0.42 | 0.52 | 39.1% | 38.6% | 10.8% | 34.1%/25.4% | n/a (profitable_beyond_25.0x) | pass | 0.016 (unverified) | 0.68 |
| 170 | `cfg_3d33` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=-1.25, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 60/3/38 | 101 | 30.0% | 5.4% | 0.82 | -7.7% | 201 | 1.49 | 5.3% | 51.8 | 9/9 | 0.67 | 0.45 | 0.37 | 4 | 17.1% | 0.37 | 0.64 | 29.6% | 29.2% | 18.8% | 27.8%/19.5% | n/a (profitable_beyond_25.0x) | pass | 0.013 (unverified) | 0.82 |
| 171 | `cfg_e746` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 149/282/0 | 431 | 34.1% | 6.0% | 0.80 | -13.5% | 219 | 1.25 | 7.1% | 218.3 | 9/9 | 0.78 | 0.44 | 0.35 | 4 | 9.3% | 0.77 | 0.56 | 31.5% | 29.6% | 22.7% | 31.5%/23.9% | 10.6 (interpolated) | pass | 0.008 (unverified) | 0.20 |
| 172 | `cfg_acb1` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=5, entry_z=-3.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 87/59/0 | 146 | 40.7% | 7.1% | 0.77 | -9.9% | 184 | 1.47 | 13.5% | 75.3 | 9/9 | 0.89 | 0.60 | 0.18 | 5 | 28.2% | 0.30 | 0.50 | 39.9% | 39.1% | 13.8% | 38.5%/30.5% | n/a (profitable_beyond_25.0x) | pass | 0.009 (unverified) | 0.73 |
| 173 | `cfg_7b9c` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=5, entry_z=-3.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 36/104/62 | 202 | 35.4% | 6.3% | 0.78 | -6.6% | 182 | 1.39 | 10.5% | 101.9 | 10/10 | 0.90 | 0.54 | 0.25 | 4 | 19.9% | 0.44 | 0.59 | 34.7% | 34.2% | 36.0% | 32.7%/23.4% | 21.0 (interpolated) | pass | 0.009 (unverified) | 0.61 |
| 174 | `cfg_7319` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=15, entry_z=-2.0, exit_z=-1.25, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 228/37/0 | 265 | 35.6% | 6.3% | 1.08 | -4.1% | 179 | 1.58 | 5.2% | 134.9 | 10/10 | 0.80 | 0.37 | 0.71 | 5 | 20.2% | 0.43 | 0.39 | 34.3% | 32.4% | 37.2% | 32.6%/27.8% | 16.6 (interpolated) | pass | 0.043 (unverified) | 0.10 |
| 175 | `cfg_0220` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=8, entry_z=-3.5, exit_z=-1.25, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 62/24/60 | 146 | 43.0% | 7.4% | 0.75 | -14.1% | 140 | 1.39 | 10.5% | 75.5 | 8/8 | 0.88 | 0.63 | 0.13 | 5 | 26.0% | 0.40 | 0.55 | 40.4% | 38.3% | 30.6% | 38.3%/30.4% | n/a (profitable_beyond_25.0x) | pass | 0.009 (unverified) | 0.23 |
| 176 | `cfg_db2e` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=5, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 90/96/82 | 268 | 45.1% | 7.7% | 0.79 | -11.2% | 395 | 1.35 | 13.1% | 135.8 | 9/9 | 0.89 | 0.54 | 0.26 | 4 | 11.7% | 0.70 | 0.58 | 44.4% | 42.9% | 33.2% | 38.9%/28.9% | 19.9 (interpolated) | pass | 0.011 (unverified) | 0.65 |
| 177 | `cfg_18f9` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=5, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 100/60/0 | 160 | 46.9% | 8.0% | 0.81 | -7.4% | 243 | 1.43 | 14.4% | 83.2 | 8/8 | 0.88 | 0.64 | 0.17 | 4 | 14.8% | 0.61 | 0.58 | 46.7% | 46.5% | 34.0% | 40.0%/30.6% | n/a (profitable_beyond_25.0x) | pass | 0.011 (unverified) | 0.50 |
| 178 | `cfg_58e0` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=5, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 73/62/0 | 135 | 52.6% | 8.8% | 0.86 | -9.1% | 385 | 1.56 | 13.3% | 71.1 | 10/10 | 0.90 | 0.67 | 0.19 | 4 | 32.6% | 0.35 | 0.51 | 52.0% | 51.9% | 29.0% | 47.3%/36.1% | n/a (profitable_beyond_25.0x) | pass | 0.015 (unverified) | 0.42 |
| 179 | `cfg_2fea` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=8, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 48/62/0 | 110 | 33.7% | 6.0% | 0.75 | -7.0% | 243 | 1.53 | 11.5% | 56.8 | 11/11 | 0.73 | 0.37 | 0.38 | 4 | 19.4% | 0.39 | 0.61 | 33.7% | 32.8% | 23.2% | 31.0%/24.1% | n/a (profitable_beyond_25.0x) | pass | 0.009 (unverified) | 0.12 |
| 180 | `cfg_018e` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.5, exit_z=-1.25, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 12/91/0 | 103 | 13.4% | 2.6% | 0.79 | -3.5% | 360 | 1.99 | 1.2% | 51.1 | 9/9 | 0.89 | 0.16 | 0.63 | 5 | 8.9% | 0.32 | 0.62 | 13.1% | 12.7% | 19.3% | 11.6%/8.4% | 19.8 (interpolated) | pass | 0.001 (unverified) | 0.68 |
| 181 | `cfg_6bd1` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=-1.25, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 76/190/0 | 266 | 27.4% | 5.0% | 0.86 | -9.3% | 233 | 1.39 | 4.6% | 133.4 | 11/11 | 0.91 | 0.33 | 0.53 | 5 | 14.8% | 0.40 | 0.42 | 26.6% | 25.6% | 22.5% | 23.5%/17.4% | 13.5 (interpolated) | pass | 0.012 (unverified) | 0.45 |
| 182 | `cfg_6553` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 24/81/0 | 105 | 16.8% | 3.2% | 0.76 | -5.7% | 169 | 1.59 | 1.9% | 52.3 | 12/12 | 0.83 | 0.36 | 0.40 | 5 | 11.3% | 0.32 | 0.67 | 16.2% | 15.8% | 4.8% | 14.2%/10.0% | 21.2 (interpolated) | pass | 0.005 (unverified) | 1.23 |
| 183 | `cfg_624c` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 45/70/0 | 115 | 43.0% | 7.4% | 0.84 | -7.3% | 195 | 1.65 | 12.3% | 59.2 | 11/11 | 0.91 | 0.61 | 0.23 | 5 | 25.3% | 0.35 | 0.49 | 42.6% | 42.0% | 38.2% | 40.9%/31.1% | n/a (profitable_beyond_25.0x) | pass | 0.015 (unverified) | 0.05 |
| 184 | `cfg_c16e` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=8, entry_z=-2.0, exit_z=-1.25, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 74/3/35 | 112 | 22.5% | 4.1% | 0.75 | -6.0% | 324 | 1.46 | 5.3% | 56.8 | 8/8 | 0.88 | 0.59 | 0.16 | 5 | 9.0% | 0.60 | 0.61 | 21.5% | 21.5% | 3.6% | 18.9%/13.4% | n/a (profitable_beyond_25.0x) | pass | 0.008 (unverified) | 0.04 |
| 185 | `cfg_b73c` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 112/59/0 | 171 | 24.7% | 4.5% | 0.79 | -7.4% | 245 | 1.46 | 4.4% | 85.6 | 12/12 | 0.83 | 0.32 | 0.47 | 5 | 16.3% | 0.34 | 0.53 | 23.4% | 22.6% | 26.6% | 22.0%/17.8% | 17.7 (interpolated) | pass | 0.009 (unverified) | -0.08 |
| 186 | `cfg_fcc0` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 8/95/0 | 103 | 12.9% | 2.5% | 0.76 | -3.6% | 360 | 1.96 | 1.2% | 51.0 | 10/10 | 0.80 | 0.28 | 0.49 | 5 | 8.5% | 0.33 | 0.65 | 12.6% | 12.2% | 17.0% | 11.3%/7.6% | 18.8 (interpolated) | pass | 0.001 (unverified) | 0.68 |
| 187 | `cfg_9c5c` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=8, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 73/73/53 | 199 | 37.2% | 6.5% | 0.77 | -8.1% | 209 | 1.40 | 10.4% | 101.1 | 11/11 | 0.82 | 0.57 | 0.21 | 4 | 18.1% | 0.46 | 0.55 | 34.8% | 34.1% | 11.9% | 31.5%/19.9% | 22.5 (interpolated) | pass | 0.013 (unverified) | 0.32 |
| 188 | `cfg_2699` | timeframe=1h, mean_type=sma, mean_lookback=25, std_lookback=8, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 42/67/0 | 109 | 40.6% | 7.1% | 0.81 | -5.6% | 156 | 1.58 | 11.9% | 56.8 | 10/10 | 0.70 | 0.44 | 0.37 | 5 | 26.8% | 0.33 | 0.62 | 39.9% | 39.8% | 37.2% | 35.6%/28.2% | n/a (profitable_beyond_25.0x) | pass | 0.012 (unverified) | 0.13 |
| 189 | `cfg_e484` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 41/21/44 | 106 | 33.2% | 5.9% | 0.78 | -8.6% | 184 | 1.52 | 8.0% | 53.2 | 11/11 | 0.91 | 0.57 | 0.21 | 5 | 15.6% | 0.53 | 0.62 | 32.0% | 31.5% | 14.3% | 29.5%/21.4% | n/a (profitable_beyond_25.0x) | pass | 0.009 (unverified) | 0.64 |
| 190 | `cfg_feef` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=8, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 55/51/0 | 106 | 37.5% | 6.6% | 0.79 | -7.2% | 311 | 1.59 | 10.4% | 54.5 | 10/10 | 0.90 | 0.53 | 0.26 | 5 | 14.6% | 0.55 | 0.53 | 37.1% | 36.6% | 28.9% | 34.7%/28.8% | n/a (profitable_beyond_25.0x) | pass | 0.011 (unverified) | 0.19 |
| 191 | `cfg_bee3` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-3.5, exit_z=-1.25, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 92/116/0 | 208 | 27.3% | 4.9% | 0.76 | -11.8% | 248 | 1.38 | 6.0% | 105.5 | 10/10 | 0.80 | 0.28 | 0.48 | 4 | 14.7% | 0.45 | 0.52 | 25.8% | 24.4% | 24.5% | 25.8%/21.8% | 17.4 (interpolated) | pass | 0.007 (unverified) | 0.41 |
| 192 | `cfg_3c0b` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=10, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 24/77/46 | 147 | 41.5% | 7.2% | 0.93 | -9.6% | 200 | 1.54 | 8.2% | 75.4 | 11/11 | 0.73 | 0.27 | 0.66 | 4 | 23.5% | 0.37 | 0.48 | 41.1% | 40.5% | 5.7% | 36.1%/23.4% | n/a (profitable_beyond_25.0x) | pass | 0.014 (unverified) | 0.31 |
| 193 | `cfg_2822` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 108/320/0 | 428 | 32.0% | 5.7% | 0.75 | -14.3% | 219 | 1.23 | 7.3% | 217.1 | 10/10 | 0.80 | 0.40 | 0.35 | 4 | 5.6% | 0.90 | 0.62 | 30.8% | 26.9% | 21.3% | 27.6%/17.3% | 10.0 (interpolated) | pass | 0.006 (unverified) | 0.12 |
| 194 | `cfg_acf4` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=10, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 7/93/47 | 147 | 38.1% | 6.7% | 0.87 | -9.5% | 270 | 1.49 | 8.4% | 75.2 | 10/10 | 0.70 | 0.34 | 0.53 | 4 | 20.5% | 0.41 | 0.53 | 37.5% | 37.1% | 9.3% | 35.1%/24.2% | n/a (profitable_beyond_25.0x) | pass | 0.010 (unverified) | 0.34 |
| 195 | `cfg_b8af` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=5, entry_z=-2.0, exit_z=0.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 28/157/0 | 185 | 34.4% | 6.1% | 0.86 | -10.6% | 544 | 1.53 | 8.2% | 93.3 | 8/8 | 0.88 | 0.36 | 0.50 | 4 | 10.2% | 0.59 | 0.56 | 34.2% | 33.6% | 17.5% | 30.7%/21.6% | 23.7 (interpolated) | pass | 0.012 (unverified) | 0.31 |
| 196 | `cfg_a571` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 52/20/48 | 120 | 41.5% | 7.2% | 0.84 | -11.0% | 184 | 1.53 | 8.2% | 61.4 | 10/10 | 0.90 | 0.56 | 0.29 | 5 | 21.7% | 0.42 | 0.56 | 41.5% | 40.8% | 27.0% | 38.0%/28.1% | n/a (profitable_beyond_25.0x) | pass | 0.012 (unverified) | 0.20 |
| 197 | `cfg_d3ee` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 54/211/0 | 265 | 26.2% | 4.8% | 0.84 | -9.5% | 253 | 1.37 | 4.7% | 132.7 | 12/12 | 0.92 | 0.32 | 0.52 | 4 | 12.6% | 0.46 | 0.44 | 25.3% | 24.3% | 23.3% | 22.4%/15.4% | 13.3 (interpolated) | pass | 0.011 (unverified) | 0.49 |
| 198 | `cfg_0343` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=15, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 144/103/0 | 247 | 27.2% | 4.9% | 0.76 | -6.1% | 382 | 1.34 | 6.6% | 124.5 | 11/11 | 0.82 | 0.30 | 0.46 | 5 | 14.5% | 0.47 | 0.55 | 26.9% | 25.8% | 31.3% | 25.5%/18.3% | 14.3 (interpolated) | pass | 0.008 (unverified) | -0.35 |
| 199 | `cfg_f8eb` | timeframe=1h, mean_type=ema, mean_lookback=25, std_lookback=5, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 37/148/0 | 185 | 30.7% | 5.5% | 0.81 | -11.0% | 546 | 1.49 | 8.1% | 92.7 | 9/9 | 0.89 | 0.28 | 0.53 | 4 | 8.9% | 0.60 | 0.59 | 30.1% | 29.1% | 15.6% | 25.9%/15.8% | 21.1 (interpolated) | pass | 0.008 (unverified) | 0.32 |
| 200 | `cfg_e54c` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.25, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 19/89/0 | 108 | 13.2% | 2.5% | 0.75 | -3.7% | 381 | 1.77 | 1.3% | 53.3 | 11/11 | 0.82 | 0.44 | 0.31 | 5 | 7.7% | 0.41 | 0.65 | 12.8% | 12.4% | 20.5% | 11.7%/8.5% | 17.6 (interpolated) | pass | 0.001 (unverified) | 0.39 |
| 201 | `cfg_2848` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 17/91/0 | 108 | 13.2% | 2.5% | 0.75 | -3.7% | 381 | 1.77 | 1.3% | 53.3 | 12/12 | 0.75 | 0.46 | 0.29 | 5 | 7.7% | 0.41 | 0.65 | 12.8% | 12.4% | 20.2% | 11.5%/6.7% | 17.6 (interpolated) | pass | 0.001 (unverified) | 0.39 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 3.9% / 0.51 / 27 | 6.2% / 1.69 / 15 | 22.4% / 2.02 / 17 | 3.5% / 1.03 / 10 | 22.5% / 2.15 / 40 |
| 2 | 3.3% / 0.54 / 25 | 5.6% / 1.75 / 18 | 16.0% / 1.88 / 16 | 7.3% / 2.18 / 14 | 14.1% / 1.62 / 41 |
| 3 | 4.2% / 0.53 / 27 | 5.9% / 1.62 / 15 | 21.3% / 1.93 / 17 | 3.6% / 1.05 / 10 | 18.6% / 1.92 / 40 |
| 4 | 8.4% / 1.25 / 23 | 6.1% / 1.91 / 16 | 9.0% / 1.69 / 15 | 1.1% / 0.36 / 13 | 11.0% / 1.34 / 40 |
| 5 | 7.8% / 1.17 / 23 | 5.6% / 1.77 / 16 | 9.4% / 1.80 / 15 | 0.7% / 0.26 / 13 | 10.1% / 1.27 / 40 |
| 6 | 0.1% / 0.05 / 29 | 7.1% / 1.74 / 21 | 22.9% / 2.55 / 19 | 2.1% / 0.54 / 18 | 9.8% / 1.11 / 45 |
| 7 | -0.1% / 0.02 / 29 | 6.0% / 1.49 / 21 | 20.9% / 2.30 / 19 | 1.9% / 0.51 / 18 | 10.8% / 1.20 / 45 |
| 8 | 6.3% / 0.93 / 25 | 5.5% / 1.71 / 18 | 11.2% / 1.42 / 15 | 5.8% / 1.80 / 14 | 11.4% / 1.35 / 39 |
| 9 | 4.6% / 0.55 / 28 | 5.8% / 1.30 / 19 | 26.7% / 2.82 / 19 | 4.0% / 0.78 / 18 | 15.0% / 1.20 / 51 |
| 10 | -3.2% / -0.37 / 33 | 8.2% / 2.69 / 13 | 19.8% / 1.44 / 19 | 8.7% / 2.18 / 15 | 18.7% / 1.64 / 49 |
| 11 | 3.7% / 0.45 / 27 | 4.1% / 0.94 / 16 | 16.7% / 1.74 / 17 | 7.0% / 1.90 / 10 | 15.1% / 1.27 / 42 |
| 12 | 8.8% / 1.18 / 25 | 5.3% / 1.63 / 18 | 11.0% / 1.12 / 15 | 5.3% / 1.68 / 14 | 11.9% / 1.39 / 39 |
| 13 | -2.8% / -0.32 / 33 | 8.4% / 2.75 / 13 | 19.1% / 1.34 / 19 | 8.9% / 2.24 / 15 | 15.8% / 1.45 / 49 |
| 14 | 0.4% / 0.09 / 27 | 4.3% / 0.95 / 16 | 17.1% / 1.92 / 17 | 10.1% / 2.50 / 10 | 16.4% / 1.26 / 42 |
| 15 | 2.3% / 0.37 / 23 | 3.8% / 1.06 / 15 | 14.0% / 1.78 / 14 | 0.1% / 0.05 / 13 | 17.1% / 2.03 / 41 |
| 16 | 4.4% / 0.54 / 34 | 4.0% / 1.05 / 18 | 14.9% / 1.29 / 20 | 8.7% / 2.07 / 13 | 14.1% / 1.49 / 39 |
| 17 | 4.3% / 0.61 / 23 | 4.3% / 1.12 / 15 | 13.9% / 1.51 / 14 | -0.5% / -0.14 / 13 | 17.4% / 2.06 / 41 |
| 18 | 4.8% / 0.58 / 34 | 3.9% / 1.02 / 18 | 15.8% / 1.35 / 20 | 8.4% / 2.00 / 13 | 14.3% / 1.51 / 39 |
| 19 | 4.1% / 0.55 / 28 | 4.0% / 0.99 / 19 | 22.3% / 2.53 / 19 | 6.8% / 1.40 / 18 | 7.5% / 0.69 / 51 |
| 20 | 0.6% / 0.11 / 34 | 2.9% / 0.78 / 19 | 16.9% / 2.09 / 21 | 4.3% / 0.93 / 18 | 9.0% / 1.12 / 39 |
| 21 | 0.6% / 0.11 / 34 | 2.9% / 0.78 / 19 | 17.4% / 2.11 / 21 | 3.9% / 0.87 / 18 | 8.4% / 1.06 / 39 |
| 22 | 3.1% / 0.34 / 43 | 6.8% / 1.14 / 32 | 31.4% / 2.06 / 31 | 10.6% / 1.63 / 31 | 14.4% / 0.99 / 64 |
| 23 | 5.0% / 0.61 / 37 | 6.3% / 1.42 / 24 | 18.5% / 1.66 / 27 | 4.3% / 0.99 / 21 | 10.0% / 1.10 / 42 |
| 24 | 4.4% / 0.56 / 30 | 5.3% / 1.45 / 21 | 11.5% / 0.93 / 20 | 9.4% / 2.08 / 17 | 15.4% / 1.43 / 47 |
| 25 | 1.1% / 0.16 / 46 | 6.9% / 1.14 / 32 | 33.5% / 1.93 / 36 | 12.6% / 1.90 / 36 | 10.5% / 0.78 / 66 |
| 26 | 0.1% / 0.07 / 33 | 6.8% / 1.32 / 20 | 18.1% / 1.61 / 21 | 9.0% / 1.61 / 18 | 15.9% / 1.13 / 56 |
| 27 | 5.3% / 0.65 / 37 | 4.3% / 0.83 / 24 | 18.2% / 1.61 / 27 | 4.5% / 1.07 / 21 | 10.0% / 1.12 / 42 |
| 28 | 3.5% / 0.41 / 20 | 5.5% / 0.96 / 17 | 29.9% / 3.26 / 16 | 9.1% / 1.95 / 15 | 5.7% / 0.54 / 34 |
| 29 | 1.0% / 0.27 / 29 | 2.5% / 1.13 / 14 | 13.6% / 1.61 / 18 | 4.3% / 1.67 / 21 | 7.8% / 0.96 / 46 |
| 30 | 1.0% / 0.27 / 29 | 2.5% / 1.13 / 14 | 12.4% / 1.53 / 18 | 4.3% / 1.65 / 21 | 7.8% / 0.97 / 46 |
| 31 | 8.0% / 0.99 / 22 | 4.0% / 0.93 / 15 | 8.9% / 1.41 / 13 | 5.1% / 1.29 / 13 | 11.5% / 1.08 / 43 |
| 32 | 7.4% / 0.79 / 34 | 2.8% / 0.62 / 20 | 19.9% / 1.40 / 20 | 11.9% / 2.23 / 14 | 13.8% / 1.13 / 45 |
| 33 | 2.5% / 0.67 / 21 | 1.7% / 0.54 / 15 | 6.3% / 1.24 / 13 | 2.2% / 0.70 / 11 | 11.1% / 1.69 / 40 |
| 34 | 4.0% / 0.43 / 35 | 4.3% / 0.98 / 16 | 16.7% / 1.36 / 20 | 12.2% / 2.34 / 15 | 8.9% / 0.72 / 51 |
| 35 | 1.4% / 0.18 / 40 | 3.4% / 0.62 / 23 | 22.7% / 1.67 / 29 | 13.9% / 2.16 / 27 | 10.6% / 0.77 / 60 |
| 36 | 4.0% / 0.51 / 30 | 4.6% / 1.29 / 21 | 11.6% / 0.93 / 20 | 8.8% / 2.07 / 17 | 14.3% / 1.35 / 47 |
| 37 | 2.3% / 0.29 / 33 | 4.1% / 0.85 / 21 | 15.2% / 1.37 / 21 | 8.6% / 1.95 / 18 | 14.7% / 1.13 / 56 |
| 38 | 3.9% / 0.61 / 31 | 4.4% / 1.43 / 14 | 21.6% / 1.79 / 21 | 4.8% / 1.37 / 22 | 7.3% / 0.66 / 45 |
| 39 | 1.4% / 0.24 / 28 | 7.7% / 1.96 / 22 | 11.9% / 1.39 / 22 | 4.1% / 1.01 / 20 | 14.9% / 1.41 / 43 |
| 40 | 9.9% / 1.01 / 36 | 4.0% / 0.69 / 24 | 13.2% / 0.90 / 26 | 6.7% / 1.14 / 22 | 14.5% / 1.11 / 51 |
| 41 | -0.4% / -0.06 / 26 | 0.9% / 0.43 / 12 | 14.8% / 1.80 / 18 | 4.9% / 2.22 / 14 | 7.3% / 1.16 / 32 |
| 42 | -0.6% / -0.03 / 34 | 5.8% / 1.58 / 19 | 22.8% / 2.16 / 21 | 3.6% / 0.99 / 18 | 11.1% / 1.09 / 51 |
| 43 | -2.7% / -0.26 / 39 | 7.2% / 1.77 / 22 | 37.3% / 3.04 / 24 | 0.3% / 0.08 / 24 | 2.1% / 0.25 / 55 |
| 44 | -2.5% / -0.29 / 34 | 4.3% / 1.19 / 19 | 22.5% / 2.55 / 21 | 3.4% / 0.99 / 18 | 10.3% / 1.04 / 51 |
| 45 | 0.4% / 0.09 / 40 | 3.9% / 0.67 / 23 | 21.8% / 1.57 / 29 | 15.0% / 2.22 / 27 | 10.3% / 0.76 / 59 |
| 46 | 3.7% / 0.85 / 21 | 1.6% / 0.51 / 15 | 6.3% / 1.24 / 13 | 2.1% / 0.69 / 11 | 11.1% / 1.68 / 40 |
| 47 | 2.6% / 0.40 / 26 | -3.4% / -0.88 / 14 | 23.9% / 2.12 / 18 | 12.6% / 3.08 / 14 | -0.2% / 0.03 / 35 |
| 48 | 8.0% / 0.89 / 35 | 1.7% / 0.42 / 20 | 17.4% / 1.32 / 20 | 12.4% / 2.83 / 14 | 8.6% / 0.76 / 45 |
| 49 | -0.4% / -0.02 / 26 | -2.1% / -0.64 / 12 | 25.4% / 2.49 / 16 | 5.2% / 1.75 / 14 | 5.5% / 0.64 / 35 |
| 50 | 3.0% / 0.34 / 42 | 7.6% / 1.29 / 30 | 15.5% / 0.88 / 35 | 15.3% / 2.11 / 32 | 10.4% / 0.72 / 71 |
| 51 | 0.3% / 0.08 / 35 | 4.8% / 1.04 / 16 | 18.4% / 1.49 / 20 | 14.6% / 2.72 / 15 | 7.8% / 0.61 / 51 |
| 52 | 4.1% / 0.46 / 30 | 3.0% / 0.67 / 23 | 16.2% / 1.32 / 20 | 15.5% / 2.69 / 18 | 7.3% / 0.59 / 52 |
| 53 | 4.3% / 0.67 / 31 | 4.4% / 1.39 / 14 | 20.5% / 1.74 / 21 | 4.5% / 1.31 / 22 | 6.7% / 0.61 / 45 |
| 54 | -3.5% / -0.42 / 40 | 6.2% / 1.59 / 23 | 21.6% / 1.68 / 23 | 11.4% / 2.47 / 30 | 12.4% / 1.20 / 56 |
| 55 | 1.4% / 0.19 / 20 | 3.5% / 0.64 / 17 | 26.0% / 3.06 / 16 | 10.6% / 2.17 / 15 | -0.5% / 0.00 / 34 |
| 56 | 6.7% / 0.73 / 29 | 11.9% / 2.20 / 27 | 12.2% / 1.26 / 23 | 8.1% / 1.38 / 21 | 8.0% / 0.62 / 59 |
| 57 | 5.9% / 0.64 / 32 | 5.0% / 1.09 / 20 | 15.3% / 1.21 / 21 | 6.0% / 1.02 / 18 | 12.1% / 1.01 / 47 |
| 58 | 4.0% / 0.47 / 43 | 5.8% / 1.00 / 30 | 35.3% / 1.99 / 36 | 12.9% / 2.14 / 32 | -2.7% / -0.12 / 72 |
| 59 | -1.1% / -0.12 / 28 | 5.8% / 1.64 / 22 | 12.6% / 1.42 / 22 | 3.3% / 0.82 / 20 | 13.5% / 1.47 / 42 |
| 60 | 6.9% / 0.93 / 22 | 3.6% / 0.89 / 15 | 7.7% / 1.26 / 13 | 2.3% / 0.63 / 13 | 6.3% / 0.64 / 43 |
| 61 | 8.1% / 1.04 / 23 | 5.4% / 1.48 / 18 | 11.4% / 1.40 / 14 | 12.3% / 3.20 / 14 | -1.3% / -0.07 / 42 |
| 62 | 5.0% / 0.52 / 36 | 5.3% / 0.86 / 24 | 13.7% / 0.88 / 26 | 8.2% / 1.31 / 22 | 12.6% / 0.91 / 51 |
| 63 | 3.4% / 0.71 / 37 | 8.4% / 2.32 / 33 | 8.0% / 1.26 / 22 | 1.7% / 0.62 / 26 | 5.0% / 0.84 / 63 |
| 64 | 2.3% / 0.51 / 41 | 10.1% / 2.75 / 36 | 6.6% / 1.08 / 24 | 1.5% / 0.51 / 26 | 8.3% / 1.30 / 59 |
| 65 | -0.4% / -0.06 / 26 | 0.9% / 0.43 / 12 | 13.6% / 1.73 / 18 | 4.8% / 2.18 / 14 | 7.2% / 1.15 / 32 |
| 66 | 7.8% / 0.79 / 35 | 6.8% / 1.36 / 24 | 22.0% / 1.37 / 25 | 6.7% / 1.12 / 26 | 6.9% / 0.52 / 64 |
| 67 | 0.8% / 0.14 / 28 | 2.6% / 0.72 / 15 | 18.6% / 1.85 / 18 | 2.4% / 0.73 / 14 | 6.5% / 0.70 / 47 |
| 68 | 1.1% / 0.18 / 28 | 2.6% / 0.72 / 15 | 17.8% / 1.77 / 18 | 2.2% / 0.70 / 14 | 5.7% / 0.64 / 47 |
| 69 | 2.3% / 0.27 / 44 | 6.3% / 1.02 / 31 | 18.5% / 1.43 / 29 | 9.7% / 1.43 / 34 | 11.2% / 0.80 / 65 |
| 70 | 2.5% / 0.29 / 42 | 7.9% / 1.29 / 30 | 13.7% / 0.79 / 35 | 15.5% / 2.02 / 32 | 14.2% / 0.92 / 71 |
| 71 | 0.2% / 0.07 / 24 | 2.0% / 0.68 / 21 | 9.4% / 1.39 / 20 | 3.5% / 1.20 / 16 | 9.5% / 1.23 / 41 |
| 72 | 3.1% / 0.58 / 24 | -1.8% / -0.78 / 17 | 8.5% / 1.35 / 15 | 5.3% / 1.98 / 13 | 9.3% / 1.35 / 36 |
| 73 | -5.6% / -0.72 / 47 | 3.5% / 0.66 / 35 | 25.6% / 2.47 / 31 | 4.7% / 0.98 / 31 | 14.0% / 1.35 / 67 |
| 74 | 4.5% / 1.08 / 17 | -0.1% / -0.02 / 14 | 6.9% / 1.32 / 12 | 4.5% / 1.90 / 12 | 8.1% / 1.49 / 46 |
| 75 | 0.2% / 0.07 / 24 | 2.2% / 0.71 / 21 | 9.4% / 1.39 / 20 | 3.5% / 1.19 / 16 | 7.4% / 1.04 / 41 |
| 76 | 5.1% / 0.59 / 23 | 6.1% / 1.48 / 18 | 13.5% / 1.62 / 14 | 9.8% / 2.08 / 14 | -2.2% / -0.15 / 42 |
| 77 | 3.8% / 0.41 / 35 | 6.9% / 1.30 / 24 | 23.6% / 1.41 / 25 | 8.6% / 1.36 / 26 | 9.7% / 0.68 / 64 |
| 78 | 0.4% / 0.09 / 33 | 4.4% / 1.68 / 10 | 14.3% / 1.12 / 16 | 6.9% / 2.08 / 12 | 5.7% / 0.63 / 42 |
| 79 | -0.1% / 0.04 / 44 | 5.7% / 0.90 / 31 | 11.3% / 0.98 / 29 | 14.5% / 2.02 / 34 | 15.1% / 1.02 / 65 |
| 80 | -3.0% / -0.30 / 39 | 8.0% / 1.95 / 22 | 33.6% / 2.86 / 24 | 0.4% / 0.12 / 24 | 2.2% / 0.25 / 55 |
| 81 | 2.4% / 0.32 / 31 | 3.4% / 0.87 / 16 | 18.5% / 1.72 / 22 | 10.6% / 2.03 / 18 | 6.8% / 0.58 / 47 |
| 82 | 0.5% / 0.10 / 37 | 8.3% / 1.53 / 25 | 6.4% / 0.55 / 23 | 18.8% / 2.92 / 27 | 9.8% / 0.74 / 59 |
| 83 | -0.9% / -0.03 / 59 | 18.3% / 2.47 / 50 | 29.1% / 1.63 / 43 | 6.7% / 0.98 / 50 | 3.3% / 0.29 / 80 |
| 84 | 0.2% / 0.06 / 40 | 5.1% / 1.29 / 22 | 9.7% / 0.77 / 21 | 9.4% / 2.18 / 27 | 14.6% / 1.31 / 53 |
| 85 | 5.9% / 0.96 / 24 | -1.8% / -0.77 / 17 | 4.1% / 0.80 / 14 | 5.3% / 1.96 / 13 | 8.6% / 1.27 / 35 |
| 86 | 5.3% / 0.68 / 28 | 1.9% / 0.60 / 13 | 12.7% / 2.15 / 15 | 0.8% / 0.24 / 13 | 7.4% / 0.99 / 42 |
| 87 | -1.0% / -0.06 / 59 | 17.6% / 2.41 / 50 | 26.0% / 1.48 / 43 | 8.5% / 1.29 / 50 | 0.3% / 0.10 / 80 |
| 88 | -5.3% / -0.68 / 47 | 3.2% / 0.61 / 35 | 27.5% / 2.58 / 31 | 3.3% / 0.71 / 31 | 10.7% / 1.03 / 68 |
| 89 | 5.3% / 0.68 / 28 | 1.5% / 0.49 / 13 | 13.0% / 2.19 / 15 | 0.5% / 0.15 / 13 | 7.2% / 0.97 / 42 |
| 90 | -1.9% / -0.19 / 40 | 6.3% / 1.62 / 23 | 12.3% / 1.02 / 22 | 6.8% / 1.92 / 27 | 10.6% / 1.06 / 53 |
| 91 | 0.5% / 0.10 / 52 | 11.2% / 1.77 / 42 | 29.5% / 1.63 / 42 | 6.6% / 0.95 / 40 | 2.7% / 0.25 / 77 |
| 92 | -6.7% / -0.91 / 44 | 5.7% / 1.12 / 31 | 34.4% / 2.14 / 34 | 9.4% / 1.66 / 34 | 2.2% / 0.25 / 66 |
| 93 | 0.4% / 0.09 / 33 | 4.4% / 1.68 / 10 | 13.4% / 1.06 / 16 | 7.1% / 2.11 / 12 | 6.8% / 0.73 / 42 |
| 94 | -6.8% / -0.92 / 48 | 4.6% / 0.85 / 35 | 33.8% / 2.50 / 36 | 4.5% / 0.87 / 36 | 11.0% / 1.06 / 70 |
| 95 | 4.9% / 0.62 / 27 | 9.2% / 2.08 / 22 | 4.8% / 0.54 / 21 | 7.6% / 1.63 / 20 | 6.8% / 0.63 / 43 |
| 96 | 7.1% / 0.90 / 21 | 4.9% / 1.45 / 14 | 8.6% / 1.18 / 15 | 1.9% / 0.47 / 13 | 5.6% / 0.57 / 44 |
| 97 | 0.1% / 0.06 / 32 | 5.5% / 1.14 / 20 | 18.0% / 1.36 / 21 | 6.3% / 1.09 / 18 | 7.8% / 0.67 / 47 |
| 98 | 4.6% / 0.47 / 41 | 4.6% / 0.89 / 32 | 10.8% / 0.85 / 26 | 17.5% / 2.74 / 28 | 2.5% / 0.24 / 62 |
| 99 | 4.7% / 1.09 / 20 | 0.2% / 0.09 / 13 | 4.3% / 0.82 / 14 | 5.1% / 1.84 / 13 | 5.4% / 0.97 / 45 |
| 100 | 6.7% / 0.81 / 29 | 8.3% / 1.72 / 27 | 9.4% / 0.99 / 23 | 8.9% / 1.69 / 21 | 1.0% / 0.14 / 59 |
| 101 | 1.8% / 0.33 / 24 | 2.3% / 0.81 / 12 | 16.7% / 1.92 / 15 | 2.7% / 0.85 / 18 | 8.4% / 0.90 / 39 |
| 102 | 3.4% / 0.40 / 38 | 3.9% / 0.68 / 26 | 13.6% / 1.27 / 21 | 13.6% / 2.06 / 30 | 4.8% / 0.42 / 56 |
| 103 | 2.7% / 0.31 / 46 | 8.0% / 1.24 / 37 | 17.2% / 1.08 / 36 | 12.4% / 1.78 / 36 | 9.5% / 0.65 / 73 |
| 104 | -1.5% / -0.22 / 85 | 9.0% / 2.36 / 70 | 13.4% / 1.44 / 65 | 4.0% / 0.96 / 70 | 8.4% / 0.85 / 130 |
| 105 | 1.6% / 0.20 / 48 | 8.1% / 1.31 / 36 | 17.9% / 1.12 / 39 | 11.5% / 1.55 / 38 | 8.9% / 0.63 / 73 |
| 106 | 7.3% / 1.13 / 23 | 5.5% / 1.51 / 18 | 10.6% / 1.46 / 15 | 8.3% / 2.33 / 14 | 1.8% / 0.23 / 44 |
| 107 | 2.6% / 0.28 / 52 | 12.4% / 1.91 / 42 | 25.7% / 1.47 / 42 | 4.9% / 0.70 / 40 | 7.8% / 0.56 / 76 |
| 108 | 4.8% / 0.50 / 42 | 4.9% / 0.89 / 26 | 23.6% / 1.32 / 36 | 15.7% / 2.35 / 31 | 0.2% / 0.09 / 68 |
| 109 | 1.5% / 0.27 / 24 | 2.3% / 0.81 / 12 | 18.6% / 2.08 / 15 | 3.4% / 1.00 / 18 | 6.7% / 0.73 / 39 |
| 110 | 7.0% / 0.74 / 43 | 4.1% / 0.75 / 26 | 21.4% / 1.24 / 36 | 12.5% / 2.05 / 31 | -0.6% / 0.03 / 69 |
| 111 | 4.6% / 1.11 / 17 | 0.3% / 0.13 / 14 | 6.2% / 1.33 / 12 | 4.2% / 1.78 / 12 | 6.8% / 1.29 / 46 |
| 112 | -8.1% / -1.24 / 37 | 2.1% / 0.45 / 30 | 18.8% / 1.99 / 31 | 8.6% / 2.38 / 35 | 12.5% / 1.39 / 56 |
| 113 | 1.6% / 0.36 / 41 | 9.9% / 2.71 / 36 | 7.1% / 1.13 / 24 | 0.7% / 0.25 / 26 | 8.0% / 1.25 / 59 |
| 114 | 1.7% / 0.23 / 27 | 6.8% / 2.06 / 12 | 7.4% / 0.63 / 16 | 8.9% / 2.08 / 10 | 12.6% / 1.18 / 38 |
| 115 | -1.5% / -0.21 / 27 | 4.2% / 1.24 / 17 | 9.1% / 1.51 / 14 | 2.5% / 0.76 / 14 | 8.6% / 1.07 / 42 |
| 116 | -2.0% / -0.20 / 38 | 6.8% / 1.70 / 27 | 18.8% / 1.77 / 27 | 2.3% / 0.68 / 21 | 7.3% / 0.75 / 51 |
| 117 | -7.0% / -0.93 / 48 | 1.0% / 0.20 / 34 | 31.1% / 2.44 / 36 | 3.3% / 0.70 / 35 | 11.1% / 1.10 / 67 |
| 118 | 2.5% / 0.31 / 37 | 6.4% / 1.29 / 25 | 3.5% / 0.33 / 23 | 21.2% / 3.70 / 27 | 6.8% / 0.57 / 59 |
| 119 | 9.2% / 1.15 / 32 | 4.2% / 1.09 / 16 | 11.8% / 1.19 / 22 | 11.0% / 2.23 / 18 | 3.7% / 0.36 / 47 |
| 120 | 6.6% / 0.92 / 21 | 3.8% / 1.25 / 14 | 10.3% / 1.72 / 15 | 3.2% / 0.95 / 13 | 0.8% / 0.13 / 44 |
| 121 | -0.3% / -0.00 / 27 | 2.5% / 0.73 / 17 | 9.8% / 1.60 / 14 | 2.5% / 0.76 / 14 | 7.7% / 0.95 / 42 |
| 122 | 3.7% / 0.75 / 37 | 9.4% / 2.41 / 33 | 8.6% / 1.29 / 22 | 1.6% / 0.56 / 26 | -0.3% / -0.01 / 63 |
| 123 | -9.5% / -1.45 / 37 | 1.8% / 0.40 / 30 | 20.4% / 2.07 / 31 | 8.9% / 2.45 / 35 | 14.6% / 1.55 / 56 |
| 124 | -8.9% / -1.24 / 46 | 4.4% / 0.80 / 34 | 19.7% / 1.81 / 30 | 5.0% / 0.93 / 31 | 14.9% / 1.30 / 66 |
| 125 | -6.7% / -0.91 / 44 | 5.0% / 1.00 / 30 | 28.6% / 1.84 / 33 | 8.3% / 1.53 / 34 | 5.0% / 0.49 / 66 |
| 126 | 1.6% / 0.24 / 34 | 5.4% / 1.94 / 15 | 14.6% / 1.22 / 18 | 7.0% / 1.70 / 13 | 3.1% / 0.37 / 48 |
| 127 | 2.4% / 0.40 / 24 | 1.4% / 0.40 / 14 | 12.5% / 1.35 / 16 | 9.2% / 2.42 / 15 | 3.5% / 0.40 / 40 |
| 128 | 0.4% / 0.10 / 26 | -0.2% / -0.05 / 17 | 9.0% / 1.32 / 16 | 3.6% / 1.18 / 10 | 11.3% / 1.47 / 38 |
| 129 | -1.0% / -0.13 / 73 | 11.4% / 2.79 / 57 | 10.7% / 1.25 / 52 | 2.4% / 0.62 / 58 | 8.9% / 1.02 / 117 |
| 130 | -3.0% / -0.33 / 38 | 6.9% / 1.70 / 27 | 19.6% / 1.89 / 27 | 2.3% / 0.68 / 21 | 5.4% / 0.58 / 51 |
| 131 | -0.1% / 0.04 / 36 | 2.9% / 0.56 / 18 | 10.8% / 1.09 / 20 | 13.0% / 2.06 / 26 | 8.4% / 0.65 / 55 |
| 132 | 1.7% / 0.23 / 27 | 6.6% / 2.07 / 12 | 7.4% / 0.68 / 16 | 8.1% / 1.99 / 10 | 10.0% / 0.97 / 38 |
| 133 | 5.3% / 0.68 / 32 | 0.8% / 0.21 / 15 | 14.1% / 1.61 / 24 | 4.7% / 1.03 / 20 | 5.0% / 0.58 / 45 |
| 134 | -3.0% / -0.27 / 22 | 12.8% / 1.92 / 26 | 10.6% / 1.11 / 17 | 10.3% / 1.76 / 28 | 5.5% / 0.52 / 40 |
| 135 | 12.5% / 1.46 / 29 | 5.3% / 1.43 / 16 | 3.1% / 0.30 / 17 | 7.3% / 1.97 / 10 | 5.0% / 0.59 / 40 |
| 136 | -0.4% / 0.02 / 22 | 9.0% / 1.45 / 14 | 15.6% / 1.52 / 14 | 14.9% / 2.33 / 20 | 4.4% / 0.40 / 35 |
| 137 | 3.2% / 0.37 / 30 | 3.2% / 0.59 / 19 | 13.1% / 0.86 / 23 | 7.4% / 1.20 / 20 | 17.9% / 1.24 / 52 |
| 138 | 3.5% / 0.42 / 37 | 2.4% / 0.83 / 15 | 25.1% / 2.42 / 18 | 2.9% / 0.72 / 18 | -0.6% / -0.02 / 48 |
| 139 | 3.0% / 0.48 / 29 | 7.4% / 1.82 / 27 | 10.8% / 1.30 / 22 | 1.2% / 0.34 / 22 | 5.3% / 0.56 / 53 |
| 140 | 5.3% / 0.68 / 32 | 0.8% / 0.21 / 15 | 13.0% / 1.49 / 24 | 4.3% / 0.95 / 20 | 8.3% / 0.90 / 45 |
| 141 | 1.4% / 0.19 / 21 | 4.1% / 0.75 / 16 | 22.9% / 1.95 / 18 | 10.9% / 2.30 / 14 | 3.7% / 0.36 / 36 |
| 142 | 4.1% / 0.48 / 37 | 1.9% / 0.64 / 15 | 25.8% / 2.50 / 18 | 3.4% / 0.84 / 18 | -0.6% / -0.02 / 48 |
| 143 | 4.3% / 0.63 / 24 | -0.9% / -0.28 / 10 | 16.2% / 1.74 / 14 | 4.2% / 1.33 / 11 | 12.4% / 1.19 / 41 |
| 144 | -1.2% / -0.22 / 49 | 7.0% / 1.80 / 49 | 11.7% / 1.36 / 41 | -3.2% / -0.93 / 41 | 9.5% / 1.19 / 82 |
| 145 | 4.7% / 1.09 / 20 | 0.4% / 0.16 / 13 | 4.4% / 0.83 / 14 | 4.6% / 1.71 / 13 | 3.4% / 0.66 / 45 |
| 146 | 2.1% / 0.25 / 28 | 5.4% / 0.88 / 17 | 19.9% / 1.65 / 24 | 11.5% / 2.00 / 25 | 4.8% / 0.43 / 45 |
| 147 | -2.8% / -0.22 / 26 | 7.1% / 1.07 / 17 | 15.4% / 1.10 / 24 | 16.9% / 2.34 / 25 | 6.4% / 0.54 / 42 |
| 148 | -1.2% / -0.10 / 48 | 4.1% / 0.73 / 32 | 33.0% / 2.27 / 37 | 8.6% / 1.46 / 36 | -1.6% / -0.06 / 68 |
| 149 | -1.7% / -0.31 / 49 | 7.0% / 1.80 / 49 | 11.5% / 1.33 / 41 | -3.1% / -0.92 / 41 | 13.9% / 1.73 / 84 |
| 150 | 1.1% / 0.17 / 24 | 0.7% / 0.19 / 14 | 15.4% / 1.60 / 16 | 9.1% / 2.06 / 15 | 3.1% / 0.35 / 40 |
| 151 | -3.0% / -0.27 / 22 | 8.5% / 1.41 / 15 | 15.2% / 1.45 / 14 | 17.4% / 2.75 / 23 | 6.6% / 0.59 / 38 |
| 152 | 2.0% / 0.30 / 27 | 8.1% / 1.94 / 22 | 3.8% / 0.46 / 21 | 4.5% / 1.06 / 20 | 12.6% / 1.17 / 43 |
| 153 | 2.5% / 0.40 / 25 | 1.9% / 0.60 / 15 | 5.4% / 1.03 / 13 | 1.5% / 0.55 / 13 | 13.0% / 1.39 / 45 |
| 154 | -5.3% / -0.56 / 60 | 13.1% / 1.90 / 50 | 28.6% / 1.86 / 44 | 6.5% / 1.06 / 50 | 0.9% / 0.13 / 81 |
| 155 | 3.0% / 0.83 / 18 | 4.9% / 1.44 / 18 | 4.9% / 0.92 / 15 | 3.2% / 1.31 / 15 | 1.7% / 0.35 / 39 |
| 156 | -0.2% / 0.02 / 38 | 5.9% / 1.23 / 26 | 13.6% / 1.16 / 25 | 15.3% / 3.16 / 31 | 4.7% / 0.44 / 62 |
| 157 | 4.9% / 0.72 / 21 | 5.0% / 1.41 / 20 | 7.3% / 1.23 / 14 | 0.6% / 0.19 / 11 | 4.0% / 0.53 / 41 |
| 158 | 0.4% / 0.10 / 26 | -0.1% / -0.01 / 17 | 7.9% / 1.18 / 16 | 3.4% / 1.14 / 10 | 10.3% / 1.40 / 38 |
| 159 | -0.2% / 0.03 / 28 | 5.6% / 0.89 / 18 | 21.3% / 1.83 / 25 | 10.2% / 1.83 / 25 | 1.6% / 0.19 / 45 |
| 160 | -6.7% / -0.63 / 28 | 7.4% / 1.08 / 25 | 29.4% / 1.84 / 27 | 10.4% / 1.47 / 31 | 12.5% / 0.95 / 47 |
| 161 | 1.2% / 0.17 / 46 | 8.3% / 1.27 / 37 | 7.5% / 0.54 / 36 | 16.3% / 2.25 / 36 | 9.8% / 0.68 / 73 |
| 162 | -0.9% / -0.12 / 85 | 10.5% / 2.64 / 70 | 7.9% / 0.74 / 64 | 3.7% / 0.87 / 70 | 7.0% / 0.76 / 128 |
| 163 | -2.9% / -0.32 / 43 | 3.7% / 0.70 / 32 | 8.3% / 0.94 / 29 | 10.0% / 1.95 / 35 | 14.6% / 1.20 / 63 |
| 164 | -6.5% / -0.77 / 50 | 5.5% / 1.00 / 33 | 29.5% / 2.07 / 38 | 6.6% / 1.23 / 37 | 4.2% / 0.41 / 71 |
| 165 | -2.8% / -0.41 / 72 | 11.1% / 2.84 / 56 | 12.6% / 1.43 / 52 | 1.0% / 0.28 / 58 | 6.7% / 0.76 / 115 |
| 166 | -8.7% / -1.20 / 57 | 13.1% / 1.96 / 51 | 34.6% / 2.12 / 41 | 1.1% / 0.23 / 47 | 0.9% / 0.13 / 74 |
| 167 | 1.0% / 0.16 / 31 | 4.1% / 1.00 / 16 | 16.6% / 1.48 / 22 | 12.7% / 2.34 / 18 | 3.3% / 0.31 / 47 |
| 168 | 0.4% / 0.09 / 40 | 4.8% / 0.82 / 24 | 22.9% / 1.51 / 30 | 11.5% / 1.76 / 26 | 3.6% / 0.31 / 65 |
| 169 | 4.4% / 0.64 / 32 | 2.1% / 0.55 / 17 | 13.9% / 1.36 / 22 | 13.9% / 3.53 / 19 | 1.0% / 0.15 / 47 |
| 170 | 2.6% / 0.41 / 24 | -0.4% / -0.11 / 11 | 11.0% / 1.28 / 14 | 6.5% / 2.07 / 11 | 7.7% / 0.85 / 41 |
| 171 | 6.5% / 1.06 / 90 | 8.3% / 1.70 / 78 | 22.7% / 1.81 / 77 | 3.6% / 0.81 / 79 | -8.5% / -0.93 / 107 |
| 172 | 5.7% / 0.62 / 28 | 7.6% / 1.07 / 25 | 10.1% / 0.92 / 21 | 9.7% / 1.66 / 28 | 2.4% / 0.26 / 44 |
| 173 | -2.9% / -0.33 / 43 | 3.7% / 0.70 / 32 | 9.1% / 1.01 / 29 | 9.2% / 1.88 / 35 | 12.9% / 1.10 / 63 |
| 174 | 5.0% / 0.92 / 53 | 4.4% / 1.25 / 46 | 5.3% / 0.85 / 37 | 4.2% / 1.17 / 41 | 12.7% / 1.46 / 88 |
| 175 | 8.5% / 0.94 / 30 | 4.4% / 0.90 / 19 | 3.3% / 0.29 / 24 | 7.7% / 1.50 / 20 | 13.6% / 1.02 / 53 |
| 176 | -8.9% / -1.22 / 57 | 15.4% / 2.26 / 51 | 29.9% / 1.75 / 41 | 0.7% / 0.15 / 47 | 5.5% / 0.53 / 72 |
| 177 | -3.8% / -0.33 / 30 | 7.0% / 1.03 / 25 | 28.0% / 1.94 / 27 | 6.8% / 1.06 / 31 | 4.4% / 0.41 / 47 |
| 178 | -2.3% / -0.17 / 26 | 6.9% / 1.06 / 17 | 16.9% / 1.22 / 24 | 15.1% / 2.26 / 25 | 8.6% / 0.70 / 43 |
| 179 | 3.2% / 0.40 / 20 | 6.0% / 1.08 / 22 | 12.0% / 1.48 / 16 | 10.0% / 1.89 / 16 | -0.7% / -0.00 / 36 |
| 180 | 2.1% / 0.64 / 18 | 1.3% / 0.96 / 14 | 4.1% / 0.76 / 12 | 1.7% / 1.61 / 12 | 3.5% / 1.13 / 47 |
| 181 | 0.0% / 0.04 / 53 | 11.0% / 2.95 / 41 | 9.5% / 1.21 / 38 | 0.0% / 0.03 / 40 | 4.7% / 0.65 / 94 |
| 182 | 1.9% / 0.55 / 18 | 5.2% / 1.57 / 18 | 4.9% / 0.92 / 15 | 3.2% / 1.31 / 15 | 0.6% / 0.14 / 39 |
| 183 | 1.3% / 0.19 / 21 | 5.1% / 0.88 / 22 | 14.2% / 1.20 / 20 | 12.0% / 2.32 / 17 | 5.0% / 0.48 / 35 |
| 184 | 1.9% / 0.32 / 25 | 1.6% / 0.52 / 15 | 4.4% / 0.88 / 14 | 0.8% / 0.29 / 13 | 12.3% / 1.45 / 45 |
| 185 | 4.0% / 0.85 / 35 | 4.2% / 1.03 / 29 | 3.7% / 0.64 / 22 | 3.5% / 1.05 / 26 | 7.2% / 0.80 / 59 |
| 186 | 1.9% / 0.58 / 18 | 1.2% / 0.90 / 14 | 4.1% / 0.76 / 12 | 1.8% / 1.61 / 12 | 3.3% / 1.11 / 47 |
| 187 | -2.2% / -0.25 / 38 | 8.5% / 2.15 / 33 | 16.2% / 1.27 / 33 | 6.1% / 1.45 / 31 | 4.8% / 0.47 / 64 |
| 188 | 2.9% / 0.35 / 20 | 7.9% / 1.29 / 22 | 11.7% / 1.35 / 16 | 10.9% / 2.03 / 16 | 2.2% / 0.23 / 35 |
| 189 | 5.0% / 0.59 / 30 | 4.4% / 1.88 / 6 | 1.4% / 0.19 / 17 | 4.0% / 1.07 / 14 | 15.1% / 1.48 / 39 |
| 190 | 2.1% / 0.28 / 21 | 0.9% / 0.18 / 17 | 20.0% / 1.86 / 18 | 9.8% / 2.12 / 14 | 1.3% / 0.17 / 36 |
| 191 | 4.3% / 0.77 / 44 | 7.9% / 1.74 / 38 | 10.9% / 1.44 / 25 | 2.5% / 0.66 / 30 | -0.4% / 0.01 / 71 |
| 192 | -0.7% / -0.04 / 38 | 6.3% / 1.86 / 17 | 14.5% / 1.36 / 22 | 12.1% / 2.26 / 21 | 4.4% / 0.49 / 49 |
| 193 | 6.7% / 1.09 / 89 | 8.5% / 1.73 / 78 | 24.9% / 1.94 / 76 | 1.6% / 0.37 / 79 | -10.1% / -1.15 / 106 |
| 194 | -0.2% / 0.02 / 38 | 6.0% / 1.78 / 17 | 14.6% / 1.37 / 22 | 12.0% / 2.21 / 21 | 1.7% / 0.22 / 49 |
| 195 | -9.7% / -1.42 / 36 | 3.2% / 0.70 / 32 | 21.9% / 2.21 / 32 | 7.4% / 1.73 / 35 | 10.1% / 1.12 / 50 |
| 196 | 7.7% / 0.95 / 29 | 0.4% / 0.16 / 7 | 16.2% / 1.21 / 20 | 6.1% / 1.63 / 16 | 6.2% / 0.61 / 48 |
| 197 | -0.7% / -0.12 / 52 | 12.1% / 3.17 / 41 | 8.8% / 1.16 / 38 | 0.1% / 0.04 / 40 | 4.2% / 0.59 / 94 |
| 198 | 2.9% / 0.53 / 49 | 2.5% / 0.66 / 42 | 4.5% / 0.66 / 33 | 3.8% / 0.97 / 39 | 11.1% / 1.07 / 84 |
| 199 | -10.1% / -1.57 / 36 | 3.1% / 0.67 / 32 | 20.0% / 2.08 / 32 | 7.7% / 1.87 / 35 | 9.0% / 1.03 / 50 |
| 200 | 2.6% / 0.81 / 20 | 1.4% / 1.36 / 14 | 1.8% / 0.35 / 14 | 5.1% / 2.56 / 13 | 1.7% / 0.51 / 47 |
| 201 | 2.6% / 0.81 / 20 | 1.4% / 1.36 / 14 | 1.8% / 0.35 / 14 | 5.1% / 2.56 / 13 | 1.7% / 0.51 / 47 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_d5cb` | 5 | 0.94 | 0.96/0.96 | 0.95/0.95 |
| 1 | `cfg_28ab` | 5 | 0.93 | 0.95/0.97 | 0.88/0.93 |
| 2 | `cfg_018e` | 5 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 3 | `cfg_5849` | 4 | 0.90 | 0.94/0.98 | 0.91/0.95 |
| 4 | `cfg_3786` | 2 | 0.91 | 0.90/0.90 | 0.82/0.82 |
| 5 | `cfg_7932` | 3 | 0.96 | 0.97/0.98 | 0.95/0.97 |
| 6 | `cfg_02d6` | 5 | 0.84 | 0.87/0.93 | 0.75/0.86 |
| 7 | `cfg_b73c` | 2 | 0.81 | 0.82/0.82 | 0.72/0.72 |
| 8 | `cfg_f328` | 3 | 0.90 | 0.90/0.92 | 0.82/0.87 |
| 9 | `cfg_632c` | 4 | 0.93 | 0.95/0.97 | 0.93/0.93 |
| 10 | `cfg_7e8f` | 2 | 0.87 | 0.98/0.98 | 0.97/0.97 |
| 11 | `cfg_4f4e` | 4 | 0.92 | 0.94/0.97 | 0.89/0.93 |
| 12 | `cfg_21aa` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 13 | `cfg_9aa3` | 5 | 0.98 | 0.99/0.99 | 0.94/0.99 |
| 14 | `cfg_acb3` | 10 | 0.84 | 0.87/0.88 | 0.68/0.75 |
| 15 | `cfg_cd73` | 5 | 0.90 | 0.91/0.95 | 0.84/0.92 |
| 16 | `cfg_9020` | 4 | 0.80 | 0.89/0.97 | 0.68/0.93 |
| 17 | `cfg_d6d2` | 5 | 0.86 | 0.86/0.93 | 0.75/0.82 |
| 18 | `cfg_52a1` | 6 | 0.83 | 0.81/0.97 | 0.80/0.88 |
| 19 | `cfg_4541` | 6 | 0.85 | 0.79/0.91 | 0.67/0.88 |
| 20 | `cfg_4220` | 4 | 0.91 | 0.97/0.99 | 0.90/0.98 |
| 21 | `cfg_133c` | 6 | 0.94 | 0.91/0.99 | 0.74/0.93 |
| 22 | `cfg_1223` | 5 | 0.89 | 0.92/0.96 | 0.78/0.90 |
| 23 | `cfg_1484` | 1 | n/a | n/a/n/a | n/a/n/a |
| 24 | `cfg_fb2f` | 10 | 0.81 | 0.79/0.81 | 0.56/0.57 |
| 25 | `cfg_4570` | 7 | 0.84 | 0.86/0.91 | 0.77/0.87 |
| 26 | `cfg_1752` | 3 | 0.92 | 0.92/0.95 | 0.88/0.93 |
| 27 | `cfg_50b3` | 5 | 0.95 | 0.98/0.99 | 0.98/0.99 |
| 28 | `cfg_17a2` | 5 | 0.85 | 0.70/0.82 | 0.56/0.75 |
| 29 | `cfg_17a8` | 7 | 0.82 | 0.82/0.85 | 0.71/0.77 |
| 30 | `cfg_e465` | 3 | 0.93 | 0.92/0.93 | 0.88/0.91 |
| 31 | `cfg_eab5` | 4 | 0.93 | 0.98/0.99 | 0.91/0.96 |
| 32 | `cfg_1d41` | 5 | 0.93 | 0.95/0.98 | 0.95/0.97 |
| 33 | `cfg_54bf` | 8 | 0.82 | 0.85/0.93 | 0.74/0.82 |
| 34 | `cfg_1fc3` | 5 | 0.88 | 0.82/0.98 | 0.68/0.92 |
| 35 | `cfg_f0ee` | 2 | 0.97 | 0.99/0.99 | 0.95/0.95 |
| 36 | `cfg_76c6` | 4 | 0.86 | 0.95/0.97 | 0.90/0.97 |
| 37 | `cfg_2437` | 5 | 0.87 | 0.91/0.96 | 0.79/0.87 |
| 38 | `cfg_4d88` | 4 | 0.87 | 0.97/0.97 | 0.96/0.96 |
| 39 | `cfg_2fea` | 2 | 0.93 | 0.94/0.94 | 0.91/0.91 |
| 40 | `cfg_26d7` | 5 | 0.94 | 0.96/0.98 | 0.86/0.91 |
| 41 | `cfg_ea18` | 3 | 0.98 | 0.99/0.99 | 0.98/0.99 |
| 42 | `cfg_98ab` | 4 | 0.82 | 0.89/0.97 | 0.79/0.93 |
| 43 | `cfg_27b7` | 3 | 0.93 | 0.91/0.94 | 0.79/0.85 |
| 44 | `cfg_bebf` | 3 | 0.81 | 0.92/0.94 | 0.74/0.84 |
| 45 | `cfg_e746` | 2 | 0.99 | 0.98/0.98 | 0.98/0.98 |
| 46 | `cfg_e54c` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 47 | `cfg_3fc1` | 4 | 0.91 | 0.94/0.98 | 0.90/0.94 |
| 48 | `cfg_b73e` | 4 | 0.85 | 0.90/0.93 | 0.77/0.79 |
| 49 | `cfg_2e49` | 6 | 0.81 | 0.86/0.96 | 0.86/0.99 |
| 50 | `cfg_2b5f` | 3 | 0.91 | 0.95/0.97 | 0.94/0.95 |
| 51 | `cfg_3afa` | 5 | 0.96 | 0.95/0.95 | 0.98/1.00 |
| 52 | `cfg_e550` | 2 | 0.89 | 0.95/0.95 | 0.93/0.93 |
| 53 | `cfg_9ff3` | 2 | 0.89 | 0.96/0.96 | 0.94/0.94 |
| 54 | `cfg_7a6c` | 5 | 0.87 | 0.90/0.95 | 0.78/0.90 |
| 55 | `cfg_31ed` | 2 | 0.96 | 0.97/0.97 | 0.93/0.93 |
| 56 | `cfg_34a7` | 2 | 0.89 | 0.92/0.92 | 0.87/0.87 |
| 57 | `cfg_352d` | 5 | 0.93 | 0.97/0.97 | 0.89/0.94 |
| 58 | `cfg_b3ff` | 5 | 0.95 | 0.97/0.97 | 0.93/0.93 |
| 59 | `cfg_6421` | 5 | 0.92 | 0.96/0.96 | 0.90/0.94 |
| 60 | `cfg_9c5a` | 2 | 0.90 | 0.95/0.95 | 0.90/0.90 |
| 61 | `cfg_3c0b` | 4 | 0.95 | 0.99/0.99 | 0.97/0.99 |
| 62 | `cfg_3c6f` | 2 | 0.96 | 0.98/0.98 | 0.94/0.94 |
| 63 | `cfg_3e55` | 2 | 0.96 | 0.94/0.94 | 0.80/0.80 |
| 64 | `cfg_bada` | 5 | 0.94 | 0.97/0.97 | 0.97/0.97 |
| 65 | `cfg_b3b8` | 5 | 0.97 | 0.99/1.00 | 0.98/0.99 |
| 66 | `cfg_485f` | 1 | n/a | n/a/n/a | n/a/n/a |
| 67 | `cfg_8359` | 6 | 0.82 | 0.78/0.87 | 0.62/0.65 |
| 68 | `cfg_cfe7` | 4 | 0.87 | 0.83/0.96 | 0.71/0.90 |
| 69 | `cfg_ea9b` | 4 | 0.93 | 0.94/0.94 | 0.89/0.90 |
| 70 | `cfg_eb2b` | 4 | 0.86 | 0.92/0.93 | 0.76/0.78 |
| 71 | `cfg_c5fa` | 5 | 0.87 | 0.97/0.98 | 0.94/0.95 |
| 72 | `cfg_9b31` | 2 | 0.91 | 0.95/0.95 | 0.97/0.97 |
| 73 | `cfg_ad33` | 6 | 0.88 | 0.91/0.92 | 0.75/0.79 |
| 74 | `cfg_590f` | 1 | n/a | n/a/n/a | n/a/n/a |
| 75 | `cfg_9edc` | 2 | 0.96 | 0.98/0.98 | 0.95/0.95 |
| 76 | `cfg_7648` | 4 | 0.91 | 0.95/0.97 | 0.90/0.97 |
| 77 | `cfg_6564` | 5 | 0.85 | 0.90/0.93 | 0.90/0.90 |
| 78 | `cfg_61e1` | 3 | 0.89 | 0.86/0.87 | 0.80/0.81 |
| 79 | `cfg_624c` | 1 | n/a | n/a/n/a | n/a/n/a |
| 80 | `cfg_c00f` | 2 | 0.98 | 0.99/0.99 | 0.99/0.99 |
| 81 | `cfg_6646` | 4 | 0.95 | 0.98/0.99 | 0.99/0.99 |
| 82 | `cfg_6897` | 1 | n/a | n/a/n/a | n/a/n/a |
| 83 | `cfg_6aca` | 5 | 0.99 | 0.99/1.00 | 0.99/0.99 |
| 84 | `cfg_6bd1` | 2 | 0.99 | 0.99/0.99 | 0.97/0.97 |
| 85 | `cfg_c73b` | 6 | 0.82 | 0.87/0.94 | 0.68/0.84 |
| 86 | `cfg_6f20` | 1 | n/a | n/a/n/a | n/a/n/a |
| 87 | `cfg_c89b` | 2 | 0.94 | 0.94/0.94 | 0.93/0.93 |
| 88 | `cfg_7319` | 1 | n/a | n/a/n/a | n/a/n/a |
| 89 | `cfg_bf51` | 3 | 0.99 | 0.99/1.00 | 0.97/0.98 |
| 90 | `cfg_c58e` | 4 | 0.90 | 0.82/0.95 | 0.86/0.90 |
| 91 | `cfg_8130` | 2 | 0.96 | 0.97/0.97 | 0.97/0.97 |
| 92 | `cfg_817f` | 1 | n/a | n/a/n/a | n/a/n/a |
| 93 | `cfg_8ed5` | 3 | 0.92 | 0.96/0.96 | 0.91/0.92 |
| 94 | `cfg_9862` | 1 | n/a | n/a/n/a | n/a/n/a |
| 95 | `cfg_9c5c` | 1 | n/a | n/a/n/a | n/a/n/a |
| 96 | `cfg_9f87` | 1 | n/a | n/a/n/a | n/a/n/a |
| 97 | `cfg_a571` | 1 | n/a | n/a/n/a | n/a/n/a |
| 98 | `cfg_acb1` | 1 | n/a | n/a/n/a | n/a/n/a |
| 99 | `cfg_c2d9` | 3 | 0.95 | 0.97/0.98 | 0.98/0.98 |
| 100 | `cfg_b42e` | 2 | 0.92 | 0.95/0.95 | 0.93/0.93 |
| 101 | `cfg_b8af` | 3 | 0.97 | 0.95/0.97 | 0.94/0.97 |
| 102 | `cfg_bee3` | 1 | n/a | n/a/n/a | n/a/n/a |
| 103 | `cfg_e998` | 2 | 0.95 | 0.95/0.95 | 0.92/0.92 |
| 104 | `cfg_c580` | 1 | n/a | n/a/n/a | n/a/n/a |
| 105 | `cfg_e741` | 2 | 0.81 | 0.78/0.78 | 0.64/0.64 |
| 106 | `cfg_f012` | 3 | 0.89 | 0.94/0.95 | 0.88/0.90 |
| 107 | `cfg_e19e` | 1 | n/a | n/a/n/a | n/a/n/a |
| 108 | `cfg_e484` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.268e-03 over 20310 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 986.0, participation ratio 31.4, 95%-variance components 275 (rank bound T = 1259); raw grid 21600; raw + known prior 577032
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
