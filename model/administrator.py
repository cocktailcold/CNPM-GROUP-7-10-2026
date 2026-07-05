from model.person import Person


class Administrator(Person):
    def __init__(self, person_id, full_name, email, password, phone,
                 admin_code):
        super().__init__(person_id, full_name, email, password, phone)
        self.admin_code = admin_code
