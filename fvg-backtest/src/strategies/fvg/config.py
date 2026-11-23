"""Typed configs + ablation axes for the 1-minute fair-value-gap (FVG) trade after displacement,
with and against the gap, on equity index futures.

Source: reports/ICT strategies to backtest.md (rank 4, "FVG continuation after displacement", a
216-cell grid). ICT teaches that a displacement leg leaves a three-candle gap that price returns
to and then continues from. A placebo-controlled study found real FVGs no better than random
zones, and a random-walk simulation reproduces the famous fill rates, so the `mode` axis trades
every setting both WITH the gap (ICT) and AGAINST it (the control).

Bars: each session's Globex 1-minute bars from 18:00 the evening before to 16:00 ET (ATR warms
up overnight); setups and entries are 09:45-15:30 ET only.

Setup (bullish; bearish mirrors it): three consecutive 1-minute bars of one session, all opening
inside the window, with high[1] < low[3]; gap = [high[1], low[3]]; gap >= fvg_min x ATR (and > 0);
the middle bar's true range >= disp x ATR. ATR = 14-bar mean 1-minute true range at bar 1.
  mode   : with -- long a bullish gap (ICT); against -- short it
  vwap   : off / on -- on: the trade's direction must agree with the close of bar 3 vs the
           session VWAP (09:30 onward, volume-weighted typical price)
  entry  : prox -- order at the gap's near edge (low[3]); ce -- at its midpoint; mkt -- market at
           the open of the bar after bar 3. A `with` order at the gap is a limit (fills on a 1-tick
           trade-through, at the better of the level and the bar's open); an `against` order at the
           gap is a stop (fills when a bar touches the level, at the worse of the level and the
           bar's open, with stop slippage) -- it sells as price falls into a bullish gap.
  wait   : 5 / 15 / 30 bars the order rests (inside the window); not used by mkt
  stop   : struct -- 2 ticks beyond the three bars' extreme on the stop side; a1.5 / a3.0 -- that
           many ATR; never closer than 1.0 ATR to the entry reference
  target : 1R / 2R / 3R / none -- limit, 1-tick trade-through, from the bar after the fill
  hold   : 15 / 30 / 60 minutes -- time exit at the close of the hold's last bar (and by 16:00)
  window : am 09:45-12:00 / pm 12:00-15:30 / rth 09:45-15:30 (setups and entries)
One trade per session. 3 x 4 x 2 x 2 x 2 x (2 x 3 + 1) x 3 x 4 x 3 = 24,192 configs.
"""

from __future__ import annotations

from typing import Literal

from src.utils.config_models import FrozenModel

SESSION_END_MIN = 16 * 60        # nothing is held at or after 16:00 ET
EVENING_START_MIN = 18 * 60      # Globex reopens 18:00 ET; those bars carry the NEXT session date
RTH_START_MIN = 9 * 60 + 30      # session VWAP starts here
ATR_LEN = 14
PAD_TICKS = 2
MIN_STOP_ATR = 1.0
THROUGH_TICKS = 1

WINDOWS: dict[str, tuple[int, int]] = {
    "am": (585, 720),
    "pm": (720, 930),
    "rth": (585, 930),
}


def parse_target(t: str) -> float | None:
    if t == "none":
        return None
    if t.endswith("R"):
        return float(t[:-1])
    raise ValueError(f"Unknown target {t!r}")


def parse_stop(s: str) -> tuple[str, float | None]:
    if s == "struct":
        return "struct", None
    if s.startswith("a"):
        return "atr", float(s[1:])
    raise ValueError(f"Unknown stop {s!r}")


V1_WINDOWS: tuple[str, ...] = ("am", "pm", "rth")
V1_DISPS: tuple[str, ...] = ("1.0", "1.5", "2.0", "3.0")
V1_FVG_MINS: tuple[str, ...] = ("0.0", "0.5")
V1_MODES: tuple[str, ...] = ("with", "against")
V1_VWAPS: tuple[str, ...] = ("off", "on")
V1_ENTRIES: tuple[str, ...] = ("prox", "ce", "mkt")
V1_WAITS: tuple[int, ...] = (5, 15, 30)
V1_STOPS: tuple[str, ...] = ("struct", "a1.5", "a3.0")
V1_TARGETS: tuple[str, ...] = ("1R", "2R", "3R", "none")
V1_HOLDS: tuple[int, ...] = (15, 30, 60)


# --- fvg v1 (24,192 configs) -----------------------------------------------------------------
# Specified 2026-11-23 from reports/ICT strategies to backtest.md (rank 4, a 216-cell grid),
# widened before any run at the user's request ("roughly 25k"): the with/against mode, the window,
# a fourth displacement level, the gap minimum, the market entry and the ATR stops. No FVG run has
# been made yet. A mkt entry has no resting order, so its `wait` is fixed at 0 in the grid.

class FvgV1Config(FrozenModel):
    symbol: str
    timeframe: Literal["1min"] = "1min"
    window: Literal["am", "pm", "rth"] = "rth"
    mode: Literal["with", "against"] = "with"
    disp: Literal["1.0", "1.5", "2.0", "3.0"] = "1.5"
    fvg_min: Literal["0.0", "0.5"] = "0.0"
    vwap: Literal["off", "on"] = "off"
    entry: Literal["prox", "ce", "mkt"] = "prox"
    wait: Literal[0, 5, 15, 30] = 15
    stop: Literal["struct", "a1.5", "a3.0"] = "struct"
    target: Literal["1R", "2R", "3R", "none"] = "2R"
    hold: Literal[15, 30, 60] = 30
