# portfolio_v1 -- validation 2023-01-01 to 2024-12-31

502 trading days (1.99 years). equal capital per sleeve on the window's first day, no rebalancing; SPY buy-and-hold close-to-close, no costs.

| Metric | Mean reversion v2 | RSI divergence v3 | MA crossover v2 | Portfolio | SPY B&H |
|---|---|---|---|---|---|
| Total return | 3.9% | 3.8% | 6.1% | 4.6% | 53.2% |
| CAGR | 2.0% | 1.9% | 3.0% | 2.3% | 23.9% |
| Sharpe | 0.41 | 0.70 | 0.53 | 0.76 | 1.73 |
| Sortino | 0.62 | 1.02 | 0.80 | 1.15 | 2.58 |
| Ann. volatility | 5.0% | 2.7% | 5.9% | 3.0% | 12.8% |
| Max drawdown | -7.6% | -2.1% | -6.4% | -3.8% | -10.3% |
| Longest drawdown (days) | 330 | 134 | 362 | 329 | 86 |
| Calmar | 0.26 | 0.92 | 0.47 | 0.61 | 2.32 |
| Trades | 93 | 65 | 128 | 286 | 1 |
| Win rate | 50.5% | 58.5% | 42.2% |  |  |
| Avg trade | 0.04% | 0.06% | 0.05% |  |  |
| Profit factor | 1.14 | 1.36 | 1.16 |  |  |
| Avg hold (session hours) | 5.3 | 2.2 | 5.5 |  |  |
| Time in market | 14.0% | 4.4% | 21.7% | 37.3% (any) | 100% |
| Years in market | 0.28 | 0.09 | 0.43 | 0.74 | 1.99 |
| Beta to SPY | 0.16 | 0.06 | 0.23 | 0.15 | 1.00 |
| Correlation to SPY | 0.42 | 0.27 | 0.49 | 0.63 | 1.00 |

Sleeves:
- Mean reversion v2: `cfg_8bf5ce8a2763c7d2c5b0` (mr_v2, 1h) {"cooldown_bars": 8, "entry_confirmation": "positive_bar_return", "entry_z": -1.0, "exit_z": 0.5, "max_holding_bars": 8, "mean_lookback": 12, "mean_type": "sma", "stop_atr_multiple": "1.5", "symbol": "SPY", "timeframe": "1h", "trend_filter": "none"}
- RSI divergence v3: `cfg_5b670566dfd725e154ff` (rsi_v3, 5min) {"adx_filter": "off", "entry_confirmation": "immediate", "max_hold": 48, "max_pivot_gap": 12, "min_price_div_atr": 0.0, "min_rsi_diff": 5.0, "pivot_left": 5, "pivot_right": 1, "rsi_extreme": "30/70", "rsi_lookback": 10, "session_window": "excl_last30", "stop_atr": 2.5, "symbol": "SPY", "target_r": 1.5, "timeframe": "5min", "trend_filter": "off"}
- MA crossover v2: `cfg_d4f739a36463c2aefdec` (ma_v2, 15min) {"buffer_atr": 0.2, "confirm_bars": 2, "cooldown_bars": 4, "fast_length": 5, "ma_pair": "EMA/EMA", "max_extension_atr": null, "max_hold": 32, "min_adx": 15.0, "slope_filter": true, "slow_length": 100, "stop_atr": null, "symbol": "SPY", "take_profit_atr": null, "timeframe": "15min"}

Capital deployed on average: 13.4%; share of time with 0/1/2/3 sleeves in: 62.7% / 34.6% / 2.7% / 0.1%
Sleeve daily-return correlations: [[1.0, 0.2746, 0.13], [0.2746, 1.0, 0.0542], [0.13, 0.0542, 1.0]]
