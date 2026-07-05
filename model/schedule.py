class Schedule:
    def __init__(self, schedule_id, section_id, day_of_week,
                 start_period, end_period, room=""):
        self.schedule_id = schedule_id
        self.section_id = section_id
        self.day_of_week = day_of_week
        self.start_period = start_period
        self.end_period = end_period
        self.room = room

    def overlaps(self, other):
        # trung lich khi cung thu va khoang tiet giao nhau
        if self.day_of_week != other.day_of_week:
            return False
        return (self.start_period <= other.end_period
                and other.start_period <= self.end_period)
