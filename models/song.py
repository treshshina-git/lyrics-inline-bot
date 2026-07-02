from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class Song:
    """
    Song model returned by Genius search.
    """

    id: int
    title: str
    artist: str
    url: str
    artwork_url: str | None = None
    album: str | None = None
    release_date: str | None = None

    @property
    def caption(self) -> str:
        return f"{self.title} — {self.artist}"

    @property
    def cache_key(self) -> str:
        return str(self.id)

    @classmethod
    def from_search_hit(cls, hit: dict[str, Any]) -> "Song":
        result = hit.get("result", {})

        artist = result.get("primary_artist", {}) or {}

        album = result.get("album")

        return cls(
            id=result.get("id", 0),
            title=result.get("title", "").strip(),
            artist=artist.get("name", "").strip(),
            url=result.get("url", ""),
            artwork_url=(
                result.get("song_art_image_thumbnail_url")
                or result.get("song_art_image_url")
            ),
            album=album.get("name") if isinstance(album, dict) else None,
            release_date=result.get("release_date_for_display"),
        )

    def to_callback_data(self) -> str:
        """
        Callback payload.

        Format:
            song:<id>
        """
        return f"song:{self.id}"

    @classmethod
    def from_callback_data(
        cls,
        callback_data: str,
        songs: list["Song"],
    ) -> "Song | None":
        if not callback_data.startswith("song:"):
            return None

        try:
            song_id = int(callback_data.split(":")[1])
        except (ValueError, IndexError):
            return None

        for song in songs:
            if song.id == song_id:
                return song

        return None