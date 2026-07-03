from __future__ import annotations

from bot.models.song import Song
from bot.utils.text import safe_description, safe_title
from bot.services.genius import genius_api

async def format_song_inline(song: Song) -> str:
    print(f"format_song_inline: {song.title} - {song.artist} -> {song.id}")
    title = safe_title(song.title)
    artist = safe_description(song.artist)
    lyricser = await genius_api.get_song_lrc(title, artist)
    lyrics = str(lyricser) if lyricser else "Lyrics not found"
    parts = [
        f"<b>{title}</b>",
        f"👤 {artist}",
    ]

    #if song.album:
    #    parts.append(f"💽 {song.album}")

    #if song.release_date:
    #    parts.append(f"📅 {song.release_date}")

    if song.lyrics:
        parts.append(f"📝 {lyrics}")

    #if song.url:
    #    parts.append(f"\n🔗 {song.url}")

    return "\n".join(parts)