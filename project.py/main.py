from database.db_shema import create_tables
from database.db_users import add_user,get_all_users
from database.db_products import add_product,get_all_products


create_tables()

add_user("vcwrv","ecre",2)
add_user("Fw","vqqq",32)

add_product("Qv",32)
add_product("qccq",3)

print("пользователи")
for users in get_all_users(): # не было скобок 
    print(users)

print("\n продукты")
for products in get_all_products():
    print(products)