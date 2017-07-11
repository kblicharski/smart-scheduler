"""
This is the entry point to the program.
"""
from factories import CourseFactory
from constraint import Problem


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


def fetch_courses(course_input: list):
    """
    Fetches courses based on an input in the format `CS:2230`.
    Raises an exception if a course was not found.

    :param course_input: list of courses the user wants to enroll in
    identified by their department and number
    :return: list of identified courses, or an error if one was not found
    """
    fetched_courses = []

    for course_id in course_input:
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


problem = Problem()
course_set = populate_courses()

user_input = ['CS:2230', 'CS:2210', 'MATH:3700']
invalid_user_input = ['CS:2230', 'ECE:2230']

courses = fetch_courses(user_input)
print(courses)
# print("\n".join(str(x) for x in course_set))


# This will work but then the library isn't useful anymore
for course in course_set:
    problem.addVariable(course, course.time_blocks)

# This won't work because lists aren't hashable
# problem.addVariable(list(course_set), [course.get_time_block() for course in
#                                  course_set])

"""
Essentially, here is what we want to do:

The user inputs a list of course numbers they want to enroll in.
We then fetch the list of Courses that are identified by these course numbers.
Each course will then contain the times that it is running at.

We will then add a variable for each Course in the course list, with its domain.
The domain will be the list of possible time_block values the course is
offered at.

e.g.
user_input  [2230, 2210, 2630, 4172, 3700]
(if a course with that course number does not exist, print an error)

courses     [ ... ]

We then define the Problem by adding each variable with its domain.
The variables will be the Courses, and the domain will be the
list of time_blocks associated with the Course, looking something
like this:

problem.addVariable(Course1: [12:30-13:30, 14:30-15:30, 12:00-13:00])
...
problem.addVariable(CourseN: [9:00-11:00, 12:00-14:00]

After defining these variables and their domains, all we need to do is define a
constraint for them -- this is the algorithm that the solver will use to build
the solution space.

This is the part I am really unsure of. After a cursory glance at the docs,
I am not even sure if this is what the library was intended for.
http://labix.org/doc/constraint/
"""
