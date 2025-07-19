import sqlite3
import xml.etree.ElementTree as ET

# Подключение к БД
conn = sqlite3.connect("tools.db")
cursor = conn.cursor()

# Получаем все одобренные заявки
cursor.execute("""
    SELECT r.id, r.tool_id, r.from_location, r.to_location, r.status
    FROM requests r
    WHERE r.status = 'approved'
""")
requests = cursor.fetchall()

conn.close()

root = ET.Element("requests")

for req in requests:
    request_elem = ET.SubElement(root, "request", id=str(req[0]))

    tool_elem = ET.SubElement(request_elem, "tool_id")
    tool_elem.text = str(req[1])

    from_elem = ET.SubElement(request_elem, "from")
    from_elem.text = req[2]

    to_elem = ET.SubElement(request_elem, "to")
    to_elem.text = req[3]

    status_elem = ET.SubElement(request_elem, "status")
    status_elem.text = req[4]

tree = ET.ElementTree(root)
tree.write("requests_export.xml", encoding="utf-8", xml_declaration=True)

print("📦 Заявки выгружены в файл requests_export.xml")

import sqlite3
import xml.etree.ElementTree as ET

conn = sqlite3.connect("tools.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT r.id, r.tool_id, r.from_location, r.to_location, r.status
    FROM requests r
    WHERE r.status = 'approved'
""")
requests = cursor.fetchall()

conn.close()

root = ET.Element("requests")

for req in requests:
    request_elem = ET.SubElement(root, "request", id=str(req[0]))

    tool_elem = ET.SubElement(request_elem, "tool_id")
    tool_elem.text = str(req[1])

    from_elem = ET.SubElement(request_elem, "from")
    from_elem.text = req[2]

    to_elem = ET.SubElement(request_elem, "to")
    to_elem.text = req[3]

    status_elem = ET.SubElement(request_elem, "status")
    status_elem.text = req[4]

tree = ET.ElementTree(root)
tree.write("requests_export.xml", encoding="utf-8", xml_declaration=True)

print("📦 Заявки выгружены в файл requests_export.xml")

