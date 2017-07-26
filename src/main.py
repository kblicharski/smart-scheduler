"""
This is the entry point to the program.
"""
import time
from itertools import groupby
from operator import itemgetter

from api import get_course_sections
from utils import log_courses, make_section
from pprint import pprint

start = time.time()
course_sections = get_course_sections(68, 'cs', 5)
log_courses(course_sections)
# pprint(course_sections)

course_sections = sorted(course_sections, key=itemgetter('subjectCourse'))

for key, values in groupby(course_sections, key=itemgetter('subjectCourse')):
    print(key)
    values = list(values)
    print(values)
    for value in values:
        section = make_section(value)
        print(section)


end = time.time()

print('Process took {} seconds'.format(end - start))

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
