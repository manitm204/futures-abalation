# Screening funnel -- mr_gc_v6_15m (development stages only)

- Code: `7ba1d7ded49f` (dirty working tree: True, diff sha256 `1b4e42f34204`)
- Config: `configs/funnel/mr_funnel_gc_v6_15m.yaml` sha256 `ec4813f17167f994`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'GC': '2026-10-16'}
- Frozen manifest sha256: `2e87b14c042e8940` (221 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_gc_v5 gated 89 GC candidates on 2023-2024 (24 passed) and this grid was written after reading those results, so GC 2023-2024 is partly in-sample here.
- Holdout 2025+ previously inspected: **False** -- No GC strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection). The index and crude holdouts (ES/NQ/YM/RTY/CL) have been scored (other markets).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 21504 | 21504 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 21504 | 21504 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 21504 | 15700 | 5804 | 0 |  | 16992 | 73.01 | 73.01 |  |
| 3 performance & risk | hard_gate | 15700 | 739 | 14961 | 0 |  | 0 | 3.44 | 4.71 |  |
| 4 parameter stability | hard_gate | 739 | 733 | 6 | 0 |  | 0 | 3.41 | 99.19 |  |
| 5 time stability | hard_gate | 733 | 732 | 1 | 0 |  | 362 | 3.40 | 99.86 |  |
| 6 deduplication | dedup | 732 | 221 |  |  | 511 |  | 1.03 | 30.19 | best 2 per cluster |
| 7 execution stress | hard_gate | 221 | 221 | 0 | 0 |  | 0 | 1.03 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 221 |  |  |  |  |  |  |  | diagnostic only: unverified: 221 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 5804 |
| s2:hard_reject:years_with_>=10_trades | 4628 |
| s3:hard_reject:net_return | 8396 |
| s3:hard_reject:sharpe | 14961 |
| s4:hard_reject:local_median_sharpe | 6 |
| s5:hard_reject:profitable_years | 1 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | transfer dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_a956` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 196/29/95 | 320 | 33.8% | 6.1% | 1.31 | -4.7% | 336 | 1.49 | 10.9% | 175.4 | 11/11 | 1.00 | 0.96 | 0.34 | 5 | 17.5% | 0.43 | 0.29 | 31.0% | 26.7% | 28.1% | 32.3%/28.3% | 6.9 (interpolated) | pass | 0.322 (unverified) | n/a |
| 2 | `cfg_9635` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 208/24/88 | 320 | 31.1% | 5.7% | 1.27 | -4.5% | 337 | 1.48 | 10.4% | 174.7 | 11/11 | 1.00 | 0.92 | 0.36 | 5 | 15.7% | 0.45 | 0.28 | 27.8% | 23.4% | 25.6% | 29.6%/25.0% | 6.4 (interpolated) | pass | 0.296 (unverified) | n/a |
| 3 | `cfg_f226` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-3.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 179/89/0 | 268 | 30.3% | 5.5% | 1.19 | -5.6% | 368 | 1.54 | 11.5% | 146.4 | 8/8 | 1.00 | 1.05 | 0.14 | 5 | 15.0% | 0.46 | 0.28 | 27.9% | 24.6% | 27.1% | 30.1%/25.7% | 7.4 (interpolated) | pass | 0.239 (unverified) | n/a |
| 4 | `cfg_3b2f` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 198/90/0 | 288 | 33.0% | 6.0% | 1.21 | -4.9% | 319 | 1.52 | 12.4% | 158.6 | 10/10 | 1.00 | 0.99 | 0.23 | 5 | 18.7% | 0.39 | 0.29 | 30.7% | 26.8% | 27.3% | 31.5%/26.5% | 7.5 (interpolated) | pass | 0.255 (unverified) | n/a |
| 5 | `cfg_f48e` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 143/159/0 | 302 | 30.6% | 5.6% | 1.12 | -6.3% | 336 | 1.47 | 14.1% | 164.9 | 9/9 | 1.00 | 0.95 | 0.17 | 5 | 15.3% | 0.46 | 0.28 | 27.8% | 24.1% | 28.6% | 28.9%/25.0% | 6.7 (interpolated) | pass | 0.199 (unverified) | n/a |
| 6 | `cfg_0bc6` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 181/73/0 | 254 | 27.0% | 5.0% | 1.09 | -4.4% | 306 | 1.53 | 10.3% | 138.6 | 9/9 | 1.00 | 0.92 | 0.18 | 5 | 13.9% | 0.45 | 0.34 | 24.5% | 22.5% | 24.3% | 24.4%/22.3% | 7.4 (interpolated) | pass | 0.182 (unverified) | n/a |
| 7 | `cfg_4a3b` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=12, entry_z=-3.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 147/58/0 | 205 | 24.5% | 4.6% | 1.08 | -4.7% | 336 | 1.59 | 8.6% | 112.0 | 8/8 | 1.00 | 0.90 | 0.19 | 4 | 12.4% | 0.47 | 0.36 | 22.9% | 20.6% | 22.6% | 23.7%/20.8% | 8.1 (interpolated) | pass | 0.176 (unverified) | n/a |
| 8 | `cfg_c3cb` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=8, entry_z=-3.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 173/70/0 | 243 | 22.4% | 4.2% | 1.04 | -6.4% | 424 | 1.53 | 9.6% | 133.0 | 8/8 | 1.00 | 0.79 | 0.25 | 5 | 8.0% | 0.61 | 0.40 | 19.2% | 16.8% | 22.7% | 20.7%/16.9% | 6.2 (interpolated) | pass | 0.152 (unverified) | n/a |
| 9 | `cfg_7d28` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=12, entry_z=-3.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 118/135/0 | 253 | 26.0% | 4.8% | 1.03 | -6.0% | 375 | 1.47 | 11.6% | 137.6 | 9/9 | 1.00 | 0.89 | 0.14 | 4 | 12.6% | 0.49 | 0.32 | 23.7% | 20.5% | 21.3% | 24.1%/18.5% | 6.8 (interpolated) | pass | 0.145 (unverified) | n/a |
| 10 | `cfg_3bd7` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 65/66/30 | 161 | 12.5% | 2.4% | 1.01 | -1.7% | 299 | 1.60 | 4.2% | 89.2 | 11/11 | 0.91 | 0.80 | 0.20 | 5 | 5.8% | 0.52 | 0.49 | 10.8% | 9.5% | 7.1% | 11.5%/9.2% | 6.0 (interpolated) | pass | 0.127 (unverified) | n/a |
| 11 | `cfg_a8f2` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=8, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 186/100/0 | 286 | 24.5% | 4.6% | 0.97 | -4.8% | 313 | 1.43 | 12.0% | 156.1 | 10/10 | 1.00 | 0.86 | 0.11 | 5 | 12.3% | 0.46 | 0.38 | 21.4% | 18.6% | 24.2% | 23.9%/19.8% | 5.8 (interpolated) | pass | 0.118 (unverified) | n/a |
| 12 | `cfg_a7f9` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 153/9/51 | 213 | 18.7% | 3.6% | 0.99 | -5.1% | 388 | 1.49 | 6.4% | 116.8 | 10/10 | 1.00 | 0.84 | 0.15 | 5 | 12.1% | 0.34 | 0.45 | 16.6% | 14.9% | 16.6% | 17.6%/15.6% | 6.5 (interpolated) | pass | 0.122 (unverified) | n/a |
| 13 | `cfg_d004` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 191/21/132 | 344 | 28.6% | 5.2% | 1.13 | -5.8% | 370 | 1.39 | 10.5% | 187.6 | 11/11 | 1.00 | 0.81 | 0.31 | 5 | 14.6% | 0.45 | 0.34 | 24.6% | 20.9% | 20.9% | 27.9%/23.2% | 5.6 (interpolated) | pass | 0.193 (unverified) | n/a |
| 14 | `cfg_3f34` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=8, entry_z=-3.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 158/84/0 | 242 | 23.2% | 4.3% | 1.03 | -5.9% | 419 | 1.50 | 10.2% | 133.3 | 9/9 | 1.00 | 0.94 | 0.09 | 4 | 9.3% | 0.57 | 0.39 | 21.6% | 18.8% | 24.2% | 22.7%/18.4% | 6.6 (interpolated) | pass | 0.143 (unverified) | n/a |
| 15 | `cfg_2add` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-3.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 149/76/0 | 225 | 21.9% | 4.1% | 0.93 | -7.2% | 388 | 1.42 | 9.8% | 123.6 | 9/9 | 0.89 | 0.92 | 0.00 | 5 | 13.7% | 0.36 | 0.44 | 20.4% | 17.8% | 16.9% | 21.1%/17.8% | 7.0 (interpolated) | pass | 0.099 (unverified) | n/a |
| 16 | `cfg_d86e` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-3.0, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 218/15/87 | 320 | 23.4% | 4.4% | 1.03 | -4.6% | 375 | 1.38 | 9.8% | 174.3 | 10/10 | 1.00 | 0.85 | 0.18 | 5 | 10.2% | 0.53 | 0.38 | 20.4% | 17.3% | 18.0% | 22.3%/19.7% | 5.3 (interpolated) | pass | 0.144 (unverified) | n/a |
| 17 | `cfg_bce1` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=18, entry_z=-3.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 36/104/27 | 167 | 11.8% | 2.3% | 0.96 | -2.2% | 389 | 1.61 | 3.3% | 91.5 | 7/7 | 1.00 | 0.85 | 0.11 | 5 | 7.0% | 0.39 | 0.51 | 10.7% | 9.1% | 8.1% | 10.5%/8.3% | 5.6 (interpolated) | pass | 0.104 (unverified) | n/a |
| 18 | `cfg_a1e5` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 102/8/62 | 172 | 11.2% | 2.2% | 1.10 | -1.7% | 336 | 1.65 | 2.9% | 94.7 | 9/9 | 1.00 | 0.93 | 0.16 | 5 | 4.3% | 0.60 | 0.53 | 10.1% | 8.5% | 5.1% | 10.4%/8.7% | 5.4 (interpolated) | pass | 0.164 (unverified) | n/a |
| 19 | `cfg_a4bd` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-3.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 36/95/42 | 173 | 11.4% | 2.2% | 1.00 | -2.0% | 350 | 1.60 | 3.3% | 95.6 | 8/8 | 1.00 | 0.76 | 0.24 | 4 | 4.0% | 0.63 | 0.50 | 10.1% | 8.6% | 9.5% | 10.1%/8.4% | 5.5 (interpolated) | pass | 0.123 (unverified) | n/a |
| 20 | `cfg_ef5a` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-3.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 200/136/0 | 336 | 26.5% | 4.9% | 0.94 | -5.4% | 451 | 1.38 | 15.2% | 185.0 | 9/9 | 1.00 | 0.78 | 0.16 | 4 | 14.8% | 0.39 | 0.36 | 22.8% | 19.6% | 25.7% | 25.6%/21.6% | 5.8 (interpolated) | pass | 0.103 (unverified) | n/a |
| 21 | `cfg_9202` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=8, entry_z=-3.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 171/114/0 | 285 | 26.6% | 4.9% | 0.99 | -4.7% | 333 | 1.43 | 12.7% | 155.8 | 10/10 | 1.00 | 0.82 | 0.17 | 5 | 12.1% | 0.51 | 0.37 | 24.0% | 21.8% | 26.6% | 26.4%/23.1% | 6.4 (interpolated) | pass | 0.123 (unverified) | n/a |
| 22 | `cfg_a9b1` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 145/97/0 | 242 | 26.2% | 4.9% | 1.02 | -5.5% | 336 | 1.48 | 10.4% | 133.0 | 10/10 | 1.00 | 0.77 | 0.25 | 5 | 14.4% | 0.42 | 0.35 | 24.9% | 21.7% | 22.8% | 26.3%/21.9% | 7.4 (interpolated) | pass | 0.139 (unverified) | n/a |
| 23 | `cfg_b810` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-3.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 154/18/71 | 243 | 21.5% | 4.0% | 0.99 | -5.9% | 388 | 1.41 | 8.0% | 133.1 | 10/10 | 0.90 | 0.91 | 0.08 | 5 | 11.6% | 0.44 | 0.41 | 19.8% | 16.8% | 18.2% | 20.8%/16.8% | 6.4 (interpolated) | pass | 0.122 (unverified) | n/a |
| 24 | `cfg_cc15` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-3.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 160/65/0 | 225 | 21.1% | 4.0% | 0.92 | -7.6% | 388 | 1.42 | 9.3% | 123.5 | 9/9 | 1.00 | 0.94 | -0.02 | 5 | 13.2% | 0.36 | 0.42 | 18.7% | 16.7% | 15.2% | 21.0%/16.7% | 6.7 (interpolated) | pass | 0.100 (unverified) | n/a |
| 25 | `cfg_454e` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=18, entry_z=-3.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 19/120/28 | 167 | 11.9% | 2.3% | 0.95 | -2.3% | 486 | 1.60 | 3.4% | 91.9 | 7/7 | 1.00 | 0.83 | 0.12 | 5 | 6.7% | 0.41 | 0.51 | 10.4% | 9.2% | 9.0% | 10.7%/8.8% | 5.6 (interpolated) | pass | 0.097 (unverified) | n/a |
| 26 | `cfg_15b7` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 104/4/63 | 171 | 10.7% | 2.1% | 1.02 | -2.2% | 335 | 1.60 | 2.9% | 94.2 | 9/9 | 1.00 | 0.90 | 0.12 | 4 | 3.6% | 0.65 | 0.55 | 9.5% | 7.9% | 4.0% | 9.9%/8.1% | 5.2 (interpolated) | pass | 0.128 (unverified) | n/a |
| 27 | `cfg_8a0f` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 66/2/49 | 117 | 11.5% | 2.2% | 1.04 | -1.9% | 202 | 1.74 | 2.4% | 63.5 | 10/10 | 0.90 | 0.84 | 0.20 | 5 | 5.2% | 0.53 | 0.55 | 10.5% | 9.6% | 9.9% | 10.7%/8.3% | 7.4 (interpolated) | pass | 0.135 (unverified) | n/a |
| 28 | `cfg_9c26` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-3.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 213/123/0 | 336 | 27.7% | 5.1% | 1.00 | -5.0% | 338 | 1.41 | 14.6% | 184.7 | 8/8 | 1.00 | 0.67 | 0.33 | 4 | 13.9% | 0.44 | 0.34 | 24.1% | 19.9% | 24.9% | 27.0%/23.0% | 5.8 (interpolated) | pass | 0.129 (unverified) | n/a |
| 29 | `cfg_da0c` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 116/86/0 | 202 | 22.9% | 4.3% | 1.03 | -5.1% | 337 | 1.57 | 8.8% | 110.8 | 10/10 | 1.00 | 0.84 | 0.20 | 4 | 13.1% | 0.40 | 0.42 | 21.2% | 19.7% | 21.7% | 21.7%/18.6% | 7.9 (interpolated) | pass | 0.142 (unverified) | n/a |
| 30 | `cfg_671d` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 134/33/47 | 214 | 17.8% | 3.4% | 0.95 | -4.7% | 385 | 1.48 | 6.1% | 117.7 | 11/11 | 1.00 | 0.88 | 0.07 | 5 | 11.1% | 0.36 | 0.46 | 15.8% | 14.2% | 15.5% | 17.2%/14.5% | 6.1 (interpolated) | pass | 0.107 (unverified) | n/a |
| 31 | `cfg_c569` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-3.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 145/21/77 | 243 | 21.6% | 4.1% | 0.96 | -5.8% | 388 | 1.40 | 8.4% | 133.2 | 10/10 | 0.90 | 0.91 | 0.06 | 5 | 11.6% | 0.45 | 0.44 | 19.7% | 17.0% | 18.3% | 20.9%/16.4% | 6.5 (interpolated) | pass | 0.108 (unverified) | n/a |
| 32 | `cfg_991a` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-3.0, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 169/74/0 | 243 | 25.0% | 4.6% | 1.03 | -5.2% | 385 | 1.50 | 9.9% | 133.5 | 9/9 | 1.00 | 0.81 | 0.21 | 4 | 14.5% | 0.39 | 0.31 | 22.0% | 20.2% | 19.8% | 24.5%/20.8% | 7.0 (interpolated) | pass | 0.147 (unverified) | n/a |
| 33 | `cfg_be8b` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 50/57/30 | 137 | 12.7% | 2.5% | 0.98 | -2.5% | 275 | 1.61 | 3.7% | 75.6 | 12/12 | 1.00 | 0.90 | 0.08 | 4 | 6.3% | 0.49 | 0.50 | 11.3% | 10.0% | 10.8% | 11.9%/9.6% | 7.1 (interpolated) | pass | 0.119 (unverified) | n/a |
| 34 | `cfg_ab6e` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 192/141/0 | 333 | 26.9% | 5.0% | 0.94 | -5.4% | 351 | 1.35 | 15.4% | 182.5 | 9/9 | 1.00 | 0.85 | 0.09 | 5 | 14.3% | 0.43 | 0.42 | 22.8% | 18.6% | 23.9% | 25.6%/21.2% | 5.6 (interpolated) | pass | 0.100 (unverified) | n/a |
| 35 | `cfg_0275` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 61/38/70 | 169 | 10.9% | 2.1% | 0.97 | -1.7% | 336 | 1.55 | 3.6% | 93.3 | 10/10 | 1.00 | 0.90 | 0.07 | 5 | 3.7% | 0.64 | 0.55 | 9.8% | 8.4% | 7.4% | 10.0%/8.1% | 5.4 (interpolated) | pass | 0.103 (unverified) | n/a |
| 36 | `cfg_ac0e` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=8, entry_z=-3.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 192/67/0 | 259 | 27.7% | 5.1% | 1.22 | -6.5% | 318 | 1.61 | 11.1% | 141.9 | 8/8 | 0.88 | 0.74 | 0.48 | 4 | 11.3% | 0.55 | 0.32 | 25.1% | 22.3% | 23.0% | 26.2%/22.2% | 7.1 (interpolated) | pass | 0.256 (unverified) | n/a |
| 37 | `cfg_3921` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 136/66/0 | 202 | 21.3% | 4.0% | 1.02 | -4.7% | 338 | 1.57 | 8.3% | 110.8 | 10/10 | 1.00 | 0.81 | 0.21 | 5 | 12.9% | 0.37 | 0.40 | 19.5% | 17.7% | 19.7% | 20.4%/17.1% | 7.4 (interpolated) | pass | 0.142 (unverified) | n/a |
| 38 | `cfg_a901` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=8, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 162/58/0 | 220 | 21.9% | 4.1% | 1.08 | -6.7% | 350 | 1.66 | 8.6% | 121.4 | 10/10 | 1.00 | 0.72 | 0.36 | 3 | 10.6% | 0.48 | 0.41 | 19.9% | 18.3% | 22.7% | 20.9%/18.2% | 7.0 (interpolated) | pass | 0.174 (unverified) | n/a |
| 39 | `cfg_3206` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-3.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 30/101/42 | 173 | 10.8% | 2.1% | 0.94 | -2.0% | 350 | 1.57 | 3.4% | 95.8 | 9/9 | 1.00 | 0.76 | 0.18 | 4 | 3.3% | 0.68 | 0.51 | 9.4% | 8.0% | 8.6% | 9.5%/7.5% | 5.2 (interpolated) | pass | 0.099 (unverified) | n/a |
| 40 | `cfg_f095` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=8, entry_z=-3.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 205/100/0 | 305 | 23.8% | 4.4% | 0.94 | -5.4% | 330 | 1.38 | 13.2% | 167.2 | 9/9 | 1.00 | 0.91 | 0.03 | 4 | 8.6% | 0.59 | 0.35 | 20.1% | 17.1% | 22.0% | 23.4%/19.5% | 5.8 (interpolated) | pass | 0.105 (unverified) | n/a |
| 41 | `cfg_e87b` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 85/92/38 | 215 | 16.7% | 3.2% | 0.94 | -3.8% | 226 | 1.50 | 5.9% | 117.8 | 12/12 | 1.00 | 0.82 | 0.12 | 5 | 11.5% | 0.31 | 0.48 | 15.2% | 13.5% | 14.8% | 16.3%/14.3% | 5.8 (interpolated) | pass | 0.099 (unverified) | n/a |
| 42 | `cfg_95b7` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 59/11/47 | 117 | 11.1% | 2.2% | 1.01 | -1.8% | 202 | 1.73 | 2.3% | 63.5 | 11/11 | 0.91 | 0.85 | 0.16 | 5 | 5.0% | 0.53 | 0.57 | 10.3% | 9.4% | 9.3% | 10.4%/8.9% | 7.2 (interpolated) | pass | 0.123 (unverified) | n/a |
| 43 | `cfg_4c21` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 56/62/59 | 177 | 12.5% | 2.4% | 0.97 | -2.8% | 475 | 1.53 | 4.3% | 98.2 | 9/9 | 1.00 | 0.76 | 0.21 | 4 | 4.6% | 0.60 | 0.45 | 11.4% | 10.0% | 10.9% | 11.8%/9.4% | 5.6 (interpolated) | pass | 0.108 (unverified) | n/a |
| 44 | `cfg_a5f6` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 229/117/0 | 346 | 24.5% | 4.6% | 0.88 | -4.6% | 292 | 1.33 | 14.7% | 189.5 | 9/9 | 0.89 | 0.86 | 0.02 | 5 | 13.7% | 0.40 | 0.41 | 21.6% | 17.4% | 18.8% | 25.2%/20.2% | 5.1 (interpolated) | pass | 0.079 (unverified) | n/a |
| 45 | `cfg_ca39` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 202/69/0 | 271 | 22.8% | 4.3% | 1.03 | -7.9% | 336 | 1.46 | 11.0% | 148.7 | 9/9 | 0.78 | 0.81 | 0.22 | 5 | 15.5% | 0.32 | 0.32 | 20.4% | 17.8% | 20.1% | 22.5%/18.8% | 6.0 (interpolated) | pass | 0.148 (unverified) | n/a |
| 46 | `cfg_787f` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 222/112/0 | 334 | 28.4% | 5.2% | 0.99 | -5.4% | 341 | 1.38 | 14.6% | 184.1 | 10/10 | 1.00 | 0.84 | 0.15 | 5 | 15.8% | 0.41 | 0.40 | 24.7% | 21.7% | 24.3% | 27.2%/22.0% | 5.8 (interpolated) | pass | 0.120 (unverified) | n/a |
| 47 | `cfg_ee3e` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 89/16/23 | 128 | 12.4% | 2.4% | 1.00 | -2.9% | 175 | 1.78 | 3.2% | 69.3 | 11/11 | 1.00 | 0.77 | 0.23 | 5 | 7.0% | 0.44 | 0.48 | 11.2% | 10.1% | 9.8% | 11.2%/9.2% | 7.3 (interpolated) | pass | 0.134 (unverified) | n/a |
| 48 | `cfg_f281` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 37/42/38 | 117 | 9.1% | 1.8% | 0.97 | -1.2% | 165 | 1.75 | 2.0% | 62.8 | 10/10 | 0.90 | 0.79 | 0.19 | 4 | 5.2% | 0.41 | 0.67 | 7.9% | 7.1% | 10.9% | 8.1%/6.3% | 6.1 (interpolated) | pass | 0.095 (unverified) | n/a |
| 49 | `cfg_f411` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=12, entry_z=-3.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 134/24/68 | 226 | 18.5% | 3.5% | 0.90 | -5.0% | 378 | 1.40 | 7.5% | 124.2 | 9/9 | 1.00 | 0.81 | 0.08 | 4 | 7.9% | 0.55 | 0.44 | 16.4% | 14.6% | 18.8% | 18.5%/14.9% | 6.0 (interpolated) | pass | 0.085 (unverified) | n/a |
| 50 | `cfg_2684` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=15, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 24/55/38 | 117 | 8.4% | 1.6% | 0.91 | -1.2% | 166 | 1.68 | 2.1% | 62.7 | 9/9 | 0.89 | 0.70 | 0.21 | 5 | 5.4% | 0.34 | 0.68 | 7.5% | 6.6% | 8.8% | 8.0%/6.4% | 5.8 (interpolated) | pass | 0.074 (unverified) | n/a |
| 51 | `cfg_76b6` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=8, entry_z=-3.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 190/115/0 | 305 | 25.7% | 4.8% | 0.97 | -5.0% | 349 | 1.39 | 13.7% | 166.9 | 9/9 | 1.00 | 0.86 | 0.11 | 4 | 10.5% | 0.54 | 0.35 | 23.3% | 19.4% | 24.8% | 25.2%/20.8% | 6.0 (interpolated) | pass | 0.116 (unverified) | n/a |
| 52 | `cfg_ad59` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 103/213/0 | 316 | 22.5% | 4.2% | 0.93 | -5.5% | 451 | 1.39 | 11.9% | 172.8 | 11/11 | 1.00 | 0.76 | 0.17 | 4 | 12.9% | 0.42 | 0.38 | 19.8% | 17.2% | 21.0% | 21.9%/18.1% | 5.4 (interpolated) | pass | 0.105 (unverified) | n/a |
| 53 | `cfg_326c` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=12, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 112/56/0 | 168 | 13.5% | 2.6% | 0.85 | -4.9% | 335 | 1.55 | 5.7% | 90.8 | 10/10 | 1.00 | 0.82 | 0.03 | 4 | 5.7% | 0.58 | 0.47 | 11.9% | 10.9% | 11.4% | 12.8%/10.9% | 5.8 (interpolated) | pass | 0.076 (unverified) | n/a |
| 54 | `cfg_b06d` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=12, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 118/12/41 | 171 | 13.7% | 2.6% | 0.90 | -4.6% | 337 | 1.52 | 5.5% | 92.7 | 10/10 | 1.00 | 0.72 | 0.17 | 4 | 6.9% | 0.50 | 0.46 | 12.2% | 10.9% | 12.6% | 13.3%/10.6% | 5.9 (interpolated) | pass | 0.084 (unverified) | n/a |
| 55 | `cfg_3971` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 53/18/79 | 150 | 12.5% | 2.4% | 0.91 | -2.5% | 314 | 1.53 | 4.0% | 82.8 | 9/9 | 0.89 | 0.70 | 0.21 | 4 | 3.7% | 0.70 | 0.55 | 11.5% | 10.0% | 8.3% | 11.4%/8.3% | 6.5 (interpolated) | pass | 0.083 (unverified) | n/a |
| 56 | `cfg_6ff1` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 144/172/0 | 316 | 21.1% | 4.0% | 0.90 | -6.1% | 351 | 1.38 | 11.3% | 173.0 | 10/10 | 1.00 | 0.84 | 0.06 | 5 | 10.8% | 0.45 | 0.40 | 18.4% | 16.1% | 22.7% | 20.3%/18.1% | 5.1 (interpolated) | pass | 0.094 (unverified) | n/a |
| 57 | `cfg_cbe7` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 146/113/0 | 259 | 22.2% | 4.2% | 0.92 | -4.9% | 336 | 1.43 | 9.0% | 141.8 | 10/10 | 1.00 | 0.80 | 0.12 | 5 | 9.3% | 0.54 | 0.40 | 20.3% | 17.6% | 23.3% | 21.1%/18.0% | 6.1 (interpolated) | pass | 0.098 (unverified) | n/a |
| 58 | `cfg_fea1` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 143/56/0 | 199 | 20.9% | 3.9% | 0.96 | -5.9% | 362 | 1.52 | 8.3% | 109.5 | 10/10 | 1.00 | 0.87 | 0.09 | 5 | 13.4% | 0.36 | 0.39 | 19.0% | 16.7% | 17.1% | 19.3%/16.9% | 7.6 (interpolated) | pass | 0.115 (unverified) | n/a |
| 59 | `cfg_61f6` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 56/74/37 | 167 | 11.7% | 2.3% | 0.88 | -2.4% | 353 | 1.48 | 4.4% | 92.5 | 9/9 | 1.00 | 0.78 | 0.10 | 4 | 4.1% | 0.62 | 0.49 | 10.4% | 9.2% | 10.4% | 10.6%/7.9% | 5.8 (interpolated) | pass | 0.078 (unverified) | n/a |
| 60 | `cfg_3f8f` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=12, entry_z=-3.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 123/81/0 | 204 | 19.5% | 3.7% | 0.89 | -4.6% | 336 | 1.46 | 9.1% | 111.6 | 9/9 | 1.00 | 0.87 | 0.02 | 5 | 10.5% | 0.43 | 0.39 | 17.5% | 15.3% | 15.8% | 18.6%/14.9% | 6.8 (interpolated) | pass | 0.088 (unverified) | n/a |
| 61 | `cfg_f355` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=12, entry_z=-2.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 185/119/0 | 304 | 23.4% | 4.4% | 0.85 | -4.8% | 272 | 1.36 | 13.1% | 165.4 | 10/10 | 0.90 | 0.78 | 0.07 | 5 | 13.5% | 0.39 | 0.45 | 21.3% | 18.8% | 19.5% | 23.4%/19.5% | 5.9 (interpolated) | pass | 0.073 (unverified) | n/a |
| 62 | `cfg_87d8` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 99/79/37 | 215 | 16.1% | 3.1% | 0.92 | -3.4% | 205 | 1.48 | 5.7% | 118.0 | 11/11 | 1.00 | 0.78 | 0.14 | 5 | 10.0% | 0.35 | 0.50 | 14.7% | 12.7% | 15.1% | 15.8%/12.5% | 5.6 (interpolated) | pass | 0.091 (unverified) | n/a |
| 63 | `cfg_3f14` | timeframe=15min, mean_type=ema, mean_lookback=16, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 61/44/15 | 120 | 12.4% | 2.4% | 1.09 | -2.4% | 214 | 1.89 | 3.2% | 64.9 | 11/11 | 1.00 | 0.75 | 0.34 | 4 | 7.5% | 0.39 | 0.49 | 11.3% | 10.2% | 9.9% | 11.5%/9.7% | 7.6 (interpolated) | pass | 0.169 (unverified) | n/a |
| 64 | `cfg_ec81` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 63/11/76 | 150 | 13.0% | 2.5% | 0.99 | -2.4% | 275 | 1.57 | 3.7% | 82.7 | 10/10 | 1.00 | 0.81 | 0.18 | 4 | 4.8% | 0.62 | 0.51 | 11.8% | 10.4% | 7.4% | 12.1%/10.1% | 6.6 (interpolated) | pass | 0.117 (unverified) | n/a |
| 65 | `cfg_86d4` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=8, entry_z=-3.0, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 178/42/0 | 220 | 17.2% | 3.3% | 0.91 | -6.8% | 361 | 1.53 | 7.9% | 121.3 | 9/9 | 1.00 | 0.64 | 0.27 | 3 | 7.5% | 0.54 | 0.43 | 15.7% | 14.5% | 17.8% | 16.6%/14.6% | 5.9 (interpolated) | pass | 0.100 (unverified) | n/a |
| 66 | `cfg_ccc3` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=12, entry_z=-3.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 114/50/61 | 225 | 18.2% | 3.5% | 0.90 | -4.5% | 370 | 1.42 | 6.8% | 123.5 | 10/10 | 1.00 | 0.75 | 0.15 | 5 | 7.6% | 0.55 | 0.44 | 16.2% | 14.3% | 20.1% | 17.5%/14.7% | 5.9 (interpolated) | pass | 0.085 (unverified) | n/a |
| 67 | `cfg_6136` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 152/47/0 | 199 | 18.3% | 3.5% | 0.87 | -6.0% | 375 | 1.47 | 7.8% | 109.2 | 10/10 | 1.00 | 0.84 | 0.02 | 4 | 11.7% | 0.36 | 0.44 | 16.4% | 14.4% | 15.5% | 17.2%/14.2% | 6.8 (interpolated) | pass | 0.084 (unverified) | n/a |
| 68 | `cfg_b497` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 63/19/26 | 108 | 10.9% | 2.1% | 0.96 | -2.2% | 202 | 1.70 | 2.6% | 58.8 | 12/12 | 0.92 | 0.75 | 0.20 | 5 | 6.0% | 0.43 | 0.58 | 9.9% | 9.0% | 10.3% | 10.5%/8.6% | 7.6 (interpolated) | pass | 0.100 (unverified) | n/a |
| 69 | `cfg_2d4d` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 41/65/31 | 137 | 11.9% | 2.3% | 0.91 | -2.5% | 275 | 1.56 | 3.8% | 75.4 | 11/11 | 1.00 | 0.83 | 0.08 | 4 | 5.7% | 0.50 | 0.53 | 10.6% | 9.6% | 10.4% | 11.0%/8.9% | 6.9 (interpolated) | pass | 0.090 (unverified) | n/a |
| 70 | `cfg_9d13` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 79/157/105 | 341 | 23.3% | 4.3% | 0.96 | -5.6% | 519 | 1.35 | 10.7% | 186.8 | 11/11 | 0.91 | 0.80 | 0.16 | 3 | 4.9% | 0.74 | 0.44 | 19.9% | 16.3% | 30.9% | 23.1%/17.9% | 5.2 (interpolated) | pass | 0.117 (unverified) | n/a |
| 71 | `cfg_8389` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 50/78/0 | 128 | 14.0% | 2.7% | 1.05 | -1.7% | 133 | 1.74 | 3.9% | 70.8 | 11/11 | 1.00 | 0.85 | 0.20 | 5 | 7.9% | 0.42 | 0.46 | 12.9% | 11.6% | 10.3% | 13.0%/10.2% | 7.9 (interpolated) | pass | 0.158 (unverified) | n/a |
| 72 | `cfg_d210` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 172/29/88 | 289 | 20.8% | 3.9% | 0.88 | -4.9% | 375 | 1.35 | 9.2% | 158.3 | 10/10 | 1.00 | 0.88 | 0.01 | 5 | 7.4% | 0.61 | 0.43 | 18.4% | 14.9% | 19.6% | 19.9%/17.3% | 5.3 (interpolated) | pass | 0.083 (unverified) | n/a |
| 73 | `cfg_f2d9` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 158/120/0 | 278 | 19.7% | 3.7% | 0.94 | -6.1% | 310 | 1.43 | 9.9% | 152.0 | 10/10 | 0.80 | 0.76 | 0.18 | 5 | 13.7% | 0.29 | 0.35 | 17.0% | 15.2% | 21.5% | 19.6%/16.1% | 5.3 (interpolated) | pass | 0.112 (unverified) | n/a |
| 74 | `cfg_d82b` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 77/82/44 | 203 | 15.0% | 2.9% | 0.98 | -3.1% | 471 | 1.51 | 5.4% | 111.9 | 12/12 | 1.00 | 0.84 | 0.14 | 5 | 8.0% | 0.43 | 0.47 | 13.3% | 11.8% | 11.5% | 14.0%/11.6% | 5.9 (interpolated) | pass | 0.117 (unverified) | n/a |
| 75 | `cfg_368a` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 39/106/0 | 145 | 10.4% | 2.0% | 0.95 | -2.0% | 420 | 1.67 | 3.1% | 79.8 | 8/8 | 1.00 | 0.58 | 0.37 | 5 | 4.8% | 0.52 | 0.50 | 9.3% | 8.2% | 4.4% | 8.9%/6.9% | 5.6 (interpolated) | pass | 0.112 (unverified) | n/a |
| 76 | `cfg_3552` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=8, entry_z=-3.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 142/100/0 | 242 | 27.9% | 5.1% | 1.13 | -5.9% | 328 | 1.57 | 10.8% | 132.9 | 9/9 | 1.00 | 0.85 | 0.28 | 4 | 11.6% | 0.54 | 0.36 | 25.6% | 24.0% | 28.0% | 26.7%/21.7% | 7.7 (interpolated) | pass | 0.197 (unverified) | n/a |
| 77 | `cfg_6a1e` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=12, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 110/26/36 | 172 | 13.2% | 2.5% | 0.88 | -4.3% | 337 | 1.53 | 5.2% | 93.2 | 11/11 | 1.00 | 0.77 | 0.11 | 4 | 5.9% | 0.55 | 0.48 | 11.8% | 10.1% | 11.9% | 12.3%/10.5% | 5.7 (interpolated) | pass | 0.080 (unverified) | n/a |
| 78 | `cfg_b58e` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 158/107/0 | 265 | 22.4% | 4.2% | 0.85 | -5.6% | 378 | 1.38 | 11.7% | 144.3 | 9/9 | 1.00 | 0.85 | 0.00 | 5 | 15.0% | 0.30 | 0.46 | 20.4% | 18.5% | 17.5% | 21.1%/17.2% | 6.2 (interpolated) | pass | 0.073 (unverified) | n/a |
| 79 | `cfg_04e2` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-2.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 194/71/0 | 265 | 21.5% | 4.0% | 0.86 | -5.8% | 388 | 1.39 | 10.5% | 144.6 | 10/10 | 1.00 | 0.85 | 0.01 | 5 | 14.1% | 0.32 | 0.47 | 19.7% | 16.9% | 17.3% | 19.9%/16.9% | 6.1 (interpolated) | pass | 0.077 (unverified) | n/a |
| 80 | `cfg_459d` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 148/199/0 | 347 | 21.4% | 4.0% | 0.86 | -4.4% | 451 | 1.35 | 12.8% | 188.8 | 11/11 | 0.82 | 0.84 | 0.02 | 5 | 9.4% | 0.52 | 0.51 | 18.5% | 15.4% | 22.5% | 20.5%/16.6% | 4.6 (interpolated) | pass | 0.071 (unverified) | n/a |
| 81 | `cfg_042e` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=8, entry_z=-3.0, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 206/82/0 | 288 | 20.5% | 3.9% | 0.87 | -5.1% | 333 | 1.38 | 11.2% | 157.2 | 9/9 | 1.00 | 0.76 | 0.11 | 5 | 8.6% | 0.55 | 0.44 | 17.9% | 15.3% | 21.6% | 20.5%/16.4% | 5.3 (interpolated) | pass | 0.080 (unverified) | n/a |
| 82 | `cfg_66f0` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=8, entry_z=-3.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 185/29/135 | 349 | 21.7% | 4.1% | 0.94 | -5.1% | 409 | 1.31 | 10.3% | 191.5 | 9/9 | 1.00 | 0.67 | 0.27 | 4 | 11.2% | 0.46 | 0.43 | 18.9% | 15.8% | 24.4% | 21.3%/17.5% | 4.8 (interpolated) | pass | 0.100 (unverified) | n/a |
| 83 | `cfg_5689` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 212/92/0 | 304 | 26.4% | 4.9% | 0.95 | -5.0% | 273 | 1.42 | 12.5% | 166.4 | 9/9 | 0.89 | 0.83 | 0.13 | 5 | 15.5% | 0.38 | 0.43 | 22.9% | 20.6% | 22.4% | 26.4%/22.2% | 6.2 (interpolated) | pass | 0.107 (unverified) | n/a |
| 84 | `cfg_6b59` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 125/90/82 | 297 | 21.4% | 4.0% | 0.90 | -4.7% | 384 | 1.37 | 9.4% | 161.7 | 11/11 | 1.00 | 0.81 | 0.09 | 4 | 10.0% | 0.48 | 0.48 | 19.1% | 16.8% | 18.2% | 19.9%/15.8% | 5.4 (interpolated) | pass | 0.081 (unverified) | n/a |
| 85 | `cfg_fa7c` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 157/197/0 | 354 | 21.8% | 4.1% | 0.91 | -4.3% | 351 | 1.36 | 12.6% | 193.4 | 10/10 | 0.80 | 0.66 | 0.25 | 5 | 10.3% | 0.49 | 0.46 | 18.4% | 15.9% | 16.4% | 22.1%/18.2% | 4.7 (interpolated) | pass | 0.089 (unverified) | n/a |
| 86 | `cfg_205f` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 124/44/0 | 168 | 12.8% | 2.5% | 0.83 | -5.6% | 336 | 1.55 | 5.3% | 91.0 | 11/11 | 1.00 | 0.70 | 0.13 | 4 | 5.0% | 0.61 | 0.50 | 11.5% | 10.3% | 10.3% | 12.0%/9.9% | 5.5 (interpolated) | pass | 0.070 (unverified) | n/a |
| 87 | `cfg_5722` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 87/30/31 | 148 | 13.9% | 2.7% | 0.92 | -3.4% | 299 | 1.58 | 4.1% | 81.6 | 11/11 | 1.00 | 0.77 | 0.14 | 5 | 7.4% | 0.45 | 0.53 | 12.3% | 11.3% | 13.8% | 12.8%/10.2% | 6.8 (interpolated) | pass | 0.094 (unverified) | n/a |
| 88 | `cfg_82d8` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-3.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 125/99/78 | 302 | 17.0% | 3.2% | 0.80 | -6.4% | 453 | 1.30 | 9.1% | 165.7 | 10/10 | 1.00 | 0.76 | 0.05 | 3 | 5.8% | 0.62 | 0.49 | 15.1% | 12.6% | 23.2% | 18.2%/15.3% | 4.5 (interpolated) | pass | 0.059 (unverified) | n/a |
| 89 | `cfg_2c70` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 74/5/28 | 107 | 10.7% | 2.1% | 0.94 | -2.2% | 202 | 1.69 | 2.8% | 58.2 | 11/11 | 0.91 | 0.72 | 0.22 | 5 | 6.4% | 0.39 | 0.59 | 9.8% | 8.9% | 9.6% | 10.3%/8.3% | 7.6 (interpolated) | pass | 0.096 (unverified) | n/a |
| 90 | `cfg_c3c1` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 78/36/34 | 148 | 13.4% | 2.6% | 0.87 | -3.4% | 299 | 1.53 | 4.4% | 81.5 | 12/12 | 1.00 | 0.82 | 0.05 | 5 | 8.6% | 0.34 | 0.55 | 12.4% | 11.8% | 13.3% | 13.1%/11.0% | 6.8 (interpolated) | pass | 0.078 (unverified) | n/a |
| 91 | `cfg_dfdf` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 93/9/25 | 127 | 10.7% | 2.1% | 0.86 | -3.7% | 248 | 1.61 | 3.4% | 68.8 | 10/10 | 1.00 | 0.69 | 0.17 | 4 | 6.1% | 0.42 | 0.54 | 9.7% | 8.7% | 9.3% | 10.2%/8.4% | 6.6 (interpolated) | pass | 0.079 (unverified) | n/a |
| 92 | `cfg_044f` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 123/224/0 | 347 | 22.0% | 4.1% | 0.87 | -4.5% | 453 | 1.35 | 13.2% | 189.2 | 10/10 | 0.80 | 0.83 | 0.04 | 5 | 9.6% | 0.52 | 0.49 | 18.6% | 16.3% | 21.9% | 21.2%/18.5% | 4.7 (interpolated) | pass | 0.073 (unverified) | n/a |
| 93 | `cfg_e63e` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 161/64/72 | 297 | 22.5% | 4.2% | 0.99 | -3.8% | 339 | 1.41 | 8.7% | 161.7 | 12/12 | 1.00 | 0.84 | 0.15 | 4 | 9.9% | 0.51 | 0.44 | 19.9% | 17.9% | 18.1% | 22.0%/18.1% | 5.6 (interpolated) | pass | 0.122 (unverified) | n/a |
| 94 | `cfg_4d9d` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 138/104/77 | 319 | 22.2% | 4.2% | 1.00 | -4.8% | 453 | 1.37 | 9.9% | 173.6 | 12/12 | 1.00 | 0.83 | 0.16 | 5 | 10.6% | 0.48 | 0.40 | 19.3% | 17.0% | 26.8% | 21.2%/18.9% | 5.3 (interpolated) | pass | 0.126 (unverified) | n/a |
| 95 | `cfg_4cd3` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=15, entry_z=-2.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 67/61/0 | 128 | 12.8% | 2.5% | 1.00 | -1.7% | 200 | 1.71 | 3.7% | 70.6 | 11/11 | 1.00 | 0.82 | 0.18 | 5 | 6.2% | 0.50 | 0.48 | 11.6% | 10.6% | 9.1% | 11.7%/9.8% | 7.4 (interpolated) | pass | 0.138 (unverified) | n/a |
| 96 | `cfg_d4b1` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 142/44/124 | 310 | 23.2% | 4.3% | 0.97 | -4.9% | 399 | 1.36 | 9.5% | 170.1 | 11/11 | 1.00 | 0.64 | 0.34 | 4 | 9.7% | 0.55 | 0.41 | 19.8% | 17.0% | 21.8% | 22.9%/18.8% | 5.3 (interpolated) | pass | 0.112 (unverified) | n/a |
| 97 | `cfg_1bbc` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=8, entry_z=-3.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 163/44/139 | 346 | 22.9% | 4.3% | 0.94 | -5.1% | 419 | 1.32 | 11.1% | 190.6 | 10/10 | 0.90 | 0.78 | 0.16 | 4 | 11.8% | 0.46 | 0.46 | 20.0% | 16.8% | 24.3% | 21.5%/18.5% | 4.9 (interpolated) | pass | 0.097 (unverified) | n/a |
| 98 | `cfg_e101` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 33/111/0 | 144 | 10.1% | 2.0% | 0.92 | -2.2% | 533 | 1.64 | 3.1% | 79.1 | 9/9 | 1.00 | 0.72 | 0.20 | 4 | 4.5% | 0.54 | 0.52 | 9.0% | 8.0% | 4.3% | 9.0%/7.2% | 5.6 (interpolated) | pass | 0.101 (unverified) | n/a |
| 99 | `cfg_1817` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=12, entry_z=-3.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 60/24/20 | 104 | 10.5% | 2.1% | 0.89 | -3.4% | 340 | 1.68 | 3.0% | 57.6 | 10/10 | 1.00 | 0.80 | 0.09 | 5 | 6.6% | 0.36 | 0.61 | 9.6% | 9.0% | 11.1% | 10.2%/8.5% | 7.7 (interpolated) | pass | 0.086 (unverified) | n/a |
| 100 | `cfg_2894` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 143/53/92 | 288 | 20.9% | 3.9% | 0.89 | -5.2% | 408 | 1.33 | 9.7% | 157.3 | 11/11 | 0.91 | 0.71 | 0.19 | 4 | 8.1% | 0.58 | 0.43 | 18.3% | 14.8% | 26.7% | 20.5%/15.8% | 5.3 (interpolated) | pass | 0.081 (unverified) | n/a |
| 101 | `cfg_0976` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 97/62/55 | 214 | 15.5% | 3.0% | 0.81 | -5.2% | 375 | 1.38 | 7.0% | 117.7 | 11/11 | 1.00 | 0.77 | 0.03 | 5 | 11.6% | 0.25 | 0.49 | 14.0% | 12.4% | 15.0% | 15.0%/12.6% | 5.7 (interpolated) | pass | 0.059 (unverified) | n/a |
| 102 | `cfg_6718` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-3.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 83/144/0 | 227 | 20.3% | 3.8% | 0.93 | -7.6% | 351 | 1.45 | 8.5% | 124.1 | 9/9 | 1.00 | 0.82 | 0.10 | 5 | 12.1% | 0.39 | 0.45 | 18.9% | 16.9% | 15.4% | 19.9%/16.9% | 6.6 (interpolated) | pass | 0.102 (unverified) | n/a |
| 103 | `cfg_eb02` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 179/50/68 | 297 | 21.3% | 4.0% | 0.96 | -4.5% | 337 | 1.41 | 8.2% | 161.8 | 11/11 | 1.00 | 0.82 | 0.14 | 5 | 9.3% | 0.53 | 0.49 | 19.2% | 16.2% | 16.3% | 20.7%/17.1% | 5.4 (interpolated) | pass | 0.106 (unverified) | n/a |
| 104 | `cfg_3edb` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 135/45/0 | 180 | 16.0% | 3.1% | 0.93 | -6.6% | 388 | 1.57 | 6.9% | 99.1 | 10/10 | 1.00 | 0.66 | 0.26 | 4 | 9.4% | 0.40 | 0.48 | 14.6% | 13.0% | 14.7% | 15.7%/13.6% | 6.8 (interpolated) | pass | 0.104 (unverified) | n/a |
| 105 | `cfg_e045` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 144/64/77 | 285 | 21.5% | 4.0% | 0.93 | -4.2% | 337 | 1.39 | 8.4% | 156.4 | 11/11 | 1.00 | 0.77 | 0.16 | 4 | 8.6% | 0.56 | 0.41 | 18.8% | 15.6% | 20.3% | 19.2%/16.0% | 5.5 (interpolated) | pass | 0.100 (unverified) | n/a |
| 106 | `cfg_0c93` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=8, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 180/29/140 | 349 | 22.0% | 4.1% | 0.94 | -5.6% | 424 | 1.32 | 10.3% | 190.6 | 11/11 | 1.00 | 0.71 | 0.23 | 4 | 8.5% | 0.59 | 0.44 | 18.7% | 15.4% | 21.7% | 20.9%/17.4% | 4.7 (interpolated) | pass | 0.098 (unverified) | n/a |
| 107 | `cfg_3141` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=8, entry_z=-3.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 208/34/106 | 348 | 22.1% | 4.1% | 0.91 | -5.4% | 385 | 1.31 | 11.9% | 190.6 | 10/10 | 1.00 | 0.70 | 0.20 | 5 | 7.9% | 0.61 | 0.43 | 18.6% | 15.1% | 18.8% | 21.8%/17.1% | 4.7 (interpolated) | pass | 0.089 (unverified) | n/a |
| 108 | `cfg_ae53` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 183/160/0 | 343 | 23.8% | 4.4% | 0.83 | -5.2% | 310 | 1.31 | 16.0% | 187.5 | 10/10 | 0.90 | 0.80 | 0.03 | 5 | 16.8% | 0.28 | 0.44 | 22.2% | 18.0% | 18.5% | 24.5%/21.0% | 5.4 (interpolated) | pass | 0.064 (unverified) | n/a |
| 109 | `cfg_311a` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 101/61/43 | 205 | 14.0% | 2.7% | 0.93 | -3.0% | 476 | 1.48 | 5.1% | 113.1 | 11/11 | 1.00 | 0.68 | 0.25 | 5 | 7.1% | 0.47 | 0.50 | 12.1% | 10.8% | 10.8% | 12.7%/10.2% | 5.4 (interpolated) | pass | 0.096 (unverified) | n/a |
| 110 | `cfg_a1e6` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 99/50/71 | 220 | 13.7% | 2.6% | 0.92 | -2.7% | 477 | 1.44 | 5.0% | 121.7 | 11/11 | 1.00 | 0.63 | 0.29 | 5 | 7.0% | 0.46 | 0.51 | 11.8% | 10.4% | 8.9% | 13.2%/10.0% | 4.9 (interpolated) | pass | 0.090 (unverified) | n/a |
| 111 | `cfg_bc43` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=8, entry_z=-3.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 126/136/0 | 262 | 20.3% | 3.8% | 1.02 | -4.3% | 345 | 1.50 | 9.5% | 144.1 | 9/9 | 0.89 | 0.67 | 0.35 | 3 | 7.1% | 0.61 | 0.43 | 17.3% | 14.9% | 15.5% | 19.1%/15.6% | 5.5 (interpolated) | pass | 0.138 (unverified) | n/a |
| 112 | `cfg_351f` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 76/106/0 | 182 | 14.5% | 2.8% | 0.91 | -2.5% | 121 | 1.51 | 5.4% | 100.9 | 11/11 | 1.00 | 0.80 | 0.11 | 5 | 8.3% | 0.40 | 0.48 | 13.1% | 11.6% | 13.4% | 13.9%/11.0% | 6.1 (interpolated) | pass | 0.094 (unverified) | n/a |
| 113 | `cfg_d52d` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=12, entry_z=-3.0, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 59/37/14 | 110 | 8.8% | 1.7% | 0.83 | -2.9% | 453 | 1.64 | 3.1% | 59.4 | 11/11 | 1.00 | 0.57 | 0.25 | 4 | 4.8% | 0.45 | 0.61 | 8.0% | 7.1% | 7.3% | 8.1%/6.2% | 5.9 (interpolated) | pass | 0.066 (unverified) | n/a |
| 114 | `cfg_fa55` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 214/42/111 | 367 | 23.5% | 4.4% | 0.91 | -4.4% | 351 | 1.31 | 12.0% | 199.6 | 10/10 | 1.00 | 0.78 | 0.12 | 4 | 5.2% | 0.73 | 0.47 | 20.5% | 18.0% | 26.5% | 23.3%/21.1% | 5.0 (interpolated) | pass | 0.086 (unverified) | n/a |
| 115 | `cfg_f78e` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 25/71/57 | 153 | 9.0% | 1.8% | 0.85 | -1.9% | 166 | 1.53 | 2.7% | 84.2 | 9/9 | 1.00 | 0.78 | 0.07 | 5 | 4.1% | 0.54 | 0.68 | 7.7% | 6.4% | 8.1% | 8.5%/6.1% | 5.0 (interpolated) | pass | 0.063 (unverified) | n/a |
| 116 | `cfg_cd03` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=12, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 74/16/20 | 110 | 8.5% | 1.7% | 0.77 | -2.7% | 336 | 1.60 | 3.3% | 59.5 | 11/11 | 1.00 | 0.59 | 0.18 | 4 | 3.8% | 0.55 | 0.59 | 7.5% | 6.6% | 6.3% | 7.8%/6.3% | 5.6 (interpolated) | pass | 0.053 (unverified) | n/a |
| 117 | `cfg_dc2a` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=18, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 55/14/55 | 124 | 8.1% | 1.6% | 0.87 | -2.2% | 349 | 1.61 | 2.2% | 67.4 | 9/9 | 1.00 | 0.77 | 0.10 | 4 | 3.5% | 0.55 | 0.62 | 7.0% | 6.2% | 6.2% | 7.2%/4.8% | 5.6 (interpolated) | pass | 0.063 (unverified) | n/a |
| 118 | `cfg_cc6e` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=18, entry_z=-3.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 46/22/56 | 124 | 8.1% | 1.6% | 0.86 | -2.1% | 349 | 1.60 | 2.4% | 67.4 | 10/10 | 1.00 | 0.76 | 0.10 | 4 | 3.6% | 0.54 | 0.63 | 7.1% | 6.3% | 6.7% | 7.2%/6.1% | 5.6 (interpolated) | pass | 0.061 (unverified) | n/a |
| 119 | `cfg_3e75` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 120/31/62 | 213 | 16.2% | 3.1% | 0.82 | -5.8% | 385 | 1.37 | 7.7% | 117.0 | 10/10 | 1.00 | 0.74 | 0.08 | 5 | 12.4% | 0.23 | 0.47 | 14.1% | 12.5% | 12.6% | 15.3%/12.3% | 5.8 (interpolated) | pass | 0.062 (unverified) | n/a |
| 120 | `cfg_d4f2` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=15, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 25/89/32 | 146 | 9.7% | 1.9% | 0.88 | -2.2% | 166 | 1.58 | 2.9% | 80.6 | 10/10 | 1.00 | 0.80 | 0.08 | 5 | 5.4% | 0.43 | 0.66 | 8.8% | 7.4% | 10.1% | 9.4%/7.4% | 5.5 (interpolated) | pass | 0.077 (unverified) | n/a |
| 121 | `cfg_04bd` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=8, entry_z=-3.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 222/49/129 | 400 | 21.9% | 4.1% | 0.86 | -5.4% | 525 | 1.27 | 13.6% | 217.8 | 9/9 | 0.89 | 0.72 | 0.14 | 4 | 7.0% | 0.63 | 0.44 | 17.9% | 14.4% | 20.7% | 20.9%/15.9% | 4.3 (interpolated) | pass | 0.074 (unverified) | n/a |
| 122 | `cfg_b669` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 57/92/0 | 149 | 11.6% | 2.2% | 0.83 | -3.4% | 475 | 1.51 | 4.4% | 82.4 | 8/8 | 1.00 | 0.73 | 0.10 | 4 | 3.2% | 0.70 | 0.50 | 10.6% | 9.1% | 8.6% | 10.7%/8.8% | 6.2 (interpolated) | pass | 0.069 (unverified) | n/a |
| 123 | `cfg_f3df` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 121/59/0 | 180 | 18.4% | 3.5% | 0.97 | -6.8% | 388 | 1.55 | 7.4% | 98.1 | 10/10 | 1.00 | 0.73 | 0.24 | 5 | 10.9% | 0.40 | 0.46 | 16.1% | 14.5% | 16.5% | 17.3%/14.8% | 7.2 (interpolated) | pass | 0.119 (unverified) | n/a |
| 124 | `cfg_4405` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-3.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 98/86/59 | 243 | 20.4% | 3.9% | 0.99 | -4.9% | 351 | 1.44 | 7.6% | 132.7 | 11/11 | 0.91 | 0.78 | 0.21 | 5 | 10.8% | 0.45 | 0.46 | 18.6% | 16.6% | 17.5% | 20.2%/16.9% | 6.1 (interpolated) | pass | 0.117 (unverified) | n/a |
| 125 | `cfg_1def` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=8, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 184/40/103 | 327 | 20.6% | 3.9% | 0.86 | -4.8% | 419 | 1.30 | 10.6% | 178.6 | 11/11 | 1.00 | 0.74 | 0.13 | 5 | 8.1% | 0.58 | 0.47 | 18.2% | 14.8% | 22.7% | 21.0%/17.1% | 4.8 (interpolated) | pass | 0.072 (unverified) | n/a |
| 126 | `cfg_dc6e` | timeframe=15min, mean_type=ema, mean_lookback=16, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 75/22/21 | 118 | 11.5% | 2.2% | 0.98 | -2.6% | 326 | 1.75 | 3.4% | 63.9 | 11/11 | 1.00 | 0.61 | 0.37 | 4 | 6.8% | 0.41 | 0.52 | 10.1% | 9.2% | 9.9% | 10.6%/9.1% | 7.1 (interpolated) | pass | 0.119 (unverified) | n/a |
| 127 | `cfg_7c6c` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=12, entry_z=-3.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 55/28/21 | 104 | 10.7% | 2.1% | 0.89 | -3.5% | 311 | 1.67 | 3.2% | 57.3 | 11/11 | 1.00 | 0.80 | 0.09 | 5 | 7.5% | 0.30 | 0.60 | 10.0% | 8.7% | 10.8% | 9.9%/7.9% | 7.6 (interpolated) | pass | 0.083 (unverified) | n/a |
| 128 | `cfg_fad7` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 65/183/96 | 344 | 25.1% | 4.7% | 1.01 | -4.4% | 520 | 1.39 | 9.5% | 188.9 | 11/11 | 0.91 | 0.48 | 0.53 | 3 | 9.0% | 0.58 | 0.42 | 21.4% | 18.7% | 30.8% | 24.2%/18.8% | 5.3 (interpolated) | pass | 0.128 (unverified) | n/a |
| 129 | `cfg_9365` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=18, entry_z=-3.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 44/105/0 | 149 | 11.4% | 2.2% | 0.81 | -3.7% | 487 | 1.50 | 4.6% | 82.3 | 9/9 | 1.00 | 0.76 | 0.06 | 3 | 2.7% | 0.73 | 0.50 | 9.8% | 8.8% | 7.9% | 10.4%/7.6% | 5.8 (interpolated) | pass | 0.063 (unverified) | n/a |
| 130 | `cfg_6484` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 99/106/0 | 205 | 15.2% | 2.9% | 0.83 | -3.6% | 375 | 1.46 | 6.0% | 112.2 | 10/10 | 1.00 | 0.79 | 0.04 | 5 | 8.6% | 0.42 | 0.53 | 13.4% | 12.0% | 14.5% | 14.8%/12.2% | 5.7 (interpolated) | pass | 0.067 (unverified) | n/a |
| 131 | `cfg_f0e4` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 199/15/81 | 295 | 19.2% | 3.6% | 0.90 | -7.4% | 388 | 1.34 | 9.5% | 161.6 | 10/10 | 0.80 | 0.67 | 0.23 | 5 | 12.5% | 0.33 | 0.41 | 16.6% | 14.1% | 20.4% | 18.1%/14.7% | 5.0 (interpolated) | pass | 0.091 (unverified) | n/a |
| 132 | `cfg_956f` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 82/36/53 | 171 | 9.2% | 1.8% | 0.96 | -1.4% | 239 | 1.58 | 2.7% | 93.7 | 8/8 | 1.00 | 0.62 | 0.35 | 5 | 3.1% | 0.65 | 0.63 | 7.7% | 6.3% | 5.6% | 8.7%/6.9% | 4.6 (interpolated) | pass | 0.099 (unverified) | n/a |
| 133 | `cfg_c8fc` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 75/101/57 | 233 | 15.1% | 2.9% | 0.90 | -3.2% | 244 | 1.40 | 6.3% | 127.9 | 9/9 | 1.00 | 0.75 | 0.15 | 4 | 7.6% | 0.47 | 0.46 | 13.1% | 10.9% | 15.5% | 14.1%/11.1% | 5.1 (interpolated) | pass | 0.087 (unverified) | n/a |
| 134 | `cfg_d01f` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 202/14/80 | 296 | 18.7% | 3.6% | 0.84 | -6.4% | 388 | 1.34 | 8.7% | 161.2 | 10/10 | 1.00 | 0.77 | 0.07 | 4 | 6.8% | 0.61 | 0.56 | 16.8% | 13.5% | 15.9% | 17.5%/14.5% | 4.9 (interpolated) | pass | 0.065 (unverified) | n/a |
| 135 | `cfg_f638` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 66/91/46 | 203 | 14.4% | 2.8% | 0.93 | -3.3% | 464 | 1.48 | 5.5% | 111.9 | 12/12 | 1.00 | 0.75 | 0.19 | 5 | 7.5% | 0.45 | 0.48 | 12.7% | 11.2% | 10.1% | 13.6%/11.0% | 5.7 (interpolated) | pass | 0.098 (unverified) | n/a |
| 136 | `cfg_2467` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 70/30/28 | 128 | 10.9% | 2.1% | 0.78 | -3.4% | 332 | 1.51 | 3.8% | 70.8 | 12/12 | 1.00 | 0.71 | 0.06 | 5 | 7.1% | 0.34 | 0.59 | 10.1% | 9.1% | 9.7% | 10.3%/8.4% | 6.4 (interpolated) | pass | 0.055 (unverified) | n/a |
| 137 | `cfg_a10d` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 60/62/29 | 151 | 11.6% | 2.3% | 0.80 | -2.8% | 299 | 1.47 | 4.0% | 82.2 | 12/12 | 1.00 | 0.76 | 0.04 | 5 | 7.1% | 0.37 | 0.63 | 9.9% | 8.7% | 13.5% | 11.1%/8.1% | 5.5 (interpolated) | pass | 0.058 (unverified) | n/a |
| 138 | `cfg_ef4c` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 92/145/64 | 301 | 17.5% | 3.3% | 0.82 | -5.1% | 347 | 1.34 | 8.3% | 165.7 | 12/12 | 0.92 | 0.66 | 0.16 | 4 | 6.7% | 0.57 | 0.57 | 15.5% | 13.3% | 17.5% | 16.8%/13.4% | 4.5 (interpolated) | pass | 0.059 (unverified) | n/a |
| 139 | `cfg_bd6c` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 109/244/0 | 353 | 21.6% | 4.1% | 0.89 | -4.5% | 208 | 1.34 | 13.3% | 193.3 | 11/11 | 0.82 | 0.74 | 0.15 | 5 | 13.4% | 0.38 | 0.44 | 18.1% | 16.1% | 16.5% | 21.2%/17.9% | 4.7 (interpolated) | pass | 0.083 (unverified) | n/a |
| 140 | `cfg_eea6` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-2.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 116/124/61 | 301 | 17.6% | 3.4% | 0.84 | -5.1% | 342 | 1.35 | 8.1% | 165.4 | 12/12 | 0.92 | 0.71 | 0.13 | 4 | 7.1% | 0.55 | 0.57 | 15.4% | 13.5% | 17.2% | 17.0%/13.2% | 4.5 (interpolated) | pass | 0.064 (unverified) | n/a |
| 141 | `cfg_9cb0` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 115/37/69 | 221 | 16.5% | 3.1% | 0.82 | -5.0% | 439 | 1.37 | 7.4% | 121.7 | 11/11 | 1.00 | 0.81 | 0.02 | 4 | 9.3% | 0.40 | 0.49 | 15.1% | 13.1% | 16.4% | 15.6%/13.0% | 5.9 (interpolated) | pass | 0.065 (unverified) | n/a |
| 142 | `cfg_464b` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 84/121/0 | 205 | 16.4% | 3.1% | 0.87 | -3.5% | 333 | 1.48 | 6.2% | 112.3 | 11/11 | 1.00 | 0.80 | 0.07 | 5 | 9.8% | 0.37 | 0.49 | 14.7% | 13.1% | 14.4% | 15.3%/12.5% | 6.0 (interpolated) | pass | 0.079 (unverified) | n/a |
| 143 | `cfg_d3d1` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 247/50/141 | 438 | 20.5% | 3.9% | 0.76 | -6.0% | 351 | 1.22 | 14.8% | 239.2 | 10/10 | 1.00 | 0.68 | 0.09 | 4 | 5.3% | 0.70 | 0.48 | 15.9% | 11.6% | 19.6% | 20.3%/16.3% | 3.8 (interpolated) | pass | 0.048 (unverified) | n/a |
| 144 | `cfg_d787` | timeframe=15min, mean_type=ema, mean_lookback=16, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 68/9/54 | 131 | 9.5% | 1.9% | 0.87 | -2.6% | 357 | 1.57 | 2.9% | 71.2 | 10/10 | 1.00 | 0.48 | 0.39 | 4 | 4.9% | 0.46 | 0.61 | 8.4% | 7.3% | 12.2% | 8.8%/7.1% | 5.8 (interpolated) | pass | 0.074 (unverified) | n/a |
| 145 | `cfg_551a` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 111/33/94 | 238 | 17.6% | 3.3% | 0.88 | -4.1% | 366 | 1.37 | 7.2% | 130.3 | 11/11 | 1.00 | 0.73 | 0.14 | 4 | 8.0% | 0.51 | 0.46 | 15.6% | 13.4% | 14.6% | 16.9%/14.0% | 5.7 (interpolated) | pass | 0.080 (unverified) | n/a |
| 146 | `cfg_80eb` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-3.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 29/31/41 | 101 | 8.8% | 1.7% | 0.83 | -2.3% | 422 | 1.61 | 3.5% | 55.5 | 9/9 | 1.00 | 0.68 | 0.15 | 4 | 3.5% | 0.58 | 0.68 | 8.0% | 7.3% | 6.2% | 8.2%/6.1% | 6.8 (interpolated) | pass | 0.055 (unverified) | n/a |
| 147 | `cfg_ecc1` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=18, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 48/79/38 | 165 | 11.6% | 2.3% | 0.85 | -2.9% | 422 | 1.49 | 4.3% | 90.6 | 8/8 | 0.88 | 0.75 | 0.10 | 4 | 5.1% | 0.54 | 0.48 | 10.5% | 9.2% | 8.7% | 10.2%/7.7% | 5.5 (interpolated) | pass | 0.070 (unverified) | n/a |
| 148 | `cfg_7864` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=8, entry_z=-3.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 101/145/81 | 327 | 20.1% | 3.8% | 0.91 | -5.0% | 496 | 1.35 | 10.4% | 179.5 | 11/11 | 0.82 | 0.72 | 0.19 | 4 | 8.3% | 0.55 | 0.46 | 17.4% | 14.2% | 16.0% | 20.2%/14.9% | 4.7 (interpolated) | pass | 0.088 (unverified) | n/a |
| 149 | `cfg_fb50` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=18, entry_z=-3.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 34/71/59 | 164 | 12.4% | 2.4% | 0.78 | -5.5% | 440 | 1.39 | 6.5% | 90.6 | 7/7 | 0.86 | 0.68 | 0.10 | 3 | 2.9% | 0.75 | 0.57 | 11.2% | 9.9% | 13.4% | 11.1%/8.6% | 6.1 (interpolated) | pass | 0.046 (unverified) | n/a |
| 150 | `cfg_11f9` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 172/145/0 | 317 | 20.1% | 3.8% | 0.78 | -4.3% | 356 | 1.33 | 11.0% | 173.3 | 10/10 | 1.00 | 0.81 | -0.03 | 5 | 8.0% | 0.56 | 0.52 | 17.5% | 15.2% | 17.9% | 20.5%/17.9% | 5.0 (interpolated) | pass | 0.053 (unverified) | n/a |
| 151 | `cfg_7be2` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 52/54/22 | 128 | 10.4% | 2.0% | 0.77 | -2.6% | 181 | 1.50 | 3.4% | 70.4 | 12/12 | 1.00 | 0.64 | 0.13 | 5 | 6.8% | 0.34 | 0.62 | 9.4% | 8.1% | 11.1% | 10.1%/7.3% | 5.9 (interpolated) | pass | 0.052 (unverified) | n/a |
| 152 | `cfg_8eb8` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 72/52/27 | 151 | 10.9% | 2.1% | 0.77 | -2.7% | 299 | 1.46 | 3.9% | 82.8 | 11/11 | 1.00 | 0.74 | 0.03 | 5 | 5.3% | 0.50 | 0.67 | 9.1% | 8.1% | 13.3% | 10.5%/7.3% | 5.4 (interpolated) | pass | 0.050 (unverified) | n/a |
| 153 | `cfg_c094` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=12, entry_z=-2.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 155/111/94 | 360 | 20.2% | 3.8% | 0.81 | -5.3% | 495 | 1.29 | 11.2% | 197.1 | 12/12 | 0.92 | 0.66 | 0.15 | 3 | 4.9% | 0.71 | 0.52 | 17.3% | 14.6% | 21.2% | 20.3%/16.5% | 4.5 (interpolated) | pass | 0.056 (unverified) | n/a |
| 154 | `cfg_227b` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 215/56/0 | 271 | 17.2% | 3.3% | 0.81 | -9.1% | 388 | 1.36 | 10.2% | 149.0 | 10/10 | 0.70 | 0.75 | 0.06 | 5 | 11.7% | 0.32 | 0.42 | 15.1% | 13.6% | 15.3% | 16.5%/13.8% | 5.0 (interpolated) | pass | 0.067 (unverified) | n/a |
| 155 | `cfg_1bb8` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 100/80/0 | 180 | 16.9% | 3.2% | 0.86 | -7.6% | 388 | 1.46 | 8.0% | 98.6 | 9/9 | 0.89 | 0.63 | 0.23 | 5 | 9.5% | 0.43 | 0.46 | 15.2% | 13.4% | 14.7% | 16.4%/12.9% | 7.0 (interpolated) | pass | 0.078 (unverified) | n/a |
| 156 | `cfg_ecb0` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-3.5, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 21/39/41 | 101 | 8.7% | 1.7% | 0.82 | -2.6% | 455 | 1.60 | 3.8% | 55.5 | 8/8 | 1.00 | 0.66 | 0.16 | 4 | 3.4% | 0.60 | 0.68 | 7.9% | 7.1% | 5.6% | 7.9%/6.1% | 6.7 (interpolated) | pass | 0.052 (unverified) | n/a |
| 157 | `cfg_96cc` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=8, entry_z=-3.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 123/124/80 | 327 | 19.7% | 3.7% | 0.88 | -4.1% | 496 | 1.34 | 10.0% | 178.9 | 11/11 | 0.82 | 0.76 | 0.12 | 5 | 7.0% | 0.61 | 0.51 | 16.4% | 13.6% | 16.0% | 19.0%/15.5% | 4.5 (interpolated) | pass | 0.077 (unverified) | n/a |
| 158 | `cfg_dd3a` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 110/43/68 | 221 | 16.4% | 3.1% | 0.79 | -5.0% | 437 | 1.36 | 7.7% | 120.6 | 11/11 | 1.00 | 0.76 | 0.04 | 4 | 6.3% | 0.59 | 0.55 | 14.3% | 12.6% | 14.9% | 15.9%/12.9% | 5.5 (interpolated) | pass | 0.052 (unverified) | n/a |
| 159 | `cfg_50f4` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=8, entry_z=-3.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 125/188/0 | 313 | 17.7% | 3.4% | 0.81 | -5.7% | 461 | 1.33 | 11.5% | 172.2 | 10/10 | 1.00 | 0.66 | 0.14 | 3 | 4.2% | 0.70 | 0.48 | 14.9% | 12.3% | 11.5% | 16.8%/13.4% | 4.6 (interpolated) | pass | 0.059 (unverified) | n/a |
| 160 | `cfg_49ff` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 150/31/0 | 181 | 12.8% | 2.5% | 0.75 | -6.4% | 388 | 1.45 | 6.3% | 99.4 | 9/9 | 0.89 | 0.66 | 0.10 | 4 | 7.7% | 0.39 | 0.60 | 11.2% | 10.6% | 12.4% | 12.8%/11.2% | 5.6 (interpolated) | pass | 0.051 (unverified) | n/a |
| 161 | `cfg_769d` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=15, entry_z=-2.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 31/83/56 | 170 | 9.3% | 1.8% | 0.93 | -1.3% | 214 | 1.55 | 3.1% | 93.0 | 8/8 | 1.00 | 0.61 | 0.32 | 5 | 4.0% | 0.55 | 0.63 | 7.7% | 6.7% | 7.3% | 8.7%/6.6% | 4.6 (interpolated) | pass | 0.085 (unverified) | n/a |
| 162 | `cfg_90db` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 155/133/0 | 288 | 24.6% | 4.6% | 0.94 | -5.4% | 336 | 1.41 | 12.6% | 157.3 | 9/9 | 0.89 | 0.57 | 0.37 | 5 | 12.5% | 0.45 | 0.41 | 20.5% | 17.3% | 20.0% | 23.5%/17.5% | 6.0 (interpolated) | pass | 0.099 (unverified) | n/a |
| 163 | `cfg_0a29` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-3.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 53/122/58 | 233 | 15.1% | 2.9% | 0.88 | -3.1% | 242 | 1.39 | 6.5% | 127.9 | 10/10 | 1.00 | 0.74 | 0.15 | 4 | 7.6% | 0.47 | 0.46 | 13.1% | 11.2% | 16.5% | 14.6%/11.2% | 5.1 (interpolated) | pass | 0.081 (unverified) | n/a |
| 164 | `cfg_d88c` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 98/195/0 | 293 | 24.1% | 4.5% | 0.96 | -4.5% | 515 | 1.42 | 9.1% | 160.3 | 9/9 | 0.78 | 0.46 | 0.51 | 4 | 9.1% | 0.57 | 0.39 | 21.9% | 18.8% | 26.7% | 23.9%/19.7% | 5.9 (interpolated) | pass | 0.113 (unverified) | n/a |
| 165 | `cfg_8206` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=12, entry_z=-2.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 129/64/0 | 193 | 15.9% | 3.0% | 0.77 | -4.6% | 374 | 1.41 | 7.7% | 106.2 | 10/10 | 1.00 | 0.62 | 0.15 | 5 | 7.6% | 0.50 | 0.51 | 13.5% | 12.0% | 15.2% | 15.3%/12.2% | 6.1 (interpolated) | pass | 0.055 (unverified) | n/a |
| 166 | `cfg_e1b8` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=10, entry_z=-3.0, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 84/82/53 | 219 | 15.3% | 2.9% | 0.79 | -4.6% | 351 | 1.38 | 6.7% | 119.6 | 12/12 | 1.00 | 0.71 | 0.07 | 4 | 6.0% | 0.59 | 0.59 | 13.6% | 12.1% | 14.9% | 15.2%/12.3% | 5.3 (interpolated) | pass | 0.051 (unverified) | n/a |
| 167 | `cfg_0e45` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=18, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 47/189/0 | 236 | 15.2% | 2.9% | 0.82 | -4.8% | 197 | 1.39 | 7.5% | 128.9 | 9/9 | 1.00 | 0.69 | 0.14 | 4 | 5.2% | 0.63 | 0.46 | 13.2% | 10.8% | 12.5% | 13.2%/9.6% | 4.9 (interpolated) | pass | 0.065 (unverified) | n/a |
| 168 | `cfg_0a93` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=15, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 59/23/71 | 153 | 9.7% | 1.9% | 0.75 | -4.0% | 349 | 1.41 | 3.1% | 84.1 | 9/9 | 1.00 | 0.70 | 0.05 | 4 | 3.9% | 0.60 | 0.70 | 8.4% | 6.8% | 8.0% | 9.4%/6.8% | 5.1 (interpolated) | pass | 0.041 (unverified) | n/a |
| 169 | `cfg_4e44` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=8, entry_z=-3.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 98/150/0 | 248 | 18.7% | 3.5% | 0.89 | -5.0% | 359 | 1.46 | 9.0% | 135.6 | 10/10 | 0.90 | 0.68 | 0.22 | 4 | 4.4% | 0.74 | 0.51 | 15.7% | 13.3% | 16.0% | 18.4%/14.3% | 5.2 (interpolated) | pass | 0.086 (unverified) | n/a |
| 170 | `cfg_e6dc` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=12, entry_z=-3.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 105/108/92 | 305 | 17.6% | 3.3% | 0.76 | -4.1% | 359 | 1.28 | 9.1% | 167.0 | 9/9 | 0.89 | 0.60 | 0.16 | 4 | 5.2% | 0.68 | 0.47 | 15.0% | 12.2% | 24.9% | 17.5%/13.6% | 4.5 (interpolated) | pass | 0.048 (unverified) | n/a |
| 171 | `cfg_eb0b` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=8, entry_z=-3.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 102/211/0 | 313 | 18.3% | 3.5% | 0.82 | -6.0% | 462 | 1.34 | 11.9% | 172.7 | 9/9 | 1.00 | 0.66 | 0.17 | 3 | 5.1% | 0.66 | 0.46 | 15.6% | 12.9% | 10.8% | 18.1%/13.7% | 4.7 (interpolated) | pass | 0.064 (unverified) | n/a |
| 172 | `cfg_26aa` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 66/115/0 | 181 | 13.6% | 2.6% | 0.85 | -2.4% | 133 | 1.46 | 5.5% | 99.6 | 11/11 | 0.91 | 0.74 | 0.11 | 5 | 7.5% | 0.43 | 0.51 | 12.0% | 10.8% | 12.4% | 13.2%/10.9% | 5.9 (interpolated) | pass | 0.073 (unverified) | n/a |
| 173 | `cfg_67c4` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=8, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 87/136/0 | 223 | 18.2% | 3.5% | 0.91 | -5.0% | 255 | 1.51 | 8.1% | 122.9 | 10/10 | 1.00 | 0.58 | 0.33 | 4 | 7.0% | 0.59 | 0.52 | 16.0% | 14.0% | 13.1% | 17.4%/13.3% | 5.7 (interpolated) | pass | 0.092 (unverified) | n/a |
| 174 | `cfg_e406` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-3.0, exit_z=0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 101/140/0 | 241 | 19.8% | 3.7% | 0.79 | -5.3% | 444 | 1.36 | 11.7% | 132.7 | 9/9 | 0.89 | 0.57 | 0.22 | 4 | 11.2% | 0.44 | 0.42 | 18.0% | 16.3% | 16.9% | 19.7%/15.6% | 6.2 (interpolated) | pass | 0.058 (unverified) | n/a |
| 175 | `cfg_f2cb` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=18, entry_z=-3.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 58/52/54 | 164 | 11.1% | 2.2% | 0.75 | -4.4% | 422 | 1.37 | 5.8% | 90.7 | 7/7 | 0.86 | 0.69 | 0.06 | 4 | 3.3% | 0.68 | 0.57 | 10.1% | 8.7% | 11.4% | 10.7%/7.7% | 5.8 (interpolated) | pass | 0.043 (unverified) | n/a |
| 176 | `cfg_56e2` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=18, entry_z=-3.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 64/172/0 | 236 | 16.0% | 3.1% | 0.86 | -4.0% | 360 | 1.41 | 7.4% | 129.0 | 9/9 | 1.00 | 0.73 | 0.13 | 4 | 5.9% | 0.60 | 0.43 | 13.6% | 11.5% | 14.3% | 15.1%/12.0% | 5.1 (interpolated) | pass | 0.077 (unverified) | n/a |
| 177 | `cfg_88b5` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=15, entry_z=-3.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 85/207/0 | 292 | 26.3% | 4.9% | 1.04 | -4.2% | 497 | 1.46 | 9.3% | 159.6 | 10/10 | 0.80 | 0.69 | 0.35 | 4 | 10.3% | 0.55 | 0.36 | 23.5% | 21.2% | 27.6% | 24.9%/21.2% | 6.5 (interpolated) | pass | 0.148 (unverified) | n/a |
| 178 | `cfg_6204` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 114/79/0 | 193 | 18.7% | 3.5% | 0.86 | -4.0% | 371 | 1.46 | 8.2% | 105.9 | 10/10 | 1.00 | 0.72 | 0.14 | 5 | 10.6% | 0.41 | 0.44 | 16.9% | 15.2% | 18.9% | 17.5%/14.2% | 7.0 (interpolated) | pass | 0.082 (unverified) | n/a |
| 179 | `cfg_cf08` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 224/41/125 | 390 | 21.7% | 4.1% | 0.80 | -6.3% | 351 | 1.25 | 13.7% | 212.4 | 11/11 | 1.00 | 0.71 | 0.09 | 4 | 7.1% | 0.64 | 0.50 | 19.0% | 15.2% | 21.8% | 21.9%/17.9% | 4.5 (interpolated) | pass | 0.055 (unverified) | n/a |
| 180 | `cfg_a0a5` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=18, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 50/97/0 | 147 | 15.0% | 2.9% | 1.02 | -2.3% | 422 | 1.70 | 4.3% | 81.1 | 7/7 | 1.00 | 0.83 | 0.19 | 4 | 9.3% | 0.35 | 0.41 | 13.8% | 12.9% | 11.5% | 13.4%/10.5% | 7.7 (interpolated) | pass | 0.143 (unverified) | n/a |
| 181 | `cfg_6f33` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=12, entry_z=-3.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 124/150/0 | 274 | 22.9% | 4.3% | 0.84 | -4.6% | 323 | 1.35 | 12.6% | 149.6 | 7/7 | 1.00 | 0.53 | 0.31 | 4 | 7.2% | 0.65 | 0.46 | 19.8% | 17.6% | 20.5% | 21.3%/16.5% | 5.7 (interpolated) | pass | 0.067 (unverified) | n/a |
| 182 | `cfg_4a3c` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 105/103/76 | 284 | 16.0% | 3.1% | 0.76 | -5.2% | 456 | 1.30 | 8.5% | 155.5 | 12/12 | 0.83 | 0.66 | 0.09 | 4 | 5.1% | 0.64 | 0.54 | 14.0% | 11.7% | 23.2% | 15.7%/13.4% | 4.4 (interpolated) | pass | 0.045 (unverified) | n/a |
| 183 | `cfg_79ff` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 57/48/49 | 154 | 11.2% | 2.2% | 0.79 | -3.2% | 476 | 1.43 | 5.5% | 85.2 | 10/10 | 0.80 | 0.65 | 0.14 | 4 | 2.0% | 0.80 | 0.56 | 9.9% | 8.4% | 8.1% | 10.6%/8.0% | 5.7 (interpolated) | pass | 0.053 (unverified) | n/a |
| 184 | `cfg_b16e` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 61/78/0 | 139 | 11.7% | 2.3% | 0.85 | -3.3% | 418 | 1.54 | 4.7% | 77.2 | 9/9 | 0.89 | 0.64 | 0.21 | 4 | 3.8% | 0.67 | 0.47 | 10.6% | 9.4% | 5.0% | 10.7%/8.8% | 6.5 (interpolated) | pass | 0.082 (unverified) | n/a |
| 185 | `cfg_bd2b` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 105/110/75 | 290 | 16.8% | 3.2% | 0.79 | -5.5% | 494 | 1.32 | 8.8% | 159.2 | 12/12 | 0.75 | 0.70 | 0.10 | 4 | 6.8% | 0.55 | 0.50 | 14.5% | 12.0% | 18.7% | 17.4%/14.1% | 4.5 (interpolated) | pass | 0.055 (unverified) | n/a |
| 186 | `cfg_9beb` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-3.0, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 64/42/48 | 154 | 10.7% | 2.1% | 0.79 | -2.6% | 445 | 1.42 | 5.2% | 85.1 | 9/9 | 0.78 | 0.64 | 0.15 | 4 | 2.5% | 0.75 | 0.56 | 9.5% | 8.1% | 6.4% | 9.4%/7.5% | 5.6 (interpolated) | pass | 0.054 (unverified) | n/a |
| 187 | `cfg_cf4e` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=12, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 131/154/0 | 285 | 26.1% | 4.8% | 0.98 | -5.2% | 413 | 1.43 | 13.1% | 155.7 | 10/10 | 0.90 | 0.73 | 0.25 | 5 | 11.7% | 0.50 | 0.39 | 23.1% | 19.2% | 22.1% | 24.5%/18.7% | 6.4 (interpolated) | pass | 0.115 (unverified) | n/a |
| 188 | `cfg_551f` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=12, entry_z=-3.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 109/165/0 | 274 | 21.7% | 4.1% | 0.80 | -5.3% | 438 | 1.33 | 13.0% | 149.2 | 8/8 | 1.00 | 0.57 | 0.23 | 4 | 5.3% | 0.74 | 0.48 | 18.2% | 15.7% | 18.6% | 19.4%/14.8% | 5.6 (interpolated) | pass | 0.056 (unverified) | n/a |
| 189 | `cfg_d520` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=12, entry_z=-3.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 99/75/77 | 251 | 15.9% | 3.0% | 0.77 | -4.6% | 223 | 1.32 | 7.4% | 138.4 | 10/10 | 1.00 | 0.69 | 0.08 | 4 | 7.4% | 0.51 | 0.51 | 13.7% | 11.2% | 17.0% | 15.0%/11.5% | 4.9 (interpolated) | pass | 0.049 (unverified) | n/a |
| 190 | `cfg_f61e` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=12, entry_z=-3.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 108/59/78 | 245 | 16.7% | 3.2% | 0.80 | -4.1% | 326 | 1.32 | 8.2% | 134.7 | 9/9 | 1.00 | 0.72 | 0.09 | 4 | 7.3% | 0.55 | 0.49 | 14.4% | 12.0% | 14.1% | 15.7%/12.7% | 5.3 (interpolated) | pass | 0.056 (unverified) | n/a |
| 191 | `cfg_3e3d` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=12, entry_z=-3.0, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 123/131/0 | 254 | 23.4% | 4.4% | 0.87 | -4.3% | 347 | 1.39 | 11.4% | 138.6 | 10/10 | 1.00 | 0.60 | 0.28 | 4 | 7.5% | 0.64 | 0.44 | 21.4% | 17.7% | 27.3% | 22.8%/17.9% | 6.4 (interpolated) | pass | 0.077 (unverified) | n/a |
| 192 | `cfg_0438` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=18, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 53/88/0 | 141 | 10.2% | 2.0% | 0.80 | -2.2% | 422 | 1.51 | 4.1% | 77.7 | 9/9 | 1.00 | 0.63 | 0.16 | 5 | 3.0% | 0.69 | 0.54 | 8.9% | 7.8% | 6.2% | 9.4%/7.4% | 5.7 (interpolated) | pass | 0.063 (unverified) | n/a |
| 193 | `cfg_1140` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 84/80/49 | 213 | 13.7% | 2.6% | 0.79 | -4.6% | 337 | 1.39 | 5.5% | 116.2 | 11/11 | 1.00 | 0.70 | 0.08 | 4 | 7.8% | 0.43 | 0.59 | 11.5% | 9.9% | 14.9% | 13.1%/10.1% | 4.7 (interpolated) | pass | 0.051 (unverified) | n/a |
| 194 | `cfg_4f6d` | timeframe=15min, mean_type=ema, mean_lookback=16, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 57/25/50 | 132 | 8.6% | 1.7% | 0.82 | -2.5% | 357 | 1.53 | 2.7% | 71.8 | 10/10 | 1.00 | 0.57 | 0.25 | 4 | 5.1% | 0.41 | 0.68 | 7.5% | 6.7% | 13.0% | 8.4%/6.4% | 5.3 (interpolated) | pass | 0.059 (unverified) | n/a |
| 195 | `cfg_e44e` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=12, entry_z=-3.0, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 144/113/0 | 257 | 21.5% | 4.0% | 0.78 | -4.8% | 350 | 1.34 | 10.9% | 140.1 | 9/9 | 1.00 | 0.64 | 0.14 | 3 | 3.3% | 0.83 | 0.50 | 18.5% | 16.5% | 24.7% | 20.8%/16.4% | 5.8 (interpolated) | pass | 0.054 (unverified) | n/a |
| 196 | `cfg_281e` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=12, entry_z=-2.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 58/111/49 | 218 | 13.7% | 2.7% | 0.76 | -5.4% | 468 | 1.38 | 6.1% | 118.7 | 11/11 | 0.91 | 0.70 | 0.07 | 4 | 6.6% | 0.48 | 0.59 | 11.5% | 9.8% | 13.1% | 13.2%/9.9% | 4.6 (interpolated) | pass | 0.047 (unverified) | n/a |
| 197 | `cfg_8c0e` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-3.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 74/64/31 | 169 | 11.4% | 2.2% | 0.75 | -3.3% | 330 | 1.42 | 4.5% | 92.7 | 10/10 | 1.00 | 0.67 | 0.08 | 5 | 6.0% | 0.46 | 0.64 | 9.4% | 8.0% | 10.1% | 10.4%/7.3% | 5.1 (interpolated) | pass | 0.043 (unverified) | n/a |
| 198 | `cfg_f739` | timeframe=15min, mean_type=sma, mean_lookback=30, std_lookback=12, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 128/134/98 | 360 | 18.3% | 3.5% | 0.76 | -5.6% | 543 | 1.27 | 11.6% | 197.4 | 12/12 | 0.83 | 0.62 | 0.14 | 3 | 5.9% | 0.63 | 0.51 | 15.8% | 12.1% | 20.1% | 17.6%/14.6% | 4.1 (interpolated) | pass | 0.047 (unverified) | n/a |
| 199 | `cfg_b367` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=18, entry_z=-3.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 19/185/0 | 204 | 13.8% | 2.7% | 0.81 | -4.1% | 201 | 1.43 | 4.6% | 112.3 | 6/6 | 0.83 | 0.66 | 0.15 | 5 | 4.1% | 0.69 | 0.53 | 11.8% | 10.5% | 12.5% | 12.4%/8.7% | 5.2 (interpolated) | pass | 0.059 (unverified) | n/a |
| 200 | `cfg_4dc3` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-3.0, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 122/88/0 | 210 | 13.7% | 2.6% | 0.77 | -7.0% | 352 | 1.40 | 7.4% | 115.5 | 10/10 | 0.90 | 0.61 | 0.16 | 5 | 8.5% | 0.37 | 0.53 | 12.3% | 10.7% | 10.2% | 12.9%/11.0% | 5.2 (interpolated) | pass | 0.053 (unverified) | n/a |
| 201 | `cfg_d076` | timeframe=15min, mean_type=sma, mean_lookback=50, std_lookback=18, entry_z=-3.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 31/173/0 | 204 | 13.2% | 2.5% | 0.79 | -4.0% | 308 | 1.42 | 4.5% | 112.1 | 7/7 | 1.00 | 0.76 | 0.03 | 4 | 3.6% | 0.72 | 0.54 | 11.5% | 10.1% | 13.0% | 11.3%/8.4% | 5.0 (interpolated) | pass | 0.054 (unverified) | n/a |
| 202 | `cfg_eafd` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-3.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 82/89/62 | 233 | 15.2% | 2.9% | 0.89 | -3.0% | 175 | 1.38 | 7.0% | 127.4 | 9/9 | 1.00 | 0.66 | 0.23 | 4 | 6.3% | 0.56 | 0.47 | 12.9% | 11.1% | 10.1% | 13.9%/11.1% | 5.1 (interpolated) | pass | 0.081 (unverified) | n/a |
| 203 | `cfg_5277` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-3.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 88/64/73 | 225 | 15.1% | 2.9% | 0.83 | -4.3% | 234 | 1.34 | 7.9% | 123.3 | 8/8 | 1.00 | 0.70 | 0.13 | 4 | 6.6% | 0.56 | 0.50 | 13.5% | 11.0% | 13.9% | 14.4%/11.5% | 5.2 (interpolated) | pass | 0.064 (unverified) | n/a |
| 204 | `cfg_384f` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=15, entry_z=-3.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 87/76/61 | 224 | 14.2% | 2.7% | 0.83 | -3.4% | 173 | 1.38 | 6.5% | 122.6 | 11/11 | 1.00 | 0.68 | 0.15 | 5 | 6.2% | 0.55 | 0.49 | 12.2% | 10.3% | 9.6% | 13.0%/10.6% | 5.0 (interpolated) | pass | 0.065 (unverified) | n/a |
| 205 | `cfg_7139` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 26/184/0 | 210 | 11.7% | 2.3% | 0.88 | -2.4% | 159 | 1.55 | 4.7% | 114.6 | 9/9 | 1.00 | 0.65 | 0.23 | 5 | 6.0% | 0.49 | 0.65 | 9.9% | 7.7% | 12.1% | 11.2%/7.7% | 4.4 (interpolated) | pass | 0.070 (unverified) | n/a |
| 206 | `cfg_ce90` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=18, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 49/92/0 | 141 | 8.2% | 1.6% | 0.86 | -2.4% | 293 | 1.60 | 2.9% | 77.0 | 8/8 | 1.00 | 0.54 | 0.32 | 4 | 3.3% | 0.59 | 0.54 | 7.1% | 6.2% | 2.5% | 7.1%/5.8% | 4.8 (interpolated) | pass | 0.073 (unverified) | n/a |
| 207 | `cfg_9301` | timeframe=15min, mean_type=ema, mean_lookback=30, std_lookback=18, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 26/114/0 | 140 | 8.0% | 1.6% | 0.83 | -2.4% | 288 | 1.58 | 3.1% | 76.6 | 9/9 | 1.00 | 0.52 | 0.31 | 4 | 3.3% | 0.57 | 0.59 | 7.2% | 6.1% | 2.7% | 7.0%/5.0% | 4.7 (interpolated) | pass | 0.064 (unverified) | n/a |
| 208 | `cfg_6a19` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 72/82/45 | 199 | 13.4% | 2.6% | 0.78 | -5.9% | 350 | 1.39 | 6.3% | 109.6 | 11/11 | 0.91 | 0.58 | 0.20 | 3 | 6.0% | 0.54 | 0.57 | 11.6% | 10.4% | 15.3% | 12.9%/10.2% | 5.2 (interpolated) | pass | 0.053 (unverified) | n/a |
| 209 | `cfg_0351` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-3.5, exit_z=-0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 72/97/64 | 233 | 14.9% | 2.9% | 0.86 | -2.8% | 175 | 1.37 | 7.2% | 127.3 | 10/10 | 0.90 | 0.59 | 0.27 | 4 | 6.1% | 0.57 | 0.48 | 12.8% | 10.8% | 9.9% | 13.4%/9.5% | 5.0 (interpolated) | pass | 0.073 (unverified) | n/a |
| 210 | `cfg_5108` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=15, entry_z=-2.5, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 66/50/0 | 116 | 11.9% | 2.3% | 0.79 | -3.4% | 200 | 1.55 | 4.9% | 64.3 | 10/10 | 1.00 | 0.64 | 0.15 | 4 | 4.8% | 0.59 | 0.58 | 10.5% | 9.4% | 7.9% | 10.4%/7.9% | 7.4 (interpolated) | pass | 0.066 (unverified) | n/a |
| 211 | `cfg_04dc` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=6, entry_z=-3.5, exit_z=-1.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 214/65/0 | 279 | 16.1% | 3.1% | 0.81 | -5.9% | 317 | 1.37 | 10.3% | 152.1 | 7/7 | 1.00 | 0.62 | 0.19 | 5 | 8.8% | 0.45 | 0.47 | 12.7% | 10.9% | 22.2% | 15.6%/12.1% | 4.5 (interpolated) | pass | 0.066 (unverified) | n/a |
| 212 | `cfg_843b` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 100/102/0 | 202 | 13.4% | 2.6% | 0.75 | -3.7% | 337 | 1.43 | 5.7% | 110.3 | 10/10 | 0.90 | 0.54 | 0.22 | 4 | 5.1% | 0.58 | 0.60 | 11.8% | 10.2% | 14.9% | 13.5%/10.6% | 4.9 (interpolated) | pass | 0.049 (unverified) | n/a |
| 213 | `cfg_39ba` | timeframe=15min, mean_type=sma, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 36/174/0 | 210 | 11.0% | 2.1% | 0.83 | -2.4% | 381 | 1.52 | 4.7% | 114.4 | 10/10 | 1.00 | 0.61 | 0.21 | 5 | 5.4% | 0.51 | 0.71 | 8.9% | 6.8% | 12.2% | 10.2%/7.6% | 4.2 (interpolated) | pass | 0.057 (unverified) | n/a |
| 214 | `cfg_60de` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=15, entry_z=-3.5, exit_z=-0.5, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=2.0 | 76/72/77 | 225 | 14.4% | 2.8% | 0.78 | -4.7% | 203 | 1.32 | 8.2% | 123.6 | 9/9 | 1.00 | 0.69 | 0.09 | 4 | 5.7% | 0.60 | 0.52 | 12.0% | 10.1% | 12.6% | 12.9%/9.6% | 5.0 (interpolated) | pass | 0.051 (unverified) | n/a |
| 215 | `cfg_c2e8` | timeframe=15min, mean_type=ema, mean_lookback=16, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=14, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 127/41/0 | 168 | 13.4% | 2.6% | 0.77 | -6.0% | 388 | 1.45 | 6.5% | 92.5 | 9/9 | 1.00 | 0.67 | 0.11 | 4 | 7.5% | 0.43 | 0.55 | 11.8% | 11.2% | 11.2% | 12.6%/11.1% | 6.2 (interpolated) | pass | 0.056 (unverified) | n/a |
| 216 | `cfg_1399` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=12, entry_z=-3.5, exit_z=-1.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 111/161/0 | 272 | 21.2% | 4.0% | 0.83 | -4.1% | 329 | 1.35 | 9.9% | 148.7 | 8/8 | 1.00 | 0.55 | 0.28 | 4 | 9.6% | 0.52 | 0.40 | 18.8% | 16.1% | 24.8% | 20.2%/15.7% | 5.6 (interpolated) | pass | 0.071 (unverified) | n/a |
| 217 | `cfg_6b7d` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 21/95/54 | 170 | 9.3% | 1.8% | 0.77 | -3.2% | 372 | 1.48 | 3.1% | 92.8 | 9/9 | 1.00 | 0.56 | 0.21 | 4 | 2.7% | 0.71 | 0.72 | 8.0% | 6.7% | 8.1% | 9.1%/6.8% | 4.5 (interpolated) | pass | 0.051 (unverified) | n/a |
| 218 | `cfg_d24f` | timeframe=15min, mean_type=ema, mean_lookback=25, std_lookback=12, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.0 | 27/89/54 | 170 | 9.0% | 1.8% | 0.75 | -3.2% | 372 | 1.47 | 3.1% | 92.9 | 10/10 | 1.00 | 0.63 | 0.12 | 4 | 2.4% | 0.73 | 0.74 | 7.6% | 6.4% | 8.0% | 8.7%/7.0% | 4.4 (interpolated) | pass | 0.048 (unverified) | n/a |
| 219 | `cfg_fb2c` | timeframe=15min, mean_type=sma, mean_lookback=20, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 120/92/0 | 212 | 11.7% | 2.3% | 0.79 | -3.1% | 309 | 1.45 | 6.0% | 116.4 | 11/11 | 0.73 | 0.60 | 0.19 | 5 | 6.6% | 0.42 | 0.62 | 9.9% | 8.3% | 6.7% | 10.8%/8.4% | 4.3 (interpolated) | pass | 0.053 (unverified) | n/a |
| 220 | `cfg_4065` | timeframe=15min, mean_type=ema, mean_lookback=20, std_lookback=10, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 76/107/0 | 183 | 14.7% | 2.8% | 0.80 | -7.7% | 350 | 1.46 | 6.7% | 100.4 | 10/10 | 0.90 | 0.64 | 0.16 | 4 | 7.1% | 0.51 | 0.52 | 13.0% | 11.2% | 14.7% | 14.2%/11.5% | 6.1 (interpolated) | pass | 0.064 (unverified) | n/a |
| 221 | `cfg_956a` | timeframe=15min, mean_type=ema, mean_lookback=50, std_lookback=18, entry_z=-2.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 116/252/0 | 368 | 19.1% | 3.6% | 0.79 | -7.1% | 350 | 1.28 | 11.3% | 200.8 | 8/8 | 1.00 | 0.58 | 0.21 | 4 | 6.0% | 0.68 | 0.48 | 16.4% | 13.4% | 22.5% | 16.5%/12.7% | 4.3 (interpolated) | pass | 0.055 (unverified) | n/a |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 2.6% / 0.71 / 76 | 2.7% / 0.94 / 62 | 13.8% / 2.39 / 59 | 5.5% / 1.16 / 54 | 5.7% / 1.07 / 69 |
| 2 | 2.1% / 0.65 / 76 | 2.3% / 0.84 / 62 | 13.4% / 2.42 / 59 | 4.5% / 1.01 / 54 | 5.9% / 1.11 / 69 |
| 3 | 4.0% / 0.98 / 64 | 1.8% / 0.66 / 45 | 13.3% / 2.39 / 51 | 1.8% / 0.39 / 46 | 6.8% / 1.27 / 62 |
| 4 | 3.8% / 0.92 / 67 | 2.3% / 0.74 / 52 | 12.1% / 2.06 / 52 | 4.0% / 0.79 / 51 | 7.4% / 1.34 / 66 |
| 5 | 1.5% / 0.36 / 72 | 4.1% / 1.28 / 57 | 13.3% / 2.41 / 56 | 1.6% / 0.31 / 54 | 7.4% / 1.28 / 63 |
| 6 | 1.3% / 0.37 / 56 | 3.2% / 1.10 / 45 | 11.6% / 2.10 / 48 | 1.9% / 0.42 / 44 | 6.9% / 1.31 / 61 |
| 7 | 2.2% / 0.62 / 48 | 3.8% / 1.64 / 35 | 10.8% / 2.23 / 39 | -0.5% / -0.09 / 34 | 6.5% / 1.31 / 49 |
| 8 | 2.6% / 0.94 / 58 | 0.3% / 0.13 / 41 | 13.3% / 2.66 / 46 | 0.2% / 0.07 / 45 | 4.7% / 1.04 / 53 |
| 9 | 3.4% / 0.80 / 59 | 3.5% / 1.08 / 46 | 12.0% / 2.21 / 50 | -0.1% / -0.01 / 41 | 5.4% / 0.99 / 57 |
| 10 | 1.3% / 0.95 / 38 | 0.6% / 0.44 / 29 | 6.3% / 2.29 / 28 | 2.1% / 0.69 / 32 | 1.6% / 0.60 / 34 |
| 11 | 3.5% / 0.98 / 64 | 0.3% / 0.10 / 50 | 10.9% / 1.81 / 56 | 1.7% / 0.37 / 50 | 6.4% / 1.19 / 66 |
| 12 | 2.7% / 1.09 / 48 | 4.0% / 1.96 / 38 | 6.0% / 1.40 / 41 | 2.2% / 0.62 / 34 | 2.6% / 0.58 / 52 |
| 13 | 2.7% / 0.71 / 82 | 2.7% / 0.96 / 63 | 12.2% / 2.09 / 65 | 1.7% / 0.39 / 59 | 6.9% / 1.26 / 75 |
| 14 | 4.5% / 1.41 / 58 | -1.1% / -0.39 / 41 | 12.8% / 2.41 / 45 | 1.1% / 0.25 / 45 | 4.6% / 0.98 / 53 |
| 15 | 6.3% / 1.93 / 52 | 3.3% / 1.55 / 36 | 7.2% / 1.28 / 43 | 0.6% / 0.14 / 41 | 3.0% / 0.62 / 53 |
| 16 | 2.2% / 0.79 / 76 | 1.2% / 0.48 / 62 | 12.0% / 2.22 / 59 | 3.6% / 0.83 / 54 | 2.8% / 0.56 / 69 |
| 17 | 0.7% / 0.32 / 45 | 0.3% / 0.36 / 26 | 4.5% / 2.20 / 23 | 3.2% / 1.30 / 30 | 2.7% / 0.77 / 43 |
| 18 | 1.1% / 0.72 / 42 | 0.2% / 0.16 / 30 | 6.6% / 2.94 / 31 | 0.1% / 0.05 / 34 | 2.9% / 1.38 / 35 |
| 19 | -0.3% / -0.14 / 40 | 1.3% / 0.95 / 34 | 7.2% / 2.69 / 31 | 1.1% / 0.49 / 25 | 1.8% / 0.68 / 43 |
| 20 | -1.6% / -0.31 / 78 | 2.3% / 0.73 / 59 | 10.2% / 1.57 / 61 | 5.5% / 1.04 / 63 | 8.1% / 1.40 / 75 |
| 21 | 4.3% / 1.08 / 64 | 0.1% / 0.06 / 50 | 13.0% / 1.95 / 56 | 2.5% / 0.54 / 50 | 4.7% / 0.84 / 65 |
| 22 | 6.2% / 1.64 / 57 | 0.4% / 0.16 / 42 | 10.4% / 1.71 / 46 | 0.1% / 0.04 / 42 | 7.2% / 1.31 / 55 |
| 23 | 6.1% / 2.12 / 57 | 1.3% / 0.60 / 43 | 8.9% / 1.68 / 47 | 1.0% / 0.25 / 41 | 2.8% / 0.61 / 55 |
| 24 | 6.4% / 2.23 / 52 | 3.2% / 1.50 / 36 | 6.9% / 1.31 / 43 | 0.0% / 0.03 / 41 | 3.2% / 0.64 / 53 |
| 25 | 0.3% / 0.16 / 45 | 0.2% / 0.26 / 26 | 4.9% / 2.15 / 23 | 3.4% / 1.37 / 30 | 2.6% / 0.75 / 43 |
| 26 | 1.2% / 0.79 / 42 | 0.3% / 0.29 / 29 | 6.9% / 2.98 / 31 | -0.6% / -0.23 / 35 | 2.7% / 1.26 / 34 |
| 27 | 1.2% / 1.11 / 22 | 1.3% / 1.28 / 21 | 6.0% / 2.62 / 26 | 0.4% / 0.17 / 23 | 2.3% / 0.73 / 25 |
| 28 | -0.4% / -0.06 / 78 | 1.3% / 0.42 / 59 | 12.2% / 1.90 / 61 | 4.9% / 0.95 / 63 | 7.6% / 1.31 / 75 |
| 29 | 6.4% / 2.10 / 49 | -0.5% / -0.22 / 33 | 8.7% / 1.61 / 38 | 2.2% / 0.57 / 31 | 4.6% / 0.90 / 51 |
| 30 | 2.3% / 0.92 / 48 | 3.0% / 1.70 / 39 | 6.0% / 1.41 / 41 | 2.6% / 0.71 / 34 | 2.8% / 0.62 / 52 |
| 31 | 6.0% / 1.81 / 57 | 1.6% / 0.73 / 43 | 9.0% / 1.64 / 47 | 1.4% / 0.34 / 41 | 2.1% / 0.46 / 55 |
| 32 | 5.7% / 1.66 / 57 | 0.6% / 0.26 / 43 | 9.1% / 1.62 / 46 | -0.4% / -0.06 / 42 | 8.0% / 1.54 / 55 |
| 33 | 2.7% / 1.49 / 32 | 0.6% / 0.44 / 21 | 6.0% / 2.37 / 23 | 3.2% / 1.08 / 28 | -0.2% / -0.04 / 33 |
| 34 | 3.3% / 0.70 / 80 | 1.8% / 0.56 / 59 | 11.0% / 1.52 / 57 | 5.6% / 1.14 / 61 | 3.0% / 0.58 / 76 |
| 35 | 0.4% / 0.27 / 40 | 0.0% / 0.02 / 30 | 7.0% / 2.66 / 31 | 0.9% / 0.34 / 33 | 2.4% / 1.01 / 35 |
| 36 | 1.7% / 0.60 / 57 | 1.1% / 0.41 / 51 | 14.7% / 2.65 / 45 | -0.5% / -0.08 / 48 | 8.9% / 2.04 / 58 |
| 37 | 5.1% / 1.99 / 49 | 1.0% / 0.45 / 33 | 7.4% / 1.51 / 38 | 2.0% / 0.51 / 31 | 4.3% / 0.88 / 51 |
| 38 | 3.3% / 1.42 / 53 | -0.3% / -0.14 / 37 | 10.2% / 2.05 / 39 | -1.1% / -0.22 / 38 | 8.6% / 2.04 / 53 |
| 39 | -0.3% / -0.14 / 40 | 1.3% / 0.95 / 34 | 7.2% / 2.59 / 31 | 0.4% / 0.20 / 25 | 1.9% / 0.69 / 43 |
| 40 | -0.3% / -0.05 / 70 | 0.7% / 0.24 / 54 | 14.0% / 2.36 / 56 | 2.2% / 0.48 / 55 | 5.9% / 1.08 / 70 |
| 41 | 1.1% / 0.48 / 48 | 1.8% / 1.16 / 39 | 5.0% / 1.15 / 42 | 3.1% / 0.95 / 34 | 4.7% / 1.08 / 52 |
| 42 | 0.9% / 0.88 / 22 | 1.3% / 1.24 / 21 | 5.8% / 2.58 / 26 | 0.5% / 0.25 / 23 | 2.2% / 0.71 / 25 |
| 43 | -1.1% / -0.51 / 43 | 0.3% / 0.23 / 33 | 7.6% / 2.61 / 30 | 2.3% / 0.91 / 27 | 3.0% / 0.98 / 44 |
| 44 | 1.8% / 0.43 / 83 | 2.1% / 0.62 / 61 | 9.5% / 1.38 / 62 | 4.2% / 0.85 / 63 | 5.0% / 0.89 / 77 |
| 45 | 4.2% / 1.52 / 61 | 4.1% / 1.49 / 50 | 2.6% / 0.51 / 47 | 3.8% / 0.85 / 52 | 6.3% / 1.35 / 61 |
| 46 | 4.0% / 0.88 / 81 | 2.0% / 0.61 / 59 | 10.9% / 1.49 / 57 | 5.9% / 1.21 / 61 | 3.1% / 0.59 / 76 |
| 47 | 1.1% / 0.62 / 29 | 1.1% / 0.76 / 21 | 4.2% / 1.45 / 24 | 0.5% / 0.20 / 21 | 5.1% / 1.72 / 33 |
| 48 | -0.1% / -0.11 / 22 | 1.2% / 1.14 / 21 | 3.7% / 1.80 / 26 | 1.2% / 0.56 / 23 | 2.9% / 1.14 / 25 |
| 49 | 2.9% / 0.93 / 54 | 1.0% / 0.43 / 41 | 9.8% / 2.13 / 42 | -0.1% / -0.00 / 36 | 4.0% / 0.83 / 53 |
| 50 | 0.5% / 0.48 / 22 | 1.2% / 1.15 / 21 | 2.8% / 1.44 / 26 | 1.2% / 0.57 / 23 | 2.4% / 1.03 / 25 |
| 51 | -0.0% / 0.02 / 70 | 0.9% / 0.32 / 54 | 13.8% / 2.21 / 56 | 3.1% / 0.67 / 55 | 6.3% / 1.10 / 70 |
| 52 | -0.2% / -0.04 / 78 | 2.6% / 0.90 / 56 | 8.2% / 1.49 / 57 | 8.5% / 1.85 / 54 | 1.9% / 0.38 / 71 |
| 53 | 1.3% / 0.75 / 34 | -1.0% / -0.47 / 29 | 4.0% / 1.10 / 29 | 1.3% / 0.39 / 31 | 7.4% / 1.97 / 45 |
| 54 | 0.7% / 0.49 / 35 | -0.3% / -0.16 / 30 | 4.3% / 1.19 / 30 | 2.0% / 0.63 / 31 | 6.3% / 1.75 / 45 |
| 55 | 2.0% / 1.01 / 36 | 0.2% / 0.17 / 23 | 8.5% / 2.76 / 25 | 1.7% / 0.56 / 32 | -0.2% / -0.04 / 34 |
| 56 | 0.4% / 0.14 / 78 | 1.9% / 0.67 / 56 | 9.3% / 1.71 / 57 | 6.8% / 1.53 / 54 | 1.4% / 0.29 / 71 |
| 57 | 1.4% / 0.37 / 60 | 0.9% / 0.34 / 45 | 11.7% / 2.14 / 48 | 2.1% / 0.49 / 44 | 4.7% / 0.86 / 62 |
| 58 | 1.7% / 0.52 / 44 | 4.9% / 2.07 / 35 | 5.2% / 1.14 / 36 | 1.0% / 0.24 / 34 | 6.6% / 1.36 / 50 |
| 59 | -0.7% / -0.32 / 40 | 1.0% / 0.73 / 32 | 7.3% / 2.45 / 30 | 1.5% / 0.57 / 25 | 2.3% / 0.70 / 40 |
| 60 | 2.4% / 0.67 / 48 | 2.2% / 0.90 / 35 | 8.1% / 1.72 / 39 | 0.4% / 0.10 / 34 | 5.3% / 1.10 / 48 |
| 61 | 1.9% / 0.45 / 70 | 1.7% / 0.54 / 55 | 8.7% / 1.27 / 55 | 6.5% / 1.31 / 54 | 2.8% / 0.54 / 70 |
| 62 | 1.3% / 0.57 / 48 | 2.2% / 1.40 / 39 | 5.5% / 1.31 / 42 | 2.6% / 0.77 / 34 | 3.6% / 0.84 / 52 |
| 63 | 1.2% / 0.78 / 27 | -0.4% / -0.27 / 21 | 4.8% / 1.95 / 22 | 1.8% / 0.65 / 22 | 4.6% / 1.85 / 28 |
| 64 | 2.9% / 1.54 / 36 | 0.9% / 0.84 / 23 | 7.8% / 2.69 / 25 | 1.9% / 0.65 / 32 | -0.9% / -0.28 / 34 |
| 65 | 2.3% / 1.08 / 53 | -0.4% / -0.17 / 37 | 9.1% / 2.03 / 39 | -1.5% / -0.30 / 38 | 7.0% / 1.78 / 53 |
| 66 | 2.2% / 0.71 / 54 | 0.2% / 0.09 / 41 | 9.8% / 2.13 / 42 | 0.3% / 0.09 / 36 | 4.8% / 1.04 / 52 |
| 67 | 1.4% / 0.47 / 44 | 4.5% / 1.98 / 35 | 5.4% / 1.19 / 36 | -0.0% / 0.02 / 34 | 6.0% / 1.25 / 50 |
| 68 | 0.7% / 0.63 / 21 | 1.2% / 1.01 / 19 | 4.6% / 1.98 / 23 | 1.6% / 0.69 / 20 | 2.3% / 0.72 / 25 |
| 69 | 1.9% / 0.99 / 32 | 0.4% / 0.35 / 21 | 5.9% / 2.38 / 23 | 3.4% / 1.14 / 28 | -0.1% / -0.01 / 33 |
| 70 | -0.9% / -0.22 / 84 | -0.6% / -0.20 / 54 | 17.5% / 2.97 / 65 | 1.9% / 0.47 / 57 | 4.5% / 0.80 / 81 |
| 71 | 3.3% / 1.84 / 32 | 1.1% / 0.80 / 20 | 5.7% / 2.07 / 23 | 2.3% / 0.72 / 24 | 1.1% / 0.35 / 29 |
| 72 | 1.7% / 0.50 / 68 | 0.2% / 0.09 / 53 | 12.5% / 2.27 / 53 | 1.9% / 0.43 / 48 | 3.5% / 0.66 / 67 |
| 73 | 2.1% / 0.95 / 62 | 2.4% / 0.96 / 51 | 4.5% / 0.88 / 51 | 5.3% / 1.23 / 52 | 4.1% / 0.91 / 62 |
| 74 | 0.5% / 0.22 / 52 | 0.7% / 0.46 / 35 | 6.4% / 2.44 / 30 | 2.8% / 0.93 / 33 | 3.8% / 0.91 / 53 |
| 75 | 0.0% / 0.04 / 39 | 0.7% / 0.45 / 28 | 5.4% / 3.01 / 21 | 1.0% / 0.46 / 24 | 3.0% / 0.97 / 33 |
| 76 | 5.3% / 1.47 / 58 | -1.5% / -0.56 / 41 | 14.7% / 2.43 / 45 | 1.7% / 0.37 / 45 | 5.8% / 1.20 / 53 |
| 77 | 0.3% / 0.23 / 35 | -1.1% / -0.68 / 30 | 4.5% / 1.22 / 30 | 2.1% / 0.67 / 31 | 6.9% / 1.92 / 46 |
| 78 | 1.4% / 0.35 / 61 | 3.0% / 0.96 / 50 | 6.4% / 0.98 / 49 | 5.2% / 1.12 / 43 | 4.8% / 0.89 / 62 |
| 79 | 1.3% / 0.36 / 61 | 4.5% / 1.60 / 50 | 6.5% / 1.02 / 49 | 3.8% / 0.88 / 43 | 3.8% / 0.72 / 62 |
| 80 | 2.1% / 0.57 / 84 | 0.3% / 0.13 / 64 | 10.9% / 1.58 / 60 | 6.5% / 1.56 / 61 | 0.3% / 0.09 / 78 |
| 81 | 1.4% / 0.44 / 64 | 1.1% / 0.42 / 51 | 10.9% / 1.90 / 57 | 0.6% / 0.15 / 50 | 5.3% / 1.04 / 66 |
| 82 | 4.1% / 1.19 / 83 | 1.5% / 0.55 / 65 | 9.5% / 1.82 / 66 | -0.9% / -0.18 / 61 | 6.1% / 1.20 / 74 |
| 83 | 2.5% / 0.60 / 70 | 2.9% / 0.93 / 55 | 9.5% / 1.34 / 55 | 5.5% / 1.12 / 54 | 3.9% / 0.73 / 70 |
| 84 | 1.8% / 0.52 / 73 | -1.8% / -0.69 / 58 | 10.4% / 1.68 / 56 | 6.4% / 1.51 / 45 | 3.4% / 0.68 / 65 |
| 85 | 2.3% / 0.73 / 85 | 1.0% / 0.36 / 64 | 10.4% / 1.65 / 64 | 5.5% / 1.28 / 63 | 1.2% / 0.27 / 78 |
| 86 | 1.2% / 0.73 / 34 | -0.7% / -0.35 / 29 | 3.9% / 1.10 / 29 | 0.6% / 0.19 / 31 | 7.4% / 2.04 / 45 |
| 87 | 1.5% / 0.64 / 36 | 1.3% / 0.85 / 23 | 6.0% / 1.98 / 26 | 1.2% / 0.42 / 25 | 3.3% / 0.81 / 38 |
| 88 | 0.6% / 0.21 / 73 | -0.5% / -0.19 / 55 | 10.6% / 2.04 / 56 | 5.8% / 1.41 / 48 | -0.1% / 0.01 / 70 |
| 89 | 0.9% / 0.77 / 21 | 1.4% / 1.23 / 19 | 4.0% / 1.76 / 22 | 1.8% / 0.76 / 20 | 2.1% / 0.66 / 25 |
| 90 | 1.6% / 0.69 / 36 | 1.2% / 0.75 / 23 | 4.4% / 1.36 / 26 | 1.6% / 0.55 / 25 | 4.0% / 0.99 / 38 |
| 91 | 1.5% / 0.86 / 29 | 1.0% / 0.66 / 21 | 4.0% / 1.39 / 24 | -0.4% / -0.14 / 21 | 4.3% / 1.42 / 32 |
| 92 | 1.3% / 0.34 / 84 | 0.5% / 0.17 / 64 | 11.3% / 1.62 / 60 | 7.0% / 1.64 / 61 | 0.6% / 0.16 / 78 |
| 93 | 1.0% / 0.33 / 73 | -0.4% / -0.16 / 58 | 11.4% / 1.94 / 56 | 5.7% / 1.43 / 45 | 3.3% / 0.69 / 65 |
| 94 | 0.3% / 0.13 / 76 | 1.1% / 0.46 / 62 | 10.5% / 1.89 / 59 | 8.0% / 1.87 / 53 | 0.9% / 0.21 / 69 |
| 95 | 2.2% / 1.42 / 32 | 1.0% / 0.77 / 20 | 6.2% / 2.46 / 23 | 1.8% / 0.58 / 24 | 1.1% / 0.36 / 29 |
| 96 | 5.9% / 1.66 / 73 | -1.8% / -0.65 / 59 | 12.3% / 2.18 / 59 | 0.4% / 0.11 / 51 | 5.2% / 0.98 / 68 |
| 97 | 5.3% / 1.43 / 83 | 0.9% / 0.31 / 65 | 10.0% / 1.75 / 64 | -0.0% / 0.01 / 60 | 5.3% / 1.00 / 74 |
| 98 | -0.1% / -0.08 / 38 | 0.6% / 0.39 / 28 | 5.4% / 3.02 / 21 | 1.0% / 0.44 / 24 | 3.0% / 0.98 / 33 |
| 99 | 2.7% / 1.41 / 24 | 0.9% / 0.71 / 18 | 3.6% / 1.51 / 17 | 0.7% / 0.27 / 22 | 2.1% / 0.83 / 23 |
| 100 | 4.7% / 1.34 / 67 | -2.3% / -0.87 / 57 | 11.8% / 2.09 / 54 | 0.9% / 0.22 / 47 | 4.7% / 0.93 / 63 |
| 101 | 1.9% / 0.63 / 48 | 2.1% / 1.12 / 39 | 3.7% / 0.91 / 41 | 3.4% / 0.87 / 34 | 3.5% / 0.76 / 52 |
| 102 | 4.2% / 1.71 / 52 | 3.7% / 1.95 / 36 | 7.3% / 1.40 / 45 | 2.7% / 0.60 / 41 | 1.0% / 0.23 / 53 |
| 103 | 2.1% / 0.70 / 73 | 0.6% / 0.29 / 58 | 10.9% / 1.85 / 56 | 5.0% / 1.31 / 45 | 1.4% / 0.31 / 65 |
| 104 | 3.7% / 1.83 / 43 | 2.1% / 1.19 / 31 | 6.1% / 1.41 / 33 | -0.5% / -0.09 / 27 | 3.8% / 1.08 / 46 |
| 105 | 1.7% / 0.52 / 67 | -0.3% / -0.10 / 53 | 11.9% / 2.19 / 53 | 2.1% / 0.48 / 47 | 4.9% / 0.94 / 65 |
| 106 | 2.9% / 0.91 / 83 | 1.3% / 0.50 / 62 | 12.5% / 2.26 / 68 | -0.4% / -0.06 / 60 | 4.4% / 0.85 / 76 |
| 107 | 0.8% / 0.23 / 85 | 0.8% / 0.31 / 64 | 13.2% / 2.42 / 62 | 1.1% / 0.23 / 59 | 5.0% / 0.96 / 78 |
| 108 | 0.8% / 0.20 / 82 | 3.6% / 1.04 / 60 | 6.2% / 0.90 / 62 | 6.0% / 1.16 / 63 | 5.3% / 0.93 / 76 |
| 109 | 0.1% / 0.04 / 52 | 0.8% / 0.47 / 35 | 6.5% / 2.44 / 30 | 2.1% / 0.70 / 34 | 4.0% / 0.97 / 54 |
| 110 | 0.1% / 0.05 / 55 | 0.1% / 0.09 / 40 | 6.2% / 2.35 / 32 | 3.1% / 1.05 / 37 | 3.6% / 0.89 / 56 |
| 111 | -0.6% / -0.26 / 57 | 1.6% / 0.68 / 52 | 12.3% / 2.28 / 45 | -0.2% / -0.02 / 49 | 6.2% / 1.60 / 59 |
| 112 | 2.1% / 0.93 / 46 | 1.1% / 0.67 / 31 | 5.7% / 1.90 / 28 | 1.3% / 0.40 / 28 | 3.6% / 0.85 / 49 |
| 113 | 1.0% / 0.94 / 24 | 0.4% / 0.34 / 18 | 3.9% / 1.34 / 18 | -0.5% / -0.19 / 20 | 3.8% / 1.75 / 30 |
| 114 | 0.3% / 0.08 / 89 | -0.9% / -0.33 / 67 | 17.4% / 2.65 / 66 | 4.8% / 1.04 / 62 | 1.1% / 0.23 / 83 |
| 115 | 1.3% / 0.88 / 37 | 0.6% / 0.55 / 25 | 4.8% / 2.03 / 25 | 1.5% / 0.60 / 32 | 0.6% / 0.26 / 34 |
| 116 | 1.2% / 1.03 / 24 | -0.1% / -0.10 / 18 | 2.1% / 0.70 / 18 | 0.6% / 0.25 / 20 | 4.5% / 2.00 / 30 |
| 117 | -0.3% / -0.20 / 29 | 1.1% / 1.09 / 19 | 4.4% / 2.26 / 17 | 0.9% / 0.47 / 23 | 1.7% / 0.70 / 36 |
| 118 | -0.2% / -0.17 / 29 | 1.1% / 1.04 / 19 | 4.3% / 2.25 / 17 | 1.0% / 0.53 / 23 | 1.7% / 0.67 / 36 |
| 119 | 2.7% / 0.88 / 48 | 2.7% / 1.18 / 38 | 3.4% / 0.81 / 41 | 3.1% / 0.78 / 34 | 3.3% / 0.72 / 52 |
| 120 | 2.1% / 1.47 / 34 | 0.3% / 0.28 / 24 | 4.1% / 1.75 / 24 | 2.6% / 0.99 / 30 | 0.3% / 0.12 / 34 |
| 121 | -2.5% / -0.62 / 99 | 1.4% / 0.47 / 73 | 13.9% / 2.41 / 73 | 5.0% / 0.97 / 70 | 3.1% / 0.57 / 85 |
| 122 | -1.4% / -0.50 / 37 | 0.7% / 0.51 / 31 | 8.1% / 2.93 / 28 | 0.3% / 0.13 / 21 | 3.6% / 1.15 / 32 |
| 123 | 5.5% / 2.29 / 43 | 2.2% / 1.12 / 31 | 6.8% / 1.47 / 33 | 1.1% / 0.28 / 27 | 1.7% / 0.44 / 46 |
| 124 | 3.0% / 1.32 / 57 | 2.0% / 0.98 / 43 | 8.7% / 1.60 / 47 | 4.0% / 1.00 / 41 | 1.4% / 0.32 / 55 |
| 125 | 2.0% / 0.58 / 78 | 1.7% / 0.62 / 59 | 11.5% / 2.09 / 62 | 2.2% / 0.46 / 56 | 2.0% / 0.40 / 72 |
| 126 | 1.3% / 0.83 / 27 | -0.4% / -0.32 / 20 | 4.2% / 1.71 / 22 | 1.5% / 0.54 / 21 | 4.4% / 1.70 / 28 |
| 127 | 2.8% / 1.45 / 24 | 0.8% / 0.58 / 18 | 2.6% / 1.06 / 17 | 1.1% / 0.41 / 22 | 3.0% / 1.12 / 23 |
| 128 | -1.5% / -0.43 / 82 | -0.2% / -0.07 / 56 | 14.8% / 2.25 / 68 | 3.5% / 0.84 / 59 | 7.2% / 1.34 / 79 |
| 129 | -2.0% / -0.70 / 37 | 0.7% / 0.53 / 31 | 8.4% / 2.91 / 28 | -0.0% / -0.00 / 21 | 4.1% / 1.28 / 32 |
| 130 | 0.7% / 0.25 / 45 | 2.8% / 1.76 / 36 | 6.1% / 1.46 / 39 | 1.5% / 0.43 / 34 | 3.3% / 0.76 / 51 |
| 131 | 2.8% / 1.08 / 65 | 2.8% / 1.04 / 58 | 5.9% / 1.23 / 54 | 1.9% / 0.44 / 54 | 4.5% / 0.98 / 64 |
| 132 | 0.5% / 0.45 / 41 | 0.1% / 0.05 / 30 | 5.9% / 2.52 / 31 | 0.9% / 0.36 / 34 | 1.6% / 0.97 / 35 |
| 133 | 1.9% / 0.67 / 60 | -0.4% / -0.22 / 36 | 7.0% / 2.21 / 41 | 3.8% / 1.04 / 40 | 2.1% / 0.53 / 56 |
| 134 | 1.1% / 0.39 / 72 | 1.5% / 0.65 / 57 | 11.2% / 1.88 / 56 | 4.1% / 1.06 / 45 | -0.0% / 0.03 / 66 |
| 135 | 0.1% / 0.04 / 52 | 0.7% / 0.46 / 35 | 6.5% / 2.46 / 30 | 2.7% / 0.90 / 33 | 3.7% / 0.89 / 53 |
| 136 | 2.6% / 1.20 / 29 | 1.6% / 1.00 / 21 | 3.6% / 1.15 / 24 | 1.0% / 0.35 / 21 | 1.8% / 0.52 / 33 |
| 137 | 0.4% / 0.19 / 37 | 1.2% / 0.80 / 23 | 4.2% / 1.35 / 27 | 1.7% / 0.63 / 25 | 3.6% / 0.96 / 39 |
| 138 | 0.9% / 0.33 / 75 | -2.6% / -1.18 / 59 | 10.1% / 1.72 / 57 | 5.3% / 1.39 / 45 | 3.1% / 0.69 / 65 |
| 139 | 2.5% / 0.69 / 85 | 2.0% / 0.66 / 64 | 7.6% / 1.24 / 64 | 7.3% / 1.60 / 63 | 0.8% / 0.19 / 77 |
| 140 | 1.2% / 0.41 / 75 | -2.1% / -0.99 / 59 | 9.8% / 1.70 / 57 | 5.1% / 1.40 / 45 | 2.9% / 0.65 / 65 |
| 141 | 5.1% / 1.68 / 54 | -3.4% / -1.56 / 42 | 6.6% / 1.41 / 41 | 3.2% / 0.82 / 36 | 4.3% / 0.94 / 48 |
| 142 | 0.6% / 0.22 / 45 | 2.4% / 1.52 / 36 | 5.9% / 1.35 / 39 | 1.9% / 0.55 / 34 | 4.5% / 1.01 / 51 |
| 143 | -0.4% / -0.06 / 108 | 0.2% / 0.07 / 83 | 14.4% / 2.12 / 81 | 3.3% / 0.71 / 72 | 2.1% / 0.39 / 94 |
| 144 | 1.4% / 1.12 / 31 | -0.8% / -0.68 / 24 | 4.3% / 1.78 / 25 | 0.6% / 0.23 / 22 | 3.7% / 1.47 / 29 |
| 145 | 4.3% / 1.39 / 57 | -2.2% / -1.06 / 44 | 8.9% / 1.81 / 44 | 2.9% / 0.79 / 39 | 2.9% / 0.65 / 54 |
| 146 | -0.1% / -0.08 / 27 | 0.3% / 0.34 / 17 | 5.1% / 2.11 / 14 | 1.4% / 0.58 / 19 | 2.0% / 0.80 / 24 |
| 147 | 0.9% / 0.36 / 44 | -0.5% / -0.52 / 25 | 6.2% / 2.45 / 22 | 2.2% / 0.78 / 31 | 2.4% / 0.69 / 43 |
| 148 | -0.5% / -0.15 / 77 | 1.6% / 0.57 / 62 | 10.9% / 2.04 / 59 | 4.6% / 0.99 / 57 | 2.4% / 0.55 / 72 |
| 149 | -0.3% / -0.09 / 45 | 0.2% / 0.22 / 23 | 9.3% / 2.86 / 22 | 4.5% / 1.32 / 30 | -1.5% / -0.36 / 44 |
| 150 | 0.9% / 0.24 / 75 | 0.4% / 0.15 / 57 | 11.2% / 1.67 / 57 | 5.4% / 1.15 / 55 | 1.2% / 0.24 / 73 |
| 151 | 2.4% / 1.11 / 29 | 1.3% / 0.84 / 22 | 3.4% / 1.13 / 24 | 1.0% / 0.38 / 21 | 2.0% / 0.58 / 32 |
| 152 | 0.2% / 0.12 / 37 | 1.1% / 0.76 / 23 | 5.3% / 1.76 / 27 | 1.1% / 0.44 / 25 | 2.7% / 0.72 / 39 |
| 153 | -0.7% / -0.15 / 89 | -1.3% / -0.50 / 66 | 14.6% / 2.29 / 65 | 6.9% / 1.46 / 60 | 0.1% / 0.05 / 80 |
| 154 | 2.9% / 1.24 / 61 | 2.9% / 1.11 / 50 | 3.2% / 0.67 / 47 | 2.2% / 0.48 / 52 | 4.9% / 1.04 / 61 |
| 155 | 5.4% / 1.85 / 43 | 0.7% / 0.35 / 31 | 6.8% / 1.44 / 33 | 0.6% / 0.16 / 27 | 2.5% / 0.62 / 46 |
| 156 | -0.2% / -0.14 / 27 | 0.1% / 0.18 / 17 | 5.2% / 2.17 / 14 | 1.4% / 0.58 / 19 | 2.0% / 0.80 / 24 |
| 157 | 0.4% / 0.16 / 77 | 0.9% / 0.35 / 62 | 11.8% / 2.06 / 59 | 3.9% / 0.86 / 57 | 1.6% / 0.38 / 72 |
| 158 | 4.8% / 1.66 / 54 | -2.4% / -1.13 / 41 | 9.5% / 1.76 / 40 | 1.8% / 0.49 / 31 | 2.1% / 0.47 / 55 |
| 159 | -2.8% / -0.94 / 73 | -1.0% / -0.36 / 56 | 12.9% / 2.31 / 57 | 3.6% / 0.87 / 55 | 4.5% / 0.91 / 72 |
| 160 | 2.6% / 1.36 / 43 | 1.8% / 0.97 / 32 | 4.7% / 1.11 / 33 | -0.3% / -0.04 / 27 | 3.5% / 1.02 / 46 |
| 161 | 0.6% / 0.58 / 41 | 0.2% / 0.13 / 30 | 5.1% / 2.08 / 30 | 1.1% / 0.43 / 34 | 2.1% / 1.10 / 35 |
| 162 | 1.1% / 0.28 / 68 | 1.2% / 0.38 / 55 | 10.8% / 1.73 / 52 | 2.4% / 0.55 / 48 | 7.4% / 1.33 / 65 |
| 163 | 1.9% / 0.66 / 60 | -0.1% / -0.07 / 36 | 6.9% / 2.14 / 41 | 3.8% / 1.03 / 40 | 1.9% / 0.48 / 56 |
| 164 | -0.9% / -0.21 / 69 | 0.9% / 0.36 / 47 | 13.8% / 2.11 / 61 | 3.7% / 0.97 / 48 | 5.3% / 0.94 / 68 |
| 165 | 3.0% / 1.00 / 47 | 0.3% / 0.13 / 35 | 7.7% / 1.74 / 36 | 0.5% / 0.13 / 32 | 3.7% / 0.76 / 43 |
| 166 | 3.6% / 1.50 / 53 | -1.3% / -0.60 / 41 | 8.8% / 1.69 / 39 | 3.0% / 0.81 / 32 | 0.5% / 0.14 / 54 |
| 167 | 1.1% / 0.32 / 60 | -0.1% / -0.05 / 37 | 9.5% / 2.55 / 50 | 1.1% / 0.37 / 34 | 3.0% / 0.66 / 55 |
| 168 | 3.2% / 1.47 / 32 | 1.3% / 1.13 / 25 | 5.6% / 2.41 / 28 | -1.0% / -0.34 / 28 | 0.4% / 0.12 / 40 |
| 169 | 2.6% / 0.95 / 59 | -1.4% / -0.59 / 41 | 13.7% / 2.35 / 47 | 1.4% / 0.34 / 45 | 1.8% / 0.47 / 56 |
| 170 | 4.7% / 1.38 / 71 | -2.6% / -1.02 / 51 | 11.7% / 2.22 / 54 | 0.5% / 0.13 / 56 | 2.6% / 0.53 / 73 |
| 171 | -2.4% / -0.77 / 73 | -1.1% / -0.39 / 56 | 12.6% / 2.26 / 57 | 3.6% / 0.87 / 55 | 5.1% / 1.03 / 72 |
| 172 | 1.5% / 0.64 / 46 | 1.1% / 0.68 / 31 | 5.7% / 1.93 / 28 | 1.3% / 0.40 / 28 | 3.4% / 0.79 / 48 |
| 173 | 3.7% / 1.49 / 55 | -1.0% / -0.52 / 37 | 10.5% / 1.86 / 40 | 0.4% / 0.11 / 38 | 3.8% / 0.96 / 53 |
| 174 | 3.0% / 0.73 / 56 | 0.1% / 0.04 / 42 | 7.9% / 1.40 / 46 | -0.0% / 0.02 / 42 | 7.8% / 1.44 / 55 |
| 175 | 0.9% / 0.34 / 45 | 0.5% / 0.43 / 23 | 7.5% / 2.69 / 22 | 2.6% / 0.89 / 30 | -0.6% / -0.13 / 44 |
| 176 | 0.9% / 0.27 / 60 | -0.3% / -0.14 / 37 | 9.6% / 2.55 / 50 | 1.4% / 0.45 / 34 | 3.7% / 0.80 / 55 |
| 177 | -0.5% / -0.10 / 69 | 0.9% / 0.37 / 47 | 14.5% / 2.20 / 61 | 3.7% / 0.98 / 47 | 6.0% / 1.07 / 68 |
| 178 | 5.3% / 1.57 / 47 | 0.2% / 0.11 / 35 | 7.3% / 1.61 / 36 | 0.9% / 0.22 / 32 | 3.8% / 0.78 / 43 |
| 179 | 1.3% / 0.32 / 97 | -0.0% / 0.01 / 73 | 13.7% / 1.94 / 69 | 5.1% / 1.05 / 64 | 0.6% / 0.13 / 87 |
| 180 | 2.0% / 0.81 / 40 | -0.7% / -0.60 / 23 | 5.3% / 1.80 / 21 | 2.9% / 0.97 / 27 | 4.8% / 1.25 / 36 |
| 181 | 0.7% / 0.19 / 61 | 1.8% / 0.58 / 45 | 14.6% / 2.12 / 58 | -1.7% / -0.33 / 48 | 6.3% / 1.11 / 62 |
| 182 | 0.8% / 0.30 / 67 | -2.2% / -0.84 / 57 | 10.4% / 1.97 / 53 | 3.3% / 0.77 / 45 | 3.2% / 0.71 / 62 |
| 183 | -1.8% / -0.87 / 42 | 1.1% / 0.71 / 26 | 9.0% / 3.28 / 20 | 1.6% / 0.61 / 27 | 1.1% / 0.29 / 39 |
| 184 | 0.5% / 0.27 / 39 | 1.9% / 1.22 / 25 | 7.7% / 3.19 / 20 | -0.6% / -0.17 / 24 | 1.9% / 0.54 / 31 |
| 185 | 1.1% / 0.37 / 69 | -2.8% / -0.99 / 57 | 9.4% / 1.73 / 55 | 3.9% / 0.96 / 45 | 4.7% / 1.05 / 64 |
| 186 | -1.1% / -0.56 / 42 | 1.3% / 0.82 / 26 | 8.0% / 3.24 / 20 | 1.5% / 0.56 / 27 | 0.9% / 0.24 / 39 |
| 187 | 0.3% / 0.09 / 67 | 1.3% / 0.39 / 54 | 12.9% / 2.05 / 52 | 2.6% / 0.59 / 47 | 7.2% / 1.28 / 65 |
| 188 | 1.3% / 0.32 / 61 | 2.0% / 0.64 / 45 | 15.6% / 2.25 / 58 | -3.4% / -0.69 / 48 | 5.4% / 0.96 / 62 |
| 189 | 4.4% / 1.37 / 58 | -0.9% / -0.37 / 49 | 7.9% / 1.83 / 43 | 2.6% / 0.62 / 40 | 1.1% / 0.25 / 61 |
| 190 | 5.5% / 1.68 / 56 | -1.5% / -0.64 / 46 | 8.8% / 1.97 / 43 | 2.3% / 0.54 / 39 | 0.9% / 0.21 / 61 |
| 191 | 2.7% / 0.65 / 57 | -1.5% / -0.52 / 42 | 14.8% / 2.20 / 48 | 1.1% / 0.26 / 46 | 5.1% / 0.88 / 61 |
| 192 | 0.4% / 0.20 / 39 | 0.1% / 0.07 / 26 | 7.0% / 3.21 / 20 | 0.5% / 0.20 / 24 | 2.0% / 0.57 / 32 |
| 193 | 1.7% / 0.64 / 51 | -1.7% / -0.82 / 40 | 5.2% / 1.25 / 39 | 2.6% / 0.77 / 34 | 5.4% / 1.34 / 49 |
| 194 | 1.3% / 1.06 / 31 | -0.7% / -0.59 / 24 | 3.3% / 1.54 / 24 | 1.1% / 0.42 / 23 | 3.3% / 1.33 / 30 |
| 195 | 3.3% / 0.79 / 57 | -2.2% / -0.80 / 42 | 17.7% / 2.47 / 48 | -2.6% / -0.44 / 47 | 5.0% / 0.90 / 63 |
| 196 | 2.3% / 0.90 / 52 | -4.1% / -1.99 / 43 | 6.7% / 1.57 / 41 | 2.5% / 0.67 / 34 | 6.0% / 1.45 / 48 |
| 197 | 1.9% / 0.98 / 39 | 0.7% / 0.50 / 27 | 5.1% / 1.43 / 33 | 0.3% / 0.14 / 28 | 2.9% / 0.71 / 42 |
| 198 | -0.5% / -0.09 / 89 | -1.6% / -0.60 / 66 | 11.7% / 2.08 / 65 | 7.7% / 1.59 / 60 | 0.4% / 0.11 / 80 |
| 199 | 1.9% / 0.70 / 53 | 1.0% / 0.53 / 36 | 9.2% / 2.52 / 40 | 0.1% / 0.06 / 32 | 1.1% / 0.27 / 43 |
| 200 | 2.2% / 1.10 / 48 | 2.5% / 1.46 / 37 | 4.8% / 1.05 / 38 | 0.7% / 0.19 / 38 | 2.9% / 0.74 / 49 |
| 201 | 1.9% / 0.70 / 53 | 0.7% / 0.41 / 36 | 9.3% / 2.59 / 40 | -0.1% / -0.01 / 32 | 1.0% / 0.26 / 43 |
| 202 | 2.9% / 0.96 / 57 | -0.3% / -0.14 / 35 | 8.3% / 2.73 / 41 | 3.0% / 0.80 / 41 | 0.6% / 0.16 / 59 |
| 203 | 3.4% / 1.10 / 57 | 2.4% / 1.10 / 31 | 8.1% / 2.36 / 38 | 1.0% / 0.27 / 40 | -0.4% / -0.06 / 59 |
| 204 | 3.2% / 1.06 / 54 | 0.5% / 0.26 / 40 | 7.6% / 2.49 / 36 | 0.9% / 0.24 / 38 | 1.5% / 0.38 / 56 |
| 205 | 0.9% / 0.41 / 47 | 0.8% / 0.72 / 37 | 2.4% / 0.72 / 40 | 1.7% / 0.76 / 35 | 5.4% / 1.67 / 51 |
| 206 | 0.7% / 0.52 / 38 | 0.6% / 0.43 / 28 | 4.7% / 2.76 / 17 | -1.6% / -0.69 / 23 | 3.6% / 1.51 / 35 |
| 207 | 0.7% / 0.51 / 38 | 0.5% / 0.38 / 28 | 4.5% / 2.73 / 17 | -1.6% / -0.71 / 22 | 3.7% / 1.53 / 35 |
| 208 | 4.3% / 1.83 / 50 | -1.1% / -0.51 / 39 | 7.0% / 1.55 / 34 | 3.9% / 1.15 / 28 | -1.1% / -0.29 / 48 |
| 209 | 2.6% / 0.85 / 57 | -0.1% / -0.06 / 35 | 8.3% / 2.69 / 41 | 3.3% / 0.86 / 41 | 0.3% / 0.09 / 59 |
| 210 | 2.7% / 1.61 / 27 | 1.5% / 1.15 / 20 | 6.7% / 2.28 / 21 | 1.7% / 0.47 / 23 | -1.2% / -0.29 / 25 |
| 211 | 1.6% / 0.67 / 61 | 2.0% / 0.75 / 50 | 2.9% / 0.62 / 51 | 2.0% / 0.44 / 54 | 6.7% / 1.93 / 63 |
| 212 | 0.6% / 0.21 / 49 | -1.4% / -0.89 / 36 | 7.9% / 1.92 / 37 | 0.1% / 0.04 / 32 | 5.9% / 1.47 / 48 |
| 213 | 0.3% / 0.17 / 47 | 0.7% / 0.60 / 37 | 2.5% / 0.75 / 40 | 1.8% / 0.79 / 35 | 5.3% / 1.64 / 51 |
| 214 | 2.1% / 0.68 / 57 | 2.6% / 1.16 / 31 | 8.3% / 2.38 / 38 | 1.6% / 0.42 / 40 | -0.8% / -0.15 / 59 |
| 215 | 3.8% / 1.91 / 38 | 0.6% / 0.38 / 28 | 5.5% / 1.23 / 34 | -1.2% / -0.30 / 26 | 4.2% / 1.13 / 42 |
| 216 | 5.3% / 1.52 / 61 | -1.3% / -0.48 / 44 | 10.6% / 1.87 / 51 | 0.9% / 0.19 / 51 | 4.4% / 0.81 / 65 |
| 217 | 0.8% / 0.54 / 43 | 1.0% / 0.74 / 28 | 1.4% / 0.52 / 28 | -0.5% / -0.24 / 28 | 6.4% / 1.88 / 43 |
| 218 | 0.8% / 0.57 / 43 | 0.8% / 0.60 / 28 | 1.4% / 0.51 / 28 | -0.6% / -0.25 / 28 | 6.4% / 1.89 / 43 |
| 219 | 1.0% / 0.58 / 48 | 0.2% / 0.13 / 38 | 4.8% / 1.15 / 38 | 2.2% / 0.82 / 38 | 3.2% / 0.95 / 50 |
| 220 | 3.8% / 1.66 / 44 | 1.2% / 0.67 / 31 | 7.1% / 1.50 / 34 | 2.2% / 0.57 / 28 | -0.2% / -0.03 / 46 |
| 221 | 1.3% / 0.35 / 90 | 4.0% / 1.43 / 60 | 12.4% / 2.28 / 73 | 1.3% / 0.31 / 65 | -0.8% / -0.11 / 80 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_3bd7` | 20 | 0.80 | 0.83/0.92 | 0.76/0.91 |
| 1 | `cfg_a9b1` | 7 | 0.86 | 0.89/0.94 | 0.82/0.88 |
| 2 | `cfg_7864` | 10 | 0.86 | 0.87/0.94 | 0.77/0.91 |
| 3 | `cfg_0c93` | 10 | 0.83 | 0.82/0.91 | 0.77/0.87 |
| 4 | `cfg_eafd` | 3 | 0.95 | 0.97/0.98 | 0.99/0.99 |
| 5 | `cfg_c3cb` | 2 | 0.90 | 0.88/0.88 | 0.82/0.82 |
| 6 | `cfg_b16e` | 6 | 0.89 | 0.93/0.93 | 0.83/0.91 |
| 7 | `cfg_459d` | 4 | 0.94 | 0.96/0.98 | 0.94/0.98 |
| 8 | `cfg_1140` | 7 | 0.86 | 0.85/0.89 | 0.68/0.77 |
| 9 | `cfg_3141` | 5 | 0.85 | 0.89/0.93 | 0.81/0.88 |
| 10 | `cfg_eb02` | 8 | 0.89 | 0.89/0.92 | 0.74/0.80 |
| 11 | `cfg_04dc` | 1 | n/a | n/a/n/a | n/a/n/a |
| 12 | `cfg_b58e` | 8 | 0.85 | 0.90/0.94 | 0.82/0.92 |
| 13 | `cfg_5722` | 18 | 0.83 | 0.89/0.93 | 0.77/0.90 |
| 14 | `cfg_a4bd` | 12 | 0.87 | 0.91/0.97 | 0.97/0.99 |
| 15 | `cfg_dc2a` | 15 | 0.81 | 0.88/0.95 | 0.90/0.93 |
| 16 | `cfg_ecc1` | 10 | 0.81 | 0.85/0.90 | 0.91/0.96 |
| 17 | `cfg_f48e` | 8 | 0.81 | 0.87/0.88 | 0.66/0.68 |
| 18 | `cfg_4c21` | 16 | 0.83 | 0.85/0.94 | 0.75/0.95 |
| 19 | `cfg_b367` | 5 | 0.88 | 0.89/0.99 | 0.93/1.00 |
| 20 | `cfg_be8b` | 21 | 0.80 | 0.88/0.93 | 0.79/0.87 |
| 21 | `cfg_3f14` | 9 | 0.89 | 0.92/0.95 | 0.82/0.90 |
| 22 | `cfg_d4b1` | 8 | 0.87 | 0.89/0.92 | 0.83/0.91 |
| 23 | `cfg_0976` | 2 | 0.97 | 0.98/0.98 | 0.98/0.98 |
| 24 | `cfg_d210` | 7 | 0.83 | 0.85/0.95 | 0.73/0.93 |
| 25 | `cfg_c8fc` | 5 | 0.85 | 0.93/0.98 | 0.93/0.99 |
| 26 | `cfg_5277` | 4 | 0.90 | 0.94/0.95 | 0.84/0.86 |
| 27 | `cfg_0a93` | 1 | n/a | n/a/n/a | n/a/n/a |
| 28 | `cfg_d004` | 10 | 0.85 | 0.91/0.93 | 0.80/0.86 |
| 29 | `cfg_9cb0` | 12 | 0.84 | 0.88/0.94 | 0.81/0.91 |
| 30 | `cfg_0bc6` | 6 | 0.90 | 0.93/0.96 | 0.87/0.91 |
| 31 | `cfg_bce1` | 12 | 0.86 | 0.93/0.97 | 0.98/0.98 |
| 32 | `cfg_82d8` | 11 | 0.81 | 0.82/0.92 | 0.62/0.82 |
| 33 | `cfg_f78e` | 10 | 0.82 | 0.90/0.94 | 0.86/0.90 |
| 34 | `cfg_9d13` | 15 | 0.82 | 0.85/0.90 | 0.76/0.90 |
| 35 | `cfg_0e45` | 5 | 0.82 | 0.79/0.99 | 0.64/0.98 |
| 36 | `cfg_4a3b` | 5 | 0.83 | 0.95/0.96 | 0.91/0.94 |
| 37 | `cfg_a5f6` | 4 | 0.89 | 0.95/0.97 | 0.88/0.91 |
| 38 | `cfg_ab6e` | 4 | 0.91 | 0.91/0.95 | 0.84/0.89 |
| 39 | `cfg_8a0f` | 12 | 0.87 | 0.96/0.97 | 0.92/0.93 |
| 40 | `cfg_b497` | 16 | 0.81 | 0.93/0.96 | 0.87/0.94 |
| 41 | `cfg_2add` | 4 | 0.92 | 0.96/0.98 | 0.93/0.96 |
| 42 | `cfg_66f0` | 9 | 0.84 | 0.90/0.93 | 0.80/0.88 |
| 43 | `cfg_f281` | 7 | 0.89 | 0.95/0.97 | 0.94/0.94 |
| 44 | `cfg_11f9` | 2 | 0.86 | 0.89/0.89 | 0.85/0.85 |
| 45 | `cfg_b669` | 8 | 0.86 | 0.87/0.91 | 0.82/0.85 |
| 46 | `cfg_dd3a` | 5 | 0.84 | 0.88/0.91 | 0.72/0.79 |
| 47 | `cfg_6b59` | 10 | 0.82 | 0.83/0.95 | 0.67/0.91 |
| 48 | `cfg_e6dc` | 2 | 0.90 | 0.92/0.92 | 0.89/0.89 |
| 49 | `cfg_ee3e` | 4 | 0.95 | 0.97/0.98 | 0.92/0.95 |
| 50 | `cfg_a1e5` | 9 | 0.89 | 0.90/0.93 | 0.84/0.92 |
| 51 | `cfg_a8f2` | 6 | 0.89 | 0.91/0.94 | 0.83/0.89 |
| 52 | `cfg_1817` | 11 | 0.85 | 0.90/0.95 | 0.86/0.93 |
| 53 | `cfg_4dc3` | 3 | 0.82 | 0.84/0.84 | 0.68/0.70 |
| 54 | `cfg_ad59` | 14 | 0.82 | 0.86/0.89 | 0.68/0.75 |
| 55 | `cfg_ef4c` | 12 | 0.85 | 0.89/0.96 | 0.74/0.87 |
| 56 | `cfg_f3df` | 2 | 0.97 | 0.96/0.96 | 0.94/0.94 |
| 57 | `cfg_fa55` | 4 | 0.91 | 0.94/0.96 | 0.92/0.94 |
| 58 | `cfg_ce90` | 4 | 0.95 | 0.97/0.99 | 0.97/0.98 |
| 59 | `cfg_8389` | 7 | 0.88 | 0.93/0.95 | 0.92/0.94 |
| 60 | `cfg_fea1` | 7 | 0.85 | 0.92/0.95 | 0.84/0.91 |
| 61 | `cfg_326c` | 4 | 0.91 | 0.94/0.95 | 0.90/0.93 |
| 62 | `cfg_a901` | 8 | 0.81 | 0.81/0.91 | 0.60/0.82 |
| 63 | `cfg_ca39` | 3 | 0.93 | 0.92/0.94 | 0.85/0.90 |
| 64 | `cfg_b810` | 7 | 0.89 | 0.93/0.96 | 0.87/0.93 |
| 65 | `cfg_6484` | 4 | 0.94 | 0.96/0.98 | 0.94/0.96 |
| 66 | `cfg_2467` | 4 | 0.81 | 0.80/0.94 | 0.66/0.89 |
| 67 | `cfg_351f` | 3 | 0.85 | 0.95/0.97 | 0.92/0.95 |
| 68 | `cfg_a7f9` | 9 | 0.87 | 0.91/0.95 | 0.86/0.93 |
| 69 | `cfg_f411` | 5 | 0.83 | 0.95/0.97 | 0.95/0.96 |
| 70 | `cfg_3971` | 9 | 0.90 | 0.89/0.94 | 0.89/0.92 |
| 71 | `cfg_f226` | 12 | 0.83 | 0.89/0.94 | 0.75/0.82 |
| 72 | `cfg_d52d` | 7 | 0.86 | 0.92/0.93 | 0.77/0.85 |
| 73 | `cfg_311a` | 6 | 0.82 | 0.91/0.94 | 0.86/0.90 |
| 74 | `cfg_4a3c` | 4 | 0.89 | 0.89/0.94 | 0.79/0.87 |
| 75 | `cfg_3f34` | 6 | 0.82 | 0.87/0.93 | 0.73/0.85 |
| 76 | `cfg_368a` | 5 | 0.90 | 0.94/0.98 | 0.97/0.98 |
| 77 | `cfg_ef5a` | 3 | 0.93 | 0.98/0.98 | 0.95/0.95 |
| 78 | `cfg_f095` | 3 | 0.96 | 0.96/0.97 | 0.92/0.94 |
| 79 | `cfg_384f` | 1 | n/a | n/a/n/a | n/a/n/a |
| 80 | `cfg_da0c` | 5 | 0.82 | 0.86/0.95 | 0.82/0.94 |
| 81 | `cfg_7139` | 4 | 0.99 | 0.98/0.99 | 0.98/0.99 |
| 82 | `cfg_956f` | 5 | 0.87 | 0.92/0.94 | 0.84/0.88 |
| 83 | `cfg_3e3d` | 2 | 0.90 | 0.95/0.95 | 0.98/0.98 |
| 84 | `cfg_6718` | 8 | 0.83 | 0.89/0.93 | 0.88/0.91 |
| 85 | `cfg_3edb` | 3 | 0.89 | 0.92/0.95 | 0.77/0.85 |
| 86 | `cfg_a956` | 11 | 0.83 | 0.88/0.93 | 0.78/0.83 |
| 87 | `cfg_6a19` | 2 | 0.92 | 0.94/0.94 | 0.87/0.87 |
| 88 | `cfg_e87b` | 8 | 0.88 | 0.95/0.96 | 0.89/0.92 |
| 89 | `cfg_4e44` | 6 | 0.82 | 0.80/0.88 | 0.70/0.79 |
| 90 | `cfg_d787` | 4 | 0.95 | 0.96/0.97 | 0.87/0.95 |
| 91 | `cfg_50f4` | 2 | 0.99 | 0.99/0.99 | 0.98/0.98 |
| 92 | `cfg_5108` | 1 | n/a | n/a/n/a | n/a/n/a |
| 93 | `cfg_fa7c` | 4 | 0.92 | 0.96/0.97 | 0.95/0.98 |
| 94 | `cfg_ac0e` | 12 | 0.81 | 0.76/0.87 | 0.52/0.69 |
| 95 | `cfg_6f33` | 3 | 0.81 | 0.78/0.88 | 0.65/0.82 |
| 96 | `cfg_f355` | 3 | 0.94 | 0.98/0.98 | 0.96/0.97 |
| 97 | `cfg_90db` | 5 | 0.85 | 0.89/0.97 | 0.85/0.95 |
| 98 | `cfg_f2d9` | 4 | 0.87 | 0.87/0.92 | 0.75/0.89 |
| 99 | `cfg_79ff` | 4 | 0.95 | 0.98/0.99 | 0.96/0.98 |
| 100 | `cfg_8206` | 6 | 0.80 | 0.90/0.96 | 0.78/0.92 |
| 101 | `cfg_d88c` | 8 | 0.90 | 0.89/0.93 | 0.89/0.91 |
| 102 | `cfg_b06d` | 5 | 0.83 | 0.83/0.96 | 0.75/0.91 |
| 103 | `cfg_6b7d` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 104 | `cfg_d82b` | 7 | 0.86 | 0.94/0.96 | 0.88/0.91 |
| 105 | `cfg_80eb` | 4 | 0.97 | 0.98/0.99 | 0.92/0.96 |
| 106 | `cfg_843b` | 1 | n/a | n/a/n/a | n/a/n/a |
| 107 | `cfg_fb50` | 3 | 0.96 | 0.97/0.98 | 0.94/0.95 |
| 108 | `cfg_8c0e` | 1 | n/a | n/a/n/a | n/a/n/a |
| 109 | `cfg_a10d` | 4 | 0.95 | 0.98/0.98 | 0.97/0.98 |
| 110 | `cfg_956a` | 1 | n/a | n/a/n/a | n/a/n/a |
| 111 | `cfg_c2e8` | 1 | n/a | n/a/n/a | n/a/n/a |
| 112 | `cfg_d3d1` | 3 | 0.90 | 0.92/0.92 | 0.83/0.84 |
| 113 | `cfg_d520` | 2 | 0.95 | 0.97/0.97 | 0.95/0.95 |
| 114 | `cfg_e406` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 8.993e-04 over 19968 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 780.0, participation ratio 9.8, 95%-variance components 183 (rank bound T = 1239); raw grid 21504; raw + known prior 712008
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
