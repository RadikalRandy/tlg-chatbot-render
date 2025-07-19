from telethon import events
from datetime import datetime

@events.register(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def simple_chat_handler(event):
    text = event.raw_text.strip().lower()

    if "hello randy" in text:
        await event.respond("Hey there, Randy! 👋")

    elif "what day is it" in text:
        today = datetime.now().strftime("%A, %B %d")
        await event.respond(f"📅 Today is {today}.")

    elif "how are you" in text:
        await event.respond("I’m doing great! Ready to chat whenever you are. 😊")

    else:
        await event.respond("I'm here, but didn't quite catch that. Try saying 'hello randy' or 'what day is it'.")
