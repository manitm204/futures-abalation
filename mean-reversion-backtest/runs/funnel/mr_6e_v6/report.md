# Screening funnel -- mr_6e_v6 (development stages only)

- Code: `7ba1d7ded49f` (dirty working tree: True, diff sha256 `2ae1975346a5`)
- Config: `configs/funnel/mr_funnel_6e_v6.yaml` sha256 `a1a513c3be2b1ca5`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'6E': '2026-10-16', '6J': '2026-10-16'}
- Frozen manifest sha256: `f7dbc2f72fdedd93` (252 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_6e_v5 gated 2 6E candidates on 2023-2024 (both failed, Sharpe about -0.55) and this grid was written after reading those results, so 6E 2023-2024 is partly in-sample here.
- Holdout 2025+ previously inspected: **False** -- No 6E strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection). The index, crude and gold holdouts (ES/NQ/YM/RTY/CL/GC) have been scored (other markets).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 24000 | 24000 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 24000 | 24000 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 24000 | 24000 | 0 | 0 |  | 21644 | 100.00 | 100.00 |  |
| 3 performance & risk | hard_gate | 24000 | 1053 | 22947 | 0 |  | 0 | 4.39 | 4.39 |  |
| 4 parameter stability | hard_gate | 1053 | 1018 | 35 | 0 |  | 0 | 4.24 | 96.68 |  |
| 5 time stability | hard_gate | 1018 | 970 | 48 | 0 |  | 288 | 4.04 | 95.28 |  |
| 6 deduplication | dedup | 970 | 252 |  |  | 718 |  | 1.05 | 25.98 | best 2 per cluster |
| 7 execution stress | hard_gate | 252 | 252 | 0 | 0 |  | 21 | 1.05 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 252 |  |  |  |  |  |  |  | diagnostic only: unverified: 252 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s3:hard_reject:net_return | 11883 |
| s3:hard_reject:sharpe | 22947 |
| s4:hard_reject:local_median_sharpe | 35 |
| s5:hard_reject:profitable_years | 48 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | 6J dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_6cbf` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-2.25, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 49/141/0 | 190 | 11.8% | 2.3% | 1.28 | -2.0% | 172 | 1.74 | 10.1% | 79.5 | 10/10 | 1.00 | 1.20 | 0.09 | 5 | 6.2% | 0.47 | 0.36 | 10.5% | 9.1% | 5.0% | 10.2%/8.3% | 5.9 (interpolated) | pass | 0.327 (unverified) | -0.15 |
| 2 | `cfg_fbc4` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-2.25, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 26/161/0 | 187 | 12.5% | 2.4% | 1.29 | -2.1% | 225 | 1.80 | 10.3% | 78.5 | 11/11 | 1.00 | 1.19 | 0.10 | 5 | 7.0% | 0.43 | 0.36 | 10.9% | 9.8% | 5.1% | 10.8%/8.9% | 6.3 (interpolated) | pass | 0.328 (unverified) | -0.13 |
| 3 | `cfg_5885` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 43/159/0 | 202 | 13.6% | 2.6% | 1.38 | -1.7% | 323 | 1.87 | 10.8% | 84.7 | 11/11 | 1.00 | 1.21 | 0.17 | 4 | 7.6% | 0.44 | 0.33 | 12.0% | 10.7% | 8.1% | 11.9%/10.0% | 6.5 (interpolated) | pass | 0.410 (unverified) | 0.04 |
| 4 | `cfg_a7ef` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 30/171/0 | 201 | 14.3% | 2.7% | 1.42 | -1.7% | 173 | 1.91 | 11.1% | 84.6 | 11/11 | 1.00 | 1.20 | 0.22 | 4 | 8.4% | 0.41 | 0.33 | 12.9% | 11.1% | 8.2% | 12.5%/10.1% | 6.7 (interpolated) | pass | 0.441 (unverified) | 0.03 |
| 5 | `cfg_e062` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-1.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 31/171/0 | 202 | 13.7% | 2.6% | 1.35 | -2.0% | 246 | 1.74 | 13.2% | 84.5 | 9/9 | 1.00 | 1.11 | 0.24 | 4 | 7.0% | 0.48 | 0.33 | 12.3% | 10.6% | 12.6% | 12.0%/10.0% | 6.4 (interpolated) | pass | 0.384 (unverified) | 0.01 |
| 6 | `cfg_61e8` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 45/153/0 | 198 | 14.0% | 2.7% | 1.25 | -2.2% | 367 | 1.74 | 12.6% | 82.9 | 11/11 | 1.00 | 1.09 | 0.16 | 4 | 7.8% | 0.44 | 0.37 | 12.4% | 11.0% | 7.2% | 11.8%/9.5% | 6.7 (interpolated) | pass | 0.293 (unverified) | 0.02 |
| 7 | `cfg_dd2f` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.25, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 19/164/13 | 196 | 10.9% | 2.1% | 1.20 | -1.5% | 146 | 1.73 | 10.4% | 81.1 | 12/12 | 1.00 | 1.05 | 0.15 | 5 | 4.1% | 0.62 | 0.41 | 9.7% | 8.7% | -1.3% | 9.5%/8.0% | 5.6 (interpolated) | pass | 0.261 (unverified) | -0.62 |
| 8 | `cfg_6dac` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 53/157/0 | 210 | 13.1% | 2.5% | 1.25 | -1.9% | 316 | 1.75 | 11.1% | 88.1 | 11/11 | 1.00 | 1.10 | 0.15 | 4 | 7.2% | 0.45 | 0.32 | 11.7% | 10.3% | 10.0% | 11.6%/9.9% | 6.0 (interpolated) | pass | 0.297 (unverified) | 0.07 |
| 9 | `cfg_bf1d` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.25, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 34/149/13 | 196 | 11.1% | 2.1% | 1.23 | -1.3% | 146 | 1.75 | 10.2% | 81.1 | 12/12 | 1.00 | 1.06 | 0.17 | 5 | 4.2% | 0.62 | 0.38 | 9.8% | 8.7% | -1.0% | 9.7%/8.3% | 5.6 (interpolated) | pass | 0.287 (unverified) | -0.61 |
| 10 | `cfg_d67e` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 64/137/0 | 201 | 13.1% | 2.5% | 1.19 | -2.5% | 324 | 1.68 | 12.4% | 84.0 | 11/11 | 1.00 | 1.07 | 0.12 | 4 | 6.9% | 0.47 | 0.37 | 11.4% | 10.2% | 7.2% | 11.0%/9.6% | 6.3 (interpolated) | pass | 0.253 (unverified) | 0.04 |
| 11 | `cfg_0025` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.0, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 42/155/15 | 212 | 11.4% | 2.2% | 1.20 | -1.8% | 151 | 1.68 | 11.0% | 87.9 | 12/12 | 1.00 | 1.04 | 0.16 | 5 | 5.1% | 0.55 | 0.34 | 10.0% | 8.8% | 1.8% | 10.2%/8.1% | 5.5 (interpolated) | pass | 0.277 (unverified) | -0.31 |
| 12 | `cfg_bd46` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-1.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 86/129/0 | 215 | 10.5% | 2.0% | 1.10 | -2.5% | 546 | 1.57 | 12.4% | 89.0 | 9/9 | 1.00 | 0.89 | 0.21 | 4 | 3.7% | 0.65 | 0.36 | 9.2% | 7.9% | 7.2% | 9.3%/7.5% | 5.1 (interpolated) | pass | 0.183 (unverified) | -0.13 |
| 13 | `cfg_5c3b` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.0, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 19/177/15 | 211 | 11.0% | 2.1% | 1.15 | -1.8% | 151 | 1.65 | 11.2% | 87.6 | 11/11 | 1.00 | 0.98 | 0.17 | 5 | 5.1% | 0.54 | 0.38 | 9.7% | 8.6% | 1.3% | 9.8%/8.3% | 5.4 (interpolated) | pass | 0.240 (unverified) | -0.36 |
| 14 | `cfg_995d` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=12, entry_z=-1.5, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 22/179/10 | 211 | 11.9% | 2.3% | 1.29 | -1.4% | 249 | 1.67 | 11.5% | 88.1 | 9/9 | 1.00 | 1.07 | 0.22 | 4 | 7.3% | 0.37 | 0.38 | 10.3% | 8.9% | 8.3% | 10.4%/8.5% | 5.5 (interpolated) | pass | 0.324 (unverified) | -0.39 |
| 15 | `cfg_ea40` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-1.5, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 50/161/24 | 235 | 11.5% | 2.2% | 1.26 | -1.7% | 323 | 1.60 | 11.9% | 97.8 | 11/11 | 1.00 | 0.97 | 0.29 | 4 | 5.5% | 0.53 | 0.31 | 10.0% | 8.2% | 8.9% | 10.1%/8.3% | 5.0 (interpolated) | pass | 0.304 (unverified) | -0.29 |
| 16 | `cfg_ffdf` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-1.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 32/169/27 | 228 | 13.8% | 2.6% | 1.31 | -1.6% | 228 | 1.66 | 14.1% | 95.2 | 10/10 | 1.00 | 0.96 | 0.34 | 4 | 6.8% | 0.50 | 0.32 | 12.3% | 10.5% | 10.7% | 12.2%/10.1% | 5.9 (interpolated) | pass | 0.339 (unverified) | -0.05 |
| 17 | `cfg_9937` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 87/127/0 | 214 | 12.7% | 2.4% | 1.26 | -2.4% | 241 | 1.68 | 12.5% | 89.2 | 9/9 | 1.00 | 1.01 | 0.25 | 3 | 4.7% | 0.63 | 0.36 | 11.2% | 9.7% | 12.9% | 11.4%/9.8% | 5.8 (interpolated) | pass | 0.298 (unverified) | -0.10 |
| 18 | `cfg_a2ac` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=12, entry_z=-1.5, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 34/168/10 | 212 | 12.1% | 2.3% | 1.33 | -1.4% | 228 | 1.69 | 11.3% | 88.6 | 10/10 | 1.00 | 1.12 | 0.21 | 4 | 7.8% | 0.34 | 0.37 | 10.6% | 9.1% | 8.6% | 10.8%/8.6% | 5.6 (interpolated) | pass | 0.355 (unverified) | -0.40 |
| 19 | `cfg_f0c6` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 37/172/0 | 209 | 13.7% | 2.6% | 1.28 | -1.8% | 313 | 1.78 | 11.3% | 87.7 | 11/11 | 1.00 | 1.04 | 0.24 | 4 | 7.7% | 0.44 | 0.33 | 12.2% | 11.0% | 9.7% | 12.0%/10.1% | 6.3 (interpolated) | pass | 0.319 (unverified) | -0.10 |
| 20 | `cfg_019b` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-1.5, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 24/185/11 | 220 | 11.3% | 2.2% | 1.24 | -1.9% | 259 | 1.61 | 11.9% | 91.4 | 10/10 | 1.00 | 1.00 | 0.24 | 4 | 5.1% | 0.54 | 0.35 | 9.9% | 8.2% | 11.0% | 9.9%/8.1% | 5.3 (interpolated) | pass | 0.287 (unverified) | -0.17 |
| 21 | `cfg_e445` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-1.5, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 75/145/11 | 231 | 10.2% | 2.0% | 1.16 | -2.2% | 361 | 1.56 | 11.4% | 96.1 | 10/10 | 1.00 | 0.94 | 0.22 | 4 | 5.0% | 0.51 | 0.36 | 8.8% | 7.3% | 7.9% | 9.3%/7.7% | 4.7 (interpolated) | pass | 0.221 (unverified) | -0.22 |
| 22 | `cfg_9bfd` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 33/162/0 | 195 | 12.9% | 2.5% | 1.25 | -2.1% | 210 | 1.69 | 12.8% | 81.6 | 9/9 | 1.00 | 1.00 | 0.25 | 4 | 6.1% | 0.53 | 0.38 | 11.2% | 10.0% | 14.9% | 11.5%/9.7% | 6.4 (interpolated) | pass | 0.288 (unverified) | -0.23 |
| 23 | `cfg_6ea4` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.5, exit_z=0.5, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 44/142/0 | 186 | 14.0% | 2.7% | 1.16 | -2.7% | 261 | 1.66 | 13.8% | 77.6 | 9/9 | 1.00 | 0.88 | 0.28 | 4 | 6.6% | 0.53 | 0.35 | 12.8% | 11.4% | 14.6% | 11.9%/10.0% | 7.2 (interpolated) | pass | 0.225 (unverified) | -0.23 |
| 24 | `cfg_544b` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-1.5, exit_z=0.5, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 39/153/0 | 192 | 14.0% | 2.7% | 1.19 | -2.6% | 227 | 1.64 | 14.3% | 79.8 | 9/9 | 1.00 | 0.94 | 0.25 | 4 | 7.6% | 0.43 | 0.32 | 12.7% | 11.2% | 12.3% | 12.2%/9.6% | 6.9 (interpolated) | pass | 0.247 (unverified) | 0.08 |
| 25 | `cfg_46c7` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.5, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=1.5 | 49/137/40 | 226 | 9.9% | 1.9% | 1.04 | -2.0% | 483 | 1.52 | 10.8% | 93.3 | 9/9 | 0.89 | 0.98 | 0.06 | 4 | 4.1% | 0.59 | 0.42 | 8.5% | 7.3% | -1.6% | 8.6%/6.9% | 4.7 (interpolated) | pass | 0.167 (unverified) | -0.69 |
| 26 | `cfg_ad3b` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-1.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 64/137/0 | 201 | 10.8% | 2.1% | 0.99 | -3.4% | 480 | 1.53 | 12.1% | 83.0 | 10/10 | 1.00 | 0.89 | 0.11 | 3 | 4.5% | 0.58 | 0.46 | 9.8% | 8.7% | 3.6% | 10.0%/8.0% | 5.5 (interpolated) | pass | 0.123 (unverified) | -0.01 |
| 27 | `cfg_123b` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=10, entry_z=-1.75, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 30/172/7 | 209 | 10.3% | 2.0% | 1.12 | -2.2% | 349 | 1.58 | 11.3% | 86.9 | 11/11 | 0.91 | 0.92 | 0.20 | 4 | 4.1% | 0.60 | 0.43 | 9.2% | 7.8% | 7.1% | 9.2%/7.3% | 5.3 (interpolated) | pass | 0.198 (unverified) | -0.03 |
| 28 | `cfg_a8ca` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 40/151/20 | 211 | 12.1% | 2.3% | 1.15 | -3.1% | 223 | 1.62 | 13.0% | 88.3 | 12/12 | 1.00 | 0.90 | 0.25 | 5 | 7.5% | 0.37 | 0.36 | 10.8% | 9.5% | 7.3% | 10.8%/8.3% | 5.7 (interpolated) | pass | 0.241 (unverified) | -0.05 |
| 29 | `cfg_8c05` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 68/112/0 | 180 | 12.5% | 2.4% | 0.98 | -2.9% | 282 | 1.51 | 16.0% | 75.0 | 9/9 | 1.00 | 0.88 | 0.11 | 4 | 5.6% | 0.55 | 0.47 | 11.2% | 10.2% | 13.6% | 10.9%/8.6% | 6.7 (interpolated) | pass | 0.132 (unverified) | -0.10 |
| 30 | `cfg_4755` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-2.25, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 21/173/0 | 194 | 11.0% | 2.1% | 1.27 | -1.6% | 176 | 1.80 | 8.7% | 80.5 | 10/10 | 0.90 | 0.93 | 0.34 | 5 | 6.8% | 0.38 | 0.37 | 9.8% | 8.6% | 7.9% | 9.9%/8.3% | 5.7 (interpolated) | pass | 0.300 (unverified) | -0.54 |
| 31 | `cfg_3bef` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 65/131/20 | 216 | 12.7% | 2.4% | 1.21 | -2.8% | 209 | 1.66 | 12.8% | 90.2 | 12/12 | 1.00 | 0.92 | 0.29 | 5 | 7.8% | 0.37 | 0.31 | 11.2% | 10.0% | 7.6% | 11.4%/8.8% | 5.8 (interpolated) | pass | 0.282 (unverified) | 0.03 |
| 32 | `cfg_4a7b` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.25, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 27/170/0 | 197 | 7.6% | 1.5% | 0.91 | -2.2% | 238 | 1.52 | 8.6% | 81.1 | 10/10 | 1.00 | 0.89 | 0.02 | 4 | 3.4% | 0.55 | 0.55 | 6.6% | 5.5% | 3.6% | 7.0%/5.6% | 4.4 (interpolated) | pass | 0.095 (unverified) | -0.84 |
| 33 | `cfg_eb7d` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=10, entry_z=-1.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 70/131/0 | 201 | 14.5% | 2.7% | 1.26 | -1.6% | 289 | 1.72 | 12.2% | 84.1 | 10/10 | 1.00 | 0.99 | 0.27 | 5 | 6.8% | 0.53 | 0.37 | 12.9% | 11.4% | 6.7% | 12.8%/10.9% | 6.8 (interpolated) | pass | 0.298 (unverified) | -0.20 |
| 34 | `cfg_5cd1` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-1.75, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 36/168/26 | 230 | 12.2% | 2.3% | 1.09 | -2.7% | 456 | 1.55 | 11.9% | 96.3 | 12/12 | 1.00 | 0.88 | 0.20 | 4 | 5.0% | 0.55 | 0.39 | 10.4% | 9.3% | 2.6% | 10.0%/8.2% | 5.5 (interpolated) | pass | 0.193 (unverified) | -0.20 |
| 35 | `cfg_a1cf` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.5, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=1.5 | 23/161/40 | 224 | 10.1% | 1.9% | 1.00 | -1.6% | 418 | 1.53 | 11.2% | 93.2 | 10/10 | 1.00 | 0.94 | 0.06 | 5 | 4.7% | 0.54 | 0.46 | 8.8% | 7.4% | -1.4% | 9.0%/7.0% | 4.9 (interpolated) | pass | 0.133 (unverified) | -0.66 |
| 36 | `cfg_62dc` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-1.75, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 25/178/6 | 209 | 8.0% | 1.6% | 0.89 | -3.1% | 219 | 1.45 | 11.3% | 87.2 | 11/11 | 1.00 | 0.85 | 0.04 | 5 | 5.3% | 0.32 | 0.45 | 6.6% | 5.6% | 10.1% | 7.4%/5.9% | 4.2 (interpolated) | pass | 0.118 (unverified) | -0.73 |
| 37 | `cfg_12df` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-1.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 52/147/0 | 199 | 10.8% | 2.1% | 1.00 | -3.2% | 520 | 1.53 | 12.4% | 82.1 | 10/10 | 1.00 | 0.88 | 0.13 | 4 | 4.2% | 0.61 | 0.43 | 9.8% | 8.7% | 2.9% | 10.0%/8.7% | 5.6 (interpolated) | pass | 0.134 (unverified) | 0.07 |
| 38 | `cfg_4223` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.25, exit_z=0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 15/182/0 | 197 | 8.2% | 1.6% | 0.95 | -2.3% | 238 | 1.56 | 8.8% | 81.1 | 9/9 | 1.00 | 0.88 | 0.07 | 4 | 3.5% | 0.58 | 0.55 | 7.2% | 6.0% | 3.3% | 7.6%/6.0% | 4.6 (interpolated) | pass | 0.106 (unverified) | -0.79 |
| 39 | `cfg_dfc2` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-2.25, exit_z=0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 15/177/0 | 192 | 10.6% | 2.0% | 1.23 | -1.5% | 176 | 1.78 | 8.6% | 79.6 | 9/9 | 0.89 | 0.90 | 0.33 | 5 | 6.3% | 0.40 | 0.38 | 9.4% | 8.2% | 6.7% | 9.2%/7.8% | 5.5 (interpolated) | pass | 0.265 (unverified) | -0.52 |
| 40 | `cfg_f26e` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-1.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 42/150/0 | 192 | 9.7% | 1.9% | 0.93 | -3.3% | 522 | 1.49 | 12.3% | 79.9 | 10/10 | 1.00 | 0.87 | 0.06 | 4 | 4.1% | 0.55 | 0.46 | 8.5% | 7.4% | 6.7% | 8.4%/6.6% | 5.3 (interpolated) | pass | 0.106 (unverified) | 0.22 |
| 41 | `cfg_20b3` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-1.75, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 26/177/17 | 220 | 8.9% | 1.7% | 0.97 | -3.1% | 219 | 1.47 | 11.7% | 91.7 | 11/11 | 1.00 | 0.78 | 0.19 | 5 | 6.1% | 0.30 | 0.45 | 7.4% | 6.3% | 10.1% | 7.6%/6.1% | 4.4 (interpolated) | pass | 0.153 (unverified) | -0.83 |
| 42 | `cfg_88ea` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.5, exit_z=0.0, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 55/133/0 | 188 | 10.1% | 1.9% | 0.88 | -3.0% | 385 | 1.46 | 13.7% | 78.5 | 10/10 | 1.00 | 0.90 | -0.02 | 4 | 4.1% | 0.56 | 0.48 | 8.8% | 7.9% | 15.1% | 9.0%/6.9% | 5.6 (interpolated) | pass | 0.082 (unverified) | -0.31 |
| 43 | `cfg_c673` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-2.25, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 52/127/13 | 192 | 9.4% | 1.8% | 0.97 | -2.2% | 436 | 1.57 | 9.8% | 79.7 | 11/11 | 0.91 | 0.83 | 0.14 | 4 | 4.1% | 0.57 | 0.44 | 8.1% | 7.0% | 3.4% | 8.3%/6.7% | 5.4 (interpolated) | pass | 0.139 (unverified) | -0.10 |
| 44 | `cfg_a0b4` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 39/156/0 | 195 | 9.2% | 1.8% | 0.96 | -2.6% | 558 | 1.48 | 12.6% | 80.8 | 11/11 | 1.00 | 0.88 | 0.08 | 3 | 3.7% | 0.57 | 0.49 | 8.0% | 6.9% | 1.1% | 8.2%/6.7% | 5.0 (interpolated) | pass | 0.127 (unverified) | -0.09 |
| 45 | `cfg_02d1` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-1.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 37/155/0 | 192 | 10.0% | 1.9% | 0.95 | -2.8% | 497 | 1.53 | 12.5% | 79.1 | 9/9 | 1.00 | 0.91 | 0.04 | 4 | 3.7% | 0.63 | 0.47 | 9.2% | 8.0% | 10.4% | 8.9%/7.3% | 5.4 (interpolated) | pass | 0.111 (unverified) | 0.36 |
| 46 | `cfg_5c44` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-1.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 47/149/0 | 196 | 10.3% | 2.0% | 0.98 | -2.9% | 497 | 1.53 | 12.5% | 81.4 | 10/10 | 1.00 | 0.94 | 0.05 | 4 | 4.6% | 0.55 | 0.43 | 9.3% | 8.1% | 9.8% | 9.5%/7.3% | 5.6 (interpolated) | pass | 0.129 (unverified) | 0.41 |
| 47 | `cfg_80bc` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=10, entry_z=-1.5, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 54/153/18 | 225 | 11.9% | 2.3% | 1.08 | -1.5% | 291 | 1.56 | 11.5% | 93.6 | 11/11 | 1.00 | 0.89 | 0.19 | 4 | 5.3% | 0.55 | 0.43 | 10.2% | 9.1% | 9.4% | 10.4%/8.3% | 5.4 (interpolated) | pass | 0.171 (unverified) | -0.37 |
| 48 | `cfg_2eaa` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-1.5, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 43/162/25 | 230 | 10.6% | 2.0% | 0.97 | -2.4% | 519 | 1.50 | 11.7% | 95.0 | 11/11 | 1.00 | 0.87 | 0.10 | 3 | 4.1% | 0.61 | 0.43 | 9.2% | 8.0% | 5.4% | 8.8%/7.0% | 4.9 (interpolated) | pass | 0.116 (unverified) | -0.13 |
| 49 | `cfg_2d34` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=12, entry_z=-1.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 25/167/0 | 192 | 11.5% | 2.2% | 1.11 | -2.5% | 249 | 1.60 | 12.5% | 79.9 | 8/8 | 1.00 | 0.95 | 0.16 | 4 | 5.8% | 0.47 | 0.40 | 10.0% | 8.7% | 6.7% | 9.9%/7.9% | 5.9 (interpolated) | pass | 0.195 (unverified) | -0.12 |
| 50 | `cfg_9d5d` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-2.25, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 53/128/0 | 181 | 12.1% | 2.3% | 1.25 | -1.8% | 365 | 1.81 | 9.5% | 75.5 | 10/10 | 1.00 | 0.86 | 0.39 | 5 | 6.5% | 0.47 | 0.35 | 10.9% | 9.5% | 4.4% | 10.5%/8.7% | 6.6 (interpolated) | pass | 0.305 (unverified) | 0.04 |
| 51 | `cfg_7ea2` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-1.75, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 30/173/26 | 229 | 11.6% | 2.2% | 1.04 | -2.7% | 368 | 1.53 | 12.0% | 95.7 | 11/11 | 1.00 | 0.83 | 0.20 | 4 | 4.7% | 0.56 | 0.41 | 10.1% | 8.9% | 2.9% | 9.7%/8.4% | 5.3 (interpolated) | pass | 0.164 (unverified) | -0.20 |
| 52 | `cfg_6d26` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-1.5, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 59/147/25 | 231 | 11.0% | 2.1% | 1.02 | -2.7% | 481 | 1.52 | 11.5% | 95.3 | 11/11 | 1.00 | 0.87 | 0.16 | 3 | 4.7% | 0.57 | 0.45 | 9.5% | 8.4% | 6.1% | 9.5%/7.3% | 5.0 (interpolated) | pass | 0.138 (unverified) | -0.23 |
| 53 | `cfg_4b3b` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 53/123/0 | 176 | 12.0% | 2.3% | 0.94 | -2.8% | 329 | 1.49 | 16.2% | 73.5 | 8/8 | 1.00 | 0.81 | 0.13 | 3 | 5.5% | 0.54 | 0.47 | 10.4% | 9.5% | 12.1% | 10.0%/7.9% | 6.5 (interpolated) | pass | 0.111 (unverified) | -0.14 |
| 54 | `cfg_bceb` | timeframe=1h, mean_type=ema, mean_lookback=90, std_lookback=12, entry_z=-1.5, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 76/143/14 | 233 | 8.3% | 1.6% | 0.90 | -2.8% | 535 | 1.40 | 11.5% | 96.4 | 10/10 | 1.00 | 0.76 | 0.14 | 3 | 2.0% | 0.73 | 0.53 | 7.0% | 5.7% | 3.0% | 7.0%/5.3% | 4.1 (interpolated) | pass | 0.100 (unverified) | -0.53 |
| 55 | `cfg_bc5b` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=12, entry_z=-1.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 75/129/0 | 204 | 9.9% | 1.9% | 1.03 | -1.8% | 249 | 1.51 | 11.9% | 84.8 | 8/8 | 1.00 | 0.91 | 0.12 | 4 | 5.7% | 0.40 | 0.45 | 8.5% | 7.0% | 6.8% | 9.0%/6.8% | 4.9 (interpolated) | pass | 0.151 (unverified) | -0.14 |
| 56 | `cfg_47c9` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=10, entry_z=-1.75, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 17/184/7 | 208 | 10.1% | 1.9% | 1.09 | -2.3% | 260 | 1.56 | 11.5% | 86.0 | 10/10 | 0.90 | 0.87 | 0.22 | 3 | 4.2% | 0.59 | 0.46 | 8.8% | 7.7% | 7.7% | 8.8%/7.2% | 5.1 (interpolated) | pass | 0.181 (unverified) | -0.02 |
| 57 | `cfg_3662` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 29/166/0 | 195 | 9.6% | 1.9% | 0.99 | -2.5% | 534 | 1.49 | 12.8% | 80.8 | 10/10 | 1.00 | 0.77 | 0.22 | 3 | 3.9% | 0.57 | 0.49 | 8.5% | 7.0% | 2.2% | 8.8%/6.8% | 5.2 (interpolated) | pass | 0.139 (unverified) | -0.07 |
| 58 | `cfg_a68c` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=12, entry_z=-1.75, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 28/170/12 | 210 | 8.6% | 1.7% | 0.93 | -3.3% | 546 | 1.45 | 11.2% | 87.3 | 11/11 | 1.00 | 0.87 | 0.06 | 3 | 2.0% | 0.77 | 0.50 | 7.4% | 6.3% | 6.7% | 7.8%/6.2% | 4.7 (interpolated) | pass | 0.109 (unverified) | 0.08 |
| 59 | `cfg_22e3` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-1.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 65/133/0 | 198 | 9.3% | 1.8% | 0.88 | -3.6% | 521 | 1.44 | 12.2% | 82.2 | 10/10 | 1.00 | 0.84 | 0.04 | 4 | 3.6% | 0.59 | 0.45 | 8.2% | 6.9% | 5.2% | 8.2%/6.7% | 5.1 (interpolated) | pass | 0.086 (unverified) | 0.19 |
| 60 | `cfg_f2ab` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=0.0, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 54/132/0 | 186 | 11.1% | 2.1% | 0.88 | -2.7% | 405 | 1.49 | 13.4% | 78.0 | 11/11 | 1.00 | 0.77 | 0.11 | 3 | 6.3% | 0.43 | 0.43 | 9.9% | 8.5% | 8.4% | 9.5%/7.4% | 5.8 (interpolated) | pass | 0.092 (unverified) | -0.15 |
| 61 | `cfg_be54` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=10, entry_z=-1.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 37/148/0 | 185 | 10.0% | 1.9% | 0.98 | -2.5% | 508 | 1.54 | 11.9% | 76.4 | 9/9 | 1.00 | 0.85 | 0.12 | 3 | 4.2% | 0.56 | 0.51 | 8.8% | 7.6% | 8.1% | 8.7%/6.3% | 5.5 (interpolated) | pass | 0.123 (unverified) | 0.36 |
| 62 | `cfg_dd01` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=10, entry_z=-1.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 85/98/0 | 183 | 15.4% | 2.9% | 1.17 | -2.6% | 306 | 1.70 | 14.9% | 76.6 | 9/9 | 1.00 | 0.79 | 0.38 | 4 | 7.1% | 0.54 | 0.37 | 13.7% | 12.2% | 9.8% | 13.6%/10.9% | 7.5 (interpolated) | pass | 0.230 (unverified) | -0.34 |
| 63 | `cfg_e446` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 68/134/0 | 202 | 9.4% | 1.8% | 1.01 | -2.7% | 333 | 1.51 | 12.3% | 83.4 | 10/10 | 1.00 | 0.81 | 0.20 | 4 | 2.8% | 0.70 | 0.41 | 8.3% | 7.1% | 6.8% | 8.6%/6.7% | 4.9 (interpolated) | pass | 0.138 (unverified) | -0.30 |
| 64 | `cfg_da60` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-1.75, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 61/148/0 | 209 | 8.8% | 1.7% | 0.97 | -3.3% | 649 | 1.50 | 10.8% | 86.9 | 10/10 | 1.00 | 0.85 | 0.13 | 4 | 3.0% | 0.66 | 0.48 | 7.6% | 6.5% | 5.1% | 8.1%/6.7% | 4.7 (interpolated) | pass | 0.123 (unverified) | -0.34 |
| 65 | `cfg_df08` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.5, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 71/151/0 | 222 | 8.7% | 1.7% | 0.95 | -2.2% | 241 | 1.46 | 11.2% | 92.4 | 9/9 | 1.00 | 0.85 | 0.11 | 3 | 3.7% | 0.58 | 0.48 | 7.3% | 6.1% | 14.0% | 7.8%/6.3% | 4.3 (interpolated) | pass | 0.115 (unverified) | -0.35 |
| 66 | `cfg_6fb4` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=12, entry_z=-1.75, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 17/180/12 | 209 | 8.2% | 1.6% | 0.88 | -3.4% | 541 | 1.43 | 11.3% | 87.0 | 10/10 | 1.00 | 0.82 | 0.06 | 3 | 1.9% | 0.77 | 0.55 | 7.0% | 5.9% | 6.9% | 7.5%/5.7% | 4.6 (interpolated) | pass | 0.089 (unverified) | 0.11 |
| 67 | `cfg_d442` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-1.75, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 46/138/26 | 210 | 11.0% | 2.1% | 1.04 | -3.2% | 496 | 1.56 | 10.6% | 86.3 | 12/12 | 1.00 | 0.83 | 0.20 | 3 | 4.5% | 0.59 | 0.46 | 9.6% | 8.7% | 4.9% | 9.2%/7.2% | 5.5 (interpolated) | pass | 0.141 (unverified) | -0.13 |
| 68 | `cfg_0ca4` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-1.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 66/118/0 | 184 | 13.3% | 2.5% | 1.04 | -3.3% | 398 | 1.55 | 16.3% | 76.5 | 9/9 | 1.00 | 0.81 | 0.23 | 4 | 7.5% | 0.44 | 0.42 | 12.1% | 10.4% | 8.9% | 11.4%/8.5% | 6.9 (interpolated) | pass | 0.162 (unverified) | 0.23 |
| 69 | `cfg_ff35` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-1.75, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 42/161/0 | 203 | 9.6% | 1.8% | 1.07 | -2.9% | 612 | 1.55 | 10.9% | 84.4 | 11/11 | 1.00 | 0.88 | 0.19 | 4 | 4.2% | 0.56 | 0.46 | 8.2% | 6.9% | 5.8% | 8.5%/6.8% | 5.0 (interpolated) | pass | 0.181 (unverified) | -0.29 |
| 70 | `cfg_7b17` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 38/153/0 | 191 | 8.7% | 1.7% | 0.93 | -3.0% | 602 | 1.48 | 12.4% | 78.4 | 11/11 | 1.00 | 0.76 | 0.17 | 3 | 3.1% | 0.64 | 0.46 | 7.5% | 6.4% | 4.1% | 8.1%/5.9% | 4.8 (interpolated) | pass | 0.110 (unverified) | -0.43 |
| 71 | `cfg_dd35` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=10, entry_z=-1.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 47/139/26 | 212 | 9.3% | 1.8% | 0.93 | -2.3% | 509 | 1.42 | 12.8% | 87.6 | 11/11 | 1.00 | 0.77 | 0.16 | 3 | 3.7% | 0.57 | 0.53 | 8.0% | 6.9% | 4.5% | 7.9%/6.0% | 4.6 (interpolated) | pass | 0.098 (unverified) | 0.29 |
| 72 | `cfg_34ef` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=12, entry_z=-1.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 26/165/28 | 219 | 10.1% | 1.9% | 0.93 | -2.6% | 249 | 1.46 | 13.5% | 91.2 | 9/9 | 1.00 | 0.86 | 0.07 | 4 | 4.8% | 0.50 | 0.46 | 8.6% | 7.1% | 4.4% | 8.6%/6.7% | 4.8 (interpolated) | pass | 0.107 (unverified) | -0.05 |
| 73 | `cfg_7a6e` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=10, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 36/157/0 | 193 | 9.5% | 1.8% | 0.97 | -2.9% | 352 | 1.51 | 12.5% | 80.1 | 10/10 | 1.00 | 0.89 | 0.08 | 4 | 3.9% | 0.59 | 0.49 | 8.1% | 7.1% | 4.6% | 8.6%/6.3% | 5.1 (interpolated) | pass | 0.120 (unverified) | -0.02 |
| 74 | `cfg_d56a` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 64/135/0 | 199 | 9.2% | 1.8% | 0.97 | -2.6% | 379 | 1.49 | 12.1% | 82.5 | 9/9 | 1.00 | 0.84 | 0.13 | 3 | 3.5% | 0.62 | 0.49 | 7.8% | 6.8% | 5.3% | 8.3%/6.4% | 4.8 (interpolated) | pass | 0.123 (unverified) | -0.29 |
| 75 | `cfg_b1c3` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-1.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 72/108/0 | 180 | 14.0% | 2.7% | 1.04 | -2.1% | 366 | 1.62 | 15.4% | 75.5 | 9/9 | 1.00 | 0.66 | 0.39 | 5 | 6.9% | 0.51 | 0.39 | 11.9% | 10.6% | 8.4% | 11.8%/9.7% | 7.2 (interpolated) | pass | 0.160 (unverified) | -0.11 |
| 76 | `cfg_8c09` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=10, entry_z=-1.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 51/120/0 | 171 | 15.0% | 2.8% | 1.09 | -2.2% | 458 | 1.66 | 15.6% | 71.1 | 8/8 | 1.00 | 0.70 | 0.38 | 5 | 5.3% | 0.65 | 0.39 | 13.7% | 12.3% | 9.0% | 13.6%/11.0% | 8.2 (interpolated) | pass | 0.177 (unverified) | -0.23 |
| 77 | `cfg_f3ad` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=12, entry_z=-1.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 41/151/28 | 220 | 9.5% | 1.8% | 0.89 | -2.6% | 336 | 1.43 | 13.2% | 91.7 | 10/10 | 1.00 | 0.84 | 0.05 | 4 | 5.1% | 0.45 | 0.47 | 8.1% | 6.6% | 5.1% | 8.3%/6.4% | 4.6 (interpolated) | pass | 0.093 (unverified) | -0.07 |
| 78 | `cfg_7e2e` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=10, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 55/131/0 | 186 | 10.7% | 2.1% | 1.02 | -2.5% | 437 | 1.58 | 11.5% | 77.1 | 11/11 | 1.00 | 0.84 | 0.18 | 4 | 4.9% | 0.51 | 0.49 | 9.6% | 8.5% | 2.6% | 9.5%/7.0% | 5.9 (interpolated) | pass | 0.136 (unverified) | 0.07 |
| 79 | `cfg_d81a` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.5, exit_z=-1.0, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 95/114/0 | 209 | 11.9% | 2.3% | 1.04 | -3.1% | 414 | 1.55 | 13.5% | 87.0 | 9/9 | 1.00 | 0.82 | 0.22 | 3 | 4.0% | 0.66 | 0.39 | 10.7% | 9.4% | 14.8% | 10.2%/8.4% | 5.7 (interpolated) | pass | 0.153 (unverified) | -0.19 |
| 80 | `cfg_63a1` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 86/102/0 | 188 | 10.7% | 2.1% | 0.88 | -3.2% | 407 | 1.43 | 15.7% | 78.4 | 9/9 | 1.00 | 0.81 | 0.07 | 3 | 5.5% | 0.49 | 0.48 | 9.4% | 8.2% | 10.8% | 9.5%/7.3% | 5.6 (interpolated) | pass | 0.092 (unverified) | 0.00 |
| 81 | `cfg_7fac` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.5, exit_z=0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.5 | 18/188/8 | 214 | 10.4% | 2.0% | 1.13 | -1.1% | 238 | 1.69 | 9.4% | 89.3 | 9/9 | 1.00 | 0.88 | 0.25 | 5 | 5.8% | 0.44 | 0.43 | 9.0% | 7.5% | 1.0% | 9.1%/7.3% | 5.1 (interpolated) | pass | 0.193 (unverified) | -0.88 |
| 82 | `cfg_2a8f` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.5 | 21/185/8 | 214 | 10.1% | 1.9% | 1.11 | -1.1% | 238 | 1.67 | 9.3% | 89.3 | 10/10 | 1.00 | 0.89 | 0.21 | 5 | 5.6% | 0.45 | 0.44 | 8.5% | 7.1% | 0.9% | 8.6%/6.8% | 4.9 (interpolated) | pass | 0.181 (unverified) | -0.84 |
| 83 | `cfg_12f2` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 44/168/0 | 212 | 7.4% | 1.4% | 0.80 | -2.2% | 278 | 1.46 | 9.2% | 87.4 | 9/9 | 1.00 | 0.75 | 0.05 | 5 | 2.8% | 0.62 | 0.57 | 6.2% | 5.0% | 5.3% | 6.7%/5.2% | 3.9 (interpolated) | pass | 0.067 (unverified) | -1.05 |
| 84 | `cfg_49d0` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=10, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 42/142/0 | 184 | 9.4% | 1.8% | 0.91 | -3.1% | 522 | 1.51 | 11.7% | 75.3 | 11/11 | 1.00 | 0.80 | 0.11 | 3 | 4.1% | 0.56 | 0.50 | 8.2% | 7.2% | 1.7% | 8.3%/6.7% | 5.4 (interpolated) | pass | 0.091 (unverified) | 0.09 |
| 85 | `cfg_13a7` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-1.75, exit_z=0.5, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 43/139/0 | 182 | 11.1% | 2.1% | 0.88 | -2.7% | 396 | 1.50 | 13.4% | 76.0 | 10/10 | 1.00 | 0.79 | 0.09 | 4 | 6.3% | 0.44 | 0.43 | 10.1% | 8.6% | 7.7% | 9.7%/7.0% | 5.9 (interpolated) | pass | 0.091 (unverified) | -0.25 |
| 86 | `cfg_fe98` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.5, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 71/150/22 | 243 | 8.4% | 1.6% | 0.91 | -2.0% | 239 | 1.40 | 11.9% | 101.0 | 10/10 | 1.00 | 0.85 | 0.06 | 3 | 3.0% | 0.64 | 0.51 | 7.0% | 5.5% | 11.6% | 7.4%/6.0% | 3.9 (interpolated) | pass | 0.091 (unverified) | -0.27 |
| 87 | `cfg_f77f` | timeframe=1h, mean_type=ema, mean_lookback=90, std_lookback=10, entry_z=-1.5, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 76/153/0 | 229 | 8.0% | 1.5% | 0.85 | -2.4% | 576 | 1.40 | 11.4% | 94.5 | 9/9 | 1.00 | 0.78 | 0.07 | 3 | 1.8% | 0.78 | 0.55 | 6.7% | 5.3% | 6.3% | 7.3%/5.3% | 3.8 (interpolated) | pass | 0.084 (unverified) | -0.43 |
| 88 | `cfg_bf3a` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-1.5, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 80/134/25 | 239 | 10.9% | 2.1% | 1.03 | -2.2% | 412 | 1.51 | 11.4% | 99.3 | 10/10 | 1.00 | 0.85 | 0.19 | 4 | 5.7% | 0.45 | 0.42 | 9.3% | 7.8% | 2.4% | 9.2%/7.1% | 4.8 (interpolated) | pass | 0.147 (unverified) | -0.23 |
| 89 | `cfg_eb6d` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-2.25, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.5 | 37/148/10 | 195 | 8.4% | 1.6% | 0.91 | -2.3% | 417 | 1.53 | 8.3% | 80.7 | 10/10 | 1.00 | 0.74 | 0.17 | 4 | 3.4% | 0.59 | 0.47 | 7.3% | 6.2% | 3.7% | 7.4%/5.9% | 4.9 (interpolated) | pass | 0.110 (unverified) | 0.07 |
| 90 | `cfg_c34b` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 53/143/0 | 196 | 9.1% | 1.8% | 0.98 | -2.5% | 313 | 1.50 | 12.4% | 81.2 | 11/11 | 1.00 | 0.80 | 0.18 | 4 | 3.6% | 0.60 | 0.43 | 7.9% | 6.7% | 5.5% | 8.2%/6.6% | 4.9 (interpolated) | pass | 0.129 (unverified) | -0.29 |
| 91 | `cfg_12b7` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=8, entry_z=-1.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 42/144/0 | 186 | 8.8% | 1.7% | 0.96 | -1.7% | 355 | 1.49 | 11.7% | 77.2 | 10/10 | 1.00 | 0.71 | 0.25 | 3 | 3.4% | 0.60 | 0.58 | 7.6% | 6.6% | 7.3% | 7.6%/5.7% | 4.8 (interpolated) | pass | 0.121 (unverified) | 0.29 |
| 92 | `cfg_5632` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 21/174/9 | 204 | 8.1% | 1.6% | 0.92 | -2.2% | 312 | 1.46 | 11.1% | 84.7 | 11/11 | 0.91 | 0.80 | 0.11 | 3 | 3.4% | 0.58 | 0.55 | 6.7% | 5.7% | 6.3% | 6.8%/5.0% | 4.4 (interpolated) | pass | 0.094 (unverified) | -0.16 |
| 93 | `cfg_81a3` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=12, entry_z=-1.5, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 29/147/8 | 184 | 7.5% | 1.5% | 0.86 | -2.1% | 285 | 1.45 | 9.9% | 76.6 | 10/10 | 1.00 | 0.73 | 0.12 | 4 | 2.5% | 0.64 | 0.60 | 6.2% | 5.1% | 6.7% | 6.6%/4.8% | 4.5 (interpolated) | pass | 0.073 (unverified) | -0.94 |
| 94 | `cfg_96ad` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-1.75, exit_z=-0.5, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 70/120/0 | 190 | 9.9% | 1.9% | 0.89 | -2.6% | 289 | 1.48 | 13.0% | 79.0 | 11/11 | 1.00 | 0.78 | 0.11 | 5 | 6.4% | 0.35 | 0.35 | 8.9% | 7.8% | 11.8% | 9.0%/7.2% | 5.3 (interpolated) | pass | 0.101 (unverified) | -0.02 |
| 95 | `cfg_cfdf` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-1.5, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 80/136/0 | 216 | 10.2% | 2.0% | 0.99 | -2.6% | 412 | 1.54 | 10.7% | 89.3 | 9/9 | 1.00 | 0.89 | 0.10 | 3 | 5.0% | 0.51 | 0.43 | 8.8% | 7.5% | 5.6% | 9.3%/7.5% | 5.1 (interpolated) | pass | 0.123 (unverified) | -0.21 |
| 96 | `cfg_33e3` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-1.75, exit_z=0.5, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 41/139/0 | 180 | 10.4% | 2.0% | 0.92 | -2.8% | 145 | 1.54 | 13.4% | 74.6 | 10/10 | 1.00 | 0.76 | 0.16 | 5 | 6.7% | 0.36 | 0.39 | 9.3% | 8.3% | 11.1% | 9.1%/7.4% | 5.8 (interpolated) | pass | 0.112 (unverified) | -0.09 |
| 97 | `cfg_9e05` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-1.75, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 55/119/0 | 174 | 11.4% | 2.2% | 0.89 | -2.4% | 416 | 1.49 | 15.9% | 72.0 | 9/9 | 1.00 | 0.68 | 0.20 | 4 | 5.3% | 0.54 | 0.46 | 10.3% | 9.3% | 13.6% | 10.7%/9.0% | 6.5 (interpolated) | pass | 0.091 (unverified) | -0.60 |
| 98 | `cfg_67a4` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=6, entry_z=-2.25, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 71/116/0 | 187 | 12.1% | 2.3% | 0.89 | -4.5% | 415 | 1.47 | 16.2% | 77.4 | 9/9 | 1.00 | 0.59 | 0.30 | 4 | 4.9% | 0.60 | 0.50 | 10.8% | 9.8% | 10.9% | 11.1%/8.8% | 6.5 (interpolated) | pass | 0.091 (unverified) | -0.12 |
| 99 | `cfg_10c7` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=12, entry_z=-1.5, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 37/141/7 | 185 | 7.3% | 1.4% | 0.85 | -2.1% | 285 | 1.45 | 9.7% | 77.2 | 10/10 | 1.00 | 0.68 | 0.17 | 4 | 2.1% | 0.69 | 0.61 | 6.0% | 5.0% | 7.0% | 6.1%/4.2% | 4.4 (interpolated) | pass | 0.072 (unverified) | -1.00 |
| 100 | `cfg_d1c0` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=10, entry_z=-1.5, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=1.5 | 53/149/51 | 253 | 9.5% | 1.8% | 0.89 | -3.1% | 630 | 1.41 | 12.3% | 103.4 | 10/10 | 1.00 | 0.73 | 0.16 | 3 | 3.2% | 0.66 | 0.48 | 8.1% | 6.7% | 7.3% | 8.9%/6.9% | 4.1 (interpolated) | pass | 0.085 (unverified) | -0.57 |
| 101 | `cfg_881b` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=12, entry_z=-1.5, exit_z=0.0, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 48/139/0 | 187 | 8.6% | 1.7% | 0.79 | -3.8% | 442 | 1.38 | 13.5% | 77.6 | 9/9 | 1.00 | 0.80 | -0.01 | 4 | 3.2% | 0.59 | 0.54 | 7.3% | 6.2% | 8.0% | 7.6%/5.4% | 4.9 (interpolated) | pass | 0.058 (unverified) | -0.10 |
| 102 | `cfg_b53b` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=10, entry_z=-1.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 91/118/0 | 209 | 10.9% | 2.1% | 0.99 | -1.9% | 458 | 1.52 | 12.0% | 87.0 | 9/9 | 1.00 | 0.85 | 0.15 | 4 | 5.2% | 0.53 | 0.43 | 9.3% | 8.5% | 6.5% | 10.2%/8.1% | 5.4 (interpolated) | pass | 0.129 (unverified) | -0.13 |
| 103 | `cfg_cf11` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.5 | 23/188/4 | 215 | 7.6% | 1.5% | 0.83 | -3.1% | 230 | 1.47 | 9.6% | 88.5 | 11/11 | 1.00 | 0.77 | 0.06 | 5 | 4.8% | 0.37 | 0.54 | 6.2% | 5.0% | 10.1% | 6.6%/4.8% | 4.0 (interpolated) | pass | 0.071 (unverified) | -0.51 |
| 104 | `cfg_1d68` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.0, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.5 | 31/179/8 | 218 | 8.0% | 1.5% | 0.87 | -2.4% | 296 | 1.48 | 9.4% | 90.2 | 11/11 | 1.00 | 0.77 | 0.09 | 5 | 3.3% | 0.58 | 0.57 | 6.7% | 5.4% | 5.6% | 7.0%/5.6% | 4.0 (interpolated) | pass | 0.087 (unverified) | -0.89 |
| 105 | `cfg_129d` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-1.5, exit_z=-1.0, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 93/119/0 | 212 | 9.0% | 1.7% | 0.82 | -3.1% | 572 | 1.39 | 13.6% | 87.0 | 9/9 | 1.00 | 0.70 | 0.12 | 3 | 3.4% | 0.63 | 0.42 | 7.9% | 6.7% | 7.5% | 8.1%/5.9% | 4.6 (interpolated) | pass | 0.064 (unverified) | -0.07 |
| 106 | `cfg_9c9b` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=10, entry_z=-1.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 76/129/0 | 205 | 7.8% | 1.5% | 0.82 | -2.9% | 392 | 1.40 | 12.0% | 84.9 | 8/8 | 1.00 | 0.73 | 0.09 | 4 | 3.8% | 0.51 | 0.56 | 6.4% | 5.1% | 7.5% | 6.9%/4.8% | 4.1 (interpolated) | pass | 0.068 (unverified) | -0.11 |
| 107 | `cfg_9381` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=10, entry_z=-1.5, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 77/135/0 | 212 | 11.3% | 2.2% | 1.07 | -1.4% | 411 | 1.58 | 10.6% | 88.2 | 9/9 | 1.00 | 0.81 | 0.26 | 4 | 5.6% | 0.50 | 0.42 | 9.9% | 8.6% | 8.0% | 10.1%/8.1% | 5.5 (interpolated) | pass | 0.163 (unverified) | -0.30 |
| 108 | `cfg_c749` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=8, entry_z=-1.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 43/143/24 | 210 | 9.0% | 1.7% | 0.94 | -1.7% | 355 | 1.44 | 12.6% | 87.0 | 11/11 | 1.00 | 0.74 | 0.19 | 3 | 3.8% | 0.57 | 0.56 | 7.7% | 6.3% | 5.5% | 7.4%/5.5% | 4.5 (interpolated) | pass | 0.101 (unverified) | 0.08 |
| 109 | `cfg_f15a` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-1.75, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 35/148/26 | 209 | 10.2% | 2.0% | 0.96 | -3.1% | 496 | 1.52 | 10.7% | 85.6 | 12/12 | 1.00 | 0.75 | 0.21 | 3 | 3.5% | 0.66 | 0.45 | 9.1% | 7.9% | 4.9% | 8.5%/6.8% | 5.2 (interpolated) | pass | 0.107 (unverified) | -0.12 |
| 110 | `cfg_7ebf` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=12, entry_z=-1.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 62/114/0 | 176 | 10.1% | 1.9% | 0.81 | -3.7% | 371 | 1.42 | 15.4% | 73.1 | 8/8 | 1.00 | 0.74 | 0.07 | 4 | 5.0% | 0.48 | 0.55 | 9.0% | 8.0% | 5.2% | 8.7%/6.5% | 6.0 (interpolated) | pass | 0.067 (unverified) | -0.03 |
| 111 | `cfg_675d` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=10, entry_z=-2.0, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 33/179/0 | 212 | 7.8% | 1.5% | 0.90 | -2.5% | 166 | 1.50 | 9.3% | 87.6 | 10/10 | 1.00 | 0.81 | 0.09 | 5 | 4.9% | 0.36 | 0.49 | 6.4% | 5.3% | 10.1% | 7.0%/5.6% | 4.2 (interpolated) | pass | 0.089 (unverified) | -0.48 |
| 112 | `cfg_a2c6` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=10, entry_z=-1.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 63/112/0 | 175 | 8.9% | 1.7% | 1.01 | -1.8% | 230 | 1.61 | 10.4% | 73.3 | 8/8 | 1.00 | 0.71 | 0.31 | 4 | 3.2% | 0.62 | 0.42 | 7.8% | 6.6% | 7.7% | 7.8%/5.8% | 5.1 (interpolated) | pass | 0.136 (unverified) | -0.59 |
| 113 | `cfg_da37` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 57/152/15 | 224 | 7.2% | 1.4% | 0.83 | -2.3% | 360 | 1.38 | 11.4% | 92.8 | 11/11 | 1.00 | 0.81 | 0.02 | 3 | 2.2% | 0.70 | 0.52 | 5.9% | 4.5% | 8.0% | 6.3%/4.9% | 3.7 (interpolated) | pass | 0.068 (unverified) | -0.46 |
| 114 | `cfg_6a3d` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=6, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 77/139/0 | 216 | 9.3% | 1.8% | 0.93 | -2.4% | 380 | 1.44 | 12.6% | 89.3 | 10/10 | 1.00 | 0.68 | 0.24 | 4 | 3.2% | 0.66 | 0.41 | 8.0% | 6.7% | 3.4% | 8.0%/6.0% | 4.5 (interpolated) | pass | 0.112 (unverified) | -0.27 |
| 115 | `cfg_c634` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=8, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 30/142/0 | 172 | 7.3% | 1.4% | 0.75 | -3.0% | 630 | 1.45 | 11.0% | 70.6 | 10/10 | 1.00 | 0.78 | -0.03 | 3 | 2.4% | 0.66 | 0.57 | 6.4% | 5.5% | -2.1% | 6.5%/4.9% | 4.5 (interpolated) | pass | 0.046 (unverified) | -0.38 |
| 116 | `cfg_ff80` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=6, entry_z=-1.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 80/133/0 | 213 | 7.5% | 1.5% | 0.76 | -2.1% | 348 | 1.35 | 12.4% | 88.3 | 9/9 | 1.00 | 0.62 | 0.14 | 4 | 4.0% | 0.46 | 0.49 | 6.1% | 4.9% | 1.8% | 6.7%/5.3% | 3.9 (interpolated) | pass | 0.047 (unverified) | -0.40 |
| 117 | `cfg_7162` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=10, entry_z=-1.5, exit_z=0.5, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 44/134/0 | 178 | 10.2% | 2.0% | 0.85 | -2.9% | 555 | 1.46 | 13.0% | 73.2 | 9/9 | 1.00 | 0.60 | 0.26 | 3 | 3.9% | 0.59 | 0.51 | 9.0% | 8.0% | 9.7% | 8.5%/6.6% | 5.8 (interpolated) | pass | 0.076 (unverified) | 0.13 |
| 118 | `cfg_9b56` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.75, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 27/163/0 | 190 | 9.4% | 1.8% | 1.00 | -2.7% | 598 | 1.53 | 12.6% | 78.0 | 10/10 | 1.00 | 0.74 | 0.26 | 3 | 3.9% | 0.58 | 0.45 | 8.3% | 7.2% | 5.8% | 8.4%/6.6% | 5.2 (interpolated) | pass | 0.144 (unverified) | -0.42 |
| 119 | `cfg_71f7` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=10, entry_z=-1.5, exit_z=0.0, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 54/126/0 | 180 | 9.9% | 1.9% | 0.86 | -3.1% | 555 | 1.44 | 12.8% | 74.2 | 10/10 | 1.00 | 0.68 | 0.18 | 3 | 3.1% | 0.66 | 0.52 | 9.0% | 7.8% | 10.8% | 8.6%/6.2% | 5.6 (interpolated) | pass | 0.087 (unverified) | 0.18 |
| 120 | `cfg_e7ff` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-2.25, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 37/149/0 | 186 | 9.0% | 1.7% | 0.98 | -2.2% | 416 | 1.60 | 8.1% | 76.8 | 9/9 | 1.00 | 0.75 | 0.22 | 4 | 4.1% | 0.55 | 0.45 | 7.9% | 6.8% | 5.0% | 8.0%/7.1% | 5.2 (interpolated) | pass | 0.138 (unverified) | 0.01 |
| 121 | `cfg_2e64` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 58/154/5 | 217 | 7.1% | 1.4% | 0.81 | -2.5% | 360 | 1.38 | 11.2% | 89.9 | 11/11 | 1.00 | 0.76 | 0.05 | 4 | 2.4% | 0.66 | 0.53 | 5.8% | 4.4% | 8.6% | 6.5%/5.1% | 3.7 (interpolated) | pass | 0.071 (unverified) | -0.33 |
| 122 | `cfg_d877` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=6, entry_z=-2.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 96/104/0 | 200 | 13.4% | 2.5% | 0.98 | -2.6% | 232 | 1.48 | 16.1% | 83.8 | 9/9 | 1.00 | 0.73 | 0.25 | 5 | 7.6% | 0.43 | 0.46 | 11.7% | 10.3% | 10.9% | 11.6%/9.5% | 6.4 (interpolated) | pass | 0.137 (unverified) | 0.07 |
| 123 | `cfg_85f1` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=6, entry_z=-2.0, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 36/173/0 | 209 | 7.5% | 1.5% | 0.77 | -1.7% | 235 | 1.37 | 11.3% | 86.8 | 9/9 | 0.89 | 0.63 | 0.13 | 4 | 4.2% | 0.43 | 0.63 | 6.3% | 5.0% | 2.3% | 6.4%/4.6% | 4.0 (interpolated) | pass | 0.052 (unverified) | 0.28 |
| 124 | `cfg_bde5` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=10, entry_z=-1.75, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 38/153/20 | 211 | 8.8% | 1.7% | 0.84 | -2.9% | 521 | 1.45 | 10.8% | 86.6 | 12/12 | 1.00 | 0.71 | 0.12 | 3 | 3.3% | 0.60 | 0.60 | 7.4% | 6.4% | 6.6% | 7.7%/5.6% | 4.5 (interpolated) | pass | 0.065 (unverified) | 0.05 |
| 125 | `cfg_c687` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=6, entry_z=-2.25, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 87/107/0 | 194 | 12.1% | 2.3% | 0.89 | -4.5% | 415 | 1.46 | 15.7% | 80.1 | 9/9 | 1.00 | 0.56 | 0.33 | 4 | 4.9% | 0.59 | 0.49 | 10.9% | 9.8% | 9.5% | 11.4%/8.6% | 6.4 (interpolated) | pass | 0.089 (unverified) | -0.04 |
| 126 | `cfg_ae73` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=6, entry_z=-2.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 113/97/0 | 210 | 13.2% | 2.5% | 1.02 | -2.6% | 232 | 1.48 | 16.0% | 87.9 | 8/8 | 1.00 | 0.67 | 0.35 | 5 | 6.7% | 0.47 | 0.39 | 12.0% | 10.5% | 11.8% | 12.0%/9.3% | 5.9 (interpolated) | pass | 0.164 (unverified) | 0.03 |
| 127 | `cfg_6cb7` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=8, entry_z=-1.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 32/151/23 | 206 | 7.9% | 1.5% | 0.82 | -1.7% | 355 | 1.40 | 12.7% | 85.7 | 10/10 | 1.00 | 0.69 | 0.13 | 3 | 2.8% | 0.64 | 0.59 | 6.7% | 5.4% | 5.2% | 6.6%/3.6% | 4.2 (interpolated) | pass | 0.065 (unverified) | 0.08 |
| 128 | `cfg_4ade` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=8, entry_z=-2.5, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 22/168/0 | 190 | 7.2% | 1.4% | 0.79 | -2.9% | 587 | 1.42 | 10.4% | 78.1 | 10/10 | 1.00 | 0.75 | 0.04 | 3 | 1.7% | 0.77 | 0.62 | 6.1% | 4.8% | 2.0% | 6.7%/5.1% | 4.1 (interpolated) | pass | 0.053 (unverified) | -0.60 |
| 129 | `cfg_1f75` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=8, entry_z=-1.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 32/151/0 | 183 | 7.7% | 1.5% | 0.85 | -1.6% | 326 | 1.45 | 11.9% | 76.1 | 9/9 | 1.00 | 0.66 | 0.19 | 3 | 2.4% | 0.68 | 0.60 | 6.6% | 5.6% | 6.7% | 7.0%/4.9% | 4.5 (interpolated) | pass | 0.070 (unverified) | 0.29 |
| 130 | `cfg_f3c0` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=8, entry_z=-2.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 40/133/0 | 173 | 8.1% | 1.6% | 0.87 | -1.9% | 505 | 1.52 | 10.9% | 71.1 | 10/10 | 1.00 | 0.75 | 0.12 | 4 | 4.0% | 0.50 | 0.47 | 7.1% | 6.1% | -0.9% | 7.2%/5.7% | 4.9 (interpolated) | pass | 0.078 (unverified) | -0.41 |
| 131 | `cfg_51d0` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=10, entry_z=-1.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 43/151/0 | 194 | 7.8% | 1.5% | 0.79 | -3.3% | 386 | 1.39 | 12.5% | 80.7 | 9/9 | 1.00 | 0.76 | 0.03 | 4 | 3.7% | 0.50 | 0.56 | 6.6% | 5.4% | 10.2% | 6.8%/5.0% | 4.4 (interpolated) | pass | 0.059 (unverified) | -0.04 |
| 132 | `cfg_bd4d` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=6, entry_z=-2.25, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 75/137/0 | 212 | 10.0% | 1.9% | 1.00 | -2.4% | 376 | 1.52 | 10.7% | 88.8 | 9/9 | 1.00 | 0.72 | 0.27 | 5 | 4.0% | 0.58 | 0.37 | 8.7% | 7.3% | 8.1% | 8.8%/7.2% | 4.8 (interpolated) | pass | 0.139 (unverified) | -0.09 |
| 133 | `cfg_b809` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=6, entry_z=-2.0, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 62/153/0 | 215 | 7.9% | 1.5% | 0.76 | -2.4% | 298 | 1.38 | 11.1% | 89.5 | 10/10 | 0.90 | 0.71 | 0.05 | 4 | 4.2% | 0.45 | 0.44 | 6.5% | 5.1% | 8.0% | 7.5%/5.2% | 4.0 (interpolated) | pass | 0.057 (unverified) | -0.02 |
| 134 | `cfg_925d` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=8, entry_z=-1.75, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 24/163/22 | 209 | 7.7% | 1.5% | 0.86 | -2.6% | 354 | 1.40 | 11.0% | 86.5 | 11/11 | 1.00 | 0.64 | 0.21 | 4 | 4.1% | 0.47 | 0.65 | 6.5% | 5.4% | 2.1% | 6.5%/4.8% | 4.0 (interpolated) | pass | 0.071 (unverified) | 0.18 |
| 135 | `cfg_bc6c` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=10, entry_z=-1.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 68/128/60 | 256 | 11.4% | 2.2% | 1.01 | -3.5% | 594 | 1.45 | 14.2% | 104.8 | 10/10 | 0.90 | 0.75 | 0.26 | 3 | 3.8% | 0.67 | 0.42 | 10.0% | 8.5% | 4.0% | 10.3%/8.1% | 4.8 (interpolated) | pass | 0.137 (unverified) | -0.29 |
| 136 | `cfg_e4e6` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=8, entry_z=-2.5, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 33/157/0 | 190 | 6.7% | 1.3% | 0.76 | -2.9% | 587 | 1.39 | 10.2% | 78.1 | 10/10 | 1.00 | 0.77 | -0.01 | 3 | 1.8% | 0.73 | 0.62 | 5.5% | 4.3% | 2.4% | 6.1%/4.3% | 3.8 (interpolated) | pass | 0.046 (unverified) | -0.62 |
| 137 | `cfg_cee4` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-1.75, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 88/97/0 | 185 | 10.4% | 2.0% | 0.82 | -3.0% | 406 | 1.42 | 15.2% | 77.3 | 10/10 | 1.00 | 0.64 | 0.18 | 4 | 6.2% | 0.39 | 0.46 | 8.9% | 8.1% | 10.1% | 9.3%/7.6% | 5.6 (interpolated) | pass | 0.076 (unverified) | -0.13 |
| 138 | `cfg_1b74` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=6, entry_z=-2.5, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 55/172/0 | 227 | 7.7% | 1.5% | 0.77 | -2.7% | 207 | 1.37 | 9.7% | 93.9 | 8/8 | 1.00 | 0.74 | 0.03 | 4 | 4.1% | 0.47 | 0.46 | 6.1% | 4.9% | 5.9% | 7.3%/5.0% | 3.9 (interpolated) | pass | 0.068 (unverified) | -0.37 |
| 139 | `cfg_e096` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=8, entry_z=-1.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.5 | 33/124/5 | 162 | 6.3% | 1.2% | 0.83 | -2.0% | 446 | 1.49 | 10.0% | 67.0 | 10/10 | 1.00 | 0.72 | 0.11 | 3 | 2.5% | 0.58 | 0.65 | 5.4% | 4.5% | 0.4% | 5.3%/4.0% | 4.5 (interpolated) | pass | 0.061 (unverified) | -0.14 |
| 140 | `cfg_ef0b` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 29/162/0 | 191 | 7.3% | 1.4% | 0.76 | -2.0% | 312 | 1.43 | 10.4% | 78.8 | 11/11 | 1.00 | 0.65 | 0.11 | 3 | 3.8% | 0.48 | 0.54 | 6.0% | 4.9% | 3.1% | 6.3%/4.7% | 4.4 (interpolated) | pass | 0.058 (unverified) | -0.14 |
| 141 | `cfg_7a94` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=6, entry_z=-1.75, exit_z=-1.0, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 103/119/0 | 222 | 8.7% | 1.7% | 0.78 | -3.9% | 632 | 1.36 | 13.7% | 90.5 | 9/9 | 1.00 | 0.59 | 0.19 | 4 | 1.5% | 0.83 | 0.46 | 7.4% | 5.8% | 4.4% | 7.6%/5.3% | 4.1 (interpolated) | pass | 0.061 (unverified) | -0.09 |
| 142 | `cfg_bc77` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-2.25, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.5 | 22/143/15 | 180 | 9.1% | 1.8% | 0.92 | -3.1% | 325 | 1.51 | 11.4% | 75.7 | 11/11 | 0.91 | 0.65 | 0.27 | 4 | 2.9% | 0.66 | 0.49 | 7.7% | 6.4% | -3.0% | 8.0%/5.4% | 5.2 (interpolated) | pass | 0.101 (unverified) | -0.31 |
| 143 | `cfg_9c56` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-1.5, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 22/168/0 | 190 | 10.1% | 1.9% | 1.04 | -1.9% | 325 | 1.61 | 10.4% | 79.8 | 8/8 | 1.00 | 0.73 | 0.31 | 3 | 2.7% | 0.71 | 0.42 | 8.7% | 7.8% | 5.7% | 9.1%/7.0% | 5.4 (interpolated) | pass | 0.152 (unverified) | -0.44 |
| 144 | `cfg_3e60` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=12, entry_z=-1.5, exit_z=0.5, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 31/155/0 | 186 | 9.0% | 1.7% | 0.80 | -3.6% | 347 | 1.39 | 14.0% | 77.3 | 8/8 | 1.00 | 0.77 | 0.03 | 4 | 3.3% | 0.60 | 0.53 | 7.5% | 6.6% | 5.4% | 8.4%/6.8% | 5.0 (interpolated) | pass | 0.059 (unverified) | 0.01 |
| 145 | `cfg_c079` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-1.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 51/122/0 | 173 | 12.5% | 2.4% | 0.93 | -2.3% | 367 | 1.56 | 15.7% | 71.6 | 8/8 | 1.00 | 0.49 | 0.45 | 4 | 5.0% | 0.60 | 0.44 | 11.3% | 10.3% | 7.2% | 11.0%/8.6% | 7.2 (interpolated) | pass | 0.102 (unverified) | -0.11 |
| 146 | `cfg_724e` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-1.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 63/136/0 | 199 | 7.2% | 1.4% | 0.76 | -2.1% | 397 | 1.37 | 12.1% | 82.6 | 10/10 | 1.00 | 0.64 | 0.12 | 4 | 3.7% | 0.49 | 0.53 | 5.9% | 4.7% | 5.7% | 6.2%/4.5% | 3.8 (interpolated) | pass | 0.051 (unverified) | 0.27 |
| 147 | `cfg_eb4c` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=8, entry_z=-2.0, exit_z=0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 13/181/0 | 194 | 6.9% | 1.3% | 0.87 | -1.9% | 323 | 1.45 | 8.7% | 80.7 | 9/9 | 0.89 | 0.67 | 0.20 | 4 | 3.1% | 0.55 | 0.69 | 5.8% | 4.6% | 1.5% | 6.1%/4.8% | 3.9 (interpolated) | pass | 0.090 (unverified) | 0.00 |
| 148 | `cfg_2a9b` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=12, entry_z=-1.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.5 | 45/122/12 | 179 | 7.2% | 1.4% | 0.77 | -3.9% | 590 | 1.40 | 10.9% | 73.5 | 10/10 | 1.00 | 0.60 | 0.17 | 3 | 1.1% | 0.81 | 0.58 | 6.2% | 5.0% | 5.6% | 6.1%/4.7% | 4.7 (interpolated) | pass | 0.053 (unverified) | -0.62 |
| 149 | `cfg_6e52` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=12, entry_z=-1.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 44/124/0 | 168 | 8.0% | 1.6% | 0.87 | -2.9% | 546 | 1.49 | 10.4% | 69.7 | 9/9 | 1.00 | 0.66 | 0.22 | 3 | 1.6% | 0.78 | 0.54 | 7.0% | 5.8% | 6.1% | 6.8%/5.0% | 5.2 (interpolated) | pass | 0.081 (unverified) | -0.60 |
| 150 | `cfg_7f53` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-1.5, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 30/160/0 | 190 | 9.8% | 1.9% | 1.02 | -1.9% | 325 | 1.60 | 10.3% | 79.9 | 9/9 | 1.00 | 0.73 | 0.29 | 3 | 2.6% | 0.72 | 0.43 | 8.5% | 7.4% | 5.6% | 9.1%/7.4% | 5.3 (interpolated) | pass | 0.141 (unverified) | -0.41 |
| 151 | `cfg_7643` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.5, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=1.5 | 71/146/41 | 258 | 7.4% | 1.4% | 0.82 | -2.2% | 539 | 1.34 | 12.1% | 106.3 | 9/9 | 1.00 | 0.54 | 0.29 | 3 | 2.6% | 0.65 | 0.55 | 6.0% | 4.6% | 9.5% | 7.1%/5.1% | 3.5 (interpolated) | pass | 0.067 (unverified) | -0.37 |
| 152 | `cfg_efaf` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=12, entry_z=-2.25, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.5 | 38/129/15 | 182 | 7.8% | 1.5% | 0.81 | -2.7% | 369 | 1.43 | 11.1% | 75.8 | 12/12 | 0.92 | 0.73 | 0.09 | 3 | 1.9% | 0.73 | 0.52 | 6.6% | 5.5% | -2.2% | 7.2%/5.4% | 4.8 (interpolated) | pass | 0.067 (unverified) | -0.37 |
| 153 | `cfg_65d8` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=10, entry_z=-1.75, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 38/155/0 | 193 | 9.2% | 1.8% | 0.90 | -2.3% | 419 | 1.53 | 10.2% | 80.3 | 11/11 | 1.00 | 0.75 | 0.15 | 4 | 3.8% | 0.56 | 0.55 | 8.0% | 6.9% | 7.4% | 8.1%/6.2% | 5.1 (interpolated) | pass | 0.081 (unverified) | -0.01 |
| 154 | `cfg_e482` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=6, entry_z=-2.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 62/164/0 | 226 | 8.2% | 1.6% | 0.84 | -2.9% | 258 | 1.40 | 9.6% | 94.3 | 7/7 | 1.00 | 0.74 | 0.10 | 4 | 2.4% | 0.70 | 0.53 | 6.9% | 5.5% | 6.5% | 6.8%/5.0% | 4.1 (interpolated) | pass | 0.076 (unverified) | 0.14 |
| 155 | `cfg_ddc3` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=10, entry_z=-1.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 67/112/0 | 179 | 13.0% | 2.5% | 1.00 | -3.9% | 348 | 1.54 | 15.8% | 74.5 | 8/8 | 1.00 | 0.81 | 0.19 | 4 | 6.8% | 0.45 | 0.45 | 11.6% | 10.5% | 11.0% | 11.1%/8.6% | 6.9 (interpolated) | pass | 0.135 (unverified) | 0.15 |
| 156 | `cfg_80c2` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 37/178/51 | 266 | 8.7% | 1.7% | 0.87 | -1.6% | 327 | 1.35 | 10.6% | 110.9 | 8/8 | 1.00 | 0.55 | 0.32 | 4 | 4.7% | 0.45 | 0.50 | 7.1% | 5.5% | -2.7% | 7.6%/5.0% | 3.7 (interpolated) | pass | 0.083 (unverified) | -0.29 |
| 157 | `cfg_58fa` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=6, entry_z=-2.25, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 59/150/30 | 239 | 9.6% | 1.9% | 0.92 | -2.4% | 278 | 1.44 | 11.6% | 100.2 | 11/11 | 1.00 | 0.73 | 0.19 | 5 | 3.7% | 0.60 | 0.38 | 7.9% | 6.4% | 7.2% | 8.6%/6.4% | 4.3 (interpolated) | pass | 0.100 (unverified) | -0.14 |
| 158 | `cfg_d6b3` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 45/182/0 | 227 | 7.7% | 1.5% | 0.77 | -2.7% | 207 | 1.37 | 9.8% | 93.8 | 8/8 | 1.00 | 0.68 | 0.09 | 4 | 4.2% | 0.46 | 0.46 | 6.1% | 4.9% | 5.5% | 7.0%/5.4% | 3.8 (interpolated) | pass | 0.067 (unverified) | -0.32 |
| 159 | `cfg_0ad1` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 73/102/0 | 175 | 9.9% | 1.9% | 0.80 | -4.7% | 510 | 1.41 | 14.9% | 72.3 | 10/10 | 1.00 | 0.61 | 0.19 | 4 | 2.3% | 0.77 | 0.57 | 9.0% | 8.1% | 4.9% | 9.1%/6.6% | 5.7 (interpolated) | pass | 0.059 (unverified) | 0.06 |
| 160 | `cfg_76ea` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=6, entry_z=-1.75, exit_z=-0.5, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 83/130/0 | 213 | 8.8% | 1.7% | 0.79 | -3.3% | 511 | 1.37 | 14.0% | 87.0 | 10/10 | 1.00 | 0.64 | 0.15 | 4 | 2.1% | 0.76 | 0.44 | 7.8% | 6.3% | 5.5% | 7.5%/5.4% | 4.3 (interpolated) | pass | 0.062 (unverified) | -0.11 |
| 161 | `cfg_0a72` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=10, entry_z=-1.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 31/183/0 | 214 | 7.3% | 1.4% | 0.81 | -2.1% | 530 | 1.42 | 9.4% | 87.8 | 9/9 | 0.78 | 0.70 | 0.11 | 4 | 1.9% | 0.74 | 0.60 | 6.2% | 4.9% | 7.1% | 6.5%/5.0% | 3.7 (interpolated) | pass | 0.058 (unverified) | -1.52 |
| 162 | `cfg_5fcb` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=8, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 28/149/0 | 177 | 6.9% | 1.3% | 0.81 | -2.4% | 642 | 1.42 | 11.4% | 72.7 | 10/10 | 1.00 | 0.72 | 0.09 | 4 | 3.1% | 0.55 | 0.52 | 5.9% | 4.9% | 3.6% | 5.6%/3.8% | 4.2 (interpolated) | pass | 0.068 (unverified) | 0.15 |
| 163 | `cfg_8acb` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=10, entry_z=-1.5, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 44/172/0 | 216 | 7.9% | 1.5% | 0.85 | -2.1% | 515 | 1.44 | 9.4% | 88.6 | 9/9 | 0.78 | 0.70 | 0.15 | 4 | 2.4% | 0.69 | 0.59 | 6.7% | 5.4% | 8.7% | 7.2%/5.7% | 4.0 (interpolated) | pass | 0.064 (unverified) | -1.52 |
| 164 | `cfg_66d6` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 21/174/0 | 195 | 8.1% | 1.6% | 0.92 | -2.2% | 312 | 1.49 | 10.8% | 80.9 | 10/10 | 1.00 | 0.80 | 0.12 | 3 | 3.5% | 0.56 | 0.55 | 6.8% | 5.8% | 7.1% | 7.3%/5.6% | 4.6 (interpolated) | pass | 0.094 (unverified) | -0.18 |
| 165 | `cfg_49fa` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=15, entry_z=-1.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 67/127/0 | 194 | 7.5% | 1.5% | 0.85 | -2.4% | 367 | 1.43 | 11.4% | 80.2 | 7/7 | 1.00 | 0.74 | 0.10 | 4 | 4.0% | 0.47 | 0.56 | 6.3% | 5.2% | 6.2% | 7.2%/5.4% | 4.4 (interpolated) | pass | 0.077 (unverified) | -0.21 |
| 166 | `cfg_2d64` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 59/111/0 | 170 | 9.6% | 1.9% | 0.76 | -4.9% | 690 | 1.41 | 15.4% | 70.1 | 10/10 | 1.00 | 0.71 | 0.04 | 4 | 1.6% | 0.83 | 0.59 | 8.7% | 7.4% | 4.9% | 8.8%/6.5% | 5.8 (interpolated) | pass | 0.049 (unverified) | -0.22 |
| 167 | `cfg_271d` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=6, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 93/103/0 | 196 | 15.0% | 2.8% | 1.14 | -3.2% | 521 | 1.59 | 15.4% | 81.4 | 7/7 | 1.00 | 0.71 | 0.44 | 4 | 7.4% | 0.51 | 0.38 | 13.5% | 12.4% | 9.7% | 13.5%/10.9% | 7.4 (interpolated) | pass | 0.230 (unverified) | 0.06 |
| 168 | `cfg_2762` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=6, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 44/158/0 | 202 | 8.2% | 1.6% | 0.77 | -3.1% | 477 | 1.38 | 12.6% | 83.8 | 9/9 | 1.00 | 0.69 | 0.08 | 5 | 3.6% | 0.57 | 0.56 | 7.1% | 5.7% | 5.7% | 7.2%/4.1% | 4.4 (interpolated) | pass | 0.054 (unverified) | 0.07 |
| 169 | `cfg_63c2` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 56/120/50 | 226 | 9.2% | 1.8% | 0.98 | -2.6% | 520 | 1.46 | 12.3% | 91.8 | 9/9 | 1.00 | 0.70 | 0.28 | 3 | 2.3% | 0.75 | 0.45 | 8.0% | 6.5% | -5.1% | 8.1%/6.0% | 4.4 (interpolated) | pass | 0.137 (unverified) | -0.49 |
| 170 | `cfg_00e1` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=10, entry_z=-1.5, exit_z=-1.0, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 85/115/0 | 200 | 8.0% | 1.5% | 0.75 | -3.5% | 377 | 1.35 | 13.2% | 83.3 | 8/8 | 1.00 | 0.70 | 0.06 | 4 | 3.3% | 0.56 | 0.59 | 6.7% | 5.4% | 6.5% | 7.2%/4.9% | 4.4 (interpolated) | pass | 0.050 (unverified) | -0.15 |
| 171 | `cfg_9b1a` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=8, entry_z=-1.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 63/109/0 | 172 | 6.5% | 1.3% | 0.87 | -1.7% | 518 | 1.50 | 10.0% | 71.0 | 8/8 | 1.00 | 0.68 | 0.19 | 3 | 2.6% | 0.58 | 0.56 | 5.4% | 4.4% | 4.2% | 5.7%/3.8% | 4.2 (interpolated) | pass | 0.078 (unverified) | -0.45 |
| 172 | `cfg_4d15` | timeframe=1h, mean_type=ema, mean_lookback=90, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 65/141/0 | 206 | 7.5% | 1.5% | 0.76 | -4.6% | 744 | 1.37 | 12.5% | 83.4 | 10/10 | 1.00 | 0.61 | 0.15 | 3 | 1.3% | 0.83 | 0.59 | 6.2% | 4.8% | 0.4% | 7.0%/5.3% | 4.0 (interpolated) | pass | 0.046 (unverified) | -0.57 |
| 173 | `cfg_08f9` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.0, exit_z=0.5, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 29/144/0 | 173 | 9.5% | 1.8% | 0.78 | -3.4% | 507 | 1.44 | 13.0% | 71.2 | 10/10 | 1.00 | 0.66 | 0.12 | 4 | 2.5% | 0.74 | 0.51 | 8.6% | 7.6% | 7.7% | 9.0%/6.6% | 5.6 (interpolated) | pass | 0.064 (unverified) | 0.13 |
| 174 | `cfg_5df6` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 53/126/0 | 179 | 8.9% | 1.7% | 1.01 | -1.6% | 319 | 1.56 | 10.8% | 73.3 | 9/9 | 1.00 | 0.80 | 0.22 | 4 | 3.6% | 0.60 | 0.44 | 7.7% | 6.7% | -2.4% | 7.5%/6.1% | 5.1 (interpolated) | pass | 0.159 (unverified) | -0.30 |
| 175 | `cfg_43f7` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=12, entry_z=-2.25, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 32/147/0 | 179 | 6.2% | 1.2% | 0.76 | -3.1% | 654 | 1.40 | 9.7% | 73.1 | 11/11 | 1.00 | 0.72 | 0.04 | 3 | 2.4% | 0.62 | 0.69 | 5.2% | 4.2% | 6.0% | 5.8%/4.2% | 3.9 (interpolated) | pass | 0.058 (unverified) | -0.73 |
| 176 | `cfg_6e86` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 72/119/0 | 191 | 8.3% | 1.6% | 0.79 | -2.7% | 355 | 1.37 | 13.0% | 79.6 | 9/9 | 1.00 | 0.64 | 0.15 | 3 | 3.5% | 0.57 | 0.57 | 7.3% | 6.0% | 5.4% | 7.5%/5.2% | 4.7 (interpolated) | pass | 0.060 (unverified) | -0.16 |
| 177 | `cfg_08ca` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=8, entry_z=-2.0, exit_z=0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.5 | 13/181/6 | 200 | 6.5% | 1.3% | 0.80 | -1.9% | 323 | 1.41 | 8.8% | 83.2 | 10/10 | 0.90 | 0.63 | 0.17 | 4 | 2.7% | 0.59 | 0.73 | 5.3% | 4.1% | 1.1% | 5.8%/4.0% | 3.7 (interpolated) | pass | 0.071 (unverified) | 0.10 |
| 178 | `cfg_2b30` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=8, entry_z=-2.0, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 22/162/21 | 205 | 7.2% | 1.4% | 0.81 | -1.9% | 219 | 1.38 | 10.8% | 85.1 | 11/11 | 1.00 | 0.61 | 0.20 | 4 | 3.3% | 0.54 | 0.71 | 6.1% | 4.9% | 0.1% | 5.9%/4.1% | 4.0 (interpolated) | pass | 0.067 (unverified) | 0.48 |
| 179 | `cfg_8229` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=8, entry_z=-1.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 32/125/0 | 157 | 5.9% | 1.2% | 0.82 | -1.8% | 443 | 1.49 | 9.7% | 64.8 | 9/9 | 1.00 | 0.65 | 0.17 | 3 | 2.7% | 0.52 | 0.66 | 5.1% | 4.2% | 1.2% | 5.4%/4.0% | 4.5 (interpolated) | pass | 0.061 (unverified) | -0.21 |
| 180 | `cfg_3ac0` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=10, entry_z=-1.5, exit_z=0.0, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 52/135/0 | 187 | 9.6% | 1.8% | 0.85 | -3.7% | 355 | 1.42 | 13.6% | 77.8 | 9/9 | 1.00 | 0.74 | 0.10 | 4 | 3.9% | 0.56 | 0.49 | 8.4% | 7.2% | 9.9% | 8.3%/5.7% | 5.3 (interpolated) | pass | 0.079 (unverified) | 0.10 |
| 181 | `cfg_dee5` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=8, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 26/151/0 | 177 | 7.3% | 1.4% | 0.81 | -2.4% | 503 | 1.45 | 11.5% | 72.8 | 9/9 | 1.00 | 0.69 | 0.12 | 4 | 3.4% | 0.53 | 0.50 | 6.2% | 5.2% | 3.9% | 6.4%/4.7% | 4.4 (interpolated) | pass | 0.065 (unverified) | 0.15 |
| 182 | `cfg_3ffa` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=6, entry_z=-2.5, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 48/167/51 | 266 | 8.6% | 1.7% | 0.86 | -1.6% | 327 | 1.35 | 10.6% | 110.9 | 8/8 | 1.00 | 0.57 | 0.29 | 4 | 4.6% | 0.45 | 0.50 | 7.0% | 5.5% | -3.2% | 7.2%/5.2% | 3.7 (interpolated) | pass | 0.081 (unverified) | -0.24 |
| 183 | `cfg_f6f8` | timeframe=1h, mean_type=ema, mean_lookback=90, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 54/161/0 | 215 | 7.1% | 1.4% | 0.78 | -4.0% | 731 | 1.39 | 11.2% | 87.2 | 10/10 | 1.00 | 0.64 | 0.14 | 3 | 0.7% | 0.90 | 0.63 | 5.9% | 4.3% | 3.7% | 6.9%/4.6% | 3.7 (interpolated) | pass | 0.051 (unverified) | -0.57 |
| 184 | `cfg_69bc` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=6, entry_z=-2.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 72/137/0 | 209 | 8.5% | 1.6% | 0.79 | -2.2% | 260 | 1.41 | 12.5% | 86.7 | 10/10 | 1.00 | 0.65 | 0.14 | 5 | 4.5% | 0.47 | 0.40 | 7.1% | 5.6% | 7.1% | 7.8%/5.4% | 4.4 (interpolated) | pass | 0.069 (unverified) | -0.07 |
| 185 | `cfg_6d6b` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=12, entry_z=-1.75, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 37/141/6 | 184 | 7.9% | 1.5% | 0.88 | -1.9% | 361 | 1.50 | 9.8% | 76.9 | 11/11 | 1.00 | 0.58 | 0.30 | 4 | 3.5% | 0.54 | 0.54 | 6.6% | 5.7% | 2.3% | 6.4%/4.8% | 4.7 (interpolated) | pass | 0.084 (unverified) | -0.54 |
| 186 | `cfg_229e` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 90/120/60 | 270 | 9.7% | 1.9% | 0.91 | -2.8% | 381 | 1.39 | 14.3% | 112.1 | 9/9 | 1.00 | 0.65 | 0.26 | 3 | 3.1% | 0.68 | 0.45 | 8.1% | 6.5% | 6.8% | 8.9%/7.1% | 3.9 (interpolated) | pass | 0.098 (unverified) | -0.09 |
| 187 | `cfg_9818` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 35/141/0 | 176 | 7.4% | 1.4% | 0.77 | -2.4% | 613 | 1.43 | 11.2% | 72.2 | 11/11 | 1.00 | 0.56 | 0.22 | 4 | 2.7% | 0.61 | 0.63 | 6.3% | 5.1% | 0.6% | 6.4%/4.8% | 4.5 (interpolated) | pass | 0.049 (unverified) | 0.11 |
| 188 | `cfg_4f51` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=6, entry_z=-2.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 62/158/52 | 272 | 8.2% | 1.6% | 0.82 | -1.9% | 342 | 1.33 | 10.6% | 114.4 | 7/7 | 1.00 | 0.72 | 0.10 | 4 | 2.3% | 0.71 | 0.53 | 6.4% | 4.8% | 3.3% | 6.9%/4.7% | 3.5 (interpolated) | pass | 0.079 (unverified) | -0.08 |
| 189 | `cfg_1c51` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=15, entry_z=-1.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 19/163/22 | 204 | 7.7% | 1.5% | 0.79 | -2.6% | 234 | 1.39 | 12.9% | 84.5 | 8/8 | 1.00 | 0.67 | 0.12 | 4 | 3.7% | 0.52 | 0.58 | 6.5% | 5.2% | 1.9% | 7.0%/5.7% | 4.2 (interpolated) | pass | 0.059 (unverified) | -0.28 |
| 190 | `cfg_5579` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=12, entry_z=-1.5, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 73/153/0 | 226 | 7.7% | 1.5% | 0.75 | -4.2% | 575 | 1.38 | 11.5% | 91.2 | 9/9 | 0.89 | 0.56 | 0.19 | 3 | 1.4% | 0.78 | 0.59 | 6.4% | 5.1% | 6.4% | 6.7%/4.9% | 3.8 (interpolated) | pass | 0.044 (unverified) | -0.60 |
| 191 | `cfg_a7c1` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=10, entry_z=-1.5, exit_z=-1.0, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 95/109/0 | 204 | 8.9% | 1.7% | 0.76 | -4.4% | 626 | 1.38 | 13.0% | 82.5 | 9/9 | 0.89 | 0.75 | 0.01 | 3 | 2.4% | 0.73 | 0.49 | 7.8% | 6.8% | 8.9% | 8.4%/6.2% | 4.7 (interpolated) | pass | 0.050 (unverified) | -0.11 |
| 192 | `cfg_ff97` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=10, entry_z=-2.25, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 46/151/0 | 197 | 7.5% | 1.5% | 0.78 | -2.4% | 539 | 1.43 | 10.6% | 80.7 | 9/9 | 0.89 | 0.63 | 0.16 | 4 | 3.3% | 0.56 | 0.57 | 6.4% | 5.3% | 7.7% | 7.0%/5.3% | 4.2 (interpolated) | pass | 0.050 (unverified) | -0.10 |
| 193 | `cfg_d2d6` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=12, entry_z=-1.5, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 28/164/17 | 209 | 7.0% | 1.4% | 0.79 | -1.9% | 218 | 1.36 | 11.1% | 86.6 | 10/10 | 1.00 | 0.56 | 0.23 | 4 | 2.4% | 0.64 | 0.59 | 5.7% | 4.5% | -0.7% | 5.9%/4.2% | 3.9 (interpolated) | pass | 0.056 (unverified) | 0.00 |
| 194 | `cfg_ee7b` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=12, entry_z=-1.75, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 28/148/7 | 183 | 7.8% | 1.5% | 0.86 | -2.0% | 361 | 1.49 | 9.9% | 76.5 | 11/11 | 1.00 | 0.61 | 0.25 | 4 | 3.6% | 0.52 | 0.54 | 6.6% | 5.7% | 2.1% | 6.6%/5.0% | 4.6 (interpolated) | pass | 0.079 (unverified) | -0.54 |
| 195 | `cfg_d7af` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=12, entry_z=-2.25, exit_z=0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.5 | 22/146/18 | 186 | 7.7% | 1.5% | 0.80 | -3.4% | 398 | 1.39 | 11.7% | 76.9 | 11/11 | 0.91 | 0.61 | 0.19 | 4 | 3.5% | 0.55 | 0.64 | 6.8% | 6.0% | -0.2% | 6.8%/5.7% | 4.7 (interpolated) | pass | 0.069 (unverified) | -0.92 |
| 196 | `cfg_2c07` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=10, entry_z=-1.5, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 42/122/0 | 164 | 6.3% | 1.2% | 0.75 | -3.6% | 488 | 1.46 | 10.1% | 67.6 | 9/9 | 1.00 | 0.68 | 0.07 | 3 | 1.5% | 0.74 | 0.58 | 5.4% | 4.5% | 4.5% | 5.6%/4.1% | 4.4 (interpolated) | pass | 0.045 (unverified) | -0.47 |
| 197 | `cfg_3c04` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 30/153/0 | 183 | 8.4% | 1.6% | 0.90 | -2.2% | 308 | 1.49 | 12.0% | 76.1 | 10/10 | 1.00 | 0.74 | 0.16 | 4 | 4.0% | 0.53 | 0.55 | 7.0% | 6.2% | 5.5% | 7.3%/5.3% | 4.9 (interpolated) | pass | 0.089 (unverified) | -0.14 |
| 198 | `cfg_5dcf` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=15, entry_z=-1.75, exit_z=-0.5, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 38/137/0 | 175 | 7.4% | 1.4% | 0.76 | -2.7% | 558 | 1.40 | 11.1% | 73.1 | 10/10 | 1.00 | 0.55 | 0.21 | 4 | 1.1% | 0.82 | 0.68 | 6.3% | 5.4% | -0.1% | 6.4%/4.8% | 4.8 (interpolated) | pass | 0.051 (unverified) | -0.25 |
| 199 | `cfg_e13a` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=8, entry_z=-2.0, exit_z=-0.5, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 58/124/0 | 182 | 9.4% | 1.8% | 0.78 | -3.4% | 456 | 1.42 | 12.8% | 74.8 | 11/11 | 1.00 | 0.67 | 0.11 | 4 | 2.9% | 0.69 | 0.49 | 8.5% | 7.5% | 7.3% | 8.7%/7.0% | 5.5 (interpolated) | pass | 0.066 (unverified) | 0.16 |
| 200 | `cfg_a130` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=12, entry_z=-1.5, exit_z=0.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 31/161/17 | 209 | 6.6% | 1.3% | 0.79 | -1.9% | 218 | 1.34 | 10.9% | 86.7 | 11/11 | 1.00 | 0.51 | 0.28 | 4 | 1.9% | 0.70 | 0.59 | 5.2% | 4.1% | -1.1% | 5.7%/3.8% | 3.8 (interpolated) | pass | 0.057 (unverified) | 0.01 |
| 201 | `cfg_90ee` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=12, entry_z=-2.5, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 29/154/11 | 194 | 7.2% | 1.4% | 0.75 | -2.5% | 406 | 1.40 | 10.3% | 80.6 | 11/11 | 1.00 | 0.64 | 0.12 | 4 | 3.7% | 0.49 | 0.66 | 6.2% | 5.2% | 2.6% | 6.6%/4.9% | 4.3 (interpolated) | pass | 0.057 (unverified) | -1.03 |
| 202 | `cfg_2af3` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=12, entry_z=-1.75, exit_z=0.0, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 40/142/0 | 182 | 8.5% | 1.6% | 0.77 | -3.4% | 443 | 1.38 | 13.4% | 75.4 | 10/10 | 1.00 | 0.68 | 0.09 | 3 | 2.9% | 0.66 | 0.56 | 7.5% | 6.3% | 5.8% | 7.5%/5.2% | 5.0 (interpolated) | pass | 0.052 (unverified) | 0.06 |
| 203 | `cfg_95c0` | timeframe=1h, mean_type=ema, mean_lookback=80, std_lookback=12, entry_z=-1.5, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 74/150/17 | 241 | 7.8% | 1.5% | 0.76 | -4.2% | 554 | 1.36 | 11.9% | 97.4 | 10/10 | 0.90 | 0.49 | 0.27 | 3 | 1.4% | 0.78 | 0.58 | 6.5% | 5.3% | 3.9% | 6.8%/5.3% | 3.7 (interpolated) | pass | 0.045 (unverified) | -0.64 |
| 204 | `cfg_c57c` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=10, entry_z=-1.5, exit_z=-1.0, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 72/99/0 | 171 | 8.5% | 1.6% | 0.83 | -3.0% | 510 | 1.46 | 11.4% | 70.4 | 8/8 | 1.00 | 0.60 | 0.23 | 3 | 1.8% | 0.76 | 0.55 | 7.4% | 6.3% | 5.7% | 7.3%/5.2% | 5.2 (interpolated) | pass | 0.066 (unverified) | -0.54 |
| 205 | `cfg_c536` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=10, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 30/143/0 | 173 | 7.7% | 1.5% | 0.79 | -2.7% | 418 | 1.43 | 11.3% | 70.8 | 10/10 | 1.00 | 0.63 | 0.16 | 3 | 2.9% | 0.62 | 0.59 | 6.6% | 5.7% | 2.9% | 6.4%/3.7% | 4.6 (interpolated) | pass | 0.055 (unverified) | -0.67 |
| 206 | `cfg_92e3` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=6, entry_z=-2.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 79/112/0 | 191 | 14.9% | 2.8% | 1.11 | -3.1% | 519 | 1.59 | 15.8% | 79.4 | 8/8 | 1.00 | 0.62 | 0.49 | 4 | 7.3% | 0.51 | 0.41 | 13.6% | 12.6% | 11.5% | 14.0%/11.6% | 7.5 (interpolated) | pass | 0.200 (unverified) | 0.03 |
| 207 | `cfg_5732` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-1.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 88/115/61 | 264 | 8.3% | 1.6% | 0.77 | -3.0% | 566 | 1.32 | 13.6% | 108.0 | 9/9 | 1.00 | 0.60 | 0.17 | 3 | 2.4% | 0.69 | 0.49 | 6.9% | 5.3% | 0.4% | 7.7%/5.6% | 3.7 (interpolated) | pass | 0.054 (unverified) | 0.05 |
| 208 | `cfg_8716` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=12, entry_z=-2.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.5 | 45/152/10 | 207 | 7.8% | 1.5% | 0.91 | -3.1% | 324 | 1.43 | 8.8% | 85.5 | 10/10 | 1.00 | 0.67 | 0.24 | 4 | 2.9% | 0.62 | 0.62 | 6.5% | 5.3% | 2.8% | 6.6%/5.3% | 4.2 (interpolated) | pass | 0.105 (unverified) | 0.15 |
| 209 | `cfg_6d24` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=10, entry_z=-2.25, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 31/165/0 | 196 | 7.4% | 1.4% | 0.76 | -2.2% | 538 | 1.42 | 10.7% | 80.2 | 10/10 | 0.90 | 0.65 | 0.11 | 4 | 3.1% | 0.58 | 0.58 | 6.2% | 5.2% | 8.2% | 6.7%/4.9% | 4.1 (interpolated) | pass | 0.045 (unverified) | -0.04 |
| 210 | `cfg_17b7` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=10, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.5 | 30/153/12 | 195 | 7.5% | 1.5% | 0.80 | -2.4% | 309 | 1.40 | 12.5% | 81.1 | 11/11 | 1.00 | 0.64 | 0.16 | 4 | 3.4% | 0.54 | 0.60 | 6.5% | 5.4% | 4.8% | 6.2%/4.0% | 4.3 (interpolated) | pass | 0.059 (unverified) | -0.28 |
| 211 | `cfg_f8f6` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=12, entry_z=-2.0, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 32/162/7 | 201 | 6.8% | 1.3% | 0.82 | -2.2% | 355 | 1.40 | 10.7% | 83.7 | 11/11 | 1.00 | 0.68 | 0.14 | 3 | 3.0% | 0.55 | 0.59 | 5.4% | 4.3% | 2.7% | 6.0%/4.4% | 3.9 (interpolated) | pass | 0.070 (unverified) | -0.03 |
| 212 | `cfg_82d5` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=12, entry_z=-2.0, exit_z=-0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 32/162/0 | 194 | 6.4% | 1.3% | 0.78 | -2.3% | 564 | 1.39 | 10.5% | 80.8 | 10/10 | 1.00 | 0.73 | 0.05 | 3 | 2.7% | 0.56 | 0.59 | 5.3% | 4.3% | 4.8% | 5.8%/4.5% | 4.1 (interpolated) | pass | 0.061 (unverified) | 0.09 |
| 213 | `cfg_fa6f` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=12, entry_z=-2.0, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.5 | 32/163/11 | 206 | 6.6% | 1.3% | 0.78 | -3.1% | 323 | 1.35 | 8.9% | 85.3 | 11/11 | 1.00 | 0.66 | 0.11 | 3 | 2.3% | 0.64 | 0.73 | 5.5% | 4.2% | 2.2% | 5.9%/4.6% | 3.7 (interpolated) | pass | 0.066 (unverified) | 0.15 |
| 214 | `cfg_a189` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=12, entry_z=-2.25, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 46/139/0 | 185 | 7.2% | 1.4% | 0.75 | -2.9% | 454 | 1.39 | 9.8% | 76.5 | 10/10 | 0.90 | 0.69 | 0.06 | 4 | 2.1% | 0.69 | 0.59 | 5.9% | 4.8% | 4.7% | 5.9%/4.2% | 4.4 (interpolated) | pass | 0.049 (unverified) | -0.15 |
| 215 | `cfg_6a92` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-1.5, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 16/167/21 | 204 | 7.9% | 1.5% | 0.83 | -2.3% | 443 | 1.43 | 10.9% | 85.6 | 9/9 | 1.00 | 0.59 | 0.24 | 3 | 1.4% | 0.82 | 0.60 | 6.6% | 5.4% | 2.3% | 6.7%/4.9% | 4.4 (interpolated) | pass | 0.067 (unverified) | -0.42 |
| 216 | `cfg_891c` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=12, entry_z=-1.5, exit_z=-1.0, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 92/113/0 | 205 | 8.4% | 1.6% | 0.75 | -3.4% | 604 | 1.37 | 12.9% | 83.7 | 9/9 | 1.00 | 0.61 | 0.14 | 3 | 3.2% | 0.62 | 0.51 | 7.2% | 5.8% | 7.0% | 7.7%/5.5% | 4.5 (interpolated) | pass | 0.050 (unverified) | 0.08 |
| 217 | `cfg_e57f` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=8, entry_z=-1.75, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 96/102/0 | 198 | 11.1% | 2.1% | 0.93 | -2.9% | 338 | 1.47 | 15.8% | 82.2 | 9/9 | 1.00 | 0.59 | 0.33 | 3 | 6.0% | 0.46 | 0.45 | 9.6% | 8.7% | 6.9% | 10.0%/7.9% | 5.5 (interpolated) | pass | 0.109 (unverified) | -0.09 |
| 218 | `cfg_b757` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=6, entry_z=-1.75, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 104/107/0 | 211 | 10.3% | 2.0% | 0.79 | -2.5% | 261 | 1.39 | 16.8% | 87.4 | 7/7 | 1.00 | 0.47 | 0.33 | 4 | 3.9% | 0.63 | 0.52 | 8.9% | 7.6% | 6.5% | 9.0%/7.6% | 4.9 (interpolated) | pass | 0.060 (unverified) | 0.00 |
| 219 | `cfg_7882` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=6, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 70/113/0 | 183 | 7.6% | 1.5% | 0.84 | -3.8% | 277 | 1.44 | 10.5% | 76.6 | 8/8 | 1.00 | 0.61 | 0.22 | 5 | 2.8% | 0.62 | 0.55 | 6.5% | 5.3% | 4.3% | 6.8%/4.5% | 4.5 (interpolated) | pass | 0.084 (unverified) | -0.82 |
| 220 | `cfg_4883` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=12, entry_z=-2.25, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 30/152/37 | 219 | 7.3% | 1.4% | 0.86 | -2.8% | 526 | 1.38 | 8.9% | 90.4 | 10/10 | 0.80 | 0.56 | 0.30 | 4 | 2.7% | 0.60 | 0.61 | 6.1% | 4.9% | 0.2% | 5.9%/4.3% | 4.0 (interpolated) | pass | 0.080 (unverified) | -0.01 |
| 221 | `cfg_7e8e` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=12, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 64/120/29 | 213 | 7.7% | 1.5% | 0.75 | -4.1% | 671 | 1.35 | 12.0% | 86.2 | 10/10 | 1.00 | 0.60 | 0.15 | 3 | 1.9% | 0.75 | 0.60 | 6.7% | 5.5% | -2.7% | 6.7%/5.2% | 4.1 (interpolated) | pass | 0.045 (unverified) | -0.17 |
| 222 | `cfg_622d` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=6, entry_z=-1.75, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 29/175/0 | 204 | 7.5% | 1.5% | 0.79 | -1.8% | 355 | 1.39 | 11.0% | 84.9 | 9/9 | 0.89 | 0.63 | 0.16 | 4 | 4.2% | 0.45 | 0.60 | 6.3% | 5.1% | 2.8% | 6.9%/5.2% | 4.0 (interpolated) | pass | 0.056 (unverified) | 0.31 |
| 223 | `cfg_9d98` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=8, entry_z=-1.5, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 30/167/11 | 208 | 7.3% | 1.4% | 0.78 | -2.8% | 355 | 1.37 | 11.2% | 86.3 | 10/10 | 1.00 | 0.63 | 0.14 | 3 | 2.5% | 0.64 | 0.69 | 6.0% | 4.8% | 2.9% | 6.4%/4.4% | 3.9 (interpolated) | pass | 0.055 (unverified) | 0.23 |
| 224 | `cfg_76d8` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=12, entry_z=-2.0, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 52/135/10 | 197 | 6.8% | 1.3% | 0.77 | -3.7% | 393 | 1.35 | 10.0% | 82.3 | 11/11 | 1.00 | 0.59 | 0.18 | 3 | 1.7% | 0.74 | 0.67 | 5.4% | 4.3% | -0.2% | 5.6%/3.7% | 3.9 (interpolated) | pass | 0.059 (unverified) | 0.05 |
| 225 | `cfg_751d` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 57/143/15 | 215 | 7.6% | 1.5% | 0.77 | -3.5% | 339 | 1.37 | 10.8% | 88.9 | 11/11 | 1.00 | 0.60 | 0.17 | 3 | 3.0% | 0.59 | 0.62 | 6.3% | 4.7% | 0.3% | 6.9%/4.8% | 3.9 (interpolated) | pass | 0.062 (unverified) | 0.27 |
| 226 | `cfg_46ab` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=8, entry_z=-2.25, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 23/182/0 | 205 | 6.4% | 1.2% | 0.77 | -1.8% | 427 | 1.41 | 9.0% | 84.2 | 10/10 | 0.90 | 0.63 | 0.14 | 3 | 0.3% | 0.95 | 0.66 | 5.2% | 3.9% | -2.2% | 5.9%/4.4% | 3.6 (interpolated) | pass | 0.049 (unverified) | -1.19 |
| 227 | `cfg_34f9` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-1.75, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 32/178/0 | 210 | 7.2% | 1.4% | 0.88 | -2.3% | 656 | 1.43 | 9.2% | 86.9 | 10/10 | 0.90 | 0.66 | 0.22 | 4 | 2.0% | 0.72 | 0.56 | 6.0% | 4.8% | 6.1% | 6.5%/5.0% | 4.1 (interpolated) | pass | 0.090 (unverified) | -0.35 |
| 228 | `cfg_1d1d` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=8, entry_z=-1.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.5 | 64/108/7 | 179 | 6.1% | 1.2% | 0.81 | -1.8% | 518 | 1.44 | 10.3% | 73.9 | 9/9 | 1.00 | 0.62 | 0.19 | 4 | 2.6% | 0.56 | 0.59 | 5.0% | 4.0% | 2.1% | 5.3%/3.6% | 3.9 (interpolated) | pass | 0.065 (unverified) | -0.37 |
| 229 | `cfg_6f6a` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=12, entry_z=-2.5, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 40/146/0 | 186 | 7.3% | 1.4% | 0.79 | -2.4% | 406 | 1.43 | 9.9% | 77.2 | 9/9 | 1.00 | 0.56 | 0.23 | 4 | 3.6% | 0.49 | 0.63 | 6.5% | 5.5% | 5.0% | 6.7%/5.3% | 4.6 (interpolated) | pass | 0.061 (unverified) | -0.98 |
| 230 | `cfg_2b8d` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=8, entry_z=-1.5, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 30/166/21 | 217 | 7.4% | 1.4% | 0.77 | -2.5% | 355 | 1.36 | 11.5% | 90.2 | 10/10 | 1.00 | 0.67 | 0.10 | 3 | 2.8% | 0.60 | 0.68 | 6.1% | 4.8% | 2.6% | 6.4%/4.8% | 3.9 (interpolated) | pass | 0.051 (unverified) | 0.16 |
| 231 | `cfg_4026` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=12, entry_z=-2.25, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 40/142/38 | 220 | 7.1% | 1.4% | 0.84 | -2.8% | 529 | 1.37 | 8.9% | 90.9 | 9/9 | 0.78 | 0.52 | 0.32 | 4 | 2.8% | 0.59 | 0.62 | 5.9% | 4.8% | 0.2% | 5.6%/4.2% | 3.9 (interpolated) | pass | 0.075 (unverified) | -0.01 |
| 232 | `cfg_b70a` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=8, entry_z=-1.75, exit_z=0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.0 | 17/182/14 | 213 | 7.2% | 1.4% | 0.78 | -3.2% | 516 | 1.42 | 9.3% | 88.5 | 10/10 | 0.90 | 0.56 | 0.23 | 4 | 1.7% | 0.76 | 0.76 | 5.9% | 4.8% | 2.6% | 6.3%/4.3% | 3.8 (interpolated) | pass | 0.059 (unverified) | -0.17 |
| 233 | `cfg_868e` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=15, entry_z=-1.5, exit_z=0.5, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.5 | 16/168/10 | 194 | 7.4% | 1.4% | 0.80 | -2.6% | 451 | 1.41 | 10.6% | 81.2 | 9/9 | 1.00 | 0.57 | 0.23 | 3 | 1.0% | 0.85 | 0.65 | 6.1% | 4.8% | 3.5% | 6.2%/4.4% | 4.3 (interpolated) | pass | 0.062 (unverified) | -0.42 |
| 234 | `cfg_ad5c` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-1.5, exit_z=0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 44/119/0 | 163 | 11.0% | 2.1% | 0.87 | -2.8% | 404 | 1.49 | 15.2% | 68.0 | 7/7 | 1.00 | 0.50 | 0.37 | 4 | 5.4% | 0.49 | 0.50 | 9.8% | 8.7% | 11.4% | 9.8%/7.6% | 6.3 (interpolated) | pass | 0.085 (unverified) | -0.67 |
| 235 | `cfg_c5ff` | timeframe=1h, mean_type=sma, mean_lookback=100, std_lookback=8, entry_z=-1.75, exit_z=0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.5 | 17/182/9 | 208 | 7.4% | 1.4% | 0.80 | -3.3% | 515 | 1.44 | 9.1% | 86.4 | 10/10 | 1.00 | 0.59 | 0.21 | 4 | 1.7% | 0.77 | 0.74 | 6.2% | 5.0% | 1.7% | 6.5%/4.9% | 4.0 (interpolated) | pass | 0.062 (unverified) | -0.07 |
| 236 | `cfg_8b2c` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=8, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 32/127/0 | 159 | 6.0% | 1.2% | 0.77 | -2.8% | 279 | 1.44 | 9.9% | 66.4 | 10/10 | 1.00 | 0.69 | 0.08 | 4 | 1.8% | 0.69 | 0.64 | 5.0% | 4.0% | 3.4% | 5.0%/3.3% | 4.2 (interpolated) | pass | 0.061 (unverified) | -0.65 |
| 237 | `cfg_7c2c` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=8, entry_z=-2.5, exit_z=0.5, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 31/140/0 | 171 | 9.0% | 1.7% | 0.82 | -2.7% | 442 | 1.43 | 12.7% | 70.8 | 9/9 | 0.89 | 0.48 | 0.34 | 4 | 5.5% | 0.39 | 0.50 | 8.1% | 7.0% | 1.5% | 7.6%/6.0% | 5.3 (interpolated) | pass | 0.067 (unverified) | -0.00 |
| 238 | `cfg_3470` | timeframe=1h, mean_type=sma, mean_lookback=80, std_lookback=15, entry_z=-1.5, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 56/109/0 | 165 | 10.2% | 2.0% | 0.78 | -4.0% | 423 | 1.43 | 14.9% | 68.9 | 8/8 | 1.00 | 0.53 | 0.25 | 4 | 4.4% | 0.56 | 0.54 | 9.2% | 8.1% | 8.7% | 9.3%/6.0% | 5.7 (interpolated) | pass | 0.060 (unverified) | -0.58 |
| 239 | `cfg_da22` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=8, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 71/132/27 | 230 | 7.5% | 1.5% | 0.82 | -2.1% | 310 | 1.36 | 13.0% | 95.5 | 11/11 | 0.91 | 0.52 | 0.30 | 3 | 3.6% | 0.51 | 0.49 | 6.1% | 4.7% | 2.1% | 6.6%/4.8% | 3.7 (interpolated) | pass | 0.067 (unverified) | -0.19 |
| 240 | `cfg_4337` | timeframe=1h, mean_type=ema, mean_lookback=90, std_lookback=10, entry_z=-1.5, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 86/103/0 | 189 | 9.7% | 1.9% | 0.81 | -3.2% | 413 | 1.39 | 15.8% | 78.3 | 9/9 | 1.00 | 0.55 | 0.25 | 4 | 4.2% | 0.56 | 0.51 | 8.5% | 7.5% | 6.2% | 8.7%/6.6% | 5.3 (interpolated) | pass | 0.072 (unverified) | -0.16 |
| 241 | `cfg_473f` | timeframe=1h, mean_type=sma, mean_lookback=90, std_lookback=8, entry_z=-2.5, exit_z=0.0, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 37/135/0 | 172 | 8.7% | 1.7% | 0.83 | -2.6% | 442 | 1.42 | 12.7% | 71.2 | 10/10 | 0.90 | 0.52 | 0.31 | 4 | 5.1% | 0.41 | 0.52 | 7.4% | 6.6% | 1.4% | 7.7%/5.4% | 5.0 (interpolated) | pass | 0.069 (unverified) | 0.04 |
| 242 | `cfg_71a8` | timeframe=1h, mean_type=ema, mean_lookback=120, std_lookback=8, entry_z=-1.75, exit_z=0.0, max_holding_bars=6, entry_confirmation=none, stop_atr_multiple=none | 42/136/0 | 178 | 8.1% | 1.6% | 0.76 | -2.5% | 328 | 1.41 | 13.0% | 73.5 | 10/10 | 1.00 | 0.59 | 0.17 | 3 | 4.1% | 0.50 | 0.60 | 7.2% | 6.1% | 8.7% | 7.3%/5.4% | 4.9 (interpolated) | pass | 0.047 (unverified) | 0.09 |
| 243 | `cfg_5bed` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=6, entry_z=-2.0, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 94/109/0 | 203 | 10.5% | 2.0% | 0.77 | -3.7% | 536 | 1.36 | 16.3% | 82.9 | 8/8 | 1.00 | 0.57 | 0.21 | 4 | 4.6% | 0.57 | 0.51 | 9.1% | 8.0% | -2.7% | 9.6%/7.1% | 5.1 (interpolated) | pass | 0.058 (unverified) | -0.43 |
| 244 | `cfg_74f0` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=8, entry_z=-1.75, exit_z=-0.5, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 81/106/0 | 187 | 10.5% | 2.0% | 0.85 | -2.6% | 333 | 1.43 | 15.6% | 78.0 | 10/10 | 1.00 | 0.58 | 0.27 | 3 | 5.9% | 0.44 | 0.48 | 9.1% | 7.8% | 5.2% | 8.8%/7.2% | 5.4 (interpolated) | pass | 0.082 (unverified) | -0.07 |
| 245 | `cfg_a675` | timeframe=1h, mean_type=sma, mean_lookback=70, std_lookback=6, entry_z=-2.0, exit_z=-0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 55/165/50 | 270 | 7.8% | 1.5% | 0.83 | -2.5% | 204 | 1.34 | 10.7% | 111.7 | 9/9 | 1.00 | 0.58 | 0.25 | 4 | 2.4% | 0.69 | 0.50 | 6.5% | 5.0% | 0.6% | 7.0%/5.2% | 3.5 (interpolated) | pass | 0.086 (unverified) | -0.63 |
| 246 | `cfg_66e7` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=12, entry_z=-1.5, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=2.0 | 76/131/25 | 232 | 7.7% | 1.5% | 0.76 | -4.7% | 704 | 1.37 | 11.1% | 93.1 | 9/9 | 1.00 | 0.56 | 0.20 | 3 | 1.3% | 0.83 | 0.59 | 6.4% | 5.0% | 2.8% | 6.9%/4.9% | 3.7 (interpolated) | pass | 0.052 (unverified) | -0.51 |
| 247 | `cfg_8933` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=8, entry_z=-1.75, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 70/135/0 | 205 | 6.7% | 1.3% | 0.79 | -2.4% | 333 | 1.37 | 12.1% | 84.7 | 10/10 | 0.90 | 0.62 | 0.18 | 4 | 3.3% | 0.49 | 0.53 | 5.4% | 4.2% | 5.2% | 6.0%/4.1% | 3.7 (interpolated) | pass | 0.060 (unverified) | -0.27 |
| 248 | `cfg_e7e2` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=10, entry_z=-1.75, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 92/93/0 | 185 | 8.7% | 1.7% | 0.76 | -4.0% | 359 | 1.37 | 14.9% | 76.7 | 9/9 | 0.89 | 0.51 | 0.25 | 3 | 2.2% | 0.75 | 0.54 | 7.5% | 6.1% | 5.0% | 7.5%/5.6% | 4.9 (interpolated) | pass | 0.056 (unverified) | -0.05 |
| 249 | `cfg_8301` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=6, entry_z=-1.75, exit_z=-1.0, max_holding_bars=4, entry_confirmation=none, stop_atr_multiple=none | 65/120/0 | 185 | 6.8% | 1.3% | 0.78 | -3.6% | 234 | 1.41 | 9.3% | 77.5 | 8/8 | 1.00 | 0.58 | 0.20 | 5 | 2.7% | 0.59 | 0.61 | 5.7% | 4.5% | 5.5% | 6.1%/4.6% | 4.2 (interpolated) | pass | 0.062 (unverified) | -0.80 |
| 250 | `cfg_5499` | timeframe=1h, mean_type=sma, mean_lookback=60, std_lookback=6, entry_z=-2.0, exit_z=0.5, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=2.5 | 37/184/14 | 235 | 7.2% | 1.4% | 0.77 | -2.9% | 643 | 1.33 | 10.0% | 95.6 | 8/8 | 1.00 | 0.48 | 0.30 | 4 | 2.3% | 0.69 | 0.63 | 5.7% | 4.3% | -3.6% | 6.2%/4.2% | 3.4 (interpolated) | pass | 0.056 (unverified) | -1.34 |
| 251 | `cfg_a243` | timeframe=1h, mean_type=ema, mean_lookback=100, std_lookback=12, entry_z=-1.75, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 22/186/0 | 208 | 6.1% | 1.2% | 0.76 | -2.5% | 662 | 1.36 | 9.2% | 85.8 | 10/10 | 0.90 | 0.55 | 0.20 | 3 | 0.9% | 0.85 | 0.66 | 4.9% | 3.6% | 5.4% | 5.4%/4.1% | 3.6 (interpolated) | pass | 0.055 (unverified) | -0.39 |
| 252 | `cfg_b072` | timeframe=1h, mean_type=sma, mean_lookback=120, std_lookback=8, entry_z=-1.75, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.5 | 32/127/6 | 165 | 6.0% | 1.2% | 0.78 | -2.7% | 253 | 1.42 | 10.2% | 69.0 | 11/11 | 1.00 | 0.53 | 0.25 | 4 | 2.1% | 0.64 | 0.63 | 5.0% | 3.9% | 0.5% | 4.7%/3.3% | 4.1 (interpolated) | pass | 0.065 (unverified) | -0.57 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 2.2% / 1.64 / 37 | 0.0% / 0.02 / 29 | 2.8% / 1.53 / 38 | 1.1% / 0.68 / 40 | 5.2% / 2.12 / 46 |
| 2 | 2.2% / 1.54 / 36 | 0.3% / 0.19 / 29 | 3.2% / 1.71 / 37 | 1.3% / 0.78 / 40 | 5.1% / 1.93 / 45 |
| 3 | 2.2% / 1.23 / 40 | -0.8% / -0.69 / 31 | 4.5% / 2.34 / 44 | 1.7% / 1.08 / 41 | 5.6% / 2.09 / 46 |
| 4 | 2.3% / 1.28 / 40 | -0.5% / -0.35 / 31 | 4.5% / 2.37 / 44 | 1.8% / 1.17 / 41 | 5.5% / 2.03 / 45 |
| 5 | 0.9% / 0.50 / 38 | -1.3% / -0.95 / 41 | 6.0% / 2.79 / 38 | 1.4% / 0.92 / 44 | 6.2% / 2.43 / 41 |
| 6 | 2.2% / 1.15 / 39 | -1.3% / -0.93 / 35 | 5.9% / 2.61 / 42 | 0.9% / 0.49 / 37 | 5.7% / 1.89 / 45 |
| 7 | 0.6% / 0.36 / 37 | 0.6% / 0.47 / 32 | 1.8% / 1.16 / 41 | 1.1% / 0.73 / 42 | 6.5% / 2.56 / 44 |
| 8 | 2.9% / 1.71 / 41 | -1.2% / -1.06 / 37 | 5.1% / 2.51 / 45 | 0.3% / 0.18 / 39 | 5.6% / 1.83 / 48 |
| 9 | 0.6% / 0.36 / 37 | 0.4% / 0.35 / 32 | 2.1% / 1.35 / 41 | 1.1% / 0.71 / 42 | 6.6% / 2.60 / 44 |
| 10 | 2.0% / 1.07 / 40 | -1.5% / -1.28 / 35 | 5.6% / 2.56 / 43 | 0.8% / 0.43 / 37 | 5.8% / 1.92 / 46 |
| 11 | 1.2% / 0.81 / 40 | 0.3% / 0.26 / 38 | 1.9% / 0.85 / 45 | 1.6% / 1.02 / 44 | 5.9% / 2.60 / 45 |
| 12 | 0.6% / 0.35 / 41 | -2.3% / -1.81 / 44 | 4.6% / 2.50 / 39 | 0.9% / 0.65 / 46 | 6.6% / 2.45 / 45 |
| 13 | 1.4% / 0.89 / 40 | 0.5% / 0.40 / 38 | 1.4% / 0.62 / 44 | 1.7% / 1.07 / 44 | 5.6% / 2.46 / 45 |
| 14 | 3.0% / 1.86 / 46 | -0.9% / -0.72 / 41 | 4.3% / 2.09 / 38 | 1.8% / 1.21 / 44 | 3.2% / 1.43 / 42 |
| 15 | 1.5% / 0.90 / 43 | -1.6% / -1.27 / 51 | 4.9% / 2.55 / 42 | 0.7% / 0.44 / 51 | 5.7% / 2.55 / 48 |
| 16 | 1.0% / 0.52 / 43 | -0.9% / -0.65 / 49 | 5.8% / 2.68 / 42 | 0.9% / 0.55 / 51 | 6.5% / 2.42 / 43 |
| 17 | 1.6% / 1.03 / 38 | -1.8% / -1.40 / 43 | 5.1% / 2.47 / 41 | -0.1% / -0.06 / 44 | 7.6% / 2.66 / 48 |
| 18 | 3.3% / 2.02 / 47 | -0.8% / -0.61 / 41 | 4.0% / 2.05 / 38 | 1.8% / 1.21 / 44 | 3.3% / 1.48 / 42 |
| 19 | 3.0% / 1.75 / 41 | -0.9% / -0.65 / 37 | 5.1% / 2.50 / 45 | 0.3% / 0.22 / 39 | 5.6% / 1.83 / 47 |
| 20 | 1.9% / 1.19 / 41 | -1.7% / -1.48 / 45 | 4.5% / 2.46 / 40 | 0.4% / 0.29 / 47 | 5.8% / 2.51 / 47 |
| 21 | 1.8% / 1.21 / 44 | -2.1% / -1.97 / 48 | 4.9% / 2.58 / 41 | 0.5% / 0.35 / 50 | 4.9% / 2.15 / 48 |
| 22 | 0.5% / 0.28 / 35 | -1.0% / -0.73 / 40 | 6.3% / 2.94 / 38 | 0.3% / 0.23 / 40 | 6.4% / 2.29 / 42 |
| 23 | 0.7% / 0.33 / 35 | -1.4% / -0.94 / 39 | 5.9% / 2.57 / 33 | 1.5% / 0.74 / 38 | 6.9% / 2.11 / 41 |
| 24 | 1.0% / 0.48 / 36 | -0.9% / -0.60 / 40 | 6.0% / 2.42 / 35 | 2.1% / 1.07 / 42 | 5.2% / 1.77 / 39 |
| 25 | -0.2% / -0.12 / 50 | 0.1% / 0.09 / 39 | 2.8% / 1.87 / 42 | 1.3% / 0.92 / 46 | 5.6% / 1.95 / 49 |
| 26 | -0.4% / -0.19 / 37 | -1.0% / -0.66 / 44 | 5.7% / 2.29 / 38 | 0.3% / 0.19 / 38 | 6.0% / 2.04 / 44 |
| 27 | 0.2% / 0.16 / 42 | -0.0% / 0.01 / 39 | 3.3% / 1.67 / 37 | 0.6% / 0.42 / 43 | 5.9% / 2.35 / 48 |
| 28 | 2.3% / 1.24 / 45 | 0.6% / 0.67 / 35 | 4.3% / 1.99 / 41 | 2.0% / 1.29 / 41 | 2.4% / 0.80 / 49 |
| 29 | 1.8% / 0.85 / 34 | -1.7% / -1.03 / 37 | 5.3% / 2.07 / 33 | 0.2% / 0.11 / 38 | 6.6% / 1.96 / 38 |
| 30 | 1.3% / 1.19 / 37 | 1.3% / 1.02 / 29 | 2.6% / 1.49 / 39 | 1.4% / 0.96 / 42 | 3.9% / 1.64 / 47 |
| 31 | 2.4% / 1.26 / 45 | 0.7% / 0.68 / 36 | 4.6% / 2.17 / 44 | 1.8% / 1.24 / 41 | 2.7% / 0.91 / 50 |
| 32 | -0.3% / -0.18 / 38 | 0.6% / 0.53 / 29 | 1.9% / 1.15 / 39 | 1.1% / 0.93 / 43 | 4.1% / 1.73 / 48 |
| 33 | 1.0% / 0.51 / 39 | 0.0% / 0.02 / 38 | 4.5% / 1.78 / 38 | 1.2% / 0.74 / 39 | 7.2% / 2.35 / 47 |
| 34 | 1.4% / 0.76 / 46 | -1.9% / -1.36 / 37 | 6.8% / 3.00 / 47 | 1.1% / 0.62 / 48 | 4.5% / 1.45 / 52 |
| 35 | 0.0% / 0.01 / 50 | 0.5% / 0.37 / 39 | 2.8% / 1.76 / 40 | 1.3% / 0.89 / 46 | 5.2% / 1.68 / 49 |
| 36 | 2.5% / 1.55 / 40 | 0.9% / 0.80 / 38 | 2.3% / 1.54 / 43 | 0.7% / 0.52 / 40 | 1.4% / 0.51 / 48 |
| 37 | 0.1% / 0.07 / 36 | -1.3% / -0.83 / 44 | 4.8% / 2.07 / 37 | 0.6% / 0.47 / 38 | 6.3% / 2.12 / 44 |
| 38 | -0.0% / 0.00 / 38 | 0.7% / 0.52 / 29 | 1.6% / 0.99 / 39 | 1.1% / 0.95 / 43 | 4.6% / 1.88 / 48 |
| 39 | 1.0% / 0.96 / 36 | 1.3% / 1.02 / 29 | 2.7% / 1.49 / 39 | 1.2% / 0.87 / 41 | 4.0% / 1.65 / 47 |
| 40 | 2.1% / 1.06 / 38 | -2.2% / -2.27 / 34 | 5.3% / 2.49 / 40 | 0.4% / 0.25 / 37 | 3.9% / 1.37 / 43 |
| 41 | 2.7% / 1.67 / 42 | 1.2% / 0.99 / 40 | 1.8% / 1.18 / 47 | 1.6% / 1.09 / 43 | 1.4% / 0.52 / 48 |
| 42 | 0.5% / 0.27 / 35 | -2.2% / -1.59 / 39 | 5.8% / 2.60 / 34 | 1.0% / 0.47 / 39 | 4.8% / 1.55 / 41 |
| 43 | 0.4% / 0.29 / 32 | -0.2% / -0.11 / 37 | 3.4% / 1.43 / 38 | 0.4% / 0.22 / 46 | 5.1% / 2.42 / 39 |
| 44 | -0.3% / -0.19 / 35 | -1.1% / -0.85 / 41 | 5.4% / 2.58 / 37 | 0.6% / 0.44 / 40 | 4.5% / 1.75 / 42 |
| 45 | 1.5% / 0.74 / 37 | -2.0% / -1.98 / 34 | 3.0% / 1.47 / 42 | 1.2% / 0.82 / 34 | 6.1% / 1.98 / 45 |
| 46 | 1.9% / 0.97 / 38 | -2.0% / -1.98 / 34 | 3.9% / 1.89 / 43 | 0.8% / 0.51 / 35 | 5.4% / 1.82 / 46 |
| 47 | 1.0% / 0.54 / 45 | -0.7% / -0.53 / 41 | 4.0% / 1.68 / 42 | 0.9% / 0.57 / 48 | 6.2% / 2.15 / 49 |
| 48 | -0.1% / -0.04 / 41 | -0.2% / -0.13 / 50 | 4.0% / 1.64 / 43 | 0.4% / 0.25 / 47 | 6.2% / 2.09 / 49 |
| 49 | 2.2% / 1.13 / 40 | -2.1% / -1.65 / 39 | 5.4% / 2.39 / 35 | 2.2% / 1.40 / 40 | 3.4% / 1.32 / 38 |
| 50 | 1.3% / 0.86 / 31 | 0.0% / 0.02 / 33 | 3.5% / 1.54 / 36 | 1.5% / 0.89 / 42 | 5.3% / 2.43 / 39 |
| 51 | 1.0% / 0.56 / 45 | -1.9% / -1.36 / 37 | 6.6% / 2.95 / 47 | 1.1% / 0.60 / 48 | 4.6% / 1.47 / 52 |
| 52 | -0.4% / -0.21 / 42 | -0.1% / -0.10 / 50 | 4.6% / 1.97 / 43 | 0.6% / 0.40 / 47 | 6.0% / 2.03 / 49 |
| 53 | 1.8% / 0.85 / 34 | -1.2% / -0.67 / 37 | 5.3% / 1.95 / 33 | -0.4% / -0.18 / 35 | 6.1% / 1.83 / 37 |
| 54 | 0.0% / 0.01 / 39 | -1.9% / -1.70 / 47 | 6.1% / 3.04 / 44 | -1.2% / -0.72 / 54 | 5.3% / 2.02 / 49 |
| 55 | 2.7% / 1.62 / 44 | -1.4% / -1.01 / 42 | 4.0% / 2.00 / 36 | 1.2% / 0.74 / 43 | 3.1% / 1.26 / 39 |
| 56 | -0.2% / -0.13 / 41 | -0.2% / -0.15 / 39 | 3.9% / 1.82 / 37 | 0.6% / 0.42 / 43 | 5.7% / 2.24 / 48 |
| 57 | -0.3% / -0.20 / 35 | -0.8% / -0.60 / 41 | 5.5% / 2.57 / 37 | 0.7% / 0.49 / 40 | 4.3% / 1.67 / 42 |
| 58 | 1.4% / 0.98 / 38 | -1.6% / -1.24 / 45 | 3.2% / 1.72 / 36 | -1.0% / -0.54 / 46 | 6.5% / 2.59 / 45 |
| 59 | 2.0% / 1.04 / 39 | -2.6% / -2.46 / 35 | 5.5% / 2.40 / 43 | 0.3% / 0.20 / 37 | 3.8% / 1.34 / 44 |
| 60 | 2.6% / 1.19 / 38 | -0.6% / -0.37 / 30 | 4.5% / 1.88 / 39 | -0.2% / -0.13 / 35 | 4.4% / 1.19 / 44 |
| 61 | -0.3% / -0.16 / 35 | -0.1% / -0.09 / 34 | 5.6% / 2.43 / 48 | 0.8% / 0.63 / 34 | 3.8% / 1.36 / 34 |
| 62 | 0.4% / 0.18 / 34 | -0.3% / -0.19 / 33 | 6.4% / 2.30 / 34 | 0.6% / 0.28 / 38 | 7.7% / 2.18 / 44 |
| 63 | 0.5% / 0.34 / 38 | -1.8% / -1.45 / 37 | 3.9% / 1.91 / 38 | 0.3% / 0.21 / 43 | 6.4% / 2.54 / 46 |
| 64 | 0.3% / 0.26 / 40 | -2.1% / -1.86 / 44 | 4.3% / 2.24 / 38 | 0.5% / 0.36 / 44 | 5.6% / 2.16 / 43 |
| 65 | 1.3% / 0.88 / 41 | -1.7% / -1.52 / 44 | 4.3% / 2.13 / 41 | -0.2% / -0.12 / 48 | 4.8% / 1.93 / 48 |
| 66 | 0.8% / 0.61 / 37 | -1.7% / -1.46 / 45 | 3.8% / 1.86 / 36 | -0.9% / -0.53 / 46 | 6.2% / 2.45 / 45 |
| 67 | -0.5% / -0.27 / 42 | -1.3% / -0.85 / 45 | 5.7% / 2.36 / 40 | 0.7% / 0.46 / 42 | 6.2% / 2.31 / 41 |
| 68 | 1.8% / 0.81 / 35 | -2.4% / -1.45 / 38 | 5.4% / 1.99 / 34 | 2.6% / 1.17 / 42 | 5.4% / 1.72 / 35 |
| 69 | 0.6% / 0.43 / 38 | -1.8% / -1.56 / 43 | 4.9% / 2.40 / 38 | 0.6% / 0.43 / 42 | 5.1% / 2.16 / 42 |
| 70 | -1.0% / -0.58 / 35 | -1.3% / -1.02 / 36 | 4.5% / 2.23 / 36 | 1.0% / 0.77 / 40 | 5.4% / 2.16 / 44 |
| 71 | -0.6% / -0.28 / 43 | -0.5% / -0.40 / 37 | 5.3% / 2.29 / 53 | 0.3% / 0.26 / 40 | 4.4% / 1.70 / 39 |
| 72 | 2.4% / 1.22 / 44 | -2.2% / -1.74 / 45 | 5.1% / 2.21 / 39 | 1.5% / 0.80 / 48 | 3.1% / 1.09 / 43 |
| 73 | 1.3% / 0.77 / 36 | -1.4% / -1.01 / 37 | 3.7% / 1.96 / 36 | 0.3% / 0.18 / 40 | 5.4% / 1.97 / 44 |
| 74 | 2.1% / 1.29 / 36 | -1.0% / -0.81 / 39 | 2.9% / 1.60 / 36 | -0.4% / -0.21 / 42 | 5.5% / 2.05 / 46 |
| 75 | 0.4% / 0.17 / 31 | 0.1% / 0.08 / 37 | 6.2% / 2.20 / 33 | 0.2% / 0.13 / 38 | 6.6% / 1.85 / 41 |
| 76 | 0.1% / 0.04 / 33 | 0.1% / 0.07 / 30 | 4.5% / 1.68 / 30 | 0.5% / 0.28 / 36 | 9.2% / 2.42 / 42 |
| 77 | 2.6% / 1.31 / 45 | -2.0% / -1.46 / 45 | 4.3% / 2.05 / 39 | 1.4% / 0.74 / 48 | 3.1% / 1.10 / 43 |
| 78 | 0.1% / 0.08 / 36 | -0.7% / -0.42 / 37 | 5.5% / 2.24 / 37 | 0.5% / 0.32 / 36 | 4.9% / 1.88 / 40 |
| 79 | 1.6% / 0.87 / 38 | -2.8% / -2.07 / 42 | 5.6% / 2.60 / 38 | -0.2% / -0.10 / 44 | 7.6% / 2.33 / 47 |
| 80 | 3.3% / 1.58 / 36 | -2.1% / -1.30 / 38 | 4.8% / 1.96 / 35 | -0.5% / -0.23 / 39 | 4.9% / 1.57 / 40 |
| 81 | 0.5% / 0.32 / 40 | 0.6% / 0.43 / 36 | 3.2% / 1.79 / 43 | 1.5% / 1.17 / 50 | 4.3% / 1.65 / 45 |
| 82 | 0.3% / 0.22 / 40 | 0.6% / 0.43 / 36 | 3.1% / 1.76 / 43 | 1.5% / 1.17 / 50 | 4.3% / 1.64 / 45 |
| 83 | 0.6% / 0.48 / 40 | 0.1% / 0.06 / 36 | 1.5% / 0.64 / 44 | 0.6% / 0.59 / 42 | 4.5% / 1.76 / 50 |
| 84 | -0.7% / -0.36 / 35 | -0.5% / -0.34 / 37 | 4.5% / 1.96 / 36 | 0.9% / 0.52 / 36 | 5.1% / 1.93 / 40 |
| 85 | 2.4% / 1.08 / 37 | -0.6% / -0.37 / 30 | 4.1% / 1.72 / 38 | 0.2% / 0.12 / 34 | 4.5% / 1.21 / 43 |
| 86 | 1.0% / 0.63 / 45 | -1.2% / -1.09 / 47 | 4.2% / 2.07 / 44 | -0.8% / -0.59 / 54 | 5.2% / 2.04 / 53 |
| 87 | 0.1% / 0.09 / 43 | -2.0% / -1.88 / 42 | 4.5% / 2.21 / 42 | -0.6% / -0.40 / 51 | 6.1% / 2.18 / 51 |
| 88 | -0.1% / -0.06 / 42 | 0.4% / 0.30 / 52 | 4.9% / 2.09 / 44 | 1.0% / 0.68 / 49 | 4.4% / 1.49 / 52 |
| 89 | 0.9% / 0.59 / 36 | -0.6% / -0.45 / 36 | 3.0% / 1.25 / 39 | 0.1% / 0.10 / 45 | 4.8% / 2.39 / 39 |
| 90 | 0.6% / 0.39 / 37 | -1.5% / -1.16 / 36 | 3.9% / 1.95 / 38 | 0.6% / 0.42 / 41 | 5.3% / 2.13 / 44 |
| 91 | 1.1% / 0.66 / 39 | -0.0% / -0.04 / 32 | 5.2% / 2.54 / 44 | -0.5% / -0.42 / 36 | 2.9% / 1.15 / 35 |
| 92 | 0.9% / 0.55 / 43 | -0.2% / -0.25 / 38 | 3.2% / 1.61 / 39 | -0.4% / -0.28 / 41 | 4.6% / 1.95 / 43 |
| 93 | 0.6% / 0.48 / 34 | -1.2% / -1.05 / 38 | 4.8% / 2.11 / 44 | 2.0% / 1.44 / 33 | 1.1% / 0.52 / 35 |
| 94 | 2.0% / 1.05 / 38 | 0.7% / 0.51 / 33 | 3.1% / 1.69 / 38 | 0.6% / 0.36 / 37 | 3.2% / 0.94 / 44 |
| 95 | -0.0% / -0.01 / 38 | 0.3% / 0.23 / 49 | 4.7% / 1.99 / 40 | -0.1% / -0.03 / 41 | 5.0% / 1.80 / 48 |
| 96 | 1.7% / 0.87 / 37 | 0.8% / 0.60 / 30 | 2.6% / 1.40 / 35 | 1.4% / 0.89 / 36 | 3.5% / 1.01 / 42 |
| 97 | 3.1% / 1.39 / 36 | -1.1% / -0.65 / 28 | 2.3% / 1.05 / 33 | 0.9% / 0.49 / 35 | 5.8% / 1.49 / 42 |
| 98 | 1.6% / 0.75 / 37 | -1.3% / -0.86 / 33 | 3.1% / 1.04 / 40 | 1.5% / 0.69 / 35 | 6.9% / 1.85 / 42 |
| 99 | 0.3% / 0.25 / 34 | -1.2% / -1.02 / 39 | 5.1% / 2.27 / 44 | 2.0% / 1.42 / 33 | 1.0% / 0.49 / 35 |
| 100 | -0.9% / -0.45 / 55 | -0.4% / -0.32 / 47 | 4.3% / 1.88 / 41 | 0.4% / 0.22 / 58 | 6.1% / 2.18 / 52 |
| 101 | 1.7% / 0.82 / 40 | -3.1% / -2.18 / 38 | 5.2% / 2.34 / 33 | 2.1% / 1.23 / 39 | 2.6% / 0.91 / 37 |
| 102 | 0.5% / 0.30 / 41 | -0.2% / -0.12 / 40 | 3.9% / 1.64 / 39 | 0.8% / 0.53 / 40 | 5.5% / 1.82 / 49 |
| 103 | 0.0% / 0.01 / 42 | 0.0% / 0.04 / 32 | 2.8% / 1.59 / 46 | 1.9% / 1.30 / 44 | 2.7% / 0.97 / 51 |
| 104 | 0.6% / 0.44 / 41 | 0.4% / 0.35 / 39 | 1.9% / 0.83 / 45 | 0.4% / 0.31 / 43 | 4.5% / 1.81 / 50 |
| 105 | -0.2% / -0.11 / 40 | -2.2% / -1.66 / 43 | 5.0% / 2.47 / 38 | 0.9% / 0.46 / 46 | 5.5% / 1.77 / 45 |
| 106 | 1.5% / 0.94 / 37 | -1.9% / -1.45 / 41 | 2.9% / 1.54 / 38 | 1.3% / 0.85 / 46 | 3.8% / 1.47 / 43 |
| 107 | 1.1% / 0.59 / 42 | -0.3% / -0.24 / 40 | 4.0% / 1.67 / 40 | 0.8% / 0.51 / 41 | 5.4% / 1.93 / 49 |
| 108 | 1.1% / 0.67 / 43 | -0.0% / -0.04 / 34 | 5.0% / 2.33 / 50 | -1.0% / -0.77 / 43 | 3.7% / 1.39 / 40 |
| 109 | -0.6% / -0.33 / 41 | -1.2% / -0.78 / 45 | 4.9% / 2.04 / 40 | 0.5% / 0.34 / 42 | 6.5% / 2.36 / 41 |
| 110 | 2.0% / 0.94 / 38 | -2.6% / -1.48 / 35 | 4.8% / 1.85 / 31 | 2.1% / 1.07 / 37 | 3.6% / 1.08 / 35 |
| 111 | 0.1% / 0.07 / 41 | 0.0% / 0.04 / 32 | 2.7% / 1.52 / 45 | 2.1% / 1.58 / 43 | 2.7% / 1.04 / 51 |
| 112 | 0.0% / 0.03 / 29 | -0.1% / -0.10 / 37 | 5.5% / 2.70 / 47 | 0.9% / 0.68 / 30 | 2.4% / 1.02 / 32 |
| 113 | 0.7% / 0.49 / 42 | -1.3% / -1.14 / 43 | 3.0% / 1.45 / 42 | -0.2% / -0.15 / 49 | 4.9% / 2.14 / 48 |
| 114 | 0.6% / 0.32 / 43 | 1.5% / 1.16 / 39 | 1.5% / 0.74 / 41 | -0.4% / -0.25 / 43 | 5.9% / 2.20 / 50 |
| 115 | -0.4% / -0.22 / 33 | -0.4% / -0.25 / 35 | 1.5% / 0.90 / 29 | 1.7% / 1.10 / 38 | 4.7% / 1.75 / 37 |
| 116 | 0.4% / 0.25 / 41 | 0.8% / 0.79 / 34 | 3.5% / 1.55 / 43 | -0.6% / -0.37 / 44 | 3.3% / 1.25 / 51 |
| 117 | -0.2% / -0.08 / 35 | -0.3% / -0.24 / 31 | 6.1% / 2.39 / 45 | 1.1% / 0.63 / 34 | 3.2% / 0.98 / 33 |
| 118 | -1.0% / -0.58 / 35 | -1.0% / -0.77 / 36 | 4.6% / 2.24 / 36 | 1.4% / 1.11 / 39 | 5.2% / 2.11 / 44 |
| 119 | -0.5% / -0.23 / 36 | -0.4% / -0.32 / 32 | 6.6% / 2.60 / 45 | 1.1% / 0.59 / 34 | 2.9% / 0.96 / 33 |
| 120 | 1.2% / 0.88 / 34 | -0.4% / -0.29 / 33 | 3.0% / 1.21 / 37 | 0.2% / 0.12 / 43 | 4.8% / 2.39 / 39 |
| 121 | 1.0% / 0.74 / 42 | -1.8% / -1.63 / 41 | 3.2% / 1.49 / 40 | 0.1% / 0.08 / 47 | 4.5% / 2.03 / 47 |
| 122 | 1.3% / 0.58 / 38 | 0.1% / 0.06 / 33 | 5.1% / 1.90 / 44 | 1.0% / 0.48 / 36 | 5.3% / 1.35 / 49 |
| 123 | 1.3% / 0.87 / 43 | 0.9% / 0.62 / 44 | 2.7% / 1.26 / 41 | -0.7% / -0.46 / 43 | 3.1% / 1.18 / 38 |
| 124 | -0.6% / -0.34 / 42 | -0.6% / -0.40 / 41 | 5.4% / 2.11 / 39 | 0.8% / 0.46 / 46 | 3.7% / 1.44 / 43 |
| 125 | 1.4% / 0.66 / 38 | -1.8% / -1.19 / 35 | 3.5% / 1.17 / 43 | 1.7% / 0.82 / 35 | 6.9% / 1.81 / 43 |
| 126 | 1.9% / 0.87 / 40 | 0.2% / 0.15 / 35 | 6.1% / 2.25 / 47 | 0.9% / 0.44 / 37 | 3.5% / 1.03 / 51 |
| 127 | 1.6% / 0.92 / 41 | -0.1% / -0.13 / 34 | 5.0% / 2.34 / 50 | -1.0% / -0.74 / 43 | 2.3% / 0.88 / 38 |
| 128 | 1.0% / 0.66 / 36 | -0.4% / -0.29 / 36 | -0.3% / -0.25 / 31 | 1.5% / 0.94 / 45 | 5.4% / 2.01 / 42 |
| 129 | 1.4% / 0.82 / 38 | -0.1% / -0.13 / 32 | 5.1% / 2.55 / 44 | -0.5% / -0.35 / 36 | 1.6% / 0.66 / 33 |
| 130 | 0.6% / 0.36 / 34 | -0.3% / -0.15 / 35 | 1.5% / 0.91 / 29 | 2.2% / 1.40 / 38 | 3.9% / 1.55 / 37 |
| 131 | 0.8% / 0.43 / 36 | -2.1% / -1.47 / 37 | 3.9% / 1.97 / 38 | 1.7% / 1.11 / 42 | 3.4% / 1.28 / 41 |
| 132 | 1.0% / 0.55 / 40 | 0.2% / 0.12 / 39 | 5.7% / 2.33 / 48 | 0.3% / 0.24 / 38 | 2.6% / 1.05 / 47 |
| 133 | 0.9% / 0.57 / 40 | 0.9% / 0.64 / 38 | 3.5% / 1.25 / 48 | -0.1% / -0.09 / 38 | 2.5% / 0.97 / 51 |
| 134 | 1.7% / 1.14 / 40 | 0.7% / 0.66 / 42 | 3.0% / 1.51 / 41 | -1.4% / -0.84 / 49 | 3.5% / 1.50 / 37 |
| 135 | -1.2% / -0.54 / 56 | -0.1% / -0.07 / 50 | 5.0% / 2.04 / 41 | 0.1% / 0.08 / 56 | 7.3% / 2.60 / 53 |
| 136 | 1.1% / 0.73 / 36 | -0.4% / -0.29 / 36 | -0.3% / -0.21 / 31 | 1.4% / 0.92 / 45 | 4.8% / 1.88 / 42 |
| 137 | 2.4% / 1.16 / 37 | -0.7% / -0.46 / 31 | 4.0% / 1.90 / 37 | 0.7% / 0.36 / 36 | 3.7% / 0.95 / 44 |
| 138 | 0.3% / 0.18 / 43 | 1.3% / 0.91 / 42 | -0.4% / -0.14 / 43 | 2.8% / 1.60 / 51 | 3.4% / 1.51 / 48 |
| 139 | -0.4% / -0.27 / 32 | -0.6% / -0.56 / 37 | 3.7% / 1.72 / 40 | 1.4% / 1.51 / 27 | 2.1% / 1.38 / 26 |
| 140 | 0.7% / 0.49 / 37 | -0.2% / -0.11 / 35 | 3.3% / 1.40 / 39 | -0.0% / -0.02 / 38 | 3.4% / 1.41 / 42 |
| 141 | -1.7% / -0.78 / 45 | 1.2% / 0.88 / 38 | 1.9% / 0.86 / 43 | 0.1% / 0.08 / 44 | 7.1% / 2.38 / 52 |
| 142 | 0.2% / 0.11 / 33 | -0.2% / -0.13 / 35 | 6.1% / 3.01 / 35 | 0.2% / 0.10 / 44 | 2.8% / 1.19 / 33 |
| 143 | 0.6% / 0.32 / 38 | -0.8% / -0.77 / 37 | 7.2% / 3.24 / 42 | -0.5% / -0.37 / 33 | 3.4% / 1.29 / 40 |
| 144 | 1.5% / 0.69 / 39 | -2.9% / -2.08 / 38 | 5.5% / 2.24 / 33 | 2.0% / 1.18 / 39 | 2.8% / 0.95 / 37 |
| 145 | 0.1% / 0.05 / 31 | 0.0% / 0.03 / 35 | 5.1% / 1.90 / 32 | -0.2% / -0.09 / 36 | 7.1% / 1.94 / 39 |
| 146 | 0.9% / 0.50 / 40 | 0.2% / 0.14 / 34 | 2.9% / 1.52 / 44 | -0.3% / -0.21 / 35 | 3.4% / 1.21 / 46 |
| 147 | 2.3% / 1.87 / 39 | 0.2% / 0.15 / 41 | 1.1% / 0.70 / 40 | -0.6% / -0.42 / 39 | 3.7% / 1.66 / 35 |
| 148 | -1.8% / -1.00 / 32 | -0.9% / -0.81 / 37 | 6.0% / 2.60 / 44 | 2.5% / 1.74 / 32 | 1.4% / 0.66 / 34 |
| 149 | -0.9% / -0.56 / 29 | -0.8% / -0.75 / 35 | 6.4% / 2.75 / 43 | 2.4% / 1.68 / 30 | 0.9% / 0.43 / 31 |
| 150 | 0.4% / 0.22 / 38 | -0.7% / -0.74 / 37 | 7.1% / 3.23 / 42 | -0.5% / -0.37 / 33 | 3.4% / 1.30 / 40 |
| 151 | 0.2% / 0.10 / 51 | -1.7% / -1.63 / 49 | 4.5% / 2.38 / 43 | -0.2% / -0.18 / 60 | 4.7% / 1.86 / 55 |
| 152 | -0.1% / -0.09 / 33 | -1.2% / -0.75 / 35 | 5.7% / 3.03 / 35 | 0.1% / 0.08 / 45 | 3.1% / 1.31 / 34 |
| 153 | 0.4% / 0.28 / 36 | -0.6% / -0.44 / 39 | 5.1% / 2.02 / 38 | 0.3% / 0.23 / 38 | 3.7% / 1.46 / 42 |
| 154 | 0.8% / 0.45 / 40 | -0.6% / -0.39 / 41 | 5.7% / 2.54 / 49 | 0.2% / 0.12 / 47 | 2.0% / 0.81 / 49 |
| 155 | 1.6% / 0.78 / 35 | -2.1% / -1.17 / 35 | 5.9% / 2.18 / 33 | 2.6% / 1.19 / 38 | 4.6% / 1.32 / 38 |
| 156 | 0.4% / 0.30 / 44 | 0.9% / 0.62 / 57 | 3.9% / 1.82 / 52 | -0.2% / -0.10 / 58 | 3.4% / 1.23 / 55 |
| 157 | 0.7% / 0.41 / 45 | 0.0% / 0.04 / 49 | 5.7% / 2.25 / 53 | 0.2% / 0.16 / 42 | 2.7% / 0.99 / 50 |
| 158 | 0.3% / 0.18 / 43 | 1.4% / 0.94 / 42 | -0.3% / -0.12 / 43 | 2.8% / 1.59 / 51 | 3.4% / 1.48 / 48 |
| 159 | 1.5% / 0.72 / 34 | -3.3% / -1.90 / 30 | 3.4% / 1.54 / 35 | 0.8% / 0.39 / 36 | 7.4% / 2.02 / 40 |
| 160 | -1.0% / -0.46 / 43 | 1.3% / 0.97 / 38 | 1.6% / 0.71 / 41 | 0.2% / 0.10 / 42 | 6.6% / 2.22 / 49 |
| 161 | -0.4% / -0.22 / 42 | 0.5% / 0.44 / 43 | 1.6% / 0.82 / 39 | 0.2% / 0.15 / 41 | 5.3% / 2.18 / 49 |
| 162 | 0.9% / 0.59 / 36 | -0.7% / -0.52 / 32 | 1.1% / 0.78 / 34 | 1.7% / 1.23 / 35 | 3.7% / 1.51 / 40 |
| 163 | -0.4% / -0.22 / 42 | 0.4% / 0.39 / 43 | 2.1% / 1.00 / 41 | 0.3% / 0.17 / 41 | 5.3% / 2.18 / 49 |
| 164 | 1.0% / 0.68 / 40 | -0.3% / -0.28 / 37 | 3.1% / 1.58 / 38 | -0.4% / -0.25 / 38 | 4.4% / 1.86 / 42 |
| 165 | 1.4% / 0.83 / 40 | -1.6% / -1.20 / 43 | 2.1% / 1.56 / 31 | 2.1% / 1.40 / 42 | 3.4% / 1.33 / 38 |
| 166 | 1.9% / 0.90 / 33 | -3.6% / -2.00 / 28 | 2.6% / 1.14 / 33 | 0.9% / 0.47 / 36 | 7.9% / 2.09 / 40 |
| 167 | 0.2% / 0.08 / 38 | -0.9% / -0.51 / 38 | 4.9% / 1.85 / 36 | 3.1% / 1.51 / 44 | 7.1% / 2.04 / 40 |
| 168 | 0.0% / 0.02 / 36 | 0.9% / 0.58 / 39 | 2.0% / 0.97 / 40 | 0.6% / 0.48 / 42 | 4.5% / 1.41 / 45 |
| 169 | -0.8% / -0.44 / 50 | -0.1% / -0.10 / 39 | 2.7% / 1.77 / 41 | 0.7% / 0.43 / 51 | 6.7% / 2.54 / 45 |
| 170 | 1.5% / 0.85 / 37 | -2.4% / -1.62 / 41 | 4.5% / 2.15 / 35 | 0.3% / 0.18 / 46 | 3.9% / 1.33 / 41 |
| 171 | -0.8% / -0.64 / 31 | -0.1% / -0.05 / 40 | 3.8% / 2.01 / 42 | 1.8% / 1.57 / 29 | 1.7% / 0.96 / 30 |
| 172 | -1.5% / -1.01 / 39 | -1.7% / -1.38 / 40 | 4.1% / 2.00 / 37 | 0.5% / 0.34 / 43 | 6.1% / 2.10 / 47 |
| 173 | 1.0% / 0.48 / 34 | -1.1% / -0.70 / 29 | 1.1% / 0.45 / 34 | 1.5% / 0.92 / 35 | 6.8% / 1.96 / 41 |
| 174 | -0.0% / 0.00 / 36 | 0.3% / 0.23 / 31 | 2.5% / 1.74 / 35 | 0.8% / 0.50 / 39 | 5.2% / 2.12 / 38 |
| 175 | -0.3% / -0.20 / 32 | -0.8% / -0.57 / 36 | 2.2% / 1.17 / 37 | 1.3% / 0.78 / 39 | 3.8% / 2.10 / 35 |
| 176 | 1.7% / 0.98 / 35 | -1.7% / -1.22 / 38 | 4.7% / 2.42 / 33 | -1.0% / -0.58 / 42 | 4.6% / 1.52 / 43 |
| 177 | 2.3% / 1.87 / 39 | 0.3% / 0.26 / 43 | 1.1% / 0.67 / 41 | -1.0% / -0.68 / 42 | 3.7% / 1.66 / 35 |
| 178 | 1.0% / 0.69 / 38 | 1.0% / 0.80 / 44 | 1.5% / 0.90 / 40 | -0.1% / -0.08 / 45 | 3.8% / 1.51 / 38 |
| 179 | -0.2% / -0.16 / 30 | -0.6% / -0.54 / 36 | 3.1% / 1.60 / 38 | 1.4% / 1.49 / 27 | 2.1% / 1.40 / 26 |
| 180 | 0.9% / 0.44 / 36 | -2.4% / -1.62 / 37 | 5.4% / 2.33 / 34 | 2.2% / 1.31 / 41 | 3.3% / 1.08 / 39 |
| 181 | 1.3% / 0.78 / 36 | -0.8% / -0.59 / 32 | 1.1% / 0.82 / 34 | 1.7% / 1.22 / 35 | 3.8% / 1.40 / 40 |
| 182 | 0.5% / 0.32 / 44 | 0.9% / 0.64 / 57 | 3.9% / 1.82 / 52 | -0.3% / -0.19 / 58 | 3.4% / 1.23 / 55 |
| 183 | -1.3% / -1.15 / 42 | -1.7% / -1.52 / 43 | 3.5% / 1.65 / 37 | 0.3% / 0.22 / 44 | 6.4% / 2.39 / 49 |
| 184 | 0.8% / 0.48 / 39 | 1.2% / 0.95 / 35 | 2.1% / 0.72 / 46 | 0.4% / 0.33 / 38 | 3.8% / 1.37 / 51 |
| 185 | 0.8% / 0.61 / 33 | -1.0% / -0.59 / 42 | 4.3% / 2.00 / 42 | 1.7% / 1.25 / 32 | 2.0% / 0.95 / 35 |
| 186 | 1.2% / 0.64 / 51 | -2.4% / -1.89 / 56 | 5.5% / 2.71 / 43 | -1.0% / -0.63 / 61 | 6.4% / 2.09 / 59 |
| 187 | 0.1% / 0.07 / 34 | -1.0% / -0.70 / 33 | 4.6% / 2.44 / 33 | 0.5% / 0.33 / 39 | 3.1% / 1.25 / 37 |
| 188 | 0.6% / 0.36 / 48 | 0.1% / 0.08 / 53 | 5.8% / 2.53 / 53 | -0.0% / -0.01 / 57 | 1.6% / 0.59 / 61 |
| 189 | 1.3% / 0.67 / 41 | -1.9% / -1.48 / 47 | 2.9% / 1.66 / 33 | 1.4% / 0.86 / 44 | 3.9% / 1.45 / 39 |
| 190 | -0.9% / -0.56 / 43 | -3.0% / -2.33 / 46 | 6.2% / 2.86 / 43 | 0.8% / 0.42 / 47 | 4.6% / 1.63 / 47 |
| 191 | -1.3% / -0.61 / 39 | -1.8% / -1.43 / 38 | 5.4% / 2.08 / 38 | 0.3% / 0.16 / 40 | 6.3% / 1.96 / 49 |
| 192 | 0.6% / 0.40 / 38 | -1.1% / -0.84 / 34 | 3.0% / 1.37 / 34 | 0.9% / 0.54 / 47 | 4.1% / 1.65 / 44 |
| 193 | 0.9% / 0.53 / 44 | -1.1% / -1.05 / 41 | 4.5% / 2.21 / 47 | 0.9% / 0.65 / 41 | 1.7% / 0.79 / 36 |
| 194 | 0.9% / 0.65 / 33 | -1.1% / -0.62 / 41 | 4.1% / 1.87 / 42 | 1.7% / 1.25 / 32 | 2.1% / 0.98 / 35 |
| 195 | 0.3% / 0.17 / 33 | -0.5% / -0.25 / 41 | 2.3% / 1.20 / 35 | 1.4% / 0.76 / 41 | 4.1% / 2.09 / 36 |
| 196 | -0.7% / -0.49 / 28 | -1.4% / -1.37 / 35 | 4.8% / 2.25 / 44 | 0.5% / 0.48 / 27 | 3.2% / 1.46 / 30 |
| 197 | 0.4% / 0.26 / 35 | -0.3% / -0.26 / 35 | 3.7% / 2.05 / 37 | 0.1% / 0.07 / 37 | 4.2% / 1.64 / 39 |
| 198 | 0.3% / 0.17 / 33 | -2.2% / -1.45 / 40 | 6.2% / 2.83 / 32 | 1.0% / 0.71 / 37 | 2.1% / 0.84 / 33 |
| 199 | 1.1% / 0.56 / 36 | -1.3% / -0.82 / 31 | 2.3% / 0.88 / 37 | 0.8% / 0.46 / 36 | 6.3% / 1.85 / 42 |
| 200 | 0.7% / 0.40 / 44 | -1.1% / -1.03 / 41 | 4.6% / 2.27 / 47 | 0.8% / 0.58 / 41 | 1.6% / 0.86 / 36 |
| 201 | 0.1% / 0.08 / 35 | -0.6% / -0.32 / 43 | 3.4% / 1.82 / 37 | 0.7% / 0.39 / 41 | 3.4% / 1.56 / 38 |
| 202 | 2.1% / 1.24 / 32 | -2.6% / -1.82 / 39 | 4.2% / 2.06 / 32 | -0.7% / -0.35 / 40 | 5.4% / 1.64 / 39 |
| 203 | -0.9% / -0.55 / 48 | -2.6% / -2.18 / 50 | 6.4% / 2.93 / 44 | 0.4% / 0.23 / 51 | 4.6% / 1.67 / 48 |
| 204 | -1.6% / -1.00 / 29 | -0.2% / -0.14 / 36 | 6.6% / 2.49 / 45 | 1.0% / 0.64 / 29 | 2.7% / 1.05 / 32 |
| 205 | 2.0% / 1.13 / 33 | -1.0% / -0.70 / 30 | 2.8% / 1.61 / 33 | -0.8% / -0.50 / 42 | 4.6% / 1.74 / 35 |
| 206 | 0.1% / 0.04 / 36 | -0.6% / -0.37 / 37 | 4.7% / 1.80 / 35 | 3.1% / 1.47 / 44 | 7.0% / 1.93 / 39 |
| 207 | -1.7% / -0.84 / 54 | 0.7% / 0.50 / 54 | 5.8% / 2.47 / 44 | -0.3% / -0.22 / 55 | 3.8% / 1.33 / 57 |
| 208 | 1.6% / 1.10 / 43 | -1.2% / -1.02 / 34 | 4.8% / 2.65 / 44 | 0.3% / 0.17 / 44 | 2.1% / 1.03 / 42 |
| 209 | 0.9% / 0.55 / 38 | -1.1% / -0.84 / 34 | 2.9% / 1.33 / 34 | 0.5% / 0.34 / 47 | 4.1% / 1.63 / 43 |
| 210 | 0.2% / 0.10 / 40 | -0.2% / -0.17 / 37 | 3.2% / 1.78 / 39 | 0.2% / 0.17 / 39 | 3.9% / 1.50 / 40 |
| 211 | 1.4% / 0.91 / 40 | -1.2% / -1.36 / 42 | 3.7% / 2.04 / 34 | -0.6% / -0.35 / 45 | 3.4% / 1.73 / 40 |
| 212 | 0.9% / 0.56 / 39 | -1.3% / -1.38 / 41 | 3.6% / 2.01 / 34 | -0.2% / -0.11 / 41 | 3.4% / 1.64 / 39 |
| 213 | 1.6% / 1.13 / 43 | -1.2% / -1.02 / 34 | 4.2% / 2.50 / 42 | -0.2% / -0.12 / 45 | 2.1% / 1.00 / 42 |
| 214 | 1.0% / 0.61 / 38 | -1.5% / -1.06 / 33 | 5.0% / 2.58 / 40 | 0.9% / 0.49 / 35 | 1.7% / 0.73 / 39 |
| 215 | 1.3% / 0.72 / 40 | -1.5% / -1.48 / 40 | 6.5% / 3.12 / 46 | -0.7% / -0.44 / 42 | 2.4% / 0.96 / 36 |
| 216 | -1.4% / -0.66 / 35 | -0.7% / -0.48 / 44 | 5.3% / 2.23 / 39 | 0.0% / 0.03 / 40 | 5.0% / 1.59 / 47 |
| 217 | 2.8% / 1.53 / 36 | -1.7% / -1.06 / 37 | 4.9% / 1.98 / 37 | -0.1% / -0.02 / 45 | 4.8% / 1.50 / 43 |
| 218 | 0.3% / 0.16 / 40 | 0.6% / 0.38 / 47 | 3.8% / 1.49 / 36 | -0.9% / -0.37 / 43 | 6.2% / 1.79 / 45 |
| 219 | 0.1% / 0.05 / 31 | 0.9% / 0.63 / 43 | 4.7% / 2.25 / 41 | 1.6% / 1.39 / 29 | 0.3% / 0.11 / 39 |
| 220 | 0.3% / 0.26 / 43 | -1.3% / -0.96 / 41 | 4.4% / 2.59 / 46 | 0.7% / 0.42 / 46 | 3.1% / 1.46 / 43 |
| 221 | -1.2% / -0.57 / 45 | -0.5% / -0.39 / 38 | 3.1% / 1.47 / 40 | 0.6% / 0.34 / 51 | 5.7% / 2.15 / 39 |
| 222 | 1.6% / 1.06 / 41 | 0.1% / 0.09 / 42 | 2.9% / 1.40 / 39 | -0.5% / -0.33 / 43 | 3.2% / 1.27 / 39 |
| 223 | 0.6% / 0.44 / 38 | -0.3% / -0.24 / 39 | 4.7% / 2.13 / 44 | -1.7% / -1.01 / 48 | 3.9% / 1.59 / 39 |
| 224 | 1.5% / 1.00 / 41 | -0.9% / -0.77 / 33 | 5.0% / 2.79 / 41 | -0.1% / -0.06 / 41 | 1.2% / 0.55 / 41 |
| 225 | 1.1% / 0.70 / 44 | -0.5% / -0.52 / 33 | 4.5% / 1.67 / 49 | -0.7% / -0.49 / 48 | 3.0% / 1.21 / 41 |
| 226 | -0.3% / -0.25 / 37 | 1.3% / 1.03 / 37 | -0.7% / -0.62 / 34 | 0.1% / 0.12 / 49 | 6.0% / 2.25 / 48 |
| 227 | 0.3% / 0.22 / 39 | -1.0% / -1.00 / 44 | 2.6% / 1.46 / 40 | 0.1% / 0.07 / 44 | 5.1% / 2.27 / 43 |
| 228 | -1.0% / -0.73 / 33 | 0.4% / 0.30 / 42 | 3.5% / 1.82 / 43 | 1.8% / 1.57 / 29 | 1.4% / 0.81 / 32 |
| 229 | 0.4% / 0.30 / 33 | -0.8% / -0.61 / 40 | 3.6% / 1.87 / 36 | 0.9% / 0.50 / 39 | 3.0% / 1.37 / 38 |
| 230 | 0.4% / 0.29 / 40 | -0.3% / -0.26 / 39 | 4.4% / 1.93 / 48 | -1.3% / -0.79 / 50 | 4.0% / 1.56 / 40 |
| 231 | 0.3% / 0.26 / 43 | -1.3% / -0.96 / 41 | 4.2% / 2.45 / 47 | 0.7% / 0.43 / 46 | 3.1% / 1.47 / 43 |
| 232 | 1.7% / 1.19 / 41 | 0.6% / 0.62 / 44 | 1.7% / 0.89 / 42 | -2.2% / -1.36 / 49 | 5.4% / 2.03 / 37 |
| 233 | 1.3% / 0.75 / 39 | -1.8% / -1.83 / 37 | 6.3% / 3.00 / 45 | -1.0% / -0.62 / 39 | 2.6% / 1.17 / 34 |
| 234 | 2.2% / 0.99 / 31 | -0.6% / -0.37 / 32 | 5.3% / 2.06 / 34 | 0.2% / 0.09 / 31 | 3.6% / 1.02 / 35 |
| 235 | 1.7% / 1.19 / 41 | 0.7% / 0.70 / 43 | 1.6% / 0.86 / 41 | -2.3% / -1.34 / 48 | 5.6% / 2.13 / 35 |
| 236 | 0.5% / 0.40 / 31 | 0.2% / 0.14 / 37 | 4.1% / 2.30 / 35 | 2.2% / 1.90 / 27 | -1.0% / -0.49 / 29 |
| 237 | 2.3% / 1.11 / 35 | -0.2% / -0.10 / 31 | 2.6% / 1.32 / 33 | 0.7% / 0.41 / 34 | 3.3% / 1.13 / 38 |
| 238 | 1.8% / 0.84 / 31 | -0.0% / -0.02 / 33 | 5.6% / 2.18 / 35 | 0.2% / 0.11 / 31 | 2.4% / 0.64 / 35 |
| 239 | 1.0% / 0.67 / 41 | -0.1% / -0.11 / 44 | 3.7% / 1.94 / 43 | -0.1% / -0.06 / 53 | 2.8% / 1.15 / 49 |
| 240 | 1.0% / 0.49 / 35 | -1.9% / -1.18 / 36 | 5.1% / 2.07 / 33 | 0.2% / 0.09 / 44 | 5.3% / 1.71 / 41 |
| 241 | 1.9% / 0.99 / 35 | -0.2% / -0.10 / 32 | 2.6% / 1.29 / 33 | 0.7% / 0.41 / 34 | 3.4% / 1.28 / 38 |
| 242 | -0.3% / -0.14 / 33 | -1.0% / -0.69 / 36 | 3.7% / 1.76 / 31 | 1.7% / 0.87 / 38 | 3.9% / 1.32 / 40 |
| 243 | -1.6% / -0.69 / 36 | 1.1% / 0.68 / 33 | 3.0% / 1.13 / 34 | 2.1% / 0.87 / 50 | 5.7% / 1.48 / 50 |
| 244 | 3.2% / 1.64 / 35 | -1.4% / -0.90 / 36 | 4.5% / 1.78 / 35 | -0.5% / -0.19 / 40 | 4.4% / 1.35 / 41 |
| 245 | 0.7% / 0.49 / 53 | 1.5% / 1.18 / 47 | 0.4% / 0.28 / 47 | -0.2% / -0.15 / 58 | 5.3% / 1.85 / 65 |
| 246 | -2.2% / -1.21 / 43 | -0.7% / -0.56 / 44 | 3.5% / 1.72 / 42 | 0.8% / 0.51 / 56 | 6.4% / 2.16 / 47 |
| 247 | 0.8% / 0.57 / 37 | -1.1% / -0.86 / 39 | 3.3% / 1.91 / 38 | 0.6% / 0.46 / 46 | 3.0% / 1.32 / 45 |
| 248 | 1.0% / 0.52 / 34 | -2.8% / -1.74 / 37 | 4.6% / 1.99 / 33 | -0.6% / -0.27 / 42 | 6.4% / 2.07 / 39 |
| 249 | 0.3% / 0.24 / 31 | 1.0% / 0.82 / 44 | 4.0% / 1.82 / 42 | 0.9% / 0.72 / 29 | 0.6% / 0.25 / 39 |
| 250 | -1.7% / -1.11 / 43 | 0.2% / 0.12 / 43 | 2.1% / 1.15 / 39 | 1.7% / 1.00 / 55 | 4.8% / 1.88 / 55 |
| 251 | -0.5% / -0.41 / 38 | -1.0% / -1.07 / 43 | 2.4% / 1.37 / 40 | 0.1% / 0.05 / 44 | 5.1% / 2.25 / 43 |
| 252 | 0.3% / 0.23 / 32 | 0.6% / 0.45 / 39 | 3.8% / 2.12 / 36 | 2.2% / 1.90 / 27 | -0.9% / -0.47 / 31 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_5885` | 29 | 0.82 | 0.82/0.90 | 0.57/0.74 |
| 1 | `cfg_0025` | 30 | 0.85 | 0.83/0.92 | 0.53/0.74 |
| 2 | `cfg_34ef` | 7 | 0.81 | 0.85/0.92 | 0.72/0.79 |
| 3 | `cfg_00e1` | 2 | 0.90 | 0.92/0.92 | 0.87/0.87 |
| 4 | `cfg_be54` | 15 | 0.82 | 0.84/0.88 | 0.75/0.80 |
| 5 | `cfg_4883` | 5 | 0.87 | 0.93/0.97 | 0.89/0.98 |
| 6 | `cfg_4a7b` | 16 | 0.92 | 0.94/0.98 | 0.80/0.93 |
| 7 | `cfg_62dc` | 14 | 0.89 | 0.89/0.97 | 0.72/0.91 |
| 8 | `cfg_bd4d` | 13 | 0.91 | 0.93/0.95 | 0.83/0.91 |
| 9 | `cfg_ea40` | 9 | 0.92 | 0.94/0.96 | 0.86/0.89 |
| 10 | `cfg_f2ab` | 12 | 0.86 | 0.83/0.87 | 0.71/0.76 |
| 11 | `cfg_6cbf` | 30 | 0.81 | 0.79/0.88 | 0.57/0.76 |
| 12 | `cfg_eb6d` | 10 | 0.93 | 0.94/0.96 | 0.88/0.97 |
| 13 | `cfg_02d1` | 18 | 0.80 | 0.81/0.90 | 0.71/0.83 |
| 14 | `cfg_85f1` | 3 | 0.85 | 0.86/0.87 | 0.66/0.72 |
| 15 | `cfg_dd2f` | 28 | 0.81 | 0.81/0.94 | 0.59/0.81 |
| 16 | `cfg_b809` | 4 | 0.85 | 0.90/0.92 | 0.79/0.82 |
| 17 | `cfg_a7c1` | 6 | 0.81 | 0.85/0.88 | 0.71/0.79 |
| 18 | `cfg_4755` | 16 | 0.93 | 0.92/0.99 | 0.85/0.95 |
| 19 | `cfg_6a3d` | 7 | 0.82 | 0.79/0.88 | 0.63/0.76 |
| 20 | `cfg_bd46` | 6 | 0.85 | 0.87/0.89 | 0.78/0.83 |
| 21 | `cfg_ff97` | 8 | 0.85 | 0.80/0.86 | 0.63/0.69 |
| 22 | `cfg_63c2` | 13 | 0.90 | 0.88/0.92 | 0.65/0.78 |
| 23 | `cfg_a8ca` | 16 | 0.83 | 0.86/0.93 | 0.73/0.88 |
| 24 | `cfg_eb4c` | 4 | 0.91 | 0.95/0.97 | 0.93/0.98 |
| 25 | `cfg_08f9` | 4 | 0.92 | 0.91/0.92 | 0.74/0.78 |
| 26 | `cfg_61e8` | 15 | 0.87 | 0.87/0.94 | 0.71/0.89 |
| 27 | `cfg_5cd1` | 29 | 0.88 | 0.85/0.92 | 0.61/0.80 |
| 28 | `cfg_43f7` | 5 | 0.86 | 0.85/0.86 | 0.73/0.76 |
| 29 | `cfg_2d34` | 9 | 0.85 | 0.88/0.95 | 0.80/0.90 |
| 30 | `cfg_0a72` | 7 | 0.97 | 0.96/0.98 | 0.92/0.94 |
| 31 | `cfg_0ad1` | 3 | 0.94 | 0.95/0.96 | 0.88/0.89 |
| 32 | `cfg_e482` | 5 | 0.82 | 0.73/0.84 | 0.69/0.81 |
| 33 | `cfg_df08` | 12 | 0.80 | 0.87/0.95 | 0.79/0.84 |
| 34 | `cfg_bc77` | 11 | 0.87 | 0.88/0.94 | 0.75/0.94 |
| 35 | `cfg_bf3a` | 6 | 0.81 | 0.90/0.92 | 0.73/0.85 |
| 36 | `cfg_544b` | 9 | 0.82 | 0.81/0.91 | 0.78/0.87 |
| 37 | `cfg_49fa` | 8 | 0.81 | 0.86/0.93 | 0.61/0.88 |
| 38 | `cfg_e062` | 13 | 0.85 | 0.80/0.93 | 0.66/0.88 |
| 39 | `cfg_f8f6` | 6 | 0.97 | 0.98/0.98 | 0.96/0.98 |
| 40 | `cfg_d81a` | 6 | 0.82 | 0.83/0.90 | 0.80/0.88 |
| 41 | `cfg_a68c` | 23 | 0.86 | 0.86/0.93 | 0.70/0.83 |
| 42 | `cfg_6d6b` | 7 | 0.90 | 0.94/0.97 | 0.92/0.95 |
| 43 | `cfg_4ade` | 20 | 0.89 | 0.88/0.91 | 0.52/0.58 |
| 44 | `cfg_81a3` | 6 | 0.93 | 0.95/0.97 | 0.94/0.96 |
| 45 | `cfg_123b` | 12 | 0.90 | 0.89/0.95 | 0.83/0.91 |
| 46 | `cfg_129d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 47 | `cfg_12b7` | 9 | 0.87 | 0.84/0.90 | 0.77/0.82 |
| 48 | `cfg_ad3b` | 10 | 0.88 | 0.87/0.91 | 0.59/0.78 |
| 49 | `cfg_12f2` | 8 | 0.95 | 0.95/0.96 | 0.88/0.91 |
| 50 | `cfg_eb7d` | 18 | 0.84 | 0.88/0.91 | 0.69/0.79 |
| 51 | `cfg_6dac` | 16 | 0.85 | 0.88/0.96 | 0.77/0.91 |
| 52 | `cfg_c673` | 13 | 0.91 | 0.93/0.94 | 0.81/0.93 |
| 53 | `cfg_3c04` | 5 | 0.89 | 0.96/0.98 | 0.94/0.96 |
| 54 | `cfg_9937` | 10 | 0.82 | 0.87/0.93 | 0.75/0.84 |
| 55 | `cfg_46c7` | 16 | 0.88 | 0.86/0.90 | 0.72/0.77 |
| 56 | `cfg_96ad` | 9 | 0.86 | 0.83/0.89 | 0.74/0.84 |
| 57 | `cfg_1b74` | 5 | 0.80 | 0.79/0.87 | 0.57/0.73 |
| 58 | `cfg_f26e` | 12 | 0.86 | 0.88/0.90 | 0.72/0.79 |
| 59 | `cfg_9b1a` | 2 | 0.99 | 0.96/0.96 | 0.96/0.96 |
| 60 | `cfg_6cb7` | 3 | 0.86 | 0.87/0.91 | 0.76/0.82 |
| 61 | `cfg_9c9b` | 4 | 0.92 | 0.92/0.93 | 0.82/0.87 |
| 62 | `cfg_995d` | 16 | 0.81 | 0.89/0.94 | 0.75/0.91 |
| 63 | `cfg_8c05` | 5 | 0.83 | 0.84/0.93 | 0.71/0.81 |
| 64 | `cfg_7643` | 4 | 0.84 | 0.85/0.89 | 0.69/0.77 |
| 65 | `cfg_881b` | 4 | 0.92 | 0.92/0.95 | 0.85/0.90 |
| 66 | `cfg_cf11` | 8 | 0.97 | 0.94/0.99 | 0.93/0.98 |
| 67 | `cfg_8716` | 9 | 0.91 | 0.92/0.96 | 0.91/0.93 |
| 68 | `cfg_b53b` | 6 | 0.89 | 0.93/0.94 | 0.76/0.81 |
| 69 | `cfg_271d` | 4 | 0.96 | 0.95/0.97 | 0.86/0.91 |
| 70 | `cfg_2762` | 1 | n/a | n/a/n/a | n/a/n/a |
| 71 | `cfg_7e2e` | 5 | 0.90 | 0.95/0.95 | 0.88/0.94 |
| 72 | `cfg_7fac` | 16 | 0.90 | 0.93/0.97 | 0.88/0.94 |
| 73 | `cfg_2a9b` | 4 | 0.91 | 0.92/0.96 | 0.87/0.91 |
| 74 | `cfg_6e86` | 3 | 0.83 | 0.80/0.84 | 0.72/0.79 |
| 75 | `cfg_2b30` | 1 | n/a | n/a/n/a | n/a/n/a |
| 76 | `cfg_9d98` | 2 | 0.99 | 0.97/0.97 | 0.94/0.94 |
| 77 | `cfg_a2c6` | 3 | 0.84 | 0.88/0.93 | 0.88/0.93 |
| 78 | `cfg_da37` | 7 | 0.81 | 0.87/0.93 | 0.78/0.89 |
| 79 | `cfg_2eaa` | 8 | 0.87 | 0.92/0.95 | 0.82/0.90 |
| 80 | `cfg_da60` | 12 | 0.83 | 0.89/0.93 | 0.72/0.87 |
| 81 | `cfg_e446` | 5 | 0.90 | 0.89/0.95 | 0.82/0.91 |
| 82 | `cfg_bde5` | 5 | 0.88 | 0.93/0.94 | 0.80/0.89 |
| 83 | `cfg_ad5c` | 2 | 0.98 | 0.97/0.97 | 0.97/0.97 |
| 84 | `cfg_34f9` | 2 | 0.96 | 0.98/0.98 | 0.98/0.98 |
| 85 | `cfg_d2d6` | 3 | 0.93 | 0.92/0.94 | 0.96/0.97 |
| 86 | `cfg_d1c0` | 6 | 0.89 | 0.85/0.91 | 0.72/0.80 |
| 87 | `cfg_a0b4` | 5 | 0.87 | 0.91/0.96 | 0.87/0.92 |
| 88 | `cfg_5632` | 10 | 0.89 | 0.94/0.97 | 0.88/0.95 |
| 89 | `cfg_90ee` | 5 | 0.96 | 0.96/0.97 | 0.92/0.94 |
| 90 | `cfg_80c2` | 4 | 0.97 | 0.98/1.00 | 0.99/1.00 |
| 91 | `cfg_d442` | 5 | 0.80 | 0.79/0.97 | 0.53/0.95 |
| 92 | `cfg_9c56` | 8 | 0.91 | 0.92/0.97 | 0.75/0.95 |
| 93 | `cfg_4337` | 2 | 0.89 | 0.86/0.86 | 0.74/0.74 |
| 94 | `cfg_7a6e` | 10 | 0.82 | 0.88/0.95 | 0.86/0.94 |
| 95 | `cfg_46ab` | 1 | n/a | n/a/n/a | n/a/n/a |
| 96 | `cfg_d877` | 4 | 0.89 | 0.96/0.96 | 0.89/0.92 |
| 97 | `cfg_7c2c` | 2 | 1.00 | 0.98/0.98 | 0.98/0.98 |
| 98 | `cfg_c634` | 8 | 0.81 | 0.78/0.82 | 0.60/0.62 |
| 99 | `cfg_4d15` | 4 | 0.88 | 0.87/0.90 | 0.73/0.79 |
| 100 | `cfg_5499` | 1 | n/a | n/a/n/a | n/a/n/a |
| 101 | `cfg_5579` | 2 | 0.95 | 0.97/0.97 | 0.93/0.93 |
| 102 | `cfg_5732` | 1 | n/a | n/a/n/a | n/a/n/a |
| 103 | `cfg_5bed` | 1 | n/a | n/a/n/a | n/a/n/a |
| 104 | `cfg_5dcf` | 1 | n/a | n/a/n/a | n/a/n/a |
| 105 | `cfg_5fcb` | 2 | 1.00 | 0.97/0.97 | 0.98/0.98 |
| 106 | `cfg_6ea4` | 6 | 0.89 | 0.91/0.93 | 0.77/0.88 |
| 107 | `cfg_7e8e` | 2 | 0.84 | 0.79/0.79 | 0.55/0.55 |
| 108 | `cfg_7a94` | 4 | 0.90 | 0.90/0.94 | 0.84/0.86 |
| 109 | `cfg_6a92` | 4 | 0.90 | 0.89/0.98 | 0.87/0.94 |
| 110 | `cfg_67a4` | 4 | 0.93 | 0.94/0.97 | 0.90/0.92 |
| 111 | `cfg_7162` | 2 | 0.99 | 0.98/0.98 | 0.97/0.97 |
| 112 | `cfg_71a8` | 1 | n/a | n/a/n/a | n/a/n/a |
| 113 | `cfg_724e` | 1 | n/a | n/a/n/a | n/a/n/a |
| 114 | `cfg_e57f` | 2 | 0.96 | 0.97/0.97 | 0.90/0.90 |
| 115 | `cfg_751d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 116 | `cfg_a189` | 2 | 0.81 | 0.81/0.81 | 0.59/0.59 |
| 117 | `cfg_7882` | 2 | 0.89 | 0.92/0.92 | 0.85/0.85 |
| 118 | `cfg_7b17` | 5 | 0.90 | 0.92/0.95 | 0.88/0.90 |
| 119 | `cfg_7ebf` | 4 | 0.85 | 0.87/0.90 | 0.71/0.74 |
| 120 | `cfg_e096` | 3 | 0.94 | 0.96/0.97 | 0.93/0.94 |
| 121 | `cfg_da22` | 2 | 0.96 | 0.96/0.96 | 0.86/0.86 |
| 122 | `cfg_8b2c` | 2 | 0.98 | 0.98/0.98 | 0.96/0.96 |
| 123 | `cfg_dd01` | 5 | 0.87 | 0.90/0.93 | 0.80/0.86 |
| 124 | `cfg_9e05` | 5 | 0.84 | 0.83/0.86 | 0.70/0.74 |
| 125 | `cfg_925d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 126 | `cfg_9818` | 1 | n/a | n/a/n/a | n/a/n/a |
| 127 | `cfg_bceb` | 5 | 0.82 | 0.79/0.85 | 0.68/0.72 |
| 128 | `cfg_a675` | 1 | n/a | n/a/n/a | n/a/n/a |
| 129 | `cfg_b1c3` | 3 | 0.92 | 0.89/0.92 | 0.79/0.85 |
| 130 | `cfg_b70a` | 3 | 0.97 | 0.98/0.99 | 0.96/0.97 |
| 131 | `cfg_b757` | 1 | n/a | n/a/n/a | n/a/n/a |
| 132 | `cfg_c536` | 1 | n/a | n/a/n/a | n/a/n/a |
| 133 | `cfg_c57c` | 1 | n/a | n/a/n/a | n/a/n/a |
| 134 | `cfg_ef0b` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 8.555e-04 over 24000 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 810.0, participation ratio 7.6, 95%-variance components 189 (rank bound T = 1259); raw grid 24000; raw + known prior 755976
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
6J results are unchanged rules on the development period: supporting evidence, not an independent replication.

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
