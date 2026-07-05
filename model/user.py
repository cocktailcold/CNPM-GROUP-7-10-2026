# Lop cha cua Admin va Student


class User:
    def __init__(self, user_id, username, password, sex=None, national_id=None,
                 role=None, status=None, created_date=None):
        self.user_id = user_id
        self.username = username
        self.password = password  # da duoc hash truoc khi luu
        self.sex = sex
        self.national_id = national_id
        self.role = role
        self.status = status
        self.created_date = created_date

    def login(self, username, password):
        return self.username == username and self.password == password

    def logout(self):
        pass

    def change_password(self, new_password):
        self.password = new_password
