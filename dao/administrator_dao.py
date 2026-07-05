from dao.base_dao import BaseDAO
from model.administrator import Administrator


def _row_to_admin(row):
    if row is None:
        return None
    return Administrator(row["person_id"], row["full_name"], row["email"],
                         row["password"], row["phone"], row["admin_code"])


class AdministratorDAO(BaseDAO):

    def insert(self, ad):
        self.conn.execute(
            """INSERT INTO administrators (person_id, full_name, email,
               password, phone, admin_code) VALUES (?, ?, ?, ?, ?, ?)""",
            (ad.person_id, ad.full_name, ad.email, ad.password, ad.phone,
             ad.admin_code))
        self.commit()

    def find_by_id(self, person_id):
        cur = self.conn.execute(
            "SELECT * FROM administrators WHERE person_id = ?", (person_id,))
        return _row_to_admin(cur.fetchone())

    def find_by_email(self, email):
        cur = self.conn.execute(
            "SELECT * FROM administrators WHERE email = ?", (email,))
        return _row_to_admin(cur.fetchone())
