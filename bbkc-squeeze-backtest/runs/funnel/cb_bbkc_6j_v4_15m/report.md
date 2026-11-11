# Screening funnel -- cb_bbkc_6j_v4_15m (development stages only)

- Code: `36bde5f6ce84` (dirty working tree: True, diff sha256 `99d2740b6266`)
- Config: `configs/funnel/cb_bbkc_funnel_6j_v4_15m.yaml` sha256 `b381d70aade7f6d8`; seed 20261112
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'6J': '2026-10-16', '6E': '2026-10-16'}
- Frozen manifest sha256: `6b183abdeb131df8` (3 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **False** -- No compression-breakout strategy has been selected or scored on 6J 2023-2024. This grid was chosen after reading ES, NQ and YM squeeze results on 2023-2024 and 2025+. Other families were validated there (mean-reversion: mr_6j_v5), so the period has been looked at by the researcher, but not for this strategy.
- Holdout 2025+ previously inspected: **False** -- No metrics of any family have been computed on 6J 2025+ (no holdout reads in the mean-reversion or noise-band ledgers).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 3840 | 3840 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 3840 | 3840 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 3840 | 3258 | 582 | 0 |  | 3140 | 84.84 | 84.84 |  |
| 3 performance & risk | hard_gate | 3258 | 4 | 3254 | 0 |  | 0 | 0.10 | 0.12 |  |
| 4 parameter stability | hard_gate | 4 | 3 | 1 | 0 |  | 0 | 0.08 | 75.00 |  |
| 5 time stability | hard_gate | 3 | 3 | 0 | 0 |  | 3 | 0.08 | 100.00 |  |
| 6 deduplication | dedup | 3 | 3 |  |  | 0 |  | 0.08 | 100.00 | best 2 per cluster |
| 7 execution stress | hard_gate | 3 | 3 | 0 | 0 |  | 0 | 0.08 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 3 |  |  |  |  |  |  |  | diagnostic only: unverified: 3 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 582 |
| s2:hard_reject:years_with_>=10_trades | 288 |
| s3:hard_reject:net_return | 2702 |
| s3:hard_reject:sharpe | 3254 |
| s4:hard_reject:local_frac_profitable | 1 |
| s4:hard_reject:local_median_sharpe | 1 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | target/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | 6E dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_6fc3` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=4, stop=1.5, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/294/159 | 453 | 9.0% | 1.7% | 1.00 | -2.8% | 190 | 1.38 | 17.1% | 201.3 | 6/6 | 0.83 | 0.56 | 0.44 | 4 | 5.7% | 0.35 | 0.55 | 5.2% | 2.0% | 4.0% | 8.0%/5.9% | 2.3 (interpolated) | pass | 0.020 (unverified) | 0.19 |
| 2 | `cfg_16c5` | timeframe=15min, compression=bbkc, squeeze_length=45, kc_mult=2.5, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=none, direction=both, trend_filter=none, min_box_atr=0.0 | 0/289/156 | 445 | 8.6% | 1.7% | 0.97 | -2.5% | 190 | 1.37 | 16.7% | 197.0 | 6/6 | 0.83 | 0.42 | 0.56 | 4 | 5.7% | 0.33 | 0.57 | 5.0% | 1.8% | 3.1% | 7.7%/6.1% | 2.3 (interpolated) | pass | 0.017 (unverified) | 0.14 |
| 3 | `cfg_1783` | timeframe=15min, compression=bbkc, squeeze_length=25, kc_mult=2.0, min_squeeze_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=2.5, direction=long, trend_filter=ema50, min_box_atr=0.0 | 42/47/66 | 155 | 3.5% | 0.7% | 0.82 | -1.2% | 509 | 1.50 | 4.3% | 67.7 | 8/8 | 0.50 | 0.21 | 0.61 | 4 | 1.6% | 0.53 | 0.74 | 2.3% | 1.2% | 2.2% | 3.2%/2.4% | 2.5 (interpolated) | pass | 0.008 (unverified) | 0.48 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 1.9% / 1.29 / 85 | 3.1% / 1.33 / 113 | 2.5% / 1.39 / 98 | 2.5% / 1.96 / 80 | -1.2% / -0.66 / 77 |
| 2 | 1.8% / 1.26 / 84 | 2.7% / 1.19 / 113 | 2.4% / 1.41 / 93 | 2.3% / 1.82 / 79 | -0.9% / -0.50 / 76 |
| 3 | 0.1% / 0.09 / 38 | -0.1% / -0.16 / 33 | 0.4% / 0.56 / 33 | 1.3% / 2.01 / 30 | 1.8% / 1.47 / 21 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_6fc3` | 2 | 0.99 | 0.98/0.98 | 0.98/0.98 |
| 1 | `cfg_1783` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.362e-03 over 3840 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 527.0, participation ratio 17.9, 95%-variance components 221 (rank bound T = 1257); raw grid 3840; raw + known prior 736656
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
6E results are unchanged rules on the development period: supporting evidence, not an independent replication.

## Integrity audit

- Compression at bar k uses bars through k only: bbkc = 2 x population sd(close, L) < kc_mult x Wilder ATR(L) (Bollinger 2 sd inside a Keltner channel, both centred on SMA(L)); nr = the bar's high-low range is the narrowest of the last N bars (ties count), and with inside_bar also inside the previous bar's range. Indicators run over the RTH bar series across sessions.
- A run is a maximal stretch of consecutive compression bars inside one session (never continued across the open); its box through bar r is [min low, max high] of its bars up to r. The decision at bar k uses the run holding the last compression bar r <= k-1 of k's session, live when k - r <= setup_expiry_bars, the run is at least min_squeeze_bars long (NR: 1) and the box is at least min_box_atr x ATR(14)[r] wide, so the box never includes the decision bar. A box too narrow to be live never consumes its run.
- Breakout: close entries need close_k beyond the box and fill at the NEXT bar's open (market slippage); wick entries are a stop order at the box edge, filled on bar k at the worse of its open and the edge (stop slippage); a wick bar through both edges is ambiguous and not traded. The fill bar must be in the decision's session.
- The FIRST breakout of a run decides and consumes it, traded or not (wrong direction, trend filter, inside the last 30 minutes, a position already open, a missed entry). Each setup is one decision.
- Filters known at the decision: ema50 needs close > EMA(50) for a long / < for a short (close entries at bar k, wick entries at bar k-1); no decision on the session's last bar or less than 30 minutes before its last close.
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
