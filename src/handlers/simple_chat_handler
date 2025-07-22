import logging
import openai
from telethon import events

# Simple in-memory session per user (no persistence yet)
user_sessions = {}

async def gpt_handler(event: events.NewMessage.Event):
    user_id = event.sender_id
    text = event.raw_text.strip()
    
    # Ignore commands like /start, /clear, etc.
    if text.startswith("/"):
        return

    # Show "typing…" status in chat
    await event.client.send_chat_action(event.chat_id, "typing")

    # Initialize or retrieve user message history
    history = user_sessions.get(user_id, [])

    # Inject system prompt once per user session
    if not any(msg.get("role") == "system" for msg in history):
        history.insert(0, {
            "role": "system",
            "content": (
                "You are a friendly, conversational AI who replies in a witty, casual, and helpful tone. "
                "You remember user preferences when possible and make chats feel natural and engaging."
            )
        })

    # Add the user's message to history
    history.append({"role": "user", "content": text})

    # Request GPT completion
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=history,
            temperature=0.7,
        )
        answer = response.choices[0].message.content.strip()

        # Append GPT's reply to history
        history.append({"role": "assistant", "content": answer})
        user_sessions[user_id] = history  # Save updated session

    except Exception as e:
        logging.exception("❌ GPT API error")
        answer = "Sorry, I had trouble thinking. 🤖💤"

    # Send reply to user
    await event.respond(answer)
