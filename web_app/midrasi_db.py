import sqlite3

def migrate_database():
    conn = sqlite3.connect("bot_actions.db")
    cursor = conn.cursor()

    # Ganti nama tabel lama jika ada
    cursor.execute("ALTER TABLE actions RENAME TO actions_old")

    # Buat tabel baru dengan skema yang diperbarui
    cursor.execute('''
        CREATE TABLE actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_name TEXT NOT NULL,
            xpath TEXT NOT NULL,
            action_type TEXT NOT NULL,
            url TEXT NULL,
            insert_value TEXT NULL,
            insert_file TEXT NULL,  -- Sekarang insert_file hanya menyimpan path
            methode TEXT NULL,
            bytext TEXT NULL,
            byindex TEXT NULL
        )
    ''')

    # Pindahkan data dari tabel lama ke tabel baru
    cursor.execute('''
        INSERT INTO actions (id, action_name, xpath, action_type, url, insert_value, methode, bytext, byindex)
        SELECT id, action_name, xpath, action_type, url, insert_value, methode, bytext, byindex FROM actions_old
    ''')

    # Hapus tabel lama setelah data berhasil dipindahkan
    cursor.execute("DROP TABLE actions_old")

    conn.commit()
    conn.close()
    print("Migrasi database selesai!")

if __name__ == "__main__":
    migrate_database()
