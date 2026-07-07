from repositories.base_repository import BaseRepository, field
from model.user import User


def _to_user(row):
    if row is None:
        return None
    return User(row["userID"], row["userName"], row["password"], row["role"],
                row["sex"], row["createdDate"], row["status"])


class UserRepository(BaseRepository):

    def find_by_username(self, username):
        row = self.db.fetch_one(
            "SELECT * FROM Users WHERE userName = ?", (username,))
        return _to_user(row)

    def find_by_id(self, user_id):
        row = self.db.fetch_one(
            "SELECT * FROM Users WHERE userID = ?", (user_id,))
        return _to_user(row)

    def find_by_username_and_email(self, username, email):
        row = self.db.fetch_one(
            """SELECT u.*
               FROM Users u
               JOIN Student s ON s.userID = u.userID
               WHERE u.userName = ? AND LOWER(s.email) = LOWER(?)""",
            (username, email),
        )
        return _to_user(row)

    def find_all(self):
        rows = self.db.fetch_all("SELECT * FROM Users ORDER BY userID")
        return [_to_user(r) for r in rows]

    def save(self, user):
        user_id = field(user, "userID")
        if user_id:  # da co -> cap nhat
            self.db.execute(
                """UPDATE Users SET userName = ?, password = ?, role = ?,
                   sex = ?, createdDate = ?, status = ? WHERE userID = ?""",
                (field(user, "userName"), field(user, "password"),
                 field(user, "role"), field(user, "sex"),
                 field(user, "createdDate"), field(user, "status"), user_id))
            self.db.commit()
            return self.find_by_id(user_id)
        # chua co -> them moi
        self.db.execute(
            """INSERT INTO Users (userName, password, role, sex, createdDate,
               status) VALUES (?, ?, ?, ?, ?, ?)""",
            (field(user, "userName"), field(user, "password"),
             field(user, "role"), field(user, "sex"),
             field(user, "createdDate"), field(user, "status", "Active")))
        self.db.commit()
        return self.find_by_id(self._last_id())
