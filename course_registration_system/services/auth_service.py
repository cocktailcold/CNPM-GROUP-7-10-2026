from repositories.user_repository import UserRepository

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def login(self, username, password):
        user = self.user_repo.find_by_username(username)
        if user is None or user.password != password:
            raise Exception("Invalid username or password")
        if user.status != "Active":
            raise Exception("Account is inactive")
        return user

    def change_password(self, user_id, old_password, new_password):
        user = self.user_repo.find_by_id(user_id)
        if user is None:
            raise Exception("User not found")
        if user.password != old_password:
            raise Exception("Old password is incorrect")
        if len(new_password) < 6:
            raise Exception("New password must be at least 6 characters")
        user.password = new_password
        return self.user_repo.save(user)