# Replication, Decay and Robustness of Published Intraday Futures Anomalies

Scope: evidence quality across intraday futures strategies (flat by session close, 1-min OHLCV only) for a strict test design: development 2018–2022, validation 2023–2024, holdout 2025–2026, costs of 1 tick + $2.50 per side, Sharpe ≥ 0.75, deflated Sharpe across a 500–10,000 config grid. Families already tested by the user (ORB/noise-band, generic MR, RSI, squeeze, MA cross, Donchian, convexity fade, EMRT pairs, FX-fix reversal, drift-burst fade) are excluded as standalone candidates.

Source-quality note: several of the most relevant post-2024 replications are GitHub repos, Substack posts, arXiv preprints or SSRN working papers, not peer-reviewed. Treat them as indicative. One search tool repeatedly mislabelled the Baltussen et al. (JFE 2021) PDF hosted at nd.edu as a "Zarattini et al." paper. The attribution below was checked against the PDF text (authors Baltussen, Da, Lammers, Martens).

## Q1. What do large replication and multiple-testing studies say about anomaly decay, and is there futures or intraday-specific evidence?

### Takeaway
On average, published anomalies lose about a quarter of their return out of sample and over half after publication (equities). About two-thirds fail even plain replication once microcaps are controlled, and multiple-testing work argues for t ≥ 3. The intraday-futures-specific evidence is thin but points the same way. The canonical intraday momentum results (Gao et al. 2018) fail out of sample in at least one peer-reviewed test (Rosa 2022) and in independent informal replications. Post-2024 tests of the "Beat the Market" noise-band strategy show weakening or flat results on ES.

### Cited Findings
- McLean & Pontiff (JF 2016), 97 predictors: portfolio returns are 26% lower out-of-sample and 58% lower post-publication. The authors treat the 26% as an upper bound on data mining and attribute about 32 pp to publication-informed trading. — [Ivey copy of McLean & Pontiff](https://ivey.uwo.ca/media/3775549/pontiff.pdf); [Gwern mirror](https://Www.Gwern.net/doc/economics/2016-mclean.pdf)
- Jacobs & Müller: across 241 anomalies in 39 markets, the US is the only country with a reliable post-publication decline in long/short returns. None of the 38 international markets show one. — [Jacobs & Müller paper](https://www.wiwi.hu-berlin.de/en/Professorships/bwl/finance/seminars/papers-fin-acc-res-seminars/17s/jacobs.pdf)
- Hou, Xue & Zhang (RFS 2020), "Replicating Anomalies": with microcaps controlled (NYSE breakpoints, value weights), 65% of 452 anomalies fail |t| = 1.96, including 96% of the trading-frictions category. A multiple-test hurdle of 2.78 raises the failure rate to 82%. Even replicated anomalies have much smaller economic magnitudes than originally reported. — [NBER w23394](https://nber.org/papers/w23394); [EconPapers RFS listing](https://econpapers.repec.org/RePEc:oup:rfinst:v:33:y:2020:i:5:p:2019-2133.)
- Harvey, Liu & Zhu (RFS 2016): new factors should clear t ≈ 3.0 rather than 2.0, and many published findings in financial economics are likely false. — [NBER w20592](https://www.nber.org/papers/w20592); [EconPapers](https://econpapers.repec.org/RePEc:oup:rfinst:v:29:y:2016:i:1:p:5-68.)
- A 2026 NBER working paper by Harvey, Sancetta & Zhao still argues for a t-cutoff of at least 3.0 and cites Hou-Xue-Zhang among the replication literature. — [NBER w34898](https://www.nber.org/system/files/working_papers/w34898/w34898.pdf)
- Bailey & López de Prado (JPM 2014), Deflated Sharpe Ratio: corrects for selection bias under multiple testing and for non-normal returns (skew, kurtosis). It sets the PSR benchmark at the expected maximum Sharpe across all trials. Not controlling for the number of trials gives over-optimistic expectations. López de Prado (2018) proposes clustering similar strategies to estimate the effective number of independent trials. — [SSRN 2460551](https://papers.ssrn.com/abstract=2460551); [Wikipedia summary of inputs](https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Intraday-specific, peer-reviewed failure.** Rosa (J. Futures Markets 2022, "Understanding intraday momentum strategies") tests the Gao et al. overnight-plus-first-half-hour → last-half-hour strategy out of sample and finds the predictability disappears. A Markov-switching model shows two regimes. A thresholded (signal-strength) version earns more than an always-on version. — [IDEAS listing](https://ideas.repec.org/a/wly/jfutmk/v42y2022i12p2218-2234.html); [EconPapers](https://econpapers.repec.org/RePEc:wly:jfutmk:v:42:y:2022:i:12:p:2218-2234)
- **Intraday-specific, peer-reviewed support.** Li, Sakkas & Urquhart (J. Financial Markets 2022): intraday time-series momentum across 16 developed markets is economically meaningful and statistically significant in- and out-of-sample in most countries. It is stronger when liquidity is low, volatility is high, and information arrives in bursts. — [IDEAS](https://ideas.repec.org/a/eee/finmar/v57y2022ics138641812100001x.html)
- **Pre-FOMC drift decay (event-day anomaly).** Kurov, Wolfe & Gilbert (Finance Research Letters 2021) find the Lucca-Moench pre-FOMC drift essentially vanished after 2015 (sample to Dec 2019), both with and without press conferences. Ben Dor & Rosa (2019) found no change, so the break date is disputed. Lucca-Moench found no drift in Treasuries or money-market futures. — [Kurov et al. PDF](https://www.skidmore.edu/economics/documents/KurovWolfeGilbert-TheDisappearingPre-FOMC-Announce-Drift-200914.pdf); [IDEAS](https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html)

### Inferences
- A reasonable prior is that a published intraday edge keeps at most about 40–50% of its in-paper return post-publication. Intraday effects tied to trading frictions or liquidity, which are most of the intraday literature, belong to the category with the worst replication rate (96% failure in HXZ, equities).
- The US-only decay in Jacobs & Müller fits arbitrage capital erasing published effects in the most-watched markets. ES/NQ are the most-watched intraday instruments in the world, so decay risk there is maximal.

### Gaps
- I found no futures-specific meta-analysis equivalent to McLean & Pontiff, meaning a systematic pre/post-publication study across many intraday futures anomalies. The futures and intraday evidence is study-by-study.
- I could not read the full text of Delgado's SSRN audit of "Beat the Market" (HTTP 403), so its post-publication Sharpe figures are not recorded.

## Q2. Which intraday futures strategies have independent replications confirming them after 2018, and which failed?

### Takeaway
The best-documented candidate is **market intraday momentum in the last 30 minutes** (Baltussen, Da, Lammers & Martens, JFE 2021). It uses the return from the prior close to 30 minutes before the close (r_ROD) to predict the last half hour, and holds across 60+ futures in four asset classes from 1974 to 2020, including the 2000–2020 subsample. Its mechanism is negative-gamma hedging. The weaker Gao et al. signal (first half-hour → last half-hour) has failed out of sample (Rosa 2022) and in informal 2021–2026 replications. Post-publication tests of the noise-band strategy (already in the user's book) on futures are flat for ES and insignificant for NQ. A 2026 falsification study of 14 OHLCV momentum families on MNQ found none that survived costs plus walk-forward. Announcement-day drifts (pre-FOMC) have decayed.

### Cited Findings
**Market intraday momentum (r_ROD → last half hour). Strongest evidence, but no published post-2020 futures replication found.**
- Data: tick data on 60+ futures (equity index; 16 government bond futures; 21 commodities: 5 metals, 4 energy, 12 softs; 8 currency futures), 1974–May 2020. "Strong market intraday momentum everywhere." — [Baltussen et al. JFE 2021, author PDF](https://www3.nd.edu/~zda/intramom.pdf); [IDEAS](https://ideas.repec.org/a/eee/jfinec/v142y2021i1p377-403.html)
- A simple timing strategy (sign of r_ROD, hold last 30 min) earns annualized Sharpe ratios of 0.87–1.73 at the asset-class level, gross of costs. — [Baltussen et al.](https://www3.nd.edu/~zda/intramom.pdf)
- r_ROD has higher OOS R² and t-stats than Gao's first-half-hour signal in equities, bonds and commodities. Currencies are the exception: weakest effect, coefficients positive but insignificant in some specifications. The second-to-last half-hour predictor (r_SLH) does not extend to commodities and currencies. — [Baltussen et al.](https://www3.nd.edu/~zda/intramom.pdf)
- Subsample table (1974–1999 vs 2000–2020): the effect is present in both, and the authors call it "robust over time" and "increasingly prominent." — [Baltussen et al.](https://www3.nd.edu/~zda/intramom.pdf)
- **Costs:** the paper's main results ignore transaction costs. The authors say the strategy "might not be exploitable to many investors" after costs, but that S&P 500 futures yield a positive net Sharpe at a one-tick cost. — [Baltussen et al.](https://www3.nd.edu/~zda/intramom.pdf)
- The authors also find next-day reversals in all four markets, insignificant in currencies, consistent with price pressure. — [Baltussen et al.](https://www3.nd.edu/~zda/intramom.pdf)
- Mechanism: hedging of short gamma exposure (option dealers, leveraged-ETF rebalancing) trades in the direction of the move. A direct negative-gamma-exposure proxy confirms the effect is stronger when dealer gamma is more negative. — [Baltussen et al.](https://www3.nd.edu/~zda/intramom.pdf); [Alpha Architect summary](https://alphaarchitect.com/hot-topic-does-gamma-hedging-actually-affect-stock-prices/)
- Crude oil: on Wednesday EIA days, the third half-hour predicts the last half-hour. On other days only the first half-hour predicts, mainly via the overnight component. — [Hull repository paper](https://hull-repository.worktribe.com/OutputFile/3303156)
- Chinese commodity futures (JFM 2020): the first half-hour predicts the last half-hour in copper, rebar, soybean and soymeal, strongest after high-volume or high-volatility openings in metals. — [EconPapers JFM 40(4)](https://econpapers.repec.org/RePEc:wly:jfutmk:v:40:y:2020:i:4:p:632-650)

**Gao et al. (JFE 2018) first-half-hour → last-half-hour. Failed or fragile.**
- Original: SPY 1993–2013, plus 10 other ETFs. Stronger on high-volatility and high-volume days. — [Alpha Architect summary](https://alphaarchitect.com/2014/08/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/)
- Rosa (JFM 2022): predictability disappears out of sample. — [IDEAS](https://ideas.repec.org/a/wly/jfutmk/v42y2022i12p2218-2234.html)
- Independent CFD replication, 7 instruments, M15 bars, 2021–2026: the Gao β₁ is *negative* on all seven (t from −2.50 to −0.31). Of 19 "displacement" specifications significant in development, 0 survived the 2025–26 holdout. Unconditional effects were 0.01–0.07 ATR, about an order of magnitude below costs. An apparent late-session reversal was a bug: including the 16:00 post-close bar. Caveat: retail CFD data, not futures. — [talalmalikllc-debug/market-anomaly-replications](https://github.com/talalmalikllc-debug/market-anomaly-replications)
- The same repo finds that the overnight→intraday reversal (Della Corte et al.) has the right sign (corr −0.05 to −0.08 on four indices), but gap-fade win rates sit near 49% and the effect is not exploitable after costs. — [market-anomaly-replications](https://github.com/talalmalikllc-debug/market-anomaly-replications)

**Noise-band / "Beat the Market" (Zarattini, Aziz & Barbon 2024). Already in the user's book; relevant as decay evidence.**
- A GitHub replication on 16 years of 1-min ES/NQ futures after costs finds NQ still positive post-publication but not significant (t = 1.37 over about 585 days), and ES flat or negative post-publication. The repo page now returns 404; this information is from the search snippet only. — [VigorTas/beat-the-market-replication (search result)](https://github.com/VigorTas/beat-the-market-replication)
- Serpa (June 2026) reproduced the in-sample result almost exactly (19.8% p.a., Sharpe 1.34 vs original 19.6%, 1.33). On unseen data (May 2024–Mar 2026), Swedroe reports the result "told a very different story." The exact OOS numbers are paywalled. — [Swedroe Substack](https://larryswedroe.substack.com/p/when-beat-the-market-meets-the-real)
- Delgado (SSRN, 2026) audits SPY 2000–Aug 2026: a strong early post-publication period, then a materially weak recent regime. Conclusions are sensitive to window choice, and the author argues against a simple story of immediate decay. — [SSRN 7323419 (search snippet; full text 403)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7323419)

**OHLCV intraday momentum broadly. Systematic falsification.**
- Mesfin (arXiv 2605.04004 v3, Sep 2026): 14 OHLCV intraday momentum families on MNQ 5-min bars, 2021–2025, expanding walk-forward, OOS years 2023–2025. Criteria: net t ≥ 2, ≥ 30 trades per fold, positive net, year-consistent sign, permutation p < 0.001. No family passed. Eleven failed because gross edge (0.07–1.50 pts) was below a 2-pt round-trip friction floor. ORB-long (t = 0.88), a classifier reversal (t = 1.26) and gap-continuation short (+16.5 pts gross, t = 1.46) cleared friction but were unstable across years. Single author, unreviewed preprint. — [arXiv 2605.04004](https://arxiv.org/abs/2605.04004)

**Announcement-day effects**
- The pre-FOMC equity drift has largely vanished since 2016 (Kurov et al.), though this is disputed. — [Kurov et al.](https://www.skidmore.edu/economics/documents/KurovWolfeGilbert-TheDisappearingPre-FOMC-Announce-Drift-200914.pdf)

**Intraday seasonality / time-of-day**
- Heston, Korajczyk & Sadka (JF 2010): a stock's return in a given half-hour predicts returns in the same half-hour on later days, for at least 40 trading days. This is cross-sectional equities. Baltussen et al. show market intraday momentum is distinct from it, and find that the previous day's last half-hour coefficient is *negative* and significant for equity index futures. — [HKS paper](https://www.bauer.uh.edu/departments/finance/documents/Heston_Korajczyk_Sadka_paper_UH.pdf); [Baltussen et al.](https://www3.nd.edu/~zda/intramom.pdf)
- A Nov 2025 working paper (Haendler, Heston, Korajczyk, Sadka) revisits the periodicity puzzle in stocks. Findings not retrieved. — [SSRN 5749704](https://papers.ssrn.com/ab_id=5749704)

**Cross-asset lead-lag at minute horizons**
- Huth & Abergel: high-frequency lead-lag between equities and equity futures varies over the day and around news. — [arXiv 1111.7103](https://www.arxiv.org/pdf/1111.7103)
- A Frankfurt study finds significant lead-lag among related instruments (e.g., long vs medium bond futures) at lags from microseconds up to one minute. — [Uni Frankfurt](https://publikationen.ub.uni-frankfurt.de/opus4/files/80803/4-5.pdf)
- Chinese index futures calendar-spread lead-lag is reported profitable after costs, but at tick level. — [arXiv 2501.03171](https://arxiv.org/pdf/2501.03171)

### Inferences
- **Strongest candidate not yet in the user's book: Baltussen r_ROD → last-30-min momentum**, run on ES, NQ, RTY, YM, ZN, ZB, CL and GC, but probably not 6E/6J, where the effect is weakest. Reasons: (a) an economic mechanism that is not simply "a pattern" (dealer and leveraged-ETF gamma hedging, which has grown with 0DTE options); (b) 45 years and four asset classes; (c) one trade per day per market, about 250/yr, which fits the trade-frequency window; (d) a very small config grid (signal threshold, entry minute, which "close" to use), so DSR deflation is small. Risks: no published futures replication after May 2020 was found. The overlap with the noise-band family is partial: both are trend-into-close. Gao's related signal failed OOS. The 30-minute hold has a small per-trade standard deviation, so the per-trade edge in bps is small relative to cost on ZN/ZB/CL (see Q5).
- Rosa's regime/threshold finding and the high-volatility result in Li-Sakkas-Urquhart and Gao suggest r_ROD momentum should be traded conditionally, when |r_ROD| is large or realized volatility is high, not unconditionally. That conditioning is also a natural way to raise gross edge per trade above costs.
- The 2021–2026 informal replications that "fail" mostly test the *first-half-hour* signal on CFDs or ETFs with spreads. They do not directly refute Baltussen's r_ROD futures result. They do show that the effect on ES is at most a few bps.
- Lead-lag at minute horizons is mostly a sub-minute or tick phenomenon in the literature. With 1-min bars and 1-tick slippage it is unlikely to be exploitable. Treat it as low priority.

### Gaps
- No peer-reviewed post-2020 out-of-sample test of Baltussen r_ROD momentum on US futures was found. That is precisely the user's 2023–2026 window.
- No credible study of same-half-hour intraday seasonality (HKS-style) on futures time series was found.
- No futures-specific post-2015 test of the pre-FOMC drift was found. Macro-announcement-day intraday effects (CPI/NFP) in futures were not covered by retrieved sources.

## Q3. Which ideas work as filters or overlays rather than standalone strategies?

### Takeaway
Volatility *management* of portfolios (Moreira-Muir) mostly fails out of sample, including in commodity futures. Conditioning an intraday momentum signal on high volatility, large signal magnitude or negative dealer gamma has consistent support across several independent studies. The most defensible overlays are therefore "trade only when the signal or volatility is large," not volatility-scaled sizing of a weak strategy.

### Cited Findings
- Cederburg, O'Doherty, Wang & Yan (JFE 2020), 103 equity strategies: volatility-managed versions do not systematically beat the originals. Real-time out-of-sample versions earn *lower* Sharpe ratios and certainty-equivalent returns, which the authors attribute to structural instability in the spanning regressions. — [Lehigh copy](https://www.lehigh.edu/~xuy219/research/COWY.pdf); [Alpha Architect](https://alphaarchitect.com/does-portfolio-timing-based-on-volatility-signals-outperform-buy-and-hold/)
- Kang & Kwon (JFM 2021), commodity futures: volatility management looks successful in-sample for 12-month momentum and the market portfolio but fails to improve real-time out-of-sample performance. — [IDEAS](https://ideas.repec.org/a/wly/jfutmk/v41y2021i2p159-178.html)
- Counterpoint: DeMiguel, Martín-Utrera & Uppal (JF 2024) find a conditional *multifactor* volatility-managed portfolio beats its unconditional counterpart out of sample and net of costs. — [LBS PDF](https://lbsresearch.london.edu/id/eprint/3716/1/The%20Journal%20of%20Finance%20-%202024%20-%20DeMIGUEL%20-%20A%20Multifactor%20Perspective%20on%20Volatility%E2%80%90Managed%20Portfolios.pdf)
- Intraday momentum is stronger when volatility is high, liquidity is low, and information arrives in bursts, across 16 countries and over time. — [Li, Sakkas & Urquhart 2022](https://ideas.repec.org/a/eee/finmar/v57y2022ics138641812100001x.html)
- Gao et al.: predictability is stronger on high-volatility and high-volume days. — [Alpha Architect](https://alphaarchitect.com/2014/08/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/)
- Rosa 2022: a thresholded (signal-strength) intraday momentum strategy beats always-active. — [IDEAS](https://ideas.repec.org/a/wly/jfutmk/v42y2022i12p2218-2234.html)
- Chinese metals: the strongest intraday momentum follows high-volume or high-volatility first sessions. — [EconPapers JFM 2020](https://econpapers.repec.org/RePEc:wly:jfutmk:v:40:y:2020:i:4:p:632-650)
- Baltussen et al.: the effect is stronger with more negative dealer gamma exposure. This proxy needs options data the user lacks. — [Baltussen et al.](https://www3.nd.edu/~zda/intramom.pdf)
- The "Beat the Market" strategy already uses volatility-targeted sizing (2% daily target, 4× cap), yet still weakened out of sample. Vol targeting did not prevent decay. — [Swedroe Substack](https://larryswedroe.substack.com/p/when-beat-the-market-meets-the-real)

### Inferences
- With 1-min OHLCV only, usable proxies for "high-gamma-pressure" or high-predictability days are: prior-day or intraday realized volatility rank, |r_ROD| relative to its trailing volatility, opening-session volume relative to its trailing average, and trend state. Each adds only 1–3 parameters, which keeps the DSR grid small.
- Volatility-scaled *sizing* should be treated as a risk-control choice, not a Sharpe-improving overlay. The out-of-sample evidence that it raises Sharpe is negative in both equities and commodity futures.
- No retrieved source tested VIX-level regime filters on intraday futures strategies. VIX is also not in the user's dataset, though ES realized volatility is a close substitute.

### Gaps
- No study was found that applies a trend-state or VIX filter to an intraday futures strategy and reports out-of-sample Sharpe improvement.
- No study was found on volatility-targeted *intraday* (as opposed to monthly or daily) futures strategies out of sample.

## Q4. Newer (2020–2026) price/volume-only intraday futures papers with strong OOS claims, including ML: how credible?

### Takeaway
I found no credible peer-reviewed 2020–2026 paper showing a strong net-of-cost out-of-sample intraday futures edge from OHLCV alone, ML or otherwise. The most rigorous recent work is negative (the MNQ falsification study, informal replications). Positive claims tend to be tick or order-book based, Chinese markets, or ignore costs.

### Cited Findings
- MNQ falsification (2026): 0 of 14 OHLCV intraday momentum families pass net-of-cost walk-forward criteria. Two "positive controls" (an RTH confluence signal, OOS t = 3.11, n = 196; a London-session signal, OOS t = 4.30, n = 247) are claimed but not fully described. This is a single-author preprint with v3 corrections to t-stats, so treat the controls with caution. — [arXiv 2605.04004](https://arxiv.org/abs/2605.04004)
- An ES ML paper (arXiv 2020) classifies price extrema with microstructure and price-action features. It predates the window, uses microstructure inputs, and no net-of-cost OOS result was retrieved. — [arXiv 2009.09993](https://arxiv.org/pdf/2009.09993v2)
- A daily (not intraday) stat-arb transferred to futures reports an OOS break-even cost of only 6.3 bp. — [JRFM 2021](https://mdpi.com/1911-8074/14/3/119)
- Retail-CFD replications of three top-journal intraday anomalies (JF 2024 FX fix, JFE 2018 intraday momentum, overnight-intraday reversal): none replicates net of realistic per-event costs. Sign-level patterns often appear but do not survive costs or holdouts. Placebo time anchors performed as well as the true FX-fix anchors. — [market-anomaly-replications](https://github.com/talalmalikllc-debug/market-anomaly-replications)

### Inferences
- An ML model on 1-min OHLCV across a 500–10,000 config grid faces the steepest DSR hurdle (see Q5) and has no published OOS support. It should be deprioritised as a standalone strategy. If used, it belongs as a filter on a mechanism-based signal (e.g., r_ROD momentum) with a small hyperparameter grid.
- Common failure modes visible in the replications: (1) gross edge of 0.1–1.5 index points vs a 1–2 point round-trip cost; (2) year-to-year sign instability; (3) data artifacts (post-close bars, session-boundary errors); (4) cost estimated at median spread when actual event-time spreads are about 3× higher; (5) pooling correlated instruments inflates t-stats; (6) regime dependence (Rosa); (7) post-publication crowding (McLean-Pontiff, noise-band OOS).

### Gaps
- I found no peer-reviewed deep-learning paper on US futures 1-min bars with walk-forward, net-of-cost OOS results post-2020. Absence in a limited search is not proof of absence.

## Q5. What per-trade edge (bps) is needed to survive realistic futures costs at 50–500 trades/year?

### Takeaway
Round-trip cost under "1 tick + $2.50 per side" is about 0.4–2 bp on equity index futures, GC and 6E at 2024–26 price levels, and about 3–6 bp on ZN, ZB and CL. The Sharpe ≥ 0.75 hurdle needs net mean per trade ≥ 0.75/√N times the per-trade standard deviation. The DSR hurdle from a large grid is far stricter than 0.75: under independence the expected maximum null Sharpe is about 1.4–1.7 on a 5-year development sample with 500–10,000 trials. A small, mechanism-driven grid is therefore essential.

### Cited Findings
- Baltussen et al. note that S&P 500 futures intraday momentum stays net-positive at a one-tick cost, implying the edge is of the order of a few bps. — [Baltussen et al.](https://www3.nd.edu/~zda/intramom.pdf)
- The MNQ study's 2-point round-trip friction floor (about 1 bp at NQ ≈ 20,000) wiped out 11 of 14 signal families with gross edges of 0.07–1.5 pts. — [arXiv 2605.04004](https://arxiv.org/abs/2605.04004)
- For CFD event trades, average per-event spread (1.29 ATR) swamped a +0.56 ATR gross edge. Costing at the median spread understates event-time costs by about 3×. — [market-anomaly-replications](https://github.com/talalmalikllc-debug/market-anomaly-replications)
- DSR: the benchmark Sharpe rises with the number of trials and the cross-trial variance of Sharpe. — [SSRN 2460551](https://papers.ssrn.com/abstract=2460551); [Wikipedia](https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)

### Inferences (my own calculations from contract specs; tick values are standard CME specs, prices approximate)
Round trip = 2 ticks + $5.

| Contract | Tick $ | Round-trip $ | Approx. notional (2025) | RT cost bp | RT cost bp at 2018 prices |
|---|---|---|---|---|---|
| ES | 12.50 | 30 | ~6,000×50 = $300k | ~1.0 | ~2.2 (ES≈2,700) |
| NQ | 5.00 | 15 | ~21,000×20 = $420k | ~0.36 | ~1.1 (NQ≈7,000) |
| RTY | 5.00 | 15 | ~2,200×50 = $110k | ~1.4 | ~1.9 |
| YM | 5.00 | 15 | ~44,000×5 = $220k | ~0.7 | ~1.2 |
| ZN | 15.625 | ~36 | ~$110k | ~3.3 | ~3.0 |
| ZB | 31.25 | ~67.5 | ~$115k | ~5.9 | ~4.5 |
| CL | 10.00 | 25 | ~$70k | ~3.6 | ~3.8 |
| GC | 10.00 | 25 | ~$250–400k | ~0.6–1.0 | ~1.9 |
| 6E | 6.25 | 17.5 | ~$137k | ~1.3 | ~1.2 |
| 6J | 6.25 | 17.5 | ~$84k | ~2.1 | ~1.6 |

- **Sharpe hurdle.** Annual SR ≈ (net mean per trade ÷ SD per trade) × √N. To reach SR 0.75, net mean / SD must be at least 0.106 (N = 50), 0.075 (N = 100), 0.047 (N = 250) or 0.034 (N = 500).
  - Example: a last-30-min ES hold with SD about 20–30 bp at N = 250 needs net ≈ 1.0–1.4 bp, so gross ≈ 2–3.5 bp after 1–2 bp of cost.
  - Example: a full-session hold with SD about 80–100 bp at N = 250 needs net ≈ 4–5 bp per trade.
  - Example: at N = 50, a session hold with SD about 100 bp needs net about 10 bp per trade, plus cost.
  - Per-trade SDs are rough assumptions, not sourced; measure them on the data.
- **DSR hurdle.** Expected maximum Sharpe under the null, with N_eff independent trials and annual-SR sampling SD ≈ 1/√T_years: (1−γ)Φ⁻¹(1−1/N)+γΦ⁻¹(1−1/(Ne)) ≈ 2.28 (N = 50), 3.05 (500), 3.26 (1,000), 3.86 (10,000) standard deviations.
  - Over a 5-year development window, that is about 1.02, 1.37, 1.46 and 1.73 annual SR respectively.
  - Over the 2-year validation window it is about 1.6–2.7, so validation alone cannot reject the null for a large grid. It must be a confirmation of a single pre-chosen config.
  - Correlated grids have N_eff far below the raw count, so cluster configs (López de Prado) before computing DSR.
- **Practical implication.** Intraday edges in the literature are a few bps per trade. On ZN, ZB and CL, costs of 3–6 bp per round trip likely consume most of a last-30-min momentum edge. Equity index futures (especially NQ and ES at current price levels) and GC are where cost drag is smallest. Rising index levels since 2018 mean costs in bp roughly halved from the development period to the holdout. A strategy marginal in 2018–2022 may look better later for cost reasons alone, so that should not be mistaken for edge persistence.

### Gaps
- No sourced estimate was found of realistic slippage beyond 1 tick for market orders in the last 30 minutes (MOC imbalance periods), or around 14:30 ET settlement for ZN/ZB/CL/GC. The 1-tick assumption may be optimistic for ZB and CL at those times.
- Per-trade return SD by hold length per contract was not sourced. Measure it directly.
