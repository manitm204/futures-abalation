# Quantitative evidence for and against ICT / Smart Money Concepts (as of Nov 2026)

Evidence-quality legend used below:
- **[A]** peer-reviewed / central-bank research with stated data and method
- **[B]** preprint or practitioner study with stated sample, null/baseline and (ideally) costs/OOS
- **[C]** vendor/blog/indicator statistic, method partly stated, not independently verifiable
- **[D]** marketing claim / anecdote / forum allegation

## 1. Systematic backtests of ICT setups (FVG, order blocks, liquidity sweeps, Silver Bullet, killzones)

### Takeaway
Every test that uses a proper baseline (random/placebo levels, matched-return null, multiple-testing correction) finds that FVGs, order blocks and OTE carry no detectable edge over random entry; the one ICT element that repeatedly survives is the **liquidity sweep of a prior level**, and even there the evidence is mixed on direction (one FX study finds swept levels predict *continuation*, not reversal). Favourable numbers come almost exclusively from vendor pages, tiny samples, in-sample optimisation or no-cost tests.

### Cited Findings

**Fair value gaps**
- [B/C] TradingView "FVG Statistics with Placebo Control": for each real FVG it builds placebo zones of identical height, direction and distance anchored on bars where no FVG formed, scored by the same symmetric target/stop rules. 14 measurements across crypto, FX and equity-index futures, 5m/30m/1h, two non-overlapping periods, three target/stop distances, two time limits. Largest real-minus-placebo deviation = 1.49 standard errors (≈1.9 expected by chance across 14 tests); pooled real-minus-placebo = **−0.04 pp (95% CI ≈ −1.2 to +1.1 pp)**. Shows how a 54% raw hit rate is "significant" vs 50% (p≈0.003) but not vs the observed placebo baseline. Costs excluded. Per-instrument equity-index table did not render in the extracted text. — [TradingView script, placebo-control FVG](https://de.tradingview.com/script/Kbq3WncE-Fair-Value-Gap-FVG-Statistics-with-Placebo-Control/)
- [C] Random-walk simulation by a trade-copier blog (1,000,000 bars, seed 42 and 7): 148,789 bullish gaps; revisited within 20 bars 83.4% vs 83.5% for random levels; fully filled 73.1% for both, i.e. high "FVG fill rates" are what a random walk produces. — [ThorTradeCopier blog](https://thortradecopier.com/blog/does-ict-smart-money-concepts-work)
- [C] FVG "fill rate" indicator statistics (e.g. ~8/10 BTC 1h gaps filled within 100 bars; "82% of daily gold gaps fill") depend entirely on fill definition (full traverse vs midpoint) and bar window, and do not compare to a baseline. — [TradingView M-Alpha FVG fill script](https://www.tradingview.com/script/KDRll5dY/)
- [B] Bindra (2026, SSRN preprint): 473 FVG trades in gold + three FX pairs in 2025, reported 78.0% win rate and +265R; abstract mentions no OOS test, random baseline, or transaction costs (as summarised secondhand). — [ThorTradeCopier summary](https://thortradecopier.com/blog/does-ict-smart-money-concepts-work)

**Multi-concept systematic studies**
- [B] Tangirala (SSRN 2026), "Do Smart Money Concepts Predict Returns? Evidence from 44 Formalised Detectors on S&P 500 Daily Bars, 2010–2026": against a zero-return null 38/44 detectors look significant; against a **matched-return null with Benjamini-Hochberg control over 352 concept×horizon hypotheses, none beats random entry at any horizon**. Described as a corrected re-analysis of an earlier version that had reported favourable results. (Daily bars, not intraday.) — [SSRN 7483658](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7483658) (abstract via search snippet; full page blocked to fetch)
- [B] Mahadzva (SSRN 2026, unreviewed), "Smart Money or Costly Folklore? A Systematic Evaluation of ICT/SMC Trading Rules in G10 FX": six ICT/SMC rules coded mechanically on intraday EURUSD, GBPUSD, AUDUSD, USDJPY; walk-forward, bootstrap, permutation and holdout tests. Abstract: "We find no evidence that ICT/SMC concepts work as literally taught." Three independently built sweep rules agreed in **65 of 66 fold selections that a swept level predicts continuation, not reversal**. Flagship survivor: a change-of-character confirmed by FVG retracement **traded in the opposite (faded) direction** on EURUSD 1h, p = 0.0192, +19.3% on 60 holdout trades, PF 1.50 — but it fails a Deflated Sharpe Ratio check at every defensible trial count. One strategy's per-trade edge was smaller than the fixed commission forced by its tight stops until a minimum stop distance was imposed. — [SSRN 7430998](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7430998); details via [ThorTradeCopier summary](https://thortradecopier.com/blog/does-ict-smart-money-concepts-work)
- [B] StatOasis "I Backtested ICT / SMC — What Survives": SPY/QQQ/DIA/IWM daily bars (from 1993–2000 to 2026), 648 backtests (7 entry families × 54 variants × 3 exits × 4 markets), frictionless, next-open fills, no holdout. SPY forward edge vs drift: Order Block 736 events +0.121% at 5d (t=1.22); FVG 1,122 events −0.005% (t=−0.08); Liquidity Sweep 547 events +0.119% (t=0.94); OTE 206 events −0.028% (t=−0.17). Only 1 of 32 t-stats reached 2 (OTE on DIA 10d, t=2.07 — consistent with chance). No variant of any family beat buy-and-hold; Order Block was the only family that beat a frequency-matched coin flip in a majority of variants in every market (81.5/66.7/59.3/55.6%), not a significance test. — [StatOasis](https://statoasis.com/overfit/research/ict-backtest-what-survives)
- [C] IndicatorEdge: EURUSD 1-minute (2,553,973 bars, HistData), 2019–2025, 0.5-pip round-trip cost, 54 variations (2 encodings: "sweep → structure shift → gap" and "first gap"; windows London 03–04, AM 10–11, PM 14–15 ET; R:R 1/2/3; bias daily/none/open). No lookahead, fills require trade-through, ambiguous bars = stop first. **0 of 54 profitable after costs; best PF 0.89**; best win rate 56.3% (PM, 1:1, 126 trades) but expectancy −0.054R. Also states it found no peer-reviewed validation of order blocks. — [IndicatorEdge smart-money research](https://indicatoredge.io/smart-money-research)
- [C] FXNX (broker blog): 1,000 mechanical trades on EURUSD/GBPUSD/USDJPY in Python; isolated order block bounce rate 43.1% (56.9% failure); OBs only useful when accompanied by displacement leaving an FVG; full setup win rate ≈41% (no PF/cost detail captured). — [FXNX blog](https://fxnx.com/en/blog/smart-money-concepts-work-backtest-evidence)

**Silver Bullet / killzones (ES & NQ 1-minute — the most directly relevant test found)**
- [B/C] "I backtested 25,000 ICT Silver Bullet trades" (YouTube, summarised by Gistly; author "Adam S."): 16 years of NQ and ES 1-minute data, last 2 years held out; 25,000 random configurations sampled from ~258M; >10M simulated trades; commissions and slippage included (amounts not stated); same-bar stop+target = loss; paper fills (touch-fills, so optimistic). Funnel: 9,481 configs with 100+ trades → 6,190 profitable after costs → 1,614 passed a luck correction → **420 passed a no-adjustment ES "cold run" (1.7% survive)**. Findings: **requiring a liquidity sweep before entry was the only rule that consistently added edge**; 1-min FVG entry beat 5-min; 15-min bias and market-structure-shift filters *hurt* performance; **the ICT "special hours" did no better than other hours** (10:00 window slightly negative; 14:00 and London "fine"); textbook frequency (~34 trades/yr) too sparse. Best survivor +$455k on one contract over the 2-year holdout, but holdout was a strong bull market (long-biased dip buying after sweeps benefits) and fills were paper. — [Gistly summary](https://gist.ly/youtube-summarizer/i-backtested-25000-ict-silver-bullet-trades)
- [D] takeprofitapp guide: 2024–2025 EURUSD Silver Bullet, 134 setups, 60.4% WR, avg R:R 1:2.3, PF 2.81 — tiny sample, no OOS/cost detail, marketing page. — [takeprofitapp](https://takeprofitapp.com/en/learn/ict-silver-bullet-strategy)
- [D] dev.to Pine Script ICT OB+FVG: BTCUSDT PF 1.42, MaxDD −8.2%, 312 trades; methodology unverifiable. — [dev.to](https://dev.to/isabelle_dubuis_d858453d7/ict-order-block-fvg-strategy-in-pine-script-v5-backtest-results-full-code-l5c)
- The popular Python library `joshyattridge/smart-money-concepts` provides detectors (FVG, OB, BOS/CHoCH, liquidity) but publishes no strategy performance. — [GitHub](https://github.com/joshyattridge/smart-money-concepts)

**Turtle soup (failed breakout — ICT relabels it)**
- [C] Oxfordstrat tested Connors/Raschke Turtle Soup with and without $100 round-turn costs; values only in charts, not extractable. — [Oxfordstrat](https://oxfordstrat.com/?p=5614)

### Inferences
- The consistent pattern: **raw hit/fill rates look impressive, but vanish against a matched/placebo baseline**. Any FVG/OB test you run must include a placebo-zone or random-level control or it is uninformative.
- **Liquidity sweep is the only ICT element with repeated (weak-to-moderate) support**, but the *direction* is contested: NQ/ES Silver Bullet test says sweep→reversal entry adds edge; Mahadzva's FX folds say swept levels predict continuation. This is a cleanly testable, falsifiable hypothesis on 1-min futures (sweep-then-reclaim vs sweep-then-continue, with a random-level control).
- ICT's high-timeframe bias / MSS filters and "magic" killzone hours did not help in the one large ES/NQ test; time-of-day matters for volatility, not for directional edge of the ICT pattern.
- Several apparent survivors (Mahadzva flagship, Silver Bullet top config) are artefacts of searching huge spaces; DSR/luck correction kills most. Report trial counts.

### Gaps
- Could not retrieve SSRN full texts (403); Tangirala and Mahadzva numbers come from abstract snippets/secondary summary.
- No independent, reproducible ES/NQ test of order blocks, Judas swing, or Asian/London range raids with costs + OOS found. The Silver Bullet study is a YouTube video (summary only; code/data not verified; cost assumptions unstated).
- Placebo-FVG script's equity-index-futures per-instrument numbers not extractable.
- No Quantified Strategies or Robot Wealth ICT-specific test was found in searches.

## 2. Academic literature on the mechanisms ICT invokes

### Takeaway
The microstructure ICT borrows from is real and well-documented in FX (stop-loss clustering just beyond round numbers, take-profit clustering at round numbers, stop-triggered cascades, modest bounce at published S/R levels), and equity-index intraday momentum (first half-hour → last half-hour) is a robust, published futures effect; but these effects are small, mostly FX/1990s–2000s, and none validate ICT's specific constructions (FVG, OB, OTE).

### Cited Findings
- [A] Osler (2003, Journal of Finance 58(5):1791–1819; FRBNY SR125): 9,667 stop-loss/take-profit orders at a large dealing bank, Sep 1999–Apr 2000. Take-profit orders cluster at round numbers (explains reversals at S/R); stop-loss orders cluster just beyond round numbers (explains acceleration after levels break). Stop-loss buys: 14.4% at prices just above round numbers (01–10) vs 7.4% just below; stop-loss sells: 10.0% just below vs 5.1% just above. — [NY Fed SR125](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr125.pdf); [RePEc JF](https://ideas.repec.org/a/bla/jfinan/v58y2003i5p1791-1819.html); figures via [ThorTradeCopier](https://thortradecopier.com/blog/does-ict-smart-money-concepts-work)
- [A] Osler (2005, J. of International Money and Finance; FRBNY SR150) "Stop-loss orders and price cascades in currency markets": minute FX data (USD/DEM, USD/JPY etc.); rates move faster after hitting levels where stop-losses cluster; stop-loss response larger and longer-lasting than take-profit response; significant over hours, not days; Osler notes causality not proven. — [NY Fed SR150](https://www.newyorkfed.org/research/staff_reports/sr150.html); [paper draft](https://icmaif.soc.uoc.gr/Year/8conf/docs/Osler-Price%20Cascades-03-03.doc)
- [A] Osler (2000, FRBNY Economic Policy Review 6(2)) "Support for Resistance": published S/R levels from six firms, Jan 1996–Mar 1998, 1-minute FX, vs 10,000 sets of arbitrary levels. Bounce rate 60.8% at published levels vs 56.2% at arbitrary levels (+4.6 pp); profitability not assessed. — [NY Fed EPR](https://www.newyorkfed.org/medialibrary/media/research/epr/00v06n2/0007osle.pdf); numbers via [ThorTradeCopier](https://thortradecopier.com/blog/does-ict-smart-money-concepts-work)
- [A] Savaser & Osler (2010 working paper): price-contingent (stop/take-profit) trading may account for over half the excess kurtosis in currency returns. — [Brandeis WP](https://www.brandeis.edu/economics/RePEc/brd/doc/Brandeis_WP04.pdf)
- [A] Gao, Han, Li & Zhou (2018, JFE 129(2):394–414): first half-hour return predicts last half-hour return on SPY 1993–2013 (predictive R² ≈1.6%); holds for S&P 500 futures and international index futures. — [working paper](https://www3.nd.edu/~zda/intramom.pdf); [RePEc](https://econpapers.repec.org/RePEc:eee:jfinec:v:129:y:2018:i:2:p:394-414)
- [A] Baltussen, Da, Lammers & Martens (2021, JFE) "Hedging demand and market intraday momentum": >60 futures (equity, bond, commodity, FX), 1974–2020; intraday momentum driven by negative-gamma option dealer and leveraged-ETF hedging. — [Alpha Architect summary](https://alphaarchitect.com/hot-topic-does-gamma-hedging-actually-affect-stock-prices/); [ND](https://www3.nd.edu/~zda/EOD.pdf)
- [A] Individual stocks show end-of-day *reversal* rather than momentum (contrasts with market-level momentum). — [ND EOD paper](https://www3.nd.edu/~zda/EOD.pdf)
- [A] Session/killzone volatility: Andersen & Bollerslev (1997/98) and Ito & Hashimoto (2006, NBER w12413) document U-shaped intraday activity/volatility and session-open clustering — volatility, not direction. — [NBER w12413](https://www.nber.org/papers/w12413); cited list at [IndicatorEdge](https://indicatoredge.io/smart-money-research)
- [A] Tsinaslanidis et al. (2022): Fibonacci zones performed no better than random non-Fibonacci zones (relevant to OTE 62–79%). — cited at [IndicatorEdge](https://indicatoredge.io/smart-money-research)
- [C] ES opening-gap fill: ES daily Jan 2002–Feb 2004, 528 gaps, ~76% filled (prior close touched) during RTH; author calls study unfinished; no comparison to unconditional range. — [mypivots](https://mypivots.com/gapfill)
- [C] Prior-day range (Edgeful): when ES/NQ/TSLA/NVDA open inside yesterday's range, yesterday's high or low is reached 81–88% of the time (last 6 months, NY session); YM: green close 67% after prior-high break, red close 62% after prior-low break, varies strongly by weekday. — [Edgeful inside-day](https://www.edgeful.com/blog/posts/inside-day-in-trading-breakout-data); [Edgeful prior-day range report](https://www.edgeful.com/blog/posts/previous-days-range-report)
- [D] NexusFi personal log, NQ: "break either" yesterday's high/low on 90.32% of 168 days. — [NexusFi](https://nexusfi.com/showthread.php?p=550945)
- [A] Harvey, Liu & Zhu (2016): require t > 3.0 for new factors in data-mined fields — relevant bar for ICT-variant searches. — [NBER w20592](https://www.nber.org/papers/w20592)

### Inferences
- Osler's work supports the *existence* of stop clusters beyond obvious levels and cascades through them — which actually argues for **momentum/continuation after a clean break**, matching Mahadzva's continuation finding; ICT's "sweep and reverse" reading corresponds instead to take-profit/limit-depth absorption at the level, which Osler finds produces only a few-pp bounce excess.
- Very high "prior-day high/low gets hit" and "gap fill" rates are largely mechanical (daily range vs distance to level). Edge must be measured as conditional return vs unconditional, not hit rate.
- The best-documented futures intraday effect that overlaps ICT "timing" is intraday momentum into the close (not killzone reversal) — and your repo has already been testing a last-half-hour family.

### Gaps
- No peer-reviewed study found specifically on ES/NQ behaviour after sweeps of prior-day/overnight (Globex) highs/lows at the 9:30 open, or on failed-breakout reversals in index futures intraday with costs.
- Osler data are FX 1996–2005; transferability to CME futures (centralised book, different stop placement) is unverified.
- Kavajecz & Odders-White style limit-order-book/S&R studies not retrieved in this pass.

## 3. Practitioner / stats-site evidence quality

### Takeaway
Practitioner evidence splits into (a) baseline-controlled tests (placebo FVG, StatOasis, IndicatorEdge, Tangirala, Mahadzva) that are uniformly negative, and (b) descriptive stats sites (Edgeful, TradingView indicators, vendor blogs) that report hit/fill rates without baselines and are not evidence of a tradable edge.

### Cited Findings
- Edgeful sells 150+ "reports" including an "ICT opening retracement report"; these are frequency statistics over recent windows (e.g. last 6 months), not cost-inclusive backtests. — [Edgeful reports guide](https://www.edgeful.com/blog/posts/edgeful-reports-the-complete-guide); [ICT opening retracement report](https://intercom.help/edgeful/en/articles/14998693-ict-opening-retracement-report-what-it-measures-and-how-to-read-it)
- ES/NQ gap-fill TradingView indicator claims 2,600+ ES and 2,700+ NQ days (2014–2024); method not public. — [TradingView gap-fill stats](https://www.tradingview.com/script/32pGGSWx-Gap-Fill-Probability-Statistics-ES-NQ/)
- A blog search of Crossref found no peer-reviewed test of ICT/SMC concepts as defined; a 2026 Informatica paper on SMC signals for XAUUSD reports in-sample results only. — [ThorTradeCopier](https://thortradecopier.com/blog/does-ict-smart-money-concepts-work); [Informatica](https://www.informatica.si/index.php/informatica/article/view/12899/6712)
- IJNRD paper using SMC features in ML reports favourable but in-sample results with paired t-tests (weak design). — [IJNRD2411009](https://www.ijnrd.org/papers/IJNRD2411009.pdf)

### Inferences
- Effect sizes in the credible studies are ~0 (placebo FVG: −0.04 pp; StatOasis t-stats mostly <1.3). Anything claiming 60–80% win rates for FVG/Silver Bullet comes from small, in-sample or no-cost samples.

### Gaps
- No r/algotrading systematic test with code/data retrieved in this pass.
- Quantpedia / Quantified Strategies / Robot Wealth: no ICT-specific articles found.

## 4. Critiques: relabeled TA, hindsight bias, Huddleston's record, regulation

### Takeaway
Core ICT ideas map onto older TA (turtle soup = Connors/Raschke 1995 failed breakout; OTE = Fibonacci retracement; liquidity pools = Osler-style stop clusters); there is no verified, broker-statement-backed public track record for Huddleston; the contest episode commonly cited is the **2024** (not 2023) Robbins World Cup, and claims about its outcome are unverified forum allegations. No regulatory action was found.

### Cited Findings
- Turtle Soup originates in Connors & Raschke's *Street Smarts* (fade of a failed 20-day breakout) — the pattern ICT's "liquidity sweep / turtle soup" borrows. — [therighttrader](https://therighttrader.com/learn/trading-strategies/turtle-soup)
- NexusFi open letter to Joel Robbins says Huddleston entered the 2024 Robbins World Cup and alleges he publicly committed to posting broker statements and daily stats by 1 March 2024 but did not; raises multiple-account transparency concerns. Unverified forum post (page 403 to fetch; content via search snippets). — [NexusFi](https://nexusfi.com/showthread.php?p=899824)
- Robbins WCTC rules allow entry any time and average a second account into results. — [Finance Magnates](https://www.financemagnates.com/thought-leadership/robbins-world-cup-trading-championship-expands-japan/)
- ICT podcast archive: ICT discussed plans to enter the Robbins Cup for 2024; "Final ICT Shotgun Saturday — farewell" episode dated 11 Nov 2023. — [Chartable archive](https://chartable.com/podcasts/the-inner-circle-trader-twitter-spaces-archive/episodes/154989542-final-ict-shotgun-saturday-farewell-and-adieu-november-11-2023)
- Forex Peace Army user reviews allege he failed a 2016 public bid to trade to $1M and "blew his account" in the 2024 Robbins Cup — anonymous, unverified. — [FPA review](https://www.forexpeacearmy.com/forex-reviews/13001/inner-circle-trader-ict)
- A BabyPips thread tracked an earlier ICT "5k to 1mil" live challenge. — [BabyPips](https://forums.babypips.com/t/inner-circle-traders-5k-to-1mil-live-trading-tracking-thread/49488?page=15)
- Critics allege hindsight showcasing (posting winners, not losers) in contest contexts — opinion, no data. — [Gistly summary of critical video](https://gist.ly/youtube-summarizer/the-truth-behind-robins-world-cup-trading-championship)
- Writofinance: before 2016 shift to free content Huddleston charged up to $20,000 for mentorship; main criticism is lack of independently verified performance. — [Writofinance](https://www.writofinance.com/inner-circle-trader-ict-michael/)
- Search of SEC/FTC/CFTC-related results found no action against Huddleston/ICT. — (negative search result; see Gaps)

### Inferences
- The user's "2023 public challenge" premise is likely the 2024 Robbins Cup entry announced in late 2023; no official WCTC result for him was found.
- Hindsight/survivorship bias is structural in ICT teaching: setups are drawn on completed charts with discretionary definitions, which is exactly why mechanical encodings with baselines show the edge disappearing.

### Gaps
- No official Robbins WCTC 2024 standings or broker statements for Huddleston found (worldcupadvisor.com not checked).
- CFTC/NFA BASIC registry not queried directly; "no regulatory action" is an absence-of-search-results finding, not confirmation.

## 5. Which ICT ideas plausibly carry edge after costs on 1-minute futures bars

### Takeaway
Plausible (worth testing with controls): **liquidity sweeps of objective prior levels** (prior-day H/L, overnight/Globex H/L, round numbers), tested both as reversal and as continuation, with a random-level control; and **time-of-day conditioning tied to known flows** (open, intraday momentum into close). Likely noise: FVG fill/reaction, order blocks, OTE/Fibonacci, HTF bias/MSS filters, and the specific Silver Bullet/killzone hours.

### Cited Findings
- Sweep requirement was the only rule consistently adding edge in the 25k-config ES/NQ 1-min Silver Bullet test; killzone hours no better than others; MSS/15-min bias hurt. — [Gistly](https://gist.ly/youtube-summarizer/i-backtested-25000-ict-silver-bullet-trades)
- Swept levels predicted continuation in 65/66 FX walk-forward folds. — [ThorTradeCopier summary of Mahadzva](https://thortradecopier.com/blog/does-ict-smart-money-concepts-work)
- Stop clusters sit just beyond round numbers and their triggering accelerates moves (FX). — [NY Fed SR125](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr125.pdf); [SR150](https://www.newyorkfed.org/research/staff_reports/sr150.html)
- FVG ≈ placebo (−0.04 pp pooled), and FVG revisit rates equal random levels in random-walk simulation. — [placebo FVG](https://de.tradingview.com/script/Kbq3WncE-Fair-Value-Gap-FVG-Statistics-with-Placebo-Control/); [ThorTradeCopier](https://thortradecopier.com/blog/does-ict-smart-money-concepts-work)
- EURUSD 1-min ICT encodings: 0/54 profitable after 0.5-pip costs, best PF 0.89. — [IndicatorEdge](https://indicatoredge.io/smart-money-research)
- Intraday momentum (first 30 min → last 30 min) robust in index futures. — [Gao et al.](https://www3.nd.edu/~zda/intramom.pdf); [Baltussen et al.](https://alphaarchitect.com/hot-topic-does-gamma-hedging-actually-affect-stock-prices/)

### Inferences
- Recommended test design for this repo: (1) define sweep = trade through prior-day/overnight/round-number level by ≥k ticks then close back inside within N bars; (2) evaluate both fade and continuation; (3) compare with matched random levels at equal distance; (4) include ES/NQ round-trip costs and a no-touch-fill rule; (5) record trial counts and apply DSR/BH correction; (6) holdout spanning a non-bull regime.
- Expect any survivor to be small (Osler's level effect ≈ +4.6 pp bounce excess in FX) and therefore sensitive to 1-tick slippage on tight-stop 1-min trades — the Mahadzva cost note shows tight-stop ICT entries can be eaten by commissions.
- FVG and OB are better treated as entry-timing refinements whose value should be ablated (sweep alone vs sweep+FVG) rather than as standalone signals.

### Gaps
- No credible CL, GC, Treasury or CME FX-futures-specific ICT test found; FX spot (EURUSD etc.) evidence is the closest proxy for 6E.
- Silver Bullet study's cost assumptions and code unavailable, so its positive holdout cannot be reproduced from public info.
