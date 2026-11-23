"""Compact 1-minute backtester for the volume-gated drift-burst fade (day session only).

Bars: the market's regular day session (`is_regular_session`, src/data/futures.py SESSIONS) in
1-minute bars (`db_day_bars`); each session is one NY date, so nothing can be held overnight.

Signal (all within one session; nothing crosses the overnight gap), k = burst_window:
    ret1_i  = log C_i - log C_{i-1}                         (NaN on a session's first bar)
    r_k(t)  = log C_t - log C_{t-k}                         (needs t - session start >= k)
    s(t)    = sqrt(mean of ret1^2 over bars t-6k+1 .. t-k)   (5k returns before the burst window;
                                                            needs t - session start >= 6k)
    T(t)    = r_k(t) / (s(t) sqrt(k))                       (NaN when s = 0)
    vnorm_i = mean volume at bar i's minute of day over the prior 20 sessions (>= 10 needed)
    ratio(t)= sum(volume, t-k+1..t) / sum(vnorm, t-k+1..t)  (NaN if any vnorm is NaN)

Decision at the close of bar t, with r = t - lag the burst reference bar, all in one session
(entry_mode: cross lag 0, peak lag 1 = v1, confirm lag 2):
  * cross:   |T_t| > threshold and |T_{t-1}| was not (same sign) -- a fresh cross;
  * peak:    |T_r| > threshold and |T| stopped rising at t (T_t NaN, opposite sign, or smaller);
  * confirm: as peak at r+1, and |T_{r+2}| < |T_{r+1}| (NaN counts as 0) or the sign flipped;
  * side = -sign(T_r) (fade); side = long_only keeps only longs (fades of drops);
  * vol gate: ratio(r) >= gate;
  * news filter: no news zone overlaps [open of bar r-k+1, open of bar t] (NY minutes);
  * bar t is not the session's last bar; at most `max_trades` trades per session (v1: 1); a
    signal while a position is open is dropped (never queued).

Execution (audited by src/experiments/db_integrity.py):
  * fill at the OPEN of bar t+1 (+ entry_delay_bars under stress) with market slippage; the fill
    bar must be in the decision's session, else the signal is skipped;
  * stop (v2, optional): base -/+ stop x B, B = |C_r - C_{r-k}| (the burst move), live intrabar
    from the entry bar, filled at the worse of the bar's open and the stop with stop slippage;
  * target (v2, optional): base +/- target x B, filled at the better of the bar's open and the
    target with market slippage; a bar touching both counts as the stop (stop_first);
  * time exit at the CLOSE of bar e + hold - 1 with market slippage; when that is at or past the
    session's last bar the trade closes at the session's last close (eod_exit);
  * one position at a time, compounding equity, unlevered whole contracts (the other families'
    sizing); every fill pays adverse slippage + commission;
  * a position closed on the data's final bar by the session-close rule is flagged forced and is
    not a completed trade.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import polars as pl

from src.engine.events import EquityPoint, ExitReason, Fill, Trade
from src.strategies.compression_breakout.backtest import CBData
from src.strategies.drift_burst.config import (
    ENTRY_LAG,
    ENTRY_MODES,
    NEWS_ZONES,
    SIDES,
    VOL_LOOKBACK_MULT,
    VOLUME_LOOKBACK_SESSIONS,
    VOLUME_MIN_SESSIONS,
    WED_ZONES,
)
from src.strategies.mean_reversion.backtest import CostModel, scale_variable_costs  # noqa: F401  (re-export)
from src.utils.config_models import ExecutionConfig

TIME_EXIT, EOD_EXIT, STOP_EXIT, TARGET_EXIT, FORCED = "time_exit", "eod_exit", "stop_exit", "target_exit", "forced_close"


def db_day_bars(df_1min: pl.DataFrame, *, timeframe: str = "1min") -> pl.DataFrame:
    """The strategy's bars: the regular day session's clean 1-minute bars. Single symbol."""
    if timeframe != "1min":
        raise ValueError(f"drift_burst runs on 1-minute bars only, got {timeframe!r}")
    if df_1min.is_empty():
        return df_1min
    return df_1min.filter(pl.col("is_regular_session")).sort("bar_open_ts")


class DBData(CBData):
    """CBData (session structure, tod, caching) plus the burst statistic and volume ratios."""

    def __init__(self, bars: pl.DataFrame) -> None:
        super().__init__(bars)
        self.volume = (bars.sort("bar_open_ts")["volume"].to_numpy().astype(float) if "volume" in bars.columns
                       else np.zeros(self.n))
        self.pos = np.arange(self.n) - self.sess_start if self.n else np.array([], dtype=np.int64)
        wd = (self.days.astype("datetime64[D]").view("int64") + 3) % 7  # 1970-01-01 was a Thursday -> Mon=0
        self.weekday = wd[self.sess] if self.n else np.array([], dtype=np.int64)

    def ret1(self) -> np.ndarray:
        def calc():
            lc = np.log(self.close)
            r = np.full(self.n, np.nan)
            if self.n > 1:
                r[1:] = lc[1:] - lc[:-1]
            r[self.pos == 0] = np.nan
            return r
        return self._get(("ret1",), calc)

    def tstat(self, k: int) -> np.ndarray:
        def calc():
            n, m = self.n, VOL_LOOKBACK_MULT * k
            lc = np.log(self.close)
            T = np.full(n, np.nan)
            if n <= m + k:
                return T
            rk = np.full(n, np.nan)
            rk[k:] = lc[k:] - lc[:-k]
            cs = np.concatenate([[0.0], np.cumsum(np.nan_to_num(self.ret1() ** 2))])
            idx = np.arange(n)
            hi, lo = idx - k + 1, idx - k - m + 1           # cs[hi] - cs[lo] = sum over i-k-m+1 .. i-k
            ok = self.pos >= (VOL_LOOKBACK_MULT + 1) * k
            S = np.full(n, np.nan)
            S[ok] = cs[hi[ok]] - cs[lo[ok]]
            s = np.sqrt(S / m)
            with np.errstate(invalid="ignore", divide="ignore"):
                T = np.where(ok & (s > 0), rk / (s * np.sqrt(k)), np.nan)
            return T
        return self._get(("T", k), calc)

    def vnorm(self) -> np.ndarray:
        """Mean volume at each bar's minute of day over the prior VOLUME_LOOKBACK_SESSIONS sessions."""
        def calc():
            df = pl.DataFrame({"tod": self.tod, "v": self.volume})
            out = df.select(pl.col("v").shift(1).rolling_mean(VOLUME_LOOKBACK_SESSIONS,
                                                               min_samples=VOLUME_MIN_SESSIONS).over("tod"))
            return out["v"].fill_null(np.nan).to_numpy().astype(float)
        return self._get(("vnorm",), calc)

    def volume_ratio(self, k: int) -> np.ndarray:
        def calc():
            n = self.n
            out = np.full(n, np.nan)
            if n < k:
                return out
            vn = self.vnorm()
            cv = np.concatenate([[0.0], np.cumsum(self.volume)])
            cn = np.concatenate([[0.0], np.cumsum(np.nan_to_num(vn))])
            cbad = np.concatenate([[0], np.cumsum(~np.isfinite(vn))])
            idx = np.arange(n)
            ok = self.pos >= k - 1
            a, b = idx[ok] - k + 1, idx[ok] + 1
            V, N, bad = cv[b] - cv[a], cn[b] - cn[a], cbad[b] - cbad[a]
            with np.errstate(invalid="ignore", divide="ignore"):
                out[ok] = np.where((bad == 0) & (N > 0), V / N, np.nan)
            return out
        return self._get(("vratio", k), calc)

    def news_blocked(self, k: int, lag: int = 1) -> np.ndarray:
        """Per decision bar t: does a news zone overlap [open of bar t-lag-k+1, open of bar t]?
        (r = t-lag is the burst bar, so its window starts at bar r-k+1; v1: lag 1 -> bar t-k.)"""
        w = k + lag - 1

        def calc():
            n = self.n
            start = np.full(n, -1, dtype=np.int64)
            same = np.zeros(n, dtype=bool)
            if w == 0:
                start, same = self.tod.copy(), np.ones(n, dtype=bool)
            elif n > w:
                start[w:] = self.tod[:-w]
                same[w:] = self.sess[w:] == self.sess[:-w]
            start = np.where(same, start, self.tod[self.sess_start])
            out = np.zeros(n, dtype=bool)
            for z0, z1 in NEWS_ZONES:
                out |= (start <= z1) & (self.tod >= z0)
            wed = self.weekday == 2
            for z0, z1 in WED_ZONES:
                out |= wed & (start <= z1) & (self.tod >= z0)
            return out
        return self._get(("news", k, lag), calc)


@dataclass(frozen=True)
class DBParams:
    """Free-valued strategy parameters (the config class restricts them to the grid lattice);
    used for off-grid perturbations too."""

    symbol: str
    timeframe: str
    burst_window: int
    threshold: float
    vol_gate: float | None   # None = no gate
    side: str
    hold: int
    news_filter: str
    entry_mode: str = "peak"          # v2; v1 configs are all "peak"
    target: float | None = None       # v2; x the burst move
    stop: float | None = None         # v2; x the burst move
    max_trades: int = 1               # v2; per session

    @classmethod
    def from_config(cls, cfg) -> "DBParams":
        return cls(cfg.symbol, cfg.timeframe, int(cfg.burst_window), float(cfg.threshold), cfg.vol_gate_value,
                   cfg.side, int(cfg.hold), cfg.news_filter, getattr(cfg, "entry_mode", "peak"),
                   getattr(cfg, "target_value", None), getattr(cfg, "stop_value", None),
                   int(getattr(cfg, "max_trades", 1)))


def as_params(cfg) -> DBParams:
    return cfg if isinstance(cfg, DBParams) else DBParams.from_config(cfg)


@dataclass
class SimResult:
    """Trades plus the bar indices needed for mark-to-market and integrity checks.
    `side` is +1 (long) / -1 (short); quantities are always positive."""

    trades: list[Trade]
    equity_curve: list[EquityPoint]
    signal_idx: np.ndarray     # decision bar t
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
    stop_level: np.ndarray    # nan = no stop
    entry_base: np.ndarray    # entry price before slippage
    side: np.ndarray
    peak_t: np.ndarray        # T at the burst reference bar (diagnostic)
    burst_pts: np.ndarray     # |C_r - C_{r-k}|, the burst move the stop / target scale with
    target_level: np.ndarray  # nan = no target


def signals(data: DBData, p: DBParams) -> dict[str, np.ndarray]:
    """Every decision bar t with its side; filters applied (the per-session cap and open positions
    are handled by the simulator)."""
    if p.side not in SIDES:
        raise ValueError(f"Unknown side {p.side!r}")
    if p.news_filter not in ("off", "on"):
        raise ValueError(f"Unknown news_filter {p.news_filter!r}")
    if p.entry_mode not in ENTRY_MODES:
        raise ValueError(f"Unknown entry_mode {p.entry_mode!r}")
    n, k, lag = data.n, p.burst_window, ENTRY_LAG[p.entry_mode]
    empty = {"k": np.array([], dtype=np.int64), "side": np.array([], dtype=np.int64), "peak_t": np.array([]),
             "burst_pts": np.array([])}
    if n < lag + 2:
        return empty
    T = data.tstat(k)

    def shift(a, j):
        """a[t - j] at t (NaN before the start), as floats."""
        out = np.full(n, np.nan)
        if j:
            out[j:] = a[:-j]
        else:
            out[:] = a
        return out
    sess_same = np.ones(n, dtype=bool)
    for j in range(1, max(lag, 1) + 1):
        sess_same &= shift(data.sess.astype(float), j) == data.sess
    Tr = shift(T, lag)                                       # T at r = t - lag
    with np.errstate(invalid="ignore"):
        if p.entry_mode == "cross":
            Tm = shift(T, 1)
            ok = (np.abs(T) > p.threshold) & ~((np.abs(Tm) > p.threshold) & (np.sign(Tm) == np.sign(T)))
        else:
            T1 = shift(T, lag - 1)                           # bar r + 1
            rising = np.isfinite(T1) & (np.sign(T1) == np.sign(Tr)) & (np.abs(T1) >= np.abs(Tr))
            ok = (np.abs(Tr) > p.threshold) & ~rising
            if p.entry_mode == "confirm":
                a1, a2 = np.abs(np.nan_to_num(T1)), np.abs(np.nan_to_num(T))
                flip = np.isfinite(T) & np.isfinite(T1) & (np.sign(T) != np.sign(T1))
                ok &= (a2 < a1) | flip
    ok &= sess_same
    side = -np.sign(np.nan_to_num(Tr)).astype(np.int64)
    ok &= side != 0
    if p.side == "long_only":
        ok &= side > 0
    if p.vol_gate is not None:
        vrr = shift(data.volume_ratio(k), lag)
        with np.errstate(invalid="ignore"):
            ok &= vrr >= p.vol_gate                           # NaN -> False
    if p.news_filter == "on":
        ok &= ~data.news_blocked(k, lag)
    ok &= ~data.is_last
    ks = np.flatnonzero(ok)
    lc = data.close
    r = ks - lag
    bp = np.abs(lc[r] - lc[np.maximum(r - k, 0)])
    return {"k": ks, "side": side[ks], "peak_t": Tr[ks], "burst_pts": bp}


def simulate_drift_burst(
    data: DBData,
    cfg,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
) -> SimResult:
    """Execution-stress knobs (default off): `entry_delay_bars` fills that many extra bars late
    (still within the session, else skipped); `missed_entry_frac` drops that fraction of the
    signals that would have been traded."""
    p = as_params(cfg)
    st = signals(data, p)
    o, hi, lo, c, ts, n = data.open, data.high, data.low, data.close, data.ts, data.n
    costs = CostModel.for_symbol(exec_config, p.symbol)
    rng = np.random.default_rng(stress_seed) if missed_entry_frac > 0 else None

    trades: list[Trade] = []
    equity_curve: list[EquityPoint] = []
    rows: list[tuple] = []
    equity = starting_equity
    seq = 0
    free_from = 0
    cur_sess, n_today = -1, 0
    for t, d, pt, bp in zip(st["k"].tolist(), st["side"].tolist(), st["peak_t"].tolist(), st["burst_pts"].tolist()):
        if data.sess[t] != cur_sess:
            cur_sess, n_today = int(data.sess[t]), 0
        if t < free_from or n_today >= p.max_trades:
            continue
        if rng is not None and rng.random() < missed_entry_frac:
            continue
        e = t + 1 + entry_delay_bars
        if e >= n or e > data.sess_end[t]:
            continue
        base = o[e]
        fill_px = costs.fill(base, "buy" if d > 0 else "sell")
        qty = costs.size(equity, fill_px, fill_px - data.price_adj[e])
        if qty <= 0:
            continue
        seq += 1
        n_today += 1
        L = int(data.sess_end[e])
        T = e + p.hold - 1
        if T < L:
            x, why = T, TIME_EXIT
        else:
            x, why = L, (FORCED if L == n - 1 else EOD_EXIT)
        side = "long" if d > 0 else "short"
        x_action = "sell" if d > 0 else "buy"
        stop = base - d * p.stop * bp if p.stop is not None else float("nan")
        target = base + d * p.target * bp if p.target is not None else float("nan")
        exit_px = None
        if p.stop is not None or p.target is not None:
            for j in range(e, x + 1):
                if p.stop is not None and ((d > 0 and lo[j] <= stop) or (d < 0 and hi[j] >= stop)):
                    px = min(o[j], stop) if d > 0 else max(o[j], stop)
                    x, why, exit_px = j, STOP_EXIT, costs.fill(px, x_action, stop=True)
                    break
                if p.target is not None and ((d > 0 and hi[j] >= target) or (d < 0 and lo[j] <= target)):
                    px = max(o[j], target) if d > 0 else min(o[j], target)
                    x, why, exit_px = j, TARGET_EXIT, costs.fill(px, x_action)
                    break
        if exit_px is None:
            exit_px = costs.fill(c[x], x_action)
        entry_fill = Fill(order_id=f"e{seq}", symbol=p.symbol, side=side, quantity=qty, fill_price=fill_px,
                          fill_ts=ts[e], commission=costs.commission(qty),
                          slippage_points=abs(fill_px - base), bar_open_ts=ts[e])
        exit_fill = Fill(order_id=f"x{seq}", symbol=p.symbol, side=side, quantity=qty, fill_price=exit_px,
                         fill_ts=ts[x], commission=costs.commission(qty), slippage_points=0.0, bar_open_ts=ts[x])
        commissions = entry_fill.commission + exit_fill.commission
        realized = d * (exit_px - fill_px) * qty - commissions
        forced = why == FORCED
        reason = {EOD_EXIT: ExitReason.SESSION_EXIT, FORCED: ExitReason.SESSION_EXIT,
                  TIME_EXIT: ExitReason.TIME_EXIT, STOP_EXIT: ExitReason.STOP_LOSS,
                  TARGET_EXIT: ExitReason.TAKE_PROFIT}[why]
        trades.append(Trade(
            trade_id=f"t{seq}", config_id="", symbol=p.symbol, side=side, entry_order_id=entry_fill.order_id,
            entry_fill=entry_fill, quantity=qty, stop_price=stop, target_price=None if p.target is None else target,
            exit_fill=exit_fill, exit_reason=reason, realized_pnl=realized, realized_r=None,
            commission_total=commissions, holding_bars=x - e,
        ))
        rows.append((t, e, x, t, qty, fill_px, exit_px, entry_fill.commission, realized, forced, why,
                     stop, base, d, pt, bp, target))
        equity += realized
        equity_curve.append(EquityPoint(ts=ts[x], cash=equity, position_value=0.0, equity=equity))
        if forced:
            break
        free_from = x + 1

    cols = list(zip(*rows)) if rows else [()] * 17
    f, i64 = (lambda a: np.asarray(a, dtype=float)), (lambda a: np.asarray(a, dtype=np.int64))
    return SimResult(
        trades=trades, equity_curve=equity_curve,
        signal_idx=i64(cols[0]), entry_idx=i64(cols[1]), exit_idx=i64(cols[2]), decision_idx=i64(cols[3]),
        quantity=f(cols[4]), entry_px=f(cols[5]), exit_px=f(cols[6]), entry_commission=f(cols[7]),
        realized_pnl=f(cols[8]), forced_close=np.asarray(cols[9], dtype=bool),
        exit_reason=np.asarray(cols[10], dtype=object), stop_level=f(cols[11]), entry_base=f(cols[12]),
        side=i64(cols[13]), peak_t=f(cols[14]), burst_pts=f(cols[15]), target_level=f(cols[16]),
    )
