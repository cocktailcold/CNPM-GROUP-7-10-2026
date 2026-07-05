class Course:
    def __init__(self, course_id, course_name, credits, description="",
                 department_id=None, prerequisites=None):
        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits
        self.description = description
        self.department_id = department_id
        self.prerequisites = prerequisites or []  # ma cac mon tien quyet

    def get_prerequisites(self):
        return self.prerequisites
