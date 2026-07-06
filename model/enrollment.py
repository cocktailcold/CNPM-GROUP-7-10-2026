# Entity Enrollment - khop bang Enrollment trong Database/db.sql
# Ghi chu: db.sql chua co cot status. Quy uoc: con ban ghi = "Confirmed";
# huy = xoa ban ghi. (Nhom nen bo sung cot status vao db.sql neu can luu lai.)


class Enrollment:
    def __init__(self, enrollID=None, studentID=None, courseClassID=None,
                 enrollDate=None, status="Confirmed"):
        self.enrollID = enrollID
        self.studentID = studentID
        self.courseClassID = courseClassID
        self.enrollDate = enrollDate
        self.status = status
