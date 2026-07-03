from __future__ import annotations

import logging

from telegram import InlineQueryResultArticle
from telegram import InputTextMessageContent
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.services.genius import genius_api
from bot.services.cache import TTLCache
from bot.services.rate_limiter import inline_rate_limiter
from bot.utils.validators import is_valid_query
from bot.utils.formatters import format_song_inline

logger = logging.getLogger(__name__)

cache: TTLCache = TTLCache(ttl=300)


async def inline_query_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = (update.inline_query.query or "").strip()

    if not is_valid_query(query):
        await update.inline_query.answer(results=[], cache_time=1)
        return

    user_id = str(update.effective_user.id) if update.effective_user else "anon"

    if not inline_rate_limiter.allow(user_id):
        await update.inline_query.answer(results=[], cache_time=1)
        return

    cache_key = query.lower()

    cached = cache.get(cache_key)
    if cached:
        songs = cached
    else:
        songs = await genius_api.search(query)
        cache.set(cache_key, songs)

    results: list[InlineQueryResultArticle] = []

    for song in songs:
        
        message = await format_song_inline(song)
        print(f"inline_query_handler: {song.title} - {song.artist} -> {message}")  

        results.append(
            InlineQueryResultArticle(
                id=str(song.id),
                title=song.title,
                description=song.artist,
                input_message_content=InputTextMessageContent(
                    message_text=message,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                ),
            )
        )

    await update.inline_query.answer(
        results=results,
        cache_time=30,
        is_personal=True,
    )