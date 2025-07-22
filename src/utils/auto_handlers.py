import importlib
import logging
import os
from telethon import TelegramClient

def autoload_handlers(client: TelegramClient) -> None:
    """
    Scan src/handlers/, import each .py (except __init__.py),
    and call its register(client) function if present.
    """
    # locate src/utils/, then go up one to src/, then into handlers/
    base = os.path.dirname(__file__)
    handlers_dir = os.path.abspath(os.path.join(base, "..", "handlers"))
    pkg_root = "src.handlers"

    if not os.path.isdir(handlers_dir):
        logging.error(f"❌ Handlers directory not found: {handlers_dir}")
        return

    for fname in os.listdir(handlers_dir):
        if not fname.endswith(".py") or fname.startswith("__"):
            continue
        mod_name = fname[:-3]
        import_path = f"{pkg_root}.{mod_name}"
        try:
            module = importlib.import_module(import_path)
            if hasattr(module, "register"):
                module.register(client)
                logging.info(f"✅ Registered handler: {mod_name}")
            else:
                logging.warning(f"⚠️ No register() in handler: {mod_name}")
        except Exception:
            logging.exception(f"❌ Failed loading handler module: {import_path}")
