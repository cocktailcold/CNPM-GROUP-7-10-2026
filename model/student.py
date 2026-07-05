from model.person import Person


class Student(Person):
    def __init__(self, person_id, full_name, email, password, phone,
                 student_code, major, enrollment_year, gpa=0.0):
        super().__init__(person_id, full_name, email, password, phone)
        self.student_code = student_code
        self.major = major
        self.enrollment_year = enrollment_year
        self.gpa = gpa
