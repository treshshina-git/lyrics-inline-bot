from __future__ import annotations

import signal

from bot.app import create_application


def main() -> None:
    application = create_application()

    stop_signals = (signal.SIGINT, signal.SIGTERM)

    for sig in stop_signals:
        signal.signal(sig, lambda *_: application.stop())

    application.run_polling(
        allowed_updates=["inline_query", "message"],
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()