from pathlib import Path

from src.utils.hashing import canonical_json, config_id, file_checksum, stable_hash


def test_stable_hash_is_order_independent() -> None:
    a = {"symbol": "SPY", "window": "ny_am", "risk": 0.0025}
    b = {"risk": 0.0025, "window": "ny_am", "symbol": "SPY"}
    assert stable_hash(a) == stable_hash(b)


def test_stable_hash_is_deterministic_across_calls() -> None:
    obj = {"x": [1, 2, 3], "y": {"nested": True}}
    assert stable_hash(obj) == stable_hash(obj)


def test_stable_hash_differs_for_different_values() -> None:
    assert stable_hash({"a": 1}) != stable_hash({"a": 2})


def test_config_id_prefix_and_stability() -> None:
    cfg = {"symbol": "QQQ", "fvg_min_atr": 0.25}
    cid1 = config_id(cfg)
    cid2 = config_id(cfg)
    assert cid1 == cid2
    assert cid1.startswith("cfg_")


def test_canonical_json_sorted_keys() -> None:
    assert canonical_json({"b": 1, "a": 2}) == canonical_json({"a": 2, "b": 1})


def test_file_checksum(tmp_path: Path) -> None:
    f = tmp_path / "sample.bin"
    f.write_bytes(b"hello world")
    checksum1 = file_checksum(f)
    f2 = tmp_path / "sample2.bin"
    f2.write_bytes(b"hello world")
    assert checksum1 == file_checksum(f2)

    f3 = tmp_path / "sample3.bin"
    f3.write_bytes(b"different content")
    assert checksum1 != file_checksum(f3)
