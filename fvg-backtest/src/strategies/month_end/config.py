"""Typed configs + ablation axes for the Treasury month-end long (day session only).

Source: Hartley & Schwarz, "Predictable End-of-Month Treasury Returns" (Federal Reserve working
paper; https://www.kristaschwarz.com/EOM.pdf). Coupon Treasury excess returns are positive and
significant only over the last few days of the calendar month; a long held over those days
earns an annualised Sharpe of about 1 over 1990-2018. Their futures table: 10-year futures earn
9 / 14 / 17 / 22 bp of price over the last 1 / 2 / 3 / 5 days, 30-year futures 15 / 21 / 27 /
33 bp; windows of 7+ days are insignificant. The cause is index-extension and window-dressing
demand from benchmarked holders, which buy at the index "strike" (the month's last pricing
time). Bloomberg moved that pricing time from 15:00 to 16:00 ET on 14 January 2021, and the
4 p.m. window's share of month-end Treasury volume rose from 11.6% (2021) to 20.4% (2025)
(NY Fed, Liberty Street Economics, Sep 2026). An independent futures test (2010-Sep 2026,
ohlcv.io) still finds ZN +5.2 bp a day over the last three days (t = 4.1).
See reports/Futures papers with strong edges.md (rank 1).

Every published number is CLOSE-TO-CLOSE and includes the overnight session. The user does not
hold overnight, so this tests only the DAY-SESSION part of the effect: on each of the last
`window` NYSE trading days of a calendar month, buy at `entry` and sell at `exit`, flat every
night. Nobody has measured how much of the month-end return accrues in that window; this run is
that measurement.

v1 axes (972 configs per contract; one run per contract):
  window       : 1, 2, 3, 4, 5, 6 -- trade on each of the last N NYSE trading days of the month
                 (each day is its own trade). The paper's significant windows are 1-5 days; 6 is
                 the edge where the effect should fade.
  entry        : 08:20, 09:00, 10:00, 11:00, 12:00, 14:00 ET (08:20 = the CBOT day-session open)
  exit         : 15:00   -- the CBOT settlement / former pit close
                 16:00   -- the post-2021 index strike
                 strike  -- 15:00 on month-ends before 14 Jan 2021, 16:00 from then on (follows
                            the index pricing time, the paper's mechanism)
  event_filter : none
                 skip_fomc          -- skip scheduled FOMC statement days
                 skip_fomc_auction  -- also skip days with a fixed-rate Treasury note/bond
                                       auction (configs/calendars/coupon_auctions.csv; the 2/5/7-
                                       year auctions sit in the last week of the month and move
                                       yields into 13:00 ET)
  stop         : none, 0.25, 0.50 -- percent of the entry price below the entry, live intrabar
                 (the paper has no stop)

Fixed: long only; 1-minute bars from 08:00 to 17:00 ET only (nothing outside is loaded, so
nothing is held overnight); one trade per eligible day.
"""

from __future__ import annotations

import csv
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Literal

from src.utils.config_models import FrozenModel

# Day window (NY clock, minutes from midnight): bars from 08:00 up to (not including) 17:00.
DAY_START_MIN = 8 * 60
DAY_END_MIN = 17 * 60
# An entry must fill within this many minutes of its target time, else the day is skipped.
MAX_ENTRY_LAG_MIN = 5
# Bloomberg Treasury index pricing ("strike") time: 15:00 ET before this date, 16:00 ET from it.
STRIKE_SWITCH_DATE = date(2021, 1, 14)
STRIKE_BEFORE_MIN = 15 * 60
STRIKE_AFTER_MIN = 16 * 60

def hhmm_minutes(t: str) -> int:
    """"HH:MM" -> NY minutes from midnight."""
    h, m = t.split(":")
    if not (h.isdigit() and m.isdigit() and 0 <= int(h) < 24 and 0 <= int(m) < 60):
        raise ValueError(f"Bad clock time {t!r}")
    return int(h) * 60 + int(m)


ENTRY_TIMES: dict[str, int] = {t: hhmm_minutes(t) for t in
                               ("08:20", "09:00", "09:30", "10:00", "10:30", "11:00", "12:00", "13:00", "14:00", "15:00")}
EXIT_RULES = ("15:00", "16:00", "strike")
EVENT_FILTERS = ("none", "skip_fomc", "skip_fomc_auction")

V1_WINDOWS: tuple[int, ...] = (1, 2, 3, 4, 5, 6)
V1_ENTRIES: tuple[str, ...] = ("08:20", "09:00", "10:00", "11:00", "12:00", "14:00")
V1_EXITS: tuple[str, ...] = EXIT_RULES
V1_EVENT_FILTERS: tuple[str, ...] = EVENT_FILTERS
V1_STOPS: tuple[str, ...] = ("none", "0.25", "0.50")

# Scheduled FOMC statement days (federalreserve.gov meeting calendars), plus the 3 Mar 2020
# intermeeting cut (a weekday statement; the 15 Mar 2020 one was a Sunday).
FOMC_DAYS: frozenset[date] = frozenset(date.fromisoformat(d) for d in (
    "2018-01-31", "2018-03-21", "2018-05-02", "2018-06-13", "2018-08-01", "2018-09-26", "2018-11-08", "2018-12-19",
    "2019-01-30", "2019-03-20", "2019-05-01", "2019-06-19", "2019-07-31", "2019-09-18", "2019-10-30", "2019-12-11",
    "2020-01-29", "2020-03-03", "2020-04-29", "2020-06-10", "2020-07-29", "2020-09-16", "2020-11-05", "2020-12-16",
    "2021-01-27", "2021-03-17", "2021-04-28", "2021-06-16", "2021-07-28", "2021-09-22", "2021-11-03", "2021-12-15",
    "2022-01-26", "2022-03-16", "2022-05-04", "2022-06-15", "2022-07-27", "2022-09-21", "2022-11-02", "2022-12-14",
    "2023-02-01", "2023-03-22", "2023-05-03", "2023-06-14", "2023-07-26", "2023-09-20", "2023-11-01", "2023-12-13",
    "2024-01-31", "2024-03-20", "2024-05-01", "2024-06-12", "2024-07-31", "2024-09-18", "2024-11-07", "2024-12-18",
    "2025-01-29", "2025-03-19", "2025-05-07", "2025-06-18", "2025-07-30", "2025-09-17", "2025-10-29", "2025-12-10",
    "2026-01-28", "2026-03-18", "2026-04-29", "2026-06-17", "2026-07-29", "2026-09-16", "2026-10-28", "2026-12-09",
))

AUCTION_CSV = Path(__file__).resolve().parents[3] / "configs" / "calendars" / "coupon_auctions.csv"


@lru_cache(maxsize=None)
def auction_days(path: str = str(AUCTION_CSV)) -> frozenset[date]:
    """Dates of fixed-rate Treasury note and bond auctions (TIPS included, FRNs excluded), from
    the Treasury's Fiscal Data auctions_query API, Dec 2017 - Oct 2026."""
    with open(path, newline="") as f:
        return frozenset(date.fromisoformat(r["auction_date"]) for r in csv.DictReader(f))


def strike_minutes(day: date) -> int:
    return STRIKE_AFTER_MIN if day >= STRIKE_SWITCH_DATE else STRIKE_BEFORE_MIN


def exit_minutes(rule: str, day: date) -> int:
    """The exit target (NY minutes) of an exit rule on `day`."""
    if rule == "strike":
        return strike_minutes(day)
    try:
        return hhmm_minutes(rule)
    except ValueError:
        raise ValueError(f"Unknown exit rule {rule!r}") from None


class _MonthEndConfig(FrozenModel):
    symbol: str
    timeframe: Literal["1min"] = "1min"
    window: Literal[1, 2, 3, 4, 5, 6] = 3
    entry: Literal["08:20", "09:00", "10:00", "11:00", "12:00", "14:00"] = "08:20"
    exit: Literal["15:00", "16:00", "strike"] = "strike"
    event_filter: Literal["none", "skip_fomc", "skip_fomc_auction"] = "none"
    stop: Literal["none", "0.25", "0.50"] = "none"

    @property
    def stop_pct_value(self) -> float | None:
        return None if self.stop == "none" else float(self.stop)


# --- month_end v1 (972 configs) ----------------------------------------------------------------
# Specified 2026-11-22 from reports/Futures papers with strong edges.md (rank 1), day session
# only at the user's request (no overnight). Enlarged the same day, before any run, at the user's
# request ("around 1k configs"): window 6, entries 09:00 and 11:00, and the stop axis added
# (180 -> 972). No month-end run has been made yet.

class MonthEndV1Config(_MonthEndConfig):
    pass


# --- month_end v2 (4,864 configs) ----------------------------------------------------------------
# Specified by the user (2026-11-22) after v1 on ZN (me_zn_v1: 972 configs, 2 frozen, 0 passed
# 2023-2024): "a wider config like 5k, run it on ES". Equity index futures have their own calendar
# effect, the TURN OF THE MONTH: McConnell & Xu (2008, Financial Analysts Journal) find that the
# last trading day of a month and the first three of the next carried essentially all of the US
# equity premium, 1926-2005 (month-end pension / payroll flows; Etula, Rinne, Suominen & Vaittinen,
# RFS 2020, tie it to monthly institutional cash needs). reports/Futures papers with strong
# edges.md rated the ES evidence as conflicting (one Fed study finds the effect gone in S&P futures
# after 1990; CXO finds the first day still pays, mostly intraday). v2 spans both sides of the
# turn, day session only:
#   window       : 0-4 -- the month's last N trading days (0 = none)
#   first_days   : 0-3 -- the next month's first N trading days (0 = none); window = first = 0
#                  is not in the grid
#   entry        : 09:30 (the open), 10:00, 10:30, 11:00, 12:00, 13:00, 14:00, 15:00 ET
#   exit         : 12:00, 13:00, 15:00, 15:30, 16:00 (the close) ET; only pairs with the exit
#                  after the entry are in the grid (32 pairs)
#   event_filter : none, skip_fomc
#   stop         : none, 0.25, 0.50, 1.00 percent below the entry
# 19 day sets x 32 clocks x 2 filters x 4 stops = 4,864.
V2_WINDOWS: tuple[int, ...] = (0, 1, 2, 3, 4)
V2_FIRST_DAYS: tuple[int, ...] = (0, 1, 2, 3)
V2_ENTRIES: tuple[str, ...] = ("09:30", "10:00", "10:30", "11:00", "12:00", "13:00", "14:00", "15:00")
V2_EXITS: tuple[str, ...] = ("12:00", "13:00", "15:00", "15:30", "16:00")
V2_EVENT_FILTERS: tuple[str, ...] = ("none", "skip_fomc")
V2_STOPS: tuple[str, ...] = ("none", "0.25", "0.50", "1.00")


class MonthEndV2Config(FrozenModel):
    symbol: str
    timeframe: Literal["1min"] = "1min"
    window: Literal[0, 1, 2, 3, 4] = 1
    first_days: Literal[0, 1, 2, 3] = 3
    entry: Literal["09:30", "10:00", "10:30", "11:00", "12:00", "13:00", "14:00", "15:00"] = "09:30"
    exit: Literal["12:00", "13:00", "15:00", "15:30", "16:00"] = "16:00"
    event_filter: Literal["none", "skip_fomc"] = "none"
    stop: Literal["none", "0.25", "0.50", "1.00"] = "none"

    @property
    def stop_pct_value(self) -> float | None:
        return None if self.stop == "none" else float(self.stop)
