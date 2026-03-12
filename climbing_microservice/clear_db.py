"""
Clear the database.
"""

import os
from database import init_db

DB_PATH = "climbs.db"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print(f'deleted')

init_db()
print(f'new database initialized')