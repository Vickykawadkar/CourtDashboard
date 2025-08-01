import sqlite3
import json

DB_NAME = "queries.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT,
            case_number TEXT,
            filing_year TEXT,
            response_json TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_query(case_type, case_number, filing_year, response_data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO queries (case_type, case_number, filing_year, response_json)
        VALUES (?, ?, ?, ?)
    """, (case_type, case_number, filing_year, json.dumps(response_data)))
    conn.commit()
    conn.close()

init_db()
