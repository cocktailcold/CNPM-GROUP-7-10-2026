# Lop hoc phan


class CourseSection:
    def __init__(self, section_id, course_id, lecturer_id, semester_id,
                 max_capacity, current_enrollment=0, room=""):
        self.section_id = section_id
        self.course_id = course_id
        self.lecturer_id = lecturer_id
        self.semester_id = semester_id
        self.max_capacity = max_capacity
        self.current_enrollment = current_enrollment
        self.room = room

    def is_full(self):
        return self.current_enrollment >= self.max_capacity

    def add_student(self):
        if self.is_full():
            return False
        self.current_enrollment += 1
        return True

    def remove_student(self):
        if self.current_enrollment > 0:
            self.current_enrollment -= 1
