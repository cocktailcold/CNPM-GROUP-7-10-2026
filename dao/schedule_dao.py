from dao.base_dao import BaseDAO
from model.schedule import Schedule

# Class diagram: Schedule co thuoc tinh "time". DB (bang Schedule) luu thoi
# gian o cot "session" (con startDate/endDate de trong) -> map time <-> session.


def _row_to_schedule(row):
    if row is None:
        return None
    return Schedule(row["scheduleID"], row["courseClassID"], row["roomCode"],
                    row["session"])


class ScheduleDAO(BaseDAO):

    def insert(self, sch):
        cur = self.conn.execute(
            """INSERT INTO Schedule (courseClassID, roomCode, startDate,
               endDate, session) VALUES (?, ?, ?, ?, ?)""",
            (sch.course_class_id, sch.room_code, None, None, sch.time))
        self.commit()
        return cur.lastrowid  # scheduleID tu tang

    def delete_by_course_class(self, course_class_id):
        self.conn.execute(
            "DELETE FROM Schedule WHERE courseClassID = ?", (course_class_id,))
        self.commit()

    def find_by_course_class(self, course_class_id):
        cur = self.conn.execute(
            "SELECT * FROM Schedule WHERE courseClassID = ?",
            (course_class_id,))
        return [_row_to_schedule(r) for r in cur.fetchall()]

    def find_by_student(self, student_id):
        # lich hoc cua tat ca lop ma sinh vien da dang ky
        cur = self.conn.execute(
            """SELECT s.* FROM Schedule s
               JOIN Enrollment e ON e.courseClassID = s.courseClassID
               WHERE e.studentID = ?""",
            (student_id,))
        return [_row_to_schedule(r) for r in cur.fetchall()]
