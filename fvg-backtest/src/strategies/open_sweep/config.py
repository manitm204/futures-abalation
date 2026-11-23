"""Typed configs + ablation axes for the NY-open liquidity sweep (ICT Judas / Venom / NY-open
reversal, and its continuation control) on equity index futures, 1-minute bars.

Source: reports/ICT strategies to backtest.md (rank 1). ICT teaches that at the 09:30 open price
"sweeps" an obvious pool of resting stops -- the overnight high/low, the prior session's high/low,
the London-session high/low or the 08:00-09:30 "Venom box" -- and then reverses (the Judas swing).
Independent tests disagree on the direction: a 25k-config ES/NQ Silver Bullet study found that a
sweep requirement was the one rule that added edge, while a walk-forward FX study found swept
levels predicted CONTINUATION in 65 of 66 folds (and Osler's stop-order data fits continuation).
So every setting is run in both modes; the continuation arm is the control.

Per session (NY date D), a range [L, H] is known before 09:30:
  level : onh  -- overnight Globex session, 18:00 (D-1) .. 09:30
          asia -- 20:00 .. 00:00 (the session's evening bars)
          lon  -- London, 02:00 .. 05:00
          box  -- the "Venom box", 08:00 .. 09:30
          pdr  -- the prior RTH session's high / low (09:30 .. 16:00)
  side  : both / high / low -- which side's sweep may trigger a trade (both = the first to trigger)
  window: 15 / 30 / 60 -- the penetration AND the trigger must happen within this many minutes
          after 09:30
  pen   : 0.00 / 0.05 -- the penetration must exceed the level by more than pen x dATR
          (dATR = mean RTH high-low range of the previous 14 sessions)
  confirm: 1 / 3 / 5 bars
          fade -- the first close back inside the range within `confirm` bars of the penetration
                  bar (the penetration bar itself counts as bar 1) -> trade AGAINST the sweep
          cont -- `confirm` consecutive closes beyond the level, starting with the penetration
                  bar -> trade WITH the break
  mode  : fade / cont
  stop  : struct -- beyond the sweep's extreme (fade) or the break's low/high (cont) +2 ticks;
          d0.10 / d0.20 -- 0.10 / 0.20 x dATR from the entry. Every stop is at least
          0.03 x dATR from the entry (the cost wall: NQ round trip ~0.75 point).
  target: none / 1R / 2R / 3R / range -- range = the opposite side of [L, H] (fade) or a
          measured move of one range height beyond the broken level (cont)
  exit  : 11:00 / 12:30 / 16:00 -- time exit (16:00 = the session's last RTH bar)

Execution: entry at the open of the bar after the trigger bar; stop live intrabar (stop first);
target as a limit needing a 1-tick trade-through, filled at the target; one trade per session;
flat by 16:00. 5 x 3 x 3 x 2 x 3 x 2 x 3 x 5 x 3 = 24,300 configs.
"""

from __future__ import annotations

from typing import Literal

from src.utils.config_models import FrozenModel

DAY_START_MIN = 9 * 60 + 30     # 09:30 ET
DAY_END_MIN = 16 * 60           # 16:00 ET
EVENING_START_MIN = 18 * 60     # Globex reopens 18:00 ET; those bars carry the NEXT session date
# The 09:30 open must come from a bar opening within this many minutes of 09:30.
MAX_OPEN_LAG_MIN = 2
# The entry bar must open within this many minutes of the trigger bar's open.
MAX_ENTRY_GAP_MIN = 2
# dATR: mean RTH (high - low) range of the previous DATR_LOOKBACK sessions (all defined).
DATR_LOOKBACK = 14
# Structural stops sit this many ticks beyond the extreme; every stop is >= MIN_STOP_DATR x dATR.
STRUCT_PAD_TICKS = 2
MIN_STOP_DATR = 0.03
# A pre-open level needs at least this share of its window's minutes to have bars.
LEVEL_MIN_COVERAGE = 0.5
# Target limit orders fill only when the bar trades this many ticks through the target.
TARGET_THROUGH_TICKS = 1

# Level windows, NY minutes [start, end). `onh` spans the evening (>= 18:00) + [0, 09:30).
LEVEL_WINDOWS: dict[str, tuple[int, int] | None] = {
    "onh": None,
    "asia": (20 * 60, 24 * 60),
    "lon": (2 * 60, 5 * 60),
    "box": (8 * 60, 9 * 60 + 30),
    "pdr": None,
}
LEVELS = ("onh", "asia", "lon", "box", "pdr")
PRE_OPEN_LEVELS = ("onh", "asia", "lon", "box")


def level_minutes(level: str) -> int:
    """Minutes in a pre-open level's window (for the coverage check)."""
    if level == "onh":
        return (24 * 60 - EVENING_START_MIN) + DAY_START_MIN
    a, b = LEVEL_WINDOWS[level]
    return b - a


def parse_stop(s: str) -> tuple[str, float | None]:
    if s == "struct":
        return "struct", None
    if s.startswith("d"):
        return "datr", float(s[1:])
    raise ValueError(f"Unknown stop {s!r}")


def parse_target(t: str) -> tuple[str, float | None]:
    if t in ("none", "range"):
        return t, None
    if t.endswith("R"):
        return "r", float(t[:-1])
    raise ValueError(f"Unknown target {t!r}")


def hhmm_minutes(t: str) -> int:
    h, m = t.split(":")
    if not (h.isdigit() and m.isdigit() and 0 <= int(h) < 24 and 0 <= int(m) < 60):
        raise ValueError(f"Bad clock time {t!r}")
    return int(h) * 60 + int(m)


V1_LEVELS: tuple[str, ...] = LEVELS
V1_SIDES: tuple[str, ...] = ("both", "high", "low")
V1_WINDOWS: tuple[int, ...] = (15, 30, 60)
V1_PENS: tuple[str, ...] = ("0.00", "0.05")
V1_CONFIRMS: tuple[int, ...] = (1, 3, 5)
V1_MODES: tuple[str, ...] = ("fade", "cont")
V1_STOPS: tuple[str, ...] = ("struct", "d0.10", "d0.20")
V1_TARGETS: tuple[str, ...] = ("none", "1R", "2R", "3R", "range")
V1_EXITS: tuple[str, ...] = ("11:00", "12:30", "16:00")


# --- open_sweep v1 (24,300 configs) ---------------------------------------------------------
# Specified 2026-11-22 from reports/ICT strategies to backtest.md (rank 1, a 432-cell grid),
# widened before any run at the user's request ("roughly 25k configurations"): the Asia level,
# the side and penetration axes, a fifth confirm/target level and the time-exit axis. No
# open-sweep run has been made yet.

class OpenSweepV1Config(FrozenModel):
    symbol: str
    timeframe: Literal["1min"] = "1min"
    level: Literal["onh", "asia", "lon", "box", "pdr"] = "onh"
    side: Literal["both", "high", "low"] = "both"
    window: Literal[15, 30, 60] = 30
    pen: Literal["0.00", "0.05"] = "0.00"
    confirm: Literal[1, 3, 5] = 1
    mode: Literal["fade", "cont"] = "fade"
    stop: Literal["struct", "d0.10", "d0.20"] = "struct"
    target: Literal["none", "1R", "2R", "3R", "range"] = "2R"
    exit: Literal["11:00", "12:30", "16:00"] = "16:00"
