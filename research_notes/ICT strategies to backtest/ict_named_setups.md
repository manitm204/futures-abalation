# Popular named ICT (Inner Circle Trader) setups: rule sets for 1-minute futures backtesting

Scope note: ICT (Michael J. Huddleston) teaches mostly in long YouTube livestreams and mentorship videos and never published a written rulebook. Nearly every written source below is a community or vendor interpretation (LuxAlgo concept library, TradingView scripts and ideas, Quantum Algo, TradingFinder). Several sources say this outright. Treat every "rule" here as one community version of the setup, not as ICT canon. Primary-source video transcripts were not retrievable in this pass. innercircletrader.net pages came back as image data or a paywall ad, and fxreplay returned HTTP 403.

Common building blocks used by every model below. Each must be coded once and shared:
- **FVG (fair value gap)**: a three-candle imbalance. On a bullish FVG, candle 3's low is above candle 1's high, and the gap is the space between them. On a bearish FVG, candle 3's high is below candle 1's low — [LuxAlgo Model 2022 / Quantum Algo](https://www.quantum-algo.com/blog/guides/ict-2022-model-complete-guide/); [TradingView Unicorn guide](https://www.tradingview.com/chart/XAUUSD/zb6bDQzM-The-Unicorn-Model-Guide-to-ICT-s-Best-Standalone-setup)
- **CE (consequent encroachment)**: "ICT's term for the gap's midpoint, the 50% level of the box" — [LuxAlgo Opening Gap](https://www.luxalgo.com/library/concept/opening-gap.md)
- **Liquidity sweep**: "Price spikes past that high or low, triggering the resting stops, then rejects". A close beyond the level "usually invalidates the setup" — [Quantum Algo](https://www.quantum-algo.com/blog/guides/ict-2022-model-complete-guide/)
- **MSS (market structure shift)**: after the sweep, price breaks "the most recent opposing short-term structure point with intent" — [Quantum Algo](https://www.quantum-algo.com/blog/guides/ict-2022-model-complete-guide/)
- **Displacement**: "large-bodied candles that leave an inefficiency behind… Weak, overlapping candles do not count". No numeric threshold is given — [Quantum Algo](https://www.quantum-algo.com/blog/guides/ict-2022-model-complete-guide/). One TradingView script makes it numeric as a candle at least 3x the standard deviation of recent price history — [TradingView ICT 2022 Mentorship Model scripts](https://in.tradingview.com/scripts/ict2022mentorship/)
- **Kill zones (NY time)**: London Open 02:00–05:00, NY AM 07:00–10:00, London Close 10:00–12:00, NY PM 13:30–16:00 — [Quantum Algo](https://www.quantum-algo.com/blog/guides/ict-2022-model-complete-guide/). LuxAlgo lists an index-futures NY variant of 08:30–11:00 — [LuxAlgo Killzones](https://www.luxalgo.com/library/concept/killzones.md)

---

## Q0. Popularity / prominence ranking

### Takeaway
No source measures popularity directly. Judged by the volume of TradingView scripts and ideas, dedicated guide pages and community discussion, the Silver Bullet and the 2022 Mentorship Model are clearly the most prominent ICT setups. Next come the Judas Swing / Power of Three, the Unicorn, OTE, Turtle Soup, and the opening-gap / first-FVG concepts. The Venom model (2025) is the newest and is growing.

### Cited Findings
- The Silver Bullet has dedicated TradingView tag pages for scripts and ideas (silverbullet, ictsilverbullet), many open-source implementations (Flux Charts, TradingFinder, GBB, "ICT Silver Bullet Backtest"), and at least one large YouTube backtest of about 25,000 variations — [TV silverbullet scripts](https://id.tradingview.com/scripts/silverbullet/); [TV ictsilverbullet ideas](https://www.tradingview.com/ideas/ictsilverbullet); [gist.ly summary of "I backtested 25,000 ICT Silver Bullet trades"](https://gist.ly/youtube-summarizer/i-backtested-25000-ict-silver-bullet-trades)
- The 2022 Model has its own TradingView tag pages (ict2022, ict2022mentorship) and is marketed as "One Setup For Life" — [TV ict2022mentorship](https://in.tradingview.com/scripts/ict2022mentorship/); [LuxAlgo/TradingFinder "2022 Model ICT Entry Strategy… One Setup For Life"](https://www.luxalgo.com/library/indicator/FK960gz8-2022-model-ict-entry-strategy-one-setup-for-life/)
- The Unicorn is promoted as "the most powerful setup in ICT" and "ICT's best standalone setup" and has its own TradingView tag pages — [TV Unicorn guide](https://www.tradingview.com/chart/XAUUSD/zb6bDQzM-The-Unicorn-Model-Guide-to-ICT-s-Best-Standalone-setup); [TV unicornmodel scripts](https://www.tradingview.com/scripts/unicornmodel/)
- Venom is presented as "ICT's 2025 Venom Model" and already has several TradingView scripts and an ideas tag — [fxreplay title](https://www.fxreplay.com/strategies/icts-2025-venom-model); [TV ictvenom ideas](https://www.tradingview.com/ideas/ictvenom)

### Inferences
- Suggested ranking by prominence: (1) Silver Bullet, (2) 2022 Mentorship Model, (3) Judas Swing / Power of Three (AMD), (4) Unicorn, (5) OTE, (6) Turtle Soup (ICT liquidity-raid version), (7) Opening Range Gap / first presented FVG / NDOG / NWOG, (8) Venom, (9) London-open Asian-range raid and London-close reversal, (10) weekly profiles / daily-bias templates, which are a context layer rather than an entry model.

### Gaps
- No survey, search-volume or other quantitative popularity data was found. The ranking is my judgement from how much content exists for each setup.

---

## Q1. ICT Silver Bullet

### Takeaway
There are three one-hour NY-time windows: 03:00–04:00, 10:00–11:00 and 14:00–15:00. Inside a window, look for a sweep or structure shift, then displacement that leaves an FVG formed inside the window. Enter in the FVG, stop beyond the manipulation swing, and target the opposing liquidity pool mapped before the window. Allow one attempt per window. The point minimum (for example 10 points on indices) is a community convention I could not trace to ICT. The windows and FVG geometry are objective. Choosing the draw on liquidity is discretionary.

### Cited Findings
- Windows are 3–4 am, 10–11 am and 2–3 pm New York time. They are tied to NY local time, so they shift against other time zones when daylight saving changes — [LuxAlgo Silver Bullet](https://www.luxalgo.com/library/concept/silver-bullet.md)
- "Take the entry only on a fair value gap created inside the window by displacement". If no valid gap forms before the window closes, there is no trade — [LuxAlgo Silver Bullet](https://www.luxalgo.com/library/concept/silver-bullet.md). A community checklist says the FVG "MUST BE created DURING the Silver Bullet hours", and another source treats a gap confirmed at 11:00 as past the deadline — [TradingView ICT Silver Bullet ideas](https://www.tradingview.com/ideas/ictsilverbullet)
- Map the draw on liquidity before the window: "untapped session highs and lows, resting liquidity beyond equal extremes, and any unfilled imbalances". Inside the window, expect a manipulation (sweep of a mapped pool or a clear structure shift) and then displacement the other way that leaves the FVG — [LuxAlgo Silver Bullet](https://www.luxalgo.com/library/concept/silver-bullet.md)
- Several sources require a prior sweep. One says a gap formed without a sweep of an obvious level "is a gap, not a Silver Bullet" — [TradingView ICT Silver Bullet ideas](https://www.tradingview.com/ideas/ictsilverbullet)
- Stop goes beyond the manipulation swing. A tighter variant puts it beyond the far edge of the entry FVG — [LuxAlgo Silver Bullet](https://www.luxalgo.com/library/concept/silver-bullet.md)
- Target is the opposing liquidity pool identified before the window. Partial exits are common, as are time caps, but the time caps are unspecified — [LuxAlgo Silver Bullet](https://www.luxalgo.com/library/concept/silver-bullet.md). Other sources state a "minimum two to one" reward-to-risk — [TradingView Silver Bullet idea](https://pl.tradingview.com/chart/EURUSD/jOkVQBxm-What-Is-the-ICT-Silver-Bullet-Strategy-and-How-Does-It-Work)
- The only minimum-size figure found: traders "generally look for at least 15 pips when trading forex and 10 points in indices" — [TradingView ictsilverbullet ideas](https://www.tradingview.com/ideas/ictsilverbullet). LuxAlgo gives no minimum — [LuxAlgo Silver Bullet](https://www.luxalgo.com/library/concept/silver-bullet.md)
- Instruments: "originally designed and tested on US index futures, NASDAQ 100 (NQ Futures) and the E-mini S&P 500 (ES Futures)" — [TradingView silverbullet scripts](https://cn.tradingview.com/scripts/silverbullet). LuxAlgo says it suits liquid index futures (especially ES and NQ) and major FX, and suits instruments without a New York session rhythm poorly — [LuxAlgo Silver Bullet](https://www.luxalgo.com/library/concept/silver-bullet.md)
- Trades per day: "one window, one setup shape, one attempt". There is no explicit cap across the three windows — [LuxAlgo Silver Bullet](https://www.luxalgo.com/library/concept/silver-bullet.md)
- Example coded version ("ICT Silver Bullet Backtest" on TradingView): each of the three windows can be toggled; entry on a retrace "into the 50% midpoint of the FVG"; stop at a selected candle or the FVG boundary plus a tick buffer; target a fixed 1:1 to 1:4 R, or S/R, or a trail at 2×ATR(14) that activates at 1.5R; max trades per session is configurable; no sweep filter. No results are published — [TV ICT Silver Bullet Backtest](https://es.tradingview.com/script/SuBXi3p8-ICT-Silver-Bullet-Backtest/)
- **Independent evidence (negative):** The Silver Bullet [GBB] author tested 1-minute ES, NQ, YM and GC from 2011–2026 across all 23 hours, with 2 ticks of slippage and $4.50 per round trip. They concluded "the Silver Bullet hours are not special, and the model is not a profitable strategy on its own". They attribute the apparent edge to higher volatility in those hours, because fixed costs become a smaller share of a wider stop — [TV Silver Bullet GBB](https://br.tradingview.com/script/teL2dDvS-Silver-Bullet-GBB/)
- A YouTube backtest of 16 years of NQ/ES 1-minute data (about 25,000 variations) found the 2 pm and London windows acceptable and the popular 10 am window slightly negative, and said the strategy could work as a system at about 2:1 R — [gist.ly summary](https://gist.ly/youtube-summarizer/i-backtested-25000-ict-silver-bullet-trades)

### Inferences
Codable rule set for 1-minute bars:
- [OBJ] Window W in {03:00–04:00, 10:00–11:00, 14:00–15:00} ET. Candle 3 of the FVG must close inside W.
- [OBJ-ish] Pre-window liquidity map: prior-session high/low, current-session high/low before W, prior day high/low, and swing highs/lows on a fractal of N bars. The draw is the nearest unswept pool on the side opposite the sweep. In reality this is discretionary; the mechanical proxy is a parameter.
- [OBJ] Sweep: a bar in W (or in the 30–60 minutes before it, as a parameter) trades beyond a mapped level and closes back inside it.
- [OBJ, with a parameter] Displacement leaves an FVG pointing away from the sweep. Make the gap size or body/ATR threshold a parameter.
- [OBJ] Entry: limit at the near edge or at CE. Stop: beyond the sweep extreme (or the far edge of the FVG plus a buffer). Target: the draw level, or a fixed R.
- [OBJ] Skip if the distance to the draw is below a minimum. Suggested parameter grid: NQ 10/15/20 points, ES 5/10 points.
- [OBJ] One trade per window. Flatten at a time cap, for example end of window plus 60 minutes, or 16:00. Fully intraday, no overnight hold. The 03:00 window falls in Globex overnight hours but is still intraday on the futures session.
- Prior evidence says expect little or no edge net of costs, especially in the 10 am window. The GBB control is a good one to copy: run identical rules in every hour and compare windows against hours of matched volatility.

### Gaps
- I could not verify from ICT's own material the often-repeated "minimum handles" rule (I recall something like ≥10 handles NQ / ≥5 ES in his 2023 lectures, but found no transcript). Treat the minimum as a parameter.
- Whether ICT requires the sweep to happen inside the window or allows it before is ambiguous across sources.

---

## Q2. ICT 2022 Mentorship Model

### Takeaway
The sequence is fixed: a sweep of an obvious high or low, then displacement that causes an MSS, then the FVG that displacement left, then a limit entry in that FVG. The stop goes beyond the sweep wick and the target is the opposite liquidity pool, ideally inside a kill zone. Typical R is about 3:1 or better. The sequence is codable. "Displacement strength", choice of draw and HTF bias are discretionary.

### Cited Findings
- Fixed order: liquidity pool → sweep and rejection → MSS of the opposing short-term structure → caused by displacement → displacement leaves an FVG, which becomes the entry zone. "Never enter before the sweep" — [Quantum Algo 2022 Model](https://www.quantum-algo.com/blog/guides/ict-2022-model-complete-guide/)
- A shift "only counts here after a sweep and with displacement". Structure breaks with no preceding raid are continuation noise — [LuxAlgo Model 2022](https://www.luxalgo.com/library/concept/model-2022/)
- Entry is a limit order at the FVG. Sources contradict each other on the conservative choice: one section says the near edge, the FAQ says the CE (50%), and aggressive traders use the far edge — [Quantum Algo](https://www.quantum-algo.com/blog/guides/ict-2022-model-complete-guide/)
- Stop goes "just below the low of the sweep wick" for longs, and widening it is called a mistake — [Quantum Algo](https://www.quantum-algo.com/blog/guides/ict-2022-model-complete-guide/). One indicator does the same: "stop-loss placed below the liquidity low for bullish setups" — [LuxAlgo/TradingFinder 2022 Model indicator](https://www.luxalgo.com/library/indicator/FK960gz8-2022-model-ict-entry-strategy-one-setup-for-life/)
- Target is the opposite liquidity pool, such as buy-side above the latest swing high, an old high, a session high or a premium array. Textbook setups "routinely offer 3:1 to 5:1" — [Quantum Algo](https://www.quantum-algo.com/blog/guides/ict-2022-model-complete-guide/)
- Timeframes: entries on 1m–15m, bias on 1H/4H. Kill zones are "ideal", and setups outside them are lower probability. The source is inconsistent between "ideally" and "skip" — [Quantum Algo](https://www.quantum-algo.com/blog/guides/ict-2022-model-complete-guide/)
- Some versions add an OTE (62–79% retracement) entry — [TV ICT 2022 search results / LuxAlgo Model 2022](https://www.luxalgo.com/library/concept/model-2022/)
- Which pool counts as the draw, how much energy qualifies as displacement, and which gap is the entry "vary by operator" — [LuxAlgo Model 2022](https://www.luxalgo.com/library/concept/model-2022/)

### Inferences
Codable rule set:
- [OBJ] Liquidity levels: swing highs/lows by N-bar pivot (on 1m or 5m), prior-day H/L, session H/L (Asia 20:00–00:00, London 02:00–05:00).
- [OBJ] Sweep: a wick beyond the level with a close back inside (or within k bars).
- [OBJ, with a parameter] MSS: a close beyond the most recent opposing pivot (N-bar fractal) within M bars of the sweep.
- [OBJ, with a parameter] Displacement: the MSS leg contains at least one candle with body ≥ x·ATR(14), or ≥3σ, and an FVG of at least y ticks.
- [OBJ] Entry: limit at the FVG near edge or CE, valid for Z bars. Stop: sweep extreme plus a buffer. Target: the opposite pool, or 2R/3R. Kill-zone filter on or off as a parameter.
- Intraday only, flat by 16:00 (or 11:00/12:00 for the AM kill zone).
- This is the same machinery as the Silver Bullet without the hour restriction, so code it once and parameterise the time filter.

### Gaps
- No primary-source transcript of the 2022 mentorship (YouTube, 2022) was retrieved. Exact ICT wording on swing definition and FVG choice could not be confirmed.

---

## Q3. Judas Swing, Power of Three (AMD), midnight-open bias

### Takeaway
The Judas Swing is an early false move against the day's bias, measured from the NY midnight open (00:00 ET) and usually between 00:00 and 05:00 (London). You trade the reversal back through the open after a sweep and displacement. Power of Three / AMD is the same idea treated as a fractal template (consolidation around the open, then a manipulation sweep, then distribution through the open). Sources call it "descriptive, not mechanical". The anchor times are objective. Whether a given push is "the" Judas leg is only known in hindsight.

### Cited Findings
- The Judas Swing forms "between the New York Midnight Open (00:00) and 5:00 AM New York Time" — [TradingFinder Judas Swing script](https://br.tradingview.com/script/TYoIs4Q3-Judas-Swing-ICT-01-TradingFinder-New-York-Midnight-Opening-M15). Others use 02:00–05:00 (London), and narrower variants use 03:00–05:30 — [TMGM academy](https://www.tmgm.com/ru/academy/trading-academy/judas-swing); [LuxAlgo Judas Swing](https://www.luxalgo.com/library/concept/judas-swing.md). Some TradingView scripts use the first 15 minutes after midnight as the reference range — [TradingFinder M15 script](https://cn.tradingview.com/script/TYoIs4Q3-Judas-Swing-ICT-01-TradingFinder-New-York-Midnight-Opening-M15)
- Reference levels: the NY midnight open (primary), the session open, prior-day H/L, and Asian extremes. Rules: (1) mark the levels, (2) confirm the session timing, (3) watch for an early push through a level where stops sit, (4) require failure, with rejection and a break back through short-term structure with displacement, often leaving an FVG, (5) bullish means the day's low forms early below the open, bearish the mirror, (6) if price holds beyond the swept level, it is not a Judas swing — [LuxAlgo Judas Swing](https://www.luxalgo.com/library/concept/judas-swing.md)
- Entry is on the retrace into the displacement leg (OTE or FVG), not by chasing. Stop goes beyond the swept extreme. Target is the opposite-side liquidity pool. Some practitioners project with standard deviations of the manipulation leg — [LuxAlgo Judas Swing](https://www.luxalgo.com/library/concept/judas-swing.md)
- It is "an expectation, not a rule". A session can open and trend with no false move — [TradingView judas scripts](https://www.tradingview.com/scripts/judas/)
- PO3/AMD is anchored to "the midnight New York open for the day, Monday's open for the week, or a session open for intraday work". Accumulation straddles the open, manipulation runs resting liquidity and stalls, and distribution displaces back through the open and holds into the close. In intraday terms: Asia accumulates, London open manipulates, London into NY distributes. A bullish PO3 day "opens near its low, wicks below the open, and closes near its high". PO3 "is descriptive, not mechanical" — [LuxAlgo AMD](https://www.luxalgo.com/library/concept/accumulation-manipulation-distribution/)
- Entry per PO3: "wait for the manipulation sweep and the displacement back through the range, then join the distribution leg on a retracement". No stop or target is specified — [LuxAlgo AMD](https://www.luxalgo.com/library/concept/accumulation-manipulation-distribution/)

### Inferences
Codable Judas / PO3 rule set (1-minute, ET):
- [OBJ] MO = open of the 00:00 bar. Optionally also the 08:30 open and the 09:30 RTH open as alternative anchors, as a parameter.
- [OBJ] Bullish trigger: between 00:00 and 05:00 (or 09:30–10:30 for an NY variant), price trades below MO and sweeps the Asian low (20:00–00:00) or the prior-day low, then closes back above MO. Alternatively an MSS with an FVG. Entry is a limit at the FVG or OTE of the return leg. Stop goes below the swept low. Target is the Asian high, the prior-day high, or a standard-deviation projection of the manipulation leg (−1, −2 SD) as a parameter. Flat at 11:00 or 16:00.
- [OBJ] Alternative bias-only use: "below MO in the AM = discount, look for longs only" as a filter on other models.
- [DISC] Whether the session "should" reverse depends on HTF bias. The mechanical proxy is the prior-day close vs. the prior-day midpoint, or price relative to the weekly open.
- No overnight hold is needed. The London version trades 00:00–05:00 ET, which is overnight clock time but inside the same Globex session.

### Gaps
- The window (00:00–05:00 vs. 02:00–05:00) and whether ICT treats 08:30 as a second "true day open" anchor could not be confirmed from ICT material in this pass.

---

## Q4. London open / Asian range raid, NY open reversal, London close reversal, Turtle Soup

### Takeaway
These are all liquidity-raid reversals tied to kill zones. The Asian range (roughly 20:00–00:00 ET) is raided in the London open (02:00–05:00), and that extreme often becomes the day's high or low. NY open (07:00–10:00, or 08:30–11:00 for indices) extends or reverses London. London close (10:00–12:00) retraces the morning move. ICT's "turtle soup" is a generic raid of an obvious high or low plus structure confirmation. The Raschke/Connors original is a mechanical daily-bar system with a multi-day hold, so it inherently needs overnight holds in its original form.

### Cited Findings
- Session roles: the Asian range builds liquidity, London open tends to set the HOD/LOD, NY open extends or reverses London, and London close often retraces the morning range. NY open is 07:00–10:00 and London close 10:00–12:00 NY time, with an index-futures NY variant of 08:30–11:00 — [LuxAlgo Killzones](https://www.luxalgo.com/library/concept/killzones.md)
- Asian-raid rules (one vendor model): a raid of the Asian high on its own "most of the time, a trap". It is high probability only inside an HTF point of interest, and is not valid until price trades back into an FVG. If the London raid then breaks the opposite side of the Asian range with displacement, "the London extreme is very likely the high or the low of the day" — [TV Asian Range Liquidity Sweep Kill Zone Reversal](https://in.tradingview.com/script/1ZcOyqs5-Asian-Range-Liquidity-Sweep-Kill-Zone-Reversal/)
- London close times conflict across sources (10–12 EST vs. 15:00–17:00 vs. 14:00–16:00 GMT) — [LiteFinance kill zones](https://www.litefinance.org/blog/for-beginners/trading-strategies/ict-killzones?cid=303543); [LuxAlgo Killzones](https://www.luxalgo.com/library/concept/killzones/)
- **Original Turtle Soup (Street Smarts, 1995):** today makes a new 20-day low; "the previous 20-day low is at least four sessions old"; "the trade enters on a buy stop back above that prior low"; "initial stop below the new extreme"; no fixed target. Shorts are the mirror. Turtle Soup Plus One allows the failure on the next session — [LuxAlgo Turtle Soup](https://www.luxalgo.com/library/concept/turtle-soup.md). The entry buy-stop is "good for today only", profits are taken in 2–6 days, and the stop is trailed — [quantvps / tradingmarkets summaries via search](https://www.quantvps.com/blog/turtle-soup-trading-strategy); [TradingMarkets "Breakout After Failure"](https://tradingmarkets.com/recent/breakout_after_failure-654653). One forex article uses 3 sessions instead of 4 — [TradingMarkets](https://tradingmarkets.com/recent/breakout_after_failure-654653)
- **ICT version:** a discretionary restatement on any obvious swing high or low with visible stops, from weekly down to intraday session extremes. It "usually demands structure confirmation before entry" (change of character or an impulsive leg). Stop goes beyond the sweep, and the idea is abandoned if price closes back beyond the level. Target is the opposite side of the range or the opposite liquidity — [LuxAlgo Turtle Soup](https://www.luxalgo.com/library/concept/turtle-soup.md)
- TradingView "Turtle Soup" strategies often add RSI/ADX filters and cooldowns that are not in the original — [TV Turtle Soup strategy](https://www.tradingview.com/script/32Y7ZsaN-Grok-Claude-Turtle-Soup-Strategy)

### Inferences
- [OBJ] **London Asian-raid**: Asian range = H/L of 20:00–00:00 ET. Between 02:00 and 05:00, a sweep of one side followed by a close back inside plus an FVG in the opposite direction gives an entry at the FVG. Stop at the sweep extreme. Target the opposite Asian extreme, then the prior-day H/L. Flat by 11:00 (London close) or 12:00.
- [OBJ] **NY open reversal**: between 08:30 and 11:00, a sweep of the London session H/L (02:00–05:00) or the prior-day H/L, then MSS + FVG. Target the opposite London extreme. Flat by 12:00 or 16:00.
- [OBJ] **London close reversal**: between 10:00 and 12:00, if the day has already moved more than k×ADR from the midnight open, fade toward 50% of the morning range or the 08:30/09:30 open. ICT treats this as a lower-probability retracement trade.
- [OBJ] **Intraday turtle soup** (keeps the user's no-overnight constraint): replace "20-day" with a 20-bar lookback on 5m/15m, or use prior-day H/L as the level. Require the prior extreme to be at least 4 bars old (or simply the prior day). Use a buy-stop back above the level, valid for N bars. Stop below the new extreme. Exit at a fixed R, or at the opposite level, or by 16:00.
- The **original daily Turtle Soup needs overnight holds** (2–6 day hold). It can only be tested faithfully with overnight carry. An intraday-only proxy is "enter on the daily reclaim intraday, exit at 16:00".

### Gaps
- I did not obtain Street Smarts itself, so the 3 vs. 4 session age rule is not settled from the primary text. Most secondary sources say 4.
- I found no ICT source that formally defines the "NY open reversal" or "London close reversal" as stand-alone named models with entry rules. They appear as kill-zone tendencies.

---

## Q5. Unicorn, OTE, Venom, opening gaps (ORG/NDOG/NWOG), first presented FVG

### Takeaway
The **Unicorn** is a breaker block overlapping an FVG from the same displacement, entered on a retest. **OTE** is a 62–79% (sweet spot 70.5%) retracement of a displacement leg. **Venom** (introduced by ICT in 2025) uses the 08:00–09:30 ET range ("Venom box"), a sweep after 09:30, then MSS or CISD into an FVG. **ORG/NDOG/NWOG** are opening-gap reference levels whose CE (50%) is the key level. The **first presented FVG** is the first 1-minute FVG after 09:30. All of these geometries are codable. Swing selection and context are discretionary.

### Cited Findings
- **Unicorn:** the breaker block (an order block invalidated by a structure break, then retested) and an FVG from the same displacement overlap, and "the overlap is the unicorn zone". Bullish: a lower low, then a higher high, with the FVG overlapping the breaker and a retest. Entry on rejection in the zone on a lower timeframe. Stop just beyond the breaker. Target the next high/low or liquidity pool — [TV Unicorn guide](https://www.tradingview.com/chart/XAUUSD/zb6bDQzM-The-Unicorn-Model-Guide-to-ICT-s-Best-Standalone-setup). The Kodexius script uses an ATR-based minimum gap filter and close-based invalidation against the breaker boundary — [TV ICT Unicorn Model Kodexius](https://cn.tradingview.com/script/LSZLk5vJ-ICT-Unicorn-Model-Kodexius)
- **OTE:** zone 0.62–0.79 with the preferred level at 0.705. Anchor swing low to swing high on a displacement leg that breaks structure. Stop beyond the anchoring swing. Targets are the swing first, then extensions (not specified). A move beyond the leg's origin invalidates the setup. A sweep and MSS are expected first, and OTE "is not a standalone signal" — [LuxAlgo OTE](https://www.luxalgo.com/library/concept/optimal-trade-entry/)
- **Venom:** the 08:00–09:30 ET 90-minute "Venom box". After the 09:30 open, price sweeps one side (the low for a bullish day, the high for a bearish day) and reverses. Confirmation is MSS/CISD/FVG/order block, and entry is on a retrace to a PD array. NQ is called the cleanest market, with ES and YM also used. ICT "has described the model but has not released every detail" — [TradingFinder Venom script](https://cn.tradingview.com/script/0LMNMrpu-ICT-Venom-Trading-Model-TradingFinder-SMC-NY-Session-2025Setup); [TV Venom idea](https://cn.tradingview.com/chart/NQM2025/Gv0GpBle-Understanding-the-ICT-Venom-Model); [fxreplay "ICT's 2025 Venom Model"](https://www.fxreplay.com/strategies/icts-2025-venom-model); [innercircletrader.net "90-Minute Sweep Strategy"](https://innercircletrader.net/tutorials/ict-venom-trading-model-2025/)
- **NDOG** is the gap between the futures close and the reopen; on equity-index futures this is the 17:00–18:00 ET maintenance break. **NWOG** is Friday's close to the Sunday reopen. **Opening Range Gap** is the prior RTH close (16:00 or 16:15 ET) to the 09:30 open. CE is the 50% midpoint. "Many do fill… some fill only partway (commonly to the midpoint)", and there is no stable fill rate across instruments — [LuxAlgo Opening Gap](https://www.luxalgo.com/library/concept/opening-gap.md)
- One TradingView ORG script cites a "statistical probability of 70%" that price closes 50% or more of the ORG within the first 30 minutes. This is attributed to ICT but unverified — [TV MW ICT Open Range Gap](https://th.tradingview.com/script/q8eZ6kK4/)
- **First presented FVG:** indicator pages attribute to ICT a focus on the first 1-minute FVG after 09:30, which must form at 09:31 or later to count — [TV ICT Open Range Gap & 1st FVG](https://www.tradingview.com/script/gRgzwdXI-ICT-Open-Range-Gap-1st-FVG-fadi); [TV ICT 9:30am First FVG](https://tradingview.com/script/K587gQPT-ICT-9-30am-First-FVG)

### Inferences
- [OBJ] **Venom**: box = H/L of 08:00–09:29 bars. From 09:30 to about 10:30, a wick beyond one side followed by a close back inside the box plus MSS/FVG gives an entry at the FVG or CE. Stop beyond the sweep. Target the opposite box side, then 1–2× box height. Flat by 11:00 or 12:00. Very codable. Box-size filters (min/max points) are parameters.
- [OBJ] **First presented FVG**: the first FVG whose candle 3 closes at or after 09:31 (some versions use 09:30–10:00). Trade the first retrace into it in the FVG's direction (continuation) or use it as a level. Stop at the far edge. Target ORG CE / prior-day H/L.
- [OBJ] **ORG fill**: if |09:30 open − prior 16:00/16:15 close| > threshold, fade toward the CE within 30 minutes. Stop at k×gap beyond the open. This directly tests the "70% half-fill in 30 min" claim.
- [OBJ] **NDOG/NWOG** levels can serve as targets or filters intraday. Trading the NWOG fill as a multi-day trade would need overnight holds.
- [OBJ, with a parameter] **Unicorn**: define the order block as the last opposing candle before the leg that swept; the breaker forms when price closes through it. Unicorn zone = intersection of the breaker range and the FVG; skip if empty. Swing and order-block definitions are the main discretionary choices.
- [OBJ] **OTE** as an entry overlay on any of the above legs (limit at 0.705, stop beyond 1.0).

### Gaps
- Venom's official target, invalidation and time-cutoff details could not be retrieved. innercircletrader.net and fxreplay were unreadable (images / 403). Community sources say ICT did not release full details.
- The 70% ORG statistic and the "09:31 or later" first-FVG rule could not be traced to a dated ICT lecture.

---

## Q6. Daily bias methods: can bias be made mechanical?

### Takeaway
ICT bias is built from the higher-timeframe draw on liquidity (prior-day and prior-week H/L, unfilled HTF FVGs) and premium/discount relative to a dealing range, plus weekly-profile templates such as "Classic Tuesday low of week". It can be partly mechanised with proxies (which prior-day extreme is nearer or unswept, price vs. the midnight or weekly open, premium/discount of the prior-day range). The template choice itself is discretionary and largely hindsight-labelled.

### Cited Findings
- Daily bias is "the expected direction of the day's expansion", built from HTF structure, prior-day H/L and the nearest pool of resting liquidity. The Judas swing is the false move against bias that forms the day's extreme. A bullish week typically puts its low on Monday or Tuesday — [LuxAlgo Session & Weekly Profiles](https://www.luxalgo.com/library/concept/session-and-weekly-profiles.md)
- Classic Tuesday low: if Monday doesn't reach the discount array, Tuesday often drives lower to set the week's low in London or NY, then resumes up — [TV Master ICT Weekly Profiles](https://www.tradingview.com/chart/GC1!/vVKtluBi-Master-ICT-Weekly-Profiles)
- If the weekly draw is up, a Tuesday low should be protected — [TV NQ Tuesday setup idea](https://www.tradingview.com/chart/MNQU2025/gUMxR6qv-NQ-Nasdaq-Futures-Tuesday-Setup-09-09-2025/)
- A TradingView "Bias Engine" script automates bias from prior-week and prior-day H/L, draw targets and premium/discount — [TV Bias Engine ICT Concept](https://fr.tradingview.com/script/kJOkZ7PG-Bias-Engine-ICT-Concept/)

### Inferences
Candidate mechanical bias rules to test as filters:
- (a) Prior-day close in the upper or lower half of the prior-day range → long or short bias (premium/discount).
- (b) Did yesterday sweep the prior-day high but not the low? Then the draw is the low (or the reverse).
- (c) Price at 08:30 or 09:30 relative to the midnight open (Judas logic: below the open → long bias).
- (d) Weekly-profile proxy: if Monday–Tuesday made the week's low by Tuesday close and price is above the weekly open, bias long Wednesday–Thursday.
- Each is objective, and none has published validation. Weekly profiles look out across several days but do not require overnight positions when used only as a filter.

### Gaps
- No primary ICT definition of a deterministic bias algorithm was found. ICT presents bias as discretionary. No published out-of-sample test of any mechanical ICT bias rule was found.

---

## Q7. Instruments, R:R, trades/day, discretion: summary table

### Takeaway
ICT's index-futures models (Silver Bullet, 2022, Venom, ORG/first FVG) are taught primarily on NQ and ES. London-session models come from his FX teaching (6E/6B equivalents). Target R is typically 2:1 to 3–5:1, and he favours one or two trades per day or per window. Time windows and geometry are objective. Draw-on-liquidity choice, displacement quality and HTF bias are the recurring discretionary elements.

### Cited Findings
- Silver Bullet was designed for and tested on NQ/ES — [TV silverbullet scripts](https://cn.tradingview.com/scripts/silverbullet). Venom is "cleanest" on NQ and also used on ES/YM — [TV Venom idea](https://cn.tradingview.com/chart/NQM2025/Gv0GpBle-Understanding-the-ICT-Venom-Model). The Silver Bullet suits index futures and major FX — [LuxAlgo Silver Bullet](https://www.luxalgo.com/library/concept/silver-bullet.md)
- 2022 Model: 3:1–5:1 textbook R — [Quantum Algo](https://www.quantum-algo.com/blog/guides/ict-2022-model-complete-guide/). Silver Bullet: minimum 2:1, one attempt per window — [TV SB idea](https://pl.tradingview.com/chart/EURUSD/jOkVQBxm-What-Is-the-ICT-Silver-Bullet-Strategy-and-How-Does-It-Work); [LuxAlgo Silver Bullet](https://www.luxalgo.com/library/concept/silver-bullet.md)

### Inferences
| Setup | Window (ET) | Primary instruments | Typical target | Trades/day | Overnight hold? | Objective parts | Discretionary parts |
|---|---|---|---|---|---|---|---|
| Silver Bullet | 03–04, 10–11, 14–15 | NQ, ES (also GC, 6E) | opposing liquidity, ≥2R; min pts (param) | ≤1 per window | No | window, FVG, entry, stop | draw on liquidity, sweep validity |
| 2022 Model | kill zones (07–10, 08:30–11, 13:30–16) | NQ, ES, FX | opposite pool, 3–5R | 1–2 | No | sweep→MSS→FVG sequence | displacement strength, HTF bias, which FVG |
| Judas / PO3 | 00–05 (London), NY variant 09:30–10:30 | ES/NQ, 6E/6B | opposite Asian/PD extreme, SD projections | 1 | No | midnight open, sweep, reclaim | whether bias day is "reversal" |
| Asian-range raid (London) | 02–05 | 6E, 6B, GC, ES/NQ | opposite Asian extreme | 1 | No | Asian H/L, sweep, FVG | HTF POI filter |
| NY open reversal | 08:30–11 | ES, NQ | London H/L | 1 | No | levels, MSS | bias |
| London close reversal | 10–12 | 6E, ES/NQ | 50% of AM range | 1 | No | time, range | when trend is "done" |
| Turtle Soup (ICT intraday) | any kill zone | all | opposite range side | 1–2 | No | level, reclaim stop-entry | which level |
| Turtle Soup (Raschke original) | daily bars | all | 2–6 day hold | ≤1 | **Yes** | fully mechanical | none |
| Unicorn | kill zones | NQ, ES, GC | next H/L | 0–2 | No | breaker ∩ FVG | OB/swing definition |
| OTE | overlay | all | swing, extensions | n/a | No | fib levels | leg anchoring |
| Venom | box 08:00–09:30, trade 09:30–~11 | NQ (ES, YM) | opposite box side | 1 | No | box, sweep, FVG | target/exit details unreleased |
| ORG / 1st FVG | 09:30–10:00 | ES, NQ | ORG CE / PD levels | 1 | No | gap, CE, first FVG | context |
| NWOG/NDOG | levels | ES, NQ | as targets | n/a | Yes for weekly-fill trades | levels | usage |

- Trades-per-day and instrument assignments in the table beyond the cited items are my synthesis.
- Given the negative independent Silver Bullet backtests (GBB, the 25k-variation video), the most informative tests are: (1) a shared sweep→MSS→FVG engine with a time filter on/off, comparing each window against volatility-matched non-window hours; (2) mechanical Judas/Venom/ORG variants, which are the most rule-complete; (3) bias filters (a)–(d) as add-on ablations.

### Gaps
- No source states ICT's own recommended trades per day for each model. "One trade per window" is a community summary. CL, ZN, ZB, 6J and RTY are rarely mentioned in ICT-model sources. Applying the models to them is untested extrapolation.
