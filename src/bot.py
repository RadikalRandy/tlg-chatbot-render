# src/bot.py

import logging
import os
from typing import Tuple

from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.events import StopPropagation
from telethon.errors.rpcerrorlist import UnauthorizedError

from src.utils.handler_loader import autoload_handlers  # ✅ Dynamic handler registration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_keys() -> Tuple[int, str, str]:
    """Load API keys from environment variables."""
    load_dotenv()
    return (
        int(os.getenv("API_ID", "0")),
        os.getenv("API_HASH", ""),
        os.getenv("BOTTOKEN", "")
    )

async def bot() -> None:
    """Start and run the Telegram bot."""
    api_id, api_hash, bot_token = load_keys()

    if not bot_token:
        logging.error("❌ Bot token is missing — check your .env file.")
        return

    client = TelegramClient("bot_session", api_id, api_hash)

    try:
        await client.start(bot_token=bot_token)
        logging.info("✅ Telegram client started successfully.")
    except UnauthorizedError:
        logging.error("❌ Unauthorized — check API credentials.")
        return
    except Exception as e:
        logging.exception("❌ Unexpected error during startup.")
        return

    # 📩 Handle /start in private chat only
    @client.on(events.NewMessage(incoming=True, pattern=r"(?i)^/start$"))
    async def start_handler(event):
        if event.is_private:
            await event.respond("Hello Randy! Your bot is up and running. 🤖")
            raise StopPropagation

    # 🧠 Auto-register all handlers in src/handlers
    autoload_handlers(client)

    logging.info("🤖 Bot is now listening for Telegram events.")
    await client.run_until_disconnected()
