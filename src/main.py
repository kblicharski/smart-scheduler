"""
This is the entry point to the program.
"""
from factories import CourseFactory
from constraint import Problem, Solver


def print_all_courses_in_mock_data():
    """
    Originally for testing purposes -- verifies that courses are
    formatted correctly.
    """
    i = 0
    course_set = set()
    factory = CourseFactory()

    while i < factory.number_of_courses:
        course = factory.get_course()

        # If it's a unique course, print it
        if course.number not in course_set:
            course_set.add(course.number)
            print(course)
            i += 1


problem = Problem()
