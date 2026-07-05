# Model & Data Access Layer — Phi Hùng

Phần Model + DAO của hệ thống đăng ký môn học (nhóm 8).

## Cấu trúc

```
model/      các lớp thực thể theo Class Diagram
            (Person, Student, Lecturer, Administrator, Department,
             Course, CourseSection, Registration, Semester, Schedule)
dao/        các lớp truy xuất SQLite, mỗi bảng một DAO
test_dao.py chạy thử riêng phần này: python test_dao.py
```

DAO không tự tạo kết nối — nhận `conn` (kết nối SQLite) qua constructor.
Kết nối và schema thật do phần Database cung cấp; `test_dao.py` chỉ tạo
CSDL tạm trong bộ nhớ để test.

## Cách dùng (cho phần Service)

```python
from dao import StudentDAO, CourseDAO

student_dao = StudentDAO(conn)   # conn lấy từ phần Database
sv = student_dao.find_by_email("a@st.uni.edu.vn")
```

Service không viết SQL trực tiếp, chỉ gọi qua DAO.

## Mấy điểm cần lưu ý

- Kế thừa Person → mỗi lớp con một bảng riêng (students, lecturers, administrators).
- Môn tiên quyết là quan hệ nhiều-nhiều → bảng `course_prerequisites`.
  Xét điều kiện: so sánh `CourseDAO.get_prerequisite_ids()` với
  `RegistrationDAO.find_completed_course_ids()`.
- Trùng lịch: lấy lịch đã đăng ký bằng `ScheduleDAO.find_by_student_and_semester()`
  rồi so từng lịch bằng `Schedule.overlaps()`.
- Sĩ số: `increment_enrollment()` chỉ UPDATE khi `current_enrollment < max_capacity`
  nên không vượt sĩ số được; bảng registrations cần `UNIQUE(student_id, section_id)`
  để không đăng ký trùng lớp.
- Cột `password` lưu chuỗi đã hash (phần hash nằm bên Utilities).
