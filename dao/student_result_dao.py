from dao.base_dao import BaseDAO
from model.student_result import StudentResult


def _row_to_result(row):
    if row is None:
        return None
    return StudentResult(row["resultID"], row["studentID"], row["courseID"],
                         row["gpa"], row["status"])


class StudentResultDAO(BaseDAO):

    def insert(self, sr):
        cur = self.conn.execute(
            """INSERT INTO studentResult (studentID, courseID, gpa, status)
               VALUES (?, ?, ?, ?)""",
            (sr.student_id, sr.course_id, sr.gpa, sr.status))
        self.commit()
        return cur.lastrowid  # resultID tu tang

    def update(self, sr):
        self.conn.execute(
            """UPDATE studentResult SET gpa = ?, status = ?
               WHERE studentID = ? AND courseID = ?""",
            (sr.gpa, sr.status, sr.student_id, sr.course_id))
        self.commit()

    def find_by_id(self, result_id):
        cur = self.conn.execute(
            "SELECT * FROM studentResult WHERE resultID = ?", (result_id,))
        return _row_to_result(cur.fetchone())

    def find_by_student(self, student_id):
        cur = self.conn.execute(
            "SELECT * FROM studentResult WHERE studentID = ?", (student_id,))
        return [_row_to_result(r) for r in cur.fetchall()]

    def find_by_student_and_course(self, student_id, course_id):
        cur = self.conn.execute(
            """SELECT * FROM studentResult
               WHERE studentID = ? AND courseID = ?""",
            (student_id, course_id))
        return _row_to_result(cur.fetchone())

    def find_passed_course_ids(self, student_id):
        # cac mon sinh vien da hoc DAT (Pass), dung de xet tien quyet
        cur = self.conn.execute(
            """SELECT courseID FROM studentResult
               WHERE studentID = ? AND status = 'Pass'""",
            (student_id,))
        return [r["courseID"] for r in cur.fetchall()]
