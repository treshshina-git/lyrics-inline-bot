from __future__ import annotations

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from core.logger import get_logger
from services.cache import cache
from services.formatter import formatter
from services.genius import genius
from services.paginator import SongPaginator

logger = get_logger(__name__)


async def callback_query_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if query is None:
        return

    await query.answer()

    data = query.data or ""

    if data == "noop":
        return

    if data.startswith("page:"):
        try:
            _, page, search_query = data.split(":", 2)

            page = int(page)

        except Exception:
            return

        songs = cache.search.get(search_query)

        if songs is None:
            await query.edit_message_text(
                "⚠️ Результаты поиска устарели.\n"
                "Выполните поиск ещё раз."
            )
            return

        paginator = SongPaginator(songs)

        await query.edit_message_reply_markup(
            reply_markup=paginator.keyboard(
                page=page,
                query=search_query,
            )
        )

        return

    if not data.startswith("song:"):
        return

    try:
        song_id = int(data.split(":")[1])

    except Exception:
        return

    song = cache.songs.get(song_id)

    if song is None:
        song = await genius.get_song(song_id)

    if song is None:
        await query.edit_message_text(
            "⚠️ Песня больше недоступна."
        )
        return

    await query.edit_message_text(
        formatter.message(song),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=False,
    )

    logger.info(
        "Selected song %s by %s",
        song.title,
        song.artist,
    )