# Minh chứng sử dụng công cụ 

## Minh chứng sử dụng công cụ (Tool)

| Công cụ | Mục đích sử dụng | Minh chứng cụ thể |
| --- | --- | --- |
| Python | Ngôn ngữ lập trình chính của dự án | Các file mã nguồn `.py` |
| Tkinter | Xây dựng giao diện đồ họa (GUI) | File `main.py` |
| SQLite | Hệ quản trị cơ sở dữ liệu | Các file `database/app.db`, `database/db.sql` |
| unittest | Thư viện kiểm thử tự động (Automated Testing) | File `test_services.py` |
| Docker | Đóng gói môi trường chạy lệnh kiểm thử | File `Dockerfile` |
| Git | Quản lý mã nguồn và phiên bản code | Lịch sử commit trên Kho chứa (Repository) |
| Mẫu Excel | Thiết kế tài liệu kịch bản kiểm thử thủ công | File `Testing Document Group8.xlsx` |

## Các lệnh Xác thực Hệ thống (Verification Commands)

```powershell
python -m py_compile main.py test_services.py
python -m unittest test_services.py
python test_repositories.py
## Docker Verification

```powershell
docker build -t cnpm-group8 .
docker run --rm cnpm-group8
```
