from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from core.logger import get_logger

logger = get_logger(__name__)


async def chosen_inline_result_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """
    Called when the user selects one of the inline results.

    Can be extended later for analytics,
    statistics or caching.
    """

    result = update.chosen_inline_result

    if result is None:
        return

    logger.info(
        "Chosen inline result | user=%s | query='%s' | result_id=%s",
        result.from_user.id,
        result.query,
        result.result_id,
    )