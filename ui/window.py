import time
import webview
from core.config import logger

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
            time.sleep(0.1)
            window.restore()
            if callable(getattr(window, 'focus', None)):
                window.focus()
            if hasattr(window, 'gui_handle') and window.gui_handle:
                import ctypes
                ctypes.windll.user32.SetForegroundWindow(window.gui_handle)
        except Exception as e:
            logger.error(f"Focus window error: {e}")

    webview.start(on_shown)
