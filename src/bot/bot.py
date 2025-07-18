import logging
import os
from typing import Tuple

import google.generativeai as genai
import openai
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.events import StopPropagation
from telethon.errors.rpcerrorlist import UnauthorizedError

from src.handlers import (
    bard_chat_handler,
    bash_handler,
    bing_chat_handler,
    clear_handler,
    gemini_chat_handler,
    group_chat_handler,
    search_handler,
    security_check,
    senpai_chat_handler,
    switch_model_handler,
    user_chat_handler,
)

# 🛠 Logging configuration
logging.basicConfig(level=logging.INFO)

# 🔐 Load API keys and tokens
def load_keys() -> Tuple[int, str, str]:
    load_dotenv()

    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.organization = os.getenv("OPENAI_ORG")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    try:
        api_id = int(os.getenv("API_ID"))
        api_hash = os.getenv("API_HASH")
        bot_token = os.getenv("BOTTOKEN")
    except Exception:
        logging.error(
            "❌ Environment variable loading failed. Double-check your .env or Render settings."
        )
        raise

    return api_id, api_hash, bot_token

# 🚀 Start and run the bot
async def bot() -> None:
    api_id, api_hash, bot_token = load_keys()

    if not bot_token:
        logging.error(
            "❌ Bot token is missing. Please check your Render environment variables."
        )
        return

    try:
        client = TelegramClient("bot_session", api_id, api_hash)
        await client.start(bot_token=bot_token)
        logging.info("✅ Bot started and authenticated successfully.")
    except UnauthorizedError:
        logging.error(
            "❌ Unauthorized. Check if your API ID, API Hash, and bot token are correct."
        )
        return
    except Exception:
        logging.exception("❌ Unhandled exception during bot startup")
        return

    # 💬 Respond to /start with "Hello Randy!" and stop further handlers
    @client.on(events.NewMessage(pattern=r"(?i)^/start$", incoming=True))
    async def start_handler(event):
        await event.respond("Hello Randy!")
        raise StopPropagation

    # 💬 Register security_check only for non-command group messages
    from telethon import events as _events

    client.add_event_handler(
        security_check,
        _events.NewMessage(
            incoming=True,
            func=lambda e: not (e.is_private or (e.raw_text or "").startswith("/")),
        ),
    )

    # 💬 Register all other handlers normally
    client.add_event_handler(search_handler)
    client.add_event_handler(bash_handler)
    client.add_event_handler(clear_handler)
    client.add_event_handler(switch_model_handler)
    client.add_event_handler(bard_chat_handler)
    client.add_event_handler(bing_chat_handler)
    client.add_event_handler(gemini_chat_handler)
    client.add_event_handler(senpai_chat_handler)
    client.add_event_handler(group_chat_handler)
    client.add_event_handler(user_chat_handler)

    logging.info("🤖 Bot is now listening for events.")
    await client.run_until_disconnected()
