import logging
from telethon import events

async def security_check(event: events.NewMessage.Event):
    """
    Fires only for non-command messages in group chats,
    because bot.py registers it with a filter.
    """
    logging.info(f"Blocked in group {event.chat_id}: {event.raw_text!r}")
    await event.respond("🚫 This is personal property, you are not allowed to proceed!")
