import sys
import os
import threading
import socket
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.config import logger, APP_VERSION, APP_DATA_DIR, STATIC_DIR
from database.db import init_db
from routes import pages, entries, settings_routes
from ui.window import create_main_window

app = FastAPI(title="چند ساعت؟ - ChandSaat")

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include Routers
app.include_router(pages.router)
app.include_router(entries.router)
app.include_router(settings_routes.router)

server_instance = None
SERVER_PORT = 28475

def get_free_port(default_port=28475) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", default_port))
            return default_port
        except OSError:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]

def run_server(port: int):
    global server_instance
    try:
        config = uvicorn.Config(app, host="127.0.0.1", port=port, log_config=None, access_log=False)
        server_instance = uvicorn.Server(config)
        server_instance.run()
    except Exception as e:
        logger.critical(f"Uvicorn server failed to start on port {port}: {e}", exc_info=True)

def launch_app():
    global SERVER_PORT
    try:
        # 1. Fast SQLite Init (pandas is lazy loaded)
        init_db()

        # 2. Instant port check (0.1ms)
        SERVER_PORT = get_free_port(default_port=28475)

        # 3. Start Uvicorn daemon thread immediately
        t = threading.Thread(target=run_server, args=(SERVER_PORT,), daemon=True)
        t.start()

        # 4. Launch PyWebView window directly without blocking loops
        create_main_window(url=f"http://127.0.0.1:{SERVER_PORT}/")
    except Exception as launch_err:
        logger.critical(f"Unhandled error during launch_app: {launch_err}", exc_info=True)

if __name__ == "__main__":
    launch_app()
