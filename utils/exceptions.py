from __future__ import annotations


class BotError(Exception):
    """Base exception for bot-related errors."""


class GeniusAPIError(BotError):
    """Raised when Genius API request fails."""


class InvalidQueryError(BotError):
    """Raised when user query is invalid."""