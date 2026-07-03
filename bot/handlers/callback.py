from __future__ import annotations

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from bot.services.genius import genius_api
from bot.services.cache import TTLCache

cache = TTLCache[dict](ttl=600)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if not query.data:
        return

    if query.data.startswith("song:"):
        song_id = int(query.data.split(":")[1])

        cached = cache.get(str(song_id))
        if cached:
            song = cached
        else:
            song = await genius_api.get_song(song_id)
            if not song:
                await query.edit_message_text("❌ Song not found")
                return
            cache.set(str(song_id), song)

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔁 Refresh",
                        callback_data=f"song:{song_id}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔗 Open on Genius",
                        url=song.url
                    )
                ]
            ]
        )

        text = (
            f"🎵 <b>{song.title}</b>\n"
            f"👤 {song.artist}\n"
        )

        if song.album:
            text += f"💽 {song.album}\n"

        if song.release_date:
            text += f"📅 {song.release_date}\n"

        text += f"\n🔗 {song.url}"

        await query.edit_message_text(
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard,
            disable_web_page_preview=False,
        )