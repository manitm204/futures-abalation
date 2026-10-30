# Screening funnel -- mr_rty_v7_15m (development stages only)

- Code: `5342a94cdc84` (dirty working tree: True, diff sha256 `4935ac06549a`)
- Config: `configs/funnel/mr_funnel_rty_v7_15m.yaml` sha256 `12a257956634bb44`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ES': '2026-10-16', 'RTY': '2026-10-16'}
- Frozen manifest sha256: `deccb899980a38f7` (154 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_rty_v5 gated 27 RTY candidates on 2023-2024 (5 passed) and mr_rty_v6 gated 108 (19 passed); this v7 grid was written after reading both, so RTY 2023-2024 is largely in-sample for v7. The stage-4 test and 40-trade rule were also shaped by ES 2023-2024.
- Holdout 2025+ previously inspected: **False** -- No RTY strategy metrics have been computed on 2025+. The futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no selection). Correlated indices were scored on their 2025+ holdouts on 2026-10-24: ES (mr_es_v6_1h #8, #15), NQ (mr_nq_v7_15m #1 + mr_nq_v7_1h #119) and YM (mr_ym_v7_15m #9 + mr_ym_v7_1h #51). The RTY holdout is the only untouched test for this run.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 13608 | 13608 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 13608 | 13608 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 13608 | 9711 | 3897 | 0 |  | 12049 | 71.36 | 71.36 |  |
| 3 performance & risk | hard_gate | 9711 | 498 | 9213 | 0 |  | 0 | 3.66 | 5.13 |  |
| 4 parameter stability | hard_gate | 498 | 473 | 25 | 0 |  | 0 | 3.48 | 94.98 |  |
| 5 time stability | hard_gate | 473 | 460 | 13 | 0 |  | 462 | 3.38 | 97.25 |  |
| 6 deduplication | dedup | 460 | 154 |  |  | 306 |  | 1.13 | 33.48 | best 2 per cluster |
| 7 execution stress | hard_gate | 154 | 154 | 0 | 0 |  | 10 | 1.13 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 154 |  |  |  |  |  |  |  | diagnostic only: unverified: 154 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 3897 |
| s2:hard_reject:years_with_>=10_trades | 2199 |
| s3:hard_reject:max_drawdown | 417 |
| s3:hard_reject:net_return | 5307 |
| s3:hard_reject:sharpe | 9213 |
| s4:hard_reject:local_frac_profitable | 4 |
| s4:hard_reject:local_median_sharpe | 25 |
| s5:hard_reject:profitable_years | 13 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_5371` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=55, entry_z=-3.0, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 0/128/35 | 163 | 19.1% | 3.6% | 1.24 | -2.9% | 318 | 1.67 | 1.8% | 73.9 | 8/8 | 0.75 | 0.77 | 0.46 | 4 | 10.0% | 0.48 | 0.48 | 17.6% | 16.2% | 9.1% | 16.5%/13.5% | 7.5 (interpolated) | pass | 0.281 (unverified) | -0.31 |
| 2 | `cfg_0981` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=55, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 0/128/35 | 163 | 19.1% | 3.6% | 1.24 | -2.9% | 318 | 1.67 | 1.8% | 73.9 | 9/9 | 0.78 | 0.85 | 0.39 | 4 | 10.0% | 0.48 | 0.48 | 17.6% | 16.2% | 9.1% | 16.7%/13.4% | 7.5 (interpolated) | pass | 0.281 (unverified) | -0.31 |
| 3 | `cfg_140b` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=65, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 4/84/27 | 115 | 12.1% | 2.3% | 0.99 | -2.4% | 307 | 1.57 | 1.2% | 51.9 | 7/7 | 1.00 | 0.86 | 0.13 | 3 | 5.7% | 0.53 | 0.68 | 10.9% | 10.0% | 3.6% | 10.3%/8.3% | 7.1 (interpolated) | pass | 0.131 (unverified) | -0.78 |
| 4 | `cfg_4cf5` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=65, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 0/88/27 | 115 | 12.0% | 2.3% | 0.99 | -2.4% | 307 | 1.57 | 1.2% | 51.9 | 8/8 | 1.00 | 0.86 | 0.13 | 3 | 5.7% | 0.52 | 0.68 | 10.8% | 9.9% | 3.0% | 10.7%/8.8% | 7.0 (interpolated) | pass | 0.129 (unverified) | -0.77 |
| 5 | `cfg_36f2` | timeframe=15min, mean_type=sma, mean_lookback=65, std_lookback=55, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 30/113/0 | 143 | 27.1% | 4.9% | 1.09 | -6.7% | 284 | 1.69 | 3.8% | 65.2 | 8/8 | 1.00 | 0.69 | 0.40 | 4 | 14.2% | 0.49 | 0.50 | 25.1% | 23.8% | 7.5% | 24.0%/19.4% | 11.1 (interpolated) | pass | 0.185 (unverified) | -0.05 |
| 6 | `cfg_4830` | timeframe=15min, mean_type=ema, mean_lookback=105, std_lookback=85, entry_z=-3.0, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 0/108/0 | 108 | 16.2% | 3.0% | 1.00 | -5.1% | 390 | 1.69 | 1.3% | 48.8 | 8/8 | 0.88 | 0.89 | 0.12 | 3 | 7.8% | 0.54 | 0.61 | 15.2% | 14.4% | 6.6% | 15.1%/12.3% | 9.2 (interpolated) | pass | 0.166 (unverified) | 0.41 |
| 7 | `cfg_b481` | timeframe=15min, mean_type=ema, mean_lookback=105, std_lookback=85, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 0/108/0 | 108 | 16.2% | 3.0% | 1.00 | -5.1% | 390 | 1.69 | 1.3% | 48.8 | 9/9 | 0.89 | 0.94 | 0.06 | 3 | 7.8% | 0.54 | 0.61 | 15.2% | 14.4% | 6.6% | 15.3%/12.3% | 9.2 (interpolated) | pass | 0.166 (unverified) | 0.42 |
| 8 | `cfg_7475` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=55, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 13/117/0 | 130 | 19.2% | 3.6% | 0.94 | -5.0% | 332 | 1.70 | 2.3% | 59.0 | 9/9 | 1.00 | 0.92 | 0.02 | 4 | 9.7% | 0.47 | 0.72 | 18.1% | 16.8% | 8.4% | 17.4%/13.1% | 9.2 (interpolated) | pass | 0.073 (unverified) | -0.35 |
| 9 | `cfg_8782` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=85, entry_z=-2.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 1/147/0 | 148 | 15.9% | 3.0% | 0.96 | -3.8% | 325 | 1.62 | 1.8% | 66.5 | 9/9 | 1.00 | 0.96 | 0.00 | 3 | 6.6% | 0.55 | 0.64 | 14.7% | 13.4% | 7.0% | 15.0%/12.1% | 7.1 (interpolated) | pass | 0.113 (unverified) | 0.08 |
| 10 | `cfg_88d9` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=85, entry_z=-2.5, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 0/148/0 | 148 | 15.9% | 3.0% | 0.96 | -3.8% | 325 | 1.62 | 1.8% | 66.5 | 8/8 | 1.00 | 0.98 | -0.01 | 3 | 6.6% | 0.55 | 0.64 | 14.7% | 13.4% | 6.9% | 14.7%/11.2% | 7.1 (interpolated) | pass | 0.113 (unverified) | 0.08 |
| 11 | `cfg_09c9` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=105, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 3/193/0 | 196 | 24.7% | 4.5% | 1.03 | -5.3% | 301 | 1.52 | 3.6% | 88.4 | 8/8 | 1.00 | 0.80 | 0.24 | 4 | 14.9% | 0.41 | 0.59 | 22.5% | 20.7% | 13.2% | 22.6%/17.0% | 7.6 (interpolated) | pass | 0.159 (unverified) | 0.11 |
| 12 | `cfg_6cb8` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=65, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 2/108/32 | 142 | 13.4% | 2.5% | 0.96 | -5.6% | 332 | 1.46 | 1.5% | 64.3 | 8/8 | 1.00 | 0.65 | 0.30 | 3 | 4.6% | 0.68 | 0.60 | 12.1% | 10.7% | 5.0% | 11.9%/8.8% | 6.3 (interpolated) | pass | 0.122 (unverified) | -0.32 |
| 13 | `cfg_d880` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=85, entry_z=-2.0, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 2/242/73 | 317 | 22.9% | 4.2% | 1.14 | -3.9% | 315 | 1.37 | 3.4% | 142.2 | 8/8 | 1.00 | 0.82 | 0.32 | 4 | 9.1% | 0.55 | 0.51 | 19.8% | 16.9% | 8.4% | 19.1%/15.2% | 4.9 (interpolated) | pass | 0.229 (unverified) | -0.58 |
| 14 | `cfg_7aeb` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=105, entry_z=-2.0, exit_z=1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 0/196/0 | 196 | 24.1% | 4.4% | 1.02 | -5.4% | 289 | 1.51 | 3.6% | 88.3 | 7/7 | 1.00 | 0.76 | 0.26 | 4 | 13.6% | 0.41 | 0.59 | 21.9% | 20.6% | 11.6% | 23.0%/17.2% | 7.5 (interpolated) | pass | 0.149 (unverified) | 0.10 |
| 15 | `cfg_142a` | timeframe=15min, mean_type=ema, mean_lookback=55, std_lookback=85, entry_z=-2.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 1/131/42 | 174 | 16.6% | 3.1% | 1.06 | -3.1% | 332 | 1.50 | 1.9% | 78.1 | 10/10 | 1.00 | 0.80 | 0.26 | 3 | 8.7% | 0.48 | 0.53 | 15.0% | 13.5% | 3.0% | 14.8%/10.3% | 6.4 (interpolated) | pass | 0.186 (unverified) | 0.07 |
| 16 | `cfg_3bcb` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=65, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 0/110/32 | 142 | 13.3% | 2.5% | 0.95 | -5.6% | 332 | 1.46 | 1.5% | 64.3 | 9/9 | 1.00 | 0.66 | 0.30 | 3 | 4.6% | 0.67 | 0.61 | 11.9% | 10.6% | 4.2% | 11.9%/8.0% | 6.3 (interpolated) | pass | 0.120 (unverified) | -0.31 |
| 17 | `cfg_4a27` | timeframe=15min, mean_type=sma, mean_lookback=85, std_lookback=85, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 11/95/0 | 106 | 21.3% | 3.9% | 1.10 | -3.3% | 186 | 1.89 | 2.8% | 47.9 | 8/8 | 1.00 | 0.92 | 0.18 | 5 | 9.7% | 0.54 | 0.49 | 20.3% | 19.3% | 7.5% | 19.6%/15.8% | 11.9 (interpolated) | pass | 0.209 (unverified) | 0.10 |
| 18 | `cfg_db93` | timeframe=15min, mean_type=ema, mean_lookback=55, std_lookback=85, entry_z=-2.5, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 0/132/42 | 174 | 16.6% | 3.1% | 1.06 | -3.1% | 332 | 1.50 | 1.9% | 78.1 | 9/9 | 1.00 | 0.80 | 0.26 | 3 | 8.7% | 0.48 | 0.53 | 15.0% | 13.5% | 2.9% | 14.5%/10.6% | 6.4 (interpolated) | pass | 0.186 (unverified) | 0.07 |
| 19 | `cfg_d70c` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=85, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 4/240/73 | 317 | 22.8% | 4.2% | 1.14 | -3.9% | 315 | 1.36 | 3.4% | 142.2 | 9/9 | 1.00 | 0.84 | 0.30 | 4 | 9.0% | 0.55 | 0.51 | 19.6% | 16.5% | 8.2% | 18.0%/13.9% | 4.8 (interpolated) | pass | 0.231 (unverified) | -0.59 |
| 20 | `cfg_4f41` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=55, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 5/115/36 | 156 | 12.5% | 2.4% | 0.93 | -3.3% | 385 | 1.43 | 1.7% | 70.2 | 7/7 | 0.86 | 0.89 | 0.04 | 3 | 5.4% | 0.56 | 0.59 | 11.4% | 9.9% | 3.3% | 11.6%/8.9% | 5.8 (interpolated) | pass | 0.107 (unverified) | -0.95 |
| 21 | `cfg_c6a1` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=55, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 4/123/0 | 127 | 12.4% | 2.4% | 0.96 | -2.8% | 371 | 1.64 | 1.5% | 57.2 | 7/7 | 1.00 | 0.85 | 0.11 | 4 | 6.5% | 0.46 | 0.59 | 11.3% | 10.1% | 2.1% | 11.6%/8.9% | 6.7 (interpolated) | pass | 0.109 (unverified) | -0.84 |
| 22 | `cfg_8910` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=55, entry_z=-3.0, exit_z=1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 0/129/0 | 129 | 18.7% | 3.5% | 0.92 | -5.5% | 332 | 1.70 | 2.4% | 58.6 | 9/9 | 1.00 | 0.89 | 0.04 | 4 | 9.3% | 0.49 | 0.74 | 17.5% | 16.3% | 7.4% | 17.5%/12.0% | 9.1 (interpolated) | pass | 0.068 (unverified) | -0.36 |
| 23 | `cfg_cdae` | timeframe=15min, mean_type=ema, mean_lookback=35, std_lookback=85, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 6/200/56 | 262 | 25.7% | 4.7% | 1.40 | -2.7% | 314 | 1.53 | 2.8% | 117.1 | 8/8 | 1.00 | 0.96 | 0.44 | 4 | 13.3% | 0.43 | 0.47 | 23.0% | 20.4% | 7.5% | 21.3%/16.4% | 6.3 (interpolated) | pass | 0.440 (unverified) | -0.32 |
| 24 | `cfg_c27b` | timeframe=15min, mean_type=sma, mean_lookback=85, std_lookback=85, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 2/112/0 | 114 | 15.6% | 3.0% | 1.08 | -3.1% | 304 | 1.78 | 1.4% | 51.3 | 8/8 | 1.00 | 0.87 | 0.21 | 3 | 7.7% | 0.49 | 0.51 | 14.5% | 13.3% | 7.1% | 14.3%/11.5% | 8.5 (interpolated) | pass | 0.186 (unverified) | 0.10 |
| 25 | `cfg_f69a` | timeframe=15min, mean_type=sma, mean_lookback=85, std_lookback=85, entry_z=-3.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 1/105/0 | 106 | 20.7% | 3.8% | 1.06 | -3.3% | 153 | 1.86 | 2.9% | 47.8 | 8/8 | 1.00 | 0.89 | 0.17 | 5 | 10.0% | 0.51 | 0.53 | 19.9% | 19.1% | 6.1% | 19.6%/14.5% | 11.6 (interpolated) | pass | 0.179 (unverified) | 0.18 |
| 26 | `cfg_15b8` | timeframe=15min, mean_type=sma, mean_lookback=85, std_lookback=85, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 6/105/0 | 111 | 17.5% | 3.3% | 0.97 | -3.5% | 186 | 1.74 | 2.0% | 50.0 | 9/9 | 1.00 | 0.88 | 0.09 | 4 | 10.4% | 0.41 | 0.59 | 16.5% | 15.4% | 9.3% | 15.6%/11.7% | 9.7 (interpolated) | pass | 0.122 (unverified) | 0.40 |
| 27 | `cfg_61bb` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=95, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 13/132/57 | 202 | 17.5% | 3.3% | 0.90 | -4.9% | 335 | 1.37 | 3.1% | 90.6 | 10/10 | 1.00 | 0.81 | 0.09 | 3 | 6.0% | 0.67 | 0.63 | 15.3% | 13.5% | 11.2% | 14.1%/8.8% | 5.7 (interpolated) | pass | 0.096 (unverified) | 0.02 |
| 28 | `cfg_0d59` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=85, entry_z=-2.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 5/116/0 | 121 | 14.2% | 2.7% | 1.00 | -3.5% | 324 | 1.68 | 1.5% | 54.5 | 9/9 | 1.00 | 0.87 | 0.13 | 4 | 6.2% | 0.57 | 0.52 | 13.1% | 12.2% | 5.8% | 13.4%/10.3% | 7.5 (interpolated) | pass | 0.148 (unverified) | 0.22 |
| 29 | `cfg_980f` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=85, entry_z=-2.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 0/121/0 | 121 | 14.1% | 2.7% | 1.00 | -3.5% | 324 | 1.67 | 1.5% | 54.5 | 10/10 | 1.00 | 0.87 | 0.13 | 4 | 6.2% | 0.57 | 0.53 | 13.0% | 12.1% | 4.8% | 13.3%/10.8% | 7.5 (interpolated) | pass | 0.146 (unverified) | 0.24 |
| 30 | `cfg_c7e0` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=85, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 1/167/0 | 168 | 23.5% | 4.3% | 1.01 | -3.8% | 284 | 1.66 | 3.1% | 75.7 | 11/11 | 1.00 | 0.93 | 0.08 | 4 | 11.6% | 0.46 | 0.62 | 21.4% | 19.6% | 9.0% | 21.1%/16.9% | 8.5 (interpolated) | pass | 0.119 (unverified) | 0.25 |
| 31 | `cfg_6ed9` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=85, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 1/167/0 | 168 | 23.8% | 4.4% | 1.02 | -3.8% | 284 | 1.67 | 3.1% | 75.7 | 10/10 | 1.00 | 0.89 | 0.13 | 5 | 11.8% | 0.45 | 0.61 | 21.5% | 20.0% | 9.2% | 20.9%/15.6% | 8.5 (interpolated) | pass | 0.123 (unverified) | 0.23 |
| 32 | `cfg_1e2c` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=95, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 0/144/55 | 199 | 18.2% | 3.4% | 0.95 | -5.0% | 477 | 1.40 | 3.1% | 89.5 | 10/10 | 1.00 | 0.82 | 0.13 | 3 | 7.3% | 0.61 | 0.60 | 16.4% | 14.2% | 8.2% | 15.3%/9.8% | 6.0 (interpolated) | pass | 0.115 (unverified) | 0.01 |
| 33 | `cfg_231f` | timeframe=15min, mean_type=sma, mean_lookback=115, std_lookback=105, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 3/103/0 | 106 | 16.2% | 3.0% | 0.96 | -4.7% | 388 | 1.75 | 1.9% | 47.7 | 7/7 | 1.00 | 0.79 | 0.18 | 4 | 8.4% | 0.47 | 0.63 | 15.2% | 14.0% | 14.8% | 14.3%/11.2% | 9.2 (interpolated) | pass | 0.115 (unverified) | -0.28 |
| 34 | `cfg_fbf5` | timeframe=15min, mean_type=ema, mean_lookback=35, std_lookback=85, entry_z=-2.0, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 2/204/56 | 262 | 26.0% | 4.7% | 1.40 | -2.7% | 314 | 1.53 | 2.8% | 117.3 | 7/7 | 1.00 | 0.94 | 0.47 | 4 | 13.6% | 0.43 | 0.48 | 23.2% | 20.6% | 7.3% | 21.9%/17.3% | 6.3 (interpolated) | pass | 0.443 (unverified) | -0.30 |
| 35 | `cfg_3c77` | timeframe=15min, mean_type=ema, mean_lookback=105, std_lookback=95, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 4/75/26 | 105 | 16.2% | 3.1% | 1.06 | -3.1% | 307 | 1.78 | 1.1% | 47.4 | 8/8 | 0.88 | 0.90 | 0.16 | 3 | 8.9% | 0.45 | 0.55 | 15.2% | 14.3% | 12.4% | 15.8%/12.7% | 9.6 (interpolated) | pass | 0.179 (unverified) | 0.62 |
| 36 | `cfg_1737` | timeframe=15min, mean_type=ema, mean_lookback=105, std_lookback=95, entry_z=-3.0, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 1/78/26 | 105 | 17.0% | 3.2% | 1.09 | -3.1% | 307 | 1.81 | 1.1% | 47.4 | 8/8 | 0.88 | 0.91 | 0.18 | 3 | 9.7% | 0.43 | 0.57 | 15.9% | 14.8% | 12.8% | 16.4%/12.9% | 9.9 (interpolated) | pass | 0.198 (unverified) | 0.62 |
| 37 | `cfg_8982` | timeframe=15min, mean_type=sma, mean_lookback=115, std_lookback=105, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 0/106/0 | 106 | 15.2% | 2.9% | 0.93 | -4.6% | 388 | 1.71 | 2.0% | 47.8 | 8/8 | 1.00 | 0.82 | 0.11 | 4 | 7.5% | 0.49 | 0.67 | 14.0% | 13.1% | 13.4% | 13.6%/11.7% | 8.8 (interpolated) | pass | 0.098 (unverified) | -0.30 |
| 38 | `cfg_5121` | timeframe=15min, mean_type=ema, mean_lookback=35, std_lookback=95, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 5/156/0 | 161 | 20.9% | 3.9% | 1.00 | -3.0% | 284 | 1.63 | 2.9% | 72.0 | 9/9 | 1.00 | 0.85 | 0.15 | 5 | 10.5% | 0.50 | 0.61 | 19.6% | 17.7% | 5.4% | 18.8%/13.8% | 8.1 (interpolated) | pass | 0.131 (unverified) | -0.39 |
| 39 | `cfg_fd80` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=95, entry_z=-2.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 25/221/69 | 315 | 19.0% | 3.5% | 1.08 | -3.0% | 209 | 1.33 | 3.4% | 141.2 | 7/7 | 1.00 | 0.78 | 0.30 | 4 | 8.7% | 0.52 | 0.52 | 16.1% | 13.0% | 12.3% | 15.5%/11.8% | 4.4 (interpolated) | pass | 0.176 (unverified) | 0.30 |
| 40 | `cfg_9495` | timeframe=15min, mean_type=sma, mean_lookback=65, std_lookback=85, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 2/91/24 | 117 | 14.7% | 2.8% | 1.04 | -4.0% | 276 | 1.68 | 1.3% | 52.8 | 8/8 | 1.00 | 0.70 | 0.34 | 3 | 6.0% | 0.61 | 0.51 | 13.5% | 12.4% | 7.2% | 13.7%/10.7% | 8.0 (interpolated) | pass | 0.176 (unverified) | 0.11 |
| 41 | `cfg_b875` | timeframe=15min, mean_type=ema, mean_lookback=55, std_lookback=105, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 3/190/57 | 250 | 19.0% | 3.5% | 1.08 | -3.6% | 314 | 1.39 | 2.7% | 111.8 | 8/8 | 1.00 | 0.84 | 0.24 | 4 | 7.4% | 0.57 | 0.57 | 16.7% | 14.4% | 9.4% | 15.0%/10.5% | 5.2 (interpolated) | pass | 0.199 (unverified) | -0.39 |
| 42 | `cfg_9fae` | timeframe=15min, mean_type=sma, mean_lookback=65, std_lookback=85, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 0/93/24 | 117 | 14.6% | 2.8% | 1.04 | -4.0% | 276 | 1.68 | 1.3% | 52.8 | 9/9 | 1.00 | 0.68 | 0.36 | 3 | 6.0% | 0.61 | 0.51 | 13.4% | 12.4% | 6.7% | 13.4%/10.4% | 8.0 (interpolated) | pass | 0.174 (unverified) | 0.11 |
| 43 | `cfg_4110` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=65, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 9/102/0 | 111 | 18.3% | 3.4% | 1.01 | -5.7% | 332 | 1.72 | 2.0% | 50.4 | 9/9 | 1.00 | 0.92 | 0.09 | 4 | 7.7% | 0.60 | 0.60 | 17.5% | 16.4% | 1.4% | 17.3%/13.6% | 10.2 (interpolated) | pass | 0.133 (unverified) | -0.13 |
| 44 | `cfg_67e5` | timeframe=15min, mean_type=ema, mean_lookback=55, std_lookback=105, entry_z=-2.0, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 0/193/57 | 250 | 19.0% | 3.5% | 1.08 | -3.6% | 314 | 1.39 | 2.7% | 111.8 | 7/7 | 1.00 | 0.83 | 0.25 | 4 | 7.4% | 0.57 | 0.57 | 16.7% | 14.4% | 9.2% | 15.9%/11.2% | 5.2 (interpolated) | pass | 0.199 (unverified) | -0.39 |
| 45 | `cfg_7386` | timeframe=15min, mean_type=ema, mean_lookback=35, std_lookback=95, entry_z=-2.0, exit_z=1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 1/160/0 | 161 | 20.8% | 3.9% | 0.98 | -2.9% | 289 | 1.63 | 3.0% | 72.0 | 8/8 | 1.00 | 0.84 | 0.15 | 5 | 9.6% | 0.53 | 0.63 | 18.8% | 17.5% | 4.0% | 19.3%/14.3% | 8.0 (interpolated) | pass | 0.121 (unverified) | -0.39 |
| 46 | `cfg_9a29` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=85, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 38/134/0 | 172 | 26.1% | 4.7% | 1.02 | -4.1% | 477 | 1.65 | 4.5% | 77.6 | 9/9 | 1.00 | 0.85 | 0.16 | 5 | 11.4% | 0.56 | 0.61 | 24.7% | 23.0% | 10.4% | 24.9%/19.8% | 9.3 (interpolated) | pass | 0.134 (unverified) | -0.53 |
| 47 | `cfg_0dfd` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=105, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 0/107/41 | 148 | 15.0% | 2.8% | 0.87 | -2.9% | 243 | 1.43 | 2.3% | 66.7 | 9/9 | 1.00 | 0.61 | 0.27 | 4 | 7.1% | 0.53 | 0.73 | 13.8% | 12.5% | -1.8% | 11.9%/8.0% | 6.7 (interpolated) | pass | 0.080 (unverified) | -0.12 |
| 48 | `cfg_5a17` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=65, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 0/111/0 | 111 | 17.7% | 3.3% | 0.99 | -5.5% | 332 | 1.70 | 2.0% | 50.2 | 10/10 | 0.90 | 0.88 | 0.10 | 4 | 7.4% | 0.60 | 0.62 | 16.6% | 15.6% | 0.4% | 16.4%/13.1% | 9.7 (interpolated) | pass | 0.119 (unverified) | -0.11 |
| 49 | `cfg_66ec` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=95, entry_z=-2.0, exit_z=1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 1/193/0 | 194 | 22.2% | 4.1% | 0.90 | -3.9% | 314 | 1.53 | 3.6% | 87.3 | 9/9 | 1.00 | 0.81 | 0.09 | 4 | 11.3% | 0.44 | 0.70 | 19.9% | 18.4% | 16.3% | 19.7%/15.4% | 7.2 (interpolated) | pass | 0.079 (unverified) | -0.38 |
| 50 | `cfg_0851` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=105, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 0/107/41 | 148 | 15.0% | 2.8% | 0.87 | -2.9% | 243 | 1.43 | 2.3% | 66.7 | 10/10 | 1.00 | 0.63 | 0.24 | 4 | 7.1% | 0.53 | 0.73 | 13.8% | 12.5% | -1.8% | 12.2%/7.8% | 6.7 (interpolated) | pass | 0.080 (unverified) | -0.12 |
| 51 | `cfg_6123` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=95, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 4/190/0 | 194 | 22.3% | 4.1% | 0.91 | -3.9% | 314 | 1.53 | 3.5% | 87.2 | 10/10 | 1.00 | 0.81 | 0.11 | 4 | 11.2% | 0.45 | 0.67 | 19.8% | 18.4% | 16.6% | 20.0%/14.4% | 7.1 (interpolated) | pass | 0.084 (unverified) | -0.37 |
| 52 | `cfg_4185` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=95, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 3/243/69 | 315 | 20.0% | 3.7% | 1.10 | -3.0% | 209 | 1.34 | 3.4% | 141.1 | 8/8 | 1.00 | 0.84 | 0.26 | 4 | 9.6% | 0.49 | 0.54 | 17.1% | 14.2% | 10.7% | 16.8%/12.8% | 4.5 (interpolated) | pass | 0.191 (unverified) | 0.32 |
| 53 | `cfg_455e` | timeframe=15min, mean_type=sma, mean_lookback=65, std_lookback=55, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 3/139/0 | 142 | 23.4% | 4.3% | 0.95 | -7.6% | 347 | 1.60 | 3.9% | 64.5 | 9/9 | 1.00 | 0.69 | 0.27 | 3 | 11.8% | 0.51 | 0.61 | 21.9% | 20.3% | 4.8% | 21.4%/16.4% | 9.9 (interpolated) | pass | 0.111 (unverified) | -0.00 |
| 54 | `cfg_34d8` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=85, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 2/139/0 | 141 | 23.3% | 4.3% | 1.00 | -3.9% | 318 | 1.76 | 2.6% | 63.5 | 10/10 | 1.00 | 0.92 | 0.08 | 4 | 10.3% | 0.56 | 0.68 | 21.9% | 20.4% | 7.3% | 21.4%/16.5% | 9.9 (interpolated) | pass | 0.112 (unverified) | 0.14 |
| 55 | `cfg_aec7` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=105, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 12/116/51 | 179 | 20.0% | 3.7% | 0.99 | -3.3% | 153 | 1.45 | 2.7% | 80.1 | 9/9 | 0.89 | 0.81 | 0.18 | 5 | 9.5% | 0.52 | 0.60 | 18.2% | 16.6% | 6.2% | 16.6%/12.3% | 7.1 (interpolated) | pass | 0.127 (unverified) | 0.03 |
| 56 | `cfg_062d` | timeframe=15min, mean_type=sma, mean_lookback=105, std_lookback=85, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 11/118/0 | 129 | 22.9% | 4.2% | 1.01 | -4.4% | 308 | 1.69 | 3.5% | 57.5 | 8/8 | 1.00 | 0.61 | 0.40 | 4 | 12.3% | 0.43 | 0.54 | 21.4% | 20.1% | 13.2% | 20.3%/15.7% | 10.2 (interpolated) | pass | 0.157 (unverified) | -0.07 |
| 57 | `cfg_fa05` | timeframe=15min, mean_type=sma, mean_lookback=85, std_lookback=85, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 6/99/40 | 145 | 15.9% | 3.0% | 0.88 | -3.0% | 397 | 1.49 | 2.2% | 65.3 | 9/9 | 0.89 | 0.83 | 0.05 | 3 | 6.9% | 0.57 | 0.63 | 14.5% | 13.3% | 6.0% | 14.2%/9.9% | 7.2 (interpolated) | pass | 0.087 (unverified) | 0.46 |
| 58 | `cfg_ebbd` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=55, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 33/104/0 | 137 | 25.7% | 4.7% | 1.21 | -3.9% | 347 | 1.82 | 3.6% | 62.6 | 8/8 | 1.00 | 0.93 | 0.28 | 4 | 14.5% | 0.44 | 0.43 | 23.9% | 22.4% | 14.9% | 23.3%/19.7% | 11.0 (interpolated) | pass | 0.277 (unverified) | -0.13 |
| 59 | `cfg_76d7` | timeframe=15min, mean_type=sma, mean_lookback=85, std_lookback=95, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 5/86/35 | 126 | 15.9% | 3.0% | 0.90 | -3.1% | 314 | 1.52 | 1.9% | 56.8 | 9/9 | 1.00 | 0.77 | 0.13 | 4 | 6.3% | 0.58 | 0.64 | 14.9% | 13.8% | 3.3% | 14.8%/11.9% | 8.1 (interpolated) | pass | 0.095 (unverified) | 0.03 |
| 60 | `cfg_33ce` | timeframe=15min, mean_type=ema, mean_lookback=35, std_lookback=85, entry_z=-2.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 10/84/28 | 122 | 13.2% | 2.5% | 1.01 | -4.2% | 324 | 1.59 | 1.3% | 55.1 | 8/8 | 1.00 | 0.84 | 0.17 | 3 | 5.8% | 0.58 | 0.50 | 12.1% | 11.0% | -0.1% | 12.4%/9.5% | 7.0 (interpolated) | pass | 0.159 (unverified) | -0.06 |
| 61 | `cfg_072d` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=85, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 19/123/0 | 142 | 21.4% | 4.0% | 0.97 | -3.8% | 318 | 1.69 | 2.6% | 63.9 | 9/9 | 1.00 | 0.86 | 0.11 | 3 | 8.2% | 0.62 | 0.65 | 20.0% | 18.5% | 7.1% | 19.2%/15.7% | 9.3 (interpolated) | pass | 0.107 (unverified) | 0.17 |
| 62 | `cfg_4db9` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=85, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 9/270/0 | 279 | 22.8% | 4.2% | 0.87 | -6.2% | 203 | 1.35 | 5.1% | 126.0 | 9/9 | 1.00 | 0.86 | 0.01 | 4 | 10.5% | 0.52 | 0.63 | 20.4% | 17.8% | 6.6% | 20.3%/15.5% | 5.5 (interpolated) | pass | 0.100 (unverified) | -0.37 |
| 63 | `cfg_0674` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=105, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 2/171/47 | 220 | 15.8% | 3.0% | 1.04 | -3.8% | 315 | 1.41 | 2.4% | 98.4 | 8/8 | 1.00 | 0.97 | 0.07 | 4 | 7.6% | 0.49 | 0.56 | 13.7% | 11.6% | 2.4% | 12.8%/8.8% | 4.9 (interpolated) | pass | 0.175 (unverified) | 0.03 |
| 64 | `cfg_bd35` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=105, entry_z=-2.0, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 0/173/47 | 220 | 15.8% | 3.0% | 1.04 | -3.8% | 315 | 1.41 | 2.4% | 98.4 | 7/7 | 1.00 | 0.95 | 0.09 | 4 | 7.6% | 0.49 | 0.56 | 13.7% | 11.6% | 2.4% | 12.5%/8.4% | 4.9 (interpolated) | pass | 0.175 (unverified) | 0.03 |
| 65 | `cfg_c85a` | timeframe=15min, mean_type=ema, mean_lookback=65, std_lookback=85, entry_z=-2.5, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 0/161/0 | 161 | 12.7% | 2.4% | 0.83 | -4.8% | 278 | 1.43 | 2.0% | 72.4 | 9/9 | 1.00 | 0.74 | 0.10 | 3 | 4.5% | 0.61 | 0.76 | 10.9% | 9.4% | 1.4% | 11.7%/8.3% | 5.3 (interpolated) | pass | 0.083 (unverified) | -0.08 |
| 66 | `cfg_e8d8` | timeframe=15min, mean_type=ema, mean_lookback=65, std_lookback=85, entry_z=-2.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 1/160/0 | 161 | 12.7% | 2.4% | 0.83 | -4.8% | 278 | 1.43 | 2.0% | 72.4 | 10/10 | 1.00 | 0.78 | 0.05 | 3 | 4.5% | 0.61 | 0.76 | 10.9% | 9.4% | 1.6% | 11.9%/7.4% | 5.3 (interpolated) | pass | 0.083 (unverified) | -0.08 |
| 67 | `cfg_aadc` | timeframe=15min, mean_type=ema, mean_lookback=105, std_lookback=95, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 7/68/33 | 108 | 20.1% | 3.7% | 1.04 | -2.8% | 318 | 1.73 | 1.6% | 48.8 | 9/9 | 1.00 | 0.79 | 0.26 | 4 | 11.4% | 0.42 | 0.55 | 19.2% | 17.6% | 8.6% | 18.4%/15.1% | 11.0 (interpolated) | pass | 0.158 (unverified) | 0.56 |
| 68 | `cfg_4c8f` | timeframe=15min, mean_type=ema, mean_lookback=35, std_lookback=85, entry_z=-2.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 0/94/28 | 122 | 12.8% | 2.4% | 0.99 | -4.2% | 324 | 1.57 | 1.3% | 55.2 | 9/9 | 1.00 | 0.88 | 0.11 | 3 | 5.5% | 0.59 | 0.51 | 11.6% | 10.4% | -0.5% | 12.1%/9.3% | 6.8 (interpolated) | pass | 0.147 (unverified) | -0.06 |
| 69 | `cfg_f808` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=85, entry_z=-2.0, exit_z=1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 2/277/0 | 279 | 22.5% | 4.1% | 0.87 | -6.2% | 203 | 1.35 | 5.1% | 126.0 | 8/8 | 1.00 | 0.79 | 0.08 | 4 | 10.2% | 0.53 | 0.61 | 20.2% | 17.2% | 5.1% | 19.3%/12.8% | 5.4 (interpolated) | pass | 0.099 (unverified) | -0.36 |
| 70 | `cfg_e790` | timeframe=15min, mean_type=ema, mean_lookback=85, std_lookback=85, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 2/76/23 | 101 | 10.6% | 2.0% | 0.81 | -6.7% | 377 | 1.50 | 1.1% | 45.8 | 8/8 | 1.00 | 0.80 | 0.02 | 3 | 2.6% | 0.76 | 0.64 | 9.6% | 8.7% | -1.1% | 10.8%/7.6% | 6.9 (interpolated) | pass | 0.082 (unverified) | 0.73 |
| 71 | `cfg_daa4` | timeframe=15min, mean_type=ema, mean_lookback=35, std_lookback=105, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 2/141/42 | 185 | 14.0% | 2.7% | 0.95 | -4.3% | 318 | 1.40 | 2.0% | 83.0 | 7/7 | 1.00 | 0.83 | 0.12 | 4 | 6.2% | 0.53 | 0.63 | 12.3% | 10.3% | 1.8% | 12.1%/8.1% | 5.2 (interpolated) | pass | 0.135 (unverified) | -0.07 |
| 72 | `cfg_4eeb` | timeframe=15min, mean_type=ema, mean_lookback=35, std_lookback=105, entry_z=-2.0, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 0/143/42 | 185 | 14.0% | 2.7% | 0.95 | -4.3% | 318 | 1.40 | 2.0% | 83.0 | 6/6 | 1.00 | 0.84 | 0.11 | 4 | 6.2% | 0.53 | 0.63 | 12.3% | 10.3% | 1.8% | 11.4%/8.3% | 5.2 (interpolated) | pass | 0.135 (unverified) | -0.07 |
| 73 | `cfg_0157` | timeframe=15min, mean_type=ema, mean_lookback=85, std_lookback=85, entry_z=-3.0, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 0/78/23 | 101 | 10.5% | 2.0% | 0.81 | -6.7% | 377 | 1.50 | 1.1% | 45.8 | 8/8 | 1.00 | 0.80 | 0.01 | 3 | 2.6% | 0.77 | 0.65 | 9.6% | 8.6% | -1.4% | 10.7%/7.3% | 6.9 (interpolated) | pass | 0.081 (unverified) | 0.73 |
| 74 | `cfg_55ea` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=105, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 0/126/47 | 173 | 19.9% | 3.7% | 1.00 | -3.3% | 153 | 1.48 | 2.7% | 77.6 | 9/9 | 0.89 | 0.77 | 0.22 | 5 | 10.0% | 0.49 | 0.60 | 18.3% | 16.6% | 3.5% | 16.3%/12.6% | 7.4 (interpolated) | pass | 0.128 (unverified) | 0.03 |
| 75 | `cfg_abc8` | timeframe=15min, mean_type=ema, mean_lookback=55, std_lookback=85, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 15/114/0 | 129 | 13.9% | 2.6% | 0.78 | -3.6% | 181 | 1.53 | 2.3% | 57.7 | 10/10 | 0.90 | 0.70 | 0.09 | 5 | 6.6% | 0.53 | 0.72 | 12.9% | 11.5% | 1.0% | 12.8%/8.5% | 7.0 (interpolated) | pass | 0.055 (unverified) | 0.07 |
| 76 | `cfg_7caa` | timeframe=15min, mean_type=sma, mean_lookback=105, std_lookback=105, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 5/95/0 | 100 | 16.1% | 3.0% | 0.93 | -3.3% | 284 | 1.73 | 1.8% | 45.3 | 8/8 | 1.00 | 0.72 | 0.21 | 5 | 10.2% | 0.35 | 0.63 | 15.1% | 14.3% | 9.8% | 15.7%/12.6% | 9.9 (interpolated) | pass | 0.107 (unverified) | -0.47 |
| 77 | `cfg_b005` | timeframe=15min, mean_type=sma, mean_lookback=105, std_lookback=85, entry_z=-3.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 1/127/0 | 128 | 23.0% | 4.2% | 0.98 | -4.4% | 308 | 1.69 | 3.5% | 57.2 | 8/8 | 1.00 | 0.57 | 0.40 | 5 | 12.4% | 0.43 | 0.59 | 21.5% | 19.8% | 13.0% | 21.2%/16.7% | 10.4 (interpolated) | pass | 0.134 (unverified) | -0.06 |
| 78 | `cfg_ca7d` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=95, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 36/107/0 | 143 | 21.4% | 4.0% | 0.94 | -5.6% | 398 | 1.59 | 3.7% | 64.4 | 9/9 | 1.00 | 0.74 | 0.20 | 5 | 7.9% | 0.63 | 0.60 | 19.8% | 18.3% | 6.2% | 19.8%/15.1% | 9.0 (interpolated) | pass | 0.115 (unverified) | 0.04 |
| 79 | `cfg_e052` | timeframe=15min, mean_type=sma, mean_lookback=65, std_lookback=85, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 13/174/79 | 266 | 21.0% | 3.9% | 0.94 | -3.8% | 363 | 1.33 | 4.0% | 119.5 | 10/10 | 0.80 | 0.73 | 0.21 | 3 | 8.9% | 0.58 | 0.55 | 18.7% | 16.5% | 4.2% | 18.1%/12.1% | 5.3 (interpolated) | pass | 0.113 (unverified) | -0.12 |
| 80 | `cfg_1ed7` | timeframe=15min, mean_type=sma, mean_lookback=65, std_lookback=85, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 31/149/0 | 180 | 20.0% | 3.7% | 0.87 | -3.9% | 525 | 1.50 | 4.8% | 80.9 | 9/9 | 1.00 | 0.72 | 0.15 | 3 | 5.4% | 0.73 | 0.58 | 17.7% | 15.9% | 3.1% | 18.6%/14.0% | 7.0 (interpolated) | pass | 0.086 (unverified) | -0.45 |
| 81 | `cfg_b712` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=75, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 2/102/0 | 104 | 12.7% | 2.4% | 0.93 | -3.6% | 415 | 1.68 | 1.3% | 47.1 | 8/8 | 1.00 | 0.83 | 0.11 | 3 | 5.0% | 0.62 | 0.58 | 11.7% | 10.6% | 5.9% | 11.4%/8.5% | 7.8 (interpolated) | pass | 0.114 (unverified) | -0.29 |
| 82 | `cfg_373b` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=75, entry_z=-3.0, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 0/104/0 | 104 | 12.7% | 2.4% | 0.93 | -3.6% | 415 | 1.68 | 1.3% | 47.1 | 8/8 | 1.00 | 0.83 | 0.11 | 3 | 5.0% | 0.61 | 0.58 | 11.6% | 10.6% | 5.7% | 11.7%/9.1% | 7.7 (interpolated) | pass | 0.114 (unverified) | -0.28 |
| 83 | `cfg_eb13` | timeframe=15min, mean_type=sma, mean_lookback=95, std_lookback=85, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 11/109/0 | 120 | 20.1% | 3.7% | 1.01 | -3.4% | 284 | 1.71 | 3.2% | 53.9 | 8/8 | 1.00 | 0.74 | 0.26 | 5 | 11.3% | 0.44 | 0.56 | 18.7% | 17.5% | 8.1% | 18.3%/14.6% | 10.0 (interpolated) | pass | 0.149 (unverified) | 0.03 |
| 84 | `cfg_79d2` | timeframe=15min, mean_type=sma, mean_lookback=105, std_lookback=105, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 0/100/0 | 100 | 15.2% | 2.9% | 0.88 | -3.3% | 268 | 1.69 | 1.8% | 45.2 | 9/9 | 1.00 | 0.78 | 0.11 | 5 | 9.3% | 0.37 | 0.67 | 14.5% | 13.5% | 9.0% | 15.0%/11.9% | 9.3 (interpolated) | pass | 0.089 (unverified) | -0.47 |
| 85 | `cfg_2295` | timeframe=15min, mean_type=ema, mean_lookback=75, std_lookback=105, entry_z=-2.0, exit_z=1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 2/228/103 | 333 | 29.7% | 5.3% | 0.94 | -9.6% | 203 | 1.33 | 5.1% | 149.4 | 8/8 | 1.00 | 0.64 | 0.30 | 4 | 14.5% | 0.52 | 0.65 | 25.7% | 22.6% | 12.8% | 24.9%/17.9% | 5.6 (interpolated) | pass | 0.102 (unverified) | -0.08 |
| 86 | `cfg_aea9` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=95, entry_z=-2.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 1/120/0 | 121 | 12.3% | 2.3% | 0.83 | -4.5% | 318 | 1.52 | 1.5% | 54.5 | 9/9 | 1.00 | 0.69 | 0.14 | 3 | 4.2% | 0.68 | 0.73 | 10.8% | 9.5% | 3.4% | 10.3%/7.7% | 6.5 (interpolated) | pass | 0.088 (unverified) | -0.04 |
| 87 | `cfg_2459` | timeframe=15min, mean_type=ema, mean_lookback=55, std_lookback=85, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 1/128/0 | 129 | 13.9% | 2.6% | 0.78 | -3.6% | 181 | 1.52 | 2.4% | 57.9 | 11/11 | 0.91 | 0.72 | 0.06 | 4 | 6.8% | 0.51 | 0.79 | 12.5% | 11.1% | -0.2% | 12.6%/9.2% | 6.9 (interpolated) | pass | 0.054 (unverified) | 0.13 |
| 88 | `cfg_62a6` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=95, entry_z=-2.5, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 0/121/0 | 121 | 12.3% | 2.3% | 0.83 | -4.5% | 318 | 1.52 | 1.5% | 54.5 | 8/8 | 1.00 | 0.69 | 0.14 | 3 | 4.2% | 0.68 | 0.73 | 10.8% | 9.5% | 3.3% | 10.7%/7.5% | 6.5 (interpolated) | pass | 0.088 (unverified) | -0.04 |
| 89 | `cfg_83bb` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=55, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 13/125/0 | 138 | 16.5% | 3.1% | 0.92 | -6.2% | 347 | 1.54 | 2.5% | 62.8 | 9/9 | 0.89 | 0.76 | 0.16 | 4 | 8.8% | 0.48 | 0.62 | 15.6% | 14.2% | 8.6% | 15.2%/10.3% | 7.8 (interpolated) | pass | 0.095 (unverified) | -0.37 |
| 90 | `cfg_9b7e` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=55, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 2/139/0 | 141 | 10.4% | 2.0% | 0.76 | -4.2% | 284 | 1.44 | 1.7% | 63.9 | 8/8 | 0.75 | 0.74 | 0.02 | 4 | 3.4% | 0.69 | 0.70 | 9.1% | 7.7% | 6.4% | 9.8%/7.2% | 5.3 (interpolated) | pass | 0.054 (unverified) | -0.36 |
| 91 | `cfg_228b` | timeframe=15min, mean_type=sma, mean_lookback=65, std_lookback=105, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 12/131/59 | 202 | 17.8% | 3.3% | 0.81 | -4.9% | 199 | 1.35 | 3.1% | 91.0 | 9/9 | 0.89 | 0.67 | 0.14 | 4 | 6.2% | 0.65 | 0.63 | 15.9% | 13.5% | 6.3% | 14.9%/9.1% | 5.7 (interpolated) | pass | 0.070 (unverified) | -0.05 |
| 92 | `cfg_efb0` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=105, entry_z=-2.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 17/190/59 | 266 | 13.8% | 2.6% | 0.88 | -4.1% | 315 | 1.28 | 2.9% | 120.2 | 6/6 | 1.00 | 0.81 | 0.07 | 3 | 6.3% | 0.55 | 0.59 | 11.4% | 8.6% | 7.0% | 11.5%/8.0% | 3.9 (interpolated) | pass | 0.098 (unverified) | 0.31 |
| 93 | `cfg_5831` | timeframe=15min, mean_type=ema, mean_lookback=75, std_lookback=105, entry_z=-2.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 7/223/103 | 333 | 29.0% | 5.2% | 0.92 | -9.6% | 203 | 1.33 | 5.1% | 149.6 | 9/9 | 1.00 | 0.69 | 0.24 | 4 | 14.2% | 0.51 | 0.64 | 25.0% | 21.3% | 12.8% | 24.2%/17.1% | 5.5 (interpolated) | pass | 0.097 (unverified) | -0.08 |
| 94 | `cfg_1510` | timeframe=15min, mean_type=ema, mean_lookback=105, std_lookback=95, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 1/74/33 | 108 | 19.4% | 3.6% | 1.01 | -2.8% | 318 | 1.70 | 1.6% | 48.9 | 10/10 | 1.00 | 0.81 | 0.19 | 4 | 11.4% | 0.40 | 0.59 | 18.0% | 16.9% | 7.2% | 18.1%/13.4% | 10.6 (interpolated) | pass | 0.140 (unverified) | 0.54 |
| 95 | `cfg_3b1d` | timeframe=15min, mean_type=sma, mean_lookback=95, std_lookback=85, entry_z=-3.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 1/119/0 | 120 | 20.4% | 3.8% | 0.98 | -3.4% | 284 | 1.73 | 3.3% | 53.9 | 8/8 | 1.00 | 0.71 | 0.27 | 5 | 12.8% | 0.37 | 0.62 | 18.7% | 17.5% | 7.5% | 18.3%/14.4% | 10.1 (interpolated) | pass | 0.123 (unverified) | 0.07 |
| 96 | `cfg_d288` | timeframe=15min, mean_type=sma, mean_lookback=65, std_lookback=85, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 2/185/79 | 266 | 20.1% | 3.7% | 0.91 | -4.4% | 524 | 1.32 | 4.1% | 119.8 | 11/11 | 0.82 | 0.68 | 0.23 | 3 | 8.4% | 0.59 | 0.57 | 17.8% | 15.5% | 3.0% | 17.1%/11.5% | 5.2 (interpolated) | pass | 0.101 (unverified) | -0.05 |
| 97 | `cfg_01b9` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=105, entry_z=-2.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 2/205/59 | 266 | 13.5% | 2.6% | 0.86 | -4.9% | 315 | 1.27 | 2.9% | 120.1 | 7/7 | 1.00 | 0.77 | 0.09 | 3 | 6.0% | 0.57 | 0.65 | 11.2% | 8.7% | 5.6% | 11.0%/8.2% | 3.9 (interpolated) | pass | 0.095 (unverified) | 0.31 |
| 98 | `cfg_a82b` | timeframe=15min, mean_type=ema, mean_lookback=65, std_lookback=105, entry_z=-2.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 73/130/0 | 203 | 25.4% | 4.6% | 0.87 | -6.7% | 318 | 1.44 | 5.0% | 91.2 | 7/7 | 1.00 | 0.72 | 0.15 | 3 | 3.1% | 0.91 | 0.60 | 23.4% | 21.2% | 15.7% | 23.1%/17.3% | 7.5 (interpolated) | pass | 0.085 (unverified) | 0.00 |
| 99 | `cfg_dff3` | timeframe=15min, mean_type=ema, mean_lookback=105, std_lookback=95, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 14/51/43 | 108 | 16.1% | 3.0% | 0.79 | -4.2% | 539 | 1.51 | 2.1% | 48.6 | 8/8 | 1.00 | 0.65 | 0.13 | 4 | 5.9% | 0.61 | 0.80 | 15.1% | 13.6% | 8.2% | 15.4%/11.5% | 9.4 (interpolated) | pass | 0.061 (unverified) | 0.38 |
| 100 | `cfg_1676` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=95, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 2/140/0 | 142 | 17.9% | 3.3% | 0.81 | -6.0% | 628 | 1.50 | 3.9% | 64.0 | 9/9 | 1.00 | 0.69 | 0.13 | 4 | 5.8% | 0.68 | 0.69 | 16.2% | 14.5% | 3.1% | 16.0%/11.3% | 7.7 (interpolated) | pass | 0.068 (unverified) | 0.04 |
| 101 | `cfg_4dd1` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=85, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 1/169/0 | 170 | 20.7% | 3.8% | 0.89 | -4.8% | 477 | 1.53 | 4.7% | 76.8 | 9/9 | 1.00 | 0.74 | 0.15 | 4 | 7.5% | 0.63 | 0.64 | 18.7% | 16.8% | 5.6% | 19.1%/14.9% | 7.5 (interpolated) | pass | 0.090 (unverified) | -0.45 |
| 102 | `cfg_9ee2` | timeframe=15min, mean_type=ema, mean_lookback=105, std_lookback=95, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 2/63/43 | 108 | 15.7% | 3.0% | 0.76 | -4.2% | 539 | 1.50 | 2.2% | 48.6 | 9/9 | 1.00 | 0.74 | 0.01 | 4 | 6.3% | 0.58 | 0.86 | 14.1% | 13.2% | 9.0% | 15.0%/10.8% | 9.1 (interpolated) | pass | 0.051 (unverified) | 0.35 |
| 103 | `cfg_082c` | timeframe=15min, mean_type=ema, mean_lookback=55, std_lookback=55, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 32/74/0 | 106 | 17.7% | 3.3% | 0.86 | -4.1% | 345 | 1.66 | 2.7% | 48.1 | 8/8 | 0.88 | 0.56 | 0.30 | 5 | 8.6% | 0.51 | 0.62 | 16.6% | 15.6% | 4.8% | 16.7%/12.3% | 10.3 (interpolated) | pass | 0.076 (unverified) | -0.52 |
| 104 | `cfg_e6e5` | timeframe=15min, mean_type=sma, mean_lookback=115, std_lookback=105, entry_z=-3.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 1/92/52 | 145 | 16.9% | 3.2% | 0.78 | -4.2% | 441 | 1.40 | 3.1% | 65.5 | 6/6 | 1.00 | 0.70 | 0.08 | 4 | 9.1% | 0.45 | 0.83 | 15.6% | 14.1% | 9.3% | 14.5%/8.7% | 7.5 (interpolated) | pass | 0.061 (unverified) | -0.18 |
| 105 | `cfg_65fa` | timeframe=15min, mean_type=sma, mean_lookback=115, std_lookback=105, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 7/86/52 | 145 | 16.7% | 3.1% | 0.80 | -4.1% | 441 | 1.40 | 3.1% | 65.4 | 6/6 | 1.00 | 0.72 | 0.09 | 4 | 8.1% | 0.51 | 0.77 | 15.1% | 13.5% | 8.4% | 14.4%/9.9% | 7.3 (interpolated) | pass | 0.072 (unverified) | -0.19 |
| 106 | `cfg_1186` | timeframe=15min, mean_type=sma, mean_lookback=95, std_lookback=95, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 5/98/40 | 143 | 17.1% | 3.2% | 0.89 | -3.2% | 192 | 1.49 | 2.2% | 64.4 | 9/9 | 1.00 | 0.74 | 0.14 | 4 | 9.4% | 0.42 | 0.60 | 15.7% | 14.4% | 4.5% | 15.7%/12.2% | 7.5 (interpolated) | pass | 0.097 (unverified) | -0.07 |
| 107 | `cfg_3d6d` | timeframe=15min, mean_type=ema, mean_lookback=95, std_lookback=95, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 30/114/0 | 144 | 22.8% | 4.2% | 0.84 | -4.2% | 325 | 1.58 | 3.8% | 64.8 | 9/9 | 1.00 | 0.62 | 0.23 | 5 | 11.7% | 0.48 | 0.68 | 21.8% | 20.2% | 13.6% | 20.9%/16.3% | 9.3 (interpolated) | pass | 0.066 (unverified) | -0.03 |
| 108 | `cfg_511d` | timeframe=15min, mean_type=sma, mean_lookback=95, std_lookback=95, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 5/101/0 | 106 | 17.8% | 3.3% | 0.94 | -3.6% | 186 | 1.69 | 1.9% | 48.0 | 9/9 | 1.00 | 0.77 | 0.17 | 4 | 10.1% | 0.43 | 0.61 | 16.8% | 15.4% | 8.8% | 16.7%/13.8% | 10.0 (interpolated) | pass | 0.112 (unverified) | -0.18 |
| 109 | `cfg_487b` | timeframe=15min, mean_type=ema, mean_lookback=75, std_lookback=105, entry_z=-2.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 74/155/0 | 229 | 33.7% | 6.0% | 1.04 | -6.9% | 309 | 1.52 | 5.6% | 102.7 | 7/7 | 1.00 | 0.69 | 0.35 | 4 | 11.2% | 0.65 | 0.54 | 31.0% | 28.2% | 21.2% | 29.9%/21.8% | 8.3 (interpolated) | pass | 0.155 (unverified) | -0.16 |
| 110 | `cfg_8a30` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=105, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 32/93/0 | 125 | 18.8% | 3.5% | 0.83 | -5.1% | 286 | 1.57 | 3.3% | 56.0 | 8/8 | 1.00 | 0.72 | 0.11 | 5 | 5.9% | 0.68 | 0.69 | 17.3% | 15.7% | 5.0% | 16.8%/13.5% | 9.2 (interpolated) | pass | 0.072 (unverified) | -0.34 |
| 111 | `cfg_3228` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=55, entry_z=-3.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 1/134/0 | 135 | 21.5% | 4.0% | 1.00 | -4.2% | 307 | 1.69 | 3.7% | 61.6 | 8/8 | 1.00 | 0.89 | 0.11 | 5 | 11.8% | 0.44 | 0.56 | 20.3% | 18.5% | 11.0% | 20.2%/16.2% | 9.8 (interpolated) | pass | 0.131 (unverified) | 0.03 |
| 112 | `cfg_c91c` | timeframe=15min, mean_type=ema, mean_lookback=65, std_lookback=95, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 11/111/0 | 122 | 16.7% | 3.1% | 0.93 | -3.9% | 186 | 1.64 | 2.2% | 54.7 | 10/10 | 1.00 | 0.68 | 0.25 | 4 | 8.1% | 0.52 | 0.62 | 15.4% | 14.6% | 4.9% | 15.6%/12.2% | 8.7 (interpolated) | pass | 0.107 (unverified) | 0.14 |
| 113 | `cfg_2616` | timeframe=15min, mean_type=sma, mean_lookback=65, std_lookback=105, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 31/110/0 | 141 | 17.7% | 3.3% | 0.75 | -5.3% | 315 | 1.46 | 3.7% | 63.2 | 8/8 | 1.00 | 0.62 | 0.14 | 4 | 3.7% | 0.77 | 0.66 | 16.2% | 15.2% | 6.0% | 17.1%/10.6% | 7.9 (interpolated) | pass | 0.057 (unverified) | -0.17 |
| 114 | `cfg_bd17` | timeframe=15min, mean_type=ema, mean_lookback=75, std_lookback=85, entry_z=-2.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 2/177/52 | 231 | 13.5% | 2.6% | 0.80 | -4.3% | 315 | 1.29 | 2.5% | 103.6 | 10/10 | 0.90 | 0.58 | 0.22 | 3 | 5.2% | 0.63 | 0.74 | 11.1% | 9.0% | 5.2% | 12.0%/7.8% | 4.3 (interpolated) | pass | 0.079 (unverified) | 0.10 |
| 115 | `cfg_d3ea` | timeframe=15min, mean_type=ema, mean_lookback=55, std_lookback=55, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 5/100/0 | 105 | 15.7% | 3.0% | 0.75 | -4.6% | 345 | 1.58 | 2.9% | 47.4 | 9/9 | 0.89 | 0.43 | 0.33 | 5 | 8.0% | 0.49 | 0.82 | 14.7% | 13.6% | 2.6% | 13.8%/10.3% | 9.3 (interpolated) | pass | 0.044 (unverified) | -0.45 |
| 116 | `cfg_a318` | timeframe=15min, mean_type=ema, mean_lookback=75, std_lookback=85, entry_z=-2.5, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 6/173/52 | 231 | 13.0% | 2.5% | 0.78 | -4.3% | 315 | 1.28 | 2.5% | 103.6 | 9/9 | 0.89 | 0.57 | 0.20 | 3 | 4.4% | 0.68 | 0.72 | 11.0% | 8.8% | 5.2% | 11.1%/6.9% | 4.2 (interpolated) | pass | 0.069 (unverified) | 0.06 |
| 117 | `cfg_1881` | timeframe=15min, mean_type=ema, mean_lookback=65, std_lookback=95, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=none | 1/121/0 | 122 | 17.1% | 3.2% | 0.94 | -3.9% | 186 | 1.65 | 2.2% | 54.8 | 11/11 | 1.00 | 0.69 | 0.25 | 4 | 8.9% | 0.48 | 0.65 | 15.6% | 14.7% | 4.7% | 15.6%/12.2% | 8.7 (interpolated) | pass | 0.116 (unverified) | 0.17 |
| 118 | `cfg_e394` | timeframe=15min, mean_type=sma, mean_lookback=105, std_lookback=85, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 1/150/44 | 195 | 13.4% | 2.6% | 0.77 | -4.6% | 315 | 1.32 | 2.1% | 87.9 | 9/9 | 0.78 | 0.49 | 0.28 | 3 | 2.6% | 0.79 | 0.68 | 12.0% | 9.9% | 5.7% | 11.8%/7.4% | 5.0 (interpolated) | pass | 0.065 (unverified) | 0.33 |
| 119 | `cfg_2655` | timeframe=15min, mean_type=ema, mean_lookback=95, std_lookback=95, entry_z=-2.5, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 2/142/0 | 144 | 22.4% | 4.1% | 0.82 | -4.6% | 325 | 1.58 | 4.0% | 64.9 | 9/9 | 1.00 | 0.59 | 0.23 | 4 | 11.2% | 0.48 | 0.68 | 21.1% | 18.9% | 14.1% | 22.5%/16.2% | 9.2 (interpolated) | pass | 0.061 (unverified) | -0.16 |
| 120 | `cfg_10a4` | timeframe=15min, mean_type=ema, mean_lookback=115, std_lookback=85, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 1/117/0 | 118 | 15.3% | 2.9% | 0.84 | -3.6% | 308 | 1.57 | 1.4% | 52.9 | 8/8 | 1.00 | 0.73 | 0.11 | 3 | 7.3% | 0.50 | 0.72 | 14.1% | 12.9% | 13.1% | 14.3%/10.7% | 7.9 (interpolated) | pass | 0.079 (unverified) | 0.36 |
| 121 | `cfg_a2cc` | timeframe=15min, mean_type=sma, mean_lookback=105, std_lookback=85, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 3/148/44 | 195 | 13.3% | 2.5% | 0.77 | -4.6% | 315 | 1.32 | 2.1% | 87.9 | 8/8 | 0.75 | 0.45 | 0.32 | 3 | 2.4% | 0.80 | 0.69 | 11.8% | 9.8% | 5.8% | 11.7%/7.6% | 4.9 (interpolated) | pass | 0.063 (unverified) | 0.33 |
| 122 | `cfg_7ca1` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=105, entry_z=-2.5, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 0/139/38 | 177 | 12.5% | 2.4% | 0.77 | -2.8% | 315 | 1.36 | 1.9% | 79.7 | 8/8 | 1.00 | 0.66 | 0.12 | 3 | 3.3% | 0.71 | 0.72 | 10.6% | 8.9% | 3.7% | 10.9%/7.6% | 5.0 (interpolated) | pass | 0.060 (unverified) | -0.20 |
| 123 | `cfg_9210` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=105, entry_z=-2.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 0/139/38 | 177 | 12.5% | 2.4% | 0.77 | -2.8% | 315 | 1.36 | 1.9% | 79.7 | 9/9 | 1.00 | 0.77 | 0.00 | 3 | 3.3% | 0.71 | 0.72 | 10.6% | 8.9% | 3.7% | 10.4%/7.7% | 5.0 (interpolated) | pass | 0.060 (unverified) | -0.20 |
| 124 | `cfg_88c4` | timeframe=15min, mean_type=ema, mean_lookback=115, std_lookback=85, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 4/114/0 | 118 | 15.4% | 2.9% | 0.84 | -3.6% | 308 | 1.57 | 1.4% | 52.9 | 7/7 | 0.86 | 0.73 | 0.11 | 3 | 7.4% | 0.49 | 0.72 | 14.2% | 13.0% | 13.9% | 14.1%/10.8% | 7.9 (interpolated) | pass | 0.080 (unverified) | 0.36 |
| 125 | `cfg_b22d` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=85, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 17/203/0 | 220 | 26.1% | 4.7% | 0.94 | -8.3% | 450 | 1.46 | 5.9% | 98.4 | 9/9 | 1.00 | 0.73 | 0.21 | 4 | 10.0% | 0.59 | 0.55 | 24.0% | 21.9% | 10.1% | 23.4%/17.7% | 7.3 (interpolated) | pass | 0.110 (unverified) | -0.71 |
| 126 | `cfg_e523` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=85, entry_z=-2.0, exit_z=1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 5/215/0 | 220 | 25.5% | 4.6% | 0.92 | -8.2% | 445 | 1.45 | 6.0% | 98.4 | 8/8 | 1.00 | 0.63 | 0.29 | 4 | 10.1% | 0.58 | 0.57 | 23.3% | 21.3% | 10.5% | 22.5%/17.1% | 7.1 (interpolated) | pass | 0.102 (unverified) | -0.72 |
| 127 | `cfg_1836` | timeframe=15min, mean_type=sma, mean_lookback=85, std_lookback=105, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 13/156/82 | 251 | 18.4% | 3.4% | 0.78 | -5.1% | 156 | 1.28 | 3.7% | 112.8 | 9/9 | 1.00 | 0.54 | 0.24 | 3 | 7.1% | 0.62 | 0.67 | 15.5% | 13.7% | 22.1% | 14.7%/8.8% | 4.9 (interpolated) | pass | 0.066 (unverified) | -0.14 |
| 128 | `cfg_5092` | timeframe=15min, mean_type=ema, mean_lookback=115, std_lookback=105, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 1/155/79 | 235 | 22.9% | 4.2% | 0.88 | -5.6% | 325 | 1.36 | 3.5% | 105.3 | 9/9 | 1.00 | 0.64 | 0.24 | 3 | 9.0% | 0.60 | 0.67 | 20.4% | 18.0% | 5.5% | 19.8%/13.4% | 6.0 (interpolated) | pass | 0.083 (unverified) | 0.16 |
| 129 | `cfg_c352` | timeframe=15min, mean_type=ema, mean_lookback=115, std_lookback=105, entry_z=-2.5, exit_z=1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 0/156/79 | 235 | 22.9% | 4.2% | 0.88 | -5.6% | 325 | 1.36 | 3.5% | 105.3 | 8/8 | 1.00 | 0.62 | 0.26 | 3 | 9.0% | 0.60 | 0.67 | 20.4% | 18.0% | 5.6% | 18.9%/13.1% | 6.0 (interpolated) | pass | 0.083 (unverified) | 0.15 |
| 130 | `cfg_6adf` | timeframe=15min, mean_type=ema, mean_lookback=55, std_lookback=95, entry_z=-2.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 78/123/0 | 201 | 20.4% | 3.8% | 0.75 | -7.4% | 347 | 1.38 | 4.9% | 89.9 | 8/8 | 1.00 | 0.66 | 0.09 | 3 | 7.4% | 0.63 | 0.70 | 17.4% | 15.5% | 10.6% | 16.8%/13.3% | 6.5 (interpolated) | pass | 0.054 (unverified) | -0.84 |
| 131 | `cfg_e32b` | timeframe=15min, mean_type=ema, mean_lookback=85, std_lookback=85, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 5/65/32 | 102 | 12.7% | 2.4% | 0.76 | -3.7% | 377 | 1.48 | 1.5% | 46.3 | 9/9 | 1.00 | 0.71 | 0.05 | 3 | 5.2% | 0.57 | 0.78 | 11.7% | 10.8% | -2.5% | 12.5%/8.0% | 8.1 (interpolated) | pass | 0.050 (unverified) | 0.78 |
| 132 | `cfg_7956` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=65, entry_z=-2.5, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 3/195/55 | 253 | 13.8% | 2.6% | 0.84 | -3.8% | 325 | 1.30 | 2.8% | 114.2 | 9/9 | 0.89 | 0.73 | 0.11 | 3 | 4.5% | 0.64 | 0.67 | 11.7% | 9.3% | 0.1% | 10.6%/6.7% | 4.1 (interpolated) | pass | 0.070 (unverified) | -0.54 |
| 133 | `cfg_bb8f` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=65, entry_z=-2.5, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=1.5 | 0/198/55 | 253 | 13.8% | 2.6% | 0.84 | -3.8% | 325 | 1.30 | 2.8% | 114.2 | 8/8 | 0.88 | 0.62 | 0.22 | 3 | 4.6% | 0.64 | 0.66 | 11.7% | 9.4% | 0.2% | 10.9%/7.5% | 4.2 (interpolated) | pass | 0.071 (unverified) | -0.54 |
| 134 | `cfg_d2b8` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 101/482/0 | 583 | 45.0% | 7.7% | 0.78 | -22.3% | 570 | 1.26 | 15.1% | 262.0 | 8/8 | 1.00 | 0.54 | 0.24 | 4 | 11.7% | 0.60 | 0.57 | 38.1% | 30.9% | 55.1% | 40.2%/29.5% | 4.9 (interpolated) | pass | 0.059 (unverified) | -0.17 |
| 135 | `cfg_8aeb` | timeframe=15min, mean_type=ema, mean_lookback=45, std_lookback=95, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 13/171/0 | 184 | 21.3% | 3.9% | 0.83 | -7.8% | 469 | 1.44 | 5.0% | 82.1 | 9/9 | 1.00 | 0.67 | 0.16 | 3 | 6.3% | 0.66 | 0.65 | 19.1% | 17.8% | 8.5% | 17.7%/11.9% | 7.2 (interpolated) | pass | 0.072 (unverified) | -0.81 |
| 136 | `cfg_05da` | timeframe=15min, mean_type=sma, mean_lookback=75, std_lookback=85, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 10/191/89 | 290 | 17.7% | 3.3% | 0.81 | -3.4% | 237 | 1.25 | 4.4% | 130.5 | 10/10 | 0.80 | 0.59 | 0.21 | 3 | 7.6% | 0.58 | 0.63 | 14.7% | 12.3% | 6.6% | 14.5%/9.7% | 4.4 (interpolated) | pass | 0.070 (unverified) | -0.05 |
| 137 | `cfg_64d2` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=105, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=1.5 | 37/81/71 | 189 | 17.9% | 3.4% | 0.75 | -6.1% | 365 | 1.32 | 3.8% | 85.2 | 8/8 | 0.88 | 0.55 | 0.20 | 5 | 3.0% | 0.82 | 0.81 | 15.8% | 14.5% | 6.5% | 15.1%/10.2% | 6.1 (interpolated) | pass | 0.056 (unverified) | -0.25 |
| 138 | `cfg_d7c9` | timeframe=15min, mean_type=sma, mean_lookback=95, std_lookback=95, entry_z=-3.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 3/106/0 | 109 | 10.6% | 2.0% | 0.77 | -3.8% | 303 | 1.48 | 1.3% | 48.9 | 8/8 | 1.00 | 0.75 | 0.02 | 3 | 3.5% | 0.65 | 0.66 | 9.5% | 8.4% | 5.6% | 9.6%/6.7% | 6.3 (interpolated) | pass | 0.063 (unverified) | -0.62 |
| 139 | `cfg_225b` | timeframe=15min, mean_type=sma, mean_lookback=95, std_lookback=95, entry_z=-3.0, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 0/109/0 | 109 | 10.5% | 2.0% | 0.77 | -3.8% | 303 | 1.48 | 1.3% | 48.9 | 8/8 | 1.00 | 0.75 | 0.01 | 3 | 3.5% | 0.65 | 0.66 | 9.4% | 8.3% | 5.2% | 8.9%/6.0% | 6.2 (interpolated) | pass | 0.062 (unverified) | -0.62 |
| 140 | `cfg_04d4` | timeframe=15min, mean_type=sma, mean_lookback=45, std_lookback=15, entry_z=-3.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 185/406/0 | 591 | 45.9% | 7.9% | 0.82 | -19.2% | 592 | 1.26 | 14.4% | 266.1 | 7/7 | 1.00 | 0.55 | 0.27 | 4 | 14.5% | 0.55 | 0.54 | 39.5% | 30.4% | 51.5% | 38.8%/27.9% | 4.8 (interpolated) | pass | 0.069 (unverified) | -0.06 |
| 141 | `cfg_f97f` | timeframe=15min, mean_type=ema, mean_lookback=115, std_lookback=105, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 19/164/0 | 183 | 26.6% | 4.8% | 0.97 | -5.2% | 219 | 1.61 | 3.3% | 82.8 | 7/7 | 1.00 | 0.59 | 0.37 | 5 | 16.4% | 0.38 | 0.72 | 24.3% | 22.4% | 20.3% | 22.5%/15.2% | 8.4 (interpolated) | pass | 0.127 (unverified) | 0.07 |
| 142 | `cfg_204b` | timeframe=15min, mean_type=ema, mean_lookback=65, std_lookback=105, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 9/190/0 | 199 | 21.0% | 3.9% | 0.76 | -8.2% | 325 | 1.37 | 5.4% | 89.4 | 8/8 | 1.00 | 0.69 | 0.07 | 3 | -0.9% | 1.09 | 0.67 | 18.8% | 16.7% | 6.5% | 18.3%/13.5% | 6.7 (interpolated) | pass | 0.054 (unverified) | -0.16 |
| 143 | `cfg_6bcb` | timeframe=15min, mean_type=ema, mean_lookback=35, std_lookback=15, entry_z=-3.0, exit_z=0.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 28/454/0 | 482 | 26.9% | 4.9% | 0.77 | -8.1% | 462 | 1.26 | 5.8% | 219.5 | 7/7 | 0.86 | 0.70 | 0.07 | 4 | 4.7% | 0.83 | 0.89 | 22.5% | 17.1% | -0.4% | 24.8%/17.7% | 3.9 (interpolated) | pass | 0.041 (unverified) | -0.52 |
| 144 | `cfg_5e66` | timeframe=15min, mean_type=sma, mean_lookback=105, std_lookback=95, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 26/192/0 | 218 | 29.3% | 5.3% | 0.94 | -8.6% | 203 | 1.50 | 5.8% | 97.0 | 9/9 | 0.89 | 0.66 | 0.28 | 3 | 4.5% | 0.87 | 0.49 | 26.8% | 24.3% | 24.6% | 25.3%/21.4% | 7.9 (interpolated) | pass | 0.136 (unverified) | 0.01 |
| 145 | `cfg_5c24` | timeframe=15min, mean_type=sma, mean_lookback=75, std_lookback=85, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 1/200/90 | 291 | 17.1% | 3.2% | 0.79 | -3.3% | 203 | 1.24 | 4.4% | 131.1 | 11/11 | 0.82 | 0.52 | 0.27 | 3 | 6.9% | 0.61 | 0.66 | 14.3% | 12.0% | 5.0% | 12.9%/7.9% | 4.3 (interpolated) | pass | 0.064 (unverified) | -0.01 |
| 146 | `cfg_ff27` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=85, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 15/243/0 | 258 | 22.3% | 4.1% | 0.77 | -6.5% | 555 | 1.32 | 7.0% | 116.4 | 8/8 | 1.00 | 0.64 | 0.14 | 3 | 2.7% | 0.89 | 0.61 | 18.9% | 16.3% | 0.2% | 18.3%/12.7% | 5.6 (interpolated) | pass | 0.066 (unverified) | -0.52 |
| 147 | `cfg_ba25` | timeframe=15min, mean_type=ema, mean_lookback=75, std_lookback=105, entry_z=-2.0, exit_z=0.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 11/214/0 | 225 | 29.2% | 5.3% | 0.92 | -7.8% | 325 | 1.46 | 6.1% | 101.1 | 8/8 | 1.00 | 0.72 | 0.20 | 4 | 6.5% | 0.76 | 0.54 | 26.9% | 24.6% | 12.9% | 25.5%/19.2% | 7.9 (interpolated) | pass | 0.105 (unverified) | -0.28 |
| 148 | `cfg_1f78` | timeframe=15min, mean_type=ema, mean_lookback=35, std_lookback=15, entry_z=-3.0, exit_z=1.0, max_holding_bars=3, entry_confirmation=none, stop_atr_multiple=none | 15/466/0 | 481 | 27.4% | 5.0% | 0.78 | -8.2% | 462 | 1.26 | 5.8% | 219.1 | 6/6 | 1.00 | 0.60 | 0.18 | 4 | 5.1% | 0.82 | 0.87 | 23.1% | 18.0% | -3.0% | 25.2%/15.9% | 4.0 (interpolated) | pass | 0.043 (unverified) | -0.51 |
| 149 | `cfg_fe4d` | timeframe=15min, mean_type=sma, mean_lookback=105, std_lookback=95, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.5 | 15/202/104 | 321 | 20.9% | 3.9% | 0.80 | -5.5% | 185 | 1.25 | 4.8% | 144.6 | 10/10 | 0.90 | 0.58 | 0.22 | 3 | 4.0% | 0.84 | 0.60 | 18.0% | 14.0% | 9.8% | 15.0%/8.9% | 4.4 (interpolated) | pass | 0.073 (unverified) | -0.32 |
| 150 | `cfg_5bee` | timeframe=15min, mean_type=sma, mean_lookback=55, std_lookback=75, entry_z=-2.5, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 50/156/0 | 206 | 19.2% | 3.6% | 0.80 | -8.2% | 467 | 1.36 | 5.4% | 92.6 | 9/9 | 0.89 | 0.53 | 0.26 | 4 | 4.2% | 0.76 | 0.60 | 17.6% | 15.7% | 13.9% | 17.4%/12.5% | 6.2 (interpolated) | pass | 0.074 (unverified) | -0.34 |
| 151 | `cfg_0877` | timeframe=15min, mean_type=sma, mean_lookback=35, std_lookback=85, entry_z=-2.0, exit_z=-1.0, max_holding_bars=8, entry_confirmation=none, stop_atr_multiple=none | 116/145/0 | 261 | 24.1% | 4.4% | 0.85 | -5.8% | 341 | 1.35 | 6.2% | 118.0 | 7/7 | 1.00 | 0.64 | 0.21 | 3 | 5.1% | 0.79 | 0.52 | 20.8% | 17.3% | 6.0% | 20.6%/15.2% | 5.8 (interpolated) | pass | 0.099 (unverified) | -0.28 |
| 152 | `cfg_cc63` | timeframe=15min, mean_type=sma, mean_lookback=95, std_lookback=85, entry_z=-2.0, exit_z=-1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 14/246/55 | 315 | 20.5% | 3.8% | 0.91 | -6.3% | 573 | 1.36 | 3.5% | 142.1 | 8/8 | 0.75 | 0.32 | 0.59 | 4 | 8.1% | 0.54 | 0.57 | 17.4% | 13.6% | 17.6% | 16.6%/11.7% | 4.6 (interpolated) | pass | 0.097 (unverified) | 0.12 |
| 153 | `cfg_8584` | timeframe=15min, mean_type=sma, mean_lookback=95, std_lookback=85, entry_z=-2.0, exit_z=1.0, max_holding_bars=3, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 1/259/55 | 315 | 20.3% | 3.8% | 0.90 | -6.3% | 573 | 1.35 | 3.6% | 142.2 | 8/8 | 0.75 | 0.31 | 0.60 | 4 | 7.9% | 0.55 | 0.58 | 17.1% | 13.3% | 16.0% | 18.4%/12.8% | 4.5 (interpolated) | pass | 0.094 (unverified) | 0.16 |
| 154 | `cfg_54c0` | timeframe=15min, mean_type=sma, mean_lookback=95, std_lookback=85, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 31/216/94 | 341 | 24.9% | 4.6% | 0.90 | -7.5% | 641 | 1.31 | 5.3% | 153.7 | 9/9 | 0.89 | 0.41 | 0.48 | 4 | 9.5% | 0.56 | 0.53 | 21.0% | 18.2% | 20.6% | 21.0%/15.7% | 4.8 (interpolated) | pass | 0.101 (unverified) | 0.30 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 0.7% / 0.28 / 26 | 0.8% / 0.54 / 25 | 8.5% / 2.05 / 35 | 8.3% / 2.52 / 47 | -0.2% / -0.05 / 30 |
| 2 | 0.7% / 0.28 / 26 | 0.8% / 0.54 / 25 | 8.5% / 2.05 / 35 | 8.3% / 2.52 / 47 | -0.2% / -0.05 / 30 |
| 3 | 2.8% / 1.31 / 18 | -1.5% / -0.90 / 19 | 4.4% / 1.85 / 26 | 6.0% / 2.06 / 33 | -0.1% / -0.04 / 19 |
| 4 | 2.8% / 1.31 / 18 | -1.5% / -0.90 / 19 | 4.4% / 1.85 / 26 | 5.9% / 2.05 / 33 | -0.1% / -0.04 / 19 |
| 5 | 3.2% / 0.94 / 24 | 0.7% / 0.33 / 23 | 12.1% / 1.89 / 31 | 11.4% / 2.22 / 41 | -2.1% / -0.42 / 24 |
| 6 | 7.7% / 1.98 / 32 | -0.5% / -0.36 / 14 | 4.9% / 1.82 / 21 | 7.8% / 2.01 / 27 | -4.1% / -1.44 / 14 |
| 7 | 7.7% / 1.98 / 32 | -0.5% / -0.36 / 14 | 4.9% / 1.82 / 21 | 7.8% / 2.01 / 27 | -4.1% / -1.44 / 14 |
| 8 | 0.9% / 0.48 / 20 | 3.8% / 2.38 / 22 | 8.6% / 1.35 / 27 | 6.2% / 1.52 / 36 | -1.4% / -0.38 / 25 |
| 9 | 3.1% / 1.08 / 29 | -2.5% / -1.57 / 29 | 8.8% / 2.19 / 31 | 7.3% / 1.99 / 38 | -1.2% / -0.38 / 21 |
| 10 | 3.1% / 1.08 / 29 | -2.5% / -1.57 / 29 | 8.8% / 2.19 / 31 | 7.3% / 1.99 / 38 | -1.2% / -0.38 / 21 |
| 11 | 7.6% / 1.96 / 45 | 0.0% / 0.03 / 33 | 9.2% / 1.70 / 44 | 8.5% / 1.59 / 47 | -2.3% / -0.47 / 27 |
| 12 | 3.1% / 1.39 / 24 | -1.0% / -0.68 / 19 | 5.8% / 1.94 / 31 | 8.3% / 2.30 / 41 | -3.1% / -1.15 / 27 |
| 13 | 0.5% / 0.15 / 79 | -0.3% / -0.17 / 49 | 12.6% / 2.51 / 68 | 6.5% / 1.52 / 80 | 2.3% / 0.70 / 41 |
| 14 | 7.2% / 1.92 / 45 | 0.1% / 0.07 / 33 | 9.3% / 1.70 / 44 | 8.5% / 1.58 / 47 | -2.4% / -0.51 / 27 |
| 15 | 4.7% / 1.73 / 37 | -0.9% / -0.42 / 33 | 6.3% / 2.43 / 32 | 7.3% / 1.79 / 50 | -1.4% / -0.46 / 22 |
| 16 | 3.1% / 1.39 / 24 | -1.0% / -0.68 / 19 | 5.8% / 1.94 / 31 | 8.3% / 2.29 / 41 | -3.1% / -1.15 / 27 |
| 17 | 2.6% / 0.97 / 23 | 2.4% / 1.14 / 17 | 4.1% / 1.13 / 21 | 10.6% / 2.31 / 34 | 0.2% / 0.07 / 11 |
| 18 | 4.7% / 1.73 / 37 | -0.9% / -0.42 / 33 | 6.3% / 2.43 / 32 | 7.3% / 1.79 / 50 | -1.4% / -0.46 / 22 |
| 19 | 0.2% / 0.09 / 79 | -0.3% / -0.17 / 49 | 12.6% / 2.54 / 68 | 6.6% / 1.53 / 80 | 2.4% / 0.72 / 41 |
| 20 | -1.3% / -0.73 / 20 | -0.2% / -0.14 / 26 | 5.1% / 1.74 / 36 | 6.8% / 2.19 / 46 | 1.8% / 0.56 / 28 |
| 21 | -0.6% / -0.43 / 16 | 0.3% / 0.25 / 23 | 3.8% / 1.23 / 28 | 5.5% / 1.77 / 37 | 2.9% / 0.99 / 23 |
| 22 | 0.7% / 0.36 / 20 | 4.7% / 2.77 / 21 | 8.6% / 1.35 / 27 | 5.6% / 1.40 / 36 | -1.8% / -0.52 / 25 |
| 23 | 3.8% / 1.41 / 57 | -1.2% / -0.70 / 47 | 10.9% / 2.46 / 55 | 5.5% / 1.42 / 68 | 4.8% / 1.39 / 35 |
| 24 | 5.0% / 1.61 / 25 | -1.3% / -0.86 / 19 | 7.4% / 2.67 / 22 | 5.9% / 1.71 / 36 | -1.9% / -0.71 / 12 |
| 25 | 2.5% / 0.93 / 23 | 2.3% / 1.10 / 17 | 4.1% / 1.12 / 21 | 9.7% / 2.25 / 34 | 0.8% / 0.19 / 11 |
| 26 | 3.9% / 1.53 / 24 | 1.2% / 0.67 / 19 | 6.4% / 1.68 / 21 | 6.4% / 1.46 / 35 | -1.3% / -0.32 / 12 |
| 27 | -1.6% / -0.64 / 45 | 0.9% / 0.48 / 29 | 8.6% / 1.92 / 49 | 10.9% / 2.28 / 51 | -1.6% / -0.37 / 28 |
| 28 | 2.8% / 1.41 / 23 | 0.2% / 0.10 / 22 | 5.0% / 1.87 / 27 | 7.6% / 2.06 / 35 | -1.8% / -0.58 / 14 |
| 29 | 2.8% / 1.41 / 23 | 0.2% / 0.10 / 22 | 5.0% / 1.87 / 27 | 7.5% / 2.05 / 35 | -1.8% / -0.58 / 14 |
| 30 | -0.1% / -0.04 / 36 | 1.0% / 0.44 / 27 | 10.7% / 1.63 / 38 | 9.2% / 1.98 / 41 | 1.4% / 0.33 / 26 |
| 31 | 0.0% / 0.02 / 36 | 1.0% / 0.45 / 27 | 10.7% / 1.62 / 38 | 9.1% / 1.98 / 41 | 1.4% / 0.35 / 26 |
| 32 | -2.2% / -0.90 / 45 | 2.6% / 1.59 / 26 | 8.8% / 1.96 / 49 | 10.2% / 2.20 / 51 | -1.7% / -0.39 / 28 |
| 33 | 5.0% / 1.95 / 29 | -0.1% / -0.05 / 17 | 7.2% / 1.86 / 23 | 3.0% / 0.83 / 26 | 0.4% / 0.12 / 11 |
| 34 | 4.0% / 1.43 / 57 | -1.2% / -0.69 / 47 | 10.8% / 2.46 / 55 | 5.5% / 1.43 / 68 | 4.9% / 1.36 / 35 |
| 35 | 4.8% / 1.87 / 27 | -1.3% / -0.88 / 13 | 5.6% / 1.91 / 21 | 6.7% / 1.75 / 27 | -0.3% / -0.07 / 17 |
| 36 | 5.6% / 1.95 / 27 | -1.3% / -0.87 / 13 | 5.6% / 1.92 / 21 | 6.7% / 1.75 / 27 | -0.3% / -0.06 / 17 |
| 37 | 4.6% / 1.85 / 29 | -0.1% / -0.05 / 17 | 7.1% / 1.84 / 23 | 2.5% / 0.71 / 26 | 0.4% / 0.14 / 11 |
| 38 | 1.2% / 0.41 / 33 | 0.9% / 0.36 / 30 | 7.3% / 1.74 / 38 | 9.5% / 1.83 / 42 | 0.8% / 0.21 / 18 |
| 39 | 2.1% / 0.80 / 78 | 1.5% / 0.81 / 46 | 9.5% / 2.24 / 67 | 5.3% / 1.45 / 78 | -0.4% / -0.09 / 46 |
| 40 | 3.6% / 1.75 / 25 | -0.1% / -0.06 / 19 | 5.5% / 2.23 / 22 | 8.2% / 2.11 / 33 | -3.0% / -1.01 / 18 |
| 41 | 2.8% / 0.94 / 60 | -2.1% / -1.16 / 41 | 10.8% / 2.56 / 54 | 6.6% / 1.60 / 65 | 0.2% / 0.07 / 30 |
| 42 | 3.6% / 1.75 / 25 | -0.1% / -0.06 / 19 | 5.5% / 2.23 / 22 | 8.1% / 2.10 / 33 | -3.0% / -1.01 / 18 |
| 43 | 2.4% / 1.12 / 22 | 0.7% / 0.51 / 15 | 8.2% / 1.79 / 25 | 9.9% / 2.27 / 30 | -3.5% / -0.98 / 19 |
| 44 | 2.8% / 0.94 / 60 | -2.1% / -1.16 / 41 | 10.8% / 2.56 / 54 | 6.6% / 1.60 / 65 | 0.2% / 0.07 / 30 |
| 45 | 0.8% / 0.30 / 33 | 0.7% / 0.31 / 30 | 7.2% / 1.71 / 38 | 10.2% / 1.84 / 42 | 0.8% / 0.20 / 18 |
| 46 | 0.2% / 0.08 / 37 | 0.7% / 0.36 / 29 | 8.8% / 1.38 / 36 | 13.2% / 2.44 / 44 | 1.4% / 0.29 / 26 |
| 47 | 0.2% / 0.14 / 32 | 2.0% / 1.09 / 20 | 6.3% / 1.66 / 36 | 7.4% / 1.66 / 40 | -1.5% / -0.38 / 20 |
| 48 | 2.0% / 0.99 / 22 | 0.7% / 0.49 / 15 | 8.2% / 1.79 / 25 | 9.6% / 2.24 / 30 | -3.4% / -0.96 / 19 |
| 49 | -0.6% / -0.17 / 39 | 0.5% / 0.21 / 33 | 9.8% / 1.51 / 46 | 6.5% / 1.20 / 51 | 4.7% / 1.07 / 25 |
| 50 | 0.2% / 0.14 / 32 | 2.0% / 1.09 / 20 | 6.3% / 1.66 / 36 | 7.4% / 1.66 / 40 | -1.5% / -0.38 / 20 |
| 51 | -0.2% / -0.05 / 39 | 0.5% / 0.23 / 33 | 10.0% / 1.54 / 46 | 5.9% / 1.15 / 51 | 4.7% / 1.07 / 25 |
| 52 | 2.7% / 0.95 / 78 | 1.6% / 0.85 / 46 | 9.4% / 2.20 / 67 | 5.4% / 1.47 / 78 | -0.4% / -0.09 / 46 |
| 53 | 3.6% / 0.96 / 24 | -0.7% / -0.29 / 22 | 11.4% / 1.80 / 31 | 10.4% / 2.06 / 41 | -2.5% / -0.52 / 24 |
| 54 | 2.7% / 0.97 / 28 | 0.2% / 0.08 / 27 | 8.1% / 1.29 / 30 | 11.8% / 2.32 / 36 | -0.9% / -0.19 / 20 |
| 55 | 1.3% / 0.48 / 35 | 0.8% / 0.40 / 29 | 6.5% / 1.68 / 44 | 9.6% / 1.97 / 48 | 0.7% / 0.18 / 23 |
| 56 | 3.5% / 0.88 / 39 | 0.7% / 0.28 / 19 | 9.4% / 1.82 / 27 | 8.3% / 1.80 / 29 | -0.4% / -0.06 / 15 |
| 57 | -0.7% / -0.27 / 33 | 0.8% / 0.38 / 22 | 7.3% / 1.90 / 23 | 8.4% / 1.90 / 48 | -0.4% / -0.08 / 19 |
| 58 | 2.4% / 1.12 / 19 | 4.9% / 1.83 / 23 | 6.6% / 1.40 / 29 | 9.8% / 2.00 / 41 | -0.0% / 0.02 / 25 |
| 59 | 2.0% / 0.76 / 29 | 0.1% / 0.06 / 19 | 9.0% / 2.16 / 25 | 4.5% / 1.17 / 36 | -0.3% / -0.06 / 17 |
| 60 | 2.7% / 1.40 / 24 | -0.8% / -0.43 / 22 | 7.2% / 2.69 / 27 | 7.0% / 2.32 / 31 | -3.1% / -1.06 / 18 |
| 61 | 2.4% / 0.92 / 28 | -0.8% / -0.31 / 28 | 7.2% / 1.26 / 30 | 12.3% / 2.39 / 36 | -0.7% / -0.17 / 20 |
| 62 | 3.4% / 0.74 / 67 | 3.0% / 0.94 / 41 | 11.2% / 1.88 / 59 | 8.8% / 1.58 / 67 | -4.7% / -0.99 / 45 |
| 63 | 2.5% / 0.85 / 54 | -1.4% / -0.87 / 36 | 7.6% / 2.39 / 51 | 5.8% / 1.49 / 59 | 0.7% / 0.31 / 20 |
| 64 | 2.5% / 0.85 / 54 | -1.4% / -0.87 / 36 | 7.6% / 2.39 / 51 | 5.8% / 1.49 / 59 | 0.7% / 0.31 / 20 |
| 65 | 7.8% / 2.04 / 39 | -0.9% / -0.52 / 29 | 3.6% / 1.60 / 33 | 5.2% / 1.53 / 42 | -3.3% / -1.05 / 18 |
| 66 | 7.8% / 2.04 / 39 | -0.9% / -0.52 / 29 | 3.6% / 1.60 / 33 | 5.2% / 1.53 / 42 | -3.3% / -1.05 / 18 |
| 67 | 2.5% / 0.94 / 27 | -0.5% / -0.28 / 13 | 5.7% / 1.47 / 22 | 7.8% / 1.73 / 28 | 3.4% / 0.78 / 18 |
| 68 | 2.7% / 1.40 / 24 | -0.8% / -0.43 / 22 | 6.8% / 2.62 / 27 | 6.9% / 2.31 / 31 | -3.0% / -1.05 / 18 |
| 69 | 3.1% / 0.69 / 67 | 2.9% / 0.94 / 41 | 11.2% / 1.89 / 59 | 8.9% / 1.60 / 67 | -4.7% / -0.98 / 45 |
| 70 | 4.9% / 2.14 / 25 | -1.0% / -0.61 / 14 | 7.8% / 2.83 / 17 | 3.6% / 1.22 / 27 | -4.5% / -1.61 / 18 |
| 71 | 2.4% / 0.87 / 42 | -1.1% / -0.73 / 31 | 7.3% / 2.26 / 44 | 4.7% / 1.27 / 49 | 0.2% / 0.08 / 19 |
| 72 | 2.4% / 0.87 / 42 | -1.1% / -0.73 / 31 | 7.3% / 2.26 / 44 | 4.7% / 1.27 / 49 | 0.2% / 0.08 / 19 |
| 73 | 4.9% / 2.14 / 25 | -1.0% / -0.61 / 14 | 7.8% / 2.83 / 17 | 3.5% / 1.20 / 27 | -4.5% / -1.61 / 18 |
| 74 | 0.9% / 0.36 / 35 | 2.5% / 1.33 / 26 | 5.4% / 1.41 / 41 | 9.0% / 1.88 / 48 | 0.8% / 0.20 / 23 |
| 75 | 2.0% / 0.79 / 28 | 0.3% / 0.14 / 26 | 4.0% / 1.08 / 24 | 6.9% / 1.64 / 35 | 0.1% / 0.05 / 16 |
| 76 | 3.6% / 1.69 / 24 | 1.2% / 0.74 / 19 | 5.3% / 1.25 / 22 | 3.6% / 0.96 / 25 | 1.4% / 0.39 / 10 |
| 77 | 3.1% / 0.80 / 38 | 0.9% / 0.37 / 19 | 9.4% / 1.82 / 27 | 7.2% / 1.64 / 29 | 0.8% / 0.17 / 15 |
| 78 | 0.7% / 0.25 / 30 | 1.6% / 0.89 / 24 | 5.2% / 1.18 / 36 | 12.6% / 2.26 / 35 | 0.2% / 0.06 / 18 |
| 79 | -1.6% / -0.42 / 62 | 0.2% / 0.10 / 41 | 11.0% / 2.26 / 54 | 11.0% / 2.25 / 72 | -0.4% / -0.07 / 37 |
| 80 | -2.2% / -0.58 / 41 | 0.4% / 0.17 / 29 | 7.5% / 1.73 / 39 | 13.9% / 2.41 / 45 | -0.2% / -0.02 / 26 |
| 81 | 2.8% / 1.39 / 21 | -0.1% / -0.09 / 15 | 4.0% / 1.26 / 23 | 7.3% / 2.13 / 28 | -1.6% / -0.61 / 17 |
| 82 | 2.8% / 1.39 / 21 | -0.1% / -0.09 / 15 | 4.0% / 1.26 / 23 | 7.3% / 2.13 / 28 | -1.6% / -0.61 / 17 |
| 83 | 2.5% / 0.83 / 32 | 0.9% / 0.45 / 16 | 6.5% / 1.55 / 27 | 7.9% / 1.82 / 30 | 1.0% / 0.24 / 15 |
| 84 | 3.2% / 1.56 / 24 | 1.4% / 0.81 / 19 | 5.4% / 1.25 / 22 | 3.1% / 0.83 / 25 | 1.3% / 0.37 / 10 |
| 85 | 3.5% / 0.75 / 81 | 1.3% / 0.37 / 53 | 10.1% / 1.46 / 64 | 13.3% / 2.22 / 81 | -0.7% / -0.07 / 54 |
| 86 | 4.0% / 1.19 / 26 | -1.7% / -1.27 / 24 | 5.3% / 1.91 / 30 | 7.8% / 2.17 / 30 | -3.1% / -1.13 / 11 |
| 87 | 2.3% / 0.85 / 28 | 0.3% / 0.16 / 26 | 4.1% / 1.09 / 24 | 6.6% / 1.59 / 35 | -0.1% / -0.00 / 16 |
| 88 | 4.0% / 1.19 / 26 | -1.7% / -1.27 / 24 | 5.3% / 1.91 / 30 | 7.8% / 2.17 / 30 | -3.1% / -1.13 / 11 |
| 89 | 0.8% / 0.41 / 19 | 3.7% / 1.89 / 23 | 7.6% / 1.66 / 29 | 7.1% / 1.75 / 42 | -3.3% / -0.88 / 25 |
| 90 | 1.1% / 0.59 / 19 | 2.0% / 1.41 / 25 | 2.3% / 0.69 / 29 | 6.8% / 1.79 / 43 | -2.0% / -0.99 / 25 |
| 91 | -0.4% / -0.12 / 40 | 0.4% / 0.17 / 34 | 5.8% / 1.47 / 45 | 10.8% / 2.03 / 54 | 0.4% / 0.10 / 29 |
| 92 | 3.1% / 1.25 / 61 | -1.9% / -1.17 / 41 | 7.0% / 2.24 / 58 | 7.1% / 1.73 / 70 | -1.8% / -0.56 / 36 |
| 93 | 2.9% / 0.63 / 81 | 1.3% / 0.38 / 53 | 10.4% / 1.50 / 64 | 13.0% / 2.27 / 81 | -0.7% / -0.07 / 54 |
| 94 | 2.4% / 0.90 / 27 | -0.5% / -0.28 / 13 | 5.7% / 1.47 / 22 | 7.2% / 1.62 / 28 | 3.4% / 0.78 / 18 |
| 95 | 2.4% / 0.81 / 32 | 1.0% / 0.50 / 16 | 6.5% / 1.55 / 27 | 6.8% / 1.63 / 30 | 2.3% / 0.46 / 15 |
| 96 | -2.2% / -0.59 / 62 | 0.0% / 0.02 / 41 | 11.2% / 2.30 / 54 | 10.9% / 2.23 / 72 | -0.4% / -0.07 / 37 |
| 97 | 3.9% / 1.40 / 61 | -1.9% / -1.17 / 41 | 6.8% / 2.18 / 58 | 7.0% / 1.72 / 70 | -2.6% / -0.88 / 36 |
| 98 | 2.2% / 0.57 / 43 | -1.3% / -0.35 / 37 | 6.4% / 1.00 / 43 | 21.6% / 3.08 / 51 | -3.9% / -0.68 / 29 |
| 99 | 2.5% / 0.74 / 27 | -1.0% / -0.42 / 13 | 1.2% / 0.43 / 21 | 9.6% / 1.82 / 28 | 3.1% / 0.65 / 19 |
| 100 | 0.3% / 0.11 / 30 | 0.7% / 0.32 / 23 | 5.5% / 1.25 / 36 | 11.5% / 2.17 / 35 | -0.7% / -0.12 / 18 |
| 101 | -0.4% / -0.11 / 37 | 0.3% / 0.14 / 28 | 7.0% / 1.39 / 36 | 12.2% / 2.38 / 43 | 0.5% / 0.13 / 26 |
| 102 | 2.0% / 0.63 / 27 | -0.9% / -0.36 / 13 | 1.1% / 0.39 / 21 | 8.9% / 1.70 / 28 | 3.9% / 0.76 / 19 |
| 103 | 0.2% / 0.08 / 13 | 1.5% / 0.62 / 21 | 5.6% / 1.03 / 25 | 8.3% / 1.85 / 30 | 1.2% / 0.33 / 17 |
| 104 | 1.8% / 0.48 / 35 | -0.4% / -0.13 / 22 | 5.2% / 1.26 / 28 | 7.1% / 1.59 / 42 | 2.3% / 0.47 / 18 |
| 105 | 2.0% / 0.55 / 35 | -0.4% / -0.13 / 22 | 5.2% / 1.26 / 28 | 7.9% / 1.70 / 42 | 1.1% / 0.27 / 18 |
| 106 | 3.7% / 1.20 / 36 | 0.3% / 0.17 / 20 | 7.0% / 1.47 / 30 | 5.8% / 1.41 / 39 | -0.6% / -0.13 / 18 |
| 107 | 0.8% / 0.19 / 37 | 0.5% / 0.18 / 22 | 8.4% / 1.34 / 33 | 10.0% / 1.89 / 30 | 1.7% / 0.32 / 22 |
| 108 | 6.5% / 2.36 / 28 | 0.8% / 0.51 / 16 | 7.1% / 1.54 / 25 | 3.9% / 0.89 / 26 | -1.3% / -0.33 / 11 |
| 109 | 3.2% / 0.72 / 51 | -0.6% / -0.14 / 41 | 5.9% / 0.94 / 45 | 20.2% / 3.10 / 56 | 2.3% / 0.34 / 36 |
| 110 | 2.5% / 0.74 / 23 | 1.1% / 0.52 / 23 | 1.3% / 0.35 / 32 | 12.2% / 2.23 / 33 | 0.9% / 0.18 / 14 |
| 111 | 2.1% / 1.00 / 19 | 1.8% / 0.80 / 21 | 6.5% / 1.39 / 29 | 8.6% / 1.84 / 41 | 1.0% / 0.21 / 25 |
| 112 | 3.2% / 1.17 / 33 | 0.5% / 0.26 / 20 | 5.5% / 1.42 / 26 | 8.0% / 1.93 / 30 | -1.3% / -0.31 / 13 |
| 113 | -0.4% / -0.11 / 26 | 0.6% / 0.26 / 28 | 1.0% / 0.27 / 32 | 13.5% / 2.36 / 37 | 2.4% / 0.42 / 18 |
| 114 | 1.6% / 0.51 / 65 | -0.9% / -0.45 / 36 | 6.9% / 1.82 / 42 | 7.9% / 2.11 / 58 | -2.2% / -0.63 / 30 |
| 115 | 0.7% / 0.24 / 13 | 0.0% / 0.01 / 20 | 5.7% / 1.03 / 25 | 7.2% / 1.67 / 30 | 1.5% / 0.37 / 17 |
| 116 | 0.9% / 0.32 / 65 | -1.0% / -0.50 / 36 | 6.8% / 1.79 / 42 | 8.3% / 2.13 / 58 | -2.1% / -0.61 / 30 |
| 117 | 3.7% / 1.25 / 33 | 0.6% / 0.31 / 20 | 5.5% / 1.43 / 26 | 7.5% / 1.87 / 30 | -1.1% / -0.27 / 13 |
| 118 | 1.4% / 0.47 / 55 | -0.7% / -0.44 / 24 | 10.6% / 2.26 / 37 | 5.5% / 1.59 / 53 | -3.4% / -1.04 / 26 |
| 119 | 1.0% / 0.23 / 37 | -0.1% / -0.02 / 22 | 6.7% / 1.34 / 33 | 10.1% / 1.88 / 30 | 3.3% / 0.51 / 22 |
| 120 | 2.6% / 0.64 / 35 | -0.2% / -0.17 / 17 | 7.4% / 1.70 / 22 | 6.8% / 1.89 / 26 | -1.8% / -0.54 / 18 |
| 121 | 1.2% / 0.41 / 55 | -0.7% / -0.44 / 24 | 10.6% / 2.26 / 37 | 5.6% / 1.61 / 53 | -3.5% / -1.04 / 26 |
| 122 | 0.1% / 0.07 / 35 | -1.1% / -0.68 / 32 | 8.9% / 2.23 / 43 | 6.1% / 1.66 / 45 | -1.7% / -0.47 / 22 |
| 123 | 0.1% / 0.07 / 35 | -1.1% / -0.68 / 32 | 8.9% / 2.23 / 43 | 6.1% / 1.66 / 45 | -1.7% / -0.47 / 22 |
| 124 | 2.6% / 0.64 / 35 | -0.2% / -0.17 / 17 | 7.4% / 1.70 / 22 | 6.9% / 1.90 / 26 | -1.8% / -0.54 / 18 |
| 125 | 1.0% / 0.23 / 51 | -2.9% / -0.93 / 34 | 7.6% / 1.31 / 51 | 14.6% / 2.31 / 51 | 4.3% / 0.82 / 33 |
| 126 | 0.3% / 0.08 / 51 | -2.8% / -0.88 / 34 | 7.6% / 1.30 / 51 | 14.0% / 2.29 / 51 | 5.0% / 0.90 / 33 |
| 127 | 1.1% / 0.34 / 51 | -1.9% / -0.61 / 47 | 9.0% / 1.87 / 51 | 10.6% / 2.04 / 64 | -0.9% / -0.14 / 38 |
| 128 | -1.0% / -0.21 / 59 | -0.8% / -0.26 / 37 | 10.1% / 1.54 / 46 | 12.8% / 2.33 / 56 | 0.8% / 0.18 / 37 |
| 129 | -1.0% / -0.21 / 59 | -0.8% / -0.26 / 37 | 10.1% / 1.54 / 46 | 12.8% / 2.33 / 56 | 0.8% / 0.18 / 37 |
| 130 | -3.9% / -0.85 / 45 | -1.1% / -0.33 / 36 | 10.6% / 1.63 / 43 | 12.1% / 2.21 / 49 | 2.0% / 0.38 / 28 |
| 131 | 1.1% / 0.48 / 24 | -0.4% / -0.18 / 14 | 7.1% / 1.79 / 18 | 5.1% / 1.44 / 27 | -0.6% / -0.14 / 19 |
| 132 | 1.0% / 0.42 / 52 | -1.3% / -0.59 / 47 | 8.8% / 1.93 / 55 | 6.1% / 1.71 / 60 | -1.1% / -0.42 / 39 |
| 133 | 1.0% / 0.42 / 52 | -1.3% / -0.59 / 47 | 8.8% / 1.93 / 55 | 6.1% / 1.72 / 60 | -1.1% / -0.42 / 39 |
| 134 | -9.7% / -1.36 / 117 | 0.0% / 0.03 / 107 | 29.8% / 1.70 / 108 | 6.3% / 0.72 / 130 | 16.3% / 1.57 / 121 |
| 135 | -2.1% / -0.50 / 37 | -2.1% / -0.74 / 31 | 4.5% / 0.83 / 43 | 14.1% / 2.34 / 49 | 6.2% / 1.16 / 24 |
| 136 | 1.9% / 0.50 / 67 | -0.3% / -0.09 / 48 | 7.3% / 1.57 / 53 | 9.4% / 2.06 / 76 | -1.3% / -0.25 / 46 |
| 137 | 0.0% / 0.03 / 38 | 1.2% / 0.47 / 32 | 0.5% / 0.14 / 45 | 14.4% / 2.48 / 50 | 1.3% / 0.26 / 24 |
| 138 | 2.4% / 0.83 / 29 | -1.3% / -0.93 / 16 | 6.8% / 2.31 / 25 | 5.3% / 1.66 / 28 | -2.7% / -1.04 / 11 |
| 139 | 2.4% / 0.83 / 29 | -1.3% / -0.93 / 16 | 6.8% / 2.31 / 25 | 5.3% / 1.65 / 28 | -2.7% / -1.04 / 11 |
| 140 | -9.6% / -1.36 / 118 | 2.5% / 0.54 / 109 | 27.5% / 1.67 / 109 | 5.9% / 0.69 / 133 | 16.6% / 1.65 / 122 |
| 141 | 0.3% / 0.09 / 40 | 0.1% / 0.08 / 27 | 6.0% / 0.84 / 37 | 9.4% / 2.22 / 40 | 8.8% / 1.37 / 39 |
| 142 | 1.2% / 0.30 / 42 | -2.8% / -0.79 / 35 | 5.7% / 0.98 / 43 | 22.1% / 3.11 / 50 | -4.6% / -0.85 / 29 |
| 143 | 2.7% / 0.54 / 92 | 2.6% / 0.76 / 87 | 21.2% / 1.80 / 89 | -4.5% / -0.96 / 97 | 4.1% / 0.79 / 117 |
| 144 | -1.4% / -0.19 / 54 | 1.1% / 0.28 / 41 | 7.6% / 1.49 / 41 | 23.8% / 3.14 / 52 | -2.5% / -0.46 / 30 |
| 145 | 1.5% / 0.41 / 67 | -0.5% / -0.17 / 48 | 7.2% / 1.55 / 53 | 9.6% / 2.07 / 77 | -1.2% / -0.24 / 46 |
| 146 | 2.3% / 0.50 / 62 | -1.0% / -0.25 / 39 | 2.6% / 0.45 / 52 | 19.1% / 2.89 / 61 | -1.2% / -0.18 / 44 |
| 147 | 2.6% / 0.53 / 50 | -3.0% / -0.79 / 39 | 5.2% / 0.92 / 45 | 21.3% / 3.12 / 55 | 1.7% / 0.26 / 36 |
| 148 | 2.9% / 0.58 / 92 | 2.6% / 0.75 / 86 | 21.2% / 1.80 / 89 | -4.6% / -0.98 / 97 | 4.4% / 0.83 / 117 |
| 149 | 1.3% / 0.28 / 81 | -0.1% / -0.00 / 54 | 6.7% / 1.46 / 59 | 16.3% / 2.52 / 78 | -3.7% / -0.80 / 49 |
| 150 | 1.2% / 0.38 / 44 | 0.7% / 0.33 / 33 | -0.9% / -0.14 / 46 | 14.4% / 2.61 / 49 | 3.1% / 0.59 / 34 |
| 151 | 1.2% / 0.31 / 62 | -0.0% / 0.01 / 40 | 4.7% / 0.75 / 53 | 18.0% / 3.01 / 62 | -0.8% / -0.10 / 44 |
| 152 | -4.9% / -1.41 / 69 | 1.4% / 0.72 / 44 | 11.5% / 1.81 / 54 | 9.0% / 1.98 / 83 | 2.7% / 0.71 / 65 |
| 153 | -4.8% / -1.40 / 69 | 1.2% / 0.64 / 44 | 11.6% / 1.81 / 54 | 8.9% / 1.97 / 83 | 2.8% / 0.73 / 65 |
| 154 | -5.2% / -1.17 / 80 | 3.9% / 1.34 / 47 | 1.0% / 0.18 / 60 | 14.1% / 2.39 / 87 | 10.1% / 1.76 / 67 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_c27b` | 12 | 0.83 | 0.79/0.84 | 0.59/0.64 |
| 1 | `cfg_5371` | 15 | 0.82 | 0.52/0.55 | 0.32/0.48 |
| 2 | `cfg_e790` | 6 | 0.89 | 0.87/0.87 | 0.79/0.79 |
| 3 | `cfg_efb0` | 6 | 0.91 | 0.85/0.86 | 0.83/0.83 |
| 4 | `cfg_cdae` | 12 | 0.85 | 0.81/0.84 | 0.62/0.68 |
| 5 | `cfg_4f41` | 6 | 0.94 | 0.93/0.94 | 0.75/0.76 |
| 6 | `cfg_eb13` | 9 | 0.87 | 0.86/0.87 | 0.56/0.76 |
| 7 | `cfg_c7e0` | 18 | 0.81 | 0.82/0.88 | 0.60/0.67 |
| 8 | `cfg_66ec` | 19 | 0.81 | 0.73/0.82 | 0.34/0.45 |
| 9 | `cfg_d2b8` | 2 | 0.97 | 0.96/0.96 | 0.95/0.95 |
| 10 | `cfg_05da` | 3 | 1.00 | 1.00/1.00 | 0.99/0.99 |
| 11 | `cfg_fa05` | 10 | 0.83 | 0.88/0.95 | 0.59/0.87 |
| 12 | `cfg_5121` | 9 | 0.80 | 0.79/0.91 | 0.69/0.75 |
| 13 | `cfg_fd80` | 9 | 0.85 | 0.66/0.68 | 0.56/0.59 |
| 14 | `cfg_062d` | 3 | 0.99 | 0.99/0.99 | 0.98/0.98 |
| 15 | `cfg_0674` | 7 | 0.84 | 0.67/0.77 | 0.50/0.68 |
| 16 | `cfg_34d8` | 7 | 0.88 | 0.85/0.94 | 0.66/0.78 |
| 17 | `cfg_082c` | 3 | 0.95 | 0.95/0.95 | 0.94/0.94 |
| 18 | `cfg_0dfd` | 12 | 0.82 | 0.75/0.80 | 0.50/0.53 |
| 19 | `cfg_ff27` | 2 | 0.96 | 0.94/0.94 | 0.90/0.90 |
| 20 | `cfg_4110` | 6 | 0.87 | 0.76/0.78 | 0.64/0.65 |
| 21 | `cfg_c91c` | 4 | 0.90 | 0.88/0.99 | 0.82/0.99 |
| 22 | `cfg_e052` | 6 | 0.90 | 0.86/0.86 | 0.73/0.74 |
| 23 | `cfg_09c9` | 8 | 0.85 | 0.77/0.83 | 0.66/0.73 |
| 24 | `cfg_6adf` | 4 | 0.84 | 0.85/0.86 | 0.63/0.63 |
| 25 | `cfg_231f` | 9 | 0.88 | 0.81/0.90 | 0.63/0.73 |
| 26 | `cfg_7ca1` | 6 | 0.88 | 0.86/0.86 | 0.82/0.82 |
| 27 | `cfg_10a4` | 6 | 0.83 | 0.65/0.74 | 0.54/0.55 |
| 28 | `cfg_0d59` | 10 | 0.84 | 0.83/0.92 | 0.53/0.78 |
| 29 | `cfg_bd17` | 3 | 1.00 | 0.99/1.00 | 1.00/1.00 |
| 30 | `cfg_a82b` | 4 | 0.91 | 0.90/0.96 | 0.60/0.91 |
| 31 | `cfg_1186` | 6 | 0.90 | 0.91/0.91 | 0.73/0.74 |
| 32 | `cfg_3c77` | 6 | 0.88 | 0.88/0.89 | 0.62/0.62 |
| 33 | `cfg_b875` | 13 | 0.83 | 0.73/0.84 | 0.40/0.58 |
| 34 | `cfg_140b` | 9 | 0.84 | 0.89/0.90 | 0.49/0.64 |
| 35 | `cfg_142a` | 9 | 0.84 | 0.86/0.94 | 0.82/0.87 |
| 36 | `cfg_aadc` | 4 | 0.93 | 0.94/1.00 | 0.61/0.99 |
| 37 | `cfg_ca7d` | 3 | 0.99 | 0.98/0.98 | 0.97/0.97 |
| 38 | `cfg_1836` | 1 | n/a | n/a/n/a | n/a/n/a |
| 39 | `cfg_6cb8` | 9 | 0.82 | 0.77/0.89 | 0.57/0.79 |
| 40 | `cfg_4a27` | 6 | 0.89 | 0.90/0.90 | 0.89/0.90 |
| 41 | `cfg_daa4` | 7 | 0.89 | 0.80/0.97 | 0.71/0.89 |
| 42 | `cfg_dff3` | 3 | 0.99 | 0.99/0.99 | 0.98/0.98 |
| 43 | `cfg_61bb` | 5 | 0.89 | 0.85/0.91 | 0.73/0.86 |
| 44 | `cfg_2295` | 5 | 0.93 | 0.91/0.95 | 0.65/0.81 |
| 45 | `cfg_1ed7` | 1 | n/a | n/a/n/a | n/a/n/a |
| 46 | `cfg_6bcb` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 47 | `cfg_9495` | 9 | 0.88 | 0.86/0.91 | 0.68/0.75 |
| 48 | `cfg_d7c9` | 3 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 49 | `cfg_228b` | 2 | 0.89 | 0.79/0.79 | 0.52/0.52 |
| 50 | `cfg_abc8` | 4 | 0.92 | 0.92/0.99 | 0.87/0.99 |
| 51 | `cfg_83bb` | 6 | 0.83 | 0.79/0.79 | 0.50/0.50 |
| 52 | `cfg_3d6d` | 4 | 0.89 | 0.86/0.97 | 0.62/0.96 |
| 53 | `cfg_d880` | 9 | 0.90 | 0.72/0.93 | 0.62/0.73 |
| 54 | `cfg_5092` | 3 | 1.00 | 1.00/1.00 | 0.99/1.00 |
| 55 | `cfg_4830` | 9 | 0.82 | 0.75/0.79 | 0.63/0.67 |
| 56 | `cfg_ebbd` | 3 | 0.94 | 0.95/0.95 | 0.96/0.96 |
| 57 | `cfg_33ce` | 3 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 58 | `cfg_36f2` | 3 | 0.98 | 0.98/0.98 | 0.97/0.97 |
| 59 | `cfg_5e66` | 3 | 0.86 | 0.79/0.80 | 0.47/0.48 |
| 60 | `cfg_b712` | 3 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 61 | `cfg_7956` | 6 | 0.96 | 0.95/0.95 | 0.78/0.78 |
| 62 | `cfg_aea9` | 6 | 0.85 | 0.77/0.78 | 0.51/0.51 |
| 63 | `cfg_487b` | 3 | 0.96 | 0.96/0.96 | 0.92/0.93 |
| 64 | `cfg_4db9` | 8 | 0.84 | 0.66/0.87 | 0.52/0.56 |
| 65 | `cfg_9a29` | 6 | 0.88 | 0.89/0.92 | 0.65/0.66 |
| 66 | `cfg_54c0` | 1 | n/a | n/a/n/a | n/a/n/a |
| 67 | `cfg_aec7` | 6 | 0.89 | 0.87/0.89 | 0.75/0.76 |
| 68 | `cfg_5bee` | 1 | n/a | n/a/n/a | n/a/n/a |
| 69 | `cfg_8a30` | 2 | 0.91 | 0.89/0.89 | 0.71/0.71 |
| 70 | `cfg_e6e5` | 3 | 0.99 | 0.99/0.99 | 0.99/1.00 |
| 71 | `cfg_7475` | 6 | 0.86 | 0.79/0.84 | 0.70/0.74 |
| 72 | `cfg_8782` | 6 | 0.94 | 0.94/0.95 | 0.82/0.82 |
| 73 | `cfg_7caa` | 3 | 1.00 | 1.00/1.00 | 0.99/0.99 |
| 74 | `cfg_cc63` | 3 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 75 | `cfg_c85a` | 3 | 0.99 | 0.99/1.00 | 1.00/1.00 |
| 76 | `cfg_e394` | 3 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 77 | `cfg_b22d` | 3 | 0.91 | 0.91/0.95 | 0.89/0.94 |
| 78 | `cfg_e32b` | 1 | n/a | n/a/n/a | n/a/n/a |
| 79 | `cfg_f97f` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 8.636e-04 over 13608 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 647.0, participation ratio 11.6, 95%-variance components 161 (rank bound T = 1259); raw grid 13608; raw + known prior 924612
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
