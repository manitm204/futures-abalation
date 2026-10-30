# Screening funnel -- mr_rty_v5 (development stages only)

- Code: `5342a94cdc84` (dirty working tree: True, diff sha256 `598f57a8e7c7`)
- Config: `configs/funnel/mr_funnel_rty_v5.yaml` sha256 `189f2ecae24f6b9d`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ES': '2026-10-16', 'RTY': '2026-10-16'}
- Frozen manifest sha256: `e0c3943531bfaedc` (27 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **False** -- No strategy has been selected on RTY 2023-2024. But RTY is correlated with ES/NQ, and this v5 grid and the 40-trade validation rule were chosen after reading ES 2023-2024 results (mr_es_v3..v5) and run alongside NQ (mr_nq_v5). So the slice is not fully independent of earlier research.
- Holdout 2025+ previously inspected: **False** -- No RTY strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 41472 | 41472 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 41472 | 41472 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 41472 | 29848 | 11624 | 0 |  | 33234 | 71.97 | 71.97 |  |
| 3 performance & risk | hard_gate | 29848 | 69 | 29779 | 0 |  | 0 | 0.17 | 0.23 |  |
| 4 parameter stability | hard_gate | 69 | 63 | 6 | 0 |  | 0 | 0.15 | 91.30 |  |
| 5 time stability | hard_gate | 63 | 61 | 2 | 0 |  | 58 | 0.15 | 96.83 |  |
| 6 deduplication | dedup | 61 | 27 |  |  | 34 |  | 0.07 | 44.26 | best 2 per cluster |
| 7 execution stress | hard_gate | 27 | 27 | 0 | 0 |  | 7 | 0.07 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 27 |  |  |  |  |  |  |  | diagnostic only: unverified: 27 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 11624 |
| s2:hard_reject:years_with_>=10_trades | 8011 |
| s3:hard_reject:max_drawdown | 7111 |
| s3:hard_reject:net_return | 23917 |
| s3:hard_reject:sharpe | 29779 |
| s4:hard_reject:local_median_sharpe | 6 |
| s5:hard_reject:profitable_years | 2 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_8fea` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 23/103/0 | 126 | 50.6% | 8.5% | 0.91 | -8.3% | 221 | 1.62 | 15.2% | 57.4 | 8/8 | 0.75 | 0.51 | 0.40 | 4 | 26.6% | 0.43 | 0.63 | 49.7% | 48.4% | 53.2% | 44.8%/32.4% | 20.3 (interpolated) | pass | 0.082 (unverified) | -0.13 |
| 2 | `cfg_cac3` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 4/118/0 | 122 | 15.3% | 2.9% | 0.87 | -4.1% | 347 | 1.61 | 2.2% | 55.0 | 8/8 | 0.62 | 0.53 | 0.34 | 3 | 7.3% | 0.50 | 0.65 | 14.5% | 13.3% | 5.4% | 14.5%/10.8% | 8.0 (interpolated) | pass | 0.062 (unverified) | 0.01 |
| 3 | `cfg_d785` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 21/97/0 | 118 | 56.5% | 9.4% | 0.98 | -11.2% | 221 | 1.61 | 14.1% | 54.5 | 8/8 | 0.50 | 0.20 | 0.77 | 4 | 33.6% | 0.38 | 0.59 | 54.2% | 52.8% | 37.2% | 48.0%/34.7% | 23.0 (interpolated) | pass | 0.116 (unverified) | -0.02 |
| 4 | `cfg_372d` | timeframe=15min, mean_type=sma, mean_lookback=80, std_lookback=80, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 0/122/0 | 122 | 14.8% | 2.8% | 0.85 | -4.2% | 347 | 1.59 | 2.2% | 55.0 | 9/9 | 0.78 | 0.56 | 0.29 | 3 | 6.8% | 0.52 | 0.68 | 13.8% | 12.8% | 4.6% | 13.9%/10.9% | 7.7 (interpolated) | pass | 0.057 (unverified) | 0.02 |
| 5 | `cfg_6d68` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 25/101/0 | 126 | 47.8% | 8.1% | 0.88 | -8.4% | 221 | 1.60 | 14.9% | 57.3 | 9/9 | 0.78 | 0.63 | 0.25 | 4 | 24.8% | 0.44 | 0.67 | 45.4% | 43.8% | 47.7% | 40.9%/26.4% | 19.3 (interpolated) | pass | 0.072 (unverified) | -0.10 |
| 6 | `cfg_adac` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=60, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 10/106/0 | 116 | 26.5% | 4.8% | 1.21 | -5.7% | 332 | 2.04 | 2.1% | 53.3 | 10/10 | 0.90 | 0.63 | 0.59 | 4 | 10.6% | 0.56 | 0.56 | 25.4% | 24.1% | 6.6% | 24.1%/18.9% | 13.0 (interpolated) | pass | 0.181 (unverified) | -0.55 |
| 7 | `cfg_39f4` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 24/94/0 | 118 | 50.7% | 8.6% | 0.91 | -11.3% | 221 | 1.56 | 13.9% | 54.3 | 9/9 | 0.56 | 0.29 | 0.62 | 4 | 30.5% | 0.37 | 0.63 | 48.9% | 46.9% | 33.6% | 41.8%/32.0% | 21.8 (interpolated) | pass | 0.091 (unverified) | -0.03 |
| 8 | `cfg_0b1c` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=60, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 0/116/0 | 116 | 25.6% | 4.7% | 1.18 | -5.7% | 332 | 2.01 | 2.1% | 53.4 | 11/11 | 0.91 | 0.69 | 0.49 | 4 | 9.7% | 0.58 | 0.58 | 24.4% | 23.2% | 6.0% | 23.0%/18.7% | 12.6 (interpolated) | pass | 0.156 (unverified) | -0.54 |
| 9 | `cfg_f567` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=80, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 21/92/0 | 113 | 14.0% | 2.7% | 0.81 | -4.3% | 318 | 1.56 | 2.0% | 51.2 | 10/10 | 0.80 | 0.58 | 0.22 | 3 | 6.9% | 0.52 | 0.71 | 13.3% | 12.4% | -4.1% | 12.9%/10.0% | 8.0 (interpolated) | pass | 0.048 (unverified) | -0.14 |
| 10 | `cfg_c4f3` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=80, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 32/70/0 | 102 | 15.9% | 3.0% | 0.88 | -3.1% | 284 | 1.66 | 1.8% | 46.5 | 9/9 | 0.78 | 0.51 | 0.36 | 5 | 9.5% | 0.37 | 0.69 | 15.0% | 13.8% | 2.8% | 15.0%/11.0% | 9.6 (interpolated) | pass | 0.064 (unverified) | -0.58 |
| 11 | `cfg_3ccc` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=80, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 14/88/0 | 102 | 15.4% | 2.9% | 0.86 | -3.1% | 284 | 1.64 | 1.8% | 46.4 | 10/10 | 0.90 | 0.57 | 0.29 | 5 | 9.2% | 0.40 | 0.71 | 14.7% | 13.7% | 2.9% | 14.2%/10.2% | 9.4 (interpolated) | pass | 0.059 (unverified) | -0.58 |
| 12 | `cfg_f9e4` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 30/98/0 | 128 | 40.2% | 7.0% | 0.76 | -11.1% | 271 | 1.46 | 15.2% | 58.7 | 9/9 | 0.89 | 0.49 | 0.26 | 3 | 22.8% | 0.40 | 0.77 | 39.2% | 38.7% | 33.2% | 38.4%/25.0% | 17.1 (interpolated) | pass | 0.042 (unverified) | -0.31 |
| 13 | `cfg_c7d5` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=80, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 12/131/0 | 143 | 15.6% | 2.9% | 0.83 | -3.4% | 282 | 1.49 | 2.6% | 64.4 | 9/9 | 0.89 | 0.55 | 0.28 | 4 | 7.8% | 0.49 | 0.71 | 14.1% | 12.8% | -2.7% | 13.5%/9.9% | 7.0 (interpolated) | pass | 0.052 (unverified) | -0.82 |
| 14 | `cfg_ec2b` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=30, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 8/168/0 | 176 | 17.5% | 3.3% | 0.81 | -5.6% | 337 | 1.45 | 3.2% | 79.7 | 11/11 | 0.82 | 0.34 | 0.47 | 4 | 8.8% | 0.47 | 0.71 | 15.7% | 14.0% | 10.1% | 15.5%/10.7% | 6.4 (interpolated) | pass | 0.043 (unverified) | -0.76 |
| 15 | `cfg_565d` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=30, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 15/161/0 | 176 | 17.5% | 3.3% | 0.81 | -5.6% | 337 | 1.45 | 3.2% | 79.6 | 11/11 | 0.82 | 0.34 | 0.46 | 4 | 8.9% | 0.46 | 0.71 | 15.7% | 14.0% | 10.2% | 16.1%/12.0% | 6.4 (interpolated) | pass | 0.043 (unverified) | -0.76 |
| 16 | `cfg_16f4` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=80, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 38/106/0 | 144 | 15.5% | 2.9% | 0.82 | -3.4% | 194 | 1.48 | 2.5% | 64.8 | 9/9 | 0.89 | 0.54 | 0.28 | 4 | 7.7% | 0.49 | 0.72 | 14.0% | 12.5% | -2.7% | 13.7%/10.7% | 6.9 (interpolated) | pass | 0.050 (unverified) | -0.81 |
| 17 | `cfg_055b` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=80, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 1/192/0 | 193 | 17.8% | 3.3% | 0.75 | -5.2% | 520 | 1.42 | 3.5% | 87.1 | 10/10 | 0.90 | 0.34 | 0.41 | 4 | 7.8% | 0.56 | 0.80 | 15.8% | 14.5% | 12.2% | 16.4%/11.1% | 6.0 (interpolated) | pass | 0.030 (unverified) | 0.01 |
| 18 | `cfg_1667` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=80, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 7/106/0 | 113 | 14.0% | 2.7% | 0.81 | -4.5% | 318 | 1.56 | 2.1% | 51.2 | 11/11 | 0.82 | 0.59 | 0.21 | 3 | 6.7% | 0.53 | 0.72 | 13.1% | 12.1% | -4.4% | 12.8%/10.3% | 7.9 (interpolated) | pass | 0.047 (unverified) | -0.07 |
| 19 | `cfg_d9e5` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 71/196/0 | 267 | 21.6% | 4.0% | 0.76 | -6.0% | 318 | 1.34 | 4.6% | 120.1 | 9/9 | 0.78 | 0.45 | 0.31 | 4 | 6.8% | 0.65 | 0.67 | 18.6% | 16.0% | 3.8% | 19.3%/13.6% | 5.4 (interpolated) | pass | 0.032 (unverified) | -0.21 |
| 20 | `cfg_11d7` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 228/300/0 | 528 | 44.7% | 7.7% | 0.75 | -15.9% | 556 | 1.25 | 14.9% | 239.7 | 10/10 | 0.70 | 0.32 | 0.43 | 4 | 19.1% | 0.57 | 0.58 | 37.9% | 32.1% | 55.0% | 36.0%/22.2% | 5.1 (interpolated) | pass | 0.042 (unverified) | 0.01 |
| 21 | `cfg_d7ac` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 211/355/0 | 566 | 48.9% | 8.3% | 0.76 | -23.3% | 552 | 1.23 | 16.3% | 257.0 | 10/10 | 0.70 | 0.26 | 0.50 | 3 | 5.6% | 0.80 | 0.62 | 40.7% | 37.1% | 57.8% | 40.4%/29.9% | 5.2 (interpolated) | pass | 0.040 (unverified) | -0.23 |
| 22 | `cfg_f0c4` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=60, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 12/64/56 | 132 | 13.6% | 2.6% | 0.85 | -4.2% | 365 | 1.50 | 1.7% | 59.7 | 10/10 | 0.90 | 0.42 | 0.43 | 3 | 6.0% | 0.57 | 0.80 | 12.4% | 10.7% | -5.4% | 12.7%/8.8% | 6.8 (interpolated) | pass | 0.053 (unverified) | -0.88 |
| 23 | `cfg_1781` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=60, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 3/73/56 | 132 | 13.5% | 2.6% | 0.85 | -4.2% | 365 | 1.50 | 1.7% | 59.8 | 11/11 | 0.91 | 0.46 | 0.39 | 3 | 5.9% | 0.57 | 0.80 | 12.1% | 10.5% | -5.6% | 12.0%/9.2% | 6.8 (interpolated) | pass | 0.051 (unverified) | -0.90 |
| 24 | `cfg_c8e3` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 293/346/0 | 639 | 58.5% | 9.7% | 0.76 | -17.8% | 344 | 1.21 | 17.5% | 291.8 | 11/11 | 0.73 | 0.25 | 0.51 | 3 | 15.4% | 0.67 | 0.61 | 48.5% | 41.3% | 28.6% | 50.6%/34.9% | 5.2 (interpolated) | pass | 0.048 (unverified) | 0.27 |
| 25 | `cfg_d774` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 19/78/17 | 114 | 18.7% | 3.5% | 0.75 | -4.8% | 238 | 1.41 | 6.9% | 51.5 | 9/9 | 1.00 | 0.58 | 0.17 | 4 | 7.5% | 0.60 | 0.83 | 17.5% | 16.3% | 6.7% | 16.9%/11.7% | 10.2 (interpolated) | pass | 0.041 (unverified) | 0.36 |
| 26 | `cfg_ad11` | timeframe=15min, mean_type=ema, mean_lookback=60, std_lookback=80, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 7/57/41 | 105 | 12.2% | 2.3% | 0.78 | -3.8% | 324 | 1.52 | 1.4% | 47.6 | 9/9 | 0.89 | 0.45 | 0.33 | 4 | 6.4% | 0.46 | 0.88 | 11.3% | 10.2% | -6.0% | 11.3%/7.4% | 7.8 (interpolated) | pass | 0.039 (unverified) | -0.13 |
| 27 | `cfg_0f33` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 126/385/0 | 511 | 36.7% | 6.5% | 0.86 | -10.3% | 298 | 1.30 | 8.7% | 232.3 | 10/10 | 0.60 | 0.20 | 0.67 | 4 | 6.4% | 0.81 | 0.76 | 30.9% | 24.9% | 10.0% | 30.5%/21.7% | 4.7 (interpolated) | pass | 0.067 (unverified) | -0.65 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | -3.0% / -0.33 / 31 | 9.3% / 1.47 / 22 | 7.8% / 0.63 / 20 | 19.0% / 2.20 / 21 | 10.8% / 1.02 / 32 |
| 2 | 3.5% / 1.37 / 26 | -0.1% / -0.03 / 21 | 7.5% / 1.85 / 24 | 5.5% / 1.41 / 35 | -1.7% / -0.40 / 16 |
| 3 | -0.1% / 0.02 / 27 | 12.9% / 2.01 / 18 | 10.3% / 0.87 / 17 | 17.1% / 1.81 / 22 | 7.4% / 0.65 / 34 |
| 4 | 3.4% / 1.35 / 26 | -0.1% / -0.03 / 21 | 7.5% / 1.85 / 24 | 5.0% / 1.32 / 35 | -1.6% / -0.38 / 16 |
| 5 | -3.2% / -0.37 / 31 | 9.1% / 1.44 / 22 | 7.5% / 0.63 / 20 | 18.4% / 2.16 / 21 | 10.0% / 0.96 / 32 |
| 6 | 1.4% / 0.71 / 18 | 1.2% / 0.77 / 17 | 14.4% / 2.12 / 26 | 11.7% / 2.51 / 32 | -3.5% / -1.13 / 23 |
| 7 | -1.0% / -0.09 / 27 | 12.7% / 1.97 / 18 | 9.0% / 0.79 / 17 | 15.5% / 1.66 / 22 | 7.3% / 0.65 / 34 |
| 8 | 1.1% / 0.56 / 18 | 1.2% / 0.77 / 17 | 14.6% / 2.14 / 26 | 11.2% / 2.42 / 32 | -3.5% / -1.13 / 23 |
| 9 | 2.0% / 1.09 / 23 | -0.7% / -0.35 / 18 | 6.7% / 1.68 / 26 | 6.7% / 1.80 / 27 | -1.2% / -0.25 / 19 |
| 10 | 1.6% / 0.73 / 17 | 0.5% / 0.22 / 19 | 5.8% / 1.44 / 24 | 5.4% / 1.38 / 22 | 1.8% / 0.44 / 20 |
| 11 | 2.1% / 0.93 / 17 | 0.7% / 0.28 / 19 | 4.8% / 1.24 / 24 | 5.7% / 1.42 / 22 | 1.4% / 0.36 / 20 |
| 12 | -1.2% / -0.15 / 28 | -0.3% / -0.03 / 22 | 15.6% / 1.33 / 20 | 14.1% / 1.33 / 27 | 7.8% / 0.69 / 31 |
| 13 | 2.8% / 1.08 / 32 | 2.7% / 1.27 / 26 | 7.3% / 1.67 / 30 | 3.4% / 0.89 / 32 | -1.3% / -0.26 / 23 |
| 14 | -0.2% / -0.08 / 27 | 2.5% / 1.03 / 33 | 8.0% / 1.31 / 46 | 6.2% / 1.53 / 41 | 0.1% / 0.05 / 29 |
| 15 | -0.1% / -0.01 / 27 | 2.5% / 1.03 / 33 | 7.9% / 1.29 / 46 | 6.2% / 1.53 / 41 | 0.1% / 0.05 / 29 |
| 16 | 2.6% / 1.00 / 32 | 2.3% / 1.16 / 27 | 7.2% / 1.65 / 30 | 3.5% / 0.92 / 32 | -0.9% / -0.17 / 23 |
| 17 | -2.4% / -0.81 / 41 | 1.0% / 0.51 / 32 | 8.9% / 1.32 / 44 | 9.3% / 1.99 / 46 | 0.3% / 0.10 / 30 |
| 18 | 2.2% / 1.15 / 23 | -0.4% / -0.23 / 18 | 6.9% / 1.68 / 26 | 6.9% / 1.83 / 27 | -1.9% / -0.42 / 19 |
| 19 | 1.1% / 0.29 / 65 | 0.5% / 0.20 / 40 | 13.9% / 1.71 / 58 | 8.0% / 1.36 / 60 | -2.7% / -0.52 / 44 |
| 20 | -6.7% / -0.98 / 102 | 2.1% / 0.45 / 99 | 24.4% / 1.32 / 98 | 21.5% / 2.20 / 118 | 0.4% / 0.09 / 111 |
| 21 | -7.4% / -1.05 / 109 | 2.9% / 0.57 / 107 | 41.0% / 1.94 / 105 | 13.8% / 1.35 / 130 | -2.5% / -0.20 / 115 |
| 22 | 1.2% / 0.83 / 17 | -0.6% / -0.30 / 29 | 7.5% / 1.74 / 29 | 7.1% / 2.04 / 36 | -1.9% / -0.55 / 21 |
| 23 | 1.0% / 0.72 / 17 | -0.6% / -0.28 / 29 | 7.5% / 1.74 / 29 | 7.1% / 2.04 / 36 | -1.9% / -0.55 / 21 |
| 24 | -4.9% / -0.70 / 120 | 11.1% / 1.86 / 121 | 37.3% / 1.48 / 127 | 16.5% / 1.55 / 142 | -6.2% / -0.45 / 129 |
| 25 | 5.1% / 1.21 / 32 | 2.7% / 0.88 / 17 | -0.6% / -0.10 / 17 | 10.4% / 1.49 / 30 | 0.2% / 0.06 / 18 |
| 26 | 1.6% / 1.10 / 15 | 0.7% / 0.49 / 16 | 5.5% / 1.33 / 18 | 5.2% / 1.60 / 31 | -1.1% / -0.28 / 25 |
| 27 | -0.1% / -0.01 / 91 | 4.5% / 1.37 / 95 | 28.5% / 1.98 / 104 | 1.0% / 0.21 / 114 | 0.9% / 0.16 / 107 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_f567` | 4 | 1.00 | 0.99/0.99 | 0.98/0.98 |
| 1 | `cfg_8fea` | 5 | 0.86 | 0.84/0.91 | 0.65/0.81 |
| 2 | `cfg_055b` | 2 | 0.82 | 0.72/0.72 | 0.36/0.36 |
| 3 | `cfg_ec2b` | 7 | 0.89 | 0.84/0.92 | 0.46/0.72 |
| 4 | `cfg_adac` | 11 | 0.86 | 0.72/0.94 | 0.50/0.76 |
| 5 | `cfg_0f33` | 1 | n/a | n/a/n/a | n/a/n/a |
| 6 | `cfg_11d7` | 2 | 0.80 | 0.78/0.78 | 0.59/0.59 |
| 7 | `cfg_f0c4` | 4 | 1.00 | 1.00/1.00 | 0.98/0.98 |
| 8 | `cfg_c4f3` | 6 | 0.89 | 0.90/0.99 | 0.78/0.96 |
| 9 | `cfg_c7d5` | 3 | 0.98 | 0.99/0.99 | 0.97/0.98 |
| 10 | `cfg_cac3` | 8 | 0.80 | 0.84/0.84 | 0.48/0.48 |
| 11 | `cfg_d785` | 4 | 0.89 | 0.92/0.97 | 0.90/0.96 |
| 12 | `cfg_ad11` | 1 | n/a | n/a/n/a | n/a/n/a |
| 13 | `cfg_c8e3` | 1 | n/a | n/a/n/a | n/a/n/a |
| 14 | `cfg_d774` | 1 | n/a | n/a/n/a | n/a/n/a |
| 15 | `cfg_f9e4` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 8.239e-04 over 41088 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1297.0, participation ratio 23.1, 95%-variance components 316 (rank bound T = 1259); raw grid 41472; raw + known prior 513960
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
