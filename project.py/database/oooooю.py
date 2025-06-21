import sqlite3

DB_тAME = "my_database.db"

def get_connection():
    return sqlite3.connect(DB_тAME)

def create_tables():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
        conn.commit()

def add_user(name,email,age):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO users( name, email, age) VALUES(?,?,?)",(name,email,age))
            conn.commit()
            return True
    except sqlite3.IntegrityError as e:
        print(f"Ошибк при добавлении пользователя:{e}")
        return False
def get_all_users():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, age FROM  users")
        return cur.fetchall()
def add_product(title,price):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO products (title, price) VALUES(?,?)",(title,price))
        conn.commit()

def get_all_products():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, title, price FROM products")
        return cur.fetchall()
    
create_tables()

add_user("vcwrv","ecre",2)
add_user("Fw","vqqq",32)

add_product("Qv",32)
add_product("qccq",3)

print("пользователи")
for users in get_all_users():
    print(users)

print("\n продукты")
for products in get_all_products():
    print(products)
