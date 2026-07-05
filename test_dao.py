# Test rieng phan Model + DAO: python test_dao.py
# Dung CSDL SQLite tam trong bo nho, tao dung schema that (Database/db.sql).
import os
import sqlite3

from model import (User, Admin, Student, Course, CourseClass,
                   StudentResult, Enrollment, Schedule, Room, Building)
from dao import (UserDAO, AdminDAO, StudentDAO, CourseDAO, CourseClassDAO,
                 StudentResultDAO, EnrollmentDAO, ScheduleDAO, RoomDAO,
                 BuildingDAO)

# Doc schema that tu Database/db.sql
schema_path = os.path.join(os.path.dirname(__file__), "Database", "db.sql")
with open(schema_path, encoding="utf-8") as f:
    schema = f.read()

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.executescript(schema)

user_dao = UserDAO(conn)
admin_dao = AdminDAO(conn)
student_dao = StudentDAO(conn)
course_dao = CourseDAO(conn)
class_dao = CourseClassDAO(conn)
result_dao = StudentResultDAO(conn)
enroll_dao = EnrollmentDAO(conn)
schedule_dao = ScheduleDAO(conn)
room_dao = RoomDAO(conn)
building_dao = BuildingDAO(conn)

# ---- Tao tai khoan + sinh vien ----
uid = user_dao.insert(User(None, "sv_a", "123456", sex="Nam",
                           role="Student", status="Active",
                           created_date="2026-07-01"))
sid = student_dao.insert(Student(uid, "sv_a", "123456", None, "Nguyen Van A",
                                 "a@st.uni.edu.vn", "0903333444",
                                 "2005-01-01"))

# ---- Tao tai khoan admin ----
admin_uid = user_dao.insert(User(None, "admin1", "adminpw", role="Admin",
                                 status="Active", created_date="2026-07-01"))
admin_dao.insert(Admin(admin_uid, "admin1", "adminpw", None, "Tran Admin",
                       "0900000000"))

# ---- Dang nhap ----
sv = student_dao.find_by_email("a@st.uni.edu.vn")
print("Dang nhap SV:", sv.login("sv_a", "123456"))
print("Ho ten SV:", sv.student_name)

# ---- Giao vien (chua co model Teacher trong class diagram) ----
conn.execute("INSERT INTO Teacher (teacherName, phone) VALUES (?, ?)",
             ("Tran Van B", "0901111222"))
conn.commit()
teacher_id = conn.execute("SELECT teacherID FROM Teacher").fetchone()[0]

# ---- Mon hoc + tien quyet ----
oop_id = course_dao.insert(Course(None, "Lap trinh huong doi tuong", 4,
                                  "2026-1", "OPEN", 4000000))
cnpm_id = course_dao.insert(Course(None, "Cong nghe phan mem", 3,
                                   "2026-1", "OPEN", 3000000))
course_dao.add_prerequisite(cnpm_id, oop_id)
print("Tien quyet CNPM:", course_dao.get_prerequisite_ids(cnpm_id),
      "=> [", oop_id, "]")

# ---- Lop hoc phan ----
oop_class = class_dao.insert(CourseClass(None, oop_id, None, 50, 0),
                            teacher_id=teacher_id)
cnpm_class = class_dao.insert(CourseClass(None, cnpm_id, None, 2, 0),
                             teacher_id=teacher_id)
cc = class_dao.find_by_id(cnpm_class)
print("Giang vien lop CNPM:", cc.instructor_name, "| si so toi da:",
      cc.max_enroll)

# ---- Toa nha + phong ----
b_id = building_dao.insert(Building(None, "Toa B4"))
room_dao.insert(Room(None, b_id), room_name="B4.02")
r_code = room_dao.find_by_building(b_id)[0].room_code

# ---- Lich hoc ----
schedule_dao.insert(Schedule(None, oop_class, r_code, "Thu 2, tiet 1-3"))
schedule_dao.insert(Schedule(None, cnpm_class, r_code, "Thu 2, tiet 1-3"))

# ---- Xet tien quyet: SV chua hoc OOP ----
passed = result_dao.find_passed_course_ids(sid)
print("Da hoc dat:", passed, "-> du dieu kien hoc CNPM:", oop_id in passed)

# cho SV hoc dat OOP roi xet lai
result_dao.insert(StudentResult(None, sid, oop_id, 8.5, "Pass"))
passed = result_dao.find_passed_course_ids(sid)
print("Sau khi hoc OOP:", passed, "-> du dieu kien:", oop_id in passed)

# ---- Kiem tra trung lich ----
lich_cnpm = schedule_dao.find_by_course_class(cnpm_class)[0]
schedule_dao.insert(Schedule(None, oop_class, r_code, "Thu 2, tiet 1-3"))
# gia lap SV da dang ky OOP de co lich cu
enroll_dao.insert(Enrollment(None, sid, oop_class, "2026-07-05"))
lich_cu = schedule_dao.find_by_student(sid)
print("Trung lich:", any(lich_cnpm.conflict_with(l) for l in lich_cu))

# ---- Dang ky lop CNPM (con 2 cho) ----
if class_dao.increment_enroll(cnpm_class):
    enroll_dao.insert(Enrollment(None, sid, cnpm_class, "2026-07-06"))
    print("Dang ky CNPM thanh cong")

# ---- Lop day -> nguoi tiep theo bi tu choi ----
class_dao.increment_enroll(cnpm_class)  # cho thu 2
print("Dang ky khi lop day:", class_dao.increment_enroll(cnpm_class))
print("Si so:", class_dao.find_by_id(cnpm_class).get_current_enroll(), "/ 2")

# ---- Xem cac lop da dang ky roi huy ----
print("So lop da dang ky:", len(enroll_dao.find_by_student(sid)))
en = enroll_dao.find_active_enrollment(sid, cnpm_class)
enroll_dao.cancel(en.enroll_id)
class_dao.decrement_enroll(cnpm_class)
print("Sau khi huy con:", len(enroll_dao.find_by_student(sid)), "lop")

print("\n== TAT CA TEST CHAY OK ==")
conn.close()
