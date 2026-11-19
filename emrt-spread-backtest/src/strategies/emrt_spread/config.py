"""Typed configs + ablation axes for the EMRT two-leg spread strategy.

Source: Ning & Lee, "Advanced Statistical Arbitrage with Reinforcement Learning" (arXiv 2403.12180,
Purdue Statistics). The spread of a pair (A, B) is A - beta x B; the paper picks beta by minimising
the EMPIRICAL MEAN-REVERSION TIME (EMRT): the average time from each "important extremum" of the
formation-window spread back to its sample mean. An important minimum is a point that is the lowest
of some segment whose two ends are both at least C x s above it (s = the spread's sample sd); maxima
likewise. Here the reinforcement-learning trading layer is NOT used: a plain sigma band trades the
spread (the paper's RL policy only matters if a band on the EMRT spread already works).

Spread units (notional): per $1 of A, short $beta of B. With anchors at the last formation bar
(adjusted close A0, raw close RA = A0 - price_adjustment), a_t = (A_t - A0) / RA and likewise b_t;
S_t = a_t - beta x b_t. Point differences of the back-adjusted series are real P&L, so only
differences of adjusted prices enter S and the anchors' raw prices scale them.

A pair is the experiment's `symbol`, written "A-B" (e.g. "ES-NQ"); leg A is the first.

v1 axes (51,840 configs per pair):
  timeframe   : 15min, 30min, 1h
  formation   : 3, 6, 12  (months of bars before the trading month; refit at each month start)
  hedge       : emrt_c1.5, emrt_c2.0, emrt_c2.5 -- the EMRT-minimising beta at that C
                ols       -- CONTROL: the formation-window OLS slope of a on b
                notional  -- CONTROL: beta = 1 (dollar-neutral 1:1)
  z_mode      : formation   -- z from the formation window's mean / sd of S (the paper)
                rolling_W   -- z from the last W bars' mean / sd of S (same beta), W = 50, 100, 250
  entry_z     : 1.0, 1.5, 2.0, 2.5   (enter on a fresh cross beyond -/+ this)
  exit        : mean      -- close when z gets back to 0
                half      -- close when z gets back inside -/+ entry_z / 2
  stop        : none, 1.5, 2.5       (close when |z| >= entry_z + this, against the position)
  time_stop   : none, 3emrt          (close after ceil(3 x the spread's EMRT) bars)
  side        : both, long, short    (long spread = long A, short beta x B)
  overnight   : flat      -- every position closed at the session's last close
                hold      -- positions may be held across sessions (roll costs charged)
"""

from __future__ import annotations

from typing import Literal

from src.utils.config_models import FrozenModel

V1_TIMEFRAMES: tuple[str, ...] = ("15min", "30min", "1h")
V1_FORMATIONS: tuple[int, ...] = (3, 6, 12)
V1_HEDGES: tuple[str, ...] = ("emrt_c1.5", "emrt_c2.0", "emrt_c2.5", "ols", "notional")
V1_Z_MODES: tuple[str, ...] = ("formation", "rolling_50", "rolling_100", "rolling_250")
V1_ENTRY_ZS: tuple[float, ...] = (1.0, 1.5, 2.0, 2.5)
V1_EXITS: tuple[str, ...] = ("mean", "half")
V1_STOPS: tuple[str, ...] = ("none", "1.5", "2.5")
V1_TIME_STOPS: tuple[str, ...] = ("none", "3emrt")
V1_SIDES: tuple[str, ...] = ("both", "long", "short")
V1_OVERNIGHTS: tuple[str, ...] = ("flat", "hold")

HEDGES = V1_HEDGES
Z_MODES = V1_Z_MODES
EXITS = V1_EXITS
SIDES = V1_SIDES
OVERNIGHTS = V1_OVERNIGHTS

# Fixed settings (not ablated in v1).
BETA_MIN, BETA_MAX, BETA_STEP = 0.20, 3.00, 0.01   # EMRT search grid (notional ratio); OLS is clipped to it
VARIANCE_CAP = 2.0          # EMRT beta needs var(S) <= VARIANCE_CAP x var(S at the OLS beta)
MIN_PIVOTS = 4              # an EMRT needs at least this many important extrema (else not eligible)
CONTROL_C = 2.0             # C used for the EMRT of the OLS / notional spreads (time stop only)
TIME_STOP_EMRT_MULT = 3.0   # time_stop = 3emrt
LAST_ENTRY_CUTOFF_MINUTES = 30


def hedge_name(c: float) -> str:
    """Canonical EMRT hedge name: 2.0 -> "emrt_c2.0", 1.75 -> "emrt_c1.75"."""
    c = round(float(c), 6)
    return f"emrt_c{c:.1f}" if round(c, 1) == c else f"emrt_c{c:g}"


GRID_CS: tuple[float, ...] = (1.5, 2.0, 2.5)


def hedge_c(hedge: str) -> float | None:
    """The C of an EMRT hedge ("emrt_c2.0" -> 2.0); None for the controls."""
    if hedge.startswith("emrt_c"):
        return float(hedge[len("emrt_c"):])
    if hedge in ("ols", "notional"):
        return None
    raise ValueError(f"Unknown hedge {hedge!r}")


def z_kind(z_mode: str) -> tuple[str, int | None]:
    """("formation", None) | ("rolling", W bars) | ("tod", N sessions)."""
    if z_mode == "formation":
        return "formation", None
    for kind, lo in (("rolling", 10), ("tod", 5)):
        pre = f"{kind}_"
        if z_mode.startswith(pre) and z_mode[len(pre):].isdigit() and int(z_mode[len(pre):]) >= lo:
            return kind, int(z_mode[len(pre):])
    raise ValueError(f"Unknown z_mode {z_mode!r}")


def rolling_window(z_mode: str) -> int | None:
    """Bars of a rolling z ("rolling_100" -> 100); None for any other z (formation, time of day)."""
    kind, w = z_kind(z_mode)
    return w if kind == "rolling" else None


def tod_sessions(z_mode: str) -> int | None:
    """Sessions of a time-of-day z ("tod_20" -> 20); None otherwise."""
    kind, w = z_kind(z_mode)
    return w if kind == "tod" else None


def split_pair(pair: str) -> tuple[str, str]:
    a, sep, b = pair.partition("-")
    if not sep or not a or not b or "-" in b:
        raise ValueError(f"A pair is written 'A-B' (e.g. 'ES-NQ'), got {pair!r}")
    return a, b


class _EMRTConfig(FrozenModel):
    symbol: str                      # the pair, "A-B"
    timeframe: Literal["15min", "30min", "1h"] = "15min"
    formation: Literal[3, 6, 12] = 6
    hedge: Literal["emrt_c1.5", "emrt_c2.0", "emrt_c2.5", "ols", "notional"] = "emrt_c2.0"
    z_mode: Literal["formation", "rolling_50", "rolling_100", "rolling_250"] = "formation"
    entry_z: Literal[1.0, 1.5, 2.0, 2.5] = 2.0
    exit: Literal["mean", "half"] = "mean"
    stop: Literal["none", "1.5", "2.5"] = "none"
    time_stop: Literal["none", "3emrt"] = "none"
    side: Literal["both", "long", "short"] = "both"
    overnight: Literal["flat", "hold"] = "flat"

    @property
    def stop_z_value(self) -> float | None:
        return None if self.stop == "none" else float(self.stop)


# --- emrt_spread v1 (51,840 configs per pair) -------------------------------------------------
# Specified by the user (2026-11-18) from the Purdue research report
# (reports/Purdue trading strategy research.md, Pick 3), before any EMRT run was made.

class EMRTV1Config(_EMRTConfig):
    pass


# --- emrt_spread v2: session-anchored, intraday only (13,824 configs per pair) ----------------
# Specified by the user (2026-11-18) after v1 on ES-NQ (emrt_esnq_v1: 16 frozen, all holding
# overnight; 0 of the 25,920 flat-at-close configs passed the profit gate) because prop accounts
# must be flat by the close. Each leg is measured from TODAY's open:
#     a_k = (A_k - A_open) / A_open_raw,   b_k likewise,   S_k = a_k - beta x b_k
# (A_open = the session's first bar open), so S starts every session at ~0 and every trade is
# flat by the session close. beta is fit monthly on these intraday spreads (important extrema and
# their reversion counted within a session only; a swing not back by the close is censored there).
#   z_mode formation : (S_k - formation mean) / formation sd
#   z_mode tod_N     : (S_k - mean) / sd of S at the SAME bar of the session over the previous N
#                      sessions (time-of-day normalisation; same beta)
#   first_entry      : no entry decision before this many minutes after the open (0 / 30)
V2_TIMEFRAMES: tuple[str, ...] = ("5min", "15min")
V2_FORMATIONS: tuple[int, ...] = (1, 3, 6)
V2_HEDGES: tuple[str, ...] = ("emrt_c1.5", "emrt_c2.0", "ols", "notional")
V2_Z_MODES: tuple[str, ...] = ("formation", "tod_20", "tod_60")
V2_ENTRY_ZS: tuple[float, ...] = (1.0, 1.5, 2.0, 2.5)
V2_EXITS: tuple[str, ...] = ("mean", "half")
V2_STOPS: tuple[str, ...] = ("none", "1.5")
V2_TIME_STOPS: tuple[str, ...] = ("none", "3emrt")
V2_SIDES: tuple[str, ...] = ("both", "long", "short")
V2_FIRST_ENTRIES: tuple[int, ...] = (0, 30)
V2_OVERNIGHTS: tuple[str, ...] = ("flat",)


class EMRTV2Config(_EMRTConfig):
    timeframe: Literal["5min", "15min"] = "15min"
    formation: Literal[1, 3, 6] = 3
    hedge: Literal["emrt_c1.5", "emrt_c2.0", "ols", "notional"] = "emrt_c2.0"
    z_mode: Literal["formation", "tod_20", "tod_60"] = "tod_20"
    stop: Literal["none", "1.5"] = "none"
    first_entry: Literal[0, 30] = 0
    overnight: Literal["flat"] = "flat"
    anchor: Literal["session"] = "session"
