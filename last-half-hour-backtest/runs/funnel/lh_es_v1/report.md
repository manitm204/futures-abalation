# Screening funnel -- lh_es_v1 (development stages only)

- Code: `85258bebd6f4` (dirty working tree: True, diff sha256 `3c88a1a46a85`)
- Config: `configs/funnel/lh_funnel_es_v1.yaml` sha256 `b36b9c38a270a63d`; seed 20261125
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ES': '2026-10-16', 'NQ': '2026-10-16'}
- Frozen manifest sha256: `0017213b0156c214` (1 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No last-half-hour strategy has been scored on ES 2023-2024, but the noise-band, mean-reversion, squeeze, convexity, drift-burst and month-end families were selected there and the researcher has read those results. The NQ run of this same grid (lh_nq_v1) was validated and holdout-tested before this run was specified.
- Holdout 2025+ previously inspected: **True** -- No last-half-hour metrics have been computed on ES 2025+. Other families (noise band, mean reversion, squeezes, convexity, month-end #1/#7/#17) were scored there, and lh_nq_v1 #49/#56 failed or added nothing on NQ 2025+, so this run is not blind to the period.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 500 | 500 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 500 | 500 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 500 | 500 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 3 performance & risk | hard_gate | 500 | 1 | 499 | 0 |  | 0 | 0.20 | 0.20 |  |
| 4 parameter stability | hard_gate | 1 | 1 | 0 | 0 |  | 0 | 0.20 | 100.00 |  |
| 5 time stability | hard_gate | 1 | 1 | 0 | 0 |  | 1 | 0.20 | 100.00 |  |
| 6 deduplication | dedup | 1 | 1 |  |  | 0 |  | 0.20 | 100.00 | best 2 per cluster |
| 7 execution stress | hard_gate | 1 | 1 | 0 | 0 |  | 0 | 0.20 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 1 |  |  |  |  |  |  |  | diagnostic only: unverified: 1 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s3:hard_reject:max_drawdown | 5 |
| s3:hard_reject:net_return | 371 |
| s3:hard_reject:sharpe | 499 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | NQ dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_e962` | timeframe=1min, signal=open, agree=off, window=15:50-16:00, filter=rv_high, stop=0.10 | 0/285/250 | 535 | 10.9% | 2.0% | 0.80 | -3.7% | 306 | 1.28 | 0.8% | 241.6 | 2/2 | 1.00 | 0.47 | 0.33 | 4 | 0.7% | 0.91 | 0.79 | 6.0% | 1.4% | 1.2% | 10.1%/7.0% | 2.2 (interpolated) | pass | 0.082 (unverified) | 1.68 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 0.9% / 0.61 / 53 | -2.2% / -2.05 / 92 | 10.1% / 2.04 / 130 | 1.8% / 1.13 / 89 | 0.3% / 0.14 / 171 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_e962` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.132e-03 over 500 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 100.0, participation ratio 7.7, 95%-variance components 55 (rank bound T = 1290); raw grid 500; raw + known prior 1648904
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

- Bars: 1-minute bars with NY open time in [09:30, 16:00) on their own session date only (lh_day_bars); each NY date is one session and no position can be held overnight.
- Signal per session: prev_close = close of the last bar opening before the entry time / the previous session's last close - 1; open = the same over today's first bar's open (bar opening by 09:35); first_half = close of the last bar opening before 10:00 / previous close - 1. The decision bar must open within 3 minutes of the entry time; the entry is the bar right after it.
- Filters: z = |signal| above z x the std (ddof 1) of the same signal over the previous 20 sessions (>= 15 defined); rv_high = std of the previous 20 daily close-to-close returns above its median over the previous 120 sessions (>= 60 defined); down_only = signal < 0. Agreement: the first-half-hour return has the signal's sign. All recomputed with plain loops in the integrity check.
- Entry: in the signal's direction (long > 0, short < 0) at the OPEN of the first bar opening at/after the entry time with market slippage; skipped when that bar opens more than 2 minutes late.
- Exit at the CLOSE of the last bar opening before the exit time with market slippage; a 16:00 exit (and any early close) is the session's last bar. Stop (optional) = entry open x (1 -/+ stop%) against the position, live intrabar from the entry bar, filled at the worse of the bar's open and the stop with stop slippage.
- One trade per session; sizing is the other families' (as many whole contracts as equity covers at full contract value, unlevered, compounding).
- Development backtests run on data physically truncated at the development end; the final session's trade is closed at the last development bar and flagged forced (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC). Log returns use back-adjusted prices; the adjustment is constant within a session, so 1-minute returns are distorted only by the level shift (tiny for ES).
- Session: each root's day session only (src/data/futures.py SESSIONS), on NYSE trading days; overnight Globex bars are not traded or used in any statistic.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side plus commission per contract per side, from the execution YAML; cost stress scales both. ES ticks are 0.25 point ($12.50), NQ 0.25 point ($5.00).
- Session: 09:30-16:00 ET of each NY date with data; Globex bars outside it are never loaded, so the previous close is the last RTH bar's close (09:30-16:00), not the 17:00 settlement.

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- The paper's effect is strongest on days dealers are short gamma; the bars cannot see dealer positioning, so z, rv_high and down_only are bar-observable stand-ins chosen before the run, not measured gamma.
- Post-2013 replications find the unconditional slope near zero in SPY / SPX; the 2018-2026 sample sits entirely in that decayed period.
- The 16:00 exit fills at the close of the 15:59 bar (the last RTH bar), not the 16:00 settlement or closing auction price; the 16:00-16:15 ES/NQ trading is never used.
- Early-close days (13:00 / 13:15 ET) have no 15:00+ bars, so no trade is taken on them.
- Sizing ignores volatility (full equity per trade, as in the other families).
