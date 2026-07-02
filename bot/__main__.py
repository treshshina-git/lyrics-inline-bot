from __future__ import annotations

import signal

from bot.app import create_application
from bot.utils.requirements_check import check_python_version


def main() -> None:
    check_python_version()

    application = create_application()

    def _shutdown(*_) -> None:
        application.stop()

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    application.run_polling(
        allowed_updates=["inline_query", "message"],
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()