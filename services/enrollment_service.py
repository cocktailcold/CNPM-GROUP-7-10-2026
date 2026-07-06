from repositories.enrollment_repository import EnrollmentRepository
from repositories.course_class_repository import CourseClassRepository
from repositories.course_repository import CourseRepository
from repositories.result_repository import ResultRepository
from repositories.schedule_repository import ScheduleRepository
from services.business_rules import missing_prerequisites, has_conflict

class EnrollmentService:
    def __init__(self):
        self.enrollment_repo = EnrollmentRepository()
        self.class_repo = CourseClassRepository()
        self.course_repo = CourseRepository()
        self.result_repo = ResultRepository()
        self.schedule_repo = ScheduleRepository()

    def enroll_course(self, student_id, class_id):
        existing = self.enrollment_repo.find_by_student_and_class(student_id, class_id)
        if existing is not None and existing.status == "Confirmed":
            raise Exception("You are already enrolled in this class")

        course_class = self.class_repo.find_by_id(class_id)
        if course_class is None:
            raise Exception("Class not found")

        if course_class.currentEnroll >= course_class.maxEnroll:
            raise Exception("This class is full")

        missing = missing_prerequisites(
            student_id, course_class.courseID, self.course_repo, self.result_repo
        )
        if missing:
            names = ", ".join(p.courseName or str(p.courseID) for p in missing)
            raise Exception(f"Prerequisite not met: {names}")

        if has_conflict(student_id, class_id, self.schedule_repo):
            raise Exception("Schedule conflict detected")

        course_class.currentEnroll += 1
        self.class_repo.save(course_class)
        return self.enrollment_repo.save({
            "studentID": student_id, "courseClassID": class_id, "status": "Confirmed"
        })

    def cancel_enrollment(self, enrollment_id):
        e = self.enrollment_repo.find_by_id(enrollment_id)
        if e is None:
            raise Exception("Enrollment not found")
        if e.status == "Cancelled":
            raise Exception("This enrollment has already been cancelled")

        e.status = "Cancelled"
        course_class = self.class_repo.find_by_id(e.courseClassID)
        course_class.currentEnroll = max(0, course_class.currentEnroll - 1)
        self.class_repo.save(course_class)
        return self.enrollment_repo.save(e)
