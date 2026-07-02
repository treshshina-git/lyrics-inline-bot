from __future__ import annotations

from math import ceil
from typing import Sequence

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from models.song import Song


class SongPaginator:
    ROWS = 3
    COLS = 2
    PAGE_SIZE = ROWS * COLS

    def __init__(self, songs: Sequence[Song]) -> None:
        self._songs = list(songs)

    @property
    def total(self) -> int:
        return len(self._songs)

    @property
    def pages(self) -> int:
        if not self._songs:
            return 1

        return ceil(len(self._songs) / self.PAGE_SIZE)

    def page(self, index: int) -> list[Song]:
        if index < 0:
            index = 0

        if index >= self.pages:
            index = self.pages - 1

        start = index * self.PAGE_SIZE
        end = start + self.PAGE_SIZE

        return self._songs[start:end]

    def keyboard(
        self,
        page: int,
        query: str,
    ) -> InlineKeyboardMarkup:
        page_songs = self.page(page)

        keyboard: list[list[InlineKeyboardButton]] = []

        for i in range(0, len(page_songs), self.COLS):
            row: list[InlineKeyboardButton] = []

            for song in page_songs[i : i + self.COLS]:
                row.append(
                    InlineKeyboardButton(
                        text=f"{song.title} — {song.artist}",
                        callback_data=song.to_callback_data(),
                    )
                )

            keyboard.append(row)

        navigation: list[InlineKeyboardButton] = []

        if page > 0:
            navigation.append(
                InlineKeyboardButton(
                    "⬅️",
                    callback_data=f"page:{page-1}:{query}",
                )
            )

        navigation.append(
            InlineKeyboardButton(
                f"{page + 1}/{self.pages}",
                callback_data="noop",
            )
        )

        if page < self.pages - 1:
            navigation.append(
                InlineKeyboardButton(
                    "➡️",
                    callback_data=f"page:{page+1}:{query}",
                )
            )

        if navigation:
            keyboard.append(navigation)

        return InlineKeyboardMarkup(keyboard)