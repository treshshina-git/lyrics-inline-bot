from __future__ import annotations

from html import escape

from models.song import Song


class Formatter:
    @staticmethod
    def inline_title(song: Song) -> str:
        return f"{song.title} — {song.artist}"

    @staticmethod
    def inline_description(song: Song) -> str:
        parts: list[str] = []

        if song.album:
            parts.append(song.album)

        if song.release_date:
            parts.append(song.release_date)

        return " • ".join(parts)

    @staticmethod
    def message(song: Song) -> str:
        lines: list[str] = [
            f"🎵 <b>{escape(song.title)}</b>",
            f"👤 {escape(song.artist)}",
        ]

        if song.album:
            lines.append(
                f"💿 {escape(song.album)}"
            )

        if song.release_date:
            lines.append(
                f"📅 {escape(song.release_date)}"
            )

        lines.extend(
            [
                "",
                f'🔗 <a href="{escape(song.url)}">Открыть страницу на Genius</a>',
            ]
        )

        return "\n".join(lines)

    @staticmethod
    def empty(query: str) -> str:
        return (
            "🔍 Ничего не найдено.\n\n"
            f"Запрос: <code>{escape(query)}</code>"
        )

    @staticmethod
    def error() -> str:
        return (
            "⚠️ Во время обращения к Genius "
            "произошла ошибка.\n"
            "Попробуйте повторить запрос позже."
        )


formatter = Formatter()