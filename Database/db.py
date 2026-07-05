import sqlite3
import os

class Database:
    def __init__(self):
        # Tự động tạo file app.db nằm cùng thư mục với file db.py này
        db_path = os.path.join(os.path.dirname(__file__), "app.db")
        try:
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            
            # Kích hoạt tính năng khóa ngoại để bắt lỗi môn tiên quyết
            self.conn.execute("PRAGMA foreign_keys = ON;")
        except Exception as e:
            print(f"[DB ERROR] Kết nối thất bại: {e}")
            raise Exception(f"Database connection failed: {e}")

    def get_cursor(self):
        if not self.conn:
             raise Exception("Kết nối SQLite đã bị đóng!")
        return self.conn.cursor()

    def _convert_query(self, query):
        # Tự động chuyển đổi %s của MySQL thành ? của SQLite
        return query.replace('%s', '?')

    def execute(self, query, params=None):
        cursor = self.get_cursor()
        try:
            cursor.execute(self._convert_query(query), params or ())
            return cursor.rowcount
        except Exception as e:
            print(f"[EXECUTE ERROR] {e}")
            raise e
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        cursor = self.get_cursor()
        try:
            cursor.execute(self._convert_query(query), params or ())
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"[FETCH_ALL ERROR] {e}")
            return []
        finally:
            cursor.close()

    def fetch_one(self, query, params=None):
        cursor = self.get_cursor()
        try:
            cursor.execute(self._convert_query(query), params or ())
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"[FETCH_ONE ERROR] {e}")
            return None
        finally:
            cursor.close()

    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()

    def close(self):
        if self.conn:
            self.conn.close()