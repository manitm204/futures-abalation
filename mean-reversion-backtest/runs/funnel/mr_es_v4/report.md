# Screening funnel -- mr_es_v4 (development stages only)

- Code: `3b70ca612d69` (dirty working tree: True, diff sha256 `d13052ae8f8f`)
- Config: `configs/funnel/mr_funnel_es_v4.yaml` sha256 `accf188ed54956b2`; seed 20261021
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ES': '2026-10-16', 'NQ': '2026-10-16'}
- Frozen manifest sha256: `146ee509da092df0` (18 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_es_v3 gated 11 ES candidates on 2023-2024 and this v4 stage-4 change was made after reading those results. Also, ES and SPY track the same index, and SPY 2023-2024 gated the mr_v1/mr_v2 (and channel/Donchian) candidates, and this v3 grid was written after those results -- so the slice is not fully independent of earlier research.
- Holdout 2025+ previously inspected: **False** -- No ES strategy metrics have been computed on 2025+. SPY 2025-2026 holdout metrics were inspected in earlier SPY studies, and the futures correlation matrix (test-dabento/correlation.py) used 2025-2026 returns (no strategy selection).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 46080 | 46080 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 46080 | 46080 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 46080 | 22842 | 23238 | 0 |  | 27108 | 49.57 | 49.57 |  |
| 3 performance & risk | hard_gate | 22842 | 57 | 22785 | 0 |  | 0 | 0.12 | 0.25 |  |
| 4 parameter stability | hard_gate | 57 | 55 | 2 | 0 |  | 0 | 0.12 | 96.49 |  |
| 5 time stability | hard_gate | 55 | 55 | 0 | 0 |  | 31 | 0.12 | 100.00 |  |
| 6 deduplication | dedup | 55 | 18 |  |  | 37 |  | 0.04 | 32.73 | best 2 per cluster |
| 7 execution stress | hard_gate | 18 | 18 | 0 | 0 |  | 0 | 0.04 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 18 |  |  |  |  |  |  |  | diagnostic only: unverified: 18 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 23233 |
| s2:hard_reject:years_with_>=10_trades | 20267 |
| s3:hard_reject:max_drawdown | 4739 |
| s3:hard_reject:net_return | 20276 |
| s3:hard_reject:sharpe | 22785 |
| s4:hard_reject:local_median_sharpe | 2 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | NQ dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_50da` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 63/102/23 | 188 | 27.1% | 4.9% | 1.00 | -4.7% | 281 | 1.64 | 3.1% | 87.9 | 10/10 | 0.60 | 0.41 | 0.59 | 4 | 15.7% | 0.39 | 0.41 | 25.8% | 23.6% | 16.9% | 22.9%/17.1% | 8.4 (interpolated) | pass | 0.009 (unverified) | 0.89 |
| 2 | `cfg_b2cb` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-3.0, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 33/132/23 | 188 | 25.3% | 4.6% | 0.99 | -5.5% | 242 | 1.59 | 3.2% | 88.1 | 11/11 | 0.64 | 0.52 | 0.47 | 4 | 15.0% | 0.35 | 0.38 | 23.3% | 21.3% | 18.8% | 21.4%/16.7% | 7.8 (interpolated) | pass | 0.010 (unverified) | 0.79 |
| 3 | `cfg_54b2` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 59/11/53 | 123 | 33.9% | 6.0% | 0.89 | -6.3% | 276 | 1.63 | 8.1% | 56.5 | 10/10 | 0.80 | 0.49 | 0.40 | 4 | 19.7% | 0.40 | 0.52 | 32.4% | 31.0% | 26.1% | 29.6%/21.7% | 15.1 (interpolated) | pass | 0.006 (unverified) | -0.27 |
| 4 | `cfg_5575` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=2.0 | 58/13/39 | 110 | 30.7% | 5.5% | 0.83 | -11.2% | 358 | 1.60 | 8.2% | 50.6 | 10/10 | 0.90 | 0.50 | 0.33 | 4 | 13.4% | 0.53 | 0.54 | 28.6% | 27.8% | 24.1% | 28.6%/21.3% | 15.5 (interpolated) | pass | 0.005 (unverified) | -0.12 |
| 5 | `cfg_c485` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 18/166/0 | 184 | 27.3% | 5.0% | 0.95 | -6.9% | 462 | 1.69 | 3.3% | 86.0 | 10/10 | 0.60 | 0.56 | 0.38 | 4 | 7.9% | 0.66 | 0.54 | 24.8% | 23.2% | 26.9% | 24.0%/18.3% | 8.8 (interpolated) | pass | 0.004 (unverified) | 0.53 |
| 6 | `cfg_8d96` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=16, entry_confirmation=none, stop_atr_multiple=1.0 | 63/0/92 | 155 | 27.2% | 4.9% | 0.79 | -6.0% | 314 | 1.41 | 8.2% | 71.8 | 9/9 | 0.78 | 0.39 | 0.40 | 4 | 12.4% | 0.53 | 0.65 | 25.1% | 22.5% | 18.3% | 23.5%/13.7% | 10.6 (interpolated) | pass | 0.003 (unverified) | -0.12 |
| 7 | `cfg_43e0` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=30, entry_confirmation=none, stop_atr_multiple=1.0 | 63/0/92 | 155 | 27.2% | 4.9% | 0.79 | -6.0% | 314 | 1.41 | 8.2% | 71.8 | 8/8 | 0.75 | 0.29 | 0.50 | 4 | 12.4% | 0.53 | 0.65 | 25.1% | 22.5% | 18.3% | 24.8%/15.6% | 10.6 (interpolated) | pass | 0.003 (unverified) | -0.12 |
| 8 | `cfg_8a46` | timeframe=15min, mean_type=ema, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 27/157/0 | 184 | 27.1% | 4.9% | 0.95 | -6.9% | 519 | 1.68 | 3.3% | 86.1 | 11/11 | 0.64 | 0.60 | 0.35 | 4 | 7.5% | 0.67 | 0.56 | 25.1% | 23.5% | 25.8% | 22.7%/16.5% | 8.8 (interpolated) | pass | 0.004 (unverified) | 0.57 |
| 9 | `cfg_2e9e` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.5 | 37/30/54 | 121 | 34.6% | 6.1% | 0.85 | -5.9% | 122 | 1.62 | 9.2% | 55.4 | 11/11 | 0.82 | 0.58 | 0.27 | 5 | 19.7% | 0.40 | 0.62 | 33.5% | 31.2% | 24.2% | 29.5%/21.0% | 16.0 (interpolated) | pass | 0.004 (unverified) | -0.28 |
| 10 | `cfg_bed1` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=2.0 | 23/53/25 | 101 | 19.9% | 3.7% | 0.84 | -9.7% | 330 | 1.63 | 5.8% | 46.3 | 9/9 | 0.78 | 0.41 | 0.43 | 4 | 11.2% | 0.41 | 0.63 | 18.9% | 18.3% | 18.9% | 18.6%/13.8% | 11.7 (interpolated) | pass | 0.008 (unverified) | -0.08 |
| 11 | `cfg_cb04` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-0.5, max_holding_bars=10, entry_confirmation=none, stop_atr_multiple=1.0 | 37/24/88 | 149 | 28.3% | 5.1% | 0.79 | -6.0% | 235 | 1.45 | 9.0% | 68.8 | 10/10 | 0.80 | 0.64 | 0.15 | 4 | 12.9% | 0.51 | 0.73 | 25.6% | 24.1% | 18.4% | 24.2%/12.9% | 11.0 (interpolated) | pass | 0.003 (unverified) | -0.04 |
| 12 | `cfg_7cad` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.0, exit_z=-0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 20/60/26 | 106 | 36.0% | 6.3% | 0.92 | -7.0% | 248 | 1.96 | 6.0% | 50.1 | 9/9 | 0.78 | 0.64 | 0.28 | 4 | 19.5% | 0.46 | 0.48 | 34.2% | 33.2% | 19.1% | 31.0%/25.3% | 17.9 (interpolated) | pass | 0.010 (unverified) | 1.14 |
| 13 | `cfg_5c5a` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=10, entry_z=-3.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=1.5 | 31/49/26 | 106 | 35.0% | 6.2% | 0.91 | -6.9% | 242 | 1.93 | 6.0% | 50.2 | 8/8 | 0.75 | 0.61 | 0.30 | 4 | 18.8% | 0.46 | 0.49 | 33.6% | 32.4% | 19.2% | 31.1%/24.1% | 17.5 (interpolated) | pass | 0.009 (unverified) | 1.02 |
| 14 | `cfg_b545` | timeframe=1h, mean_type=sma, mean_lookback=40, std_lookback=80, entry_z=-2.0, exit_z=-1.0, max_holding_bars=5, entry_confirmation=none, stop_atr_multiple=1.0 | 31/40/77 | 148 | 18.7% | 3.5% | 0.77 | -8.5% | 330 | 1.42 | 6.3% | 67.6 | 8/8 | 0.75 | 0.25 | 0.52 | 4 | 8.7% | 0.51 | 0.69 | 17.3% | 15.4% | 12.8% | 17.3%/10.5% | 7.9 (interpolated) | pass | 0.002 (unverified) | -0.15 |
| 15 | `cfg_a341` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=-1.0, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=2.5 | 88/196/41 | 325 | 30.5% | 5.5% | 0.90 | -6.4% | 283 | 1.42 | 5.3% | 152.3 | 11/11 | 0.55 | 0.44 | 0.45 | 4 | 14.4% | 0.46 | 0.55 | 27.3% | 23.6% | 21.1% | 27.7%/20.8% | 5.9 (interpolated) | pass | 0.003 (unverified) | 0.39 |
| 16 | `cfg_9dd2` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=5, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 29/268/0 | 297 | 30.3% | 5.4% | 0.91 | -5.7% | 344 | 1.49 | 5.3% | 139.8 | 10/10 | 0.50 | 0.11 | 0.81 | 4 | 17.1% | 0.38 | 0.56 | 27.2% | 23.5% | 24.2% | 28.8%/22.3% | 6.2 (interpolated) | pass | 0.004 (unverified) | 0.50 |
| 17 | `cfg_313f` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=0.5, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 82/197/0 | 279 | 42.7% | 7.4% | 0.86 | -13.8% | 249 | 1.42 | 8.6% | 129.4 | 11/11 | 0.64 | 0.37 | 0.49 | 4 | 17.8% | 0.56 | 0.65 | 40.2% | 38.4% | 28.2% | 39.5%/27.9% | 8.3 (interpolated) | pass | 0.004 (unverified) | 0.18 |
| 18 | `cfg_103b` | timeframe=15min, mean_type=sma, mean_lookback=40, std_lookback=20, entry_z=-2.5, exit_z=0.0, max_holding_bars=10, entry_confirmation=positive_bar_return, stop_atr_multiple=none | 104/177/0 | 281 | 40.3% | 7.0% | 0.83 | -13.1% | 249 | 1.40 | 8.3% | 131.2 | 12/12 | 0.67 | 0.42 | 0.41 | 4 | 20.3% | 0.47 | 0.62 | 38.3% | 31.3% | 26.0% | 34.1%/27.4% | 7.8 (interpolated) | pass | 0.005 (unverified) | 0.11 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | -1.4% / -0.29 / 36 | 8.5% / 2.83 / 38 | 9.8% / 1.18 / 42 | 6.5% / 2.30 / 19 | 1.5% / 0.38 / 53 |
| 2 | -0.8% / -0.14 / 36 | 9.0% / 2.98 / 38 | 7.7% / 1.02 / 42 | 6.6% / 2.35 / 19 | 1.0% / 0.26 / 53 |
| 3 | 8.2% / 0.98 / 35 | -0.7% / -0.18 / 18 | 6.2% / 0.75 / 17 | 11.8% / 2.05 / 32 | 4.9% / 0.74 / 21 |
| 4 | 6.1% / 0.73 / 32 | -1.2% / -0.30 / 17 | 2.4% / 0.33 / 17 | 15.3% / 2.82 / 25 | 5.8% / 0.86 / 19 |
| 5 | -2.5% / -0.54 / 35 | 3.0% / 1.26 / 31 | 18.0% / 1.83 / 39 | 5.5% / 1.98 / 20 | 1.9% / 0.46 / 59 |
| 6 | 6.9% / 1.00 / 44 | -0.2% / -0.03 / 20 | 2.9% / 0.41 / 22 | 13.2% / 2.58 / 42 | 2.3% / 0.34 / 27 |
| 7 | 6.9% / 1.00 / 44 | -0.2% / -0.03 / 20 | 2.9% / 0.41 / 22 | 13.2% / 2.58 / 42 | 2.3% / 0.34 / 27 |
| 8 | -2.2% / -0.46 / 35 | 2.4% / 1.00 / 31 | 18.2% / 1.89 / 39 | 5.4% / 1.98 / 20 | 1.8% / 0.45 / 59 |
| 9 | 5.1% / 0.60 / 35 | 1.3% / 0.34 / 18 | 4.0% / 0.49 / 15 | 12.5% / 1.96 / 32 | 8.0% / 1.08 / 21 |
| 10 | -1.9% / -0.23 / 31 | 2.1% / 1.13 / 15 | 3.6% / 1.02 / 14 | 7.8% / 2.01 / 25 | 7.1% / 1.62 / 16 |
| 11 | 4.1% / 0.58 / 44 | 2.3% / 0.57 / 20 | -1.1% / -0.11 / 18 | 13.6% / 2.34 / 40 | 7.2% / 0.97 / 27 |
| 12 | -0.1% / 0.01 / 31 | 4.0% / 1.33 / 15 | 10.3% / 0.88 / 20 | 4.3% / 2.03 / 6 | 13.7% / 2.04 / 34 |
| 13 | -0.1% / 0.01 / 31 | 4.2% / 1.39 / 15 | 9.4% / 0.81 / 20 | 4.4% / 2.03 / 6 | 13.7% / 2.02 / 34 |
| 14 | -1.1% / -0.16 / 44 | 2.7% / 1.47 / 18 | 2.1% / 0.45 / 21 | 9.3% / 2.21 / 41 | 4.7% / 0.90 / 24 |
| 15 | -3.6% / -0.66 / 79 | 4.6% / 1.47 / 58 | 14.1% / 1.29 / 59 | 6.3% / 1.93 / 41 | 6.8% / 1.27 / 88 |
| 16 | -2.0% / -0.36 / 69 | 5.0% / 1.54 / 53 | 11.3% / 1.11 / 55 | 7.4% / 2.09 / 39 | 6.1% / 1.13 / 81 |
| 17 | 4.9% / 0.77 / 65 | 8.4% / 2.14 / 52 | 21.1% / 1.33 / 53 | 11.9% / 2.74 / 38 | -7.5% / -0.89 / 71 |
| 18 | 5.6% / 0.87 / 66 | 8.1% / 2.08 / 52 | 16.6% / 1.10 / 54 | 11.8% / 2.73 / 38 | -5.7% / -0.67 / 71 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_7cad` | 8 | 0.87 | 0.95/0.97 | 0.91/0.95 |
| 1 | `cfg_313f` | 5 | 0.92 | 0.82/0.90 | 0.69/0.84 |
| 2 | `cfg_c485` | 10 | 0.82 | 0.77/0.96 | 0.52/0.91 |
| 3 | `cfg_a341` | 8 | 0.96 | 0.92/0.93 | 0.85/0.90 |
| 4 | `cfg_2e9e` | 2 | 0.88 | 0.89/0.89 | 0.81/0.81 |
| 5 | `cfg_54b2` | 9 | 0.89 | 0.93/0.95 | 0.87/0.90 |
| 6 | `cfg_8d96` | 3 | 0.98 | 0.98/0.99 | 0.98/0.99 |
| 7 | `cfg_50da` | 8 | 0.93 | 0.90/0.92 | 0.85/0.91 |
| 8 | `cfg_bed1` | 2 | 0.91 | 0.83/0.83 | 0.61/0.61 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.511e-03 over 38080 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1128.0, participation ratio 25.0, 95%-variance components 255 (rank bound T = 1259); raw grid 46080; raw + known prior 389544
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
NQ results are unchanged rules on the development period: supporting evidence, not an independent replication.

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
