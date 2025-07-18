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
from src.handlers.gpt_handler import gpt_handler  # our new GPT handler

# 🛠 Logging configuration
logging.basicConfig(level=logging.INFO)


def load_keys() -> Tuple[int, str, str]:
    """
    Load API keys and tokens from environment (.env or Render settings).
    """
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.organization = os.getenv("OPENAI_ORG")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    api_id = int(os.getenv("API_ID", "0"))
    api_hash = os.getenv("API_HASH", "")
    bot_token = os.getenv("BOTTOKEN", "")
    return api_id, api_hash, bot_token


async def bot() -> None:
    api_id, api_hash, bot_token = load_keys()
    if not bot_token:
        logging.error("❌ Bot token is missing. Check your environment variables.")
        return

    try:
        client = TelegramClient("bot_session", api_id, api_hash)
        await client.start(bot_token=bot_token)
        logging.info("✅ Bot started and authenticated successfully.")
    except UnauthorizedError:
        logging.error("❌ Unauthorized. Check API_ID, API_HASH & BOTTOKEN.")
        return
    except Exception:
        logging.exception("❌ Unhandled exception during bot startup")
        return

    # 1️⃣ Handle /start in private chats, respond and stop propagation
    @client.on(events.NewMessage(pattern=r"(?i)^/start$", incoming=True))
    async def start_handler(event):
        await event.respond("Hello Randy!")
        raise StopPropagation

    # 2️⃣ Security check: only for non-command messages in group chats
    client.add_event_handler(
        security_check,
        events.NewMessage(
            incoming=True,
            func=lambda e: (e.chat_id or 0) < 0 and not (e.raw_text or "").startswith("/"),
        ),
    )

    # 3️⃣ GPT handler: all non-command messages (private or group commands passed)
    client.add_event_handler(
        gpt_handler,
        events.NewMessage(
            incoming=True,
            func=lambda e: not (e.raw_text or "").startswith("/")
        ),
    )

    # 4️⃣ Other specialized handlers
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
