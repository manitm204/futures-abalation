"""Stable, deterministic hashing for configurations and datasets.

Used to produce config_id / dataset manifest hashes that stay stable across
process runs and machines (unlike Python's built-in `hash()`), enabling
reproducibility, duplicate-configuration detection, and resumable experiments.
"""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

import xxhash


def _default_json(obj: Any) -> Any:
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable for hashing")


def canonical_json(obj: Any) -> str:
    """Deterministic JSON serialization: sorted keys, fixed separators, no whitespace drift."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=_default_json)


def stable_hash(obj: Any, *, length: int = 16) -> str:
    """Stable hex digest for any JSON-serializable object (or pydantic model / dataclass)."""
    payload = canonical_json(obj).encode("utf-8")
    digest = xxhash.xxh3_128_hexdigest(payload)
    return digest[:length]


def config_id(config: Any) -> str:
    """Config hash used as the primary key for experiment configurations."""
    return f"cfg_{stable_hash(config, length=20)}"


def file_checksum(path: Path, *, algorithm: str = "sha256") -> str:
    """Checksum of a file's bytes, for raw-data manifest integrity records."""
    h = hashlib.new(algorithm)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()
