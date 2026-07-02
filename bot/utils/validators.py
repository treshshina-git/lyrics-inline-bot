from __future__ import annotations


def is_valid_query(query: str) -> bool:
    """
    Validate inline search query for Genius search.
    """

    if query is None:
        return False

    query = query.strip()

    if len(query) < 2:
        return False

    if len(query) > 100:
        return False

    # block pure symbols / spam
    if all(not c.isalnum() for c in query):
        return False

    return True