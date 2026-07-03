from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Song:
    id: int
    title: str
    lyrics: str | None
    artist: str
    #url: str
    #thumbnail: str | None = None
    #album: str | None = None
    #release_date: str | None = None