from datetime import datetime
from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse, FileResponse
from services.settings_service import save_settings
from database import repository
from core.config import DEFAULT_SETTINGS, logger

router = APIRouter()

@router.post("/settings")
async def update_settings(
    daily_target_hours: float = Form(...),
    daily_target_tests: int = Form(...),
    pomo_study_min: int = Form(25),
    pomo_break_min: int = Form(5),
    pomo_include_break: bool = Form(False),
    courses_raw: str = Form(...)
):
    try:
        daily_target_hours = max(0.1, daily_target_hours)
        daily_target_tests = max(1, daily_target_tests)
        pomo_study_min = max(1, pomo_study_min)
        pomo_break_min = max(1, pomo_break_min)

        courses_list = [c.strip() for c in courses_raw.split("\n") if c.strip()]
        if not courses_list:
            courses_list = DEFAULT_SETTINGS["courses"]

        new_settings = {
            "daily_target_hours": daily_target_hours,
            "daily_target_tests": daily_target_tests,
            "pomo_study_min": pomo_study_min,
            "pomo_break_min": pomo_break_min,
            "pomo_include_break": pomo_include_break,
            "courses": courses_list
        }
        save_settings(new_settings)
    except Exception as e:
        logger.error(f"Error in update_settings route: {e}")

    return RedirectResponse(url="/", status_code=303)

@router.get("/export")
async def export_excel():
    try:
        from urllib.parse import quote
        excel_path = repository.export_to_excel()
        filename = f"گزارش_مطالعه_چند_ساعت_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
        encoded_filename = quote(filename)
        headers = {
            "Content-Disposition": f"attachment; filename=\"ChandSaat_Report.xlsx\"; filename*=UTF-8''{encoded_filename}"
        }
        return FileResponse(
            excel_path,
            headers=headers,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        logger.error(f"Error exporting file: {e}")
        return RedirectResponse(url="/", status_code=303)
