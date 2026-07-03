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
from bot.handlers.callback import callback_handler
from telegram.ext import CallbackQueryHandler

logger = logging.getLogger(__name__)


def create_application() -> Application:
    app = Application.builder().token(settings.bot_token).build()
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("health", health_handler))
    app.add_handler(CommandHandler("version", version_handler))
    app.add_handler(InlineQueryHandler(inline_query_handler))

    app.add_error_handler(error_handler)

    return app


def main() -> None:
    setup_logging()

    app = create_application()

    logger.info("Starting webhook bot...")

    app.run_webhook(
        listen="0.0.0.0",
        port=settings.port,
        url_path=settings.bot_token,
        webhook_url=f"{settings.webhook_url}/{settings.bot_token}",
        drop_pending_updates=True,
    )