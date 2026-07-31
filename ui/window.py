import os
import time
import webview
from core.config import logger, APP_DATA_DIR

class WindowAPI:
    def __init__(self, window_instance=None):
        self._window = window_instance

    def set_window(self, window_instance):
        self._window = window_instance

    def minimize(self):
        if self._window:
            self._window.minimize()

    def toggle_maximize(self):
        if self._window:
            try:
                if getattr(self._window, '_is_maximized', False):
                    self._window.restore()
                    self._window._is_maximized = False
                else:
                    self._window.maximize()
                    self._window._is_maximized = True
                return self._window._is_maximized
            except Exception as e:
                logger.error(f"Error toggling maximize: {e}")
                return False
        return False

    def is_maximized(self):
        if self._window:
            return getattr(self._window, '_is_maximized', False)
        return False

    def toggle_fullscreen(self):
        if self._window:
            self._window.toggle_fullscreen()

    def close(self):
        if self._window:
            self._window.destroy()

    def save_excel_dialog(self):
        if self._window:
            try:
                from database import repository
                from datetime import datetime
                import shutil

                excel_path = repository.export_to_excel()
                default_filename = f"گزارش_مطالعه_چند_ساعت_{datetime.now().strftime('%Y-%m-%d')}.xlsx"

                result = self._window.create_file_dialog(
                    webview.SAVE_DIALOG,
                    save_filename=default_filename,
                    file_types=('Excel Files (*.xlsx)', 'All Files (*.*)')
                )
                if result:
                    dest_path = result[0] if isinstance(result, (tuple, list)) and len(result) > 0 else (result if isinstance(result, str) else None)
                    if dest_path:
                        shutil.copyfile(excel_path, dest_path)
                        logger.info(f"Excel report saved successfully to: {dest_path}")
                        return {"success": True, "path": dest_path}
                return {"success": False, "canceled": True}
            except Exception as e:
                logger.error(f"Error in save_excel_dialog: {e}")
                return {"success": False, "error": str(e)}
        return {"success": False, "error": "No window"}

window_api = WindowAPI()

def create_main_window(url: str = "http://127.0.0.1:28475/"):
    window = webview.create_window(
        'چند ساعت؟',
        url,
        width=1120,
        height=760,
        resizable=True,
        focus=True,
        js_api=window_api
    )
    window_api.set_window(window)

    def on_shown():
        try:
            from routes.pages import set_window_ready
            set_window_ready()
            time.sleep(0.1)
            window.restore()
            focus_attr = getattr(window, 'focus', None)
            if callable(focus_attr):
                focus_attr()
            if hasattr(window, 'gui_handle') and window.gui_handle:
                import ctypes
                ctypes.windll.user32.SetForegroundWindow(window.gui_handle)
        except Exception as e:
            logger.error(f"Focus window error: {e}")

    storage_dir = os.path.join(APP_DATA_DIR, "webcache")
    os.makedirs(storage_dir, exist_ok=True)

    try:
        webview.start(on_shown, storage_path=storage_dir)
    except Exception as e:
        logger.critical(f"PyWebView start failure: {e}", exc_info=True)

