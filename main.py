import threading
import time
import socket
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
SERVER_PORT = 28475

def find_available_port(default_port=28475) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", default_port))
            return default_port
        except OSError:
            # Check if existing server is responsive on default_port
            try:
                req = urllib.request.Request(f"http://127.0.0.1:{default_port}/", headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=0.5) as resp:
                    if resp.status == 200:
                        logger.info(f"Existing ChandSaat server found running on port {default_port}")
                        return default_port
            except Exception:
                pass

            # Pick dynamic free port
            s.bind(("127.0.0.1", 0))
            free_port = s.getsockname()[1]
            logger.info(f"Port {default_port} busy, assigned dynamic port {free_port}")
            return free_port

def run_server(port: int):
    global server_instance
    try:
        config = uvicorn.Config(app, host="127.0.0.1", port=port, log_config=None)
        server_instance = uvicorn.Server(config)
        logger.info(f"Starting Uvicorn server on http://127.0.0.1:{port}...")
        server_instance.run()
    except Exception as e:
        logger.critical(f"Uvicorn server failed to start on port {port}: {e}", exc_info=True)

def wait_for_server(port: int, timeout=15):
    start = time.time()
    url = f"http://127.0.0.1:{port}/"
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
    global SERVER_PORT
    logger.info("==================================================")
    logger.info(f"ChandSaat v{APP_VERSION} starting... APP_DATA_DIR={APP_DATA_DIR}")

    # 1. Initialize SQLite Database (and auto-migrate legacy Excel if present)
    init_db()

    # 2. Find available port
    SERVER_PORT = find_available_port(default_port=28475)

    # 3. Check if server already running on port 28475
    server_already_running = False
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{SERVER_PORT}/", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=0.3) as resp:
            if resp.status == 200:
                server_already_running = True
    except Exception:
        server_already_running = False

    if not server_already_running:
        # Start Uvicorn server in a daemon thread
        t = threading.Thread(target=run_server, args=(SERVER_PORT,), daemon=True)
        t.start()

    # 4. Show desktop splash screen
    show_splash(server_port=SERVER_PORT)

    # 5. Wait for server readiness
    wait_for_server(port=SERVER_PORT, timeout=15)

    # 6. Create native pywebview window
    create_main_window(url=f"http://127.0.0.1:{SERVER_PORT}/")

if __name__ == "__main__":
    launch_app()
