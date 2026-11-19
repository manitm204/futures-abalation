# Screening funnel -- emrt_esrty_v2 (development stages only)

- Code: `66e9a379b8f4` (dirty working tree: True, diff sha256 `5d03eeeb1bf1`)
- Config: `configs/funnel/emrt_funnel_esrty_v2.yaml` sha256 `aab665d76bcbc2b0`; seed 20261118
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'ES': '2026-10-16', 'RTY': '2026-10-16', 'YM': '2026-10-16'}
- Frozen manifest sha256: `7651283c50bf0753` (10 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No pair strategy has been scored on ES-RTY 2023-2024, but mean-reversion, noise-band, squeeze and convexity strategies were selected on ES and RTY 2023-2024 and the researcher has read those results. Treated as used for selection.
- Holdout 2025+ previously inspected: **True** -- No EMRT or other pair metrics have been computed on 2025+. Single-instrument picks were scored on ES 2025+ (BB/KC squeeze, convexity v2 #115) and NQ 2025+ (convexity v3 #38 and #32), so the researcher has seen how ES traded in that period (RTY single-market picks were also tested there by earlier families).

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 13824 | 13824 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 13824 | 13824 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 13824 | 9679 | 4145 | 0 |  | 13200 | 70.02 | 70.02 |  |
| 3 performance & risk | hard_gate | 9679 | 79 | 9600 | 0 |  | 0 | 0.57 | 0.82 |  |
| 4 parameter stability | hard_gate | 79 | 77 | 2 | 0 |  | 0 | 0.56 | 97.47 |  |
| 5 time stability | hard_gate | 77 | 59 | 18 | 0 |  | 31 | 0.43 | 76.62 |  |
| 6 deduplication | dedup | 59 | 10 |  |  | 49 |  | 0.07 | 16.95 | best 2 per cluster |
| 7 execution stress | hard_gate | 10 | 10 | 0 | 0 |  | 0 | 0.07 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 10 |  |  |  |  |  |  |  | diagnostic only: unverified: 10 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 4143 |
| s2:hard_reject:years_with_>=10_trades | 2671 |
| s3:hard_reject:max_drawdown | 57 |
| s3:hard_reject:net_return | 7966 |
| s3:hard_reject:sharpe | 9600 |
| s4:hard_reject:local_median_sharpe | 2 |
| s5:hard_reject:profitable_years | 18 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES-YM dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_55c2` | timeframe=5min, formation=6, hedge=notional, z_mode=formation, entry_z=2.5, exit=half, stop=none, time_stop=3emrt, side=both, overnight=flat, first_entry=0, anchor=session | 2/69/0 | 112 | 12.8% | 2.4% | 1.13 | -1.5% | 406 | 2.34 | 3.7% | 43.6 | 4/4 | 1.00 | 0.75 | 0.38 | 4 | 0.9% | 0.91 | 0.29 | 11.4% | 10.2% | 9.8% | 11.6%/10.4% | 6.3 (interpolated) | pass | 0.057 (unverified) | -0.32 |
| 2 | `cfg_49cb` | timeframe=5min, formation=6, hedge=notional, z_mode=formation, entry_z=2.5, exit=mean, stop=none, time_stop=3emrt, side=both, overnight=flat, first_entry=0, anchor=session | 2/84/0 | 104 | 14.0% | 2.7% | 1.11 | -1.8% | 406 | 2.41 | 4.0% | 40.6 | 4/4 | 1.00 | 0.76 | 0.35 | 4 | 0.5% | 0.95 | 0.39 | 12.8% | 11.6% | 11.2% | 12.6%/10.8% | 7.3 (interpolated) | pass | 0.029 (unverified) | -0.08 |
| 3 | `cfg_7b40` | timeframe=5min, formation=6, hedge=notional, z_mode=formation, entry_z=1.5, exit=half, stop=none, time_stop=none, side=long, overnight=flat, first_entry=0, anchor=session | 0/145/0 | 218 | 7.9% | 1.5% | 0.85 | -2.5% | 629 | 1.46 | 8.8% | 85.8 | 5/5 | 1.00 | 0.60 | 0.25 | 3 | 1.1% | 0.85 | 0.36 | 5.7% | 3.6% | 5.3% | 7.3%/6.3% | 2.9 (interpolated) | pass | 0.013 (unverified) | -1.06 |
| 4 | `cfg_d93d` | timeframe=5min, formation=3, hedge=notional, z_mode=formation, entry_z=1.5, exit=half, stop=none, time_stop=3emrt, side=long, overnight=flat, first_entry=0, anchor=session | 8/153/0 | 249 | 9.4% | 1.8% | 0.96 | -2.2% | 445 | 1.49 | 9.6% | 98.0 | 6/6 | 1.00 | 0.72 | 0.24 | 4 | 1.6% | 0.82 | 0.30 | 6.9% | 4.5% | 6.2% | 8.6%/7.4% | 3.0 (interpolated) | pass | 0.025 (unverified) | -1.05 |
| 5 | `cfg_d47b` | timeframe=5min, formation=6, hedge=notional, z_mode=formation, entry_z=2.0, exit=half, stop=none, time_stop=none, side=long, overnight=flat, first_entry=0, anchor=session | 0/74/0 | 112 | 6.5% | 1.3% | 0.91 | -1.3% | 297 | 1.74 | 4.2% | 43.9 | 5/5 | 1.00 | 0.85 | 0.06 | 4 | 2.0% | 0.68 | 0.41 | 5.3% | 4.2% | 5.2% | 6.3%/5.4% | 3.9 (interpolated) | pass | 0.024 (unverified) | -0.20 |
| 6 | `cfg_f17f` | timeframe=5min, formation=3, hedge=notional, z_mode=formation, entry_z=2.5, exit=mean, stop=none, time_stop=none, side=both, overnight=flat, first_entry=0, anchor=session | 0/88/0 | 106 | 10.2% | 2.0% | 0.86 | -1.7% | 405 | 2.06 | 4.0% | 41.3 | 5/5 | 1.00 | 0.79 | 0.07 | 4 | 0.7% | 0.92 | 0.50 | 9.0% | 7.9% | 10.1% | 9.6%/8.2% | 5.7 (interpolated) | pass | 0.002 (unverified) | 0.14 |
| 7 | `cfg_57f6` | timeframe=5min, formation=3, hedge=notional, z_mode=formation, entry_z=2.5, exit=half, stop=none, time_stop=none, side=both, overnight=flat, first_entry=0, anchor=session | 0/75/0 | 113 | 8.2% | 1.6% | 0.86 | -1.6% | 405 | 1.87 | 3.7% | 44.2 | 5/5 | 1.00 | 0.76 | 0.10 | 4 | 1.1% | 0.85 | 0.45 | 7.0% | 5.8% | 8.1% | 7.6%/6.6% | 4.5 (interpolated) | pass | 0.009 (unverified) | 0.01 |
| 8 | `cfg_8ee7` | timeframe=5min, formation=6, hedge=notional, z_mode=formation, entry_z=2.0, exit=half, stop=none, time_stop=3emrt, side=long, overnight=flat, first_entry=0, anchor=session | 2/72/0 | 112 | 6.5% | 1.3% | 0.92 | -1.3% | 297 | 1.74 | 4.1% | 43.9 | 5/5 | 1.00 | 0.82 | 0.09 | 4 | 2.1% | 0.67 | 0.40 | 5.4% | 4.2% | 5.2% | 6.2%/5.6% | 4.0 (interpolated) | pass | 0.025 (unverified) | -0.20 |
| 9 | `cfg_3756` | timeframe=5min, formation=6, hedge=ols, z_mode=tod_60, entry_z=2.5, exit=half, stop=none, time_stop=3emrt, side=both, overnight=flat, first_entry=30, anchor=session | 14/57/0 | 146 | 7.4% | 1.4% | 0.79 | -1.6% | 223 | 1.54 | 4.7% | 57.4 | 4/4 | 0.75 | 0.27 | 0.52 | 5 | 1.4% | 0.81 | 0.43 | 5.9% | 4.5% | 4.8% | 7.1%/5.8% | 3.6 (interpolated) | pass | 0.006 (unverified) | -0.39 |
| 10 | `cfg_555d` | timeframe=5min, formation=6, hedge=ols, z_mode=tod_60, entry_z=2.5, exit=half, stop=none, time_stop=3emrt, side=both, overnight=flat, first_entry=0, anchor=session | 16/58/0 | 178 | 8.1% | 1.6% | 0.82 | -1.6% | 236 | 1.51 | 5.5% | 69.8 | 4/4 | 0.75 | 0.25 | 0.57 | 3 | 0.5% | 0.93 | 0.40 | 6.3% | 4.6% | 4.5% | 7.7%/6.5% | 3.3 (interpolated) | pass | 0.008 (unverified) | -0.33 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 0.1% / 0.13 / 19 | -0.7% / -1.28 / 14 | 11.8% / 2.50 / 51 | 0.7% / 0.55 / 22 | 0.8% / 1.31 / 6 |
| 2 | 0.0% / 0.03 / 19 | -0.7% / -1.28 / 14 | 13.4% / 2.52 / 43 | 0.3% / 0.28 / 22 | 0.8% / 1.24 / 6 |
| 3 | 0.3% / 0.31 / 31 | -0.5% / -0.42 / 42 | 6.7% / 2.02 / 65 | -2.0% / -1.28 / 38 | 3.4% / 2.91 / 42 |
| 4 | 0.5% / 0.56 / 46 | 0.1% / 0.08 / 45 | 7.7% / 2.20 / 74 | -1.6% / -0.96 / 41 | 2.6% / 2.24 / 43 |
| 5 | 1.1% / 1.54 / 21 | -0.4% / -0.49 / 19 | 4.4% / 1.70 / 36 | 0.3% / 0.23 / 24 | 1.1% / 1.44 / 12 |
| 6 | 0.4% / 0.59 / 23 | -0.9% / -1.55 / 14 | 9.4% / 1.92 / 39 | 0.3% / 0.20 / 24 | 1.0% / 1.35 / 6 |
| 7 | 0.7% / 0.93 / 23 | -0.9% / -1.55 / 14 | 7.0% / 1.84 / 46 | 0.2% / 0.20 / 24 | 1.1% / 1.42 / 6 |
| 8 | 1.1% / 1.59 / 21 | -0.4% / -0.48 / 19 | 4.4% / 1.70 / 36 | 0.3% / 0.23 / 24 | 1.1% / 1.44 / 12 |
| 9 | 0.3% / 0.34 / 25 | 0.3% / 0.57 / 18 | 6.0% / 1.66 / 56 | 0.7% / 0.68 / 22 | 0.0% / 0.02 / 25 |
| 10 | -0.0% / -0.03 / 29 | -0.1% / -0.14 / 29 | 7.5% / 2.06 / 64 | 0.3% / 0.24 / 28 | 0.3% / 0.24 / 28 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_f17f` | 13 | 0.87 | 0.72/0.79 | 0.37/0.47 |
| 1 | `cfg_55c2` | 20 | 0.87 | 0.61/0.69 | 0.26/0.29 |
| 2 | `cfg_7b40` | 9 | 0.93 | 0.86/0.90 | 0.68/0.75 |
| 3 | `cfg_3756` | 3 | 0.82 | 0.76/0.85 | 0.77/0.81 |
| 4 | `cfg_d47b` | 14 | 0.81 | 0.64/0.88 | 0.45/0.92 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.282e-03 over 13824 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 728.0, participation ratio 19.9, 95%-variance components 184 (rank bound T = 1259); raw grid 13824; raw + known prior 2135700
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
ES-YM results are unchanged rules on the development period: supporting evidence, not an independent replication.

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
