# ICT / Smart Money Concepts: fit with the existing ablation framework

Scope: how to turn ICT/SMC setups into a look-ahead-free ablation grid of about 100-500 configs, where they overlap with families already tested, and which contracts to use. Intraday only, 1-minute bars, US Eastern time.

**Research limits (read first).** The local repository was read in full detail. Web access hit a rate limit after three calls. I got one primary web source: the full `smartmoneyconcepts/smc.py` source, fetched and analysed. I also got one search-results page on Silver Bullet backtests. LuxAlgo's documentation, TradingView Pine sources, the `smartmoneyconcepts` GitHub issues and other backtesters could **not** be fetched. Statements about them are listed under Gaps, not as findings. Local file links point into the repo; repo root = `/home/manit/Desktop/fun_projects/abalation_backtest`.

**Key local discovery.** The repo already contains a full ICT Silver Bullet implementation. It was the framework's original strategy, built on FMP SPY/QQQ data before the move to futures. It ships, unchanged, in every `*-backtest/src/strategies/ict_silver_bullet/`, with causal feature modules in `src/features/` (`swings.py`, `fvg.py`, `sweeps.py`, `liquidity.py`, `market_structure.py`, `displacement.py`, `bias.py`, `sessions.py`) and unit tests (`tests/unit/test_fvg.py`, `test_sweeps.py`, `test_swings.py`, `test_silver_bullet_config.py`). A 400-config random-search pilot on SPY was run in Aug 2026 (results below). It was never run through the current futures funnel.

---

## 1. Which already-tested families overlap with ICT ideas, and what did they show?

### Takeaway
ICT's main ideas map closely onto five families already tested. NY-open/opening-range momentum maps to **noise-band**. Fading a stop-run maps to **drift-burst fade** and **mean reversion**. The London close maps to the **FX-fix reversal**. Displacement out of consolidation maps to the **squeeze breakouts**. The overlap results are a warning. The only open-session edge that survived is a *continuation* (noise-band), and only on NQ. Every *fade-the-extreme-move* family failed after costs (drift-burst 0 survivors out of 10,944 configs, FX-fix 0 of 405 profitable). The existing ICT Silver Bullet pilot on SPY is indistinguishable from noise (median PF 1.005).

### Cited Findings

**The ICT Silver Bullet pilot already in the repo (SPY, 2018-2026, equity costs)**
- Run `spy_pilot_400`: 400 randomly sampled Silver Bullet configs on SPY 1-min data. 182 completed with metrics, 38 crashed on a Polars schema error (`"ny_pm"` builder error), and the rest have no result file. Trades span 2018-01-03 to 2026-08-14. There is **no dev/validation/holdout split**: it is one whole-history backtest per config. — [runs/manifests/experiment_spy_pilot_400.json](channel-breakout-backtest/runs/manifests/experiment_spy_pilot_400.json); [runs/results/experiment_id=spy_pilot_400/](channel-breakout-backtest/runs/results/experiment_id=spy_pilot_400/) (aggregated by me)
- Across the 182: median Sharpe 0.06 (max 2.82), median profit factor 1.005 (max 1.42), 53% with PF > 1, median 802 trades (~93/yr), and a median limit-order fill rate of 0.44. — same source (my aggregation)
- Per-axis median PF: entry at FVG midpoint 1.034 / distal 1.032 / proximal 0.974. Stop at swept extreme 1.027 / swing 1.008 / FVG distal 0.955. MSS required 1.027 vs not required 0.984. Target R-multiple 1.005 vs end-of-window 1.007. — same source (my aggregation)
- By window (net P&L across configs): the NY AM (10:00-11:00) leg was profitable in only 42% of configs (median −$980). The NY PM (14:00-15:00) leg was profitable in 58% (median +$1,056). Longs were profitable in 42% of configs, shorts in 53%. — same source
- The pilot had no London window (FMP had no pre-market bars). Its daily-bias modes were disabled because daily bars were never wired in, and its trial count was flagged as unknown. — [ASSUMPTIONS.md](ma-crossover-backtest/ASSUMPTIONS.md) (sections "Data coverage limitation" and "Known gap: daily-bar bias modes"; DSR note "The ICT search's trial count is unknown")
- Example config from the pilot: 1-min FVG, swing 7/9, sweep reclaim within 5 bars, MSS required on close, FVG-distal stop, end-of-window target → 344 trades, win rate 22.7%, net −$434. — [cfg_7a7684ef154b871a4220.json](channel-breakout-backtest/runs/results/experiment_id=spy_pilot_400/cfg_7a7684ef154b871a4220.json)

**Noise-band breakout (Zarattini et al.): closest to the "NY open" / opening-range ideas**
- NQ v2 (3,456 configs, 15m): 374 finalists, all 374 passed 2023-24. Median finalist Sharpe 1.58, PF 1.43, drawdown −2.7%, and it beat 98% of random-entry runs. A band lookback of 1 day stood out (median Sharpe 2.09). — [notes/NQ/noise_band_v2.html](futures-results/notes/NQ/noise_band_v2.html)
- NQ v2 #1 on the 2025+ holdout: +10.3%, Sharpe 0.65, beat 86% of random runs. — git commit e84559a
- ES v4 pick pair (5m #17 + 15m #104) on the 2025-01-01..2026-10-19 holdout: −2.4%, Sharpe −0.20, PF 0.94, 491 trades. — [data/ES/noise_band_portfolio_v4_holdout.json](futures-results/data/ES/noise_band_portfolio_v4_holdout.json)
- On other markets (2018-22): RTY 0% of versions profitable, ZN 0%, YM 58% (median Sharpe 0.09), CL 17%. Commit note: "The edge is Nasdaq-specific." — git commit e1aeaf5

**Drift-burst fade: closest to "liquidity sweep → reversal" / turtle soup in mechanism (fade an extreme short-horizon move)**
- db_es_v1: 0 of 576 passed the profit gate. db_es_v2 (10,368 configs, adding entry mode, target, stop and trades per session): 0 survivors, best Sharpe 0.47, PF 1.42 on 63 trades. — git commit d7cd024; [drift_burst/config.py docstring](last-half-hour-backtest/src/strategies/drift_burst/config.py)

**FX-fix reversal: overlaps with ICT's "London close" killzone idea**
- fx_6e_v1: 0 of 405 configs made money (best PF 0.96). "The post-London edge is far smaller than costs." — git commit 05d9b26
- The family traded the post-London-fix USD reversal on 6E, with the London fix built in London time and converted per date (12:00 ET in DST-mismatch weeks). — [fx_fix/config.py](last-half-hour-backtest/src/strategies/fx_fix/config.py)

**Mean reversion: overlaps with "fade the stop run" and with discount/premium (equilibrium) ideas**
- ES v6 15m: 0 of 7 finalists passed 2023-24. A volatility length of 21 was a "knife edge". — [notes/ES/mean_reversion_v6__15m.html](futures-results/notes/ES/mean_reversion_v6__15m.html)
- NQ v7 15m: 6 of 8 passed, but weakly (Sharpe 0.39-0.74). "Not better than luck": the median finalist beat 53% of random-entry runs. — [notes/NQ/mean_reversion_v7__15m.html](futures-results/notes/NQ/mean_reversion_v7__15m.html)

**Squeeze breakouts (BB/KC, NR-N): overlap with "consolidation → displacement"**
- BB/KC NQ v3 15m: 439 of 567 finalists passed 2023-24 (median Sharpe 0.81), and the best beat 99% of random runs. "Search-adjusted, nothing is significant": the highest deflated Sharpe was 0.63 against a 0.95 bar, after ~990 effective trials. — [notes/NQ/squeeze_breakout_v3__15m.html](futures-results/notes/NQ/squeeze_breakout_v3__15m.html)
- NQ squeeze holdout picks 15m #7 + 5m #13: +7.7%, Sharpe 0.75. YM, GC and CL picks failed. — git commit a1a24e9

**Last-half-hour momentum (NQ/ES): relevant to the ICT "PM session / last hour" ideas**
- NQ: 16 of 56 finalists passed 2023-24, all in the 15:00-16:00 window. Holdout #49 Sharpe 0.19, #56 −0.59. ES: 1 of 500 passed the profit gate and failed 2023-24. — [notes/NQ/last_half_hour_v1.html](futures-results/notes/NQ/last_half_hour_v1.html); [notes/ES/last_half_hour_v1.html](futures-results/notes/ES/last_half_hour_v1.html)

**EMRT ES-NQ intraday spread: overlaps with ICT "SMT divergence" (ES vs NQ disagreeing at a high or low)**
- emrt_esnq_v2 (intraday, flat by close): 6 frozen, 0 of 6 passed 2023-24. — git commit 7eae686

**External (secondary) evidence on the Silver Bullet itself**
- A TradingView indicator author ("Silver Bullet [GBB]") reports testing the rules on Sierra Chart 1-min ES, NQ, YM and GC data, 2011-2026, all 23 hours, with 2 ticks slippage and $4.50 round-trip commission. They conclude the rules did not make the model profitable, and that in an "hour-scan" the Silver Bullet hours were no better than other hours that move just as much on ES, NQ or YM. — [TradingView: Silver Bullet [GBB]](https://br.tradingview.com/script/teL2dDvS-Silver-Bullet-GBB/) (seen only as a search summary; the page could not be fetched to verify)
- A summary of a YouTube "25,000 Silver Bullet variants" study (16 years of 1-min NQ/ES) says profitable variants clustered around a 52% win rate, not the 70-80% claimed in the ICT community. The original study could not be located, so this is **unverified**. — [gist.ly summary](https://gist.ly/youtube-summarizer/i-backtested-25000-ict-silver-bullet-trades)

### Inferences
- The ICT "Judas swing" fades the first move out of the overnight range at the NY open. That is the **opposite sign** of noise-band, the only open-session family with an edge that survived the NQ holdout. An ICT open-fade grid should therefore carry a **continuation control arm** (same trigger, trade in the break direction). Then the result shows whether the "sweep" framing adds anything beyond the known NQ open momentum.
- Drift-burst and FX-fix failures suggest that fading short-horizon extremes on 1-min bars rarely clears 1 tick + $2.50/side. A sweep-reversal grid should expect the same cost wall. Its stops are tighter (the sweep extreme), which makes costs a larger fraction of R (see section 2).
- In the SPY pilot, PM beat AM and shorts beat longs. This hints that the Silver Bullet's two windows are not interchangeable and that the **window** should be an explicit categorical axis with a placebo hour, not pooled. The pilot is unsplit SPY with equity costs, so this is weak evidence.
- A Silver Bullet result that "beats random entry" may only be picking up time-of-day volatility. GBB's hour-scan finding argues for including **placebo windows** (e.g. 11:00-12:00, 12:00-13:00) as grid levels, not just as a post-hoc luck benchmark.

### Gaps
- The SPY pilot has no per-split metrics. The 2018-22 / 2023-24 / 2025+ breakdown would need trade parquet re-slicing (the parquet files exist under `runs/trades/experiment_id=spy_pilot_400/`). Not done here (read-only brief).
- GBB's exact numbers (per-hour expectancy, sample sizes) and the 25k-variant study's methodology could not be verified (web fetch blocked).
- No independent, peer-reviewed test of any ICT setup was found in the limited search.

---

## 2. How do open-source ICT/SMC implementations detect swings, FVGs, order blocks and sweeps, and where do they leak future data?

### Takeaway
The popular `smartmoneyconcepts` Python package (joshyattridge) is **non-causal in almost every function**. It writes swings, FVGs, order blocks, BOS/CHoCH and liquidity sweeps at the *formation* bar using later bars. It fills mitigation/broken/swept indices by forward scans, and the liquidity tolerance uses the whole dataset's range. Only `previous_high_low` and `sessions` are causal. The repo's own `src/features/` layer already does what the package does not: each object carries an explicit `availability_ts` / `confirmation_ts`. It is the right base. Wrap or port it; do not import the package.

### Cited Findings
**`smartmoneyconcepts/smc.py` (primary source, read directly)** — [smc.py on GitHub](https://raw.githubusercontent.com/joshyattridge/smart-money-concepts/master/smartmoneyconcepts/smc.py)
- **Swings:** the default `swing_length=50` is doubled to a 100-bar centred window: `high == high.shift(-(swing_length // 2)).rolling(swing_length).max()`. A swing at bar k is confirmed only 50 bars later but labelled at k. The consecutive-swing filter and the first/last-point flips also write into recent bars.
- **FVG:** bullish when `high.shift(1) < low.shift(-1)` with a bullish middle candle. `Top = low.shift(-1)` (a future candle), and the gap is stored on the middle candle i, though it is only knowable after candle i+1 closes.
- **FVG `MitigatedIndex`:** a forward scan from i+2 for the first touch, written back to row i. Unmitigated rows hold `0`, which is ambiguous with index 0.
- **`join_consecutive=True`:** merges adjacent same-sign FVGs into the last bar of the run, and the merge happens before mitigation. Max-top/min-bottom are taken regardless of direction.
- **Order blocks:** use the *whole-dataset* swing series, so at bar c they can reference swings confirmed later. The OB is detected at the break bar but written to the earlier candle. The bullish vs bearish `MitigatedIndex` differs by one bar (`close_index - 1` vs `close_index`). In the default case Top/Bottom are swapped.
- **Liquidity:** the tolerance `pip_range = (high.max() - low.min()) * range_percent` uses the max/min over the **entire dataset**. `Swept` is the first later candle reaching the band (forward scan). If nothing sweeps, grouping keeps running to the end of the data.
- **BOS/CHoCH:** need four confirmed swings (already ~50 bars late), and the label is written to a swing two positions back. `BrokenIndex` is a forward scan. **Unbroken BOS/CHoCH rows are deleted afterwards**, so whether a signal *exists* depends on future prices (survivorship look-ahead).
- **Causal parts:** `previous_high_low` uses the previous *completed* period (with a boundary off-by-one when a candle timestamp equals a period start: `searchsorted(side='left')`). `sessions` uses only current and past bars, but mutates the caller's DataFrame index.

**The repo's own feature layer (causal by construction)**
- Swings are N-bar fractals with explicit `availability_ts = bar[i+R].bar_close_ts`. Consumers must filter on `availability_ts`, never `pivot_ts`. — [src/features/swings.py](last-half-hour-backtest/src/features/swings.py)
- A 3-bar FVG has `confirmation_ts = bar3.bar_close_ts`, and touches are searched from the first bar strictly after confirmation (`source_row_index + 3`). — [src/features/fvg.py](last-half-hour-backtest/src/features/fvg.py)
- A sweep = penetration of an already-available level, then a close back across within K bars. Only levels with `availability_ts <=` the penetration bar's open are eligible. Levels expire after 500 bars by default. — [src/features/sweeps.py](last-half-hour-backtest/src/features/sweeps.py)
- Prior-session levels become available at the current session's open, and pre-window levels freeze at window start. **Overnight/extended-hours highs and lows are explicitly NOT implemented**, because the module was written for RTH-only FMP data ("If extended-hours data becomes available, this module must be revisited"). — [src/features/liquidity.py](last-half-hour-backtest/src/features/liquidity.py)
- The Silver Bullet signal sets the earliest entry to `max(FVG confirmation, MSS break bar, first touch)`. Every rejected candidate is logged with a reason. — [ict_silver_bullet/signals.py](last-half-hour-backtest/src/strategies/ict_silver_bullet/signals.py)
- Same-bar stop/target ambiguity defaults to `stop_first`, with the trade flagged `intrabar_ambiguous`. — [ASSUMPTIONS.md "Strategy conventions"](ma-crossover-backtest/ASSUMPTIONS.md)

**Futures data specifics that affect ICT levels**
- Futures bars are Databento `GLBX.MDP3 ohlcv-1m`, continuous front month by volume, difference back-adjusted at each roll. Databento rolls at 00:00 UTC. `session_date_ny` is the CME trading date for non-RTH bars (bars from 18:00 NY belong to the next day). — [src/data/futures.py](last-half-hour-backtest/src/data/futures.py)
- Costs in the funnel: $2.50/contract/side commission + 1 tick slippage per side on market and stop fills; $1M equity. — [configs/execution/futures.yaml](last-half-hour-backtest/configs/execution/futures.yaml)

### Inferences
- **Implementation pitfalls checklist** for an ICT family in this framework:
  1. *Pivot confirmation:* any "swing high/low", "BOS", "CHoCH", "MSS" or "order block" must use `availability_ts`. Do not port smc.py's centred `shift(-n)` logic or its "delete unbroken BOS" step.
  2. *FVG timing:* the gap exists at bar-3 close. A limit order at the FVG edge or at consequent encroachment (CE, the midpoint) can only rest from the **next** bar. The local code already does this.
  3. *Limit-fill realism:* on 1-min OHLC a "touch" of the CE is not a fill. Require a trade-through by ≥1 tick, or fill at the limit only if `low < limit` (long). The SPY pilot's median fill rate of 0.44 shows how much the result depends on this rule. Treat it as a stress axis in the cost stage, not a grid axis.
  4. *Same-bar ambiguity:* ICT stops sit a few ticks beyond a sweep wick, so stop and target are often both inside one 1-min bar. Keep `stop_first` and report the `intrabar_ambiguous` share per config.
  5. *Cost-to-R ratio:* using standard contract specs (ES $50/pt with a 0.25 tick, NQ $20/pt with a 0.25 tick), the funnel's round-trip cost is about 0.6 ES points and 0.75 NQ points. An ICT stop of 3-5 ES points or 10-20 NQ points pays 4-20% of R in costs per trade. Add a **minimum stop distance** (e.g. ≥ 8 ticks or ≥ k×ATR) so the grid does not search sub-cost stops.
  6. *Sizing:* whole contracts on $1M unlevered means few contracts (about 2 NQ or 3-4 ES at current notional). The R-based risk sizing in `SilverBulletConfig` (0.25% risk) does not apply. Size by notional as in the other futures families.
  7. *Overnight levels and rolls:* the Asian range (19:00-00:00 ET) straddles Databento's 00:00 UTC roll on roll days. Compute ON/Asia/London highs and lows on the back-adjusted series, so the distance to the RTH price is consistent, and exclude or flag roll dates.
  8. *DST:* ICT windows are quoted in NY time. The London open (02:00-05:00 ET) shifts against London time in the weeks when US and UK daylight saving disagree. Use the fx-fix approach (build in the venue's zone, convert per date) and decide explicitly which clock the window follows.
  9. *Placebo and luck:* time-of-day volatility makes any window look special. Include placebo windows in the grid and keep the random-entry benchmark at the same time-of-day.
  10. *Discretion → trial count:* ICT rules are loosely defined (swing length, "displacement", "draw on liquidity"). Fix the definitions in code before the run and count every definitional variant as a trial for DSR. The pilot's "trial count is unknown" is exactly the problem to avoid.
  11. *Random sampling vs lattice:* the pilot sampled continuous values at random (e.g. `displacement_true_range_atr_threshold=2.997`). The current funnel's local-perturbation stage needs a discrete lattice, so define each axis as a short list of levels.
  12. *Known code issues to fix before reuse:* the pilot's Polars schema error (38 configs failed on the `sb_window` builder); `TRADABLE_WINDOWS` hard-blocks `london`; `bias_mode` is restricted to `none` because no daily bars are wired in; `liquidity.py` has no overnight levels; equity sizing/costs.

### Gaps
- LuxAlgo SMC (TradingView): I could not read its documentation or source. Its swing "length" / internal-vs-swing structure and whether its historical labels repaint are **unverified** here. Pine `ta.pivothigh(left, right)` also confirms only after `right` bars, but this could not be source-checked this session.
- Whether `smartmoneyconcepts` has open GitHub issues acknowledging look-ahead was not checked (search blocked).
- Other GitHub ICT backtesters (backtesting.py/vectorbt examples) were not reviewed.

---

## 3. Candidate setups and concrete ablation grids (about 100-500 configs each)

### Takeaway
The five most codeable ICT setups each reduce to a few discrete axes, and most of the code already exists in `src/features/`. Ranked by fit (overlap-informed): **(A)** NY-open sweep of the overnight/prior-day range with a continuation control, the most direct test against noise-band. **(B)** Silver Bullet FVG with placebo windows, reusing the existing strategy. **(C)** a generic FVG retracement after displacement. **(D)** a London/Asian range raid, on 6E/GC only. **(E)** a prior-day high/low turtle-soup reversal all day. Each grid below is sized to 216-432 configs.

### Cited Findings (axis levels grounded in existing code or results)
- The existing config already exposes these knobs: `fvg_entry_rule` (proximal/midpoint/distal/first_touch), `fvg_min_points/bps/atr_multiple`, `fvg_max_age_bars`, `swing_left/right_bars`, `sweep_k_bars`, `sweep_min_penetration_*`, displacement TR/ATR and body/ATR toggles, `require_market_structure_shift` + `mss_break_mode` + `mss_max_bars_after_sweep`, `stop_type` (swing/fvg_distal/swept_extreme/fixed/atr), `target_type` (r_multiple/liquidity/fixed/end_of_window/end_of_session/max_holding_time). — [ict_silver_bullet/config.py](last-half-hour-backtest/src/strategies/ict_silver_bullet/config.py)
- Windows are hard-coded as London 03:00-04:00, NY AM 10:00-11:00 and NY PM 14:00-15:00, half-open, NY time. — [src/utils/config_models.py](last-half-hour-backtest/src/utils/config_models.py)
- Pilot evidence on axis importance (SPY): the entry at proximal is the weakest (median PF 0.974); the swept-extreme stop beats the FVG-distal stop (1.027 vs 0.955); requiring an MSS helps slightly (1.027 vs 0.984); the target type barely matters. — section 1 aggregation of [spy_pilot_400](channel-breakout-backtest/runs/results/experiment_id=spy_pilot_400/)
- The recent family spec pattern is about 5 categorical axes × 2-5 levels = 500 configs, with fixed rules stated in the docstring (one trade per session, flat nightly, next-bar-open fills). — [last_half_hour/config.py](last-half-hour-backtest/src/strategies/last_half_hour/config.py)
- On NQ, noise-band's strongest variant used a 1-day lookback, 30-60 min momentum confirmation and VWAP exits. — [notes/NQ/noise_band_v2.html](futures-results/notes/NQ/noise_band_v2.html)

### Inferences: proposed grids
All grids share these fixed rules: 1-min bars; signal on bar close, fill at next bar open (market) or a resting limit from the bar after confirmation; at most one trade per session; flat by 16:00 ET (or by the window end where stated); whole contracts sized by notional; stop live intrabar with `stop_first`; a minimum stop distance of 8 ticks (reject the setup otherwise). Every swing, FVG and level uses `availability_ts`.

**(A) NY-open overnight-range sweep: "Judas swing" vs continuation (NQ primary, ES transfer). 432 configs.**
- Trigger: between 09:30 and 09:30+`window`, price trades beyond `level` by ≥ `pen` and then closes back inside within `k` bars → fade (Judas). The `mode=continuation` arm trades the same penetration in the break direction (the noise-band-like control).
- `level`: ONH/ONL (18:00-09:30 Globex) · PDH/PDL (prior RTH) · London H/L (02:00-05:00) · Asia H/L (19:00-00:00) — 4
- `window` (minutes after 09:30 in which the sweep may occur): 15, 30, 60 — 3
- `confirm`: reclaim close within k=1 · k=3 bars · reclaim + MSS (close beyond the last available 1-min swing, swing 3/3) — 3
- `mode`: fade · continuation — 2
- `stop`: sweep extreme + 2 ticks · 1.0 × 14-bar 1-min ATR beyond the entry — 2
- `exit`: 2R · opposite side of the same range ("draw on liquidity") · time exit 12:00 ET — 3
- 4×3×3×2×2×3 = **432**. The `continuation` levels are a built-in control. If fade loses and continuation wins, this collapses into noise-band.

**(B) Silver Bullet FVG with placebo windows (reuse `ict_silver_bullet`). 360 configs.**
- `window`: 10:00-11:00 · 14:00-15:00 · 03:00-04:00 (London; needs Globex bars, possible now) · placebo 11:00-12:00 · placebo 12:30-13:30 — 5
- `fvg_min`: 0 · 0.5×ATR · 1.0×ATR (ATR at confirmation) — 3
- `entry`: FVG proximal edge · CE (midpoint) — 2 (distal dropped: lowest fill rate; proximal kept as the "worst" in the pilot for contrast)
- `stop`: FVG far edge · swept extreme — 2
- `target`: 2R · nearest opposing available liquidity · end of window — 3
- `require_sweep_before_fvg`: yes (classic) · no (FVG-only control) — 2
- Fixed: swing 5/5, sweep k=3, MSS off (or fixed on; do not grid it), displacement TR ≥ 1.5 ATR on the FVG middle bar, FVG max age 30 bars, limit must fill inside the window.
- 5×3×2×2×3×2 = **360**. The placebo windows test GBB's claim directly. The sweep toggle tests whether "liquidity" adds anything to a plain FVG.

**(C) FVG retracement after displacement, any time 09:45-15:30 (NQ, ES). 288 configs.**
- `tf` for FVG detection: 1m · 5m — 2
- `displacement`: middle-bar true range ≥ 1.5 · 2.0 · 3.0 × ATR(14) — 3
- `entry`: proximal · CE — 2
- `max_wait` for the retrace fill: 5 · 15 · 30 bars — 3
- `stop`: FVG far edge · first bar (bar 1) extreme — 2
- `exit`: 1.5R · 3R · time exit after 30 min (with stop) — 3
- `trend_gate`: off · trade only in the direction of price vs session VWAP — 2 (×) → 2×3×2×3×2×3×2 = 432. Drop `tf=5m` to get **216**, or keep 432.
- This is the *continuation* counterpart of drift-burst (which faded bursts and failed). The two together bracket the "extreme 1-min move" question.

**(D) London/Asian range raid (6E primary, GC transfer; ES/NQ as a check). 324 configs.** *Requires deciding whether 02:00-11:00 ET trades count as "intraday"; the FX-fix family used an 08:00-17:00 ET envelope.*
- `range`: Asia (19:00-00:00) · Asia+early (19:00-02:00) · prior NY session (08:00-17:00) — 3
- `raid_window`: London open 02:00-05:00 · NY open 08:00-11:00 · both — 3
- `confirm`: reclaim k=1 · k=3 · reclaim + 1-min FVG in the fade direction — 3
- `stop`: raid extreme + 2 ticks · 1×ATR — 2
- `exit`: range midpoint (equilibrium) · opposite range edge · time exit 11:00 ET (the "London close" killzone) — 3
- `pen_min`: 0 · 0.25×range height — 2
- 3×3×3×2×3×2 = **324**.

**(E) Prior-day high/low turtle soup, all RTH (ES, NQ, YM). 216 configs.**
- `level`: PDH/PDL · prior-week H/L · both — 3
- `pen`: any · ≥ 4 ticks · ≥ 0.1×daily ATR — 3
- `reclaim_k`: 1 · 5 bars — 2
- `entry`: market at the reclaim close · limit at the level retest — 2
- `stop`: extreme + 2 ticks · 2× penetration distance — 2
- `exit`: 2R · VWAP · 16:00 — 3
- 3×3×2×2×2×3 = **216**. Overlaps mean reversion and drift-burst; cheap to run and a useful negative control.

**Ordering suggestion:** start with (B) on NQ, since the code exists and it settles the "Silver Bullet" question with a built-in placebo. Then (A) on NQ, which tests ICT against the one edge the user has. (C) and (E) are cheap follow-ups. Run (D) only if the London-hours trading envelope is accepted.

**Axes deliberately left out (fix them, don't grid them):** order-block definitions (most ambiguous, and smc.py's version is non-causal); "daily bias" / premium-discount / PD-array hierarchy (needs a definition the user signs off on first; the existing `bias.py` modes need daily bars wired in); SMT divergence (cross-market; the EMRT ES-NQ results suggest low prior); breaker/mitigation blocks.

### Gaps
- No external source was available this session to confirm canonical ICT parameter values: Silver Bullet window times beyond the repo's convention, the CE definition, or Judas-swing timing. The levels above are design proposals, not sourced ICT rules.
- The effect of the 8-tick minimum stop on trade counts is unknown until run. It may push some grids below the funnel's 100-trades/yr or 40-trade validation minimums.

---

## 4. Which contracts are most appropriate?

### Takeaway
Use **NQ** as the development contract and **ES** as the transfer. NQ is where ICT is mostly traded, and NQ is the only market where an open-session momentum edge survived the user's own holdout, so an ICT test there has a meaningful comparison. Use **6E** (and GC) only for the London/Asia range-raid grid. Skip RTY, ZN and ZB for open-based grids, because noise-band found nothing there.

### Cited Findings
- Noise-band versions profitable on 2018-22: NQ very high (86% cleared Sharpe ≥ 0.75), YM 58% (median Sharpe 0.09), CL 17%, RTY 0%, ZN 0%. ES pick pair lost on the holdout (Sharpe −0.20); NQ #1 made +10.3% (Sharpe 0.65). — git commits e1aeaf5, e84559a; [NQ noise_band_v2 note](futures-results/notes/NQ/noise_band_v2.html); [ES holdout json](futures-results/data/ES/noise_band_portfolio_v4_holdout.json)
- The squeeze (displacement-like) holdout survived on NQ (+7.7%, Sharpe 0.75) and RTY #101 (Sharpe 0.96), and failed on YM, GC and CL. — git commit a1a24e9
- Available 1-min futures: ES, NQ, RTY, YM, CL, GC, ZN, ZB, 6E, 6J from Databento GLBX, including Globex hours (non-RTH bars carry the CME trading date). — [src/data/futures.py](last-half-hour-backtest/src/data/futures.py); [test-dabento/main.py](test-dabento/main.py)
- The FX-fix family already handles European fix times in their own time zones on 6E. — [fx_fix/config.py](last-half-hour-backtest/src/strategies/fx_fix/config.py)
- The GBB author's Silver Bullet test (ES, NQ, YM, GC; 2011-2026) found no edge on ES, NQ or YM vs equally volatile hours. — [TradingView Silver Bullet [GBB]](https://br.tradingview.com/script/teL2dDvS-Silver-Bullet-GBB/) (search summary only)

### Inferences
- NQ 2023-24 and 2025+ have already been seen through noise-band, mean reversion, squeeze, LHH, month-end and convexity. An ICT holdout on NQ is therefore "previously inspected" in the funnel's sense. Label it as such, as the LHH note did.
- ES as the transfer contract is a strict test, since ES failed noise-band and LHH. An ICT config that transfers to ES would be more convincing than one that only works on NQ.
- For London/Asia grids, 6E has the longest active session around 02:00-11:00 ET. GC is a secondary choice (London AM/PM fixes), with the caveat that GC squeeze picks failed the holdout.

### Gaps
- Databento `ohlcv-1m` likely has no bar for minutes with no trades. Overnight NQ/ES and the Asian session for 6E may therefore have sparse minutes, which affects range highs/lows and k-bar reclaim counts. This was not verified for this dataset.
- No external evidence was retrieved comparing ICT setups across specific contracts beyond the GBB summary.
