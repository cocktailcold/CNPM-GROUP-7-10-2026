from repositories.course_repository import CourseRepository
from repositories.course_class_repository import CourseClassRepository

class CourseService:
    def __init__(self):
        self.course_repo = CourseRepository()
        self.class_repo = CourseClassRepository()

    def get_all_courses(self):
        return self.course_repo.find_all()

    def add_course(self, name, credit, fee):
        if not name or not name.strip():
            raise Exception("Course name is required")
        if credit <= 0:
            raise Exception("Credits must be greater than 0")
        if fee < 0:
            raise Exception("Fee must be a non-negative number")
        if self.course_repo.find_by_name(name) is not None:
            raise Exception("Course name already exists")
        return self.course_repo.save({"courseName": name, "credit": credit, "fee": fee})

    def create_class(self, course_id, instructor, max_enroll):
        course = self.course_repo.find_by_id(course_id)
        if course is None:
            raise Exception("Course not found")
        if not instructor or not instructor.strip():
            raise Exception("Instructor name is required")
        if max_enroll <= 0:
            raise Exception("Max enrollment must be greater than 0")
        return self.class_repo.save({
            "courseID": course_id, "instructorName": instructor,
            "maxEnroll": max_enroll, "currentEnroll": 0
        })

    def is_full(self, class_id):
        c = self.class_repo.find_by_id(class_id)
        if c is None:
            raise Exception("Class not found")
        return c.currentEnroll >= c.maxEnroll