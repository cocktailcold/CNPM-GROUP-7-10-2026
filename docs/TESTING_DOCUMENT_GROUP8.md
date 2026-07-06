# Testing Document - Course Registration System - Group 8

Note: This file drafts the test case content. For final submission, move these
test cases into the official Testing Document Template from Elearning 5.

## Test Cases

| TC ID | Function | Precondition | Test Data | Steps | Expected Result | Actual Result | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-LOGIN-01 | Login student | Database has active student account | IT00000003 / Hung1003@ | Open app, enter username and password, click Login | Student dashboard is displayed | As expected | Pass |
| TC-LOGIN-02 | Login admin | Database has active admin account | Admin1 / 123456 | Open app, enter username and password, click Login | Admin dashboard is displayed | As expected | Pass |
| TC-LOGIN-03 | Reject wrong password | User exists | IT00000003 / wrongpass | Enter username and wrong password, click Login | Error message "Invalid username or password" is shown | As expected | Pass |
| TC-COURSE-01 | View course classes | Student is logged in | IT00000003 | Open Course registration tab | Available classes with teacher, capacity, and schedule are listed | As expected | Pass |
| TC-ENROLL-01 | Enroll valid class | Student is logged in and class is open | Student 5, Class 3 | Select Class 3, click Enroll selected class | Enrollment is created and appears in My classes | As expected | Pass |
| TC-ENROLL-02 | Reject duplicate enrollment | Student is already enrolled in class | Student 5, Class 3 | Enroll Class 3 twice | Second enrollment is rejected | As expected | Pass |
| TC-ENROLL-03 | Reject missing prerequisite | Student has not passed prerequisite course | Student 1, Software Engineering class | Select Software Engineering class, click Enroll | Error message "Prerequisite not met" is shown | As expected | Pass |
| TC-ENROLL-04 | Reject full class | Class currentEnroll equals maxEnroll | Full class data | Select full class, click Enroll | Error message "This class is full" is shown | Not executed with seed data | Pending |
| TC-ENROLL-05 | Reject schedule conflict | Student has another class with same session | Conflicting class data | Select conflicting class, click Enroll | Error message "Schedule conflict detected" is shown | Not executed with seed data | Pending |
| TC-CANCEL-01 | Cancel enrollment | Student has at least one enrollment | Existing enrollment | Open My classes, select enrollment, click Cancel selected enrollment | Enrollment is removed and class currentEnroll decreases by 1 | As expected | Pass |
| TC-SCHEDULE-01 | View schedule | Student has enrolled classes | IT00000003 | Open Schedule tab | Schedule rows show class, session, start date, end date, and room | As expected | Pass |
| TC-RESULT-01 | View results | Student has result records | IT00000003 | Open Results tab | GPA and pass/fail status are displayed | As expected | Pass |
| TC-ADMIN-01 | Add course | Admin is logged in | Name: AI Basics, credit: 3, semester: 6, fee: 5500000 | Open Courses tab, enter data, click Add course | New course appears in course list | As expected | Pass |
| TC-ADMIN-02 | Reject duplicate course | Course name already exists | Introduction to Programming | Add a course with existing name | Error message "Course name already exists" is shown | As expected | Pass |
| TC-ADMIN-03 | Create class | Admin is logged in and course exists | Course ID: 1, Teacher: Demo Teacher, Max: 40 | Open Classes tab, enter data, click Create class | New class appears in class list | As expected | Pass |
| TC-ADMIN-04 | Reject invalid class course | Admin is logged in | Course ID: 9999 | Create class for non-existing course | Error message "Course not found" is shown | As expected | Pass |

## Automated Test Command

```powershell
python test_repositories.py
python -m unittest test_services.py
```

The command verifies repository loading, prerequisite checks, schedule conflict
checks, enrollment create/cancel behavior, and service-level login/enrollment.
