# Screening funnel -- mr_ym_v5 (development stages only)

- Code: `5342a94cdc84` (dirty working tree: True, diff sha256 `1dcfc89b166d`)
- Config: `configs/funnel/mr_funnel_ym_v5.yaml` sha256 `ab0047304657cdd1`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'YM': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `b53bf80f16a8eb62` (61 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **False** -- No strategy has been selected on YM 2023-2024. But YM is correlated with ES/NQ, and this v5 grid and the 40-trade validation rule were chosen after reading ES 2023-2024 results (mr_es_v3..v5) and run alongside NQ (mr_nq_v5). So the slice is not fully independent of earlier research.
- Holdout 2025+ previously inspected: **False** -- No YM strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 41472 | 41472 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 41472 | 41472 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 41472 | 29921 | 11551 | 0 |  | 32651 | 72.15 | 72.15 |  |
| 3 performance & risk | hard_gate | 29921 | 127 | 29794 | 0 |  | 0 | 0.31 | 0.42 |  |
| 4 parameter stability | hard_gate | 127 | 122 | 5 | 0 |  | 0 | 0.29 | 96.06 |  |
| 5 time stability | hard_gate | 122 | 121 | 1 | 0 |  | 96 | 0.29 | 99.18 |  |
| 6 deduplication | dedup | 121 | 61 |  |  | 60 |  | 0.15 | 50.41 | best 2 per cluster |
| 7 execution stress | hard_gate | 61 | 61 | 0 | 0 |  | 12 | 0.15 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 61 |  |  |  |  |  |  |  | diagnostic only: unverified: 61 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 11551 |
| s2:hard_reject:years_with_>=10_trades | 7682 |
| s3:hard_reject:max_drawdown | 2745 |
| s3:hard_reject:net_return | 23365 |
| s3:hard_reject:sharpe | 29794 |
| s4:hard_reject:local_median_sharpe | 5 |
| s5:hard_reject:profitable_years | 1 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_7fa2` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 45/22/35 | 102 | 59.2% | 9.8% | 1.40 | -6.9% | 189 | 2.59 | 4.7% | 46.5 | 9/9 | 0.78 | 0.82 | 0.58 | 5 | 30.3% | 0.43 | 0.53 | 58.9% | 58.3% | 18.9% | 51.6%/41.3% | n/a (profitable_beyond_25.0x) | pass | 0.168 (unverified) | 0.81 |
| 2 | `cfg_afcf` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 60/2/45 | 107 | 53.3% | 8.9% | 1.20 | -10.1% | 154 | 2.12 | 5.4% | 48.2 | 9/9 | 0.78 | 0.73 | 0.47 | 4 | 29.8% | 0.39 | 0.56 | 52.1% | 51.4% | 16.7% | 46.2%/37.3% | n/a (profitable_beyond_25.0x) | pass | 0.088 (unverified) | 0.86 |
| 3 | `cfg_902b` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 45/38/57 | 140 | 43.2% | 7.5% | 1.03 | -6.0% | 190 | 1.83 | 6.2% | 61.6 | 9/9 | 0.89 | 0.65 | 0.38 | 5 | 16.9% | 0.54 | 0.67 | 42.5% | 41.3% | 12.0% | 39.7%/28.7% | n/a (profitable_beyond_25.0x) | pass | 0.032 (unverified) | 0.72 |
| 4 | `cfg_0544` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 34/57/20 | 111 | 22.8% | 4.2% | 1.27 | -2.7% | 248 | 2.32 | 1.7% | 49.6 | 11/11 | 0.64 | 0.59 | 0.68 | 4 | 9.9% | 0.55 | 0.42 | 21.9% | 21.3% | 16.1% | 20.4%/16.8% | 19.0 (interpolated) | pass | 0.081 (unverified) | 0.52 |
| 5 | `cfg_eade` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 29/57/63 | 149 | 31.3% | 5.6% | 1.01 | -4.7% | 326 | 1.57 | 7.0% | 65.8 | 8/8 | 1.00 | 0.67 | 0.33 | 5 | 19.7% | 0.33 | 0.61 | 30.3% | 28.3% | -9.9% | 26.7%/21.0% | 19.0 (interpolated) | pass | 0.038 (unverified) | 0.06 |
| 6 | `cfg_0646` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 10/74/65 | 149 | 34.4% | 6.1% | 1.06 | -5.2% | 326 | 1.62 | 7.4% | 65.9 | 9/9 | 1.00 | 0.71 | 0.35 | 5 | 20.2% | 0.37 | 0.63 | 33.5% | 31.8% | -7.5% | 30.6%/21.7% | 20.8 (interpolated) | pass | 0.047 (unverified) | 0.09 |
| 7 | `cfg_c591` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 48/60/65 | 173 | 32.3% | 5.8% | 1.00 | -6.5% | 268 | 1.49 | 8.2% | 76.8 | 7/7 | 0.86 | 0.71 | 0.29 | 5 | 21.6% | 0.27 | 0.52 | 31.4% | 30.3% | -4.9% | 30.2%/24.5% | 17.2 (interpolated) | pass | 0.043 (unverified) | 0.71 |
| 8 | `cfg_95c0` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 30/65/20 | 115 | 29.9% | 5.4% | 1.00 | -5.0% | 234 | 1.60 | 6.9% | 50.3 | 9/9 | 0.89 | 0.52 | 0.48 | 4 | 13.2% | 0.49 | 0.64 | 29.2% | 28.3% | 8.3% | 25.6%/19.4% | 23.1 (interpolated) | pass | 0.038 (unverified) | 0.25 |
| 9 | `cfg_237a` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 39/47/61 | 147 | 45.5% | 7.8% | 0.96 | -9.3% | 279 | 1.68 | 7.1% | 67.0 | 9/9 | 0.89 | 0.72 | 0.24 | 5 | 28.7% | 0.37 | 0.61 | 44.0% | 41.4% | 3.9% | 38.9%/30.1% | n/a (profitable_beyond_25.0x) | pass | 0.028 (unverified) | 0.54 |
| 10 | `cfg_ef6a` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 10/68/62 | 140 | 37.3% | 6.6% | 0.89 | -6.1% | 292 | 1.69 | 7.0% | 62.3 | 9/9 | 0.89 | 0.69 | 0.20 | 5 | 13.7% | 0.57 | 0.76 | 36.1% | 34.9% | 4.3% | 32.8%/23.3% | 22.6 (interpolated) | pass | 0.014 (unverified) | 0.82 |
| 11 | `cfg_3534` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 24/61/60 | 145 | 44.2% | 7.6% | 0.90 | -10.9% | 279 | 1.68 | 7.3% | 66.0 | 8/8 | 0.88 | 0.51 | 0.39 | 5 | 27.7% | 0.37 | 0.63 | 41.9% | 41.0% | 3.1% | 38.0%/29.9% | 24.9 (interpolated) | pass | 0.025 (unverified) | 0.58 |
| 12 | `cfg_49c6` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 48/46/55 | 149 | 38.3% | 6.7% | 0.90 | -5.8% | 273 | 1.47 | 12.8% | 66.5 | 10/10 | 0.80 | 0.53 | 0.38 | 4 | 22.4% | 0.39 | 0.74 | 38.2% | 36.8% | 35.7% | 35.1%/25.0% | 23.2 (interpolated) | pass | 0.025 (unverified) | 0.58 |
| 13 | `cfg_08d4` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 35/47/60 | 142 | 32.1% | 5.7% | 0.82 | -9.8% | 311 | 1.60 | 6.8% | 62.7 | 9/9 | 1.00 | 0.63 | 0.19 | 5 | 15.5% | 0.48 | 0.77 | 30.9% | 30.2% | -5.6% | 30.0%/21.5% | 20.4 (interpolated) | pass | 0.010 (unverified) | 0.62 |
| 14 | `cfg_5545` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 26/63/21 | 110 | 18.9% | 3.5% | 1.14 | -2.9% | 248 | 2.03 | 1.7% | 48.7 | 12/12 | 0.67 | 0.67 | 0.47 | 4 | 7.9% | 0.57 | 0.48 | 18.3% | 17.7% | 13.9% | 16.5%/13.7% | 17.0 (interpolated) | pass | 0.048 (unverified) | 0.58 |
| 15 | `cfg_cdde` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 63/32/54 | 149 | 36.4% | 6.4% | 0.87 | -6.0% | 299 | 1.47 | 12.0% | 65.6 | 11/11 | 0.82 | 0.60 | 0.27 | 4 | 21.7% | 0.38 | 0.71 | 35.6% | 34.7% | 33.5% | 33.8%/24.5% | 22.2 (interpolated) | pass | 0.021 (unverified) | 0.73 |
| 16 | `cfg_bf79` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 19/43/41 | 103 | 45.8% | 7.8% | 1.17 | -5.4% | 153 | 2.16 | 5.0% | 46.6 | 10/10 | 1.00 | 0.75 | 0.42 | 5 | 17.7% | 0.59 | 0.60 | 44.1% | 43.4% | -1.5% | 40.2%/32.1% | n/a (profitable_beyond_25.0x) | pass | 0.047 (unverified) | 0.45 |
| 17 | `cfg_a317` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 43/23/36 | 102 | 35.6% | 6.3% | 0.86 | -4.9% | 276 | 1.70 | 8.4% | 45.1 | 11/11 | 1.00 | 0.49 | 0.37 | 5 | 14.9% | 0.55 | 0.77 | 35.1% | 34.1% | 28.5% | 31.3%/22.1% | n/a (profitable_beyond_25.0x) | pass | 0.013 (unverified) | 0.39 |
| 18 | `cfg_204e` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 21/81/64 | 166 | 23.2% | 4.3% | 0.77 | -6.4% | 290 | 1.37 | 8.5% | 73.5 | 8/8 | 0.88 | 0.64 | 0.13 | 4 | 13.9% | 0.35 | 0.71 | 22.3% | 20.5% | -10.0% | 21.3%/14.6% | 13.0 (interpolated) | pass | 0.014 (unverified) | 0.69 |
| 19 | `cfg_c34b` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=60, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 13/42/46 | 101 | 16.2% | 3.1% | 0.86 | -3.6% | 270 | 1.61 | 4.7% | 44.0 | 10/10 | 0.90 | 0.56 | 0.30 | 4 | 7.9% | 0.51 | 0.89 | 15.5% | 15.1% | 21.6% | 14.3%/9.9% | 16.1 (interpolated) | pass | 0.023 (unverified) | 0.57 |
| 20 | `cfg_f560` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 72/35/54 | 161 | 53.7% | 9.0% | 0.89 | -12.2% | 316 | 1.60 | 13.3% | 71.4 | 12/12 | 0.83 | 0.50 | 0.39 | 5 | 29.0% | 0.36 | 0.57 | 52.4% | 51.3% | 42.1% | 46.8%/36.6% | n/a (profitable_beyond_25.0x) | pass | 0.029 (unverified) | 0.42 |
| 21 | `cfg_e30c` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 28/37/37 | 102 | 35.0% | 6.2% | 0.85 | -5.2% | 276 | 1.69 | 9.1% | 45.2 | 10/10 | 1.00 | 0.42 | 0.43 | 5 | 16.3% | 0.50 | 0.71 | 34.5% | 33.9% | 29.1% | 32.4%/23.3% | n/a (profitable_beyond_25.0x) | pass | 0.013 (unverified) | 0.43 |
| 22 | `cfg_732d` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 69/6/81 | 156 | 41.2% | 7.2% | 0.84 | -8.3% | 255 | 1.56 | 8.0% | 69.7 | 9/9 | 0.89 | 0.69 | 0.16 | 4 | 15.9% | 0.56 | 0.71 | 40.6% | 38.9% | 13.0% | 37.6%/26.3% | 23.4 (interpolated) | pass | 0.017 (unverified) | 0.46 |
| 23 | `cfg_0b90` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 36/72/69 | 177 | 25.9% | 4.7% | 0.78 | -6.7% | 405 | 1.41 | 8.5% | 77.8 | 9/9 | 0.89 | 0.49 | 0.29 | 5 | 17.8% | 0.28 | 0.75 | 24.9% | 23.8% | -8.9% | 22.9%/14.3% | 13.8 (interpolated) | pass | 0.014 (unverified) | 0.02 |
| 24 | `cfg_904f` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=60, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 24/20/60 | 104 | 26.6% | 4.8% | 0.80 | -7.5% | 436 | 1.59 | 6.8% | 45.2 | 11/11 | 0.91 | 0.58 | 0.22 | 4 | 16.0% | 0.37 | 0.97 | 26.1% | 25.5% | 25.2% | 23.1%/14.8% | 23.7 (interpolated) | pass | 0.018 (unverified) | 0.35 |
| 25 | `cfg_cee9` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 4/89/61 | 154 | 20.4% | 3.8% | 0.80 | -5.4% | 307 | 1.39 | 8.0% | 68.6 | 8/8 | 0.75 | 0.59 | 0.21 | 5 | 13.8% | 0.31 | 0.85 | 19.6% | 18.8% | -7.6% | 19.6%/14.2% | 13.5 (interpolated) | pass | 0.017 (unverified) | 0.26 |
| 26 | `cfg_2ec9` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 7/87/60 | 154 | 20.7% | 3.8% | 0.81 | -5.5% | 307 | 1.40 | 7.9% | 68.6 | 9/9 | 0.78 | 0.62 | 0.19 | 5 | 14.1% | 0.31 | 0.84 | 19.8% | 19.0% | -9.2% | 20.2%/13.9% | 13.7 (interpolated) | pass | 0.018 (unverified) | 0.26 |
| 27 | `cfg_1851` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 29/39/53 | 121 | 13.5% | 2.6% | 1.08 | -2.0% | 248 | 1.72 | 1.5% | 53.8 | 10/10 | 0.60 | 0.39 | 0.69 | 4 | 8.3% | 0.36 | 0.58 | 12.8% | 12.2% | 15.3% | 12.0%/8.6% | 10.9 (interpolated) | pass | 0.045 (unverified) | -0.24 |
| 28 | `cfg_0631` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 46/28/105 | 179 | 30.3% | 5.4% | 0.81 | -8.6% | 183 | 1.38 | 11.1% | 79.2 | 9/9 | 0.78 | 0.45 | 0.36 | 5 | 18.4% | 0.33 | 0.89 | 29.3% | 28.4% | 31.4% | 26.7%/19.6% | 15.6 (interpolated) | pass | 0.015 (unverified) | 0.66 |
| 29 | `cfg_bc15` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 80/14/39 | 133 | 40.7% | 7.1% | 0.77 | -14.7% | 323 | 1.56 | 9.0% | 59.4 | 10/10 | 0.90 | 0.45 | 0.33 | 4 | 20.5% | 0.44 | 0.66 | 39.7% | 37.6% | 11.3% | 34.9%/26.5% | n/a (profitable_beyond_25.0x) | pass | 0.017 (unverified) | 0.67 |
| 30 | `cfg_55ca` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 55/39/63 | 157 | 20.4% | 3.8% | 0.82 | -6.0% | 369 | 1.43 | 7.4% | 69.7 | 8/8 | 0.75 | 0.62 | 0.20 | 4 | 9.4% | 0.54 | 0.65 | 19.6% | 19.0% | 0.8% | 17.5%/12.3% | 12.7 (interpolated) | pass | 0.019 (unverified) | 0.77 |
| 31 | `cfg_dcae` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 8/86/24 | 118 | 30.7% | 5.5% | 0.95 | -6.7% | 234 | 1.58 | 7.4% | 51.7 | 10/10 | 0.90 | 0.51 | 0.44 | 5 | 14.7% | 0.45 | 0.72 | 29.7% | 29.1% | 7.9% | 25.9%/19.3% | 23.0 (interpolated) | pass | 0.031 (unverified) | 0.32 |
| 32 | `cfg_433b` | timeframe=1h, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 92/45/74 | 211 | 45.5% | 7.8% | 0.80 | -11.6% | 241 | 1.38 | 17.0% | 94.4 | 10/10 | 0.80 | 0.42 | 0.38 | 4 | 23.9% | 0.38 | 0.65 | 43.0% | 41.3% | 48.7% | 38.3%/26.6% | 18.4 (interpolated) | pass | 0.018 (unverified) | 0.61 |
| 33 | `cfg_0ee6` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 99/11/56 | 166 | 47.2% | 8.0% | 0.88 | -14.3% | 170 | 1.55 | 11.4% | 73.6 | 11/11 | 0.91 | 0.44 | 0.44 | 5 | 24.6% | 0.38 | 0.53 | 46.2% | 45.4% | 43.7% | 43.4%/34.3% | 24.4 (interpolated) | pass | 0.027 (unverified) | 0.34 |
| 34 | `cfg_f175` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=60, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 0/67/43 | 110 | 30.6% | 5.5% | 0.85 | -7.7% | 307 | 1.74 | 6.0% | 48.7 | 9/9 | 0.89 | 0.64 | 0.22 | 4 | 15.9% | 0.44 | 0.69 | 29.9% | 28.4% | 0.5% | 27.9%/21.3% | 24.4 (interpolated) | pass | 0.011 (unverified) | 0.12 |
| 35 | `cfg_3fa2` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=60, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 0/67/43 | 110 | 30.6% | 5.5% | 0.85 | -7.7% | 307 | 1.74 | 6.0% | 48.7 | 8/8 | 0.88 | 0.63 | 0.23 | 4 | 15.9% | 0.44 | 0.69 | 29.9% | 28.4% | 0.5% | 26.7%/21.4% | 24.4 (interpolated) | pass | 0.011 (unverified) | 0.15 |
| 36 | `cfg_8786` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=60, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 5/49/46 | 100 | 15.1% | 2.9% | 0.81 | -3.6% | 313 | 1.57 | 4.7% | 43.6 | 11/11 | 0.91 | 0.61 | 0.20 | 4 | 7.0% | 0.54 | 0.94 | 14.6% | 14.2% | 21.3% | 14.2%/8.6% | 15.6 (interpolated) | pass | 0.015 (unverified) | 0.46 |
| 37 | `cfg_2e7d` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 78/68/0 | 146 | 37.9% | 6.6% | 0.88 | -8.9% | 179 | 1.61 | 14.1% | 64.2 | 8/8 | 1.00 | 0.39 | 0.49 | 4 | 22.5% | 0.41 | 0.48 | 36.6% | 35.6% | 43.3% | 33.8%/27.4% | 22.9 (interpolated) | pass | 0.027 (unverified) | 0.10 |
| 38 | `cfg_e15f` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 16/133/38 | 187 | 25.0% | 4.6% | 0.89 | -6.2% | 241 | 1.61 | 3.0% | 82.7 | 11/11 | 0.82 | 0.35 | 0.55 | 4 | 5.5% | 0.78 | 0.62 | 23.8% | 22.7% | 7.2% | 22.3%/15.3% | 12.9 (interpolated) | pass | 0.017 (unverified) | 0.77 |
| 39 | `cfg_5413` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 21/128/38 | 187 | 25.7% | 4.7% | 0.91 | -6.1% | 241 | 1.63 | 3.0% | 82.6 | 12/12 | 0.83 | 0.37 | 0.54 | 4 | 5.3% | 0.79 | 0.63 | 24.6% | 23.6% | 7.4% | 22.4%/14.9% | 13.4 (interpolated) | pass | 0.018 (unverified) | 0.77 |
| 40 | `cfg_aadb` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 46/11/72 | 129 | 10.7% | 2.0% | 0.79 | -3.4% | 248 | 1.44 | 1.9% | 57.4 | 10/10 | 0.80 | 0.25 | 0.54 | 4 | 5.2% | 0.49 | 0.75 | 9.9% | 9.3% | 15.0% | 9.2%/6.9% | 8.8 (interpolated) | pass | 0.012 (unverified) | -0.12 |
| 41 | `cfg_2a39` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 30/66/26 | 122 | 22.4% | 4.1% | 0.78 | -6.1% | 329 | 1.44 | 7.0% | 54.3 | 9/9 | 0.67 | 0.27 | 0.52 | 4 | 11.3% | 0.48 | 0.70 | 21.1% | 19.4% | 21.0% | 18.9%/11.0% | 17.0 (interpolated) | pass | 0.012 (unverified) | 0.48 |
| 42 | `cfg_3871` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=40, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 74/35/83 | 192 | 23.8% | 4.4% | 0.98 | -4.7% | 154 | 1.43 | 8.2% | 84.9 | 8/8 | 0.75 | 0.51 | 0.47 | 4 | 12.3% | 0.43 | 0.60 | 22.7% | 21.7% | 9.3% | 19.2%/13.9% | 11.5 (interpolated) | pass | 0.040 (unverified) | -0.07 |
| 43 | `cfg_5a90` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=40, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 57/71/0 | 128 | 36.9% | 6.5% | 0.80 | -12.9% | 155 | 1.53 | 13.5% | 57.3 | 10/10 | 0.90 | 0.47 | 0.33 | 4 | 15.8% | 0.63 | 0.69 | 35.8% | 35.0% | 33.3% | 34.2%/21.9% | 24.9 (interpolated) | pass | 0.013 (unverified) | 0.25 |
| 44 | `cfg_f434` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=80, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 40/16/82 | 138 | 25.8% | 4.7% | 0.75 | -6.4% | 258 | 1.47 | 8.3% | 60.0 | 9/9 | 0.89 | 0.46 | 0.30 | 5 | 11.2% | 0.54 | 0.91 | 25.2% | 24.7% | 19.1% | 24.2%/13.6% | 17.4 (interpolated) | pass | 0.010 (unverified) | 0.48 |
| 45 | `cfg_ffb5` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 56/139/0 | 195 | 19.0% | 3.5% | 0.81 | -4.1% | 241 | 1.53 | 3.4% | 85.2 | 10/10 | 0.80 | 0.55 | 0.26 | 4 | 10.0% | 0.45 | 0.52 | 17.9% | 16.8% | 31.0% | 16.8%/13.2% | 10.2 (interpolated) | pass | 0.019 (unverified) | 0.91 |
| 46 | `cfg_f72c` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 11/76/71 | 158 | 28.3% | 5.1% | 0.76 | -6.5% | 197 | 1.43 | 7.6% | 70.4 | 10/10 | 0.90 | 0.52 | 0.24 | 5 | 17.5% | 0.36 | 0.76 | 27.7% | 26.0% | -11.8% | 26.0%/17.6% | 16.8 (interpolated) | pass | 0.011 (unverified) | -0.03 |
| 47 | `cfg_6236` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 59/23/33 | 115 | 16.2% | 3.1% | 0.81 | -5.9% | 238 | 1.59 | 2.3% | 50.7 | 11/11 | 0.73 | 0.28 | 0.53 | 4 | 6.5% | 0.60 | 0.59 | 15.6% | 14.9% | 16.2% | 14.5%/11.6% | 14.3 (interpolated) | pass | 0.013 (unverified) | -0.09 |
| 48 | `cfg_9dba` | timeframe=1h, mean_type=sma, mean_lookback=20, std_lookback=40, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 102/0/90 | 192 | 27.1% | 4.9% | 0.92 | -5.2% | 170 | 1.41 | 8.8% | 85.9 | 8/8 | 0.88 | 0.45 | 0.48 | 3 | 10.6% | 0.62 | 0.58 | 26.2% | 24.9% | 9.8% | 23.8%/16.5% | 13.7 (interpolated) | pass | 0.034 (unverified) | -0.20 |
| 49 | `cfg_d557` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 31/164/0 | 195 | 21.1% | 3.9% | 0.88 | -4.1% | 172 | 1.58 | 3.5% | 85.5 | 11/11 | 0.82 | 0.52 | 0.36 | 4 | 11.8% | 0.41 | 0.50 | 20.1% | 18.9% | 25.8% | 19.1%/14.7% | 11.3 (interpolated) | pass | 0.026 (unverified) | 0.91 |
| 50 | `cfg_e8be` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 330/180/0 | 510 | 40.5% | 7.0% | 0.76 | -10.3% | 331 | 1.29 | 12.8% | 226.7 | 11/11 | 0.91 | 0.46 | 0.29 | 3 | 6.7% | 0.77 | 0.52 | 38.2% | 35.4% | 30.7% | 36.5%/26.7% | 7.9 (interpolated) | pass | 0.018 (unverified) | 0.11 |
| 51 | `cfg_391b` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=10, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 51/86/0 | 137 | 34.7% | 6.1% | 0.79 | -8.9% | 254 | 1.53 | 14.8% | 60.3 | 9/9 | 0.78 | 0.35 | 0.44 | 4 | 19.8% | 0.43 | 0.58 | 33.7% | 32.9% | 40.7% | 30.7%/22.6% | 22.2 (interpolated) | pass | 0.016 (unverified) | -0.05 |
| 52 | `cfg_363c` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=25, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 125/288/0 | 413 | 45.1% | 7.7% | 1.03 | -7.5% | 206 | 1.39 | 12.3% | 184.9 | 11/11 | 0.91 | 0.33 | 0.69 | 4 | 26.7% | 0.37 | 0.39 | 42.7% | 40.2% | 35.6% | 39.2%/29.3% | 10.4 (interpolated) | pass | 0.047 (unverified) | 0.14 |
| 53 | `cfg_a86e` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=25, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 78/85/0 | 163 | 35.7% | 6.3% | 0.75 | -11.3% | 163 | 1.42 | 17.1% | 71.9 | 10/10 | 0.90 | 0.53 | 0.22 | 3 | 18.0% | 0.51 | 0.71 | 34.8% | 34.2% | 33.1% | 35.2%/25.3% | 20.4 (interpolated) | pass | 0.011 (unverified) | 0.27 |
| 54 | `cfg_43ed` | timeframe=15min, mean_type=sma, mean_lookback=60, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 68/341/0 | 409 | 50.4% | 8.5% | 1.08 | -6.9% | 203 | 1.43 | 12.9% | 183.3 | 10/10 | 0.90 | 0.31 | 0.77 | 5 | 32.1% | 0.36 | 0.36 | 48.1% | 43.6% | 36.0% | 42.1%/35.6% | 11.0 (interpolated) | pass | 0.059 (unverified) | 0.10 |
| 55 | `cfg_d18c` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 130/404/0 | 534 | 26.6% | 4.8% | 0.89 | -8.3% | 335 | 1.26 | 9.1% | 235.0 | 10/10 | 0.60 | 0.19 | 0.70 | 3 | 4.3% | 0.78 | 0.59 | 23.3% | 20.1% | 4.3% | 23.3%/16.5% | 5.6 (interpolated) | pass | 0.025 (unverified) | -0.13 |
| 56 | `cfg_f9bd` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 40/64/0 | 104 | 42.6% | 7.4% | 0.88 | -10.6% | 173 | 1.84 | 11.2% | 46.0 | 10/10 | 0.90 | 0.44 | 0.44 | 5 | 24.8% | 0.34 | 0.51 | 40.7% | 40.5% | 29.1% | 37.3%/26.2% | n/a (profitable_beyond_25.0x) | pass | 0.029 (unverified) | 0.33 |
| 57 | `cfg_197e` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 58/122/53 | 233 | 30.6% | 5.5% | 0.79 | -10.3% | 527 | 1.40 | 12.7% | 101.3 | 10/10 | 0.60 | 0.13 | 0.66 | 4 | 10.0% | 0.67 | 0.57 | 28.3% | 27.1% | 23.4% | 26.5%/18.4% | 12.1 (interpolated) | pass | 0.015 (unverified) | 0.08 |
| 58 | `cfg_87f7` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 5/82/69 | 156 | 25.8% | 4.7% | 0.80 | -7.8% | 237 | 1.43 | 7.8% | 69.0 | 9/9 | 0.89 | 0.47 | 0.33 | 5 | 14.0% | 0.40 | 0.73 | 25.0% | 23.3% | -2.2% | 23.8%/15.5% | 15.9 (interpolated) | pass | 0.016 (unverified) | -0.34 |
| 59 | `cfg_05eb` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 95/436/0 | 531 | 23.8% | 4.4% | 0.83 | -8.7% | 344 | 1.23 | 9.3% | 234.6 | 11/11 | 0.55 | 0.19 | 0.64 | 3 | 4.7% | 0.75 | 0.63 | 20.6% | 17.7% | 2.1% | 20.5%/16.1% | 5.3 (interpolated) | pass | 0.019 (unverified) | -0.20 |
| 60 | `cfg_04a7` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 12/75/69 | 156 | 25.4% | 4.6% | 0.80 | -7.8% | 237 | 1.43 | 7.7% | 68.9 | 10/10 | 0.90 | 0.51 | 0.29 | 5 | 13.6% | 0.41 | 0.73 | 23.9% | 23.2% | -3.4% | 22.8%/14.5% | 15.7 (interpolated) | pass | 0.015 (unverified) | -0.36 |
| 61 | `cfg_0406` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=20, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 56/128/0 | 184 | 30.7% | 5.5% | 0.87 | -5.0% | 299 | 1.54 | 11.3% | 80.8 | 9/9 | 0.56 | 0.08 | 0.78 | 4 | 10.2% | 0.67 | 0.55 | 30.1% | 28.0% | 27.1% | 27.1%/19.4% | 15.2 (interpolated) | pass | 0.018 (unverified) | -0.21 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 14.1% / 2.76 / 24 | 0.3% / 0.17 / 12 | 22.2% / 1.61 / 20 | 4.9% / 2.05 / 18 | 8.5% / 1.46 / 28 |
| 2 | 15.8% / 2.95 / 25 | -0.4% / -0.17 / 12 | 18.1% / 1.25 / 22 | 6.2% / 2.29 / 18 | 6.0% / 1.00 / 30 |
| 3 | 3.7% / 0.68 / 39 | 0.2% / 0.08 / 17 | 22.5% / 1.56 / 29 | 4.7% / 1.65 / 22 | 7.5% / 1.28 / 33 |
| 4 | 3.6% / 1.45 / 23 | 2.6% / 1.30 / 22 | 11.7% / 1.91 / 22 | 3.7% / 1.80 / 13 | -0.3% / -0.15 / 31 |
| 5 | 4.2% / 0.66 / 49 | 2.7% / 0.86 / 16 | 9.7% / 1.29 / 21 | 4.3% / 1.44 / 21 | 7.3% / 1.15 / 42 |
| 6 | 3.7% / 0.59 / 49 | 2.9% / 0.92 / 16 | 11.8% / 1.45 / 21 | 4.4% / 1.36 / 21 | 7.9% / 1.24 / 42 |
| 7 | 8.8% / 1.39 / 52 | 5.1% / 1.47 / 26 | 4.9% / 0.63 / 28 | 6.1% / 2.03 / 17 | 4.0% / 0.63 / 50 |
| 8 | 14.7% / 2.07 / 38 | 2.0% / 0.64 / 14 | 5.8% / 0.82 / 18 | 5.1% / 1.71 / 17 | -0.3% / -0.02 / 28 |
| 9 | 4.4% / 0.68 / 36 | 3.9% / 1.13 / 23 | 12.5% / 0.87 / 31 | 5.5% / 1.71 / 17 | 13.0% / 1.74 / 40 |
| 10 | 2.0% / 0.34 / 39 | 1.0% / 0.37 / 17 | 20.8% / 1.47 / 29 | 3.3% / 1.11 / 22 | 6.8% / 1.12 / 33 |
| 11 | 4.8% / 0.72 / 36 | 3.9% / 1.14 / 23 | 11.6% / 0.78 / 29 | 5.0% / 1.60 / 17 | 12.9% / 1.73 / 40 |
| 12 | 11.4% / 1.50 / 33 | 4.4% / 1.03 / 27 | 13.0% / 1.09 / 30 | 8.6% / 1.52 / 31 | -3.2% / -0.48 / 28 |
| 13 | 5.2% / 0.78 / 40 | 0.6% / 0.21 / 22 | 14.4% / 1.14 / 29 | 5.1% / 1.51 / 20 | 3.7% / 0.67 / 31 |
| 14 | 3.7% / 1.48 / 23 | 2.1% / 1.03 / 22 | 10.2% / 1.83 / 22 | 3.5% / 1.83 / 13 | -1.6% / -0.73 / 30 |
| 15 | 10.8% / 1.43 / 33 | 3.2% / 0.78 / 27 | 12.0% / 1.01 / 30 | 9.7% / 1.88 / 31 | -3.0% / -0.47 / 28 |
| 16 | 11.5% / 1.76 / 27 | 1.8% / 0.81 / 11 | 23.8% / 1.86 / 17 | 3.3% / 1.43 / 15 | 0.5% / 0.11 / 33 |
| 17 | 3.7% / 0.68 / 24 | 4.4% / 1.45 / 17 | 18.0% / 1.27 / 23 | 5.5% / 1.38 / 19 | 0.6% / 0.13 / 19 |
| 18 | 8.1% / 1.31 / 52 | 2.3% / 0.84 / 22 | -0.1% / 0.03 / 26 | 5.7% / 1.89 / 16 | 5.4% / 0.83 / 50 |
| 19 | -0.3% / -0.06 / 23 | 0.4% / 0.18 / 21 | 4.8% / 1.01 / 22 | 2.9% / 1.02 / 23 | 7.6% / 2.18 / 12 |
| 20 | 19.1% / 1.85 / 38 | 2.0% / 0.55 / 27 | 3.6% / 0.28 / 32 | 13.2% / 2.37 / 33 | 7.9% / 1.09 / 31 |
| 21 | 3.5% / 0.65 / 24 | 4.3% / 1.40 / 17 | 16.1% / 1.16 / 23 | 6.2% / 1.45 / 19 | 1.5% / 0.29 / 19 |
| 22 | 7.4% / 1.27 / 42 | -1.5% / -0.49 / 18 | 21.8% / 1.28 / 31 | 5.5% / 1.82 / 22 | 3.8% / 0.56 / 43 |
| 23 | 2.4% / 0.42 / 50 | 4.1% / 1.43 / 25 | 6.9% / 0.71 / 35 | 4.1% / 1.38 / 20 | 6.1% / 1.06 / 47 |
| 24 | 8.2% / 1.32 / 23 | 1.3% / 0.38 / 23 | -1.2% / -0.09 / 21 | 9.2% / 1.92 / 24 | 7.1% / 1.16 / 13 |
| 25 | 5.1% / 0.96 / 38 | 3.6% / 1.02 / 27 | 1.3% / 0.29 / 27 | 5.8% / 1.84 / 18 | 3.2% / 0.54 / 44 |
| 26 | 5.6% / 1.06 / 38 | 3.5% / 0.99 / 27 | 1.3% / 0.29 / 27 | 5.8% / 1.84 / 18 | 3.1% / 0.53 / 44 |
| 27 | 4.8% / 2.01 / 23 | 3.0% / 1.65 / 24 | 3.5% / 0.99 / 23 | 2.0% / 1.47 / 14 | -0.4% / -0.18 / 37 |
| 28 | 10.1% / 1.38 / 42 | 5.0% / 1.21 / 31 | 2.0% / 0.24 / 37 | 7.8% / 1.48 / 36 | 2.6% / 0.49 / 33 |
| 29 | 6.8% / 1.18 / 36 | -0.9% / -0.28 / 15 | 16.8% / 0.92 / 27 | 7.3% / 1.95 / 22 | 6.1% / 0.95 / 33 |
| 30 | -2.9% / -0.68 / 44 | 4.9% / 1.81 / 29 | 2.8% / 0.52 / 25 | 4.5% / 2.09 / 16 | 10.1% / 1.41 / 43 |
| 31 | 13.9% / 1.96 / 38 | 2.1% / 0.66 / 14 | 7.6% / 0.93 / 18 | 4.0% / 1.05 / 20 | 0.4% / 0.10 / 28 |
| 32 | 17.4% / 1.88 / 44 | 0.4% / 0.10 / 35 | 11.8% / 0.73 / 43 | 13.2% / 2.07 / 43 | -2.5% / -0.27 / 46 |
| 33 | 18.1% / 2.01 / 38 | 1.6% / 0.45 / 27 | 5.8% / 0.42 / 34 | 9.9% / 2.10 / 34 | 5.6% / 0.83 / 33 |
| 34 | 6.4% / 0.99 / 34 | -0.1% / -0.05 / 17 | 12.6% / 1.16 / 18 | 4.0% / 1.06 / 20 | 4.9% / 0.86 / 21 |
| 35 | 6.4% / 0.99 / 34 | -0.1% / -0.05 / 17 | 12.6% / 1.16 / 18 | 4.0% / 1.06 / 20 | 4.9% / 0.86 / 21 |
| 36 | -0.7% / -0.17 / 23 | 0.3% / 0.14 / 21 | 3.4% / 0.74 / 21 | 3.9% / 1.25 / 23 | 7.7% / 2.16 / 12 |
| 37 | -1.4% / -0.11 / 35 | 4.3% / 0.78 / 24 | 9.1% / 1.00 / 21 | 9.2% / 1.68 / 24 | 12.5% / 1.51 / 42 |
| 38 | 0.3% / 0.09 / 39 | 4.4% / 1.94 / 36 | 18.5% / 1.86 / 39 | 3.8% / 1.27 / 24 | -3.0% / -0.77 / 49 |
| 39 | 0.1% / 0.04 / 39 | 4.1% / 1.87 / 36 | 19.4% / 1.92 / 39 | 4.0% / 1.31 / 24 | -2.9% / -0.74 / 49 |
| 40 | 5.2% / 2.08 / 23 | 3.5% / 1.79 / 24 | 2.5% / 0.66 / 26 | 2.4% / 1.70 / 15 | -3.1% / -1.16 / 41 |
| 41 | 5.5% / 0.97 / 35 | 1.9% / 0.58 / 21 | 9.9% / 1.29 / 18 | 5.3% / 1.42 / 14 | -1.6% / -0.28 / 34 |
| 42 | 2.2% / 0.53 / 35 | -1.9% / -0.61 / 35 | 10.3% / 1.50 / 42 | 9.2% / 2.64 / 40 | 2.6% / 0.66 / 40 |
| 43 | 12.1% / 1.35 / 29 | 3.1% / 0.79 / 21 | 10.9% / 0.89 / 25 | 18.3% / 2.81 / 32 | -9.7% / -1.34 / 21 |
| 44 | 3.2% / 0.46 / 34 | 0.5% / 0.13 / 26 | 3.6% / 0.48 / 22 | 13.1% / 2.46 / 34 | 3.6% / 0.59 / 22 |
| 45 | -1.4% / -0.27 / 42 | 5.9% / 2.04 / 36 | 8.1% / 1.16 / 44 | 5.3% / 1.76 / 27 | 0.1% / 0.05 / 46 |
| 46 | 9.0% / 1.23 / 46 | 1.7% / 0.52 / 20 | 9.2% / 0.86 / 26 | 3.9% / 1.16 / 22 | 1.9% / 0.32 / 44 |
| 47 | 4.3% / 1.57 / 23 | 2.2% / 1.09 / 22 | 9.1% / 1.42 / 24 | 4.7% / 2.35 / 14 | -4.5% / -1.12 / 32 |
| 48 | 5.7% / 1.04 / 35 | -1.8% / -0.55 / 35 | 7.5% / 0.98 / 42 | 15.0% / 3.20 / 40 | -1.0% / -0.17 / 40 |
| 49 | -1.7% / -0.31 / 42 | 5.9% / 2.04 / 36 | 8.3% / 1.17 / 44 | 5.9% / 1.86 / 27 | 1.4% / 0.49 / 46 |
| 50 | -4.2% / -0.53 / 110 | 2.2% / 0.53 / 93 | 31.8% / 1.66 / 106 | 11.0% / 2.12 / 90 | -1.9% / -0.24 / 111 |
| 51 | -1.9% / -0.16 / 35 | 1.2% / 0.26 / 22 | 10.3% / 1.09 / 20 | 9.3% / 1.58 / 21 | 12.5% / 1.40 / 39 |
| 52 | 8.4% / 1.33 / 88 | 5.8% / 1.30 / 75 | 14.5% / 1.19 / 84 | 11.5% / 2.15 / 70 | -0.9% / -0.09 / 96 |
| 53 | 11.5% / 1.27 / 41 | -2.5% / -0.57 / 27 | 11.8% / 0.90 / 31 | 15.0% / 2.41 / 33 | -2.9% / -0.34 / 31 |
| 54 | 9.2% / 1.42 / 87 | 5.2% / 1.14 / 75 | 14.6% / 1.14 / 84 | 13.9% / 2.42 / 69 | 0.3% / 0.08 / 94 |
| 55 | -6.6% / -1.16 / 114 | 4.0% / 1.38 / 87 | 21.4% / 2.58 / 112 | -1.2% / -0.29 / 89 | 8.7% / 1.51 / 132 |
| 56 | 14.3% / 1.74 / 27 | 2.0% / 0.52 / 15 | 10.9% / 0.77 / 21 | 8.8% / 1.72 / 17 | 1.4% / 0.26 / 24 |
| 57 | -4.0% / -0.41 / 62 | 2.4% / 0.67 / 41 | 9.2% / 0.91 / 38 | 2.4% / 0.62 / 44 | 18.7% / 2.84 / 48 |
| 58 | 10.4% / 1.38 / 41 | 2.1% / 0.65 / 23 | 3.4% / 0.47 / 26 | 2.4% / 0.85 / 21 | 5.4% / 0.83 / 45 |
| 59 | -6.7% / -1.16 / 114 | 4.5% / 1.52 / 87 | 18.2% / 2.45 / 111 | -1.7% / -0.40 / 88 | 9.2% / 1.54 / 131 |
| 60 | 10.4% / 1.38 / 41 | 2.4% / 0.70 / 23 | 3.3% / 0.46 / 26 | 2.4% / 0.85 / 21 | 5.0% / 0.79 / 45 |
| 61 | -1.3% / -0.17 / 41 | 2.2% / 0.61 / 30 | 7.8% / 0.83 / 30 | 1.3% / 0.32 / 37 | 18.6% / 2.70 / 46 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_197e` | 2 | 0.85 | 0.85/0.85 | 0.76/0.76 |
| 1 | `cfg_87f7` | 4 | 0.99 | 0.98/1.00 | 0.98/0.99 |
| 2 | `cfg_0544` | 8 | 0.81 | 0.92/0.96 | 0.89/0.93 |
| 3 | `cfg_ffb5` | 4 | 0.98 | 0.98/0.99 | 0.95/0.98 |
| 4 | `cfg_d18c` | 2 | 0.97 | 0.96/0.96 | 0.99/0.99 |
| 5 | `cfg_0631` | 1 | n/a | n/a/n/a | n/a/n/a |
| 6 | `cfg_eade` | 4 | 0.95 | 0.96/0.96 | 0.97/0.97 |
| 7 | `cfg_08d4` | 11 | 0.84 | 0.84/0.86 | 0.42/0.46 |
| 8 | `cfg_0b90` | 1 | n/a | n/a/n/a | n/a/n/a |
| 9 | `cfg_f560` | 2 | 0.84 | 0.91/0.91 | 0.81/0.81 |
| 10 | `cfg_e15f` | 8 | 0.94 | 0.93/0.94 | 0.91/0.92 |
| 11 | `cfg_7fa2` | 19 | 0.80 | 0.65/0.72 | 0.30/0.45 |
| 12 | `cfg_1851` | 5 | 0.82 | 0.87/0.96 | 0.86/0.95 |
| 13 | `cfg_363c` | 4 | 0.97 | 0.98/0.98 | 0.94/0.96 |
| 14 | `cfg_204e` | 1 | n/a | n/a/n/a | n/a/n/a |
| 15 | `cfg_237a` | 4 | 0.90 | 0.91/0.94 | 0.83/0.94 |
| 16 | `cfg_2a39` | 1 | n/a | n/a/n/a | n/a/n/a |
| 17 | `cfg_2e7d` | 2 | 0.89 | 0.89/0.89 | 0.89/0.89 |
| 18 | `cfg_cee9` | 4 | 0.98 | 0.94/0.98 | 0.96/0.99 |
| 19 | `cfg_3871` | 2 | 0.82 | 0.88/0.88 | 0.76/0.76 |
| 20 | `cfg_f175` | 4 | 0.99 | 0.99/1.00 | 0.98/0.99 |
| 21 | `cfg_433b` | 1 | n/a | n/a/n/a | n/a/n/a |
| 22 | `cfg_49c6` | 2 | 0.98 | 0.98/0.98 | 0.96/0.96 |
| 23 | `cfg_55ca` | 1 | n/a | n/a/n/a | n/a/n/a |
| 24 | `cfg_5a90` | 2 | 0.84 | 0.80/0.80 | 0.54/0.54 |
| 25 | `cfg_6236` | 1 | n/a | n/a/n/a | n/a/n/a |
| 26 | `cfg_95c0` | 4 | 0.96 | 0.94/0.94 | 0.93/0.93 |
| 27 | `cfg_732d` | 2 | 0.88 | 0.92/0.92 | 0.68/0.68 |
| 28 | `cfg_c34b` | 2 | 0.96 | 0.99/0.99 | 0.88/0.88 |
| 29 | `cfg_902b` | 5 | 0.84 | 0.90/0.96 | 0.56/0.90 |
| 30 | `cfg_904f` | 1 | n/a | n/a/n/a | n/a/n/a |
| 31 | `cfg_a317` | 2 | 0.99 | 0.98/0.98 | 0.94/0.94 |
| 32 | `cfg_c591` | 1 | n/a | n/a/n/a | n/a/n/a |
| 33 | `cfg_e8be` | 1 | n/a | n/a/n/a | n/a/n/a |
| 34 | `cfg_f434` | 1 | n/a | n/a/n/a | n/a/n/a |
| 35 | `cfg_f72c` | 1 | n/a | n/a/n/a | n/a/n/a |
| 36 | `cfg_f9bd` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.118e-03 over 41112 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1204.0, participation ratio 20.3, 95%-variance components 265 (rank bound T = 1259); raw grid 41472; raw + known prior 513960
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
