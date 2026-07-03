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
from bot.services.cache import cache


async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = (update.inline_query.query or "").strip()

    if not query:
        await update.inline_query.answer(results=[], cache_time=1)
        return

    songs = await genius_api.search(query)

    # Надёжная схема: inline отдаёт метаданные.
    # После выбора Telegram вызывает chosen_inline_result_handler,
    # который уже запрашивает lyrics через bot/services/lrclib.py:get_lyrics().
    results: list[InlineQueryResultArticle] = []

    for song in songs:
        cache.set(str(song.id), {"artist": song.artist, "title": song.title})

        # Вставляем inline-клавиатуру, чтобы после выбора можно было нажать кнопку
        # и обработчик перешёл в callback_handler (data: songlyrics:{id}).
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


