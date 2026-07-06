from repositories.base_repository import BaseRepository, field
from model.course import Course


class CourseRepository(BaseRepository):

    def _to_course(self, row):
        if row is None:
            return None
        course = Course(row["courseID"], row["courseName"], row["credit"],
                        row["semester"], row["status"], row["fee"])
        course.prerequisites = self._load_prerequisites(course.courseID)
        return course

    def _load_prerequisites(self, course_id):
        rows = self.db.fetch_all(
            "SELECT prerequisiteID FROM hasPrerequisite WHERE courseID = ?",
            (course_id,))
        # tra ve list<Course> toi gian (chi can courseID cho business_rules)
        return [Course(courseID=r["prerequisiteID"]) for r in rows]

    def find_all(self):
        rows = self.db.fetch_all("SELECT * FROM Courses ORDER BY courseID")
        return [self._to_course(r) for r in rows]

    def find_by_id(self, course_id):
        row = self.db.fetch_one(
            "SELECT * FROM Courses WHERE courseID = ?", (course_id,))
        return self._to_course(row)

    def find_by_name(self, name):
        row = self.db.fetch_one(
            "SELECT * FROM Courses WHERE courseName = ?", (name,))
        return self._to_course(row)

    def save(self, course):
        course_id = field(course, "courseID")
        if course_id:  # cap nhat
            self.db.execute(
                """UPDATE Courses SET courseName = ?, credit = ?, semester = ?,
                   status = ?, fee = ? WHERE courseID = ?""",
                (field(course, "courseName"), field(course, "credit"),
                 field(course, "semester"), field(course, "status"),
                 field(course, "fee"), course_id))
            self.db.commit()
            return self.find_by_id(course_id)
        # them moi
        self.db.execute(
            """INSERT INTO Courses (courseName, credit, semester, status, fee)
               VALUES (?, ?, ?, ?, ?)""",
            (field(course, "courseName"), field(course, "credit"),
             field(course, "semester"), field(course, "status", "Active"),
             field(course, "fee")))
        self.db.commit()
        return self.find_by_id(self._last_id())

    def add_prerequisite(self, course_id, prerequisite_id):
        self.db.execute(
            "INSERT INTO hasPrerequisite (courseID, prerequisiteID) VALUES (?, ?)",
            (course_id, prerequisite_id))
        self.db.commit()
