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

    results = []

    for song in songs:
        # store meta for later lyrics request in chosen handler
        cache.set(str(song.id), {"artist": song.artist, "title": song.title})

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📜 Lyrics",
                        callback_data=f"songlyrics:{song.id}",
                    )
                ]
            ]
        )

        results.append(
            InlineQueryResultArticle(
                id=str(song.id),
                title=song.title,
                description=song.artist,
                input_message_content=InputTextMessageContent(
                    f"🎵 {song.title} — {song.artist}"
                ),
                reply_markup=keyboard,
            )
        )

    await update.inline_query.answer(
        results=results,
        cache_time=30,
        is_personal=True,
    )


