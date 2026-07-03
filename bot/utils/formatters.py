from __future__ import annotations

from bot.models.song import Song
from bot.utils.text import safe_description, safe_title
#from bot.services.genius import genius_api
from bot.services.lrclib import get_lyrics
async def format_song_inline(song: Song) -> str:

    title = safe_title(song.title)
    artist = safe_description(song.artist)

    lyricser = await get_lyrics(artist, title)
    print(f"format_song_inline: {lyricser}")
    #if lyricser is None:
    #    lyricser = "Lyrics not found"
    #else:
    #    print(f"format_song_inline: {lyricser}")
    #    lyricser = lyricser.strip()
        
    lyrics = lyricser if lyricser else "Lyrics not found"
    #lyrics = song.lyrics if song.lyrics else "Lyrics not found"
    parts = [
        f"<b>{title}</b>",
        f"👤 {artist}",
    ]

    #if song.album:
    #    parts.append(f"💽 {song.album}")

    #if song.release_date:
    #    parts.append(f"📅 {song.release_date}")

    if lyrics:
        parts.append(f"📝 {lyrics}")

    #if song.url:
    #    parts.append(f"\n🔗 {song.url}")

    return "\n".join(parts)