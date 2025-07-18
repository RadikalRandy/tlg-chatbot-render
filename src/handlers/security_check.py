# src/handlers/security_check.py

import logging
from telethon import events

async def security_check(event: events.NewMessage.Event):
    """
    Blocks non-command messages in group chats only.
    Skips:
      - Any message in a private (1:1) chat (chat_id > 0)
      - Any message that starts with '/'
    """

    chat_id = event.chat_id

    # 1) Private chats have positive IDs
    if chat_id and chat_id > 0:
        return

    # 2) Skip commands everywhere
    text = event.raw_text or ""
    if text.startswith("/"):
        return

    # 3) Otherwise it’s a non-command in a group → block it
    logging.info(f"Blocked message in group {chat_id}: {text!r}")
    await event.respond("🚫 This is personal property, you are not allowed to proceed!")
