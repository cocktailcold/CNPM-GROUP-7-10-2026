from dao.base_dao import BaseDAO
from model.registration import Registration


def _row_to_registration(row):
    if row is None:
        return None
    return Registration(row["registration_id"], row["student_id"],
                        row["section_id"], row["registration_date"],
                        row["status"], row["grade"])


class RegistrationDAO(BaseDAO):

    def insert(self, phieu):
        self.conn.execute(
            """INSERT INTO registrations (registration_id, student_id,
               section_id, registration_date, status, grade)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (phieu.registration_id, phieu.student_id, phieu.section_id,
             phieu.registration_date, phieu.status, phieu.grade))
        self.commit()

    def exists(self, student_id, section_id):
        cur = self.conn.execute(
            """SELECT COUNT(*) AS n FROM registrations
               WHERE student_id = ? AND section_id = ? AND status = ?""",
            (student_id, section_id, Registration.STATUS_REGISTERED))
        return cur.fetchone()["n"] > 0

    def cancel(self, registration_id):
        self.conn.execute(
            "UPDATE registrations SET status = ? WHERE registration_id = ?",
            (Registration.STATUS_CANCELLED, registration_id))
        self.commit()

    def find_by_id(self, registration_id):
        cur = self.conn.execute(
            "SELECT * FROM registrations WHERE registration_id = ?",
            (registration_id,))
        return _row_to_registration(cur.fetchone())

    def find_by_student(self, student_id):
        cur = self.conn.execute(
            "SELECT * FROM registrations WHERE student_id = ? AND status = ?",
            (student_id, Registration.STATUS_REGISTERED))
        return [_row_to_registration(r) for r in cur.fetchall()]

    def find_by_section(self, section_id):
        cur = self.conn.execute(
            "SELECT * FROM registrations WHERE section_id = ?", (section_id,))
        return [_row_to_registration(r) for r in cur.fetchall()]

    def find_active_registration(self, student_id, section_id):
        cur = self.conn.execute(
            """SELECT * FROM registrations
               WHERE student_id = ? AND section_id = ? AND status = ?""",
            (student_id, section_id, Registration.STATUS_REGISTERED))
        return _row_to_registration(cur.fetchone())

    def find_completed_course_ids(self, student_id):
        # cac mon sinh vien da hoc xong, dung de xet tien quyet
        cur = self.conn.execute(
            """SELECT DISTINCT cs.course_id FROM registrations r
               JOIN course_sections cs ON r.section_id = cs.section_id
               WHERE r.student_id = ? AND r.status = ?""",
            (student_id, Registration.STATUS_COMPLETED))
        return [r["course_id"] for r in cur.fetchall()]

    def update_grade(self, registration_id, grade):
        self.conn.execute(
            "UPDATE registrations SET grade = ?, status = ? WHERE registration_id = ?",
            (grade, Registration.STATUS_COMPLETED, registration_id))
        self.commit()
