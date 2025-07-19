from telethon import events

@events.register(events.NewMessage(pattern=r"(?i)^/search (.+)"))
async def search_handler(event):
    query = event.pattern_match.group(1).strip()

    if not query:
        await event.respond("❌ You didn't provide a search query. Try using `/search your topic`.")
        return

    # Simulated search logic
    # You can later integrate real APIs like Bing or Google here
    response_text = (
        f"🔍 You searched for: `{query}`\n"
        "📚 Here's a pretend result just to get things rolling:\n"
        "👉 https://example.com/fake-search-result"
    )

    await event.respond(response_text)
