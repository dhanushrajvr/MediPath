import sqlite3

conn = sqlite3.connect("./database/app.db")

with open("./database/schema.sql", "r") as file:
    sql_script = file.read()

conn.executescript(sql_script)

conn.commit()
conn.close()