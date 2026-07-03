from __future__ import annotations

import httpx
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
        #artist=results[0].get("primary_artist", {}).get("name", "") if results else None,
        #title=results[0].get("title", "") if results else None,
        #lyrics = await get_lyrics(artist, title) if results else None  
        #print(f"search: {query} -> {hits}")
        for item in hits[:limit]:
            result = item.get("result", {})
            #print(f"search: {query} -> {result.get('title', '')} - {result.get('primary_artist', {}).get('name', '')}")
            results.append(
                Song(
                    id=result.get("id", 0),
                    title=result.get("title", ""),
                    lyrics=None,  # lyrics will be fetched separately
                    #release_date=result.get("release_date", ""),
                    #album=result.get("album", {}).get("name", ""),
                    artist=result.get("primary_artist", {}).get("name", ""),
                    #url=result.get("url", ""),
                    #thumbnail=result.get("song_art_image_thumbnail_url"),
                )
            )

        return results

    async def get_song_lrc(self, title: str, artist: str) -> str | None:
        #print(f"get_song_lrc: {title} - {artist} -> 1")
        # Используем lrclib для получения текста песни

        lyrics = await get_lyrics(artist, title)
        if lyrics is None:
            return None
        else:
            #print(f" get_song_lrc: {title} - {artist} -> {lyrics}")
            data = lyrics
            #return lyrics
            
            #lyrics.raise_for_status()

                

            #r = await client.get(
            #    f"{self.base_url}/songs/{song_id}",
            #    headers=self.headers,
            #)
            #r.raise_for_status()
            #data = r.json()

            #song = lyrics
        print(f"get_song_lrc: {data} -> 7")
            #if not song:
            #    return None

        return lyrics
    


genius_api = GeniusAPI()