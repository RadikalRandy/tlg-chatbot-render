import logging
import os
from typing import Tuple
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.events import StopPropagation
from telethon.errors.rpcerrorlist import UnauthorizedError

# Handlers
from src.handlers.simple_chat_handler import simple_chat_handler
from src.handlers.clear_handler import clear_handler

logging.basicConfig(level=logging.INFO)

def load_keys() -> Tuple[int, str, str]:
    load_dotenv()
    return (
        int(os.getenv("API_ID", "0")),
        os.getenv("API_HASH", ""),
        os.getenv("BOTTOKEN", "")
    )

async def bot() -> None:
    api_id, api_hash, bot_token = load_keys()
    if not bot_token:
        logging.error("❌ Bot token missing.")
        return

    client = TelegramClient("bot_session", api_id, api_hash)
    try:
        await client.start(bot_token=bot_token)
        logging.info("✅ Telegram client started.")
    except UnauthorizedError:
        logging.error("❌ Unauthorized: check credentials.")
        return
    except Exception:
        logging.exception("❌ Client startup error.")
        return

    @client.on(events.NewMessage(incoming=True, pattern=r"(?i)^/start$"))
    async def start_handler(event):
        if not event.is_private:
            return
        await event.respond("Hello Randy! Your bot is up and running. 🤖")
        raise StopPropagation

    # Register all message handlers
    client.add_event_handler(simple_chat_handler)
    client.add_event_handler(clear_handler)

    logging.info("🤖 Bot is listening.")
    await client.run_until_disconnected()
