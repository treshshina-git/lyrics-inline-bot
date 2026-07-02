from __future__ import annotations

import time
from collections import deque


class RateLimiter:
    """
    Sliding window rate limiter (in-memory).
    """

    def __init__(self, max_requests: int, window_seconds: float) -> None:
        self._max_requests = max_requests
        self._window = window_seconds
        self._events: dict[str, deque[float]] = {}

    def allow(self, key: str) -> bool:
        now = time.monotonic()

        queue = self._events.setdefault(key, deque())

        # remove expired events
        while queue and (now - queue[0]) > self._window:
            queue.popleft()

        if len(queue) >= self._max_requests:
            return False

        queue.append(now)
        return True

    def clear(self) -> None:
        self._events.clear()


inline_rate_limiter = RateLimiter(
    max_requests=10,
    window_seconds=5.0,
)