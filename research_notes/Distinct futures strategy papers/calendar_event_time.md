# Calendar, Seasonality and Scheduled-Event-Time Strategies for Liquid US Futures (OHLCV-only)

Scope: strategies driven by clock time or scheduled events, not price patterns, that can be built from 1-minute OHLCV on ES, NQ, RTY, YM, CL, GC, 6E, 6J, ZN (2018-01 to 2026-10). Breakouts, intraday momentum continuation and mean reversion are excluded because the user already tests them.

Shortlist (detail below):
1. Overnight drift / European-open window, with an optional "buy-the-dip" condition (Boyarchenko-Larsen-Whelan RFS 2023; Bondarenko-Muravyev JFQA 2023). Strong evidence, tested on ES futures, but the effect has DECAYED in 2021-2025.
2. Pre-FOMC announcement drift (Lucca-Moench JF 2015) and its post-2015 decay (Kurov-Wolfe-Gilbert FRL 2021).
3. FOMC-cycle even-week effect (Cieslak-Morse-Vissing-Jorgensen JF 2019).
4. Turn-of-the-month / "Dash for Cash" monthly liquidity cycle (Etula et al. RFS 2020), with mixed futures evidence.
5. Monthly-expiry effects: SOQ / "derivative payoff bias" around the 3rd-Friday AM settlement (Baltussen-Terstegge-Whelan, 2024 WP) and option-expiration-week returns (Stivers-Sun JBF 2013).
6. FX local-trading-hours depreciation (Breedon-Ranaldo JMCB 2013) for 6E/6J session handoffs.
7. Borderline or not usable: Heston-Korajczyk-Sadka intraday periodicity (cross-sectional stocks only), leveraged-ETF / market-on-close rebalancing (Cheng-Madhavan; Tuzun), end-of-day reversal (Baltussen-Da-Soebhag, cross-sectional stocks), and Gao-Han-Li-Zhou / Baltussen-Da-Lammers-Martens market intraday momentum (OVERLAPS the user's existing momentum work).

---

## Q1. Which calendar/event effects have published evidence in futures or index ETFs?

### Takeaway
The best-documented effects tested directly on futures are the ES overnight drift around the European open (2:00-3:00 ET), the pre-FOMC drift, FOMC-cycle even weeks, and the 3rd-Friday SOQ settlement reversal. Turn-of-month evidence in futures is old and mixed. FX local-hours depreciation is documented in spot FX and maps directly to 6E/6J. Two flagship effects (overnight drift, pre-FOMC drift) have published evidence of decay that falls inside the user's 2018-2026 sample.

### Cited Findings

**1. Overnight drift / European-open window (ES, also NQ, YM)**
- Citation: Boyarchenko, N., Larsen, L. S., and Whelan, P., "The Overnight Drift," *Review of Financial Studies* 36(9), 2023, pp. 3502-3547. NY Fed Staff Report 917 version: https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf ; IDEAS listing: https://ideas.repec.org/p/fip/fednsr/87539.html — [IDEAS](https://ideas.repec.org/p/fip/fednsr/87539.html)
- Core fact: a large positive return to holding E-mini S&P 500 futures between 2:00 and 3:00 a.m. ET, the European open. It averaged about 3.7% per year (1.48 bp/day), was positive in 20 of 23 years since 1998, and was significant in 17 of them — [NY Fed SR917](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf)
- Strategy definitions in the paper, all ET with returns from mid-quotes: CTC = 16:15 to 16:15; CTO = 16:15 to 9:30; OTC = 9:30 to 16:15; OD = long 2:00 to 3:00; OD+ = long 1:30 to 3:30; BtD ("buy-the-dip") = hold over the OD+ window only on days after negative end-of-day relative signed volume (RSV over the last hour, 15:15-16:15 ET) — [NY Fed SR917](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf); RSV window from [Liberty Street 2026](https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/)
- Results, 2004.1-2020.12, before costs: buy-and-hold ES has an 8.9%/yr return and Sharpe 0.42. CTO earns 4.6%/yr and OTC 4.2%/yr. OD earns 3.8%/yr with Sharpe 1.1. OD+ has Sharpe 1.3. BtD has Sharpe 1.8 and is in the market on about 50% of days — [NY Fed SR917](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf)
- After costs (paying the bid-ask from Refinitiv quotes): OD falls to Sharpe -0.5 and OD+ to 0.3, but BtD stays at Sharpe 1.1 because it trades only half the days — [NY Fed SR917](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf)
- Mechanism: dealer inventory management after end-of-day order imbalances, with a strong negative relation between closing imbalance and the drift. Scheduled macro, monetary and earnings news do NOT explain it — [NY Fed SR917](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf); [Liberty Street 2021](https://libertystreeteconomics.newyorkfed.org/2021/05/the-overnight-drift-in-us-equity-returns)
- Sub-sample: the 1998-2010 and 2011-2020 panels differ somewhat. Returns between 17:00 and 18:00 are insignificant early and significant later — [NY Fed SR917](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf)
- **DECAY:** the authors' July 2026 Liberty Street post reports that returns in the 2:00-3:00 ET window averaged close to zero in Jan 2021-Dec 2025 (1,245 trading days), against about 3.7%/yr in 1998-2020. The main driver is that the standard deviation of end-of-day RSV fell from 6.5% to 2.9%, so extreme closing-imbalance days are rarer. VIX changed little (mean 20.4 to 19.4), and the overnight volume share rose only from 15% to 16%. The post says the pattern also appeared in NQ and YM. NightShares' overnight ETFs (NSPY, NIWM), launched in June 2022, closed about 14 months later — [Liberty Street 2026](https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/)
- Companion paper: Bondarenko, O., and Muravyev, D., "Market Return Around the Clock: A Puzzle," *JFQA* 58(3), 2023, 939-967, DOI 10.1017/S0022109022000783. Using E-mini S&P 500 futures, they find that about 4 hours around the European open account for the entire average market return, with Sharpe about 1.6 that "stays high after transaction costs". The other 20 hours average about zero. The effect was stronger in the 2020 COVID crisis. VIX futures rise overnight and fall around the European open — [Cambridge abstract](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/market-return-around-the-clock-a-puzzle/089E33AC0B4D3B9A02CBA31EDF6505B3)
- Bondarenko-Muravyev use tick data for 2004-2018 and suggest buying just before the European open and exiting after it — [Alpha Architect summary via search](https://alphaarchitect.com/?p=57408)

**2. Pre-FOMC announcement drift (ES; equity index)**
- Original: Lucca, D. O., and Moench, E., "The Pre-FOMC Announcement Drift," *Journal of Finance* 70(1), 2015. NY Fed SR512: https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf. Holding the index only in the 24 hours before a scheduled FOMC announcement gives an annualized Sharpe above 1.1 — [NY Fed SR512](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf)
- Window: 2pm-to-2pm SPX log returns (2pm on the day before to 2pm on announcement day, just before the 2:15pm release used in that era), with E-mini futures data — [Boston Fed slides, Lucca](https://www.bostonfed.org/economic/conf/Macro-Finance-2012/presentations/lucca.pdf)
- Original sample: Sep 1994-Mar 2011 — [Kurov-Wolfe-Gilbert listing](https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html)
- **DECAY:** Kurov, A., Wolfe, M. H., and Gilbert, T., "The Disappearing Pre-FOMC Announcement Drift," *Finance Research Letters* 40, 2021. The drift essentially disappeared after 2015, both with and without press conferences. They test reduced uncertainty as an explanation — [IDEAS](https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html); [SSRN author page](https://papers.ssrn.com/author=3571041)
- Contested: Ben Dor and Rosa (2019) find no change after 2015 — [search summary of Kurov et al.](https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html)
- A BIS working paper puts the 1996-2011 drift at about 45 bp. After 2011 the drift shifted to the SECOND day before the announcement and shrank to about 22 bp. Over 1996-2020 it averaged about 36 bp — [BIS WP 1079](https://www.bis.org/publ/work1079.pdf)
- Related: Kurov et al. find drift before other US macro releases, starting about 30 minutes before the release time — [KSSW 2017, "Price Drift Before US Macroeconomic News"](https://www.skidmore.edu/economics/documents/KSSW2017-PriceDriftBeforeUSMacroeconomicNews.pdf)
- Post-announcement: "Relief Rallies After FOMC Announcements" (Gilbert, Kurov, Wolfe, 2019 WP) — [Skidmore PDF](https://www.skidmore.edu/economics/documents/GKW_ReliefRalliesAfterFOMCAnnouncements-July2019.pdf). I did not retrieve the rules.

**3. FOMC-cycle even weeks (equity index)**
- Cieslak, A., Morse, A., and Vissing-Jorgensen, A., "Stock Returns over the FOMC Cycle," *Journal of Finance* 74(5), 2019, 2201-2248. Since 1994 the equity premium has been earned entirely in weeks 0, 2, 4 and 6 of FOMC cycle time, where week 0 starts the day before a scheduled announcement — [SSRN](https://papers.ssrn.com/abstract=2687614); [EconPapers](https://econpapers.repec.org/RePEc:bla:jfinan:v:74:y:2019:i:5:p:2201-2248)
- Average excess returns are 0.33% to 0.60% in even weeks and -0.09% to -0.18% in odd weeks. Sample 1994-2016, Fama-French excess returns (not futures). About half of the even-week return comes from mean reversion after significant market declines. Fed funds futures volatility peaks in even weeks — [CFA Digest](https://rpc.cfainstitute.org/research/cfa-digest/2020/05/dig-v50-n5-2)

**4. Turn-of-the-month (ToM) / month-end liquidity cycle**
- Etula, E., Rinne, K., Suominen, M., and Vaittinen, L., "Dash for Cash: Monthly Market Impact of Institutional Liquidity Needs," *RFS* 33(1), 2020, 75-111. Returns are low from T-8 to T-4 ("selling pressure", T = last trading day of the month) and high over the following 7 days, as institutions raise cash for month-end payments and then reinvest — [OUP](https://academic.oup.com/rfs/article/33/1/75/5494694); [WP PDF](https://orbilu.uni.lu/bitstream/10993/21145/1/Dash4Cash.pdf)
- Futures evidence (old and mixed): Maberly and Waggoner (Atlanta Fed WP 2000-11) find ToM effects in S&P 500 futures disappear after 1990 — [Atlanta Fed](https://www.atlantafed.org/research/publications/wp/2000/11.aspx). Carchano and Pardo (2011) find the ToM effect in S&P 500 futures is the only calendar effect with persistent net profitability across subperiods (Dec 1991-Apr 2008) — [CXO summary](https://www.cxoadvisory.com/?p=17701). McConnell and Xu (FAJ 2008) use CRSP 1926-2005 plus futures 1993-2009 — [IDEAS](https://ideas.repec.org/a/taf/ufajxx/v64y2008i2p49-64.html); [Quantpedia](https://quantpedia.com/strategies/turn-of-the-month-in-equity-indexes)
- A 2025 *Finance Research Letters* paper, "The disappearing turn-of-month effect" (Han, Han and Tian), appears in citation lists. I could not read it — [search result](https://quantpedia.com/strategies/turn-of-the-month-in-equity-indexes)

**5. Monthly options/futures expiry (3rd Friday)**
- Baltussen, G., Terstegge, J., and Whelan, P., "The Derivative Payoff Bias" (WP, Sept 2024 version, AEA 2025). Using 24-hour futures trading, they find a "tent-shaped" pattern: prices rise from the 3rd-Thursday regular close, peak exactly at the Special Opening Quotation (SOQ) on 3rd-Friday morning, then reverse. The pattern appears only for AM/SOQ-settled contracts, not PM/close-settled ones. They estimate a wealth transfer of about $3.5bn per year in SPX options, and propose market-maker "charm" hedging as the mechanism — [AEA program](https://www.aeaweb.org/conference/2025/program/paper/N7rsBN2N); [AFA listing](https://afajof.org/management/viewp.php?n=98196); [Advisor Perspectives/Bloomberg coverage](https://www.advisorperspectives.com/articles/2023/09/28/sandp-500-options-quirk-mints-billions-stirring-manipulation-talk)
- Stivers, C., and Sun, L., *Journal of Banking & Finance* 37(11), 2013, 4226-4240. Weekly returns in option-expiration (OE) weeks (the week of the 3rd Friday) are high relative to other weeks for S&P 100 stocks, and the following (4th-Friday) week underperforms modestly — [IDEAS](https://ideas.repec.org/a/eee/jbfina/v37y2013i11p4226-4240.html). The S&P 500 index's OE week was relatively high in 1983-2008 but not before 1983 (CXO summary of the WP) — [CXO](https://www.cxoadvisory.com/?p=2463). A non-peer-reviewed blog test (1990 to Nov 2026) concludes OE week is "mostly a normal week" recently — [chartinglens](https://chartinglens.com/blog/options-expiration-week-stock-returns). Treat this as weak.

**6. FX local-trading-hours effect (6E, 6J)**
- Breedon, F., and Ranaldo, A., "Intraday Patterns in FX Returns and Order Flow," *Journal of Money, Credit and Banking* 45(5), 2013, 953-965 (SNB WP 2011-04). Currencies tend to depreciate during their own local trading hours, across a range of currencies and time zones. The same pattern shows up in order flow, consistent with participants being net buyers of foreign currency during their own hours — [SNB WP](https://www.snb.ch/en/mmr/papers/id/working_paper_2011_04); [EconPapers](https://econpapers.repec.org/RePEc:wly:jmoncb:v:45:y:2013:i:5:p:953-965)

**7. Borderline, overlapping or not directly applicable**
- Heston, Korajczyk and Sadka, "Intraday Patterns in the Cross-section of Stock Returns" (*JF* 2010). Splits the day into 13 half-hours and finds continuation at lags that are exact multiples of a day, lasting at least 40 days. It is CROSS-SECTIONAL stocks only — [arXiv 1005.3535](https://arxiv.org/pdf/1005.3535.pdf). A Nov 2025 follow-up, "The Intra-Day Stock Return Periodicity Puzzle" (Haendler, Heston, Korajczyk, Sadka) — [SSRN](https://papers.ssrn.com/ab_id=5749704). I found NO published test of the same-half-hour effect on commodity or index futures time series.
- Market intraday momentum: Gao, Han, Li and Zhou (*JFE* 2018), and Baltussen, Da, Lammers and Martens (*JFE* 2021, 60+ futures, distinct from the HKS seasonality). Both are first-part-of-day predicting last half-hour — [Baltussen et al. PDF](https://www3.nd.edu/~zda/intramom.pdf). **OVERLAPS the user's existing intraday-momentum/noise-band work; mention only.**
- End-of-day reversal: Baltussen, Da and Soebhag, "End-of-Day Reversal" (WP Sept 2026), sample 1993-2024. CROSS-SECTIONAL individual stocks: early-day losers rebound in the last 30 minutes. They say it is distinct from market intraday momentum. NOT applicable to single-futures OHLCV — [ND PDF](https://www3.nd.edu/~zda/EOD.pdf)
- Leveraged-ETF / MOC rebalancing: Cheng and Madhavan (2009) argue LETF rebalancing puts price pressure on end-of-day S&P 500 returns. Tuzun (FEDS 2013-48) estimates that a 1% SPX move leads to a 6.9 bp rebalancing-driven price increase in an average large-cap stock in the last hour, and notes LETFs rebalance with swaps and futures — [Fed FEDS 2013-48](https://www.federalreserve.gov/pubs/feds/2013/201348/201348pap.pdf). Barbon, Beckmeyer, Buraschi and Moerke (St. Gallen WP 2021) link LETF and option-hedging flows to end-of-day momentum and reversal — [Unisg PDF](https://www.alexandria.unisg.ch/server/api/core/bitstreams/5a99db31-0d37-4f86-9502-8cb0f3bff4fe/content). The predicted direction is momentum into the close (same sign as the day's move), so this OVERLAPS intraday momentum.

### Inferences
- The two cleanest futures-native effects (overnight drift, pre-FOMC drift) have published post-2015/2020 decay evidence. The user's 2018-2026 sample, and especially a sealed holdout in 2024-2026, will probably show weak or zero edge. That is a useful test of decay, but these are unlikely to be standalone winners.
- The 3rd-Friday SOQ "tent" is the most mechanistic (it depends on settlement design) and is least likely to have been arbitraged away by a published calendar rule. It needs only a calendar of 3rd Fridays plus exchange holidays.
- ToM, OE week and FOMC even weeks are daily-frequency effects. 1-minute data lets you refine entry and exit times (for example the close of T-4 versus the 16:00 settle), but they could be tested on daily bars too.

### Gaps
- I did not retrieve the exact clock window in Bondarenko-Muravyev, only "4 hours around European open". Their cost-adjusted Sharpe of about 1.6 conflicts in spirit with Boyarchenko et al.'s finding that OD/OD+ are unprofitable after costs. Possible reasons are different cost assumptions or quote data; I did not verify which.
- I could not read the content of the 2025 FRL "disappearing turn-of-month effect" paper.
- I did not get exact local-hours windows or magnitudes from Breedon-Ranaldo, and their sample period is not confirmed here.
- I found no paper documenting settlement-time effects in CL (14:28-14:30 ET), GC (13:29-13:30 ET) or ZN (14:59-15:00 ET) futures, and no academic test of NFP/CPI-day intraday patterns in futures beyond the pre-announcement drift work.

---

## Q2. Exact rules, sample, reported performance, costs, and post-publication decay

### Takeaway
Rules are precise for the overnight drift (ET clock windows plus an order-flow condition), pre-FOMC (2pm to 2pm), FOMC even weeks (week 0 = the day before the meeting) and Dash-for-Cash (T-8 to T-4 / T-3 to T+3). Decay evidence for 2016+ exists for pre-FOMC and the overnight drift.

### Cited Findings
- Overnight drift rules and Sharpe ratios (OD 1.1 / OD+ 1.3 / BtD 1.8 gross; -0.5 / 0.3 / 1.1 net of spread; 2004-2020; costs from Refinitiv bid-ask; the overnight spread reached the minimum tick after 2004) — [NY Fed SR917](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf)
- Overnight drift decay to about zero in 2021-2025 — [Liberty Street 2026](https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/)
- Pre-FOMC: 24h window before the announcement, Sharpe >1.1 in 1994-2011 — [SR512](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf). Gone after 2015 per [Kurov-Wolfe-Gilbert 2021](https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html). After 2011 it shifted to day -2 at about 22 bp per [BIS WP 1079](https://www.bis.org/publ/work1079.pdf)
- FOMC even weeks: weeks 0/2/4/6 (week 0 starts the day before the meeting), 1994-2016, even-week excess returns 0.33-0.60% vs odd -0.09 to -0.18% — [CFA Digest](https://rpc.cfainstitute.org/research/cfa-digest/2020/05/dig-v50-n5-2)
- Dash for Cash: weak T-8 to T-4, strong over the next 7 days — [Aalto WP](https://acris.aalto.fi/ws/portalfiles/portal/40965155/hhz054.pdf)
- SOQ tent: from the 3rd-Thursday close to the 3rd-Friday SOQ, then reversal — [AEA](https://www.aeaweb.org/conference/2025/program/paper/N7rsBN2N)

### Inferences (concrete backtest specs; ET times; the user should check DST and Globex maintenance-break handling)
- **A. Overnight drift (ES, NQ, YM, RTY):** enter at the 1-min bar at t1 and exit at t2. Grid: t1 in {01:00, 01:30, 02:00, 02:30}; t2 in {03:00, 03:30, 04:00, 09:30}. Condition options: none; prior-day RTH return < 0; prior-day last-hour (15:00-16:00) return < 0 or below the bottom-quintile threshold; last-hour volume-weighted signed return as a proxy for the paper's RSV. The proxy is my substitution, because true signed volume needs trade direction. A bar-level proxy is sum(sign(close-open) * volume) / total volume over 15:15-16:15. Expectation: the 2018-2020 in-sample period shows the effect, and 2021+ is about zero.
- **B. Pre-FOMC drift (ES/NQ/RTY/YM; also ZN, 6E, GC as cross-checks):** long from t-1 at H1 to day t at 13:55 ET (before the 14:00 statement used since 2013). Grid: start in {day-2 close, day-1 14:00, day-1 16:00 close, day t 09:30}; exit in {13:30, 13:55, 14:00}; press-conference meetings only vs all; a day -2 variant per the BIS finding.
- **C. FOMC even weeks:** long ES on days in weeks 0/2/4/6 of the cycle (day -1 = start of week 0), flat or short otherwise. Grid: week definition offset (-1/0/+1 day); long-only vs long/short; condition on a prior 5-day decline (the mean-reversion half of the effect).
- **D. Dash for Cash / ToM:** short (or flat) from the close of T-8 to the close of T-4, long from the close of T-4 to the close of T+3. Grid: entry day in {T-5, T-4, T-3, T-2}, exit day in {T+1 ... T+4}, long-only vs long/short, instrument (ES/RTY/NQ/YM, ZN as a flight-to-cash contrast).
- **E. SOQ tent (ES/NQ/RTY on quarterly and monthly 3rd Fridays):** long from the 3rd-Thursday 16:00 close to 09:30 Friday (around SOQ), then optionally short 09:30-close Friday or to Monday. Grid: entry time {Thu 15:00, 16:00, 18:00, Fri 02:00}; exit {09:25, 09:30, 09:35, 10:00}; quarterly-only vs monthly; reversal leg on/off.
- **F. OE week:** long from the Friday close before OE week to the 3rd-Friday close; optional short the following week. This is weak, and recent evidence suggests it is gone.
- **G. FX local-hours (6E, 6J):** for 6J, short JPY (long USD/JPY means SHORT the 6J future, since 6J is quoted USD per JPY) during Tokyo hours (about 19:00-03:00 ET), then reverse during US hours. For 6E, short 6E during European hours (about 02:00-11:00 ET) and long 6E during US-only hours (11:00-16:00 ET). The direction comes from Breedon-Ranaldo (a currency depreciates in its home hours). The exact windows here are my mapping, not the paper's.

### Gaps
- The cost assumptions and net Sharpe ratios for pre-FOMC, FOMC-cycle and Dash-for-Cash were not retrieved. Most are reported gross on index data.
- I did not find out-of-sample studies for FOMC even weeks after 2016.

---

## Q3. Natural ablation grids

### Takeaway
Every strategy here is described by (entry clock time, exit clock time, event-day offset, conditioning filter, instrument), so the grids are small and discrete, roughly 50-300 cells. Overfitting risk mainly comes from choosing time windows, so lock windows on 2018-2022 and test on the sealed holdout.

### Cited Findings
- The time-window sensitivity is itself documented. Extending the overnight drift window from 2:00-3:00 to 1:30-3:30 raises the gross Sharpe (1.1 to 1.3) but changes the net economics (-0.5 to 0.3). Conditioning on closing order flow (BtD) beats unconditional versions after costs — [NY Fed SR917](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf)
- The pre-FOMC drift migrated in event time from day -1 to day -2 after 2011, which argues for an event-offset dimension in the grid — [BIS WP 1079](https://www.bis.org/publ/work1079.pdf)

### Inferences
- Common axes: entry offset (±30/60 min), hold length, event-day offset (-2 to +2), long-only vs long/short, condition (none / prior-day down / prior-day last-hour down / volatility regime), and instrument set. A cost model of 1 tick per side plus commission matters most for the overnight strategies, given the bid-ask results in SR917.
- Include a "placebo calendar" test: the same rule on randomly shifted dates. A real effect should beat about 95% of shifts.

### Gaps
- No paper gives a recommended grid. The above is my design.

---

## Q4. Event calendar data needed and availability

### Takeaway
All calendars needed are free: FOMC meeting dates from the Fed, macro release dates from BLS/BEA, and expiry dates computed as 3rd Fridays adjusted for exchange holidays.

### Cited Findings
- FOMC meeting calendars, historical and current: Federal Reserve Board, https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm (historical years via https://www.federalreserve.gov/monetarypolicy/fomc_historical.htm). These are standard public pages; I did not fetch them in this session.
- BLS release schedule (CPI, NFP): https://www.bls.gov/schedule/ (not fetched in this session).
- The SOQ mechanism applies only to AM-settled contracts (the quarterly ES/NQ/RTY/YM futures and AM SPX options on 3rd Fridays) — [AEA](https://www.aeaweb.org/conference/2025/program/paper/N7rsBN2N)

### Inferences
- Unscheduled FOMC actions (for example March 2020) must be excluded. Scheduled 2018-2026 meetings come to 8 per year, about 70 events, so statistical power is low. Report bootstrap CIs.
- Statement time is 14:00 ET throughout 2018-2026. Press conferences follow every meeting from 2019 onward. This should be verified against the Fed calendar.

### Gaps
- I did not verify a machine-readable FOMC CSV source. Scraping the Fed page, or hand-entering about 70 dates, is straightforward.
