# Task Assignment and Tool Usage Evidence - Group 8

## Task Assignment

| Member | Main Responsibility | Evidence Files |
| --- | --- | --- |
| Member 1 | Database design and seed data | `database/db.sql`, `database/insertData.sql` |
| Member 2 | Entity/model classes | `model/` |
| Member 3 | Repository layer | `repositories/` |
| Member 4 | Business/service layer | `services/` |
| Member 5 | GUI, testing document, and integration testing | `main.py`, `Testing Document Group8.xlsx`, `test_services.py` |

Update the member names before final submission.

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
