"""Reproducible, coverage-preserving sampling of SilverBulletConfig instances
from a SearchSpace.

Uses a scrambled Sobol sequence (quasi-random, coverage-preserving) for
continuous/integer dimensions and a seeded independent draw for categorical
dimensions, stratified so every categorical combination gets roughly
proportional representation rather than relying on naive i.i.d. random
sampling to happen to cover the space evenly.

Reproducibility contract: same (space, n, seed) -> identical sampled config
list, in the same order, every time -- this is what "resume an interrupted
search" and "prevent duplicate configurations" both depend on.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.stats import qmc

from src.experiments.spaces import Dimension, SearchSpace
from src.strategies.ict_silver_bullet.config import SilverBulletConfig
from src.utils.hashing import config_id as compute_config_id


@dataclass
class SampledConfig:
    config: SilverBulletConfig
    config_id: str
    seed: int


def _categorical_dims(space: SearchSpace) -> list[Dimension]:
    return [d for d in space.dimensions if d.kind == "categorical"]


def _numeric_dims(space: SearchSpace) -> list[Dimension]:
    return [d for d in space.dimensions if d.kind != "categorical"]


def _strata(space: SearchSpace) -> list[dict]:
    """Cartesian product of all categorical dimensions -- each combination is
    one stratum. For the default space this is a modest number of strata
    (symbol x timeframe x fvg_entry_rule x ... ), so sampling can allocate
    roughly n/len(strata) draws to each, preserving coverage across categorical
    choices instead of letting large-cardinality dims dominate.
    """
    cat_dims = _categorical_dims(space)
    if not cat_dims:
        return [{}]
    combos: list[dict] = [{}]
    for d in cat_dims:
        combos = [dict(c, **{d.name: choice}) for c in combos for choice in d.choices]
    return combos


def sample_configs(
    space: SearchSpace, *, n: int, seed: int, max_attempts_multiplier: int = 20
) -> list[SampledConfig]:
    """Draw up to `n` unique, valid configs. Invalid raw draws (rejected by
    SilverBulletConfig's conditional validators) are skipped, not silently
    coerced -- the Sobol sequence just keeps advancing until `n` valid unique
    configs are found or the attempt budget is exhausted.
    """
    strata = _strata(space)
    numeric_dims = _numeric_dims(space)
    n_numeric = len(numeric_dims)

    rng = np.random.default_rng(seed)
    per_stratum = max(1, -(-n // len(strata)))  # ceil division
    sobol_engine = qmc.Sobol(d=max(n_numeric, 1), scramble=True, seed=seed) if n_numeric > 0 else None

    results: list[SampledConfig] = []
    seen_ids: set[str] = set()
    max_attempts = n * max_attempts_multiplier

    attempts = 0
    stratum_idx = 0
    draws_per_stratum: dict[int, int] = {}

    while len(results) < n and attempts < max_attempts:
        s_idx = stratum_idx % len(strata)
        stratum = strata[s_idx]
        stratum_idx += 1
        attempts += 1
        draws_per_stratum[s_idx] = draws_per_stratum.get(s_idx, 0) + 1
        if draws_per_stratum[s_idx] > per_stratum * max_attempts_multiplier:
            continue  # this stratum has been over-sampled without success; move on

        raw: dict = dict(stratum)
        if sobol_engine is not None:
            point = sobol_engine.random(1)[0]
        else:
            point = np.array([])

        for i, d in enumerate(numeric_dims):
            u = point[i]
            if d.kind == "int_range":
                raw[d.name] = int(round(d.low + u * (d.high - d.low)))
            else:
                raw[d.name] = float(d.low + u * (d.high - d.low))

        try:
            cfg = SilverBulletConfig(**raw)
        except Exception:
            continue  # invalid combination for this draw -- skip, don't coerce

        cid = compute_config_id(cfg.model_dump(mode="json"))
        if cid in seen_ids:
            continue

        seen_ids.add(cid)
        results.append(SampledConfig(config=cfg, config_id=cid, seed=seed))

    return results
