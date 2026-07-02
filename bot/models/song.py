from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Song:
    id: int
    title: str
    artist: str
    lyrics: str | None = None
    url: str
    thumbnail: str | None = None
    album: str | None = None
    release_date: str | None = None