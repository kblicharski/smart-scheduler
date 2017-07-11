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

problem = Problem()
course_set = populate_courses()
print("\n".join(str(x) for x in course_set))

for course in course_set:
    problem.addVariable(course, course.time_blocks)

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
