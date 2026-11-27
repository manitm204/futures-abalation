# Screening funnel -- fx_6e_v2 (development stages only)

- Code: `acf4e9adf0bf` (dirty working tree: True, diff sha256 `12827c6315b7`)
- Config: `configs/funnel/fx_funnel_6e_v2.yaml` sha256 `1db5a8af6a1fcb53`; seed 20261127
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'6J': '2026-10-16', '6E': '2026-10-16'}
- Frozen manifest sha256: `f67ce475974d609a` (2 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- No FX-fix strategy has been scored on 6E 2023-2024, but mean-reversion, BB/KC squeeze, NR-N squeeze and convexity strategies were selected there and the researcher has read those results. Treated as used for selection.
- Holdout 2025+ previously inspected: **False** -- The data-access ledgers of every project show no 6E holdout (2025+) access to date.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 1224 | 1224 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 1224 | 1224 | 0 | 0 |  | 0 | 100.00 | 100.00 |  |
| 2 trade count & coverage | hard_gate | 1224 | 534 | 690 | 0 |  | 0 | 43.63 | 43.63 |  |
| 3 performance & risk | hard_gate | 534 | 2 | 532 | 0 |  | 0 | 0.16 | 0.37 |  |
| 4 parameter stability | hard_gate | 2 | 2 | 0 | 0 |  | 0 | 0.16 | 100.00 |  |
| 5 time stability | hard_gate | 2 | 2 | 0 | 0 |  | 1 | 0.16 | 100.00 |  |
| 6 deduplication | dedup | 2 | 2 |  |  | 0 |  | 0.16 | 100.00 | best 2 per cluster |
| 7 execution stress | hard_gate | 2 | 2 | 0 | 0 |  | 0 | 0.16 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 2 |  |  |  |  |  |  |  | diagnostic only: unverified: 2 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s2:hard_reject:completed_trades | 612 |
| s2:hard_reject:years_with_>=10_trades | 564 |
| s3:hard_reject:net_return | 462 |
| s3:hard_reject:sharpe | 532 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | time/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | 6J dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_413d` | timeframe=1min, leg=post, switch_offset=0, post_hold=eod, vol_gate=none, stop=none, anchor=ecb, direction=long, move=any, trend=counter, month=me | 0/105/0 | 105 | 3.6% | 0.7% | 0.75 | -1.2% | 581 | 1.60 | 5.3% | 42.1 | 2/4 | 1.00 | 0.57 | 0.19 | 3 | 2.0% | 0.46 | 0.80 | 2.9% | 2.3% | 3.4% | 3.1%/2.3% | 3.7 (interpolated) | pass | 0.037 (unverified) | -0.05 |
| 2 | `cfg_b8dc` | timeframe=1min, leg=post, switch_offset=0, post_hold=eod, vol_gate=none, stop=0.50, anchor=ecb, direction=momentum, move=big, trend=counter, month=any | 0/193/5 | 198 | 5.3% | 1.0% | 0.76 | -1.3% | 184 | 1.39 | 10.0% | 79.8 | 2/4 | 1.00 | 0.62 | 0.14 | 5 | 3.2% | 0.38 | 0.66 | 4.2% | 3.1% | 5.1% | 4.8%/3.7% | 3.4 (interpolated) | pass | 0.033 (unverified) | -0.77 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 1.0% / 1.04 / 20 | -0.3% / -0.28 / 25 | 1.5% / 1.83 / 17 | -0.3% / -0.31 / 22 | 1.6% / 1.58 / 21 |
| 2 | 2.0% / 2.36 / 34 | 0.4% / 0.51 / 40 | 0.2% / 0.13 / 40 | 0.8% / 0.94 / 39 | 1.8% / 0.78 / 45 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_413d` | 1 | n/a | n/a/n/a | n/a/n/a |
| 1 | `cfg_b8dc` | 1 | n/a | n/a/n/a | n/a/n/a |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 1.433e-03 over 1224 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 116.0, participation ratio 16.1, 95%-variance components 44 (rank bound T = 1292); raw grid 1224; raw + known prior 176925
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

- Bars: 1-minute bars with NY open time in [08:00, 17:00) only (fx_day_bars); each NY date is one session, so the session's last bar is the last bar before 17:00 ET and no position can be held overnight.
- Fix times per session date, each built in its own time zone and converted to New York: London 16:00 Europe/London (WM/R) and ECB 14:15 Europe/Berlin. The integrity check recomputes both with pandas tz conversion and compares them with the backtester's zoneinfo values.
- Switch time S = London fix + switch_offset. Pre leg: SHORT from the ECB fix to S. Post leg: LONG from S for post_hold minutes, or to the session's last bar for eod. Both: the pre trade then the post trade (they never overlap: the pre leg exits on the bar before the post leg enters).
- Entry at the OPEN of the first bar opening at/after the target time with market slippage; skipped when that bar opens more than 5 minutes late (a gap in the bars) or is not before the exit time.
- Time exit at the CLOSE of the last bar opening before the exit time, with market slippage; when that bar is the session's last bar the exit counts as a session (eod) exit.
- Stop (optional) = entry open x (1 -/+ stop%), live intrabar from the entry bar, filled at the worse of the bar's open and the stop with stop slippage.
- Vol gate, known at the session's open: v = sqrt(sum of squared log returns of 5-minute-bucket closes, 08:00-17:00 ET) per session; g = mean of v over the 20 sessions BEFORE this one; m = median of g over the last 250 sessions. high: g > m; low: g <= m; NaN (warm-up) -> no trade. Recomputed with plain loops in the integrity check.
- Long and short: P&L = side x (exit fill - entry fill) x quantity - commissions; sizing is the other families' (as many whole contracts as equity covers at full contract value, unlevered, compounding).
- Development backtests run on data physically truncated at the development end; the final session's trade is closed at the last development bar and flagged forced (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC; the 1-minute step there is taken as the roll spread). Point moves are preserved; pre-roll price levels are not real traded prices.
- Session: 08:00-17:00 ET of each NY date with data (NOT the 08:20-15:00 pit session the other 6E runs use), because the paper's post-London window runs to 17:00 ET. Globex bars before 08:00 and after 17:00 are never loaded into the strategy.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side (stops too) plus commission per contract per side, from the execution YAML; cost stress scales both.
- Every position is flat by 17:00 ET, so no trade straddles a roll (rolls happen at 00:00 UTC). The stop is a percent of the back-adjusted price; the back-adjustment on 6E is under 0.1 points, so the distortion is negligible.

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- The paper (Krohn, Mueller & Whelan, JF 2024) measured SPOT returns 1999-2019 and charged half the indicative spot spread; the futures evidence it cites starts in 2006. Nothing after 2019 was in the paper.
- Unlevered sizing: a post-London leg that earns ~5%/yr gross in the paper's levered-to-notional terms earns about the same here, so the 0.75 development Sharpe gate is demanding for a one-trade-a-day FX strategy.
- The pre-London leg (ECB fix to London fix) had no clear sign in the paper; it is in the grid as an exploratory leg and as one half of the paper's W shape.
- The pre-ECB (02:00-08:15 ET) and Tokyo legs are left out on purpose (no overnight trading), although the paper found the pre-ECB leg the strongest net of costs.
- 6J is the stage-9 transfer symbol. The paper found the yen moves the OTHER way after London, so 6J doing well with unchanged rules is a warning sign (sign or timing), not support.
- Days with a fix-time gap (no bar within 5 minutes after the target) are skipped; CME holidays with thin trading are traded if bars exist.
- Sizing ignores the stop distance (full equity per trade, as in the other families), so the percent stops change the exit, not the position size.
