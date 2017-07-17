"""
This is the entry point to the program.
"""
import re

from requests import get
from boltons.iterutils import remap
from pprint import pprint


INTERESTED_KEYS = ['courseTitle', 'sectionId', 'sectionNumber',
                   'subjectCourse', 'timeAndLocations']
INTERESTED_TIME_KEYS = ['startTime', 'endTime', 'days']


def log_courses(courses: list):
    """
    Opens and writes to two different files.
    One for raw, comma-separated data and the other for human-readable output.
    """
    pretty_file = open('output.txt', mode='w')
    csv_file = open('raw_output.txt', mode='w')

    for course in courses:
        try:
            str = '{}:{}\t{} - {}\t\t{}'\
                .format(course['subjectCourse'],
                        course['sectionNumber'],
                        course['timeAndLocations'][0]['startTime'],
                        course['timeAndLocations'][0]['endTime'],
                        course['courseTitle'])
        except KeyError:
            """
            Some courses do not have times. We do not want to halt execution,
            just print them in a different format.
            """
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


def get_courses(id: int, subject: str):
    """
    Does all of the dirty work of grabbing course data from the API endpoint
    and cleaning it up into the format we want. The constants defined at the
    top of this module determine what JSON fields we are interested in.

    :param id:
    the sessionId of the courses (what semester/year they were offered in)
    :param subject:
    the department of the course (note: only works past the year 2007,
    or ID 1, as this is when course listings were adopted in the current format)
    :return:
    the complete list of fetched courses
    """
    def clean_and_filter_courses(courses: list):
        """
        Removes unnecessary information (namely, values that are None or
        empty lists). Also filters according to the keys we want, defined above.

        :param courses:
        the raw, unfiltered list of course data
        :return:
        a list of cleaned courses
        """
        def filter_keys(input: dict, keys: list):
            return {k: v for k, v in input.items() if k in keys}

        def filter_time_fields(input: list):
            for i in range(len(input)):
                filtered_times = list(map(lambda p:
                                          filter_keys(p, INTERESTED_TIME_KEYS),
                                          input[i]['timeAndLocations']))
                input[i]['timeAndLocations'] = filtered_times

        cleaned = remap(courses, lambda p, k, v: v is not None and v != [])
        filtered = list(map(lambda p: filter_keys(p, INTERESTED_KEYS), cleaned))
        filter_time_fields(filtered)
        return filtered

    payload = "json={{sessionId: {}, courseSubject: '{}'}}"\
        .format(str(id), subject)
    url = 'https://api.maui.uiowa.edu/maui/api/pub/registrar/sections'
    response = get(url=url, params=payload).json()
    pprint(response['payload'])
    raw_courses = response['payload']
    return clean_and_filter_courses(raw_courses)


cs_courses = get_courses(68, 'cs')
ece_courses = get_courses(68, 'ece')
math_courses = get_courses(68, 'math')

courses = cs_courses + ece_courses + math_courses
log_courses(courses)


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

'''
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


def fetch_courses(courses: list):
    """
    Fetches courses based on an input in the format `CS:2230`.
    Raises an exception if a course was not found.

    :param courses: list of courses the user wants to enroll in
    identified by their department and number
    :return: list of identified courses, or an error if one was not found
    """
    fetched_courses = []

    for course_id in courses:
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

'''
