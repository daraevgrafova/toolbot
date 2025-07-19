import sqlite3

conn = sqlite3.connect("tools.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id TEXT UNIQUE,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    qr_code TEXT UNIQUE,
    location TEXT,
    assigned_to INTEGER,
    FOREIGN KEY (assigned_to) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS move_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_id INTEGER NOT NULL,
    from_location TEXT NOT NULL,
    to_location TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'new',
    requested_by INTEGER NOT NULL,
    FOREIGN KEY (tool_id) REFERENCES tools(id),
    FOREIGN KEY (requested_by) REFERENCES users(id)
)
""")

cursor.execute("""
INSERT OR IGNORE INTO users (telegram_id, name) VALUES (?, ?)
""", ("370064769", "Дара"))

cursor.execute("""
INSERT OR IGNORE INTO users (telegram_id, name) VALUES (?, ?)
""", ("111111111", "Тестовый"))

cursor.execute("SELECT id FROM users WHERE telegram_id = ?", ("370064769",))
dara_id = cursor.fetchone()[0]

cursor.execute("SELECT id FROM users WHERE telegram_id = ?", ("111111111",))
test_id = cursor.fetchone()[0]

cursor.execute("""
INSERT OR IGNORE INTO tools (name, qr_code, location, assigned_to)
VALUES (?, ?, ?, ?)
""", ("Перфоратор", "QR123", "Объект А", dara_id))

cursor.execute("""
INSERT OR IGNORE INTO tools (name, qr_code, location, assigned_to)
VALUES (?, ?, ?, ?)
""", ("Шуруповёрт", "QR456", "Объект Б", dara_id))

cursor.execute("""
INSERT OR IGNORE INTO tools (name, qr_code, location, assigned_to)
VALUES (?, ?, ?, ?)
""", ("Дрель", "QR789", "Склад", test_id))

cursor.execute("SELECT id FROM tools WHERE qr_code = 'QR123'")
tool1_id = cursor.fetchone()[0]

cursor.execute("SELECT id FROM tools WHERE qr_code = 'QR456'")
tool2_id = cursor.fetchone()[0]

cursor.execute("SELECT id FROM tools WHERE qr_code = 'QR789'")
tool3_id = cursor.fetchone()[0]

cursor.execute("""
INSERT OR IGNORE INTO move_requests (tool_id, from_location, to_location, status, requested_by)
VALUES (?, ?, ?, ?, ?)
""", (tool1_id, "Объект А", "Объект В", "new", dara_id))

cursor.execute("""
INSERT OR IGNORE INTO move_requests (tool_id, from_location, to_location, status, requested_by)
VALUES (?, ?, ?, ?, ?)
""", (tool2_id, "Объект Б", "Склад", "approved", dara_id))

cursor.execute("""
INSERT OR IGNORE INTO move_requests (tool_id, from_location, to_location, status, requested_by)
VALUES (?, ?, ?, ?, ?)
""", (tool3_id, "Склад", "Объект Г", "rejected", test_id))

conn.commit()
conn.close()

print("✅ База успешно инициализирована: пользователи, инструменты и заявки добавлены.")

import sqlite3

conn = sqlite3.connect("tools.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id TEXT UNIQUE,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    qr_code TEXT UNIQUE,
    location TEXT,
    assigned_to INTEGER,
    FOREIGN KEY (assigned_to) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS move_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_id INTEGER NOT NULL,
    from_location TEXT NOT NULL,
    to_location TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'new',
    requested_by INTEGER NOT NULL,
    FOREIGN KEY (tool_id) REFERENCES tools(id),
    FOREIGN KEY (requested_by) REFERENCES users(id)
)
""")

cursor.execute("""
INSERT OR IGNORE INTO users (telegram_id, name) VALUES (?, ?)
""", ("370064769", "Дара"))

cursor.execute("""
INSERT OR IGNORE INTO users (telegram_id, name) VALUES (?, ?)
""", ("111111111", "Тестовый"))

cursor.execute("SELECT id FROM users WHERE telegram_id = ?", ("370064769",))
dara_id = cursor.fetchone()[0]

cursor.execute("SELECT id FROM users WHERE telegram_id = ?", ("111111111",))
test_id = cursor.fetchone()[0]

cursor.execute("""
INSERT OR IGNORE INTO tools (name, qr_code, location, assigned_to)
VALUES (?, ?, ?, ?)
""", ("Перфоратор", "QR123", "Объект А", dara_id))

cursor.execute("""
INSERT OR IGNORE INTO tools (name, qr_code, location, assigned_to)
VALUES (?, ?, ?, ?)
""", ("Шуруповёрт", "QR456", "Объект Б", dara_id))

cursor.execute("""
INSERT OR IGNORE INTO tools (name, qr_code, location, assigned_to)
VALUES (?, ?, ?, ?)
""", ("Дрель", "QR789", "Склад", test_id))

cursor.execute("SELECT id FROM tools WHERE qr_code = 'QR123'")
tool1_id = cursor.fetchone()[0]

cursor.execute("SELECT id FROM tools WHERE qr_code = 'QR456'")
tool2_id = cursor.fetchone()[0]

cursor.execute("SELECT id FROM tools WHERE qr_code = 'QR789'")
tool3_id = cursor.fetchone()[0]

cursor.execute("""
INSERT OR IGNORE INTO move_requests (tool_id, from_location, to_location, status, requested_by)
VALUES (?, ?, ?, ?, ?)
""", (tool1_id, "Объект А", "Объект В", "new", dara_id))

cursor.execute("""
INSERT OR IGNORE INTO move_requests (tool_id, from_location, to_location, status, requested_by)
VALUES (?, ?, ?, ?, ?)
""", (tool2_id, "Объект Б", "Склад", "approved", dara_id))

cursor.execute("""
INSERT OR IGNORE INTO move_requests (tool_id, from_location, to_location, status, requested_by)
VALUES (?, ?, ?, ?, ?)
""", (tool3_id, "Склад", "Объект Г", "rejected", test_id))

conn.commit()
conn.close()

print("✅ База успешно инициализирована: пользователи, инструменты и заявки добавлены.")
