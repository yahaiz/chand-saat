import sys
import io
import os
import logging
import threading

# Fix PyInstaller noconsole / GUI mode where sys.stdout and sys.stderr are None
class DummyStream(io.StringIO):
    def write(self, s):
        pass
    def isatty(self):
        return False
    def flush(self):
        pass

if sys.stdout is None:
    sys.stdout = DummyStream()
if sys.stderr is None:
    sys.stderr = DummyStream()

# Enable High-DPI Awareness on Windows to prevent blurry rendering
def setup_dpi_awareness():
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-monitor DPI aware
        except Exception:
            try:
                import ctypes
                ctypes.windll.user32.SetProcessDpiAware()
            except Exception:
                pass

setup_dpi_awareness()

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = get_base_dir()

if getattr(sys, 'frozen', False):
    APP_DATA_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "ChandSaat")
    os.makedirs(APP_DATA_DIR, exist_ok=True)
else:
    APP_DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_FILE = os.path.join(APP_DATA_DIR, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ],
    force=True
)

logger = logging.getLogger("ChandSaat")

APP_VERSION = "0.3.0"

DB_FILE = os.path.join(APP_DATA_DIR, "study_log.db")
EXCEL_FILE = os.path.join(APP_DATA_DIR, "study_log.xlsx")
SETTINGS_FILE = os.path.join(APP_DATA_DIR, "settings.json")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Thread Lock for file and DB operations synchronization
FILE_LOCK = threading.Lock()

REQUIRED_COLUMNS = ["id", "تاریخ", "درس", "مبحث", "زمان (دقیقه)", "تعداد تست", "تست‌های مرور", "یادداشت"]

DEFAULT_SETTINGS = {
    "daily_target_hours": 6.0,
    "daily_target_tests": 100,
    "pomo_study_min": 25,
    "pomo_break_min": 5,
    "pomo_include_break": False,
    "courses": [
        "ریاضیات عمومی/پایه",
        "آمار و احتمال",
        "ساختمان داده و الگوریتم",
        "نظریه زبان‌ها و ماشین‌ها",
        "مدار منطقی و معماری",
        "سایر"
    ]
}
