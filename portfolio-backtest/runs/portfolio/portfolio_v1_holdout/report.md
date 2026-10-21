# portfolio_v1 -- holdout 2025-01-01 to 2026-08-18

407 trading days (1.62 years). equal capital per sleeve on the window's first day, no rebalancing; SPY buy-and-hold close-to-close, no costs.

**holdout previously inspected -- NOT an untouched test**

| Metric | Mean reversion v2 | RSI divergence v3 | MA crossover v2 | Portfolio | SPY B&H |
|---|---|---|---|---|---|
| Total return | 18.2% | -7.9% | 1.5% | 3.9% | 30.9% |
| CAGR | 10.9% | -4.9% | 0.9% | 2.4% | 18.2% |
| Sharpe | 1.56 | -1.81 | 0.15 | 0.65 | 1.07 |
| Sortino | 2.76 | -2.06 | 0.19 | 0.88 | 1.59 |
| Ann. volatility | 6.8% | 2.8% | 8.2% | 3.8% | 17.0% |
| Max drawdown | -3.7% | -8.8% | -10.6% | -2.8% | -19.0% |
| Longest drawdown (days) | 96 | 388 | 390 | 193 | 88 |
| Calmar | 2.98 | -0.56 | 0.09 | 0.87 | 0.95 |
| Trades | 85 | 52 | 98 | 235 | 1 |
| Win rate | 56.5% | 32.7% | 43.9% |  |  |
| Avg trade | 0.20% | -0.16% | 0.02% |  |  |
| Profit factor | 1.71 | 0.44 | 1.04 |  |  |
| Avg hold (session hours) | 5.0 | 2.0 | 6.1 |  |  |
| Time in market | 14.8% | 3.9% | 22.5% | 37.9% (any) | 100% |
| Years in market | 0.24 | 0.06 | 0.36 | 0.61 | 1.62 |
| Beta to SPY | 0.10 | 0.02 | 0.24 | 0.12 | 1.00 |
| Correlation to SPY | 0.25 | 0.14 | 0.50 | 0.54 | 1.00 |

Sleeves:
- Mean reversion v2: `cfg_8bf5ce8a2763c7d2c5b0` (mr_v2, 1h) {"cooldown_bars": 8, "entry_confirmation": "positive_bar_return", "entry_z": -1.0, "exit_z": 0.5, "max_holding_bars": 8, "mean_lookback": 12, "mean_type": "sma", "stop_atr_multiple": "1.5", "symbol": "SPY", "timeframe": "1h", "trend_filter": "none"}
- RSI divergence v3: `cfg_5b670566dfd725e154ff` (rsi_v3, 5min) {"adx_filter": "off", "entry_confirmation": "immediate", "max_hold": 48, "max_pivot_gap": 12, "min_price_div_atr": 0.0, "min_rsi_diff": 5.0, "pivot_left": 5, "pivot_right": 1, "rsi_extreme": "30/70", "rsi_lookback": 10, "session_window": "excl_last30", "stop_atr": 2.5, "symbol": "SPY", "target_r": 1.5, "timeframe": "5min", "trend_filter": "off"}
- MA crossover v2: `cfg_d4f739a36463c2aefdec` (ma_v2, 15min) {"buffer_atr": 0.2, "confirm_bars": 2, "cooldown_bars": 4, "fast_length": 5, "ma_pair": "EMA/EMA", "max_extension_atr": null, "max_hold": 32, "min_adx": 15.0, "slope_filter": true, "slow_length": 100, "stop_atr": null, "symbol": "SPY", "take_profit_atr": null, "timeframe": "15min"}

Capital deployed on average: 13.7%; share of time with 0/1/2/3 sleeves in: 62.1% / 34.7% / 3.2% / 0.1%
Sleeve daily-return correlations: [[1.0, -0.08, 0.0827], [-0.08, 1.0, 0.0243], [0.0827, 0.0243, 1.0]]
