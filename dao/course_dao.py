from dao.base_dao import BaseDAO
from model.course import Course


class CourseDAO(BaseDAO):

    def _row_to_course(self, row):
        if row is None:
            return None
        course = Course(row["course_id"], row["course_name"], row["credits"],
                        row["description"], row["department_id"])
        course.prerequisites = self.get_prerequisite_ids(course.course_id)
        return course

    def insert(self, c):
        self.conn.execute(
            """INSERT INTO courses (course_id, course_name, credits,
               description, department_id) VALUES (?, ?, ?, ?, ?)""",
            (c.course_id, c.course_name, c.credits, c.description,
             c.department_id))
        self.commit()

    def update(self, c):
        self.conn.execute(
            """UPDATE courses SET course_name = ?, credits = ?,
               description = ?, department_id = ? WHERE course_id = ?""",
            (c.course_name, c.credits, c.description, c.department_id,
             c.course_id))
        self.commit()

    def delete(self, course_id):
        self.conn.execute(
            "DELETE FROM course_prerequisites WHERE course_id = ? OR prerequisite_id = ?",
            (course_id, course_id))
        self.conn.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
        self.commit()

    def find_by_id(self, course_id):
        cur = self.conn.execute(
            "SELECT * FROM courses WHERE course_id = ?", (course_id,))
        return self._row_to_course(cur.fetchone())

    def find_all(self):
        cur = self.conn.execute("SELECT * FROM courses ORDER BY course_id")
        return [self._row_to_course(r) for r in cur.fetchall()]

    def find_by_department(self, department_id):
        cur = self.conn.execute(
            "SELECT * FROM courses WHERE department_id = ? ORDER BY course_id",
            (department_id,))
        return [self._row_to_course(r) for r in cur.fetchall()]

    def get_prerequisite_ids(self, course_id):
        cur = self.conn.execute(
            "SELECT prerequisite_id FROM course_prerequisites WHERE course_id = ?",
            (course_id,))
        return [r["prerequisite_id"] for r in cur.fetchall()]

    def add_prerequisite(self, course_id, prerequisite_id):
        self.conn.execute(
            "INSERT INTO course_prerequisites (course_id, prerequisite_id) VALUES (?, ?)",
            (course_id, prerequisite_id))
        self.commit()

    def remove_prerequisite(self, course_id, prerequisite_id):
        self.conn.execute(
            "DELETE FROM course_prerequisites WHERE course_id = ? AND prerequisite_id = ?",
            (course_id, prerequisite_id))
        self.commit()
