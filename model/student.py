from model.person import Person


class Student(Person):
    def __init__(self, person_id, full_name, email, password, phone,
                 student_code, major, enrollment_year, gpa=0.0):
        super().__init__(person_id, full_name, email, password, phone)
        self.student_code = student_code
        self.major = major
        self.enrollment_year = enrollment_year
        self.gpa = gpa

    def register_section(self, section):
        # dang ky vao mot lop hoc phan, tra ve True neu con cho
        return section.add_student()

    def drop_section(self, section):
        # huy dang ky khoi mot lop hoc phan
        section.remove_student()
        return True

    def view_schedule(self):
        # tra ve danh sach lich hoc (du lieu lay qua DAO o tang service)
        return []

    def view_grades(self):
        # tra ve danh sach diem (du lieu lay qua DAO o tang service)
        return []
