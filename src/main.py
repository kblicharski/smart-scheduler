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
    pretty_file = open('output.txt', mode='w')
    csv_file = open('raw_output.txt', mode='w')

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


problem = Problem()

course1 = [make_course(courses[0]),
           make_course(courses[1])]

course2 = [make_course(courses[2]),
           make_course(courses[6]),
           make_course(courses[7])]

print('First Year Seminar')
for section in course1:
    print('{} - {}'.format(section.section_number, section.time_block))

print('Principles of Computing')
for section in course2:
    print('{} - {}'.format(section.section_number, section.time_block))


problem.addVariable('a', course1)
problem.addVariable('b', course2)

# Pairs
'''
present
[17:30-20:00]
[13:30-14:20]

[17:30-20:00]
[17:30-18:20]

present
[17:30-20:00]
[09:30-10:20]

present
[09:30-10:20]
[13:30-14:20]

present
[09:30-10:20]
[17:30-18:20]

present
[09:30-10:20]
[09:30-10:20]
'''


def no_time_conflicts(a: CourseSection, b: CourseSection):
    return a.end_time <= b.start_time and b.end_time <= a.start_time

total_solutions = problem.getSolutions()
print('Total Pairs: ' + str(len(total_solutions)))

problem.addConstraint(no_time_conflicts, ['a', 'b'])

solution_set = problem.getSolutions()
print('Valid Pairs: ' + str(len(solution_set)))

# the solution is a dictionary containing two courses that form a valid solution
for solution in solution_set:
    # the key is the name of the variables
    for key in solution:
        print(solution[key])
        print(solution[key].time_block)
    print('\n')

'''
def populate_courses():
    """
    Populates the list of courses from mock data.
    """
    i = 0
    courses = set()
    course_names = set()
    factory = CourseFactory()

    while i < factory.number_of_courses:
        course = factory.get_course()

        # If it's a unique course, add it
        if course.name not in course_names:
            courses.add(course)
            course_names.add(course.name)
            i += 1

    return courses


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
