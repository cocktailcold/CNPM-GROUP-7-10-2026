import sqlite3
import os

def create_db():
    # Đường dẫn tới file app.db
    db_path = os.path.join(os.path.dirname(__file__), "app.db")

    # Nếu đã có database thì xóa để tạo mới
    if os.path.exists(db_path):
        os.remove(db_path)

    # Kết nối SQLite
    conn = sqlite3.connect(db_path)

    # Bật khóa ngoại
    conn.execute("PRAGMA foreign_keys = ON;")

    cursor = conn.cursor()

    # Đọc và chạy db.sql
    with open(
        os.path.join(os.path.dirname(__file__), "db.sql"),
        "r",
        encoding="utf-8"
    ) as f:
        cursor.executescript(f.read())

    # Đọc và chạy insertData.sql
    with open(
        os.path.join(os.path.dirname(__file__), "insertData.sql"),
        "r",
        encoding="utf-8"
    ) as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()

    print("Database created successfully!")

if __name__ == "__main__":
    create_db()