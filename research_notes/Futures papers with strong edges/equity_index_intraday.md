# Intraday strategies for US equity-index futures (ES, NQ, RTY, YM) with published evidence

Scope: strategies that can be computed from 1-minute OHLCV bars (plus a public event calendar), are flat by the close, and are not in the families already tested (ORB/noise-band, z-score/Bollinger mean reversion, RSI, squeezes, MA cross, Donchian, convexity fade, EMRT pairs, FX-fix, drift-burst fade).

Cost benchmark used below: about 1 tick plus $2.50 per side, so an ES round trip is about $30, or about 0.6 index points. With ES at 5,000 to 6,000 that is about **1.0 to 1.2 bps per round trip**. Any edge under about 2 bps gross per trade is marginal.

Research budget note: roughly 20 tool calls. The core paper (Baltussen et al. 2021) was read in full. The other papers were read only through abstracts or secondary summaries, and this is flagged wherever it applies.

---

## Q1. Which intraday effects have evidence that survives costs, holds after publication and has been replicated?

### Takeaway
The only family with heavyweight, multi-market, peer-reviewed evidence is **market intraday momentum**: the day's return so far predicts the return over the last 30 minutes. The papers are Gao-Han-Li-Zhou (JFE 2018) and Baltussen-Da-Lammers-Martens (JFE 2021). However, independent replications show the **unconditional** effect in the S&P 500 has been **flat since about 2013** and flat in the 0DTE era from 2022 to 2026. What survives is **conditional**: it appears only on short-gamma or high-volatility days. The user cannot observe gamma directly, so a volatility or move-size proxy is needed. The other candidates either have thin or conflicting evidence (FOMC-day reversal, turn of month), no direct evidence on index futures (opex days, Treasury-to-ES lead-lag), or need data the user does not have (MOC imbalances, dealer gamma).

### Cited Findings

**A. Market intraday momentum, last half hour (top candidate, but decayed)**
- Gao, Han, Li & Zhou, "Market Intraday Momentum" (JFE 2018). On SPY from 1993 to 2013, the first half-hour return (measured from the **previous close** to 10:00) predicts the last half-hour return (15:30 to 16:00). The out-of-sample R² is about 1.2% to 1.6%. The paper says futures data gives similar results. — [SSRN PDF mirror](https://www.smallake.kr/wp-content/uploads/2015/01/SSRN-id2440866.pdf); [search summary of paper](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf)
- Gao et al. report the effect is stronger on high-volume, high-volatility and macro-news days. They say transaction costs reduce the average return by "only 1.22% to 4.30%" (annualized). — [search summary citing SSRN 2440866](https://www.smallake.kr/wp-content/uploads/2015/01/SSRN-id2440866.pdf)
- **Note on the signal:** Gao's first-half-hour return includes the **overnight gap**. That gap is only a signal computed from bars, so the position is still intraday-only, but it needs the prior RTH close.
- Baltussen, Da, Lammers & Martens, "Hedging Demand and Market Intraday Momentum" (JFE 142, 2021, pp. 377–403). The data cover 60+ futures from Dec 1974 to May 2020, including 17 equity index futures (6 North American). The best predictor is the **rest-of-day return, rROD**: from the prior close to 30 minutes before the close (overnight + first half hour + midday + second-to-last half hour). It predicts the last 30 minutes, rLH. The predictability reverses over the next days. — [paper PDF](https://academicweb.nd.edu/~zda/intramom.pdf)
- Baltussen Table 6, equity index futures as a 1/N portfolio from 1974 to 2020, **gross of costs**:

  | Rule | Ann. return | Sharpe | Hit rate |
  |---|---|---|---|
  | η(rROD) | 6.86% (vol 3.96%) | 1.73 | 0.55 |
  | η(rONFH), first-half-hour signal | 4.21% | 1.07 | 0.55 |
  | Both signals agree, else flat | 5.47% | 1.60 | 0.61 |
  | Always long last half hour | 0.44% | 0.11 | 0.53 |

  — [paper PDF](https://academicweb.nd.edu/~zda/intramom.pdf)
- Baltussen et al. state they "do not consider transaction costs." Their only cost statement is that the S&P 500 futures version "yields a positive net Sharpe ratio when we assume transaction cost equal to a tick." — [paper PDF](https://academicweb.nd.edu/~zda/intramom.pdf)
- Baltussen et al. split the regressions into 1974–1999 and 2000–2020. The rROD slope for equities is 5.96 (t 4.80) in the first half and 3.98 (t 6.65) in the second. — [paper PDF](https://academicweb.nd.edu/~zda/intramom.pdf)
- **Gamma conditioning:** the momentum is much stronger on days with negative net gamma exposure (NGE) and absent on positive-NGE days. NGE comes from S&P 500 options open interest (OptionMetrics, with SqueezeMetrics from 2018). From 1996 to May 2020 there were 2,930 negative-NGE days and 3,158 positive ones. — [paper PDF](https://academicweb.nd.edu/~zda/intramom.pdf); [Alpha Architect summary](https://alphaarchitect.com/hot-topic-does-gamma-hedging-actually-affect-stock-prices/)
- Leveraged-ETF rebalancing is a second channel in the same mechanism. LETFs must rebalance near the close in the direction of the day's move. Beckmeyer et al. find that higher LETF rebalancing flows raise end-of-day returns. — [Beckmeyer et al. (FMA Derivatives 2021)](https://fmai.memberclicks.net/assets/docs/Derivatives2021/beckmeyer_etf_options.pdf); [NFA listing](https://portal.northernfinanceassociation.org/viewp.php?n=2240036708). Earlier work (Trainor 2010) found no confirming evidence that LETF rebalancing causes extra end-of-day momentum. — [Do Leveraged ETFs Increase Volatility](https://www.scirp.org/html/8-9900042_2498.htm)
- **Replication failure 1 (decay):** an independent replication on SPY 1-minute bars from Aug 2000 to Dec 2019 (4,785 sessions) used the Gao signal (prior close to 10:00, predicting 15:30 to 16:00). Results by period:

  | Period | Slope | t-stat |
  |---|---|---|
  | Full sample | 0.060 | 3.30 (R² 1.39%) |
  | 2000–2007 | 0.053 | 3.31 |
  | 2008–2012 | 0.091 | 2.64 |
  | **2013–2019** | **0.003** | **0.20** |

  Yearly slopes were zero or negative in **every year from 2015 to 2019**. The mean absolute last-half-hour return is about 20 bps, and the predictable part is small compared with costs. This is a blog source, in-sample, not peer reviewed. — [Temperance Capital replication](https://temperancecapital.substack.com/p/market-intraday-momentum-replicates)
- **Replication failure 2 (0DTE era):** 1,085 SPX sessions from 2022-04-14 to 2026-08-20, regressing the last 30 minutes on rROD (open to 15:30). Slope +0.006 ± 0.009 (t +0.6). By year:

  | Year | Slope | t |
  |---|---|---|
  | 2022 | +0.009 | +0.4 |
  | 2023 | +0.002 | +0.1 |
  | 2024 | −0.016 | −0.7 |
  | 2025 | +0.016 | +1.0 |
  | 2026 | −0.012 | −0.6 |

  The author's summary: "flat in every single year." On days when dealers were short gamma per the vendor's own tape-signed 0DTE book (about 15% of sessions), the slope was +0.055 (t +3.1), with the sign positive in all 5 years. A public open-interest gamma proxy showed **no** effect. The author is a commercial data vendor with an interest in the result and calls the finding "not worth a position." — [FirmTape / DEV Community](https://dev.to/firmtape/intraday-momentum-is-dead-in-the-0dte-era-we-measured-it-on-1085-spx-sessions-43g0)
- Rosa (2022, Journal of Futures Markets), "Understanding intraday momentum strategies," analyzes data after publication. A summary says the overnight-to-last-half-hour predictability **disappears out of sample**, and a Markov-switching model suggests predictability depends on signal strength. Only the abstract or summary was seen. — [Wiley](https://onlinelibrary.wiley.com/doi/10.1002/fut.22375?af=R); [ResearchGate](https://www.researchgate.net/publication/363384228_Understanding_intraday_momentum_strategies)
- A Finnish (Aalto) thesis on futures from Jan 2008 to Oct 2024 reports intraday momentum "still exist[s]." Most of the last-half-hour predictability comes from the **last 10 minutes**, which it links to option-writer and LETF hedging. Only a search snippet was seen. — [Aalto thesis](https://aaltodoc.aalto.fi/items/1011f043-edd1-4cb2-9694-b1216d77561f)
- International evidence: the first half hour predicts the last half hour in 12 of 16 markets, with out-of-sample power in most of them (Li et al.). — [Intraday Time Series Momentum: International Evidence](https://centaur.reading.ac.uk/95566/1/Accepted-Version.pdf)
- Practitioner variant (Zarattini, Aziz & Barbon 2024, "Beat the Market," SPY): Sharpe 1.33, 19.6% a year net, 2007 to early 2024. **This is the noise-area breakout the user has already tested, so it is excluded.** — [SFI WP 24-97](https://www.sfi.ch/fr/publications/n-24-97-beat-the-market-an-effective-intraday-momentum-strategy-for-s-p500-etf-spy); [Concretum](https://concretumgroup.com/beat-the-market-an-effective-intraday-momentum-strategy-for-sp500-etf-spy/)

**B. FOMC announcement-day reversal (intraday part only)**
- Baglioni & Ribeiro, "The FOMC Announcement Reversal" (SSRN 4182628; drafts from Aug 2022 to Feb 2025). Rule: at 13:50 ET on scheduled FOMC days, buy ES if the prior **24-hour** return is negative and sell if it is positive, then exit at the end of the trading day. Sample: Oct 1997 to Jan 2020, 180 announcements. Result: **+0.18% net per announcement** (trades filled at bid/ask), **Sharpe 0.36** on their per-day definition. Sub-periods (1997–2011 and 2011–2020) and VIX interactions were tested, but the numbers sit behind a paywall. — [CXO Advisory](https://cxoadvisory.com/calendar-effects/stock-market-return-reversal-after-fomc-announcements); [CXO summary 2](https://www.cxoadvisory.com/?p=43272); [Papers With Backtest](https://paperswithbacktest.com/strategies/the-fomc-announcement-reversal)
- The signal window (prior 24 hours) spans the previous afternoon and overnight, but it is only a **signal**. The position is held from 13:50 to the close, so it meets the no-overnight rule. It is **not** the pre-FOMC drift trade, which the user excluded.
- A related paper (Martineau abstract) finds a reversal of about 60 bps in ES, from 30 minutes before FOMC to the next-day settlement. That holding period goes overnight, so it is not directly usable. — [Martineau abstract](https://ies.keio.ac.jp/upload/20190716macro_Martineau_abstract-1.pdf)
- Lucca & Moench: the post-announcement equity return is close to zero on average. The well-known drift is **before** the announcement and held from the prior afternoon, so it is excluded. — [NY Fed SR 512](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.html)
- A Fed note shows volatility spikes right after 14:00 and again just after 14:30, when the press conference starts. — [FEDS 2026-023](https://www.federalreserve.gov/econres/feds/files/2026023pap.pdf)

**C. Turn of the month (calendar effect, traded in RTH only)**
- Conflicting evidence. A Fed working paper finds turn-of-month effects in S&P 500 futures **disappear after 1990**. — [Fed (fedinprint)](https://www.fedinprint.org/item/fedawp/13394/original)
- CXO's futures calendar study says the "+1" effect (close of the last trading day of the month to the close of the next day) is the only calendar effect with persistent net profitability, and that profit sits mainly in the **next-day session rather than overnight**. — [CXO Stock Index Futures Calendar Effects](https://www.cxoadvisory.com/calendar-effects/stock-index-futures-calendar-effects/)
- A practitioner test on SPY from 2006 to 2026 found the turn-of-month window beat 79% of random windows after costs. The author warns that the window was chosen after seeing the data. — [Quanterlab](https://quanterlab.com/research/in-search-of-the-market-s-payday)

**D. Options-expiration and quad-witching days**
- No study was found that isolates **intraday ES returns** on monthly opex or quad-witching days. The related work covers volatility or needs options data. One example: positive dealer gamma in SPX 0DTE options comes before lower volatility and more reversals, and negative gamma comes with momentum. — [Adams et al., 0DTE](https://www.jean-sebastienfontaine.com/papers/0dte-options-volatility.pdf)

**E. Cross-market lead-lag (ZN leading ES, futures leading cash)**
- Pan et al. (2025), using 5-minute bars: 10-year Treasury futures returns positively predict subsequent ES returns. No trading or cost results were seen. — [Stock-Bond Correlation, SAIF 2025](https://en.saif.sjtu.edu.cn/junpan/Correlation_2025.pdf)
- Classic evidence that futures lead the cash index (Hasbrouck 2003 and others) is about price discovery, not a tradeable futures-on-futures edge. — [PMC review](https://pmc.ncbi.nlm.nih.gov/articles/PMC9107071)

**F. MOC / closing-auction imbalance**
- This needs imbalance feeds the user does not have. It reaches ES only through the same end-of-day hedging and LETF channel as section A. No bar-only evidence was found.

### Inferences
- **Per-trade edge versus cost:**
  - Baltussen's equity η(rROD) earns 6.86% a year over about 252 trades, about **2.7 bps per trade gross**. That is roughly 2.3x the 1.0–1.2 bps ES round-trip cost, so net per trade is about 1.5 bps, or **about 0.8–0.9 ES points on a 6.86% gross basis before decay**. This is a 1974–2020 average across 17 equity futures, not ES-only after 2013.
  - In ES since 2013, replications show a slope of about 0, which implies **no net edge unconditionally**.
  - It only becomes viable if a filter concentrates the trades on days where the signal is strong.
- **FOMC reversal:** +18 bps net per trade is large against costs (about 10–11 ES points gross on a 5,500 index). But there are only **8 trades a year**, the Sharpe is 0.36, and the sample is 180 events. It is statistically fragile; the 2020–2026 period is truly out of sample and worth testing.
- **Gamma proxy without options data:** the gamma-conditional result cannot be replicated directly. Bar-only proxies are guesses that need testing: a large |rROD| relative to trailing ATR (dealers drift short gamma after big moves), high realized volatility in the prior N days, or down days (puts dominate, so dealers are short gamma on selloffs). Gao et al. say the effect is stronger on high-volatility and high-volume days, which supports a volume or volatility filter.
- **Lead-lag:** with 1-minute bars and a 0.6-point cost, any lead-lag edge at 1–5 minute horizons is almost certainly smaller than costs. Treat it as a filter (for example, require ZN to agree) rather than a standalone strategy.
- **Turn of month:** a version that is long ES from the RTH open to the RTH close on day +1 (and possibly −1 to +3) fits the constraints. It is low frequency (12–48 trades a year) and the evidence conflicts.
- **Overlap with excluded families:** last-half-hour momentum is a fixed-time timing rule, not a breakout. It differs from the noise-band ORB in mechanism (a 15:30 entry on the sign of rROD). It does share the "trade intraday trend" exposure, so expect correlation with the noise-band results the user already has.

### Gaps
- ES-only (not 1/N) Sharpe, and net-of-one-tick numbers from Baltussen et al., were not extracted. The text says only that the net Sharpe is "positive."
- Gao et al.'s exact market-timing annual return and Sharpe could not be verified from a primary source in this session.
- The Rosa (2022) full results and the Baglioni & Ribeiro sub-period and VIX-conditional numbers sit behind paywalls or 403 errors.
- No peer-reviewed post-2020 ES-specific replication of last-half-hour momentum was found. The decay evidence comes from blogs and vendors.
- No primary evidence was found for intraday NQ, RTY or YM separately, for CPI or NFP intraday drift in ES, or for opex-day intraday ES patterns.

---

## Q2. Exact rules, holding period, trades per year, reported performance, costs, out-of-sample status

### Takeaway
The testable rules are listed below. Only S1 and S3 have primary-source rules and performance numbers. S2 is a variant suggested by the gamma evidence. S4 and S5 are lower-confidence fillers.

### Cited Findings

**S1. Last-half-hour momentum (Baltussen η(rROD)).** Source: [Baltussen et al. 2021](https://academicweb.nd.edu/~zda/intramom.pdf)
- Signal: rROD = log(P[close − 30 min] / P[prior RTH close]). For ES, the close is 16:00 ET for cash and the RTH settlement window is about 16:00.
- Entry: at 15:30 ET, long if rROD > 0, short otherwise.
- Exit: at the close, 16:00 ET. The paper finds the predictability ends at the cash close.
- Holding: 30 minutes. Trades: about 250 a year.
- Performance: equity 1/N SR 1.73 and 6.86% a year gross (1974–2020); positive net Sharpe at 1 tick in ES.
- Out of sample after 2013: fails unconditionally ([Temperance](https://temperancecapital.substack.com/p/market-intraday-momentum-replicates); [FirmTape](https://dev.to/firmtape/intraday-momentum-is-dead-in-the-0dte-era-we-measured-it-on-1085-spx-sessions-43g0)).
- Variant (Gao): signal = previous close to 10:00 ET.
- Variant (agreement filter): trade only when the first-half-hour and rROD signs agree. Gross SR 1.60, hit rate 61%, fewer trades.

**S2. Conditional last-half-hour momentum (the gamma or volatility filter).** Source: same as S1, plus [FirmTape](https://dev.to/firmtape/intraday-momentum-is-dead-in-the-0dte-era-we-measured-it-on-1085-spx-sessions-43g0)
- Same as S1, but trade only when the bar-observable filter is "on."
- Evidence base: the effect is concentrated on negative-gamma days (Baltussen) and high-volume, high-volatility days (Gao). Short-gamma-only days after 2022 showed t = 3.1.

**S3. FOMC-day reversal.** Sources: [CXO](https://cxoadvisory.com/calendar-effects/stock-market-return-reversal-after-fomc-announcements); [PWB](https://paperswithbacktest.com/strategies/the-fomc-announcement-reversal)
- Calendar: scheduled FOMC days (public).
- Signal: ES return over the 24 hours to 13:50 ET.
- Entry: at 13:50 ET, opposite to the sign of that return.
- Exit: at the end of the session.
- Holding: about 2 hours. Trades: 8 a year.
- Performance: +0.18% net per trade, Sharpe 0.36 (1997–2020, 180 events), at bid/ask.
- Out of sample: not verified for 2020 onward.

**S4. Turn-of-month, RTH only.** Sources: [CXO](https://www.cxoadvisory.com/calendar-effects/stock-index-futures-calendar-effects/); contradicted by the [Fed WP](https://www.fedinprint.org/item/fedawp/13394/original)
- Long ES from the RTH open to the RTH close on the first trading day of the month (optionally days −1 to +3).
- Trades: 12–48 a year. No primary per-trade number was found.

**S5. ZN-to-ES lead-lag filter.** Source: [Pan et al. 2025](https://en.saif.sjtu.edu.cn/junpan/Correlation_2025.pdf)
- The return of ZN over the last k minutes predicts ES. No cost evidence was found. Use it only as a confirmation filter for S1 or S2.

### Inferences
- S1 and S2 are the best-documented and most testable choices given the user's data. The user's 2018–2026 sample sits entirely in the post-decay window, so the honest prior is that unconditional S1 is roughly zero net, and that any S2 filter found in-sample needs holdout confirmation.
- S3 is cheap to test and does not overlap the tested families, but expect wide confidence intervals with about 60 events from 2018 to 2026.

### Gaps
- Exact per-trade bps for ES alone, for S1 net after 2018, and for S4 were not found in primary sources.

---

## Q3. Ablation-grid parameters

### Takeaway
Vary the signal window, the entry and exit times (especially a last-10-minute exit), the conditioning filter, the trade direction, and the instrument. Keep the grid small, because the per-trade edge is close to costs and a large grid will overfit.

### Cited Findings
- The predictive window choices that matter in the literature are the first half hour (Gao) versus the rest of the day (Baltussen), and the second-to-last half hour on its own. — [Baltussen et al.](https://academicweb.nd.edu/~zda/intramom.pdf)
- The effect is concentrated in the last 10 minutes. — [Aalto thesis](https://aaltodoc.aalto.fi/items/1011f043-edd1-4cb2-9694-b1216d77561f)
- Conditioning on signal strength matters: Rosa's Markov-switching result, and Gao's high-volatility and high-volume days. — [Rosa 2022](https://onlinelibrary.wiley.com/doi/10.1002/fut.22375?af=R); [Gao et al.](https://www.smallake.kr/wp-content/uploads/2015/01/SSRN-id2440866.pdf)

### Inferences (suggested grids)

**S1/S2, last-half-hour momentum**

| Parameter | Values |
|---|---|
| Signal start | prior RTH close; today's RTH open (excludes the gap); 09:30 + 30 min only (Gao FH) |
| Signal end / entry time | 15:00, 15:30, 15:45, 15:50 ET |
| Exit | 15:50, 15:55, 16:00, 16:15 (the ES settlement and close) |
| Filter type | none; \|rROD\| > k × ATR20 or k × the trailing stdev of rROD, with k in {0.5, 1, 1.5}; prior 5- or 20-day realized vol above its rolling median; down days only (rROD < 0, a proxy for put-heavy short gamma); RTH volume to 15:30 above its 20-day median |
| Signal agreement | require the sign of FH and rROD to agree, on or off |
| Instrument | ES, NQ, RTY, YM separately, plus an equal-weight basket |
| Cross-market filter | ZN return over the same window agrees with or opposes ES, on or off |

**S3, FOMC reversal**

| Parameter | Values |
|---|---|
| Signal window | 24h, RTH-open-to-entry, 4h |
| Entry | 13:45, 13:50, 13:55 |
| Exit | 15:00, 15:30, 16:00 |
| Magnitude threshold | \|signal\| > 0, 0.25%, 0.5% |
| Delay after 14:00 | 0 or 5 min (to avoid the announcement spike) |

**S4, turn of month**

| Parameter | Values |
|---|---|
| Window | day −1, +1, +2, +3 RTH sessions |
| Entry | at the open or at 10:00 |

**Cost-stress**
- Run every variant at 1 tick and at 2 ticks slippage. Report bps per trade alongside PF, so the 1.0–1.2 bps hurdle is visible.

### Gaps
- No paper validates the specific bar-only gamma proxies above. They are hypotheses to test, not documented effects.
