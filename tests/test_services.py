import unittest

from database.create_database import create_db
from repositories.course_class_repository import CourseClassRepository
from repositories.enrollment_repository import EnrollmentRepository
from services.auth_service import AuthService
from services.course_service import CourseService
from services.enrollment_service import EnrollmentService


class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        create_db()
        self.auth = AuthService()
        self.course_service = CourseService()
        self.enrollment_service = EnrollmentService()
        self.class_repo = CourseClassRepository()
        self.enroll_repo = EnrollmentRepository()

    def tearDown(self):
        repositories = [
            self.auth.user_repo,
            self.course_service.course_repo,
            self.course_service.class_repo,
            self.enrollment_service.enrollment_repo,
            self.enrollment_service.class_repo,
            self.enrollment_service.course_repo,
            self.enrollment_service.result_repo,
            self.enrollment_service.schedule_repo,
            self.class_repo,
            self.enroll_repo,
        ]
        for repo in repositories:
            repo.db.close()

    def test_student_login_success(self):
        user = self.auth.login("IT00000003", "Hung1003@")
        self.assertEqual(user.role, "Student")

    def test_login_rejects_wrong_password(self):
        with self.assertRaisesRegex(Exception, "Invalid username or password"):
            self.auth.login("IT00000003", "wrong-password")

    def test_forgot_password_resets_student_password(self):
        user = self.auth.verify_identity("IT00000003", "hungal1003@edu.com")
        self.auth.reset_password(user.userID, "NewPass123", "NewPass123")

        updated = self.auth.user_repo.find_by_id(user.userID)
        self.assertNotEqual(updated.password, "NewPass123")
        logged = self.auth.login("IT00000003", "NewPass123")
        self.assertEqual(logged.userID, user.userID)

    def test_forgot_password_rejects_wrong_email(self):
        with self.assertRaisesRegex(Exception, "Username or email does not exist"):
            self.auth.verify_identity("IT00000003", "wrong@edu.com")

    def test_forgot_password_requires_username_and_email(self):
        with self.assertRaisesRegex(Exception, "Username and email are required"):
            self.auth.verify_identity("", "hungal1003@edu.com")

    def test_reset_password_requires_matching_confirmation(self):
        user = self.auth.verify_identity("IT00000003", "hungal1003@edu.com")
        with self.assertRaisesRegex(Exception, "Passwords do not match"):
            self.auth.reset_password(user.userID, "NewPass123", "Different123")

    def test_reset_password_rejects_short_password(self):
        user = self.auth.verify_identity("IT00000003", "hungal1003@edu.com")
        with self.assertRaisesRegex(Exception, "New password must be at least 6 characters"):
            self.auth.reset_password(user.userID, "12345", "12345")

    def test_admin_can_add_course(self):
        course = self.course_service.add_course("AI Basics", 3, 5500000, "6")
        self.assertEqual(course.courseName, "AI Basics")
        self.assertEqual(course.semester, "6")

    def test_admin_can_create_class(self):
        course_class = self.course_service.create_class(1, "Demo Teacher", 40)
        self.assertEqual(course_class.courseID, 1)
        self.assertEqual(course_class.maxEnroll, 40)

    def test_enroll_rejects_missing_prerequisite(self):
        with self.assertRaisesRegex(Exception, "Prerequisite not met: Database Systems"):
            self.enrollment_service.enroll_course(1, 12)

    def test_enroll_rejects_duplicate_class(self):
        with self.assertRaisesRegex(Exception, "already enrolled"):
            self.enrollment_service.enroll_course(5, 7)

    def test_enroll_and_cancel_success(self):
        before = len(self.enroll_repo.find_by_student(5))
        enrollment = self.enrollment_service.enroll_course(5, 3)
        after_enroll = len(self.enroll_repo.find_by_student(5))
        self.assertEqual(after_enroll, before + 1)

        self.enrollment_service.cancel_enrollment(enrollment.enrollID)
        after_cancel = len(self.enroll_repo.find_by_student(5))
        self.assertEqual(after_cancel, before)


if __name__ == "__main__":
    unittest.main()
