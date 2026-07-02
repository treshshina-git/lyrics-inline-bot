from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from typing import Any


def serialize(obj: Any) -> str:
    """
    Serialize dataclass or dict-like objects to JSON string.
    """

    if is_dataclass(obj):
        obj = asdict(obj)

    return json.dumps(obj, ensure_ascii=False, default=str)


def deserialize(data: str) -> dict:
    """
    Deserialize JSON string into dict.
    """

    return json.loads(data)