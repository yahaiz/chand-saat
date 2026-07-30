import threading
import time
import urllib.request
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.config import logger, APP_VERSION, APP_DATA_DIR, STATIC_DIR
from database.db import init_db
from routes import pages, entries, settings_routes
from ui.splash import show_splash
from ui.window import create_main_window

app = FastAPI(title="چند ساعت؟ - ChandSaat")

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include Routers
app.include_router(pages.router)
app.include_router(entries.router)
app.include_router(settings_routes.router)

server_instance = None

def run_server():
    global server_instance
    try:
        config = uvicorn.Config(app, host="127.0.0.1", port=28475, log_config=None)
        server_instance = uvicorn.Server(config)
        logger.info("Starting Uvicorn server on http://127.0.0.1:28475...")
        server_instance.run()
    except Exception as e:
        logger.critical(f"Uvicorn server failed to start: {e}", exc_info=True)

def wait_for_server(timeout=15):
    start = time.time()
    url = "http://127.0.0.1:28475/"
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=1) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.15)
    return False

def launch_app():
    logger.info("==================================================")
    logger.info(f"ChandSaat v{APP_VERSION} starting... APP_DATA_DIR={APP_DATA_DIR}")

    # 1. Initialize SQLite Database (and auto-migrate legacy Excel if present)
    init_db()

    # 2. Start Uvicorn server in a daemon thread
    t = threading.Thread(target=run_server, daemon=True)
    t.start()

    # 3. Show desktop splash screen
    show_splash(server_port=28475)

    # 4. Wait for server readiness
    wait_for_server(timeout=15)

    # 5. Create native pywebview window
    create_main_window(url="http://127.0.0.1:28475/")

if __name__ == "__main__":
    launch_app()
