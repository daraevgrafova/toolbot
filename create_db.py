import sqlite3

conn = sqlite3.connect("tools.db")
cursor = conn.cursor()

# Таблица пользователей
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id TEXT UNIQUE,
    name TEXT
)
""")

# Таблица инструментов
cursor.execute("""
CREATE TABLE IF NOT EXISTS tools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    qr_code TEXT UNIQUE NOT NULL,
    location TEXT,
    assigned_to INTEGER,
    FOREIGN KEY (assigned_to) REFERENCES users(id)
)
""")

# Таблица заявок
cursor.execute("""
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_id INTEGER,
    from_location TEXT,
    to_location TEXT,
    requested_by INTEGER,
    status TEXT CHECK(status IN ('new', 'approved', 'rejected')) DEFAULT 'new',
    FOREIGN KEY (tool_id) REFERENCES tools(id),
    FOREIGN KEY (requested_by) REFERENCES users(id)
)
""")

conn.commit()
conn.close()

print("✅ База данных создана (tools.db)")

import sqlite3

conn = sqlite3.connect("tools.db")
cursor = conn.cursor()

# Таблица пользователей
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id TEXT UNIQUE,
    name TEXT
)
""")

# Таблица инструментов
cursor.execute("""
CREATE TABLE IF NOT EXISTS tools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    qr_code TEXT UNIQUE NOT NULL,
    location TEXT,
    assigned_to INTEGER,
    FOREIGN KEY (assigned_to) REFERENCES users(id)
)
""")

# Таблица заявок
cursor.execute("""
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_id INTEGER,
    from_location TEXT,
    to_location TEXT,
    requested_by INTEGER,
    status TEXT CHECK(status IN ('new', 'approved', 'rejected')) DEFAULT 'new',
    FOREIGN KEY (tool_id) REFERENCES tools(id),
    FOREIGN KEY (requested_by) REFERENCES users(id)
)
""")

conn.commit()
conn.close()

print("✅ База данных создана (tools.db)")
