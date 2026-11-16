# Purdue-affiliated technical-analysis, pattern and quant/ML trading strategies

Scope note: about 20 search/fetch calls. Full text was read (PDF extracted) for 4 items: Ning & Lee 2024 (RL stat arb), Ning, Chakraborty & Lee 2023/24 (signature optimal stopping), Gupta, Gupta, Singh & Kais 2025 (entropy pattern library), and Retter 2022 (Purdue Ag Econ honors thesis). The other items rest on abstracts and catalog records only. ECE, CS and IE searches turned up no Purdue price-based trading-rule paper, so the coverage gap is real. It does not mean such papers were checked and judged weak.

## Q1. Which Purdue-affiliated researchers have published uncommon price-based trading rules or market patterns?

### Takeaway
There are three clusters. (1) Kiseop Lee's group in Purdue Statistics, with PhD student Boming Ning: model-free statistical arbitrage with empirical mean-reversion time, RL entry/exit, signature optimal stopping, multi-pair diversification, and limit-order-book forecasting. (2) Sabre Kais's quantum/chemistry group in Purdue Chemistry: an entropy-filtered OHLC pattern library on gold and GBPUSD, plus entropy-corrected GBM. (3) Purdue Agricultural Economics in the 1980s (B. Wade Brorsen, Lukac, Irwin, Boyd): classic computer-guided technical trading systems on commodity futures, plus a 2022 honors-thesis update.

### Cited Findings
**Purdue Statistics (Kiseop Lee, Boming Ning)**
- "Advanced Statistical Arbitrage with Reinforcement Learning", Boming Ning and Kiseop Lee, both listed as "Department of Statistics, Purdue University". arXiv:2403.12180, March 2024, q-fin.ST. The corresponding author email is ningb@purdue.edu. — [arXiv PDF](https://arxiv.org/pdf/2403.12180)
- "Optimal Entry and Exit with Signature in Statistical Arbitrage", Boming Ning and Kiseop Lee (Dept. of Statistics, Purdue) with Prakash Chakraborty (Industrial & Manufacturing Engineering, Penn State). arXiv:2309.16008, v1 Sept 2023, v4 March 2024, q-fin.CP. — [arXiv PDF](https://arxiv.org/pdf/2309.16008)
- Kiseop Lee, Tim Leung and Boming Ning, a framework for diversified portfolios of multiple pairs-trading strategies. *Risks* 11(5):93, 2023. — [IDEAS/RePEc](https://ideas.repec.org/a/gam/jrisks/v11y2023i5p93-d1148312.html)
- Purdue Graduate School thesis "Quantitative Methods of Statistical Arbitrage" (Purdue HAMMER/Figshare item 25654227). Per the search snippet, chapter 2 proposes the diversified multi-pair framework. It appears to be Ning's dissertation collecting the papers above, but the author could not be confirmed because the page returned 403. — [Purdue HAMMER](https://hammer.purdue.edu/articles/thesis/Quantitative_Methods_of_Statistical_Arbitrage/25654227)
- "Attention-Based Reading, Highlighting, and Forecasting of the Limit Order Book", Jiwon Jung and Kiseop Lee (Purdue Statistics). It applies a Spacetimeformer attention model to Level-5 LOB snapshots at millisecond resolution over one trading day. It forecasts the book and is not an OHLCV rule. — [arXiv HTML](https://arxiv.org/html/2409.02277v2)

**Purdue Chemistry (Sabre Kais group)**
- "Entropy-Assisted Quality Pattern Identification in Finance", Rishabh Gupta (Dept. of Chemistry, Purdue), Shivam Gupta (EntropyX Labs), Jaskirat Singh (Softure Solutions) and Sabre Kais (Dept. of Chemistry, Purdue, and ECE, NC State). *Entropy* 2025, 27, 430, published 16 April 2025. — [OSTI full text](https://www.osti.gov/pages/servlets/purl/3673261); [DOI](https://doi.org/10.3390/e27040430)
- "Entropy corrected geometric Brownian motion" (EC-GBM), by R. Gupta, E. A. Drzazga-Szczęśniak, S. Kais (Purdue Chemistry) and D. Szczęśniak. arXiv 2403.06253; *Scientific Reports*, Nov 2024. It is a forecasting model and not a trading rule. — [arXiv](https://arxiv.org/pdf/2403.06253); [DOAJ](https://doaj.org/article/bee7d5987faf4857af21fd7d15976c57)

**Purdue Agricultural Economics (technical trading on futures)**
- Milton S. Boyd, PhD dissertation "Disequilibrium in commodity futures markets", Purdue University, advisor Brorsen. — [Purdue e-Pubs](https://docs.lib.purdue.edu/dissertations/AAI9132426)
- Lukac, Brorsen & Irwin (1988), "A test of futures market disequilibrium using twelve different technical trading systems". — [Scilit](https://scilit.com/publications/c283eba5ed79a2127bb9f8b70eb70fe9). Lukac & Brorsen (1990), "A Comprehensive Test of Futures Market Disequilibrium", *Financial Review* 25(4):593–622. — [IDEAS](https://ideas.repec.org/a/bla/finrev/v25y1990i4p593-622.html)
- Irwin & Brorsen (1985), a Purdue working paper on technical trading systems that use only past prices (AAEA 1985 paper, per the search snippet). The PDF fetch returned 403. — [AgEcon Search](https://ageconsearch.umn.edu/record/278568/files/aaea-1985-045.pdf)
- Jaden C. Retter, "Technical Trading Systems in U.S. Commodity Futures Markets", Purdue Agricultural Economics undergraduate honors thesis (the PDF metadata dates it to 2022). — [Purdue Ag Econ PDF](https://ag.purdue.edu/department/agecon/_docs/undergraduate/thesis/jaden-retter_honors-thesis.pdf)

**Purdue Krannert (finance): no trading-rule papers found**
- Purdue CIBER working papers surfaced, such as Gulen & Mayhew on index futures and volatility, and a turn-of-the-month returns paper. None tests a price-based trading rule. — [Gulen & Mayhew CIBER WP](https://docs.lib.purdue.edu/ciberwp/144/); [Turn of the month CIBER WP](https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1042&context=ciberwp)
- Purdue e-Pubs dissertation: Chi Wai Law (2015), "A pure-jump market-making model for high-frequency trading". It is LOB market making with no directional OHLCV rule. — [Purdue e-Pubs](https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1401&context=open_access_dissertations)

### Inferences
- The most unusual and most portable Purdue rules are (a) the entropy-filtered nearest-neighbour OHLC pattern library (Kais group) and (b) the empirical-mean-reversion-time (EMRT) spread construction combined with a discretised-return-state Q-learning policy (Lee/Ning).
- Purdue's 1980s Ag Econ technical-trading work is historically important: it is the origin of the Lukac/Brorsen/Irwin line that Park & Irwin later extended. The rules it tests (channels, MA crossovers, parabolic) are mainstream.
- Lukac's Purdue affiliation in 1988 is inferred, not verified. Brorsen's Purdue affiliation is confirmed by the Boyd dissertation record.

### Gaps
- No Purdue ECE, CS, IE or Math paper with a concrete price-based trading rule turned up. Candidates not searched by name include Purdue IE/ECE faculty doing RL for trading and Purdue Math computational-finance faculty.
- The 1985 Irwin–Brorsen and 1988 Lukac et al. full texts were not accessed (403, or no free PDF). Exact system definitions and author affiliations at the time are unverified.
- The author and committee of the HAMMER thesis could not be confirmed (403).

## Q2. What exact rules define each strategy, and which parameters could be tuned?

### Takeaway
Two rules are fully specified and deterministic enough to code on 1-minute futures bars. The first is the Kais entropy pattern library: 8-bar OHLC-difference feature vector, L1 template match, fixed target/stop. The second is the Lee/Ning stack: EMRT-minimising hedge ratio with "important extrema", a 4^l discretised-return-state Q-table, and a signature optimal-stopping entry/exit. The Ag Econ systems are standard TradeStation-style rules.

### Cited Findings
**A. Entropy-assisted quality pattern library (Gupta, Gupta, Singh, Kais 2025)** — [OSTI full text](https://www.osti.gov/pages/servlets/purl/3673261)
- Raw pattern extraction: find time segments that precede a large swing (e.g. ±15 points in gold within the next 2 hours). Label each segment Buy or Sell by the direction of the move that follows.
- Pattern definition: 8 consecutive 30-minute OHLC bars (a 4-hour window). Each pattern is a 32-dimensional vector made of the 8 values each of H−L, C−O, H−O and O−L. Each pattern also carries a historical PnL.
- Scoring: local entropy H(x) of the Buy/Sell labels among the pattern's neighbours in feature space. Information gain is IG(x) = H_global − H(x). The score is α·IG(x) + (1−α)·PnL_norm(x), with α = 0.8 in the paper.
- Pruning (Algorithm 1): sort all patterns by score, descending. Accept a Buy pattern only if its L1 distance to every accepted Sell pattern is at least θ, and the reverse for Sell patterns. The result is disjoint libraries B′ and S′. Pruning took the gold set from 913 Buy / 1004 Sell to 543 Buy / 655 Sell.
- Live rule: every 30 minutes, compute the same 32 features over the last 8 bars. If the L1 distance to any Buy template is below a threshold, go long at the current open; if it is below the threshold for a Sell template, go short. Exit on a fixed profit target or a fixed stop (e.g. 12–18 gold points).
- Tunable parameters: swing threshold (±15 points), forward horizon (2 hours), bar size (30 minutes), window length (8 bars), feature set, neighbourhood size for local entropy (not stated), α, overlap threshold θ, match threshold, target T and stop S.

**B. EMRT spread plus RL trading (Ning & Lee 2024)** — [arXiv PDF](https://arxiv.org/pdf/2403.12180)
- "Important extrema" (from Fink & Gandhi 2007): X_m is an important minimum if it is the minimum of some segment X_i…X_j and both endpoints are at least C·s above it, where s is the sample standard deviation. Important maxima are defined symmetrically.
- EMRT: build alternating times τ1 (first important extreme), τ2 (first crossing of the sample mean θ̂ after τ1), τ3 (next extreme), and so on. EMRT is r = (2/N)·Σ(τ_even − τ_prev), the average time from an extreme back to the mean. C = 2 was used in the simulations.
- Hedge ratio: set a1 = 1 and grid-search the other coefficients over [−3.00, 3.00] in steps of 0.01 to minimise the EMRT of the spread, subject to a variance cap M.
- State: S_t = [d_{t−l+1}, …, d_t], with d_i = +2 if the percentage change π_i > k, +1 if 0 < π_i < k, −1 if −k < π_i < 0, and −2 if π_i < −k. With l = 4 there are 16 states (the paper says 4^l; for l = 4 that would be 256, but the text says "16 distinct states", which is an internal inconsistency to flag). k = 3% is the example value; k = 1 is used in the empirical section.
- Actions: buy 1, hold, or sell 1. The strategy is long-only: no short entries.
- Reward: R_{t+1} = A_t·(θ − X_t) − c·|A_t|, where c is the transaction cost. Tabular Q-learning with learning rate 0.1, γ = 0.99, ε = 0.1, 10 episodes. Training is on simulated Ornstein–Uhlenbeck (OU) paths, and ε = 0 at test time.
- Baselines: the distance method (B = 1, k = 1 s.d. bands) and OU (maximum-likelihood B, enter at −0.5·σ_eq and exit at +0.5·σ_eq).
- Tunable parameters: C, l, k, c, the coefficient grid, M, and the OU simulation parameters used for training.

**C. Signature optimal stopping entry/exit (Ning, Chakraborty & Lee 2023/24)** — [arXiv PDF](https://arxiv.org/pdf/2309.16008)
- Sequential optimal stopping. Entry solves sup over τ0 of E[e^{−rτ0}(−X_τ0 − c)]. Exit solves sup over ν0 of E[e^{−r̂ν0}(X_ν0 − ĉ)]. The pair is solved iteratively for each round trip, with separate entry and exit costs c and ĉ.
- Each stopping rule is a linear functional of the N-truncated signature of the time-augmented spread path. It is fitted by minimising a sigmoid-smoothed loss on training paths simulated from an OU process. Block bootstrap is suggested as an alternative.
- Baseline: go long when X_t < MA − k·Std and exit when X_t > MA + k·Std, with k = 0.1 and a 100-sample lookback. The SOT setting used a threshold k = 0.05.
- Tunable parameters: signature truncation level N, sigmoid sharpness μ, discount rates, costs, and the training-path generator.

**D. Purdue Ag Econ technical trading systems (Retter 2022)** — [PDF](https://ag.purdue.edu/department/agecon/_docs/undergraduate/thesis/jaden-retter_honors-thesis.pdf)
- Eight always-in-the-market systems: single SMA with an N-day confirmation filter, dual-MA cross, pivot reversal (breakout of a pivot high or low over N bars), MACD zero-cross, price channel (Donchian-style), Keltner channel breakout (stop at the breakout bar's high + 1 point), Bollinger re-entry (2 s.d.; buy stop when the low re-crosses the lower band), and RSI 30/70 cross.
- Boyd's dissertation simulated five technical systems. The channel system had the best mean return relative to its variance. — [Purdue e-Pubs](https://docs.lib.purdue.edu/dissertations/AAI9132426)

### Inferences
- Rule A ports directly to 1-minute futures. Resample to N-minute bars, build the 4×W OHLC-difference vectors, set the swing threshold in ATR units rather than fixed points, and walk it forward. It is a k-NN/template-matching analog forecaster with an entropy-purity filter.
- Rule B's EMRT is itself a reusable diagnostic. On a single instrument it can rank spreads (for example ES−NQ, GC−SI, ZN versus equity) or choose a de-trending lookback. The Q-learning state is a 4-bin discretisation of the last l returns, which is easy to replicate deterministically on 1-minute bars.
- Rule C needs a signature library (iisignature or signatory) and simulated training paths. It is deterministic once fitted, but heavier to build.

### Gaps
- The Kais paper does not report the neighbourhood size for local entropy, the overlap threshold θ, the match threshold, or the exact target/stop grid behind each equity curve.
- Ning & Lee have the internal inconsistency on the state count (4^l versus 16).

## Q3. What were the findings, and were they out of sample or net of costs?

### Takeaway
Every Purdue result is short-sample and favourable to the authors. The Kais pattern library reports 30–70% annual returns in one out-of-sample year (2024) with no costs. Lee/Ning report higher daily Sharpe than OU or distance baselines on 10 and 4 hand-picked stock pairs, with one-year out-of-sample tests and costs only inside the reward or stopping objective. The Ag Econ work found returns above costs, but in-sample (Retter) or decaying over time (Lukac et al., per Park & Irwin).

### Cited Findings
- **Entropy patterns:** gold vs USD, 2017–2023 for pattern extraction and tuning, 2024 held out. The results were "annual returns ranging from 30% to 60%" across target/stop configurations. GBPUSD in 2024 returned "approximately 30% to 70%". The authors say "commissions, exchange fees, and slippage are not yet incorporated". No Sharpe ratio, drawdown or trade counts are reported, only equity-curve figures. — [OSTI](https://www.osti.gov/pages/servlets/purl/3673261)
- **RL stat arb:** 10 US stock pairs (MSFT-GOOGL, CVS-JNJ, CL-KMB, V-MA, GE-BA, OXY-XOM, WELL-VTR, PPG-SHW, VZ-TMUS, CSX-NSC), daily Yahoo adjusted closes. Formation was 2022 and trading 2023 (out of sample). Example RL cumulative PnL: MSFT-GOOGL 37.8% vs 11.4% (distance) and 8.2% (OU); CL-KMB 22.3% vs 15.6% and 4.3%; GE-BA 48.8% vs 64.2% (distance was better here) and 10.0%. RL daily Sharpe ranged from 0.051 to 0.138. Max drawdown was 0% in 4 of 10 pairs, which is suspicious and partly because the strategy is long-only and holds to the end. — [arXiv PDF](https://arxiv.org/pdf/2403.12180)
- **Signature stopping:** 4 pairs (WM-RSG, UAL-DAL, V-MA, GS-MS), daily, formation 2021 and trading 2022. SOT vs baseline cumulative PnL: 10.0% vs 2.6%, 42.5% vs 9.6%, 6.8% vs 2.5%, 15.8% vs 2.9%. Daily Sharpe: 0.090 vs 0.031, 0.178 vs 0.049, 0.052 vs 0.026, 0.101 vs 0.035. There were only 5–7 trades per pair per year. GS-MS max drawdown was worse under SOT (−7.9% vs −2.3%). — [arXiv PDF](https://arxiv.org/pdf/2309.16008)
- **Retter (2022):** corn, soybeans and Chicago wheat, daily, back-adjusted, 2010–2020. Costs were $50 commission plus slippage and $5 fees per round turn. Parameters were optimised over the full 10 years, so the test is in-sample and the author says real-time results "would show a performance decay". The average across systems was 3.43% per year. DMA was best at 5.18% and SMA worst at 1.74%. Returns fell from 11.16% (2011) to −0.12% (2020), and the excess over T-bills was small. — [PDF](https://ag.purdue.edu/department/agecon/_docs/undergraduate/thesis/jaden-retter_honors-thesis.pdf)
- **Boyd (Purdue PhD, advisor Brorsen):** 5 systems on 7 commodities (corn, soybeans, sugar, silver, live cattle, T-bills, Deutsche Mark), 1960–1986. Returns were significantly above zero for most commodities, and weak-form efficiency was rejected even after CAPM risk adjustment. Returns were far more correlated across systems than across commodities, and monthly returns had high kurtosis. Price variability was the main correlate of returns. — [Purdue e-Pubs](https://docs.lib.purdue.edu/dissertations/AAI9132426)
- **Lukac, Brorsen & Irwin (1988):** 12 systems on a portfolio of 12 commodities, 1978–1984. Seven systems had significant gross returns and four had significant net, risk-adjusted returns. — [Scilit](https://scilit.com/publications/c283eba5ed79a2127bb9f8b70eb70fe9). A later review gives the sample end as 1985. — [vLex review](https://law-journals-books.vlex.com/vid/profitability-of-alternative-methods-855614780). Park & Irwin found the performance did not persist on 1985–2003 data, and with data-snooping correction the best rules were profitable for only 2 of 17 futures contracts. — [AgEcon Search Park & Irwin](https://ageconsearch.umn.edu/record/19039/files/cp05pa01.pdf); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=722264)

### Inferences
- **Overfitting risk.** The Kais results come from one test year in which gold trended strongly up (2024 had the highest monthly volatility in the sample). The authors also have a commercial affiliation (EntropyX Labs). Treat the 30–70% figures as unverified. Fixed-point targets/stops on a 30-minute signal with no costs will likely shrink sharply after costs. The edge would have to be re-measured on 1-minute GC/SI with realistic slippage.
- **Small samples.** The Lee/Ning pairs were hand-picked as co-moving in-sample, with 1 out-of-sample year and few trades (5–7 per pair in the signature paper). That is far too small a sample to separate skill from luck. Costs enter the RL reward and the stopping objective, but the reported PnL tables do not state whether net PnL deducts realistic costs.

### Gaps
- No Purdue study found was run on intraday futures with explicit costs plus a walk-forward or multiple-testing correction.
- Exact Lukac et al. net return figures were not retrieved from primary text.

## Q4. How unusual is it compared with mainstream strategies (MA crossover, plain mean reversion, Donchian or noise-band breakouts, Bollinger/Keltner squeeze)?

### Takeaway
The entropy pattern library and the EMRT/RL/signature work are genuinely different from the user's current families. The first is non-parametric analog template matching; the second is a learned exit policy and a hedge ratio chosen by time-to-revert rather than by cointegration. The Purdue Ag Econ systems are mainstream: MA cross, channel/Donchian, Keltner, Bollinger, RSI.

### Cited Findings
- The Kais paper says its patterns are extracted automatically from price history and "may or may not resemble well-known trading motifs (like breakouts or retracements)". It frames itself as an alternative to K-means and GMM clustering, which gave unbalanced groupings (K-means 300 Buy vs 1617 Sell; GMM 1347 Buy vs 570 Sell). — [OSTI](https://www.osti.gov/pages/servlets/purl/3673261)
- Ning & Lee contrast their state space ("recent trends in price movements") with traditional rules that "primarily focus on price deviations from a long-term mean". They also note that the threshold choice in standard rules has no principled selection method. — [arXiv PDF](https://arxiv.org/pdf/2403.12180)
- Retter's eight systems are explicitly "classic trending, breakout, and mean reversion" systems: SMA, DMA, MACD, pivot reversal, price channel, Keltner, Bollinger and RSI. — [PDF](https://ag.purdue.edu/department/agecon/_docs/undergraduate/thesis/jaden-retter_honors-thesis.pdf)

### Inferences
- **Novelty ranking for this project (high to low):**
  1. Entropy-filtered OHLC template library (analog forecasting, single instrument, good fit for GC, SI and 6E on 1-minute bars resampled to 15–30 minutes).
  2. EMRT-based spread or hedge-ratio selection plus an "important extrema" swing detector. The C·s important-extrema definition is also a usable zig-zag swing filter for single-instrument mean reversion.
  3. Signature optimal-stopping exits (complex to build).
  4. Discretised-return-state Q-learning (simple, but it overfits easily).
  5. Ag Econ channel and MA systems (already covered by the Donchian and MA families).
- **Determinism on 1-minute bars.** Rule A is deterministic once the library is frozen. Rule B is deterministic once the Q-table is frozen, but training on simulated OU paths makes it less sensitive to look-ahead. Both should be walk-forwarded (re-extract or re-train per fold) to avoid the in-sample flattery seen in all of these papers.

### Gaps
- No independent replication of either the Kais or the Lee/Ning rules was found.
- No Purdue work was found on fractal or Hurst rules, volatility-clustering timing rules, or candlestick-pattern rules on futures.
