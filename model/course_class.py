# Lop hoc phan (CourseClass) - thuoc ve mot Course


class CourseClass:
    def __init__(self, course_class_id, course_id, class_id, max_enroll,
                 current_enroll=0, instructor_name=""):
        self.course_class_id = course_class_id
        self.course_id = course_id  # FK toi Course
        self.class_id = class_id
        self.max_enroll = max_enroll
        self.current_enroll = current_enroll
        self.instructor_name = instructor_name

    def is_full(self):
        # tra ve boolean
        return self.current_enroll >= self.max_enroll

    def get_current_enroll(self):
        # tra ve int
        return self.current_enroll
