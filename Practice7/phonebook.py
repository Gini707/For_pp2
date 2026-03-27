from connect import connect
import csv

# 1. Создание таблицы
def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# 2. Вставка с консоли
def insert_contact(name, phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()

# 3. Загрузка из CSV
def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (row[0], row[1])
            )
    conn.commit()
    cur.close()
    conn.close()

# 4. Показ всех контактов
def show_contacts():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

# 5. Обновление
def update_contact(name, new_phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE name = %s",
        (new_phone, name)
    )
    conn.commit()
    cur.close()
    conn.close()

# 6. Поиск (filter)
def search_by_name(name):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM phonebook WHERE name = %s",
        (name,)
    )
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def search_by_prefix(prefix):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s",
        (prefix + "%",)
    )
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

# 7. Удаление
def delete_contact_by_name(name):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM phonebook WHERE name = %s",
        (name,)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_contact_by_phone(phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM phonebook WHERE phone = %s",
        (phone,)
    )
    conn.commit()
    cur.close()
    conn.close()

