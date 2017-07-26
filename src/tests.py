"""
This is a placeholder for where automated unit tests will go later.
"""
from constraint import Problem

from classes import CourseSection, Course
from main import course_sections
from utils import make_section, print_solutions, get_number_of_pairs

problem = Problem()

section_type_one = [make_section(course_sections[0]),
                    make_section(course_sections[1])]

section_type_two = [make_section(course_sections[2]),
                    make_section(course_sections[6]),
                    make_section(course_sections[7])]

course_one = Course(section_type_one)
course_two = Course(section_type_two)

problem.addVariable('a', course_one.sections)
problem.addVariable('b', course_two.sections)

total_solutions = problem.getSolutions()
print('Total Pairs: {}'.format(get_number_of_pairs(total_solutions)))


# TODO: fix so it works when the a.end_time matches b.start_time or vice versa
def no_time_conflicts(a: CourseSection, b: CourseSection) -> bool:
    return (a.end_time < b.start_time or b.end_time < a.start_time) and \
           (a.end_time != b.end_time or a.start_time != b.start_time)


problem.addConstraint(no_time_conflicts, ['a', 'b'])

solution_set = problem.getSolutions()
print('Valid Pairs: {}'.format(get_number_of_pairs(solution_set)))

print_solutions(solution_set)

"""
[17:30-20:00]
[13:30-14:20]

[17:30-20:00]
[17:30-18:20]

PRESENT
[17:30-20:00]
[09:30-10:20]

PRESENT
[09:30-10:20]
[13:30-14:20]

PRESENT
[09:30-10:20]
[17:30-18:20]


[09:30-10:20]
[09:30-10:20]
"""
