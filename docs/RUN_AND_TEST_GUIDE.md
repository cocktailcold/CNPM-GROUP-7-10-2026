# Run and Test Guide - Group 8

## 1. Run The GUI Application

Open PowerShell in the project folder:

```powershell
cd C:\CNPM-GROUP-8\CNPM-GROUP-8
python main.py
```

Demo accounts:

| Role | Username | Password |
| --- | --- | --- |
| Student | IT00000003 | Hung1003@ |
| Student | IT00000005 | Hien&2022! |
| Admin | Admin1 | 123456 |

## 2. Manual Testing With Excel Test Cases

Open:

```text
docs\Testing Document Group8.xlsx
```

Then execute each row:

1. Read `Test Steps`.
2. Enter the values in `Input Data`.
3. Compare the app behavior with `Expected Result`.
4. Mark the result during presentation or in the official template if required.

Important manual flows:

- Student login success and failed login.
- View class list.
- Enroll a valid class.
- Reject duplicate enrollment.
- Reject missing prerequisite.
- Cancel enrollment.
- View schedule and results.
- Admin add course.
- Admin create class.

## 3. Automated Testing

Run syntax check:

```powershell
python -m py_compile main.py tests\test_services.py
```

Run service tests:

```powershell
python -m unittest discover -s tests -p "test_services.py"
```

Run repository/service smoke test:

```powershell
python tests\test_repositories.py
```

Expected result:

```text
OK
TAT CA TEST REPOSITORIES CHAY OK
```

## 4. Docker Testing

Build image:

```powershell
docker build -t cnpm-group8 .
```

Run tests in container:

```powershell
docker run --rm cnpm-group8
```

Expected result:

```text
Ran 7 tests
OK
```

The Docker command is for automated tests. The GUI should be run directly on
Windows with `python main.py`.

## 5. Submission Folder

Create a folder named like:

```text
ProgAndTest_Group8
```

Put these files/folders inside:

- `main.py`
- `model/`
- `repositories/`
- `services/`
- `database/`
- `tests/`
- `docs/Testing Document Group8.xlsx`
- `docs/TASK_ASSIGNMENT_AND_EVIDENCE.md`
- `docs/TOOLS_USAGE_GROUP8.md`
- `Dockerfile`
- `README.md`

Then compress the folder and submit.
