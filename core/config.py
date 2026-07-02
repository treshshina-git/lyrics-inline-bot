from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)

    if value is None:
        raise RuntimeError(f"Environment variable '{name}' is not set.")

    return value


@dataclass(slots=True, frozen=True)
class TelegramSettings:
    token: str = _env("TELEGRAM_TOKEN")
    inline_results_per_page: int = int(
        os.getenv("INLINE_RESULTS_PER_PAGE", "6")
    )


@dataclass(slots=True, frozen=True)
class GeniusSettings:
    token: str = _env("GENIUS_TOKEN")
    search_limit: int = min(
        int(os.getenv("GENIUS_SEARCH_LIMIT", "24")),
        24,
    )
    timeout: int = int(os.getenv("GENIUS_TIMEOUT", "15"))
    retries: int = int(os.getenv("GENIUS_RETRIES", "3"))
    retry_delay: int = int(
        os.getenv("GENIUS_RETRY_DELAY", "2")
    )


@dataclass(slots=True, frozen=True)
class CacheSettings:
    ttl: int = int(os.getenv("CACHE_TTL", "3600"))
    size: int = int(os.getenv("CACHE_SIZE", "1024"))


@dataclass(slots=True, frozen=True)
class LoggingSettings:
    level: str = os.getenv("LOG_LEVEL", "INFO").upper()


@dataclass(slots=True, frozen=True)
class Settings:
    telegram: TelegramSettings = TelegramSettings()
    genius: GeniusSettings = GeniusSettings()
    cache: CacheSettings = CacheSettings()
    logging: LoggingSettings = LoggingSettings()


settings = Settings()