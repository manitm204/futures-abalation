"""Long-only intraday-bar moving-average crossover (5min / 15min / 1h): buy the
next open after the fast MA crosses above the slow MA (optionally confirmed for
several bars, separated by an ATR buffer, and in the direction of the slow MA's
slope), exit at the next open after the fast MA falls back to or below the slow
MA, with an optional ATR initial stop. Ships its own compact backtester
(backtest.py) that reuses the engine's slippage/commission primitives and emits
engine `Trade` objects, mirroring the RSI-divergence and mean-reversion families.
"""
