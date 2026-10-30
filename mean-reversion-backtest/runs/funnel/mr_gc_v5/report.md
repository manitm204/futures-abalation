# Screening funnel -- mr_gc_v5 (development stages only)

- Code: `5342a94cdc84` (dirty working tree: True, diff sha256 `eb245db5b3f6`)
- Config: `configs/funnel/mr_funnel_gc_v5.yaml` sha256 `9583b32f4435faf7`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'GC': '2026-10-16'}
- Frozen manifest sha256: `f38aa8cd1bc810cd` (89 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **False** -- No strategy has been tested on GC before. The v5 grid, the stage-4 test and the 40-trade rule were chosen after reading ES (and NQ/YM/RTY) results, a different asset class, so GC 2023-2024 is close to a fresh check.
- Holdout 2025+ previously inspected: **False** -- No GC strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 41472 | 41472 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 41472 | 41472 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 41472 | 29344 | 12128 | 0 |  | 32517 | 70.76 | 70.76 |  |
| 3 performance & risk | hard_gate | 29344 | 177 | 29167 | 0 |  | 0 | 0.43 | 0.60 |  |
| 4 parameter stability | hard_gate | 177 | 162 | 15 | 0 |  | 0 | 0.39 | 91.53 |  |
| 5 time stability | hard_gate | 162 | 162 | 0 | 0 |  | 123 | 0.39 | 100.00 |  |
| 6 deduplication | dedup | 162 | 89 |  |  | 73 |  | 0.21 | 54.94 | best 2 per cluster |
| 7 execution stress | hard_gate | 89 | 89 | 0 | 0 |  | 0 | 0.21 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 89 |  |  |  |  |  |  |  | diagnostic only: unverified: 89 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 12104 |
| s2:hard_reject:years_with_>=10_trades | 8105 |
| s3:hard_reject:max_drawdown | 496 |
| s3:hard_reject:net_return | 24126 |
| s3:hard_reject:sharpe | 29167 |
| s4:hard_reject:local_median_sharpe | 15 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | transfer dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_f7d6` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=40, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 12/64/31 | 107 | 39.0% | 6.9% | 1.13 | -6.4% | 181 | 1.90 | 13.1% | 59.7 | 9/9 | 0.89 | 0.67 | 0.46 | 4 | 16.9% | 0.52 | 0.66 | 38.0% | 36.6% | 22.6% | 35.0%/26.2% | 21.6 (interpolated) | pass | 0.067 (unverified) | n/a |
| 2 | `cfg_4d9f` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=40, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 16/60/31 | 107 | 36.6% | 6.6% | 1.08 | -6.4% | 187 | 1.85 | 12.8% | 59.7 | 10/10 | 0.90 | 0.71 | 0.38 | 4 | 15.5% | 0.54 | 0.70 | 35.7% | 34.7% | 22.1% | 34.9%/27.9% | 20.6 (interpolated) | pass | 0.055 (unverified) | n/a |
| 3 | `cfg_6ab2` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 24/78/42 | 144 | 36.2% | 6.5% | 1.16 | -7.6% | 263 | 1.64 | 17.0% | 78.8 | 11/11 | 0.91 | 0.63 | 0.53 | 4 | 14.8% | 0.57 | 0.55 | 34.8% | 33.6% | 26.2% | 32.0%/25.9% | 15.6 (interpolated) | pass | 0.087 (unverified) | n/a |
| 4 | `cfg_15b7` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 104/4/63 | 171 | 10.7% | 2.1% | 1.02 | -2.2% | 335 | 1.60 | 2.9% | 94.2 | 9/9 | 0.67 | 0.42 | 0.60 | 4 | 3.6% | 0.65 | 0.55 | 9.5% | 7.9% | 4.0% | 9.9%/8.1% | 5.2 (interpolated) | pass | 0.044 (unverified) | n/a |
| 5 | `cfg_6b6a` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 18/58/29 | 105 | 34.0% | 6.1% | 1.15 | -5.4% | 321 | 1.95 | 12.2% | 57.9 | 11/11 | 1.00 | 0.67 | 0.48 | 4 | 11.2% | 0.63 | 0.45 | 32.6% | 31.5% | 23.1% | 30.5%/24.9% | 19.0 (interpolated) | pass | 0.078 (unverified) | n/a |
| 6 | `cfg_52bd` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 31/45/29 | 105 | 34.8% | 6.3% | 1.19 | -5.4% | 321 | 1.97 | 11.6% | 57.8 | 12/12 | 1.00 | 0.66 | 0.53 | 4 | 12.2% | 0.61 | 0.44 | 33.7% | 32.3% | 21.6% | 30.9%/24.8% | 19.4 (interpolated) | pass | 0.091 (unverified) | n/a |
| 7 | `cfg_8f22` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 21/72/44 | 137 | 29.4% | 5.4% | 1.04 | -5.2% | 297 | 1.58 | 16.1% | 75.6 | 10/10 | 1.00 | 0.56 | 0.48 | 5 | 11.8% | 0.56 | 0.66 | 28.2% | 25.6% | 22.1% | 23.8%/15.7% | 13.4 (interpolated) | pass | 0.057 (unverified) | n/a |
| 8 | `cfg_ad59` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 103/213/0 | 316 | 22.5% | 4.2% | 0.93 | -5.5% | 451 | 1.39 | 11.9% | 172.8 | 10/10 | 0.80 | 0.63 | 0.30 | 4 | 12.9% | 0.42 | 0.38 | 19.8% | 17.2% | 21.0% | 21.9%/18.1% | 5.4 (interpolated) | pass | 0.037 (unverified) | n/a |
| 9 | `cfg_1820` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 124/10/28 | 162 | 10.8% | 2.1% | 0.95 | -2.0% | 264 | 1.59 | 3.3% | 89.9 | 10/10 | 0.80 | 0.53 | 0.42 | 5 | 4.9% | 0.54 | 0.55 | 9.7% | 8.4% | 2.8% | 10.3%/8.6% | 5.5 (interpolated) | pass | 0.040 (unverified) | n/a |
| 10 | `cfg_bee6` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 13/68/39 | 120 | 29.0% | 5.3% | 1.00 | -9.6% | 234 | 1.54 | 14.5% | 66.6 | 10/10 | 1.00 | 0.71 | 0.29 | 3 | 6.9% | 0.78 | 0.70 | 27.8% | 27.1% | 20.0% | 24.9%/18.3% | 15.6 (interpolated) | pass | 0.048 (unverified) | n/a |
| 11 | `cfg_6ff1` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 144/172/0 | 316 | 21.1% | 4.0% | 0.90 | -6.1% | 351 | 1.38 | 11.3% | 173.0 | 9/9 | 0.78 | 0.47 | 0.43 | 5 | 10.8% | 0.45 | 0.40 | 18.4% | 16.1% | 22.7% | 20.3%/18.1% | 5.1 (interpolated) | pass | 0.032 (unverified) | n/a |
| 12 | `cfg_c7be` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 33/69/44 | 146 | 30.8% | 5.6% | 1.04 | -7.7% | 263 | 1.55 | 16.6% | 79.7 | 12/12 | 0.92 | 0.59 | 0.45 | 4 | 12.6% | 0.58 | 0.58 | 29.7% | 29.1% | 23.8% | 30.3%/22.3% | 13.3 (interpolated) | pass | 0.053 (unverified) | n/a |
| 13 | `cfg_9d13` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 79/157/105 | 341 | 23.3% | 4.3% | 0.96 | -5.6% | 519 | 1.35 | 10.7% | 186.8 | 12/12 | 0.67 | 0.34 | 0.62 | 3 | 4.9% | 0.74 | 0.44 | 19.9% | 16.3% | 30.9% | 23.1%/17.9% | 5.2 (interpolated) | pass | 0.043 (unverified) | n/a |
| 14 | `cfg_f2d9` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 158/120/0 | 278 | 19.7% | 3.7% | 0.94 | -6.1% | 310 | 1.43 | 9.9% | 152.0 | 9/9 | 0.67 | 0.59 | 0.35 | 5 | 13.7% | 0.29 | 0.35 | 17.0% | 15.2% | 21.5% | 19.6%/16.1% | 5.3 (interpolated) | pass | 0.040 (unverified) | n/a |
| 15 | `cfg_b81c` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 11/115/20 | 146 | 23.3% | 4.4% | 1.04 | -3.8% | 181 | 1.64 | 11.0% | 79.9 | 11/11 | 0.91 | 0.69 | 0.35 | 5 | 13.9% | 0.38 | 0.57 | 21.4% | 20.5% | 20.9% | 20.9%/15.1% | 10.7 (interpolated) | pass | 0.043 (unverified) | n/a |
| 16 | `cfg_f413` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 14/112/20 | 146 | 23.7% | 4.4% | 1.06 | -3.8% | 181 | 1.66 | 10.9% | 79.8 | 12/12 | 0.92 | 0.70 | 0.37 | 5 | 14.3% | 0.38 | 0.56 | 21.9% | 20.5% | 21.0% | 20.8%/16.7% | 10.8 (interpolated) | pass | 0.048 (unverified) | n/a |
| 17 | `cfg_fa7c` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 157/197/0 | 354 | 21.8% | 4.1% | 0.91 | -4.3% | 351 | 1.36 | 12.6% | 193.4 | 10/10 | 0.70 | 0.53 | 0.39 | 5 | 10.3% | 0.49 | 0.46 | 18.4% | 15.9% | 16.4% | 22.1%/18.2% | 4.7 (interpolated) | pass | 0.029 (unverified) | n/a |
| 18 | `cfg_447b` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 19/65/120 | 204 | 28.0% | 5.1% | 0.89 | -10.9% | 220 | 1.39 | 17.7% | 113.3 | 9/9 | 1.00 | 0.68 | 0.21 | 5 | 8.0% | 0.68 | 0.74 | 24.5% | 22.9% | 11.7% | 24.1%/15.4% | 9.2 (interpolated) | pass | 0.026 (unverified) | n/a |
| 19 | `cfg_5c04` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 26/85/55 | 166 | 27.2% | 5.0% | 0.86 | -9.0% | 350 | 1.38 | 19.3% | 91.6 | 11/11 | 0.91 | 0.69 | 0.17 | 3 | 6.8% | 0.77 | 0.70 | 26.5% | 24.7% | 24.5% | 24.4%/17.3% | 11.2 (interpolated) | pass | 0.023 (unverified) | n/a |
| 20 | `cfg_43ab` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 20/88/49 | 157 | 26.0% | 4.8% | 0.83 | -10.6% | 567 | 1.39 | 18.7% | 87.6 | 11/11 | 0.91 | 0.46 | 0.37 | 4 | 7.5% | 0.75 | 0.74 | 24.6% | 24.1% | 18.7% | 23.3%/18.1% | 11.1 (interpolated) | pass | 0.019 (unverified) | n/a |
| 21 | `cfg_eed6` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 23/62/116 | 201 | 25.8% | 4.8% | 0.85 | -10.5% | 311 | 1.37 | 17.9% | 111.4 | 9/9 | 1.00 | 0.46 | 0.39 | 3 | 6.2% | 0.73 | 0.77 | 22.3% | 21.4% | 10.9% | 21.0%/13.0% | 8.7 (interpolated) | pass | 0.024 (unverified) | n/a |
| 22 | `cfg_9461` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 67/26/76 | 169 | 10.3% | 2.0% | 0.88 | -2.3% | 349 | 1.48 | 3.9% | 93.3 | 10/10 | 0.80 | 0.60 | 0.29 | 4 | 2.6% | 0.74 | 0.58 | 9.0% | 7.4% | 5.8% | 9.4%/7.5% | 5.1 (interpolated) | pass | 0.022 (unverified) | n/a |
| 23 | `cfg_abc6` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 26/67/46 | 139 | 24.6% | 4.6% | 0.92 | -5.3% | 297 | 1.49 | 15.8% | 75.8 | 11/11 | 0.91 | 0.64 | 0.29 | 5 | 9.0% | 0.60 | 0.72 | 23.5% | 21.8% | 19.5% | 22.1%/14.0% | 11.4 (interpolated) | pass | 0.033 (unverified) | n/a |
| 24 | `cfg_0f5d` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 18/91/51 | 160 | 26.2% | 4.9% | 0.89 | -7.4% | 373 | 1.44 | 19.3% | 86.4 | 10/10 | 0.90 | 0.52 | 0.36 | 3 | 11.1% | 0.56 | 0.65 | 25.2% | 23.4% | 20.1% | 23.1%/16.2% | 11.1 (interpolated) | pass | 0.024 (unverified) | n/a |
| 25 | `cfg_fa68` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 21/56/39 | 116 | 27.7% | 5.1% | 0.98 | -4.9% | 147 | 1.60 | 13.1% | 64.2 | 10/10 | 0.90 | 0.60 | 0.39 | 5 | 17.7% | 0.33 | 0.57 | 26.3% | 25.6% | 12.0% | 24.7%/18.9% | 14.7 (interpolated) | pass | 0.035 (unverified) | n/a |
| 26 | `cfg_956f` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 82/36/53 | 171 | 9.2% | 1.8% | 0.96 | -1.4% | 239 | 1.58 | 2.7% | 93.7 | 9/9 | 0.56 | 0.10 | 0.86 | 5 | 3.1% | 0.65 | 0.63 | 7.7% | 6.3% | 5.6% | 8.7%/6.9% | 4.6 (interpolated) | pass | 0.031 (unverified) | n/a |
| 27 | `cfg_762d` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 23/58/39 | 120 | 24.9% | 4.6% | 0.90 | -10.7% | 388 | 1.47 | 14.1% | 66.4 | 11/11 | 1.00 | 0.64 | 0.26 | 3 | 3.7% | 0.90 | 0.81 | 23.9% | 23.0% | 17.6% | 22.6%/16.4% | 13.6 (interpolated) | pass | 0.031 (unverified) | n/a |
| 28 | `cfg_7acc` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=25, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 22/54/37 | 113 | 22.5% | 4.2% | 0.92 | -4.8% | 529 | 1.54 | 13.2% | 61.8 | 11/11 | 0.82 | 0.65 | 0.27 | 4 | 12.2% | 0.44 | 0.78 | 21.7% | 20.4% | 17.2% | 19.2%/14.0% | 12.6 (interpolated) | pass | 0.038 (unverified) | n/a |
| 29 | `cfg_000b` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 82/13/74 | 169 | 10.1% | 2.0% | 0.90 | -2.2% | 349 | 1.49 | 3.5% | 93.4 | 10/10 | 0.80 | 0.65 | 0.25 | 4 | 2.2% | 0.77 | 0.59 | 8.6% | 7.4% | 4.6% | 9.6%/8.0% | 5.0 (interpolated) | pass | 0.024 (unverified) | n/a |
| 30 | `cfg_8104` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 96/143/103 | 342 | 21.7% | 4.1% | 0.94 | -5.6% | 519 | 1.34 | 10.5% | 187.4 | 12/12 | 0.67 | 0.40 | 0.55 | 3 | 5.3% | 0.71 | 0.41 | 18.1% | 14.7% | 25.1% | 20.8%/16.0% | 4.7 (interpolated) | pass | 0.040 (unverified) | n/a |
| 31 | `cfg_bd6c` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 109/244/0 | 353 | 21.6% | 4.1% | 0.89 | -4.5% | 208 | 1.34 | 13.3% | 193.3 | 11/11 | 0.73 | 0.58 | 0.30 | 5 | 13.4% | 0.38 | 0.44 | 18.1% | 16.1% | 16.5% | 21.2%/17.9% | 4.7 (interpolated) | pass | 0.027 (unverified) | n/a |
| 32 | `cfg_e662` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 13/60/33 | 106 | 19.7% | 3.7% | 0.83 | -7.3% | 228 | 1.50 | 12.6% | 57.9 | 10/10 | 1.00 | 0.66 | 0.17 | 3 | 7.0% | 0.63 | 0.82 | 18.8% | 18.2% | 7.7% | 18.3%/12.5% | 12.5 (interpolated) | pass | 0.017 (unverified) | n/a |
| 33 | `cfg_b9f9` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 23/90/54 | 167 | 24.7% | 4.6% | 0.83 | -7.6% | 326 | 1.37 | 19.3% | 91.9 | 11/11 | 0.91 | 0.66 | 0.16 | 4 | 7.3% | 0.70 | 0.77 | 23.9% | 22.5% | 16.6% | 22.6%/17.7% | 10.2 (interpolated) | pass | 0.022 (unverified) | n/a |
| 34 | `cfg_a175` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 84/63/52 | 199 | 13.1% | 2.5% | 0.84 | -3.2% | 463 | 1.43 | 5.8% | 109.6 | 13/13 | 0.77 | 0.60 | 0.25 | 4 | 6.1% | 0.51 | 0.53 | 11.4% | 10.2% | 4.8% | 12.1%/9.8% | 5.3 (interpolated) | pass | 0.020 (unverified) | n/a |
| 35 | `cfg_f32f` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 29/48/39 | 116 | 25.3% | 4.7% | 0.94 | -4.9% | 136 | 1.55 | 12.7% | 64.1 | 11/11 | 0.91 | 0.60 | 0.34 | 4 | 14.8% | 0.40 | 0.59 | 24.3% | 23.0% | 10.0% | 23.6%/16.8% | 13.7 (interpolated) | pass | 0.030 (unverified) | n/a |
| 36 | `cfg_1ca2` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 21/86/0 | 107 | 24.3% | 4.5% | 0.82 | -6.3% | 275 | 1.52 | 14.8% | 58.8 | 10/10 | 0.90 | 0.63 | 0.20 | 4 | 9.6% | 0.62 | 0.81 | 23.8% | 22.2% | 22.3% | 21.7%/15.5% | 14.1 (interpolated) | pass | 0.023 (unverified) | n/a |
| 37 | `cfg_abb5` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 110/42/49 | 201 | 13.9% | 2.7% | 0.90 | -3.1% | 458 | 1.46 | 5.3% | 110.9 | 12/12 | 0.83 | 0.56 | 0.35 | 4 | 6.1% | 0.53 | 0.50 | 12.2% | 10.5% | 6.9% | 13.1%/10.5% | 5.5 (interpolated) | pass | 0.028 (unverified) | n/a |
| 38 | `cfg_bdb0` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 18/55/42 | 115 | 20.9% | 3.9% | 0.79 | -11.2% | 356 | 1.43 | 13.2% | 62.4 | 10/10 | 0.80 | 0.73 | 0.06 | 3 | 5.1% | 0.78 | 0.81 | 20.1% | 19.1% | 18.6% | 19.0%/11.8% | 12.1 (interpolated) | pass | 0.013 (unverified) | n/a |
| 39 | `cfg_769d` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 31/83/56 | 170 | 9.3% | 1.8% | 0.93 | -1.3% | 214 | 1.55 | 3.1% | 93.0 | 9/9 | 0.56 | 0.02 | 0.91 | 5 | 4.0% | 0.55 | 0.63 | 7.7% | 6.7% | 7.3% | 8.7%/6.6% | 4.6 (interpolated) | pass | 0.025 (unverified) | n/a |
| 40 | `cfg_3324` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=40, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 8/81/17 | 106 | 17.4% | 3.3% | 0.88 | -4.0% | 393 | 1.67 | 7.9% | 58.8 | 10/10 | 0.80 | 0.68 | 0.20 | 5 | 10.6% | 0.38 | 0.75 | 16.0% | 14.9% | 6.2% | 15.6%/11.0% | 11.1 (interpolated) | pass | 0.012 (unverified) | n/a |
| 41 | `cfg_c538` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 29/79/51 | 159 | 23.3% | 4.3% | 0.78 | -10.2% | 567 | 1.36 | 18.4% | 86.5 | 12/12 | 0.83 | 0.50 | 0.28 | 4 | 7.5% | 0.71 | 0.75 | 22.6% | 20.9% | 17.4% | 20.6%/14.1% | 9.7 (interpolated) | pass | 0.014 (unverified) | n/a |
| 42 | `cfg_8507` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=40, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 6/83/17 | 106 | 17.2% | 3.3% | 0.87 | -4.0% | 393 | 1.66 | 7.9% | 58.8 | 10/10 | 0.80 | 0.68 | 0.20 | 5 | 10.3% | 0.38 | 0.75 | 15.4% | 14.6% | 6.3% | 15.9%/11.8% | 10.8 (interpolated) | pass | 0.012 (unverified) | n/a |
| 43 | `cfg_ced7` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 29/78/0 | 107 | 23.4% | 4.4% | 0.80 | -7.2% | 275 | 1.50 | 14.3% | 59.2 | 11/11 | 0.91 | 0.60 | 0.20 | 3 | 9.3% | 0.62 | 0.81 | 23.0% | 22.3% | 19.4% | 21.5%/15.0% | 13.7 (interpolated) | pass | 0.020 (unverified) | n/a |
| 44 | `cfg_bda7` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 36/75/55 | 166 | 23.0% | 4.3% | 0.77 | -10.0% | 350 | 1.34 | 18.7% | 90.6 | 12/12 | 0.92 | 0.61 | 0.16 | 3 | 5.5% | 0.79 | 0.77 | 21.8% | 20.9% | 18.9% | 19.3%/13.1% | 9.3 (interpolated) | pass | 0.013 (unverified) | n/a |
| 45 | `cfg_f1e7` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=25, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 31/45/37 | 113 | 19.9% | 3.8% | 0.84 | -5.0% | 529 | 1.49 | 12.6% | 62.0 | 12/12 | 0.83 | 0.63 | 0.21 | 4 | 10.5% | 0.46 | 0.85 | 19.2% | 18.1% | 14.9% | 19.0%/12.3% | 11.8 (interpolated) | pass | 0.028 (unverified) | n/a |
| 46 | `cfg_9934` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 55/96/69 | 220 | 27.4% | 5.0% | 0.80 | -7.4% | 234 | 1.31 | 24.7% | 120.9 | 10/10 | 0.90 | 0.50 | 0.30 | 4 | 7.0% | 0.75 | 0.64 | 24.6% | 23.6% | 24.3% | 23.6%/18.4% | 8.7 (interpolated) | pass | 0.019 (unverified) | n/a |
| 47 | `cfg_9b18` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 24/63/49 | 136 | 24.1% | 4.5% | 0.77 | -6.8% | 566 | 1.38 | 15.2% | 75.3 | 10/10 | 0.90 | 0.45 | 0.32 | 4 | 4.3% | 0.85 | 0.63 | 23.0% | 20.6% | 13.2% | 22.1%/15.9% | 11.9 (interpolated) | pass | 0.012 (unverified) | n/a |
| 48 | `cfg_db0b` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 46/83/64 | 193 | 22.6% | 4.2% | 0.76 | -7.5% | 467 | 1.29 | 21.3% | 104.6 | 10/10 | 0.90 | 0.61 | 0.15 | 3 | 7.4% | 0.69 | 0.77 | 21.4% | 20.1% | 22.4% | 22.2%/16.1% | 8.1 (interpolated) | pass | 0.014 (unverified) | n/a |
| 49 | `cfg_125c` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 15/94/80 | 189 | 20.1% | 3.8% | 0.85 | -5.7% | 308 | 1.42 | 11.5% | 103.1 | 11/11 | 0.91 | 0.62 | 0.24 | 3 | 7.6% | 0.60 | 0.67 | 19.0% | 16.6% | 17.9% | 19.0%/13.0% | 7.5 (interpolated) | pass | 0.019 (unverified) | n/a |
| 50 | `cfg_7c46` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 180/98/0 | 278 | 17.1% | 3.3% | 0.84 | -7.1% | 362 | 1.38 | 9.3% | 152.5 | 10/10 | 0.60 | 0.65 | 0.18 | 5 | 12.0% | 0.29 | 0.40 | 15.2% | 12.6% | 16.2% | 16.9%/13.7% | 4.7 (interpolated) | pass | 0.024 (unverified) | n/a |
| 51 | `cfg_4a3c` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 105/103/76 | 284 | 16.0% | 3.1% | 0.76 | -5.2% | 456 | 1.30 | 8.5% | 155.5 | 11/11 | 0.73 | 0.38 | 0.38 | 4 | 5.1% | 0.64 | 0.54 | 14.0% | 11.7% | 23.2% | 15.7%/13.4% | 4.4 (interpolated) | pass | 0.012 (unverified) | n/a |
| 52 | `cfg_21bb` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 26/47/42 | 115 | 19.9% | 3.8% | 0.77 | -11.2% | 367 | 1.41 | 12.9% | 62.3 | 11/11 | 0.82 | 0.76 | 0.01 | 3 | 4.4% | 0.80 | 0.84 | 19.2% | 18.4% | 19.0% | 17.8%/12.3% | 11.7 (interpolated) | pass | 0.012 (unverified) | n/a |
| 53 | `cfg_3a70` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 59/23/37 | 119 | 18.1% | 3.4% | 0.75 | -5.7% | 566 | 1.43 | 11.2% | 65.7 | 10/10 | 0.90 | 0.59 | 0.16 | 4 | 8.7% | 0.51 | 0.77 | 17.2% | 16.3% | 9.4% | 16.7%/12.2% | 10.9 (interpolated) | pass | 0.009 (unverified) | n/a |
| 54 | `cfg_3f8b` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 18/79/51 | 148 | 22.4% | 4.2% | 0.80 | -6.3% | 327 | 1.39 | 17.0% | 80.4 | 11/11 | 0.91 | 0.61 | 0.18 | 3 | 10.5% | 0.52 | 0.75 | 21.0% | 18.4% | 13.8% | 21.3%/13.4% | 9.6 (interpolated) | pass | 0.015 (unverified) | n/a |
| 55 | `cfg_7726` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 42/105/0 | 147 | 24.0% | 4.5% | 0.78 | -10.9% | 467 | 1.39 | 19.7% | 81.8 | 9/9 | 0.89 | 0.63 | 0.16 | 3 | 5.9% | 0.81 | 0.74 | 23.4% | 21.7% | 18.0% | 22.8%/18.0% | 11.1 (interpolated) | pass | 0.019 (unverified) | n/a |
| 56 | `cfg_40b3` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 11/98/80 | 189 | 20.1% | 3.8% | 0.85 | -5.7% | 308 | 1.42 | 11.6% | 103.0 | 10/10 | 0.90 | 0.56 | 0.29 | 3 | 7.7% | 0.60 | 0.67 | 18.4% | 16.0% | 17.9% | 18.6%/14.2% | 7.3 (interpolated) | pass | 0.019 (unverified) | n/a |
| 57 | `cfg_5c0f` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 30/99/66 | 195 | 25.6% | 4.7% | 0.78 | -6.6% | 567 | 1.33 | 22.4% | 106.6 | 10/10 | 0.90 | 0.59 | 0.19 | 4 | 5.6% | 0.80 | 0.73 | 24.2% | 21.6% | 15.0% | 23.3%/14.7% | 8.8 (interpolated) | pass | 0.014 (unverified) | n/a |
| 58 | `cfg_5eec` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 27/82/54 | 163 | 23.5% | 4.4% | 0.80 | -7.4% | 373 | 1.38 | 19.1% | 88.0 | 11/11 | 0.91 | 0.50 | 0.29 | 3 | 9.8% | 0.57 | 0.72 | 22.2% | 20.3% | 19.6% | 21.5%/15.0% | 9.8 (interpolated) | pass | 0.016 (unverified) | n/a |
| 59 | `cfg_d861` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 32/75/153 | 260 | 26.2% | 4.8% | 0.78 | -8.1% | 212 | 1.29 | 21.8% | 142.2 | 10/10 | 0.90 | 0.51 | 0.27 | 4 | 7.6% | 0.70 | 0.73 | 23.5% | 20.5% | 11.2% | 22.2%/13.3% | 6.7 (interpolated) | pass | 0.012 (unverified) | n/a |
| 60 | `cfg_986c` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 82/124/78 | 284 | 16.1% | 3.1% | 0.75 | -5.6% | 465 | 1.30 | 8.8% | 155.5 | 11/11 | 0.73 | 0.35 | 0.40 | 3 | 5.4% | 0.61 | 0.51 | 13.9% | 11.5% | 20.1% | 15.7%/12.4% | 4.4 (interpolated) | pass | 0.012 (unverified) | n/a |
| 61 | `cfg_384f` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=15, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 87/76/61 | 224 | 14.2% | 2.7% | 0.83 | -3.4% | 173 | 1.38 | 6.5% | 122.6 | 11/11 | 0.82 | 0.36 | 0.48 | 5 | 6.2% | 0.55 | 0.49 | 12.2% | 10.3% | 9.6% | 13.0%/10.6% | 5.0 (interpolated) | pass | 0.019 (unverified) | n/a |
| 62 | `cfg_6676` | timeframe=5min, mean_type=ema, mean_lookback=20, std_lookback=30, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 10/101/0 | 111 | 5.3% | 1.1% | 0.87 | -1.2% | 131 | 1.64 | 0.9% | 59.6 | 9/9 | 0.78 | 0.45 | 0.41 | 5 | 3.5% | 0.33 | 0.56 | 4.5% | 3.7% | 1.8% | 4.9%/3.9% | 4.3 (interpolated) | pass | 0.030 (unverified) | n/a |
| 63 | `cfg_1ce5` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=30, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 45/8/53 | 106 | 16.0% | 3.1% | 0.78 | -5.3% | 557 | 1.50 | 7.6% | 58.3 | 9/9 | 0.78 | 0.60 | 0.18 | 5 | 8.6% | 0.44 | 0.84 | 15.3% | 14.5% | 6.3% | 14.4%/10.9% | 11.1 (interpolated) | pass | 0.008 (unverified) | n/a |
| 64 | `cfg_2731` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 20/89/0 | 109 | 22.1% | 4.1% | 0.77 | -8.9% | 505 | 1.50 | 15.4% | 60.1 | 9/9 | 0.67 | 0.43 | 0.34 | 5 | 10.4% | 0.50 | 0.81 | 20.9% | 19.6% | 19.5% | 19.1%/14.7% | 13.7 (interpolated) | pass | 0.021 (unverified) | n/a |
| 65 | `cfg_6a19` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 72/82/45 | 199 | 13.4% | 2.6% | 0.78 | -5.9% | 350 | 1.39 | 6.3% | 109.6 | 10/10 | 0.80 | 0.26 | 0.52 | 3 | 6.0% | 0.54 | 0.57 | 11.6% | 10.4% | 15.3% | 12.9%/10.2% | 5.2 (interpolated) | pass | 0.015 (unverified) | n/a |
| 66 | `cfg_6e8a` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 110/73/0 | 183 | 13.4% | 2.6% | 0.83 | -6.1% | 350 | 1.51 | 6.0% | 100.4 | 10/10 | 0.90 | 0.46 | 0.37 | 5 | 6.9% | 0.47 | 0.56 | 11.7% | 10.0% | 15.0% | 13.2%/11.0% | 5.7 (interpolated) | pass | 0.023 (unverified) | n/a |
| 67 | `cfg_282e` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=20, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 29/47/34 | 110 | 17.2% | 3.3% | 0.76 | -6.7% | 303 | 1.45 | 11.9% | 59.7 | 11/11 | 1.00 | 0.65 | 0.11 | 3 | 6.6% | 0.60 | 0.78 | 15.1% | 14.3% | 6.2% | 14.9%/10.9% | 10.3 (interpolated) | pass | 0.012 (unverified) | n/a |
| 68 | `cfg_09c8` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=10, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 43/320/0 | 363 | 22.1% | 4.1% | 1.16 | -2.9% | 131 | 1.49 | 8.2% | 198.9 | 9/9 | 0.44 | -0.02 | 1.17 | 5 | 9.9% | 0.53 | 0.41 | 19.0% | 15.3% | 14.5% | 19.3%/15.1% | 4.6 (interpolated) | pass | 0.083 (unverified) | n/a |
| 69 | `cfg_c087` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 32/51/38 | 121 | 19.8% | 3.7% | 0.81 | -9.5% | 388 | 1.42 | 13.3% | 66.4 | 11/11 | 0.91 | 0.52 | 0.29 | 4 | 4.6% | 0.80 | 0.71 | 18.8% | 17.4% | 6.8% | 18.3%/12.0% | 10.6 (interpolated) | pass | 0.014 (unverified) | n/a |
| 70 | `cfg_80c5` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 48/39/36 | 123 | 18.3% | 3.5% | 0.78 | -7.8% | 388 | 1.41 | 12.3% | 67.4 | 10/10 | 0.90 | 0.41 | 0.37 | 4 | 4.0% | 0.80 | 0.71 | 17.1% | 15.6% | 9.6% | 17.0%/12.1% | 10.6 (interpolated) | pass | 0.012 (unverified) | n/a |
| 71 | `cfg_7776` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 36/50/51 | 137 | 8.1% | 1.6% | 0.81 | -1.6% | 166 | 1.52 | 2.4% | 74.6 | 10/10 | 0.60 | 0.16 | 0.65 | 5 | 3.1% | 0.60 | 0.72 | 6.8% | 5.8% | 8.1% | 7.6%/5.6% | 5.0 (interpolated) | pass | 0.015 (unverified) | n/a |
| 72 | `cfg_ab2a` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 28/69/51 | 148 | 20.8% | 3.9% | 0.76 | -6.3% | 327 | 1.36 | 16.4% | 80.5 | 12/12 | 0.92 | 0.59 | 0.18 | 3 | 8.8% | 0.57 | 0.77 | 19.8% | 18.3% | 12.4% | 18.9%/11.8% | 9.3 (interpolated) | pass | 0.013 (unverified) | n/a |
| 73 | `cfg_b1a8` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 40/89/66 | 195 | 24.5% | 4.6% | 0.76 | -7.0% | 567 | 1.32 | 21.7% | 106.0 | 11/11 | 0.91 | 0.49 | 0.27 | 3 | 5.3% | 0.81 | 0.72 | 21.5% | 20.5% | 9.4% | 22.2%/15.0% | 8.3 (interpolated) | pass | 0.013 (unverified) | n/a |
| 74 | `cfg_e32e` | timeframe=5min, mean_type=ema, mean_lookback=20, std_lookback=30, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 14/97/0 | 111 | 4.8% | 1.0% | 0.80 | -1.2% | 204 | 1.57 | 0.8% | 59.8 | 10/10 | 0.80 | 0.45 | 0.35 | 5 | 3.2% | 0.33 | 0.58 | 4.0% | 3.2% | 1.5% | 4.3%/3.0% | 3.9 (interpolated) | pass | 0.023 (unverified) | n/a |
| 75 | `cfg_9d4a` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 53/310/0 | 363 | 21.1% | 4.0% | 1.11 | -2.8% | 158 | 1.47 | 8.1% | 198.7 | 10/10 | 0.50 | 0.24 | 0.87 | 5 | 9.0% | 0.55 | 0.43 | 17.9% | 14.4% | 14.6% | 18.2%/13.5% | 4.5 (interpolated) | pass | 0.069 (unverified) | n/a |
| 76 | `cfg_a69f` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 110/72/0 | 182 | 14.8% | 2.8% | 0.88 | -3.8% | 359 | 1.49 | 5.6% | 100.8 | 11/11 | 0.82 | 0.51 | 0.37 | 4 | 7.7% | 0.46 | 0.47 | 13.2% | 12.0% | 10.9% | 13.9%/11.4% | 6.2 (interpolated) | pass | 0.031 (unverified) | n/a |
| 77 | `cfg_6ac2` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 17/88/0 | 105 | 14.9% | 2.9% | 0.84 | -7.3% | 381 | 1.60 | 8.1% | 58.3 | 8/8 | 0.62 | 0.38 | 0.46 | 5 | 7.8% | 0.44 | 0.67 | 13.7% | 12.8% | 9.5% | 12.8%/9.6% | 10.4 (interpolated) | pass | 0.027 (unverified) | n/a |
| 78 | `cfg_ef68` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 86/92/0 | 178 | 13.7% | 2.6% | 0.80 | -3.8% | 307 | 1.44 | 6.0% | 98.4 | 12/12 | 0.83 | 0.47 | 0.33 | 5 | 8.1% | 0.39 | 0.51 | 12.3% | 10.7% | 7.6% | 13.0%/10.4% | 5.9 (interpolated) | pass | 0.020 (unverified) | n/a |
| 79 | `cfg_0cf0` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=25, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 112/7/36 | 155 | 17.8% | 3.4% | 0.81 | -5.9% | 439 | 1.41 | 12.8% | 85.9 | 9/9 | 0.89 | 0.50 | 0.30 | 4 | 9.4% | 0.47 | 0.61 | 16.0% | 14.8% | 11.9% | 14.7%/10.8% | 7.7 (interpolated) | pass | 0.017 (unverified) | n/a |
| 80 | `cfg_e938` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=25, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 15/68/42 | 125 | 18.3% | 3.5% | 0.75 | -7.5% | 399 | 1.40 | 14.6% | 69.0 | 10/10 | 0.90 | 0.37 | 0.38 | 3 | 8.0% | 0.54 | 0.84 | 16.1% | 14.5% | 5.7% | 16.6%/11.5% | 9.9 (interpolated) | pass | 0.012 (unverified) | n/a |
| 81 | `cfg_1fd1` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=25, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 8/75/42 | 125 | 18.2% | 3.5% | 0.75 | -7.5% | 399 | 1.40 | 14.9% | 68.9 | 9/9 | 0.89 | 0.39 | 0.36 | 3 | 7.4% | 0.57 | 0.83 | 17.1% | 15.5% | 5.9% | 15.6%/9.6% | 10.2 (interpolated) | pass | 0.013 (unverified) | n/a |
| 82 | `cfg_6dd7` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 22/83/0 | 105 | 14.6% | 2.8% | 0.83 | -7.2% | 394 | 1.60 | 8.0% | 58.1 | 9/9 | 0.67 | 0.47 | 0.36 | 5 | 7.5% | 0.45 | 0.63 | 13.6% | 12.8% | 9.9% | 12.9%/9.0% | 10.4 (interpolated) | pass | 0.026 (unverified) | n/a |
| 83 | `cfg_30e4` | timeframe=5min, mean_type=ema, mean_lookback=20, std_lookback=30, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 9/55/47 | 111 | 4.0% | 0.8% | 0.82 | -1.5% | 139 | 1.55 | 0.6% | 59.7 | 9/9 | 0.67 | 0.36 | 0.46 | 4 | 2.7% | 0.32 | 0.73 | 3.2% | 2.5% | 1.2% | 3.8%/2.9% | 3.6 (interpolated) | pass | 0.010 (unverified) | n/a |
| 84 | `cfg_d144` | timeframe=5min, mean_type=ema, mean_lookback=50, std_lookback=40, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 7/169/0 | 176 | 6.2% | 1.2% | 0.83 | -1.8% | 144 | 1.52 | 1.4% | 95.0 | 9/9 | 0.89 | 0.32 | 0.52 | 5 | 4.1% | 0.34 | 0.62 | 4.9% | 3.6% | 3.0% | 5.6%/4.3% | 3.4 (interpolated) | pass | 0.024 (unverified) | n/a |
| 85 | `cfg_44d3` | timeframe=5min, mean_type=ema, mean_lookback=50, std_lookback=40, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 14/162/0 | 176 | 6.2% | 1.2% | 0.83 | -1.8% | 144 | 1.52 | 1.4% | 95.0 | 10/10 | 0.90 | 0.46 | 0.37 | 5 | 3.9% | 0.36 | 0.62 | 4.8% | 3.5% | 3.1% | 5.6%/4.2% | 3.4 (interpolated) | pass | 0.025 (unverified) | n/a |
| 86 | `cfg_cc6b` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 9/86/22 | 117 | 13.8% | 2.7% | 0.78 | -4.7% | 380 | 1.45 | 8.7% | 63.7 | 11/11 | 0.73 | 0.55 | 0.23 | 4 | 5.8% | 0.56 | 0.74 | 12.9% | 11.8% | 11.4% | 12.9%/8.0% | 8.7 (interpolated) | pass | 0.013 (unverified) | n/a |
| 87 | `cfg_9330` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=25, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 53/55/45 | 153 | 22.7% | 4.2% | 0.82 | -4.5% | 421 | 1.42 | 16.4% | 84.4 | 10/10 | 0.90 | 0.54 | 0.28 | 4 | 7.9% | 0.62 | 0.76 | 21.2% | 19.4% | 12.3% | 20.1%/14.0% | 9.7 (interpolated) | pass | 0.019 (unverified) | n/a |
| 88 | `cfg_a21c` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 15/89/0 | 104 | 18.5% | 3.5% | 0.99 | -3.4% | 308 | 1.77 | 8.3% | 56.8 | 10/10 | 0.80 | 0.63 | 0.36 | 4 | 10.7% | 0.39 | 0.59 | 17.1% | 16.2% | 13.7% | 17.1%/12.4% | 11.8 (interpolated) | pass | 0.036 (unverified) | n/a |
| 89 | `cfg_ba17` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=25, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 53/76/20 | 149 | 14.0% | 2.7% | 0.77 | -5.0% | 439 | 1.39 | 10.0% | 82.1 | 9/9 | 0.89 | 0.34 | 0.43 | 4 | 8.4% | 0.40 | 0.68 | 12.6% | 11.3% | 11.3% | 12.3%/8.4% | 6.8 (interpolated) | pass | 0.012 (unverified) | n/a |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 2.6% / 0.72 / 25 | 5.7% / 2.21 / 12 | 18.8% / 1.80 / 12 | 8.6% / 1.51 / 28 | -0.7% / -0.10 / 30 |
| 2 | 2.4% / 0.70 / 25 | 5.6% / 2.20 / 12 | 18.3% / 1.76 / 12 | 7.3% / 1.33 / 28 | -0.6% / -0.07 / 30 |
| 3 | -0.6% / -0.15 / 37 | 12.2% / 3.50 / 21 | 18.6% / 2.16 / 22 | 1.2% / 0.27 / 30 | 1.7% / 0.30 / 34 |
| 4 | 1.2% / 0.79 / 42 | 0.3% / 0.29 / 29 | 6.9% / 2.98 / 31 | -0.6% / -0.23 / 35 | 2.7% / 1.26 / 34 |
| 5 | 5.2% / 1.45 / 26 | -0.7% / -0.26 / 16 | 20.5% / 2.59 / 18 | 0.9% / 0.18 / 20 | 5.5% / 1.05 / 25 |
| 6 | 5.1% / 1.43 / 26 | -0.1% / -0.03 / 16 | 20.1% / 2.58 / 18 | 1.5% / 0.28 / 20 | 5.4% / 1.07 / 25 |
| 7 | 1.0% / 0.34 / 28 | 2.5% / 0.76 / 22 | 15.8% / 2.38 / 19 | 3.1% / 0.60 / 29 | 4.6% / 0.75 / 39 |
| 8 | -0.2% / -0.04 / 78 | 2.6% / 0.90 / 56 | 8.2% / 1.49 / 57 | 8.5% / 1.85 / 54 | 1.9% / 0.38 / 71 |
| 9 | 1.6% / 1.09 / 39 | 1.3% / 1.00 / 28 | 5.7% / 2.35 / 28 | 0.2% / 0.10 / 33 | 1.6% / 0.67 / 34 |
| 10 | 2.0% / 0.66 / 28 | 7.1% / 2.02 / 18 | 20.6% / 2.57 / 15 | -2.0% / -0.42 / 27 | -0.2% / 0.01 / 32 |
| 11 | 0.4% / 0.14 / 78 | 1.9% / 0.67 / 56 | 9.3% / 1.71 / 57 | 6.8% / 1.53 / 54 | 1.4% / 0.29 / 71 |
| 12 | -1.0% / -0.25 / 39 | 11.3% / 3.33 / 21 | 16.2% / 2.04 / 22 | 0.8% / 0.20 / 30 | 1.3% / 0.24 / 34 |
| 13 | -0.9% / -0.22 / 84 | -0.6% / -0.20 / 54 | 17.5% / 2.97 / 65 | 1.9% / 0.47 / 57 | 4.5% / 0.80 / 81 |
| 14 | 2.1% / 0.95 / 62 | 2.4% / 0.96 / 51 | 4.5% / 0.88 / 51 | 5.3% / 1.23 / 52 | 4.1% / 0.91 / 62 |
| 15 | 2.2% / 0.72 / 37 | 5.6% / 2.20 / 22 | 8.3% / 1.45 / 21 | 3.6% / 1.03 / 28 | 1.9% / 0.41 / 38 |
| 16 | 2.6% / 0.82 / 37 | 5.6% / 2.21 / 22 | 8.2% / 1.45 / 21 | 3.5% / 1.03 / 28 | 1.9% / 0.41 / 38 |
| 17 | 2.3% / 0.73 / 85 | 1.0% / 0.36 / 64 | 10.4% / 1.65 / 64 | 5.5% / 1.28 / 63 | 1.2% / 0.27 / 78 |
| 18 | 0.6% / 0.17 / 51 | 1.8% / 0.53 / 27 | 18.5% / 2.47 / 27 | 5.4% / 0.96 / 40 | 0.1% / 0.05 / 59 |
| 19 | 1.7% / 0.48 / 37 | 7.9% / 1.83 / 30 | 19.1% / 2.15 / 30 | -0.1% / 0.01 / 34 | -2.6% / -0.41 / 35 |
| 20 | 2.1% / 0.62 / 37 | 10.5% / 2.78 / 24 | 17.2% / 2.05 / 21 | -5.4% / -0.96 / 33 | 0.8% / 0.14 / 42 |
| 21 | -0.6% / -0.14 / 46 | 3.1% / 0.95 / 27 | 18.4% / 2.54 / 24 | 4.6% / 0.79 / 43 | -0.9% / -0.09 / 61 |
| 22 | 0.6% / 0.44 / 40 | 0.2% / 0.19 / 29 | 7.5% / 2.67 / 31 | -0.1% / -0.02 / 35 | 1.8% / 0.78 / 34 |
| 23 | 0.3% / 0.12 / 30 | 2.7% / 0.81 / 22 | 14.3% / 2.33 / 19 | 2.6% / 0.55 / 29 | 3.0% / 0.51 / 39 |
| 24 | -3.4% / -0.89 / 38 | 11.6% / 3.08 / 25 | 13.6% / 2.00 / 22 | -0.6% / -0.08 / 38 | 3.8% / 0.60 / 37 |
| 25 | 2.9% / 0.91 / 23 | 6.7% / 2.20 / 17 | 8.4% / 1.34 / 17 | 5.3% / 0.88 / 29 | 1.8% / 0.33 / 30 |
| 26 | 0.5% / 0.45 / 41 | 0.1% / 0.05 / 30 | 5.9% / 2.52 / 31 | 0.9% / 0.36 / 34 | 1.6% / 0.97 / 35 |
| 27 | 1.8% / 0.60 / 28 | 7.3% / 2.07 / 18 | 20.4% / 2.57 / 15 | -1.7% / -0.36 / 27 | -3.5% / -0.58 / 32 |
| 28 | 1.9% / 0.52 / 32 | 5.8% / 2.10 / 16 | 9.2% / 1.44 / 17 | -0.0% / 0.02 / 25 | 4.1% / 0.95 / 23 |
| 29 | 0.7% / 0.47 / 40 | 0.7% / 0.61 / 29 | 7.7% / 2.94 / 31 | -0.5% / -0.17 / 35 | 1.3% / 0.59 / 34 |
| 30 | -1.0% / -0.25 / 85 | -0.1% / -0.04 / 54 | 15.6% / 3.03 / 65 | 2.0% / 0.49 / 57 | 4.4% / 0.83 / 81 |
| 31 | 2.5% / 0.69 / 85 | 2.0% / 0.66 / 64 | 7.6% / 1.24 / 64 | 7.3% / 1.60 / 63 | 0.8% / 0.19 / 77 |
| 32 | -1.4% / -0.47 / 26 | 6.3% / 3.05 / 12 | 11.9% / 1.89 / 12 | 4.4% / 0.99 / 27 | -2.2% / -0.37 / 29 |
| 33 | 4.0% / 1.04 / 38 | 2.6% / 0.69 / 26 | 16.2% / 1.99 / 27 | -0.3% / -0.05 / 31 | 0.8% / 0.15 / 45 |
| 34 | -1.0% / -0.41 / 51 | 1.3% / 0.78 / 33 | 6.6% / 2.36 / 30 | 1.6% / 0.51 / 33 | 4.1% / 0.97 / 52 |
| 35 | 3.0% / 0.94 / 23 | 6.7% / 2.22 / 17 | 9.2% / 1.47 / 17 | 4.8% / 0.83 / 29 | -0.3% / -0.03 / 30 |
| 36 | 3.4% / 0.89 / 28 | 8.1% / 2.65 / 17 | 13.4% / 1.61 / 18 | -2.5% / -0.38 / 23 | 0.5% / 0.13 / 21 |
| 37 | -1.4% / -0.57 / 51 | 1.8% / 1.10 / 33 | 7.4% / 2.70 / 30 | 1.8% / 0.59 / 33 | 3.8% / 0.90 / 54 |
| 38 | -2.1% / -0.77 / 25 | 10.6% / 2.70 / 22 | 15.0% / 2.07 / 17 | 1.6% / 0.35 / 26 | -4.5% / -0.82 / 25 |
| 39 | 0.6% / 0.58 / 41 | 0.2% / 0.13 / 30 | 5.1% / 2.08 / 30 | 1.1% / 0.43 / 34 | 2.1% / 1.10 / 35 |
| 40 | 2.0% / 0.72 / 28 | 4.6% / 2.28 / 12 | 6.2% / 1.13 / 16 | 1.0% / 0.29 / 25 | 2.6% / 0.68 / 25 |
| 41 | 2.0% / 0.57 / 39 | 10.3% / 2.75 / 24 | 14.7% / 1.89 / 21 | -5.3% / -0.96 / 33 | 0.9% / 0.17 / 42 |
| 42 | 2.0% / 0.72 / 28 | 4.4% / 2.30 / 12 | 6.2% / 1.13 / 16 | 1.0% / 0.29 / 25 | 2.6% / 0.68 / 25 |
| 43 | 2.7% / 0.69 / 28 | 9.5% / 2.78 / 17 | 13.0% / 1.58 / 18 | -2.5% / -0.39 / 23 | -0.3% / -0.04 / 21 |
| 44 | 1.1% / 0.31 / 37 | 7.9% / 1.83 / 30 | 16.6% / 1.98 / 30 | -0.1% / -0.00 / 34 | -3.1% / -0.51 / 35 |
| 45 | 1.2% / 0.35 / 32 | 5.3% / 1.91 / 16 | 8.5% / 1.35 / 17 | -0.7% / -0.12 / 25 | 4.4% / 1.02 / 23 |
| 46 | 6.0% / 1.24 / 53 | 2.0% / 0.51 / 37 | 19.0% / 2.16 / 35 | -3.3% / -0.44 / 47 | 2.3% / 0.38 / 48 |
| 47 | 6.9% / 1.83 / 26 | 1.3% / 0.38 / 24 | 19.0% / 2.28 / 23 | -3.7% / -0.52 / 30 | 0.0% / 0.03 / 33 |
| 48 | 1.4% / 0.34 / 49 | 8.6% / 2.04 / 32 | 14.2% / 1.82 / 30 | -1.8% / -0.31 / 40 | -0.7% / -0.08 / 42 |
| 49 | -0.9% / -0.25 / 53 | 5.2% / 1.71 / 26 | 11.6% / 1.77 / 27 | 3.4% / 0.97 / 34 | -0.2% / -0.01 / 49 |
| 50 | 2.0% / 0.95 / 62 | 2.4% / 0.92 / 51 | 4.0% / 0.79 / 51 | 4.5% / 1.07 / 52 | 3.2% / 0.72 / 62 |
| 51 | 0.8% / 0.30 / 67 | -2.2% / -0.84 / 57 | 10.4% / 1.97 / 53 | 3.3% / 0.77 / 45 | 3.2% / 0.71 / 62 |
| 52 | -2.5% / -0.92 / 25 | 10.6% / 2.70 / 22 | 14.8% / 2.10 / 17 | 1.1% / 0.26 / 26 | -4.3% / -0.77 / 25 |
| 53 | 4.6% / 1.45 / 26 | 3.0% / 1.15 / 20 | 8.6% / 1.41 / 19 | -1.7% / -0.30 / 30 | 2.7% / 0.54 / 24 |
| 54 | -0.4% / -0.09 / 37 | 8.2% / 2.29 / 26 | 10.8% / 1.60 / 20 | -2.0% / -0.37 / 31 | 4.7% / 0.76 / 34 |
| 55 | 4.0% / 0.96 / 38 | 9.5% / 2.27 / 25 | 17.1% / 1.99 / 23 | -3.9% / -0.71 / 32 | -3.3% / -0.54 / 29 |
| 56 | -1.0% / -0.31 / 53 | 5.2% / 1.71 / 26 | 11.5% / 1.76 / 27 | 3.6% / 1.02 / 34 | -0.2% / -0.01 / 49 |
| 57 | 0.2% / 0.08 / 50 | 8.5% / 1.76 / 35 | 18.9% / 2.11 / 30 | -3.9% / -0.66 / 38 | 1.1% / 0.21 / 42 |
| 58 | -4.1% / -1.03 / 40 | 11.7% / 3.10 / 25 | 12.5% / 1.88 / 22 | -0.9% / -0.11 / 39 | 3.4% / 0.55 / 37 |
| 59 | 2.8% / 0.66 / 67 | 2.7% / 0.68 / 41 | 17.3% / 1.90 / 44 | 2.8% / 0.46 / 52 | -0.9% / -0.10 / 56 |
| 60 | -0.1% / -0.00 / 67 | -2.1% / -0.78 / 57 | 10.1% / 1.92 / 53 | 3.9% / 0.90 / 45 | 3.7% / 0.81 / 62 |
| 61 | 3.2% / 1.06 / 54 | 0.5% / 0.26 / 40 | 7.6% / 2.49 / 36 | 0.9% / 0.24 / 38 | 1.5% / 0.38 / 56 |
| 62 | 0.5% / 0.47 / 23 | 1.0% / 0.88 / 22 | 0.9% / 0.78 / 22 | 1.7% / 1.16 / 21 | 1.1% / 0.94 / 23 |
| 63 | 3.3% / 1.20 / 25 | 0.4% / 0.29 / 13 | 6.8% / 1.22 / 16 | 3.0% / 0.71 / 26 | 1.6% / 0.41 / 26 |
| 64 | 0.4% / 0.15 / 21 | 3.7% / 1.10 / 16 | 10.6% / 1.67 / 16 | 1.7% / 0.29 / 25 | 4.2% / 0.68 / 31 |
| 65 | 4.3% / 1.83 / 50 | -1.1% / -0.51 / 39 | 7.0% / 1.55 / 34 | 3.9% / 1.15 / 28 | -1.1% / -0.29 / 48 |
| 66 | 2.1% / 1.19 / 44 | 2.0% / 1.17 / 31 | 6.1% / 1.41 / 34 | 1.2% / 0.33 / 28 | 1.4% / 0.48 / 46 |
| 67 | -2.0% / -0.74 / 28 | 5.5% / 2.94 / 12 | 9.9% / 1.72 / 12 | 5.9% / 1.30 / 28 | -2.6% / -0.45 / 30 |
| 68 | 3.6% / 1.76 / 78 | 1.9% / 0.69 / 62 | 11.1% / 2.28 / 69 | 0.2% / 0.09 / 69 | 3.8% / 0.90 / 85 |
| 69 | 4.0% / 1.32 / 26 | 4.9% / 1.38 / 20 | 14.5% / 2.25 / 22 | 1.9% / 0.48 / 21 | -5.9% / -1.05 / 32 |
| 70 | 4.2% / 1.41 / 27 | 2.3% / 0.82 / 20 | 13.8% / 2.18 / 22 | 1.6% / 0.43 / 21 | -4.0% / -0.70 / 33 |
| 71 | 0.8% / 0.59 / 32 | 0.8% / 0.81 / 22 | 4.8% / 2.19 / 24 | 0.6% / 0.24 / 30 | 0.9% / 0.43 / 29 |
| 72 | -0.5% / -0.10 / 37 | 8.7% / 2.49 / 26 | 11.0% / 1.63 / 20 | -2.2% / -0.41 / 31 | 2.8% / 0.49 / 34 |
| 73 | -0.5% / -0.08 / 50 | 9.5% / 1.88 / 35 | 18.2% / 2.11 / 30 | -4.0% / -0.70 / 38 | 0.6% / 0.13 / 42 |
| 74 | 0.2% / 0.26 / 23 | 0.9% / 0.82 / 22 | 0.9% / 0.78 / 22 | 1.5% / 1.06 / 21 | 1.1% / 0.94 / 23 |
| 75 | 3.3% / 1.65 / 78 | 1.6% / 0.58 / 62 | 11.1% / 2.27 / 69 | 0.0% / 0.02 / 69 | 3.9% / 0.91 / 85 |
| 76 | 1.9% / 0.75 / 46 | 2.3% / 1.36 / 30 | 6.6% / 2.11 / 29 | -0.2% / -0.03 / 29 | 3.6% / 0.81 / 48 |
| 77 | 6.6% / 2.46 / 26 | 0.7% / 0.30 / 17 | 5.5% / 1.31 / 16 | 1.2% / 0.34 / 21 | 0.3% / 0.09 / 25 |
| 78 | 2.3% / 0.90 / 46 | 1.9% / 1.11 / 30 | 5.2% / 1.63 / 28 | 0.4% / 0.13 / 28 | 3.3% / 0.73 / 46 |
| 79 | 3.4% / 0.96 / 36 | 3.1% / 1.28 / 24 | 5.8% / 1.10 / 26 | -3.0% / -0.63 / 36 | 7.7% / 1.71 / 33 |
| 80 | -5.1% / -1.59 / 31 | 9.6% / 3.25 / 16 | 9.6% / 1.58 / 15 | -2.6% / -0.58 / 26 | 6.6% / 1.13 / 37 |
| 81 | -5.1% / -1.59 / 31 | 9.3% / 3.18 / 16 | 10.0% / 1.69 / 15 | -2.7% / -0.61 / 26 | 6.4% / 1.09 / 37 |
| 82 | 6.6% / 2.47 / 26 | 0.7% / 0.30 / 17 | 4.8% / 1.21 / 16 | 1.2% / 0.34 / 21 | 0.7% / 0.19 / 25 |
| 83 | 0.6% / 0.78 / 23 | 1.3% / 1.24 / 22 | 1.2% / 1.21 / 22 | 1.1% / 1.11 / 21 | -0.3% / -0.25 / 23 |
| 84 | 0.9% / 1.30 / 40 | 0.1% / 0.10 / 31 | 1.5% / 0.90 / 31 | 1.5% / 0.71 / 36 | 2.0% / 1.55 / 38 |
| 85 | 0.9% / 1.38 / 40 | 0.1% / 0.10 / 31 | 1.5% / 0.90 / 31 | 1.3% / 0.63 / 36 | 2.1% / 1.63 / 38 |
| 86 | -2.1% / -0.80 / 26 | 3.5% / 1.39 / 22 | 7.6% / 1.91 / 18 | 4.0% / 1.04 / 27 | 0.3% / 0.11 / 24 |
| 87 | 1.2% / 0.32 / 35 | 2.0% / 0.60 / 24 | 13.7% / 1.84 / 26 | -0.6% / -0.09 / 35 | 5.1% / 1.00 / 33 |
| 88 | -1.2% / -0.49 / 21 | 4.4% / 1.78 / 19 | 7.1% / 1.63 / 16 | 4.0% / 0.97 / 25 | 3.2% / 0.84 / 23 |
| 89 | 3.2% / 0.98 / 35 | 2.0% / 0.88 / 23 | 4.5% / 1.06 / 25 | -1.5% / -0.34 / 33 | 5.2% / 1.55 / 33 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_9461` | 6 | 0.85 | 0.86/0.89 | 0.85/0.88 |
| 1 | `cfg_09c8` | 4 | 0.98 | 0.99/0.99 | 0.97/0.99 |
| 2 | `cfg_0cf0` | 4 | 0.82 | 0.80/0.81 | 0.75/0.76 |
| 3 | `cfg_0f5d` | 2 | 0.99 | 0.98/0.98 | 0.95/0.95 |
| 4 | `cfg_cc6b` | 5 | 0.87 | 0.88/0.92 | 0.85/0.86 |
| 5 | `cfg_5c04` | 6 | 0.86 | 0.90/0.91 | 0.76/0.79 |
| 6 | `cfg_125c` | 4 | 0.96 | 0.97/0.98 | 0.95/0.98 |
| 7 | `cfg_9d13` | 8 | 0.88 | 0.87/0.90 | 0.88/0.88 |
| 8 | `cfg_f7d6` | 6 | 0.87 | 0.83/0.89 | 0.79/0.83 |
| 9 | `cfg_15b7` | 2 | 0.93 | 0.92/0.92 | 0.91/0.91 |
| 10 | `cfg_447b` | 4 | 0.87 | 0.89/0.90 | 0.70/0.70 |
| 11 | `cfg_1ca2` | 3 | 0.96 | 0.97/0.98 | 0.92/0.94 |
| 12 | `cfg_3a70` | 2 | 0.82 | 0.77/0.77 | 0.56/0.56 |
| 13 | `cfg_6ab2` | 8 | 0.82 | 0.81/0.92 | 0.75/0.81 |
| 14 | `cfg_e938` | 4 | 0.94 | 0.84/0.85 | 0.76/0.77 |
| 15 | `cfg_bdb0` | 6 | 0.91 | 0.89/0.90 | 0.82/0.84 |
| 16 | `cfg_8f22` | 3 | 0.97 | 0.96/0.97 | 0.92/0.94 |
| 17 | `cfg_2731` | 1 | n/a | n/a/n/a | n/a/n/a |
| 18 | `cfg_e662` | 2 | 0.96 | 0.96/0.96 | 0.92/0.92 |
| 19 | `cfg_30e4` | 1 | n/a | n/a/n/a | n/a/n/a |
| 20 | `cfg_b81c` | 7 | 0.92 | 0.94/0.97 | 0.85/0.91 |
| 21 | `cfg_3324` | 3 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 22 | `cfg_b9f9` | 3 | 0.82 | 0.73/0.85 | 0.51/0.74 |
| 23 | `cfg_384f` | 1 | n/a | n/a/n/a | n/a/n/a |
| 24 | `cfg_3f8b` | 2 | 0.98 | 0.98/0.98 | 0.97/0.97 |
| 25 | `cfg_6a19` | 3 | 0.83 | 0.84/0.89 | 0.80/0.83 |
| 26 | `cfg_ad59` | 5 | 0.88 | 0.90/0.98 | 0.84/0.97 |
| 27 | `cfg_43ab` | 3 | 0.97 | 0.96/0.97 | 0.92/0.94 |
| 28 | `cfg_d144` | 3 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 29 | `cfg_4a3c` | 2 | 0.99 | 0.99/0.99 | 0.99/0.99 |
| 30 | `cfg_f2d9` | 4 | 0.81 | 0.84/0.92 | 0.74/0.89 |
| 31 | `cfg_6b6a` | 4 | 0.97 | 0.96/0.97 | 0.90/0.92 |
| 32 | `cfg_fa7c` | 4 | 0.92 | 0.96/0.97 | 0.95/0.98 |
| 33 | `cfg_5c0f` | 2 | 0.99 | 0.99/0.99 | 0.98/0.98 |
| 34 | `cfg_956f` | 4 | 0.91 | 0.92/0.93 | 0.84/0.85 |
| 35 | `cfg_6676` | 2 | 0.99 | 0.99/0.99 | 0.99/0.99 |
| 36 | `cfg_6ac2` | 4 | 0.98 | 0.97/0.99 | 0.95/0.95 |
| 37 | `cfg_a175` | 3 | 0.89 | 0.96/0.98 | 0.95/0.97 |
| 38 | `cfg_bee6` | 5 | 0.82 | 0.79/0.87 | 0.68/0.81 |
| 39 | `cfg_db0b` | 2 | 0.88 | 0.91/0.91 | 0.83/0.83 |
| 40 | `cfg_7776` | 1 | n/a | n/a/n/a | n/a/n/a |
| 41 | `cfg_7acc` | 4 | 0.90 | 0.90/0.92 | 0.75/0.80 |
| 42 | `cfg_c087` | 2 | 0.96 | 0.97/0.97 | 0.91/0.91 |
| 43 | `cfg_fa68` | 3 | 0.90 | 0.91/0.94 | 0.88/0.91 |
| 44 | `cfg_9330` | 1 | n/a | n/a/n/a | n/a/n/a |
| 45 | `cfg_9934` | 1 | n/a | n/a/n/a | n/a/n/a |
| 46 | `cfg_9b18` | 1 | n/a | n/a/n/a | n/a/n/a |
| 47 | `cfg_a69f` | 2 | 0.89 | 0.95/0.95 | 0.95/0.95 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.111e-03 over 40968 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1323.0, participation ratio 18.8, 95%-variance components 331 (rank bound T = 1239); raw grid 41472; raw + known prior 690504
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
None results are unchanged rules on the development period: supporting evidence, not an independent replication.

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
