from telethon import events
from telethon.events import StopPropagation
import logging

async def gpt_handler(event):
    # Only private, non-slash messages
    text = (event.raw_text or "").strip()
    if event.is_private and text and not text.startswith("/"):
        # Insert your GPT call here; placeholder reply below
        reply = f"🤖 You said: {text}"
        await event.respond(reply)
        logging.info(f"Replied to user {event.sender_id} with GPT placeholder.")
        raise StopPropagation

def register(client):
    """
    Called by autoload_handlers().
    Attaches this handler to any incoming private non-slash messages.
    """
    client.add_event_handler(
        gpt_handler,
        events.NewMessage(
            incoming=True,
            func=lambda e: e.is_private and (e.raw_text or "").strip() and not e.raw_text.startswith("/")
        )
    )
