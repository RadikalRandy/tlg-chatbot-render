import logging
import os
from typing import Tuple

from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.events import StopPropagation
from telethon.errors.rpcerrorlist import UnauthorizedError

# Autoloader for handlers
from src.utils.handler_loader import autoload_handlers  # 👈 you'll create this file

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_keys() -> Tuple[int, str, str]:
    load_dotenv()
    api_id = int(os.getenv("API_ID", "0"))
    api_hash = os.getenv("API_HASH", "")
    bot_token = os.getenv("BOTTOKEN", "")
    return api_id, api_hash, bot_token

async def start_bot() -> None:
    api_id, api_hash, bot_token = load_keys()
    if not bot_token:
        logging.error("❌ Bot token missing. Check .env file.")
        return

    client = TelegramClient("bot_session", api_id, api_hash)

    try:
        await client.start(bot_token=bot_token)
        logging.info("✅ Telegram client started.")
    except UnauthorizedError:
        logging.error("❌ Unauthorized. Check credentials.")
        return
    except Exception:
        logging.exception("❌ Startup error.")
        return

    @client.on(events.NewMessage(incoming=True, pattern=r"(?i)^/start$"))
    async def start_handler(event):
        if event.is_private:
            await event.respond("Hello Randy! Your bot is up and running. 🤖")
            raise StopPropagation

    # 🔗 Autoload all handlers from src/handlers/
    autoload_handlers(client)

    logging.info("🤖 Bot is listening.")
    await client.run_until_disconnected()
