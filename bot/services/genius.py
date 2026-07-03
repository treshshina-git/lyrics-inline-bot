from __future__ import annotations

import httpx

from bot.config import settings
from bot.models.song import Song
from lrclib import get_lyrics

class GeniusAPI:
    def __init__(self) -> None:
        self.base_url = "https://api.genius.com"
        self.headers = {
            "Authorization": f"Bearer {settings.genius_access_token}"
        }

    async def search(self, query: str, limit: int = 10) -> list[Song]:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(
                f"{self.base_url}/search",
                params={"q": query},
                headers=self.headers,
            )
            r.raise_for_status()
            data = r.json()

        hits = data.get("response", {}).get("hits", [])

        results: list[Song] = []

        for item in hits[:limit]:
            result = item.get("result", {})

            results.append(
                Song(
                    id=result.get("id", 0),
                    title=result.get("title", ""),
                    artist=result.get("primary_artist", {}).get("name", ""),
                    url=result.get("url", ""),
                    thumbnail=result.get("song_art_image_thumbnail_url"),
                )
            )

        return results

    async def get_song(self, song_id: int) -> Song | None:
        async with httpx.AsyncClient(timeout=10) as client:
            get_lyrics_result = await get_lyrics(
                artist="Denzel Curry",
                title="ULTIMATE"
            )
            data = get_lyrics_result.json()
            #r = await client.get(
            #    f"{self.base_url}/songs/{song_id}",
            #    headers=self.headers,
            #)
            #r.raise_for_status()
            #data = r.json()

        song = data.get("response", {}).get("song")
        if not song:
            return None

        return Song(
            id=song.get("id", 0),
            title=song.get("title", ""),
            lyrics=get_lyrics_result,
            artist=song.get("primary_artist", {}).get("name", ""),
            url=song.get("url", ""),
            thumbnail=song.get("song_art_image_thumbnail_url"),
            album=song.get("album", {}).get("name") if song.get("album") else None,
            release_date=song.get("release_date_for_display"),
        )


genius_api = GeniusAPI()