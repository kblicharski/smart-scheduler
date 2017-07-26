"""
This is a placeholder for where automated unit tests will go.
It currently contains some of the manual tests I have done which should be
compiled into coherent test suites.
"""
from constraint import Problem

from classes import CourseSection
from main import courses
from utils import print_solution, make_course

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

'''
PRESENT
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
'''


# will not work when the a.end_time matches b.start_time or vice versa
def no_time_conflicts(a: CourseSection, b: CourseSection):
    return (a.end_time < b.start_time or b.end_time < a.start_time) and \
           (a.end_time != b.end_time or a.start_time != b.start_time)


total_solutions = problem.getSolutions()
print('Total Pairs: ' + str(len(total_solutions)))

problem.addConstraint(no_time_conflicts, ['a', 'b'])

solution_set = problem.getSolutions()
print('Valid Pairs: ' + str(len(solution_set)))

# the solution is a dictionary containing two courses
for solution in solution_set:
    # the key is the name of the variables
    for key in solution:
        print_solution(solution, key)
    print('\n')
