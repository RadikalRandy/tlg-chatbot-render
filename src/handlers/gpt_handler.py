import logging
import openai
from telethon import events

# Simple in-memory session per user
user_sessions = {}

async def gpt_handler(event: events.NewMessage.Event):
    user_id = event.sender_id
    text = event.raw_text or ""
    if text.startswith("/"):
        return

    # Show typing action
    await event.client.send_chat_action(event.chat_id, "typing")

    # Get or initialize message history
    history = user_sessions.get(user_id, [])
    history.append({"role": "user", "content": text})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=history,
            temperature=0.7,
        )
        answer = response.choices[0].message.content.strip()
        history.append({"role": "assistant", "content": answer})
        user_sessions[user_id] = history  # Save session
    except Exception as e:
        logging.exception("❌ GPT API error")
        answer = "Sorry, I had trouble thinking. 🤖💤"

    await event.respond(answer)
