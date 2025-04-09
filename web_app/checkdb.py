import sqlite3

# Koneksi ke database
conn = sqlite3.connect("bot_actions.db")
cursor = conn.cursor()

# Ambil data dari tabel
cursor.execute("SELECT * FROM actions")
rows = cursor.fetchall()

# Tampilkan data
for row in rows:
    print(row)

# Menjalankan query untuk mendapatkan daftar tabel
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Mengambil semua hasil
tables = cursor.fetchall()

# Menampilkan nama-nama tabel
for table in tables:
    print(table[0])

# Menutup koneksi
conn.close()


