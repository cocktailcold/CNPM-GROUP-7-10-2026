# Phieu dang ky cua sinh vien voi mot lop hoc phan


class Registration:
    STATUS_REGISTERED = "REGISTERED"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_COMPLETED = "COMPLETED"

    def __init__(self, registration_id, student_id, section_id,
                 registration_date, status=STATUS_REGISTERED, grade=None):
        self.registration_id = registration_id
        self.student_id = student_id
        self.section_id = section_id
        self.registration_date = registration_date
        self.status = status
        self.grade = grade

    def confirm(self):
        self.status = Registration.STATUS_REGISTERED

    def cancel(self):
        self.status = Registration.STATUS_CANCELLED

