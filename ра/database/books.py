from db import get_connection

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