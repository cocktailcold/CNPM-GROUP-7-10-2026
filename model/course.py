class Course:
    def __init__(self, course_id, course_name, credit, semester=None,
                 status=None, fee=0.0, prerequisites=None):
        self.course_id = course_id
        self.course_name = course_name
        self.credit = credit
        self.semester = semester
        self.status = status
        self.fee = fee
        self.prerequisites = prerequisites or []  # list<Course> mon tien quyet

    def open_course(self):
        self.status = "OPEN"

    def close_course(self):
        self.status = "CLOSED"

    def add_prerequisite(self, course):
        if course not in self.prerequisites:
            self.prerequisites.append(course)

    def remove_prerequisite(self, course):
        if course in self.prerequisites:
            self.prerequisites.remove(course)

    def get_prerequisites(self):
        # tra ve list<Course>
        return self.prerequisites

    def calculate_fee(self):
        # tra ve double
        return self.fee
