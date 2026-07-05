from dao.base_dao import BaseDAO
from model.user import User


def _row_to_user(row):
    if row is None:
        return None
    # DB (bang Users) khong co cot nationalID -> None
    return User(row["userID"], row["userName"], row["password"], row["sex"],
                None, row["role"], row["status"], row["createdDate"])


class UserDAO(BaseDAO):

    def insert(self, u):
        cur = self.conn.execute(
            """INSERT INTO Users (userName, password, role, sex, createdDate,
               status) VALUES (?, ?, ?, ?, ?, ?)""",
            (u.username, u.password, u.role, u.sex, u.created_date, u.status))
        self.commit()
        return cur.lastrowid  # userID tu tang

    def find_by_id(self, user_id):
        cur = self.conn.execute(
            "SELECT * FROM Users WHERE userID = ?", (user_id,))
        return _row_to_user(cur.fetchone())

    def find_by_username(self, username):
        cur = self.conn.execute(
            "SELECT * FROM Users WHERE userName = ?", (username,))
        return _row_to_user(cur.fetchone())

    def find_all(self):
        cur = self.conn.execute("SELECT * FROM Users ORDER BY userID")
        return [_row_to_user(r) for r in cur.fetchall()]

    def update_password(self, user_id, new_password):
        self.conn.execute(
            "UPDATE Users SET password = ? WHERE userID = ?",
            (new_password, user_id))
        self.commit()

    def update_status(self, user_id, status):
        self.conn.execute(
            "UPDATE Users SET status = ? WHERE userID = ?", (status, user_id))
        self.commit()
