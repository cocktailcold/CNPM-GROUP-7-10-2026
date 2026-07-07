# Task Assignment and Tool Usage Evidence - Group 8

## Task Assignment

| Phân Chia | Công việc | Hiệu quả |
| --- | --- | --- |
| Thiên Kim | UI (Presentation Layer) | |
| Ngọc Hân | Service (Business Logic Layer) | Bonus: Minh Chiến support phần này. |
| Phi Hùng | Model & Data Access Layer (DAO/Repository) | |
| Khả Diệp | Database & SQLite Integration | |
| Minh Chiến | System Integration & Deployment(Main+Utilities) | |
| Hiếu,Nghĩa | Testing & Documentation | Bonus: Thiên Kim support phần này. |

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
