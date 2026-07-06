# CNPM-GROUP-8

Course Registration System implemented in Python with an object-oriented
model/repository/service structure and a Tkinter graphical user interface.

## Run

```powershell
python main.py
```

If `database/app.db` does not exist, the application creates it from
`database/db.sql` and `database/insertData.sql`.

## Demo Accounts

| Role | Username | Password |
| --- | --- | --- |
| Student | IT00000003 | Hung1003@ |
| Student | IT00000005 | Hien&2022! |
| Admin | Admin1 | 123456 |

## Main Functions

Student:

- Login and validate account status.
- View available course classes.
- Enroll in a class with prerequisite, capacity, duplicate, and schedule conflict checks.
- Cancel an enrollment.
- View personal schedule.
- View learning results.

Admin:

- View all courses, classes, and users.
- Add a new course.
- Create a new class for an existing course.

## Testing

Detailed run and test instructions are in `docs/RUN_AND_TEST_GUIDE.md`.

Run the repository/service integration smoke test:

```powershell
python tests/test_repositories.py
```

Run assertion-based service tests:

```powershell
python -m unittest discover -s tests -p "test_services.py"
```

Manual test cases are drafted in `docs/TESTING_DOCUMENT_GROUP8.md`. Before final
submission, copy them into the official Testing Document Template from
Elearning 5.
