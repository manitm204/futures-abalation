# Intraday strategies for US Treasury futures (ZN, ZB) with published evidence

Cost yardstick used throughout (from the brief): 1 tick slippage plus $2.50 commission per side.
- ZN: tick = 1/64 point = $15.625. Round trip ≈ 2 × 15.625 + 5 = **$36.25**. On ~$110k notional (ZN near 110), that is **≈3.3 bp of price per round trip (≈2.3 ticks)**.
- ZB: tick = 1/32 point = $31.25. Round trip ≈ 2 × 31.25 + 5 = **$67.50**. On ~$115k notional, that is **≈5.9 bp of price per round trip (≈2.2 ticks)**.
- These conversions are my own arithmetic from contract specs, not taken from a source.

Main result: none of the candidate effects I found clearly survives this cost level as a stand-alone, intraday-only ZN/ZB trade in published work. The **month-end long** has the strongest and most durable evidence, but almost all published numbers are close-to-close (they include overnight). The intraday-only share has to be measured on the user's data. The **auction-day intraday V** is real (NY Fed) but roughly breaks even at a cost of 1 tick per round trip in an independent 2010–2026 futures test, so it loses money at the user's 2-tick cost. **Bond intraday momentum** is statistically robust, but its gross edge is about 1 bp per trade, well under the 3.3 bp round-trip cost.

---

## Q1. Which intraday effects in Treasury futures have published evidence that survives costs and holds out of sample?

### Takeaway
Month-end Treasury strength (Hartley & Schwarz) is the most robust published effect. It persists in 2010–2026 futures data and is far from the user's excluded families, but the published figures are close-to-close. The auction-day intraday V (Fleming, Liu & Nguyen; Lou, Yan & Zhang) and bond intraday momentum (Baltussen et al.) are statistically real, but their per-trade gross edges are at or below a 1–2 tick cost. Post-release drift after NFP is absent at 30-minute horizons. The post-FOMC drift in bond futures is documented, but mostly as a multi-day effect.

### Cited Findings

**A. Month-end Treasury returns (index-extension / window-dressing flows)**
- Hartley & Schwarz (Fed Board WP, 1990–2018): coupon Treasury excess returns are positive and significant only in the last few days of the month. A long held only over those days has an annualized Sharpe of about 1. The authors attribute this to demand spikes from window dressing and portfolio rebalancing, including insurer flows and index-extension demand. — [Hartley & Schwarz, EOM.pdf](https://www.kristaschwarz.com/EOM.pdf); [SSRN 3440417](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3440417)
- Futures evidence in the same paper (Table 8), long only over the last t days, in percentage points of price per month, 1990–2018:
  - 10-year futures: t=1 **0.09** (s.e. 0.01), t=2 0.14, t=3 0.17, t=5 0.22.
  - 30-year futures: t=1 **0.15** (s.e. 0.02), t=2 0.21, t=3 0.27, t=5 0.33.
  - 5-year futures: t=1 0.07.
  - Windows of t ≥ 7 days are insignificant or negative for the 10-year.
  - The paper says annualized returns on the longest futures held only over the last few days "can exceed 3 percentage points."
  - — [EOM.pdf, Table 8 and §4.2](https://www.kristaschwarz.com/EOM.pdf)
- The same paper argues that cash bid-ask costs (2–3 bp) are an order of magnitude below the effect, and that futures have lower costs still. Its cost argument is for close-to-close, multi-day holds, not intraday. — [EOM.pdf](https://www.kristaschwarz.com/EOM.pdf)
- Independent out-of-sample practitioner test on futures, June 2010 to September 2026 (ohlcv.io blog; not peer reviewed):
  - Per-day returns over the last three trade dates of each month: ZT +1.2 bp/day (t 3.9), ZF +3.8 (t 4.7), **ZN +5.2 bp/day (t 4.1)**, UB +11.3 (t 3.5). Other days were slightly negative.
  - Month-end trade (buy the last three trade dates, one round trip): ZT +3.1 bp/month (Sharpe 0.86), ZF +10.8 bp (Sharpe 1.13).
  - The author notes the three-day definition was chosen after looking at the chart. That is a researcher degree of freedom.
  - — [OHLCV, "The Treasury auction cycle, out of sample"](https://ohlcv.io/posts/treasury-auction-cycle/)
- The NY Fed (BrokerTec, 2016–2025) shows that Treasury trading concentrates at the index strike time, mainly on month-end days:
  - The Bloomberg index strike moved from 3 p.m. to 4 p.m. ET on 14 January 2021.
  - On month-end days, the 4 p.m. window held 11.6% of daily volume in 2021 and 20.4% in 2025.
  - In 2025, 3:45–4:15 p.m. carried more than a quarter of month-end volume, about half of it in 3:55–4:00 p.m.
  - The article reports volume only and has no return analysis.
  - — [Dyer, Fleming & Shachar, Liberty Street Economics, Sept 2026](https://libertystreeteconomics.newyorkfed.org/2026/09/treasury-trading-at-the-close/)

**B. Treasury auction-day intraday pattern**
- NY Fed Staff Report 1188 (Fleming, Liu & Nguyen; 33 years of intraday BrokerTec/GovPX data):
  - Yields rise in the hours before an auction and reverse afterward.
  - The pressure is driven mainly by dealer net order flow. It is stronger when dealers' risk-bearing constraints are tighter and weaker when investor demand is stronger.
  - The pressure **has not increased in recent years**, partly because non-dealers now absorb more supply.
  - The page shows no trading strategy and no basis-point magnitudes.
  - — [NY Fed SR1188](https://www.newyorkfed.org/research/staff_reports/sr1188.html)
- Fleming & Liu (2017) document the V-shaped pattern at the intraday level. — [Fleming paper, UZH seminar](https://www.phd-finance.uzh.ch/dam/jcr:ecc38075-0640-42d8-9ece-96ec2cb790f6/FS_spring18_paper_Fleming.pdf)
- Robeco (practitioner): futures prices decline by about 6 bp on average ahead of the auction and recover in the following hours. — [Robeco quant chart, 2025](https://www.robeco.com/en-int/insights/2025/03/quant-chart-us-treasuries-up-for-auction)
- Lou, Yan & Zhang (JF 2013) find a multi-day version: cheapening in the days before the auction and recovery after. The OHLCV post reports a Sharpe of 1.08 for the full sample and 1.44 for 1998–2008, using cash notes with a bill/10-year hedge. This version is multi-day and excluded by the brief. — [OHLCV](https://ohlcv.io/posts/treasury-auction-cycle/); [Sigaux 2019, AEA](https://www.aeaweb.org/conference/2019/preliminary/paper/QhNQQ2Zr)
- Out-of-sample futures test of the intraday trade, 2010–2026, 1,250 auctions. Rules: short from 150 minutes before the bidding close (P0), then long from P0 to P0 + 3 hours. Controls are same-weekday non-auction days.
  - Intraday swing against controls: ZN 7-year +3.6 bp of price (t 2.7), **ZN 10-year +4.0 bp (t 2.4)**, UB 30-year +10.7 bp (t 2.0; fails the block bootstrap).
  - Gross per auction (two legs): ZN +2.6 bp (t 1.9), UB +8.4 bp (t 1.7).
  - Costs at **1 tick per round trip** × 2 round trips: ZN 2.5 bp, UB 4.1 bp. **Net: ZN +0.1 bp; UB +4.2 bp (t 0.8)**; ZF +1.0 bp (t 1.1); ZT −0.1 bp.
  - Hedged 20-year (ZB vs ZN, 77 auctions): gap +17.7 bp (t 2.6), net +8.2 bp (t 1.2) after 9.5 bp costs. The author flags this as exploratory.
  - — [OHLCV](https://ohlcv.io/posts/treasury-auction-cycle/)
- Month-end confound: the same test finds that most of the daily auction-cycle gap disappears once month-end days are removed. For example, the ZN 7-year gap falls from +9.2 to −2.4 bp. "Every month in the sample ends within a week or so of a 2-, 5-, and 7-year auction." — [OHLCV](https://ohlcv.io/posts/treasury-auction-cycle/)

**C. Market intraday momentum in bond futures**
- Baltussen, Da, Lammers & Martens (JFE 2021). Sample: 16 developed-market bond futures, including TU/FV/TY/US/UB, 1974 to May 2020, with bond trading hours set to 08:20–15:00 ET.
  - Signal: the return up to 30 minutes before the close (rROD) predicts the last-half-hour return (rLH).
  - For 11 of 16 bond contracts, the out-of-sample R² is positive and significant.
  - TY: βROD = 2.53 (t 6.96), R² 1.06%, out-of-sample R² 0.86%. US (30-year): βROD = 2.11 (t 3.85), out-of-sample R² 0.22%.
  - Pooled bond results hold in both 1974–1999 (βROD 3.19, t 8.38) and 2000–2020 (βROD 1.53, t 3.61). The 2000–2020 coefficient is about half the early-period value.
  - — [Baltussen et al., working-paper PDF](https://twoquants.com/wp-content/uploads/2021/02/2020_Baltussen_LAmmers_Martens_Intra-day-Momentum.pdf); [SSRN 3760365](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3760365)
- Timing strategy for an equal-weight bond portfolio: long the last 30 minutes if rROD > 0, else short.
  - **2.16% per year gross**, volatility 1.33%, Sharpe 1.62, hit rate 0.55.
  - Using the first-half-hour signal instead: 1.08% per year, Sharpe 0.81.
  - The authors state that **transaction costs are not considered** and that the strategy "might not be exploitable … after accounting for transaction costs."
  - In bond futures, the gamma-hedging variable has the wrong sign. The hedging-demand explanation does not carry over to bonds.
  - — [Baltussen et al., Table 6 and §3.5](https://twoquants.com/wp-content/uploads/2021/02/2020_Baltussen_LAmmers_Martens_Intra-day-Momentum.pdf)
- A separate "Bond intraday momentum" study (Finance Research Letters, around 2021) uses **Chinese** Treasury futures. Its first-15-minute and first-half-hour signals predict the last period, with in-sample and out-of-sample tests. It is not US evidence. — [ScienceDirect S2214635021000599](https://www.sciencedirect.com/science/article/abs/pii/S2214635021000599)

**D. Macro-announcement reactions (NFP, CPI, ISM)**
- Kurov, Sancetta, Strasser & Wolfe (JFQA, online 2018). Data: second-by-second E-mini and 10-year T-note futures, January 2008 to March 2014.
  - Prices begin drifting about 30 minutes **before** release, in the direction of the coming surprise.
  - That drift is about 40% of the total price adjustment (around half in earlier drafts).
  - 9 of 20 market-moving announcements show it.
  - — [ECB WP 1901](https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1901.en.pdf); [JFQA](https://cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/price-drift-before-us-macroeconomic-news-private-information-about-public-announcements/E1AE41FB94D4F2CA5134410D5C82A0E2)
- A GWU seminar paper (Vega et al.) finds **no post-announcement drift** for nonfarm payroll announcements in Treasury note futures, measured from one second before release to 30 minutes after. — [GWU paper](https://business.gwu.edu/sites/g/files/zaxdzs5326/files/GWSB%20Finance%20Department%20Seminar%20Series%20-%20Clara%20Vega%20paper.pdf)
- Another pre-announcement paper reports that average post-announcement returns for NFP, ISM and GDP are small and insignificant. — [SAIF/SJTU PreAnn paper](https://en.saif.sjtu.edu.cn/junpan/PreAnn_20210728.pdf)
- Bollerslev, Cai & Song (2000) find that scheduled announcements are a major source of intraday volatility in T-bond futures (5-minute data, 1994–1997). This is a volatility result, not a return result. — [JEF 2000](http://w.long-memory.com/volatility/BollerslevCaiSong2000.pdf)

**E. FOMC days**
- Indriawan, Jiao & Tse (J. Banking & Finance 2021). Data: transaction-level US and German long-term bond futures, post-crisis.
  - FOMC-day intraday returns are significant, and there is a sizable **post-announcement drift**.
  - The strategy goes long after expansionary surprises and short after contractionary ones. Its Sharpe is up to 4× that of buy-and-hold.
  - The drift lasts **about 15 days**, so it is mostly multi-day.
  - They find no pre-FOMC drift in bond futures.
  - — [IDEAS/RePEc](https://ideas.repec.org:443/a/eee/jbfina/v123y2021ics0378426620302880.html); [ScienceDirect abstract](https://www.sciencedirect.com/science/article/abs/pii/S0378426620302880)
- Brooks, Katz & Lustig (NBER w25127) document post-FOMC drift in long-term yields over days to weeks, which is multi-day. — [NBER w25127](https://www.nber.org/papers/w25127)
- The "FOMC Announcement Reversal" paper (April 2011 to January 2020) finds a reversal of the pre-announcement move from 10 minutes before to 20 minutes after in **E-mini** futures. It also reports drift in government bond futures. — [ResearchGate](https://www.researchgate.net/publication/362775066_The_FOMC_Announcement_Reversal)

**F. Equity–bond intraday lead-lag**
- My searches found only equity cash-versus-futures lead-lag studies, with a lead of about 0–5 minutes and sometimes 20–45 minutes depending on method. None covered Treasury futures. — [Reading/centaur lead-lag strategy paper](https://centaur.reading.ac.uk/35962/1/35962.pdf); [Tilburg](https://research.tilburguniversity.edu/files/526098/108.pdf)

### Inferences
- **Month-end** is the best-supported and most persistent effect. It held in 1990–2018 (Hartley & Schwarz) and again in 2010–2026 futures (OHLCV, ZN +5.2 bp/day over the last three days).
  - A plausible intraday-only version: long ZN/ZB from the day-session open to the 16:00 ET strike (or the 15:00 ET settlement before 14 January 2021) on the last 1–3 trading days.
  - With only 12–36 trades a year, per-trade gross needs to be at least 5 bp to clear 3.3 bp of cost.
  - If the overnight share of the effect is large, the intraday-only version may fail.
  - It is distinct from every excluded family.
- **Auction intraday V**: the ZN gross of about 2.6 bp against 3.3 bp of costs for two legs at the user's cost level means it is **expected to lose**.
  - Only UB/ZB looks potentially positive (UB +8.4 bp gross; ZB-vs-ZN hedged, 20-year auction +17.7 bp gross), with weak t-stats.
  - Trading only one leg (the post-P0 long) halves the costs. Still worth an ablation.
- **Bond intraday momentum**: 2.16% a year over about 250 trades is about **0.9 bp per trade gross**, under 1 tick, against a 3.3 bp cost. It is **too small**, and the coefficient roughly halved after 2000. The family also overlaps the excluded "noise-band intraday momentum" family. **Flag: likely redundant with an already-tested family, and the edge is too small.**
- **Macro releases**: no published post-release drift in T-note futures at minute horizons. The documented drift happens before release, and its direction requires knowing the surprise, so it is not tradable from bars alone. A reaction-continuation rule after 08:30 would be exploratory, not literature-backed.
- **FOMC**: a testable intraday slice is "trade the sign of the ZN move from 14:00 to 14:00+k (or through the 14:30 press conference) and hold to the session close." The published effect is mainly multi-day, so the intraday portion's size is unknown. About 8 events a year means very low statistical power.

### Gaps
- No paper reports **intraday-only** (open-to-close on the same day) month-end returns for ZN/ZB, or how the effect splits between overnight and RTH. This needs to be measured.
- I found no bp magnitudes in NY Fed SR1188 itself; only the summary page was accessible.
- I found no US paper on intraday lead-lag between equity futures and Treasury futures, and no study of time-of-day **return** seasonality (08:30 window, 15:00 settlement, 16:00 strike) for ZN/ZB. The NY Fed note covers volume only.
- The OHLCV post is a single practitioner blog of unknown authorship and unclear peer review. Its figures are detailed and internally consistent but unverified.
- I could not access the full text of Indriawan, Jiao & Tse (403 error), so its FOMC-day intraday bp figures are missing.
- I found no published failed replication of Hartley & Schwarz, but also no post-2018 peer-reviewed update. The OHLCV test is the only post-2018 evidence.

---

## Q2. Exact rules, holding period, trades/year, reported performance, sample, costs, OOS

### Takeaway
Concrete rules are available for four candidates: month-end long, auction intraday V, bond intraday momentum, and FOMC continuation. Only the first two have futures-specific, post-2010 evidence with costs, and both sit near the cost threshold.

### Cited Findings
- **Month-end long (Hartley & Schwarz):**
  - Rule: long Treasury futures over the last t trading days of the month, with t = 1–5.
  - Holding period: close-to-close, so it includes overnight.
  - Trades per year: 12.
  - Performance: 10-year futures earn 9 bp (t=1) to 22 bp (t=5) of price per month. 30-year futures earn 15–33 bp. Sharpe is about 1. Sample 1990–2018. The paper discusses costs qualitatively.
  - — [EOM.pdf Table 8](https://www.kristaschwarz.com/EOM.pdf)
  - OOS 2010–2026: ZN +5.2 bp/day over the last three days, ZF Sharpe 1.13 for the three-day trade. — [OHLCV](https://ohlcv.io/posts/treasury-auction-cycle/)
- **Auction intraday V:**
  - Rule: short at P0 − 150 minutes, cover and go long at P0 (the 13:00 ET bidding close for most coupon auctions), exit at P0 + 3 hours.
  - Trades: roughly 75 auctions a year across maturities. For ZN-mapped auctions (3-, 7- and 10-year, each monthly), roughly 30–36 a year. That count is my estimate from the auction calendar.
  - Performance 2010–2026: ZN gross +2.6 bp, net +0.1 bp at 1 tick per round trip. UB net +4.2 bp (t 0.8).
  - Exclusions used: other coupon auctions, FOMC days, early closes. Removing 11:30 auctions and FOMC days changed the swings by at most 0.7 bp.
  - — [OHLCV](https://ohlcv.io/posts/treasury-auction-cycle/)
- **Bond intraday momentum (Baltussen et al.):**
  - Rule: sign of the return from the prior close (or the 08:20 open) to 14:30 ET decides long or short for 14:30–15:00 ET.
  - Trades: about 250 a year.
  - Performance: bond portfolio 2.16% a year gross, Sharpe 1.62, 1974–2020. No costs.
  - — [Baltussen et al.](https://twoquants.com/wp-content/uploads/2021/02/2020_Baltussen_LAmmers_Martens_Intra-day-Momentum.pdf)
- **FOMC post-announcement drift:**
  - Rule: long after expansionary surprises, short after contractionary ones.
  - Performance: Sharpe up to 4× buy-and-hold. The drift lasts about 15 days. Post-crisis sample.
  - — [Indriawan, Jiao & Tse 2021](https://ideas.repec.org:443/a/eee/jbfina/v123y2021ics0378426620302880.html)

### Inferences
- **Per-trade gross versus the ZN round-trip cost of about 3.3 bp:**
  - Bond intraday momentum, about 0.9 bp: **fails.**
  - Auction V on ZN, about 2.6 bp over two legs (cost about 6.6 bp at the user's level): **fails.**
  - Auction long leg only on ZN, roughly half of 4 bp: **fails or marginal.**
  - Month-end last day, about 9 bp close-to-close (1990–2018) or about 5 bp/day (2010–2026): **passes only if most of it accrues during the session.**
  - UB/ZB auction, about 8 bp gross versus 2 × 5.9 bp of ZB costs: **marginal or fails.**
- On costs, ZB scales in about the same proportion as ZN: roughly 2.2 ticks per round trip either way. The larger bp moves in ZB do not change the ratio much.

### Gaps
- Exact P0 times differ: 11:30 ET for some auctions (for example 20-year/TIPS reopenings and Tuesday 7-year auctions in some periods), 13:00 ET for most coupons. The user needs the Treasury auction calendar (TreasuryDirect) to map each auction to ZN or ZB.
- No per-contract annual strategy returns for TY or US alone are reported in Baltussen et al.; only regressions and a pooled portfolio.

---

## Q3. Which parameters make a good ablation grid?

### Takeaway
The grid should be organised around **calendar anchors** (month-end day, auction P0, FOMC 14:00, 08:30 releases) and **intraday entry/exit clock times**. Cost is a first-class axis, and the overnight portion must be excluded explicitly.

### Cited Findings
- Month-end parameters the literature varies:
  - Number of days t = 1–10. The effect peaks around t = 3–5 and disappears at t ≥ 7.
  - Maturity: 5-, 10- and 30-year.
  - Two-day versus three-day definition. The two-day ZF gap is only +2.8 bp (t 0.7), so results are sensitive to the definition.
  - — [EOM.pdf](https://www.kristaschwarz.com/EOM.pdf); [OHLCV](https://ohlcv.io/posts/treasury-auction-cycle/)
- Index strike-time regime change: 15:00 ET before, and 16:00 ET from, 14 January 2021. Month-end volume at the strike roughly doubled between 2021 and 2025. — [Liberty Street 2026](https://libertystreeteconomics.newyorkfed.org/2026/09/treasury-trading-at-the-close/)
- Auction parameters tested by OHLCV:
  - Pre-window length (150 minutes).
  - Post-window (first 5 minutes versus the remainder up to 3 hours).
  - Maturity-to-futures mapping and hedged versus unhedged.
  - Excluding FOMC days and month-end days.
  - Placebo shift of 10 days. All placebos fell within 1.7 SE of zero.
  - — [OHLCV](https://ohlcv.io/posts/treasury-auction-cycle/)
- Intraday momentum parameters: the signal window (first half-hour versus rest of day), the last-period length, and a both-signals-agree filter. The agree filter improved the bond Sharpe from 0.81 to 1.42. — [Baltussen et al.](https://twoquants.com/wp-content/uploads/2021/02/2020_Baltussen_LAmmers_Martens_Intra-day-Momentum.pdf)

### Inferences (suggested grid)
1. **Month-end intraday long (top priority)**
   - Instrument: {ZN, ZB}.
   - Days before month-end: {last 1, 2, 3 trading days}. Index-calendar month-end versus calendar month-end.
   - Entry: {08:20, 09:30, 12:00, 14:00 ET}.
   - Exit: {15:00 settlement, 15:55, 16:00, 16:05 ET}.
   - Regime split at 14 January 2021: 15:00 versus 16:00 exit.
   - Filters: {skip if auction day, skip if FOMC/NFP day}.
   - Variant: fade after the strike (short 16:00–16:30 ET), since that is when the flow pressure ends. This is exploratory and has no published evidence.
2. **Auction-day intraday**
   - Leg: {long leg only, short leg only, both}.
   - Pre-window: {60, 120, 150, 180 minutes before P0}.
   - Post-window: {30, 60, 120, 180 minutes, or to the session close}.
   - Auctions: {all coupons, 10-year only, 30-year/20-year only (ZB), 3/10/30 refunding only}.
   - Instrument mapping: {ZN, ZB}.
   - Exclusions: {month-end week, FOMC days}.
   - Condition on the pre-auction drawdown size (only take the long if the pre-window move ≤ −x bp).
3. **FOMC continuation (exploratory, about 8 events a year)**
   - Signal window after 14:00: {5, 15, 30 minutes, through the end of the 14:30 press conference}.
   - Threshold: |move| > {0, 0.5, 1} × the 20-day ATR.
   - Exit: {15:00, 16:00, 17:00 ET}.
   - Instrument: {ZN, ZB}.
   - Statistical power is very low, so treat any result cautiously.
4. **Post-08:30 release continuation or fade (no literature support; include only as a control)**
   - Releases: {NFP, CPI, ISM 10:00}.
   - Signal: {1, 5, 15 minutes after release}.
   - Direction: {momentum, fade}.
   - Hold: {30 minutes, 60 minutes, to 15:00}.
5. **Last-half-hour bond momentum**: deprioritise. Its edge of about 0.9 bp is far below the 3.3 bp cost, and it overlaps the already-tested intraday-momentum family.
6. **Global axes**:
   - Cost multiplier {0, 1, 2 ticks per round trip + $5}.
   - Subsamples: 2018–2021 versus 2022–2026, the hiking regime.
   - Hold out the most recent 2 years.

### Gaps
- The user's bar data must cover ZN and ZB trading up to at least 16:05 ET for the post-2021 month-end strike tests. If the user's "day session" ends at the 15:00 ET settlement, the 16:00 strike flows fall outside the session.
- No source gives the expected parameter sensitivity of the intraday-only month-end effect. That is exactly what the ablation would establish.
