# Entity Schedule - khop bang Schedule trong Database/db.sql
# Ghi chu: db.sql luu thoi gian o cot "session"; repository anh xa sang
# thuoc tinh "time" cho khop voi services.


class Schedule:
    def __init__(self, scheduleID=None, courseClassID=None, roomCode=None,
                 time=None, startDate=None, endDate=None):
        self.scheduleID = scheduleID
        self.courseClassID = courseClassID
        self.roomCode = roomCode
        self.time = time
        self.startDate = startDate
        self.endDate = endDate

    def conflict_with(self, other):
        return self.time == other.time
