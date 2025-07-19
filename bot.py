import sqlite3
import xml.etree.ElementTree as ET
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F
from aiogram import types
from aiogram.types import FSInputFile
import asyncio
from pyzbar.pyzbar import decode
from PIL import Image
import io


BOT_TOKEN = "8028617164:AAFDdWdS0q_23NfFsvDoPNoqahtW4i4ffmY"

from aiogram.client.default import DefaultBotProperties

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("Привет! Я бот учёта инструментов 🛠")

@dp.message(F.text == "/inventory")
async def inventory_handler(message: Message):
    conn = sqlite3.connect("tools.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (str(message.from_user.id),))
    user = cursor.fetchone()

    if not user:
        await message.answer("Ты не зарегистрирован в базе 🤷‍♀️")
        conn.close()
        return

    user_id = user[0]

    cursor.execute("SELECT name, location FROM tools WHERE assigned_to = ?", (user_id,))
    tools = cursor.fetchall()
    conn.close()

    if not tools:
        await message.answer("За тобой пока не закреплено ни одного инструмента.")
    else:
        text = "<b>🔧 Твои инструменты:</b>\n"
        for name, location in tools:
            text += f"• {name} — {location}\n"
        await message.answer(text)

@dp.message(F.photo)
async def scan_qr_handler(message: Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path
    file_bytes = await bot.download_file(file_path)

    image = Image.open(io.BytesIO(file_bytes.read()))
    decoded = decode(image)

    if not decoded:
        await message.answer("QR-код не найден 🤷‍♀️")
        return

    qr_data = decoded[0].data.decode("utf-8")

    conn = sqlite3.connect("tools.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, location FROM tools WHERE qr_code = ?", (qr_data,))
    result = cursor.fetchone()
    conn.close()

    if result:
        name, location = result
        await message.answer(f"🛠 Найден инструмент:\n<b>{name}</b> — {location}")
    else:
        await message.answer(f"QR: <code>{qr_data}</code>\nИнструмент не найден в базе.")

@dp.message(F.text.startswith("/move_request"))
async def move_request_handler(message: Message):
    parts = message.text.strip().split()

    if len(parts) < 3:
        await message.answer("Формат команды:\n<code>/move_request QR123 Новое_место</code>")
        return

    qr_code = parts[1]
    new_location = " ".join(parts[2:])

    conn = sqlite3.connect("tools.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, location FROM tools WHERE qr_code = ?", (qr_code,))
    tool = cursor.fetchone()

    if not tool:
        await message.answer("Инструмент с таким QR не найден.")
        conn.close()
        return

    tool_id, current_location = tool

    cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (str(message.from_user.id),))
    user = cursor.fetchone()

    if not user:
        await message.answer("Ты не зарегистрирован в базе.")
        conn.close()
        return

    user_id = user[0]

    cursor.execute("""
        INSERT INTO move_requests (tool_id, from_location, to_location, requested_by, status)
        VALUES (?, ?, ?, ?, 'new')
    """, (tool_id, current_location, new_location, user_id))

    conn.commit()
    conn.close()

    await message.answer(f"✅ Заявка на перемещение инструмента создана:\n"
                         f"<b>QR:</b> {qr_code}\n"
                         f"<b>Куда:</b> {new_location}")
    
@dp.message(F.text == "/my_requests")
async def my_requests_handler(message: Message):
    conn = sqlite3.connect("tools.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (str(message.from_user.id),))
    user = cursor.fetchone()

    if not user:
        await message.answer("Ты не зарегистрирован в базе.")
        conn.close()
        return

    user_id = user[0]

    cursor.execute("""
        SELECT r.id, t.name, r.from_location, r.to_location, r.status
        FROM move_requests r
        JOIN tools t ON r.tool_id = t.id
        WHERE r.requested_by = ?
        ORDER BY r.id DESC
    """, (user_id,))
    
    requests = cursor.fetchall()
    conn.close()

    if not requests:
        await message.answer("У тебя пока нет заявок на перемещение.")
    else:
        text = "<b>📋 Твои заявки:</b>\n\n"
        for r_id, tool_name, from_loc, to_loc, status in requests:
            text += f"🧾 <b>Заявка №{r_id}</b>\n🔧 {tool_name}\n📍 Из: {from_loc}\n📦 В: {to_loc}\n🛈 Статус: <i>{status}</i>\n\n"
        await message.answer(text)

@dp.message(F.text.startswith("/approve"))
async def approve_handler(message: Message):
    parts = message.text.strip().split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Формат команды: /approve <ID заявки>")
        return

    request_id = int(parts[1])

    conn = sqlite3.connect("tools.db")
    cursor = conn.cursor()

    cursor.execute("SELECT tool_id, to_location FROM move_requests WHERE id = ? AND status = 'new'", (request_id,))
    data = cursor.fetchone()

    if not data:
        await message.answer("Заявка не найдена или уже обработана.")
        conn.close()
        return

    tool_id, new_location = data

    cursor.execute("UPDATE move_requests SET status = 'approved' WHERE id = ?", (request_id,))
    cursor.execute("UPDATE tools SET location = ? WHERE id = ?", (new_location, tool_id))

    conn.commit()
    conn.close()

    await message.answer(f"✅ Заявка №{request_id} одобрена. Инструмент перемещён в <b>{new_location}</b>")

@dp.message(F.text.startswith("/reject"))
async def reject_request(message: Message):
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("❗ Формат: /reject <id заявки>")
        return

    request_id = int(parts[1])
    conn = sqlite3.connect("tools.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM move_requests WHERE id = ? AND status = 'new'", (request_id,))
    if not cursor.fetchone():
        await message.answer("⚠️ Заявка не найдена или уже обработана.")
        conn.close()
        return

    cursor.execute("UPDATE move_requests SET status = 'rejected' WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()

    await message.answer(f"⛔ Заявка №{request_id} отклонена.")

@dp.message(F.text == "/export_requests")
async def export_requests_handler(message: types.Message):
    try:
        conn = sqlite3.connect("tools.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT r.id, t.name, r.from_location, r.to_location, r.status, u.name
            FROM move_requests r
            JOIN tools t ON r.tool_id = t.id
            JOIN users u ON r.requested_by = u.id
        """)
        rows = cursor.fetchall()
        conn.close()

        root = ET.Element("requests")
        for row in rows:
            request = ET.SubElement(root, "request")
            ET.SubElement(request, "id").text = str(row[0])
            ET.SubElement(request, "tool_name").text = row[1]
            ET.SubElement(request, "from").text = row[2]
            ET.SubElement(request, "to").text = row[3]
            ET.SubElement(request, "status").text = row[4]
            ET.SubElement(request, "requested_by").text = row[5]

        tree = ET.ElementTree(root)
        file_path = "requests_export.xml"
        tree.write(file_path, encoding="utf-8", xml_declaration=True)

        xml_file = FSInputFile(file_path)
        await message.answer_document(xml_file)

    except Exception as e:
        await message.answer(f"❌ Ошибка при экспорте: {e}")


async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
