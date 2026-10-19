"""Atomic, versioned read/write helpers for JSON/YAML manifests and configs."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

import yaml

from src.utils.hashing import _default_json


def atomic_write_bytes(path: Path, data: bytes) -> None:
    """Write `data` to `path` atomically (write to temp file, fsync, rename).

    Prevents partial/corrupt files if the process is interrupted mid-write, which
    matters for immutable raw-data files and manifests that must not be silently
    corrupted or half-overwritten.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def atomic_write_json(path: Path, obj: Any, *, indent: int = 2) -> None:
    payload = json.dumps(obj, indent=indent, sort_keys=True, default=_default_json).encode("utf-8")
    atomic_write_bytes(path, payload)


def atomic_write_yaml(path: Path, obj: Any) -> None:
    payload = yaml.safe_dump(obj, sort_keys=True, default_flow_style=False).encode("utf-8")
    atomic_write_bytes(path, payload)


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def raw_file_exists_and_immutable(path: Path) -> bool:
    """Guard used before writing raw data: raw files are never overwritten implicitly."""
    return path.exists()
