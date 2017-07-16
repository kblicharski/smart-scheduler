"""
This is the entry point to the program.
"""
from factories import CourseFactory
from requests import get
from boltons.iterutils import remap
from pprint import pprint


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


# this gets the information from the API endpoint
payload = "json={sessionId: 68, courseSubject: 'cs'}"
url = 'https://api.maui.uiowa.edu/maui/api/pub/registrar/sections'
response = get(url=url, params=payload)

# this is a dictionary of all CS courses being offered this fall, and metadata
json_response = response.json()

# this is the courses themselves, as a list of dictionaries
courses = json_response['payload']

# here we remove empty information
remapped = remap(courses, lambda p, k, v: v is not None and v != [])

for course in remapped:
    pprint(course['courseTitle'])

"""
Session IDs for upcoming semesters
    {
        "id": 69,
        "startDate": "2017-05-15T05:00:00.000+0000",
        "endDate": "2017-08-04T05:00:00.000+0000",
        "shortDescription": "Summer 2017",
        "legacyCode": "20171"
    },
    {
        "id": 68,
        "startDate": "2017-08-21T05:00:00.000+0000",
        "endDate": "2017-12-08T06:00:00.000+0000",
        "shortDescription": "Fall 2017",
        "legacyCode": "20173"
    },
    {
        "id": 70,
        "startDate": "2017-12-27T06:00:00.000+0000",
        "endDate": "2018-01-12T06:00:00.000+0000",
        "shortDescription": "Winter 2017",
        "legacyCode": "20175"
    },
    {
        "id": 71,
        "startDate": "2018-01-16T06:00:00.000+0000",
        "endDate": "2018-05-04T05:00:00.000+0000",
        "shortDescription": "Spring 2018",
        "legacyCode": "20178"
    },
"""
