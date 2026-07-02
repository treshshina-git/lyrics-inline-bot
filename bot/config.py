from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True, slots=True)
class Settings:
    bot_token: str
    genius_access_token: str
    webhook_url: str
    port: int


def _get(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing env: {name}")
    return v


settings = Settings(
    bot_token=_get("BOT_TOKEN"),
    genius_access_token=_get("GENIUS_ACCESS_TOKEN"),
    webhook_url=_get("WEBHOOK_URL"),
    port=int(os.getenv("PORT", "8080")),
)