from __future__ import annotations

from telegram import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes

from bot.services.genius import genius_api
from bot.services.cache import TTLCache


# NOTE: this cache is in-memory. If you deploy multiple instances, inline chosen may not find data.
cache = TTLCache[dict](ttl=600)


async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = (update.inline_query.query or "").strip()

    if not query:
        await update.inline_query.answer(results=[], cache_time=1)
        return

    songs = await genius_api.search(query)

    # IMPORTANT:
    # inline -> user chooses a result -> Telegram sends message immediately from input_message_content.
    # Поэтому lyrics нужно вставить прямо в input_message_content, без callback.
    results: list[InlineQueryResultArticle] = []

    for song in songs:
        lyrics_text = None
        try:
            from bot.services.lrclib import get_lyrics

            lyrics_text = await get_lyrics(artist=song.artist, title=song.title)
        except Exception:
            lyrics_text = None

        if not lyrics_text:
            lyrics_text = "⚠️ Не удалось найти текст песни."

        # Можно дополнительно сохранить meta, но уже не обязательно.
        cache.set(
            str(song.id),
            {"artist": song.artist, "title": song.title},
        )

        results.append(
            InlineQueryResultArticle(
                id=str(song.id),
                title=song.title,
                description=song.artist,
                input_message_content=InputTextMessageContent(
                    f"🎵 {song.title} — {song.artist}\n\n{lyrics_text}"
                ),
            )
        )

    await update.inline_query.answer(
        results=results,
        cache_time=30,
        is_personal=True,
    )


