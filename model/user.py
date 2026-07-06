# Entity User - khop bang Users trong Database/db.sql


class User:
    def __init__(self, userID=None, userName=None, password=None, role=None,
                 sex=None, createdDate=None, status=None):
        self.userID = userID
        self.userName = userName
        self.password = password
        self.role = role
        self.sex = sex
        self.createdDate = createdDate
        self.status = status
