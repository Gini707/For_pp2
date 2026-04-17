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

    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    cur.execute(
                        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                        (row[0], row[1])
                    )
        conn.commit()
        print("CSV data inserted successfully")
    except Exception as e:
        print("Error:", e)

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

# 5. Обновление телефона
def update_phone(name, new_phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE name = %s",
        (new_phone, name)
    )
    conn.commit()
    cur.close()
    conn.close()

# 6. Обновление имени
def update_name(old_name, new_name):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE phonebook SET name = %s WHERE name = %s",
        (new_name, old_name)
    )
    conn.commit()
    cur.close()
    conn.close()

# 7. Поиск по имени
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

# 8. Поиск по префиксу телефона
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

# 9. Удаление по имени
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

# 10. Удаление по телефону
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


if __name__ == "__main__":
    create_table()

    while True:
        print("\n1. Add contact")
        print("2. Show contacts")
        print("3. Search by name")
        print("4. Delete contact by name")
        print("5. Exit")
        print("6. Update phone")
        print("7. Update name")
        print("8. Insert from CSV")

        choice = input("Choose: ")

        if choice == "1":
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            insert_contact(name, phone)

        elif choice == "2":
            show_contacts()

        elif choice == "3":
            name = input("Enter name: ")
            search_by_name(name)

        elif choice == "4":
            name = input("Enter name: ")
            delete_contact_by_name(name)

        elif choice == "5":
            break

        elif choice == "6":
            name = input("Enter name: ")
            new_phone = input("Enter new phone: ")
            update_phone(name, new_phone)

        elif choice == "7":
            old_name = input("Enter old name: ")
            new_name = input("Enter new name: ")
            update_name(old_name, new_name)

        elif choice == "8":
            insert_from_csv("contacts.csv")

        else:
            print("Invalid choice")