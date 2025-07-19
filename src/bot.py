import logging
import os
from typing import Tuple

import google.generativeai as genai
import openai
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.events import StopPropagation
from telethon.errors.rpcerrorlist import UnauthorizedError

# Handlers
from src.handlers.security_check import security_check
from src.handlers.gpt_handler import gpt_handler
from src.handlers.search_handler import search_handler
from src.handlers.bash_handler import bash_handler
from src.handlers.clear_handler import clear_handler
from src.handlers.switch_model_handler import switch_model_handler
from src.handlers.bard_chat_handler import bard_chat_handler
from src.handlers.bing_chat_handler import bing_chat_handler
from src.handlers.gemini_chat_handler import gemini_chat_handler
from src.handlers.senpai_chat_handler import senpai_chat_handler
from src.handlers.group_chat_handler import group_chat_handler

logging.basicConfig(level=logging.INFO)

def load_keys() -> Tuple[int, str, str]:
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY", "")
    openai.organization = os.getenv("OPENAI_ORG", "")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY", ""))
    return (
        int(os.getenv("API_ID", "0")),
        os.getenv("API_HASH", ""),
        os.getenv("BOTTOKEN", ""),
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

    # /start command
    @client.on(events.NewMessage(incoming=True, pattern=r"(?i)^/start$"))
    async def start_handler(event):
        if not event.is_private:
            return
        await event.respond("Hello Randy! Your bot is up and running. 🤖")
        raise StopPropagation

    # Group security check for non-commands
    client.add_event_handler(
        security_check,
        events.NewMessage(
            incoming=True,
            func=lambda e: e.chat_id < 0 and not (e.raw_text or "").startswith("/")
        ),
    )

    # GPT handler for private non-command messages
    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and not (e.raw_text or "").startswith("/")))
    async def _gpt(event):
        await gpt_handler(event)
        raise StopPropagation

    # Slash-command handlers
    client.add_event_handler(search_handler)
    client.add_event_handler(bash_handler)
    client.add_event_handler(clear_handler)
    client.add_event_handler(switch_model_handler)
    client.add_event_handler(bard_chat_handler)
    client.add_event_handler(bing_chat_handler)
    client.add_event_handler(gemini_chat_handler)
    client.add_event_handler(senpai_chat_handler)
    client.add_event_handler(group_chat_handler)

    logging.info("🤖 Bot listening for events.")
    await client.run_until_disconnected()
