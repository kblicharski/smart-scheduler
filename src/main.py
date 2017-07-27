"""
This is the entry point to the program.
"""
import time
from pprint import pprint

from api import get_course_sections, get_all_department_identifiers
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
        print('What departments would you like to access? If multiple, add '
              'each on a new line, in lowercase (ece, cs, etc). Enter -1 to '
              'continue.')
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

semester = 68
departments = ['cs']

course_section_data = get_course_section_data(semester, departments)
log_course_sections(course_section_data)

courses = create_course_groups(course_section_data)
log_courses(courses)

end = time.time()

print('Process 1 took {} seconds'.format(end - start))

departments = get_all_department_identifiers()
pprint(departments)

start = time.time()

course_section_data = get_course_section_data(semester, departments)
log_course_sections(course_section_data)

courses = create_course_groups(course_section_data)
log_courses(courses)

end = time.time()
print('Process 2 took {} seconds'.format(end - start))

total_enrolled_students = 0
current_department = courses[0].subject_course.split(':')[0]
for course in courses:
    new_department = course.subject_course.split(':')[0]

    # Check to see if there's been a department change
    if new_department != current_department:
        print("The total enrolled students for {} is: {}"
              .format(current_department, total_enrolled_students))
        current_department = new_department
        total_enrolled_students = 0

    # this needs to come after to ensure accurate counting
    for section in course.sections:
        total_enrolled_students += section.current_enroll

if current_department == new_department:
    print('The total enrolled students for {} is: {}'
          .format(new_department, total_enrolled_students))
