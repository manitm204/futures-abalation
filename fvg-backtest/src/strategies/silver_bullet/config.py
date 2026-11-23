"""Typed configs + ablation axes for ICT's Silver Bullet / 2022 Model on equity index futures,
1-minute bars, with placebo windows.

Source: reports/ICT strategies to backtest.md (rank 2). Stripped of vocabulary, the Silver Bullet
is: liquidity is swept (price trades through a prior swing high/low and closes back inside), a
displacement leg leaves a three-candle fair value gap (FVG), a limit order rests in the gap, the
stop goes beyond the gap or the sweep, the target is a multiple of risk or the opposite pool. ICT
says it only works in 03:00-04:00, 10:00-11:00 and 14:00-15:00 ET; the 2022 Model is the same
sequence in the wider killzones. Two placebo hours test whether the "special hours" matter, and
the sweep toggle tests whether "liquidity" adds anything to a plain FVG.

Per session (the CME day: 18:00 the evening before .. 16:00 ET), one trade at most:
  window : 10-11 / 14-15 / 03-04  (ICT's Silver Bullet hours)
           kz    (2022 Model killzones 08:30-11:00 and 13:30-16:00)
           p11-12 / p1230-1330  (placebo hours)
           All three FVG bars must open inside one window interval; the order must fill inside it;
           an open position is closed at the window end.
  fvg_min: 0 / 0.5 / 1.0 -- the gap must be > 0 and at least this many ATR
  disp   : 1.0 / 1.5 / 2.0 -- the FVG's middle bar's true range >= this many ATR (displacement)
  entry  : prox / ce -- limit at the gap's near edge, or its midpoint (consequent encroachment)
  stop   : fvg -- beyond the gap's far edge by 2 ticks;
           struct -- beyond the swept extreme by 2 ticks (no qualifying sweep: the extreme of the
           10 bars ending with the FVG's first bar). Every stop is >= 1.0 ATR from the limit.
  target : 2R / 3R / liq / none -- liq = the nearest unswept swing high (long) / low (short) of
           the session beyond the entry, known when the gap is confirmed; none = out at window end
  sweep  : yes / no -- yes requires a same-direction liquidity sweep confirmed within the 60
           minutes before the FVG's first bar opens

ATR = 14-bar simple mean of 1-minute true range, as of the FVG's first bar (before the
displacement). Fixed (not gridded, report's choices): swings 5/5, sweep reclaim within 3 bars, no
market-structure-shift filter, FVG order lives 30 bars, 1-tick trade-through for limit fills.
6 x 3 x 3 x 2 x 2 x 4 x 2 = 1,728 configs.
"""

from __future__ import annotations

from typing import Literal

from src.utils.config_models import FrozenModel

SESSION_END_MIN = 16 * 60        # nothing is traded at or after 16:00 ET
EVENING_START_MIN = 18 * 60      # Globex reopens 18:00 ET; those bars carry the NEXT session date
ATR_LEN = 14
SWING_LEN = 5                    # swing = strictly beyond the 5 bars before, at least the 5 after
SWEEP_RECLAIM_BARS = 3           # a close back inside within 3 bars of the penetration (it counts)
SWEEP_LOOKBACK_MIN = 60          # the sweep must be confirmed within 60 minutes before FVG bar 1
STRUCT_FALLBACK_BARS = 10        # struct stop without a sweep: extreme of the 10 bars to bar 1
MAX_AGE_BARS = 30                # the limit order rests at most 30 bars after the gap's confirmation
PAD_TICKS = 2                    # stops sit 2 ticks beyond their reference
MIN_STOP_ATR = 1.0               # cost wall: stop at least 1 ATR (NQ round trip ~0.75 pt)
THROUGH_TICKS = 1                # limit entries and targets fill only on a 1-tick trade-through

# NY-minute intervals [start, end) per window.
WINDOWS: dict[str, tuple[tuple[int, int], ...]] = {
    "10-11": ((600, 660),),
    "14-15": ((840, 900),),
    "03-04": ((180, 240),),
    "kz": ((510, 660), (810, 960)),
    "p11-12": ((660, 720),),
    "p1230-1330": ((750, 810),),
}


def parse_target(t: str) -> tuple[str, float | None]:
    if t in ("liq", "none"):
        return t, None
    if t.endswith("R"):
        return "r", float(t[:-1])
    raise ValueError(f"Unknown target {t!r}")


V1_WINDOWS: tuple[str, ...] = tuple(WINDOWS)
V1_FVG_MINS: tuple[str, ...] = ("0.0", "0.5", "1.0")
V1_DISPS: tuple[str, ...] = ("1.0", "1.5", "2.0")
V1_ENTRIES: tuple[str, ...] = ("prox", "ce")
V1_STOPS: tuple[str, ...] = ("fvg", "struct")
V1_TARGETS: tuple[str, ...] = ("2R", "3R", "liq", "none")
V1_SWEEPS: tuple[str, ...] = ("yes", "no")


# --- silver_bullet v1 (1,728 configs) -------------------------------------------------------
# Specified 2026-11-22 from reports/ICT strategies to backtest.md (rank 2, a 432-cell grid),
# widened before any run at the user's request ("like 2k configs"): the displacement axis and a
# 3R target. No Silver Bullet run on futures has been made yet (only the 2026-08 SPY pilot).

class SilverBulletV1Config(FrozenModel):
    symbol: str
    timeframe: Literal["1min"] = "1min"
    window: Literal["10-11", "14-15", "03-04", "kz", "p11-12", "p1230-1330"] = "10-11"
    fvg_min: Literal["0.0", "0.5", "1.0"] = "0.0"
    disp: Literal["1.0", "1.5", "2.0"] = "1.5"
    entry: Literal["prox", "ce"] = "prox"
    stop: Literal["fvg", "struct"] = "fvg"
    target: Literal["2R", "3R", "liq", "none"] = "2R"
    sweep: Literal["yes", "no"] = "yes"
