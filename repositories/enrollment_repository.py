from repositories.base_repository import BaseRepository, field
from model.enrollment import Enrollment

# db.sql khong co cot status -> quy uoc: con ban ghi = "Confirmed",
# huy (status "Cancelled") = xoa ban ghi.


def _to_enrollment(row):
    if row is None:
        return None
    return Enrollment(row["enrollID"], row["studentID"], row["courseClassID"],
                      row["enrollDate"], "Confirmed")


class EnrollmentRepository(BaseRepository):

    def find_by_id(self, enroll_id):
        row = self.db.fetch_one(
            "SELECT * FROM Enrollment WHERE enrollID = ?", (enroll_id,))
        return _to_enrollment(row)

    def find_by_student_and_class(self, student_id, class_id):
        row = self.db.fetch_one(
            """SELECT * FROM Enrollment
               WHERE studentID = ? AND courseClassID = ?""",
            (student_id, class_id))
        return _to_enrollment(row)

    def find_by_student(self, student_id):
        rows = self.db.fetch_all(
            "SELECT * FROM Enrollment WHERE studentID = ?", (student_id,))
        return [_to_enrollment(r) for r in rows]

    def save(self, enrollment):
        status = field(enrollment, "status", "Confirmed")
        enroll_id = field(enrollment, "enrollID")

        if status == "Cancelled" and enroll_id:
            # huy dang ky = xoa ban ghi (db.sql khong co cot status)
            self.db.execute(
                "DELETE FROM Enrollment WHERE enrollID = ?", (enroll_id,))
            self.db.commit()
            return None

        if enroll_id:  # da ton tai -> giu nguyen
            return self.find_by_id(enroll_id)

        # them moi
        self.db.execute(
            """INSERT INTO Enrollment (studentID, courseClassID, enrollDate)
               VALUES (?, ?, DATE('now'))""",
            (field(enrollment, "studentID"),
             field(enrollment, "courseClassID")))
        self.db.commit()
        return self.find_by_id(self._last_id())
