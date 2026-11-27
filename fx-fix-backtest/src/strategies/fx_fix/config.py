"""Typed configs + ablation axes for the FX-fix reversal strategy (daytime legs only).

Source: Krohn, Mueller & Whelan, "Foreign Exchange Fixings and Returns Around the Clock",
Journal of Finance 79(1), 2024 (Bank of Canada SWP 2021-48). The USD appreciates in the run-up
to the big FX fixes and depreciates after them. The paper's windows (ET) are: pre-Tokyo,
post-Tokyo, pre-ECB (02:00-08:15), ECB-to-London (08:15-11:00) and post-London (11:00-17:00).
Net of half the spot spread the post-London reversal stayed profitable through 2019, while the
Tokyo legs decayed after ~2013.

The user does not trade overnight, so only the two DAYTIME windows are tested:
  post-London : the USD falls after the 16:00 London (WM/R) fix -> LONG 6E (6E is USD per EUR,
                so long the future = short the USD).
  pre-London  : the USD rises into the London fix -> SHORT 6E, from the ECB fix (14:15
                Frankfurt) to the London fix. The paper reports no clear sign for this window,
                so it is the exploratory half of the grid.
Every fix time is built in the fix's OWN time zone (Europe/London, Europe/Berlin) and converted
to New York per session date, so the weeks when US and European daylight saving disagree are
right (the London fix is then 12:00 ET instead of 11:00 ET).

v1 axes (405 configs; one run per contract):
  leg           : post   -- long from the switch time for `post_hold`
                  pre    -- short from the ECB fix to the switch time
                  both   -- the pre leg, then the post leg (two trades a day)
  switch_offset : -15, -5, 0, 5, 15  minutes relative to the London fix. The post leg enters at
                  fix + offset; the pre leg exits at fix + offset. 0 = the paper's boundary.
  post_hold     : 60, 120, 240 minutes after the post entry, or "eod" (the last bar before
                  17:00 ET, the paper's end of day). Not used by leg = pre (fixed to "eod" there,
                  so the pre leg has no duplicate configs).
  vol_gate      : none -- trade every day
                  high -- only when the trailing 20-day mean of daily realized vol (5-minute
                          returns, 08:00-17:00 ET) is above its trailing 250-day median (the
                          paper finds bigger reversals in volatile periods)
                  low  -- only when it is at or below that median (the control for `high`)
  stop          : none, 0.25, 0.50  percent of the entry price (the paper has no stop)

Fixed: 1-minute bars from 08:00 to 17:00 ET only (nothing before 08:00 or after 17:00 is ever
loaded into the strategy, so nothing can be held overnight); at most one position at a time;
flat by 17:00 ET.
"""

from __future__ import annotations

from typing import Literal

from src.utils.config_models import FrozenModel

# Day window (NY clock, minutes from midnight): bars from 08:00 up to (not including) 17:00.
DAY_START_MIN = 8 * 60
DAY_END_MIN = 17 * 60
# Fixes in their own time zones.
LONDON_FIX = ("Europe/London", 16, 0)   # WM/R 4 pm London fix
ECB_FIX = ("Europe/Berlin", 14, 15)     # ECB reference rate, 14:15 CET/CEST
# An entry must fill within this many minutes of its target time, else the day is skipped
# (a gap in the 1-minute bars should not turn into a much later, different trade).
MAX_ENTRY_LAG_MIN = 5
# Realized-vol gate.
RV_SAMPLE_MIN = 5
RV_SHORT_DAYS = 20
RV_LONG_DAYS = 250

LEGS = ("post", "pre", "both")
VOL_GATES = ("none", "high", "low")

V1_LEGS: tuple[str, ...] = ("post", "pre", "both")
V1_SWITCH_OFFSETS: tuple[int, ...] = (-15, -5, 0, 5, 15)
V1_POST_HOLDS: tuple[str, ...] = ("60", "120", "240", "eod")
V1_VOL_GATES: tuple[str, ...] = ("none", "high", "low")
V1_STOPS: tuple[str, ...] = ("none", "0.25", "0.50")


def post_hold_minutes(post_hold: str) -> int | None:
    """Minutes the post leg is held (None = until the last bar before 17:00 ET)."""
    if post_hold == "eod":
        return None
    if post_hold.isdigit() and int(post_hold) > 0:
        return int(post_hold)
    raise ValueError(f"Unknown post_hold {post_hold!r}")


class _FXFixConfig(FrozenModel):
    symbol: str
    timeframe: Literal["1min"] = "1min"
    leg: Literal["post", "pre", "both"] = "post"
    switch_offset: Literal[-15, -5, 0, 5, 15] = 0
    post_hold: Literal["60", "120", "240", "eod"] = "eod"
    vol_gate: Literal["none", "high", "low"] = "none"
    stop: Literal["none", "0.25", "0.50"] = "none"

    @property
    def stop_pct_value(self) -> float | None:
        return None if self.stop == "none" else float(self.stop)


# --- fx_fix v1 (405 configs) -------------------------------------------------------------------
# Specified 2026-11-20 from reports/Distinct futures strategy papers.md (pick 1, FX-fix W-pattern),
# restricted to the daytime legs at the user's request (no overnight positions). No FX-fix run
# has been made yet.

class FXFixV1Config(_FXFixConfig):
    pass


# --- fx_fix v2 (about 1,200 configs): conditioned post leg -------------------------------------
# Specified 2026-11-27 after v1 (fx_6e_v1 / fx_6j_v1) found no gross edge in the unconditional legs.
# Post leg only. Everything below is known before the entry bar opens:
#   R      : log move of the 1-minute closes from the anchor (ECB fix open, or the 08:00 open) to
#            the bar BEFORE the entry bar (so the entry bar's own open is never used).
#   z      : R divided by the standard deviation of R over the previous 20 sessions (>= 10 needed).
#   trend  : sign of the previous session's last close vs the close 20 sessions earlier.
#   month  : last two weekdays of a month or the first weekday of the next (calendar rule, no holidays).
# direction: long      -- always long 6E (the v1 rule)
#            reversal  -- trade against R: long 6E if R < 0 (USD ran up into the fix), short if R > 0
#            momentum  -- trade with R
# move     : any | small (|z| < MOVE_Z) | big (|z| >= MOVE_Z)
# trend    : any | aligned (trade side == trend sign) | counter (trade side == -trend sign)
# month    : any | me (month-end window only)
MOVE_Z = 1.0
MOVE_LOOKBACK = 20
MOVE_MIN_SESSIONS = 10
TREND_DAYS = 20
V2_ANCHORS: tuple[str, ...] = ("ecb", "open")
V2_DIRECTIONS: tuple[str, ...] = ("long", "reversal", "momentum")
V2_MOVES: tuple[str, ...] = ("any", "small", "big")
V2_TRENDS: tuple[str, ...] = ("any", "aligned", "counter")
V2_MONTHS: tuple[str, ...] = ("any", "me")
V2_SWITCH_OFFSETS: tuple[int, ...] = (0,)
V2_POST_HOLDS: tuple[str, ...] = ("60", "240", "eod")
V2_VOL_GATES: tuple[str, ...] = ("none", "high")
V2_STOPS: tuple[str, ...] = ("none", "0.50")


class FXFixV2Config(_FXFixConfig):
    anchor: Literal["ecb", "open"] = "ecb"
    direction: Literal["long", "reversal", "momentum"] = "long"
    move: Literal["any", "small", "big"] = "any"
    trend: Literal["any", "aligned", "counter"] = "any"
    month: Literal["any", "me"] = "any"
