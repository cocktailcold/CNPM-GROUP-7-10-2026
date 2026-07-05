from dao.base_dao import BaseDAO
from model.course_class import CourseClass

# DB (coursesClass) khong co cot classID; instructorName lay tu bang Teacher
# (teacherID). Class diagram dung classID + instructorName truc tiep -> DAO
# doc instructor_name qua JOIN Teacher; class_id de None.
_SELECT = """SELECT cc.courseClassID, cc.courseID, cc.teacherID, cc.maxEnroll,
             cc.currentEnroll, cc.status, t.teacherName
             FROM coursesClass cc
             LEFT JOIN Teacher t ON cc.teacherID = t.teacherID"""


def _row_to_course_class(row):
    if row is None:
        return None
    return CourseClass(row["courseClassID"], row["courseID"], None,
                       row["maxEnroll"], row["currentEnroll"],
                       row["teacherName"])


class CourseClassDAO(BaseDAO):

    def insert(self, cc, teacher_id=None):
        cur = self.conn.execute(
            """INSERT INTO coursesClass (courseID, teacherID, maxEnroll,
               currentEnroll, status) VALUES (?, ?, ?, ?, ?)""",
            (cc.course_id, teacher_id, cc.max_enroll, cc.current_enroll, None))
        self.commit()
        return cur.lastrowid  # courseClassID tu tang

    def update(self, cc, teacher_id=None):
        self.conn.execute(
            """UPDATE coursesClass SET courseID = ?, teacherID = ?,
               maxEnroll = ?, currentEnroll = ? WHERE courseClassID = ?""",
            (cc.course_id, teacher_id, cc.max_enroll, cc.current_enroll,
             cc.course_class_id))
        self.commit()

    def delete(self, course_class_id):
        self.conn.execute(
            "DELETE FROM coursesClass WHERE courseClassID = ?",
            (course_class_id,))
        self.commit()

    def find_by_id(self, course_class_id):
        cur = self.conn.execute(_SELECT + " WHERE cc.courseClassID = ?",
                                (course_class_id,))
        return _row_to_course_class(cur.fetchone())

    def find_by_course(self, course_id):
        cur = self.conn.execute(_SELECT + " WHERE cc.courseID = ?",
                                (course_id,))
        return [_row_to_course_class(r) for r in cur.fetchall()]

    def find_all(self):
        cur = self.conn.execute(_SELECT + " ORDER BY cc.courseClassID")
        return [_row_to_course_class(r) for r in cur.fetchall()]

    def increment_enroll(self, course_class_id):
        # chi tang duoc khi lop chua day
        cur = self.conn.execute(
            """UPDATE coursesClass SET currentEnroll = currentEnroll + 1
               WHERE courseClassID = ? AND currentEnroll < maxEnroll""",
            (course_class_id,))
        self.commit()
        return cur.rowcount > 0

    def decrement_enroll(self, course_class_id):
        self.conn.execute(
            """UPDATE coursesClass SET currentEnroll = currentEnroll - 1
               WHERE courseClassID = ? AND currentEnroll > 0""",
            (course_class_id,))
        self.commit()
