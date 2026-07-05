from model.person import Person


class Lecturer(Person):
    def __init__(self, person_id, full_name, email, password, phone,
                 lecturer_code, title):
        super().__init__(person_id, full_name, email, password, phone)
        self.lecturer_code = lecturer_code
        self.title = title
