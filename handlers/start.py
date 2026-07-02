from __future__ import annotations

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from core.logger import get_logger

logger = get_logger(__name__)


START_TEXT = """
🎵 <b>Genius Inline Bot</b>

Использование:

<code>@{bot_username} название песни</code>

Примеры:

<code>@{bot_username} Yesterday</code>

<code>@{bot_username} Queen Bohemian Rhapsody</code>

Что умеет бот:

• поиск песен через Genius;
• показывает название;
• показывает исполнителя;
• показывает альбом (если есть);
• показывает дату релиза (если есть);
• открывает страницу песни на Genius.

Бот работает полностью через Inline Mode.
"""


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.effective_message is None:
        return

    bot = await context.bot.get_me()

    await update.effective_message.reply_html(
        START_TEXT.format(
            bot_username=bot.username,
        ),
        disable_web_page_preview=True,
    )

    logger.info(
        "/start from %s",
        update.effective_user.id if update.effective_user else "unknown",
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    await start(update, context)