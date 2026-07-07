# Task Assignment and Tool Usage Evidence - Group 8

## Task Assignment

| Phân Chia | Công việc | Hiệu quả |
| --- | --- | --- |
| Thiên Kim | UI (Presentation Layer) | 100% |
| Ngọc Hân | Service (Business Logic Layer) | 100% |
| Phi Hùng | Model & Data Access Layer (DAO/Repository) | 100% |
| Khả Diệp | Database & SQLite Integration | 100% |
| Minh Chiến | System Integration & Deployment(Main+Utilities) | 100% |
| Hiếu Nghĩa | Testing & Documentation | |

## Tool Usage Evidence

| Tool | Usage | Evidence |
| --- | --- | --- |
| Python | Main programming language | `.py` source files |
| Tkinter | Graphical user interface | `main.py` |
| SQLite | Database | `database/app.db`, `database/db.sql` |
| unittest | Automated testing | `test_services.py` |
| Docker | Containerized test command | `Dockerfile` |
| Git | Version control | Repository history |
| Excel template | Manual test case document | `Testing Document Group8.xlsx` |

## Verification Commands

```powershell
python -m py_compile main.py test_services.py
python -m unittest test_services.py
python test_repositories.py
```

## Docker Verification

```powershell
docker build -t cnpm-group8 .
docker run --rm cnpm-group8
```
