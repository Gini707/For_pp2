import csv   # нужен для чтения contacts.csv
import json  # нужен для импорта/экспорта contacts.json
from connect import get_connection  # импортируем функцию подключения к PostgreSQL


def show_contacts():
    # Подключаемся к базе данных
    conn = get_connection()
    cur = conn.cursor()

    # Здесь показываются все контакты.
    # LEFT JOIN нужен, чтобы вместе с контактом показать название группы.
    cur.execute("""
        SELECT 
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name AS group_name,
            c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.name;
    """)

    rows = cur.fetchall()

    print("\nCONTACTS:")
    for row in rows:
        print(row)

    # Закрываем cursor и соединение
    cur.close()
    conn.close()


def add_contact():
    # Пользователь вводит данные нового контакта
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday YYYY-MM-DD: ")
    group_name = input("Group Family/Work/Friend/Other: ")

    conn = get_connection()
    cur = conn.cursor()

    # Сначала создаём группу, если её ещё нет.
    # ON CONFLICT нужен, чтобы не было ошибки, если такая группа уже существует.
    cur.execute("""
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT(name) DO NOTHING;
    """, (group_name,))

    # Берём id группы, чтобы связать контакт с этой группой через foreign key
    cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
    group_id = cur.fetchone()[0]

    # Здесь добавляется сам контакт в таблицу contacts
    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s);
    """, (name, email, birthday, group_id))

    # commit сохраняет изменения в базе
    conn.commit()
    cur.close()
    conn.close()

    print("Contact added!")


def add_phone():
    # Вводим имя контакта и новый номер телефона
    name = input("Contact name: ")
    phone = input("Phone: ")
    phone_type = input("Type home/work/mobile: ")

    conn = get_connection()
    cur = conn.cursor()

    # Здесь вызывается stored procedure add_phone из PostgreSQL.
    # Она ищет контакт по имени и добавляет ему номер в таблицу phones.
    cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added!")


def search_contacts():
    # Пользователь вводит текст для поиска
    query = input("Search name/email/phone: ")

    conn = get_connection()
    cur = conn.cursor()

    # Здесь вызывается SQL-функция search_contacts.
    # Она ищет по имени, email, телефону и группе.
    cur.execute("SELECT * FROM search_contacts(%s);", (query,))
    rows = cur.fetchall()

    print("\nSEARCH RESULTS:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def filter_by_group():
    # Вводим название группы, например Family, Work, Friend
    group_name = input("Group name: ")

    conn = get_connection()
    cur = conn.cursor()

    # Здесь фильтрация контактов по группе.
    # ILIKE делает поиск без учёта регистра.
    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name ILIKE %s
        ORDER BY c.name;
    """, (group_name,))

    rows = cur.fetchall()

    print("\nCONTACTS IN GROUP:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def sort_contacts():
    # Меню выбора сортировки
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")

    choice = input("Choose: ")

    # Здесь выбирается поле, по которому будет сортировка
    if choice == "1":
        order_by = "c.name"
    elif choice == "2":
        order_by = "c.birthday"
    elif choice == "3":
        order_by = "c.created_at"
    else:
        print("Wrong choice")
        return

    conn = get_connection()
    cur = conn.cursor()

    # Здесь выводятся контакты с ORDER BY.
    # order_by выбирается выше через if/elif.
    cur.execute(f"""
        SELECT c.name, c.email, c.birthday, g.name, c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY {order_by};
    """)

    rows = cur.fetchall()

    print("\nSORTED CONTACTS:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def export_json():
    # Эта функция экспортирует все контакты в contacts.json
    conn = get_connection()
    cur = conn.cursor()

    # Сначала берём основные данные контакта и название группы
    cur.execute("""
        SELECT 
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id;
    """)

    contacts = []

    # Для каждого контакта отдельно берём все его телефоны из таблицы phones
    for contact_id, name, email, birthday, group_name in cur.fetchall():
        cur.execute("""
            SELECT phone, type
            FROM phones
            WHERE contact_id = %s;
        """, (contact_id,))

        phones = []

        # Здесь собирается список телефонов одного контакта
        for phone, phone_type in cur.fetchall():
            phones.append({
                "phone": phone,
                "type": phone_type
            })

        # Здесь собирается один полный контакт в формате dictionary
        contacts.append({
            "name": name,
            "email": email,
            "birthday": str(birthday),
            "group": group_name,
            "phones": phones
        })

    # Здесь данные сохраняются в файл contacts.json
    with open("contacts.json", "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4, ensure_ascii=False)

    cur.close()
    conn.close()

    print("Exported to contacts.json")


def import_json():
    # Открываем contacts.json и читаем список контактов
    with open("contacts.json", "r", encoding="utf-8") as file:
        contacts = json.load(file)

    conn = get_connection()
    cur = conn.cursor()

    for contact in contacts:
        name = contact["name"]

        # Проверяем, существует ли контакт с таким именем
        cur.execute("SELECT id FROM contacts WHERE name = %s;", (name,))
        existing = cur.fetchone()

        if existing:
            # Если контакт уже есть, пользователь выбирает: skip или overwrite
            answer = input(f"{name} already exists. skip or overwrite? ")

            if answer == "skip":
                continue

            if answer == "overwrite":
                contact_id = existing[0]

                # Создаём группу, если её нет
                cur.execute("""
                    INSERT INTO groups(name)
                    VALUES (%s)
                    ON CONFLICT(name) DO NOTHING;
                """, (contact["group"],))

                # Получаем id группы
                cur.execute("SELECT id FROM groups WHERE name = %s;", (contact["group"],))
                group_id = cur.fetchone()[0]

                # Обновляем данные уже существующего контакта
                cur.execute("""
                    UPDATE contacts
                    SET email = %s,
                        birthday = %s,
                        group_id = %s
                    WHERE id = %s;
                """, (contact["email"], contact["birthday"], group_id, contact_id))

                # Удаляем старые телефоны, чтобы потом вставить новые из JSON
                cur.execute("DELETE FROM phones WHERE contact_id = %s;", (contact_id,))

        else:
            # Если контакта нет, создаём группу
            cur.execute("""
                INSERT INTO groups(name)
                VALUES (%s)
                ON CONFLICT(name) DO NOTHING;
            """, (contact["group"],))

            # Получаем id группы
            cur.execute("SELECT id FROM groups WHERE name = %s;", (contact["group"],))
            group_id = cur.fetchone()[0]

            # Создаём новый контакт и сразу получаем его id через RETURNING
            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (contact["name"], contact["email"], contact["birthday"], group_id))

            contact_id = cur.fetchone()[0]

        # Здесь добавляются все телефоны контакта из JSON
        for phone in contact["phones"]:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s);
            """, (contact_id, phone["phone"], phone["type"]))

    conn.commit()
    cur.close()
    conn.close()

    print("Imported from JSON")


def import_csv():
    # Эта функция импортирует данные из contacts.csv
    conn = get_connection()
    cur = conn.cursor()

    # DictReader читает CSV по названиям колонок:
    # name,email,birthday,group,phone,phone_type
    with open("contacts.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Достаём значения из каждой строки CSV
            name = row["name"]
            email = row["email"]
            birthday = row["birthday"]
            group_name = row["group"]
            phone = row["phone"]
            phone_type = row["phone_type"]

            # Создаём группу, если её нет
            cur.execute("""
                INSERT INTO groups(name)
                VALUES (%s)
                ON CONFLICT(name) DO NOTHING;
            """, (group_name,))

            # Получаем id группы
            cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
            group_id = cur.fetchone()[0]

            # Добавляем контакт.
            # ON CONFLICT(name) DO NOTHING защищает от дубликатов имени.
            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT(name) DO NOTHING;
            """, (name, email, birthday, group_id))

            # Получаем id контакта, чтобы добавить ему телефон
            cur.execute("SELECT id FROM contacts WHERE name = %s;", (name,))
            contact_id = cur.fetchone()[0]

            # Добавляем телефон в отдельную таблицу phones.
            # Это показывает связь 1 контакт -> много телефонов.
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s);
            """, (contact_id, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Imported from CSV")


def move_to_group():
    # Пользователь вводит имя контакта и новую группу
    contact_name = input("Contact name: ")
    group_name = input("New group name: ")

    conn = get_connection()
    cur = conn.cursor()

    # Здесь вызывается stored procedure move_to_group.
    # Она создаёт группу, если её нет, и переносит контакт в эту группу.
    cur.execute("CALL move_to_group(%s, %s);", (contact_name, group_name))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact moved to group!")


def menu():
    # Главный консольный цикл программы.
    # Он постоянно показывает меню, пока пользователь не выберет 0.
    while True:
        print("\nPHONEBOOK MENU")
        print("1. Show contacts")
        print("2. Add contact")
        print("3. Add phone")
        print("4. Search contacts")
        print("5. Filter by group")
        print("6. Sort contacts")
        print("7. Export to JSON")
        print("8. Import from JSON")
        print("9. Import from CSV")
        print("10. Move contact to group")
        print("0. Exit")

        choice = input("Choose: ")

        # Здесь по выбранной цифре вызывается нужная функция
        if choice == "1":
            show_contacts()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            add_phone()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            filter_by_group()
        elif choice == "6":
            sort_contacts()
        elif choice == "7":
            export_json()
        elif choice == "8":
            import_json()
        elif choice == "9":
            import_csv()
        elif choice == "10":
            move_to_group()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Wrong choice")


# Запуск программы начинается здесь
menu()