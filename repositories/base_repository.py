from database.db import Database


def field(data, key, default=None):
    # doc gia tri tu dict hoac tu object entity
    if isinstance(data, dict):
        return data.get(key, default)
    return getattr(data, key, default)


class BaseRepository:
    def __init__(self, db=None):
        # services goi Repository() khong tham so -> tu tao ket noi Database
        self.db = db or Database()

    def _last_id(self):
        row = self.db.fetch_one("SELECT last_insert_rowid() AS id")
        return row["id"] if row else None
