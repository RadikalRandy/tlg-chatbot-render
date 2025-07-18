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
    search_handler,
    bash_handler,
    clear_handler,
    switch_model_handler,
    bard_chat_handler,
    bing_chat_handler,
    gemini_chat_handler,
    senpai_chat_handler,
    group_chat_handler,
    user_chat_handler,
    security_check,
)
from src.handlers.gpt_handler import gpt_handler  # your GPT integration

# Configure root logger
logging.basicConfig(level=logging.INFO)

def load_keys() -> Tuple[int, str, str]:
    """
    Load API credentials from environment variables or .env file.
    """
    load_dotenv()

    openai.api_key = os.getenv("OPENAI_API_KEY", "")
    openai.organization = os.getenv("OPENAI_ORG", "")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY", ""))

    api_id = int(os.getenv("API_ID", "0"))
    api_hash = os.getenv("API_HASH", "")
    bot_token = os.getenv("BOTTOKEN", "")
    return api_id, api_hash, bot_token

async def bot() -> None:
    """
    Initializes and runs the Telegram client with all handlers:
    - /start command
    - security_check for group non-commands
    - GPT handler for AI replies
    - other custom handlers
    """
    api_id, api_hash, bot_token = load_keys()
    if not bot_token:
        logging.error("❌ Bot token is missing. Check your environment variables.")
        return

    client = TelegramClient("bot_session", api_id, api_hash)
    try:
        await client.start(bot_token=bot_token)
        logging.info("✅ Telegram client started and authenticated successfully.")
    except UnauthorizedError:
        logging.error("❌ Unauthorized. Verify API_ID, API_HASH, and BOTTOKEN.")
        return
    except Exception:
        logging.exception("❌ Unexpected error during client startup")
        return

    # 1️⃣ /start handler (private chats)
    @client.on(events.NewMessage(pattern=r"(?i)^/start$", incoming=True))
    async def start_handler(event):
        await event.respond("Hello Randy!")
        raise StopPropagation

    # 2️⃣ security_check (only non-commands in group chats)
    client.add_event_handler(
        security_check,
        events.NewMessage(
            incoming=True,
            func=lambda e: (e.chat_id or 0) < 0 and not (e.raw_text or "").startswith("/")
        ),
    )

    # 3️⃣ gpt_handler (all non-command messages)
    client.add_event_handler(
        gpt_handler,
        events.NewMessage(
            incoming=True,
            func=lambda e: not (e.raw_text or "").startswith("/")
        ),
    )

    # 4️⃣ Other custom handlers
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

    logging.info("🤖 Bot is now listening for Telegram events.")
    # Keep the bot running until manually stopped
    await client.run_until_disconnected()
