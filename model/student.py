# Entity Student - khop bang Student trong Database/db.sql


class Student:
    def __init__(self, studentID=None, userID=None, studentName=None,
                 phone=None, email=None, birthdate=None):
        self.studentID = studentID
        self.userID = userID
        self.studentName = studentName
        self.phone = phone
        self.email = email
        self.birthdate = birthdate
