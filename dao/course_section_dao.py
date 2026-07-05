from dao.base_dao import BaseDAO
from model.course_section import CourseSection


def _row_to_section(row):
    if row is None:
        return None
    return CourseSection(row["section_id"], row["course_id"],
                         row["lecturer_id"], row["semester_id"],
                         row["max_capacity"], row["current_enrollment"],
                         row["room"])


class CourseSectionDAO(BaseDAO):

    def insert(self, lop):
        self.conn.execute(
            """INSERT INTO course_sections (section_id, course_id,
               lecturer_id, semester_id, max_capacity, current_enrollment,
               room) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (lop.section_id, lop.course_id, lop.lecturer_id, lop.semester_id,
             lop.max_capacity, lop.current_enrollment, lop.room))
        self.commit()

    def update(self, lop):
        self.conn.execute(
            """UPDATE course_sections SET course_id = ?, lecturer_id = ?,
               semester_id = ?, max_capacity = ?, current_enrollment = ?,
               room = ? WHERE section_id = ?""",
            (lop.course_id, lop.lecturer_id, lop.semester_id,
             lop.max_capacity, lop.current_enrollment, lop.room,
             lop.section_id))
        self.commit()

    def delete(self, section_id):
        self.conn.execute(
            "DELETE FROM course_sections WHERE section_id = ?", (section_id,))
        self.commit()

    def find_by_id(self, section_id):
        cur = self.conn.execute(
            "SELECT * FROM course_sections WHERE section_id = ?", (section_id,))
        return _row_to_section(cur.fetchone())

    def find_by_course(self, course_id):
        cur = self.conn.execute(
            "SELECT * FROM course_sections WHERE course_id = ?", (course_id,))
        return [_row_to_section(r) for r in cur.fetchall()]

    def find_by_semester(self, semester_id):
        cur = self.conn.execute(
            "SELECT * FROM course_sections WHERE semester_id = ?", (semester_id,))
        return [_row_to_section(r) for r in cur.fetchall()]

    def increment_enrollment(self, section_id):
        # chi tang duoc khi lop chua day
        cur = self.conn.execute(
            """UPDATE course_sections
               SET current_enrollment = current_enrollment + 1
               WHERE section_id = ? AND current_enrollment < max_capacity""",
            (section_id,))
        self.commit()
        return cur.rowcount > 0

    def decrement_enrollment(self, section_id):
        self.conn.execute(
            """UPDATE course_sections
               SET current_enrollment = current_enrollment - 1
               WHERE section_id = ? AND current_enrollment > 0""",
            (section_id,))
        self.commit()
