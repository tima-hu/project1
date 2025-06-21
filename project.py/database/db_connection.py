import sqlite3

DB_MAME = "my_database.db"

def get_connection():
    return sqlite3.connect(DB_MAME)

