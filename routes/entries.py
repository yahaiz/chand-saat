from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse
from database import repository
from core.config import logger

router = APIRouter()

@router.post("/add")
async def add_entry(
    course: str = Form(...),
    topic: str = Form(""),
    duration: int = Form(...),
    tests: int = Form(0),
    wrongs: str = Form("-"),
    notes: str = Form("-")
):
    try:
        repository.add_entry(
            course=course,
            topic=topic,
            duration=duration,
            tests=tests,
            wrongs=wrongs,
            notes=notes
        )
    except Exception as e:
        logger.error(f"Error in add_entry route: {e}")

    return RedirectResponse(url="/", status_code=303)

@router.post("/delete/{item_id}")
async def delete_entry(item_id: int):
    try:
        repository.delete_entry(item_id)
    except Exception as e:
        logger.error(f"Error in delete_entry route: {e}")

    return RedirectResponse(url="/", status_code=303)
