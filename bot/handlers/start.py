from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes


async def start_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.effective_message is None:
        return

    bot_username = (context.bot.username or "this bot")

    await update.effective_message.reply_text(
        (
            "🎵 Inline Lyrics Bot\n\n"
            "Использование:\n\n"
            f"1. В любом чате напишите:\n"
            f"   @{bot_username} название песни\n\n"
            "2. Выберите результат из списка\n\n"
            "Бот ищет треки через Genius API и показывает метаданные."
        )
    )