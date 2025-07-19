# src/handlers/clear_handler.py

from telethon import events

# Responds to "/clear" command in private chat
@events.register(events.NewMessage(pattern=r"(?i)^/clear$"))
async def clear_handler(event):
    if not event.is_private:
        await event.respond("🧹 /clear can only be used in private chat.")
        return

    # Placeholder behavior — you can expand this later!
    await event.respond("✅ Cleared! I'm ready for a fresh start.")
