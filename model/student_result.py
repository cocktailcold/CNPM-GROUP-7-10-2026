# Ket qua hoc tap cua sinh vien


class StudentResult:
    def __init__(self, student_res_id, student_id, course_id, gpa=0.0,
                 status=None):
        self.student_res_id = student_res_id
        self.student_id = student_id  # FK toi Student
        self.course_id = course_id    # FK toi Course
        self.gpa = gpa
        self.status = status

    def print_result(self):
        pass
