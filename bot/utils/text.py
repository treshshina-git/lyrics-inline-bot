from __future__ import annotations


MAX_TITLE_LENGTH = 256
MAX_DESCRIPTION_LENGTH = 256


def truncate(text: str, limit: int) -> str:
    """
    Truncate text to the specified length.

    If truncation is required, the resulting string ends with "...".
    """

    text = text.strip()

    if len(text) <= limit:
        return text

    if limit <= 3:
        return text[:limit]

    return text[: limit - 3].rstrip() + "..."


def safe_title(title: str) -> str:
    return truncate(title, MAX_TITLE_LENGTH)


def safe_description(description: str) -> str:
    return truncate(description, MAX_DESCRIPTION_LENGTH)