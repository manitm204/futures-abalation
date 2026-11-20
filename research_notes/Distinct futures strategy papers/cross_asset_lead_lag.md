# Cross-asset, lead-lag, carry and cross-sectional strategy papers for a 9-market US futures universe (ES, NQ, RTY, YM, CL, GC, 6E, 6J, ZN)

Research scope note: about 18 tool calls were used. Full texts were read for Krohn-Mueller-Whelan (JF 2024, via the Bank of Canada working paper), Koijen-Moskowitz-Pedersen-Vrugt (JFE 2018 accepted manuscript), and Bennett-Cucuringu-Reinert (arXiv 2022). Pitkäjärvi-Suominen-Vaittinen and Driesprong-Jacobsen-Maat were reached only through abstracts and secondary summaries, because the full texts returned 403. Their exact rules are flagged as unverified below.

## Q1. Which peer-reviewed or strong working papers give cross-asset, lead-lag, carry or cross-sectional families that fit these 9 markets and differ from what is already tested?

### Takeaway
Six papers, from strongest fit to weakest:
1. **Krohn-Mueller-Whelan (JF 2024): FX fix "W-pattern" in 6E and 6J.** This is an intraday cross-session family. It needs 1-minute data.
2. **Pitkäjärvi-Suominen-Vaittinen (JFE 2020): cross-asset TSMOM.** ZN's past return sets the ES/NQ/RTY/YM position, and the negative of equity's past return sets the ZN position.
3. **Driesprong-Jacobsen-Maat (JFE 2008): oil predicts equities with a lag.** CL's past return sets the equity-index position.
4. **Koijen-Moskowitz-Pedersen-Vrugt (JFE 2018): carry.** This needs back-month contracts.
5. **Asness-Moskowitz-Pedersen (JF 2013): rank-weighted cross-sectional momentum**, plus Kwon-Kang-Yun (FRL 2020) weekly short-term momentum.
6. **Bennett-Cucuringu-Reinert (arXiv 2022): data-driven lead-lag network signal.** It was built for large stock universes, so for these 9 markets only the pairwise lead-lag idea carries over.

### Cited Findings

**A. Krohn, Mueller and Whelan, "Foreign Exchange Fixings and Returns Around the Clock," *Journal of Finance* 79(1), 2024, pp. 541-578**
Links: [RePEc](https://econpapers.repec.org/RePEc:bla:jfinan:v:79:y:2024:i:1:p:541-578); [Bank of Canada SWP 2021-48 PDF](https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf)
- **Finding.** The USD appreciates in the run-up to the FX fixes and depreciates afterwards, giving a W-shaped return pattern around the clock. The authors attribute this to dealer inventory and pre-hedging of unconditional USD demand at the fixes. — [BoC WP](https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf)
- **Five ET windows used in the paper:**

  | Window | Name | ET times |
  |---|---|---|
  | (i) | pre-Tokyo | 5:00 pm–8:55 pm (7:55 pm outside DST) |
  | (ii) | post-Tokyo | 8:55 pm–2:00 am |
  | (iii) | pre-ECB | 2:00 am–8:15 am |
  | (iv) | ECB-to-London | 8:15 am–11:00 am |
  | (v) | post-London | 11:00 am–5:00 pm |

  Fix times: Tokyo 9:55 am JST, ECB 2:15 pm CET, London WM/R 4:00 pm London time. — [BoC WP](https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf)
- **Strategy rules (Eqs. 3-4):**
  - Tokyo leg: return = −Δs(pre-T) + Δs(post-T). Short the foreign currency (long USD) before the Tokyo fix, then flip to long the foreign currency after it.
  - Europe leg: return = −Δs(pre-E) + Δs(post-L). Long USD 2:00–8:15 am ET, flat 8:15–11:00 am, then short USD 11:00 am–5:00 pm ET.
  - The ECB-to-London window is skipped because it has no clear direction. — [BoC WP](https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf)
- **Win rates.** For the Tokyo reversal, about 55% (CHF) to about 60% (dollar portfolio) of days are positive. For the Europe window the range is about 51% to 56%. — [BoC WP](https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf)
- **Gross returns.** Ignoring costs, $1 invested in 1999 grows by 2019 as follows. — [BoC WP](https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf)

  | Window | JPY | EUR | GBP | USD basket |
  |---|---|---|---|---|
  | Tokyo | $12 | $9 | $5 | $9 |
  | Europe | ~6% total loss | $27 | $14 | $6 |

  The yen is the exception: it appreciates during Asian hours and moves the opposite way after London.
- **Annualized gross returns, long USD pre-Tokyo then reversed:** EUR 10.44%, GBP 7.94%, JPY 12.0%. — [BoC WP](https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf)
- **Effect of costs (Table IX, spot bid-ask, 1999-2019):**
  - With the full indicative bid-ask spread, most windows turn negative.
  - With 50% of the spread, returns are EUR 2.65%, GBP 0.51%, JPY 2.73% for the Tokyo leg.
  - With 50% of the spread, EUR earns 8.64% pre-ECB and 5.46% post-London.
  - Sharpe ratios at the 50% spread are 0.12 to 1.03. Gross Sharpe ratios reach about 1.2 to 2.0. — [BoC WP](https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf)
- **Decay in the Tokyo leg.** Net of 50% of the spread, the Tokyo reversal was flat to positive until about 2007, gave back gains until about 2013, then turned negative for EUR and GBP and flat for JPY. The London reversal net of costs stayed strong: $1 grows to $6.08 (EUR) and $3.13 (GBP). — [BoC WP](https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf)
- **Futures check.** The reversal patterns also appear in CME FX futures (data from 2006). CME futures order imbalances are unrelated to the reversals. Reversal returns are higher when volatility is high and are predictable with the VIX. — [BoC WP](https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf)

**B. Pitkäjärvi, Suominen and Vaittinen, "Cross-asset signals and time series momentum," *JFE* 136(1), 2020, pp. 63-85**
Links: [DOI 10.1016/j.jfineco.2019.02.011](https://doi.org/10.1016/j.jfineco.2019.02.011); [RePEc](https://ideas.repec.org/a/eee/jfinec/v136y2020i1p63-85.html)
- **Finding.** Past bond returns positively predict future equity-index returns. Past equity returns negatively predict future bond returns. — [RePEc abstract](https://ideas.repec.org/a/eee/jfinec/v136y2020i1p63-85.html)
- **Performance.** A diversified cross-asset TSMOM portfolio has a Sharpe ratio about 45% higher than standard TSMOM. One summary says it is almost 70% higher than a similarly diversified buy-and-hold portfolio. Controlling for the cross-asset portfolio makes standard TSMOM alpha insignificant. — [RePEc](https://ideas.repec.org/a/eee/jfinec/v136y2020i1p63-85.html); [Aalto news](https://www.aalto.fi/news/finance-paper-accepted-to-be-published-in-the-journal-of-financial-economics); [IBKR/Alpha Architect summary](https://www.interactivebrokers.com/campus/ibkr-quant-news/cross-asset-signals-and-time-series-momentum/)
- **Sample.** Bond and equity indices for 20 developed countries, January 1980 to December 2016. The authors explain the effect with slow-moving capital. When both momentum signals are positive at the same time, industrial production and investment grow faster and unemployment is lower over the next 12 months. — [IBKR summary](https://www.interactivebrokers.com/campus/ibkr-quant-news/cross-asset-signals-and-time-series-momentum/)

**C. Driesprong, Jacobsen and Maat, "Striking oil: Another puzzle?," *JFE* 89(2), 2008, pp. 307-327**
Links: [RePEc](https://ideas.repec.org/a/eee/jfinec/v89y2008i2p307-327.html); [working paper, ERIM 2003](https://ideas.repec.org/p/ems/eureri/1017.html)
- **Finding.** Oil price changes strongly predict future stock-market returns. A rise in oil prices lowers future returns. The paper reads this as investors underreacting to oil information. — [RePEc](https://ideas.repec.org/a/eee/jfinec/v89y2008i2p307-327.html)
- **Scope and robustness.** Predictability holds in 12 of 18 developed markets and the world index, with similar results in emerging markets. It is robust across sample periods and oil measures, and to the January and Halloween effects. The authors find no evidence that time-varying risk premia explain it. — [ERIM abstract](https://ideas.repec.org/p/ems/eureri/1017.html)
- **US industry follow-up.** Fan and Jahan-Parvar (2009) find negative coefficients on lagged oil returns at the US industry level, in line with Driesprong's reported value of -0.086. At industry level the predictability does not last beyond a one-month lag. — [MPRA 15670](https://mpra.ub.uni-muenchen.de/15670/1/MPRA_paper_15670.pdf)

**D. Koijen, Moskowitz, Pedersen and Vrugt, "Carry," *JFE* 127(2), 2018, pp. 197-225**
Links: [DOI 10.1016/j.jfineco.2017.11.002](https://doi.org/10.1016/j.jfineco.2017.11.002); [accepted manuscript PDF](https://research-api.cbs.dk/ws/files/57294842/lasse_heje_pedersen_et_al_carry_acceptedmanuscript.pdf)
- **Carry definitions.** General definition: Ct = (St − Ft)/Ft, the return if prices stay unchanged.

  | Asset class | Carry equals |
  |---|---|
  | FX | Interest-rate differential |
  | Equity | Expected dividend yield minus the local risk-free rate |
  | Commodity | Convenience yield net of storage, i.e. the basis |
  | Bonds | Yield spread plus roll-down |

  — [manuscript](https://research-api.cbs.dk/ws/files/57294842/lasse_heje_pedersen_et_al_carry_acceptedmanuscript.pdf)
- **Back-month data needed.** Equity carry uses a synthetic 1-month futures price interpolated between the two nearest-to-maturity contracts. Commodity and bond carry also interpolate futures prices. **So carry needs at least the front and second-month contracts.** — [manuscript](https://research-api.cbs.dk/ws/files/57294842/lasse_heje_pedersen_et_al_carry_acceptedmanuscript.pdf)
- **Portfolio construction (Eq. 19).** Weights are wt = zt·(rank(Ct) − mean rank), scaled so the long and short legs are each $1. All assets are held, weighted by rank. Rebalanced monthly. — [manuscript](https://research-api.cbs.dk/ws/files/57294842/lasse_heje_pedersen_et_al_carry_acceptedmanuscript.pdf)
- **Performance (1972-2012 sample):**
  - Cross-sectional carry: Sharpe about 0.8 per asset class on average, 1.2 diversified.
  - Carry-timing (time series): Sharpe about 0.6 on average, 0.9 for the global version.
  - Passive exposure to the asset classes: Sharpe 0.13 on average.
  - Smoothed "carry1-12" signal: global Sharpe 1.12.
  - Largest drawdowns come in global recessions. Currency carry shows crash risk and negative skew.

  — [manuscript](https://research-api.cbs.dk/ws/files/57294842/lasse_heje_pedersen_et_al_carry_acceptedmanuscript.pdf)
- **Equity universe.** The equity carry universe is country index futures (US S&P 500, Canada, UK, France, Germany and others). — [manuscript](https://research-api.cbs.dk/ws/files/57294842/lasse_heje_pedersen_et_al_carry_acceptedmanuscript.pdf)

**E. Basis-momentum: Boons and Prado, "Basis-Momentum," *Journal of Finance* 74(1), 2019**
- **Signal.** Basis-momentum is the difference between momentum in the first- and second-nearby futures. It decomposes into average curvature and changes in the slope of the futures curve. It beats basis and momentum in predicting commodity spot and term premiums, in both the time series and the cross section, from 1959 onward. — [CEPR/BI version](https://www.bi.no/link/af8ef92ed3ee4896bc0cea7fc855b1ba.aspx); [NBER conf paper](https://conference.nber.org/conf_papers/f89296/f89296.pdf) (the search-result summary was not fully verified against the text)
- **Back-month data needed.** It requires first- and second-nearby contract series. It is built for commodities (about 20 or more), and only CL and GC are commodities here. — same sources

**F. Cross-sectional momentum: Asness, Moskowitz and Pedersen, "Value and Momentum Everywhere," *JF* 68(3), 2013; plus Kwon, Kang and Yun (2020)**
- **Weighting.** Koijen et al. credit AMP (2013) with the rank-based weighting scheme above. AMP use it for momentum and value across country equity-index futures, bond futures, currencies and commodities. Rank weighting is more stable than signal weighting because it puts less extreme weight on outliers. — [Carry manuscript](https://research-api.cbs.dk/ws/files/57294842/lasse_heje_pedersen_et_al_carry_acceptedmanuscript.pdf)
- **Weekly commodity momentum.** Kwon, Kang and Yun, *Finance Research Letters* 35 (2020), rank commodity futures weekly. They find strong **short-term momentum** rather than short-term reversal, and it survives controls for carry, equity momentum and hedging pressure. — [RePEc](https://ideas.repec.org/a/eee/finlet/v35y2020ics1544612319308980.html)
- **Short-horizon reversal (secondary source).** A Quantpedia summary of a multi-asset study reports significant reversal at very short horizons. Its universe is 24 commodities, 12 currency pairs, 9 equity indices and 13 bond futures. This was not verified against the original paper. — [Quantpedia](https://quantpedia.com/Screener/Details/118)

**G. Bennett, Cucuringu and Reinert, "Lead-lag detection and network clustering for multivariate time series with an application to the US equity market," arXiv:2201.08283 (2022)**
Link: [arXiv](https://arxiv.org/pdf/2201.08283)
- **Method.**
  1. Compute pairwise lead-lag metrics, based on cross-correlation of lagged returns, over a yearly look-back.
  2. Build a directed network and cluster it.
  3. Keep only the leader→lagger cluster pairs whose historical "flow" exceeds a threshold c.
  4. Signal: fit a linear regression of the lagger cluster's return on the leader's lagged returns.
  5. Scale the signal by a 21-day rolling volatility estimate.
  6. Smooth lagged returns over a week. — [arXiv](https://arxiv.org/pdf/2201.08283)
- **Results (daily US equities).** Sharpe 0.62 before costs (permutation p about 1/201), versus 0.40 for the S&P 500. Correlation with the market is 0.04, and the mean daily return is 2.4 bp. **Performance decays after 2012.** Costs are ignored, though turnover is low because of the weekly smoothing. — [arXiv](https://arxiv.org/pdf/2201.08283)

**Counter-evidence on cross-asset lead-lag at daily frequency**
- **Weak cross-serial correlation.** Moskowitz, Ooi and Pedersen ("Time series momentum," JFE 2012) report that negative cross-serial correlations (lead-lag across securities) are negligible in their 58-futures universe. An asset's own lagged return is the main predictor. — [MOP PDF](https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf) (as summarized by the search tool)
- **Weak TSMOM evidence.** Huang, Li, Wang and Zhou ("Time series momentum: Is it there?", JFE 2020) find little asset-by-asset evidence of TSMOM in or out of sample. Only 3 assets have significant out-of-sample R². — [SMU repository](https://ink.library.smu.edu.sg/lkcsb_research/6550); [Alpha Architect](https://alphaarchitect.com/2020/03/an-empirical-challenge-for-trend-following/)

**Intraday cross-market lead-lag**
- **Treasury and equity futures.** Dobrev and Schaumburg (Atlanta Fed / AEA 2018) measure high-frequency lead-lag between Treasury and equity markets. Most cross-market activity happens in futures rather than cash. Theirs is a measurement paper, not a trading strategy. — [Atlanta Fed PDF](https://www.atlantafed.org/-/media/documents/news/conferences/2018/1018-financial-stability-implications-of-new-technology/papers/dobrev-schaumburg_high-frequency-cross-market-trading.pdf)
- **Chinese index futures.** Li, Chen and Liu (arXiv 2501.03171, 2025) find that a "lead-lag spread" signal predicts the leading asset's returns and stays profitable after costs. This covers Chinese index futures across maturities, not US markets. — [arXiv](https://arxiv.org/pdf/2501.03171)

### Inferences
- **6E/6J fix reversal (A) is the most distinctive candidate.** It is calendar and clock based, not price-pattern based. It needs the 1-minute data, and it involves no indicator the user already tests.
- **Futures session conflict for (A).** CME Globex has a daily halt from 5:00 to 6:00 pm ET, so the paper's pre-Tokyo window (5:00–8:55 pm) can only be traded from 6:00 pm. The window start should be an ablation parameter.
- **Sign convention for (A).** 6E and 6J are quoted as USD per foreign unit. Long USD therefore means short 6E or 6J.
- **Expected performance for (A).** The net Tokyo leg decayed after about 2013 in spot. Expect the post-London leg (short USD = long 6E from 11:00 am to 5:00 pm ET) to be the more robust part.
- **Yen leg for (A).** The yen goes the opposite way after London, so the yen Europe leg is a natural negative control.
- **Pitkäjärvi (B) maps directly onto the universe.** ZN is the "bond market" and ES/NQ/RTY/YM are the "equity markets". It needs only front-month data. With one country (the US), the 20-country diversification behind the reported Sharpe ratio is lost, so expect a much lower Sharpe ratio.
- **Driesprong (C) is a sign-flipped cross-asset signal.** Equity position = −sign(CL return over the past L days). Front-month CL roll gaps have to be handled with a back-adjusted series, or the roll will contaminate the signal.
- **Carry (D) and basis-momentum (E) need the second contract.** Databento sells individual contract symbols (e.g., `CL.c.1`/`CL.c.2` continuous by rank), so this should be a feasible download. It should be confirmed against the user's dataset.
- **FX carry without back months.** For 6E/6J, carry could be approximated from the futures-spot basis, or from rates data (e.g., the EUR, JPY and USD 3-month rates). Neither is in the current dataset.
- **Universe size for carry and cross-sectional momentum.** These papers rank within an asset class: about 10 to 24 assets in commodities and about 10 countries in equities and bonds. The 9 markets are 4 highly correlated US equity indices, 1 bond, 2 FX and 2 commodities, so cross-sectional ranking is close to degenerate.
- **Workable cross-sectional variants:**
  - Cross-asset-class ranking on vol-scaled returns (e.g., hold the top 3 and short the bottom 3 of the 9).
  - Rank within the equity block only (ES/NQ/RTY/YM rotation).
  - Note that the equity-block rotation overlaps conceptually with the EMRT spreads the user already runs.
- **Bennett et al. (G) shrinks to pairwise rules.** With 9 assets the clustering step is pointless. What survives is a pairwise lead-lag score (e.g., lagged cross-correlation of 5- to 60-minute returns) used to choose leader→lagger pairs on a rolling basis, then trading the lagger. Intraday 1-minute data could be valuable here, since the daily signal decayed after 2012.

### Gaps
- **Exact Pitkäjärvi rules not verified.** The look-back (1-month vs 12-month), signal form (sign vs magnitude), volatility scaling, rebalance frequency and per-horizon Sharpe ratios could not be read because the full text was blocked (403). From memory and unverified: the paper uses monthly rebalancing with 1- to 12-month look-backs and builds positions as in Moskowitz-Ooi-Pedersen with volatility scaling. Check this against the JFE text before implementing.
- **Driesprong lag and strategy figures not verified.** The paper's lag structure (whether daily or weekly data show a lag of a few trading days) and its trading-strategy Sharpe ratio were not verified. The abstract gives no lag.
- **No post-2018 replication found for B, C or D.** Specifically: bonds predicting equities, oil predicting equities, and the carry factor.
- **No paper found for some requested families:**
  - Bond futures intraday returns predicting equity intraday returns.
  - Gold–equity hedging-flow strategies.
  - Risk-on/risk-off timing.
- **Sources not reached:**
  - Rapach-Strauss-Zhou (JF 2013, US leading international markets).
  - Hong-Torous-Valkanov (JFE 2007, industries leading the market).
  - AQR/Man research on small-universe factor rotation.
  - Ranaldo (2009) on FX time-of-day segmentation.

## Q2. Exact construction, natural ablation grids, and minimum universe

### Takeaway
The cleanest grids are:
- **FX fix:** window boundaries × leg on/off × currency.
- **Cross-asset TSMOM and oil:** look-back L × holding H × signal transform (sign / z-score / volatility-scaled) × execution lag.
- **Carry and cross-sectional momentum:** signal look-back × rank vs top/bottom-k weighting × rebalance frequency.

### Cited Findings
- **FX fix parameters to vary.** The paper's window cut-points are 8:55 pm, 2:00 am, 8:15 am and 11:00 am ET, with the day ending at 5:00 pm ET. They follow Tokyo, ECB and London fix times and shift with DST. — [BoC WP](https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf)
- **FX fix costs.** Gross versus 50%-spread results differ sharply, so costs and slippage per turn are the key ablation axis. — [BoC WP](https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf)
- **FX fix volatility filter.** Reversal returns are higher in high-volatility regimes and predictable with the VIX. This supports a volatility-regime filter. — [BoC WP](https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf)
- **Carry and cross-sectional portfolio parameters.** Rank weights versus top/bottom-x% equal weights, monthly rebalancing, and a 1-month carry versus a smoothed 12-month average ("carry1-12"). — [Carry manuscript](https://research-api.cbs.dk/ws/files/57294842/lasse_heje_pedersen_et_al_carry_acceptedmanuscript.pdf)
- **Weekly momentum ranking.** Short-term momentum in commodity futures is tested with several ranking periods at weekly frequency. — [Kwon-Kang-Yun RePEc](https://ideas.repec.org/a/eee/finlet/v35y2020ics1544612319308980.html)
- **Lead-lag parameters.** Yearly look-back for estimating lead-lag, a flow threshold c, 21-day volatility normalization, and weekly smoothing. — [arXiv 2201.08283](https://arxiv.org/pdf/2201.08283)

### Inferences
Proposed ablation grids:

1. **FX fix reversal (6E, 6J, optionally the inverse-ES hedge).**

   | Parameter | Values |
   |---|---|
   | Legs | {Tokyo only, Europe only, both, post-London only} |
   | Window start offset | {0, ±15, ±30 min} |
   | Tokyo window start | {6:00 pm, 6:30 pm} |
   | Currency | {6E, 6J, both} |
   | Volatility filter | {none, trailing 20-day realized vol > median} |
   | Cost per turn | {1, 2 ticks} |

   Negative control: the 6J Europe leg.

2. **Bond→equity cross-asset TSMOM.**

   | Parameter | Values |
   |---|---|
   | Signal | sign or z-score of ZN return over L ∈ {1, 5, 21, 63, 252} days |
   | Target | ES/NQ/RTY/YM position, entered next open or next close |
   | Holding H | {1, 5, 21} days |
   | Reverse leg | ZN position = −sign(ES return over L) |
   | Volatility target | {off, 10% annual} |
   | Variants | intraday version: ZN return over the last {30, 60, 120} min → ES next {30, 60} min |

   The intraday version is speculative. No paper was found that confirms it.

3. **Oil→equity.**

   | Parameter | Values |
   |---|---|
   | Signal | −sign(CL back-adjusted return over L ∈ {1, 3, 5, 10, 21} days) |
   | Execution lag | {0, 1, 2} days |
   | Holding | {1, 5, 21} days |
   | Target | {ES, RTY} |
   | Threshold | |CL z-score| > {0, 1, 2} |

4. **Cross-sectional momentum or reversal across all 9 markets (vol-normalized).**

   | Parameter | Values |
   |---|---|
   | Look-back | {1d, 5d, 21d, 126d, 252d-skip-21d} |
   | Weighting | rank-weighted vs long top 3 / short bottom 3 |
   | Rebalance | {daily, weekly, monthly} |
   | Universe | {all 9, one representative equity (ES) + others = 6 markets} |

5. **Carry (only with second-month data).**

   | Parameter | Values |
   |---|---|
   | Carry definition | (F1 − F2)/F2 annualized by days between expiries |
   | Mode | cross-sectional rank vs time-series sign |
   | Smoothing | 1m vs 12m average |

   Basis-momentum adds the 12-month return of F1 minus that of F2, for CL and GC only.

6. **Rolling pairwise lead-lag.**

   | Parameter | Values |
   |---|---|
   | Bar size | {5, 15, 60 min, daily} |
   | Look-back for lead-lag score | {60, 120, 250} days |
   | Number of lags | {1, 2, 5} |
   | Flow threshold c | top {1, 3} pairs |
   | Trading | the lagger in the direction of the leader's last bar(s) |

**Universe-size verdict:**
- Families 1 to 3 and 6 are fine with 9 markets.
- Families 4 and 5 assumed 10 to 24 assets per class. With 9 markets spanning 5 asset classes, power will be low and results noisy, so treat them as exploratory.

### Gaps
- No source specifies optimal look-backs for a single-country bond→equity implementation.
- No source found tests a 9-asset cross-sectional futures momentum universe directly.
- No information found on whether CME 6E/6J futures spreads make the Tokyo leg profitable after 2019. The paper's cost analysis uses spot indicative quotes up to 2019.
