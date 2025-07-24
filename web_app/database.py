import sqlite3

def create_table():
    conn = sqlite3.connect("bot_actions.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_name TEXT NOT NULL,
            xpath TEXT NOT NULL,
            action_type TEXT NOT NULL,
            url TEXT NULL,
            insert_value TEXT NULL,
            insert_file TEXT NULL,
            methode TEXT NULL,
            bytext TEXT NULL,
            byindex TEXT NULL
        )
    ''')

    


    

if __name__ == "__main__":
    create_table()
    print("Database dan tabel berhasil dibuat!")