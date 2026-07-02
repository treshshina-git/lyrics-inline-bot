from __future__ import annotations

import logging
from collections.abc import Callable, Awaitable

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def logging_middleware(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    next_handler: Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]],
) -> None:
    user = update.effective_user
    logger.info(
        "Update from user=%s (%s)",
        user.username if user else None,
        user.id if user else None,
    )

    await next_handler(update, context)