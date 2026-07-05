# Lop cha cua Student, Lecturer, Administrator


class Person:
    def __init__(self, person_id, full_name, email, password, phone):
        self.person_id = person_id
        self.full_name = full_name
        self.email = email
        self.password = password  # da duoc hash truoc khi luu
        self.phone = phone

    def login(self, email, password):
        return self.email == email and self.password == password

    def logout(self):
        pass
