# Screening funnel -- nb_zn_v2 (development stages only)

- Code: `e84559a57227` (dirty working tree: True, diff sha256 `853674264b0b`)
- Config: `configs/funnel/nb_funnel_zn_v2.yaml` sha256 `186f7eebb8cb2946`; seed 20261030
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ZB': '2026-10-16', 'ZN': '2026-10-16'}
- Frozen manifest sha256: `524d74c93b64a9f3` (0 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **False** -- No noise-band strategy has been selected or scored on ZN 2023-2024, and no ZN noise-band development results had been seen before this grid was chosen (it is NQ v2's grid, chosen from NQ results). The mean-reversion family was validated there (mr_zn_v5), so the period has been looked at by the researcher, but not for this strategy.
- Holdout 2025+ previously inspected: **False** -- No noise-band metrics have been computed on ZN 2025+. The mean-reversion data-access ledger has no ZN holdout read for any family.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 3456 | 3456 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 3456 | 3456 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 3456 | 3456 | 0 | 0 |  | 2304 | 100.00 | 100.00 |  |
| 3 performance & risk | hard_gate | 3456 | 0 | 3456 | 0 |  | 0 | 0.00 | 0.00 |  |
| 4 parameter stability | hard_gate | 0 | 0 | 0 | 0 |  | 0 | 0.00 |  |  |
| 5 time stability | hard_gate | 0 | 0 | 0 | 0 |  | 0 | 0.00 |  |  |
| 6 deduplication | dedup | 0 | 0 |  |  | 0 |  | 0.00 |  | best 2 per cluster |
| 7 execution stress | hard_gate | 0 | 0 | 0 | 0 |  | 0 | 0.00 |  |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 0 |  |  |  |  |  |  |  | diagnostic only:  |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s3:hard_reject:max_drawdown | 49 |
| s3:hard_reject:net_return | 3456 |
| s3:hard_reject:sharpe | 3456 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | trail/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ZB dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.665e-03 over 3456 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 220.0, participation ratio 2.7, 95%-variance components 47 (rank bound T = 1254); raw grid 3456; raw + known prior 583332
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
ZB results are unchanged rules on the development period: supporting evidence, not an independent replication.

## Integrity audit

- Noise sigma at bar k = mean of |close - session open| / raw session open at the SAME time of day (bar-open minute, NY) over the previous band_lookback sessions that have a bar at that time; today's own move is never included, so sigma is known before the session starts.
- Bands: upper = hi + band_mult x sigma x raw open, lower = lo - band_mult x sigma x raw open, with hi = lo = session open (anchor=open) or hi/lo = max/min(open, previous session's last close) (anchor=open_prev_close). Session VWAP uses typical price x volume of the session's bars through bar k.
- Signals and trailing exits are evaluated only at check-bar closes (bar close a multiple of check_minutes after the session open) at least first_entry_minutes after the open; an entry is decided at that close and fills at the NEXT bar's open in the same session; the session's last bar never signals.
- Trailing exit (decided at a check close, filled at the next open): long below the upper band / VWAP / max of the two (trail = band / vwap / band_vwap), short above the lower band / VWAP / min of the two.
- Every position is closed at the session's last bar CLOSE (market-on-close with the same slippage); nothing is held overnight. This takes precedence over a trailing exit decided at the same close.
- Optional protective stop = entry-bar open -/+ k x ATR(14) using the ATR known before the fill, live from the entry bar, filled at the worse of open and stop; it takes precedence over close-based exits of the same bar.
- After a trailing or stop exit, a same-direction entry needs a check close back inside that side's band (at or after the exit decision, same session); each session starts armed. Missed-entry stress blocks the missed direction the same way, so a missed entry is never re-taken a bar later.
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
- Rolls happen outside the day session (Databento rolls at 00:00 UTC) and every position is flat by the session close, so no trade straddles a roll; the band is scaled by the RAW session open (adjusted - price_adjustment).

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Whole-contract granularity: at ~$1M equity the position is a handful of ES contracts, so position size steps with price; results are sensitive to starting equity at small sizes.
- band_lookback counts SESSIONS (per time-of-day slot); ATR(14) counts bars of the config's timeframe and runs across sessions (RTH bars only).
- The paper sizes by volatility targeting with up to 4x leverage; here sizing is unlevered full-equity whole contracts, identical to the mean-reversion funnel so results are comparable.
- Session VWAP is built from the aggregated bars' typical price, not tick data; a session's first bar opens at the day-session open (RTH only), so the paper's 'move from the open' is measured from that open, not the overnight Globex session.
- 5min and 15min bars with the same check interval decide at the same clock times (v1 has no stop), so they differ only in fill timing granularity; near-duplicates are expected and left to stage 6.
- first_entry_minutes below the first check time changes nothing (check 30: first entry 15 = 30; check 60: 15 = 30 = 60), so 2,700 of the 8,100 v1 configs repeat another config's backtest exactly; they count in the raw trial total and collapse in stage 6.
