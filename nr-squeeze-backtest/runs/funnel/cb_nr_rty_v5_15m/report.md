# Screening funnel -- cb_nr_rty_v5_15m (development stages only)

- Code: `46ee6e771bde` (dirty working tree: True, diff sha256 `295affb2b87d`)
- Config: `configs/funnel/cb_nr_funnel_rty_v5_15m.yaml` sha256 `2e796c15b6af5060`; seed 2026112530
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'RTY': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `928230e738ba1b49` (9 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- RTY 2023-2024 was read for other families and for NR v2-v4; this grid is largely in-sample for this line.
- Holdout 2025+ previously inspected: **False** -- No NR-N metrics have been computed on RTY 2025+ for this grid; other families were scored there.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 400 | 400 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 400 | 200 | 200 | 0 |  | 0 | 50.00 | 50.00 |  |
| 2 trade count & coverage | hard_gate | 200 | 200 | 0 | 0 |  | 200 | 50.00 | 100.00 |  |
| 3 performance & risk | hard_gate | 200 | 14 | 186 | 0 |  | 0 | 3.50 | 7.00 |  |
| 4 parameter stability | hard_gate | 14 | 14 | 0 | 0 |  | 0 | 3.50 | 100.00 |  |
| 5 time stability | hard_gate | 14 | 14 | 0 | 0 |  | 14 | 3.50 | 100.00 |  |
| 6 deduplication | dedup | 14 | 9 |  |  | 5 |  | 2.25 | 64.29 | best 2 per cluster |
| 7 execution stress | hard_gate | 9 | 9 | 0 | 0 |  | 0 | 2.25 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 9 |  |  |  |  |  |  |  | diagnostic only: unverified: 9 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s1:hard_reject:integrity:box_not_from_prior_compression_run | 200 |
| s1:hard_reject:integrity:entry_signal_condition_not_met | 193 |
| s1:hard_reject:integrity:exit_not_at_first_touch | 25 |
| s1:hard_reject:integrity:not_first_breakout_of_run | 160 |
| s1:hard_reject:integrity:stop_exit_without_touch | 100 |
| s1:hard_reject:integrity:stop_fill_better_than_rule | 100 |
| s1:hard_reject:integrity:stop_not_per_rule | 100 |
| s1:hard_reject:integrity:target_not_per_rule | 80 |
| s3:hard_reject:max_drawdown | 45 |
| s3:hard_reject:net_return | 124 |
| s3:hard_reject:sharpe | 186 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | target/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_5f4a` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=4.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 8/215/156 | 379 | 32.5% | 5.8% | 1.13 | -5.8% | 317 | 1.53 | 9.0% | 170.4 | 3/3 | 1.00 | 1.06 | 0.07 | 4 | 18.5% | 0.43 | 0.49 | 28.5% | 23.6% | 28.7% | 29.5%/23.7% | 5.4 (interpolated) | pass | 0.222 (unverified) | 0.17 |
| 2 | `cfg_f03c` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=3.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 22/201/156 | 379 | 31.2% | 5.6% | 1.08 | -5.8% | 317 | 1.51 | 8.8% | 170.2 | 3/3 | 1.00 | 1.04 | 0.04 | 4 | 18.0% | 0.42 | 0.50 | 27.2% | 22.5% | 25.2% | 27.9%/22.8% | 5.2 (interpolated) | pass | 0.174 (unverified) | 0.31 |
| 3 | `cfg_e586` | timeframe=15min, compression=nr, nr_lookback=5, inside_bar=True, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=box, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 411/76/352 | 839 | 31.4% | 5.6% | 1.07 | -8.8% | 505 | 1.24 | 11.5% | 378.1 | 3/3 | 1.00 | 0.59 | 0.48 | 3 | 10.8% | 0.60 | 0.38 | 22.0% | 13.7% | 9.1% | 27.9%/22.6% | 2.9 (interpolated) | pass | 0.256 (unverified) | 0.56 |
| 4 | `cfg_ac26` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=4.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 17/345/279 | 641 | 30.8% | 5.5% | 0.91 | -6.5% | 330 | 1.28 | 14.8% | 288.5 | 3/3 | 1.00 | 0.87 | 0.04 | 4 | 14.9% | 0.45 | 0.57 | 24.4% | 17.4% | 27.2% | 28.3%/20.0% | 3.5 (interpolated) | pass | 0.105 (unverified) | 0.10 |
| 5 | `cfg_0485` | timeframe=15min, compression=nr, nr_lookback=5, inside_bar=True, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 407/89/332 | 828 | 23.4% | 4.3% | 0.85 | -8.3% | 469 | 1.18 | 12.4% | 374.5 | 3/3 | 1.00 | 0.47 | 0.37 | 4 | 7.5% | 0.68 | 0.46 | 15.5% | 6.9% | 18.9% | 20.5%/15.2% | 2.5 (interpolated) | pass | 0.106 (unverified) | 0.48 |
| 6 | `cfg_a160` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 199/50/143 | 392 | 17.3% | 3.2% | 1.04 | -4.7% | 317 | 1.34 | 6.0% | 176.2 | 2/2 | 1.00 | 0.90 | 0.14 | 4 | 7.8% | 0.55 | 0.37 | 13.6% | 10.1% | 17.8% | 15.3%/12.9% | 3.4 (interpolated) | pass | 0.202 (unverified) | -0.39 |
| 7 | `cfg_6aa9` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=3.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 42/320/279 | 641 | 30.1% | 5.4% | 0.89 | -6.9% | 330 | 1.27 | 14.5% | 288.0 | 3/3 | 1.00 | 0.80 | 0.09 | 4 | 11.4% | 0.56 | 0.60 | 23.5% | 16.4% | 22.9% | 27.0%/20.3% | 3.4 (interpolated) | pass | 0.093 (unverified) | 0.21 |
| 8 | `cfg_3c9f` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 328/93/250 | 671 | 20.4% | 3.8% | 0.95 | -6.6% | 334 | 1.22 | 10.0% | 302.0 | 2/2 | 1.00 | 0.55 | 0.40 | 4 | 10.6% | 0.48 | 0.33 | 13.4% | 7.0% | 9.7% | 17.8%/13.7% | 2.6 (interpolated) | pass | 0.155 (unverified) | -0.51 |
| 9 | `cfg_5a8f` | timeframe=15min, compression=nr, nr_lookback=8, inside_bar=True, min_nr_bars=1, entry_type=close, setup_expiry_bars=3, stop=1.0, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 310/69/250 | 629 | 17.2% | 3.2% | 0.75 | -5.8% | 469 | 1.18 | 9.9% | 283.7 | 3/3 | 1.00 | 0.85 | -0.09 | 5 | 3.9% | 0.77 | 0.49 | 11.4% | 5.2% | 15.2% | 15.1%/12.1% | 2.5 (interpolated) | pass | 0.074 (unverified) | 0.35 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 1.4% / 0.37 / 62 | -0.8% / -0.31 / 94 | 11.9% / 1.37 / 79 | 5.3% / 1.28 / 80 | 11.8% / 2.50 / 64 |
| 2 | 0.5% / 0.15 / 62 | -0.6% / -0.25 / 94 | 12.8% / 1.38 / 79 | 4.7% / 1.26 / 80 | 11.2% / 2.45 / 64 |
| 3 | 3.0% / 0.79 / 155 | -1.9% / -0.58 / 183 | 18.5% / 2.10 / 173 | -1.5% / -0.31 / 181 | 11.4% / 2.39 / 147 |
| 4 | 1.1% / 0.26 / 120 | -0.1% / -0.02 / 149 | 13.8% / 1.38 / 126 | 3.2% / 0.67 / 132 | 10.2% / 1.71 / 114 |
| 5 | 2.3% / 0.66 / 155 | -0.1% / -0.00 / 183 | 0.9% / 0.15 / 172 | 4.1% / 0.96 / 174 | 14.9% / 2.94 / 144 |
| 6 | -0.4% / -0.15 / 66 | 0.3% / 0.15 / 95 | 3.7% / 0.82 / 80 | 4.0% / 1.47 / 83 | 8.8% / 2.79 / 68 |
| 7 | 0.0% / 0.03 / 120 | -0.3% / -0.08 / 149 | 16.8% / 1.56 / 126 | 2.7% / 0.61 / 132 | 8.8% / 1.53 / 114 |
| 8 | -1.6% / -0.52 / 127 | 1.2% / 0.42 / 155 | 6.8% / 1.20 / 130 | 4.1% / 1.15 / 138 | 8.9% / 2.00 / 121 |
| 9 | 1.2% / 0.38 / 113 | 0.2% / 0.09 / 144 | 0.6% / 0.12 / 133 | 1.9% / 0.53 / 132 | 12.8% / 3.00 / 107 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_0485` | 2 | 0.80 | 0.86/0.86 | 0.79/0.79 |
| 1 | `cfg_a160` | 2 | 0.83 | 0.76/0.76 | 0.60/0.60 |
| 2 | `cfg_5f4a` | 5 | 0.85 | 0.68/0.97 | 0.53/0.94 |
| 3 | `cfg_ac26` | 4 | 0.94 | 0.93/0.98 | 0.90/0.98 |
| 4 | `cfg_e586` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.287e-03 over 400 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 82.0, participation ratio 8.0, 95%-variance components 51 (rank bound T = 1259); raw grid 400; raw + known prior 606736
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
