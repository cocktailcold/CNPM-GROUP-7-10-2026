# Entity CourseClass - khop bang coursesClass trong Database/db.sql
# Ghi chu: db.sql luu teacherID (FK Teacher); repository doc teacherName ra
# thuoc tinh instructorName cho khop voi services.


class CourseClass:
    def __init__(self, courseClassID=None, courseID=None, instructorName=None,
                 maxEnroll=None, currentEnroll=0, status=None):
        self.courseClassID = courseClassID
        self.courseID = courseID
        self.instructorName = instructorName
        self.maxEnroll = maxEnroll
        self.currentEnroll = currentEnroll
        self.status = status
