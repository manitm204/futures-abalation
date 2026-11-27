"""Typed configs + ablation axes for last-half-hour momentum (equity index futures, RTH only).

Source: Baltussen, Da, Lammers & Martens, "Hedging demand and market intraday momentum",
Journal of Financial Economics 142 (2021); https://academicweb.nd.edu/~zda/intramom.pdf. Across
60+ futures, 1974-2020, the return from the previous close to 30 minutes before today's close
(rROD) predicts the last 30 minutes. For equity index futures, "long the last half hour if
rROD > 0, else short" earned 6.86% a year gross at 3.96% volatility (Sharpe 1.73, 55% hit
rate); requiring rROD and the first-half-hour return to agree gave a 61% hit rate. The cause is
dealers and leveraged ETFs hedging short gamma in the direction of the day's move, so the effect
is much stronger on negative-gamma days. Post-2013 replications find the unconditional slope
near zero (SPY 2013-2019; SPX 2022-2026), while the slope on short-gamma days stays positive.
The bars cannot see dealer gamma, so this grid tests bar-observable stand-ins: a large move so
far (|signal| in units of its own 20-day standard deviation), a high-volatility regime, and down
days only (put-heavy hedging). See reports/Futures papers with strong edges.md (rank 2).

v1 axes (500 configs per contract):
  signal  : prev_close -- prior session's last RTH close to the decision time (rROD, the paper's)
            open       -- today's 09:30 open to the decision time (no overnight gap)
            first_half -- prior close to 10:00 (Gao, Han, Li & Zhou 2018; ignores the rest of the day)
  agree   : off / on -- on = trade only when the signal and the first-half-hour return (prior
            close to 10:00) have the same sign. Only with prev_close and open (with first_half
            it is the signal itself, so not in the grid).
  window  : entry-exit, ET. 15:30-16:00 is the paper's; 15:00-16:00 the last hour; 15:30-15:50
            avoids the closing auction; 15:45-16:00 and 15:50-16:00 the late window, where a
            thesis finds most of the remaining predictability (Aalto).
  filter  : none
            z0.5 / z1.0 -- trade only when |signal| > 0.5 / 1.0 x the standard deviation of the
                           same signal over the previous 20 sessions
            rv_high     -- trade only when the 20-day realized volatility of daily RTH-close
                           returns is above its median over the previous 120 sessions
            down_only   -- trade only when the signal is negative (so only shorts)
  stop    : none, 0.10, 0.20, 0.40 -- percent of the entry price against the position, live
            intrabar

Direction: long if the signal > 0, short if < 0, no trade if 0. The decision uses the close of
the last bar that opens before the entry time; the entry fills at the next bar's open. Fixed:
1-minute bars 09:30-16:00 ET only; one trade per session; flat every night.
5 signal variants x 5 windows x 5 filters x 4 stops = 500.
"""

from __future__ import annotations

from typing import Literal

from src.utils.config_models import FrozenModel

# RTH window (NY clock, minutes from midnight): bars from 09:30 up to (not including) 16:00.
DAY_START_MIN = 9 * 60 + 30
DAY_END_MIN = 16 * 60
# The first-half-hour return ends at the close of the last bar opening before 10:00.
FIRST_HALF_END_MIN = 10 * 60
# An entry (and the decision bar before it) must be within this many minutes of the target time.
MAX_ENTRY_LAG_MIN = 2
# The 09:30 open must come from a bar opening within this many minutes of 09:30.
MAX_OPEN_LAG_MIN = 5
# z filters: standard deviation of the signal over the previous Z_LOOKBACK sessions.
Z_LOOKBACK = 20
Z_MIN_PERIODS = 15
# rv_high: RV over RV_LOOKBACK daily returns vs its median over the previous RV_MEDIAN_LOOKBACK.
RV_LOOKBACK = 20
RV_MEDIAN_LOOKBACK = 120
RV_MEDIAN_MIN_PERIODS = 60

SIGNALS = ("prev_close", "open", "first_half")
FILTERS = ("none", "z0.5", "z1.0", "rv_high", "down_only")


def hhmm_minutes(t: str) -> int:
    """"HH:MM" -> NY minutes from midnight."""
    h, m = t.split(":")
    if not (h.isdigit() and m.isdigit() and 0 <= int(h) < 24 and 0 <= int(m) < 60):
        raise ValueError(f"Bad clock time {t!r}")
    return int(h) * 60 + int(m)


def window_minutes(w: str) -> tuple[int, int]:
    """"HH:MM-HH:MM" -> (entry, exit) NY minutes."""
    a, b = w.split("-")
    return hhmm_minutes(a), hhmm_minutes(b)


def parse_filter(f: str) -> tuple[str, float | None]:
    """"z0.5" -> ("z", 0.5); others -> (name, None)."""
    if f.startswith("z"):
        return "z", float(f[1:])
    if f not in FILTERS:
        raise ValueError(f"Unknown filter {f!r}")
    return f, None


V1_SIGNALS: tuple[str, ...] = SIGNALS
V1_AGREE: tuple[str, ...] = ("off", "on")
V1_WINDOWS: tuple[str, ...] = ("15:00-16:00", "15:30-15:50", "15:30-16:00", "15:45-16:00", "15:50-16:00")
V1_FILTERS: tuple[str, ...] = FILTERS
V1_STOPS: tuple[str, ...] = ("none", "0.10", "0.20", "0.40")


# --- last_half_hour v1 (500 configs) ----------------------------------------------------------
# Specified 2026-11-22 from reports/Futures papers with strong edges.md (rank 2: 90 cells),
# widened before any run at the user's request ("maybe like 500 configs"): two more windows
# (15:00-16:00, 15:45-16:00) and the stop axis. No last-half-hour run has been made yet.

class LastHalfHourV1Config(FrozenModel):
    symbol: str
    timeframe: Literal["1min"] = "1min"
    signal: Literal["prev_close", "open", "first_half"] = "prev_close"
    agree: Literal["off", "on"] = "off"
    window: Literal["15:00-16:00", "15:30-15:50", "15:30-16:00", "15:45-16:00", "15:50-16:00"] = "15:30-16:00"
    filter: Literal["none", "z0.5", "z1.0", "rv_high", "down_only"] = "none"
    stop: Literal["none", "0.10", "0.20", "0.40"] = "none"

    @property
    def stop_pct_value(self) -> float | None:
        return None if self.stop == "none" else float(self.stop)


# --- last_half_hour v2 (1,296 configs per contract) --------------------------------------------
# Specified 2026-11-26 at the user's request ("a lot more variables ... how much is the change, is
# the intraday momentum pointing the other way, is there sufficient volume"), after v1 on NQ (16 of
# 500 passed validation; the prior-close -> 15:00 cluster; #49 +0.8% and #56 -3.7% on 2025+).
#   signal    : prev_close / open               (the day's move so far, as in v1)
#   window    : 15:00-16:00 / 15:30-16:00
#   filter    : none / z0.5 / z1.0              (how big the day's move is, in units of its own 20-day sd)
#   fh_rel    : any / same / opp                (first-half-hour move, prior close -> 10:00, has the same / the
#                                                opposite sign to the day's move)
#   late_rel  : any / same / opp                (the move over the LATE_MIN minutes before the entry, has the
#                                                same / the opposite sign to the day's move: is the late-day
#                                                momentum pointing the other way?)
#   vol_gate  : none / 1.0 / 1.5                (volume over the LATE_MIN minutes before the entry / its
#                                                time-of-day norm over the prior 20 sessions >= the gate)
#   direction : follow / fade                   (trade with or against the day's move)
#   stop      : none / 0.20                     (percent against the entry)
# 2 x 2 x 3 x 3 x 3 x 3 x 2 x 2 = 1,296.
LATE_MIN = 60
VOLUME_LOOKBACK_SESSIONS = 20
VOLUME_MIN_SESSIONS = 10

V2_SIGNALS: tuple[str, ...] = ("prev_close", "open")
V2_WINDOWS: tuple[str, ...] = ("15:00-16:00", "15:30-16:00")
V2_FILTERS: tuple[str, ...] = ("none", "z0.5", "z1.0")
V2_RELS: tuple[str, ...] = ("any", "same", "opp")
V2_VOL_GATES: tuple[str, ...] = ("none", "1.0", "1.5")
V2_DIRECTIONS: tuple[str, ...] = ("follow", "fade")
V2_STOPS: tuple[str, ...] = ("none", "0.20")


class LastHalfHourV2Config(FrozenModel):
    symbol: str
    timeframe: Literal["1min"] = "1min"
    signal: Literal["prev_close", "open"] = "prev_close"
    window: Literal["15:00-16:00", "15:30-16:00"] = "15:00-16:00"
    filter: Literal["none", "z0.5", "z1.0"] = "none"
    fh_rel: Literal["any", "same", "opp"] = "any"
    late_rel: Literal["any", "same", "opp"] = "any"
    vol_gate: Literal["none", "1.0", "1.5"] = "none"
    direction: Literal["follow", "fade"] = "follow"
    stop: Literal["none", "0.20"] = "none"

    @property
    def stop_pct_value(self) -> float | None:
        return None if self.stop == "none" else float(self.stop)

    @property
    def vol_gate_value(self) -> float | None:
        return None if self.vol_gate == "none" else float(self.vol_gate)
