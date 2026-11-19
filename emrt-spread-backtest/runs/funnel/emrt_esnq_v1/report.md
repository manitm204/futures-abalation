# Screening funnel -- emrt_esnq_v1 (development stages only)

- Code: `66e9a379b8f4` (dirty working tree: False, diff sha256 `e3b0c44298fc`)
- Config: `configs/funnel/emrt_funnel_esnq_v1.yaml` sha256 `ad7823c33d8c8f6e`; seed 20261118
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ES': '2026-10-16', 'NQ': '2026-10-16', 'RTY': '2026-10-16'}
- Frozen manifest sha256: `a6facfb4a35ca5b5` (16 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No pair strategy has been scored on ES-NQ 2023-2024, but mean-reversion, noise-band, squeeze and convexity strategies were selected on ES and NQ 2023-2024 and the researcher has read those results. Treated as used for selection.
- Holdout 2025+ previously inspected: **True** -- No EMRT or other pair metrics have been computed on 2025+. Single-instrument picks were scored on ES 2025+ (BB/KC squeeze, convexity v2 #115) and NQ 2025+ (convexity v3 #38 and #32), so the researcher has seen how both legs traded in that period.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 51840 | 51840 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 51840 | 51840 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 51840 | 20401 | 31439 | 0 |  | 16436 | 39.35 | 39.35 |  |
| 3 performance & risk | hard_gate | 20401 | 32 | 20369 | 0 |  | 0 | 0.06 | 0.16 |  |
| 4 parameter stability | hard_gate | 32 | 23 | 9 | 0 |  | 0 | 0.04 | 71.88 |  |
| 5 time stability | hard_gate | 23 | 23 | 0 | 0 |  | 22 | 0.04 | 100.00 |  |
| 6 deduplication | dedup | 23 | 16 |  |  | 7 |  | 0.03 | 69.57 | best 2 per cluster |
| 7 execution stress | hard_gate | 16 | 16 | 0 | 0 |  | 0 | 0.03 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 16 |  |  |  |  |  |  |  | diagnostic only: unverified: 16 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 30294 |
| s2:hard_reject:years_with_>=10_trades | 24026 |
| s3:hard_reject:net_return | 17502 |
| s3:hard_reject:sharpe | 20369 |
| s4:hard_reject:local_median_sharpe | 9 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES-RTY dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_403d` | timeframe=15min, formation=3, hedge=notional, z_mode=rolling_250, entry_z=2.0, exit=half, stop=1.5, time_stop=3emrt, side=both, overnight=hold | 0/0/18 | 197 | 12.0% | 2.3% | 0.89 | -4.3% | 218 | 1.60 | 32.1% | 77.9 | 5/5 | 0.80 | 0.59 | 0.30 | 5 | 8.1% | 0.31 | 0.32 | 10.8% | 9.2% | 10.5% | 11.6%/10.2% | 5.6 (interpolated) | pass | 0.045 (unverified) | -0.25 |
| 2 | `cfg_c126` | timeframe=30min, formation=3, hedge=emrt_c1.5, z_mode=rolling_100, entry_z=2.5, exit=half, stop=2.5, time_stop=3emrt, side=both, overnight=hold | 1/0/0 | 112 | 8.3% | 1.6% | 0.88 | -4.2% | 519 | 1.78 | 14.7% | 44.2 | 6/6 | 0.83 | 0.42 | 0.46 | 4 | 4.5% | 0.43 | 0.48 | 7.4% | 6.5% | 7.0% | 7.8%/6.5% | 6.2 (interpolated) | pass | 0.041 (unverified) | 0.23 |
| 3 | `cfg_e6c1` | timeframe=15min, formation=6, hedge=notional, z_mode=rolling_250, entry_z=2.0, exit=half, stop=1.5, time_stop=3emrt, side=both, overnight=hold | 0/0/18 | 186 | 11.5% | 2.2% | 0.87 | -4.3% | 218 | 1.60 | 29.7% | 73.7 | 6/6 | 0.83 | 0.56 | 0.31 | 5 | 7.7% | 0.32 | 0.33 | 10.2% | 8.9% | 9.7% | 11.2%/10.2% | 5.7 (interpolated) | pass | 0.042 (unverified) | -0.28 |
| 4 | `cfg_f3a7` | timeframe=15min, formation=3, hedge=ols, z_mode=rolling_250, entry_z=2.0, exit=half, stop=1.5, time_stop=3emrt, side=short, overnight=hold | 0/0/13 | 104 | 6.1% | 1.2% | 0.87 | -1.8% | 300 | 1.72 | 15.0% | 41.0 | 5/5 | 1.00 | 0.58 | 0.29 | 3 | 2.3% | 0.63 | 0.50 | 5.4% | 4.7% | 6.6% | 5.7%/4.8% | 5.3 (interpolated) | pass | 0.040 (unverified) | -0.81 |
| 5 | `cfg_cf93` | timeframe=30min, formation=3, hedge=emrt_c1.5, z_mode=rolling_100, entry_z=2.5, exit=mean, stop=2.5, time_stop=3emrt, side=both, overnight=hold | 22/0/0 | 101 | 12.4% | 2.4% | 0.88 | -3.4% | 170 | 1.80 | 31.8% | 39.7 | 6/6 | 0.67 | 0.57 | 0.31 | 4 | 5.7% | 0.51 | 0.41 | 11.6% | 10.9% | 11.1% | 11.6%/9.9% | 9.1 (interpolated) | pass | 0.039 (unverified) | 0.07 |
| 6 | `cfg_942f` | timeframe=15min, formation=3, hedge=ols, z_mode=rolling_250, entry_z=2.0, exit=half, stop=1.5, time_stop=none, side=short, overnight=hold | 0/0/13 | 104 | 6.1% | 1.2% | 0.87 | -1.8% | 300 | 1.72 | 15.0% | 41.0 | 5/5 | 1.00 | 0.58 | 0.29 | 3 | 2.3% | 0.63 | 0.50 | 5.4% | 4.7% | 6.6% | 5.6%/4.8% | 5.3 (interpolated) | pass | 0.040 (unverified) | -0.76 |
| 7 | `cfg_c1d8` | timeframe=15min, formation=3, hedge=emrt_c1.5, z_mode=rolling_250, entry_z=1.5, exit=half, stop=1.5, time_stop=none, side=short, overnight=hold | 0/0/23 | 148 | 8.1% | 1.6% | 0.81 | -3.1% | 311 | 1.67 | 20.5% | 58.4 | 5/5 | 0.80 | 0.65 | 0.16 | 4 | 3.8% | 0.52 | 0.38 | 6.8% | 5.6% | 7.8% | 7.7%/6.5% | 4.9 (interpolated) | pass | 0.030 (unverified) | -0.67 |
| 8 | `cfg_665c` | timeframe=30min, formation=3, hedge=emrt_c1.5, z_mode=rolling_100, entry_z=2.5, exit=mean, stop=1.5, time_stop=3emrt, side=both, overnight=hold | 21/0/5 | 102 | 10.2% | 2.0% | 0.76 | -3.3% | 215 | 1.67 | 30.6% | 40.2 | 5/5 | 0.80 | 0.58 | 0.18 | 4 | 3.5% | 0.63 | 0.41 | 9.3% | 8.6% | 10.3% | 9.5%/7.6% | 7.5 (interpolated) | pass | 0.022 (unverified) | 0.06 |
| 9 | `cfg_0f30` | timeframe=15min, formation=3, hedge=emrt_c1.5, z_mode=rolling_250, entry_z=2.5, exit=half, stop=1.5, time_stop=none, side=both, overnight=hold | 0/0/8 | 117 | 8.1% | 1.6% | 0.82 | -2.8% | 535 | 1.73 | 15.5% | 46.1 | 4/4 | 1.00 | 0.71 | 0.11 | 4 | 4.4% | 0.46 | 0.54 | 7.1% | 6.2% | 7.9% | 8.1%/6.4% | 5.9 (interpolated) | pass | 0.027 (unverified) | 0.26 |
| 10 | `cfg_4748` | timeframe=15min, formation=3, hedge=emrt_c1.5, z_mode=rolling_250, entry_z=2.5, exit=half, stop=1.5, time_stop=3emrt, side=both, overnight=hold | 3/0/8 | 118 | 7.5% | 1.5% | 0.78 | -3.1% | 541 | 1.65 | 15.2% | 46.5 | 4/4 | 1.00 | 0.68 | 0.10 | 4 | 4.1% | 0.45 | 0.58 | 6.5% | 5.7% | 7.2% | 7.4%/6.4% | 5.6 (interpolated) | pass | 0.023 (unverified) | 0.25 |
| 11 | `cfg_42b0` | timeframe=15min, formation=3, hedge=emrt_c1.5, z_mode=rolling_250, entry_z=2.0, exit=half, stop=none, time_stop=none, side=both, overnight=hold | 0/0/0 | 181 | 9.2% | 1.8% | 0.76 | -3.6% | 433 | 1.57 | 30.0% | 71.4 | 5/5 | 1.00 | 0.59 | 0.18 | 4 | 4.2% | 0.53 | 0.29 | 7.9% | 6.8% | 9.5% | 9.2%/7.8% | 4.4 (interpolated) | pass | 0.025 (unverified) | -0.33 |
| 12 | `cfg_1d8e` | timeframe=15min, formation=3, hedge=emrt_c1.5, z_mode=rolling_250, entry_z=2.0, exit=half, stop=none, time_stop=3emrt, side=both, overnight=hold | 6/0/0 | 183 | 9.1% | 1.8% | 0.76 | -3.6% | 433 | 1.54 | 29.6% | 72.2 | 5/5 | 1.00 | 0.50 | 0.26 | 4 | 4.0% | 0.54 | 0.31 | 7.8% | 6.7% | 9.4% | 8.9%/7.9% | 4.4 (interpolated) | pass | 0.024 (unverified) | -0.37 |
| 13 | `cfg_3c18` | timeframe=30min, formation=3, hedge=emrt_c1.5, z_mode=rolling_100, entry_z=2.5, exit=half, stop=none, time_stop=3emrt, side=both, overnight=hold | 1/0/0 | 112 | 8.3% | 1.6% | 0.88 | -4.2% | 519 | 1.78 | 14.7% | 44.2 | 5/5 | 0.80 | 0.24 | 0.64 | 4 | 4.5% | 0.43 | 0.48 | 7.4% | 6.5% | 7.0% | 7.6%/6.2% | 6.2 (interpolated) | pass | 0.041 (unverified) | 0.25 |
| 14 | `cfg_8f80` | timeframe=15min, formation=6, hedge=emrt_c1.5, z_mode=rolling_250, entry_z=1.5, exit=half, stop=2.5, time_stop=3emrt, side=short, overnight=hold | 0/0/6 | 120 | 6.5% | 1.3% | 0.76 | -2.5% | 320 | 1.74 | 18.8% | 47.3 | 7/7 | 0.71 | 0.22 | 0.55 | 4 | 3.3% | 0.49 | 0.40 | 5.8% | 4.9% | 6.6% | 6.2%/5.5% | 5.2 (interpolated) | pass | 0.025 (unverified) | -0.80 |
| 15 | `cfg_e0e0` | timeframe=1h, formation=3, hedge=emrt_c1.5, z_mode=rolling_250, entry_z=1.5, exit=half, stop=1.5, time_stop=3emrt, side=both, overnight=hold | 26/0/13 | 102 | 10.6% | 2.0% | 0.75 | -6.0% | 407 | 1.53 | 31.8% | 40.3 | 5/5 | 0.60 | 0.27 | 0.49 | 4 | 2.0% | 0.79 | 0.58 | 9.7% | 9.0% | 7.9% | 10.0%/8.8% | 7.7 (interpolated) | pass | 0.021 (unverified) | 0.37 |
| 16 | `cfg_cc2f` | timeframe=15min, formation=6, hedge=emrt_c1.5, z_mode=rolling_250, entry_z=1.5, exit=half, stop=1.5, time_stop=3emrt, side=short, overnight=hold | 0/0/22 | 129 | 6.8% | 1.3% | 0.90 | -2.0% | 456 | 1.73 | 16.4% | 50.9 | 6/6 | 0.67 | 0.35 | 0.56 | 3 | 3.2% | 0.52 | 0.40 | 5.8% | 4.9% | 6.9% | 6.2%/5.5% | 4.9 (interpolated) | pass | 0.052 (unverified) | -0.79 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 1.0% / 0.54 / 30 | 1.3% / 0.95 / 40 | 2.6% / 0.72 / 33 | 3.6% / 1.33 / 47 | 3.1% / 1.06 / 47 |
| 2 | 3.6% / 1.95 / 21 | 1.8% / 2.38 / 28 | -2.4% / -0.99 / 19 | 2.0% / 1.09 / 23 | 3.0% / 1.56 / 21 |
| 3 | 0.6% / 0.38 / 19 | 1.3% / 0.95 / 40 | 2.6% / 0.73 / 33 | 3.5% / 1.32 / 47 | 3.1% / 1.06 / 47 |
| 4 | 1.7% / 1.42 / 18 | 1.1% / 1.34 / 25 | 3.7% / 2.51 / 14 | -0.2% / -0.08 / 26 | -0.3% / -0.21 / 21 |
| 5 | 6.4% / 2.10 / 20 | 2.9% / 2.11 / 25 | 1.8% / 0.58 / 19 | 3.4% / 1.16 / 20 | -2.4% / -0.87 / 17 |
| 6 | 1.7% / 1.42 / 18 | 1.1% / 1.34 / 25 | 3.7% / 2.51 / 14 | -0.2% / -0.08 / 26 | -0.3% / -0.21 / 21 |
| 7 | 0.9% / 0.44 / 24 | 1.1% / 1.08 / 34 | 4.1% / 2.32 / 22 | -1.1% / -0.42 / 34 | 2.9% / 1.49 / 34 |
| 8 | 6.5% / 2.15 / 20 | 2.9% / 2.11 / 25 | 1.6% / 0.51 / 19 | 1.4% / 0.55 / 21 | -2.3% / -0.83 / 17 |
| 9 | 2.9% / 1.51 / 20 | 1.8% / 1.99 / 27 | -1.0% / -0.42 / 15 | 0.6% / 0.33 / 26 | 3.5% / 1.45 / 29 |
| 10 | 2.9% / 1.51 / 20 | 1.8% / 1.99 / 27 | -1.2% / -0.58 / 16 | 0.5% / 0.32 / 26 | 3.3% / 1.38 / 29 |
| 11 | 4.9% / 1.95 / 33 | 2.3% / 1.80 / 44 | -0.9% / -0.30 / 25 | 1.7% / 0.69 / 40 | 1.0% / 0.45 / 39 |
| 12 | 4.9% / 1.95 / 33 | 2.2% / 1.74 / 44 | -0.9% / -0.31 / 27 | 1.7% / 0.68 / 40 | 1.0% / 0.45 / 39 |
| 13 | 3.6% / 1.95 / 21 | 1.8% / 2.38 / 28 | -2.4% / -0.99 / 19 | 2.0% / 1.09 / 23 | 3.0% / 1.56 / 21 |
| 14 | 1.5% / 1.20 / 16 | 0.1% / 0.13 / 30 | 3.1% / 2.00 / 13 | -0.7% / -0.32 / 30 | 2.4% / 1.19 / 31 |
| 15 | 8.4% / 2.70 / 24 | 2.0% / 1.29 / 26 | 0.6% / 0.24 / 15 | -3.8% / -1.22 / 19 | 3.4% / 1.14 / 18 |
| 16 | 1.4% / 1.16 / 16 | -0.3% / -0.30 / 32 | 3.5% / 2.49 / 14 | -0.3% / -0.17 / 33 | 2.3% / 1.22 / 34 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_403d` | 7 | 0.91 | 0.94/0.97 | 0.85/0.92 |
| 1 | `cfg_cf93` | 3 | 0.96 | 0.97/0.98 | 0.97/0.98 |
| 2 | `cfg_0f30` | 2 | 0.99 | 0.98/0.98 | 0.98/0.98 |
| 3 | `cfg_42b0` | 2 | 1.00 | 0.99/0.99 | 0.99/0.99 |
| 4 | `cfg_c126` | 3 | 1.00 | 1.00/1.00 | 0.99/0.99 |
| 5 | `cfg_8f80` | 2 | 0.96 | 0.91/0.91 | 0.89/0.89 |
| 6 | `cfg_f3a7` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 7 | `cfg_c1d8` | 1 | n/a | n/a/n/a | n/a/n/a |
| 8 | `cfg_e0e0` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 9.505e-04 over 51840 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1587.0, participation ratio 50.9, 95%-variance components 456 (rank bound T = 1259); raw grid 51840; raw + known prior 2108052
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
ES-RTY results are unchanged rules on the development period: supporting evidence, not an independent replication.

## Integrity audit

- Pair data: both legs' day-session bars of one timeframe, inner-joined on bar open time (a bar missing in either leg is dropped from both); leg A is the pair's first symbol.
- Hedge refit at each calendar-month start on the bars of the previous `formation` months only (strictly before the trading month; a month is fit only when the data reaches back to its start). Spread S = (A - A0)/RA - beta (B - B0)/RB on closes, anchors at the last formation bar (A0 adjusted close, RA raw close): per $1 of A, short $beta of B.
- Hedges: emrt_cC = the beta in 0.20..3.00 (step 0.01) minimising the empirical mean-reversion time (mean bars from each important extremum at C x sd back to the formation mean; zigzag pivots, the first dropped; never-reverting extrema censored at the window end; >= 4 extrema), subject to var(S) <= 2 x var(S at the OLS beta); ols = formation OLS slope of a on b clipped to 0.20..3.00 (CONTROL); notional = 1 (CONTROL).
- z_k under bar k's month hedge: formation = (S_k - formation mean) / formation sd; rolling_W = (S_k - mean) / sd of the last W bars' S (population, same beta / anchors). z_prev_k is bar k-1 under bar k's month hedge.
- Decision at bar k's close: long spread (long A, short B) on a fresh cross z_k <= -entry_z, short spread on z_k >= entry_z; side filter; no decision on the session's last bar or less than 30 minutes before its last close. A signal while a position is open is dropped, never queued.
- Entry fills both legs at the NEXT bar's open with market slippage; the fill bar must be in the decision's session. The open position keeps its ENTRY month's hedge and z definition for its exits, even after a refit.
- Exits from the entry bar's close on: target z back to 0 (mean) or inside -/+ entry_z/2 (half); stop |z| >= entry_z + stop against the position; both decided at a close and filled at the next bar's open (stop slippage for stops) -- with overnight = hold that can be the next session's open. Time stop (3emrt): closed at the close of bar entry + ceil(3 x EMRT of the entry month's spread) - 1. overnight = flat: closed at the session's last close. The data's last bar closes at its close (forced, not a completed trade).
- P&L = side x qa x multA x (A exit - A entry) - side x qb x multB x (B exit - B entry) - commissions - roll costs; with overnight = hold, each roll of a leg's contract while open costs that leg a round turn (2 x (commission + 1 tick) per contract).
- Sizing: whole contracts, unlevered: gross notional of both legs (raw price x multiplier) + entry commissions <= equity; qa = floor(equity / (VA (1 + beta))), qb = round(qa VA beta / VB), reduced until it fits; >= 1 contract per leg. Starting equity $10M so the ratio is carried by tens of contracts, not a handful.
- Development backtests run on data physically truncated at the development end; a trade still open there is closed at the last development bar and flagged forced (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0) per leg, built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted per leg; the spread uses only differences of adjusted prices (real point moves) scaled by raw anchor prices, so back-adjustment does not distort it. Rolls of the two legs need not coincide.
- Session: each leg's day session (src/data/futures.py SESSIONS); both legs of every pair here share one session (index futures 09:30-16:00 NY, Treasuries 08:20-15:00 NY).
- Costs: per leg, slippage in ticks per side (stops too) plus commission per contract per side, from the execution YAML; cost stress scales both on both legs (and the roll costs).

## Unresolved assumptions

- Drawdown limit -30% is reused from the single-instrument funnels; it was not separately approved for an unlevered, market-neutral pair.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. A real futures account keeps the margin-free cash in T-bills.
- Unlevered gross sizing makes the spread's returns small: a market-neutral book would normally run levered. Sharpe is unaffected by the leverage choice; net return and drawdown scale with it.
- The paper fits on DAILY closes of stock pairs with one formation year; every bar size here is intraday and the pairs are index / Treasury futures, so the whole grid is extrapolation of the paper. Its reinforcement-learning trading layer is not used (a sigma band trades the spread).
- Important extrema are found with a zigzag at C x sd (first pivot dropped), an equivalent construction of the paper's definition; the paper does not say how extrema it never returns from are scored -- here they are censored at the window end.
- The paper's variance cap M is not given numerically; here var(S) <= 2 x var(S at the OLS beta).
- Entry decisions use bar closes of both legs, which are not exactly simultaneous prints; fills at the next bar's open on both legs assume both can be traded at that open.
- A rolling z window spans sessions over day-session bars, so the overnight gap of the spread enters it.
- COVID (March-April 2020) falls inside the development period and inside formation windows of the following months.
