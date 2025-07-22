import asyncio
import logging
import os

from fastapi import FastAPI

from src.bot import bot  # <-- will point at src/bot.py

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = FastAPI(title="Randy's Telegram+FastAPI Bot")

@app.on_event("startup")
async def startup_event():
    logging.info("🚀 Starting Telegram bot in background…")
    # Fire-and-forget the Telegram client
    asyncio.create_task(bot())

@app.get("/", tags=["health"])
async def root():
    return {"status": "ok", "message": "FastAPI is up."}

@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy", "env": os.getenv("ENV", "dev")}
