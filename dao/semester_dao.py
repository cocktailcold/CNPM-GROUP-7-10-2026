from dao.base_dao import BaseDAO
from model.semester import Semester


def _row_to_semester(row):
    if row is None:
        return None
    return Semester(row["semester_id"], row["name"], row["start_date"],
                    row["end_date"], row["registration_deadline"])


class SemesterDAO(BaseDAO):

    def insert(self, hk):
        self.conn.execute(
            """INSERT INTO semesters (semester_id, name, start_date,
               end_date, registration_deadline) VALUES (?, ?, ?, ?, ?)""",
            (hk.semester_id, hk.name, hk.start_date, hk.end_date,
             hk.registration_deadline))
        self.commit()

    def find_by_id(self, semester_id):
        cur = self.conn.execute(
            "SELECT * FROM semesters WHERE semester_id = ?", (semester_id,))
        return _row_to_semester(cur.fetchone())

    def find_all(self):
        cur = self.conn.execute("SELECT * FROM semesters ORDER BY start_date")
        return [_row_to_semester(r) for r in cur.fetchall()]
