# Screening funnel -- mr_nq_v7_1h (development stages only)

- Code: `5342a94cdc84` (dirty working tree: True, diff sha256 `4a857123c444`)
- Config: `configs/funnel/mr_funnel_nq_v7_1h.yaml` sha256 `8e6063f9364d137d`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'NQ': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `f1024d58e29e862d` (153 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_nq_v5 gated 93 NQ candidates on 2023-2024 (38 passed), mr_nq_v6 was narrowed around those survivors, and this v7 grid was chosen after reading both, so NQ 2023-2024 is largely in-sample for v7. The grid, the stage-4 test and the 40-trade rule were also shaped by ES 2023-2024 (mr_es_v3..v5).
- Holdout 2025+ previously inspected: **False** -- No NQ strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection), and two ES strategies (mr_es_v6_1h #8, #15; a correlated index) were scored on the ES 2025+ holdout on 2026-10-24. The holdout is the only untouched test for this run.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 3456 | 3456 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 3456 | 3456 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 3456 | 901 | 2555 | 0 |  | 1239 | 26.07 | 26.07 |  |
| 3 performance & risk | hard_gate | 901 | 214 | 687 | 0 |  | 0 | 6.19 | 23.75 |  |
| 4 parameter stability | hard_gate | 214 | 214 | 0 | 0 |  | 0 | 6.19 | 100.00 |  |
| 5 time stability | hard_gate | 214 | 214 | 0 | 0 |  | 202 | 6.19 | 100.00 |  |
| 6 deduplication | dedup | 214 | 153 |  |  | 61 |  | 4.43 | 71.50 | best 2 per cluster |
| 7 execution stress | hard_gate | 153 | 153 | 0 | 0 |  | 4 | 4.43 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 153 |  |  |  |  |  |  |  | diagnostic only: unverified: 153 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 2555 |
| s2:hard_reject:years_with_>=10_trades | 2222 |
| s3:hard_reject:net_return | 63 |
| s3:hard_reject:sharpe | 687 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_5ee1` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 21/63/24 | 108 | 50.9% | 8.6% | 1.15 | -7.7% | 190 | 2.10 | 6.0% | 54.8 | 9/9 | 1.00 | 0.92 | 0.23 | 5 | 22.2% | 0.56 | 0.42 | 50.4% | 49.9% | 12.9% | 46.0%/36.5% | n/a (profitable_beyond_25.0x) | pass | 0.289 (unverified) | 0.87 |
| 2 | `cfg_b6a3` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=9, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 21/64/32 | 117 | 44.8% | 7.7% | 1.11 | -5.6% | 209 | 1.88 | 6.6% | 60.3 | 8/8 | 1.00 | 0.96 | 0.15 | 5 | 27.9% | 0.38 | 0.44 | 44.4% | 43.9% | 29.0% | 41.9%/34.5% | n/a (profitable_beyond_25.0x) | pass | 0.230 (unverified) | 0.68 |
| 3 | `cfg_4b85` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=9, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 41/53/51 | 145 | 72.1% | 11.5% | 1.22 | -7.2% | 147 | 1.84 | 10.4% | 75.6 | 8/8 | 1.00 | 0.97 | 0.25 | 5 | 44.5% | 0.38 | 0.36 | 70.8% | 70.2% | 22.1% | 63.3%/52.9% | n/a (profitable_beyond_25.0x) | pass | 0.339 (unverified) | 0.22 |
| 4 | `cfg_1c62` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=9, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 38/41/41 | 120 | 59.3% | 9.8% | 1.24 | -8.6% | 275 | 1.83 | 8.6% | 63.4 | 9/9 | 1.00 | 1.02 | 0.22 | 5 | 41.4% | 0.30 | 0.42 | 57.7% | 57.7% | 19.7% | 55.5%/46.0% | n/a (profitable_beyond_25.0x) | pass | 0.347 (unverified) | 0.51 |
| 5 | `cfg_5e0f` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 27/57/30 | 114 | 65.5% | 10.6% | 1.31 | -6.0% | 143 | 2.12 | 6.2% | 60.5 | 8/8 | 1.00 | 0.99 | 0.32 | 5 | 35.5% | 0.46 | 0.39 | 64.8% | 61.5% | 17.7% | 55.7%/43.4% | n/a (profitable_beyond_25.0x) | pass | 0.416 (unverified) | 0.62 |
| 6 | `cfg_1c51` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=9, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 61/34/50 | 145 | 61.8% | 10.1% | 1.14 | -7.2% | 214 | 1.74 | 9.5% | 76.2 | 8/8 | 1.00 | 0.92 | 0.21 | 5 | 41.3% | 0.33 | 0.40 | 61.5% | 59.9% | 23.8% | 55.7%/45.2% | n/a (profitable_beyond_25.0x) | pass | 0.279 (unverified) | 0.18 |
| 7 | `cfg_f19c` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 60/43/56 | 159 | 64.9% | 10.5% | 1.13 | -6.9% | 147 | 1.62 | 11.1% | 82.2 | 9/9 | 1.00 | 1.02 | 0.10 | 5 | 38.7% | 0.34 | 0.39 | 63.7% | 61.8% | 29.6% | 58.2%/46.9% | n/a (profitable_beyond_25.0x) | pass | 0.267 (unverified) | 0.22 |
| 8 | `cfg_faa3` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 35/50/24 | 109 | 45.9% | 7.9% | 1.08 | -7.7% | 190 | 2.00 | 5.8% | 55.3 | 9/9 | 1.00 | 0.83 | 0.24 | 5 | 21.9% | 0.52 | 0.43 | 45.3% | 44.9% | 10.5% | 41.4%/31.5% | n/a (profitable_beyond_25.0x) | pass | 0.240 (unverified) | 0.77 |
| 9 | `cfg_6615` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 51/56/58 | 165 | 60.8% | 10.0% | 1.06 | -7.3% | 147 | 1.60 | 11.9% | 86.0 | 10/10 | 1.00 | 0.90 | 0.16 | 5 | 40.4% | 0.31 | 0.41 | 59.5% | 58.7% | 23.0% | 53.4%/43.9% | n/a (profitable_beyond_25.0x) | pass | 0.223 (unverified) | 0.17 |
| 10 | `cfg_feb6` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 42/33/39 | 114 | 64.6% | 10.5% | 1.17 | -9.3% | 182 | 1.86 | 7.8% | 60.6 | 9/9 | 1.00 | 0.88 | 0.29 | 5 | 39.3% | 0.39 | 0.41 | 62.5% | 62.0% | 12.5% | 53.8%/44.6% | n/a (profitable_beyond_25.0x) | pass | 0.298 (unverified) | 0.37 |
| 11 | `cfg_3f81` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 22/50/30 | 102 | 37.9% | 6.6% | 1.03 | -5.9% | 314 | 1.78 | 5.5% | 51.9 | 8/8 | 1.00 | 0.92 | 0.11 | 4 | 21.5% | 0.43 | 0.53 | 37.9% | 38.0% | 11.5% | 34.1%/24.1% | n/a (profitable_beyond_25.0x) | pass | 0.179 (unverified) | 1.01 |
| 12 | `cfg_bf72` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=9, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 19/81/40 | 140 | 49.3% | 8.4% | 1.01 | -6.9% | 205 | 1.77 | 7.8% | 71.1 | 7/7 | 1.00 | 0.95 | 0.06 | 5 | 22.0% | 0.55 | 0.44 | 48.6% | 48.3% | 28.3% | 45.8%/35.0% | n/a (profitable_beyond_25.0x) | pass | 0.177 (unverified) | 0.56 |
| 13 | `cfg_4530` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 27/76/39 | 142 | 59.0% | 9.7% | 1.22 | -5.4% | 199 | 1.86 | 8.0% | 73.5 | 9/9 | 1.00 | 0.85 | 0.37 | 5 | 29.6% | 0.42 | 0.39 | 58.3% | 57.3% | 14.9% | 52.3%/43.2% | n/a (profitable_beyond_25.0x) | pass | 0.324 (unverified) | 0.52 |
| 14 | `cfg_a082` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=9, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 32/53/32 | 117 | 39.9% | 7.0% | 1.03 | -5.6% | 209 | 1.80 | 6.3% | 60.3 | 8/8 | 1.00 | 0.89 | 0.14 | 5 | 25.4% | 0.36 | 0.48 | 38.4% | 37.8% | 22.0% | 35.9%/26.5% | n/a (profitable_beyond_25.0x) | pass | 0.175 (unverified) | 0.88 |
| 15 | `cfg_b94b` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 61/35/52 | 148 | 66.5% | 10.7% | 1.14 | -6.6% | 212 | 1.71 | 9.8% | 77.2 | 9/9 | 1.00 | 0.90 | 0.24 | 5 | 38.7% | 0.34 | 0.37 | 65.8% | 64.7% | 32.7% | 61.4%/51.9% | n/a (profitable_beyond_25.0x) | pass | 0.280 (unverified) | 0.35 |
| 16 | `cfg_7c72` | timeframe=1h, mean_type=ema, mean_lookback=23, std_lookback=6, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 100/21/60 | 181 | 68.9% | 11.1% | 1.07 | -10.1% | 269 | 1.54 | 13.8% | 92.9 | 7/7 | 1.00 | 0.92 | 0.15 | 4 | 32.0% | 0.44 | 0.41 | 68.1% | 67.3% | 39.8% | 60.0%/48.7% | n/a (profitable_beyond_25.0x) | pass | 0.224 (unverified) | 0.29 |
| 17 | `cfg_f30f` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 43/64/36 | 143 | 57.6% | 9.5% | 1.05 | -7.4% | 145 | 1.67 | 11.3% | 74.6 | 11/11 | 1.00 | 0.85 | 0.21 | 5 | 38.8% | 0.30 | 0.43 | 56.8% | 56.3% | 44.2% | 53.4%/42.4% | n/a (profitable_beyond_25.0x) | pass | 0.222 (unverified) | 0.05 |
| 18 | `cfg_02a0` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 49/46/53 | 148 | 55.5% | 9.2% | 1.13 | -6.1% | 165 | 1.60 | 10.4% | 77.3 | 10/10 | 1.00 | 0.86 | 0.27 | 5 | 32.5% | 0.35 | 0.45 | 55.2% | 54.9% | 18.8% | 51.3%/39.1% | n/a (profitable_beyond_25.0x) | pass | 0.263 (unverified) | 0.48 |
| 19 | `cfg_d64d` | timeframe=1h, mean_type=ema, mean_lookback=23, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 36/48/32 | 116 | 44.2% | 7.6% | 1.02 | -6.6% | 205 | 1.80 | 6.4% | 59.9 | 7/7 | 1.00 | 0.81 | 0.21 | 5 | 19.5% | 0.49 | 0.45 | 43.7% | 43.4% | 11.1% | 38.9%/31.6% | n/a (profitable_beyond_25.0x) | pass | 0.174 (unverified) | 0.83 |
| 20 | `cfg_36b9` | timeframe=1h, mean_type=ema, mean_lookback=37, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 42/40/48 | 130 | 53.7% | 9.0% | 1.00 | -6.7% | 212 | 1.65 | 9.1% | 68.1 | 9/9 | 1.00 | 0.75 | 0.25 | 5 | 33.8% | 0.37 | 0.42 | 53.1% | 52.1% | 20.4% | 47.0%/35.4% | n/a (profitable_beyond_25.0x) | pass | 0.184 (unverified) | 0.38 |
| 21 | `cfg_b813` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=9, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 45/59/38 | 142 | 54.7% | 9.1% | 1.18 | -5.5% | 249 | 1.83 | 7.6% | 73.7 | 9/9 | 1.00 | 0.83 | 0.34 | 5 | 24.0% | 0.48 | 0.41 | 53.4% | 52.4% | 7.2% | 46.1%/37.6% | n/a (profitable_beyond_25.0x) | pass | 0.285 (unverified) | 0.59 |
| 22 | `cfg_883c` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 76/15/78 | 169 | 69.1% | 11.1% | 1.02 | -7.4% | 249 | 1.54 | 13.1% | 88.7 | 8/8 | 1.00 | 0.93 | 0.10 | 4 | 36.1% | 0.37 | 0.40 | 65.5% | 65.0% | 42.8% | 59.3%/48.1% | n/a (profitable_beyond_25.0x) | pass | 0.195 (unverified) | 0.43 |
| 23 | `cfg_2db3` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 40/29/43 | 112 | 54.3% | 9.1% | 1.14 | -5.9% | 216 | 1.77 | 7.5% | 58.9 | 10/10 | 1.00 | 0.92 | 0.22 | 5 | 33.8% | 0.38 | 0.42 | 53.4% | 51.3% | 17.8% | 42.8%/34.9% | n/a (profitable_beyond_25.0x) | pass | 0.266 (unverified) | 0.39 |
| 24 | `cfg_2017` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 47/58/61 | 166 | 59.3% | 9.8% | 0.99 | -12.9% | 140 | 1.52 | 12.0% | 86.8 | 9/9 | 1.00 | 0.75 | 0.24 | 5 | 38.4% | 0.31 | 0.42 | 58.5% | 55.3% | 9.9% | 51.7%/38.0% | n/a (profitable_beyond_25.0x) | pass | 0.179 (unverified) | 0.16 |
| 25 | `cfg_512e` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=9, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 36/47/30 | 113 | 47.1% | 8.0% | 1.02 | -7.7% | 255 | 1.68 | 8.6% | 58.7 | 10/10 | 1.00 | 0.81 | 0.21 | 5 | 30.1% | 0.30 | 0.49 | 47.0% | 47.1% | 37.7% | 43.5%/33.3% | n/a (profitable_beyond_25.0x) | pass | 0.185 (unverified) | 0.37 |
| 26 | `cfg_9f03` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=6, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 49/77/49 | 175 | 57.0% | 9.4% | 0.97 | -8.7% | 153 | 1.52 | 13.6% | 89.6 | 8/8 | 1.00 | 0.80 | 0.17 | 5 | 30.5% | 0.40 | 0.38 | 55.7% | 54.8% | 29.7% | 55.6%/44.7% | n/a (profitable_beyond_25.0x) | pass | 0.161 (unverified) | 0.76 |
| 27 | `cfg_1dcc` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=6, entry_z=-2.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 99/18/51 | 168 | 71.0% | 11.3% | 1.10 | -9.1% | 384 | 1.59 | 11.9% | 87.4 | 9/9 | 1.00 | 0.73 | 0.37 | 5 | 25.8% | 0.54 | 0.42 | 71.5% | 68.6% | 47.4% | 58.7%/49.0% | n/a (profitable_beyond_25.0x) | pass | 0.239 (unverified) | 0.68 |
| 28 | `cfg_2fc7` | timeframe=1h, mean_type=ema, mean_lookback=37, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 49/51/60 | 160 | 57.2% | 9.5% | 0.99 | -7.4% | 147 | 1.52 | 11.4% | 82.6 | 8/8 | 1.00 | 0.81 | 0.18 | 5 | 31.9% | 0.39 | 0.47 | 53.7% | 52.5% | 31.0% | 53.4%/44.3% | n/a (profitable_beyond_25.0x) | pass | 0.174 (unverified) | 0.04 |
| 29 | `cfg_2446` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 64/35/49 | 148 | 63.9% | 10.4% | 0.99 | -8.3% | 165 | 1.64 | 13.9% | 77.1 | 10/10 | 1.00 | 0.89 | 0.10 | 4 | 40.9% | 0.36 | 0.40 | 63.1% | 60.0% | 36.8% | 56.2%/45.7% | n/a (profitable_beyond_25.0x) | pass | 0.175 (unverified) | 0.28 |
| 30 | `cfg_6722` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 32/44/36 | 112 | 43.6% | 7.5% | 0.92 | -9.0% | 343 | 1.71 | 8.1% | 57.4 | 10/10 | 1.00 | 0.79 | 0.13 | 4 | 23.3% | 0.47 | 0.49 | 43.1% | 42.7% | 3.1% | 40.8%/33.2% | n/a (profitable_beyond_25.0x) | pass | 0.138 (unverified) | 0.71 |
| 31 | `cfg_f828` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 63/20/67 | 150 | 57.2% | 9.5% | 1.00 | -7.7% | 331 | 1.52 | 12.1% | 78.2 | 9/9 | 1.00 | 0.80 | 0.20 | 5 | 27.7% | 0.42 | 0.45 | 55.6% | 55.2% | 29.0% | 50.8%/39.7% | n/a (profitable_beyond_25.0x) | pass | 0.178 (unverified) | 0.43 |
| 32 | `cfg_4f13` | timeframe=1h, mean_type=sma, mean_lookback=23, std_lookback=12, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 54/40/30 | 124 | 39.7% | 6.9% | 1.12 | -6.5% | 462 | 1.74 | 6.2% | 63.9 | 7/7 | 1.00 | 0.73 | 0.39 | 4 | 19.6% | 0.43 | 0.47 | 39.6% | 38.7% | 7.7% | 35.5%/28.7% | n/a (profitable_beyond_25.0x) | pass | 0.256 (unverified) | 0.54 |
| 33 | `cfg_3b5e` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=6, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 73/55/47 | 175 | 61.0% | 10.0% | 1.04 | -7.0% | 173 | 1.55 | 12.5% | 91.0 | 8/8 | 1.00 | 0.79 | 0.25 | 4 | 27.6% | 0.49 | 0.37 | 60.7% | 57.9% | 32.0% | 55.8%/47.5% | n/a (profitable_beyond_25.0x) | pass | 0.203 (unverified) | 0.80 |
| 34 | `cfg_c4a5` | timeframe=1h, mean_type=ema, mean_lookback=23, std_lookback=9, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 59/28/30 | 117 | 39.1% | 6.8% | 1.03 | -8.0% | 427 | 1.77 | 5.6% | 59.8 | 7/7 | 1.00 | 0.84 | 0.20 | 4 | 16.6% | 0.49 | 0.45 | 38.8% | 38.1% | 13.0% | 33.2%/23.3% | n/a (profitable_beyond_25.0x) | pass | 0.186 (unverified) | 0.67 |
| 35 | `cfg_21ad` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 41/65/39 | 145 | 54.7% | 9.1% | 0.99 | -13.4% | 141 | 1.58 | 11.4% | 75.0 | 10/10 | 1.00 | 0.73 | 0.26 | 5 | 37.0% | 0.32 | 0.44 | 54.3% | 54.1% | 26.8% | 46.2%/34.4% | n/a (profitable_beyond_25.0x) | pass | 0.182 (unverified) | 0.11 |
| 36 | `cfg_a54a` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 97/40/66 | 203 | 70.2% | 11.2% | 1.04 | -12.7% | 258 | 1.49 | 17.5% | 106.2 | 9/9 | 1.00 | 0.86 | 0.18 | 5 | 44.4% | 0.37 | 0.35 | 69.5% | 68.2% | 33.1% | 61.0%/50.1% | n/a (profitable_beyond_25.0x) | pass | 0.213 (unverified) | 0.55 |
| 37 | `cfg_2989` | timeframe=1h, mean_type=ema, mean_lookback=23, std_lookback=6, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 101/14/87 | 202 | 61.5% | 10.1% | 0.98 | -12.0% | 388 | 1.44 | 13.4% | 105.7 | 6/6 | 1.00 | 0.86 | 0.11 | 4 | 26.9% | 0.46 | 0.45 | 59.3% | 57.9% | 31.8% | 54.0%/41.1% | n/a (profitable_beyond_25.0x) | pass | 0.163 (unverified) | 0.26 |
| 38 | `cfg_6dcc` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=9, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 42/58/40 | 140 | 46.2% | 7.9% | 0.95 | -7.7% | 204 | 1.73 | 7.5% | 71.0 | 7/7 | 1.00 | 1.01 | -0.06 | 5 | 22.8% | 0.51 | 0.46 | 46.2% | 45.9% | 26.3% | 42.1%/33.1% | n/a (profitable_beyond_25.0x) | pass | 0.146 (unverified) | 0.57 |
| 39 | `cfg_042c` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 49/36/30 | 115 | 49.4% | 8.4% | 1.12 | -6.1% | 131 | 1.91 | 5.7% | 59.8 | 8/8 | 1.00 | 0.84 | 0.28 | 5 | 26.2% | 0.47 | 0.41 | 48.9% | 46.9% | 7.8% | 40.5%/27.2% | n/a (profitable_beyond_25.0x) | pass | 0.265 (unverified) | 0.48 |
| 40 | `cfg_6131` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 34/76/46 | 156 | 53.4% | 8.9% | 0.99 | -7.5% | 311 | 1.68 | 8.6% | 81.0 | 8/8 | 1.00 | 0.89 | 0.10 | 5 | 24.4% | 0.46 | 0.42 | 51.3% | 49.1% | 29.0% | 48.8%/37.5% | n/a (profitable_beyond_25.0x) | pass | 0.170 (unverified) | 0.41 |
| 41 | `cfg_d9e5` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=9, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 52/17/55 | 124 | 50.1% | 8.5% | 0.94 | -11.2% | 275 | 1.59 | 10.0% | 65.1 | 8/8 | 1.00 | 0.78 | 0.16 | 5 | 28.7% | 0.34 | 0.48 | 45.8% | 44.4% | 21.0% | 44.1%/35.4% | n/a (profitable_beyond_25.0x) | pass | 0.139 (unverified) | 0.65 |
| 42 | `cfg_586b` | timeframe=1h, mean_type=ema, mean_lookback=37, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 42/59/36 | 137 | 54.6% | 9.1% | 1.01 | -7.7% | 156 | 1.59 | 10.9% | 70.4 | 9/9 | 1.00 | 0.72 | 0.29 | 5 | 33.9% | 0.33 | 0.50 | 53.4% | 53.2% | 37.1% | 49.8%/43.2% | n/a (profitable_beyond_25.0x) | pass | 0.187 (unverified) | 0.21 |
| 43 | `cfg_30b0` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 61/26/50 | 137 | 53.1% | 8.9% | 0.95 | -8.2% | 312 | 1.54 | 12.4% | 70.7 | 10/10 | 1.00 | 0.79 | 0.16 | 4 | 26.6% | 0.41 | 0.46 | 53.1% | 51.4% | 28.8% | 45.6%/36.7% | n/a (profitable_beyond_25.0x) | pass | 0.154 (unverified) | 0.39 |
| 44 | `cfg_06a9` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 54/21/51 | 126 | 54.4% | 9.1% | 1.01 | -7.1% | 170 | 1.62 | 10.9% | 65.3 | 8/8 | 1.00 | 0.79 | 0.23 | 4 | 22.0% | 0.51 | 0.49 | 53.9% | 53.5% | 19.4% | 48.0%/36.2% | n/a (profitable_beyond_25.0x) | pass | 0.182 (unverified) | 0.71 |
| 45 | `cfg_4cf2` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 24/86/42 | 152 | 45.5% | 7.8% | 0.90 | -8.8% | 315 | 1.63 | 8.7% | 77.4 | 8/8 | 1.00 | 0.80 | 0.10 | 4 | 24.0% | 0.39 | 0.47 | 43.4% | 42.4% | 13.3% | 40.7%/28.6% | n/a (profitable_beyond_25.0x) | pass | 0.120 (unverified) | 0.47 |
| 46 | `cfg_306b` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=6, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 53/71/72 | 196 | 55.1% | 9.2% | 0.90 | -7.6% | 138 | 1.43 | 13.8% | 100.8 | 7/7 | 1.00 | 0.85 | 0.05 | 5 | 32.3% | 0.36 | 0.45 | 53.4% | 51.5% | 15.2% | 52.0%/42.4% | n/a (profitable_beyond_25.0x) | pass | 0.129 (unverified) | 0.57 |
| 47 | `cfg_1d30` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 68/27/73 | 168 | 55.1% | 9.2% | 0.87 | -8.0% | 211 | 1.45 | 14.0% | 87.7 | 9/9 | 1.00 | 0.82 | 0.06 | 5 | 28.3% | 0.40 | 0.45 | 54.6% | 54.0% | 32.8% | 53.8%/42.0% | n/a (profitable_beyond_25.0x) | pass | 0.115 (unverified) | 0.44 |
| 48 | `cfg_d8c0` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 35/69/44 | 148 | 58.6% | 9.7% | 1.07 | -10.5% | 420 | 1.82 | 8.0% | 77.0 | 8/8 | 1.00 | 0.99 | 0.08 | 4 | 27.2% | 0.43 | 0.40 | 58.0% | 57.6% | 39.1% | 51.6%/39.4% | n/a (profitable_beyond_25.0x) | pass | 0.221 (unverified) | 0.51 |
| 49 | `cfg_7ffe` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=6, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 100/31/61 | 192 | 77.7% | 12.2% | 1.05 | -10.6% | 244 | 1.53 | 16.1% | 100.8 | 8/8 | 1.00 | 0.87 | 0.17 | 5 | 48.9% | 0.34 | 0.37 | 76.0% | 74.3% | 42.2% | 71.3%/60.6% | n/a (profitable_beyond_25.0x) | pass | 0.213 (unverified) | 0.72 |
| 50 | `cfg_8113` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 73/12/68 | 153 | 63.1% | 10.3% | 0.99 | -6.2% | 134 | 1.56 | 11.3% | 80.6 | 8/8 | 1.00 | 0.88 | 0.11 | 5 | 33.8% | 0.37 | 0.41 | 59.1% | 58.3% | 34.5% | 56.3%/40.8% | n/a (profitable_beyond_25.0x) | pass | 0.172 (unverified) | 0.42 |
| 51 | `cfg_29ff` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 85/52/63 | 200 | 66.9% | 10.8% | 0.96 | -12.4% | 258 | 1.47 | 18.4% | 103.8 | 9/9 | 0.89 | 0.94 | 0.01 | 5 | 43.7% | 0.35 | 0.39 | 66.0% | 65.1% | 32.0% | 61.5%/48.0% | n/a (profitable_beyond_25.0x) | pass | 0.164 (unverified) | 0.59 |
| 52 | `cfg_0e52` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 52/15/54 | 121 | 64.8% | 10.5% | 1.02 | -7.1% | 195 | 1.66 | 9.5% | 64.3 | 8/8 | 1.00 | 0.95 | 0.07 | 5 | 42.8% | 0.34 | 0.41 | 65.0% | 64.1% | 20.1% | 58.0%/43.8% | n/a (profitable_beyond_25.0x) | pass | 0.193 (unverified) | 0.58 |
| 53 | `cfg_95f8` | timeframe=1h, mean_type=ema, mean_lookback=23, std_lookback=6, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 84/45/51 | 180 | 66.8% | 10.8% | 1.08 | -6.1% | 156 | 1.56 | 12.2% | 93.1 | 8/8 | 1.00 | 0.86 | 0.22 | 5 | 28.5% | 0.50 | 0.42 | 66.2% | 61.6% | 55.9% | 56.6%/42.0% | n/a (profitable_beyond_25.0x) | pass | 0.231 (unverified) | 0.37 |
| 54 | `cfg_b761` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 78/32/52 | 162 | 71.5% | 11.4% | 0.99 | -10.2% | 353 | 1.58 | 14.0% | 84.6 | 9/9 | 1.00 | 0.78 | 0.21 | 5 | 45.5% | 0.32 | 0.40 | 71.2% | 70.7% | 49.4% | 61.5%/49.9% | n/a (profitable_beyond_25.0x) | pass | 0.178 (unverified) | 0.36 |
| 55 | `cfg_0d48` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 63/58/47 | 168 | 74.6% | 11.8% | 1.03 | -6.4% | 184 | 1.57 | 12.3% | 88.5 | 10/10 | 1.00 | 0.78 | 0.25 | 5 | 33.0% | 0.48 | 0.44 | 73.9% | 73.5% | 69.7% | 66.3%/52.9% | n/a (profitable_beyond_25.0x) | pass | 0.195 (unverified) | 0.40 |
| 56 | `cfg_680b` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=12, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 44/28/30 | 102 | 32.4% | 5.8% | 0.95 | -6.2% | 354 | 1.68 | 5.0% | 51.7 | 8/8 | 1.00 | 0.76 | 0.19 | 4 | 20.0% | 0.38 | 0.56 | 32.0% | 30.6% | 9.4% | 26.8%/20.3% | n/a (profitable_beyond_25.0x) | pass | 0.138 (unverified) | 0.82 |
| 57 | `cfg_d377` | timeframe=1h, mean_type=sma, mean_lookback=23, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 63/9/51 | 123 | 45.4% | 7.8% | 0.93 | -12.6% | 197 | 1.53 | 9.7% | 64.4 | 7/7 | 1.00 | 0.83 | 0.10 | 5 | 24.3% | 0.46 | 0.51 | 44.9% | 42.4% | 10.1% | 39.3%/30.0% | n/a (profitable_beyond_25.0x) | pass | 0.142 (unverified) | 0.43 |
| 58 | `cfg_9fed` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=6, entry_z=-2.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 104/10/76 | 190 | 57.4% | 9.5% | 0.91 | -9.0% | 388 | 1.44 | 11.8% | 98.7 | 8/8 | 1.00 | 0.64 | 0.26 | 5 | 22.1% | 0.52 | 0.46 | 56.9% | 56.1% | 36.9% | 51.3%/37.6% | n/a (profitable_beyond_25.0x) | pass | 0.129 (unverified) | 0.49 |
| 59 | `cfg_aee5` | timeframe=1h, mean_type=sma, mean_lookback=23, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 27/64/30 | 121 | 35.1% | 6.2% | 0.99 | -6.9% | 404 | 1.65 | 6.8% | 61.5 | 7/7 | 1.00 | 0.65 | 0.34 | 4 | 20.0% | 0.37 | 0.54 | 34.8% | 34.1% | 7.1% | 28.7%/20.8% | n/a (profitable_beyond_25.0x) | pass | 0.170 (unverified) | 0.75 |
| 60 | `cfg_49a9` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 36/29/39 | 104 | 35.5% | 6.3% | 0.88 | -8.3% | 375 | 1.58 | 6.9% | 53.2 | 9/9 | 0.89 | 0.87 | 0.01 | 4 | 22.6% | 0.36 | 0.60 | 35.1% | 34.6% | 8.1% | 32.4%/25.3% | n/a (profitable_beyond_25.0x) | pass | 0.108 (unverified) | 0.75 |
| 61 | `cfg_cfd4` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 18/74/36 | 128 | 38.7% | 6.8% | 0.94 | -7.8% | 314 | 1.59 | 7.3% | 65.8 | 8/8 | 1.00 | 0.75 | 0.19 | 5 | 12.0% | 0.64 | 0.63 | 38.3% | 37.9% | 2.6% | 33.5%/24.5% | n/a (profitable_beyond_25.0x) | pass | 0.136 (unverified) | 0.68 |
| 62 | `cfg_2642` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 46/12/49 | 107 | 42.2% | 7.3% | 0.87 | -7.1% | 218 | 1.53 | 8.2% | 55.9 | 8/8 | 0.88 | 0.76 | 0.11 | 5 | 29.5% | 0.30 | 0.55 | 42.0% | 40.0% | 12.6% | 36.9%/26.4% | n/a (profitable_beyond_25.0x) | pass | 0.109 (unverified) | 0.77 |
| 63 | `cfg_6af5` | timeframe=1h, mean_type=ema, mean_lookback=23, std_lookback=6, entry_z=-2.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 124/11/57 | 192 | 51.6% | 8.7% | 0.92 | -9.6% | 384 | 1.45 | 11.8% | 98.2 | 7/7 | 1.00 | 0.84 | 0.09 | 4 | 18.5% | 0.56 | 0.45 | 50.6% | 50.8% | 38.1% | 46.9%/35.6% | n/a (profitable_beyond_25.0x) | pass | 0.138 (unverified) | 0.63 |
| 64 | `cfg_9833` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 43/53/39 | 135 | 39.0% | 6.8% | 0.84 | -6.3% | 164 | 1.45 | 10.3% | 69.9 | 11/11 | 1.00 | 0.80 | 0.05 | 5 | 21.4% | 0.41 | 0.58 | 38.6% | 38.0% | 32.3% | 40.2%/28.4% | n/a (profitable_beyond_25.0x) | pass | 0.105 (unverified) | 0.33 |
| 65 | `cfg_08b6` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 54/24/40 | 118 | 51.0% | 8.6% | 0.95 | -10.0% | 374 | 1.59 | 11.2% | 61.1 | 9/9 | 1.00 | 0.75 | 0.20 | 4 | 17.4% | 0.57 | 0.51 | 50.7% | 49.5% | 35.4% | 45.4%/33.7% | n/a (profitable_beyond_25.0x) | pass | 0.147 (unverified) | 0.71 |
| 66 | `cfg_2397` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 15/91/45 | 151 | 44.3% | 7.6% | 0.92 | -5.7% | 198 | 1.54 | 8.5% | 78.2 | 7/7 | 1.00 | 0.70 | 0.22 | 5 | 18.0% | 0.52 | 0.56 | 42.9% | 42.5% | -4.2% | 40.5%/25.4% | n/a (profitable_beyond_25.0x) | pass | 0.121 (unverified) | 0.72 |
| 67 | `cfg_2874` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=6, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 105/21/91 | 217 | 66.4% | 10.7% | 0.89 | -10.5% | 172 | 1.41 | 15.9% | 113.2 | 7/7 | 1.00 | 0.85 | 0.05 | 5 | 40.4% | 0.37 | 0.41 | 63.1% | 63.0% | 33.0% | 60.7%/50.7% | n/a (profitable_beyond_25.0x) | pass | 0.130 (unverified) | 0.56 |
| 68 | `cfg_335b` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 65/80/52 | 197 | 62.8% | 10.2% | 0.94 | -7.7% | 108 | 1.51 | 14.8% | 100.2 | 10/10 | 1.00 | 0.83 | 0.12 | 5 | 37.1% | 0.36 | 0.41 | 61.9% | 61.6% | 21.5% | 60.0%/47.0% | n/a (profitable_beyond_25.0x) | pass | 0.147 (unverified) | 0.74 |
| 69 | `cfg_e3cc` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 20/56/36 | 112 | 39.3% | 6.9% | 0.93 | -6.1% | 286 | 1.69 | 6.1% | 57.7 | 9/9 | 1.00 | 0.84 | 0.09 | 4 | 18.6% | 0.45 | 0.54 | 38.8% | 37.5% | 32.3% | 33.8%/26.8% | n/a (profitable_beyond_25.0x) | pass | 0.123 (unverified) | 0.38 |
| 70 | `cfg_ee3c` | timeframe=1h, mean_type=sma, mean_lookback=23, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 62/14/37 | 113 | 43.0% | 7.4% | 0.89 | -8.8% | 443 | 1.58 | 9.9% | 59.0 | 8/8 | 1.00 | 0.75 | 0.14 | 4 | 20.7% | 0.50 | 0.52 | 42.6% | 41.7% | 19.7% | 37.8%/29.4% | n/a (profitable_beyond_25.0x) | pass | 0.122 (unverified) | 0.49 |
| 71 | `cfg_4631` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=6, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 62/59/77 | 198 | 50.0% | 8.5% | 0.85 | -7.7% | 93 | 1.39 | 13.2% | 102.5 | 8/8 | 1.00 | 0.84 | 0.01 | 5 | 24.8% | 0.44 | 0.48 | 49.1% | 47.0% | 6.8% | 46.5%/36.8% | n/a (profitable_beyond_25.0x) | pass | 0.105 (unverified) | 0.45 |
| 72 | `cfg_a77e` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=6, entry_z=-2.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 107/35/65 | 207 | 67.6% | 10.9% | 1.05 | -11.5% | 172 | 1.49 | 16.5% | 106.1 | 9/9 | 0.89 | 0.86 | 0.19 | 4 | 39.7% | 0.32 | 0.35 | 66.6% | 64.0% | 23.8% | 55.1%/48.2% | n/a (profitable_beyond_25.0x) | pass | 0.220 (unverified) | 0.93 |
| 73 | `cfg_3e1c` | timeframe=1h, mean_type=sma, mean_lookback=23, std_lookback=9, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 43/37/34 | 114 | 30.7% | 5.5% | 0.84 | -6.9% | 348 | 1.59 | 5.8% | 58.0 | 8/8 | 1.00 | 0.62 | 0.23 | 5 | 15.5% | 0.44 | 0.59 | 30.3% | 29.9% | 9.9% | 25.7%/18.1% | n/a (profitable_beyond_25.0x) | pass | 0.089 (unverified) | 0.59 |
| 74 | `cfg_e14d` | timeframe=1h, mean_type=ema, mean_lookback=23, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 48/29/40 | 117 | 37.2% | 6.5% | 0.90 | -7.9% | 336 | 1.56 | 7.7% | 60.2 | 8/8 | 1.00 | 0.85 | 0.05 | 5 | 19.4% | 0.42 | 0.54 | 36.0% | 35.5% | 6.9% | 32.6%/22.2% | n/a (profitable_beyond_25.0x) | pass | 0.126 (unverified) | 0.68 |
| 75 | `cfg_fa64` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=6, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 87/38/46 | 171 | 57.5% | 9.5% | 0.88 | -8.3% | 353 | 1.49 | 10.8% | 88.4 | 10/10 | 1.00 | 0.67 | 0.21 | 4 | 19.0% | 0.61 | 0.44 | 56.7% | 55.6% | 61.5% | 51.0%/38.7% | n/a (profitable_beyond_25.0x) | pass | 0.111 (unverified) | 0.42 |
| 76 | `cfg_337d` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 74/3/35 | 112 | 38.8% | 6.8% | 0.86 | -8.5% | 201 | 1.60 | 8.1% | 57.4 | 9/9 | 1.00 | 0.67 | 0.19 | 4 | 14.3% | 0.55 | 0.51 | 38.3% | 38.2% | 27.2% | 34.4%/28.0% | n/a (profitable_beyond_25.0x) | pass | 0.108 (unverified) | 0.88 |
| 77 | `cfg_1ad9` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=6, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 59/62/48 | 169 | 43.1% | 7.4% | 0.82 | -6.9% | 141 | 1.41 | 12.3% | 87.1 | 9/9 | 1.00 | 0.74 | 0.09 | 5 | 22.9% | 0.41 | 0.50 | 42.7% | 42.9% | 30.8% | 41.7%/30.9% | n/a (profitable_beyond_25.0x) | pass | 0.093 (unverified) | 0.59 |
| 78 | `cfg_78ac` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=6, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 60/53/74 | 187 | 46.5% | 7.9% | 0.87 | -7.0% | 150 | 1.38 | 12.3% | 97.3 | 8/8 | 1.00 | 0.76 | 0.11 | 5 | 20.9% | 0.49 | 0.53 | 46.0% | 42.8% | 8.4% | 42.2%/34.4% | n/a (profitable_beyond_25.0x) | pass | 0.110 (unverified) | 0.56 |
| 79 | `cfg_0eaa` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 68/72/83 | 223 | 55.4% | 9.2% | 0.88 | -9.7% | 186 | 1.36 | 15.4% | 114.4 | 9/9 | 1.00 | 0.78 | 0.10 | 4 | 29.3% | 0.44 | 0.50 | 54.4% | 51.4% | 12.8% | 55.9%/41.5% | n/a (profitable_beyond_25.0x) | pass | 0.124 (unverified) | 0.48 |
| 80 | `cfg_6f75` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 78/8/61 | 147 | 51.4% | 8.7% | 0.97 | -9.5% | 214 | 1.53 | 10.3% | 75.5 | 7/7 | 1.00 | 0.69 | 0.28 | 4 | 26.2% | 0.40 | 0.47 | 50.4% | 49.8% | 17.4% | 47.5%/37.6% | n/a (profitable_beyond_25.0x) | pass | 0.159 (unverified) | 0.20 |
| 81 | `cfg_ed79` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=9, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 65/41/44 | 150 | 47.7% | 8.1% | 0.99 | -10.3% | 524 | 1.69 | 7.5% | 77.6 | 8/8 | 1.00 | 0.85 | 0.14 | 4 | 20.4% | 0.47 | 0.43 | 45.7% | 44.0% | 22.4% | 41.4%/32.7% | n/a (profitable_beyond_25.0x) | pass | 0.174 (unverified) | 0.47 |
| 82 | `cfg_5490` | timeframe=1h, mean_type=ema, mean_lookback=23, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 46/34/28 | 108 | 36.6% | 6.4% | 0.89 | -6.9% | 305 | 1.62 | 7.7% | 55.5 | 9/9 | 1.00 | 0.78 | 0.11 | 5 | 20.5% | 0.39 | 0.55 | 35.3% | 34.3% | 20.8% | 31.6%/23.2% | n/a (profitable_beyond_25.0x) | pass | 0.124 (unverified) | 0.50 |
| 83 | `cfg_1c93` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=6, entry_z=-3.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 87/35/56 | 178 | 59.0% | 9.7% | 0.93 | -11.9% | 313 | 1.46 | 14.7% | 92.1 | 7/7 | 0.86 | 0.72 | 0.22 | 4 | 31.7% | 0.38 | 0.39 | 58.6% | 58.1% | 17.6% | 55.5%/45.8% | n/a (profitable_beyond_25.0x) | pass | 0.146 (unverified) | 0.75 |
| 84 | `cfg_70e9` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 65/23/69 | 157 | 51.7% | 8.7% | 0.85 | -9.5% | 184 | 1.44 | 12.9% | 81.7 | 8/8 | 1.00 | 0.80 | 0.05 | 5 | 31.1% | 0.39 | 0.50 | 51.1% | 50.5% | 4.0% | 48.7%/36.7% | n/a (profitable_beyond_25.0x) | pass | 0.109 (unverified) | 0.76 |
| 85 | `cfg_ce20` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=6, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 73/37/57 | 167 | 43.3% | 7.5% | 0.80 | -10.3% | 353 | 1.40 | 14.6% | 85.3 | 8/8 | 1.00 | 0.68 | 0.11 | 4 | 26.4% | 0.36 | 0.46 | 43.0% | 42.2% | 7.5% | 37.4%/28.3% | n/a (profitable_beyond_25.0x) | pass | 0.084 (unverified) | 0.40 |
| 86 | `cfg_42ec` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=6, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 77/42/60 | 179 | 61.1% | 10.0% | 0.95 | -11.9% | 332 | 1.50 | 16.0% | 92.8 | 8/8 | 1.00 | 0.79 | 0.16 | 4 | 34.8% | 0.33 | 0.42 | 59.2% | 57.2% | 10.9% | 53.0%/44.4% | n/a (profitable_beyond_25.0x) | pass | 0.153 (unverified) | 0.44 |
| 87 | `cfg_9412` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 47/22/38 | 107 | 66.0% | 10.7% | 1.11 | -6.9% | 314 | 1.85 | 9.5% | 56.3 | 9/9 | 1.00 | 0.92 | 0.19 | 4 | 36.9% | 0.44 | 0.41 | 66.7% | 65.7% | 37.7% | 60.8%/48.1% | n/a (profitable_beyond_25.0x) | pass | 0.244 (unverified) | 0.60 |
| 88 | `cfg_8b06` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 85/21/78 | 184 | 61.1% | 10.0% | 0.86 | -10.7% | 378 | 1.45 | 13.9% | 97.0 | 8/8 | 1.00 | 0.78 | 0.09 | 4 | 39.0% | 0.36 | 0.42 | 60.9% | 59.7% | 31.8% | 56.4%/39.6% | n/a (profitable_beyond_25.0x) | pass | 0.114 (unverified) | 0.28 |
| 89 | `cfg_d341` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=6, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 101/43/70 | 214 | 71.1% | 11.3% | 0.95 | -12.3% | 258 | 1.43 | 18.9% | 110.6 | 8/8 | 1.00 | 0.72 | 0.23 | 4 | 34.6% | 0.44 | 0.43 | 70.9% | 68.4% | 32.2% | 66.7%/53.4% | n/a (profitable_beyond_25.0x) | pass | 0.162 (unverified) | 0.28 |
| 90 | `cfg_7d06` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 67/50/68 | 185 | 65.2% | 10.6% | 1.00 | -7.6% | 129 | 1.51 | 12.3% | 95.8 | 9/9 | 1.00 | 0.82 | 0.18 | 5 | 31.9% | 0.43 | 0.45 | 65.0% | 63.9% | 38.7% | 61.7%/45.3% | n/a (profitable_beyond_25.0x) | pass | 0.185 (unverified) | 0.54 |
| 91 | `cfg_f507` | timeframe=1h, mean_type=ema, mean_lookback=37, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 50/67/45 | 162 | 52.6% | 8.8% | 0.88 | -11.8% | 175 | 1.46 | 12.5% | 84.5 | 9/9 | 1.00 | 0.75 | 0.13 | 4 | 26.7% | 0.45 | 0.51 | 52.2% | 52.5% | 45.2% | 49.9%/40.7% | n/a (profitable_beyond_25.0x) | pass | 0.115 (unverified) | 0.53 |
| 92 | `cfg_9050` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=6, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 57/69/47 | 173 | 47.8% | 8.1% | 0.80 | -7.4% | 126 | 1.45 | 13.0% | 89.2 | 9/9 | 1.00 | 0.85 | -0.05 | 4 | 23.3% | 0.45 | 0.45 | 47.1% | 45.4% | 19.7% | 43.5%/33.8% | n/a (profitable_beyond_25.0x) | pass | 0.080 (unverified) | 0.65 |
| 93 | `cfg_0800` | timeframe=1h, mean_type=ema, mean_lookback=23, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 60/7/51 | 118 | 38.1% | 6.7% | 0.82 | -8.0% | 326 | 1.49 | 8.7% | 60.5 | 7/7 | 1.00 | 0.78 | 0.04 | 5 | 22.8% | 0.40 | 0.55 | 37.8% | 37.9% | 12.4% | 33.8%/22.8% | n/a (profitable_beyond_25.0x) | pass | 0.091 (unverified) | 0.44 |
| 94 | `cfg_af71` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 10/84/41 | 135 | 40.0% | 7.0% | 0.91 | -9.5% | 530 | 1.58 | 7.7% | 70.8 | 7/7 | 1.00 | 0.77 | 0.14 | 4 | 12.2% | 0.60 | 0.65 | 39.0% | 38.4% | 11.1% | 35.2%/26.6% | n/a (profitable_beyond_25.0x) | pass | 0.126 (unverified) | 0.22 |
| 95 | `cfg_7cdc` | timeframe=1h, mean_type=ema, mean_lookback=23, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 60/12/39 | 111 | 37.0% | 6.5% | 0.78 | -8.8% | 326 | 1.52 | 8.9% | 56.6 | 8/8 | 1.00 | 0.85 | -0.07 | 4 | 18.7% | 0.49 | 0.56 | 36.5% | 36.1% | 13.1% | 33.6%/25.2% | n/a (profitable_beyond_25.0x) | pass | 0.080 (unverified) | 0.39 |
| 96 | `cfg_604e` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 73/72/54 | 199 | 53.7% | 9.0% | 0.86 | -8.0% | 168 | 1.43 | 14.4% | 101.8 | 10/10 | 1.00 | 0.83 | 0.03 | 5 | 32.1% | 0.36 | 0.39 | 52.7% | 51.8% | 20.3% | 49.7%/36.8% | n/a (profitable_beyond_25.0x) | pass | 0.108 (unverified) | 0.62 |
| 97 | `cfg_e3b4` | timeframe=1h, mean_type=ema, mean_lookback=37, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 22/72/43 | 137 | 45.7% | 7.8% | 0.92 | -6.4% | 209 | 1.61 | 7.5% | 71.0 | 7/7 | 1.00 | 0.66 | 0.26 | 5 | 25.2% | 0.37 | 0.47 | 44.8% | 44.4% | 15.9% | 41.0%/27.0% | n/a (profitable_beyond_25.0x) | pass | 0.130 (unverified) | 0.68 |
| 98 | `cfg_7ccb` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=6, entry_z=-2.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 116/25/64 | 205 | 49.9% | 8.4% | 0.86 | -9.1% | 202 | 1.37 | 15.5% | 106.4 | 9/9 | 1.00 | 0.68 | 0.18 | 5 | 35.8% | 0.26 | 0.41 | 50.0% | 49.2% | 26.6% | 46.5%/37.6% | n/a (profitable_beyond_25.0x) | pass | 0.121 (unverified) | 0.76 |
| 99 | `cfg_539d` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 51/57/0 | 108 | 53.3% | 8.9% | 0.94 | -9.0% | 472 | 1.82 | 13.2% | 56.0 | 9/9 | 0.89 | 0.65 | 0.28 | 4 | 20.1% | 0.52 | 0.44 | 52.0% | 52.1% | 30.9% | 51.1%/40.9% | n/a (profitable_beyond_25.0x) | pass | 0.148 (unverified) | 0.20 |
| 100 | `cfg_d547` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 57/43/0 | 100 | 53.6% | 9.0% | 0.95 | -6.3% | 465 | 1.88 | 11.2% | 51.8 | 8/8 | 1.00 | 0.67 | 0.29 | 4 | 19.6% | 0.54 | 0.41 | 53.2% | 53.1% | 44.5% | 51.2%/40.5% | n/a (profitable_beyond_25.0x) | pass | 0.156 (unverified) | 0.43 |
| 101 | `cfg_b068` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 59/12/32 | 103 | 44.1% | 7.6% | 0.90 | -7.7% | 379 | 1.74 | 8.7% | 52.6 | 10/10 | 1.00 | 0.70 | 0.20 | 4 | 23.1% | 0.48 | 0.46 | 42.9% | 42.5% | 9.1% | 40.0%/30.7% | n/a (profitable_beyond_25.0x) | pass | 0.132 (unverified) | 0.53 |
| 102 | `cfg_d5d7` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 60/8/47 | 115 | 43.5% | 7.5% | 0.88 | -7.7% | 328 | 1.58 | 8.6% | 59.8 | 9/9 | 1.00 | 0.65 | 0.23 | 5 | 27.9% | 0.33 | 0.48 | 42.9% | 42.8% | 7.3% | 37.1%/30.6% | n/a (profitable_beyond_25.0x) | pass | 0.119 (unverified) | 0.54 |
| 103 | `cfg_9016` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=6, entry_z=-2.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 103/37/63 | 203 | 62.3% | 10.2% | 0.89 | -13.3% | 307 | 1.44 | 16.6% | 104.6 | 8/8 | 0.88 | 0.73 | 0.16 | 4 | 36.5% | 0.37 | 0.40 | 60.7% | 58.7% | 26.5% | 55.6%/44.0% | n/a (profitable_beyond_25.0x) | pass | 0.131 (unverified) | 0.51 |
| 104 | `cfg_8f9e` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=9, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 50/22/42 | 114 | 38.5% | 6.7% | 0.79 | -9.0% | 255 | 1.48 | 10.2% | 58.7 | 9/9 | 1.00 | 0.72 | 0.07 | 4 | 19.9% | 0.41 | 0.56 | 37.7% | 37.3% | 22.3% | 35.0%/26.1% | n/a (profitable_beyond_25.0x) | pass | 0.081 (unverified) | 0.54 |
| 105 | `cfg_202f` | timeframe=1h, mean_type=ema, mean_lookback=37, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 57/34/49 | 140 | 66.2% | 10.7% | 0.99 | -8.7% | 498 | 1.64 | 13.5% | 73.3 | 8/8 | 1.00 | 0.76 | 0.23 | 4 | 29.3% | 0.43 | 0.42 | 64.9% | 64.4% | 33.0% | 57.1%/46.9% | n/a (profitable_beyond_25.0x) | pass | 0.173 (unverified) | 0.26 |
| 106 | `cfg_a8bf` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 12/85/37 | 134 | 47.2% | 8.0% | 0.98 | -5.3% | 202 | 1.69 | 7.7% | 68.7 | 8/8 | 1.00 | 0.77 | 0.21 | 5 | 17.9% | 0.55 | 0.56 | 46.6% | 45.1% | -4.3% | 40.7%/28.0% | n/a (profitable_beyond_25.0x) | pass | 0.148 (unverified) | 0.99 |
| 107 | `cfg_cc61` | timeframe=1h, mean_type=ema, mean_lookback=37, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 61/27/75 | 163 | 59.4% | 9.8% | 0.90 | -9.9% | 250 | 1.47 | 13.7% | 84.6 | 7/7 | 1.00 | 0.78 | 0.12 | 4 | 22.7% | 0.52 | 0.47 | 58.7% | 58.6% | 35.6% | 55.5%/43.7% | n/a (profitable_beyond_25.0x) | pass | 0.127 (unverified) | 0.38 |
| 108 | `cfg_72f9` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 81/16/79 | 176 | 49.9% | 8.4% | 0.85 | -9.1% | 313 | 1.40 | 12.6% | 91.8 | 8/8 | 1.00 | 0.72 | 0.13 | 4 | 28.6% | 0.35 | 0.52 | 49.4% | 49.5% | 7.1% | 41.6%/29.7% | n/a (profitable_beyond_25.0x) | pass | 0.102 (unverified) | 0.28 |
| 109 | `cfg_c3d1` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 92/40/99 | 231 | 52.1% | 8.8% | 0.76 | -11.4% | 258 | 1.31 | 18.4% | 118.9 | 8/8 | 1.00 | 0.78 | -0.02 | 5 | 35.7% | 0.29 | 0.50 | 52.2% | 51.6% | 23.7% | 51.0%/35.4% | n/a (profitable_beyond_25.0x) | pass | 0.078 (unverified) | 0.36 |
| 110 | `cfg_915f` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 52/39/49 | 140 | 52.8% | 8.9% | 0.85 | -9.7% | 211 | 1.53 | 13.4% | 73.2 | 9/9 | 1.00 | 0.68 | 0.17 | 5 | 32.8% | 0.34 | 0.48 | 51.4% | 49.5% | 11.2% | 46.4%/35.4% | n/a (profitable_beyond_25.0x) | pass | 0.110 (unverified) | 0.72 |
| 111 | `cfg_a521` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=9, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 66/46/48 | 160 | 39.3% | 6.9% | 0.85 | -7.9% | 524 | 1.54 | 7.9% | 81.1 | 8/8 | 1.00 | 0.77 | 0.08 | 4 | 15.6% | 0.53 | 0.46 | 38.9% | 37.3% | 18.0% | 34.3%/26.9% | n/a (profitable_beyond_25.0x) | pass | 0.103 (unverified) | 0.18 |
| 112 | `cfg_2b4e` | timeframe=1h, mean_type=ema, mean_lookback=23, std_lookback=6, entry_z=-2.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 113/25/49 | 187 | 45.9% | 7.8% | 0.87 | -9.8% | 363 | 1.44 | 10.7% | 95.8 | 8/8 | 1.00 | 0.70 | 0.17 | 4 | 13.0% | 0.65 | 0.47 | 45.2% | 44.9% | 38.1% | 42.6%/32.5% | n/a (profitable_beyond_25.0x) | pass | 0.112 (unverified) | 0.46 |
| 113 | `cfg_df0f` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=6, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 78/48/70 | 196 | 49.9% | 8.4% | 0.85 | -7.4% | 173 | 1.40 | 12.7% | 101.3 | 7/7 | 1.00 | 0.72 | 0.13 | 5 | 26.3% | 0.42 | 0.46 | 49.0% | 48.8% | 19.8% | 48.6%/38.1% | n/a (profitable_beyond_25.0x) | pass | 0.108 (unverified) | 0.60 |
| 114 | `cfg_0f5d` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 35/41/25 | 101 | 50.4% | 8.5% | 0.94 | -7.7% | 180 | 1.78 | 7.6% | 53.4 | 10/10 | 1.00 | 0.69 | 0.25 | 5 | 31.8% | 0.34 | 0.49 | 50.3% | 48.7% | 39.0% | 46.3%/31.1% | n/a (profitable_beyond_25.0x) | pass | 0.139 (unverified) | 0.27 |
| 115 | `cfg_3e3f` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 43/22/49 | 114 | 40.2% | 7.0% | 0.76 | -9.0% | 335 | 1.53 | 9.8% | 58.6 | 9/9 | 1.00 | 0.79 | -0.04 | 5 | 24.0% | 0.40 | 0.53 | 39.8% | 38.8% | 6.1% | 36.6%/30.7% | n/a (profitable_beyond_25.0x) | pass | 0.072 (unverified) | 0.75 |
| 116 | `cfg_88c7` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 57/31/69 | 157 | 49.8% | 8.4% | 0.79 | -9.2% | 211 | 1.43 | 13.7% | 81.6 | 8/8 | 1.00 | 0.70 | 0.09 | 5 | 28.1% | 0.42 | 0.50 | 49.7% | 49.1% | 3.7% | 47.5%/35.2% | n/a (profitable_beyond_25.0x) | pass | 0.088 (unverified) | 0.65 |
| 117 | `cfg_78a2` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 65/40/63 | 168 | 42.3% | 7.3% | 0.82 | -6.4% | 200 | 1.41 | 10.9% | 86.4 | 9/9 | 1.00 | 0.76 | 0.06 | 5 | 24.5% | 0.37 | 0.51 | 42.2% | 41.2% | 10.4% | 39.9%/30.3% | n/a (profitable_beyond_25.0x) | pass | 0.093 (unverified) | 0.63 |
| 118 | `cfg_ea6b` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 99/31/99 | 229 | 51.4% | 8.7% | 0.80 | -10.4% | 249 | 1.31 | 17.1% | 119.2 | 8/8 | 1.00 | 0.76 | 0.04 | 5 | 36.6% | 0.27 | 0.48 | 50.6% | 50.3% | 21.1% | 46.4%/36.3% | n/a (profitable_beyond_25.0x) | pass | 0.094 (unverified) | 0.33 |
| 119 | `cfg_bc9a` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 62/28/53 | 143 | 47.3% | 8.1% | 0.80 | -7.4% | 381 | 1.46 | 13.1% | 74.2 | 9/9 | 1.00 | 0.85 | -0.04 | 5 | 28.0% | 0.38 | 0.50 | 44.7% | 44.3% | 18.1% | 43.8%/33.0% | n/a (profitable_beyond_25.0x) | pass | 0.092 (unverified) | 0.86 |
| 120 | `cfg_07b1` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 74/57/65 | 196 | 54.3% | 9.1% | 0.77 | -13.3% | 362 | 1.38 | 18.6% | 101.4 | 8/8 | 0.88 | 0.75 | 0.02 | 4 | 30.0% | 0.40 | 0.51 | 53.5% | 53.2% | 19.5% | 51.1%/42.1% | n/a (profitable_beyond_25.0x) | pass | 0.081 (unverified) | 0.30 |
| 121 | `cfg_a304` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=6, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 68/48/60 | 176 | 53.4% | 8.9% | 0.80 | -11.0% | 277 | 1.39 | 16.6% | 90.8 | 7/7 | 0.86 | 0.77 | 0.03 | 4 | 31.3% | 0.40 | 0.52 | 53.3% | 52.9% | 13.0% | 50.6%/39.7% | n/a (profitable_beyond_25.0x) | pass | 0.088 (unverified) | 0.55 |
| 122 | `cfg_661a` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=6, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 82/59/55 | 196 | 59.0% | 9.7% | 0.85 | -12.0% | 218 | 1.42 | 14.1% | 101.2 | 9/9 | 1.00 | 0.70 | 0.15 | 4 | 24.5% | 0.53 | 0.48 | 58.5% | 58.1% | 47.7% | 55.9%/45.5% | n/a (profitable_beyond_25.0x) | pass | 0.104 (unverified) | 0.62 |
| 123 | `cfg_5b3d` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 69/22/64 | 155 | 41.4% | 7.2% | 0.75 | -12.1% | 322 | 1.38 | 12.1% | 80.3 | 7/7 | 1.00 | 0.64 | 0.12 | 4 | 22.4% | 0.46 | 0.57 | 37.7% | 37.1% | 13.1% | 37.2%/29.4% | n/a (profitable_beyond_25.0x) | pass | 0.072 (unverified) | 0.39 |
| 124 | `cfg_9626` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 78/59/86 | 223 | 49.1% | 8.3% | 0.83 | -9.0% | 175 | 1.33 | 14.6% | 114.5 | 9/9 | 1.00 | 0.80 | 0.03 | 5 | 27.8% | 0.40 | 0.48 | 47.8% | 46.4% | 5.1% | 45.2%/35.2% | n/a (profitable_beyond_25.0x) | pass | 0.105 (unverified) | 0.57 |
| 125 | `cfg_426f` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 25/87/29 | 141 | 36.4% | 6.4% | 0.76 | -6.7% | 378 | 1.51 | 8.5% | 71.2 | 9/9 | 1.00 | 0.73 | 0.03 | 4 | 20.1% | 0.38 | 0.55 | 36.1% | 35.1% | 23.2% | 32.5%/23.0% | n/a (profitable_beyond_25.0x) | pass | 0.069 (unverified) | 0.46 |
| 126 | `cfg_2e6a` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=6, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 86/51/82 | 219 | 53.9% | 9.0% | 0.84 | -13.2% | 186 | 1.35 | 14.3% | 113.1 | 8/8 | 1.00 | 0.84 | 0.01 | 4 | 24.0% | 0.50 | 0.52 | 52.5% | 51.8% | 29.9% | 53.3%/41.7% | n/a (profitable_beyond_25.0x) | pass | 0.107 (unverified) | 0.58 |
| 127 | `cfg_09ec` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=6, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 73/82/60 | 215 | 53.9% | 9.0% | 0.84 | -9.8% | 226 | 1.38 | 15.8% | 109.1 | 9/9 | 1.00 | 0.65 | 0.19 | 4 | 22.3% | 0.57 | 0.52 | 52.9% | 51.1% | 27.4% | 52.5%/42.6% | n/a (profitable_beyond_25.0x) | pass | 0.111 (unverified) | 0.49 |
| 128 | `cfg_4346` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=9, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 38/38/36 | 112 | 31.2% | 5.6% | 0.84 | -6.6% | 286 | 1.56 | 5.7% | 56.9 | 9/9 | 1.00 | 0.68 | 0.16 | 4 | 13.9% | 0.49 | 0.57 | 30.8% | 29.9% | 17.2% | 26.1%/18.5% | n/a (profitable_beyond_25.0x) | pass | 0.089 (unverified) | 0.42 |
| 129 | `cfg_d994` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=6, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 81/33/92 | 206 | 47.5% | 8.1% | 0.76 | -9.7% | 313 | 1.34 | 15.8% | 106.7 | 7/7 | 1.00 | 0.76 | 0.00 | 4 | 29.4% | 0.34 | 0.54 | 47.0% | 45.5% | -8.5% | 43.0%/32.9% | n/a (profitable_beyond_25.0x) | pass | 0.073 (unverified) | 0.16 |
| 130 | `cfg_4c80` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=6, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 87/61/54 | 202 | 54.6% | 9.1% | 0.87 | -7.3% | 186 | 1.45 | 13.9% | 102.5 | 10/10 | 1.00 | 0.71 | 0.16 | 4 | 27.1% | 0.44 | 0.40 | 53.7% | 52.4% | 13.6% | 48.1%/38.3% | n/a (profitable_beyond_25.0x) | pass | 0.113 (unverified) | 0.77 |
| 131 | `cfg_6600` | timeframe=1h, mean_type=sma, mean_lookback=23, std_lookback=9, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 26/51/36 | 113 | 30.5% | 5.5% | 0.78 | -7.0% | 335 | 1.56 | 6.1% | 57.4 | 8/8 | 1.00 | 0.63 | 0.15 | 5 | 16.6% | 0.42 | 0.63 | 30.1% | 29.6% | 10.9% | 26.0%/17.6% | n/a (profitable_beyond_25.0x) | pass | 0.065 (unverified) | 0.43 |
| 132 | `cfg_3296` | timeframe=1h, mean_type=sma, mean_lookback=23, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 87/21/57 | 165 | 45.1% | 7.7% | 0.77 | -7.5% | 131 | 1.40 | 14.1% | 85.0 | 8/8 | 1.00 | 0.65 | 0.12 | 5 | 26.8% | 0.37 | 0.48 | 44.8% | 44.2% | 12.7% | 40.2%/28.4% | n/a (profitable_beyond_25.0x) | pass | 0.083 (unverified) | 0.23 |
| 133 | `cfg_c6b1` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 76/25/55 | 156 | 47.7% | 8.1% | 0.81 | -12.0% | 395 | 1.42 | 12.8% | 81.0 | 9/9 | 1.00 | 0.67 | 0.13 | 4 | 25.7% | 0.38 | 0.52 | 47.6% | 47.2% | 20.3% | 39.5%/31.3% | n/a (profitable_beyond_25.0x) | pass | 0.087 (unverified) | 0.55 |
| 134 | `cfg_1a53` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 10/67/33 | 110 | 29.4% | 5.3% | 0.82 | -9.5% | 542 | 1.59 | 6.4% | 55.8 | 8/8 | 0.88 | 0.73 | 0.09 | 3 | 6.3% | 0.69 | 0.79 | 29.5% | 29.3% | 1.6% | 27.3%/20.4% | n/a (profitable_beyond_25.0x) | pass | 0.082 (unverified) | 0.92 |
| 135 | `cfg_8ee4` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 33/78/29 | 140 | 39.3% | 6.9% | 0.81 | -6.0% | 377 | 1.54 | 8.3% | 71.6 | 9/9 | 1.00 | 0.64 | 0.16 | 5 | 14.7% | 0.57 | 0.50 | 38.7% | 37.0% | 35.4% | 35.7%/27.2% | n/a (profitable_beyond_25.0x) | pass | 0.084 (unverified) | 0.42 |
| 136 | `cfg_b57e` | timeframe=1h, mean_type=sma, mean_lookback=23, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 99/19/93 | 211 | 41.8% | 7.2% | 0.77 | -10.0% | 137 | 1.30 | 14.9% | 109.2 | 7/7 | 1.00 | 0.66 | 0.11 | 5 | 25.0% | 0.32 | 0.58 | 40.1% | 39.6% | 6.1% | 35.8%/27.4% | 24.1 (interpolated) | pass | 0.076 (unverified) | 0.38 |
| 137 | `cfg_753b` | timeframe=1h, mean_type=sma, mean_lookback=28, std_lookback=9, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 21/50/32 | 103 | 27.6% | 5.0% | 0.78 | -4.7% | 205 | 1.56 | 5.7% | 52.8 | 8/8 | 1.00 | 0.69 | 0.10 | 5 | 14.0% | 0.47 | 0.69 | 27.0% | 25.8% | 17.4% | 24.9%/17.7% | n/a (profitable_beyond_25.0x) | pass | 0.063 (unverified) | 0.22 |
| 138 | `cfg_c631` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-2.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 58/20/39 | 117 | 38.3% | 6.7% | 0.85 | -8.9% | 281 | 1.58 | 6.8% | 59.7 | 9/9 | 1.00 | 0.65 | 0.20 | 5 | 23.8% | 0.38 | 0.54 | 37.9% | 37.8% | -4.1% | 34.2%/24.0% | n/a (profitable_beyond_25.0x) | pass | 0.109 (unverified) | 0.09 |
| 139 | `cfg_bee2` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 22/70/37 | 129 | 40.0% | 7.0% | 0.81 | -10.4% | 184 | 1.45 | 10.4% | 66.5 | 9/9 | 1.00 | 0.51 | 0.30 | 3 | 18.4% | 0.49 | 0.69 | 39.4% | 38.9% | 5.4% | 33.8%/24.7% | n/a (profitable_beyond_25.0x) | pass | 0.086 (unverified) | 0.17 |
| 140 | `cfg_ccc9` | timeframe=1h, mean_type=ema, mean_lookback=28, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 38/81/47 | 166 | 30.8% | 5.5% | 0.76 | -5.4% | 325 | 1.40 | 8.6% | 84.2 | 8/8 | 1.00 | 0.69 | 0.07 | 4 | 15.0% | 0.47 | 0.64 | 30.6% | 29.4% | 6.5% | 30.4%/21.8% | 24.0 (interpolated) | pass | 0.075 (unverified) | 0.75 |
| 141 | `cfg_f46e` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=6, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 94/51/84 | 229 | 45.7% | 7.8% | 0.78 | -9.0% | 186 | 1.32 | 14.3% | 117.5 | 9/9 | 1.00 | 0.72 | 0.06 | 4 | 22.5% | 0.46 | 0.49 | 44.1% | 43.1% | 11.8% | 42.8%/34.0% | 22.4 (interpolated) | pass | 0.085 (unverified) | 0.58 |
| 142 | `cfg_3c44` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 62/50/56 | 168 | 57.4% | 9.5% | 0.92 | -9.6% | 488 | 1.49 | 16.9% | 86.4 | 8/8 | 1.00 | 0.62 | 0.30 | 4 | 27.2% | 0.50 | 0.46 | 56.5% | 55.1% | 10.7% | 53.4%/45.6% | n/a (profitable_beyond_25.0x) | pass | 0.142 (unverified) | 0.06 |
| 143 | `cfg_827a` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 49/50/51 | 150 | 50.8% | 8.6% | 0.79 | -9.3% | 394 | 1.50 | 15.2% | 77.4 | 8/8 | 1.00 | 0.67 | 0.12 | 4 | 23.9% | 0.48 | 0.52 | 50.2% | 46.9% | 11.3% | 39.3%/28.5% | n/a (profitable_beyond_25.0x) | pass | 0.088 (unverified) | 0.39 |
| 144 | `cfg_4f94` | timeframe=1h, mean_type=ema, mean_lookback=37, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 65/42/55 | 162 | 52.6% | 8.8% | 0.78 | -10.6% | 353 | 1.40 | 14.9% | 84.7 | 8/8 | 0.88 | 0.59 | 0.20 | 5 | 28.4% | 0.45 | 0.55 | 52.8% | 52.0% | 29.3% | 50.5%/35.0% | n/a (profitable_beyond_25.0x) | pass | 0.082 (unverified) | 0.43 |
| 145 | `cfg_0672` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 72/13/56 | 141 | 39.8% | 6.9% | 0.78 | -9.3% | 185 | 1.43 | 10.4% | 72.0 | 8/8 | 1.00 | 0.76 | 0.02 | 5 | 23.0% | 0.42 | 0.54 | 38.2% | 37.7% | 9.4% | 34.8%/25.6% | n/a (profitable_beyond_25.0x) | pass | 0.083 (unverified) | 0.61 |
| 146 | `cfg_e312` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 21/104/45 | 170 | 45.4% | 7.8% | 0.89 | -6.8% | 323 | 1.56 | 9.7% | 87.2 | 7/7 | 1.00 | 0.73 | 0.17 | 5 | 26.5% | 0.34 | 0.43 | 44.1% | 42.8% | 5.1% | 40.7%/28.2% | n/a (profitable_beyond_25.0x) | pass | 0.128 (unverified) | 0.67 |
| 147 | `cfg_e326` | timeframe=1h, mean_type=sma, mean_lookback=23, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 99/26/66 | 191 | 42.9% | 7.4% | 0.77 | -9.8% | 137 | 1.32 | 15.3% | 99.3 | 8/8 | 1.00 | 0.62 | 0.15 | 4 | 24.1% | 0.35 | 0.55 | 40.3% | 37.9% | 16.1% | 34.5%/26.0% | n/a (profitable_beyond_25.0x) | pass | 0.077 (unverified) | 0.52 |
| 148 | `cfg_c53a` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 25/63/50 | 138 | 40.6% | 7.1% | 0.84 | -10.0% | 324 | 1.47 | 10.3% | 72.2 | 8/8 | 1.00 | 0.61 | 0.23 | 4 | 21.3% | 0.46 | 0.59 | 40.2% | 39.6% | 1.2% | 34.7%/26.1% | n/a (profitable_beyond_25.0x) | pass | 0.098 (unverified) | 0.08 |
| 149 | `cfg_1a57` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 50/28/57 | 135 | 44.2% | 7.6% | 0.77 | -7.5% | 213 | 1.47 | 12.4% | 69.4 | 8/8 | 1.00 | 0.64 | 0.13 | 5 | 22.0% | 0.48 | 0.53 | 41.5% | 41.0% | 11.4% | 35.6%/28.6% | n/a (profitable_beyond_25.0x) | pass | 0.080 (unverified) | 0.66 |
| 150 | `cfg_3c7d` | timeframe=1h, mean_type=sma, mean_lookback=32, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 69/18/39 | 126 | 39.4% | 6.9% | 0.78 | -10.7% | 173 | 1.46 | 10.3% | 64.6 | 9/9 | 1.00 | 0.68 | 0.11 | 5 | 24.8% | 0.36 | 0.54 | 39.5% | 38.9% | 17.2% | 34.7%/26.5% | n/a (profitable_beyond_25.0x) | pass | 0.087 (unverified) | 0.72 |
| 151 | `cfg_617b` | timeframe=1h, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-2.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 64/11/37 | 112 | 36.8% | 6.5% | 0.78 | -7.0% | 298 | 1.53 | 8.1% | 57.1 | 9/9 | 1.00 | 0.62 | 0.16 | 4 | 21.7% | 0.41 | 0.56 | 36.4% | 35.3% | 18.2% | 33.7%/23.5% | n/a (profitable_beyond_25.0x) | pass | 0.079 (unverified) | 0.16 |
| 152 | `cfg_be50` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=9, entry_z=-2.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 67/41/88 | 196 | 55.4% | 9.2% | 0.85 | -14.6% | 417 | 1.35 | 17.2% | 102.6 | 7/7 | 1.00 | 0.54 | 0.31 | 3 | 24.3% | 0.60 | 0.56 | 55.2% | 54.7% | 24.9% | 52.6%/37.5% | n/a (profitable_beyond_25.0x) | pass | 0.107 (unverified) | 0.26 |
| 153 | `cfg_d0ef` | timeframe=1h, mean_type=sma, mean_lookback=37, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 20/106/30 | 156 | 35.2% | 6.2% | 0.76 | -6.8% | 344 | 1.48 | 9.5% | 78.7 | 8/8 | 1.00 | 0.59 | 0.17 | 5 | 22.6% | 0.31 | 0.52 | 34.6% | 34.4% | 2.4% | 32.9%/22.1% | n/a (profitable_beyond_25.0x) | pass | 0.075 (unverified) | 0.66 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 3.2% / 0.51 / 24 | 3.2% / 0.91 / 13 | 6.4% / 0.64 / 15 | 7.9% / 2.17 / 17 | 23.4% / 2.20 / 39 |
| 2 | 6.3% / 0.90 / 24 | 1.9% / 0.50 / 19 | 11.7% / 1.22 / 17 | 5.7% / 1.54 / 16 | 13.2% / 1.54 / 41 |
| 3 | 4.4% / 0.51 / 34 | 4.0% / 0.82 / 21 | 19.9% / 1.56 / 22 | 11.0% / 2.10 / 20 | 19.1% / 1.52 / 48 |
| 4 | 9.0% / 1.06 / 25 | 1.5% / 0.35 / 19 | 15.5% / 1.87 / 16 | 10.7% / 2.22 / 16 | 12.7% / 1.12 / 44 |
| 5 | 2.9% / 0.41 / 30 | 3.0% / 0.97 / 9 | 16.1% / 1.38 / 18 | 10.1% / 2.36 / 15 | 22.1% / 2.05 / 42 |
| 6 | 4.9% / 0.60 / 34 | 2.6% / 0.59 / 21 | 18.1% / 1.45 / 22 | 11.2% / 2.23 / 20 | 14.5% / 1.26 / 48 |
| 7 | 10.1% / 1.01 / 38 | 6.9% / 1.60 / 21 | 18.9% / 1.51 / 23 | 9.5% / 1.77 / 23 | 7.7% / 0.67 / 54 |
| 8 | 3.2% / 0.51 / 24 | 3.5% / 1.03 / 14 | 6.5% / 0.66 / 15 | 7.1% / 2.12 / 17 | 19.7% / 1.96 / 39 |
| 9 | 6.2% / 0.64 / 38 | 5.4% / 1.01 / 27 | 16.2% / 1.35 / 24 | 14.5% / 2.64 / 24 | 8.0% / 0.70 / 52 |
| 10 | 8.3% / 0.90 / 31 | 3.7% / 1.25 / 7 | 8.8% / 0.77 / 18 | 14.1% / 2.99 / 14 | 18.2% / 1.49 / 44 |
| 11 | -0.1% / 0.02 / 28 | 3.6% / 1.11 / 9 | 11.4% / 1.48 / 13 | 5.4% / 1.45 / 14 | 13.5% / 1.48 / 38 |
| 12 | 0.1% / 0.05 / 32 | 1.3% / 0.33 / 21 | 14.5% / 1.16 / 23 | 5.1% / 1.25 / 20 | 22.4% / 2.12 / 44 |
| 13 | 4.0% / 0.51 / 31 | 4.6% / 1.17 / 21 | 22.7% / 2.01 / 21 | 6.2% / 1.31 / 23 | 12.2% / 1.23 / 46 |
| 14 | 6.2% / 0.89 / 24 | 2.4% / 0.63 / 19 | 10.8% / 1.14 / 17 | 4.0% / 1.25 / 16 | 11.6% / 1.40 / 41 |
| 15 | 6.7% / 0.70 / 35 | 5.0% / 0.99 / 20 | 20.0% / 1.56 / 22 | 9.7% / 2.04 / 19 | 12.9% / 1.08 / 52 |
| 16 | -0.3% / 0.02 / 37 | 8.4% / 1.66 / 25 | 28.0% / 1.83 / 27 | 10.5% / 1.85 / 31 | 10.5% / 0.82 / 61 |
| 17 | 5.5% / 0.67 / 30 | 6.1% / 1.08 / 26 | 13.5% / 1.12 / 23 | 13.5% / 2.42 / 22 | 9.3% / 0.83 / 42 |
| 18 | 8.8% / 0.99 / 32 | 3.2% / 0.64 / 23 | 17.4% / 1.99 / 20 | 11.3% / 2.16 / 23 | 6.1% / 0.57 / 50 |
| 19 | 0.8% / 0.13 / 27 | 3.8% / 1.03 / 14 | 20.7% / 2.00 / 19 | 1.2% / 0.41 / 11 | 12.8% / 1.32 / 45 |
| 20 | 6.1% / 0.64 / 34 | 2.6% / 0.52 / 17 | 10.9% / 0.97 / 16 | 11.0% / 2.38 / 16 | 14.9% / 1.25 / 47 |
| 21 | 1.8% / 0.27 / 31 | 3.7% / 0.96 / 21 | 24.7% / 2.17 / 21 | 4.4% / 1.06 / 23 | 12.5% / 1.26 / 46 |
| 22 | -1.4% / -0.09 / 36 | 6.5% / 1.27 / 25 | 24.3% / 1.67 / 25 | 10.5% / 1.39 / 24 | 17.2% / 1.15 / 59 |
| 23 | 4.0% / 0.46 / 31 | 1.6% / 0.38 / 14 | 14.9% / 1.92 / 12 | 10.2% / 2.19 / 10 | 15.3% / 1.32 / 45 |
| 24 | 8.1% / 0.80 / 41 | 8.7% / 1.56 / 26 | 5.2% / 0.46 / 26 | 15.1% / 2.63 / 22 | 12.0% / 0.94 / 51 |
| 25 | 5.2% / 0.61 / 24 | 3.1% / 0.64 / 19 | 13.1% / 1.61 / 15 | 11.4% / 2.31 / 15 | 7.6% / 0.71 / 40 |
| 26 | 2.6% / 0.29 / 39 | 10.2% / 1.80 / 26 | 20.2% / 1.59 / 25 | 14.7% / 2.08 / 32 | 0.7% / 0.12 / 53 |
| 27 | 2.2% / 0.27 / 37 | 4.3% / 1.03 / 18 | 36.0% / 2.16 / 28 | 12.9% / 2.40 / 28 | 4.6% / 0.41 / 57 |
| 28 | 9.9% / 1.04 / 37 | 6.2% / 1.45 / 20 | 19.2% / 1.38 / 23 | 9.6% / 1.73 / 24 | 3.1% / 0.31 / 56 |
| 29 | -2.4% / -0.18 / 31 | 5.5% / 0.94 / 25 | 18.9% / 1.33 / 24 | 15.1% / 1.99 / 23 | 16.4% / 1.22 / 45 |
| 30 | 3.0% / 0.40 / 24 | -0.2% / -0.03 / 16 | 7.8% / 0.76 / 15 | 11.3% / 2.79 / 15 | 16.4% / 1.44 / 42 |
| 31 | 0.2% / 0.07 / 31 | 4.1% / 0.85 / 23 | 23.1% / 1.99 / 21 | 14.8% / 1.99 / 23 | 6.6% / 0.55 / 52 |
| 32 | -2.8% / -0.46 / 27 | 5.2% / 2.07 / 14 | 16.9% / 2.28 / 17 | 10.3% / 2.59 / 20 | 6.1% / 0.69 / 46 |
| 33 | 3.9% / 0.40 / 39 | 9.5% / 1.77 / 26 | 26.2% / 2.08 / 25 | 13.6% / 2.03 / 32 | -1.2% / -0.04 / 53 |
| 34 | -3.6% / -0.48 / 27 | 2.8% / 0.81 / 14 | 19.2% / 2.26 / 19 | 1.7% / 0.68 / 11 | 15.7% / 1.65 / 46 |
| 35 | 9.8% / 1.12 / 33 | 8.9% / 1.55 / 25 | 1.8% / 0.21 / 25 | 12.5% / 2.16 / 22 | 12.9% / 1.12 / 40 |
| 36 | 0.4% / 0.09 / 44 | 13.9% / 2.39 / 32 | 13.6% / 1.10 / 28 | 11.1% / 1.28 / 35 | 17.9% / 1.19 / 64 |
| 37 | -4.0% / -0.35 / 43 | 7.5% / 1.65 / 27 | 27.3% / 1.85 / 29 | 8.8% / 1.44 / 35 | 12.9% / 0.95 / 68 |
| 38 | 0.0% / 0.04 / 32 | 2.0% / 0.53 / 21 | 15.1% / 1.15 / 23 | 4.5% / 1.07 / 20 | 19.1% / 1.88 / 44 |
| 39 | 0.9% / 0.16 / 30 | 2.7% / 0.89 / 9 | 10.8% / 1.00 / 18 | 10.0% / 2.73 / 15 | 18.4% / 1.91 / 43 |
| 40 | 0.5% / 0.11 / 39 | 5.2% / 1.43 / 21 | 23.3% / 1.58 / 24 | 3.5% / 0.71 / 23 | 13.6% / 1.28 / 49 |
| 41 | 2.0% / 0.27 / 26 | 0.7% / 0.17 / 19 | 16.7% / 1.53 / 17 | 11.5% / 1.75 / 16 | 12.4% / 0.98 / 46 |
| 42 | 12.3% / 1.58 / 30 | 5.1% / 1.20 / 19 | 15.4% / 1.13 / 22 | 9.3% / 1.74 / 21 | 3.8% / 0.39 / 45 |
| 43 | -1.7% / -0.13 / 28 | 5.9% / 1.16 / 22 | 20.9% / 1.76 / 20 | 12.3% / 1.80 / 21 | 8.4% / 0.71 / 46 |
| 44 | -0.2% / 0.02 / 27 | 4.0% / 0.91 / 16 | 26.6% / 2.02 / 22 | 13.9% / 2.08 / 18 | 3.2% / 0.32 / 43 |
| 45 | -2.5% / -0.25 / 41 | 6.3% / 1.26 / 22 | 17.3% / 1.24 / 27 | 6.9% / 1.56 / 22 | 11.9% / 1.28 / 40 |
| 46 | 4.9% / 0.50 / 43 | 9.8% / 1.87 / 28 | 17.2% / 1.22 / 28 | 12.4% / 1.67 / 36 | 2.2% / 0.24 / 61 |
| 47 | 0.9% / 0.13 / 37 | 3.5% / 0.62 / 26 | 20.9% / 1.50 / 25 | 16.4% / 2.10 / 25 | 5.5% / 0.45 / 55 |
| 48 | -5.2% / -0.61 / 37 | 9.1% / 2.33 / 18 | 24.6% / 1.65 / 23 | 6.2% / 1.39 / 19 | 15.9% / 1.45 / 51 |
| 49 | 0.8% / 0.12 / 39 | 12.2% / 2.29 / 27 | 22.6% / 1.37 / 31 | 19.3% / 2.26 / 34 | 7.5% / 0.57 / 61 |
| 50 | 0.2% / 0.07 / 36 | 5.9% / 1.19 / 20 | 21.9% / 1.55 / 23 | 11.1% / 1.62 / 19 | 13.4% / 0.97 / 55 |
| 51 | 1.5% / 0.19 / 42 | 12.2% / 1.95 / 30 | 12.3% / 0.88 / 33 | 12.4% / 1.47 / 36 | 16.1% / 1.09 / 59 |
| 52 | 6.4% / 0.70 / 29 | 3.7% / 0.92 / 11 | 14.0% / 0.97 / 20 | 13.5% / 1.96 / 15 | 15.4% / 1.16 / 46 |
| 53 | 3.3% / 0.38 / 38 | 8.5% / 1.68 / 25 | 29.8% / 2.00 / 26 | 7.9% / 1.46 / 30 | 6.2% / 0.54 / 61 |
| 54 | 0.4% / 0.09 / 33 | 7.0% / 1.48 / 18 | 18.1% / 1.11 / 27 | 17.8% / 2.19 / 28 | 14.7% / 1.04 / 56 |
| 55 | 8.2% / 0.77 / 36 | 6.1% / 1.30 / 19 | 31.3% / 1.69 / 28 | 14.6% / 2.21 / 28 | 1.0% / 0.14 / 57 |
| 56 | -1.7% / -0.23 / 28 | 3.9% / 1.27 / 9 | 8.8% / 1.21 / 13 | 8.0% / 2.03 / 14 | 10.3% / 1.24 / 38 |
| 57 | 3.7% / 0.53 / 25 | 6.3% / 1.52 / 16 | 12.3% / 1.18 / 17 | 16.9% / 3.66 / 19 | 0.5% / 0.10 / 46 |
| 58 | 0.6% / 0.11 / 44 | 2.9% / 0.78 / 20 | 28.9% / 1.70 / 30 | 10.2% / 1.69 / 32 | 7.1% / 0.57 / 64 |
| 59 | -1.5% / -0.20 / 27 | 5.9% / 2.09 / 14 | 12.6% / 1.82 / 16 | 7.5% / 2.27 / 20 | 7.0% / 0.75 / 44 |
| 60 | 6.4% / 0.74 / 28 | -0.4% / -0.08 / 11 | 5.5% / 0.79 / 13 | 9.7% / 2.42 / 12 | 10.5% / 1.06 / 40 |
| 61 | 1.0% / 0.19 / 29 | 3.4% / 1.16 / 14 | 23.9% / 2.32 / 20 | 5.0% / 1.49 / 22 | 2.1% / 0.25 / 43 |
| 62 | 5.8% / 0.68 / 27 | 2.1% / 0.54 / 11 | 10.2% / 0.97 / 15 | 8.8% / 1.88 / 13 | 9.8% / 0.86 / 41 |
| 63 | -3.3% / -0.34 / 40 | 6.2% / 1.32 / 26 | 27.9% / 1.94 / 28 | 8.2% / 1.60 / 33 | 6.7% / 0.58 / 65 |
| 64 | 4.8% / 0.54 / 30 | 3.7% / 0.72 / 22 | 14.5% / 1.64 / 19 | 9.5% / 1.80 / 21 | 2.0% / 0.23 / 43 |
| 65 | -1.6% / -0.17 / 25 | 3.6% / 0.74 / 15 | 28.6% / 2.05 / 21 | 13.4% / 1.99 / 17 | 1.5% / 0.19 / 40 |
| 66 | 3.2% / 0.46 / 37 | 0.5% / 0.16 / 16 | 22.3% / 1.82 / 24 | 6.7% / 1.48 / 28 | 6.6% / 0.62 / 46 |
| 67 | 1.8% / 0.22 / 45 | 10.8% / 2.27 / 29 | 17.3% / 0.99 / 35 | 18.6% / 2.10 / 38 | 6.1% / 0.47 / 70 |
| 68 | 5.8% / 0.56 / 43 | 12.9% / 2.25 / 32 | 18.8% / 1.18 / 31 | 9.7% / 1.48 / 35 | 4.6% / 0.42 / 56 |
| 69 | -2.5% / -0.28 / 31 | 4.7% / 1.69 / 12 | 17.4% / 1.75 / 13 | 4.8% / 1.28 / 10 | 10.9% / 1.10 / 46 |
| 70 | -2.2% / -0.26 / 23 | 6.7% / 1.58 / 15 | 11.2% / 1.06 / 16 | 18.5% / 3.73 / 18 | 4.0% / 0.38 / 41 |
| 71 | 2.1% / 0.25 / 43 | 7.7% / 1.64 / 28 | 20.2% / 1.47 / 28 | 11.0% / 1.56 / 37 | 2.2% / 0.23 / 62 |
| 72 | -4.0% / -0.33 / 46 | 14.7% / 2.63 / 32 | 19.9% / 1.45 / 34 | 14.7% / 2.08 / 36 | 10.6% / 0.83 / 59 |
| 73 | 1.4% / 0.25 / 24 | 1.4% / 0.39 / 17 | 13.2% / 1.61 / 17 | 2.3% / 0.68 / 13 | 9.8% / 1.03 / 43 |
| 74 | 3.3% / 0.41 / 27 | 0.6% / 0.15 / 16 | 14.9% / 2.05 / 18 | 4.8% / 1.46 / 11 | 9.7% / 0.93 / 45 |
| 75 | 5.4% / 0.58 / 38 | 3.5% / 0.81 / 19 | 32.3% / 1.67 / 28 | 12.2% / 2.32 / 28 | -2.8% / -0.17 / 58 |
| 76 | 0.7% / 0.12 / 25 | -1.6% / -0.36 / 14 | 21.4% / 1.77 / 19 | 7.4% / 1.99 / 19 | 7.4% / 0.79 / 35 |
| 77 | 1.4% / 0.19 / 36 | 5.9% / 1.16 / 26 | 16.4% / 1.56 / 22 | 10.6% / 1.66 / 31 | 3.5% / 0.34 / 54 |
| 78 | 3.9% / 0.45 / 40 | 4.1% / 0.91 / 28 | 21.2% / 1.89 / 25 | 9.3% / 1.34 / 34 | 2.2% / 0.24 / 60 |
| 79 | 8.2% / 0.78 / 47 | 11.8% / 2.26 / 34 | 20.2% / 1.41 / 34 | 7.0% / 0.99 / 40 | -0.2% / 0.06 / 68 |
| 80 | 4.9% / 0.63 / 33 | -1.0% / -0.19 / 17 | 20.0% / 1.56 / 22 | 14.1% / 2.84 / 26 | 6.5% / 0.59 / 49 |
| 81 | -6.6% / -0.83 / 37 | 7.0% / 1.83 / 19 | 22.7% / 1.76 / 23 | 6.5% / 1.61 / 20 | 13.3% / 1.29 / 51 |
| 82 | 5.5% / 0.71 / 24 | 1.9% / 0.41 / 15 | 13.3% / 1.82 / 17 | 3.2% / 0.90 / 11 | 8.6% / 0.82 / 41 |
| 83 | -0.7% / -0.01 / 38 | 9.6% / 1.84 / 24 | 20.8% / 1.52 / 29 | 16.3% / 1.88 / 32 | 4.1% / 0.37 / 55 |
| 84 | 8.4% / 0.95 / 35 | 2.5% / 0.53 / 23 | 14.5% / 0.99 / 24 | 15.7% / 2.35 / 22 | 3.1% / 0.29 / 53 |
| 85 | -4.4% / -0.40 / 35 | 7.1% / 1.40 / 26 | 14.4% / 1.40 / 21 | 13.4% / 1.70 / 31 | 7.9% / 0.63 / 54 |
| 86 | -4.7% / -0.40 / 38 | 9.1% / 1.71 / 25 | 19.5% / 1.54 / 27 | 15.4% / 1.99 / 32 | 12.3% / 0.86 / 57 |
| 87 | -0.1% / 0.04 / 26 | 4.0% / 0.88 / 10 | 16.6% / 1.33 / 18 | 13.1% / 1.97 / 14 | 21.3% / 1.68 / 39 |
| 88 | -0.1% / 0.05 / 40 | 5.7% / 1.36 / 20 | 13.6% / 0.83 / 29 | 16.0% / 1.96 / 32 | 15.9% / 1.09 / 63 |
| 89 | -0.0% / 0.05 / 41 | 15.6% / 3.10 / 33 | 27.1% / 1.46 / 36 | 9.5% / 1.13 / 40 | 6.3% / 0.49 / 64 |
| 90 | 6.2% / 0.60 / 42 | 4.8% / 1.13 / 21 | 25.3% / 1.58 / 29 | 11.8% / 1.78 / 31 | 5.9% / 0.52 / 62 |
| 91 | 8.5% / 0.81 / 34 | 5.9% / 1.24 / 20 | 20.5% / 1.52 / 25 | 14.7% / 2.27 / 28 | -3.9% / -0.22 / 55 |
| 92 | -0.4% / 0.02 / 39 | 8.2% / 1.62 / 25 | 19.8% / 1.30 / 25 | 13.4% / 2.05 / 32 | 0.9% / 0.14 / 52 |
| 93 | 0.3% / 0.08 / 25 | 2.9% / 0.66 / 16 | 14.5% / 1.49 / 19 | 3.8% / 1.14 / 11 | 12.4% / 1.02 / 47 |
| 94 | -4.9% / -0.64 / 32 | 1.4% / 0.41 / 15 | 24.7% / 2.29 / 20 | 10.2% / 2.09 / 24 | 5.6% / 0.57 / 44 |
| 95 | -1.8% / -0.14 / 25 | 3.7% / 0.76 / 15 | 14.1% / 1.38 / 18 | 2.2% / 0.62 / 11 | 15.4% / 1.28 / 42 |
| 96 | 3.7% / 0.40 / 47 | 13.4% / 2.41 / 32 | 16.3% / 1.09 / 27 | 9.2% / 1.38 / 35 | 2.9% / 0.28 / 58 |
| 97 | 3.3% / 0.44 / 36 | 0.7% / 0.24 / 11 | 16.4% / 1.22 / 23 | 9.7% / 2.20 / 17 | 9.8% / 0.98 / 50 |
| 98 | 2.1% / 0.27 / 44 | 11.8% / 2.03 / 33 | 9.3% / 0.81 / 29 | 10.4% / 1.66 / 35 | 8.8% / 0.67 / 64 |
| 99 | -2.9% / -0.25 / 21 | 2.3% / 0.44 / 19 | 27.6% / 1.98 / 19 | 15.3% / 2.50 / 18 | 4.7% / 0.45 / 31 |
| 100 | -3.2% / -0.29 / 20 | 5.4% / 1.06 / 14 | 28.4% / 2.03 / 19 | 10.4% / 1.84 / 14 | 6.3% / 0.58 / 33 |
| 101 | -0.6% / -0.04 / 20 | 4.1% / 0.91 / 16 | 6.6% / 0.57 / 15 | 11.7% / 3.10 / 15 | 17.1% / 1.49 / 37 |
| 102 | 4.3% / 0.64 / 23 | 3.0% / 0.69 / 17 | 8.0% / 0.69 / 16 | 12.2% / 2.95 / 16 | 10.3% / 0.88 / 43 |
| 103 | -3.1% / -0.23 / 42 | 13.1% / 2.19 / 31 | 12.4% / 0.78 / 36 | 18.9% / 2.11 / 36 | 10.9% / 0.85 / 58 |
| 104 | -1.8% / -0.17 / 23 | 3.9% / 0.74 / 19 | 15.5% / 1.48 / 16 | 10.9% / 1.70 / 15 | 6.1% / 0.57 / 41 |
| 105 | -4.7% / -0.47 / 28 | 4.9% / 1.04 / 18 | 28.5% / 1.65 / 23 | 9.4% / 1.25 / 22 | 18.2% / 1.34 / 49 |
| 106 | 0.8% / 0.14 / 32 | 4.0% / 1.34 / 14 | 24.8% / 1.97 / 21 | 4.2% / 1.10 / 25 | 8.1% / 0.72 / 42 |
| 107 | -1.3% / -0.10 / 33 | 5.2% / 1.14 / 19 | 30.0% / 1.83 / 24 | 9.8% / 1.30 / 25 | 7.5% / 0.55 / 62 |
| 108 | -1.8% / -0.13 / 39 | 7.0% / 1.58 / 19 | 16.6% / 1.39 / 25 | 10.7% / 1.41 / 30 | 10.6% / 0.77 / 63 |
| 109 | 2.8% / 0.31 / 48 | 11.0% / 1.91 / 32 | 8.5% / 0.59 / 37 | 12.0% / 1.39 / 41 | 9.7% / 0.66 / 73 |
| 110 | 2.4% / 0.27 / 32 | 3.1% / 0.53 / 20 | 13.4% / 0.96 / 23 | 15.1% / 2.27 / 20 | 11.0% / 0.87 / 45 |
| 111 | -3.4% / -0.38 / 41 | 4.5% / 1.27 / 22 | 20.5% / 1.62 / 24 | 1.1% / 0.30 / 23 | 13.3% / 1.31 / 50 |
| 112 | -4.2% / -0.44 / 40 | 6.3% / 1.39 / 26 | 29.1% / 2.05 / 27 | 7.8% / 1.52 / 32 | 2.9% / 0.31 / 62 |
| 113 | 5.2% / 0.53 / 43 | 7.8% / 1.63 / 28 | 18.7% / 1.36 / 28 | 11.2% / 1.56 / 36 | 0.1% / 0.07 / 61 |
| 114 | 4.2% / 0.54 / 25 | 3.8% / 1.22 / 7 | 10.8% / 0.80 / 17 | 14.2% / 2.92 / 13 | 10.1% / 0.92 / 39 |
| 115 | 1.0% / 0.15 / 23 | 0.5% / 0.14 / 16 | 8.7% / 0.73 / 16 | 12.4% / 1.89 / 16 | 13.1% / 1.03 / 43 |
| 116 | 5.7% / 0.59 / 37 | 3.1% / 0.58 / 21 | 13.4% / 0.92 / 24 | 16.9% / 2.68 / 21 | 3.6% / 0.32 / 54 |
| 117 | 2.3% / 0.27 / 38 | 7.6% / 1.75 / 19 | 14.3% / 1.25 / 24 | 6.5% / 1.05 / 29 | 6.3% / 0.61 / 58 |
| 118 | 1.8% / 0.23 / 49 | 12.0% / 2.26 / 34 | 11.4% / 0.83 / 33 | 10.8% / 1.30 / 39 | 7.6% / 0.57 / 74 |
| 119 | 1.7% / 0.22 / 32 | 1.4% / 0.29 / 22 | 16.0% / 1.10 / 22 | 15.1% / 2.31 / 21 | 7.1% / 0.59 / 46 |
| 120 | -3.0% / -0.21 / 42 | 10.6% / 1.58 / 28 | 9.6% / 0.62 / 34 | 18.7% / 2.07 / 35 | 10.5% / 0.76 / 57 |
| 121 | -2.9% / -0.21 / 38 | 10.8% / 1.89 / 23 | 17.5% / 1.12 / 29 | 16.8% / 1.89 / 32 | 3.9% / 0.33 / 54 |
| 122 | 3.9% / 0.40 / 42 | 8.7% / 1.62 / 28 | 27.7% / 1.50 / 32 | 14.1% / 2.05 / 33 | -3.4% / -0.19 / 61 |
| 123 | 7.9% / 0.86 / 36 | 2.5% / 0.54 / 18 | 11.6% / 0.89 / 27 | 15.6% / 2.39 / 24 | -0.8% / -0.00 / 50 |
| 124 | 5.4% / 0.58 / 50 | 12.2% / 2.43 / 34 | 16.7% / 1.23 / 30 | 7.6% / 1.09 / 39 | 0.4% / 0.10 / 70 |
| 125 | -2.7% / -0.30 / 35 | 6.1% / 1.20 / 22 | 13.6% / 0.99 / 26 | 6.6% / 1.37 / 22 | 9.2% / 1.04 / 36 |
| 126 | 4.5% / 0.45 / 47 | 7.5% / 1.53 / 30 | 24.0% / 1.52 / 35 | 14.4% / 1.99 / 37 | -3.4% / -0.19 / 70 |
| 127 | 6.7% / 0.65 / 48 | 11.6% / 2.33 / 35 | 25.8% / 1.49 / 33 | 4.4% / 0.75 / 39 | -1.6% / -0.06 / 60 |
| 128 | -3.0% / -0.35 / 31 | 4.0% / 1.50 / 12 | 15.2% / 1.85 / 13 | 3.5% / 1.06 / 10 | 9.1% / 0.98 / 46 |
| 129 | -3.6% / -0.30 / 44 | 7.5% / 1.52 / 28 | 13.2% / 0.96 / 31 | 13.9% / 1.66 / 38 | 10.4% / 0.73 / 65 |
| 130 | -0.1% / 0.04 / 47 | 11.6% / 2.05 / 33 | 21.6% / 1.34 / 31 | 11.6% / 1.84 / 35 | 2.2% / 0.24 / 56 |
| 131 | 4.3% / 0.63 / 24 | 2.0% / 0.51 / 17 | 11.9% / 1.26 / 17 | 2.1% / 0.63 / 13 | 7.4% / 0.80 / 42 |
| 132 | 2.1% / 0.25 / 33 | 6.5% / 1.21 / 26 | 7.7% / 0.59 / 24 | 14.4% / 2.74 / 27 | 8.3% / 0.66 / 55 |
| 133 | -3.2% / -0.26 / 33 | 7.7% / 1.57 / 18 | 17.5% / 1.39 / 24 | 12.2% / 1.66 / 26 | 7.5% / 0.58 / 55 |
| 134 | -4.1% / -0.69 / 26 | -2.0% / -0.57 / 12 | 21.7% / 2.36 / 17 | 3.7% / 1.08 / 18 | 9.1% / 0.99 / 37 |
| 135 | 0.2% / 0.06 / 34 | 3.6% / 0.99 / 19 | 21.5% / 1.50 / 23 | 3.7% / 0.87 / 19 | 6.5% / 0.68 / 45 |
| 136 | 0.6% / 0.11 / 43 | 13.4% / 2.31 / 36 | 8.0% / 0.79 / 26 | 8.8% / 1.32 / 37 | 5.7% / 0.47 / 69 |
| 137 | 7.4% / 1.02 / 25 | 1.6% / 0.52 / 16 | 11.9% / 1.24 / 17 | 2.9% / 0.90 / 10 | 1.6% / 0.26 / 35 |
| 138 | 3.7% / 0.48 / 31 | 3.9% / 1.29 / 7 | 2.5% / 0.28 / 18 | 12.0% / 3.07 / 15 | 11.7% / 1.12 / 46 |
| 139 | 7.5% / 0.86 / 27 | -0.1% / -0.00 / 16 | 18.2% / 1.60 / 20 | 11.0% / 2.04 / 24 | -0.6% / 0.01 / 42 |
| 140 | -0.7% / -0.05 / 36 | 5.4% / 1.49 / 20 | 13.7% / 1.50 / 25 | 6.6% / 1.18 / 30 | 3.0% / 0.36 / 55 |
| 141 | 1.0% / 0.14 / 52 | 10.2% / 1.97 / 35 | 19.0% / 1.33 / 34 | 11.7% / 1.75 / 40 | -1.5% / -0.04 / 68 |
| 142 | -5.3% / -0.51 / 31 | 7.4% / 1.34 / 27 | 18.9% / 1.34 / 29 | 23.8% / 2.88 / 29 | 5.3% / 0.44 / 52 |
| 143 | -1.3% / -0.09 / 30 | 3.4% / 0.57 / 23 | 9.5% / 0.63 / 27 | 21.7% / 2.69 / 25 | 10.8% / 0.85 / 45 |
| 144 | 0.1% / 0.06 / 32 | 7.8% / 1.54 / 18 | 16.1% / 1.00 / 29 | 18.9% / 2.27 / 28 | 2.5% / 0.24 / 55 |
| 145 | 5.4% / 0.74 / 34 | 4.8% / 1.24 / 16 | 10.8% / 0.83 / 23 | 13.7% / 3.20 / 21 | 0.4% / 0.10 / 47 |
| 146 | 3.0% / 0.41 / 43 | 1.2% / 0.28 / 24 | 14.9% / 1.06 / 30 | 9.3% / 2.34 / 26 | 11.2% / 1.13 / 47 |
| 147 | -1.0% / -0.05 / 38 | 15.2% / 2.37 / 34 | 8.0% / 0.78 / 23 | 10.8% / 1.66 / 33 | 4.6% / 0.39 / 63 |
| 148 | 1.6% / 0.22 / 31 | -1.1% / -0.22 / 17 | 15.6% / 1.55 / 20 | 16.0% / 2.81 / 25 | 4.4% / 0.43 / 45 |
| 149 | 5.2% / 0.57 / 31 | 1.3% / 0.26 / 16 | 10.3% / 0.80 / 21 | 18.2% / 2.47 / 21 | 3.8% / 0.35 / 46 |
| 150 | 6.3% / 0.80 / 30 | 4.3% / 1.00 / 15 | 8.4% / 0.65 / 22 | 11.7% / 2.69 / 20 | 3.8% / 0.40 / 39 |
| 151 | -1.6% / -0.13 / 28 | 3.0% / 0.72 / 10 | 8.0% / 0.74 / 18 | 11.0% / 2.76 / 15 | 12.4% / 1.14 / 41 |
| 152 | -3.5% / -0.35 / 35 | 8.3% / 1.56 / 28 | 27.3% / 1.90 / 31 | 25.0% / 2.68 / 34 | -6.6% / -0.34 / 68 |
| 153 | 3.9% / 0.63 / 36 | 1.5% / 0.35 / 24 | 10.3% / 0.76 / 28 | 7.7% / 1.88 / 26 | 7.9% / 0.89 / 42 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_5ee1` | 5 | 0.82 | 0.91/0.98 | 0.78/0.95 |
| 1 | `cfg_af71` | 5 | 0.88 | 0.80/0.90 | 0.70/0.85 |
| 2 | `cfg_1dcc` | 5 | 0.86 | 0.83/0.89 | 0.76/0.81 |
| 3 | `cfg_6615` | 4 | 0.87 | 0.83/0.86 | 0.76/0.84 |
| 4 | `cfg_5e0f` | 4 | 0.84 | 0.96/0.97 | 0.88/0.93 |
| 5 | `cfg_4530` | 6 | 0.80 | 0.80/0.95 | 0.76/0.87 |
| 6 | `cfg_5b3d` | 2 | 0.88 | 0.90/0.90 | 0.82/0.82 |
| 7 | `cfg_337d` | 4 | 0.85 | 0.81/0.85 | 0.67/0.68 |
| 8 | `cfg_06a9` | 3 | 0.81 | 0.88/0.92 | 0.79/0.86 |
| 9 | `cfg_29ff` | 2 | 0.91 | 0.90/0.90 | 0.85/0.85 |
| 10 | `cfg_0800` | 2 | 0.88 | 0.95/0.95 | 0.93/0.93 |
| 11 | `cfg_09ec` | 1 | n/a | n/a/n/a | n/a/n/a |
| 12 | `cfg_d64d` | 4 | 0.80 | 0.87/0.92 | 0.77/0.82 |
| 13 | `cfg_0d48` | 3 | 0.91 | 0.90/0.93 | 0.84/0.90 |
| 14 | `cfg_7c72` | 4 | 0.82 | 0.78/0.91 | 0.58/0.82 |
| 15 | `cfg_0e52` | 2 | 0.86 | 0.83/0.83 | 0.82/0.82 |
| 16 | `cfg_0eaa` | 2 | 0.86 | 0.92/0.92 | 0.85/0.85 |
| 17 | `cfg_0f5d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 18 | `cfg_827a` | 2 | 0.81 | 0.75/0.75 | 0.60/0.60 |
| 19 | `cfg_1ad9` | 2 | 0.92 | 0.95/0.95 | 0.94/0.94 |
| 20 | `cfg_4b85` | 4 | 0.87 | 0.94/0.96 | 0.84/0.91 |
| 21 | `cfg_1c62` | 5 | 0.87 | 0.90/0.94 | 0.78/0.91 |
| 22 | `cfg_1c93` | 2 | 0.85 | 0.88/0.88 | 0.85/0.85 |
| 23 | `cfg_d377` | 5 | 0.86 | 0.85/0.90 | 0.73/0.82 |
| 24 | `cfg_f828` | 6 | 0.85 | 0.82/0.85 | 0.65/0.81 |
| 25 | `cfg_2017` | 3 | 0.80 | 0.83/0.86 | 0.72/0.81 |
| 26 | `cfg_202f` | 4 | 0.81 | 0.84/0.89 | 0.72/0.79 |
| 27 | `cfg_f19c` | 4 | 0.82 | 0.84/0.91 | 0.73/0.79 |
| 28 | `cfg_bf72` | 4 | 0.93 | 0.97/0.98 | 0.89/0.94 |
| 29 | `cfg_2397` | 2 | 0.83 | 0.88/0.88 | 0.81/0.81 |
| 30 | `cfg_2446` | 5 | 0.83 | 0.88/0.90 | 0.71/0.76 |
| 31 | `cfg_a77e` | 3 | 0.87 | 0.83/0.84 | 0.78/0.79 |
| 32 | `cfg_7ffe` | 2 | 0.87 | 0.92/0.92 | 0.93/0.93 |
| 33 | `cfg_2989` | 2 | 0.93 | 0.88/0.88 | 0.81/0.81 |
| 34 | `cfg_6af5` | 5 | 0.85 | 0.82/0.94 | 0.68/0.90 |
| 35 | `cfg_36b9` | 4 | 0.84 | 0.80/0.84 | 0.78/0.84 |
| 36 | `cfg_661a` | 2 | 0.90 | 0.95/0.95 | 0.93/0.93 |
| 37 | `cfg_2fc7` | 2 | 0.95 | 0.91/0.91 | 0.87/0.87 |
| 38 | `cfg_306b` | 2 | 0.90 | 0.96/0.96 | 0.90/0.90 |
| 39 | `cfg_3296` | 1 | n/a | n/a/n/a | n/a/n/a |
| 40 | `cfg_335b` | 2 | 0.88 | 0.93/0.93 | 0.85/0.85 |
| 41 | `cfg_b6a3` | 4 | 0.93 | 0.96/0.98 | 0.91/0.95 |
| 42 | `cfg_9f03` | 2 | 0.89 | 0.96/0.96 | 0.90/0.90 |
| 43 | `cfg_3c44` | 2 | 0.89 | 0.89/0.89 | 0.91/0.91 |
| 44 | `cfg_3c7d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 45 | `cfg_3e1c` | 2 | 0.95 | 0.97/0.97 | 0.94/0.94 |
| 46 | `cfg_d5d7` | 2 | 0.92 | 0.93/0.93 | 0.87/0.87 |
| 47 | `cfg_3f81` | 2 | 0.93 | 0.95/0.95 | 0.87/0.87 |
| 48 | `cfg_4cf2` | 2 | 0.96 | 0.95/0.95 | 0.91/0.91 |
| 49 | `cfg_42ec` | 2 | 0.88 | 0.93/0.93 | 0.94/0.94 |
| 50 | `cfg_e3cc` | 2 | 0.97 | 0.96/0.96 | 0.93/0.93 |
| 51 | `cfg_4631` | 2 | 0.83 | 0.93/0.93 | 0.92/0.92 |
| 52 | `cfg_49a9` | 1 | n/a | n/a/n/a | n/a/n/a |
| 53 | `cfg_4c80` | 2 | 0.84 | 0.92/0.92 | 0.92/0.92 |
| 54 | `cfg_72f9` | 3 | 0.84 | 0.76/0.86 | 0.62/0.77 |
| 55 | `cfg_4f13` | 3 | 0.85 | 0.91/0.95 | 0.86/0.91 |
| 56 | `cfg_b761` | 2 | 0.88 | 0.95/0.95 | 0.89/0.89 |
| 57 | `cfg_539d` | 2 | 0.81 | 0.88/0.88 | 0.70/0.70 |
| 58 | `cfg_e14d` | 2 | 0.91 | 0.90/0.90 | 0.90/0.90 |
| 59 | `cfg_6131` | 2 | 0.93 | 0.93/0.93 | 0.85/0.85 |
| 60 | `cfg_9412` | 2 | 0.87 | 0.92/0.92 | 0.84/0.84 |
| 61 | `cfg_6722` | 3 | 0.85 | 0.87/0.92 | 0.76/0.85 |
| 62 | `cfg_d8c0` | 3 | 0.87 | 0.94/0.94 | 0.85/0.86 |
| 63 | `cfg_d9e5` | 3 | 0.85 | 0.94/0.94 | 0.91/0.92 |
| 64 | `cfg_70e9` | 2 | 0.94 | 0.96/0.96 | 0.87/0.87 |
| 65 | `cfg_753b` | 1 | n/a | n/a/n/a | n/a/n/a |
| 66 | `cfg_78a2` | 2 | 0.90 | 0.83/0.83 | 0.67/0.67 |
| 67 | `cfg_a54a` | 2 | 0.85 | 0.92/0.92 | 0.90/0.90 |
| 68 | `cfg_883c` | 2 | 0.93 | 0.96/0.96 | 0.85/0.85 |
| 69 | `cfg_8b06` | 1 | n/a | n/a/n/a | n/a/n/a |
| 70 | `cfg_915f` | 2 | 0.92 | 0.93/0.93 | 0.85/0.85 |
| 71 | `cfg_f30f` | 3 | 0.90 | 0.81/0.89 | 0.83/0.88 |
| 72 | `cfg_a304` | 1 | n/a | n/a/n/a | n/a/n/a |
| 73 | `cfg_a521` | 1 | n/a | n/a/n/a | n/a/n/a |
| 74 | `cfg_b57e` | 2 | 0.96 | 0.97/0.97 | 0.96/0.96 |
| 75 | `cfg_bee2` | 2 | 0.91 | 0.92/0.92 | 0.91/0.91 |
| 76 | `cfg_c3d1` | 2 | 0.90 | 0.91/0.91 | 0.87/0.87 |
| 77 | `cfg_feb6` | 2 | 0.87 | 0.94/0.94 | 0.89/0.89 |
| 78 | `cfg_ce20` | 1 | n/a | n/a/n/a | n/a/n/a |
| 79 | `cfg_cfd4` | 1 | n/a | n/a/n/a | n/a/n/a |
| 80 | `cfg_e312` | 2 | 0.93 | 0.94/0.94 | 0.93/0.93 |
| 81 | `cfg_e3b4` | 1 | n/a | n/a/n/a | n/a/n/a |
| 82 | `cfg_f507` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 9.455e-04 over 3150 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 284.0, participation ratio 9.3, 95%-variance components 95 (rank bound T = 1259); raw grid 3456; raw + known prior 588156
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
