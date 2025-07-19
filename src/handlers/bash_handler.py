# src/handlers/bash_handler.py

import subprocess
from telethon import events

# Slash command pattern: /bash <command>
@events.register(events.NewMessage(pattern=r"(?i)^/bash (.+)"))
async def bash_handler(event):
    command = event.pattern_match.group(1)

    # Optional: restrict usage to private chats or certain users
    if not event.is_private:
        await event.reply("⚠️ Bash commands are only allowed in private chat.")
        return

    try:
        # Run the command securely with timeout
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )

        output = result.stdout.strip() or result.stderr.strip()
        if not output:
            output = "✅ Command executed successfully, but no output returned."
        elif len(output) > 4000:
            output = output[:4000] + "\n⚠️ Output truncated."

        await event.reply(f"🖥️ Bash Output:\n```{output}```")
    
    except subprocess.TimeoutExpired:
        await event.reply("⏳ Command timed out.")
    
    except Exception as e:
        await event.reply(f"❌ Error:\n{str(e)}")
