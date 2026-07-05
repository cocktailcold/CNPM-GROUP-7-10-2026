from dao.base_dao import BaseDAO
from model.room import Room

# Class diagram: Room co roomCode + status. DB (bang Room) co roomCode,
# buildingID, roomName (khong co status) -> status doc len de None.


def _row_to_room(row):
    if row is None:
        return None
    return Room(row["roomCode"], row["buildingID"], None)


class RoomDAO(BaseDAO):

    def insert(self, r, room_name=None):
        cur = self.conn.execute(
            "INSERT INTO Room (buildingID, roomName) VALUES (?, ?)",
            (r.building_id, room_name))
        self.commit()
        return cur.lastrowid  # roomCode tu tang

    def find_by_id(self, room_code):
        cur = self.conn.execute(
            "SELECT * FROM Room WHERE roomCode = ?", (room_code,))
        return _row_to_room(cur.fetchone())

    def find_by_building(self, building_id):
        cur = self.conn.execute(
            "SELECT * FROM Room WHERE buildingID = ? ORDER BY roomCode",
            (building_id,))
        return [_row_to_room(r) for r in cur.fetchall()]

    def find_all(self):
        cur = self.conn.execute("SELECT * FROM Room ORDER BY roomCode")
        return [_row_to_room(r) for r in cur.fetchall()]
