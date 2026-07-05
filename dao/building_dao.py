from dao.base_dao import BaseDAO
from model.building import Building
from model.room import Room


def _row_to_building(row):
    if row is None:
        return None
    return Building(row["buildingID"], row["buildingName"])


class BuildingDAO(BaseDAO):

    def insert(self, b):
        cur = self.conn.execute(
            "INSERT INTO Building (buildingName) VALUES (?)",
            (b.building_name,))
        self.commit()
        return cur.lastrowid  # buildingID tu tang

    def find_by_id(self, building_id):
        cur = self.conn.execute(
            "SELECT * FROM Building WHERE buildingID = ?", (building_id,))
        return _row_to_building(cur.fetchone())

    def find_all(self):
        cur = self.conn.execute("SELECT * FROM Building ORDER BY buildingID")
        return [_row_to_building(r) for r in cur.fetchall()]

    def get_rooms(self, building_id):
        # tra ve list<Room> thuoc toa nha
        cur = self.conn.execute(
            "SELECT * FROM Room WHERE buildingID = ? ORDER BY roomCode",
            (building_id,))
        return [Room(r["roomCode"], r["buildingID"], None)
                for r in cur.fetchall()]
