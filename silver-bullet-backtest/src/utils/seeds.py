"""Deterministic seeding for reproducible sampling and any stochastic components."""

from __future__ import annotations

import random

import numpy as np


def seed_everything(seed: int) -> np.random.Generator:
    """Seed stdlib random and return a numpy Generator seeded identically.

    Prefer the returned Generator for new code (numpy's modern API). stdlib `random`
    is seeded too for any legacy/third-party code paths that rely on it.
    """
    random.seed(seed)
    return np.random.default_rng(seed)


def derive_seed(base_seed: int, *labels: str) -> int:
    """Derive a reproducible child seed from a base seed and arbitrary labels.

    Use this instead of incrementing a counter so seeds stay stable even if
    unrelated configurations are added/removed/reordered upstream.
    """
    import hashlib

    payload = f"{base_seed}:" + ":".join(labels)
    digest = hashlib.sha256(payload.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % (2**32 - 1)
