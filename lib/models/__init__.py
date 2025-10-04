# lib/models/__init__.py
import os
import sqlite3

# DB file lives at lib/db.sqlite3 (relative to this file)
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db.sqlite3"))

CONN = sqlite3.connect(DB_PATH)
CURSOR = CONN.cursor()

# Important: enable foreign keys (for ON DELETE CASCADE)
CURSOR.execute("PRAGMA foreign_keys = ON;")
CONN.commit()

# Import models at the end to avoid circular imports
from .owner import Owner  # noqa: E402
from .car import Car      # noqa: E402

__all__ = ["CONN", "CURSOR", "Owner", "Car"]
