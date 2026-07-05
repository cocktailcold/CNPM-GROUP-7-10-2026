class Semester:
    def __init__(self, semester_id, name, start_date, end_date,
                 registration_deadline):
        self.semester_id = semester_id
        self.name = name
        self.start_date = start_date  # dang 'YYYY-MM-DD'
        self.end_date = end_date
        self.registration_deadline = registration_deadline
