from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes


def get_user_id(update: Update) -> int | None:
    if update.effective_user:
        return update.effective_user.id
    return None


def get_chat_id(update: Update) -> int | None:
    if update.effective_chat:
        return update.effective_chat.id
    return None


def get_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    if update.inline_query:
        return (update.inline_query.query or "").strip()

    if update.effective_message and context.args:
        return " ".join(context.args).strip()

    return ""