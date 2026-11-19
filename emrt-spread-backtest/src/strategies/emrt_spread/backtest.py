"""Bar-based two-leg backtester for the EMRT spread (15min / 30min / 1h bars).

Data: the two legs' day-session bars of one timeframe, inner-joined on the bar open time (a bar
missing in either leg is dropped from both); leg A's columns keep the usual names (open .. close,
price_adjustment) so the session structure of CBData applies, leg B's are prefixed `b_`.

Hedge (src/strategies/emrt_spread/hedge.py): refit at each calendar-month start on the formation
window (the F months before), giving per month beta, anchors A0 / RA / B0 / RB, the formation
mean / sd of S and the spread's EMRT. Every bar of the month uses its month's hedge.

Spread and z at bar k (month params of k): S_k = (A_k - A0)/RA - beta (B_k - B0)/RB, on CLOSES.
    z_mode formation : z_k = (S_k - mu_F) / sd_F
    z_mode rolling_W : z_k = (S_k - mean) / sd over bars k-W+1..k (population; same beta / anchors)
z_prev_k is bar k-1's z under bar k's month params, so a refit never creates a cross by itself.

Decisions at bar k's close:
  * long spread (long A, short B) on a fresh cross z_k <= -entry_z (z_prev_k > -entry_z); short
    spread on z_k >= entry_z (z_prev_k < entry_z); side long / short / both; no decision on the
    session's last bar or less than `last_entry_cutoff` minutes before its last close; a signal
    while a position is open is dropped. A month with no tradable fit (no data back to month m-F,
    or no EMRT-eligible beta) has NaN z and so no entries.
  * entry fills at the NEXT bar's open (k+1+delay) on both legs with market slippage; that bar
    must be in the decision's session.
  * the open position keeps the hedge, anchors and z definition of its ENTRY month: its exits are
    judged on that z even after a refit (z_pos below).
Exits, checked from the entry bar's close on (bar j):
  * target: z_pos_j >= 0 (long; mean) / >= -entry_z / 2 (long; half); mirrored for a short;
  * stop:   z_pos_j <= -(entry_z + stop) (long) / >= entry_z + stop (short);
  * a target or stop decided at bar j's close fills at bar j+1's open (both legs; stop slippage for
    stops, market for targets) -- with overnight = hold that can be the next session's open;
  * time stop (3emrt): closed at the CLOSE of bar entry + H - 1, H = ceil(3 x EMRT of the entry
    month's spread) bars (no time stop when that EMRT is undefined);
  * overnight = flat: a position still open on the session's last bar is closed at that bar's CLOSE;
    a target / stop / time stop on that same bar also closes at that close;
  * the data's last bar closes any open position at its close, flagged forced (not a completed trade).
Sizing: whole contracts, gross notional |A leg| + |B leg| (raw price x multiplier) + entry
commissions <= equity (unlevered), qa = floor(equity / (VA (1 + beta))), qb = round(qa VA beta / VB),
reduced until it fits; a trade needs at least one contract per leg. Compounding on realized equity.
Costs: every fill on each leg pays its own tick slippage + commission per contract. With
overnight = hold, each roll of a leg's contract while the position is open (a change of its
price_adjustment between consecutive bars) costs that leg a round turn (2 x (commission + market
slippage) per contract); P&L across the roll uses the back-adjusted series, i.e. the real point moves.
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl

from src.data.futures import contract_spec
from src.strategies.compression_breakout.backtest import CBData
from src.strategies.emrt_spread.config import (
    GRID_CS,
    LAST_ENTRY_CUTOFF_MINUTES,
    TIME_STOP_EMRT_MULT,
    hedge_c,
    rolling_window,
    split_pair,
    tod_sessions,
)
from src.strategies.emrt_spread.hedge import FIT_CACHE_ENV, cached_monthly_fits
from src.strategies.mean_reversion.backtest import scale_variable_costs  # noqa: F401  (re-export)
from src.utils.config_models import ExecutionConfig

TARGET_EXIT, STOP_EXIT, TIME_EXIT, EOD_EXIT, FORCED = "target_exit", "stop_exit", "time_exit", "eod_exit", "forced_close"
LEG_COLS = ("open", "high", "low", "close", "price_adjustment", "volume")


def pair_frame(bars_a: pl.DataFrame, bars_b: pl.DataFrame, pair: str) -> pl.DataFrame:
    """Join two legs' aggregated bars (same timeframe) on bar open time and session date."""
    keep = ["bar_open_ts", "bar_close_ts", "bar_open_ts_ny", "session_date_ny", "timeframe", *LEG_COLS]
    a = bars_a.select([c for c in keep if c in bars_a.columns])
    if "price_adjustment" not in a.columns:
        a = a.with_columns(pl.lit(0.0).alias("price_adjustment"))
    b = bars_b.select(["bar_open_ts", "session_date_ny", *[c for c in LEG_COLS if c in bars_b.columns]])
    if "price_adjustment" not in b.columns:
        b = b.with_columns(pl.lit(0.0).alias("price_adjustment"))
    b = b.rename({c: f"b_{c}" for c in b.columns if c != "bar_open_ts"})
    j = a.join(b, on="bar_open_ts", how="inner").filter(pl.col("session_date_ny") == pl.col("b_session_date_ny"))
    return j.drop("b_session_date_ny").with_columns(pl.lit(pair).alias("symbol")).sort("bar_open_ts")


class PairData(CBData):
    """CBData's session structure on leg A, plus leg B, the monthly hedge fits and the z arrays."""

    def __init__(self, bars: pl.DataFrame) -> None:
        super().__init__(bars)
        df = self._df
        self.pair = str(df["symbol"][0]) if self.n and "symbol" in df.columns else ""
        self.b_open = df["b_open"].to_numpy().astype(float)
        self.b_close = df["b_close"].to_numpy().astype(float)
        self.b_price_adj = df["b_price_adjustment"].to_numpy().astype(float)
        self.a_close = self.close
        self.a_open = self.open

    # ---- session-anchored (intraday) legs: return since the session's first open ----
    def intraday(self) -> dict[str, np.ndarray]:
        def calc():
            s0 = self.sess_start
            ra = self.open[s0] - self.price_adj[s0]
            rb = self.b_open[s0] - self.b_price_adj[s0]
            with np.errstate(invalid="ignore", divide="ignore"):
                a = np.where(ra > 0, (self.close - self.open[s0]) / ra, np.nan)
                b = np.where(rb > 0, (self.b_close - self.b_open[s0]) / rb, np.nan)
            return {"a": a, "b": b, "sess_start": np.arange(self.n) == s0, "sess_end": self.sess_end.astype(np.int64),
                    "pos": np.arange(self.n) - s0}
        return self._get(("intraday",), calc)

    # ---- hedge fits ----
    def fits(self, formation: int, hedge: str | None = None, anchor: str = "formation_end") -> dict:
        """Monthly fits of every grid hedge (an off-grid EMRT C, e.g. from a stage-4 local move,
        is fit on its own). anchor = "session": fit on the session-anchored legs."""
        if anchor not in ("formation_end", "session"):
            raise ValueError(f"Unknown anchor {anchor!r}")
        c = hedge_c(hedge) if hedge is not None else None
        cs = GRID_CS if c is None or round(c, 6) in GRID_CS else (round(c, 6),)
        intra = None
        if anchor == "session":
            d = self.intraday()
            intra = {k: d[k] for k in ("a", "b", "sess_start", "sess_end")}
        return self._get(("fits", formation, cs, anchor), lambda: cached_monthly_fits(
            self.close, self.b_close, self.price_adj, self.b_price_adj, self.session_date, formation, cs, intra))

    def bar_params(self, formation: int, hedge: str, anchor: str = "formation_end") -> dict[str, np.ndarray]:
        """Per bar: its month's beta, mu, sd, emrt, anchors and month index (NaN = no fit)."""
        def calc():
            f = self.fits(formation, hedge, anchor)
            mi = f["month_of_bar"]
            h = f["fits"][hedge]
            return {"month": mi, "beta": h["beta"][mi], "mu": h["mu"][mi], "sd": h["sd"][mi],
                    "emrt": h["emrt"][mi], "A0": f["A0"][mi], "RA": f["RA"][mi], "B0": f["B0"][mi],
                    "RB": f["RB"][mi], "fit_end": f["fit_end"][mi]}
        return self._get(("bp", formation, hedge, anchor), calc)

    def rolling_stats(self, w: int) -> dict[str, np.ndarray]:
        def calc():
            # shifted by a constant first (variance and covariance are unchanged) to keep the
            # rolling sums small; the means are shifted back
            ca = float(self.close[0]) if self.n else 0.0
            cb = float(self.b_close[0]) if self.n else 0.0
            A, B = pd.Series(self.close - ca), pd.Series(self.b_close - cb)
            ra, rb = A.rolling(w, min_periods=w), B.rolling(w, min_periods=w)
            return {"mA": ra.mean().to_numpy() + ca, "mB": rb.mean().to_numpy() + cb,
                    "vA": ra.var(ddof=0).to_numpy(), "vB": rb.var(ddof=0).to_numpy(),
                    "cAB": A.rolling(w, min_periods=w).cov(B, ddof=0).to_numpy()}
        return self._get(("roll", w), calc)

    def tod_stats(self, n_sess: int) -> dict[str, np.ndarray]:
        """Per bar: mean / var of the intraday legs a, b and their covariance at the SAME bar of the
        session over the previous `n_sess` sessions (the current session excluded; at least
        max(5, n_sess // 2) of them must have that bar, else NaN)."""
        def calc():
            d = self.intraday()
            pos = d["pos"]
            ns = len(self.day_start_idx)
            L = int(pos.max()) + 1 if self.n else 0
            out = {}
            mats = {}
            for key, v in (("a", d["a"]), ("b", d["b"]), ("aa", d["a"] ** 2), ("bb", d["b"] ** 2),
                           ("ab", d["a"] * d["b"])):
                M = np.full((ns, L), np.nan)
                M[self.sess, pos] = v
                mats[key] = (pd.DataFrame(M).shift(1).rolling(n_sess, min_periods=max(5, n_sess // 2))
                             .mean().to_numpy()[self.sess, pos])
            out["mA"], out["mB"] = mats["a"], mats["b"]
            out["vA"] = np.maximum(mats["aa"] - mats["a"] ** 2, 0.0)
            out["vB"] = np.maximum(mats["bb"] - mats["b"] ** 2, 0.0)
            out["cAB"] = mats["ab"] - mats["a"] * mats["b"]
            return out
        return self._get(("tod", n_sess), calc)

    def z_at(self, idx: np.ndarray, bp: dict, z_mode: str, anchor: str = "formation_end") -> np.ndarray:
        """z of bars `idx` under the hedge params `bp` (arrays aligned with idx, or scalars)."""
        beta = bp["beta"]
        if anchor == "session":
            d = self.intraday()
            S = d["a"][idx] - beta * d["b"][idx]
        else:
            A0, RA, B0, RB = bp["A0"], bp["RA"], bp["B0"], bp["RB"]
            S = (self.close[idx] - A0) / RA - beta * (self.b_close[idx] - B0) / RB
        w, nt = rolling_window(z_mode), tod_sessions(z_mode)
        with np.errstate(invalid="ignore", divide="ignore"):
            if w is None and nt is None:
                return np.where(bp["sd"] > 0, (S - bp["mu"]) / bp["sd"], np.nan)
            if nt is not None:
                if anchor != "session":
                    raise ValueError("a time-of-day z needs the session anchor")
                r = self.tod_stats(nt)
                mu = r["mA"][idx] - beta * r["mB"][idx]
                var = r["vA"][idx] + beta ** 2 * r["vB"][idx] - 2 * beta * r["cAB"][idx]
                sd = np.sqrt(np.maximum(var, 0.0))
                return np.where(sd > 1e-12, (S - mu) / sd, np.nan)
            if anchor == "session":
                raise ValueError("a rolling z is defined for the formation-end anchor only")
            r = self.rolling_stats(w)
            mu = (r["mA"][idx] - A0) / RA - beta * (r["mB"][idx] - B0) / RB
            var = r["vA"][idx] / RA ** 2 + beta ** 2 * r["vB"][idx] / RB ** 2 - 2 * beta * r["cAB"][idx] / (RA * RB)
            sd = np.sqrt(np.maximum(var, 0.0))
            return np.where(sd > 1e-12, (S - mu) / sd, np.nan)

    def zscores(self, formation: int, hedge: str, z_mode: str, anchor: str = "formation_end") -> tuple[np.ndarray, np.ndarray]:
        """(z_k, z_prev_k) for every bar, both under bar k's month params. With the session anchor,
        z_prev of a session's first bar is NaN (the spread restarts there, so no cross can form)."""
        def calc():
            bp = self.bar_params(formation, hedge, anchor)
            k = np.arange(self.n)
            z = self.z_at(k, bp, z_mode, anchor)
            zp = np.full(self.n, np.nan)
            if self.n > 1:
                bp1 = {key: v[1:] for key, v in bp.items()}
                zp[1:] = self.z_at(k[:-1], bp1, z_mode, anchor)
                if anchor == "session":
                    zp[self.intraday()["sess_start"]] = np.nan
            return z, zp
        return self._get(("z", formation, hedge, z_mode, anchor), calc)


@dataclass(frozen=True)
class EMRTParams:
    """Free-valued strategy parameters (the config restricts them to the grid); used for off-grid
    perturbations too."""

    symbol: str
    timeframe: str
    formation: int
    hedge: str
    z_mode: str
    entry_z: float
    exit: str
    stop_z: float | None      # None = no stop
    time_stop: str
    side: str
    overnight: str
    time_stop_mult: float = TIME_STOP_EMRT_MULT
    last_entry_cutoff: int = LAST_ENTRY_CUTOFF_MINUTES
    anchor: str = "formation_end"   # v2: "session" (legs measured from today's open)
    first_entry: int = 0            # v2: no entry decision before this many minutes after the open

    @classmethod
    def from_config(cls, cfg) -> "EMRTParams":
        return cls(cfg.symbol, cfg.timeframe, int(cfg.formation), cfg.hedge, cfg.z_mode, float(cfg.entry_z),
                   cfg.exit, cfg.stop_z_value, cfg.time_stop, cfg.side, cfg.overnight,
                   anchor=getattr(cfg, "anchor", "formation_end"), first_entry=int(getattr(cfg, "first_entry", 0)))


def as_params(cfg) -> EMRTParams:
    return cfg if isinstance(cfg, EMRTParams) else EMRTParams.from_config(cfg)


@dataclass
class SimResult:
    """Per trade (one row per round trip of the pair). `side` +1 = long spread (long A, short B),
    -1 = short spread. qa / qb are contracts. `quantity` is 1 and entry_px / exit_px are the gross
    notional of both legs at the fills, so turnover = sum(quantity x (entry_px + exit_px)) is the
    traded notional, as for one-leg families."""

    trades: list
    equity_curve: list
    signal_idx: np.ndarray
    entry_idx: np.ndarray
    exit_idx: np.ndarray        # bar of the exit fill
    decision_idx: np.ndarray    # bar whose close decided the exit
    side: np.ndarray
    qa: np.ndarray
    qb: np.ndarray
    beta: np.ndarray
    month: np.ndarray
    a_entry: np.ndarray
    a_exit: np.ndarray
    b_entry: np.ndarray
    b_exit: np.ndarray
    a_entry_base: np.ndarray    # opens before slippage
    b_entry_base: np.ndarray
    entry_commission: np.ndarray
    roll_cost: np.ndarray
    n_rolls: np.ndarray
    hold_limit: np.ndarray      # time-stop bars (-1 = none)
    realized_pnl: np.ndarray
    forced_close: np.ndarray
    exit_reason: np.ndarray
    quantity: np.ndarray
    entry_px: np.ndarray
    exit_px: np.ndarray
    equity_before: np.ndarray


@dataclass(frozen=True)
class _Leg:
    mult: float
    tick: float


def _legs(pair: str) -> tuple[_Leg, _Leg]:
    a, b = split_pair(pair)
    sa, sb = contract_spec(a), contract_spec(b)
    return _Leg(sa.multiplier, sa.tick_size), _Leg(sb.multiplier, sb.tick_size)


def _slip(px: float, buy: bool, ticks: float, leg: _Leg) -> float:
    d = ticks * leg.tick
    return px + d if buy else px - d


def size_pair(equity: float, va: float, vb: float, beta: float, commission: float) -> tuple[int, int]:
    """Whole contracts (qa, qb) for a pair trade; (0, 0) if it does not fit."""
    if not (va > 0 and vb > 0 and beta > 0 and math.isfinite(va * vb * beta)):
        return 0, 0
    qa = math.floor(equity / (va * (1 + beta)))
    while qa >= 1:
        qb = round(qa * va * beta / vb)
        if qb >= 1 and qa * va + qb * vb + commission * (qa + qb) <= equity:
            return qa, qb
        qa -= 1
    return 0, 0


def signals(data: PairData, p: EMRTParams) -> dict[str, np.ndarray]:
    """Decision bars k and sides (+1 long spread / -1 short spread), filters applied."""
    if p.side not in ("long", "short", "both"):
        raise ValueError(f"Unknown side {p.side!r}")
    if p.anchor == "session" and p.overnight != "flat":
        raise ValueError("the session-anchored spread is intraday only (overnight = flat)")
    z, zp = data.zscores(p.formation, p.hedge, p.z_mode, p.anchor)
    E = p.entry_z
    with np.errstate(invalid="ignore"):
        long_ = (z <= -E) & (zp > -E)
        short = (z >= E) & (zp < E)
    side = np.where(long_, 1, np.where(short, -1, 0)).astype(np.int64)
    ok = side != 0
    if p.side == "long":
        ok &= side > 0
    elif p.side == "short":
        ok &= side < 0
    to_close = data.tod[data.sess_end] - data.tod
    ok &= ~data.is_last & (to_close >= p.last_entry_cutoff)
    if p.first_entry > 0:
        since_open = data.tod + data.tf_minutes - data.tod[data.sess_start]
        ok &= since_open >= p.first_entry
    ks = np.flatnonzero(ok)
    return {"k": ks, "side": side[ks]}


def time_stop_bars(p: EMRTParams, emrt_bars: float) -> int | None:
    if p.time_stop == "none":
        return None
    if p.time_stop != "3emrt":
        raise ValueError(f"Unknown time_stop {p.time_stop!r}")
    if not math.isfinite(emrt_bars):
        return None
    return max(1, math.ceil(p.time_stop_mult * emrt_bars))


def exit_levels(p: EMRTParams, d: int) -> tuple[float, float | None]:
    """(target level, stop level) on z_pos for side d: long exits at z >= target, stops at z <= stop."""
    if p.exit not in ("mean", "half"):
        raise ValueError(f"Unknown exit {p.exit!r}")
    tgt = 0.0 if p.exit == "mean" else p.entry_z / 2
    stop = None if p.stop_z is None else p.entry_z + p.stop_z
    return (-d * tgt if p.exit == "half" else 0.0), (None if stop is None else -d * stop)


def simulate_emrt_spread(
    data: PairData,
    cfg,
    *,
    exec_config: ExecutionConfig,
    starting_equity: float,
    entry_delay_bars: int = 0,
    missed_entry_frac: float = 0.0,
    stress_seed: int = 0,
) -> SimResult:
    """Execution-stress knobs (default off): `entry_delay_bars` fills entries that many extra bars
    late (still within the session, else skipped); `missed_entry_frac` drops that fraction of the
    signals that would have been traded."""
    p = as_params(cfg)
    if p.overnight not in ("flat", "hold"):
        raise ValueError(f"Unknown overnight {p.overnight!r}")
    hedge_c(p.hedge)  # validates the name
    st = signals(data, p)
    bp = data.bar_params(p.formation, p.hedge, p.anchor)
    la, lb = _legs(data.pair or p.symbol)
    ec = exec_config
    com, tk_m, tk_s = ec.commission_per_contract, ec.slippage_ticks_market, ec.slippage_ticks_stop
    oA, cA, oB, cB = data.open, data.close, data.b_open, data.b_close
    adjA, adjB = data.price_adj, data.b_price_adj
    n = data.n
    flat = p.overnight == "flat"
    rng = np.random.default_rng(stress_seed) if missed_entry_frac > 0 else None
    rollA = np.concatenate([[False], adjA[1:] != adjA[:-1]]) if n else np.zeros(0, bool)
    rollB = np.concatenate([[False], adjB[1:] != adjB[:-1]]) if n else np.zeros(0, bool)
    cumRA, cumRB = np.cumsum(rollA), np.cumsum(rollB)

    rows: list[tuple] = []
    equity = starting_equity
    free_from = 0
    for k, d in zip(st["k"].tolist(), st["side"].tolist()):
        if k < free_from:
            continue
        if rng is not None and rng.random() < missed_entry_frac:
            continue
        e = k + 1 + entry_delay_bars
        if e >= n or e > data.sess_end[k]:
            continue
        beta = float(bp["beta"][k])
        va = (oA[e] - adjA[e]) * la.mult
        vb = (oB[e] - adjB[e]) * lb.mult
        qa, qb = size_pair(equity, va, vb, beta, com)
        if qa < 1:
            continue
        a_in = _slip(oA[e], d > 0, tk_m, la)
        b_in = _slip(oB[e], d < 0, tk_m, lb)
        entry_com = com * (qa + qb)
        pp = {key: v[k] for key, v in bp.items()}
        H = time_stop_bars(p, float(pp["emrt"]))
        T = e + H - 1 if H is not None else n
        tgt, stp = exit_levels(p, d)

        # scan exits block by block (z under the entry month's params)
        j0, blk = e, 64
        found = None
        while found is None:
            j1 = min(n, j0 + blk)
            idx = np.arange(j0, j1)
            zz = data.z_at(idx, pp, p.z_mode, p.anchor)
            with np.errstate(invalid="ignore"):
                hit_t = (zz >= tgt) if d > 0 else (zz <= tgt)
                hit_s = np.zeros(len(idx), bool) if stp is None else ((zz <= stp) if d > 0 else (zz >= stp))
            close_now = (idx == T) | (idx == n - 1)
            if flat:
                close_now |= idx == data.sess_end[idx]
            ev = np.flatnonzero(hit_t | hit_s | close_now)
            if len(ev):
                found = int(idx[ev[0]])
                why_s, why_t = bool(hit_s[ev[0]]), bool(hit_t[ev[0]])
                break
            j0, blk = j1, blk * 2
        j = found
        at_close = j == T or j == n - 1 or (flat and j == data.sess_end[j])
        if j == n - 1:
            why = FORCED          # the data ends here (its session may be cut short)
        elif why_s:
            why = STOP_EXIT
        elif why_t:
            why = TARGET_EXIT
        elif j == T:
            why = TIME_EXIT
        else:
            why = EOD_EXIT
        if at_close:
            x = j
            a_px, b_px = cA[x], cB[x]
        else:
            x = j + 1
            a_px, b_px = oA[x], oB[x]
        ticks = tk_s if why == STOP_EXIT else tk_m
        a_out = _slip(a_px, d < 0, ticks, la)
        b_out = _slip(b_px, d > 0, ticks, lb)
        exit_com = com * (qa + qb)
        nra = int(cumRA[x] - cumRA[e])
        nrb = int(cumRB[x] - cumRB[e])
        roll = (nra * qa * 2 * (com + tk_m * la.tick * la.mult)
                + nrb * qb * 2 * (com + tk_m * lb.tick * lb.mult))
        pnl = (d * qa * la.mult * (a_out - a_in) - d * qb * lb.mult * (b_out - b_in)
               - entry_com - exit_com - roll)
        g_in = qa * la.mult * (a_in - adjA[e]) + qb * lb.mult * (b_in - adjB[e])
        g_out = qa * la.mult * (a_out - adjA[x]) + qb * lb.mult * (b_out - adjB[x])
        forced = why == FORCED
        rows.append((k, e, x, j, d, qa, qb, beta, int(pp["month"]), a_in, a_out, b_in, b_out, oA[e], oB[e],
                     entry_com, roll, nra + nrb, -1 if H is None else H, pnl, forced, why, 1.0, g_in, g_out, equity))
        equity += pnl
        if forced:
            break
        free_from = x  # a decision at the exit bar's close may enter on the next bar

    cols = list(zip(*rows)) if rows else [()] * 26
    f, i64 = (lambda a: np.asarray(a, dtype=float)), (lambda a: np.asarray(a, dtype=np.int64))
    return SimResult(
        trades=[], equity_curve=[],
        signal_idx=i64(cols[0]), entry_idx=i64(cols[1]), exit_idx=i64(cols[2]), decision_idx=i64(cols[3]),
        side=i64(cols[4]), qa=i64(cols[5]), qb=i64(cols[6]), beta=f(cols[7]), month=i64(cols[8]),
        a_entry=f(cols[9]), a_exit=f(cols[10]), b_entry=f(cols[11]), b_exit=f(cols[12]),
        a_entry_base=f(cols[13]), b_entry_base=f(cols[14]), entry_commission=f(cols[15]), roll_cost=f(cols[16]),
        n_rolls=i64(cols[17]), hold_limit=i64(cols[18]), realized_pnl=f(cols[19]),
        forced_close=np.asarray(cols[20], dtype=bool), exit_reason=np.asarray(cols[21], dtype=object),
        quantity=f(cols[22]), entry_px=f(cols[23]), exit_px=f(cols[24]), equity_before=f(cols[25]),
    )


def pair_daily_equity(sim: SimResult, data: PairData, starting_equity: float) -> np.ndarray:
    """Mark-to-market equity at every session close: realized P&L of trades exited by then, plus
    an open trade's two legs marked at the closes, minus its entry commissions."""
    e = data.day_end_idx
    eq = np.full(len(e), float(starting_equity))
    if len(sim.entry_idx) == 0:
        return eq
    la, lb = _legs(data.pair)
    cum = np.concatenate([[0.0], np.cumsum(sim.realized_pnl)])
    eq += cum[np.searchsorted(sim.exit_idx, e, side="right")]
    j = np.searchsorted(sim.entry_idx, e, side="right") - 1
    has = j >= 0
    jj = np.where(has, j, 0)
    om = has & (sim.exit_idx[jj] > e)
    if om.any():
        jo, eo = jj[om], e[om]
        d = sim.side[jo]
        eq[om] += (d * sim.qa[jo] * la.mult * (data.close[eo] - sim.a_entry[jo])
                   - d * sim.qb[jo] * lb.mult * (data.b_close[eo] - sim.b_entry[jo])
                   - sim.entry_commission[jo])
    return eq


def _fit_job(args) -> str:
    path, formation, hedge, anchor, cache = args
    os.environ[FIT_CACHE_ENV] = cache
    d = PairData(pl.read_parquet(path))
    d.fits(formation, hedge, anchor)
    return f"{path}|{formation}|{hedge}|{anchor}"


def precompute_fits(jobs: list[tuple], cache_dir: Path, n_workers: int = 1) -> int:
    """Fill the shared fit cache for each (frame, formation, hedge) -- hedge None or a grid hedge =
    the grid C set, an off-grid EMRT hedge = its own C -- in parallel, and point this process (and
    the workers it spawns later) at the cache. Returns the number of fit sets requested."""
    import multiprocessing
    import tempfile
    from concurrent.futures import ProcessPoolExecutor
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ[FIT_CACHE_ENV] = str(cache_dir)
    with tempfile.TemporaryDirectory() as td:
        paths: dict[int, str] = {}
        todo, seen = [], set()
        for job in jobs:
            df, formation, hedge = job[:3]
            anchor = job[3] if len(job) > 3 else "formation_end"
            c = hedge_c(hedge) if hedge is not None else None
            cs = GRID_CS if c is None or round(c, 6) in GRID_CS else (round(c, 6),)
            if (id(df), int(formation), cs, anchor) in seen:
                continue
            seen.add((id(df), int(formation), cs, anchor))
            if id(df) not in paths:
                paths[id(df)] = str(Path(td) / f"f{len(paths)}.parquet")
                df.write_parquet(paths[id(df)])
            todo.append((paths[id(df)], int(formation), hedge, anchor, str(cache_dir)))
        if n_workers <= 1 or len(todo) < 2:
            for j in todo:
                _fit_job(j)
        else:
            with ProcessPoolExecutor(max_workers=min(n_workers, len(todo)),
                                     mp_context=multiprocessing.get_context("spawn")) as ex:
                list(ex.map(_fit_job, todo))
    return len(todo)
