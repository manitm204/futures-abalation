"""Compact 1-minute backtester for ICT's Silver Bullet / 2022 Model (with placebo windows).

Bars: `sb_bars` keeps each CME session's Globex 1-minute bars from 18:00 ET the evening before up
to 16:00 ET (bars from 18:00 carry the next day's `session_date_ny`). Nothing is held across
sessions; a trade lives inside one window interval.

Features (all causal; computed once per data object and shared by every config):
  ATR[i]   14-bar simple mean of true range (prev close = the previous bar of the session; the
           session's first bar uses high - low); NaN for the first 13 bars of a session.
  swing high at i: high[i] > every high of the L bars before and >= every high of the L bars
           after, all in the session (L = 5); known from the close of bar i + L. Its first
           penetration is the first later bar with high > it (always after i + L).
  bearish sweep (of swing high P, first penetrated at k): the first close < P among bars
           k .. k+2 (same session); confirmed at that bar j; extreme = max high of k..j.
           Swing lows mirror it (bullish sweep).
  bullish FVG confirmed at bar m (bars m-2, m-1, m consecutive minutes, same session):
           high[m-2] < low[m]; gap = [high[m-2], low[m]]; size = low[m] - high[m-2];
           displacement = true range of m-1 (vs close[m-2]). Bearish mirrors it.

Per config and session (one trade at most):
  * candidate setups in time order: an FVG whose three bars open inside one window interval,
    with size > 0 and >= fvg_min x ATR[m-2], displacement >= disp x ATR[m-2], and (sweep=yes) a
    same-direction sweep confirmed at or before bar m-3 and within 60 minutes before bar m-2
    opens. Long for a bullish FVG, short for a bearish one.
  * order: a limit at the near edge (prox: low[m] for longs) or the midpoint (ce), live from bar
    m+1 for at most 30 bars and only on bars opening inside the interval. While it rests, later
    setups are ignored; if it expires unfilled, the next setup confirmed after it may arm.
  * stop (from the limit price): fvg = far edge -/+ 2 ticks; struct = swept extreme -/+ 2 ticks
    (the setup's sweep, else the extreme of the 10 bars ending at m-2); the distance is at least
    1.0 x ATR[m-2]; a struct reference on the wrong side of the limit skips the setup.
  * target: R x stop distance from the limit; liq = the nearest swing high of the session (long)
    beyond the limit, confirmed by bar m and not penetrated through bar m (none -> skip the
    setup); none = no target.
  * fill: the first live bar trading 1 tick through the limit; filled at the better of the limit
    and the bar's open (no slippage on a limit). Stop live from the fill bar (stop first), filled
    at the worse of the bar's open and the stop with stop slippage; the target only from the bar
    after the fill, a limit needing a 1-tick trade-through, filled at the target. Otherwise out
    at the CLOSE of the last bar opening inside the interval (market slippage).
  * whole contracts as equity covers at full contract value, compounding; a position still open
    at the data's last bar is closed there and flagged forced.
Audited by src/experiments/sb_integrity.py (independent plain-loop re-derivation).
"""

from __future__ import annotations

from dataclasses import dataclass, replace  # noqa: F401  (replace re-exported for perturbations)

import numpy as np
import polars as pl

from src.engine.events import EquityPoint, ExitReason, Fill, Trade
from src.strategies.compression_breakout.backtest import CBData
from src.strategies.mean_reversion.backtest import CostModel, scale_variable_costs  # noqa: F401  (re-export)
from src.strategies.silver_bullet.config import (
    ATR_LEN,
    EVENING_START_MIN,
    MAX_AGE_BARS,
    MIN_STOP_ATR,
    PAD_TICKS,
    SESSION_END_MIN,
    STRUCT_FALLBACK_BARS,
    SWEEP_LOOKBACK_MIN,
    SWEEP_RECLAIM_BARS,
    SWING_LEN,
    THROUGH_TICKS,
    WINDOWS,
    parse_target,
)
from src.utils.config_models import ExecutionConfig

TIME_EXIT, STOP_EXIT, TARGET_EXIT, FORCED = "time_exit", "stop_exit", "target_exit", "forced_close"


def sb_bars(df_full: pl.DataFrame, *, timeframe: str = "1min") -> pl.DataFrame:
    """Each session's Globex bars from 18:00 the evening before to 16:00 ET. Single symbol."""
    if timeframe != "1min":
        raise ValueError(f"silver_bullet runs on 1-minute bars only, got {timeframe!r}")
    if df_full.is_empty():
        return df_full
    ny = pl.col("bar_open_ts_ny")
    tod = ny.dt.hour().cast(pl.Int32) * 60 + ny.dt.minute().cast(pl.Int32)
    keep = (tod >= EVENING_START_MIN) | ((tod < SESSION_END_MIN) & (ny.dt.date() == pl.col("session_date_ny")))
    return df_full.filter(keep).sort("bar_open_ts")


@dataclass(frozen=True)
class SBParams:
    """Free-valued parameters (the config class restricts them to the grid); used off-grid by the
    perturbations and the stage-4 local moves (which also move the fixed swing length / order age)."""

    symbol: str
    timeframe: str
    window: str
    fvg_min: float
    disp: float
    entry: str              # prox / ce
    stop: str               # fvg / struct
    target_kind: str        # r / liq / none
    target_r: float | None
    sweep: bool
    swing: int = SWING_LEN
    max_age: int = MAX_AGE_BARS

    @classmethod
    def from_config(cls, cfg) -> "SBParams":
        tk, tr = parse_target(cfg.target)
        return cls(cfg.symbol, cfg.timeframe, cfg.window, float(cfg.fvg_min), float(cfg.disp), cfg.entry,
                   cfg.stop, tk, tr, cfg.sweep == "yes")


def as_params(cfg) -> SBParams:
    return cfg if isinstance(cfg, SBParams) else SBParams.from_config(cfg)


def validate_params(p: SBParams) -> None:
    if p.window not in WINDOWS:
        raise ValueError(f"Unknown window {p.window!r}")
    if p.entry not in ("prox", "ce") or p.stop not in ("fvg", "struct"):
        raise ValueError(f"Bad entry/stop {p.entry!r}/{p.stop!r}")
    if p.target_kind not in ("r", "liq", "none") or (p.target_kind == "r" and not (p.target_r or 0) > 0):
        raise ValueError(f"Bad target {p.target_kind!r} {p.target_r!r}")
    if p.fvg_min < 0 or p.disp < 0 or p.swing < 1 or p.max_age < 1:
        raise ValueError("fvg_min, disp >= 0; swing, max_age >= 1")


class SBData(CBData):
    """CBData (session structure, tod, caching) plus the shared Silver Bullet features."""

    def __init__(self, bars: pl.DataFrame) -> None:
        super().__init__(bars)
        self._tick: float | None = None  # set from the cost model by the simulator (stop padding, fills)
        self.minute = self.bar_open.astype("datetime64[m]").astype(np.int64) if self.n else np.array([], np.int64)
        h, lo, c = self.high, self.low, self.close
        if self.n:
            pc = np.concatenate([[np.nan], c[:-1]])
            first = np.arange(self.n) == self.sess_start
            pc[first] = np.nan
            tr = np.where(np.isnan(pc), h - lo, np.maximum(h - lo, np.maximum(np.abs(h - pc), np.abs(lo - pc))))
            cs = np.concatenate([[0.0], np.cumsum(tr)])
            idx = np.arange(self.n)
            atr = (cs[idx + 1] - cs[np.maximum(idx + 1 - ATR_LEN, 0)]) / ATR_LEN
            atr[idx - self.sess_start < ATR_LEN - 1] = np.nan
            self.tr, self.atr = tr, atr
            self._fvg_features()
        else:
            self.tr = self.atr = np.array([])

    def _fvg_features(self) -> None:
        n, h, lo, c = self.n, self.high, self.low, self.close
        m = np.arange(2, n)
        ok = (self.sess[m - 2] == self.sess[m]) & (self.minute[m] - self.minute[m - 2] == 2)
        a = m - 2
        pc = c[a]
        mid_tr = np.maximum(h[m - 1] - lo[m - 1], np.maximum(np.abs(h[m - 1] - pc), np.abs(lo[m - 1] - pc)))
        bull = ok & (h[a] < lo[m])
        bear = ok & (lo[a] > h[m])
        self.fvg_m = m[bull | bear]
        self.fvg_side = np.where(bull, 1, -1)[bull | bear]
        mm = self.fvg_m
        self.fvg_lo = np.where(self.fvg_side > 0, h[mm - 2], h[mm])     # gap bottom
        self.fvg_hi = np.where(self.fvg_side > 0, lo[mm], lo[mm - 2])   # gap top
        self.fvg_disp = mid_tr[bull | bear]
        self.fvg_atr = self.atr[mm - 2]

    # --- swings and sweeps (cached per swing length) ---------------------------------------
    def _next_beyond(self) -> tuple[np.ndarray, np.ndarray]:
        """Per bar: index of the first later bar in the session with a strictly higher high /
        strictly lower low (n = none). Monotonic stack per session."""
        def build():
            n = self.n
            nh = np.full(n, n, dtype=np.int64)
            nl = np.full(n, n, dtype=np.int64)
            h, lo, se = self.high.tolist(), self.low.tolist(), self.sess_end.tolist()
            sh: list[int] = []
            sl: list[int] = []
            for j in range(n):
                if j and se[j] != se[j - 1]:
                    sh, sl = [], []
                hj, lj = h[j], lo[j]
                while sh and h[sh[-1]] < hj:
                    nh[sh.pop()] = j
                sh.append(j)
                while sl and lo[sl[-1]] > lj:
                    nl[sl.pop()] = j
                sl.append(j)
            return nh, nl
        return self._get(("next_beyond",), build)

    def swings(self, L: int) -> dict[str, np.ndarray]:
        """Swing highs/lows of length L: index i, price, penetration bar k (n = never)."""
        def build():
            n, h, lo = self.n, self.high, self.low
            idx = np.arange(n)
            okw = (idx - L >= self.sess_start) & (idx + L <= self.sess_end)
            if n < 2 * L + 1:
                okw[:] = False
            from numpy.lib.stride_tricks import sliding_window_view as swv
            hp = np.concatenate([np.full(L, np.inf), h, np.full(L, np.inf)])
            lp = np.concatenate([np.full(L, -np.inf), lo, np.full(L, -np.inf)])
            win_h = swv(hp, 2 * L + 1)  # row i covers bars i-L .. i+L
            win_l = swv(lp, 2 * L + 1)
            left_h, right_h = win_h[:, :L].max(axis=1), win_h[:, L + 1:].max(axis=1)
            left_l, right_l = win_l[:, :L].min(axis=1), win_l[:, L + 1:].min(axis=1)
            is_h = okw & (h > left_h) & (h >= right_h)
            is_l = okw & (lo < left_l) & (lo <= right_l)
            nh, nl = self._next_beyond()
            hi_i, lo_i = np.flatnonzero(is_h), np.flatnonzero(is_l)
            return {"h_i": hi_i, "h_px": h[hi_i], "h_k": nh[hi_i], "l_i": lo_i, "l_px": lo[lo_i], "l_k": nl[lo_i]}
        return self._get(("swings", L), build)

    def sweeps(self, L: int) -> dict[str, np.ndarray]:
        """Confirmed sweeps per direction (+1 bullish = a swing low swept, -1 bearish), sorted by
        confirmation bar j: j, extreme."""
        def build():
            sw = self.swings(L)
            n, c, h, lo, se = self.n, self.close, self.high, self.low, self.sess_end
            out = {}
            for d, ii, px, kk in ((1, sw["l_i"], sw["l_px"], sw["l_k"]), (-1, sw["h_i"], sw["h_px"], sw["h_k"])):
                js, ex = [], []
                for k, P in zip(kk.tolist(), px.tolist()):
                    if k >= n:
                        continue
                    last = min(k + SWEEP_RECLAIM_BARS - 1, int(se[k]))
                    seg = c[k:last + 1]
                    back = np.flatnonzero(seg > P) if d > 0 else np.flatnonzero(seg < P)
                    if not len(back):
                        continue
                    j = k + int(back[0])
                    js.append(j)
                    ex.append(float(lo[k:j + 1].min()) if d > 0 else float(h[k:j + 1].max()))
                o = np.argsort(np.asarray(js, dtype=np.int64), kind="stable")
                out[d] = (np.asarray(js, dtype=np.int64)[o], np.asarray(ex, dtype=float)[o])
            return out
        return self._get(("sweeps", L), build)


def set_tick(data: SBData, exec_config: ExecutionConfig, symbol: str) -> None:
    data._tick = CostModel.for_symbol(exec_config, symbol).tick


def setups(data: SBData, p: SBParams) -> dict[str, np.ndarray]:
    """Every candidate setup (all filters passed) in time order: confirmation bar m, side, limit,
    stop, target (nan = none), the interval's last bar x, ATR, sweep extreme (nan = none)."""
    if data._tick is None:
        raise ValueError("SBData._tick is unset; call simulate_silver_bullet (or set_tick) first")

    def build():
        tick = data._tick
        L = p.swing
        m, sd = data.fvg_m, data.fvg_side
        tod, minute = data.tod, data.minute
        atr = data.fvg_atr
        ok = np.isfinite(atr) & (data.fvg_disp >= p.disp * atr)
        size = data.fvg_hi - data.fvg_lo
        ok &= (size > 0) & (size >= p.fvg_min * atr)
        ivs = WINDOWS[p.window]
        t0, t2 = tod[m - 2], tod[m]
        iv = np.full(len(m), -1)
        for q, (a, b) in enumerate(ivs):
            iv[(t0 >= a) & (t2 < b) & (t2 >= t0)] = q
        ok &= iv >= 0
        sel = np.flatnonzero(ok)
        sw = data.sweeps(L)
        swg = data.swings(L)
        rows = []
        for r in sel.tolist():
            mi, s = int(m[r]), int(sd[r])
            a_bar = mi - 2
            js, ex = sw[s]
            # most recent same-direction sweep confirmed by bar m-3, in this session, within 60 min
            pos = int(np.searchsorted(js, mi - 3, side="right")) - 1
            sweep_ext = np.nan
            if pos >= 0:
                j = int(js[pos])
                if data.sess[j] == data.sess[a_bar] and minute[a_bar] - minute[j] <= SWEEP_LOOKBACK_MIN:
                    sweep_ext = float(ex[pos])
            if p.sweep and not np.isfinite(sweep_ext):
                continue
            lo_g, hi_g = float(data.fvg_lo[r]), float(data.fvg_hi[r])
            if p.entry == "prox":
                lim = hi_g if s > 0 else lo_g
            else:
                lim = (lo_g + hi_g) / 2
            pad = PAD_TICKS * tick
            if p.stop == "fvg":
                ref = lo_g - pad if s > 0 else hi_g + pad
            else:
                if np.isfinite(sweep_ext):
                    e0 = sweep_ext
                else:
                    a0 = max(int(data.sess_start[a_bar]), a_bar - STRUCT_FALLBACK_BARS + 1)
                    e0 = float(data.low[a0:a_bar + 1].min()) if s > 0 else float(data.high[a0:a_bar + 1].max())
                ref = e0 - pad if s > 0 else e0 + pad
            raw = (lim - ref) * s
            if raw <= 0:
                continue
            dist = max(raw, MIN_STOP_ATR * float(atr[r]))
            stop = lim - s * dist
            if p.target_kind == "r":
                tgt = lim + s * p.target_r * dist
            elif p.target_kind == "liq":
                if s > 0:
                    ii, px, kk = swg["h_i"], swg["h_px"], swg["h_k"]
                else:
                    ii, px, kk = swg["l_i"], swg["l_px"], swg["l_k"]
                sess0 = int(data.sess_start[mi])
                lo_i = int(np.searchsorted(ii, sess0, side="left"))
                hi_i = int(np.searchsorted(ii, mi - L, side="right"))  # confirmed by bar m: i + L <= m
                cand = px[lo_i:hi_i][(kk[lo_i:hi_i] > mi) & ((px[lo_i:hi_i] - lim) * s > 0)]
                if not len(cand):
                    continue
                tgt = float(cand.min() if s > 0 else cand.max())
            else:
                tgt = np.nan
            a_iv, b_iv = ivs[iv[r]]
            # the last bar of the session opening inside the interval (tod rises after midnight)
            seg_end = min(int(data.sess_end[mi]), mi + (b_iv - a_iv) + 5)
            tt = tod[mi:seg_end + 1]
            inside = np.flatnonzero((tt >= a_iv) & (tt < b_iv))
            x = mi + int(inside[-1])
            rows.append((mi, s, lim, stop, tgt, x, float(atr[r]), sweep_ext))
        cols = list(zip(*rows)) if rows else [()] * 8
        return {"m": np.asarray(cols[0], dtype=np.int64), "side": np.asarray(cols[1], dtype=np.int64),
                "lim": np.asarray(cols[2], dtype=float), "stop": np.asarray(cols[3], dtype=float),
                "tgt": np.asarray(cols[4], dtype=float), "x": np.asarray(cols[5], dtype=np.int64),
                "atr": np.asarray(cols[6], dtype=float), "sweep_ext": np.asarray(cols[7], dtype=float)}
    key = ("setups", p.window, round(p.fvg_min, 9), round(p.disp, 9), p.entry, p.stop, p.target_kind,
           None if p.target_r is None else round(p.target_r, 9), p.sweep, p.swing)
    return data._get(key, build)


def planned_trades(data: SBData, p: SBParams) -> dict[str, np.ndarray]:
    """The trades the rules call for, before sizing: setup bar m, fill bar e, last bar x, side,
    limit, stop, target. One per session; a resting order blocks later setups until it expires."""
    validate_params(p)
    st = setups(data, p)
    lo, hi = data.low, data.high
    thru = THROUGH_TICKS * data._tick
    rows = []
    busy_until = -1
    done_sess = -1
    for r in range(len(st["m"])):
        mi = int(st["m"][r])
        s_id = int(data.sess[mi])
        if s_id == done_sess or mi <= busy_until:
            continue
        s, lim, x = int(st["side"][r]), float(st["lim"][r]), int(st["x"][r])
        last_live = min(mi + p.max_age, x)
        if last_live <= mi:
            continue
        seg = (lo[mi + 1:last_live + 1] <= lim - thru) if s > 0 else (hi[mi + 1:last_live + 1] >= lim + thru)
        f = np.flatnonzero(seg)
        if not len(f):
            busy_until = last_live
            continue
        e = mi + 1 + int(f[0])
        rows.append((mi, e, x, s, lim, float(st["stop"][r]), float(st["tgt"][r]), float(st["atr"][r])))
        done_sess = s_id
    cols = list(zip(*rows)) if rows else [()] * 8
    i64, f = (lambda a: np.asarray(a, dtype=np.int64)), (lambda a: np.asarray(a, dtype=float))
    return {"m": i64(cols[0]), "e": i64(cols[1]), "x": i64(cols[2]), "side": i64(cols[3]), "lim": f(cols[4]),
            "stop": f(cols[5]), "tgt": f(cols[6]), "atr": f(cols[7])}


@dataclass
class SimResult:
    """Trades plus the bar indices needed for mark-to-market and integrity checks."""

    trades: list[Trade]
    equity_curve: list[EquityPoint]
    signal_idx: np.ndarray    # setup (FVG confirmation) bar
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
    entry_base: np.ndarray    # the limit price
    side: np.ndarray          # +1 long / -1 short
    stop_level: np.ndarray
    target_level: np.ndarray  # nan = no target


def simulate_silver_bullet(
    data: SBData,
    cfg,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
    side_override: np.ndarray | None = None,
) -> SimResult:
    """Execution-stress knobs (default off): `entry_delay_bars` -- the limit must be traded
    through again that many bars later (fill on the first qualifying bar >= fill + delay, still
    inside the interval, else skipped); `missed_entry_frac` drops that fraction of the trades.
    `side_override` is accepted for interface parity and must be None (a limit's side is fixed)."""
    if side_override is not None:
        raise ValueError("silver_bullet trades limit orders; side_override is not supported")
    p = as_params(cfg)
    costs = CostModel.for_symbol(exec_config, p.symbol)
    data._tick = costs.tick
    plan = planned_trades(data, p)
    o, hi, lo, c, ts, n = data.open, data.high, data.low, data.close, data.ts, data.n
    tick = costs.tick
    thru = THROUGH_TICKS * tick
    rng = np.random.default_rng(stress_seed) if missed_entry_frac > 0 else None

    trades: list[Trade] = []
    equity_curve: list[EquityPoint] = []
    rows: list[tuple] = []
    equity = starting_equity
    seq = 0
    for mi, e0, x, sd, lim, stop, tgt in zip(plan["m"].tolist(), plan["e"].tolist(), plan["x"].tolist(),
                                            plan["side"].tolist(), plan["lim"].tolist(), plan["stop"].tolist(),
                                            plan["tgt"].tolist()):
        if rng is not None and rng.random() < missed_entry_frac:
            continue
        e = e0
        if entry_delay_bars:
            cand = np.arange(e0 + entry_delay_bars, min(x, mi + p.max_age) + 1)
            okb = (lo[cand] <= lim - thru) if sd > 0 else (hi[cand] >= lim + thru)
            if not okb.any():
                continue
            e = int(cand[np.flatnonzero(okb)[0]])
        long = sd > 0
        fill_px = min(o[e], lim) if long else max(o[e], lim)
        qty = costs.size(equity, fill_px, fill_px - data.price_adj[e])
        if qty <= 0:
            continue
        seq += 1
        side_s = "long" if long else "short"
        entry_fill = Fill(order_id=f"e{seq}", symbol=p.symbol, side=side_s, quantity=qty, fill_price=fill_px,
                          fill_ts=ts[e], commission=costs.commission(qty), slippage_points=0.0, bar_open_ts=ts[e])
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
        dist = abs(lim - stop)
        trades.append(Trade(
            trade_id=f"t{seq}", config_id="", symbol=p.symbol, side=side_s, entry_order_id=entry_fill.order_id,
            entry_fill=entry_fill, quantity=qty, stop_price=stop,
            target_price=tgt if np.isfinite(tgt) else None,
            exit_fill=exit_fill, exit_reason=reason, realized_pnl=realized,
            realized_r=realized / (dist * qty) if dist > 0 else None,
            commission_total=commissions, holding_bars=j - e,
        ))
        rows.append((mi, e, j, mi, qty, fill_px, exit_px, entry_fill.commission, realized, forced, why, lim, sd,
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
        stop_level=f(cols[13]), target_level=f(cols[14]),
    )
