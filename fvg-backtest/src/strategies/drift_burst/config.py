"""Typed configs + ablation axes for the volume-gated drift-burst fade (1-minute day-session bars).

Source: Christensen, Oomen & Renò, "The drift burst hypothesis" (Journal of Econometrics; arXiv
2601.08974). On tick data for ES, the 10-year note, 6E and CL (2010/2012-2017) they detect
"drift bursts": points where local drift is extreme relative to local volatility (t-stat > 4 to
4.5; ~1 a week in ES). About 71% reverse over the next 5 minutes (slope -0.23). Negative bursts
reverse more than positive ones, and bursts on high volume (relative to the time of day) reverse
much more: +42.8 bps vs +14.3 bps for the most-negative quartile. No costs, no trading P&L and no
out-of-sample test in the paper; returns are on mid-quotes.

Simplified detector on 1-minute bars (reports/Distinct futures strategy papers.md, pick 3):
    r_k(t)  = log C_t - log C_{t-k}                                (the k-minute burst return)
    s(t)    = RMS of the 5k one-minute log returns ending at bar t-k (before the burst window)
    T(t)    = r_k(t) / (s(t) * sqrt(k))
Everything inside one session (no overnight returns). A burst PEAKS at bar p when |T_p| > c and
|T| stops rising at the next bar (|T_{p+1}| < |T_p|, or T changes sign / is undefined). The
decision is made at the close of bar p+1 and fills at the open of bar p+2, against the burst.

v1 axes (576 configs per market; one run per market):
  burst_window : 3, 5, 10 minutes (k; 5 = the paper's main bandwidth)
  threshold    : 3.5, 4.0, 4.5, 5.0 (c; the paper uses 4.0 and 4.5)
  vol_gate     : none, 1.5, 2.0, 3.0 -- burst-window volume / the trailing 20-session mean volume
                 of the same minutes of the day must be >= this. (The paper sorts events into
                 volume quartiles after the fact; a fixed multiple of normal volume is the causal
                 version.)
  side         : both      -- fade drops (long) and spikes (short)
                 long_only -- only buy after drops (the paper's negative bursts reverse more)
  hold         : 5, 15, 30 minutes (5 = the paper's measurement window)
  news_filter  : off, on -- on skips bursts whose window or decision bar touches 08:28-08:45,
                 09:58-10:15 (US data releases) or, on Wednesdays, 13:58-15:00 ET (FOMC
                 statement / press conference days are Wednesdays). Unscheduled-news bursts
                 continue rather than reverse (Xiao, Yin & Zhao), so scheduled ones are suspect.

Fixed: at most one trade per market per session (the paper's one event per day); flat at the
session close; nothing held overnight; no stop.
"""

from __future__ import annotations

from typing import Literal

from src.utils.config_models import FrozenModel

VOL_LOOKBACK_MULT = 5          # local volatility over 5k one-minute returns
VOLUME_LOOKBACK_SESSIONS = 20  # time-of-day volume norm: mean over the prior 20 sessions
VOLUME_MIN_SESSIONS = 10       # ... needing at least 10 of them with a bar at that minute
NEWS_ZONES = ((8 * 60 + 28, 8 * 60 + 45), (9 * 60 + 58, 10 * 60 + 15))   # every day, NY minutes
WED_ZONES = ((13 * 60 + 58, 15 * 60),)                                   # Wednesdays only
SIDES = ("both", "long_only")

V1_BURST_WINDOWS: tuple[int, ...] = (3, 5, 10)
V1_THRESHOLDS: tuple[float, ...] = (3.5, 4.0, 4.5, 5.0)
V1_VOL_GATES: tuple[str, ...] = ("none", "1.5", "2.0", "3.0")
V1_SIDES: tuple[str, ...] = ("both", "long_only")
V1_HOLDS: tuple[int, ...] = (5, 15, 30)
V1_NEWS_FILTERS: tuple[str, ...] = ("off", "on")


class _DriftBurstConfig(FrozenModel):
    symbol: str
    timeframe: Literal["1min"] = "1min"
    burst_window: Literal[3, 5, 10] = 5
    threshold: Literal[3.5, 4.0, 4.5, 5.0] = 4.5
    vol_gate: Literal["none", "1.5", "2.0", "3.0"] = "none"
    side: Literal["both", "long_only"] = "both"
    hold: Literal[5, 15, 30] = 5
    news_filter: Literal["off", "on"] = "off"

    @property
    def vol_gate_value(self) -> float | None:
        return None if self.vol_gate == "none" else float(self.vol_gate)


# --- drift_burst v1 (576 configs) --------------------------------------------------------------
# Specified 2026-11-20 from reports/Distinct futures strategy papers.md (pick 3), day session only
# at the user's request (no overnight). No drift-burst run has been made yet.

class DriftBurstV1Config(_DriftBurstConfig):
    pass


# --- drift_burst v2 (10,368 configs) -----------------------------------------------------------
# Specified by the user (2026-11-20) after v1 on ES (db_es_v1: 0 of 576 passed the profit gate; 1
# made money): "a 10k configuration" on ES with more parameters. New mechanics rather than finer
# steps on the v1 axes:
#   entry_mode : cross   -- decide at the bar where |T| first crosses the threshold (no wait)
#                peak    -- v1's rule: the bar after |T| peaks (stopped rising)
#                confirm -- two falling bars after the peak (|T_{r+1}| < |T_r| and |T_{r+2}| < |T_{r+1}|)
#   target     : none, 0.5, 1.0 -- exit when price retraces this fraction of the burst move
#                (|C_r - C_{r-k}|, r = the burst reference bar), filled at the better of the bar's
#                open and the target with market slippage
#   stop       : none, 1.0 -- stop this multiple of the burst move beyond the entry, filled at the
#                worse of the bar's open and the stop with stop slippage (checked before the target)
#   max_trades : 1, 3 trades per session
# news_filter is fixed off (v1: no difference).
V2_ENTRY_MODES: tuple[str, ...] = ("cross", "peak", "confirm")
V2_TARGETS: tuple[str, ...] = ("none", "0.5", "1.0")
V2_STOPS: tuple[str, ...] = ("none", "1.0")
V2_MAX_TRADES: tuple[int, ...] = (1, 3)
ENTRY_MODES = ("cross", "peak", "confirm")
ENTRY_LAG = {"cross": 0, "peak": 1, "confirm": 2}   # decision bar t = reference (burst) bar r + lag


class DriftBurstV2Config(_DriftBurstConfig):
    news_filter: Literal["off"] = "off"
    entry_mode: Literal["cross", "peak", "confirm"] = "peak"
    target: Literal["none", "0.5", "1.0"] = "none"
    stop: Literal["none", "1.0"] = "none"
    max_trades: Literal[1, 3] = 1

    @property
    def target_value(self) -> float | None:
        return None if self.target == "none" else float(self.target)

    @property
    def stop_value(self) -> float | None:
        return None if self.stop == "none" else float(self.stop)
