# src/handlers/security_check.py

import logging
from telethon import events

async def security_check(event: events.NewMessage.Event):
    """
    Blocks non-command messages in group chats only.
    Skips:
      - Any message in a private (1:1) chat
      - Any message that starts with '/'
    """

    # 1) If this is a private chat, allow it
    if event.is_private:
        return

    # 2) If it’s a command, allow it
    text = event.raw_text or ""
    if text.startswith("/"):
        return

    # 3) Otherwise, we’re in a group and it’s not a command → block it
    logging.info(f"Blocked message in group {event.chat_id}: {text!r}")
    await event.respond("🚫 This is personal property, you are not allowed to proceed!")
