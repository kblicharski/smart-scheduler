"""
This file contains helper functions used throughout the program.
"""
from itertools import groupby
from operator import itemgetter

from classes import CourseSection, Course


def print_solution(solution: dict, key: str) -> None:
    """
    Prints a solution in a human-readable format.
    """
    print('{}:{} - {}'.format(solution[key].subject_course,
                              solution[key].section_number,
                              solution[key].time_block))


def print_solutions(solution_set) -> None:
    """
    Prints all of the solutions in the solution set.
    """
    for solution in solution_set:
        for key in solution:
            print_solution(solution, key)
        print('\n')


def get_number_of_solutions(solution_set) -> int:
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
                         course['timeAndLocations'],
                         course['currentEnroll'],
                         course['maxEnroll'],
                         course['sectionType'])


def log_course_sections(course_sections: [dict]) -> None:
    """
    Opens and writes to two different files.
    One for raw, comma-separated data and the other for human-readable output.
    """
    def course_section_with_times(course_section: dict) -> str:
        """
        This is the output format for sections with times.
        """

        return ('{}:{}\t{}/{}\t\t{} - {}\t\t{}\t\t{}'
                .format(course_section['subjectCourse'],
                        course_section['sectionNumber'],
                        course_section['currentEnroll'],
                        course_section['maxEnroll'],
                        course_section['timeAndLocations'][0]['startTime'],
                        course_section['timeAndLocations'][0]['endTime'],
                        course_section['sectionType'],
                        course_section['courseTitle']) + '\n')

    def course_section_without_times(course_section: dict) -> str:
        """
        Some sections do not have times.
        We do not want to halt execution, so we log them in a different format.
        """

        return ('{}:{}\t{}/{}\t{}\t\t\t\t\t\t{}'
                .format(course_section['subjectCourse'],
                        course_section['sectionNumber'],
                        course_section['currentEnroll'],
                        course_section['maxEnroll'],
                        course_section['sectionType'],
                        course_section['courseTitle']) + '\n')

    def raw_course_section(course_section: dict) -> str:
        """
        In the future, we may want to work with the raw data. Storing it in
        CSV format is the most natural solution.
        """

        return ('{},{},{},{},{},{}'
                .format(course_section['subjectCourse'],
                        course_section['sectionNumber'],
                        course_section['currentEnroll'],
                        course_section['maxEnroll'],
                        course_section['sectionType'],
                        course_section['courseTitle']) + '\n')

    formatted_file = open('all_sections_formatted.txt', mode='w')
    raw_file = open('all_sections_raw.txt', mode='w')

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


def log_courses(courses: [Course]) -> None:
    # TODO (docs)
    """
    """
    def course_formatted(course: Course) -> str:
        # TODO (docs)
        """
        """
        time_block_output = []

        count = 0
        for block in course.time_blocks:
            time_block_output.append(str(block).replace("'", ""))
            count += 1

            if count == 4:
                time_block_output.append('\n')
                count = 0

        time_block_output = ' '.join(time_block_output)

        output = ('{}\t{}\t{}/{}\n {}\n\n\n'.format(course.subject_course,
                                                    course.course_title,
                                                    course.enrolled_students,
                                                    course.max_students,
                                                    time_block_output))
        return output

    def course_raw(course: Course) -> str:
        # TODO (docs)
        """
        """
        # TODO: clean up this logic
        return ('{},{},{},{},{}\n'.format(course.subject_course,
                                          course.course_title,
                                          course.enrolled_students,
                                          course.max_students,
                                          ', '.join([str(block) for block in
                                                     course.time_blocks])))

    formatted_file = open('all_courses_formatted.txt', mode='w')
    raw_file = open('all_courses_raw.txt', mode='w')

    for course in courses:
        formatted_output = course_formatted(course)
        raw_output = course_raw(course)

        formatted_file.write(formatted_output)
        raw_file.write(raw_output)

    formatted_file.close()
    raw_file.close()


def create_course_groups(course_section_data: [dict]) -> [Course]:
    # TODO (docs)
    """
    :param course_section_data:
    :return:
    """
    course_section_data = sorted(course_section_data,
                                 key=itemgetter('subjectCourse'))

    courses = []
    for key, values in groupby(course_section_data,
                               key=itemgetter('subjectCourse')):
        values = list(values)
        sections = []
        for value in values:
            sections.append(make_section(value))
        courses.append(Course(sections))

    return courses
