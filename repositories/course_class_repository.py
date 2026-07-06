from repositories.base_repository import BaseRepository, field
from model.course_class import CourseClass

# coursesClass luu teacherID (FK Teacher). Doc instructorName qua JOIN Teacher;
# khi them moi thi tao ban ghi Teacher tu instructorName roi lay teacherID.
_SELECT = """SELECT cc.courseClassID, cc.courseID, cc.maxEnroll,
             cc.currentEnroll, cc.status, t.teacherName AS instructorName
             FROM coursesClass cc
             LEFT JOIN Teacher t ON cc.teacherID = t.teacherID"""


def _to_class(row):
    if row is None:
        return None
    return CourseClass(row["courseClassID"], row["courseID"],
                       row["instructorName"], row["maxEnroll"],
                       row["currentEnroll"], row["status"])


class CourseClassRepository(BaseRepository):

    def find_by_id(self, class_id):
        row = self.db.fetch_one(
            _SELECT + " WHERE cc.courseClassID = ?", (class_id,))
        return _to_class(row)

    def find_by_course(self, course_id):
        rows = self.db.fetch_all(
            _SELECT + " WHERE cc.courseID = ?", (course_id,))
        return [_to_class(r) for r in rows]

    def find_all(self):
        rows = self.db.fetch_all(_SELECT + " ORDER BY cc.courseClassID")
        return [_to_class(r) for r in rows]

    def _teacher_id_for(self, instructor_name):
        if not instructor_name:
            return None
        self.db.execute(
            "INSERT INTO Teacher (teacherName, phone) VALUES (?, NULL)",
            (instructor_name,))
        self.db.commit()
        return self._last_id()

    def save(self, course_class):
        class_id = field(course_class, "courseClassID")
        if class_id:  # cap nhat (vd currentEnroll thay doi)
            self.db.execute(
                """UPDATE coursesClass SET courseID = ?, maxEnroll = ?,
                   currentEnroll = ?, status = ? WHERE courseClassID = ?""",
                (field(course_class, "courseID"),
                 field(course_class, "maxEnroll"),
                 field(course_class, "currentEnroll"),
                 field(course_class, "status", "Open"), class_id))
            self.db.commit()
            return self.find_by_id(class_id)
        # them moi
        teacher_id = self._teacher_id_for(field(course_class, "instructorName"))
        self.db.execute(
            """INSERT INTO coursesClass (courseID, teacherID, maxEnroll,
               currentEnroll, status) VALUES (?, ?, ?, ?, ?)""",
            (field(course_class, "courseID"), teacher_id,
             field(course_class, "maxEnroll"),
             field(course_class, "currentEnroll", 0),
             field(course_class, "status", "Open")))
        self.db.commit()
        return self.find_by_id(self._last_id())
