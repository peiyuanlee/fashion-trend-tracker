import sqlite3
import os

print(os.path.abspath('./db/fashion_trends.db'))

connection = sqlite3.connect("./db/fashion_trends.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM trends LIMIT 5")
print(cursor.fetchall())
