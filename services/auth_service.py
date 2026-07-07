import hashlib

from repositories.user_repository import UserRepository


def _hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _password_matches(stored_password, password):
    return stored_password in (password, _hash_password(password))


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def login(self, username, password):
        user = self.user_repo.find_by_username(username)
        if user is None or not _password_matches(user.password, password):
            raise Exception("Invalid username or password")
        if user.status != "Active":
            raise Exception("Account is inactive")
        return user

    def verify_identity(self, username, email):
        if not username or not email:
            raise Exception("Username and email are required")
        user = self.user_repo.find_by_username_and_email(username, email)
        if user is None:
            raise Exception("Username or email does not exist")
        if user.status != "Active":
            raise Exception("Account is inactive")
        return user

    def reset_password(self, user_id, new_password, confirm_password):
        user = self.user_repo.find_by_id(user_id)
        if user is None:
            raise Exception("User not found")
        if not new_password or not confirm_password:
            raise Exception("New password and confirmation are required")
        if new_password != confirm_password:
            raise Exception("Passwords do not match")
        if len(new_password) < 6:
            raise Exception("New password must be at least 6 characters")
        user.password = _hash_password(new_password)
        return self.user_repo.save(user)

    def change_password(self, user_id, old_password, new_password):
        user = self.user_repo.find_by_id(user_id)
        if user is None:
            raise Exception("User not found")
        if not _password_matches(user.password, old_password):
            raise Exception("Old password is incorrect")
        if len(new_password) < 6:
            raise Exception("New password must be at least 6 characters")
        user.password = _hash_password(new_password)
        return self.user_repo.save(user)
