import sqlite3

conn = sqlite3.connect("parts.db")
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT PartDescription FROM parts")
parts = cursor.fetchall()

print("Unique parts:")
for part in parts:
    print(part[0])

conn.close()
