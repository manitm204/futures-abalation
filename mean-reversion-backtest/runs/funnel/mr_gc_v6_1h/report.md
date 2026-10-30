# Screening funnel -- mr_gc_v6_1h (development stages only)

- Code: `7ba1d7ded49f` (dirty working tree: True, diff sha256 `31d84a59f562`)
- Config: `configs/funnel/mr_funnel_gc_v6_1h.yaml` sha256 `cced305f25192bc2`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'GC': '2026-10-16'}
- Frozen manifest sha256: `b0a8dbad6fbf9dc2` (282 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_gc_v5 gated 89 GC candidates on 2023-2024 (24 passed) and this grid was written after reading those results, so GC 2023-2024 is partly in-sample here.
- Holdout 2025+ previously inspected: **False** -- No GC strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection). The index and crude holdouts (ES/NQ/YM/RTY/CL) have been scored (other markets).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 17280 | 17280 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 17280 | 17280 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 17280 | 10945 | 6335 | 0 |  | 12288 | 63.34 | 63.34 |  |
| 3 performance & risk | hard_gate | 10945 | 838 | 10107 | 0 |  | 0 | 4.85 | 7.66 |  |
| 4 parameter stability | hard_gate | 838 | 808 | 30 | 0 |  | 0 | 4.68 | 96.42 |  |
| 5 time stability | hard_gate | 808 | 805 | 3 | 0 |  | 709 | 4.66 | 99.63 |  |
| 6 deduplication | dedup | 805 | 282 |  |  | 523 |  | 1.63 | 35.03 | best 2 per cluster |
| 7 execution stress | hard_gate | 282 | 282 | 0 | 0 |  | 0 | 1.63 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 282 |  |  |  |  |  |  |  | diagnostic only: unverified: 282 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 6326 |
| s2:hard_reject:years_with_>=10_trades | 2692 |
| s3:hard_reject:net_return | 2233 |
| s3:hard_reject:sharpe | 10107 |
| s4:hard_reject:local_median_sharpe | 30 |
| s5:hard_reject:profitable_years | 3 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | transfer dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_d91f` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 24/82/0 | 106 | 36.3% | 6.5% | 1.20 | -7.4% | 275 | 1.98 | 14.4% | 58.7 | 9/9 | 1.00 | 0.84 | 0.37 | 5 | 12.4% | 0.63 | 0.43 | 35.4% | 34.5% | 27.7% | 34.0%/26.6% | 20.4 (interpolated) | pass | 0.636 (unverified) | n/a |
| 2 | `cfg_41d0` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 38/47/69 | 154 | 42.9% | 7.5% | 1.26 | -10.0% | 173 | 1.65 | 20.1% | 85.9 | 9/9 | 1.00 | 1.00 | 0.25 | 4 | 19.7% | 0.49 | 0.45 | 41.0% | 40.0% | 39.8% | 37.8%/28.0% | 16.3 (interpolated) | pass | 0.678 (unverified) | n/a |
| 3 | `cfg_c598` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 23/69/59 | 151 | 34.9% | 6.3% | 1.16 | -6.5% | 167 | 1.65 | 16.5% | 84.4 | 10/10 | 1.00 | 0.84 | 0.31 | 5 | 15.8% | 0.50 | 0.56 | 33.1% | 31.7% | 23.9% | 31.1%/23.1% | 14.2 (interpolated) | pass | 0.588 (unverified) | n/a |
| 4 | `cfg_e7e9` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 19/101/0 | 120 | 30.0% | 5.5% | 1.05 | -6.5% | 350 | 1.67 | 13.9% | 66.2 | 10/10 | 1.00 | 0.85 | 0.20 | 4 | 13.0% | 0.57 | 0.62 | 29.5% | 27.8% | 29.1% | 28.3%/23.2% | 15.8 (interpolated) | pass | 0.495 (unverified) | n/a |
| 5 | `cfg_2975` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 21/88/40 | 149 | 34.9% | 6.3% | 1.16 | -5.8% | 246 | 1.65 | 15.2% | 81.8 | 11/11 | 1.00 | 0.94 | 0.23 | 5 | 15.0% | 0.55 | 0.59 | 32.6% | 31.6% | 28.4% | 32.5%/25.2% | 14.2 (interpolated) | pass | 0.597 (unverified) | n/a |
| 6 | `cfg_d928` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 19/85/53 | 157 | 30.5% | 5.6% | 1.08 | -6.7% | 181 | 1.59 | 14.8% | 86.4 | 11/11 | 1.00 | 0.92 | 0.15 | 5 | 12.4% | 0.57 | 0.63 | 28.6% | 27.0% | 30.5% | 27.4%/22.3% | 12.2 (interpolated) | pass | 0.517 (unverified) | n/a |
| 7 | `cfg_72c6` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 37/69/0 | 106 | 34.7% | 6.2% | 1.18 | -7.5% | 275 | 1.96 | 13.9% | 58.6 | 10/10 | 1.00 | 0.85 | 0.33 | 5 | 12.1% | 0.62 | 0.44 | 32.7% | 31.2% | 25.5% | 28.9%/22.7% | 18.9 (interpolated) | pass | 0.618 (unverified) | n/a |
| 8 | `cfg_fabe` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 25/95/0 | 120 | 28.7% | 5.3% | 1.02 | -7.3% | 350 | 1.65 | 13.7% | 66.2 | 11/11 | 1.00 | 0.86 | 0.16 | 4 | 11.9% | 0.59 | 0.65 | 27.2% | 26.0% | 26.6% | 26.4%/19.7% | 14.7 (interpolated) | pass | 0.466 (unverified) | n/a |
| 9 | `cfg_f978` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 35/60/89 | 184 | 35.4% | 6.4% | 1.04 | -9.5% | 173 | 1.46 | 23.5% | 101.0 | 10/10 | 1.00 | 0.90 | 0.14 | 4 | 19.1% | 0.42 | 0.51 | 33.7% | 31.7% | 19.0% | 29.0%/22.3% | 12.0 (interpolated) | pass | 0.485 (unverified) | n/a |
| 10 | `cfg_9dbb` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 44/31/32 | 107 | 22.7% | 4.3% | 1.01 | -7.3% | 455 | 1.66 | 10.8% | 58.8 | 10/10 | 1.00 | 0.90 | 0.11 | 4 | 7.2% | 0.67 | 0.56 | 22.0% | 20.8% | 11.4% | 20.6%/17.7% | 13.9 (interpolated) | pass | 0.454 (unverified) | n/a |
| 11 | `cfg_6c1e` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 10/73/47 | 130 | 26.0% | 4.8% | 0.99 | -7.0% | 350 | 1.60 | 12.4% | 72.1 | 10/10 | 1.00 | 0.89 | 0.10 | 4 | 5.7% | 0.78 | 0.77 | 24.3% | 23.6% | 18.3% | 23.2%/17.5% | 12.7 (interpolated) | pass | 0.434 (unverified) | n/a |
| 12 | `cfg_46f1` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=2.0 | 36/48/61 | 145 | 31.5% | 5.7% | 0.97 | -10.7% | 173 | 1.48 | 20.0% | 79.0 | 9/9 | 1.00 | 0.77 | 0.20 | 4 | 12.6% | 0.58 | 0.55 | 30.3% | 28.7% | 32.0% | 26.3%/19.7% | 13.7 (interpolated) | pass | 0.421 (unverified) | n/a |
| 13 | `cfg_5d59` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 29/43/31 | 103 | 36.3% | 6.5% | 1.11 | -6.7% | 256 | 1.85 | 14.8% | 56.8 | 10/10 | 1.00 | 0.79 | 0.33 | 5 | 11.1% | 0.66 | 0.49 | 35.0% | 33.4% | 20.9% | 32.8%/25.5% | 20.9 (interpolated) | pass | 0.548 (unverified) | n/a |
| 14 | `cfg_8dae` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 19/74/63 | 156 | 36.4% | 6.5% | 1.20 | -6.2% | 128 | 1.65 | 16.7% | 86.1 | 10/10 | 1.00 | 0.95 | 0.25 | 5 | 17.4% | 0.47 | 0.53 | 34.9% | 33.6% | 26.4% | 31.6%/24.8% | 14.4 (interpolated) | pass | 0.632 (unverified) | n/a |
| 15 | `cfg_722a` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 38/57/58 | 153 | 34.6% | 6.2% | 1.19 | -6.1% | 169 | 1.67 | 15.8% | 85.4 | 10/10 | 1.00 | 0.80 | 0.39 | 5 | 18.0% | 0.43 | 0.52 | 32.8% | 31.3% | 22.5% | 29.3%/22.9% | 14.0 (interpolated) | pass | 0.617 (unverified) | n/a |
| 16 | `cfg_e9e9` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 23/70/46 | 139 | 31.8% | 5.8% | 1.06 | -10.6% | 350 | 1.58 | 16.2% | 75.5 | 10/10 | 1.00 | 0.92 | 0.14 | 4 | 6.8% | 0.80 | 0.61 | 30.6% | 29.2% | 32.5% | 28.7%/22.8% | 14.4 (interpolated) | pass | 0.502 (unverified) | n/a |
| 17 | `cfg_1e20` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=22, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 20/56/50 | 126 | 30.5% | 5.6% | 1.01 | -5.7% | 388 | 1.58 | 13.7% | 69.6 | 10/10 | 1.00 | 0.76 | 0.25 | 5 | 14.9% | 0.49 | 0.54 | 29.2% | 28.8% | 11.1% | 28.2%/20.4% | 15.6 (interpolated) | pass | 0.459 (unverified) | n/a |
| 18 | `cfg_6ab2` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 24/78/42 | 144 | 36.2% | 6.5% | 1.16 | -7.6% | 263 | 1.64 | 17.0% | 78.8 | 11/11 | 1.00 | 0.98 | 0.17 | 4 | 14.8% | 0.57 | 0.55 | 34.8% | 33.6% | 26.2% | 32.0%/25.9% | 15.6 (interpolated) | pass | 0.588 (unverified) | n/a |
| 19 | `cfg_b2b6` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 19/75/62 | 156 | 32.6% | 5.9% | 1.02 | -8.7% | 417 | 1.54 | 17.0% | 86.7 | 10/10 | 1.00 | 0.95 | 0.06 | 4 | 9.4% | 0.70 | 0.61 | 31.1% | 29.4% | 27.0% | 28.5%/21.3% | 13.2 (interpolated) | pass | 0.467 (unverified) | n/a |
| 20 | `cfg_b054` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 25/63/63 | 151 | 33.6% | 6.1% | 1.12 | -8.4% | 275 | 1.62 | 15.9% | 81.7 | 10/10 | 1.00 | 0.95 | 0.17 | 3 | 7.3% | 0.76 | 0.59 | 32.2% | 30.1% | 37.0% | 29.5%/23.3% | 13.4 (interpolated) | pass | 0.558 (unverified) | n/a |
| 21 | `cfg_99fa` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 46/56/94 | 196 | 38.6% | 6.9% | 1.07 | -5.4% | 151 | 1.49 | 23.9% | 107.9 | 10/10 | 1.00 | 0.87 | 0.20 | 5 | 24.2% | 0.34 | 0.46 | 37.7% | 35.6% | 31.3% | 33.8%/24.7% | 12.0 (interpolated) | pass | 0.514 (unverified) | n/a |
| 22 | `cfg_8962` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 21/54/46 | 121 | 32.3% | 5.9% | 1.14 | -4.7% | 121 | 1.72 | 13.1% | 67.4 | 9/9 | 1.00 | 0.88 | 0.26 | 5 | 21.0% | 0.32 | 0.49 | 30.8% | 29.5% | 14.7% | 28.5%/23.0% | 16.6 (interpolated) | pass | 0.578 (unverified) | n/a |
| 23 | `cfg_d1fa` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 26/54/73 | 153 | 31.7% | 5.8% | 1.04 | -10.1% | 274 | 1.51 | 19.6% | 84.8 | 9/9 | 1.00 | 0.93 | 0.11 | 4 | 13.8% | 0.53 | 0.54 | 30.2% | 28.7% | 21.4% | 29.0%/21.6% | 13.3 (interpolated) | pass | 0.481 (unverified) | n/a |
| 24 | `cfg_1132` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 13/62/61 | 136 | 30.7% | 5.6% | 1.02 | -9.2% | 311 | 1.58 | 14.8% | 75.5 | 10/10 | 1.00 | 0.92 | 0.11 | 4 | 7.3% | 0.76 | 0.66 | 28.9% | 27.6% | 19.3% | 26.4%/20.3% | 14.3 (interpolated) | pass | 0.469 (unverified) | n/a |
| 25 | `cfg_e1d6` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 25/93/41 | 159 | 27.2% | 5.0% | 0.99 | -7.1% | 350 | 1.52 | 16.2% | 86.4 | 11/11 | 1.00 | 0.78 | 0.21 | 3 | 10.5% | 0.59 | 0.65 | 25.6% | 24.2% | 15.4% | 24.4%/18.5% | 10.8 (interpolated) | pass | 0.438 (unverified) | n/a |
| 26 | `cfg_fb8c` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 37/43/73 | 153 | 28.7% | 5.3% | 0.96 | -11.0% | 197 | 1.46 | 18.7% | 85.1 | 10/10 | 1.00 | 0.92 | 0.04 | 4 | 11.9% | 0.56 | 0.58 | 27.1% | 26.2% | 17.9% | 26.6%/19.6% | 12.3 (interpolated) | pass | 0.409 (unverified) | n/a |
| 27 | `cfg_d32d` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 26/50/76 | 152 | 31.7% | 5.8% | 0.93 | -11.7% | 417 | 1.46 | 19.4% | 83.9 | 9/9 | 1.00 | 0.98 | -0.05 | 3 | 6.6% | 0.82 | 0.62 | 29.4% | 28.1% | 24.7% | 26.2%/18.7% | 12.9 (interpolated) | pass | 0.387 (unverified) | n/a |
| 28 | `cfg_b0e6` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 32/74/49 | 155 | 26.2% | 4.8% | 0.92 | -8.6% | 388 | 1.45 | 18.0% | 84.6 | 11/11 | 1.00 | 0.69 | 0.23 | 4 | 7.6% | 0.72 | 0.66 | 25.8% | 24.2% | 18.6% | 24.1%/18.5% | 11.5 (interpolated) | pass | 0.380 (unverified) | n/a |
| 29 | `cfg_df4a` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 15/59/51 | 125 | 27.2% | 5.0% | 1.05 | -8.2% | 350 | 1.62 | 11.4% | 68.3 | 10/10 | 1.00 | 0.90 | 0.16 | 3 | 7.9% | 0.70 | 0.68 | 26.1% | 25.0% | 23.8% | 25.0%/18.1% | 13.7 (interpolated) | pass | 0.496 (unverified) | n/a |
| 30 | `cfg_919d` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 37/40/46 | 123 | 25.8% | 4.8% | 1.01 | -5.4% | 127 | 1.59 | 12.1% | 68.1 | 9/9 | 1.00 | 0.81 | 0.21 | 4 | 15.6% | 0.38 | 0.56 | 25.1% | 23.7% | 8.7% | 23.3%/17.7% | 13.6 (interpolated) | pass | 0.458 (unverified) | n/a |
| 31 | `cfg_9c48` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 42/28/42 | 112 | 20.7% | 3.9% | 0.94 | -6.3% | 455 | 1.59 | 10.4% | 61.1 | 10/10 | 1.00 | 0.82 | 0.12 | 4 | 7.6% | 0.61 | 0.62 | 19.8% | 19.0% | 10.7% | 19.3%/14.4% | 12.5 (interpolated) | pass | 0.389 (unverified) | n/a |
| 32 | `cfg_6b6a` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 18/58/29 | 105 | 34.0% | 6.1% | 1.15 | -5.4% | 321 | 1.95 | 12.2% | 57.9 | 11/11 | 1.00 | 0.77 | 0.38 | 4 | 11.2% | 0.63 | 0.45 | 32.6% | 31.5% | 23.1% | 30.5%/24.9% | 19.0 (interpolated) | pass | 0.588 (unverified) | n/a |
| 33 | `cfg_872c` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 42/41/62 | 145 | 29.5% | 5.4% | 1.04 | -8.1% | 173 | 1.57 | 17.6% | 80.9 | 9/9 | 1.00 | 0.77 | 0.27 | 4 | 14.0% | 0.50 | 0.48 | 28.3% | 26.4% | 13.2% | 27.1%/19.8% | 13.1 (interpolated) | pass | 0.485 (unverified) | n/a |
| 34 | `cfg_9efe` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=22, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 39/40/50 | 129 | 25.1% | 4.7% | 0.92 | -7.3% | 388 | 1.49 | 12.9% | 70.6 | 10/10 | 1.00 | 0.73 | 0.20 | 4 | 10.8% | 0.57 | 0.57 | 24.5% | 22.3% | 7.1% | 23.2%/16.3% | 12.9 (interpolated) | pass | 0.381 (unverified) | n/a |
| 35 | `cfg_3f8b` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 26/88/57 | 171 | 28.5% | 5.2% | 1.03 | -5.4% | 308 | 1.56 | 16.0% | 93.1 | 11/11 | 1.00 | 0.87 | 0.16 | 4 | 9.5% | 0.63 | 0.62 | 27.2% | 24.9% | 22.0% | 26.6%/19.9% | 11.0 (interpolated) | pass | 0.475 (unverified) | n/a |
| 36 | `cfg_3c25` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 15/65/62 | 142 | 23.7% | 4.4% | 0.89 | -6.5% | 365 | 1.49 | 15.4% | 76.9 | 10/10 | 1.00 | 0.79 | 0.10 | 4 | 10.3% | 0.54 | 0.75 | 22.6% | 21.4% | 20.1% | 20.9%/14.8% | 11.2 (interpolated) | pass | 0.351 (unverified) | n/a |
| 37 | `cfg_b6a2` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 25/72/63 | 160 | 34.4% | 6.2% | 1.08 | -8.8% | 304 | 1.58 | 17.4% | 87.2 | 11/11 | 1.00 | 0.89 | 0.19 | 4 | 13.2% | 0.59 | 0.57 | 32.6% | 31.7% | 25.5% | 30.4%/23.7% | 13.0 (interpolated) | pass | 0.521 (unverified) | n/a |
| 38 | `cfg_4393` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 17/111/0 | 128 | 29.1% | 5.3% | 1.04 | -6.6% | 350 | 1.70 | 15.1% | 70.8 | 10/10 | 1.00 | 0.82 | 0.22 | 5 | 11.9% | 0.59 | 0.63 | 27.0% | 26.4% | 26.4% | 26.2%/20.2% | 14.1 (interpolated) | pass | 0.486 (unverified) | n/a |
| 39 | `cfg_6f33` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=22, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 18/83/79 | 180 | 33.4% | 6.0% | 0.98 | -8.6% | 263 | 1.47 | 19.5% | 97.9 | 11/11 | 1.00 | 0.78 | 0.20 | 3 | 9.6% | 0.71 | 0.60 | 31.5% | 29.6% | 21.9% | 30.9%/23.1% | 11.9 (interpolated) | pass | 0.429 (unverified) | n/a |
| 40 | `cfg_4e6a` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 21/95/0 | 116 | 24.6% | 4.6% | 0.79 | -7.8% | 356 | 1.49 | 16.2% | 64.0 | 10/10 | 1.00 | 0.84 | -0.05 | 4 | 9.0% | 0.67 | 0.78 | 24.3% | 24.1% | 18.1% | 23.3%/17.8% | 13.2 (interpolated) | pass | 0.285 (unverified) | n/a |
| 41 | `cfg_f6d5` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 23/55/67 | 145 | 26.9% | 5.0% | 0.91 | -8.3% | 365 | 1.49 | 19.0% | 80.1 | 9/9 | 1.00 | 0.76 | 0.15 | 3 | 11.9% | 0.52 | 0.64 | 26.2% | 24.0% | 15.3% | 23.2%/15.9% | 11.9 (interpolated) | pass | 0.372 (unverified) | n/a |
| 42 | `cfg_503c` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=25, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 17/66/30 | 113 | 29.0% | 5.3% | 1.17 | -4.4% | 422 | 1.76 | 11.5% | 61.7 | 9/9 | 0.89 | 0.80 | 0.37 | 4 | 16.3% | 0.42 | 0.64 | 27.7% | 26.8% | 15.2% | 24.6%/19.7% | 15.8 (interpolated) | pass | 0.592 (unverified) | n/a |
| 43 | `cfg_30c1` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 25/86/68 | 179 | 35.2% | 6.3% | 1.12 | -6.2% | 128 | 1.54 | 19.3% | 99.1 | 11/11 | 1.00 | 0.83 | 0.29 | 5 | 16.6% | 0.49 | 0.55 | 33.3% | 31.7% | 24.0% | 29.7%/21.9% | 12.3 (interpolated) | pass | 0.552 (unverified) | n/a |
| 44 | `cfg_1ef0` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 13/99/0 | 112 | 27.1% | 5.0% | 0.99 | -5.6% | 521 | 1.71 | 13.1% | 62.1 | 9/9 | 1.00 | 0.80 | 0.19 | 4 | 12.9% | 0.52 | 0.66 | 26.7% | 26.5% | 23.5% | 26.2%/18.7% | 15.4 (interpolated) | pass | 0.437 (unverified) | n/a |
| 45 | `cfg_7154` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 20/87/70 | 177 | 28.4% | 5.2% | 0.94 | -7.6% | 345 | 1.44 | 16.0% | 97.1 | 11/11 | 1.00 | 0.81 | 0.14 | 4 | 10.2% | 0.63 | 0.68 | 26.8% | 26.0% | 25.4% | 25.5%/18.1% | 10.5 (interpolated) | pass | 0.397 (unverified) | n/a |
| 46 | `cfg_7eb2` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=25, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 16/62/43 | 121 | 29.3% | 5.4% | 1.20 | -4.6% | 363 | 1.80 | 11.2% | 65.9 | 9/9 | 1.00 | 0.89 | 0.31 | 4 | 15.3% | 0.45 | 0.64 | 28.0% | 27.0% | 20.5% | 26.6%/21.6% | 14.6 (interpolated) | pass | 0.625 (unverified) | n/a |
| 47 | `cfg_4f7d` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 31/68/68 | 167 | 24.9% | 4.6% | 0.87 | -5.6% | 364 | 1.44 | 17.8% | 91.1 | 11/11 | 1.00 | 0.73 | 0.14 | 4 | 6.3% | 0.73 | 0.68 | 23.5% | 20.8% | 20.1% | 21.9%/15.8% | 9.5 (interpolated) | pass | 0.331 (unverified) | n/a |
| 48 | `cfg_26ad` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 26/43/48 | 117 | 28.5% | 5.2% | 0.98 | -5.9% | 127 | 1.63 | 15.1% | 65.0 | 8/8 | 1.00 | 0.82 | 0.15 | 4 | 18.2% | 0.34 | 0.60 | 27.8% | 26.6% | 18.5% | 27.0%/20.3% | 15.4 (interpolated) | pass | 0.427 (unverified) | n/a |
| 49 | `cfg_f868` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 44/36/50 | 130 | 22.7% | 4.3% | 0.89 | -3.9% | 217 | 1.51 | 12.7% | 70.9 | 10/10 | 1.00 | 0.77 | 0.12 | 5 | 9.7% | 0.56 | 0.60 | 21.4% | 19.5% | 8.5% | 20.0%/15.4% | 11.7 (interpolated) | pass | 0.349 (unverified) | n/a |
| 50 | `cfg_98e0` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 48/48/88 | 184 | 34.7% | 6.3% | 1.04 | -9.8% | 173 | 1.46 | 22.6% | 100.6 | 11/11 | 1.00 | 0.86 | 0.18 | 4 | 17.2% | 0.47 | 0.50 | 32.0% | 30.2% | 17.2% | 29.4%/22.1% | 11.7 (interpolated) | pass | 0.483 (unverified) | n/a |
| 51 | `cfg_21cb` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 39/90/0 | 129 | 29.5% | 5.4% | 1.09 | -6.3% | 350 | 1.74 | 14.5% | 71.0 | 10/10 | 1.00 | 0.83 | 0.26 | 5 | 13.1% | 0.55 | 0.59 | 29.1% | 27.8% | 29.0% | 26.7%/21.1% | 14.5 (interpolated) | pass | 0.532 (unverified) | n/a |
| 52 | `cfg_afc7` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 25/52/66 | 143 | 28.9% | 5.3% | 0.92 | -6.4% | 309 | 1.50 | 19.1% | 78.9 | 9/9 | 1.00 | 0.84 | 0.08 | 4 | 11.9% | 0.56 | 0.59 | 26.5% | 24.9% | 17.3% | 24.1%/17.8% | 13.3 (interpolated) | pass | 0.378 (unverified) | n/a |
| 53 | `cfg_4d95` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 36/36/76 | 148 | 32.1% | 5.8% | 0.99 | -9.2% | 359 | 1.51 | 18.0% | 80.6 | 9/9 | 1.00 | 0.90 | 0.09 | 3 | 6.8% | 0.79 | 0.54 | 30.9% | 29.1% | 31.9% | 29.2%/20.9% | 13.7 (interpolated) | pass | 0.438 (unverified) | n/a |
| 54 | `cfg_37fc` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 37/114/0 | 151 | 32.2% | 5.8% | 1.09 | -4.9% | 350 | 1.66 | 17.2% | 83.6 | 8/8 | 1.00 | 0.82 | 0.28 | 4 | 13.1% | 0.59 | 0.56 | 30.4% | 28.6% | 28.6% | 28.9%/20.4% | 13.4 (interpolated) | pass | 0.531 (unverified) | n/a |
| 55 | `cfg_7c34` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 21/53/51 | 125 | 24.9% | 4.6% | 0.99 | -8.2% | 350 | 1.57 | 11.2% | 68.3 | 11/11 | 1.00 | 0.93 | 0.06 | 3 | 7.4% | 0.70 | 0.69 | 23.9% | 22.7% | 20.3% | 23.5%/17.1% | 13.0 (interpolated) | pass | 0.436 (unverified) | n/a |
| 56 | `cfg_cc94` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 36/105/69 | 210 | 38.8% | 6.9% | 1.06 | -7.8% | 275 | 1.43 | 24.3% | 115.9 | 10/10 | 1.00 | 0.74 | 0.31 | 3 | 11.7% | 0.70 | 0.53 | 37.5% | 36.0% | 29.5% | 34.1%/24.8% | 11.5 (interpolated) | pass | 0.499 (unverified) | n/a |
| 57 | `cfg_51af` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 14/105/37 | 156 | 22.5% | 4.2% | 1.01 | -4.0% | 172 | 1.58 | 10.9% | 85.1 | 11/11 | 0.91 | 0.80 | 0.21 | 5 | 12.5% | 0.43 | 0.59 | 21.0% | 19.7% | 24.1% | 20.5%/14.7% | 9.7 (interpolated) | pass | 0.450 (unverified) | n/a |
| 58 | `cfg_cf19` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 49/67/111 | 227 | 36.4% | 6.5% | 0.96 | -7.5% | 251 | 1.39 | 28.3% | 123.7 | 9/9 | 1.00 | 0.75 | 0.21 | 4 | 13.4% | 0.60 | 0.49 | 33.1% | 30.9% | 29.1% | 33.9%/23.0% | 9.9 (interpolated) | pass | 0.410 (unverified) | n/a |
| 59 | `cfg_c39f` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 11/108/37 | 156 | 22.5% | 4.2% | 1.00 | -4.0% | 172 | 1.57 | 11.0% | 85.2 | 10/10 | 0.90 | 0.76 | 0.24 | 5 | 12.4% | 0.43 | 0.59 | 21.0% | 19.7% | 23.3% | 19.7%/15.7% | 9.6 (interpolated) | pass | 0.444 (unverified) | n/a |
| 60 | `cfg_a082` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 22/90/0 | 112 | 27.4% | 5.0% | 1.00 | -5.9% | 521 | 1.71 | 12.9% | 62.2 | 10/10 | 1.00 | 0.82 | 0.18 | 4 | 12.9% | 0.53 | 0.64 | 27.0% | 26.6% | 22.3% | 25.4%/16.5% | 15.6 (interpolated) | pass | 0.447 (unverified) | n/a |
| 61 | `cfg_02d2` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 40/104/68 | 212 | 29.9% | 5.5% | 0.88 | -6.1% | 275 | 1.35 | 23.9% | 117.0 | 10/10 | 1.00 | 0.62 | 0.26 | 3 | 7.0% | 0.78 | 0.64 | 27.4% | 25.9% | 20.5% | 25.1%/17.9% | 9.0 (interpolated) | pass | 0.340 (unverified) | n/a |
| 62 | `cfg_1917` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 27/80/75 | 182 | 27.2% | 5.0% | 0.87 | -8.5% | 181 | 1.38 | 19.7% | 99.7 | 11/11 | 1.00 | 0.76 | 0.11 | 4 | 5.7% | 0.79 | 0.70 | 24.6% | 23.4% | 28.6% | 23.3%/17.6% | 9.3 (interpolated) | pass | 0.330 (unverified) | n/a |
| 63 | `cfg_0887` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 26/81/66 | 173 | 36.6% | 6.6% | 1.08 | -7.6% | 196 | 1.57 | 18.4% | 95.4 | 11/11 | 1.00 | 0.86 | 0.22 | 5 | 11.3% | 0.67 | 0.53 | 34.9% | 33.6% | 31.8% | 31.8%/26.5% | 13.0 (interpolated) | pass | 0.521 (unverified) | n/a |
| 64 | `cfg_c40a` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 53/63/110 | 226 | 36.3% | 6.5% | 0.96 | -6.6% | 185 | 1.38 | 27.1% | 123.3 | 9/9 | 1.00 | 0.69 | 0.27 | 5 | 16.1% | 0.53 | 0.49 | 34.1% | 31.0% | 25.9% | 28.6%/20.1% | 9.9 (interpolated) | pass | 0.415 (unverified) | n/a |
| 65 | `cfg_f6fc` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 30/63/63 | 156 | 32.2% | 5.8% | 1.11 | -6.1% | 128 | 1.58 | 16.3% | 86.4 | 11/11 | 1.00 | 0.90 | 0.21 | 5 | 14.0% | 0.53 | 0.58 | 30.7% | 28.9% | 22.5% | 28.1%/22.1% | 13.1 (interpolated) | pass | 0.549 (unverified) | n/a |
| 66 | `cfg_3f4c` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 34/23/43 | 100 | 23.0% | 4.3% | 0.89 | -6.7% | 313 | 1.61 | 11.7% | 54.8 | 11/11 | 1.00 | 0.79 | 0.10 | 5 | 14.4% | 0.35 | 0.72 | 21.9% | 21.5% | 15.9% | 20.9%/17.1% | 14.6 (interpolated) | pass | 0.346 (unverified) | n/a |
| 67 | `cfg_a762` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 31/69/0 | 100 | 24.1% | 4.5% | 1.01 | -6.5% | 350 | 1.80 | 10.7% | 55.0 | 9/9 | 1.00 | 0.73 | 0.28 | 4 | 6.7% | 0.72 | 0.61 | 22.9% | 22.1% | 25.8% | 23.0%/17.5% | 15.6 (interpolated) | pass | 0.454 (unverified) | n/a |
| 68 | `cfg_0265` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 25/53/35 | 113 | 28.0% | 5.1% | 1.16 | -5.3% | 455 | 1.84 | 10.4% | 62.2 | 10/10 | 1.00 | 0.84 | 0.31 | 4 | 7.8% | 0.71 | 0.56 | 26.6% | 25.6% | 15.0% | 24.8%/20.3% | 15.7 (interpolated) | pass | 0.595 (unverified) | n/a |
| 69 | `cfg_447f` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 22/32/46 | 100 | 22.3% | 4.2% | 0.84 | -7.3% | 317 | 1.57 | 12.7% | 54.8 | 10/10 | 1.00 | 0.69 | 0.15 | 5 | 14.0% | 0.35 | 0.76 | 21.4% | 20.0% | 14.8% | 19.9%/15.6% | 14.1 (interpolated) | pass | 0.301 (unverified) | n/a |
| 70 | `cfg_8efb` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=none | 60/83/0 | 143 | 32.3% | 5.9% | 0.86 | -8.2% | 275 | 1.52 | 24.3% | 78.7 | 9/9 | 1.00 | 0.79 | 0.06 | 4 | 16.4% | 0.49 | 0.50 | 30.8% | 29.1% | 26.5% | 29.1%/23.1% | 13.9 (interpolated) | pass | 0.330 (unverified) | n/a |
| 71 | `cfg_41d6` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=22, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 36/90/54 | 180 | 27.4% | 5.0% | 0.92 | -6.6% | 211 | 1.42 | 17.4% | 98.3 | 9/9 | 1.00 | 0.74 | 0.18 | 4 | 11.0% | 0.60 | 0.65 | 25.8% | 24.8% | 7.8% | 24.4%/17.2% | 10.0 (interpolated) | pass | 0.382 (unverified) | n/a |
| 72 | `cfg_99af` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 25/90/80 | 195 | 31.5% | 5.7% | 0.98 | -7.9% | 184 | 1.43 | 20.6% | 108.0 | 11/11 | 1.00 | 0.82 | 0.16 | 4 | 11.5% | 0.61 | 0.63 | 29.4% | 27.3% | 21.1% | 27.1%/21.2% | 10.4 (interpolated) | pass | 0.426 (unverified) | n/a |
| 73 | `cfg_447b` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 19/65/120 | 204 | 28.0% | 5.1% | 0.89 | -10.9% | 220 | 1.39 | 17.7% | 113.3 | 9/9 | 1.00 | 0.81 | 0.08 | 5 | 8.0% | 0.68 | 0.74 | 24.5% | 22.9% | 11.7% | 24.1%/15.4% | 9.2 (interpolated) | pass | 0.353 (unverified) | n/a |
| 74 | `cfg_5185` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 28/89/0 | 117 | 25.9% | 4.8% | 0.86 | -6.3% | 356 | 1.53 | 15.9% | 64.2 | 11/11 | 1.00 | 0.79 | 0.06 | 4 | 10.6% | 0.61 | 0.71 | 25.6% | 24.4% | 19.7% | 23.4%/18.1% | 13.8 (interpolated) | pass | 0.333 (unverified) | n/a |
| 75 | `cfg_6382` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=none | 47/96/0 | 143 | 39.6% | 7.0% | 1.00 | -7.1% | 275 | 1.63 | 25.8% | 78.2 | 8/8 | 1.00 | 0.83 | 0.17 | 5 | 19.5% | 0.49 | 0.44 | 37.6% | 36.4% | 35.3% | 33.8%/27.3% | 16.2 (interpolated) | pass | 0.450 (unverified) | n/a |
| 76 | `cfg_2dc0` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=18, entry_z=-3.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 33/45/65 | 143 | 26.6% | 4.9% | 0.87 | -6.3% | 293 | 1.47 | 18.2% | 77.9 | 10/10 | 1.00 | 0.77 | 0.11 | 5 | 12.6% | 0.51 | 0.61 | 24.8% | 23.3% | 13.3% | 20.9%/15.2% | 12.5 (interpolated) | pass | 0.344 (unverified) | n/a |
| 77 | `cfg_1fbe` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 39/50/81 | 170 | 33.8% | 6.1% | 1.05 | -12.0% | 277 | 1.48 | 21.4% | 93.7 | 10/10 | 1.00 | 0.76 | 0.28 | 4 | 17.2% | 0.45 | 0.50 | 32.0% | 30.5% | 23.5% | 28.4%/21.4% | 12.6 (interpolated) | pass | 0.490 (unverified) | n/a |
| 78 | `cfg_4544` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 34/46/72 | 152 | 34.8% | 6.3% | 1.05 | -6.4% | 319 | 1.57 | 19.4% | 83.5 | 10/10 | 1.00 | 0.77 | 0.27 | 4 | 20.6% | 0.36 | 0.51 | 33.0% | 30.8% | 22.4% | 30.2%/22.4% | 13.7 (interpolated) | pass | 0.490 (unverified) | n/a |
| 79 | `cfg_ad97` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 37/101/96 | 234 | 27.9% | 5.1% | 0.83 | -5.0% | 166 | 1.32 | 23.8% | 128.5 | 10/10 | 1.00 | 0.76 | 0.07 | 5 | 8.1% | 0.69 | 0.66 | 25.6% | 23.4% | 25.2% | 22.9%/16.8% | 8.0 (interpolated) | pass | 0.305 (unverified) | n/a |
| 80 | `cfg_132e` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=22, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 30/71/79 | 180 | 31.6% | 5.7% | 0.95 | -8.5% | 263 | 1.44 | 19.1% | 97.9 | 12/12 | 1.00 | 0.72 | 0.23 | 3 | 7.8% | 0.76 | 0.64 | 29.8% | 27.8% | 20.6% | 29.7%/21.6% | 11.3 (interpolated) | pass | 0.400 (unverified) | n/a |
| 81 | `cfg_2d04` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=2.0 | 37/38/62 | 137 | 35.2% | 6.3% | 1.02 | -11.1% | 275 | 1.52 | 18.8% | 75.0 | 9/9 | 1.00 | 0.94 | 0.08 | 3 | 11.3% | 0.67 | 0.55 | 33.1% | 32.6% | 29.4% | 29.5%/22.9% | 15.3 (interpolated) | pass | 0.463 (unverified) | n/a |
| 82 | `cfg_dbd3` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 19/63/60 | 142 | 23.6% | 4.4% | 0.89 | -6.5% | 310 | 1.48 | 15.1% | 77.4 | 11/11 | 1.00 | 0.73 | 0.16 | 4 | 11.0% | 0.51 | 0.76 | 22.5% | 21.1% | 19.3% | 22.4%/15.6% | 11.1 (interpolated) | pass | 0.351 (unverified) | n/a |
| 83 | `cfg_e936` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 53/99/0 | 152 | 26.7% | 4.9% | 0.96 | -5.4% | 350 | 1.56 | 16.7% | 84.3 | 9/9 | 1.00 | 0.70 | 0.26 | 4 | 10.2% | 0.62 | 0.63 | 25.7% | 24.4% | 23.0% | 23.8%/18.9% | 11.8 (interpolated) | pass | 0.412 (unverified) | n/a |
| 84 | `cfg_2509` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 24/93/59 | 176 | 28.5% | 5.2% | 0.87 | -8.6% | 466 | 1.39 | 20.1% | 97.3 | 11/11 | 1.00 | 0.70 | 0.17 | 4 | 6.2% | 0.78 | 0.69 | 27.0% | 25.5% | 14.7% | 27.1%/18.0% | 10.3 (interpolated) | pass | 0.332 (unverified) | n/a |
| 85 | `cfg_a503` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 40/74/58 | 172 | 24.3% | 4.5% | 0.93 | -5.2% | 336 | 1.48 | 15.6% | 93.4 | 12/12 | 1.00 | 0.79 | 0.14 | 4 | 8.2% | 0.63 | 0.63 | 23.3% | 21.8% | 18.7% | 23.8%/18.8% | 9.7 (interpolated) | pass | 0.386 (unverified) | n/a |
| 86 | `cfg_a098` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=22, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 13/88/47 | 148 | 25.1% | 4.7% | 0.91 | -7.0% | 307 | 1.49 | 14.7% | 80.1 | 11/11 | 1.00 | 0.68 | 0.23 | 3 | 9.9% | 0.59 | 0.79 | 24.2% | 22.8% | 13.2% | 23.7%/16.8% | 11.2 (interpolated) | pass | 0.373 (unverified) | n/a |
| 87 | `cfg_f6ae` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 12/77/37 | 126 | 24.3% | 4.5% | 0.98 | -5.4% | 488 | 1.61 | 12.4% | 68.6 | 10/10 | 1.00 | 0.70 | 0.29 | 4 | 4.7% | 0.82 | 0.65 | 23.1% | 21.8% | 12.6% | 21.3%/15.5% | 12.7 (interpolated) | pass | 0.428 (unverified) | n/a |
| 88 | `cfg_9ca0` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 50/40/43 | 133 | 26.0% | 4.8% | 0.94 | -6.8% | 275 | 1.50 | 13.8% | 73.5 | 10/10 | 1.00 | 0.76 | 0.17 | 4 | 5.9% | 0.77 | 0.54 | 24.4% | 22.9% | 12.7% | 22.9%/17.2% | 12.8 (interpolated) | pass | 0.387 (unverified) | n/a |
| 89 | `cfg_4e6b` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 33/44/52 | 129 | 22.7% | 4.3% | 0.83 | -5.6% | 266 | 1.48 | 13.5% | 69.9 | 11/11 | 1.00 | 0.76 | 0.07 | 5 | 10.5% | 0.53 | 0.64 | 20.5% | 19.5% | 9.6% | 20.9%/15.3% | 11.6 (interpolated) | pass | 0.301 (unverified) | n/a |
| 90 | `cfg_0bac` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 20/50/45 | 115 | 20.7% | 3.9% | 0.93 | -6.4% | 275 | 1.57 | 10.2% | 62.0 | 11/11 | 1.00 | 0.85 | 0.08 | 3 | 9.9% | 0.48 | 0.62 | 19.5% | 18.5% | 8.3% | 18.0%/13.0% | 12.3 (interpolated) | pass | 0.383 (unverified) | n/a |
| 91 | `cfg_09d4` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 42/43/88 | 173 | 30.5% | 5.6% | 0.86 | -8.3% | 173 | 1.40 | 21.3% | 95.8 | 10/10 | 1.00 | 0.76 | 0.10 | 4 | 11.3% | 0.61 | 0.57 | 29.0% | 27.4% | 25.7% | 27.7%/20.5% | 11.9 (interpolated) | pass | 0.330 (unverified) | n/a |
| 92 | `cfg_2bc9` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.0 | 27/48/130 | 205 | 26.8% | 4.9% | 0.83 | -13.0% | 353 | 1.35 | 20.6% | 113.8 | 8/8 | 1.00 | 0.80 | 0.03 | 3 | 7.5% | 0.69 | 0.72 | 24.3% | 21.8% | 11.9% | 22.1%/14.5% | 8.6 (interpolated) | pass | 0.306 (unverified) | n/a |
| 93 | `cfg_befa` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=none | 33/94/0 | 127 | 33.1% | 6.0% | 0.90 | -6.9% | 150 | 1.58 | 23.2% | 69.7 | 7/7 | 1.00 | 0.71 | 0.19 | 5 | 18.5% | 0.43 | 0.58 | 32.1% | 31.0% | 21.5% | 29.7%/22.3% | 16.4 (interpolated) | pass | 0.363 (unverified) | n/a |
| 94 | `cfg_43ab` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 20/88/49 | 157 | 26.0% | 4.8% | 0.83 | -10.6% | 567 | 1.39 | 18.7% | 87.6 | 11/11 | 1.00 | 0.68 | 0.15 | 4 | 7.5% | 0.75 | 0.74 | 24.6% | 24.1% | 18.7% | 23.3%/18.1% | 11.1 (interpolated) | pass | 0.307 (unverified) | n/a |
| 95 | `cfg_2384` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 38/73/68 | 179 | 32.3% | 5.9% | 1.06 | -6.2% | 128 | 1.50 | 18.8% | 98.8 | 12/12 | 1.00 | 0.79 | 0.27 | 4 | 13.9% | 0.54 | 0.58 | 30.1% | 28.8% | 20.9% | 26.6%/19.2% | 11.4 (interpolated) | pass | 0.505 (unverified) | n/a |
| 96 | `cfg_18cd` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=18, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 18/67/21 | 106 | 18.6% | 3.5% | 1.05 | -3.4% | 234 | 1.83 | 7.4% | 58.2 | 9/9 | 1.00 | 0.66 | 0.38 | 5 | 13.2% | 0.26 | 0.57 | 17.1% | 15.8% | 4.3% | 15.4%/11.5% | 12.0 (interpolated) | pass | 0.489 (unverified) | n/a |
| 97 | `cfg_ddfe` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 17/77/65 | 159 | 26.0% | 4.8% | 0.90 | -5.7% | 312 | 1.47 | 16.9% | 86.4 | 10/10 | 1.00 | 0.74 | 0.16 | 4 | 12.8% | 0.48 | 0.67 | 23.9% | 21.1% | 18.6% | 24.2%/15.9% | 10.1 (interpolated) | pass | 0.362 (unverified) | n/a |
| 98 | `cfg_0cd1` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 69/49/108 | 226 | 31.8% | 5.8% | 0.88 | -7.6% | 173 | 1.34 | 25.6% | 123.8 | 10/10 | 1.00 | 0.72 | 0.16 | 5 | 14.5% | 0.52 | 0.49 | 29.6% | 27.3% | 23.0% | 25.9%/18.9% | 9.2 (interpolated) | pass | 0.347 (unverified) | n/a |
| 99 | `cfg_7b6a` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 44/41/82 | 167 | 25.6% | 4.8% | 0.82 | -6.9% | 277 | 1.39 | 20.3% | 92.0 | 10/10 | 1.00 | 0.74 | 0.08 | 4 | 12.1% | 0.49 | 0.61 | 25.1% | 24.4% | 20.9% | 24.8%/18.3% | 10.6 (interpolated) | pass | 0.293 (unverified) | n/a |
| 100 | `cfg_d93c` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 33/49/45 | 127 | 27.2% | 5.0% | 0.86 | -7.4% | 275 | 1.49 | 17.4% | 69.8 | 9/9 | 1.00 | 0.74 | 0.12 | 4 | 5.0% | 0.82 | 0.56 | 25.6% | 24.5% | 11.3% | 24.7%/20.3% | 13.7 (interpolated) | pass | 0.323 (unverified) | n/a |
| 101 | `cfg_cb00` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=18, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 18/69/16 | 103 | 15.9% | 3.0% | 0.97 | -3.3% | 246 | 1.74 | 7.4% | 56.4 | 9/9 | 1.00 | 0.72 | 0.24 | 5 | 10.7% | 0.29 | 0.58 | 14.8% | 13.7% | 7.3% | 13.8%/10.1% | 11.3 (interpolated) | pass | 0.417 (unverified) | n/a |
| 102 | `cfg_0041` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 22/81/69 | 172 | 28.9% | 5.3% | 0.89 | -8.4% | 376 | 1.44 | 18.9% | 95.3 | 11/11 | 1.00 | 0.79 | 0.11 | 4 | 9.8% | 0.66 | 0.66 | 27.3% | 24.7% | 24.8% | 24.9%/18.7% | 11.3 (interpolated) | pass | 0.349 (unverified) | n/a |
| 103 | `cfg_e580` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=22, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 16/62/56 | 134 | 24.1% | 4.5% | 0.90 | -7.2% | 365 | 1.53 | 14.8% | 72.8 | 10/10 | 1.00 | 0.73 | 0.18 | 4 | 14.2% | 0.35 | 0.61 | 22.9% | 21.3% | 23.7% | 22.5%/16.5% | 11.6 (interpolated) | pass | 0.360 (unverified) | n/a |
| 104 | `cfg_3e97` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 12/62/43 | 117 | 20.7% | 3.9% | 0.89 | -6.0% | 246 | 1.57 | 11.1% | 64.1 | 10/10 | 1.00 | 0.77 | 0.11 | 3 | 8.5% | 0.57 | 0.76 | 19.5% | 18.5% | 11.0% | 18.5%/14.7% | 12.1 (interpolated) | pass | 0.348 (unverified) | n/a |
| 105 | `cfg_0a42` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 20/72/58 | 150 | 23.3% | 4.4% | 0.84 | -5.6% | 386 | 1.45 | 16.3% | 81.6 | 10/10 | 1.00 | 0.81 | 0.02 | 4 | 4.8% | 0.78 | 0.76 | 21.8% | 20.9% | 15.6% | 20.8%/13.1% | 10.5 (interpolated) | pass | 0.319 (unverified) | n/a |
| 106 | `cfg_9cd6` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=22, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 16/57/54 | 127 | 21.4% | 4.0% | 0.85 | -8.0% | 308 | 1.50 | 11.3% | 68.8 | 11/11 | 1.00 | 0.78 | 0.06 | 3 | 6.5% | 0.69 | 0.84 | 20.7% | 19.1% | 13.3% | 19.1%/13.0% | 11.4 (interpolated) | pass | 0.312 (unverified) | n/a |
| 107 | `cfg_a20b` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=22, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 26/57/85 | 168 | 30.2% | 5.5% | 0.86 | -7.5% | 367 | 1.43 | 21.3% | 92.6 | 10/10 | 1.00 | 0.69 | 0.17 | 4 | 13.3% | 0.52 | 0.63 | 28.0% | 27.5% | 31.4% | 28.9%/19.2% | 11.4 (interpolated) | pass | 0.322 (unverified) | n/a |
| 108 | `cfg_4fae` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 23/41/48 | 112 | 23.7% | 4.4% | 0.85 | -5.5% | 254 | 1.54 | 14.7% | 61.0 | 8/8 | 1.00 | 0.58 | 0.27 | 5 | 15.2% | 0.31 | 0.66 | 22.7% | 21.2% | 14.8% | 20.8%/15.9% | 14.0 (interpolated) | pass | 0.323 (unverified) | n/a |
| 109 | `cfg_8c46` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 18/50/47 | 115 | 22.4% | 4.2% | 0.87 | -4.9% | 304 | 1.51 | 12.4% | 63.0 | 9/9 | 1.00 | 0.62 | 0.25 | 4 | 11.7% | 0.45 | 0.69 | 20.8% | 19.9% | 16.4% | 20.5%/15.2% | 13.1 (interpolated) | pass | 0.329 (unverified) | n/a |
| 110 | `cfg_0f5d` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 18/91/51 | 160 | 26.2% | 4.9% | 0.89 | -7.4% | 373 | 1.44 | 19.3% | 86.4 | 10/10 | 1.00 | 0.69 | 0.19 | 3 | 11.1% | 0.56 | 0.65 | 25.2% | 23.4% | 20.1% | 23.1%/16.2% | 11.1 (interpolated) | pass | 0.349 (unverified) | n/a |
| 111 | `cfg_6080` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 19/49/58 | 126 | 24.7% | 4.6% | 0.92 | -9.8% | 356 | 1.50 | 13.1% | 68.7 | 10/10 | 1.00 | 0.83 | 0.09 | 3 | 6.8% | 0.74 | 0.74 | 23.3% | 21.8% | 22.6% | 21.8%/17.7% | 12.8 (interpolated) | pass | 0.373 (unverified) | n/a |
| 112 | `cfg_4c4a` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=25, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 6/80/43 | 129 | 26.9% | 5.0% | 1.11 | -7.4% | 277 | 1.72 | 12.8% | 71.1 | 8/8 | 1.00 | 0.88 | 0.24 | 3 | 12.5% | 0.51 | 0.61 | 26.5% | 25.7% | 11.9% | 25.9%/18.7% | 14.0 (interpolated) | pass | 0.552 (unverified) | n/a |
| 113 | `cfg_2334` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 13/56/45 | 114 | 20.2% | 3.8% | 0.86 | -8.8% | 275 | 1.53 | 10.3% | 62.0 | 10/10 | 1.00 | 0.76 | 0.10 | 3 | 9.3% | 0.49 | 0.72 | 19.4% | 17.6% | 6.3% | 17.3%/12.4% | 11.9 (interpolated) | pass | 0.327 (unverified) | n/a |
| 114 | `cfg_e1dc` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 15/70/42 | 127 | 21.7% | 4.1% | 0.88 | -5.1% | 184 | 1.51 | 12.2% | 69.4 | 9/9 | 1.00 | 0.70 | 0.18 | 5 | 10.2% | 0.52 | 0.68 | 20.3% | 19.2% | 11.7% | 20.0%/14.7% | 11.3 (interpolated) | pass | 0.337 (unverified) | n/a |
| 115 | `cfg_275f` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 43/33/50 | 126 | 22.2% | 4.2% | 0.91 | -3.7% | 127 | 1.53 | 12.0% | 68.5 | 9/9 | 1.00 | 0.73 | 0.18 | 5 | 11.8% | 0.45 | 0.59 | 21.1% | 19.9% | 5.2% | 19.2%/14.3% | 11.7 (interpolated) | pass | 0.363 (unverified) | n/a |
| 116 | `cfg_f9bf` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 39/94/79 | 212 | 24.9% | 4.6% | 0.87 | -6.1% | 337 | 1.35 | 18.9% | 116.5 | 9/9 | 1.00 | 0.74 | 0.13 | 3 | 7.6% | 0.70 | 0.72 | 23.9% | 23.1% | 19.3% | 23.3%/16.2% | 8.3 (interpolated) | pass | 0.334 (unverified) | n/a |
| 117 | `cfg_1626` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=22, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 9/64/54 | 127 | 21.0% | 3.9% | 0.83 | -8.0% | 308 | 1.49 | 11.5% | 68.8 | 10/10 | 1.00 | 0.77 | 0.06 | 3 | 6.1% | 0.71 | 0.86 | 19.5% | 18.5% | 13.9% | 18.4%/14.0% | 11.2 (interpolated) | pass | 0.299 (unverified) | n/a |
| 118 | `cfg_3706` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 17/78/40 | 135 | 23.0% | 4.3% | 0.84 | -8.6% | 388 | 1.44 | 16.3% | 73.3 | 10/10 | 1.00 | 0.82 | 0.02 | 3 | 4.3% | 0.83 | 0.76 | 22.0% | 19.9% | 14.3% | 20.2%/14.1% | 11.3 (interpolated) | pass | 0.321 (unverified) | n/a |
| 119 | `cfg_ef22` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 42/68/104 | 214 | 34.7% | 6.2% | 0.94 | -8.1% | 225 | 1.38 | 27.0% | 117.4 | 9/9 | 1.00 | 0.70 | 0.24 | 4 | 13.8% | 0.57 | 0.54 | 30.7% | 28.8% | 23.2% | 27.7%/21.6% | 10.2 (interpolated) | pass | 0.395 (unverified) | n/a |
| 120 | `cfg_9cec` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 25/60/59 | 144 | 26.5% | 4.9% | 0.90 | -6.5% | 275 | 1.46 | 15.1% | 79.7 | 10/10 | 1.00 | 0.65 | 0.25 | 4 | 7.9% | 0.70 | 0.56 | 25.2% | 23.7% | 12.6% | 23.4%/16.2% | 12.2 (interpolated) | pass | 0.355 (unverified) | n/a |
| 121 | `cfg_7aee` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 35/74/73 | 182 | 28.6% | 5.2% | 0.85 | -6.7% | 298 | 1.41 | 19.3% | 100.8 | 11/11 | 1.00 | 0.69 | 0.16 | 4 | 4.2% | 0.85 | 0.63 | 26.5% | 25.3% | 18.1% | 25.1%/16.9% | 10.2 (interpolated) | pass | 0.320 (unverified) | n/a |
| 122 | `cfg_316c` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 12/64/33 | 109 | 19.9% | 3.8% | 0.85 | -5.9% | 260 | 1.55 | 11.2% | 59.8 | 10/10 | 1.00 | 0.71 | 0.14 | 3 | 8.4% | 0.55 | 0.77 | 19.1% | 18.4% | 9.8% | 18.4%/13.4% | 12.7 (interpolated) | pass | 0.318 (unverified) | n/a |
| 123 | `cfg_e453` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 51/39/80 | 170 | 29.1% | 5.3% | 0.94 | -12.3% | 277 | 1.42 | 20.1% | 94.5 | 11/11 | 1.00 | 0.75 | 0.19 | 4 | 16.6% | 0.44 | 0.52 | 27.1% | 25.1% | 17.1% | 25.5%/17.9% | 11.5 (interpolated) | pass | 0.395 (unverified) | n/a |
| 124 | `cfg_2787` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=22, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 12/85/64 | 161 | 22.7% | 4.2% | 0.84 | -6.9% | 353 | 1.44 | 14.8% | 86.8 | 11/11 | 1.00 | 0.73 | 0.11 | 3 | 7.8% | 0.65 | 0.87 | 20.9% | 19.0% | 14.8% | 20.8%/13.9% | 9.0 (interpolated) | pass | 0.311 (unverified) | n/a |
| 125 | `cfg_9400` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.0 | 39/28/115 | 182 | 27.7% | 5.1% | 0.90 | -8.6% | 353 | 1.43 | 17.2% | 99.2 | 8/8 | 0.88 | 0.83 | 0.07 | 3 | 4.7% | 0.82 | 0.62 | 25.5% | 24.3% | 28.5% | 25.6%/17.5% | 10.1 (interpolated) | pass | 0.354 (unverified) | n/a |
| 126 | `cfg_0108` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 18/89/70 | 177 | 24.3% | 4.5% | 0.82 | -8.8% | 386 | 1.40 | 19.6% | 96.3 | 10/10 | 1.00 | 0.72 | 0.10 | 4 | 10.9% | 0.51 | 0.64 | 22.7% | 21.4% | 20.1% | 22.0%/15.2% | 9.5 (interpolated) | pass | 0.296 (unverified) | n/a |
| 127 | `cfg_d3f3` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 27/67/65 | 159 | 23.7% | 4.4% | 0.86 | -5.8% | 240 | 1.43 | 16.3% | 86.3 | 11/11 | 1.00 | 0.76 | 0.10 | 3 | 10.6% | 0.54 | 0.69 | 22.2% | 20.0% | 16.5% | 21.6%/14.1% | 9.6 (interpolated) | pass | 0.326 (unverified) | n/a |
| 128 | `cfg_8f1b` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=22, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 14/66/50 | 130 | 18.9% | 3.6% | 0.80 | -6.0% | 277 | 1.47 | 11.7% | 71.0 | 11/11 | 1.00 | 0.62 | 0.18 | 3 | 6.3% | 0.65 | 0.87 | 18.0% | 17.0% | 9.9% | 17.1%/12.0% | 9.7 (interpolated) | pass | 0.277 (unverified) | n/a |
| 129 | `cfg_3f18` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 18/92/78 | 188 | 25.9% | 4.8% | 0.78 | -8.4% | 386 | 1.34 | 20.4% | 102.3 | 11/11 | 1.00 | 0.70 | 0.08 | 4 | 9.0% | 0.64 | 0.75 | 24.3% | 23.2% | 29.8% | 22.8%/17.3% | 9.4 (interpolated) | pass | 0.270 (unverified) | n/a |
| 130 | `cfg_01f4` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 17/69/25 | 111 | 17.7% | 3.4% | 0.97 | -5.2% | 437 | 1.72 | 7.7% | 61.4 | 9/9 | 1.00 | 0.63 | 0.34 | 4 | 8.0% | 0.54 | 0.66 | 16.9% | 15.4% | 11.7% | 15.6%/12.2% | 10.7 (interpolated) | pass | 0.416 (unverified) | n/a |
| 131 | `cfg_d1dd` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=2.0 | 51/67/81 | 199 | 37.6% | 6.7% | 0.97 | -6.4% | 186 | 1.42 | 27.6% | 108.4 | 9/9 | 1.00 | 0.77 | 0.20 | 5 | 16.9% | 0.51 | 0.47 | 36.0% | 34.3% | 23.5% | 34.2%/26.9% | 11.7 (interpolated) | pass | 0.422 (unverified) | n/a |
| 132 | `cfg_78e3` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 28/76/67 | 171 | 27.8% | 5.1% | 0.94 | -5.7% | 303 | 1.44 | 18.0% | 94.4 | 11/11 | 1.00 | 0.66 | 0.29 | 4 | 17.0% | 0.35 | 0.59 | 26.7% | 25.3% | 17.3% | 24.7%/18.0% | 11.3 (interpolated) | pass | 0.397 (unverified) | n/a |
| 133 | `cfg_c83e` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 19/42/45 | 106 | 22.8% | 4.3% | 0.89 | -5.9% | 456 | 1.60 | 11.1% | 57.6 | 11/11 | 1.00 | 0.72 | 0.16 | 5 | 7.2% | 0.66 | 0.64 | 21.9% | 21.0% | 12.7% | 20.6%/14.5% | 13.7 (interpolated) | pass | 0.350 (unverified) | n/a |
| 134 | `cfg_71f7` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=22, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 24/51/39 | 114 | 25.0% | 4.6% | 0.85 | -7.0% | 275 | 1.49 | 16.2% | 63.3 | 9/9 | 1.00 | 0.72 | 0.13 | 4 | 9.7% | 0.61 | 0.69 | 23.4% | 22.3% | 11.9% | 24.0%/19.1% | 14.3 (interpolated) | pass | 0.317 (unverified) | n/a |
| 135 | `cfg_833e` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 24/58/25 | 107 | 28.5% | 5.2% | 1.19 | -5.5% | 455 | 1.93 | 10.4% | 58.7 | 10/10 | 1.00 | 0.83 | 0.36 | 4 | 6.5% | 0.76 | 0.55 | 27.6% | 26.8% | 13.0% | 24.9%/19.6% | 16.5 (interpolated) | pass | 0.627 (unverified) | n/a |
| 136 | `cfg_8be3` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 16/87/59 | 162 | 23.7% | 4.4% | 0.81 | -5.2% | 394 | 1.43 | 14.9% | 88.8 | 10/10 | 0.90 | 0.70 | 0.10 | 5 | 11.5% | 0.49 | 0.75 | 22.2% | 20.8% | 10.0% | 22.0%/14.6% | 10.0 (interpolated) | pass | 0.291 (unverified) | n/a |
| 137 | `cfg_f496` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 50/38/57 | 145 | 23.9% | 4.5% | 0.89 | -5.9% | 275 | 1.45 | 13.7% | 79.8 | 10/10 | 1.00 | 0.64 | 0.25 | 4 | 7.5% | 0.68 | 0.59 | 23.2% | 21.8% | 9.9% | 20.6%/14.2% | 11.4 (interpolated) | pass | 0.344 (unverified) | n/a |
| 138 | `cfg_5318` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=none | 34/79/0 | 113 | 31.3% | 5.7% | 0.90 | -7.0% | 249 | 1.61 | 20.3% | 62.0 | 9/9 | 1.00 | 0.72 | 0.18 | 4 | 16.1% | 0.42 | 0.55 | 30.1% | 28.6% | 26.0% | 27.9%/19.5% | 16.7 (interpolated) | pass | 0.370 (unverified) | n/a |
| 139 | `cfg_42c0` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=22, entry_z=-3.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 27/39/61 | 127 | 22.9% | 4.3% | 0.81 | -5.9% | 365 | 1.47 | 16.1% | 69.4 | 10/10 | 1.00 | 0.70 | 0.12 | 4 | 11.0% | 0.46 | 0.67 | 21.3% | 20.3% | 28.8% | 20.2%/15.1% | 11.5 (interpolated) | pass | 0.290 (unverified) | n/a |
| 140 | `cfg_45d0` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 56/88/93 | 237 | 31.4% | 5.7% | 0.90 | -7.1% | 215 | 1.36 | 24.4% | 130.8 | 9/9 | 1.00 | 0.74 | 0.15 | 5 | 13.3% | 0.56 | 0.55 | 28.8% | 26.7% | 32.4% | 24.5%/18.7% | 8.6 (interpolated) | pass | 0.362 (unverified) | n/a |
| 141 | `cfg_3788` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 36/104/91 | 231 | 27.6% | 5.1% | 0.77 | -5.4% | 457 | 1.31 | 24.6% | 126.3 | 10/10 | 1.00 | 0.66 | 0.10 | 4 | 9.3% | 0.66 | 0.69 | 26.2% | 24.6% | 25.7% | 22.7%/15.8% | 8.0 (interpolated) | pass | 0.260 (unverified) | n/a |
| 142 | `cfg_ba37` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=12, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 48/47/91 | 186 | 37.5% | 6.7% | 1.01 | -7.4% | 128 | 1.46 | 22.7% | 103.2 | 8/8 | 1.00 | 0.76 | 0.25 | 5 | 20.2% | 0.42 | 0.47 | 35.4% | 32.7% | 32.4% | 31.2%/23.2% | 12.2 (interpolated) | pass | 0.459 (unverified) | n/a |
| 143 | `cfg_cca7` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 17/76/32 | 125 | 19.9% | 3.8% | 0.80 | -5.2% | 275 | 1.46 | 12.3% | 68.9 | 10/10 | 1.00 | 0.72 | 0.08 | 4 | 6.3% | 0.67 | 0.75 | 18.6% | 17.9% | 13.6% | 18.0%/13.4% | 10.8 (interpolated) | pass | 0.277 (unverified) | n/a |
| 144 | `cfg_510f` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 8/89/24 | 121 | 14.8% | 2.9% | 0.82 | -5.2% | 296 | 1.51 | 8.9% | 66.2 | 9/9 | 1.00 | 0.49 | 0.32 | 4 | 7.0% | 0.52 | 0.69 | 14.1% | 12.9% | 10.4% | 13.2%/10.0% | 8.6 (interpolated) | pass | 0.285 (unverified) | n/a |
| 145 | `cfg_a6af` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=25, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 11/75/43 | 129 | 26.4% | 4.9% | 1.11 | -7.0% | 277 | 1.72 | 12.7% | 70.9 | 9/9 | 1.00 | 0.92 | 0.19 | 3 | 13.1% | 0.48 | 0.61 | 25.6% | 24.3% | 10.8% | 24.6%/19.4% | 13.5 (interpolated) | pass | 0.549 (unverified) | n/a |
| 146 | `cfg_51fa` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 58/44/94 | 196 | 32.1% | 5.8% | 0.94 | -5.7% | 158 | 1.41 | 22.5% | 107.7 | 11/11 | 1.00 | 0.70 | 0.24 | 5 | 22.2% | 0.28 | 0.50 | 28.5% | 26.7% | 24.9% | 25.0%/18.4% | 10.2 (interpolated) | pass | 0.391 (unverified) | n/a |
| 147 | `cfg_91ac` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 31/93/52 | 176 | 26.0% | 4.8% | 0.79 | -5.5% | 251 | 1.37 | 20.4% | 96.5 | 11/11 | 1.00 | 0.73 | 0.06 | 5 | 8.9% | 0.65 | 0.73 | 24.7% | 23.3% | 20.8% | 23.4%/18.0% | 9.6 (interpolated) | pass | 0.277 (unverified) | n/a |
| 148 | `cfg_5422` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 42/122/0 | 164 | 24.4% | 4.5% | 0.84 | -7.9% | 350 | 1.42 | 18.5% | 90.8 | 8/8 | 0.88 | 0.69 | 0.15 | 4 | 7.1% | 0.72 | 0.71 | 22.9% | 21.9% | 28.3% | 22.1%/16.2% | 9.6 (interpolated) | pass | 0.308 (unverified) | n/a |
| 149 | `cfg_ea31` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=18, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 34/28/45 | 107 | 18.8% | 3.6% | 0.83 | -5.0% | 263 | 1.53 | 9.9% | 58.3 | 11/11 | 1.00 | 0.69 | 0.14 | 4 | 11.1% | 0.38 | 0.70 | 17.4% | 16.2% | 20.9% | 17.8%/13.6% | 11.6 (interpolated) | pass | 0.298 (unverified) | n/a |
| 150 | `cfg_a180` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 22/81/59 | 162 | 23.4% | 4.4% | 0.80 | -5.4% | 366 | 1.42 | 14.8% | 88.9 | 11/11 | 0.91 | 0.73 | 0.07 | 5 | 11.3% | 0.49 | 0.76 | 21.9% | 20.7% | 8.7% | 20.5%/14.9% | 9.9 (interpolated) | pass | 0.287 (unverified) | n/a |
| 151 | `cfg_1795` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 11/52/42 | 105 | 17.2% | 3.3% | 0.81 | -7.1% | 317 | 1.52 | 11.7% | 57.7 | 10/10 | 1.00 | 0.63 | 0.18 | 4 | 8.6% | 0.48 | 0.82 | 15.8% | 15.0% | 7.6% | 15.6%/11.5% | 11.2 (interpolated) | pass | 0.287 (unverified) | n/a |
| 152 | `cfg_15d6` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=22, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=none | 38/89/0 | 127 | 29.8% | 5.4% | 0.81 | -7.6% | 384 | 1.50 | 23.0% | 69.3 | 8/8 | 1.00 | 0.71 | 0.10 | 4 | 14.7% | 0.50 | 0.62 | 27.8% | 26.7% | 17.1% | 27.5%/19.6% | 14.5 (interpolated) | pass | 0.296 (unverified) | n/a |
| 153 | `cfg_1d0e` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 46/44/83 | 173 | 32.4% | 5.9% | 0.96 | -9.7% | 277 | 1.45 | 21.2% | 96.0 | 10/10 | 1.00 | 0.76 | 0.20 | 4 | 12.7% | 0.56 | 0.54 | 29.8% | 28.8% | 25.1% | 28.5%/21.4% | 12.1 (interpolated) | pass | 0.414 (unverified) | n/a |
| 154 | `cfg_e897` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 21/64/42 | 127 | 19.4% | 3.7% | 0.81 | -5.1% | 317 | 1.45 | 11.9% | 69.4 | 10/10 | 1.00 | 0.67 | 0.14 | 4 | 8.3% | 0.57 | 0.75 | 18.3% | 16.9% | 8.8% | 18.0%/14.1% | 10.5 (interpolated) | pass | 0.285 (unverified) | n/a |
| 155 | `cfg_a4a2` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=22, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 24/86/0 | 110 | 18.8% | 3.6% | 0.80 | -6.5% | 466 | 1.49 | 12.3% | 59.9 | 11/11 | 1.00 | 0.66 | 0.14 | 4 | 9.7% | 0.50 | 0.85 | 17.9% | 16.1% | 10.5% | 16.8%/10.6% | 11.1 (interpolated) | pass | 0.292 (unverified) | n/a |
| 156 | `cfg_164a` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 12/60/37 | 109 | 18.0% | 3.4% | 0.86 | -4.3% | 245 | 1.57 | 10.4% | 59.6 | 10/10 | 1.00 | 0.74 | 0.12 | 4 | 9.4% | 0.45 | 0.74 | 16.9% | 16.0% | 9.6% | 15.4%/11.5% | 11.1 (interpolated) | pass | 0.329 (unverified) | n/a |
| 157 | `cfg_b8e3` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=22, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 23/58/50 | 131 | 19.6% | 3.7% | 0.86 | -4.7% | 298 | 1.50 | 11.7% | 71.7 | 12/12 | 1.00 | 0.66 | 0.20 | 3 | 7.2% | 0.61 | 0.80 | 18.6% | 17.6% | 9.9% | 17.8%/11.5% | 9.9 (interpolated) | pass | 0.332 (unverified) | n/a |
| 158 | `cfg_4945` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 20/109/43 | 172 | 23.4% | 4.4% | 0.78 | -6.6% | 386 | 1.40 | 17.5% | 94.2 | 11/11 | 1.00 | 0.61 | 0.17 | 4 | 11.3% | 0.50 | 0.78 | 21.7% | 20.9% | 21.6% | 20.3%/14.3% | 9.1 (interpolated) | pass | 0.273 (unverified) | n/a |
| 159 | `cfg_0954` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 33/50/50 | 133 | 26.1% | 4.8% | 0.78 | -7.6% | 169 | 1.39 | 18.0% | 74.4 | 9/9 | 1.00 | 0.71 | 0.07 | 4 | 4.9% | 0.84 | 0.66 | 25.2% | 24.0% | 12.0% | 24.8%/17.7% | 13.0 (interpolated) | pass | 0.264 (unverified) | n/a |
| 160 | `cfg_fe21` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=22, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 10/110/27 | 147 | 16.3% | 3.1% | 0.78 | -7.1% | 308 | 1.44 | 10.7% | 80.9 | 11/11 | 1.00 | 0.65 | 0.13 | 4 | 8.9% | 0.45 | 0.66 | 13.9% | 12.3% | 15.7% | 13.9%/8.6% | 7.8 (interpolated) | pass | 0.268 (unverified) | n/a |
| 161 | `cfg_0aed` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=22, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 18/91/0 | 109 | 18.5% | 3.5% | 0.79 | -6.4% | 466 | 1.48 | 12.6% | 59.5 | 10/10 | 1.00 | 0.60 | 0.19 | 4 | 8.5% | 0.51 | 0.86 | 17.6% | 15.7% | 11.7% | 15.5%/11.3% | 11.1 (interpolated) | pass | 0.281 (unverified) | n/a |
| 162 | `cfg_f7cb` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=22, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=2.0 | 23/69/37 | 129 | 20.6% | 3.9% | 0.80 | -7.2% | 388 | 1.42 | 12.8% | 70.3 | 10/10 | 1.00 | 0.72 | 0.08 | 3 | 5.8% | 0.74 | 0.89 | 19.6% | 18.7% | 9.7% | 18.8%/14.2% | 10.6 (interpolated) | pass | 0.291 (unverified) | n/a |
| 163 | `cfg_2563` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 34/35/48 | 117 | 23.2% | 4.3% | 0.84 | -5.7% | 127 | 1.53 | 14.2% | 64.6 | 9/9 | 1.00 | 0.74 | 0.10 | 4 | 13.9% | 0.38 | 0.65 | 21.4% | 20.6% | 14.3% | 21.0%/14.6% | 13.0 (interpolated) | pass | 0.313 (unverified) | n/a |
| 164 | `cfg_2d3c` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 20/122/0 | 142 | 22.3% | 4.2% | 0.77 | -8.6% | 386 | 1.46 | 16.4% | 77.6 | 10/10 | 1.00 | 0.65 | 0.13 | 4 | 8.4% | 0.63 | 0.78 | 21.6% | 20.9% | 24.8% | 20.5%/13.3% | 10.7 (interpolated) | pass | 0.264 (unverified) | n/a |
| 165 | `cfg_8638` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=22, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 23/84/0 | 107 | 22.3% | 4.2% | 0.86 | -7.2% | 466 | 1.56 | 12.3% | 58.6 | 9/9 | 1.00 | 0.68 | 0.18 | 3 | 5.1% | 0.80 | 0.81 | 20.3% | 19.3% | 20.3% | 19.3%/13.1% | 13.0 (interpolated) | pass | 0.330 (unverified) | n/a |
| 166 | `cfg_9136` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 14/83/24 | 121 | 13.3% | 2.6% | 0.75 | -5.5% | 312 | 1.46 | 8.7% | 66.2 | 10/10 | 1.00 | 0.53 | 0.22 | 4 | 6.1% | 0.53 | 0.75 | 12.3% | 11.5% | 9.4% | 11.9%/9.1% | 7.8 (interpolated) | pass | 0.237 (unverified) | n/a |
| 167 | `cfg_8d7e` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 43/38/71 | 152 | 29.2% | 5.3% | 0.93 | -6.6% | 336 | 1.49 | 18.5% | 83.0 | 11/11 | 1.00 | 0.71 | 0.22 | 4 | 18.9% | 0.34 | 0.53 | 27.2% | 26.0% | 18.3% | 25.6%/19.9% | 12.3 (interpolated) | pass | 0.385 (unverified) | n/a |
| 168 | `cfg_5b62` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 25/72/67 | 164 | 23.6% | 4.4% | 0.76 | -7.5% | 157 | 1.37 | 17.7% | 89.6 | 10/10 | 1.00 | 0.65 | 0.10 | 4 | 3.4% | 0.86 | 0.80 | 21.9% | 19.9% | 42.1% | 20.6%/14.2% | 9.3 (interpolated) | pass | 0.252 (unverified) | n/a |
| 169 | `cfg_fd03` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 30/31/45 | 106 | 20.5% | 3.9% | 0.81 | -6.7% | 456 | 1.54 | 10.4% | 57.5 | 12/12 | 1.00 | 0.71 | 0.10 | 5 | 6.1% | 0.69 | 0.69 | 19.6% | 18.5% | 10.1% | 18.6%/13.3% | 12.9 (interpolated) | pass | 0.288 (unverified) | n/a |
| 170 | `cfg_c50f` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=22, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 6/113/28 | 147 | 16.0% | 3.1% | 0.77 | -7.1% | 308 | 1.43 | 10.8% | 80.8 | 10/10 | 0.90 | 0.61 | 0.17 | 4 | 8.5% | 0.47 | 0.66 | 13.7% | 12.2% | 15.2% | 13.3%/8.4% | 7.6 (interpolated) | pass | 0.260 (unverified) | n/a |
| 171 | `cfg_6a3f` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 31/120/0 | 151 | 30.1% | 5.5% | 0.89 | -9.9% | 275 | 1.47 | 21.2% | 82.7 | 9/9 | 1.00 | 0.75 | 0.14 | 3 | 10.9% | 0.66 | 0.54 | 28.4% | 26.5% | 29.6% | 27.0%/22.1% | 12.2 (interpolated) | pass | 0.352 (unverified) | n/a |
| 172 | `cfg_4232` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 16/74/17 | 107 | 15.6% | 3.0% | 0.89 | -4.3% | 437 | 1.66 | 7.7% | 59.6 | 9/9 | 1.00 | 0.63 | 0.25 | 4 | 7.0% | 0.54 | 0.68 | 14.7% | 13.8% | 14.0% | 14.2%/10.3% | 10.1 (interpolated) | pass | 0.345 (unverified) | n/a |
| 173 | `cfg_72ac` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 26/46/40 | 112 | 25.9% | 4.8% | 0.89 | -6.1% | 193 | 1.57 | 15.3% | 61.6 | 8/8 | 1.00 | 0.72 | 0.17 | 5 | 17.2% | 0.31 | 0.61 | 24.5% | 23.9% | 13.4% | 23.7%/17.4% | 15.2 (interpolated) | pass | 0.354 (unverified) | n/a |
| 174 | `cfg_9934` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 55/96/69 | 220 | 27.4% | 5.0% | 0.80 | -7.4% | 234 | 1.31 | 24.7% | 120.9 | 9/9 | 1.00 | 0.65 | 0.15 | 4 | 7.0% | 0.75 | 0.64 | 24.6% | 23.6% | 24.3% | 23.6%/18.4% | 8.7 (interpolated) | pass | 0.289 (unverified) | n/a |
| 175 | `cfg_f55d` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 40/22/42 | 104 | 17.1% | 3.3% | 0.78 | -5.2% | 271 | 1.48 | 9.7% | 56.7 | 10/10 | 1.00 | 0.67 | 0.11 | 4 | 5.6% | 0.67 | 0.76 | 16.0% | 15.1% | 6.5% | 14.9%/11.4% | 11.1 (interpolated) | pass | 0.262 (unverified) | n/a |
| 176 | `cfg_9b18` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 24/63/49 | 136 | 24.1% | 4.5% | 0.77 | -6.8% | 566 | 1.38 | 15.2% | 75.3 | 10/10 | 1.00 | 0.70 | 0.07 | 4 | 4.3% | 0.85 | 0.63 | 23.0% | 20.6% | 13.2% | 22.1%/15.9% | 11.9 (interpolated) | pass | 0.256 (unverified) | n/a |
| 177 | `cfg_10b8` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 12/121/0 | 133 | 27.2% | 5.0% | 0.87 | -12.3% | 437 | 1.54 | 15.7% | 73.7 | 10/10 | 1.00 | 0.65 | 0.22 | 4 | 6.9% | 0.78 | 0.73 | 25.7% | 25.2% | 26.1% | 24.4%/19.0% | 12.8 (interpolated) | pass | 0.344 (unverified) | n/a |
| 178 | `cfg_a49a` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=2.0 | 36/40/48 | 124 | 21.9% | 4.1% | 0.79 | -11.4% | 173 | 1.43 | 17.6% | 68.0 | 10/10 | 1.00 | 0.75 | 0.04 | 4 | 11.5% | 0.49 | 0.62 | 21.4% | 20.0% | 8.1% | 20.2%/14.7% | 12.3 (interpolated) | pass | 0.278 (unverified) | n/a |
| 179 | `cfg_b784` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 60/52/102 | 214 | 29.1% | 5.3% | 0.83 | -8.4% | 225 | 1.33 | 25.3% | 117.9 | 10/10 | 1.00 | 0.66 | 0.17 | 4 | 9.4% | 0.67 | 0.59 | 27.1% | 26.1% | 18.1% | 25.2%/18.1% | 9.2 (interpolated) | pass | 0.301 (unverified) | n/a |
| 180 | `cfg_db0b` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 46/83/64 | 193 | 22.6% | 4.2% | 0.76 | -7.5% | 467 | 1.29 | 21.3% | 104.6 | 9/9 | 1.00 | 0.67 | 0.09 | 3 | 7.4% | 0.69 | 0.77 | 21.4% | 20.1% | 22.4% | 22.2%/16.1% | 8.1 (interpolated) | pass | 0.255 (unverified) | n/a |
| 181 | `cfg_11ac` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=12, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 54/55/109 | 218 | 32.1% | 5.8% | 0.90 | -7.7% | 173 | 1.35 | 25.9% | 120.5 | 9/9 | 1.00 | 0.64 | 0.25 | 4 | 20.3% | 0.35 | 0.55 | 29.9% | 26.9% | 25.4% | 23.5%/17.0% | 9.7 (interpolated) | pass | 0.359 (unverified) | n/a |
| 182 | `cfg_361e` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=2.0 | 24/52/46 | 122 | 23.9% | 4.4% | 0.84 | -12.0% | 213 | 1.45 | 18.3% | 68.1 | 9/9 | 1.00 | 0.74 | 0.10 | 4 | 12.5% | 0.49 | 0.64 | 22.7% | 22.2% | 7.2% | 21.4%/14.5% | 13.0 (interpolated) | pass | 0.318 (unverified) | n/a |
| 183 | `cfg_6c61` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=none | 44/70/0 | 114 | 28.7% | 5.3% | 0.86 | -6.9% | 318 | 1.59 | 19.6% | 61.6 | 10/10 | 1.00 | 0.74 | 0.12 | 4 | 13.2% | 0.47 | 0.56 | 27.7% | 26.2% | 25.8% | 25.7%/19.5% | 15.9 (interpolated) | pass | 0.339 (unverified) | n/a |
| 184 | `cfg_125c` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 15/94/80 | 189 | 20.1% | 3.8% | 0.85 | -5.7% | 308 | 1.42 | 11.5% | 103.1 | 10/10 | 1.00 | 0.62 | 0.23 | 3 | 7.6% | 0.60 | 0.67 | 19.0% | 16.6% | 17.9% | 19.0%/13.0% | 7.5 (interpolated) | pass | 0.319 (unverified) | n/a |
| 185 | `cfg_c50b` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 32/56/81 | 169 | 22.6% | 4.2% | 0.76 | -7.1% | 400 | 1.35 | 21.4% | 92.0 | 10/10 | 1.00 | 0.70 | 0.06 | 4 | 12.9% | 0.39 | 0.64 | 21.5% | 20.0% | 17.2% | 18.6%/12.4% | 9.1 (interpolated) | pass | 0.255 (unverified) | n/a |
| 186 | `cfg_fab2` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=none | 33/67/0 | 100 | 26.5% | 4.9% | 0.86 | -5.8% | 249 | 1.61 | 17.9% | 54.6 | 8/8 | 0.88 | 0.71 | 0.15 | 5 | 16.3% | 0.33 | 0.64 | 25.8% | 23.9% | 24.1% | 23.9%/17.4% | 16.1 (interpolated) | pass | 0.337 (unverified) | n/a |
| 187 | `cfg_c49f` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=25, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 18/81/68 | 167 | 26.2% | 4.8% | 0.90 | -5.7% | 277 | 1.47 | 17.8% | 91.4 | 10/10 | 1.00 | 0.61 | 0.29 | 4 | 11.6% | 0.52 | 0.66 | 22.8% | 21.3% | 18.9% | 24.2%/18.7% | 10.4 (interpolated) | pass | 0.357 (unverified) | n/a |
| 188 | `cfg_a533` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=22, entry_z=-2.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 97/15/88 | 200 | 25.8% | 4.8% | 0.86 | -5.6% | 240 | 1.36 | 18.6% | 108.5 | 8/8 | 1.00 | 0.67 | 0.19 | 4 | 10.3% | 0.57 | 0.68 | 24.8% | 22.9% | 19.6% | 24.0%/17.7% | 8.8 (interpolated) | pass | 0.327 (unverified) | n/a |
| 189 | `cfg_be50` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=none | 43/76/0 | 119 | 26.8% | 4.9% | 0.82 | -7.6% | 216 | 1.49 | 20.8% | 65.3 | 9/9 | 1.00 | 0.55 | 0.27 | 5 | 13.0% | 0.46 | 0.49 | 25.8% | 24.8% | 19.5% | 25.5%/19.0% | 15.1 (interpolated) | pass | 0.305 (unverified) | n/a |
| 190 | `cfg_3e81` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 26/87/0 | 113 | 25.0% | 4.6% | 0.94 | -9.8% | 275 | 1.60 | 12.8% | 62.1 | 10/10 | 0.90 | 0.85 | 0.09 | 4 | 6.1% | 0.76 | 0.70 | 23.7% | 23.2% | 22.2% | 23.8%/16.4% | 14.4 (interpolated) | pass | 0.395 (unverified) | n/a |
| 191 | `cfg_f108` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 18/101/66 | 185 | 23.2% | 4.3% | 0.84 | -5.4% | 332 | 1.38 | 17.4% | 101.2 | 8/8 | 1.00 | 0.56 | 0.27 | 4 | 13.7% | 0.39 | 0.72 | 22.2% | 20.5% | 23.8% | 19.3%/13.5% | 8.4 (interpolated) | pass | 0.310 (unverified) | n/a |
| 192 | `cfg_b093` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=2.0 | 24/47/45 | 116 | 23.1% | 4.3% | 0.84 | -10.4% | 173 | 1.50 | 17.5% | 63.8 | 9/9 | 1.00 | 0.65 | 0.18 | 4 | 12.5% | 0.44 | 0.67 | 21.7% | 20.3% | 15.1% | 22.1%/14.8% | 13.0 (interpolated) | pass | 0.301 (unverified) | n/a |
| 193 | `cfg_7726` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 42/105/0 | 147 | 24.0% | 4.5% | 0.78 | -10.9% | 467 | 1.39 | 19.7% | 81.8 | 8/8 | 1.00 | 0.71 | 0.07 | 3 | 5.9% | 0.81 | 0.74 | 23.4% | 21.7% | 18.0% | 22.8%/18.0% | 11.1 (interpolated) | pass | 0.281 (unverified) | n/a |
| 194 | `cfg_5fea` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=2.0 | 31/60/66 | 157 | 26.4% | 4.9% | 0.80 | -10.4% | 230 | 1.38 | 22.3% | 85.9 | 9/9 | 1.00 | 0.68 | 0.12 | 3 | 16.3% | 0.38 | 0.55 | 25.7% | 24.3% | 17.9% | 23.4%/17.1% | 11.3 (interpolated) | pass | 0.287 (unverified) | n/a |
| 195 | `cfg_9dcb` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=25, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 25/94/66 | 185 | 23.8% | 4.4% | 0.85 | -5.4% | 286 | 1.39 | 17.2% | 101.0 | 9/9 | 1.00 | 0.57 | 0.27 | 4 | 13.1% | 0.40 | 0.69 | 22.3% | 21.3% | 24.5% | 19.6%/13.9% | 8.5 (interpolated) | pass | 0.321 (unverified) | n/a |
| 196 | `cfg_40b3` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 11/98/80 | 189 | 20.1% | 3.8% | 0.85 | -5.7% | 308 | 1.42 | 11.6% | 103.0 | 9/9 | 1.00 | 0.59 | 0.27 | 3 | 7.7% | 0.60 | 0.67 | 18.4% | 16.0% | 17.9% | 18.6%/14.2% | 7.3 (interpolated) | pass | 0.319 (unverified) | n/a |
| 197 | `cfg_7b64` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 38/66/67 | 171 | 25.9% | 4.8% | 0.90 | -5.8% | 278 | 1.42 | 17.6% | 94.2 | 12/12 | 1.00 | 0.67 | 0.23 | 4 | 16.4% | 0.33 | 0.61 | 24.0% | 22.6% | 15.2% | 21.1%/15.4% | 10.3 (interpolated) | pass | 0.361 (unverified) | n/a |
| 198 | `cfg_d4aa` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 17/96/0 | 113 | 25.2% | 4.7% | 0.94 | -9.3% | 275 | 1.60 | 13.1% | 62.2 | 9/9 | 0.89 | 0.81 | 0.13 | 4 | 6.2% | 0.76 | 0.71 | 24.3% | 23.4% | 23.2% | 24.5%/19.3% | 14.3 (interpolated) | pass | 0.395 (unverified) | n/a |
| 199 | `cfg_7644` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 22/95/0 | 117 | 19.4% | 3.7% | 0.76 | -7.2% | 521 | 1.48 | 13.6% | 63.9 | 7/7 | 1.00 | 0.55 | 0.21 | 4 | 6.4% | 0.68 | 0.88 | 18.2% | 17.5% | 12.3% | 16.1%/10.9% | 11.2 (interpolated) | pass | 0.252 (unverified) | n/a |
| 200 | `cfg_a5c4` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 15/70/37 | 122 | 23.2% | 4.3% | 0.89 | -7.8% | 246 | 1.56 | 14.9% | 67.0 | 10/10 | 1.00 | 0.75 | 0.14 | 3 | 10.9% | 0.51 | 0.71 | 22.7% | 21.4% | 15.4% | 21.3%/15.1% | 12.9 (interpolated) | pass | 0.342 (unverified) | n/a |
| 201 | `cfg_2a2b` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 26/34/45 | 105 | 18.0% | 3.4% | 0.79 | -5.1% | 246 | 1.50 | 10.3% | 57.2 | 12/12 | 1.00 | 0.68 | 0.12 | 4 | 10.4% | 0.40 | 0.75 | 17.0% | 15.3% | 22.0% | 16.9%/11.2% | 11.3 (interpolated) | pass | 0.269 (unverified) | n/a |
| 202 | `cfg_1935` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 37/56/87 | 180 | 28.4% | 5.2% | 0.85 | -7.0% | 236 | 1.38 | 22.7% | 99.0 | 9/9 | 1.00 | 0.65 | 0.20 | 4 | 13.0% | 0.52 | 0.56 | 25.8% | 24.6% | 18.7% | 23.3%/18.7% | 10.2 (interpolated) | pass | 0.331 (unverified) | n/a |
| 203 | `cfg_7b52` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 29/93/94 | 216 | 24.9% | 4.6% | 0.76 | -8.5% | 367 | 1.31 | 22.6% | 118.0 | 9/9 | 0.89 | 0.67 | 0.09 | 3 | 2.6% | 0.91 | 0.74 | 21.3% | 20.0% | 16.9% | 22.8%/16.7% | 7.6 (interpolated) | pass | 0.247 (unverified) | n/a |
| 204 | `cfg_eb11` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 65/49/108 | 222 | 27.7% | 5.1% | 0.80 | -8.3% | 160 | 1.31 | 25.8% | 122.2 | 8/8 | 1.00 | 0.65 | 0.15 | 4 | 11.5% | 0.56 | 0.56 | 26.1% | 23.9% | 14.7% | 24.3%/17.3% | 8.1 (interpolated) | pass | 0.281 (unverified) | n/a |
| 205 | `cfg_5c0f` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 30/99/66 | 195 | 25.6% | 4.7% | 0.78 | -6.6% | 567 | 1.33 | 22.4% | 106.6 | 9/9 | 1.00 | 0.66 | 0.12 | 4 | 5.6% | 0.80 | 0.73 | 24.2% | 21.6% | 15.0% | 23.3%/14.7% | 8.8 (interpolated) | pass | 0.266 (unverified) | n/a |
| 206 | `cfg_a524` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 26/83/78 | 187 | 24.2% | 4.5% | 0.76 | -6.9% | 272 | 1.34 | 19.8% | 102.2 | 11/11 | 1.00 | 0.66 | 0.10 | 4 | 7.1% | 0.69 | 0.74 | 22.0% | 20.4% | 17.4% | 19.6%/13.1% | 8.9 (interpolated) | pass | 0.258 (unverified) | n/a |
| 207 | `cfg_f79e` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=25, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 38/62/67 | 167 | 25.7% | 4.8% | 0.90 | -5.7% | 277 | 1.47 | 16.8% | 91.2 | 10/10 | 1.00 | 0.59 | 0.31 | 4 | 12.8% | 0.47 | 0.65 | 22.6% | 21.2% | 17.2% | 23.6%/16.7% | 10.1 (interpolated) | pass | 0.360 (unverified) | n/a |
| 208 | `cfg_666c` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=12, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 38/42/34 | 114 | 23.6% | 4.4% | 0.91 | -5.2% | 258 | 1.61 | 12.7% | 63.4 | 8/8 | 1.00 | 0.70 | 0.21 | 4 | 9.2% | 0.58 | 0.52 | 23.0% | 22.2% | 9.3% | 21.5%/17.5% | 13.4 (interpolated) | pass | 0.375 (unverified) | n/a |
| 209 | `cfg_bbba` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=22, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 39/96/0 | 135 | 24.4% | 4.5% | 0.81 | -7.0% | 328 | 1.46 | 18.0% | 74.7 | 8/8 | 1.00 | 0.75 | 0.06 | 3 | 8.6% | 0.67 | 0.74 | 23.0% | 21.7% | 20.6% | 22.9%/18.2% | 11.7 (interpolated) | pass | 0.297 (unverified) | n/a |
| 210 | `cfg_2059` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 51/44/87 | 182 | 27.3% | 5.0% | 0.83 | -6.8% | 236 | 1.36 | 22.0% | 100.1 | 10/10 | 1.00 | 0.59 | 0.24 | 5 | 12.7% | 0.52 | 0.55 | 25.7% | 24.4% | 19.3% | 23.7%/15.5% | 9.8 (interpolated) | pass | 0.313 (unverified) | n/a |
| 211 | `cfg_46f1` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 57/56/105 | 218 | 28.9% | 5.3% | 0.83 | -11.2% | 173 | 1.32 | 26.0% | 120.8 | 9/9 | 1.00 | 0.67 | 0.16 | 4 | 11.1% | 0.61 | 0.56 | 27.0% | 25.4% | 20.9% | 25.6%/17.8% | 8.9 (interpolated) | pass | 0.299 (unverified) | n/a |
| 212 | `cfg_fa00` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 18/55/38 | 111 | 17.2% | 3.3% | 0.84 | -4.3% | 225 | 1.54 | 10.3% | 60.9 | 11/11 | 1.00 | 0.70 | 0.14 | 4 | 9.7% | 0.41 | 0.71 | 15.6% | 14.6% | 10.9% | 14.4%/10.3% | 10.0 (interpolated) | pass | 0.308 (unverified) | n/a |
| 213 | `cfg_cdf9` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=2.0 | 63/49/79 | 191 | 26.9% | 5.0% | 0.76 | -7.7% | 255 | 1.31 | 24.3% | 105.1 | 8/8 | 1.00 | 0.63 | 0.14 | 4 | 16.2% | 0.38 | 0.60 | 24.0% | 23.3% | 22.0% | 23.2%/18.2% | 9.2 (interpolated) | pass | 0.255 (unverified) | n/a |
| 214 | `cfg_19a8` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 11/115/37 | 163 | 18.3% | 3.5% | 0.88 | -5.0% | 453 | 1.47 | 11.4% | 89.4 | 10/10 | 1.00 | 0.57 | 0.31 | 4 | 8.0% | 0.53 | 0.63 | 17.1% | 15.3% | 18.7% | 18.3%/12.1% | 8.1 (interpolated) | pass | 0.336 (unverified) | n/a |
| 215 | `cfg_8d94` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 40/140/0 | 180 | 23.6% | 4.4% | 0.82 | -9.8% | 554 | 1.43 | 20.6% | 99.2 | 8/8 | 1.00 | 0.67 | 0.14 | 4 | 12.6% | 0.47 | 0.59 | 22.0% | 20.4% | 28.4% | 21.5%/16.0% | 9.2 (interpolated) | pass | 0.298 (unverified) | n/a |
| 216 | `cfg_6408` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 19/114/0 | 133 | 26.7% | 4.9% | 0.86 | -12.7% | 437 | 1.53 | 15.6% | 73.6 | 11/11 | 1.00 | 0.71 | 0.15 | 4 | 6.2% | 0.81 | 0.74 | 26.0% | 24.6% | 24.0% | 23.8%/16.7% | 12.6 (interpolated) | pass | 0.334 (unverified) | n/a |
| 217 | `cfg_d861` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 32/75/153 | 260 | 26.2% | 4.8% | 0.78 | -8.1% | 212 | 1.29 | 21.8% | 142.2 | 10/10 | 1.00 | 0.66 | 0.12 | 4 | 7.6% | 0.70 | 0.73 | 23.5% | 20.5% | 11.2% | 22.2%/13.3% | 6.7 (interpolated) | pass | 0.262 (unverified) | n/a |
| 218 | `cfg_3f14` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 41/85/168 | 294 | 27.3% | 5.0% | 0.79 | -8.9% | 133 | 1.27 | 24.2% | 160.5 | 9/9 | 1.00 | 0.65 | 0.14 | 4 | 7.2% | 0.74 | 0.70 | 23.4% | 20.7% | 10.0% | 22.0%/13.6% | 5.9 (interpolated) | pass | 0.274 (unverified) | n/a |
| 219 | `cfg_9f79` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 50/105/0 | 155 | 24.0% | 4.5% | 0.86 | -8.3% | 275 | 1.47 | 17.2% | 85.7 | 9/9 | 1.00 | 0.67 | 0.19 | 3 | 9.3% | 0.62 | 0.60 | 22.5% | 20.5% | 25.2% | 22.9%/17.7% | 10.1 (interpolated) | pass | 0.323 (unverified) | n/a |
| 220 | `cfg_4599` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 44/45/80 | 169 | 21.9% | 4.1% | 0.75 | -7.7% | 333 | 1.34 | 20.6% | 92.0 | 11/11 | 1.00 | 0.64 | 0.11 | 4 | 12.8% | 0.38 | 0.65 | 19.9% | 18.7% | 15.5% | 19.2%/11.9% | 8.7 (interpolated) | pass | 0.246 (unverified) | n/a |
| 221 | `cfg_04b5` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=none | 77/70/0 | 147 | 28.6% | 5.2% | 0.80 | -7.2% | 275 | 1.47 | 23.0% | 81.5 | 8/8 | 0.88 | 0.75 | 0.05 | 4 | 11.2% | 0.62 | 0.51 | 27.5% | 26.7% | 28.3% | 27.8%/22.7% | 12.6 (interpolated) | pass | 0.288 (unverified) | n/a |
| 222 | `cfg_9fb6` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=25, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 15/58/45 | 118 | 19.6% | 3.7% | 0.85 | -4.9% | 234 | 1.53 | 10.8% | 65.1 | 10/10 | 1.00 | 0.55 | 0.30 | 5 | 11.0% | 0.42 | 0.88 | 19.0% | 16.0% | 11.5% | 17.3%/11.9% | 10.5 (interpolated) | pass | 0.314 (unverified) | n/a |
| 223 | `cfg_f966` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 11/81/28 | 120 | 20.6% | 3.9% | 0.85 | -6.4% | 566 | 1.50 | 12.2% | 65.9 | 10/10 | 1.00 | 0.62 | 0.23 | 3 | 6.0% | 0.71 | 0.74 | 19.4% | 17.9% | 15.0% | 19.0%/12.9% | 11.8 (interpolated) | pass | 0.311 (unverified) | n/a |
| 224 | `cfg_93ed` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=2.0 | 25/37/47 | 109 | 22.9% | 4.3% | 0.86 | -8.7% | 265 | 1.50 | 15.6% | 58.7 | 9/9 | 1.00 | 0.67 | 0.18 | 3 | 9.1% | 0.63 | 0.64 | 21.9% | 20.4% | 11.0% | 19.9%/14.8% | 13.3 (interpolated) | pass | 0.323 (unverified) | n/a |
| 225 | `cfg_07bd` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 17/109/38 | 164 | 17.6% | 3.4% | 0.86 | -4.8% | 453 | 1.45 | 11.3% | 90.1 | 11/11 | 1.00 | 0.59 | 0.27 | 4 | 7.7% | 0.53 | 0.64 | 16.1% | 14.5% | 18.2% | 16.5%/11.8% | 7.8 (interpolated) | pass | 0.320 (unverified) | n/a |
| 226 | `cfg_73f8` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 25/43/64 | 132 | 21.5% | 4.0% | 0.76 | -12.1% | 195 | 1.43 | 17.7% | 72.5 | 9/9 | 1.00 | 0.68 | 0.08 | 4 | 6.7% | 0.68 | 0.78 | 20.0% | 18.2% | 14.9% | 20.1%/12.7% | 11.1 (interpolated) | pass | 0.245 (unverified) | n/a |
| 227 | `cfg_f7e5` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 68/50/106 | 224 | 29.2% | 5.3% | 0.85 | -10.1% | 173 | 1.32 | 26.1% | 124.6 | 8/8 | 1.00 | 0.70 | 0.15 | 4 | 14.0% | 0.49 | 0.54 | 27.0% | 25.4% | 23.5% | 24.8%/19.6% | 8.7 (interpolated) | pass | 0.316 (unverified) | n/a |
| 228 | `cfg_f619` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 5/75/30 | 110 | 12.9% | 2.5% | 0.81 | -3.7% | 437 | 1.52 | 7.7% | 60.9 | 9/9 | 1.00 | 0.67 | 0.13 | 4 | 5.9% | 0.53 | 0.76 | 11.7% | 11.5% | 13.8% | 11.8%/8.8% | 8.5 (interpolated) | pass | 0.284 (unverified) | n/a |
| 229 | `cfg_7038` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.0 | 22/32/88 | 142 | 20.9% | 3.9% | 0.81 | -7.1% | 285 | 1.44 | 14.5% | 76.3 | 8/8 | 1.00 | 0.67 | 0.14 | 3 | 12.3% | 0.42 | 0.77 | 19.6% | 18.1% | 15.0% | 17.8%/11.3% | 9.8 (interpolated) | pass | 0.289 (unverified) | n/a |
| 230 | `cfg_22a2` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=25, entry_z=-2.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=none | 46/84/0 | 130 | 28.2% | 5.2% | 0.79 | -7.4% | 179 | 1.51 | 22.8% | 72.0 | 8/8 | 0.88 | 0.73 | 0.06 | 4 | 13.0% | 0.53 | 0.57 | 27.5% | 26.0% | 25.1% | 27.8%/22.7% | 13.8 (interpolated) | pass | 0.281 (unverified) | n/a |
| 231 | `cfg_b06f` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=18, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 39/48/39 | 126 | 21.7% | 4.1% | 0.86 | -7.3% | 289 | 1.53 | 13.9% | 68.8 | 10/10 | 1.00 | 0.68 | 0.18 | 3 | 11.7% | 0.43 | 0.66 | 20.5% | 19.1% | 14.2% | 19.2%/13.5% | 11.5 (interpolated) | pass | 0.323 (unverified) | n/a |
| 232 | `cfg_91e4` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 17/58/26 | 101 | 18.0% | 3.4% | 0.91 | -3.0% | 292 | 1.73 | 6.9% | 56.2 | 11/11 | 1.00 | 0.72 | 0.19 | 5 | 11.6% | 0.34 | 0.70 | 17.3% | 15.7% | 8.0% | 15.8%/11.9% | 12.2 (interpolated) | pass | 0.362 (unverified) | n/a |
| 233 | `cfg_22f5` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=12, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 34/36/30 | 100 | 19.9% | 3.8% | 0.82 | -5.7% | 258 | 1.62 | 10.7% | 54.8 | 9/9 | 1.00 | 0.48 | 0.34 | 3 | 6.8% | 0.63 | 0.63 | 18.7% | 18.0% | 15.4% | 18.5%/13.6% | 13.1 (interpolated) | pass | 0.299 (unverified) | n/a |
| 234 | `cfg_2105` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=25, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 10/76/56 | 142 | 18.0% | 3.4% | 0.77 | -5.9% | 347 | 1.41 | 13.1% | 79.3 | 10/10 | 1.00 | 0.52 | 0.25 | 3 | 4.8% | 0.72 | 0.84 | 16.8% | 14.8% | 10.1% | 16.2%/12.7% | 9.0 (interpolated) | pass | 0.258 (unverified) | n/a |
| 235 | `cfg_49f3` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 8/72/30 | 110 | 12.7% | 2.5% | 0.80 | -3.7% | 380 | 1.51 | 7.6% | 61.0 | 10/10 | 1.00 | 0.67 | 0.13 | 4 | 6.0% | 0.52 | 0.77 | 11.7% | 11.3% | 13.8% | 11.6%/8.2% | 8.4 (interpolated) | pass | 0.277 (unverified) | n/a |
| 236 | `cfg_fbe7` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.0 | 21/74/106 | 201 | 25.0% | 4.6% | 0.80 | -8.6% | 252 | 1.36 | 15.8% | 110.4 | 9/9 | 1.00 | 0.65 | 0.16 | 3 | 4.9% | 0.79 | 0.77 | 23.4% | 22.1% | 25.3% | 20.9%/14.0% | 8.6 (interpolated) | pass | 0.283 (unverified) | n/a |
| 237 | `cfg_4970` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=25, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 29/36/56 | 121 | 24.7% | 4.6% | 0.91 | -5.1% | 235 | 1.57 | 15.1% | 66.9 | 8/8 | 0.88 | 0.72 | 0.19 | 5 | 17.4% | 0.27 | 0.62 | 23.2% | 22.1% | 18.9% | 21.8%/15.5% | 12.5 (interpolated) | pass | 0.364 (unverified) | n/a |
| 238 | `cfg_6238` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 106/25/101 | 232 | 23.1% | 4.3% | 0.76 | -6.5% | 292 | 1.29 | 23.0% | 127.4 | 8/8 | 1.00 | 0.58 | 0.17 | 5 | 14.4% | 0.35 | 0.69 | 21.1% | 18.9% | 23.2% | 20.6%/14.2% | 6.9 (interpolated) | pass | 0.249 (unverified) | n/a |
| 239 | `cfg_17a7` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=12, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 31/52/41 | 124 | 23.8% | 4.4% | 0.80 | -4.5% | 188 | 1.45 | 17.9% | 67.3 | 8/8 | 1.00 | 0.57 | 0.24 | 5 | 6.3% | 0.73 | 0.67 | 22.8% | 21.7% | 9.1% | 23.6%/20.0% | 12.8 (interpolated) | pass | 0.286 (unverified) | n/a |
| 240 | `cfg_20e6` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=22, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 9/75/63 | 147 | 21.0% | 4.0% | 0.82 | -8.7% | 278 | 1.43 | 16.5% | 78.8 | 9/9 | 1.00 | 0.50 | 0.32 | 3 | 9.1% | 0.56 | 0.84 | 18.9% | 17.8% | 17.3% | 17.7%/12.1% | 9.6 (interpolated) | pass | 0.293 (unverified) | n/a |
| 241 | `cfg_5770` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 9/64/28 | 101 | 14.8% | 2.8% | 0.75 | -3.6% | 318 | 1.53 | 10.0% | 55.5 | 10/10 | 0.90 | 0.59 | 0.16 | 5 | 9.9% | 0.31 | 0.89 | 13.8% | 13.1% | 2.8% | 13.7%/10.3% | 10.4 (interpolated) | pass | 0.239 (unverified) | n/a |
| 242 | `cfg_1e82` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=25, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 41/24/56 | 121 | 22.1% | 4.1% | 0.84 | -5.2% | 324 | 1.51 | 14.0% | 66.9 | 9/9 | 0.89 | 0.72 | 0.12 | 5 | 15.7% | 0.29 | 0.67 | 21.3% | 20.1% | 16.1% | 21.1%/16.9% | 11.6 (interpolated) | pass | 0.311 (unverified) | n/a |
| 243 | `cfg_46e0` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 15/77/32 | 124 | 19.5% | 3.7% | 0.78 | -8.9% | 575 | 1.44 | 12.3% | 67.7 | 10/10 | 1.00 | 0.57 | 0.21 | 3 | 4.5% | 0.79 | 0.76 | 17.7% | 17.0% | 12.6% | 17.9%/12.8% | 10.9 (interpolated) | pass | 0.255 (unverified) | n/a |
| 244 | `cfg_cb58` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 21/132/0 | 153 | 23.8% | 4.4% | 0.85 | -8.6% | 275 | 1.47 | 18.0% | 84.3 | 9/9 | 1.00 | 0.59 | 0.25 | 3 | 9.8% | 0.60 | 0.62 | 22.2% | 21.0% | 26.0% | 21.0%/15.0% | 9.9 (interpolated) | pass | 0.315 (unverified) | n/a |
| 245 | `cfg_6847` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=18, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 18/79/25 | 122 | 18.0% | 3.4% | 0.95 | -3.1% | 150 | 1.63 | 8.6% | 67.0 | 10/10 | 1.00 | 0.60 | 0.35 | 5 | 12.6% | 0.27 | 0.61 | 15.7% | 14.4% | 0.3% | 15.2%/11.2% | 10.1 (interpolated) | pass | 0.403 (unverified) | n/a |
| 246 | `cfg_7e52` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 13/84/25 | 122 | 18.4% | 3.5% | 0.96 | -3.1% | 150 | 1.65 | 8.7% | 67.1 | 9/9 | 1.00 | 0.54 | 0.42 | 5 | 13.5% | 0.27 | 0.61 | 16.1% | 15.1% | 0.4% | 15.4%/11.2% | 10.3 (interpolated) | pass | 0.411 (unverified) | n/a |
| 247 | `cfg_1a81` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=18, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 10/64/27 | 101 | 17.8% | 3.4% | 0.88 | -2.8% | 321 | 1.71 | 7.0% | 56.3 | 10/10 | 1.00 | 0.63 | 0.25 | 5 | 10.6% | 0.38 | 0.74 | 16.1% | 15.2% | 8.0% | 14.9%/10.8% | 12.0 (interpolated) | pass | 0.332 (unverified) | n/a |
| 248 | `cfg_a1c5` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=12, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 55/28/32 | 115 | 18.8% | 3.6% | 0.79 | -5.2% | 292 | 1.53 | 11.2% | 63.9 | 8/8 | 1.00 | 0.64 | 0.15 | 3 | 7.6% | 0.57 | 0.61 | 17.8% | 16.6% | 5.8% | 17.8%/13.0% | 10.8 (interpolated) | pass | 0.282 (unverified) | n/a |
| 249 | `cfg_94b5` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 5/80/39 | 124 | 14.0% | 2.7% | 0.77 | -5.1% | 308 | 1.42 | 8.6% | 67.7 | 9/9 | 1.00 | 0.73 | 0.05 | 3 | 6.1% | 0.55 | 0.77 | 12.9% | 12.0% | 13.2% | 12.4%/8.4% | 8.3 (interpolated) | pass | 0.255 (unverified) | n/a |
| 250 | `cfg_6995` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 10/76/38 | 124 | 15.2% | 2.9% | 0.84 | -4.7% | 308 | 1.46 | 8.6% | 67.8 | 10/10 | 1.00 | 0.77 | 0.07 | 3 | 6.9% | 0.53 | 0.72 | 13.4% | 12.4% | 12.9% | 12.8%/8.2% | 8.4 (interpolated) | pass | 0.301 (unverified) | n/a |
| 251 | `cfg_4aaa` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=18, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=2.0 | 44/31/45 | 120 | 19.8% | 3.7% | 0.82 | -7.8% | 304 | 1.44 | 15.3% | 65.4 | 9/9 | 1.00 | 0.65 | 0.18 | 3 | 7.4% | 0.63 | 0.62 | 18.7% | 17.9% | 14.9% | 17.3%/12.7% | 11.2 (interpolated) | pass | 0.298 (unverified) | n/a |
| 252 | `cfg_6ec0` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=1.5 | 56/40/90 | 186 | 30.3% | 5.5% | 0.87 | -7.5% | 128 | 1.39 | 21.2% | 103.0 | 9/9 | 0.89 | 0.70 | 0.17 | 5 | 18.8% | 0.35 | 0.52 | 28.3% | 25.7% | 27.0% | 25.0%/17.8% | 10.3 (interpolated) | pass | 0.331 (unverified) | n/a |
| 253 | `cfg_f777` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=none | 70/74/0 | 144 | 29.5% | 5.4% | 0.83 | -8.6% | 275 | 1.45 | 23.2% | 79.1 | 9/9 | 1.00 | 0.69 | 0.15 | 4 | 15.8% | 0.46 | 0.53 | 27.6% | 26.0% | 31.0% | 23.5%/18.8% | 12.8 (interpolated) | pass | 0.322 (unverified) | n/a |
| 254 | `cfg_c292` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=22, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 62/92/0 | 154 | 24.4% | 4.5% | 0.75 | -11.4% | 275 | 1.39 | 19.8% | 84.8 | 9/9 | 0.89 | 0.75 | 0.01 | 4 | 8.6% | 0.67 | 0.58 | 22.6% | 21.3% | 24.7% | 22.6%/17.9% | 10.5 (interpolated) | pass | 0.257 (unverified) | n/a |
| 255 | `cfg_bb7f` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 14/86/0 | 100 | 21.1% | 4.0% | 0.89 | -6.6% | 575 | 1.71 | 11.5% | 54.9 | 9/9 | 1.00 | 0.67 | 0.22 | 3 | 6.1% | 0.70 | 0.70 | 20.4% | 19.6% | 21.8% | 20.1%/15.4% | 14.8 (interpolated) | pass | 0.344 (unverified) | n/a |
| 256 | `cfg_98a0` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=22, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=none | 53/75/0 | 128 | 25.3% | 4.7% | 0.76 | -7.6% | 346 | 1.47 | 21.6% | 70.1 | 7/7 | 0.86 | 0.59 | 0.17 | 4 | 13.9% | 0.38 | 0.63 | 24.9% | 24.2% | 22.9% | 23.3%/18.3% | 13.1 (interpolated) | pass | 0.253 (unverified) | n/a |
| 257 | `cfg_ac56` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 13/93/42 | 148 | 15.3% | 2.9% | 0.76 | -7.6% | 466 | 1.40 | 10.1% | 80.6 | 10/10 | 0.90 | 0.71 | 0.05 | 3 | 2.2% | 0.84 | 0.79 | 14.2% | 13.0% | 18.5% | 15.0%/9.8% | 7.7 (interpolated) | pass | 0.248 (unverified) | n/a |
| 258 | `cfg_b054` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 17/43/62 | 122 | 15.6% | 3.0% | 0.75 | -7.9% | 317 | 1.41 | 11.5% | 66.4 | 10/10 | 1.00 | 0.52 | 0.23 | 4 | 8.1% | 0.48 | 0.88 | 14.7% | 13.6% | 3.2% | 14.9%/10.0% | 9.2 (interpolated) | pass | 0.247 (unverified) | n/a |
| 259 | `cfg_88a1` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=12, entry_z=-2.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 21/64/41 | 126 | 23.9% | 4.5% | 0.84 | -4.4% | 222 | 1.49 | 14.8% | 69.1 | 9/9 | 1.00 | 0.46 | 0.38 | 4 | 9.9% | 0.56 | 0.64 | 22.4% | 21.7% | 11.2% | 23.8%/18.6% | 12.8 (interpolated) | pass | 0.315 (unverified) | n/a |
| 260 | `cfg_aefd` | timeframe=1h, mean_type=ema, mean_lookback=60, std_lookback=18, entry_z=-3.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=2.0 | 36/35/47 | 118 | 19.9% | 3.8% | 0.80 | -8.4% | 195 | 1.42 | 16.1% | 64.1 | 10/10 | 1.00 | 0.69 | 0.11 | 3 | 8.1% | 0.60 | 0.65 | 18.6% | 17.6% | 14.5% | 17.7%/13.7% | 11.3 (interpolated) | pass | 0.281 (unverified) | n/a |
| 261 | `cfg_1f6a` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=18, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=none | 42/58/0 | 100 | 24.1% | 4.5% | 0.81 | -9.1% | 487 | 1.57 | 16.7% | 54.4 | 8/8 | 0.88 | 0.73 | 0.08 | 4 | 9.3% | 0.63 | 0.54 | 23.2% | 22.0% | 18.4% | 21.6%/14.8% | 14.8 (interpolated) | pass | 0.300 (unverified) | n/a |
| 262 | `cfg_42e2` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=12, entry_z=-2.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 27/73/0 | 100 | 25.0% | 4.6% | 1.02 | -5.4% | 283 | 1.90 | 11.0% | 55.5 | 7/7 | 1.00 | 0.80 | 0.22 | 4 | 11.8% | 0.49 | 0.52 | 23.4% | 22.6% | 21.9% | 22.6%/17.7% | 15.7 (interpolated) | pass | 0.471 (unverified) | n/a |
| 263 | `cfg_5d40` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=18, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 24/73/45 | 142 | 22.7% | 4.2% | 0.83 | -5.8% | 380 | 1.47 | 16.5% | 77.8 | 10/10 | 1.00 | 0.49 | 0.34 | 4 | 11.4% | 0.47 | 0.69 | 21.5% | 20.4% | 11.4% | 19.8%/14.2% | 11.4 (interpolated) | pass | 0.302 (unverified) | n/a |
| 264 | `cfg_2841` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=none | 51/92/0 | 143 | 28.9% | 5.3% | 0.80 | -8.8% | 275 | 1.43 | 24.5% | 78.3 | 8/8 | 1.00 | 0.64 | 0.15 | 4 | 16.3% | 0.43 | 0.57 | 27.4% | 25.8% | 30.1% | 25.0%/18.3% | 12.8 (interpolated) | pass | 0.293 (unverified) | n/a |
| 265 | `cfg_49a5` | timeframe=1h, mean_type=sma, mean_lookback=50, std_lookback=25, entry_z=-2.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 38/107/0 | 145 | 20.9% | 3.9% | 0.78 | -7.5% | 567 | 1.44 | 16.1% | 78.8 | 8/8 | 0.88 | 0.57 | 0.22 | 4 | 10.4% | 0.51 | 0.70 | 20.1% | 18.9% | 13.3% | 18.3%/11.7% | 9.7 (interpolated) | pass | 0.271 (unverified) | n/a |
| 266 | `cfg_009d` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=25, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 6/87/36 | 129 | 15.7% | 3.0% | 0.80 | -5.2% | 482 | 1.47 | 8.8% | 71.4 | 9/9 | 0.89 | 0.55 | 0.25 | 3 | 7.4% | 0.51 | 0.79 | 14.4% | 13.5% | 8.3% | 14.2%/10.8% | 8.5 (interpolated) | pass | 0.281 (unverified) | n/a |
| 267 | `cfg_ef39` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 32/71/0 | 103 | 17.0% | 3.2% | 0.78 | -8.1% | 271 | 1.53 | 11.1% | 56.0 | 9/9 | 1.00 | 0.65 | 0.13 | 4 | 0.2% | 1.02 | 0.85 | 14.8% | 14.0% | 8.6% | 15.1%/10.4% | 11.3 (interpolated) | pass | 0.270 (unverified) | n/a |
| 268 | `cfg_785a` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=25, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 7/86/36 | 129 | 15.8% | 3.0% | 0.80 | -5.2% | 482 | 1.48 | 8.8% | 71.4 | 10/10 | 0.90 | 0.55 | 0.25 | 3 | 7.4% | 0.51 | 0.79 | 14.4% | 13.6% | 8.3% | 13.6%/10.3% | 8.6 (interpolated) | pass | 0.283 (unverified) | n/a |
| 269 | `cfg_5015` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 25/93/0 | 118 | 36.8% | 6.6% | 1.17 | -6.4% | 196 | 1.79 | 16.2% | 65.0 | 10/10 | 1.00 | 0.59 | 0.58 | 4 | 19.0% | 0.47 | 0.53 | 35.8% | 34.4% | 22.0% | 31.5%/25.3% | 18.7 (interpolated) | pass | 0.593 (unverified) | n/a |
| 270 | `cfg_ce73` | timeframe=1h, mean_type=ema, mean_lookback=40, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=none | 53/87/0 | 140 | 33.4% | 6.0% | 0.91 | -5.9% | 173 | 1.54 | 24.4% | 77.2 | 8/8 | 1.00 | 0.47 | 0.43 | 5 | 17.6% | 0.44 | 0.47 | 31.8% | 31.5% | 30.2% | 27.3%/19.1% | 14.5 (interpolated) | pass | 0.370 (unverified) | n/a |
| 271 | `cfg_7816` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 36/72/72 | 180 | 20.9% | 3.9% | 0.76 | -5.5% | 396 | 1.34 | 18.3% | 97.4 | 11/11 | 1.00 | 0.49 | 0.27 | 4 | 12.5% | 0.36 | 0.74 | 19.5% | 18.0% | 7.5% | 16.9%/9.3% | 8.1 (interpolated) | pass | 0.253 (unverified) | n/a |
| 272 | `cfg_095a` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=12, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 36/64/26 | 126 | 14.3% | 2.7% | 0.87 | -3.1% | 162 | 1.61 | 8.2% | 69.1 | 7/7 | 0.86 | 0.50 | 0.36 | 4 | 8.1% | 0.40 | 0.64 | 13.3% | 12.3% | 0.6% | 13.1%/10.0% | 8.1 (interpolated) | pass | 0.326 (unverified) | n/a |
| 273 | `cfg_8547` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=25, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 1/98/27 | 126 | 13.5% | 2.6% | 0.82 | -3.9% | 345 | 1.47 | 9.1% | 70.1 | 7/7 | 0.86 | 0.62 | 0.20 | 3 | 7.1% | 0.46 | 0.81 | 12.8% | 11.8% | 8.8% | 12.6%/7.9% | 8.2 (interpolated) | pass | 0.303 (unverified) | n/a |
| 274 | `cfg_1767` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 13/107/0 | 120 | 16.7% | 3.2% | 0.86 | -7.2% | 275 | 1.55 | 9.5% | 65.7 | 9/9 | 0.89 | 0.71 | 0.15 | 4 | 6.9% | 0.58 | 0.72 | 15.4% | 14.3% | 15.7% | 15.3%/11.1% | 9.3 (interpolated) | pass | 0.333 (unverified) | n/a |
| 275 | `cfg_f9c4` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 52/69/0 | 121 | 30.7% | 5.6% | 1.05 | -6.4% | 196 | 1.65 | 15.2% | 67.0 | 10/10 | 1.00 | 0.51 | 0.53 | 5 | 16.4% | 0.46 | 0.52 | 29.7% | 28.6% | 15.8% | 26.6%/22.0% | 16.1 (interpolated) | pass | 0.490 (unverified) | n/a |
| 276 | `cfg_22c3` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 7/113/0 | 120 | 15.4% | 3.0% | 0.81 | -7.3% | 275 | 1.51 | 9.5% | 65.8 | 8/8 | 0.88 | 0.69 | 0.12 | 4 | 5.6% | 0.63 | 0.76 | 14.3% | 13.4% | 14.1% | 14.6%/9.8% | 8.9 (interpolated) | pass | 0.291 (unverified) | n/a |
| 277 | `cfg_6a25` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=12, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 18/78/28 | 124 | 13.7% | 2.6% | 0.82 | -3.4% | 339 | 1.57 | 8.5% | 68.3 | 7/7 | 0.86 | 0.48 | 0.35 | 4 | 7.9% | 0.39 | 0.66 | 12.8% | 11.6% | 2.3% | 11.8%/7.6% | 7.9 (interpolated) | pass | 0.291 (unverified) | n/a |
| 278 | `cfg_4e71` | timeframe=1h, mean_type=ema, mean_lookback=50, std_lookback=20, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 24/66/30 | 120 | 18.8% | 3.6% | 0.79 | -7.9% | 539 | 1.48 | 11.7% | 65.6 | 11/11 | 1.00 | 0.57 | 0.22 | 3 | -0.3% | 1.06 | 0.84 | 17.8% | 16.1% | 0.7% | 17.2%/10.2% | 10.5 (interpolated) | pass | 0.263 (unverified) | n/a |
| 279 | `cfg_184d` | timeframe=1h, mean_type=ema, mean_lookback=30, std_lookback=22, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=none | 56/82/0 | 138 | 21.9% | 4.1% | 0.78 | -7.5% | 211 | 1.44 | 17.3% | 75.4 | 9/9 | 1.00 | 0.67 | 0.11 | 4 | 9.1% | 0.59 | 0.74 | 21.1% | 20.0% | 14.4% | 19.3%/15.0% | 10.1 (interpolated) | pass | 0.273 (unverified) | n/a |
| 280 | `cfg_a6ea` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-2.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=none, stop_atr_multiple=none | 68/61/0 | 129 | 26.8% | 4.9% | 0.78 | -6.8% | 251 | 1.50 | 20.3% | 70.4 | 9/9 | 1.00 | 0.60 | 0.18 | 4 | 12.8% | 0.51 | 0.51 | 26.8% | 25.2% | 30.7% | 24.6%/19.0% | 13.4 (interpolated) | pass | 0.275 (unverified) | n/a |
| 281 | `cfg_d0e8` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=25, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 6/79/34 | 119 | 15.1% | 2.9% | 0.89 | -5.4% | 483 | 1.52 | 8.2% | 65.8 | 8/8 | 0.88 | 0.54 | 0.35 | 4 | 8.7% | 0.41 | 0.75 | 14.0% | 13.3% | 16.0% | 14.1%/10.2% | 8.8 (interpolated) | pass | 0.358 (unverified) | n/a |
| 282 | `cfg_5381` | timeframe=1h, mean_type=sma, mean_lookback=30, std_lookback=25, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 9/76/34 | 119 | 15.3% | 2.9% | 0.90 | -5.4% | 483 | 1.53 | 8.1% | 65.9 | 9/9 | 0.78 | 0.56 | 0.34 | 4 | 8.8% | 0.41 | 0.74 | 14.0% | 13.3% | 17.0% | 13.7%/10.4% | 8.8 (interpolated) | pass | 0.365 (unverified) | n/a |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 5.3% / 1.57 / 23 | 2.7% / 0.83 / 15 | 21.2% / 2.34 / 21 | 2.3% / 0.50 / 24 | 1.6% / 0.36 / 23 |
| 2 | 5.2% / 1.24 / 36 | 4.3% / 1.10 / 26 | 19.4% / 2.20 / 24 | 12.7% / 2.24 / 30 | -3.1% / -0.46 / 38 |
| 3 | 0.2% / 0.08 / 29 | 4.8% / 1.38 / 23 | 16.5% / 2.43 / 20 | 7.2% / 1.23 / 35 | 2.8% / 0.46 / 44 |
| 4 | 2.9% / 0.82 / 28 | 10.2% / 2.58 / 24 | 15.0% / 2.07 / 20 | -2.1% / -0.38 / 26 | 1.9% / 0.38 / 22 |
| 5 | 1.6% / 0.48 / 39 | 8.5% / 2.95 / 21 | 17.3% / 2.09 / 22 | 3.3% / 0.76 / 30 | 1.0% / 0.18 / 37 |
| 6 | 2.4% / 0.75 / 42 | 5.7% / 2.01 / 22 | 16.1% / 2.02 / 22 | 3.6% / 0.86 / 32 | 0.2% / 0.07 / 39 |
| 7 | 4.5% / 1.35 / 23 | 2.9% / 0.85 / 15 | 20.2% / 2.28 / 21 | 2.5% / 0.57 / 24 | 1.7% / 0.39 / 23 |
| 8 | 2.5% / 0.73 / 28 | 10.1% / 2.57 / 24 | 15.0% / 2.06 / 20 | -2.2% / -0.40 / 26 | 1.4% / 0.28 / 22 |
| 9 | 1.7% / 0.41 / 44 | 7.1% / 1.69 / 28 | 13.6% / 1.55 / 29 | 10.5% / 2.12 / 32 | -1.1% / -0.12 / 51 |
| 10 | 2.9% / 0.95 / 25 | 2.7% / 1.33 / 17 | 14.4% / 2.38 / 18 | 3.3% / 0.81 / 22 | -1.8% / -0.35 / 25 |
| 11 | 1.0% / 0.36 / 32 | 4.4% / 1.45 / 19 | 19.2% / 2.44 / 15 | 1.6% / 0.44 / 29 | -1.3% / -0.21 / 35 |
| 12 | 5.8% / 1.33 / 35 | 2.9% / 0.75 / 25 | 16.8% / 1.92 / 24 | 8.1% / 1.56 / 24 | -4.3% / -0.65 / 37 |
| 13 | 5.8% / 1.54 / 26 | 0.4% / 0.13 / 17 | 22.7% / 2.54 / 18 | 4.0% / 0.66 / 17 | 0.6% / 0.13 / 25 |
| 14 | 3.5% / 1.10 / 31 | 2.6% / 0.74 / 22 | 16.2% / 2.40 / 22 | 5.2% / 0.92 / 34 | 5.1% / 0.78 / 47 |
| 15 | 0.9% / 0.29 / 31 | 5.5% / 1.55 / 23 | 14.1% / 2.26 / 20 | 8.6% / 1.48 / 35 | 2.0% / 0.35 / 44 |
| 16 | 0.6% / 0.19 / 31 | 7.4% / 2.00 / 24 | 23.4% / 2.66 / 22 | 4.8% / 0.98 / 30 | -5.7% / -1.05 / 32 |
| 17 | 2.6% / 0.85 / 26 | 6.8% / 2.31 / 17 | 13.6% / 1.88 / 20 | 3.4% / 0.55 / 29 | 1.4% / 0.24 / 34 |
| 18 | -0.6% / -0.15 / 37 | 12.2% / 3.50 / 21 | 18.6% / 2.16 / 22 | 1.2% / 0.27 / 30 | 1.7% / 0.30 / 34 |
| 19 | 2.9% / 0.84 / 40 | 4.7% / 1.38 / 22 | 21.2% / 2.58 / 21 | -0.9% / -0.11 / 31 | 2.5% / 0.42 / 42 |
| 20 | -0.3% / -0.07 / 36 | 5.0% / 1.39 / 26 | 24.5% / 2.76 / 23 | 7.1% / 1.47 / 32 | -4.3% / -0.78 / 34 |
| 21 | 5.1% / 1.13 / 47 | 6.1% / 1.32 / 34 | 11.6% / 1.26 / 33 | 6.7% / 1.17 / 37 | 4.4% / 0.69 / 45 |
| 22 | 3.0% / 1.00 / 24 | 7.2% / 2.41 / 17 | 9.3% / 1.49 / 19 | 6.7% / 1.14 / 29 | 2.6% / 0.46 / 32 |
| 23 | 2.1% / 0.56 / 36 | 4.1% / 1.16 / 22 | 15.8% / 2.03 / 22 | 9.4% / 1.85 / 27 | -2.1% / -0.29 / 46 |
| 24 | -0.7% / -0.21 / 32 | 7.4% / 2.09 / 19 | 21.8% / 2.66 / 15 | 0.4% / 0.11 / 31 | 0.3% / 0.08 / 39 |
| 25 | -0.5% / -0.13 / 41 | 7.5% / 2.30 / 25 | 15.1% / 1.97 / 25 | -0.5% / -0.11 / 31 | 3.9% / 0.69 / 37 |
| 26 | 2.6% / 0.69 / 36 | 4.3% / 1.20 / 22 | 15.1% / 1.96 / 22 | 9.0% / 1.78 / 27 | -4.1% / -0.60 / 46 |
| 27 | 2.3% / 0.58 / 39 | 8.0% / 2.10 / 20 | 23.6% / 2.55 / 20 | -1.5% / -0.17 / 34 | -2.1% / -0.34 / 39 |
| 28 | 0.8% / 0.24 / 39 | 8.0% / 2.40 / 24 | 17.3% / 2.17 / 25 | -3.1% / -0.66 / 31 | 2.0% / 0.36 / 36 |
| 29 | -1.5% / -0.53 / 30 | 8.2% / 2.44 / 22 | 17.9% / 2.47 / 19 | 4.5% / 1.02 / 28 | -3.1% / -0.59 / 26 |
| 30 | 2.7% / 0.93 / 24 | 8.1% / 2.31 / 19 | 8.8% / 1.66 / 19 | 4.6% / 0.85 / 29 | -0.4% / -0.05 / 32 |
| 31 | 1.4% / 0.50 / 26 | 2.9% / 1.48 / 17 | 12.1% / 2.04 / 20 | 4.1% / 1.03 / 22 | -0.9% / -0.15 / 27 |
| 32 | 5.2% / 1.45 / 26 | -0.7% / -0.26 / 16 | 20.5% / 2.59 / 18 | 0.9% / 0.18 / 20 | 5.5% / 1.05 / 25 |
| 33 | 0.7% / 0.22 / 35 | 6.7% / 1.83 / 22 | 13.6% / 1.89 / 20 | 7.8% / 1.74 / 24 | -1.6% / -0.24 / 44 |
| 34 | 3.0% / 0.97 / 27 | 7.6% / 2.19 / 19 | 12.9% / 2.13 / 20 | 1.5% / 0.28 / 29 | -1.5% / -0.24 / 34 |
| 35 | -0.6% / -0.16 / 46 | 4.1% / 1.29 / 27 | 17.4% / 2.20 / 26 | 2.0% / 0.51 / 34 | 3.7% / 0.66 / 38 |
| 36 | -1.6% / -0.47 / 35 | 6.4% / 2.09 / 19 | 12.2% / 1.99 / 15 | 1.0% / 0.23 / 32 | 4.3% / 0.69 / 41 |
| 37 | -0.3% / -0.07 / 42 | 8.5% / 2.53 / 22 | 18.8% / 2.24 / 22 | 3.8% / 0.69 / 35 | 0.8% / 0.16 / 39 |
| 38 | 2.6% / 0.77 / 30 | 7.9% / 2.31 / 23 | 15.4% / 2.01 / 23 | 0.4% / 0.12 / 27 | 0.6% / 0.14 / 25 |
| 39 | -1.0% / -0.24 / 45 | 10.5% / 2.64 / 27 | 21.8% / 2.34 / 24 | 0.9% / 0.19 / 37 | -0.8% / -0.08 / 47 |
| 40 | 2.2% / 0.61 / 27 | 12.0% / 2.90 / 24 | 14.3% / 1.65 / 20 | -5.4% / -0.93 / 24 | 0.7% / 0.15 / 21 |
| 41 | -1.4% / -0.34 / 35 | 6.1% / 1.73 / 22 | 13.4% / 1.71 / 20 | 7.8% / 1.62 / 24 | -0.7% / -0.09 / 44 |
| 42 | 5.3% / 1.49 / 32 | 5.4% / 1.98 / 16 | 10.9% / 1.63 / 17 | -0.8% / -0.16 / 25 | 5.7% / 1.32 / 23 |
| 43 | 3.7% / 0.92 / 40 | 3.7% / 0.96 / 27 | 15.9% / 1.99 / 27 | 5.7% / 1.23 / 36 | 2.5% / 0.41 / 49 |
| 44 | 2.9% / 0.76 / 27 | 10.0% / 3.04 / 19 | 12.5% / 1.76 / 17 | -2.8% / -0.54 / 23 | 2.6% / 0.52 / 26 |
| 45 | -0.8% / -0.22 / 42 | 9.0% / 2.24 / 31 | 16.5% / 2.15 / 27 | 1.8% / 0.34 / 40 | 0.2% / 0.06 / 37 |
| 46 | 5.4% / 1.52 / 33 | 3.6% / 1.22 / 18 | 12.2% / 1.89 / 17 | -0.3% / -0.05 / 29 | 5.9% / 1.38 / 24 |
| 47 | -1.3% / -0.39 / 43 | 4.5% / 1.41 / 26 | 17.6% / 2.18 / 25 | 0.0% / 0.03 / 36 | 3.0% / 0.53 / 37 |
| 48 | 3.2% / 0.99 / 24 | 6.7% / 2.05 / 17 | 8.7% / 1.30 / 19 | 7.6% / 1.31 / 27 | -0.2% / -0.00 / 30 |
| 49 | 0.2% / 0.09 / 27 | 6.2% / 1.83 / 24 | 11.9% / 1.78 / 25 | 1.8% / 0.42 / 27 | 1.3% / 0.26 / 27 |
| 50 | 2.0% / 0.47 / 44 | 7.2% / 1.73 / 28 | 15.0% / 1.71 / 29 | 10.2% / 2.05 / 32 | -2.7% / -0.37 / 51 |
| 51 | 1.9% / 0.59 / 30 | 8.4% / 2.40 / 23 | 14.6% / 1.97 / 23 | 1.1% / 0.27 / 28 | 1.2% / 0.26 / 25 |
| 52 | -1.1% / -0.26 / 33 | 7.3% / 2.09 / 19 | 15.1% / 2.10 / 20 | 3.7% / 0.53 / 32 | 1.8% / 0.32 / 39 |
| 53 | -0.5% / -0.14 / 35 | 8.4% / 2.10 / 23 | 23.7% / 2.53 / 23 | 3.2% / 0.63 / 31 | -4.0% / -0.61 / 36 |
| 54 | 6.2% / 1.43 / 39 | 5.5% / 1.62 / 25 | 16.9% / 2.25 / 23 | -1.3% / -0.22 / 33 | 2.3% / 0.44 / 31 |
| 55 | -1.4% / -0.48 / 30 | 8.0% / 2.41 / 22 | 16.3% / 2.31 / 19 | 3.8% / 0.92 / 28 | -2.9% / -0.55 / 26 |
| 56 | 4.5% / 0.99 / 50 | 8.0% / 1.62 / 34 | 24.3% / 2.54 / 34 | -0.5% / -0.04 / 44 | -0.5% / -0.04 / 48 |
| 57 | 3.2% / 1.02 / 39 | 4.0% / 1.52 / 23 | 9.0% / 1.51 / 22 | 2.9% / 0.92 / 30 | 1.8% / 0.38 / 42 |
| 58 | -1.2% / -0.22 / 56 | 8.6% / 1.74 / 36 | 20.3% / 2.04 / 36 | 2.7% / 0.41 / 51 | 2.9% / 0.47 / 48 |
| 59 | 2.8% / 0.92 / 39 | 4.0% / 1.52 / 23 | 9.0% / 1.51 / 22 | 3.2% / 0.97 / 30 | 1.8% / 0.38 / 42 |
| 60 | 2.8% / 0.76 / 27 | 10.0% / 3.08 / 19 | 12.9% / 1.79 / 17 | -3.1% / -0.61 / 23 | 2.9% / 0.57 / 26 |
| 61 | 4.5% / 1.04 / 50 | 4.0% / 0.94 / 33 | 21.4% / 2.26 / 36 | -1.4% / -0.18 / 43 | -0.2% / -0.01 / 50 |
| 62 | 0.8% / 0.23 / 41 | 5.6% / 1.49 / 32 | 20.3% / 2.33 / 30 | 2.6% / 0.46 / 40 | -3.2% / -0.50 / 39 |
| 63 | 1.8% / 0.52 / 39 | 5.2% / 1.65 / 25 | 22.8% / 2.59 / 26 | 1.9% / 0.30 / 42 | 2.0% / 0.35 / 41 |
| 64 | 2.6% / 0.58 / 53 | 7.1% / 1.48 / 35 | 17.4% / 1.69 / 41 | 4.3% / 0.73 / 44 | 1.3% / 0.22 / 53 |
| 65 | 3.3% / 1.05 / 31 | 2.9% / 0.85 / 22 | 16.0% / 2.39 / 22 | 5.6% / 0.99 / 34 | 1.5% / 0.27 / 47 |
| 66 | 1.4% / 0.48 / 27 | 5.5% / 1.92 / 14 | 7.5% / 1.11 / 16 | 6.7% / 1.39 / 20 | 0.2% / 0.06 / 23 |
| 67 | 2.3% / 0.87 / 21 | 4.3% / 1.37 / 17 | 16.4% / 2.55 / 19 | -1.5% / -0.33 / 21 | 1.4% / 0.32 / 22 |
| 68 | 2.1% / 0.74 / 28 | 3.8% / 1.55 / 19 | 18.7% / 2.59 / 21 | 2.2% / 0.56 / 21 | -0.4% / -0.06 / 24 |
| 69 | 0.3% / 0.13 / 27 | 6.7% / 2.20 / 14 | 7.3% / 1.04 / 16 | 5.5% / 1.12 / 20 | 1.0% / 0.20 / 23 |
| 70 | 4.8% / 0.97 / 35 | 9.9% / 2.09 / 23 | 13.6% / 1.34 / 24 | 1.8% / 0.29 / 29 | -0.7% / -0.08 / 32 |
| 71 | 1.9% / 0.47 / 47 | 8.6% / 2.29 / 29 | 14.7% / 1.92 / 26 | -2.0% / -0.34 / 40 | 2.3% / 0.43 / 38 |
| 72 | 0.2% / 0.08 / 47 | 6.0% / 1.58 / 28 | 18.0% / 2.13 / 30 | 5.4% / 0.99 / 39 | -0.4% / -0.03 / 51 |
| 73 | 0.6% / 0.17 / 51 | 1.8% / 0.53 / 27 | 18.5% / 2.47 / 27 | 5.4% / 0.96 / 40 | 0.1% / 0.05 / 59 |
| 74 | 1.7% / 0.48 / 27 | 12.7% / 2.95 / 24 | 13.9% / 1.65 / 20 | -5.3% / -0.96 / 24 | 1.9% / 0.38 / 22 |
| 75 | 6.6% / 1.31 / 35 | 8.6% / 1.94 / 23 | 16.8% / 1.58 / 24 | 2.3% / 0.37 / 29 | 0.8% / 0.15 / 32 |
| 76 | 0.9% / 0.25 / 33 | 7.6% / 2.16 / 19 | 12.5% / 1.86 / 20 | 2.6% / 0.40 / 32 | 1.1% / 0.21 / 39 |
| 77 | 0.9% / 0.25 / 40 | 6.8% / 1.70 / 24 | 14.1% / 1.75 / 26 | 10.9% / 1.89 / 34 | -1.9% / -0.26 / 46 |
| 78 | -1.5% / -0.37 / 39 | 8.4% / 2.35 / 21 | 11.8% / 1.41 / 20 | 9.8% / 1.52 / 35 | 2.8% / 0.47 / 37 |
| 79 | 3.5% / 0.81 / 54 | 2.2% / 0.54 / 34 | 18.3% / 1.96 / 41 | 1.7% / 0.31 / 48 | 0.5% / 0.11 / 57 |
| 80 | -1.0% / -0.24 / 45 | 10.7% / 2.72 / 27 | 22.0% / 2.36 / 24 | 1.2% / 0.24 / 37 | -2.7% / -0.37 / 47 |
| 81 | -0.6% / -0.16 / 30 | 11.4% / 2.73 / 21 | 21.4% / 2.25 / 22 | 6.2% / 0.99 / 30 | -5.4% / -0.84 / 34 |
| 82 | -0.5% / -0.14 / 35 | 6.8% / 2.14 / 19 | 11.3% / 1.92 / 15 | 1.0% / 0.22 / 32 | 3.5% / 0.57 / 41 |
| 83 | 4.9% / 1.17 / 40 | 5.0% / 1.50 / 25 | 15.0% / 2.21 / 23 | -1.3% / -0.23 / 33 | 1.3% / 0.27 / 31 |
| 84 | 0.8% / 0.22 / 43 | 5.7% / 1.48 / 28 | 21.0% / 2.19 / 29 | 1.4% / 0.29 / 33 | -1.6% / -0.22 / 43 |
| 85 | -0.9% / -0.28 / 46 | 3.5% / 1.17 / 27 | 14.8% / 2.07 / 26 | 1.2% / 0.32 / 34 | 4.3% / 0.75 / 39 |
| 86 | -1.9% / -0.52 / 41 | 10.0% / 3.08 / 21 | 13.8% / 1.82 / 19 | -1.1% / -0.25 / 29 | 3.1% / 0.54 / 38 |
| 87 | 2.1% / 0.83 / 28 | 4.3% / 1.50 / 24 | 18.7% / 2.52 / 23 | -2.7% / -0.69 / 26 | 1.0% / 0.22 / 25 |
| 88 | 4.0% / 1.17 / 28 | 1.6% / 0.47 / 22 | 18.9% / 2.38 / 25 | 4.2% / 0.97 / 26 | -3.8% / -0.67 / 32 |
| 89 | 0.1% / 0.06 / 27 | 7.3% / 2.04 / 24 | 11.1% / 1.46 / 25 | 2.0% / 0.46 / 27 | 0.7% / 0.15 / 26 |
| 90 | -0.1% / -0.03 / 29 | 9.9% / 2.81 / 20 | 6.7% / 1.33 / 14 | 5.4% / 1.24 / 28 | -2.2% / -0.43 / 24 |
| 91 | 0.8% / 0.22 / 44 | 6.4% / 1.76 / 21 | 17.3% / 1.95 / 25 | 4.8% / 0.61 / 41 | -1.1% / -0.13 / 42 |
| 92 | -0.2% / -0.03 / 53 | 3.3% / 0.92 / 26 | 17.9% / 2.27 / 29 | 9.5% / 1.55 / 38 | -4.8% / -0.63 / 59 |
| 93 | 6.6% / 1.50 / 30 | 8.4% / 1.95 / 20 | 12.4% / 1.25 / 20 | 0.6% / 0.12 / 27 | 1.9% / 0.32 / 30 |
| 94 | 2.1% / 0.62 / 37 | 10.5% / 2.78 / 24 | 17.2% / 2.05 / 21 | -5.4% / -0.96 / 33 | 0.8% / 0.14 / 42 |
| 95 | 3.4% / 0.86 / 40 | 4.0% / 1.06 / 27 | 16.2% / 2.03 / 27 | 6.1% / 1.31 / 36 | -0.2% / 0.00 / 49 |
| 96 | 4.8% / 1.83 / 24 | 2.2% / 0.99 / 14 | 3.2% / 0.74 / 18 | 3.8% / 1.34 / 23 | 3.4% / 0.85 / 27 |
| 97 | 0.2% / 0.07 / 39 | 7.8% / 2.21 / 26 | 11.7% / 1.77 / 20 | -1.7% / -0.28 / 37 | 6.3% / 1.00 / 37 |
| 98 | 1.6% / 0.36 / 53 | 7.5% / 1.53 / 35 | 15.1% / 1.54 / 41 | 4.5% / 0.77 / 44 | 0.4% / 0.09 / 53 |
| 99 | -0.7% / -0.17 / 43 | 5.4% / 1.50 / 25 | 12.1% / 1.49 / 24 | 4.4% / 0.78 / 36 | 2.6% / 0.41 / 39 |
| 100 | 3.9% / 1.07 / 27 | 0.8% / 0.24 / 20 | 21.2% / 2.21 / 25 | 5.0% / 0.94 / 24 | -4.5% / -0.75 / 31 |
| 101 | 4.7% / 1.78 / 24 | 1.8% / 0.79 / 14 | 1.2% / 0.35 / 16 | 3.6% / 1.26 / 23 | 3.7% / 0.96 / 26 |
| 102 | 0.7% / 0.22 / 41 | 8.1% / 2.32 / 26 | 17.4% / 2.08 / 21 | -1.6% / -0.22 / 41 | 2.5% / 0.39 / 43 |
| 103 | -1.3% / -0.35 / 31 | 8.6% / 2.58 / 17 | 7.2% / 1.32 / 14 | 3.9% / 0.77 / 32 | 3.9% / 0.62 / 40 |
| 104 | -1.3% / -0.39 / 32 | 5.6% / 3.01 / 12 | 11.2% / 1.84 / 12 | 5.3% / 1.30 / 30 | -1.2% / -0.19 / 31 |
| 105 | -0.9% / -0.25 / 35 | 4.4% / 1.43 / 21 | 17.6% / 2.48 / 22 | 0.5% / 0.12 / 30 | 0.8% / 0.17 / 42 |
| 106 | -2.0% / -0.61 / 35 | 8.0% / 2.32 / 17 | 14.0% / 2.12 / 12 | 3.6% / 0.89 / 29 | -2.9% / -0.48 / 34 |
| 107 | -3.0% / -0.70 / 44 | 9.5% / 2.39 / 23 | 14.9% / 1.58 / 23 | 3.3% / 0.56 / 37 | 3.2% / 0.48 / 41 |
| 108 | 1.9% / 0.63 / 22 | 7.3% / 2.33 / 16 | 6.8% / 0.98 / 18 | 3.9% / 0.76 / 26 | 2.0% / 0.35 / 30 |
| 109 | -1.1% / -0.34 / 23 | 7.1% / 2.45 / 16 | 9.6% / 1.46 / 18 | 3.8% / 0.79 / 28 | 1.5% / 0.29 / 30 |
| 110 | -3.4% / -0.89 / 38 | 11.6% / 3.08 / 25 | 13.6% / 2.00 / 22 | -0.6% / -0.08 / 38 | 3.8% / 0.60 / 37 |
| 111 | -1.4% / -0.48 / 29 | 11.3% / 2.87 / 22 | 16.7% / 2.32 / 19 | 2.3% / 0.49 / 28 | -4.9% / -0.88 / 28 |
| 112 | -0.4% / -0.11 / 31 | 7.6% / 2.81 / 16 | 12.9% / 2.07 / 15 | -1.3% / -0.38 / 28 | 6.3% / 1.07 / 39 |
| 113 | -0.1% / -0.01 / 29 | 9.9% / 2.82 / 20 | 7.9% / 1.52 / 14 | 6.5% / 1.31 / 28 | -4.8% / -0.91 / 23 |
| 114 | 2.4% / 0.86 / 29 | 5.7% / 1.97 / 18 | 10.4% / 1.66 / 19 | 1.1% / 0.25 / 28 | 0.7% / 0.15 / 33 |
| 115 | 2.2% / 0.67 / 27 | 5.5% / 1.71 / 21 | 9.3% / 1.61 / 21 | 1.5% / 0.34 / 29 | 2.2% / 0.43 / 28 |
| 116 | 4.2% / 0.97 / 57 | 4.4% / 1.24 / 34 | 16.2% / 2.14 / 31 | -0.9% / -0.16 / 47 | -0.2% / -0.01 / 43 |
| 117 | -2.0% / -0.61 / 35 | 7.9% / 2.31 / 17 | 14.0% / 2.12 / 12 | 3.6% / 0.87 / 29 | -3.2% / -0.52 / 34 |
| 118 | 0.3% / 0.10 / 30 | 6.4% / 1.81 / 21 | 17.9% / 2.58 / 20 | -1.4% / -0.23 / 27 | -0.9% / -0.12 / 37 |
| 119 | -0.4% / -0.06 / 49 | 8.9% / 1.91 / 32 | 18.3% / 1.89 / 35 | 1.9% / 0.32 / 47 | 3.0% / 0.45 / 51 |
| 120 | 5.2% / 1.52 / 30 | 2.1% / 0.64 / 24 | 17.2% / 1.97 / 28 | 4.9% / 1.06 / 27 | -4.2% / -0.71 / 35 |
| 121 | 1.3% / 0.33 / 41 | 2.5% / 0.76 / 24 | 23.4% / 2.63 / 29 | -1.6% / -0.18 / 44 | 2.0% / 0.35 / 44 |
| 122 | -1.6% / -0.48 / 28 | 5.4% / 2.88 / 12 | 10.6% / 1.75 / 12 | 5.8% / 1.34 / 28 | -1.2% / -0.20 / 29 |
| 123 | 1.2% / 0.33 / 40 | 6.0% / 1.57 / 24 | 11.5% / 1.50 / 26 | 10.7% / 1.89 / 34 | -2.5% / -0.35 / 46 |
| 124 | -2.4% / -0.67 / 45 | 9.9% / 2.94 / 23 | 13.8% / 1.83 / 19 | -2.4% / -0.57 / 32 | 3.0% / 0.52 / 42 |
| 125 | -2.4% / -0.73 / 45 | 5.8% / 1.56 / 29 | 22.0% / 2.55 / 25 | 5.5% / 0.93 / 41 | -3.9% / -0.63 / 42 |
| 126 | -4.9% / -1.18 / 44 | 8.1% / 2.28 / 27 | 12.1% / 1.85 / 22 | 2.8% / 0.47 / 44 | 5.0% / 0.77 / 40 |
| 127 | -0.0% / 0.01 / 39 | 8.4% / 2.41 / 26 | 11.9% / 1.81 / 20 | -1.8% / -0.30 / 37 | 3.9% / 0.69 / 37 |
| 128 | -1.6% / -0.52 / 36 | 5.8% / 2.44 / 16 | 11.9% / 1.80 / 17 | -0.1% / 0.00 / 32 | 2.2% / 0.44 / 29 |
| 129 | 1.7% / 0.46 / 45 | 5.0% / 1.44 / 27 | 15.5% / 1.82 / 27 | -2.3% / -0.30 / 38 | 4.5% / 0.64 / 51 |
| 130 | 3.7% / 1.51 / 28 | 2.4% / 1.17 / 18 | 9.0% / 1.73 / 21 | -0.2% / -0.05 / 21 | 2.0% / 0.57 / 23 |
| 131 | 1.0% / 0.23 / 48 | 7.5% / 1.52 / 33 | 17.8% / 1.79 / 34 | 6.7% / 0.96 / 39 | 0.8% / 0.15 / 45 |
| 132 | -1.1% / -0.23 / 41 | 6.7% / 1.82 / 25 | 9.2% / 1.36 / 27 | 7.1% / 1.33 / 35 | 3.5% / 0.57 / 43 |
| 133 | 0.6% / 0.25 / 27 | 3.2% / 1.30 / 18 | 14.5% / 2.19 / 17 | 0.4% / 0.09 / 18 | 2.8% / 0.54 / 26 |
| 134 | 2.6% / 0.78 / 25 | 6.1% / 1.86 / 16 | 13.9% / 1.74 / 18 | 4.4% / 0.82 / 26 | -3.5% / -0.56 / 29 |
| 135 | 1.4% / 0.52 / 25 | 3.5% / 1.43 / 18 | 20.7% / 2.92 / 20 | 1.9% / 0.48 / 21 | -0.4% / -0.06 / 23 |
| 136 | 3.2% / 1.05 / 34 | 2.8% / 0.80 / 22 | 10.9% / 1.60 / 23 | 1.0% / 0.19 / 34 | 4.1% / 0.64 / 49 |
| 137 | 4.1% / 1.27 / 30 | 2.2% / 0.61 / 24 | 15.2% / 2.03 / 28 | 4.6% / 1.12 / 27 | -3.4% / -0.57 / 36 |
| 138 | -0.6% / -0.12 / 27 | 13.1% / 3.02 / 23 | 8.8% / 0.99 / 18 | 3.3% / 0.51 / 24 | 3.9% / 0.65 / 21 |
| 139 | -2.8% / -0.74 / 32 | 10.7% / 3.09 / 16 | 4.5% / 0.75 / 14 | 5.5% / 0.96 / 31 | 3.6% / 0.57 / 34 |
| 140 | 5.3% / 1.09 / 58 | 3.7% / 0.85 / 39 | 16.0% / 1.93 / 36 | 0.9% / 0.16 / 54 | 2.8% / 0.47 / 50 |
| 141 | 5.7% / 1.26 / 52 | 3.0% / 0.73 / 32 | 16.7% / 1.77 / 41 | -4.1% / -0.48 / 57 | 4.8% / 0.79 / 49 |
| 142 | 5.9% / 1.23 / 45 | 3.8% / 0.85 / 31 | 14.4% / 1.54 / 32 | 7.6% / 1.24 / 33 | 1.5% / 0.25 / 45 |
| 143 | 3.0% / 0.91 / 30 | 0.7% / 0.28 / 18 | 12.8% / 1.89 / 20 | 3.0% / 0.74 / 24 | -0.5% / -0.06 / 33 |
| 144 | 1.9% / 0.78 / 28 | 2.2% / 0.92 / 24 | 7.4% / 1.65 / 23 | -1.3% / -0.32 / 24 | 3.9% / 1.02 / 22 |
| 145 | -0.4% / -0.11 / 31 | 7.8% / 2.92 / 16 | 11.8% / 1.92 / 15 | -1.3% / -0.38 / 28 | 6.7% / 1.16 / 39 |
| 146 | 3.8% / 0.86 / 47 | 7.7% / 1.59 / 34 | 8.1% / 0.93 / 33 | 6.0% / 1.06 / 37 | 3.1% / 0.53 / 45 |
| 147 | 2.9% / 0.83 / 38 | 4.8% / 1.18 / 32 | 15.6% / 1.78 / 31 | 0.9% / 0.16 / 39 | 0.2% / 0.06 / 36 |
| 148 | 3.9% / 0.90 / 40 | 4.3% / 1.16 / 28 | 16.2% / 2.11 / 31 | 1.1% / 0.22 / 34 | -2.1% / -0.36 / 31 |
| 149 | -0.5% / -0.16 / 27 | 3.5% / 1.45 / 17 | 6.9% / 1.24 / 16 | 5.5% / 1.23 / 20 | 2.3% / 0.47 / 27 |
| 150 | 3.0% / 1.00 / 34 | 2.8% / 0.80 / 22 | 10.9% / 1.60 / 23 | 1.1% / 0.21 / 34 | 3.9% / 0.61 / 49 |
| 151 | 1.8% / 0.54 / 27 | 2.7% / 1.09 / 15 | 7.9% / 1.48 / 15 | 4.0% / 1.09 / 23 | -0.0% / 0.01 / 25 |
| 152 | 3.0% / 0.74 / 29 | 9.0% / 2.12 / 19 | 13.1% / 1.31 / 23 | -3.5% / -0.44 / 29 | 5.8% / 0.92 / 27 |
| 153 | -0.0% / 0.01 / 41 | 4.2% / 1.22 / 23 | 17.5% / 1.91 / 28 | 7.3% / 1.25 / 37 | 0.9% / 0.16 / 44 |
| 154 | 2.4% / 0.86 / 29 | 5.7% / 2.14 / 18 | 10.2% / 1.65 / 19 | 0.7% / 0.17 / 28 | -0.7% / -0.10 / 33 |
| 155 | 3.1% / 0.94 / 28 | 9.0% / 2.74 / 18 | 8.4% / 1.41 / 13 | -3.9% / -1.02 / 23 | 1.5% / 0.30 / 28 |
| 156 | -1.9% / -0.71 / 30 | 5.3% / 2.77 / 11 | 7.8% / 1.60 / 13 | 4.9% / 1.22 / 27 | 0.9% / 0.21 / 28 |
| 157 | -1.8% / -0.57 / 36 | 5.5% / 2.42 / 16 | 11.6% / 1.79 / 17 | -1.2% / -0.28 / 32 | 4.6% / 1.00 / 30 |
| 158 | 2.8% / 0.83 / 39 | 5.8% / 1.58 / 27 | 10.9% / 1.40 / 31 | -1.1% / -0.13 / 38 | 3.5% / 0.65 / 37 |
| 159 | 5.3% / 1.43 / 25 | 2.5% / 0.64 / 24 | 20.2% / 2.25 / 23 | 0.3% / 0.08 / 28 | -3.1% / -0.47 / 33 |
| 160 | -1.6% / -0.55 / 40 | 5.5% / 2.09 / 22 | 4.4% / 0.94 / 18 | 6.8% / 1.61 / 30 | 0.5% / 0.12 / 37 |
| 161 | 3.0% / 0.93 / 27 | 9.2% / 2.77 / 18 | 7.9% / 1.32 / 13 | -3.7% / -0.96 / 23 | 1.4% / 0.29 / 28 |
| 162 | 1.0% / 0.33 / 31 | 8.2% / 2.48 / 23 | 14.0% / 1.93 / 21 | -0.5% / -0.08 / 27 | -2.8% / -0.52 / 27 |
| 163 | 3.6% / 1.13 / 24 | 5.7% / 1.84 / 17 | 8.1% / 1.22 / 19 | 5.9% / 1.07 / 27 | -1.8% / -0.27 / 30 |
| 164 | 2.9% / 0.86 / 32 | 7.3% / 2.03 / 24 | 12.8% / 1.71 / 26 | -2.6% / -0.37 / 30 | 0.9% / 0.18 / 30 |
| 165 | 1.9% / 0.60 / 25 | 6.5% / 1.88 / 19 | 16.4% / 2.28 / 18 | -0.8% / -0.15 / 23 | -2.4% / -0.44 / 22 |
| 166 | 2.2% / 0.84 / 28 | 2.2% / 0.92 / 24 | 6.8% / 1.57 / 23 | -1.5% / -0.41 / 24 | 3.2% / 0.85 / 22 |
| 167 | -1.5% / -0.39 / 39 | 7.4% / 2.18 / 21 | 9.2% / 1.17 / 20 | 8.6% / 1.43 / 35 | 2.9% / 0.48 / 37 |
| 168 | 2.5% / 0.65 / 39 | 1.7% / 0.49 / 27 | 19.6% / 2.42 / 25 | 0.8% / 0.14 / 35 | -1.6% / -0.23 / 38 |
| 169 | 0.5% / 0.18 / 27 | 3.3% / 1.32 / 18 | 13.5% / 2.05 / 17 | 0.4% / 0.11 / 18 | 1.8% / 0.36 / 26 |
| 170 | -2.0% / -0.68 / 40 | 5.2% / 2.08 / 22 | 4.7% / 1.02 / 18 | 7.0% / 1.62 / 30 | 0.5% / 0.12 / 37 |
| 171 | 6.3% / 1.42 / 37 | 8.0% / 1.82 / 24 | 17.4% / 1.83 / 27 | -1.1% / -0.15 / 31 | -2.4% / -0.38 / 32 |
| 172 | 3.3% / 1.31 / 27 | 2.0% / 0.91 / 18 | 8.0% / 1.65 / 20 | -0.6% / -0.16 / 20 | 2.3% / 0.71 / 22 |
| 173 | 2.2% / 0.65 / 23 | 6.3% / 1.90 / 17 | 7.4% / 1.08 / 17 | 4.7% / 0.84 / 27 | 3.1% / 0.50 / 28 |
| 174 | 6.0% / 1.24 / 53 | 2.0% / 0.51 / 37 | 19.0% / 2.16 / 35 | -3.3% / -0.44 / 47 | 2.3% / 0.38 / 48 |
| 175 | 0.5% / 0.20 / 22 | 4.0% / 1.91 / 18 | 11.0% / 1.93 / 18 | 2.8% / 0.62 / 22 | -1.7% / -0.31 / 24 |
| 176 | 6.9% / 1.83 / 26 | 1.3% / 0.38 / 24 | 19.0% / 2.28 / 23 | -3.7% / -0.52 / 30 | 0.0% / 0.03 / 33 |
| 177 | 3.6% / 1.15 / 31 | 8.2% / 2.51 / 22 | 18.9% / 2.07 / 23 | -4.8% / -0.78 / 24 | 0.2% / 0.06 / 33 |
| 178 | 1.7% / 0.43 / 34 | 6.2% / 2.31 / 15 | 5.8% / 0.90 / 17 | 9.4% / 1.62 / 25 | -2.4% / -0.36 / 33 |
| 179 | -0.3% / -0.05 / 49 | 7.7% / 1.71 / 32 | 18.0% / 1.92 / 35 | 1.8% / 0.31 / 47 | 0.0% / 0.04 / 51 |
| 180 | 1.4% / 0.34 / 49 | 8.6% / 2.04 / 32 | 14.2% / 1.82 / 30 | -1.8% / -0.31 / 40 | -0.7% / -0.08 / 42 |
| 181 | 5.6% / 1.11 / 54 | 6.6% / 1.30 / 36 | 9.8% / 1.10 / 39 | 7.3% / 1.22 / 40 | -0.5% / -0.05 / 49 |
| 182 | 2.2% / 0.56 / 32 | 6.6% / 2.31 / 15 | 7.1% / 1.08 / 17 | 10.1% / 1.72 / 25 | -3.6% / -0.56 / 33 |
| 183 | -1.5% / -0.37 / 27 | 13.7% / 3.06 / 23 | 6.1% / 0.72 / 18 | 3.3% / 0.55 / 24 | 4.9% / 0.85 / 22 |
| 184 | -0.9% / -0.25 / 53 | 5.2% / 1.71 / 26 | 11.6% / 1.77 / 27 | 3.4% / 0.97 / 34 | -0.2% / -0.01 / 49 |
| 185 | -5.2% / -1.31 / 44 | 7.7% / 1.92 / 24 | 8.6% / 1.18 / 25 | 7.3% / 1.39 / 30 | 3.1% / 0.49 / 46 |
| 186 | 0.1% / 0.06 / 25 | 8.8% / 2.62 / 17 | 7.7% / 1.00 / 16 | 1.5% / 0.28 / 22 | 6.1% / 1.05 / 20 |
| 187 | -1.4% / -0.29 / 42 | 5.7% / 1.74 / 23 | 13.0% / 1.90 / 20 | 1.7% / 0.34 / 41 | 5.3% / 0.87 / 41 |
| 188 | -0.0% / 0.02 / 50 | 5.0% / 1.42 / 30 | 14.0% / 1.90 / 28 | 1.8% / 0.34 / 47 | 3.3% / 0.54 / 45 |
| 189 | 1.1% / 0.27 / 29 | 12.2% / 2.92 / 20 | 2.0% / 0.30 / 16 | 8.0% / 1.20 / 27 | 1.6% / 0.26 / 27 |
| 190 | 0.3% / 0.12 / 24 | 5.6% / 1.65 / 19 | 17.8% / 2.31 / 20 | 3.7% / 0.75 / 26 | -3.4% / -0.70 / 24 |
| 191 | 0.9% / 0.29 / 41 | 8.7% / 2.01 / 32 | 8.3% / 1.29 / 26 | -1.5% / -0.28 / 43 | 5.3% / 0.85 / 43 |
| 192 | 2.9% / 0.81 / 31 | 4.7% / 1.74 / 13 | 9.4% / 1.29 / 16 | 7.2% / 1.42 / 23 | -2.6% / -0.41 / 33 |
| 193 | 4.0% / 0.96 / 38 | 9.5% / 2.27 / 25 | 17.1% / 1.99 / 23 | -3.9% / -0.71 / 32 | -3.3% / -0.54 / 29 |
| 194 | -1.9% / -0.42 / 38 | 9.6% / 2.54 / 23 | 8.3% / 1.11 / 21 | 8.7% / 1.26 / 36 | -0.2% / 0.01 / 39 |
| 195 | 0.7% / 0.24 / 41 | 9.4% / 2.10 / 32 | 7.9% / 1.24 / 26 | -0.8% / -0.13 / 43 | 5.0% / 0.81 / 43 |
| 196 | -1.0% / -0.31 / 53 | 5.2% / 1.71 / 26 | 11.5% / 1.76 / 27 | 3.6% / 1.02 / 34 | -0.2% / -0.01 / 49 |
| 197 | -1.5% / -0.34 / 41 | 6.4% / 1.76 / 25 | 8.2% / 1.27 / 27 | 7.5% / 1.40 / 35 | 3.3% / 0.54 / 43 |
| 198 | 0.3% / 0.11 / 24 | 5.8% / 1.69 / 19 | 18.0% / 2.32 / 20 | 3.7% / 0.75 / 26 | -3.5% / -0.71 / 24 |
| 199 | 5.2% / 1.34 / 31 | 3.1% / 0.97 / 16 | 12.2% / 1.89 / 17 | -2.6% / -0.47 / 26 | 0.7% / 0.17 / 27 |
| 200 | -0.2% / -0.05 / 30 | 6.7% / 2.72 / 16 | 11.0% / 1.70 / 15 | 5.0% / 1.00 / 28 | -0.8% / -0.09 / 33 |
| 201 | -0.3% / -0.09 / 27 | 3.8% / 1.55 / 17 | 6.9% / 1.22 / 16 | 4.1% / 0.94 / 19 | 2.5% / 0.50 / 26 |
| 202 | -0.6% / -0.11 / 45 | 8.4% / 1.94 / 28 | 13.6% / 1.78 / 24 | 3.4% / 0.50 / 41 | 1.4% / 0.25 / 42 |
| 203 | -2.9% / -0.64 / 56 | 7.5% / 1.60 / 37 | 21.7% / 2.47 / 31 | -2.5% / -0.34 / 47 | 0.8% / 0.16 / 45 |
| 204 | 0.3% / 0.08 / 55 | 6.8% / 1.40 / 38 | 14.5% / 1.59 / 35 | 5.8% / 0.91 / 49 | -1.5% / -0.21 / 45 |
| 205 | 0.2% / 0.08 / 50 | 8.5% / 1.76 / 35 | 18.9% / 2.11 / 30 | -3.9% / -0.66 / 38 | 1.1% / 0.21 / 42 |
| 206 | 0.3% / 0.09 / 42 | 4.7% / 1.26 / 26 | 16.0% / 2.11 / 27 | -0.0% / 0.03 / 43 | 2.0% / 0.34 / 49 |
| 207 | -1.6% / -0.35 / 43 | 8.2% / 2.33 / 22 | 11.4% / 1.75 / 20 | 1.6% / 0.32 / 41 | 4.3% / 0.72 / 41 |
| 208 | 4.4% / 1.14 / 28 | -0.2% / -0.06 / 18 | 13.2% / 2.47 / 16 | 0.5% / 0.12 / 21 | 4.2% / 0.82 / 31 |
| 209 | 2.6% / 0.61 / 34 | 8.8% / 2.18 / 23 | 14.6% / 1.79 / 20 | -2.0% / -0.34 / 29 | -0.8% / -0.11 / 29 |
| 210 | 0.3% / 0.08 / 46 | 9.5% / 2.16 / 28 | 12.9% / 1.73 / 24 | 1.7% / 0.27 / 42 | 1.0% / 0.19 / 42 |
| 211 | 2.7% / 0.63 / 51 | 6.4% / 1.46 / 34 | 16.1% / 1.70 / 33 | 2.9% / 0.48 / 47 | -1.1% / -0.13 / 53 |
| 212 | -1.5% / -0.51 / 32 | 5.1% / 2.77 / 11 | 6.8% / 1.49 / 13 | 4.9% / 1.22 / 27 | 1.0% / 0.21 / 28 |
| 213 | 2.2% / 0.47 / 48 | 9.6% / 2.16 / 32 | 9.2% / 1.02 / 30 | 5.0% / 0.77 / 40 | -1.2% / -0.15 / 41 |
| 214 | -1.4% / -0.47 / 41 | 2.4% / 0.88 / 25 | 9.6% / 1.80 / 25 | 3.6% / 0.94 / 34 | 3.1% / 0.72 / 38 |
| 215 | 6.7% / 1.43 / 44 | 3.1% / 0.93 / 29 | 8.1% / 1.32 / 29 | -5.3% / -0.77 / 38 | 9.8% / 1.74 / 40 |
| 216 | 3.5% / 1.13 / 31 | 8.0% / 2.47 / 22 | 19.3% / 2.09 / 23 | -5.2% / -0.86 / 24 | 0.3% / 0.08 / 33 |
| 217 | 2.8% / 0.66 / 67 | 2.7% / 0.68 / 41 | 17.3% / 1.90 / 44 | 2.8% / 0.46 / 52 | -0.9% / -0.10 / 56 |
| 218 | 2.6% / 0.59 / 73 | 4.4% / 0.96 / 47 | 18.8% / 1.93 / 51 | 4.1% / 0.72 / 55 | -3.9% / -0.57 / 68 |
| 219 | 4.5% / 1.09 / 37 | 6.5% / 1.71 / 25 | 13.4% / 1.87 / 27 | -1.0% / -0.17 / 32 | -0.8% / -0.12 / 34 |
| 220 | -4.2% / -1.08 / 44 | 7.2% / 1.83 / 24 | 8.0% / 1.13 / 25 | 6.8% / 1.32 / 30 | 2.8% / 0.45 / 46 |
| 221 | 4.1% / 0.86 / 35 | 8.8% / 1.89 / 23 | 15.6% / 1.65 / 26 | -3.0% / -0.40 / 29 | 1.2% / 0.21 / 34 |
| 222 | 1.2% / 0.39 / 33 | 4.5% / 1.97 / 12 | 7.8% / 1.28 / 15 | 1.3% / 0.31 / 31 | 3.6% / 0.75 / 27 |
| 223 | 3.4% / 1.33 / 24 | 2.7% / 0.86 / 20 | 13.8% / 1.98 / 21 | -0.1% / 0.00 / 23 | -0.1% / 0.01 / 32 |
| 224 | -0.9% / -0.26 / 27 | 8.6% / 3.39 / 12 | 5.4% / 1.03 / 11 | 12.7% / 1.90 / 29 | -3.8% / -0.61 / 30 |
| 225 | -0.9% / -0.30 / 41 | 2.4% / 0.88 / 25 | 9.2% / 1.79 / 25 | 3.1% / 0.81 / 34 | 2.9% / 0.67 / 39 |
| 226 | 0.3% / 0.10 / 35 | 4.6% / 1.73 / 15 | 13.8% / 1.78 / 17 | 6.1% / 1.28 / 26 | -4.1% / -0.63 / 39 |
| 227 | 2.5% / 0.55 / 56 | 5.7% / 1.24 / 36 | 13.3% / 1.51 / 35 | 7.4% / 1.20 / 47 | -2.0% / -0.26 / 50 |
| 228 | -2.0% / -0.66 / 33 | 2.7% / 2.15 / 11 | 3.0% / 0.98 / 12 | 6.6% / 1.79 / 26 | 2.1% / 0.57 / 28 |
| 229 | -1.5% / -0.48 / 38 | 8.4% / 3.26 / 14 | 7.3% / 1.41 / 13 | 7.6% / 1.23 / 41 | -2.0% / -0.31 / 36 |
| 230 | 2.6% / 0.57 / 31 | 8.4% / 1.79 / 23 | 13.5% / 1.41 / 22 | -0.0% / 0.03 / 25 | 1.6% / 0.28 / 29 |
| 231 | -0.7% / -0.23 / 32 | 6.0% / 2.66 / 16 | 9.0% / 1.50 / 15 | 6.7% / 1.32 / 29 | -0.5% / -0.05 / 34 |
| 232 | 3.3% / 1.36 / 26 | 2.6% / 1.25 / 16 | 5.8% / 0.99 / 18 | 0.4% / 0.17 / 16 | 4.8% / 1.11 / 25 |
| 233 | 2.2% / 0.70 / 23 | -0.2% / -0.04 / 17 | 12.3% / 2.11 / 17 | -1.6% / -0.25 / 18 | 6.3% / 1.33 / 25 |
| 234 | -1.7% / -0.44 / 44 | 4.3% / 1.60 / 16 | 12.7% / 2.18 / 16 | -2.2% / -0.46 / 32 | 4.4% / 0.86 / 34 |
| 235 | -1.8% / -0.61 / 33 | 2.6% / 2.15 / 11 | 3.0% / 0.98 / 12 | 6.4% / 1.74 / 26 | 2.1% / 0.57 / 28 |
| 236 | 3.8% / 1.03 / 45 | -0.8% / -0.23 / 33 | 19.1% / 2.25 / 34 | 5.0% / 0.78 / 38 | -3.0% / -0.48 / 51 |
| 237 | 2.9% / 0.73 / 33 | 3.4% / 1.10 / 18 | 6.3% / 0.91 / 17 | 5.1% / 0.97 / 29 | 5.0% / 1.02 / 24 |
| 238 | 2.1% / 0.48 / 58 | 3.1% / 0.78 / 37 | 7.6% / 1.06 / 35 | 6.6% / 1.11 / 49 | 2.0% / 0.34 / 53 |
| 239 | 2.8% / 0.83 / 26 | 2.3% / 0.66 / 20 | 16.4% / 2.10 / 24 | 1.0% / 0.19 / 22 | 0.2% / 0.06 / 32 |
| 240 | -2.3% / -0.69 / 40 | 10.9% / 3.99 / 18 | 10.9% / 1.70 / 15 | -0.4% / -0.05 / 34 | 1.1% / 0.22 / 40 |
| 241 | 2.5% / 0.88 / 26 | 1.5% / 0.69 / 14 | 4.4% / 0.83 / 15 | 3.2% / 0.91 / 23 | 2.4% / 0.61 / 23 |
| 242 | 2.5% / 0.66 / 33 | 2.6% / 0.86 / 18 | 5.8% / 0.86 / 17 | 3.8% / 0.78 / 29 | 5.6% / 1.14 / 24 |
| 243 | 7.4% / 2.19 / 25 | -0.1% / -0.01 / 22 | 14.4% / 2.21 / 21 | -3.7% / -0.84 / 25 | 1.0% / 0.20 / 31 |
| 244 | 6.1% / 1.44 / 37 | 6.2% / 1.64 / 25 | 12.8% / 1.78 / 27 | -1.3% / -0.23 / 31 | -1.2% / -0.20 / 33 |
| 245 | 4.8% / 2.25 / 25 | 1.7% / 0.94 / 15 | 3.8% / 0.79 / 21 | 2.8% / 0.88 / 28 | 3.8% / 0.81 / 33 |
| 246 | 4.6% / 2.20 / 25 | 1.7% / 0.94 / 15 | 3.8% / 0.79 / 21 | 2.8% / 0.87 / 28 | 4.3% / 0.90 / 33 |
| 247 | 2.7% / 1.11 / 26 | 2.7% / 1.26 / 16 | 6.5% / 1.08 / 18 | 0.2% / 0.08 / 16 | 4.7% / 1.06 / 25 |
| 248 | 4.6% / 1.23 / 28 | -1.7% / -0.61 / 18 | 10.4% / 2.14 / 16 | -1.0% / -0.14 / 21 | 5.6% / 1.17 / 32 |
| 249 | -1.3% / -0.50 / 29 | 3.3% / 1.31 / 22 | 7.5% / 1.87 / 18 | 4.6% / 1.16 / 28 | -0.6% / -0.14 / 27 |
| 250 | -1.3% / -0.50 / 29 | 4.0% / 1.59 / 22 | 7.8% / 1.91 / 18 | 4.5% / 1.14 / 28 | -0.3% / -0.06 / 27 |
| 251 | -2.1% / -0.69 / 30 | 6.1% / 2.60 / 12 | 4.1% / 1.02 / 14 | 11.5% / 1.82 / 31 | -0.7% / -0.08 / 33 |
| 252 | 4.2% / 0.92 / 45 | 5.2% / 1.10 / 31 | 9.7% / 1.09 / 32 | 7.1% / 1.17 / 33 | 1.2% / 0.21 / 45 |
| 253 | 4.7% / 1.03 / 36 | 9.1% / 2.08 / 20 | 11.8% / 1.20 / 27 | 3.6% / 0.59 / 28 | -2.2% / -0.34 / 33 |
| 254 | 4.1% / 0.96 / 37 | 8.4% / 1.87 / 24 | 14.6% / 1.66 / 27 | 0.3% / 0.08 / 32 | -4.0% / -0.62 / 34 |
| 255 | 8.2% / 2.51 / 24 | -3.1% / -1.08 / 14 | 14.2% / 2.18 / 18 | -2.8% / -0.72 / 19 | 4.0% / 0.79 / 25 |
| 256 | -2.9% / -0.67 / 31 | 10.0% / 2.23 / 22 | 7.4% / 0.90 / 19 | 3.4% / 0.55 / 28 | 5.6% / 0.84 / 28 |
| 257 | -1.8% / -0.67 / 33 | 2.2% / 0.76 / 25 | 12.8% / 2.33 / 24 | 4.5% / 1.11 / 32 | -2.5% / -0.68 / 34 |
| 258 | 3.8% / 1.18 / 29 | 3.9% / 1.45 / 18 | 6.9% / 1.40 / 16 | 3.6% / 0.84 / 29 | -3.2% / -0.70 / 30 |
| 259 | 5.2% / 1.43 / 26 | 0.6% / 0.19 / 21 | 12.7% / 1.84 / 25 | -1.9% / -0.33 / 22 | 5.9% / 0.97 / 32 |
| 260 | -0.2% / -0.03 / 30 | 6.3% / 2.63 / 12 | 2.9% / 0.66 / 14 | 10.9% / 1.73 / 30 | -1.0% / -0.13 / 32 |
| 261 | 3.1% / 0.90 / 22 | 9.0% / 2.41 / 14 | 13.5% / 1.93 / 16 | -4.6% / -0.68 / 21 | 2.0% / 0.36 / 27 |
| 262 | 6.2% / 1.78 / 23 | -2.9% / -0.89 / 15 | 11.8% / 2.20 / 16 | 0.2% / 0.07 / 20 | 8.1% / 1.79 / 26 |
| 263 | -2.9% / -0.77 / 35 | 7.9% / 2.69 / 19 | 10.1% / 1.50 / 15 | 2.1% / 0.39 / 37 | 4.1% / 0.73 / 36 |
| 264 | 6.1% / 1.31 / 36 | 8.9% / 2.05 / 20 | 10.8% / 1.06 / 26 | 3.0% / 0.48 / 28 | -2.2% / -0.34 / 33 |
| 265 | 2.0% / 0.53 / 35 | 8.2% / 2.08 / 22 | 9.6% / 1.47 / 23 | -2.0% / -0.38 / 29 | 2.1% / 0.40 / 36 |
| 266 | -0.2% / -0.04 / 35 | 4.2% / 1.66 / 16 | 7.7% / 1.49 / 14 | -2.4% / -0.70 / 29 | 5.8% / 1.41 / 35 |
| 267 | 1.6% / 0.64 / 22 | 1.7% / 0.76 / 16 | 16.8% / 2.63 / 18 | 0.5% / 0.17 / 22 | -3.5% / -0.64 / 25 |
| 268 | -0.1% / -0.02 / 35 | 4.2% / 1.66 / 16 | 7.7% / 1.49 / 14 | -2.4% / -0.70 / 29 | 5.8% / 1.41 / 35 |
| 269 | 3.8% / 1.12 / 29 | 11.7% / 3.10 / 19 | 15.0% / 1.68 / 18 | -0.9% / -0.18 / 25 | 3.5% / 0.63 / 27 |
| 270 | 3.1% / 0.72 / 33 | 6.0% / 1.47 / 21 | 13.5% / 1.34 / 23 | 1.1% / 0.19 / 31 | 6.4% / 1.02 / 32 |
| 271 | -0.8% / -0.16 / 43 | 2.5% / 0.74 / 29 | 7.5% / 1.22 / 24 | 6.5% / 1.22 / 39 | 3.9% / 0.64 / 45 |
| 272 | 2.9% / 1.13 / 30 | -2.1% / -0.73 / 23 | 5.7% / 1.39 / 19 | 2.8% / 1.46 / 22 | 4.4% / 1.11 / 32 |
| 273 | -0.8% / -0.27 / 33 | 5.3% / 2.32 / 17 | 6.0% / 1.52 / 14 | -0.9% / -0.33 / 25 | 3.5% / 0.90 / 37 |
| 274 | 1.4% / 0.56 / 26 | 4.5% / 1.62 / 20 | 9.2% / 1.79 / 21 | 1.7% / 0.43 / 27 | -0.7% / -0.19 / 26 |
| 275 | 4.2% / 1.15 / 30 | 9.1% / 2.64 / 19 | 12.3% / 1.53 / 18 | 0.3% / 0.09 / 26 | 2.1% / 0.40 / 28 |
| 276 | 1.4% / 0.56 / 26 | 4.0% / 1.55 / 20 | 9.2% / 1.79 / 21 | 1.4% / 0.37 / 27 | -1.2% / -0.33 / 26 |
| 277 | 3.3% / 1.23 / 30 | -2.8% / -0.95 / 23 | 5.3% / 1.32 / 19 | 2.4% / 1.29 / 21 | 4.9% / 1.23 / 31 |
| 278 | 1.1% / 0.39 / 26 | 2.7% / 1.24 / 20 | 19.1% / 2.66 / 20 | -3.3% / -0.82 / 26 | -0.7% / -0.10 / 28 |
| 279 | 2.0% / 0.49 / 35 | 7.6% / 1.94 / 23 | 11.8% / 1.68 / 20 | 0.8% / 0.17 / 31 | -1.4% / -0.21 / 29 |
| 280 | 0.7% / 0.18 / 29 | 9.3% / 2.27 / 20 | 12.4% / 1.32 / 24 | -0.4% / -0.02 / 26 | 2.9% / 0.49 / 30 |
| 281 | 3.3% / 1.11 / 32 | 2.6% / 0.95 / 18 | 5.9% / 1.55 / 17 | -2.3% / -0.65 / 28 | 5.1% / 1.68 / 24 |
| 282 | 3.0% / 1.01 / 32 | 3.0% / 1.08 / 18 | 6.0% / 1.57 / 17 | -2.3% / -0.65 / 28 | 5.1% / 1.68 / 24 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_37fc` | 5 | 0.83 | 0.83/0.89 | 0.60/0.77 |
| 1 | `cfg_43ab` | 8 | 0.90 | 0.86/0.90 | 0.72/0.83 |
| 2 | `cfg_009d` | 2 | 1.00 | 1.00/1.00 | 0.99/0.99 |
| 3 | `cfg_a5c4` | 5 | 0.90 | 0.93/0.97 | 0.81/0.90 |
| 4 | `cfg_0f5d` | 4 | 0.92 | 0.93/0.95 | 0.88/0.90 |
| 5 | `cfg_e1d6` | 11 | 0.81 | 0.80/0.88 | 0.58/0.75 |
| 6 | `cfg_01f4` | 5 | 0.88 | 0.91/0.95 | 0.85/0.89 |
| 7 | `cfg_0265` | 8 | 0.91 | 0.91/0.95 | 0.81/0.87 |
| 8 | `cfg_02d2` | 9 | 0.82 | 0.83/0.91 | 0.64/0.78 |
| 9 | `cfg_cf19` | 9 | 0.82 | 0.89/0.93 | 0.76/0.85 |
| 10 | `cfg_f978` | 6 | 0.83 | 0.88/0.89 | 0.75/0.84 |
| 11 | `cfg_2975` | 17 | 0.85 | 0.75/0.86 | 0.55/0.72 |
| 12 | `cfg_04b5` | 2 | 0.89 | 0.86/0.86 | 0.70/0.70 |
| 13 | `cfg_5d59` | 12 | 0.84 | 0.90/0.92 | 0.78/0.84 |
| 14 | `cfg_503c` | 15 | 0.86 | 0.88/0.93 | 0.71/0.84 |
| 15 | `cfg_e7e9` | 15 | 0.81 | 0.79/0.84 | 0.53/0.59 |
| 16 | `cfg_19a8` | 4 | 0.88 | 0.88/0.89 | 0.87/0.89 |
| 17 | `cfg_b2b6` | 26 | 0.84 | 0.78/0.85 | 0.56/0.73 |
| 18 | `cfg_0887` | 7 | 0.85 | 0.68/0.91 | 0.32/0.76 |
| 19 | `cfg_0a42` | 7 | 0.86 | 0.90/0.92 | 0.70/0.79 |
| 20 | `cfg_0954` | 2 | 0.90 | 0.92/0.92 | 0.85/0.85 |
| 21 | `cfg_095a` | 3 | 0.99 | 0.98/0.99 | 0.95/0.96 |
| 22 | `cfg_6f33` | 9 | 0.87 | 0.79/0.88 | 0.65/0.79 |
| 23 | `cfg_ef22` | 5 | 0.88 | 0.88/0.93 | 0.71/0.79 |
| 24 | `cfg_46e0` | 4 | 0.87 | 0.86/0.87 | 0.74/0.75 |
| 25 | `cfg_d91f` | 8 | 0.83 | 0.84/0.89 | 0.64/0.70 |
| 26 | `cfg_09d4` | 5 | 0.83 | 0.77/0.81 | 0.64/0.68 |
| 27 | `cfg_78e3` | 6 | 0.83 | 0.88/0.89 | 0.74/0.74 |
| 28 | `cfg_df4a` | 15 | 0.84 | 0.77/0.89 | 0.62/0.87 |
| 29 | `cfg_a4a2` | 4 | 0.93 | 0.92/0.94 | 0.76/0.77 |
| 30 | `cfg_e9e9` | 12 | 0.87 | 0.90/0.92 | 0.79/0.85 |
| 31 | `cfg_0bac` | 6 | 0.89 | 0.89/0.92 | 0.83/0.88 |
| 32 | `cfg_c40a` | 6 | 0.86 | 0.89/0.94 | 0.76/0.85 |
| 33 | `cfg_4970` | 5 | 0.89 | 0.95/0.96 | 0.80/0.89 |
| 34 | `cfg_99af` | 8 | 0.81 | 0.81/0.89 | 0.74/0.85 |
| 35 | `cfg_4945` | 5 | 0.86 | 0.93/0.94 | 0.80/0.81 |
| 36 | `cfg_6c1e` | 20 | 0.87 | 0.76/0.88 | 0.54/0.78 |
| 37 | `cfg_a762` | 6 | 0.83 | 0.84/0.87 | 0.75/0.77 |
| 38 | `cfg_94b5` | 7 | 0.82 | 0.88/0.95 | 0.79/0.92 |
| 39 | `cfg_4393` | 6 | 0.89 | 0.90/0.91 | 0.80/0.81 |
| 40 | `cfg_10b8` | 3 | 0.99 | 0.99/0.99 | 0.97/0.98 |
| 41 | `cfg_11ac` | 1 | n/a | n/a/n/a | n/a/n/a |
| 42 | `cfg_9dbb` | 7 | 0.82 | 0.84/0.90 | 0.79/0.85 |
| 43 | `cfg_125c` | 3 | 0.97 | 0.98/0.99 | 0.98/0.99 |
| 44 | `cfg_3e97` | 11 | 0.88 | 0.86/0.94 | 0.73/0.83 |
| 45 | `cfg_6ab2` | 13 | 0.82 | 0.70/0.85 | 0.49/0.74 |
| 46 | `cfg_befa` | 6 | 0.81 | 0.83/0.89 | 0.61/0.73 |
| 47 | `cfg_9cd6` | 7 | 0.87 | 0.81/0.94 | 0.49/0.87 |
| 48 | `cfg_164a` | 3 | 0.96 | 0.97/0.98 | 0.96/0.96 |
| 49 | `cfg_99fa` | 5 | 0.88 | 0.90/0.96 | 0.85/0.88 |
| 50 | `cfg_4c4a` | 13 | 0.87 | 0.79/0.89 | 0.66/0.78 |
| 51 | `cfg_1767` | 3 | 0.96 | 0.97/0.99 | 0.95/0.97 |
| 52 | `cfg_1795` | 2 | 0.92 | 0.88/0.88 | 0.77/0.77 |
| 53 | `cfg_17a7` | 3 | 0.83 | 0.88/0.89 | 0.76/0.77 |
| 54 | `cfg_f868` | 6 | 0.88 | 0.91/0.94 | 0.82/0.89 |
| 55 | `cfg_93ed` | 6 | 0.88 | 0.89/0.94 | 0.77/0.88 |
| 56 | `cfg_bbba` | 3 | 0.90 | 0.94/0.95 | 0.90/0.93 |
| 57 | `cfg_18cd` | 6 | 0.86 | 0.90/0.93 | 0.94/0.94 |
| 58 | `cfg_cc94` | 17 | 0.80 | 0.79/0.84 | 0.58/0.64 |
| 59 | `cfg_1935` | 2 | 0.98 | 0.98/0.98 | 0.95/0.95 |
| 60 | `cfg_8dae` | 5 | 0.82 | 0.83/0.90 | 0.60/0.77 |
| 61 | `cfg_91e4` | 2 | 0.98 | 0.99/0.99 | 0.99/0.99 |
| 62 | `cfg_e1dc` | 4 | 0.84 | 0.86/0.96 | 0.82/0.93 |
| 63 | `cfg_1e20` | 9 | 0.81 | 0.74/0.90 | 0.68/0.86 |
| 64 | `cfg_7154` | 15 | 0.82 | 0.81/0.92 | 0.64/0.86 |
| 65 | `cfg_1ef0` | 6 | 0.81 | 0.82/0.83 | 0.57/0.58 |
| 66 | `cfg_1f6a` | 1 | n/a | n/a/n/a | n/a/n/a |
| 67 | `cfg_1fbe` | 4 | 0.89 | 0.89/0.96 | 0.82/0.86 |
| 68 | `cfg_6847` | 5 | 0.93 | 0.91/0.94 | 0.93/0.94 |
| 69 | `cfg_e580` | 6 | 0.91 | 0.90/0.92 | 0.74/0.76 |
| 70 | `cfg_30c1` | 7 | 0.83 | 0.86/0.94 | 0.73/0.89 |
| 71 | `cfg_20e6` | 1 | n/a | n/a/n/a | n/a/n/a |
| 72 | `cfg_9fb6` | 3 | 0.84 | 0.76/0.84 | 0.54/0.71 |
| 73 | `cfg_6080` | 18 | 0.82 | 0.75/0.89 | 0.58/0.78 |
| 74 | `cfg_c598` | 7 | 0.87 | 0.81/0.93 | 0.65/0.89 |
| 75 | `cfg_fab2` | 3 | 0.86 | 0.80/0.80 | 0.58/0.59 |
| 76 | `cfg_d1fa` | 10 | 0.83 | 0.72/0.77 | 0.59/0.64 |
| 77 | `cfg_22f5` | 2 | 0.83 | 0.69/0.69 | 0.41/0.41 |
| 78 | `cfg_26ad` | 2 | 0.95 | 0.97/0.97 | 0.94/0.94 |
| 79 | `cfg_666c` | 4 | 0.88 | 0.82/0.95 | 0.63/0.84 |
| 80 | `cfg_8be3` | 6 | 0.81 | 0.72/0.76 | 0.48/0.53 |
| 81 | `cfg_275f` | 1 | n/a | n/a/n/a | n/a/n/a |
| 82 | `cfg_a098` | 10 | 0.81 | 0.56/0.92 | 0.44/0.80 |
| 83 | `cfg_f777` | 2 | 0.96 | 0.97/0.97 | 0.92/0.92 |
| 84 | `cfg_ea31` | 2 | 0.96 | 0.98/0.98 | 0.94/0.94 |
| 85 | `cfg_447b` | 3 | 0.90 | 0.90/0.94 | 0.75/0.86 |
| 86 | `cfg_4d95` | 6 | 0.90 | 0.92/0.95 | 0.81/0.87 |
| 87 | `cfg_afc7` | 8 | 0.88 | 0.85/0.94 | 0.63/0.89 |
| 88 | `cfg_ddfe` | 9 | 0.88 | 0.84/0.89 | 0.74/0.83 |
| 89 | `cfg_f619` | 3 | 0.98 | 0.98/0.99 | 0.99/0.99 |
| 90 | `cfg_51af` | 9 | 0.89 | 0.90/0.94 | 0.80/0.89 |
| 91 | `cfg_c49f` | 3 | 0.98 | 0.99/0.99 | 0.93/0.94 |
| 92 | `cfg_5015` | 3 | 0.93 | 0.96/0.98 | 0.92/0.94 |
| 93 | `cfg_a49a` | 5 | 0.92 | 0.96/0.97 | 0.85/0.92 |
| 94 | `cfg_f9bf` | 7 | 0.80 | 0.77/0.94 | 0.55/0.89 |
| 95 | `cfg_3788` | 2 | 0.83 | 0.87/0.87 | 0.62/0.62 |
| 96 | `cfg_3f8b` | 5 | 0.87 | 0.87/0.94 | 0.77/0.86 |
| 97 | `cfg_872c` | 3 | 0.94 | 0.95/0.96 | 0.89/0.91 |
| 98 | `cfg_3c25` | 5 | 0.94 | 0.93/0.96 | 0.84/0.90 |
| 99 | `cfg_3e81` | 5 | 0.89 | 0.90/0.94 | 0.83/0.90 |
| 100 | `cfg_d861` | 2 | 0.91 | 0.85/0.85 | 0.69/0.69 |
| 101 | `cfg_a20b` | 7 | 0.81 | 0.78/0.87 | 0.57/0.78 |
| 102 | `cfg_3f4c` | 5 | 0.86 | 0.90/0.95 | 0.84/0.92 |
| 103 | `cfg_c50b` | 3 | 0.83 | 0.85/0.92 | 0.78/0.86 |
| 104 | `cfg_cca7` | 5 | 0.82 | 0.74/0.78 | 0.62/0.68 |
| 105 | `cfg_41d0` | 9 | 0.81 | 0.88/0.95 | 0.74/0.85 |
| 106 | `cfg_45d0` | 5 | 0.87 | 0.88/0.93 | 0.73/0.83 |
| 107 | `cfg_f108` | 3 | 0.97 | 0.97/0.98 | 0.94/0.95 |
| 108 | `cfg_4544` | 7 | 0.85 | 0.84/0.94 | 0.74/0.87 |
| 109 | `cfg_8962` | 6 | 0.88 | 0.89/0.96 | 0.84/0.90 |
| 110 | `cfg_71f7` | 4 | 0.85 | 0.84/0.86 | 0.70/0.73 |
| 111 | `cfg_46f1` | 1 | n/a | n/a/n/a | n/a/n/a |
| 112 | `cfg_a533` | 4 | 0.82 | 0.79/0.92 | 0.60/0.82 |
| 113 | `cfg_9cec` | 3 | 0.95 | 0.95/0.97 | 0.88/0.91 |
| 114 | `cfg_49a5` | 1 | n/a | n/a/n/a | n/a/n/a |
| 115 | `cfg_4aaa` | 5 | 0.81 | 0.83/0.85 | 0.70/0.79 |
| 116 | `cfg_7b52` | 5 | 0.82 | 0.70/0.81 | 0.46/0.66 |
| 117 | `cfg_4e6a` | 3 | 0.94 | 0.96/0.97 | 0.92/0.94 |
| 118 | `cfg_ef39` | 3 | 0.90 | 0.89/0.93 | 0.73/0.84 |
| 119 | `cfg_4f7d` | 3 | 0.91 | 0.82/0.86 | 0.64/0.68 |
| 120 | `cfg_4fae` | 6 | 0.84 | 0.88/0.91 | 0.73/0.81 |
| 121 | `cfg_510f` | 5 | 0.86 | 0.90/0.94 | 0.84/0.89 |
| 122 | `cfg_5318` | 3 | 0.91 | 0.90/0.94 | 0.85/0.89 |
| 123 | `cfg_d0e8` | 2 | 1.00 | 1.00/1.00 | 0.99/0.99 |
| 124 | `cfg_8f1b` | 3 | 0.93 | 0.95/0.96 | 0.94/0.96 |
| 125 | `cfg_5770` | 1 | n/a | n/a/n/a | n/a/n/a |
| 126 | `cfg_f7cb` | 4 | 0.91 | 0.94/0.94 | 0.84/0.85 |
| 127 | `cfg_5b62` | 2 | 0.87 | 0.89/0.89 | 0.69/0.69 |
| 128 | `cfg_5d40` | 1 | n/a | n/a/n/a | n/a/n/a |
| 129 | `cfg_be50` | 3 | 0.81 | 0.82/0.83 | 0.70/0.72 |
| 130 | `cfg_f7e5` | 3 | 0.90 | 0.91/0.94 | 0.82/0.87 |
| 131 | `cfg_8efb` | 4 | 0.81 | 0.75/0.83 | 0.51/0.64 |
| 132 | `cfg_6a3f` | 2 | 0.95 | 0.98/0.98 | 0.92/0.92 |
| 133 | `cfg_ba37` | 4 | 0.85 | 0.92/0.96 | 0.83/0.88 |
| 134 | `cfg_b093` | 4 | 0.93 | 0.93/0.93 | 0.84/0.91 |
| 135 | `cfg_7644` | 1 | n/a | n/a/n/a | n/a/n/a |
| 136 | `cfg_db0b` | 2 | 0.88 | 0.91/0.91 | 0.83/0.83 |
| 137 | `cfg_7816` | 1 | n/a | n/a/n/a | n/a/n/a |
| 138 | `cfg_8547` | 1 | n/a | n/a/n/a | n/a/n/a |
| 139 | `cfg_9ca0` | 5 | 0.84 | 0.88/0.94 | 0.75/0.87 |
| 140 | `cfg_8d94` | 1 | n/a | n/a/n/a | n/a/n/a |
| 141 | `cfg_cdf9` | 2 | 0.85 | 0.83/0.83 | 0.68/0.68 |
| 142 | `cfg_9f79` | 3 | 0.97 | 0.99/0.99 | 0.96/0.96 |
| 143 | `cfg_a524` | 1 | n/a | n/a/n/a | n/a/n/a |
| 144 | `cfg_ac56` | 1 | n/a | n/a/n/a | n/a/n/a |
| 145 | `cfg_fe21` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 146 | `cfg_c83e` | 2 | 0.99 | 0.99/0.99 | 0.92/0.92 |
| 147 | `cfg_ce73` | 1 | n/a | n/a/n/a | n/a/n/a |
| 148 | `cfg_f55d` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 4.563e-04 over 17280 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 630.0, participation ratio 6.6, 95%-variance components 149 (rank bound T = 1239); raw grid 17280; raw + known prior 707784
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
