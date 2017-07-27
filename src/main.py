"""
This is the entry point to the program.
"""
import time
from pprint import pprint

from constraint import Problem

from api import get_course_sections, get_all_department_identifiers
from classes import Course, CourseSection
from utils import log_course_sections, log_courses, create_course_groups, \
    print_solutions, get_number_of_solutions


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


def get_courses_from_user_input(input_ids: [str],
                                courses: [Course]) -> [Course]:
    selected_courses = []
    for id in input_ids:
        for course in courses:
            if course.subject_course == id:
                selected_courses.append(course)

    return selected_courses

start = time.time()

semester = 68
departments = ['cs', 'ece', 'ie']

course_section_data = get_course_section_data(semester, departments)
log_course_sections(course_section_data)

courses = create_course_groups(course_section_data)
log_courses(courses)

end = time.time()

print('Process 1 took {} seconds'.format(end - start))


requested_course_identifiers = ['CS:3330',
                                'ECE:3000',
                                'ECE:3330',
                                'ECE:3320',
                                'ECE:3540',
                                'IE:4172']

chosen_courses = get_courses_from_user_input(requested_course_identifiers,
                                             courses)

log_courses(chosen_courses)


def find_solutions(courses: [Course]) -> [dict]:
    problem = Problem()

    for course in courses:
        problem.addVariable(course.subject_course,
                            course.sections)

    def no_time_conflicts(*args) -> bool:
        is_valid = False
        valid_count = 0
        for arg in args:
            for arg_other in args:
                check1 = (arg.end_time < arg_other.start_time or
                          arg_other.end_time < arg.start_time)
                check2 = (arg.end_time != arg_other.end_time or
                          arg.start_time != arg_other.start_time)
                check3 = (arg != arg_other)
                is_valid = check1 and check2 and check3
                if is_valid:
                    valid_count += 1
                print('{}\t{}\t{}'.format(arg, arg_other, is_valid))
        # this returns all of the solutions
        print('Total Valid Pairings: ' + str(valid_count))
        return True

        # this returns none of the solutions
        # return is_valid

    problem.addConstraint(no_time_conflicts,
                          [course.subject_course for course in courses])

    solution_set = problem.getSolutions()
    solutions = get_number_of_solutions(solution_set)
    pprint(solution_set)
    print('Solutions: ' + str(solutions))

    # TODO
    # print_solutions needs to be altered
    # print_solutions(solution_set)


find_solutions(chosen_courses)

'''
departments = get_all_department_identifiers()
pprint(departments)

start = time.time()

course_section_data = get_course_section_data(semester, departments)
log_course_sections(course_section_data)

courses = create_course_groups(course_section_data)
log_courses(courses)

end = time.time()
print('Process 2 took {} seconds'.format(end - start))
'''


def print_all_department_enrollments(courses: [Course]) -> None:
    # TODO
    """

    :param courses:
    :return:
    """
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

