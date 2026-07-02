from __future__ import annotations

import traceback

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from core.logger import get_logger

logger = get_logger(__name__)


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    logger.exception(
        "Unhandled exception",
        exc_info=context.error,
    )

    if isinstance(update, Update):
        target = (
            update.effective_message
            or update.callback_query.message
            if update.callback_query
            else None
        )

        if target is not None:
            try:
                await target.reply_text(
                    (
                        "⚠️ Произошла внутренняя ошибка.\n"
                        "Попробуйте выполнить запрос ещё раз."
                    ),
                    parse_mode=ParseMode.HTML,
                )
            except Exception:
                logger.exception(
                    "Failed to send error message."
                )

    tb = "".join(
        traceback.format_exception(
            None,
            context.error,
            context.error.__traceback__,
        )
    )

    logger.debug(tb)