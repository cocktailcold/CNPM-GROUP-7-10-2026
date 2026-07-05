from model.person import Person


class Administrator(Person):
    def __init__(self, person_id, full_name, email, password, phone,
                 admin_code):
        super().__init__(person_id, full_name, email, password, phone)
        self.admin_code = admin_code

    def create_course(self, course):
        # tao mon hoc moi (luu qua DAO o tang service)
        return course

    def open_section(self, section):
        # mo mot lop hoc phan (luu qua DAO o tang service)
        return section

    def manage_registration_period(self):
        # quan ly dot dang ky (thiet lap qua DAO o tang service)
        pass
