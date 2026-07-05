from model.user import User


class Student(User):
    def __init__(self, user_id, username, password, student_id, student_name,
                 email, phone, birth_date, sex=None, national_id=None,
                 role="STUDENT", status=None, created_date=None):
        super().__init__(user_id, username, password, sex, national_id, role,
                         status, created_date)
        self.student_id = student_id
        self.student_name = student_name
        self.email = email
        self.phone = phone
        self.birth_date = birth_date

    def enroll_course(self):
        # tra ve boolean
        pass

    def cancel_enrollment(self):
        pass

    def view_schedule(self):
        # tra ve list<Schedule>
        return []

    def view_tuition(self):
        # tra ve double (hoc phi)
        return 0.0
