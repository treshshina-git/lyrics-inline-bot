from __future__ import annotations

import logging

from telegram.ext import (
    Application,
    CommandHandler,
    InlineQueryHandler,
)

from bot.config import settings
from bot.handlers.inline import inline_query_handler
from bot.handlers.start import start_handler
from bot.handlers.help import help_handler
from bot.handlers.health import health_handler
from bot.handlers.version import version_handler
from bot.handlers.error import error_handler
from bot.utils.logging import setup_logging


logger = logging.getLogger(__name__)


def create_application() -> Application:
    application = (
        Application.builder()
        .token(settings.bot_token)
        .build()
    )

    # commands
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("health", health_handler))
    application.add_handler(CommandHandler("version", version_handler))

    # inline
    application.add_handler(InlineQueryHandler(inline_query_handler))

    # errors
    application.add_error_handler(error_handler)

    return application


def main() -> None:
    setup_logging()

    logger.info("Starting Telegram Inline Lyrics Bot...")

    application = create_application()

    application.run_polling(
        allowed_updates=["inline_query", "message"],
        drop_pending_updates=True,
    )