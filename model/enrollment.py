# Phieu dang ky cua sinh vien voi mot lop hoc phan (CourseClass)


class Enrollment:
    STATUS_REGISTERED = "REGISTERED"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_COMPLETED = "COMPLETED"

    def __init__(self, enroll_id, student_id, course_class_id, enroll_date,
                 status=STATUS_REGISTERED):
        self.enroll_id = enroll_id
        self.student_id = student_id            # FK toi Student
        self.course_class_id = course_class_id  # FK toi CourseClass
        self.enroll_date = enroll_date
        self.status = status

    def confirm(self):
        self.status = Enrollment.STATUS_REGISTERED

    def cancel(self):
        self.status = Enrollment.STATUS_CANCELLED
