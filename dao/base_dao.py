class BaseDAO:
    def __init__(self, conn):
        self.conn = conn

    def commit(self):
        self.conn.commit()
