from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass(slots=True)
class CacheItem(Generic[T]):
    value: T
    expires_at: float


class TTLCache(Generic[T]):
    """
    Simple in-memory TTL cache (sync-safe).
    """

    def __init__(self, ttl: int = 300) -> None:
        self._ttl = ttl
        self._storage: dict[str, CacheItem[T]] = {}

    def get(self, key: str) -> T | None:
        item = self._storage.get(key)

        if item is None:
            return None

        if time.monotonic() > item.expires_at:
            self._storage.pop(key, None)
            return None

        return item.value

    def set(self, key: str, value: T) -> None:
        self._storage[key] = CacheItem(
            value=value,
            expires_at=time.monotonic() + self._ttl,
        )

    def clear(self) -> None:
        self._storage.clear()

    def cleanup(self) -> None:
        now = time.monotonic()

        expired_keys = [
            key for key, item in self._storage.items()
            if item.expires_at < now
        ]

        for key in expired_keys:
            self._storage.pop(key, None)