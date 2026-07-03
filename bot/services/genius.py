from __future__ import annotations

import asyncio
import logging

import lyricsgenius

from bot.config import settings
from bot.models.song import Song

logger = logging.getLogger(__name__)


class GeniusService:
    def __init__(self) -> None:
        self._client = lyricsgenius.Genius(
            settings.genius_access_token,
            verbose=False,
            remove_section_headers=False,
            skip_non_songs=True,
            timeout=10,
        )

    async def search(self, query: str, limit: int = 10) -> list[Song]:
        return await asyncio.to_thread(self._search_sync, query, limit)

    def _search_sync(self, query: str, limit: int) -> list[Song]:
        try:
            response = self._client.search(query, per_page=limit)
        except Exception as e:
            logger.exception("Genius search failed: %s", e)
            return []

        hits = response.get("hits", []) if isinstance(response, dict) else []

        results: list[Song] = []

        for item in hits:
            result = item.get("result", {})
            if not result:
                continue
            print(result)
            primary_artist = result.get("primary_artist", {}) or {}

            results.append(
                Song(
                    id=result.get("id", 0),
                    title=result.get("title", "Unknown"),
                    artist=primary_artist.get("name", "Unknown"),
                    url=result.get("url", ""),
                    lyrics=result.get("lyrics", None),
                    thumbnail=result.get("song_art_image_thumbnail_url"),
                    album=result.get("album", {}).get("name") if result.get("album") else None,
                    release_date=result.get("release_date_for_display"),
                )
            )

        return results


genius_service = GeniusService()