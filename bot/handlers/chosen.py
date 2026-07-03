from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from core.logger import get_logger

from bot.services.cache import TTLCache
from bot.services.lrclib import get_lyrics


logger = get_logger(__name__)

cache = TTLCache[dict](ttl=600)


async def chosen_inline_result_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Called when the user selects one of the inline results.

    Can be extended later for analytics,
    statistics or caching.
    """
    print("chosen_inline_result_handler: called")
    result = update.chosen_inline_result

    if result is None:
        return

    logger.info(
        "Chosen inline result | user=%s | query='%s' | result_id=%s",
        result.from_user.id,
        result.query,
        result.result_id,
    )

    song_key = str(result.result_id)

    cached = cache.get(song_key)

    if not cached:
        # As fallback - try to answer with a short message (lyrics will be fetched only if we know artist/title)
        return

    artist = cached.get("artist")
    title = cached.get("title")

    if not artist or not title:
        return

    lyrics = await get_lyrics(artist=artist, title=title)

    if lyrics is None:
        lyrics_text = "⚠️ Не удалось найти текст песни."  # plain text
    else:
        lyrics_text = lyrics

    # Send lyrics to the inline message recipient (user) by answering chosen inline result.
    # In python-telegram-bot, chosen_inline_result is not a message update, so we send a normal message.
    try:
        await context.bot.send_message(
            chat_id=result.from_user.id,
            text=lyrics_text,
            disable_web_page_preview=True,
        )
    except Exception:
        # avoid crashing chosen handler
        return
