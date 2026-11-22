from pathlib import Path

from src.utils.serialization import (
    atomic_write_json,
    atomic_write_yaml,
    read_json,
    read_yaml,
    raw_file_exists_and_immutable,
)


def test_atomic_write_json_roundtrip(tmp_path: Path) -> None:
    p = tmp_path / "nested" / "manifest.json"
    obj = {"symbol": "SPY", "rows": 1234, "checksums": ["a", "b"]}
    atomic_write_json(p, obj)
    assert p.exists()
    assert read_json(p) == obj


def test_atomic_write_yaml_roundtrip(tmp_path: Path) -> None:
    p = tmp_path / "config.yaml"
    obj = {"fvg": {"min_atr_multiple": 0.25, "timeframe": "5min"}}
    atomic_write_yaml(p, obj)
    assert read_yaml(p) == obj


def test_atomic_write_leaves_no_tmp_files(tmp_path: Path) -> None:
    p = tmp_path / "manifest.json"
    atomic_write_json(p, {"a": 1})
    leftovers = list(tmp_path.glob(".*.tmp"))
    assert leftovers == []


def test_raw_file_immutability_guard(tmp_path: Path) -> None:
    p = tmp_path / "raw.parquet"
    assert raw_file_exists_and_immutable(p) is False
    p.write_bytes(b"x")
    assert raw_file_exists_and_immutable(p) is True
