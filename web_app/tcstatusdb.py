import sqlite3

def create_statusTable():
    conn = sqlite3.connect("bot_actions.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS statusTable (
                     id INTEGER PRIMARY PRIMARY KEY AUTOINCREMENT,
                     testcasename TEXT NOT NULL,
                     status TEXT NOT NULL,
                     result BOOL
                   
                   
                   
                   ''')
    