# Entity Room - khop bang Room trong Database/db.sql


class Room:
    def __init__(self, roomCode=None, buildingID=None, roomName=None):
        self.roomCode = roomCode
        self.buildingID = buildingID
        self.roomName = roomName
