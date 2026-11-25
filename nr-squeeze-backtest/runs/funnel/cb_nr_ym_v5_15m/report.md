# Screening funnel -- cb_nr_ym_v5_15m (development stages only)

- Code: `46ee6e771bde` (dirty working tree: True, diff sha256 `316eb80ae414`)
- Config: `configs/funnel/cb_nr_funnel_ym_v5_15m.yaml` sha256 `37e9c1eea9779341`; seed 2026112540
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'YM': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `15f58e598510037b` (7 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- YM 2023-2024 was read for other families and for NR v2-v4; this grid is largely in-sample for this line.
- Holdout 2025+ previously inspected: **False** -- No NR-N metrics have been computed on YM 2025+ for this grid; other families were scored there.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 400 | 400 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 400 | 400 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 400 | 400 | 0 | 0 |  | 400 | 100.00 | 100.00 |  |
| 3 performance & risk | hard_gate | 400 | 13 | 387 | 0 |  | 0 | 3.25 | 3.25 |  |
| 4 parameter stability | hard_gate | 13 | 13 | 0 | 0 |  | 0 | 3.25 | 100.00 |  |
| 5 time stability | hard_gate | 13 | 13 | 0 | 0 |  | 13 | 3.25 | 100.00 |  |
| 6 deduplication | dedup | 13 | 7 |  |  | 6 |  | 1.75 | 53.85 | best 2 per cluster |
| 7 execution stress | hard_gate | 7 | 7 | 0 | 0 |  | 0 | 1.75 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 7 |  |  |  |  |  |  |  | diagnostic only: unverified: 7 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s3:hard_reject:max_drawdown | 17 |
| s3:hard_reject:net_return | 248 |
| s3:hard_reject:sharpe | 387 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | target/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_3c9f` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/387/386 | 773 | 43.0% | 7.4% | 1.22 | -6.5% | 303 | 1.37 | 19.7% | 342.3 | 2/2 | 1.00 | 1.00 | 0.22 | 4 | 26.7% | 0.38 | 0.43 | 39.2% | 33.5% | 19.6% | 38.0%/31.5% | 5.8 (interpolated) | pass | 0.716 (unverified) | 0.32 |
| 2 | `cfg_a3dc` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=4.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 41/347/385 | 773 | 37.6% | 6.6% | 1.15 | -6.4% | 303 | 1.34 | 19.3% | 344.1 | 3/3 | 1.00 | 1.05 | 0.09 | 4 | 23.0% | 0.39 | 0.45 | 32.5% | 28.1% | 16.3% | 32.3%/24.9% | 5.2 (interpolated) | pass | 0.646 (unverified) | 0.10 |
| 3 | `cfg_f2b9` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=2.0, direction=long, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 106/129/198 | 433 | 17.7% | 3.3% | 0.99 | -3.5% | 212 | 1.36 | 9.7% | 190.9 | 3/3 | 1.00 | 0.63 | 0.36 | 5 | 9.9% | 0.44 | 0.52 | 15.9% | 13.4% | 10.3% | 16.4%/12.4% | 4.9 (interpolated) | pass | 0.492 (unverified) | 0.15 |
| 4 | `cfg_cac1` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=2.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 204/202/379 | 785 | 24.2% | 4.4% | 0.97 | -4.6% | 308 | 1.24 | 16.9% | 346.2 | 3/3 | 1.00 | 0.83 | 0.15 | 4 | 12.6% | 0.48 | 0.48 | 19.6% | 15.3% | 12.4% | 21.3%/16.7% | 3.8 (interpolated) | pass | 0.472 (unverified) | 0.11 |
| 5 | `cfg_3051` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=4.0, direction=long, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 12/214/200 | 426 | 17.9% | 3.3% | 0.83 | -5.3% | 511 | 1.35 | 10.6% | 188.0 | 3/3 | 1.00 | 0.79 | 0.04 | 5 | 9.7% | 0.46 | 0.69 | 16.0% | 14.3% | 10.5% | 16.3%/13.1% | 5.0 (interpolated) | pass | 0.333 (unverified) | 0.16 |
| 6 | `cfg_07f6` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=none, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 0/216/236 | 452 | 18.4% | 3.4% | 0.78 | -5.2% | 462 | 1.30 | 11.1% | 201.1 | 2/2 | 1.00 | 0.53 | 0.25 | 4 | 6.8% | 0.63 | 0.70 | 15.6% | 13.6% | 5.7% | 16.4%/12.6% | 4.9 (interpolated) | pass | 0.300 (unverified) | 0.29 |
| 7 | `cfg_ee7f` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 429/68/332 | 829 | 14.3% | 2.7% | 0.83 | -6.8% | 518 | 1.18 | 12.5% | 363.0 | 2/2 | 1.00 | 0.65 | 0.18 | 3 | 1.9% | 0.87 | 0.38 | 9.4% | 5.4% | 1.1% | 12.4%/9.0% | 2.7 (interpolated) | pass | 0.349 (unverified) | -0.51 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 15.3% / 2.20 / 155 | -2.2% / -0.75 / 167 | 11.6% / 1.21 / 139 | 0.6% / 0.26 / 159 | 12.8% / 2.12 / 153 |
| 2 | 11.3% / 1.97 / 155 | -2.3% / -0.85 / 167 | 12.2% / 1.27 / 139 | 0.8% / 0.31 / 159 | 11.9% / 2.11 / 153 |
| 3 | 2.3% / 0.82 / 87 | 1.8% / 0.84 / 97 | 3.9% / 0.75 / 65 | 1.5% / 0.78 / 101 | 7.1% / 2.08 / 83 |
| 4 | 6.5% / 1.53 / 159 | -1.7% / -0.65 / 170 | 6.4% / 0.90 / 139 | 1.1% / 0.45 / 163 | 10.3% / 2.14 / 154 |
| 5 | 3.5% / 1.00 / 84 | 2.3% / 0.99 / 95 | 3.3% / 0.50 / 65 | 0.3% / 0.20 / 99 | 7.4% / 2.04 / 83 |
| 6 | 7.6% / 1.33 / 91 | -3.5% / -1.70 / 92 | 2.5% / 0.45 / 72 | 0.5% / 0.24 / 100 | 10.8% / 2.05 / 97 |
| 7 | 4.1% / 1.40 / 173 | -0.7% / -0.33 / 178 | -2.6% / -0.49 / 144 | 1.3% / 0.63 / 172 | 12.3% / 3.57 / 162 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_07f6` | 1 | n/a | n/a/n/a | n/a/n/a |
| 1 | `cfg_3c9f` | 6 | 0.82 | 0.72/0.93 | 0.60/0.80 |
| 2 | `cfg_f2b9` | 4 | 0.92 | 0.87/0.87 | 0.89/0.89 |
| 3 | `cfg_cac1` | 1 | n/a | n/a/n/a | n/a/n/a |
| 4 | `cfg_ee7f` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 6.628e-04 over 400 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 81.0, participation ratio 7.9, 95%-variance components 49 (rank bound T = 1259); raw grid 400; raw + known prior 606736
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
