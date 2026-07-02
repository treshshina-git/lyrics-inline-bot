from __future__ import annotations

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ChosenInlineResultHandler,
    CommandHandler,
    InlineQueryHandler,
)

from core.config import settings
from core.logger import get_logger, setup_logging
from handlers import (
    callback_query_handler,
    chosen_inline_result_handler,
    error_handler,
    help_command,
    inline_query_handler,
    start,
)

logger = get_logger(__name__)


def build_application() -> Application:
    application = (
        Application.builder()
        .token(settings.telegram.token)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(
        InlineQueryHandler(
            inline_query_handler
        )
    )

    application.add_handler(
        ChosenInlineResultHandler(
            chosen_inline_result_handler
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_query_handler
        )
    )

    application.add_error_handler(
        error_handler
    )

    return application


def main() -> None:
    setup_logging()

    logger.info("Bot is starting...")

    application = build_application()

    application.run_polling(
        allowed_updates=[
            "message",
            "inline_query",
            "chosen_inline_result",
            "callback_query",
        ],
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()