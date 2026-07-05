# Phong hoc - thuoc ve mot Building


class Room:
    def __init__(self, room_code, building_id, status=None):
        self.room_code = room_code
        self.building_id = building_id  # FK toi Building
        self.status = status

    def is_available(self):
        # tra ve boolean
        return self.status == "AVAILABLE"
