"""Channel breakout (turtle-style) strategy: N-bar Donchian breakout entry with a
trailing M-bar opposite-channel exit, an optional fixed ATR stop, a breakout
buffer, and entry confirmation. Long-only.

This family needs a *trailing* channel exit, which the fixed stop/target engine
in src/engine/simulator.py cannot express, so it ships its own compact
backtester (backtest.py) that still reuses the shared execution primitives
(sizing, slippage, commission) and produces engine `Trade` objects so the
standard metrics / split analysis apply unchanged.
"""
