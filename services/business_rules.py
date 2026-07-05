def passed_prerequisites(student_id, course_id, course_repo, result_repo):
    course = course_repo.find_by_id(course_id)
    if course is None:
        raise Exception("Course not found")
    prerequisites = course.prerequisites
    if not prerequisites:
        return True
    student_results = result_repo.find_by_student(student_id)
    passed_course_ids = {r.courseID for r in student_results if r.status == "Pass"}
    return all(p.courseID in passed_course_ids for p in prerequisites)


def has_conflict(student_id, class_id, schedule_repo):
    new_schedule = schedule_repo.find_by_class(class_id)
    current_schedules = schedule_repo.find_by_student(student_id)
    for current in current_schedules:
        for new in new_schedule:
            if current.time == new.time:
                return True
    return False