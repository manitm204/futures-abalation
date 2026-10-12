"""Strategy registry. New strategies register themselves here; experiment/CLI
code looks strategies up by name instead of importing concrete classes."""

from __future__ import annotations

from typing import Callable

_REGISTRY: dict[str, Callable] = {}


def register_strategy(name: str) -> Callable:
    def _decorator(cls: Callable) -> Callable:
        if name in _REGISTRY:
            raise ValueError(f"Strategy {name!r} is already registered")
        _REGISTRY[name] = cls
        return cls

    return _decorator


def get_strategy(name: str) -> Callable:
    if name not in _REGISTRY:
        raise KeyError(f"Unknown strategy {name!r}. Registered: {sorted(_REGISTRY)}")
    return _REGISTRY[name]


def list_strategies() -> list[str]:
    return sorted(_REGISTRY)
