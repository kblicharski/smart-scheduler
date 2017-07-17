"""
This is the entry point to the program.
"""
import re

from factories import CourseFactory
from requests import get
from boltons.iterutils import remap
from pprint import pprint


INTERESTED_KEYS = ['courseTitle', 'sectionId', 'sectionNumber',
                   'subjectCourse', 'timeAndLocations']
INTERESTED_TIME_KEYS = ['startTime', 'endTime', 'days']


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


def clean_and_filter_courses(courses):
    def filter_keys(input_dict, keys):
        return {k: v for k, v in input_dict.items() if k in keys}

    def filter_time_fields(input_list):
        for i in range(len(input_list)):
            filtered_times = list(map(lambda p: filter_keys(p,
                                                            INTERESTED_TIME_KEYS),
                                      input_list[i]['timeAndLocations']))
            input_list[i]['timeAndLocations'] = filtered_times

    cleaned = remap(courses, lambda p, k, v: v is not None and v != [])
    filtered = list(map(lambda p: filter_keys(p, INTERESTED_KEYS), cleaned))
    filter_time_fields(filtered)
    return filtered


def print_and_log_courses(course_list):
    pretty_file = open('output.txt', mode='w')
    csv_file = open('raw_output.txt', mode='w')

    for course in course_list:
        try:
            str = '{}:{}\t{} - {}\t\t{}'\
                .format(course['subjectCourse'],
                        course['sectionNumber'],
                        course['timeAndLocations'][0]['startTime'],
                        course['timeAndLocations'][0]['endTime'],
                        course['courseTitle'])
        except KeyError:
            str = '{}:{}\t\t\t\t\t\t{}'\
                .format(course['subjectCourse'],
                        course['sectionNumber'],
                        course['courseTitle'])

        str += '\n'
        pretty_file.write(str)

        str = re.sub('\t+', ',', str)
        str = re.sub(' - ', ',', str)
        csv_file.write(str)

    pretty_file.close()
    csv_file.close()


# this gets the information from the API endpoint
payload = "json={sessionId: 68, courseSubject: 'cs'}"
url = 'https://api.maui.uiowa.edu/maui/api/pub/registrar/sections'
response = get(url=url, params=payload)
json_response = response.json()
raw_courses = json_response['payload']

courses = clean_and_filter_courses(raw_courses)
pprint(courses)
print_and_log_courses(courses)

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
