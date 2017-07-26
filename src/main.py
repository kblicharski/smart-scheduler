"""
This is the entry point to the program.
"""
import time

from api import get_course_sections
from utils import log_course_sections, log_courses, create_course_groups

start = time.time()

course_section_data = get_course_sections(68, 'cs')
course_section_data += get_course_sections(68, 'ece')
course_section_data += get_course_sections(68, 'ie')
course_section_data += get_course_sections(68, 'math')

log_course_sections(course_section_data)

courses = create_course_groups(course_section_data)
log_courses(courses)

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
