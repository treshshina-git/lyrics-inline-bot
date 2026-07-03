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


async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = (update.inline_query.query or "").strip()

    if not query:
        await update.inline_query.answer(results=[], cache_time=1)
        return

    songs = await genius_api.search(query)

    results = []

    for song in songs:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🎵 Details",
                        callback_data=f"song:{song.id}"
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