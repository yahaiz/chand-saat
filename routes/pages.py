import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from core.config import TEMPLATES_DIR, BASE_DIR, logger
from database import repository
from services.settings_service import load_settings

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        records = repository.get_all_entries()
        settings = load_settings()
        today_hours, today_tests = repository.get_today_stats()

        target_hours = float(settings.get("daily_target_hours", 6.0))
        target_tests = int(settings.get("daily_target_tests", 100))

        progress_hours = min(int((today_hours / target_hours) * 100), 100) if target_hours > 0 else 0
        progress_tests = min(int((today_tests / target_tests) * 100), 100) if target_tests > 0 else 0

        initial_data = {
            "records": records,
            "settings": settings,
            "today_hours": today_hours,
            "today_tests": today_tests,
            "progress_hours": progress_hours,
            "progress_tests": progress_tests,
            "total_records": len(records)
        }
        import json
        initial_data_json = json.dumps(initial_data, ensure_ascii=False)

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "records": records,
                "settings": settings,
                "today_hours": today_hours,
                "today_tests": today_tests,
                "progress_hours": progress_hours,
                "progress_tests": progress_tests,
                "total_records": len(records),
                "initial_data_json": initial_data_json
            }
        )
    except Exception as e:
        logger.error(f"Error rendering root page: {e}")
        return HTMLResponse(content=f"<h3>خطا در بارگذاری برنامه: {e}</h3>", status_code=500)

WINDOW_READY = False

def set_window_ready():
    global WINDOW_READY
    WINDOW_READY = True

@router.get("/splash_ready")
async def is_splash_ready():
    if WINDOW_READY:
        return {"ready": True}
    return JSONResponse(status_code=503, content={"ready": False})

@router.get("/icon.png")
async def get_icon():
    icon_path = os.path.join(BASE_DIR, "icon.png")
    if os.path.exists(icon_path):
        return FileResponse(icon_path, media_type="image/png")
    return HTMLResponse(status_code=404)

@router.get("/splash.png")
async def get_splash():
    splash_path = os.path.join(BASE_DIR, "splash.png")
    if os.path.exists(splash_path):
        return FileResponse(splash_path, media_type="image/png")
    return HTMLResponse(status_code=404)

@router.get("/svg_showcase.html", response_class=HTMLResponse)
@router.get("/showcase", response_class=HTMLResponse)
async def get_svg_showcase(request: Request):
    return templates.TemplateResponse(request=request, name="svg_showcase.html")


