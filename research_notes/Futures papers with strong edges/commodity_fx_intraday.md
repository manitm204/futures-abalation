# Intraday strategies for CL, GC, 6E and 6J futures: published evidence, costs and ablation design

Scope: intraday-only (flat by the end of the day) strategies computable from 1-minute OHLCV bars plus public event calendars. Families the user has already tested are excluded (see the last section). Research budget: about 18 tool calls, so several papers were read from their abstracts only. This is flagged wherever it applies.

Cost benchmark used throughout: about 1 tick plus $2.50 per side, so a round trip costs about $25 for CL, $25 for GC and $30 for 6E/6J. For scale, using approximate late-2025/2026 prices (my assumption, not sourced): GC at about $4,000/oz x 100 oz is about $400k notional, so 1 bp is about $40. CL at about $65 x 1,000 bbl is about $65k notional, so 1 bp is about $6.5. 6E at about 1.15 x 125,000 is about $144k, so 1 bp is about $14. 6J at about 12.5M yen is about $80k, so 1 bp is about $8. A strategy therefore needs gross edges of roughly 0.6 bp (GC), 4 bp (CL), 2 bp (6E) or 4 bp (6J) per round trip just to break even.

## Q1. Which intraday effects in these markets have evidence that survives costs and holds out of sample?

### Takeaway
No published intraday strategy on CL, GC, 6E or 6J has strong, peer-reviewed evidence of profits net of realistic costs AND out of sample after 2018. The best documented candidate is "market intraday momentum" (rest-of-day return predicts the last 30 minutes before the pit-hours close). It is out-of-sample significant in GC only. It is not significant for CL, and it is absent in 6E and weak or absent in 6J and in currencies since 2000. Gross per-trade edges are on the order of the cost. Event-driven CL strategies around the EIA report (pre-release drift and the post-release reaction and reversal) have evidence but no published net-of-cost or post-2018 numbers.

### Cited Findings

**A. Market intraday momentum (Baltussen, Da, Lammers & Martens 2021, JFE 142:377–403)**
- Data: tick data on more than 60 futures (equities, bonds, 21 commodities, 8 currencies), 1974–2020. Finding: "The return during the last 30 minutes before the market close is positively predicted by the return during the rest of the day (from previous market close to the last 30 minutes)" and "reverts over the next days." — [Baltussen et al. 2021, JFE (author PDF)](https://academicweb.nd.edu/~zda/intramom.pdf)
- The sessions used are pit/volume-based "day" sessions in ET: GC 08:20–13:30 (sample 1984–2020), CL 09:00–14:30 (1987–2020), Euro FX (EC=6E) 07:20–14:00 (1999–2020), JY (6J) 07:20–14:00 (1977–2020). The last half-hour is therefore GC 13:00–13:30, CL 14:00–14:30, and 6E/6J 13:30–14:00. — [Baltussen et al. 2021, Tables 1 and A3–A4](https://academicweb.nd.edu/~zda/intramom.pdf)
- Strategy rule (Eq. 12): if the predictor return r > 0, go long over the last half-hour; otherwise go short. The predictors are rONFH (prior close to the end of the first half-hour) or rROD (prior close to 30 minutes before the close). A combined variant trades only when the signs of rONFH and rROD agree. — [Baltussen et al. 2021](https://academicweb.nd.edu/~zda/intramom.pdf)
- Table 6 results for an equal-weighted 1/N portfolio per asset class, 1974–2020, gross of costs:
  - Commodities: η(rONFH) 2.48%/yr, vol 3.03%, SR 0.82. η(rONFH, rROD) 3.29%, SR 1.29. η(rROD) 4.34%, SR 1.42, hit rate 0.56. Always-long in the last half-hour: SR −0.19.
  - Currencies: η(rONFH) 0.93%/yr, SR 0.96. η(rROD) 0.85%, SR 0.87, hit rate 0.53. — [Baltussen et al. 2021, Table 6](https://academicweb.nd.edu/~zda/intramom.pdf)
- The authors state: "Note that we do not consider transaction costs... the strategy as presented might not be exploitable to many investors after accounting for transaction costs." They report a positive net Sharpe ratio only for S&P 500 futures at a cost of 1 tick. — [Baltussen et al. 2021, p. 386](https://academicweb.nd.edu/~zda/intramom.pdf)
- Subperiod decay (Table 5, pooled βROD x100):
  - Currencies: 1.31*** in 1974–1999, falling to 0.33 (t = 1.45, not significant; R² 0.04%) in 2000–2020. βONFH for currencies also falls, from 1.79*** to 0.38 (not significant).
  - Commodities: βROD 1.59*** (R² 0.23%) in 1974–1999 and 1.04*** (R² 0.12%) in 2000–2020. — [Baltussen et al. 2021, Table 5](https://academicweb.nd.edu/~zda/intramom.pdf)
- Per-contract results, full sample, with slopes x100 and out-of-sample R² from an expanding window (Tables B3–B4):
  - **GC:** βONFH 1.43*** (R² 0.23%, R²OOS 0.18%***). βROD 1.09*** (R² 0.25%, R²OOS 0.08%**).
  - **CL:** βONFH 2.00 (not significant, R² 0.17%, R²OOS −0.48%). βROD 0.67 (not significant, R² 0.03%, R²OOS −1.04%).
  - **EC (6E):** βONFH 0.04, βROD −0.04, with negative R² and R²OOS (−0.08% / −0.07%), so no effect.
  - **JY (6J):** βONFH 0.45* (R²OOS −0.01%), βROD 0.39 (not significant, R²OOS −0.01%).
  - Pooled "Energies" βROD is 2.10** (R² 0.45%) and pooled "Metals" βROD is 1.19*** (R²OOS 0.31%). — [Baltussen et al. 2021, Appendix B](https://academicweb.nd.edu/~zda/intramom.pdf)
- Mechanism: the authors attribute the effect to gamma hedging (options market makers and leveraged-ETF rebalancing). They show the effect in natural gas, silver, gold and oil rises with LETF market share. — [Baltussen et al. 2021, Section 4](https://academicweb.nd.edu/~zda/intramom.pdf)
- Origin paper: Gao, Han, Li & Zhou (2018 JFE) on SPY, 1993–2013, with a first-half-hour to last-half-hour R² of 1.6%. Alpha Architect summarizes it. — [Alpha Architect](https://alphaarchitect.com/2014/08/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/)
- Counter-evidence for index futures: Liu & Tse (2017) find that the first half-hour return did not predict in 12 international index futures, although overnight returns did. — [IDEAS / search summary](https://ideas.repec.org/p/pra/mprapa/97134.html)

**B. Crude oil intraday momentum conditioned on EIA days (Wen, Indriawan, Lien & Xu 2023, The Energy Journal 44(5):149–172)**
- On EIA announcement days (Wednesday 10:30 ET), the third half-hour return significantly predicts the last half-hour return. On non-EIA days only the first half-hour return predicts it, and that first half-hour predictability comes mainly from its overnight component. — [IDEAS / RePEc record](https://ideas.repec.org/a/aen/journl/ej44-5-xu.html); [EconPapers](https://econpapers.repec.org/RePEc:sae:enejou:v:44:y:2023:i:5:p:149-172)
- Search-engine summaries report Sharpe ratios of 9.28 (first half-hour signal, non-announcement days) and 11.98 (overnight-component signal). I could NOT verify these figures in the paper itself; the working-paper PDF at the Adelaide repository would not render. Sharpe ratios this high for a CL timing strategy almost certainly exclude costs and should be treated as suspect. — [Adelaide repository (PDF did not render)](https://digital.library.adelaide.edu.au/dspace/bitstream/2440/141224/2/hdl_141224.pdf)
- These results conflict with Baltussen et al., who find CL's βONFH insignificant with a negative R²OOS over 1987–2020. The differences in sample, session definition and contract roll are unknown. — [Baltussen et al. 2021](https://academicweb.nd.edu/~zda/intramom.pdf)

**C. EIA inventory-report reaction in CL (Geman & Li 2018, Journal of Energy Markets 11(2):1–35)**
- Returns, volatility and volume react within minutes, and the effects last about 25 minutes. A positive (bearish) inventory surprise moves price down at once and a negative surprise moves it up. Price "reverts quickly" after the initial reaction. Higher belief dispersion produces a larger response. — [Risk.net abstract](https://www.risk.net/journal-of-energy-markets/5728636/an-analysis-of-intraday-market-response-to-crude-oil-inventory-shocks)
- Strategies tested on EIA days: (i) the "natural" strategy trades in the direction of the surprise; (ii) the alternative follows the 10:20–10:25 price move, before the release, and beats the natural one ("remarkably profitable" per the summary). The authors suggest that some participants get the news about 10 minutes early. No return magnitudes, sample period or cost treatment are visible outside the paywall. — [Risk.net](https://www.risk.net/journal-of-energy-markets/5728636/an-analysis-of-intraday-market-response-to-crude-oil-inventory-shocks)
- Note: the strategy depends on pre-release information leakage. Since about 2012–2014 the EIA has tightened its release procedures (I did not verify this here), so the 10:20–10:25 effect may have decayed. This needs a post-2018 test.
- Ye & Karali (UGA dissertation, 2016): both API (Tuesday 16:30 ET) and EIA surprises have an immediate negative effect on CL returns and raise volatility, with asymmetric instantaneous responses to EIA surprises. An EIA-hosted presentation (Yang 2017) finds no asymmetry. — [Ye dissertation, UGA](https://openscholar.uga.edu/record/7887/files/ye_shiyu_201612_phd.pdf); [EIA presentation](https://www.eia.gov/finance/markets/reports_presentations/2017/yang.pdf)
- Data constraint: the "surprise" needs consensus forecasts (for example Bloomberg or Reuters surveys), which are not in the user's bar data. A price-only proxy uses the sign of the 10:30–10:31 (or 10:30–10:35) bar return as the "surprise" direction.

**D. Gold London PM fix (Caminschi & Heaney 2014, JFM 34(11):1003–1039)**
- At the start of the PM fix, GC futures and GLD show sharply higher volume and volatility, and informed traders earn significant returns in the first 4 minutes. Trades in the opening minutes predict the fix direction, "in some cases exceeding 90%". Publication of the result has no significant price effect. — [IDEAS abstract](https://ideas.repec.org/a/wly/jfutmk/v34y2014i11p1003-1039.html)
- Caveat: the sample predates 2015, when the phone-based fix was replaced by the electronic LBMA Gold Price auction (I did not verify the date here). The leakage mechanism the paper exploits is likely gone. No net-of-cost or post-2015 numbers were found.
- Donati & Jung (CBS master's thesis): a "hat-shaped" pattern in which gold rises in Asian hours and falls in the London and New York sessions, plus declines around the London fixings in the years of alleged manipulation. Strategy Sharpe ratios reach 1.61 but are before transaction costs. The work is not peer reviewed. — [CBS thesis record](https://research.cbs.dk/en/studentProjects/gold-price-dynamics-around-the-clock/); [PDF](https://research-api.cbs.dk/ws/portalfiles/portal/59803241/651553_Thesis_Contract_13383.pdf)
- StoneX commentary (Nov 2026): since September, gold returned +2.7% in Asian hours, −2.5% in Europe and −12.2% in the US session. For 2026 as a whole the figures are Asia +3.4%, Europe −0.9% and US −28.1%. The author notes the pattern is not consistent month to month. These are short-window, unadjusted commentary figures. — [StoneX](https://www.stonex.com/en-gb/news-and-analysis/gold-outlook-asia-buys-the-dip-us-hammers-the-rip-2026-11-16/)
- Bell (MPRA WP), "Arbitrage Trading Strategy in Gold Futures": a hold-between-fixes strategy that worked in 2000–2010. It involves overnight holding, so it is EXCLUDED. — [IDEAS](https://ideas.repec.org/p/pra/mprapa/96124.html)

**E. Gold reaction to US macro releases**
- COMEX gold futures (30-second data) respond significantly in activity, returns and volatility to scheduled US releases such as CPI, GDP, unemployment, PPI and personal income (VAR-GARCH study, Curtin). — [Curtin study PDF](https://espace.curtin.edu.au/bitstream/handle/20.500.11937/28039/227202_227202.pdf?sequence=2)
- I found no study that measures post-announcement intraday DRIFT in GC (continuation after the first minutes) with trading rules or costs. — [search summary; Erasmus thesis](https://thesis.eur.nl/pub/12225/12225-Timmermans.pdf)

**F. CL settlement window (14:28–14:30 ET VWAP)**
- CL settles on the 2-minute VWAP from 14:28:00 to 14:30:00 ET. — [NexusFi settlement table](https://nexusfi.com/a/data/futures-settlement-data); [AEA 2023 paper](https://aeaweb.org/conference/2023/program/paper/FRQksbtk)
- No academic study of a tradable price pattern (pre-settlement drift or post-settlement reversal) in the CL window was found. The CFTC interim report on the April 20, 2020 negative settlement (−$37.63) is a one-off event study, not a strategy. — [CFTC interim staff report](https://cftc.gov/media/5296/InterimStaffReportNYMEX_WTICrudeOil/download)

**G. FX futures intraday momentum**
- The only positive FX evidence is Elaut, Frömmel & Lampaert (2018, Journal of Financial Markets) on RUB/USD, a market with fixed trading hours. — [EconPapers](https://econpapers.repec.org/RePEc:eee:finmar:v:37:y:2018:i:c:p:35-51)
- For US-listed 6E/6J, Baltussen et al. find nothing for EC and weak, out-of-sample-negative results for JY. Currency intraday momentum was not significant in 2000–2020 (see A).

**H. Cross-asset lead-lag**
- An arXiv preprint (stop-and-reverse MinMax method) reports lead-lags of 5–10 minutes at price extrema for index futures, FX (including yen pairs) and gold versus silver. It is not peer reviewed and has no trading costs. — [arXiv 1504.06235](https://arxiv.org/pdf/1504.06235)
- Dobrev & Schaumburg (2018): price discovery in Treasuries and equities happens mainly in futures, with cross-market activity measured at millisecond scale. This implies minute-level lead-lag between ES/ZN and GC/6J is arbitraged away at 1-minute resolution. — [Dobrev & Schaumburg PDF](https://www.atlantafed.org/-/media/documents/news/conferences/2018/1018-financial-stability-implications-of-new-technology/papers/dobrev-schaumburg_high-frequency-cross-market-trading.pdf)
- I found no peer-reviewed study showing a profitable 1-minute-bar lead-lag strategy (for example ZN to GC, or ES to 6J) net of costs.

### Inferences
- **Ranked shortlist (most to least promising for this user):**
  1. **GC market intraday momentum (rROD or rONFH sign, trade 13:00–13:30 ET).** It is the only contract-level result here with a significant out-of-sample R², and the authors give it a plausible structural driver (gamma or LETF hedging, which may have grown since GLD and GLD-option volume surged). Caveats: the gross edge is near the cost (see Q2), the per-contract R²OOS is only 0.08–0.18%, and there are no published post-2020 tests.
  2. **CL EIA-day momentum (Wen et al. 2023): the sign of the third half-hour return predicts the last half-hour, on Wednesdays only.** It is peer reviewed but its headline numbers are unverified, and it conflicts with Baltussen's insignificant CL results. Wednesdays give only about 50 trades a year, so the statistical power over 2018–2026 is low (about 400 trades).
  3. **CL EIA pre-release drift (follow the 10:20–10:25 move, exit by about 10:55) and post-release reaction or reversal (fade after roughly 25 minutes).** There is evidence of a strong price effect, but it depends on leakage and has probably decayed, with no cost numbers. Note that a post-release reversal is a short-horizon event fade. It is not generic mean reversion, but it is conceptually near the user's drift-burst fade, which the user has already tested, so if the reversal leg is tested it should be keyed strictly to the 10:30 timestamp.
  4. **GC session seasonality (short GC during the US session).** The evidence is weak (a student thesis, plus 2026 commentary that may reflect regime-specific selling). It is cheap to test (one trade a day) but at high risk of data-mining.
  5. **6E / 6J intraday momentum and lead-lag:** published evidence says no edge since 2000. Low priority.
- None of the candidates has documented post-2018 out-of-sample evidence. The user's own 2018–2026 data would itself be the out-of-sample test for papers whose samples end in 2020 or earlier.

### Gaps
- Full-text numbers for Wen et al. 2023 (EIA-day Sharpe ratios, costs, sample) and Geman & Li 2018 (strategy returns, sample period) were not accessible: one PDF would not render and the other is behind a paywall.
- No post-2018 replication was found for any of the candidates.
- No source was found on trading the CL settlement window, on the gold electronic-auction (post-2015) fix, or on GC post-macro-release drift with trading rules.
- Li, Sakkas & Urquhart (2022, JFM) on intraday time-series momentum covers 16 equity markets only, not commodities or FX. — [Reading repository](https://centaur.reading.ac.uk/95566)

## Q2. Exact rules, holding period, trades per year, reported performance, and gross edge versus cost

### Takeaway
Every shortlisted candidate holds for 5–30 minutes and trades about 50–250 times a year. The published gross per-trade edges, where they can be derived at all, are about 0.5–2 bp. That is roughly break-even in GC and well below the cost in CL, 6E and 6J. All of them must be flagged as small-edge strategies, which is the same failure mode as the user's 6E FX-fix test.

### Cited Findings
- **Market intraday momentum, commodity portfolio (gross):** 4.34%/yr from about 252 trades a year is about 1.7 bp per trade on unlevered notional for the 1/N commodity basket. The currency basket gives 0.85–0.93%/yr, about 0.35 bp per trade. The hit rate is 53–56%. No costs are included. — [Baltussen et al. 2021, Table 6](https://academicweb.nd.edu/~zda/intramom.pdf)
- Rules (Baltussen):
  - Signal: rROD, the return from the prior session's close (GC 13:30, CL 14:30, FX 14:00 ET) to 30 minutes before today's close.
  - Entry: at 13:00 ET (GC), 14:00 ET (CL) or 13:30 ET (6E/6J), long if the signal is positive and short otherwise.
  - Exit: at the close of the session or settlement (13:30 / 14:30 / 14:00 ET).
  - Holding period 30 minutes, one trade a day, about 250 trades a year. — [Baltussen et al. 2021](https://academicweb.nd.edu/~zda/intramom.pdf)
- **Wen et al. (CL, EIA days):** the signal is the 3rd half-hour return on EIA Wednesdays (or the 1st half-hour on other days), and the trade is the last half-hour, about 50 (EIA) or about 200 (non-EIA) trades a year. Performance could not be verified. — [IDEAS](https://ideas.repec.org/a/aen/journl/ej44-5-xu.html)
- **Geman & Li (CL EIA):** take the direction of the 10:20–10:25 ET move on EIA days and hold through the release. The price effects last about 25 minutes. About 50 trades a year. No magnitudes are available. — [Risk.net](https://www.risk.net/journal-of-energy-markets/5728636/an-analysis-of-intraday-market-response-to-crude-oil-inventory-shocks)
- **Caminschi & Heaney (GC PM fix):** trade in the direction of the first minutes of the 15:00 London fix and hold about 4 minutes. About 250 trades a year. Pre-2015 sample, no net numbers. — [IDEAS](https://ideas.repec.org/a/wly/jfutmk/v34y2014i11p1003-1039.html)

### Inferences
- **Rough per-trade arithmetic for GC momentum** (my own estimate, not from a paper). Take a last-half-hour return standard deviation of about 0.15% and an R² of about 0.25%, so a correlation of about 0.05. The expected sign-strategy gain is about ρ·σ·√(2/π) ≈ 0.05 x 0.15% x 0.8 ≈ 0.6 bp, about $24 per GC contract at a $400k notional, against about $25 of cost. That is break-even at best. The basket-level 1.7 bp (about $68 on GC notional) is more favorable, but the basket average includes the stronger 1974–1999 period.
- **CL:** at a $65k notional, even 2 bp is only about $13, below the $25 cost. CL momentum must therefore show a per-trade edge several times larger than the published averages, which is plausible only on EIA days, where volatility is higher.
- **6E / 6J:** about 0.35 bp on $80–144k notional is about $3–5 per trade against a $30 cost. Clearly not viable.
- **Filters that raise edge per trade** (fewer, larger-signal trades) are the main way to clear costs. Examples: trade only when |rROD| exceeds a high percentile; trade only when rONFH and rROD agree (Baltussen's combined variant had the best commodity Sharpe ratio, 1.29 vs 0.82); trade only on high-volatility or event days. Baltussen et al. report a stronger effect on days with large early moves and jumps. — [Baltussen et al. 2021](https://academicweb.nd.edu/~zda/intramom.pdf)
- **Bar mechanics:** use a single-leg entry and exit with market or limit orders at bar boundaries. Avoid multi-leg structures, which inflated costs in the user's FX-fix test to about $140.

### Gaps
- Per-contract net-of-cost results and post-2020 performance are not published for any candidate.
- The actual last-half-hour volatility of GC and CL over 2018–2026 is needed to replace my approximate σ; the user can compute it from their bars.

## Q3. What parameters would make a good ablation grid?

### Takeaway
The grid should vary the signal window, the trade window, the size and agreement filters, the event conditioning (EIA, CPI, NFP or FOMC days versus other days) and the session definition (pit-hour close versus 17:00 ET Globex close). Each cell should be judged on net-of-cost PnL per trade and on 2018–2021 versus 2022–2026 subperiod stability, because the published edges are near the cost.

### Cited Findings
- **Predictor windows tested in the literature:** rONFH (prior close to the end of the first half-hour), rM (first half-hour to the last hour), rSLH (second-to-last half-hour), rROD (prior close to 30 minutes before the close), and combined sign agreement. rROD dominates in commodities; in currencies rONFH ties or wins. — [Baltussen et al. 2021, Tables 2–6](https://academicweb.nd.edu/~zda/intramom.pdf)
- **Event conditioning:** on EIA days the 3rd half-hour (about 10:00–10:30 or 10:30–11:00, depending on the session start) becomes the predictor. The overnight component of the first half-hour return carries most of the predictive power. — [Wen et al. 2023, IDEAS](https://ideas.repec.org/a/aen/journl/ej44-5-xu.html)
- **EIA timing variables:** the pre-release window (10:20–10:25 ET), a reaction lasting about 25 minutes, belief dispersion (proxy: realized volatility before the release), and API Tuesday 16:30 ET as a second event (the trade must still close the same session). — [Geman & Li 2018](https://www.risk.net/journal-of-energy-markets/5728636/an-analysis-of-intraday-market-response-to-crude-oil-inventory-shocks); [Ye dissertation](https://openscholar.uga.edu/record/7887/files/ye_shiyu_201612_phd.pdf)
- **Conditions that strengthen intraday momentum:** low liquidity, high volatility, and discrete (scheduled) information. — [Li, Sakkas & Urquhart 2022 (equities)](https://centaur.reading.ac.uk/95566)

### Inferences
Suggested grid, all intraday and flat by the session close:
- **Intraday momentum (GC primary; CL, 6E and 6J as controls):**
  - Signal window: {rONFH, rROD, r from 08:20/09:00 to T−30, rSLH, sign agreement of rONFH and rROD}.
  - Trade window: last {15, 30, 60} minutes before the {pit close 13:30 / 14:30 / 14:00 ET, or Globex 17:00 ET}.
  - Entry: at the open of the first bar of the window (or with a 1-minute delay to test robustness).
  - Size filter: |signal| above {0, 50th, 75th, 90th} percentile of a trailing 60-day distribution, or above k x the trailing ATR, with k in {0, 0.5, 1}.
  - Volatility regime filter: trade only if first-hour realized volatility is above its trailing median.
  - Day filter: {all days, EIA Wednesdays only (CL), macro-release days (CPI, NFP, FOMC) only, non-event days only}.
  - Optional stop: {none, 1x, 2x the trade-window ATR}.
- **CL EIA event:**
  - Mode: {pre-release follow (enter 10:25, exit at 10:30, 10:35 or 10:55); post-release continuation (enter 10:31–10:35 in the direction of the first 1–5 minutes, exit at 10:45, 11:00, 11:30 or 14:30); post-release fade (enter at 10:55, exit at 11:30 or 14:30)}.
  - Threshold on the initial reaction: {0, 0.5, 1, 2} x the trailing 10:30-bar volatility.
  - Holiday-shifted release days must use the actual release timestamp from the EIA calendar.
- **GC fix / session seasonality:**
  - Fix-window follow: direction of 10:30 or 15:00 London plus {1–4} minutes, hold {4, 10, 30} minutes; London times converted to ET with DST handled.
  - US-session short: from {08:20, 09:30} ET to {13:30, 17:00} ET.
- **Evaluation:** per-trade net PnL in dollars at $25 / $30 round trip plus one extra tick of slippage as a stress test; profit factor; 2018–2021 versus 2022–2026 splits; and the number of trades per cell. Discard cells with fewer than about 150 trades, or apply multiple-testing haircuts (for example deflated Sharpe ratios).

### Gaps
- No paper reports which grid dimensions matter most out of sample for these four contracts, so the grid choices above are inferences from the equity and pooled-futures literature.

## Exclusion and overlap notes (applies across questions)
- **Market intraday momentum (last-half-hour timing) vs. the already-tested opening-range breakout / noise-band intraday momentum:** these are related but distinct. Noise-band ORB trades breakouts during the day; this strategy only times the final 30 minutes, based on the sign of the cumulative return. The user should still check correlation with the noise-band results. The signal family is the same: "intraday momentum".
- **EIA post-release fade** is close to the drift-burst fade (already tested) and to generic mean reversion. Test it only as an event-keyed fade.
- **Gold PM fix (15:00 London)** is related to the failed FX 4pm-fix reversal. The direction here is continuation (follow the opening minutes), not reversal, but the mechanism (leakage) is likely dead after 2015.
- **Bell's gold fix-to-fix strategy and Asian-hours gold long** (if held across 17:00 ET) involve overnight legs: EXCLUDED, or restrict them to within one Globex session (18:00–17:00 ET), which the user should decide.
