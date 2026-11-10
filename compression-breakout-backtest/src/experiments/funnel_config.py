"""Typed loader for the screening-funnel configuration (configs/funnel/*.yaml).

Every threshold lives in that one YAML file. The loaded model is frozen and
hashed (`config_sha256`) into every run's outputs so a run's thresholds can
never drift silently mid-run or between the development run and the frozen
validation / holdout steps.
"""

from __future__ import annotations

import hashlib
from datetime import date
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict

from src.utils.config_models import ExecutionConfig
from src.utils.hashing import canonical_json

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FUNNEL_CONFIG = PROJECT_ROOT / "configs" / "funnel" / "mr_funnel.yaml"


class _Frozen(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class Window(_Frozen):
    start: date
    end: date | None


class DataCfg(_Frozen):
    clean_root: str
    development: Window
    validation: Window
    holdout: Window
    timeframes: list[str]


class DataHistory(_Frozen):
    validation_previously_used_for_selection: bool
    validation_note: str
    holdout_previously_inspected: bool
    holdout_note: str


class MetricsCfg(_Frozen):
    return_frequency: Literal["daily"]
    periods_per_year: int
    risk_free_rate_annual: float
    cash_treatment: str
    drawdown_basis: str


class ExecutionRef(_Frozen):
    baseline: str


class IntegrityCfg(_Frozen):
    truncation_check_sample: int
    truncation_points: int


class TradeCountCfg(_Frozen):
    min_completed_trades: int
    min_trades_per_year: int
    min_years_meeting_floor: int


class PerformanceCfg(_Frozen):
    min_net_return: float
    min_sharpe: float
    max_drawdown: float | None
    max_drawdown_source: str | None = None


class PerturbationCfg(_Frozen):
    n_per_config: int
    integer_rel_step: float
    z_abs: float | None = None          # mean reversion: entry / exit z
    float_rel_step: float | None = None  # noise band: band multiple and ATR stop, relative


class LocalPerturbationCfg(_Frozen):
    """One-setting-at-a-time local moves (stage-4 gate when mode = local_perturbation).
    Lengths and the holding cap move by x(1 -/+ int_rel), rounded, at least 1 bar;
    z levels and a numeric ATR stop move by +/- the absolute steps."""
    int_rel: float
    stop_atr_abs: float
    entry_z_abs: float | None = None    # mean reversion
    exit_z_abs: float | None = None     # mean reversion
    band_mult_abs: float | None = None  # noise band
    kc_mult_abs: float | None = None    # compression breakout: Keltner multiple
    target_r_abs: float | None = None   # compression breakout: profit target in R
    min_box_atr_abs: float | None = None  # compression breakout: minimum box width in ATR


class PrescreenCfg(_Frozen):
    """Big grids only: when more than `max_configs` configs pass stage 3, cluster them first
    (stage-6 rules on development monthly returns) and send only the best `per_cluster` of
    each cluster by development Sharpe into stage 4. Fixed before the run, like every gate."""
    max_configs: int
    per_cluster: int


class ParamStabilityCfg(_Frozen):
    neighbor_mode: Literal["single_axis", "single_and_joint"]
    min_frac_profitable: float
    min_median_sharpe: float
    perturbation: PerturbationCfg
    # grid_neighbors: gate on one-step grid neighbors (original). local_perturbation:
    # gate on `local` moves; grid neighbors are then reported as a diagnostic only.
    mode: Literal["grid_neighbors", "local_perturbation"] = "grid_neighbors"
    local: LocalPerturbationCfg | None = None
    prescreen: PrescreenCfg | None = None


class TimeStabilityCfg(_Frozen):
    min_profitable_years: int
    top_trades_k: int
    top_trades_frac: float


class DedupCfg(_Frozen):
    corr_threshold: float
    return_basis: Literal["monthly"]
    linkage: Literal["complete", "average", "single"]
    reps_per_cluster: int = 1   # best-k per cluster go forward (a 1-member cluster yields 1)


class StressCfg(_Frozen):
    gate_cost_multiplier: float
    diagnostic_cost_multipliers: list[float]
    entry_delay_bars: int
    missed_entry_frac: float
    missed_entry_sims: int
    breakeven_max_multiplier: float


class ValidationCfg(_Frozen):
    min_net_return: float
    min_sharpe: float
    max_drawdown: float | None
    min_completed_trades: int


class ConfidenceCfg(_Frozen):
    dsr_threshold: float
    dsr_calibration_verified: bool
    effective_trials_method: Literal["li_ji", "participation_ratio", "raw"]
    serial_dependence: Literal["lag1_effective_n", "none"]
    transfer_symbol: str | None


class Acceptance(_Frozen):
    min_net_return: float
    min_sharpe: float
    max_drawdown: float | None
    min_completed_trades: int | None


class HoldoutCfg(_Frozen):
    acceptance: Acceptance


class ResearchTrial(_Frozen):
    name: str
    n_configs: int | None
    note: str


class FunnelConfig(_Frozen):
    version: int
    strategy: str
    symbol: str
    seed: int
    data: DataCfg
    data_history: DataHistory
    metrics: MetricsCfg
    execution: ExecutionRef
    integrity: IntegrityCfg
    trade_count: TradeCountCfg
    performance: PerformanceCfg
    parameter_stability: ParamStabilityCfg
    time_stability: TimeStabilityCfg
    dedup: DedupCfg
    execution_stress: StressCfg
    validation: ValidationCfg
    confidence: ConfidenceCfg
    holdout: HoldoutCfg
    research_history: list[ResearchTrial]

    @property
    def dev_years(self) -> list[int]:
        return list(range(self.data.development.start.year, self.data.development.end.year + 1))

    def config_sha256(self) -> str:
        d = self.model_dump(mode="json")
        # Keep the hashes of configs written before these knobs existed.
        if d["dedup"]["reps_per_cluster"] == 1:
            del d["dedup"]["reps_per_cluster"]
        ps = d["parameter_stability"]
        # Knobs one family doesn't use are left out of the hash when unset.
        for sub in (ps.get("local") or {}, ps["perturbation"]):
            for k in [k for k, v in sub.items() if v is None]:
                del sub[k]
        if ps["mode"] == "grid_neighbors" and ps["local"] is None:
            del ps["mode"], ps["local"]
        if ps.get("prescreen", 0) is None:
            del ps["prescreen"]
        return hashlib.sha256(canonical_json(d).encode()).hexdigest()


def load_funnel_config(path: Path = DEFAULT_FUNNEL_CONFIG) -> FunnelConfig:
    with open(path) as f:
        return FunnelConfig.model_validate(yaml.safe_load(f))


def load_execution_config(cfg: FunnelConfig) -> ExecutionConfig:
    p = Path(cfg.execution.baseline)
    if not p.is_absolute():
        p = PROJECT_ROOT / p
    with open(p) as f:
        return ExecutionConfig.model_validate(yaml.safe_load(f))
