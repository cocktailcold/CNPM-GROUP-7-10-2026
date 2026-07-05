from dao.base_dao import BaseDAO
from model.admin import Admin

# Cac cot lay tu JOIN Admin + Users
_SELECT = """SELECT a.adminID, a.userID, a.name, a.phone,
             u.userName, u.password, u.role, u.sex, u.status, u.createdDate
             FROM Admin a JOIN Users u ON a.userID = u.userID"""


def _row_to_admin(row):
    if row is None:
        return None
    return Admin(row["userID"], row["userName"], row["password"],
                 row["adminID"], row["name"], row["phone"], row["sex"],
                 None, row["role"], row["status"], row["createdDate"])


class AdminDAO(BaseDAO):

    def insert(self, a):
        # tai khoan (Users) phai duoc tao truoc, o day chi them ban ghi Admin
        cur = self.conn.execute(
            "INSERT INTO Admin (userID, name, phone) VALUES (?, ?, ?)",
            (a.user_id, a.name, a.phone))
        self.commit()
        return cur.lastrowid  # adminID tu tang

    def find_by_id(self, admin_id):
        cur = self.conn.execute(_SELECT + " WHERE a.adminID = ?", (admin_id,))
        return _row_to_admin(cur.fetchone())

    def find_by_user_id(self, user_id):
        cur = self.conn.execute(_SELECT + " WHERE a.userID = ?", (user_id,))
        return _row_to_admin(cur.fetchone())

    def find_all(self):
        cur = self.conn.execute(_SELECT + " ORDER BY a.adminID")
        return [_row_to_admin(r) for r in cur.fetchall()]
