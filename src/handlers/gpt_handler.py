import logging
import openai
from telethon import events

async def gpt_handler(event: events.NewMessage.Event):
    # 1) Ignore commands
    text = event.raw_text or ""
    if text.startswith("/"):
        return

    # 2) Show typing… (optional)
    await event.client.send_chat_action(event.chat_id, "typing")

    # 3) Call OpenAI
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
            temperature=0.7,
        )
        answer = resp.choices[0].message.content.strip()
    except Exception as e:
        logging.exception("❌ GPT API error")
        answer = "Sorry, I had trouble thinking. 🤖💤"

    # 4) Send GPT’s reply
    await event.respond(answer)
