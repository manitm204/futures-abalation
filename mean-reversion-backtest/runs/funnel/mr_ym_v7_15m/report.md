# Screening funnel -- mr_ym_v7_15m (development stages only)

- Code: `5342a94cdc84` (dirty working tree: True, diff sha256 `eaa7c284b6e8`)
- Config: `configs/funnel/mr_funnel_ym_v7_15m.yaml` sha256 `6306c785c4578b1c`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'YM': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `2ded5c70d9e97c49` (156 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_ym_v5 gated 61 YM candidates on 2023-2024 (9 passed) and mr_ym_v6 gated 267 (41 passed); this v7 grid was written after reading both, so YM 2023-2024 is largely in-sample for v7. The stage-4 test and 40-trade rule were also shaped by ES 2023-2024.
- Holdout 2025+ previously inspected: **False** -- No YM strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection). Correlated indices were scored on their 2025+ holdouts on 2026-10-24: two ES strategies (mr_es_v6_1h #8, #15) and an NQ portfolio (mr_nq_v7_15m #1 + mr_nq_v7_1h #119). The YM holdout is the only untouched test for this run.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 17280 | 17280 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 17280 | 17280 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 17280 | 10644 | 6636 | 0 |  | 13755 | 61.60 | 61.60 |  |
| 3 performance & risk | hard_gate | 10644 | 377 | 10267 | 0 |  | 0 | 2.18 | 3.54 |  |
| 4 parameter stability | hard_gate | 377 | 347 | 30 | 0 |  | 0 | 2.01 | 92.04 |  |
| 5 time stability | hard_gate | 347 | 340 | 7 | 0 |  | 328 | 1.97 | 97.98 |  |
| 6 deduplication | dedup | 340 | 156 |  |  | 184 |  | 0.90 | 45.88 | best 2 per cluster |
| 7 execution stress | hard_gate | 156 | 156 | 0 | 0 |  | 1 | 0.90 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 156 |  |  |  |  |  |  |  | diagnostic only: unverified: 156 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 6636 |
| s2:hard_reject:years_with_>=10_trades | 4590 |
| s3:hard_reject:max_drawdown | 18 |
| s3:hard_reject:net_return | 5024 |
| s3:hard_reject:sharpe | 10267 |
| s4:hard_reject:local_frac_profitable | 1 |
| s4:hard_reject:local_median_sharpe | 30 |
| s5:hard_reject:profitable_years | 7 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_9cfa` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-3.5, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 94/3/83 | 180 | 24.7% | 4.5% | 1.28 | -4.2% | 183 | 1.66 | 3.0% | 80.2 | 9/9 | 1.00 | 0.80 | 0.47 | 4 | 15.0% | 0.39 | 0.35 | 23.7% | 22.4% | 23.6% | 22.5%/19.0% | 13.1 (interpolated) | pass | 0.515 (unverified) | -0.06 |
| 2 | `cfg_ccac` | timeframe=15min, mean_type=sma, mean_lookback=32, std_lookback=17, entry_z=-4.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=1.3 | 66/28/104 | 198 | 28.2% | 5.1% | 1.20 | -4.7% | 183 | 1.61 | 4.0% | 87.6 | 7/7 | 0.86 | 0.46 | 0.74 | 4 | 8.7% | 0.68 | 0.54 | 27.1% | 25.5% | 28.0% | 24.0%/17.5% | 13.3 (interpolated) | pass | 0.436 (unverified) | -0.35 |
| 3 | `cfg_3866` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-3.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 87/7/86 | 180 | 23.2% | 4.3% | 1.11 | -4.2% | 252 | 1.56 | 3.2% | 80.3 | 10/10 | 1.00 | 0.78 | 0.33 | 5 | 14.9% | 0.33 | 0.45 | 22.2% | 21.1% | 20.5% | 21.7%/18.6% | 12.6 (interpolated) | pass | 0.355 (unverified) | 0.05 |
| 4 | `cfg_7a24` | timeframe=15min, mean_type=sma, mean_lookback=32, std_lookback=17, entry_z=-4.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=1.8 | 71/34/76 | 181 | 26.6% | 4.8% | 1.10 | -6.5% | 244 | 1.56 | 4.3% | 79.4 | 8/8 | 0.88 | 0.74 | 0.36 | 4 | 2.8% | 0.90 | 0.59 | 25.8% | 24.2% | 25.2% | 23.3%/19.0% | 13.9 (interpolated) | pass | 0.352 (unverified) | -0.19 |
| 5 | `cfg_6b8c` | timeframe=15min, mean_type=ema, mean_lookback=47, std_lookback=17, entry_z=-4.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 46/7/49 | 102 | 19.2% | 3.6% | 1.17 | -3.4% | 175 | 1.86 | 1.9% | 45.6 | 8/8 | 1.00 | 0.80 | 0.36 | 4 | 8.9% | 0.53 | 0.51 | 18.5% | 18.0% | 18.3% | 17.5%/14.9% | 18.0 (interpolated) | pass | 0.396 (unverified) | 0.03 |
| 6 | `cfg_1ac2` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-3.5, exit_z=-1.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 81/23/74 | 178 | 20.9% | 3.9% | 1.14 | -4.2% | 183 | 1.61 | 2.9% | 78.8 | 10/10 | 0.90 | 0.75 | 0.39 | 4 | 11.7% | 0.43 | 0.41 | 19.8% | 18.7% | 24.6% | 19.5%/15.6% | 11.7 (interpolated) | pass | 0.377 (unverified) | 0.05 |
| 7 | `cfg_0d18` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-3.5, exit_z=-1.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.3 | 153/56/173 | 382 | 32.7% | 5.8% | 1.09 | -4.8% | 329 | 1.38 | 5.5% | 168.3 | 10/10 | 1.00 | 0.82 | 0.26 | 4 | 8.5% | 0.74 | 0.48 | 30.6% | 27.3% | 30.5% | 28.1%/22.4% | 8.3 (interpolated) | pass | 0.341 (unverified) | 0.22 |
| 8 | `cfg_869d` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-4.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 158/51/0 | 209 | 29.9% | 5.4% | 0.94 | -10.0% | 238 | 1.55 | 5.9% | 91.4 | 8/8 | 1.00 | 0.78 | 0.16 | 3 | 0.9% | 0.98 | 0.43 | 28.7% | 27.5% | 39.0% | 28.0%/21.6% | 13.8 (interpolated) | pass | 0.235 (unverified) | 0.56 |
| 9 | `cfg_a764` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-4.0, exit_z=-1.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 62/126/0 | 188 | 26.1% | 4.7% | 1.04 | -4.3% | 585 | 1.60 | 3.2% | 84.1 | 9/9 | 1.00 | 0.88 | 0.16 | 5 | 10.6% | 0.58 | 0.49 | 24.8% | 24.0% | 16.3% | 23.4%/19.9% | 13.3 (interpolated) | pass | 0.300 (unverified) | 0.34 |
| 10 | `cfg_0fb1` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-3.5, exit_z=-1.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 102/145/0 | 247 | 28.8% | 5.2% | 1.04 | -4.1% | 430 | 1.53 | 4.1% | 109.6 | 10/10 | 0.90 | 0.88 | 0.17 | 4 | 7.9% | 0.72 | 0.42 | 27.1% | 26.2% | 25.7% | 26.2%/20.4% | 11.5 (interpolated) | pass | 0.303 (unverified) | 0.69 |
| 11 | `cfg_0e0a` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.3 | 104/63/150 | 317 | 31.3% | 5.6% | 1.09 | -4.2% | 375 | 1.43 | 4.8% | 139.4 | 11/11 | 0.91 | 0.67 | 0.42 | 4 | 9.7% | 0.68 | 0.51 | 29.1% | 27.2% | 32.1% | 26.9%/20.4% | 9.7 (interpolated) | pass | 0.339 (unverified) | 0.16 |
| 12 | `cfg_003c` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=17, entry_z=-4.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=1.3 | 66/12/93 | 171 | 23.5% | 4.3% | 1.00 | -4.3% | 238 | 1.56 | 3.1% | 76.5 | 9/9 | 0.89 | 0.61 | 0.40 | 4 | 1.9% | 0.95 | 0.66 | 22.7% | 21.8% | 23.8% | 20.9%/16.4% | 13.2 (interpolated) | pass | 0.284 (unverified) | -0.13 |
| 13 | `cfg_b19d` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-4.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 50/2/49 | 101 | 16.3% | 3.1% | 1.04 | -2.9% | 210 | 1.80 | 1.9% | 44.6 | 9/9 | 1.00 | 0.87 | 0.17 | 5 | 6.8% | 0.57 | 0.59 | 15.9% | 15.4% | 14.0% | 15.5%/12.3% | 15.6 (interpolated) | pass | 0.280 (unverified) | -0.10 |
| 14 | `cfg_bc1a` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-3.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 70/19/90 | 179 | 20.7% | 3.8% | 0.99 | -5.0% | 252 | 1.47 | 3.7% | 80.4 | 9/9 | 1.00 | 0.68 | 0.31 | 4 | 12.5% | 0.37 | 0.48 | 19.0% | 18.6% | 7.8% | 18.5%/15.1% | 11.5 (interpolated) | pass | 0.261 (unverified) | 0.10 |
| 15 | `cfg_cf84` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=17, entry_z=-4.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 179/84/0 | 263 | 32.6% | 5.8% | 0.90 | -7.8% | 261 | 1.42 | 7.8% | 115.7 | 8/8 | 1.00 | 0.61 | 0.29 | 4 | 9.7% | 0.69 | 0.42 | 31.3% | 29.4% | 36.8% | 30.1%/24.0% | 12.0 (interpolated) | pass | 0.215 (unverified) | 0.43 |
| 16 | `cfg_c224` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-4.0, exit_z=-1.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 95/87/0 | 182 | 28.7% | 5.2% | 1.06 | -5.3% | 238 | 1.62 | 4.1% | 80.0 | 9/9 | 1.00 | 0.80 | 0.26 | 4 | 6.8% | 0.78 | 0.52 | 27.6% | 26.3% | 22.9% | 25.9%/21.0% | 14.6 (interpolated) | pass | 0.311 (unverified) | 0.30 |
| 17 | `cfg_1bd6` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-3.5, exit_z=-1.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.3 | 101/80/133 | 314 | 27.5% | 5.0% | 1.07 | -6.1% | 430 | 1.42 | 3.8% | 138.6 | 10/10 | 1.00 | 0.90 | 0.17 | 4 | 6.0% | 0.79 | 0.46 | 25.4% | 23.4% | 26.0% | 23.4%/16.8% | 8.6 (interpolated) | pass | 0.324 (unverified) | 0.45 |
| 18 | `cfg_7328` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-4.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=1.8 | 129/30/116 | 275 | 30.1% | 5.4% | 0.95 | -5.8% | 238 | 1.38 | 6.1% | 121.2 | 10/10 | 1.00 | 0.70 | 0.26 | 4 | 6.1% | 0.80 | 0.49 | 29.0% | 27.7% | 30.5% | 26.5%/21.3% | 10.5 (interpolated) | pass | 0.243 (unverified) | 0.11 |
| 19 | `cfg_8265` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-3.5, exit_z=-1.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 50/68/56 | 174 | 15.5% | 2.9% | 1.04 | -3.5% | 208 | 1.58 | 2.4% | 76.7 | 10/10 | 1.00 | 0.65 | 0.39 | 5 | 10.1% | 0.34 | 0.50 | 14.5% | 13.3% | 15.2% | 14.7%/12.0% | 9.3 (interpolated) | pass | 0.289 (unverified) | 0.05 |
| 20 | `cfg_2844` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-3.5, exit_z=-1.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.3 | 109/118/154 | 381 | 33.4% | 5.9% | 1.19 | -5.1% | 430 | 1.43 | 4.8% | 168.4 | 10/10 | 1.00 | 0.82 | 0.37 | 4 | 8.9% | 0.74 | 0.40 | 31.1% | 28.4% | 34.2% | 29.1%/23.3% | 8.3 (interpolated) | pass | 0.434 (unverified) | 0.15 |
| 21 | `cfg_74a4` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 110/133/0 | 243 | 34.8% | 6.2% | 1.14 | -6.3% | 333 | 1.58 | 5.6% | 107.5 | 11/11 | 1.00 | 0.82 | 0.32 | 4 | 8.0% | 0.76 | 0.42 | 33.3% | 32.3% | 31.4% | 31.5%/26.2% | 13.3 (interpolated) | pass | 0.382 (unverified) | 0.32 |
| 22 | `cfg_3460` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-4.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 128/77/0 | 205 | 30.5% | 5.5% | 0.92 | -7.1% | 238 | 1.52 | 6.4% | 89.5 | 9/9 | 1.00 | 0.69 | 0.23 | 3 | 4.4% | 0.84 | 0.44 | 29.9% | 28.3% | 39.8% | 27.9%/22.4% | 13.9 (interpolated) | pass | 0.225 (unverified) | 0.45 |
| 23 | `cfg_6ef4` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=17, entry_z=-3.5, exit_z=-1.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 32/53/33 | 118 | 14.0% | 2.7% | 1.01 | -2.0% | 208 | 1.76 | 1.7% | 52.4 | 10/10 | 0.90 | 0.72 | 0.29 | 5 | 7.1% | 0.48 | 0.62 | 13.5% | 12.8% | 14.0% | 12.8%/10.3% | 11.9 (interpolated) | pass | 0.244 (unverified) | -0.19 |
| 24 | `cfg_d3d2` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-4.0, exit_z=-1.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.3 | 63/75/108 | 246 | 24.2% | 4.4% | 0.98 | -5.4% | 430 | 1.46 | 3.0% | 109.9 | 9/9 | 1.00 | 0.89 | 0.09 | 4 | 6.7% | 0.73 | 0.53 | 23.2% | 21.6% | 22.4% | 22.6%/18.2% | 9.6 (interpolated) | pass | 0.248 (unverified) | -0.04 |
| 25 | `cfg_12a6` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=17, entry_z=-3.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 68/10/67 | 145 | 19.2% | 3.6% | 0.99 | -4.8% | 208 | 1.57 | 2.7% | 64.7 | 10/10 | 0.90 | 0.76 | 0.22 | 4 | 11.0% | 0.38 | 0.51 | 18.3% | 17.0% | 14.5% | 18.3%/14.9% | 12.9 (interpolated) | pass | 0.268 (unverified) | -0.12 |
| 26 | `cfg_14a1` | timeframe=15min, mean_type=ema, mean_lookback=47, std_lookback=22, entry_z=-3.0, exit_z=-1.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 51/43/46 | 140 | 23.4% | 4.3% | 1.08 | -5.0% | 238 | 1.91 | 1.9% | 62.7 | 10/10 | 1.00 | 0.74 | 0.34 | 4 | 8.1% | 0.66 | 0.48 | 22.2% | 21.4% | 8.8% | 20.5%/17.2% | 15.6 (interpolated) | pass | 0.334 (unverified) | -0.07 |
| 27 | `cfg_f6b3` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-4.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 54/0/47 | 101 | 15.1% | 2.9% | 1.03 | -2.9% | 245 | 1.78 | 1.8% | 44.4 | 8/8 | 1.00 | 0.72 | 0.31 | 5 | 4.7% | 0.68 | 0.55 | 14.5% | 14.0% | 13.0% | 14.3%/11.5% | 14.6 (interpolated) | pass | 0.275 (unverified) | -0.19 |
| 28 | `cfg_8649` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=17, entry_z=-4.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 99/155/0 | 254 | 36.9% | 6.5% | 0.88 | -7.2% | 241 | 1.41 | 8.9% | 112.9 | 8/8 | 1.00 | 0.57 | 0.30 | 4 | 16.7% | 0.50 | 0.46 | 34.8% | 31.4% | 40.7% | 32.9%/26.7% | 13.0 (interpolated) | pass | 0.201 (unverified) | 0.58 |
| 29 | `cfg_8a00` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=17, entry_z=-4.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=1.8 | 75/17/67 | 159 | 22.5% | 4.2% | 0.93 | -5.0% | 322 | 1.50 | 3.4% | 70.6 | 10/10 | 1.00 | 0.65 | 0.28 | 4 | -2.2% | 1.14 | 0.67 | 21.6% | 21.0% | 21.9% | 19.9%/15.4% | 14.3 (interpolated) | pass | 0.243 (unverified) | -0.34 |
| 30 | `cfg_9ba0` | timeframe=15min, mean_type=ema, mean_lookback=47, std_lookback=22, entry_z=-4.0, exit_z=-1.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 80/52/0 | 132 | 22.1% | 4.1% | 0.98 | -4.2% | 238 | 1.68 | 3.0% | 58.9 | 9/9 | 1.00 | 0.66 | 0.32 | 4 | 9.8% | 0.55 | 0.52 | 21.3% | 20.4% | 16.6% | 20.5%/15.9% | 15.7 (interpolated) | pass | 0.245 (unverified) | 0.37 |
| 31 | `cfg_dba7` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=17, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 33/65/43 | 141 | 15.2% | 2.9% | 1.07 | -2.2% | 208 | 1.68 | 2.0% | 62.2 | 11/11 | 0.91 | 0.65 | 0.42 | 4 | 8.1% | 0.46 | 0.57 | 14.4% | 13.7% | 15.0% | 14.1%/11.2% | 11.1 (interpolated) | pass | 0.304 (unverified) | -0.17 |
| 32 | `cfg_eea0` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-4.0, exit_z=-1.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.3 | 45/47/70 | 162 | 16.7% | 3.1% | 0.94 | -2.6% | 430 | 1.56 | 2.0% | 71.1 | 9/9 | 1.00 | 0.84 | 0.10 | 4 | 6.0% | 0.64 | 0.62 | 15.6% | 14.7% | 9.6% | 14.2%/10.2% | 10.1 (interpolated) | pass | 0.203 (unverified) | 0.39 |
| 33 | `cfg_b8e4` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=17, entry_z=-3.5, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 58/6/57 | 121 | 15.1% | 2.9% | 0.82 | -5.6% | 208 | 1.53 | 2.2% | 53.6 | 9/9 | 1.00 | 0.81 | 0.01 | 4 | 8.4% | 0.44 | 0.62 | 14.3% | 13.7% | 14.2% | 14.4%/10.3% | 12.6 (interpolated) | pass | 0.161 (unverified) | -0.28 |
| 34 | `cfg_2a53` | timeframe=15min, mean_type=sma, mean_lookback=32, std_lookback=12, entry_z=-4.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 93/71/0 | 164 | 23.3% | 4.3% | 0.98 | -5.1% | 169 | 1.78 | 5.4% | 72.1 | 7/7 | 1.00 | 0.79 | 0.19 | 4 | 13.0% | 0.40 | 0.33 | 22.4% | 21.3% | 25.4% | 22.2%/18.8% | 13.5 (interpolated) | pass | 0.257 (unverified) | 0.70 |
| 35 | `cfg_6a8e` | timeframe=15min, mean_type=sma, mean_lookback=32, std_lookback=12, entry_z=-4.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 74/90/0 | 164 | 26.1% | 4.8% | 1.04 | -5.1% | 164 | 1.80 | 5.7% | 72.2 | 6/6 | 1.00 | 0.56 | 0.48 | 4 | 17.3% | 0.32 | 0.33 | 25.2% | 24.5% | 25.6% | 24.6%/21.1% | 15.3 (interpolated) | pass | 0.299 (unverified) | 0.40 |
| 36 | `cfg_b01b` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-3.5, exit_z=-1.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.3 | 59/150/96 | 305 | 23.0% | 4.2% | 1.11 | -4.2% | 374 | 1.46 | 3.0% | 134.0 | 9/9 | 0.89 | 0.80 | 0.31 | 4 | 6.7% | 0.69 | 0.54 | 21.4% | 19.5% | 27.4% | 19.5%/14.9% | 7.6 (interpolated) | pass | 0.361 (unverified) | 0.27 |
| 37 | `cfg_4e51` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-4.0, exit_z=-1.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 79/51/0 | 130 | 18.1% | 3.4% | 0.84 | -5.2% | 282 | 1.58 | 2.9% | 57.9 | 9/9 | 0.89 | 0.86 | -0.02 | 4 | 5.8% | 0.70 | 0.62 | 16.9% | 16.0% | 7.9% | 16.5%/11.6% | 13.3 (interpolated) | pass | 0.157 (unverified) | 0.41 |
| 38 | `cfg_295e` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-3.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 39/79/56 | 174 | 13.5% | 2.6% | 0.91 | -3.5% | 198 | 1.50 | 2.4% | 76.9 | 11/11 | 0.91 | 0.64 | 0.27 | 5 | 8.7% | 0.34 | 0.58 | 12.4% | 11.4% | 15.0% | 13.1%/10.1% | 8.3 (interpolated) | pass | 0.194 (unverified) | 0.15 |
| 39 | `cfg_e0cb` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=17, entry_z=-3.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 104/11/103 | 218 | 20.1% | 3.7% | 0.86 | -5.2% | 208 | 1.40 | 3.6% | 97.3 | 9/9 | 1.00 | 0.69 | 0.17 | 4 | 9.3% | 0.54 | 0.50 | 18.9% | 17.5% | 11.3% | 18.7%/15.5% | 9.4 (interpolated) | pass | 0.180 (unverified) | -0.04 |
| 40 | `cfg_6db0` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-4.0, exit_z=-1.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 33/166/0 | 199 | 22.1% | 4.1% | 1.13 | -2.9% | 265 | 1.73 | 2.4% | 87.7 | 8/8 | 1.00 | 0.85 | 0.28 | 4 | 7.1% | 0.66 | 0.59 | 20.9% | 20.1% | 20.2% | 20.5%/15.5% | 11.2 (interpolated) | pass | 0.376 (unverified) | 0.23 |
| 41 | `cfg_d55f` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=17, entry_z=-3.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 23/61/34 | 118 | 12.7% | 2.4% | 0.92 | -1.8% | 208 | 1.69 | 1.7% | 52.5 | 11/11 | 0.91 | 0.65 | 0.27 | 5 | 6.8% | 0.46 | 0.66 | 12.1% | 11.5% | 12.2% | 11.5%/9.1% | 10.9 (interpolated) | pass | 0.182 (unverified) | -0.10 |
| 42 | `cfg_4bc2` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.3 | 114/90/177 | 381 | 27.3% | 4.9% | 0.91 | -5.1% | 252 | 1.30 | 6.1% | 169.3 | 11/11 | 1.00 | 0.74 | 0.17 | 4 | 11.6% | 0.56 | 0.54 | 25.4% | 23.0% | 26.8% | 23.3%/17.8% | 7.4 (interpolated) | pass | 0.213 (unverified) | 0.35 |
| 43 | `cfg_ae46` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=22, entry_z=-2.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.8 | 87/18/44 | 149 | 21.4% | 4.0% | 1.05 | -3.7% | 129 | 1.67 | 3.1% | 66.0 | 10/10 | 0.90 | 0.65 | 0.41 | 4 | 8.7% | 0.58 | 0.47 | 20.4% | 19.4% | 17.1% | 18.7%/16.1% | 13.7 (interpolated) | pass | 0.294 (unverified) | 0.29 |
| 44 | `cfg_08e9` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-4.0, exit_z=-1.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.3 | 24/81/49 | 154 | 12.8% | 2.4% | 0.93 | -2.1% | 277 | 1.58 | 1.5% | 68.6 | 8/8 | 1.00 | 0.88 | 0.05 | 3 | 4.1% | 0.67 | 0.78 | 12.0% | 10.9% | 10.9% | 10.9%/8.2% | 8.4 (interpolated) | pass | 0.204 (unverified) | 0.31 |
| 45 | `cfg_6755` | timeframe=15min, mean_type=ema, mean_lookback=47, std_lookback=22, entry_z=-4.0, exit_z=-1.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.3 | 14/97/56 | 167 | 13.2% | 2.5% | 0.96 | -2.6% | 338 | 1.54 | 1.6% | 74.5 | 8/8 | 0.75 | 0.47 | 0.49 | 3 | 3.7% | 0.70 | 0.75 | 12.3% | 11.5% | 13.3% | 11.6%/8.8% | 8.4 (interpolated) | pass | 0.243 (unverified) | 0.13 |
| 46 | `cfg_b474` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=17, entry_z=-4.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=1.3 | 83/21/127 | 231 | 20.8% | 3.9% | 0.78 | -6.1% | 238 | 1.33 | 4.3% | 103.3 | 9/9 | 0.89 | 0.59 | 0.19 | 4 | 2.3% | 0.91 | 0.79 | 18.6% | 17.4% | 21.8% | 15.4%/10.6% | 8.9 (interpolated) | pass | 0.163 (unverified) | -0.12 |
| 47 | `cfg_4363` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-3.0, exit_z=-1.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 53/33/44 | 130 | 17.4% | 3.3% | 0.89 | -5.2% | 238 | 1.73 | 1.7% | 57.9 | 10/10 | 0.90 | 0.77 | 0.13 | 4 | 6.5% | 0.65 | 0.52 | 16.8% | 15.9% | 11.3% | 15.9%/13.9% | 13.5 (interpolated) | pass | 0.199 (unverified) | 0.09 |
| 48 | `cfg_3d8a` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-4.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=1.3 | 119/22/160 | 301 | 24.1% | 4.4% | 0.85 | -6.1% | 183 | 1.31 | 5.7% | 133.9 | 9/9 | 0.89 | 0.71 | 0.14 | 4 | 8.1% | 0.66 | 0.58 | 22.3% | 20.7% | 37.9% | 21.1%/15.1% | 7.9 (interpolated) | pass | 0.182 (unverified) | -0.15 |
| 49 | `cfg_2aae` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=17, entry_z=-4.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=1.8 | 91/28/87 | 206 | 23.7% | 4.3% | 0.81 | -4.4% | 320 | 1.38 | 4.6% | 91.8 | 10/10 | 0.90 | 0.67 | 0.14 | 4 | 1.2% | 0.97 | 0.70 | 22.8% | 21.7% | 16.9% | 20.4%/14.9% | 11.3 (interpolated) | pass | 0.153 (unverified) | 0.02 |
| 50 | `cfg_7669` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=22, entry_z=-4.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.3 | 32/34/59 | 125 | 16.8% | 3.2% | 0.84 | -2.6% | 319 | 1.64 | 2.0% | 55.5 | 10/10 | 1.00 | 0.71 | 0.12 | 5 | 9.6% | 0.41 | 0.76 | 16.0% | 15.3% | 8.4% | 14.2%/10.5% | 13.1 (interpolated) | pass | 0.126 (unverified) | -0.07 |
| 51 | `cfg_9178` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=17, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 19/79/43 | 141 | 14.0% | 2.7% | 1.04 | -2.1% | 208 | 1.63 | 2.1% | 62.5 | 10/10 | 0.80 | 0.61 | 0.43 | 5 | 7.2% | 0.45 | 0.54 | 13.1% | 12.2% | 7.2% | 13.1%/10.1% | 10.3 (interpolated) | pass | 0.287 (unverified) | -0.14 |
| 52 | `cfg_269c` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-4.0, exit_z=-1.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.8 | 47/54/46 | 147 | 16.6% | 3.1% | 0.90 | -2.7% | 241 | 1.55 | 2.1% | 64.3 | 10/10 | 0.80 | 0.85 | 0.05 | 4 | 4.5% | 0.73 | 0.61 | 15.8% | 14.9% | 7.1% | 14.6%/11.3% | 10.9 (interpolated) | pass | 0.177 (unverified) | 0.39 |
| 53 | `cfg_fb94` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-4.0, exit_z=-1.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.3 | 31/129/77 | 237 | 18.3% | 3.4% | 0.92 | -3.6% | 345 | 1.47 | 2.3% | 104.6 | 8/8 | 1.00 | 0.93 | -0.01 | 4 | 6.6% | 0.62 | 0.71 | 16.4% | 14.6% | 27.7% | 16.1%/11.2% | 7.7 (interpolated) | pass | 0.229 (unverified) | 0.23 |
| 54 | `cfg_d70d` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=12, entry_z=-3.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 129/125/0 | 254 | 24.9% | 4.6% | 0.79 | -8.0% | 383 | 1.46 | 8.3% | 110.9 | 9/9 | 1.00 | 0.65 | 0.14 | 4 | 12.2% | 0.45 | 0.42 | 23.4% | 21.1% | 34.2% | 25.9%/19.9% | 9.6 (interpolated) | pass | 0.140 (unverified) | 0.37 |
| 55 | `cfg_1fd4` | timeframe=15min, mean_type=ema, mean_lookback=47, std_lookback=17, entry_z=-3.5, exit_z=-1.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 36/69/51 | 156 | 15.9% | 3.0% | 0.86 | -3.3% | 208 | 1.61 | 2.2% | 68.9 | 10/10 | 0.90 | 0.69 | 0.17 | 4 | 5.7% | 0.64 | 0.65 | 14.9% | 13.9% | 16.5% | 14.8%/11.7% | 10.6 (interpolated) | pass | 0.153 (unverified) | -0.29 |
| 56 | `cfg_6926` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-4.0, exit_z=-1.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.8 | 62/92/65 | 219 | 24.5% | 4.5% | 0.98 | -3.7% | 375 | 1.50 | 3.1% | 97.7 | 10/10 | 0.90 | 0.73 | 0.25 | 4 | 7.8% | 0.68 | 0.52 | 23.1% | 22.2% | 15.7% | 22.3%/16.8% | 10.5 (interpolated) | pass | 0.254 (unverified) | 0.04 |
| 57 | `cfg_5d32` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=22, entry_z=-4.0, exit_z=-1.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 68/33/0 | 101 | 20.3% | 3.8% | 0.96 | -3.7% | 175 | 1.90 | 2.2% | 44.8 | 9/9 | 0.89 | 0.72 | 0.24 | 5 | 10.1% | 0.49 | 0.55 | 19.7% | 19.0% | 10.7% | 18.2%/13.6% | 18.8 (interpolated) | pass | 0.227 (unverified) | 0.14 |
| 58 | `cfg_c2b9` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=22, entry_z=-4.0, exit_z=-1.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.3 | 50/16/59 | 125 | 15.1% | 2.9% | 0.80 | -2.3% | 214 | 1.59 | 1.8% | 55.5 | 9/9 | 0.89 | 0.74 | 0.06 | 5 | 9.0% | 0.39 | 0.72 | 14.5% | 13.7% | 7.0% | 13.5%/9.5% | 12.0 (interpolated) | pass | 0.116 (unverified) | 0.06 |
| 59 | `cfg_67c3` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-3.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.3 | 64/132/182 | 378 | 29.1% | 5.2% | 0.92 | -4.7% | 142 | 1.31 | 6.5% | 169.3 | 10/10 | 1.00 | 0.64 | 0.28 | 4 | 11.8% | 0.57 | 0.55 | 27.0% | 25.3% | 29.0% | 26.7%/19.0% | 7.7 (interpolated) | pass | 0.217 (unverified) | 0.41 |
| 60 | `cfg_4f6c` | timeframe=15min, mean_type=sma, mean_lookback=47, std_lookback=17, entry_z=-3.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 260/230/0 | 490 | 52.7% | 8.8% | 0.89 | -12.2% | 146 | 1.35 | 15.5% | 218.0 | 10/10 | 1.00 | 0.71 | 0.18 | 5 | 26.8% | 0.41 | 0.43 | 49.8% | 46.7% | 45.5% | 48.3%/36.1% | 10.0 (interpolated) | pass | 0.222 (unverified) | 0.37 |
| 61 | `cfg_329f` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=17, entry_z=-4.0, exit_z=-1.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 57/31/69 | 157 | 16.5% | 3.1% | 0.92 | -3.1% | 208 | 1.54 | 2.6% | 68.9 | 9/9 | 0.89 | 0.72 | 0.20 | 4 | 7.4% | 0.55 | 0.58 | 15.6% | 14.7% | 19.6% | 15.4%/12.2% | 10.7 (interpolated) | pass | 0.199 (unverified) | 0.31 |
| 62 | `cfg_007b` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-3.0, exit_z=-1.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 85/29/80 | 194 | 21.2% | 3.9% | 0.85 | -7.2% | 241 | 1.49 | 2.9% | 86.5 | 10/10 | 1.00 | 0.78 | 0.07 | 4 | 6.7% | 0.72 | 0.56 | 20.1% | 18.9% | 3.9% | 19.6%/15.3% | 10.5 (interpolated) | pass | 0.173 (unverified) | 0.08 |
| 63 | `cfg_eec4` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=17, entry_z=-3.5, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 112/11/125 | 248 | 21.0% | 3.9% | 0.80 | -7.6% | 241 | 1.34 | 4.4% | 110.8 | 9/9 | 1.00 | 0.66 | 0.15 | 4 | 12.6% | 0.40 | 0.55 | 19.4% | 17.6% | 13.3% | 18.7%/13.5% | 8.5 (interpolated) | pass | 0.154 (unverified) | -0.30 |
| 64 | `cfg_e6a0` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-3.5, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 109/38/0 | 147 | 20.8% | 3.9% | 0.90 | -7.3% | 238 | 1.58 | 3.9% | 65.1 | 9/9 | 1.00 | 0.70 | 0.20 | 4 | 10.6% | 0.48 | 0.35 | 19.7% | 18.9% | 16.3% | 18.3%/14.8% | 12.9 (interpolated) | pass | 0.218 (unverified) | 0.40 |
| 65 | `cfg_6450` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=17, entry_z=-4.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 73/5/81 | 159 | 16.8% | 3.2% | 0.90 | -3.5% | 241 | 1.47 | 2.8% | 69.9 | 8/8 | 1.00 | 0.74 | 0.16 | 4 | 7.8% | 0.54 | 0.57 | 15.9% | 15.0% | 16.1% | 15.8%/12.6% | 10.8 (interpolated) | pass | 0.188 (unverified) | 0.08 |
| 66 | `cfg_a2e1` | timeframe=15min, mean_type=ema, mean_lookback=47, std_lookback=22, entry_z=-3.0, exit_z=-1.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.8 | 51/54/33 | 138 | 19.2% | 3.6% | 0.90 | -5.7% | 238 | 1.66 | 2.0% | 62.0 | 11/11 | 0.91 | 0.62 | 0.28 | 4 | 5.9% | 0.70 | 0.54 | 18.6% | 17.6% | 7.9% | 17.5%/13.7% | 13.5 (interpolated) | pass | 0.205 (unverified) | 0.08 |
| 67 | `cfg_e4ce` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-4.0, exit_z=-1.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.3 | 63/23/77 | 163 | 15.1% | 2.9% | 0.79 | -2.7% | 430 | 1.47 | 2.3% | 71.6 | 9/9 | 0.89 | 0.76 | 0.03 | 4 | 5.2% | 0.65 | 0.74 | 13.7% | 12.7% | 7.4% | 13.1%/8.6% | 9.2 (interpolated) | pass | 0.115 (unverified) | 0.26 |
| 68 | `cfg_0f8d` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-4.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.3 | 14/91/49 | 154 | 12.2% | 2.3% | 0.89 | -2.2% | 277 | 1.56 | 1.5% | 68.7 | 9/9 | 1.00 | 0.84 | 0.05 | 3 | 3.5% | 0.71 | 0.81 | 11.5% | 10.3% | 10.1% | 10.7%/7.6% | 8.0 (interpolated) | pass | 0.182 (unverified) | 0.31 |
| 69 | `cfg_a3a2` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-3.0, exit_z=-1.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 71/52/70 | 193 | 21.4% | 4.0% | 0.90 | -7.6% | 241 | 1.54 | 2.5% | 85.7 | 10/10 | 1.00 | 0.73 | 0.17 | 4 | 5.6% | 0.78 | 0.55 | 20.1% | 19.2% | 7.3% | 19.7%/16.1% | 10.6 (interpolated) | pass | 0.193 (unverified) | -0.02 |
| 70 | `cfg_eae3` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-3.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.3 | 33/175/96 | 304 | 21.0% | 3.9% | 1.03 | -4.4% | 384 | 1.42 | 3.0% | 133.7 | 10/10 | 0.90 | 0.80 | 0.22 | 4 | 5.0% | 0.75 | 0.59 | 19.4% | 17.5% | 25.1% | 16.3%/13.0% | 7.0 (interpolated) | pass | 0.293 (unverified) | 0.27 |
| 71 | `cfg_d65b` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=12, entry_z=-4.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 103/100/0 | 203 | 22.7% | 4.2% | 0.79 | -5.1% | 254 | 1.52 | 6.8% | 88.9 | 8/8 | 0.88 | 0.62 | 0.17 | 4 | 12.7% | 0.40 | 0.41 | 21.5% | 20.2% | 24.1% | 22.0%/17.9% | 10.9 (interpolated) | pass | 0.138 (unverified) | 0.38 |
| 72 | `cfg_80fd` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 114/158/0 | 272 | 27.0% | 4.9% | 0.84 | -7.8% | 286 | 1.37 | 6.4% | 120.3 | 11/11 | 1.00 | 0.74 | 0.10 | 4 | 8.4% | 0.68 | 0.54 | 25.5% | 24.6% | 26.1% | 25.0%/20.3% | 10.1 (interpolated) | pass | 0.172 (unverified) | 0.56 |
| 73 | `cfg_64e1` | timeframe=15min, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-3.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 59/71/0 | 130 | 23.7% | 4.3% | 1.04 | -4.6% | 155 | 1.80 | 4.4% | 57.7 | 7/7 | 1.00 | 0.44 | 0.60 | 5 | 13.2% | 0.41 | 0.39 | 23.3% | 22.3% | 20.2% | 22.9%/18.5% | 17.2 (interpolated) | pass | 0.294 (unverified) | 0.16 |
| 74 | `cfg_d801` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 55/24/51 | 130 | 21.1% | 3.9% | 0.95 | -4.9% | 238 | 1.79 | 2.1% | 58.4 | 11/11 | 0.91 | 0.77 | 0.18 | 4 | 9.4% | 0.57 | 0.52 | 20.6% | 19.8% | 13.3% | 19.2%/15.8% | 15.2 (interpolated) | pass | 0.242 (unverified) | 0.27 |
| 75 | `cfg_bcb5` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=17, entry_z=-3.0, exit_z=-1.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.3 | 282/142/345 | 769 | 36.1% | 6.4% | 0.88 | -9.2% | 137 | 1.22 | 11.9% | 340.1 | 10/10 | 0.90 | 0.57 | 0.31 | 5 | 11.9% | 0.61 | 0.55 | 31.0% | 25.3% | 26.1% | 31.0%/19.8% | 5.0 (interpolated) | pass | 0.218 (unverified) | 0.35 |
| 76 | `cfg_e108` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-3.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 63/204/0 | 267 | 28.7% | 5.2% | 0.85 | -7.1% | 252 | 1.38 | 6.8% | 118.7 | 10/10 | 1.00 | 0.70 | 0.15 | 4 | 8.1% | 0.70 | 0.54 | 27.5% | 25.7% | 29.9% | 26.3%/21.7% | 10.5 (interpolated) | pass | 0.179 (unverified) | 0.55 |
| 77 | `cfg_1ec6` | timeframe=15min, mean_type=ema, mean_lookback=47, std_lookback=22, entry_z=-2.5, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 152/8/126 | 286 | 30.6% | 5.5% | 0.88 | -7.4% | 238 | 1.40 | 4.5% | 126.6 | 8/8 | 0.88 | 0.60 | 0.28 | 4 | 9.1% | 0.72 | 0.60 | 27.8% | 26.8% | 0.3% | 29.2%/24.2% | 10.3 (interpolated) | pass | 0.178 (unverified) | 0.23 |
| 78 | `cfg_a657` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=22, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.3 | 47/206/129 | 382 | 18.9% | 3.5% | 0.88 | -5.5% | 359 | 1.32 | 3.7% | 167.8 | 10/10 | 0.90 | 0.56 | 0.32 | 3 | 2.6% | 0.83 | 0.65 | 16.3% | 14.3% | 25.0% | 15.6%/10.8% | 5.6 (interpolated) | pass | 0.203 (unverified) | -0.16 |
| 79 | `cfg_0dd8` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=17, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.8 | 35/72/29 | 136 | 12.1% | 2.3% | 0.80 | -4.4% | 208 | 1.50 | 2.1% | 60.3 | 12/12 | 0.92 | 0.50 | 0.30 | 4 | 4.0% | 0.68 | 0.70 | 11.5% | 11.0% | 9.7% | 11.7%/8.8% | 9.5 (interpolated) | pass | 0.130 (unverified) | 0.11 |
| 80 | `cfg_2102` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=22, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 68/30/57 | 155 | 19.3% | 3.6% | 0.91 | -4.9% | 141 | 1.64 | 2.6% | 68.9 | 10/10 | 0.90 | 0.75 | 0.16 | 4 | 9.3% | 0.51 | 0.52 | 18.4% | 16.8% | 10.8% | 17.0%/14.1% | 12.2 (interpolated) | pass | 0.212 (unverified) | 0.30 |
| 81 | `cfg_9ed1` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=17, entry_z=-3.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 100/20/128 | 248 | 19.9% | 3.7% | 0.76 | -7.6% | 241 | 1.32 | 4.7% | 110.2 | 10/10 | 1.00 | 0.65 | 0.11 | 4 | 12.5% | 0.33 | 0.58 | 18.9% | 17.5% | 3.2% | 18.0%/14.5% | 8.4 (interpolated) | pass | 0.132 (unverified) | -0.19 |
| 82 | `cfg_d0d0` | timeframe=15min, mean_type=ema, mean_lookback=47, std_lookback=17, entry_z=-3.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 130/12/130 | 272 | 27.7% | 5.0% | 0.93 | -4.7% | 156 | 1.39 | 4.7% | 121.4 | 9/9 | 1.00 | 0.63 | 0.30 | 4 | 14.7% | 0.46 | 0.46 | 25.4% | 24.0% | 16.2% | 25.9%/20.9% | 9.9 (interpolated) | pass | 0.229 (unverified) | -0.38 |
| 83 | `cfg_b5ac` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=12, entry_z=-4.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 65/56/0 | 121 | 18.3% | 3.4% | 0.82 | -5.1% | 244 | 1.64 | 3.9% | 53.6 | 8/8 | 0.88 | 0.56 | 0.26 | 5 | 12.2% | 0.33 | 0.44 | 17.9% | 17.4% | 17.7% | 17.5%/14.7% | 14.8 (interpolated) | pass | 0.155 (unverified) | 0.16 |
| 84 | `cfg_f36c` | timeframe=15min, mean_type=ema, mean_lookback=52, std_lookback=17, entry_z=-4.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 20/71/39 | 130 | 10.0% | 1.9% | 0.76 | -3.4% | 209 | 1.49 | 1.9% | 58.0 | 9/9 | 0.89 | 0.61 | 0.15 | 4 | 4.8% | 0.49 | 0.75 | 9.4% | 8.6% | 4.5% | 9.2%/6.4% | 7.9 (interpolated) | pass | 0.110 (unverified) | 0.43 |
| 85 | `cfg_11ad` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=22, entry_z=-3.0, exit_z=-1.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.3 | 87/167/132 | 386 | 18.7% | 3.5% | 0.87 | -5.6% | 359 | 1.31 | 3.6% | 169.2 | 9/9 | 1.00 | 0.61 | 0.26 | 3 | 2.4% | 0.84 | 0.66 | 16.3% | 14.5% | 21.4% | 16.5%/11.6% | 5.6 (interpolated) | pass | 0.197 (unverified) | -0.14 |
| 86 | `cfg_723b` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=17, entry_z=-4.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 94/66/0 | 160 | 24.1% | 4.4% | 0.77 | -7.4% | 330 | 1.49 | 4.9% | 70.8 | 9/9 | 1.00 | 0.63 | 0.14 | 3 | 0.5% | 0.98 | 0.64 | 23.3% | 21.0% | 23.1% | 20.4%/14.2% | 14.1 (interpolated) | pass | 0.143 (unverified) | 0.09 |
| 87 | `cfg_4334` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=17, entry_z=-3.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 348/143/0 | 491 | 49.9% | 8.4% | 0.90 | -11.5% | 261 | 1.34 | 13.5% | 217.6 | 9/9 | 1.00 | 0.60 | 0.30 | 4 | 15.7% | 0.65 | 0.47 | 47.5% | 45.1% | 30.3% | 48.0%/37.1% | 9.6 (interpolated) | pass | 0.228 (unverified) | 0.36 |
| 88 | `cfg_6b50` | timeframe=15min, mean_type=sma, mean_lookback=52, std_lookback=17, entry_z=-4.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 83/213/0 | 296 | 40.0% | 7.0% | 0.80 | -8.5% | 208 | 1.37 | 10.8% | 132.4 | 7/7 | 0.86 | 0.57 | 0.23 | 4 | 14.7% | 0.60 | 0.59 | 37.2% | 34.6% | 40.6% | 34.1%/25.8% | 12.2 (interpolated) | pass | 0.146 (unverified) | 0.90 |
| 89 | `cfg_f192` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=12, entry_z=-4.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 112/91/0 | 203 | 20.9% | 3.9% | 0.76 | -5.2% | 282 | 1.50 | 6.6% | 89.0 | 7/7 | 0.86 | 0.70 | 0.06 | 4 | 10.2% | 0.47 | 0.41 | 19.8% | 18.2% | 22.2% | 21.1%/15.4% | 10.2 (interpolated) | pass | 0.128 (unverified) | 0.57 |
| 90 | `cfg_15cb` | timeframe=15min, mean_type=sma, mean_lookback=52, std_lookback=22, entry_z=-3.5, exit_z=-1.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 61/46/80 | 187 | 26.4% | 4.8% | 0.80 | -8.0% | 141 | 1.55 | 3.1% | 83.4 | 9/9 | 0.89 | 0.63 | 0.18 | 4 | 14.0% | 0.45 | 0.64 | 25.0% | 24.2% | 8.8% | 24.7%/18.9% | 13.3 (interpolated) | pass | 0.172 (unverified) | 0.53 |
| 91 | `cfg_a815` | timeframe=15min, mean_type=ema, mean_lookback=52, std_lookback=17, entry_z=-4.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 10/81/39 | 130 | 10.5% | 2.0% | 0.78 | -3.6% | 208 | 1.51 | 2.0% | 58.0 | 8/8 | 1.00 | 0.62 | 0.17 | 4 | 5.1% | 0.49 | 0.74 | 9.9% | 9.2% | 5.4% | 9.8%/7.3% | 8.5 (interpolated) | pass | 0.117 (unverified) | 0.37 |
| 92 | `cfg_c318` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=17, entry_z=-3.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 92/20/106 | 218 | 20.5% | 3.8% | 0.81 | -4.5% | 208 | 1.38 | 4.1% | 97.2 | 10/10 | 1.00 | 0.59 | 0.22 | 4 | 10.7% | 0.48 | 0.57 | 19.1% | 18.1% | 11.2% | 19.9%/16.5% | 9.6 (interpolated) | pass | 0.152 (unverified) | -0.03 |
| 93 | `cfg_6868` | timeframe=15min, mean_type=ema, mean_lookback=47, std_lookback=22, entry_z=-2.5, exit_z=-1.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 138/30/113 | 281 | 28.8% | 5.2% | 0.85 | -7.8% | 238 | 1.40 | 4.2% | 124.0 | 9/9 | 0.89 | 0.69 | 0.15 | 4 | 8.7% | 0.72 | 0.64 | 27.1% | 25.1% | -0.4% | 26.7%/21.0% | 10.1 (interpolated) | pass | 0.155 (unverified) | 0.37 |
| 94 | `cfg_134f` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=12, entry_z=-3.5, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 143/111/0 | 254 | 22.3% | 4.1% | 0.75 | -8.3% | 314 | 1.43 | 8.0% | 111.0 | 8/8 | 1.00 | 0.69 | 0.06 | 4 | 10.2% | 0.50 | 0.44 | 20.8% | 19.5% | 31.2% | 22.9%/19.3% | 9.1 (interpolated) | pass | 0.127 (unverified) | 0.23 |
| 95 | `cfg_94e7` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=22, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 49/60/47 | 156 | 19.8% | 3.7% | 0.99 | -4.3% | 238 | 1.76 | 2.2% | 68.9 | 10/10 | 0.90 | 0.70 | 0.30 | 4 | 8.7% | 0.56 | 0.51 | 18.9% | 18.0% | 15.2% | 17.9%/15.6% | 12.6 (interpolated) | pass | 0.264 (unverified) | 0.11 |
| 96 | `cfg_8d36` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=17, entry_z=-4.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 63/106/0 | 169 | 19.0% | 3.5% | 0.76 | -5.2% | 376 | 1.49 | 4.1% | 74.4 | 10/10 | 1.00 | 0.60 | 0.15 | 3 | 2.0% | 0.88 | 0.72 | 17.8% | 17.1% | 29.1% | 17.3%/13.4% | 11.7 (interpolated) | pass | 0.121 (unverified) | 0.44 |
| 97 | `cfg_e85a` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-3.5, exit_z=-1.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 87/63/0 | 150 | 17.3% | 3.2% | 0.84 | -6.7% | 203 | 1.53 | 3.3% | 66.2 | 10/10 | 1.00 | 0.55 | 0.29 | 4 | 9.6% | 0.43 | 0.39 | 16.4% | 16.1% | 18.7% | 16.4%/13.5% | 11.8 (interpolated) | pass | 0.182 (unverified) | 0.37 |
| 98 | `cfg_516c` | timeframe=15min, mean_type=ema, mean_lookback=47, std_lookback=17, entry_z=-3.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 326/105/0 | 431 | 46.8% | 8.0% | 0.89 | -9.5% | 357 | 1.36 | 11.3% | 190.0 | 9/9 | 1.00 | 0.57 | 0.32 | 4 | 8.6% | 0.80 | 0.51 | 44.6% | 40.4% | 38.4% | 40.5%/30.6% | 10.0 (interpolated) | pass | 0.212 (unverified) | 0.21 |
| 99 | `cfg_3d5a` | timeframe=15min, mean_type=ema, mean_lookback=47, std_lookback=17, entry_z=-3.0, exit_z=-1.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.3 | 249/104/311 | 664 | 31.9% | 5.7% | 0.75 | -9.6% | 353 | 1.22 | 9.7% | 290.0 | 10/10 | 1.00 | 0.54 | 0.21 | 4 | -1.8% | 1.01 | 0.67 | 26.9% | 21.4% | 25.4% | 32.0%/19.1% | 5.0 (interpolated) | pass | 0.129 (unverified) | 0.17 |
| 100 | `cfg_53a0` | timeframe=15min, mean_type=ema, mean_lookback=47, std_lookback=17, entry_z=-4.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 40/10/52 | 102 | 13.1% | 2.5% | 0.79 | -4.8% | 188 | 1.53 | 2.1% | 45.2 | 9/9 | 1.00 | 0.55 | 0.24 | 4 | 3.2% | 0.77 | 0.79 | 12.6% | 12.0% | 4.2% | 12.4%/10.0% | 13.5 (interpolated) | pass | 0.117 (unverified) | 0.15 |
| 101 | `cfg_5c3c` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=17, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.3 | 209/203/351 | 763 | 39.0% | 6.8% | 0.88 | -11.4% | 161 | 1.22 | 12.8% | 336.4 | 11/11 | 0.91 | 0.56 | 0.33 | 5 | 16.4% | 0.52 | 0.58 | 33.1% | 30.5% | 17.6% | 34.2%/22.8% | 5.4 (interpolated) | pass | 0.207 (unverified) | 0.50 |
| 102 | `cfg_0fb9` | timeframe=15min, mean_type=sma, mean_lookback=47, std_lookback=22, entry_z=-3.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 126/21/127 | 274 | 28.6% | 5.2% | 0.80 | -8.6% | 241 | 1.41 | 4.8% | 121.1 | 9/9 | 1.00 | 0.66 | 0.14 | 4 | 15.0% | 0.46 | 0.60 | 26.5% | 24.6% | 12.1% | 26.4%/19.1% | 9.9 (interpolated) | pass | 0.165 (unverified) | 0.38 |
| 103 | `cfg_cf0d` | timeframe=15min, mean_type=sma, mean_lookback=32, std_lookback=17, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 195/232/0 | 427 | 39.9% | 7.0% | 0.80 | -9.5% | 233 | 1.30 | 14.5% | 189.2 | 8/8 | 0.88 | 0.50 | 0.30 | 5 | 18.6% | 0.47 | 0.45 | 35.5% | 32.5% | 26.5% | 32.4%/24.8% | 8.7 (interpolated) | pass | 0.170 (unverified) | 0.49 |
| 104 | `cfg_ed9f` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-3.0, exit_z=-1.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 71/91/0 | 162 | 19.8% | 3.7% | 0.78 | -6.0% | 241 | 1.54 | 2.7% | 72.0 | 10/10 | 1.00 | 0.62 | 0.16 | 4 | 7.9% | 0.61 | 0.56 | 18.8% | 18.0% | 11.4% | 17.5%/12.9% | 11.9 (interpolated) | pass | 0.135 (unverified) | 0.21 |
| 105 | `cfg_1b71` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-2.5, exit_z=-1.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 181/104/0 | 285 | 34.9% | 6.2% | 0.92 | -10.3% | 261 | 1.44 | 5.8% | 126.5 | 9/9 | 1.00 | 0.60 | 0.32 | 4 | 8.0% | 0.79 | 0.54 | 33.2% | 30.6% | 9.7% | 30.2%/23.9% | 11.3 (interpolated) | pass | 0.207 (unverified) | 0.53 |
| 106 | `cfg_25f4` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=17, entry_z=-3.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 172/80/0 | 252 | 26.2% | 4.8% | 0.76 | -9.3% | 261 | 1.38 | 7.2% | 111.3 | 9/9 | 1.00 | 0.52 | 0.24 | 4 | 9.4% | 0.63 | 0.39 | 24.4% | 22.5% | 26.3% | 24.0%/20.3% | 10.1 (interpolated) | pass | 0.132 (unverified) | 0.51 |
| 107 | `cfg_98a4` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-2.5, exit_z=-1.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 181/44/161 | 386 | 30.4% | 5.5% | 0.90 | -12.5% | 241 | 1.33 | 5.6% | 172.1 | 9/9 | 1.00 | 0.66 | 0.24 | 4 | 8.2% | 0.77 | 0.61 | 28.7% | 26.4% | 6.0% | 29.0%/24.8% | 7.9 (interpolated) | pass | 0.189 (unverified) | 0.24 |
| 108 | `cfg_24f6` | timeframe=15min, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-3.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.8 | 73/25/47 | 145 | 15.0% | 2.8% | 0.82 | -5.7% | 330 | 1.48 | 3.5% | 64.2 | 9/9 | 0.89 | 0.52 | 0.30 | 5 | 9.5% | 0.33 | 0.57 | 14.2% | 13.4% | 6.8% | 14.2%/10.8% | 10.5 (interpolated) | pass | 0.150 (unverified) | 0.13 |
| 109 | `cfg_ef40` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=12, entry_z=-4.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 79/42/0 | 121 | 17.0% | 3.2% | 0.80 | -4.5% | 270 | 1.62 | 3.6% | 53.5 | 7/7 | 1.00 | 0.67 | 0.12 | 5 | 11.2% | 0.34 | 0.46 | 16.7% | 16.0% | 16.8% | 16.4%/12.7% | 14.0 (interpolated) | pass | 0.141 (unverified) | 0.49 |
| 110 | `cfg_b95c` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-4.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 39/140/0 | 179 | 20.9% | 3.9% | 0.79 | -6.0% | 238 | 1.41 | 4.6% | 79.9 | 9/9 | 1.00 | 0.66 | 0.12 | 4 | 6.0% | 0.71 | 0.69 | 19.1% | 17.7% | 16.4% | 17.8%/13.0% | 11.3 (interpolated) | pass | 0.140 (unverified) | 0.42 |
| 111 | `cfg_b574` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=17, entry_z=-3.5, exit_z=-1.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.8 | 33/56/25 | 114 | 10.9% | 2.1% | 0.76 | -3.9% | 208 | 1.54 | 1.7% | 50.8 | 11/11 | 0.91 | 0.60 | 0.16 | 4 | 3.7% | 0.67 | 0.78 | 10.2% | 9.3% | 9.6% | 10.0%/6.7% | 9.6 (interpolated) | pass | 0.105 (unverified) | 0.18 |
| 112 | `cfg_7dd1` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=17, entry_z=-3.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 254/152/0 | 406 | 39.7% | 6.9% | 0.78 | -9.2% | 355 | 1.31 | 12.1% | 181.9 | 10/10 | 1.00 | 0.57 | 0.21 | 4 | 9.9% | 0.71 | 0.51 | 35.3% | 33.2% | 29.1% | 34.7%/26.6% | 9.4 (interpolated) | pass | 0.152 (unverified) | -0.08 |
| 113 | `cfg_6f4a` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=22, entry_z=-2.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.8 | 117/30/72 | 219 | 24.4% | 4.5% | 0.92 | -5.7% | 238 | 1.42 | 4.6% | 97.6 | 10/10 | 0.90 | 0.54 | 0.38 | 4 | 10.1% | 0.59 | 0.49 | 22.9% | 21.3% | 6.6% | 21.3%/17.3% | 10.7 (interpolated) | pass | 0.213 (unverified) | -0.06 |
| 114 | `cfg_495d` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-4.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 79/132/0 | 211 | 19.7% | 3.7% | 0.77 | -6.3% | 352 | 1.43 | 5.3% | 93.3 | 10/10 | 0.90 | 0.66 | 0.11 | 3 | 2.4% | 0.86 | 0.65 | 18.5% | 16.9% | 40.3% | 18.1%/14.3% | 9.6 (interpolated) | pass | 0.135 (unverified) | 0.27 |
| 115 | `cfg_c995` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-3.0, exit_z=-1.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 32/65/30 | 127 | 16.0% | 3.0% | 0.83 | -3.0% | 238 | 1.90 | 1.3% | 55.5 | 9/9 | 0.89 | 0.71 | 0.12 | 4 | 5.2% | 0.68 | 0.66 | 15.3% | 14.7% | 13.4% | 15.0%/12.8% | 12.6 (interpolated) | pass | 0.104 (unverified) | -0.26 |
| 116 | `cfg_e205` | timeframe=15min, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-3.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 81/49/0 | 130 | 21.5% | 4.0% | 1.02 | -3.2% | 238 | 1.80 | 4.0% | 57.5 | 8/8 | 0.88 | 0.72 | 0.30 | 5 | 11.4% | 0.45 | 0.38 | 20.6% | 20.0% | 18.4% | 20.0%/17.0% | 15.9 (interpolated) | pass | 0.282 (unverified) | 0.40 |
| 117 | `cfg_ce7c` | timeframe=15min, mean_type=ema, mean_lookback=47, std_lookback=17, entry_z=-3.0, exit_z=-1.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 106/44/111 | 261 | 24.0% | 4.4% | 0.86 | -4.2% | 267 | 1.38 | 4.2% | 116.6 | 10/10 | 1.00 | 0.60 | 0.26 | 5 | 10.6% | 0.54 | 0.50 | 22.1% | 20.4% | 16.5% | 22.0%/18.3% | 9.4 (interpolated) | pass | 0.188 (unverified) | -0.23 |
| 118 | `cfg_3962` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=22, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.8 | 49/73/33 | 155 | 15.5% | 2.9% | 0.76 | -5.0% | 238 | 1.54 | 2.3% | 68.2 | 11/11 | 0.91 | 0.64 | 0.12 | 4 | 6.0% | 0.62 | 0.65 | 14.8% | 14.0% | 15.7% | 14.7%/12.5% | 10.2 (interpolated) | pass | 0.125 (unverified) | 0.29 |
| 119 | `cfg_8880` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=22, entry_z=-2.5, exit_z=-1.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 127/15/87 | 229 | 20.5% | 3.8% | 0.79 | -5.4% | 238 | 1.41 | 3.2% | 102.5 | 9/9 | 0.78 | 0.74 | 0.05 | 4 | 8.6% | 0.59 | 0.53 | 19.5% | 17.6% | 3.8% | 18.6%/13.7% | 8.6 (interpolated) | pass | 0.139 (unverified) | 0.08 |
| 120 | `cfg_1d07` | timeframe=15min, mean_type=ema, mean_lookback=52, std_lookback=17, entry_z=-4.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 142/77/0 | 219 | 26.1% | 4.7% | 0.77 | -8.3% | 376 | 1.42 | 6.7% | 97.0 | 7/7 | 0.86 | 0.57 | 0.20 | 3 | 4.9% | 0.77 | 0.51 | 24.9% | 23.6% | 25.2% | 23.9%/19.2% | 11.9 (interpolated) | pass | 0.129 (unverified) | 0.09 |
| 121 | `cfg_3ab0` | timeframe=15min, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-3.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.8 | 10/128/8 | 146 | 8.4% | 1.6% | 0.76 | -2.6% | 208 | 1.55 | 1.7% | 65.2 | 8/8 | 0.62 | 0.47 | 0.29 | 3 | 4.3% | 0.48 | 0.80 | 7.6% | 6.8% | 8.1% | 7.2%/4.5% | 6.7 (interpolated) | pass | 0.094 (unverified) | -0.22 |
| 122 | `cfg_7c38` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-3.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.8 | 152/12/108 | 272 | 20.5% | 3.8% | 0.75 | -9.0% | 238 | 1.28 | 5.3% | 120.9 | 10/10 | 1.00 | 0.54 | 0.22 | 4 | 8.0% | 0.62 | 0.53 | 18.9% | 17.4% | 13.8% | 18.8%/14.4% | 7.6 (interpolated) | pass | 0.130 (unverified) | 0.02 |
| 123 | `cfg_4dd6` | timeframe=15min, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-3.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.8 | 19/119/8 | 146 | 8.3% | 1.6% | 0.76 | -2.6% | 208 | 1.54 | 1.7% | 65.1 | 9/9 | 0.67 | 0.61 | 0.15 | 3 | 4.2% | 0.49 | 0.81 | 7.5% | 6.8% | 8.2% | 7.5%/5.2% | 6.6 (interpolated) | pass | 0.095 (unverified) | -0.20 |
| 124 | `cfg_dfdd` | timeframe=15min, mean_type=sma, mean_lookback=32, std_lookback=17, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 31/89/65 | 185 | 16.7% | 3.1% | 1.01 | -2.9% | 296 | 1.58 | 2.6% | 80.9 | 9/9 | 1.00 | 0.39 | 0.63 | 5 | 5.6% | 0.66 | 0.57 | 15.5% | 14.4% | 14.2% | 15.4%/11.1% | 9.4 (interpolated) | pass | 0.265 (unverified) | -0.07 |
| 125 | `cfg_2e2f` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=17, entry_z=-3.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=1.3 | 243/59/309 | 611 | 33.9% | 6.0% | 0.76 | -9.7% | 354 | 1.21 | 10.9% | 271.4 | 10/10 | 1.00 | 0.48 | 0.28 | 3 | 11.0% | 0.62 | 0.57 | 30.9% | 26.6% | 27.0% | 28.0%/20.3% | 5.9 (interpolated) | pass | 0.157 (unverified) | -0.32 |
| 126 | `cfg_2cf3` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-4.0, exit_z=-1.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 111/104/0 | 215 | 22.5% | 4.1% | 0.93 | -6.1% | 352 | 1.52 | 5.1% | 95.7 | 9/9 | 1.00 | 0.67 | 0.26 | 4 | 2.8% | 0.87 | 0.51 | 21.4% | 19.9% | 41.6% | 20.6%/15.0% | 10.5 (interpolated) | pass | 0.223 (unverified) | 0.33 |
| 127 | `cfg_bc16` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=12, entry_z=-4.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 67/14/69 | 150 | 13.5% | 2.6% | 0.79 | -5.0% | 330 | 1.45 | 2.9% | 66.6 | 7/7 | 1.00 | 0.50 | 0.29 | 5 | 6.7% | 0.47 | 0.63 | 12.5% | 11.8% | 5.6% | 12.6%/10.2% | 9.4 (interpolated) | pass | 0.127 (unverified) | -0.03 |
| 128 | `cfg_b6b3` | timeframe=15min, mean_type=ema, mean_lookback=42, std_lookback=17, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.3 | 189/142/292 | 623 | 31.8% | 5.7% | 0.79 | -8.8% | 356 | 1.22 | 9.9% | 274.1 | 11/11 | 1.00 | 0.47 | 0.32 | 4 | 3.6% | 0.82 | 0.61 | 27.2% | 23.0% | 26.2% | 27.2%/19.8% | 5.3 (interpolated) | pass | 0.147 (unverified) | -0.13 |
| 129 | `cfg_fc55` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-3.0, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 159/57/0 | 216 | 24.5% | 4.5% | 0.79 | -9.7% | 238 | 1.43 | 6.0% | 95.7 | 9/9 | 1.00 | 0.59 | 0.20 | 4 | 8.0% | 0.67 | 0.40 | 23.5% | 22.5% | 20.0% | 23.4%/19.4% | 11.5 (interpolated) | pass | 0.146 (unverified) | 0.38 |
| 130 | `cfg_d701` | timeframe=15min, mean_type=sma, mean_lookback=42, std_lookback=22, entry_z=-4.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 66/115/0 | 181 | 20.4% | 3.8% | 0.80 | -5.7% | 238 | 1.42 | 4.4% | 80.7 | 10/10 | 1.00 | 0.69 | 0.12 | 4 | 7.8% | 0.62 | 0.66 | 18.8% | 17.6% | 14.7% | 17.8%/12.9% | 11.0 (interpolated) | pass | 0.146 (unverified) | 0.45 |
| 131 | `cfg_38b0` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 115/51/126 | 292 | 20.9% | 3.9% | 0.77 | -7.2% | 241 | 1.31 | 4.5% | 130.4 | 10/10 | 0.90 | 0.61 | 0.16 | 4 | 8.5% | 0.62 | 0.57 | 19.4% | 17.8% | 7.0% | 19.7%/15.9% | 7.3 (interpolated) | pass | 0.131 (unverified) | -0.00 |
| 132 | `cfg_d77d` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-3.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 57/182/0 | 239 | 23.0% | 4.2% | 0.82 | -6.5% | 307 | 1.37 | 6.0% | 106.5 | 10/10 | 1.00 | 0.55 | 0.26 | 4 | 6.6% | 0.71 | 0.58 | 21.3% | 19.6% | 16.8% | 18.9%/13.3% | 9.4 (interpolated) | pass | 0.156 (unverified) | 0.39 |
| 133 | `cfg_da46` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-2.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 142/16/140 | 298 | 23.7% | 4.3% | 0.85 | -7.2% | 324 | 1.33 | 5.0% | 132.9 | 9/9 | 0.89 | 0.63 | 0.22 | 4 | 9.1% | 0.65 | 0.50 | 21.9% | 20.7% | 12.2% | 22.1%/17.2% | 7.9 (interpolated) | pass | 0.175 (unverified) | 0.05 |
| 134 | `cfg_1d6e` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.3 | 221/161/337 | 719 | 30.7% | 5.5% | 0.78 | -11.1% | 197 | 1.20 | 11.7% | 314.5 | 11/11 | 1.00 | 0.52 | 0.26 | 5 | 20.2% | 0.32 | 0.56 | 26.6% | 21.5% | 14.0% | 26.8%/19.1% | 4.8 (interpolated) | pass | 0.158 (unverified) | 0.17 |
| 135 | `cfg_555e` | timeframe=15min, mean_type=sma, mean_lookback=47, std_lookback=17, entry_z=-3.0, exit_z=-1.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.3 | 265/184/358 | 807 | 34.4% | 6.1% | 0.82 | -10.4% | 341 | 1.20 | 12.9% | 357.5 | 10/10 | 0.80 | 0.42 | 0.40 | 4 | 9.2% | 0.68 | 0.68 | 30.1% | 25.0% | 26.5% | 26.8%/15.4% | 4.8 (interpolated) | pass | 0.169 (unverified) | 0.65 |
| 136 | `cfg_42c7` | timeframe=15min, mean_type=ema, mean_lookback=47, std_lookback=22, entry_z=-4.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.3 | 6/104/56 | 166 | 11.7% | 2.2% | 0.85 | -2.9% | 343 | 1.47 | 1.7% | 74.0 | 8/8 | 0.75 | 0.24 | 0.61 | 3 | 2.7% | 0.75 | 0.82 | 10.9% | 10.0% | 3.9% | 10.0%/6.7% | 7.8 (interpolated) | pass | 0.177 (unverified) | 0.11 |
| 137 | `cfg_5725` | timeframe=15min, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-3.5, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 75/13/70 | 158 | 13.0% | 2.5% | 0.77 | -4.0% | 223 | 1.44 | 3.1% | 69.6 | 7/7 | 0.86 | 0.50 | 0.27 | 4 | 5.2% | 0.60 | 0.74 | 12.2% | 11.4% | 3.8% | 12.7%/9.5% | 9.0 (interpolated) | pass | 0.112 (unverified) | 0.09 |
| 138 | `cfg_136b` | timeframe=15min, mean_type=sma, mean_lookback=47, std_lookback=17, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.3 | 195/240/358 | 793 | 31.2% | 5.6% | 0.78 | -9.8% | 323 | 1.18 | 13.6% | 352.0 | 11/11 | 0.82 | 0.38 | 0.40 | 4 | 13.7% | 0.51 | 0.62 | 27.1% | 22.1% | 24.1% | 23.9%/13.4% | 4.5 (interpolated) | pass | 0.153 (unverified) | 0.45 |
| 139 | `cfg_a354` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=12, entry_z=-4.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 15/102/24 | 141 | 8.7% | 1.7% | 0.76 | -3.9% | 284 | 1.54 | 1.6% | 62.9 | 8/8 | 0.75 | 0.55 | 0.21 | 4 | 3.1% | 0.62 | 0.80 | 7.9% | 7.1% | 6.8% | 7.6%/5.0% | 7.0 (interpolated) | pass | 0.098 (unverified) | 0.24 |
| 140 | `cfg_c92f` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-3.5, exit_z=-1.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 58/196/0 | 254 | 19.5% | 3.6% | 0.99 | -2.8% | 264 | 1.51 | 3.0% | 112.8 | 9/9 | 0.89 | 0.80 | 0.19 | 5 | 6.5% | 0.64 | 0.54 | 17.7% | 15.9% | 22.3% | 16.6%/12.4% | 7.7 (interpolated) | pass | 0.286 (unverified) | 0.00 |
| 141 | `cfg_b4c1` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=12, entry_z=-4.0, exit_z=-1.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 24/93/24 | 141 | 8.5% | 1.7% | 0.75 | -3.9% | 284 | 1.53 | 1.6% | 63.0 | 7/7 | 0.71 | 0.52 | 0.24 | 4 | 2.8% | 0.65 | 0.81 | 7.8% | 7.0% | 7.0% | 8.0%/5.7% | 6.9 (interpolated) | pass | 0.097 (unverified) | 0.25 |
| 142 | `cfg_c68b` | timeframe=15min, mean_type=sma, mean_lookback=32, std_lookback=17, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 53/68/64 | 185 | 16.6% | 3.1% | 1.01 | -2.9% | 511 | 1.58 | 2.5% | 80.9 | 10/10 | 1.00 | 0.39 | 0.62 | 5 | 5.3% | 0.67 | 0.56 | 15.5% | 14.5% | 14.1% | 14.6%/12.4% | 9.3 (interpolated) | pass | 0.267 (unverified) | -0.07 |
| 143 | `cfg_dd97` | timeframe=15min, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-3.5, exit_z=-1.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 65/36/57 | 158 | 14.0% | 2.7% | 0.85 | -3.5% | 208 | 1.56 | 2.8% | 69.6 | 8/8 | 0.75 | 0.56 | 0.29 | 3 | 4.9% | 0.64 | 0.69 | 12.9% | 12.2% | 7.1% | 12.9%/10.5% | 9.3 (interpolated) | pass | 0.150 (unverified) | -0.01 |
| 144 | `cfg_95de` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=22, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.8 | 31/80/39 | 150 | 15.4% | 2.9% | 0.76 | -5.5% | 182 | 1.47 | 3.2% | 66.7 | 10/10 | 0.90 | 0.55 | 0.21 | 4 | 10.6% | 0.31 | 0.65 | 14.8% | 14.1% | 10.8% | 14.4%/11.0% | 10.3 (interpolated) | pass | 0.135 (unverified) | 0.10 |
| 145 | `cfg_917a` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-3.5, exit_z=-1.5, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 27/125/0 | 152 | 9.4% | 1.8% | 0.78 | -2.8% | 411 | 1.49 | 1.8% | 67.9 | 9/9 | 0.56 | 0.01 | 0.76 | 5 | 5.5% | 0.39 | 0.60 | 8.7% | 7.9% | 8.0% | 8.7%/6.5% | 7.1 (interpolated) | pass | 0.146 (unverified) | 0.15 |
| 146 | `cfg_2d1b` | timeframe=15min, mean_type=ema, mean_lookback=52, std_lookback=17, entry_z=-4.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 69/146/0 | 215 | 31.2% | 5.6% | 0.77 | -6.9% | 315 | 1.43 | 7.8% | 94.8 | 7/7 | 0.86 | 0.49 | 0.28 | 4 | 11.2% | 0.60 | 0.54 | 29.9% | 27.9% | 29.2% | 27.2%/19.3% | 13.5 (interpolated) | pass | 0.132 (unverified) | 0.19 |
| 147 | `cfg_f961` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=17, entry_z=-3.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 22/130/0 | 152 | 9.5% | 1.8% | 0.78 | -2.8% | 411 | 1.50 | 1.8% | 67.9 | 10/10 | 0.60 | 0.16 | 0.62 | 5 | 5.6% | 0.39 | 0.60 | 8.8% | 7.9% | 8.1% | 8.7%/6.6% | 7.1 (interpolated) | pass | 0.147 (unverified) | 0.19 |
| 148 | `cfg_eedd` | timeframe=15min, mean_type=ema, mean_lookback=32, std_lookback=17, entry_z=-4.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.8 | 29/42/36 | 107 | 13.9% | 2.6% | 0.86 | -2.8% | 196 | 1.60 | 2.1% | 46.9 | 9/9 | 0.89 | 0.50 | 0.36 | 3 | 0.6% | 0.95 | 0.82 | 13.3% | 12.4% | 9.1% | 12.1%/9.0% | 13.4 (interpolated) | pass | 0.151 (unverified) | 0.42 |
| 149 | `cfg_101e` | timeframe=15min, mean_type=sma, mean_lookback=47, std_lookback=27, entry_z=-4.0, exit_z=-1.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 7/112/0 | 119 | 10.3% | 2.0% | 0.76 | -4.9% | 430 | 1.61 | 1.4% | 52.6 | 8/8 | 1.00 | 0.53 | 0.23 | 3 | 0.3% | 1.00 | 0.95 | 9.7% | 8.4% | 4.4% | 9.1%/6.7% | 8.9 (interpolated) | pass | 0.110 (unverified) | 0.02 |
| 150 | `cfg_133e` | timeframe=15min, mean_type=sma, mean_lookback=47, std_lookback=27, entry_z=-4.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 1/118/0 | 119 | 10.2% | 2.0% | 0.76 | -4.9% | 664 | 1.60 | 1.5% | 52.6 | 8/8 | 1.00 | 0.54 | 0.22 | 3 | 0.3% | 1.00 | 0.96 | 9.6% | 8.4% | 4.2% | 9.0%/6.0% | 8.8 (interpolated) | pass | 0.108 (unverified) | 0.06 |
| 151 | `cfg_8516` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-3.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 14/239/0 | 253 | 18.0% | 3.4% | 0.92 | -3.0% | 299 | 1.47 | 3.1% | 112.1 | 9/9 | 0.78 | 0.68 | 0.24 | 5 | 4.6% | 0.72 | 0.58 | 16.0% | 14.3% | 12.0% | 15.3%/11.5% | 7.2 (interpolated) | pass | 0.243 (unverified) | -0.12 |
| 152 | `cfg_3f7a` | timeframe=15min, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 57/43/58 | 158 | 12.1% | 2.3% | 0.78 | -3.7% | 211 | 1.47 | 2.9% | 70.1 | 9/9 | 0.78 | 0.49 | 0.29 | 4 | 6.2% | 0.46 | 0.69 | 11.1% | 10.1% | 6.5% | 11.3%/7.8% | 8.3 (interpolated) | pass | 0.117 (unverified) | -0.15 |
| 153 | `cfg_4a28` | timeframe=15min, mean_type=ema, mean_lookback=32, std_lookback=17, entry_z=-4.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=1.8 | 42/22/43 | 107 | 16.5% | 3.1% | 0.91 | -5.4% | 202 | 1.58 | 2.5% | 46.9 | 8/8 | 0.88 | 0.49 | 0.42 | 3 | 1.2% | 0.93 | 0.73 | 15.9% | 15.4% | 8.9% | 14.8%/10.2% | 16.2 (interpolated) | pass | 0.219 (unverified) | 0.10 |
| 154 | `cfg_33c9` | timeframe=15min, mean_type=ema, mean_lookback=32, std_lookback=12, entry_z=-3.5, exit_z=-1.5, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 90/40/0 | 130 | 18.6% | 3.5% | 0.90 | -3.5% | 165 | 1.75 | 3.8% | 57.4 | 7/7 | 0.86 | 0.55 | 0.35 | 4 | 7.0% | 0.60 | 0.50 | 18.0% | 17.0% | 16.0% | 17.3%/14.4% | 14.0 (interpolated) | pass | 0.189 (unverified) | 0.62 |
| 155 | `cfg_9dc5` | timeframe=15min, mean_type=ema, mean_lookback=37, std_lookback=22, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 93/201/0 | 294 | 23.1% | 4.2% | 0.82 | -5.8% | 159 | 1.35 | 5.0% | 130.2 | 11/11 | 0.82 | 0.47 | 0.35 | 3 | 4.6% | 0.78 | 0.52 | 21.0% | 18.9% | 14.2% | 20.9%/14.4% | 7.9 (interpolated) | pass | 0.167 (unverified) | -0.12 |
| 156 | `cfg_4af8` | timeframe=15min, mean_type=sma, mean_lookback=37, std_lookback=22, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.3 | 22/75/30 | 127 | 15.4% | 2.9% | 0.81 | -3.3% | 238 | 1.86 | 1.3% | 55.7 | 10/10 | 0.90 | 0.57 | 0.23 | 4 | 5.1% | 0.68 | 0.68 | 14.8% | 14.1% | 14.6% | 14.1%/11.7% | 12.2 (interpolated) | pass | 0.091 (unverified) | -0.29 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 5.9% / 1.45 / 42 | 5.9% / 2.60 / 31 | 8.5% / 1.70 / 37 | 2.9% / 1.41 / 25 | -0.4% / -0.09 / 45 |
| 2 | 1.6% / 0.53 / 38 | 4.8% / 1.52 / 42 | 18.0% / 2.44 / 43 | 5.0% / 1.79 / 28 | -2.7% / -0.68 / 47 |
| 3 | 6.3% / 1.53 / 42 | 7.3% / 2.54 / 31 | 6.3% / 1.15 / 37 | 1.2% / 0.48 / 25 | 0.4% / 0.14 / 45 |
| 4 | 0.1% / 0.05 / 36 | 2.9% / 1.03 / 39 | 23.2% / 3.08 / 40 | 4.1% / 1.51 / 25 | -4.2% / -0.93 / 41 |
| 5 | 5.3% / 1.68 / 19 | 2.9% / 1.50 / 17 | 9.4% / 1.89 / 26 | 2.1% / 1.27 / 8 | -1.6% / -0.57 / 32 |
| 6 | 4.5% / 1.16 / 42 | 5.0% / 2.44 / 31 | 8.2% / 1.65 / 36 | 2.2% / 1.22 / 25 | -0.4% / -0.11 / 44 |
| 7 | 1.8% / 0.48 / 75 | 6.2% / 1.84 / 73 | 22.4% / 2.26 / 85 | 2.4% / 0.89 / 63 | -2.1% / -0.40 / 86 |
| 8 | -0.8% / -0.10 / 46 | 2.6% / 0.84 / 37 | 28.8% / 2.95 / 46 | 7.9% / 2.56 / 33 | -8.2% / -1.47 / 47 |
| 9 | 5.7% / 1.37 / 38 | 2.5% / 0.95 / 36 | 14.0% / 1.81 / 40 | 1.8% / 0.71 / 30 | 0.3% / 0.08 / 44 |
| 10 | 1.6% / 0.34 / 51 | 4.6% / 1.54 / 47 | 19.4% / 2.31 / 59 | 1.6% / 0.62 / 39 | -0.2% / -0.01 / 51 |
| 11 | 0.6% / 0.19 / 65 | 7.2% / 2.00 / 59 | 19.6% / 2.07 / 73 | 2.1% / 0.78 / 52 | -0.3% / -0.04 / 68 |
| 12 | 2.2% / 0.69 / 34 | 2.8% / 1.15 / 30 | 21.2% / 2.61 / 33 | 0.7% / 0.29 / 27 | -3.7% / -1.03 / 47 |
| 13 | 1.9% / 0.77 / 23 | 2.7% / 1.19 / 19 | 8.9% / 1.76 / 24 | 1.0% / 0.70 / 12 | 1.1% / 0.44 / 23 |
| 14 | 6.3% / 1.43 / 42 | 7.2% / 2.53 / 31 | 6.0% / 1.20 / 37 | 1.9% / 0.71 / 25 | -2.1% / -0.50 / 44 |
| 15 | 4.1% / 0.62 / 64 | 2.9% / 0.71 / 44 | 20.9% / 2.00 / 53 | 7.0% / 1.78 / 41 | -4.2% / -0.65 / 61 |
| 16 | 5.5% / 1.30 / 38 | 3.2% / 1.23 / 35 | 20.5% / 2.34 / 40 | 2.1% / 0.86 / 28 | -3.9% / -0.82 / 41 |
| 17 | 1.3% / 0.40 / 65 | 6.2% / 1.97 / 59 | 20.4% / 2.39 / 71 | 0.8% / 0.33 / 51 | -2.2% / -0.48 / 68 |
| 18 | 2.7% / 0.50 / 62 | 4.0% / 1.25 / 53 | 22.6% / 2.26 / 56 | 4.4% / 1.45 / 40 | -4.8% / -0.93 / 64 |
| 19 | 3.7% / 1.01 / 43 | 4.4% / 2.38 / 31 | 4.9% / 1.31 / 34 | 1.0% / 0.76 / 24 | 0.7% / 0.27 / 42 |
| 20 | 2.2% / 0.62 / 75 | 6.5% / 1.88 / 73 | 22.6% / 2.54 / 83 | 1.8% / 0.65 / 62 | -1.8% / -0.34 / 88 |
| 21 | 1.0% / 0.24 / 50 | 5.9% / 1.67 / 46 | 24.8% / 2.62 / 59 | 3.8% / 1.33 / 39 | -2.7% / -0.48 / 49 |
| 22 | -0.7% / -0.08 / 45 | 3.0% / 0.84 / 36 | 25.0% / 2.52 / 45 | 7.7% / 2.44 / 32 | -5.2% / -0.87 / 47 |
| 23 | 4.4% / 1.47 / 26 | 1.4% / 1.15 / 18 | 6.4% / 1.48 / 27 | 0.8% / 0.74 / 9 | 0.4% / 0.16 / 38 |
| 24 | 4.3% / 1.20 / 46 | 3.5% / 1.25 / 47 | 16.4% / 2.02 / 53 | 0.9% / 0.37 / 41 | -2.0% / -0.47 / 59 |
| 25 | 7.4% / 2.07 / 32 | 3.4% / 1.73 / 23 | 6.6% / 1.09 / 31 | 2.8% / 1.58 / 13 | -2.1% / -0.61 / 46 |
| 26 | 5.8% / 2.52 / 25 | 3.6% / 2.19 / 26 | 14.1% / 1.75 / 31 | 2.9% / 1.36 / 17 | -4.1% / -1.55 / 41 |
| 27 | 1.7% / 0.71 / 23 | 1.6% / 1.00 / 19 | 9.9% / 2.05 / 24 | 0.8% / 0.62 / 12 | 0.6% / 0.24 / 23 |
| 28 | 4.5% / 0.67 / 62 | 1.8% / 0.40 / 42 | 17.3% / 1.42 / 50 | 10.1% / 2.23 / 41 | -0.3% / -0.01 / 59 |
| 29 | 1.0% / 0.31 / 31 | 0.5% / 0.22 / 27 | 25.3% / 3.13 / 31 | 0.7% / 0.26 / 26 | -4.4% / -1.01 / 44 |
| 30 | 7.1% / 1.93 / 26 | 2.0% / 1.05 / 24 | 11.2% / 1.64 / 27 | 2.6% / 1.10 / 21 | -2.0% / -0.42 / 34 |
| 31 | 6.2% / 1.87 / 34 | 1.4% / 0.98 / 21 | 6.6% / 1.59 / 28 | 0.6% / 0.56 / 13 | -0.1% / -0.05 / 45 |
| 32 | 3.6% / 1.40 / 28 | 1.9% / 0.96 / 36 | 10.1% / 1.70 / 34 | 1.0% / 0.49 / 26 | -0.6% / -0.21 / 38 |
| 33 | 5.7% / 1.70 / 25 | 2.9% / 1.53 / 19 | 6.2% / 1.02 / 30 | 2.4% / 1.52 / 9 | -2.7% / -0.91 / 38 |
| 34 | -0.4% / -0.07 / 34 | 2.3% / 0.87 / 32 | 9.1% / 1.31 / 34 | 7.3% / 2.54 / 29 | 3.5% / 1.00 / 35 |
| 35 | -0.4% / -0.06 / 34 | 3.4% / 1.12 / 32 | 7.5% / 1.08 / 34 | 7.5% / 2.58 / 29 | 6.0% / 1.47 / 35 |
| 36 | 1.4% / 0.52 / 64 | 2.4% / 1.01 / 59 | 15.2% / 2.18 / 71 | -0.4% / -0.24 / 48 | 3.3% / 0.94 / 63 |
| 37 | 5.5% / 1.70 / 25 | 2.4% / 1.44 / 30 | 11.7% / 1.68 / 28 | 2.0% / 0.88 / 20 | -4.1% / -0.92 / 27 |
| 38 | 3.5% / 0.95 / 43 | 4.5% / 2.43 / 31 | 3.2% / 0.85 / 34 | 1.1% / 0.80 / 24 | 0.6% / 0.24 / 42 |
| 39 | 3.8% / 0.97 / 49 | 6.5% / 2.91 / 41 | 9.9% / 1.32 / 38 | 2.1% / 0.94 / 28 | -3.2% / -0.80 / 62 |
| 40 | 2.6% / 0.93 / 39 | 1.0% / 0.49 / 38 | 14.0% / 2.02 / 42 | -0.0% / 0.01 / 32 | 3.4% / 1.24 / 48 |
| 41 | 4.2% / 1.40 / 26 | 1.2% / 1.00 / 18 | 5.5% / 1.28 / 27 | 0.9% / 0.80 / 9 | 0.3% / 0.16 / 38 |
| 42 | 1.5% / 0.40 / 75 | 7.6% / 2.00 / 73 | 14.0% / 1.49 / 85 | 3.8% / 1.26 / 63 | -1.5% / -0.26 / 85 |
| 43 | 4.1% / 1.45 / 28 | 1.8% / 0.92 / 28 | 11.6% / 1.67 / 36 | 4.4% / 2.27 / 20 | -1.8% / -0.57 / 37 |
| 44 | 3.0% / 1.39 / 27 | -0.1% / -0.09 / 36 | 8.4% / 1.79 / 32 | -1.0% / -0.67 / 24 | 2.2% / 0.94 / 35 |
| 45 | 1.4% / 0.73 / 28 | -0.4% / -0.34 / 34 | 9.1% / 2.10 / 31 | -1.0% / -0.64 / 26 | 3.7% / 1.23 / 48 |
| 46 | 3.5% / 0.86 / 46 | 1.5% / 0.58 / 36 | 18.1% / 1.98 / 49 | 2.9% / 0.96 / 35 | -5.3% / -1.25 / 65 |
| 47 | 5.3% / 2.38 / 23 | 4.9% / 2.05 / 28 | 10.3% / 1.46 / 32 | 1.4% / 0.95 / 16 | -4.9% / -1.83 / 31 |
| 48 | 3.4% / 0.65 / 70 | 3.4% / 1.06 / 53 | 14.8% / 1.75 / 63 | 4.6% / 1.42 / 43 | -3.3% / -0.67 / 72 |
| 49 | 0.5% / 0.15 / 42 | 3.0% / 1.25 / 34 | 22.2% / 2.19 / 43 | 1.5% / 0.51 / 33 | -3.8% / -0.77 / 54 |
| 50 | 1.5% / 0.59 / 20 | 3.9% / 2.08 / 24 | 6.5% / 0.96 / 26 | 0.8% / 0.36 / 20 | 3.2% / 0.99 / 35 |
| 51 | 6.3% / 1.90 / 34 | 1.4% / 1.01 / 21 | 4.8% / 1.37 / 28 | 0.7% / 0.62 / 13 | 0.1% / 0.07 / 45 |
| 52 | 2.3% / 0.87 / 27 | 2.0% / 0.99 / 35 | 11.6% / 1.88 / 30 | 1.5% / 0.68 / 23 | -1.4% / -0.42 / 32 |
| 53 | 3.5% / 1.10 / 45 | 0.8% / 0.39 / 47 | 10.9% / 1.62 / 51 | -0.5% / -0.33 / 37 | 2.6% / 0.86 / 57 |
| 54 | -4.6% / -0.77 / 54 | 3.9% / 1.00 / 49 | 11.4% / 1.21 / 56 | 5.7% / 1.82 / 43 | 7.1% / 1.29 / 52 |
| 55 | 5.0% / 1.39 / 38 | 0.9% / 0.55 / 31 | 9.6% / 1.54 / 32 | 0.4% / 0.36 / 13 | -0.7% / -0.25 / 42 |
| 56 | 4.1% / 1.11 / 44 | 2.7% / 1.01 / 43 | 15.5% / 1.91 / 43 | 1.8% / 0.69 / 36 | -1.0% / -0.21 / 53 |
| 57 | 4.1% / 1.23 / 17 | 2.6% / 1.51 / 20 | 9.3% / 1.39 / 22 | 2.0% / 0.96 / 15 | 0.9% / 0.25 / 27 |
| 58 | 1.7% / 0.65 / 20 | 3.3% / 1.85 / 24 | 5.6% / 0.88 / 26 | 0.5% / 0.27 / 20 | 3.2% / 1.03 / 35 |
| 59 | 2.1% / 0.56 / 75 | 5.0% / 1.26 / 73 | 15.5% / 1.56 / 84 | 4.4% / 1.28 / 63 | -0.2% / -0.01 / 83 |
| 60 | 2.3% / 0.33 / 103 | 4.4% / 0.90 / 84 | 20.4% / 1.11 / 108 | 13.2% / 2.36 / 88 | 5.0% / 0.64 / 107 |
| 61 | 4.5% / 1.17 / 38 | 2.4% / 1.25 / 28 | 8.5% / 1.57 / 34 | 0.7% / 0.45 / 19 | -0.3% / -0.09 / 38 |
| 62 | 4.5% / 1.33 / 40 | 7.3% / 2.60 / 39 | 13.6% / 1.56 / 46 | 2.4% / 1.23 / 22 | -7.1% / -1.97 / 47 |
| 63 | 7.7% / 1.74 / 57 | 4.1% / 1.56 / 48 | 7.4% / 0.91 / 45 | 3.9% / 1.30 / 35 | -3.4% / -0.82 / 63 |
| 64 | 3.2% / 0.61 / 35 | 5.1% / 1.88 / 27 | 9.2% / 1.81 / 27 | 5.5% / 2.17 / 23 | -3.3% / -0.65 / 35 |
| 65 | 5.7% / 1.43 / 38 | 3.1% / 1.33 / 29 | 8.4% / 1.54 / 34 | 1.3% / 0.74 / 19 | -2.3% / -0.73 / 39 |
| 66 | 4.9% / 2.12 / 25 | 2.6% / 1.46 / 25 | 12.5% / 1.63 / 30 | 3.0% / 1.23 / 17 | -4.5% / -1.45 / 41 |
| 67 | 3.1% / 1.23 / 28 | 1.3% / 0.68 / 36 | 9.5% / 1.41 / 34 | 1.2% / 0.55 / 27 | -0.4% / -0.12 / 38 |
| 68 | 3.0% / 1.39 / 27 | -0.3% / -0.18 / 36 | 8.4% / 1.79 / 32 | -1.1% / -0.76 / 24 | 1.9% / 0.85 / 35 |
| 69 | 3.9% / 1.21 / 40 | 7.6% / 2.74 / 39 | 14.9% / 1.75 / 47 | 1.8% / 0.93 / 21 | -7.2% / -2.26 / 46 |
| 70 | 1.4% / 0.53 / 64 | 2.3% / 0.93 / 59 | 15.3% / 2.18 / 71 | -0.6% / -0.35 / 48 | 1.8% / 0.56 / 62 |
| 71 | -1.9% / -0.33 / 41 | 3.6% / 1.10 / 40 | 8.9% / 1.00 / 43 | 6.8% / 2.31 / 36 | 3.7% / 0.90 / 43 |
| 72 | 1.6% / 0.32 / 54 | 5.4% / 1.46 / 51 | 17.1% / 1.79 / 65 | 7.1% / 2.37 / 45 | -5.5% / -0.84 / 57 |
| 73 | 2.2% / 0.51 / 27 | 3.5% / 1.07 / 24 | 9.2% / 1.41 / 28 | 3.7% / 1.71 / 20 | 3.3% / 0.96 / 31 |
| 74 | 5.6% / 2.34 / 23 | 6.5% / 2.24 / 28 | 10.7% / 1.35 / 32 | 2.2% / 1.37 / 17 | -4.8% / -1.64 / 30 |
| 75 | 0.1% / 0.04 / 175 | 2.3% / 0.64 / 130 | 21.6% / 1.62 / 161 | 4.7% / 1.09 / 138 | 4.3% / 0.68 / 165 |
| 76 | 1.7% / 0.36 / 54 | 3.0% / 0.76 / 49 | 19.1% / 1.87 / 64 | 8.6% / 2.60 / 45 | -5.0% / -0.76 / 55 |
| 77 | 4.2% / 1.02 / 62 | 7.0% / 2.56 / 44 | 19.7% / 1.60 / 62 | 4.6% / 1.58 / 35 | -6.4% / -1.23 / 83 |
| 78 | -1.2% / -0.36 / 85 | 0.5% / 0.26 / 68 | 15.8% / 2.30 / 78 | -1.0% / -0.44 / 62 | 4.4% / 1.04 / 89 |
| 79 | 4.5% / 1.25 / 33 | 0.9% / 0.54 / 20 | 7.8% / 1.75 / 28 | 1.5% / 1.10 / 13 | -2.8% / -1.12 / 42 |
| 80 | 5.5% / 2.00 / 29 | 3.0% / 1.71 / 29 | 9.1% / 1.19 / 37 | 4.1% / 2.29 / 20 | -3.4% / -1.21 / 40 |
| 81 | 6.6% / 1.37 / 57 | 5.3% / 1.73 / 48 | 5.1% / 0.66 / 45 | 4.0% / 1.35 / 35 | -2.2% / -0.50 / 63 |
| 82 | 5.2% / 1.06 / 62 | 5.8% / 2.54 / 46 | 11.3% / 1.16 / 47 | 3.7% / 1.29 / 38 | -0.6% / -0.13 / 79 |
| 83 | 2.6% / 0.60 / 25 | 1.8% / 0.63 / 25 | 4.8% / 0.72 / 25 | 5.5% / 2.32 / 20 | 2.5% / 0.84 / 26 |
| 84 | 4.9% / 1.50 / 32 | 1.2% / 0.88 / 23 | 3.5% / 0.97 / 28 | 1.1% / 0.90 / 11 | -1.1% / -0.47 / 36 |
| 85 | -1.4% / -0.39 / 85 | 0.6% / 0.28 / 68 | 15.8% / 2.31 / 78 | -1.1% / -0.48 / 66 | 4.5% / 1.05 / 89 |
| 86 | -1.4% / -0.19 / 34 | 2.3% / 0.79 / 25 | 23.5% / 2.32 / 35 | 5.6% / 1.80 / 27 | -5.6% / -1.12 / 39 |
| 87 | 7.4% / 0.97 / 107 | 2.8% / 0.62 / 85 | 29.5% / 1.62 / 111 | 11.0% / 2.11 / 90 | -5.6% / -0.73 / 98 |
| 88 | 5.7% / 0.80 / 68 | 2.7% / 0.61 / 53 | 22.0% / 1.39 / 59 | 8.9% / 1.76 / 47 | -3.0% / -0.34 / 69 |
| 89 | -2.2% / -0.39 / 41 | 3.8% / 1.30 / 40 | 9.6% / 1.12 / 43 | 6.6% / 2.25 / 36 | 1.9% / 0.50 / 43 |
| 90 | 2.2% / 0.70 / 40 | 8.1% / 2.49 / 38 | 10.8% / 0.95 / 33 | 4.5% / 1.35 / 26 | -1.2% / -0.25 / 50 |
| 91 | 5.1% / 1.51 / 32 | 1.5% / 1.04 / 23 | 3.6% / 0.99 / 28 | 1.5% / 0.95 / 11 | -1.4% / -0.66 / 36 |
| 92 | 3.6% / 0.81 / 49 | 5.9% / 2.57 / 41 | 8.9% / 1.10 / 38 | 3.1% / 1.12 / 28 | -2.2% / -0.55 / 62 |
| 93 | 4.2% / 1.09 / 60 | 7.1% / 2.62 / 45 | 18.4% / 1.50 / 62 | 4.6% / 1.65 / 32 | -6.8% / -1.34 / 82 |
| 94 | -4.6% / -0.79 / 54 | 4.9% / 1.42 / 49 | 11.1% / 1.24 / 56 | 5.3% / 1.73 / 43 | 4.5% / 0.89 / 52 |
| 95 | 5.3% / 2.09 / 29 | 2.9% / 1.66 / 29 | 10.2% / 1.41 / 38 | 3.5% / 2.00 / 20 | -3.1% / -1.21 / 40 |
| 96 | -1.9% / -0.34 / 34 | 1.9% / 0.73 / 27 | 16.7% / 2.03 / 35 | 3.6% / 1.55 / 28 | -1.5% / -0.37 / 45 |
| 97 | 2.8% / 0.59 / 36 | 3.3% / 1.37 / 27 | 7.1% / 1.53 / 28 | 4.4% / 2.24 / 23 | -1.2% / -0.23 / 36 |
| 98 | 2.4% / 0.35 / 103 | 4.0% / 0.91 / 70 | 35.2% / 1.93 / 87 | 5.3% / 1.17 / 70 | -3.1% / -0.39 / 101 |
| 99 | -8.0% / -1.32 / 168 | 2.0% / 0.53 / 104 | 34.3% / 2.14 / 125 | 3.9% / 1.26 / 105 | 0.8% / 0.16 / 162 |
| 100 | 4.5% / 1.37 / 19 | 0.6% / 0.27 / 17 | 9.5% / 1.90 / 26 | 2.0% / 1.27 / 8 | -3.7% / -1.29 / 32 |
| 101 | 1.1% / 0.21 / 174 | 4.3% / 1.04 / 130 | 19.4% / 1.38 / 157 | 5.4% / 1.14 / 138 | 4.8% / 0.73 / 164 |
| 102 | 5.5% / 1.20 / 59 | 6.3% / 1.87 / 50 | 11.8% / 0.97 / 60 | 6.8% / 2.18 / 36 | -4.0% / -0.84 / 69 |
| 103 | 0.9% / 0.16 / 96 | 4.0% / 0.79 / 71 | 18.0% / 1.19 / 94 | 10.1% / 1.87 / 79 | 2.6% / 0.35 / 87 |
| 104 | 2.7% / 0.69 / 34 | 6.5% / 2.11 / 35 | 11.0% / 1.27 / 40 | 4.4% / 1.88 / 18 | -5.5% / -1.70 / 35 |
| 105 | 4.3% / 0.78 / 66 | 6.5% / 1.89 / 50 | 24.9% / 1.95 / 67 | 5.9% / 1.49 / 41 | -8.2% / -1.47 / 61 |
| 106 | 5.6% / 0.87 / 60 | 2.2% / 0.58 / 45 | 15.3% / 1.50 / 51 | 6.8% / 1.67 / 40 | -5.1% / -0.90 / 56 |
| 107 | 5.7% / 1.27 / 87 | 8.1% / 2.57 / 70 | 20.6% / 1.74 / 81 | 6.6% / 2.21 / 50 | -11.2% / -2.35 / 98 |
| 108 | 5.0% / 1.48 / 30 | 1.6% / 0.75 / 27 | 2.4% / 0.46 / 32 | 3.4% / 1.57 / 21 | 1.8% / 0.58 / 35 |
| 109 | 4.3% / 1.07 / 25 | 1.2% / 0.43 / 25 | 4.4% / 0.67 / 25 | 5.2% / 2.37 / 20 | 0.9% / 0.36 / 26 |
| 110 | 4.8% / 1.19 / 37 | 0.8% / 0.26 / 33 | 14.1% / 1.72 / 40 | 3.8% / 1.25 / 28 | -3.4% / -0.68 / 41 |
| 111 | 3.3% / 1.03 / 25 | 0.2% / 0.14 / 17 | 7.0% / 1.61 / 27 | 1.7% / 1.26 / 9 | -1.6% / -0.72 / 36 |
| 112 | 1.8% / 0.26 / 96 | 2.6% / 0.59 / 66 | 27.2% / 1.61 / 84 | 9.0% / 1.83 / 66 | -3.5% / -0.44 / 94 |
| 113 | 4.9% / 1.26 / 44 | 6.2% / 2.08 / 41 | 13.0% / 1.53 / 50 | 3.5% / 1.49 / 24 | -4.5% / -0.95 / 60 |
| 114 | -0.2% / -0.00 / 47 | 0.4% / 0.14 / 38 | 16.9% / 2.14 / 45 | 5.9% / 2.41 / 32 | -3.5% / -0.88 / 49 |
| 115 | 4.1% / 2.30 / 23 | 2.9% / 1.40 / 28 | 10.2% / 1.36 / 31 | 0.8% / 0.73 / 17 | -2.6% / -1.33 / 28 |
| 116 | 4.2% / 1.12 / 27 | 2.0% / 0.71 / 24 | 9.1% / 1.41 / 28 | 4.2% / 2.07 / 20 | 0.6% / 0.21 / 31 |
| 117 | 4.1% / 0.91 / 60 | 3.1% / 1.58 / 43 | 12.1% / 1.27 / 48 | 2.9% / 1.08 / 35 | 0.2% / 0.08 / 75 |
| 118 | 4.4% / 1.65 / 29 | 2.6% / 1.34 / 29 | 9.0% / 1.22 / 38 | 3.5% / 1.94 / 20 | -4.4% / -1.52 / 39 |
| 119 | 4.9% / 1.51 / 46 | 5.6% / 2.20 / 41 | 10.9% / 1.18 / 53 | 2.9% / 1.55 / 22 | -4.7% / -1.17 / 67 |
| 120 | -3.6% / -0.57 / 53 | 2.8% / 0.77 / 34 | 20.1% / 1.90 / 41 | 7.8% / 2.07 / 35 | -1.8% / -0.29 / 56 |
| 121 | 3.9% / 1.85 / 29 | -0.4% / -0.31 / 29 | 3.9% / 1.12 / 30 | 1.2% / 0.83 / 22 | -0.5% / -0.25 / 36 |
| 122 | 5.9% / 1.15 / 67 | 4.4% / 1.37 / 47 | 11.6% / 1.41 / 56 | 5.1% / 1.90 / 39 | -7.1% / -1.47 / 63 |
| 123 | 4.0% / 1.90 / 29 | -0.4% / -0.31 / 29 | 3.9% / 1.12 / 30 | 1.0% / 0.80 / 22 | -0.5% / -0.25 / 36 |
| 124 | 1.8% / 0.56 / 43 | 2.9% / 1.82 / 34 | 10.5% / 2.07 / 38 | 0.5% / 0.33 / 25 | 0.3% / 0.11 / 45 |
| 125 | -2.4% / -0.34 / 147 | 4.4% / 1.12 / 97 | 20.6% / 1.34 / 118 | 9.0% / 2.17 / 103 | -0.2% / 0.00 / 146 |
| 126 | 0.4% / 0.10 / 48 | 1.3% / 0.50 / 39 | 19.2% / 2.69 / 46 | 5.8% / 2.45 / 33 | -4.4% / -1.15 / 49 |
| 127 | 6.4% / 1.84 / 32 | 1.0% / 0.49 / 32 | 1.7% / 0.36 / 30 | 2.3% / 1.21 / 23 | 1.4% / 0.52 / 33 |
| 128 | -6.1% / -1.03 / 156 | 1.7% / 0.47 / 97 | 27.2% / 1.87 / 119 | 6.4% / 1.92 / 99 | 1.9% / 0.36 / 152 |
| 129 | 4.2% / 0.67 / 51 | 3.1% / 0.86 / 40 | 15.3% / 1.70 / 45 | 8.1% / 2.70 / 33 | -7.0% / -1.38 / 47 |
| 130 | 4.8% / 1.17 / 37 | 3.3% / 1.24 / 35 | 11.7% / 1.48 / 40 | 2.6% / 1.00 / 28 | -3.0% / -0.58 / 41 |
| 131 | 3.3% / 0.79 / 61 | 9.9% / 2.90 / 56 | 11.5% / 1.28 / 68 | 1.7% / 0.61 / 35 | -6.0% / -1.49 / 72 |
| 132 | 0.5% / 0.13 / 49 | 5.4% / 1.53 / 46 | 15.3% / 1.79 / 58 | 4.5% / 1.47 / 39 | -3.7% / -0.68 / 47 |
| 133 | 4.0% / 0.89 / 59 | 9.9% / 2.90 / 58 | 13.4% / 1.48 / 68 | 1.6% / 0.61 / 38 | -6.0% / -1.45 / 75 |
| 134 | 0.8% / 0.16 / 169 | 3.0% / 0.75 / 122 | 7.9% / 0.69 / 144 | 8.7% / 2.00 / 133 | 7.3% / 1.11 / 151 |
| 135 | -0.7% / -0.07 / 180 | 1.9% / 0.53 / 138 | 23.1% / 1.65 / 175 | 4.4% / 1.05 / 142 | 3.3% / 0.54 / 172 |
| 136 | 1.4% / 0.73 / 28 | -1.6% / -0.89 / 33 | 8.8% / 2.06 / 31 | -0.8% / -0.53 / 26 | 3.6% / 1.24 / 48 |
| 137 | 4.1% / 1.43 / 34 | 1.0% / 0.57 / 32 | 7.4% / 1.32 / 32 | 1.1% / 0.64 / 23 | -1.0% / -0.33 / 37 |
| 138 | -0.3% / -0.02 / 179 | 3.9% / 0.98 / 136 | 15.4% / 1.25 / 167 | 5.4% / 1.18 / 141 | 4.2% / 0.66 / 170 |
| 139 | 5.4% / 2.18 / 30 | -1.6% / -1.21 / 29 | 2.3% / 0.67 / 28 | 1.9% / 1.17 / 22 | 0.6% / 0.36 / 32 |
| 140 | 0.5% / 0.20 / 52 | 1.1% / 0.44 / 48 | 12.2% / 1.90 / 60 | 0.9% / 0.54 / 41 | 3.8% / 1.12 / 53 |
| 141 | 5.6% / 2.22 / 30 | -1.6% / -1.18 / 29 | 2.3% / 0.67 / 28 | 1.6% / 1.13 / 22 | 0.6% / 0.36 / 32 |
| 142 | 1.7% / 0.55 / 43 | 2.7% / 1.69 / 34 | 10.7% / 2.11 / 38 | 0.4% / 0.26 / 25 | 0.4% / 0.16 / 45 |
| 143 | 5.3% / 1.82 / 34 | -0.9% / -0.53 / 32 | 8.6% / 1.57 / 32 | 1.3% / 0.98 / 23 | -0.7% / -0.25 / 37 |
| 144 | 3.7% / 1.40 / 29 | 3.3% / 1.35 / 28 | 3.5% / 0.54 / 37 | 4.3% / 1.99 / 20 | -0.2% / -0.04 / 36 |
| 145 | 3.7% / 1.00 / 37 | 0.6% / 0.43 / 28 | 2.0% / 1.05 / 28 | 2.7% / 1.52 / 23 | 0.1% / 0.05 / 36 |
| 146 | 0.4% / 0.10 / 52 | 3.1% / 0.76 / 34 | 18.0% / 1.39 / 41 | 10.4% / 2.46 / 35 | -2.7% / -0.41 / 53 |
| 147 | 3.7% / 1.00 / 37 | 0.6% / 0.43 / 28 | 2.0% / 1.05 / 28 | 2.7% / 1.53 / 23 | 0.1% / 0.05 / 36 |
| 148 | -0.9% / -0.38 / 21 | 1.7% / 0.70 / 20 | 13.1% / 2.51 / 22 | 1.5% / 0.85 / 17 | -1.7% / -0.58 / 27 |
| 149 | 2.3% / 1.33 / 22 | 1.2% / 0.89 / 25 | 9.9% / 1.96 / 25 | -2.1% / -1.51 / 18 | -1.0% / -0.49 / 29 |
| 150 | 2.3% / 1.33 / 22 | 1.2% / 0.89 / 25 | 9.8% / 1.95 / 25 | -2.0% / -1.45 / 18 | -1.0% / -0.52 / 29 |
| 151 | 0.5% / 0.18 / 52 | 1.1% / 0.44 / 48 | 12.8% / 1.98 / 60 | 0.2% / 0.09 / 41 | 2.8% / 0.87 / 52 |
| 152 | 5.6% / 1.82 / 34 | -0.7% / -0.37 / 32 | 5.1% / 1.06 / 32 | 1.3% / 0.91 / 23 | 0.4% / 0.15 / 37 |
| 153 | -0.3% / -0.13 / 21 | 2.0% / 0.81 / 20 | 15.1% / 2.80 / 21 | 3.0% / 1.49 / 17 | -3.4% / -0.82 / 28 |
| 154 | 2.6% / 0.78 / 27 | 0.6% / 0.23 / 24 | 10.9% / 1.58 / 28 | 3.7% / 1.93 / 20 | -0.1% / -0.00 / 31 |
| 155 | -0.6% / -0.10 / 62 | 2.5% / 0.90 / 54 | 17.7% / 2.14 / 65 | 3.1% / 1.00 / 46 | -0.4% / -0.04 / 67 |
| 156 | 4.2% / 2.34 / 23 | 2.8% / 1.33 / 28 | 9.8% / 1.31 / 31 | 1.0% / 0.87 / 17 | -2.9% / -1.51 / 28 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_003c` | 6 | 0.87 | 0.82/0.91 | 0.62/0.75 |
| 1 | `cfg_007b` | 8 | 0.84 | 0.74/0.91 | 0.55/0.79 |
| 2 | `cfg_4f6c` | 5 | 0.82 | 0.86/0.94 | 0.78/0.86 |
| 3 | `cfg_0e0a` | 8 | 0.81 | 0.85/0.93 | 0.68/0.88 |
| 4 | `cfg_0fb1` | 13 | 0.81 | 0.57/0.82 | 0.31/0.63 |
| 5 | `cfg_ccac` | 8 | 0.82 | 0.82/0.90 | 0.54/0.71 |
| 6 | `cfg_c224` | 5 | 0.85 | 0.85/0.89 | 0.69/0.73 |
| 7 | `cfg_7328` | 7 | 0.83 | 0.78/0.83 | 0.58/0.76 |
| 8 | `cfg_4e51` | 8 | 0.88 | 0.88/0.92 | 0.76/0.93 |
| 9 | `cfg_08e9` | 9 | 0.91 | 0.91/0.95 | 0.65/0.71 |
| 10 | `cfg_869d` | 6 | 0.82 | 0.64/0.72 | 0.50/0.74 |
| 11 | `cfg_a354` | 3 | 0.99 | 1.00/1.00 | 1.00/1.00 |
| 12 | `cfg_0d18` | 5 | 0.86 | 0.62/0.80 | 0.73/0.86 |
| 13 | `cfg_0dd8` | 3 | 0.86 | 0.93/0.96 | 0.93/0.93 |
| 14 | `cfg_1b71` | 7 | 0.81 | 0.85/0.87 | 0.67/0.74 |
| 15 | `cfg_15cb` | 2 | 0.81 | 0.87/0.87 | 0.66/0.66 |
| 16 | `cfg_101e` | 3 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 17 | `cfg_eea0` | 8 | 0.83 | 0.81/0.92 | 0.54/0.93 |
| 18 | `cfg_a657` | 2 | 1.00 | 1.00/1.00 | 0.98/0.98 |
| 19 | `cfg_12a6` | 11 | 0.80 | 0.80/0.90 | 0.69/0.80 |
| 20 | `cfg_d70d` | 2 | 0.93 | 0.97/0.97 | 0.92/0.92 |
| 21 | `cfg_6db0` | 9 | 0.87 | 0.87/0.95 | 0.55/0.84 |
| 22 | `cfg_555e` | 2 | 0.89 | 0.91/0.91 | 0.92/0.92 |
| 23 | `cfg_14a1` | 6 | 0.81 | 0.92/0.93 | 0.75/0.81 |
| 24 | `cfg_f36c` | 3 | 0.95 | 0.98/0.99 | 0.98/0.99 |
| 25 | `cfg_ae46` | 4 | 0.85 | 0.88/0.89 | 0.76/0.81 |
| 26 | `cfg_4bc2` | 5 | 0.88 | 0.89/0.91 | 0.86/0.90 |
| 27 | `cfg_9cfa` | 5 | 0.82 | 0.87/0.92 | 0.67/0.74 |
| 28 | `cfg_4363` | 18 | 0.80 | 0.84/0.95 | 0.55/0.76 |
| 29 | `cfg_1d07` | 2 | 0.97 | 0.79/0.79 | 0.85/0.85 |
| 30 | `cfg_1d6e` | 1 | n/a | n/a/n/a | n/a/n/a |
| 31 | `cfg_1ec6` | 5 | 0.82 | 0.54/0.90 | 0.25/0.75 |
| 32 | `cfg_1fd4` | 1 | n/a | n/a/n/a | n/a/n/a |
| 33 | `cfg_9ba0` | 5 | 0.85 | 0.87/0.90 | 0.59/0.61 |
| 34 | `cfg_24f6` | 3 | 0.82 | 0.87/0.90 | 0.61/0.68 |
| 35 | `cfg_25f4` | 2 | 0.90 | 0.83/0.83 | 0.75/0.75 |
| 36 | `cfg_8265` | 4 | 0.87 | 0.92/0.96 | 0.70/0.87 |
| 37 | `cfg_2a53` | 3 | 0.90 | 0.96/0.97 | 0.91/0.93 |
| 38 | `cfg_b474` | 3 | 0.83 | 0.77/0.84 | 0.63/0.69 |
| 39 | `cfg_495d` | 2 | 0.94 | 0.96/0.96 | 0.94/0.94 |
| 40 | `cfg_2e2f` | 1 | n/a | n/a/n/a | n/a/n/a |
| 41 | `cfg_b5ac` | 3 | 0.88 | 0.96/0.97 | 0.87/0.90 |
| 42 | `cfg_6ef4` | 3 | 0.92 | 0.97/0.98 | 0.91/0.92 |
| 43 | `cfg_329f` | 4 | 0.83 | 0.87/0.89 | 0.77/0.79 |
| 44 | `cfg_eec4` | 4 | 0.80 | 0.68/0.72 | 0.53/0.59 |
| 45 | `cfg_33c9` | 1 | n/a | n/a/n/a | n/a/n/a |
| 46 | `cfg_3866` | 4 | 0.87 | 0.89/0.93 | 0.86/0.87 |
| 47 | `cfg_38b0` | 2 | 0.98 | 0.98/0.98 | 0.93/0.93 |
| 48 | `cfg_94e7` | 4 | 0.92 | 0.96/0.97 | 0.82/0.86 |
| 49 | `cfg_3ab0` | 6 | 0.81 | 0.75/0.96 | 0.46/0.80 |
| 50 | `cfg_7669` | 11 | 0.87 | 0.71/0.91 | 0.55/0.81 |
| 51 | `cfg_6f4a` | 9 | 0.81 | 0.85/0.87 | 0.60/0.74 |
| 52 | `cfg_3d5a` | 2 | 0.90 | 0.87/0.87 | 0.75/0.75 |
| 53 | `cfg_3f7a` | 1 | n/a | n/a/n/a | n/a/n/a |
| 54 | `cfg_6755` | 3 | 0.98 | 0.98/0.98 | 0.91/0.91 |
| 55 | `cfg_eedd` | 2 | 0.93 | 0.89/0.89 | 0.82/0.82 |
| 56 | `cfg_c92f` | 5 | 0.83 | 0.78/0.89 | 0.49/0.75 |
| 57 | `cfg_c995` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 58 | `cfg_516c` | 2 | 0.89 | 0.90/0.90 | 0.80/0.80 |
| 59 | `cfg_6b8c` | 2 | 0.91 | 0.93/0.93 | 0.78/0.78 |
| 60 | `cfg_5725` | 2 | 0.92 | 0.95/0.95 | 0.79/0.79 |
| 61 | `cfg_bcb5` | 2 | 0.95 | 0.84/0.84 | 0.89/0.89 |
| 62 | `cfg_64e1` | 2 | 0.90 | 0.95/0.95 | 0.88/0.88 |
| 63 | `cfg_a764` | 2 | 0.90 | 0.90/0.90 | 0.82/0.82 |
| 64 | `cfg_6b50` | 1 | n/a | n/a/n/a | n/a/n/a |
| 65 | `cfg_723b` | 2 | 0.90 | 0.84/0.84 | 0.66/0.66 |
| 66 | `cfg_917a` | 3 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 67 | `cfg_7c38` | 1 | n/a | n/a/n/a | n/a/n/a |
| 68 | `cfg_cf84` | 5 | 0.85 | 0.71/0.74 | 0.75/0.84 |
| 69 | `cfg_80fd` | 5 | 0.82 | 0.85/0.87 | 0.85/0.87 |
| 70 | `cfg_b19d` | 6 | 0.81 | 0.89/0.92 | 0.80/0.88 |
| 71 | `cfg_d65b` | 3 | 0.81 | 0.89/0.93 | 0.70/0.83 |
| 72 | `cfg_dba7` | 3 | 0.89 | 0.98/0.98 | 0.91/0.92 |
| 73 | `cfg_95de` | 1 | n/a | n/a/n/a | n/a/n/a |
| 74 | `cfg_9dc5` | 1 | n/a | n/a/n/a | n/a/n/a |
| 75 | `cfg_b01b` | 4 | 0.90 | 0.90/0.99 | 0.69/0.98 |
| 76 | `cfg_b95c` | 2 | 0.95 | 0.96/0.96 | 0.95/0.95 |
| 77 | `cfg_e0cb` | 2 | 0.91 | 0.94/0.94 | 0.85/0.85 |
| 78 | `cfg_dfdd` | 3 | 0.93 | 0.89/0.93 | 0.69/0.80 |
| 79 | `cfg_d0d0` | 2 | 0.92 | 0.96/0.96 | 0.88/0.88 |
| 80 | `cfg_cf0d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 81 | `cfg_d77d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 82 | `cfg_e6a0` | 2 | 0.89 | 0.90/0.90 | 0.74/0.74 |
| 83 | `cfg_ed9f` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 6.541e-04 over 16848 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 611.0, participation ratio 13.7, 95%-variance components 134 (rank bound T = 1259); raw grid 17280; raw + known prior 678588
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
