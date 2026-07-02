"""
Handlers layer.
"""

from bot.handlers.error import error_handler
from bot.handlers.help import help_handler
from bot.handlers.health import health_handler
from bot.handlers.inline import inline_query_handler
from bot.handlers.start import start_handler
from bot.handlers.version import version_handler

__all__ = [
    "inline_query_handler",
    "start_handler",
    "help_handler",
    "health_handler",
    "version_handler",
    "error_handler",
]