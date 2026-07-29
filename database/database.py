import sqlite3


def get_db_connection():
    connection = sqlite3.connect("muttville.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS behavior_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dog_name TEXT NOT NULL,
            occurred_at TEXT NOT NULL,
            source TEXT NOT NULL,
            summary TEXT,
            details TEXT
        )
    """)

    connection.commit()
    connection.close()

def get_behavior_events():
    connection = get_db_connection()

    rows = connection.execute(
        "SELECT * FROM behavior_events"
    ).fetchall()

    connection.close()
    return rows