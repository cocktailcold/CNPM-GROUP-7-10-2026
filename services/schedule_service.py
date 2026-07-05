from repositories.schedule_repository import ScheduleRepository

class ScheduleService:
    def __init__(self):
        self.schedule_repo = ScheduleRepository()

    def view_schedule(self, student_id):
        return self.schedule_repo.find_by_student(student_id)

    def conflict_with(self, schedule_a, schedule_b):
        return schedule_a.time == schedule_b.time