# Screening funnel -- pc_gc_v3_15m (development stages only)

- Code: `a7616723a070` (dirty working tree: True, diff sha256 `13f94a718c59`)
- Config: `configs/funnel/pc_funnel_gc_v3_15m.yaml` sha256 `b248ab8bd9ff9609`; seed 20261116
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ES': '2026-10-16', 'GC': '2026-10-16'}
- Frozen manifest sha256: `9fc056c7286e23cc` (2 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No convexity strategy has been scored on GC 2023-2024, but BB/KC squeeze, NR-N and mean-reversion strategies were selected there and the researcher has read those results. Treated as used for selection.
- Holdout 2025+ previously inspected: **False** -- No convexity metrics have been computed on GC 2025+. Other families (BB/KC squeeze, NR-N, mean reversion) were scored there, and convexity picks were scored on ES and NQ 2025+ (all lost), so the researcher has seen how that period treated intraday strategies.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 103680 | 103680 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 103680 | 103680 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 103680 | 76868 | 26812 | 0 |  | 62743 | 74.14 | 74.14 |  |
| 3 performance & risk | hard_gate | 76868 | 5 | 76863 | 0 |  | 0 | 0.00 | 0.01 |  |
| 4 parameter stability | hard_gate | 5 | 2 | 3 | 0 |  | 0 | 0.00 | 40.00 |  |
| 5 time stability | hard_gate | 2 | 2 | 0 | 0 |  | 2 | 0.00 | 100.00 |  |
| 6 deduplication | dedup | 2 | 2 |  |  | 0 |  | 0.00 | 100.00 | best 2 per cluster |
| 7 execution stress | hard_gate | 2 | 2 | 0 | 0 |  | 0 | 0.00 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 2 |  |  |  |  |  |  |  | diagnostic only: unverified: 2 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 26812 |
| s2:hard_reject:years_with_>=10_trades | 22888 |
| s3:hard_reject:max_drawdown | 3419 |
| s3:hard_reject:net_return | 70288 |
| s3:hard_reject:sharpe | 76863 |
| s4:hard_reject:local_median_sharpe | 3 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_7299` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=250, entry_z=0.5, quadrant=late, min_move_atr=3.0, direction=short, hold=full, stop=2.0, trend_filter=none | 131/9/52 | 192 | 10.7% | 2.1% | 0.78 | -3.0% | 191 | 1.38 | 6.2% | 102.4 | 8/8 | 0.88 | 0.33 | 0.45 | 5 | 6.0% | 0.44 | 0.73 | 9.1% | 7.7% | 3.8% | 9.5%/6.7% | 4.5 (interpolated) | pass | 0.021 (unverified) | -0.25 |
| 2 | `cfg_4d22` | timeframe=15min, lookback=10, signal_form=maxgap, z_lookback=25, entry_z=0.5, quadrant=late, min_move_atr=3.0, direction=short, hold=full, stop=2.0, trend_filter=none | 123/12/51 | 186 | 11.0% | 2.1% | 0.80 | -3.7% | 237 | 1.40 | 5.9% | 100.1 | 8/8 | 0.75 | 0.43 | 0.37 | 5 | 6.8% | 0.38 | 0.70 | 9.4% | 8.1% | 4.5% | 10.2%/7.5% | 4.9 (interpolated) | pass | 0.024 (unverified) | -0.33 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 1.4% / 0.85 / 25 | 1.6% / 0.75 / 39 | 1.4% / 0.42 / 41 | 1.5% / 0.66 / 43 | 4.4% / 1.35 / 44 |
| 2 | 1.5% / 0.98 / 23 | 1.0% / 0.48 / 44 | 4.1% / 1.12 / 40 | 0.1% / 0.05 / 40 | 3.9% / 1.22 / 39 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_7299` | 2 | 0.92 | 0.92/0.92 | 0.78/0.78 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 8.982e-04 over 95748 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1732.0, participation ratio 27.3, 95%-variance components 398 (rank bound T = 1239); raw grid 103680; raw + known prior 1838484
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

- Signal at bar k from the closes of bars k-N+1..k only (N = lookback, over the RTH bar series across sessions): paper = (midpoint - mean) / midpoint, midpoint = (P1 + PN) / 2 (Gulen & Woeppel's convexity); atr = (midpoint - mean) / ATR(14)[k]; maxgap = the signed line-minus-path gap of largest magnitude / ATR(14)[k]; reversal (control) = (PN - P1) / ATR(14)[k].
- z_k = (S_k - mean(S over the last z_lookback bars, k included)) / population sd of the same; NaN during warm-up.
- Decision at bar k's close: short on a fresh cross z_k >= entry_z (z_{k-1} was not), long on a fresh cross z_k <= -entry_z. A HIGH signal always fades to SHORT. A signal while a position is open is dropped, never queued.
- Filters known at bar k: quadrant late = only against the window's net move PN - P1, early = only with it; |PN - P1| >= min_move_atr x ATR(14)[k]; direction; emaN needs close_k > EMA(N)_k for a long, < for a short; no decision on the session's last bar or less than 30 minutes before its last close.
- Entry fills at the NEXT bar's open with market slippage; the fill bar must be in the decision's session.
- Stop (optional) = open -/+ stop x ATR(14) of the bar before the fill, live intrabar from the entry bar, filled at the worse of the bar's open and the stop with stop slippage. Hold half = ceil(N/2) bars, full = N bars: closed at the close of bar entry + H - 1; session = the session's last close. Every position still open on the session's last bar is closed at that bar's CLOSE; nothing is held overnight.
- Long and short: P&L = side x (exit fill - entry fill) x quantity - commissions; sizing is the mean-reversion funnel's (as many whole contracts as equity covers at full contract value, unlevered, compounding).
- Development backtests run on data physically truncated at the development end; the final session's trade is closed at the last development bar and flagged forced (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC; the 1-minute step there is taken as the roll spread). Point moves are preserved; pre-roll price levels are not real traded prices.
- Session: each root's day session only (src/data/futures.py SESSIONS), on NYSE trading days; overnight Globex bars are not traded or used in indicators.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side (stops too) plus commission per contract per side, from the execution YAML; cost stress scales both.
- Every position is flat by the session close, so no trade straddles a roll. The atr / maxgap / reversal signals are point distances and unaffected by back-adjustment; the paper form divides by a back-adjusted price level, so its scale drifts slightly with the cumulative roll adjustment (the rolling z-score absorbs most of it).

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- The paper tested convexity on DAILY closes with 5- to 21-day holds; every look-back here is intraday, so this whole grid is untested extrapolation of the paper.
- Windows (N up to 96 bars) and the z-score history (250 / 500 bars) run across sessions over RTH bars, so the overnight gap enters the path: a window spanning the open sees the gap as a jump between two adjacent closes.
- The paper form divides by a price level; on a contract whose back-adjusted price nears zero (e.g. CL in April 2020) it is undefined or explodes. The atr form is the same gap without that problem.
- The reversal control has no convex/concave split: its z is extreme almost only in the direction of the net move, so its quadrant=late configs nearly duplicate quadrant=all and its quadrant=early configs trade rarely. They stay in the full factorial (and the raw trial count) so every axis has the same values.
- hold=full equals hold=session whenever N exceeds the bars left in the session (most of N = 48 / 64 / 96 on 15m bars).
- COVID (March-April 2020) falls inside the development period; the paper found the signal much weaker with those months included.
- Sizing ignores the stop distance (full equity per trade, as in the other families), so the ATR stops change the exit, not the position size.
