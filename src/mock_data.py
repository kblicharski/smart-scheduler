from classes import CourseNumber


mock_courses = [
    {
        'course_name': 'Computer Science II: Data Structures',
        'course_number': CourseNumber('CS', 2230)
    },
    {
        'course_name': 'Algorithms',
        'course_number': CourseNumber('CS', 3330)
    },
    {
        'course_name': 'Discrete Structures',
        'course_number': CourseNumber('CS', 2210)
    },
    {
        'course_name': 'Computer Organization',
        'course_number': CourseNumber('CS', 2630)
    },
    {
        'course_name': 'Introduction to Software Design',
        'course_number': CourseNumber('ECE', 3330)
    },
    {
        'course_name': 'Big Data Analytics',
        'course_number': CourseNumber('IE', 4172)
    },
    {
        'course_name': 'Communication Networks',
        'course_number': CourseNumber('ECE', 3540)
    },
    {
        'course_name': 'Introduction to Digital Design',
        'course_number': CourseNumber('ECE', 3320)
    },
    {
        'course_name': 'Elementary Numerical Analysis',
        'course_number': CourseNumber('MATH', 3700)
    }
]

mock_times = [
    # Hours
    [i for i in range(0, 23)],
    # Minutes
    [i for i in range(0, 59)]
]
