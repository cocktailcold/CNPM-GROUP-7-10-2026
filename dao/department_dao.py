from dao.base_dao import BaseDAO
from model.department import Department


class DepartmentDAO(BaseDAO):

    def insert(self, khoa):
        self.conn.execute(
            "INSERT INTO departments (department_id, department_name) VALUES (?, ?)",
            (khoa.department_id, khoa.department_name))
        self.commit()

    def find_by_id(self, department_id):
        cur = self.conn.execute(
            "SELECT * FROM departments WHERE department_id = ?",
            (department_id,))
        row = cur.fetchone()
        if row is None:
            return None
        return Department(row["department_id"], row["department_name"])

    def find_all(self):
        cur = self.conn.execute("SELECT * FROM departments ORDER BY department_id")
        return [Department(r["department_id"], r["department_name"])
                for r in cur.fetchall()]
