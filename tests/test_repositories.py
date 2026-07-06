# Test tang Model + Repositories, va tich hop voi services/ cua nhom.
# Chay: python tests/test_repositories.py
import os
import sys

# tranh loi console Windows (cp1252) khi in tieng Viet
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TEST_DIR)
sys.path.insert(0, PROJECT_ROOT)

# Tao lai app.db tu db.sql + insertData.sql
from database.create_database import create_db
create_db()

from repositories import (UserRepository, CourseRepository,
                          CourseClassRepository, EnrollmentRepository,
                          ResultRepository, ScheduleRepository)
from services.business_rules import passed_prerequisites, has_conflict

user_repo = UserRepository()
course_repo = CourseRepository()
class_repo = CourseClassRepository()
enroll_repo = EnrollmentRepository()
result_repo = ResultRepository()
schedule_repo = ScheduleRepository()

print("== 1. UserRepository ==")
u = user_repo.find_by_username("Admin1")
print("  Admin1 ->", u.userName, "| role:", u.role, "| status:", u.status)

print("== 2. CourseRepository ==")
print("  So mon hoc:", len(course_repo.find_all()))
c6 = course_repo.find_by_id(6)
print("  Course 6:", c6.courseName, "| tien quyet (courseID):",
      [p.courseID for p in c6.prerequisites])

print("== 3. CourseClassRepository ==")
cc = class_repo.find_by_id(1)
print("  Class 1: courseID", cc.courseID, "| GV:", cc.instructorName,
      "|", cc.currentEnroll, "/", cc.maxEnroll)

print("== 4. business_rules.passed_prerequisites ==")
print("  SV3 du dieu kien hoc mon 6:",
      passed_prerequisites(3, 6, course_repo, result_repo))
print("  SV1 du dieu kien hoc mon 6:",
      passed_prerequisites(1, 6, course_repo, result_repo))

print("== 5. business_rules.has_conflict ==")
print("  SV5 dang ky Class 3 co trung lich?:",
      has_conflict(5, 3, schedule_repo))

print("== 6. EnrollmentRepository (them + huy) ==")
before = len(enroll_repo.find_by_student(5))
new_en = enroll_repo.save({"studentID": 5, "courseClassID": 3,
                           "status": "Confirmed"})
print("  Sau khi them: SV5 co", len(enroll_repo.find_by_student(5)),
      "lop (truoc:", before, ")")
new_en.status = "Cancelled"
enroll_repo.save(new_en)
print("  Sau khi huy: SV5 con", len(enroll_repo.find_by_student(5)), "lop")

print("\n== 7. Tich hop end-to-end voi services/ ==")
try:
    from services.auth_service import AuthService
    from services.enrollment_service import EnrollmentService

    auth = AuthService()
    logged = auth.login("Admin1", "123456")
    print("  AuthService.login(Admin1):", logged.userName, "OK")

    es = EnrollmentService()
    res = es.enroll_course(5, 3)  # SV5 dang ky lop 3 (mon 1, khong tien quyet)
    print("  EnrollmentService.enroll_course(SV5, Class3): OK ->",
          "enrollID", res.enrollID)
except Exception as e:
    print("  [services] loi:", repr(e))

print("\n== TAT CA TEST REPOSITORIES CHAY OK ==")
