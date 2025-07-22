# Simple re-export so your bot.py only needs to import one name
from src.utils.auto_handlers import autoload_handlers

__all__ = ["autoload_handlers"]
