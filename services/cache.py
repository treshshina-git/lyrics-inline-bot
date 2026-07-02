from __future__ import annotations

from cachetools import TTLCache

from core.config import settings
from models.song import Song


class SearchCache:
    def __init__(self) -> None:
        self._cache: TTLCache[str, list[Song]] = TTLCache(
            maxsize=settings.cache.size,
            ttl=settings.cache.ttl,
        )

    def get(self, query: str) -> list[Song] | None:
        return self._cache.get(query)

    def set(self, query: str, songs: list[Song]) -> None:
        self._cache[query] = songs

    def clear(self) -> None:
        self._cache.clear()


class SongCache:
    def __init__(self) -> None:
        self._cache: TTLCache[int, Song] = TTLCache(
            maxsize=settings.cache.size,
            ttl=settings.cache.ttl,
        )

    def get(self, song_id: int) -> Song | None:
        return self._cache.get(song_id)

    def set(self, song: Song) -> None:
        self._cache[song.id] = song

    def clear(self) -> None:
        self._cache.clear()


class Cache:
    def __init__(self) -> None:
        self.search = SearchCache()
        self.songs = SongCache()

    def clear(self) -> None:
        self.search.clear()
        self.songs.clear()


cache = Cache()