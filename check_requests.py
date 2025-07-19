import sqlite3

conn = sqlite3.connect("tools.db")
cursor = conn.cursor()

print("📦 Заявки на перемещение:")

cursor.execute("SELECT * FROM move_requests ORDER BY id DESC")
requests = cursor.fetchall()

if not requests:
    print("❌ Нет заявок.")
else:
    for row in requests:
        request_id = row[0]
        tool_id = row[1]
        from_location = row[2]
        to_location = row[3]
        user_id = row[4]
        status = row[5]

        print(f"📄 Заявка №{request_id} | Инструмент ID: {tool_id} | Из: {from_location} → В: {to_location} | "
              f"Пользователь ID: {user_id} | Статус: {status}")

conn.close()