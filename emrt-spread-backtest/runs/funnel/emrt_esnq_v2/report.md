# Screening funnel -- emrt_esnq_v2 (development stages only)

- Code: `66e9a379b8f4` (dirty working tree: True, diff sha256 `5d03eeeb1bf1`)
- Config: `configs/funnel/emrt_funnel_esnq_v2.yaml` sha256 `c5cf3166727fd6f3`; seed 20261118
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ES': '2026-10-16', 'NQ': '2026-10-16', 'RTY': '2026-10-16'}
- Frozen manifest sha256: `040f7f588d9b37fb` (6 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No pair strategy has been scored on ES-NQ 2023-2024, but mean-reversion, noise-band, squeeze and convexity strategies were selected on ES and NQ 2023-2024 and the researcher has read those results. Treated as used for selection.
- Holdout 2025+ previously inspected: **True** -- No EMRT or other pair metrics have been computed on 2025+. Single-instrument picks were scored on ES 2025+ (BB/KC squeeze, convexity v2 #115) and NQ 2025+ (convexity v3 #38 and #32), so the researcher has seen how both legs traded in that period.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 13824 | 13824 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 13824 | 13824 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 13824 | 10055 | 3769 | 0 |  | 13127 | 72.74 | 72.74 |  |
| 3 performance & risk | hard_gate | 10055 | 46 | 10009 | 0 |  | 0 | 0.33 | 0.46 |  |
| 4 parameter stability | hard_gate | 46 | 39 | 7 | 0 |  | 0 | 0.28 | 84.78 |  |
| 5 time stability | hard_gate | 39 | 34 | 5 | 0 |  | 29 | 0.25 | 87.18 |  |
| 6 deduplication | dedup | 34 | 6 |  |  | 28 |  | 0.04 | 17.65 | best 2 per cluster |
| 7 execution stress | hard_gate | 6 | 6 | 0 | 0 |  | 0 | 0.04 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 6 |  |  |  |  |  |  |  | diagnostic only: unverified: 6 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 3676 |
| s2:hard_reject:years_with_>=10_trades | 2442 |
| s3:hard_reject:net_return | 9320 |
| s3:hard_reject:sharpe | 10009 |
| s4:hard_reject:local_frac_profitable | 1 |
| s4:hard_reject:local_median_sharpe | 7 |
| s5:hard_reject:profitable_years | 5 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES-RTY dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_eb21` | timeframe=5min, formation=3, hedge=emrt_c2.0, z_mode=tod_20, entry_z=2.5, exit=half, stop=1.5, time_stop=none, side=long, overnight=flat, first_entry=0, anchor=session | 0/18/17 | 102 | 8.5% | 1.6% | 1.20 | -1.2% | 267 | 2.04 | 2.0% | 40.4 | 5/5 | 1.00 | 0.92 | 0.29 | 4 | 3.2% | 0.61 | 0.47 | 7.6% | 6.8% | 4.6% | 7.8%/6.5% | 6.2 (interpolated) | pass | 0.115 (unverified) | -0.33 |
| 2 | `cfg_881b` | timeframe=5min, formation=3, hedge=emrt_c2.0, z_mode=tod_20, entry_z=2.5, exit=half, stop=1.5, time_stop=3emrt, side=long, overnight=flat, first_entry=0, anchor=session | 4/14/17 | 102 | 8.9% | 1.7% | 1.26 | -1.2% | 160 | 2.12 | 1.9% | 40.4 | 5/5 | 1.00 | 0.93 | 0.33 | 4 | 3.2% | 0.61 | 0.45 | 8.0% | 7.2% | 4.8% | 8.4%/7.2% | 6.4 (interpolated) | pass | 0.144 (unverified) | -0.30 |
| 3 | `cfg_1839` | timeframe=15min, formation=3, hedge=emrt_c1.5, z_mode=tod_20, entry_z=2.5, exit=half, stop=1.5, time_stop=3emrt, side=long, overnight=flat, first_entry=0, anchor=session | 12/29/17 | 112 | 7.7% | 1.5% | 1.10 | -1.1% | 252 | 1.85 | 2.9% | 44.3 | 5/5 | 0.80 | 0.59 | 0.51 | 4 | 3.4% | 0.54 | 0.55 | 6.7% | 6.0% | 6.0% | 7.6%/6.5% | 5.4 (interpolated) | pass | 0.091 (unverified) | -0.08 |
| 4 | `cfg_ac54` | timeframe=15min, formation=3, hedge=emrt_c1.5, z_mode=tod_20, entry_z=2.5, exit=half, stop=1.5, time_stop=3emrt, side=long, overnight=flat, first_entry=30, anchor=session | 12/29/17 | 112 | 7.7% | 1.5% | 1.10 | -1.1% | 252 | 1.85 | 2.9% | 44.3 | 5/5 | 0.80 | 0.41 | 0.68 | 4 | 3.4% | 0.54 | 0.55 | 6.7% | 6.0% | 6.0% | 7.6%/6.4% | 5.4 (interpolated) | pass | 0.091 (unverified) | -0.08 |
| 5 | `cfg_8400` | timeframe=5min, formation=3, hedge=ols, z_mode=formation, entry_z=2.5, exit=half, stop=none, time_stop=3emrt, side=long, overnight=flat, first_entry=0, anchor=session | 2/61/0 | 106 | 5.4% | 1.1% | 0.83 | -1.9% | 464 | 1.68 | 3.5% | 41.5 | 5/5 | 0.80 | 0.48 | 0.36 | 3 | 1.4% | 0.72 | 0.52 | 4.5% | 3.6% | 3.3% | 4.8%/4.1% | 4.2 (interpolated) | pass | 0.102 (unverified) | -0.21 |
| 6 | `cfg_e065` | timeframe=5min, formation=3, hedge=ols, z_mode=formation, entry_z=2.5, exit=half, stop=none, time_stop=none, side=long, overnight=flat, first_entry=0, anchor=session | 0/63/0 | 106 | 5.2% | 1.0% | 0.79 | -1.9% | 464 | 1.64 | 3.5% | 41.5 | 5/5 | 0.80 | 0.44 | 0.35 | 3 | 1.4% | 0.71 | 0.54 | 4.2% | 3.4% | 3.0% | 4.7%/4.0% | 4.1 (interpolated) | pass | 0.091 (unverified) | -0.42 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | -0.3% / -0.31 / 12 | 0.5% / 1.09 / 12 | 5.1% / 2.08 / 35 | 1.2% / 0.97 / 20 | 1.9% / 2.19 / 23 |
| 2 | -0.3% / -0.25 / 12 | 0.5% / 1.09 / 12 | 5.4% / 2.21 / 35 | 1.2% / 0.97 / 20 | 1.9% / 2.14 / 23 |
| 3 | 2.3% / 1.58 / 22 | -0.3% / -0.81 / 16 | 4.1% / 2.05 / 24 | 1.4% / 1.05 / 24 | 0.0% / 0.02 / 26 |
| 4 | 2.3% / 1.58 / 22 | -0.3% / -0.81 / 16 | 4.1% / 2.05 / 24 | 1.4% / 1.05 / 24 | 0.0% / 0.02 / 26 |
| 5 | -0.5% / -0.38 / 27 | -0.5% / -1.80 / 11 | 4.0% / 1.68 / 42 | 0.4% / 0.78 / 10 | 2.0% / 2.77 / 16 |
| 6 | -0.5% / -0.38 / 27 | -0.5% / -1.80 / 11 | 3.7% / 1.57 / 42 | 0.4% / 0.75 / 10 | 2.0% / 2.77 / 16 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_1839` | 12 | 0.86 | 0.67/0.85 | 0.44/0.76 |
| 1 | `cfg_eb21` | 19 | 0.81 | 0.30/0.58 | 0.09/0.25 |
| 2 | `cfg_8400` | 3 | 0.99 | 0.86/0.93 | 0.95/0.97 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.077e-03 over 13824 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 675.0, participation ratio 16.3, 95%-variance components 161 (rank bound T = 1259); raw grid 13824; raw + known prior 2121876
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
- v2 (anchor = session): each leg is measured from TODAY's first open, a = (A - A_open) / A_open_raw, so S = a - beta b restarts every session; beta is fit monthly on these intraday spreads (extremum search and reversion confined to a session, a swing not back by the close censored there); z = formation mean / sd, or tod_N = mean / sd of S at the same bar of the previous N sessions (>= max(5, N/2) present); z_prev of a session's first bar is NaN (no cross across sessions); first_entry = no decision before that many minutes after the open; every position closes at the session's last close (overnight = flat only).
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
