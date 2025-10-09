# lib/models/__init__.py
import os, sqlite3
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db.sqlite3"))
CONN = sqlite3.connect(DB_PATH)
CURSOR = CONN.cursor()
CURSOR.execute("PRAGMA foreign_keys = ON;")
CONN.commit()

__all__ = ["CONN", "CURSOR", "DB_PATH"]