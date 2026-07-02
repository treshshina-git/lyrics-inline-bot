from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes


async def health_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        await update.effective_message.reply_text("ok")