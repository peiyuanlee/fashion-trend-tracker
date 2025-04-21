import sqlite3
import os

connection = sqlite3.connect("./db/fashion_trends.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM trends WHERE variable = 'y2k fashion' ORDER BY popularity DESC LIMIT 5")
print(cursor.fetchall())
