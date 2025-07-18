import logging
import os
from typing import Tuple

import google.generativeai as genai
import openai
from dotenv import load_dotenv
from telethon import TelegramClient
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

# Load keys from environment
def load_keys() -> Tuple[int, str, str]:
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.organization = os.getenv("OPENAI_ORG")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    api_id = int(os.getenv("API_ID"))
    api_hash = os.getenv("API_HASH")
    bot_token = os.getenv("BOTTOKEN")
    
    return api_id, api_hash, bot_token

# Start and run the bot
async def bot() -> None:
    api_id, api_hash, bot_token = load_keys()

    try:
        client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)
        logging.info("✅ Bot started successfully.")
    except UnauthorizedError:
        logging.error("❌ Unauthorized access. Check your Telethon API ID and Hash.")
        raise
    except Exception as e:
        logging.error(f"❌ Unexpected error during bot startup: {e}")
        raise

    # Add event handlers
    client.add_event_handler(security_check)
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

    logging.info("🤖 Bot is now running and listening for events.")
    await client.run_until_disconnected()
