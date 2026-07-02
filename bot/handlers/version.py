from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.utils.version import get_version


async def version_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.effective_message is None:
        return

    await update.effective_message.reply_text(
        f"📦 Bot version: {get_version()}"
    )