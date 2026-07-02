from __future__ import annotations

import sys


def check_python_version() -> None:
    """
    Ensure Python 3.12+ is used.
    """
    if sys.version_info < (3, 12):
        raise RuntimeError(
            f"Python 3.12+ required, got {sys.version}"
        )