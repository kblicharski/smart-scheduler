from factories import CourseFactory


i = 0
course_set = set()
factory = CourseFactory()

while i < factory.number_of_courses:
    course = factory.get_course()

    # If it's a unique course, print it
    if course.number not in course_set:
        course_set.add(course.number)
        print(i, course)
        i += 1
