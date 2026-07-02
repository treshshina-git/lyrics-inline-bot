from __future__ import annotations

from bot.models.song import Song
from bot.utils.text import safe_description, safe_title


def format_song_inline(song: Song) -> str:
    title = safe_title(song.title)
    artist = safe_description(song.artist)

    parts = [
        f"🎵 <b>{title}</b>",
        f"👤 {artist}",
    ]

    if song.album:
        parts.append(f"💽 {song.album}")

    if song.release_date:
        parts.append(f"📅 {song.release_date}")

    if song.lyrics:
        parts.append(f"📝 {song.lyrics}")

    if song.url:
        parts.append(f"\n🔗 {song.url}")

    return "\n".join(parts)