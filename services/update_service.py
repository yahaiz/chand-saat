import json
import re
import sys
import os
import urllib.request
from core.config import logger, APP_VERSION

GITHUB_RELEASES_API = "https://api.github.com/repos/yahaiz/chand-saat/releases/latest"

def parse_version_tuple(v_str: str) -> tuple:
    """Extract numeric tuple (major, minor, patch) from version string like 'v0.2.1' or '0.2.1'."""
    clean = re.sub(r'^[^\d]+', '', str(v_str or '')).strip()
    parts = clean.split('-')[0].split('.')
    nums = []
    for p in parts:
        try:
            nums.append(int(p))
        except ValueError:
            nums.append(0)
    while len(nums) < 3:
        nums.append(0)
    return tuple(nums[:3])

def is_installed_setup_env() -> bool:
    """Check if app is running from a standard Windows installation directory."""
    if getattr(sys, 'frozen', False):
        exe_path = os.path.abspath(sys.executable).lower()
        if "program files" in exe_path or "localappdata\\programs" in exe_path:
            return True
    return False

def check_github_update(current_version: str = None) -> dict:
    if not current_version:
        current_version = APP_VERSION

    try:
        req = urllib.request.Request(
            GITHUB_RELEASES_API,
            headers={
                "User-Agent": "ChandSaat-Desktop-App",
                "Accept": "application/vnd.github.v3+json"
            }
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                tag_name = data.get("tag_name", "")
                release_name = data.get("name", tag_name)
                release_notes = data.get("body", "به‌روزرسانی جدید چند ساعت؟ منتشر شد.")
                html_url = data.get("html_url", "https://github.com/yahaiz/chand-saat/releases")

                setup_url = None
                portable_url = None
                apk_url = None

                assets = data.get("assets", [])
                for asset in assets:
                    name = asset.get("name", "").lower()
                    url = asset.get("browser_download_url", "")
                    if url.endswith(".apk"):
                        apk_url = url
                    elif "setup" in name or "installer" in name:
                        setup_url = url
                    elif "portable" in name or url.endswith(".zip"):
                        portable_url = url
                    elif url.endswith(".exe") and not setup_url:
                        setup_url = url

                is_setup = is_installed_setup_env()
                if is_setup and setup_url:
                    download_url = setup_url
                elif portable_url:
                    download_url = portable_url
                else:
                    download_url = setup_url or apk_url or html_url

                current_tuple = parse_version_tuple(current_version)
                latest_tuple = parse_version_tuple(tag_name)

                has_update = latest_tuple > current_tuple

                return {
                    "success": True,
                    "has_update": has_update,
                    "current_version": current_version,
                    "latest_version": tag_name,
                    "release_name": release_name,
                    "release_notes": release_notes,
                    "html_url": html_url,
                    "download_url": download_url,
                    "setup_url": setup_url or download_url,
                    "portable_url": portable_url or download_url,
                    "apk_url": apk_url,
                    "is_installed_env": is_setup
                }
    except Exception as e:
        logger.warning(f"Failed to check GitHub update: {e}")
        return {
            "success": False,
            "has_update": False,
            "current_version": current_version,
            "error": str(e)
        }
