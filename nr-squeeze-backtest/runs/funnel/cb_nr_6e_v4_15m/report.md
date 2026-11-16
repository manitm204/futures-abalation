# Screening funnel -- cb_nr_6e_v4_15m (development stages only)

- Code: `278b87465dd4` (dirty working tree: True, diff sha256 `234dce23ae0e`)
- Config: `configs/funnel/cb_nr_funnel_6e_v4_15m.yaml` sha256 `b2e79935edd7247e`; seed 20261121
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ES': '2026-10-16', '6E': '2026-10-16'}
- Frozen manifest sha256: `9c6aa085282a4f28` (14 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- 6E 2023-2024 was used to select BB/KC squeeze strategies (cb_bbkc_6e_v4_15m) and mean-reversion strategies; no NR-N strategy has been selected on 6E. This grid was chosen after reading NR v2/v3 on ES; it was run on 6E after its NQ / YM / RTY / CL v4 results were seen.
- Holdout 2025+ previously inspected: **False** -- No compression-breakout or other-family holdout metrics have been computed on 6E 2025+ per the data-access ledgers.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 2304 | 2304 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 2304 | 792 | 1512 | 0 |  | 0 | 34.38 | 34.38 |  |
| 2 trade count & coverage | hard_gate | 792 | 696 | 96 | 0 |  | 693 | 30.21 | 87.88 |  |
| 3 performance & risk | hard_gate | 696 | 62 | 634 | 0 |  | 0 | 2.69 | 8.91 |  |
| 4 parameter stability | hard_gate | 62 | 60 | 2 | 0 |  | 30 | 2.60 | 96.77 |  |
| 5 time stability | hard_gate | 60 | 60 | 0 | 0 |  | 55 | 2.60 | 100.00 |  |
| 6 deduplication | dedup | 60 | 14 |  |  | 46 |  | 0.61 | 23.33 | best 2 per cluster |
| 7 execution stress | hard_gate | 14 | 14 | 0 | 0 |  | 10 | 0.61 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 14 |  |  |  |  |  |  |  | diagnostic only: unverified: 14 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s1:hard_reject:integrity:box_not_from_prior_compression_run | 1512 |
| s1:hard_reject:integrity:entry_fill_better_than_market | 1416 |
| s1:hard_reject:integrity:entry_signal_condition_not_met | 1024 |
| s1:hard_reject:integrity:eod_exit_not_at_session_close | 226 |
| s1:hard_reject:integrity:exit_not_at_first_touch | 338 |
| s1:hard_reject:integrity:not_first_breakout_of_run | 1128 |
| s1:hard_reject:integrity:stop_exit_without_touch | 444 |
| s1:hard_reject:integrity:stop_fill_better_than_rule | 474 |
| s1:hard_reject:integrity:stop_not_per_rule | 1444 |
| s1:hard_reject:integrity:target_not_per_rule | 1086 |
| s1:hard_reject:integrity:target_taken_when_stop_touched | 8 |
| s2:hard_reject:completed_trades | 96 |
| s2:hard_reject:years_with_>=10_trades | 24 |
| s3:hard_reject:net_return | 342 |
| s3:hard_reject:sharpe | 634 |
| s4:hard_reject:local_frac_profitable | 2 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | target/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_c252` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 95/295/49 | 439 | 5.1% | 1.0% | 1.12 | -1.1% | 368 | 1.40 | 8.8% | 180.6 | 4/4 | 1.00 | 1.04 | 0.08 | 3 | 2.7% | 0.48 | 0.36 | 2.5% | -0.1% | -2.0% | 4.7%/3.9% | 2.0 (interpolated) | pass | 0.025 (unverified) | 0.69 |
| 2 | `cfg_73f5` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=3.5, direction=both, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 4/374/52 | 430 | 5.2% | 1.0% | 1.04 | -1.7% | 337 | 1.39 | 10.4% | 177.5 | 5/5 | 0.80 | 0.99 | 0.05 | 4 | 3.0% | 0.43 | 0.49 | 2.6% | 0.2% | -1.8% | 4.7%/3.9% | 2.0 (interpolated) | pass | 0.017 (unverified) | 0.50 |
| 3 | `cfg_6d2b` | timeframe=15min, compression=nr, nr_lookback=3, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 85/257/44 | 386 | 4.3% | 0.8% | 1.01 | -0.9% | 384 | 1.38 | 7.8% | 158.4 | 5/5 | 1.00 | 0.97 | 0.04 | 3 | 2.3% | 0.46 | 0.38 | 2.1% | -0.2% | -2.1% | 3.8%/3.2% | 2.0 (interpolated) | pass | 0.015 (unverified) | 0.72 |
| 4 | `cfg_baa9` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=none, direction=both, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 0/376/51 | 427 | 5.5% | 1.1% | 1.07 | -1.7% | 337 | 1.41 | 10.5% | 176.5 | 4/4 | 1.00 | 1.00 | 0.07 | 4 | 3.2% | 0.41 | 0.50 | 2.9% | 0.5% | -1.4% | 5.0%/4.0% | 2.1 (interpolated) | pass | 0.018 (unverified) | 0.47 |
| 5 | `cfg_be78` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 176/185/94 | 455 | 3.8% | 0.7% | 1.05 | -0.8% | 207 | 1.32 | 6.9% | 187.4 | 4/4 | 1.00 | 0.91 | 0.14 | 4 | 2.0% | 0.46 | 0.31 | 1.2% | -1.5% | -2.5% | 3.5%/2.9% | 1.7 (interpolated) | pass | 0.021 (unverified) | -0.10 |
| 6 | `cfg_c65a` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 162/172/88 | 422 | 3.6% | 0.7% | 1.02 | -0.8% | 207 | 1.32 | 6.5% | 173.4 | 4/4 | 1.00 | 0.87 | 0.15 | 4 | 1.6% | 0.56 | 0.33 | 1.1% | -1.4% | -2.5% | 3.1%/2.5% | 1.7 (interpolated) | pass | 0.018 (unverified) | -0.12 |
| 7 | `cfg_1b6d` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 33/95/12 | 140 | 2.4% | 0.5% | 1.01 | -0.4% | 328 | 1.66 | 2.8% | 56.9 | 5/5 | 1.00 | 0.66 | 0.35 | 4 | 1.3% | 0.43 | 0.47 | 1.5% | 0.7% | 0.4% | 2.1%/1.6% | 2.5 (interpolated) | pass | 0.015 (unverified) | 0.15 |
| 8 | `cfg_1990` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 36/107/16 | 159 | 2.4% | 0.5% | 0.96 | -0.5% | 328 | 1.57 | 3.1% | 64.7 | 5/5 | 1.00 | 0.62 | 0.34 | 4 | 1.4% | 0.41 | 0.47 | 1.4% | 0.5% | 0.2% | 2.2%/1.7% | 2.3 (interpolated) | pass | 0.012 (unverified) | -0.02 |
| 9 | `cfg_ec71` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 77/73/39 | 189 | 1.7% | 0.3% | 0.78 | -0.4% | 283 | 1.35 | 3.1% | 77.4 | 4/4 | 1.00 | 0.60 | 0.18 | 4 | 1.1% | 0.36 | 0.50 | 0.7% | -0.4% | -0.8% | 1.7%/1.2% | 1.8 (interpolated) | pass | 0.005 (unverified) | 0.04 |
| 10 | `cfg_bdac` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=3.5, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 4/106/29 | 139 | 2.2% | 0.4% | 0.80 | -0.5% | 540 | 1.59 | 2.9% | 56.4 | 6/6 | 1.00 | 0.64 | 0.16 | 5 | 1.3% | 0.38 | 0.82 | 1.4% | 0.6% | 0.2% | 2.0%/1.5% | 2.4 (interpolated) | pass | 0.001 (unverified) | 0.21 |
| 11 | `cfg_3608` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 83/80/44 | 207 | 1.8% | 0.4% | 0.76 | -0.5% | 254 | 1.33 | 3.3% | 84.8 | 4/4 | 1.00 | 0.60 | 0.16 | 4 | 1.2% | 0.30 | 0.49 | 0.6% | -0.6% | -1.0% | 1.5%/1.2% | 1.7 (interpolated) | pass | 0.005 (unverified) | -0.06 |
| 12 | `cfg_7a99` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=3.5, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 4/119/35 | 158 | 2.4% | 0.5% | 0.83 | -0.6% | 540 | 1.57 | 3.2% | 64.2 | 6/6 | 1.00 | 0.69 | 0.15 | 5 | 1.5% | 0.39 | 0.75 | 1.4% | 0.5% | 0.2% | 2.1%/1.6% | 2.3 (interpolated) | pass | 0.002 (unverified) | 0.08 |
| 13 | `cfg_8b42` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 44/120/20 | 184 | 2.1% | 0.4% | 0.77 | -0.8% | 384 | 1.39 | 3.9% | 75.0 | 4/4 | 1.00 | 0.58 | 0.19 | 3 | 0.9% | 0.59 | 0.56 | 1.1% | 0.1% | -0.7% | 1.9%/1.5% | 2.0 (interpolated) | pass | 0.004 (unverified) | 0.31 |
| 14 | `cfg_c673` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 63/62/35 | 160 | 1.5% | 0.3% | 0.76 | -0.4% | 283 | 1.39 | 2.5% | 65.2 | 5/5 | 1.00 | 0.51 | 0.25 | 5 | 1.0% | 0.33 | 0.51 | 0.6% | -0.3% | -0.7% | 1.4%/1.0% | 1.8 (interpolated) | pass | 0.005 (unverified) | -0.24 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 1.2% / 1.40 / 79 | -0.3% / -0.57 / 81 | 1.9% / 1.54 / 90 | -0.1% / -0.15 / 102 | 2.4% / 2.24 / 87 |
| 2 | 1.0% / 0.99 / 78 | -0.7% / -1.10 / 81 | 2.0% / 1.57 / 88 | 0.6% / 0.69 / 98 | 2.2% / 2.03 / 85 |
| 3 | 1.4% / 1.59 / 76 | -0.2% / -0.43 / 70 | 1.3% / 1.15 / 75 | -0.1% / -0.12 / 91 | 1.9% / 2.00 / 74 |
| 4 | 1.0% / 1.01 / 76 | -0.7% / -1.15 / 80 | 2.0% / 1.57 / 88 | 0.8% / 0.86 / 98 | 2.2% / 2.05 / 85 |
| 5 | 0.5% / 0.74 / 80 | -0.0% / -0.08 / 88 | 1.4% / 1.66 / 92 | 0.1% / 0.26 / 105 | 1.7% / 1.89 / 90 |
| 6 | 0.3% / 0.43 / 79 | -0.1% / -0.29 / 80 | 1.3% / 1.48 / 84 | 0.1% / 0.27 / 99 | 2.0% / 2.33 / 80 |
| 7 | 0.1% / 0.30 / 21 | -0.1% / -0.35 / 23 | 1.0% / 1.73 / 33 | 0.5% / 1.60 / 40 | 0.8% / 1.30 / 23 |
| 8 | 0.1% / 0.30 / 21 | -0.0% / -0.13 / 27 | 1.0% / 1.61 / 38 | 0.5% / 1.48 / 43 | 0.7% / 1.20 / 30 |
| 9 | 0.2% / 0.57 / 34 | -0.1% / -0.36 / 33 | 0.5% / 0.96 / 39 | 0.5% / 1.41 / 50 | 0.6% / 1.05 / 33 |
| 10 | 0.1% / 0.23 / 21 | 0.0% / 0.05 / 23 | 0.8% / 1.19 / 33 | 0.4% / 1.22 / 39 | 0.8% / 1.01 / 23 |
| 11 | 0.2% / 0.57 / 34 | -0.0% / -0.07 / 37 | 0.5% / 1.02 / 44 | 0.5% / 1.38 / 53 | 0.5% / 0.84 / 39 |
| 12 | 0.1% / 0.23 / 21 | 0.1% / 0.25 / 27 | 0.9% / 1.20 / 38 | 0.4% / 1.21 / 42 | 0.9% / 1.06 / 30 |
| 13 | -0.0% / -0.01 / 34 | -0.5% / -1.32 / 31 | 1.1% / 1.78 / 39 | 0.3% / 0.68 / 48 | 1.3% / 1.77 / 32 |
| 14 | 0.5% / 1.38 / 21 | 0.0% / 0.08 / 28 | 0.5% / 1.06 / 38 | 0.4% / 1.40 / 43 | 0.1% / 0.19 / 30 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_be78` | 6 | 0.92 | 0.91/0.95 | 0.85/0.92 |
| 1 | `cfg_bdac` | 5 | 0.89 | 0.91/0.95 | 0.86/0.88 |
| 2 | `cfg_73f5` | 27 | 0.86 | 0.85/0.92 | 0.76/0.90 |
| 3 | `cfg_ec71` | 4 | 0.92 | 0.94/0.97 | 0.85/0.92 |
| 4 | `cfg_1b6d` | 8 | 0.82 | 0.85/0.90 | 0.77/0.84 |
| 5 | `cfg_c252` | 8 | 0.91 | 0.88/0.93 | 0.79/0.89 |
| 6 | `cfg_8b42` | 1 | n/a | n/a/n/a | n/a/n/a |
| 7 | `cfg_c673` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.875e-03 over 2304 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 292.0, participation ratio 12.7, 95%-variance components 119 (rank bound T = 1259); raw grid 2304; raw + known prior 608640
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

- Compression at bar k uses bars through k only: bbkc = 2 x population sd(close, L) < kc_mult x Wilder ATR(L) (Bollinger 2 sd inside a Keltner channel, both centred on SMA(L)); nr = the bar's high-low range is the narrowest of the last N bars (ties count), and with inside_bar also inside the previous bar's range. Indicators run over the RTH bar series across sessions.
- A run is a maximal stretch of consecutive compression bars inside one session (never continued across the open); its box through bar r is [min low, max high] of its bars up to r. The decision at bar k uses the run holding the last compression bar r <= k-1 of k's session, live when k - r <= setup_expiry_bars, the run is at least min_squeeze_bars long (NR: min_nr_bars, 1 unless the round sets it) and the box is at least min_box_atr x ATR(14)[r] wide, so the box never includes the decision bar. A box too narrow to be live never consumes its run.
- Breakout: close entries need close_k beyond the box and fill at the NEXT bar's open (market slippage); wick entries are a stop order at the box edge, filled on bar k at the worse of its open and the edge (stop slippage); a wick bar through both edges is ambiguous and not traded. The fill bar must be in the decision's session.
- The FIRST breakout of a run decides and consumes it, traded or not (wrong direction, trend filter, inside the last 30 minutes, a position already open, a missed entry). Each setup is one decision.
- Filters known at the decision: emaN (ema20 / ema50 / ema200) needs close > EMA(N) for a long / < for a short (close entries at bar k, wick entries at bar k-1); no decision on the session's last bar or less than 30 minutes before its last close.
- Stop = the far side of the box, or entry price -/+ k x ATR(14) using the ATR known before the fill bar; R = entry price (before slippage) to stop; target = entry +/- target_r x R. Stop and target are live intrabar from the entry bar; a bar touching both counts as the stop; on a wick entry's own bar only the stop is checked, and a touch there counts (conservative). Stops fill at the worse of open and stop, targets at the better of open and target (a gap through it), each with slippage.
- Every position still open on the session's last bar is closed at that bar's CLOSE (market-on-close with the same slippage); nothing is held overnight. Stop and target take precedence over the close.
- Long and short: P&L = side x (exit fill - entry fill) x quantity - commissions; sizing is the mean-reversion funnel's (as many whole contracts as equity covers at full contract value, unlevered, compounding).
- Development backtests run on data physically truncated at the development end; the final session's trade is closed at the last development bar and flagged forced (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC; the 1-minute step there is taken as the roll spread). Point moves are preserved; pre-roll price levels are not real traded prices.
- Session: each root's day session only (src/data/futures.py SESSIONS: NYSE 09:30-16:00 NY for equity indexes, 09:00-14:30 NY for crude, 08:20-13:30 NY for gold, 08:20-15:00 NY for FX; sessions under 5% of normal volume are skipped), on NYSE trading days; overnight Globex bars are not traded or used in indicators.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side (stops too) plus commission per contract per side, from the execution YAML; cost stress scales both.
- Rolls happen outside the day session (Databento rolls at 00:00 UTC) and every position is flat by the session close, so no trade straddles a roll; compression, box, stop and target are all point distances, so back-adjustment does not change them.

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Whole-contract granularity: at ~$1M equity the position is a handful of ES contracts, so position size steps with price; results are sensitive to starting equity at small sizes.
- All lengths (BB/KC length, NR-N, ATR(14), EMA(50), min squeeze bars, setup expiry) count bars of the config's timeframe and run across sessions over RTH bars only, so the overnight gap enters the first bars of each session: it widens sd and ATR there (bbkc) and can make the first bar's range look normal (nr). Runs and boxes themselves never span sessions.
- Bar data cannot order events inside a bar: a stop and a target in the same bar count as the stop, and a wick entry's own bar checks only the stop. Both choices are conservative; a target is never credited on the entry bar of a wick entry even when it was reached after the fill.
- Targets fill as if they were market orders at the target (with slippage), not as resting limits that may or may not be filled at the touch.
- Sizing ignores the stop distance (full equity per trade, as in the other families), so the box stop and the ATR stops change the exit, not the position size.
- Squeeze (BB inside KC) and NR-N are separate strategy lines with their own runs; a breakout is never compared across lines inside one run, so stage-6 dedup does not merge a squeeze config with an NR config that trades the same days.
