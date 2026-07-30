import sqlite3
import os
from core.config import DB_FILE, EXCEL_FILE, REQUIRED_COLUMNS, FILE_LOCK, logger

def get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with FILE_LOCK:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS study_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    course TEXT NOT NULL,
                    topic TEXT DEFAULT '-',
                    duration INTEGER NOT NULL DEFAULT 0,
                    tests INTEGER NOT NULL DEFAULT 0,
                    wrongs TEXT DEFAULT '-',
                    notes TEXT DEFAULT '-'
                )
            """)
            conn.commit()

            # Check if database is brand new and if existing study_log.xlsx exists for auto-migration
            cursor.execute("SELECT COUNT(*) as count FROM study_logs")
            count = cursor.fetchone()["count"]

            if count == 0 and os.path.exists(EXCEL_FILE):
                logger.info("Migrating legacy study_log.xlsx into SQLite database...")
                try:
                    import pandas as pd
                    df = pd.read_excel(EXCEL_FILE)
                    if not df.empty:
                        for _, row in df.iterrows():
                            date_str = str(row.get("تاریخ", "")).strip()
                            if not date_str or date_str == "nan":
                                continue
                            course = str(row.get("درس", "سایر")).strip()
                            topic = str(row.get("مبحث", "-")).strip()
                            duration = int(pd.to_numeric(row.get("زمان (دقیقه)", 0), errors="coerce") or 0)
                            tests = int(pd.to_numeric(row.get("تعداد تست", 0), errors="coerce") or 0)
                            wrongs = str(row.get("تست‌های مرور", "-")).strip()
                            notes = str(row.get("یادداشت", "-")).strip()

                            cursor.execute("""
                                INSERT INTO study_logs (date, course, topic, duration, tests, wrongs, notes)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (date_str, course, topic, duration, tests, wrongs, notes))
                        conn.commit()
                        logger.info("Successfully migrated legacy Excel data to SQLite.")
                except Exception as mig_err:
                    logger.error(f"Error during legacy Excel migration: {mig_err}")
        finally:
            conn.close()
