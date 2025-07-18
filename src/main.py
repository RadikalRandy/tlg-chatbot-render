# src/main.py

import asyncio
import logging
import subprocess
from contextlib import asynccontextmanager
from typing import Generator

import uvicorn
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import HTMLResponse, StreamingResponse

from __version__ import __version__
from src.bot import bot
from src.utils import (
    BOT_NAME,
    LOG_PATH,
    create_initial_folders,
    get_date_time,
    initialize_logging,
    terminal_html,
)

# Initialize folders & logging
create_initial_folders()
console_out = initialize_logging()
time_str = get_date_time("Asia/Ho_Chi_Minh")

# Bot version fallback
try:
    BOT_VERSION = __version__
except ImportError:
    BOT_VERSION = "with unknown version"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan handler to start the Telegram bot in the background
    when the app starts and to log shutdown when the app closes.
    """
    # Startup
    try:
        logging.info("🚀 Launching Telegram bot in background…")
        loop = asyncio.get_event_loop()
        task = loop.create_task(bot())
        # Optional: track background tasks if needed
        task.add_done_callback(lambda t: logging.info("🔹 Telegram bot task completed."))
        logging.info("✅ App initiated")
    except Exception as e:
        logging.critical(f"❌ Error starting Telegram bot: {e}")
        raise

    yield  # Application runs here

    # Shutdown
    logging.info("🛑 Application close…")

# Create FastAPI app with our lifespan manager
app = FastAPI(lifespan=lifespan, title=BOT_NAME)

@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    """
    Root endpoint to confirm the app is running.
    """
    return f"{BOT_NAME} {BOT_VERSION} is deployed on {time_str}"

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> str:
    """
    Simple health check endpoint.
    """
    return f"{BOT_NAME} {BOT_VERSION} is healthy"

@app.get("/log")
async def log_check() -> StreamingResponse:
    """
    Stream the in-memory console log for debugging.
    """
    async def generate_log() -> Generator[bytes, None, None]:
        console_log = console_out.getvalue()
        yield console_log.encode("utf-8")

    return StreamingResponse(generate_log(), media_type="text/plain")

# Uncomment these if you want a web-based terminal:
# @app.get("/terminal", response_class=HTMLResponse)
# async def terminal(request: Request) -> Response:
#     return Response(content=terminal_html(), media_type="text/html")
#
# @app.post("/terminal/run")
# async def run_command(command: dict) -> str:
#     try:
#         output_bytes = subprocess.check_output(
#             command["command"], shell=True, stderr=subprocess.STDOUT
#         )
#         output_str = output_bytes.decode("utf-8")
#         return "<br>".join(line.strip() for line in output_str.splitlines())
#     except subprocess.CalledProcessError as e:
#         return e.output.decode("utf-8")

# If you run this file directly, start Uvicorn
if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=False)
