from __future__ import annotations

import asyncio
from typing import Callable


class HealthCheck:
    """
    Simple async health checker for Railway / uptime monitoring.
    """

    def __init__(self) -> None:
        self._ok = True

    def set_ok(self, value: bool) -> None:
        self._ok = value

    def is_ok(self) -> bool:
        return self._ok

    async def wait_forever(self) -> None:
        while True:
            await asyncio.sleep(3600)


healthcheck = HealthCheck()


def health_endpoint() -> Callable[[], bool]:
    """
    Can be used later for HTTP server integration.
    """
    return healthcheck.is_ok