"""Compact 1-minute backtester for the FVG-after-displacement trade, with and against the gap.

Bars: `fv_bars` (= the Silver Bullet `sb_bars`) keeps each session's Globex bars from 18:00 ET the
evening before to 16:00 ET, so ATR is warm at 09:45. Setups and entries are inside the window
(09:45-12:00, 12:00-15:30 or 09:45-15:30 ET); a position is closed after `hold` minutes or at
16:00. Nothing is held across sessions. See src/strategies/fvg/config.py for the rules.

Shared features (FVData, computed once): ATR (14-bar mean true range, from the SBData parent), the
three-bar gaps (bullish high[m-2] < low[m], bearish low[m-2] > high[m]; consecutive minutes, one
session), the middle bar's true range, and the session VWAP from 09:30.

Per config and session (one trade at most; while an order rests later setups are ignored; after an
unfilled expiry the next setup confirmed after it may arm):
  gap side g (+1 bullish); trade side sd = g (with) or -g (against)
  level  = near edge (bullish: low[m]) or midpoint; mkt = open of bar m+1 (within 2 minutes)
  with   : limit, live bars m+1 .. m+wait inside the window, fills when a bar trades 1 tick
           through the level, at the better of the level and the bar's open, no slippage
  against: stop order at the level, fills when a bar touches it, at the worse of the level and
           the bar's open, with stop slippage
  stop   : from the reference (the level, or bar m+1's open for mkt): struct = 2 ticks beyond the
           extreme of bars m-2..m on the stop side (wrong side -> skip); aK = K x ATR; >= 1 ATR
  target : R x stop distance from the reference; limit with a 1-tick trade-through from the bar
           after the fill; stop first on a bar touching both
  exit   : otherwise at the close of the last bar opening within `hold` minutes of the fill bar's
           open, and before 16:00 (market slippage)
Audited by src/experiments/fv_integrity.py (independent plain-loop re-derivation).
"""

from __future__ import annotations

from dataclasses import dataclass, replace  # noqa: F401  (replace re-exported for perturbations)

import numpy as np
import polars as pl

from src.engine.events import EquityPoint, ExitReason, Fill, Trade
from src.strategies.fvg.config import (
    MIN_STOP_ATR,
    PAD_TICKS,
    RTH_START_MIN,
    SESSION_END_MIN,
    THROUGH_TICKS,
    WINDOWS,
    parse_stop,
    parse_target,
)
from src.strategies.mean_reversion.backtest import CostModel, scale_variable_costs  # noqa: F401  (re-export)
from src.strategies.silver_bullet.backtest import SBData, sb_bars
from src.utils.config_models import ExecutionConfig

TIME_EXIT, STOP_EXIT, TARGET_EXIT, FORCED = "time_exit", "stop_exit", "target_exit", "forced_close"
MAX_ENTRY_GAP_MIN = 2  # a mkt entry bar must open within 2 minutes of bar 3


def fv_bars(df_full: pl.DataFrame, *, timeframe: str = "1min") -> pl.DataFrame:
    return sb_bars(df_full, timeframe=timeframe)


@dataclass(frozen=True)
class FVParams:
    """Free-valued parameters (the config class restricts them to the grid); used off-grid by the
    perturbations and stage-4 local moves."""

    symbol: str
    timeframe: str
    window: str
    mode: str               # with / against
    disp: float
    fvg_min: float
    vwap: bool
    entry: str              # prox / ce / mkt
    wait: int               # bars (0 for mkt)
    stop_kind: str          # struct / atr
    stop_mult: float | None
    target_r: float | None  # None = no target
    hold: int               # minutes

    @classmethod
    def from_config(cls, cfg) -> "FVParams":
        sk, sm = parse_stop(cfg.stop)
        return cls(cfg.symbol, cfg.timeframe, cfg.window, cfg.mode, float(cfg.disp), float(cfg.fvg_min),
                   cfg.vwap == "on", cfg.entry, int(cfg.wait), sk, sm, parse_target(cfg.target), int(cfg.hold))


def as_params(cfg) -> FVParams:
    return cfg if isinstance(cfg, FVParams) else FVParams.from_config(cfg)


def validate_params(p: FVParams) -> None:
    if p.window not in WINDOWS or p.mode not in ("with", "against") or p.entry not in ("prox", "ce", "mkt"):
        raise ValueError(f"Bad window/mode/entry {p.window!r}/{p.mode!r}/{p.entry!r}")
    if p.entry != "mkt" and p.wait < 1:
        raise ValueError("a resting order needs wait >= 1")
    if p.stop_kind not in ("struct", "atr") or (p.stop_kind == "atr" and not (p.stop_mult or 0) > 0):
        raise ValueError(f"Bad stop {p.stop_kind!r} {p.stop_mult!r}")
    if p.target_r is not None and not p.target_r > 0:
        raise ValueError("target_r must be > 0")
    if p.hold < 1 or p.disp < 0 or p.fvg_min < 0:
        raise ValueError("hold >= 1, disp and fvg_min >= 0")


class FVData(SBData):
    """SBData (sessions, ATR, the gap arrays) plus the session VWAP from 09:30."""

    def __init__(self, bars: pl.DataFrame) -> None:
        super().__init__(bars)
        if self.n:
            vol = (self._df["volume"].to_numpy().astype(float) if "volume" in self._df.columns
                   else np.ones(self.n))
            rth = (self.tod >= RTH_START_MIN) & (self.tod < SESSION_END_MIN)
            tp = (self.high + self.low + self.close) / 3.0
            pv = np.where(rth, tp * vol, 0.0)
            vv = np.where(rth, vol, 0.0)
            cpv, cvv = np.cumsum(pv), np.cumsum(vv)
            base = self.sess_start
            off_pv = np.where(base > 0, cpv[np.maximum(base - 1, 0)], 0.0)
            off_vv = np.where(base > 0, cvv[np.maximum(base - 1, 0)], 0.0)
            spv, svv = cpv - off_pv, cvv - off_vv
            with np.errstate(invalid="ignore", divide="ignore"):
                self.vwap = np.where(rth & (svv > 0), spv / svv, np.nan)
        else:
            self.vwap = np.array([])


def setups(data: FVData, p: FVParams) -> dict[str, np.ndarray]:
    """Gaps passing the window / size / displacement / VWAP filters, in time order: bar m, gap side,
    trade side, level (nan for mkt), struct stop reference, ATR, the window's last bar index."""
    def build():
        m, g = data.fvg_m, data.fvg_side
        atr = data.fvg_atr
        a, b = WINDOWS[p.window]
        t0, t2 = data.tod[m - 2], data.tod[m]
        size = data.fvg_hi - data.fvg_lo
        ok = (np.isfinite(atr) & (t0 >= a) & (t2 < b) & (t2 >= t0) & (data.fvg_disp >= p.disp * atr)
              & (size > 0) & (size >= p.fvg_min * atr))
        sd = g if p.mode == "with" else -g
        if p.vwap:
            vw = data.vwap[m]
            ok &= np.isfinite(vw) & ((data.close[m] - vw) * sd > 0)
        sel = np.flatnonzero(ok)
        mm, gg, ss = m[sel], g[sel], sd[sel]
        lo3 = np.minimum.reduce([data.low[mm - 2], data.low[mm - 1], data.low[mm]])
        hi3 = np.maximum.reduce([data.high[mm - 2], data.high[mm - 1], data.high[mm]])
        if p.entry == "prox":
            lvl = np.where(gg > 0, data.fvg_hi[sel], data.fvg_lo[sel])
        elif p.entry == "ce":
            lvl = (data.fvg_hi[sel] + data.fvg_lo[sel]) / 2
        else:
            lvl = np.full(len(sel), np.nan)
        # the window's last bar for each setup (bars inside the window are contiguous after 09:45)
        wl = np.empty(len(sel), dtype=np.int64)
        for k, mi in enumerate(mm.tolist()):
            end = min(int(data.sess_end[mi]), mi + (b - a) + 5)
            inside = np.flatnonzero(data.tod[mi:end + 1] < b)
            wl[k] = mi + int(inside[-1])
        return {"m": mm, "g": gg, "side": ss, "lvl": lvl, "lo3": lo3, "hi3": hi3, "atr": atr[sel], "wlast": wl}
    key = ("fv_setups", p.window, p.mode, round(p.disp, 9), round(p.fvg_min, 9), p.vwap, p.entry)
    return data._get(key, build)


def stop_and_target(p: FVParams, base: float, sd: int, lo3: float, hi3: float, atr: float, tick: float):
    """(stop, target) from the entry reference; None when a struct stop is on the wrong side."""
    if p.stop_kind == "struct":
        ref = lo3 - PAD_TICKS * tick if sd > 0 else hi3 + PAD_TICKS * tick
        raw = (base - ref) * sd
        if raw <= 0:
            return None
    else:
        raw = p.stop_mult * atr
    dist = max(raw, MIN_STOP_ATR * atr)
    stop = base - sd * dist
    tgt = base + sd * p.target_r * dist if p.target_r is not None else np.nan
    return stop, tgt


def exit_bar(data: FVData, e: int, hold: int) -> int:
    """The last bar of the session opening within `hold` minutes of bar e's open and before 16:00."""
    end = min(int(data.sess_end[e]), e + hold + 5)
    seg = np.arange(e, end + 1)
    ok = (data.minute[seg] - data.minute[e] < hold) & (data.tod[seg] < SESSION_END_MIN)
    return int(seg[np.flatnonzero(ok)[-1]])


def planned_trades(data: FVData, p: FVParams, tick: float, *, entry_delay_bars: int = 0) -> dict[str, np.ndarray]:
    """Trades before sizing: setup bar m, fill bar e, exit bar x, side, reference price, fill kind
    (0 limit, 1 stop order, 2 market), stop, target."""
    validate_params(p)
    st = setups(data, p)
    o, lo, hi = data.open, data.low, data.high
    thru = THROUGH_TICKS * tick
    rows = []
    busy_until = -1
    done_sess = -1
    for r in range(len(st["m"])):
        mi = int(st["m"][r])
        s_id = int(data.sess[mi])
        if s_id == done_sess or mi <= busy_until:
            continue
        g, sd, wl = int(st["g"][r]), int(st["side"][r]), int(st["wlast"][r])
        if p.entry == "mkt":
            e = mi + 1 + entry_delay_bars
            if (e > wl or data.sess[e] != s_id
                    or data.minute[mi + 1] - data.minute[mi] > MAX_ENTRY_GAP_MIN):
                continue
            base, kind = float(o[e]), 2
        else:
            lvl = float(st["lvl"][r])
            last_live = min(mi + p.wait, wl)
            if last_live <= mi:
                continue
            seg = slice(mi + 1, last_live + 1)
            if p.mode == "with":  # limit: 1-tick trade-through, toward the gap
                hit = (lo[seg] <= lvl - thru) if g > 0 else (hi[seg] >= lvl + thru)
                kind = 0
            else:                 # stop order at the level: a touch
                hit = (lo[seg] <= lvl) if g > 0 else (hi[seg] >= lvl)
                kind = 1
            f = np.flatnonzero(hit)
            if entry_delay_bars:
                f = f[f >= int(f[0]) + entry_delay_bars] if len(f) else f
            if not len(f):
                busy_until = last_live
                continue
            e = mi + 1 + int(f[0])
            base = lvl
        sl = stop_and_target(p, base, sd, float(st["lo3"][r]), float(st["hi3"][r]), float(st["atr"][r]), tick)
        if sl is None:
            continue
        x = exit_bar(data, e, p.hold)
        rows.append((mi, e, x, sd, base, kind, sl[0], sl[1]))
        done_sess = s_id
    cols = list(zip(*rows)) if rows else [()] * 8
    i64, f64 = (lambda v: np.asarray(v, dtype=np.int64)), (lambda v: np.asarray(v, dtype=float))
    return {"m": i64(cols[0]), "e": i64(cols[1]), "x": i64(cols[2]), "side": i64(cols[3]), "base": f64(cols[4]),
            "kind": i64(cols[5]), "stop": f64(cols[6]), "tgt": f64(cols[7])}


@dataclass
class SimResult:
    trades: list[Trade]
    equity_curve: list[EquityPoint]
    signal_idx: np.ndarray    # setup (bar 3) index
    entry_idx: np.ndarray
    exit_idx: np.ndarray
    decision_idx: np.ndarray
    quantity: np.ndarray
    entry_px: np.ndarray
    exit_px: np.ndarray
    entry_commission: np.ndarray
    realized_pnl: np.ndarray
    forced_close: np.ndarray
    exit_reason: np.ndarray
    entry_base: np.ndarray    # the order's level (limit / stop) or the market bar's open
    side: np.ndarray
    stop_level: np.ndarray
    target_level: np.ndarray


def simulate_fvg(
    data: FVData,
    cfg,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
    side_override: np.ndarray | None = None,
    plan: dict[str, np.ndarray] | None = None,
) -> SimResult:
    """Stress knobs (default off): `entry_delay_bars` -- a resting order needs a qualifying bar that
    many bars after its first one (mkt: that many bars later); `missed_entry_frac` drops trades.
    `side_override` is not supported (an order's side is fixed by its level). `plan` replaces the
    planned trades (the random-entry benchmark; same shape as planned_trades returns)."""
    if side_override is not None:
        raise ValueError("fvg trades resting orders; side_override is not supported")
    p = as_params(cfg)
    costs = CostModel.for_symbol(exec_config, p.symbol)
    tick = costs.tick
    if plan is None:
        plan = planned_trades(data, p, tick, entry_delay_bars=entry_delay_bars)
    o, hi, lo, c, ts, n = data.open, data.high, data.low, data.close, data.ts, data.n
    thru = THROUGH_TICKS * tick
    rng = np.random.default_rng(stress_seed) if missed_entry_frac > 0 else None
    trades, equity_curve, rows = [], [], []
    equity = starting_equity
    seq = 0
    for mi, e, x, sd, base, kind, stop, tgt in zip(*(plan[k].tolist() for k in
                                                     ("m", "e", "x", "side", "base", "kind", "stop", "tgt"))):
        if rng is not None and rng.random() < missed_entry_frac:
            continue
        long = sd > 0
        act = "buy" if long else "sell"
        if kind == 0:
            fill_px = min(o[e], base) if long else max(o[e], base)
        elif kind == 1:
            fill_px = costs.fill(max(o[e], base) if long else min(o[e], base), act, stop=True)
        else:
            fill_px = costs.fill(o[e], act)
        qty = costs.size(equity, fill_px, fill_px - data.price_adj[e])
        if qty <= 0:
            continue
        seq += 1
        side_s = "long" if long else "short"
        entry_fill = Fill(order_id=f"e{seq}", symbol=p.symbol, side=side_s, quantity=qty, fill_price=fill_px,
                          fill_ts=ts[e], commission=costs.commission(qty), slippage_points=abs(fill_px - base),
                          bar_open_ts=ts[e])
        sh = np.flatnonzero(lo[e:x + 1] <= stop) if long else np.flatnonzero(hi[e:x + 1] >= stop)
        js = e + int(sh[0]) if len(sh) else x + 1
        jt = x + 1
        if np.isfinite(tgt) and e + 1 <= x:
            th = (np.flatnonzero(hi[e + 1:x + 1] >= tgt + thru) if long
                  else np.flatnonzero(lo[e + 1:x + 1] <= tgt - thru))
            jt = e + 1 + int(th[0]) if len(th) else x + 1
        if js <= x and js <= jt:
            j, why = js, STOP_EXIT
            exit_px = costs.fill(min(o[j], stop) if long else max(o[j], stop), "sell" if long else "buy", stop=True)
        elif jt <= x:
            j, why = jt, TARGET_EXIT
            exit_px = tgt
        else:
            j = x
            why = FORCED if x == n - 1 else TIME_EXIT
            exit_px = costs.fill(c[x], "sell" if long else "buy")
        forced = why == FORCED
        exit_fill = Fill(order_id=f"x{seq}", symbol=p.symbol, side=side_s, quantity=qty, fill_price=exit_px,
                         fill_ts=ts[j], commission=costs.commission(qty), slippage_points=0.0, bar_open_ts=ts[j])
        commissions = entry_fill.commission + exit_fill.commission
        realized = sd * (exit_px - fill_px) * qty - commissions
        reason = {FORCED: ExitReason.SESSION_EXIT, TIME_EXIT: ExitReason.TIME_EXIT,
                  STOP_EXIT: ExitReason.STOP_LOSS, TARGET_EXIT: ExitReason.TAKE_PROFIT}[why]
        dist = abs(base - stop)
        trades.append(Trade(
            trade_id=f"t{seq}", config_id="", symbol=p.symbol, side=side_s, entry_order_id=entry_fill.order_id,
            entry_fill=entry_fill, quantity=qty, stop_price=stop, target_price=tgt if np.isfinite(tgt) else None,
            exit_fill=exit_fill, exit_reason=reason, realized_pnl=realized,
            realized_r=realized / (dist * qty) if dist > 0 else None,
            commission_total=commissions, holding_bars=j - e))
        rows.append((mi, e, j, mi, qty, fill_px, exit_px, entry_fill.commission, realized, forced, why, base, sd,
                     stop, tgt))
        equity += realized
        equity_curve.append(EquityPoint(ts=ts[j], cash=equity, position_value=0.0, equity=equity))
        if forced:
            break
    cols = list(zip(*rows)) if rows else [()] * 15
    f, i64 = (lambda a: np.asarray(a, dtype=float)), (lambda a: np.asarray(a, dtype=np.int64))
    return SimResult(
        trades=trades, equity_curve=equity_curve,
        signal_idx=i64(cols[0]), entry_idx=i64(cols[1]), exit_idx=i64(cols[2]), decision_idx=i64(cols[3]),
        quantity=f(cols[4]), entry_px=f(cols[5]), exit_px=f(cols[6]), entry_commission=f(cols[7]),
        realized_pnl=f(cols[8]), forced_close=np.asarray(cols[9], dtype=bool),
        exit_reason=np.asarray(cols[10], dtype=object), entry_base=f(cols[11]), side=i64(cols[12]),
        stop_level=f(cols[13]), target_level=f(cols[14]))
