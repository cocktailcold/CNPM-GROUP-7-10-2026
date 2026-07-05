# Toa nha - chua nhieu Room


class Building:
    def __init__(self, building_id, building_name, rooms=None):
        self.building_id = building_id
        self.building_name = building_name
        self.rooms = rooms or []  # list<Room>

    def get_rooms(self):
        # tra ve list<Room>
        return self.rooms
