from dao.base_dao import BaseDAO
from model.student import Student


def _row_to_student(row):
    if row is None:
        return None
    return Student(row["person_id"], row["full_name"], row["email"],
                   row["password"], row["phone"], row["student_code"],
                   row["major"], row["enrollment_year"], row["gpa"])


class StudentDAO(BaseDAO):

    def insert(self, s):
        self.conn.execute(
            """INSERT INTO students (person_id, full_name, email, password,
               phone, student_code, major, enrollment_year, gpa)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (s.person_id, s.full_name, s.email, s.password, s.phone,
             s.student_code, s.major, s.enrollment_year, s.gpa))
        self.commit()

    def update(self, s):
        self.conn.execute(
            """UPDATE students SET full_name = ?, email = ?, phone = ?,
               major = ?, enrollment_year = ?, gpa = ? WHERE person_id = ?""",
            (s.full_name, s.email, s.phone, s.major, s.enrollment_year,
             s.gpa, s.person_id))
        self.commit()

    def delete(self, person_id):
        self.conn.execute("DELETE FROM students WHERE person_id = ?",
                          (person_id,))
        self.commit()

    def find_by_id(self, person_id):
        cur = self.conn.execute(
            "SELECT * FROM students WHERE person_id = ?", (person_id,))
        return _row_to_student(cur.fetchone())

    def find_by_email(self, email):
        cur = self.conn.execute(
            "SELECT * FROM students WHERE email = ?", (email,))
        return _row_to_student(cur.fetchone())

    def find_by_student_code(self, code):
        cur = self.conn.execute(
            "SELECT * FROM students WHERE student_code = ?", (code,))
        return _row_to_student(cur.fetchone())

    def find_all(self):
        cur = self.conn.execute("SELECT * FROM students ORDER BY student_code")
        return [_row_to_student(r) for r in cur.fetchall()]

    def update_password(self, person_id, new_password):
        self.conn.execute(
            "UPDATE students SET password = ? WHERE person_id = ?",
            (new_password, person_id))
        self.commit()
