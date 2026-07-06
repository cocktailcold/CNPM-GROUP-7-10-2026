# Entity Course - khop bang Courses trong Database/db.sql


class Course:
    def __init__(self, courseID=None, courseName=None, credit=None,
                 semester=None, status=None, fee=None, prerequisites=None):
        self.courseID = courseID
        self.courseName = courseName
        self.credit = credit
        self.semester = semester
        self.status = status
        self.fee = fee
        # danh sach mon tien quyet (list<Course>)
        self.prerequisites = prerequisites or []
