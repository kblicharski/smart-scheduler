"""
This file contains functions which wrap the MAUI API endpoints with Python
functions for ease of development. Long-term goals include writing a
fully-fledged API wrapper.
"""
from pprint import pprint

from requests import get
from boltons.iterutils import remap


INTERESTED_KEYS = ['courseTitle', 'sectionId', 'sectionNumber',
                   'subjectCourse', 'timeAndLocations', 'currentEnroll',
                   'maxEnroll',
                   'sectionType']
INTERESTED_TIME_KEYS = ['startTime', 'endTime', 'days']


def filter_keys(input: dict, keys: list):
    return {k: v for k, v in input.items() if k in keys}


def clean_and_filter_courses(courses: list):
    """
    Removes unnecessary information (namely, values that are None or
    empty lists).
    Also filters according to the keys we want, defined above.

    :param courses:
    the raw, unfiltered list of course data
    :return:
    a list of cleaned courses
    """
    def filter_time_fields(input: list):
        for i in range(len(input)):
            filtered_times = list(map(lambda p:
                                      filter_keys(p, INTERESTED_TIME_KEYS),
                                      input[i]['timeAndLocations']))
            input[i]['timeAndLocations'] = filtered_times

    cleaned = remap(courses,
                    lambda p, k, v: v is not None and v != [] and v != '' and
                    v != [{}] and v != {})
    filtered = list(map(lambda p: filter_keys(p, INTERESTED_KEYS),
                        cleaned))
    filter_time_fields(filtered)
    return filtered


def get_course_sections(id: int, subject: str, count=None) -> [dict]:
    """
    Does all of the dirty work of grabbing CourseSection data from the API
    endpoint and cleaning it up into the format we want. The constants
    defined at the top of this module determine what JSON fields we are
    interested in.

    :param id:
    the sessionId of the courses (what semester/year they were offered in)
    :param subject:
    the department of the course (note: only works past the year 2007,
    as this is when course listings were adopted in the current format)
    :param count:
    optional argument to determine how many sections we return
    :return:
    the list of fetched course sections
    """
    url = 'https://api.maui.uiowa.edu/maui/api/pub/registrar/sections'
    payload = "json={{sessionId: {}, courseSubject: '{}'}}".format(str(id),
                                                                   subject)
    response = get(url=url, params=payload)

    if response.status_code != 200:
        print('ERROR: HTTP{}'.format(response.status_code))
        raise ValueError

    data = response.json()
    raw_courses = data['payload']

    if count:
        return clean_and_filter_courses(raw_courses)[0:count]
    return clean_and_filter_courses(raw_courses)


def get_all_department_identifiers() -> [dict]:
    """
    """
    url = 'https://api.maui.uiowa.edu/maui/api/pub/registrar/program-of' \
        '-study/program'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json'}
    response = get(url=url, headers=headers)

    if response.status_code != 200:
        print('ERROR: HTTP{}'.format(response.status_code))
        raise ValueError

    data = response.json()
    cleaned = remap(data,
                    lambda p, k, v: v is not None and v != [] and v != '' and
                    v != [{}] and v != {})
    filtered = list(map(lambda p: filter_keys(p, ['academicUnit']), cleaned))
    filtered = list(map(lambda p: p['academicUnit'], filtered))
    departments = list(map(lambda p: filter_keys(p, ['naturalKey']), filtered))
    departments = list(map(lambda p: p['naturalKey'], departments))
    pprint(departments)
    departments = list(sorted(list(set(departments))))

    new_filtered = []
    for item in departments:
        if len(item) > 1:
            new_filtered.append(item)

    return new_filtered
