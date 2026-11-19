"""Hedge-ratio fitting for the EMRT spread: important extrema, EMRT, and the monthly refits.

Important extrema (Ning & Lee, after Fink & Pratt): a point is an important minimum when it is the
lowest of a segment whose two ends both sit at least R = C x s above it (s = the formation spread's
population sd); maxima likewise. They are found with a zigzag at threshold R: a running low is
confirmed as a minimum once the series has risen R above it, a running high as a maximum once it
has fallen R below it, alternating. Every confirmed pivot after the first then has a move of at
least R on BOTH sides (the previous, opposite pivot is at least R away), so the first pivot of each
series, which only has the move after it, is dropped.

EMRT = mean over the important extrema i of (first j > i where S_j - mean has the other sign, or
is 0) - i, in bars. An extremum the series never returns from is censored at the window's end
(L - i), which penalises spreads that do not revert. Fewer than MIN_PIVOTS extrema -> no EMRT.

Monthly refits: at the first bar of each calendar month m (NY session date) the hedge is fit on the
bars of months m-F .. m-1 (F = formation) -- all strictly before the trading month -- and used for
every bar of month m. A month is fit only when the data reaches back to the start of month m-F.
"""

from __future__ import annotations

import hashlib
import os
import pickle
from pathlib import Path

import numpy as np

from src.strategies.emrt_spread.config import (
    BETA_MAX,
    BETA_MIN,
    BETA_STEP,
    CONTROL_C,
    GRID_CS,
    MIN_PIVOTS,
    VARIANCE_CAP,
    hedge_name,
)

BETA_GRID = np.round(np.arange(BETA_MIN, BETA_MAX + BETA_STEP / 2, BETA_STEP), 6)
MIN_FORMATION_BARS = 100


def zigzag_pivots(S: np.ndarray, R: np.ndarray, resets: np.ndarray | None = None) -> np.ndarray:
    """Boolean (rows, L): the important extrema of each row of S at threshold R[row] (> 0).
    The first confirmed pivot of each row is dropped (see the module docstring). `resets` (bool,
    length L): the search restarts at each True index (session starts of an intraday spread), so
    no swing spans two segments and each segment's first pivot is dropped too."""
    S = np.atleast_2d(np.asarray(S, dtype=float))
    rows, L = S.shape
    if L < 2:
        return np.zeros((rows, L), dtype=bool)
    ST = np.ascontiguousarray(S.T)              # time-major: each step reads one contiguous row
    PT = np.zeros((L, rows), dtype=bool)
    R = np.broadcast_to(np.asarray(R, dtype=float), (rows,))
    mode = np.zeros(rows, dtype=np.int8)        # 0 undecided, +1 tracking a high, -1 tracking a low
    hi = ST[0].copy(); hi_i = np.zeros(rows, dtype=np.int64)
    lo = ST[0].copy(); lo_i = np.zeros(rows, dtype=np.int64)
    ext = ST[0].copy(); ext_i = np.zeros(rows, dtype=np.int64)
    first = np.ones(rows, dtype=bool)           # next confirmed pivot is the row's first (dropped)
    ar = np.arange(rows)
    n_undecided = rows

    def mark(m: np.ndarray, idx: np.ndarray) -> None:
        keep = m & ~first
        if keep.any():
            PT[idx[keep], ar[keep]] = True
        first[m] = False

    for t in range(1, L):
        x = ST[t]
        if resets is not None and resets[t]:
            mode[:] = 0
            hi[:] = x; lo[:] = x; ext[:] = x
            hi_i[:] = t; lo_i[:] = t; ext_i[:] = t
            first[:] = True
            n_undecided = rows
            continue
        if n_undecided:
            u = mode == 0
            nh = u & (x > hi)
            hi[nh], hi_i[nh] = x[nh], t
            nl = u & (x < lo)
            lo[nl], lo_i[nl] = x[nl], t
            cmin = u & (x - lo >= R)
            cmax = u & ~cmin & (hi - x >= R)
            if cmin.any():
                mark(cmin, lo_i)
                mode[cmin], ext[cmin], ext_i[cmin] = 1, x[cmin], t
            if cmax.any():
                mark(cmax, hi_i)
                mode[cmax], ext[cmax], ext_i[cmax] = -1, x[cmax], t
            n_undecided = int((mode == 0).sum())
            just = cmin | cmax
        else:
            just = None
        # tracking rows (rows that only just left "undecided" were fully handled above)
        up = mode == 1
        dn = mode == -1
        if just is not None:
            up &= ~just
            dn &= ~just
        d = x - ext
        newhi = up & (d > 0)
        newlo = dn & (d < 0)
        c_up = up & ~newhi & (-d >= R)
        c_dn = dn & ~newlo & (d >= R)
        nx = newhi | newlo
        ext[nx], ext_i[nx] = x[nx], t
        c = c_up | c_dn
        if c.any():
            mark(c, ext_i)
            mode[c_up], mode[c_dn] = -1, 1
            ext[c], ext_i[c] = x[c], t
    return np.ascontiguousarray(PT.T)


def emrt(S: np.ndarray, Cs, resets: np.ndarray | None = None,
         seg_end: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Per row of S and per threshold C in `Cs`: (EMRT in bars, shape (rows, len(Cs)) [inf when
    fewer than MIN_PIVOTS extrema], number of important extrema (same shape), mean, population sd).
    Segmented (intraday) series: `resets` restarts the extremum search at segment starts and
    `seg_end[i]` (last index of i's segment) censors a reversion at its segment's end."""
    S = np.atleast_2d(np.asarray(S, dtype=float))
    Cs = np.atleast_1d(np.asarray(Cs, dtype=float))
    rows, L = S.shape
    nC = len(Cs)
    mu = S.mean(axis=1)
    sd = S.std(axis=1)
    out = np.full((rows, nC), np.inf)
    npiv = np.zeros((rows, nC), dtype=np.int64)
    ok = sd > 0
    if not ok.any():
        return out, npiv, mu, sd
    So = S[ok]
    ro = len(So)
    R = (sd[ok][:, None] * Cs[None, :]).reshape(-1)
    P = zigzag_pivots(np.repeat(So, nC, axis=0), R, resets).reshape(ro, nC, L)
    D = So - mu[ok, None]
    idx = np.arange(L)
    # first j >= i with D_j <= 0 (resp. >= 0); L when none
    nxt_le = np.minimum.accumulate(np.where(D <= 0, idx, L)[:, ::-1], axis=1)[:, ::-1]
    nxt_ge = np.minimum.accumulate(np.where(D >= 0, idx, L)[:, ::-1], axis=1)[:, ::-1]
    back = np.where(D > 0, nxt_le, np.where(D < 0, nxt_ge, idx))  # D == 0: already at the mean
    if seg_end is not None:
        back = np.minimum(back, np.asarray(seg_end)[None, :] + 1)
    times = (back - idx).astype(float)
    del nxt_le, nxt_ge, back
    n = P.sum(axis=2)
    tot = np.einsum("rcl,rl->rc", P.astype(float), times)
    out[ok] = np.where(n >= MIN_PIVOTS, tot / np.maximum(n, 1), np.inf)
    npiv[ok] = n
    return out, npiv, mu, sd


def ols_beta(a: np.ndarray, b: np.ndarray) -> float:
    """Formation OLS slope of a on b (with intercept), clipped to [BETA_MIN, BETA_MAX]; NaN if b is flat."""
    vb = float(np.var(b))
    if not vb > 0:
        return float("nan")
    beta = float(np.mean((a - a.mean()) * (b - b.mean())) / vb)
    return float(np.clip(beta, BETA_MIN, BETA_MAX))


def hedge_names(cs) -> tuple[str, ...]:
    return (*(hedge_name(c) for c in cs), "ols", "notional")


def fit_formation(a: np.ndarray, b: np.ndarray, cs=GRID_CS, resets: np.ndarray | None = None,
                  seg_end: np.ndarray | None = None) -> dict[str, dict]:
    """Every hedge's fit on one formation window (a, b in notional units): the EMRT hedge at each
    C in `cs` plus the two controls. Returns {hedge: {beta, mu, sd, emrt, n_pivots}}; beta NaN =
    no tradable fit."""
    out: dict[str, dict] = {}
    HEDGES = hedge_names(cs)
    bo = ols_beta(a, b)
    nan = {"beta": float("nan"), "mu": float("nan"), "sd": float("nan"), "emrt": float("inf"), "n_pivots": 0}
    if not np.isfinite(bo):
        return {h: dict(nan) for h in HEDGES}
    Cs = sorted({round(float(c), 6) for c in cs})
    G = BETA_GRID
    S = a[None, :] - G[:, None] * b[None, :]
    var_cap = VARIANCE_CAP * float(np.var(a - bo * b))
    feasible = S.var(axis=1) <= var_cap
    E, NP, MU, SD = emrt(S, Cs, resets, seg_end)
    ctrl = np.stack([a - bo * b, a - 1.0 * b])
    e2, np2, mu2, sd2 = emrt(ctrl, [CONTROL_C], resets, seg_end)
    for r, h in enumerate(("ols", "notional")):
        beta = bo if h == "ols" else 1.0
        out[h] = ({"beta": beta, "mu": float(mu2[r]), "sd": float(sd2[r]), "emrt": float(e2[r, 0]),
                   "n_pivots": int(np2[r, 0])} if sd2[r] > 0 else dict(nan))
    for ci, C in enumerate(Cs):
        col = np.where(feasible & (SD > 0), E[:, ci], np.inf)
        h = hedge_name(C)
        if not np.isfinite(col).any():
            out[h] = dict(nan)
            continue
        g = int(np.argmin(col))  # first (smallest beta) on ties
        out[h] = {"beta": float(G[g]), "mu": float(MU[g]), "sd": float(SD[g]), "emrt": float(E[g, ci]),
                  "n_pivots": int(NP[g, ci])}
    return out


def month_keys(session_date: np.ndarray) -> np.ndarray:
    """Calendar-month key (year x 12 + month - 1) of each bar's NY session date."""
    y = session_date.astype("datetime64[Y]").astype(int) + 1970
    m = session_date.astype("datetime64[M]").astype(int) % 12
    return (y * 12 + m).astype(np.int64)


def monthly_fits(A: np.ndarray, B: np.ndarray, adjA: np.ndarray, adjB: np.ndarray,
                 session_date: np.ndarray, formation: int, cs=GRID_CS, intraday: dict | None = None) -> dict:
    """Refit every hedge at each month start. Returns arrays over the months that start in the
    data: key, start (first bar), fit_end (last formation bar, < start), anchors A0/RA/B0/RB and,
    per hedge, beta / mu / sd / emrt (NaN beta = not tradable that month).
    `intraday` = {"a", "b": session-anchored legs, "sess_start": bool, "sess_end": index arrays}:
    fit on those (anchors unused) with the extremum search and reversion confined to a session."""
    keys = month_keys(session_date)
    n = len(A)
    if n == 0:
        return {"key": np.array([], dtype=np.int64), "start": np.array([], dtype=np.int64), "fits": {}}
    starts = np.concatenate([[0], np.flatnonzero(keys[1:] != keys[:-1]) + 1])
    mkeys = keys[starts]
    first_key = int(keys[0])
    HEDGES = hedge_names(cs)
    rec = {k: [] for k in ("key", "start", "fit_start", "fit_end", "A0", "RA", "B0", "RB")}
    fits = {h: {k: [] for k in ("beta", "mu", "sd", "emrt", "n_pivots")} for h in HEDGES}
    for i, (s, mk) in enumerate(zip(starts.tolist(), mkeys.tolist())):
        lo_key = mk - formation
        fs = int(np.searchsorted(keys, lo_key, side="left")) if lo_key >= first_key else -1
        fe = s - 1
        ok = fs >= 0 and fe - fs + 1 >= MIN_FORMATION_BARS
        rec["key"].append(mk); rec["start"].append(s); rec["fit_start"].append(fs); rec["fit_end"].append(fe)
        if ok:
            A0, B0 = A[fe], B[fe]
            RA, RB = A0 - adjA[fe], B0 - adjB[fe]
            ok = RA > 0 and RB > 0
        if not ok:
            for k in ("A0", "RA", "B0", "RB"):
                rec[k].append(np.nan)
            for h in HEDGES:
                for k, v in (("beta", np.nan), ("mu", np.nan), ("sd", np.nan), ("emrt", np.inf), ("n_pivots", 0)):
                    fits[h][k].append(v)
            continue
        rec["A0"].append(A0); rec["RA"].append(RA); rec["B0"].append(B0); rec["RB"].append(RB)
        if intraday is None:
            a = (A[fs:fe + 1] - A0) / RA
            b = (B[fs:fe + 1] - B0) / RB
            f = fit_formation(a, b, cs)
        else:
            a, b = intraday["a"][fs:fe + 1], intraday["b"][fs:fe + 1]
            f = fit_formation(a, b, cs, resets=intraday["sess_start"][fs:fe + 1],
                              seg_end=intraday["sess_end"][fs:fe + 1] - fs)
        for h in HEDGES:
            for k in ("beta", "mu", "sd", "emrt", "n_pivots"):
                fits[h][k].append(f[h][k])
    out = {k: np.asarray(v, dtype=np.int64 if k in ("key", "start", "fit_start", "fit_end") else float)
           for k, v in rec.items()}
    out["fits"] = {h: {k: np.asarray(v, dtype=np.int64 if k == "n_pivots" else float) for k, v in d.items()}
                   for h, d in fits.items()}
    out["month_of_bar"] = np.searchsorted(starts, np.arange(n), side="right") - 1
    return out


# --- shared fit cache --------------------------------------------------------------------------
# The refits are the slow part and are identical for every config sharing (data, formation, C set),
# so a run computes each set once (precompute_fits) and its workers read it back. The key hashes
# the exact arrays the fit reads, so a truncated or longer data window can never reuse another's.
FIT_CACHE_ENV = "EMRT_FIT_CACHE"
_HEDGE_SRC = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:16]


def fit_key(A, B, adjA, adjB, session_date, formation: int, cs, intraday: dict | None = None) -> str:
    h = hashlib.sha256()
    arrs = [A, B, adjA, adjB] + ([] if intraday is None else [intraday["a"], intraday["b"], intraday["sess_end"]])
    for arr in arrs:
        h.update(np.ascontiguousarray(arr, dtype=np.float64).tobytes())
    if intraday is not None:
        h.update(b"intraday")
    h.update(np.ascontiguousarray(session_date.astype("datetime64[D]").astype(np.int64)).tobytes())
    h.update(f"{formation}|{tuple(round(float(c), 6) for c in cs)}|{_HEDGE_SRC}".encode())
    return h.hexdigest()[:32]


def cached_monthly_fits(A, B, adjA, adjB, session_date, formation: int, cs=GRID_CS,
                        intraday: dict | None = None) -> dict:
    """monthly_fits, read from / written to $EMRT_FIT_CACHE when that is set."""
    root = os.environ.get(FIT_CACHE_ENV)
    if not root:
        return monthly_fits(A, B, adjA, adjB, session_date, formation, cs, intraday)
    path = Path(root) / f"{fit_key(A, B, adjA, adjB, session_date, formation, cs, intraday)}.pkl"
    if path.exists():
        return pickle.loads(path.read_bytes())
    out = monthly_fits(A, B, adjA, adjB, session_date, formation, cs, intraday)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(f".{os.getpid()}.tmp")
    tmp.write_bytes(pickle.dumps(out, protocol=pickle.HIGHEST_PROTOCOL))
    tmp.replace(path)
    return out
