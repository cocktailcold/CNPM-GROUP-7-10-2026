# Lich hoc cua mot lop hoc phan (CourseClass) tai mot phong (Room)


class Schedule:
    def __init__(self, schedule_id, course_class_id, room_code, time):
        self.schedule_id = schedule_id
        self.course_class_id = course_class_id  # FK toi CourseClass
        self.room_code = room_code              # FK toi Room
        self.time = time

    def conflict_with(self, other):
        # tra ve boolean - True neu trung lich (cung phong va cung thoi gian)
        return (self.time == other.time
                and self.room_code == other.room_code)
