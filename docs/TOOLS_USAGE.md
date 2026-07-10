# Sử dụng Công cụ (Tools Usage) 

Tài liệu này ghi lại các công cụ được áp dụng trong suốt quá trình lập trình và kiểm thử ứng dụng.

| Giai đoạn | Công cụ | Mục đích sử dụng | Minh chứng cụ thể |
| --- | --- | --- | --- |
| Lập trình | Python 3 | Ngôn ngữ lập trình chính của dự án | Các file/thư mục `main.py`, `model/`, `repositories/`, `services/` |
| Lập trình | Tkinter | Xây dựng giao diện đồ họa người dùng (GUI) | File `main.py` |
| Lập trình | SQLite | Lưu trữ cơ sở dữ liệu cục bộ | Các file `database/app.db`, `database/db.sql` |
| Lập trình | Git | Quản lý mã nguồn và theo dõi các thay đổi (Change tracking) | Lịch sử commit trên hệ thống và lệnh `git status` |
| Kiểm thử | Thư viện `unittest` của Python | Thực hiện các câu lệnh khẳng định (Assertions) tự động ở tầng Service | File `test_services.py` |
| Kiểm thử | Bảng kịch bản kiểm thử thủ công | Thiết kế các bài kiểm thử chức năng dựa trên các tình huống sử dụng (Use cases) | File `TESTING_DOCUMENT_GROUP8.md` |
| Kiểm thử | Thư viện `py_compile` | Xác thực và kiểm tra lỗi cú pháp của mã nguồn | Lệnh chạy `python -m py_compile ...` |

