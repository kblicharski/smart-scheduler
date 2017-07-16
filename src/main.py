"""
This is the entry point to the program.
"""
from factories import CourseFactory
from constraint import Problem

import requests


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


# print("\n".join(str(x) for x in course_set))

payload = "json={sessionId: 69, courseSubject: 'cs'}"
url = 'https://api.maui.uiowa.edu/maui/api/pub/registrar/sections'
response = requests.get(url=url, params=payload)
print(response.status_code)
print(response.url)
print(response.json())

url_2 = "https://api.maui.uiowa.edu/maui/api/pub/registrar/sections?json={sessionId: 69, courseSubject: 'cs'}&exclude={}&pageStart=0&pageSize=9999&"
other_response = requests.get(url_2)
print(other_response.status_code)
print(other_response.url)
print(response.json())

# https://api.maui.uiowa.edu/maui/api/pub/registrar/sections?json={sessionId: 69, courseSubject: 'cs'}&exclude={}&pageStart=0&pageSize=9999&
# https://api.maui.uiowa.edu/maui/api/pub/registrar/sections?sessionId=69&courseSubject=cs

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
