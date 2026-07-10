# CNPM-GROUP-8

Hệ thống đăng ký học phần được triển khai bằng ngôn ngữ Python theo kiến trúc hướng đối tượng với cấu trúc Model / Repository / Service, kết hợp giao diện đồ họa trực quan sử dụng thư viện Tkinter.

## Run

```powershell
python main.py
```

## Demo Accounts

| Role | Username | Password |
| --- | --- | --- |
| Student | IT00000003 | Hung1003@ |
| Student | IT00000005 | Hien&2022! |
| Admin | Admin1 | 123456 |

## Main Functions

Student:
- Dành cho Sinh viên:
- Đăng nhập và tự động kiểm tra trạng thái hoạt động của tài khoản.
- Xem danh sách các lớp học phần hiện đang mở.
- Đăng ký lớp học phần (hệ thống tự động kiểm tra điều kiện môn tiên quyết, sĩ số tối đa, đăng ký trùng môn và trùng lịch học).
- Hủy lớp học phần đã đăng ký.
- Xem thời khóa biểu cá nhân chi tiết.
- Xem kết quả học tập (điểm GPA, trạng thái đạt/không đạt).
  
Admin:
- Xem danh sách toàn bộ môn học, lớp học phần và người dùng trong hệ thống.
- Thêm môn học mới vào hệ thống.
- Tạo lớp học phần mới cho một môn học sẵn có.
Manual test cases are drafted in `docs/TESTING_DOCUMENT_GROUP8.md`. Before final
submission, copy them into the official Testing Document Template from
Elearning 5.
