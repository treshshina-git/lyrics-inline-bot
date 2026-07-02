from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    logger.exception("Unhandled error occurred", exc_info=context.error)

    if isinstance(update, Update):
        message = update.effective_message

        if message:
            try:
                await message.reply_text(
                    "⚠️ Произошла ошибка. Попробуйте позже."
                )
            except Exception:
                # avoid secondary crash
                pass