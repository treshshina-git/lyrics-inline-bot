from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes


async def help_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.effective_message is None:
        return

    bot_username = context.bot.username or "bot"

    await update.effective_message.reply_text(
        (
            "🎵 Inline Lyrics Bot Help\n\n"
            "Как использовать:\n\n"
            f"1. В любом чате напиши:\n"
            f"   @{bot_username} название песни\n\n"
            "2. Выбери подходящий трек из списка\n\n"
            "Функции:\n"
            "- Поиск через Genius API\n"
            "- Только метаданные (без текста песен)\n"
            "- Inline режим\n"
        )
    )