from dao.base_dao import BaseDAO
from model.student import Student

# Cac cot lay tu JOIN Student + Users
_SELECT = """SELECT s.studentID, s.userID, s.studentName, s.phone, s.email,
             s.birthdate, u.userName, u.password, u.role, u.sex, u.status,
             u.createdDate
             FROM Student s JOIN Users u ON s.userID = u.userID"""


def _row_to_student(row):
    if row is None:
        return None
    return Student(row["userID"], row["userName"], row["password"],
                   row["studentID"], row["studentName"], row["email"],
                   row["phone"], row["birthdate"], row["sex"], None,
                   row["role"], row["status"], row["createdDate"])


class StudentDAO(BaseDAO):

    def insert(self, s):
        # tai khoan (Users) phai duoc tao truoc
        cur = self.conn.execute(
            """INSERT INTO Student (userID, studentName, phone, email,
               birthdate) VALUES (?, ?, ?, ?, ?)""",
            (s.user_id, s.student_name, s.phone, s.email, s.birth_date))
        self.commit()
        return cur.lastrowid  # studentID tu tang

    def update(self, s):
        self.conn.execute(
            """UPDATE Student SET studentName = ?, phone = ?, email = ?,
               birthdate = ? WHERE studentID = ?""",
            (s.student_name, s.phone, s.email, s.birth_date, s.student_id))
        self.commit()

    def delete(self, student_id):
        self.conn.execute(
            "DELETE FROM Student WHERE studentID = ?", (student_id,))
        self.commit()

    def find_by_id(self, student_id):
        cur = self.conn.execute(_SELECT + " WHERE s.studentID = ?",
                                (student_id,))
        return _row_to_student(cur.fetchone())

    def find_by_user_id(self, user_id):
        cur = self.conn.execute(_SELECT + " WHERE s.userID = ?", (user_id,))
        return _row_to_student(cur.fetchone())

    def find_by_email(self, email):
        cur = self.conn.execute(_SELECT + " WHERE s.email = ?", (email,))
        return _row_to_student(cur.fetchone())

    def find_all(self):
        cur = self.conn.execute(_SELECT + " ORDER BY s.studentID")
        return [_row_to_student(r) for r in cur.fetchall()]

    def update_password(self, user_id, new_password):
        # mat khau nam o bang Users
        self.conn.execute(
            "UPDATE Users SET password = ? WHERE userID = ?",
            (new_password, user_id))
        self.commit()
