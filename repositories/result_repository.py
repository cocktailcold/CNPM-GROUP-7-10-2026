from repositories.base_repository import BaseRepository, field
from model.result import Result


def _to_result(row):
    if row is None:
        return None
    return Result(row["resultID"], row["studentID"], row["courseID"],
                  row["gpa"], row["status"])


class ResultRepository(BaseRepository):

    def find_by_student(self, student_id):
        rows = self.db.fetch_all(
            "SELECT * FROM studentResult WHERE studentID = ?", (student_id,))
        return [_to_result(r) for r in rows]

    def find_by_student_and_course(self, student_id, course_id):
        row = self.db.fetch_one(
            """SELECT * FROM studentResult
               WHERE studentID = ? AND courseID = ?""",
            (student_id, course_id))
        return _to_result(row)

    def save(self, result):
        result_id = field(result, "resultID")
        if result_id:
            self.db.execute(
                """UPDATE studentResult SET gpa = ?, status = ?
                   WHERE resultID = ?""",
                (field(result, "gpa"), field(result, "status"), result_id))
            self.db.commit()
            return self.find_by_student_and_course(
                field(result, "studentID"), field(result, "courseID"))
        self.db.execute(
            """INSERT INTO studentResult (studentID, courseID, gpa, status)
               VALUES (?, ?, ?, ?)""",
            (field(result, "studentID"), field(result, "courseID"),
             field(result, "gpa"), field(result, "status")))
        self.db.commit()
        return self.find_by_student_and_course(
            field(result, "studentID"), field(result, "courseID"))
