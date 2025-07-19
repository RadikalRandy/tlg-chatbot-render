# src/handlers/simple_chat_handler.py

from telethon import events
from datetime import datetime

# This function handles simple private messages from users
@events.register(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def simple_chat_handler(event):
    message = event.raw_text.strip().lower()

    if "hello randy" in message:
        await event.respond("Hey there, Randy! 👋")

    elif "what day is it" in message:
        today = datetime.now().strftime("%A, %B %d")
        await event.respond(f"📅 Today is {today}.")

    elif "how are you" in message:
        await event.respond("I’m doing great! Ready to chat whenever you are. 😊")

    elif "what's my name" in message:
        await event.respond("You’re Randy, of course! 🧠 I never forget.")

    else:
        await event.respond("Hmm, I didn't catch that. You can say things like 'hello randy' or 'what day is it'.")
