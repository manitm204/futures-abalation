# Screening funnel -- mr_rty_v7_1h (development stages only)

- Code: `5342a94cdc84` (dirty working tree: True, diff sha256 `e22935eed467`)
- Config: `configs/funnel/mr_funnel_rty_v7_1h.yaml` sha256 `9376c054102cf159`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'RTY': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `989f2dacdc060a07` (162 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_rty_v5 gated 27 RTY candidates on 2023-2024 (5 passed) and mr_rty_v6 gated 108 (19 passed); this v7 grid was written after reading both, so RTY 2023-2024 is largely in-sample for v7. The stage-4 test and 40-trade rule were also shaped by ES 2023-2024.
- Holdout 2025+ previously inspected: **False** -- No RTY strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection). Correlated indices were scored on their 2025+ holdouts on 2026-10-24: ES (mr_es_v6_1h #8, #15), NQ (mr_nq_v7_15m #1 + mr_nq_v7_1h #119) and YM (mr_ym_v7_15m #9 + mr_ym_v7_1h #51). The RTY holdout is the only untouched test for this run.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 8640 | 8640 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 8640 | 8640 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 8640 | 7171 | 1469 | 0 |  | 6312 | 83.00 | 83.00 |  |
| 3 performance & risk | hard_gate | 7171 | 299 | 6872 | 0 |  | 0 | 3.46 | 4.17 |  |
| 4 parameter stability | hard_gate | 299 | 280 | 19 | 0 |  | 0 | 3.24 | 93.65 |  |
| 5 time stability | hard_gate | 280 | 280 | 0 | 0 |  | 241 | 3.24 | 100.00 |  |
| 6 deduplication | dedup | 280 | 162 |  |  | 118 |  | 1.88 | 57.86 | best 2 per cluster |
| 7 execution stress | hard_gate | 162 | 162 | 0 | 0 |  | 0 | 1.88 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 162 |  |  |  |  |  |  |  | diagnostic only: unverified: 162 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 1469 |
| s2:hard_reject:years_with_>=10_trades | 96 |
| s3:hard_reject:max_drawdown | 671 |
| s3:hard_reject:net_return | 2346 |
| s3:hard_reject:sharpe | 6872 |
| s4:hard_reject:local_median_sharpe | 19 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_c0c4` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 14/69/18 | 101 | 60.9% | 10.0% | 1.37 | -7.3% | 211 | 2.15 | 9.1% | 46.2 | 11/11 | 1.00 | 0.83 | 0.54 | 4 | 39.6% | 0.35 | 0.46 | 58.8% | 57.5% | 30.7% | 54.4%/42.2% | n/a (profitable_beyond_25.0x) | pass | 0.788 (unverified) | 0.08 |
| 2 | `cfg_195d` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 20/62/20 | 102 | 48.0% | 8.2% | 1.08 | -8.3% | 162 | 1.75 | 9.1% | 46.9 | 11/11 | 1.00 | 0.83 | 0.25 | 5 | 24.3% | 0.42 | 0.64 | 46.6% | 45.5% | 28.1% | 42.9%/31.0% | 23.8 (interpolated) | pass | 0.543 (unverified) | -0.06 |
| 3 | `cfg_0209` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 14/68/20 | 102 | 43.8% | 7.5% | 0.99 | -9.9% | 148 | 1.66 | 9.1% | 46.8 | 10/10 | 1.00 | 0.82 | 0.17 | 5 | 27.5% | 0.37 | 0.62 | 42.7% | 42.0% | 53.6% | 40.4%/29.4% | 22.1 (interpolated) | pass | 0.459 (unverified) | 0.11 |
| 4 | `cfg_3a9b` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 4/78/20 | 102 | 47.0% | 8.0% | 1.07 | -8.1% | 162 | 1.74 | 9.5% | 46.9 | 10/10 | 1.00 | 0.82 | 0.25 | 5 | 24.6% | 0.40 | 0.60 | 46.1% | 44.4% | 26.9% | 42.6%/33.3% | 23.2 (interpolated) | pass | 0.532 (unverified) | -0.06 |
| 5 | `cfg_63d2` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 31/51/20 | 102 | 41.3% | 7.2% | 0.96 | -9.6% | 157 | 1.63 | 8.6% | 47.0 | 9/9 | 1.00 | 0.80 | 0.17 | 5 | 27.6% | 0.33 | 0.61 | 40.8% | 40.2% | 48.6% | 38.4%/29.2% | 20.9 (interpolated) | pass | 0.434 (unverified) | 0.25 |
| 6 | `cfg_8624` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 25/79/0 | 104 | 59.3% | 9.8% | 1.13 | -11.9% | 293 | 1.82 | 13.9% | 48.2 | 9/9 | 1.00 | 0.91 | 0.21 | 4 | 30.5% | 0.39 | 0.51 | 57.2% | 55.4% | 44.5% | 51.0%/37.6% | n/a (profitable_beyond_25.0x) | pass | 0.580 (unverified) | 0.20 |
| 7 | `cfg_c0cc` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=20, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 2/88/32 | 122 | 33.2% | 5.9% | 1.03 | -6.8% | 339 | 1.69 | 7.2% | 55.5 | 7/7 | 1.00 | 0.50 | 0.54 | 5 | 16.6% | 0.47 | 0.63 | 31.9% | 30.5% | 22.1% | 31.9%/23.9% | 14.6 (interpolated) | pass | 0.499 (unverified) | 0.17 |
| 8 | `cfg_b053` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 5/85/32 | 122 | 32.2% | 5.8% | 1.02 | -6.8% | 339 | 1.67 | 7.2% | 55.6 | 8/8 | 1.00 | 0.65 | 0.38 | 5 | 15.7% | 0.49 | 0.65 | 30.6% | 29.7% | 22.6% | 31.3%/23.4% | 14.3 (interpolated) | pass | 0.489 (unverified) | 0.17 |
| 9 | `cfg_6023` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 7/82/35 | 124 | 47.2% | 8.0% | 1.20 | -4.9% | 215 | 1.79 | 7.2% | 57.1 | 9/9 | 1.00 | 0.77 | 0.43 | 4 | 25.5% | 0.39 | 0.59 | 45.3% | 44.3% | 38.5% | 44.6%/37.0% | 19.6 (interpolated) | pass | 0.650 (unverified) | 0.57 |
| 10 | `cfg_be97` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 44/74/0 | 118 | 72.5% | 11.5% | 1.21 | -7.8% | 223 | 1.93 | 15.0% | 55.1 | 8/8 | 1.00 | 0.86 | 0.35 | 5 | 45.0% | 0.38 | 0.49 | 71.7% | 71.0% | 53.2% | 58.9%/44.2% | n/a (profitable_beyond_25.0x) | pass | 0.661 (unverified) | 0.28 |
| 11 | `cfg_5754` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=12, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 16/99/0 | 115 | 61.8% | 10.1% | 0.96 | -16.6% | 280 | 1.58 | 16.5% | 54.3 | 8/8 | 1.00 | 0.66 | 0.30 | 5 | 22.5% | 0.59 | 0.63 | 60.3% | 58.6% | 41.4% | 51.3%/39.7% | n/a (profitable_beyond_25.0x) | pass | 0.434 (unverified) | 0.58 |
| 12 | `cfg_fbc1` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 14/70/22 | 106 | 42.2% | 7.3% | 1.05 | -7.8% | 184 | 1.65 | 9.6% | 48.1 | 10/10 | 1.00 | 0.77 | 0.28 | 5 | 25.9% | 0.37 | 0.64 | 41.1% | 40.3% | 36.3% | 41.0%/28.7% | 20.7 (interpolated) | pass | 0.510 (unverified) | 0.02 |
| 13 | `cfg_bbb8` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=18, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 6/77/18 | 101 | 52.9% | 8.9% | 1.18 | -7.2% | 216 | 1.99 | 9.3% | 46.1 | 10/10 | 0.90 | 0.67 | 0.51 | 4 | 34.2% | 0.31 | 0.52 | 51.6% | 49.5% | 24.2% | 47.7%/39.1% | n/a (profitable_beyond_25.0x) | pass | 0.635 (unverified) | 0.02 |
| 14 | `cfg_89fc` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 19/74/24 | 117 | 52.9% | 8.9% | 1.12 | -7.4% | 173 | 1.70 | 9.9% | 54.1 | 11/11 | 1.00 | 0.82 | 0.30 | 5 | 32.7% | 0.33 | 0.64 | 50.6% | 49.2% | 41.3% | 48.2%/33.5% | 22.5 (interpolated) | pass | 0.575 (unverified) | 0.15 |
| 15 | `cfg_3c7a` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 20/73/22 | 115 | 46.5% | 7.9% | 1.01 | -5.1% | 177 | 1.64 | 9.9% | 52.4 | 11/11 | 1.00 | 0.67 | 0.34 | 5 | 22.4% | 0.46 | 0.71 | 45.7% | 44.5% | 38.3% | 44.0%/31.8% | 20.7 (interpolated) | pass | 0.476 (unverified) | 0.25 |
| 16 | `cfg_689e` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 2/87/24 | 113 | 36.7% | 6.5% | 0.96 | -5.9% | 239 | 1.62 | 7.0% | 52.0 | 9/9 | 0.89 | 0.85 | 0.11 | 4 | 16.2% | 0.49 | 0.75 | 35.4% | 33.1% | 37.3% | 35.5%/24.8% | 17.2 (interpolated) | pass | 0.433 (unverified) | 0.45 |
| 17 | `cfg_81a9` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 34/82/0 | 116 | 58.2% | 9.6% | 0.99 | -9.1% | 216 | 1.67 | 15.4% | 54.1 | 8/8 | 1.00 | 0.75 | 0.24 | 5 | 26.0% | 0.49 | 0.60 | 56.3% | 55.1% | 51.3% | 52.5%/39.7% | 24.0 (interpolated) | pass | 0.462 (unverified) | -0.19 |
| 18 | `cfg_5d27` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=18, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 8/78/21 | 107 | 29.6% | 5.3% | 0.87 | -7.2% | 336 | 1.55 | 6.6% | 48.9 | 10/10 | 1.00 | 0.72 | 0.15 | 4 | 15.3% | 0.48 | 0.59 | 27.6% | 26.8% | 28.4% | 27.1%/17.7% | 15.3 (interpolated) | pass | 0.366 (unverified) | 0.22 |
| 19 | `cfg_e300` | timeframe=1h, mean_type=ema, mean_lookback=90, std_lookback=12, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 5/85/23 | 113 | 53.1% | 8.9% | 1.02 | -8.6% | 163 | 1.72 | 10.2% | 52.8 | 10/10 | 0.90 | 0.63 | 0.40 | 5 | 30.2% | 0.36 | 0.61 | 51.7% | 50.5% | 37.2% | 48.5%/37.8% | 23.8 (interpolated) | pass | 0.489 (unverified) | 0.63 |
| 20 | `cfg_8200` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=20, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 2/82/22 | 106 | 38.9% | 6.8% | 0.97 | -8.0% | 184 | 1.61 | 9.9% | 48.0 | 9/9 | 1.00 | 0.71 | 0.26 | 5 | 24.8% | 0.35 | 0.68 | 37.8% | 36.6% | 30.0% | 35.5%/26.4% | 19.2 (interpolated) | pass | 0.446 (unverified) | -0.02 |
| 21 | `cfg_2c25` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 12/80/45 | 137 | 39.3% | 6.9% | 1.01 | -6.6% | 258 | 1.61 | 7.8% | 62.5 | 9/9 | 1.00 | 0.71 | 0.30 | 4 | 19.6% | 0.48 | 0.60 | 37.6% | 35.9% | 43.7% | 37.7%/27.6% | 15.4 (interpolated) | pass | 0.473 (unverified) | 0.35 |
| 22 | `cfg_591a` | timeframe=1h, mean_type=sma, mean_lookback=110, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 22/78/0 | 100 | 54.8% | 9.1% | 1.09 | -8.7% | 181 | 1.74 | 13.9% | 46.7 | 9/9 | 1.00 | 0.80 | 0.30 | 4 | 31.8% | 0.40 | 0.59 | 52.8% | 52.0% | 43.9% | 47.7%/36.5% | n/a (profitable_beyond_25.0x) | pass | 0.553 (unverified) | -0.30 |
| 23 | `cfg_75fc` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 17/72/25 | 114 | 35.9% | 6.3% | 0.83 | -8.2% | 164 | 1.47 | 9.9% | 51.9 | 11/11 | 1.00 | 0.65 | 0.18 | 4 | 18.3% | 0.46 | 0.85 | 34.3% | 33.3% | 25.2% | 34.4%/24.8% | 16.7 (interpolated) | pass | 0.322 (unverified) | -0.08 |
| 24 | `cfg_da5c` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 7/82/11 | 100 | 31.9% | 5.7% | 0.90 | -8.0% | 440 | 1.69 | 6.4% | 46.0 | 9/9 | 1.00 | 0.82 | 0.08 | 4 | 15.8% | 0.50 | 0.66 | 30.9% | 29.7% | 49.5% | 31.2%/23.5% | 17.7 (interpolated) | pass | 0.375 (unverified) | 0.61 |
| 25 | `cfg_3d4c` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 36/68/0 | 104 | 46.8% | 8.0% | 0.97 | -13.0% | 310 | 1.69 | 13.2% | 47.9 | 8/8 | 1.00 | 0.73 | 0.24 | 4 | 25.0% | 0.39 | 0.53 | 44.8% | 43.2% | 38.0% | 39.7%/30.5% | 22.8 (interpolated) | pass | 0.442 (unverified) | 0.18 |
| 26 | `cfg_2843` | timeframe=1h, mean_type=sma, mean_lookback=110, std_lookback=15, entry_z=-3.0, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 8/92/0 | 100 | 53.8% | 9.0% | 1.06 | -8.7% | 194 | 1.70 | 14.4% | 46.6 | 8/8 | 1.00 | 0.72 | 0.34 | 4 | 29.5% | 0.44 | 0.60 | 52.3% | 51.2% | 45.1% | 47.0%/35.0% | n/a (profitable_beyond_25.0x) | pass | 0.523 (unverified) | -0.32 |
| 27 | `cfg_d16c` | timeframe=1h, mean_type=ema, mean_lookback=90, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 21/69/23 | 113 | 53.7% | 9.0% | 1.06 | -8.7% | 156 | 1.75 | 9.8% | 53.0 | 11/11 | 0.91 | 0.68 | 0.39 | 5 | 32.0% | 0.40 | 0.59 | 52.5% | 51.2% | 34.5% | 49.2%/37.5% | 23.4 (interpolated) | pass | 0.526 (unverified) | 0.64 |
| 28 | `cfg_2c81` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 12/92/0 | 104 | 43.9% | 7.6% | 0.81 | -9.0% | 376 | 1.52 | 14.8% | 48.3 | 8/8 | 1.00 | 0.68 | 0.14 | 4 | 17.0% | 0.61 | 0.75 | 42.5% | 41.1% | 50.5% | 40.7%/28.4% | 21.7 (interpolated) | pass | 0.311 (unverified) | -0.42 |
| 29 | `cfg_2625` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 18/71/11 | 100 | 29.7% | 5.4% | 0.87 | -8.0% | 440 | 1.65 | 6.3% | 45.9 | 8/8 | 1.00 | 0.79 | 0.08 | 4 | 15.0% | 0.49 | 0.69 | 28.8% | 28.3% | 49.9% | 28.8%/20.1% | 16.9 (interpolated) | pass | 0.353 (unverified) | 0.70 |
| 30 | `cfg_2d69` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 2/88/23 | 113 | 29.7% | 5.3% | 0.85 | -10.4% | 194 | 1.51 | 7.0% | 52.0 | 9/9 | 1.00 | 0.76 | 0.09 | 5 | 14.7% | 0.46 | 0.85 | 29.0% | 27.8% | 36.4% | 27.3%/19.7% | 14.6 (interpolated) | pass | 0.337 (unverified) | 0.43 |
| 31 | `cfg_317c` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 37/79/0 | 116 | 61.2% | 10.0% | 1.01 | -14.3% | 280 | 1.61 | 15.2% | 54.9 | 9/9 | 1.00 | 0.74 | 0.26 | 5 | 27.3% | 0.49 | 0.53 | 60.0% | 58.8% | 40.7% | 52.5%/39.1% | 24.7 (interpolated) | pass | 0.476 (unverified) | 0.47 |
| 32 | `cfg_d21a` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 4/79/20 | 103 | 27.8% | 5.0% | 0.83 | -11.1% | 624 | 1.59 | 6.2% | 47.3 | 10/10 | 1.00 | 0.75 | 0.07 | 4 | 15.7% | 0.44 | 0.71 | 27.0% | 26.2% | 31.7% | 27.4%/19.6% | 15.1 (interpolated) | pass | 0.327 (unverified) | 0.27 |
| 33 | `cfg_48f4` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 31/78/0 | 109 | 42.7% | 7.4% | 0.81 | -8.5% | 270 | 1.51 | 14.6% | 51.0 | 9/9 | 1.00 | 0.73 | 0.09 | 5 | 16.3% | 0.55 | 0.68 | 41.2% | 40.1% | 27.3% | 37.7%/27.2% | 19.9 (interpolated) | pass | 0.312 (unverified) | 0.01 |
| 34 | `cfg_35e8` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 6/84/23 | 113 | 29.2% | 5.3% | 0.84 | -10.6% | 194 | 1.50 | 6.9% | 52.0 | 10/10 | 1.00 | 0.78 | 0.06 | 5 | 14.2% | 0.47 | 0.86 | 28.5% | 26.8% | 36.3% | 27.8%/20.2% | 14.5 (interpolated) | pass | 0.328 (unverified) | 0.43 |
| 35 | `cfg_3c83` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=10, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 23/94/0 | 117 | 53.3% | 8.9% | 0.88 | -12.6% | 245 | 1.54 | 16.2% | 54.6 | 7/7 | 1.00 | 0.71 | 0.17 | 5 | 24.8% | 0.46 | 0.67 | 50.9% | 50.1% | 32.9% | 47.8%/37.0% | 22.7 (interpolated) | pass | 0.360 (unverified) | 0.37 |
| 36 | `cfg_ed6b` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 34/78/0 | 112 | 43.0% | 7.4% | 0.83 | -9.2% | 401 | 1.54 | 14.9% | 52.4 | 9/9 | 1.00 | 0.63 | 0.19 | 4 | 14.6% | 0.57 | 0.70 | 41.0% | 40.1% | 38.3% | 38.3%/29.0% | 19.5 (interpolated) | pass | 0.319 (unverified) | 0.12 |
| 37 | `cfg_37de` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 15/72/23 | 110 | 38.7% | 6.8% | 0.88 | -8.2% | 416 | 1.58 | 9.6% | 51.2 | 11/11 | 1.00 | 0.70 | 0.18 | 4 | 22.4% | 0.42 | 0.78 | 38.1% | 36.4% | 46.3% | 37.3%/26.8% | 18.6 (interpolated) | pass | 0.361 (unverified) | -0.15 |
| 38 | `cfg_2a22` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 33/56/21 | 110 | 47.5% | 8.1% | 1.07 | -7.9% | 240 | 1.74 | 9.1% | 51.3 | 10/10 | 1.00 | 0.60 | 0.48 | 4 | 22.8% | 0.52 | 0.46 | 46.6% | 45.1% | 30.6% | 42.5%/32.4% | 22.0 (interpolated) | pass | 0.535 (unverified) | 0.59 |
| 39 | `cfg_4b0a` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 20/69/21 | 110 | 49.5% | 8.4% | 1.00 | -11.0% | 229 | 1.71 | 9.8% | 51.2 | 11/11 | 1.00 | 0.73 | 0.27 | 4 | 21.6% | 0.56 | 0.54 | 47.4% | 45.9% | 26.1% | 42.7%/33.0% | 22.4 (interpolated) | pass | 0.465 (unverified) | 0.71 |
| 40 | `cfg_f682` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.5 | 27/97/29 | 153 | 61.4% | 10.1% | 1.07 | -9.6% | 253 | 1.65 | 14.0% | 69.7 | 11/11 | 1.00 | 0.52 | 0.55 | 5 | 38.1% | 0.34 | 0.54 | 59.8% | 58.1% | 70.0% | 56.7%/42.2% | 19.4 (interpolated) | pass | 0.534 (unverified) | 0.03 |
| 41 | `cfg_63a8` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=18, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 20/73/44 | 137 | 36.8% | 6.5% | 0.96 | -6.6% | 258 | 1.58 | 7.6% | 62.5 | 8/8 | 0.88 | 0.60 | 0.37 | 4 | 18.2% | 0.49 | 0.62 | 35.3% | 33.9% | 38.4% | 37.1%/26.4% | 14.6 (interpolated) | pass | 0.428 (unverified) | 0.36 |
| 42 | `cfg_d2d0` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 21/72/38 | 131 | 28.7% | 5.2% | 0.81 | -6.8% | 346 | 1.47 | 7.3% | 60.7 | 8/8 | 1.00 | 0.68 | 0.12 | 4 | 15.4% | 0.46 | 0.66 | 27.5% | 26.3% | 39.1% | 28.5%/22.5% | 12.3 (interpolated) | pass | 0.303 (unverified) | 0.08 |
| 43 | `cfg_bbdf` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 3/79/36 | 118 | 27.9% | 5.1% | 0.80 | -7.9% | 438 | 1.54 | 6.8% | 54.3 | 9/9 | 1.00 | 0.72 | 0.08 | 5 | 15.2% | 0.42 | 0.73 | 26.9% | 25.9% | 30.2% | 29.0%/19.7% | 13.4 (interpolated) | pass | 0.287 (unverified) | 0.61 |
| 44 | `cfg_d8e0` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 19/74/23 | 116 | 34.7% | 6.2% | 0.82 | -8.5% | 252 | 1.47 | 10.2% | 53.9 | 10/10 | 1.00 | 0.58 | 0.23 | 4 | 15.4% | 0.49 | 0.74 | 34.0% | 32.6% | 20.4% | 31.2%/22.0% | 16.3 (interpolated) | pass | 0.308 (unverified) | -0.28 |
| 45 | `cfg_b5cf` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-3.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 4/89/24 | 117 | 45.4% | 7.8% | 0.95 | -10.9% | 173 | 1.59 | 10.6% | 53.8 | 10/10 | 1.00 | 0.69 | 0.26 | 5 | 23.8% | 0.43 | 0.74 | 43.5% | 42.1% | 38.7% | 41.8%/33.4% | 20.0 (interpolated) | pass | 0.426 (unverified) | 0.06 |
| 46 | `cfg_e8ef` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-3.0, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 19/97/0 | 116 | 60.9% | 10.0% | 0.97 | -10.9% | 350 | 1.65 | 16.5% | 53.9 | 7/7 | 1.00 | 0.65 | 0.32 | 5 | 24.3% | 0.57 | 0.66 | 59.0% | 56.8% | 55.6% | 53.5%/38.5% | 24.9 (interpolated) | pass | 0.439 (unverified) | -0.13 |
| 47 | `cfg_ccfb` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=12, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=2.0 | 15/89/72 | 176 | 64.8% | 10.5% | 0.91 | -13.4% | 360 | 1.39 | 20.4% | 83.5 | 9/9 | 1.00 | 0.66 | 0.25 | 4 | 28.7% | 0.45 | 0.62 | 61.9% | 60.3% | 22.1% | 51.5%/35.2% | 17.7 (interpolated) | pass | 0.388 (unverified) | 0.87 |
| 48 | `cfg_28e7` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 25/91/53 | 169 | 53.9% | 9.0% | 0.93 | -8.7% | 220 | 1.48 | 14.2% | 76.7 | 11/11 | 0.91 | 0.46 | 0.47 | 4 | 35.8% | 0.31 | 0.62 | 51.5% | 49.5% | 38.0% | 47.9%/35.8% | 16.0 (interpolated) | pass | 0.408 (unverified) | -0.02 |
| 49 | `cfg_4065` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=18, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 16/70/21 | 107 | 26.5% | 4.8% | 0.81 | -7.2% | 336 | 1.49 | 6.4% | 48.8 | 9/9 | 0.89 | 0.57 | 0.23 | 4 | 13.2% | 0.50 | 0.60 | 25.2% | 24.6% | 24.7% | 25.6%/18.4% | 14.2 (interpolated) | pass | 0.310 (unverified) | 0.22 |
| 50 | `cfg_fbbc` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=15, entry_z=-3.0, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 8/98/0 | 106 | 45.0% | 7.7% | 0.88 | -7.8% | 223 | 1.62 | 15.3% | 48.5 | 8/8 | 1.00 | 0.66 | 0.22 | 4 | 22.0% | 0.43 | 0.64 | 43.9% | 42.1% | 28.3% | 41.9%/29.6% | 21.7 (interpolated) | pass | 0.363 (unverified) | -0.01 |
| 51 | `cfg_f4fb` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=12, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 1/88/21 | 110 | 48.9% | 8.3% | 0.94 | -11.0% | 233 | 1.67 | 10.3% | 51.2 | 10/10 | 1.00 | 0.65 | 0.29 | 4 | 27.2% | 0.44 | 0.64 | 46.9% | 44.8% | 26.3% | 45.1%/33.0% | 22.3 (interpolated) | pass | 0.417 (unverified) | 0.76 |
| 52 | `cfg_ed1f` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 22/85/0 | 107 | 43.3% | 7.5% | 0.87 | -8.0% | 223 | 1.58 | 14.7% | 49.1 | 9/9 | 1.00 | 0.69 | 0.18 | 4 | 19.9% | 0.46 | 0.67 | 42.5% | 40.0% | 32.2% | 40.7%/28.9% | 20.8 (interpolated) | pass | 0.356 (unverified) | -0.03 |
| 53 | `cfg_4345` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 30/97/51 | 178 | 58.3% | 9.6% | 1.00 | -8.9% | 328 | 1.52 | 14.9% | 82.5 | 11/11 | 1.00 | 0.81 | 0.19 | 4 | 31.5% | 0.40 | 0.52 | 57.3% | 54.1% | 25.4% | 52.4%/37.4% | 16.2 (interpolated) | pass | 0.471 (unverified) | 0.10 |
| 54 | `cfg_9070` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 29/75/0 | 104 | 38.2% | 6.7% | 0.76 | -9.0% | 383 | 1.48 | 13.8% | 48.0 | 9/9 | 1.00 | 0.75 | 0.01 | 3 | 13.9% | 0.53 | 0.83 | 36.9% | 35.5% | 55.9% | 36.6%/25.3% | 19.5 (interpolated) | pass | 0.279 (unverified) | -0.43 |
| 55 | `cfg_c4cd` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 6/87/22 | 115 | 44.2% | 7.6% | 0.93 | -6.5% | 169 | 1.59 | 10.5% | 52.4 | 10/10 | 1.00 | 0.59 | 0.34 | 5 | 18.2% | 0.53 | 0.74 | 42.3% | 40.6% | 35.6% | 40.5%/28.4% | 19.3 (interpolated) | pass | 0.399 (unverified) | 0.26 |
| 56 | `cfg_3791` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 7/100/52 | 159 | 47.8% | 8.1% | 0.88 | -9.9% | 159 | 1.41 | 13.7% | 72.6 | 10/10 | 0.80 | 0.56 | 0.32 | 5 | 30.4% | 0.31 | 0.64 | 45.6% | 44.1% | 56.6% | 40.8%/28.1% | 15.5 (interpolated) | pass | 0.359 (unverified) | 0.02 |
| 57 | `cfg_7502` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 4/83/23 | 110 | 45.6% | 7.8% | 0.91 | -7.6% | 166 | 1.58 | 10.0% | 51.4 | 10/10 | 1.00 | 0.61 | 0.30 | 5 | 23.8% | 0.44 | 0.74 | 44.3% | 42.8% | 47.9% | 44.2%/32.5% | 21.1 (interpolated) | pass | 0.388 (unverified) | 0.84 |
| 58 | `cfg_bcd7` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 34/89/89 | 212 | 66.1% | 10.7% | 1.03 | -11.0% | 195 | 1.45 | 16.0% | 98.4 | 10/10 | 1.00 | 0.71 | 0.32 | 5 | 40.3% | 0.39 | 0.53 | 62.1% | 60.4% | 29.3% | 53.4%/38.1% | 15.1 (interpolated) | pass | 0.497 (unverified) | -0.12 |
| 59 | `cfg_e0cc` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=18, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 13/99/0 | 112 | 52.2% | 8.8% | 0.88 | -9.9% | 453 | 1.64 | 15.9% | 51.3 | 8/8 | 1.00 | 0.63 | 0.26 | 4 | 24.8% | 0.47 | 0.71 | 51.3% | 49.3% | 51.3% | 43.3%/30.6% | 23.1 (interpolated) | pass | 0.369 (unverified) | -0.27 |
| 60 | `cfg_8cd1` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=18, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 7/75/38 | 120 | 30.0% | 5.4% | 0.88 | -8.0% | 258 | 1.53 | 6.9% | 54.9 | 9/9 | 1.00 | 0.62 | 0.26 | 4 | 18.4% | 0.39 | 0.58 | 28.7% | 27.8% | 28.0% | 28.2%/20.8% | 13.9 (interpolated) | pass | 0.355 (unverified) | 0.32 |
| 61 | `cfg_fd1e` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 13/70/25 | 108 | 41.1% | 7.1% | 1.03 | -8.1% | 319 | 1.65 | 9.5% | 48.9 | 11/11 | 1.00 | 0.92 | 0.10 | 5 | 24.7% | 0.40 | 0.62 | 38.9% | 37.9% | 30.2% | 37.5%/28.3% | 19.7 (interpolated) | pass | 0.494 (unverified) | 0.09 |
| 62 | `cfg_2c46` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 12/88/0 | 100 | 54.4% | 9.1% | 1.10 | -9.2% | 137 | 1.89 | 9.8% | 45.9 | 8/8 | 1.00 | 0.57 | 0.53 | 5 | 31.2% | 0.36 | 0.58 | 52.9% | 51.9% | 59.7% | 45.5%/36.3% | n/a (profitable_beyond_25.0x) | pass | 0.560 (unverified) | -0.11 |
| 63 | `cfg_3949` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 9/84/38 | 131 | 29.3% | 5.3% | 0.81 | -6.6% | 476 | 1.48 | 7.4% | 60.7 | 9/9 | 1.00 | 0.73 | 0.08 | 4 | 16.3% | 0.44 | 0.64 | 28.1% | 27.0% | 42.0% | 29.9%/22.9% | 12.8 (interpolated) | pass | 0.305 (unverified) | 0.17 |
| 64 | `cfg_5a53` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=12, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 13/97/0 | 110 | 42.4% | 7.3% | 0.75 | -18.5% | 280 | 1.43 | 15.9% | 51.4 | 7/7 | 1.00 | 0.56 | 0.20 | 4 | 12.8% | 0.70 | 0.78 | 42.1% | 40.3% | 43.3% | 36.2%/26.7% | 19.8 (interpolated) | pass | 0.264 (unverified) | 0.19 |
| 65 | `cfg_6024` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 14/87/29 | 130 | 33.3% | 5.9% | 0.93 | -6.3% | 185 | 1.53 | 7.6% | 59.1 | 10/10 | 1.00 | 0.70 | 0.23 | 4 | 20.5% | 0.35 | 0.57 | 32.2% | 30.9% | 37.0% | 32.5%/22.6% | 13.8 (interpolated) | pass | 0.409 (unverified) | 0.32 |
| 66 | `cfg_5857` | timeframe=1h, mean_type=ema, mean_lookback=70, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 8/81/20 | 109 | 40.5% | 7.1% | 0.78 | -17.4% | 193 | 1.56 | 10.0% | 50.4 | 9/9 | 0.89 | 0.81 | -0.03 | 5 | 14.8% | 0.64 | 0.69 | 39.5% | 38.8% | 36.4% | 39.1%/26.3% | 19.8 (interpolated) | pass | 0.320 (unverified) | 0.05 |
| 67 | `cfg_b119` | timeframe=1h, mean_type=sma, mean_lookback=110, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=2.5 | 47/54/41 | 142 | 45.7% | 7.8% | 0.82 | -12.5% | 546 | 1.41 | 14.9% | 66.3 | 9/9 | 1.00 | 0.62 | 0.20 | 4 | 9.7% | 0.66 | 0.66 | 43.3% | 41.1% | 41.2% | 39.8%/28.2% | 16.6 (interpolated) | pass | 0.317 (unverified) | -0.03 |
| 68 | `cfg_f465` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 21/79/0 | 100 | 49.2% | 8.3% | 1.03 | -9.3% | 140 | 1.82 | 9.5% | 45.7 | 9/9 | 1.00 | 0.67 | 0.36 | 5 | 28.2% | 0.36 | 0.63 | 48.1% | 47.2% | 53.1% | 43.1%/31.8% | 24.4 (interpolated) | pass | 0.495 (unverified) | -0.16 |
| 69 | `cfg_0031` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=18, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 3/80/25 | 108 | 36.0% | 6.3% | 0.92 | -8.2% | 372 | 1.58 | 9.8% | 48.9 | 10/10 | 1.00 | 0.93 | -0.00 | 4 | 19.8% | 0.45 | 0.66 | 34.6% | 33.7% | 26.7% | 31.7%/23.9% | 17.9 (interpolated) | pass | 0.405 (unverified) | 0.10 |
| 70 | `cfg_492d` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 19/88/52 | 159 | 42.6% | 7.4% | 0.81 | -9.9% | 194 | 1.38 | 13.4% | 72.7 | 11/11 | 0.82 | 0.54 | 0.26 | 4 | 27.6% | 0.28 | 0.65 | 41.1% | 39.5% | 52.0% | 37.1%/23.8% | 13.7 (interpolated) | pass | 0.300 (unverified) | 0.02 |
| 71 | `cfg_e962` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 18/75/25 | 118 | 35.0% | 6.2% | 0.81 | -7.5% | 198 | 1.47 | 10.3% | 54.2 | 11/11 | 1.00 | 0.64 | 0.17 | 5 | 22.8% | 0.31 | 0.88 | 34.2% | 33.0% | 30.0% | 33.3%/24.4% | 15.9 (interpolated) | pass | 0.308 (unverified) | 0.01 |
| 72 | `cfg_72f6` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=2.5 | 32/71/45 | 148 | 42.6% | 7.4% | 0.75 | -11.9% | 593 | 1.36 | 16.8% | 68.5 | 10/10 | 1.00 | 0.69 | 0.06 | 4 | 14.1% | 0.56 | 0.71 | 41.1% | 38.8% | 44.5% | 39.5%/22.9% | 14.9 (interpolated) | pass | 0.263 (unverified) | -0.03 |
| 73 | `cfg_77a5` | timeframe=1h, mean_type=ema, mean_lookback=70, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 10/71/33 | 114 | 54.8% | 9.1% | 0.89 | -16.5% | 434 | 1.58 | 14.2% | 52.3 | 8/8 | 0.88 | 0.58 | 0.31 | 4 | 36.8% | 0.33 | 0.63 | 53.8% | 53.0% | 31.8% | 45.9%/32.4% | 23.3 (interpolated) | pass | 0.374 (unverified) | -0.12 |
| 74 | `cfg_745b` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 58/73/54 | 185 | 54.9% | 9.2% | 0.96 | -9.4% | 158 | 1.50 | 14.3% | 85.6 | 10/10 | 1.00 | 0.61 | 0.34 | 5 | 28.9% | 0.47 | 0.52 | 52.6% | 50.4% | 20.1% | 47.8%/35.4% | 15.0 (interpolated) | pass | 0.436 (unverified) | 0.04 |
| 75 | `cfg_34df` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 22/65/23 | 110 | 39.0% | 6.8% | 0.85 | -7.4% | 105 | 1.53 | 9.4% | 51.3 | 11/11 | 1.00 | 0.60 | 0.25 | 5 | 23.6% | 0.36 | 0.70 | 37.8% | 36.9% | 44.5% | 36.7%/24.9% | 18.9 (interpolated) | pass | 0.334 (unverified) | 0.71 |
| 76 | `cfg_b7f1` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 16/73/19 | 108 | 51.7% | 8.7% | 0.95 | -16.2% | 142 | 1.71 | 9.7% | 49.2 | 10/10 | 1.00 | 0.71 | 0.24 | 5 | 33.6% | 0.35 | 0.66 | 50.1% | 47.8% | 25.0% | 46.2%/35.9% | 23.4 (interpolated) | pass | 0.441 (unverified) | -0.19 |
| 77 | `cfg_713f` | timeframe=1h, mean_type=sma, mean_lookback=110, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 40/61/0 | 101 | 41.8% | 7.2% | 0.83 | -10.3% | 223 | 1.56 | 12.4% | 47.6 | 8/8 | 1.00 | 0.76 | 0.07 | 4 | 7.7% | 0.75 | 0.77 | 40.3% | 38.2% | 44.4% | 38.7%/27.7% | 20.7 (interpolated) | pass | 0.331 (unverified) | -0.41 |
| 78 | `cfg_c96a` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 17/54/34 | 105 | 45.3% | 7.8% | 0.82 | -15.3% | 380 | 1.48 | 12.5% | 49.0 | 9/9 | 0.89 | 0.67 | 0.15 | 4 | 19.7% | 0.48 | 0.72 | 43.8% | 43.1% | 48.5% | 38.3%/25.3% | 22.2 (interpolated) | pass | 0.325 (unverified) | 0.17 |
| 79 | `cfg_e45d` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 34/40/35 | 109 | 44.8% | 7.7% | 0.85 | -15.3% | 437 | 1.48 | 11.7% | 50.7 | 8/8 | 0.88 | 0.72 | 0.14 | 4 | 24.2% | 0.39 | 0.61 | 44.1% | 43.2% | 44.6% | 38.4%/28.7% | 21.3 (interpolated) | pass | 0.348 (unverified) | 0.22 |
| 80 | `cfg_a69c` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-3.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 6/83/19 | 108 | 50.4% | 8.5% | 0.93 | -16.1% | 142 | 1.69 | 9.9% | 49.1 | 9/9 | 1.00 | 0.70 | 0.23 | 5 | 32.8% | 0.35 | 0.68 | 49.3% | 47.9% | 32.4% | 45.6%/34.0% | 23.0 (interpolated) | pass | 0.424 (unverified) | -0.17 |
| 81 | `cfg_9f9f` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=12, entry_z=-3.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 8/105/49 | 162 | 37.1% | 6.5% | 0.76 | -9.2% | 226 | 1.33 | 14.1% | 75.0 | 10/10 | 1.00 | 0.57 | 0.20 | 5 | 21.3% | 0.40 | 0.77 | 35.4% | 34.0% | 31.1% | 34.5%/23.3% | 12.6 (interpolated) | pass | 0.272 (unverified) | -0.36 |
| 82 | `cfg_f35e` | timeframe=1h, mean_type=ema, mean_lookback=70, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 28/53/33 | 114 | 49.3% | 8.4% | 0.86 | -16.7% | 429 | 1.53 | 13.0% | 52.7 | 9/9 | 0.89 | 0.74 | 0.11 | 4 | 32.4% | 0.34 | 0.58 | 48.7% | 48.0% | 24.6% | 44.1%/29.5% | 22.0 (interpolated) | pass | 0.345 (unverified) | -0.16 |
| 83 | `cfg_a006` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 37/58/43 | 138 | 50.9% | 8.6% | 0.87 | -14.2% | 395 | 1.46 | 15.1% | 62.9 | 9/9 | 1.00 | 0.64 | 0.23 | 4 | 15.9% | 0.57 | 0.68 | 49.1% | 48.3% | 70.9% | 47.6%/34.4% | 19.0 (interpolated) | pass | 0.354 (unverified) | 0.03 |
| 84 | `cfg_7e26` | timeframe=1h, mean_type=ema, mean_lookback=70, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 23/66/20 | 109 | 36.9% | 6.5% | 0.75 | -16.7% | 291 | 1.53 | 9.6% | 50.4 | 10/10 | 0.90 | 0.77 | -0.02 | 4 | 12.6% | 0.66 | 0.73 | 35.3% | 33.3% | 27.5% | 35.2%/23.3% | 17.0 (interpolated) | pass | 0.298 (unverified) | -0.01 |
| 85 | `cfg_ac39` | timeframe=1h, mean_type=ema, mean_lookback=70, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 16/110/0 | 126 | 62.2% | 10.2% | 1.03 | -8.2% | 254 | 1.65 | 17.7% | 58.6 | 7/7 | 1.00 | 0.56 | 0.47 | 5 | 39.0% | 0.32 | 0.56 | 60.9% | 59.2% | 47.9% | 55.8%/43.8% | 24.0 (interpolated) | pass | 0.497 (unverified) | 0.17 |
| 86 | `cfg_6865` | timeframe=1h, mean_type=sma, mean_lookback=110, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=2.5 | 26/71/43 | 140 | 47.4% | 8.1% | 0.78 | -11.1% | 546 | 1.39 | 16.3% | 65.3 | 10/10 | 1.00 | 0.70 | 0.08 | 4 | 4.3% | 0.81 | 0.79 | 45.6% | 43.2% | 44.3% | 45.8%/28.4% | 16.7 (interpolated) | pass | 0.282 (unverified) | 0.06 |
| 87 | `cfg_e639` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=2.5 | 27/69/44 | 140 | 44.3% | 7.6% | 0.78 | -15.9% | 395 | 1.37 | 15.7% | 64.5 | 10/10 | 1.00 | 0.65 | 0.13 | 4 | 17.2% | 0.53 | 0.76 | 42.0% | 39.9% | 32.0% | 41.3%/24.6% | 16.9 (interpolated) | pass | 0.302 (unverified) | 0.10 |
| 88 | `cfg_fde2` | timeframe=1h, mean_type=sma, mean_lookback=110, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 14/95/49 | 158 | 41.6% | 7.2% | 0.79 | -9.1% | 225 | 1.39 | 13.4% | 73.5 | 11/11 | 1.00 | 0.64 | 0.16 | 4 | 24.1% | 0.34 | 0.84 | 37.6% | 35.4% | 33.4% | 35.7%/23.1% | 13.8 (interpolated) | pass | 0.284 (unverified) | -0.35 |
| 89 | `cfg_5527` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=2.0 | 16/92/73 | 181 | 55.7% | 9.3% | 0.82 | -14.8% | 254 | 1.34 | 20.6% | 84.3 | 9/9 | 1.00 | 0.62 | 0.21 | 4 | 24.0% | 0.57 | 0.66 | 54.2% | 50.3% | 40.3% | 45.5%/32.8% | 15.6 (interpolated) | pass | 0.317 (unverified) | 0.67 |
| 90 | `cfg_b509` | timeframe=1h, mean_type=sma, mean_lookback=110, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=2.0 | 28/69/65 | 162 | 50.2% | 8.5% | 0.77 | -18.1% | 367 | 1.35 | 17.6% | 74.8 | 10/10 | 1.00 | 0.65 | 0.12 | 4 | 5.5% | 0.77 | 0.76 | 47.9% | 46.2% | 30.0% | 42.1%/28.1% | 15.6 (interpolated) | pass | 0.274 (unverified) | 0.53 |
| 91 | `cfg_109f` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 30/84/0 | 114 | 50.3% | 8.5% | 0.93 | -9.3% | 421 | 1.63 | 15.5% | 53.0 | 8/8 | 1.00 | 0.76 | 0.17 | 4 | 26.5% | 0.39 | 0.58 | 48.2% | 47.1% | 33.8% | 43.4%/30.4% | 21.8 (interpolated) | pass | 0.409 (unverified) | -0.06 |
| 92 | `cfg_39ad` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 18/96/0 | 114 | 42.4% | 7.3% | 0.76 | -19.7% | 280 | 1.41 | 16.1% | 53.7 | 8/8 | 1.00 | 0.58 | 0.18 | 4 | 17.5% | 0.59 | 0.79 | 41.6% | 39.7% | 53.9% | 36.6%/23.8% | 19.3 (interpolated) | pass | 0.270 (unverified) | 0.74 |
| 93 | `cfg_3af4` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=2.0 | 16/94/81 | 191 | 55.2% | 9.2% | 0.80 | -13.2% | 560 | 1.35 | 21.1% | 87.2 | 9/9 | 1.00 | 0.58 | 0.23 | 4 | 16.7% | 0.57 | 0.63 | 52.8% | 50.5% | 21.7% | 48.3%/31.1% | 14.5 (interpolated) | pass | 0.301 (unverified) | 0.09 |
| 94 | `cfg_044e` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-3.0, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 15/108/0 | 123 | 60.1% | 9.9% | 0.86 | -18.7% | 225 | 1.56 | 17.5% | 56.9 | 7/7 | 1.00 | 0.68 | 0.19 | 5 | 25.3% | 0.58 | 0.59 | 59.3% | 56.7% | 36.0% | 53.4%/40.3% | 24.0 (interpolated) | pass | 0.353 (unverified) | 0.08 |
| 95 | `cfg_fda5` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 27/83/92 | 202 | 41.7% | 7.2% | 0.75 | -15.1% | 412 | 1.31 | 15.2% | 92.6 | 10/10 | 1.00 | 0.58 | 0.17 | 4 | 23.8% | 0.39 | 0.84 | 39.2% | 36.5% | 31.0% | 37.2%/22.0% | 11.4 (interpolated) | pass | 0.266 (unverified) | -0.41 |
| 96 | `cfg_940a` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 36/79/0 | 115 | 41.8% | 7.2% | 0.80 | -16.8% | 280 | 1.45 | 15.1% | 54.1 | 9/9 | 1.00 | 0.54 | 0.26 | 4 | 22.3% | 0.43 | 0.63 | 40.8% | 40.2% | 53.2% | 35.2%/24.6% | 19.2 (interpolated) | pass | 0.302 (unverified) | 0.55 |
| 97 | `cfg_dc4a` | timeframe=1h, mean_type=ema, mean_lookback=90, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 10/113/60 | 183 | 50.1% | 8.5% | 0.88 | -10.9% | 326 | 1.38 | 15.5% | 83.5 | 10/10 | 0.90 | 0.60 | 0.28 | 5 | 30.2% | 0.36 | 0.66 | 48.4% | 46.0% | 40.4% | 42.9%/27.9% | 14.0 (interpolated) | pass | 0.360 (unverified) | -0.15 |
| 98 | `cfg_838a` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=2.0 | 46/64/82 | 192 | 51.3% | 8.6% | 0.78 | -13.6% | 561 | 1.33 | 19.6% | 87.9 | 10/10 | 0.90 | 0.53 | 0.26 | 4 | 15.8% | 0.56 | 0.68 | 48.2% | 45.0% | 22.1% | 43.7%/27.5% | 13.9 (interpolated) | pass | 0.285 (unverified) | 0.22 |
| 99 | `cfg_0daf` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=18, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 16/66/38 | 120 | 27.6% | 5.0% | 0.82 | -8.0% | 258 | 1.49 | 6.8% | 55.0 | 8/8 | 0.88 | 0.57 | 0.26 | 4 | 16.6% | 0.40 | 0.59 | 26.9% | 25.4% | 24.6% | 25.6%/18.7% | 12.9 (interpolated) | pass | 0.309 (unverified) | 0.32 |
| 100 | `cfg_3272` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 62/62/0 | 124 | 61.3% | 10.0% | 1.04 | -10.8% | 203 | 1.70 | 14.1% | 58.3 | 8/8 | 1.00 | 0.50 | 0.54 | 5 | 24.0% | 0.54 | 0.45 | 59.1% | 57.1% | 34.3% | 48.7%/38.7% | 23.4 (interpolated) | pass | 0.508 (unverified) | 0.28 |
| 101 | `cfg_a510` | timeframe=1h, mean_type=ema, mean_lookback=90, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 0/87/26 | 113 | 33.1% | 5.9% | 0.85 | -6.8% | 247 | 1.51 | 6.9% | 51.8 | 9/9 | 1.00 | 0.65 | 0.20 | 5 | 9.3% | 0.69 | 0.89 | 31.8% | 30.2% | 34.3% | 31.6%/23.6% | 15.8 (interpolated) | pass | 0.327 (unverified) | 0.15 |
| 102 | `cfg_7d1d` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 63/65/91 | 219 | 55.5% | 9.2% | 0.90 | -11.3% | 215 | 1.39 | 15.2% | 100.9 | 9/9 | 1.00 | 0.52 | 0.38 | 5 | 31.4% | 0.43 | 0.57 | 53.9% | 52.3% | 15.5% | 44.2%/31.9% | 13.0 (interpolated) | pass | 0.387 (unverified) | -0.21 |
| 103 | `cfg_e524` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 2/84/20 | 106 | 28.4% | 5.1% | 0.79 | -8.5% | 313 | 1.51 | 6.5% | 48.2 | 8/8 | 0.88 | 0.62 | 0.16 | 4 | 13.7% | 0.48 | 0.95 | 27.4% | 25.2% | 26.5% | 24.3%/12.3% | 14.8 (interpolated) | pass | 0.296 (unverified) | 0.81 |
| 104 | `cfg_47e2` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 40/74/49 | 163 | 35.1% | 6.2% | 0.75 | -10.3% | 276 | 1.32 | 13.0% | 75.3 | 10/10 | 1.00 | 0.54 | 0.22 | 5 | 22.5% | 0.33 | 0.75 | 33.4% | 31.1% | 20.6% | 32.9%/22.0% | 12.2 (interpolated) | pass | 0.265 (unverified) | -0.40 |
| 105 | `cfg_8dca` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 11/86/41 | 138 | 27.8% | 5.0% | 0.78 | -4.6% | 228 | 1.43 | 7.8% | 63.1 | 9/9 | 1.00 | 0.64 | 0.14 | 3 | 5.7% | 0.76 | 0.84 | 26.7% | 25.2% | 26.3% | 29.0%/20.9% | 11.6 (interpolated) | pass | 0.269 (unverified) | 0.74 |
| 106 | `cfg_98d4` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 6/80/20 | 106 | 28.6% | 5.2% | 0.79 | -8.4% | 313 | 1.52 | 6.5% | 48.1 | 9/9 | 0.89 | 0.64 | 0.15 | 4 | 13.5% | 0.49 | 0.96 | 27.0% | 25.5% | 26.6% | 26.0%/15.0% | 14.7 (interpolated) | pass | 0.299 (unverified) | 0.81 |
| 107 | `cfg_ae3d` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 21/94/0 | 115 | 50.9% | 8.6% | 0.89 | -12.3% | 421 | 1.65 | 16.3% | 52.9 | 7/7 | 1.00 | 0.71 | 0.19 | 3 | 14.0% | 0.61 | 0.59 | 49.2% | 47.8% | 35.1% | 44.9%/32.5% | 22.6 (interpolated) | pass | 0.374 (unverified) | 0.33 |
| 108 | `cfg_4f65` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 35/88/0 | 123 | 53.5% | 9.0% | 0.80 | -18.6% | 225 | 1.52 | 16.5% | 56.9 | 8/8 | 1.00 | 0.61 | 0.20 | 5 | 23.8% | 0.55 | 0.68 | 51.1% | 49.7% | 20.0% | 48.2%/35.0% | 21.4 (interpolated) | pass | 0.308 (unverified) | -0.01 |
| 109 | `cfg_6b6d` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=20, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 4/67/30 | 101 | 43.8% | 7.5% | 0.82 | -15.0% | 566 | 1.54 | 12.8% | 47.4 | 7/7 | 0.86 | 0.45 | 0.37 | 4 | 25.4% | 0.42 | 0.61 | 40.0% | 38.9% | 40.5% | 37.1%/22.0% | 21.8 (interpolated) | pass | 0.312 (unverified) | 0.19 |
| 110 | `cfg_a3b1` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=12, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=1.5 | 16/85/110 | 211 | 57.5% | 9.5% | 0.76 | -18.3% | 415 | 1.30 | 21.5% | 98.8 | 8/8 | 1.00 | 0.54 | 0.23 | 4 | 13.6% | 0.65 | 0.75 | 55.6% | 53.0% | 24.9% | 45.3%/27.8% | 13.8 (interpolated) | pass | 0.273 (unverified) | 0.54 |
| 111 | `cfg_b4e3` | timeframe=1h, mean_type=sma, mean_lookback=110, std_lookback=12, entry_z=-3.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 5/104/49 | 158 | 39.2% | 6.8% | 0.75 | -9.1% | 225 | 1.37 | 13.7% | 73.5 | 10/10 | 1.00 | 0.57 | 0.18 | 4 | 22.1% | 0.36 | 0.88 | 36.2% | 34.3% | 30.3% | 34.5%/24.3% | 13.4 (interpolated) | pass | 0.256 (unverified) | -0.36 |
| 112 | `cfg_dd11` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 2/70/38 | 110 | 30.0% | 5.4% | 0.77 | -7.2% | 372 | 1.50 | 6.2% | 50.7 | 8/8 | 1.00 | 0.51 | 0.26 | 3 | 8.1% | 0.69 | 0.97 | 28.6% | 27.1% | 30.6% | 27.7%/18.3% | 14.7 (interpolated) | pass | 0.256 (unverified) | 0.34 |
| 113 | `cfg_1001` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 22/79/29 | 130 | 28.9% | 5.2% | 0.84 | -7.2% | 408 | 1.47 | 7.4% | 58.8 | 9/9 | 1.00 | 0.61 | 0.22 | 4 | 17.2% | 0.37 | 0.64 | 27.6% | 25.4% | 35.1% | 28.3%/18.3% | 12.3 (interpolated) | pass | 0.324 (unverified) | 0.30 |
| 114 | `cfg_0b25` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 36/83/0 | 119 | 57.9% | 9.6% | 0.94 | -12.4% | 225 | 1.61 | 15.7% | 54.7 | 8/8 | 1.00 | 0.74 | 0.20 | 5 | 27.5% | 0.45 | 0.60 | 55.5% | 54.3% | 39.2% | 55.2%/40.8% | 23.4 (interpolated) | pass | 0.415 (unverified) | -0.06 |
| 115 | `cfg_a30d` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 38/78/0 | 116 | 52.3% | 8.8% | 0.94 | -10.4% | 540 | 1.70 | 15.1% | 53.4 | 8/8 | 1.00 | 0.75 | 0.19 | 3 | 18.2% | 0.52 | 0.57 | 50.8% | 48.6% | 38.5% | 46.6%/37.9% | 22.7 (interpolated) | pass | 0.413 (unverified) | 0.33 |
| 116 | `cfg_c976` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 14/63/24 | 101 | 35.6% | 6.3% | 0.75 | -15.0% | 276 | 1.48 | 9.0% | 45.8 | 10/10 | 0.90 | 0.48 | 0.27 | 4 | 21.6% | 0.39 | 0.87 | 34.4% | 33.9% | 26.4% | 32.9%/20.4% | 18.7 (interpolated) | pass | 0.267 (unverified) | -0.03 |
| 117 | `cfg_e5b5` | timeframe=1h, mean_type=ema, mean_lookback=90, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 36/77/0 | 113 | 48.1% | 8.2% | 0.81 | -11.6% | 191 | 1.53 | 15.2% | 52.8 | 8/8 | 0.88 | 0.54 | 0.27 | 5 | 27.1% | 0.38 | 0.67 | 47.3% | 46.3% | 39.1% | 43.2%/27.6% | 21.3 (interpolated) | pass | 0.303 (unverified) | -0.11 |
| 118 | `cfg_902f` | timeframe=1h, mean_type=ema, mean_lookback=90, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 27/96/60 | 183 | 49.6% | 8.4% | 0.87 | -10.9% | 326 | 1.39 | 15.3% | 83.5 | 11/11 | 0.91 | 0.54 | 0.33 | 5 | 30.4% | 0.35 | 0.66 | 46.5% | 45.0% | 32.9% | 41.0%/23.9% | 13.9 (interpolated) | pass | 0.354 (unverified) | -0.14 |
| 119 | `cfg_27f9` | timeframe=1h, mean_type=ema, mean_lookback=70, std_lookback=12, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 14/73/39 | 126 | 54.9% | 9.2% | 0.87 | -15.0% | 428 | 1.55 | 15.2% | 59.0 | 8/8 | 1.00 | 0.79 | 0.08 | 4 | 32.6% | 0.41 | 0.57 | 53.3% | 51.0% | 38.5% | 51.3%/35.5% | 21.7 (interpolated) | pass | 0.353 (unverified) | -0.10 |
| 120 | `cfg_b19a` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 28/88/90 | 206 | 48.3% | 8.2% | 0.90 | -9.7% | 286 | 1.34 | 15.5% | 95.4 | 9/9 | 1.00 | 0.65 | 0.24 | 5 | 32.7% | 0.32 | 0.66 | 45.6% | 43.7% | 31.6% | 37.4%/25.7% | 12.2 (interpolated) | pass | 0.375 (unverified) | -0.23 |
| 121 | `cfg_a5fd` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 30/63/23 | 116 | 30.9% | 5.5% | 0.76 | -8.4% | 252 | 1.43 | 9.7% | 53.5 | 9/9 | 1.00 | 0.54 | 0.22 | 4 | 12.8% | 0.53 | 0.78 | 29.9% | 29.1% | 19.7% | 27.4%/17.2% | 14.8 (interpolated) | pass | 0.263 (unverified) | -0.34 |
| 122 | `cfg_5251` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 22/59/57 | 138 | 35.1% | 6.2% | 0.77 | -17.3% | 414 | 1.41 | 10.5% | 62.7 | 10/10 | 1.00 | 0.55 | 0.21 | 4 | 13.6% | 0.51 | 0.80 | 33.1% | 31.6% | 39.7% | 33.3%/22.5% | 13.6 (interpolated) | pass | 0.289 (unverified) | 0.15 |
| 123 | `cfg_683c` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 27/93/54 | 174 | 43.9% | 7.6% | 0.83 | -10.8% | 205 | 1.39 | 14.6% | 80.4 | 10/10 | 1.00 | 0.64 | 0.19 | 5 | 19.0% | 0.54 | 0.63 | 41.6% | 40.3% | 25.7% | 36.4%/23.9% | 13.5 (interpolated) | pass | 0.331 (unverified) | -0.08 |
| 124 | `cfg_30f0` | timeframe=1h, mean_type=ema, mean_lookback=90, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 13/103/0 | 116 | 43.7% | 7.5% | 0.78 | -18.1% | 276 | 1.46 | 16.5% | 53.4 | 8/8 | 1.00 | 0.58 | 0.20 | 3 | 13.4% | 0.69 | 0.85 | 42.2% | 40.2% | 34.7% | 40.2%/27.9% | 19.3 (interpolated) | pass | 0.276 (unverified) | 0.11 |
| 125 | `cfg_13a7` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 12/93/0 | 105 | 50.7% | 8.6% | 0.94 | -9.8% | 216 | 1.64 | 14.8% | 49.0 | 8/8 | 1.00 | 0.70 | 0.24 | 3 | 20.1% | 0.53 | 0.68 | 49.5% | 48.4% | 46.7% | 42.1%/29.7% | 24.1 (interpolated) | pass | 0.412 (unverified) | 0.10 |
| 126 | `cfg_5910` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 17/64/21 | 102 | 33.5% | 6.0% | 0.78 | -8.4% | 212 | 1.54 | 8.8% | 47.2 | 11/11 | 1.00 | 0.53 | 0.25 | 5 | 17.7% | 0.47 | 0.65 | 32.1% | 30.9% | 27.4% | 30.3%/22.1% | 17.7 (interpolated) | pass | 0.283 (unverified) | 0.40 |
| 127 | `cfg_9195` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=2.0 | 39/73/71 | 183 | 47.1% | 8.0% | 0.77 | -14.1% | 394 | 1.31 | 19.5% | 83.9 | 9/9 | 1.00 | 0.65 | 0.12 | 4 | 15.0% | 0.58 | 0.72 | 44.8% | 42.4% | 47.0% | 41.9%/26.2% | 13.5 (interpolated) | pass | 0.274 (unverified) | 0.14 |
| 128 | `cfg_50ab` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 26/91/92 | 209 | 45.1% | 7.7% | 0.89 | -12.7% | 499 | 1.36 | 16.0% | 95.9 | 9/9 | 1.00 | 0.70 | 0.19 | 3 | 22.5% | 0.50 | 0.63 | 42.3% | 40.1% | 10.5% | 35.9%/22.0% | 11.3 (interpolated) | pass | 0.371 (unverified) | -0.06 |
| 129 | `cfg_efc3` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 19/79/40 | 138 | 28.5% | 5.1% | 0.79 | -4.9% | 228 | 1.44 | 7.6% | 63.2 | 8/8 | 1.00 | 0.52 | 0.27 | 3 | 5.5% | 0.77 | 0.82 | 27.0% | 25.5% | 21.0% | 28.7%/21.3% | 11.6 (interpolated) | pass | 0.278 (unverified) | 0.75 |
| 130 | `cfg_cd5b` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=10, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 10/112/88 | 210 | 51.8% | 8.7% | 0.89 | -9.5% | 164 | 1.38 | 16.6% | 96.7 | 8/8 | 1.00 | 0.54 | 0.35 | 5 | 25.4% | 0.46 | 0.65 | 48.9% | 47.5% | 18.4% | 40.6%/25.3% | 12.9 (interpolated) | pass | 0.369 (unverified) | -0.25 |
| 131 | `cfg_a7c9` | timeframe=1h, mean_type=ema, mean_lookback=70, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 37/51/38 | 126 | 56.2% | 9.3% | 0.91 | -15.1% | 539 | 1.56 | 13.8% | 59.0 | 9/9 | 1.00 | 0.72 | 0.19 | 4 | 32.7% | 0.37 | 0.54 | 53.3% | 52.2% | 33.5% | 49.2%/34.8% | 21.6 (interpolated) | pass | 0.391 (unverified) | -0.08 |
| 132 | `cfg_586e` | timeframe=1h, mean_type=ema, mean_lookback=70, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 3/93/30 | 126 | 32.3% | 5.8% | 0.77 | -12.1% | 428 | 1.49 | 7.6% | 57.5 | 8/8 | 0.88 | 0.50 | 0.27 | 5 | 17.5% | 0.46 | 0.78 | 30.7% | 29.8% | 28.5% | 31.6%/21.9% | 14.3 (interpolated) | pass | 0.268 (unverified) | 0.04 |
| 133 | `cfg_722b` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 28/77/0 | 105 | 46.4% | 7.9% | 0.91 | -6.9% | 367 | 1.63 | 14.2% | 48.6 | 9/9 | 1.00 | 0.71 | 0.20 | 3 | 16.1% | 0.58 | 0.69 | 45.6% | 44.0% | 46.9% | 39.5%/30.6% | 22.9 (interpolated) | pass | 0.386 (unverified) | 0.03 |
| 134 | `cfg_85d8` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-3.0, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 5/97/27 | 129 | 38.8% | 6.8% | 0.91 | -9.0% | 259 | 1.58 | 7.8% | 58.3 | 8/8 | 1.00 | 0.49 | 0.42 | 4 | 26.3% | 0.32 | 0.62 | 38.0% | 35.6% | 33.4% | 31.8%/22.0% | 15.8 (interpolated) | pass | 0.382 (unverified) | 0.05 |
| 135 | `cfg_b259` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 30/82/0 | 112 | 39.6% | 6.9% | 0.75 | -10.0% | 504 | 1.51 | 15.0% | 51.1 | 9/9 | 1.00 | 0.48 | 0.27 | 4 | 19.9% | 0.44 | 0.75 | 38.2% | 37.3% | 41.8% | 37.2%/20.4% | 18.4 (interpolated) | pass | 0.274 (unverified) | -0.29 |
| 136 | `cfg_aa96` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-3.0, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 16/103/0 | 119 | 49.1% | 8.3% | 0.81 | -16.6% | 247 | 1.51 | 16.9% | 54.4 | 7/7 | 1.00 | 0.71 | 0.10 | 4 | 20.3% | 0.53 | 0.66 | 48.1% | 47.0% | 33.9% | 45.6%/33.9% | 21.3 (interpolated) | pass | 0.301 (unverified) | -0.16 |
| 137 | `cfg_2bf0` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 24/58/21 | 103 | 32.3% | 5.8% | 0.78 | -8.6% | 237 | 1.53 | 8.5% | 47.7 | 10/10 | 1.00 | 0.51 | 0.27 | 5 | 19.7% | 0.39 | 0.59 | 30.7% | 29.4% | 27.2% | 30.9%/22.4% | 16.9 (interpolated) | pass | 0.283 (unverified) | 0.29 |
| 138 | `cfg_f068` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 9/93/27 | 129 | 38.3% | 6.7% | 0.91 | -9.0% | 259 | 1.58 | 7.7% | 58.4 | 9/9 | 1.00 | 0.62 | 0.30 | 4 | 25.8% | 0.33 | 0.62 | 36.0% | 34.7% | 32.9% | 32.3%/21.7% | 15.6 (interpolated) | pass | 0.386 (unverified) | 0.04 |
| 139 | `cfg_9112` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=10, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 50/68/90 | 208 | 43.3% | 7.5% | 0.84 | -9.3% | 314 | 1.32 | 14.8% | 95.6 | 8/8 | 1.00 | 0.53 | 0.31 | 5 | 26.9% | 0.38 | 0.65 | 40.3% | 37.2% | 28.5% | 35.1%/25.2% | 11.3 (interpolated) | pass | 0.333 (unverified) | -0.30 |
| 140 | `cfg_be6d` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-3.0, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 10/98/0 | 108 | 45.9% | 7.9% | 0.83 | -11.2% | 194 | 1.55 | 15.3% | 49.9 | 8/8 | 1.00 | 0.59 | 0.23 | 5 | 30.5% | 0.33 | 0.65 | 44.4% | 43.7% | 37.9% | 39.6%/26.8% | 21.3 (interpolated) | pass | 0.315 (unverified) | -0.16 |
| 141 | `cfg_0579` | timeframe=1h, mean_type=ema, mean_lookback=90, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 30/86/0 | 116 | 39.5% | 6.9% | 0.76 | -17.1% | 276 | 1.44 | 15.7% | 53.0 | 9/9 | 1.00 | 0.54 | 0.21 | 3 | 11.5% | 0.70 | 0.84 | 38.5% | 36.9% | 33.8% | 36.7%/26.0% | 17.9 (interpolated) | pass | 0.265 (unverified) | 0.09 |
| 142 | `cfg_34a2` | timeframe=1h, mean_type=ema, mean_lookback=70, std_lookback=15, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 3/98/14 | 115 | 33.5% | 5.9% | 0.83 | -11.8% | 428 | 1.61 | 7.4% | 52.5 | 8/8 | 0.88 | 0.67 | 0.16 | 5 | 18.1% | 0.46 | 0.75 | 31.4% | 29.8% | 26.3% | 30.6%/22.0% | 15.5 (interpolated) | pass | 0.316 (unverified) | -0.15 |
| 143 | `cfg_2e75` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 21/81/27 | 129 | 36.4% | 6.4% | 0.82 | -9.9% | 173 | 1.42 | 11.1% | 58.6 | 10/10 | 1.00 | 0.58 | 0.24 | 4 | 20.8% | 0.39 | 0.79 | 35.4% | 33.6% | 13.4% | 33.6%/25.1% | 15.1 (interpolated) | pass | 0.309 (unverified) | -0.12 |
| 144 | `cfg_a7f9` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=18, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 7/116/56 | 179 | 45.9% | 7.9% | 0.85 | -9.4% | 599 | 1.42 | 15.4% | 82.1 | 10/10 | 1.00 | 0.44 | 0.41 | 4 | 13.8% | 0.66 | 0.67 | 43.6% | 41.8% | 37.3% | 34.8%/22.2% | 13.7 (interpolated) | pass | 0.337 (unverified) | -0.29 |
| 145 | `cfg_e86c` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=10, entry_z=-3.0, exit_z=-1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 49/69/0 | 118 | 36.4% | 6.4% | 0.76 | -9.1% | 251 | 1.47 | 14.6% | 54.6 | 7/7 | 1.00 | 0.70 | 0.05 | 4 | 18.9% | 0.41 | 0.62 | 35.0% | 33.0% | 22.1% | 30.5%/20.4% | 16.2 (interpolated) | pass | 0.267 (unverified) | -0.08 |
| 146 | `cfg_b5fd` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.5 | 32/90/29 | 151 | 51.3% | 8.6% | 0.97 | -10.1% | 394 | 1.56 | 13.3% | 70.3 | 10/10 | 1.00 | 0.61 | 0.37 | 4 | 27.1% | 0.47 | 0.59 | 50.3% | 48.9% | 40.3% | 40.7%/29.8% | 17.5 (interpolated) | pass | 0.444 (unverified) | 0.09 |
| 147 | `cfg_bd63` | timeframe=1h, mean_type=ema, mean_lookback=70, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 39/87/0 | 126 | 53.6% | 9.0% | 0.94 | -8.9% | 254 | 1.59 | 16.7% | 58.5 | 8/8 | 1.00 | 0.48 | 0.46 | 5 | 33.8% | 0.32 | 0.59 | 52.9% | 49.9% | 40.3% | 46.4%/33.8% | 21.8 (interpolated) | pass | 0.417 (unverified) | 0.17 |
| 148 | `cfg_45b4` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 36/52/37 | 125 | 32.7% | 5.8% | 0.76 | -10.9% | 416 | 1.42 | 9.6% | 57.1 | 10/10 | 1.00 | 0.45 | 0.31 | 3 | 11.3% | 0.65 | 0.60 | 32.0% | 31.0% | 30.8% | 29.4%/22.0% | 15.3 (interpolated) | pass | 0.270 (unverified) | 0.80 |
| 149 | `cfg_87fe` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=18, entry_z=-3.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 4/110/0 | 114 | 53.5% | 9.0% | 0.99 | -11.5% | 243 | 1.62 | 11.6% | 53.6 | 8/8 | 0.88 | 0.37 | 0.62 | 4 | 21.0% | 0.62 | 0.55 | 52.2% | 50.4% | 34.2% | 47.3%/36.2% | 23.3 (interpolated) | pass | 0.461 (unverified) | 0.62 |
| 150 | `cfg_8247` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=10, entry_z=-3.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 5/112/92 | 209 | 38.0% | 6.7% | 0.77 | -12.6% | 521 | 1.30 | 16.3% | 95.8 | 8/8 | 1.00 | 0.58 | 0.19 | 4 | 22.9% | 0.40 | 0.71 | 36.0% | 33.6% | 12.0% | 33.2%/19.7% | 10.1 (interpolated) | pass | 0.271 (unverified) | 0.02 |
| 151 | `cfg_f903` | timeframe=1h, mean_type=ema, mean_lookback=90, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=2.0 | 32/67/65 | 164 | 49.6% | 8.4% | 0.79 | -14.1% | 372 | 1.35 | 18.0% | 74.9 | 10/10 | 0.90 | 0.47 | 0.31 | 4 | 15.8% | 0.63 | 0.73 | 48.2% | 47.3% | 12.9% | 38.4%/15.2% | 16.0 (interpolated) | pass | 0.285 (unverified) | 0.40 |
| 152 | `cfg_4bd1` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=2.5 | 23/71/39 | 133 | 48.2% | 8.2% | 0.86 | -11.1% | 234 | 1.42 | 15.6% | 60.6 | 10/10 | 1.00 | 0.51 | 0.34 | 4 | 25.4% | 0.41 | 0.72 | 45.4% | 44.1% | 40.0% | 40.2%/27.3% | 18.3 (interpolated) | pass | 0.343 (unverified) | 0.12 |
| 153 | `cfg_8dc6` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=1.0, max_holding_bars=12, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 18/76/44 | 138 | 49.0% | 8.3% | 0.81 | -14.3% | 395 | 1.42 | 16.7% | 62.5 | 8/8 | 1.00 | 0.55 | 0.26 | 4 | 11.8% | 0.65 | 0.70 | 47.1% | 45.9% | 69.3% | 43.9%/32.1% | 18.3 (interpolated) | pass | 0.308 (unverified) | 0.10 |
| 154 | `cfg_2dad` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 26/109/0 | 135 | 40.4% | 7.0% | 0.80 | -12.1% | 326 | 1.50 | 13.1% | 62.8 | 10/10 | 1.00 | 0.70 | 0.10 | 4 | 22.7% | 0.44 | 0.64 | 39.3% | 37.9% | 63.9% | 35.8%/23.8% | 16.4 (interpolated) | pass | 0.303 (unverified) | -0.00 |
| 155 | `cfg_3326` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 32/89/0 | 121 | 39.6% | 6.9% | 0.77 | -13.6% | 662 | 1.51 | 16.4% | 55.5 | 9/9 | 0.89 | 0.59 | 0.17 | 4 | 7.9% | 0.74 | 0.63 | 37.9% | 36.8% | 26.6% | 35.4%/24.2% | 17.3 (interpolated) | pass | 0.276 (unverified) | -0.17 |
| 156 | `cfg_a9c2` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=20, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 4/109/58 | 171 | 48.3% | 8.2% | 0.83 | -10.8% | 309 | 1.37 | 14.7% | 79.5 | 9/9 | 1.00 | 0.37 | 0.46 | 5 | 21.4% | 0.55 | 0.70 | 45.3% | 43.8% | 27.4% | 38.5%/25.5% | 14.4 (interpolated) | pass | 0.323 (unverified) | 0.17 |
| 157 | `cfg_b6f4` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=15, entry_z=-3.0, exit_z=1.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=2.5 | 9/85/39 | 133 | 51.4% | 8.7% | 0.87 | -10.8% | 278 | 1.43 | 16.3% | 61.4 | 9/9 | 1.00 | 0.61 | 0.25 | 4 | 24.3% | 0.46 | 0.78 | 50.6% | 48.6% | 43.0% | 40.4%/28.9% | 19.2 (interpolated) | pass | 0.354 (unverified) | 0.12 |
| 158 | `cfg_25ec` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 24/102/0 | 126 | 34.6% | 6.1% | 0.75 | -15.6% | 570 | 1.49 | 12.3% | 58.8 | 9/9 | 0.89 | 0.64 | 0.11 | 4 | 16.4% | 0.48 | 0.62 | 33.3% | 31.6% | 46.2% | 29.6%/20.1% | 15.0 (interpolated) | pass | 0.255 (unverified) | -0.19 |
| 159 | `cfg_510b` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=12, entry_confirmation=none, stop_atr_multiple=none | 24/84/0 | 108 | 41.8% | 7.2% | 0.79 | -11.3% | 359 | 1.51 | 14.6% | 49.5 | 9/9 | 0.89 | 0.54 | 0.24 | 5 | 26.3% | 0.30 | 0.69 | 40.5% | 39.4% | 27.7% | 34.7%/21.9% | 20.8 (interpolated) | pass | 0.285 (unverified) | -0.22 |
| 160 | `cfg_4220` | timeframe=1h, mean_type=ema, mean_lookback=110, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 36/63/20 | 119 | 31.3% | 5.6% | 0.77 | -10.8% | 197 | 1.47 | 10.1% | 54.8 | 9/9 | 1.00 | 0.39 | 0.38 | 4 | 16.0% | 0.49 | 0.65 | 30.1% | 29.1% | 9.3% | 27.6%/19.3% | 14.6 (interpolated) | pass | 0.273 (unverified) | 0.31 |
| 161 | `cfg_d52b` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 32/95/0 | 127 | 41.4% | 7.2% | 0.85 | -10.4% | 394 | 1.54 | 12.1% | 59.0 | 9/9 | 1.00 | 0.61 | 0.24 | 4 | 19.6% | 0.43 | 0.70 | 40.6% | 38.5% | 43.1% | 35.2%/26.0% | 17.0 (interpolated) | pass | 0.341 (unverified) | 0.16 |
| 162 | `cfg_1fab` | timeframe=1h, mean_type=ema, mean_lookback=90, std_lookback=15, entry_z=-3.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 9/114/0 | 123 | 42.9% | 7.4% | 0.82 | -10.6% | 113 | 1.52 | 12.4% | 56.5 | 9/9 | 0.78 | 0.51 | 0.31 | 4 | 24.4% | 0.34 | 0.65 | 41.5% | 39.7% | 51.2% | 37.2%/24.7% | 17.6 (interpolated) | pass | 0.313 (unverified) | 0.16 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | -2.1% / -0.31 / 24 | 10.9% / 2.05 / 19 | 11.0% / 1.28 / 14 | 15.8% / 2.01 / 18 | 15.3% / 1.79 / 26 |
| 2 | 2.6% / 0.50 / 22 | 2.4% / 0.47 / 19 | 19.1% / 1.93 / 13 | 8.4% / 1.06 / 21 | 9.1% / 1.07 / 27 |
| 3 | 5.5% / 0.95 / 23 | 10.9% / 1.73 / 18 | 7.7% / 0.89 / 10 | 1.2% / 0.21 / 19 | 12.8% / 1.28 / 32 |
| 4 | 1.3% / 0.26 / 22 | 2.9% / 0.55 / 19 | 17.9% / 1.88 / 13 | 9.1% / 1.13 / 21 | 9.5% / 1.11 / 27 |
| 5 | 4.8% / 0.84 / 23 | 11.4% / 1.77 / 18 | 7.3% / 0.87 / 10 | 1.9% / 0.32 / 19 | 10.7% / 1.12 / 32 |
| 6 | -6.4% / -0.99 / 21 | 12.7% / 1.82 / 18 | 22.1% / 2.03 / 16 | 15.4% / 1.82 / 18 | 7.2% / 0.70 / 31 |
| 7 | 0.1% / 0.04 / 32 | 2.8% / 0.65 / 21 | 7.4% / 1.17 / 18 | 14.3% / 2.23 / 21 | 5.5% / 0.86 / 30 |
| 8 | 0.1% / 0.04 / 32 | 2.8% / 0.65 / 21 | 6.6% / 1.12 / 18 | 14.3% / 2.22 / 21 | 5.5% / 0.86 / 30 |
| 9 | 6.0% / 1.16 / 28 | -0.2% / -0.03 / 23 | 17.3% / 1.85 / 17 | 7.3% / 1.15 / 24 | 10.5% / 1.35 / 32 |
| 10 | 1.9% / 0.33 / 23 | 0.9% / 0.16 / 21 | 26.4% / 2.22 / 20 | 11.5% / 1.11 / 25 | 19.0% / 1.60 / 29 |
| 11 | 7.7% / 1.07 / 22 | 6.3% / 1.05 / 18 | 32.1% / 2.03 / 16 | 4.5% / 0.48 / 25 | 2.4% / 0.25 / 34 |
| 12 | 4.2% / 0.63 / 26 | 7.4% / 1.26 / 21 | 8.2% / 1.12 / 16 | 12.9% / 1.73 / 17 | 4.1% / 0.56 / 26 |
| 13 | -1.9% / -0.29 / 24 | 10.4% / 1.95 / 19 | 10.8% / 1.27 / 14 | 13.9% / 1.77 / 18 | 11.9% / 1.26 / 26 |
| 14 | 2.6% / 0.41 / 27 | 10.1% / 2.01 / 19 | 15.3% / 1.56 / 17 | 9.8% / 1.15 / 25 | 6.9% / 0.79 / 29 |
| 15 | 3.8% / 0.59 / 27 | 4.3% / 0.85 / 22 | 19.7% / 1.77 / 18 | 5.5% / 0.73 / 21 | 7.2% / 0.87 / 27 |
| 16 | 3.5% / 0.73 / 25 | -1.6% / -0.35 / 22 | 17.7% / 1.94 / 14 | 7.1% / 1.06 / 21 | 6.6% / 0.81 / 31 |
| 17 | 8.3% / 1.32 / 23 | 3.9% / 0.58 / 21 | 25.5% / 1.94 / 20 | 9.1% / 0.95 / 20 | 2.7% / 0.28 / 32 |
| 18 | -3.5% / -0.55 / 33 | 4.4% / 1.19 / 14 | 4.2% / 0.59 / 16 | 10.0% / 1.97 / 14 | 12.4% / 1.55 / 30 |
| 19 | 2.8% / 0.41 / 25 | 5.8% / 1.36 / 17 | 17.6% / 1.50 / 14 | 5.2% / 0.68 / 24 | 13.8% / 1.23 / 33 |
| 20 | 4.1% / 0.62 / 26 | 7.3% / 1.26 / 21 | 7.8% / 1.07 / 16 | 11.3% / 1.50 / 17 | 3.7% / 0.50 / 26 |
| 21 | -0.3% / -0.04 / 36 | 5.9% / 1.35 / 21 | 7.9% / 0.94 / 20 | 16.5% / 2.52 / 21 | 5.0% / 0.59 / 39 |
| 22 | -4.7% / -0.76 / 21 | 10.9% / 1.79 / 16 | 20.1% / 1.95 / 13 | 17.4% / 1.90 / 20 | 3.8% / 0.42 / 30 |
| 23 | 2.2% / 0.36 / 28 | 7.7% / 1.50 / 21 | 14.9% / 1.56 / 14 | 7.5% / 0.98 / 22 | -0.1% / 0.04 / 29 |
| 24 | -0.9% / -0.16 / 25 | 2.3% / 0.54 / 17 | 4.5% / 0.54 / 9 | 9.4% / 1.75 / 18 | 13.9% / 1.74 / 31 |
| 25 | -7.4% / -1.17 / 21 | 11.8% / 1.73 / 18 | 17.4% / 1.76 / 16 | 11.5% / 1.47 / 18 | 8.3% / 0.81 / 31 |
| 26 | -4.8% / -0.79 / 21 | 11.6% / 1.81 / 16 | 19.0% / 1.84 / 13 | 18.8% / 2.00 / 20 | 2.5% / 0.28 / 30 |
| 27 | 2.0% / 0.31 / 25 | 6.2% / 1.38 / 17 | 16.8% / 1.46 / 14 | 4.4% / 0.59 / 24 | 16.5% / 1.58 / 33 |
| 28 | -3.9% / -0.63 / 22 | 0.3% / 0.08 / 14 | 21.1% / 1.58 / 16 | 22.9% / 1.89 / 26 | 0.3% / 0.08 / 26 |
| 29 | -1.1% / -0.22 / 25 | 2.2% / 0.52 / 17 | 4.0% / 0.50 / 9 | 9.5% / 1.78 / 18 | 12.8% / 1.67 / 31 |
| 30 | 1.9% / 0.45 / 24 | 2.1% / 0.53 / 20 | 13.1% / 1.70 / 12 | 9.3% / 1.33 / 24 | 0.9% / 0.15 / 33 |
| 31 | 7.4% / 1.07 / 22 | 5.7% / 0.98 / 18 | 26.6% / 1.79 / 16 | 6.0% / 0.61 / 26 | 5.8% / 0.57 / 34 |
| 32 | -0.6% / -0.09 / 30 | 0.1% / 0.05 / 14 | 4.1% / 0.57 / 13 | 11.6% / 2.13 / 16 | 10.5% / 1.26 / 30 |
| 33 | 0.2% / 0.07 / 20 | 2.7% / 0.41 / 20 | 22.7% / 1.98 / 18 | 6.9% / 0.79 / 21 | 5.7% / 0.53 / 30 |
| 34 | 2.2% / 0.50 / 24 | 1.7% / 0.45 / 20 | 13.1% / 1.70 / 12 | 9.3% / 1.32 / 24 | 0.6% / 0.12 / 33 |
| 35 | 4.8% / 0.73 / 23 | 2.8% / 0.42 / 21 | 22.8% / 1.83 / 19 | 11.9% / 1.08 / 25 | 3.5% / 0.32 / 29 |
| 36 | 0.7% / 0.13 / 22 | -1.1% / -0.15 / 19 | 24.8% / 2.03 / 17 | 6.6% / 0.69 / 25 | 8.0% / 0.78 / 29 |
| 37 | 4.9% / 0.74 / 25 | -0.7% / -0.13 / 18 | 10.6% / 1.05 / 17 | 6.1% / 0.81 / 22 | 13.3% / 1.45 / 28 |
| 38 | 2.1% / 0.38 / 20 | 9.3% / 1.63 / 17 | 10.6% / 1.21 / 14 | -0.6% / -0.05 / 25 | 20.1% / 2.01 / 34 |
| 39 | 2.1% / 0.37 / 20 | 8.2% / 1.47 / 17 | 10.2% / 0.91 / 14 | -0.2% / 0.02 / 25 | 23.0% / 2.20 / 34 |
| 40 | 1.6% / 0.25 / 40 | 9.5% / 1.56 / 25 | 11.6% / 0.96 / 23 | 16.9% / 1.84 / 27 | 11.2% / 1.03 / 38 |
| 41 | -0.6% / -0.09 / 36 | 5.3% / 1.25 / 21 | 8.7% / 1.03 / 20 | 15.7% / 2.42 / 21 | 3.9% / 0.47 / 39 |
| 42 | 5.5% / 0.97 / 29 | -4.1% / -1.07 / 23 | 5.8% / 0.80 / 18 | 7.9% / 1.21 / 27 | 11.5% / 1.33 / 34 |
| 43 | 0.8% / 0.17 / 34 | 0.4% / 0.14 / 14 | 4.4% / 0.63 / 16 | 11.0% / 1.94 / 19 | 9.1% / 0.98 / 35 |
| 44 | 1.6% / 0.28 / 26 | -0.5% / -0.08 / 18 | 16.8% / 1.85 / 18 | 2.0% / 0.31 / 21 | 11.9% / 1.19 / 33 |
| 45 | 1.5% / 0.25 / 27 | 9.9% / 1.93 / 19 | 17.5% / 1.67 / 17 | 7.8% / 0.94 / 25 | 2.9% / 0.34 / 29 |
| 46 | 10.7% / 1.62 / 23 | 6.4% / 0.91 / 21 | 29.5% / 2.08 / 20 | 3.7% / 0.42 / 20 | 1.7% / 0.19 / 32 |
| 47 | -6.8% / -0.67 / 37 | 10.5% / 1.65 / 23 | 28.1% / 1.81 / 23 | 17.4% / 1.36 / 42 | 6.4% / 0.51 / 51 |
| 48 | -1.1% / -0.08 / 44 | 9.6% / 1.57 / 26 | 14.8% / 1.16 / 27 | 13.3% / 1.52 / 29 | 9.1% / 0.84 / 43 |
| 49 | -3.5% / -0.55 / 33 | 4.4% / 1.19 / 14 | 3.4% / 0.49 / 16 | 8.8% / 1.80 / 14 | 11.7% / 1.48 / 30 |
| 50 | -0.8% / -0.07 / 24 | 4.7% / 0.76 / 19 | 18.8% / 1.75 / 16 | 10.1% / 1.15 / 19 | 6.7% / 0.64 / 28 |
| 51 | 2.6% / 0.45 / 20 | 8.1% / 1.46 / 17 | 15.3% / 1.23 / 14 | -0.5% / -0.02 / 25 | 17.0% / 1.52 / 34 |
| 52 | -1.2% / -0.13 / 24 | 3.7% / 0.62 / 19 | 19.5% / 1.77 / 16 | 8.8% / 1.00 / 19 | 7.6% / 0.75 / 29 |
| 53 | 6.1% / 0.75 / 41 | -3.2% / -0.53 / 29 | 10.3% / 0.89 / 24 | 20.5% / 1.78 / 41 | 16.0% / 1.51 / 43 |
| 54 | -3.9% / -0.63 / 22 | -0.5% / -0.08 / 14 | 21.3% / 1.61 / 16 | 16.6% / 1.51 / 26 | 2.3% / 0.30 / 26 |
| 55 | 2.9% / 0.46 / 27 | 3.4% / 0.68 / 22 | 22.1% / 1.88 / 18 | 5.6% / 0.76 / 21 | 5.1% / 0.56 / 27 |
| 56 | 0.7% / 0.12 / 37 | 12.2% / 1.93 / 23 | 13.3% / 1.12 / 24 | 10.3% / 1.23 / 28 | 4.7% / 0.47 / 47 |
| 57 | 4.7% / 0.75 / 20 | 10.1% / 1.73 / 19 | 17.6% / 1.50 / 14 | 3.8% / 0.53 / 24 | 3.5% / 0.37 / 33 |
| 58 | 5.2% / 0.68 / 45 | 0.7% / 0.13 / 37 | 11.5% / 0.89 / 29 | 18.8% / 1.70 / 45 | 18.4% / 1.53 / 56 |
| 59 | -7.4% / -0.92 / 27 | 8.6% / 1.13 / 18 | 11.3% / 0.90 / 17 | 21.9% / 1.90 / 22 | 11.5% / 1.09 / 28 |
| 60 | -0.9% / -0.11 / 38 | 4.6% / 1.30 / 14 | 4.2% / 0.71 / 18 | 9.6% / 1.85 / 15 | 9.8% / 1.09 / 35 |
| 61 | 0.8% / 0.15 / 27 | 4.5% / 0.83 / 22 | 9.7% / 1.32 / 15 | 8.0% / 1.19 / 16 | 13.2% / 1.52 / 28 |
| 62 | 0.7% / 0.14 / 22 | 9.3% / 1.67 / 19 | 17.6% / 1.41 / 17 | 9.4% / 1.39 / 17 | 9.0% / 1.04 / 25 |
| 63 | 5.0% / 0.90 / 29 | -4.1% / -1.07 / 23 | 6.3% / 0.87 / 18 | 8.6% / 1.30 / 27 | 11.2% / 1.25 / 34 |
| 64 | 7.4% / 1.01 / 23 | 5.3% / 0.87 / 17 | 26.2% / 1.90 / 15 | 5.3% / 0.56 / 25 | -5.3% / -0.39 / 30 |
| 65 | -3.7% / -0.65 / 32 | 3.3% / 0.79 / 23 | 11.2% / 1.58 / 19 | 10.6% / 1.52 / 25 | 9.1% / 1.15 / 31 |
| 66 | 1.3% / 0.22 / 25 | 10.1% / 2.14 / 16 | 0.1% / 0.08 / 16 | 2.8% / 0.41 / 19 | 22.5% / 2.20 / 33 |
| 67 | -10.7% / -1.24 / 30 | 3.0% / 0.53 / 20 | 32.8% / 2.32 / 21 | 7.2% / 0.72 / 34 | 11.3% / 1.12 / 37 |
| 68 | 0.5% / 0.11 / 22 | 8.4% / 1.57 / 19 | 16.4% / 1.33 / 17 | 9.2% / 1.33 / 17 | 7.7% / 0.94 / 25 |
| 69 | -0.3% / -0.01 / 27 | 3.5% / 0.66 / 22 | 9.6% / 1.31 / 15 | 5.8% / 0.90 / 16 | 13.6% / 1.57 / 28 |
| 70 | -0.2% / 0.02 / 37 | 11.8% / 1.88 / 23 | 10.1% / 0.90 / 24 | 9.4% / 1.11 / 28 | 6.2% / 0.59 / 47 |
| 71 | 4.4% / 0.70 / 27 | 3.8% / 0.90 / 19 | 9.9% / 1.00 / 19 | 5.6% / 0.74 / 22 | 7.3% / 0.81 / 31 |
| 72 | -10.2% / -1.07 / 33 | 6.3% / 0.91 / 24 | 25.0% / 2.07 / 23 | 6.7% / 0.68 / 29 | 12.0% / 1.03 / 39 |
| 73 | -6.4% / -0.80 / 28 | 11.7% / 1.90 / 17 | 17.0% / 1.21 / 15 | 11.8% / 1.15 / 21 | 13.2% / 1.05 / 33 |
| 74 | 1.9% / 0.26 / 44 | 1.0% / 0.19 / 30 | 9.1% / 0.73 / 26 | 14.8% / 1.64 / 41 | 20.2% / 1.90 / 44 |
| 75 | 3.9% / 0.65 / 20 | 8.7% / 1.53 / 19 | 12.5% / 1.19 / 14 | 3.5% / 0.49 / 24 | 5.7% / 0.61 / 33 |
| 76 | 1.7% / 0.30 / 25 | 11.3% / 2.59 / 16 | 6.0% / 0.46 / 20 | 11.4% / 1.43 / 22 | 13.6% / 1.52 / 25 |
| 77 | -1.4% / -0.20 / 17 | 0.6% / 0.13 / 16 | 31.6% / 2.47 / 16 | 7.8% / 0.91 / 23 | 0.8% / 0.13 / 29 |
| 78 | -3.9% / -0.48 / 26 | 5.4% / 0.93 / 14 | 21.4% / 1.89 / 10 | 9.6% / 1.00 / 20 | 7.8% / 0.64 / 35 |
| 79 | -3.0% / -0.37 / 27 | 7.4% / 1.26 / 15 | 16.6% / 1.71 / 10 | 8.3% / 0.96 / 21 | 10.0% / 0.80 / 36 |
| 80 | 1.7% / 0.30 / 25 | 12.0% / 2.67 / 16 | 6.5% / 0.49 / 20 | 9.4% / 1.20 / 22 | 13.3% / 1.49 / 25 |
| 81 | 2.8% / 0.43 / 35 | 4.8% / 0.75 / 26 | 4.3% / 0.57 / 24 | 13.0% / 1.30 / 34 | 7.9% / 0.72 / 43 |
| 82 | -6.4% / -0.81 / 28 | 10.3% / 1.74 / 17 | 12.3% / 0.97 / 15 | 14.1% / 1.40 / 21 | 12.8% / 1.07 / 33 |
| 83 | -8.2% / -0.93 / 33 | 4.2% / 0.67 / 25 | 30.2% / 2.11 / 22 | 16.9% / 1.54 / 28 | 3.7% / 0.40 / 30 |
| 84 | 0.8% / 0.14 / 25 | 9.0% / 2.00 / 16 | -0.1% / 0.06 / 16 | 2.7% / 0.41 / 19 | 21.6% / 2.17 / 33 |
| 85 | 8.2% / 1.11 / 24 | 10.1% / 1.50 / 23 | 16.7% / 1.32 / 16 | 11.3% / 1.05 / 28 | 4.8% / 0.48 / 35 |
| 86 | -9.0% / -1.01 / 30 | 2.6% / 0.47 / 19 | 41.3% / 2.63 / 20 | 5.5% / 0.55 / 33 | 5.9% / 0.51 / 38 |
| 87 | -14.4% / -1.79 / 33 | 17.8% / 2.55 / 19 | 23.2% / 1.99 / 21 | 9.5% / 1.15 / 21 | 6.0% / 0.48 / 46 |
| 88 | 1.6% / 0.28 / 32 | -1.2% / -0.20 / 23 | 14.1% / 1.16 / 24 | 11.3% / 1.14 / 38 | 11.1% / 0.99 / 41 |
| 89 | -9.4% / -1.04 / 41 | 18.1% / 2.37 / 25 | 15.4% / 1.21 / 23 | 25.5% / 1.85 / 42 | 0.5% / 0.10 / 50 |
| 90 | -14.2% / -1.31 / 39 | 6.6% / 1.09 / 21 | 42.3% / 2.67 / 22 | 8.7% / 0.80 / 37 | 6.2% / 0.52 / 43 |
| 91 | 4.5% / 0.63 / 26 | -1.6% / -0.23 / 19 | 18.9% / 1.72 / 19 | 13.7% / 1.38 / 20 | 8.2% / 0.74 / 30 |
| 92 | 8.6% / 1.23 / 21 | 8.5% / 1.48 / 18 | 21.1% / 1.56 / 14 | 9.1% / 0.99 / 25 | -8.6% / -0.62 / 36 |
| 93 | -9.0% / -0.85 / 45 | 4.0% / 0.56 / 29 | 33.0% / 2.36 / 26 | 12.5% / 0.97 / 46 | 9.5% / 0.71 / 45 |
| 94 | 6.9% / 0.77 / 26 | 6.5% / 1.08 / 19 | 9.6% / 0.63 / 21 | 27.8% / 2.20 / 25 | 0.4% / 0.10 / 32 |
| 95 | -2.5% / -0.34 / 44 | 0.2% / 0.06 / 32 | 15.0% / 1.15 / 31 | 14.5% / 1.31 / 48 | 10.2% / 0.92 / 47 |
| 96 | 6.9% / 1.08 / 21 | 6.2% / 1.16 / 18 | 16.0% / 1.29 / 14 | 10.1% / 1.12 / 26 | -2.2% / -0.13 / 36 |
| 97 | 1.9% / 0.26 / 42 | 5.4% / 0.76 / 33 | 10.5% / 0.91 / 24 | 15.2% / 1.44 / 41 | 9.8% / 0.91 / 43 |
| 98 | -9.7% / -0.93 / 45 | 3.7% / 0.54 / 29 | 30.6% / 2.23 / 26 | 12.0% / 0.93 / 46 | 10.4% / 0.84 / 46 |
| 99 | -0.9% / -0.11 / 38 | 4.6% / 1.30 / 14 | 3.4% / 0.60 / 18 | 8.8% / 1.72 / 15 | 9.4% / 1.04 / 35 |
| 100 | 3.6% / 0.53 / 25 | 6.4% / 1.04 / 19 | 30.1% / 1.98 / 18 | 4.1% / 0.51 / 27 | 8.1% / 0.79 / 35 |
| 101 | 2.0% / 0.49 / 23 | 2.6% / 0.70 / 19 | 21.8% / 1.95 / 14 | 3.3% / 0.51 / 22 | 1.1% / 0.18 / 35 |
| 102 | 1.5% / 0.22 / 49 | 3.7% / 0.52 / 38 | 10.7% / 0.76 / 31 | 12.8% / 1.47 / 45 | 18.4% / 1.56 / 56 |
| 103 | -0.2% / -0.03 / 27 | 5.0% / 1.36 / 18 | 13.0% / 1.42 / 11 | 4.8% / 0.72 / 23 | 3.5% / 0.48 / 27 |
| 104 | 3.3% / 0.48 / 35 | 2.8% / 0.47 / 26 | 6.5% / 0.83 / 25 | 10.3% / 1.09 / 34 | 8.3% / 0.80 / 43 |
| 105 | 2.6% / 0.53 / 31 | -1.3% / -0.32 / 28 | 20.9% / 2.16 / 19 | 7.6% / 1.23 / 24 | -2.9% / -0.35 / 36 |
| 106 | -0.0% / 0.02 / 27 | 5.0% / 1.36 / 18 | 13.3% / 1.43 / 11 | 4.8% / 0.72 / 23 | 3.2% / 0.44 / 27 |
| 107 | -0.6% / -0.05 / 23 | -3.5% / -0.52 / 20 | 32.3% / 2.32 / 20 | 14.3% / 1.45 / 25 | 3.9% / 0.39 / 27 |
| 108 | 5.1% / 0.59 / 26 | 6.0% / 1.01 / 19 | 10.4% / 0.68 / 21 | 24.0% / 1.93 / 25 | 0.6% / 0.11 / 32 |
| 109 | -6.4% / -0.81 / 25 | 7.3% / 1.29 / 13 | 8.6% / 0.95 / 11 | 14.9% / 1.46 / 20 | 14.7% / 1.10 / 32 |
| 110 | -9.4% / -0.88 / 51 | 7.3% / 1.14 / 27 | 38.7% / 1.98 / 26 | 16.0% / 1.28 / 45 | 0.6% / 0.12 / 62 |
| 111 | 1.4% / 0.24 / 32 | -1.2% / -0.21 / 23 | 14.0% / 1.15 / 24 | 10.7% / 1.09 / 38 | 10.1% / 0.91 / 41 |
| 112 | -3.0% / -0.60 / 26 | 5.1% / 1.13 / 14 | 20.3% / 1.79 / 17 | 8.0% / 1.44 / 16 | -1.8% / -0.17 / 37 |
| 113 | -5.0% / -0.93 / 32 | 2.8% / 0.69 / 23 | 10.6% / 1.52 / 19 | 10.0% / 1.45 / 25 | 8.5% / 1.08 / 31 |
| 114 | 8.4% / 0.91 / 29 | 1.3% / 0.25 / 18 | 23.8% / 1.83 / 19 | 13.4% / 1.31 / 22 | 2.5% / 0.25 / 31 |
| 115 | -2.0% / -0.25 / 23 | -3.0% / -0.44 / 20 | 28.9% / 2.14 / 20 | 12.5% / 1.31 / 25 | 10.5% / 0.97 / 28 |
| 116 | -2.7% / -0.42 / 24 | 13.1% / 2.51 / 15 | 9.7% / 0.77 / 17 | 11.6% / 1.45 / 20 | 0.7% / 0.12 / 25 |
| 117 | 2.7% / 0.40 / 25 | 7.1% / 1.17 / 18 | 16.5% / 1.23 / 14 | 4.7% / 0.49 / 21 | 10.3% / 0.83 / 35 |
| 118 | 0.9% / 0.15 / 42 | 4.1% / 0.60 / 33 | 11.3% / 0.96 / 24 | 14.7% / 1.42 / 41 | 11.5% / 1.05 / 43 |
| 119 | -6.9% / -0.83 / 26 | 4.5% / 0.69 / 20 | 16.4% / 1.20 / 17 | 17.1% / 1.56 / 24 | 16.8% / 1.25 / 39 |
| 120 | 3.8% / 0.56 / 42 | 5.8% / 0.78 / 34 | 12.5% / 1.18 / 32 | 7.5% / 0.78 / 44 | 11.7% / 1.07 / 54 |
| 121 | 1.9% / 0.32 / 26 | -0.5% / -0.07 / 18 | 16.0% / 1.76 / 18 | 1.0% / 0.17 / 21 | 10.2% / 1.10 / 33 |
| 122 | -9.1% / -1.11 / 35 | 4.2% / 0.77 / 24 | 18.9% / 1.85 / 20 | 5.3% / 0.69 / 25 | 13.8% / 1.43 / 34 |
| 123 | 3.2% / 0.42 / 37 | 3.2% / 0.56 / 26 | 6.7% / 0.60 / 26 | 21.0% / 2.02 / 42 | 4.7% / 0.54 / 43 |
| 124 | -0.7% / -0.06 / 24 | 13.5% / 1.96 / 22 | 26.8% / 1.80 / 15 | 9.3% / 0.90 / 26 | -8.0% / -0.77 / 29 |
| 125 | -1.1% / -0.15 / 22 | 5.6% / 0.89 / 16 | 25.5% / 2.07 / 16 | 19.7% / 1.73 / 25 | -3.9% / -0.35 / 26 |
| 126 | 1.9% / 0.38 / 19 | 9.5% / 1.54 / 18 | 2.0% / 0.28 / 13 | 3.4% / 0.46 / 19 | 13.4% / 1.28 / 33 |
| 127 | -8.2% / -0.82 / 40 | 7.2% / 0.90 / 33 | 27.9% / 2.06 / 27 | 5.4% / 0.53 / 38 | 10.8% / 0.90 / 45 |
| 128 | -0.6% / -0.04 / 54 | -0.2% / -0.00 / 33 | 10.1% / 1.08 / 31 | 12.1% / 1.28 / 39 | 18.5% / 1.62 / 52 |
| 129 | 2.0% / 0.41 / 31 | -1.6% / -0.39 / 28 | 21.8% / 2.23 / 19 | 7.8% / 1.25 / 24 | -2.4% / -0.28 / 36 |
| 130 | 3.3% / 0.46 / 45 | 4.4% / 0.66 / 33 | 5.7% / 0.49 / 31 | 21.1% / 2.14 / 47 | 10.0% / 0.87 / 54 |
| 131 | -7.8% / -0.96 / 26 | 8.6% / 1.30 / 20 | 16.9% / 1.23 / 17 | 17.7% / 1.70 / 24 | 13.2% / 1.08 / 39 |
| 132 | 1.0% / 0.21 / 28 | 1.4% / 0.37 / 22 | 11.1% / 0.97 / 16 | 3.2% / 0.49 / 25 | 12.6% / 1.46 / 35 |
| 133 | -1.1% / -0.15 / 22 | 4.4% / 0.74 / 16 | 26.0% / 2.07 / 16 | 15.5% / 1.46 / 25 | -2.7% / -0.27 / 26 |
| 134 | -4.2% / -0.72 / 33 | 7.2% / 1.78 / 19 | 11.1% / 0.96 / 23 | 10.7% / 1.61 / 26 | 9.9% / 1.29 / 28 |
| 135 | -7.8% / -0.99 / 27 | 7.7% / 1.04 / 18 | 7.6% / 0.68 / 17 | 16.4% / 1.58 / 22 | 12.3% / 1.22 / 28 |
| 136 | 7.7% / 0.84 / 29 | 0.8% / 0.17 / 18 | 24.0% / 1.80 / 19 | 13.1% / 1.33 / 22 | -2.1% / -0.08 / 31 |
| 137 | 2.4% / 0.46 / 19 | 10.0% / 1.58 / 18 | 1.0% / 0.16 / 13 | 5.2% / 0.75 / 20 | 10.5% / 1.07 / 33 |
| 138 | -4.2% / -0.72 / 33 | 7.2% / 1.78 / 19 | 10.7% / 0.96 / 23 | 10.6% / 1.61 / 26 | 9.9% / 1.29 / 28 |
| 139 | 4.6% / 0.68 / 42 | 4.4% / 0.61 / 35 | 9.2% / 0.94 / 33 | 6.5% / 0.69 / 44 | 12.9% / 1.20 / 54 |
| 140 | 2.0% / 0.30 / 24 | 12.9% / 2.02 / 17 | 9.3% / 0.78 / 14 | 11.9% / 1.18 / 21 | 3.6% / 0.37 / 32 |
| 141 | -1.5% / -0.18 / 24 | 12.5% / 1.86 / 22 | 25.0% / 1.85 / 15 | 6.6% / 0.69 / 26 | -5.5% / -0.55 / 29 |
| 142 | 1.6% / 0.35 / 25 | 1.7% / 0.41 / 21 | 12.5% / 1.08 / 16 | 1.6% / 0.30 / 21 | 13.0% / 1.65 / 32 |
| 143 | 4.2% / 0.57 / 35 | 5.7% / 1.21 / 18 | 12.9% / 1.27 / 22 | 10.2% / 1.32 / 24 | -0.5% / -0.00 / 30 |
| 144 | -6.7% / -0.75 / 42 | 3.7% / 0.64 / 27 | 10.6% / 1.09 / 29 | 28.3% / 2.42 / 39 | 6.3% / 0.60 / 42 |
| 145 | 4.5% / 0.64 / 27 | -1.5% / -0.22 / 19 | 14.6% / 1.47 / 21 | 10.9% / 1.18 / 21 | 4.1% / 0.43 / 30 |
| 146 | 2.1% / 0.38 / 28 | -3.0% / -0.41 / 28 | 12.7% / 1.26 / 23 | 13.9% / 1.34 / 34 | 19.0% / 1.69 / 38 |
| 147 | 6.8% / 0.94 / 24 | 10.1% / 1.47 / 23 | 14.7% / 1.22 / 16 | 8.1% / 0.82 / 28 | 5.3% / 0.53 / 35 |
| 148 | -2.8% / -0.43 / 24 | 9.0% / 1.50 / 19 | 8.3% / 0.93 / 17 | -3.0% / -0.35 / 28 | 19.2% / 1.90 / 37 |
| 149 | 4.3% / 0.66 / 24 | 7.6% / 1.26 / 18 | 9.2% / 0.77 / 13 | 26.9% / 3.15 / 21 | -1.2% / -0.05 / 38 |
| 150 | 0.5% / 0.10 / 54 | -0.1% / 0.01 / 33 | 9.5% / 1.05 / 31 | 11.9% / 1.25 / 39 | 12.3% / 1.06 / 52 |
| 151 | -8.1% / -0.79 / 41 | 15.9% / 2.20 / 22 | 29.2% / 2.05 / 20 | 4.8% / 0.46 / 31 | 3.7% / 0.35 / 50 |
| 152 | -5.0% / -0.64 / 28 | 14.8% / 2.12 / 20 | 18.2% / 1.35 / 19 | 9.2% / 1.00 / 24 | 5.4% / 0.53 / 42 |
| 153 | -7.9% / -0.87 / 33 | 4.3% / 0.67 / 25 | 33.3% / 2.26 / 22 | 15.0% / 1.35 / 28 | 1.2% / 0.16 / 30 |
| 154 | 3.2% / 0.55 / 26 | -5.5% / -0.92 / 22 | 13.4% / 1.16 / 20 | 10.9% / 1.11 / 30 | 14.5% / 1.37 / 37 |
| 155 | -10.8% / -1.39 / 26 | 5.9% / 1.00 / 19 | 6.3% / 0.62 / 20 | 29.4% / 2.48 / 27 | 7.5% / 0.75 / 29 |
| 156 | 5.1% / 0.64 / 35 | 2.8% / 0.42 / 28 | 11.6% / 0.91 / 23 | 22.1% / 2.09 / 37 | 0.6% / 0.11 / 48 |
| 157 | -4.6% / -0.57 / 28 | 14.9% / 2.12 / 20 | 21.7% / 1.55 / 19 | 11.7% / 1.19 / 24 | 1.6% / 0.19 / 42 |
| 158 | 0.9% / 0.17 / 27 | -10.7% / -1.77 / 20 | 17.1% / 1.50 / 18 | 15.6% / 1.87 / 28 | 10.4% / 1.10 / 33 |
| 159 | 1.5% / 0.23 / 24 | 12.2% / 1.96 / 17 | 8.4% / 0.74 / 14 | 9.3% / 0.97 / 21 | 5.0% / 0.51 / 32 |
| 160 | 1.2% / 0.23 / 22 | 3.0% / 0.56 / 19 | 11.4% / 1.30 / 17 | -0.1% / 0.02 / 25 | 13.1% / 1.36 / 36 |
| 161 | 0.4% / 0.10 / 27 | -3.0% / -0.41 / 22 | 18.2% / 1.82 / 20 | 9.5% / 1.11 / 26 | 12.1% / 1.08 / 32 |
| 162 | -1.6% / -0.22 / 26 | 14.9% / 2.02 / 21 | 5.7% / 0.52 / 17 | 10.8% / 1.27 / 22 | 7.9% / 0.75 / 37 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_fd1e` | 5 | 0.93 | 0.91/0.95 | 0.83/0.91 |
| 1 | `cfg_b7f1` | 4 | 0.84 | 0.84/0.85 | 0.52/0.52 |
| 2 | `cfg_0209` | 9 | 0.80 | 0.87/0.92 | 0.75/0.82 |
| 3 | `cfg_044e` | 2 | 0.99 | 0.99/0.99 | 0.96/0.96 |
| 4 | `cfg_f682` | 8 | 0.86 | 0.91/0.92 | 0.82/0.85 |
| 5 | `cfg_e300` | 3 | 0.88 | 0.89/0.93 | 0.91/0.94 |
| 6 | `cfg_30f0` | 2 | 0.99 | 0.98/0.98 | 0.95/0.95 |
| 7 | `cfg_0b25` | 3 | 0.84 | 0.84/0.90 | 0.63/0.79 |
| 8 | `cfg_8cd1` | 3 | 0.98 | 0.98/0.99 | 0.98/0.99 |
| 9 | `cfg_3c7a` | 3 | 0.97 | 0.97/0.97 | 0.96/0.96 |
| 10 | `cfg_6024` | 3 | 0.98 | 0.98/0.99 | 0.98/0.98 |
| 11 | `cfg_109f` | 2 | 0.97 | 0.96/0.96 | 0.90/0.90 |
| 12 | `cfg_4345` | 5 | 0.82 | 0.80/0.89 | 0.78/0.80 |
| 13 | `cfg_13a7` | 4 | 0.85 | 0.82/0.84 | 0.64/0.67 |
| 14 | `cfg_c0cc` | 5 | 0.93 | 0.93/0.96 | 0.81/0.90 |
| 15 | `cfg_81a9` | 3 | 0.93 | 0.94/0.95 | 0.90/0.91 |
| 16 | `cfg_ccfb` | 5 | 0.84 | 0.85/0.89 | 0.77/0.82 |
| 17 | `cfg_195d` | 6 | 0.85 | 0.78/0.89 | 0.69/0.81 |
| 18 | `cfg_683c` | 5 | 0.87 | 0.88/0.89 | 0.81/0.86 |
| 19 | `cfg_591a` | 7 | 0.81 | 0.77/0.83 | 0.58/0.72 |
| 20 | `cfg_d2d0` | 9 | 0.80 | 0.81/0.85 | 0.64/0.68 |
| 21 | `cfg_1fab` | 1 | n/a | n/a/n/a | n/a/n/a |
| 22 | `cfg_a7f9` | 6 | 0.82 | 0.78/0.85 | 0.67/0.76 |
| 23 | `cfg_a510` | 4 | 0.81 | 0.71/0.96 | 0.44/0.96 |
| 24 | `cfg_c0c4` | 6 | 0.90 | 0.89/0.92 | 0.81/0.83 |
| 25 | `cfg_2dad` | 2 | 0.85 | 0.78/0.78 | 0.76/0.76 |
| 26 | `cfg_da5c` | 7 | 0.88 | 0.85/0.89 | 0.80/0.83 |
| 27 | `cfg_27f9` | 3 | 0.94 | 0.94/0.96 | 0.84/0.88 |
| 28 | `cfg_2c25` | 7 | 0.83 | 0.80/0.88 | 0.70/0.78 |
| 29 | `cfg_2a22` | 2 | 0.94 | 0.94/0.94 | 0.85/0.85 |
| 30 | `cfg_5910` | 2 | 0.98 | 0.98/0.98 | 0.96/0.96 |
| 31 | `cfg_5d27` | 3 | 0.98 | 0.98/0.99 | 0.99/0.99 |
| 32 | `cfg_2c46` | 2 | 1.00 | 1.00/1.00 | 0.99/0.99 |
| 33 | `cfg_2c81` | 2 | 0.97 | 0.94/0.94 | 0.94/0.94 |
| 34 | `cfg_2d69` | 5 | 0.94 | 0.92/0.95 | 0.89/0.91 |
| 35 | `cfg_2e75` | 1 | n/a | n/a/n/a | n/a/n/a |
| 36 | `cfg_6023` | 8 | 0.86 | 0.88/0.95 | 0.78/0.87 |
| 37 | `cfg_5754` | 2 | 0.93 | 0.95/0.95 | 0.92/0.92 |
| 38 | `cfg_3272` | 1 | n/a | n/a/n/a | n/a/n/a |
| 39 | `cfg_586e` | 5 | 0.93 | 0.90/0.92 | 0.75/0.83 |
| 40 | `cfg_7502` | 2 | 0.95 | 0.95/0.95 | 0.96/0.96 |
| 41 | `cfg_3791` | 3 | 0.93 | 0.95/0.97 | 0.95/0.96 |
| 42 | `cfg_37de` | 3 | 0.92 | 0.93/0.96 | 0.81/0.89 |
| 43 | `cfg_39ad` | 2 | 0.91 | 0.95/0.95 | 0.93/0.93 |
| 44 | `cfg_3af4` | 2 | 0.97 | 0.96/0.96 | 0.92/0.92 |
| 45 | `cfg_be97` | 3 | 0.83 | 0.92/0.93 | 0.85/0.88 |
| 46 | `cfg_8624` | 3 | 0.91 | 0.95/0.96 | 0.95/0.95 |
| 47 | `cfg_4220` | 1 | n/a | n/a/n/a | n/a/n/a |
| 48 | `cfg_9f9f` | 2 | 0.96 | 0.98/0.98 | 0.93/0.93 |
| 49 | `cfg_48f4` | 1 | n/a | n/a/n/a | n/a/n/a |
| 50 | `cfg_4b0a` | 2 | 0.94 | 0.95/0.95 | 0.96/0.96 |
| 51 | `cfg_4bd1` | 2 | 0.97 | 0.97/0.97 | 0.98/0.98 |
| 52 | `cfg_50ab` | 3 | 0.84 | 0.81/0.89 | 0.68/0.84 |
| 53 | `cfg_be6d` | 2 | 0.99 | 0.99/0.99 | 0.97/0.97 |
| 54 | `cfg_b19a` | 3 | 0.97 | 0.97/0.98 | 0.95/0.96 |
| 55 | `cfg_5251` | 1 | n/a | n/a/n/a | n/a/n/a |
| 56 | `cfg_5527` | 1 | n/a | n/a/n/a | n/a/n/a |
| 57 | `cfg_fbc1` | 4 | 0.91 | 0.92/0.98 | 0.82/0.96 |
| 58 | `cfg_5857` | 2 | 1.00 | 1.00/1.00 | 0.97/0.97 |
| 59 | `cfg_5a53` | 1 | n/a | n/a/n/a | n/a/n/a |
| 60 | `cfg_85d8` | 5 | 0.97 | 0.94/0.97 | 0.92/0.95 |
| 61 | `cfg_6865` | 2 | 0.92 | 0.91/0.91 | 0.88/0.88 |
| 62 | `cfg_c96a` | 8 | 0.82 | 0.81/0.92 | 0.61/0.84 |
| 63 | `cfg_fbbc` | 4 | 0.86 | 0.66/0.68 | 0.48/0.49 |
| 64 | `cfg_6b6d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 65 | `cfg_fde2` | 3 | 0.95 | 0.97/0.98 | 0.96/0.97 |
| 66 | `cfg_b119` | 2 | 0.83 | 0.83/0.83 | 0.74/0.74 |
| 67 | `cfg_72f6` | 1 | n/a | n/a/n/a | n/a/n/a |
| 68 | `cfg_745b` | 2 | 0.90 | 0.89/0.89 | 0.82/0.82 |
| 69 | `cfg_87fe` | 6 | 0.82 | 0.75/0.90 | 0.52/0.74 |
| 70 | `cfg_75fc` | 1 | n/a | n/a/n/a | n/a/n/a |
| 71 | `cfg_77a5` | 2 | 0.97 | 0.97/0.97 | 0.93/0.93 |
| 72 | `cfg_dc4a` | 3 | 0.91 | 0.92/0.96 | 0.86/0.92 |
| 73 | `cfg_d21a` | 4 | 0.88 | 0.85/0.96 | 0.82/0.97 |
| 74 | `cfg_89fc` | 4 | 0.92 | 0.94/0.95 | 0.81/0.94 |
| 75 | `cfg_a006` | 2 | 0.95 | 0.96/0.96 | 0.91/0.91 |
| 76 | `cfg_8dca` | 2 | 0.99 | 0.99/0.99 | 0.99/0.99 |
| 77 | `cfg_9195` | 1 | n/a | n/a/n/a | n/a/n/a |
| 78 | `cfg_ac39` | 3 | 0.86 | 0.91/0.95 | 0.80/0.86 |
| 79 | `cfg_e524` | 2 | 1.00 | 1.00/1.00 | 0.99/0.99 |
| 80 | `cfg_ae3d` | 2 | 0.96 | 0.96/0.96 | 0.92/0.92 |
| 81 | `cfg_d8e0` | 2 | 0.99 | 0.99/0.99 | 0.96/0.96 |
| 82 | `cfg_e0cc` | 2 | 0.98 | 0.93/0.93 | 0.94/0.94 |
| 83 | `cfg_b5fd` | 2 | 0.89 | 0.89/0.89 | 0.84/0.84 |
| 84 | `cfg_c976` | 1 | n/a | n/a/n/a | n/a/n/a |
| 85 | `cfg_e5b5` | 1 | n/a | n/a/n/a | n/a/n/a |
| 86 | `cfg_e639` | 1 | n/a | n/a/n/a | n/a/n/a |
| 87 | `cfg_ed6b` | 1 | n/a | n/a/n/a | n/a/n/a |
| 88 | `cfg_f903` | 1 | n/a | n/a/n/a | n/a/n/a |
| 89 | `cfg_fda5` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 4.555e-04 over 8640 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 503.0, participation ratio 6.8, 95%-variance components 136 (rank bound T = 1259); raw grid 8640; raw + known prior 919644
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
