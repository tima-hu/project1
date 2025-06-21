import sqlite3

DB_MAME = "my_books.db"

def get_connection():
    return sqlite3.connect(DB_MAME)

def create_tables():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER
            )
        """)

from database.db import get_connection

def add_book(title, author, year):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO books (title, author, year) VALUES(?,?,?)",(title,author,year))
        conn.commit() 

def get_all_books():
        with get_connection() as conn:
            rut = conn.cursor()
            rut.execute("SELECT id, title, author, year FROM books")
            return rut.fetchall()
        
from database.books import get_all_books,add_book
from database.db import create_tables,get_connection
create_tables()


add_book("btrw","bwrbt",24)
add_book("vwvw","vew",24)

print("все книги ")
for books in get_all_books:
    print(books)