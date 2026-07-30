import os
from datetime import datetime
from database.db import get_connection
from core.config import FILE_LOCK, EXCEL_FILE, REQUIRED_COLUMNS, logger

def get_all_entries() -> list[dict]:
    with FILE_LOCK:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, date AS "تاریخ", course AS "درس", topic AS "مبحث",
                       duration AS "زمان (دقیقه)", tests AS "تعداد تست",
                       wrongs AS "تست‌های مرور", notes AS "یادداشت"
                FROM study_logs
                ORDER BY id DESC
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

def add_entry(course: str, topic: str, duration: int, tests: int, wrongs: str, notes: str) -> int:
    with FILE_LOCK:
        duration = max(0, duration)
        tests = max(0, tests)
        date_str = datetime.now().strftime("%Y-%m-%d")
        course_clean = course.strip() if course else "سایر"
        topic_clean = topic.strip() if topic and topic.strip() else "-"
        wrongs_clean = wrongs.strip() if wrongs and wrongs.strip() else "-"
        notes_clean = notes.strip() if notes and notes.strip() else "-"

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO study_logs (date, course, topic, duration, tests, wrongs, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (date_str, course_clean, topic_clean, duration, tests, wrongs_clean, notes_clean))
            conn.commit()
            new_id = cursor.lastrowid
            logger.info(f"Added new study entry ID={new_id}")
            return new_id
        finally:
            conn.close()

def delete_entry(item_id: int) -> bool:
    with FILE_LOCK:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM study_logs WHERE id = ?", (item_id,))
            conn.commit()
            logger.info(f"Deleted study entry ID={item_id}")
            return cursor.rowcount > 0
        finally:
            conn.close()

def get_today_stats() -> tuple[float, int]:
    today_str = datetime.now().strftime("%Y-%m-%d")
    with FILE_LOCK:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(duration) as total_duration, SUM(tests) as total_tests
                FROM study_logs
                WHERE date = ?
            """, (today_str,))
            row = cursor.fetchone()
            total_minutes = row["total_duration"] or 0
            total_tests = row["total_tests"] or 0
            today_hours = round(float(total_minutes) / 60.0, 1)
            return today_hours, int(total_tests)
        finally:
            conn.close()

def export_to_excel() -> str:
    import pandas as pd
    with FILE_LOCK:
        conn = get_connection()
        try:
            df = pd.read_sql_query("""
                SELECT id, date AS "تاریخ", course AS "درس", topic AS "مبحث",
                       duration AS "زمان (دقیقه)", tests AS "تعداد تست",
                       wrongs AS "تست‌های مرور", notes AS "یادداشت"
                FROM study_logs
                ORDER BY id ASC
            """, conn)
            
            if df.empty:
                df = pd.DataFrame(columns=REQUIRED_COLUMNS)
                
            temp_excel = EXCEL_FILE + ".tmp.xlsx"
            df.to_excel(temp_excel, index=False)
            if os.path.exists(EXCEL_FILE):
                os.remove(EXCEL_FILE)
            os.rename(temp_excel, EXCEL_FILE)
            return EXCEL_FILE
        except Exception as e:
            logger.error(f"Error exporting database to Excel: {e}")
            df_empty = pd.DataFrame(columns=REQUIRED_COLUMNS)
            df_empty.to_excel(EXCEL_FILE, index=False)
            return EXCEL_FILE
        finally:
            conn.close()
