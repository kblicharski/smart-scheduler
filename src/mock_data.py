"""
This file is temporary and intended for rudimentary testing of the constraint
solver that we are using.
"""
mock_courses = [
    {
        'course_name': 'Computer Science II: Data Structures',
        'course_department': 'CS',
        'course_number': 2230
    },
    {
        'course_name': 'Algorithms',
        'course_department': 'CS',
        'course_number': 3330
    },
    {
        'course_name': 'Discrete Structures',
        'course_department': 'CS',
        'course_number': 2210
    },
    {
        'course_name': 'Computer Organization',
        'course_department': 'CS',
        'course_number': 2630
    },
    {
        'course_name': 'Introduction to Software Design',
        'course_department': 'ECE',
        'course_number': 3330
    },
    {
        'course_name': 'Big Data Analytics',
        'course_department': 'IE',
        'course_number': 4172
    },
    {
        'course_name': 'Communication Networks',
        'course_department': 'ECE',
        'course_number': 3540
    },
    {
        'course_name': 'Introduction to Digital Design',
        'course_department': 'ECE',
        'course_number': 3320
    },
    {
        'course_name': 'Elementary Numerical Analysis',
        'course_department': 'MATH',
        'course_number': 3700
    }
]

# Classes generally start between 8am and 5pm,
# at either the beginning of the hour or at the 30 minute mark
mock_start_times = [
    # Hours
    [i for i in range(8, 17)],
    # Minutes
    [0, 30]
]

# Standard classes are either 50 or 75 minutes long
mock_class_durations = [50, 75]
