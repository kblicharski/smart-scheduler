"""
This is the entry point to the program.
"""
import time

from api import get_course_sections
from utils import log_course_sections, log_courses, create_course_groups


def get_course_section_data(semester: int = None, departments: [str] = None) \
        -> [dict]:
    # TODO (docs)
    """
    :param semester:
    :param departments:
    :return:
    """
    # TODO: Add validation and error handling
    # TODO: Add the capability to specify how many of each they want

    if not semester:
        print('What semester would you like to access course data from?')
        print('69: Summer 2017')
        print('68: Fall 2017')
        print('70: Winter 2017')
        print('71: Spring 2018')
        semester = int(input())

    if not departments:
        print('What departments would you like to access? If multiple, add'
              'each on a new line. Enter -1 to continue.')
        departments = []
        while True:
            user_input = input()
            if user_input == '-1':
                break
            departments.append(user_input)

    course_section_data = []
    for department in departments:
        course_section_data += get_course_sections(semester, department)

    return course_section_data


start = time.time()

# semester = 68
# departments = ['math', 'cs']

course_section_data = get_course_section_data()
log_course_sections(course_section_data)

courses = create_course_groups(course_section_data)
log_courses(courses)

end = time.time()

print('Process took {} seconds'.format(end - start))
