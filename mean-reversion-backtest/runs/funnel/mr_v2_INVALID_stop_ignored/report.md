# Screening funnel -- mr_v2 (development stages only)

- Code: `737d995cb21f` (dirty working tree: True, diff sha256 `49954e49c33e`)
- Config: `configs/funnel/mr_funnel_v2.yaml` sha256 `6e0f333c7997432d`; seed 20261016
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'QQQ': '2026-08-18', 'SPY': '2026-08-18'}
- Frozen manifest sha256: `4602f72f54e4c13a` (0 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- mr_v1 evaluated 15 frozen mean-reversion candidates on 2023-2024 (all failed) and the v2 parameter space was designed after those results were read. The same slice also gated the channel-breakout funnels and the Donchian ablation.
- Holdout 2025+ previously inspected: **True** -- SPY 2025-2026 holdout metrics were computed and inspected for the Donchian ablation and the channel-breakout funnels (funnel_v1..v3 records.parquet). The holdout is NOT an untouched test of SPY.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 240000 | 240000 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 240000 | 240000 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 240000 | 140610 | 99390 | 0 |  | 144095 | 58.59 | 58.59 |  |
| 3 performance & risk | hard_gate | 140610 | 5 | 140605 | 0 |  | 0 | 0.00 | 0.00 |  |
| 4 parameter stability | hard_gate | 5 | 0 | 5 | 0 |  | 5 | 0.00 | 0.00 |  |
| 5 time stability | hard_gate | 0 | 0 | 0 | 0 |  | 0 | 0.00 |  |  |
| 6 deduplication | dedup | 0 | 0 |  |  | 0 |  | 0.00 |  |  |
| 7 execution stress | hard_gate | 0 | 0 | 0 | 0 |  | 0 | 0.00 |  |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 0 |  |  |  |  |  |  |  | diagnostic only:  |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 99390 |
| s2:hard_reject:years_with_>=10_trades | 59850 |
| s3:hard_reject:max_drawdown | 45690 |
| s3:hard_reject:net_return | 133275 |
| s3:hard_reject:sharpe | 140605 |
| s4:hard_reject:neighbor_median_sharpe | 5 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | z/time/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | QQQ dev SR |
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
- Trial-Sharpe variance (per period): 2.182e-03 over 227600 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 1682.0, participation ratio 29.9, 95%-variance components 346 (rank bound T = 1259); raw grid 240000; raw + known prior 343464
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
QQQ results are unchanged rules on the development period: supporting evidence, not an independent replication.

## Integrity audit

- z = (close - mean) / std with mean = SMA/EMA of the last N closes and std = rolling sample std of the last M closes (bars of the config's timeframe), both INCLUDING the signal bar's close; the signal is decided at that close and the entry fills at the NEXT bar's open.
- Exits are decided at a close on or after the entry bar (z >= exit_z, or held max_hold bars) and fill at the next bar's open, so a time exit fills exactly max_hold bars after entry.
- Trend filter compares the signal bar's close to the SMA(100/150/200 bars) of closes up to that bar; warm-up bars (SMA undefined) never signal.
- No profit target exists. v1 has no stop; v2's optional ATR stop is entry fill - k x ATR(14) using the ATR known before the fill, live from the entry bar, filled at the worse of open and stop. Sizing (v1 and v2): as many whole shares as current equity affords (no leverage).
- v2 only: the z-score std uses the same window as the mean; positive_bar_return requires the signal bar's close above the previous close; cooldown_bars = N requires the next signal bar to be >= N bars after the previous exit.
- After a time exit the setup re-arms only once z closes above entry_z, so the holding cap cannot be undone by an immediate re-entry.
- Missed-entry stress skips a whole signal episode (contiguous signal bars), never re-entering one bar later.
- Adverse slippage + commission on every fill; a fill at a session's first bar bears the full overnight gap.
- Development backtests run on data physically truncated at the development end; open positions are force-closed at the last development bar and flagged (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Positions are held overnight (no session-end flattening), as in the channel family; rolling windows run continuously across sessions over RTH bars only.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Unresolved assumptions

- Drawdown limit -30% is reused from the channel-breakout funnel (src/experiments/validation.py); that approval was given for 0.25%-risk stop-based sizing, while this strategy invests full equity per trade -- it has not been separately approved for this sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0: Sharpe vs. cash is overstated in high-rate years (2023-2024 ~5%).
- Variable cost stress scales per-share commission and slippage bps; the $1 per-order minimum commission is treated as fixed.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Prices are split-adjusted but NOT dividend-adjusted: SPY's ~1.5%/yr dividend is not credited while long, and each ex-dividend drop slightly lowers z (a small bias toward entries on ex-div dates).
- Neighbor lattice: v1 orders timeframe, mean/std lookback, entry/exit z and max hold; v2 orders timeframe, mean lookback, entry/exit z, max holding bars, cooldown and ATR stop (1.0 < 1.5 < 2.0 < 3.0 < none). mean_type, trend_filter (and v2 entry_confirmation) are held fixed (categorical).
- All lookbacks, trend SMAs and holding periods are counted in bars of the config's timeframe (e.g. sma200 on 5min bars spans ~2.6 sessions), not in trading days.
