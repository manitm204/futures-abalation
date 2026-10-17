# Screening funnel -- funnel_v4_dev (development stages only)

- Code: `737d995cb21f` (dirty working tree: True, diff sha256 `7bb371241a72`)
- Config: `/home/manit/Desktop/fun_projects/backtest/configs/funnel/channel_funnel.yaml` sha256 `59ab3f74a9f0a486`; seed 20261016
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'SPY': '2026-08-18', 'QQQ': '2026-08-18'}
- Frozen manifest sha256: `77d6f996bf2460f3` (16 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- funnel_v1, funnel_v2_screened and funnel_v3_dsr gated on 2023-2024 validation metrics, and thresholds (Sharpe gate, multiple-testing method) were changed between those runs. Validation is previously inspected data.
- Holdout 2025+ previously inspected: **True** -- funnel_v1..v3 records.parquet store 2025-2026 holdout metrics for all 24,576 configs, and the Donchian ablation report discussed holdout degradation. The holdout is NOT an untouched test.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 24576 | 24576 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 24576 | 24576 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 24576 | 14901 | 9675 | 0 |  | 16895 | 60.63 | 60.63 |  |
| 3 performance & risk | hard_gate | 14901 | 137 | 14764 | 0 |  | 0 | 0.56 | 0.92 |  |
| 4 parameter stability | hard_gate | 137 | 126 | 11 | 0 |  | 137 | 0.51 | 91.97 |  |
| 5 time stability | hard_gate | 126 | 126 | 0 | 0 |  | 126 | 0.51 | 100.00 |  |
| 6 deduplication | dedup | 126 | 16 |  |  | 110 |  | 0.07 | 12.70 |  |
| 7 execution stress | hard_gate | 16 | 16 | 0 | 0 |  | 0 | 0.07 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 16 |  |  |  |  |  |  |  | diagnostic only: unverified: 16 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 9675 |
| s2:hard_reject:years_with_>=10_trades | 3739 |
| s3:hard_reject:max_drawdown | 663 |
| s3:hard_reject:net_return | 9757 |
| s3:hard_reject:sharpe | 14764 |
| s4:hard_reject:neighbor_frac_profitable | 11 |
| s4:hard_reject:neighbor_median_sharpe | 2 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | tf | entry/exit | buf | stop | conf | trend | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | QQQ dev SR |
|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_cd00` | 15min | 40/40 | 0.1 | 3 | 1 | ema200 | 236 | 12.9% | 2.5% | 0.78 | -2.5% | 246 | 1.35 | 43.1% | 40.9 | 10/10 | 0.90 | 0.75 | 0.03 | 5 | 7.7% | 0.37 | 0.68 | 11.6% | 10.4% | 9.5% | 12.1%/9.8% | 6.2 (interpolated) | pass | 0.009 (unverified) | 0.70 |
| 2 | `cfg_2f28` | 15min | 30/30 | 0.1 | 3 | 1 | ema200 | 272 | 12.6% | 2.4% | 0.77 | -3.1% | 286 | 1.31 | 41.9% | 47.0 | 10/10 | 1.00 | 0.71 | 0.06 | 4 | 7.0% | 0.42 | 0.69 | 11.2% | 9.8% | 8.9% | 12.0%/10.0% | 5.5 (interpolated) | pass | 0.008 (unverified) | 0.90 |
| 3 | `cfg_34cb` | 15min | 55/55 | 0.0 | 3 | 1 | ema200 | 185 | 14.0% | 2.7% | 0.81 | -2.2% | 143 | 1.48 | 45.7% | 32.3 | 9/9 | 1.00 | 0.69 | 0.11 | 5 | 9.3% | 0.33 | 0.72 | 13.0% | 12.0% | 11.0% | 13.3%/10.9% | 8.1 (interpolated) | pass | 0.010 (unverified) | 1.13 |
| 4 | `cfg_d367` | 15min | 40/30 | 0.1 | off | 2 | sma100 | 151 | 5.0% | 1.0% | 0.90 | -0.9% | 204 | 1.63 | 29.7% | 11.3 | 10/10 | 0.90 | 0.68 | 0.22 | 5 | 3.2% | 0.37 | 0.52 | 4.7% | 4.4% | 4.3% | 4.7%/4.0% | 8.9 (interpolated) | pass | 0.018 (unverified) | 0.66 |
| 5 | `cfg_5eb7` | 15min | 40/40 | 0.0 | 3 | 2 | sma200 | 164 | 10.4% | 2.0% | 0.79 | -2.6% | 293 | 1.46 | 30.8% | 28.0 | 9/9 | 0.89 | 0.66 | 0.12 | 4 | 5.3% | 0.47 | 0.63 | 9.5% | 8.7% | 6.1% | 9.1%/7.5% | 7.2 (interpolated) | pass | 0.008 (unverified) | 0.62 |
| 6 | `cfg_8b29` | 15min | 55/55 | 0.1 | off | 1 | ema200 | 150 | 6.1% | 1.2% | 0.93 | -1.2% | 191 | 1.62 | 50.1% | 9.4 | 9/9 | 1.00 | 0.65 | 0.29 | 5 | 4.0% | 0.33 | 0.69 | 5.8% | 5.5% | 4.6% | 5.5%/4.9% | 12.2 (interpolated) | pass | 0.024 (unverified) | 0.99 |
| 7 | `cfg_3e76` | 15min | 40/20 | 0.1 | off | 2 | sma200 | 162 | 5.2% | 1.0% | 0.89 | -1.1% | 392 | 1.61 | 19.6% | 17.3 | 10/10 | 0.90 | 0.65 | 0.24 | 4 | 3.4% | 0.35 | 0.74 | 4.7% | 4.2% | 4.4% | 4.9%/3.8% | 6.3 (interpolated) | pass | 0.013 (unverified) | 0.44 |
| 8 | `cfg_55d3` | 15min | 40/40 | 0.1 | 2 | 1 | ema200 | 262 | 18.4% | 3.4% | 0.81 | -3.5% | 217 | 1.37 | 39.7% | 65.1 | 10/10 | 1.00 | 0.62 | 0.19 | 5 | 12.8% | 0.27 | 0.66 | 16.3% | 14.2% | 17.9% | 16.4%/12.8% | 5.5 (interpolated) | pass | 0.012 (unverified) | 0.47 |
| 9 | `cfg_0e38` | 15min | 55/13 | 0.1 | off | 2 | ema100 | 183 | 5.4% | 1.0% | 0.92 | -1.5% | 294 | 1.60 | 14.8% | 22.5 | 9/9 | 0.78 | 0.60 | 0.32 | 4 | 3.4% | 0.36 | 0.56 | 4.7% | 4.1% | 4.6% | 4.8%/3.7% | 5.2 (interpolated) | pass | 0.013 (unverified) | 0.10 |
| 10 | `cfg_3972` | 15min | 30/15 | 0.1 | off | 2 | ema100 | 221 | 5.9% | 1.2% | 0.95 | -1.9% | 510 | 1.52 | 20.1% | 25.0 | 10/10 | 0.80 | 0.58 | 0.37 | 4 | 4.0% | 0.31 | 0.51 | 5.3% | 4.5% | 5.3% | 5.6%/4.4% | 5.2 (interpolated) | pass | 0.018 (unverified) | 0.61 |
| 11 | `cfg_0ad3` | 15min | 55/27 | 0.0 | off | 2 | sma200 | 153 | 4.4% | 0.9% | 0.81 | -1.0% | 396 | 1.51 | 27.1% | 12.3 | 9/9 | 0.78 | 0.57 | 0.24 | 4 | 2.3% | 0.46 | 0.71 | 4.1% | 3.7% | 3.5% | 4.1%/3.4% | 7.3 (interpolated) | pass | 0.009 (unverified) | 0.62 |
| 12 | `cfg_2d12` | 15min | 55/27 | 0.0 | off | 1 | ema100 | 243 | 6.4% | 1.2% | 0.76 | -1.3% | 288 | 1.35 | 39.5% | 22.5 | 9/9 | 1.00 | 0.54 | 0.23 | 4 | 3.7% | 0.41 | 0.77 | 5.8% | 5.1% | 6.1% | 6.1%/5.1% | 6.0 (interpolated) | pass | 0.007 (unverified) | 0.85 |
| 13 | `cfg_2cab` | 1h | 15/7 | 0.0 | off | 1 | sma50 | 215 | 6.5% | 1.3% | 0.82 | -1.6% | 518 | 1.42 | 35.8% | 20.9 | 8/8 | 0.88 | 0.54 | 0.28 | 4 | 3.3% | 0.48 | 0.89 | 5.9% | 5.3% | 6.1% | 6.1%/4.9% | 6.4 (interpolated) | pass | 0.015 (unverified) | 0.68 |
| 14 | `cfg_5367` | 5min | 55/55 | 0.5 | off | 1 | ema50 | 443 | 11.0% | 2.1% | 0.83 | -3.0% | 277 | 1.28 | 44.1% | 55.2 | 7/7 | 0.86 | 0.44 | 0.39 | 4 | 6.7% | 0.39 | 0.72 | 9.4% | 7.8% | 10.1% | 10.6%/8.4% | 4.4 (interpolated) | pass | 0.010 (unverified) | 0.74 |
| 15 | `cfg_34e6` | 15min | 30/15 | 0.1 | off | 2 | sma200 | 189 | 5.8% | 1.1% | 0.99 | -1.6% | 515 | 1.63 | 17.4% | 23.1 | 10/10 | 0.80 | 0.43 | 0.55 | 4 | 3.5% | 0.38 | 0.47 | 5.1% | 4.5% | 5.6% | 5.5%/4.7% | 5.4 (interpolated) | pass | 0.020 (unverified) | 0.61 |
| 16 | `cfg_9861` | 15min | 30/15 | 0.25 | off | 1 | ema100 | 379 | 8.2% | 1.6% | 0.77 | -2.3% | 191 | 1.30 | 32.2% | 48.9 | 10/10 | 0.80 | 0.39 | 0.38 | 5 | 6.0% | 0.26 | 0.73 | 6.8% | 5.4% | 5.9% | 7.8%/5.8% | 3.9 (interpolated) | pass | 0.006 (unverified) | 0.55 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 4.8% / 1.57 / 38 | 1.1% / 0.35 / 57 | 2.3% / 0.67 / 51 | 3.1% / 1.00 / 49 | 1.0% / 0.35 / 41 |
| 2 | 5.3% / 1.74 / 45 | 2.4% / 0.74 / 63 | 3.3% / 0.98 / 57 | -0.5% / -0.13 / 63 | 1.6% / 0.57 / 44 |
| 3 | 4.0% / 1.15 / 32 | 1.9% / 0.63 / 42 | 2.0% / 0.53 / 43 | 4.3% / 1.40 / 36 | 1.0% / 0.37 / 32 |
| 4 | 1.6% / 1.61 / 26 | 0.4% / 0.36 / 33 | 0.9% / 0.71 / 32 | 1.8% / 1.64 / 32 | 0.3% / 0.25 / 28 |
| 5 | 4.8% / 1.92 / 24 | -0.0% / 0.00 / 35 | 1.4% / 0.52 / 38 | 3.6% / 1.42 / 36 | 0.2% / 0.09 / 31 |
| 6 | 0.9% / 0.84 / 28 | 0.8% / 0.67 / 34 | 2.0% / 1.34 / 30 | 1.8% / 1.40 / 30 | 0.4% / 0.34 / 28 |
| 7 | 1.6% / 1.48 / 26 | -0.3% / -0.33 / 38 | 1.5% / 1.16 / 31 | 1.8% / 1.37 / 42 | 0.6% / 0.51 / 25 |
| 8 | 5.0% / 1.31 / 42 | 1.8% / 0.44 / 62 | 4.0% / 0.84 / 57 | 4.2% / 0.95 / 58 | 2.3% / 0.59 / 43 |
| 9 | 1.9% / 1.82 / 32 | -0.3% / -0.38 / 39 | 1.1% / 1.01 / 34 | 1.5% / 1.09 / 46 | 1.0% / 0.81 / 32 |
| 10 | 1.9% / 1.54 / 43 | -0.5% / -0.53 / 45 | 1.5% / 1.15 / 43 | 1.3% / 1.05 / 53 | 1.6% / 1.22 / 37 |
| 11 | 2.0% / 2.09 / 23 | -0.4% / -0.43 / 36 | 0.7% / 0.58 / 34 | 1.9% / 1.51 / 34 | 0.2% / 0.16 / 26 |
| 12 | 2.6% / 1.69 / 42 | 0.8% / 0.51 / 52 | 1.2% / 0.72 / 54 | 2.3% / 1.24 / 49 | -0.7% / -0.48 / 46 |
| 13 | 3.1% / 2.02 / 32 | -0.6% / -0.43 / 51 | 1.0% / 0.69 / 49 | 2.9% / 1.48 / 47 | 0.0% / 0.01 / 36 |
| 14 | 3.4% / 1.46 / 84 | 1.7% / 0.62 / 94 | 4.1% / 1.35 / 91 | 2.9% / 1.18 / 92 | -1.4% / -0.58 / 82 |
| 15 | 1.9% / 1.75 / 34 | -0.7% / -0.74 / 43 | 1.1% / 0.91 / 38 | 2.2% / 1.61 / 47 | 1.3% / 1.07 / 27 |
| 16 | 1.7% / 0.99 / 69 | 2.0% / 0.92 / 78 | 1.8% / 0.77 / 86 | 2.0% / 1.00 / 82 | 0.4% / 0.21 / 64 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_2cab` | 2 | 0.99 | 0.99/0.99 | 1.00/1.00 |
| 1 | `cfg_d367` | 28 | 0.84 | 0.80/0.87 | 0.80/0.88 |
| 2 | `cfg_0e38` | 14 | 0.84 | 0.89/0.92 | 0.76/0.81 |
| 3 | `cfg_0ad3` | 7 | 0.95 | 0.95/0.95 | 0.94/0.94 |
| 4 | `cfg_34cb` | 6 | 0.97 | 0.97/0.97 | 0.97/0.97 |
| 5 | `cfg_5eb7` | 16 | 0.83 | 0.78/0.89 | 0.76/0.84 |
| 6 | `cfg_cd00` | 3 | 0.87 | 0.92/0.95 | 0.89/0.93 |
| 7 | `cfg_34e6` | 2 | 0.93 | 0.96/0.96 | 0.93/0.93 |
| 8 | `cfg_8b29` | 4 | 0.91 | 0.94/0.96 | 0.94/0.97 |
| 9 | `cfg_2d12` | 2 | 0.93 | 0.96/0.96 | 0.96/0.96 |
| 10 | `cfg_2f28` | 9 | 0.82 | 0.90/0.93 | 0.87/0.90 |
| 11 | `cfg_3972` | 7 | 0.88 | 0.90/0.98 | 0.91/0.98 |
| 12 | `cfg_3e76` | 8 | 0.87 | 0.90/0.94 | 0.84/0.88 |
| 13 | `cfg_55d3` | 14 | 0.80 | 0.85/0.93 | 0.81/0.88 |
| 14 | `cfg_5367` | 3 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 15 | `cfg_9861` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.286e-03 over 24576 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 996.0, participation ratio 6.8, 95%-variance components 195 (rank bound T = 1259); raw grid 24576; raw + known prior 28464
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the 24,576-config development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
QQQ results are unchanged rules on the development period: supporting evidence, not an independent replication.

## Integrity audit

- Signal at bar i uses the channel of bars < i (rolling max shifted by 1) and bar i's close; entry fills at bar i+1's open.
- FIXED (this revision): initial ATR stop / sizing used the ENTRY bar's ATR (look-ahead); now uses the last ATR known before the fill.
- FIXED (this revision): stop was first checked on the bar AFTER entry; it is now live on the entry bar (conservative).
- FIXED (this revision): a 'missed entry' re-entered on the next signal bar; it now skips the whole breakout episode.
- Gaps through the stop fill at the worse open; adverse slippage + commission on every fill.
- No profit target exists, so no bar can touch both stop and target; checked per trade.
- Development backtests run on data physically truncated at the development end; open positions are force-closed at the last development bar and flagged (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Positions are held overnight (no session-end flattening) by strategy design; overnight gaps are captured by the gap-fill rule.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Unresolved assumptions

- Drawdown limit -30% is reused from src/experiments/validation.py; it has not been separately approved as a risk limit for this strategy.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0: Sharpe vs. cash is overstated in high-rate years (2023-2024 ~5%).
- Variable cost stress scales per-share commission and slippage bps; the $1 per-order minimum commission is treated as fixed.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Neighbor lattice treats timeframe and init_stop (1.5 < 2 < 3 < off) as ordered axes; trend_filter is held fixed (categorical).
