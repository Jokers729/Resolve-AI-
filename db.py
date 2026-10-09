import sqlite3

DB_NAME = "resolveai.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            location TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            priority TEXT DEFAULT 'Medium'
        )
    """)

    # Add priority column to an existing database if needed
    try:
        conn.execute(
            "ALTER TABLE complaints ADD COLUMN priority TEXT DEFAULT 'Medium'"
        )
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()


def add_complaint(description, location, category):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        """
        INSERT INTO complaints (description, location, category)
        VALUES (?, ?, ?)
        """,
        (description, location, category)
    )

    conn.commit()
    conn.close()


def get_complaints():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.execute(
        "SELECT * FROM complaints ORDER BY id DESC"
    )

    complaints = cursor.fetchall()
    conn.close()

    return complaints