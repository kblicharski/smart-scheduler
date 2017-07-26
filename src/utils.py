"""
This file contains helper functions used throughout the program.
"""
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
    Prints all of the solutions in the solution set.
    """
    for solution in solution_set:
        for key in solution:
            print_solution(solution, key)
        print('\n')


def get_number_of_pairs(solution_set: [dict]) -> int:
    """
    Helper function for syntactical sugar.
    """
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

    def raw_course_section(course_section: dict) -> str:
        """
        In the future, we may want to work with the raw data. Storing it in
        CSV format is the most natural solution.
        """
        return '{},{},{}' \
            .format(course_section['subjectCourse'],
                    course_section['sectionNumber'],
                    course_section['courseTitle'])

    formatted_file = open('output.txt', mode='w')
    raw_file = open('raw_output.txt', mode='w')

    for course_section in course_sections:
        try:
            formatted_output = course_section_with_times(course_section)
        except KeyError:
            formatted_output = course_section_without_times(course_section)

        raw_output = raw_course_section(course_section)

        formatted_file.write(formatted_output)
        raw_file.write(raw_output)

    formatted_file.close()
    raw_file.close()
