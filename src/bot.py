import logging
import os
from typing import Tuple

from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.events import StopPropagation
from telethon.errors.rpcerrorlist import UnauthorizedError

from src.utils.handler_loader import autoload_handlers  # dynamic handler registration

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def load_keys() -> Tuple[int, str, str]:
    load_dotenv()
    return (
        int(os.getenv("API_ID", "0")),
        os.getenv("API_HASH", ""),
        os.getenv("BOTTOKEN", ""),
    )

async def bot() -> None:
    api_id, api_hash, bot_token = load_keys()
    if not bot_token:
        logging.error("❌ Bot token missing. Check your .env.")
        return

    client = TelegramClient("bot_session", api_id, api_hash)

    try:
        await client.start(bot_token=bot_token)
        logging.info("✅ Telegram client started.")
    except UnauthorizedError:
        logging.error("❌ Unauthorized: invalid credentials.")
        return
    except Exception:
        logging.exception("❌ Unexpected startup error.")
        return

    # Handle /start only once per private chat
    @client.on(events.NewMessage(incoming=True, pattern=r"(?i)^/start$"))
    async def start_handler(event):
        if event.is_private:
            await event.respond("Hello Randy! Your bot is up and running. 🤖")
            raise StopPropagation

    # Auto-register all handlers under src/handlers/
    autoload_handlers(client)

    logging.info("🤖 Bot is now listening for Telegram events.")
    await client.run_until_disconnected()

# ensure the name matches main.py's import
__all__ = ["bot"]
