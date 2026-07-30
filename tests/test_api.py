import pytest
from fastapi.testclient import TestClient
from main import app
from database.db import init_db

@pytest.fixture(autouse=True)
def setup_api_test_db():
    init_db()

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "چند ساعت؟" in response.text

def test_add_entry_route():
    response = client.post("/add", data={
        "course": "تست API",
        "topic": "اندپکیک",
        "duration": 45,
        "tests": 20,
        "wrongs": "-",
        "notes": "-"
    }, follow_redirects=False)
    assert response.status_code == 303

def test_settings_route():
    response = client.post("/settings", data={
        "daily_target_hours": 8.0,
        "daily_target_tests": 120,
        "pomo_study_min": 30,
        "pomo_break_min": 5,
        "pomo_include_break": False,
        "courses_raw": "درس یک\nدرس دو"
    }, follow_redirects=False)
    assert response.status_code == 303

def test_export_route():
    response = client.get("/export")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
