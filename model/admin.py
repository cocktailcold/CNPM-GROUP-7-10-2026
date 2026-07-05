from model.user import User


class Admin(User):
    def __init__(self, user_id, username, password, admin_id, name, phone,
                 sex=None, national_id=None, role="ADMIN", status=None,
                 created_date=None):
        super().__init__(user_id, username, password, sex, national_id, role,
                         status, created_date)
        self.admin_id = admin_id
        self.name = name
        self.phone = phone

    def create_course(self):
        pass

    def update_course(self):
        pass

    def create_course_class(self):
        # tra ve mot doi tuong CourseClass
        pass

    def assign_schedule(self):
        pass
