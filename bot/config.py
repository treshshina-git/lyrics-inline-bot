from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True, slots=True)
class Settings:
    bot_token: str
    genius_access_token: str


def _get_env(name: str) -> str:
    value = os.getenv(name)

    if value is None or not value.strip():
        raise RuntimeError(
            f"Environment variable '{name}' is not set."
        )

    return value.strip()


settings = Settings(
    bot_token=_get_env("BOT_TOKEN"),
    genius_access_token=_get_env("GENIUS_ACCESS_TOKEN"),
)