# Statistical-model and ML trading strategies (regime models, filters, ML forecasters) with credible OOS on futures / index

Scope note: all sources were read in Nov 2026. Primary full texts were read for Shu-Yu-Mulvey (arXiv HTML), Lim-Zohren-Roberts (PDF), Wood-Roberts-Zohren (PDF) and Goulding-Harvey-Mazzoleni "Breaking Bad Trends" (PDF). The other papers are known only from abstracts or catalog pages, and this is flagged where it applies. Budget limits meant wavelet/spectral methods and Ang & Timmermann were not researched (see Gaps).

## Q1. Which papers have a model (not a hand-tuned indicator) produce the signal, are implementable from OHLCV, have few parameters, and report honest OOS results? Exact specs and trading rules.

### Takeaway
The best fit is the **statistical jump model (JM) risk-on/risk-off switch** of Shu, Yu & Mulvey (2024). It has three EWM features from returns, K=2 states, one jump penalty λ chosen by rolling validation, a 0/1 position, a 1-day delay and 10 bps costs, over 1990-2023 OOS on S&P 500, DAX and Nikkei. The cheapest-to-test model-based family is the **momentum turning-points dynamic-speed rule** (Goulding, Harvey & Mazzoleni, JFE 2023 / FAJ 2023). It has two lookbacks, and its two mixing weights are estimated ex ante in closed form with no look-ahead. The deep-learning momentum papers (Lim et al. 2019; Wood et al. 2022) report high OOS Sharpe ratios gross of costs, but they are fragile to costs and heavy on hyperparameters. Intraday ML return forecasting on index futures from OHLCV alone has a documented null result.

### Cited Findings

**Paper 1. Statistical jump model regime switch (strongest candidate)**
- Citation: Yizhan Shu, Chenyu Yu, John M. Mulvey, "Downside Risk Reduction Using Regime-Switching Signals: A Statistical Jump Model Approach," arXiv:2402.05272 (v3, 17 Sep 2024). The journal DOI 10.1057/s41260-024-00376-x is a Palgrave journal, likely the *Journal of Asset Management*. — [arXiv abstract](https://arxiv.org/abs/2402.05272)
- Model: a statistical jump model (clustering with a jump penalty λ charged at each state transition) that "enhances regime persistence" compared with Markov-switching models. — [arXiv](https://arxiv.org/abs/2402.05272)
- Features: three exponentially smoothed features of excess returns: downside deviation (halflife 10d), Sortino ratio (halflife 20d) and Sortino ratio (halflife 60d). K=2 states (bull/bear). — [arXiv HTML v3](https://arxiv.org/html/2402.05272v3)
- Training and refit: 3,000-day training window (about 12 years), JM parameters re-estimated every 6 months. Online inference of the latest state uses dynamic programming over a 3,000-day lookback with fixed parameters. — [arXiv HTML v3](https://arxiv.org/html/2402.05272v3)
- λ selection: chosen **monthly** from candidate values by the highest Sharpe of the 0/1 strategy over an **8-year validation lookback**, with costs and the 1-day delay included. Illustrative λ values are 0, 5, 15, 35, 50, 70 and 150; the exact candidate grid is not stated. — [arXiv HTML v3](https://arxiv.org/html/2402.05272v3)
- Signal to position: 100% index in bull, 100% 3-month T-bill in bear. A signal at the close of t is applied from t+2 (1-day delay). Robustness checks use 5- and 10-day delays. Cost is 10 bps one-way. — [arXiv HTML v3](https://arxiv.org/html/2402.05272v3)
- OOS 1990-2023 results:

  | Index | Strategy | Sharpe | Max drawdown |
  |---|---|---|---|
  | S&P 500 | JM | 0.68 | -26.6% |
  | S&P 500 | HMM | 0.54 | -28.9% |
  | S&P 500 | Buy & hold | 0.48 | -55.2% |
  | DAX | JM | 0.44 | -39.4% |
  | DAX | HMM | 0.35 | not recorded |
  | DAX | Buy & hold | 0.30 | -72.7% |
  | Nikkei 225 | JM | 0.31 | -45.3% |
  | Nikkei 225 | HMM | 0.19 | not recorded |
  | Nikkei 225 | Buy & hold | 0.12 | -79.1% |

  — [arXiv HTML v3](https://arxiv.org/html/2402.05272v3)
- HMM baseline: refit daily on a rolling 3,000-day window (Bulla et al. approach), with a median/rolling-mean filter window k tuned monthly. — [arXiv HTML v3](https://arxiv.org/html/2402.05272v3)
- Caveats from the paper: the regimes lag turning points by about two weeks. Some figures (Figs 2-4) are in-sample illustrations, while model selection uses online-inferred regimes. Each index is tested separately. The paper does not discuss look-ahead explicitly. — [arXiv HTML v3](https://arxiv.org/html/2402.05272v3)
- Free parameters: 3 feature halflives (fixed by the authors), K=2, λ (tuned), training length, refit frequency and validation length. Effectively **one tuned parameter (λ)**. — [arXiv HTML v3](https://arxiv.org/html/2402.05272v3)

**Paper 2. Jump model with intraday realized-volatility features (directly relevant to 1-min data; abstract-level only)**
- Citation: Peter Nystrup, Petter N. Kolm, Erik Lindström, "Greedy Online Classification of Persistent Market States Using Realized Intraday Volatility Features," *Journal of Financial Data Science* 2(3), 25-39 (2020), DOI 10.3905/jfds.2020.2.3.025. — [DTU Orbit](https://orbit.dtu.dk/en/publications/greedy-online-classification-of-persistent-market-states-using-re/); [Lund record](https://lup.lub.lu.se/record/8724d7aa-68dd-407b-bdfa-fb7bf5e810e0)
- What it does: a greedy online classifier assigns each new observation to a hidden state without re-parsing history while keeping persistence. Adding features **built from intraday data** improves classification accuracy. It is applied to the S&P 500. The jump model loss is ‖y_t − θ_s‖² plus a penalty λ on state changes. — [Kolm slides, UC Berkeley CDAR 2021](https://cdar.berkeley.edu/sites/default/files/petter_kolm_uc_berkeley_20210216_-_slides.pdf); [econbiz record](https://www.econbiz.de/Record/greedy-online-classification-of-persistent-market-states-using-realized-intraday-volatility-features/10012834827)
- Exact feature list, trading results and OOS numbers were not retrieved (paywalled full text).

**Paper 3. HMM regime-based allocation (Nystrup and co-authors; abstract-level only)**
- Nystrup, Madsen & Lindström, "Dynamic portfolio optimization across hidden market regimes," *Quantitative Finance* 18(1), 83-95 (2018). It uses a two-state HMM with time-varying (adaptively estimated) parameters to forecast mean and variance inside model predictive control. A trading penalty that reduces trades improves robustness. — [RePEc](https://econpapers.repec.org/RePEc:taf:quantf:v:18:y:2018:i:1:p:83-95); [Lund record](https://lup.lub.lu.se/record/aee3840b-06ee-4e2d-8b50-65f2c0d66b92)
- Nystrup, Hansen, Olejasz Larsen, Madsen, "Regime-Based versus Static Asset Allocation: Letting the Data Speak," *JPM* 44(2), 2017. Regime-based allocation was profitable even against a diversified 60/40 benchmark. — [search summary of JPM listing](https://lup.lub.lu.se/record/52fff970-3b25-460d-ba95-31351c98d0a2)
- Nystrup, Boyd, Lindström, Madsen, "Multi-period portfolio selection with drawdown control," *Annals of OR* 282 (2019). Tested OOS over about two decades. — [DTU PDF](https://backend.orbit.dtu.dk/ws/files/149812772/Multi_Period_Portfolio_Selection_with_Drawdown_Control.pdf)
- Exact OOS Sharpe ratios were not extracted. Shu et al. (Paper 1) is the cleanest head-to-head JM-vs-HMM OOS comparison found, and there the HMM is the weaker model.

**Paper 4. Momentum turning points / dynamic-speed trend (few parameters, closed-form, no look-ahead)**
- Citations: Christian Goulding, Campbell R. Harvey, Michele Mazzoleni, "Momentum Turning Points," *Journal of Financial Economics* 149(3), 378-406 (2023), DOI 10.1016/j.jfineco.2023.05.007. An earlier SSRN version (2019) included Ashish Garg. — [RePEc](https://econpapers.repec.org/RePEc:eee:jfinec:v:149:y:2023:i:3:p:378-406)
- Follow-up: Goulding, Harvey, Mazzoleni, "Breaking Bad Trends," *Financial Analysts Journal* (2023/2024), DOI 10.1080/0015198X.2023.2270084. — [Duke PDF](https://people.duke.edu/~charvey/Research/Published_Papers/P167_Breaking_bad_trends.pdf)
- States: Bull = slow ≥ 0 and fast ≥ 0; Correction = slow ≥ 0 and fast < 0; Bear = both < 0; Rebound = slow < 0 and fast ≥ 0. The slow signal is the trailing 12-month return. The fast signal is the trailing 2-month return in the main FAJ analysis (1-month in robustness checks and the JFE version). — [Breaking Bad Trends](https://people.duke.edu/~charvey/Research/Published_Papers/P167_Breaking_bad_trends.pdf)
- Position rule: +1 in Bull and −1 in Bear. In Correction the return is (1−a_Co)·r_SLOW + a_Co·r_FAST, and in Rebound it is (1−a_Re)·r_SLOW + a_Re·r_FAST. Each state is observable at the start of the month. — [Breaking Bad Trends](https://people.duke.edu/~charvey/Research/Published_Papers/P167_Breaking_bad_trends.pdf)
- Mixing weights are closed form (Appendix C): a_Co = ½(1 − (1/C)·AVG[r|Co]/AVG[r²|Co]) and a_Re = ½(1 + (1/C)·AVG[r|Re]/AVG[r²|Re]), where C = FREQ[Bu]/FREQ[Bu or Be]·AVG[r|Bu]/AVG[r²|Bu or Be] − FREQ[Be]/FREQ[Bu or Be]·AVG[r|Be]/AVG[r²|Bu or Be]. They are re-estimated every 30 months from inception-to-date data and clipped to [0,1]. At least 12 months of history in each phase is required. The authors say this is "implementable as a trading strategy with no look-ahead bias." — [Breaking Bad Trends](https://people.duke.edu/~charvey/Research/Published_Papers/P167_Breaking_bad_trends.pdf)
- Sign convention: as extracted, the PDF's mixing equations both read ½(1 − …). However, the text says positive returns after rebounds imply a_Re > 0.5, which implies a + sign for a_Re. Verify against the JFE paper before coding.
- Results: on 43 futures markets, 1990-2022, scaled to 10% vol, static 12-month trend earned about 6.4% a year over the full sample but only 0.3% in 2009-2019. The dynamic version earned 3.4% in 2009-2019. Worst drawdown was −13.2% (dynamic) vs −18.8% (static). Turning points make up about 35% of months (1969-2018 US equity). — [Breaking Bad Trends](https://people.duke.edu/~charvey/Research/Published_Papers/P167_Breaking_bad_trends.pdf); [AEA 2021 slides](https://benny.aeaweb.org/conference/2021/preliminary/powerpoint/ihbRDkeH)
- Costs: transaction costs are not modelled in what was read. This was a monthly rebalance.

**Paper 5. Deep Momentum Networks (complex; flag cost fragility)**
- Citation: Bryan Lim, Stefan Zohren, Stephen Roberts, "Enhancing Time-Series Momentum Strategies Using Deep Neural Networks," *Journal of Financial Data Science*, Fall 2019, arXiv:1904.04912. — [arXiv](https://arxiv.org/abs/1904.04912)
- Inputs: volatility-normalised returns over 1d, 1m, 3m, 6m and 12m (e.g. r_{t−252,t}/(σ_t√252)), plus volatility-normalised MACD indicators at several (S,L) pairs. The output is a position in [−1,1] scaled by σ_tgt/σ_t, with σ_tgt = 15%. The loss directly optimises Sharpe. — [arXiv PDF](https://arxiv.org/pdf/1904.04912)
- Training: recalibrated from scratch **every 5 years** using all data to date. Each refit reruns a 50-iteration random hyperparameter search (dropout, hidden size, and so on), with up to 100 epochs, early stopping at patience 25, and the last 10% of each block as validation. Weights are frozen for the next 5 years. Data: 88 continuous futures (Pinnacle CLC), 1990-2015, tested 1995-2015. — [arXiv PDF](https://arxiv.org/pdf/1904.04912)
- Raw OOS Sharpe ratios: LSTM-Sharpe 2.80; Sgn(returns) TSMOM 1.19; MACD 0.98; long-only 0.74. — [arXiv PDF](https://arxiv.org/pdf/1904.04912)
- **With 10 bps costs** the unregularised LSTM collapses to Sharpe **−5.31**. The turnover-regularised LSTM gets 0.91, against 0.86 for Sgn(returns) and 0.72 for MACD. The LSTM beats the benchmarks only up to about 2-3 bps. — [arXiv PDF](https://arxiv.org/pdf/1904.04912)

**Paper 6. Changepoint-detection-augmented momentum (complex; gross of costs)**
- Citation: Kieran Wood, Stephen Roberts, Stefan Zohren, "Slow Momentum with Fast Reversion: A Trading Strategy Using Deep Learning and Changepoint Detection," *Journal of Financial Data Science*, Winter 2022, arXiv:2105.13727. — [arXiv](https://arxiv.org/abs/2105.13727)
- CPD module: online Gaussian-process changepoint detection. A Matérn 3/2 kernel is compared with a Changepoint kernel (GPflow) over a lookback window (LBW) l ∈ {10, 21, 63, 126, 252} days. It outputs changepoint location and severity, which are fed with the DMN features into an LSTM with Sharpe loss. — [arXiv PDF](https://arxiv.org/pdf/2105.13727)
- Data and scheme: 50 liquid continuous futures, 1990-2020, expanding window (train 1990-1995, test 1995-2000, and so on in 5-year steps). — [arXiv PDF](https://arxiv.org/pdf/2105.13727)
- Raw OOS Sharpe, 1995-2020: long-only 0.44, MACD 0.77, TSMOM 0.94, LSTM 1.62, LSTM+CPD 1.77 / 2.04 / 2.08 / 1.75 / 1.45 for LBW 10 / 21 / 63 / 126 / 252, and LBW-optimised 2.16. — [arXiv PDF](https://arxiv.org/pdf/2105.13727)
- Main results are **before transaction costs**. Costs of 0-5 bps are only in an appendix. — [arXiv PDF](https://arxiv.org/pdf/2105.13727)

**Kalman / linear trend filters (not a distinct family for this user)**
- Levine & Pedersen, "Which Trend Is Your Friend?" *Financial Analysts Journal* 72(3), 2016. In their general forms, time-series momentum, MA crossovers, the HP filter, the **Kalman filter** and all other linear filters are equivalent representations, compared via "trend signature plots." — [CBS publisher's version](https://research-api.cbs.dk/ws/files/60084063/lasse_heje_pedersen_et_al_which_trend_is_your_friend_publishersversion.pdf); [RePEc](https://ideas.repec.org/a/taf/ufajxx/v72y2016i3p51-66.html)

**Intraday ML return forecasting from OHLCV (negative or weak evidence)**
- Mathias Mesfin, "Sequential Structure in Intraday Futures Data: LSTM vs Gradient Boosting on MNQ," arXiv:2605.17724 (May 2026). Data: MNQ 5-minute OHLCV, 944 days 2021-2025. Label: whether the session close exceeds the 10:30 open by more than 10 points. Expanding-window walk-forward over 3 OOS periods. OOS accuracy was 50.0-50.9% for gradient boosting and 50.6% for the LSTM, against a 51.8% base rate. Permutation p-values were 0.135 and 0.515. "No configuration produces statistically significant out-of-sample accuracy." — [arXiv](https://arxiv.org/abs/2605.17724)
- Ferreira & Medeiros, "Modeling and Forecasting Intraday Market Returns: a Machine Learning Approach," arXiv:2112.15108. Minute-by-minute rolling-window LSTM and random forest. VIX is the strongest predictor; random forests gave no gain. VIX is not in the user's OHLCV set. — [arXiv](https://arxiv.org/abs/2112.15108)
- A *Journal of Financial Econometrics* 2023 paper (21(2):485-527) on 5-minute market returns with ML ensembles reports Sharpe ratios of about 0.98 after costs. A search summary attributed it to Huddleston, Liu & Stentoft, but that was not verified. It uses lagged constituent returns, which are not available from futures OHLCV alone. — [RePEc](https://econpapers.repec.org/RePEc:oup:jfinec:v:21:y:2023:i:2:p:485-527.)

### Inferences
- **Paper 1 (JM) and Paper 4 (turning points) are the two strongest picks** for an anti-overfitting ablation suite. Both have one or two effective free parameters, ex-ante estimation, and a published OOS/no-look-ahead design.
- **Papers 5-6 (DMN/CPD) do not suit a small grid.** Each 5-year refit re-runs a 50-trial hyperparameter search. A simplified "CPD severity as a feature or filter" variant (GP changepoint score with LBW ∈ {21, 63}) would be testable without the LSTM.
- **Kalman trend is not a genuinely new family for this user.** By the Levine-Pedersen equivalence, a Kalman level/slope filter is a linear filter of past prices, so it is close to the user's existing MA-crossover/channel tests. The new information from a Kalman filter is the **state uncertainty** (filter variance), not the trend estimate itself.
- **Data-length conflict:** the user's data starts 2018-01, so there are about 2,200 daily bars per instrument before the holdout. That is shorter than JM's 3,000-day training window plus 8-year λ validation. Options are (a) build daily features from 1-min data and train on about 3-4 years, (b) run the JM on intraday bars (e.g. 15-min or 30-min) with halflives rescaled, or (c) pool across instruments (ES/NQ/RTY/YM share regimes). The turning-points model also needs ≥12 months per phase on monthly data, which is infeasible on 8 years. It must be translated to faster horizons (e.g. daily bars with slow = 60d and fast = 10d) or pooled across the 9 instruments.
- Intraday 1-min-bar ML direction forecasting on a single index future is likely to be a null result (Mesfin 2026). If tried, it should carry permutation tests as the honesty check.

### Gaps
- Exact feature list and OOS numbers for Nystrup-Kolm-Lindström (2020) were not retrieved (paywall).
- Nystrup HMM OOS Sharpe figures were not extracted.
- Ang & Timmermann (2012) "Regime Changes and Financial Markets" (a review) was not examined.
- Wavelet/spectral trading papers with credible OOS on futures were not researched in the time budget.
- No Gu-Kelly-Xiu-style ML study on **futures** intraday returns with walk-forward and costs was found, except Mesfin's null result.
- No independent replication of Shu-Yu-Mulvey was found. The same Mulvey/Kolm group has follow-ups (continuous/sparse JM) that were not checked.
- The JFE "Momentum Turning Points" paper's own Sharpe tables (US equity 1969-2018) were not read directly.

## Q2. Which of these could serve as a regime FILTER on the user's existing strategies?

### Takeaway
The JM bull/bear state and the realized-volatility-feature JM are natural filters, for example running intraday momentum or breakout only in the "bear/high-risk" state and mean reversion only in the calm state. The turning-points state (Bull / Correction / Bear / Rebound) is a free, parameter-light filter. The CPD severity score is a third candidate.

### Cited Findings
- The JM bear state is defined by high downside deviation and low Sortino. It cut S&P 500 max drawdown from −55% to −27% with only a 0/1 switch, so the state separates high-risk from low-risk periods. — [Shu et al. arXiv HTML](https://arxiv.org/html/2402.05272v3)
- Intraday-data features improve persistent-state classification accuracy in the greedy online JM. — [DTU Orbit record](https://orbit.dtu.dk/en/publications/greedy-online-classification-of-persistent-market-states-using-re/)
- Trend-following returns are hurt by turning points. Years with more slow/fast disagreements have lower trend Sharpe (R² = 0.69 across years for a multi-asset portfolio). The number of turning points is nearly uncorrelated with volatility (correlation 0.07), so it is a different conditioning variable from a volatility filter. — [Breaking Bad Trends](https://people.duke.edu/~charvey/Research/Published_Papers/P167_Breaking_bad_trends.pdf)
- In the CPD paper, changepoint severity helps the model exit momentum after reversals ("fast reversion"), especially in 2015-2020. — [arXiv 2105.13727](https://arxiv.org/abs/2105.13727)

### Inferences
- **Filter test 1:** a JM-on-RV state (features = EWM of daily realized variance from 1-min bars, downside RV, EWM daily return) as a gate. Run mean reversion or RSI-divergence only in the calm state; run noise-band momentum only in the turbulent state. One grid: λ × {gate on, gate off, inverse gate}.
- **Filter test 2:** the turning-points state from daily data as a gate. Breakouts and channel strategies trade only in Bull/Bear (slow and fast agree). Mean reversion trades in Correction/Rebound. This adds almost zero parameters (two lookbacks) and is uncorrelated with vol, per the paper.
- **Filter test 3:** "trend breaking" count, the number of slow/fast sign disagreements in the last N days, as a continuous gate.
- Because a filter cuts the trade count, report trade counts and PF per gate state to avoid declaring a winner on thin samples.

### Gaps
- No paper found explicitly tests a JM or HMM state as a gate on an intraday momentum or mean-reversion strategy. This use is an inference, not a published result.

## Q3. Natural ablation grid for each (parameter counts)

### Takeaway
Keep each grid at 12-36 cells. Fix model internals at the paper defaults, and vary only the 1-2 parameters the paper itself tunes or flags as sensitive (λ for JM, LBW for CPD, fast lookback for turning points). Choose those parameters on validation, then run the sealed holdout once.

### Cited Findings
- JM sensitivity: λ (illustrative 0-150), trading delay (1, 5, 10 days), and a 2-week regime lag are flagged by the authors. — [arXiv HTML v3](https://arxiv.org/html/2402.05272v3)
- CPD sensitivity: LBW 21-63d is best, and performance dips beyond a quarter (Sharpe 2.08 at 63d vs 1.45 at 252d). — [arXiv PDF](https://arxiv.org/pdf/2105.13727)
- Turning points: fast lookback of 1 vs 2 months (and 1/3/12 blends) gives similar conclusions. — [Breaking Bad Trends](https://people.duke.edu/~charvey/Research/Published_Papers/P167_Breaking_bad_trends.pdf)
- DMN: costs are the binding constraint (2-3 bps breakeven, so turnover regularisation is essential). — [arXiv PDF](https://arxiv.org/pdf/1904.04912)

### Inferences (proposed grids for the user's data)

| Family | Free params | Proposed grid | Instruments / bar |
|---|---|---|---|
| JM risk-on/off (Shu et al.) | λ (+ train length) | λ ∈ {0, 10, 25, 50, 100, 200}; train ∈ {3y, 5y}; features: paper set vs paper set + daily RV from 1-min; delay ∈ {1d, next open}. That is 6×2×2×2 = 48 cells; drop the delay dimension to get 24. | ES, NQ, RTY, YM, SPY, QQQ daily; also 6E, 6J, GC, CL, ZN for long/flat and long/short variants |
| JM as filter | λ only | λ ∈ {10, 50, 200} × gate mode {none, calm-only, turbulent-only} × host strategy | existing strategies |
| Turning-points dynamic speed | slow, fast lookbacks; a_Co/a_Re estimated | (slow, fast) ∈ {(252, 21), (252, 42), (126, 21), (60, 10)} trading days; refit of a every {6m, 12m}; pooled vs per-instrument a. That is 4×2×2 = 16 cells. | all 9 futures daily, vol-targeted |
| Simplified CPD filter | LBW, severity threshold | LBW ∈ {21, 63} × threshold ∈ {0.9, 0.95, 0.99}, used to flatten TSMOM or a host strategy. That is 6 cells (GP fit cost is per bar, so use daily bars). | daily |
| DMN-lite (optional) | many | Sharpe-loss linear model or small MLP on the 5 normalised returns + 3 MACDs, refit yearly, turnover penalty. Stop here; skip LSTM search. | daily, pooled |

- Expected Sharpe from the literature, for honest priors: JM switch on an equity index scores about 0.3-0.7 vs 0.1-0.5 buy-and-hold. Its main benefit is **drawdown**, not return. The DMN/CPD Sharpes of 1.6-2.8 are portfolio-level across 50-88 futures and gross or near-gross of costs, so they should not be expected on single instruments.
