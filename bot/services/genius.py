from __future__ import annotations

import httpx, json

from bot.config import settings
from bot.models.song import Song
from .lrclib import get_lyrics

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
    
        #id=result.get("id", 0),
        lyrics = await get_lyrics(results[0].artist, results[0].title) if results else None  
        print(f"search: {query} -> {lyrics}")
        for item in hits[:limit]:
            result = item.get("result", {})
            
            results.append(
                Song(
                    id=result.get("id", 0),
                    title=result.get("title", ""),
                    lyrics=lyrics.get("lyrics", {}).get("plain", ""),
                    album=result.get("album", {}).get("name", ""),
                    artist=result.get("primary_artist", {}).get("name", ""),
                    url=result.get("url", ""),
                    thumbnail=result.get("song_art_image_thumbnail_url"),
                )
            )

        return results

    async def get_song_lrc(self, title: str, artist: str) -> str | None:
        async with httpx.AsyncClient(timeout=10) as client:
            lyrics = await get_lyrics(artist, title)

            print(f"get_song_lrc: {title} - {artist} -> {lyrics}")
            #lyrics.raise_for_status()
            #data = lyrics.json()

            #r = await client.get(
            #    f"{self.base_url}/songs/{song_id}",
            #    headers=self.headers,
            #)
            #r.raise_for_status()
            #data = r.json()

            song = lyrics
            print(f"get_song_lrc: {title} - {artist} -> {song}")
            if not song:
                return None

        return song.get("lyrics", {}).get("plain", None)
    


genius_api = GeniusAPI()