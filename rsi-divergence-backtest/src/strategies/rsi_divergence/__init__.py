"""Long-only intraday-bar RSI divergence (5min / 15min / 1h): buy the next open
after a regular bullish divergence (price lower low, RSI higher low between two
consecutive confirmed RSI pivot lows), with an ATR stop (1R), an R-multiple
profit target and a maximum holding period. Ships its own compact backtester
(backtest.py) that reuses the engine's slippage/commission primitives and emits
engine `Trade` objects, mirroring the mean-reversion family.
"""
