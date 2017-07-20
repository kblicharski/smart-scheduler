"""
This is the entry point to the program.
"""
import re

from constraint import Problem, Solver, Constraint

from api import get_courses
from classes import CourseSection


def log_courses(courses: list):
    """
    Opens and writes to two different files.
    One for raw, comma-separated data and the other for human-readable output.
    """
    pretty_file = open('../output.txt', mode='w')
    csv_file = open('../raw_output.txt', mode='w')

    for course in courses:
        try:
            str = '{}:{}\t{} - {}\t\t{}' \
                .format(course['subjectCourse'],
                        course['sectionNumber'],
                        course['timeAndLocations'][0]['startTime'],
                        course['timeAndLocations'][0]['endTime'],
                        course['courseTitle'])
        except KeyError:
            """
            Some courses do not have times. We do not want to halt execution,
            just print them in a different format.
            """
            str = '{}:{}\t\t\t\t\t\t{}' \
                .format(course['subjectCourse'],
                        course['sectionNumber'],
                        course['courseTitle'])

        str += '\n'
        pretty_file.write(str)

        str = re.sub('\t+', ',', str)
        str = re.sub(' - ', ',', str)
        csv_file.write(str)

    pretty_file.close()
    csv_file.close()


def make_course(course: dict):
    """
    Helper function to quickly turn JSON data into CourseSections for testing
    """
    return CourseSection(course['courseTitle'], course[
        'sectionId'], course['sectionNumber'], course[
                             'subjectCourse'], course['timeAndLocations'])

cs_courses = get_courses(68, 'cs')
# ece_courses = get_courses(68, 'ece')
# math_courses = get_courses(68, 'math')
courses = cs_courses

log_courses(courses)

'''
def fetch_courses(courses: list):
    """
    Fetches courses based on an input in the format `CS:2230`.
    Raises an exception if a course was not found.

    :param courses: list of courses the user wants to enroll in
    identified by their department and number
    :return: list of identified courses, or an error if one was not found
    """
    fetched_courses = []

    for course_id in courses:
        course_values = course_id.partition(':')
        course_department = course_values[0]
        course_number = course_values[2]

        num_courses = len(fetched_courses)

        for course in course_set:
            print('{} == {}'.format(course.department, course_department))
            print('{} == {}'.format(course.number, course_number))
            if course.department == course_department and course.number == \
                    course_number:
                print('Found course' + course_id)
                fetched_courses.append(course)

        # We didn't actually find the course
        if len(fetched_courses) == num_courses:
            raise Exception('We could not find ' + course_id)

    return fetched_courses
'''
