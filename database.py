import sqlite3

conn = sqlite3.connect("traffic.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS traffic_log(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    pedestrian_count INTEGER
)
""")

conn.commit()
conn.close()
print("Database Created Successfully")
