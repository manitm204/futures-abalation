"""Compact 1-minute backtester for the NY-open liquidity sweep (fade vs continuation).

Bars: `os_day_bars` takes the full 24-hour Globex 1-minute bars, computes the pre-open ranges of
each session (overnight, Asia, London, the 08:00-09:30 box) from bars that open BEFORE 09:30,
and returns only the 09:30-16:00 ET bars with those ranges attached as per-session columns.
Nothing is traded or held outside 09:30-16:00; each NY date is one session.

Per session s (all inputs known at or before the trigger bar's close):
    [L, H]   = the level's range (pre-open columns, or the prior RTH session's low/high for `pdr`)
    open09   = open of the session's first bar (if it opens by 09:32)
    dATR     = mean RTH high-low range of the previous 14 sessions
    window   = bars opening in [09:30, 09:30 + window)
    high side (needs open09 <= H): p = first window bar with high > H + pen x dATR
        fade: t = first bar in p .. p+confirm-1 (and in the window) closing < H  -> short
        cont: closes of p .. p+confirm-1 (all in the window) all > H, t = p+confirm-1 -> long
    low side mirrors it (open09 >= L; low < L - pen x dATR; fade closes > L -> long, cont < L -> short)
    side = both: the side whose trigger bar comes first (a same-bar tie trades nothing)

Execution (audited by src/experiments/os_integrity.py):
  * entry at the OPEN of bar t+1 (same session, opening within 2 minutes of t) with market
    slippage; `signal_idx` = t;
  * stop distance: struct = from the entry open to the extreme of bars p..t (+2 ticks beyond),
    or k x dATR; never below 0.03 x dATR. Live intrabar from the entry bar, filled at the worse of
    the bar's open and the stop with stop slippage;
  * target (optional) = entry open +/- R x stop distance, or the range target; a limit that fills
    at the target only when a bar trades 1 tick through it; a bar touching stop and target is a
    stop (stop_first). A target on the wrong side of the entry skips the trade;
  * time exit at the CLOSE of the last bar opening before the exit time; 16:00 = the session's
    last bar (`eod_exit`);
  * one trade per session, compounding equity, unlevered whole contracts;
  * a position closed on the data's final bar is flagged forced and is not a completed trade.
`side_override` (luck benchmark) replaces the direction of each planned trade; `level_override`
(placebo benchmark) replaces the [L, H] range of the config's level.
"""

from __future__ import annotations

from dataclasses import dataclass, replace  # noqa: F401  (replace re-exported for perturbations)

import numpy as np
import pandas as pd
import polars as pl

from src.engine.events import EquityPoint, ExitReason, Fill, Trade
from src.strategies.compression_breakout.backtest import CBData
from src.strategies.mean_reversion.backtest import CostModel, scale_variable_costs  # noqa: F401  (re-export)
from src.strategies.open_sweep.config import (
    DATR_LOOKBACK,
    DAY_END_MIN,
    DAY_START_MIN,
    EVENING_START_MIN,
    LEVEL_MIN_COVERAGE,
    LEVEL_WINDOWS,
    LEVELS,
    MAX_ENTRY_GAP_MIN,
    MAX_OPEN_LAG_MIN,
    MIN_STOP_DATR,
    PRE_OPEN_LEVELS,
    STRUCT_PAD_TICKS,
    TARGET_THROUGH_TICKS,
    hhmm_minutes,
    level_minutes,
    parse_stop,
    parse_target,
)
from src.utils.config_models import ExecutionConfig

TIME_EXIT, EOD_EXIT, STOP_EXIT, TARGET_EXIT, FORCED = "time_exit", "eod_exit", "stop_exit", "target_exit", "forced_close"


def _tod_expr():
    ny = pl.col("bar_open_ts_ny")
    return ny.dt.hour().cast(pl.Int32) * 60 + ny.dt.minute().cast(pl.Int32)


def level_mask(level: str, tod: pl.Expr) -> pl.Expr:
    """Bars (of the level's own session date) that form a pre-open level."""
    if level == "onh":
        return (tod >= EVENING_START_MIN) | (tod < DAY_START_MIN)
    a, b = LEVEL_WINDOWS[level]
    return (tod >= a) & (tod < b)


def pre_open_levels(df_full: pl.DataFrame) -> pl.DataFrame:
    """Per session date: <level>_h / <level>_l for every pre-open level (null when its window has
    fewer than LEVEL_MIN_COVERAGE of its minutes)."""
    tod = _tod_expr()
    aggs = []
    for lv in PRE_OPEN_LEVELS:
        m = level_mask(lv, tod)
        need = int(np.ceil(LEVEL_MIN_COVERAGE * level_minutes(lv)))
        ok = m.sum() >= need
        aggs += [pl.when(ok).then(pl.col("high").filter(m).max()).otherwise(None).alias(f"{lv}_h"),
                 pl.when(ok).then(pl.col("low").filter(m).min()).otherwise(None).alias(f"{lv}_l")]
    return df_full.group_by("session_date_ny").agg(aggs).sort("session_date_ny")


def os_day_bars(df_full: pl.DataFrame, *, timeframe: str = "1min") -> pl.DataFrame:
    """The strategy's bars: 09:30-16:00 ET 1-minute bars on their own session date, with the
    session's pre-open levels attached as columns. Single symbol, full Globex bars in."""
    if timeframe != "1min":
        raise ValueError(f"open_sweep runs on 1-minute bars only, got {timeframe!r}")
    if df_full.is_empty():
        return df_full
    df_full = df_full.sort("bar_open_ts")
    tod = _tod_expr()
    ny = pl.col("bar_open_ts_ny")
    rth = df_full.filter((tod >= DAY_START_MIN) & (tod < DAY_END_MIN) & (ny.dt.date() == pl.col("session_date_ny")))
    lv = pre_open_levels(df_full)
    return rth.join(lv, on="session_date_ny", how="left").sort("bar_open_ts")


class OSData(CBData):
    """CBData (session structure, tod, caching) plus per-session levels, dATR and triggers."""

    def __init__(self, bars: pl.DataFrame) -> None:
        super().__init__(bars)
        S = len(self.days)
        self._key = self.sess * 1440 + self.tod
        st, en = self.day_start_idx, self.day_end_idx
        self.level_override: dict[str, tuple[np.ndarray, np.ndarray]] = {}
        if S:
            self.open09 = np.where(self.tod[st] - DAY_START_MIN <= MAX_OPEN_LAG_MIN, self.open[st], np.nan)
            self.sess_high = np.maximum.reduceat(self.high, st)
            self.sess_low = np.minimum.reduceat(self.low, st)
        else:
            self.open09 = self.sess_high = self.sess_low = np.array([])
        rng = self.sess_high - self.sess_low
        self.datr = pd.Series(rng).shift(1).rolling(DATR_LOOKBACK, min_periods=DATR_LOOKBACK).mean().to_numpy()
        self._levels: dict[str, tuple[np.ndarray, np.ndarray]] = {}
        for lvname in PRE_OPEN_LEVELS:
            for c in (f"{lvname}_h", f"{lvname}_l"):
                if c not in self._df.columns:
                    raise ValueError(f"bars lack the {c!r} column; build them with os_day_bars")
            h = self._df[f"{lvname}_h"].fill_null(np.nan).to_numpy().astype(float)
            lo = self._df[f"{lvname}_l"].fill_null(np.nan).to_numpy().astype(float)
            self._levels[lvname] = (h[st], lo[st]) if S else (np.array([]), np.array([]))
        self._levels["pdr"] = (np.concatenate([[np.nan], self.sess_high[:-1]]) if S else np.array([]),
                               np.concatenate([[np.nan], self.sess_low[:-1]]) if S else np.array([]))

    def levels(self, name: str) -> tuple[np.ndarray, np.ndarray]:
        """(H, L) per session for a level (a placebo override wins)."""
        if name not in LEVELS:
            raise ValueError(f"Unknown level {name!r}")
        return self.level_override.get(name, self._levels[name])

    def bar_before(self, minutes: int) -> np.ndarray:
        """Per session: index of the last bar opening before `minutes` (day_start - 1 if none)."""
        s = np.arange(len(self.days), dtype=np.int64)
        return np.searchsorted(self._key, s * 1440 + int(minutes), side="left") - 1


@dataclass(frozen=True)
class OSParams:
    """Free-valued strategy parameters (the config class restricts them to the grid lattice);
    used for off-grid perturbations too."""

    symbol: str
    timeframe: str
    level: str
    side: str               # both / high / low
    window: int             # minutes after 09:30
    pen: float              # x dATR
    confirm: int            # bars
    mode: str               # fade / cont
    stop_kind: str          # struct / datr
    stop_mult: float | None  # x dATR (datr stops)
    target_kind: str        # none / r / range
    target_r: float | None
    exit_min: int           # NY minutes; 16:00 = the session's last bar

    @classmethod
    def from_config(cls, cfg) -> "OSParams":
        sk, sm = parse_stop(cfg.stop)
        tk, tr = parse_target(cfg.target)
        return cls(cfg.symbol, cfg.timeframe, cfg.level, cfg.side, int(cfg.window), float(cfg.pen),
                   int(cfg.confirm), cfg.mode, sk, sm, tk, tr, hhmm_minutes(cfg.exit))


def as_params(cfg) -> OSParams:
    return cfg if isinstance(cfg, OSParams) else OSParams.from_config(cfg)


def validate_params(p: OSParams) -> None:
    if p.side not in ("both", "high", "low") or p.mode not in ("fade", "cont"):
        raise ValueError(f"Bad side/mode {p.side!r}/{p.mode!r}")
    if p.window < 1 or p.confirm < 1 or p.pen < 0:
        raise ValueError("window and confirm must be >= 1 and pen >= 0")
    if p.stop_kind not in ("struct", "datr") or (p.stop_kind == "datr" and not (p.stop_mult or 0) > 0):
        raise ValueError(f"Bad stop {p.stop_kind!r} {p.stop_mult!r}")
    if p.target_kind not in ("none", "r", "range") or (p.target_kind == "r" and not (p.target_r or 0) > 0):
        raise ValueError(f"Bad target {p.target_kind!r} {p.target_r!r}")
    if not DAY_START_MIN + p.window < p.exit_min <= DAY_END_MIN:
        raise ValueError(f"exit {p.exit_min} must be after the window end and by 16:00")


def _side_trigger(hi, lo, cl, lvl: float, pen_pts: float, k: int, mode: str, upper: bool):
    """One side of one session's window (relative bar arrays). Returns (t, side, extreme) or None."""
    pens = np.flatnonzero(hi > lvl + pen_pts) if upper else np.flatnonzero(lo < lvl - pen_pts)
    if not len(pens):
        return None
    p = int(pens[0])
    n = len(cl)
    if mode == "fade":
        last = min(p + k - 1, n - 1)
        back = cl[p:last + 1] < lvl if upper else cl[p:last + 1] > lvl
        idx = np.flatnonzero(back)
        if not len(idx):
            return None
        t = p + int(idx[0])
        return (t, -1, float(hi[p:t + 1].max())) if upper else (t, 1, float(lo[p:t + 1].min()))
    t = p + k - 1
    if t > n - 1:
        return None
    beyond = cl[p:t + 1] > lvl if upper else cl[p:t + 1] < lvl
    if not beyond.all():
        return None
    return (t, 1, float(lo[p:t + 1].min())) if upper else (t, -1, float(hi[p:t + 1].max()))


def session_triggers(data: OSData, p: OSParams) -> dict[str, np.ndarray]:
    """Per session: trigger bar t (-1 = none), side, structural extreme, and the range [L, H]."""
    def build():
        S = len(data.days)
        H, L = data.levels(p.level)
        t_out = np.full(S, -1, dtype=np.int64)
        sd_out = np.zeros(S, dtype=np.int64)
        ext_out = np.full(S, np.nan)
        wend = data.bar_before(DAY_START_MIN + p.window)
        hi, lo, cl = data.high, data.low, data.close
        for s in range(S):
            a = int(data.day_start_idx[s])
            w = int(wend[s])
            o9, da = data.open09[s], data.datr[s]
            if w < a or not (np.isfinite(o9) and np.isfinite(da)):
                continue
            pen_pts = p.pen * da
            hs, ls, cs = hi[a:w + 1], lo[a:w + 1], cl[a:w + 1]
            cands = []
            if p.side in ("both", "high") and np.isfinite(H[s]) and o9 <= H[s]:
                r = _side_trigger(hs, ls, cs, H[s], pen_pts, p.confirm, p.mode, True)
                if r is not None:
                    cands.append(r)
            if p.side in ("both", "low") and np.isfinite(L[s]) and o9 >= L[s]:
                r = _side_trigger(hs, ls, cs, L[s], pen_pts, p.confirm, p.mode, False)
                if r is not None:
                    cands.append(r)
            if not cands:
                continue
            if len(cands) == 2 and cands[0][0] == cands[1][0]:
                continue  # both sides on the same bar: ambiguous, no trade
            t, sd, ext = min(cands, key=lambda c: c[0])
            t_out[s], sd_out[s], ext_out[s] = a + t, sd, ext
        return {"t": t_out, "side": sd_out, "ext": ext_out, "H": H, "L": L}
    key = ("trig", p.level, p.side, p.window, round(p.pen, 9), p.confirm, p.mode)
    if p.level in data.level_override:
        return build()
    return data._get(key, build)


def planned_trades(data: OSData, p: OSParams) -> dict[str, np.ndarray]:
    """Every trade the rules call for, before sizing, in time order: trigger bar t, entry bar e,
    time-exit bar x, side, structural extreme, the range, dATR and whether x is a time exit."""
    validate_params(p)
    keys = ("t", "e", "x", "side", "s")
    if data.n == 0:
        out = {k: np.array([], dtype=np.int64) for k in keys}
        out.update({k: np.array([]) for k in ("ext", "H", "L", "datr")})
        out["timed"] = np.array([], dtype=bool)
        return out
    tr = session_triggers(data, p)
    de = data.day_end_idx
    t = tr["t"]
    e = t + 1
    x = np.minimum(data.bar_before(min(p.exit_min, DAY_END_MIN)), de)
    e_c = np.clip(e, 0, data.n - 1)
    t_c = np.clip(t, 0, data.n - 1)
    valid = (t >= 0) & (e <= de) & (data.tod[e_c] - data.tod[t_c] <= MAX_ENTRY_GAP_MIN) & (e <= x)
    s = np.flatnonzero(valid)
    return {"t": t[s], "e": e[s], "x": x[s].astype(np.int64), "side": tr["side"][s], "s": s.astype(np.int64),
            "ext": tr["ext"][s], "H": tr["H"][s], "L": tr["L"][s], "datr": data.datr[s], "timed": (x < de)[s]}


def stop_distance(p: OSParams, base: float, sd: int, ext: float, datr: float, tick: float) -> float:
    floor = MIN_STOP_DATR * datr
    if p.stop_kind == "datr":
        return max(p.stop_mult * datr, floor)
    pad = STRUCT_PAD_TICKS * tick
    raw = (base - (ext - pad)) if sd > 0 else ((ext + pad) - base)
    return max(raw, floor)


def target_price(p: OSParams, base: float, sd: int, dist: float, H: float, L: float) -> float:
    """nan = no target; a target on the wrong side of the entry returns -inf (skip the trade)."""
    if p.target_kind == "none":
        return float("nan")
    if p.target_kind == "r":
        return base + sd * p.target_r * dist
    if p.mode == "fade":
        tgt = L if sd < 0 else H
    else:
        tgt = H + (H - L) if sd > 0 else L - (H - L)
    return tgt if sd * (tgt - base) > 0 else float("-inf")


@dataclass
class SimResult:
    """Trades plus the bar indices needed for mark-to-market and integrity checks."""

    trades: list[Trade]
    equity_curve: list[EquityPoint]
    signal_idx: np.ndarray
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
    entry_base: np.ndarray    # entry price before slippage
    side: np.ndarray          # +1 long / -1 short
    stop_level: np.ndarray
    target_level: np.ndarray  # nan = no target


def simulate_open_sweep(
    data: OSData,
    cfg,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
    side_override: np.ndarray | None = None,
) -> SimResult:
    """Execution-stress knobs (default off): `entry_delay_bars` fills that many bars late (same
    session, not after the time-exit bar, else skipped); `missed_entry_frac` drops that fraction
    of the trades. `side_override` (one +1/-1 per planned trade) replaces the direction."""
    p = as_params(cfg)
    plan = planned_trades(data, p)
    if side_override is not None:
        if len(side_override) != len(plan["e"]):
            raise ValueError("side_override needs one entry per planned trade")
        plan["side"] = np.asarray(side_override, dtype=np.int64)
    o, hi, lo, c, ts, n = data.open, data.high, data.low, data.close, data.ts, data.n
    costs = CostModel.for_symbol(exec_config, p.symbol)
    tick = costs.tick
    thru = TARGET_THROUGH_TICKS * tick
    rng = np.random.default_rng(stress_seed) if missed_entry_frac > 0 else None

    trades: list[Trade] = []
    equity_curve: list[EquityPoint] = []
    rows: list[tuple] = []
    equity = starting_equity
    seq = 0
    free_from = 0
    for t, e0, x, sd, ext, H, L, da, timed in zip(
            plan["t"].tolist(), plan["e"].tolist(), plan["x"].tolist(), plan["side"].tolist(),
            plan["ext"].tolist(), plan["H"].tolist(), plan["L"].tolist(), plan["datr"].tolist(),
            plan["timed"].tolist()):
        if rng is not None and rng.random() < missed_entry_frac:
            continue
        e = e0 + entry_delay_bars
        if e < free_from or e > x:
            continue
        long = sd > 0
        base = o[e]
        dist = stop_distance(p, base, sd, ext, da, tick)
        stop = base - sd * dist
        tgt = target_price(p, base, sd, dist, H, L)
        if tgt == float("-inf"):
            continue
        fill_px = costs.fill(base, "buy" if long else "sell")
        qty = costs.size(equity, fill_px, fill_px - data.price_adj[e])
        if qty <= 0:
            continue
        seq += 1
        side_s = "long" if long else "short"
        entry_fill = Fill(order_id=f"e{seq}", symbol=p.symbol, side=side_s, quantity=qty, fill_price=fill_px,
                          fill_ts=ts[e], commission=costs.commission(qty),
                          slippage_points=abs(fill_px - base), bar_open_ts=ts[e])
        sh = np.flatnonzero(lo[e:x + 1] <= stop) if long else np.flatnonzero(hi[e:x + 1] >= stop)
        js = e + int(sh[0]) if len(sh) else x + 1
        jt = x + 1
        if np.isfinite(tgt):
            th = np.flatnonzero(hi[e:x + 1] >= tgt + thru) if long else np.flatnonzero(lo[e:x + 1] <= tgt - thru)
            jt = e + int(th[0]) if len(th) else x + 1
        if js <= x and js <= jt:
            j, why = js, STOP_EXIT
            exit_px = costs.fill(min(o[j], stop) if long else max(o[j], stop), "sell" if long else "buy", stop=True)
        elif jt <= x:
            j, why = jt, TARGET_EXIT
            exit_px = tgt
        else:
            j = x
            why = TIME_EXIT if timed else (FORCED if x == n - 1 else EOD_EXIT)
            exit_px = costs.fill(c[x], "sell" if long else "buy")
        forced = why == FORCED
        exit_fill = Fill(order_id=f"x{seq}", symbol=p.symbol, side=side_s, quantity=qty, fill_price=exit_px,
                         fill_ts=ts[j], commission=costs.commission(qty), slippage_points=0.0,
                         bar_open_ts=ts[j])
        commissions = entry_fill.commission + exit_fill.commission
        realized = sd * (exit_px - fill_px) * qty - commissions
        reason = {EOD_EXIT: ExitReason.SESSION_EXIT, FORCED: ExitReason.SESSION_EXIT,
                  TIME_EXIT: ExitReason.TIME_EXIT, STOP_EXIT: ExitReason.STOP_LOSS,
                  TARGET_EXIT: ExitReason.TAKE_PROFIT}[why]
        trades.append(Trade(
            trade_id=f"t{seq}", config_id="", symbol=p.symbol, side=side_s, entry_order_id=entry_fill.order_id,
            entry_fill=entry_fill, quantity=qty, stop_price=stop,
            target_price=tgt if np.isfinite(tgt) else None,
            exit_fill=exit_fill, exit_reason=reason, realized_pnl=realized,
            realized_r=realized / (dist * qty) if dist > 0 else None,
            commission_total=commissions, holding_bars=j - e,
        ))
        rows.append((t, e, j, t, qty, fill_px, exit_px, entry_fill.commission, realized, forced, why, base, sd,
                     stop, tgt))
        equity += realized
        equity_curve.append(EquityPoint(ts=ts[j], cash=equity, position_value=0.0, equity=equity))
        if forced:
            break
        free_from = j + 1

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
