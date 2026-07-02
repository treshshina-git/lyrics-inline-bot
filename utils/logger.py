"""
Project logging configuration.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
import sys

from config import LOG_FILE, LOG_LEVEL


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _create_console_handler() -> logging.Handler:
    """
    Console logger.
    """

    handler = logging.StreamHandler(sys.stdout)

    handler.setFormatter(
        logging.Formatter(
            fmt=LOG_FORMAT,
            datefmt=DATE_FORMAT,
        )
    )

    return handler


def _create_file_handler() -> logging.Handler:
    """
    Rotating log file.
    """

    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    handler.setFormatter(
        logging.Formatter(
            fmt=LOG_FORMAT,
            datefmt=DATE_FORMAT,
        )
    )

    return handler


def setup_logging() -> None:
    """
    Configure root logger.
    """

    root = logging.getLogger()

    if root.handlers:
        return

    root.setLevel(LOG_LEVEL)

    root.addHandler(_create_console_handler())
    root.addHandler(_create_file_handler())


def get_logger(name: str) -> logging.Logger:
    """
    Return project logger.
    """

    return logging.getLogger(name)