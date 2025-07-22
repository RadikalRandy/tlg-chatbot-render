import os
import importlib
import inspect
from telethon import events

def autoload_handlers(client, handlers_dir="src/handlers"):
    for filename in os.listdir(handlers_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_path = f"{handlers_dir.replace('/', '.')}.{filename[:-3]}"
            module = importlib.import_module(module_path)

            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and "event" in inspect.signature(obj).parameters:
                    client.add_event_handler(obj, events.NewMessage)
                    print(f"📦 Loaded handler: {name} from {filename}")
