from db import create_tables
from books import add_book,get_all_books


create_tables()


add_book("btrw","bwrbt",24)
add_book("vwvw","vew",24)

print("все книги ")
for books in get_all_books():
    print(books)