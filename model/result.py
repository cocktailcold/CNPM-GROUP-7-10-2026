# Entity Result - khop bang studentResult trong Database/db.sql


class Result:
    def __init__(self, resultID=None, studentID=None, courseID=None, gpa=None,
                 status=None):
        self.resultID = resultID
        self.studentID = studentID
        self.courseID = courseID
        self.gpa = gpa
        self.status = status
