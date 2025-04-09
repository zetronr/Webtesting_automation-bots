import os

db_path = "bot_actions.db"

if os.path.exists(db_path):
    os.remove(db_path)
    print("Database deleted successfully.")
else:
    print("Database file not found.")