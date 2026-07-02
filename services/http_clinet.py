from __future__ import annotations

import httpx


class HttpClient:
    """
    Lightweight HTTP client wrapper for future integrations.
    """

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=10.0)

    async def get(self, url: str, params: dict | None = None) -> dict:
        response = await self._client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        await self._client.aclose()


http_client = HttpClient()