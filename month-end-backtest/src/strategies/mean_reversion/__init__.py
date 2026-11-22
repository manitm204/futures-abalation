"""Long-only intraday-bar mean reversion (5min / 15min / 1h): buy when the close's z-score versus a rolling
SMA/EMA drops below an entry threshold (optionally only above a long trend SMA),
exit when the z-score recovers past an exit threshold or after a maximum
holding period. Ships its own compact backtester (backtest.py) that
reuses the engine's slippage/commission primitives and emits engine `Trade`
objects, mirroring the channel-breakout family.
"""
