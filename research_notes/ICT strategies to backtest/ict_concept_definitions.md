# ICT / Smart Money Concepts: mechanical definitions and free parameters for a 1-minute CME futures ablation grid

Scope note: no full verbatim ICT transcript could be fetched (innercircletrader.net pages were mostly ads plus base64 images; the YouTube transcripts were reachable only through AI-summary sites). "ICT's own definition" below therefore comes from faithful-summary sources (innercircletrader.net, LuxAlgo's ICT concept library, episode summaries of the 2022 Mentorship) and is labelled that way. The code-level definitions were read directly from source: `smartmoneyconcepts/smc.py` (joshyattridge, master branch, 987 lines, downloaded 2026-11-22) and the Pine v5 source of LuxAlgo "Smart Money Concepts" (a public gist fork that keeps the LuxAlgo code and CC BY-NC-SA header).

Source abbreviations used below:
- **smc.py**: https://github.com/joshyattridge/smart-money-concepts/blob/master/smartmoneyconcepts/smc.py
- **Lux-SMC Pine**: https://gist.github.com/niquedegraaff/8c2f45dc73519458afeae14b0096d719 (fork of the LuxAlgo SMC script, https://www.tradingview.com/script/CnB3fSph-Smart-Money-Concepts-SMC-LuxAlgo/)
- **Lux-ICT**: https://www.tradingview.com/script/ib4uqBJx-ICT-Concepts-LuxAlgo/
- **LuxLib/<slug>**: https://www.luxalgo.com/library/concept/<slug>/

---

## 1. Fair value gap (FVG), BISI/SIBI, inversion FVG, consequent encroachment, related imbalances

### Takeaway
Every source agrees on the core 3-candle rule: a bullish FVG exists when low[3] > high[1], and the gap runs from high[1] to low[3]; the bearish case is the mirror. They disagree on (i) whether the middle candle must close in the gap direction or close beyond candle 1's extreme, (ii) the minimum-size filter, and (iii) what counts as "mitigated/filled" (touch of the near edge, touch of CE, or a trade through the far edge, by wick or by close). These three choices are the main ablation axes. Watch out: smc.py stamps the FVG on the middle bar, one bar before it can be known.

### Cited Findings
- **ICT/summary definition:** a three-candle imbalance. When the middle candle moves so fast that candle 1's high and candle 3's low do not overlap (bullish), the untraded span between them is the gap. A bearish FVG spans candle 1's low to candle 3's high. — [LuxLib/fair-value-gap](https://www.luxalgo.com/library/concept/fair-value-gap/)
- **BISI = Buy-side Imbalance, Sell-side Inefficiency** (bullish FVG). **SIBI = Sell-side Imbalance, Buy-side Inefficiency** (bearish FVG). The zone lies between candle 1 and candle 3. The page says a lower-timeframe market structure shift is needed for a high-probability entry. — [innercircletrader.net SIBI/BISI](https://innercircletrader.net/tutorials/sibi-and-bisi-the-ict-concepts/). Caveat: a search summary flagged that this page has a garbled section, with the BISI text under the SIBI heading.
- **Consequent encroachment (CE)** is the 50% midpoint of an FVG: CE = (upper + lower)/2, with bullish lower = H1 and upper = L3. "A touch of CE is a partial fill, and trading through the far boundary is a full fill." ICT also applies CE to the midpoint of a candle wick. The order-block equivalent is the **mean threshold**, the 50% of the block's range. — [LuxLib/consequent-encroachment](https://www.luxalgo.com/library/concept/consequent-encroachment/)
- CE has "no independent statistics behind it". Stops just past CE ("strict-respect model") and stops beyond the far edge ("full-gap model") are two different trades. — [LuxLib/consequent-encroachment](https://www.luxalgo.com/library/concept/consequent-encroachment/)
- **Inversion FVG (IFVG):** an FVG that price has closed through. "The common requirement is a candle body closing beyond the far side of the gap; a wick-through alone is usually read as a probe." After that the zone flips polarity and the first retest is the trade. — [LuxLib/inversion-fvg](https://www.luxalgo.com/library/concept/inversion-fvg/)
- **Balanced price range (BPR):** the intersection (not the union) of a bullish and a bearish FVG that overlap. Bias comes from the newer gap. — [LuxLib/balanced-price-range](https://www.luxalgo.com/library/concept/balanced-price-range/)
- **Volume imbalance:** a gap between the real bodies of two consecutive candles (close[1] to open[0]) while the wicks still overlap. No volume data is used. If even the wicks don't overlap, it is an opening gap instead. — [LuxLib/volume-imbalance](https://www.luxalgo.com/library/concept/volume-imbalance/)
- **Lux-ICT "Implied FVG":** adjacent shadows overlap, and the gap is built from the average of each shadow and the nearest end of its candle body. — [Lux-ICT](https://www.tradingview.com/script/ib4uqBJx-ICT-Concepts-LuxAlgo/)
- **smc.py `fvg()`:** bullish when `high.shift(1) < low.shift(-1)` AND the middle candle `close > open`; bearish when `low.shift(1) > high.shift(-1)` AND `close < open`. Top/bottom = low[i+1]/high[i-1] (bull). The signal is stamped on the middle bar i, which uses bar i+1 (`shift(-1)`), so it has **one bar of look-ahead** if used as-of bar i. `MitigatedIndex` is the first bar j ≥ i+2 with `low <= top` for a bull gap, i.e. any touch of the near edge counts as mitigation. `join_consecutive=True` merges same-direction FVGs on consecutive bars into one (highest top, lowest bottom). There is no size filter. — [smc.py](https://github.com/joshyattridge/smart-money-concepts/blob/master/smartmoneyconcepts/smc.py)
- **Lux-SMC Pine FVG:** bullish when `low > high[2] and close[1] > high[2] and delta_per > threshold`. Here `delta_per = (close[1]-open[1])/open[1]*100`, the middle-candle body in %. Note the middle candle must **close above candle 1's high**, which is stricter than "bullish candle". Auto threshold = `ta.cum(abs(delta_per))/n * 2`, i.e. 2x the cumulative mean absolute body % since chart start (default `fvg_auto = true`). A higher-timeframe option goes through `request.security`. The box is split at CE (two halves). A bull FVG box is deleted when `low < bottom`, i.e. a wick through the far edge = full fill. `Extend FVG` default 1 bar. Detection happens on the close of candle 3, so it is causal. — [Lux-SMC Pine](https://gist.github.com/niquedegraaff/8c2f45dc73519458afeae14b0096d719)
- LuxAlgo notes that "raw three-candle gaps print constantly, so most tools require a minimum size (ATR- or percentage-based) or confluence with market structure". — [LuxLib/fair-value-gap](https://www.luxalgo.com/library/concept/fair-value-gap/)

### Inferences
- **Free parameters for FVG (ablation grid):**
  1. Middle-candle direction rule: none / close>open / close > H1 (Lux) / body ≥ x% of range.
  2. Minimum gap size: none / ≥ k ticks / ≥ a·ATR(n) / ≥ b·median range / Lux auto (2x cumulative mean body%). The Lux auto threshold depends on where the data starts; for a backtest, replace it with a rolling window.
  3. Displacement filter on the middle candle: body ≥ c·ATR(n), or range z-score.
  4. Merge consecutive gaps (smc `join_consecutive`) yes/no.
  5. Entry level inside the gap: near edge / CE / far edge.
  6. "Respected" rule: price enters the gap and closes back outside on the same side without closing beyond CE (strict), or without closing beyond the far edge (loose).
  7. "Filled/invalidated" rule: wick through the far edge (Lux) / close through the far edge (IFVG rule) / close through CE.
  8. Expiry: N bars, end of session, or first touch only (first-touch-only is the common "first return" convention).
  9. Gap source timeframe: 1m, or HTF gaps (5m/15m) projected onto 1m.
  10. Tick-size rounding: on ES (0.25), a 1-tick gap is legal but meaningless, so a tick floor matters.
- **IFVG parameters:** body-close vs wick-close beyond the far edge; how long the inverted zone stays alive; whether the original gap must first have been "respected" once.
- To make smc.py causal, shift its FVG output forward by one bar (signal known at the close of i+1).

### Gaps
- I could not retrieve a verbatim ICT transcript saying whether ICT requires the middle candle to close beyond candle 1's extreme. He usually describes it visually. Treat this as a free parameter.
- I found no ICT-sourced minimum FVG size. All size filters come from coders.

---

## 2. Order blocks, breaker blocks, mitigation blocks, rejection blocks

### Takeaway
The ICT-faithful definition is "the last opposite-closing candle (or run of them) before a displacement that breaks structure". Popular code does something different: both smc.py and LuxAlgo SMC pick the candle with the **lowest low (or highest high) between the broken swing and the breaking bar**, without requiring a down-close. Breaker and mitigation blocks are failed order blocks, and they differ only in whether the failing swing swept the prior extreme. Invalidation is by wick in smc.py by default, and by close in LuxAlgo.

### Cited Findings
- **Summary of ICT definition:** a bullish OB is the final down-closing candle, or a consecutive group of them, before an impulsive rally; a bearish OB is the final up-closing candle before an impulsive decline. "A candidate only earns the label when the move away shows displacement... that produce[s] a break of structure... ideally leaving a fair value gap." Zone = full high-to-low, or refined to the body or the 50% mean threshold. A "decisive close through the entire zone" invalidates it. — [LuxLib/bullish-bearish-order-block](https://www.luxalgo.com/library/concept/bullish-bearish-order-block/)
- **Refinement conventions:** when several opposing candles are clustered, either take the one nearest the move's origin or merge the cluster. Bounds can be wick-to-wick or bodies only, and a common hybrid enters off the body while invalidating at the wick extreme. A block is "mitigated" once price trades back into it and "invalidated" once price closes through the far side, at which point it is re-labelled a breaker. — [LuxLib/order-block-anatomy-and-refinement](https://www.luxalgo.com/library/concept/order-block-anatomy-and-refinement/)
- A TradingView "ICT Order Block" script that cites ICT Core Content (per a search summary) describes the block as the **lowest down-close candle** within the pullback from a swing high. — search summary of [TV ICT Order Block](https://www.tradingview.com/script/HVcKIE8w-ICT-Order-Block/). Contradiction: fetching that script page directly gave the author's own definition: "the last down candle before a strong up candle". Displacement there = a candle body ≥ a chosen ATR multiple. Optional filters require an FVG or a BOS/CHoCH. Mitigation is "the first time price trades into it", measured by close or by wick. — [TV ICT Order Block](https://www.tradingview.com/script/HVcKIE8w-ICT-Order-Block/)
- ATAS draws the bullish OB's upper boundary from the candle **open**, with some sources using the high. Displacement is required, while an FVG or MSS is optional. — [ATAS](https://atas.net/blog/what-are-ict-order-blocks-and-breaker-blocks-in-trading/)
- **smc.py `ob()`:** at bar i, if `close[i] > high[last_swing_high]` and that swing has not yet been crossed, the OB candle is the bar with the **lowest low** in (swing_idx, i), taking the last occurrence on ties, or bar i-1 if they are adjacent. OB = [low, high] of that candle. There is no candle-colour requirement. Lifecycle: once `low < bottom` (or, with `close_mitigation=True`, `min(open, close) < bottom`), the OB is flagged `breaker`. Once a breaker's `high > top`, the OB is deleted entirely. It also outputs `OBVolume` (sum of volume over bars i, i-1, i-2) and `Percentage` (min/max of the volume split). The swing input carries look-ahead (see Section 7). — [smc.py](https://github.com/joshyattridge/smart-money-concepts/blob/master/smartmoneyconcepts/smc.py)
- **Lux-SMC Pine `ob_coord()`:** when close crosses over a swing high (BOS/CHoCH), it scans bars back to the swing and picks the **lowest low**, skipping bars whose `high-low >= 2 × threshold`, where threshold = ATR(200) (default "Atr") or the cumulative mean range (`ta.cum(high-low)/n`). This is the volatility filter. Zone = that candle's [low, high]. A bullish OB is removed when `close < bottom`, i.e. close-based invalidation. Defaults: show the last 5 internal and 5 swing OBs. — [Lux-SMC Pine](https://gist.github.com/niquedegraaff/8c2f45dc73519458afeae14b0096d719)
- **Lux-ICT:** a breaker is confirmed when price mitigates (breaks out of) an OB. It has settings "Swing Lookback" and "Use Candle Body". — [Lux-ICT](https://www.tradingview.com/script/ib4uqBJx-ICT-Concepts-LuxAlgo/)
- **Breaker block (strict ICT):** "price runs below a prior low to take out the stops resting there, then reverses and breaks back above the swing high that preceded the run." The down-closing candle(s) of that failed leg form the bullish breaker. "The strict ICT definition requires the liquidity run... the looser retail reading treats any violated order block as a breaker." — [LuxLib/breaker-block](https://www.luxalgo.com/library/concept/breaker-block/)
- **Mitigation block:** the same role flip **without** the sweep. The swing fails to exceed the prior extreme (a lower high), and then structure breaks the other way. "Sweep means breaker, failure means mitigation block." — [LuxLib/mitigation-block](https://www.luxalgo.com/library/concept/mitigation-block/)
- **Rejection block:** a wick-based zone at a swing extreme. Bearish: from the top of the body to the wick high. Stop just beyond the wick. "Body acceptance beyond the wick extreme" is the failure case. There is no fixed wick size, it is "conspicuous against recent bars". — [LuxLib/rejection-block](https://www.luxalgo.com/library/concept/rejection-block/)

### Inferences
- **OB free parameters:**
  1. Candle selection: last opposite-close candle (ICT) / lowest-low candle in the swing→break interval (smc, Lux) / merge the run of consecutive opposite candles.
  2. Validation requirement: BOS or MSS by close / displacement (body ≥ k·ATR) / FVG left in the leg / prior liquidity sweep.
  3. Zone bounds: wick-to-wick / body (open to low for a bull block) / open to mean threshold.
  4. Entry: near edge (bull: high or open) / mean threshold / far edge.
  5. Invalidation: wick < low (smc default) / body close < low (Lux, ICT "decisive close") / close < mean threshold.
  6. Volatility exclusion of huge bars (Lux 2×ATR(200)).
  7. Max age or first-touch-only.
  8. Swing length used to define "structure".
- **Breaker vs mitigation block** is a single boolean in code: did the failing leg's extreme exceed the prior swing extreme (by wick? by ≥ k ticks?) before the opposite structure break.
- **Rejection block parameters:** minimum wick/range ratio, wick ≥ k·ATR, whether the wick must have swept a prior swing or session level, and entry at the body edge vs the wick CE.

### Gaps
- I found no primary-source ICT quote for "highest up-close / lowest down-close candle with most range". A targeted search returned nothing, so that wording stays unverified.
- I could not confirm from primary material whether ICT's 2022 Mentorship de-emphasised order blocks in favour of FVGs. That is commonly asserted but was not sourced here.

---

## 3. Liquidity: buy-side/sell-side, equal highs/lows, swing definitions, sweep vs breakout

### Takeaway
Liquidity = resting stops beyond swing extremes, equal highs/lows, and session, day or week extremes. A "sweep" differs from a "breakout" only by what follows the trade-through. Usually that means a close back inside the level, on the same bar or within N bars, often plus displacement or a CHoCH. The equal-highs tolerance, the swing fractal length, and the sweep confirmation window are the key parameters. The smc.py liquidity function has full-sample look-ahead.

### Cited Findings
- **ICT swing fractals (summary):** a Short-Term High (STH) is a 3-candle pattern whose middle high exceeds the highs of the candles on both sides. An Intermediate-Term High (ITH) is an STH with lower STHs on both sides. A Long-Term High is an ITH with lower ITHs on both sides. Lows are mirrored. One glossary instead says an STH "elevated by forming at an FVG rebalancing event" becomes an ITH, which conflicts with the structural rule. — [x10hop STH/STL glossary](https://x10hop.pages.dev/concepts/short-term-high-low); [innercircletrader.net swing high](https://innercircletrader.net/tutorials/ict-swing-high-explained/); [TV ICT Swing Structure STH/ITH](https://www.tradingview.com/script/Tf5fodO2-ICT-Swing-Structure-STH-STL-ITH-ITL/)
- **Generic swing definition:** a high above the highs of N bars on each side. "A swing high with strength 5 is only knowable five bars after it printed." Optionally filter by a minimum swing-to-swing move (% or ATR). — [LuxLib/swing-high-low](https://www.luxalgo.com/library/concept/swing-high-low/)
- **Equal highs/lows:** two or more swing highs "within a few ticks... or a small fraction of ATR". A meaningful pullback between them is required, and the level is drawn as a band. Once price closes beyond it with acceptance, the pool is spent. — [LuxLib/equal-highs-lows-as-liquidity](https://www.luxalgo.com/library/concept/equal-highs-lows-as-liquidity/)
- **Lux-SMC Pine EQH/EQL:** compares consecutive `ta.pivothigh(3,3)` values (Bars Confirmation `eq_len = 3`). EQH if `max < min + ATR(200) × 0.1` (threshold default 0.1). Confirmation is 3 bars after the second pivot. — [Lux-SMC Pine](https://gist.github.com/niquedegraaff/8c2f45dc73519458afeae14b0096d719)
- **Lux-ICT liquidity:** two points count as equal if point 1 lies within point 2 ± (ATR(10)/(10/margin)). — [Lux-ICT](https://www.tradingview.com/script/ib4uqBJx-ICT-Concepts-LuxAlgo/)
- **smc.py `liquidity()`:** groups swing highs within ± `range_percent × (max(high) − min(low)) over the WHOLE dataframe` (default 0.01). That uses the full sample's range, which is **look-ahead**. A group needs at least 2 swings. `Swept` = the first later bar whose high ≥ level + band, i.e. a wick beyond the band with no close-back requirement. — [smc.py](https://github.com/joshyattridge/smart-money-concepts/blob/master/smartmoneyconcepts/smc.py)
- **smc.py `previous_high_low()`:** resamples to 1D/1W etc. using pandas calendar bins (midnight of the index timezone), and outputs PDH/PDL with `BrokenHigh`/`BrokenLow` flags. Bars inside a period use the prior completed period. — [smc.py](https://github.com/joshyattridge/smart-money-concepts/blob/master/smartmoneyconcepts/smc.py)
- **Sweep vs breakout:** "price closes back inside the prior range instead of holding beyond the level. A close that holds beyond it, with continuation, is a breakout." "Some traders require the close back inside on the sweeping candle itself, while others accept any tag-and-reject that resolves within a few bars." Stricter versions add displacement or a lower-timeframe CHoCH. — [LuxLib/liquidity-sweep](https://www.luxalgo.com/library/concept/liquidity-sweep/)
- Higher-weight pools are prior-day, session and weekly highs/lows, which carry more weight than minor intraday swings. — [LuxLib/liquidity-sweep](https://www.luxalgo.com/library/concept/liquidity-sweep/)

### Inferences
- **Free parameters:**
  1. Swing definition: N-left/N-right fractal (N = 1 is ICT's STH; also try 2, 3, 5, 10, 20 on 1m), or ICT's STH→ITH→LTH hierarchy.
  2. Pool set: swing points only / EQH-EQL only / PDH-PDL / Asian range / London range / overnight (18:00–09:30) high-low / prior week high-low / midnight-open range.
  3. EQH tolerance: k ticks / a·ATR(n) (Lux 0.1·ATR(200)) / % of price. Also the minimum bar separation and minimum pullback depth between the equal points.
  4. Sweep penetration: ≥ 1 tick / ≥ k ticks / ≥ a·ATR, plus an optional maximum penetration (too deep = breakout).
  5. Rejection rule: same-bar close back inside / close back inside within M bars / CISD or MSS within M bars.
  6. Pool age limits and "already-swept" bookkeeping. A pool consumed once cannot be swept again.
- To make smc.py `liquidity()` causal, replace the global range with a rolling ATR or a rolling range.
- For CME futures, PDH/PDL should use the CME session (18:00–17:00 ET) or the RTH session (09:30–16:00), not pandas midnight-UTC bins. Both are reasonable ablation options.

### Gaps
- I found no ICT-sourced numeric tolerance for "relative equal highs". It is always discretionary in ICT's teaching.

---

## 4. Market structure shift (MSS), change of character (CHoCH), break of structure (BOS), displacement

### Takeaway
BOS = a with-trend break of the last swing; CHoCH/MSS = the first counter-trend break. ICT's own term is MSS, usually framed as a break of a short-term swing **with displacement after a liquidity sweep**. CHoCH is broader SMC-community vocabulary. Implementations differ on the swing length, close vs wick confirmation, and which swing counts. Displacement has no canonical threshold.

### Cited Findings
- **CHoCH:** the first structural break against the prevailing trend. "Many traders use CHoCH and market structure shift (MSS) interchangeably; others reserve MSS for... a counter-trend break delivered with displacement right after a liquidity sweep." Which swing counts is disputed: the most recent higher low, or the higher low that produced the final high. "A body close beyond it, ideally with displacement, is the usual filter." — [LuxLib/change-of-character](https://www.luxalgo.com/library/concept/change-of-character/)
- **BOS:** price trades through the most recent significant swing in the trend direction. "Many traders require a candle body to close beyond the swing, because a wick-only poke frequently turns out to be a liquidity sweep." — [LuxLib/break-of-structure](https://www.luxalgo.com/library/concept/break-of-structure/)
- **2022 Mentorship (episode summaries):** a break below a short-term low indicates a shift in market structure (Ep. 2). A bullish MSS on the daily is identified when price takes out a short-term high, confirmed when price rebalances and makes a new swing high (Ep. 38). Price runs back up into the FVG and then sells off toward an old low (Ep. 4). These are AI summaries, not verbatim transcripts. — [videohighlight Ep2](https://videohighlight.com/v/tmeCWULSTHc); [videohighlight Ep38](https://videohighlight.com/v/36184dDAqtM); [SozAI Ep4 transcript](https://sozai.app/transcript/2022-ict-mentorship-episode-4/index.md)
- **Displacement:** "There is no fixed threshold." It is judged relative to recent bars: bodies conspicuously larger than the last few dozen, small wicks, consecutive one-directional closes, FVGs left behind. "One enormous body can qualify on its own, and a run of three to five strong closes qualifies." — [LuxLib/displacement](https://www.luxalgo.com/library/concept/displacement/). Lux-ICT likewise describes displacement as successive same-direction large-body, short-shadow candles, citing autocorrelation and volatility clustering as technical proxies. — [Lux-ICT](https://www.tradingview.com/script/ib4uqBJx-ICT-Concepts-LuxAlgo/)
- **CISD (Change in State of Delivery), a later-cycle ICT trigger:** find the last unbroken series of down-closing candles into the extreme. CISD level = the open of the first candle in that series. Bullish CISD = a candle **body closes** above that open, and wicks don't count. No swing break is needed, so it fires earlier than an MSS but is less filtered. — [LuxLib/change-in-state-of-delivery](https://www.luxalgo.com/library/concept/change-in-state-of-delivery/). The TradingFinder variant instead looks back 1–4 candles for the first opposite candle and uses the next candle's open. — [TradingFinder CISD](https://www.tradingview.com/script/g5X05qNk-Change-in-State-of-Delivery-CISD-ICT-TradingFinder-Liquidity-1)
- **smc.py `bos_choch()`:** works on the last 4 alternating swings. Bullish BOS: pattern [-1, 1, -1, 1] with levels L4 < L2 < L3 < L1 (higher lows and higher highs). Bullish CHoCH: same pattern with L1 > L3 > L4 > L2. The level is the 3rd-last swing. Break confirmation: `close` (default `close_break=True`) or `high` beyond the level, searched from bar i+2. **The label is stamped on the earlier swing's index**, and earlier unbroken BOS/CHoCH whose break comes later are deleted retroactively. Use `BrokenIndex` as the event time. — [smc.py](https://github.com/joshyattridge/smart-money-concepts/blob/master/smartmoneyconcepts/smc.py)
- **Lux-SMC Pine:** swing structure uses `length = 50` and internal structure uses `swings(5)`. A bullish break is `ta.crossover(close, top_y)`, which is close-based. It is labelled CHoCH if the running trend was bearish, else BOS. There is an optional internal "confluence filter" based on wick/body. — [Lux-SMC Pine](https://gist.github.com/niquedegraaff/8c2f45dc73519458afeae14b0096d719)

### Inferences
- **Free parameters:**
  1. Swing length N (1 = ICT STH; Lux internal 5, swing 50; smc default 50 means a ±50-bar window).
  2. Break confirmation: wick / close / close + k ticks / close + displacement.
  3. Which swing a CHoCH must break: most recent opposing swing / the swing that created the last extreme ("protected" swing).
  4. Displacement definition: body ≥ k·ATR(n) (k ∈ {1, 1.5, 2}), body/range ≥ r (0.6–0.7), N consecutive same-direction closes, or "leg leaves ≥ 1 FVG".
  5. MSS prerequisite: a sweep within M bars before the break, yes/no.
  6. CISD as an alternative trigger, with its own series-definition choice.
  7. Timeframe of structure (1m vs 5m/15m) for the bias layer vs the entry layer.

### Gaps
- I found no authoritative ICT numeric displacement threshold. It does not appear to exist.
- I could not verify from primary sources when ICT introduced "CISD" (it is described only as "later teaching cycles").

---

## 5. Premium/discount, equilibrium, OTE, dealing range

### Takeaway
Once a dealing range is chosen, the math is trivial: EQ = 50%, premium > 0.5, discount < 0.5, OTE = 62–79% retracement with 70.5% as the sweet spot. The hard and look-ahead-prone part is choosing the range anchors. Some sources use the last displacement leg; LuxAlgo uses the trailing max/min since the last swing.

### Cited Findings
- **OTE:** the 61.8/62% to 79% retracement of an impulse leg, with 70.5% as the midpoint. level(p) = H1 − p·(H1 − L0) for longs. The leg must be complete, and a move beyond the leg's origin invalidates it. ICT uses 0.62/0.705/0.79, whereas classical tools use 0.618/0.786. The standard sequence is liquidity taken → structure shifted → retrace into the band, ideally into a PD array. — [LuxLib/optimal-trade-entry](https://www.luxalgo.com/library/concept/optimal-trade-entry/)
- **Premium/discount:** EQ = (R_high + R_low)/2 and pos = (P − R_low)/(R_high − R_low). Premium if pos > 0.5, discount if pos < 0.5. Refinements add quadrants at 0.25/0.75. "The range choice is discretionary or fractal-based." Re-anchor when there is a close beyond either extreme. — [LuxLib/premium-and-discount](https://www.luxalgo.com/library/concept/premium-and-discount/)
- **Lux-SMC Pine premium/discount** uses `trail_up`/`trail_dn` (the trailing extremes of the current swing structure). The premium box runs from `trail_up` to `0.95·trail_up + 0.05·trail_dn`, i.e. the top 5% band. Equilibrium = the average of the two. It is drawn only on `barstate.islast`, as a display of the current state. — [Lux-SMC Pine](https://gist.github.com/niquedegraaff/8c2f45dc73519458afeae14b0096d719)
- **smc.py `retracements()`** gives the current and deepest retracement % from the last swing high/low, built on the look-ahead swing series. — [smc.py](https://github.com/joshyattridge/smart-money-concepts/blob/master/smartmoneyconcepts/smc.py)

### Inferences
- **Free parameters:**
  1. Dealing range anchors: last confirmed swing high/low pair (fractal N) / the displacement leg that caused the MSS / the session range (Asian, overnight, prior day) / the midnight-to-now range / HTF (daily/weekly) range.
  2. Premium/discount cutoff: 0.5, or quadrant-based (0.25/0.75).
  3. OTE band: [0.62, 0.79] vs [0.618, 0.786], with entry at 0.62, 0.705 or 0.79 (limit) or on touch + confirmation.
  4. Invalidation: beyond 1.0 (the leg origin), or at a deeper stop.
  5. Targets: −0.27 / −0.62 / −1 / −2 standard-deviation extensions (the LuxLib pages mention "standard-deviation projections" but give no values here).
  6. The leg end-point must be confirmed (a swing high with N right bars) before OTE levels are valid, and that is a source of look-ahead.

### Gaps
- I did not retrieve ICT's standard-deviation projection multiples (e.g. −2, −2.5, −4) from a citable source in this pass.

---

## 6. Time: killzones, Silver Bullet, macros, opening prices, midnight / true day open

### Takeaway
The times are the most mechanical part of ICT, yet sources still disagree by 30–90 minutes. The widely cited New York-time set is: Asian 20:00–00:00, London open 02:00–05:00, NY AM 07:00–10:00 (index futures 08:30–11:00), London close 10:00–12:00, NY PM 13:30–16:00. Silver Bullet: 03–04, 10–11, 14–15. Macros: xx:50–xx:10 plus some odd windows. Anchors: midnight open (00:00 ET), 08:30 open, 09:30 open, plus NDOG/NWOG at the CME maintenance break. All times must be computed in America/New_York. smc.py's killzones are hard-coded in UTC and therefore shift by an hour from early November to early March.

### Cited Findings
- **Killzones (New York time):** Asian 20:00–00:00 (also quoted as "~8–10 pm"), London open 02:00–05:00, New York open 07:00–10:00 ("index-futures variants use 08:30 to 11:00"), London close 10:00–12:00, NY PM 13:30–16:00. "Window boundaries differ by 30 to 90 minutes across ICT sources and platforms." — [LuxLib/killzones](https://www.luxalgo.com/library/concept/killzones/)
- **Lux-ICT killzones** are listed as New York 7–9, London Open 2–5, London Close 10–12, and Asian starting 20:00. The NY end time differs from the library page. — [Lux-ICT](https://www.tradingview.com/script/ib4uqBJx-ICT-Concepts-LuxAlgo/)
- **smc.py `sessions()`** has fixed **UTC** presets: Asian KZ 00:00–04:00, London open KZ 06:00–09:00, NY KZ 11:00–14:00, London close KZ 14:00–16:00. It also has Sydney 21–06, Tokyo 00–09, London 07–16, New York 13–22 and Custom. The candle timezone is set via a fixed `UTC±n` string. — [smc.py](https://github.com/joshyattridge/smart-money-concepts/blob/master/smartmoneyconcepts/smc.py)
- **Silver Bullet:** one-hour New York-time windows 03:00–04:00, 10:00–11:00, 14:00–15:00. Inside the window: sweep or structure shift → displacement → entry in an FVG formed **inside the window**. Stop beyond the manipulation swing, target the opposing pool. No trade if no FVG forms. — [LuxLib/silver-bullet](https://www.luxalgo.com/library/concept/silver-bullet/)
- **Macros:** canonical shape is xx:50–xx:10. The most quoted are 09:50–10:10 and 10:50–11:10 ET. Fuller lists add 02:33–03:00 and 04:03–04:30 (London), 08:50–09:10, 11:50–12:10, 13:10–13:40 and 15:15–15:45 (New York time). "Exact minutes vary between sources and course years." LuxAlgo notes that the 10:00 ET data releases are a mundane explanation. — [LuxLib/ict-macros](https://www.luxalgo.com/library/concept/ict-macros/); [ICT Macros (LuxAlgo) script](https://www.tradingview.com/script/aLTywnJ0-ICT-Macros-LuxAlgo/)
- **Time anchors:** the midnight open (00:00 America/New_York) begins the "true day", and its opening price is extended as a level. Further anchors are the 08:30 open and the 09:30 open for index futures. On a bullish day the model wants the low to form below the midnight or 08:30 open (Judas swing / power of three). — [LuxLib/ict-time-anchors](https://www.luxalgo.com/library/concept/ict-time-anchors/)
- One wiki says ICT's true day runs 00:00–15:00 New York time. This is a secondary source. — [x10hop ICT true day](https://x10hop.pages.dev/concepts/ict-true-day)
- **Opening gaps:** NDOG = the CME maintenance-break close to the reopen. NWOG = Friday close to the weekly reopen. The opening range gap = the prior RTH close (16:00 or 16:15 ET) to the RTH open. Mark the high, low and CE, and keep roughly the last 5 NWOGs. — [LuxLib/opening-gap](https://www.luxalgo.com/library/concept/opening-gap/)

### Inferences
- **DST trap:** the smc.py killzone presets equal the New York-time killzones only under EDT (UTC−4). For example, 11:00–14:00 UTC = 07:00–10:00 EDT but 06:00–09:00 EST. For a multi-year 1m backtest, compute every window from `America/New_York` local time.
- **CME specifics (inference from the opening-gap page plus CME hours):** NDOG = 17:00 ET close to 18:00 ET open; NWOG = Friday 17:00 to Sunday 18:00. For the opening range gap on equity index futures, use the 16:00 or 16:15 ET close vs the 09:30 open. For CL, GC, ZN, ZB, 6E and 6J, the RTH and settlement times differ (e.g. CL settles at 14:30 ET, ZN/ZB at 15:00 ET), so the "regular session" anchors must be chosen per product.
- **Time parameters to ablate:** killzone variant (07–10 vs 08:30–11 vs 07–09), whether the setup must form inside the window, whether the entry must also be inside it, macro list (core 2 vs full 8), anchor price (midnight / 08:30 / 09:30 / 18:00 CME open), true-day end (15:00 vs 16:00 vs 17:00), and Silver Bullet window set.

### Gaps
- I could not cite how ICT's killzone times changed across years (e.g. 2016 vs 2022 vs 2024 content). The LuxAlgo note says only that they "vary by source and course years".
- I did not find a citable definition of "true week open" (Monday 18:00 vs Monday 00:00 vs Sunday 18:00). Quarterly-theory sources were not retrieved.

---

## 7. Look-ahead and repainting risk, and how to avoid it

### Takeaway
Most open-source SMC code is built for drawing charts, not for backtesting. smc.py in particular stamps events at bars earlier than the bar where they become knowable: FVGs at the middle bar, swings at the pivot bar using N future bars plus later swings, BOS/CHoCH at the earlier swing index with retroactive deletion, and a liquidity tolerance computed from the whole dataset. Every concept needs an explicit "known-at" timestamp.

### Cited Findings
- **smc.py swing detection** uses `high == high.shift(-N).rolling(2N).max()`, a centered window of N−1 bars left and N bars right. It then iteratively deletes the lower of two consecutive same-type swings, a decision that depends on **later** swings. It also forces artificial swings on the **first and last bar**, so the last bar's label changes as data arrives. — [smc.py](https://github.com/joshyattridge/smart-money-concepts/blob/master/smartmoneyconcepts/smc.py)
- **smc.py BOS/CHoCH** writes the signal at `last_positions[-2]`, an earlier swing, and deletes earlier signals whose break happens later. **FVG** uses `shift(-1)`. **Liquidity** uses the global `high.max() − low.min()`. The **OB** depends on the swing series. — [smc.py](https://github.com/joshyattridge/smart-money-concepts/blob/master/smartmoneyconcepts/smc.py)
- **Lux-SMC Pine swings** use `os := high[len] > ta.highest(len) ? 0 : ...`. A top at bar t−len is confirmed at bar t and only checks the `len` bars to its right, a causal "leg" detector with len-bar lag. FVG detection uses `high[2]`, `close[1]` and the current `low`, so it is causal. EQH uses `pivothigh(3,3)`, a 3-bar lag. PDH/PDL use `request.security(..., lookahead = barmerge.lookahead_on)`. Whether that repaints depends on whether `hl()` returns the prior bar's values, which was not checked. — [Lux-SMC Pine](https://gist.github.com/niquedegraaff/8c2f45dc73519458afeae14b0096d719)
- "A swing point cannot be confirmed until the right-side bars have closed... any tool built on swings labels the past, not the present." — [LuxLib/swing-high-low](https://www.luxalgo.com/library/concept/swing-high-low/)
- OTE "is only evaluated after the leg completes". — [LuxLib/optimal-trade-entry](https://www.luxalgo.com/library/concept/optimal-trade-entry/)

### Inferences
- **Rules for a causal implementation:**
  1. Each swing gets `pivot_idx` and `confirm_idx = pivot_idx + N_right`, and it is usable only for bars > confirm_idx. Never apply the "remove consecutive same-type swings" clean-up using future swings. Instead, use a state machine that alternates highs and lows in real time and replaces the pending swing when a more extreme one confirms.
  2. An FVG becomes known at the close of candle 3, so the earliest entry is the open of candle 4 (or a limit order placed after candle 3 closes).
  3. BOS/MSS/CHoCH events are timestamped at the breaking bar's close (close rule) or intrabar (wick rule). With wick rules on 1-minute bars, the order of OHLC inside the bar is unknown. Use 1-second data or a conservative fill assumption when both the stop and the entry are inside one bar.
  4. An OB becomes known only when the BOS that validates it occurs. Entries can happen only on later retests.
  5. Use rolling, not global or cumulative-from-chart-start, normalisers (ATR(n), rolling median range) for size and tolerance filters. Lux's `ta.cum(...)/n` thresholds are causal but non-stationary and depend on the start date.
  6. Session and anchor levels (Asian high/low, midnight open, PDH/PDL) are usable only after their window closes. A killzone's high/low is not final until the window ends.
  7. For HTF arrays projected onto 1m (5m/15m FVGs, daily ranges), use only completed HTF bars. That is the `lookahead_off` / `[1]` idiom in Pine, and `resample(..., label='right', closed='right')` plus a shift in pandas.
  8. Daily boundaries for CME products should be set explicitly: CME day 18:00–17:00 ET vs ICT true day 00:00 ET. Pandas default resampling uses midnight of the index timezone, so localise to America/New_York first.
- **Repainting distinction:** smc.py is "batch-correct but not causal". Running it on an expanding window bar by bar would change past labels, so a backtest must either re-implement the logic causally or re-run it on data truncated at each decision bar. The second option is expensive on 1m data.

### Gaps
- I did not verify the current official LuxAlgo SMC release (TradingView) line by line. I read a public fork that keeps the LuxAlgo code, so the defaults (swing 50, internal 5, ATR(200), EQH 0.1·ATR, 3-bar EQ confirmation, OB 2×ATR volatility filter) may differ slightly in later LuxAlgo revisions. The TradingView description page itself does not list these defaults.
- I did not check the `hl()` helper behind the LuxAlgo PDH/PDL lookahead.
