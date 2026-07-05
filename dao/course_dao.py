from dao.base_dao import BaseDAO
from model.course import Course


class CourseDAO(BaseDAO):

    def _row_to_course(self, row):
        if row is None:
            return None
        course = Course(row["courseID"], row["courseName"], row["credit"],
                        row["semester"], row["status"], row["fee"])
        course.prerequisites = self.get_prerequisite_ids(course.course_id)
        return course

    def insert(self, c):
        cur = self.conn.execute(
            """INSERT INTO Courses (courseName, credit, semester, status, fee)
               VALUES (?, ?, ?, ?, ?)""",
            (c.course_name, c.credit, c.semester, c.status, c.fee))
        self.commit()
        return cur.lastrowid  # courseID tu tang

    def update(self, c):
        self.conn.execute(
            """UPDATE Courses SET courseName = ?, credit = ?, semester = ?,
               status = ?, fee = ? WHERE courseID = ?""",
            (c.course_name, c.credit, c.semester, c.status, c.fee,
             c.course_id))
        self.commit()

    def delete(self, course_id):
        self.conn.execute(
            "DELETE FROM hasPrerequisite WHERE courseID = ? OR prerequisiteID = ?",
            (course_id, course_id))
        self.conn.execute("DELETE FROM Courses WHERE courseID = ?", (course_id,))
        self.commit()

    def find_by_id(self, course_id):
        cur = self.conn.execute(
            "SELECT * FROM Courses WHERE courseID = ?", (course_id,))
        return self._row_to_course(cur.fetchone())

    def find_all(self):
        cur = self.conn.execute("SELECT * FROM Courses ORDER BY courseID")
        return [self._row_to_course(r) for r in cur.fetchall()]

    def get_prerequisite_ids(self, course_id):
        cur = self.conn.execute(
            "SELECT prerequisiteID FROM hasPrerequisite WHERE courseID = ?",
            (course_id,))
        return [r["prerequisiteID"] for r in cur.fetchall()]

    def add_prerequisite(self, course_id, prerequisite_id):
        self.conn.execute(
            "INSERT INTO hasPrerequisite (courseID, prerequisiteID) VALUES (?, ?)",
            (course_id, prerequisite_id))
        self.commit()

    def remove_prerequisite(self, course_id, prerequisite_id):
        self.conn.execute(
            "DELETE FROM hasPrerequisite WHERE courseID = ? AND prerequisiteID = ?",
            (course_id, prerequisite_id))
        self.commit()
