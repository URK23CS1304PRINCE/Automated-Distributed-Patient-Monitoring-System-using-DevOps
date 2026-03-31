import sqlite3

def init_db():
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vitals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        heart_rate INTEGER,
        temperature REAL,
        spo2 INTEGER,
        state TEXT
    )
    """)

    conn.commit()
    conn.close()