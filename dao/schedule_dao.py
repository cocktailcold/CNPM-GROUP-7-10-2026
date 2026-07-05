from dao.base_dao import BaseDAO
from model.schedule import Schedule
from model.registration import Registration


def _row_to_schedule(row):
    if row is None:
        return None
    return Schedule(row["schedule_id"], row["section_id"],
                    row["day_of_week"], row["start_period"],
                    row["end_period"], row["room"])


class ScheduleDAO(BaseDAO):

    def insert(self, lich):
        self.conn.execute(
            """INSERT INTO schedules (schedule_id, section_id, day_of_week,
               start_period, end_period, room) VALUES (?, ?, ?, ?, ?, ?)""",
            (lich.schedule_id, lich.section_id, lich.day_of_week,
             lich.start_period, lich.end_period, lich.room))
        self.commit()

    def delete_by_section(self, section_id):
        self.conn.execute(
            "DELETE FROM schedules WHERE section_id = ?", (section_id,))
        self.commit()

    def find_by_section(self, section_id):
        cur = self.conn.execute(
            "SELECT * FROM schedules WHERE section_id = ?", (section_id,))
        return [_row_to_schedule(r) for r in cur.fetchall()]

    def find_by_student_and_semester(self, student_id, semester_id):
        # lich hoc cac lop sinh vien da dang ky trong hoc ky
        cur = self.conn.execute(
            """SELECT s.* FROM schedules s
               JOIN course_sections cs ON s.section_id = cs.section_id
               JOIN registrations r ON r.section_id = cs.section_id
               WHERE r.student_id = ? AND cs.semester_id = ? AND r.status = ?""",
            (student_id, semester_id, Registration.STATUS_REGISTERED))
        return [_row_to_schedule(r) for r in cur.fetchall()]
