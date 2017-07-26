"""
This file contains helper functions used throughout the program.
"""
import re
from classes import CourseSection


def print_solution(solution: dict, key: str) -> None:
    """
    Prints a solution in a human-readable format.
    """
    print('{}:{} - {}'.format(solution[key].subject_course,
                              solution[key].section_number,
                              solution[key].time_block))


def make_course(course: dict) -> CourseSection:
    """
    Factory to create a CourseSection from JSON data.
    """
    return CourseSection(course['courseTitle'],
                         course['sectionId'],
                         course['sectionNumber'],
                         course['subjectCourse'],
                         course['timeAndLocations'])


def log_courses(courses: list) -> None:
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


