# Purdue Papers Supply Three Untested Signal Shapes

The three best less-mainstream Purdue candidates for the futures ablation suite are Huseyin Gulen's **price-path convexity** signal, the Kais group's **entropy-filtered OHLC pattern library**, and Boming Ning and Kiseop Lee's **empirical-mean-reversion-time (EMRT) spread trade**. Each conditions on something the suite has not tested yet. Convexity looks at the *shape* of a price path inside a window. The pattern library matches recent bars against a pruned set of historical templates, which makes it a nonparametric analog forecaster. EMRT builds a two-leg spread whose hedge ratio is chosen to make it revert as fast as possible. That is a different mechanism from MA crossovers, single-instrument mean reversion, noise bands and squeezes, which work on price levels, the size of a move, or volatility compression. All three have a Purdue author confirmed by a source that names the affiliation, and the researchers read the full text of all three. The evidence is uneven, though. Convexity rests on a 1963–2022 S&P 500 sample with positive out-of-sample R², which makes it the most credible pick. The pattern library reports 30–70% annual returns from a single out-of-sample year with no trading costs. The EMRT results come from one out-of-sample year on ten hand-picked stock pairs. Many of the better-known Purdue findings, such as turn of the month, night versus day returns and the January Barometer, are cheap calendar overlays. They are already widely traded, so they appear under the candidates that were not picked.

## How the three picks were chosen and how solid the sourcing is

The research covered four Purdue clusters: Daniels/Krannert finance (Gulen, McConnell, Cooper, Chakravarty, Saretto), Purdue Statistics (Kiseop Lee's group), Purdue Chemistry (Sabre Kais's group) and Purdue Agricultural Economics (Brorsen, Irwin, Lukac, Boyd, Mallory). Each pick had to meet three conditions. It needed a Purdue author confirmed from the paper or an institutional record. It had to be buildable from 1-minute OHLCV alone, without options, surveys or quote data. And it had to be mechanically different from the families already in the suite.

That last condition ruled out most of the Agricultural Economics work, even though it is the only Purdue research that tested trading rules directly on futures. The 1980s Lukac, Brorsen and Irwin systems were channel, moving-average and similar trend rules. Their edge also faded: a later data-snooping-corrected replication by Illinois authors found the best rules profitable in only **2 of 17 futures contracts** ([IDEAS](https://ideas.repec.org/a/wly/jfutmk/v30y2010i7p633-659.html)).

The sourcing for the three picks is better than for most of the field. Gulen and Woeppel's convexity paper was read as the accepted JFQA manuscript. The Gupta–Kais pattern paper was read as full text on OSTI, and both Ning–Lee arXiv papers were read as full PDFs. The other candidates mostly rest on abstracts, Purdue repository pages or secondary summaries, mainly from CXO Advisory and Alpha Architect. The table at the end marks which source type each one depends on.

## Pick 1: price-path convexity bets against the shape of the recent move

**Purdue affiliation.** The JFQA manuscript footnote lists "Gulen, hgulen@purdue.edu, Purdue University Daniels School of Business". Co-author Michael Woeppel is at Indiana Kelley ([JFQA accepted manuscript](https://jfqa.org/wp-content/uploads/2025/05/25822_Price-path-convexity.pdf)). Gulen is the head of the Daniels finance department. All figures in this section come from that full text.

**How it works.** Take N closing prices P1 to PN. Convexity is [(P1+PN)/2 − mean(P1..PN)] / [(P1+PN)/2], meaning the midpoint of the two endpoints minus the average price, scaled by the midpoint. A positive value means the path bows below the straight line joining its endpoints, so most of the move happened late in the window. A negative value, a concave path, means the move happened early and then flattened.

Two windows with the same net return can therefore give opposite signals. That is why the signal is new to the suite: none of the existing families uses the timing of a move inside a window. The authors' explanation is overextrapolation. Survey expectations rise with 21-day convexity, so investors push up prices after late, accelerating moves, and those prices later fall back. High convexity therefore predicts lower returns.

**What the researchers found.** In a time-series test on the S&P 500 index from **July 1963 to December 2022**, a one-standard-deviation rise in convexity went with a **0.40% lower next-month return**. In-sample R² was **0.85%**, the highest of the 15 Welch–Goyal predictors. Out-of-sample R² was **0.39% to 0.61%**, while nearly every other predictor came out negative.

The firm-level sort is stronger. Low-minus-high convexity quintiles earned **0.84% per month (t = 6.29)**, with factor alphas of 0.78% to 0.97% per month. The result also holds at short horizons that suit futures: a **10-day look-back with a 10-day hold earned 0.64% per 10 days (t = 7.31)**, and a **5-day look-back with a 5-day hold earned 0.37% per 5 days (t = 4.94)**. A double sort on convexity and past return shows the signal is not short-term reversal in disguise. It also holds in a 1926–1963 out-of-period sample and on bid-ask midpoints ([JFQA manuscript](https://jfqa.org/wp-content/uploads/2025/05/25822_Price-path-convexity.pdf)).

**Caveats that matter here.** First, the index result is monthly and the 5- and 10-day results are for individual stocks. Applying 5- to 10-day horizons to ES or NQ is an extrapolation, and no published test exists on any intraday bars or on commodity, rate or FX futures. Second, excluding March and April 2020 raised the coefficient by about 50% and roughly quadrupled out-of-sample R². COVID falls inside the 2018–2022 development period, so the dev-period funnel will understate the signal relative to validation, or show it as unstable. Third, a search of the full text found no transaction-cost or turnover analysis.

**What the ablation grid could look like.** The main control is a plain N-bar return-reversal rule at the same N and hold. If convexity does not beat it, the suite has only rediscovered mean reversion. Back-adjust with ratios rather than differences, because roll gaps distort the comparison between the endpoint midpoint and the window average.

| Parameter | Suggested grid | Ablation purpose |
|---|---|---|
| Look-back N | 5, 10, 21 daily RTH closes; intraday 20/40/60/120 bars at 5m, 15m, 30m, 60m | Daily matches the paper; intraday is untested extrapolation |
| Denominator | Endpoint midpoint vs window mean | Paper says the choice gives "nearly identical" results, so a cheap robustness check |
| Price transform | Level vs log price | Tests scale dependence on trending contracts |
| Signal form | Raw sign; rolling z-score at ±0.5/1.0/1.5 over 126 or 252 periods | Replaces the paper's cross-sectional quintile cut |
| Hold H | N/2, N, 2N, non-overlapping vs rolling | Paper uses hold equal to look-back |
| Direction | Long concave only, short convex only, both | Equity-index drift favours long-side tests |
| Use mode | Standalone vs filter on existing breakout/MR entries | Tests whether shape adds information to other families' entries |

## Pick 2: the entropy pattern library trades nearest-neighbour bar templates

**Purdue affiliation.** Rishabh Gupta and Sabre Kais are listed under the Department of Chemistry, Purdue. Co-authors Shivam Gupta and Jaskirat Singh are at EntropyX Labs and Softure Solutions. The paper is "Entropy-Assisted Quality Pattern Identification in Finance," *Entropy* 27, 430, April 2025 ([OSTI full text](https://www.osti.gov/pages/servlets/purl/3673261)). All figures here come from that full text. The paper was tested on **gold and GBPUSD**, which map to GC and, loosely, 6E. That makes it unusually close to the suite's instruments.

**How it works.** First, the method finds time segments that come before a large swing, for example ±15 gold points within the next two hours. Each segment is labelled Buy or Sell by the direction of that swing. A pattern is **8 consecutive 30-minute bars** encoded as a 32-dimensional vector of H−L, C−O, H−O and O−L. Each pattern is scored as α·(information gain) + (1−α)·(normalised historical PnL), with α = 0.8. Information gain measures how pure the Buy and Sell labels are among the pattern's neighbours in feature space.

Next comes pruning. Patterns are sorted by score, and a Buy template is accepted only if its L1 distance to every accepted Sell template is at least θ, and the same in reverse. On gold this cut 913 Buy and 1,004 Sell patterns down to **543 Buy and 655 Sell**.

In live trading, every 30 minutes the method computes the same vector over the last eight bars. If the vector is within a match threshold of a Buy template the rule goes long, and if it is within the threshold of a Sell template it goes short. Exits are a fixed target or stop, for example 12–18 gold points. This is the only Purdue candidate that learns its entry shapes from data rather than encoding them by hand. The authors note that the patterns "may or may not resemble well-known trading motifs".

**What the researchers found.** Patterns were extracted and tuned on 2017–2023 gold, with 2024 held out. Out-of-sample annual returns ranged from **30% to 60%** across target and stop settings, and GBPUSD in 2024 returned about **30% to 70%**. The authors state that "commissions, exchange fees, and slippage are not yet incorporated". They report no Sharpe ratio, drawdown or trade counts, only equity curves ([OSTI](https://www.osti.gov/pages/servlets/purl/3673261)).

These numbers are weak evidence. The test covers one year in which gold rallied strongly, a co-author has a commercial affiliation, and the paper leaves out the neighbourhood size, θ and the match threshold. The suite's dev/validation/holdout split is exactly the test this paper lacks. Extract the library on 2018–2022, freeze it, then score 2023–2024.

**What the ablation grid could look like.** Set swings, targets and stops in ATR units rather than fixed points so that one grid works across all ten contracts. The α parameter gives a ready-made ablation: α = 0 keeps the PnL score only, and α = 1 keeps the entropy score only. Two essential controls are a library with no pruning and a library of randomly drawn segments of the same size. If either matches the full method, the entropy machinery adds nothing.

| Parameter | Suggested grid | Ablation purpose |
|---|---|---|
| Bar size | 15m, 30m, 60m | Paper uses 30m |
| Window W | 4, 8, 12 bars | Paper uses 8 |
| Swing label | 1.5, 2, 3 × ATR within 1h, 2h, 4h | Replaces the ±15-point, 2-hour rule |
| Neighbourhood k | 10, 25, 50 | Not reported in the paper; must be swept |
| α | 0, 0.5, 0.8, 1.0 | Separates the entropy and PnL scoring |
| Overlap θ / match threshold | Distance quantiles (e.g. 5th, 10th, 20th pct) | Controls library size and trade frequency |
| Exit | Target and stop at 1–3 × ATR, plus a time stop | Paper uses fixed points |
| Library refresh | Frozen from dev vs rolling re-extraction | Tests decay |
| Controls | No pruning; random library | Shows whether the method adds value |

## Pick 3: EMRT spreads pick hedge ratios by how fast they revert

**Purdue affiliation.** Boming Ning and Kiseop Lee are both listed as "Department of Statistics, Purdue University" on "Advanced Statistical Arbitrage with Reinforcement Learning" (arXiv 2403.12180, 2024), with corresponding email ningb@purdue.edu ([arXiv PDF](https://arxiv.org/pdf/2403.12180)). The companion signature-stopping paper also lists both at Purdue Statistics ([arXiv PDF](https://arxiv.org/pdf/2309.16008)). Figures here come from the full texts.

**How it works.** The building block is the "important extremum". A point is an important minimum if it is the lowest point of some segment and both ends of that segment sit at least **C·s** above it, where s is the sample standard deviation. Important maxima are defined the same way, and the simulations use C = 2. EMRT is the average time from each important extremum back to a crossing of the sample mean.

The hedge ratio is set by fixing the first leg's coefficient at 1 and grid-searching the other leg over [−3, 3] in 0.01 steps. The chosen ratio is the one that **minimises EMRT**, subject to a variance cap M. This replaces the usual OLS or cointegration fit with "make the spread snap back fastest".

Trading then uses a tabular Q-learning policy. The state is the last l returns, each binned into four buckets at ±k. The actions are buy one, hold or sell one, and the reward is A_t·(θ − X_t) − c·|A_t|. Training runs on simulated Ornstein–Uhlenbeck paths, not on historical data.

For the suite, this is the first cross-instrument family. The natural spreads are ES–NQ, ES–RTY, ES–YM, NQ–RTY and GC–SI, and possibly ZN against ES. If the engine cannot yet hold two legs, the important-extremum detector alone could serve as a single-instrument swing filter. That fallback is weaker, because it brings the strategy back toward the mean-reversion family the suite has already tested.

**What the researchers found.** The test used ten US stock pairs on daily adjusted closes, with 2022 for formation and 2023 for out-of-sample trading. The RL policy usually beat the distance-method and OU baselines. MSFT–GOOGL returned **37.8% against 11.4% and 8.2%**, but on GE–BA the distance method won, 64.2% against 48.8%. Daily Sharpe ratios ranged from **0.051 to 0.138**, which works out to roughly 0.8 to 2.2 annualised by the √252 rule (a conversion made for this report, not by the authors). Maximum drawdown was 0% in 4 of the 10 pairs. That is implausible, and it comes partly from the strategy being long-only and holding to the end of the period ([arXiv PDF](https://arxiv.org/pdf/2403.12180)).

The companion paper replaces the Q-table with signature-based optimal stopping. Over 2022 on four pairs it beat a moving-average-band baseline on every pair, for example 42.5% against 9.6% on UAL–DAL. But it made only **5–7 trades per pair per year**, and GS–MS drawdown got worse, at −7.9% against −2.3% ([arXiv PDF](https://arxiv.org/pdf/2309.16008)). The paper also contradicts itself on the size of the state space: it says 4^l states, but for l = 4 it says "16 distinct states" rather than 256. None of this has been tested on futures, and the pairs were hand-picked from stocks that already moved together in-sample.

**What the ablation grid could look like.** The key ablation compares hedge ratios: the EMRT-minimising ratio against an OLS ratio and against 1:1 dollar-neutral, all with the same entry and exit rule. If EMRT shows no advantage there, the RL layer is unlikely to rescue it. Futures can short as easily as they can go long, so test both sides rather than only the paper's long-only setup.

| Parameter | Suggested grid | Ablation purpose |
|---|---|---|
| Pair | ES–NQ, ES–RTY, ES–YM, NQ–RTY, GC–SI, ZN–ES | Tests which co-movements carry the effect |
| Bar size | 15m, 60m, daily | Paper uses daily |
| Formation window | 3, 6, 12 months, rolled forward | Paper uses one year |
| Extremum C | 1.5, 2, 2.5 | Swing significance |
| Hedge method | EMRT-min vs OLS vs 1:1 notional | Isolates the paper's contribution |
| Variance cap M | 2–3 levels | Stops EMRT from picking tiny, noisy spreads |
| Entry/exit | ±0.5/1.0/1.5 σ entry, exit at mean; vs Q-policy with l ∈ {2,3,4}, k ∈ {0.5,1} σ | Separates the RL policy from simple bands |
| Side | Long-only vs both | Paper is long-only |

## Other Purdue candidates found but not picked

The calendar and session effects have the best-established Purdue sources, but they are widely known and work as overlays more than standalone families. McConnell and Xu found that essentially all market excess return over 1926–2005 came in the **four-day turn-of-month window**, at about 0.15% per day against roughly zero on other days, in 31 of 35 countries ([CFA Institute](https://rpc.cfainstitute.org/research/financial-analysts-journal/2008/equity-returns-at-the-turn-of-the-month); [Purdue CIBER WP 43](https://docs.lib.purdue.edu/ciberwp/43)). Cliff, Cooper and Gulen found that the 1993–2006 US equity premium accrued overnight, with a weak first trading hour ([CXO Advisory](https://cxoadvisory.com/?p=1377)). An untested but cheap idea combines the two: hold only overnight, and only inside the turn-of-month window. Cooper's volume-conditioned weekly reversal is the most interesting runner-up. Large moves on *falling* volume reverse more strongly ([IDEAS](https://ideas.repec.org/a/oup/rfinst/v12y1999i4p901-35.html)). It was set aside because it is mean reversion with a volume filter, and only the abstract was reached.

| Candidate | Purdue author (status) | Why not picked | Source depth |
|---|---|---|---|
| Turn of month (McConnell & Xu 2008) | McConnell, Xu (CIBER WP lists both at Purdue) | Well known; overlay rather than a family | Abstract / working-paper page |
| Night vs day plus first-hour fade (Cliff, Cooper & Gulen) | Gulen (not confirmed on paper header) | Widely traded; reported decay after 2006 | Secondary summary |
| Volume-filtered reversal (Cooper 1999, RFS) | Cooper (Krannert, per working version) | Close to existing MR family; thresholds unknown | Abstract |
| Absolute-strength momentum (Gulen & Petkova) | Gulen | Cross-sectional stock result; time-series port is speculative | Summaries only ([Alpha Architect](https://alphaarchitect.com/2015/10/absolute-strength-momentum-investing-strategy/)) |
| Market-state momentum filter (Cooper, Gutierrez & Hameed 2004) | Cooper (Krannert at the time) | Regime filter, not a strategy; failed a Spanish replication | Summary ([typeset](https://typeset.io/pdf/market-states-and-momentum-4wtc7g4rqv.pdf)) |
| January Barometer long/T-bill rule (Cooper, McConnell & Ovtchinnikov) | McConnell (Krannert, on PDF) | One decision a year, so about 15 observations in the data | Full text ([Purdue PDF](https://business.purdue.edu/faculty/mcconnell/publications/Whats-the-best-way.pdf)) |
| Signature optimal-stopping exits (Ning, Chakraborty & Lee) | Ning, Lee (Purdue Statistics) | Heavy to build; could become an exit module for Pick 3 later | Full text |
| Lukac/Brorsen/Irwin trend systems; Boyd; Retter 2022 | Brorsen, Irwin, Boyd (Purdue Ag Econ) | Mainstream MA/channel rules; edge decayed | Mixed; Retter full text |
| USDA-report intraday windows (Hu & Mallory 2022) | Mallory (Purdue Ag Econ) | Descriptive grain study; an EIA/CPI port would not be Purdue-tested | Summary |
| Option IV gap, DOX timing, ISO order flow, option information share | Saretto, Gulen/Cassella, Chakravarty | Need options, surveys or TAQ data | Abstracts |

## Conclusion

Purdue's most useful contribution here is a set of new conditioning variables rather than ready-made strategies. Convexity conditions on when a move happened, the pattern library on the bar-by-bar shape of the move, and EMRT on how fast a spread reverts. None of these depends on how far price moved or where it sits against a band, which is what every family the suite has tested so far relies on. So even a pick that fails on its own may help as a filter on existing breakout and mean-reversion entries. Convexity is the cheapest to test in that role and is worth running first.

The weak point in all three is the same one the suite was built to handle. Each paper's headline result rests on a short or favourable test window, and none reports costs that fit 1-minute futures execution. The main thing a funnel adds is the control comparisons: convexity against plain reversal, the entropy library against a random library, and EMRT hedge ratios against OLS. If a pick does not beat its control, the Purdue mechanism added nothing, however good the dev-period numbers look.
