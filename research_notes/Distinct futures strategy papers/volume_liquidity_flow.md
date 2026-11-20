# Volume-, liquidity- and flow-based trading signals computable from intraday OHLCV bars (liquid US futures)

Scope note: data is 1-min OHLCV continuous futures (ES, NQ, RTY, YM, CL, GC, 6E, 6J, ZN, plus SPY/QQQ), 2018-01 to 2026-10. No book, no aggressor side, no options. Families already tested by the user (ORB/noise-band momentum, mean reversion, RSI divergence, squeezes, MA cross, channel breakout, convexity, EMRT pairs) are excluded except where volume is the conditioning variable.

Research budget: about 20 tool calls. Primary-source text was read for three papers (Christensen-Oomen-Renò drift burst; Easley-López de Prado-O'Hara-Zhang "Microstructure in the Machine Age"; Gervais-Kaniel-Mingelgrin). The rest is from abstracts and search snippets, and this is flagged per item.

## Q1. Which papers have a core signal using volume or liquidity derivable from OHLCV bars? (candidate shortlist with exact rules)

### Takeaway
Seven sources form a usable shortlist. The strongest futures-native, bar-computable and volume-conditioned evidence is the **drift-burst / volume-conditioned 5-minute reversal** in ES (Christensen, Oomen and Renò). Next come **bar-level microstructure features** (Amihud, Kyle lambda, Roll, BVC-VPIN) on 87 futures (Easley, López de Prado, O'Hara and Zhang). The features predict the *sign of change in volatility or higher moments* out of sample (54-61% accuracy), not return direction. That makes them better as regime filters on existing strategies than as stand-alone entries. Classic volume-return papers (Campbell-Grossman-Wang, Llorente et al., Gervais-Kaniel-Mingelgrin) give the conditioning logic, but they are daily equity studies, so futures/intraday adaptation is the user's own contribution. The VWAP-trend evidence is practitioner-grade and weak on independent replication.

### Cited Findings

**A. Drift burst + volume-conditioned reversal (top pick: futures-native, includes ES/ZN/CL/6E)**
- Paper: Kim Christensen, Roel C. A. Oomen, Roberto Renò, "The drift burst hypothesis." arXiv:2601.08974 (v2, 15 Jan 2026), econ.EM. The arXiv page lists related DOI 10.1016/j.jeconom.2020.11.004, which is the Journal of Econometrics version (I did not verify the volume/issue). — [arXiv](https://arxiv.org/abs/2601.08974)
- Data: tick-level futures for six asset classes, including E-mini S&P 500 (ES), 10-yr T-Note, Euro FX (6E), crude (CL). Sample Jan 2012 to Dec 2017 (ES from Jan 2010). Analysis restricted to liquid parts of the day. — [arXiv PDF](https://arxiv.org/pdf/2601.08974)
- Detection: a nonparametric t-statistic, the ratio of a kernel-smoothed local drift estimate to local spot volatility. Drift bandwidth h_n in {120, 300, 600} s (main spec 5 min). Volatility bandwidth 5×h_n (25 min in the main spec, Parzen kernel). Critical values 4.0 / 4.5 (also 4 to 6 tested), with extreme-value-theory-based critical values. Events are taken at local extrema of the t-stat over any 5-min window. At critical value 4.5 there are 202 drift bursts in ES, about one a week. — [arXiv PDF](https://arxiv.org/pdf/2601.08974)
- Reversal rule as measured: R− = 5-min log return ending at the burst peak t_j; R+ = next 5-min log return. Regression R+ = a + b·R−. Pooled slope b = −0.23 (−0.19 ex top decile). About 71% of events reverse, and per-contract reversal frequency "rarely drops below 65%". Regression R² is about 25-40%, roughly 30% on average. — [arXiv PDF](https://arxiv.org/pdf/2601.08974)
- Volume conditioning (ES): volume = 5-min notional volume normalized by the average trading rate at that time of day. Raw volume gives "broadly consistent" results. Negative bursts average −37.39 bps over 5 min, followed by +8.01 bps; positive bursts +36.41 bps, followed by −5.44 bps. Serial correlation is −0.80 (negative) vs −0.26 (positive). The reversal is stronger when the pre-burst move is larger or the volume is higher, mainly for negative bursts. In the double sort (Table 6, quartiles), the most-negative-return × high-volume cell has a +42.8 bps post-burst return vs 14.3 bps for low volume. They estimate the CGW interaction regression R+ = a + b R− + c R−·V−, and once volume is controlled, the serial correlation in negative bursts is "largely subsumed" by the interaction. — [arXiv PDF](https://arxiv.org/pdf/2601.08974)
- Unconditional caution: across *all* 5-min intervals, ES return autocorrelation is "tiny negative", slightly stronger when volume is above average. The authors call these effects "present, but extremely weak". The edge sits only in the extreme-event tail. — [arXiv PDF](https://arxiv.org/pdf/2601.08974)
- Costs / trading P&L: no trading strategy, transaction costs, or out-of-sample test is reported. Returns are measured on mid-quotes, not traded prices. — [arXiv PDF](https://arxiv.org/pdf/2601.08974)

**B. Bar-level microstructure features on 87 futures (Amihud, Kyle lambda, Roll, Roll impact, BVC-VPIN)**
- Paper: David Easley, Marcos López de Prado, Maureen O'Hara, Zhibai Zhang, "Microstructure in the Machine Age" (NBER conference draft Feb 2019; later published in the Review of Financial Studies 2021, a venue I did not verify in this session). — [NBER PDF](https://conference.nber.org/conf_papers/f117415.pdf)
- Data: 5 years of tick data for the 87 most liquid futures. Dollar-volume bars sized to give about 50 bars/day in 2016, with an hourly time-bar robustness check giving "slightly greater accuracy using volume bars" and largely unchanged importance. Rolling lookback W from 25 to 2000 bars. Rolls are handled by an "ETF price" ($1 invested) back-adjusted series, with the corresponding volume. — [NBER PDF](https://conference.nber.org/conf_papers/f117415.pdf)
- Exact feature formulas (all on bars, window W):
  - Roll measure R = 2·sqrt(|cov(ΔP_τ, ΔP_{τ−1})|) on close-to-close changes.
  - Roll impact = Roll / (p_τ·V_τ).
  - Kyle lambda λ = (p_τ − p_{τ−W}) / Σ_{i=τ−W}^{τ} b_i V_i, with b_i = sign(p_i − p_{i−1}) (bar tick rule).
  - Amihud λ_A = (1/W) Σ |r_i| / (p_i V_i).
  - VPIN = (1/W) Σ |V_i^S − V_i^B| / V_i, with BVC: V_i^B = V_i·Z(Δp_i/σ_Δp), V_i^S = V_i − V_i^B (Z = standard normal CDF).
  — [NBER PDF](https://conference.nber.org/conf_papers/f117415.pdf)
- Targets: the sign of change, over about a one-week horizon, in the Corwin-Schultz spread, realized volatility, Jarque-Bera, first-order autocorrelation, absolute skewness, and kurtosis. Validation is random forest + 10-fold purged CV, with MDI/MDA importance. — [NBER PDF](https://conference.nber.org/conf_papers/f117415.pdf)
- Results: out-of-sample accuracy is 0.54-0.61 depending on window, except the spread target, which is weaker. Amihud dominates in-sample importance, and VPIN dominates out-of-sample (most important for 5 of 6 targets). Roll is best for autocorrelation change. Kyle lambda and Roll are "never the most important" in-sample. Return *direction* is not predicted. — [NBER PDF](https://conference.nber.org/conf_papers/f117415.pdf)

**C. BVC / VPIN and its critiques (flow imbalance from bars)**
- ELO, "Discerning Information from Trade Data," JFE 120(2), 2016, 269-285: tick rule and BVC are both reasonable aggressor classifiers, but BVC is "better linked to proxies of information-based trading". — [SSRN](https://papers.ssrn.com/abstract=1989555); [RePEc](https://ideas.repec.org/a/eee/jfinec/v120y2016i2p269-285.html)
- Earlier ELO WP ("Bulk Classification of Trading Activity"): BVC correctly classifies about 91% of ES volume, 91.59% of oil, and 87.36% of gold, depending on bar specification. — [academia.edu](https://www.academia.edu/20057247/Bulk_Classification_of_Trading_Activity)
- Critique: Andersen and Bondarenko, "Assessing Measures of Order Flow Toxicity and Early Warning Signals for Market Turbulence," Review of Finance 19(1), 2015, 1-54. Using ES quote/trade data, BVC is inferior to the tick rule. VPIN predicts volatility only because rising volatility causes systematic BVC misclassification, and all of its predictive power vanishes after controlling for realized volatility. With perfect classification, VPIN behaves "diametrically opposite". — [RePEc](https://econpapers.repec.org/RePEc:oup:revfin:v:19:y:2015:i:1:p:1-54.); [CREATES WP 2013-43](https://repec.econ.au.dk/repec/creates/rp/13/rp13_43.pdf); [CREATES WP 2013-42](https://repec.econ.au.dk/repec/creates/rp/13/rp13_42.pdf)
- Chakrabarty, Pascual and Shkilko, "Evaluating trade classification algorithms: BVC versus the tick rule and the Lee-Ready algorithm," J. Financial Markets 25 (2015) 52-79: transaction-based classifiers are more accurate than BVC (equities). — [IDEAS](https://ideas.repec.org/a/eee/finmar/v25y2015icp52-79.html)
- BVC accuracy is strongly bar-size dependent: about 92.4% with 5-min time bars vs 50.9% with 1-sec bars (Indian equities; Massot, Nawn and Pascual WP). — [ACFR WP PDF](https://acfr.aut.ac.nz/__data/assets/pdf_file/0016/222037/ROBERTO-Massot-Samarpan-and-Pascual-2018-BVC-and-NOF-Preliminary-and-incomplete.pdf)
- Time-bar VPIN mechanically picks up trading intensity, while fixed-volume buckets avoid this (CREATES 2011-50). — [CREATES WP 2011-50](https://repec.econ.au.dk/repec/creates/rp/11/rp11_50.pdf)

**D. Volume-conditioned reversal vs continuation (theory + daily equity evidence)**
- Campbell, Grossman and Wang, "Trading Volume and Serial Correlation in Stock Returns," QJE 108 (1993) 905-939. Daily returns following high-volume periods are more negatively autocorrelated (liquidity-provider compensation). — [Harvard DASH PDF](https://dash.harvard.edu/bitstream/1/3128710/2/campbell_trading.pdf); [SSRN](https://papers.ssrn.com/abstract=297335)
- Llorente, Michaely, Saar and Wang (RFS 2002): small or high-spread stocks continue after high-volume days, while large or low-spread stocks "show almost no continuation and mostly return reversal following high-volume days." This implies hedging/liquidity trades dominate in very liquid instruments (relevant for ES/NQ/ZN). — [NYU archive PDF](https://archive.nyu.edu/jspui/bitstream/2451/26698/1/FIN-00-032.pdf)
- A 2024 century-long study (LeBaron et al., "A Century of Market Reversals") finds the intraday volume effect on reversals is "diminished, albeit still negative", with a strong negative volatility effect. — [PDF](https://bdlebaron.github.io/pdfs/ACenturyofMarketReversalsMarch2024.pdf)
- Index-futures intraday reversal after large price changes appears only on days with higher liquidity provision, and reversal predictability rises with volatility and volume (Lithuanian TEDE journal paper; full text fetch failed, snippet only). — [TEDE](https://bme.vgtu.lt/index.php/TEDE/article/download/22634/12772)
- Huang and Wang (2009, cited in the drift-burst paper) predict asymmetric, volume-amplified reversals after sell-offs. The drift-burst ES data confirm this asymmetry. — [arXiv PDF](https://arxiv.org/pdf/2601.08974)

**E. High-volume return premium (abnormal volume shocks)**
- Gervais, Kaniel and Mingelgrin, "The High-Volume Return Premium," JF 56(3) 2001, 877-919. Exact construction (daily sample, NYSE 1963-1996): non-overlapping 50-trading-day intervals (with a 1-day skip). The first 49 days are the reference period and day 50 is the formation day. A stock is "high (low) volume" if formation-day volume ranks in the top (bottom) 10% of the 50 daily volumes of the interval. Returns are measured over about the next 20 days (test period), with 1/10/20/50-day horizons. A weekly version uses 10-week intervals. Unusually high (low) volume stocks subsequently outperform (underperform). — [Wharton WP PDF](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/9901.pdf); [RePEc](https://econpapers.repec.org/RePEc:bla:jfinan:v:56:y:2001:i:3:p:877-919)
- Futures analogue (energy, daily): high volume levels precede extreme returns, while low volume has "no information about future returns" (J. Energy Markets). — [Risk.net](https://www.risk.net/journal-of-energy-markets/7932046/directional-predictability-between-returns-and-trading-volume-in-the-futures-markets-of-energy-insights-into-traders-behavior)

**F. Volume-conditioned intraday momentum (volume as a filter on an existing family)**
- Gao, Han, Li and Zhou (JFE 2018), "Market Intraday Momentum": the first half-hour SPY return predicts the last half-hour (1993-2013, R² about 1.6%), and predictability is stronger on higher-volume and higher-volatility days. — [WUSTL](https://profiles.wustl.edu/en/publications/market-intraday-momentum/); [AMS abstract](https://community.ams.org/amsmtgs/2229_abstracts/1108-00-199.pdf)
- Baltussen, Da, Lammers and Martens (JFE 142, 2021), 60+ futures 1974-2020: rest-of-day return predicts the last 30 min, with asset-class Sharpe 0.87-1.73. They use 1-min open/close/volume, and volume data are available from 2003. — [JFE via ND PDF](https://www3.nd.edu/~zda/intramom.pdf)
- Chinese commodity futures: intraday time-series momentum is strongest after high-volume or high-volatility first sessions (metals only). — [Hull repository](https://hull-repository.worktribe.com/OutputFile/3303156)

**G. VWAP trend (practitioner working paper)**
- Zarattini and Aziz, "Volume Weighted Average Price (VWAP): The Holy Grail for Day Trading Systems" (SSRN 2023). Rule: long when price > session VWAP, short when below, on QQQ/TQQQ intraday, 2 Jan 2018 to 28 Sep 2023. Reported $25k → $192,656 net of commissions (+671%). — [Concretum](https://concretumgroup.com/volume-weighted-average-price-vwap-the-holy-grail-for-day-trading-systems/)
- Replication concerns: a QuantConnect "not so fast" thread disputes the results, and an independent replication cites a Sharpe of about 0.7 OOS vs about 2.1 claimed. One author sells trading education. — [QuantConnect forum](https://www.quantconnect.com/forum/discussion/16706/bear-bull-traders-039-paper-on-quot-the-holy-grail-quot-not-so-fast/)

**H. Open interest (needs data beyond OHLCV)**
- Hong and Yogo, "What Does Futures Market Interest Tell Us about the Macroeconomy and Asset Prices?" JFE 105(3) 2012, 473-490. Open-interest growth forecasts commodity returns: one-SD higher commodity market interest gives +0.63%/month expected return (0.73% in another WP revision). It also predicts bond, currency and stock returns "to a lesser degree" and beats past prices as a predictor. — [NBER w16712](https://www.nber.org/papers/W16712); [RePEc](https://econpapers.repec.org/RePEc:eee:jfinec:v:105:y:2012:i:3:p:473-490)

**I. Realized (intraday) Amihud**
- "Realized Illiquidity" (Management Science, 2024/25): an Amihud measure using realized power variation from intraday returns. The expected component positively predicts returns and the unexpected component negatively (US stocks 2012-2024, daily frequency). — [INFORMS](https://pubsonline.informs.org/doi/10.1287/mnsc.2023.02505)

### Inferences
- Recommended families, in priority order for an ablation suite:
  1. **Volume-conditioned extreme-move reversal (drift-burst lite).** Signal: on 1-min bars, compute a k-min return (k ∈ {3, 5, 10}) and z-score it against a trailing realized-vol estimate (bandwidth 5k to 25k min). Trigger when |z| > c (c ∈ {3, 4, 4.5, 5}) at a local extremum, and require time-of-day-normalized volume above the q-th percentile (q ∈ {50, 75, 90}). Fade the move, hold H ∈ {5, 10, 30} min, with a side filter (long-only after drops vs symmetric) motivated by the documented asymmetry. Distinct from the user's existing mean reversion because the trigger is a volatility-scaled burst + volume gate.
  2. **CGW interaction reversal/continuation at the bar level.** Estimate rolling R_{t+1} = a + b R_t + c R_t·V_t, where V = log volume detrended by time-of-day profile. Trade sign(b + c·V_t)·R_t only when |prediction| exceeds a threshold. Llorente et al. imply reversal (c < 0) for very liquid contracts, but CL/GC/6J may differ, which is itself a testable ablation.
  3. **High-volume return premium, time-series version.** A daily or session bar is "high volume" if its volume is in the top 10% of the trailing N-day window (GKM: N = 50, 10%). Go long (or in the direction of the formation-day return) for H days. Weakest prior for futures, because GKM is cross-sectional and the visibility mechanism is about stocks.
  4. **Bar-level flow imbalance (BVC) / VPIN / Kyle lambda / Amihud as regime filters.** Use them to switch the user's existing momentum vs mean-reversion families on and off (Easley et al. show they forecast vol and autocorrelation changes, not direction). Use volume bars or ≥5-min time bars given the BVC bar-size sensitivity, and always include realized vol as a control (Andersen-Bondarenko).
  5. **Volume-filtered intraday momentum.** Add a "first-window volume / trailing same-window volume" gate to the existing noise-band/last-half-hour family (Gao et al.; Chinese futures). This is a cheap ablation axis, not a new family.
  6. **VWAP trend / VWAP-deviation reversion.** Easy to compute (cumulative Σ typical_price·V / ΣV from the session open). Treat it as a low-prior baseline given the replication issues.
- Since none of A-F report net-of-cost futures trading P&L with a post-2018 OOS period, every one of these must be validated by the user's own holdout. The drift-burst events are rare (about 1/week in ES), so trade counts will be small. Pooling across the 9 contracts helps.

### Gaps
- Llorente et al. (2002) exact regression form (R_{t+1} = C0 + C1 R_t + C2 V_t R_t with detrended log turnover, about 200-day trend) is from my prior knowledge. I did not verify it from the text in this session.
- No paper found that tests BVC-estimated order-flow imbalance from bars as a *return-direction* predictor in US futures. Evidence found is for volatility/toxicity, not returns.
- Gao et al. (2018): exact definition of "high-volume days" and the R² split were not extracted (the PDF fetched was actually Baltussen et al.).
- Nagel (2012, RFS, "Evaporating Liquidity", reversal returns as a liquidity-provision signature) is cited inside the drift-burst paper. I did not pull its rules.
- Intraday volume-profile / volume-at-price (market profile, POC/value area) support/resistance: I found no peer-reviewed paper in this session.
- No post-2018 out-of-sample evidence was found for any of the volume signals in US futures. The drift-burst sample ends 2017, and the Easley et al. sample is about 5 years ending about 2017.

## Q2. Which signals are robust to continuous-contract roll effects on volume?

### Takeaway
Signals that use **within-bar or within-session ratios** (BVC buy fraction, CGW interaction with time-of-day-normalized volume, drift-burst volume relative to the same time of day) are fairly roll-robust. Signals that compare **volume levels across days** (GKM 50-day ranking, Amihud/Kyle levels, abnormal-volume z-scores, VWAP anchored over multiple days) are exposed to roll-window volume migration and need a volume-based roll or summed-across-contracts volume plus roll-day masking. Open interest is the most roll-sensitive and is not in OHLCV.

### Cited Findings
- Easley et al. remove price jumps with an "ETF price" ($1-invested) continuous series and use the corresponding volume. They note futures "trade over a 23.75 hour day and volume patterns are very pronounced", which motivates dollar-volume bars. — [NBER PDF](https://conference.nber.org/conf_papers/f117415.pdf)
- Baltussen et al. roll to the next contract "when the daily tick volume of the next back-month contract exceeds the current contract" (a volume-based roll, which keeps volume on the liquid contract), and drop days with total volume < 100 contracts and early-close days. — [JFE 2021 via ND PDF](https://www3.nd.edu/~zda/intramom.pdf)
- Christensen et al. normalize 5-min notional volume by "the average trading rate at that time of the day" to remove intraday seasonality. Raw volume gave broadly consistent results. — [arXiv PDF](https://arxiv.org/pdf/2601.08974)
- GKM's own design compares a day's volume only to the prior 49 days of the same security (ranked within a 50-day window), so a level shift in the volume series mid-window directly contaminates the ranking. — [Wharton WP PDF](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/9901.pdf)
- Hong-Yogo's predictor is open interest growth, which on a single-contract series collapses at each expiry. It requires aggregate open interest across maturities. — [NBER w16712](https://www.nber.org/papers/W16712)

### Inferences
- With Databento, build continuous series with a volume-based roll (the user should confirm their continuous symbology, e.g. calendar vs volume vs open-interest ranked). Ideally, also sum volume across the front two contracts for volume-level features.
- Mask roll windows: for ES/NQ/RTY/YM/6E/6J/ZN quarterly rolls (about 8 days before expiry for equity index; ZN rolls near end of month before delivery), and for CL/GC monthly/bi-monthly rolls. Exclude roll day ±2 sessions for any feature with a cross-day volume denominator. This exclusion width is an ablation parameter.
- Prefer time-of-day-normalized volume (ratio to trailing D-day mean at the same minute-of-day, D ∈ {10, 20, 50}). This removes the U-shape and the Globex overnight vs RTH regime, and partly absorbs roll steps when D is short.
- Calendar-rolled front-month volume decays for several days before the roll date. That would mechanically create "low-volume" signals pre-roll and "high-volume" spikes post-roll, a likely false-positive source in GKM-style or abnormal-volume rules.
- BVC uses Δp/σ_Δp per bar, so it needs a back-adjusted price (or same-contract bar differences). Never difference across the roll seam.

### Gaps
- No paper found that quantifies how much roll-induced volume artifacts bias volume-based signals in continuous futures. This needs the user's own diagnostic (signal firing rate by days-to-roll).
- Whether the Databento OHLCV continuous series aggregates or switches volume at the roll was not checked here, nor whether open interest is available via a separate statistics feed.

## Q3. Natural ablation grids per family

### Takeaway
Each family has 3-5 natural axes: an event-size threshold, a volume-gate threshold, a volume normalization lookback, a bar/aggregation size, and a holding horizon. Most axes are directly anchored to values used in the papers.

### Cited Findings
- Drift-burst anchors: drift bandwidth {2, 5, 10} min, volatility bandwidth = 5× drift, critical value {4.0, 4.5, up to 6}, event window 5 min, post horizon 5 min, volume quartile sorts (low = Q1, medium = IQR, high = Q4), and at most one event per day. — [arXiv PDF](https://arxiv.org/pdf/2601.08974)
- Easley et al. anchors: lookback W ∈ {25, 50, …, 2000} bars, about 50 dollar-volume bars/day vs hourly time bars, about 1-week forecast horizon. — [NBER PDF](https://conference.nber.org/conf_papers/f117415.pdf)
- GKM anchors: reference window 49 days, top/bottom 10% cutoff, test horizons 1/10/20/50 days, daily vs weekly formation. — [Wharton WP PDF](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/9901.pdf)
- BVC bar-size sensitivity: 5-min time bars give much higher accuracy than 1-sec bars. — [ACFR WP PDF](https://acfr.aut.ac.nz/__data/assets/pdf_file/0016/222037/ROBERTO-Massot-Samarpan-and-Pascual-2018-BVC-and-NOF-Preliminary-and-incomplete.pdf)
- VWAP trend: binary price-vs-session-VWAP rule. The paper uses no grid, which leaves the anchor (session vs rolling) and a band/hysteresis as the natural axes. — [Concretum](https://concretumgroup.com/volume-weighted-average-price-vwap-the-holy-grail-for-day-trading-systems/)

### Inferences
Suggested grids. Values marked (paper) come from the source and the rest are my proposals.
- **Volume-gated burst reversal:** burst window k ∈ {3, 5 (paper), 10} min; vol bandwidth ∈ {5k (paper), 10k}; z threshold ∈ {3, 4 (paper), 4.5 (paper), 5}; volume gate ∈ {none, >median, >Q3 (paper), >P90} of time-of-day-normalized volume; side ∈ {both, long-after-drop only}; hold ∈ {5 (paper), 15, 30, to-close} min; session ∈ {RTH only, 24h}; max events/day = 1 (paper).
- **CGW interaction:** bar size ∈ {5, 15, 30, 60} min; volume detrend lookback D ∈ {10, 20, 50} days by minute-of-day; regression window ∈ {60, 120, 250} days (rolling, refit monthly); entry threshold on predicted |R| in units of trailing σ ∈ {0.1, 0.25, 0.5}; hold = 1 bar vs 2 bars.
- **Time-series HVRP:** bar ∈ {session, RTH-only day}; reference N ∈ {20, 49 (paper), 100}; cutoff ∈ {5%, 10% (paper), 20%}; direction ∈ {always long, with formation-day return, against it}; hold ∈ {1, 5, 10, 20 (paper)} days; roll mask ∈ {0, ±2, ±5} days.
- **BVC imbalance / VPIN / Kyle λ / Amihud regime filter:** bar type ∈ {5-min, 15-min, volume bars at 50/day (paper)}; σ_Δp window ∈ {50, 250} bars; W ∈ {25, 50, 250, 1000} bars (paper range); filter rule ∈ {tercile of feature → enable momentum vs mean-reversion family}; control ∈ {with/without realized-vol orthogonalization}.
- **Volume-filtered intraday momentum (add-on):** first-window length ∈ {15, 30, 60} min; volume ratio vs trailing 20-day same window ∈ {>1, >1.25, >1.5}.
- **VWAP:** anchor ∈ {RTH open, Globex open (18:00 ET), rolling N bars}; band ∈ {0, 0.25σ, 0.5σ}; mode ∈ {trend (above → long), reversion (fade |dev| > kσ)}; exit ∈ {cross back, close}.

### Gaps
- None of the sources supplies cost-adjusted futures P&L to calibrate realistic thresholds. The ES/NQ tick cost (about 0.25-0.5 tick slippage + fees) should be added by the user. Burst-reversal trades of about 5-10 bps net would be marginal after costs on ES (tick ≈ 0.5 bp at 5000+), so the larger-move/high-volume cells are the only plausible ones.
