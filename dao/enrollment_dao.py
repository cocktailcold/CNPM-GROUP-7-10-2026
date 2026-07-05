from dao.base_dao import BaseDAO
from model.enrollment import Enrollment

# Luu y: bang Enrollment trong DB khong co cot status -> khi doc len status
# de mac dinh REGISTERED; huy dang ky = xoa ban ghi.


def _row_to_enrollment(row):
    if row is None:
        return None
    return Enrollment(row["enrollID"], row["studentID"], row["courseClassID"],
                      row["enrollDate"])


class EnrollmentDAO(BaseDAO):

    def insert(self, e):
        cur = self.conn.execute(
            """INSERT INTO Enrollment (studentID, courseClassID, enrollDate)
               VALUES (?, ?, ?)""",
            (e.student_id, e.course_class_id, e.enroll_date))
        self.commit()
        return cur.lastrowid  # enrollID tu tang

    def exists(self, student_id, course_class_id):
        cur = self.conn.execute(
            """SELECT COUNT(*) AS n FROM Enrollment
               WHERE studentID = ? AND courseClassID = ?""",
            (student_id, course_class_id))
        return cur.fetchone()["n"] > 0

    def cancel(self, enroll_id):
        # DB khong co cot status nen huy = xoa ban ghi
        self.conn.execute(
            "DELETE FROM Enrollment WHERE enrollID = ?", (enroll_id,))
        self.commit()

    def find_by_id(self, enroll_id):
        cur = self.conn.execute(
            "SELECT * FROM Enrollment WHERE enrollID = ?", (enroll_id,))
        return _row_to_enrollment(cur.fetchone())

    def find_by_student(self, student_id):
        cur = self.conn.execute(
            "SELECT * FROM Enrollment WHERE studentID = ?", (student_id,))
        return [_row_to_enrollment(r) for r in cur.fetchall()]

    def find_by_course_class(self, course_class_id):
        cur = self.conn.execute(
            "SELECT * FROM Enrollment WHERE courseClassID = ?",
            (course_class_id,))
        return [_row_to_enrollment(r) for r in cur.fetchall()]

    def find_active_enrollment(self, student_id, course_class_id):
        cur = self.conn.execute(
            """SELECT * FROM Enrollment
               WHERE studentID = ? AND courseClassID = ?""",
            (student_id, course_class_id))
        return _row_to_enrollment(cur.fetchone())
