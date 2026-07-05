# Test rieng phan Model + DAO: python test_dao.py
# Dung CSDL tam trong bo nho. Ket noi va schema that do phan Database lam,
# o day chi tao bang toi thieu de test duoc cac DAO.
import sqlite3

from model import (Student, Department, Course, CourseSection,
                   Registration, Semester, Schedule)
from dao import (StudentDAO, DepartmentDAO, CourseDAO,
                 SemesterDAO, CourseSectionDAO, ScheduleDAO, RegistrationDAO)

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.executescript("""
CREATE TABLE departments (department_id TEXT PRIMARY KEY, department_name TEXT);
CREATE TABLE students (person_id TEXT PRIMARY KEY, full_name TEXT, email TEXT,
    password TEXT, phone TEXT, student_code TEXT, major TEXT,
    enrollment_year INTEGER, gpa REAL);
CREATE TABLE administrators (person_id TEXT PRIMARY KEY, full_name TEXT,
    email TEXT, password TEXT, phone TEXT, admin_code TEXT);
CREATE TABLE courses (course_id TEXT PRIMARY KEY, course_name TEXT,
    credits INTEGER, description TEXT, department_id TEXT);
CREATE TABLE course_prerequisites (course_id TEXT, prerequisite_id TEXT,
    PRIMARY KEY (course_id, prerequisite_id));
CREATE TABLE semesters (semester_id TEXT PRIMARY KEY, name TEXT,
    start_date TEXT, end_date TEXT, registration_deadline TEXT);
CREATE TABLE course_sections (section_id TEXT PRIMARY KEY, course_id TEXT,
    semester_id TEXT, max_capacity INTEGER,
    current_enrollment INTEGER DEFAULT 0, room TEXT);
CREATE TABLE schedules (schedule_id TEXT PRIMARY KEY, section_id TEXT,
    day_of_week TEXT, start_period INTEGER, end_period INTEGER, room TEXT);
CREATE TABLE registrations (registration_id TEXT PRIMARY KEY, student_id TEXT,
    section_id TEXT, registration_date TEXT, status TEXT DEFAULT 'REGISTERED',
    grade REAL, UNIQUE (student_id, section_id));
""")

student_dao = StudentDAO(conn)
department_dao = DepartmentDAO(conn)
course_dao = CourseDAO(conn)
semester_dao = SemesterDAO(conn)
section_dao = CourseSectionDAO(conn)
schedule_dao = ScheduleDAO(conn)
registration_dao = RegistrationDAO(conn)

# du lieu mau
department_dao.insert(Department("CNTT", "Cong nghe thong tin"))
student_dao.insert(Student("SV01", "Nguyen Van A", "a@st.uni.edu.vn",
                           "123456", "0903333444", "23520001",
                           "Ky thuat phan mem", 2023, 3.2))
semester_dao.insert(Semester("HK1", "Hoc ky 1 2026-2027",
                             "2026-09-01", "2027-01-15", "2026-08-25"))
course_dao.insert(Course("OOP", "Lap trinh huong doi tuong", 4, "", "CNTT"))
course_dao.insert(Course("CNPM", "Cong nghe phan mem", 3, "", "CNTT"))
course_dao.add_prerequisite("CNPM", "OOP")
section_dao.insert(CourseSection("OOP.1", "OOP", "HK1", 50, room="B1.10"))
section_dao.insert(CourseSection("CNPM.1", "CNPM", "HK1", 2, room="B4.02"))
schedule_dao.insert(Schedule("L01", "CNPM.1", "Mon", 1, 3, "B4.02"))

# dang nhap
sv = student_dao.find_by_email("a@st.uni.edu.vn")
print("Dang nhap:", sv.login("a@st.uni.edu.vn", "123456"))

# kiem tra tien quyet cua mon CNPM
prereqs = course_dao.get_prerequisite_ids("CNPM")
completed = registration_dao.find_completed_course_ids("SV01")
print("Tien quyet CNPM:", prereqs, "- da hoc xong:", completed)

# cho SV hoc xong OOP roi kiem tra lai
registration_dao.insert(Registration("R0", "SV01", "OOP.1", "2026-01-10"))
registration_dao.update_grade("R0", 8.5)
print("Sau khi hoc OOP:", registration_dao.find_completed_course_ids("SV01"))

# kiem tra trung lich
lich_moi = schedule_dao.find_by_section("CNPM.1")[0]
lich_cu = schedule_dao.find_by_student_and_semester("SV01", "HK1")
print("Trung lich:", any(lich_moi.overlaps(l) for l in lich_cu))

# dang ky lop CNPM.1
if section_dao.increment_enrollment("CNPM.1"):
    registration_dao.insert(Registration("R1", "SV01", "CNPM.1", "2026-07-03"))
    print("Dang ky CNPM.1 thanh cong")

# lop chi co 2 cho -> nguoi thu 3 phai bi tu choi
section_dao.increment_enrollment("CNPM.1")
print("Dang ky khi lop day:", section_dao.increment_enrollment("CNPM.1"))
print("Si so:", section_dao.find_by_id("CNPM.1").current_enrollment, "/ 2")

# xem danh sach da dang ky roi huy
for r in registration_dao.find_by_student("SV01"):
    print("Da dang ky:", r.section_id, r.status)
registration_dao.cancel("R1")
section_dao.decrement_enrollment("CNPM.1")
print("Sau khi huy con:", len(registration_dao.find_by_student("SV01")), "lop")

conn.close()
