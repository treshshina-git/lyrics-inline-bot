from __future__ import annotations

from bot.models.song import Song


def format_song_caption(song: Song) -> str:
    lines = [
        f"🎵 {song.title}",
        f"👤 {song.artist}",
    ]

    if song.album:
        lines.append(f"💽 {song.album}")

    if song.release_date:
        lines.append(f"📅 {song.release_date}")

    if song.url:
        lines.append(f"🔗 {song.url}")

    return "\n".join(lines)