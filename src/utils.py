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


def print_solutions(solution_set: [dict]) -> None:
    """
    The solution is a dictionary containing two courses
    The key is the name of the variables
    """
    for solution in solution_set:
        for key in solution:
            print_solution(solution, key)
        print('\n')


def get_number_of_pairs(solution_set: [dict]) -> int:
    return len(solution_set)


def make_section(course: dict) -> CourseSection:
    """
    Factory to create a CourseSection from JSON data.
    """
    return CourseSection(course['courseTitle'],
                         course['sectionId'],
                         course['sectionNumber'],
                         course['subjectCourse'],
                         course['timeAndLocations'])


def log_courses(course_sections: list) -> None:
    """
    Opens and writes to two different files.
    One for raw, comma-separated data and the other for human-readable output.
    """
    def course_section_with_times(course_section: dict) -> str:
        """
        This is the output format for sections with times.
        """
        return '{}:{}\t{} - {}\t\t{}' \
            .format(course_section['subjectCourse'],
                    course_section['sectionNumber'],
                    course_section['timeAndLocations'][0]['startTime'],
                    course_section['timeAndLocations'][0]['endTime'],
                    course_section['courseTitle']) + '\n'

    def course_section_without_times(course_section: dict) -> str:
        """
        Some sections do not have times.
        We do not want to halt execution, so we log them in a different format.
        """
        return '{}:{}\t\t\t\t\t\t{}' \
            .format(course_section['subjectCourse'],
                    course_section['sectionNumber'],
                    course_section['courseTitle'])

    pretty_file = open('output.txt', mode='w')
    csv_file = open('raw_output.txt', mode='w')

    for course_section in course_sections:
        try:
            file_output = course_section_with_times(course_section)
        except KeyError:
            file_output = course_section_without_times(course_section)

        pretty_file.write(file_output)

        file_output = re.sub('\t+', ',', file_output)
        file_output = re.sub(' - ', ',', file_output)
        # TODO: Find a way to separate the course number from section number
        # with a comma without removing all colons
        csv_file.write(file_output)

    pretty_file.close()
    csv_file.close()
