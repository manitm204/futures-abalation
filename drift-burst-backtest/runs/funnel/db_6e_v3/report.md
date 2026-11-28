# Screening funnel -- db_6e_v3 (development stages only)

- Code: `acf4e9adf0bf` (dirty working tree: True, diff sha256 `6031d2273395`)
- Config: `configs/funnel/db_funnel_6e_v3.yaml` sha256 `cc53f820e4aa9723`; seed 20261126
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'6J': '2026-10-16', '6E': '2026-10-16'}
- Frozen manifest sha256: `033d986b3aaee95c` (0 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No drift-burst strategy has been scored on 6E 2023-2024 (ES v1/v2 and NQ v3 froze nothing), but the mean-reversion, noise-band, BB/KC squeeze, NR-N and convexity families were selected there and the researcher has read those results. Treated as used for selection.
- Holdout 2025+ previously inspected: **False** -- No drift-burst metrics have been computed on 6E 2025+. Other families (mean reversion, noise band, BB/KC squeeze, NR-N, convexity, EMRT ES-RTY) were scored there, so the researcher has seen how that period treated intraday ES strategies.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 1296 | 1296 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 1296 | 1296 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 1296 | 1080 | 216 | 0 |  | 0 | 83.33 | 83.33 |  |
| 3 performance & risk | hard_gate | 1080 | 0 | 1080 | 0 |  | 0 | 0.00 | 0.00 |  |
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
| s2:hard_reject:completed_trades | 216 |
| s3:hard_reject:net_return | 1080 |
| s3:hard_reject:sharpe | 1080 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | 6J dev SR |
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
- Trial-Sharpe variance (per period): 8.219e-04 over 1296 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 146.0, participation ratio 7.3, 95%-variance components 56 (rank bound T = 1259); raw grid 1296; raw + known prior 1645236
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
6J results are unchanged rules on the development period: supporting evidence, not an independent replication.

## Integrity audit

- Bars: the market's regular day session (src/data/futures.py SESSIONS) in 1-minute bars (db_day_bars); one session per NY date, so no position can be held overnight.
- Burst statistic at bar t, inside one session only: T = (log C_t - log C_{t-k}) / (s sqrt(k)), s = RMS of the 5k one-minute log returns ending at bar t-k (needs 6k bars of the session first). Recomputed per session with sliding windows in the integrity check.
- Volume ratio at bar t: volume over bars t-k+1..t / the sum of each bar's time-of-day norm (mean volume at that minute over the prior 20 sessions, >= 10 needed). Recomputed with plain dictionaries in the integrity check.
- Decision at bar t's close, p = t-1: |T_p| > threshold and |T| stopped rising at t (T_t NaN, opposite sign or smaller); side = -sign(T_p) (fade); long_only keeps longs; volume gate on the ratio at p; news filter on overlap of [open of bar t-k, open of bar t] with 08:28-08:45, 09:58-10:15 ET and, on Wednesdays, 13:58-15:00 ET.
- At most one trade per session; no decision on the session's last bar; a signal while a position is open is dropped, never queued.
- Entry at the NEXT bar's open with market slippage, same session. Time exit at the close of bar entry + hold - 1 with market slippage; at or past the session's last bar the trade closes at the session's last close. No stop.
- Long and short: P&L = side x (exit fill - entry fill) x quantity - commissions; sizing is the other families' (as many whole contracts as equity covers at full contract value, unlevered, compounding).
- Development backtests run on data physically truncated at the development end; the final session's trade is closed at the last development bar and flagged forced (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC). Log returns use back-adjusted prices; the adjustment is constant within a session, so 1-minute returns are distorted only by the level shift (tiny for ES).
- Session: each root's day session only (src/data/futures.py SESSIONS), on NYSE trading days; overnight Globex bars are not traded or used in any statistic.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side plus commission per contract per side, from the execution YAML; cost stress scales both. Fills come right after a violent minute, so 1 tick may be optimistic on the entry.
- Volume is the continuous front contract's. Around a roll the time-of-day norm mixes the old and new contract's volume for up to 20 sessions; Databento's front-by-volume roll keeps this small.

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- The paper (Christensen, Oomen & Renò) used tick data 2010/2012-2017, a kernel-smoothed drift estimator and EVT critical values, and measured mid-quote returns with no costs. This is a simplified 1-minute version; nothing in it was tested in the paper on traded prices.
- The volume gate is a fixed multiple of the time-of-day norm, not the paper's within-event quartiles (those need every event in the sample, i.e. hindsight).
- The news filter covers scheduled US releases at 08:30 and 10:00 ET and every Wednesday 14:00-15:00 ET (a superset of FOMC days). Unscheduled news is not filtered.
- The first 6k minutes of each session cannot produce a burst (the local-volatility window needs them), so the open's most violent minutes are never traded.
- Fading drops and spikes overlaps the mean-reversion family's bet; check daily P&L correlation with the mean-reversion finalists before adding a survivor to the book.
- Sizing ignores volatility (full equity per trade, as in the other families).
