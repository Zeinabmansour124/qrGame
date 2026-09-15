import sqlite3

conn = sqlite3.connect("database.db")
with open (r"qrChallenge\schema.sql", "r") as f:
    conn.executescript(f.read())
conn.close()
print("Base créée avec succès.")