"""Portfolio config, sleeve loading (manifest -> params) and sleeve simulation.

A sleeve is the #1 candidate (candidates[0], development order) of one family's
selection manifest. It is simulated with the family's own simulator, its funnel
YAML's execution config and metric settings, on continuous history from 2018, so
its numbers match what that funnel's `validate` / `final-test` would report.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np
import polars as pl
import yaml
from pydantic import BaseModel, ConfigDict

from src.analysis.daily_performance import daily_equity, window_metrics
from src.data.aggregation import AGG_INTERVAL_MINUTES
from src.experiments.funnel_config import PROJECT_ROOT, FunnelConfig, load_execution_config, load_funnel_config
from src.experiments.funnel_prep import _metric_kwargs, family_for
from src.strategies.ma_crossover.backtest import MAParams
from src.strategies.ma_crossover.config import MACrossoverConfig, MACrossoverV2Config
from src.strategies.mean_reversion.backtest import MRParams
from src.strategies.mean_reversion.config import MeanReversionConfig, MeanReversionV2Config
from src.strategies.rsi_divergence.backtest import RSIParams
from src.strategies.rsi_divergence.config import (
    RSIDivergenceConfig,
    RSIDivergenceV2Config,
    RSIDivergenceV3Config,
)
from src.utils.hashing import canonical_json

# funnel YAML `strategy` -> (grid config class, simulator params class)
SPACES = {
    "mean_reversion": (MeanReversionConfig, MRParams),
    "mean_reversion_v2": (MeanReversionV2Config, MRParams),
    "rsi_divergence": (RSIDivergenceConfig, RSIParams),
    "rsi_divergence_v2": (RSIDivergenceV2Config, RSIParams),
    "rsi_divergence_v3": (RSIDivergenceV3Config, RSIParams),
    "ma_crossover": (MACrossoverConfig, MAParams),
    "ma_crossover_v2": (MACrossoverV2Config, MAParams),
}


def sha(obj) -> str:
    return hashlib.sha256(canonical_json(obj).encode()).hexdigest()


class _Frozen(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class SleeveSpec(_Frozen):
    name: str
    label: str
    weight: float
    manifest: str
    funnel_config: str


class Window(_Frozen):
    start: date
    end: date | None = None


class PortfolioConfig(_Frozen):
    version: int
    name: str
    symbol: str
    starting_equity: float
    rebalance: str
    sleeves: list[SleeveSpec]
    windows: dict[str, Window]

    def config_sha256(self) -> str:
        return sha(self.model_dump(mode="json"))


def load_portfolio_config(path: Path) -> PortfolioConfig:
    cfg = PortfolioConfig.model_validate(yaml.safe_load(Path(path).read_text()))
    if cfg.rebalance != "none":
        raise ValueError("Only rebalance: none is implemented")
    if abs(sum(s.weight for s in cfg.sleeves) - 1.0) > 1e-9:
        raise ValueError("Sleeve weights must sum to 1")
    return cfg


@dataclass(frozen=True)
class Sleeve:
    spec: SleeveSpec
    fcfg: FunnelConfig
    manifest: dict
    manifest_sha256: str
    candidate: dict
    params: object

    @property
    def timeframe(self) -> str:
        return self.params.timeframe


def _config_hashes(fcfg: FunnelConfig) -> set[str]:
    """The YAML's hash under this schema, plus under older schemas that lacked the
    optional perturbation fields added for later families (mean_reversion's funnel
    hashed a dump without `rsi_diff_abs` / `float_rel_step`)."""
    out = {fcfg.config_sha256()}
    d = fcfg.model_dump(mode="json")
    pert = d["parameter_stability"]["perturbation"]
    for k in ("z_abs", "rsi_diff_abs", "float_rel_step"):
        if pert.get(k) is None:
            pert.pop(k, None)
    out.add(sha(d))
    return out


def load_sleeve(spec: SleeveSpec, root: Path = PROJECT_ROOT) -> Sleeve:
    """Read the manifest, check it against its recorded hash and its funnel YAML, and
    build the simulator params of candidates[0]."""
    mpath = root / spec.manifest
    manifest = json.loads(mpath.read_text())
    msha = sha(manifest)
    recorded = mpath.with_suffix(".sha256")
    if recorded.exists() and recorded.read_text().strip() != msha:
        raise ValueError(f"{spec.name}: manifest hash {msha[:16]} != recorded {recorded.read_text()[:16]}")
    fcfg = load_funnel_config(root / spec.funnel_config)
    if manifest["config_sha256"] not in _config_hashes(fcfg):
        raise ValueError(f"{spec.name}: funnel config changed since the manifest was frozen")
    if not manifest["candidates"]:
        raise ValueError(f"{spec.name}: manifest has no validated candidates")
    cand = manifest["candidates"][0]
    cfg_cls, params_cls = SPACES[fcfg.strategy]
    params = params_cls.from_config(cfg_cls(**cand["params"]))
    return Sleeve(spec, fcfg, manifest, msha, cand, params)


@dataclass
class SleeveRun:
    sleeve: Sleeve
    funnel_metrics: dict      # window_metrics(), exactly as the funnel computes them
    days: np.ndarray          # window trading days (datetime64[D])
    rets: np.ndarray          # daily returns over `days`
    trades: pl.DataFrame      # trades entered in the window
    starts: np.ndarray        # position intervals overlapping the window, datetime64[us] [start, end)
    ends: np.ndarray


def simulate_sleeve(sleeve: Sleeve, bars: pl.DataFrame, *, start: date, end: date) -> SleeveRun:
    """`bars`: the sleeve timeframe's aggregated bars from the start of history."""
    fcfg = sleeve.fcfg
    fam = family_for(fcfg)
    ec = load_execution_config(fcfg)
    eq0 = ec.starting_equity
    data = fam.data_cls(bars)
    sim = fam.simulate(data, sleeve.params, exec_config=ec, starting_equity=eq0)
    eq = daily_equity(sim, data, eq0)
    m, rets = window_metrics(sim, data, eq, start=start, end=end, starting_equity=eq0, **_metric_kwargs(fcfg))
    s64, e64 = np.datetime64(start, "D"), np.datetime64(end, "D")
    days = data.days[(data.days >= s64) & (data.days <= e64)]

    ts = bars.sort("bar_open_ts")["bar_open_ts"].dt.replace_time_zone(None).to_numpy().astype("datetime64[us]")
    bar_len = np.timedelta64(AGG_INTERVAL_MINUTES[sleeve.timeframe], "m")
    ei, xi = sim.entry_idx.astype(int), sim.exit_idx.astype(int)
    starts, ends = ts[ei], ts[xi] + bar_len
    win_lo = ts[np.argmax(data.session_date >= s64)]
    win_hi = ts[len(ts) - 1 - np.argmax((data.session_date <= e64)[::-1])] + bar_len
    keep = (ends > win_lo) & (starts < win_hi)

    ent_day = data.session_date[ei]
    tmask = (ent_day >= s64) & (ent_day <= e64)
    notional = sim.quantity * sim.entry_px
    hold_bars = xi - ei + 1
    trades = pl.DataFrame({
        "sleeve": [sleeve.spec.name] * int(tmask.sum()),
        "entry_ts": ts[ei][tmask], "exit_ts": ts[xi][tmask],
        "entry_px": sim.entry_px[tmask], "exit_px": sim.exit_px[tmask],
        "quantity": sim.quantity[tmask], "pnl": sim.realized_pnl[tmask],
        "return": np.where(notional[tmask] > 0, sim.realized_pnl[tmask] / np.maximum(notional[tmask], 1e-12), 0.0),
        "hold_bars": hold_bars[tmask],
        "hold_minutes": hold_bars[tmask] * AGG_INTERVAL_MINUTES[sleeve.timeframe],
        "exit_reason": [str(x) for x in sim.exit_reason[tmask]],
        "forced_close": sim.forced_close[tmask],
    })
    return SleeveRun(sleeve, m, days, np.asarray(rets, float), trades, starts[keep], ends[keep])


def trade_stats(trades: pl.DataFrame) -> dict:
    n = trades.height
    if n == 0:
        return {"n_trades": 0}
    r = trades["return"].to_numpy()
    wins, losses = r[r > 0], r[r < 0]
    return {
        "n_trades": n,
        "win_rate": float((r > 0).mean()),
        "avg_trade_return": float(r.mean()),
        "avg_win": float(wins.mean()) if len(wins) else None,
        "avg_loss": float(losses.mean()) if len(losses) else None,
        "best_trade": float(r.max()), "worst_trade": float(r.min()),
        "profit_factor": (float(trades.filter(pl.col("pnl") > 0)["pnl"].sum()
                                / -trades.filter(pl.col("pnl") < 0)["pnl"].sum())
                          if (trades["pnl"] < 0).any() else None),
        "avg_hold_hours": float(trades["hold_minutes"].mean() / 60.0),
        "median_hold_hours": float(trades["hold_minutes"].median() / 60.0),
        "exit_reasons": dict(sorted(trades["exit_reason"].value_counts().iter_rows())),
    }
