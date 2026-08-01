import os
import pytest
from database import db, repository

@pytest.fixture(autouse=True)
def setup_test_db():
    db.init_db()
    yield

def test_add_and_get_entry():
    initial_entries = repository.get_all_entries()
    initial_count = len(initial_entries)

    entry_id = repository.add_entry(
        course="تست ریاضی",
        topic="تست مبحث",
        duration=60,
        tests=30,
        wrongs="1,2,3",
        notes="یادداشت تست"
    )

    assert entry_id > 0
    updated_entries = repository.get_all_entries()
    assert len(updated_entries) == initial_count + 1

    latest = updated_entries[0]
    assert latest["درس"] == "تست ریاضی"
    assert latest["زمان (دقیقه)"] == 60

def test_delete_entry():
    entry_id = repository.add_entry(
        course="حذفی",
        topic="تست",
        duration=10,
        tests=5,
        wrongs="-",
        notes="-"
    )
    success = repository.delete_entry(entry_id)
    assert success is True

def test_today_stats():
    repository.add_entry(
        course="امروز",
        topic="آمار",
        duration=120,
        tests=50,
        wrongs="-",
        notes="-"
    )
    today_hours, today_tests = repository.get_today_stats()
    assert today_hours >= 2.0
    assert today_tests >= 50

def test_delete_entries_batch():
    id1 = repository.add_entry(course="حذف گروهی ۱", topic="تست ۱", duration=15, tests=10, wrongs="-", notes="-")
    id2 = repository.add_entry(course="حذف گروهی ۲", topic="تست ۲", duration=25, tests=20, wrongs="-", notes="-")

    deleted_count = repository.delete_entries([id1, id2])
    assert deleted_count == 2

