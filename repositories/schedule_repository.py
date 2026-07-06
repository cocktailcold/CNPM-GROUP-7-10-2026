from repositories.base_repository import BaseRepository
from model.schedule import Schedule

# db.sql luu thoi gian o cot "session" -> anh xa sang thuoc tinh "time".


def _to_schedule(row):
    if row is None:
        return None
    return Schedule(row["scheduleID"], row["courseClassID"], row["roomCode"],
                    row["session"], row["startDate"], row["endDate"])


class ScheduleRepository(BaseRepository):

    def find_by_class(self, class_id):
        rows = self.db.fetch_all(
            "SELECT * FROM Schedule WHERE courseClassID = ?", (class_id,))
        return [_to_schedule(r) for r in rows]

    def find_by_student(self, student_id):
        # lich hoc cua tat ca lop ma sinh vien da dang ky
        rows = self.db.fetch_all(
            """SELECT s.* FROM Schedule s
               JOIN Enrollment e ON e.courseClassID = s.courseClassID
               WHERE e.studentID = ?""",
            (student_id,))
        return [_to_schedule(r) for r in rows]
