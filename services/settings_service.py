import os
import json
from core.config import SETTINGS_FILE, DEFAULT_SETTINGS, FILE_LOCK, logger

def load_settings() -> dict:
    with FILE_LOCK:
        if not os.path.exists(SETTINGS_FILE):
            save_settings_unlocked(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS.copy()
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            updated = False
            for k, v in DEFAULT_SETTINGS.items():
                if k not in data:
                    data[k] = v
                    updated = True
            if updated:
                save_settings_unlocked(data)
            return data
        except Exception as e:
            logger.error(f"Error reading settings.json, reverting to defaults: {e}")
            return DEFAULT_SETTINGS.copy()

def save_settings_unlocked(data: dict):
    temp_file = SETTINGS_FILE + ".tmp"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        if os.path.exists(SETTINGS_FILE):
            os.remove(SETTINGS_FILE)
        os.rename(temp_file, SETTINGS_FILE)
    except Exception as e:
        logger.error(f"Error saving settings: {e}")
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass

def save_settings(data: dict):
    with FILE_LOCK:
        save_settings_unlocked(data)
