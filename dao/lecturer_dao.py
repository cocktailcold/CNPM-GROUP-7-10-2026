from dao.base_dao import BaseDAO
from model.lecturer import Lecturer


def _row_to_lecturer(row):
    if row is None:
        return None
    return Lecturer(row["person_id"], row["full_name"], row["email"],
                    row["password"], row["phone"], row["lecturer_code"],
                    row["title"])


class LecturerDAO(BaseDAO):

    def insert(self, gv):
        self.conn.execute(
            """INSERT INTO lecturers (person_id, full_name, email, password,
               phone, lecturer_code, title) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (gv.person_id, gv.full_name, gv.email, gv.password, gv.phone,
             gv.lecturer_code, gv.title))
        self.commit()

    def find_by_id(self, person_id):
        cur = self.conn.execute(
            "SELECT * FROM lecturers WHERE person_id = ?", (person_id,))
        return _row_to_lecturer(cur.fetchone())

    def find_by_email(self, email):
        cur = self.conn.execute(
            "SELECT * FROM lecturers WHERE email = ?", (email,))
        return _row_to_lecturer(cur.fetchone())

    def find_all(self):
        cur = self.conn.execute("SELECT * FROM lecturers ORDER BY lecturer_code")
        return [_row_to_lecturer(r) for r in cur.fetchall()]
