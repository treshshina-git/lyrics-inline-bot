from __future__ import annotations

import asyncio
from typing import Any

import lyricsgenius
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)

from core.config import settings
from core.logger import get_logger
from models.song import Song
from services.cache import cache

logger = get_logger(__name__)


class GeniusServiceError(Exception):
    pass


class GeniusSearchError(GeniusServiceError):
    pass


class GeniusService:
    def __init__(self) -> None:
        self.client = lyricsgenius.PublicAPI(
            settings.genius.token,
            timeout=settings.genius.timeout,
        )

    @retry(
        stop=stop_after_attempt(settings.genius.retries),
        wait=wait_fixed(settings.genius.retry_delay),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    async def _search(
        self,
        query: str,
    ) -> dict[str, Any]:
        return await asyncio.to_thread(
            self.client.search,
            query=query,
            per_page=settings.genius.search_limit,
            page=1,
        )

    async def search(
        self,
        query: str,
    ) -> list[Song]:
        query = query.strip()

        if not query:
            return []

        cached = cache.search.get(query)

        if cached is not None:
            logger.info(
                "Search cache hit: %s",
                query,
            )
            return cached

        try:
            response = await self._search(query)
        except Exception as exc:
            logger.exception("Genius search failed")
            raise GeniusSearchError(str(exc)) from exc

        hits = response.get("hits", [])

        songs: list[Song] = []
        seen: set[int] = set()

        for hit in hits:
            try:
                song = Song.from_search_hit(hit)
            except Exception:
                continue

            if song.id in seen:
                continue

            seen.add(song.id)
            songs.append(song)

            cache.songs.set(song)

            if len(songs) >= settings.genius.search_limit:
                break

        cache.search.set(query, songs)

        logger.info(
            "Found %d songs for '%s'",
            len(songs),
            query,
        )

        return songs
    @retry(
        stop=stop_after_attempt(settings.genius.retries),
        wait=wait_fixed(settings.genius.retry_delay),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    async def _song(
        self,
        song_id: int,
    ) -> dict[str, Any]:
        return await asyncio.to_thread(
            self.client.song,
            song_id=song_id,
        )

    async def get_song(
        self,
        song_id: int,
    ) -> Song | None:
        cached = cache.songs.get(song_id)

        if cached is not None:
            logger.info(
                "Song cache hit: %s",
                song_id,
            )
            return cached

        try:
            response = await self._song(song_id)
        except Exception as exc:
            logger.exception("Failed to load song")

            raise GeniusSearchError(str(exc)) from exc

        song_data = response.get("song")

        if not song_data:
            return None

        artist = song_data.get(
            "primary_artist",
            {},
        )

        album = song_data.get("album")

        song = Song(
            id=song_data.get("id", 0),
            title=song_data.get("title", ""),
            artist=artist.get("name", ""),
            url=song_data.get("url", ""),
            artwork_url=(
                song_data.get("song_art_image_thumbnail_url")
                or song_data.get("song_art_image_url")
            ),
            album=(
                album.get("name")
                if isinstance(album, dict)
                else None
            ),
            release_date=song_data.get(
                "release_date_for_display"
            ),
        )

        cache.songs.set(song)

        return song

    async def healthcheck(self) -> bool:
        """
        Проверка доступности Genius API.
        """

        try:
            await self._search("Imagine")

            return True

        except Exception:
            logger.exception(
                "Genius API is unavailable."
            )

            return False


genius = GeniusService()