from __future__ import annotations

import json
from uuid import uuid4

from telegram import (
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from core.logger import get_logger
from services.formatter import formatter
from services.genius import genius

logger = get_logger(__name__)


async def inline_query_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.inline_query is None:
        return

    query = update.inline_query.query.strip()

    if not query:
        await update.inline_query.answer(
            [],
            cache_time=1,
            is_personal=True,
        )
        return

    try:
        songs = await genius.search(query)

    except Exception:
        logger.exception("Inline search failed")

        await update.inline_query.answer(
            [],
            cache_time=1,
            is_personal=True,
            switch_pm_text="Ошибка поиска",
            switch_pm_parameter="error",
        )
        return

    results: list[InlineQueryResultArticle] = []

    for song in songs:
        description = formatter.inline_description(song)

        message = formatter.message(song)

        results.append(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=formatter.inline_title(song),
                description=description,
                input_message_content=InputTextMessageContent(
                    message_text=message,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=False,
                ),
                reply_markup=InlineKeyboardMarkup([]),
            )
        ) 
    try:
        await update.inline_query.answer(
            results=results,
            cache_time=60,
            is_personal=True,
            button=None,
        )

        logger.info(
            "Inline query '%s' -> %d result(s)",
            query,
            len(results),
        )

    except Exception:
        logger.exception(
            "Failed to answer inline query."
        )